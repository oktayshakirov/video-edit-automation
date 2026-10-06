"""Is a five cent coin smaller than a hundred dollar coin? ~45s crypto short.

Source: crypto-wiki/content/posts/what-is-market-cap-in-crypto.mdx - the same
post as the `market-cap` long form, written in the same pass.

**The single move.** The long form walks the formula, the three ways to
count supply, unlocks and the thin-float twist. The Short does the one move
all of that rests on: price is half of a multiplication, so a five cent coin
can be five times the size of a hundred dollar one - and even that number
depends on which coins you count.

**Re-cut 2026-10-06, after the first review.** The opener was a `Split`
whose divider ran through the type, and the user asked for the long form's
`Stamp` instead. The question also now says what people actually connect a
low price with - more room to grow - and the second beat answers that with
arithmetic (doubling costs the same fifty million at either price; one dollar
across five hundred trillion coins is five times the world economy) rather
than with the long form's grid. Coin footage is down to four shots, each
under a line about a coin; the chain is gone.

**Opener: `Stamp`**, judging the claim "a cheap coin has more room to grow" -
a claim, never a coin. The verdict lands on "price" in sentence 2. The last
three shorts ran `hook=`, `Search` and `Stamp`; the long form runs the same
opener on purpose, because a pair is recognised as a pair.

**Sentence 2 is a partial answer** (`narration.md`, 2026-09-21): "not because
of its price - the price is only half of the sum" makes the other half the
thing the viewer now wants.

**Two beats:** `bars` (three coins through the formula) and `chapter` (the
one figure that ends the argument, full screen - `stat` has no portrait
layout). The world-economy figure is IMF, roughly $100 trillion a year, said
as a ratio so it cannot date.

**Cold close**, recontextualising the opening question rather than asking
one, with `outro=` holding it to the last frame. **No disclaimer** - the long
form carries it. **No financial advice:** no coin is named, rated or
recommended; every figure is the article's worked example or arithmetic on it.

**Clips** are the long form's roster.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/market-cap.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from PIL import Image

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp
from video_automation.longform import thumb as T

SOURCE_POST = "what-is-market-cap-in-crypto"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Screened across their length and on a labelled contact sheet - see the long
# form's header for the rejects.
TWO = V / "coins-on-table-dark-moody/8370544.mp4"                          # 10s, L49-72 S49-69, a silver and a gold coin, rack focus
CALC = V / "calculator-hands-close-up-dark/6963484.mp4"                    # 16s, L77-82 S32-34, two hands on a desk calculator
SPREAD = V / "gold-coins-macro-dark-background/35996678.mp4"               # 10s, L9 S0, coins of different sizes on black
COLUMNS = V / "coins-on-table-dark-moody/8370537.mp4"                      # 9s,  L81-84 S25-27, coins laid out in columns
CASH = V / "hands-exchanging-cash/34579102.mp4"                            # 19s, L68-70 S17-18, a banknote passed hand to hand on dark
PHONE = V / "hand-phone-glow-dark-night/6611948.mp4"                       # 26s, L68-73 S21-22, hands on a phone, the screen a blank glow
STREET = V / "busy-people-walking-city-night/4122942.mp4"                  # 28s, L45-64 S29-36, a packed street at night - clip_at >= 6
SPIN = V / "coin-spinning-on-table-dark/18977071.mp4"                      # 17s, L37-67 S11-22, a coin spinning down to rest

THUMB = ROOT / "assets/crypto/market-cap/meme-coins.jpg"                   # 1536x1024, supplied by the user - see CREDITS.md
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly - and it names the belief the Stamp shows.
    ("Does a five cent coin have more room to grow than a hundred dollar coin?",),

    # The partial answer: new, true, and it opens the other half. "price"
    # lands at ~4.5s, which is the frame the Stamp's verdict lands on.
    ("Not because of its price.", "The price is only half of the sum."),

    ("Market cap is the price, times the coins in circulation.",),

    # Hinge into the bars - its own sentence, so it cannot eat reveal 0.
    ("So run three coins through it.",),

    # The bars' own sentence - one chunk per row.
    ("A hundred dollar coin, with a hundred thousand of them, is ten million.",
     "A fifty dollar coin, with a million of them, is fifty million.",
     "A five cent coin, with a billion of them, is fifty million too."),

    ("To double, the five cent coin needs fifty million more in value.",
     "Exactly what the fifty dollar coin needs."),

    # Hinge into the chapter card.
    ("And a tiny price can hide an enormous supply.",),

    # The card: capitals on screen, a sentence in the voice.
    (("500 TRILLION COINS AT $1 = $500 TRILLION",
      "Five hundred trillion coins at one dollar would be worth "
      "five hundred trillion dollars."),),

    ("Five times what the whole world economy produces in a year.",),

    # Cold close. It answers the opening question instead of re-asking it.
    ("A low price is not room to grow. It is just a lot of coins.",),
]

SHOTS = [
    Shot(clip=TWO, clip_at=1.0, clip_ax=0.80),
    Shot(clip=CALC, clip_at=1.0, clip_ax=0.60),
    Shot(clip=SPREAD, clip_at=0.5, clip_ax=1.0),
    Shot(clip=COLUMNS, clip_at=0.5, clip_ax=0.45),
    Shot(graphic="bars", backdrop=BEATGROUND,
         payload=([("$100 x 100,000 coins", 0.2, "$10M"),
                   ("$50 x 1 million coins", 1.0, "$50M"),
                   ("5 cents x 1 billion coins", 1.0, "$50M")],
                  "PRICE x COINS IN CIRCULATION")),
    Shot(clip=CASH, clip_at=7.0, clip_ax=0.45),
    Shot(clip=PHONE, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="chapter", payload=("500 TRILLION COINS AT $1 = $500 TRILLION",)),
    Shot(clip=STREET, clip_at=8.0, clip_ax=0.50),
    Shot(clip=SPIN, clip_at=2.0, clip_ax=0.40),
]

GAPS = [0.70, 0.80, 0.65, 0.55, 1.30, 0.85, 0.60, 1.30, 0.90, 1.20]


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's image cropped onto the centre coin, the
    same words on two rows - one row across 1080px sets too small to read."""
    im = Image.open(THUMB).convert("RGB")
    im = im.crop((330, 0, 330 + 576, 1024)).resize((1080, 1920), Image.LANCZOS)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "Cheap coin.\nEasy [win?]", 200, 1080 - 2 * 52, 52, fill,
                ink, max_lines=2, max_block=1920 * 0.3, leading=1.02,
                band="top", margin=int(1920 * 0.13), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/market-cap-short.mp4"
    work = Path.home() / "Desktop/.market-cap-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # A belief to overturn, judged as a claim. Lands on "price".
        opener=Stamp("A cheap coin can grow more", "MYTH",
                     at_word="price"),
        outro="A low price is not room to grow. It is just a lot of [coins].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/market-cap-short-thumb.jpg"))
    else:
        main()
