"""Phase 3 — edit decision engine.

Works backwards from the usual approach. Instead of imposing a duration grid
and hunting for footage to fill it, each slot chooses a (clip, length) pair
jointly: the length is whatever legal bar count the chosen clip can actually
deliver, biased toward the section's preferred length. Shot rhythm therefore
varies naturally with what the library holds, and a select is never asked to
be longer than it is.

Frame snapping: every timeline boundary is computed independently from the
closed-form bar time and then rounded once. Adjacent clips share a boundary
exactly, so there are no gaps and no accumulating drift — the error at bar 90
is the same half-frame as at bar 1.
"""

from __future__ import annotations

import math
import sqlite3
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .config import (
    ALLOW_RAMPS,
    ALLOW_SPEEDUP,
    AUTO_REVERSE,
    HEAD_TRIM,
    PENALTY_SPEEDUP_WHEN_CALM,
    RAMP_END_SPEED,
    SPEED_CHOICES,
    SPEEDUP_MIN_REMAINING,
    W_BITE,
    W_COVERAGE,
    W_PUNCH,
    MAX_USES_BY_MOVE,
    MAX_USES_DEFAULT,
    MIN_SLOT_BARS_BY_MOVE,
    RAMP_MIN_BARS,
    REVERSIBLE_MOVES,
    HUE_CLOSE_DEG,
    LEGAL_SLOT_BARS,
    MAX_SHOT_SECONDS,
    MIN_TAIL_MARGIN,
    PENALTY_CLOSE_HUE,
    PENALTY_OVERUSE,
    PENALTY_REUSE,
    PENALTY_SAME_GROUP,
    PENALTY_SAME_MOVE,
    PHRASE_ACCENT_MULTIPLIER,
    PHRASE_BARS,
    REUSE_COOLDOWN_SLOTS,
    REUSE_RECENCY_WINDOW,
    SLOT_BARS_BY_ENERGY,
    W_ENERGY_MATCH,
    W_SLOT_LENGTH,
)
from .music import Track


@dataclass
class Clip:
    hash: str
    path: str
    filename: str
    duration: float
    fps: float
    move_type: str
    motion_energy: float
    hue: float
    group: str
    tx_rate: float = 0.0
    ty_rate: float = 0.0
    reverse: bool = False        # play backwards, to break direction duplication
    energy_rank: float = 0.0     # 0..1 within the library
    cursor: int = 0              # source frames already consumed
    last_used_slot: int = -999
    times_used: int = 0

    @property
    def max_uses(self) -> int:
        return MAX_USES_BY_MOVE.get(self.move_type, MAX_USES_DEFAULT)

    @property
    def min_slot_bars(self) -> int:
        return MIN_SLOT_BARS_BY_MOVE.get(self.move_type, 1)

    def total_frames(self, fps: int) -> int:
        return int((self.duration - MIN_TAIL_MARGIN) * fps)

    def remaining(self, fps: int) -> int:
        return max(self.total_frames(fps) - self.cursor, 0)


@dataclass
class Cut:
    clip: Clip
    start_bar: int
    bars: int
    timeline_start: int      # frames
    duration: int            # frames on the timeline
    source_start: int        # frames into the source
    source_duration: int     # frames consumed from the source
    rate: float              # 1.0 normal, <1.0 slower
    section_label: str
    reverse: bool = False
    ramp: str | None = None  # None | "accel" | "decel"


def _group_of(filename: str) -> str:
    """Coarse location bucket from the filename.

    This is weak and known to be weak: the numbering is edit order, so all the
    tool has is the leading word. 'City 1..12' and 'City Above' collapse into
    one bucket of 13 against two hill clips, which means the same-location
    penalty almost never fires. Proper grouping needs visual clustering.
    """
    stem = Path(filename).stem.lower()
    first = stem.split()[0] if stem.split() else stem
    return first.rstrip("s")


