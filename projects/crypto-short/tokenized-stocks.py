"""If you buy Tesla on a blockchain, do you own Tesla? ~45s crypto short.

Source: crypto-wiki/content/posts/what-are-tokenized-stocks.mdx - the same
post as the `tokenized-stocks` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks what a tokenized
stock is, the two kinds, what a backed token gives you (its turn), the
OpenAI case, the weekend price and the 2026 rule. This does one move, in
the order a viewer asks it (`shorts.md`, 2026-10-13): do I own the share
(usually not), why (the diagram: the custodian holds it), is there always
one (no - synthetic), the proof (OpenAI's reply), and what changed.

**Sentence 2 overturns the title's assumption and opens the next
question.** "Do you own Tesla?" assumes yes; "You own a token. The share,
if there even is one, has someone else's name on it" overturns it and
opens two questions - whose name, and why might there be no share. The
first draft led with "Usually not." and `opening_check` flagged it as a
verdict, so sentence 2 says what you do own instead of saying no
(`narration.md`, 2026-10-11).

**Opener: `Split`**, TOKEN against SHARE, "SAME THING?", shared with the
long form. One word a side (`shorts.md`, "Split collides with its own
labels in 9:16"). The last three crypto Shorts opened Stamp / Counter /
Stamp.

**Close: a plain last sentence, no `outro=` card** (2026-11-06), a
directive answering the opening ("before you call it a share, find out
whose name is on it"), on the clip the Short opened on. **No disclaimer**
(the long form carries it).

**Robinhood's page is not in this cut**: its 9:16 capture set the help
text at a size nobody can read on a phone, and a bright page under the
karaoke line is the 2026-10-27 fault. OpenAI's reply carries the proof as
a drawn `post`.

**Clips** are the long form's roster.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/tokenized-stocks.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Split

SOURCE_POST = "what-are-tokenized-stocks"
DEMAND = ("Finance Simply Explained 'Tokenized Stocks Are Back: Do You Really "
          "Own the Shares?' 9.1x; Kraken 'Tokenized equities explained' 32.4x")

V = STOCK / "videos"
POSTS = _P.home() / "Coding/crypto-wiki/public/images/posts"

# The long form's roster - screened there, see its header.
APP = V / "investing-app-phone-hands-night/34453449.mp4"               # a finger on a stock app - opens and closes
HEATMAP = V / "nasdaq-times-square-night/38905686.mp4"                 # a market heat map of real tickers
NIGHTCHART = V / "nasdaq-times-square-night/38841404.mp4"              # a price chart on a monitor in the dark
DOCS = V / "legal-documents-folder-dark-desk/8061377.mp4"              # a hand laying paperwork on a desk
CAPITOL = V / "government-building-columns-night/35120905.mp4"         # a capitol dome lit at night
INVESTING = V / "stock-app-smartphone-dark-room/7947481.mp4"           # a phone showing a retail app's "Investing" balance
COVER = POSTS / "what-are-tokenized-stocks.jpg"                        # the site's cover: hands on a tablet chart

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, under the Split.
    ("If you buy Tesla on a blockchain, do you own Tesla?",),

    # The reversal, without a bare "no": you own something else. Opens
    # "whose, then?" and "if there is one?".
    ("You own a token. The share, if there even is one, has someone else's name on it.",),

    # The hinge, then the diagram: one chunk per box.
    ("Here is how the backed kind works.",),
    ("Someone buys real Tesla shares,",
     "a custodian holds them,",
     "and you get a token that follows the price."),

    ("The name on Tesla's list of shareholders is the custodian's, not yours.",),

    ("And some tokens have no share behind them at all, just a contract that copies the price.",),

    # The case on its own clip, so the card holds only for the quote: the
    # first cut ran both on the card and held it ~10s (2026-11-07).
    ("In 2025, Robinhood sold tokens of OpenAI.",),
    # The post: lead-in, then the line read.
    ("OpenAI's answer:",
     "These OpenAI tokens are not OpenAI equity."),

    ("Since September 2026, American rules say a token must carry the share's rights, votes included.",),

    # The close, said and captioned - no outro card.
    ("So before you call it a share, find out whose name is on it.",),
]

SHOTS = [
    Shot(clip=APP, clip_at=0.5, clip_ax=0.55),
    Shot(clip=HEATMAP, clip_at=2.0, clip_ax=0.40),
    Shot(image=COVER, parallax=0.6),
    Shot(graphic="diagram",
         payload=([("Real shares", "bought by someone else", "\U0001F4B8"),
                   ("A custodian", "holds them", "\U0001F512"),
                   ("Your token", "follows the price", "\U0001F4C8")],
                  "THE BACKED KIND", False)),
    Shot(clip=DOCS, clip_at=1.0, clip_ax=0.55),
    Shot(clip=NIGHTCHART, clip_at=1.0, clip_ax=0.50),
    Shot(clip=INVESTING, clip_at=0.5, clip_ax=0.35),
    Shot(graphic="post",
         payload=("post",
                  {"name": "OpenAI Newsroom", "handle": "@OpenAINewsroom",
                   "date": "2 Jul 2025",
                   "text": "[These “OpenAI tokens” are not OpenAI "
                           "equity.] We did not partner with Robinhood."},
                  "")),
    Shot(clip=CAPITOL, clip_at=4.0, clip_ax=0.50),
    Shot(clip=APP, clip_at=6.0, clip_ax=0.55),
]

GAPS = [1.00, 0.85, 0.55, 1.30, 0.70, 0.80, 0.60, 1.30, 0.90, 1.20]

HEADLINE = "Do you\nown\n[this?]"

# The long form's cover picture and question (2026-11-08): a pair shares
# a thumbnail (`thumbnails.md`). Pexels 258083, see CREDITS.md there.
TESLA = _P(__file__).resolve().parents[2] / "assets/crypto/tokenized-stocks/tesla-sign.jpg"


def main() -> None:
    out = Path.home() / "Desktop/tokenized-stocks-short.mp4"
    work = Path.home() / "Desktop/.tokenized-stocks-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        opener=Split("TOKEN", "SHARE", "SAME THING?"))
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


def thumbs(out: Path) -> Path:
    """The 9:16 cover: the charger full width in the lower frame, the
    question in three rows on the black above, a white ring round TESLA and
    a white arrow down to it."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(TESLA).convert("RGB")
    c0, c1, top = 0.07, 0.81, 0.24
    crop = src.crop((int(src.width * c0), int(src.height * top),
                     int(src.width * c1), src.height))
    pic = crop.resize((1080, int(crop.height * 1080 / crop.width)),
                      Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (0, 0, 0))
    y = 1920 - pic.height
    im.paste(pic, (0, y))
    # the wordmark: x .26-.65, y .45-.53 of the source
    k = 1080 / crop.width
    tx0, tx1 = (0.26 - c0) * src.width * k, (0.65 - c0) * src.width * k
    ty0 = (0.45 - top) * src.height * k + y
    ty1 = (0.53 - top) * src.height * k + y
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 230, 1080 - 2 * 60, 60, fill, ink,
                max_lines=3, max_block=1920 * 0.32, leading=1.02,
                band="top", margin=int(1920 * 0.17), shadow=14, drop=(6, 8))
    im = im.convert("RGBA")
    # ~90px clear of the letters each side, ~70 above and below (2026-11-08)
    im.alpha_composite(T.ring_layer(
        im.size, (tx0 - 90, ty0 - 70, tx1 + 90, ty1 + 70), width=14))
    im.alpha_composite(T.arrow_layer(
        im.size, (885, ty0 - 450), (tx1 + 58, ty0 - 74),
        width=26, head=76, bow=-0.25))
    im.convert("RGB").save(out, quality=92)
    return out


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/tokenized-stocks-short-thumb.jpg"))
    else:
        main()
