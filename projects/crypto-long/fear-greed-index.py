"""What is the Crypto Fear & Greed Index? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/crypto-fear-and-greed-index-for-beginners.mdx.

**The angle.** The article spends most of its length on how to *use* the index
as a contrarian trading tool - buy more in extreme fear, scale out in extreme
greed. None of that goes in the video. The one idea a beginner actually needs
is the mechanism: a single 0-100 score blended from six weighted inputs, that
measures the crowd's *mood* rather than the market's value - and the reason it
swings so hard is that fear and greed are both self-reinforcing loops. What
the score cannot do (predict, judge, replace research, signal a trade) is the
video's own twist, not a caveat bolted on at the end.

**No financial advice, anywhere.** No token or platform is named, no price
level or direction is given, nothing is recommended to buy, sell, hold or
avoid. Every drawn reading of the dial is parked at the midpoint for the same
reason: a needle pinned into the red would read as a claim about today's
market, which is exactly the claim this channel never makes.

## The re-cut, and why the first one was wrong

**The first cut was rejected for irrelevant stock footage, and the diagnosis
is worth keeping because it generalises to every abstract topic on both
channels.** The shot list ran a fireworks festival under "plenty of people
check it", a woman celebrating under string lights under the greed line, and
a metronome, a rain window and three portraits under claims about *a number*.
None of it was wrong by the screening rules - every clip was dark, on-palette,
unused elsewhere and passed `audit_assets.py`.

The fault was upstream of screening: **the nouns in this script are "a
number", "a score", "a scale" and "a feedback loop", and none of them has a
photographic referent at all.** A shot list built from stock will therefore
always drift to mood - somebody looking worried, somebody celebrating - because
that is the only thing a stock library has for an abstraction. `footage.md`'s
"say the noun the narration says" cannot be satisfied here by choosing better
footage. It can only be satisfied by *drawing the noun*.

So this cut inverts the ratio. Eight of twenty-six shots are drawn graphics or
the site's own scale, against the format's usual four to nine, and **every
remaining clip shows a screen, a hand on a phone, or people in numbers** -
which is what "checking an index" actually looks like. Dropped entirely:
the fireworks crowd, the string-light celebration, the hands-in-hair portrait
and the frontal studio portrait.

**A second thing fell out of that, and it is the more important one.** Most of
the replaced shots were close-up faces, and `footage.md` already records why
this pipeline keeps producing the same casting: screening on `MAX_LUMA`
against dark backdrops selects for it structurally, whatever the search query
says. Shooting an abstract topic through hands, screens and crowds instead of
portraits removes the question from most slots rather than trying to steer a
filter that does not steer. The rule is written up in `footage.md`.

## The beats

`dial` is **new, and was built for this video** - a radial 0-100 gauge with
the index's own five band colours and a needle that sweeps on the voice. It is
the literal subject of the piece and nothing in the library could draw it;
`gauge` is one value against one threshold and has a straight track, which
reads as a stacked bar the moment five colours go on it. See `beats.md`.

Set, checked against the last three crypto long-forms (rug-pull: diagram /
grid / gauge / steps / stat; vitalik: compare / grid / quote / stat / steps;
perpetual: bars / checklist / compare / logos / stat) - `stat` ran in all
three in a row and is dropped here:

* `dial` x2 - the scale, then the midpoint
* `bars` - the six weighted inputs
* `diagram(loop=True)` - fear feeding itself
* `quote` - the Buffett line
* `checklist` - the four things the score cannot do, all struck

Plus two composed stills, which carry the two longest sentences in the script
because **a still has no stretch ceiling and a clip does**: the site's own
legend (`fear-greed-legend.png`) and the sentiment history
(`fear-greed-wave.png`, from `tools/make_wave.py`).

**`fear-greed-legend.png`** is a crop of the site's own
`public/images/posts/fear-and-greed-index.png` - the bottom legend row only,
at 2x. The full source also carries a live "Current Index: 98 - Extreme Greed
/ Last updated: 3/28/2025" reading, which is stale and reads as a claim about
today if left in. The legend strip is timeless: the site's own five band names
in the site's own colours.

**Thumbnail: the dial, and no person in it.** `fear-greed-dial.png` is the
`dial` beat rendered as a still and shifted right, so the headline sits on
real black. The previous thumbnail was a stock portrait that said nothing
about the topic - see `thumbnails.md`.

**Phonemes, checked with espeak-ng.** "Buffett", "volatility", "dominance",
"sentiment", "momentum" all phonemize correctly as written.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/fear-greed-index.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"
V = STOCK / "videos"
PH = STOCK / "photos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

# --- the roster: screens, hands and people in numbers. No portrait carries a
# claim about a number in this cut - see the module docstring.
# Used **once**, and not on the opener: the best-composed clip in the roster
# is running a photo editor on its phone, legibly. See `footage.md`.
PHONE_HAND = V / "person-holding-phone-screen-glow-dark-night/17643375.mp4"  # 11.2s L13-15 S11, a hand and a lit phone on black
DESK = V / "man-looking-at-laptop-screen-glow-dark/33874628.mp4"     # 17.8s L9-12 S10-14, someone at a desk with a phone, night
FACE2 = V / "man-checking-phone-anxious-dark-room/7280528.mp4"       # 18.1s L42 S24, a reaction to something on a phone
TYPING = V / "hands-typing-phone-dark-close-up-night/33942937.mp4"   # 15.4s L11-14 S4-5, thumbs on a phone, close
PHONE1 = V / "woman-looking-at-phone-reaction-dark/7986753.mp4"      # 20.6s L7-9 S1-2, two people reading one phone
SCROLL = V / "man-scrolling-social-media-phone-dark/13358555.mp4"    # 14.5s L14 S5, a hand scrolling a feed
FACE1 = V / "man-checking-phone-anxious-dark-room/8212368.mp4"       # 11.7s L9-11 S9-11, a face lit by its own phone
PENDULUM = V / "pendulum-swinging-dark-macro/29339462.mp4"           # 21.6s L21-26 S1-2, a metronome ticking - on "swings", once
TRAIN = V / "subway-train-passengers-phones-dark/36111567.mp4"       # 15.3s L18-21 S10-12, a night train, lit windows, passengers
RAIN = V / "rain-window-night-dark-slow/4458918.mp4"                 # 9.9s L20-21 S16-23, rain on a window - the disclaimer shot

# Composed stills. Both carry long sentences on purpose: a still has no
# stretch ceiling, and a clip that is short for its slot kills the render.
LEGEND = BRAND / "graphics/fear-greed-legend.png"                    # 1340x80, the site's own scale, cropped + 2x
WAVE = BRAND / "graphics/fear-greed-wave.png"                        # 1920x1080, tools/make_wave.py
BEATGROUND = BRAND / "beat-ground-crypto.jpg"                        # warm near-black bloom behind every drawn beat

THUMB = BRAND / "graphics/fear-greed-dial.png"                       # the dial beat, rendered as a still

ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/crypto-fear-and-greed-index-for-beginners"
A = 16 / 9

# The index's own bands and the site's own hex values, so the dial, the
# legend crop and the wave all agree with each other and with the site.
BANDS = [("Extreme fear", 0.25, "#f85032"), ("Fear", 0.50, "#ff7e5f"),
         ("Neutral", 0.55, "#f2c94c"), ("Greed", 0.75, "#a8ff78"),
         ("Extreme greed", 1.00, "#56ab2f")]

E_FALL, E_FEAR, E_SELL = "\U0001F53B", "\U0001F628", "\U0001F4E4"


SECTIONS = [
    # --- hook. No card. Open on motion: a hand and a lit screen. ----------
    Section(
        title="The mood ring",
        card=False,
        sentences=[
            ("One number claims to know the crypto market's mood.",),
            ("It runs from zero to a hundred -",
             "fear on one end, greed on the other."),
            ("Plenty of people check it before they check the price itself -",
             "because a mood is easier to read than a chart."),
            ("Stay to the end,",
             "and you will know exactly what this number is measuring -",
             "and just as importantly, what it is not."),
        ],
        shots=[
            # **Thumbs on a phone, not the hand-and-phone shot**, which is the
            # better composition and has a legibly *wrong* screen on it: its
            # phone is running a photo editor, sliders and all, which a viewer
            # reads under "a number that measures mood". A prop's screen is a
            # noun like any other - see `footage.md`.
            Shot(clip=TYPING, clip_at=1.0),
            # The scale, with no needle on it. One reveal, because the line
            # describes the instrument rather than a reading on it.
            Shot(graphic="dial", backdrop=BEATGROUND,
                 payload=(BANDS, None, "", "A SCORE FROM 0 TO 100")),
            # A carriage of people each on their own screen, not a crowd:
            # `crowd-walking-city-night-dark-aerial` measured L19 and still
            # rendered as an unreadable smear once `VideoShot` dimmed it, so
            # "plenty of people" was a dark frame with nothing in it.
            Shot(clip=TRAIN, clip_at=1.0,
                 payload=("", "What Is the Crypto Fear & Greed Index?")),
            Shot(clip=DESK, clip_at=1.0),
        ],
        gaps=[0.55, 0.70, 0.60, 0.85],
    ),

    # --- reframe: a mood score, not a price -------------------------------
    Section(
        title="What does the number actually measure?",
        spoken_title="So what is this number actually measuring?",
        sentences=[
            ("It is not a price.",
             "It is a sentiment score -",
             "one figure standing in for how fearful or how greedy the "
             "market feels at any given moment."),
            # The dial's own sentence: scale first, needle second.
            ("Score under fifty, and the reading leans toward fear.",
             "Score over fifty, and it leans toward greed."),
            ("It updates every single day,",
             "sometimes more than once, as fresh data rolls in."),
            ("Five bands, from extreme fear to extreme greed.",),
            ("But a mood is not something you can just read off one "
             "sensor -",
             "so how does one number claim to summarize an entire "
             "market's feelings?"),
        ],
        shots=[
            Shot(clip=FACE2, clip_at=1.0),
            Shot(graphic="dial", backdrop=BEATGROUND,
                 payload=(BANDS, 0.5, "Neutral", "WHERE THE LINE FALLS")),
            # The metronome again, on cadence rather than on swing: "it
            # updates every single day" is a regular beat, which is the one
            # thing this clip unambiguously shows.
            Shot(clip=PENDULUM, clip_at=10.0),
            # The site's own legend - a still, so no Ken Burns crops it.
            Shot(image=LEGEND, zoom=1.0, pan=(0.0, 0.0), aspect=1340 / 80),
            Shot(clip=PHONE1, clip_at=1.0),
        ],
        gaps=[0.55, 0.60, 0.55, 0.60, 0.85],
    ),

    # --- deep dive: six weighted inputs, blended into one score -----------
    Section(
        title="How does that score get built?",
        spoken_title="So how exactly does that score get built?",
        sentences=[
            ("So the score is not one measurement -",
             "it is six, blended into one."),
            # the bars' own sentence - one caption chunk per row.
            ("Volatility, twenty-five percent - how wild the price swings "
             "have been,",
             "market momentum and trading volume, another twenty-five,",
             "social media chatter, fifteen percent,",
             "historical survey data, fifteen percent, when it is running,",
             "bitcoin's share of the whole market, ten percent,",
             "and search trends - what people are actually typing into "
             "Google - the last ten."),
            ("It pulls straight from Bitcoin's own trading data,",
             "and from what people are actually saying about it."),
            ("None of that is a price.",
             "All of it is a mood."),
        ],
        shots=[
            Shot(clip=SCROLL, clip_at=1.0),
            Shot(graphic="bars", backdrop=BEATGROUND,
                 payload=([("Volatility", 0.25, "25%"),
                           ("Momentum & volume", 0.25, "25%"),
                           ("Social sentiment", 0.15, "15%"),
                           ("Surveys", 0.15, "15%"),
                           ("Bitcoin dominance", 0.10, "10%"),
                           ("Search trends", 0.10, "10%")],
                          "HOW THE SCORE IS BUILT")),
            Shot(clip=DESK, clip_at=9.0),
            Shot(clip=FACE1, clip_at=1.0),
        ],
        gaps=[0.60, 0.70, 0.55, 0.85],
    ),

    # --- twist: fear and greed are both self-reinforcing loops ------------
    Section(
        title="Why does it swing so hard?",
        spoken_title="So why does the market swing between the two so hard?",
        sentences=[
            ("The reason the number swings so hard is not mysterious -",
             "sentiment feeds on itself."),
            # the diagram's own sentence - one caption chunk per node.
            ("Prices dip,",
             "fear spreads, because a falling chart reads as danger,",
             "and fear turns into more selling - which drops the price "
             "further, and starts the loop again."),
            ("Flip it around, and greed runs the exact same loop upward -",
             "which is why extremes on this index can run so far, in "
             "either direction."),
        ],
        shots=[
            Shot(clip=PENDULUM, clip_at=1.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("Prices dip", "the first move", E_FALL),
                           ("Fear spreads", "a falling chart reads as danger",
                            E_FEAR),
                           ("More selling", "fear becomes the next drop",
                            E_SELL)],
                          "WHY SENTIMENT FEEDS ON ITSELF", True)),
            # The history, as one shape. A beat that revealed it left to
            # right would be drawing a forecast; a still is a record.
            Shot(image=WAVE, zoom=1.0, pan=(0.0, 0.0), aspect=A),
        ],
        gaps=[0.55, 0.85, 0.85],
    ),

    # --- why people watch it: the Buffett line -----------------------------
    Section(
        title="Why do millions watch a mood?",
        spoken_title="So why do millions of people bother watching a mood?",
        sentences=[
            ("There's a reason this index has millions of readers,",
             "and it traces back to one old line about market psychology."),
            ("Be fearful when others are greedy,",
             "and greedy when others are fearful."),
            ("Extreme readings on this index have shown up again and "
             "again, in cycle after cycle -",
             "long before this particular chart ever existed."),
            ("The index itself is not a crystal ball -",
             "it is just a number trying to measure which side of that "
             "line the crowd is standing on."),
        ],
        shots=[
            Shot(clip=TRAIN, clip_at=6.0),
            Shot(graphic="quote", backdrop=BEATGROUND,
                 payload=("Be fearful when others are greedy, and greedy "
                          "when others are fearful.", "Warren Buffett")),
            Shot(clip=SCROLL, clip_at=5.0),
            Shot(clip=PHONE1, clip_at=10.0),
        ],
        gaps=[0.60, 1.10, 0.60, 0.85],
    ),

    # --- mirror, echo, the ask ----------------------------------------------
    Section(
        title="Can you trade off this number?",
        spoken_title="So can you actually trade off this number?",
        sentences=[
            ("Here is what that score cannot do,",
             "no matter which way it points."),
            # the checklist's own sentence - flow=True, one chunk per item.
            ("It cannot predict where the price goes next,",
             "it cannot tell you whether any project is actually any "
             "good,",
             "it cannot replace your own research,",
             "and it was never built to be a signal to buy or sell "
             "anything."),
            ("It only measures one thing -",
             "how the crowd feels, this minute, and nothing else."),
            ("That is not a flaw somebody forgot to fix -",
             "it is the entire design:",
             "never built to predict, only to describe."),
            ("Nothing in this video is financial advice.",),
            ("So the next time that number swings from fear to greed -",
             "whose mood do you think it is actually measuring:",
             "the market's, or yours?"),
        ],
        shots=[
            Shot(clip=FACE2, clip_at=9.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Predict where the price goes next.", False),
                           ("Tell you whether any project is actually "
                            "any good.", False),
                           ("Replace your own research.", False),
                           ("Work as a signal to buy or sell anything.",
                            False)],
                          "CAN YOU TRADE OFF THIS NUMBER ALONE?", True)),
            Shot(clip=PHONE_HAND, clip_at=3.0),
            Shot(clip=FACE1, clip_at=3.0),
            Shot(clip=RAIN, clip_at=1.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=TYPING, clip_at=6.0),
        ],
        gaps=[0.60, 0.85, 0.70, 0.60, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is the Crypto Fear and Greed Index?",
    hook="One number claims to measure whether the crypto market is scared "
         "or greedy. Here is exactly how that score is built, why it "
         "swings so hard between the two - and what it can never tell you.",
    url=URL,
    summary="What the Crypto Fear & Greed Index actually is: a 0-100 "
            "sentiment score blended from six weighted inputs - volatility, "
            "momentum and volume, social media chatter, surveys, Bitcoin "
            "dominance and search trends. Why fear and greed both run as "
            "self-reinforcing loops, the Buffett line behind why anyone "
            "tracks this at all, and the four things the score can never "
            "do - predict a price, judge a project, replace research, or "
            "act as a buy or sell signal. Nothing here is financial advice.",
    tags=["crypto fear and greed index", "what is the fear and greed index",
          "crypto market sentiment", "bitcoin fear and greed",
          "crypto fear and greed explained", "market psychology crypto",
          "crypto for beginners", "how the fear and greed index works",
          "crypto sentiment analysis", "warren buffett fear and greed"],
    cta=f"The full guide - how to read every band, and the limits of using "
        f"it as a tool: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Fear & Greed Index scale: thecrypto.wiki.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-fear-greed-index-long.mp4"
    work = Path.home() / "Desktop/.crypto-fear-greed-index-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        thumb_headline="This number claims to know crypto's [mood]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        # The source is frame-sized already, so `crop_at` only bypasses the
        # scorer; `shift` slides the dial right and fades the uncovered edge
        # to black, which is where the headline goes.
        thumb_crop_at=(0.5, 0.5), thumb_side="left", thumb_shift=0.24,
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