def load_clips(db_path: Path) -> list[Clip]:
    conn = sqlite3.connect(db_path)
    rows = conn.execute(
        "SELECT hash, path, filename, duration, fps, move_type, motion_energy, hue, "
        "tx_rate, ty_rate FROM clips"
    ).fetchall()
    clips = [
        Clip(hash=r[0], path=r[1], filename=r[2], duration=r[3], fps=r[4],
             move_type=r[5], motion_energy=r[6], hue=r[7], group=_group_of(r[2]),
             tx_rate=r[8], ty_rate=r[9])
        for r in rows
    ]
    if AUTO_REVERSE:
        _assign_reversals(clips)
    # Rank-normalise energy so matching is relative to this library, not to an
    # absolute scale that means nothing across shoots.
    order = np.argsort([c.motion_energy for c in clips])
    for rank, idx in enumerate(order):
        clips[idx].energy_rank = rank / max(len(clips) - 1, 1)
    return clips


def _assign_reversals(clips: list[Clip]) -> None:
    """Flip every second clip that travels the same way as another.

    Two lateral moves in the same direction read as the same shot however far
    apart they sit. The dominant axis and its sign identify the direction; the
    strongest example of each direction is kept as-is and alternates after it
    are reversed.
    """
    buckets: dict[tuple, list[Clip]] = {}
    for c in clips:
        if c.move_type not in REVERSIBLE_MOVES:
            continue
        vertical = abs(c.ty_rate) > abs(c.tx_rate)
        sign = (c.ty_rate if vertical else c.tx_rate) >= 0
        buckets.setdefault((c.move_type, vertical, sign), []).append(c)

    for group in buckets.values():
        if len(group) < 2:
            continue
        group.sort(key=lambda c: -max(abs(c.tx_rate), abs(c.ty_rate)))
        for i, c in enumerate(group):
            c.reverse = bool(i % 2)


def overlapping_slices(cuts: list[Cut]) -> list[str]:
    """Report any clip whose slices cover the same source twice.

    Slices are handed out by a monotonically advancing per-clip cursor, so this
    should always be empty. It is checked rather than assumed because the one
    thing that broke it — a ramp inflating its source appetite after allocation
    — was invisible in the timeline and showed up only as a vague sense that
    footage was repeating.
    """
    by: dict[str, list[tuple[float, float, int]]] = {}
    for i, c in enumerate(cuts, 1):
        by.setdefault(c.clip.filename, []).append(
            (c.source_start, c.source_start + c.source_duration, i))

    out = []
    for fn, segs in by.items():
        segs.sort()
        for (a0, a1, ia), (b0, b1, ib) in zip(segs, segs[1:]):
            if b0 < a1:
                out.append(f"{fn}: cuts #{ia} and #{ib} share source "
                           f"{b0/30:.1f}-{min(a1, b1)/30:.1f}s")
    return out


def _preferred_bars(section_energy_norm: float) -> int:
    for threshold, bars in SLOT_BARS_BY_ENERGY:
        if section_energy_norm < threshold:
            return bars
    return SLOT_BARS_BY_ENERGY[-1][1]


