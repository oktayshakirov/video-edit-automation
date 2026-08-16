"""The two-dollar part that starts fires. ~45s crypto short.

Source: crypto-wiki/content/posts/how-to-build-a-mining-rig.mdx, the same post
as the `crypto-mining-rig-long` explainer.

**It deliberately does not reuse the long form's angle.** That video is built on
the electricity price, which is the honest answer to "should you build one" and
needs three minutes to pay off — a spare-room rig against an industrial farm,
four variables, a calculator. None of that survives compression to forty
seconds, and a short that opens on "your power bill decides this" is a short
nobody stops for.

The article's other strong idea is perfect short material instead: **the
component that burns houses down is the cheapest thing on the list.** It is
concrete, it is genuinely counterintuitive — the danger is not the
two-thousand-dollar cards — it is safety information rather than financial
advice, and it resolves inside one beat. The two videos now complement each
other rather than repeating; a viewer who sees both gets the economics and the
hazard, not the same script twice.

**Rebuilt on motion after review.** The first cut was eight site photographs
and a checklist, and the user's verdict was that it looked boring and not
engaging. It was: eight Ken Burns pushes in a row is one move repeated eight
times, and the site owns no photograph of a riser, an adapter or a graphics
card, so the pictures were also generic. Half the shots are stock clips now and
the piece opens on one — motion on frame one, which is the long-form rule
arriving in 9:16 where it matters more, not less, because a Short is judged in
its first second.

The site's own hero still carries the line about doing the wiring properly, and
the checklist still carries the argument. **Stock supports; it does not lead.**

**`proof-of-work.jpg` is not used**, though it is the most on-topic file in the
library at 1000px. It is an infographic, and a 9:16 crop takes its title off the
top and its last row off the bottom exactly as the long-form cut did before the
rule landed. A diagram cannot take a crop.

**Nothing here is financial advice, and this angle cannot become it** — it is a
wiring warning. The claim is the article's own, stated twice and in bold: power
risers directly from the supply, never through a drive-connector adapter.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto/mining-rig.py
"""

from pathlib import Path

from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot

POSTS = SITE_IMAGES / "posts"

# Screened across their length, not at one second — the trailing comment is the
# luma/saturation range over the whole clip. Cached from the long-form build.
RIG = STOCK / "videos/computer-cooling-fan-dark/33356261.mp4"        # L35-51
BOARD = STOCK / "videos/motherboard-computer-close-up-dark/6754818.mp4"  # L37-39
CIRCUIT = STOCK / "videos/circuit-board-macro-dark/6755170.mp4"      # L39-59
CARDS = STOCK / "photos/graphics-card-gpu-dark/8622912.jpg"          # L27 S4

VOICE = "mia"                   # female, af_heart. Matches the long form from
                                # the same post. Still a candidate, not approved.

# One tuple per sentence; each string is one caption. The checklist beat must
# have exactly one caption per item — that is what times its reveals.
SENTENCES = [
    ("The part of a mining rig",
     "that burns houses down",
     "costs about two dollars."),

    ("Everyone worries about the graphics cards.",
     "They cost the most,",
     "so they get all the attention."),

    # The beat. Three items, and the one nobody suspects is the one ticked.
    ("The graphics cards.",
     "The power supply.",
     "A two-dollar adapter."),

    ("Every card sits on a riser,",
     "and every riser",
     "needs its own power."),

    ("There is a cheap adapter that takes it",
     "from the drive connector instead.",
     "It fits. It works.",
     "It is a known fire hazard."),

    ("Those connectors were built for a hard drive,",
     "not a card pulling",
     "seventy-five watts."),

    ("Run a six-pin cable",
     "from the power supply",
     "to every riser. Directly."),

    ("Would you have caught that",
     "before switching it on?"),
]

SHOTS = [
    # 1 — **motion on frame one.** A Short is judged in its first second and the
    # first cut spent that second on a slow push across a still. Orange-lit rig
    # internals, already moving before the voice starts.
    Shot(clip=RIG, clip_at=1.0),

    # 2 — two graphics cards on black. The site owns no picture of a graphics
    # card, which is the whole reason the stock rule had to change here.
    Shot(image=CARDS, zoom=1.12, pan=(-0.03, 0.02), aspect=1.15, bias=0.45),

    # 3 — the drawn beat, over the green server room dimmed to 0.5. Still the
    # argument, and still the only place the piece stops moving on purpose.
    Shot(graphic="checklist",
         payload=([("The graphics cards", False),
                   ("The power supply", False),
                   ("A $2 riser adapter", True)],
                  "WHAT ACTUALLY STARTS FIRES"),
         backdrop=POSTS / "data-center.jpg"),

    # 4 — a board macro under the line about risers and their power.
    Shot(clip=BOARD, clip_at=2.0),

    # 5 — circuit macro for the adapter and the hazard. Motion under the
    # longest sentence in the piece, which is where a still sags worst.
    Shot(clip=CIRCUIT),

    # 6 — a glowing core inside a dark lattice, for the watts. **Not
    # `industrial.jpg`**, which was the first choice and is a daylight sky full
    # of white cloud: it measured L149 and was the only bright rectangle in a
    # gold-on-near-black piece, and cooling towers read as power *generation*
    # rather than as what a single card draws. This one is L59 and its amber
    # sits with the palette. `aspect=1.05` because the source is the flattest in
    # the set at 800x448, and cropping it toward 1.15 would narrow it past the
    # point `MAX_UPSCALE` can carry.
    Shot(image=POSTS / "quantum-computing.png",
         zoom=1.12, pan=(0.03, -0.01), aspect=1.05, bias=0.45),

    # 7 — the article's own hero, on the line about doing the wiring properly.
    # The site's picture carries the instruction; the stock carries the texture.
    Shot(image=POSTS / "mining-rig.jpg",
         zoom=1.12, pan=(0.02, -0.02), aspect=1.15, bias=0.30),

    # 8 — back to the opening clip at a different moment, so the return reads
    # as a return and the piece ends moving rather than on a held still.
    Shot(clip=RIG, clip_at=8.0),
]


EMOJI = {
    "It is a known fire hazard.": "🔥",
    "before switching it on?": "👇",
}

# The checklist (index 2) buys its pause: three options sit unmarked, the voice
# stops, and cross-cross-tick lands in the silence. Everything else stays tight.
GAPS = [0.34, 0.34, 2.10, 0.34, 0.34, 0.34, 0.34, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-mining-rig-short.mp4"
    work = Path.home() / "Desktop/.crypto-mining-rig-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS)
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
