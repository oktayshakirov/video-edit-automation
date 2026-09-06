"""Why Was Ethereum Created? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/crypto-ogs/vitalik-buterin.mdx. Built as a pair with
`crypto-short/vitalik-ethereum.py`. One article at two angles, not one video at
two lengths: this file asks why Ethereum exists at all and resolves into who
runs it; the Short takes only the governance half and asks its own question.
This file's YouTube title is a search query on a different angle from the
Short's curiosity hook.

**No financial advice** - this is design and governance history. No price, no
prediction, no platform rated. The outro asks one question and stops, after the
bare compliance line, which is on screen while it is spoken.

**Four statement cards in the whole video, and that is the point.** The first
cut put a big centred `payload` line on all twenty-five clips, because
`longform.md` had "every clip carries a payload line" as a hard rule. The user's
verdict was "we have too many titles after each other and the script is very
hard to follow". The rule was written to stop *generic stock playing silent
under a specific claim* - and the real fix for that is a picture that names the
noun, not a caption bolted onto a picture that does not. So a payload survives
here only where it **adds something the narration does not say**: the title
stamp, the name of an event the script deliberately does not pronounce, and the
compliance line the user requires on screen. Never two in a row.

**Kokoro respellings, spoken half only** (`es()`): `Ethereum` -> `Etheerium`;
`Vitalik Buterin` -> `Veetalik Booterin`; `went live` -> `went lyve` (Kokoro
reads it as the verb otherwise). Initialisms are avoided in speech - "a written
proposal", not EIP - and `The DAO` is on screen but never spoken.

**Pictures.** `P_WIDE` is the only landscape photograph of him and the only one
that may fill the 16:9 frame; the square and portrait crops are framed insets in
a beat's picture column, where a portrait source is a downscale by design.
`VIT_STUDIO` is the site's own second photo of him. The Ethereum and Ethereum
Classic marks are recoloured to the brand palette so the fork reads as gold
against pewter. See `assets/crypto/vitalik-buterin/CREDITS.md`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/vitalik-ethereum.py

Preflight the clip slots and runtime first:

    PYTHONPATH=. .venv/bin/python -m video_automation.longform.preflight \\
        projects/crypto-long/vitalik-ethereum.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

POSTS = SITE_IMAGES / "posts"
VIT = Path(__file__).resolve().parents[2] / "assets/crypto/vitalik-buterin"

A = 16 / 9


def es(caption: str) -> tuple[str, str] | str:
    """A `(caption, spoken)` pair when Kokoro needs a different spelling.

    Kokoro stresses `Ethereum` and the name wrong, and reads "went live" as the
    verb (`lɪv`, rhymes with "give") instead of the adjective (`laɪv`). Returns
    a bare string when nothing needs changing, so it is safe to wrap any chunk.
    """
    spoken = (caption.replace("Ethereum", "Etheerium")
                     .replace("Vitalik", "Veetalik")
                     .replace("Buterin", "Booterin")
                     .replace("went live", "went lyve"))
    return caption if spoken == caption else (caption, spoken)


# Pictures. Only P_WIDE is landscape and may fill the frame.
BITCOIN = VIT / "bitcoin-neon-wide.jpg"               # site photo, cropped to 16:9
P_WIDE = VIT / "vitalik-techcrunch-wide.jpg"          # 5760x3840 - full-frame
P_SQUARE = VIT / "vitalik-techcrunch-square.jpg"      # 3223x3597 - beat column only
P_FACE = VIT / "vitalik-techcrunch-portrait.jpg"      # 1670x2553 - beat column only
VIT_STUDIO = VIT / "vitalik-studio-blue.jpg"          # 1920x1080 - site photo
ETH_SLIDE = VIT / "ethereum-mark-slide.jpg"           # gold Ethereum mark, 16:9
ETH_MARK = VIT / "ethereum-mark-gold.jpg"             # gold Ethereum mark, square
ETC_SLIDE = VIT / "etc-mark-slide.jpg"                # pewter Ethereum Classic mark

# Stock, screened at 0.5/2/4/6/9/12s - max luma in the trailing comment. Shared
# with the Short (one video for the reuse rule); at most twice, five slots apart.
CODE_B = STOCK / "videos/programming-code-screen-dark/34160292.mp4"          # L17 sharp code
CODE_C = STOCK / "videos/programming-code-screen-dark/5495781.mp4"           # L31 hands on a laptop
TYPING = STOCK / "videos/hands-typing-keyboard-dark-close-up/34771078.mp4"   # L25 hands on a keyboard
WRITING = STOCK / "videos/adding-machine-vintage-dark/9569879.mp4"           # L38 writing at a desk
NET_WIRE = STOCK / "videos/digital-network-grid-gold-dark/28561594.mp4"      # L5  wireframe mesh
NET_FLOW = STOCK / "videos/abstract-flowing-data-network-dark-blue/28561463.mp4"  # L10 dot wave
NET_SPARK = STOCK / "videos/digital-network-grid-gold-dark/34645139.mp4"     # L32 light points
CIRCUIT = STOCK / "videos/circuit-board-glowing-traces-dark/2792370.mp4"     # L11 circuit + chip
ROADS = STOCK / "videos/diverging-roads-highway-night/15510172.mp4"         # L15 split highway
GOLD_A = STOCK / "videos/abstract-gold-particles-floating-dark/8551791.mp4"  # L15 gold bokeh
GOLD_B = STOCK / "videos/golden-dust-particles-black-background/10296171.mp4"  # L17 gold dust
STAGE_A = STOCK / "videos/empty-conference-stage-dark/7985880.mp4"          # L12 empty seating
STAGE_B = STOCK / "videos/empty-conference-stage-dark/7988176.mp4"          # L13 empty seating
GEARS = STOCK / "videos/clockwork-gears-dark/6867665.mp4"                    # L18 watch movement
POWER = STOCK / "videos/power-plant-cooling-towers-night/6216703.mp4"        # L26 plant at night
CROWD = STOCK / "videos/people-walking-street-silhouette-dark/35186847.mp4"  # L35 figures, underpass
CROWD_LIGHTS = STOCK / "videos/audience-raising-hands-auditorium-dark/36499729.mp4"  # L33 arena
LEDGER = STOCK / "videos/blockchain-blocks-chain-digital-dark/34127877.mp4"  # L15 dot sphere

ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "otis"                  # male, am_puck on the ENERGETIC chain. Candidate.

URL = "https://thecrypto.wiki/crypto-ogs/vitalik-buterin"


SECTIONS = [
    # --- the hook, first thirty seconds. No card. --------------------------
    #
    # The picture names the noun in every slot: Bitcoin, then him, then the desk
    # he wrote from, then the ledger, then the network. Only two payloads, and
    # the second is the title stamp.
    Section(
        title="It started as a complaint about Bitcoin",
        card=False,
        sentences=[
            (es("Ethereum started"),
             "as a complaint about Bitcoin."),
            (es("The complaint came from Vitalik Buterin."),
             "He was nineteen."),
            ("At seventeen he had co-founded Bitcoin Magazine,",
             "and he had been writing about the technology ever since."),
            ("Bitcoin was built to move money.",
             "That was the only job it was ever given."),
            ("Vitalik wanted something wider.",
             "A blockchain that could run any program you could write."),
            ("He wrote the idea up",
             "and took it to the developers who maintain Bitcoin.",
             "They turned him down."),
            ("So in twenty thirteen,",
             "he went and built his own."),
            ("Stay to the end,",
             es("and you will know who actually decides what Ethereum does.")),
        ],
        shots=[
            # The site's own Bitcoin photograph - a man looking at the symbol.
            Shot(image=BITCOIN, zoom=1.07, pan=(0.02, -0.01), aspect=A, bias=0.45),
            Shot(image=P_WIDE, zoom=1.06, pan=(0.02, -0.01), aspect=A, bias=0.20),
            Shot(clip=WRITING, clip_at=2.0),
            Shot(clip=LEDGER, clip_at=1.0),
            # payload 1 of 4 - the mesh cannot say this and the claim is the hook.
            Shot(clip=NET_WIRE, clip_at=1.0,
                 payload=("", "A blockchain that could run any program")),
            Shot(clip=STAGE_B, clip_at=1.0),
            # payload 2 of 4 - the title stamp, ~18s in.
            Shot(clip=CODE_B, clip_at=1.0,
                 payload=("", "WHY ETHEREUM WAS CREATED")),
            Shot(clip=NET_FLOW, clip_at=1.0),
        ],
        gaps=[0.45, 0.55, 0.60, 0.70, 0.60, 0.85, 0.80, 0.85],
    ),

    # --- reframe: the calculator and the computer -----------------------
    #
    # No payloads at all. The `compare` and the `quote` carry the argument, and
    # every clip between them names its own noun.
    Section(
        title="A calculator, or a computer?",
        spoken_title="So what was actually missing from Bitcoin?",
        sentences=[
            ("Think of Bitcoin as a pocket calculator.",
             "It does one job, and it does it extremely well."),
            ("It moves money from one person to another.",
             "Ask it to do anything else, and it cannot."),
            # compare: name_columns=True. 2 headings + 3 + 3 = 8 caption chunks,
            # in column order, nothing else inside the span.
            ("On Bitcoin.",
             "Send coins.",
             "Lock them with simple rules.",
             "That is close to the whole list.",
             es("On Ethereum."),
             "Run any program you can write.",
             "Store data that stays forever.",
             "Let apps build on other apps."),
            ("Vitalik wanted the opposite of a calculator.",
             "He wanted a blank computer",
             "that anyone on earth could program."),
            ("You write a program and upload it to the network.",
             "Every machine on that network runs it",
             "and they all agree on the answer."),
            ("Those programs are called smart contracts.",
             "Code that runs exactly as written,",
             "and that nobody can stop once it is running."),
            # quote beat - his own line, with his face beside it.
            (es("Vitalik put it simply."),
             es("If Bitcoin is a calculator, Ethereum is a smartphone.")),
        ],
        shots=[
            Shot(clip=GEARS, clip_at=1.0),
            Shot(clip=LEDGER, clip_at=6.0),
            Shot(graphic="compare",
                 payload=("ON BITCOIN",
                          ["Send coins",
                           "Lock with simple rules",
                           "Close to the whole list"],
                          "ON ETHEREUM",
                          ["Run any program",
                           "Store data forever",
                           "Apps build on apps"],
                          True)),
            Shot(image=VIT_STUDIO, zoom=1.06, pan=(-0.02, 0.01), aspect=A, bias=0.35),
            Shot(clip=CIRCUIT, clip_at=1.0),
            Shot(clip=CODE_C, clip_at=1.0),
            Shot(graphic="quote",
                 payload=("If Bitcoin is a calculator, Ethereum is a smartphone.",
                          "Vitalik Buterin"),
                 picture=P_SQUARE),
        ],
        gaps=[0.45, 0.60, 0.50, 0.60, 0.55, 0.75, 0.85],
    ),

    # --- deep dive: what the world computer unlocked -------------------
    Section(
        title="So what did that make possible?",
        sentences=[
            (es("Ethereum went live in twenty fifteen."),
             "Eight founders, a public crowd sale,",
             "and a working network."),
            ("Now anyone could write code that held real money.",
             "People built things Bitcoin never could."),
            # grid: 4 cards, one caption per card.
            ("Lending and trading with no bank in the middle.",
             "Tokens that stand in for art or property.",
             "Coins pegged to the value of a dollar.",
             "Groups voting on a shared budget in the open."),
            ("Some of it worked.",
             "Some of it collapsed.",
             "And almost all of it was copied onto every blockchain that came after."),
            ("But the shape was set.",
             "A base layer that does not care what you build on top of it."),
        ],
        shots=[
            # the mark itself, under the line that says the network went live.
            Shot(image=ETH_SLIDE, zoom=1.04, pan=(0.01, 0.0), aspect=A, bias=0.5),
            Shot(clip=TYPING, clip_at=1.0),
            Shot(graphic="grid",
                 payload=([("Lending & trading", "no bank in the middle"),
                           ("Ownership tokens", "art, property, a ticket"),
                           ("Stablecoins", "pegged to a dollar"),
                           ("Shared budgets", "voted on in the open")],
                          "BUILT ON THE WORLD COMPUTER")),
            Shot(clip=GOLD_A, clip_at=1.0),
            Shot(clip=NET_SPARK, clip_at=1.0),
        ],
        gaps=[0.55, 0.60, 0.45, 0.70, 0.85],
    ),

    # --- the twist: no company, no chief executive --------------------
    Section(
        title="So who is in charge?",
        sentences=[
            ("Here is where Ethereum stops behaving",
             "like a normal technology company."),
            (es("There is no Ethereum company."),
             "There is no chief executive.",
             es("Vitalik has never held that title.")),
            (es("There is a non-profit called the Ethereum Foundation."),
             "It pays for research and it runs events."),
            ("It cannot change the network.",
             "It cannot freeze your account, reverse your payment,",
             "or switch anything off."),
            # stat, with his face in the picture column - the note names him.
            ("Ask how many people can override Ethereum on their own,",
             "and the honest answer is a round number."),
            ("So if nobody is in charge,",
             "how does anything ever change?"),
        ],
        shots=[
            Shot(clip=STAGE_A, clip_at=1.0),
            Shot(image=P_WIDE, zoom=1.11, pan=(-0.03, 0.02), aspect=A, bias=0.30),
            Shot(clip=CROWD, clip_at=1.0),
            Shot(clip=GEARS, clip_at=6.0),
            Shot(graphic="stat",
                 payload=("0", "PEOPLE WHO CAN OVERRIDE IT",
                          "Vitalik Buterin included.", False),
                 picture=P_FACE),
            Shot(clip=NET_FLOW, clip_at=8.0),
        ],
        gaps=[0.55, 0.75, 0.60, 0.70, 1.10, 0.85],
    ),

    # --- the mirror: how a change actually ships ----------------------
    Section(
        title="How does a change actually happen?",
        sentences=[
            (es("Every change to Ethereum starts as a written proposal."),
             "Anyone can write one."),
            # steps: 5 nodes, one caption per node.
            ("Someone writes the proposal.",
             "Developers argue it out in the open.",
             "Independent teams build it into their software.",
             "The people running the network choose to upgrade.",
             "If enough of them do, it is live."),
            ("Nobody signs it off.",
             "It ships when enough people decide to run it."),
            (es("In twenty twenty-two, Ethereum replaced its entire engine this way."),
             "They called it the Merge.",
             "Mining was switched off overnight."),
            ("Only once has the community forced a change by hand.",
             es("In twenty sixteen, a project on Ethereum was drained of millions,"),
             "and most of the network voted to rewind it."),
            ("The minority refused.",
             "They kept the original chain running,",
             es("and it still exists today, as Ethereum Classic.")),
        ],
        shots=[
            Shot(clip=CODE_B, clip_at=5.0),
            Shot(graphic="steps",
                 payload=(["Someone writes a proposal",
                           "Developers argue in the open",
                           "Independent teams build it in",
                           "Operators choose to upgrade",
                           "Enough upgrade, it is live"],
                          "HOW A CHANGE SHIPS")),
            Shot(clip=CROWD_LIGHTS, clip_at=1.0),
            Shot(clip=POWER, clip_at=1.0),
            # payload 3 of 4 - the on-screen name the narration deliberately
            # never pronounces ("DAO" phonemizes as "dow").
            Shot(clip=CODE_C, clip_at=8.0,
                 payload=("", "2016 - the DAO hack")),
            # the other chain, in pewter against the gold mark earlier.
            Shot(image=ETC_SLIDE, zoom=1.04, pan=(-0.01, 0.0), aspect=A, bias=0.5),
        ],
        gaps=[0.55, 0.45, 0.70, 0.60, 0.80, 0.90],
    ),

    # --- echo, and the ask. No "below", no "subscribe". ---------------
    Section(
        title="So what did he actually build?",
        sentences=[
            ("Go back to the nineteen-year-old",
             "who wanted to change Bitcoin."),
            ("He did not just want software that could run anything.",
             "He wanted a network that nobody could run."),
            ("Both halves are the same idea.",
             "General purpose, all the way down."),
            (es("It makes Ethereum very hard to shut down."),
             "It also makes it slow to agree, and hard to fix."),
            ("Nothing in this video is financial advice.",),
            ("So, here is the question.",),
            ("If nobody is in charge,",
             "who do you hold responsible when it breaks?"),
        ],
        shots=[
            Shot(image=VIT_STUDIO, zoom=1.08, pan=(0.02, -0.01), aspect=A, bias=0.35),
            Shot(clip=ROADS, clip_at=1.0),
            Shot(image=ETH_MARK, zoom=1.05, pan=(0.01, 0.0), aspect=A, bias=0.5),
            Shot(clip=CIRCUIT, clip_at=1.0),
            # payload 4 of 4 - the compliance line is on screen while it is
            # spoken, over a quiet clip. The user's standing rule.
            Shot(clip=GOLD_A, clip_at=8.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=NET_SPARK, clip_at=8.0),
            # the outro stays uncluttered for the end-screen cards.
            Shot(clip=GOLD_B, clip_at=1.0),
        ],
        gaps=[0.45, 0.60, 0.70, 0.70, 0.60, 0.45, 2.40],
    ),
]

META = Meta(
    title="Why Was Ethereum Created?",
    hook="A 19-year-old wanted Bitcoin to run any program. The Bitcoin "
         "developers turned him down, so he built his own network - and then "
         "built it so nobody, himself included, controls it.",
    url=URL,
    summary="Vitalik Buterin proposed Ethereum in 2013 after Bitcoin's "
            "developers turned down his idea for a fully programmable "
            "blockchain. What that design bought, why Ethereum has no company "
            "or CEO, and how a change to the network actually ships.",
    tags=["vitalik buterin", "ethereum", "what is ethereum",
          "why was ethereum created", "smart contracts", "ethereum classic",
          "who controls ethereum"],
    cta=f"Full profile, quick facts and sources: {URL}",
    credits=["Photographs of Vitalik Buterin by John Phillips / TechCrunch, "
             "CC BY 2.0, via Wikimedia Commons (TechCrunch Disrupt London "
             "2015).",
             "Ethereum mark by the Ethereum Foundation, CC BY 3.0, via "
             "Wikimedia Commons (recoloured). Ethereum Classic mark: CC0.",
             "Additional footage: Pexels (Pexels licence, no attribution "
             "required).",
             "Music: night-drift, licensed for this channel.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-vitalik-ethereum-long.mp4"
    work = Path.home() / "Desktop/.crypto-vitalik-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=music.track("night-drift"),
        callouts=None,
        thumb_headline="He built it. He can't [control] it.",
        thumb_image=P_WIDE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
