"""The Squid Game crypto scam - long-form 16:9 for YouTube, an E26 story.

Source: crypto-wiki/content/posts/the-squid-game-crypto-scam.mdx.

**The angle.** One theft told as a story (E26, `projects/crypto.md`): who,
the plan, the moment it worked, the mistake that did or did not catch them,
where the money is now. The search ("squid game crypto scam") is proven but
old - the 2021 Shorts own it and every recent small-channel retelling sits
under 250 views (`demand/teardowns/squid-game-crypto-scam.md`). None of
them draws the one thing the story turns on: a token anyone could buy and
only its creators could sell. This does, with a beat built for it
(`honeypot`), and then follows the money with TRM Labs' trace.

**Investigative devices** (`projects/crypto.md`): a planted fact - the
show's own rule, only one player walks out with the money - is said in
chapter one and pays off as the echo; the warning signs come back as a
list, every one of them visible before the pull.

**No financial advice.** The video judges claims and a mechanism, never an
asset: no price level or direction, nothing to buy or sell. The creators
are "the creators" and the scam is called a rug pull, which is how Gizmodo,
CoinDesk, Cointelegraph and TRM describe it; nobody is named because nobody
has been. The one check in the last chapter is the article's own lesson 2
(can a token be sold at all), framed as a check, never as a reason to buy.

**Figures, each with its source.** Netflix released Squid Game on 17
September 2021. Presale 20 October (the project's white paper: "sold out
within a second"); trading opened about 26 October at about a cent
(Cointelegraph); $38 on 31 October, ~$90 on the morning of 1 November;
peak $2,861.80 at about 09:35 UTC on 1 November, then $0.0007926 five
minutes later (CoinMarketCap via several outlets, 99.99%). Selling needed
Marbles, earned only by playing the project's game, which never launched
(CoinMarketCap Academy; "anti-dumping" was the team's own word,
Cointelegraph). The white paper: 10% of each entry fee to the developers.
Comments off on its Twitter, a closed Telegram (Cointelegraph, from Crypto
Tyrion 29 Oct). It claimed Netflix and CoinGecko as partners; CoinGecko's
co-founder Bobby Ong denied it (Cointelegraph). Cointelegraph's headline
"Users unable to sell Squid Game token clocking 45,000% gains" ran 29
October. About $3.38M taken (Gizmodo's revised estimate; CoinDesk 1 Nov).
The Telegram farewell: the developers no longer wanted to run the project
(CoinDesk). Twitter restricted the account for "unusual activity"; the
site and Medium went down (CoinDesk). TRM Labs: the creators swapped SQUID
for WBNB in the PancakeSwap pool, 55 deposits into Tornado Cash on 1
November, bridges to Ethereum, Compound, two exchanges with minimal KYC;
the same scammers linked to two other rug pulls, at least 35,025 BNB
(~$19.3M) across the three; not identified, no funds returned "as of yet".
The streamer who caught the crash live: TheDent on Twitch (TheClipZone's
Short, 1.8M views) - said, never shown.

## The beats

Last two crypto long forms: logan-paul (diagram / pile / checklist /
behind / timeline), stablecoin-interest (post / grid / reserve / stat /
bars / timeline / checklist). Signature beats resting: pile, behind, post,
reserve. `timeline` was in both, so the climb is a `chart`... no - a price
from one cent to $2,861 has no honest linear axis, so it is the real
TradingView capture (the site's `rugpull.jpg`) under `spotlight`, and the
climb is said over moving pictures with `note=` cards.

* `spotlight` - the real SQUID/WBNB chart, the camera going to the cliff.
* `diagram` - the game they pitched: buy, enter, survive, winner takes it.
* `honeypot` - **new, built for this video.** Buy passes the contract,
  your sell bounces off NEEDS MARBLES, the creators' sell goes through.
* `pool` - SQUID on one side, buyers' BNB on the other, drained.
* `steps` - the money's route: pool, Tornado Cash, a bridge, two exchanges.
* `stat` - $19.3M, three rug pulls, one trail.
* `checklist` - the warning signs, each one there before the pull.

**Opener: `Counter`** on $2,861 - the payoff of sentence 1 is a number.
The last three long forms opened Stamp / Search / Search.

**Real pages and pictures:** Cointelegraph's 29 October headline (users
unable to sell, three days before the pull), TRM Labs' report twice (only
the creators could sell; two more rug pulls), the real price chart, the
show's art from the site's own post (framed, credited).

**E26: 5-8 minutes, `FORMAT = "story"`.**

    PYTHONPATH=. .venv/bin/python projects/crypto-long/squid-game-token.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music, stillclip
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Counter

SOURCE_POST = "the-squid-game-crypto-scam"
DEMAND = ("'squid game crypto scam': TheClipZone 'Live RUG PULL of $SQUID' "
          "Short 978.8x (1.8M); Anant Ladha Short 15.5x (1.5M); CoinGecko "
          "'Rug Pull, Honeypot Scams Explained' ~15x (85k) - old; recent "
          "retellings under 250 views")
FORMAT = "story"
# The cover's style, for the review to compare views and clicks by
# (`thumbnails.md`, "Cover styles are a choice, and every video says which").
COVER_STYLE = "cutout"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
SITE = Path.home() / "Coding/crypto-wiki/public/images/posts"
CAP = STOCK / "captures"

# The site's own pictures. `rugpull.jpg` is a real TradingView capture of
# SQUID / Wrapped BNB on PancakeSwap, 06:30-10:30 UTC on 1 Nov 2021 only
# (one-minute candles, priced in WBNB, log scale): the cliff at
# 09:35 UTC. `squid-game.jpg` is the show's art the post carries.
CHART = SITE / "rugpull.jpg"            # 1149x745
SHOW = SITE / "squid-game.jpg"          # 900x450

# Real pages, captured 2026-11-19 (`screencap`, records committed).
CT_HEAD = CAP / "cointelegraph-squid-cant-sell/cointelegraph-squid-cant-sell-l.mp4"
CT_ADDR = "cointelegraph.com/news/users-not-able-to-sell-squid-game-token"
TRM_ONLY = CAP / "trm-squid-trail/trm-only-l.mp4"
TRM_LINK = CAP / "trm-squid-trail/trm-link-l.mp4"
TRM_ADDR = "trmlabs.com/post/on-the-trail-of-the-squid-game-scammers"

# Fetched for this pair 2026-11-19, contact-sheeted, B = the set's luma at
# 0.5/3/6/9s - see the footage.md verdicts.
# The trading-app phone and the three chart screens were dropped after the
# first render: each carries a readable ticker (Apple Inc, EUR/USDC, BTC/USDT)
# that has nothing to do with SQUID. Price moments sit on the real chart.
TAPDARK = V / "finger-tapping-phone-screen-dark/33942937.mp4"   # 15s, B8-9, a finger over a phone in the dark
TAP = V / "finger-tapping-phone-screen-dark/13161559.mp4"       # 9s, B20-25, a finger tapping a tablet
LAPTOP = V / "man-frustrated-laptop-night-dark/8311535.mp4"     # 24s, B10-31, a man at a laptop at night
SCROLL = V / "person-scrolling-phone-news-dark/13358555.mp4"    # 15s, B9-10, two hands on a phone, dark
HOOD = V / "person-laptop-anonymous-dark-room/36036810.mp4"     # 12s, B24-26, a hooded figure at a laptop, face unseen
CHAT = V / "phone-chat-typing-dark-night/39494892.mp4"          # 27s, B26-28, a hand on a phone in a chat app
CHATLIST = V / "phone-chat-typing-dark-night/28828935.mp4"      # 17s, B14-24, a phone's chat list in the dark
COUNT = V / "countdown-timer-digital-screen-dark/33504957.mp4"  # 11s, B6-9, digits counting down in gold dots
STREAMER = V / "game-streamer-microphone-dark/9071269.mp4"      # 22s, B33-34, a gamer on a headset mic at his desk
SERVERS = V / "server-room-lights-dark/7140928.mp4"             # 9s, B23-39, server fronts with green lights
MARBLES = V / "glass-marbles-close-up-dark/7233704.mp4"         # 10s, bright (B150+): glass marbles, framed only

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/the-squid-game-crypto-scam"

DISCLAIMER_BG = stillclip.path(CHART, focus=(0.68, 0.5))


def sections() -> list:
    return [
    # --- hook. No card. ---------------------------------------------------------
    Section(
        title="The Squid Game crypto scam",
        card=False,
        sentences=[
            ("On the first of November 2021, a token called SQUID hit two thousand eight hundred and sixty one dollars.",),
            ("Five minutes later, it was worth less than a tenth of a cent.",),
            ("And almost nobody holding it could sell a single coin on the way down.",),
            ("Its creators left with about three point four million dollars, and nobody has ever been named.",),
            ("So how do you build a coin that nobody can sell?",),
            ("Stay to the end for the one check that would have caught it in a minute.",),
        ],
        shots=[
            Shot(clip=TAPDARK, clip_at=1.0),
            # The real chart: the whole day, then the camera on the cliff.
            Shot(graphic="spotlight",
                 payload=(CHART, [(None, ""),
                                  ((0.50, 0.06, 0.92, 0.96), "09:35 UTC, 1 NOV 2021")],
                          "SQUID / BNB, THE REAL CHART", False)),
            None,
            Shot(clip=HOOD, clip_at=1.0, note=("~$3.38M", "taken, Gizmodo's estimate")),
            Shot(clip=CHAT, clip_at=3.0, window=("player", "A coin you can buy, and not sell")),
            None,
        ],
        gaps=[0.75, 0.85, 0.70, 0.80, 0.80, 0.90],
    ),

    # --- the plan -----------------------------------------------------------------
    Section(
        title="Who made the Squid Game token?",
        spoken_title="So who was behind the Squid Game token?",
        kicker="THE PLAN",
        sentences=[
            ("In September 2021, Squid Game became the biggest show on Netflix.",),
            ("A month later, an anonymous team launched a token named after it, with no link to Netflix at all.",),
            ("They said SQUID would pay for an online game based on the show.",),
            # the diagram's own sentence: one chunk per box.
            ("You buy SQUID,",
             "pay it to enter,",
             "survive six rounds,",
             "and the last player standing wins the pot."),
            ("Unlike the show, they said, the prize would have no limit. The team would keep ten percent of every entry fee.",),
            ("On the twentieth of October, the presale sold out, the project said, in a second.",),
            ("And the show they borrowed has one rule worth remembering. Only one player walks out with the money.",),
        ],
        shots=[
            Shot(image=SHOW, parallax=0.4),
            Shot(clip=HOOD, clip_at=0.0, window=("player", "An anonymous team, no names given")),
            None,
            Shot(graphic="diagram", ground="grid",
                 payload=([("Buy SQUID", "the project's own token", "\U0001FA99"),
                           ("Pay to enter", "an entry fee in SQUID", "\U0001F39F"),
                           ("Survive six rounds", "games from the show", "\U0001F3AE"),
                           ("Winner takes the pot", "90% of the fees", "\U0001F3C6")],
                          "THE GAME THEY PITCHED", False)),
            Shot(clip=CHATLIST, clip_at=2.0, note=("10%", "of every entry fee, to the team")),
            Shot(clip=COUNT, clip_at=1.0, note=("20 OCT", "the presale, sold out")),
            Shot(image=SHOW, parallax=0.5),
        ],
        gaps=[0.60, 0.70, 0.55, 1.40, 0.70, 0.80, 0.95],
    ),

    # --- the climb ------------------------------------------------------------------
    Section(
        title="Why did SQUID only go up?",
        spoken_title="So why did the price only ever go up?",
        kicker="THE CLIMB",
        sentences=[
            ("Trading opened on the twenty-sixth of October, at about a cent.",),
            ("Five days later it was thirty-eight dollars, and on the morning of November first, ninety.",),
            ("News sites covered the climb, and every story brought new buyers in.",),
            ("The BBC reported that buyers were complaining they could not sell. People kept buying anyway.",),
            ("Actually, three days before the end, this headline already said what was wrong.",),
            ("Users unable to sell.",),
            ("A price that only climbs is not proof that people want in. It can mean nobody is allowed out.",),
        ],
        shots=[
            Shot(clip=SCROLL, clip_at=1.0, note=("$0.01", "SQUID's first trades, 26 Oct")),
            # The real chart again, the camera on the climb this time.
            Shot(graphic="spotlight",
                 payload=(CHART, [((0.25, 0.15, 0.70, 0.45), "1 NOV, THE LAST MORNING")],
                          "SQUID / BNB", False)),
            None,
            Shot(image=SHOW, window=("player", "Squid Game, Netflix, 2021")),
            Shot(clip=CT_HEAD, clip_at=0.0, window=("browser", CT_ADDR)),
            None,
            Shot(clip=COUNT, clip_at=3.0),
        ],
        gaps=[0.60, 0.70, 0.60, 0.80, 0.55, 0.90, 0.95],
    ),

    # --- the trap -------------------------------------------------------------------
    Section(
        title="Why couldn't anyone sell SQUID?",
        spoken_title="So why couldn't anyone sell?",
        kicker="THE TRAP",
        card_gap=1.30,
        sentences=[
            ("SQUID traded on PancakeSwap, where you swap with a pool of coins, not with a person.",),
            ("And the token's own rules decided who could use it.",),
            # the honeypot's own sentence: one chunk per reveal.
            ("Anyone could buy SQUID with BNB.",
             "But when a holder tried to sell,",
             "the rules asked for marbles, earned only in a game that never launched.",
             "The creators' own wallet needed nothing at all."),
            ("The team called it anti-dumping technology, a way to stop people selling too fast.",),
            ("It stopped everyone except them.",),
            ("TRM Labs, a firm that traces stolen crypto, read the contracts the same way.",),
            ("A token you can buy and never sell has a name: a honeypot.",),
        ],
        shots=[
            Shot(clip=TAP, clip_at=0.5, window=("player", "Swapping with a pool, not a person")),
            Shot(clip=MARBLES, clip_at=1.0, window=("player", "Marbles: the second token you needed")),
            Shot(graphic="honeypot", ground="grid",
                 payload=(("YOU", "a SQUID holder"), ("THE CREATORS", "anonymous"),
                          ("THE POOL", "BNB, on PancakeSwap"), "NEEDS MARBLES",
                          "THE GAME NEVER LAUNCHED", "NO RULE FOR THEM",
                          "WHO COULD SELL SQUID")),
            Shot(clip=CHATLIST, clip_at=8.0, note=("ANTI-DUMPING", "the team's word for it")),
            None,
            Shot(clip=TRM_ONLY, clip_at=0.0, window=("browser", TRM_ADDR)),
            Shot(clip=SERVERS, clip_at=1.0, window=("player", "A honeypot: in, never out")),
        ],
        gaps=[0.60, 0.55, 1.80, 0.70, 0.95, 0.70, 0.90],
    ),

    # --- the other warnings -------------------------------------------------------
    Section(
        title="Were there other warning signs?",
        spoken_title="And were there other warnings?",
        kicker="THE SIGNS",
        sentences=[
            ("Plenty, and all of them in public.",),
            ("Replies were switched off on its Twitter account, and its Telegram group did not let anyone talk.",),
            ("It claimed Netflix and CoinGecko as partners. CoinGecko's co-founder said that was not true.",),
            ("Its white paper was full of spelling mistakes and claims nobody could check.",),
            ("And by the last weekend, CoinMarketCap was telling visitors it had reports that holders could not sell.",),
        ],
        shots=[
            Shot(clip=LAPTOP, clip_at=2.0),
            Shot(clip=CHAT, clip_at=20.0, note=("REPLIES OFF", "Twitter, and a closed Telegram")),
            Shot(image=SHOW, window=("player", "Squid Game, Netflix, 2021")),
            None,
            Shot(clip=SCROLL, clip_at=7.0, note=("CoinMarketCap", "warned holders could not sell")),
        ],
        gaps=[0.60, 0.70, 0.80, 0.70, 0.90],
    ),

    # --- the pull -------------------------------------------------------------------
    Section(
        title="What happened on November 1?",
        spoken_title="So what happened on November first?",
        kicker="THE PULL",
        card_gap=1.30,
        sentences=[
            ("At about nine thirty-five in the morning, UTC, SQUID touched its peak.",),
            ("Then the creators did the one thing nobody else could. They sold.",),
            # the pool's own sentence: coins, money, the pull.
            ("On one side of the pool sat everyone's SQUID.",
             "On the other, the money that buyers had paid in.",
             "The creators swapped their own SQUID for that money, until the money side was empty."),
            ("Within five minutes, the price had fallen ninety-nine point nine nine percent.",),
            ("A streamer happened to be reading the price out loud on Twitch at that moment. His scream became one of crypto's most watched clips.",),
            ("In the project's Telegram channel, a last message said the developers no longer wanted to run it.",),
            ("By that afternoon the website was down, and Twitter had restricted the account.",),
        ],
        shots=[
            Shot(clip=COUNT, clip_at=0.0, note=("09:35 UTC", "SQUID's peak, 1 Nov")),
            None,
            Shot(graphic="pool", ground="grid",
                 payload=("SQUID", "everyone's coins",
                          "BNB", "what buyers paid in",
                          "THE CREATORS", "nothing left to sell into",
                          "1 NOVEMBER, 09:35 UTC")),
            Shot(graphic="spotlight",
                 payload=(CHART, [((0.50, 0.06, 0.92, 0.96), "-99.99% IN FIVE MINUTES")],
                          "SQUID / BNB", False)),
            Shot(clip=STREAMER, clip_at=10.0),
            Shot(clip=CHATLIST, clip_at=10.5, note=("LAST MESSAGE", "the developers quit")),
            Shot(clip=HOOD, clip_at=3.0),
        ],
        gaps=[0.60, 0.85, 1.80, 0.80, 0.80, 0.70, 0.90],
    ),

    # --- the trail ------------------------------------------------------------------
    Section(
        title="Where did the Squid Game money go?",
        spoken_title="So where did the money go?",
        kicker="THE TRAIL",
        sentences=[
            ("Not far, at first. TRM Labs followed it, step by step.",),
            # the steps' own sentence: one chunk per node.
            ("It left the pool as BNB,",
             "went into Tornado Cash, a mixer, in fifty-five deposits that same day,",
             "crossed a bridge onto Ethereum,",
             "and came out through two exchanges that checked almost no identity."),
            ("The US Treasury sanctioned Tornado Cash itself in 2022, and lifted the sanctions in 2025.",),
            ("But the same trail led somewhere else too.",),
            ("TRM linked the people behind SQUID to two more rug pulls.",),
            ("Across all three, about nineteen million dollars.",),
            ("And as of TRM's report, nobody had been named, and no buyer had been paid back.",),
        ],
        shots=[
            Shot(clip=SERVERS, clip_at=3.0, window=("player", "Following the money, block by block")),
            Shot(graphic="steps", ground="grid",
                 payload=([("Out of the pool, as BNB", "\U0001F4B0"),
                           ("Into Tornado Cash, 55 deposits", "\U0001F300"),
                           ("Across a bridge to Ethereum", "\U0001F309"),
                           ("Out through two exchanges", "\U0001F3E6")],
                          "WHERE THE MONEY WENT")),
            None,
            None,
            Shot(clip=TRM_LINK, clip_at=0.0, window=("browser", TRM_ADDR)),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("$19.3M", "three rug pulls", "one trail, by TRM Labs' count")),
            Shot(clip=HOOD, clip_at=5.0),
        ],
        gaps=[0.60, 1.50, 0.70, 0.80, 0.55, 0.85, 0.95],
    ),

    # --- the check and the echo -----------------------------------------------------
    Section(
        title="How would you have caught it?",
        spoken_title="So how would you have caught it?",
        kicker="THE CHECK",
        card_gap=1.30,
        sentences=[
            ("Every one of these was there before the pull.",),
            # the checklist's own sentence: one chunk per row.
            ("A price that only went up.",
             "Comments switched off.",
             "A partnership nobody confirmed.",
             "A warning that holders could not sell.",
             "And a rule that said you could not leave."),
            ("The check that would have caught it costs a few dollars.",),
            ("Try to sell a tiny amount back. If it will not let you sell that, it will not let you sell more.",),
            ("In the show, only one player walks out with the money. SQUID kept that rule, and the creators were the player.",),
            ("Nothing in this video is financial advice.",),
            ("So, the last thing you bought online: did you ever check that you could sell it?",),
        ],
        shots=[
            Shot(clip=LAPTOP, clip_at=12.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("A price that only went up", True),
                           ("Comments switched off", True),
                           ("A partner nobody confirmed", True),
                           ("A can't-sell warning", True),
                           ("A rule against leaving", True)],
                          "SQUID HAD EVERY ONE", True)),
            Shot(clip=CHAT, clip_at=8.0, note=("A FEW DOLLARS", "the cost of a test sale")),
            None,
            Shot(image=SHOW, window=("player", "Squid Game, Netflix, 2021")),
            # The video's own subject, not weather (2026-11-06).
            Shot(clip=DISCLAIMER_BG, clip_at=0.5,
                 payload=("", "This is not financial advice.")),
            Shot(clip=TAPDARK, clip_at=6.0),
        ],
        gaps=[0.55, 2.40, 0.55, 0.90, 0.90, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="Squid Game Crypto Scam: How $3.4 Million Vanished in 5 Minutes",
    hook="On 1 November 2021 a token called SQUID, named after Netflix's "
         "Squid Game, hit $2,861. Five minutes later it was worth less than "
         "a tenth of a cent, and almost nobody holding it could sell. Here "
         "is how the trap was built, what happened at 09:35 UTC, where the "
         "money went, and the one check that would have caught it.",
    url=URL,
    summary="The Squid Game token (SQUID) scam, told in order: an anonymous "
            "team launched SQUID in October 2021 for a play-to-earn game "
            "based on the Netflix show, with no link to Netflix; the presale "
            "on 20 October and trading on PancakeSwap from about a cent; the "
            "climb to $2,861.80; the honeypot - selling needed Marbles, "
            "earned only in a game that never launched, while the creators' "
            "wallet could sell freely; the warning signs (comments off, a "
            "closed Telegram, partnerships with Netflix and CoinGecko that "
            "were denied, Cointelegraph's 29 October headline, CoinMarketCap's "
            "warning); the rug pull at about 09:35 UTC on 1 November, when "
            "the creators swapped their SQUID for the pool's BNB and took an "
            "estimated $3.38 million; and TRM Labs' trace of the money "
            "through 55 Tornado Cash deposits, a bridge to Ethereum and two "
            "exchanges, linking the same people to two more rug pulls worth "
            "about $19.3 million in all. Nothing here is financial advice.",
    tags=["squid game crypto scam", "squid game token", "squid game coin",
          "squid token rug pull", "squid game crypto", "honeypot token",
          "what is a honeypot crypto", "rug pull", "crypto rug pull",
          "can't sell crypto token", "tornado cash", "crypto scams",
          "pancakeswap scam"],
    cta=f"Every warning sign, the full timeline and how to check a token "
        f"before you touch it: {URL}",
    credits=["Nothing in this video is financial advice.",
             "Pages: Cointelegraph, \"Users unable to sell Squid Game token "
             "clocking 45,000% gains\" (29 Oct 2021); TRM Labs, \"On the "
             "Trail of the Squid Game Scammers\" (captured 19 Nov 2026).",
             "Squid Game artwork: Netflix, shown for commentary. SQUID/WBNB "
             "chart: TradingView, via thecrypto.wiki.",
             "Sources: Gizmodo, CoinDesk, Cointelegraph, CoinMarketCap, TRM "
             "Labs."],
)

HEADLINE = "Only one\n[winner]"
# A hooded man on black, face lost in the hood: Pexels 761684, fetched for
# the cover only and never used inside the video (`thumbnails.md`, "The
# cover's picture stays on the cover").
HOODED = STOCK / "photos/hooded-man-dark-background/761684.jpg"
# The picked direction first (`thumbnails.md`, "A cover is written once").
COVERS = ("cutout",)


def _cut(src):
    import numpy as np
    from PIL import Image
    from video_automation.core import vision
    im = Image.open(src).convert("RGB")
    im.thumbnail((1800, 1800))
    c = Image.fromarray(np.asarray(vision.cutout(im)).copy())
    return c.crop(c.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox())


def _radial(size, centre, inner, outer, r):
    import numpy as np
    from PIL import Image
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    k = np.clip(np.sqrt((xx - centre[0]) ** 2 + (yy - centre[1]) ** 2) / r, 0, 1)[:, :, None]
    arr = np.array(inner, np.float32) * (1 - k) + np.array(outer, np.float32) * k
    return Image.fromarray(arr.astype(np.uint8)).convert("RGBA")


def cover(kind: str, portrait: bool = False):
    """One cover, 1280x720 or (`portrait`) 1080x1920, as an RGB image.

    `cutout`: the hooded man in front of an extruded 1, ONLY ONE [WINNER] -
    the show's rule, the twist the title does not say. The editor picked it
    over the real chart's cliff with a ring (NOBODY COULD [SELL]), whose
    code was deleted 2026-11-19."""
    from PIL import Image
    from video_automation.longform import thumb as T
    W, H = (1080, 1920) if portrait else (1280, 720)
    gold, deep = (255, 199, 0), (120, 80, 0)
    fill, ink = T.ACCENTS["yellow"]
    if kind == "cutout":
        man = _cut(HOODED)
        if portrait:
            im = _radial((W, H), (540, 1150), (90, 66, 8), (8, 7, 4), 1100)
            im.alpha_composite(T.extrude_text((W, H), "1", (90, 470), 820,
                               face=gold, side=deep, depth=30, direction=(0.7, 1.0)))
            h = 1000
            c = man.resize((int(man.width * h / man.height), h), Image.LANCZOS)
            im.alpha_composite(c, (W - c.width + 120, H - h))
            im = im.convert("RGB")
            T._headline(im, HEADLINE, 210, W - 120, 60, fill, ink, max_lines=2,
                        max_block=H * 0.22, leading=1.02, band="top",
                        margin=int(H * 0.06), shadow=14, drop=(6, 8))
            return im
        im = _radial((W, H), (760, 330), (90, 66, 8), (8, 7, 4), 900)
        im.alpha_composite(T.extrude_text((W, H), "1", (520, -60), 700,
                           face=gold, side=deep, depth=24, direction=(0.7, 1.0)))
        h = 640
        c = man.resize((int(man.width * h / man.height), h), Image.LANCZOS)
        im.alpha_composite(c, (W - c.width + 90, H - h))
        im = im.convert("RGB")
        T._headline(im, HEADLINE, 170, int(600 / 1.38), 48, fill, ink,
                    max_lines=2, leading=1.0, band="bottom", margin=44,
                    shadow=12, drop=(5, 6))
        return im
    raise ValueError(f"unknown cover {kind!r} - {COVERS}")


def thumbs(out: Path, portrait: bool = False, variants: bool = False) -> list[Path]:
    """The picked cover (the first of COVERS) at `out`, and nothing else;
    `variants=True` (`--thumb-variants`) writes the other directions as
    `-<style>` beside it, for choosing."""
    cover(COVERS[0], portrait).save(out, quality=92)
    made = [out]
    if variants:
        for k in COVERS[1:]:
            q = out.with_name(f"{out.stem}-{k}{out.suffix}")
            cover(k, portrait).save(q, quality=92)
            made.append(q)
    return made


def main() -> None:
    stillclip.make(CHART, focus=(0.68, 0.5))
    out = Path.home() / "Desktop/squid-game-token-long.mp4"
    work = Path.home() / "Desktop/.squid-game-token-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        opener=Counter("$2,861", "SQUID, 1 NOV 2021", at_word="two",
                       spin_from="$0,000"),
        emphasis=["nobody is allowed out", "except them", "nineteen million"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))[0]
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv or "--thumb-variants" in sys.argv:
        for q in thumbs(Path.home() / "Desktop/squid-game-token-long-thumb.jpg",
                        variants="--thumb-variants" in sys.argv):
            print(q)
    else:
        main()
