"""Jungle waterfall + birdsong, 4-7-8 breathing, 20 minutes — long-form sound therapy.

**The first session that is not a nebula.** The picture is this video's own
look, `NightFronds` in `tinnitus/session_looks/jungle_waterfall_478.py`: drawn
fern silhouettes swaying round the edges of the frame, a moonlit green glow,
two sheets of mist and fireflies. It was picked from five test looks
(2026-10-15) and is not reused; the next session builds its own on the
`core/looks.py` format. Generated, so there is no licence and no stock credit.

* **`inhale=4.0, hold=7.0, exhale=8.0`**, a 19s cycle, and **`loop=57.0`**
  (three cycles). The look is built with `period=loop`, so the fronds' sway,
  the mist and the fireflies all close on the same frame the ring does.
* **20 minutes: 34s intro, 1140s body (twenty loops), 26s outro**, the same
  split as the waterfall pair.
* **The bed is one real recording, five minutes long, tiled to twenty**
  (`bed_file_loop=True`). It is the subject rather than the coverage, the case
  `soundbed.tile` exists for. Its own one-second fade in and fade out are
  trimmed first (`TRIM`), or every seam would dip by them; the seam is then
  measured with `soundbed.seam_drop` rather than assumed.
* **`band_energy` on the recording (three 30s windows): <200 Hz 0.2%,
  200 Hz-1 kHz 0.2-0.5%, 1-4 kHz 38-47%, 4-8 kHz 51-60%, >8 kHz 1-2%.** Almost
  all of it sits in 1-8 kHz, which is where the partial-masking instruction
  has something to work with, so this is a masking session, not a comfort
  one (`docs/video/projects/tinnitus.md`). The copy still makes no claim about
  what the sound does — it says how to set the level.
* **The sound is a waterfall and birdsong. "Jungle" is the picture.** The
  narration names only the sound.

The caption reads "4-7-8"; the voice does not — the usual `(caption, spoken)`
pair, because espeak reads a bare `4-7-8` as "four dash seven dash eight".

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/jungle-waterfall-478-breathing-20min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.jungle_waterfall_478 import NightFronds

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Jungle Waterfall + 4-7-8 Breathing for Tinnitus (20 Minutes).mp4"
SOURCE = DESKTOP / "WaterfallBirds.wav"
WORK = Path("/tmp/tinnitus-long-asmr-jungle-waterfall-478-20min")
TRIM = (1.5, 298.5)          # inside the recording's own fade in / fade out

MINUTES = 20.0
INHALE, HOLD, EXHALE = 4.0, 7.0, 8.0
LOOP = 3 * (INHALE + HOLD + EXHALE)    # 57.0
LOOK = NightFronds

INTRO = [
    ("Twenty minutes of a waterfall and birdsong,",
     ("with 4-7-8 breathing.", "with four, seven, eight breathing.")),
    ("Set the volume just below your tinnitus.",),
    ("You should still hear it",
     "faintly underneath. That is the point.",),
    ("Then follow the circle.",
     "Four in, seven hold, eight out.",),
]

# Not a subscribe card. A piece built to lower arousal does not end by asking
# for something.
OUTRO = [
    ("That is twenty minutes.",),
    ("If it helped, start it again",
     "and take another round.",),
    ("There are other sounds and patterns",
     "on the channel for when you want them.",),
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
        intro_len=34.0,
        outro_len=26.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # A still of the same look, t=0. Orange reads on green the way it read on
    # the teal waterfall session.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Jungle Waterfall", pattern="4-7-8 breathing",
        accent="orange", look=LOOK)
    print(thumb)
