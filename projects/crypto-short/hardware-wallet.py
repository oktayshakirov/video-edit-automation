"""Can a thief take your crypto from your hardware wallet? ~38s crypto short.

Source: crypto-wiki/content/posts/what-is-a-hardware-wallet.mdx - the same
article as the `hardware-wallet` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks what the device
does, what it cannot stop and whether you need one. This does one move, in
the order a stranger would ask it: steal the device and you get nothing,
because the coins were never on it (the key is); but the key can still be
reached without touching the device - by the owner's own button, and, in
2026, by a firmware bug (Coldcard). The close loops to the opening thief.

**Opener: `Stamp`**, shared with the long form (`shorts.md`, "A pair may
share its opener"): MY CRYPTO IS ON THE DEVICE, stamped NEVER WAS on
"never" in sentence 2. Sentence 1 is the title question at 12 words, so
sentence 2 starts near 4s (`shorts.md`, "The first eight seconds").

**Pictures:** a flashlight searching a dark room (the thief - a clip, never
a still, to open); the real Coldcard from Commons, framed and named; a
`grid` for what is on the device; `blindsign` for the button pressed on a
scammer's request; `breach` for the Coldcard drain, with 0 DEVICES TOUCHED as its
third reveal. Two stock clips of six shots; no `pile` and no
`behind` (both were in the pair before this one).

**E17: 30-40s.** **Close: a plain last sentence, no `outro=` card**, on the
clip the Short opened on. **No disclaimer** (the long form carries it).

    PYTHONPATH=. .venv/bin/python projects/crypto-short/hardware-wallet.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp

SOURCE_POST = "what-is-a-hardware-wallet"
DEMAND = ("Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' "
          "16.3x (330k); VirtualBacon 'Do you need a Crypto Hardware "
          "Wallet?' Short 220k")
# The cover's style, for the review to compare views and clicks by
# (`thumbnails.md`, "Cover styles are a choice, and every video says which").
COVER_STYLE = "arrow"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
HW = ROOT / "assets/crypto/hardware-wallet"
BEATGROUND = ROOT / "assets/brand/beat-ground-crypto.jpg"

# The long form's roster - screened there, see its header.
BURGLAR = V / "burglar-flashlight-dark-room/18449083.mp4"   # a flashlight searching a dark room - the thief
COLDCARD_DARK = HW / "coldcard-dark.jpg"                    # a Coldcard lit on black

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, 12 words with the stake in it.
    ("If someone stole your hardware wallet tonight, could they take your crypto?",),

    # Partial answer: not the device - the Stamp lands NEVER WAS on "never".
    # The next question (then what is on it?) is already open.
    ("Not from the device. Your coins were never on it.",),

    # The grid's own sentence: one chunk per card.
    ("It holds the key that signs for them, on a chip that never goes online.",
     "Without your PIN, a thief holds a locked box."),

    # The turn - the blindsign's own sentence: card, approval, truth.
    ("But a scammer's request looks like a normal send.",
     "You press the button.",
     "And the device signs it, perfectly."),

        # The breach's third reveal is the line under the verdict.
    ("In 2026, a firmware bug made some Coldcard keys guessable.",
     "About eighteen hundred bitcoin were drained.",
     "Nobody touched a single device."),

    # The close loops to the thief the Short opened on.
    ("So the thief to worry about never needs your wallet.",),
]

SHOTS = [
    # Lit from 3s, and off the person's legs that fill it after ~9s.
    Shot(clip=BURGLAR, clip_at=3.5),
    # The real device, framed and named - not a second full-frame picture.
    Shot(image=COLDCARD_DARK, aspect=0.75, zoom=1.05,
         window=("player", "A Coldcard hardware wallet")),
    Shot(graphic="grid", backdrop=BEATGROUND,
         payload=([("The key", "on a chip that never goes online", "\U0001F511"),
                   ("No PIN", "a thief holds a locked box", "\U0001F512")],
                  "WHAT IS ON THE DEVICE")),
    Shot(graphic="blindsign", backdrop=BEATGROUND,
         payload=([("Action", "Send"),
                   ("To", "Your saved address"),
                   ("Fee", "A few cents")],
                  [("Action", "Approve spending"),
                   ("Spender", "Their contract"),
                   ("Limit", "Unlimited")],
                  ["YOU"], "ONE BUTTON")),
    Shot(graphic="breach", backdrop=BEATGROUND,
         payload=("5,200+ ADDRESSES", 1816, "BTC", 4, "COLDCARD, 2026",
                  "DRAINED", "1 square = 25 addresses", "0 devices touched")),
    # The opening clip, a second earlier: from 3.5s the person's legs come
    # in on the last frame, which is the frame the loop shows.
    Shot(clip=BURGLAR, clip_at=2.5),
]

GAPS = [0.80, 0.70, 0.90, 1.90, 1.50, 1.20]

HEADLINE = "Can a [thief]\ntake it?"


# The cover only (`thumbnails.md`, "The cover's picture stays on the
# cover"): the long form's cover picture, a Ledger on its cable.
LEDGER_CABLE = HW / "ledger-cable.jpg"


def thumbs(out: Path) -> Path:
    """The 9:16 cover, the long form's picture (a pair shares one): the
    Ledger on its cable in the lower frame, its lit "Bitcoin" screen ringed
    in red, the Short's question on the black above and an arrow down from
    it to the screen."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(LEDGER_CABLE).convert("RGB")
    w, h = src.size
    crop = src.crop((int(w * 0.22), 0, int(w * 0.92), h))
    pic = crop.resize((1080, int(crop.height * 1080 / crop.width)), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (0, 0, 0))
    y = 1920 - pic.height
    im.paste(pic, (0, y))
    a = np.zeros((1920, 1), np.float32)
    a[:y + 260, 0] = 1.0
    a[y:y + 260, 0] = np.linspace(1.0, 0.0, 260)
    mask = Image.fromarray((np.repeat(a, 1080, 1) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, mask)
    red = (235, 45, 45)
    im = im.convert("RGBA")
    im.alpha_composite(T.ring_layer(im.size, (120, 1300, 680, 1640), red, 16))
    im.alpha_composite(T.arrow_layer(im.size, (330, 800), (380, 1285), red,
                                     width=22, head=62, bow=0.25))
    im = im.convert("RGB")
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 200, 1080 - 2 * 60, 60, fill, ink,
                max_lines=3, max_block=1920 * 0.30, leading=1.02,
                band="top", margin=int(1920 * 0.10), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/hardware-wallet-short.mp4"
    work = Path.home() / "Desktop/.hardware-wallet-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Stamp("My crypto is on the device", "NEVER WAS",
                     at_word="never", tone="negative", centre_y=0.40),
        opener_holds=True)
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/hardware-wallet-short-thumb.jpg"))
    else:
        main()
