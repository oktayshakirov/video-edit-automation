"""Love Swipe pick-a-truth #1 - ~55s vertical, TikTok, `loveswipe-neon` ground.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`).
Each round is two real truths from one non-NSFW deck - one light, one more
personal - and the couple picks one to answer:

| round | deck | cards |
|---|---|---|
| 1 | Stolen Hearts | h1, h30 |
| 2 | Partners in Crime | pc2, pc10 |
| 3 | Sugar & Spice | ss19, ss15 |

The first of the series and the cut the format was settled on: two truths a
round rather than a truth and a dare (six seconds is time to choose, not to
do a dare), cards low in the frame with the ring between them, titled with
the app's name.

`Round.from_app` turns the app's `{player1}`/`{player2}` into "you" and
"your partner"; nothing else in the card text is changed. Title, outro and
render settings are shared across the series in `series.py`; the format is
`video_automation/quiz/truthdare.py`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-01.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
BACKDROP = "loveswipe-neon"

ROUNDS = [
    Round.from_app(
        "{player1}, what's the worst haircut you've ever had?",
        "{player1}, how did you try to impress {player2} at the beginning of your relationship?",
        deck="Stolen Hearts"),
    Round.from_app(
        "{player1}, if you and {player2} pulled a heist, who's the brains and who's the muscle?",
        "{player1}, what did you get away with as a teenager that your parents still don't know about?",
        deck="Partners in Crime"),
    Round.from_app(
        "{player1}, what do you always steal off {player2}'s plate?",
        "{player1}, if {player2} were a dessert, which one would they be?",
        deck="Sugar & Spice"),
]


def main() -> None:
    series.render(__file__, ROUNDS, BACKDROP)


if __name__ == "__main__":
    main()
