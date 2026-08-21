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
    BEATS_PER_BAR,
    ALLOW_SPEEDUP,
    AUTO_REVERSE,
    CLIP_HEAD_SKIP,
    CLIP_MAX_USES,
    HEAD_CLIPS,
    HEAD_UNTIL_BAR,
    CLIP_REVERSE_OVERRIDE,
    CLIP_SKIP_RANGES,
    ESCALATE_AT_BARS,
    PIN_CLIPS,
    PIN_SLOT_BARS,
    ESCALATE_BODY_SPEED,
    ESCALATE_TAIL_SECONDS,
    ESCALATE_TAIL_SPEED,
    HEAD_TRIM,
    PENALTY_SPEEDUP_WHEN_CALM,
    REWIND_WHEN_EXHAUSTED,
    SPEED_CHOICES,
    SPEEDUP_MIN_REMAINING,
    W_BITE,
    W_COVERAGE,
    MAX_USES_BY_MOVE,
    MAX_USES_DEFAULT,
    MIN_SLOT_BARS_BY_MOVE,
    REVERSIBLE_MOVES,
    HUE_CLOSE_DEG,
    INTEGER_SPEEDS_ONLY,
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
    head_skip: float = 0.0       # extra seconds ignored at the head of this clip
    skips: tuple = ()            # (from, to) source seconds never to use
    energy_rank: float = 0.0     # 0..1 within the library
    cursor: int = 0              # source frames already consumed
    last_used_slot: int = -999
    times_used: int = 0

    @property
    def max_uses(self) -> int:
        named = self._named_cap()
        if named is not None:
            return named
        return MAX_USES_BY_MOVE.get(self.move_type, MAX_USES_DEFAULT)

    def _named_cap(self) -> int | None:
        """This clip's CLIP_MAX_USES entry, matched on filename substring."""
        low = self.filename.lower()
        for frag, cap in CLIP_MAX_USES.items():
            if frag.lower() in low:
                return cap
        return None

    @property
    def cap_is_absolute(self) -> bool:
        """True when the cap exists to keep the clip intact, not to pace it.

        The relax pass lifts use caps rather than let the timeline run short.
        A named cap is not a pacing preference, so it survives that pass.
        """
        return self._named_cap() is not None

    def start_for(self, need: int, fps: int) -> int | None:
        """Where the next `need` frames can start, hopping excluded ranges.

        Returns None when the clip cannot supply that many clean frames. The
        cursor is not moved; the caller commits by assigning it the returned
        start plus what it took, which is what keeps slices non-overlapping.
        """
        pos = self.cursor
        for a, b in sorted((round(a * fps), round(b * fps)) for a, b in self.skips):
            if pos + need <= a:
                break            # fits entirely before this exclusion
            if pos < b:
                pos = b          # would run into it — start after instead
        return pos if pos + need <= self.total_frames(fps) else None

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
    rate: float              # 1.0 normal, >1.0 faster
    section_label: str
    reverse: bool = False
    ramp: str | None = None  # None | "escalate"
    body_speed: float = 0.0  # actual body speed of an escalate, once fitted
    tail_speed: float = 0.0  # actual peak speed of an escalate, once fitted
    start_beat: int = 0      # slot start on the beat grid (bar * BEATS_PER_BAR)
    beats: int = 0           # slot length in beats; sub-bar slots need this
    raw_timemap: list | None = None   # captured verbatim from an FCP export


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
             tx_rate=r[8], ty_rate=r[9],
             head_skip=next((s for name, s in CLIP_HEAD_SKIP.items()
                             if name.lower() in r[2].lower()), 0.0),
             skips=tuple(tuple(rng) for name, rngs in CLIP_SKIP_RANGES.items()
                         if name.lower() in r[2].lower() for rng in rngs))
        for r in rows
    ]
    if AUTO_REVERSE:
        _assign_reversals(clips)
    # An explicit direction always wins over the automatic pairing.
    for c in clips:
        for name, want in CLIP_REVERSE_OVERRIDE.items():
            if name.lower() in c.filename.lower():
                c.reverse = bool(want)
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
        # Head clips are exempt. They were cut by hand, and revisiting a moment
        # deliberately — a whip that races back over the shot it just played —
        # is a choice there, not the allocator losing track of its cursor.
        if c.section_label == "head":
            continue
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


def _label_at(track: Track, bar: int) -> str:
    for s in track.sections:
        if s.start_bar <= bar < s.end_bar:
            return s.label
    return track.sections[-1].label if track.sections else ""


