"""Steady rain, 4-in/6-out breathing — vertical Short, the long form's companion.

**The Short version of `tinnitus-long/rain-masking-20min.py`, not a trailer
for it.** Same recording, same slate palette, same seed, same 4-in/6-out
breath, so a viewer who has seen one recognises the other as the same piece.

**It needs no tiling.** The source is 600s and a Short is under a minute, so
the plain `bed_file` path trims it. `bed_file_skip=35` still applies, for a
different reason than the long cut's seams: the recording's first 35s are
its own quieter build-in, and a Short that opens on that is a Short that
opens 4 dB under the rain it is selling.

**It opens on the instruction, not on the sound's name.** The waterfall Short
lost 27% at 5.3s opening on "A waterfall, with soft pads". The partial-masking
setting is the counterintuitive part and the reason to stay, so it is the first
line here. The rain measures ~68% in 1–8 kHz (see the long cut), which is what
makes that line honest.

* **`cycles=3`** at a 10s cycle — a 30s breathing block.
* **No CTA.** The outro points at the full session and stops.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/rain-masking-short.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Rain Sounds for Tinnitus (Short).mp4"
BED_FILE = DESKTOP / "Rain.mp3"
BED_SKIP = 35.0

INHALE, HOLD, EXHALE, CYCLES = 4.0, 0.0, 6.0, 3

# Same seed and palette as the 20-minute cut, so the pair reads as one piece.
SEED = 31
PALETTE = ((9, 12, 18), (50, 64, 96), (180, 196, 224), (222, 230, 242))

INTRO = [
    ("Play this rain just below your tinnitus.",),
    ("You should still hear it faintly underneath.",
     "That's the point.",),
    ("Now follow the circle:",
     "four counts in, six counts out.",),
]

# One closing line, nothing after it.
OUTRO = [
    ("There's a full twenty-minute version",
     "of this on the channel.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-rain"),
        bed_file=BED_FILE, bed_file_skip=BED_SKIP,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        seed=SEED, palette=PALETTE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="Rain Sounds", pattern="4 in / 6 out",
        emoji="\U0001F327️",
        seed=SEED, palette=PALETTE, accent="yellow")
    print(thumb)
