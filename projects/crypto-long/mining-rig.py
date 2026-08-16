"""How to build a mining rig — long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/how-to-build-a-mining-rig.mdx (~2,000 words).
**This is the top-demand page on the site — 1,510 views, first on the ranking in
`docs/long-form-strategy.md`** — and it is also the one page on that list whose
title is already a YouTube query typed verbatim. There is no short from this
post, so unlike the first two pilots there is no angle to inherit.

**The article is a parts list; the video cannot be.** A table of nine components
read aloud is a specification, not a piece, and it would fail the arc the skill
requires within thirty seconds. So the script takes the thing the article buries
in section two and puts it in the first ten seconds: **the electricity price
decides this, not the hardware.** That is the honest answer to the query, it is
the article's own emphasis ("often below $0.05/kWh"), and it turns a shopping
list into a question the viewer has a stake in.

The arc:

* **Hook** — the garage photo everyone has seen, then the number underneath it.
* **Reframe** — a home rig against an industrial farm. Four variables, not one.
* **Deep dive** — the parts, which is what the query actually came for.
* **Twist** — the cheapest component on the list is the one that starts fires.
  The article bolds the SATA-adapter warning twice and it is genuinely
  counterintuitive: the danger is not the two-thousand-dollar cards.
* **Mirror** — the build is the easy half; the money is made undervolting.
* **Echo** — back to the garage, reframed as a question about the meter.

**No financial advice, and this topic invites it harder than Saylor did.**
"Should you build one" is one sentence from "here is how to make money". The
script never says a rig will pay; it says the calculator decides and hands the
viewer the calculator. The close is a question about the power bill, not a
verdict about mining.

**Stock screening rejected two obvious picks and both are worth recording.**
`crypto-mining-rig-hardware/854969.mp4` measures L27 on its opening frame and
**L88 by second six** — it is a push-in onto a cream-coloured case, and screening
one frame would have shipped it. `calculator-money-desk-dark/6266425.mp4` is the
single most on-message clip found for the profitability line (hands, cash, a
calculator) and sits at a sustained L55-60 in a lilac cast; taken out anyway,
and a `stat` carries that moment instead. **Screen across the clip, not at one
second.**

**The site library cannot picture this post and that is the headline finding.**
`bitcoin-mining.jpg` (L106) and `bitcoin-renewable-energy.jpg` (L132) — the two
most on-topic photographs it owns — are both out on brightness, and the hero
`mining-rig.jpg` (L102, over the ~L82 working ceiling) is a woman in safety
goggles holding a bare motherboard, which is not a mining rig. Six screened
stock stills carry the hardware inside the video instead; the hero is kept for
the thumbnail on the user's instruction, where it is the picture the article
already trained its readers to recognise. This is the strategy doc's picture
constraint at its sharpest, arriving on the post that needed the pictures most.

**Numbers are the article's own.** Five cents a kilowatt hour, twenty percent
power-supply headroom, eight gigabytes of memory, seventy to seventy-five
degrees. Nothing about hashrates or payback periods, because the article states
none and inventing one would be the advice this must not give.

**Phonemes.** No initialism is spoken. "GPU" is "graphics card", "PSU" is
"power supply", "SATA" appears on screen only, and ASIC is "a purpose-built
machine" — the synthesiser makes a meal of all four.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/mining-rig.py
"""

from pathlib import Path

from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"

# Pexels, cached under assets/stock/ and screened across the clip rather than at
# one second — the trailing comment is the luma/saturation range over its whole
# length, not a single frame.
RIG = STOCK / "videos/computer-cooling-fan-dark"        # L35-51 S42-50
BOARD = STOCK / "videos/motherboard-computer-close-up-dark"  # L37-39 S35-36
POWER = STOCK / "videos/electricity-power-lines-night"  # L13-14 S14-16
KEYS = STOCK / "videos/typing-keyboard-night"           # L20-25 S10-12
SERVER = STOCK / "videos/server-room-data-center"       # L29 S43
CIRCUIT = STOCK / "videos/circuit-board-macro-dark"     # L41 S20
STREAM = STOCK / "videos/digital-code-stream-dark"      # L14 S6
WAVES = STOCK / "videos/abstract-dark-waves-motion"     # L4 S5
PARTICLES = STOCK / "videos/dark-abstract-digital-particles"  # L9 S0

