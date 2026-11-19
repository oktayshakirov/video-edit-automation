"""Love Swipe pick-a-truth #18 - vertical, TikTok, `crimson` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['crimson']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Partners in Crime | pc15, pc12 |
| 2 | Sugar & Spice | ss7, ss29 |
| 3 | Timeless Love | t5, t55 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-18.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'crimson'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        '{player1}, which of you is more likely to talk your way out of a speeding ticket?',
        "{player1}, if your relationship was a crime-duo movie, what's the title?",
        deck='Partners in Crime'),
    Round.from_app(
        "{player1}, what's your 3 a.m. guilty snack?",
        "{player1}, what's one dish you wish {player2} would make more often?",
        deck='Sugar & Spice'),
    Round.from_app(
        "{player1}, what's the most childish thing you still do when no one's watching?",
        "{player1}, what's one thing you hope {player2} never stops doing?",
        deck='Timeless Love'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