def _slot_beats(entry: dict) -> tuple[int, int]:
    """A lock entry's (start, length) on the beat grid.

    Slots are normally written in bars, which is all a music-cut edit needs. An
    opening burst wants shots shorter than a bar, so an entry may instead give
    `beat` and `beats` — one beat is a quarter of a bar. Everything downstream
    works in beats and bars are just the coarse case, so the two forms mix
    freely inside one lock.
    """
    if "beat" in entry or "beats" in entry:
        return (int(entry.get("beat", int(entry.get("bar", 0)) * BEATS_PER_BAR)),
                int(entry.get("beats", int(entry.get("bars", 1)) * BEATS_PER_BAR)))
    return int(entry["bar"]) * BEATS_PER_BAR, int(entry["bars"]) * BEATS_PER_BAR


def build_locked(track: Track, clips: list[Clip], fps: int,
                 lock: list[dict]) -> list[Cut]:
    """Replay an approved assignment instead of re-deciding it.

    The scorer is greedy: change any input and every later slot can land on a
    different clip. That makes parameter tuning useless for "keep this timeline
    but change one shot" — the single change drags the whole running order with
    it.

    A lock records the slot grid and clip assignment of an approved edit, and
    this replays it exactly. Nothing here consults the scoring weights, so the
    only things that vary are what was edited in the lock file or applied on top
    (escalates, head skips).
    """
    by_name = {c.filename: c for c in clips}
    entries = sorted(lock, key=lambda e: _slot_beats(e)[0])

    # What each clip owes its *other* slots at nominal speed. An escalate is
    # sized against this so it takes only genuinely spare footage — otherwise a
    # ramp early on eats the material a later slot in the approved order needs,
    # and that slot has to be dropped or re-clipped, which moves the timeline.
    # Only slots AFTER the escalate count. Summing every slot charged the clip
    # for footage its earlier slots had already consumed, so a clip used before
    # the ramp was billed twice and the ramp was refused on a shortfall that did
    # not exist. That stayed invisible until a shot earlier in the timeline was
    # lengthened, which is exactly when it bites.
    owed: dict[str, list[tuple[int, int]]] = {}
    for e in entries:
        b0, blen = _slot_beats(e)
        if ALLOW_RAMPS and b0 % BEATS_PER_BAR == 0 and b0 // BEATS_PER_BAR in ESCALATE_AT_BARS:
            continue
        tl = round(track.beat_time(b0 + blen) * fps) - round(track.beat_time(b0) * fps)
        owed.setdefault(e["clip"], []).append(
            (b0, int(round(tl * float(e.get("rate", 1.0))))))

    def owed_after(name: str, at_beat: int) -> int:
        """Frames this clip still owes slots that start after `at_beat`."""
        return sum(f for b, f in owed.get(name, []) if b > at_beat)

    cuts: list[Cut] = head_cuts(clips, fps)
    n_head = len(cuts)

    for entry in entries:
        b0, blen = _slot_beats(entry)
        bar, bars = b0 // BEATS_PER_BAR, max(blen // BEATS_PER_BAR, 1)
        on_bar = b0 % BEATS_PER_BAR == 0
        name = entry["clip"]
        clip = by_name.get(name) or next(
            (c for c in clips if name.lower() in c.filename.lower()), None)
        if clip is None:
            print(f"  note: lock names '{name}' at bar {bar}, not found in the index")
            continue

        t0, t1 = track.beat_time(b0), track.beat_time(b0 + blen)
        tl_frames = round(t1 * fps) - round(t0 * fps)
        rate = float(entry.get("rate", 1.0))

        ramp = None
        body_speed = tail_speed = 0.0
        src_frames = int(round(tl_frames * rate))
        if ALLOW_RAMPS and on_bar and bar in ESCALATE_AT_BARS:
            # "Speed up to the max that allows the transition": the launch is
            # as fast as the footage this clip can spare, not a fixed number.
            # The budget subtracts what the clip is already committed to in
            # later slots, so escalating here cannot starve them.
            clean = clip.remaining(fps) - sum(
                max(0, min(round(b * fps), clip.total_frames(fps)) - max(round(a * fps), clip.cursor))
                for a, b in clip.skips)
            budget = clean - owed_after(clip.filename, b0)
            ideal = escalate_source_frames(tl_frames, fps)
            body_speed, tail_speed = fit_escalate(tl_frames, min(ideal, budget), fps)
            if tail_speed:
                ramp, rate = "escalate", 1.0
                src_frames = escalate_source_frames(
                    tl_frames, fps, tail_speed, body_speed)
                if tail_speed < ESCALATE_TAIL_SPEED - 0.05:
                    print(f"  note: escalate at bar {bar} fitted to "
                          f"{body_speed*100:.0f}% -> {tail_speed*100:.0f}% "
                          f"(ideal {ESCALATE_BODY_SPEED*100:.0f}% -> "
                          f"{ESCALATE_TAIL_SPEED*100:.0f}%): {clip.filename} must "
                          f"keep {owed_after(clip.filename, b0)/fps:.1f}s for its "
                          f"later slots")
            else:
                print(f"  note: no escalate at bar {bar} — {clip.filename} cannot "
                      f"spare the footage without starving its later slots")

        src_at = clip.start_for(src_frames, fps)
        if src_at is None:
            # Drop to natural speed before giving up on the slot entirely.
            at_natural = clip.start_for(tl_frames, fps)
            if at_natural is not None:
                print(f"  note: bar {bar} {clip.filename} lacks material for "
                      f"{rate:.2f}x — using 1.0x")
                ramp, rate, src_frames, src_at = None, 1.0, tl_frames, at_natural
            else:
                blocked = sum(
                    max(0, min(round(b * fps), clip.total_frames(fps))
                        - max(round(a * fps), clip.cursor))
                    for a, b in clip.skips)
                print(f"  note: bar {bar} {clip.filename} cannot supply "
                      f"{src_frames/fps:.1f}s from {clip.cursor/fps:.1f}s — "
                      f"{clip.remaining(fps)/fps:.1f}s remain"
                      + (f", but {blocked/fps:.1f}s of it is excluded and the rest "
                         f"does not run long enough in one piece" if blocked else ""))
                src_at = clip.cursor
                src_frames = max(clip.remaining(fps), 1)

        cuts.append(Cut(
            clip=clip, start_bar=bar, bars=bars,
            start_beat=b0, beats=blen,
            timeline_start=round(t0 * fps), duration=tl_frames,
            source_start=src_at, source_duration=src_frames,
            rate=rate, section_label=_label_at(track, bar),
            reverse=bool(entry.get("reverse", clip.reverse)), ramp=ramp,
            body_speed=body_speed, tail_speed=tail_speed,
        ))
        clip.cursor = src_at + src_frames
        clip.times_used += 1

    # With a hand-cut head the spine already starts at frame 0; there is no
    # lead-in to absorb and the captured clips must not be re-timed.
    if not n_head:
        _absorb_lead_in(cuts, fps)
    return cuts


