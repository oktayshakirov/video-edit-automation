"""Why AI videos feel fake - the Short of OktAI's opener (~35 s).

The long form's opener on its own, told in order: the robotic read, today's
read, what changed, then the twist - the voice saying it is Oktay. Sources
and the example clips are the long form's
(`projects/oktai-long/why-ai-videos-feel-fake.py`); the Short never pitches.

**Second pass (2026-11-21):** the first voice is the deliberately worse one
the editor asked for (macOS `say`, Daniel), today's is the male explainer
voice (`noah`). They are different engines now, so the line names all three
things that changed - the engine, the pace, whole paragraphs - not "same
voice". The 87 videos are shown, not stated: our own video page scrolling.

Run: `PYTHONPATH=. .venv/bin/python projects/oktai-short/why-ai-videos-feel-fake.py [--draft]`
"""

import sys

from video_automation.core import logos, samples
from video_automation.core import screenplay as sp
from video_automation.crypto.shots import Shot
from video_automation.oktai import build_short, examples, folder, screen

NAME = "why-ai-videos-feel-fake"
TITLE = "My AI voice sounded robotic. Here's what fixed it."

EXAMPLE = ["Hi, I'm the voice of this channel.",
           "I read every script you hear on it."]
CLIPS = examples.make(folder(NAME) / "examples", {
    "oldest": ("oldest", EXAMPLE),
    "today": ("today", EXAMPLE),
})
OLDEST = samples.register(CLIPS["oldest"], "oktai-oldest")
TODAY = samples.register(CLIPS["today"], "oktai-today")


def _after(clip: str) -> float:
    return round(samples.DUR[clip] + samples.LEAD + 0.6, 2)


ROWS = [("AI, at first", "a computer voice, line by line", OLDEST),
        ("AI, today", "our explainer voice", TODAY),
        ("Me", "reading it myself", None)]

# The same take as the long form's (same steps, so the same capture).
SITE_CRYPTO = sp.Browser("https://thecrypto.wiki/videos", [
    sp.wait(1.0), sp.move("a[href*='/videos/'] >> nth=0"), sp.wait(0.8),
    sp.scroll(200), sp.wait(1.2), sp.move("a[href*='/videos/'] >> nth=6"), sp.wait(1.0),
], dark=False, tail=8.0)

SENTENCES = [
    ("This is how the AI voice on my channels sounded at first.",),
    ("And this is how it sounds today.",),
    ("A better engine, a faster read, and whole paragraphs instead of single lines.",),
    ("Eighty seven videos later, I know exactly what made them feel fake.",),
    ("And this voice is me, because on this channel, a person reads every script.",),
]
GAPS = [_after(OLDEST), _after(TODAY), 0.45, 0.45, 0.45]

SHOTS = [
    Shot(graphic="voice", ground="grid", payload=(ROWS[:1],), samples=(OLDEST,)),
    Shot(graphic="voice", ground="grid", payload=(ROWS[:2],), samples=(None, TODAY)),
    Shot(graphic="logos", payload=([(str(logos.path("kokoro")), "The engine")],
                                   "WHAT CHANGED")),
    screen(NAME, "site-crypto", SITE_CRYPTO, vertical=True),
    Shot(graphic="voice", ground="grid", payload=(ROWS,)),
]

# No box on the hook: the opener is the two AI voices; the face arrives with
# "this voice is me". Read by `build_short` below and by the script page.
FACE_HOOK = False
FACE = [("And this voice is me", 4.5)]


def main() -> None:
    out, total = build_short(SENTENCES, SHOTS, NAME, face=FACE,
                             hook=3.0 if FACE_HOOK else None, gap=GAPS,
                             opener_holds=True, emblem="microphone",
                             draft="--draft" in sys.argv)
    print(out, round(total, 1))


if __name__ == "__main__":
    main()
