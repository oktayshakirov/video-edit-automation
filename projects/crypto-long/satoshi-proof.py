"""Satoshi — the one test that settles it. Long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-it-actually-takes-to-prove-someone-is-
satoshi-nakamoto.mdx (1,838 words). The 34.75s short `crypto-satoshi-proof` came
from the same post and shares its angle, which is the right way round: the short
found the strongest framing the article has, so the long version keeps it and
goes deeper. Three minutes adds the verification procedure and the 2019 case
study — a claimant with a mathematically valid signature from the wrong address
— neither of which fits in thirty-five seconds.

**Structure, second pass.** The first cut was a sectioned presentation: seven
numbered chapter cards over a script written as headings and bullet points. It
read as a slide deck, which is what the user said and what the reference
material independently warns against. This one follows the arc that both the
reference prompt and the retention research point at:

    hook -> reframe -> deep dive -> counterintuitive twist -> mirror -> echo

and the rules that come with it:

* **Second person throughout.** "You have seen the headline." Never "we", never
  "I". The viewer is the subject of the video, not the audience for it.
* **Short. Short. One longer that builds. Short. Question?** The cadence is
  written into the sentence lengths deliberately; it is not an accident of
  where the captions fall.
* **A question every four to six sentences**, and every section turn is one.
* **The three-phase opening.** Pattern interrupt in the first five seconds, a
  specific promise by fifteen, a reason to commit by thirty. The steepest
  retention drop is between seconds ten and twenty, so nothing decorative goes
  in there.
* **The closing line echoes the opening, reframed.** The video opens on you
  seeing the headline and closes on you seeing it again, knowing what to ask.

**Scenes are held.** Shots are `None` where the picture should ride through the
next sentence rather than cut. One shot per sentence is a new scene every four
seconds, which is the thing that makes an edit feel like a metronome.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/satoshi-proof.py

**Phonemes.** `ecdsa` comes out of espeak as `ˈɛkdsə` and `secp256k1` is worse,
so neither is spoken — the script says "a cryptographic signature", which is
what the terms mean to this audience anyway. Years are safe.

**No financial advice, and none implied.** The piece is about what constitutes
proof. It never says what anyone should buy.
"""

from pathlib import Path

from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"

# Pexels, cached under assets/stock/. A supporting layer — the site's own
# pictures and the drawn beats still carry the argument. Every clip was measured
# with `stock.screen`; the trailing comment is its luma/saturation.
WAVES = STOCK / "videos/abstract-dark-waves-motion"
PARTICLES = STOCK / "videos/dark-abstract-digital-particles"
CIRCUIT = STOCK / "videos/circuit-board-macro-dark"
SERVER = STOCK / "videos/server-room-data-center"
STREAM = STOCK / "videos/digital-code-stream-dark"
KEYS = STOCK / "videos/typing-keyboard-night"

# The end-screen sting: like, dislike, subscribe, on **black** rather than
# green. Screen-blended it needs no chroma key at all, so there is no spill
# and no fringing — see longform/overlay.py. Committed, because it is a
# reusable brand asset like the drone project's location pin, not per-video
# stock.
#
# The like/dislike/subscribe strip (10378511) was tried first and rejected:
# its animation is a *moving* vertical swipe divider that crosses the whole
# width, so no crop removes it and screen-blending turns it into a bright
# bar sweeping the frame. Measure a sting's bright bounding box across the
# whole clip before committing to it, not on one frame.
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # female, af_heart. Candidate, not approved.
MUSIC = "pulse"                 # 112 BPM, plucked, no air layer. The user picked
                                # this over `bright` for a piece about proof.

URL = ("https://thecrypto.wiki/posts/"
       "what-it-actually-takes-to-prove-someone-is-satoshi-nakamoto")

A = 16 / 9                      # crop toward the frame, not the shorts' 1.15