def dump_lock(cuts: list[Cut]) -> str:
    """Serialise an edit's slot grid and assignment as an editable TOML lock."""
    lines = [
        "# Locked edit. Replayed verbatim by `build`, bypassing the scorer, so an",
        "# approved running order survives changes made elsewhere.",
        "#",
        "# Edit by hand: `clip` swaps a shot, `bars` resizes a slot (1 bar = one",
        "# musical bar), `rate` sets a constant speed-up, `reverse` sets the play",
        "# direction for this slot alone.",
        "#",
        "# `reverse` is here because direction is a property of a shot, not of a",
        "# clip. CLIP_REVERSE_OVERRIDE can only flip every use of a clip at once,",
        "# which is right for a clip used once and wrong the moment one slot wants",
        "# to run backwards and another forwards.",
        "# Regenerate from the current edit with `build --lock-out <file>`.",
        "",
    ]
    for c in cuts:
        # The hand-cut head is defined by HEAD_CLIPS and prepended on every
        # build. Writing it here too would emit it twice and, since those clips
        # have no slot on the bar grid, at bar 0 with zero length.
        if c.section_label == "head":
            continue
        lines += [
            "[[lock]]",
            f"bar = {c.start_bar}",
            f'clip = "{c.clip.filename}"',
            f"bars = {c.bars}",
            f"rate = {c.rate:.3f}",
            f"reverse = {str(c.reverse).lower()}",
            "",
        ]
    return "\n".join(lines)


