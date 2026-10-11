"""What is the Bitcoin halving - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/the-bitcoin-halving.mdx.

**The angle.** The halving is usually talked about as a date and an event.
It is neither: it is a block count, enforced by every computer running
Bitcoin, and nobody schedules it. So the video opens on that ("not on
anybody's calendar"), walks where new coins come from and the schedule,
shows why the network does not break when miners' pay halves (the difficulty
loop), splits what the code guarantees from what it does not, and lands the
twist - half of all bitcoin was minted in four years, and the last fraction
takes until around 2140. The close echoes the open: check the block count,
not the date.

**No financial advice.** It describes a schedule and a feedback loop. It
names no price level and predicts nothing; the price chapter's whole point
is that the code guarantees the supply cut and *nothing else*, and it says
what people expect only as "expected for a long time", never which way. No
coin is rated, no platform named, and no shot shows a chart, ticker or price.

**Figures.** The article's own: 50 BTC at launch, 210,000 blocks, the four
halving dates and rewards, 1,050,000 / ~April 2028 / 1.5625, ~450 and ~225 a
day, 19.7M by the 2024 halving, 2,016 blocks per difficulty reset, the 21M
cap around 2140. Arithmetic on them: 210,000 x 50 = 10.5M, half the cap, in
the first epoch; 19.7M / 21M = about 94%. Nothing from outside the post.

## The beats

Last three crypto long-forms: market-cap (bars / gauge / grid / chart /
diagram / checklist), first-bitcoin-transaction (timeline / steps / stat /
steps / quote), musk-effect (diagram / chart / stat / timeline / compare).

* `steps` (3 nodes) - where new bitcoin comes from, ending on the halving.
* `bars` - the reward, 50 / 25 / 12.5 / 6.25 / 3.125. Each bar is half the
  one above it, which is the whole idea drawn.
* `diagram`, `loop=True` - the difficulty adjustment as a thermostat. The
  first `loop=True` on this channel; market-cap's diagram was a straight
  chain.
* `compare` - what the code guarantees, against what it does not.
* `timeline` - 2009 / 2024 / ~2140, three nodes on purpose: the five
  halvings sit in the first eleven percent of the axis, and the empty
  hundred years after 2024 *is* the point. More nodes collide (labels
  alternate above and below, and 2009 and 2024 already sit 140px apart).

**Opener: `Counter`**, landing on "210,000" in sentence 2. Last three long
forms opened Stamp / hook / Search, and the defining number of the topic is
a block count, which is exactly the shape `Counter` is for. The Short runs a
`Counter` too, so the pair reads as a pair.

**Footage: the act, in the subject's world** (`footage.md`). A hand circling
a date on a calendar (the thing the halving is *not*), code and terminals
for "a rule in the software", a man with a graphics card for the miner, a
power plant and a switch panel for the electricity and the machines going
off, an open mining rig for the miners (the first cut's mine tunnels and
excavator were cut on review - physical mining is not bitcoin mining), and a
bitcoin in soil for "minted". Coin footage is capped at three shots, each under a line
about coins. Every clip is fresh - see the verdict table in `footage.md`.

**Thumbnail:** `single-gold-bitcoin-dark/5980926.jpg`, a coin half-buried
in soil - a mined coin, no person, because the video has none.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/bitcoin-halving.py
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

SOURCE_POST = "the-bitcoin-halving"

V = STOCK / "videos"
P = STOCK / "photos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Luma/saturation sampled at 12/50/88% of each clip, every clip looked at on
# a labelled three-frame contact sheet. All fetched fresh for this pair.
CAL = V / "marking-date-on-calendar/9057559.mp4"                 # 11s, L159-169, a red marker circling a date - bright, and the noun
CAL2 = V / "marking-date-on-calendar/9057678.mp4"                # 9s,  L154-156, a date circled on a September page - same shoot as CAL, a minute apart
PLANNER = V / "desk-calendar-dark/9903482.mp4"                   # 17s, L80-88, hands writing in a day planner on a dark desk
GPU = V / "graphics-card-mining-rig/7380236.mp4"                 # 15s, L53-76, a man turning a graphics card over, machines behind
CODE = V / "laptop-code-screen-night/34279721.mp4"               # 8s,  L34-38, code on a monitor, red and blue light - one short slot
TERM = V / "command-line-terminal-screen/35475096.mp4"           # 22s, L69-84, a terminal scrolling install output
LAPTOP = V / "computer-screen-code-close-up-dark/11274341.mp4"   # 28s, L83, an editor full of code on a laptop
RIG = V / "mining-rig-fans/5467579.mp4"                          # 26s, L65-71, inside an open rig: fans, cables, cards
STACKS = V / "bitcoin-miner-machine/8369987.mp4"                 # 9s,  L73-75, bitcoin stacks of falling height on wood
WATCH = V / "stopwatch-ticking-close-up/4601287.mp4"             # 12s, L65, a watch face macro, the hand sweeping
POCKET = V / "old-pocket-watch/7265818.mp4"                      # 9s,  L83-85, a pocket watch swinging by a candle
HOUR = V / "hourglass-sand-falling-dark/39488458.mp4"            # 17s, L71, an hourglass running, pink sand on blue
HOUR2 = V / "hourglass-sand-falling-dark/1196530.mp4"            # 10s, L80, an hourglass, violet sand - one use
SWITCH = V / "turning-off-power-switch/6520448.mp4"              # 8s,  L69-91, a finger flicking a row of switches off
PLANT = V / "power-plant-at-night/7628844.mp4"                   # 21s, L37-39, a power station's stacks at night, steam
PAY = V / "paying-with-phone-contactless/6602062.mp4"            # 10s, L63-66, a phone tapped on a card terminal
PAPER = V / "man-reading-newspaper-dark/9564066.mp4"             # 30s, L47-55, a man turning a newspaper in a dark bar - the claim, read
COINS = V / "bitcoin-coin-close-up-dark/4406964.mp4"             # 14s, L80-82, gold bitcoins filling the frame
SILVER = V / "bitcoin-coin-close-up-dark/8369912.mp4"            # 10s, L64-85, silver bitcoins on dark wood, rack focus
RAIN = V / "rain-drops-on-glass-dark/33938667.mp4"               # 18s, L75, drops on grey glass - the one abstract

SOIL = P / "single-gold-bitcoin-dark/5980926.jpg"                # 6638x4425, L44, a bitcoin half-buried in soil
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/the-bitcoin-halving"

# Spoken numbers. The caption half carries the figure, so the SRT and the
# opener's `at_word` both read "210,000"; the voice gets the words.
N210 = ("210,000 blocks", "two hundred and ten thousand blocks")


SECTIONS = [
    # --- hook. No card. The Counter spins from frame one and lands on
    # "210,000" in sentence 2, ~3.5s in. -----------------------------------
    Section(
        title="Not on anybody's calendar",
        card=False,
        sentences=[
            ("The Bitcoin halving is not on anybody's calendar.",),
            (("Every 210,000 blocks,", "Every two hundred and ten thousand blocks,"),
             "the code cuts the pay for mining new bitcoin in half."),
            ("There is no vote, and no one person can change it.",),
            ("It started at fifty new coins a block,",
             "and it has been cut in half every four years since."),
            ("Stay to the end,",
             "and you will know when the next one lands,",
             "and what the code does not promise."),
        ],
        shots=[
            Shot(clip=CAL, clip_at=0.5),
            Shot(clip=TERM, clip_at=1.0),
            Shot(clip=CODE, clip_at=0.5),
            Shot(clip=COINS, clip_at=0.5),
            Shot(clip=WATCH, clip_at=0.5),
        ],
        gaps=[0.80, 0.80, 0.70, 0.80, 0.90],
    ),

    # --- where new coins come from ------------------------------------------
    Section(
        title="Where do new bitcoins come from?",
        spoken_title="So where do new bitcoins actually come from?",
        sentences=[
            ("Roughly every ten minutes, a miner adds a new block to Bitcoin's ledger.",),
            ("The network pays it the fees inside that block,",
             "and a batch of brand new bitcoin."),
            ("That new batch, the block subsidy,",
             "is the only way a bitcoin is ever created."),
            ("So the whole supply runs on three steps.",),
            # the steps' own sentence - one chunk per node.
            ("A miner finds a block.",
             "The network pays it in new bitcoin.",
             ("And every 210,000 blocks, that pay is cut in half.",
              "And every two hundred and ten thousand blocks, that pay is cut in half.")),
            ("That last step is the halving.",),
            ("Think of it as a pay cut every four years,",
             "however good the miner's machines get."),
            ("It is a rule in the software,",
             "and every computer running Bitcoin checks it."),
        ],
        shots=[
            Shot(clip=GPU, clip_at=1.0),
            Shot(clip=PAY, clip_at=1.0),
            Shot(image=SOIL, zoom=1.10, pan=(0.02, -0.01), aspect=16 / 9,
                 bias=0.5),
            None,
            Shot(graphic="steps", backdrop=BEATGROUND,
                 payload=(["A miner finds a block",
                           "The network pays it new bitcoin",
                           "Every 210,000 blocks, that pay halves"],
                          "WHERE NEW BITCOIN COMES FROM")),
            None,
            Shot(clip=RIG, clip_at=1.0),
            Shot(clip=LAPTOP, clip_at=1.0),
        ],
        gaps=[0.60, 0.70, 0.85, 0.55, 1.20, 0.80, 0.70, 0.90],
    ),

    # --- why four years -----------------------------------------------------
    Section(
        title="Why every four years?",
        spoken_title="So why roughly every four years?",
        sentences=[
            (("210,000 blocks, at about ten minutes each,",
              "Two hundred and ten thousand blocks, at about ten minutes each,"),
             "comes to roughly four years."),
            ("But the code counts blocks, not days.",),
            ("When miners find blocks faster, the halving arrives early.",
             "When they slow down, it arrives late."),
            ("So any date you see for the next one is an estimate, not a deadline.",),
        ],
        shots=[
            Shot(clip=POCKET, clip_at=0.5,
                 note=("~4 years", "210,000 blocks x 10 minutes")),
            Shot(clip=CAL2, clip_at=0.5),
            Shot(clip=HOUR2, clip_at=0.5),
            Shot(clip=PLANNER, clip_at=1.0),
        ],
        gaps=[0.80, 0.90, 0.70, 0.90],
    ),

    # --- the schedule -------------------------------------------------------
    # The spoken title is the bars' hinge, so the beat comes first.
    Section(
        title="How far has the pay fallen?",
        spoken_title="So how far has the pay actually fallen?",
        sentences=[
            # the bars' own sentence - one chunk per row.
            ("Fifty bitcoin a block, from 2009.",
             "Twenty-five, from November 2012.",
             "Twelve and a half, from July 2016.",
             "Six point two five, from May 2020.",
             "And three point one two five, since April 2024."),
            ("Each bar is half the one above it.",),
            ("The next halving is expected around April 2028,",
             ("at block 1,050,000.", "at block one million and fifty thousand.")),
            ("The pay drops to about one and a half bitcoin a block,",
             "and new supply to about two hundred and twenty-five coins a day."),
        ],
        shots=[
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("2009", 0.92, "50 BTC"),
                           ("Nov 2012", 0.46, "25"),
                           ("Jul 2016", 0.23, "12.5"),
                           ("May 2020", 0.115, "6.25"),
                           ("Apr 2024", 0.0575, "3.125")],
                          "NEW BITCOIN PER BLOCK")),
            None,
            Shot(clip=CAL, clip_at=5.0,
                 note=("~2028", "block 1,050,000")),
            Shot(clip=SILVER, clip_at=0.5,
                 note=("450 to 225", "new bitcoin a day")),
        ],
        gaps=[1.30, 0.80, 0.60, 0.90],
    ),

    # --- miners -------------------------------------------------------------
    Section(
        title="What happens to the miners?",
        spoken_title="So what happens to the miners?",
        sentences=[
            ("Overnight, the part of their pay made of new coins is cut in half.",),
            ("Unless fees or the price make up the difference,",
             "the oldest, least efficient machines stop paying for their own electricity."),
            ("And some of them get switched off.",),
            ("So does Bitcoin slow down?",),
            # the diagram's own sentence - one chunk per node.
            ("Miners leave, and the computing power drops.",
             "Blocks start arriving slower than ten minutes.",
             ("Every 2,016 blocks, the network lowers the difficulty.",
              "Every two thousand and sixteen blocks, the network lowers the difficulty."),
             "And blocks settle back to about ten minutes."),
            ("It works in reverse too,",
             "and it has held through every halving so far."),
        ],
        shots=[
            Shot(clip=GPU, clip_at=8.0),
            Shot(clip=PLANT, clip_at=1.0),
            Shot(clip=SWITCH, clip_at=1.5),
            None,
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("Miners leave", "computing power drops"),
                           ("Blocks slow down", "past ten minutes"),
                           ("Difficulty resets", "every 2,016 blocks"),
                           ("Back to ten minutes", "until the next change")],
                          "HOW BITCOIN KEEPS ITS PACE", True)),
            None,
        ],
        gaps=[0.70, 0.70, 0.85, 0.80, 1.40, 0.90],
    ),

    # --- price --------------------------------------------------------------
    # The section that has to stay on the right side of the line: the code
    # guarantees the supply cut and nothing else, said as a split, never as
    # a direction.
    Section(
        title="Does the halving push the price up?",
        spoken_title="So does the halving push the price up?",
        sentences=[
            ("It is the claim you hear most, every four years.",),
            # the compare's own sentence: 8 chunks, the heading first on
            # each side, written as a spoken hinge.
            ("Here is what the code guarantees.",
             "Half as many new coins per block,",
             ("every 210,000 blocks,", "every two hundred and ten thousand blocks,"),
             "up to a cap of twenty-one million.",
             "And here is what it does not.",
             "Any move in the price,",
             "an exact date,",
             "or every miner staying online."),
            ("The halving changes how many new coins arrive.",
             "Demand, the other half of any price, is not in the code at all."),
        ],
        shots=[
            Shot(clip=PAPER, clip_at=1.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("GUARANTEED",
                          ["Half the new coins", "Every 210,000 blocks",
                           "A 21 million cap"],
                          "NOT GUARANTEED",
                          ["A price move", "An exact date",
                           "Every miner online"],
                          True)),
            Shot(clip=COINS, clip_at=7.0),
        ],
        gaps=[0.70, 1.40, 0.90],
    ),

    # --- the twist ----------------------------------------------------------
    Section(
        title="What happens when the halvings run out?",
        spoken_title="So what happens when the halvings run out?",
        sentences=[
            ("Halving fifty, over and over, gets small very fast.",),
            ("The first four years alone minted ten and a half million coins,",
             "half of all the bitcoin there will ever be."),
            ("Put that on a timeline, and the shape is lopsided.",),
            # the timeline's own sentence - one chunk per node.
            ("Mining starts in 2009.",
             "By 2024, about ninety-four percent of it is mined.",
             ("And the last fraction of a coin is expected around 2140.",
              "And the last fraction of a coin is expected around twenty-one forty.")),
            ("Fifteen years for almost all of it,",
             "and more than a century for the rest."),
            ("When the new coins finally stop, miners will be paid by fees alone.",),
            ("So over the coming decades,",
             "the network's security has to move from new coins to fees."),
        ],
        shots=[
            Shot(clip=STACKS, clip_at=0.5),
            Shot(clip=RIG, clip_at=14.0,
                 note=("10.5M", "half of all bitcoin, mined by 2012")),
            Shot(clip=CAL2, clip_at=5.0),
            Shot(graphic="timeline", backdrop=BEATGROUND,
                 payload=([("2009", "mining starts, 50 a block"),
                           ("2024", "about 94% already mined"),
                           ("~2140", "the last fraction of a coin")],
                          "WHEN THE 21 MILLION ARRIVE")),
            Shot(clip=HOUR, clip_at=1.0),
            Shot(clip=PAY, clip_at=5.0),
            Shot(clip=PLANT, clip_at=12.0),
        ],
        gaps=[0.60, 0.85, 0.55, 1.40, 0.85, 0.70, 0.90],
    ),

    # --- close: the echo ----------------------------------------------------
    Section(
        title="A rule, not an event",
        spoken_title="So the halving is a rule, not an event.",
        sentences=[
            (("It runs every 210,000 blocks,", "It runs every two hundred and ten thousand blocks,"),
             "whoever is watching, and whatever the price is doing."),
            ("It cuts new supply. It promises nothing else.",),
            ("Nothing in this video is financial advice.",),
            ("So, the next time someone gives you a date for the halving,",
             "would you check the block count instead?"),
        ],
        shots=[
            Shot(clip=TERM, clip_at=12.0),
            Shot(clip=LAPTOP, clip_at=14.0),
            Shot(clip=RAIN, clip_at=1.0,
                 payload=("", "This is not financial advice.")),
            None,
        ],
        gaps=[0.80, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is the Bitcoin Halving? How It Works and When the Next One Is",
    hook="The Bitcoin halving is not a date anyone sets. Every 210,000 blocks, "
         "roughly every four years, the code cuts the new bitcoin paid to "
         "miners in half. Here is where new bitcoin comes from, every halving "
         "so far and when the next one is expected, why the network keeps "
         "its pace when miners switch off, what the code guarantees and what "
         "it does not, and why half of all bitcoin was mined in four years "
         "while the last fraction takes until around 2140.",
    url=URL,
    summary="What the Bitcoin halving is and how it works: the block subsidy "
            "as the only way new bitcoin is created; the rule that cuts it "
            "in half every 210,000 blocks, enforced by every node with no "
            "vote; why that is roughly every four years but a block count "
            "rather than a date; every halving so far (50, 25, 12.5, 6.25, "
            "3.125 BTC) and the next, expected around April 2028 at block "
            "1,050,000; what happens to miners and how the difficulty "
            "adjustment every 2,016 blocks keeps blocks near ten minutes; "
            "what the code guarantees and what it does not, including any "
            "price move; and the long tail to the 21 million cap around "
            "2140, when fees have to carry the network. Nothing here is "
            "financial advice.",
    tags=["bitcoin halving", "what is the bitcoin halving", "bitcoin halving explained",
          "next bitcoin halving", "bitcoin halving 2028", "block reward",
          "block subsidy", "bitcoin supply", "21 million bitcoin",
          "bitcoin mining", "difficulty adjustment", "crypto for beginners"],
    cta=f"The full guide to the Bitcoin halving: {URL}",
    credits=["Footage and photography: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)

HEADLINE = "Why does Bitcoin cut its pay in [half?]"
THUMB_LAYOUT = dict(thumb_crop_at=(0.5, 0.55), thumb_side="right",
                    thumb_shift=0.20)


def main() -> None:
    out = Path.home() / "Desktop/bitcoin-halving-long.mp4"
    work = Path.home() / "Desktop/.bitcoin-halving-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The payoff of the opening is a number - the block count the whole
        # schedule runs on. Last three long forms opened Stamp / hook /
        # Search; the Short runs a Counter as well.
        opener=Counter("210,000", "BLOCKS, THEN THE PAY HALVES",
                       at_word="210,000"),
        thumb_headline=HEADLINE,
        thumb_image=SOIL,
        thumb_accent="yellow",
        # The scorer zoomed in and cut the coin at two edges. A manual crop,
        # pushed left so the whole coin sits beside the type on dark soil.
        **THUMB_LAYOUT,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        from video_automation.longform.thumb import render_thumb
        print(render_thumb(Path.home() / "Desktop/bitcoin-halving-long-thumb.jpg",
                           CRYPTO, HEADLINE, image=SOIL, accent="yellow",
                           **{k[6:]: v for k, v in THUMB_LAYOUT.items()}))
    else:
        main()