# **Stock stills, and why they were needed.** The first cut used the site's own
# `hacker.jpg`, `gamers.jpg`, `bitcoin.jpg` and `man-and-laptop.jpg` in the four
# places the script names hardware, and every one of them was wrong on the
# frame: a hooded figure under a line about purpose-built machines reads as
# crime, a neon arcade reads as gaming, and a gold coin on a white laptop is
# not a graphics card. **The library has no picture of mining hardware** — the
# two that come closest, `bitcoin-mining.jpg` and `bitcoin-renewable-energy.jpg`,
# are out on brightness. This is the strategy doc's picture constraint at its
# sharpest, and stock stills are the answer to it here.
CARDS = STOCK / "photos/graphics-card-gpu-dark/8622912.jpg"      # L27 S4
RIGFANS = STOCK / "photos/graphics-card-gpu-dark/34552790.jpg"   # L32 S24
CARDPAIR = STOCK / "photos/crypto-mining-farm-rigs/4581613.jpg"  # L57 S13
MESH = STOCK / "photos/computer-hardware-motherboard-dark/8108683.jpg"    # L20 S17
BOARDMONO = STOCK / "photos/computer-hardware-motherboard-dark/3520699.jpg"  # L29 S0
BOARDMACRO = STOCK / "photos/computer-hardware-motherboard-dark/36169772.jpg"  # L42 S15

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # female, af_heart. Candidate, not approved.
MUSIC = "pulse"                 # 112 BPM, plucked, no air layer.

URL = "https://thecrypto.wiki/posts/how-to-build-a-mining-rig"

A = 16 / 9                      # crop toward the frame, not the shorts' 1.15


