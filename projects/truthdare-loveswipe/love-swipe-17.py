"""Love Swipe pick-a-truth #17 - vertical, TikTok, `noir` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['noir']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Love Nest | ln49, ln18 |
| 2 | Twin Flames | tf25, tf20 |
| 3 | Fated Souls | f38, f4 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-17.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'noir'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        '{player1}, if you two hosted a dinner party, who cooks and who charms?',
        "{player1}, what's the coziest you've ever felt in your life?",
        deck='Love Nest'),
    Round.from_app(
        '{player1}, what does {player2} do when they think no one is watching?',
        "{player1}, what's {player2}'s favorite memory of you two? Guess before they answer.",
        deck='Twin Flames'),
    Round.from_app(
        '{player1}, if you were stranded on an island with {player2}, what would you do first?',
        "{player1}, what's the most spontaneous thing you and {player2} have ever done as a couple?",
        deck='Fated Souls'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
