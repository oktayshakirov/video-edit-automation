"""Love Swipe pick-a-truth #6 - ~55s vertical, TikTok, `loveswipe-midnight` ground.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`).
Each round is two real truths from one non-NSFW deck - one light, one more
personal - and the couple picks one to answer:

| round | deck | cards |
|---|---|---|
| 1 | Honeymoon Fever | hm7, hm49 |
| 2 | Love Nest | ln27, ln39 |
| 3 | Ever After | ea43, ea50 |

`Round.from_app` turns the app's `{player1}`/`{player2}` into "you" and
"your partner"; nothing else in the card text is changed. Title, outro and
render settings are shared across the series in `series.py`; the format is
`video_automation/quiz/truthdare.py`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-06.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
BACKDROP = "loveswipe-midnight"

ROUNDS = [
    Round.from_app(
        "{player1}, on a road trip with {player2}, who drives and who controls the music?",
        "{player1}, what's one place you'd only ever go back to with {player2}?",
        deck="Honeymoon Fever"),
    Round.from_app(
        "{player1}, what's the weirdest thing a guest could find in your home?",
        "{player1}, what does {player2} do around the house that you quietly appreciate?",
        deck="Love Nest"),
    Round.from_app(
        "{player1}, what's one thing you two will definitely still argue about in 2050?",
        "{player1}, what are you most excited about in your future with {player2}?",
        deck="Ever After"),
]


def main() -> None:
    series.render(__file__, ROUNDS, BACKDROP)


if __name__ == "__main__":
    main()
