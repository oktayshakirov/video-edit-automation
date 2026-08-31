"""Quantum computers vs. crypto — ~50s crypto short.

Source: crypto-wiki/content/posts/quantum-computers-and-crypto.mdx, the same
post as the `quantum-crypto` long-form explainer.

**It does the single move the long form spends three chapters on.** That video
walks the whole picture. Fifty seconds cannot, so this one does only the
concrete swap: on most chains your address is a hash of your public key, so the
key stays hidden while a coin just sits there - and the first time you spend,
the signature publishes it onto a record with no delete. Everything else is left
out rather than compressed.

**It opens by asking its own title question** - "Could a quantum computer steal
your Bitcoin?" - because a Short has no title card, no thumbnail on screen and
no chapter list.

**Say "quantum computers", not "quantum"** - the user flagged bare "quantum" as
a noun as confusing.

**One drawn beat**, a `checklist` (flow=True, each line carries its verdict) -
not the `steps` / `compare` shapes the long form uses for the same content.

**No financial advice.** Mechanism only. The close asks whether the viewer is
worried and what they do to stay safe - a comment prompt, not a call.

**Every asset is fresh and shared only with this post's long form.**

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/quantum-crypto.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.thumb import render_short_thumb

PH = STOCK / "photos"

# Fresh, shared only with this post's long form.
PALM = STOCK / "videos/fingerprint-biometric-scan-dark/16392048.mp4"            # 17.0s L25 S8
RACKS = STOCK / "videos/supercomputer-racks-blinking-lights-dark/12138721.mp4"   # 18.0s L14 S11
CODE = STOCK / "videos/code-scrolling-screen-terminal-dark/34268861.mp4"        # 18.0s L16 S14
TUNNEL = STOCK / "videos/digital-tunnel-data-stream-dark/33113400.mp4"          # 20.0s L12 S0
CLOCK = STOCK / "videos/clock-ticking-dark-macro/29527767.mp4"                  # 10.0s L7 S3
LEDGER = STOCK / "videos/digital-ledger-blocks-chain-dark/34128900.mp4"         # 20.0s L18 S10
FIELD = STOCK / "videos/abstract-digital-data-particles-dark/34645139.mp4"      # 20.0s L29 S0

CRYO = PH / "cryostat-quantum-computer/30547566.jpg"          # 8192x4320 L22 S11
DESK = PH / "code-on-screen-dark/5380603.jpg"                 # 6000x4000 L22 S3
CIRCUIT = PH / "encryption-padlock-circuit-dark/3520697.jpg"  # 6016x4000 L16 S0
MAGFIELD = PH / "magnetic-field-lines/38032287.jpg"          # 3840x2160 L34 S36 — thumbnail, matches the long form

VOICE = "mia"
MUSIC = music.track("night-drift")

# One tuple per sentence; each string is one caption. The checklist beat must
# have exactly one caption per item - that is what times its reveals.
SENTENCES = [
    ("Could a quantum computer",
     "steal your Bitcoin?"),

    ("Not the whole blockchain.",
     "Just your key."),

    ("Your address is not your public key.",
     "It is a hash of it."),

    ("While a coin only sits in an address,",
     "the key behind it stays hidden."),

    ("The moment you spend,",
     "your signature publishes that key.",
     "Onto a record with no delete."),

    # The question goes here, not inside the beat.
    ("So which of your addresses is exposed?",),

    # The beat: three, each line carries its own verdict -> flow=True.
    ("Never spent from - the key is hidden.",
     "Spent once - the key is public.",
     "Reused - public, and easy to find."),

    ("A quantum computer can't use that yet.",
     "Maybe a decade out. Maybe more."),

    ("But a blockchain never forgets.",
     "Copy the key now, crack it later."),

    ("It comes down to one thing.",),

    # Full-screen statement. `build` suppresses captions on any shot with a
    # graphic, so the card is capitals while the voice reads a sentence.
    (("THE CHAIN HOLDS. YOUR KEY IS THE TARGET.",
      "The chain itself holds. Your key is what quantum computers are aiming at."),),

    ("So, are you worried about quantum computers yet?",
     "What do you do to keep your crypto safe?"),
]

SHOTS = [
    # Open on the hand - a Short is judged in its first second.
    Shot(clip=PALM, clip_at=1.0),

    Shot(image=CRYO, zoom=1.11, pan=(0.02, -0.02), aspect=1.15, bias=0.4),

    Shot(clip=LEDGER, clip_at=1.0),

    Shot(clip=RACKS, clip_at=1.0),

    Shot(clip=CODE, clip_at=1.0),

    Shot(image=DESK, zoom=1.12, pan=(0.02, 0.02), aspect=1.15, bias=0.45),

    # The beat. Tick = still hidden, cross = exposed.
    Shot(graphic="checklist",
         payload=([("Never spent from", True),
                   ("Spent at least once", False),
                   ("Reused for change", False)],
                  "IS THE KEY STILL HIDDEN?",
                  True),                             # flow
         ),

    Shot(clip=CLOCK, clip_at=0.5),

    Shot(clip=TUNNEL, clip_at=1.0),

    Shot(image=CIRCUIT, zoom=1.12, pan=(-0.02, -0.02), aspect=1.15, bias=0.5),

    # The line, full screen.
    Shot(graphic="chapter",
         payload=("THE CHAIN HOLDS. YOUR KEY IS THE TARGET.",)),

    # The ask, on the abstract - an outro wants an uncluttered frame.
    Shot(clip=FIELD, clip_at=1.0),
]

EMOJI = {
    "Just your key.": "\U0001F511",                  # key
    "What do you do to keep your crypto safe?": "\U0001F447",  # down arrow
}

# 0.34 inside a thought, 0.55-0.90 at the end of one. The checklist (index 6)
# is flow=True, so it needs a shorter gap than a two-phase beat - the marks
# land on the words. The statement card (index 10) takes 1.15, because a line
# filling the screen has to be allowed to sit.
GAPS = [0.65, 0.55, 0.50, 0.55, 0.80, 1.30, 1.30, 0.70, 0.85, 0.55, 1.15, 0.40]


def main() -> None:
    out = Path.home() / "Desktop/quantum-crypto-short.mp4"
    work = Path.home() / "Desktop/.quantum-crypto-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS,
                                     music=MUSIC, music_gain=0.85)

    # One thumbnail: vertical, same source and headline as the long form.
    head = "Can quantum computers [break] Bitcoin?"
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO, head,
        image=MAGFIELD, accent="orange", band="bottom")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
