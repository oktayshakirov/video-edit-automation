"""Love Swipe pick-a-truth #8 - vertical, TikTok, `lagoon` look, flash intro.

Batch two (2026-11-07): flash intro - the Love Swipe card and "Couples, pick one.", first card at ~1.5s. Ground, card neons and header colour
are `series.LOOKS['lagoon']`.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`),
two real truths a round from one non-NSFW deck, none used in batch one:

| round | deck | cards |
|---|---|---|
| 1 | Timeless Love | t6, t29 |
| 2 | Sugar & Spice | ss38, ss10 |
| 3 | Love Nest | ln11, ln4 |

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-08.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
LOOK = 'lagoon'
INTRO = 'flash'

ROUNDS = [
    Round.from_app(
        "{player1}, what's your most irrational fear that you're embarrassed to admit?",
        '{player1}, how did you first try to get {player2} to notice you?',
        deck='Timeless Love'),
    Round.from_app(
        '{player1}, pineapple on pizza: love it, hate it, or secretly fine with it?',
        "{player1}, what's the best thing {player2} has ever cooked or ordered for you?",
        deck='Sugar & Spice'),
    Round.from_app(
        '{player1}, blanket hog, cover thief, or innocent sleeper — which are you?',
        '{player1}, what does your ideal lazy Sunday at home with {player2} look like?',
        deck='Love Nest'),
]


def main() -> None:
    series.render_look(__file__, ROUNDS, LOOK, INTRO)


if __name__ == "__main__":
    main()
