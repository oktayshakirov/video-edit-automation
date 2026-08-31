"""Quantum computers vs. crypto — long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/quantum-computers-and-crypto.mdx.

**The angle is the honest one, not the headline one.** The article's own framing
is "a large-scale quantum attack is real but distant, and the urgent parts are
Harvest Now, Decrypt Later plus a slow migration". The script opens by naming
the doomsday version, gives the hard number that makes it distant, then spends
the body on the narrower thing that is true *today* — on most chains your
address is a hash of your public key, so the key is hidden while a coin only
sits there, and the first time you spend, the signature publishes the public
key onto a permanent record that cannot be un-published.

**Say "quantum computers", not "quantum".** Bare "quantum" as a noun reads as
jargon and the user flagged it as confusing. Every reference is "quantum
computers" or "a quantum computer"; "qubit" is kept because the number needs a
unit and the stat card glosses it.

**Every clip carries an on-screen line.** `payload=("", "…")` puts a big centred
statement on the footage — the user's note was that stock playing silently under
specific narration is hard to follow, so the point is always on screen, not only
in the voice. Drawn beats carry their own text.

**Every drawn beat's sentence enumerates its own items, one caption chunk per
reveal** — this is `beats.md`'s rule and the first cut broke it: the `compare`
and `steps` beats had narrative sentences with three chunks against six-plus
reveals, so the beat filled in out of sync with the voice. The beat sentence is
now the list; the sentences around it set it up and pay it off.

**A checklist with a struck item spells out why.** The user's note: a lone ✗ in
a list is confusing. The `checklist` here is titled as a yes/no question
("CAN IT BE MIGRATED?") and every spoken chunk states its own verdict -
"doable" three times, then "never" - so the mark is never doing the explaining
on its own.

**No financial advice.** Mechanism only: no price, no prediction (timelines are
hedged), nothing rated, nothing recommended. The close asks the viewer whether
they are worried and what they do to stay safe — a comment prompt, not a call.

**Phonemes, checked with espeak.** `qubit` -> `kjˈuːbɪt`, `quantum` ->
`kwˈɔntəm`, `algorithm` -> `ˈælɡɚɹˌɪθəm` — all read plainly. `ECDSA`, `RSA`,
`SHA-256`, `NIST` are avoided; the script says "the signature", "a longer hash"
and "researchers". "Shor's algorithm" is dropped this pass — "a quantum
computer can reverse it" is clearer and needs no name.

**Delivery.** Kokoro (`mia`) has no prosody control — that ceiling is in
`voice.md`. Within it, this pass is written for the engine: short declaratives,
full stops as beats (a period is the one punctuation lever Kokoro honours, at
2-3x a comma), and the per-sentence `gaps` placed where the sense turns.

**Assets are fresh** — fetched and screened for this pair, used by no other
crypto video. Ranges are in the trailing comment on each constant.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/quantum-crypto.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"
PH = STOCK / "photos"

# --- fresh stock, screened; trailing comment is duration + luma/sat range ---
PALM = STOCK / "videos/fingerprint-biometric-scan-dark/16392048.mp4"            # 17.0s L25 S8
WHORL = STOCK / "videos/fingerprint-biometric-scan-dark/28179927.mp4"           # 20.0s L32 S7
RACKS = STOCK / "videos/supercomputer-racks-blinking-lights-dark/12138721.mp4"   # 18.0s L14 S11
PANEL = STOCK / "videos/supercomputer-racks-blinking-lights-dark/13550579.mp4"   # 10.0s L5 S7
HALL = STOCK / "videos/server-hallway-lights-dark/19217898.mp4"                  # 10.0s L25 S3
CODE = STOCK / "videos/code-scrolling-screen-terminal-dark/34268861.mp4"        # 18.0s L16 S14
CHIP = STOCK / "videos/microchip-processor-macro-dark/2792370.mp4"              # 10.0s L11 S0
TUNNEL = STOCK / "videos/digital-tunnel-data-stream-dark/33113400.mp4"          # 20.0s L12 S0
WAIT = STOCK / "videos/person-waiting-dark-contemplative/28828933.mp4"          # 16.0s L20 S6
CLOCK = STOCK / "videos/clock-ticking-dark-macro/29527767.mp4"                  # 10.0s L7 S3
LEDGER = STOCK / "videos/digital-ledger-blocks-chain-dark/34128900.mp4"         # 20.0s L18 S10
FIELD = STOCK / "videos/abstract-digital-data-particles-dark/34645139.mp4"      # 20.0s L29 S0

CRYO = PH / "cryostat-quantum-computer/30547566.jpg"          # 8192x4320 L22 S11 — a real dilution fridge
EDITOR = PH / "code-on-screen-dark/256502.jpg"                # 6016x4000 L15 S15
DESK = PH / "code-on-screen-dark/5380603.jpg"                 # 6000x4000 L22 S3
CIRCUIT = PH / "encryption-padlock-circuit-dark/3520697.jpg"  # 6016x4000 L16 S0
BOKEH = PH / "dark-abstract-gold-particles-bokeh/30278259.jpg"  # 6000x4000 L18 S3
# Thumbnail only - the user's pick. Magnetic field lines round a glowing core:
# reads as quantum physics, centred subject, dark corners for the type.
MAGFIELD = PH / "magnetic-field-lines/38032287.jpg"          # 3840x2160 L34 S36

# The article's own hero. 800x448 - beat picture column only, never a full frame.
QC = POSTS / "quantum-computing.png"

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://thecrypto.wiki/posts/quantum-computers-and-crypto"

A = 16 / 9


SECTIONS = [
    # --- hook. No card. Name the doomsday version, then the hard number. -----
    Section(
        title="What quantum computers threaten",
        card=False,
        sentences=[
            ("Quantum computers are coming for crypto.",),
            ("But not the way the headlines say.",),
            ("The scary version is one machine.",
             "It cracks Bitcoin overnight.",
             "Every wallet, drained at once."),
            ("That machine needs millions of error-free qubits.",),
            ("The best one today has a few hundred.",
             "And they are noisy."),
            ("Nobody serious names a date before the twenty-thirties.",),
            ("So the chain is not falling this year.",),
            ("But the clock has already started.",
             "And some of your coins are exposed right now."),
        ],
        shots=[
            Shot(clip=PALM, clip_at=1.0),
            Shot(clip=PANEL, clip_at=0.5,
                 payload=("", "Not the way the headlines say")),
            Shot(clip=TUNNEL, clip_at=1.0,
                 payload=("", "One machine. Every wallet. Overnight.")),
            Shot(graphic="stat",
                 payload=("Millions", "ERROR-FREE QUBITS TO BREAK ONE KEY",
                          "The best machine today has a few hundred, and they are noisy"),
                 backdrop=BOKEH),
            None,                                    # hold the figure
            Shot(clip=CLOCK, clip_at=0.5,
                 payload=("", "No credible date before the 2030s")),
            None,
            Shot(clip=HALL, clip_at=0.5,
                 payload=("", "WHICH COINS ARE EXPOSED RIGHT NOW?")),
        ],
        gaps=[0.65, 0.90, 0.34, 0.60, 0.85, 0.70, 0.90, 0.70],
    ),

    # --- reframe: two kinds of crypto, quantum only breaks one --------------
    Section(
        title="What can a quantum computer break?",
        sentences=[
            ("Every blockchain runs on two kinds of math.",),
            ("Signatures prove a coin is yours.",
             "Hashing runs mining, and builds your address."),
            # THE COMPARE BEAT. name_columns=True -> 2 headings + 6 items = 8
            # reveals, so this sentence is 8 chunks in exactly that order.
            ("Signatures.",
             "They prove a coin is yours.",
             "One-way math, for now.",
             "A quantum computer can reverse it.",
             "Now hashing.",
             "It runs mining and addresses.",
             "A quantum computer only half-dents it.",
             "A longer hash fixes that."),
            ("So a quantum computer does not break the chain.",),
            ("It breaks the signature.",
             "It comes for your key."),
        ],
        shots=[
            Shot(clip=CHIP, clip_at=0.5,
                 payload=("", "Two kinds of math. One is vulnerable.")),
            Shot(image=CIRCUIT, zoom=1.10, pan=(0.02, 0.01), aspect=A, bias=0.5),
            Shot(graphic="compare",
                 payload=("Signatures",
                          ["Prove a coin is yours",
                           "One-way math, for now",
                           "A quantum computer reverses it"],
                          "Hashing",
                          ["Runs mining and addresses",
                           "Only half-dented",
                           "A longer hash fixes it"],
                          True),
                 ),
            Shot(clip=RACKS, clip_at=1.0,
                 payload=("", "The chain itself is safe")),
            Shot(clip=WHORL, clip_at=1.0,
                 payload=("", "Your key is the target")),
        ],
        gaps=[0.60, 0.70, 1.30, 0.85, 0.90],
    ),

    # --- deep dive: your key goes public the moment you spend --------------
    Section(
        title="Is your key already public?",
        sentences=[
            ("It depends on one thing.",
             "Have you ever spent from that address?"),
            # THE STEPS BEAT. 5 nodes -> this sentence is 5 chunks, one per node.
            ("Start with your private key.",
             "It creates your public key.",
             "Your address is just a hash of that.",
             "While you only receive, the key stays hidden.",
             "Your first spend puts it in the open."),
            ("Never spent from an address?",
             "Then there is nothing there to break. Yet."),
            ("But spend once,",
             "and your wallet publishes the key."),
            ("Onto the permanent record. Forever.",),
            ("Every address you have spent from is exposed.",
             "Reuse one, and it just sits there. Waiting."),
        ],
        shots=[
            Shot(image=DESK, zoom=1.10, pan=(0.02, -0.01), aspect=A, bias=0.5),
            Shot(graphic="steps",
                 payload=([("Private key", "\U0001F511"),
                           ("Public key", "\U0001F513"),
                           ("Address = its hash", "\U0001F3F7️"),
                           ("Receiving: hidden", "\U0001F512"),
                           ("First spend: public", "\U0001F4E3")],
                          "HOW YOUR KEY GETS EXPOSED")),
            Shot(image=CRYO, zoom=1.11, pan=(-0.02, 0.01), aspect=A, bias=0.5),
            Shot(clip=CODE, clip_at=1.0,
                 payload=("", "Your wallet publishes your public key")),
            Shot(clip=LEDGER, clip_at=1.0,
                 payload=("", "Now it is on the record, forever")),
            Shot(image=EDITOR, zoom=1.12, pan=(-0.02, -0.01), aspect=A, bias=0.5),
        ],
        gaps=[0.70, 1.30, 0.85, 0.60, 0.90, 0.90],
    ),

    # --- twist: you can be a target today, with no quantum computer -------
    Section(
        title="Harvest now, decrypt later",
        sentences=[
            ("Here is why today matters.",),
            ("An attacker copies your exposed key now.",
             "It is public. It is free. It is already on chain."),
            ("Then they wait for the hardware.",
             "And break it years later."),
            ("The name for this is: harvest now, decrypt later.",),
            ("And a blockchain is the perfect thing to harvest.",),
            ("It is a public record that never forgets.",),
            ("You cannot un-publish a key from twenty seventeen.",),
        ],
        shots=[
            Shot(image=EDITOR, zoom=1.11, pan=(0.02, 0.01), aspect=A, bias=0.45),
            Shot(image=CIRCUIT, zoom=1.11, pan=(-0.02, 0.01), aspect=A, bias=0.45),
            Shot(clip=WAIT, clip_at=1.0,
                 payload=("", "...then wait for the hardware")),
            Shot(graphic="quote",
                 payload=("Harvest now. Decrypt later.",
                          "the attack that needs no quantum computer yet"),
                 picture=QC),
            None,                                    # hold the quote
            None,
            Shot(clip=CLOCK, clip_at=0.5,
                 payload=("", "You cannot un-publish a key")),
        ],
        gaps=[0.60, 0.70, 0.85, 0.90, 0.60, 0.85, 0.90],
    ),

    # --- twist 2: fixable, but the migration is the hard part -------------
    Section(
        title="Can't they just patch it?",
        sentences=[
            ("They can.",
             "It has already started."),
            ("Researchers picked new signature schemes.",
             "Quantum computers cannot reverse them.",
             "The first ones were locked in, in twenty twenty-four."),
            ("The math is the easy part.",
             "Moving everyone onto it is not."),
            # THE CHECKLIST BEAT. The title asks a yes/no question and every
            # chunk states its own verdict out loud, so a struck item is never
            # ambiguous - the voice says "doable" three times, then "never".
            ("A coordinated upgrade? Doable.",
             "A new address format? Doable.",
             "Every wallet moving at once? Doable.",
             "Coins with lost keys? Never."),
            ("Small networks that planned ahead have it easy.",
             "The big chains are still working on it."),
            ("But that last answer never changes.",),
            ("Lost wallets. Forgotten coins. The oldest ones of all.",),
            ("They stay on the old math. In the open. For good.",),
        ],
        shots=[
            Shot(clip=CHIP, clip_at=0.5,
                 payload=("", "The fix already exists")),
            Shot(image=CIRCUIT, zoom=1.10, pan=(0.02, 0.01), aspect=A, bias=0.5),
            Shot(image=DESK, zoom=1.11, pan=(-0.02, 0.01), aspect=A, bias=0.45),
            Shot(graphic="checklist",
                 payload=([("A coordinated upgrade", True),
                           ("A new address format", True),
                           ("Every wallet at once", True),
                           ("Coins with lost keys", False)],
                          "CAN IT BE MIGRATED?",
                          True),                     # flow — narration says each verdict
                 picture=EDITOR),
            Shot(clip=TUNNEL, clip_at=1.0,
                 payload=("", "A few chains planned ahead. Most didn't.")),
            None,                                    # hold the footage
            Shot(clip=HALL, clip_at=0.5,
                 payload=("", "Lost keys can never be upgraded")),
            Shot(image=CRYO, zoom=1.12, pan=(-0.02, 0.01), aspect=A, bias=0.5),
        ],
        gaps=[0.60, 0.60, 0.90, 1.30, 0.80, 0.90, 0.70, 0.95],
    ),

    # --- mirror, echo, the ask. The card resolves -> a statement. ---------
    Section(
        # No spoken_title: the card speaks its own statement title, and the
        # first sentence asks the question. Writing both said "how worried
        # should you be" twice, 3s apart.
        title="The chain holds. Your key is the target.",
        sentences=[
            ("So, how worried should you be?",),
            ("The overnight-doomsday version is still years away.",
             "And the networks would get a warning."),
            ("The real risk is quieter than that.",),
            ("Exposed keys on every address you have spent from.",
             "A record that keeps them forever.",
             "A migration no one has run at this scale."),
            ("None of it needs the doomsday machine.",
             "It just needs time."),
            ("So, a question for you.",),
            ("Are you worried about quantum computers yet?",
             "And what are you doing to keep your crypto safe?",
             "Tell me in the comments."),
            ("The full breakdown is linked below,",
             "and nothing here is financial advice."),
            ("If this helped, subscribe for more.",),
        ],
        shots=[
            Shot(image=CRYO, zoom=1.10, pan=(0.02, 0.01), aspect=A, bias=0.5),
            None,                                    # hold the cryostat
            Shot(clip=PANEL, clip_at=0.5,
                 payload=("", "The real risk is quieter")),
            Shot(image=DESK, zoom=1.11, pan=(0.02, 0.01), aspect=A, bias=0.5),
            None,                                    # hold
            Shot(image=EDITOR, zoom=1.11, pan=(-0.02, -0.01), aspect=A, bias=0.45),
            Shot(clip=PALM, clip_at=1.0,
                 payload=("", "Are you worried yet?")),
            Shot(image=CIRCUIT, zoom=1.10, pan=(0.02, -0.01), aspect=A, bias=0.5),
            # Held on the abstract, uncluttered, for YouTube's end-screen cards.
            Shot(clip=FIELD, clip_at=1.0),
        ],
        gaps=[0.85, 0.80, 0.85, 0.70, 0.90, 0.70, 2.20, 0.55, 3.00],
    ),
]

META = Meta(
    title="Quantum Computers vs. Crypto: What Actually Breaks",
    hook="A quantum computer cracking Bitcoin overnight is the headline. The "
         "real risk right now is narrower - and it is already on the chain.",
    url=URL,
    summary="What quantum computers actually threaten in crypto: why the "
            "signature is the target and not the chain, how your public key "
            "goes on the permanent record the first time you spend, what "
            "'harvest now, decrypt later' means, and why the post-quantum "
            "migration is the slow, hard part.",
    tags=["quantum computers crypto", "quantum computing bitcoin",
          "is bitcoin quantum safe", "post-quantum cryptography",
          "harvest now decrypt later", "quantum computing explained",
          "crypto security", "crypto for beginners"],
    cta=f"The full breakdown of the quantum threat and post-quantum crypto: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/quantum-crypto-long.mp4"
    work = Path.home() / "Desktop/.quantum-crypto-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # The title carries the search phrase; the thumbnail asks the question
        # it does not answer. Orange accent because the source is blue - cyan
        # would blend into the field lines.
        thumb_headline="Can quantum computers [break] Bitcoin?",
        thumb_image=MAGFIELD,
        thumb_accent="orange",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
