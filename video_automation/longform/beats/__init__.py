"""Drawn beats, in landscape.

The shorts have exactly one drawn beat — `ChecklistShot` — and it carries a
single moment in a ten-shot piece. Long form inverts that: the arithmetic in
`docs/long-form-strategy.md` says a three-minute video needs about thirty shots
against two to five available photographs, so **drawn beats have to carry the
largest single share of the runtime**. That is also the only version of this
format worth making, because a drawn beat shows the argument instead of
illustrating it.

**The split layout is the reason this works at 1920x1080.** Every beat here puts
its content in a column on the left and, optionally, a photograph in a column on
the right. A 900px source — the median on thecrypto.wiki — dropped into a 660px
column is a *downscale*. The upscale problem that dominates the full-frame photo
case (see `core/frame.py`) does not arise at all here, so the more of the piece
these beats carry, the sharper the whole video is. That is a happy alignment and
worth not breaking.

Every beat reuses the two things the shorts' checklist paid for:

* **Two phases.** Content arrives on `reveals`, taken from the caption times of
  the sentence being spoken, so a line appears exactly as it is said. Verdicts,
  where a beat has them, land afterwards on `marks` — in the pause the script
  bought with a longer `gap`. Marking each item as it arrived answered the
  question before it had been asked.
* **Things draw on, they do not appear.** At this size an instant strike reads
  as a rendering glitch; a line that travels reads as something being crossed
  out.

**This was one 3,124-line module until 2026-09-27.** Splitting it changed no
pixel - the 19 beats were verified frame by frame, on both brands, in both
frames, at four points through each - and it is only ergonomics: the file had
become the largest in the repo by a factor of two and the place every new beat
had to be threaded into by hand.

The families are by **silhouette**, which is the axis `beats.md` says actually
matters:

| module | the shape |
| --- | --- |
| `base` | `Beat` itself, the constants, the shared helpers |
| `column` | content column left, picture right - the original five |
| `wide` | full-frame layouts: a set, a lineup, a track, a division |
| `scale` | instruments: a magnitude against a scale |
| `plot` | a curve against an axis: time, trajectory, frequency |
| `annotate` | things pointed at: a photo, a chain, a plate, a drawing |

Everything the old module exported is re-exported here, so
`from .beats import Checklist, item_count, make_beat` still means what it
always did. **Add a new beat to the family whose silhouette it shares**, then
to `BEATS` and `_COUNT` below - and give it a payload in `tests/test_beats.py`,
which fails if you forget.
"""

from __future__ import annotations

from ...core.brand import Brand
from ...core.frame import Frame

# The private helpers come along too. They are not part of the surface
# `__all__` describes, but `longform/chrome.py` and `tools/make_wave.py` both
# do `from .beats import _font` and did so before the split - re-exporting
# them is what makes the split invisible to everything outside this package.
from .base import (DRAW, POP, RISE, Beat, _display, _font, _hex,  # noqa: F401
                   _mark_bottom, _round_corners, _smooth, _unit)
from .annotate import Anatomy, Callout, Diagram, Map
from .column import ChapterCard, Checklist, Compare, Quote, Stat
from .plot import Chart, Spectrum, Timeline
from .scale import Bars, Dial, Gauge
from .wide import Grid, Logos, Split, Steps

# Re-exported on purpose: `from .beats import Checklist, _font, item_count`
# meant this before the split and has to keep meaning it. `__all__` is what
# says the unused-looking names above are the package's surface, not leftovers.
__all__ = [
    "Beat", "BEATS", "item_count", "make_beat",
    "ChapterCard", "Checklist", "Stat", "Compare", "Quote",
    "Grid", "Logos", "Steps", "Split",
    "Bars", "Gauge", "Dial",
    "Timeline", "Chart", "Spectrum",
    "Callout", "Diagram", "Map", "Anatomy",
    "DRAW", "POP", "RISE",
]

BEATS = {
    "chapter": ChapterCard,
    "checklist": Checklist,
    "stat": Stat,
    "compare": Compare,
    "quote": Quote,
    "bars": Bars,
    "grid": Grid,
    "steps": Steps,
    "logos": Logos,
    "gauge": Gauge,
    "dial": Dial,
    "callout": Callout,
    "diagram": Diagram,
    "split": Split,
    "timeline": Timeline,
    "chart": Chart,
    "map": Map,
    "anatomy": Anatomy,
    "spectrum": Spectrum,
}

# How many things a beat reveals, which is what its `reveals` list has to be as
# long as. A chapter card reveals nothing on a clock — it settles as one block.
_COUNT = {
    "chapter": lambda p: 0,
    "checklist": lambda p: len(p[0]),
    "stat": lambda p: 1,
    "compare": lambda p: len(p[1]) + len(p[3]) + (2 if len(p) > 4 and p[4] else 0),
    "quote": lambda p: 1,
    "bars": lambda p: len(p[0]),
    "grid": lambda p: len(p[0]),
    "steps": lambda p: len(p[0]),
    "logos": lambda p: len(p[0]),
    "gauge": lambda p: 2,
    # A scale with no needle is one reveal, not two — see `Dial`. A script
    # that describes the instrument rather than a reading on it gets a single
    # caption chunk, and asking for two would shunt its scale a line late.
    "dial": lambda p: 2 if len(p) > 1 and p[1] is not None else 1,
    "callout": lambda p: len(p[1]),
    "diagram": lambda p: len(p[0]),
    "split": lambda p: 2,
    "timeline": lambda p: len(p[0]),
    # A line and its marked moment: two reveals, or one if nothing is marked.
    "chart": lambda p: 2 if len(p) > 2 and p[2] is not None else 1,
    "map": lambda p: len(p[0]),
    "anatomy": lambda p: len(p[0]),
    # The sweep, then the notch.
    "spectrum": lambda p: 2,
}


def item_count(graphic: str, payload: tuple) -> int:
    """Reveal count for a beat, so `build` can size its `reveals` list."""
    try:
        return _COUNT[graphic](payload)
    except KeyError:
        raise ValueError(f"unknown beat {graphic!r} — "
                         f"known: {', '.join(sorted(BEATS))}") from None


def make_beat(shot, brand: Brand, frame: Frame):
    """Build the prepared object for a `Shot` that is not a still photograph.

    This is the factory `render_shots` takes, which is what lets the long-form
    vocabulary — the drawn beats and video clips — extend the shorts' engine
    without the shorts knowing either exists.
    """
    if shot.clip is not None:
        from ..clip import VideoShot
        return VideoShot(shot.clip, shot.hold, frame=frame, brand=brand,
                         zoom=shot.zoom if shot.zoom > 1.0 else 1.06,
                         label=shot.payload or None,
                         note=shot.note,
                         begin=shot.clip_at,
                         ax=shot.clip_ax, ay=shot.clip_ay)
    if shot.graphic is None:
        return None
    try:
        cls = BEATS[shot.graphic]
    except KeyError:
        raise ValueError(f"unknown beat {shot.graphic!r} — "
                         f"known: {', '.join(sorted(BEATS))}") from None
    return cls(*shot.payload, brand=brand, frame=frame,
               backdrop=shot.backdrop, picture=getattr(shot, "picture", None),
               reveals=shot.reveals, marks=shot.marks,
               start=shot.start, hold=shot.hold)
