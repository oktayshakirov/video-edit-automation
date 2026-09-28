"""Cat purring, 4-in/6-out breathing, 20 minutes — long-form sound therapy.

**Built from `waterfall-478-breathing-20min.py`, and it is deliberately not a
masking session.** The source is a real recording, so it takes `bed_file` like
the waterfall does, but two measured facts about *this* recording change what
the video is allowed to be:

* **`band_energy` on it: 85.3% below 200 Hz, 14.0% in 200 Hz–1 kHz, 0.67% in
  1–4 kHz, 0.03% in 4–8 kHz.** Fundamental 27 Hz with amplitude modulation at
  27 Hz, which is a domestic purr exactly where the literature puts one. That
  is *less* reach than the old album tracks had, so this bed covers almost
  nothing in the band tinnitus actually occupies. **The channel's usual "set it
  just below your tinnitus" angle is meaningless here and the copy does not use
  it.** The site's own `zen/cat-purr-sounds` page does describe purrs as
  masking; this recording does not support that, and the measurement wins over
  the page. The intro says outright that it will not cover a high ringing.
* **The source is 600s and the piece is 1200s.** `bed_file` refuses a source
  shorter than the runtime, on purpose, because a trimmed recording has no
  seam. So this is the first build of **`bed_file_loop=True`**, which
  crossfades the recording onto itself with `soundbed.tile`. Measured on the
  finished 1200s bed with `soundbed.seam_drop`: **-0.13 dB** across the splice,
  which is inaudible, and `band_energy` is unchanged by tiling as it must be.

**So this is the first of a new session class: a comfort session.** Not sound
*coverage* but sound as company, which is the honest product a 27 Hz bed can
be. It still carries a breathing block, because lowering arousal is the thing
the video can actually claim.

* **`inhale=4.0, exhale=6.0, hold=0`** — the engine's own unhurried default, a
  10s cycle, and pointedly not the waterfall pair's named 4-7-8. A comfort
  piece invites breathing; it does not teach a technique.
* **`loop=30.0`** (three 10s cycles) with **60s intro, 1110s body, 30s outro**
  = 1200s exactly. 1110 is 37 whole loops, which is the constraint
  `render_asmr_long` raises on.
* **A 60s intro, the longest on the channel** — the user's brief allowed up to
  a minute, and a session whose premise is counterintuitive ("this will not
  mask anything") needs the room to say so and still arrive somewhere warm.
* **The last card announces the circle before it arrives** ("in a moment a
  circle will appear"). `intro_at` and `reveal` put a deliberate gap between
  the final card and the ring's entrance, and in review that gap read as the
  video having stopped rather than as a breath before it starts. A card that
  says what is coming turns the same silence into a pause.
* **Nothing in the copy places the listener at a time of day.** An earlier cut
  said "at three in the morning"; it is a smaller audience than the one the
  video has, and someone using this at noon should not be told they are the
  exception.
* **A warm amber palette and a fresh seed** (7 default, 42 white-noise 478, 17
  waterfall), so this reads as hearth-warm on sight against a channel of blue,
  teal and violet sessions. The thumbnail accent is cyan for the same reason
  the waterfall's was orange: a cool number on a warm field.
* **No medical claims, and no cure implied.** It names the sound, says what it
  will not do, and says how to set the level.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/cat-purr-comfort-20min.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Cat Purring for Tinnitus and Calm (20 Minutes).mp4"
BED_FILE = DESKTOP / "1.wav"

MINUTES = 20.0
INHALE, HOLD, EXHALE = 4.0, 0.0, 6.0
LOOP = 3 * (INHALE + HOLD + EXHALE)  # 30.0 — three whole cycles
INTRO_LEN, OUTRO_LEN = 60.0, 30.0

# Fresh from every other session on the channel.
SEED = 23

# (bg_deep, nebula_a, nebula_b, ring) — a near-black warm brown void, amber
# mid cloud, pale cream highlight, soft gold ring. bg_deep keeps roughly the
# default's luminance so `nebula_canvas`'s mostly-void composition still
# reads; the warmth is carried by the cloud and the ring, which is what makes
# this one look like a hearth rather than water or a night sky.
PALETTE = ((16, 10, 6), (128, 74, 24), (244, 206, 150), (250, 228, 190))

# What the sound is, then the honest limit, then what it *is* for, then the
# one setting that matters, then the breathing. The limit goes third from the
# top on purpose: someone who came looking for masking should find out in the
# first fifteen seconds, not after twenty minutes.
INTRO = [
    ("Twenty minutes of cat purring.",),
    ("A purr sits remarkably low.",
     "Around twenty-seven hertz, steady and rhythmic.",),
    ("It will not cover your tinnitus.",
     "There is almost no high sound in a purr,",
     "so a ringing or a hiss will still be there.",),
    ("It is here for company instead.",
     "Something warm in the room with you.",),
    ("Keep the volume low and comfortable.",
     "It should feel nearby, not on top of you.",),
    ("In a moment a circle will appear.",
     "Follow it, and let your breathing settle:",
     "four counts in, six counts out.",),
]

# Not a subscribe card. A piece built to lower arousal cannot end by asking
# for something.
OUTRO = [
    ("That is twenty minutes.",),
    ("If it helped, start it again",
     "and take another round.",),
    ("There are other sounds and lengths",
     "on the channel for when you want them.",),
]

if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=Path("/tmp/tinnitus-long-asmr-cat-purr-20min"),
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=BED_FILE,
        # The new path: 600s of source under a 1200s piece. See the docstring
        # for the measured seam.
        bed_file_loop=True,
        bed_file_xfade=8.0,
        intro=INTRO,
        outro=OUTRO,
        intro_len=INTRO_LEN,
        outro_len=OUTRO_LEN,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE,
        seed=SEED, palette=PALETTE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # `render_session_thumb`, not `render_thumb` — a session has no photograph.
    # Same seed and palette as the video. Cyan accent against the amber field,
    # the mirror of the waterfall's orange against teal.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Cat Purring", pattern="4 in / 6 out", emoji="\U0001F431",
        seed=SEED, palette=PALETTE, accent="cyan")
    print(thumb)
