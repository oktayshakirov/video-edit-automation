"""What is a seed phrase - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/what-is-a-seed-phrase.mdx.

**The angle.** "what is a seed phrase" is a proven query (CoinGecko twice at
11x, Hipo 4.9x), and the teardown (`demand/teardowns/what-is-a-seed-phrase.md`)
found what the standout's viewers came for: its most replayed stretch is the
bits turning into words, and its top comments are "confusing" and "can't a
hacker just try the words?". So this walks the mechanism the standout rushed
- coin flips, a checksum, numbers, words - drawn rather than read, then
answers the guessing question with the arithmetic, then turns to what the
article says actually causes losses: people, not math. The close echoes the
open: the coins are not in the app; the only way in is whoever holds the
paper.

**A mechanism, so the default arc** (`longform.md`), with the Short's move -
the odds - as the turn in chapter four.

**Every figure is the article's or arithmetic on it.** 128 bits plus a 4-bit
checksum, 2048 words, BIP39 in 2013, one seed deriving 1,000,000+
addresses, 24 words squaring the space (the article's "2^128 times
stronger"). 2^128 is 39 digits long; at a trillion guesses a second the
whole space takes ~1.1e19 years, half of it ~5.4e18 - about 390 to 780
million times the universe's 13.8 billion years, said as "hundreds of
millions of times". The three thefts are the article's own composites, told
as kinds of theft, not as named cases. The phrase the `mnemonic` beat draws is
a real BIP39 phrase computed from fixed demo entropy, and the script says so
out loud: a phrase that has been on a screen is not a secret.

## The beats

Last three crypto long forms: binance-hack (sweep / bars / compare),
prediction-markets (shares / diagram / post / checklist), north-korea-crypto
(blindsign / timeline / post / grid / reel).

* `mnemonic` - **new, built for this video.** 128 coin flips settling into
  bits, the checksum, twelve numbers, twelve words. The library could not
  draw a number becoming a word.
* `diagram` - words, seed, private keys, addresses: the tree.
* `stat` - 39 digits, the size of the space.
* `grid` - the three ways a phrase is actually taken, with icons.

**Opener: `Stamp`** on the belief newcomers start with ("the wallet app
holds my coins"), stamped WRONG on "network". The last three long forms
opened Counter / Search / Counter. The verdict judges a claim, never an
asset.

**Footage: the act, in the subject's world** - a thumb on a lit phone,
hands writing in a notebook, a coin flipping on black, a photo gallery
scrolling, a safe's keypad, a support chat on a phone, a USB cable into a
laptop. All fetched fresh; verdicts in `footage.md`.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/seed-phrase.py
"""

import hashlib
import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot

from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Stamp