def _hue_distance(a: float, b: float) -> float:
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def build_edit(track: Track, clips: list[Clip], fps: int) -> list[Cut]:
    # Rescale section energies across this track so the calmest section maps to
    # the calmest clips. Without this, a track that never drops below 0.5 would
    # only ever ask for high-energy footage.
    sec_e = np.array([s.energy for s in track.sections])
    lo, hi = sec_e.min(), sec_e.max()
    span = max(hi - lo, 1e-9)

    # Bar maths alone would allow a 20s shot at slow tempos; cap by wall clock.
    legal_bars = tuple(b for b in LEGAL_SLOT_BARS
                       if b * track.bar_period <= MAX_SHOT_SECONDS) or (1,)

    # Bars where a peak section begins — the landing points a punch ramp aims at.
    peak_starts = {s.start_bar for s in track.sections if s.label == "peak"}

    cuts: list[Cut] = []
    bar = 0
    slot_i = 0
    prev: Clip | None = None

    for section in track.sections:
        target_e = float((section.energy - lo) / span)
        pref_bars = _preferred_bars(target_e)
        bar = max(bar, section.start_bar)

        while bar < section.end_bar:
            room = section.end_bar - bar
            # Hold a longer shot on the phrase boundary. Without this every slot
            # in a section collapses to the same length and a minute of the drop
            # reads as one metronomic pulse.
            on_phrase = (bar % PHRASE_BARS) == 0
            slot_pref = pref_bars * (PHRASE_ACCENT_MULTIPLIER if on_phrase else 1)
            best = None

            for clip in clips:
                if clip.remaining(fps) <= 0:
                    continue
                cooling = (slot_i - clip.last_used_slot) < REUSE_COOLDOWN_SLOTS
                if cooling and clip.times_used > 0:
                    continue
                if clip.times_used >= clip.max_uses:
                    continue

                for bars in legal_bars:
                    if bars > room or bars < clip.min_slot_bars:
                        continue
                    t0 = track.bar_time(bar)
                    t1 = track.bar_time(bar + bars)
                    tl_frames = round(t1 * fps) - round(t0 * fps)

                    avail = clip.remaining(fps)

                    # Candidate playback modes for this slot. A punch ramp is a
                    # mode like any other, not a post-hoc edit: it consumes the
                    # mean of its speed curve, and deciding it here is what keeps
                    # that consumption inside the cursor accounting. Assigning
                    # ramps after the fact let them eat footage later cuts had
                    # already claimed, and the same seconds appeared twice.
                    modes = [(r, None) for r in (SPEED_CHOICES if ALLOW_SPEEDUP else (1.0,))]
                    # An escalate is offered only where it means something: the
                    # shot has to end on a structural boundary, so the launch
                    # lands on a real musical change rather than an arbitrary bar.
                    if ALLOW_RAMPS and bars >= RAMP_MIN_BARS and (bar + bars) in peak_starts:
                        modes.append((1.0, "punch"))

                    for rate, ramp in modes:
                        # Speed-up only: a clip never runs slower than recorded,
                        # so a slot it cannot fill at 1x simply goes to another
                        # clip rather than being stretched.
                        if ramp == "punch":
                            src_frames = int(round(tl_frames * (1.0 + RAMP_END_SPEED) / 2.0))
                        else:
                            src_frames = int(round(tl_frames * rate))
                        if avail < src_frames:
                            continue
                        if rate > 1.0 and avail < SPEEDUP_MIN_REMAINING * fps:
                            continue     # 2x is for long clips, not for coverage

                        score = -W_ENERGY_MATCH * abs(clip.energy_rank - target_e)
                        # Prefer the section's rhythm, but softly — footage wins.
                        score -= W_SLOT_LENGTH * abs(math.log2(bars / slot_pref))
                        if prev is not None:
                            if clip.move_type == prev.move_type:
                                score -= PENALTY_SAME_MOVE
                            if clip.group == prev.group:
                                score -= PENALTY_SAME_GROUP
                            if _hue_distance(clip.hue, prev.hue) < HUE_CLOSE_DEG:
                                score -= PENALTY_CLOSE_HUE
                        # Reuse penalty decays with distance rather than counting
                        # uses. A count-based penalty grows past any possible
                        # energy mismatch and degenerates into round-robin
                        # rotation, which is how hovers ended up on the drop.
                        gap = slot_i - clip.last_used_slot
                        if clip.times_used:
                            score -= PENALTY_REUSE * max(0.0, 1.0 - gap / REUSE_RECENCY_WINDOW)
                        score -= PENALTY_OVERUSE * clip.times_used

                        # Coverage pressure: prefer clips with material left, and
                        # prefer taking a bigger bite out of them. Without this the
                        # engine nibbles the head of every clip and abandons the
                        # back half of every long take.
                        total = max(clip.total_frames(fps), 1)
                        score += W_COVERAGE * (avail / total)
                        score += W_BITE * (src_frames / total)

                        if rate != 1.0:
                            score -= PENALTY_SPEEDUP_WHEN_CALM * (1.0 - target_e)
                        if ramp:
                            score += W_PUNCH      # ramps are wanted, where they fit

                        if best is None or score > best[0]:
                            best = (score, clip, bars, tl_frames, src_frames, rate, ramp)

            if best is None:
                # Every clip is either cooling or exhausted. Recycle the ones
                # not used recently rather than leave a hole in the timeline.
                recycled = False
                for clip in clips:
                    if (slot_i - clip.last_used_slot) >= REUSE_COOLDOWN_SLOTS:
                        clip.cursor = int(HEAD_TRIM * fps)
                        recycled = True
                if recycled:
                    continue
                break

            _, clip, bars, tl_frames, src_frames, rate, ramp = best
            t0 = track.bar_time(bar)
            cuts.append(Cut(
                clip=clip,
                start_bar=bar,
                bars=bars,
                timeline_start=round(t0 * fps),
                duration=tl_frames,
                source_start=clip.cursor,
                source_duration=src_frames,
                rate=rate,
                section_label=section.label,
                reverse=clip.reverse,
                ramp=ramp,
            ))
            clip.cursor += src_frames
            clip.last_used_slot = slot_i
            clip.times_used += 1
            if ramp:
                last_escalate = slot_i
            prev = clip
            bar += bars
            slot_i += 1

    _absorb_lead_in(cuts, fps)
    return cuts


