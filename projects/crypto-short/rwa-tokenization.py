"""Can you really own $100 of a building? ~45s crypto short.

Source: crypto-wiki/content/posts/real-world-asset-tokenization.mdx
- the same post as the `rwa-tokenization` long-form, written in the same pass.

**The single move.** The long form walks the definition, the paperwork, a
token's life, what the chain can see and the risks. The Short does the one
thing all of that sets up: yes, you can own a slice - but what you own is a
claim on a company, not the building. It closes cold on that, answering its
own opening question. No disclaimer (the long form carries it).

No fund, issuer, exchange, price or direction is named.

**Beats:** `split` (the building divided), `diagram` (the chain of
paperwork), `chapter` to close. Clips come from the long form's roster.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/rwa-tokenization.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb

SOURCE_POST = "real-world-asset-tokenization"

V = STOCK / "videos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

TOWER = V / "office-tower-night-exterior/7316618.mp4"
TOWER_UP = V / "skyscraper-looking-up-night/38802916.mp4"
APT = V / "apartment-building-windows-night/9431584.mp4"
PHONE2 = V / "smartphone-crypto-wallet-hand-dark/7534328.mp4"
SIGN1 = V / "hand-writing-signature-pen-dark/5923409.mp4"
LAW = V / "government-building-columns-night/34539253.mp4"
CASH = V / "hand-counting-cash-dark/34579096.mp4"
SERVER = V / "server-rack-lights-dark-close/7140931.mp4"
CITY = V / "office-windows-night-city-lights/28872822.mp4"

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
THUMB = BRAND / "graphics/rwa-tower.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question.
    ("Can you really own a hundred dollars of a building?",),
    # The payoff, sentence two.
    ("Yes -",
     "but what you own is not the building."),
    ("You own a token,",
     "and the token is a claim."),
    # Hinge into the split, its own sentence.
    ("Here is how the split works.",),
    # The split's own sentence - two chunks, whole then parts.
    ("One building, worth twelve million dollars,",
     "cut into a hundred and twenty thousand tokens, a hundred dollars each."),
    ("But a blockchain cannot hold a deed.",),
    # Hinge into the diagram.
    ("So the building sits behind a chain of paperwork.",),
    # The diagram's own sentence - one chunk per node.
    ("A company is set up to own it,",
     "a custodian holds the title,",
     "and your token is a claim on that company."),
    ("The rent comes back down the same chain,",
     "to your wallet."),
    ("The blockchain proves you hold the token.",),
    ("Only the paperwork proves there is a building behind it.",),
    # Cold close, answering the opening question.
    (("YOU OWN THE CLAIM. NOT THE BUILDING.",
      "You own the claim. Not the building."),),
]

SHOTS = [
    Shot(clip=TOWER, clip_at=0.5),
    Shot(clip=TOWER_UP, clip_at=0.3),
    Shot(clip=PHONE2, clip_at=3.0),
    Shot(clip=APT, clip_at=1.0),
    Shot(graphic="split", backdrop=BEATGROUND,
         payload=("ONE BUILDING", "$12 million",
                  "120,000 TOKENS", "$100 each",
                  "ONE ASSET, MANY OWNERS")),
    Shot(clip=SIGN1, clip_at=2.0),
    Shot(clip=LAW, clip_at=3.0),
    Shot(graphic="diagram", backdrop=BEATGROUND,
         payload=([("A company owns it", "the legal wrapper", "📜"),
                   ("A custodian", "holds the title", "🔐"),
                   ("Your token", "a claim on the company", "🎫")],
                  "WHAT YOU ACTUALLY OWN")),
    Shot(clip=CASH, clip_at=6.0),
    Shot(clip=SERVER, clip_at=0.5),
    Shot(clip=CITY, clip_at=10.0),
    Shot(graphic="chapter",
         payload=("YOU OWN THE CLAIM. NOT THE BUILDING.",)),
]

GAPS = [0.70, 0.60, 0.55, 0.45, 1.20, 0.60, 0.45, 1.10, 0.60, 0.50, 0.70, 1.30]


def main() -> None:
    out = Path.home() / "Desktop/crypto-rwa-tokenization-short.mp4"
    work = Path.home() / "Desktop/.crypto-rwa-tokenization-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, gap=GAPS,
                                     music=MUSIC, music_gain=0.85)
    # Same headline as the long form - a pair shares its thumbnail.
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "$100 of a [building?]",
        image=THUMB, accent="yellow", band="top")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
