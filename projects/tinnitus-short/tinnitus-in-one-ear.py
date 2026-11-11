"""Why is my tinnitus only in one ear? ~50s Short.

Source: tinnitus-blog/content/posts/tinnitus-in-one-ear.mdx, the same post
as the `tinnitus-in-one-ear` long form, written in the same pass.

**The promise is the one that stands out on this search** (10-28, three
channels): whether to worry, and when to act. Teardown in
`demand/teardowns/tinnitus-in-one-ear.md`.

**The long form's intro, on the long form's search** (the editor,
2026-11-11: the first cut's own opening - "is tinnitus in one ear serious"
and a hearing body-check - was "not that good"). The Search types "why is
my tinnitus only in one ear?" and the first three lines are the long
form's: one ear feels different, the scary search result, "Actually, it
usually has an ordinary cause." Sentence 2 keeps the answer back (the
scary result is named, not given), and "Actually" turns it at ~8s.
`opener_holds=True`.

**Easier to follow** (`shorts.md`, 2026-10-13): the usual causes (`grid`),
why it is still checked - each ear tested on its own (`audiogram`, built
for this pair), the one same-day sign in NIDCD's own words (a drawn `post`:
its page is small white text, which cannot sit under the caption), the
other same-day signs (`checklist`), and how fast otherwise (`dial`, no
needle).

**Close (E16): a plain line that hands back to the opening** - "So get that
ear's hearing checked, and let the test answer the worry." runs into
"Ringing in only one ear feels different from ringing in both.", on the
clip it opened on. No `outro=` card, no disclaimer (the long form carries
it).

**Casting** (2026-11-11): one clip per person, no single group carrying the
cut; screened on the set, not the person (`tools/stock_sheet.py`). The
site's cover is the thumbnail only.

**No medical claims.** Nothing promises the ringing goes away; the
audiogram is titled as an example. The red flags are on screen.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-in-one-ear.py
    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-in-one-ear.py --thumb
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Search
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "tinnitus-in-one-ear"
DEMAND = ("'tinnitus in one ear': Treble 'Should You Ring The Alarm For "
          "Tinnitus In One Ear?' 68k (11.1x), MindEar 'One-Sided Tinnitus: "
          "Possible Causes' 20k (33.1x); teardowns/tinnitus-in-one-ear.md")
COVER_STYLE = "text"

ROOT = Path(__file__).resolve().parents[2]
V = STOCK / "videos"
P = STOCK / "photos"

# The long form's roster (screened and cast there, see its header).
PHONE = V / "woman-in-bed-looking-at-phone-at-night/6466354.mp4"        # opens and closes
BEDSIDE = V / "man-sitting-on-bed-at-night/7280519.mp4"                # on the edge of his bed, phone in hand
DRIVER = V / "driving-car-at-night-window/8470705.mp4"                 # a driver, the window at his ear
COUNTDOWN = V / "clock-ticking-dark/29527767.mp4"                      # a digital countdown, 0:09 to 0:01
WINDOW = P / "man-looking-out-window-at-night/31428994.jpg"             # a man at a window with a mug - "ordinary"

# The site's own cover, cut left of the ear: the thumbnail only.
ONE_SIDE = ROOT / "assets/tinnitus/tinnitus-in-one-ear/one-side-tall.jpg"

VOICE = "noah"          # the noah test, pair 5 of 5 - same voice as the long form
MUSIC = music.track("night-drift")

OPENER = Search("why is my tinnitus only in one ear")

URGENCY = [("Within weeks", 0.62, "#ffdab9"),
           ("Same day", 1.0, "#e0605a")]
EAR_A = [10, 10, 15, 15, 20, 20]
EAR_B = [10, 15, 25, 45, 55, 60]

SENTENCES = [
    # The long form's intro, under the long form's Search.
    ("Ringing in only one ear feels different from ringing in both.",),
    ("And if you searched it at night, the scariest answer was probably near the top.",),
    ("Actually, it usually has an ordinary cause.",),
    # grid - one chunk per card.
    ("Wax against the eardrum,",
     "an infection or fluid,",
     "more noise on one side,",
     "or the jaw."),
    # audiogram - one chunk per ear.
    ("But it is also the one pattern guidelines flag for a prompt hearing test,",
     "each ear tested on its own, and the two compared."),
    # post - the lead-in, then the line read.
    ("If that ear's hearing dropped suddenly, the US hearing institute says to treat it as",
     "a medical emergency and visit a doctor immediately."),
    ("Treatment works best when it starts early.",),
    # checklist, flow - one chunk per sign.
    ("The same goes for ringing that beats with your pulse,",
     "a weak or numb face,",
     "or new dizziness."),
    # dial, no needle - one chunk.
    ("Without any of those, book a hearing test in the next few weeks.",),
    # The close, said and captioned; it hands back to the opening line.
    ("So get that ear's hearing checked, and let the test answer the worry.",),
]

GAPS = [0.85,   # into sentence 2, after the opener
        0.80,
        0.70,   # into the grid
        0.80,
        0.90,   # the turn, and the audiogram's gap shading in
        0.70,
        0.60,
        1.10,
        0.90,   # before the close
        0.34]

SHOTS = [
    Shot(clip=PHONE, clip_at=1.0, clip_ax=0.55),
    Shot(clip=BEDSIDE, clip_at=11.0, clip_ax=0.50),
    Shot(image=WINDOW, parallax=0.5),
    Shot(graphic="grid",
         payload=([("Wax on the eardrum", "", "\U0001F6A7"),
                   ("Infection or fluid", "", "\U0001F4A7"),
                   ("More noise on one side", "", "\U0001F697"),
                   ("The jaw on that side", "", "\U0001F62C")],
                  "USUALLY ORDINARY")),
    Shot(graphic="audiogram",
         payload=(EAR_A, EAR_B, "A HEARING TEST - AN EXAMPLE",
                  "the gap they look for")),
    Shot(graphic="post",
         payload=("headline",
                  {"source": "NIDCD (NIH)",
                   "date": "Sudden Deafness",
                   "headline": "You should consider sudden deafness symptoms "
                               "[a medical emergency and visit a doctor "
                               "immediately.]"},
                  "")),
    Shot(clip=COUNTDOWN, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="checklist",
         payload=([("Beats with your pulse", True),
                   ("A weak or numb face", True),
                   ("New dizziness", True)],
                  "SAME DAY TOO", True)),
    Shot(graphic="dial",
         payload=(URGENCY, None, "", "HOW FAST TO ACT", 0)),
    # The close on the clip it opened on, later in it.
    Shot(clip=PHONE, clip_at=18.0, clip_ax=0.55),
]

# The pair shares the cover's question; "tinnitus" is on it (2026-11-11).
THUMB_HEADLINE = "Tinnitus\nin [one ear?]"


def thumbs(out: Path) -> Path:
    """The site's half-lit face (cut left of the ear) on the lower frame,
    the question in two rows on the dark above."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(ONE_SIDE).convert("RGB")
    pic = src.resize((1080, int(src.height * 1080 / src.width)), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (8, 6, 6))
    im.paste(pic, (0, 1920 - pic.height))
    fill, ink = T.ACCENTS["red"]
    T._headline(im, THUMB_HEADLINE, 210, 1080 - 2 * 60, 60, fill, ink,
                max_lines=2, max_block=1920 * 0.30, leading=1.02,
                band="top", margin=int(1920 * 0.13), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-in-one-ear-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-in-one-ear-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, opener_holds=True,
                                        tail=1.5)
    thumb = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/tinnitus-in-one-ear-short-thumb.jpg"))
    else:
        main()
