"""How hard is it to guess a seed phrase? ~50s crypto short.

Source: crypto-wiki/content/posts/what-is-a-seed-phrase.mdx - the same post
as the `seed-phrase` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks what a seed phrase
is, how it is made, what it unlocks, the odds, the thefts and the backup.
This does one move, the question the standout's comments kept asking
("can't a hacker just try the words?", `demand/teardowns/what-is-a-seed-
phrase.md`), and CoinGecko's own "Can Someone Guess My Bitcoin Seed
Phrase?" sits at 18.8k on it: twelve words are really 128 coin flips, the
number of phrases is 39 digits long, so nobody guesses one - they get shown
it. Built as the plain answer in the order a viewer asks it, one drawn beat
per question (`shorts.md`, 2026-10-13): how is it made (`mnemonic`), how
many are there (`chapter`), so how are they stolen (`grid`).

**Sentence 2 overturns the title's assumption and opens the next
question.** "How hard is it to guess?" assumes twelve guessable words;
"your twelve words are really 128 coin flips" says what they are instead
and opens "so how many is that?". A how-question, not a yes/no one, and
sentence 2's first words stay on the title's subject (`narration.md`,
2026-10-23).

**Opener: `Stamp`**, MYTH over "12 words are easy to guess", landing on
"really". The last three crypto Shorts opened Search / Search / Stamp; the
long form takes a Stamp of its own on a different belief.

**Cold close**, held by `outro=`: "Nobody guesses twelve words. Somebody gets
shown them." answers the opening question without re-asking it, on the
clip the Short opened on. **No disclaimer** (the long form carries it).

**Clips** are the long form's roster.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/seed-phrase.py
"""

import hashlib
import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp

SOURCE_POST = "what-is-a-seed-phrase"
DEMAND = ("CoinGecko 'Can Someone Guess My Bitcoin Seed Phrase?' 18.8k; "
          "'what is a seed phrase' proven: CoinGecko 11x, Hipo Short 4.9x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]

# The long form's roster - screened there, see its header.
THUMB = V / "typing-on-phone-dark-close-up/33942937.mp4"      # a thumb over a lit phone in the dark - opens and closes
COINSPIN = V / "coin-flip-slow-motion/18977071.mp4"           # a coin spinning down onto a table
COIN = V / "coin-flip-slow-motion/30882814.mp4"               # a coin flipping on pure black
TYPING = V / "laptop-login-screen-dark/34771078.mp4"          # hands typing, near black
CAMERA = V / "smartphone-camera-close-up-dark/3649788.mp4"    # a phone's camera in the dark

VOICE = "noah"
MUSIC = music.track("night-drift")

# The long form's demo entropy, so both cuts draw the same phrase.
ENTROPY = hashlib.sha256(b"thecrypto.wiki seed phrase demo").hexdigest()[:32]

SENTENCES = [
    # The title question, plainly, under the Stamp.
    ("How hard is it to guess a seed phrase?",),

    # The reversal: not words, coin flips. Opens "how many is that?".
    ("Your twelve words are really a hundred and twenty-eight coin flips.",),

    # The hinge, in its own sentence, before the beat.
    ("Your wallet made them at random, then turned them into words, like this.",),

    # The mnemonic: one phrase per reveal.
    ("A hundred and twenty-eight random bits.",
     "Four more as a check, cut into twelve groups.",
     "Each group is a number, up to two thousand and forty-seven.",
     "And each number picks a word from a fixed list."),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("A 39-DIGIT NUMBER OF PHRASES",
      "So the number of possible phrases is thirty-nine digits long."),),

    ("A trillion guesses a second would take hundreds of millions of times the age of the universe.",),

    # The hinge into the grid.
    ("So how do seed phrases get stolen?",),

    # The grid: one card per phrase.
    ("A photo of the words, synced to the cloud.",
     "A device sold with the words already printed.",
     "A support page that asks you to type them in."),

    # Cold close, held by `outro=`.
    ("Nobody guesses twelve words. Somebody gets shown them.",),
]

SHOTS = [
    Shot(clip=THUMB, clip_at=1.0, clip_ax=0.50),
    Shot(clip=COINSPIN, clip_at=1.0, clip_ax=0.45),
    Shot(clip=COIN, clip_at=0.3, clip_ax=0.50),
    Shot(graphic="mnemonic", payload=(ENTROPY, "TWELVE WORDS")),
    Shot(graphic="chapter", payload=("A 39-DIGIT NUMBER OF PHRASES",)),
    # Not the long form's dark-room laptop or search screen: in 9:16 both
    # crop onto a bright screen of icons under the caption (`shorts.md`,
    # 2026-10-27).
    Shot(clip=TYPING, clip_at=1.0, clip_ax=0.50),
    Shot(clip=CAMERA, clip_at=24.0, clip_ax=0.45),
    Shot(graphic="grid",
         payload=([("A photo of the words", "synced to the cloud", "\U0001F4F8"),
                   ("A pre-printed card", "in a resold device", "\U0001F4E6"),
                   ("A fake support page", "asking for your words", "\U0001F3A3")],
                  "HOW PHRASES ARE TAKEN")),
    Shot(clip=THUMB, clip_at=9.0, clip_ax=0.50),
]

GAPS = [1.00, 0.85, 0.55, 1.70, 1.00, 0.80, 0.60, 1.40, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/seed-phrase-short.mp4"
    work = Path.home() / "Desktop/.seed-phrase-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Stamp("12 words are easy to guess", "MYTH", at_word="really"),
        outro="Nobody guesses twelve words. Somebody gets [shown] them.")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's picture, cut round the hand and nib,
    lifted into the lower frame with its own top continued upward
    (`bleed_portrait`), and the Short's question in three rows above it,
    clear of the view count."""
    import importlib.util
    from PIL import Image, ImageEnhance
    from video_automation.longform import thumb as T
    spec = importlib.util.spec_from_file_location(
        "seed_long", ROOT / "projects/crypto-long/seed-phrase.py")
    long = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(long)
    src = long.cover_frame()
    w, h = src.size
    cw = int(h * 0.80)
    crop = src.crop((w - cw - 40, 0, w - 40, h))
    im = T.bleed_portrait(crop, y=1920 - int(crop.height * 1080 / crop.width),
                          fill="blur")
    im = ImageEnhance.Brightness(im).enhance(0.95)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "Can anyone\nguess your\n[12 words?]", 190,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.30, leading=1.02, band="top",
                margin=int(1920 * 0.12), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/seed-phrase-short-thumb.jpg"))
    else:
        main()
