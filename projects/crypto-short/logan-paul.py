"""How did Logan Paul win 27 claims over CryptoZoo? ~35s crypto short.

Source: crypto-wiki/content/crypto-ogs/logan-paul.mdx - the same article
as the `logan-paul` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks what CryptoZoo
was, the buyback and the whole fight in court. This does one move: Paul's
own claim ("They Sued Me And Lost (27 Times)", his YouTube title) checked
against the record - he won round one, on one word, puffery.

**Second re-cut (2026-11-11, the editor: "too confusing to follow if you
are not familiar with the story", and the reel's cards went by too fast to
see).** It now tells the story in order for someone who has never heard of
it: who (Logan Paul sold his fans a crypto game), what (CryptoZoo, "a
really fun game that makes you money"), how it worked (the reel, one
full sentence per card so each holds ~2s), what happened (sold out, never
playable, the refund's catch), then the court and his own "they sued me and
lost" against the 26 claims allowed back in.

**Opener: `Stamp`** - his own pitch, A REALLY FUN GAME THAT MAKES YOU
MONEY, stamped NEVER FINISHED on "never". A verdict on a claim, never on
the man (`projects/crypto.md`).

**Pictures:** Logan Paul from frame one (`pop`), CryptoZoo's own egg and
wordmark, a `reel` through its egg and the lion and shark from its own
site. Two stock clips (the signature, the courthouse).

**E17: 30-40s.** **Close: a plain last sentence, no `outro=` card**,
echoing the pitch the opening asked about, on the portrait the Short opened
on. **No disclaimer** (the long form carries it).

    PYTHONPATH=. .venv/bin/python projects/crypto-short/logan-paul.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp

SOURCE_POST = "logan-paul"
DEMAND = ("'logan paul cryptozoo': Kyle Boland egg-hatching Short 11.2x; "
          "George Janko 'CryptoZoo Scandal' Short 7.6x (236 days); Logan "
          "Paul 'They Sued Me And Lost (27 Times)' 1.07M")
# The cover's style, for the review to compare views and clicks by
# (`thumbnails.md`, "Cover styles are a choice, and every video says which").
COVER_STYLE = "text"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
PEOPLE = ROOT / "assets/crypto/logan-paul"
PRESS = STOCK / "press/logan-paul"
BEATGROUND = ROOT / "assets/brand/beat-ground-crypto.jpg"

# The long form's roster - screened there, see its header.
LOGAN = PEOPLE / "lp-48086760546.jpg"
LOGAN_CAP = PEOPLE / "lp-48086619418.jpg"
EGG_SQ = PRESS / "cz-og.jpg"                  # CryptoZoo's own egg, square, on black
HERO = PRESS / "cz-hero.jpg"                  # the egg beside the CRYPTOZOO wordmark, square
# The same on a wider black, so the wordmark's tracked letters do not run
# off a 9:16 frame's edges under the Ken Burns zoom (the first render cut
# the C and the last O). Made by `_hero_pad()`.
HERO_PAD = PRESS / "cz-hero-pad.jpg"
# CryptoZoo's own site slides (cryptozoo.co/img, Dec 2022, via the Wayback
# Machine) - the animals it sold the idea with. SOURCES.md there.
LION = PRESS / "cz-slide-1.jpg"
SHARK = PRESS / "cz-slide-4.jpg"
SIGNING = V / "signing-contract-pen-close-up-dark/8061370.mp4"  # a hand signing papers - the waiver
COURTHOUSE = V / "courthouse-exterior-night/14994537.mp4"       # the long form's, a domed courthouse at dusk

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The introduction (re-cut 2026-11-11, the editor: "too confusing to
    # follow if you are not familiar with the story"): who, and what he
    # sold, before any of the court. The Stamp lands NEVER FINISHED on
    # "never", over his own pitch.
    ("Logan Paul sold his fans a crypto game that was never finished.",),

    # What it was called and how he sold it - over its own wordmark.
    ("He called CryptoZoo a really fun game that makes you money.",),

    # The reel's own sentence: one phrase per card, each long enough that
    # the card holds ~2s (the first cut's three-word phrases moved the
    # camera on before a card could be read).
    ("You bought an egg with its own coin, ZOO.",
     "The egg hatched into an animal.",
     "Breed two animals, and sell the babies."),

    # The pile's own sentence: the eggs pour in, then the floor opens.
    ("The first eggs sold out in minutes.",
     "The game never became playable."),

    ("Buyers sued. His refund had a catch: give up your right to sue.",),

    # The behind's own sentence: the word, then its line.
    ("In 2025 a judge threw out all twenty-seven claims, calling the pitch puffery,",
     "sales talk too vague to be a promise."),

    # His own claim, and what is true instead.
    ("Logan said they sued me and lost. But twenty-six claims were allowed back in.",),

    # The close, said and captioned - no outro card - on the opening
    # portrait, so the loop's last frame matches its first.
    ("So in court, a game that makes you money promised nothing.",),
]

SHOTS = [
    Shot(image=LOGAN_CAP, pop=True),
    Shot(image=HERO_PAD, aspect=1.0, zoom=1.05),
    Shot(graphic="reel", backdrop=BEATGROUND,
         payload=([(EGG_SQ, "BUY AN EGG"),
                   (LION, "HATCH AN ANIMAL"),
                   (SHARK, "BREED AND SELL")], "CRYPTOZOO")),
    Shot(graphic="pile", backdrop=BEATGROUND,
         payload=([(30, "EGGS SOLD OUT")], "CRYPTOZOO", "NO GAME")),
    Shot(clip=SIGNING, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="behind",
         payload=(LOGAN, "PUFFERY", "Too vague to be a promise",
                  "fly", None, False)),
    Shot(clip=COURTHOUSE, clip_at=1.0),
    Shot(image=LOGAN_CAP, parallax=0.6),
]

GAPS = [0.80, 0.70, 0.70, 0.80, 0.80, 0.90, 0.90, 1.20]

HEADLINE = "What\nhappened to\n[CryptoZoo?]"


def _hero_pad() -> Path:
    """`HERO` centred on a black square 1.3x its size."""
    from PIL import Image
    src = Image.open(HERO).convert("RGB")
    n = int(max(src.size) * 1.3)
    im = Image.new("RGB", (n, n), (0, 0, 0))
    im.paste(src, ((n - src.width) // 2, (n - src.height) // 2))
    im.save(HERO_PAD, quality=94)
    return HERO_PAD


def thumbs(out: Path) -> Path:
    """The 9:16 cover, the long form's picture and question (a pair shares
    a thumbnail): Logan Paul's portrait in the lower frame, the egg and the
    question on the black above."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(LOGAN_CAP).convert("RGB")
    w, h = src.size
    crop = src.crop((0, int(h * 0.02), w, int(h * 0.72)))
    pic = crop.resize((1080, int(crop.height * 1080 / crop.width)), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (0, 0, 0))
    y = 1920 - pic.height
    im.paste(pic, (0, y))
    a = np.zeros((1920, 1), np.float32)
    a[:y + 260, 0] = 1.0
    a[y:y + 260, 0] = np.linspace(1.0, 0.0, 260)
    mask = Image.fromarray((np.repeat(a, 1080, 1) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, mask)
    egg = Image.open(EGG_SQ).convert("RGB").resize((440, 440), Image.LANCZOS)
    yy, xx = np.mgrid[0:440, 0:440] / 439 - 0.5
    al = np.clip((0.5 - np.sqrt(xx ** 2 + yy ** 2)) / 0.12, 0, 1)
    im.paste(egg, (590, int(1920 * 0.07)), Image.fromarray((al * 255).astype("uint8")))
    # A ring round the egg and an arrow pointing at it (the editor,
    # 2026-11-11), the long cover's marks at 9:16 weight.
    red = (235, 45, 45)
    im = im.convert("RGBA")
    im.alpha_composite(T.ring_layer(im.size, (625, 150, 985, 570), red, 16))
    im.alpha_composite(T.arrow_layer(im.size, (170, 420), (600, 330), red,
                                     width=22, head=62, bow=0.30))
    im = im.convert("RGB")
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 200, 1080 - 2 * 60, 60, fill, ink,
                max_lines=3, max_block=1920 * 0.30, leading=1.02,
                band="top", margin=int(1920 * 0.30), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def main() -> None:
    _hero_pad()
    out = Path.home() / "Desktop/logan-paul-short.mp4"
    work = Path.home() / "Desktop/.logan-paul-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # Below the portrait's face, high enough that the four-line quote's stamp
        # stays on screen (0.80 cut it off); captions do not run under an opener.
        opener=Stamp("A really fun game that makes you money",
                     "NEVER FINISHED", at_word="never",
                     tone="negative", centre_y=0.68),
        opener_holds=True)
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/logan-paul-short-thumb.jpg"))
    else:
        main()
