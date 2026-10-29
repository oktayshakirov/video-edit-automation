"""Who decides who wins a Polymarket bet? ~45s crypto short.

Source: crypto-wiki/content/posts/what-are-prediction-markets.mdx - the same
post as the `prediction-markets` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks the share, why its
price is the odds, the oracle, the Ukraine market and when not to trust the
odds. This does one move: the answer to a bet is not Polymarket's call, it
is a vote by holders of another token - and in March 2025 that vote settled a
$7M question against the facts.

**Easy to follow first** (`shorts.md`, 2026-10-13): a viewer who has never
heard of a prediction market needs the share before "who decides" means
anything, so the `shares` beat runs first, ending on the outcome - which is
the question the rest of the Short answers.

**Sentence 2 overturns the title and keeps the answer back.** "Who
decides?" assumes the platform; "Not Polymarket. And the ones who do got a
seven million dollar question wrong." overturns it plainly, withholds *who*
(the vote, which the diagram pays off) and opens "how?". The first draft said
"a vote, by people holding a different token" there, and `opening_check`
flagged it as the answer itself. Its first words stay on the title's
subject.

**Opener: `Stamp`** - the belief is that the platform decides, and the
stamp judges that claim, never the platform. The last three crypto Shorts
opened Search / Counter / Stamp; Stamp is not three running.

**Two beats:** `shares` (portrait) and `diagram`, then a full-screen
`chapter` for the result. The last three crypto Shorts ran blindsign /
chapter, chapter / pool, checklist / chapter.

**Cold close**, held by `outro=`: "The price is the crowd's guess. The
answer is a vote." answers the opening question without re-asking it, so
the last frame loops into the first. **No disclaimer** (the long form
carries it).

**Clips** are the long form's roster; it opens on the long form's first
shot.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/prediction-markets.py
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

SOURCE_POST = "what-are-prediction-markets"
DEMAND = ("Coinsider 'What is Polymarket? The Ultimate Prediction Market' 108k, "
          "31.4x")

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
PRESS = STOCK / "press/polymarket"

# The long form's roster - screened there, see its header.
APP = V / "stock-trading-app-phone-dark/7681176.mp4"            # two hands on a phone trading app
FINGER = V / "stock-trading-app-phone-dark/34473008.mp4"        # a finger on a candle chart
CLOCK = V / "clock-ticking-dark-close-up/7033779.mp4"           # an alarm clock on black
BALLOT = V / "voting-ballot-box/7103424.mp4"                    # a ballot going into a box
KYIV = V / "kyiv-city-night/12399500.mp4"                       # Kyiv and the Dnipro from above
INVEST = V / "stock-trading-app-phone-dark/7947486.mp4"         # a phone showing a balance and a line

LOGO = PRESS / "logos/logo-white.png"

VOICE = "noah"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly, under the Stamp.
    ("Who decides who wins a Polymarket bet?",),

    # The reversal: not the platform - and whoever does got it wrong. Keeps
    # back *who* (the vote) and opens two questions at once.
    ("Not Polymarket. And the ones who do got a seven million dollar question wrong.",),

    # The hinge, then the share, ending on the outcome.
    ("Here is what you are buying.",),
    ("Every bet is a question, and a one-dollar share.",
     "Split into yes and no.",
     "Yes at sixty-two cents,",
     "means sixty-two percent.",
     "Only the right side gets the dollar."),

    # The hinge into the diagram.
    ("So someone has to say which side was right.",),
    ("Anyone can propose the answer.",
     "Anyone can challenge it, within two hours.",
     ("Then holders of the UMA token vote.",
      "Then holders of the Yuma token vote.")),

    ("In March 2025, the question was: would Ukraine agree to a minerals deal with Trump before April?",),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("NO DEAL. RESOLVED YES.",
      "No deal was agreed. It resolved yes anyway."),),

    ("Polymarket called it unprecedented, and refunded nothing.",),

    # Cold close, held by `outro=`.
    ("The price is the crowd's guess. The answer is a vote.",),
]

SHOTS = [
    Shot(clip=APP, clip_at=1.0, clip_ax=0.50),
    Shot(clip=FINGER, clip_at=1.0, clip_ax=0.55, inset=(LOGO, "top", 0.40)),
    Shot(clip=INVEST, clip_at=0.3, clip_ax=0.50),
    Shot(graphic="shares",
         payload=("Will it happen\nby 31 December?", 62, "ONE QUESTION", "YES")),
    Shot(clip=CLOCK, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="diagram",
         payload=([("Proposed", "an answer, and a bond"),
                   ("Challenged", "within two hours"),
                   ("Voted", "by UMA token holders")],
                  "WHO SETTLES IT")),
    Shot(clip=KYIV, clip_at=2.0, clip_ax=0.50),
    Shot(graphic="chapter", payload=("NO DEAL. RESOLVED YES.",)),
    Shot(clip=BALLOT, clip_at=6.0, clip_ax=0.50, clip_ay=0.85),
    # The loop: the close lands on the opening shot's own phone.
    Shot(clip=APP, clip_at=18.0, clip_ax=0.50),
]

GAPS = [1.20, 0.85, 0.40, 1.40, 0.50, 1.10, 0.75, 0.95, 0.70, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/prediction-markets-short.mp4"
    work = Path.home() / "Desktop/.prediction-markets-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Stamp("Polymarket decides who wins", "WRONG", at_word="not"),
        outro="The price is the crowd's guess. The answer is a [vote].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the long form's cover card, stacked portrait -
    Polymarket's wordmark, the `shares` card at its turn (the question, YES at
    62% on the bar, NO at 38c, THE CROWD'S ODDS) drawn landscape and scaled to
    the frame's width, then the Short's question in two rows, clear of the
    view count. The card is drawn at a settled reveal, never mid-morph: the
    first cover caught "62%" and "RESOLVED YES" half faded (2026-10-29)."""
    from PIL import Image, ImageDraw, ImageFilter
    from video_automation.core.draw import cover
    from video_automation.core.frame import LANDSCAPE
    from video_automation.longform import thumb as T
    from video_automation.longform.beats import Shares
    ground = ROOT / "assets/brand/beat-ground-crypto.jpg"
    b = Shares("Will it happen by 31 December?", 62, "", None, brand=CRYPTO,
               frame=LANDSCAPE, backdrop=ground,
               reveals=[0.0, 1.0, 2.0, 3.4], start=0.0, hold=5.0)
    full = b.draw(1.0)
    x0 = (1920 - b.card_w) // 2 - 30
    card = full.crop((x0, b.card_y - 30, x0 + b.card_w + 60, b.bar_y + b.bar_h + 110))
    cw = 1000
    card = card.resize((cw, int(card.height * cw / card.width)), Image.LANCZOS)
    im = cover(Image.open(ground).convert("RGB"), 1080, 1920)
    im = im.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * 0.45))
    x, y = (1080 - cw) // 2, 470
    shape = Image.new("L", card.size, 0)
    ImageDraw.Draw(shape).rounded_rectangle([1, 1, card.width - 2, card.height - 2],
                                            radius=24, fill=255)
    im.paste(card, (x, y), shape)
    logo = Image.open(LOGO).convert("RGBA")
    lw = 460
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    im.paste(logo, ((1080 - lw) // 2, 250), logo)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, "Who decides\nwho [wins?]", 200,
                1080 - 2 * 52, 52, fill, ink, max_lines=2,
                max_block=1920 * 0.22, leading=1.02, band="bottom",
                margin=int(1920 * 0.16) + 20, shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/prediction-markets-short-thumb.jpg"))
    else:
        main()
