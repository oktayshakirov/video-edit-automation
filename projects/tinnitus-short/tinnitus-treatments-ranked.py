"""What does the new tinnitus guideline say about your treatment? ~50s Short.

Source: tinnitus-blog/content/posts/tinnitus-guideline-2026.mdx, the same
post as the `tinnitus-treatments-ranked` long form, written in the same pass.

**The move:** the board, filled bottom up. The Short asks its title question
in full (14 words, so sentence 2 starts near 4s), and sentence 2 keeps the
answer back: the treatment most people try first is on the list to avoid -
which one, and what is on the good list, is the rest of the video. The
`Stamp` lands on "avoid" (`at_word`, `shorts.md` 2026-11-19: a full title
question and a redacted hook do not fit together).

**Easier to follow** (`shorts.md`, 2026-10-13): what the guideline is, then
the board row by row in the order a viewer would ask - what to skip, what is
optional, what is recommended - then the twist (no treatment in the top
row) and the plain close.

**Close (E16): a plain line that hands back to the title question**, on the
clip it opened on. No `outro=` card, no disclaimer (the long form carries
it).

**No medical claims.** The rows are the panel's grades, never relief; the
against row carries "for tinnitus itself" in the voice.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-treatments-ranked.py
    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-treatments-ranked.py --thumb
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "tinnitus-guideline-2026"
DEMAND = ("HearingTracker 'Four BEST Tinnitus Treatments' 402k (109x); Doctor "
          "Cliff 'The 4 BEST Tinnitus Treatments' 30.6x; 'tinnitus guideline "
          "2026' a new term (Timpanogos ~3x, rest <300); "
          "teardowns/tinnitus-treatments-ranked.md")
COVER_STYLE = "tiers"

V = STOCK / "videos"
SITE = Path.home() / "Coding/tinnitus-blog/public/images"

# The long form's roster (screened and cast there, see its header).
READER = V / "woman-reading-tablet-at-night-dark/7198399.mp4"     # opens and closes
CAPSULES = V / "supplement-capsules-in-hand-dark/5453702.mp4"      # two hands full of capsules
LAPTOP = V / "woman-looking-out-window-at-night-city/7988267.mp4"  # a woman at a laptop by a night window (7s: once)
THERAPY = SITE / "therapy-2.jpg"                                    # a therapist and a client in armchairs

VOICE = "mia"           # the long form's voice
MUSIC = music.track("night-drift")

OPENER = Stamp("Supplements for tinnitus", "AVOID", tone="negative",
               at_word="avoid", enter_word="says")

# Three rows - the board's top row is said, not drawn, in 50 seconds.
ROWS = [("Recommended", "a firm should"),
        ("An option", "may offer it"),
        ("Advised against", "not for tinnitus")]
ITEMS = [(2, "Supplements", "\U0001F48A"),
         (2, "Magnetic brain stimulation", "\U0001F9F2"),
         (2, "Medicines for the ringing", "\U0001F489"),
         (1, "Sound enrichment", "\U0001F30A"),
         (1, "Bimodal devices", "\U0001F3A7"),
         (0, "Hearing aids", "\U0001F9BB"),
         (0, "Implant check", "\U0001F442"),
         (0, "CBT", "\U0001F4AC")]
BOARD = "THE 2026 GUIDELINE"


def board(shown: int, until: int) -> Shot:
    return Shot(graphic="tiers", ground="grid",
                payload=(ROWS, ITEMS, BOARD, shown, until))


SENTENCES = [
    ("What does the new 2026 tinnitus guideline say about the treatments you have tried?",),
    ("It says to avoid the one most people try first.",),
    ("It is the US guideline, rewritten this year, and it grades every treatment.",),
    # tiers, the bottom row - one chunk per card.
    ("Advised against for tinnitus itself: supplements,",
     "magnetic brain stimulation,",
     "and medicines for the ringing."),
    # tiers, the middle row.
    ("An option: gentle sound in a quiet room,",
     "and bimodal devices, sound with mild pulses on the tongue."),
    # tiers, the top row.
    ("Recommended: hearing aids,",
     "a cochlear implant check,",
     "and cognitive behavioral therapy."),
    ("But no treatment got the top grade.",),
    ("That went to the appointment itself, and to asking how you are coping.",),
    # The close, said and captioned; it hands back to the title question.
    ("So when a treatment is offered, ask which row it is on.",),
]

GAPS = [0.85,   # into sentence 2, after the stamp
        0.70,
        0.70,   # into the board
        1.10,
        1.00,
        1.20,
        0.80,   # the turn
        0.90,   # before the close
        0.34]

SHOTS = [
    Shot(clip=READER, clip_at=1.0, clip_ax=0.50),
    Shot(clip=CAPSULES, clip_at=1.0, clip_ax=0.50,
         window=("player", "The first thing many try")),
    Shot(clip=LAPTOP, clip_at=0.5, clip_ax=0.62),
    board(0, 3),
    board(3, 5),
    board(5, 8),
    Shot(graphic="tiers", ground="grid",
         payload=([("Strong yes", "the top grade", None,
                    "No treatment got this grade")] + ROWS,
                  [(r + 1, l, e) for r, l, e in ITEMS], BOARD, 8, 8)),
    Shot(image=THERAPY, window=("player", "The appointment itself")),
    # The close on the clip it opened on, later in it.
    Shot(clip=READER, clip_at=12.0, clip_ax=0.50),
]

ROOT = Path(__file__).resolve().parents[2]


def thumbs(out: Path, variants: bool = False) -> list[Path]:
    """The 9:16 cover - a pair shares a thumbnail, so the long form's
    `cover()` draws it (`thumbnails.md`)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "ranked_long", ROOT / "projects/tinnitus-long/tinnitus-treatments-ranked.py")
    long_ = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(long_)
    return long_.thumbs(out, portrait=True, variants=variants)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-treatments-ranked-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-treatments-ranked-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, opener_holds=True,
                                        tail=1.5)
    thumb = thumbs(out.with_name(out.stem + "-thumb.jpg"))[0]
    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    if "--thumb" in sys.argv or "--thumb-variants" in sys.argv:
        for q in thumbs(Path.home() / "Desktop/tinnitus-treatments-ranked-short-thumb.jpg",
                        variants="--thumb-variants" in sys.argv):
            print(q)
    else:
        main()
