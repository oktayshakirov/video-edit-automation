"""How did North Korea steal $1.5 billion in one transaction? ~45s crypto short.

Source: crypto-wiki/content/posts/how-does-north-korea-steal-crypto.mdx -
the same post as the `north-korea-crypto` long form, written in the same
pass.

**Not a trailer for the long form.** The long form walks the thieves, the
heists, the three ways in, the laundering and what it means for you. This
does one move: the Bybit signing screen. Nobody broke the code; the signers
approved a transaction whose screen lied, drawn by the `blindsign` beat this
pair built.

**Sentence 2 overturns the title and opens the next question.** "How did
they steal it?" assumes a break-in; "Bybit's own signers approved it"
overturns that plainly and opens "why would they?", which the beat answers.
It is a how-question, not a yes/no one (`narration.md`, 2026-10-11), and
sentence 2's first word stays on the title's subject (the theft's victim).

**Opener: `Search`** - the title is a phrase people type (Johnny Harris's
18x Short is titled on it), and the editor prefers `Search` over the redacted
hook whenever it is. The last three crypto Shorts opened Stamp / Counter /
Stamp. It shares the long form's opener, which a pair may.

**Two beats:** `blindsign` and a full-screen `chapter` for the figure. The
last three crypto Shorts ran chapter / reel, chapter / pool, chart /
checklist / chapter.

**Cold close**, held by `outro=`: "They never broke the lock. They changed
what the signers saw." answers the opening question without re-asking it,
so the last frame loops into the first. **No disclaimer** (the long form
carries it).

**Clips** are the long form's roster; it opens on the long form's first
shot.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/north-korea-crypto.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Search

SOURCE_POST = "how-does-north-korea-steal-crypto"
DEMAND = ("Johnny Harris 'How North Korea Pulled off a Billion $$$ Heist' 2.9M, "
          "18.0x (Short)")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
SITE = ROOT.parent / "crypto-wiki/public/images"

# The long form's roster - screened there, see its header.
CLICK = V / "clicking-download-laptop-close-up/36392510.mp4"        # a hand on a mouse in red light - the long form's first shot
ENTER = V / "hand-pressing-enter-key/5119219.mp4"                   # a finger pressing Enter
# Not the long form's terminal: its white log text sat under the burned
# caption and the line could not be read.
KEYS = V / "office-workers-computers-night/39425751.mp4"            # fingers on a backlit keyboard
TYPING = V / "hands-typing-laptop-dark-room/6611947.mp4"            # hands on a laptop, a blank lit screen
# Not the long form's stylus clip: in 9:16 its tablet falls outside the crop
# and leaves a hand holding a pencil.
DESKS = V / "man-working-laptop-alone-night/38990451.mp4"           # a man facing two lit screens in a dark room
OPS = V / "security-camera-monitoring-room/7255101.mp4"             # analysts in front of a wall of screens
CONTRACT = V / "person-reading-contract-carefully/7841874.mp4"      # a hand with glasses over a contract

BYBIT = SITE / "exchanges/bybit.png"

VOICE = "noah"
MUSIC = music.track("night-drift")

SHOWN = [("Action", "Routine transfer"), ("From", "Cold wallet"),
         ("To", "Bybit hot wallet")]
REAL = [("Action", "Replace wallet code"), ("From", "Cold wallet"),
        ("Control", "The attackers")]

SENTENCES = [
    # The title question, plainly, under the Search.
    ("How did North Korea steal one and a half billion dollars in one transaction?",),

    # The reversal: no break-in, an approval. Opens "why would they?".
    ("Bybit's own signers approved it, every one of them.",),

    ("Nobody cracked the encryption, and Bybit's systems were never breached.",),

    ("The attackers had hacked one developer at Safe Wallet, the service Bybit signed with.",),

    # The hinge, in its own sentence, before the beat.
    ("So they controlled what the signers saw.",),

    # The blindsign: the card, the approvals, the truth.
    ("The screen showed a routine transfer to Bybit's own hot wallet.",
     "Three signers approved it, the last one the CEO.",
     "But what they signed handed the wallet to the attackers."),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("ABOUT $1.46 BILLION. ONE TRANSACTION.",
      "About one point four six billion dollars, in a single transaction."),),

    ("Five days later, the FBI named North Korea.",),

    # Cold close, held by `outro=`.
    ("They never broke the lock. They changed what the signers saw.",),
]

SHOTS = [
    Shot(clip=CLICK, clip_at=0.5, clip_ax=0.55),
    Shot(clip=ENTER, clip_at=2.0, clip_ax=0.50),
    Shot(clip=KEYS, clip_at=1.0, clip_ax=0.50),
    Shot(clip=TYPING, clip_at=1.0, clip_ax=0.50, inset=(BYBIT, "top", 0.40)),
    Shot(clip=DESKS, clip_at=2.0, clip_ax=0.50),
    Shot(graphic="blindsign",
         payload=(SHOWN, REAL, ["SIGNER", "SIGNER", "CEO"],
                  "WHAT THE SIGNERS SAW")),
    Shot(graphic="chapter", payload=("ABOUT $1.46 BILLION. ONE TRANSACTION.",)),
    Shot(clip=OPS, clip_at=1.0, clip_ax=0.60),
    Shot(clip=CONTRACT, clip_at=0.5, clip_ax=0.50),
]

GAPS = [1.20, 0.85, 0.55, 0.55, 0.55, 1.80, 1.00, 0.70, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/north-korea-crypto-short.mp4"
    work = Path.home() / "Desktop/.north-korea-crypto-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Search("how did north korea steal $1.5 billion"),
        outro="They never broke the lock. They changed what the signers [saw].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's card, drawn portrait and lifted into
    the top of the frame over the same flag, the Short's question in three
    rows under it, clear of the view count."""
    from PIL import Image
    from video_automation.core.frame import VERTICAL
    from video_automation.longform import thumb as T
    from video_automation.longform.beats import BlindSign
    ground = ROOT / "assets/brand/beat-ground-crypto.jpg"
    b = BlindSign(SHOWN, REAL, ["SIGNER", "SIGNER", "CEO"], "", brand=CRYPTO,
                  frame=VERTICAL, backdrop=ground,
                  reveals=[0.0, 3.0, 6.0], start=0.0, hold=9.0)
    # The card alone, lifted ~380px over the long form's flag ground: the
    # rows need the bottom third.
    from PIL import ImageEnhance, ImageFilter
    full = b.draw(8.9 / 9)
    flag = Image.open(ROOT / "assets/crypto/north-korea/dprk-flag.png").convert("RGB")
    flag = flag.crop(((flag.width - flag.height * 1080 // 1920) // 2, 0,
                      (flag.width + flag.height * 1080 // 1920) // 2, flag.height))
    im = ImageEnhance.Brightness(flag.resize((1080, 1920), Image.LANCZOS)
                                 .filter(ImageFilter.GaussianBlur(3))).enhance(0.42)
    x0, y0 = b.x0, b.y0
    card = full.crop((x0 - 4, y0 - 4, x0 + b.cw + 4, y0 + b.ch + 4))
    from PIL import ImageDraw
    shape = Image.new("L", card.size, 0)
    ImageDraw.Draw(shape).rounded_rectangle([2, 2, card.width - 3, card.height - 3],
                                            radius=28, fill=255)
    im.paste(card, (x0 - 4, y0 - 4 - 380), shape)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "$1.5 billion\nin one\n[transaction?]", 200,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.26, leading=1.02, band="bottom",
                margin=int(1920 * 0.16) + 20, shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/north-korea-crypto-short-thumb.jpg"))
    else:
        main()
