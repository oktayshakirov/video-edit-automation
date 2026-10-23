"""The `spotlight` beat, narrated. **Not a publishable video.**

Zoom into part of a photograph, one detail per sentence, through the real
`render_long` path. The FBI poster is a US federal government work (public
domain); see `assets/crypto/ruja-ignatova/CREDITS.md`. The regions below are
rough on purpose - `beats.spotlight.snap` fits each ring to the content, so a
box typed by hand can no longer cut a line of text.

    PYTHONPATH=. .venv/bin/python projects/demo/spotlight.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.crypto.shots import Shot
from video_automation.longform import Section, render_long

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects/demo/out"
POSTER = ROOT / "assets/crypto/ruja-ignatova/ruja-fbi.jpg"

SECTIONS = [
    Section(
        title="Most wanted", card=False,
        sentences=[
            ("This is the poster the FBI published in twenty twenty-two.",),
            ("Ruja Ignatova, on the Ten Most Wanted list.",),
            ("The charges run to wire fraud, money laundering and securities fraud.",),
            ("And one of the three photos looks like it came from a passport.",),
            ("She has not been seen since twenty seventeen.",),
        ],
        shots=[Shot(graphic="spotlight", payload=(
            POSTER,
            # One entry per sentence: open on the whole poster, end on it.
            [(None, ""),
             ((0.17, 0.02, 0.94, 0.27), "Ten Most Wanted"),
             ((0.01, 0.42, 0.63, 0.475), "The charges"),
             ((0.68, 0.51, 0.98, 0.995), "The passport photo"),
             (None, "")],
            "")),
            None, None, None, None],
    ),
]

if __name__ == "__main__":
    made = render_long(SECTIONS, OUT / "spotlight.mp4", OUT / "spotlight-work",
                       brand=CRYPTO, voice="mia",
                       music=music.track("night-drift"), callouts=None,
                       special_cuts=False)
    print(made["video"])
