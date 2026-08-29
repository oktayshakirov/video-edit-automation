"""Phase 2 — music analysis.

Produces a bar grid of legal cut points plus an energy envelope.

Two decisions here matter more than the rest:

1. The bar grid is a *fitted regular grid*, not librosa's raw beat times.
   librosa reports where it thinks each beat landed, and those wobble by tens
   of milliseconds. Produced music is metronomic, so a least-squares fit of
   (phase, period) over the detected beats is both more accurate and — more
   importantly — non-accumulating. Every bar line is computed from the closed
   form `phase + period * n`, so rounding error stays bounded at half a frame
   instead of compounding over four minutes.

2. Downbeat phase is voted using onset strength restricted to the low band.
   A full-band vote picks the snare (beats 2 and 4 in most produced music),
   which puts every cut on the backbeat and is exactly the "amateur" failure
   mode. The kick carries the downbeat, so we look below DOWNBEAT_FMAX.
   This is a heuristic and it is the weakest link in the pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import librosa
import numpy as np

from .config import (
    BARS_PER_SECTION,
    BEATS_PER_BAR,
    BPM_SEARCH_HI,
    BPM_SEARCH_LO,
    DOWNBEAT_FMAX,
    GRID_PHASE_NUDGE,
    HOP,
    PHRASE_BARS,
    SNAP_SECTIONS_TO_PHRASE,
    SR,
)


@dataclass
class Section:
    start_bar: int
    end_bar: int          # exclusive
    energy: float         # 0..1, normalised within this track
    label: str            # calm / build / peak

    @property
    def bars(self) -> int:
        return self.end_bar - self.start_bar


@dataclass
class LoopPlan:
    """Where a second pass of the track takes over from the first."""
    handoff_bar: int       # timeline bar at which pass 2 has fully taken over
    return_bar: int        # bar of the source that pass 2 re-enters at
    crossfade_bars: int


@dataclass
class Movement:
    """One song inside a medley, placed on the timeline's bar grid.

    `start_bar` is the timeline bar the song takes over at, `bars` how many
    timeline bars it holds. `track` is the song's own analysed Track, which may
    itself carry a LoopPlan — a movement can be an already-extended song.
    """
    track: "Track"
    start_bar: int
    bars: int
    start_time: float      # absolute timeline seconds of `start_bar`

    @property
    def end_bar(self) -> int:
        return self.start_bar + self.bars


@dataclass
class Track:
    path: Path
    duration: float
    bpm: float
    beat_period: float    # seconds per beat
    bar_period: float     # seconds per bar
    grid_phase: float     # absolute time of bar 0
    n_bars: int
    bar_energy: np.ndarray   # normalised 0..1, one value per bar
    sections: list[Section]
    downbeat_confidence: float
    intro_bars: int       # bars extrapolated backwards before the first detected beat
    grid_score: float = 0.0        # onset strength on the chosen grid
    grid_octaves: dict = field(default_factory=dict)   # half/double, for comparison
    source_bars: int = 0           # bars in one pass of the audio
    loop: "LoopPlan | None" = None
    # Set only on a medley. Two songs rarely share a tempo, so the bar grid
    # stops being one closed form and becomes piecewise — one linear grid per
    # movement. Empty for an ordinary single-song track, where the closed form
    # below is exact and error still cannot accumulate.
    movements: list["Movement"] = field(default_factory=list)

    def _movement_at_bar(self, n: int) -> "Movement | None":
        if not self.movements:
            return None
        for m in self.movements:
            if n < m.end_bar:
                return m
        return self.movements[-1]

    def bar_time(self, n: int) -> float:
        """Closed form, so error never accumulates.

        On a medley the closed form is per movement: the grid restarts at each
        song's own bar length, anchored to where that song took over. Error
        stays bounded inside a movement instead of compounding across the seam.
        """
        m = self._movement_at_bar(n)
        if m is None:
            return self.grid_phase + self.bar_period * n
        return m.start_time + m.track.bar_period * (n - m.start_bar)

    def beat_time(self, n: int) -> float:
        """Closed form in beats — the finer grid, for sub-bar cutting."""
        if not self.movements:
            return self.grid_phase + self.beat_period * n
        m = self._movement_at_bar(n // BEATS_PER_BAR)
        assert m is not None
        return (m.start_time
                + m.track.beat_period * (n - m.start_bar * BEATS_PER_BAR))

    def source_bar(self, n: int) -> int:
        """Timeline bar -> which bar of the audio actually plays there."""
        if self.loop is None or n < self.loop.handoff_bar:
            return n
        return self.loop.return_bar + (n - self.loop.handoff_bar)


def _fit_beat_grid(beat_times: np.ndarray, period_hint: float) -> tuple[float, float]:
    """Least-squares fit of a regular grid to detected beats.

    Detected beats may be missing or doubled, so each beat is first assigned an
    integer index against the hint, then phase and period are refit. Two passes
    is enough to settle.

    Only used to polish a grid that `_search_beat_grid` has already located.
    Run against librosa's raw beat times it silently fits noise — see there.
    """
    phase, period = float(beat_times[0]), float(period_hint)
    for _ in range(3):
        n = np.round((beat_times - phase) / period)
        # Drop duplicates from doubled detections
        _, keep = np.unique(n, return_index=True)
        n_u, t_u = n[keep], beat_times[keep]
        A = np.vstack([n_u, np.ones_like(n_u)]).T
        period, phase = np.linalg.lstsq(A, t_u, rcond=None)[0]
    return float(phase), float(period)


def _grid_score(onset_z: np.ndarray, sr: int, duration: float,
                period: float, phase: float) -> float:
    """Mean normalised onset strength sampled on a (phase, period) grid."""
    t = np.arange(phase, duration - 0.05, period)
    if len(t) < 8:
        return -np.inf
    frames = np.clip(librosa.time_to_frames(t, sr=sr, hop_length=HOP),
                     0, len(onset_z) - 1)
    return float(onset_z[frames].mean())


def _search_beat_grid(onset_env: np.ndarray, sr: int, duration: float
                      ) -> tuple[float, float, dict]:
    """Locate the beat grid by direct search over (period, phase).

    This replaced trusting `librosa.beat.beat_track`'s tempo, which on the first
    real track outside Plovdiv returned 152.11 BPM for a 75.00 BPM song. The
    least-squares fit downstream then happily fitted a regular grid to those
    wrong beat times and reported a clean-looking result: mean residual 95 ms on
    a 394 ms beat, off-beat onset strength *higher* than on-beat. Nothing in the
    old path could notice, because it never asked whether the grid it produced
    actually landed on the music. This does ask — the score is exactly that
    question — so a wrong tempo now loses to the right one by a factor of 280
    instead of passing silently.

    Octave ambiguity is left to the score rather than to a prior. A tempo prior
    centred near 120 BPM would have picked the 150 BPM double here and been
    wrong; the half and double of the winner are reported so the choice is
    visible instead of implicit.
    """
    onset_z = (onset_env - onset_env.mean()) / (onset_env.std() + 1e-9)

    def best_phase(period: float, step: float, around: float | None = None,
                   span: float | None = None) -> tuple[float, float]:
        if around is None:
            phases = np.arange(0.0, period, step)
        else:
            phases = np.arange(around - span, around + span, step) % period
        scored = [(_grid_score(onset_z, sr, duration, period, ph), ph)
                  for ph in phases]
        return max(scored)

    # Coarse sweep, then refine tempo and phase around the winner.
    coarse = [(*best_phase(60.0 / bpm, 0.010), bpm)
              for bpm in np.arange(BPM_SEARCH_LO, BPM_SEARCH_HI, 0.5)]
    coarse.sort(reverse=True)
    _, _, bpm0 = coarse[0]

    fine = [(*best_phase(60.0 / bpm, 0.005), bpm)
            for bpm in np.arange(bpm0 - 0.6, bpm0 + 0.6, 0.02)]
    fine.sort(reverse=True)
    score, phase, bpm = fine[0]
    period = 60.0 / bpm

    octaves = {}
    for label, factor in (("half", 0.5), ("double", 2.0)):
        p = period / factor
        if BPM_SEARCH_LO <= 60.0 / p <= BPM_SEARCH_HI:
            octaves[label] = (60.0 / p, best_phase(p, 0.005)[0])

    return float(phase), float(period), {"score": score, "octaves": octaves}


def _downbeat_phase(y, sr, phase, period, n_beats) -> tuple[int, float]:
    """Which beat-of-bar carries the kick. Returns (phase, confidence)."""
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, hop_length=HOP, fmax=DOWNBEAT_FMAX, n_mels=16
    )
    low_onset = librosa.onset.onset_strength(S=librosa.power_to_db(mel), sr=sr, hop_length=HOP)

    beat_n = np.arange(n_beats)
    beat_t = phase + period * beat_n
    frames = np.clip(librosa.time_to_frames(beat_t, sr=sr, hop_length=HOP),
                     0, len(low_onset) - 1)
    strength = low_onset[frames]

    scores = np.array([
        strength[beat_n % BEATS_PER_BAR == p].mean() for p in range(BEATS_PER_BAR)
    ])
    best = int(np.argmax(scores))
    # Confidence: how far the winner stands above the runner-up, 0..1
    ordered = np.sort(scores)[::-1]
    spread = ordered[0] - ordered[1]
    conf = float(spread / (abs(ordered[0]) + 1e-9)) if ordered[0] != 0 else 0.0
    return best, min(max(conf, 0.0), 1.0)


def _sections(bar_energy: np.ndarray, n_bars: int) -> list[Section]:
    """Split the bar grid into structural sections and label by energy.

    Boundaries come from changes in the energy contour rather than from
    timbre-based segmentation: for the edit engine, what matters is where the
    track gets louder or quieter, not where the instrumentation changes.
    """
    k = max(2, min(n_bars // BARS_PER_SECTION, 12))
    edges = np.linspace(0, n_bars, k + 1).round().astype(int)

    # Snap interior boundaries onto phrase lines. Slots restart at every section
    # boundary, so a boundary landing off-phrase (bar 25, bar 49...) throws every
    # cut after it a full bar out of step with the music and stays wrong for the
    # rest of the track. Music changes on phrase lines; sections must too.
    if SNAP_SECTIONS_TO_PHRASE:
        edges = np.array(
            [0]
            + [int(round(e / PHRASE_BARS)) * PHRASE_BARS for e in edges[1:-1]]
            + [n_bars]
        )
    edges = np.unique(np.clip(edges, 0, n_bars))

    # Merge neighbouring blocks whose energy is close, so a flat track doesn't
    # get split into identical-looking sections.
    raw = []
    for a, b in zip(edges[:-1], edges[1:]):
        if b > a:
            raw.append([int(a), int(b), float(bar_energy[a:b].mean())])

    merged: list[list] = []
    for blk in raw:
        if merged and abs(blk[2] - merged[-1][2]) < 0.08:
            merged[-1][1] = blk[1]
            span = blk[1] - merged[-1][0]
            merged[-1][2] = float(bar_energy[merged[-1][0]:blk[1]].mean()) if span else blk[2]
        else:
            merged.append(blk)

    out = []
    for a, b, e in merged:
        label = "calm" if e < 0.34 else ("build" if e < 0.67 else "peak")
        out.append(Section(start_bar=a, end_bar=b, energy=e, label=label))
    return out


def analyze_track(path: Path) -> Track:
    y, sr = librosa.load(str(path), sr=SR, mono=True)
    duration = float(len(y) / sr)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=HOP)

    # Search for the grid rather than trusting librosa's tempo. See
    # _search_beat_grid for why: the reported tempo can be an unrelated number
    # and every downstream check still looks healthy.
    beat_phase, beat_period, grid_info = _search_beat_grid(onset_env, sr, duration)

    # Polish the phase against detected beats that already sit near this grid.
    # Beats far from it are the doubled/spurious detections that misled the old
    # path, so they are excluded rather than fitted.
    beat_frames = librosa.beat.beat_track(
        onset_envelope=onset_env, sr=sr, hop_length=HOP, units="frames")[1]
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=HOP)
    resid = (beat_times - beat_phase + beat_period / 2) % beat_period - beat_period / 2
    near = beat_times[np.abs(resid) < beat_period * 0.15]
    if len(near) >= 8:
        beat_phase, beat_period = _fit_beat_grid(near, beat_period)
    fitted_bpm = 60.0 / beat_period

    n_beats = int((duration - beat_phase) / beat_period)
    db_phase, db_conf = _downbeat_phase(y, sr, beat_phase, beat_period, n_beats)

    # Bar 0 starts at the first downbeat at or after the fitted phase.
    grid_phase = beat_phase + beat_period * db_phase
    bar_period = beat_period * BEATS_PER_BAR

    # Extrapolate the grid backwards over the intro. Beat tracking does not lock
    # until the drums enter, so without this the whole intro falls outside the
    # grid and gets no cuts — which is precisely where the longest, calmest shot
    # belongs. ASSUMPTION: the intro shares the tempo of the body. True for
    # produced music, false for a rubato or ambient intro; if the opening cuts
    # feel loose, this is the line to suspect.
    bars_back = int(grid_phase // bar_period)
    grid_phase -= bars_back * bar_period
    intro_bars = bars_back

    # Hand correction, applied last so it is exactly what was dialled in by ear
    # and not something the extrapolation above then re-rounds.
    grid_phase += GRID_PHASE_NUDGE

    n_bars = int((duration - grid_phase) / bar_period)

    # --- energy envelope, sampled per bar ---
    rms = librosa.feature.rms(y=y, hop_length=HOP)[0]
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)
    bar_starts = grid_phase + bar_period * np.arange(n_bars)
    bar_frames = np.clip(librosa.time_to_frames(bar_starts, sr=sr, hop_length=HOP),
                         0, len(rms_db) - 1)
    bar_frames_end = np.clip(
        librosa.time_to_frames(bar_starts + bar_period, sr=sr, hop_length=HOP),
        0, len(rms_db) - 1)
    bar_energy_db = np.array([
        rms_db[a:max(b, a + 1)].mean() for a, b in zip(bar_frames, bar_frames_end)
    ])

    lo, hi = np.percentile(bar_energy_db, 5), np.percentile(bar_energy_db, 95)
    bar_energy = np.clip((bar_energy_db - lo) / max(hi - lo, 1e-9), 0.0, 1.0)

    return Track(
        path=path,
        duration=duration,
        bpm=fitted_bpm,
        beat_period=beat_period,
        bar_period=bar_period,
        grid_phase=grid_phase,
        n_bars=n_bars,
        bar_energy=bar_energy,
        sections=_sections(bar_energy, n_bars),
        downbeat_confidence=db_conf,
        intro_bars=intro_bars,
        grid_score=grid_info["score"],
        grid_octaves=grid_info["octaves"],
        source_bars=n_bars,
    )


def extend_with_loop(t: Track, handoff_bar: int, return_bar: int,
                     crossfade_bars: int) -> Track:
    """Play the track a second time so the picture can run past its length.

    The song hands off at `handoff_bar` and re-enters at `return_bar`, both
    counted in bars of the source. Because every bar is the same length, the
    timeline grid continues unbroken across the splice — `bar_time` stays the
    same closed form and no cut after the loop point moves off the beat.

    Both bars must be phrase-aligned and should sit in sections of similar
    energy: the splice is audible in proportion to how far the arrangement jumps
    across it, not to the crossfade length. The crossfade only hides the seam in
    the mix; it cannot hide a drop landing on an intro.
    """
    if not 0 < return_bar < handoff_bar <= t.source_bars:
        raise ValueError(
            f"loop needs 0 < return_bar ({return_bar}) < handoff_bar "
            f"({handoff_bar}) <= {t.source_bars}")

    tail_bars = t.source_bars - return_bar
    n_bars = handoff_bar + tail_bars

    # Timeline bar -> source bar, and the energy contour that follows from it.
    src_of = np.array([n if n < handoff_bar else return_bar + (n - handoff_bar)
                       for n in range(n_bars)])
    bar_energy = t.bar_energy[np.clip(src_of, 0, len(t.bar_energy) - 1)]

    return Track(
        path=t.path,
        duration=t.grid_phase + t.bar_period * n_bars,
        bpm=t.bpm,
        beat_period=t.beat_period,
        bar_period=t.bar_period,
        grid_phase=t.grid_phase,
        n_bars=n_bars,
        bar_energy=bar_energy,
        sections=_sections(bar_energy, n_bars),
        downbeat_confidence=t.downbeat_confidence,
        intro_bars=t.intro_bars,
        grid_score=t.grid_score,
        grid_octaves=t.grid_octaves,
        source_bars=t.source_bars,
        loop=LoopPlan(handoff_bar=handoff_bar, return_bar=return_bar,
                      crossfade_bars=crossfade_bars),
    )


def concat_tracks(tracks: list[Track], crossfade_bars: int = 2,
                  hold_bars: list[int | None] | None = None) -> Track:
    """Play several songs in sequence as one timeline — a medley.

    This is not `extend_with_loop`. That one replays a single song to give the
    footage room; this joins *different* songs, which is a different problem in
    one specific way: they do not share a tempo. A single `bar_period` cannot
    describe the result, so the grid becomes piecewise (see `Track.bar_time`)
    and every cut still lands on a real bar line of whichever song is playing.

    `hold_bars[i]` truncates song i to that many bars — use it to leave on a
    phrase line rather than at whatever bar the analysis happened to end on.
    None keeps the whole song.

    The seam is a crossfade of `crossfade_bars`, measured in the *outgoing*
    song's bars. As with a loop, the crossfade hides a level change and nothing
    else: it cannot make a full-energy outro flow into a full-energy intro. Pick
    the join by energy — a song ending calm into a song opening calm is what
    makes a medley read as one piece of music rather than as a playlist.
    """
    if not tracks:
        raise ValueError("concat_tracks needs at least one track")
    if len(tracks) == 1:
        return tracks[0]

    holds = list(hold_bars or [None] * len(tracks))
    if len(holds) != len(tracks):
        raise ValueError("hold_bars must have one entry per track")

    movements: list[Movement] = []
    energies: list[np.ndarray] = []
    sections: list[Section] = []
    bar_cursor, time_cursor = 0, tracks[0].grid_phase

    for t, hold in zip(tracks, holds):
        # 0 as well as None means "keep the whole song": TOML has no null, so a
        # project file cannot write None into this list.
        bars = t.n_bars if not hold else min(int(hold), t.n_bars)
        if bars <= 0:
            raise ValueError(f"{t.path.name}: hold_bars leaves no bars")

        movements.append(Movement(track=t, start_bar=bar_cursor, bars=bars,
                                  start_time=time_cursor))
        energies.append(t.bar_energy[:bars])

        # Sections carry over shifted, clipped to the held length, so the edit
        # engine still sees each song's own calm/build/peak structure.
        for s in t.sections:
            a, b = min(s.start_bar, bars), min(s.end_bar, bars)
            if b > a:
                sections.append(Section(start_bar=a + bar_cursor,
                                        end_bar=b + bar_cursor,
                                        energy=s.energy, label=s.label))

        bar_cursor += bars
        time_cursor += t.bar_period * bars

    first = tracks[0]
    total_bars = bar_cursor
    # A representative bar length, used only where a single number is needed to
    # judge whether a slot length is legal (MAX_SHOT_SECONDS). The longest bar
    # is the conservative choice: it never lets through a slot that would run
    # over the ceiling in the slower song.
    rep_bar = max(m.track.bar_period for m in movements)

    return Track(
        path=first.path,
        duration=time_cursor,
        bpm=first.bpm,
        beat_period=rep_bar / BEATS_PER_BAR,
        bar_period=rep_bar,
        grid_phase=first.grid_phase,
        n_bars=total_bars,
        bar_energy=np.concatenate(energies),
        sections=sections,
        downbeat_confidence=min(t.downbeat_confidence for t in tracks),
        intro_bars=first.intro_bars,
        grid_score=min(t.grid_score for t in tracks),
        source_bars=total_bars,
        movements=movements,
    )


def write_click_track(t: Track, out: Path) -> Path:
    """Mix the track against clicks on every bar line.

    Downbeat phase is the weakest inference in the pipeline — a full-band vote
    lands on the snare and puts every cut on the backbeat. This makes that
    failure audible in ten seconds instead of leaving it to be felt as "the
    edit is somehow off" after a full FCP import.

    High click = bar 1, low click = the other beats.
    """
    import soundfile as sf

    y, sr = librosa.load(str(t.path), sr=SR, mono=True)
    # The grid may run past the audio when the track is looped; clicks only
    # exist for bars that are actually in the file.
    audible = t.source_bars or t.n_bars
    bars = t.grid_phase + t.bar_period * np.arange(audible)
    beats = t.grid_phase + t.beat_period * np.arange(audible * BEATS_PER_BAR)
    beats = beats[beats < len(y) / sr - 0.05]
    bars = bars[bars < len(y) / sr - 0.05]
    offbeats = np.array([b for i, b in enumerate(beats) if i % BEATS_PER_BAR != 0])

    downs = librosa.clicks(times=bars, sr=sr, length=len(y), click_freq=1600.0)
    others = librosa.clicks(times=offbeats, sr=sr, length=len(y), click_freq=700.0)

    mix = 0.6 * y + 0.9 * downs + 0.3 * others
    peak = np.max(np.abs(mix))
    if peak > 0:
        mix = mix / peak * 0.95
    sf.write(str(out), mix, sr)
    return out


def describe(t: Track) -> str:
    lines = [
        f"{t.path.name}",
        f"  {t.duration:.1f}s   {t.bpm:.2f} BPM   bar = {t.bar_period:.3f}s   "
        f"{t.n_bars} bars   first downbeat @ {t.grid_phase:.3f}s",
        f"  downbeat confidence {t.downbeat_confidence:.2f}"
        f"{'  <-- LOW, check the grid by ear' if t.downbeat_confidence < 0.15 else ''}"
        f"   ({t.intro_bars} intro bars extrapolated)",
    ]
    if t.grid_octaves:
        alt = "  ".join(f"{k} {bpm:.2f} BPM scores {s:.2f}"
                        for k, (bpm, s) in t.grid_octaves.items())
        lines.append(f"  grid score {t.grid_score:.2f}   (vs {alt})")
    for m in t.movements:
        lines.append(
            f"  MOVEMENT: {m.track.path.name}  bars {m.start_bar}-{m.end_bar} "
            f"({m.start_time:.1f}-{m.start_time + m.track.bar_period * m.bars:.1f}s)  "
            f"{m.track.bpm:.2f} BPM   bar = {m.track.bar_period:.3f}s"
            f"{'   [looped]' if m.track.loop else ''}")
    if t.loop:
        lp = t.loop
        lines.append(
            f"  LOOPED: pass 2 re-enters at bar {lp.return_bar} "
            f"({t.grid_phase + t.bar_period * lp.return_bar:.1f}s of the song) "
            f"under a {lp.crossfade_bars}-bar crossfade ending at "
            f"{t.bar_time(lp.handoff_bar):.1f}s"
            f"  —  {t.source_bars} source bars -> {t.n_bars} timeline bars")
    lines += [
        "",
        f"  {'section':<10} {'bars':>10} {'time':>16} {'energy':>7}",
    ]
    for s in t.sections:
        lines.append(
            f"  {s.label:<10} {f'{s.start_bar}-{s.end_bar}':>10} "
            f"{f'{t.bar_time(s.start_bar):.1f}-{t.bar_time(s.end_bar):.1f}s':>16} "
            f"{s.energy:>7.2f}"
        )
    return "\n".join(lines)
