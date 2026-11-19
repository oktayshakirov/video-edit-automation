"""Love Swipe pick-a-truth #14 - vertical, TikTok, `wine` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['wine']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Partners in Crime | pc25, pc16 |
| 2 | Love Nest | ln41, ln50 |
| 3 | Timeless Love | t2, t40 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-14.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'wine'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        "{player1}, between you and {player2}, who's the good cop and who's the bad cop?",
        '{player1}, what guilty pleasure do you hide from everyone except {player2}?',
        deck='Partners in Crime'),
    Round.from_app(
        "{player1}, what's your side of the bed — and would you ever trade?",
        "{player1}, what's one home upgrade you'd gift {player2} tomorrow if you could?",
        deck='Love Nest'),
    Round.from_app(
        "{player1}, have you ever pretended to laugh at a joke you didn't understand?",
        "{player1}, what's a small gesture that {player2} does that makes you feel loved?",
        deck='Timeless Love'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
