"""Bird chirps, five-in/five-out breathing, 20 minutes — long-form sound therapy.

The bed is a bird-chirps track from the app's Feathered Tunes album
(tinnitushelp.me/zen/bird-sounds), supplied as a ten-minute WAV. The picture
is this video's own look, `SparrowBranch` in
`tinnitus/session_looks/bird_chirps_55.py`: a sparrow on a branch in morning
light, the picture coming into focus on each inhale.

* **This is a comfort session, not a masking one — measured.** `band_energy`
  over six 30s windows: **<1 kHz 0%, 1-4 kHz 80-82%, 4-8 kHz 18-20%, >8 kHz
  0%.** The energy sits right in the band tinnitus occupies, but it comes in
  calls: 30% of 100ms windows are below -70 dB and the longest gap is 6.2s.
  A sound that is silent a third of the time covers nothing a third of the
  time, so "set it just below your tinnitus" would describe an adjustment
  that does nothing in the gaps. The site's page says the album masks
  tinnitus; the measurement wins (`docs/video/projects/tinnitus.md`, "A
  comfort session is not a masking session"). No masking line, no denial.
* **The track is a 52-second recording looped**, not ten minutes of birds:
  `x[t]` equals `x[t + 52]` across 99% of the file, the album's own seams sit
  at every 52s at under -57 dB, and the last second is a fade-out. So the bed
  is that one period repeated (`period_source`) rather than a crossfaded
  tile: it has the album's seams and no new ones. A returning listener hears
  the same 52s of calls, as they would on the album.
* **`loudnorm` lifts the gaps more than the calls** - measured on four
  periods, +12 dB in the quietest windows against +2.5 dB on the calls. The
  floor goes from -76 to -68 dB, which is still silence.
* **Five in, five out, no holds** - a new pattern for the channel (4/6,
  4-7-8 and box are taken), unnamed as a comfort piece's should be.
  A 10s cycle, **`loop=60.0`** (six cycles). 20 minutes: 34s intro, 1140s
  body (nineteen loops), 26s outro.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/bird-chirps-55-breathing-20min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.bird_chirps_55 import (
    SparrowBranch, SparrowBranchThumb)

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = None

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Bird Chirps + Breathing for Tinnitus (20 Minutes).mp4"
SOURCE = DESKTOP / "1.wav"
WORK = Path("/tmp/tinnitus-long-asmr-bird-chirps-55-20min")
PERIOD = 52.0                # the album track's own loop length

MINUTES = 20.0
INHALE, HOLD, EXHALE = 5.0, 0.0, 5.0
LOOP = 6 * (INHALE + HOLD + EXHALE)    # 60.0
LOOK = SparrowBranch

# What the sound is, how loud to keep it, the pattern, and what to do when a
# call pulls attention away - with birdsong, that is the likely way out.
INTRO = [
    ("Twenty minutes of bird chirps,",
     "from our album, Feathered Tunes.",),
    ("Bright little calls that come and go.",
     "Keep it low and comfortable.",),
    ("Follow the circle:",
     "five in, five out.",),
    ("If a bird pulls your attention,",
     "let it, then come back to the circle.",),
]

# Not a subscribe card. A piece built to lower arousal does not end by asking
# for something.
OUTRO = [
    ("That is twenty minutes.",),
    ("If it helped, start it again",
     "and take another round.",),
    ("The whole album, Feathered Tunes,",
     "is on our website.",),
]


def period_source() -> Path:
    """The track's 52s recording, repeated past the finished length."""
    WORK.mkdir(parents=True, exist_ok=True)
    one = WORK.parent / f"{WORK.name}-period.wav"
    out = WORK.parent / f"{WORK.name}-src.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(SOURCE),
                    "-t", str(PERIOD), "-ar", "48000", "-ac", "2", str(one)],
                   check=True)
    reps = int(MINUTES * 60 // PERIOD) + 1
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", str(reps),
                    "-i", str(one), "-t", str(MINUTES * 60 + 10), str(out)],
                   check=True)
    return out


if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=WORK,
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=period_source(),
        intro=INTRO,
        outro=OUTRO,
        intro_len=34.0,
        outro_len=26.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # A still of the same look, re-cropped so the sparrow sits under the
    # chip instead of under the headline (`SparrowBranchThumb`).
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Bird Chirps", pattern="5-in, 5-out breathing",
        accent="orange", look=SparrowBranchThumb)
    print(thumb)
