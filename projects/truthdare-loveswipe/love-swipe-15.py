"""Love Swipe pick-a-truth #15 - vertical, TikTok, `blush` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['blush']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Twin Flames | tf46, tf39 |
| 2 | Honeymoon Fever | hm19, hm40 |
| 3 | Stolen Hearts | h28, h50 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-15.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'blush'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        "{player1}, what's {player2}'s energy at 7 a.m. — sunshine, zombie, or gremlin?",
        "{player1}, what's the fastest way to cheer {player2} up?",
        deck='Twin Flames'),
    Round.from_app(
        "{player1}, what's the pettiest argument you and {player2} could have on a trip?",
        "{player1}, what's the best photo you and {player2} have ever taken together, and where was it?",
        deck='Honeymoon Fever'),
    Round.from_app(
        '{player1}, what embarrassing thing do you wait to do until after {player2} leaves the room?',
        '{player1}, have you ever felt proud of {player2}?',
        deck='Stolen Hearts'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
