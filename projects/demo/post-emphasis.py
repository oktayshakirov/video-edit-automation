"""The `post` beat and key-word emphasis, narrated. **Not a publishable video.**

* `long` - 16:9: a headline clipping, a post and a transaction, each
  highlighted as it is read, and two key words punched in over footage.
* `short` - 9:16: the headline clipping as a Short.

Every quoted line is real and documented: the Times headline Satoshi embedded
in Bitcoin's genesis block (3 January 2009), Hal Finney's "Running bitcoin"
(@halfin, 10 January 2009), and the 22 May 2010 pizza purchase (10,000 BTC,
block 57,043). A `post` quotes; it is never a place to invent wording.

    PYTHONPATH=. .venv/bin/python projects/demo/post-emphasis.py [long|short]
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
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

# **Fresh shots per build.** The builders write timings (start, hold,
# reveals) onto the shots they are given, so a shot object shared by the long
# build and the Short carries the long form's reveals into the Short - the
# card arrived late and the highlight never fired, the first time this ran.
def times():
    return Shot(graphic="post", payload=(
    "headline", {"source": "The Times", "date": "3 January 2009",
                 "headline": "Chancellor on brink of [second bailout] for banks"},
    "In the first block"))


HAL = Shot(graphic="post", payload=(
    "post", {"name": "Hal Finney", "handle": "@halfin",
             "date": "10 Jan 2009", "text": "[Running bitcoin]"}, ""))
PIZZA = Shot(graphic="post", payload=(
    "tx", {"label": "Bitcoin transaction · block 57,043",
           "rows": [("Date", "22 May 2010"), ("*Value", "10,000 BTC"),
                    ("For", "Two pizzas")]},
    "The pizza"))

SECTIONS = [
    Section(
        title="Where it started", card=False,
        sentences=[
            ("Bitcoin did not start with a price.", "It started with a headline."),
            ("In its very first block, Satoshi left a line from that morning's paper.",
             "Chancellor on brink of second bailout for banks."),
            ("Nobody knows who Satoshi was.",),
            ("Nine days later, the first person to run it posted this.",
             "Running bitcoin."),
            ("A year after that, someone spent ten thousand coins on two pizzas.",
             "The receipt is still on the chain."),
            ("Today those coins would be worth hundreds of millions.",),
        ],
        shots=[Shot(clip=GRID), times(), Shot(clip=BLOCKS, clip_at=2.0), HAL,
               PIZZA, Shot(clip=FLOW, clip_at=4.0)],
    ),
]


def long() -> None:
    made = render_long(
        SECTIONS, OUT / "post-emphasis.mp4", OUT / "post-emphasis-work",
        brand=CRYPTO, voice="mia", music=music.track("night-drift"),
        callouts=None, special_cuts=False,
        emphasis=["Nobody", "hundreds of millions"])
    print(made["video"])


def short() -> None:
    sentences = [
        ("Bitcoin did not start with a price.",),
        ("In its very first block,", "a headline from that morning's paper."),
        ("Nobody knows who wrote it there.",),
    ]
    shots = [Shot(clip=GRID), times(), Shot(clip=BLOCKS, clip_at=2.0)]
    out, _ = render_crypto_short(sentences, shots, OUT / "post-short.mp4",
                                 OUT / "post-short-work", special_cuts=False)
    print(out)


if __name__ == "__main__":
    for s in (sys.argv[1:] or ["long", "short"]):
        long() if s == "long" else short()
