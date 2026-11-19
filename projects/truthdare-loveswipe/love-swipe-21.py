"""Love Swipe pick-a-truth #21 - vertical, TikTok, `noirgold` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['noirgold']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Partners in Crime | pc45, pc40 |
| 2 | Timeless Love | t32, t34 |
| 3 | Sugar & Spice | ss20, ss45 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-21.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'noirgold'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        '{player1}, which of you two keeps secrets better?',
        "{player1}, what skill does {player2} have that you'd want on your heist crew?",
        deck='Partners in Crime'),
    Round.from_app(
        '{player1}, what do you confidently pretend to be good at?',
        "{player1}, how does {player2} know you're stressed before you say a word?",
        deck='Timeless Love'),
    Round.from_app(
        '{player1}, cooking together: romantic teamwork or kitchen warfare?',
        '{player1}, what fruit is {player2}? Explain yourself.',
        deck='Sugar & Spice'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
