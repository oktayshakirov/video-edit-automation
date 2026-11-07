"""Low Gravity, box breathing on the box guide, 60 minutes - long-form sound therapy.

**Session queue row 2 (E12 + E13):** an hour, box breathing 4-4-4-4 on the
`box` guide. Box breathing shipped once before with the ring (Forest
Chorus), so the guide is the thing that changed.

The bed is *Low Gravity* from the app's Quiet Universe album
(tinnitushelp.me/zen/quiet-universe), supplied as a five-minute WAV. The
album is named in the description, never in the narration
(`docs/video/projects/tinnitus.md`, 2026-11-03). The picture is `LowOrbit`,
this pair's own look (`tinnitus/session_looks/low_gravity_box.py`): a
planet's limb along the bottom with its atmosphere glowing, cloud drifting
across it, stars, a faint galaxy band and floating dust. Fully generated.

* **This is a comfort session, not a masking one - measured.** `band_energy`
  over six 30s windows, identical in every one: **<200 Hz 0.7%, 200 Hz-1 kHz
  99.1%, 1-4 kHz 0.1%, 4-8 kHz 0.02%, >8 kHz 0.02%.** A soft pad clustered
  around 415-465 Hz (centred near 440), with a slow swell every ~10s. It is
  always on (0% of 100ms windows below -70 dB, 0.2% below -50 dB), but there
  is almost nothing in the band tinnitus usually sits in, so there is no
  "set it just below your tinnitus" line and no denial either. The copy
  says what the sound is and how loud to keep it (`projects/tinnitus.md`,
  "A comfort session is not a masking session"). The album page says "for
  tinnitus masking"; the measurement wins.
* **Box breathing on a comfort bed.** A comfort piece usually takes an
  unnamed pattern, but the E13 queue fixes row 2 as box on the `box` guide,
  and the guide is the experiment. The intro gives the way out of the holds.
* **The recording is not a loop** (self-correlation at most 0.15 at any lag
  from 40s to 260s), so it is tiled with `bed_file_loop=True`. Its own fade
  in (~3s, -50 to -27 dB) and fade out (last ~2.5s) are trimmed first
  (`TRIM`). `seam_drop` reads **+1.5 dB** at every seam (a rise, not a dip),
  and the crossfade is fine: the pad swells ~2 dB every 10s, so its
  reference quarter-second lands anywhere in a swell. Against the
  `cos² · tail + sin² · head` prediction (1s windows) the seam sits within
  0.4 dB except one second at +1.4 dB, inside the recording's own 1s swing
  of -22.5 to -28.6 dB around it. Tail and head correlate at 0.1.
* **`inhale=hold=exhale=rest=4`**, a 16s cycle, **`loop=64.0`** (four
  cycles). **60 minutes: 40s intro, 3520s body (55 loops), 40s outro.**
  `luna` read the first intro draft in 34.1s against the 34s that fit; the
  "quiet enough to sit in the background" half-line went.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/low-gravity-box-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.low_gravity_box import LowOrbit

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E13 'box breathing' 2026-11-03: 13 standouts of 15, 'Square "
          "Breathing Visual' 1.4M; E12 hour-plus sessions stand out")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "4-4-4-4 Box Breathing + Space Sounds for Tinnitus (1 Hour).mp4"
SOURCE = DESKTOP / "LowGravity.wav"
WORK = Path("/tmp/tinnitus-long-asmr-low-gravity-box-60min")
TRIM = (4.0, 297.5)          # inside the recording's own fade in / fade out

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 4.0, 4.0, 4.0, 4.0
LOOP = 4 * (INHALE + HOLD + EXHALE + REST)    # 64.0
LOOK = LowOrbit
GUIDE = "box"

# What the sound is, how loud to keep it, the pattern, and the way out of the
# holds. No masking line: the bed has almost nothing above 1 kHz.
INTRO = [
    ("An hour of space sounds,",
     "slow and floating, like drifting in low gravity."),
    ("Keep the volume low and comfortable.",),
    ("Follow the dot around the square.",),
    ("In for four, and hold for four.",),
    ("Out for four, and rest, empty, for four.",),
    ("If a hold feels hard,", "skip it, and just breathe."),
]

# Not a subscribe card, and not the last sessions' closes either.
OUTRO = [
    ("The hour is done.",),
    ("Let your breathing find its own pace,",
     "and feel the weight of your body again."),
    ("Bring the sound down slowly,", "rather than all at once."),
    ("Come back whenever you want to drift.",),
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
        intro_len=40.0,
        outro_len=40.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # Yellow on the deep blue: the opposite of the picture's colour, and not
    # the orange the last three sessions wore.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Space Sounds", pattern="box breathing",
        accent="yellow", look=LOOK)
    print(thumb)
