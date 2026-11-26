"""Is Bitcoin a Ponzi scheme? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-bitcoin.mdx - how a coin moves
(a public ledger, no central authority), where new coins come from (the
block subsidy, paid to miners for securing the network) and what the
paper set out to build ("peer-to-peer electronic cash").

**The angle (E24's second, the editor's yes 2026-11-24).** The title is the
claim as people type it. Proven on four channels: The Iced Coffee Hour
Clips' Peter Schiff 14.5x, Coinbase's "Myth" 4.5x, Austin Talks Money
"Bitcoin: Scam, Ponzi, or Something Bigger?" 4.0x, CNBC's McCauley 2.6x
(`demand/crypto.md`, 2026-11-25). Teardown:
`demand/teardowns/is-bitcoin-a-ponzi-scheme.md` - the definition first,
named Ponzis as the measuring stick, the sceptic's case given its own
chapter, a side-by-side that ends on a checklist. What we cannot have: his
verdict ("sound money"). **Verdicts judge the claim against a definition,
never the asset.** The sceptic's true part - Bitcoin pays nothing, so a
holder gains only if a later buyer pays more - is said plainly and left
standing. No direction, no "safe".

**Every figure and quote is sourced.** The definition: SEC, Investor.gov,
"Ponzi Scheme" ("pays existing investors with funds collected from new
investors"). Charles Ponzi: 50% in 45 days by early 1920 (US Postal
Inspection Service; American Heritage). Madoff: customers' 30 Nov 2008
statements, net of negative accounts, showed $64.8B (SIPC trustee).
BitConnect: DOJ, 25 Feb 2022 indictment, "approximately $2.4 billion",
a "Lending Program" backed by a "trading bot" and "volatility software".
Ben McKenzie: Senate Banking Committee, 14 Dec 2022, "In my opinion, the
cryptocurrency industry represents the largest Ponzi scheme in history."
Warren Buffett: CNBC Squawk Box, 7 May 2018, "The asset itself is
creating nothing." The paper: "Bitcoin: A Peer-to-Peer Electronic Cash
System", 31 Oct 2008.

## The picture (planned per sentence before any footage, `workflow.md`)

* Search opener types "is bitcoin a ponzi scheme" over $20 bills on black.
* a hand holding a fan of $100s, in a window - "early buyers ... later".
* `post` - McKenzie's own sentence to the Senate.
* `grid` - three things to check, the promise.
* `post` - the SEC's definition, word for word (Investor.gov and sec.gov
  refuse a headless browser, so the page could not be captured).
* Charles Ponzi, whole and named; Madoff as a cut-out (`behind`) with
  NASDAQ read whole, then tucked behind his head - who he was, before
  what he did; `stat` - $64.8B.
* the DOJ's BitConnect release, "$2.4 billion" ringed.
* `ponzi` (new) - new investors in, "returns" out, the inflow cut: $0.
* `ponzi` again, market mode - the same three cards with nobody in the
  middle. The one picture the pair is about, drawn twice.
* mempool.space's block page, the miner's subsidy ringed.
* `post` - the paper's own title.
* `stat` - $0 paid to holders; `post` - Buffett's line.
* `checklist` - the claim, checked, each item struck as it is said
  (`flow=True`); the disclaimer on Ponzi's photo.
* `peers` (new) - bitcoins moving wallet to wallet, nobody in the
  middle, under "Bitcoin has no payouts to stop".
* the counted cash with a red cross - NO OPERATOR - under "nobody in the
  middle"; mempool.space's chain of blocks for the public ledger.
* Clips: dollars only - on black, counted at a desk; the two bright $100
  fans only in windows. Re-cut 2026-11-25 on the editor's notes (dollars,
  a moving-bitcoin screen, a cut-out, who Madoff was, the fees ring held,
  the checklist struck item by item). No `pile`, `relay`, `honeypot`, `pool`, `reserve` (the last
  two crypto long forms' signatures).

**Opener: `Search`**, the title as typed (last three: Search, Counter,
Search - not three running).

    PYTHONPATH=. .venv/bin/python projects/crypto-long/bitcoin-ponzi.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music, stillclip
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "what-is-bitcoin"
DEMAND = ("Austin Talks Money 'Bitcoin: Scam, Ponzi, or Something Bigger?' "
          "4.0x (31.7k); Iced Coffee Hour Clips 'Why Bitcoin is a SCAM! | "
          "Peter Schiff' 14.5x (385k); Coinbase 'Myth: Bitcoin is a Ponzi "
          "Scheme' 4.5x")
# The cover's style (`thumbnails.md`, "Cover styles are a choice").
COVER_STYLE = "vector"

V = STOCK / "videos"
CAP = STOCK / "captures"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
BP = ROOT / "assets/crypto/bitcoin-ponzi"

# Fetched for this pair (2026-11-25) - see footage.md, "The bitcoin-ponzi
# fetch: verdicts".
# One shoot of banknotes; "gold bars", "empty desk" and
# "two people exchanging" found nothing on palette or on the noun.
# The phone on a trading app (34953965) showed a FTSE 100 chart under
# "Bitcoin" in the first cut - dropped from both formats (2026-11-25).
# **Dollars, not złoty** (the editor on the first cut: the counted-cash
# clips were "over used and the currency is not common one, use dollars").
# Pexels' dollars are nearly all on bright wood: the two bright fans go in
# windows only.
USD20 = V / "dollar-bills-black-background/6590462.mp4"         # 10s, $20 bills standing on black, a reflection
USD1 = V / "dollar-bills-black-background/6590464.mp4"          # 11s, $1 bills on black, darkens past 3s
STACKS = V / "counting-money-low-light/6266432.mp4"             # 18s, hands counting $100 stacks at a desk
DESK = V / "counting-money-low-light/7062994.mp4"               # 12s, a man counting at a lamp-lit desk
FAN100 = V / "counting-hundred-dollar-bills-hands-dark/5466773.mp4"  # 8s, two hands fan $100s - bright, window
FAN_ONE = V / "counting-hundred-dollar-bills-hands-dark/5466780.mp4"  # 11s, one hand holds a fan of $100s - bright, window

# The real pages (`screencap`, records in `captures/<name>/`).
# Investor.gov and sec.gov both refuse a headless browser (Access Denied,
# Rate Threshold) - the definition goes on a `post` card, word for word.
DOJ_AMOUNT = CAP / "doj-bitconnect/amount.mp4"
DOJ_PONZI = CAP / "doj-bitconnect/ponzi.mp4"
DOJ_ADDR = "justice.gov - BitConnect founder indicted"
BLOCK = CAP / "mempool-block/subsidy.mp4"
LEDGER = CAP / "mempool-block/ledger.mp4"
BLOCK_ADDR = "mempool.space - a Bitcoin block"

# Wikimedia Commons, public domain (CREDITS.md).
PONZI = BP / "charles-ponzi.jpg"
MADOFF = BP / "bernie-madoff.jpg"
# the mug shot set lower in its own wall, widened to 16:9, so `behind` has
# room for the word above his head (cover 1.0 on the 3:4 original)
MADOFF_WIDE = BP / "bernie-madoff-wide.jpg"
DISCLAIMER_BG = stillclip.path(PONZI, focus=(0.5, 0.35))

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-is-bitcoin"


def _ponzi(mode: str):
    """The pair's beat, in either mode (fresh each call, `beats.md`, "Build
    each format from fresh `Shot` objects")."""
    if mode == "ponzi":
        return Shot(graphic="ponzi", ground="grid",
                    payload=("ponzi", ("EARLY INVESTORS", "paid 'returns'"),
                             ("THE OPERATOR", "Ponzi, Madoff, BitConnect"),
                             ("NEW INVESTORS", "pay in"),
                             "'RETURNS'", "COLLAPSES", "HOW A PONZI PAYS"))
    return Shot(graphic="ponzi", ground="grid",
                payload=("market", ("THE SELLER", "gets your dollars"),
                         ("NOBODY", "in the middle"), ("YOU", "the buyer"),
                         "HOLDS NO MONEY", "PROMISES NO RETURN",
                         "WHEN YOU BUY BITCOIN", "BTC"))


