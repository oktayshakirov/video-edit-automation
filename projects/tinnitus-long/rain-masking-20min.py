"""Steady rain, 4-in/6-out breathing, 20 minutes — long-form sound therapy.

**Built from `cat-purr-comfort-20min.py`, and it lands on the other side of
the line that file drew.** Same path — one real recording through `bed_file`,
tiled to length with `bed_file_loop` — but this recording measures as a
masking bed, so the channel's partial-masking angle is back.

* **`band_energy` on it** (four 30s windows, 0s to 540s, all within a point
  of each other): **~10% below 200 Hz, ~14% in 200 Hz–1 kHz, ~34% in
  1–4 kHz, ~34% in 4–8 kHz, ~8% above 8 kHz.** Two-thirds of the energy sits
  in 1–8 kHz, which is the band tinnitus usually occupies and more reach up
  there than the generated pink bed has (17% / 9%). The purr was 0.67% in
  1–4 kHz. So "set it just below your tinnitus" describes an adjustment that
  does something here, and the copy says it.
* **Steady, with no thunder.** 1s RMS over the whole file ranges -34 to
  -28.9 dB and no second rises 3 dB over the median — nothing sudden for a
  listener with hyperacusis to brace against, which is why the intro can say
  so.
* **`bed_file_skip=35`.** The recording eases in: -34 dB at the start,
  reaching the -30 dB it then holds for nine minutes at about 35s. Tiling
  from 0 would crossfade the loud end onto the quiet start every repeat, a
  4 dB sag at each seam. Skipping past the build-in leaves 565s of flat
  source, so both seams join level audio to level audio.
* **`loop=30.0`** (three 10s cycles) with **45s intro, 1110s body, 45s
  outro** = 1200s exactly; 1110 is 37 whole loops. Not the cat-purr's
  60/30: this intro reads in 32.4s, so a 60s window left ~25s of rain over an
  empty frame before the ring, which the "a circle will appear" card cannot
  carry. At 45 the ring starts ~6s after the last word. The outro takes the
  other 15s, as rain under the closing cards rather than a gap before the
  ring.
* **The last card announces the circle**, the cat-purr lesson: a gap before
  the ring with no warning reads as the video having stopped.
* **A slate-blue night palette and a fresh seed** (7, 42, 17, 23 taken) —
  cooler and greyer than the 4-7-8 white-noise blue and nothing like the
  waterfall's teal, so it reads as rain on a window rather than water in
  general. Yellow thumbnail accent: a lit window against a wet night.
* **No medical claims, and no cure implied.** It names the sound, says how to
  set the level, and invites the breath.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/rain-masking-20min.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Rain Sounds for Tinnitus (20 Minutes).mp4"
BED_FILE = DESKTOP / "Rain.mp3"
BED_SKIP = 35.0  # past the recording's own build-in; see the docstring

MINUTES = 20.0
INHALE, HOLD, EXHALE = 4.0, 0.0, 6.0
LOOP = 3 * (INHALE + HOLD + EXHALE)  # 30.0 — three whole cycles
INTRO_LEN, OUTRO_LEN = 45.0, 45.0

SEED = 31

# (bg_deep, nebula_a, nebula_b, ring) — near-black blue-grey void, slate
# cloud, silver highlight, pale rain-grey ring.
PALETTE = ((9, 12, 18), (50, 64, 96), (180, 196, 224), (222, 230, 242))

# What the sound is, what it is like, the one setting that matters, why, then
# the breathing. The level instruction is the channel's angle and the reason
# to pick this over any other rain video, so it comes before the ring.
INTRO = [
    ("Twenty minutes of steady rain.",),
    ("Soft and even from start to finish,",
     "with nothing sudden in it.",),
    ("Set the volume just below your tinnitus.",),
    ("You should still hear it,",
     "faintly, underneath the rain.",
     "That is the point.",),
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
        workdir=Path("/tmp/tinnitus-long-asmr-rain-20min"),
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=BED_FILE,
        bed_file_skip=BED_SKIP,
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

    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Rain Sounds", pattern="4 in / 6 out",
        emoji="\U0001F327️",
        seed=SEED, palette=PALETTE, accent="yellow")
    print(thumb)
