"""Fan Noise, triangle (4-4-4) breathing on the path guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/fan-noise-444-breathing-60min.py`: same
recording (*Ambient Fan*), same pattern, same guide, same look
(`NightDraft`, this pair's own) at the long form's period. A comfort bed like
its long form (see that file's docstring for the measurements), so it makes
no masking claim and keeps a "keep it low" level line.

* **`cycles=3` at 4-4-4**, a 36s breathing block - the 12s cycle is short
  enough for three, where 4-7-8's 19s took two.
* **`look_period=60.0`**, the long form's loop, so the two move alike.
* **`bed_file_skip=30.0`**, well past the recording's one-second fade in.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/fan-noise-444-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.ambient_fan_444 import NightDraft

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Fan Noise for Tinnitus + Triangle Breathing (Short).mp4"
BED_FILE = DESKTOP / "2fan.mp3"

INHALE, HOLD, EXHALE, REST, CYCLES = 4.0, 4.0, 4.0, 0.0, 3
LOOP = 5 * (INHALE + HOLD + EXHALE + REST)    # the long form's 60.0
LOOK = NightDraft
GUIDE = "path"

INTRO = [
    ("A fan's low, steady hum,", "with triangle breathing."),
    ("Keep it low,", "then follow the dot."),
    ("In for four, hold for four,", "and out for four."),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-fan-noise-444"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Fan Noise", pattern="triangle breathing",
        accent="yellow", look=LOOK)
    print(thumb)