SECTIONS = [
    # --- the hook. No card: an opening chapter card spends the one second
    # that decides whether anybody stays. --------------------------------
    #
    # **It opens on motion, not on a photograph.** The first cut held one still
    # image for the first seven seconds and the user's word for it was boring —
    # correctly, because a Ken Burns move on a still is the slowest thing in the
    # format and putting it where the drop is steepest is the worst possible
    # place for it. A clip is moving on frame one.
    Section(
        title="The number under the photo",
        card=False,
        sentences=[
            ("You have seen the picture.",
             "A metal frame,",
             "six graphics cards,",
             "a wall of fans in somebody's garage."),
            ("It looks like a money printer.",
             "Is it one?"),
            # The retention call, said out loud and kept at the end. It is the
            # same question the outro asks, which is the point: a promise the
            # viewer can hear being made is what buys the next three minutes.
            ("Stay to the end",
             "and you will know whether to build one."),
            ("Because the whole thing turns",
             "on a single figure,",
             "and it is not on the box."),
            ("Five cents.",),
            ("That is roughly what a profitable miner",
             "pays for one kilowatt hour of electricity."),
            ("Ordinary home power costs considerably more,",
             "so the first thing to check",
             "is your bill, not your budget."),
            ("Along the way:",
             "every part that goes in,",
             "the one that starts fires,",
             "and how to run the sum yourself."),
        ],
        shots=[
            Shot(clip=RIG / "33356261.mp4", clip_at=1.0),
            None,                                    # ride the motion
            # The title stamp, on the line that makes the promise.
            Shot(clip=POWER / "5766693.mp4",
                 payload=("", "SHOULD YOU BUILD A MINING RIG?")),
            Shot(clip=BOARD / "6754818.mp4", clip_at=2.0,
                 payload=("", "It is not on the box")),
            Shot(graphic="stat",
                 payload=("$0.05", "PER KILOWATT HOUR",
                          "Below this, mining can pay. Above it, usually not."),
                 backdrop=POSTS / "bitcoin-neon.jpg"),
            None,
            Shot(image=POSTS / "digital-technology.jpg", zoom=1.11,
                 pan=(-0.02, 0.01), aspect=A, bias=0.45),
            # **Not `proof-of-work.jpg`.** That is an infographic, and a Ken
            # Burns move on a diagram crops its own title off the top and its
            # last row off the bottom — which is what shipped, and what the
            # user caught at 0:27. A site infographic cannot take a crop, and
            # at 660px in a beat's picture column its labels are unreadable,
            # so it has no full-frame use in this format at all. As a blurred
            # backdrop it is only texture, which is fine and is where it went.
            Shot(image=BOARDMACRO, zoom=1.10, pan=(0.02, 0.01), aspect=A,
                 bias=0.5),
        ],
    ),

    # --- reframe: it is an energy business, not a hardware hobby ---------
    Section(
        title="What are you actually competing with?",
        sentences=[
            ("Mining is not really a hardware hobby.",
             "It is an energy business",
             "wearing a hardware costume."),
            # **The point, then the list.** This line sat *after* the
            # comparison in the first cut and the user found it confusing —
            # rightly: a viewer who has already read both columns does not need
            # to be told what they were, and a graphic that arrives before its
            # own thesis has to be decoded rather than read.
            ("And this is who you are bidding against.",),
            ("A handful of cards.",
             "Power at the price your utility charges.",
             "Heat and noise you live with.",
             "Thousands of machines in one building.",
             "Built beside a dam or a geothermal field.",
             "Electricity bought in industrial bulk."),
            ("It also gets harder on its own.",),
            ("As more machines join,",
             "difficulty rises,",
             "so the same rig earns less each month",
             "for the same work."),
            ("Four numbers decide this,",
             "and only one is the hardware."),
            ("Your electricity cost.",
             "Your hardware's efficiency.",
             "The coin's price.",
             "The network's difficulty."),
            ("Put all four into a mining calculator",
             "before you buy a single part."),
        ],
        shots=[
            Shot(image=MESH, zoom=1.11, pan=(-0.02, 0.01), aspect=A, bias=0.4),
            Shot(clip=SERVER / "7140928.mp4",
                 payload=("", "This is who you are bidding against")),
            Shot(graphic="compare",
                 payload=("Your spare room",
                          ["A handful of cards",
                           "Power at retail price",
                           "Heat and noise you live with"],
                          "An industrial farm",
                          ["Thousands of machines",
                           "Built beside a dam",
                           "Electricity bought in bulk"]),
                 backdrop=POSTS / "futuristic-data-center.jpg"),
            None,
            Shot(image=POSTS / "analysis.jpg", zoom=1.12, pan=(0.02, -0.01),
                 aspect=A, bias=0.45),
            Shot(image=POSTS / "portfolio.jpg", zoom=1.11, pan=(-0.02, -0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="checklist",
                 payload=([("Your electricity cost", True),
                           ("Your hardware's efficiency", True),
                           ("The coin's price", True),
                           ("The network's difficulty", True)],
                          "WHAT DECIDES PROFIT"),
                 picture=POSTS / "laptop-trading.jpg"),
            Shot(image=POSTS / "futuristic-ui.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.4),
        ],
        # The checklist's own sentence buys the pause: four variables sit
        # unmarked, the voice stops, the ticks land into the silence.
        gaps=[0.34, 0.34, 0.34, 0.34, 0.34, 0.34, 2.40, 0.34],
    ),

    # --- the deep dive: the parts. What the query actually came for. -----
    Section(
        title="So what goes into a rig?",
        sentences=[
            ("Assume the sum works.",
             "Here is the shopping list."),
            ("One thing first.",
             "Bitcoin is mined by purpose-built machines",
             "you buy, not build."),
            ("Everything here is the other family:",
             "graphics cards, mining coins",
             "designed to stay out of their reach."),
            ("Six parts carry the build.",),
            # **A `grid`, not a checklist** — see `beats.Grid`. Six ticked rows
            # in a left column is the same silhouette as the four-item
            # checklist forty seconds earlier, and the user saw the two as one
            # graphic. Cards across the full width read as objects, and the
            # second line on each is room a list does not have.
            ("A motherboard with enough slots.",
             "A cheap processor.",
             "Eight gigabytes of memory.",
             "The graphics cards themselves.",
             "A serious power supply.",
             "An open frame, so air can move."),
            ("Then the small things",
             "that are not small:",
             "riser cards to space the graphics cards apart,",
             "extra fans, and a drive for the software."),
            ("One rule on the power supply.",),
            ("Add the wattage up,",
             "then buy twenty percent more.",
             "A supply running flat out",
             "wastes power as heat."),
        ],
        shots=[
            Shot(clip=RIG / "33356261.mp4", clip_at=8.0,
                 payload=("", "The shopping list")),
            # The green server room, on the line that is actually about
            # industrial single-purpose machines.
            Shot(image=POSTS / "data-center.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.4),
            Shot(image=CARDS, zoom=1.12, pan=(0.02, 0.01), aspect=A, bias=0.45),
            None,
            Shot(graphic="grid",
                 payload=([("Motherboard", "Enough slots for every card"),
                           ("A cheap processor", "It does no real work"),
                           ("8 GB of memory", "Enough for any mining OS"),
                           ("The graphics cards", "Where the hashing happens"),
                           ("A serious power supply", "Gold rated, 20% headroom"),
                           ("An open frame", "So the air can actually move")],
                          "THE SIX THAT MATTER"),
                 backdrop=MESH),
            Shot(clip=CIRCUIT / "6755170.mp4",
                 payload=("", "And the small things that are not small")),
            None,
            Shot(graphic="stat",
                 payload=("+20%", "POWER SUPPLY HEADROOM",
                          "Above the rig's total draw. Not optional."),
                 backdrop=POSTS / "digital-technology.jpg"),
        ],
    ),

    # --- the twist. A statement card: it resolves, it does not ask. ------
    Section(
        title="The cheapest part is the dangerous one",
        spoken_title="And the cheapest part is the dangerous one.",
        sentences=[
            ("Everyone worries about the graphics cards.",
             "They cost the most,",
             "so they get the attention."),
            ("The part that burns houses down",
             "costs about two dollars."),
            ("Riser cards need their own power,",
             "and there is a cheap adapter",
             "that lets you take it",
             "from the drive connector instead."),
            ("It fits. It works. It is a known fire hazard.",),
            ("Those connectors were designed",
             "for a hard drive,",
             "not for a card pulling",
             "seventy-five watts."),
            ("Run a proper six-pin cable",
             "from the power supply to every riser.",
             "Directly.",
             "Every time."),
            ("It is the one instruction in this build",
             "with no acceptable shortcut."),
        ],
        shots=[
            Shot(image=CARDPAIR, zoom=1.10, pan=(0.02, -0.01), aspect=A,
                 bias=0.5),
            None,
            Shot(clip=BOARD / "6754818.mp4", clip_at=12.0,
                 payload=("", "Risers need their own power")),
            Shot(graphic="quote",
                 payload=("Never power a riser through a SATA adapter.",
                          "the one rule with a fire behind it"),
                 picture=POSTS / "data-center.jpg"),
            None,
            Shot(clip=RIG / "33356261.mp4", clip_at=9.5,
                 payload=("", "Six-pin. Direct. Every time.")),
            Shot(image=POSTS / "security-combination-lock.jpg", zoom=1.11,
                 pan=(-0.02, 0.01), aspect=A, bias=0.45),
        ],
        gaps=[0.34, 0.34, 0.34, 1.60, 0.34, 0.34, 0.34],
    ),

    # --- mirror: the half nobody photographs -----------------------------
    # **Written as a real question**, card and voice both. The first cut titled
    # this "Where the money is actually made" — a question's word order with a
    # statement's full stop, so the synthesiser read it flat and the card
    # printed no question mark. If a title is shaped like a question, punctuate
    # it like one; the rising intonation is free and the card earns its turn.
    Section(
        title="So where is the money actually made?",
        sentences=[
            ("Bolting the frame together",
             "is a Saturday afternoon."),
            ("The half that decides your result",
             "happens after it boots,",
             "and nobody photographs it."),
            # A `steps` beat: this is a sequence, and order is the one thing
            # none of the other beats can show.
            ("You install the mining system.",
             "Then the drivers.",
             "Then the mining software.",
             "You join a pool, which shares the work.",
             "And then you turn the power down."),
            ("That last one sounds backwards.",
             "It is the whole game."),
            ("Undervolting lowers what each card draws",
             "while keeping almost all of its speed —",
             "and electricity was the deciding number."),
            ("Watch the temperatures while you do it.",),
            ("Above seventy-five degrees",
             "you are trading the hardware's life",
             "for numbers you can read today."),
        ],
        shots=[
            Shot(image=BOARDMONO, zoom=1.12, pan=(0.02, 0.01), aspect=A,
                 bias=0.4),
            None,
            Shot(graphic="steps",
                 payload=(["Install the mining OS", "Install the drivers",
                           "Configure the miner", "Join a pool",
                           "Undervolt and test"],
                          "AFTER IT BOOTS"),
                 backdrop=POSTS / "proof-of-work.jpg"),
            Shot(clip=KEYS / "8212370.mp4", clip_at=2.0,
                 payload=("", "This is the whole game")),
            Shot(image=POSTS / "futuristic-ui.jpg", zoom=1.11,
                 pan=(-0.02, -0.01), aspect=A, bias=0.45),
            Shot(clip=CIRCUIT / "6754824.mp4",       # L41-43 S36-37
                 payload=("", "Watch the temperatures")),
            Shot(graphic="stat",
                 payload=("75°C", "THE CEILING",
                          "Past it you are spending the hardware's life."),
                 backdrop=POSTS / "bitcoin-neon.jpg"),
        ],
    ),

    # --- echo, and the ask ------------------------------------------------
    Section(
        title="So is it worth it?",
        sentences=[
            ("Back to that garage.",),
            ("The frame and the fans",
             "were never the hard part."),
            ("The hard part is that you are running",
             "a small power station",
             "against people who built theirs",
             "next to a dam."),
            ("So the honest version of the question",
             "is not: can I build one."),
            ("It is: what does your electricity cost?",),
            ("Work that out first.",
             "The full parts list",
             "and the safety warnings",
             "are linked below —",
             "and nothing here is financial advice."),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            # The same picture the video opened on, so the closing line's echo
            # has a visual one under it.
            Shot(clip=RIG / "33356261.mp4", clip_at=1.0),
            Shot(clip=PARTICLES / "36703282.mp4"),
            Shot(image=POSTS / "global-map.jpg", zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(clip=STREAM / "34127877.mp4",
                 payload=("", "Not: can I build one")),
            Shot(graphic="stat",
                 payload=("$0.05", "THE WHOLE QUESTION",
                          "Everything else is shopping."),
                 backdrop=POSTS / "bitcoin-neon.jpg"),
            Shot(image=BOARDMACRO, zoom=1.10, pan=(-0.02, -0.01), aspect=A,
                 bias=0.45),
            # Held on the abstract, so YouTube's end-screen cards have
            # somewhere uncluttered to sit when they go on at upload.
            Shot(clip=WAVES / "15690300.mp4"),
        ],
        # 2.40 on the question the video builds to — the beat carrying it
        # would otherwise be gone in under two seconds.
        gaps=[0.34, 0.34, 0.34, 0.34, 2.40, 0.34, 2.80],
    ),
]

META = Meta(
    title="How To Build a Crypto Mining Rig (And Whether You Should)",
    hook="Every part that goes into a GPU mining rig, the one that starts fires, "
         "and the number that decides whether any of it pays.",
    url=URL,
    summary="A step-by-step walkthrough of building a GPU mining rig: the six "
            "core components, the riser wiring mistake that is a genuine fire "
            "hazard, the software and pool setup, and why undervolting matters "
            "more than the hardware you buy.",
    tags=["mining rig", "crypto mining", "gpu mining", "bitcoin mining",
          "how to build a mining rig", "mining profitability"],
    cta=f"Full parts list, assembly steps and safety warnings: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: generated for this channel.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-mining-rig-long.mp4"
    work = Path.home() / "Desktop/.crypto-mining-rig-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title carries the search phrase — "how to build a mining rig" is
        # typed into YouTube verbatim — so the thumbnail asks what the title
        # does not, and asks the question that actually decides it.
        #
        # **The user's call, against both the scorer and the skill's own
        # "ask what the title does not" rule.** `mining-rig.jpg` scores +0.82
        # busy and is a woman holding a bare board rather than a rig, and the
        # first cut therefore used a stock GPU with an electricity headline.
        # The user wants the article's own hero and a headline about building,
        # and that is the right call for a reason the scorer cannot see: this
        # thumbnail sits on the article page as well as in the YouTube feed,
        # where a picture the reader has already scrolled past is recognition
        # rather than repetition. The electricity angle stays where it belongs,
        # in the video's first ten seconds.
        # The accent takes "mining rig", not "Build" — the plate should land on
        # the subject, which is also the search phrase, not on the verb.
        thumb_headline="Build your own [mining rig]",
        thumb_image=POSTS / "mining-rig.jpg",
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
