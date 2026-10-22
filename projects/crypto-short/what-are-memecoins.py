"""Where does a meme coin's price come from? ~45s crypto short.

Source: crypto-wiki/content/posts/what-are-memecoins.mdx - the same post as
the `what-are-memecoins` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks what a meme coin is,
Bitcoin against Dogecoin, the supply, the factory and the four checks. This
does one move, in the order a viewer would ask it (`shorts.md`, 2026-10-13):
where the price comes from (the next buyer), and where the buyer's money
goes (a pool, which the creator can pull). No sum is said aloud; the one
figure is a full-screen card.

**Sentence 2 raises the stakes and keeps the answer back.** "Made as a joke,
worth about ninety billion dollars" makes the title question sharper rather
than answering it; "the next buyer" arrives in sentence 4.

**Two beats:** `pool` (new this run, the long form's own) and a full-screen
`chapter`. The last three crypto Shorts ran checklist / chart / chapter,
replicate / chapter, bars / diagram / steps.

**Opener: `Counter`, the long form's own** - $90B, entering on "joke" and
landing on "ninety" in sentence 2. The first cut ran the redacted hook
`[one source]`; the user's note was that the revealed phrase did not fit the
idea, and to use the long form's opener (`shorts.md`, "A hidden word must be
worth revealing"). It opens on the long form's first shot too.

**Cold close**, held by `outro=`: "A meme coin's price is the next buyer."
answers the title question without re-asking it, so the last frame loops
into the first. **No disclaimer** (the long form carries it). **No financial
advice:** the Squid Game token is history with a date.

**Clips** are the long form's roster, each once here; the Doge coin and
Musk are the long form's Commons stills, credited in its description.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/what-are-memecoins.py
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
from video_automation.longform import thumb as T
from video_automation.longform.openers import Counter

SOURCE_POST = "what-are-memecoins"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
REAL = ROOT / "assets/crypto/memecoins"

# The long form's roster - screened there, see its header.
SMILE = V / "shiba-inu-dog/20378106.mp4"                       # 15s, a Shiba Inu grinning at the lens - the long form's first shot
CROWD = V / "crowd-holding-phones/8088612.mp4"                 # 29s, a crowd each on a phone
FEED = V / "scrolling-social-media-phone-night/6279142.mp4"    # 14s, a feed scrolled in two hands
TRADE = V / "crypto-app-phone-hands/35124446.mp4"              # 12s, a chart on a phone, no name or ticker
CASE = V / "stack-of-cash-dark/6266652.mp4"                    # 10s, a briefcase of cash, red light
ALONE = V / "person-checking-phone-worried-night/8376635.mp4"  # 20s, a phone's glow under a blanket
PHONE = V / "scrolling-social-media-phone-night/17586685.mp4"  # 12s, a hand on a phone in the dark

COIN = REAL / "dogecoin-coin-black.jpg"        # 6000x4000, a physical Dogecoin on black
MUSK = REAL / "elon-musk-2023.jpg"             # 2126x2834, Musk in 2023
SHIBA = STOCK / "photos/shiba-inu/16730750.jpg"   # the long form's thumbnail dog

BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly, under the hook.
    ("Where does a meme coin's price come from?",),

    # The long form's opening line: the Counter enters on "joke" and lands on
    # "ninety". A number that raises the stakes, not the answer - "the next
    # buyer" is held back to sentence 4.
    ("Dogecoin was made as a joke, and at its peak it was worth about ninety billion dollars.",),

    ("No company, no profits, no supply limit.",),

    ("So its price is whatever the next buyer will pay.",),

    # `Elon` phonemizes uh-LON; `Eelahn` is the name (musk-effect's fix).
    (("That is why one post from Elon Musk could move it.",
      "That is why one post from Eelahn Musk could move it."),),

    # The setup for the beat, in its own sentence.
    ("And the money you buy with sits in a pool.",),

    # The pool's own sentence: coins, money, the pull.
    ("Coins on one side.",
     "The money buyers paid on the other.",
     "Pull the money out, and the coins have nothing to sell into."),

    ("That is a rug pull.",),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("$3.4M. GONE IN MINUTES.",
      "In 2021, the Squid Game token's creators pulled about three point four million dollars, in minutes."),),

    # Cold close, held by `outro=`.
    ("A meme coin's price is the next buyer.",),
]

SHOTS = [
    Shot(clip=SMILE, clip_at=1.0, clip_ax=0.62),
    Shot(clip=CROWD, clip_at=1.0, clip_ax=0.50),
    # The coin shown whole, letterboxed into the blurred fill.
    Shot(image=COIN, aspect=6000 / 4000, zoom=1.06),
    Shot(clip=TRADE, clip_at=1.0, clip_ax=0.40),
    Shot(clip=FEED, clip_at=1.0, clip_ax=0.50, inset=(MUSK, "top", 0.50)),
    Shot(clip=PHONE, clip_at=1.0, clip_ax=0.40),
    Shot(graphic="pool", backdrop=BEATGROUND,
         payload=("THE COIN", "what you can buy",
                  "THE MONEY", "what buyers paid in",
                  "THE CREATOR", "nothing left to sell into",
                  "HOW A RUG PULL WORKS")),
    Shot(clip=CASE, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="chapter", payload=("$3.4M. GONE IN MINUTES.",)),
    Shot(clip=ALONE, clip_at=2.0, clip_ax=0.50),
]

GAPS = [0.50, 0.85, 0.60, 0.70, 0.60, 0.55, 1.40, 0.80, 1.10, 1.20]

# The long form's headline. The vertical cover forces phrase-shaped rows.
HEADLINE_V = "What are\nmeme\n[coins?]"


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's grinning Shiba Inu, cut to the frame's
    shape round the dog so the face sits in the top half, the headline on
    three rows over a dark ramp at the bottom, clear of the view count."""
    import numpy as np
    src = Image.open(SHIBA).convert("RGB")
    # A full-height cut at the frame's shape put the face behind the
    # headline; a wider cut scaled to the width keeps it in the top half.
    crop = src.crop((int(src.width * 0.25), 0, int(src.width * 0.75), src.height))
    crop = crop.resize((1080, int(crop.height * 1080 / crop.width)), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (0, 0, 0))
    im.paste(crop, (0, -60))
    a = np.zeros((1920, 1), np.float32)
    a[860:1260, 0] = np.linspace(0, 1.0, 400)
    a[1260:, 0] = 1.0
    ramp = Image.fromarray((np.repeat(a, 1080, 1) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ramp)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE_V, 220,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.30, leading=1.02, band="bottom",
                margin=int(1920 * 0.16) + 20, shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/what-are-memecoins-short.mp4"
    work = Path.home() / "Desktop/.what-are-memecoins-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The long form's opener, so the pair reads as one (the user's call
        # on the first cut, which ran the redacted hook `[one source]`).
        opener=Counter("$90B", "DOGECOIN AT ITS PEAK, MAY 2021",
                       at_word="ninety", enter_word="joke"),
        outro="A meme coin's price is the [next buyer].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/what-are-memecoins-short-thumb.jpg"))
    else:
        main()
