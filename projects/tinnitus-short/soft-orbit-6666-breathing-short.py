"""Soft Orbit, 6-6-6-6 breathing on the clock guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/soft-orbit-6666-breathing-60min.py`: same
recording, same pattern, same guide, same look (`RingedWorld`, this pair's
own) at the long form's period. A comfort session like its long form (see
that file's docstring for the measurements), so no masking line.

* **`cycles=2` at 6-6-6-6**, a 48s breathing block.
* **`look_period=72.0`**, the long form's loop, so the two move alike.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/soft-orbit-6666-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.soft_orbit_6666 import RingedWorld

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "6-6-6-6 Breathing + Deep Space Sounds for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "SoftOrbit.wav"

INHALE, HOLD, EXHALE, REST, CYCLES = 6.0, 6.0, 6.0, 6.0, 2
LOOP = 3 * (INHALE + HOLD + EXHALE + REST)    # the long form's 72.0
LOOK = RingedWorld
GUIDE = "clock"

INTRO = [
    ("Deep space sounds,", "with six-count breathing."),
    ("Keep it low and comfortable,",),
    ("then follow the hand around the clock.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-soft-orbit-6666"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="6-6-6-6 Breathing", pattern="deep space sounds",
        accent="cyan", look=LOOK)
    print(thumb)
