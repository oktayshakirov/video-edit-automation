"""What is hidden inside Bitcoin's first block? ~45s crypto short.

Source: crypto-wiki/content/crypto-ogs/satoshi-nakamoto.mdx - the same bio as
the `satoshi-nakamoto` long form, written in the same pass.

**The single move.** The long form walks the whole profile. The Short does
one thing: block zero carries a newspaper headline, every block since chains
back to it, and its fifty coins can never be spent. It closes cold on a line
that recontextualises the opening question. No disclaimer (the long carries it).

**Beats:** `chapter` (the headline itself), `diagram` (the chain back to
block zero), `chapter` to close. Clips are the long form's roster.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/satoshi-nakamoto.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.thumb import render_short_thumb

SOURCE_POST = "satoshi-nakamoto"

V = STOCK / "videos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

LEDGER = V / "digital-ledger-blocks-chain-dark/34127877.mp4"
LEDGER2 = V / "digital-ledger-blocks-chain-dark/34128900.mp4"
COINS = V / "coins-falling-slow-motion-dark/39108087.mp4"
KEYS = V / "typing-keyboard-night/8212370.mp4"
TYPING = V / "hand-typing-laptop-keyboard-dark-night/34771078.mp4"
NEWS = V / "woman-reading-newspaper-dark-serious/7592929.mp4"
BANK = V / "printing-money-banknotes-machine/39061007.mp4"
PADLOCK = V / "padlock-metal-lock-macro-dark/10241357.mp4"
DRIVE = V / "old-hard-drive-data-storage-dark/19285752.mp4"

SATOSHI = SITE_IMAGES / "posts/satoshi-nakamoto.jpg"
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

HEADLINE = "CHANCELLOR ON BRINK OF SECOND BAILOUT FOR BANKS"
CLOSE = "BITCOIN STARTED WITH A HEADLINE."

SENTENCES = [
    # The title question.
    ("What is hidden inside Bitcoin's very first block?",),
    # The payoff, sentence two.
    ("A line from a newspaper's front page.",),
    ("Satoshi Nakamoto mined that block",
     "on the third of January, two thousand nine."),
    # Hinge into the headline card.
    ("And typed this into it, word for word.",),
    ((HEADLINE, "Chancellor on brink of second bailout for banks."),),
    ("The Times ran it that morning,",
     "in the middle of the banking crisis."),
    ("So the block could not have been made any earlier.",),
    # Hinge into the diagram.
    ("And every block since is chained back to it.",),
    # The diagram's own sentence - one chunk per node.
    ("Block zero holds the headline,",
     "block one points back to it,",
     "and every block after points to the one before."),
    ("The fifty bitcoins in block zero can never be spent.",),
    ("They sit there to this day,",
     "right next to the headline."),
    # Cold close, recontextualising the opener.
    ((CLOSE, "Bitcoin started with a headline."),),
]

SHOTS = [
    Shot(clip=LEDGER, clip_at=0.5),
    Shot(clip=COINS, clip_at=1.0),
    Shot(clip=KEYS, clip_at=1.0),
    Shot(clip=TYPING, clip_at=1.0),
    Shot(graphic="chapter", payload=(HEADLINE,)),
    Shot(clip=NEWS, clip_at=3.0),
    Shot(clip=BANK, clip_at=2.0),
    Shot(clip=LEDGER2, clip_at=1.0),
    Shot(graphic="diagram", backdrop=BEATGROUND,
         payload=([("Block 0", "the headline", "📰"),
                   ("Block 1", "points back", "🔗"),
                   ("Every block since", "the same chain", "⛓️")],
                  "ONE CHAIN, ONE START")),
    Shot(clip=PADLOCK, clip_at=2.0),
    Shot(clip=DRIVE, clip_at=1.0),
    Shot(graphic="chapter", payload=(CLOSE,)),
]

GAPS = [0.70, 0.70, 0.55, 0.45, 1.20, 0.55, 0.70, 0.45, 1.10, 0.60, 0.70, 1.30]


def main() -> None:
    out = Path.home() / "Desktop/crypto-satoshi-nakamoto-short.mp4"
    work = Path.home() / "Desktop/.crypto-satoshi-nakamoto-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
        karaoke_box=False, karaoke_upper=False,  # approved before box became default
                                     voice=VOICE, gap=GAPS,
                                     music=MUSIC, music_gain=0.85)
    # Same headline as the long form - a pair shares its thumbnail.
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "Who is [Satoshi?]",
        image=SATOSHI, accent="yellow", band="top")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
