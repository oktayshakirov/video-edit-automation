"""White noise vs brown noise for tinnitus - ~43s vertical Short.

Source: tinnitus-blog/content/posts/brown-noise-vs-white-noise-for-tinnitus.mdx,
the same post as the `brown-noise-vs-white-noise-for-tinnitus` long form.

**It does not compress the long cut.** The long form walks the five colours,
the pitch-matching, partial masking and notched therapy across six chapters.
What survives here is the single move a scroller has not heard: the colour is
the least important choice, and the real mistake is turning the volume up
until the ringing is gone - which the article says starts a "volume arms
race", each week needing a little more for the same effect.

**One drawn beat, and it is the new one.** Every recent tinnitus Short has
run `grid` + `steps`; this one uses `diagram` with `loop=True` for the arms
race - turn it up, the brain adjusts, turn it up again - which is a real
feedback cycle nothing else in the library can draw, and its portrait layout
(chain down the frame, feedback arrow up an inset left channel) shipped with
the beats rework. The close is a `chapter` full-screen statement, a different
silhouette.

**The opening question is split** - "Which noise colour is best for your
tinnitus?" then, after a short beat, "White, pink, or brown?" - so the three
options land as their own line instead of racing out on the tail of the
question.

**No medical claims.** Masking is described by what it does - it overlaps the
frequency, it gives partial cover, it leaves room for habituation - never as a
treatment. The close is the action, "try it tonight", not "save this", and
there is no disclaimer line (long-form only, per narration.md).

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/brown-noise-vs-white-noise-for-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Same roster as the long form from this post (a pair is one video). Every
# clip watched frame-by-frame, not just luma-screened.
LISTEN_M = STOCK / "videos/man-listening-music-dark-room-night"             # 7948198 29.5s L37-42/S6-8 - earphones (opener)
PHONE = STOCK / "videos/man-looking-at-phone-worried-dark"                 # 7699007 13.5s L36/S13 - woman + phone, screen not shown
RAIN = STOCK / "videos/rain-on-window-at-night-dark"                       # 15161525 16s L31/S13
RIPPLE = STOCK / "videos/calm-dark-water-ripple-slow-night"                # 11287848 30s L21/S23
VOL_KNOB = STOCK / "videos/hand-turning-volume-knob-dark"                  # 12213088 10s L15/S7
LAMP = STOCK / "videos/bedside-lamp-dark-bedroom-night"                    # 10387906 25s L46/S24

# A clean object shot - white earbuds on dark fabric - shared with the long
# form's cover. The two-colour headline is the hook; the picture just says
# "sound".
THUMB_PHOTO = (STOCK / "photos"
               / "person-earphones-dark-portrait"
               / "18573077.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # A Short has no title card - the first line is the title question, and
    # the three options get their own line after a beat.
    ("Which noise colour is best for your tinnitus?",),
    ("White, pink, or brown?",),

    ("The honest answer:",
     "the colour barely matters."),

    ("Match it roughly to your pitch -",
     "white or pink for a high ring, brown for a low hum -",
     "and move on."),

    ("Because the mistake almost everyone makes is the volume.",),

    ("Turning it up until the ringing disappears feels great.",
     "It also backfires."),

    # diagram, loop=True - one caption chunk per node.
    ("You turn it up to bury the ringing.",
     "Your brain settles against that new level.",
     "So next week you turn it up again."),

    ("The fix is partial masking.",
     "Set it just below the ringing, so you can still faintly hear it "
     "underneath."),

    # chapter - full-screen statement, the payoff line.
    ("So it was never really the colour.",
     "It is the volume."),

    ("Try it tonight.",),
]

# One float per sentence. Load-bearing: 0.50 after the question so "white,
# pink, or brown" is its own line, 0.70 before the answer, 2.20 on the
# diagram's own sentence so the feedback arrow has room to close, 0.90 before
# the full-screen line and 0.80 before the close.
GAPS = [0.50,
        0.70,
        0.50,
        0.70,
        0.70,
        2.20,
        0.55,
        0.90,
        0.80,
        0.80]

SHOTS = [
    # Opens on the same face the long form opens on - a person listening.
    Shot(clip=LISTEN_M / "7948198.mp4", clip_at=8.0),
    Shot(clip=PHONE / "7699007.mp4"),
    Shot(clip=RAIN / "15161525.mp4"),
    Shot(clip=RIPPLE / "11287848.mp4"),
    Shot(clip=VOL_KNOB / "12213088.mp4"),
    Shot(clip=PHONE / "7699007.mp4", clip_at=5.0),
    Shot(graphic="diagram",
         payload=([("You turn it up to bury the ringing", None, "\U0001F508"),
                   ("Your brain settles against it", None, "\U0001F9E0"),
                   ("Next week you turn it up again", None, "\U0001F4C8")],
                  "THE VOLUME ARMS RACE", True)),
    Shot(clip=LAMP / "10387906.mp4"),
    Shot(graphic="chapter", payload=("IT IS THE VOLUME.",)),
    Shot(clip=RIPPLE / "11287848.mp4", clip_at=16.0),
]


def main() -> None:
    out = Path.home() / "Desktop/brown-noise-vs-white-noise-short.mp4"
    work = Path.home() / "Desktop/.brown-white-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        keep_work=True)

    # The headline colour-codes each noise to its own box - {white noise} on a
    # pale plate, [brown] on a brown one. Object shot, no face to place, so
    # `band="bottom"` keeps the type off the earbud in the upper frame.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "{White noise} or [brown]?", image=THUMB_PHOTO,
        accent="brown", accent2="paper", ax=0.5, zoom=1.1, band="bottom")

    yt = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), TINNITUS,
        "{White noise} or [brown noise]?", image=THUMB_PHOTO,
        accent="brown", accent2="paper")

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Reel cover (Instagram, Facebook)")
    print(f"{yt}   <- YouTube thumbnail")


if __name__ == "__main__":
    main()
