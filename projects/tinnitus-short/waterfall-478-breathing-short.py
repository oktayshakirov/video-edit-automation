"""Waterfall + pads, 4-7-8 breathing — vertical Short, the long form's companion.

**The Short version of `tinnitus-long/waterfall-478-breathing-20min.py`, not a
trailer for it.** Same pattern (4-7-8), same real-recording bed, same teal
palette, same seed — a viewer who has seen one recognises the other as the
same piece at a different length, the way the 478-white-noise pair does.

**First real build of `render_asmr_short`'s `bed_file` path.** Unlike the
white-noise sessions, this one's bed is a single already-mixed field
recording (a waterfall with pads laid under it), not a generated noise
colour and not the brand's old two-track album layering — so it goes through
`bed_file`, which trims the source and puts it through the same
`loudnorm=I=-23` and fade treatment the other two bed paths get.

* **`cycles=2` at 4-7-8** — a 38s breathing block, the natural length for a
  ~55-60s short; three cycles (57s) would leave no room for the intro/outro,
  same reasoning as the white-noise pair.
* **The intro's "4-7-8" is a `(caption, spoken)` pair**, same fix as every
  other 4-7-8 build: Kokoro/espeak reads a bare `4-7-8` as "four dash seven
  dash eight".
* **No CTA.** A piece built to lower arousal doesn't end by asking for
  something — the outro just points at the full session on the channel.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/waterfall-478-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short

SOURCE_POST = None  # off-site: a generated sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Waterfall + 4-7-8 Breathing for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "waterfall-pads.mp3"

INHALE, HOLD, EXHALE, CYCLES = 4.0, 7.0, 8.0, 2

# A fresh seed from every other session on the channel (7 default, 42 for the
# white-noise 478 pair) — a different star field for a piece that is its own
# recording, not a re-skin. The palette is what actually reads as "water".
SEED = 17

# (bg_deep, nebula_a, nebula_b, ring) — a dark teal void, teal-to-aqua cloud,
# pale foam ring. Distinct from the white-noise pair's blue so the two read
# as different sessions on sight, not just a different sound under the same
# picture.
PALETTE = ((5, 18, 18), (18, 92, 92), (140, 232, 214), (196, 246, 232))

# Opens on the hook, no lead-in silence. The caption keeps "4-7-8"; the voice
# gets "four, seven, eight" — see the module docstring.
INTRO = [
    ("A waterfall, with soft pads,",
     ("and 4-7-8 breathing.", "and four, seven, eight breathing.")),
    ("Set it just below your tinnitus,",
     "so you can still hear it faintly.",),
]

# One closing line, nothing after it — not a subscribe card.
OUTRO = [
    ("There's a full twenty-minute version",
     "of this on the channel.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-waterfall-478"),
        bed_file=BED_FILE,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        seed=SEED, palette=PALETTE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="4-7-8 Breathing", pattern="4 in / 7 hold / 8 out",
        seed=SEED, palette=PALETTE, accent="orange")
    print(thumb)
