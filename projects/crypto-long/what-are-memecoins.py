"""What are meme coins and how do they work? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-are-memecoins.mdx.

**The angle.** Everyone has a confident take on meme coins - a joke, a
lottery ticket, a scam. The video's job is the mechanism under all three: a
meme coin has no company, no profits and usually no product, so its price is
only what the next buyer pays, and the next buyer only arrives while people
are talking. From there the money: whoever creates a coin decides who holds
it on day one, and the buyers' money sits in a pool the creator may still
control - which is what a rug pull removes. The mirror is the article's own
DYOR list, cut to the four things anyone can look up. The close echoes the
open: made as a joke, priced by a crowd.

**No financial advice.** Nothing here rates a coin, names a price level or a
direction, or says to buy or sell anything. Dogecoin's peak and the Squid
Game token's collapse are history with dates. The four checks say who could
take the money, never whether a coin will rise.

**Figures, each said with its date.** Dogecoin launched December 2013 by
Billy Markus and Jackson Palmer, after the Doge meme (Kabosu, a Shiba Inu).
Peak market value about $90B, May 2021 (sources give $85-93B). 10,000 DOGE
per one-minute block since 2015, no cap - about 5 billion a year. Bitcoin's
cap 21 million. Musk hosted SNL on 8 May 2021 and DOGE fell sharply during
the broadcast (about a third, widely reported). Markus sold his DOGE in 2015
"for about the price of a used Honda Civic" (his words, Benzinga 2021). The
Squid Game token (SQUID, BNB Chain, Oct-Nov 2021): a sell block in its
contract, an estimated $3.38M drained from its pool on 1 November 2021, the
price near zero within minutes (Gizmodo, BBC, Wikipedia).

**Respelled:** "Shiba Inu" phonemizes in-YOO, "Kabosu" ka-BAH-soo and
"Elon" uh-LON, so the spoken halves read "Shiba Eenoo", "Kahbosoo" and
"Eelahn". "meme coin" is two
words (`memecoin` phonemizes MEM-i-coin).

## The beats

Last three crypto long forms: gta-6-crypto (timeline / quote / checklist /
diagram / chart), decentralized-ai (replicate / gauge / compare / grid /
checklist), bear-market-in-crypto (bars / diagram / chart / steps / stat).
`diagram` and `chart` were each in two of three, so neither is here.

* `compare` - Bitcoin against Dogecoin: where each began, its supply, what
  its price rests on. The article's own table, cut to three rows.
* `stat` - 10,000 new Dogecoins a minute, the coin in the picture column.
* `steps` - how a meme coin is made today: four steps, minutes.
* `pool` - **new, built for this video.** The coin on one side of a trading
  pool, the buyers' money on the other, and the money side drained out to
  the creator while the coins go grey. A rug pull's noun is a liquidity pool
  and nothing in the library could draw one.
* `grid` - the four things anyone can check.

**Opener: `Counter`.** Last three long forms opened Stamp / hook / Search.
The pattern interrupt is a number - a joke worth about $90B - so it lands on
"ninety" in sentence 1 (`longform.md`, a 16:9 hook word may).

**Footage: the act, in the subject's world.** Real things first: a physical
Dogecoin on black, Kabosu herself (the real Doge dog), Musk at the line that
names him - all Commons, credited (`assets/crypto/memecoins/CREDITS.md`).
Shiba Inu dogs for Dogecoin; phones, feeds and a crowd on screens for
attention; code on a laptop for "create the token"; a TV studio floor for
SNL; an empty wallet, a briefcase of cash, a padlock for the pool. Every clip
fresh; verdicts in `footage.md`. The one abstract is dark water under the
disclaimer.

**Thumbnail:** a grinning Shiba Inu (Pexels 16730750) set right, the title's
question on the left. The first build used the Dogecoin coin; the user's note
was that it is boring and does not make anyone click - a cute dog does.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/what-are-memecoins.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Counter

SOURCE_POST = "what-are-memecoins"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
REAL = ROOT / "assets/crypto/memecoins"

# Every clip fetched fresh for this pair and looked at on a labelled
# three-frame contact sheet (15/50/85% of its length).
SMILE = V / "shiba-inu-dog/20378106.mp4"                       # 15s, L119, a Shiba Inu grinning at the lens - the Doge
LIE = V / "shiba-inu-dog/20660963.mp4"                         # 12s, L113, a Shiba Inu lying down, warm
WALK = V / "shiba-inu-dog/16436887.mp4"                        # 11s, L99,  a Shiba Inu on a lead, trotting
FEED = V / "scrolling-social-media-phone-night/6279142.mp4"    # 14s, L51,  a feed scrolled in two hands, lamp behind
PHONE = V / "scrolling-social-media-phone-night/17586685.mp4"  # 12s, L43,  a hand on a phone in the dark, screen away
GLOW = V / "laughing-at-phone-dark/5281602.mp4"                # 12s, L30,  a face lit by a screen, on a call
CROWD = V / "crowd-holding-phones/8088612.mp4"                 # 29s, L39,  a crowd each on a phone
NIGHT = V / "crowd-holding-phones/38471324.mp4"                # 15s, L36,  a night square of raised phones, mono
CODE = V / "typing-code-laptop-night/13522186.mp4"             # 13s, L35,  code on a laptop in the dark
TYPE = V / "typing-code-laptop-night/5495781.mp4"              # 21s, L25,  hands typing, a laptop's glow
SCREEN = V / "programmer-monitor-code-dark/34160292.mp4"       # 14s, L16,  a monitor of code, red light
TRADE = V / "crypto-app-phone-hands/35124446.mp4"              # 12s, L42,  a chart on a phone, no name or ticker - 35886692 shows AAPL
STUDIO = V / "television-studio-audience/14367163.mp4"         # 9s,  L39,  a TV studio floor, crew in silhouette
LOCK = V / "padlock-chain-dark/4889026.mp4"                    # 13s, L43,  an old padlock, close
WALLET = V / "hands-empty-wallet/16747050.mp4"                 # 11s, L50,  hands opening an empty wallet
CASE = V / "stack-of-cash-dark/6266652.mp4"                    # 10s, L56,  a briefcase of cash, red light
STUCK = V / "person-checking-phone-worried-night/7280528.mp4"  # 18s, L42,  head in hand over a phone at night
ALONE = V / "person-checking-phone-worried-night/8376635.mp4"  # 20s, L66,  a phone's glow under a blanket
WATER = V / "dark-ocean-waves-night/5678004.mp4"               # 18s, L29,  dark water - the one abstract

# Real things, Wikimedia Commons, credited below.
COIN = REAL / "dogecoin-coin-black.jpg"        # 6000x4000, L61, a physical Dogecoin on black - CC BY-SA 4.0
KABOSU = REAL / "kabosu-2023.jpg"              # 1037x1702, L104, Kabosu and Atsuko Sato, 2023 - CC0
MUSK = REAL / "elon-musk-2023.jpg"             # 2126x2834, L131, Musk in 2023 - CC BY 2.0
# Both thumbnails: a grinning Shiba Inu, tongue out, on dark green. Pexels.
SHIBA = STOCK / "photos/shiba-inu/16730750.jpg"   # 7143x4762, L53, the dog at ~0.36-0.64 of the width

from video_automation.longform.overlay import ticker_card  # noqa: E402
# A dozen copycat contracts carry the name, so no logo - a drawn card.
CARD_SQUID = ticker_card("squid", "Squid Game token, Nov 2021",
                         "unrelated to Netflix", CRYPTO,
                         REAL / "cards/squid.png")

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-are-memecoins"


SECTIONS = [
    # --- hook. No card. The Counter lands on "ninety" in sentence 1. -------
    Section(
        title="Meme coins",
        card=False,
        sentences=[
            ("Dogecoin was made as a joke, and at its peak, it was worth about ninety billion dollars.",),
            ("It has no company behind it, no profits,",
             "and no limit on how many coins can exist."),
            ("Thousands of coins have copied it since.",),
            ("So what is a meme coin, and where does its price actually come from?",),
            ("Stay to the end,",
             "and you will know how the money behind one can vanish in minutes,",
             "and what to check first."),
        ],
        shots=[
            Shot(clip=SMILE, clip_at=1.0),
            Shot(image=COIN, zoom=1.10, pan=(0.02, 0.0)),
            Shot(clip=PHONE, clip_at=9.0),
            Shot(clip=CROWD, clip_at=1.0),
            None,
        ],
        gaps=[0.85, 0.70, 0.60, 0.90, 0.90],
    ),

    # --- what a meme coin is -------------------------------------------------
    Section(
        title="What makes a coin a meme coin?",
        spoken_title="So what makes a coin a meme coin?",
        kicker="THE JOKE",
        sentences=[
            ("In December 2013, two software engineers,",
             "Billy Markus and Jackson Palmer, launched Dogecoin."),
            # "Inu" phonemizes in-YOO and "Kabosu" ka-BAH-soo: respelled.
            (("They named it after a viral meme, a Shiba Inu called Kabosu,",
              "They named it after a viral meme, a Shiba Eenoo called Kahbosoo,"),
             "and they meant it as a joke about crypto hype."),
            ("A crowd formed around the joke, and the joke became the product.",),
            ("That is a meme coin.",
             "A coin whose value is its meme and its crowd, not anything it does."),
            (("Shiba Inu, Pepe, and thousands of others followed the same recipe.",
              "Shiba Eenoo, Pepe, and thousands of others followed the same recipe."),),
            # the compare's own sentence: one chunk per reveal, headings included.
            ("Take Bitcoin.",
             "It started as a research paper.",
             "It stops at twenty-one million coins.",
             "And its price rests on adoption.",
             "Now compare that with Dogecoin.",
             "It started as a joke.",
             "It has no supply limit at all.",
             "And its price rests on attention."),
            ("And how far does no limit go?",),
            # the stat's own sentence.
            ("Ten thousand new Dogecoins are created every minute, forever.",),
        ],
        shots=[
            Shot(clip=CODE, clip_at=1.0),
            Shot(clip=FEED, clip_at=1.0, inset=(KABOSU, "right", 0.30)),
            Shot(clip=WALK, clip_at=0.5),
            None,
            Shot(clip=GLOW, clip_at=1.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("BITCOIN",
                          ["A research paper", "Capped at 21 million",
                           "Rests on adoption"],
                          "DOGECOIN",
                          ["A joke", "No cap at all", "Rests on attention"],
                          True)),
            Shot(clip=SCREEN, clip_at=2.0),
            Shot(graphic="stat", backdrop=BEATGROUND, picture=COIN,
                 payload=("10,000", "NEW DOGECOINS A MINUTE",
                          "about five billion a year, with no end", False)),
        ],
        gaps=[0.55, 0.70, 0.60, 0.80, 0.70, 1.20, 0.70, 0.90],
    ),

    # --- where the price comes from ----------------------------------------
    Section(
        title="Where does a meme coin's price come from?",
        spoken_title="So where does a meme coin's price come from?",
        kicker="THE PRICE",
        sentences=[
            ("Not from profits. A meme coin has none to share.",),
            ("Not from a product. Most launch with nothing to use.",),
            ("So a meme coin is worth exactly what the next buyer will pay for it.",),
            ("And the next buyer only shows up while people are talking about it.",),
            # `Elon` phonemizes uh-LON; `Eelahn` is the name (musk-effect's fix).
            (("In 2021, Elon Musk's posts about Dogecoin moved its price again and again,",
              "In 2021, Eelahn Musk's posts about Dogecoin moved its price again and again,"),
             "and fans started calling him the Dogefather."),
            ("That May, he hosted Saturday Night Live, and millions tuned in.",),
            ("But Dogecoin fell sharply while the show was still on air.",),
            ("Attention moves a meme coin both ways, and nobody controls which.",),
        ],
        shots=[
            Shot(clip=ALONE, clip_at=2.0),
            Shot(clip=TYPE, clip_at=2.0),
            Shot(clip=NIGHT, clip_at=1.0),
            None,
            Shot(clip=PHONE, clip_at=0.5, inset=(MUSK, "right", 0.30)),
            Shot(clip=STUDIO, clip_at=0.5),
            Shot(clip=LIE, clip_at=1.0),
            None,
        ],
        gaps=[0.55, 0.70, 0.80, 0.85, 0.60, 0.85, 0.70, 0.90],
    ),

    # --- why there are so many ---------------------------------------------
    Section(
        title="Why are there so many meme coins?",
        spoken_title="So why are there so many meme coins?",
        kicker="THE FACTORY",
        sentences=[
            ("Because making one now takes four steps, and a few minutes.",),
            # the steps' own sentence: one chunk per node.
            ("Pick a joke.",
             "Create the token.",
             "Put it in a trading pool, next to some real money.",
             "Then post it everywhere."),
            ("Whoever creates the coin decides who holds it on day one.",),
            ("Dogecoin's creators kept no hidden pile.",
             "Billy Markus says he sold all of his coins in 2015,",
             "for about the price of a used Honda Civic."),
            ("Plenty of newer coins start the other way round,",
             "with the creator and their friends holding most of the supply",
             "before anyone else can buy."),
            ("Then every coin they sell is paid for by someone who arrived later.",),
        ],
        shots=[
            Shot(clip=CODE, clip_at=7.0),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 payload=(["Pick a joke", "Create the token",
                           "Pair it with money in a pool",
                           "Post it everywhere"],
                          "HOW A MEME COIN IS MADE")),
            Shot(clip=TYPE, clip_at=12.0),
            Shot(clip=WALLET, clip_at=1.0),
            Shot(clip=SCREEN, clip_at=5.0),
            Shot(clip=CROWD, clip_at=16.0),
        ],
        gaps=[0.70, 1.30, 0.70, 0.80, 0.60, 0.90],
    ),

    # --- the twist: where the money sits, and how it goes -------------------
    # The turning point, so the card gets the longer silence.
    Section(
        title="How does a rug pull work?",
        spoken_title="So how does a rug pull actually work?",
        kicker="THE PULL",
        card_gap=1.30,
        sentences=[
            ("Buying a meme coin usually means trading with a pool, not with a person.",),
            # the pool's own sentence: coins, money, the pull.
            ("On one side of the pool sit the coins.",
             "On the other, the real money that buyers paid in.",
             "Pull the money side out, and every coin left has nothing to sell into."),
            ("That is a rug pull.",),
            ("In 2021, a token named after the show Squid Game climbed for days.",),
            ("But its buyers could not sell. One line in its code blocked them.",),
            ("On November first, its creators pulled the pool,",
             "an estimated three point four million dollars,",
             "and the price fell to almost zero within minutes."),
            ("A rug pull needs no hack. Only a creator who still controls the pool.",),
        ],
        shots=[
            Shot(clip=TRADE, clip_at=2.0),
            Shot(graphic="pool", backdrop=BEATGROUND,
                 payload=("THE COIN", "what you can buy",
                          "THE MONEY", "what buyers paid in",
                          "THE CREATOR", "nothing left to sell into",
                          "HOW A RUG PULL WORKS")),
            None,
            Shot(clip=FEED, clip_at=7.0, inset=(CARD_SQUID, "right", 0.36)),
            Shot(clip=STUCK, clip_at=2.0),
            Shot(clip=CASE, clip_at=0.5,
                 note=("~$3.38M", "pulled from its pool, 1 Nov 2021, est.")),
            Shot(clip=LOCK, clip_at=1.0),
        ],
        gaps=[0.70, 2.10, 0.90, 0.55, 0.80, 0.80, 0.90],
    ),

    # --- the mirror: what you can look up -----------------------------------
    Section(
        title="What can you actually check?",
        spoken_title="So what can you actually check?",
        kicker="THE CHECK",
        sentences=[
            ("Nothing tells you where a meme coin's price goes next.",),
            ("But four things tell you who could take the money.",),
            # the grid's own sentence: one chunk per card.
            ("Who made it, and are they named?",
             "Who holds the supply, and how much of it?",
             "Is the pool locked, so nobody can pull it?",
             "And has the code been checked by an outside firm?"),
            ("All four are public, on the blockchain or the project's own pages,",
             "if you look."),
        ],
        shots=[
            Shot(clip=GLOW, clip_at=7.0),
            Shot(clip=NIGHT, clip_at=8.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("Who made it", "a named team, or nobody", "\U0001F464"),
                           ("Who holds the supply", "a few wallets, or many", "\U0001FA99"),
                           ("Is the pool locked", "or can the creator pull it", "\U0001F512"),
                           ("Was the code audited", "by an outside firm", "\U0001F50D")],
                          "FOUR THINGS ANYONE CAN CHECK")),
            Shot(clip=ALONE, clip_at=12.0),
        ],
        gaps=[0.85, 0.70, 1.30, 0.90],
    ),

    # --- close: the echo -----------------------------------------------------
    Section(
        title="So what is a meme coin?",
        spoken_title="So, what is a meme coin, really?",
        kicker="THE ANSWER",
        sentences=[
            ("A coin whose only product is attention.",),
            ("Dogecoin was made as a joke.",
             "Every meme coin since is priced by a crowd,",
             "and the money stays only as long as the crowd does."),
            ("Nothing in this video is financial advice.",),
            ("So, the next time a meme coin is all over your feed,",
             "would you check who controls its pool?"),
        ],
        shots=[
            Shot(clip=SMILE, clip_at=8.0),
            Shot(image=COIN, zoom=1.08, pan=(-0.02, 0.0)),
            Shot(clip=WATER, clip_at=4.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=STUCK, clip_at=9.0),
        ],
        gaps=[0.85, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Are Meme Coins and How Do They Work?",
    hook="Dogecoin was made as a joke, and at its peak it was worth about "
         "$90 billion. Here is what a meme coin actually is, where its price "
         "comes from, why there are thousands of them, how a rug pull drains "
         "the money behind one in minutes, and the four things anyone can "
         "check.",
    url=URL,
    summary="What meme coins are and how they work: Dogecoin, launched in "
            "December 2013 by Billy Markus and Jackson Palmer as a joke about "
            "crypto hype and named after the Doge meme of Kabosu the Shiba "
            "Inu; how a meme coin differs from Bitcoin (a joke instead of a "
            "research paper, no supply cap - 10,000 new Dogecoins a minute - "
            "and a price that rests on attention); why its price is only "
            "what the next buyer pays, and how Elon Musk's posts and his May "
            "2021 Saturday Night Live appearance moved Dogecoin both ways; "
            "how a meme coin is made in minutes and why who holds the supply "
            "on day one matters; how a rug pull works, with the trading pool "
            "drawn, and the 2021 Squid Game token, whose creators pulled an "
            "estimated $3.38 million; and four things anyone can check - the "
            "team, the supply, whether the pool is locked, and an audit. "
            "Nothing here is financial advice.",
    tags=["what are meme coins", "meme coins explained", "how do meme coins work",
          "what is a meme coin", "dogecoin explained", "meme coin rug pull",
          "what is a rug pull", "liquidity pool rug pull", "squid game token",
          "shiba inu coin", "pepe coin", "meme coins for beginners"],
    cta=f"The full guide to meme coins: {URL}",
    credits=["Photographs: Dogecoin coin by Cyril Ernst (CC BY-SA 4.0); Elon "
             "Musk by UK Government (CC BY 2.0); Kabosu by Asanagi (CC0); via "
             "Wikimedia Commons.",
             "Nothing in this video is financial advice."],
)

# The title's own question, on the black left of the coin.
HEADLINE = "What are\nmeme\n[coins?]"


def thumbs(out: Path) -> Path:
    """The grinning Shiba Inu, cropped onto the dog and set against the right
    edge, with the title's question in three rows on the black at the left.
    A 200px ramp blends the photo into the black, clear of the dog."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(SHIBA).convert("RGB")
    # The dog sits at ~0.36-0.64 of the width, ears near the top.
    crop = src.crop((int(src.width * 0.15), 0,
                     int(src.width * 0.75), src.height))
    pw = int(720 * crop.width / crop.height)
    crop = crop.resize((pw, 720), Image.LANCZOS)
    im = Image.new("RGB", (1280, 720), (0, 0, 0))
    x = 1280 - pw
    im.paste(crop, (x, 0))
    a = np.zeros((1, 1280), np.float32)
    a[0, :x] = 1.0
    a[0, x:x + 200] = np.linspace(1.0, 0.0, 200)
    mask = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, mask)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 130, 520, 50, fill, ink, max_lines=3,
                leading=1.02, band="middle", margin=40, shadow=11, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/what-are-memecoins-long.mp4"
    work = Path.home() / "Desktop/.what-are-memecoins-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # A number as the pattern interrupt, landing in sentence 1. Last
        # three long forms opened Stamp / hook / Search.
        # Low on the frame: at the default 0.26 it covered the dog's eyes.
        opener=Counter("$90B", "DOGECOIN AT ITS PEAK, MAY 2021",
                       at_word="ninety", centre_y=0.74),
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/what-are-memecoins-long-thumb.jpg"))
    else:
        main()
