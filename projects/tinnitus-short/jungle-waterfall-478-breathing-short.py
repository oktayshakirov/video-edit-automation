"""Jungle waterfall + birdsong, 4-7-8 breathing — vertical Short, the long form's companion.

The Short of `tinnitus-long/jungle-waterfall-478-breathing-20min.py`, not a
trailer for it: same recording, same pattern, same look (`NightFronds`, this
pair's own) at the same period, laid out for portrait (fronds hang from the top corners and rise
from the bottom, leaving the middle band to the ring and the captions).

* **`cycles=2` at 4-7-8**, a 38s breathing block, the natural length for a
  ~55-60s Short — the same reasoning as the waterfall pair.
* **`look_period=57.0`**, the long form's loop, so the two move alike.
* **The outro asks for a save, and nothing else.** TikTok and Instagram never
  get the twenty-minute version, so "there's a full version on the channel"
  points at nothing there. A session is something to come back to, which
  makes a save the right ask here (unlike an article Short; see
  `docs/video/projects/tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/jungle-waterfall-478-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.jungle_waterfall_478 import NightFronds

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Jungle Waterfall + 4-7-8 Breathing for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "WaterfallBirds.wav"

INHALE, HOLD, EXHALE, CYCLES = 4.0, 7.0, 8.0, 2
LOOP = 3 * (INHALE + HOLD + EXHALE)    # the long form's 57.0
LOOK = NightFronds

INTRO = [
    ("A waterfall, with birdsong,",
     ("and 4-7-8 breathing.", "and four, seven, eight breathing.")),
    ("Set it just below your tinnitus,",
     "so you can still hear it faintly.",),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-jungle-waterfall-478"),
        bed_file=BED_FILE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK, look_period=LOOP,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Jungle Waterfall", pattern="4-7-8 breathing",
        accent="orange", look=LOOK)
    print(thumb)
