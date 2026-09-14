"""Waterfall + pads, 4-7-8 breathing, 20 minutes — long-form sound therapy.

**Same pattern as `478-breathing-white-noise-20min.py`, a different bed.**
That session generated white noise; this one plays a single already-mixed
field recording — a waterfall with soft pads laid under it — through the
new `bed_file` path (`video_automation/tinnitus/asmr.py`,
`video_automation/longform/asmr.py`), which trims a real recording to length
and gives it the same `loudnorm`/fade treatment a generated bed gets, rather
than the two-track `bed_files` layering the old album tracks used.

* **`inhale=4.0, hold=7.0, exhale=8.0`** — the same 4-7-8 pattern as the
  white-noise pair, a 19s cycle.
* **`loop=57.0`** (three 19s cycles), same reasoning as the white-noise
  build: `loop` must divide evenly by the pattern's own cycle length.
* **20 minutes: 34s intro, body, 26s outro** — same split as the white-noise
  pair.
* **A real recording, not a synthesised colour** — so this session's copy
  says "waterfall and soft pads", not "white noise", and does not claim the
  frequency coverage `soundbed.Bed` gives (see `docs/video/projects/tinnitus.md`
  on the honest limits of any fixed recording).
* **No medical claims.** The intro names the sound and says how to set the
  level; it never promises what either one will do.

**The caption reads "4-7-8"; the voice does not** — same `(caption, spoken)`
device as every other 4-7-8 build, because Kokoro/espeak reads a bare
`4-7-8` as "four dash seven dash eight".

**A fresh seed and a teal palette**, not the white-noise pair's blue or the
app's default purple/peach — `(bg_deep, nebula_a, nebula_b, ring)` moves the
mid and bright cloud toward teal/aqua and the ring to a pale foam colour, so
this session reads as "water" on sight and as a different piece from the
478-white-noise pair, not a re-skin of it.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/waterfall-478-breathing-20min.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb

SOURCE_POST = None  # off-site: a generated sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Waterfall + 4-7-8 Breathing for Tinnitus (20 Minutes).mp4"
BED_FILE = DESKTOP / "waterfall-pads.mp3"

MINUTES = 20.0
INHALE, HOLD, EXHALE = 4.0, 7.0, 8.0
LOOP = INHALE + HOLD + EXHALE  # 19.0 — one full cycle

# A fresh seed from every other session (7 default, 42 for the white-noise
# 478 pair) — a different star field for a piece built on its own recording.
SEED = 17

# (bg_deep, nebula_a, nebula_b, ring) — dark teal void, teal-to-aqua cloud,
# pale foam ring. bg_deep keeps roughly the same near-black luminance as the
# default so the "mostly void" composition in `nebula_canvas` still reads;
# nebula_a/b move the mid and bright clouds from violet toward teal/aqua;
# ring is pale foam rather than peach or ice-blue.
PALETTE = ((5, 18, 18), (18, 92, 92), (140, 232, 214), (196, 246, 232))

# What the sound is, the one setting that matters, then the pattern by name
# and by count. The pattern's caption keeps the numerals; the spoken half
# drops the hyphens so Kokoro doesn't read "4-7-8" as "four dash seven dash
# eight" — see the module docstring.
INTRO = [
    ("Twenty minutes of waterfall and pads,",
     ("with 4-7-8 breathing.", "with four, seven, eight breathing.")),
    ("Set the volume just below your tinnitus.",),
    ("You should still hear it",
     "faintly underneath. That is the point.",),
    ("Then follow the circle.",
     "Four in, seven hold, eight out.",),
]

# Not a subscribe card. A piece built to lower arousal cannot end by asking
# for something. No call to action, no music sting.
OUTRO = [
    ("That is twenty minutes.",),
    ("If it helped, start it again",
     "and take another round.",),
    ("There are other patterns and lengths",
     "on the channel for when you want them.",),
]

if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=Path("/tmp/tinnitus-long-asmr-waterfall-478-20min"),
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=BED_FILE,
        intro=INTRO,
        outro=OUTRO,
        intro_len=34.0,
        outro_len=26.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE,
        seed=SEED, palette=PALETTE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # `render_session_thumb`, not `render_thumb` — a session has no
    # photograph. Same seed and palette as the video, so it is a picture of
    # this one. Orange accent (not the format's usual cyan) reads against a
    # teal nebula the way peach read against purple — a warm number on a
    # cool field.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="4-7-8 Breathing", pattern="4 in / 7 hold / 8 out",
        seed=SEED, palette=PALETTE, accent="orange")
    print(thumb)
