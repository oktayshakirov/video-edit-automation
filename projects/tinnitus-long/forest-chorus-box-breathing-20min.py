"""Forest chorus, box breathing, 20 minutes — long-form sound therapy.

**Varies the last session on purpose: a different pattern and different
instructions.** Every session before this was 4-in/6-out or 4-7-8 with "set it
just below your tinnitus, then follow the circle". This one is box breathing
(4-4-4-4), and the level instruction comes from the other direction — start
low and bring it up until the tinnitus starts to blend in — which is still
partial masking, said fresh. It also gives the listener a way out of the
holds, because a held breath is the part of box breathing an anxious listener
is most likely to fight.

* **`inhale=4, hold=4, exhale=4, rest=4`**, a 16s cycle. `rest` is the hold
  after the exhale (ring pinned small, labelled "hold" like the first), added
  to both renderers for this video. **`loop=32.0`** (two cycles): the fog
  footage ping-pongs on a 16s cycle inside it, and the fireflies close on 32s.
* **20 minutes: 48s intro, 1120s body (35 loops), 32s outro.** The intro
  narration reads in ~36s and has to finish before the ring's 3s reveal, so
  it needs 48; a 64s loop would have forced a 70s intro to land on whole loops.
* **The look is `CanopyFog`**, `canopy-fog` from the 2026-10-15 test round,
  now this pair's own (`tinnitus/session_looks/forest_chorus_box.py`): misty
  jungle-canopy footage, Pexels 19366762 by Florian Delee.
* **The bed is one real recording, ten minutes long, tiled to twenty**
  (`bed_file_loop=True`). Its own fade in and fade out are trimmed first
  (`TRIM`): the first and last few seconds sit 5-25 dB under the body, and
  every seam would inherit that dip.
* **`band_energy` (five 30s windows across the file): <200 Hz 0.8-1.2%,
  200 Hz-1 kHz ~0.5%, 1-4 kHz 0.9-3.6%, 4-8 kHz 93-96%, >8 kHz 0.9-2.2%.**
  Almost all of it sits in 4-8 kHz, where a high-pitched tinnitus usually is,
  so this is a masking session (`docs/video/projects/tinnitus.md`). The copy
  still claims nothing about what the sound does; it says how to set the level.
  The level is steady (10s RMS within -20 to -22 dB), so `seam_drop` should
  not cry wolf the way it did on the waterfall recording.
* **"Forest chorus" names the sound and nothing more specific** — the file is
  `NaturesChorus.wav` and the narration does not guess at species.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/forest-chorus-box-breathing-20min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.forest_chorus_box import CanopyFog

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Forest Chorus + Box Breathing for Tinnitus (20 Minutes).mp4"
SOURCE = DESKTOP / "NaturesChorus.wav"
WORK = Path("/tmp/tinnitus-long-asmr-forest-chorus-box-20min")
TRIM = (3.0, 595.0)          # inside the recording's own fade in / fade out

MINUTES = 20.0
INHALE, HOLD, EXHALE, REST = 4.0, 4.0, 4.0, 4.0
LOOP = 2 * (INHALE + HOLD + EXHALE + REST)    # 32.0
LOOK = CanopyFog

INTRO = [
    ("Twenty minutes of a forest chorus,", "with box breathing."),
    ("Start with the sound low,", "and bring it up slowly."),
    ("Stop when your tinnitus starts to blend in,",
     "still faintly there underneath."),
    ("Breathe in for four. Hold for four.",),
    ("Out for four. Then hold again, empty, for four.",),
    ("If a hold feels like too much,", "let it go and just breathe."),
]

# Not a subscribe card, and not last session's "start it again" either.
OUTRO = [
    ("That is twenty minutes.",),
    ("Let your breath find its own pace again",
     "before you get up.",),
    ("Come back to it", "whenever you want another round.",),
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
        intro_len=48.0,
        outro_len=32.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE, rest=REST,
        look=LOOK,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # Yellow, not last session's orange: the fog is grey-green, and the pair
    # should not read as the jungle session's thumbnail re-shot.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Forest Chorus", pattern="box breathing",
        accent="yellow", look=LOOK)
    print(thumb)
