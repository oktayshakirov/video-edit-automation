"""Tinnitus masking sound + paced breathing, 5 minutes — long-form 16:9.

**The extended cut of the 60-second short, and the standard it is held to is
"the same video, longer".** Not the same format, not the same brand — the same
video. Everything the short does, this does:

* **The two album tracks, layered**, via the short's own `render_bed`. Not the
  generated noise `render_asmr_long` defaults to. Measured, both tracks are
  almost entirely below 200 Hz, and measured on the published short's own
  breathing block so is its bed — 99% under 200 Hz. That deep, hiss-free sound
  *is* the piece. Pink noise covers more of the spectrum on paper and is a
  different video.
* **`inhale` / `exhale` and the seconds counting down, inside the ring.** The
  first long cut had a silent circle and nothing else, which is a screensaver.
  The count is the instruction.
* **Same ring geometry**, `r_min=150`, `r_max=330`, on the same 4-in / 6-out.

What genuinely has to change going long:

* **16:9, not 9:16.** A watch-page video, not a Short.
* **The picture is a seamless 60s loop repeated five times**, per
  `longform/asmr.py`. 60s is six whole breathing cycles, so the ring, the
  count, the nebula drift and the watermark float all close together.

**No medical claims.** The intro says what the sound is and how to set the
level, not what it will do. And the copy does not claim broad-spectrum masking,
because this bed does not do that — it is deep and hiss-free, which is what it
is chosen for.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/masking-breathing-5min.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb

DESKTOP = Path.home() / "Desktop"
LOW = DESKTOP / "SpaceshipAmbience.mp3"     # the floor
HIGH = DESKTOP / "NebulaPulse.mp3"          # layered on top, as in the short

MINUTES = 5.0
OUT = DESKTOP / "Tinnitus Masking Sound + Paced Breathing (5 Minutes).mp4"

# The intro is instructions, and it is short on purpose — it has to be finished
# before the ring's entrance, and the entrance is the thing that says "start".
# Three jobs in order: what this is, the one setting that matters, how to follow
# the circle. The old cut spent a line saying the exercise was beginning; the
# animation does that now.
INTRO = [
    ("Five minutes of masking sound,",
     "with paced breathing.",),
    ("Set the volume just below your tinnitus.",),
    ("You should still hear the ringing",
     "faintly underneath. That is the point.",),
    ("Then follow the circle.",
     "Four seconds in, six seconds out.",),
]

# Not a subscribe card. A piece whose whole purpose is to lower arousal cannot
# end by asking for something — the ask is the arousal. So: it is over, run it
# again if it helped, and there are longer ones. No call to action, no music
# sting, and the bed is still fading under it.
OUTRO = [
    ("That is five minutes.",),
    ("If it helped, start it again",
     "and take another round.",),
    ("There are longer sessions on the channel",
     "for when you want them.",),
]

if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=Path("/tmp/tinnitus-long-asmr-5min"),
        brand=TINNITUS,
        minutes=MINUTES,
        bed_files=(LOW, HIGH),
        intro=INTRO,
        outro=OUTRO,
        # 30 + 240 + 30. The body is four whole 60s loops, and 60s is six whole
        # breathing cycles, so every period in the piece closes together.
        intro_len=30.0,
        outro_len=30.0,
        loop=60.0,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # `render_session_thumb`, not `render_thumb`. A session has no photograph to
    # find a face in, and the duration is what the viewer is scanning the grid
    # for, so the number takes the accent slot the boxed phrase takes on an
    # article thumbnail. Same seed as the video, so it is a picture of this one.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Tinnitus Masking Sound", pattern="4 in / 6 out", seed=7)
    print(thumb)