def escalate_source_frames(tl_frames: int, fps: int,
                           tail_speed: float | None = None,
                           body_speed: float | None = None) -> int:
    """Source consumed by an escalate: flat body, then a linear launch.

    Speed holds at ESCALATE_BODY_SPEED, then rises across the last
    ESCALATE_TAIL_SECONDS to `tail_speed`. The tail is specified in timeline
    seconds rather than as a fraction so the launch feels the same length
    whether the shot is 5s or 10s.
    """
    peak = ESCALATE_TAIL_SPEED if tail_speed is None else tail_speed
    base = ESCALATE_BODY_SPEED if body_speed is None else body_speed
    tail = min(int(round(ESCALATE_TAIL_SECONDS * fps)), tl_frames)
    body = tl_frames - tail
    return int(round(body * base + tail * (base + peak) / 2.0))


def fit_escalate(tl_frames: int, budget: int, fps: int) -> tuple[float, float]:
    """Strongest (body, tail) speed pair this much source can pay for.

    "Speed up to the max that allows the transition." The ideal profile is
    ESCALATE_BODY_SPEED through the body and ESCALATE_TAIL_SPEED at the last
    frame, but a clip that also has to serve later slots may not be able to
    fund it. Body speed is walked down from the ideal and the launch is
    recomputed each step, so the result is the fastest profile that fits rather
    than no effect at all. Returns (0, 0) when even a mild launch is impossible.
    """
    tail_f = min(int(round(ESCALATE_TAIL_SECONDS * fps)), tl_frames)
    if tail_f <= 0 or budget <= 0:
        return 0.0, 0.0
    body_f = tl_frames - tail_f

    # Whole multiples only. Stepping by 0.1 found "the fastest profile that
    # fits" and answered 160%, which stutters — see INTEGER_SPEEDS_ONLY. The
    # honest choices are 200% or 100%, and 100% with a longer launch is a
    # better shot than 160% with a shorter one.
    step = 1.0 if INTEGER_SPEEDS_ONLY else 0.1
    body = float(int(ESCALATE_BODY_SPEED)) if INTEGER_SPEEDS_ONLY else ESCALATE_BODY_SPEED
    while body >= 1.0:
        spare = budget - body_f * body
        peak = 2.0 * spare / tail_f - body
        peak = min(peak, ESCALATE_TAIL_SPEED)
        if INTEGER_SPEEDS_ONLY:
            peak = float(int(peak))
        # The launch has to be clearly faster than the body or it reads as a
        # flat speed-up rather than a ramp.
        if peak >= body * 2.0:
            return body, peak
        body -= step
    return 0.0, 0.0


def _hue_distance(a: float, b: float) -> float:
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)


