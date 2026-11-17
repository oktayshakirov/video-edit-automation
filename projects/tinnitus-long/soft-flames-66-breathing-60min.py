"""Soft Flames, coherent 6-6 breathing on the path guide, 60 minutes - long-form sound therapy.

**Session queue row 5 (E12 + E13):** an hour, coherent breathing (in for
six, out for six, no holds - five breaths a minute) on the `path` guide.
The exercise has not shipped before; the path guide has
(`wild-echoes-478-breathing`, `tranquil-zenith-21-breathing`).

The bed is *Soft Flames & Breezes* from the app's Fireside Harmony album
(tinnitushelp.me/zen/fire-sounds; the streaming release is titled
"Fireside Comfort"), supplied as a ten-minute 32-bit WAV. The album is named
in the description, never in the narration (`docs/video/projects/
tinnitus.md`, 2026-11-03). The used and unused tracks are in
`docs/video/projects/tinnitus-sounds.md`. The picture is `FiresideBreeze`,
this pair's own look (`tinnitus/session_looks/soft_flames_66.py`): a
campfire at night, flames leaning in a breeze, embers drifting off it.
Fully generated.

* **This is a comfort session, not a masking one - measured.**
  `band_energy` over nineteen 30s windows: **<200 Hz 1-68% (mean 25),
  200 Hz-1 kHz 27-87% (mean 59), 1-4 kHz 4-31% (mean 15), 4-8 kHz
  0.1-1.2% (mean 0.6), >8 kHz 0.1%.** Always on (no 100ms window below
  -50 dB; median -30.6 dB), so it is a steady bed, but with almost nothing
  where a high whistling tinnitus usually sits. The album page sells
  "a pleasant and natural masking effect"; the file does not support a
  masking line, so the copy makes no masking claim and no denial either
  (`projects/tinnitus.md`, "A comfort session is not a masking session"):
  the intro says "keep the volume low and comfortable", as Low Gravity did.
* **The recording is not a loop** (self-correlation at most 0.021), so it
  is tiled with `bed_file_loop=True`. It has no fade in and dips in its last
  second, so `TRIM` takes 0.0s to 599.0s.
* **`inhale=6, exhale=6`**, a 12s cycle, **`loop=60.0`** (five cycles).
  **60 minutes: 30s intro, 3540s body (59 loops), 30s outro.** No holds,
  so the way out is for the long phases instead ("breathe at your own
  pace"). "Coherent breathing" goes in the title, never a benefit: it is
  described, not sold.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/soft-flames-66-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.soft_flames_66 import FiresideBreeze

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E13 session queue row 5 (coherent 6-6 breathing, path guide); "
          "E12 hour-plus sessions stand out")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Coherent Breathing + Fireplace Sounds for Tinnitus (1 Hour).mp4"
SOURCE = DESKTOP / "soft flames.wav"
WORK = Path("/tmp/tinnitus-long-asmr-soft-flames-66-60min")
TRIM = (0.0, 599.0)          # no fade in; the last second dips

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 6.0, 0.0, 6.0, 0.0
LOOP = 5 * (INHALE + HOLD + EXHALE + REST)    # 60.0
LOOK = FiresideBreeze
GUIDE = "path"

# What the sound is, how loud to keep it (comfort, not masking), the
# pattern, and the way out of the long phases.
INTRO = [
    ("An hour by a quiet fire,", "soft flames and a gentle breeze."),
    ("Keep the volume low and comfortable.",),
    ("Follow the dot: in for six, out for six.",),
    ("If six feels long,", "breathe at your own pace."),
]

# Not the Tranquil Zenith close.
OUTRO = [
    ("The hour is done.",),
    ("Let your breath settle back on its own.",),
    ("Bring the sound down gently,", "and stay a moment in the quiet."),
    ("Come back whenever you want to sit by the fire.",),
]


def trimmed_source() -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK.parent / f"{WORK.name}-src.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(TRIM[0]),
                    "-to", str(TRIM[1]), "-i", str(SOURCE), str(out)],
                   check=True)
    return out


if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=WORK,
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=trimmed_source(),
        bed_file_loop=True,
        intro=INTRO,
        outro=OUTRO,
        intro_len=30.0,
        outro_len=30.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # "Fireplace sounds" is a sound people type (the album page's own
    # title), so it leads and the exercise takes the chip
    # (`docs/video/thumbnails.md`). Cyan, the complement of the fire.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Fireplace Sounds", pattern="6-in, 6-out breathing",
        accent="cyan", look=LOOK)
    print(thumb)
