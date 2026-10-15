"""Forest chorus, box breathing — vertical Short, the long form's companion.

The Short of `tinnitus-long/forest-chorus-box-breathing-20min.py`: same
recording, same pattern, same look (`CanopyFog`, this pair's own) at the same
period.

* **`cycles=2` at 4-4-4-4**, a 32s breathing block, which with the ~19s intro
  and the save line lands the Short near 57s.
* **`look_period=32.0`**, the long form's loop, so the two move alike.
* **The level instruction is the long form's**: bring the sound up until the
  tinnitus starts to blend in, not "set it just below".
* **The outro asks for a save, and nothing else** (`docs/video/projects/tinnitus.md`,
  "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/forest-chorus-box-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.forest_chorus_box import CanopyFog

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Forest Chorus + Box Breathing for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "NaturesChorus.wav"

INHALE, HOLD, EXHALE, REST, CYCLES = 4.0, 4.0, 4.0, 4.0, 2
LOOP = 2 * (INHALE + HOLD + EXHALE + REST)    # the long form's 32.0
LOOK = CanopyFog

INTRO = [
    ("A forest chorus,", "with box breathing."),
    ("Bring the sound up slowly,", "until your tinnitus starts to blend in."),
    ("In for four, hold for four,", "out for four, hold for four."),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-forest-chorus-box"),
        bed_file=BED_FILE, bed_file_skip=60.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK, look_period=LOOP,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Forest Chorus", pattern="box breathing",
        accent="yellow", look=LOOK)
    print(thumb)
