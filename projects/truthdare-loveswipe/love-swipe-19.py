"""Love Swipe pick-a-truth #19 - vertical, TikTok, `velvet` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['velvet']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Twin Flames | tf38, tf47 |
| 2 | Stolen Hearts | h44, h7 |
| 3 | Ever After | ea11, ea40 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-19.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'velvet'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        "{player1}, what's {player2}'s texting style — dry texts, slow replies, or novels?",
        "{player1}, what tiny gift would make {player2}'s whole week?",
        deck='Twin Flames'),
    Round.from_app(
        "{player1}, what would your and {player2}'s celebrity couple name be?",
        "{player1}, what's your ultimate dream date?",
        deck='Stolen Hearts'),
    Round.from_app(
        '{player1}, what will you two laugh about in 20 years that stresses you out now?',
        '{player1}, what fear about the future can you hand {player2} to carry for a while?',
        deck='Ever After'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
