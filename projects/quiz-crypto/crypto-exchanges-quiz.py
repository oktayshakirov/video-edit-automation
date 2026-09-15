"""Three questions on how crypto exchanges actually work - ~95s vertical quiz.

Source: crypto-wiki/content/posts/understanding-crypto-exchanges.mdx, which
already has a long+short explainer pair - this is quiz #1 for the channel,
and the article's own custodial-vs-non-custodial split is the whole quiz.

**Every wrong option is a real fact about the other kind of exchange, not an
invented distractor.** The three questions test the same confusion from three
angles - who holds the keys, how a trade gets matched, what happens when it
goes wrong - and every "wrong" card is something the article says is true of
a CEX, offered as the wrong answer to a question about a DEX (and vice versa
in Q1). That is what makes them plausible: a viewer who half-remembers the
article picks the CEX fact for the DEX question because the two mechanisms
rhyme.

| # | tests | wrong options are true statements about |
|---|---|---|
| 1 | who holds a CEX deposit | a DEX (self-custody, "nobody's", smart contract) |
| 2 | how a DEX matches a trade | a CEX (order book, KYC, an intermediary) |
| 3 | what custodial risk means when a CEX is hacked | the reassurances the article explicitly does *not* offer (regulation is listed as a con, not a guarantee) |

**No direction, no platform named as the right one** - the safety line for
this channel (`docs/video/projects/crypto.md`, `docs/video/projects/quiz.md`).
Every question asks about mechanism - what "custodial" means, how a trade
clears without a company in the middle - never which exchange to use or which
is safest. No exchange name appears anywhere in the script.

**No thumbnail render.** The format's own convention - see
`docs/video/projects/quiz.md` and the skill.

**Opens on "Crypto Quiz: Exchanges Edition", no number and no second intro
card** - the settled default for this format (2026-09-08).

**A card shows its letter but never speaks it.** See `LETTER_SPOKEN` in
`quiz.build` for the full eight-attempt account before touching this.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/quiz-crypto/crypto-exchanges-quiz.py
"""

from pathlib import Path

from video_automation.quiz.build import Question, render_quiz_short

SOURCE_POST = "understanding-crypto-exchanges"

TITLE = ("Crypto Quiz: Exchanges Edition", "Crypto quiz, exchanges edition.")

QUESTIONS = [
    # Whose wallet actually holds a CEX deposit. The wrong options are all
    # true of a DEX (self-custody via smart contract, no pooled custody) -
    # offered here as wrong answers to test whether the viewer confuses the
    # two mechanisms.
    Question(
        question="Whose wallet holds your crypto on a centralized exchange?",
        options=("Your own wallet, like always",
                  "The exchange's own pooled wallet",
                  "Nobody's - it just stays on-chain",
                  "A smart contract only you control"),
        correct=1,
        answer="A CEX is custodial - it holds the keys, not you. "
               "That's what a DEX does instead."),

    # How a DEX matches a trade with no company in the middle. The three
    # wrong options are all real CEX facts from the article (order book,
    # identity verification, an intermediary approving the trade).
    Question(
        question="How does a DEX match your trade with no company involved?",
        options=("It matches orders on a book, like a company would",
                  "Trades price against a shared liquidity pool",
                  "You verify your identity and it executes for you",
                  "An employee approves the trade before it clears"),
        correct=1,
        answer="No company matches your order - code prices it "
               "against a shared pool instead."),

    # What custodial risk actually means. The wrong options are the false
    # comforts the article never offers - regulation is listed as a con
    # ("subject to government regulations and potential shutdowns"), not a
    # guarantee, which is exactly the confusion this card tests.
    Question(
        question="A centralized exchange gets hacked and drained. "
                 "What happens to your funds there?",
        options=("Nothing - you held the keys all along",
                  "Regulation guarantees you get it all back",
                  "It's restored once the exchange reopens",
                  "You can lose it - the exchange held the keys"),
        correct=3,
        answer="Custodial means the exchange's security is your risk too, "
               "not just theirs."),
]


def main() -> None:
    out = Path.home() / "Desktop/quiz-crypto-exchanges.mp4"
    work = Path.home() / "Desktop/.quiz-crypto-exchanges-work"
    path, total = render_quiz_short(
        QUESTIONS,
        ("How many did you get?",),
        out, work, title=TITLE)
    print(f"{path}  {total:.1f}s")


if __name__ == "__main__":
    main()
