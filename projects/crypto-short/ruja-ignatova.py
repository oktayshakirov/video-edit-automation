"""Ruja Ignatova — the coin that never existed. ~55s crypto short.

Source: crypto-wiki/content/crypto-ogs/ruja-ignatova.mdx. Built as a pair with
`crypto-long/ruja-ignatova.py`.

**The angle is in the first line: how do you sell a cryptocurrency that does not
exist?** OneCoin took in over four billion dollars with no blockchain, no mined
coins, and no way to cash out. Fraud mechanics, not financial advice: the script
describes how the con worked and the one check that would have caught it. No
price level, no prediction, no buy/sell. The outro asks one question and stops.

**"Ruja" is Bulgarian (Ружа), said "ROO-zha".** The spoken half of the name
chunk respells it `Roozha`; the caption keeps `Ruja`.

**The music bed is automatic now** — `render_crypto_short` defaults `music` to
`night-drift` and `music_gain` to 0.85, so this file passes neither.

**Photographs.** The site's OG portrait is 441x441; her pictures come from
Wikimedia Commons (`assets/crypto/ruja-ignatova/CREDITS.md`). `ruja-glamour.jpg`
is CC BY-SA 2.0 — the attribution block belongs in any published description.
Each image is used once, except the glamour crop (open and close bookend).

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/ruja-ignatova.py
"""

from pathlib import Path

from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.thumb import render_short_thumb

RUJA = Path(__file__).resolve().parents[2] / "assets/crypto/ruja-ignatova"
POSTS = SITE_IMAGES / "posts"

# Stock, screened at 0.5/3/6/9s. Shared with the long form (one video for the
# reuse rule) — each used at most twice across the pair, far apart.
AUDIENCE_2 = STOCK / "videos/conference-audience-auditorium-dark/7988642.mp4"     # 13s L12 S8
KEYBOARD = STOCK / "videos/hands-typing-keyboard-dark-close-up/5289120.mp4"       # 20s L6-8 S2-4
CROWD_CONCERT = STOCK / "videos/concert-crowd-stage-lights-dark/26745109.mp4"     # 11s L5-12 S14-21
PLANE_WINDOW = STOCK / "videos/airplane-night-flight-window/19229592.mp4"         # 15s L4-7 S2-5

VOICE = "mia"                   # female, af_heart. Matches the long form.

# One tuple per sentence; each string is one caption. A chunk may be a
# (caption, spoken) pair. The checklist beat must have one caption per item.
SENTENCES = [
    ("How do you sell a cryptocurrency",
     "that does not exist?"),

    ("It was called OneCoin.",
     "It took in over four billion dollars.",
     "It never had a blockchain."),

    ("The coin was rows in a database.",
     "The mining was a screen animation."),

    ("You could not sell it anywhere real.",
     "You could only recruit the next person in."),

    # the checklist. Two-phase: four questions sit unmarked, then all four
    # crosses land in the pause. The fifth chunk is a reaction line.
    ("Could you inspect the blockchain?",
     "Trade it off their platform?",
     "Use it without recruiting anyone?",
     "Withdraw your money on request?",
     "No. None of it."),

    ("So why did millions believe her?",
     (("Doctor Ruja Ignatova had a law doctorate,",
       "Doctor Roozha Ignahtova had a law doctorate,")),
     "with Oxford and McKinsey behind her."),

    ("Regulators called it a scam by twenty sixteen.",
     "It kept growing."),

    ("In October twenty seventeen,",
     "she flew from Sofia to Athens and vanished."),

    ("She is on the FBI's Ten Most Wanted list,",
     "with a five million dollar reward for information."),

    # the closing statement card - a line hands off to it.
    (("STILL MISSING", "Nearly a decade on, she is still missing."),),

    ("So, what do you think -",
     "where is she now?"),
]

SHOTS = [
    # 1 - the hook, on the OneCoin publicity portrait, over the title question.
    Shot(image=RUJA / "ruja-glamour.jpg",
         zoom=1.10, pan=(0.02, -0.02), aspect=1.15, bias=0.20),

    # 2 - a seated audience being sold the pitch.
    Shot(clip=AUDIENCE_2, clip_at=1.0),

    # 3 - hands typing at a dark keyboard: the coin was rows entered by hand.
    Shot(clip=KEYBOARD, clip_at=2.0),

    # 4 - the site's own photo of Ruja at the OneCoin desk.
    Shot(image=POSTS / "one-coin.jpeg",
         zoom=1.13, pan=(-0.02, 0.02), aspect=1.15, bias=0.40),

    # 5 - the check, as a drawn beat.
    Shot(graphic="checklist",
         payload=([("A blockchain you can inspect", False),
                   ("Trading off their platform", False),
                   ("A use that needs no recruiting", False),
                   ("A withdrawal that clears", False)],
                  "COULD YOU CHECK ANY OF IT?")),

    # 6 - the tight portrait crop, for "why did millions believe".
    Shot(image=RUJA / "ruja-portrait.jpg",
         zoom=1.13, pan=(-0.03, 0.01), aspect=1.15, bias=0.15),

    # 7 - a concert crowd: the arenas, the growth despite the warnings.
    Shot(clip=CROWD_CONCERT, clip_at=1.0),

    # 8 - a plane window at night: the flight to Athens.
    Shot(clip=PLANE_WINDOW, clip_at=2.0),

    # 9 - the FBI poster on the Ten Most Wanted line (it carries the reward).
    Shot(image=RUJA / "ruja-fbi.jpg",
         zoom=1.12, pan=(0.02, 0.02), aspect=1.15, bias=0.35),

    # 10 - the full-screen statement card.
    Shot(graphic="chapter", payload=("STILL MISSING",)),

    # 11 - the ask, back on the glamour portrait (open/close bookend).
    Shot(image=RUJA / "ruja-glamour.jpg",
         zoom=1.14, pan=(-0.03, 0.01), aspect=1.15, bias=0.15),
]

EMOJI = {
    "It never had a blockchain.": "\U0001f6ab",   # 🚫
}

# Silence after each sentence. The checklist (index 4) buys the long pause for
# its verdicts; the statement card (index 9) gets room to sit.
GAPS = [0.85, 0.55, 0.40, 0.55, 2.10, 0.55, 0.50, 0.55, 0.55, 1.30, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-ruja-ignatova-short.mp4"
    work = Path.home() / "Desktop/.crypto-ruja-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS)

    # Vertical thumbnail. 2-word accent keeps it to two lines clear of her
    # face; the long form uses a 1-word accent for its taller vertical fill.
    # `band="bottom"` - her head is in the top half of the crop.
    thumb = render_short_thumb(
        Path.home() / "Desktop/crypto-ruja-ignatova-short-thumb.jpg",
        CRYPTO, "The coin that [never existed]",
        image=RUJA / "ruja-glamour.jpg", accent="yellow", band="bottom")
    print(f"{out}  {total:.2f}s")
    print(f"thumb: {thumb}")


if __name__ == "__main__":
    main()
