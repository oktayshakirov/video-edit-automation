"""Love Swipe pick-a-truth #20 - vertical, TikTok, `copper` look, cold open.

Batch three (2026-11-19), built on batch two's numbers (`series.py`): a cold
open with the first card on frame zero, a warm or dark ground, and a
judge-your-partner card first. Ground, card neons and header colour are
`series.LOOKS['copper']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batches one or
two:

| round | deck | cards |
|---|---|---|
| 1 | Love Nest | ln26, ln38 |
| 2 | Fated Souls | f22, f6 |
| 3 | Honeymoon Fever | hm41, hm26 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-20.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'copper'
INTRO = "cold"

ROUNDS = [
    Round.from_app(
        "{player1}, who's the real handyman between you two?",
        '{player1}, how long could you two survive a power outage before going feral?',
        deck='Love Nest'),
    Round.from_app(
        "{player1}, what's something future generations will make fun of you and {player2} for?",
        "{player1}, what's the best gift that {player2} could give you?",
        deck='Fated Souls'),
    Round.from_app(
        '{player1}, if {player2} planned a surprise trip, would you actually let it stay a surprise?',
        '{player1}, what festival or event somewhere in the world do you want to attend with {player2}?',
        deck='Honeymoon Fever'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
