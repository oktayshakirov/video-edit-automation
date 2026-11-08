"""Soft Orbit, 6-6-6-6 breathing on the clock guide, 60 minutes - long-form sound therapy.

**Session queue row 3 (E12 + E13):** an hour, 6-6-6-6 (box breathing at a
count of six) on the `clock` guide. Neither the exercise nor the guide has
shipped before, so this one is a first on both counts - the queue says so.

The bed is *Soft Orbit* from the app's Quiet Universe album
(tinnitushelp.me/zen/quiet-universe), supplied as a five-minute WAV. The
album is named in the description, never in the narration
(`docs/video/projects/tinnitus.md`, 2026-11-03). The second Quiet Universe
track after Low Gravity; the used and unused tracks are in
`docs/video/projects/tinnitus-sounds.md`. The picture is `RingedWorld`,
this pair's own look (`tinnitus/session_looks/soft_orbit_6666.py`): a warm
ringed planet low in the frame, its bands and rings turning once a loop, and
a small moon on one closed orbit per loop. Fully generated.

* **This is a comfort session, not a masking one - measured.** `band_energy`
  over six 30s windows: **<200 Hz 82-96%, 200 Hz-1 kHz 4-18%, everything
  above 1 kHz under 0.001%.** A deep drone on ~98 Hz and its octave ~197 Hz,
  swelling on a slow ~100s cycle. Always on (0.03% of 100ms windows below
  -50 dB), but nothing in the band tinnitus usually sits in, so no "set it
  just below your tinnitus" line and no denial either
  (`projects/tinnitus.md`, "A comfort session is not a masking session").
  The album page says "stable and calming"; that much is true of it.
* **The recording is not a loop** (self-correlation at most 0.085, at a 98s
  lag), so it is tiled with `bed_file_loop=True`. It opens with a ~0.5s
  fade in and closes with a ~1.7s fade out, both trimmed (`TRIM`).
  `seam_drop` reads **-0.99 dB** (limit -1.5), and against the
  `cos² · tail + sin² · head` prediction (1s windows) the seam sits within
  0.3 dB. The tail is ~2-3 dB quieter than the head, the recording's own
  drift, so the seam is a slow rise over the 8s crossfade. Tail and head
  correlate at 0.03.
* **`inhale=hold=exhale=rest=6`**, a 24s cycle, **`loop=72.0`** (three
  cycles). **60 minutes: 38s intro, 3528s body (49 loops), 34s outro.**
  Holds of six seconds, so the intro says once to breathe normally if a hold
  is uncomfortable (the 6s rule under "Guides"). `luna` read the first
  draft in 32.1s against the 32s that fit; "let it go, and" went.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/soft-orbit-6666-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.soft_orbit_6666 import RingedWorld

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E13 '6-6-6-6 breathing' 2026-11-03: 7 standouts across four "
          "channels; E12 hour-plus sessions stand out")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "6-6-6-6 Box Breathing + Deep Space Sounds for Tinnitus (1 Hour).mp4"
SOURCE = DESKTOP / "SoftOrbit.wav"
WORK = Path("/tmp/tinnitus-long-asmr-soft-orbit-6666-60min")
TRIM = (1.0, 298.5)          # inside the recording's own fade in / fade out

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 6.0, 6.0, 6.0, 6.0
LOOP = 3 * (INHALE + HOLD + EXHALE + REST)    # 72.0
LOOK = RingedWorld
GUIDE = "clock"

# What the sound is, how loud to keep it, the pattern, and the way out of the
# holds. No masking line: the bed has almost nothing above 1 kHz.
INTRO = [
    ("An hour of deep space sounds,",
     "low and slow, like a soft orbit."),
    ("Keep the volume low and comfortable.",),
    ("Follow the hand around the clock.",),
    ("In for six, and hold for six.",),
    ("Out for six, and rest, empty, for six.",),
    ("If a hold feels like too much,", "just breathe normally."),
]

# Not a subscribe card, and not the Low Gravity close either.
OUTRO = [
    ("That's the hour.",),
    ("Let go of the count,", "and breathe however feels easy."),
    ("Turn the sound down slowly,", "and take a moment before you move."),
    ("Come back whenever you need a slower pace.",),
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
        outro_len=34.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # "Soft Orbit" is an invented name, so the exercise leads and the sound
    # takes the chip (`docs/video/thumbnails.md`). Cyan against the amber
    # planet, and not the yellow Low Gravity wore.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="6-6-6-6 Breathing", pattern="deep space sounds",
        accent="cyan", look=LOOK)
    print(thumb)
