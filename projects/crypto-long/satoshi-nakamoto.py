"""Who is Satoshi Nakamoto? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/crypto-ogs/satoshi-nakamoto.mdx.

**The angle.** `satoshi-proof` already covers what would count as proof. This
one is the profile the bio page is: what Satoshi published, what is inside
block zero, the two-year fade-out, the coins that never moved, and the
candidates - each dismissed in turn (the OG genre's evidence-list device,
`projects/crypto.md`), resolving on the one proof nobody has produced.

**No financial advice.** No price, no dollar value of the coins, no direction.
The million-coin figure is said as an estimate, as the article says it.

## The beats

Last three crypto long-forms: rwa (split / diagram / steps / compare / grid),
miners-ai (grid / bars / stat / compare / checklist), fear-greed (dial / bars /
diagram / quote / checklist).

* `quote` - the genesis block headline
* `steps` - 2008 to 2011, whitepaper to last email
* `split` - ~1M BTC as ~20,000 rewards of 50
* `checklist` (flow) - the candidates, each struck
* `stat` - block zero's unspendable 50

Clips are hands, papers, drives, a ledger, one figure walking away - the
subject has no photograph, so nobody stands in for him.

    PYTHONPATH=. .venv/bin/python projects/crypto-long/satoshi-nakamoto.py

**Phonemes.** `Szabo` reads SHAH-bo; spoken as `Sahbo`. `Hearn` avoided.
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "satoshi-nakamoto"

V = STOCK / "videos"
POSTS = SITE_IMAGES / "posts"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

WALK = V / "man-walking-alone-night-street-dark/11792115.mp4"            # 21.8s, figure walks off into fog
TYPING = V / "hand-typing-laptop-keyboard-dark-night/34771078.mp4"        # 13.7s, hands on a laptop, dark
KEYS = V / "typing-keyboard-night/8212370.mp4"                            # 12.2s, a hand on a keyboard
PAPERS = V / "research-papers-desk-lamp-night-dark/30117914.mp4"          # 14.6s, papers and a typewriter
WRITER = V / "research-papers-desk-lamp-night-dark/7062990.mp4"           # 14.4s, man writing at night
FORUM = V / "scrolling-forum-posts-laptop-screen-dark-night/8311535.mp4"  # 23.7s, man reading a forum
LEDGER = V / "digital-ledger-blocks-chain-dark/34127877.mp4"              # 20.0s, ledger rings of figures
LEDGER2 = V / "digital-ledger-blocks-chain-dark/34128900.mp4"             # 20.0s, a field of data blocks
CODE = V / "code-scrolling-screen-terminal-dark/34268861.mp4"             # 18.3s, code on a screen
DRIVE = V / "old-hard-drive-data-storage-dark/19285752.mp4"               # 24.9s, an open hard drive
COINS = V / "coins-falling-slow-motion-dark/39108087.mp4"                 # 12.1s, coins onto a newspaper
BANK = V / "printing-money-banknotes-machine/39061007.mp4"                # 23.0s, banknotes counted
PADLOCK = V / "padlock-metal-lock-macro-dark/10241357.mp4"                # 20.7s, a padlock on black
MAGNIFY = V / "magnifying-glass-document-dark-macro/6980366.mp4"          # 30.0s, a glass over a note
NEWS = V / "woman-reading-newspaper-dark-serious/7592929.mp4"             # 15.1s, reading a newspaper
CLOSE = V / "laptop-closing-screen-dark-night/7272375.mp4"                # 19.6s, a laptop shut at night
DARKLAP = V / "laptop-closing-screen-dark-night/13375774.mp4"             # 29.6s, a silhouette at a laptop
RAIN = V / "rain-window-night-dark-slow/15161525.mp4"                     # 16.0s, rain on a window

SATOSHI = POSTS / "satoshi-nakamoto.jpg"                                  # 1200x675, L43 - the bookend
BEATGROUND = BRAND / "beat-ground-crypto.jpg"
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/crypto-ogs/satoshi-nakamoto"
A = 16 / 9


SECTIONS = [
    # --- hook. No card. ------------------------------------------------------
    Section(
        title="Nobody knows who invented Bitcoin",
        card=False,
        sentences=[
            ("The person who invented Bitcoin has never been identified.",),
            ("No face, no voice, no real name.",),
            ("Just a pen name - Satoshi Nakamoto.",),
            ("And about a million bitcoins that have never moved.",),
            ("Stay to the end,",
             "and you will know what Satoshi left behind -",
             "and why nobody has proved who it was."),
        ],
        shots=[
            Shot(clip=WALK, clip_at=0.5),
            Shot(clip=TYPING, clip_at=1.0),
            Shot(image=SATOSHI, zoom=1.08, pan=(0.02, 0.0), aspect=A, bias=0.4),
            Shot(clip=DRIVE, clip_at=1.0),
            Shot(clip=LEDGER, clip_at=1.0),
        ],
        gaps=[0.60, 0.70, 0.85, 0.95, 0.85],
    ),

    # --- the whitepaper ------------------------------------------------------
    Section(
        title="Where did Bitcoin come from?",
        spoken_title="So where did Bitcoin actually come from?",
        sentences=[
            ("In October two thousand eight,",
             "a nine-page paper appeared on a cryptography mailing list."),
            ("It was signed Satoshi Nakamoto,",
             "and it described digital cash with no bank in the middle."),
            ("Money sent straight from one person to another,",
             "with a shared public record of every payment."),
            ("That record is the blockchain.",
             "And somebody had to start it."),
        ],
        shots=[
            Shot(clip=PAPERS, clip_at=1.0),
            Shot(clip=WRITER, clip_at=1.0),
            Shot(clip=LEDGER2, clip_at=1.0),
            Shot(clip=CODE, clip_at=1.0),
        ],
        gaps=[0.60, 0.70, 0.60, 0.85],
    ),

    # --- block zero ----------------------------------------------------------
    Section(
        title="What is inside the first block?",
        spoken_title="So what is inside the very first block?",
        sentences=[
            ("On the third of January, two thousand nine,",
             "Satoshi mined block zero - the genesis block."),
            ("Hidden inside it is one line of text,",
             "copied from that day's front page of The Times."),
            # the quote's own sentence
            ("Chancellor on brink of second bailout for banks.",),
            ("It works as a timestamp -",
             "and it reads like a note on why Bitcoin was built."),
            ("One more detail.",
             "The fifty bitcoins from that block can never be spent."),
        ],
        shots=[
            Shot(clip=LEDGER, clip_at=10.0),
            Shot(clip=COINS, clip_at=1.0),
            Shot(graphic="quote", backdrop=BEATGROUND,
                 payload=("Chancellor on brink of second bailout for banks.",
                          "The Times, 3 January 2009 - inside block zero")),
            Shot(clip=BANK, clip_at=2.0),
            Shot(graphic="stat", backdrop=BEATGROUND,
                 payload=("50 BTC", "BLOCK ZERO",
                          "The code never counts them. They cannot be spent.")),
        ],
        gaps=[0.60, 0.85, 1.20, 0.70, 0.90],
    ),

    # --- the fade-out --------------------------------------------------------
    Section(
        title="How did Satoshi disappear?",
        spoken_title="Then how did Satoshi disappear?",
        sentences=[
            ("Slowly, and in public.",
             "For two years, Satoshi wrote code",
             "and answered questions on a forum called BitcoinTalk."),
            ("Nine days after the genesis block,",
             "Satoshi sent ten bitcoins to a cryptographer named Hal Finney -",
             "the first Bitcoin transaction between two people."),
            ("Here is how the rest of it played out.",),
            # the steps' own sentence - one chunk per node.
            ("October two thousand eight, the whitepaper.",
             "January two thousand nine, the genesis block.",
             "Twenty ten, the code is handed to Gavin Andresen.",
             "April twenty eleven, the last known email."),
            ("That email said:",
             "I've moved on to other things."),
            ("After that, the name never wrote again.",),
        ],
        shots=[
            Shot(clip=FORUM, clip_at=1.0),
            Shot(clip=KEYS, clip_at=1.0),
            Shot(clip=PADLOCK, clip_at=2.0),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 payload=([("2008 - the whitepaper", "📄"),
                           ("2009 - the genesis block", "🧱"),
                           ("2010 - handed to Gavin Andresen", "🤝"),
                           ("2011 - the last email", "✉️")],
                          "HOW SATOSHI STEPPED AWAY")),
            Shot(clip=CLOSE, clip_at=1.0),
            Shot(clip=WALK, clip_at=12.0),
        ],
        gaps=[0.70, 0.85, 0.45, 1.10, 0.90, 0.90],
    ),

    # --- the coins -----------------------------------------------------------
    Section(
        title="What did Satoshi leave behind?",
        spoken_title="So what did Satoshi leave behind?",
        sentences=[
            ("A mountain of coins, mined in Bitcoin's first year.",),
            # the split's own sentence - whole, then parts.
            ("About one million bitcoins,",
             "spread over roughly twenty thousand block rewards, "
             "fifty coins each."),
            ("Researchers traced them by a pattern in the early blocks,",
             "so the figure is an estimate, not a confirmed balance."),
            ("And apart from that first payment to Hal Finney,",
             "not one of those coins has ever moved."),
        ],
        shots=[
            Shot(clip=DRIVE, clip_at=12.0),
            Shot(graphic="split", backdrop=BEATGROUND,
                 payload=("ONE MILLION BTC", "mined in year one",
                          "~20,000 REWARDS", "50 BTC each",
                          "THE SATOSHI COINS")),
            Shot(clip=MAGNIFY, clip_at=2.0),
            Shot(clip=LEDGER2, clip_at=10.0),
        ],
        gaps=[0.60, 1.30, 0.70, 0.95],
    ),

    # --- the candidates, the echo, the ask -----------------------------------
    Section(
        title="So who is Satoshi Nakamoto?",
        spoken_title="So who is Satoshi Nakamoto?",
        sentences=[
            ("Plenty of names have been put forward.",
             "Not one has held up."),
            # the checklist's own sentence - one chunk per name, flow marks.
            ("Hal Finney, who denied it before he died in twenty fourteen.",
             (("Nick Szabo, who designed Bit Gold, and denies it.",
               "Nick Sahbo, who designed Bit Gold, and denies it.")),
             "Dorian Nakamoto, named by Newsweek, who says he had no part in it.",
             "And a secret group, which nobody has shown either."),
            ("None of them has produced the one proof that would count -",
             "a message signed with the keys to those early coins."),
            ("So Satoshi is still exactly what the paper said.",
             "A name."),
            ("Nothing in this video is financial advice.",),
            ("The code is public, and the coins are in plain sight.",
             "So would you want Satoshi to be found?"),
        ],
        shots=[
            Shot(clip=NEWS, clip_at=3.0),
            Shot(graphic="checklist", backdrop=BEATGROUND,
                 payload=([("Hal Finney", False),
                           ("Nick Szabo", False),
                           ("Dorian Nakamoto", False),
                           ("A secret group", False)],
                          "PROVEN SATOSHI?", True)),
            Shot(clip=CODE, clip_at=9.0),
            Shot(image=SATOSHI, zoom=1.16, pan=(-0.02, 0.01), aspect=A, bias=0.4),
            Shot(clip=RAIN, clip_at=2.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=DARKLAP, clip_at=5.0),
        ],
        gaps=[0.70, 1.20, 0.85, 1.00, 1.10, 2.30],
    ),
]

META = Meta(
    title="Who Is Satoshi Nakamoto? The Creator of Bitcoin",
    hook="The person who invented Bitcoin has never been identified. Here is "
         "what Satoshi Nakamoto published, what is hidden inside Bitcoin's "
         "first block, how Satoshi disappeared, and why no candidate has "
         "ever been proven.",
    url=URL,
    summary="Who Satoshi Nakamoto is, as far as the record goes: the 2008 "
            "Bitcoin whitepaper, the genesis block and the Times headline "
            "inside it, the first transaction to Hal Finney, the handover to "
            "Gavin Andresen and the last email in 2011, the estimated one "
            "million bitcoins that have never moved, and why Hal Finney, "
            "Nick Szabo and Dorian Nakamoto remain unproven. Nothing here is "
            "financial advice.",
    tags=["satoshi nakamoto", "who is satoshi nakamoto",
          "bitcoin creator", "who invented bitcoin", "genesis block",
          "bitcoin whitepaper", "satoshi coins", "hal finney",
          "nick szabo", "bitcoin history"],
    cta=f"The full Satoshi Nakamoto profile - timeline, wallets and theories: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-satoshi-nakamoto-long.mp4"
    work = Path.home() / "Desktop/.crypto-satoshi-nakamoto-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        thumb_headline="Who is [Satoshi?]",
        thumb_image=SATOSHI,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
