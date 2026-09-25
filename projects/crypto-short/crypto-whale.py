"""Who is the biggest Bitcoin whale? ~48s crypto short.

Source: crypto-wiki/content/posts/what-is-a-crypto-whale.mdx - the same post
as the `crypto-whale` long form, written in the same pass.

**The angle, and why it is not the obvious one.** The obvious whale short -
*can a whale move the price?* - is already shipped as `bitcoin-price-short`,
which defines the thousand-coin threshold, walks the thin order book and
closes on "stop watching whale wallets". Repeating it would argue against a
video already on the channel. So this pair takes the half of the article that
video never touched: the taxonomy, and specifically the **exchange/custodian**
row in it. The biggest wallets on any chain are custodial, so the coins in
them belong to customers, and a whale-alert feed is mostly watching a company
move its own inventory.

**The single move.** The long form walks the five kinds of holder, the
thresholds and how to read a transfer. The Short does the one thing those
chapters rest on: the biggest whale is not a person, it is a warehouse.

**Opener: `Stamp`, not the redacted hook.** The topic is a *belief to
overturn* - "the biggest whale is some early adopter with a cold wallet" -
which is precisely the shape `Stamp` exists for, and the last three shorts on
this channel ran the redacted hook or nothing. The verdict lands on the word
"exchange" in sentence 2, at roughly 4.3s.

**Sentence 2 is a partial answer, not the verdict** (`narration.md`, revised
2026-09-21): "it is an exchange, and almost none of those coins are its own"
is new, true and opens the bigger question - so whose are they, and what is a
whale then? - rather than closing the loop at five seconds.

**Two beats, two silhouettes, neither one the last three shorts used.**
`split` (the custodian address divided into customer claims) and `steps` (the
life of a whale alert, down the frame). crypto-scams ran `grid`, vitalik ran
`checklist`, satoshi ran `diagram`.

**Cold close, no question** (`narration.md`, "A Short's ending loops"). The
last line recontextualises the opening question rather than re-asking it, and
`outro=` holds it to the final frame so the piece loops into its own first
frame.

**No disclaimer** - the long form carries it, and shorts on this channel drop
it. **No financial advice:** no price, no level, no prediction, and no
exchange is named, rated or recommended. Every figure is structural - "a
thousand bitcoin" is the article's own definition and "tens of thousands of
coins" is a hypothetical - so nothing here can date.

**Clips** are the long form's roster, each used exactly once here. No live
price, chart, ticker or broker name appears in any of them: the two obvious
candidates in the cache (`woman-trader-desk-dark-office-night`,
`spreadsheet-rows-screen-dark-night`) are both a lit candlestick chart with a
broker's name on it, and both were rejected on the contact sheet.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/crypto-whale.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp
from video_automation.longform.thumb import render_short_thumb

SOURCE_POST = "what-is-a-crypto-whale"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Screened across their length, not at one frame - the trailing comment is the
# luma/saturation range over the whole clip, and every one was then looked at
# on a labelled contact sheet. Four cache clips that passed the luma box were
# cut on the sheet: `safe-deposit-box-vault-dark-interior` is a delivery van,
# `storage-lockers-corridor-dark` is a hooded figure against a pink wall,
# `crowd-silhouettes-walking-tunnel-dark/12291818` is green fog, and
# `man-serious-calm-face-dark-studio-low-key` is the hacker trope.
FEED = V / "thumb-scrolling-phone-feed-dark/38410500.mp4"                 # 30s, L32-40 S19-23, a thumb scrolling a feed
WINDOWS = V / "office-building-windows-night-dark/17499154.mp4"           # 16s, L26 S9, apartment blocks, many lit windows
ALONE = V / "person-alone-laptop-dark-room-night/34771069.mp4"            # 8s,  L20-24 S3-4, hands on a laptop in the dark
SUBWAY = V / "subway-train-passengers-phones-dark/36111567.mp4"           # 15s, L18-21 S10-12, a lit train at a platform
WALLET = V / "smartphone-crypto-wallet-hand-dark/7534328.mp4"             # 16s, L37-40 S14-15, hands holding a lit phone
LEDGER = V / "digital-ledger-blocks-chain-dark/34127877.mp4"              # 20s, L13-15 S5, a tunnel of numerals - the one abstract
WARE = V / "warehouse-shelves-dark-night/19217894.mp4"                    # 10s, L23-30 S3, an empty warehouse corridor

THUMB = ROOT / "assets/crypto/whale/nyc-skyscrapers.jpg"                  # Pexels 15836295, Adrien Daurenjou, 6000x4000
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly. A Short arrives with no title card and no
    # thumbnail on screen, so the first line is what turns the next fifty
    # seconds into an answer somebody is waiting for.
    ("Who is the biggest Bitcoin whale?",),

    # The partial answer. It says "exchange" at ~4.3s, which is the frame the
    # Stamp's verdict lands on.
    ("Not a person.",
     "It is an exchange -",
     "and almost none of those coins are its own."),

    ("A whale is any wallet holding a thousand bitcoin or more.",),

    # Hinge into the split beat - its own sentence, because a leading hinge
    # inside the beat's span eats reveal zero.
    ("An exchange holds the coins of everyone who never moved them off it.",),

    # The split's own sentence: the whole first, the division second.
    ("One address, far past every whale threshold,",
     "and every coin inside it belongs to somebody else."),

    # Hinge into the steps track.
    ("So when a feed says a whale moved tens of thousands of coins,",
     "look at what actually happened."),

    # The steps' own sentence - one chunk per node.
    ("Coins leave a wallet.",
     "They arrive at an exchange.",
     "That can mean somebody is about to sell.",
     "Or the exchange is moving its own inventory."),

    ("The chain shows you the movement.",
     "It never shows you the reason."),

    # Cold close. It answers the opening question instead of re-asking it, so
    # the last thought and the first thought are the same thought.
    ("The biggest whale is not a person. It is a warehouse.",),
]

SHOTS = [
    # The tightest, darkest shot in the cut goes in the opening slot. The
    # feed clip was here in the first pass and its blurred surround is a
    # bright social-app UI - the brightest frames in the piece, at the one
    # second that decides the swipe. It now sits under the sentence that
    # actually names a feed, which is where it says the noun.
    Shot(clip=WALLET, clip_at=1.0, clip_ax=0.42),
    Shot(clip=WINDOWS, clip_at=1.0, clip_ax=0.58),
    Shot(clip=ALONE, clip_at=0.5, clip_ax=0.42),
    Shot(clip=SUBWAY, clip_at=4.0, clip_ax=0.35),
    Shot(graphic="split", backdrop=BEATGROUND,
         payload=("ONE ADDRESS", "past every whale threshold",
                  "CUSTOMER CLAIMS", "none of the coins are its own",
                  "WHOSE COINS ARE THESE?")),
    Shot(clip=FEED, clip_at=1.0, clip_ax=0.58),
    Shot(graphic="steps", backdrop=BEATGROUND,
         payload=(["Coins leave a wallet",
                   "They arrive at an exchange",
                   "Somebody is about to sell",
                   "Or it is moving its own inventory"],
                  "WHAT A WHALE ALERT ACTUALLY SHOWS")),
    Shot(clip=LEDGER, clip_at=2.0, clip_ax=0.30),
    Shot(clip=WARE, clip_at=1.0, clip_ax=0.45),
]

GAPS = [0.70, 0.90, 0.80, 0.60, 1.20, 0.70, 1.10, 0.95, 1.30]


def main() -> None:
    out = Path.home() / "Desktop/crypto-whale-short.mp4"
    work = Path.home() / "Desktop/.crypto-whale-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # A belief to overturn - the shape `Stamp` exists for. The verdict
        # lands on "exchange" in sentence 2.
        opener=Stamp("The biggest Bitcoin whale is a person", "MYTH",
                     at_word="exchange"),
        outro="The biggest whale is not a person. It is a [warehouse].")
    # A pair shares its thumbnail.
    # **Four short forced rows, and a high starting size.** Two rows across
    # the full width set small - the user's note on the first pass - because
    # the size search is capped by the longest row, not by the height. Short
    # rows clear the column early and the search keeps climbing, and putting
    # `[person]` on its own row is what gives the plate room from the word
    # before it. Same row structure as the long form, so the pair reads as a
    # set at feed size.
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "The biggest\nwhale\nis not a\n[person]",
        image=THUMB, accent="yellow", band="top", size=240)
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
