"""Pink Noise, box breathing (4-4-4-4) on the box guide, 60 minutes - long-form sound therapy.

**E25, the third of four sessions led by a named noise** (`projects/
tinnitus.md`, "Lead with a named masking noise"): the title and the cover
start with "Pink Noise". **Session queue row 8:** box 4-4-4-4 on the `box`
guide. **The row was "visual only" and the first cut shipped to the editor
that way (no voice, 8s bookends); the editor's note, 2026-11-21: "lets not
create videos without instructions".** So it has `luna`'s intro and outro
like every session, and the visual-only idea is dropped from the queue.

The bed is *Rose Haze*, track 2 of the Colors of Calm album
(tinnitushelp.me/zen/noise-colors, released 2026-11): pink noise with a
slow +-1.5 dB level drift. The album is generated, so the bed is not
fetched from DistroKid: `rose_haze()` re-renders the track from its spec
(`~/Coding/create-song-automation/zen/albums/colors_of_calm.py`, seed 23,
mastered to -18 LUFS by `zen.album.master`) at 61 minutes, so the hour is
one take with no tiling seam. The album is named in the description. The
picture is `RoseMere`, this pair's own look
(`tinnitus/session_looks/rose_haze_box.py`): a still lake at a pink dawn,
mirrored and rippling under drifting rose haze. Fully generated.

* **A masking bed - measured.** `band_energy` on the 61-minute render:
  **<200 Hz 42.0%, 200 Hz-1 kHz 19.8%, 1-4 kHz 16.5%, 4-8 kHz 8.6%,
  >8 kHz 13.1%**, -18.2 LUFS, true peak -5.2 dB - the album docstring's
  numbers to the decimal. Broadband and always on (generated noise has no
  gaps), with real energy from 1 kHz up where tinnitus usually sits, so
  the partial-masking angle holds: `luna` says to set it just below your
  tinnitus, so you can still faintly hear it.
* **Not looped.** 61 minutes rendered, `bed_file_skip=3.0` steps past the
  render's own 3s fade in, and 3600s of it are used; the engine adds its
  6s fades and `loudnorm`.
* **`inhale=hold=exhale=rest=4`**, a 16s cycle, **`loop=64.0`** (four
  cycles). **60 minutes: 40s intro, 3520s body (55 loops), 40s outro.**
  `luna` reads the intro in 29.2s of the 34s that fit and the outro in
  16.1s. The holds are four seconds, under the six that require the line,
  but the intro still gives the way out of them.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/pink-noise-box-breathing-60min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.rose_haze_box import RoseMere

SOURCE_POST = None  # off-site: a sound-therapy session, no article
DEMAND = ("E25 a named noise leads the session (white-noise sessions 47 and "
          "7.6 views a day vs themed 0.6-4); 'pink noise for tinnitus' "
          "2026-11-21: SleepDroid 10h pink noise 5.3M, Treble Health 'Could "
          "Pink Noise Be A Treatment' 902K, Brad McBride 'Pink Noise Tinnitus "
          "Masking - 90 Minutes' 210K; 'box breathing visual': UAB 'Square "
          "Breathing Visual' 1.4M; E13 queue row 8 (box, box guide)")

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Pink Noise for Tinnitus + Box Breathing (1 Hour).mp4"
SOURCE = DESKTOP / "colors-of-calm" / "session" / "02 Rose Haze (61 min).wav"
ZEN = Path.home() / "Coding" / "create-song-automation"
WORK = Path("/tmp/tinnitus-long-asmr-pink-noise-box-60min")

MINUTES = 60.0
INHALE, HOLD, EXHALE, REST = 4.0, 4.0, 4.0, 4.0
LOOP = 4 * (INHALE + HOLD + EXHALE + REST)    # 64.0
LOOK = RoseMere
GUIDE = "box"

# What the sound is, the partial-masking level, the pattern, and the way
# out of the holds. Not the Fan Noise or Low Gravity lines.
INTRO = [
    ("An hour of soft pink noise.",),
    ("Set it just below your tinnitus,", "so you can still faintly hear it."),
    ("Box breathing:", "in for four, hold for four,"),
    ("out for four, hold for four.",),
    ("Follow the dot around the square.",),
    ("If a hold feels like too much,", "let it go and just breathe."),
]

OUTRO = [
    ("The hour is done.",),
    ("Let your breathing find its own pace again.",),
    ("Bring the sound down slowly,", "whenever you're ready."),
    ("Come back to it any time you need.",),
]


def rose_haze() -> Path:
    """The album track at 61 minutes, rendered from its spec if not on disk."""
    if not SOURCE.exists():
        SOURCE.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(ZEN / ".venv/bin/python"), "-c", f"""
from pathlib import Path
from zen.album import load_spec, master
from zen.noise import render
spec = load_spec(Path('zen/albums/colors_of_calm.py'))
t = next(t for t in spec.TRACKS if t.title == 'Rose Haze')
print(master(render(61 * 60, t.bed, t.seed), Path({str(SOURCE)!r}), mp3=False))
"""], cwd=ZEN, check=True)
    return SOURCE


if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=WORK,
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=rose_haze(),
        bed_file_skip=3.0,
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

    # E25: the named noise leads, the exercise takes the chip
    # (`docs/video/thumbnails.md`). Cyan: the cool opposite of a pink dawn.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Pink Noise", pattern="box breathing",
        accent="cyan", look=LOOK)
    print(thumb)