SOURCE_POST = "what-is-a-seed-phrase"
DEMAND = ("'what is a seed phrase' proven: CoinGecko 'What Is A SEED Phrase?? "
          "How It Is Generated' 11x (54k), CoinGecko 'Crypto Seed Phrases VS "
          "Private Keys' 11x (57k), Hipo Short 4.9x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Fetched fresh for this pair, contact-sheeted at 15/50/85%. Luma sampled at
# 0.5/3/6/9s.
THUMB = V / "typing-on-phone-dark-close-up/33942937.mp4"          # 15s, L11-14, a thumb over a lit phone in the dark - opens both cuts
PHONEHANDS = V / "typing-on-phone-dark-close-up/5925287.mp4"      # 10s, L30, hands with a phone over a laptop
CHAT = V / "typing-on-phone-dark-close-up/39494892.mp4"           # 27s, L34, a chat open on a phone - the fake support
WRITE = V / "hand-writing-notebook-close-up-night/39425741.mp4"   # 15s, L62, a hand writing in a notebook, close
NOTEBOOK = V / "hand-writing-notebook-close-up-night/6037421.mp4" # 22s, L49-59, a notebook by a candle; a face by 85%
QUILL = V / "pen-writing-paper-candlelight/11137423.mp4"          # 20s, L39, a pen on paper beside a candle
LAMP = V / "person-writing-list-desk-lamp-night/8631662.mp4"      # 13s, L42, a hand writing under a desk lamp
COIN = V / "coin-flip-slow-motion/30882814.mp4"                   # 6s, L1-3, a coin flipping on pure black
COINSPIN = V / "coin-flip-slow-motion/18977071.mp4"               # 17s, L37-67, a coin spinning down onto a table
GALLERY = V / "scrolling-photo-gallery-phone/6756650.mp4"         # 17s, L68, a thumb scrolling a photo grid
GALLERY2 = V / "scrolling-photo-gallery-phone/6756651.mp4"        # 22s, L40-52, a photo grid on a tablet, close
CAMERA = V / "smartphone-camera-close-up-dark/3649788.mp4"        # 32s, L19-63, a phone's camera in the dark
KEYPAD = V / "safe-vault-door-closing/6573544.mp4"                # 8s, L59-80, a hand on a safe's keypad
VAULT = V / "safe-vault-door-closing/39060937.mp4"                # 24s, L81-108, a key into a deposit box, then the empty box
LAPTOP = V / "phishing-email-laptop/39191965.mp4"                 # 37s, L16, hands on a laptop in the dark
DARKROOM = V / "laptop-login-screen-dark/36036732.mp4"            # 38s, L21-39, a laptop alone in a dark room
TYPING = V / "laptop-login-screen-dark/34771078.mp4"              # 14s, L21-25, hands typing, near black
KEYS = V / "laptop-login-screen-dark/5281595.mp4"                 # 9s, L28, fingers on a keyboard, close
SEARCH = V / "searching-google-laptop-night/6258096.mp4"          # 11s, L42, a figure at a screen of results
USB = V / "usb-device-plugged-into-laptop/40304895.mp4"           # 11s, L46-56, a cable into a laptop - the resold device
CANDLE = V / "pen-writing-paper-candlelight/12123578.mp4"         # 19s, L5-12, a typewriter by a candle - the disclaimer

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/what-is-a-seed-phrase"

# Fixed demo entropy, so the drawn phrase is a real, valid one and the same
# on every render: eternal elevator post slot file weapon exhibit more coin
# sister pelican kitten.
ENTROPY = hashlib.sha256(b"thecrypto.wiki seed phrase demo").hexdigest()[:32]


def _bip(s: str) -> tuple:
    """The caption says BIP39; the voice says "bip thirty-nine"."""
    return (s, s.replace("BIP39", "bip thirty-nine"))


SECTIONS = [
    # --- hook. No card. The Stamp lands on "network". ------------------------
    Section(
        title="What is a seed phrase?",
        card=False,
        sentences=[
            ("Your crypto is not inside your wallet app.",),
            ("It lives on the network, and twelve words decide who can move it.",),
            ("Lose the words, and the coins are gone for good.",
             "Show them to anyone, and the coins are theirs."),
            ("So how can twelve words hold a whole wallet, and why can't anyone guess them?",),
            ("Stay to the end for the three ways seed phrases really get stolen,",
             "because guessing is not one of them."),
        ],
        shots=[
            Shot(clip=THUMB, clip_at=1.0),
            Shot(clip=WRITE, clip_at=1.0),
            Shot(clip=LAMP, clip_at=1.0),
            Shot(clip=NOTEBOOK, clip_at=6.0),
            Shot(clip=KEYS, clip_at=1.0),
        ],
        gaps=[0.70, 0.80, 0.90, 0.80, 0.90],
    ),

    # --- what it is --------------------------------------------------------------
    Section(
        title="Is it just a password?",
        spoken_title="So is a seed phrase just a password?",
        kicker="THE MASTER KEY",
        sentences=[
            ("No. It is the backup a self-custody wallet shows you once, when you set it up.",),
            ("Twelve or twenty-four ordinary words, in order.",),
            ("A password unlocks the app on one phone.",
             "The seed phrase rebuilds the whole wallet, on any device."),
            ("There is no reset button, and no company to call.",),
            ("If you were never shown words like these, a company is holding your keys for you.",),
        ],
        shots=[
            Shot(clip=PHONEHANDS, clip_at=1.0),
            Shot(clip=WRITE, clip_at=7.0),
            Shot(clip=CHAT, clip_at=14.0),
            Shot(clip=KEYPAD, clip_at=0.5),
            Shot(clip=LAPTOP, clip_at=2.0),
        ],
        gaps=[0.60, 0.70, 0.70, 0.60, 0.90],
    ),

    # --- how the words are made ------------------------------------------------
    Section(
        title="How are the words made?",
        spoken_title="So how are the twelve words made?",
        kicker="THE COIN FLIPS",
        sentences=[
            ("It starts with chance, not with words.",),
            ("Your wallet flips a coin, a hundred and twenty-eight times.",),
            # the mnemonic's own sentence: one chunk per reveal.
            ("Each flip is one bit, a one or a zero.",
             "It adds four more bits as a checksum, and cuts the line into twelve groups of eleven.",
             "Each group is a number, from zero to two thousand and forty-seven.",
             "And each number picks one word, from a fixed list of two thousand and forty-eight."),
            (_bip("That list is a standard called BIP39, published in 2013,"),
             "so the same words work in almost any wallet."),
            ("The words are only a way to write that number down without a mistake.",),
        ],
        shots=[
            Shot(clip=COIN, clip_at=0.3),
            Shot(clip=COINSPIN, clip_at=5.0),
            Shot(graphic="mnemonic", backdrop=BEATGROUND,
                 payload=(ENTROPY, "TWELVE WORDS")),
            Shot(clip=QUILL, clip_at=1.0),
            None,
        ],
        gaps=[0.55, 0.60, 1.60, 0.70, 0.90],
    ),

    # --- what they unlock -------------------------------------------------------
    Section(
        title="What do the words unlock?",
        spoken_title="So what do those twelve words actually unlock?",
        kicker="THE KEY TREE",
        sentences=[
            ("Your wallet turns the words into one very long number, called the seed.",),
            # the diagram's own sentence: one chunk per box.
            ("Twelve words.",
             "One seed.",
             "From the seed, a whole tree of private keys.",
             "And from each key, an address that can receive coins."),
            ("One phrase can rebuild more than a million addresses, across Bitcoin, Ethereum and other coins.",),
            ("Lose the words, and you lose the whole tree at once.",),
        ],
        shots=[
            Shot(clip=DARKROOM, clip_at=1.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("Twelve words", "your backup", "\U0001F4DD"),
                           ("One seed", "a very long number", "\U0001F331"),
                           ("Private keys", "a whole tree of them", "\U0001F511"),
                           ("Addresses", "where coins arrive", "\U0001F4EC")],
                          "ONE PHRASE, EVERY KEY", False)),
            Shot(clip=GALLERY2, clip_at=2.0,
                 note=("1,000,000+", "addresses from one phrase")),
            Shot(clip=VAULT, clip_at=11.0),
        ],
        gaps=[0.60, 1.30, 0.70, 0.90],
    ),

    # --- the odds: the turn, so the card gets the longer silence -----------------
    Section(
        title="Can someone guess a seed phrase?",
        spoken_title="So can someone just guess one?",
        kicker="THE ODDS",
        card_gap=1.30,
        sentences=[
            ("Twelve words from a list of two thousand sounds easy to guess.",),
            ("Actually, it is a hundred and twenty-eight coin flips, and every one has to match.",),
            ("That makes the number of possible phrases thirty-nine digits long.",),
            ("Check a trillion phrases every second,",
             "and you would still need hundreds of millions of times the age of the universe."),
            ("Twenty-four words multiply that number by itself.",),
            ("So the math is not the weak point.",),
            ("As long as the wallet's randomness is real, nobody guesses twelve words.",),
        ],
        shots=[
            Shot(clip=KEYS, clip_at=3.5),
            Shot(clip=COINSPIN, clip_at=9.0),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("39", "digits", "in the number of possible phrases")),
            Shot(clip=DARKROOM, clip_at=14.0,
                 note=("1 TRILLION", "guesses a second, still not enough")),
            None,
            Shot(clip=TYPING, clip_at=1.0),
            Shot(clip=LAMP, clip_at=7.0),
        ],
        gaps=[0.85, 0.70, 0.80, 0.80, 0.60, 0.70, 0.90],
    ),

    # --- the real theft ------------------------------------------------------------
    Section(
        title="How do seed phrases get stolen?",
        spoken_title="So how do seed phrases actually get stolen?",
        kicker="THE REAL THEFT",
        sentences=[
            ("Almost every loss starts with a person, not with the math.",),
            # the grid's own sentence: one chunk per card.
            ("A photo of the words, on a phone that syncs to the cloud.",
             "A hardware wallet bought from a reseller, with the words already printed in the box.",
             "And a support page that looks like your wallet's, asking you to type them in."),
            ("Real wallet support will never ask for your seed phrase.",),
            ("And a phrase that has been on any screen, like the one in this video, is not a secret any more.",),
        ],
        shots=[
            Shot(clip=SEARCH, clip_at=1.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("A photo of the words", "synced to the cloud", "\U0001F4F8"),
                           ("A pre-printed card", "inside a resold device", "\U0001F4E6"),
                           ("A fake support page", "asking for your words", "\U0001F3A3")],
                          "HOW PHRASES ARE TAKEN")),
            Shot(clip=CHAT, clip_at=2.0),
            Shot(clip=GALLERY, clip_at=2.0),
        ],
        gaps=[0.60, 1.40, 0.80, 0.90],
    ),

    # --- keeping one ------------------------------------------------------------
    Section(
        title="How do you keep one safe?",
        spoken_title="So how do you keep one safe?",
        kicker="THE BACKUP",
        sentences=[
            ("Write the words by hand, in order, and keep two copies in two different places.",),
            ("Never photograph them, never type them into a website, and never keep them in a notes app.",),
            ("You can also add a passphrase, a twenty-fifth word you keep in your head.",),
            ("Without it, the twelve words open a different, empty wallet.",),
            ("But forget it, and nobody can get you back in.",),
        ],
        shots=[
            Shot(clip=NOTEBOOK, clip_at=1.0),
            Shot(clip=CAMERA, clip_at=1.0),
            Shot(clip=USB, clip_at=1.0),
            Shot(clip=VAULT, clip_at=1.0),
            Shot(clip=TYPING, clip_at=7.0),
        ],
        gaps=[0.60, 0.70, 0.55, 0.85, 0.90],
    ),

    # --- close: the echo ------------------------------------------------------
    Section(
        title="So what is a seed phrase?",
        spoken_title="So, what is a seed phrase?",
        kicker="THE ANSWER",
        sentences=[
            ("A hundred and twenty-eight coin flips, written down as twelve words.",),
            ("Nobody can guess them.",
             "So the only way in is through whoever holds the paper."),
            ("Nothing in this video is financial advice.",),
            ("So, where are your twelve words right now?",),
        ],
        shots=[
            Shot(clip=COIN, clip_at=0.2),
            Shot(clip=QUILL, clip_at=9.0),
            Shot(clip=CANDLE, clip_at=2.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=THUMB, clip_at=9.0),
        ],
        gaps=[0.80, 1.00, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is a Seed Phrase? How 12 Words Control Your Crypto",
    hook="Your crypto is not inside your wallet app - twelve words decide who "
         "can move it. Here is what a seed phrase is, how a wallet turns 128 "
         "coin flips into twelve words, what those words unlock, why nobody "
         "can guess one, and the three ways seed phrases really get stolen.",
    url=URL,
    summary="What a seed phrase is, explained: the 12 or 24 words a "
            "self-custody wallet shows you once, and why they are not a "
            "password; how BIP39 turns 128 random bits and a 4-bit checksum "
            "into twelve numbers and twelve words from a list of 2048; how one "
            "phrase derives a seed, a tree of private keys and over a million "
            "addresses; why guessing one is out of reach (the number of "
            "possible phrases is 39 digits long); the three ways phrases are "
            "actually taken - a photo synced to the cloud, a pre-printed card "
            "in a resold hardware wallet, a fake support page; and how to "
            "keep one safe, including the optional passphrase. The phrase "
            "shown in the video is a public demo - never use it. Nothing here "
            "is financial advice.",
    tags=["what is a seed phrase", "seed phrase explained", "seed phrase",
          "recovery phrase", "mnemonic phrase", "bip39", "bip39 explained",
          "can someone guess my seed phrase", "12 word seed phrase",
          "seed phrase vs private key", "crypto wallet security",
          "self custody", "hardware wallet", "crypto scams"],
    cta=f"How to back up your words, recover a wallet and plan for your family: {URL}",
    credits=["Nothing in this video is financial advice.",
             "The seed phrase shown is a public demo. Never send funds to it."],
)

HEADLINE = "How can\n12 words\nhold a\n[wallet?]"


def cover_frame():
    """The cover's picture: a hand writing with a nib by a candle - the act
    the video is about, writing the words down. Shared with the Short."""
    import io
    import subprocess
    from PIL import Image
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "6", "-i", str(QUILL),
                          "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png",
                          "-"], capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(raw)).convert("RGB")


