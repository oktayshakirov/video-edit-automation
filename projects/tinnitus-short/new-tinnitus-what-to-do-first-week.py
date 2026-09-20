"""Tinnitus just started - what do you do tonight? ~45s vertical Short.

Source: tinnitus-blog/content/posts/new-tinnitus-what-to-do-first-week.mdx, the
same post as the `new-tinnitus-what-to-do-first-week` long form.

**It does not compress the long cut.** The long form walks the threat loop, the
seven-day plan, the room setup, the overprotection twist, what not to do and
the red flags. This one does the single move: do not go looking for silence,
here is why, and here is what tonight looks like instead. Sentence two is the
answer, not a hedge.

**Two drawn beats, two silhouettes.** `diagram(loop=True)` - the silence loop,
which is the beat `shorts.md` says to reach for when every recent Short on this
channel has run `grid` plus `steps`, and no Short here has drawn a cycle yet -
then `steps` for the night routine, which is the right shape for a thing with
an order and reads nothing like the chain above it.

**No medical claims.** "Usually" and "most people" are the article's own words
and stay. The exception routes to a same-day visit. The close is cold and
answers the opening line, so the loop reads as one thought.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/new-tinnitus-what-to-do-first-week.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "new-tinnitus-what-to-do-first-week"

# Same roster as the long form from this post (a pair is one video).
SIT_UP = STOCK / "videos/woman-sleeping-dark-bedroom-night/11956220.mp4"
QUIET = STOCK / "videos/quiet-bedroom-night-window-silence-dark/11956317.mp4"
CURTAINS = STOCK / "videos/closing-curtains-at-night-dark-room/6944065.mp4"
BULB = STOCK / "videos/hand-switching-off-bedside-lamp-night/853772.mp4"
FAN = STOCK / "videos/ceiling-fan-spinning-dark-room-night/3069096.mp4"
SOUND_BOX = STOCK / "videos/hand-switching-off-bedside-lamp-night/25951436.mp4"
BREATHE = STOCK / "videos/woman-relaxing-breathing-eyes-closed-dark-room/7191271.mp4"
CALL = STOCK / "videos/man-checking-phone-anxious-dark-room/7280528.mp4"

THUMB_PHOTO = (STOCK / "photos/man-in-black-shirt-user-picked"
               / "8638769.jpg")                      # Pavel Danilyuk, Pexels

VOICE = "mia"      # the female explainer reader, same as the long form.
MUSIC = music.track("night-drift")

SENTENCES = [
    # A Short has no title card, so the first line names the subject and
    # frames the night. Stated, not asked - a rising question mark here read
    # as a query rather than as advice.
    ("Tinnitus just started.",
     "Tonight is the part you can actually change."),

    # Sentence two is the answer, not a hedge.
    ("So do not go looking for silence.",),

    ("A silent room is where tinnitus is loudest.",),

    # The hinge into the diagram gets its own sentence, so it cannot eat the
    # first node's reveal.
    ("Because a quiet room starts a loop.",),

    # diagram, loop=True - one caption chunk per node.
    ("The room goes quiet.",
     "Your brain turns its own gain up to fill the gap.",
     "So the ringing stands out more, and you want it quieter still."),

    ("The way out is to never let the room go fully silent.",),

    ("So set tonight up like this.",),

    # steps - one caption chunk per node.
    ("Soft sound on, and kept low.",
     "Lights down about forty minutes before bed.",
     "Screens away.",
     "And the same wake time tomorrow."),

    ("Low enough that you can still faintly hear the ringing -",
     "that is the level to aim for."),

    ("One exception.",
     "Sudden hearing loss, dizziness, or ear pain -",
     "get seen the same day."),

    # Cold close that answers line one, so the loop reads as continuous.
    ("Tonight, do not chase the quiet.",),
]

# 0.85 in front of the flat answer, 0.90 in front of each beat so the hinge
# lands, 0.80 before the exception and before the close so the two do not run
# together, and 0.34 on the last line - a cold close, nothing after it.
# `RUN_BREAK_GAP` is 1.00: a gap at or above it is a real silence file in the
# concat and always happens, while anything under it is only a *request* that
# `_pad_pause` drops silently when the model ran the two sentences together.
# The pause in front of the answer was asked for by name, so it is 1.00 rather
# than the 0.90 the placement table would otherwise suggest - guaranteed beats
# nominally correct.
GAPS = [1.00,   # the answer has to land into a real silence, not run on
        0.85,
        0.70,
        0.90,   # the hinge into the diagram
        0.85,
        0.75,
        0.90,   # the hinge into the steps
        0.70,
        0.85,   # before the turn into the exception
        0.80,
        0.34]   # a cold close, nothing after it

SHOTS = [
    # Opens on the same clip the long form opens on.
    Shot(clip=CURTAINS, clip_at=2.0, clip_ax=0.45),
    Shot(clip=SIT_UP),
    Shot(clip=QUIET, clip_ax=0.15),
    # A filament going out - the picture of the quiet, dark room.
    Shot(clip=BULB),
    Shot(graphic="diagram",
         payload=([("The room goes quiet", "nothing else to hear",
                    "\U0001F319"),
                   ("Your brain turns the gain up", "to fill the gap",
                    "\U0001F506"),
                   ("The ringing stands out", "so you want more quiet",
                    "\U0001F514")],
                  "WHY SILENCE BACKFIRES", True)),
    # A fan is one of the article's own sound-enrichment suggestions, so the
    # picture names the noun the line does.
    Shot(clip=FAN),
    # Replaces a bedside phone whose screen was a photo gallery - the prop's
    # screen is read, not merely seen.
    Shot(clip=SOUND_BOX, clip_at=24.0),
    Shot(graphic="steps",
         payload=([("Soft sound, kept low", "\U0001F30A"),
                   ("Lights down early", "\U0001F4A1"),
                   ("Screens away", "\U0001F6AB"),
                   ("Same wake time", "\U0001F305")],
                  "TONIGHT")),
    Shot(clip=BREATHE, clip_ax=0.25),
    Shot(clip=CALL),
    Shot(clip=CURTAINS, clip_at=12.0, clip_ax=0.45),
]


def main() -> None:
    out = Path.home() / "Desktop/new-tinnitus-first-week-short.mp4"
    work = Path.home() / "Desktop/.new-tinnitus-first-week-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)

    # Same source and headline as the long form. The rows are forced rather
    # than wrapped, so no phrase is torn across a break - "NEW TINNITUS." /
    # "WHAT DO YOU" / "DO FIRST?" - and three short rows let the size search
    # go much larger than two long ones did. `zoom` above 1.0 buys vertical
    # slack so `at` can push the subject clear of the type band.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "NEW TINNITUS.\nWHAT DO YOU\nDO [FIRST?]", image=THUMB_PHOTO,
        accent="red", ax=0.5, zoom=1.0, at=0.34, band="bottom", size=210)
    # **`band` is "bottom" here and that is forced by the picture, not a
    # preference.** The subject's head and hands occupy the top half of the
    # 9:16 crop, so a top band prints the headline straight across his face -
    # the one thing the thumbnail checklist calls fatal - and the renderer
    # then crushes the band dark to keep the type legible. His black t-shirt
    # fills the lower third and is the best type ground in the frame. The
    # bottom band also clears the Shorts grid's play count.

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
