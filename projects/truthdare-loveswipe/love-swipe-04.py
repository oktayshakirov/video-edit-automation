"""Love Swipe pick-a-truth #4 - ~55s vertical, TikTok, `loveswipe-sunset` ground.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`).
Each round is two real truths from one non-NSFW deck - one light, one more
personal - and the couple picks one to answer:

| round | deck | cards |
|---|---|---|
| 1 | Timeless Love | t25, t36 |
| 2 | Twin Flames | tf5, tf13 |
| 3 | Sugar & Spice | ss12, ss14 |

`Round.from_app` turns the app's `{player1}`/`{player2}` into "you" and
"your partner"; nothing else in the card text is changed. Title, outro and
render settings are shared across the series in `series.py`; the format is
`video_automation/quiz/truthdare.py`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-04.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
BACKDROP = "loveswipe-sunset"

ROUNDS = [
    Round.from_app(
        "{player1}, what's the most incriminating thing in your search history?",
        "{player1}, when did you know you were serious about {player2}?",
        deck="Timeless Love"),
    Round.from_app(
        "{player1}, what's {player2}'s go-to karaoke song?",
        "{player1}, what was {player2}'s first impression of you? Take a guess.",
        deck="Twin Flames"),
    Round.from_app(
        "{player1}, would you rather never eat cheese again or never eat chocolate again?",
        "{player1}, what's the most romantic meal you two have ever shared?",
        deck="Sugar & Spice"),
]


def main() -> None:
    series.render(__file__, ROUNDS, BACKDROP)


if __name__ == "__main__":
    main()
