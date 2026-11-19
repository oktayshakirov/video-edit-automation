"""Love Swipe pick-a-truth #16 - vertical, TikTok, `rosegold` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['rosegold']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Honeymoon Fever | hm43, hm35 |
| 2 | Partners in Crime | pc26, pc6 |
| 3 | Ever After | ea36, ea8 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-16.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'rosegold'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        '{player1}, who packs faster, you or {player2} — and who packs better?',
        "{player1}, if you had 24 hours in Paris with {player2}, what's the one thing you'd refuse to skip?",
        deck='Honeymoon Fever'),
    Round.from_app(
        "{player1}, what's the pettiest revenge you've ever taken?",
        "{player1}, what's one thing you and {player2} could get away with that nobody would ever suspect?",
        deck='Partners in Crime'),
    Round.from_app(
        '{player1}, whose family traditions win each holiday — honestly?',
        "{player1}, what worry about the future disappears when you're with {player2}?",
        deck='Ever After'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
