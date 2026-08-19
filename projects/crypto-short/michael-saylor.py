"""Michael Saylor — the corporate treasury bet. ~60s crypto short.

Source: crypto-wiki/content/crypto-ogs/michael-saylor.mdx.

The angle is in the first line: a boring software company emptied its bank
account. That is concrete, surprising, and needs no financial advice — the
script reports what the company did and what it cost, and ends on a question
rather than a verdict.

**The photographs are not the site's.** Both Saylor images in
`crypto-wiki/public/images` are under the ~750px floor the blurred-fill layout
needs (700x348 and 500x472), so a piece about a person had no usable picture of
him. The four portraits come from Wikimedia Commons instead, all Creative
Commons and all 2000-8000px wide; see `assets/crypto/michael-saylor/CREDITS.md`
for the attribution the licences require, which belongs in the description of
anything published. Everything else is the site's own library, as usual.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/michael-saylor.py
"""

from pathlib import Path

from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot

SAYLOR = Path(__file__).resolve().parents[2] / "assets/crypto/michael-saylor"
POSTS = SITE_IMAGES / "posts"

VOICE = "mia"                   # female, af_heart — the highest-graded English
                                # voice in Kokoro. Still a candidate, not approved.

# One tuple per sentence; each string inside it is one caption. The sentence is
# spoken whole, so chunking finely costs no prosody. The two checklist beats
# must have exactly one caption per item — that is what times their reveals.
SENTENCES = [
    ("In 2020,",
     "a boring software company",
     "emptied its bank account",
     "and bought Bitcoin."),

    ("Michael Saylor co-founded",
     "MicroStrategy back in 1989.",
     "It sold business software.",
     "Nothing about it was exciting."),

    # checklist: what a company can do with idle cash
    ("Leave the cash in the bank.",
     "Buy back your own stock.",
     "Park it in bonds.",
     "Or put all of it into Bitcoin."),

    ("He picked the last one,",
     "and said why out loud:",
     "cash was quietly losing value."),

    ("The first purchase was",
     "250 million dollars.",
     "Then he never stopped."),

    ("Debt offerings, share sales,",
     "profits from the software business —",
     "all of it went into Bitcoin."),

    ("By 2025 the company held",
     "over half a million coins,",
     "the largest corporate stack on earth."),

    # checklist: what that turned the company into
    ("It is barely a software business now.",
     "It is not a safe cash cushion.",
     "It is a leveraged bet on one asset."),

    ("He stepped back as chief executive",
     "to work on that bet full time,",
     "and renamed the company Strategy."),

    ("Visionary, or the biggest gamble",
     "in corporate history?",
     "Tell me what you think."),
]

SHOTS = [
    # 1 — the hook, on the closest portrait in the set. The one genuinely
    # portrait-shaped source, so it is the shot that decides the caption line:
    # at aspect 1.05 its photo ran to 1500px and left the type 5px of air.
    Shot(image=SAYLOR / "saylor-portrait.jpg",
         zoom=1.10, pan=(0.02, -0.02), aspect=1.12, bias=0.10),

    # 2 — young Saylor behind a MicroStrategy podium: the boring years, shown.
    Shot(image=SAYLOR / "saylor-keynote.jpg",
         zoom=1.13, pan=(-0.03, 0.02), aspect=1.15, bias=0.45),

    # 3 — the drawn beat. Corporate glass behind it, because the question is a
    # corporate one; four options, and only the last is ticked.
    Shot(graphic="checklist",
         payload=([("Leave it in the bank", False),
                   ("Buy back stock", False),
                   ("Park it in bonds", False),
                   ("Buy Bitcoin", True)],
                  "CORPORATE CASH, 2020"),
         backdrop=POSTS / "corporate.jpg"),

    # 4 — a dollar bill on fire says "losing value" without the script claiming it.
    Shot(image=POSTS / "bitcoin-vs-fiat.jpg",
         zoom=1.12, pan=(0.03, 0.02), aspect=1.15, bias=0.45),

    Shot(image=POSTS / "bitcoin.jpg",
         zoom=1.14, pan=(-0.02, -0.02), aspect=1.15, bias=0.5),

    # 6 — the conviction shot, fist raised, for the beat about funding it all.
    Shot(image=SAYLOR / "saylor-speaking.jpg",
         zoom=1.12, pan=(0.03, -0.01), aspect=1.15, bias=0.35),

    Shot(image=POSTS / "bitcoin-neon.jpg",
         zoom=1.15, pan=(-0.03, 0.01), aspect=1.15, bias=0.5),

    # 8 — the second drawn beat, and the honest one: the criticism from the
    # article, shown as a list rather than argued.
    Shot(graphic="checklist",
         payload=([("A software business", False),
                   ("A cash cushion", False),
                   ("A leveraged Bitcoin bet", True)],
                  "WHAT IT IS NOW"),
         backdrop=POSTS / "analysis.jpg"),

    Shot(image=SAYLOR / "saylor-stage.jpg",
         zoom=1.12, pan=(0.02, 0.02), aspect=1.15, bias=0.5),

    # 10 — back to the face for the question, cropped differently so the repeat
    # reads as a return rather than as the same shot.
    Shot(image=SAYLOR / "saylor-portrait.jpg",
         zoom=1.13, pan=(-0.03, 0.01), aspect=1.15, bias=0.05),
]

EMOJI = {
    "cash was quietly losing value.": "📉",
    "Tell me what you think.": "👇",
}

# Silence after each sentence. The two checklist beats (2 and 7) buy themselves
# a long one: the options are all on screen and unmarked, the voice stops, and
# the verdicts land into that pause with the marks. Everything else stays tight,
# because a pause is what a viewer scrolls away during.
GAPS = [0.34, 0.34, 2.10, 0.34, 0.34, 0.34, 0.34, 1.90, 0.34, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-saylor-treasury.mp4"
    work = Path.home() / "Desktop/.crypto-saylor-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS)
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
