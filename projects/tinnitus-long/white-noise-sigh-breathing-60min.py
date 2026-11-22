"""High Frequency White Noise, the physiological sigh on the path guide, 60 minutes - long-form sound therapy.

**E25, the fourth and last of four sessions led by a named noise**
(`projects/tinnitus.md`, "Lead with a named masking noise"): the title and
the cover start with "High Frequency White Noise". **Session queue row 9:**
the physiological sigh (a full inhale, a short second inhale on top, a long
exhale) on the `path` guide. It needed its build step first: the engine
grew a `top=` phase (`guides.Pattern.top`, `_breath`, `breathing_phases`),
and the path draws the top-up as a step on the rise.

The bed is *Ethereal Resonance*, track 5 of the app's White Noise Therapy
album (tinnitushelp.me/zen/white-noise; the DistroKid release is "Infinite
Horizons"), pulled from DistroKid as a ten-minute 320k MP3 at 48 kHz that
saves as `EtherealResonance.mp3`. The album is named in the description,
never in the narration. The picture is `AuroraSnow`, this pair's own look
(`tinnitus/session_looks/ethereal_sigh.py`): an aurora over a snowy range
at night, snow falling in two depths. Fully generated.

* **A masking bed, and a high one - measured.** `band_energy` over twenty
  30s windows: **<200 Hz 0.00%, 200 Hz-1 kHz 0.00%, 1-4 kHz 0.07-0.12%,
  4-8 kHz 77-79%, >8 kHz 21-23%**; centroid 6.9 kHz. By octave, 92% sits
  at 5-10 kHz and 8% at 2.5-5 kHz; the spectrum climbs from 2 kHz, peaks
  near 5.3 kHz (a narrow tone ~5 dB over its neighbours), holds a broad
  plateau to 9 kHz and is gone by 10.5 kHz. So it is white noise with
  everything under ~2.5 kHz filtered away: the album's "deep, resonant
  quality" is not in the file, and the title says "High Frequency", which
  is what it is. Its energy is where a high-pitched tinnitus usually sits,
  and none of it reaches a low hum - the description says so plainly.
* **Always on, with soft pings over it.** 0.00% of 100ms windows below
  -50 dB; 10s RMS -19.7 to -19.0 dB. About 39 short rises a minute sit
  6 dB or more over the 50ms median (-21.0 dB), like Tranquil Zenith's
  pings, so the copy does not call it "pure". The partial-masking line
  applies: `luna` says to set it just below your tinnitus, so you can
  still faintly hear it - and to start it quiet, since a bright hiss is
  the bed a sensitive ear is most likely to find sharp.
* **Not a loop** (self-correlation at 10-480s lags at most 0.061), so it
  is tiled with `bed_file_loop=True`. It rises from -22 dB to its level
  over the first two seconds and stops at full level, so `TRIM` takes
  2.0s to 599.5s.
* **`inhale=3, top=1, exhale=6`**, a 10s cycle (six breaths a minute),
  **`loop=40.0`** (four cycles). **60 minutes: 42s intro, 3520s body
  (88 loops), 38s outro** - the sigh needs more words than a count:
  `luna` reads the intro in 34.9s of the 36s that fit (a 40s intro left
  34s, and the first draft read 37.6s) and the outro in 16.5s. No holds,
  so no hold line; the long exhale gets a way out instead.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/white-noise-sigh-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.ethereal_sigh import AuroraSnow

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E25 a named noise leads the session (white-noise sessions 47 and "
          "7.6 views a day vs themed 0.6-4); 'high frequency white noise "
          "tinnitus' 2026-11-22: Treble Health 'Tinnitus SILK - High Range "
          "Noise Masking' 2.08M, 'Flicker' 518K, 'Fuzz' 369K, Art of Zen "
          "high-pitch sound therapy 1.5M; 'physiological sigh': Huberman clip "
          "907K, RESPIRE 'Guided Cyclic Sighing' 216K; E13 queue row 9 "
          "(physiological sigh, path)")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "High Frequency White Noise for Tinnitus + Physiological Sigh (1 Hour).mp4"
SOURCE = DESKTOP / "EtherealResonance.mp3"
WORK = Path("/tmp/tinnitus-long-asmr-white-noise-sigh-60min")
TRIM = (2.0, 599.5)          # a two-second rise in; no fade out

MINUTES = 60.0
INHALE, TOP, EXHALE = 3.0, 1.0, 6.0
LOOP = 4 * (INHALE + TOP + EXHALE)    # 40.0
LOOK = AuroraSnow
GUIDE = "path"

# What the sound is, the partial-masking level (start quiet: a bright
# hiss), the sigh in three steps, and the way out of the long exhale.
# Not the Pink Noise or Fan Noise lines.
INTRO = [
    ("An hour of high, bright white noise.",),
    ("Start it quiet, then set it just below your tinnitus,",
     "so you can still faintly hear it."),
    ("The physiological sigh:", "in through your nose,"),
    ("then a short second breath in on top,", "and a long, slow breath out."),
    ("Follow the dot along the line.",),
    ("If the breath out feels too long,", "just breathe normally."),
]

OUTRO = [
    ("The hour is over.",),
    ("Let your breathing settle back into its own rhythm.",),
    ("Turn the sound down slowly,", "whenever you're ready."),
    ("Come back to it whenever you need.",),
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
        intro_len=42.0,
        outro_len=38.0,
        loop=LOOP,
        inhale=INHALE, hold=0.0, exhale=EXHALE, rest=0.0, top=TOP,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # E25: the named noise leads, the exercise takes the chip
    # (`docs/video/thumbnails.md`). Yellow: warm against the blue-green night.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="High Frequency White Noise", pattern="physiological sigh",
        accent="yellow", look=LOOK)
    print(thumb)
