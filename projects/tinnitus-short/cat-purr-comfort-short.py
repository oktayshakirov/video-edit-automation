"""Cat purring, 4-in/6-out breathing — vertical Short, the long form's companion.

**The Short version of `tinnitus-long/cat-purr-comfort-20min.py`, not a trailer
for it.** Same recording, same amber palette, same seed, same 4-in/6-out
breath, so a viewer who has seen one recognises the other as the same piece at
a different length.

**It does not need the long form's new `bed_file_loop`.** The source is 600s
and a Short is under a minute, so the plain `bed_file` path trims it and there
is no seam at all here. The tiling exists for the 20-minute cut; see that file
for the measurement.

**The measured limit travels with the recording and governs what may be said.**
`band_energy` on this purr: 85.3% below 200 Hz, 0.67% in 1–4 kHz. It covers
almost nothing in the band tinnitus occupies, so this is a **comfort** session
rather than a masking one, and **no line here claims masking** — not the
channel's usual "set it just below your tinnitus", which would be meaningless
for this bed.

**It does not deny masking either.** Both formats state the good case
positively (deep, steady, rhythmic; comfort and contentment) and leave the
claim unmade, which is the whole of the honesty requirement. A comfort session
does not open by telling a distressed listener what the sound will fail to do.

* **`cycles=3`** at a 10s cycle — a 30s breathing block, which leaves room for
  the two intro cards and one closing line inside a ~55-60s Short.
* **No CTA.** The outro points at the full session and stops.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/cat-purr-comfort-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Cat Purring for Tinnitus and Calm (Short).mp4"
BED_FILE = DESKTOP / "1.wav"

INHALE, HOLD, EXHALE, CYCLES = 4.0, 0.0, 6.0, 3

# Same seed and palette as the 20-minute cut, so the pair reads as one piece.
SEED = 23
PALETTE = ((16, 10, 6), (128, 74, 24), (244, 206, 150), (250, 228, 190))

# Opens on the sound, then the honest limit immediately — a viewer who wants
# masking should be told inside the first ten seconds, not kept for the ring.
INTRO = [
    ("Cat purring, around twenty-seven hertz.",
     "Deep, steady and rhythmic.",),
    ("A sound of comfort and contentment.",
     "Keep it quiet, and let it settle around you.",),
    ("Follow the circle:",
     "four counts in, six counts out.",),
]

# One closing line, nothing after it.
OUTRO = [
    ("There's a full twenty-minute version",
     "of this on the channel.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-cat-purr"),
        bed_file=BED_FILE,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        seed=SEED, palette=PALETTE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Cat Purring", pattern="4 in / 6 out", emoji="\U0001F431",
        seed=SEED, palette=PALETTE, accent="cyan")
    print(thumb)
