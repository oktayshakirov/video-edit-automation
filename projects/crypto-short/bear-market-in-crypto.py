"""What is a bear market in crypto? ~49s crypto short.

Source: crypto-wiki/content/posts/bear-market-in-crypto.mdx - the same post as
the `bear-market-in-crypto` long form, written in the same pass.

**Re-cut 2026-10-13, after the first review.** The first cut did the long
form's twist on its own (a 40% jump after an 80% fall is still 72% down, and
the climb back gets steeper) and the user found it confusing and hard to
follow: arithmetic heard once, with no definition in front of it, is a sum
the viewer has to hold in their head. They asked for the long form's opener
instead - the search, stocks against crypto, the history, whether we are in
one now, and what causes it. So this cut answers the plain question in the
order a viewer would ask it, one beat per answer.

**Opener: `Search`**, typing the same query as the long form, so the pair is
recognised as a pair. Last three crypto Shorts ran Counter / Stamp / hook.

**Sentence 2 keeps the number back** (`narration.md`, 2026-10-11): "Stocks
draw the line at one number. Crypto's go about four times deeper." names the
kind of answer - a number, and a depth - and the bars beat pays it off.

**Three beats, one per question:** `bars` (how deep: the stocks line against
Bitcoin's four), `diagram` with `loop=True` (what causes it: borrowed money
and forced selling feeding each other) and `steps` (are we in one: three
checks). Three different silhouettes, and not the halving Short's `bars` +
`chart` repeated - the `bars` is shared, the rest is new.

**"Are we in one right now?" is answered with a check, not a verdict.** The
user asked for it, and it is a question people actually type. But a
statement about where the market is today is a call on direction, which
this channel never makes, and it would be stale within weeks of upload. So
the Short asks it and hands over the article's own test - how far below the
last peak, whether the highs are still falling, and for how long - as a
procedure the viewer runs themselves.

**Cold close**, echoing the opening question with the definition the video
earned; `outro=` holds it to the last frame so it loops back into the
search. **No disclaimer** - the long form carries it. **No financial
advice:** no price level, no prediction, no platform.

**Figures** are the article's: the twenty percent line in stocks, Bitcoin's
falls of over 90 (2011), 86 (2014), 84 (2018) and 77 (2022) percent; 77-93
against 20 is "about four times deeper".

**Clips** are the long form's roster, each used once here; the opening
facade is the long form's opening shot, shared on purpose.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/bear-market-in-crypto.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from PIL import Image

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform import thumb as T
from video_automation.longform.openers import Search

SOURCE_POST = "bear-market-in-crypto"

V = STOCK / "videos"
P = STOCK / "photos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# The long form's roster - screened there, see its header.
NYSE = V / "new-york-stock-exchange/4319342.mp4"                 # 10s, the stock exchange's columns - the long form's first shot too
LONECOIN = V / "gold-bitcoin-black-background/8370146.mp4"       # 14s, one gold bitcoin standing on a dark table, centred
SIGN = V / "signing-contract-pen-close-up/8439245.mp4"           # 7s,  a hand signing a form - borrowed money
LYING = V / "checking-phone-in-bed-at-night/6943545.mp4"         # 11s, a man lying in bed checking his phone
SKYLINE = V / "financial-district-night/6345205.mp4"             # 21s, a financial district's towers at night - sky above for the outro

BEAR = P / "brown-bear-dark-background/33037033.jpg"             # 9504x6336, the pair's thumbnail
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly, while Search types it.
    ("What is a bear market in crypto?",),

    # Keeps the number back: the kind of answer, not the answer.
    ("Stocks draw the line at one number.",
     "Crypto's go about four times deeper."),

    # The bars' own sentence - one chunk per row.
    ("Stocks call it at twenty percent down.",
     "Bitcoin in 2011 fell over ninety.",
     "In 2014, eighty-six.",
     "In 2018, eighty-four.",
     "And in 2022, seventy-seven."),

    # The hinge gets its own sentence: inside the diagram's span it would eat
    # reveal zero.
    ("So what causes it? Pressures stack up, and borrowed money does the rest.",),

    # The diagram's own sentence - one chunk per node.
    ("Prices fall.",
     "Traders who borrowed get sold out automatically.",
     "And that selling pushes prices down again."),

    ("So are we in one right now? Run three checks.",),

    # The steps' own sentence - one chunk per node.
    ("How far is it below its last peak?",
     "Is every high lower than the one before?",
     "And has that lasted months, not weeks?"),

    # Cold close: the opening question, answered with what the video showed.
    ("A bear market is not a bad week. It is a long fall, measured from the top.",),
]

SHOTS = [
    Shot(clip=NYSE, clip_at=0.5, clip_ax=0.50),
    Shot(clip=LONECOIN, clip_at=0.5, clip_ax=0.50),
    Shot(graphic="bars", backdrop=BEATGROUND,
         payload=([("Stocks", 0.19, "20%"),
                   ("2011", 0.874, "90%+"),
                   ("2014", 0.817, "86%"),
                   ("2018", 0.798, "84%"),
                   ("2022", 0.73, "77%")],
                  "HOW FAR FROM THE PEAK")),
    Shot(clip=SIGN, clip_at=0.5, clip_ax=0.50),
    Shot(graphic="diagram", backdrop=BEATGROUND,
         payload=([("Prices fall", "below what traders borrowed against"),
                   ("Forced selling", "the exchange sells for them"),
                   ("Prices fall further", "and the loop goes round")],
                  "WHAT MAKES IT DEEP", True)),
    Shot(clip=LYING, clip_at=1.0, clip_ax=0.45),
    Shot(graphic="steps", backdrop=BEATGROUND,
         payload=(["How far below its last peak?",
                   "Is every high lower than the last?",
                   "Has it lasted months, not weeks?"],
                  "ARE WE IN ONE? THREE CHECKS")),
    Shot(clip=SKYLINE, clip_at=1.0, clip_ax=0.50),
]

# Ran 53.8s with a "crypto never closes" line after the diagram and a longer
# first bars chunk; both cut to land inside the 40-50s window.
GAPS = [0.70, 0.85, 1.30, 0.60, 1.40, 0.70, 1.30, 1.20]

# One bracketed word on a 16:9 thumbnail (`thumbnails.md`): BEAR, beside the
# bear. The vertical cover forces three phrase-shaped rows.
HEADLINE = "What is a crypto [bear] market?"
HEADLINE_V = "What is a\ncrypto [bear]\nmarket?"


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's bear, cropped onto its head, the same
    headline on three rows in the black above it."""
    im = Image.open(BEAR).convert("RGB")
    w, h = im.size
    cw = int(h * 9 / 16)
    x0 = max(0, min(w - cw, int(w * 0.50 - cw / 2)))
    im = im.crop((x0, 0, x0 + cw, h)).resize((1080, 1920), Image.LANCZOS)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE_V, 240,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.21, leading=1.02, band="top",
                margin=int(1920 * 0.07), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/bear-market-in-crypto-short.mp4"
    work = Path.home() / "Desktop/.bear-market-in-crypto-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The same query the long form opens on, so the pair reads as a
        # pair. Question only - no answer on screen.
        opener=Search("what is a bear market in crypto"),
        outro="A bear market is not a bad week. It is a long fall, "
              "measured from the [top].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/bear-market-in-crypto-short-thumb.jpg"))
    else:
        main()
