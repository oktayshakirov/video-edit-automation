"""Love Swipe pick-a-truth #13 - vertical, TikTok, `ember` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['ember']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Fated Souls | f36, f44 |
| 2 | Twin Flames | tf23, tf21 |
| 3 | Sugar & Spice | ss34, ss48 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-13.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'ember'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        '{player1}, is {player2} a good driver?',
        '{player1}, if time froze for everyone but you and {player2} for one day, what would you do?',
        deck='Fated Souls'),
    Round.from_app(
        '{player1}, is {player2} secretly competitive, openly competitive, or a sore loser?',
        "{player1}, what's the little everyday thing that makes {player2}'s whole day?",
        deck='Twin Flames'),
    Round.from_app(
        '{player1}, if {player2} cooked something blindfolded, would you eat it?',
        "{player1}, what's the best meal you two have ever cooked together?",
        deck='Sugar & Spice'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
