"""Soft Flames, coherent 6-6 breathing on the path guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/soft-flames-66-breathing-60min.py`: same
recording, same pattern, same guide, same look (`FiresideBreeze`, this
pair's own) at the long form's period. A comfort session like its long form
(see that file's docstring for the measurements), so it makes no masking
claim and keeps the "low and comfortable" level line.

* **`cycles=4` at six-in/six-out**, a 48s breathing block.
* **`look_period=60.0`**, the long form's loop, so the two move alike.
* **`bed_file_skip=30.0`**, past the recording's opening.
* **"even breathing", not "even breaths"**: the first cut played "breaths"
  as "breath ... s" (the editor, 2026-11-17). The cause was the pause
  padding, not the word - since fixed (`voice.md`, "A sentence gap can land
  inside the last word") - but the line was re-cut before that was found,
  and it was approved as it is.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/soft-flames-66-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.soft_flames_66 import FiresideBreeze

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Coherent Breathing + Fireplace Sounds for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "soft flames.wav"

INHALE, HOLD, EXHALE, REST, CYCLES = 6.0, 0.0, 6.0, 0.0, 4
LOOP = 5 * (INHALE + HOLD + EXHALE + REST)    # the long form's 60.0
LOOK = FiresideBreeze
GUIDE = "path"

INTRO = [
    ("Soft flames and a gentle breeze,", "with slow, even breathing."),
    ("Keep it low and comfortable,",),
    ("then follow the dot along the line.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-soft-flames-66"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Fireplace Sounds", pattern="6-in, 6-out breathing",
        accent="cyan", look=LOOK)
    print(thumb)
