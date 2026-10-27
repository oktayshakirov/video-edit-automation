"""Love Swipe pick-a-truth #2 - ~55s vertical, TikTok, `loveswipe-ruby` ground.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`).
Each round is two real truths from one non-NSFW deck - one light, one more
personal - and the couple picks one to answer:

| round | deck | cards |
|---|---|---|
| 1 | Timeless Love | t13, t33 |
| 2 | Twin Flames | tf2, tf9 |
| 3 | Honeymoon Fever | hm14, hm31 |

`Round.from_app` turns the app's `{player1}`/`{player2}` into "you" and
"your partner"; nothing else in the card text is changed. Title, outro and
render settings are shared across the series in `series.py`; the format is
`video_automation/quiz/truthdare.py`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-02.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
BACKDROP = "loveswipe-ruby"

ROUNDS = [
    Round.from_app(
        "{player1}, what's the most awkward date you've ever been on?",
        "{player1}, what's the very first thing you ever said to {player2}?",
        deck="Timeless Love"),
    Round.from_app(
        "{player1}, what's {player2}'s most-used emoji?",
        "{player1}, what do you think {player2} loves most about you?",
        deck="Twin Flames"),
    Round.from_app(
        "{player1}, what's the worst travel mishap you've survived?",
        "{player1}, if your love story was a destination, what would it be?",
        deck="Honeymoon Fever"),
]


def main() -> None:
    series.render(__file__, ROUNDS, BACKDROP)


if __name__ == "__main__":
    main()
