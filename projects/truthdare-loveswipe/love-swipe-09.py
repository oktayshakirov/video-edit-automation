"""Love Swipe pick-a-truth #9 - vertical, TikTok, `blush` look, cold intro.

Batch two (2026-11-07): cold open - the first card lands on frame zero, no title. Ground, card neons and header colour
are `series.LOOKS['blush']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batch one:

| round | deck | cards |
|---|---|---|
| 1 | Stolen Hearts | h40, h12 |
| 2 | Fated Souls | f40, f7 |
| 3 | Honeymoon Fever | hm32, hm50 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-09.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'blush'
INTRO = 'cold'

ROUNDS = [
    Round.from_app(
        '{player1}, between you and {player2}, who becomes a bigger baby when sick?',
        '{player1}, if you met {player2} today, where would you take them on a first date?',
        deck='Stolen Hearts'),
    Round.from_app(
        "{player1}, if {player2} were arrested and you didn't know why, what would you assume happened?",
        "{player1}, what's the best way to make {player2} feel special?",
        deck='Fated Souls'),
    Round.from_app(
        '{player1}, which of you two would get you both kicked out of a tour group?',
        '{player1}, if your next anniversary could be anywhere in the world, where are you taking {player2}?',
        deck='Honeymoon Fever'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