def sections() -> list:
    return [
    # --- hook. No card. The Search types the title. ----------------------------
    Section(
        title="Is Bitcoin a Ponzi scheme?",
        card=False,
        sentences=[
            ("People call Bitcoin a Ponzi scheme: early buyers getting rich off the ones who come later.",),
            ("Part of that is true, and by the end you'll know exactly which part.",),
            ("But a Ponzi scheme needs three things, and Bitcoin is missing two of them.",),
            # the post's own sentence: the lead-in, then the quoted words.
            ("In 2022, the actor Ben McKenzie told the US Senate that crypto is",
             "the largest Ponzi scheme in history."),
            # the grid's own sentence: one chunk per card.
            ("So check Bitcoin against the definition: who holds the money,",
             "who promises the return,",
             "and who pays it out?"),
        ],
        shots=[
            Shot(clip=USD20, clip_at=0.5),
            Shot(clip=FAN_ONE, clip_at=0.0,
                 window=("player", "Early buyers, paid by later ones?")),
            None,
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("post",
                          {"name": "Ben McKenzie", "handle": "actor, author of Easy Money",
                           "date": "14 Dec 2022, US Senate Banking Committee",
                           "text": "In my opinion, the cryptocurrency industry "
                                   "represents [the largest Ponzi scheme in "
                                   "history.]"},
                          "THE CLAIM")),
            Shot(graphic="grid", ground="grid",
                 payload=([("Who holds the money?", "the operator", "\U0001F3E6"),
                           ("Who promises a return?", "the pitch", "\U0001F4C8"),
                           ("Who pays it out?", "the collapse", "\U0001F4B8")],
                          "THREE THINGS TO CHECK")),
        ],
        gaps=[0.70, 0.90, 0.80, 1.00, 0.90],
    ),

    # --- the definition --------------------------------------------------------
    Section(
        title="What makes a Ponzi scheme?",
        spoken_title="So what actually makes something a Ponzi scheme?",
        kicker="THE DEFINITION",
        sentences=[
            # the post's own sentence: the lead-in, then the quoted words.
            ("The US Securities and Exchange Commission defines it as a fraud that",
             "pays existing investors with money from new ones."),
            ("In 1920, Charles Ponzi promised fifty percent in forty-five days.",),
            # espeak reads Madoff MAD-off; the spoken half says MAY-doff.
            # who he was, before what he did (the editor: "we throw the
            # name very random")
            (("Bernie Madoff was a former chairman of the Nasdaq stock market, with a Wall Street firm he'd run since 1960.",
              "Bernie Maydoff was a former chairman of the Nasdaq stock market, with a Wall Street firm he'd run since 1960."),),
            ("His clients' statements showed sixty-four point eight billion dollars that never existed.",),
            ("And in crypto, BitConnect promised profits from a trading bot, and took about two point four billion dollars.",),
            # the beat's own sentence: in, out, the collapse.
            ("Every one runs the same way. New investors pay in,",
             "the operator pays earlier investors their returns out of that money,",
             "and when the new money stops, so do the payouts."),
        ],
        shots=[
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("headline",
                          {"source": "US Securities and Exchange Commission",
                           "date": "Investor.gov - Ponzi Scheme",
                           "headline": "A Ponzi scheme is an investment fraud "
                                       "that [pays existing investors with funds "
                                       "collected from new investors.]"},
                          "THE DEFINITION")),
            Shot(image=PONZI, name="Charles Ponzi · 1920",
                 note=("50%", "promised in 45 days")),
            # the cut-out: NASDAQ read whole, then tucked behind his head
            Shot(graphic="behind",
                 payload=(MADOFF_WIDE, "NASDAQ", "Bernie Madoff - former Nasdaq chairman")),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("$64.8B", "on Madoff's clients' statements",
                          "November 2008 - money that never existed")),
            Shot(clip=DOJ_AMOUNT, clip_at=0.0, window=("browser", DOJ_ADDR)),
            _ponzi("ponzi"),
        ],
        gaps=[1.00, 0.60, 0.60, 0.70, 1.70, 1.60],
    ),

    # --- the check -------------------------------------------------------------
    Section(
        title="Does Bitcoin fit the definition?",
        spoken_title="So does Bitcoin actually fit that definition?",
        kicker="THE CHECK",
        card_gap=1.30,
        sentences=[
            ("Actually, there's nobody in the middle of Bitcoin.",),
            # the beat's own sentence: the trade, then the empty middle.
            ("When you buy, your dollars go to whoever sold to you,",
             "nobody holds a pot of everyone's money,",
             "and nobody promises you a return."),
            ("And every one of those trades sits on a public ledger that anyone can read.",),
            ("New coins don't go to early investors either. They go to miners, as pay for securing the network.",),
            ("The 2008 paper that started it describes",
             "a peer-to-peer electronic cash system."),
            ("A Ponzi collapses when new money stops, because the payouts stop.",),
            ("Bitcoin has no payouts to stop.",),
        ],
        shots=[
            # the operator's job, crossed out
            Shot(clip=STACKS, clip_at=1.0, shader="aberration",
                 verdict=("wrong", "NO OPERATOR"), verdict_at=0.35),
            _ponzi("market"),
            Shot(clip=LEDGER, clip_at=0.0, window=("browser", BLOCK_ADDR)),
            Shot(clip=BLOCK, clip_at=0.0, window=("browser", BLOCK_ADDR)),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("headline",
                          {"source": "Satoshi Nakamoto", "date": "31 October 2008",
                           "headline": "Bitcoin: [A Peer-to-Peer Electronic "
                                       "Cash System]"},
                          "THE PAPER")),
            Shot(clip=USD1, clip_at=4.0),
            # the editor's "custom screen of moving bitcoins": wallet to
            # wallet, nobody in the middle (`peers`, new). It sat under the
            # closing line first, where the end card covers it.
            Shot(graphic="peers", ground="grid", payload=("", "NO PAYOUTS TO STOP")),
        ],
        gaps=[0.70, 1.60, 0.60, 2.30, 1.00, 0.60, 0.90],
    ),

    # --- what the sceptics get right -------------------------------------------
    Section(
        title="What are the sceptics right about?",
        spoken_title="So what are the sceptics right about?",
        kicker="THE TRUE PART",
        sentences=[
            ("But their real point survives.",),
            ("Bitcoin pays you nothing while you hold it. No interest, no dividend, no rent.",),
            ("In 2018, Warren Buffett put it this way:",
             "the asset itself is creating nothing."),
            ("So the only way to sell it for more is to find someone who'll pay more.",),
            ("That makes it speculation, like gold. It doesn't make it a Ponzi.",),
            ("And real Ponzi schemes do hide inside crypto. BitConnect was one.",),
            ("OneCoin took about four billion dollars, and never even had a blockchain.",),
            # the checklist's own sentence: one chunk per claim.
            # each item says its verdict, so each is struck as it is said
            # (`flow=True`) - the editor: list, strike, list, strike
            ("Someone in the middle holding the money? No.",
             "A promised return? No.",
             "Old investors paid with new money? No.",
             "Gains that need the next buyer? Yes."),
            ("Nothing in this video is financial advice.",),
            ("So, is Ponzi the right word for Bitcoin, or just the easiest one?",),
        ],
        shots=[
            Shot(clip=DESK, clip_at=1.0),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("$0", "paid to you for holding Bitcoin",
                          "no interest, no dividend, no rent")),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("post",
                          {"name": "Warren Buffett", "handle": "CNBC, Squawk Box",
                           "date": "7 May 2018",
                           "text": "[The asset itself is creating nothing.]"},
                          "THE SCEPTIC")),
            Shot(clip=FAN100, clip_at=0.5,
                 window=("player", "Sold for more - to a later buyer")),
            Shot(clip=DESK, clip_at=7.0),
            Shot(clip=DOJ_PONZI, clip_at=0.0, window=("browser", DOJ_ADDR)),
            None,
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Someone holds the money", False),
                           ("A promised return", False),
                           ("Paid with new money", False),
                           ("Gains need the next buyer", True)],
                          "THE CLAIM, CHECKED", True)),
            # The video's own subject, not weather (2026-11-06).
            Shot(clip=DISCLAIMER_BG, clip_at=0.0,
                 payload=("", "This is not financial advice.")),
            # the opening clip again, under the end card
            Shot(clip=USD20, clip_at=2.5),
        ],
        gaps=[0.70, 0.90, 1.00, 0.80, 0.90, 0.50, 0.80, 1.40, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="Is Bitcoin a Ponzi Scheme? The Definition, Checked",
    hook="People call Bitcoin a Ponzi scheme: early buyers getting rich off "
         "the ones who come later. Part of that is true - but a Ponzi scheme "
         "needs three things, and Bitcoin is missing two of them. The SEC's "
         "definition, checked against how Bitcoin actually works.",
    url=URL,
    summary="Is Bitcoin a Ponzi scheme? The SEC defines a Ponzi as a fraud "
            "that pays existing investors with money from new ones - Charles "
            "Ponzi's 50% in 45 days, Madoff's $64.8 billion of statements, "
            "BitConnect's $2.4 billion. Every one has someone in the middle "
            "holding the money, a promised return, and payouts that stop when "
            "new money stops. Bitcoin has nobody in the middle: your dollars "
            "go to whoever sold to you, new coins go to miners for securing "
            "the network, and the 2008 paper promises a payment system, not a "
            "return. What the sceptics get right: Bitcoin pays nothing while "
            "you hold it, so the only way to sell for more is a later buyer "
            "paying more - speculation, not a Ponzi. Real Ponzi schemes do "
            "hide inside crypto. Nothing here is financial advice.",
    tags=["is bitcoin a ponzi scheme", "bitcoin ponzi scheme", "is crypto a ponzi scheme",
          "is bitcoin a scam", "bitcoin ponzi", "ponzi scheme explained",
          "what is a ponzi scheme", "bitcoin explained", "bitconnect",
          "bernie madoff", "warren buffett bitcoin", "ben mckenzie crypto",
          "is bitcoin real", "bitcoin skeptic"],
    cta=f"How Bitcoin actually works, in plain English - the ledger, mining, "
        f"the 21 million cap and where new coins come from: {URL}",
    credits=["Nothing in this video is financial advice.",
             "Pages: US Department of "
             "Justice, \"BitConnect Founder Indicted in Global $2.4 Billion "
             "Cryptocurrency Scheme\" (25 Feb 2022); mempool.space block "
             "explorer - captured 25 Nov 2026.",
             "Quotes: US SEC, Investor.gov, \"Ponzi Scheme\"; Ben McKenzie, testimony to the US Senate Committee on "
             "Banking, Housing, and Urban Affairs, 14 Dec 2022; Warren "
             "Buffett, CNBC Squawk Box, 7 May 2018; Satoshi Nakamoto, "
             "\"Bitcoin: A Peer-to-Peer Electronic Cash System\" (2008).",
             "Figures: US Postal Inspection Service (Ponzi, 1920); SIPC "
             "trustee filings (Madoff, Nov 2008 statements).",
             "Photos: Charles Ponzi and Bernie Madoff, public domain "
             "(Wikimedia Commons)."],
)

