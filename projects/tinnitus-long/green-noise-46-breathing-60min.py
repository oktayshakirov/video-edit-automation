"""Green Noise, 4-6 breathing on the clock guide, 60 minutes - long-form sound therapy.

**A named noise leads, after E25's four** (`projects/tinnitus.md`, "Lead
with a named masking noise": a fifth may still lead with one, but does not
count toward the test). Green noise has the biggest search pool of any
noise colour we have not used: 'green noise sleep' 2026-11-25 returned
Noah Edwards 24h 13.3M, DJ Grossman 12h 11.8M, Eric Fischer 10h 6.6M; for
tinnitus, Noah Edwards 'Green Noise - Black Screen To Beat Tinnitus' 689K.
**The exercise is 4-6** (in for four, out for six: six breaths a minute,
the longer out-breath), last shipped in October with the ring, never with
the `clock` guide - a pair new to the channel, not the last session's
(physiological sigh, path). The queue in `tinnitus.md` is done; this is
picked by taste, as E13's verdict says.

The bed is *Green Meadow*, track 4 of the Colors of Calm album
(tinnitushelp.me/zen/noise-colors, released 2026-11): green noise with a
slow +-1.5 dB level drift. The album is generated, so the bed is not
fetched from DistroKid: `green_meadow()` re-renders the track from its
spec (`~/Coding/create-song-automation/zen/albums/colors_of_calm.py`, seed
41, mastered to -18 LUFS by `zen.album.master`) at 61 minutes, so the hour
is one take with no tiling seam (57s to render). The album is named in the
description. The picture is `WindMeadow`, this pair's own look
(`tinnitus/session_looks/green_meadow_46.py`): a meadow at blue hour with
gusts rolling across the grass, swaying blades and fireflies. Fully
generated.

* **A comfort bed - measured.** `band_energy` on six 30s windows of the
  61-minute render: **<200 Hz 17.3-18.6% (mean 18.0), 200 Hz-1 kHz 55.4%,
  1-4 kHz 26.1%, 4-8 kHz 0.5%, >8 kHz 0.0%**; centroid 775 Hz; -18.0
  LUFS, true peak -5.7 dB - the album docstring's numbers. Always on (0.0%
  of 100ms windows below -50 dB, median -23.8 dB). A soft mid-range sound
  with almost nothing above 4 kHz, where a high tinnitus usually sits, so
  the copy is comfort copy ("keep it quiet"), no masking line and no
  denial (`projects/tinnitus.md`, "A comfort session is not a masking
  session"). What it can honestly say: the room is never quite silent.
* **Not looped.** 61 minutes rendered, `bed_file_skip=3.0` steps past the
  render's own 3s fade in, and 3600s of it are used; the engine adds its
  6s fades and `loudnorm`.
* **`inhale=4, exhale=6`**, no holds, a 10s cycle, **`loop=60.0`** (six
  cycles). **60 minutes: 30s intro, 3540s body (59 loops), 30s outro.**
  No holds, so no way-out line.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/green-noise-46-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.green_meadow_46 import WindMeadow

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("a named noise leads (E25: Brown 10.3, Fan 9.5, Pink 6.0, HF white 41 "
          "views a day early vs themed 5.0); 'green noise sleep' 2026-11-25: "
          "Noah Edwards 24h 13.3M, DJ Grossman 12h 11.8M, Eric Fischer 10h 6.6M; "
          "'green noise tinnitus': Noah Edwards 24h 689K, Treble Health 'Tinnitus "
          "Verde' 1.4M; '4-6 breathing': Neil Tranter '4-6 HRV Breathing' 426K")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Green Noise for Tinnitus + 4-6 Breathing (1 Hour).mp4"
SOURCE = DESKTOP / "colors-of-calm" / "session" / "04 Green Meadow (61 min).wav"
ZEN = Path.home() / "Coding" / "create-song-automation"
WORK = Path("/tmp/tinnitus-long-asmr-green-noise-46-60min")

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 4.0, 0.0, 6.0, 0.0
LOOP = 6 * (INHALE + HOLD + EXHALE + REST)    # 60.0
LOOK = WindMeadow
GUIDE = "clock"

# What the sound is, how loud to keep it (comfort, not masking) and the
# pattern. Not the Brown Noise or Pink Noise lines.
INTRO = [
    ("An hour of soft green noise,", "like wind across a meadow."),
    ("Keep it quiet,", "just enough that the room is never silent."),
    ("Follow the hand round the dial.",),
    ("Breathe in for four,", "and out for six."),
]

OUTRO = [
    ("That's the hour.",),
    ("Let your breathing settle into its own rhythm.",),
    ("Turn the sound down slowly,", "and give yourself a moment."),
    ("The meadow is here whenever you need it.",),
]


def green_meadow() -> Path:
    """The album track at 61 minutes, rendered from its spec if not on disk."""
    if not SOURCE.exists():
        SOURCE.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(ZEN / ".venv/bin/python"), "-c", f"""
from pathlib import Path
from zen.album import load_spec, master
from zen.noise import render
spec = load_spec(Path('zen/albums/colors_of_calm.py'))
t = next(t for t in spec.TRACKS if t.title == 'Green Meadow')
print(master(render(61 * 60, t.bed, t.seed), Path({str(SOURCE)!r}), mp3=False))
"""], cwd=ZEN, check=True)
    return SOURCE


if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=WORK,
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=green_meadow(),
        bed_file_skip=3.0,
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

    # The named noise leads, the exercise takes the chip
    # (`docs/video/thumbnails.md`). Orange: the warm opposite of a
    # teal-green night, and not the last session's yellow.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Green Noise", pattern="4-6 breathing",
        accent="orange", look=LOOK)
    print(thumb)
