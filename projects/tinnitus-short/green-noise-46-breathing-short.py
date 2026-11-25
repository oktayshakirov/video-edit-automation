"""Green Noise, 4-6 breathing on the clock guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/green-noise-46-breathing-60min.py`: same bed
(*Green Meadow*, green noise, Colors of Calm), same pattern, same guide,
same look (`WindMeadow`, this pair's own) at the long form's period. A
comfort bed like its long form (see that file's docstring for the
measurements), so it carries the "keep it quiet" line, not a masking one.

* **Narrated, like its long form**, in three cards: the sound, the level
  and the guide, the count.
* **`cycles=4` at 4-in/6-out**, a 40s breathing block, as the 10s 5-5
  bird-chirps Short took.
* **`look_period=60.0`**, the long form's loop, so the two move alike.
* **`bed_file_skip=30.0`**, well past the render's 3s fade in.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/green-noise-46-breathing-short.py
"""

import importlib.util
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.green_meadow_46 import WindMeadow

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Green Noise for Tinnitus + 4-6 Breathing (Short).mp4"
LONG = Path(__file__).resolve().parents[1] / "tinnitus-long" / "green-noise-46-breathing-60min.py"

INHALE, HOLD, EXHALE, REST, CYCLES = 4.0, 0.0, 6.0, 0.0, 4
LOOP = 6 * (INHALE + HOLD + EXHALE + REST)    # the long form's 60.0
LOOK = WindMeadow
GUIDE = "clock"

INTRO = [
    ("Soft green noise,", "with four-six breathing."),
    ("Keep it quiet,", "and follow the hand round the dial."),
    ("In for four,", "out for six."),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]


def bed_file() -> Path:
    """The long form's bed: the same render of Green Meadow."""
    spec = importlib.util.spec_from_file_location("green_long", LONG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.green_meadow()


if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-green-noise-46"),
        bed_file=bed_file(), bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Green Noise", pattern="4-6 breathing",
        accent="orange", look=LOOK)
    print(thumb)
