"""Richest crypto billionaires - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/which-billionaires-own-crypto.mdx
(published 2026-11-03).

**The angle.** "richest crypto billionaires" is a proven query: Data Face
"Top Crypto Billionaires 2025" 152x its median, Gravity "Biggest Bitcoin
Holders 2024" 7.1x (1.2M), two ranked-list Shorts standing out, while the
narrated "Top 10 richest" slideshows on the same page sit at 0.0-0.4x
(`demand/teardowns/richest-crypto-billionaires.md`). The standouts are
*ranked pictures of scale*; none of them says where the money comes from.
So this keeps the ranking and the faces, draws the scale, and adds the part
the sceptical viewer is missing: the biggest fortunes are stakes in the
businesses everyone else has to use, and every one of them is a stake
multiplied by a guess. The close echoes the open: almost none of it is
coins.

**Named people, so their real pictures** (`footage.md`, "Real people"):
Commons portraits in `assets/crypto/billionaires/` (CREDITS.md carries the
attribution, `Meta.credits` the line). Devasini has no free photograph; he
is a text card in the reel, which is also the line's point - "a name most
crypto users have never heard".

**Every figure is the article's, dated, and checked** (2026-11-04): Forbes
2026 list (March) CZ ~$110B, Devasini $89.3B, Ardoino $38B on a Tether
valuation of ~$200B; Forbes February 2026 Saylor $4.6B, each Winklevoss
$3.5B, Armstrong $7.5B; Arkham, May 2026, Buterin ~$536M known holdings;
Forbes March 2026 Trump ~$6.5B with ~$2.1B in crypto holdings and cash.
**Bloomberg's CZ figure is said as "under fifty billion"**: the article's
$45.1B snapshot could not be confirmed and Bloomberg's profile reads
$41.7B. CZ called the Forbes figure "not accurate" (March 2026, widely
reported). The $500B Tether valuation is the article's hypothetical and is
said as one. The article's dollar-cost-averaging advice is left out.

**Spoken around:** `Binance` phonemizes bye-NANCE, so the voice says
"Bynanse" (`projects/crypto.md`).

## The beats

Last three crypto long forms: seed-phrase (mnemonic / diagram / stat /
grid), binance-hack (sweep / bars / compare), prediction-markets (shares /
diagram / post / checklist).

* `reel` - the four fortunes crypto made, one card per name.
* `compare` - the two toll booths: an exchange, a stablecoin issuer.
* `stake` - **new, built for this video.** Tether as a block sized by its
  valuation, Devasini's and Ardoino's slices, then the block re-valued and
  both fortunes recomputed. The library could not draw a share staying the
  same while what it is a share of changes.
* `bars` - the holders against the owners, to scale.
* `stat` with Trump's official portrait in the picture column.

**Opener: `Search`** - the title is the query. The last three long forms
opened Stamp / Counter / hook.

**Footage: the owners' world** - trading screens, a trade on a phone, a
toll plaza at night, a city at night, a crash chart, cash counted by hand.
All fetched fresh 2026-11-04; verdicts in `footage.md`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/crypto-billionaires.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "which-billionaires-own-crypto"
DEMAND = ("'richest crypto billionaires' proven: Data Face 'Top Crypto "
          "Billionaires 2025' 152x (36k), Gravity 'Biggest Bitcoin Holders "
          "2024' 7.1x (1.2M), Top 10 Galaxy Short 8.3x, Boomnix Short 519x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
PEOPLE = ROOT / "assets/crypto/billionaires"
VITALIK = ROOT / "assets/crypto/vitalik-buterin/vitalik-techcrunch-wide.jpg"
MUSK = ROOT / "assets/crypto/musk/elon-musk-33377877458.jpg"
PRESS = ROOT / "assets/stock/press/billionaires"

# Fetched fresh for this pair, contact-sheeted at 15/50/85%, luma at
# 0.5s / middle / end.
PHONE = V / "trading-app-phone-close-up-night/39494572.mp4"        # 24s, L31, a hand with a phone of red candles - opens and closes
PHONEHANDS = V / "trading-app-phone-close-up-night/35886692.mp4"   # 31s, L32-36, two hands on a phone chart, red side light
PHONELAP = V / "trading-app-phone-close-up-night/8480231.mp4"      # 11s, L48-55, a phone held sideways over a laptop
DESK = V / "stock-exchange-trading-screens-dark/38440687.mp4"      # 25s, L47, a trading desk of monitors
SCREENS = V / "stock-exchange-trading-screens-dark/39212846.mp4"   # 33s, L17, walls of candles
WALL = V / "stock-exchange-trading-screens-dark/38498180.mp4"      # 39s, L12, monitors in a dark room
PURPLE = V / "stock-market-crash-screen-red/38557069.mp4"          # 13s, L21, purple-lit screens
CRASH2 = V / "stock-market-crash-screen-red/38859052.mp4"          # 30s, L17-21, a red chart, close
CRASH3 = V / "stock-market-crash-screen-red/39558578.mp4"          # 26s, L20-24, candles turning down
TOLL = V / "toll-booth-highway-night/10072842.mp4"                 # 13s, L55, a toll plaza at night from above
SKYLINE = V / "skyscraper-office-lights-night/11589653.mp4"        # 11s, L31, towers reflected in water
TOWERS = V / "skyscraper-office-lights-night/9921281.mp4"          # 11s, L42, towers at night
UPTOWER = V / "skyscraper-office-lights-night/2852289.mp4"         # 21s, L60-75, looking up a lit tower
NIGHTCITY = V / "private-office-city-view-night/17153904.mp4"      # 26s, L10, a city at night from high up
DENSE = V / "private-office-city-view-night/18569319.mp4"          # 28s, L40, a dense city at night
STAGE = V / "conference-stage-spotlight-speaker-dark/19197406.mp4" # 27s, L67-87, a keynote stage, out of focus
MARINA = V / "luxury-yacht-night/37169294.mp4"                     # 27s, L48, yachts moored at night
CASH = V / "hands-counting-dollar-bills-dark/4524511.mp4"          # 24s, L51-57, hands counting dollar bills on black
CALC = V / "calculator-hands-desk-dark/6266425.mp4"                # 10s, L54, hands with cash by a calculator
CODE = V / "old-computer-monitor-code-dark/34160292.mp4"           # 15s, L16, code on a dark monitor, red light
KEYS = V / "old-computer-monitor-code-dark/18382358.mp4"           # 16s, L37, hands over a keyboard of code
RAIN = V / "rain-on-window-night-close-up/15161525.mp4"            # 16s, L31, rain on glass, lights behind - the disclaimer

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"          # the noah test is full (projects/crypto.md)
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/which-billionaires-own-crypto"


def _bn(s: str) -> tuple:
    """The SRT says Binance and USDT; the voice says "Bynanse" and spells
    U S D T (espeak reads "USDT" as one word, `ʌst`)."""
    return (s, s.replace("Binance", "Bynanse").replace("USDT", "U S D T"))


SECTIONS = [
    # --- hook. No card. The Search opener types the query. -------------------
    Section(
        title="Richest crypto billionaires",
        card=False,
        sentences=[
            ("The richest person crypto has ever made is worth about a hundred and ten billion dollars.",),
            ("And almost none of it is coins.",),
            ("The biggest crypto fortunes were not made by buying early and waiting.",),
            ("They were made by owning the businesses everyone else has to use.",),
            ("So who are they, and why can one man be worth fifty billion, or a hundred and ten?",),
            ("Stay to the end, because one of the largest crypto fortunes of all appears on no list.",),
        ],
        shots=[
            Shot(clip=PHONE, clip_at=1.0),
            Shot(clip=WALL, clip_at=2.0),
            Shot(clip=SKYLINE, clip_at=0.5),
            Shot(clip=DESK, clip_at=2.0),
            Shot(clip=PHONEHANDS, clip_at=2.0),
            Shot(clip=NIGHTCITY, clip_at=2.0),
        ],
        gaps=[0.55, 0.90, 0.55, 0.85, 0.75, 0.90],
    ),

    # --- the owners ---------------------------------------------------------
    Section(
        title="Who got rich from crypto itself?",
        spoken_title="So who actually got rich from crypto itself?",
        kicker="THE OWNERS",
        sentences=[
            ("Start with four people crypto itself made rich.",),
            # The reel: one sentence per card, held with None.
            (_bn("Changpeng Zhao, who founded Binance, at about a hundred and ten billion dollars."),),
            ("Giancarlo Devasini, Tether's chairman, at eighty-nine billion.",),
            ("Paolo Ardoino, Tether's chief executive, at thirty-eight billion.",),
            ("And Coinbase's Brian Armstrong, at seven and a half billion.",),
        ],
        shots=[
            Shot(clip=STAGE, clip_at=2.0),
            Shot(graphic="reel", backdrop=BEATGROUND,
                 payload=([(PEOPLE / "cz-2022.jpg", "CHANGPENG ZHAO · BINANCE"),
                           (None, "GIANCARLO DEVASINI"),
                           (PEOPLE / "ardoino.jpg", "PAOLO ARDOINO · TETHER"),
                           (PEOPLE / "armstrong.jpg", "BRIAN ARMSTRONG · COINBASE")],
                          "FORBES ESTIMATES, 2026")),
            None,
            None,
            None,
        ],
        gaps=[0.55, 0.70, 0.70, 0.60, 0.90],
    ),

    # --- where the money comes from -------------------------------------------
    Section(
        title="Where does the money come from?",
        spoken_title="So where does that money actually come from?",
        kicker="THE TOLL BOOTHS",
        sentences=[
            ("They own the places everyone else has to pass through.",),
            # The compare: two heading chunks and six items, in column order.
            ("Take an exchange first.",
             "It takes a fee on every trade.",
             "Up or down, the fee is paid.",
             _bn("And Zhao owns about ninety percent of Binance."),
             "Now a stablecoin issuer.",
             _bn("Every USDT is backed by reserves."),
             "Tether keeps most of them in US Treasuries.",
             "And it keeps the interest, billions of dollars a year."),
            ("Owning the businesses has made far more ten-figure fortunes than holding the coins.",),
        ],
        shots=[
            Shot(clip=TOLL, clip_at=1.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("AN EXCHANGE",
                          ["A fee on every trade", "Paid in any market",
                           "Zhao owns about 90%"],
                          "STABLECOIN ISSUER",
                          ["Reserves behind every USDT", "Held in US Treasuries",
                           "Tether keeps the interest"],
                          True)),
            Shot(clip=CASH, clip_at=2.0),
        ],
        gaps=[0.70, 1.40, 0.90],
    ),

    # --- the guess: the turn, so the card gets the longer silence ------------
    Section(
        title="Is a fortune like that real?",
        spoken_title="But is a hundred and ten billion even a real number?",
        kicker="THE GUESS",
        card_gap=1.30,
        sentences=[
            (_bn("Binance and Tether are private companies, so nobody can look up what they are worth."),),
            ("So a fortune like this is a stake, multiplied by a guess.",),
            # The stake beat: the company, two holders, the re-valuation.
            ("Forbes valued Tether at around two hundred billion dollars.",
             "Devasini owns an estimated forty-five percent, so eighty-nine billion.",
             "Ardoino owns about nineteen, so thirty-eight.",
             "Value Tether at five hundred billion instead, and both fortunes more than double overnight."),
            ("Zhao is the same: Bloomberg's index has put him under fifty billion, while Forbes says a hundred and ten.",),
            (_bn("Neither tracker is lying. They just value Binance differently."),),
        ],
        shots=[
            Shot(clip=UPTOWER, clip_at=2.0),
            Shot(clip=CALC, clip_at=1.0),
            Shot(graphic="stake", backdrop=BEATGROUND,
                 payload=(("Tether", "issuer of USDT"),
                          [(200, "$200B", "Forbes' valuation"),
                           (500, "$500B", "if valued higher")],
                          [("Giancarlo Devasini", 0.45, "$89.3B"),
                           ("Paolo Ardoino", 0.19, "$38B")],
                          "A STAKE TIMES A GUESS")),
            Shot(image=PEOPLE / "cz-vietnam.jpg", zoom=1.06, name="Changpeng Zhao · Binance"),
            Shot(clip=PURPLE, clip_at=1.0,
                 note=("UNDER $50B", "Bloomberg's estimate, against Forbes' $110B")),
        ],
        gaps=[0.55, 0.75, 1.80, 0.70, 0.90],
    ),

    # --- the holders ----------------------------------------------------------
    Section(
        title="Did anyone get rich just holding?",
        spoken_title="So did anyone get rich just by holding?",
        kicker="THE HOLDERS",
        sentences=[
            ("A few did, by buying early and holding through every crash.",),
            ("Michael Saylor turned his software company, now called Strategy, into a machine for buying bitcoin.",),
            ("The Winklevoss twins bought bitcoin in 2012, when one coin cost around ten dollars.",),
            ("And Vitalik Buterin was called the youngest crypto billionaire in 2021, then gave much of it away.",),
            ("Now put the holders next to the owners.",),
            # The bars: one chunk per row.
            ("Zhao, a hundred and ten billion.",
             "Devasini, eighty-nine.",
             "Saylor, four point six.",
             "Each twin, three and a half.",
             "Buterin's known wallets, about half a billion."),
            ("The holders are rich. The owners are in another league.",),
        ],
        shots=[
            Shot(clip=CRASH2, clip_at=12.0),
            Shot(image=PEOPLE / "saylor.jpg", zoom=1.06, name="Michael Saylor · Strategy"),
            Shot(image=PEOPLE / "winklevoss.jpg", zoom=1.06, name="Cameron & Tyler Winklevoss"),
            Shot(image=VITALIK, zoom=1.06, name="Vitalik Buterin · Ethereum"),
            Shot(clip=SCREENS, clip_at=3.0),
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("Changpeng Zhao", 1.0, "$110B"),
                           ("Giancarlo Devasini", 89.3 / 110, "$89.3B"),
                           ("Michael Saylor", 4.6 / 110, "$4.6B"),
                           ("Each Winklevoss twin", 3.5 / 110, "$3.5B"),
                           ("Vitalik Buterin", 0.536 / 110, "~$0.5B")],
                          "ESTIMATED FORTUNES, 2026")),
            Shot(clip=MARINA, clip_at=2.0),
        ],
        gaps=[0.55, 0.60, 0.60, 0.75, 0.45, 1.30, 0.90],
    ),

    # --- the buyers ------------------------------------------------------------
    Section(
        title="What about the ones who bought in?",
        spoken_title="And what about the billionaires who simply bought in?",
        kicker="THE BUYERS",
        sentences=[
            ("For them, crypto is a side bet on a fortune built somewhere else.",),
            ("Tesla bought one and a half billion dollars of bitcoin in 2021, and sold most of it a year later.",),
            ("Next to Tesla and SpaceX, Elon Musk's crypto is a rounding error.",),
            ("Jack Dorsey rebuilt his payments company, Block, around bitcoin.",),
            ("Pavel Durov says he bought a few thousand bitcoin in 2013, at about seven hundred dollars each.",),
            ("And Donald Trump, who called bitcoin a scam in 2021, now holds about two billion dollars in crypto and cash.",),
            ("For them, a crash is a bad quarter. For a founder, it can be half a fortune.",),
        ],
        shots=[
            Shot(clip=DENSE, clip_at=2.0),
            # Tesla's and SpaceX's marks over both Musk lines - the second names them.
            Shot(image=MUSK, zoom=1.0, name="Elon Musk",
                 inset=(PRESS / "tesla-spacex-stack.png", "right", 0.16)),
            None,
            Shot(image=PEOPLE / "dorsey.jpg", zoom=1.06, name="Jack Dorsey · Block"),
            Shot(image=PEOPLE / "durov.jpg", zoom=1.06, name="Pavel Durov · Telegram"),
            Shot(graphic="stat", backdrop=BEATGROUND, picture=PEOPLE / "trump.jpg",
                 payload=("$2.1B", "IN CRYPTO AND CASH",
                          "of Donald Trump's ~$6.5B, by Forbes' count", False)),
            Shot(clip=CRASH3, clip_at=2.0),
        ],
        gaps=[0.55, 0.45, 0.70, 0.45, 0.55, 0.80, 0.90],
    ),

    # --- the one on no list: the promise from the hook --------------------------
    Section(
        title="Who is the billionaire on no list?",
        spoken_title="So who is the billionaire on no list?",
        kicker="THE UNNAMED",
        sentences=[
            ("Blockchain analysis of Bitcoin's first blocks suggests Satoshi Nakamoto mined roughly a million coins in 2009 and 2010.",),
            ("At almost any recent price, that would rank among the largest fortunes on Earth.",),
            ("Yet it appears on no list, because nobody can prove who holds the keys.",),
        ],
        shots=[
            Shot(clip=CODE, clip_at=1.0,
                 note=("~1,000,000 BTC", "mined in 2009-10, never moved")),
            Shot(clip=NIGHTCITY, clip_at=14.0),
            Shot(clip=KEYS, clip_at=2.0),
        ],
        gaps=[0.80, 0.60, 0.90],
    ),

    # --- close: the echo ---------------------------------------------------------
    Section(
        title="So who are crypto's billionaires?",
        spoken_title="So, who are crypto's billionaires?",
        kicker="THE ANSWER",
        sentences=[
            ("Mostly the people who own the exchanges and the stablecoins, not the people holding the coins.",),
            ("And every figure is a stake times a guess, with a date on it.",),
            ("Nothing in this video is financial advice.",),
            ("So the next time a headline says a billionaire owns crypto, will you ask which kind?",),
        ],
        shots=[
            Shot(clip=TOLL, clip_at=5.0),
            Shot(clip=CRASH2, clip_at=4.0),
            Shot(clip=RAIN, clip_at=2.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=PHONE, clip_at=12.0),
        ],
        gaps=[0.70, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="Richest Crypto Billionaires 2026: Where Their Money Really Comes From",
    hook="The richest person crypto has made is worth about $110 billion, and "
         "almost none of it is coins. Here are the crypto billionaires of "
         "2026, where each fortune really comes from, why one man can be "
         "worth $50 billion or $110 billion depending on who is counting, "
         "and the largest crypto fortune that appears on no list.",
    url=URL,
    summary="Who the richest crypto billionaires are in 2026 and where their "
            "money comes from: the founders crypto made rich - Changpeng Zhao "
            "(Binance, ~$110B), Giancarlo Devasini ($89.3B) and Paolo Ardoino "
            "($38B) of Tether, Brian Armstrong (Coinbase) - and why their "
            "fortunes come from owning an exchange or a stablecoin issuer, not "
            "from holding coins; why a private company's founder is worth "
            "whatever the company is guessed to be worth (Forbes against "
            "Bloomberg on CZ); the holders who did get rich holding - Michael "
            "Saylor, the Winklevoss twins, Vitalik Buterin - drawn to scale "
            "against the owners; the billionaires who bought in - Elon Musk, "
            "Jack Dorsey, Pavel Durov, Donald Trump; and Satoshi "
            "Nakamoto's untouched coins. Every figure is a dated estimate "
            "(Forbes 2026 unless stated). Nothing here is financial advice.",
    tags=["richest crypto billionaires", "crypto billionaires", "crypto billionaires 2026",
          "richest people in crypto", "which billionaires own crypto",
          "billionaires who own bitcoin", "changpeng zhao net worth",
          "cz net worth", "giancarlo devasini", "paolo ardoino", "tether",
          "michael saylor", "winklevoss twins", "satoshi nakamoto bitcoin",
          "forbes billionaires 2026"],
    cta=f"Every billionaire on the list, with dated figures and sources: {URL}",
    credits=["Nothing in this video is financial advice.",
             "Net worth figures are published estimates (Forbes, Bloomberg, "
             "Arkham), dated as stated, and change with the market.",
             "Photographs via Wikimedia Commons: Aevozer (CC BY-SA 4.0), "
             "Gage Skidmore (CC BY-SA 3.0), TechCrunch and John Phillips "
             "(CC BY 2.0), MicroStrategy (CC BY 2.0), cellanr (CC BY-SA 2.0), "
             "JD Lasica (CC BY 2.0), Daniel "
             "Oberhaus (CC BY 2.0); official White House portrait (public "
             "domain)."],
)

HEADLINE = "Who are\ncrypto's\n[richest?]"
COVER = PEOPLE / "cover-ai-cash-car.jpg"   # an AI image the editor supplied - no person, no credit


def thumbs(out: Path) -> Path:
    """The editor's AI picture - a man fanning cash in a car - with the
    question the list answers in three rows on the left. No real person on
    the cover (2026-11-04): the click is to find out who is on the list.
    The man stays whole and unshaded on the right; only the car interior
    behind the rows is darkened (`thumbnails.md`, ink by ground)."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    im = Image.open(COVER).convert("RGB")
    w, h = im.size
    im = im.crop((0, 0, w, int(w * 9 / 16))).resize((1280, 720), Image.LANCZOS)
    a = np.zeros((1, 1280), np.float32)
    a[0, :470] = 0.62
    a[0, 470:700] = np.linspace(0.62, 0.0, 230)
    shade = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, shade)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 190, int(600 / 1.38), 40, fill, ink,
                max_lines=3, leading=1.0, band="middle", margin=40,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/crypto-billionaires-long.mp4"
    work = Path.home() / "Desktop/.crypto-billionaires-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title is the query. Last three long forms opened
        # Stamp / Counter / hook.
        opener=Search("who are the richest crypto billionaires"),
        emphasis=["almost none of it is coins", "a stake, multiplied by a guess",
                  "another league", "no list"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=10.5, title_hold=5.4, title_style="glitch",
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/crypto-billionaires-long-thumb.jpg"))
    else:
        main()
