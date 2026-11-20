"""Fan Noise, triangle (4-4-4) breathing on the path guide, 60 minutes - long-form sound therapy.

**E25, the second of four sessions led by a named noise** (`projects/
tinnitus.md`, "Lead with a named masking noise"): the title and the cover
start with "Fan Noise". **Session queue row 7:** triangle 4-4-4 (inhale,
hold, exhale) on the `path` guide - a new exercise on a guide that has
shipped three times.

The bed is *Ambient Fan* from the app's Background Blur album
(tinnitushelp.me/zen/evening-sounds; the DistroKid release has the same
name), pulled from DistroKid as a twenty-minute 320k MP3 at 44.1 kHz that
saves as `2fan.mp3`. The album is named in the description, never in the
narration. The picture is `NightDraft`, this pair's own look
(`tinnitus/session_looks/ambient_fan_444.py`): sheer curtains over a
moonlit window, stirring in a fan's draught. Fully generated.

**Rain was picked first and is already used.** Nature Inspired Sound
Therapy's "Rain" (Earth's Lullaby) measured exactly as `rain-masking-20min`'s
`Rain.mp3` docstring records it - 10 / 14 / 34 / 34 / 8% across the bands,
-34 dB rising to -30 dB by 35s, -34 to -28.9 dB overall - so that session's
bed was this track, and the ledger now says so.

* **A low fan hum, and a comfort bed - measured.** `band_energy` over
  thirty-nine 30s windows: **<200 Hz 77-82% (mean 80), 200 Hz-1 kHz 16-22%,
  1-4 kHz 1.2-1.5%, 4-8 kHz 0.03%, >8 kHz 0.00%**; centroid 164 Hz. 65% of
  the energy sits in the 40-80 Hz octave at spectral flatness 0.03 - the
  motor's hum, a tone rather than a noise - with a broadband whoosh above
  it (flatness 0.26-0.47 from 320 Hz to 2.5 kHz). Almost nothing where a
  high tinnitus sits, so no masking line and no denial: comfort copy
  ("keep it low"), as `projects/tinnitus.md`, "A comfort session is not a
  masking session". "Fan noise" names the sound, not a claim about it.
* **Steady and always on.** 10s RMS -16.9 to -14.7 dB over the whole file;
  no second rises 3 dB over the median (-15.5 dB); 0.04% of 100ms windows
  below -50 dB, all of them in the fade out.
* **Not a loop** (self-correlation at 10-600s lags at most 0.083), so it is
  tiled with `bed_file_loop=True`. A one-second fade in (-30 dB to -17 dB)
  and a four-second fade out, so `TRIM` takes 1.0s to 1196.0s.
* **`inhale=4, hold=4, exhale=4`**, a 12s cycle, **`loop=60.0`** (five
  cycles). **60 minutes: 30s intro, 3540s body (59 loops), 30s outro.** The
  hold is four seconds, under the six that require the line, but the intro
  still gives the way out of it (`projects/tinnitus.md`, "Vary the
  pattern").

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/fan-noise-444-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.ambient_fan_444 import NightDraft

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E25 a named noise leads the session (white-noise sessions 47 and "
          "7.6 views a day vs themed 0.6-4); 'fan noise for tinnitus' "
          "2026-11-20: Relaxing White Noise fan beds 127M and 51M, SleepDroid "
          "box fan 7.6M, Anatole Patel 'Virtual Fan Sound for Tinnitus' 19.5K, "
          "all plain beds with no guide; 'triangle breathing' Pocket Breath "
          "Coach 5.8K, YOGABODY 41K; E13 queue row 7 (4-4-4, path)")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Fan Noise for Tinnitus + Triangle Breathing (1 Hour).mp4"
SOURCE = DESKTOP / "2fan.mp3"
WORK = Path("/tmp/tinnitus-long-asmr-fan-noise-444-60min")
TRIM = (1.0, 1196.0)         # a one-second fade in, a four-second fade out

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 4.0, 4.0, 4.0, 0.0
LOOP = 5 * (INHALE + HOLD + EXHALE + REST)    # 60.0
LOOK = NightDraft
GUIDE = "path"

# What the sound is, how loud to keep it (comfort, not masking), the
# pattern, and the way out of the hold. Not the Brown Noise lines.
#
# A 30s intro_len leaves 24s for these before the guide comes in; the first
# draft (54 words, six cards) read 30.9s and the render refused it.
INTRO = [
    ("An hour of a fan's low, steady hum.",),
    ("Keep it low,", "in the background."),
    ("Triangle breathing:", "in for four, hold for four, out for four."),
    ("Follow the dot along the line.",),
    ("If a hold is too much, just breathe.",),
]

OUTRO = [
    ("That's the hour.",),
    ("Let your breath go back to its own pace.",),
    ("Bring the sound down slowly,", "and stay as long as you like."),
    ("Come back to it any night you need.",),
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
        intro_len=30.0,
        outro_len=30.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # E25: the named noise leads, the exercise takes the chip
    # (`docs/video/thumbnails.md`). Yellow: a lamp against the blue night.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Fan Noise", pattern="triangle breathing",
        accent="yellow", look=LOOK)
    print(thumb)