SECTIONS = [
    # --- the hook, first thirty seconds ---------------------------------
    # No card. Pattern interrupt, then a specific promise, then a reason to
    # stay — in that order, because the drop is at ten to twenty seconds.
    Section(
        title="The claim",
        card=False,
        sentences=[
            ("You have seen the headline.",),
            ("Someone has finally proved",
             "they are Satoshi Nakamoto."),
            ("It has happened four times.",
             "Four times it fell apart",
             "in under a minute."),
            ("Because there is one test",
             "that settles it,",
             "and it has never once been passed."),
            ("Here is the test —",
             "and why it keeps winning."),
            ("Anyone can run it.",
             "You will be able to",
             "by the end of this video."),
        ],
        shots=[
            Shot(image=POSTS / "satoshi-nakamoto.jpg", zoom=1.09,
                 pan=(0.02, -0.01), aspect=A, bias=0.45),
            None,                                    # ride through the claim
            Shot(graphic="stat",
                 payload=("0", "TIMES PASSED", "Out of four claims."),
                 backdrop=POSTS / "bitcoin-neon.jpg"),
            None,
            # The title stamp. It lands at about eight seconds, on the line that
            # promises the payoff — a title over the *promise* rather than over
            # the opening frame, so it costs none of the first five seconds.
            Shot(clip=STREAM / "34127877.mp4",       # L14 S6
                 payload=("", "THE SATOSHI TEST")),
            Shot(image=POSTS / "hackers.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.4),
        ],
    ),

    # --- reframe --------------------------------------------------------
    Section(
        title="So what would count as proof?",
        sentences=[
            ("Start with what Satoshi actually is.",),
            ("Not a face. Not a name.",
             "A set of private keys",
             "that have not moved since two thousand ten."),
            ("Bitcoin was built",
             "so that nobody has to trust anybody."),
            ("Whoever holds one of those keys",
             "can sign a message",
             "that you can check yourself,",
             "on your own machine, in seconds."),
            ("It either validates, or it does not.",),
            ("There is no third answer.",
             "There is no room to argue.",
             "That is the whole design."),
        ],
        shots=[
            Shot(graphic="quote",
                 payload=("Proof beats promises.", "the design of Bitcoin"),
                 picture=POSTS / "satoshi-nakamoto.png"),
            None,
            Shot(image=POSTS / "blockchain-technology.jpg", zoom=1.12,
                 pan=(0.02, 0.01), aspect=A, bias=0.5),
            Shot(clip=KEYS / "8212370.mp4",          # L24 S12
                 payload=("", "Only the key holder can sign")),
            None,
            Shot(graphic="stat",
                 payload=("YES / NO", "THE ONLY TWO ANSWERS",
                          "The maths does not take opinions."),
                 backdrop=POSTS / "analysis.jpg"),
        ],
    ),

    # --- deep dive ------------------------------------------------------
    Section(
        title="There are exactly two ways to end this",
        spoken_title="So there are exactly two ways to end this.",
        sentences=[
            ("Cryptographers broadly agree",
             "on both of them."),
            ("Move a fraction of the coins",
             "mined in two thousand nine.",
             "Or sign a fresh, dated message",
             "with one of those same keys."),
            ("Either one would take an afternoon.",),
            ("Roughly one point one million coins",
             "sit in those early addresses,",
             "and not one of them has ever moved."),
            ("If you held those keys,",
             "you could settle this before lunch.",),
        ],
        shots=[
            Shot(graphic="compare",
                 payload=("Move the coins",
                          ["Spend from a 2009 address",
                           "Auditable by anyone, forever"],
                          "Sign a message",
                          ["A fresh, dated message",
                           "Verified on your own machine"]),
                 backdrop=POSTS / "bitcoin.jpg"),
            None,
            Shot(clip=CIRCUIT / "6755170.mp4",       # L41 S20
                 payload=("", "A fresh, dated message")),
            Shot(graphic="bars",
                 payload=([("Mined by Satoshi, never moved", 0.052, "1.1M"),
                           ("Bitcoin that will ever exist", 1.0, "21M")],
                          "THE SIZE OF THE STACK"),
                 backdrop=POSTS / "bitcoin-mining.jpg"),
            Shot(image=POSTS / "bitcoin-neon.jpg", zoom=1.11, pan=(0.02, -0.01),
                 aspect=A, bias=0.5),
        ],
    ),

    # --- the twist: what everyone offers instead -------------------------
    # `flow=True`. The narration says the verdict itself — "Not a court
    # ruling" — so the cross lands on the word rather than four seconds later.
    Section(
        title="Nobody has ever done either one",
        spoken_title="But nobody has ever done either one.",
        sentences=[
            ("Every claim so far",
             "has offered you something else."),
            ("Not a court ruling.",
             "Not a writing style.",
             "Not old emails.",
             "Not a famous endorsement.",
             "Only a signed message counts."),
            ("Look at what those have in common.",
             "Every one of them asks you to trust a person.",
             "The signature asks you to trust nobody."),
        ],
        shots=[
            Shot(image=POSTS / "law.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="checklist",
                 payload=([("A court ruling", False),
                           ("A writing style", False),
                           ("Old emails", False),
                           ("A famous endorsement", False),
                           ("A signed message", True)],
                          "DOES IT PROVE ANYTHING?",
                          True),                     # flow
                 picture=POSTS / "research.jpg"),
            Shot(image=POSTS / "scammer.jpg", zoom=1.11, pan=(-0.02, -0.01),
                 aspect=A, bias=0.4),
        ],
    ),

    # --- the viewer's turn ----------------------------------------------
    Section(
        title="How would you check it yourself?",
        sentences=[
            ("You do not need to be a cryptographer.",),
            ("Get the address they claim to control.",
             "Get the message and the signature.",
             "Run both through any wallet's verify tool.",
             "Then check the address really dates to two thousand nine."),
            ("Never import an unknown wallet to do it.",
             "You only need the address itself."),
        ],
        shots=[
            Shot(clip=SERVER / "7140928.mp4",        # L29 S43
                 payload=("", "Any wallet can check it")),
            Shot(graphic="checklist",
                 payload=([("Get the address", True),
                           ("Get message and signature", True),
                           ("Verify in any wallet", True),
                           ("Check it dates to 2009", True)],
                          "FOUR STEPS",
                          True),                     # flow
                 picture=POSTS / "security-combination-lock.jpg"),
            Shot(image=POSTS / "hacker.jpg", zoom=1.12, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
        ],
    ),

    # --- the counterintuitive twist -------------------------------------
    # A statement, not a question. The section resolves something rather than
    # opening it, and forcing a question onto it would be worse than saying it.
    Section(
        title="Valid signature. Wrong address.",
        spoken_title="And here is where it gets interesting.",
        sentences=[
            ("That last step",
             "is where the claims quietly fail."),
            ("In two thousand nineteen,",
             "a claimant produced a signature",
             "that was completely valid."),
            ("The maths checked out.",
             "Every tool agreed.",
             "But the address behind it",
             "had nothing to do with Satoshi's mining."),
            ("A valid signature from the wrong address",
             "proves only that you control that address.",
             "Nothing more."),
            ("So attribution matters",
             "as much as the arithmetic does.",
             "Most people never check the second half."),
        ],
        shots=[
            Shot(image=POSTS / "analysis.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(clip=WAVES / "27980029.mp4",        # L4 S5
                 payload=("2019", "The maths checked out perfectly")),
            None,
            Shot(graphic="quote",
                 payload=("Valid signature. Wrong address.",
                          "the 2019 claim, in four words"),
                 picture=POSTS / "scammer.jpg"),
            Shot(image=POSTS / "blockchain-technology.jpg", zoom=1.11,
                 pan=(0.02, -0.01), aspect=A, bias=0.45),
        ],
    ),

    # --- mirror, echo, and the ask --------------------------------------
    Section(
        title="Seventeen years, still unsigned",
        spoken_title="So where does that leave you?",
        sentences=[
            ("One last thing worth knowing.",
             "The very first block cannot be used at all —",
             "its coins were never spendable."),
            ("So the test still stands,",
             "exactly where it was left in two thousand ten."),
            ("Which means the next time you see the headline —",
             "someone has finally proved they are Satoshi —",
             "you already know the only question that matters."),
            ("Did they sign?",),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(image=POSTS / "bitcoin.jpg", zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.5),
            Shot(clip=PARTICLES / "36703282.mp4"),   # L9 S0
            Shot(image=POSTS / "satoshi-nakamoto.jpg", zoom=1.13,
                 pan=(0.02, 0.01), aspect=A, bias=0.35),
            Shot(graphic="stat",
                 payload=("2009", "STILL UNSIGNED",
                          "No key has ever been used."),
                 backdrop=POSTS / "bitcoin-neon.jpg"),
            # Held on the abstract for the outro, so the end-screen elements
            # have somewhere uncluttered to sit when they go on at upload.
            Shot(clip=WAVES / "15690300.mp4"),       # L9 S0
        ],
        # 2.40 after "Did they sign?" — it is the echo the whole video is
        # built toward, and the beat that carries it was on screen for under
        # two seconds in the previous cut.
        gaps=[0.34, 0.34, 0.34, 2.40, 3.20],
    ),
]

META = Meta(
    title="The One Test That Proves Someone Is Satoshi Nakamoto",
    hook="Four people have claimed to be Satoshi Nakamoto. One test settles it "
         "in under a minute, and nobody has ever passed.",
    url=URL,
    summary="What would actually count as proof, what fails however persuasive "
            "it sounds, and how to check a claim yourself in four steps.",
    tags=["satoshi nakamoto", "bitcoin", "crypto security",
          "bitcoin signatures", "dyor"],
    cta=f"Full breakdown, sources and the security checklist: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: generated for this channel."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-satoshi-proof-long.mp4"
    work = Path.home() / "Desktop/.crypto-satoshi-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        # **No burned captions at all.** Showing a handful of lines and not the
        # rest reads as arbitrary; the full transcript ships as the SRT, which
        # YouTube indexes and viewers can switch on.
        callouts=None,
        # Brackets mark the accent phrase, which gets the vibrant box. The
        # layout — which side the type sits on, and the zoom and pan that put
        # the subject opposite it — is searched, not specified. See thumb.py.
        thumb_headline="[Nobody] has passed it",
        thumb_image=POSTS / "satoshi-nakamoto.jpg",
        thumb_accent="red",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
