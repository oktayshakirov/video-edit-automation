"""What are prediction markets? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-are-prediction-markets.mdx.

**The angle.** Both standouts on this subject (Coinsider's "What is
Polymarket?", Art of the Problem's "The Polymarket Paradox") earn their
replays on one mechanism: a share that pays a dollar, so its price is a
probability. Their comments then ask for what neither gives - where the
number is wrong, and who decides what happened
(`demand/teardowns/what-are-prediction-markets.md`). So the video walks the
share, why its price becomes the odds, who settles the answer, the March 2025
Ukraine minerals market that settled against the facts, and when not to
trust the odds. The close echoes the open: a price that is the crowd's guess,
and a vote that decides what the future was.

**A mechanism piece, so the default arc** (`projects/crypto.md`), with one
dated event as the turn.

**No financial advice.** No platform is rated and no live market's odds are
quoted. Polymarket is named because it is the example the viewer has heard
of; its 2022 fine and 2025 return are regulatory facts, not a verdict. "A
whale" is what users alleged, so the voice says users blamed one holder.

**Figures, all checked.** $1 / $0 shares and "62 cents means 62%" (the
article). Polymarket's own card: Yes 51c / No 49c, 51%
(polymarket.com/images/homepage-twitter-card.png). Resolution through UMA's
optimistic oracle: a proposal with a bond, typically $750; a 2-hour
challenge window; a dispute goes to a UMA token-holder vote of about 48
hours, weighted by tokens held (docs.polymarket.com/concepts/resolution).
Proposers limited to a whitelist since August 2025 (UMIP-189). The Ukraine
market: about $7M, "before April", 9% to 100% on 24-25 March 2025, resolved
Yes with no deal agreed; a Polymarket team member on Discord: "This is an
unprecedented situation."; no refunds, as not a market failure (CoinMarketCap
Academy, The Defiant, CryptoSlate). The deal was signed on 30 April 2025.
CFTC order, 3 January 2022: $1.4M civil penalty (Release 8478-22). CFTC
approval for a US return, November 2025.

**Spoken around:** `UMA` reads OO-ma, so the voice says "Yuma".

## The beats

Last three crypto long forms: north-korea-crypto (blindsign / timeline /
post / grid / reel), crypto-when-you-die (bars / reel / checklist / quorum /
post), what-are-memecoins (compare / stat / steps / pool / grid).

* `shares` - **new, built for this video.** One question, a $1 coin that
  splits into YES and NO, the price bar filling to 62/38, the price turning
  into 62%, then the outcome. The library could not draw a price becoming a
  probability, and it is the topic's whole mechanism.
* Polymarket's own odds card, straight after, as an inset over a dark
  clip: the real thing showing the same split.
* `diagram` - the resolution flow: propose, challenge, vote.
* `post` - the Polymarket team member's own words on the Ukraine market.
* `checklist` - the three times the odds lie, titled as the question its
  crosses answer ("TRUST THE ODDS?"): under "WHEN THE ODDS LIE" the strikes
  read as "not a thin market".

**Opener: `Counter`** on 62%. The last two long forms opened `Search`, so a
third is out; the payoff of the hook is a number.

**Footage: the act** - thumbs on trading apps, chart monitors, a crowd at a
screen, a typewriter printing BREAKING NEWS, a clock for the challenge
window, a ballot going in, Kyiv and an open quarry for the minerals market.
Every clip fetched fresh; verdicts in `footage.md`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/prediction-markets.py
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

SOURCE_POST = "what-are-prediction-markets"
DEMAND = ("Coinsider 'What is Polymarket? The Ultimate Prediction Market' 108k, "
          "31.4x; Art of the Problem 'The Polymarket Paradox' 776k; "
          "DGFantasy 'Prediction Markets for Dummies' 25k, 104x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"
PRESS = STOCK / "press/polymarket"

# Fetched fresh for this pair, contact-sheeted at 15/50/85%. Luma sampled at
# 0.5/3/6/9s.
APP = V / "stock-trading-app-phone-dark/7681176.mp4"            # 29s, L95-100, two hands on a phone trading app - opens both cuts
FINGER = V / "stock-trading-app-phone-dark/34473008.mp4"        # 15s, L75-80, a finger on a candle chart, monitors behind
CHARTS = V / "trading-charts-monitor-dark/38736275.mp4"         # 21s, L12, candle charts on a monitor in the dark
CHARTS2 = V / "trading-charts-monitor-dark/38771102.mp4"        # 21s, L18, one line chart, purple light
TYPE = V / "newspaper-headlines/2752278.mp4"                    # 16s, L83, a typewriter printing BREAKING NEWS
SCROLL = V / "reading-news-on-phone-at-night/35888104.mp4"      # 19s, L47-64, a thumb scrolling a news feed
BED = V / "reading-news-on-phone-at-night/7986973.mp4"          # 11s, L41-44, a woman reading her phone under a blanket
CROWD = V / "crowd-watching-big-screen-night/7986778.mp4"       # 17s, L17, an audience lit by a screen
STADIUM = V / "stadium-crowd-night-lights/34671875.mp4"         # 11s, L71-80, a stadium crowd at night
BUTTONS = V / "election-results-tv-night/7103542.mp4"           # 11s, L85, VOTE / I AM A VOTER buttons on a table
BALLOT = V / "voting-ballot-box/7103424.mp4"                    # 13s, L112-136, a ballot going into a box - bright, but the noun
KYIV = V / "kyiv-city-night/12399500.mp4"                       # 32s, L99-107, Kyiv and the Dnipro from above, dusk
QUARRY = V / "raw-minerals-ore-rocks/31100164.mp4"              # 33s, L126, an open quarry from above - the minerals
SIGN = V / "signing-document-pen-close-up/5778854.mp4"          # 7s,  L105-114, a pen signing a contract
CLOCK = V / "clock-ticking-dark-close-up/7033779.mp4"           # 16s, L25-33, an alarm clock on black
HOURGLASS = V / "hourglass-sand-dark/37223275.mp4"              # 31s, L85, three hourglasses running
HANDS = V / "business-people-shaking-hands/5977121.mp4"         # 9s,  L118-130, a handshake outside an office tower - bright, but the approval
THINK = V / "person-thinking-laptop-night/30445082.mp4"         # 14s, L37, a man weighing something at his laptop
RAIN = V / "rain-on-window-night/5930874.mp4"                   # 25s, L42 at 0.5s, rain on glass, lights beyond - the one abstract

ODDS = PRESS / "card-odds-panel.png"       # 1200x528, Polymarket's own card: "Will ___ happen this year? 51%, Yes 51c, No 49c"
LOGO = PRESS / "logos/logo-white.png"      # 911x168 RGBA, Polymarket's official wordmark

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-are-prediction-markets"

DISCORD = {"name": "A Polymarket team member", "handle": "on Discord",
           "date": "25 March 2025",
           "text": "This is an [unprecedented situation]."}


SECTIONS = [
    # --- hook. No card. The Counter lands on "sixty-two". -------------------
    Section(
        title="What are prediction markets?",
        card=False,
        sentences=[
            ("A prediction market sells you a share in something that has not happened yet.",),
            ("If that share costs sixty-two cents,",
             "the crowd is saying sixty-two percent."),
            ("Not a pundit, not a poll.",
             "People paying to be right."),
            ("But a price cannot say what actually happened.",
             "Somebody still has to decide that."),
            ("In March 2025, on a seven million dollar market,",
             "that decision went against the facts."),
            ("Stay to the end, and you will know how to read the odds,",
             "and when not to trust them."),
        ],
        shots=[
            Shot(clip=APP, clip_at=1.0),
            Shot(clip=FINGER, clip_at=1.0),
            Shot(clip=CROWD, clip_at=1.0),
            Shot(clip=BALLOT, clip_at=4.0),
            Shot(clip=KYIV, clip_at=2.0),
            Shot(clip=CHARTS, clip_at=1.0),
        ],
        gaps=[0.55, 0.80, 0.85, 0.70, 0.85, 0.90],
    ),

    # --- the share --------------------------------------------------------------
    Section(
        title="How does a prediction market work?",
        spoken_title="So how does a prediction market actually work?",
        kicker="THE SHARE",
        sentences=[
            ("Take Polymarket, the biggest crypto prediction market.",
             "Every market there is one question, with a deadline."),
            # the shares beat's own sentence: one chunk per reveal.
            ("Each share in it is worth one dollar, or nothing.",
             "It comes as a pair, one for yes and one for no.",
             "If yes trades at sixty-two cents, no costs about thirty-eight.",
             "So the crowd puts the odds at sixty-two percent.",
             "And at the deadline, the right side pays a dollar, and the wrong side pays nothing."),
            ("Polymarket's own card shows it the same way.",
             "Fifty-one cents for yes means fifty-one percent."),
            ("And you never have to wait for the deadline.",
             "You can sell your share whenever the price moves."),
        ],
        shots=[
            Shot(clip=HOURGLASS, clip_at=12.0, inset=(LOGO, "tr", 0.14)),
            Shot(graphic="shares", backdrop=BEATGROUND,
                 payload=("Will it happen by 31 December?", 62,
                          "ONE QUESTION", "YES")),
            # An inset over a dark clip, not a full-bleed still: the card is
            # white, and full-frame it was the brightest frame in the video.
            Shot(clip=BED, clip_at=3.0, inset=(ODDS, "right", 0.46)),
            Shot(clip=APP, clip_at=12.0),
        ],
        gaps=[0.70, 1.80, 0.80, 0.90],
    ),

    # --- the crowd --------------------------------------------------------------
    Section(
        title="Why would a price be the odds?",
        spoken_title="But why would a price be the odds at all?",
        kicker="THE CROWD",
        sentences=[
            ("Because anyone who thinks the price is wrong",
             "can make money correcting it."),
            ("If you think the real chance is eighty percent,",
             "a sixty-two cent share looks cheap. So you buy it."),
            ("Buying pushes the price up,",
             "until nobody thinks it is cheap any more."),
            ("Every piece of news does the same.",
             "Money moves, and the price follows."),
            ("So the odds are not anyone's opinion.",
             "They are what the opinions are worth, once they are paid for."),
        ],
        shots=[
            Shot(clip=THINK, clip_at=1.0),
            Shot(clip=FINGER, clip_at=8.0),
            Shot(clip=CHARTS2, clip_at=2.0),
            Shot(clip=TYPE, clip_at=4.0),
            Shot(clip=STADIUM, clip_at=1.0),
        ],
        gaps=[0.55, 0.70, 0.70, 0.70, 0.90],
    ),

    # --- the oracle -------------------------------------------------------------
    Section(
        title="Who decides what happened?",
        spoken_title="So who decides what actually happened?",
        kicker="THE ORACLE",
        sentences=[
            ("Not Polymarket, and not a judge.",),
            (("It uses an oracle, a system that brings a real-world answer onto the blockchain, called UMA.",
              "It uses an oracle, a system that brings a real-world answer onto the blockchain, called Yuma."),),
            # the diagram's own sentence: one chunk per node.
            ("First, someone proposes the answer, and puts down a bond, usually seven hundred and fifty dollars.",
             "Then anyone has two hours to challenge it.",
             ("If someone does, holders of the UMA token vote on the answer.",
              "If someone does, holders of the Yuma token vote on the answer.")),
            ("And the more tokens you hold,",
             "the more your vote counts."),
        ],
        shots=[
            Shot(clip=CHARTS, clip_at=9.0),
            Shot(clip=SCROLL, clip_at=1.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("Proposed", "an answer, and a $750 bond"),
                           ("Challenged", "anyone, within two hours"),
                           ("Voted", "by UMA token holders")],
                          "WHO SETTLES IT")),
            Shot(clip=BUTTONS, clip_at=1.0),
        ],
        gaps=[0.55, 0.70, 1.20, 0.90],
    ),

    # --- the dispute ------------------------------------------------------------
    # The turning point, so the card gets the longer silence.
    Section(
        title="What happens when the vote is wrong?",
        spoken_title="So what happens when the vote gets it wrong?",
        kicker="THE DISPUTE",
        card_gap=1.30,
        sentences=[
            ("In March 2025, a seven million dollar market asked one question.",
             "Would Ukraine agree to a minerals deal with Trump before April?"),
            ("In two days, the yes price climbed from nine percent to a hundred.",),
            ("And the market resolved yes.",
             "No deal had been agreed."),
            ("Users blamed one large holder of UMA tokens,",
             "for swinging the vote."),
            # the post: the lead-in, then the quote.
            ("Polymarket's own team called it",
             "an unprecedented situation."),
            ("But it refunded nothing.",
             "The market had not failed. It had followed its own rules."),
            ("The deal was signed at the end of April.",
             "A month too late."),
        ],
        shots=[
            Shot(clip=QUARRY, clip_at=2.0),
            Shot(clip=CHARTS2, clip_at=12.0, note=("9% → 100%", "in two days, 24-25 March 2025")),
            Shot(clip=KYIV, clip_at=14.0),
            Shot(clip=BALLOT, clip_at=7.0),
            Shot(graphic="post", backdrop=BEATGROUND,
                 payload=("post", DISCORD, "")),
            Shot(clip=CLOCK, clip_at=2.0),
            Shot(clip=SIGN, clip_at=0.5),
        ],
        gaps=[0.70, 0.70, 0.85, 0.70, 1.10, 0.80, 0.90],
    ),

    # --- the catch --------------------------------------------------------------
    Section(
        title="When should you not trust the odds?",
        spoken_title="So when should you not trust the odds?",
        kicker="THE CATCH",
        sentences=[
            ("A price is only as good as three things behind it.",),
            # the checklist's own sentence: one chunk per item.
            ("A market so thin that one big trade can swing it.",
             "A question vague enough to argue about.",
             "And an answer that a vote can still get wrong."),
            ("So before you read a price as the odds,",
             "check how much is traded, read the rules, and see who decides."),
            ("And check where you live.",
             "Polymarket itself paid a one point four million dollar fine in the US in 2022."),
            ("It only came back there with federal approval in late 2025.",),
        ],
        shots=[
            Shot(clip=HOURGLASS, clip_at=2.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("A thin market", False),
                           ("A vague question", False),
                           ("A disputed answer", False)],
                          "TRUST THE ODDS?", True)),
            Shot(clip=THINK, clip_at=6.0),
            Shot(clip=BED, clip_at=1.0,
                 note=("$1.4M", "the CFTC's fine, January 2022")),
            Shot(clip=HANDS, clip_at=1.0),
        ],
        gaps=[0.55, 2.20, 0.80, 0.60, 0.90],
    ),

    # --- close: the echo --------------------------------------------------------
    Section(
        title="So what is a prediction market?",
        spoken_title="So, what is a prediction market?",
        kicker="THE ANSWER",
        sentences=[
            ("A price that is the crowd's guess about the future,",
             "and a vote that decides what the future was."),
            ("Nothing in this video is financial advice.",),
            ("So, the next time a headline quotes the odds,",
             "would you check who decides the answer?"),
        ],
        shots=[
            Shot(clip=CROWD, clip_at=9.0),
            Shot(clip=RAIN, clip_at=0.3,
                 payload=("", "This is not financial advice.")),
            Shot(clip=TYPE, clip_at=7.5),
        ],
        gaps=[0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Are Prediction Markets? How Polymarket Odds Really Work",
    hook="A prediction market sells you a share in something that has not "
         "happened yet, and its price is the crowd's odds. Here is how the "
         "shares work, why a price becomes a probability, who decides what "
         "actually happened, the 2025 Polymarket market that settled against "
         "the facts, and when not to trust the odds.",
    url=URL,
    summary="What prediction markets are and how they work: YES and NO shares "
            "that pay one dollar or nothing, why a 62-cent share means a 62% "
            "chance, and why traders who disagree with the price push it toward "
            "the crowd's estimate; how Polymarket settles a market through UMA's "
            "optimistic oracle - a proposed answer with a bond, a two-hour "
            "challenge window and a token-holder vote; the March 2025 Ukraine "
            "minerals-deal market that resolved Yes with no deal agreed; when "
            "the odds are least reliable - thin markets, vague questions and "
            "disputed answers; and Polymarket's 2022 CFTC fine and 2025 US "
            "return. Nothing here is financial advice.",
    tags=["what are prediction markets", "prediction markets explained",
          "how does polymarket work", "polymarket explained", "polymarket odds",
          "prediction market odds", "uma oracle", "polymarket ukraine market",
          "crypto prediction markets",
          "what is polymarket", "how prediction markets work"],
    cta=f"How the shares, AMMs and oracles work, every risk, and a safe first workflow: {URL}",
    credits=["Polymarket logo and odds card: Polymarket's own brand assets, "
             "shown for commentary.",
             "Nothing in this video is financial advice."],
)

HEADLINE = "What are\nprediction\n[markets?]"


def thumbs(out: Path) -> Path:
    """The `shares` card at its turn - YES at 62% on the bar, NO at 38c -
    on the right over the beat's own water, Polymarket's white wordmark over
    the title's question in four rows on the left. No person: the video has
    none (`thumbnails.md`). Forced rows widen their column by 1.38, so the
    column passed is the card's edge over 1.38."""
    from PIL import Image, ImageDraw, ImageFilter
    from video_automation.core.frame import LANDSCAPE
    from video_automation.longform import thumb as T
    from video_automation.longform.beats import Shares
    b = Shares("Will it happen by 31 December?", 62, "", None, brand=CRYPTO,
               frame=LANDSCAPE, backdrop=BEATGROUND,
               reveals=[0.0, 1.0, 2.0, 3.4], start=0.0, hold=5.0)
    full = b.draw(1.0)
    x0 = (1920 - b.card_w) // 2 - 30
    card = full.crop((x0, b.card_y - 30, x0 + b.card_w + 60, b.bar_y + b.bar_h + 110))
    cw = 640
    card = card.resize((cw, int(card.height * cw / card.width)), Image.LANCZOS)
    im = Image.open(BEATGROUND).convert("RGB").resize((1280, 720), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * 0.45))
    x, y = 1280 - cw - 24, (720 - card.height) // 2 + 20
    shape = Image.new("L", card.size, 0)
    ImageDraw.Draw(shape).rounded_rectangle([1, 1, card.width - 2, card.height - 2],
                                            radius=18, fill=255)
    im.paste(card, (x, y), shape)
    logo = Image.open(LOGO).convert("RGBA")
    lw = 300
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.paste(logo, (40, 44), logo)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 180, int((x - 70) / 1.38), 34, fill, ink,
                max_lines=4, leading=1.0, band="middle", margin=34,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/prediction-markets-long.mp4"
    work = Path.home() / "Desktop/.prediction-markets-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The last two long forms opened Search; the hook's payoff is a number.
        opener=Counter("62%", "WHAT A 62¢ SHARE IS SAYING",
                       at_word="sixty-two", centre_y=0.30),
        emphasis=["paid for", "followed its own rules"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=12.5, title_hold=5.4,
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/prediction-markets-long-thumb.jpg"))
    else:
        main()
