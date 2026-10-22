"""The `reel` beat, narrated. **Not a publishable video.**

A strip of cards the camera travels along, through the real build path so the
camera, the pan whooshes, the label ticks and the card dives can be judged
against the voice. See `longform/beats/reel.py`.

* `crypto` - 16:9. Opens on a clip, the reel **emerges** out of that same clip
  (card one continues it), and **enters** its last card, which the next shot
  continues full-frame. Both cuts should be invisible.
* `tinnitus` - 16:9. The reel enters its last card straight into a chapter
  card.
* `short` - 9:16, the crypto reel as a Short: one sentence, one phrase per card.

    PYTHONPATH=. .venv/bin/python projects/demo/reel.py [crypto|tinnitus|short]
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO, TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform import Section, render_long

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects/demo/out"
V = STOCK / "videos"

GRID = V / "digital-network-grid-gold-dark/28561594.mp4"
BLOCKS = V / "blockchain-blocks-chain-digital-dark/34127877.mp4"
FLOW = V / "abstract-flowing-data-network-dark-blue/28561463.mp4"
SPARK = V / "digital-network-grid-gold-dark/34645139.mp4"

CRYPTO_CARDS = [(GRID, "2009"), (BLOCKS, "2013"), (FLOW, "2015"), (SPARK, "Today")]

CRYPTO_SECTIONS = [
    Section(
        title="How it got here", card=False,
        sentences=[
            ("Every blockchain has a history.",),
            ("Two thousand nine. The first block is mined.",),
            ("Twenty thirteen. A teenager writes the Ethereum paper.",),
            ("Twenty fifteen. The network goes live.",),
            ("And today, nobody runs it at all.",),
            ("This is what that looks like from the inside.",),
        ],
        shots=[Shot(clip=GRID),
               # Card one is the clip above; card four is the clip below.
               Shot(graphic="reel",
                    payload=(CRYPTO_CARDS, "How it got here", True, True)),
               None, None, None,
               Shot(clip=SPARK)],
    ),
    Section(
        title="Who runs it now?", kicker="The answer",
        sentences=[("Thousands of machines, and none of them in charge.",)],
        shots=[Shot(clip=FLOW, clip_at=8.0)],
    ),
]

TINNITUS_SECTIONS = [
    Section(
        title="Four habits", card=False,
        sentences=[
            ("First, the jaw. Notice when you clench it.",),
            ("Second, the desk. Take a break every hour.",),
            ("Third, the evening. Let the room go quiet slowly.",),
            ("And fourth, keep a note of what changes.",),
        ],
        shots=[Shot(graphic="reel", payload=(
                   [(V / "hand-holding-jaw-pain-dark/19149084.mp4", "The jaw"),
                    (V / "hand-on-desk-pause-break-office-night-dark/5473794.mp4",
                     "The desk"),
                    (V / "city-window-night-quiet-room/8591726.mp4", "The evening"),
                    (None, "Keep a note")],
                   "Four habits", True)),
               None, None, None],
    ),
    Section(
        title="Why the note matters", kicker="The pattern",
        sentences=[("Patterns only show up when you write them down.",)],
        shots=[Shot(clip=V / "city-window-night-quiet-room/8591726.mp4",
                    clip_at=12.0)],
    ),
]


def long(site: str) -> None:
    brand, sections = {"crypto": (CRYPTO, CRYPTO_SECTIONS),
                       "tinnitus": (TINNITUS, TINNITUS_SECTIONS)}[site]
    made = render_long(
        sections, OUT / f"{site}-reel.mp4", OUT / f"{site}-reel-work",
        brand=brand, voice="mia", music=music.track("night-drift"),
        callouts=None, special_cuts=False)
    print(made["video"])


def short() -> None:
    sentences = [
        ("Every blockchain has a history.",),
        # One phrase per card, about two seconds each, so the camera settles
        # on every card before it moves on.
        ("Two thousand nine, the first block.",
         "Twenty thirteen, the Ethereum paper.",
         "Twenty fifteen, the network goes live.",
         "And today, the whole world runs it."),
        ("Nobody runs it at all.",),
    ]
    shots = [Shot(clip=GRID),
             Shot(graphic="reel", payload=(CRYPTO_CARDS, "", True, True)),
             Shot(clip=SPARK)]
    out, _ = render_crypto_short(sentences, shots, OUT / "short-reel.mp4",
                                 OUT / "short-reel-work", special_cuts=False)
    print(out)


if __name__ == "__main__":
    for s in (sys.argv[1:] or ["crypto", "tinnitus", "short"]):
        short() if s == "short" else long(s)
