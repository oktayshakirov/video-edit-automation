"""Tokenized stocks - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-are-tokenized-stocks.mdx - its two
models (fully backed, synthetic), what you actually own, the weekend
discount case, and the 2026 SEC exemption.

**The angle.** The sceptic's question, which is the one that stands out on
this search: Finance Simply Explained "Tokenized Stocks Are Back: Do You
Really Own the Shares?" 9.1x, beside Kraken's launch explainer at 32.4x
whose 19 comments are almost all questions it left open - dividends, "how
does it work?", who audits the issuer (`demand/teardowns/what-are-
tokenized-stocks.md`). The failures beside them are a verdict ("finally
worth it"), a platform guide and a plain definition. So the title is the
search plus the ownership question, and the video never says whether to buy
one.

**A mechanism, so the default arc** (`longform.md`); the turn is the
shareholder chapter ("Actually, usually not"), and the climax is OpenAI's
public "not OpenAI equity" post on Robinhood's tokens.

**Every figure is sourced.** Robinhood's help page ("you are not buying the
actual stocks", captured 2026-11-07); Kraken's xStocks disclosure ("price
exposure without shareholder rights such as voting", the description of its
own explainer, 2025-06-30); OpenAI Newsroom on X, 2 Jul 2025; Robinhood's
answer (its stake in a special purpose vehicle) per CNBC and TechCrunch;
Binance's stock tokens, launched April 2021, sales stopped 16 Jul 2021
(Cointelegraph); CNBC, 17 Sep 2026, on the SEC's five-year exemption, whose
conditions (same rights as the share, issuer can object) are from the
Sullivan & Cromwell memo and Reuters via Wealth Professional. **The weekend
chart is the article's own illustrative case** (token down 15%, share opens
down 7%) and is said as "imagine" and titled IMAGINED.

## The beats

Last three crypto long forms: random-tokens-in-wallet (diagram / blindsign
/ pile / behind / lookalike / post / stat / checklist), crypto-billionaires
(reel / compare / stake / bars / stat), gta-6-crypto (timeline / quote /
checklist / diagram / chart).

* `diagram` - the backed kind's chain: shares bought, a custodian, a token
  per share, your wallet. All four icons animate (💸 🔒 🪙 📈).
* `compare` - backed against synthetic, the two kinds behind one name.
* `quote` - Kraken's own line on its backed tokens.
* `checklist` - the note card: what a backed token gives you.
* `post` - OpenAI's reply, and CNBC's headline on the SEC rule.
* `chart` - the weekend, imagined: the token falls, Monday pulls it back.
* `timeline` - Binance 2021 to the SEC in 2026, spaced by real time.

**Opener: `Split`**, TOKEN against SHARE, "SAME THING?" left open - the
whole video's question. Last three long forms opened Stamp / Search /
Stamp. The Short shares it (`shorts.md`, "A pair may share its opener").

**Real pages and pictures:** Robinhood's help page, captured
(`screencap`, ringing the derivative line and the "not buying the actual
stocks" line); the site's own cover photo (hands on a tablet chart) with
`parallax`; a closed "Market lane" for the shut exchange.

**Footage: the act and the place** - hands on a stock app, a market heat
map, a chart in the dark, the NYSE, an empty street at dawn, paperwork, a
padlocked door, a capitol at night. Fetched fresh 2026-11-07; verdicts in
`footage.md`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/tokenized-stocks.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music, stillclip
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Split

SOURCE_POST = "what-are-tokenized-stocks"
DEMAND = ("Kraken 'Tokenized equities explained' 32.4x (13.7k); Finance Simply "
          "Explained 'Tokenized Stocks Are Back: Do You Really Own the "
          "Shares?' 9.1x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
POSTS = _P.home() / "Coding/crypto-wiki/public/images/posts"

# Fetched fresh for this pair (2026-11-07), contact-sheeted at 15/50/85%,
# luma at 0.5/3/6/9s. None is used by another video.
APP = V / "investing-app-phone-hands-night/34453449.mp4"               # 10s, L64-80, a finger on a stock app, charts behind - buying one
HEATMAP = V / "nasdaq-times-square-night/38905686.mp4"                 # 27s, L55-68, a market heat map of real tickers - a company's share
NIGHTCHART = V / "nasdaq-times-square-night/38841404.mp4"              # 21s, L18, a price chart on a monitor in the dark
TABLET = V / "stock-market-closed-sign/39416191.mp4"                   # 26s, L20, a candlestick chart on a tablet, red and green behind
NODES = V / "gold-network-nodes-dark-abstract/35002501.mp4"            # 10s, L34, white nodes and links - the blockchain (the one abstract)
CORRIDOR = V / "bank-vault-corridor-dark/7598737.mp4"                  # 10s, L12, a dark corridor to a lit end - an account you never see
DOCS = V / "legal-documents-folder-dark-desk/8061377.mp4"              # 17s, L88, a hand laying paperwork on a desk - the register
LOCKED = V / "vault-door-dark-metal/4183797.mp4"                       # 6s, L35-55, a padlocked steel door - held for you
NYSE = V / "new-york-stock-exchange-facade-night/5631778.mp4"          # 10s, L132, the NYSE facade with its flags
MARKETLANE = V / "closing-shop-shutter-night/3150371.mp4"              # 12s, L62-15, "Market lane", shutters down, into the dark - closed
DAWN = V / "empty-city-street-early-morning/39618428.mp4"              # 14s, L99, an empty shopping street at dawn - a Saturday
CAPITOL = V / "government-building-columns-night/35120905.mp4"         # 13s, L10-24, a capitol dome lit at night - the regulator
PHONEDESK = V / "buying-stocks-on-phone-app/34408391.mp4"              # 10s, L56-60, a thumb on a phone over trading monitors
INVESTING = V / "stock-app-smartphone-dark-room/7947481.mp4"           # 7s, L77, a phone showing a stock app's "Investing" balance - a retail app
BACKROOM = V / "bank-vault-corridor-dark/19217898.mp4"                 # 10s, L23-25, a dark hall to a lit doorway - what sits behind it
NIGHTSTREET = V / "closing-shop-shutter-night/36470746.mp4"            # 8s, L33-38, a city road at night, traffic passing - after hours

# The real thing: Robinhood's own help page, captured 2026-11-07
# (`screencap`, record in `captures/robinhood-stock-tokens/`). The camera
# rings "they are derivatives tracked on the blockchain", then "you are not
# buying the actual stocks".
ROBINHOOD = STOCK / "captures/robinhood-stock-tokens/line.mp4"

# The site's own cover for the post: hands on a tablet chart. 800px, so
# moved in depth rather than pushed (`parallax`), and the disclaimer's
# picture.
COVER = POSTS / "what-are-tokenized-stocks.jpg"

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-are-tokenized-stocks"

# The weekend, imagined (the article's case): flat Friday, a slide over
# Saturday and Sunday to -15%, Monday's open at -7%. Marked at the open.
WEEKEND = [100, 100.4, 99.8, 100.2, 97.5, 93.0, 89.5, 86.8, 85.6, 84.9,
           85.3, 85.0, 93.0, 93.3, 92.9]
MONDAY = 12


def _sec(s: str) -> tuple:
    """The caption keeps SEC; the voice spells it."""
    return (s, s.replace("SEC", "S E C"))


DISCLAIMER_BG = stillclip.path(COVER, focus=(0.55, 0.45))


def sections() -> list:
    return [
    # --- hook. No card. The Split asks TOKEN or SHARE. -----------------------
    Section(
        title="Tokenized stocks",
        card=False,
        sentences=[
            ("A tokenized stock lets you buy a piece of Tesla on a blockchain, at midnight.",),
            ("But the token follows Tesla's price. Whether you own any Tesla is a separate question.",),
            ("In 2025, one company had to announce that tokens of its stock were not its stock.",),
            ("So what does a tokenized stock actually give you?",),
            ("Stay to the end for the 2026 rule that changed the answer in America.",),
        ],
        shots=[
            Shot(clip=APP, clip_at=0.5),
            Shot(clip=HEATMAP, clip_at=2.0),
            Shot(clip=NIGHTCHART, clip_at=1.0),
            Shot(image=COVER, parallax=0.8),
            None,
        ],
        gaps=[0.85, 0.80, 0.70, 0.70, 0.90],
    ),

    # --- what it is --------------------------------------------------------------
    Section(
        title="What is a tokenized stock?",
        spoken_title="So what is a tokenized stock?",
        kicker="THE WRAPPER",
        sentences=[
            ("It is a token on a blockchain whose price tracks one company's share.",),
            ("You can hold it in a crypto wallet, buy a tiny fraction of it, and trade it when the stock market is closed.",),
            ("Here is how the backed kind is built.",),
            # the diagram's own sentence: one chunk per box.
            ("An issuer buys real shares,",
             "a custodian holds them in an account,",
             "a token is issued for each one,",
             "and the token lands in your wallet."),
        ],
        shots=[
            Shot(clip=TABLET, clip_at=1.0),
            Shot(clip=NIGHTSTREET, clip_at=0.5),
            Shot(clip=NODES, clip_at=1.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("Real shares", "bought by an issuer", "\U0001F4B8"),
                           ("A custodian", "holds them in an account", "\U0001F512"),
                           ("One token per share", "issued on a blockchain", "\U0001FA99"),
                           ("Your wallet", "the token follows the price", "\U0001F4C8")],
                          "THE BACKED KIND", False)),
        ],
        gaps=[0.55, 0.70, 0.55, 1.40],
    ),

    # --- two kinds ---------------------------------------------------------------
    Section(
        title="Is there always a share behind it?",
        spoken_title="But is there always a share behind it?",
        kicker="TWO KINDS",
        sentences=[
            ("Not always.",),
            ("Two kinds of token can sit behind the same name, and in an app they look identical.",),
            # the compare's own sentence: a hinge chunk per column, one per item.
            ("Take a backed token first.",
             "Real shares, held by a custodian.",
             "One token for every share.",
             "Sometimes, you can swap it for the share.",
             "Now compare a synthetic one.",
             "No shares anywhere.",
             "A contract that copies the price.",
             "And only the issuer's promise behind it."),
            ("Both go up when Tesla goes up. Only one has a Tesla share anywhere behind it.",),
            # the capture: the ring moves from "derivatives" to the line read.
            ("Robinhood's own help page calls its stock tokens derivatives, and says buyers are not buying the actual stocks.",),
        ],
        shots=[
            Shot(clip=MARKETLANE, clip_at=0.5),
            Shot(clip=PHONEDESK, clip_at=0.5),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("BACKED",
                          ["Real shares, at a custodian", "One token per share",
                           "Sometimes swaps for the share"],
                          "SYNTHETIC",
                          ["No shares anywhere", "A contract copying the price",
                           "The issuer's promise"],
                          True)),
            Shot(clip=NIGHTCHART, clip_at=9.0),
            Shot(clip=ROBINHOOD, clip_at=0.0),
        ],
        gaps=[1.10, 0.70, 1.40, 0.90, 0.90],
    ),

    # --- the turn: the backed kind ------------------------------------------------
    Section(
        title="Does the backed kind make you a shareholder?",
        spoken_title="So does the backed kind make you a shareholder?",
        kicker="THE CLAIM",
        card_gap=1.30,
        sentences=[
            ("Actually, usually not.",),
            ("The company's list of shareholders shows the custodian, not you.",),
            ("Your token is a claim on whoever holds the share for you.",),
            ("Kraken describes its own backed tokens as price exposure without shareholder rights such as voting.",),
            ("So here is what a backed token usually gives you.",),
            # the checklist's own sentence: one chunk per row, verdicts as said.
            ("The share's price, yes.",
             "Dividends, usually, paid by the issuer as more tokens or a stablecoin.",
             "A vote at the company, no.",
             "And your name on the register, no."),
        ],
        shots=[
            Shot(clip=LOCKED, clip_at=0.0, shader="aberration"),
            Shot(clip=DOCS, clip_at=1.0),
            None,
            Shot(graphic="quote", backdrop=BEATGROUND,
                 payload=("Price exposure without shareholder rights such as voting.",
                          "Kraken, on its xStocks")),
            Shot(clip=TABLET, clip_at=12.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("The share's price", True),
                           ("Dividends, via the issuer", True),
                           ("A vote at the company", False),
                           ("Your name on the register", False)],
                          "WHAT A BACKED TOKEN GIVES YOU", True)),
        ],
        gaps=[1.10, 0.70, 0.90, 0.90, 0.55, 2.40],
    ),

    # --- the OpenAI case -----------------------------------------------------------
    Section(
        title="Not OpenAI equity",
        spoken_title="Now take the clearest case so far.",
        kicker="THE PROOF",
        sentences=[
            ("In 2025, Robinhood sold tokens of OpenAI, whose shares are not even public.",),
            # the post's own sentence: the lead-in, then the line read.
            ("OpenAI answered in public, the same week.",
             "These OpenAI tokens are not OpenAI equity."),
            ("Robinhood said the tokens were backed by its stake in a company that held OpenAI shares.",),
            ("A claim on a company, that holds a claim on the shares.",),
        ],
        shots=[
            Shot(clip=INVESTING, clip_at=0.0),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("post",
                          {"name": "OpenAI Newsroom", "handle": "@OpenAINewsroom",
                           "date": "2 Jul 2025",
                           "text": "[These “OpenAI tokens” are not OpenAI "
                                   "equity.] We did not partner with Robinhood, "
                                   "were not involved in this, and do not "
                                   "endorse it."},
                          "")),
            Shot(clip=DOCS, clip_at=9.0),
            Shot(clip=CORRIDOR, clip_at=1.0),
        ],
        gaps=[0.70, 1.30, 0.70, 0.90],
    ),

    # --- the weekend ------------------------------------------------------------------
    Section(
        title="Who sets the price when the market is closed?",
        spoken_title="So who sets the price when the market is closed?",
        kicker="THE WEEKEND",
        sentences=[
            ("The New York Stock Exchange shuts every evening, and all weekend.",),
            ("Some tokenized stocks keep trading on a blockchain anyway, priced only by the people trading them.",),
            ("Imagine bad news breaks on a Saturday.",),
            # the chart's own sentence: the line, then the marked open.
            ("The token slides fifteen percent by Sunday night.",
             "On Monday, the real share opens down seven, and the token jumps back to meet it."),
            ("If the token can be swapped for the share, traders close that gap. If it can't, the gap waits for Monday.",),
        ],
        shots=[
            Shot(clip=NYSE, clip_at=1.0),
            Shot(clip=MARKETLANE, clip_at=4.0),
            Shot(clip=DAWN, clip_at=1.0),
            Shot(graphic="chart", backdrop=BEATGROUND,
                 payload=(WEEKEND, "A WEEKEND, IMAGINED", MONDAY,
                          "the share opens down 7%")),
            Shot(clip=PHONEDESK, clip_at=2.5),
        ],
        gaps=[0.55, 0.80, 0.70, 1.40, 0.90],
    ),

    # --- the 2026 rule ------------------------------------------------------------------
    Section(
        title="What changed in 2026?",
        spoken_title="So what changed in 2026?",
        kicker="THE NEW RULE",
        sentences=[
            ("This has been tried before.",),
            # the timeline's own sentence: one chunk per date.
            ("Binance launched stock tokens in April 2021,",
             "and stopped selling them that July.",
             "Robinhood's OpenAI tokens came in 2025.",
             _sec("And in September 2026, the SEC wrote its first rule for them.")),
            # the post's own sentence: lead-in, then the headline read.
            ("CNBC, that day:",
             _sec("SEC clears path for tokenized stocks.")),
            ("On a registered venue, a token now has to carry the same rights as the share, dividends and votes included.",),
            ("And a company can refuse to have its stock tokenized at all.",),
        ],
        shots=[
            Shot(clip=NODES, clip_at=5.0),
            Shot(graphic="timeline", backdrop=BEATGROUND,
                 payload=([("Apr 2021", "Binance launches stock tokens"),
                           ("Jul 2021", "Binance stops selling them"),
                           ("Jul 2025", "Robinhood's OpenAI tokens"),
                           ("Sep 2026", "The SEC's first rule")],
                          "STOCK TOKENS, SO FAR")),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("headline",
                          {"source": "CNBC", "date": "17 September 2026",
                           "headline": "SEC [clears path for tokenized stocks], "
                                       "bringing the market closer to 24/7 trading"},
                          "")),
            Shot(clip=CAPITOL, clip_at=1.0),
            Shot(clip=LOCKED, clip_at=0.0),   # the padlock in the light; by 2.5s it is bare steel
        ],
        gaps=[0.55, 1.40, 1.20, 0.80, 0.90],
    ),

    # --- close: the echo ----------------------------------------------------------------
    Section(
        title="So do you own the share?",
        spoken_title="So, do you own the share?",
        kicker="THE ANSWER",
        sentences=[
            ("A tokenized stock always gives you the price.",),
            ("Whether it gives you the share depends on what sits behind it, and whose name is on the register.",),
            ("Nothing in this video is financial advice.",),
            ("So, the next token that follows a stock: is there a share behind it, and whose is it?",),
        ],
        shots=[
            Shot(clip=HEATMAP, clip_at=14.0),
            Shot(clip=BACKROOM, clip_at=1.0),
            # The video's own cover photo, not weather (2026-11-06).
            Shot(clip=DISCLAIMER_BG, clip_at=0.5,
                 payload=("", "This is not financial advice.")),
            Shot(clip=APP, clip_at=1.0),
        ],
        gaps=[0.80, 1.00, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="What Are Tokenized Stocks? Do You Actually Own the Share?",
    hook="A tokenized stock lets you buy a piece of Tesla on a blockchain at "
         "midnight - but following a share's price is not the same as owning "
         "it. Here is how tokenized stocks are built, the two kinds behind "
         "one name, what a backed token does and does not give you, who sets "
         "the price when the market is closed, and the 2026 SEC rule.",
    url=URL,
    summary="Tokenized stocks, explained: a token on a blockchain whose price "
            "tracks a company's share; how the backed kind is built (an "
            "issuer buys real shares, a custodian holds them, a token per "
            "share); why some tokens are synthetic, with no shares behind "
            "them at all; Robinhood's own help page calling its stock tokens "
            "derivatives; why even a backed token usually leaves the "
            "custodian on the shareholder register, with Kraken's line on "
            "its xStocks (price exposure without shareholder rights such as "
            "voting); OpenAI's July 2025 statement that Robinhood's 'OpenAI "
            "tokens' are not OpenAI equity; who sets a token's price when "
            "the stock exchange is closed, with an imagined weekend; "
            "Binance's 2021 stock tokens; and the SEC's five-year exemption "
            "of 17 September 2026, which requires the same rights as the "
            "share and lets a company refuse. Nothing here is financial "
            "advice.",
    tags=["tokenized stocks", "what are tokenized stocks", "tokenized stocks explained",
          "stock tokens", "tokenized equities", "xstocks", "robinhood stock tokens",
          "openai tokens", "do you own the share", "synthetic stocks",
          "tokenization", "SEC innovation exemption", "24/7 stock trading",
          "real world assets"],
    cta=f"The two models side by side, and the checklist for any tokenized "
        f"stock offering: {URL}",
    credits=["Nothing in this video is financial advice.",
             "Pages and quotes: Robinhood Help Center, \"About Classic Stock "
             "Tokens\" (captured 7 Nov 2026); Kraken, xStocks disclosure "
             "(2025); OpenAI Newsroom on X, 2 Jul 2025; CNBC, 17 Sep 2026.",
             "The weekend price chart is an illustration, not real data."],
)

HEADLINE = "Do you\nown\n[this?]"

# The editor's cover picture (2026-11-08): a Tesla Supercharger's lit
# wordmark on black (Pexels 258083, `assets/crypto/tokenized-stocks/
# CREDITS.md`). The first cover - the site's hands on a tablet, "TOKEN OR
# SHARE?" - was turned down; the brief was arrows, white or red, pointing at
# something, with text.
TESLA = ROOT / "assets/crypto/tokenized-stocks/tesla-sign.jpg"


def thumbs(out: Path) -> Path:
    """The charger at full height on the left, the video's question in three
    rows on its black, a white ring round TESLA and a white arrow from the
    question to it. White, not red: a red arrow vanishes on the red charger."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(TESLA).convert("RGB")
    im = Image.new("RGB", (1280, 720), (0, 0, 0))
    im.paste(src.resize((1080, 720), Image.LANCZOS), (-100, 0))
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 200, int(500 / 1.38), 770, fill, ink,
                max_lines=3, leading=1.0, band="top", margin=48,
                shadow=12, drop=(5, 6))
    im = im.convert("RGBA")
    # the wordmark sits at x ~181-602, y ~324-382 in this placement
    # ~70px clear of the letters each side, ~55 above and below - the
    # first ring sat ~30px off them and crowded the word (2026-11-08)
    im.alpha_composite(T.ring_layer(im.size, (110, 268, 672, 438), width=10))
    im.alpha_composite(T.arrow_layer(im.size, (955, 525), (692, 402),
                                     width=18, head=54, bow=-0.30))
    im.convert("RGB").save(out, quality=92)
    return out


def main() -> None:
    stillclip.make(COVER, focus=(0.55, 0.45))
    out = Path.home() / "Desktop/tokenized-stocks-long.mp4"
    work = Path.home() / "Desktop/.tokenized-stocks-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The video's question as a comparison, left open. Last three long
        # forms opened Stamp / Search / Stamp.
        opener=Split("TOKEN", "SHARE", "SAME THING?"),
        emphasis=["separate question", "not buying the actual stocks",
                  "a claim on a company", "refuse"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=11.0, title_hold=5.4,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/tokenized-stocks-long-thumb.jpg"))
    else:
        main()