# Covers (`thumbnails.md`). The search's top 12 (pulled 2026-11-25) share a
# gold Bitcoin coin (7 of 12), a face - a presenter or a famous sceptic (7)
# - and one caps word on red; none shows the real ones side by side. Three
# directions were drawn - the line-up, Charles Ponzi cut out under "Who Pays
# Your [Returns?]", and the `ponzi` beat's empty middle - and the editor
# picked the line-up (2026-11-25); the other two were deleted. First use of
# `thumb.lineup_cover` on a real video (`vector`).
COVERS = ("lineup",)
COVER_HEADLINES = {"lineup": ["Ponzi.", "Madoff.", "[Bitcoin?]"]}
HEADLINE = "\n".join(COVER_HEADLINES[COVERS[0]])
PONZI_MUG = BP / "charles-ponzi-mug.jpg"
BTC_LOGO = BP / "bitcoin-logo.png"


def _cut(src, box=None):
    import numpy as np
    from PIL import Image
    from video_automation.core import vision
    im = Image.open(src).convert("RGB")
    if box:
        w, h = im.size
        im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    im.thumbnail((1800, 1800))
    c = Image.fromarray(np.asarray(vision.cutout(im)).copy())
    return c.crop(c.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox())


def cover(kind: str, portrait: bool = False):
    """One cover, 1280x720 or (`portrait`) 1080x1920, as an RGB image: Ponzi's
    own 1910 mug shot, Madoff's 2009 one and the Bitcoin logo on the line-up
    wall. A Short's cover keeps type and plates inside y 240-1680
    (`thumb.SAFE_TOP`)."""
    from PIL import Image
    from video_automation.longform import thumb as T
    if kind != "lineup":
        raise ValueError(f"unknown cover {kind!r} - {COVERS}")
    W, H = (1080, 1920) if portrait else (1280, 720)
    head = COVER_HEADLINES[kind]
    mug = _cut(PONZI_MUG, (0.52, 0.0, 1.0, 1.0))
    mad = _cut(MADOFF)
    btc = Image.open(BTC_LOGO).convert("RGBA")
    btc = btc.crop(btc.getchannel("A").getbbox())
    if portrait:
        # narrower than the 16:9 wall: three cut-outs at full height overlap
        # on 1080 px
        wall = T.lineup_cover([(mug, 0.44), (mad, 0.44), (btc, 0.27)], "",
                              portrait=True, rows=[])
        # lifted 150 px so the numbered plates sit inside TikTok's 3:4 band
        im = Image.new("RGB", (W, H), (14, 14, 18))
        im.paste(wall, (0, -150))
        T.stack_headline(im, head, (70, 260, W - 140, 470), accent="yellow")
        return im
    im = T.lineup_cover([(mug, 0.92), (mad, 0.92), (btc, 0.45)], " ", portrait=False)
    T.stack_headline(im, ["Ponzi. Madoff. [Bitcoin?]"], (40, 24, W - 80, 170),
                     accent="yellow")
    return im


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
    stillclip.make(PONZI, focus=(0.5, 0.35))
    out = Path.home() / "Desktop/bitcoin-ponzi-long.mp4"
    work = Path.home() / "Desktop/.bitcoin-ponzi-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        opener=Search("is bitcoin a ponzi scheme", centre_y=0.30),
        emphasis=["nobody in the middle", "creating nothing"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))[0]
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv or "--thumb-variants" in sys.argv:
        for p in thumbs(Path.home() / "Desktop/bitcoin-ponzi-long-thumb.jpg",
                        variants="--thumb-variants" in sys.argv):
            print(p)
    else:
        main()