def head_cuts(clips: list[Clip], fps: int) -> list[Cut]:
    """The hand-cut opening from HEAD_CLIPS, as real cuts on the front of the spine.

    These are not scored, not snapped and not re-derived — they are replayed at
    the frame values captured from Final Cut. What they do take part in is the
    footage accounting: a head clip advances its cursor and its use count, so a
    clip spent here cannot be spent again by the scorer, and a cap of one use
    means one use in total rather than one use each side of the join.
    """
    out: list[Cut] = []
    for entry in HEAD_CLIPS:
        name = entry["clip"]
        clip = next((c for c in clips if name.lower() in c.filename.lower()), None)
        if clip is None:
            print(f"  note: HEAD_CLIPS names '{name}', not found in the index")
            continue
        off = round(entry["offset"] * fps)
        start = round(entry.get("start", 0.0) * fps)
        dur = round(entry["duration"] * fps)
        tm = entry.get("timemap")
        # Source consumed is what the timemap actually reaches over the span
        # this clip plays, not the slot length — a 4x whip eats four seconds per
        # second on screen. With a timemap, `start` is an offset into the
        # RETIMED clip, so the source range is the curve evaluated across
        # [start, start + duration]. Evaluated linearly between the captured
        # control points: close enough for cursor accounting, and the curve
        # itself is still reproduced exactly on output.
        if tm:
            def at(t_frames: int) -> int:
                pts = [(round(a * fps), round(b * fps)) for a, b, _ in tm]
                for (ta, va), (tb, vb) in zip(pts, pts[1:]):
                    if t_frames <= tb:
                        span = tb - ta or 1
                        return round(va + (vb - va) * (t_frames - ta) / span)
                return pts[-1][1]
            src_from, src_to = at(start), at(start + dur)
            src = max(src_to - src_from, 1)
        else:
            src_from, src = start, dur
        out.append(Cut(
            clip=clip, start_bar=0, bars=0, start_beat=0, beats=0,
            timeline_start=off, duration=dur,
            source_start=start, source_duration=max(src, 1),
            rate=1.0, section_label="head", reverse=False, ramp=None,
            # Frames, not seconds. Written as decimal seconds these round to a
            # hair past the asset duration and the writer's own exact rationals
            # then disagree with them — the clip validated as reaching 29.0667s
            # of a 29.0667s media.
            raw_timemap=[(round(t * fps), round(v * fps), i)
                         for t, v, i in tm] if tm else None,
        ))
        # `charge` states how far the cursor moves, overriding what this entry
        # actually consumed. A hand-cut head may revisit footage on purpose —
        # this one plays Sunset Sea 1, then whips back through the same seconds
        # — and inferring the cursor from that pushes every later slot on the
        # clip forward, which silently re-cuts the approved timeline below.
        # Stating it keeps the head's overlaps the author's business.
        charge = entry.get("charge")
        clip.cursor = (max(clip.cursor, round(charge * fps)) if charge is not None
                       else max(clip.cursor, src_from + src))
        clip.times_used += 1
    return out


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

    # Structural boundaries an escalate is allowed to launch from.
    boundaries = {s.start_bar for s in track.sections} | {track.sections[-1].end_bar}

    cuts: list[Cut] = head_cuts(clips, fps)
    n_head = len(cuts)
    bar = HEAD_UNTIL_BAR
    slot_i = 0
    last_escalate = -999
    prev: Clip | None = None
    exhausted = False

    for section in track.sections:
        if exhausted:
            break
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

            # A pin is a direct instruction: it overrides scoring, the cooldown
            # and the use cap. Everything else about the slot is unchanged.
            pin = PIN_CLIPS.get(bar)

            # A pin is also a reservation. Without this the scorer spends the
            # clip on an earlier slot on merit and the pin then reports "no
            # material left" — which is what happened to every clip capped at a
            # single use, since one use is all there was to spend.
            reserved = {frag.lower() for at, frag in PIN_CLIPS.items() if at > bar}

            def eligible(relax_uses: bool) -> list[Clip]:
                out = []
                for clip in clips:
                    if clip.remaining(fps) <= 0:
                        continue
                    if pin is not None:
                        if pin.lower() not in clip.filename.lower():
                            continue
                    else:
                        low = clip.filename.lower()
                        if any(frag in low for frag in reserved):
                            continue
                        cooling = (slot_i - clip.last_used_slot) < REUSE_COOLDOWN_SLOTS
                        if cooling and clip.times_used > 0:
                            continue
                        spent = clip.times_used >= clip.max_uses
                        if spent and (not relax_uses or clip.cap_is_absolute):
                            continue
                    out.append(clip)
                return out

            # Lift the use cap before giving up. A clip with 30 unseen seconds
            # left is always a better answer than the fallback below, which
            # rewinds cursors and puts footage the viewer has already seen back
            # on screen — the most visible failure this engine has, and the one
            # that reads as "the same shot again" even when the take continues.
            candidates = eligible(False) or eligible(True)

            for clip in candidates:
                # A pinned length is taken literally — it is an instruction, so
                # it is not filtered against the legal set or MAX_SHOT_SECONDS.
                pinned_bars = PIN_SLOT_BARS.get(bar)
                bar_choices = (pinned_bars,) if pinned_bars is not None else legal_bars
                for bars in bar_choices:
                    if bars > room:
                        continue
                    # A pinned clip is allowed to take a shorter slot than its
                    # move type would normally justify — the instruction wins.
                    if pin is None and bars < clip.min_slot_bars:
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
                    for rate, ramp in modes:
                        # Speed-up only: a clip never runs slower than recorded,
                        # so a slot it cannot fill at 1x simply goes to another
                        # clip rather than being stretched.
                        src_frames = int(round(tl_frames * rate))
                        src_at = clip.start_for(src_frames, fps)
                        if src_at is None:
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

                        if best is None or score > best[0]:
                            best = (score, clip, bars, tl_frames, src_frames,
                                    rate, ramp, src_at)

            if best is None and pin is not None:
                print(f"  note: pin at bar {bar} ('{pin}') could not be placed — "
                      f"no material left, or it cannot fill the slot at 1x")

            if best is None:
                # Genuinely out of material: the use cap has already been lifted
                # above, so every clip is either cooling or spent. Either outcome
                # is announced — a silent rewind here is indistinguishable from
                # the edit simply repeating itself, which is how it went
                # unnoticed until someone watched the result and said so.
                recycled = [c for c in clips
                            if (slot_i - c.last_used_slot) >= REUSE_COOLDOWN_SLOTS]
                if recycled and REWIND_WHEN_EXHAUSTED:
                    print(f"  note: bar {bar} — out of unused footage, rewinding "
                          f"{len(recycled)} clip(s) to the head; from here the "
                          f"edit repeats material")
                    for clip in recycled:
                        clip.cursor = int(HEAD_TRIM * fps)
                    continue
                left = (track.bar_time(track.n_bars) - track.bar_time(bar))
                print(f"  note: out of unused footage at bar {bar} — ending "
                      f"{left:.1f}s short of the track rather than repeating "
                      f"material (REWIND_WHEN_EXHAUSTED)")
                exhausted = True
                break

            _, clip, bars, tl_frames, src_frames, rate, ramp, src_at = best

            # Escalate is applied AFTER the clip is chosen, never as a competitor
            # for the slot, so switching it on cannot change the running order —
            # only how the clip that already won plays. The extra source it eats
            # is booked here, before the cursor advances, which is what keeps
            # slices from overlapping.
            if ALLOW_RAMPS and bar in ESCALATE_AT_BARS and rate == 1.0:
                need = escalate_source_frames(tl_frames, fps)
                at = clip.start_for(need, fps)
                if at is not None:
                    ramp, src_frames, src_at = "escalate", need, at
                else:
                    short = (need - clip.remaining(fps)) / fps
                    print(f"  note: no escalate at bar {bar} — {clip.filename} is "
                          f"{short:.1f}s short of the {need/fps:.1f}s it needs")

            t0 = track.bar_time(bar)
            cuts.append(Cut(
                clip=clip,
                start_bar=bar,
                bars=bars,
                timeline_start=round(t0 * fps),
                duration=tl_frames,
                source_start=src_at,
                source_duration=src_frames,
                rate=rate,
                section_label=section.label,
                reverse=clip.reverse,
                ramp=ramp,
            ))
            clip.cursor = src_at + src_frames
            clip.last_used_slot = slot_i
            clip.times_used += 1
            if ramp:
                last_escalate = slot_i
            if ramp:
                last_escalate = slot_i
            prev = clip
            bar += bars
            slot_i += 1

    # With a hand-cut head the spine already starts at frame 0; there is no
    # lead-in to absorb and the captured clips must not be re-timed.
    if not n_head:
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
        # A sped-up opening shot pays for the lead-in twice over — at 2x, five
        # extra timeline frames cost ten source frames — and a clip chosen to
        # fill its slot exactly has no such margin. Fit the rate down to what
        # the clip holds rather than leave the spine opening on a gap. The
        # floor is real time; below that the shot would be slowed, which this
        # engine never does.
        fitted = avail / new_dur
        if fitted < 1.0:
            return                             # validator will flag the gap
        print(f"  note: opening shot fitted to {fitted:.3f}x (from {c.rate:.3f}x) "
              f"to absorb the {lead}-frame lead-in without a gap")
        c.rate = fitted
        src = avail

    c.timeline_start = 0
    c.duration = new_dur
    c.source_start = 0
    c.source_duration = src


