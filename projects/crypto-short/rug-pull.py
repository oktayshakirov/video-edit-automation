"""What is a rug pull? ~45s crypto short.

Source: crypto-wiki/content/posts/what-is-a-rug-pull.mdx - the same post as the
`rug-pull` long-form explainer, written in the same pass.

**The single move.** The long form walks the whole mechanism, the five
patterns, the locked-pool decoy and a four-question check. The Short does the
one thing those chapters are built on: a new token only has a price because
the creators paired it with a pool of real money, and whoever controls that
pool controls whether the price is real. Then a three-step check, and stop.

**It opens by asking its own title question.** A Short has no title card, no
thumbnail on screen and no chapter list, so the first line is the question the
whole thing answers - "How does a token crash to almost nothing the second the
hype dies?" - said over a moving face, not over a card.

**Two drawn beats.** `steps` - the three-step check, a vertical track with
icon nodes and a connector that draws against the voice - and a `chapter`
statement card to close. Both sit on the same warm `beat-ground` the long
form's beats use, not the water. The abstract rug-pull `CHART` (line up, then
a plunge to zero) carries "pull the money straight out"; the 9:16 cut of it
is a full-bleed still.

**No financial-advice line - the standing rule for every Short on this
channel.** The paired long form carries the disclaimer; the Short closes on
the instruction. The script names no token, no price, no platform, no
direction.

**Assets.** `FACE`, `HOODED`, `DESK`, the `DOLLARS` photo and `CHART` are
shared with the long form (used once there, once here). `RESEARCH` and `CITY`
are the short's own. Every clip screened dark and contact-sheeted; none is a
price chart, ticker or trading screen. Re-cut twice after review: foreign
banknotes -> US dollars, a phone-over-rubble closing shot -> a night-city
aerial, a badly-cropped fire-escape clip -> the `CHART`, and the flat
`checklist` -> the animated `steps` track.

**Phonemes.** Same as the long form: "rug pull", "liquidity", "block explorer"
all phonemize correctly; "DeFi" and "APY" are avoided and never spoken.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/rug-pull.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.thumb import render_short_thumb

from pathlib import Path as _P

V = STOCK / "videos"
PH = STOCK / "photos"
POSTS = SITE_IMAGES / "posts"
BRAND = _P(__file__).resolve().parents[2] / "assets/brand"

# FACE / HOODED / DESK are shared with the long form (used once there, once
# here). DOLLARS and CHART are shared too. RESEARCH / CITY are the short's own.
FACE = V / "close-up-worried-man-face-dark-room/8458651.mp4"            # 19.2s L38-46 S9-11, worried face, low key
HOODED = V / "hooded-figure-computer-screen-dark/32829777.mp4"         # 21.5s L36-37 S11, hooded figure at a screen
DOLLARS = PH / "stack-of-cash-money-dark-moody/18921474.jpg"          # 6000x4000 L78 S8, three $100 bills on dark
RESEARCH = V / "woman-looking-at-laptop-screen-dark-serious/6346221.mp4"  # 10.8s L37-39 S10-11, woman studying a laptop, dark
DESK = V / "man-working-laptop-dark-office-night-alone/8311535.mp4"    # 23.7s L10-28 S5-12, man at a laptop alone, night
CITY = V / "city-skyline-night-dark-aerial/39106960.mp4"              # 21.5s L25-27 S4-5, night city from above, slow
# The abstract rug-pull chart - line steps up, plunges to a flat zero. The
# long form uses the 16:9 file; this is the 9:16 cut, full-bleed.
CHART_V = BRAND / "graphics/rug-pull-chart-vertical.png"              # 1080x1920, generated
BEATGROUND = BRAND / "beat-ground-crypto.jpg"                          # warm near-black bloom behind the drawn beat

THUMB = POSTS / "hacker.jpg"                                          # 996x664 L38 S3, hooded figure with a laptop - matches the long form

E_LOCK, E_CHART, E_CROWN = "\U0001F512", "\U0001F4CA", "\U0001F451"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, over a moving face - a Short viewer has nothing else
    # on screen but this sentence.
    ("How does a token crash to almost nothing",
     "the second the hype dies?"),

    # What it plainly is, before how it behaves.
    ("A rug pull is an exit scam dressed up as a launch.",),

    ("A new token only has a price",
     "because the creators paired it with a pool of real money.",),

    ("Control that pool,",
     "and you can pull the money straight out,",
     "and leave everyone holding a token worth nothing."),

    # Hinge, its own sentence - a beat times its reveals off the caption starts
    # of its own sentence, so the lead-in cannot live inside it.
    ("So before you buy, run a three-step check on that pool.",),

    # The `steps` beat - one caption chunk per node, in order. The track and
    # the icons carry the sequence, so the narration does not count "one, two".
    ("Is the liquidity locked, or can the team still pull it.",
     "Who holds the supply - a few wallets, or thousands.",
     "Can the owner still rewrite the contract."),

    ("You can check all three on a block explorer,",
     "in about a minute."),

    # Full-screen statement. `build` suppresses captions on any shot with a
    # graphic, so the card is capitals while the voice reads a sentence.
    (("IF THEY CAN PULL THE POOL, THEY WILL.",
      "If they can pull the pool, they will."),),

    ("So the next time a coin is mooning on your feed -",
     "check who actually controls its liquidity pool."),
]

SHOTS = [
    Shot(clip=FACE, clip_at=0.5),
    Shot(clip=HOODED, clip_at=1.0),
    Shot(image=DOLLARS, aspect=1.5, bias=0.5),
    Shot(image=CHART_V, aspect=1080 / 1920),          # full-bleed, the price to zero
    Shot(clip=RESEARCH, clip_at=0.5),
    Shot(graphic="steps", backdrop=BEATGROUND,
         payload=([("Is the liquidity locked?", E_LOCK),
                   ("Who holds the supply?", E_CHART),
                   ("Can the owner change it?", E_CROWN)],
                  "THE THREE-STEP CHECK")),
    Shot(clip=DESK, clip_at=1.0),
    Shot(graphic="chapter",
         payload=("IF THEY CAN PULL THE POOL, THEY WILL.",)),
    Shot(clip=CITY, clip_at=1.0),
]

# 0.34 inside a thought, 0.55-0.90 at the end of one. The `steps` track (index
# 5) has no verdict pause to buy - 1.10 lets the track finish drawing before
# the next line. The statement card (index 7) takes 1.30.
GAPS = [0.75, 0.85, 0.70, 0.80, 0.60, 1.10, 0.80, 1.30, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/crypto-rug-pull-short.mp4"
    work = Path.home() / "Desktop/.crypto-rug-pull-short-work"
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, gap=GAPS,
                                     music=MUSIC, music_gain=0.85)

    # Same source and headline as the long form; the Short brackets the
    # two-word phrase (its column is full-width, so the run fits).
    head = "How does a [rug pull] work?"
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO, head,
        image=THUMB, accent="yellow", band="bottom")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
