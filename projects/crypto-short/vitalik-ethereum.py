"""Who Is In Charge Of Ethereum? - ~48s crypto short.

Source: crypto-wiki/content/crypto-ogs/vitalik-buterin.mdx. Built as a pair with
`crypto-long/vitalik-ethereum.py`. The long form asks why Ethereum was created;
this one takes only the governance half and does the single move - the founder
cannot control his own creation, and nobody else can either.

Design and governance history, not financial advice: no price, no prediction,
no buy or sell. A Short carries no compliance line (the long form does). The
outro asks one question and stops.

**The picture matches the noun in the sentence, not the one after it.** The
first cut opened on his portrait while the voice said "Ethereum" and cut to the
Ethereum mark while the voice said his name - the user caught the inversion.
The mark now carries the question and the portrait carries his name.

**No emoji, deliberately.** `add_caption_emoji` re-centres the whole line around
the glyph, so a caption carrying one falls back to the single-PNG treatment and
**the per-word karaoke highlight stops on that line** - which the user saw at
0:08. Karaoke running unbroken is worth more here than two glyphs.

**Kokoro respellings, spoken half only** (`es()`): `Ethereum` -> `Etheerium`;
`Vitalik Buterin` -> `Veetalik Booterin`. `The DAO` is never spoken; the script
says "a hack".

**Voice: `otis`** (male, am_puck on the ENERGETIC chain), matching the long form.
The music bed is automatic - `render_crypto_short` defaults to `night-drift`.

**The opening portrait is shown whole.** `aspect` is set to the source's own
ratio (1670/2553 = 0.654), which makes `PhotoShot`'s crop a no-op, so the
photograph is letterboxed into the blurred fill rather than cut into. The user's
note was that it was cropped; the fix is the aspect, not the bias.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/vitalik-ethereum.py
"""

from pathlib import Path

from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.thumb import render_short_thumb

VIT = Path(__file__).resolve().parents[2] / "assets/crypto/vitalik-buterin"
POSTS = SITE_IMAGES / "posts"

P_FACE = VIT / "vitalik-techcrunch-portrait.jpg"     # 1670x2553
P_SQUARE = VIT / "vitalik-techcrunch-square.jpg"     # 3223x3597
ETH_MARK = VIT / "ethereum-mark-gold.jpg"            # gold Ethereum mark, square
ETC_MARK = VIT / "etc-mark-square.jpg"               # pewter Ethereum Classic mark

FACE_ASPECT = 1670 / 2553       # the source's own ratio - crop becomes a no-op


def es(caption: str) -> tuple[str, str] | str:
    """A `(caption, spoken)` pair when Kokoro needs a different spelling."""
    spoken = (caption.replace("Ethereum", "Etheerium")
                     .replace("Vitalik", "Veetalik")
                     .replace("Buterin", "Booterin")
                     .replace("went live", "went lyve"))
    return caption if spoken == caption else (caption, spoken)


# Stock, shared with the long form (one video for the reuse rule).
STAGE = STOCK / "videos/empty-conference-stage-dark/7988176.mp4"                   # L13 empty seating
NET_FLOW = STOCK / "videos/abstract-flowing-data-network-dark-blue/28561463.mp4"   # L10 dot wave
NET_SPARK = STOCK / "videos/digital-network-grid-gold-dark/34645139.mp4"           # L32 light points
TYPING = STOCK / "videos/hands-typing-keyboard-dark-close-up/34771078.mp4"         # L25 keyboard
ROADS = STOCK / "videos/diverging-roads-highway-night/15510172.mp4"               # L15 split highway
CROWD_LIGHTS = STOCK / "videos/audience-raising-hands-auditorium-dark/36499729.mp4"  # L33 arena

VOICE = "otis"                  # male, am_puck. Matches the long form.

