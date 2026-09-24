"""Can your neck change your tinnitus? ~45s Short.

Source: tinnitus-blog/content/posts/can-neck-tension-cause-tinnitus.mdx, the
same post as the `can-neck-tension-cause-tinnitus` long form.

**It does not compress the long cut.** The long form walks the mechanism, the
two groups of clues, what tightens the neck, the whole routine and the red
flags. This one does the single move: the thirty-second self-test, and what a
change in the sound does and does not mean. Sentence two says the hook's
hidden word, "up".

**Two drawn beats, two silhouettes.** `steps` for the test - it is an
ordered how-to and the portrait track runs down the frame - and a `chapter`
card for the cold close, which reframes the opening question instead of
asking another one (`narration.md`, "A Short's ending loops").

**It opens on the keyboard, not on the long form's stretch.** The pair would
normally share an opening face, but the centred hook block sits at 34% of the
height and the stretch clip puts her head exactly there. The hands-on-keys
shot has nothing above the lower third.

**No medical claims.** The test is described, never sold; "part of the
volume" is the strongest claim in the script, and the close says explicitly
that the neck is not the cause.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/can-neck-tension-cause-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "can-neck-tension-cause-tinnitus"

# Same roster as the long form from this post (a pair is one video).
V = STOCK / "videos"
# **Every clip here was checked as a real 9:16 crop, not on a landscape
# contact sheet.** A vertical cut keeps about 32% of a landscape source's
# width, so a wide shot with a small subject becomes a frame of background -
# which is exactly what the first cut shipped: a silhouette in the bottom
# corner with four seconds of empty wall beside it, and a keyboard whose
# hands were outside the crop. Prefer a close or medium shot where the
# subject already fills the frame; a wide can almost never be rescued by
# `clip_ax`.
KEYBOARD = V / "hands-stretching-fingers-desk-night-dark/36392564.mp4"
STRETCH = V / "man-stretching-neck-shoulders-at-desk-office-evening-dark/35331903.mp4"
THINK = V / "man-sitting-at-desk-night-close-up-thinking-dark/9618041.mp4"
THERAPIST = V / "physical-therapist-neck-massage-treatment-dark/6186698.mp4"
MONITOR = V / "man-working-late-laptop-desk-night-dark-silhouette/34492301.mp4"
LAMP = V / "close-up-hand-turning-off-desk-lamp-night-dark/8631662.mp4"
STEAM = V / "steam-rising-hot-water-dark-night/29686188.mp4"
TYPING = V / "close-up-hands-typing-laptop-night-warm-lamp-dark/34771078.mp4"
AWAKE = V / "woman-lying-awake-in-bed-at-night-dark-bedroom-close/6753383.mp4"
FOGWALK = V / "woman-walking-at-night-calm-street-dark/11839716.mp4"

THUMB_PHOTO = (STOCK / "photos/woman-holding-her-neck-pain-dark-portrait-portrait"
               / "12572742.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

HOOK = "It takes [30 seconds] to find out"

# The closing statement, drawn by the opener's own `HookOverlay` over the last
# shot instead of by a `chapter` slate - see `shorts.md`, "The outro is the
# opener's twin". The pill lands on "volume" as the voice says it.
OUTRO = "Your neck is not the cause. It might be the [volume]."

SENTENCES = [
    # The title question, subject named in line one.
    ("Can your neck really change your tinnitus?",),
    # **The hidden token is the number, and it is said second.** The first
    # version hid "up" in "the ringing can turn [up]", which every viewer
    # fills in before the bar has finished animating - so the opener spent
    # five seconds confirming what the line had already given away. A
    # duration cannot be guessed, and it lands at ~3s here rather than 5.3s.
    ("30 seconds is enough to find out -",
     "and for a lot of people, the answer is yes."),
    # Hinge into the beat, its own sentence so it cannot eat reveal zero.
    ("Try these three moves, sitting where you are.",),
    # steps - one caption chunk per node.
    ("Turn your head slowly to each side.",
     "Clench your jaw, then let it go.",
     "Press the tender spots at the base of your skull."),
    ("If the sound shifts, even for a second,",
     "your neck is part of the volume."),
    ("That does not mean your neck started it.",),
    ("It means one of the sliders is one you can reach.",),
    ("Heat on the neck first, then slow turns and tilts, inside a pain-free "
     "range.",),
    ("And a screen at eye level, so your chin is not forward all day.",),
    # Hand-off into the full-screen statement.
    ("So tonight, start with the neck.",),
    # The cold close. It is drawn by `outro=` in the opener's own type now,
    # not by a `chapter` card, so this line is spoken over footage.
    ("Your neck is not the cause. It might be the volume.",),
]

GAPS = [0.80,   # into the answer; the reveal has to land before ~7s
        1.00,   # after the answer, a real silence
        0.90,   # the hinge into the beat
        0.85,
        0.90,
        0.55,
        0.85,
        0.70,
        0.85,
        0.80,   # into the card
        0.34]   # cold close, nothing after it

SHOTS = [
    # Shot one is the only slot the hook constrains: it clears at ~4s, so
    # nothing after it has to keep 34% of the height free. A hand on a lit
    # keyboard fills the lower two thirds and leaves that band empty.
    Shot(clip=KEYBOARD, clip_at=1.0, clip_ax=0.50),
    Shot(clip=STRETCH, clip_at=4.0, clip_ax=0.50),
    Shot(clip=THINK, clip_at=4.0, clip_ax=0.50),
    Shot(graphic="steps",
         payload=([("Turn your head", "\U0001F504"),
                   ("Clench, then release", "\U0001F62C"),
                   ("Press the tender spots", "\U0001F446")],
                  "THE 30-SECOND CHECK")),
    Shot(clip=THERAPIST, clip_at=11.0, clip_ax=0.50),
    Shot(clip=MONITOR, clip_at=0.5, clip_ax=0.50),
    # A hand reaching for the lamp, under "one of the sliders you can reach".
    Shot(clip=LAMP, clip_at=3.0, clip_ax=0.50),
    Shot(clip=STEAM, clip_at=2.0, clip_ax=0.40),
    Shot(clip=TYPING, clip_at=2.0, clip_ax=0.50),
    Shot(clip=AWAKE, clip_at=3.0, clip_ax=0.50),
    # The outro card lands on this one and holds to the last frame.
    Shot(clip=FOGWALK, clip_at=8.0, clip_ax=0.50),
]


def main() -> None:
    out = Path.home() / "Desktop/can-neck-tension-cause-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.can-neck-tension-cause-tinnitus-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        hook=HOOK, outro=OUTRO,
                                        # The pill lands on the last word of
                                        # the last line, so the default 1.2s
                                        # tail left the finished statement on
                                        # screen for four frames. The card is
                                        # what the viewer loops out of - give
                                        # it a beat to be read.
                                        tail=2.6)

    # Same source and headline as the long form.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "THE\n30-SECOND\n[NECK TEST]", image=THUMB_PHOTO,
        accent="red", ax=0.5, zoom=1.0, at=0.34, band="top", size=200)

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
