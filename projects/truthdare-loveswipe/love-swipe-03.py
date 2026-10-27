"""Love Swipe pick-a-truth #3 - ~55s vertical, TikTok, `loveswipe-ocean` ground.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`).
Each round is two real truths from one non-NSFW deck - one light, one more
personal - and the couple picks one to answer:

| round | deck | cards |
|---|---|---|
| 1 | Love Nest | ln6, ln34 |
| 2 | Fated Souls | f32, f50 |
| 3 | Ever After | ea3, ea22 |

`Round.from_app` turns the app's `{player1}`/`{player2}` into "you" and
"your partner"; nothing else in the card text is changed. Title, outro and
render settings are shared across the series in `series.py`; the format is
`video_automation/quiz/truthdare.py`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-03.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
BACKDROP = "loveswipe-ocean"

ROUNDS = [
    Round.from_app(
        "{player1}, who actually controls the thermostat?",
        "{player1}, what's the best part of coming home to {player2}?",
        deck="Love Nest"),
    Round.from_app(
        "{player1}, what's the first thing you would do in a zombie apocalypse?",
        "{player1}, what was one of the first things you told your friends or family about {player2}?",
        deck="Fated Souls"),
    Round.from_app(
        "{player1}, what pet is in your future together?",
        "{player1}, what's the biggest dream you've never said out loud?",
        deck="Ever After"),
]


def main() -> None:
    series.render(__file__, ROUNDS, BACKDROP)


if __name__ == "__main__":
    main()
