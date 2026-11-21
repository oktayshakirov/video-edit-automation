"""Pink Noise, box breathing (4-4-4-4) on the box guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/pink-noise-box-breathing-60min.py`: same bed
(*Rose Haze*, pink noise, Colors of Calm), same pattern, same guide, same
look (`RoseMere`, this pair's own) at the long form's period. A masking bed
like its long form (see that file's docstring for the measurements), so it
carries the partial-masking level line.

* **Narrated, like its long form**, in three cards rather than six: the
  sound, the level line and the count.
* **`cycles=2` at 4-4-4-4**, a 32s breathing block - the 16s cycle is
  close to 4-7-8's 19s, which took two.
* **`look_period=64.0`**, the long form's loop, so the two move alike.
* **`bed_file_skip=30.0`**, well past the render's 3s fade in.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/pink-noise-box-breathing-short.py
"""

import importlib.util
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.rose_haze_box import RoseMere

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Pink Noise for Tinnitus + Box Breathing (Short).mp4"
LONG = Path(__file__).resolve().parents[1] / "tinnitus-long" / "pink-noise-box-breathing-60min.py"

INHALE, HOLD, EXHALE, REST, CYCLES = 4.0, 4.0, 4.0, 4.0, 2
LOOP = 4 * (INHALE + HOLD + EXHALE + REST)    # the long form's 64.0
LOOK = RoseMere
GUIDE = "box"

INTRO = [
    ("Soft pink noise,", "with box breathing."),
    ("Set it just below your tinnitus,", "then follow the dot."),
    ("In for four, hold for four,", "out for four, hold for four."),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]


def bed_file() -> Path:
    """The long form's bed: the same render of Rose Haze."""
    spec = importlib.util.spec_from_file_location("pink_long", LONG)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.rose_haze()


if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-pink-noise-box"),
        bed_file=bed_file(), bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Pink Noise", pattern="box breathing",
        accent="cyan", look=LOOK)
    print(thumb)
