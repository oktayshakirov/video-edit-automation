"""Why do Elon Musk's posts move crypto prices - long-form 16:9 for YouTube.

Source: crypto-wiki/content/crypto-ogs/elon-musk.mdx. There is no `posts/`
article behind this one, so `SOURCE_POST` is None and the OG bio carries every
fact in the script.

**The angle, and the video this deliberately is not.** The obvious Musk video
is a profile - what he said, when, and what the price did afterwards - and on
this channel that is a direction claim wearing a story. So the pair takes the
mechanism the bio's "Musk Effect" section rests on and never states: **a post
is not a purchase.** Nothing about a coin changes when one lands. What changes
is how many people reach the same short queue of offers in the same few
minutes, and the size of the reaction is therefore a measurement of the
*market's depth*, not of the poster's persuasiveness. That is the one framing
under which this topic is both safe and more interesting than the profile.

**It pays off its own retention call.** The opener promises the viewer will
know why the same post shakes one coin and barely moves another; the `compare`
in chapter five is that answer, and the close echoes it.

**He appears in the cut and on the thumbnail, at the user's direction.** The
first pass used no photograph of him at all, reasoning that the subject is a
queue of offers and that a face is a promise about the subject; the user's
call is that the Musk effect is the hook and he should be seen. What does not
bend is licensing: a portrait of a named individual comes from **Wikimedia
Commons**, screened, stored in `assets/crypto/musk/` and credited there and in
`Meta.credits` - **two of the four are CC BY 2.0, which makes this video a
derivative work, so the attribution line has to ship in the description.**

**There is no usable video of him.** Pexels does not license footage of a real
public figure, and Commons' only non-political clips are the two RAeS talk
files at **500x374** - a 3.8x upscale to fill a 1920 frame. The motion is
therefore a Ken Burns move on the stills, which is what `PhotoShot` is for.

**Three photographs, placed rather than sprinkled.** The landscape stage shot
(L18, on-palette) opens the video under the sentence that names him and
returns once near the end as a tighter push - two crops of one photograph
three minutes apart read as a bookend, the one sanctioned exception to "every
still is used once". The microphone shot lands on "the Musk effect". The
arms-crossed portrait is r0.92, too tall to fill a 16:9 frame without becoming
a band across the face, so it goes in the `stat`'s picture column where it is
a downscale and reads as a deliberate inset. The other twenty-odd slots are
still hands, screens and crowds: the argument is the queue, not the man, and
the pictures should not start arguing the opposite.

**No financial advice.** It names no price level, predicts nothing, rates no
platform, and recommends buying or selling nothing. The one structural risk in
a topic like this is a script that reads as "watch his posts" - the `timeline`
chapter exists specifically to foreclose it, because the same account is on
both sides of it. **Nothing in the cut shows a live price, chart, ticker or
broker name**, and the `chart` beat plots *attention*, not price, with no
y-axis numbers - which is the beat's own documented design and keeps the
`footage.md` rule about price charts untouched.

**Every figure is dated in the mouth**, so the video cannot quietly go stale:
the one and a half billion dollars is February 2021 and the three-quarters sale
is 2022, both said with their years attached. No current holding is quoted -
those move every quarter.

## The beats

Last three crypto long-forms: whale (grid / checklist / split / compare),
scams (compare / grid / quote / diagram / checklist), satoshi (quote / stat /
steps / split / checklist). `checklist` is in all three and is skipped here;
`grid`, `split` and `quote` are in two each and are also skipped.

* `diagram(loop=True)` - the amplification cycle, and the only beat in the
  library that can draw a loop. The Short takes the *straight* chain, so the
  pair never draws the same object.
* `chart` - attention after one post: the climb, and then the drain. Its
  marker is the moment the post lands. Brand new to this channel.
* `stat` - the one hard figure, with `count=False`, because `$1.5B` counting
  up shows `$1B` on the way and a paused frame would read as a claim.
* `timeline` - brand new to this channel, and the beat this chapter needed.
  Its nodes are placed by their real years, so the five-year gap between 2014
  and 2019 looks like a gap and 2021-2022 looks like the cluster it was.
  **Four distinct years, deliberately** - three events inside 2021 would parse
  to the same year and stack three labels on one point.
* `compare(name_columns=True)` - a deep market against a thin one, three items
  a side, which is the answer to the opener's promise.

Three of the five are full-width, so the video does not set type in a left
column with a ragged right edge five times running.

**Footage.** Fetched and screened for this pair across four rounds; the site's
own image library has nothing usable here (`dogecoin.jpg` is L119 and
`tesla.jpg` is already in `saylor-treasury`), which is the exhaustion
`footage.md` records. Eight candidates that passed the luma box were cut on a
labelled contact sheet: a legible green messaging UI, an Instagram feed with
the brand on it, a gavel that reads as a courtroom, red wine, a DAW timeline,
a face in a cinema seat, and two near-empty frames. Two clips that screened
clean were also dropped for being the same shoot as assets already shipped -
`empty-dark-room-single-light/19217895` sits next to the whale cut's
warehouse, and `thumb-scrolling-social-media-feed-night/38410500` is that
cut's feed clip under a new folder name.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/musk-effect.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

# No `posts/` article - the source is the crypto-og bio.
SOURCE_POST = None
SOURCE_OG = "elon-musk"

V = STOCK / "videos"
P = STOCK / "photos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Luma/saturation range across the whole clip, then checked on a labelled
# contact sheet. Durations matter: the long clips carry the paragraphs and the
# short ones the one-line sentences.
PING = V / "hand-holding-phone-notification-dark/34786856.mp4"           # 7s,  L19-21 S21-23, a phone on a table, a notification arrives
PHONE = V / "hand-holding-phone-notification-dark/6414244.mp4"           # 15s, L5-23 S7-11, a dark phone face up (faces appear past ~10s)
ARENA = V / "audience-silhouettes-auditorium-dark/36499729.mp4"          # 37s, L30-33 S22-23, an arena of phone lights in the dark
LAMP = V / "moths-flying-around-light-at-night/7779673.mp4"              # 30s, L36-38 S23-25, insects swarming one warm street lamp
GATES = V / "turnstile-subway-gate-night/35722252.mp4"                   # 18s, L24-28 S23-29, a gateline of turnstiles, amber
ESCALATOR = V / "escalator-crowd-night-city-dark/29588469.mp4"           # 11s, L31-36 S37-43, gold escalators, people descending
SEATS = V / "empty-theatre-seats-dark/7986776.mp4"                       # 17s, L9-10 S3-3, rows of empty seats, almost black
STADIUM = V / "empty-stadium-seats-night-dark/19205377.mp4"              # 10s, L18-19 S3-4, empty stands under floodlights
SHOAL = V / "school-of-fish-swimming-dark-underwater/35756706.mp4"       # 11s, L24-25 S15-19, a dense school turning together
DOMINOS = V / "domino-chain-falling-dark-background/9760429.mp4"         # 21s, L32-40 S8-13, hands setting dominoes on a dark table
CASCADE = V / "domino-chain-falling-dark-background/38003914.mp4"        # 10s, L11-17 S16-23, gold dominoes toppling on black
TRAFFIC = V / "night-city-traffic-long-exposure-dark/9299639.mp4"        # 24s, L7-13 S11-14, light trails on a night road
TUNNEL = V / "dark-tunnel-lights-moving-night/33938673.mp4"              # 15s, L4-16 S1-5, travelling through a lit tunnel
WAVES = V / "dark-ocean-waves-night/11287848.mp4"                        # 30s, L19-22 S22-23, open dark water
SMOKE = V / "smoke-swirling-dark-background/34818523.mp4"                # 30s, L2-39 S0-0, the one abstract - smoke blooming and thinning
SAND = V / "ripples-spreading-on-dark-water/36117653.mp4"                # 10s, L27-28 S3-4, a rippled dark surface
STREET = V / "empty-night-street-lamp-quiet-dark/14610896.mp4"           # 23s, L16-17 S14, an empty street under amber lamps
PLATFORM = V / "empty-subway-platform-night-dark/20630219.mp4"           # 40s, L36-37 S6, an empty platform (a train arrives past ~30s)
DUST = V / "dust-particles-floating-in-light-beam-dark/28492353.mp4"     # 33s, L12-18 S4, dust drifting in a warm beam
LAKE = V / "calm-lake-at-night-dark-reflection/10084889.mp4"             # 15s, L8-10 S11, a dark waterfront, city lights reflected

# Portraits of a named individual come from Wikimedia Commons, not stock -
# licensed, attributable, and large enough never to upscale. Screened and
# credited in `assets/crypto/musk/CREDITS.md`, which also records the four
# rejects and why there is no usable *video* of him at any resolution.
MUSK = ROOT / "assets/crypto/musk"
COLORADO = MUSK / "elon-musk-colorado-2022.jpg"                          # 4534x3018 r1.50, L18 S7, seated on a dark stage - public domain
MIC = MUSK / "elon-musk-33377877458.jpg"                                 # 4318x2879 r1.50, L45 S26, at a microphone - CC BY 2.0
ARMS = MUSK / "elon-musk-april-2022.jpg"                                 # 2428x2636 r0.92, arms crossed - public domain

THUMB = ARMS
CROWD = P / "concert-crowd-phone-lights-dark/10063270.jpg"               # Pexels 10063270, Faruk Tokluoglu, 6240x4160, L18 S15 (was the thumbnail)
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/crypto-ogs/elon-musk"


SECTIONS = [
    # --- hook. No card, and the reversal is sentence one. -------------------
    # The pattern interrupt is a fact rather than a scene: the measured curve
    # on this format drops ~20 points at the end of sentence one, so the
    # surprising thing goes there and the context follows it.
    Section(
        title="A post buys nothing",
        card=False,
        sentences=[
            # `Elon` phonemizes to `ᵻlˈɑːn` - "uh-LON", stress on the wrong
            # syllable. `Eelahn` returns `ˈiːlɑːn`, which is the name. The
            # respelling goes in the spoken half only, so the caption and the
            # SRT still read correctly.
            (("A post from Elon Musk buys nothing, sells nothing, "
              "and changes nothing about a coin.",
              "A post from Eelahn Musk buys nothing, sells nothing, "
              "and changes nothing about a coin."),),
            ("Prices have moved on one anyway.",
             "Sometimes inside a minute."),
            ("People gave that pattern a name. The Musk effect.",),
            ("But the interesting part was never the man.",
             "It is what those posts accidentally measured."),
            ("Stay to the end,",
             "and you will know why the same post can shake one coin "
             "and barely move another."),
        ],
        shots=[
            # He is named in sentence one, so he is on screen in sentence one.
            # A landscape source (r1.50) may fill the frame; the portrait one
            # may not, and goes in the `stat`'s picture column instead.
            Shot(image=COLORADO, zoom=1.10, pan=(0.02, 0.0)),
            Shot(clip=ARENA, clip_at=2.0),
            # "People gave that pattern a name. The Musk effect." - the
            # picture says the noun the sentence says.
            Shot(image=MIC, zoom=1.08, pan=(-0.02, 0.0)),
            Shot(clip=GATES, clip_at=1.0),
            Shot(clip=WAVES, clip_at=1.0),
        ],
        gaps=[0.95, 0.80, 0.75, 0.85, 0.85],
    ),

    # --- what a price is ----------------------------------------------------
    Section(
        title="What is a price, actually?",
        spoken_title="So what is a price, actually?",
        sentences=[
            ("A price is not a measure of what something is worth.",),
            ("It is the last offer somebody actually filled.",),
            ("Behind every coin sits a queue of offers to sell,",
             "stacked at rising prices."),
            ("Take the cheapest one, and the next offer up becomes the new price.",),
            # The hinge into the beat gets its own sentence: a leading hinge
            # inside the beat's span eats reveal zero.
            ("So here is what a post actually does.",),
            # The diagram's own sentence - one chunk per node. The fourth
            # closes the cycle in words, which is what the feedback arrow
            # draws across.
            ("A post lands in front of millions of people at once.",
             "A fraction of them decide to buy in the same few minutes.",
             "They take the cheapest offers in the queue, one after another.",
             "The number everybody sees moves, which brings more people to look."),
            ("Nobody in that chain had to believe anything about the coin.",
             "They only had to arrive at the same time."),
        ],
        shots=[
            Shot(clip=SEATS, clip_at=1.0),
            None,
            Shot(clip=ESCALATOR, clip_at=1.0),
            Shot(clip=DOMINOS, clip_at=1.0),
            Shot(clip=PHONE, clip_at=0.5),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("A post lands", "millions read it at once"),
                           ("They arrive together", "inside the same few minutes"),
                           ("The queue empties", "the cheapest offers go first"),
                           ("The number moves", "which brings more people to look")],
                          "THE LOOP BEHIND A MOVE", True)),
            Shot(clip=TRAFFIC, clip_at=1.0),
        ],
        gaps=[0.55, 0.85, 0.70, 0.80, 0.95, 1.60, 0.95],
    ),

    # --- why it fades -------------------------------------------------------
    Section(
        title="Why does the move fade?",
        spoken_title="So why does a move like that fade?",
        sentences=[
            ("Attention does not last.",),
            ("Within a day the post has been read,",
             "everyone who was going to act has acted,",
             "and the queue of offers refills."),
            ("Draw the attention itself, and the shape is always the same.",),
            # The chart's own sentence: the line first, the marked moment
            # second, which is the order the beat reveals in.
            ("It climbs almost vertically the moment the post lands,",
             "and then it drains away for days, "
             "while nothing about the coin has changed at all."),
            ("The record of these episodes is blunt about it.",
             "Sharp rallies, followed by sharp corrections."),
            ("And that is the giveaway.",),
            ("A change in what something is worth would stay.",
             "A change in who is watching has to fade, because attention always does."),
        ],
        shots=[
            Shot(clip=SMOKE, clip_at=8.0),
            None,
            Shot(clip=TUNNEL, clip_at=1.0),
            Shot(graphic="chart", backdrop=BEATGROUND,
                 payload=([0.05, 0.05, 0.06, 0.05, 0.07, 0.62, 1.00, 0.84,
                           0.63, 0.47, 0.36, 0.28, 0.23, 0.19, 0.16, 0.14,
                           0.12, 0.10, 0.09, 0.08],
                          "ATTENTION AFTER ONE POST", 6, "the post lands")),
            Shot(clip=LAMP, clip_at=3.0),
            Shot(clip=STADIUM, clip_at=1.0),
            Shot(clip=WAVES, clip_at=14.0),
        ],
        gaps=[0.85, 0.70, 0.90, 1.90, 0.85, 0.90, 0.95],
    ),

    # --- both directions ----------------------------------------------------
    # This chapter exists to foreclose the "watch his posts" reading. The same
    # account is on both sides of the timeline, which is the fact that makes
    # the mechanism framing honest rather than a disclaimer.
    Section(
        title="Has it ever gone the other way?",
        spoken_title="But has it ever gone the other way?",
        sentences=[
            ("This is the part that usually gets left out.",),
            ("In February twenty twenty-one, Tesla put one and a half billion "
             "dollars of its own cash into Bitcoin.",),
            ("What happened around it ran in both directions.",),
            # The timeline's own sentence - one chunk per node, and four
            # distinct years so no two nodes land on the same point.
            ("Twenty fourteen. He denies being Bitcoin's creator.",
             "Twenty nineteen. A joke poll makes him chief executive of Dogecoin.",
             "Twenty twenty-one. Tesla buys Bitcoin, takes it for cars, "
             "then stops, over the energy that mining uses.",
             "Twenty twenty-two. Tesla sells about three quarters of what it bought."),
            ("The same account was behind the moves up and the moves down.",),
            ("So a post was never a direction.",
             "It was only a crowd arriving."),
        ],
        shots=[
            Shot(clip=SEATS, clip_at=9.0),
            # The portrait is r0.92 - too tall to fill a 16:9 frame without
            # becoming a band across the face - so it goes in the split
            # layout's picture column, where it is a downscale and reads as a
            # deliberate inset. That is what the column is for.
            Shot(graphic="stat", backdrop=BEATGROUND, picture=ARMS,
                 payload=("$1.5B", "TESLA, FEBRUARY 2021",
                          "its own cash, disclosed in a filing", False)),
            Shot(clip=PLATFORM, clip_at=30.0),
            Shot(graphic="timeline", backdrop=BEATGROUND,
                 payload=([("2014", "Denies being Satoshi"),
                           ("2019", "Voted CEO of Dogecoin"),
                           ("2021", "Tesla buys, then stops"),
                           ("2022", "Three quarters sold")],
                          "THE SAME ACCOUNT, BOTH WAYS")),
            Shot(clip=TUNNEL, clip_at=7.0),
            Shot(clip=CASCADE, clip_at=0.5),
        ],
        gaps=[0.75, 0.90, 0.90, 2.00, 0.95, 0.90],
    ),

    # --- the twist: depth ---------------------------------------------------
    Section(
        title="Why barely move Bitcoin?",
        spoken_title="So why does the same post barely move Bitcoin?",
        sentences=[
            ("Because the effect was never really about the poster.",
             "It was about the queue."),
            ("A deep market has offers stacked at every level above the price.",),
            ("Money arrives, gets absorbed, and the number hardly moves.",),
            # The compare's own sentence - heading, three items, heading,
            # three items. Eight chunks for a 3+3 with named columns.
            ("Take a deep market.",
             "Offers stacked at every level.",
             "A wave of buying gets absorbed.",
             "The number barely moves.",
             "Now compare that with a thin one.",
             "Almost nothing sitting above the price.",
             "The same wave empties the queue.",
             "And the number jumps."),
            ("So the size of the reaction was never a measure "
             "of how convincing the post was.",),
            ("It was a measure of how little was standing behind the price.",),
        ],
        shots=[
            # The second and last use of this portrait, ~20 slots after the
            # first and at a tighter push: two crops of one photograph spaced
            # three minutes apart read as an open/close bookend, which is the
            # one sanctioned exception to "every still is used once".
            Shot(image=COLORADO, zoom=1.24, pan=(-0.03, 0.01)),
            Shot(clip=TRAFFIC, clip_at=13.0),
            None,
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("A DEEP MARKET",
                          ["Offers at every level",
                           "Buying gets absorbed",
                           "The number barely moves"],
                          "A THIN MARKET",
                          ["Almost nothing above",
                           "The queue empties",
                           "The number jumps"],
                          True)),
            Shot(clip=SAND, clip_at=0.5),
            Shot(clip=SMOKE, clip_at=20.0),
        ],
        gaps=[0.80, 0.70, 0.85, 1.40, 0.90, 0.95],
    ),

    # --- close --------------------------------------------------------------
    Section(
        title="So what was being measured?",
        spoken_title="So what was actually being measured?",
        sentences=[
            ("Strip the name off it,",
             "and the Musk effect is not a story about one man at all."),
            ("It is a measurement of how thin a market is.",),
            ("The posts were loud. The queue behind the price was short.",
             "Only one of those was ever about him."),
            ("Nothing in this video is financial advice.",),
            ("So, what do you think - if one post can move a price that far, "
             "what was that price actually telling you?",),
        ],
        shots=[
            # The close gets its own four clips rather than a third use of
            # anything: the pair shares one roster, so a clip the Short spends
            # is spent for the long form too, and `audit_assets.py` only
            # counts within a file.
            Shot(clip=STREET, clip_at=1.0),
            Shot(clip=PLATFORM, clip_at=2.0),
            Shot(clip=LAKE, clip_at=1.0),
            # The disclaimer runs over a quiet, contemplative frame - never a
            # person or a stage.
            Shot(clip=DUST, clip_at=4.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=SHOAL, clip_at=2.5),
        ],
        gaps=[0.70, 0.85, 0.95, 1.10, 2.30],
    ),
]

META = Meta(
    title="Why Do Elon Musk's Posts Move Crypto Prices?",
    hook="A post buys nothing and sells nothing, and crypto prices have moved "
         "on one anyway. Here is the actual mechanism - what a price is, why a "
         "queue of offers empties when everybody arrives at once, why the move "
         "always fades, and why the size of the reaction measures the market "
         "rather than the man.",
    url=URL,
    summary="How a social media post moves a cryptocurrency price, described "
            "as a mechanism rather than a story: why a price is only the last "
            "offer that was filled, how a post brings a large number of "
            "buyers to the same short queue of offers in the same few "
            "minutes, why the resulting move fades as attention does, and why "
            "the same post moves a thin market far more than a deep one - so "
            "the size of the reaction is a measure of how little is standing "
            "behind the price. The timeline runs in both directions: Tesla's "
            "1.5 billion dollar Bitcoin purchase in February 2021, the "
            "suspension of Bitcoin payments over mining energy later that "
            "year, and the sale of roughly three quarters of the holding in "
            "2022. Nothing here is financial advice: no price level, no "
            "prediction and no recommendation.",
    tags=["elon musk crypto", "musk effect", "why do crypto prices move",
          "dogecoin explained", "tesla bitcoin", "crypto market depth",
          "order book explained", "crypto volatility",
          "what moves crypto prices", "crypto for beginners"],
    cta=f"The full Elon Musk and crypto page: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Photographs of Elon Musk: Daniel Oberhaus (CC BY 2.0) and "
             "public-domain images, via Wikimedia Commons.",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/musk-effect-long.mp4"
    work = Path.home() / "Desktop/.musk-effect-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # **`Search`, not the redacted hook.** The last three long forms on
        # this channel all opened on `hook=`, and this video's title already
        # *is* the phrase somebody types - which is the one condition
        # `shorts.md` gives for this opener. It shows the question only: no
        # autocomplete, no answer.
        opener=Search("why do elon musk posts move crypto prices"),
        # No forced rows: left to wrap, the narrow column forces four big
        # short rows and lands `[queue]` on a line of its own, which keeps the
        # accent plate clear of the word in front of it.
        # **The portrait is fitted, not cropped.** A r0.92 source cover-cropped
        # to 16:9 is a band across the face, so `crop_zoom` below 1.0 scales it
        # whole onto black with the renderer's own 260px falloff and the type
        # sits on that real black rather than on a scrim over detail. Swept:
        # 0.55 left him small, 0.70 crowded the frame edge, 0.62 keeps him
        # entire. `side` is passed because `crop_at` bypasses the scorer and
        # there is no layout pass left to infer a side from.
        thumb_headline="This is the [Musk] effect",
        thumb_image=THUMB,
        thumb_accent="yellow",
        thumb_side="left", thumb_crop_at=(0.88, 0.18), thumb_crop_zoom=0.62,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
