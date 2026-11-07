"""Love Swipe pick-a-truth #10 - vertical, TikTok, `noir` look, flash intro.

Batch two (2026-11-07): flash intro - the Love Swipe card and "Couples, pick one.", first card at ~1.5s. Ground, card neons and header colour
are `series.LOOKS['noir']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batch one:

| round | deck | cards |
|---|---|---|
| 1 | Twin Flames | tf42, tf48 |
| 2 | Partners in Crime | pc24, pc46 |
| 3 | Timeless Love | t28, t53 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-10.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'noir'
INTRO = 'flash'

ROUNDS = [
    Round.from_app(
        '{player1}, who texts first after an argument — you or {player2}?',
        "{player1}, what's {player2}'s favorite way to be comforted after a bad day?",
        deck='Twin Flames'),
    Round.from_app(
        '{player1}, have you ever pretended not to see a text? How recently?',
        "{player1}, what's the boldest thing you've ever done to get {player2}'s attention?",
        deck='Partners in Crime'),
    Round.from_app(
        '{player1}, which of your habits does {player2} find strangest?',
        "{player1}, what's something {player2} said that you'll never forget?",
        deck='Timeless Love'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
