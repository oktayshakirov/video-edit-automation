"""Love Swipe pick-a-truth #7 - vertical, TikTok, `ember` look, cold intro.

Batch two (2026-11-07): cold open - the first card lands on frame zero, no title. Ground, card neons and header colour
are `series.LOOKS['ember']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batch one:

| round | deck | cards |
|---|---|---|
| 1 | Partners in Crime | pc9, pc48 |
| 2 | Twin Flames | tf44, tf45 |
| 3 | Ever After | ea28, ea27 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-07.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'ember'
INTRO = 'cold'

ROUNDS = [
    Round.from_app(
        '{player1}, who would crack first in a police interrogation — you or {player2}?',
        "{player1}, what's one thing you'd only confess under extreme pressure?",
        deck='Partners in Crime'),
    Round.from_app(
        "{player1}, what's {player2}'s 'tell' when they're lying?",
        '{player1}, what compliment makes {player2} melt?',
        deck='Twin Flames'),
    Round.from_app(
        '{player1}, what hobby will you two be insufferable about in retirement?',
        "{player1}, what's one promise you can make {player2} about the next year?",
        deck='Ever After'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
