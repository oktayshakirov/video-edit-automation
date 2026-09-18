"""Will the ringing after a concert go away - ~45s vertical Short.

Source: tinnitus-blog/content/posts/tinnitus-after-a-concert.mdx, the same post
as the `tinnitus-after-a-concert` long form.

**It does not compress the long cut.** The long form walks the gauge, the
mechanism, the 72-hour do/avoid split, the red flags and protection. This one
does the single move: the answer is usually yes, the clock says what to do,
and here is the next 72 hours. Sentence two is the answer, not a hedge.

**Two drawn beats, two silhouettes, neither of them `grid` + `steps` alone.**
`dial` (the recovery clock, no needle) and `steps` (the next 72 hours). The
dial is the one shape no Short on this channel has used yet.

**No medical claims.** "Usually" is the article's word and stays in both
places it is said. The exception routes to a same-day visit. The close is
cold - it answers the opening question so the loop reads as one thought.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-after-a-concert.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "tinnitus-after-a-concert"

# Same roster as the long form from this post (a pair is one video).
PHONES_UP = STOCK / "videos/concert-crowd-stage-lights-dark/12719510.mp4"
GIG_PURPLE = STOCK / "videos/crowd-cheering-hands-raised-night/37944732.mp4"
HANDS_BLUE = STOCK / "videos/music-festival-crowd-silhouette-dark/7722221.mp4"
GIG_SMALL = STOCK / "videos/live-music-gig-audience-dark/852304.mp4"
WALK_HOME = STOCK / "videos/walking-home-after-concert-night-street/11790102.mp4"
FADERS = STOCK / "videos/sound-engineer-mixing-desk-concert/7586162.mp4"
SITTING = STOCK / "videos/ringing-ears-after-concert/30815457.mp4"
CROWD_PINK = STOCK / "videos/concert-crowd-night-stage-lights/9481013.mp4"

THUMB_PHOTO = (STOCK / "photos/concert-crowd-silhouette-stage-lights-dark"
               / "17905270.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

BANDS = [("Hours to a day", 0.45, "#ffdab9"),
         ("1 to 3 days", 0.75, "#f2b36b"),
         ("Past a week", 1.00, "#e87878")]

SENTENCES = [
    # A Short has no title card - the first line is the title question.
    ("Will the ringing after a concert go away?",),

    # Sentence two is the answer, not a hedge.
    ("Usually, yes - most of the time within three days.",),

    ("Your ears are not broken.",
     "The tiny hair cells inside are worn out,",
     "and your brain turns up its own volume to fill the gap."),

    ("That extra volume is the ringing you hear.",),

    # The hinge into the dial gets its own sentence, so it cannot eat the
    # dial's single reveal.
    ("And how long it lasts tells you what to do.",),

    # dial, value=None - one chunk.
    ("Hours to a day for most people, up to three days for some, "
     "and past a week, get it checked.",),

    ("Until then, do this.",),

    # steps - one caption chunk per node.
    ("Give your ears a few quiet days.",
     "Keep soft sound on, never total silence.",
     "Keep your headphones low.",
     "And sleep, and let it fade."),

    ("One exception.",
     "Sudden hearing loss, dizziness, or ear pain -",
     "get seen the same day."),

    # Cold close that answers line one, so the loop reads as continuous.
    ("Give it quiet, and it usually goes away.",),
]

# 0.85 before the flat answer lands, 1.20 after the dial so the scale can be
# read, 0.80 before the exception and again before the close so the two do
# not run together.
GAPS = [0.60,
        0.85,
        0.55,
        0.60,
        0.55,
        1.20,
        0.55,
        0.60,
        0.80,
        0.34]

SHOTS = [
    # Opens on the same clip the long form opens on.
    Shot(clip=PHONES_UP),
    Shot(clip=GIG_PURPLE),
    Shot(clip=HANDS_BLUE),
    Shot(clip=GIG_SMALL),
    Shot(clip=WALK_HOME),
    Shot(graphic="dial",
         payload=(BANDS, None, "", "HOW LONG IT USUALLY LASTS")),
    Shot(clip=FADERS),
    Shot(graphic="steps",
         payload=([("A few quiet days", "\U0001F92B"),
                   ("Soft sound, not silence", "\U0001F30A"),
                   ("Headphones kept low", "\U0001F3A7"),
                   ("Sleep, let it fade", "\U0001F319")],
                  "THE NEXT 72 HOURS")),
    Shot(clip=SITTING),
    Shot(clip=CROWD_PINK),
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-after-a-concert-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-after-a-concert-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)

    # Same source and headline as the long form. The silhouette sits in the
    # lower half of the 9:16 crop with black above it, so the type goes top.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Ears ringing after a [concert?]", image=THUMB_PHOTO, accent="red",
        ax=0.5, zoom=1.0, band="top")

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
