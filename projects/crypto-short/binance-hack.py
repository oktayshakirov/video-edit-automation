"""How did North Korea take $6 billion from Binance? ~45s crypto short.

Source: crypto-wiki/content/posts/how-does-north-korea-steal-crypto.mdx -
the same post as the `binance-hack` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks the size, the way
in, the evening, the freeze and what it means for you. This does one move:
the hot wallet that signed itself over and then kept sweeping every deposit
out, drawn by the `sweep` beat this pair built.

**Sentence 2 overturns the title and opens the next question.** "How did
they take it?" assumes a break-in; "Binance's own wallet signed it over"
overturns that plainly and opens "how could a wallet do that?", which the
beat answers. A how-question, not a yes/no one, and sentence 2's first word
stays on the title's subject (`narration.md`, 2026-10-23).

**Opener: `Search`** - "how did north korea hack binance" is a phrase people
type, and the editor prefers `Search` whenever it is. The last three crypto
Shorts opened Stamp / Search / Stamp.

**Two beats:** `sweep` and a full-screen `chapter` for the figure. The last
three crypto Shorts ran shares / chapter, blindsign / chapter, chart /
checklist / chapter.

**Cold close**, held by `outro=`: "Nobody broke the lock. The wallet signed
the door open." answers the opening question without re-asking it. **No
disclaimer** (the long form carries it).

**Clips** are the long form's roster; it opens and closes on the long
form's first shot, so the last frame loops into the first.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/binance-hack.py
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
DEMAND = ("New search term 'binance hack' (29 Oct 2026, E8); Johnny Harris "
          "'How North Korea Pulled off a Billion $$$ Heist' 2.9M, 18.0x (Short)")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
SITE = ROOT.parent / "crypto-wiki/public/images"

# The long form's roster - screened there, see its header.
TRADE = V / "trading-screens-dark-night/38736270.mp4"            # line charts on a dark trading monitor - opens both cuts
SWITCH = V / "server-rack-blinking-lights-close-up/1085656.mp4"  # a network switch's lights
ETH = V / "hardware-wallet-usb-crypto/10243082.mp4"              # an Ether coin on black
CANDLES = V / "trading-screens-dark-night/38440688.mp4"          # candlesticks over an RGB keyboard
GREEN = V / "cyber-security-analyst-screens/7534243.mp4"         # a hand at a keyboard under green screens
PHONEMAN = V / "man-phone-night-city-dark/19538764.mp4"          # a man checking his phone at night

BINANCE = SITE / "exchanges/binance.png"

VOICE = "noah"
MUSIC = music.track("night-drift")

SWEEP = (("BINANCE HOT WALLET", "ETHEREUM"), ("ATTACKER CONTRACT", "SWEEPER"),
         "50 SIGNED AUTHORIZATIONS", "EMPTY IN 3 MIN 24 S",
         ["20:41", "20:59", "21:04", "21:44", "22:39", "23:56"],
         "ONE TRANSACTION")


def _b(s: str) -> tuple:
    """Caption says Binance; the voice says "Bynanse"."""
    return (s, s.replace("Binance", "Bynanse"))


SENTENCES = [
    # The title question, plainly, under the Search.
    (_b("How did North Korea take six billion dollars from Binance?"),),

    # The reversal: no break-in, a signature. Opens "how could it?".
    (_b("Binance's own wallet signed it over, fifty times in one go."),),

    (_b("No private key was stolen, Binance says."),),

    ("A recent Ethereum upgrade lets a wallet run a smart contract's code, if it signs for it.",),

    # The hinge, in its own sentence, before the beat.
    ("So the attackers sent one transaction.",),

    # The sweep: one phrase per reveal.
    (_b("It hit Binance's hot wallet at twenty past eight."),
     "Fifty signed authorizations handed it to their contract.",
     "Three and a half minutes later, it was empty.",
     "And every new deposit, for hours, went straight out."),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("$6.36 BILLION. TEN BLOCKCHAINS.",
      "About six point three six billion dollars, across ten blockchains."),),

    ("Investigators blame North Korea's TraderTraitor unit, the hackers behind Bybit.",),

    # Cold close, held by `outro=`.
    ("Nobody broke the lock. The wallet signed the door open.",),
]

SHOTS = [
    Shot(clip=TRADE, clip_at=1.0, clip_ax=0.50),
    Shot(clip=SWITCH, clip_at=2.0, clip_ax=0.50, inset=(BINANCE, "top", 0.40)),
    Shot(clip=PHONEMAN, clip_at=2.0, clip_ax=0.10),
    Shot(clip=ETH, clip_at=1.0, clip_ax=0.50),
    Shot(clip=CANDLES, clip_at=3.0, clip_ax=0.50),
    Shot(graphic="sweep", payload=SWEEP),
    Shot(graphic="chapter", payload=("$6.36 BILLION. TEN BLOCKCHAINS.",)),
    Shot(clip=GREEN, clip_at=2.0, clip_ax=0.50),
    Shot(clip=TRADE, clip_at=12.0, clip_ax=0.50),
]

GAPS = [1.20, 0.85, 0.55, 0.55, 0.50, 1.90, 1.00, 0.70, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/binance-hack-short.mp4"
    work = Path.home() / "Desktop/.binance-hack-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Search("how did north korea hack binance"),
        outro="Nobody broke the lock. The wallet signed the door [open].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the `sweep` card drawn portrait in its final state
    over the same flag as the long form, lifted into the top of the frame,
    the Short's question in three rows under it, clear of the view count."""
    from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
    from video_automation.core.frame import VERTICAL
    from video_automation.longform import thumb as T
    from video_automation.longform.beats import Sweep
    ground = ROOT / "assets/brand/beat-ground-crypto.jpg"
    b = Sweep(*SWEEP[:5], "", brand=CRYPTO, frame=VERTICAL, backdrop=ground,
              reveals=[0.0, 2.0, 4.0, 7.0], start=0.0, hold=12.0)
    full = b.draw(11.8 / 12).convert("RGB")
    x0, y0 = b.log[0] - 30, b.log[1] - 30
    x1, y1 = b.log[0] + b.log[2] + 30, b.atk[1] + b.atk[3] + 30
    card = full.crop((x0, y0, x1, y1))
    flag = Image.open(ROOT / "assets/crypto/north-korea/dprk-flag.png").convert("RGB")
    flag = flag.crop(((flag.width - flag.height * 1080 // 1920) // 2, 0,
                      (flag.width + flag.height * 1080 // 1920) // 2, flag.height))
    im = ImageEnhance.Brightness(flag.resize((1080, 1920), Image.LANCZOS)
                                 .filter(ImageFilter.GaussianBlur(3))).enhance(0.42)
    # Scaled to end above the headline band, which starts near y=1170.
    k = 1000 / card.height
    card = card.resize((int(card.width * k), 1000), Image.LANCZOS)
    shape = Image.new("L", card.size, 0)
    ImageDraw.Draw(shape).rounded_rectangle([2, 2, card.width - 3, card.height - 3],
                                            radius=24, fill=255)
    im.paste(card, ((1080 - card.width) // 2, 130), shape)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "$6 billion\nfrom\n[Binance?]", 200,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.26, leading=1.02, band="bottom",
                margin=int(1920 * 0.16) + 20, shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/binance-hack-short-thumb.jpg"))
    else:
        main()
