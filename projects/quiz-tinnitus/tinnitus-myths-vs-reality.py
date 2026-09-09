"""Three tinnitus myths, tested - ~94s vertical quiz Short.

Source: tinnitus-blog/content/posts/tinnitus-myths-vs-reality.mdx, which is
already structured as eight myth/reality pairs. That structure is why this
article was picked over every other quiz-eligible post: **the wrong options
are the article's own named myths, not this session's judgement about what
sounds wrong.** Every option below traces to one paragraph of the source.

**This replaces `tinnitus-basics.py`, and the reason is worth keeping.** That
first quiz built three questions with no source article, on the theory that
general audiology consensus would stand in for one. It mostly held — but one
question ("where does tinnitus come from?") set hair-cell damage as a *wrong*
answer against "the brain fills the gap" as the only right one, and that is a
false choice: hair-cell damage is the standard cited *cause*, "the brain fills
the gap" is the *mechanism* by which that cause produces a sound. Marking the
cause wrong read as the channel getting a basic fact wrong. Building from an
article this session did not have to invent a defensible-sounding wrong answer
for is what closes that gap — every option here is something the source
already states as true or names as a myth.

Three of the article's eight myths, chosen for variety of topic (cause,
duration, treatment) over the other five (who gets it, which ear, what it
sounds like, how serious it is):

| # | article's myth | this question's format |
|---|---|---|
| 1 | Only loud noises cause tinnitus | spot the myth among three real causes |
| 2 | Tinnitus is always temporary | spot the myth among three real facts about duration |
| 3 | There is no effective treatment | spot the myth among three real management options |

Every wrong option (the three *true* statements on each card) is also lifted
from the article's own "Reality" paragraph for that myth or an adjacent one —
none of the four cards on any question is invented.

**No thumbnail render.** The format's own convention now — see
`docs/video/projects/quiz.md` and the skill.

**Opens on "Tinnitus Quiz: Myths Edition", no number and no second intro
card.** Both were tried on an earlier cut of this same video and cut on the
user's call (2026-09-08) — the number as an unnecessary flourish, the second
card as redundant with the title.

**A card is read "C." — a real 0.70s pause — then the answer.** Five earlier
cuts of this same video were sent back, each after a different way of trying
to buy that pause: the letter read alone, flat and lengthened ("very weird and
glitchy," and again after a harder trim); kept in the answer's sentence with a
forced splice ("weird cut"); synthesised in the answer's context and trimmed
free of it ("not spoken properly," "cut in the middle"); and a short splice
that only landed on about half the cards. What ships synthesises the letter
and the answer separately and joins them around real silence — see
`LETTER_ANSWER_GAP` in `quiz.build`, including the measurement that was wrong
for two sessions and caused three of those five failures.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/quiz-tinnitus/tinnitus-myths-vs-reality.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.quiz.build import Question, render_quiz_short

SOURCE_POST = "tinnitus-myths-vs-reality"

TITLE = ("Tinnitus Quiz: Myths Edition", "Tinnitus quiz, myths edition.")

QUESTIONS = [
    # Myth 1 in the source: "Only Loud Noises Cause Tinnitus." The three
    # wrong options are drawn straight from the article's own "Reality" list
    # of other causes (ear infections, aging, ototoxic medications).
    Question(
        question="Which of these is a myth about tinnitus?",
        options=("Ear infections can cause it", "Aging can cause it",
                 "Loud noise is the only cause",
                 "Certain medications can trigger it"),
        correct=2,
        answer="Noise raises the risk, but infections, aging and "
               "medication cause it too."),

    # Myth 2: "Tinnitus is Always Temporary and Will Go Away on Its Own."
    Question(
        question="Which of these is a myth about tinnitus?",
        options=("It can fade after loud-noise exposure",
                 "It always resolves within a few days",
                 "For many it becomes a chronic condition",
                 "Persistent tinnitus is worth a doctor's visit"),
        correct=1,
        answer="Some tinnitus fades on its own, but for many it becomes "
               "a long-term condition."),

    # Myth 3: "There's No Effective Treatment or Management for Tinnitus."
    # The three wrong options are three of the article's own listed
    # strategies (sound therapy, CBT, hearing aids) — medication and
    # lifestyle changes are the other two, left out for space.
    Question(
        question="Which of these is a myth about tinnitus?",
        options=("Sound therapy can reduce how noticeable it is",
                 "Cognitive behavioral therapy can help",
                 "There is nothing that can be done about it",
                 "Hearing aids can make it less noticeable"),
        correct=2,
        answer="There is no universal cure, but therapy, CBT and hearing "
               "aids all help manage it."),
]


def main() -> None:
    out = Path.home() / "Desktop/quiz-tinnitus-myths-vs-reality.mp4"
    work = Path.home() / "Desktop/.quiz-tinnitus-myths-vs-reality-work"
    path, total = render_quiz_short(
        QUESTIONS,
        ("How many did you get?",),
        out, work, title=TITLE, brand=TINNITUS)
    print(f"{path}  {total:.1f}s")


if __name__ == "__main__":
    main()
