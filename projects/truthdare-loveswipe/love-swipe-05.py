"""Love Swipe pick-a-truth #5 - ~55s vertical, TikTok, `loveswipe-emerald` ground.

Source: the Love Swipe app (`~/Coding/couples-card-game/src/data/decks/`).
Each round is two real truths from one non-NSFW deck - one light, one more
personal - and the couple picks one to answer:

| round | deck | cards |
|---|---|---|
| 1 | Stolen Hearts | h31, h37 |
| 2 | Partners in Crime | pc36, pc32 |
| 3 | Fated Souls | f20, f8 |

`Round.from_app` turns the app's `{player1}`/`{player2}` into "you" and
"your partner"; nothing else in the card text is changed. Title, outro and
render settings are shared across the series in `series.py`; the format is
`video_automation/quiz/truthdare.py`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/truthdare-loveswipe/love-swipe-05.py
"""

import sys
from pathlib import Path

from video_automation.quiz.truthdare import Round

sys.path.insert(0, str(Path(__file__).parent))
import series  # noqa: E402

SOURCE_POST = None      # an app, not an article
DEMAND = None
BACKDROP = "loveswipe-emerald"

ROUNDS = [
    Round.from_app(
        "{player1}, what's your go-to excuse to get out of plans?",
        "{player1}, if you could pick a tattoo for {player2}, what would it be?",
        deck="Stolen Hearts"),
    Round.from_app(
        "{player1}, which movie villain do you secretly root for?",
        "{player1}, what's a secret about you that {player2} unlocked before anyone else?",
        deck="Partners in Crime"),
    Round.from_app(
        "{player1}, if you had one hour to go through a celebrity's phone, whose would it be?",
        "{player1}, what's a memory of {player2} that always makes you laugh?",
        deck="Fated Souls"),
]


def main() -> None:
    series.render(__file__, ROUNDS, BACKDROP)


if __name__ == "__main__":
    main()
