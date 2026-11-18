"""Brown Noise, 4-7-8 breathing on the clock guide, 60 minutes - long-form sound therapy.

**E25, the first of four sessions led by a named noise** (`projects/
tinnitus.md`, "Lead with a named masking noise"): the title and the cover
start with "Brown Noise". **Session queue row 6:** 4-7-8 on the `clock`
guide - the exercise has shipped on the ring and the path, the clock has
shipped once (`soft-orbit-6666-breathing`).

The bed is *Cloudscape Serenity* from the app's White Noise Therapy album
(tinnitushelp.me/zen/white-noise; the streaming release is titled "Infinite
Horizons"), pulled from DistroKid as a ten-minute 320k MP3 - the first bed
fetched by the skill itself rather than dropped by the editor
(`docs/video/projects/tinnitus-sounds.md`, "Fetching the next track").
The album is named in the description, never in the narration. The picture
is `AmberDusk`, this pair's own look (`tinnitus/session_looks/
cloudscape_478.py`): a warm dusk over three ridges of hills. Fully generated.

* **A deep brown-style noise, and a comfort bed - measured.** `band_energy`
  over nineteen 30s windows: **<200 Hz 74-76% (mean 75), 200 Hz-1 kHz
  24-25%, 1-4 kHz 0.2%, 4-8 kHz 0.0%, >8 kHz 0.0%**; centroid 144 Hz.
  Spectral flatness ~0.56 in every octave up to 320 Hz - broadband noise,
  not tones - flat to ~300 Hz and falling steeply above. Our generated
  brown noise measures 96 / 3.1 / 0.6 / 0.1 / 0.1, so "brown noise" is a
  fair name for the sound and still no masking claim: there is almost
  nothing where a high tinnitus sits. The copy is comfort copy ("keep it
  low"), no masking line and no denial (`projects/tinnitus.md`, "A comfort
  session is not a masking session"). Always on: 0.03% of 100ms windows
  below -50 dB, median -19.8 dB.
* **The recording is not a loop** (self-correlation at most 0.016), so it is
  tiled with `bed_file_loop=True`. It fades in over its first six seconds
  (-41 dB to -19.6 dB) and runs flat to the end, so `TRIM` takes 6.0s to
  599.9s.
* **`inhale=4, hold=7, exhale=8`**, a 19s cycle, **`loop=57.0`** (three
  cycles). **60 minutes: 36s intro, 3534s body (62 loops), 30s outro.** The
  hold is seven seconds, so the intro says once to breathe normally if it is
  too long (`projects/tinnitus.md`, "Copy").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/brown-noise-478-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.cloudscape_478 import AmberDusk

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E25 a named masking noise leads the session (white-noise sessions "
          "47 and 7.6 views a day vs themed 0.6-4); 'brown noise for tinnitus' "
          "2026-11-18: Mind Amend 10.4M-57.8M, Kerry Mac 1 hour 2.5M, all plain "
          "beds with no guide; E13 queue row 6 (4-7-8, clock)")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Brown Noise for Tinnitus + 4-7-8 Breathing (1 Hour).mp4"
SOURCE = DESKTOP / "CloudscapeSerenity.mp3"
WORK = Path("/tmp/tinnitus-long-asmr-brown-noise-478-60min")
TRIM = (6.0, 599.9)          # a six-second fade in; flat to the end

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 4.0, 7.0, 8.0, 0.0
LOOP = 3 * (INHALE + HOLD + EXHALE + REST)    # 57.0
LOOK = AmberDusk
GUIDE = "clock"

# What the sound is, how loud to keep it (comfort, not masking), the
# pattern, and the way out of the seven-second hold. Not the Soft Orbit or
# Wild Echoes lines.
INTRO = [
    ("An hour of deep, soft brown noise,",
     "like a far-off wind over the hills."),
    ("Keep it low,", "somewhere it can sit in the background."),
    ("Watch the hand go round the dial.",),
    ("In for four, hold for seven,", "and out slowly for eight."),
    ("If the hold feels too long,", "just breathe normally."),
]

OUTRO = [
    ("The hour is over.",),
    ("Let the count go,", "and let your breath find its own way."),
    ("Bring the sound down a little at a time,",
     "and take your time getting up."),
    ("Come back whenever the evening needs it.",),
]


def trimmed_source() -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK.parent / f"{WORK.name}-src.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(TRIM[0]),
                    "-to", str(TRIM[1]), "-i", str(SOURCE), "-ar", "48000",
                    str(out)], check=True)
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
        intro_len=36.0,
        outro_len=30.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # E25: the named noise leads, the exercise takes the chip
    # (`docs/video/thumbnails.md`). Blue, the complement of the amber dusk.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Brown Noise", pattern="4-7-8 breathing",
        accent="blue", look=LOOK)
    print(thumb)
