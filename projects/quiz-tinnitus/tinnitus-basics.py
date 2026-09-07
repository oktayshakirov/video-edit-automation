"""Three tinnitus myths and mechanisms - ~75s vertical quiz Short.

Source: none. `SOURCE_POST = None` — this is an off-site topic rather than a
quiz drawn from one tinnitushelp.me article, and it ships that way on the
user's explicit call after watching the engine-verification render this
project reproduces (2026-09-08). See `HANDOFF-PUBLISH.md` for the record.

**The questions are general audiology, not site-specific.** Each answer is
correct against the wider clinical consensus this format's own doc requires
(`docs/video/projects/quiz.md`) rather than against a specific post's
`quickFacts` — the tradeoff of building without a source article. None of the
three makes a diagnostic or treatment claim; Q3's "correct" option is the
inverse of a myth, not an instruction.

**First video in the format.** It is also what shook out `otis` as the
format's voice, `run_break` for guaranteed pauses, and the letter-stays-with-
its-option rule — see `quiz.build`'s module docstring and
`docs/video/projects/quiz.md` for what each of those cost to learn.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/quiz-tinnitus/tinnitus-basics.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_short_thumb
from video_automation.quiz.build import Question, render_quiz_short

SOURCE_POST = None

QUESTIONS = [
    Question(
        question="Where does tinnitus actually come from?",
        options=("Damage to the hair cells", "Too much earwax",
                 "The brain filling a gap", "Low blood pressure"),
        correct=2,
        answer="The brain fills in a signal the ear stopped sending."),
    Question(
        question="Does silence make tinnitus louder?",
        options=("It has no effect", "It can make it more noticeable",
                 "It cures it", "It damages the ear"),
        correct=1,
        answer="Quiet rooms remove the sound that was covering it."),
    Question(
        question="Which of these is a myth?",
        options=("Sound therapy can help", "Stress can worsen it",
                 "Nothing can ever be done", "Sleep affects it"),
        correct=2,
        answer="Nothing can be done is the myth. Habituation is real."),
]


def main() -> None:
    out = Path.home() / "Desktop/quiz-tinnitus-basics.mp4"
    work = Path.home() / "Desktop/.quiz-tinnitus-basics-work"
    path, total = render_quiz_short(
        ("Three questions on tinnitus.", "Most people miss the last one."),
        QUESTIONS,
        ("How many did you get?",),
        out, work, brand=TINNITUS)

    # No site photo exists for a topic with no source post, so the thumbnail
    # is `image=None` — a flat brand.bg field with the type plate. That is
    # the fallback `render_short_thumb` already has, not a special case.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "3 Tinnitus Myths [Tested]", accent="red", band="top")

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short/Reel cover")


if __name__ == "__main__":
    main()