def thumbs(out: Path) -> Path:
    """The hand and nib whole on the right, the video's own question (the
    hook's "how can twelve words hold a whole wallet?") in four rows on the
    dark left. The type sits on a shade over the candle side only - the hand
    is never faded (`thumbnails.md`). A person in the scene, not a drawn
    beat: `mnemonic` at 320px would be noise (2026-10-30)."""
    import numpy as np
    from PIL import Image, ImageEnhance
    from video_automation.longform import thumb as T
    im = cover_frame().resize((1280, 720), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(0.92)
    a = np.zeros((1, 1280), np.float32)
    a[0, :560] = 0.55
    a[0, 560:740] = np.linspace(0.55, 0.0, 180)
    shade = Image.fromarray((np.repeat(a, 720, 0) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, shade)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 190, int(680 / 1.38), 40, fill, ink,
                max_lines=4, leading=1.0, band="middle", margin=34,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/seed-phrase-long.mp4"
    work = Path.home() / "Desktop/.seed-phrase-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        # A belief to overturn. Last three long forms opened
        # Counter / Search / Counter.
        opener=Stamp("Your app holds your crypto", "WRONG", at_word="network"),
        emphasis=["rebuilds the whole wallet", "every one has to match", "a person",
                  "empty wallet"],
        thumb_headline=HEADLINE,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=10.5, title_hold=5.4,
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/seed-phrase-long-thumb.jpg"))
    else:
        main()
