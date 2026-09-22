"""How do you explain tinnitus to someone who cannot hear it? ~45s Short.

Source: tinnitus-blog/content/posts/explain-tinnitus-to-others.mdx, the same
post as the `explain-tinnitus-to-others` long form.

**It does not compress the long cut.** The long form walks why nobody can hear
it, the range, the one-minute script, the comparisons, the asks and the red
flags. This one does the single move: stop describing the sound, end on a
request. Sentence two says that, and the hook's hidden word is "request".

**Two drawn beats, two silhouettes.** `diagram` (straight chain) for the
three lines - not `steps`, which every recent Short on this channel has run -
and a `chapter` card for the cold close, which answers the opening line.

**No medical claims.** The only "helps" is the viewer's own ask.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/explain-tinnitus-to-others.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "explain-tinnitus-to-others"

# Same roster as the long form from this post (a pair is one video).
V = STOCK / "videos"
CAMPFIRE_2 = V / "people-talking-campfire-night/8976330.mp4"
SILHOUETTE = V / "man-and-woman-talking-night-window-silhouette/10627044.mp4"
COUPLE_SOFA = V / "couple-conversation-sofa-lamp-night/6970293.mp4"
MUG = V / "hands-holding-mug-talking-dark/6245131.mp4"
KITCHEN = V / "couple-talking-kitchen-night-dark/7669064.mp4"
SHOULDER = V / "hand-on-shoulder-comfort-dark/4763989.mp4"
WALK_TWO = V / "friends-walking-together-night-street/8101864.mp4"
STATIC_TV = V / "tv-static-noise-screen-dark/6955107.mp4"
OFFICE = V / "coworkers-talking-office-meeting-evening-dark/7668496.mp4"
PATIO = V / "friends-sitting-outdoor-patio-night-talking/7645075.mp4"
CAFE_FRONT = V / "cafe-terrace-night-lights-people/10882093.mp4"

THUMB_PHOTO = (STOCK / "photos/woman-talking-to-friend-evening-lamp-dark-portrait"
               / "6017586.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

HOOK = "The best explanation ends with a [request]"

SENTENCES = [
    # The title question, subject named in line one.
    ("How do you explain tinnitus to someone who cannot hear it?",),
    # Partial answer that says the hidden word ~4-5s in, and opens "so what
    # is the request?".
    ("The version that works ends with a request, not a description.",),
    ("They will never hear it,",
     "so describing the sound never lands."),
    # Hinge into the diagram, its own sentence so it cannot eat reveal zero.
    ("So keep it to three lines.",),
    # diagram - one caption chunk per node.
    ("What it is: a sound I hear that is not in the room.",
     "Why it changes: quiet rooms make it stand out more.",
     "And one ask: could we keep some soft sound on?"),
    ("That last line is the one that matters.",),
    ("It gives them something to do, instead of something to imagine.",),
    ("And if they need a picture,",
     "it is like a TV with a little static that never fully mutes."),
    ("At work, ask for a room with a little background hum.",),
    ("With friends, pick the patio over the loud bar.",),
    # Hand-off into the full-screen statement.
    ("So next time, remember this.",),
    # chapter - cold close that answers line one, so the loop reads through.
    ("Do not describe the sound. Ask for what helps.",),
]

GAPS = [0.80,   # into the answer; the reveal has to land before ~7s
        1.00,   # after the answer, a real silence
        0.70,
        0.90,   # the hinge into the diagram
        0.85,
        0.55,
        0.85,
        0.70,
        0.55,
        0.85,
        0.80,   # into the card
        0.34]   # cold close, nothing after it

SHOTS = [
    # Opens on the same clip the long form opens on.
    # Figures sit low in frame, clear of the centred hook.
    Shot(clip=SILHOUETTE, clip_at=1.0),
    Shot(clip=COUPLE_SOFA, clip_at=1.0, clip_ax=0.7),
    Shot(clip=KITCHEN, clip_at=0.5, clip_ax=0.6),
    Shot(clip=MUG, clip_at=0.5, clip_ax=0.3),
    Shot(graphic="diagram",
         payload=([("What it is", "a sound only I hear", "\U0001F514"),
                   ("Why it changes", "quiet makes it stand out",
                    "\U0001F92B"),
                   ("One ask", "soft sound on, please", "\U0001F64F")],
                  "THE ONE-MINUTE VERSION", False)),
    Shot(clip=CAMPFIRE_2, clip_at=0.5, clip_ax=0.6),
    Shot(clip=SHOULDER, clip_at=0.5),
    Shot(clip=STATIC_TV, clip_at=1.0, clip_ax=0.3),
    Shot(clip=OFFICE, clip_at=0.5),
    Shot(clip=PATIO, clip_at=1.0, clip_ax=0.4),
    Shot(clip=WALK_TWO, clip_at=6.0, clip_ax=0.5),
    Shot(graphic="chapter",
         payload=("DON'T DESCRIBE THE SOUND. ASK FOR WHAT HELPS.",)),
]


def main() -> None:
    out = Path.home() / "Desktop/explain-tinnitus-to-others-short.mp4"
    work = Path.home() / "Desktop/.explain-tinnitus-to-others-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        hook=HOOK)

    # Same source and headline as the long form: the title's own question.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "HOW DO YOU\nEXPLAIN\n[TINNITUS?]", image=THUMB_PHOTO,
        accent="red", ax=0.5, zoom=1.0, at=0.34, band="top", size=200)

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
