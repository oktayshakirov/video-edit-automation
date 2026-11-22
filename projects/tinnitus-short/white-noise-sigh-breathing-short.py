"""High Frequency White Noise, the physiological sigh on the path guide - vertical Short, the long form's companion.

The Short of `tinnitus-long/white-noise-sigh-breathing-60min.py`: same bed
(*Ethereal Resonance*, a high-frequency white noise, White Noise Therapy),
same pattern, same guide, same look (`AuroraSnow`, this pair's own) at the
long form's period. A masking bed like its long form (see that file's
docstring for the measurements), so it carries the partial-masking level
line.

* **Narrated, like its long form**, in three cards rather than seven: the
  sound, the level line and the sigh.
* **`cycles=3` at 3-1-6**, a 30s breathing block - a 10s cycle, like the
  12s cycles that took three before.
* **`look_period=40.0`**, the long form's loop, so the two move alike.
* **`bed_file_skip=30.0`**, well past the recording's two-second rise.
* **The outro asks for a save, and nothing else** (`docs/video/projects/
  tinnitus.md`, "The Short's outro asks for a save").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/white-noise-sigh-breathing-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short
from video_automation.tinnitus.session_looks.ethereal_sigh import AuroraSnow

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "High Frequency White Noise for Tinnitus + Physiological Sigh (Short).mp4"
SOURCE = DESKTOP / "EtherealResonance.mp3"

INHALE, TOP, EXHALE, CYCLES = 3.0, 1.0, 6.0, 3
LOOP = 4 * (INHALE + TOP + EXHALE)    # the long form's 40.0
LOOK = AuroraSnow
GUIDE = "path"

INTRO = [
    ("High, bright white noise,", "with the physiological sigh."),
    ("Set it just below your tinnitus,", "then follow the dot."),
    ("Breathe in, then a short breath in on top,", "and a long breath out."),
]

OUTRO = [
    ("If this helped,",
     "save it for the next time you need it.",),
]


if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-white-noise-sigh"),
        bed_file=SOURCE, bed_file_skip=30.0,
        cycles=CYCLES, inhale=INHALE, hold=0.0, exhale=EXHALE, top=TOP,
        look=LOOK, look_period=LOOP, guide=GUIDE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="High Frequency White Noise", pattern="physiological sigh",
        accent="yellow", look=LOOK)
    print(thumb)
