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

**Site images only.** The long-form cut reached for screened stock stills
because thirty shots against a library with no picture of mining hardware is not
survivable. Eight shots is, and the stock rule stands here as written: the
reversal in `video-crypto-long` is explicitly scoped to long form. It is worth
recording that the pressure is the same in kind and only smaller in degree — the
site owns no photograph of a riser, an adapter or a graphics card, so the two
drawn beats and the hero carry the argument, which is what they are for.

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

from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot

POSTS = SITE_IMAGES / "posts"

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
    # 1 — the article's own hero, and the only picture in the library of anybody
    # actually handling hardware. It opens and closes the piece.
    Shot(image=POSTS / "mining-rig.jpg",
         zoom=1.10, pan=(0.02, -0.02), aspect=1.15, bias=0.30),

    # 2 — people dwarfed by racks, for the line about where the attention goes.
    Shot(image=POSTS / "futuristic-data-center.jpg",
         zoom=1.13, pan=(-0.03, 0.02), aspect=1.15, bias=0.45),

    # 3 — the drawn beat, over the green server room dimmed to 0.5.
    Shot(graphic="checklist",
         payload=([("The graphics cards", False),
                   ("The power supply", False),
                   ("A $2 riser adapter", True)],
                  "WHAT ACTUALLY STARTS FIRES"),
         backdrop=POSTS / "data-center.jpg"),

    Shot(image=POSTS / "digital-technology.jpg",
         zoom=1.12, pan=(0.03, 0.02), aspect=1.15, bias=0.45),

    # 5 — the orange neon carries heat under "known fire hazard" without the
    # script having to show a fire, which would be both unavailable and lurid.
    Shot(image=POSTS / "bitcoin-neon.jpg",
         zoom=1.14, pan=(-0.02, -0.02), aspect=1.15, bias=0.50),

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

    Shot(image=POSTS / "data-center.jpg",
         zoom=1.13, pan=(-0.03, 0.01), aspect=1.15, bias=0.50),

    # 8 — back to the hero for the question, cropped differently so the return
    # reads as a return rather than as the same shot.
    Shot(image=POSTS / "mining-rig.jpg",
         zoom=1.14, pan=(-0.03, 0.01), aspect=1.15, bias=0.20),
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
