"""What is real world asset tokenization? - long-form 16:9 for YouTube.

Source: crypto-wiki/content/posts/real-world-asset-tokenization.mdx.

**The angle.** The article is a primer plus an evaluation checklist that names
exchanges and funds. None of the "how to get started" half goes in: it is a
platform recommendation by another name. What survives is the mechanism and
its one honest twist - a token is a claim, not the asset, and the blockchain
can see the claim and nothing behind it.

**No financial advice, anywhere.** No fund, issuer, exchange, price or
direction is named. The $12M building is the article's own worked example,
said as an example.

## The beats

Checked against the last three crypto long-forms (miners-ai: grid / bars /
stat / compare / checklist; fear-greed: dial / bars / diagram / quote /
checklist; rug-pull: diagram / grid / gauge / steps / stat):

* `split` (new) - one building divided into 120,000 tokens
* `diagram` - asset -> legal wrapper -> custodian -> token
* `steps` - a token's life: approved wallets, rent, trading, redemption
* `compare` - what the chain can see against what it cannot
* `grid` - the four kinds of risk

`split` was built for this video: the subject is a *division*, and nothing
in the library could draw one. See `beats.md`.

Clips are hands, paperwork, buildings and a vault - no faces. The site's two
images for this post measure L156-161 and are unusable.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-long/rwa-tokenization.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "real-world-asset-tokenization"

V = STOCK / "videos"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

TOWER = V / "office-tower-night-exterior/7316618.mp4"              # 9.8s, a lit office tower at dusk
APT = V / "apartment-building-windows-night/9431584.mp4"           # 10.7s, lit windows of a block
TOWER_UP = V / "skyscraper-looking-up-night/38802916.mp4"          # 8.7s, looking up a dark tower
TOWERS = V / "skyscraper-looking-up-night/11661545.mp4"            # 21.7s, towers from street level
CITY = V / "office-windows-night-city-lights/28872822.mp4"         # 27.9s, a city from a high window
GOLD = V / "gold-bars-vault/34961721.mp4"                          # 30.0s, gold bars (rendered)
PHONE1 = V / "smartphone-crypto-wallet-hand-dark/7534329.mp4"      # 14.7s, hands on a phone, dark
PHONE2 = V / "smartphone-crypto-wallet-hand-dark/7534328.mp4"      # 16.2s, hands on a phone, dark
SIGN1 = V / "hand-writing-signature-pen-dark/5923409.mp4"          # 10.3s, a hand signing papers
SIGN2 = V / "person-signing-document-desk-dark/8731513.mp4"        # 15.6s, papers signed across a desk
CASH = V / "hand-counting-cash-dark/34579096.mp4"                  # 16.6s, hands counting notes
SERVER = V / "server-rack-lights-dark-close/7140931.mp4"           # 9.2s, a server front, blue
HALL = V / "bank-vault-door-opening/37410272.mp4"                  # 22.5s, a bank hall interior
LAW = V / "government-building-columns-night/34539253.mp4"         # 16.7s, columned building, night
CLOCK = V / "clock-night-dark/8322155.mp4"                         # 24.5s, a hand turning a clock

BEATGROUND = BRAND / "beat-ground-crypto.jpg"
THUMB = BRAND / "graphics/rwa-tower.jpg"                           # frame 3s of TOWER
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://thecrypto.wiki/posts/real-world-asset-tokenization"


SECTIONS = [
    # --- hook. No card. The reversal is sentence two. -----------------------
    Section(
        title="A slice of a building",
        card=False,
        sentences=[
            ("You can own a hundred dollars of an office building.",),
            ("Not a share of a fund -",
             "a token, in a wallet, that you can send at midnight."),
            ("That is real world asset tokenization.",),
            ("But the token is not the building.",),
            ("Stay to the end,",
             "and you will know exactly what that token gives you -",
             "and where it can break."),
        ],
        shots=[
            Shot(clip=TOWER, clip_at=0.5),
            Shot(clip=PHONE1, clip_at=1.0),
            Shot(clip=TOWERS, clip_at=1.0),
            Shot(clip=TOWER_UP, clip_at=0.3),
            Shot(clip=SIGN1, clip_at=1.0),
        ],
        gaps=[0.60, 0.85, 0.60, 0.95, 0.85],
    ),

    # --- what it is ---------------------------------------------------------
    Section(
        title="What is real world asset tokenization?",
        spoken_title="So what is real world asset tokenization?",
        sentences=[
            ("It turns a claim on something real",
             "into a token on a blockchain."),
            # the split's own sentence - two chunks, whole then parts.
            ("Take one building, worth twelve million dollars,",
             "and split it into a hundred and twenty thousand tokens, "
             "at a hundred dollars each."),
            ("The same trick works for government bonds,",
             "for gold in a vault,",
             "even for music royalties."),
            ("Something that used to need a hundred thousand dollars to "
             "enter",
             "can now be bought in slices."),
        ],
        shots=[
            Shot(clip=APT, clip_at=1.0),
            Shot(graphic="split", backdrop=BEATGROUND,
                 payload=("ONE BUILDING", "$12 million",
                          "120,000 TOKENS", "$100 each",
                          "ONE ASSET, MANY OWNERS")),
            Shot(clip=GOLD, clip_at=2.0),
            Shot(clip=CASH, clip_at=1.0),
        ],
        gaps=[0.60, 1.30, 0.60, 0.85],
    ),

    # --- how: the chain of paperwork ----------------------------------------
    Section(
        title="How does a building become a token?",
        spoken_title="But how does a building actually become a token?",
        sentences=[
            ("A blockchain cannot hold a deed.",
             "So the building goes through a chain of paperwork first."),
            # the diagram's own sentence - one chunk per node.
            ("First, the building itself.",
             "A company is set up only to own it,",
             "a custodian keeps the legal title safe,",
             "and the token is your claim on that company."),
            ("Lawyers call that company a special purpose vehicle.",
             "Its only job is to own the one asset."),
        ],
        shots=[
            Shot(clip=SIGN2, clip_at=1.0),
            Shot(graphic="diagram", backdrop=BEATGROUND,
                 payload=([("The building", "worth $12 million", "🏠"),
                           ("A company that owns it", "the legal wrapper", "📜"),
                           ("A custodian", "holds the title", "🔐"),
                           ("Your token", "a claim on the company", "🎫")],
                          "FROM BUILDING TO TOKEN")),
            Shot(clip=HALL, clip_at=2.0),
        ],
        gaps=[0.70, 1.20, 0.85],
    ),

    # --- why a blockchain at all --------------------------------------------
    Section(
        title="Why put it on a blockchain?",
        spoken_title="So why put any of this on a blockchain?",
        sentences=[
            ("Because the rules can travel with the token.",),
            ("Here is what a token does over its life.",),
            # the steps' own sentence - one chunk per node.
            ("It can only be sent to approved wallets,",
             "the rent is paid out to every holder,",
             "it can change hands at any hour,",
             "and at the end, it is redeemed for its share of the sale."),
            ("A traditional trade can take a day or more to settle.",
             "A token can settle in minutes."),
        ],
        shots=[
            Shot(clip=SERVER, clip_at=0.5),
            Shot(clip=PHONE2, clip_at=1.0),
            Shot(graphic="steps", backdrop=BEATGROUND,
                 payload=([("Approved wallets only", "🔒"),
                           ("Rent paid to holders", "💰"),
                           ("Trades at any hour", "🌙"),
                           ("Redeemed at the end", "🏁")],
                          "A TOKEN'S LIFE")),
            Shot(clip=CLOCK, clip_at=2.0),
        ],
        gaps=[0.60, 0.55, 1.10, 0.85],
    ),

    # --- twist: what the chain can and cannot see ---------------------------
    Section(
        title="What does the blockchain actually know?",
        spoken_title="But what does the blockchain actually know?",
        sentences=[
            ("Less than it looks like.",),
            # the compare's own sentence - 2 headings + 3 + 3 = 8 chunks.
            ("Start with what the chain can see.",
             "Who holds each token,",
             "how many exist,",
             "and every single transfer.",
             "Now compare that with what it cannot.",
             "Whether the building exists,",
             "who really holds the title,",
             "and whether the rent was ever paid."),
            ("Everything on the right lives in paperwork, audits and courts.",),
            ("The token proves you own a slice.",
             "The paperwork decides what the slice is."),
        ],
        shots=[
            Shot(clip=CITY, clip_at=1.0),
            Shot(graphic="compare", backdrop=BEATGROUND,
                 payload=("ON-CHAIN",
                          ["Who holds tokens",
                           "How many exist",
                           "Every transfer"],
                          "OFF-CHAIN",
                          ["The building exists",
                           "Who holds the title",
                           "Rent was paid"],
                          True)),
            Shot(clip=LAW, clip_at=1.0),
            Shot(clip=SIGN2, clip_at=8.0),
        ],
        gaps=[0.85, 1.10, 0.70, 0.90],
    ),

    # --- risks, the echo, the ask -------------------------------------------
    Section(
        title="What can still go wrong?",
        spoken_title="So what can still go wrong?",
        sentences=[
            ("Putting an asset on a blockchain does not remove its risks.",
             "It adds some."),
            # the grid's own sentence - one chunk per card.
            ("The asset can lose value,",
             "the law can change,",
             "the company or custodian can fail,",
             "and the code or the keys can break."),
            ("A token can settle in minutes.",
             "A building still sells like a building."),
            ("Nothing in this video is financial advice.",),
            ("So if someone handed you a token for a slice of a building -",
             "would you check the blockchain, or the paperwork?"),
        ],
        shots=[
            Shot(clip=TOWERS, clip_at=12.0),
            Shot(graphic="grid", backdrop=BEATGROUND,
                 payload=([("Market risk", "the asset loses value", "🔻"),
                           ("Legal risk", "the rules change", "📜"),
                           ("Counterparty risk", "the issuer or custodian fails", "🚨"),
                           ("Technology risk", "code, oracles or keys break", "🔑")],
                          "WHERE IT CAN BREAK")),
            Shot(clip=PHONE1, clip_at=6.0),
            Shot(clip=GOLD, clip_at=16.0,
                 payload=("", "This is not financial advice.")),
            Shot(clip=HALL, clip_at=12.0),
        ],
        gaps=[0.60, 1.20, 0.85, 1.10, 2.30],
    ),
]

META = Meta(
    title="What Is Real World Asset Tokenization?",
    hook="You can own a hundred dollars of an office building as a token - "
         "but the token is not the building. Here is how real world asset "
         "tokenization works, what the blockchain can and cannot see, and "
         "where it can break.",
    url=URL,
    summary="What real world asset tokenization is: turning a claim on a "
            "building, a bond, gold or royalties into a token on a "
            "blockchain. How a building becomes 120,000 tokens through a "
            "legal wrapper and a custodian, what a token does over its life, "
            "why settlement is faster, what the blockchain can and cannot "
            "verify, and the four kinds of risk: market, legal, counterparty "
            "and technology. Nothing here is financial advice.",
    tags=["real world asset tokenization", "what is rwa tokenization",
          "rwa crypto explained", "tokenized real estate",
          "tokenization explained", "real world assets blockchain",
          "tokenized treasuries", "fractional ownership crypto",
          "special purpose vehicle token", "rwa tokens"],
    cta=f"The full guide - how it works, the risks and the legal side: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: oosongoo, via Pixabay.",
             "Nothing in this video is financial advice."],
)


def main() -> None:
    out = Path.home() / "Desktop/crypto-rwa-tokenization-long.mp4"
    work = Path.home() / "Desktop/.crypto-rwa-tokenization-long-work"
    made = render_long(
        SECTIONS, out, work, brand=CRYPTO, meta=META, voice=VOICE,
        music=MUSIC,
        callouts=None,
        thumb_headline="$100 of a [building?]",
        thumb_image=THUMB,
        thumb_accent="yellow",
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
