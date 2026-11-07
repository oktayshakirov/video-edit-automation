"""Love Swipe pick-a-truth #12 - vertical, TikTok, `electric` look, flash intro.

Batch two (2026-11-07): flash intro - the Love Swipe card and "Couples, pick one.", first card at ~1.5s. Ground, card neons and header colour
are `series.LOOKS['electric']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batch one:

| round | deck | cards |
|---|---|---|
| 1 | Stolen Hearts | h16, h33 |
| 2 | Honeymoon Fever | hm25, hm22 |
| 3 | Ever After | ea39, ea44 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-12.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'electric'
INTRO = 'flash'

ROUNDS = [
    Round.from_app(
        "{player1}, who is more likely to go through bathroom drawers at someone else's house—you or {player2}?",
        '{player1}, if you were to make a mixtape for {player2}, what three songs would you add?',
        deck='Stolen Hearts'),
    Round.from_app(
        '{player1}, if you and {player2} got lost with no phones, who would find the way back?',
        "{player1}, what's a place from your childhood you'd love to show {player2}?",
        deck='Honeymoon Fever'),
    Round.from_app(
        "{player1}, what will be your signature 'old couple' public habit?",
        '{player1}, what would your ten-years-younger self say about {player2}?',
        deck='Ever After'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
