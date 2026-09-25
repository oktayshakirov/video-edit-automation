"""What is a crypto whale - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-a-crypto-whale.mdx.

**The angle, and the video it deliberately avoids.** `bitcoin-price-long` and
its Short already argue that a whale can move the market and still cannot
choose where it lands - the thin order book, the coins that never move,
exchange flows as the thing to watch instead. That covers the article's
"How Whales Move Markets" section completely. So this video takes the section
that one never opened: **the taxonomy**. Five kinds of holder sit at whale
scale, four of them are spending their own money, and the fifth - the
exchange or custodian - is holding everybody else's. That is why the biggest
wallets on any chain are custodial, and why a whale alert usually means less
than the feed implies.

**No financial advice.** It describes what a wallet is and what a transfer
can and cannot tell you. It names no coin to buy, no level, no direction, and
no exchange as safe or unsafe - the custody point is made about exchanges as
a category, which is the article's own framing.

**Every figure is structural**, so the video cannot date: the thousand-coin
and ten-thousand-coin thresholds and the 21,000,000 cap are the article's,
and the one dated number (19.7M mined) is spoken with its year attached. No
corporate treasury figure is used - those move every quarter.

## The beats

Last three crypto long-forms: crypto-scams (compare / grid / quote / diagram /
checklist), satoshi (quote / steps / split / checklist / stat), vitalik
(compare / grid / quote / stat / steps). `quote` is in all three and is
skipped here.

* `grid` - what counts as a whale in three different markets
* `checklist` - the five kinds of holder, judged on whether the coins are
  their own. The single cross is the video's thesis, and the narration names
  it in words ("four of those are spending their own money, the fifth is
  holding yours") so the axis is never left to be inferred.
* `split` - one custodial address divided into customer claims
* `compare` - coins moving onto an exchange against coins moving off one,
  three readings each, none of them certain

**Footage.** Fetched and screened for this pair; four cache clips that passed
the luma box were cut on the labelled contact sheet (a "safe deposit box"
folder that is a delivery van, a "storage locker" folder that is a hooded
figure against a pink wall, green fog, and the hacker trope). **Nothing in
the cut shows a live price, chart, ticker or broker name** - the two closest
candidates, `woman-trader-desk-dark-office-night` and
`spreadsheet-rows-screen-dark-night`, are both a lit candlestick chart with
a broker's name burned into it.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/crypto-whale.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "what-is-a-crypto-whale"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Luma/saturation range across the whole clip, then checked on a contact
# sheet. Durations matter: cast the long clips under the paragraphs and the
# short ones under the one-line sentences.
FEED = V / "thumb-scrolling-phone-feed-dark/38410500.mp4"                 # 30s, L32-40 S19-23, a thumb scrolling a feed
WINDOWS = V / "office-building-windows-night-dark/17499154.mp4"           # 16s, L26 S9, apartment blocks, many lit windows
WALLET = V / "smartphone-crypto-wallet-hand-dark/7534328.mp4"             # 16s, L37-40 S14-15, hands holding a lit phone
ALONE = V / "person-alone-laptop-dark-room-night/34771069.mp4"            # 8s,  L20-24 S3-4, hands on a laptop in the dark
DEAL = V / "hands-shaking-silhouette-dark-deal/6101696.mp4"               # 17s, L28-36 S3-7, two suited figures shaking hands
SUBWAY = V / "subway-train-passengers-phones-dark/36111567.mp4"           # 15s, L18-21 S10-12, a lit train at a platform
TUNNEL = V / "crowd-silhouettes-walking-tunnel-dark/35186847.mp4"         # 14s, L28-33 S6-7, silhouettes leaving an underpass
LEDGER = V / "digital-ledger-blocks-chain-dark/34127877.mp4"              # 20s, L13-15 S5, a tunnel of numerals - the one abstract
OCEAN = V / "deep-ocean-underwater-dark/5678004.mp4"                      # 17s, L29-31 S2, dark open water
RIPPLE = V / "calm-dark-water-ripple-slow-night/16392053.mp4"             # 22s, L29-51 S11-13, a ripple spreading on dark water
WARE = V / "warehouse-shelves-dark-night/19217894.mp4"                    # 10s, L23-30 S3, an empty warehouse corridor
CARGO = V / "cargo-ship-containers-night-dark/37791811.mp4"               # 6s,  L31 S14, a container port at night

THUMB = ROOT / "assets/crypto/whale/nyc-skyscrapers.jpg"                  # Pexels 15836295, Adrien Daurenjou, 6000x4000
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-is-a-crypto-whale"


SECTIONS = [
    # --- hook. No card, and the reversal is sentence one. -------------------
    # The pattern interrupt is a fact, not a scene: the measured curve on this
    # format drops ~20 points at the end of sentence one, so the surprising
    # thing goes there and the setup follows it.
    Section(
        title="The biggest wallets are not people",
        card=False,
        sentences=[
            ("The biggest Bitcoin wallets on earth do not belong to people.",),
            ("They belong to exchanges.",
             "And almost every coin inside them belongs to somebody else."),
            ("A crypto whale is a holder big enough to move a market on its own.",),
            ("But a wallet never tells you who is behind it,",
             "or whether the coins in it are even theirs to spend."),
            ("Stay to the end,",
             "and you will know how to read a whale alert instead of reacting to one."),
        ],
        shots=[
            Shot(clip=WINDOWS, clip_at=1.0),
            None,
            Shot(clip=OCEAN, clip_at=1.0),
            Shot(clip=WALLET, clip_at=1.0),
            Shot(clip=FEED, clip_at=1.0),
        ],
        gaps=[0.95, 0.75, 0.80, 0.70, 0.85],
    ),

    # --- what counts ---------------------------------------------------------
    Section(
        title="What counts as a whale?",
        spoken_title="So what actually counts as a whale?",
        sentences=[
            ("There is no official line.",
             "The word is relative to the supply and to how much of it trades."),
            # the grid's own sentence - one chunk per card.
            ("In Bitcoin, watchers start using the word at a thousand coins.",
             "In Ethereum, the number people reach for is ten thousand.",
             "In a small token with a thin market, a fraction of one percent is enough."),
            ("Twenty-one million bitcoin will ever exist,",
             "and about nineteen point seven million had been mined by twenty twenty-four."),
            ("So a thousand coins is a rounding error against the supply,",
             "and still more than a thin market can absorb at once."),
        ],
        shots=[
            Shot(clip=RIPPLE, clip_at=1.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("Bitcoin", "a whale from 1,000 coins"),
                           ("Ethereum", "the line sits near 10,000"),
                           ("A small token", "a fraction of one percent")],
                          "THE WORD IS RELATIVE")),
            Shot(clip=LEDGER, clip_at=1.0),
            Shot(clip=ALONE, clip_at=0.5),
        ],
        gaps=[0.70, 1.30, 0.75, 0.90],
    ),

    # --- who is behind it ----------------------------------------------------
    Section(
        title="Who is behind a whale wallet?",
        spoken_title="So who is actually behind one of these wallets?",
        sentences=[
            ("Size tells you nothing about intent.",),
            ("There are five kinds of holder at this scale,",
             "and only one of them is the lone trader people picture."),
            # the checklist's own sentence - one chunk per item, and the
            # question is asked at the end of the sentence before it.
            ("An early individual holder.",
             "A company holding coins as a treasury.",
             "A fund, or a market maker.",
             "A foundation, or a protocol treasury.",
             "And an exchange, or a custodian."),
            ("Four of those are spending their own money.",
             "The fifth is holding yours."),
        ],
        shots=[
            Shot(clip=DEAL, clip_at=2.0),
            Shot(clip=SUBWAY, clip_at=4.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("An individual holder", True),
                           ("A company treasury", True),
                           ("A fund or market maker", True),
                           ("A foundation treasury", True),
                           ("An exchange or custodian", False)],
                          "ARE THE COINS THEIR OWN?")),
            Shot(clip=TUNNEL, clip_at=1.0),
        ],
        gaps=[0.80, 0.70, 2.40, 0.95],
    ),

    # --- the custodian -------------------------------------------------------
    Section(
        title="Whose coins is an exchange holding?",
        spoken_title="So whose coins is an exchange actually holding?",
        sentences=[
            ("When you leave crypto on an exchange, the exchange holds the keys.",),
            ("Your balance is a number in its database.",
             "The coins themselves sit in wallets it controls."),
            # the split's own sentence: the whole first, the division second.
            ("So one address can hold more bitcoin than almost anybody alive,",
             "and every coin in it is a claim somebody else has on that company."),
            ("Which is why the biggest wallets on any chain are usually custodians.",
             "They are not investors. They are warehouses."),
        ],
        shots=[
            Shot(clip=CARGO, clip_at=0.5),
            Shot(clip=WALLET, clip_at=6.0),
            Shot(graphic="split", backdrop=BEATGROUND,
                 payload=("ONE ADDRESS", "past every whale threshold",
                          "CUSTOMER CLAIMS", "none of the coins are its own",
                          "WHOSE COINS ARE THESE?")),
            Shot(clip=WARE, clip_at=1.0),
        ],
        gaps=[0.85, 0.70, 1.20, 0.90],
    ),

    # --- reading a transfer --------------------------------------------------
    Section(
        title="Does a big wallet mean a big move?",
        spoken_title="But does a big wallet mean a big move?",
        sentences=[
            ("A whale alert fires whenever a large transfer hits the chain.",),
            ("What it cannot tell you is why.",),
            # the compare's own sentence - heading, three items, heading, three.
            ("Take coins moving onto an exchange.",
             "Somebody may be getting ready to sell.",
             "A fund may be rebalancing.",
             "Or a custodian may be moving its own inventory.",
             "Now compare that with coins moving off one.",
             "Somebody may be going to cold storage.",
             "A custodian may be topping up its reserves.",
             "Or it may mean nothing at all."),
            ("The chain records the movement.",
             "It never records the reason."),
        ],
        shots=[
            Shot(clip=FEED, clip_at=12.0),
            Shot(clip=TUNNEL, clip_at=6.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("COINS MOVING IN",
                          ["Getting ready to sell",
                           "A fund rebalancing",
                           "Moving its own inventory"],
                          "COINS MOVING OUT",
                          ["Going to cold storage",
                           "Topping up reserves",
                           "Nothing at all"],
                          True)),
            Shot(clip=LEDGER, clip_at=10.0),
        ],
        gaps=[0.70, 0.90, 1.30, 0.95],
    ),

    # --- close ---------------------------------------------------------------
    Section(
        title="So what is worth watching?",
        spoken_title="So what is actually worth watching?",
        sentences=[
            ("You cannot know who is behind an address,",
             "and you usually cannot know why it moved."),
            ("What you can know is who is holding your own coins.",),
            ("Because if they are sitting on an exchange,",
             "you are one of the claims inside somebody else's whale."),
            ("Nothing in this video is financial advice.",),
            ("So, what do you think - is a custodian holding a million coins "
             "really a whale at all?",),
        ],
        shots=[
            Shot(clip=SUBWAY, clip_at=8.0),
            Shot(clip=ALONE, clip_at=2.0),
            Shot(clip=WINDOWS, clip_at=9.0),
            Shot(clip=RIPPLE, clip_at=16.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=OCEAN, clip_at=8.0),
        ],
        gaps=[0.70, 0.85, 0.95, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is a Crypto Whale? How Big Wallets Actually Work",
    hook="A crypto whale is any holder big enough to move a market on its "
         "own - but the biggest wallets on most chains are not people at "
         "all. Here is what counts as a whale, the five kinds of holder at "
         "that scale, why exchanges sit at the top of every rich list, and "
         "what a whale alert can and cannot tell you.",
    url=URL,
    summary="What a crypto whale is and how to read one: why there is no "
            "official threshold and the word is relative to supply and "
            "liquidity (roughly 1,000 BTC in Bitcoin, 10,000 ETH in "
            "Ethereum, a fraction of a percent in a thin altcoin), the five "
            "kinds of holder at whale scale - individuals, company "
            "treasuries, funds and market makers, foundations, and "
            "exchanges or custodians - why a custodial address holds "
            "customer coins rather than its own, and why a large transfer "
            "onto or off an exchange has several possible readings and the "
            "blockchain records none of them. Nothing here is financial "
            "advice.",
    tags=["crypto whale", "what is a crypto whale", "bitcoin whale",
          "crypto whale explained", "whale alert", "crypto custody",
          "exchange wallets", "cold storage", "on-chain analysis",
          "crypto for beginners"],
    cta=f"The full guide to crypto whales: {URL}",
    credits=["Footage and thumbnail photograph: Pexels (Pexels licence, "
             "no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-whale-long.mp4"
    work = Path.home() / "Desktop/.crypto-whale-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # Statement mode: the surprise is the proposition itself, not a token
        # inside it, so there is no gap worth pretending to. A redaction here
        # would fail the cover-the-bar test.
        hook="The biggest Bitcoin wallets do not belong to people",
        # **No forced rows here.** A newline in the headline is a break the
        # layout may not move, and a two-row headline gets the wider column
        # (1.38x) - which is how the first pass ended up with small type in
        # two lines, the note the user gave. Left to wrap, the narrow column
        # forces four big short rows and lands `[person]` on a line of its
        # own, which is also what keeps the plate clear of the word in front
        # of it.
        thumb_headline="The biggest whale is not a [person]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        # Type on the dark left half, the sun flare kept on the right.
        thumb_side="left", thumb_crop_at=(0.60, 0.25),
        thumb_crop_band="middle",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
