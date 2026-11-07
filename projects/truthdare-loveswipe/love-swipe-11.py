"""Love Swipe pick-a-truth #11 - vertical, TikTok, `grove` look, cold intro.

Batch two (2026-11-07): cold open - the first card lands on frame zero, no title. Ground, card neons and header colour
are `series.LOOKS['grove']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batch one:

| round | deck | cards |
|---|---|---|
| 1 | Love Nest | ln19, ln37 |
| 2 | Fated Souls | f42, f3 |
| 3 | Sugar & Spice | ss28, ss5 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-11.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'grove'
INTRO = 'cold'

ROUNDS = [
    Round.from_app(
        "{player1}, who would win a 'who left this here?' investigation — you or {player2}?",
        '{player1}, what home tradition from your childhood do you want to keep alive?',
        deck='Love Nest'),
    Round.from_app(
        '{player1}, did you stalk {player2} on social media before you first met?',
        '{player1}, what would be an accurate description of your relationship with {player2}?',
        deck='Fated Souls'),
    Round.from_app(
        "{player1}, who's the better cook between you two — honestly?",
        '{player1}, what dish from your childhood do you wish you could taste one more time?',
        deck='Sugar & Spice'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
