"""Tranquil Zenith, 2:1 breathing on the path guide, 60 minutes - long-form sound therapy.

**Session queue row 4 (E12 + E13):** an hour, 2:1 breathing (in for four,
out for eight, no holds) on the `path` guide. The exercise has not shipped
before; the path guide has (`wild-echoes-478-breathing`).

The bed is *Tranquil Zenith* from the app's White Noise Therapy album
(tinnitushelp.me/zen/white-noise), supplied as a ten-minute MP3. The album
is named in the description, never in the narration
(`docs/video/projects/tinnitus.md`, 2026-11-03). The used and unused tracks
are in `docs/video/projects/tinnitus-sounds.md`. The picture is
`ZenithSea`, this pair's own look
(`tinnitus/session_looks/tranquil_zenith_21.py`): a starry night sky with a
faint light from straight overhead, above a sea of cloud that sways on two
closed circles. Fully generated.

* **This is a masking session - measured, and the first album track on the
  channel with real energy where tinnitus usually sits.** `band_energy` over
  seven 30s windows: **<200 Hz 0.3-0.5%, 200 Hz-1 kHz 1.2-1.8%, 1-4 kHz
  5-8%, 4-8 kHz 84-89%, >8 kHz 4-6%.** Not white in the strict sense: flat
  from 125 Hz to 3 kHz, a broad hump of +10-12 dB at 4.5-7 kHz, rolling off
  by 10 kHz and gone above 12 kHz. Always on (0.45% of 100ms windows below
  -50 dB, all of them in the opening fade), so the partial-masking line
  applies (`projects/tinnitus.md`, "Copy for a session").
* **It is not a plain hiss, and the copy does not call it "pure".** Over the
  steady floor (itself broadband: 30% 1-4 kHz, 39% 4-8 kHz, 23% above
  8 kHz) sit short high pings, ~53 a minute, ~0.15s each, 12-22 dB above
  the floor, all of their energy at 4-8 kHz, pitched near 5 kHz - which is
  also the narrow peak at ~4.92 kHz the long-window spectrum shows (~30 dB
  over its neighbours, ~10 Hz wide, drifting). The album page's "pure,
  perfectly balanced white noise" is not what the file holds, so the intro
  says "soft white noise" and nothing more about its shape.
* **The recording is not a loop** (self-correlation at most 0.016), so it is
  tiled with `bed_file_loop=True`. It fades in over its first ~11s and stops
  at full level with no fade out, so `TRIM` takes 12.0s to 599.5s.
* **`inhale=4, exhale=8`**, a 12s cycle, **`loop=60.0`** (five cycles).
  **60 minutes: 30s intro, 3540s body (59 loops), 30s outro.** No holds, so
  no way-out-of-the-hold line; the long exhale gets one instead. `luna`
  read the first draft in 31.0s against the 24s that fit; it lost "Start
  it quiet" and "slowly", the dot and the counts went into one line,
  and the way out of the long exhale became "shorten it" (24.7s, then).

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tranquil-zenith-21-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.tranquil_zenith_21 import ZenithSea

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E13 session queue row 4 (2:1 breathing, path guide); E12 "
          "hour-plus sessions stand out")

DESKTOP = Path.home() / "Desktop"
# The title is "2:1 Breathing + White Noise for Tinnitus (1 Hour)"; a colon
# in a macOS file name shows as a slash in Finder, so the file says "2-1".
OUT = DESKTOP / "2-1 Breathing + White Noise for Tinnitus (1 Hour).mp4"
SOURCE = DESKTOP / "TranquilZenith.mp3"
WORK = Path("/tmp/tinnitus-long-asmr-tranquil-zenith-21-60min")
TRIM = (12.0, 599.5)         # past the recording's own fade in; no fade out

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 4.0, 0.0, 8.0, 0.0
LOOP = 5 * (INHALE + HOLD + EXHALE + REST)    # 60.0
LOOK = ZenithSea
GUIDE = "path"

# What the sound is, how loud to keep it, the pattern, and the way out of a
# long exhale. The level comes from below this time (Wild Echoes came down
# from above).
INTRO = [
    ("An hour of soft white noise.",),
    ("Raise it until your tinnitus", "starts to blend in,"),
    ("but you can still faintly hear it.",),
    ("Follow the dot: in for four, out for eight.",),
    ("If eight feels long,", "shorten it."),
]

# Not a subscribe card, and not the Soft Orbit close either.
OUTRO = [
    ("The hour is done.",),
    ("Let your breathing find its own pace again.",),
    ("Bring the sound down slowly,", "and take a moment before you get up."),
    ("Come back whenever you need a quiet hour.",),
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
        intro_len=30.0,
        outro_len=30.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK,
        guide=GUIDE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # "White noise" is a sound people type, so it leads and the exercise
    # takes the chip (`docs/video/thumbnails.md`). Yellow, the complement of
    # the blue-violet night.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="White Noise", pattern="4-in, 8-out breathing",
        accent="yellow", look=LOOK)
    print(thumb)
