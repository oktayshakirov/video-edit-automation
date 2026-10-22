"""Nebula Pulse, 4-7-8 breathing — vertical Short, the long form's companion.

The Short of `tinnitus-long/nebula-pulse-478-breathing-20min.py`: same track,
same pattern, same look (`StarPulse`, this pair's own) at the long form's
period. A comfort session like its long form — the track is 99.8% below
200 Hz, so no masking line (see that file's docstring).

* **`cycles=2` at 4-7-8**, a 38s breathing block, the natural length for a
  ~55-60s Short.
* **`look_period=57.0`**, the long form's loop, so the two move alike.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/nebula-pulse-478-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.nebula_pulse_478 import StarPulse

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Nebula Pulse + 4-7-8 Breathing for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "NebulaPulse.mp3"

INHALE, HOLD, EXHALE, CYCLES = 4.0, 7.0, 8.0, 2
LOOP = 3 * (INHALE + HOLD + EXHALE)    # the long form's 57.0
LOOK = StarPulse

INTRO = [
    ("Nebula Pulse, a deep, low hum,",
     ("with 4-7-8 breathing.", "with four, seven, eight breathing.")),
    ("Keep it quiet and comfortable.",
     "Four in, seven hold, eight out.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-nebula-pulse-478"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK, look_period=LOOP,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Nebula Pulse", pattern="4-7-8 breathing",
        accent="orange", look=LOOK)
    print(thumb)
