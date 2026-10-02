"""What was the first Bitcoin transaction - long-form 16:9 for YouTube.

Source: crypto-wiki/content/crypto-ogs/hal-finney.mdx. There is no `posts/`
article behind this one, so `SOURCE_POST` is None and the OG bio carries the
facts, with one verified exception noted under "The one outside source" below.

**The angle, and the two videos this deliberately is not.** The obvious Hal
Finney video is "was he Satoshi?" - and that video already exists twice on
this channel. `satoshi-nakamoto` names him three times and runs him as a
*struck item* in its candidates `checklist`; `satoshi-proof` covers what would
count as proof. Building the suspect angle again would be the same evidence
list a third time.

What is left is better, and it is a mechanism rather than a mystery: **Finney
is the one person who sits on both sides of Bitcoin's central claim.** In 2004
he built reusable proof of work - digital cash that worked, and that still kept
its register on one trusted machine. Five years later he received the first
Bitcoin payment ever sent, which is the first time that register had no owner.
The video walks what those ten coins actually proved, and the man who received
them is the reason the answer is legible at all.

**The planted fact pays off late** (`projects/crypto.md`, the profile genre):
2004 is stated plainly in the hook and again on the `timeline` long before the
chapter that explains why it matters, so the viewer half-sees the ending
coming. That is the "cheap surprise" fix, and this script is where it was
first used deliberately rather than by accident.

**No financial advice.** It names no price, no level, predicts nothing, rates
no platform and recommends nothing. The topic is structurally safe - the whole
argument is that the first payment was worth nothing - and the one figure in
the cut (ten coins, block 170) is a fact about a ledger, not about a price. No
live price, chart, ticker or broker name appears in any shot. Nothing here can
date.

**He appears once, and only because of what the picture actually is.** There
is **no photograph of adult Hal Finney** on Wikimedia Commons - the single file
that exists is a 1972 newspaper staff photo of him as a teenager holding up a
sheet of hand-lettered mathematics (public domain, Daily News-Post, 4677x4705).
It is square and measures L146, so it may not fill a 16:9 frame under
`footage.md`'s own rule and would glare if it did. It goes in the `quote`
beat's **picture column**, where it is a downscale and reads as a deliberate
inset, under the one line that dates it. `satoshi-nakamoto` established the
pattern for a subject with no usable picture - nobody stands in for him - and
this cut follows it everywhere else.

**The one outside source.** The bio says reusable proof of work let tokens be
"securely transferred or reused between users" and calls it a precursor to
Bitcoin; it does not say what RPOW depended on, and the trusted-server fact is
the hinge of the whole script. It is taken from Finney's own RPOW page
(nakamotoinstitute.org/finney/rpow/): ownership of tokens is "registered on a
trusted server", running on an IBM 4758 secure coprocessor that can attest
which software it is running. Cited in `Meta.credits`. Nothing else in the
script comes from outside the bio.

## The beats

Last three crypto long-forms: musk (chart / compare / diagram / stat /
timeline), whale (checklist / compare / grid / split), scams (checklist /
compare / diagram / grid / quote). `compare` is in **all three** and is
skipped; `checklist`, `grid` and `diagram` are in two each and are also
skipped.

That ban is unusually expensive here, because all four are the beats that draw
a contrast, and the contrast *is* the argument. The substitute is a deliberate
rhyme rather than a fifth shape:

* `timeline` - 1979 / 2004 / 2009 / 2014. **Four distinct years**, so no two
  nodes parse to the same point, and the real spacing is the content: the
  five-year gap between building his own digital cash and receiving the first
  Bitcoin is the gap the video is about.
* `steps` **(4 nodes)** - what had to happen every time an RPOW token changed
  hands, ending on the register and the one machine keeping it.
* `stat` - `BLOCK 170`, with `count=False`: a block height racing up from zero
  shows 43 and 112 on the way, and a paused frame would read as a fact.
* `steps` **(3 nodes)** - the same track, for a Bitcoin payment. **This is the
  rhyme and it is the point:** the viewer has just read the four-step version,
  so the three-step one lands as the four-step version with the middle removed.
  A repeated silhouette is normally the fault `beats.md` warns about; here the
  repetition carries the comparison the banned `compare` would have drawn, and
  the node counts differ, which is the thing the eye actually reads.
* `quote` - his own line, with the 1972 photograph in the picture column.

Five drawn shots rather than the eight `projects/crypto.md` wants for an
abstract topic, and that is a real shortfall with a real cause: there is no
honest payload for a sixth. `bars`, `split`, `gauge`, `dial`, `map` and
`chart` were each considered and each would have had to invent a proportion, a
threshold or a trajectory the article does not contain. Manufacturing one is
the failure `beats.md` names ("show what is being said, not a summary of it"),
so the slack is carried by holds instead.

**Footage.** Six fetch rounds, ~60 queries, every candidate screened across
its length and then looked at on a labelled contact sheet - which is the step
that did the work. Rejected after *looking*, all of them inside the luma box:
a "single server rack" that is a candle, a "lightbulb" that is a blue CG ring,
a "satellite dish" and an "observatory" that are both the moon, "server lights
blinking" that is a rainbow RGB gaming keyboard, and the two most on-topic
clips in the whole fetch - a wall of CRTs (teal) and hands typing code (green,
with a legible Dell wordmark). The site's own library is exhausted: every
post image dark enough to use is already in another video, and the only one
left is the banned exchange-UI screenshot.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/first-bitcoin-transaction.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

# No `posts/` article - the source is the crypto-og bio.
SOURCE_POST = None
SOURCE_OG = "hal-finney"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Luma/saturation across the whole clip, then read off a labelled contact
# sheet. Durations matter: the long ones carry the paragraphs, the short ones
# the single-line sentences, and anything under ~14s is a one-use clip.
LEDGER = V / "old-ledger-book-handwriting-candle-dark/11530055.mp4"      # 21s, L33-36 S26, hands over a handwritten ledger by candlelight
ROOM = V / "old-ledger-book-handwriting-candle-dark/10425839.mp4"        # 11s, L21-23 S21, a closed book and a candle in a dark room
CHAIN = V / "chain-links-metal-heavy-dark/12797959.mp4"                  # 40s, L16-18 S5, heavy rusted chain links
BRIDGE = V / "bridge-lights-at-night-long-exposure/30153497.mp4"         # 15s, L2 S0, a line of lamps receding into black over water
WEB = V / "spider-web-with-dew-dark/27175163.mp4"                        # 16s, L29-44 S0, a web and its spider, monochrome
CANDLE = V / "candle-flame-flickering-darkness/12550702.mp4"             # 19s, L2 S2, one candle on black
EMBERS = V / "embers-glowing-in-a-fire-close-up-dark/13220869.mp4"       # 22s, L3-4 S5, embers breathing in a dark grate
MATCH = V / "match-striking-flame-dark/4061849.mp4"                      # 26s, L3-28 S28, a match struck and burning down
SPARKS = V / "sparks-rising-from-fire-at-night/12298312.mp4"             # 15s, L7-11 S8, orange sparks rising on black
COIN = V / "coin-spinning-on-dark-table/35996676.mp4"                    # 9s,  L7 S0, a coin spinning and settling
GRID = V / "city-lights-from-above-at-night/9709111.mp4"                 # 12s, L38-39 S22, a lit street grid from above
CITY = V / "city-lights-from-above-at-night/8978968.mp4"                 # 36s, L7 S4, a dark city from high above
SNOW = V / "snow-falling-at-night-street-lamp/6527134.mp4"               # 33s, L24 S21, snow falling past a street lamp
FOG = V / "fog-rolling-through-dark-forest-night/4999957.mp4"            # 23s, L16-27 S4, fog over a dark treeline
MOON = V / "satellite-dish-at-night-sky/36492194.mp4"                    # 30s, L8 S3, the moon (the folder name lies)
STARS = V / "stars-night-sky-timelapse-dark/38788509.mp4"                # 17s, L14-19 S16, star trails circling
BEACON = V / "lighthouse-beacon-rotating-at-night/4814151.mp4"           # 20s, L27 S36, a lighthouse and its beam
CANOPY = V / "dark-forest-canopy-looking-up-night/27437296.mp4"          # 16s, L14-15 S20, a star field through branches
RAIN = V / "rain-on-dark-asphalt-street-night/3638386.mp4"               # 8s,  L42-44 S28, a wet street under amber lamps

# The only free photograph of him that exists, and it is of a teenager.
# Public domain, Daily News-Post staff photo, via Wikimedia Commons.
# Square (r0.99) and L146, so it may not fill a 16:9 frame - picture column only.
FINNEY = ROOT / "assets/crypto/finney/hal-finney-1972.jpg"               # 4677x4705 r0.99, L146 S0, aged 16, holding up hand-lettered mathematics

THUMB = FINNEY
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/crypto-ogs/hal-finney"


SECTIONS = [
    # --- hook. No card. The interrupt is a fact and the subject is named in
    # sentence one, per `narration.md`. The measured curve on this format
    # drops ~20 points at the end of sentence one, so the date and the number
    # go there rather than any scene-setting.
    Section(
        title="Ten coins, worth nothing",
        card=False,
        sentences=[
            ("On the twelfth of January, two thousand nine, "
             "ten bitcoins moved from one computer to another.",),
            ("It was the first time Bitcoin had ever been used to pay anybody.",
             "Three days after the software existed at all."),
            ("The man who received them was called Hal Finney.",),
            # The planted fact. Stated here, drawn on the timeline in chapter
            # three, and not explained until chapter four.
            ("And five years earlier, he had built digital money of his own.",
             "It worked. And it still needed somebody in the middle."),
            # The retention call, made out loud and answered by the close.
            ("Stay to the end,",
             "and you will know what those ten coins actually proved - "
             "and why the man who received them already knew "
             "exactly what he was looking at."),
        ],
        shots=[
            # Open on motion, and on the literal noun: a coin. 9s source, so
            # this is its only use in either file.
            Shot(clip=COIN, clip_at=0.5),
            Shot(clip=CHAIN, clip_at=2.0),
            # "The man who received them" - hands over a ledger. There is no
            # photograph of him, so a pair of hands carries the person.
            Shot(clip=LEDGER, clip_at=2.0),
            Shot(clip=CANDLE, clip_at=1.0),
            Shot(clip=CITY, clip_at=2.0),
        ],
        gaps=[0.95, 0.80, 0.75, 0.90, 0.85],
    ),

    # --- what Bitcoin was on day one ---------------------------------------
    Section(
        title="What was Bitcoin on day one?",
        spoken_title="So what was Bitcoin on day one?",
        sentences=[
            ("The software was released on the ninth of January, "
             "two thousand nine.",),
            ("Finney downloaded it the same day.",
             "He was the first person other than its creator known to run it."),
            ("His computer started mining, and it found block seventy-eight.",),
            # The reversal this chapter exists for. 0.95 in front of it,
            # because the line contradicts the one before it.
            ("But mining is not spending.",),
            ("Mining creates new coins and writes them into the ledger.",
             "It never once proves that a coin can be handed to somebody else."),
            ("So for three days, Bitcoin was a system "
             "that could make money and had never moved any.",),
        ],
        shots=[
            Shot(clip=SNOW, clip_at=3.0),
            None,
            Shot(clip=SPARKS, clip_at=1.0),
            Shot(clip=MATCH, clip_at=2.0),
            Shot(clip=LEDGER, clip_at=12.0),
            Shot(clip=FOG, clip_at=2.0),
        ],
        gaps=[0.60, 0.80, 0.85, 0.95, 0.75, 0.90],
    ),

    # --- who he was ---------------------------------------------------------
    Section(
        title="So who was Hal Finney?",
        sentences=[
            ("He was a cryptographer, and he had been one for a long time.",),
            # `Caltech` phonemizes as `kˈɔltɛk` - "cawl-tek". `Caltek` returns
            # `kˈæltɛk`, which is the name. Respelling goes in the spoken half
            # only, so the caption and the SRT still read correctly.
            (("He studied engineering at Caltech.",
              "He studied engineering at Caltek."),),
            # `PGP` checks out as `pˌiːdʒˌiːpˈiː` - the letters, correctly.
            ("He worked on P G P, the encryption that first made "
             "private email possible for ordinary people.",),
            ("And he spent the nineteen nineties on the cypherpunk mailing "
             "lists, arguing that cryptography was how ordinary people "
             "would keep their privacy.",),
            # The hinge into the beat gets its own sentence: a leading hinge
            # inside the beat's span eats reveal zero.
            ("His whole working life runs along one line.",),
            # The timeline's own sentence - one chunk per node, four distinct
            # years. `ALS` phonemizes as `ˈælz`; `A.L.S.` returns `ˌeɪˌɛlˈɛs`,
            # which is the letters.
            ("Nineteen seventy-nine. He leaves Caltech with an "
             "engineering degree.",
             "Two thousand four. He builds digital cash of his own.",
             "Two thousand nine. He receives the first Bitcoin payment "
             "ever sent.",
             ("Two thousand fourteen. He dies of ALS.",
              "Two thousand fourteen. He dies of A.L.S.")),
        ],
        shots=[
            Shot(clip=STARS, clip_at=1.0),
            Shot(clip=MOON, clip_at=2.0),
            None,
            Shot(clip=BEACON, clip_at=1.0),
            Shot(clip=CANOPY, clip_at=1.0),
            Shot(graphic="timeline", backdrop=BEATGROUND,
                 payload=([("1979", "Leaves Caltech"),
                           ("2004", "Builds his own digital cash"),
                           ("2009", "Receives the first payment"),
                           ("2014", "Dies of ALS")],
                          "ONE WORKING LIFE")),
        ],
        gaps=[0.70, 0.80, 0.85, 0.90, 0.95, 2.00],
    ),

    # --- the deep dive: why digital money kept failing ----------------------
    Section(
        title="Why did digital money keep failing?",
        spoken_title="So why did digital money keep failing?",
        sentences=[
            ("Every attempt before Bitcoin ran into the same wall.",),
            ("A digital coin is a file.",
             "And a file can be copied."),
            ("Spend the same coin twice, and nobody can tell "
             "which payment was the real one.",),
            ("In two thousand four, Finney built the closest "
             "anyone had come to solving it.",),
            ("He called it reusable proof of work.",
             "You spent real computing time to make a token, "
             "and then you could pass that token on."),
            ("But look at what had to happen every time it changed hands.",),
            # The steps track's own sentence - one chunk per node. The fourth
            # is the one the whole video turns on.
            ("You spend real computing power to make a token.",
             "You send it on to somebody else.",
             "Their copy gets checked against a register.",
             "And one machine, somewhere, is keeping that register."),
            ("He protected that machine about as well as anyone could.",
             "It could even prove which program it was running."),
            ("But it was still one machine.",
             "Trust it, or the money does not work."),
        ],
        shots=[
            Shot(clip=FOG, clip_at=12.0),
            None,
            Shot(clip=EMBERS, clip_at=10.0),
            Shot(clip=ROOM, clip_at=1.0),
            Shot(clip=SNOW, clip_at=16.0),
            Shot(clip=WEB, clip_at=1.0),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 # `steps` takes a flat list of strings. A two-tuple is read
                 # as `(text, emoji)` and raises in `emoji_image`; `grid` is
                 # the beat with a second line, so each node says it all.
                 payload=(["Make a token",
                           "Send it on",
                           "Check it against a register",
                           "One machine keeps that register"],
                          "EVERY TIME IT CHANGED HANDS")),
            Shot(clip=STARS, clip_at=8.0),
            # One flame in the dark, under "it was still one machine".
            Shot(clip=CANDLE, clip_at=9.0),
        ],
        gaps=[0.85, 0.70, 0.90, 0.85, 0.80, 0.95, 2.10, 0.85, 0.95],
    ),

    # --- the twist: what ten coins proved -----------------------------------
    Section(
        title="So what did ten coins prove?",
        spoken_title="So what did those ten coins actually prove?",
        sentences=[
            ("Which brings us back to the twelfth of January.",),
            ("Satoshi Nakamoto sent ten bitcoins, and Finney received them.",),
            # `count=False`: a block height counting up from zero shows 43 and
            # 112 on the way, and a paused frame would read as a fact.
            ("It is written down in block one hundred and seventy.",),
            ("Now run the same four steps again.",),
            # The rhyme. The viewer has just read the four-step version, so a
            # three-step track lands as that version with the middle removed.
            ("One person signs a payment.",
             "Every computer on the network checks it.",
             "And it is written into a ledger nobody owns."),
            ("There is no fourth step.",
             "Nothing in that chain is a machine you have to trust."),
            ("That is the whole difference between what he built "
             "and what he was sent.",),
        ],
        shots=[
            Shot(clip=MOON, clip_at=15.0),
            Shot(clip=BRIDGE, clip_at=1.0),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("BLOCK 170", "THE FIRST PAYMENT",
                          "ten coins, from one person to another", False)),
            Shot(clip=GRID, clip_at=1.0),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 # **Three nodes against the four above, deliberately.**
                 # `beats.md` wants four or five on a track; this one is the
                 # rhyme and the missing node is the whole argument, so the
                 # short count is the content rather than a thin payload.
                 payload=(["One person signs it",
                           "Every computer checks it",
                           "It goes in a ledger nobody owns"],
                          "THE SAME THING, WITHOUT THE MIDDLE")),
            Shot(clip=CHAIN, clip_at=20.0),
            None,
        ],
        gaps=[0.75, 0.85, 1.20, 0.95, 1.90, 0.95, 0.90],
    ),

    # --- close. The card resolves rather than asks, so it is a statement. ---
    Section(
        title="Worth nothing, and it still counted",
        sentences=[
            ("The ten coins were worth nothing.",
             "There was no price, no exchange, and almost nobody watching."),
            ("What moved that day was not money. It was proof.",),
            ("And the man holding it had spent five years "
             "building the version that still needed a middle.",),
            # The quote beat. His own words, from the bio.
            ("He had written down what he thought the point of all of it was.",),
            ("The computer can be used as a tool to liberate and protect "
             "people, rather than to control them.",),
            ("Nothing in this video is financial advice.",),
            ("So, what do you think - if you had been sent those ten coins "
             "that morning, would you have known what you were holding?",),
        ],
        shots=[
            Shot(clip=WEB, clip_at=7.0),
            Shot(clip=SPARKS, clip_at=6.0),
            Shot(clip=MATCH, clip_at=16.0),
            None,
            # The one picture of him, in the picture column where a square
            # L146 source is a downscale and reads as an inset rather than a
            # glare. The line above dates it; the beat attributes the words.
            Shot(graphic="quote", backdrop=BEATGROUND, picture=FINNEY,
                 payload=("The computer can be used as a tool to liberate "
                          "and protect people, rather than to control them.",
                          "HAL FINNEY")),
            # The compliance line runs over a quiet frame, never a person.
            Shot(clip=RAIN, clip_at=0.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=BEACON, clip_at=10.0),
        ],
        gaps=[0.85, 0.95, 0.90, 0.90, 1.60, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Was the First Bitcoin Transaction?",
    hook="On 12 January 2009, ten bitcoins moved from one computer to "
         "another - the first time Bitcoin was ever used to pay anybody. "
         "The man who received them, Hal Finney, had built digital cash of "
         "his own five years earlier, and it had still needed one trusted "
         "machine in the middle. Here is what those ten coins actually "
         "proved.",
    url=URL,
    summary="The first Bitcoin transaction, described as a mechanism rather "
            "than a milestone. Bitcoin's software was released on 9 January "
            "2009; Hal Finney downloaded it the same day, was the first "
            "person other than its creator known to run it, and mined block "
            "78 - but mining only creates coins and never proves one can be "
            "handed to somebody else. On 12 January 2009, Satoshi Nakamoto "
            "sent Finney ten bitcoins, recorded in block 170. Why that "
            "mattered is clearest through Finney himself: in 2004 he built "
            "reusable proof of work, digital cash whose token ownership was "
            "registered on a trusted server, so every transfer still ran "
            "through one machine you had to trust. The first Bitcoin payment "
            "is the same sequence with that machine removed. Nothing here is "
            "financial advice: no price, no prediction, no recommendation.",
    tags=["first bitcoin transaction", "hal finney", "block 170",
          "who received the first bitcoin", "bitcoin history",
          "reusable proof of work", "rpow", "early bitcoin 2009",
          "how bitcoin transactions work", "bitcoin for beginners"],
    cta=f"The full Hal Finney page: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Photograph of Hal Finney (1972): Daily News-Post staff photo, "
             "public domain, via Wikimedia Commons.",
             "Reusable proof of work's trusted-server design: Hal Finney's "
             "own RPOW pages, via the Nakamoto Institute "
             "(nakamotoinstitute.org/finney/rpow/).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/first-bitcoin-transaction-long.mp4"
    work = Path.home() / "Desktop/.first-bitcoin-transaction-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # **Statement mode, no brackets.** The surprise here is the
        # proposition - the first payment was worth nothing and still settled
        # the only question that mattered - not a token inside a sentence,
        # which is exactly when `shorts.md` says to drop the redaction. A
        # bracket would also fail the cover-the-bar test: "ten bitcoins moved
        # and they were worth [nothing]" is handed to you by the grammar.
        # Rotation: the last three long-forms ran Search, Search and a
        # redacted hook, so this is neither.
        hook="Ten coins moved, and they were worth nothing at all",
        thumb_headline="Who got the first [bitcoin?]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        # The source is square (r0.99) and cannot be cover-cropped to 16:9
        # without losing the sheet of mathematics, which is the half of the
        # picture that makes it interesting. `crop_zoom` below 1.0 fits it
        # whole onto black and the type sits on real black rather than on a
        # scrim over detail. `side` is passed because `crop_at` bypasses the
        # scorer and there is no layout pass left to infer a side from.
        thumb_side="right", thumb_crop_at=(0.30, 0.42), thumb_crop_zoom=0.66,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
