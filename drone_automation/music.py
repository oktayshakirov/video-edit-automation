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

from dataclasses import dataclass
from pathlib import Path

import librosa
import numpy as np

from .config import (
    BARS_PER_SECTION,
    BEATS_PER_BAR,
    DOWNBEAT_FMAX,
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

    def bar_time(self, n: int) -> float:
        """Closed form, so error never accumulates."""
        return self.grid_phase + self.bar_period * n


def _fit_beat_grid(beat_times: np.ndarray, period_hint: float) -> tuple[float, float]:
    """Least-squares fit of a regular grid to detected beats.

    Detected beats may be missing or doubled, so each beat is first assigned an
    integer index against the hint, then phase and period are refit. Two passes
    is enough to settle.
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
    bpm, beat_frames = librosa.beat.beat_track(
        onset_envelope=onset_env, sr=sr, hop_length=HOP, units="frames"
    )
    bpm = float(np.atleast_1d(bpm)[0])
    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=HOP)
    if len(beat_times) < 8:
        raise RuntimeError(f"only {len(beat_times)} beats detected — track too short or too quiet")

    beat_phase, beat_period = _fit_beat_grid(beat_times, 60.0 / bpm)
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
    bars = t.grid_phase + t.bar_period * np.arange(t.n_bars)
    beats = t.grid_phase + t.beat_period * np.arange(t.n_bars * BEATS_PER_BAR)
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
