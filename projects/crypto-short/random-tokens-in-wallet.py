"""Why would a stranger send you free crypto? ~45s crypto short.

Source: crypto-wiki/content/posts/understanding-crypto-airdrops.mdx - the
same post as the `random-tokens-in-wallet` long form, written in the same
pass.

**Not a trailer for the long form.** The long form walks where the token
came from, the claim signature, the hardware wallet, address poisoning (its
climax) and the rules. This does one move, the one the airdrops article
names in its "Beware of fake tokens" line: the token is bait, and the hook
is a signature, not the token. Built as the plain answer in the order a
viewer asks it (`shorts.md`, 2026-10-13): is it dangerous (no, receiving is
harmless), then what is it for (`blindsign`), then would a hardware wallet
stop it (no).

**Sentence 2 overturns the title's assumption and opens the next
question.** "Why would a stranger send you free crypto?" assumes a gift;
"It isn't a gift. It's bait" overturns it plainly and opens "bait for
what?". A why-question, not a yes/no one, and sentence 2's first words stay
on the title's subject (`narration.md`, 2026-10-23).

**Opener: `Stamp`**, BAIT over "Free crypto is a gift", landing on "bait".
The last three crypto Shorts opened Counter / Stamp / Counter; the long
form takes a Stamp of its own on a different belief (rotation is across
videos, `shorts.md`, 2026-10-20).

**Close: a plain last sentence, no `outro=` card** (2026-11-06). "The token
can't take anything. Your signature can." answers the opening question on
the clip the Short opened on, captioned like every other line. The editor:
"lets remove the stamp outros from the shorts (we really struggle to keep
the viewers till the end and they are slow), just add it to the script"
(`shorts.md`, "No outro card on a Short"). **No disclaimer** (the long form
carries it).

**Two of the long form's best moments, carried over on the editor's notes**
(2026-11-06): the `diagram` with its animated icons, on how the token
reached you, and the `behind` - OFFLINE between the site's Ledger and its
room - for the hardware wallet, in place of an `isolate` that cut the hand
holding it badly.

**Clips** are the long form's roster.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/random-tokens-in-wallet.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp

SOURCE_POST = "understanding-crypto-airdrops"
DEMAND = ("Cyber Scrilla 'If you find random Crypto in your wallet... DO THIS' "
          "11.7x (235k) - re-angle of the airdrops article")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]

# The long form's roster - screened there, see its header.
PHONEDARK = V / "holding-smartphone-dark-background-close-up/13358555.mp4"  # hands on a glowing phone in black - opens and closes
TRADE = V / "cryptocurrency-app-on-phone/8480231.mp4"                    # a trading app on a phone
HOLD = V / "holding-smartphone-dark-background-close-up/7534329.mp4"     # hands turning a phone over, dark
DESK = V / "thumb-scrolling-phone-close-up/17586687.mp4"                 # a hand at a phone on a dark desk

# The real thing, as in the long form: a public address on Blockscout taking
# token transfers from strangers (`screencap`, 9:16), and the site's own
# photograph of a Ledger in someone's hands.
ADDRESS = STOCK / "captures/blockscout-dead/address-vertical.mp4"
LEDGER = _P.home() / "Coding/crypto-wiki/public/images/posts/ledger.jpeg"

# The editor's cover image: a stranger holding out coins. AI-generated,
# supplied by the editor, no credit owed.
STRANGER = ROOT / "assets/crypto/random-tokens/stranger.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly, under the Stamp.
    ("Why would a stranger send you free crypto?",),

    # The reversal: not a gift, bait. Opens "bait for what?".
    ("It isn't a gift. It's bait, and it can't hurt you until you bite.",),

    # The hinge, then the long form's diagram: one chunk per box.
    ("Your address is public, so anyone can send to it.",),
    ("A script reads the chain,",
     "drops the same token in thousands of wallets,",
     "and waits for one person to bite."),

    ("But you can't sell it, and its name sends you to a website to claim it.",),

    # The hinge, in its own sentence, before the beat.
    ("That site asks for one small approval, like this.",),

    # The blindsign: card, approval, truth.
    ("The screen says claim, and a fee of a few cents.",
     "You approve.",
     "But you just let their contract move your tokens, with no limit."),

    # The pile: the tokens in, then the floor opening.
    ("Your tokens.",
     "One signature, and the wallet is empty."),

    # The behind: the word, then its line.
    ("A hardware wallet keeps your keys offline.",
     "But it still signs whatever you approve."),

    # The close, said and captioned - no outro card.
    ("The token can't take anything. Your signature can.",),
]

SHOTS = [
    Shot(clip=PHONEDARK, clip_at=1.0, clip_ax=0.50),
    # Not the nightstand: its 9:16 crop was a hand and a wall (2026-11-06).
    Shot(clip=HOLD, clip_at=1.0, clip_ax=0.50),
    Shot(clip=ADDRESS, clip_at=0.0),
    Shot(graphic="diagram",
         payload=([("A script", "reads the chain", "\U0001F916"),
                   ("Thousands of wallets", "the same free token", "\U0001F381"),
                   ("One bite", "is all it needs", "\U0001F3A3")],
                  "HOW IT REACHED YOU", False)),
    Shot(clip=TRADE, clip_at=0.5, clip_ax=0.55),
    Shot(clip=DESK, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="blindsign",
         payload=([("Action", "Claim reward"),
                   ("Amount", "5,000 tokens"),
                   ("Network fee", "A few cents")],
                  [("Action", "Approve spending"),
                   ("Spender", "Their contract"),
                   ("Limit", "Unlimited")],
                  ["YOU"], "ONE SIGNATURE")),
    Shot(graphic="pile",
         payload=([(30, "YOUR TOKENS")], "ONE SIGNATURE", "EMPTY WALLET")),
    # The long form's OFFLINE cut: the `isolate` cut the hand round the
    # device raggedly in 9:16 (2026-11-06).
    # The photo whole, OFFLINE on top: no cutout, which frayed round the
    # fingers in both cuts (2026-11-06).
    Shot(graphic="behind",
         payload=(LEDGER, "OFFLINE", "But it signs whatever you approve",
                  "fly", None, False)),
    Shot(clip=PHONEDARK, clip_at=7.0, clip_ax=0.50),
]

GAPS = [1.00, 0.85, 0.55, 1.30, 0.70, 0.55, 1.90, 1.40, 0.90, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/random-tokens-short.mp4"
    work = Path.home() / "Desktop/.random-tokens-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Stamp("Free crypto is a gift", "BAIT", at_word="bait"))
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the editor's stranger holding out coins in the lower
    frame, his own near-black ground above him, and the Short's question in
    three rows there, clear of the view count."""
    import numpy as np
    from PIL import Image, ImageEnhance
    from video_automation.longform import thumb as T
    src = Image.open(STRANGER).convert("RGB")
    w, h = src.size
    crop = src.crop((int(w * 0.10), 0, int(w * 0.90), h))
    pic = crop.resize((1080, int(crop.height * 1080 / crop.width)),
                      Image.LANCZOS)
    # His head touches the source's top edge, so `bleed_portrait` stretched
    # his forehead up the frame as a skin-coloured streak (2026-11-06). The
    # ground is the picture's own near-black, and the cut hairline feathers
    # into it over 110px instead.
    edge = tuple(int(c) for c in
                 np.asarray(pic)[:40, :60].reshape(-1, 3).mean(0))
    im = Image.new("RGB", (1080, 1920), edge)
    mask = np.ones((pic.height, 1080), np.float32)
    mask[:110] = np.linspace(0.0, 1.0, 110)[:, None]
    im.paste(pic, (0, 1920 - pic.height),
             Image.fromarray((mask * 255).astype("uint8")))
    im = ImageEnhance.Brightness(im).enhance(1.04)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "Free crypto\nfrom a\n[stranger?]", 190,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.30, leading=1.02, band="top",
                margin=int(1920 * 0.20), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/random-tokens-short-thumb.jpg"))
    else:
        main()
