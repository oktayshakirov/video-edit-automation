"""What is market cap in crypto - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-market-cap-in-crypto.mdx.

**The angle.** What people actually connect a low price with is an easy
move up - a five cent coin "only" has to reach ten cents. So the video opens
on that belief (a `Stamp`, MYTH, judging the claim and never a coin) and
answers it with the one multiplication: a five cent coin can be bigger than a
hundred dollar one, and doubling either takes the same fifty million. The
rest is the half of the multiplication nobody looks at - *which* coins are
counted. Market cap, fully diluted value and free float are three answers;
an unlock schedule is why they drift apart; and the thin-float case is the
twist - a ten-billion-dollar figure nobody ever paid.

**No financial advice.** It describes a formula and what the formula leaves
out. It names no coin, no platform, no price level and no direction. The
doubling chapter says what a move would *mean* in market cap, never whether
one happens, and the unlock chapter never says an unlock makes a price fall -
only that it adds coins the headline number was not counting.

**Figures.** The article's own worked examples ($50 x 1M, $0.05 x 1B, the
1B-minted / 100,000-listed token, the $500M coin slipping 5%) or arithmetic
on them (the $100 x 100,000 row, the doubling). **One outside figure:** world
GDP of roughly $100 trillion a year (IMF World Economic Outlook, ~$105T for
2023 and ~$110T for 2024), said as "roughly" and drawn as "~$100T" so it
cannot date into a wrong claim. The 500-trillion-coin supply is a
hypothetical - no coin is named.

## The re-cut, and what the Hal Finney pair did that this did not

The first cut ran 3:21 and was reviewed against `first-bitcoin-transaction`,
which is performing well. Measured side by side: Finney is 619 words in 40
sentences with six holds; this was 511 words in 32 with two. Finney's roster
is the subject's own world (code, terminals, keyboards) and it had already
cut its rusted chain as "a metaphor for the noun rather than the noun". This
re-cut adds the chapter on the belief, the pizza the formula is explained
with, and holds where a picture should ride; and it cuts the chain, the
padlock, the crates and six coin clips.

## The beats

Last three crypto long-forms: first-bitcoin-transaction (timeline / steps /
stat / quote), musk-effect (diagram / chart / stat / timeline / compare),
crypto-whale (grid / checklist / split / compare).

* `bars` - three coins through the formula; the five-cent coin's bar is five
  times the hundred-dollar one's.
* `gauge` - one dollar across five hundred trillion coins, against the world
  economy. The limit first, the value second.
* `grid` - three ways to count one coin (market cap / FDV / free float).
* `chart` - circulating supply over time, stepping at each unlock. No y axis.
* `diagram` - the thin-float chain to a figure nobody paid.
* `checklist` - four things market cap does not tell you, all crossed,
  titled as the question the crosses answer.

**Footage: the act in the subject's own world** (`footage.md`). Rejected on
the contact sheets: `stack-of-gold-coins-dark-background/38905685` (a
candlestick chart behind the coin), `hand-holding-phone-scrolling-dark/
10238038` and every other phone clip with a legible feed, `gold-coins-macro-
dark-background/10243082` (an Ethereum coin over code), the vault folder
(cartoon infographics), banknote clips with a monarch's portrait, and the
SALE / Rebajas price tags.

**Thumbnail: the user's own image** (`assets/crypto/market-cap/`), the
headline set on ONE row in the empty band along the top. `render_thumb`'s
narrow column cannot do one row, so `thumbs()` calls the shared `_headline`
directly - same type, plate and shadow. Rebuild it alone with `--thumb`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/market-cap.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from PIL import Image

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform import thumb as T
from video_automation.longform.openers import Stamp

SOURCE_POST = "what-is-market-cap-in-crypto"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Range is luma/saturation sampled at 0.5/3/6/9s, then each clip looked at on
# a labelled three-frame contact sheet. Ten-second clips are one-use.
#
# **Re-cut 2026-10-06, after the first review.** Out: the rusty chain, the
# padlocked door and the warehouse crates (metaphors for "locked supply",
# not the thing - the user flagged the chain and the crates at 1:01 by name),
# and six of the ten coin clips (stacks, macro, chute, hopper, a falling
# coin), because a coin under every line stopped saying anything. Four coin
# shots remain, each under a line that is actually about a coin. In: the
# pizza the formula is explained with, money changing hands where a trade
# sets the price, the team and the signatures behind a vesting schedule.
# Several sit above the L48 box; relevance outranks palette, and `VideoShot`
# dims them.
TWO = V / "coins-on-table-dark-moody/8370544.mp4"                          # 10s, L49-72 S49-69, a silver and a gold coin, rack focus
SPREAD = V / "gold-coins-macro-dark-background/35996678.mp4"               # 10s, L9 S0, coins of different sizes on black, rack focus
COLUMNS = V / "coins-on-table-dark-moody/8370537.mp4"                      # 9s,  L81-84 S25-27, coins laid out in columns
SPIN = V / "coin-spinning-on-table-dark/18977071.mp4"                      # 17s, L37-67 S11-22, a coin face, then spinning down to rest
CALC = V / "calculator-hands-close-up-dark/6963484.mp4"                    # 16s, L77-82 S32-34, two hands on a desk calculator
PHONE = V / "hand-phone-glow-dark-night/6611948.mp4"                       # 26s, L68-73 S21-22, hands on a phone, the screen a blank glow
LENS = V / "magnifying-glass-document-dark/6979933.mp4"                    # 21s, L84-90 S25-27, a magnifier over a page - clip_at <= 9, a face arrives later
PIZZA = V / "pizza-slices-dark/5899530.mp4"                                # 30s, L131-146 S33-42, a whole pizza being cut into slices
SLICE = V / "cutting-pizza-into-slices/5898902.mp4"                        # 7s,  L137-143 S46-48, a cutter running through one slice
PAPERS = V / "magnifying-glass-document-dark/6929599.mp4"                  # 12s, L80-83 S6-8, top-down hands over forms on black
CASH = V / "hands-exchanging-cash/34579102.mp4"                            # 19s, L68-70 S17-18, a banknote passed hand to hand on dark
BILLS = V / "money-printing-press-banknotes/5651771.mp4"                   # 12s, L87-123 S12-17, hundred-dollar bills, slow push
TEAM = V / "business-meeting-boardroom-night/8847933.mp4"                  # 19s, L68-94 S16-17, a team reading papers at a boardroom table
SIGN = V / "team-signing-documents-office/8731515.mp4"                     # 13s, L82-135 S31-33, two people signing documents - clip_at >= 3, a portrait opens it
DATE = V / "calendar-pages-turning/1793371.mp4"                            # 15s, L143-171 S11-15, a hand writing a date into a planner
STALL = V / "street-vendor-paying-cash-night/34396008.mp4"                 # 8s,  L61-63 S44-49, a purchase at a lit night stall
STREET = V / "busy-people-walking-city-night/4122942.mp4"                  # 28s, L45-64 S29-36, a packed street at night - clip_at >= 6, bokeh before
CROWD = V / "night-market-crowd-stalls/19926187.mp4"                       # 28s, L66-68 S40-44, a packed night market
THIN = V / "empty-market-stalls-night/15777863.mp4"                        # 23s, L51-56 S26-28, a sparse market, a few people
MOON = V / "dark-ocean-waves-night-slow/32864351.mp4"                      # 31s, L58-63 S12-13, moonlight on open water - the one abstract

THUMB = ROOT / "assets/crypto/market-cap/meme-coins.jpg"                   # 1536x1024, supplied by the user - see CREDITS.md
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-is-market-cap-in-crypto"

BARS = ([("$100 x 100,000 coins", 0.2, "$10M"),
         ("$50 x 1 million coins", 1.0, "$50M"),
         ("5 cents x 1 billion coins", 1.0, "$50M")],
        "PRICE x COINS IN CIRCULATION")


SECTIONS = [
    # --- hook. No card; the belief is sentence one and the Stamp shows it.
    # The verdict lands on "size" at ~4.5s. ------------------------------
    Section(
        title="A cheap coin is not a small coin",
        card=False,
        sentences=[
            ("A five cent coin feels like an easier win than a hundred dollar one.",),
            ("But its size was never its price.",),
            ("Size is market cap,", "and it is one multiplication."),
            ("Once you can do it, the cheap coin stops looking cheap.",),
            ("Stay to the end,",
             "and you will know why a low price is not room to grow,",
             "and which coins a market cap is quietly counting."),
        ],
        shots=[
            Shot(clip=TWO, clip_at=0.5),
            Shot(clip=SPREAD, clip_at=0.5),
            Shot(clip=CALC, clip_at=1.0),
            Shot(clip=PHONE, clip_at=1.0),
            Shot(clip=LENS, clip_at=0.5),
        ],
        gaps=[0.85, 0.80, 0.70, 0.80, 0.90],
    ),

    # --- the formula, through a pizza -------------------------------------
    Section(
        title="How is market cap calculated?",
        spoken_title="So how is market cap actually calculated?",
        sentences=[
            ("Cut a pizza into eight slices, or into a thousand.",),
            ("Every slice gets cheaper.", "The pizza does not get any bigger."),
            ("A coin's price is the price of one slice.",),
            ("Market cap is the whole pizza:",
             "the price, times the number of coins in circulation."),
            ("So run three coins through it.",),
            # the bars' own sentence - one chunk per row.
            ("A hundred dollar coin, with a hundred thousand of them, is ten million.",
             "A fifty dollar coin, with a million of them, is fifty million.",
             "And a five cent coin, with a billion of them, is fifty million as well."),
            ("The cheapest coin on that list is five times the size of the dearest.",),
        ],
        shots=[
            Shot(clip=PIZZA, clip_at=1.0),
            None,
            Shot(clip=SLICE, clip_at=0.5),
            Shot(clip=PAPERS, clip_at=0.5),
            Shot(clip=COLUMNS, clip_at=0.5),
            Shot(graphic="bars", backdrop=BEATGROUND, payload=BARS),
            None,
        ],
        gaps=[0.60, 0.85, 0.70, 0.80, 0.55, 1.30, 0.90],
    ),

    # --- the belief the hook named -----------------------------------------
    # The section the first cut was missing: what people actually connect a
    # low price with is an easy move up. Answered as arithmetic, never as a
    # direction - "the market has to value it at fifty million more" says
    # what a move would *mean*, and nothing about whether one happens.
    Section(
        title="Is a cheap coin easier to double?",
        spoken_title="So is a cheap coin easier to double?",
        sentences=[
            ("Take the fifty dollar coin and the five cent coin from that list.",),
            ("For either one to double,",
             "the market has to value it at fifty million dollars more."),
            ("Five cents to ten cents sounds like nothing.",
             "It is the same fifty million."),
            ("Now push that arithmetic all the way.",),
            # the gauge's own sentence: the limit first, the value second.
            ("The whole world economy produces roughly a hundred trillion dollars a year.",
             "A coin with five hundred trillion in circulation, at one dollar each, "
             "would be worth five times that."),
            ("A price with a lot of zeros in front is not room to grow.",
             "Usually, it is just a lot of coins."),
        ],
        shots=[
            Shot(clip=CASH, clip_at=1.0),
            Shot(clip=BILLS, clip_at=0.5,
                 note=("+$50M", "the same climb, at either price")),
            None,
            Shot(clip=LENS, clip_at=8.0),
            Shot(graphic="gauge", backdrop=BEATGROUND,
                 payload=("$500T", 0.96, "500 trillion coins at $1 each",
                          0.19, "the world economy, about $100T a year",
                          "WHAT ONE DOLLAR WOULD MEAN")),
            Shot(clip=PHONE, clip_at=14.0),
        ],
        gaps=[0.65, 0.80, 0.90, 0.60, 1.40, 0.95],
    ),

    # --- which coins ---------------------------------------------------------
    Section(
        title="Which coins does it count?",
        spoken_title="But which coins does it actually count?",
        sentences=[
            ("Circulating supply sounds like a precise number.",),
            # the hinge rides in its own sentence, so it cannot eat reveal 0.
            ("It is a definition, and data sites draw it differently,",
             "so the same coin can be measured three ways."),
            # the grid's own sentence - one chunk per card.
            ("Market cap counts the coins circulating today.",
             "Fully diluted value counts every coin that will ever exist.",
             "And free float counts only the coins that can realistically trade."),
            ("Team wallets, treasuries and locked tokens can sit inside the first number,",
             "and still be nowhere near a market."),
        ],
        shots=[
            Shot(clip=CALC, clip_at=5.0),
            None,
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("Market cap", "price x coins circulating today"),
                           ("Fully diluted value", "price x every coin that will ever exist"),
                           ("Free float", "price x coins that can actually trade")],
                          "THREE WAYS TO COUNT ONE COIN")),
            Shot(clip=TEAM, clip_at=1.0),
        ],
        gaps=[0.85, 0.65, 1.30, 0.90],
    ),

    # --- unlocks -------------------------------------------------------------
    Section(
        title="What happens when locked coins unlock?",
        spoken_title="So what happens when those locked coins unlock?",
        sentences=[
            ("Many new tokens launch with a large share promised to a team, "
             "early investors and a treasury.",),
            ("Say a billion exist, and a hundred million circulate today.",),
            ("Its fully diluted value is then ten times its market cap.",),
            ("The other nine hundred million arrive on a vesting schedule.",),
            # the chart's own sentence: the line first, the marked moment second.
            ("Draw the circulating supply over time, and it does not rise smoothly.",
             "It jumps, on the day a block of locked coins is released."),
            ("Every unlock adds coins that were never part of the market cap you were shown.",),
        ],
        shots=[
            Shot(clip=SIGN, clip_at=2.5),
            None,
            Shot(clip=CASH, clip_at=10.0,
                 note=("10x", "fully diluted value against market cap")),
            Shot(clip=DATE, clip_at=2.0),
            Shot(graphic="chart", backdrop=BEATGROUND,
                 payload=([0.10, 0.10, 0.105, 0.11, 0.11, 0.115, 0.12, 0.40,
                           0.405, 0.41, 0.41, 0.415, 0.42, 0.66, 0.665, 0.67,
                           0.67, 0.675, 0.68, 0.97, 0.98, 1.0],
                          "CIRCULATING SUPPLY OVER TIME", 7, "an unlock")),
            None,
        ],
        gaps=[0.70, 0.70, 0.75, 0.70, 1.60, 0.90],
    ),

    # --- the twist -----------------------------------------------------------
    Section(
        title="Who actually set that price?",
        spoken_title="So who actually set that price?",
        sentences=[
            ("Go back to the pizza.",
             "Market cap prices every slice at whatever the last one sold for."),
            ("But that price only came from the coins that actually traded.",),
            ("Take a new token with a billion minted,",
             "and only a hundred thousand on sale."),
            # the diagram's own sentence - one chunk per node.
            ("A handful of trades in those hundred thousand tokens,",
             "prints a price of ten dollars.",
             "That price is then applied to all billion tokens,",
             "and the screen shows a ten billion dollar valuation."),
            ("Nobody paid ten billion dollars.",
             "A few trades set a price, and the multiplication did the rest."),
        ],
        shots=[
            Shot(clip=PIZZA, clip_at=20.0),
            Shot(clip=STALL, clip_at=0.5),
            Shot(clip=TEAM, clip_at=11.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("100,000 tokens trade", "a sliver of the supply"),
                           ("The price prints $10", "set by a handful of trades"),
                           ("A billion minted", "all valued at that price"),
                           ("$10B on the screen", "never paid by anyone")],
                          "WHERE A BIG NUMBER COMES FROM", False)),
            None,
        ],
        gaps=[0.70, 0.90, 0.70, 1.40, 0.95],
    ),

    # --- what it leaves out --------------------------------------------------
    # The spoken title is the checklist's hinge, so the beat comes first.
    Section(
        title="What does market cap leave out?",
        spoken_title="So what does market cap leave out?",
        sentences=[
            # four items, then a reaction chunk that claims no reveal slot and
            # lands in the pause where the crosses draw.
            ("How much of the supply can actually trade.",
             "When the locked coins arrive.",
             "Who holds most of it.",
             "And how deep the market behind it is.",
             "Market cap tells you none of them."),
            ("A crowded market can absorb a large order.",),
            ("A thin one moves the moment you touch it.",),
            ("Even a five hundred million dollar coin with a shallow order book",
             "can slip five percent on one moderate order."),
        ],
        shots=[
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("How much can actually trade", False),
                           ("When the locked coins arrive", False),
                           ("Who holds most of it", False),
                           ("How deep the market is", False)],
                          "DOES MARKET CAP TELL YOU THIS?")),
            Shot(clip=CROWD, clip_at=1.0),
            Shot(clip=THIN, clip_at=1.0),
            Shot(clip=STREET, clip_at=8.0,
                 note=("5%", "slippage on one moderate order")),
        ],
        gaps=[2.40, 0.70, 0.80, 0.90],
    ),

    # --- close ---------------------------------------------------------------
    Section(
        title="So what is market cap good for?",
        spoken_title="So what is market cap actually good for?",
        sentences=[
            ("It is the cleanest way to compare the size of two coins,",
             "and the reason a five cent coin is not automatically small,",
             "or automatically early."),
            ("It is a starting line, not a verdict.",),
            ("Nothing in this video is financial advice.",),
            ("So, the next time a coin looks cheap,",
             "would you check how many of them there are?"),
        ],
        shots=[
            Shot(clip=SPIN, clip_at=0.5),
            None,
            Shot(clip=MOON, clip_at=1.0,
                 payload=("", "This is not financial advice.")),
            None,
        ],
        gaps=[0.80, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is Market Cap in Crypto? Price x Supply Explained",
    hook="A five cent coin feels like it has more room to grow than a "
         "hundred dollar one. It does not - because a coin's size is its "
         "market cap, the price times the number of coins in circulation. "
         "Here is how it is calculated, why doubling takes the same money "
         "at any price, the difference "
         "between market cap, fully diluted value and free float, what "
         "unlocks do to the gap between them, and how a handful of trades "
         "can put a ten-billion-dollar valuation on a screen.",
    url=URL,
    summary="What market cap means in crypto and how to read it: the formula "
            "(price x circulating supply) and why unit price says nothing "
            "about size on its own; why a low price does not make a move "
            "easier, since doubling a five cent coin and a fifty dollar coin "
            "each takes the same fifty million in market cap; why circulating supply is a definition "
            "rather than a fact; market cap against fully diluted value and "
            "free float; how vesting unlocks add coins the headline number "
            "never counted; the thin-float case, where a price set by a "
            "sliver of the supply is multiplied across all of it; and what "
            "market cap leaves out - tradable supply, unlock timing, "
            "ownership concentration and liquidity. Nothing here is "
            "financial advice.",
    tags=["market cap", "what is market cap in crypto", "crypto market cap",
          "market cap explained", "fully diluted valuation", "FDV",
          "circulating supply", "free float", "token unlocks",
          "is a cheap coin better", "low price crypto",
          "crypto for beginners"],
    cta=f"The full guide to market cap: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "World economy figure: IMF World Economic Outlook.",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


HEADLINE = "Cheap coin. Easy [win?]"


def thumbs(out: Path) -> Path:
    """The 16:9 thumbnail: the supplied image, headline on one row at the top."""
    im = Image.open(THUMB).convert("RGB")
    im = im.resize((1280, 853), Image.LANCZOS).crop((0, 40, 1280, 760))
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 160, 1280 - 2 * 58, 58, fill, ink, max_lines=1,
                max_block=200, leading=1.0, band="top", margin=34,
                shadow=11, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/market-cap-long.mp4"
    work = Path.home() / "Desktop/.market-cap-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # A belief to overturn - the shape `Stamp` exists for, judging a
        # claim and never an asset. Last three long forms opened hook /
        # Search / hook.
        opener=Stamp("A cheap coin can grow more", "MYTH", at_word="size"),
        thumb_headline="Cheap coin. Easy [win?]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        # The heap pushed right and faded to black on the left, so the type
        # sits on real black rather than over coins.
        thumb_crop_at=(0.5, 1.0), thumb_side="left", thumb_shift=0.32,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/market-cap-long-thumb.jpg"))
    else:
        main()
