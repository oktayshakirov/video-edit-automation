"""Why do so many musicians have tinnitus? ~45s Short.

Source: tinnitus-blog/content/posts/tinnitus-in-musicians.mdx, the same post
as the `tinnitus-in-musicians` long form.

**This one is the long form condensed, and that is deliberate** (the user's
call, 2026-10-02). Every other pair on this channel writes the Short on a
different angle from the long - `shorts.md`'s "it does not compress the long
cut" - and here the long form's own opening was judged the stronger piece of
writing, so the Short takes it: the same title question, the same `Counter`
spinning to 42.6%, the same spine (the figure, where the dose really comes
from, the three things that stack up, what the protection actually does).

What is dropped rather than shortened: the named musicians are one line
instead of a `grid`, the three risk factors lose their chapter, the
hearing-test routing belongs to the long form, and the close is a directive
rather than the long form's question (`narration.md`, "A Short's ending
loops; it does not ask"). **If this approach reads better than the
write-them-apart rule, `shorts.md` gets rewritten around it.**

**One drawn beat, and it is the long form's `grid` of names** (the user's
call on the first cut: list the musicians the way the long form does, with
the band on the card, and no karaoke captions over it). A drawn beat burns no
captions already, so that falls out of using the beat rather than needing a
flag - and it generalises: a Short does not have to carry captions through a
segment that explains itself.

The figure beat the long form draws (`bars`, 42.6% against 13.2%) is
deliberately *not* here: the `Counter` puts 42.6% on screen in the first
three seconds, so drawing it again at eight seconds is the same claim twice.
The three things that stack up run as narration over footage instead - two
beats of the same silhouette in one Short is the thing `shorts.md` bans, and
the names are the better use of the one slot.

**`gauge` was tried first and will not render** - `shorts.md` says it
transfers to 9:16, `crypto/build.py`'s whitelist says it does not, and the
code is the one that raises. Settling that needs a rendered portrait frame
and a whitelist change, which is not this cut's job.

**Captions do not run under the opener.** `hook_mutes_captions=True`, the
default, which the 2026-09-27 note had told a non-hook opener to turn off -
see `shorts.md`, "Captions never run under an opener". The burned line starts
at the first sentence after the `Counter` has gone.

**No medical claims.** The protection lines say what the gear does to the
dose, never what it does to anybody's tinnitus.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-in-musicians.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Counter
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "tinnitus-in-musicians"

# Same roster as the long form from this post - a pair is one video. **Every
# clip was checked as a real 9:16 crop**, not on a landscape sheet: these are
# the close and medium shots and the wides stayed in the long form.
V = STOCK / "videos"
BAND = V / "band-rehearsal-room-dark/8513516.mp4"
SINGER = V / "singer-microphone-live-concert-dark/4142312.mp4"
CROWD = V / "concert-crowd-night-stage-lights/13082773.mp4"
GUITAR = V / "guitarist-live-concert-dark-stage/15348443.mp4"
DJ = V / "dj-headphones-booth-night/30896727.mp4"
MONITOR = V / "microphone-studio-dark-low-key/4962188.mp4"
FADERS = V / "hands-on-mixing-console-faders-dark/12213084.mp4"
DESK = V / "sound-engineer-mixing-desk-concert/13968826.mp4"
CORRIDOR = V / "guitar-case-corridor-night-dark/35130887.mp4"

# The same portrait source the long form's thumbnail uses.
THUMB_PHOTO = STOCK / "photos/drummer-playing-dark-portrait/15324096.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

# The long form's own opener, on the same figure. It lands on "forty-three"
# as the voice says it, so the number is written early in sentence two.
OPENER = Counter("42.6%", "of musicians", at_word="forty-three")

# The closing statement, in the opener's own type over the last shot. The
# pill lands on "minutes". A cold close, no question.
OUTRO = "Sixty percent. Sixty [minutes]. Then a break."

SENTENCES = [
    # The long form's title question, unchanged.
    ("Why do so many musicians end up with tinnitus?",),
    # The figure, with the counter landing on it. "forty-three" sits five
    # words in so the beat lands at roughly four and a half seconds.
    #
    # **This is two sentences rather than one, and the reason is the caption
    # mute.** Captions resume at the first sentence that *starts* after the
    # opener has gone, so written as one long sentence the burned line did
    # not come back until 9.8s. Split, it resumes at the second half.
    ("Pooled across sixty-seven studies, about forty-three percent of "
     "them.",),
    ("For everybody else, about thirteen.",),
    # Hinge into the beat, its own sentence so it cannot eat reveal zero.
    ("And you already know some of them.",),
    # grid - one caption chunk per card, each written as a sentence a person
    # would say rather than a name read off a list. **The beat burns no
    # captions and that is the point here**: three cards naming three people
    # and their bands do not need a second copy of the same words along the
    # bottom of the frame. The user's note, generalised: a Short does not
    # have to carry captions through a segment that explains itself.
    ("Pete Townshend of The Who has talked about it for years.",
     "So has Chris Martin of Coldplay.",
     "And Lars Ulrich of Metallica."),
    ("The surprising part is where the dose comes from.",),
    ("Not the shows -",
     "the rehearsals and the practice hours nobody counts."),
    ("A loud show runs past a hundred decibels, and a career is thousands "
     "of hours of them.",),
    ("Musician earplugs lower the whole thing evenly instead. Same music, "
     "quieter.",),
    # **The turn to the viewer.** The first cut went from musicians straight
    # into "for headphones, sixty sixty", which is a different subject
    # arriving with no sentence saying why - `shorts.md`'s "anything that
    # changes the register of the video needs a sentence saying why it is
    # happening", and the user's note on this cut. This is that sentence.
    ("And you do not need a stage for that to matter.",),
    # The cold close, drawn by `outro=`.
    ("Your headphones run the same rule. Sixty percent of the volume, "
     "sixty minutes, then a break.",),
]

GAPS = [0.85,   # into the figure
        0.55,   # the two halves of one figure
        0.85,   # into the hinge
        0.90,   # the hinge into the beat
        1.20,   # the beat's three cards
        0.80,
        0.85,
        0.85,
        0.90,   # before the turn to the viewer
        0.80,   # into the closing statement
        0.34]   # cold close, nothing after it

SHOTS = [
    # **Shot one is the only slot the opener constrains** - its block sits at
    # 34% of the height - and it is the shot the viewer decides on, so it is
    # the most legible frame in the cut: a whole band playing, subject in the
    # lower two thirds, dark wall where the counter sits.
    Shot(clip=BAND, clip_at=10.0, clip_ax=0.55, clip_ay=0.40),
    Shot(clip=CROWD, clip_at=1.0, clip_ax=0.50),
    Shot(clip=MONITOR, clip_at=0.5, clip_ax=0.50),
    Shot(clip=SINGER, clip_at=0.5, clip_ax=0.35, clip_ay=0.30),
    Shot(graphic="grid",
         payload=([("Pete Townshend", "The Who", "\U0001F3B8"),
                   ("Chris Martin", "Coldplay", "\U0001F3A4"),
                   ("Lars Ulrich", "Metallica", "\U0001F941")],
                  "ON THE RECORD")),
    Shot(clip=DJ, clip_at=0.5, clip_ax=0.50),
    Shot(clip=GUITAR, clip_at=0.5, clip_ax=0.45),
    # "A loud show runs past a hundred decibels" gets the loud show.
    Shot(clip=CROWD, clip_at=13.0, clip_ax=0.50),
    Shot(clip=FADERS, clip_at=0.0, clip_ax=0.45),
    Shot(clip=DESK, clip_at=0.0, clip_ax=0.55),
    # The outro card lands on this one and holds to the final frame.
    Shot(clip=CORRIDOR, clip_at=1.0, clip_ax=0.50),
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-in-musicians-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-in-musicians-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, outro=OUTRO,
                                        tail=2.6)

    # Same source and headline as the long form, in short forced rows at a
    # raised size - the vertical renderer's size search is capped by the
    # longest row.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Why do so many\nmusicians have\n[tinnitus?]", image=THUMB_PHOTO,
        accent="red", ax=0.50, zoom=1.0, at=0.25, band="bottom", size=240)

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
