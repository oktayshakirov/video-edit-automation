"""Bird chirps, five-in/five-out breathing — vertical Short, the long form's companion.

The Short of `tinnitus-long/bird-chirps-55-breathing-20min.py`: same track,
same pattern, same look (`SparrowBranch`, this pair's own) at the long form's
period. A comfort session like its long form — the calls sit in 1-8 kHz but
a third of the track is silence between them, so no masking line (see that
file's docstring).

* **`cycles=4` at five-in/five-out**, a 40s breathing block, the natural
  length for a ~55-60s Short.
* **`look_period=60.0`**, the long form's loop, so the two move alike.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/bird-chirps-55-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.bird_chirps_55 import SparrowBranch

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Bird Chirps + Breathing for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "1.wav"

INHALE, HOLD, EXHALE, CYCLES = 5.0, 0.0, 5.0, 4
LOOP = 6 * (INHALE + HOLD + EXHALE)    # the long form's 60.0
LOOK = SparrowBranch

INTRO = [
    ("Bird chirps from Feathered Tunes,",
     "with five in, five out breathing.",),
    ("Keep it low and comfortable,",
     "and follow the circle.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-bird-chirps-55"),
        bed_file=BED_FILE, bed_file_skip=10.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK, look_period=LOOP,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Bird Chirps", pattern="5-in, 5-out breathing",
        accent="orange", look=LOOK)
    print(thumb)