def _absorb_lead_in(cuts: list[Cut], fps: int) -> None:
    """Close the hole between frame 0 and the first bar line.

    The grid rarely starts exactly at zero, which would leave the spine opening
    on a gap. Shifting the whole timeline earlier is not an option — that pulls
    every cut off the beat. Instead the first shot starts at frame 0 and runs
    long by the lead-in, so its *outgoing* cut still lands on the bar line and
    everything downstream is untouched.
    """
    if not cuts or cuts[0].timeline_start == 0:
        return

    c = cuts[0]
    lead = c.timeline_start
    new_dur = c.duration + lead
    avail = c.clip.total_frames(fps)          # measured from frame 0 of the source

    # Only extend if the clip genuinely has the frames; never slow it to fit.
    src = int(round(new_dur * c.rate))
    if avail < src:
        return                                 # validator will flag the gap

    c.timeline_start = 0
    c.duration = new_dur
    c.source_start = 0
    c.source_duration = src


def reset(clips: list[Clip], fps: int) -> None:
    for c in clips:
        c.cursor = int(HEAD_TRIM * fps)
        c.last_used_slot = -999
        c.times_used = 0


def describe(cuts: list[Cut], fps: int) -> str:
    lines = [
        f"{'#':>3} {'bar':>4} {'tc':>9} {'len':>6} {'bars':>4} "
        f"{'clip':<20} {'move':<10} {'sect':<6} {'src in':>8} {'rate':>6} {'fx':<12}"
    ]
    lines.append("-" * 104)
    for i, c in enumerate(cuts, 1):
        tc = c.timeline_start / fps
        fx = " ".join(filter(None, ["REV" if c.reverse else "", c.ramp or ""]))
        lines.append(
            f"{i:>3} {c.start_bar:>4} {int(tc)//60:>1}:{tc%60:0>5.2f} "
            f"{c.duration/fps:>5.2f}s {c.bars:>4} "
            f"{c.clip.filename[:19]:<20} {c.clip.move_type:<10} {c.section_label:<6} "
            f"{c.source_start/fps:>7.2f}s {c.rate:>6.3f} {fx:<12}"
        )
    total = sum(c.duration for c in cuts) / fps
    retimed = sum(1 for c in cuts if c.rate != 1.0)
    ramped = sum(1 for c in cuts if c.ramp)
    reversed_n = sum(1 for c in cuts if c.reverse)
    uses = {}
    for c in cuts:
        uses[c.clip.filename] = uses.get(c.clip.filename, 0) + 1
    lines.append("")
    src_used = sum(c.source_duration for c in cuts) / fps
    src_total = sum(c.clip.duration for c in {id(c.clip): c for c in cuts}.values())
    lines.append(f"{len(cuts)} cuts, {total/60:.2f} min, mean shot {total/max(len(cuts),1):.2f}s, "
                 f"{retimed} sped up, {ramped} punch ramps, {reversed_n} reversed")
    lines.append(f"footage used: {src_used:.0f}s of {src_total:.0f}s "
                 f"({100*src_used/max(src_total,1):.0f}%)")
    lines.append("uses per clip: " + ", ".join(
        f"{k.replace('.mp4','')}×{v}" for k, v in sorted(uses.items(), key=lambda kv: -kv[1])))
    return "\n".join(lines)
