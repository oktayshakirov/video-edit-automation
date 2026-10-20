"""Can AI run on the blockchain - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/decentralized-ai-can-ai-run-on-the-blockchain.mdx.

**The angle.** "Decentralized AI" sounds like a model living on a blockchain,
and the confident version of that claim is everywhere. The video's job is the
mechanism underneath it, and the honest answer it leads to: a blockchain is
thousands of computers repeating every step, which is what makes it
trustworthy and what makes it the most expensive place there is to do math.
So the big models stay off the chain; what goes on it is a proof, the payment
and a deposit. The twist is what a proof cannot do - it proves the math was
done, never that the answer is true - so the hard rules live in the contract.
The close echoes the open: the chain does not think, it checks.

**No financial advice.** It describes how computation is priced and checked.
It names no price level, no token, no project and no platform, predicts
nothing, and recommends nothing. The article's two case studies are left
out: both are unnamed teams with unverifiable figures, and one quotes a
trading return. No shot shows a chart, ticker or price.

**Figures.** The article's own: a 7-billion-parameter model, "tens to
hundreds of billions" of operations per response, proof checks at 200,000 to
1.5 million gas, verification in hundreds of milliseconds against minutes to
generate, storing weights on-chain costing millions, 12-second Ethereum
blocks. Arithmetic on them, from the EVM's own price list: one token of a 7B
model is ~7 billion multiply-adds; MUL is 5 gas and ADD 3, so 56 billion gas
*at the cheapest*, before a single weight is loaded and with no floating
point in the EVM at all. Ethereum mainnet's block gas limit is 60 million
(October 2026, with ~200 million tested on Sepolia for Glamsterdam), so the
script says "well under a billion" and "hundreds of blocks", which hold at
either - 933 blocks today, ~280 at 200M. 1.5M / 60M is "about a fortieth of
one block, at most", and it only gets smaller as the limit rises. "One word"
is a token, roughly a word; the description says so.

## The beats

Last three crypto long forms: bear-market-in-crypto (bars / diagram / chart /
steps / stat), bitcoin-halving (steps / bars / diagram / compare / timeline),
market-cap (bars / gauge / grid / chart / diagram / checklist). `diagram` was
in all three, so it sits this one out.

* `replicate` - **new, built for this video.** One job card fanning out into
  a grid of node tiles whose bars all fill in lockstep: every computer on the
  network doing the same math. The library had no picture of replication,
  and it is the noun every blockchain topic rests on.
* `gauge` - one word of a 7B model against one block's room. The limit is
  the whole point, which is what `gauge` is for.
* `compare` - what stays off the chain against what goes on it.
* `grid` - the three ways an answer gets trusted: a proof, a challenge
  window, an oracle.
* `checklist`, `flow=True` - CAN THE CHAIN PROVE IT? Three ticks and one
  cross, with the voice saying each verdict.

No outline overlaps bear-market's set; three overlap market-cap's, which is
two videos back.

**Opener: the redacted hook**, `One word from an AI fills [hundreds] of
blocks`, revealed in sentence 1 at ~2s. Last three long forms opened
Search / Counter / Stamp. The hidden word is a number, which passes the
cover-the-bar test, and it is not the answer to the video's question - what
a blockchain *does* for an AI.

**Footage: the act, in the subject's world** (`footage.md`). Hands at a
laptop for "the AI you use", a processor, a CPU being seated, a motherboard,
a graphics card, a server corridor, drives being slotted for "storing the
model", a countdown for the challenge window, a key in a steel locker for
"holds the money", coins falling for a lost deposit, ink clouding water for
poisoned data, a padlock for the rules in the contract. Two gold node-network
renders carry "the model" and "thousands of computers" - the only drawn-
looking footage, and both are the noun. Every clip is fresh; verdicts in
`footage.md`. The one abstract is the particle swirl under the disclaimer.

**Thumbnail:** the `replicate` beat itself as a still, shifted right, with
the title's question on the black (`thumbnails.md`: a concept video's
thumbnail is the concept, drawn, never a stranger's face).

    PYTHONPATH=. .venv/bin/python projects/crypto-long/decentralized-ai.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
import numpy as np
from PIL import Image

from video_automation.longform import Meta, Section, render_long
from video_automation.longform import thumb as T

SOURCE_POST = "decentralized-ai-can-ai-run-on-the-blockchain"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Every clip fetched fresh for this pair and looked at on a labelled
# three-frame contact sheet (15/50/85% of its length).
KEYS = V / "hands-typing-keyboard-dark/5495784.mp4"               # 18s, L17, hands typing on a laptop in the dark
TOPDOWN = V / "hands-typing-keyboard-dark/5495845.mp4"            # 21s, L46-48, top-down hands on a laptop, code on screen - KEYS's shoot, kept apart
CHIP = V / "circuit-board-close-up-dark/6755158.mp4"              # 18s, L19-36, one processor die on dark stone
CPU = V / "cpu-processor-installing/11537353.mp4"                 # 10s, L89-94, fingers seating a CPU in its socket
MOBO = V / "motherboard-assembling/9373207.mp4"                   # 14s, L100-109, hands working on a motherboard
BOARD = V / "circuit-board-close-up-dark/6754820.mp4"             # 13s, L71-72, a gold-orange circuit board, slow push
GPU = V / "graphics-card-close-up-dark/3147349.mp4"               # 20s, L47-48, a graphics card's fan in a lit case - purple, but the noun
CORRIDOR = V / "supercomputer/32386520.mp4"                       # 11s, L44-54, a corridor between server racks
NET = V / "neural-network-visualization/37101560.mp4"             # 10s, L30-73, a gold network of fibres - the model
NODES = V / "neural-network-visualization/34992913.mp4"           # 10s, L21-22, nodes joined by lines - many computers, one record
NODES2 = V / "neural-network-visualization/34994032.mp4"          # 10s, L21-23, NODES's look - cut straight after it, as one picture
BACKLIT = V / "rows-of-computers-office-night/36036749.mp4"       # 14s, L7-11, a backlit keyboard under a hand in the dark
PHONE = V / "smartphone-typing-message-night/39494839.mp4"        # 20s, L31-38, a thumb typing on a phone keyboard
DRIVES = V / "data-center-corridor-servers/38496190.mp4"          # 15s, L61-72, a hand slots drives into an enclosure
COINS = V / "stack-of-coins-dark/5253412.mp4"                     # 27s, L25-41, coins across a dark table
FALLING = V / "coin-slot-dropping-coin/5305003.mp4"               # 21s, L90-96, coins dropping and scattering on stone
COUNTDOWN = V / "stopwatch-close-up/9944842.mp4"                  # 25s, L27-30, a red LED digit counting down to 0
LOCKER = V / "bank-vault-door/39060937.mp4"                       # 24s, L42-47 after 2s, a key turned in a steel locker
PADLOCK = V / "padlock-closing-dark/4889026.mp4"                  # 13s, L43-45, a padlock's shackle, close
INK = V / "ink-drop-in-water-dark/7565451.mp4"                    # 31s, L20-34, ink clouding through dark water
SWIRL = V / "graphics-card-fan-spinning-black/33830775.mp4"       # 8s,  L10-13, a slow particle vortex - the one abstract

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/decentralized-ai-can-ai-run-on-the-blockchain"

# `Ethereum` phonemizes as ee-thuh-REE-um (`voice.md`); the caption keeps the
# real spelling and the engine gets the respell.
ETH = ("Ethereum", "Etheerium")


def es(text: str) -> tuple[str, str]:
    """(caption, spoken) with every respell applied to the spoken half."""
    return text, text.replace(*ETH)


SECTIONS = [
    # --- hook. No card. The redacted hook hides a number sentence 1 says. --
    Section(
        title="The AI you use",
        card=False,
        sentences=[
            # The number goes in sentence 1: as sentence 2 the hidden word
            # was spoken at 5.1s, past the hook's 4.2s latest, and the
            # reveal fell back to 3.0s - ahead of the voice.
            ("One word from your AI would fill hundreds of blocks.",),
            ("So the AI you use could not run on a blockchain.",),
            ("And yet there is a whole field called decentralized AI.",),
            ("So what does a blockchain actually do for an AI,",
             "if it cannot run one?"),
            ("Stay to the end,",
             "and you will know the one thing the chain can check,",
             "and the one thing it never can."),
        ],
        shots=[
            Shot(clip=KEYS, clip_at=1.0),
            Shot(clip=CPU, clip_at=0.5),
            Shot(clip=NET, clip_at=0.5),
            Shot(clip=CORRIDOR, clip_at=0.5),
            Shot(clip=TOPDOWN, clip_at=1.0),
        ],
        gaps=[0.70, 0.85, 0.70, 0.80, 0.90],
    ),

    # --- what a blockchain is: replication ---------------------------------
    Section(
        title="What is a blockchain good at?",
        spoken_title="So what is a blockchain actually good at?",
        sentences=[
            ("A blockchain is not one computer.",
             "It is thousands of them, keeping one record together."),
            ("Every one of them repeats every step,",
             "and checks that the others got the same result."),
            # the replicate beat's own sentence: the job, then the copies.
            ("Send it one job, like a single word from an AI model,",
             "and every computer on the network does the same math, again."),
            ("That repetition is the whole point.",),
            ("No one machine decides, so nobody has to trust one.",),
            ("But it also makes a blockchain the most expensive place there is to do math.",),
        ],
        shots=[
            Shot(clip=NODES, clip_at=0.5),
            # NODES's look again, so the two read as one continuing picture:
            # the drives were here first and looked identical to DRIVES a
            # minute later.
            Shot(clip=NODES2, clip_at=1.0),
            Shot(graphic="replicate", backdrop=BEATGROUND,
                 payload=("ONE JOB", "a single word from an AI model",
                          "x THOUSANDS", "every computer, the same math",
                          "WHO DOES THE MATH?")),
            None,
            Shot(clip=BACKLIT, clip_at=1.0),
            Shot(clip=BOARD, clip_at=1.0),
        ],
        gaps=[0.55, 0.60, 1.30, 0.50, 0.55, 0.85],
    ),

    # --- the arithmetic ------------------------------------------------------
    Section(
        title="Could a big AI model run on-chain?",
        spoken_title="So could a big AI model run on the chain?",
        sentences=[
            (es("On Ethereum, every step a program takes has a price,"),
             "paid in units called gas."),
            ("And every block has a ceiling on how much gas fits inside it.",),
            ("Now take a mid-sized AI model, with seven billion parameters.",),
            ("Every word it writes takes about seven billion multiplications,",
             "and as many additions."),
            (es("At the cheapest price Ethereum charges for those,"),
             "that is fifty-six billion units of gas, for one word."),
            # the gauge's own sentence: the limit first, the value second.
            ("A full block has room for well under a billion.",
             "That one word needs fifty-six billion."),
            ("So a single word would take hundreds of blocks,",
             "back to back, twelve seconds apart."),
            ("And storing the model itself on the chain would cost millions more.",),
            ("So the big models stay off the chain.",
             "What goes on it is something else."),
        ],
        shots=[
            Shot(clip=COINS, clip_at=1.0),
            None,
            Shot(clip=NET, clip_at=4.0,
                 note=("7B", "parameters in a mid-sized model")),
            Shot(clip=CHIP, clip_at=1.0),
            Shot(clip=MOBO, clip_at=1.0,
                 note=("56B gas", "one word, at the cheapest rate")),
            Shot(graphic="gauge", backdrop=BEATGROUND,
                 payload=("56 BILLION", 0.97, "one word of the answer",
                          0.05, "one full block",
                          "DOES ONE WORD FIT IN A BLOCK?")),
            Shot(clip=KEYS, clip_at=9.0),
            Shot(clip=DRIVES, clip_at=1.0),
            None,
        ],
        gaps=[0.55, 0.60, 0.50, 0.55, 0.70, 1.40, 0.60, 0.60, 0.90],
    ),

    # --- what goes on the chain --------------------------------------------
    Section(
        title="What does decentralized AI put on-chain?",
        spoken_title="So what does decentralized AI actually put on the chain?",
        sentences=[
            ("It splits the job in two.",),
            # the compare's own sentence: a heading chunk, three items, twice.
            ("Off the chain, on ordinary hardware,",
             "the model itself,",
             "the heavy math,",
             "and the data it reads.",
             "And on the chain,",
             "a proof of what ran,",
             "the payment,",
             "and a deposit it can lose."),
            ("The model runs on graphics cards, like any other AI.",),
            ("Then it hands back its answer, with a way to check it.",),
            # the grid's own sentence - one chunk per card.
            ("A proof, which the chain checks with math.",
             "A challenge window, where anyone can dispute the answer.",
             "Or an oracle, a service you trust to vouch for it."),
            ("Making a proof can take minutes.",
             "Checking it takes well under a second."),
            ("And it costs, at most, about a fortieth of one block.",),
            ("With a challenge window, the answer stands unless someone proves it wrong.",),
            ("And a provider that lied loses the deposit it put down.",),
            ("So the chain does not do the thinking.",
             "It checks the work, and it holds the money."),
        ],
        shots=[
            Shot(clip=NODES, clip_at=5.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("OFF THE CHAIN",
                          ["The model", "The heavy math", "The data it reads"],
                          "ON THE CHAIN",
                          ["A proof of what ran", "The payment",
                           "A deposit at stake"], True)),
            Shot(clip=GPU, clip_at=1.0),
            Shot(clip=PHONE, clip_at=1.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("A proof", "the chain checks the math", "\U0001F510"),
                           ("A challenge window", "anyone can dispute the answer", "⏳"),
                           ("An oracle", "a service vouches for it", "\U0001F91D")],
                          "HOW DOES THE CHAIN TRUST THE ANSWER?")),
            Shot(clip=TOPDOWN, clip_at=10.0),
            Shot(clip=CHIP, clip_at=9.0,
                 note=("1.5M gas", "the most one proof check costs")),
            Shot(clip=COUNTDOWN, clip_at=1.0),
            Shot(clip=FALLING, clip_at=0.5),
            Shot(clip=LOCKER, clip_at=0.5),
        ],
        gaps=[0.55, 1.30, 0.50, 0.55, 1.20, 0.55, 0.55, 0.50, 0.55, 0.90],
    ),

    # --- the twist -----------------------------------------------------------
    # The turning point, so the card gets the longer silence.
    Section(
        title="What can't a proof prove?",
        spoken_title="So what can a proof not prove?",
        card_gap=1.30,
        sentences=[
            ("A proof says the math was done, exactly as written.",),
            # the checklist's own sentence: the voice says each verdict.
            ("It can prove which model ran,",
             "what it was given,",
             "and that the math was done.",
             "It cannot prove the answer is true."),
            ("Train a model on poisoned data, and it gives a poisoned answer,",
             "with a perfect proof."),
            ("And a cleverly worded prompt can talk a model into the wrong answer.",),
            ("The proof checks out anyway.",),
            ("So the hard rules cannot live inside the model.",
             "They live in the contract around it."),
            ("A cap on what it can spend.",
             "A limit on how far a price can slip.",
             "A list of addresses it is allowed to pay."),
            ("Those rules do not guess.",
             "The contract refuses anything outside them."),
        ],
        shots=[
            Shot(clip=BOARD, clip_at=6.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Which model ran", True),
                           ("What it was given", True),
                           ("That the math was done", True),
                           ("That the answer is true", False)],
                          "CAN THE CHAIN PROVE IT?", True)),
            # Empty black water for its first ~2s; the cloud is in by 3.5.
            Shot(clip=INK, clip_at=3.5),
            Shot(clip=BACKLIT, clip_at=5.0),
            None,
            Shot(clip=PADLOCK, clip_at=1.0),
            Shot(clip=COINS, clip_at=12.0),
            # A part that seats one way only - the rule does not guess.
            Shot(clip=CPU, clip_at=4.5),
        ],
        gaps=[0.55, 1.30, 0.60, 0.50, 0.85, 0.55, 0.60, 0.90],
    ),

    # --- close: the echo -----------------------------------------------------
    Section(
        title="Can AI run on a blockchain?",
        spoken_title="So, can AI run on a blockchain?",
        sentences=[
            ("Not the big models.",
             "What runs there is the receipt, the rules and the money."),
            ("The blockchain does not think. It checks.",),
            ("Nothing in this video is financial advice.",),
            ("So, the next time a project says its AI runs on the blockchain,",
             "would you ask what the chain actually checks?"),
        ],
        shots=[
            Shot(clip=CORRIDOR, clip_at=5.0),
            # Where the thinking actually happens, under "does not think".
            Shot(clip=GPU, clip_at=9.0),
            Shot(clip=SWIRL, clip_at=0.5,
                 payload=("", "This is not financial advice.")),
            # The settled coins, after they have fallen - quiet under the ask.
            Shot(clip=FALLING, clip_at=10.0),
        ],
        gaps=[0.85, 0.90, 1.10, 2.30],
    ),
]

META = Meta(
    title="Can AI Run on the Blockchain? Decentralized AI Explained",
    hook="One word from the AI you use would fill hundreds of blockchain "
         "blocks, so it could not run on one. Here is why: what a "
         "blockchain actually is, the arithmetic of running a 7-billion-"
         "parameter model on Ethereum, what decentralized AI really puts on "
         "the chain instead, and the one thing a proof can never prove.",
    url=URL,
    summary="What decentralized AI is and how it works: a blockchain is "
            "thousands of computers repeating every step and checking each "
            "other, which makes it trustworthy and makes computation "
            "expensive; every step on Ethereum is priced in gas and every "
            "block has a gas limit; one token (roughly one word) from a "
            "7-billion-parameter model takes about seven billion "
            "multiplications and as many additions, which is 56 billion gas "
            "at the cheapest EVM prices against a block that holds well under "
            "a billion, so hundreds of blocks per word; so the model runs "
            "off-chain on ordinary hardware and the chain holds a proof, the "
            "payment and a deposit; three ways to trust an off-chain answer - "
            "a cryptographic proof checked on-chain, an optimistic challenge "
            "window, or an oracle; and what a proof cannot prove - that the "
            "answer is true - which is why poisoned models and prompt "
            "injection are still risks and why hard limits live in the smart "
            "contract. Nothing here is financial advice.",
    tags=["decentralized ai", "can ai run on the blockchain",
          "ai on blockchain", "decentralized ai explained",
          "ai and blockchain", "zkml", "verifiable ai", "on-chain ai",
          "ethereum gas limit", "ai crypto explained",
          "blockchain explained"],
    cta=f"The full guide to decentralized AI: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)

# One bracketed word in the 16:9 column (`thumbnails.md`): the title's own
# question, with the plate on BLOCKCHAIN.
HEADLINE = "Can AI run on a [blockchain?]"


HAND = Path("assets/stock/photos/bionic-hand/6153354.jpg")   # cottonbro studio, Pexels


def thumbs(out: Path) -> Path:
    """The 16:9 thumbnail, re-cut 2026-10-20: a bionic hand touching a human
    finger, the whole photograph with no scrim, and the headline in the empty
    lower-left corner on a local dark fade that stays clear of both hands.

    The user replaced the drawn `replicate` still below (`thumbs_beat`); a
    scrimmed `render_thumb` crop hid the human hand and set the type over the
    touch, which is the whole picture.
    """
    src = Image.open(HAND).convert("RGB")
    h = round(src.height * 1280 / src.width)
    im = src.resize((1280, h), Image.LANCZOS).crop((0, 60, 1280, 780))
    a = np.asarray(im).astype(float)
    yy, xx = np.mgrid[0:720, 0:1280]
    d = np.sqrt((xx / 900.0) ** 2 + ((yy - 720) / 440.0) ** 2)
    m = np.clip(1.25 - d, 0, 1) ** 1.4 * 0.92
    im = Image.fromarray((a * (1 - m[..., None])).astype("uint8"))
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "Can AI\nrun on a\n[blockchain?]", 120, 560, 48, fill, ink,
                max_lines=3, leading=1.02, band="bottom", margin=44,
                shadow=11, drop=(5, 6))
    im.save(out, quality=92)
    return out


def thumbs_beat(out: Path) -> Path:
    """The original 16:9 thumbnail: the `replicate` beat as a still, drawn at full
    size and *downscaled* into the right of the frame, the title's question
    on black at the left - no water, so the type and the beat share one
    ground.

    Handing the still to `render_thumb` upscaled it into a soft crop, and the
    accent plate landed on the grid's first column. Composed by hand at 1920
    and brought down to 1280, the beat stays sharp and the type has its own
    ground.
    """
    from video_automation.core.frame import LANDSCAPE
    from video_automation.longform.beats import Replicate
    b = Replicate("ONE JOB", "a single word from an AI model",
                  "x THOUSANDS", "every computer, the same math", "",
                  brand=CRYPTO, frame=LANDSCAPE, reveals=[0.0, 0.2],
                  start=0.0, hold=10.0)
    # The content alone, on black: the beat's own water ground, pasted onto
    # a second copy of it, left a visible rectangle where the two met.
    beat = Image.new("RGB", LANDSCAPE.size, (0, 0, 0))
    b.content(beat, 1.0)
    beat = beat.crop((270, 270, 1650, 1070))
    beat = beat.resize((960, int(960 * beat.height / beat.width)),
                       Image.LANCZOS)
    canvas = Image.new("RGB", LANDSCAPE.size, (0, 0, 0))
    canvas.paste(beat, (1920 - beat.width - 50, (1080 - beat.height) // 2 + 20))
    im = canvas.resize((1280, 720), Image.LANCZOS)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 150, 520, 50, fill, ink, max_lines=4,
                leading=1.02, band="middle", margin=40, shadow=11, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/decentralized-ai-long.mp4"
    work = Path.home() / "Desktop/.decentralized-ai-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # A number, said in sentence 1, and not the answer to the question.
        # Last three long forms opened Search / Counter / Stamp.
        hook="One word from an AI fills [hundreds] of blocks",
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/decentralized-ai-long-thumb.jpg"))
    else:
        main()
