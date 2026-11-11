"""Tranquil Zenith, 2:1 breathing on the path guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/tranquil-zenith-21-breathing-60min.py`: same
recording, same pattern, same guide, same look (`ZenithSea`, this pair's
own) at the long form's period. A masking session like its long form (see
that file's docstring for the measurements), so it keeps the level line.

* **`cycles=4` at four-in/eight-out**, a 48s breathing block.
* **`look_period=60.0`**, the long form's loop, so the two move alike.
* **`bed_file_skip=30.0`** clears the recording's ~11s fade in.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tranquil-zenith-21-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.tranquil_zenith_21 import ZenithSea

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "2-1 Breathing + White Noise for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "TranquilZenith.mp3"

INHALE, HOLD, EXHALE, REST, CYCLES = 4.0, 0.0, 8.0, 0.0, 4
LOOP = 5 * (INHALE + HOLD + EXHALE + REST)    # the long form's 60.0
LOOK = ZenithSea
GUIDE = "path"

INTRO = [
    ("Soft white noise,", "with a long, slow out-breath."),
    ("Set it just below your tinnitus,",),
    ("then follow the dot along the line.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-tranquil-zenith-21"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="White Noise", pattern="4-in, 8-out breathing",
        accent="yellow", look=LOOK)
    print(thumb)
