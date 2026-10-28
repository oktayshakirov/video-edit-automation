"""Who gets your Bitcoin when you die? ~45s crypto short.

Source: crypto-wiki/content/posts/what-happens-to-crypto-when-you-die.mdx -
the same post as the `crypto-when-you-die` long form, written in the same
pass.

**Not a trailer for the long form.** The long form walks the keys, the
exchange's estate process, self-custody, the will and two setups that work.
This does one move, in the order a viewer would ask it: your will does not
decide who gets self-held coins, the seed phrase does, so where do the words
go? Four places on a `reel`, each judged as the camera reaches it, ending on
the one that works.

**Sentence 2 overturns the title and opens the next question.** "Who gets
it?" assumes the will; "not the people your will names - whoever holds the
words that unlock it" overturns that plainly and opens "so where do I keep
the words?", which the reel answers. The title is a who-question, not a
yes/no one (`narration.md`, 2026-10-11).

**Opener: `Stamp`.** The belief people act on is that a will takes care of
it, and the verdict judges that claim, not a coin or a platform
(`projects/crypto.md`). Last three crypto Shorts opened hook / Counter /
Stamp; this pair's long form takes `Search` because its title is the query.

**Two beats:** a full-screen `chapter` for the lost-coin estimate and a
`reel` (its first use in a shipped Short). The last three crypto Shorts ran
checklist / chapter, pool / chapter, chart / checklist / chapter.

**Cold close**, held by `outro=`: "Your will says who gets it. Only your keys
decide if they can." answers the opening question without re-asking it, so
the last frame loops into the first. **No disclaimer** (the long form
carries it).

**Clips** are the long form's roster plus a desk drawer for the reel; it
opens on the long form's first shot.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/crypto-when-you-die.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp

SOURCE_POST = "what-happens-to-crypto-when-you-die"

V = STOCK / "videos"
P = STOCK / "photos"
ROOT = _P(__file__).resolve().parents[2]

# The long form's roster - screened there, see its header.
JUDGE = V / "judge-gavel-courtroom/6101367.mp4"            # a judge's hands by a gavel - the long form's first shot
HANDS = V / "elderly-hands-holding/8057825.mp4"            # two people holding hands
SIGN = V / "signing-documents-desk-lamp/8061370.mp4"       # hands signing a stack of papers
USB = V / "usb-device-plugged-laptop-dark/40304895.mp4"    # a device plugged into a laptop in the dark
DRIVE = V / "old-hard-drive-computer/7841655.mp4"          # an opened hard drive, platter spinning
WRITE = V / "writing-on-paper-notebook-night/39425741.mp4"  # a hand writing in a notebook under a lamp
WINDOW = V / "man-thinking-dark-window/33972359.mp4"       # a man standing still by a curtain
NOTARY = V / "notary-stamping-document/8731441.mp4"        # a hand signing papers by a law book
ENVELOPE = V / "sealed-envelope-wax-seal/5916730.mp4"      # hands sealing an envelope
# Short only: 14s, L85-98, a hand opening a white desk drawer. Bright, but
# it is the noun.
DRAWER = V / "desk-drawer-opening/9130356.mp4"

KEYPAD = P / "wall-safe/1990764.jpg"              # a keypad safe
# Both covers, the editor's pick: a man in a trench coat at a grave.
GRAVE = P / "man-at-grave/10499499.jpg"           # 6073x4049, the man at ~0.55-0.83 of the width

VOICE = "noah"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly, under the Stamp's quote.
    ("Who gets your Bitcoin when you die?",),

    # The verdict lands on "names": the reversal, with the next question
    # (where do the words go?) already open.
    ("Not the people your will names. Whoever holds the words that unlock it.",),

    ("A bank lets your family in with paperwork.",),

    ("A wallet you hold yourself has no reset.",),

    ("Lose the seed phrase, and the coins never move again.",),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("UP TO 3.7M BITCOIN. ALREADY LOST.",
      "An estimated three to three point seven million bitcoin are already stuck like that."),),

    # The hinge, in its own sentence, before the reel.
    ("So where do the words go?",),

    # The reel: one phrase per card, the camera moving on each.
    ("In your head? Your family never finds them.",
     "In a desk drawer? So does a burglar.",
     "In your will? Probate can make it public.",
     "In a safe, split in two, with a sealed letter that says where."),

    # Cold close, held by `outro=`.
    ("Your will says who gets it. Only your keys decide if they can.",),
]

SHOTS = [
    Shot(clip=JUDGE, clip_at=1.0, clip_ax=0.50),
    Shot(clip=HANDS, clip_at=1.0, clip_ax=0.50),
    Shot(clip=SIGN, clip_at=1.0, clip_ax=0.50),
    Shot(clip=USB, clip_at=1.0, clip_ax=0.50),
    Shot(clip=DRIVE, clip_at=2.0, clip_ax=0.50),
    Shot(graphic="chapter", payload=("UP TO 3.7M BITCOIN. ALREADY LOST.",)),
    Shot(clip=WRITE, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="reel",
         payload=([(WINDOW, "In your head"),
                   (DRAWER, "A desk drawer"),
                   (NOTARY, "Your will"),
                   (KEYPAD, "Split, and a letter")], "")),
    Shot(clip=ENVELOPE, clip_at=1.0, clip_ax=0.50),
]

GAPS = [0.50, 0.85, 0.45, 0.70, 0.60, 1.00, 0.55, 1.00, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/crypto-when-you-die-short.mp4"
    work = Path.home() / "Desktop/.crypto-when-you-die-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The belief, and a verdict on the claim - not on a coin or a
        # platform. Lands on "names", the reversal in sentence 2.
        opener=Stamp("Leave your Bitcoin in your will", "NOT ENOUGH",
                     tone="negative", at_word="names"),
        outro="Your will says who gets it. Only your [keys] decide if they can.")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's man at the grave, cut round him and
    scaled to the width so his face sits in the top half, the headline in
    three rows over a dark ramp at the bottom, clear of the view count."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(GRAVE).convert("RGB")
    crop = src.crop((int(src.width * 0.44), 0, int(src.width * 0.96), src.height))
    crop = crop.resize((1080, int(crop.height * 1080 / crop.width)), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (0, 0, 0))
    im.paste(crop, (0, 0))
    a = np.zeros((1920, 1), np.float32)
    a[980:1380, 0] = np.linspace(0, 1.0, 400)
    a[1380:, 0] = 1.0
    ramp = Image.fromarray((np.repeat(a, 1080, 1) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ramp)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "Who gets\nyour\n[Bitcoin?]", 220,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.30, leading=1.02, band="bottom",
                margin=int(1920 * 0.16) + 20, shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/crypto-when-you-die-short-thumb.jpg"))
    else:
        main()