def reset(clips: list[Clip], fps: int) -> None:
    for c in clips:
        c.cursor = int((HEAD_TRIM + c.head_skip) * fps)
        c.last_used_slot = -999
        c.times_used = 0


def describe(cuts: list[Cut], fps: int) -> str:
    lines = [
        f"{'#':>3} {'bar':>6} {'tc':>9} {'len':>6} {'bars':>5} "
        f"{'clip':<20} {'move':<10} {'sect':<6} {'src in':>8} {'rate':>6} {'fx':<12}"
    ]
    lines.append("-" * 104)
    for i, c in enumerate(cuts, 1):
        tc = c.timeline_start / fps
        fx = " ".join(filter(None, ["REV" if c.reverse else "", c.ramp or ""]))
        # Sub-bar slots exist, so both columns are shown in bars-and-fractions
        # rather than rounded to whole bars — six 0.5-bar shots all reporting
        # "1 bar" starting at bar 0, 0, 1, 1 is unreadable.
        beats = c.beats or c.bars * 4
        at = (c.start_beat or c.start_bar * 4) / 4
        fmt = lambda v: f"{v:g}"
        lines.append(
            f"{i:>3} {fmt(at):>6} {int(tc)//60:>1}:{tc%60:0>5.2f} "
            f"{c.duration/fps:>5.2f}s {fmt(beats/4):>5} "
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
