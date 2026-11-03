"""Wild Echoes, 4-7-8 breathing on the path guide, 60 minutes — long-form sound therapy.

**Session queue row 1 (E12 + E13):** the first hour-long session and the
first on the `path` guide, on 4-7-8 because that exercise has already shipped
four times with the ring - the guide is the thing that changed.

The bed is *Wild Echoes* from the app's Jungle Stillness album
(tinnitushelp.me/zen/jungle-stillness), supplied as a ten-minute WAV. The
picture is `FernBreath` (`fern-breath` from the 2026-10-15 test round, now
this pair's own in `tinnitus/session_looks/wild_echoes_478.py`): dark jungle
palms that zoom in and come into focus on the inhale, with fireflies.

* **`band_energy` (six 30s windows): <200 Hz 0-0.4%, 200 Hz-1 kHz 1-6%,
  1-4 kHz 18-79%, 4-8 kHz 17-81%, >8 kHz 0.2-1.8%.** The first half of the
  recording sits mostly in 4-8 kHz, the second half mostly in 1-4 kHz;
  either way almost all of it is in the band tinnitus occupies.
* **And it is always there**: 0% of 100ms windows below -70 dB, 0.2% below
  -50 dB, unlike the bird-chirps calls. So this is a masking session, not a
  comfort one (`docs/video/projects/tinnitus.md`). The copy still claims
  nothing about what the sound does; it says how to set the level.
* **The level instruction comes from above this time** - start louder than
  the tinnitus and bring it down until the tinnitus is just audible again.
  The waterfall session came from below the tinnitus, the forest chorus from
  low upwards; all three are partial masking.
* **The recording is not a loop** (self-correlation ~0 at every lag tried
  from 30s to 300s), so it is tiled with `bed_file_loop=True`. Its fade in
  (~3s) and fade out (~2s) are trimmed first (`TRIM`). The 10s RMS wanders
  between -21 and -32 dB in the second half, so `seam_drop` may cry wolf
  the way it did on the waterfall bed; check against the crossfade
  prediction before lengthening `xfade`.
* **`inhale=4, hold=7, exhale=8`**, a 19s cycle, **`loop=57.0`** (three
  cycles). **60 minutes: 38s intro, 3534s body (62 loops), 28s outro.**
  `luna` read the first intro draft in 34.6s against the 30s that fit;
  the track name went and two seconds moved from the outro.
* **A seven-second hold, so the intro says once to breathe normally if a
  hold is uncomfortable** (the 6s rule under "Guides").

The caption reads "4-7-8"; the voice does not — the usual `(caption, spoken)`
pair, because espeak reads a bare `4-7-8` as "four dash seven dash eight".

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/wild-echoes-478-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.wild_echoes_478 import FernBreath

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E12 'tinnitus at night' 2026-11-03: hour-plus sessions stand out "
          "(Doctor Cliff 10 hours 442x, Treble 10-hour crickets 67x)")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "4-7-8 Breathing + Jungle Sounds for Tinnitus (1 Hour).mp4"
SOURCE = DESKTOP / "WildEchoes.wav"
WORK = Path("/tmp/tinnitus-long-asmr-wild-echoes-478-60min")
TRIM = (3.0, 598.0)          # inside the recording's own fade in / fade out

MINUTES = 60.0
INHALE, HOLD, EXHALE = 4.0, 7.0, 8.0
LOOP = 3 * (INHALE + HOLD + EXHALE)    # 57.0
LOOK = FernBreath
GUIDE = "path"

INTRO = [
    ("An hour of jungle sounds,",
     "from our album, Jungle Stillness."),
    ("Start a little louder than your tinnitus,",
     "then bring it down"),
    ("until you can just hear it again,",
     "faintly, underneath."),
    ("Follow the dot along the line.",
     ("4-7-8: four in, seven hold, eight out.",
      "Four in, seven hold, eight out.")),
    ("If a hold feels too long,", "just breathe normally."),
]

# Not a subscribe card, and not the last two sessions' closes either.
OUTRO = [
    ("That is the hour.",),
    ("Notice the room around you again",
     "before you turn the sound off."),
    ("The whole album, Jungle Stillness,", "is on our website."),
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
        intro_len=38.0,
        outro_len=28.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # "Jungle Sounds" leads - a sound people type - and the exercise takes
    # the chip (`docs/video/thumbnails.md`). Orange reads on the dark green,
    # as it did on the jungle waterfall session.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Jungle Sounds", pattern="4-7-8 breathing",
        accent="orange", look=LOOK)
    print(thumb)
