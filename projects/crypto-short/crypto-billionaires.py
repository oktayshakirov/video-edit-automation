"""How do crypto billionaires actually get rich? ~60s crypto short.

Source: crypto-wiki/content/posts/which-billionaires-own-crypto.mdx - the
same post as the `crypto-billionaires` long form, written in the same pass.

**Re-cut 2026-11-04 on the editor's note**: keep the opening, then walk
every figure the long form names, each with how they got rich, on the
reel ("the timeline animation with the cards"), and carry the long form's
`stake` graphic between the two reels. So: the owners' reel (Zhao,
Devasini, Ardoino, Armstrong - what each one owns), the stake (a fortune
is a share times a guess), the holders' and buyers' reel (Saylor, the
Winklevoss twins, Buterin, Musk, Dorsey, Durov, Trump, Satoshi), then the
cold close. One phrase per card, ~2s each (`beats.md`, reel in a Short).
The ranked-list standouts on the demand map win on faces and scale
(`demand/teardowns/richest-crypto-billionaires.md`).

**Sentence 2 overturns the title's assumption and keeps the answer back.**
"How do they get rich?" assumes coins; "the richest one is worth about a
hundred and ten billion dollars, and almost none of it is coins" overturns
it and opens "then what?". A how-question, not a yes/no one, and sentence
2's first words stay on the title's subject (`narration.md`, 2026-10-23).

**Opener: `Counter`** on $110B, landing on "hundred". The last four crypto
Shorts opened Stamp / Search / Stamp / Search.

**Cold close**, held by `outro=` in statement mode, on the clip the Short
opened on. **No disclaimer** (the long form carries it).

**Clips and portraits** are the long form's roster.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/crypto-billionaires.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Counter

SOURCE_POST = "which-billionaires-own-crypto"
DEMAND = ("'richest crypto billionaires' proven: Boomnix 'Top 5 wealthiest "
          "crypto billionaires' Short 519x, Top 10 Galaxy Short 8.3x, Data "
          "Face long 152x, Gravity 'Biggest Bitcoin Holders 2024' 7.1x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
PEOPLE = ROOT / "assets/crypto/billionaires"

# The long form's roster - screened there, see its header.
PHONE = V / "trading-app-phone-close-up-night/39494572.mp4"       # a hand with a phone of red candles - opens and closes
DESK = V / "stock-exchange-trading-screens-dark/38440687.mp4"     # a trading desk of monitors
SKYLINE = V / "skyscraper-office-lights-night/11589653.mp4"       # towers reflected in water
CALC = V / "calculator-hands-desk-dark/6266425.mp4"               # hands with cash by a calculator
MARINA = V / "luxury-yacht-night/37169294.mp4"                    # yachts moored at night
VITALIK = ROOT / "assets/crypto/vitalik-buterin/vitalik-techcrunch-wide.jpg"
MUSK = ROOT / "assets/crypto/musk/elon-musk-33377877458.jpg"
# The site's own Satoshi illustration - a hooded figure at an investigation board.
SATOSHI = _P.home() / "Coding/crypto-wiki/public/images/posts/satoshi-nakamoto.png"

VOICE = "mia"
MUSIC = music.track("night-drift")


def _bn(s: str) -> tuple:
    """The caption says Binance and USDT; the voice says "Bynanse" and
    spells U S D T."""
    return (s, s.replace("Binance", "Bynanse").replace("USDT", "U S D T"))


SENTENCES = [
    # The title question, plainly. The Counter enters after it.
    ("How do crypto billionaires actually get rich?",),

    # The reversal: not coins. Opens "then what?".
    ("The richest one is worth about a hundred and ten billion dollars, and almost none of it is coins.",),

    # The hinge into the owners' reel.
    ("They own the business, not the coin.",),

    # Reel one, the owners: one phrase per card.
    (_bn("Changpeng Zhao owns Binance, and its fee on every trade."),
     "Giancarlo Devasini owns almost half of Tether, and the interest it earns.",
     "Paolo Ardoino runs Tether and owns about a fifth.",
     "Brian Armstrong owns about a fifth of Coinbase."),

    # The hinge into the stake.
    ("And each fortune is a stake times a guess.",),

    # The stake: the company, two holders, the re-valuation.
    ("Forbes values Tether at two hundred billion.",
     "So Devasini's share is eighty-nine.",
     "Ardoino's, thirty-eight.",
     "At five hundred, both more than double."),

    # The hinge into the holders' reel.
    ("The famous names did it differently.",),

    # Reel two, the holders and buyers: one phrase per card.
    ("Michael Saylor made his company a bitcoin buyer.",
     "The Winklevoss twins bought at ten dollars.",
     "Vitalik Buterin co-founded Ethereum.",
     # espeak says ih-LAHN for "Elon"; "Eelon" reads EE-lən.
     ("Elon Musk's Tesla bought a billion and a half.",
      "Eelon Musk's Tesla bought a billion and a half."),
     "Jack Dorsey built Block around bitcoin.",
     "Pavel Durov bought thousands in 2013.",
     "Donald Trump called it a scam, and now has two billion from it.",
     "And Satoshi's million coins sit on no list."),

    # Cold close, held by `outro=`.
    ("Crypto's richest don't hold the coins. They own what everyone uses.",),
]

SHOTS = [
    Shot(clip=PHONE, clip_at=1.0, clip_ax=0.45),
    Shot(clip=DESK, clip_at=2.0, clip_ax=0.50),
    Shot(clip=SKYLINE, clip_at=0.5, clip_ax=0.50),
    Shot(graphic="reel",
         payload=([(PEOPLE / "cz-2022.jpg", "CHANGPENG ZHAO · BINANCE"),
                   (PEOPLE / "devasini.png", "GIANCARLO DEVASINI · TETHER"),
                   (PEOPLE / "ardoino.jpg", "PAOLO ARDOINO · TETHER"),
                   (PEOPLE / "armstrong.jpg", "BRIAN ARMSTRONG · COINBASE")], "")),
    Shot(clip=CALC, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="stake",
         payload=(("Tether", "issuer of USDT"),
                  [(200, "$200B", "Forbes' valuation"),
                   (500, "$500B", "if valued higher")],
                  [("Giancarlo Devasini", 0.45, "$89.3B"),
                   ("Paolo Ardoino", 0.19, "$38B")],
                  "A STAKE TIMES A GUESS")),
    Shot(clip=MARINA, clip_at=2.0, clip_ax=0.50),
    Shot(graphic="reel",
         payload=([(PEOPLE / "saylor.jpg", "MICHAEL SAYLOR · STRATEGY"),
                   (PEOPLE / "winklevoss.jpg", "THE WINKLEVOSS TWINS"),
                   (VITALIK, "VITALIK BUTERIN · ETHEREUM"),
                   (MUSK, "ELON MUSK · TESLA"),
                   (PEOPLE / "dorsey.jpg", "JACK DORSEY · BLOCK"),
                   (PEOPLE / "durov.jpg", "PAVEL DUROV · TELEGRAM"),
                   (PEOPLE / "trump.jpg", "DONALD TRUMP"),
                   (SATOSHI, "SATOSHI NAKAMOTO")], "")),
    Shot(clip=PHONE, clip_at=12.0, clip_ax=0.45),
]

GAPS = [1.00, 0.85, 0.50, 0.90, 0.50, 1.60, 0.50, 0.90, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/crypto-billionaires-short.mp4"
    work = Path.home() / "Desktop/.crypto-billionaires-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Counter("$110B", "THE RICHEST CRYPTO FORTUNE",
                       at_word="hundred", enter_word="richest"),
        outro="Crypto's richest don't hold the coins. "
              "They own what everyone uses.")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's AI picture, cut round the man,
    lifted into the lower frame with its own top continued upward
    (`bleed_portrait`), and the Short's question in three rows above it."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(PEOPLE / "cover-ai-cash-car.jpg").convert("RGB")
    w, h = src.size
    cw = int(h * 0.78)
    crop = src.crop((w - cw - 120, 0, w - 120, h))
    im = T.bleed_portrait(crop, y=1920 - int(crop.height * 1080 / crop.width),
                          fill="blur")
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "Who are\ncrypto's\n[richest?]", 190,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.30, leading=1.02, band="top",
                margin=int(1920 * 0.09), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/crypto-billionaires-short-thumb.jpg"))
    else:
        main()
