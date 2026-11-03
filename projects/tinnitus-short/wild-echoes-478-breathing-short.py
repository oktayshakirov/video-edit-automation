"""Wild Echoes, 4-7-8 breathing on the path guide — vertical Short, the long form's companion.

The Short of `tinnitus-long/wild-echoes-478-breathing-60min.py`: same
recording, same pattern, same guide, same look (`FernBreath`, this pair's
own) at the long form's period. A masking session like its long form (see
that file's docstring for the measurements).

* **`cycles=2` at 4-7-8**, a 38s breathing block, the natural length for a
  ~55-60s Short, as on the earlier 4-7-8 Shorts.
* **`look_period=57.0`**, the long form's loop, so the two move alike.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/wild-echoes-478-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.wild_echoes_478 import FernBreath

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "4-7-8 Breathing + Jungle Sounds for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "WildEchoes.wav"

INHALE, HOLD, EXHALE, CYCLES = 4.0, 7.0, 8.0, 2
LOOP = 3 * (INHALE + HOLD + EXHALE)    # the long form's 57.0
LOOK = FernBreath
GUIDE = "path"

INTRO = [
    ("Jungle sounds,",
     ("with 4-7-8 breathing.", "with four, seven, eight breathing.")),
    ("Bring it down until your tinnitus",
     "is just there underneath,"),
    ("then follow the dot.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-wild-echoes-478"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Jungle Sounds", pattern="4-7-8 breathing",
        accent="orange", look=LOOK)
    print(thumb)
