"""Why AI videos feel fake - the Short of OktAI's opener (~35 s).

The long form's opener on its own, told in order: the robotic read, today's
read, what fixed it, then the twist - the voice saying it is Oktay. Sources
and the example clips are the long form's
(`projects/oktai-long/why-ai-videos-feel-fake.py`); the Short never pitches.

Run: `PYTHONPATH=. .venv/bin/python projects/oktai-short/why-ai-videos-feel-fake.py [--draft]`
"""

import sys

from video_automation.core import samples
from video_automation.crypto.shots import Shot
from video_automation.oktai import build_short, examples, folder

NAME = "why-ai-videos-feel-fake"
TITLE = "My AI voice sounded robotic. Here's what fixed it."

EXAMPLE = ["Hi, I'm the voice of this channel.",
           "I read every script you hear on it."]
CLIPS = examples.make(folder(NAME) / "examples", EXAMPLE)
ROBOTIC = samples.register(CLIPS["robotic"], "oktai-robotic")
TODAY = samples.register(CLIPS["today"], "oktai-today")


def _after(clip: str) -> float:
    return round(samples.DUR[clip] + samples.LEAD + 0.6, 2)


ROWS = [("AI, at first", "slowed, one line at a time", ROBOTIC),
        ("AI, today", "same voice, whole paragraphs", TODAY),
        ("Me", "reading it myself", None)]

SENTENCES = [
    ("This is how the AI voice on my channels sounded at first.",),
    ("And this is how it sounds today.",),
    ("Same voice. I sped it up, and gave it whole paragraphs instead of single lines.",),
    ("Eighty seven videos later, I know exactly what made them feel fake.",),
    ("And this voice is me, because on this channel, a person reads every script.",),
]
GAPS = [_after(ROBOTIC), _after(TODAY), 0.45, 0.45, 0.45]

SHOTS = [
    Shot(graphic="voice", ground="grid", payload=(ROWS[:1],), samples=(ROBOTIC,)),
    Shot(graphic="voice", ground="grid", payload=(ROWS[:2],), samples=(None, TODAY)),
    Shot(graphic="grid", payload=([("Before", "slow, one line at a time"),
                                   ("After", "faster, whole paragraphs")],
                                  "WHAT FIXED IT")),
    Shot(graphic="chapter", payload=("87 AI videos. Every mistake written down.",)),
    Shot(graphic="voice", ground="grid", payload=(ROWS,)),
]

# No box on the hook: the opener is the two AI voices; the face arrives with
# "this one is me". Read by `build_*` below and by the script page.
FACE_HOOK = False
FACE = [("And this voice is me", 4.5)]


def main() -> None:
    out, total = build_short(SENTENCES, SHOTS, NAME, face=FACE, hook=3.0 if FACE_HOOK else None,
                             gap=GAPS, opener_holds=True,
                             draft="--draft" in sys.argv)
    print(out, round(total, 1))


if __name__ == "__main__":
    main()
