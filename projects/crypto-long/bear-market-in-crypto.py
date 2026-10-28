"""What is a bear market in crypto - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/bear-market-in-crypto.mdx.

**The angle.** A bear market is usually explained as "prices going down". The
video's job is the two mechanisms underneath that the viewer can check: why
crypto's falls go so much deeper than the stock market's twenty percent line
(borrowed money, forced selling that feeds itself, and a market that never
pauses), and why a big rally in the middle of one is not the end of it - a
fall is measured from the top and a jump from the bottom, so a forty percent
jump after an eighty percent fall still leaves a coin seventy-two percent
down. The close echoes the open: measured from the top, not the bottom.

**No financial advice.** It describes how a fall and a rally are measured and
why forced selling cascades. It names no price level, predicts nothing, says
nothing about when a bear market ends, and recommends no action. The
article's strategy and "signals it may be ending" sections are deliberately
left out - both are the part of the post that tells a reader what to do. No
platform is named and no shot shows a chart, ticker or price; the one line
that falls is drawn, with no numbers on its axis.

**Figures.** The article's own: the twenty percent line in traditional
finance, Bitcoin's falls of over 90% (2011), ~86% (2014-15), 84% (2018) and
77% (2021-22), smaller coins at 70-95%, six to eighteen months, a +40% week
not ending a downtrend, liquidations cascading in hours without circuit
breakers. Arithmetic on them: 100 -> 20 -> 28 is 72% below the top; 20 back
to 100 is +400%; the 2018 low ($3,122) back to the $19,783 peak is +534%,
said as "more than five hundred percent". Dollar levels are not spoken.

## The beats

Last three crypto long-forms: bitcoin-halving (steps / bars / diagram /
compare / timeline), market-cap (bars / gauge / grid / chart / diagram /
checklist), first-bitcoin-transaction (timeline / steps / stat / steps /
quote).

* `bars` - how far each fall went from its peak, with the stock market's
  twenty percent line as the first row. A proportion is what the voice
  cannot say.
* `diagram`, `loop=True` - the liquidation cascade. The only beat that can
  draw a loop, and the cascade *is* one.
* `chart` - a bear market drawn: lower highs, lower lows, and the +40% week
  marked near the bottom, where it barely shows.
* `steps` - 100 -> 20 -> 28, the arithmetic in order.
* `stat` - +400%, the gain it takes to get from 20 back to 100.

`bars`, `diagram` and `chart` are all in market-cap's set, which is the cost
of a topic whose three nouns are a depth, a loop and a trajectory - each is
the only beat that draws its noun. The set differs from the halving's
(consecutive) by three of five.

**Opener: `Search`**, typing "what is a bear market in crypto". The title is
the phrase people type, which is the one condition for it; the last three
long forms opened Counter / Stamp / hook. Sentence 2 is a number that does
not answer the title - it opens "why so deep?".

**Footage: the act, in the subject's world** (`footage.md`). The stock
exchange's facade for "in stocks", bitcoins, cash being counted and falling,
a bank tower and shuttered shopfronts for a lender failing, a form being
signed for borrowed money, a row of dominoes for the cascade, a STOP button
for the circuit breaker, a city at night for "every hour of every day", and
people watching their phones in the dark for the people watching a market.
Three clips are the narration's own figure of speech, said out loud - the
dominoes, a treadmill under "still go nowhere", stone stairs under "the
steeper that climb gets". Every clip is fresh - verdicts in `footage.md`.
The one abstract is the rain under the disclaimer.

**Thumbnail:** `brown-bear-dark-background/33037033.jpg`, a brown bear's head coming out of
pure black - the noun the whole genre uses for this, no person, and a wall
of black for the type.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/bear-market-in-crypto.py
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

SOURCE_POST = "bear-market-in-crypto"

V = STOCK / "videos"
P = STOCK / "photos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Luma sampled at 15/50/85% of each clip, every clip looked at on a labelled
# three-frame contact sheet. All fetched fresh for this pair.
NYSE = V / "new-york-stock-exchange/4319342.mp4"                 # 10s, L117-120, the stock exchange's columns - bright, and the noun
LONECOIN = V / "gold-bitcoin-black-background/8370146.mp4"       # 14s, L23-38, one gold bitcoin standing on a dark table, centred
MAGNIFY = V / "gold-bitcoin-black-background/8369965.mp4"        # 13s, L63-68, a heap of coins, a bitcoin under a magnifying glass
COINSPIN = V / "bitcoin-coin-rotating/7634144.mp4"               # 10s, L78-81, a bitcoin spinning down flat on a table
SMILE = V / "man-reading-phone-at-night/8070886.mp4"             # 45s, L26-28, a man smiling at his phone in bed, dark
BILLS = V / "cash-money-dark-table/9564160.mp4"                  # 16s, L65-87, dollar bills falling onto a dark table
CASH = V / "counting-dollar-bills-hands/4524511.mp4"             # 24s, L51-58, hands counting dollar bills on black
SIGN = V / "signing-contract-pen-close-up/8439245.mp4"           # 7s,  L78-100, a hand signing a form - one short slot
DOMINO = V / "dominoes-falling/9760001.mp4"                      # 27s, L50-56, a hand tips a row of dominoes on a dark table
STOP = V / "red-emergency-stop-button/4285873.mp4"               # 7s,  L54-65, STOP pressed on a deck - one short slot
CITY = V / "city-at-night-timelapse/33637800.mp4"                # 15s, L26-29, a city from the air at night, timelapse
SKYLINE = V / "financial-district-night/6345205.mp4"             # 21s, L23-31, a financial district's towers at night
TOWERS = V / "financial-district-night/10216591.mp4"             # 13s, L16-17, office towers at night - the BANK shoot, so used once, at the close
BED = V / "man-reading-phone-at-night/7986756.mp4"               # 11s, L7-15, a woman in bed lit by her phone
LYING = V / "checking-phone-in-bed-at-night/6943545.mp4"         # 11s, L29-30, a man lying in bed staring at his phone
PHONEW = V / "checking-phone-in-bed-at-night/7924639.mp4"        # 9s,  L41-42, a woman in bed lit by her phone, close
SUBWAY = V / "people-on-subway-using-phones/7251007.mp4"         # 37s, L44-50 to ~20s (bright after), a man on his phone on a train
RAIN = V / "rain-drops-on-glass-dark/15454042.mp4"               # 25s, L64-69, drops on glass, gold bokeh - the one abstract
BANK = V / "bank-building-at-night/10216513.mp4"                 # 14s, L12-14, a city at night, a bank's tower lit
SHUTTER = V / "closed-shop-shutter-night/3150371.mp4"            # 12s, L15-22 after 2s, shuttered shopfronts down a dark alley
REDDOM = V / "dominoes-falling/5921005.mp4"                      # 22s, L54, red dominoes falling toward camera, a man blurred behind
TREAD = V / "treadmill-running-dark-gym/15112689.mp4"            # 11s, L34, feet running on a treadmill in a dark gym
STAIRS = V / "climbing-stairs-at-night/15814666.mp4"             # 18s, L49-54, someone climbing worn stone steps

BEAR = P / "brown-bear-dark-background/33037033.jpg"             # 9504x6336, L22, a bear's head out of pure black - thumbnail only
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/bear-market-in-crypto"

# A bear market, drawn: every high lower than the last, every low lower too,
# then a +40% week near the bottom (20 -> 28) that barely shows against the
# fall, and a fade after it. The earlier rallies are +13% to +17%, so the
# biggest jump in percent is the smallest to the eye - which is the point.
SERIES = [100, 78, 88, 62, 71, 45, 52, 30, 35, 20, 28, 23]
RALLY = 10


SECTIONS = [
    # --- hook. No card. Search types the title query from frame one;
    # sentence 2 is a number that opens "why so deep?". -----------------------
    Section(
        title="In stocks, twenty percent",
        card=False,
        sentences=[
            ("In stocks, a twenty percent fall makes a bear market.",),
            ("Bitcoin has had four that went past seventy-five percent.",),
            ("And along the way, there were rallies that looked like the end of it.",),
            ("So what is a bear market in crypto,",
             "and why does it go so much deeper?"),
            ("Stay to the end,",
             "and you will know why a forty percent jump does not mean it is over."),
        ],
        shots=[
            Shot(clip=NYSE, clip_at=0.5),
            Shot(clip=LONECOIN, clip_at=0.5),
            Shot(clip=SMILE, clip_at=2.0),
            Shot(clip=BILLS, clip_at=0.5),
            Shot(clip=CITY, clip_at=0.5),
        ],
        gaps=[0.80, 0.85, 0.70, 0.80, 0.90],
    ),

    # --- definition and depth ----------------------------------------------
    Section(
        title="How far does it have to fall?",
        spoken_title="So how far does a market have to fall to count?",
        sentences=[
            ("A bear market is a long stretch of falling prices,",
             "measured from the last peak."),
            # the bars' own sentence - one chunk per row.
            ("In stocks, the usual line is twenty percent.",
             "Bitcoin in 2011 fell more than ninety.",
             "In 2014 and 2015, eighty-six.",
             "In 2018, eighty-four.",
             "And from 2021 to 2022, seventy-seven."),
            ("Smaller coins often fall further,",
             "seventy to ninety-five percent,",
             "and some never come back."),
            ("These stretches last,",
             "often six to eighteen months,",
             "with sharp rallies along the way."),
            # One sentence, one picture: as two, the first took the towers
            # clip, which is the bank tower's shoot eleven seconds later.
            ("So a crypto bear market is not just a dip that went on too long.",
             "Swings get bigger, and money gets pickier about where it goes."),
        ],
        shots=[
            Shot(clip=SKYLINE, clip_at=1.0),
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("Stocks", 0.19, "20%"),
                           ("2011", 0.874, "90%+"),
                           ("2014-15", 0.817, "86%"),
                           ("2018", 0.798, "84%"),
                           ("2021-22", 0.73, "77%")],
                          "HOW FAR FROM THE PEAK")),
            Shot(clip=COINSPIN, clip_at=2.0,
                 note=("70-95%", "how far many smaller coins fall")),
            Shot(clip=SUBWAY, clip_at=2.0,
                 note=("6-18 months", "a typical crypto bear market")),
            Shot(clip=CASH, clip_at=1.0),
        ],
        gaps=[0.60, 1.30, 0.70, 0.60, 0.90],
    ),

    # --- the mechanism ------------------------------------------------------
    Section(
        title="Why does crypto fall so much further?",
        spoken_title="So why does crypto fall so much further?",
        sentences=[
            ("Bear markets usually start when pressures stack up.",),
            ("Borrowing gets more expensive, a big lender or exchange fails,",
             "or new rules scare fresh money off."),
            ("But two things make crypto's falls deeper,",
             "and the first is borrowed money."),
            ("A leveraged trade puts a little money down, and borrows the rest.",),
            ("If the price falls far enough,",
             "the exchange closes the trade for you, by selling it."),
            ("That forced sale is called a liquidation.",),
            ("And each forced sale can knock over the next,",
             "like a row of dominoes."),
            # the diagram's own sentence - one chunk per node, and a trailing
            # reaction chunk that claims no reveal while the loop closes.
            ("The price falls.",
             "Leveraged trades hit their limit, and get sold.",
             "That selling pushes the price down again.",
             "And round it goes."),
            ("When stocks fall that fast, the exchange can pause trading.",
             "It is called a circuit breaker."),
            ("That is the second thing.",
             "Crypto has no pause, and trades every hour of every day."),
            ("So a cascade that would take days elsewhere can run in hours.",),
        ],
        shots=[
            Shot(clip=BANK, clip_at=0.5),
            Shot(clip=SHUTTER, clip_at=2.5),
            Shot(clip=SIGN, clip_at=0.5),
            Shot(clip=BILLS, clip_at=8.0),
            Shot(clip=LYING, clip_at=0.5),
            None,
            Shot(clip=DOMINO, clip_at=1.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("The price falls", "past where traders borrowed"),
                           ("Liquidations", "the exchange sells for them"),
                           ("More selling", "pushes the price lower")],
                          "HOW A CASCADE FEEDS ITSELF", True)),
            Shot(clip=STOP, clip_at=0.5),
            Shot(clip=CITY, clip_at=6.0),
            Shot(clip=BED, clip_at=0.5),
        ],
        gaps=[0.45, 0.70, 0.55, 0.50, 0.45, 0.80, 0.60, 1.40, 0.70, 0.70, 0.90],
    ),

    # --- the shape ----------------------------------------------------------
    Section(
        title="What does a bear market look like?",
        spoken_title="So what does a bear market actually look like?",
        # The spoken title is the chart's hinge, so the beat comes first.
        sentences=[
            # the chart's own sentence: the line first, the marked week second.
            ("Each high lands lower than the last, and each low lands lower too.",
             "Then, near the bottom, the price jumps forty percent in a week."),
            ("Traders call a jump like that a bear market rally.",),
            ("Even the green days can be ten percent up, and still go nowhere.",),
            ("Underneath, fewer buyers wait at each price,",
             "so every sale moves it further."),
            ("And money huddles into Bitcoin,",
             "so its share of the whole market tends to rise."),
            ("To plenty of people watching, every rally still looks like the end of it.",),
        ],
        shots=[
            Shot(graphic="chart", backdrop=BEATGROUND,
                 payload=(SERIES, "A BEAR MARKET, DRAWN", RALLY,
                          "+40% in a week")),
            Shot(clip=SUBWAY, clip_at=12.0),
            Shot(clip=TREAD, clip_at=0.5),
            Shot(clip=REDDOM, clip_at=11.0),
            Shot(clip=MAGNIFY, clip_at=0.5),
            Shot(clip=SMILE, clip_at=20.0),
        ],
        gaps=[1.40, 0.60, 0.55, 0.50, 0.60, 0.90],
    ),

    # --- the twist ----------------------------------------------------------
    # The video's turning point, so the card gets the longer silence.
    Section(
        title="Why doesn't a 40% jump end it?",
        spoken_title="So why doesn't a forty percent jump end it?",
        card_gap=1.30,
        sentences=[
            ("Because a fall and a jump are not measured from the same place.",),
            # the steps' own sentence - one chunk per node.
            ("Start with a hundred dollars at the top.",
             "An eighty percent fall leaves twenty.",
             "A forty percent jump on twenty takes it to twenty-eight."),
            ("That is still seventy-two percent below the top.",),
            ("To get back to a hundred, twenty has to grow five times over.",),
            # the stat's own sentence.
            ("A four hundred percent gain,",
             "just to get back to where it started."),
            ("And the deeper the fall, the steeper that climb gets.",),
            ("Bitcoin's fall in 2018 needed more than five hundred percent,",
             "just to get back to its old high."),
        ],
        shots=[
            Shot(clip=LYING, clip_at=4.0),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 payload=(["$100 at the top", "Down 80%: $20 left",
                           "Up 40%: $28"],
                          "THE SAME 40%, FROM THE BOTTOM")),
            None,
            Shot(clip=CASH, clip_at=12.0),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("+400%", "TO BREAK EVEN",
                          "from $20 back to $100", False)),
            Shot(clip=STAIRS, clip_at=1.0),
            # From ~3s the coin is in focus; before it is a grey blur.
            Shot(clip=COINSPIN, clip_at=3.0,
                 note=("+500%", "the 2018 low, back to the old high")),
        ],
        gaps=[0.55, 1.40, 0.85, 0.55, 1.20, 0.55, 0.90],
    ),

    # --- close: the echo ----------------------------------------------------
    Section(
        title="Measured from the top",
        spoken_title="So a bear market is measured from the top.",
        sentences=[
            ("A rally is measured from the bottom.",),
            ("That is why one green week can look like the end of it, and not be.",),
            ("Nothing in this video is financial advice.",),
            ("So, the next time a coin jumps forty percent in a week,",
             "would you check how far it still is from the top?"),
        ],
        shots=[
            Shot(clip=TOWERS, clip_at=0.5),
            Shot(clip=PHONEW, clip_at=0.5),
            Shot(clip=RAIN, clip_at=1.0,
                 payload=("", "This is not financial advice.")),
            None,
        ],
        gaps=[0.85, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is a Bear Market in Crypto? Why the Drops Go So Deep",
    hook="A bear market in stocks starts at a twenty percent fall. Bitcoin has "
         "had four that went past seventy-five percent. Here is how a bear "
         "market is measured, why crypto falls so much further - borrowed "
         "money, forced selling that feeds itself, and a market that never "
         "pauses - what one looks like from the inside, and why a forty "
         "percent jump in the middle of one can still leave a coin seventy-two "
         "percent below the top.",
    url=URL,
    summary="What a bear market in crypto is and how it works: a long stretch "
            "of falling prices measured from the last peak; the twenty "
            "percent line used in stocks against Bitcoin's own bear markets "
            "(over 90% in 2011, about 86% in 2014-15, 84% in 2018, 77% in "
            "2021-22) and smaller coins at 70-95%; why crypto falls further, "
            "through leverage and liquidations that cascade in hours in a "
            "market that trades around the clock with no circuit breaker; "
            "the shape of a bear market, with lower highs, lower lows and "
            "sharp bear market rallies; and the arithmetic of a drawdown - "
            "why a forty percent jump after an eighty percent fall still "
            "leaves a coin seventy-two percent down, and why getting back "
            "takes a four hundred percent gain. Nothing here is financial "
            "advice.",
    tags=["bear market crypto", "what is a bear market in crypto",
          "crypto bear market explained", "bear market", "crypto winter",
          "bear market rally", "crypto liquidation", "leverage crypto",
          "bitcoin bear market", "crypto crash explained",
          "crypto for beginners"],
    cta=f"The full guide to crypto bear markets: {URL}",
    credits=["Nothing in this video is financial advice."],
)

# One bracketed word, BEAR, beside the bear (`thumbnails.md`: one-word accent
# in the 16:9 column). The first cut asked "why does crypto fall so far?" and
# the editor asked for words about the bear market, since the picture is a bear.
HEADLINE = "What is a crypto [bear] market?"
# The scorer zoomed in and cut the bear's ear at the right edge. A manual
# crop, shifted right so the whole head sits beside the type on the photo's
# own black; swept 0.12 (type on the left ear), 0.20, 0.26 (crowds the edge).
THUMB_LAYOUT = dict(thumb_crop_at=(0.9, 0.45), thumb_side="left",
                    thumb_shift=0.20)


def main() -> None:
    out = Path.home() / "Desktop/bear-market-in-crypto-long.mp4"
    work = Path.home() / "Desktop/.bear-market-in-crypto-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title is the phrase people type. Last three long forms opened
        # Counter / Stamp / hook. Question only - no answer on screen.
        opener=Search("what is a bear market in crypto"),
        thumb_headline=HEADLINE,
        thumb_image=BEAR,
        thumb_accent="yellow",
        **THUMB_LAYOUT,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        from video_automation.longform.thumb import render_thumb
        print(render_thumb(Path.home() / "Desktop/bear-market-in-crypto-long-thumb.jpg",
                           CRYPTO, HEADLINE, image=BEAR, accent="yellow",
                           **{k[6:]: v for k, v in THUMB_LAYOUT.items()}))
    else:
        main()
