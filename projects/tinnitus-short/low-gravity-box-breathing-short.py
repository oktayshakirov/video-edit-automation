"""Low Gravity, box breathing on the box guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/low-gravity-box-breathing-60min.py`: same
recording, same pattern, same guide, same look (`LowOrbit`, this pair's own)
at the long form's period. A comfort session like its long form (see that
file's docstring for the measurements), so no masking line.

* **`cycles=2` at 4-4-4-4**, a 32s breathing block, which puts the Short
  near 50s with the narration.
* **`look_period=64.0`**, the long form's loop, so the two move alike.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/low-gravity-box-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.low_gravity_box import LowOrbit

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Box Breathing + Space Sounds for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "LowGravity.wav"

INHALE, HOLD, EXHALE, REST, CYCLES = 4.0, 4.0, 4.0, 4.0, 2
LOOP = 4 * (INHALE + HOLD + EXHALE + REST)    # the long form's 64.0
LOOK = LowOrbit
GUIDE = "box"

INTRO = [
    ("Space sounds,", "with box breathing."),
    ("Keep it low and comfortable,",),
    ("then follow the dot around the square.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-low-gravity-box"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Space Sounds", pattern="box breathing",
        accent="yellow", look=LOOK)
    print(thumb)