# One tuple per sentence; each string is one caption. A chunk may be a
# (caption, spoken) pair. The checklist beat needs one caption per item.
SENTENCES = [
    # the title question, over the Ethereum mark - the noun the voice says.
    ("Who is actually in charge",
     es("of Ethereum?")),

    # his name, over his portrait.
    (es("Vitalik Buterin created it."),
     "He wrote the plan at nineteen.",
     "He is still its loudest voice."),

    ("But he holds no title.",
     es("There is no Ethereum company"),
     "for him to run."),

    # the hinge - its own sentence and its own shot, so the list is an answer
    # rather than a cold recital.
    (es("So what can Vitalik change about Ethereum by himself?"),),

    # checklist, two-phase. The title is the question the crosses answer, the
    # four items are the candidates, and the fifth chunk is the answer landing
    # in the pause. Every item struck, so no mark has to be interpreted.
    ("Rewrite the rules.",
     "Reverse a payment.",
     "Freeze your wallet.",
     "Shut the whole thing down.",
     "Not one of them."),

    ("So who does decide?",),

    ("Thousands of independent computers,",
     "each running software their owners chose."),

    (es("To change Ethereum,"),
     "you have to convince enough of them",
     "to run your version."),

    ("In twenty sixteen, most of them agreed to rewind a hack.",
     "Some refused."),

    # the other chain, named over its own mark.
    ("They kept the original chain running.",
     es("You can still use it today. It is called Ethereum Classic.")),

    # the closing card. "No one person runs it" read badly; this is the plain
    # sentence, and it answers the opening question in the same words.
    (("NOBODY IS IN CHARGE",
      "So nobody is in charge."),),

    (es("So when Ethereum breaks -"),
     "who do you blame?"),
]

SHOTS = [
    # 1 - the Ethereum mark, under the question that names Ethereum.
    Shot(image=ETH_MARK, zoom=1.03, pan=(0.01, 0.0), aspect=1.05, bias=0.5),

    # 2 - him, shown whole: aspect is the source's own ratio, so nothing is cut.
    Shot(image=P_FACE, zoom=1.04, pan=(0.012, -0.012), aspect=FACE_ASPECT, bias=0.5),

    # 3 - an empty auditorium: no company, no chief executive.
    Shot(clip=STAGE, clip_at=1.0),

    # 4 - the hinge, back on him as the question is put.
    Shot(image=P_SQUARE, zoom=1.05, pan=(-0.02, 0.01), aspect=1.22, bias=0.16),

    # 5 - the checklist. Title is the question; all four struck.
    Shot(graphic="checklist",
         payload=([("Rewrite the rules", False),
                   ("Reverse a payment", False),
                   ("Freeze your wallet", False),
                   ("Shut the whole thing down", False)],
                  "CAN HE DO IT ALONE?")),

    # 6 - a flowing data network: so who does decide?
    Shot(clip=NET_FLOW, clip_at=1.0),

    # 7 - drifting points of light: thousands of independent machines.
    Shot(clip=NET_SPARK, clip_at=1.0),

    # 8 - hands on a keyboard: convincing them to run your version.
    Shot(clip=TYPING, clip_at=1.0),

    # 9 - a splitting highway at night: the 2016 fork.
    Shot(clip=ROADS, clip_at=1.0),

    # 10 - the Ethereum Classic mark, in pewter against the gold one at the top.
    Shot(image=ETC_MARK, zoom=1.03, pan=(0.01, 0.0), aspect=1.05, bias=0.5),

    # 11 - the full-screen statement card.
    Shot(graphic="chapter", payload=("NOBODY IS IN CHARGE",)),

    # 12 - the ask. An arena full of people is the answer to "who do you blame":
    # everyone running it, which is nobody in particular.
    Shot(clip=CROWD_LIGHTS, clip_at=8.0),
]

# No emoji - see the module docstring. An emoji caption loses its karaoke.
EMOJI: dict[str, str] = {}

# Silence after each sentence. The checklist (index 4) buys the long pause for
# its verdicts; the statement card (index 10) gets room to sit.
GAPS = [0.85, 0.55, 0.60, 0.55, 2.10, 0.70, 0.45, 0.55, 0.70, 0.80, 1.30, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-vitalik-ethereum-short.mp4"
    work = Path.home() / "Desktop/.crypto-vitalik-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS)

    # `size=126` keeps the headline inside the frame - 168 ran "ETHEREUM?" off
    # both edges. `band="bottom"` because his head is in the top half.
    thumb = render_short_thumb(
        Path.home() / "Desktop/crypto-vitalik-ethereum-short-thumb.jpg",
        CRYPTO, "Who [runs] Ethereum?",
        image=P_SQUARE, accent="yellow", band="bottom", size=126)
    print(f"{out}  {total:.2f}s")
    print(f"thumb: {thumb}")


if __name__ == "__main__":
    main()
