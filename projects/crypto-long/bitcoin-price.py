"""Who controls Bitcoin's price? — long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/who-controls-bitcoins-price.mdx.
**Fourth explainer on the demand ranking in `docs/long-form-strategy.md`** — 227
views, behind the mining rig and the exchanges post, which have both shipped,
and behind `exchanges/cryptocom`, which is a *review* rather than an explainer
and is still an unsettled format question. Picked over the two higher explainers
(`crypto-etfs-explained` 362, `what-is-proof-of-stake` 322) because the title is
already a question, the honest answer is counterintuitive, and the arc writes
itself — the strongest script on the list rather than the biggest number.

**The article is a three-part agenda and the video cannot be one.** Read aloud,
"whales do this, developers do that, governments do the other" is a slide deck:
three unrelated facts with a conclusion bolted on. So the script takes the thing
the article states in its own opening section and then walks away from — **the
supply side is fixed, so every argument about the price is an argument about
demand** — and makes the three groups the *answer* to that rather than the
agenda.

The arc:

* **Hook** — the number moved while you were asleep. Nobody sets it. Who did?
* **Reframe** — a price is an agreement, and Bitcoin's supply side was settled
  in the code. Only demand is up for grabs.
* **Deep dive** — the whales, and why their power is not the size of the pile.
  It is that almost none of the supply is for sale, so the book is thin.
* **Twist** — none of the three is the answer. The price is set by the last
  person willing to sell, and a whale who sells changes the price they get.
* **Mirror** — so watch exchange balances, not whale wallets.
* **Echo** — back to the morning and the different number, reframed.

**No financial advice, and the line here is about *mechanism*, not direction.**
The script never says the price will rise or fall, never names a level, never
suggests buying or selling anything, and never rates a platform. The one thing
it tells the viewer to watch — how much bitcoin is sitting on exchanges — is a
description of what the flow means, not a signal to trade on, and the outro says
plainly that none of it is advice.

**Every figure is structural rather than current, deliberately.** An evergreen
video cannot carry a live number: "roughly 2.5 million coins on exchanges" is
true this month and wrong next year, and a `VideoObject` embedded on the post
has no way to age out. So the `stat` is the 21 million cap and the `bars` beat
is the halving schedule — both fixed in the protocol, both exact, neither
capable of dating. The thin-float argument is made qualitatively ("a sliver of
the total"), which is permanently true and claims no figure. The only dated
facts are historical events the article itself cites: China's 2021 ban, the
US spot exchange traded fund approval in early 2024, and SegWit in 2017.

**Beat silhouettes, checked before building** — the skill's rule is to list them
and confirm you are not drawing the same two shapes four times. Six beats, six
different shapes, no repeats: `stat` (the cap), `bars` (the halving schedule),
`grid` (the three manipulation tactics), `compare` (hours against years),
`checklist` (who sets the price, two-phase), `quote` (the twist line). Item
counts vary too — 1, 5, 3, 3+3, 4, 1.

**The `grid` moved from "the three groups" to "the three tactics" while
cutting for length, and it is a better beat there.** As a map of whales /
developers / governments it restated what the next two chapter cards were
about to say anyway; as sell wall / spoofing / pump and dump it carries three
definitions the script would otherwise have spent three sentences on, which is
exactly what a grid's optional second line is for.

**The `bars` beat is the one that carries the reframe**, and it is the reason
that beat exists: "the new supply halves roughly every four years" is a sentence
a viewer has to hold in their head, and five bars each half the last is the same
fact read instantly. The final bar is tiny, which is the argument.

**Pictures.** The post's own two images are both out on brightness —
`greedy-investor-2.jpg` measures L104 and `what-is-a-crypto-whale.jpg` L124/S116,
far over the ~L82 working ceiling for a site photograph — so the stills come
from the wider library, screened: `hacker.jpg` (L38/S3) is the darkest and most
on-palette thing in it, and `regulators.jpg` (L72/S7), `law.jpg` (L42/S11),
`gold.jpg` (L49/S29) and `global-map.jpg` (L20/S26) carry the lines they were
drawn for. `data-center.jpg` passes the box at L41 and is still rejected: it is
green-lit, and green is the one hue that cuts hardest against gold.

**Three new stock queries, two of which paid.** `deep ocean underwater dark`
returned `5678004` — a near-monochrome dark water surface at L29/S1.6, which is
the closest thing to on-palette in the whole cache and carries the whale section
without a literal whale in it (a literal whale under "crypto whale" is a pun the
script does not need). `government building columns night` returned `35120905`,
a lit capitol dome at L10-24/S4-7. `gavel courtroom dark` returned two usable
clips and **`6699964` was taken over the better-measuring `6101343`** on the
contact sheet rather than on the numbers: 6101343 is a judge whose head is cut
off by the top of frame, and 6699964 is the gavel itself being picked up and
struck, which is an object and an action rather than a headless person.
`whale swimming underwater` and `printing money banknotes machine` were both
rejected wholesale — every whale clip is bright tropical blue (L72-114, S75-177)
and every banknote clip is a bright overhead flat-lay. All five queries are
cached and manifested, rejects included.

**`dark-abstract-digital-particles/29352532` was rejected for length, not
brightness.** It measures L10/S18 and is 2.0 seconds long; a clip is never
looped and stretches at most 1.33x, so it cannot fill a slot over ~2.7s.

**Length was set by measurement, not by the skill's nominal figure.** The
table says ~2.9 words/sec, which put the first draft's 940 words at a plausible
5:20 and it would in fact have run past six minutes. The shipped exchanges
explainer is the calibration that matters: 718 words plus 42.2s of written gaps
came out at 263.21s, i.e. **3.25 words/sec including the chapter cards**. This
script is 656 words and 45.0s of gaps, which predicts 4:06. Use the shipped
number, not the table.

**Phonemes, checked with espeak rather than guessed.** `SegWit` comes back
`sˈɛɡ wˈɪt`, correct as written. `ETF` comes back
`ˈɛtf` — read as a word, not three letters — so the narration says "exchange
traded funds" throughout, which is also what a beginner needs to hear. `21,000,000`
and `1,000` both read correctly as words.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/bitcoin-price.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"

# Pexels, cached under assets/stock/ and screened across the clip rather than at
# one second — the trailing comment is the luma/saturation range over the whole
# length. The three at the bottom are this video's own additions.
CHART = STOCK / "videos/stock-market-chart-screen-dark"      # 38133087 L20 S19
FLOOR = STOCK / "videos/wall-street-trading-floor-screens"   # see per-file below
CANDLE = STOCK / "videos/trading-candlestick-chart-monitor"  # 38471109 L15-16 S18
PHONE = STOCK / "videos/smartphone-finance-app-dark"         # 35518150 L34-45 S24-29
STREAM = STOCK / "videos/digital-code-stream-dark"           # 34127877 L13-15 S5
CODE = STOCK / "videos/cryptography-code-screen"             # 14003933 L17-19 S14
KEYS = STOCK / "videos/typing-keyboard-night"                # 8212370  L20-25 S10-12
WAREHOUSE = STOCK / "videos/warehouse-industrial-dark-interior"  # 19217894 L23-34 S3
SERVER = STOCK / "videos/server-room-data-center"             # 7140928  L22-31 S24-43
WAVES = STOCK / "videos/abstract-dark-waves-motion"          # see per-file below

OCEAN = STOCK / "videos/deep-ocean-underwater-dark"          # 5678004  L29-31 S1.5-2.0
GOVT = STOCK / "videos/government-building-columns-night"    # 35120905 L10-24 S3.7-6.6
GAVEL = STOCK / "videos/gavel-courtroom-dark"                # 6699964  L33-36 S11.5-13.9

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # female, af_heart. Candidate, not approved.

# The shared library in `assets/brand/music/`, which serves both sites. Same
# track as the exchanges explainer, which is the point of a channel having one.
MUSIC = music.track("night-drift")

URL = "https://thecrypto.wiki/posts/who-controls-bitcoins-price"

A = 16 / 9                      # crop toward the frame, not the shorts' 1.15


SECTIONS = [
    # --- the hook. No card: an opening chapter card spends the one second
    # that decides whether anybody stays. Frame one is a clip, not a still. ---
    Section(
        title="Who moved it?",
        card=False,
        sentences=[
            ("Bitcoin moved while you were asleep.",),
            ("You wake up,",
             "and the number on your screen",
             "is a different number."),
            ("So who did that?",),
            ("There is no central bank here.",
             "No committee sets this price."),
            # The reversal. It contradicts the line before it, so it takes the
            # long gap — that is what the silence is for.
            ("And yet something clearly moved it.",),
            # The retention call, out loud, inside the first twenty seconds —
            # and the outro answers this exact question rather than a near one.
            ("Stay to the end",
             "and you will know which forces move Bitcoin in hours,",
             "which move it in years,",
             "and the one number to watch instead."),
            # One chunk, because a `stat` reveals one item and the caption
            # count is what times it.
            ("Twenty-one million coins.",),
            ("That is all there will ever be.",
             "It was written into the code",
             "before most of them existed."),
            ("No committee can raise it.",
             "No emergency can print more."),
        ],
        shots=[
            Shot(clip=CHART / "38133087.mp4", clip_at=1.0),
            Shot(clip=PHONE / "35518150.mp4", clip_at=0.5),
            None,                                    # ride the phone
            Shot(clip=GOVT / "35120905.mp4", clip_at=1.0,
                 payload=("", "No central bank. No committee.")),
            Shot(clip=FLOOR / "38055932.mp4", clip_at=1.0),
            # The title stamp, on the line that makes the promise — around
            # eight seconds in, so it costs none of the opening five.
            Shot(clip=FLOOR / "38797295.mp4",
                 payload=("", "WHO CONTROLS BITCOIN'S PRICE?")),
            Shot(graphic="stat",
                 payload=("21,000,000", "COINS. EVER.",
                          "Fixed in the code. Every argument is about demand."),
                 backdrop=POSTS / "digital-technology.jpg"),
            None,                                    # hold the figure
            Shot(image=POSTS / "gold.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
        ],
        gaps=[0.60, 0.70, 0.90, 0.55, 0.95, 0.60, 1.10, 0.45, 0.80],
    ),

    # --- reframe: a price is an agreement, and only one side is up for grabs -
    Section(
        title="So where does a price come from?",
        spoken_title="So where does a price actually come from?",
        sentences=[
            ("A price is not a fact about an object.",
             "It is an agreement between two people."),
            ("One person willing to sell.",
             "One willing to buy.",
             "Where they meet is the price."),
            ("So Bitcoin has two sides,",
             "and only one is up for grabs."),
            ("The supply side was settled in the code.",),
            ("New coins arrive on a schedule",
             "that only ever slows down."),
            # One caption per bar, which is what times the reveals.
            ("Fifty new coins a block.",
             "Then twenty-five.",
             "Then twelve and a half.",
             "Then six and a quarter.",
             "Now just over three."),
            ("Every four years it halves,",
             "and nobody votes on it."),
            ("So every argument about the price",
             "is an argument about demand."),
        ],
        shots=[
            Shot(image=POSTS / "laptop-trading.jpg", zoom=1.12,
                 pan=(0.02, 0.01), aspect=A, bias=0.45),
            Shot(clip=FLOOR / "38569995.mp4", clip_at=2.0),
            None,
            Shot(image=POSTS / "bitcoin-vs-fiat.jpg", zoom=1.11,
                 pan=(-0.02, 0.01), aspect=A, bias=0.45),
            Shot(clip=WAREHOUSE / "19217894.mp4", clip_at=0.5,
                 payload=("", "New coins, on a fixed schedule")),
            # **`bars`, not `stat` or `checklist`.** Neither of those can show a
            # *proportion*, and the proportion is the argument: five bars each
            # half the one above it says "this only ever slows down" faster than
            # the sentence does, and the last bar being tiny is the point.
            Shot(graphic="bars",
                 payload=([("2009", 1.000, "50 BTC"),
                           ("2012", 0.500, "25 BTC"),
                           ("2016", 0.250, "12.5 BTC"),
                           ("2020", 0.125, "6.25 BTC"),
                           ("2024", 0.0625, "3.125 BTC")],
                          "NEW COINS PER BLOCK")),
            None,                                    # hold the bars
            Shot(clip=STREAM / "34127877.mp4",
                 payload=("", "Every argument is about demand")),
        ],
        gaps=[0.70, 0.60, 0.75, 0.55, 0.60, 0.90, 0.70, 0.85],
    ),

    # --- the deep dive: why a whale's power is not the size of the pile ------
    Section(
        title="Who moves it in hours?",
        spoken_title="So who moves it in hours?",
        sentences=[
            ("Start with the whales.",),
            ("A whale is one wallet",
             "holding a thousand bitcoin or more."),
            ("Their power is not the size of the pile.",),
            ("It is that almost none of it is for sale.",),
            ("Most bitcoin sits in wallets that have not moved in years.",
             "What is on an exchange today",
             "is a sliver of the total."),
            # No jargon without an immediate plain-English decode.
            ("So the order book is thin -",
             "just a queue of offers",
             "to buy and to sell."),
            # The lead-in sits here, in the sentence *before* the beat: a beat
            # times its reveals off its own sentence, so a lead-in inside that
            # span eats reveal zero and shunts every item one line late.
            ("A thin queue moves easily,",
             "and they have names",
             "for how that gets done."),
            ("A sell wall.",
             "Spoofing.",
             "A pump and a dump."),
            ("But none of that is choosing the price.",
             "It is exploiting how few people are selling."),
        ],
        shots=[
            Shot(clip=OCEAN / "5678004.mp4", clip_at=1.0,
                 payload=("", "The whales")),
            # A number that is spoken must also be seen — and the gloss is the
            # point: "1,000 BTC" alone is a figure, with the line under it it
            # is the definition the sentence just gave.
            Shot(clip=CHART / "38055931.mp4", clip_at=1.0,
                 note=("1,000 BTC", "what makes one wallet a whale")),
            Shot(image=POSTS / "futuristic-crypto-exchange.jpg", zoom=1.11,
                 pan=(0.02, 0.01), aspect=A, bias=0.45),
            Shot(clip=WAVES / "27980029.mp4",
                 payload=("", "Almost none of it is for sale")),
            Shot(image=POSTS / "security-combination-lock.jpg", zoom=1.10,
                 pan=(-0.02, 0.01), aspect=A, bias=0.5),
            Shot(clip=CHART / "38783511.mp4", clip_at=2.0),
            Shot(clip=CANDLE / "38471109.mp4", clip_at=1.0,
                 payload=("", "A thin book moves")),
            # A `grid`, not a checklist: three tactics is a *set* with no
            # verdict column, and the second line on each card is where the
            # wide layout pays for itself — it replaces three sentences of
            # prose defining each one.
            Shot(graphic="grid",
                 payload=([("Sell wall",
                            "A huge order parked under the market"),
                           ("Spoofing",
                            "Orders they never intend to fill"),
                           ("Pump and dump",
                            "Hype it up, then sell into the hype")],
                          "HOW A THIN BOOK GETS PUSHED")),
            Shot(clip=OCEAN / "5678004.mp4", clip_at=9.0,
                 payload=("", "Not choosing the price")),
        ],
        gaps=[0.55, 0.70, 0.85, 0.90, 0.70, 0.80, 0.90, 0.90, 0.80],
    ),

    # --- the slow forces, and the comparison the chapter exists for ---------
    Section(
        title="And who moves it in years?",
        sentences=[
            ("Developers never touch the price.",),
            ("They maintain the protocol -",
             "the rules every computer on the network follows."),
            ("SegWit, in twenty seventeen,",
             "changed how transactions pack into a block."),
            ("It did not move the price that week.",
             "It decides whether the network",
             "is worth anything in ten years."),
            ("Governments are the loud ones.",),
            ("China banned trading and mining in twenty twenty-one,",
             "and the market fell."),
            # "ETF" phonemizes to `ˈɛtf` — read as a word. Say the whole thing,
            # which is also what a beginner actually needs to hear.
            ("The United States approved",
             "spot bitcoin exchange traded funds",
             "in early twenty twenty-four,",
             "and it ran to new highs."),
            ("So put the two speeds side by side.",),
            # **`name_columns=True`.** Without it both headings are painted at
            # f=0 and the viewer has to work out which column the voice is on.
            # The second column's first chunk is a **hinge**, not a bare
            # heading — "Now the ones that work in years", never "In years."
            ("In hours.",
             "A whale's sell order.",
             "A regulator's announcement.",
             "A headline anyone can trade.",
             "Now the ones that work in years.",
             "A change to the protocol.",
             "Legal clarity, or none.",
             "Whether the thing still works."),
        ],
        shots=[
            Shot(clip=KEYS / "8212370.mp4", clip_at=1.0),
            Shot(clip=CODE / "14003933.mp4", clip_at=2.0,
                 payload=("", "The rules everyone agreed to follow")),
            Shot(image=POSTS / "hacker.jpg", zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(clip=SERVER / "7140928.mp4", clip_at=1.0),
            Shot(clip=GOVT / "35120905.mp4", clip_at=6.0,
                 payload=("", "The loud ones")),
            Shot(image=POSTS / "global-map.jpg", zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.5),
            Shot(clip=GAVEL / "6699964.mp4", clip_at=2.0,
                 payload=("", "A legal door in")),
            Shot(image=POSTS / "regulators.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="compare",
                 payload=("In hours",
                          ["A whale's sell order",
                           "A regulator's announcement",
                           "A headline anyone can trade"],
                          "In years",
                          ["A change to the protocol",
                           "Legal clarity, or its absence",
                           "Whether the thing still works"],
                          True)),
        ],
        gaps=[0.60, 0.70, 0.60, 0.85, 0.70, 0.65, 0.70, 0.90, 0.90],
    ),

    # --- the twist. A statement card: it resolves, it does not ask. ---------
    Section(
        title="Nobody is driving",
        spoken_title="But none of those three is really the answer.",
        sentences=[
            ("Ask it properly.",
             "Who sets the price of bitcoin",
             "right now, this second?"),
            # Two-phase: the four options sit unmarked while the voice reads
            # them, and the verdicts land in the 2.40 gap afterwards. That
            # silence is the payoff, which is why the beat is not `flow`.
            ("The biggest whale?",
             "The core developers?",
             "A regulator in Washington?",
             "Or the last person willing to sell?"),
            ("The price is whatever",
             "the next buyer and the next seller",
             "agree on."),
            ("Which is why size is not control.",),
            ("A whale holding a hundred thousand coins",
             "cannot sell them at today's price."),
            ("The moment they start,",
             "it stops being today's price."),
            ("There is a plainer way to say it.",),
            ("The price is set by the last person willing to sell.",),
            ("So who controls Bitcoin's price?",
             "Nobody does.",
             "Everybody does."),
        ],
        shots=[
            Shot(image=POSTS / "futuristic-ui.jpg", zoom=1.11,
                 pan=(-0.02, 0.01), aspect=A, bias=0.4),
            Shot(graphic="checklist",
                 payload=([("The biggest whale", False),
                           ("The core developers", False),
                           ("A regulator in Washington", False),
                           ("The last person willing to sell", True)],
                          "WHO SETS THE PRICE?"),
                 picture=POSTS / "security-combination-lock.jpg"),
            Shot(clip=FLOOR / "38569995.mp4", clip_at=5.0),
            Shot(image=POSTS / "defi.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(clip=OCEAN / "5678004.mp4", clip_at=4.0,
                 payload=("", "A hundred thousand coins, and no exit")),
            Shot(clip=CANDLE / "38471109.mp4", clip_at=4.0),
            Shot(image=POSTS / "bitcoin-vs-fiat.jpg", zoom=1.10,
                 pan=(0.02, -0.01), aspect=A, bias=0.5),
            # The line the whole video is built toward. It takes the 2.40 so it
            # has somewhere to land.
            Shot(graphic="quote",
                 payload=("The price is set by the last person willing to sell.",
                          "not by the biggest person holding"),
                 picture=POSTS / "gold.jpg"),
            Shot(clip=WAVES / "27980029.mp4", clip_at=2.0,
                 payload=("", "Nobody does. Everybody does.")),
        ],
        gaps=[0.85, 2.40, 0.70, 0.80, 0.60, 0.90, 0.90, 2.40, 0.85],
    ),

    # --- mirror, echo, and the ask ------------------------------------------
    Section(
        title="So what should you watch?",
        spoken_title="So what should you actually watch?",
        sentences=[
            ("Which changes what is worth watching.",),
            ("Not the whale wallets.",
             "By the time a big transfer shows up,",
             "the trade is already done."),
            ("Watch how much bitcoin",
             "is sitting on exchanges instead."),
            ("Coins moving onto an exchange",
             "are getting ready to sell."),
            ("Coins moving off",
             "are going to sleep."),
            ("So - back to the morning",
             "you woke up to a different number."),
            ("The question was never who moved it.",
             "It is how few people were left to buy."),
            ("Know that,",
             "and it stops looking like a decision,",
             "and starts looking like a room",
             "changing its mind at once."),
            ("The full breakdown is linked below,",
             "and nothing here is financial advice.",
             "If that was useful, subscribe."),
        ],
        shots=[
            Shot(image=POSTS / "man-and-laptop.jpg", zoom=1.12,
                 pan=(-0.02, 0.01), aspect=A, bias=0.4),
            Shot(clip=OCEAN / "5678004.mp4", clip_at=12.0),
            Shot(clip=CHART / "38133087.mp4", clip_at=4.0,
                 payload=("", "How much is sitting on exchanges")),
            Shot(image=POSTS / "futuristic-crypto-exchange.jpg", zoom=1.11,
                 pan=(0.02, -0.01), aspect=A, bias=0.45),
            Shot(image=POSTS / "security-combination-lock.jpg", zoom=1.11,
                 pan=(-0.02, 0.01), aspect=A, bias=0.5),
            # The echo: the picture the video opened on, under the closing
            # lines that reframe the opening ones.
            Shot(clip=PHONE / "35518150.mp4", clip_at=1.0),
            Shot(clip=FLOOR / "38055932.mp4", clip_at=5.0,
                 payload=("", "How few were left to buy?")),
            Shot(image=POSTS / "global-map.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            # Held on the abstract, so YouTube's end-screen cards have
            # somewhere uncluttered to sit when they go on at upload.
            Shot(clip=WAVES / "27980029.mp4", clip_at=0.5),
        ],
        gaps=[0.55, 0.65, 0.70, 0.55, 0.85, 0.80, 0.90, 0.75, 2.80],
    ),
]

META = Meta(
    title="Who Controls Bitcoin's Price? Not Who You Think",
    hook="Whales, developers and governments all get blamed. The real answer "
         "is stranger, and it changes what is worth watching.",
    url=URL,
    summary="What actually moves Bitcoin's price: why the fixed 21 million "
            "supply means every argument is about demand, how whales use a "
            "thin order book, what developers and regulators really change, "
            "and why the price is set by the last person willing to sell.",
    tags=["who controls bitcoin price", "bitcoin price explained",
          "crypto whales", "bitcoin supply and demand", "bitcoin halving",
          "order book explained", "crypto for beginners",
          "bitcoin market manipulation"],
    cta=f"The full breakdown of whales, developers and regulators: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/bitcoin-price-long.mp4"
    work = Path.home() / "Desktop/.bitcoin-price-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # **The title's own question, tightened, with the accent on the word
        # that carries the tension.** The rule this follows is the corrected
        # one: asking the question is not answering it, so a question on the
        # thumbnail opens the loop and closes nothing. Never the answer.
        # **`hacker.jpg` scored better and was rejected as off-message**, which
        # is the skill's own rule biting on a thumbnail rather than on a shot.
        # It is the most arresting picture in the library — a hooded figure at
        # a laptop, whole subject, real black beside it, -0.15 from `_layout`
        # against `analysis.jpg`'s -0.07 — and under the question "who controls
        # Bitcoin's price?" it answers *hackers*, which is a thing this video
        # explicitly denies. A thumbnail may open the loop; it may not point at
        # the wrong answer. `bitcoin-vs-fiat.jpg` was rejected for the same
        # class of reason and harder: it is a man setting fire to a dollar bill,
        # which promises a currency-collapse video. `gold.jpg` is the prettiest
        # of the five and says nothing about price.
        #
        # `analysis.jpg` promises what the video actually is: a market being
        # read. Scored clean at -0.07, right/top, and the type sits on genuine
        # black rather than on a scrim.
        thumb_headline="Who controls [Bitcoin's price?]",
        thumb_image=POSTS / "analysis.jpg",
        thumb_accent="orange",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
