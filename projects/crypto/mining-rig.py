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

    # **The question goes here, not inside the beat.** A checklist times its
    # reveals off the caption starts of its own sentence, so a lead-in line
    # inside that span eats reveal zero and shunts every item one line late.
    # Asking it at the end of the sentence before costs nothing and gives the
    # list something to be an answer to.
    ("Everyone worries about the graphics cards.",
     "They cost the most.",
     "So what actually starts the fire?"),

    # The beat, and **the narration now reads the items as they appear** —
    # which is why it is `flow`. When the voice is already saying "not the
    # graphics cards", holding the cross back for the pause puts the picture
    # four seconds behind the word that earned it.
    ("Not the graphics cards.",
     "Not the power supply.",
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

    # A `steps` beat: this is a procedure, and order is the one thing neither
    # a photograph nor a checklist can show.
    ("A six-pin cable straight from the supply.",
     "One for every riser.",
     "Never through an adapter."),

    # **The close.** The old ending asked "would you have caught that before
    # switching it on?", which the user found confusing — fairly: "that" has
    # three possible referents by then, and the question asks the viewer to
    # audit a build they have not made. This lands the rule instead, echoing
    # the opening line's own arithmetic, and asks for the one engagement a
    # how-to short can honestly earn. A save is also a stronger signal than a
    # comment on this kind of video, and unlike "what do you think?" it is
    # something the viewer actually has a reason to do.
    ("Cheap adapter,",
     "expensive mistake."),

    ("Save this before you build one.",),
]

SHOTS = [
    # 1 — **motion on frame one.** A Short is judged in its first second and the
    # first cut spent that second on a slow push across a still. Orange-lit rig
    # internals, already moving before the voice starts.
    Shot(clip=RIG, clip_at=1.0),

    # 2 — two graphics cards on black. The site owns no picture of a graphics
    # card, which is the whole reason the stock rule had to change here.
    Shot(image=CARDS, zoom=1.12, pan=(-0.03, 0.02), aspect=1.15, bias=0.45),

    # 3 — the judged list, flowing with the voice.
    Shot(graphic="checklist",
         payload=([("The graphics cards", False),
                   ("The power supply", False),
                   ("A $2 riser adapter", True)],
                  "WHAT ACTUALLY STARTS FIRES",
                  True),                            # flow
         backdrop=POSTS / "data-center.jpg"),

    # 4 — a board macro under the line about risers and their power.
    Shot(clip=BOARD, clip_at=2.0),

    # 5 — circuit macro for the adapter and the hazard. Motion under the
    # longest sentence in the piece, which is where a still sags worst.
    Shot(clip=CIRCUIT),

    # 6 — the article's own hero, and the only picture in the library of
    # anybody handling hardware. It earns its place on the line about what
    # those connectors were actually built for.
    Shot(image=POSTS / "mining-rig.jpg",
         zoom=1.12, pan=(0.02, -0.02), aspect=1.15, bias=0.30),

    # 7 — the fix, as a vertical `steps` track. A second drawn beat with a
    # completely different silhouette from the checklist, which is the whole
    # point: two lists in one short would read as the same graphic twice.
    Shot(graphic="steps",
         payload=(["Six-pin cable from the supply",
                   "One for every riser",
                   "Never through an adapter"],
                  "DO IT THIS WAY"),
         backdrop=POSTS / "digital-technology.jpg"),

    # 8 — back to the opening clip at a different moment, so the return reads
    # as a return and the piece ends moving rather than on a held still.
    Shot(clip=RIG, clip_at=8.0),

    # 9 — the ask, held on the same footage running on.
    Shot(clip=RIG, clip_at=11.0),
]


EMOJI = {
    "It is a known fire hazard.": "🔥",
    "Save this before you build one.": "🔖",
}

# The checklist (index 2) no longer needs its long pause: `flow` lands each
# verdict on the word that earns it, so the 2.10s that used to buy room for the
# marks would now just be dead air. It keeps 1.20 so the finished list sits for
# a moment before the cut. The `steps` beat (index 6) takes 0.90 for the same
# reason — a beat whose sentence is short is gone in under two seconds.
GAPS = [0.34, 0.34, 1.20, 0.34, 0.34, 0.34, 0.90, 0.34, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-mining-rig-short.mp4"
    work = Path.home() / "Desktop/.crypto-mining-rig-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS)
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
