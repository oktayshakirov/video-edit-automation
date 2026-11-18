"""Brown Noise, 4-7-8 breathing on the clock guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/brown-noise-478-breathing-60min.py`: same
recording (*Cloudscape Serenity*), same pattern, same guide, same look
(`AmberDusk`, this pair's own) at the long form's period. A comfort bed like
its long form (see that file's docstring for the measurements), so it makes
no masking claim and keeps a "keep it low" level line.

* **`cycles=2` at 4-7-8**, a 38s breathing block, as `wild-echoes-478`.
* **`look_period=57.0`**, the long form's loop, so the two move alike.
* **`bed_file_skip=30.0`**, well past the recording's six-second fade in.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/brown-noise-478-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.cloudscape_478 import AmberDusk

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Brown Noise for Tinnitus + 4-7-8 Breathing (Short).mp4"
BED_FILE = DESKTOP / "CloudscapeSerenity.mp3"

INHALE, HOLD, EXHALE, REST, CYCLES = 4.0, 7.0, 8.0, 0.0, 2
LOOP = 3 * (INHALE + HOLD + EXHALE + REST)    # the long form's 57.0
LOOK = AmberDusk
GUIDE = "clock"

INTRO = [
    ("Deep, soft brown noise,",
     ("with 4-7-8 breathing.", "with four, seven, eight breathing.")),
    ("Keep it low and easy,",),
    ("then watch the hand go round the dial.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-brown-noise-478"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Brown Noise", pattern="4-7-8 breathing",
        accent="blue", look=LOOK)
    print(thumb)
