"""Are your teeth touching right now? ~45s Short.

Source: tinnitus-blog/content/posts/tmj-and-tinnitus-the-jaw-connection.mdx,
the same post as the `tmj-and-tinnitus` long form.

**It does not compress the long cut.** The long form walks the anatomy, the
four fingerprints, what clenches a jaw, the whole routine and the red flags.
This one does the single move: the resting jaw position, checked while the
video is still playing. It is the one thing in the article a viewer can act
on inside forty seconds.

**The opener is a `Search`, the same device as the long form**, on the
user's call after seeing the first cut. The last three Shorts on this
channel all opened on the redacted hook, so the rotation still holds; what
changed is that both halves of the pair now open on somebody typing their
own question, which is what makes them read as one piece. **The query is a
different one from the long form's** ("can tmj cause tinnitus") so the two
are not competing for one search-results page - this is the phrase a person
types once they have already noticed the sound moving.

**One drawn beat.** `steps` in its portrait track, for the resting position -
it is an ordered instruction and the frame has the height to spare. The
closing statement is the opener's own type (`outro=`), not a `chapter`
slate.

**The close is a directive, not an observation.** The first cut ended on
"two fingers in front of your ear - that is the joint", and the user's note
was that it leaves the end open: it names the thing and then stops, so there
is nothing for the viewer to do with it. It closes on the instruction the
video actually earned instead, which is still a cold close
(`narration.md`, "A Short's ending loops; it does not ask") and now answers
the question the search bar typed out at the top.

**No medical claims.** "Part of its volume" is the strongest thing said, and
the line before the close says explicitly that the jaw did not start it.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tmj-and-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Search
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "tmj-and-tinnitus-the-jaw-connection"

# Same roster as the long form from this post - a pair is one video, and the
# audit counts their uses together. **Every clip was checked as a real 9:16
# crop**, not on a landscape contact sheet: a vertical cut keeps about 32% of
# a landscape source's width, so these are the close and medium shots of the
# roster and the wides stayed in the long form.
V = STOCK / "videos"
CHEEK = V / "close-up-hand-on-cheek-jaw-dark-low-key/5119257.mp4"
MOUTH = V / "man-stretching-mouth-opening-jaw-dark/6144020.mp4"
PROFILE = V / "close-up-hand-on-cheek-jaw-dark-low-key/34725795.mp4"
JAWHANDS = V / "hand-holding-jaw-pain-dark/19149084.mp4"
KEYS = V / "tired-office-worker-late-night-screen-glow-dark/34771086.mp4"
CHEW = V / "person-chewing-food-dark-low-light/7801573.mp4"
KETTLE = V / "steam-kettle-hot-water-night-dark-kitchen/35674426.mp4"
STREET = V / "man-walking-home-late-night-empty-street/7251411.mp4"
HAND = V / "close-up-hands-stretching-fingers-night-dark/7298371.mp4"

# The user's own pick, by URL, and the same file the long form uses.
THUMB_PHOTO = (STOCK / "photos/close-up-shot-of-a-pretty-woman-10648949"
               / "10648949.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

# The viewer's own question, typing itself. No answer is shown - the answer
# is the video (`shorts.md`, "Choosing the opener").
# **Keep the query short.** "why does my tinnitus change when i move my jaw"
# is a real search and it types for 5.4 seconds, which pushes the burned
# captions past the point the opening is decided; the bar has to be gone by
# ~3s (`shorts.md`, "the gap closes by ~3s").
OPENER = Search("why does my tinnitus change")

# The closing statement, drawn by the opener's own type over the last shot.
# The pill lands on "hour" as the voice says it. It is the instruction the
# forty seconds earned, which is what a Short's last line should be.
OUTRO = "Teeth apart. Check again in an [hour]."

SENTENCES = [
    # The title question, subject named in line one.
    ("Can your jaw really change your tinnitus?",),
    # Sentence two does not hand over the verdict - it hands over a thing to
    # check, which is new information and opens the bigger question.
    ("Quick check -",
     "are your teeth touching right now?"),
    ("They are only meant to touch when you chew or swallow.",),
    ("The rest of the day they should sit slightly apart,",
     "and for a lot of people they never do."),
    # Hinge into the beat, its own sentence so it cannot eat reveal zero.
    ("So here is the resting position, and you can set it while I say it.",),
    # steps - one caption chunk per node.
    ("Teeth apart, a millimetre or two.",
     "Lips together.",
     "And the tip of your tongue on the roof of your mouth."),
    ("That takes the load off a joint sitting right in front of your ear "
     "canal.",),
    ("If the ringing shifts while your jaw moves, your jaw is part of its "
     "volume.",),
    ("That does not mean your jaw started it.",),
    ("It means one of the things making it louder is one you can feel.",),
    # The cold close, drawn by `outro=`.
    ("So set your teeth apart now, and check again in an hour.",),
]

GAPS = [0.80,   # into the check
        1.00,   # a real silence after the question; the stamp has landed
        0.85,
        0.90,
        0.90,   # the hinge into the beat
        0.85,
        0.85,
        0.90,
        0.55,
        0.80,   # into the closing statement
        0.34]   # cold close, nothing after it

SHOTS = [
    # **Shot one is the only slot the opener constrains** - its block sits at
    # 34% of the height and clears by ~3s - and it is also the shot the
    # viewer decides on, so it is the clearest frame in the cut rather than
    # the moodiest. `clip_ay` drops the crop so the face sits under the
    # quote instead of behind it.
    Shot(clip=JAWHANDS, clip_at=12.0, clip_ax=0.50, clip_ay=0.25),
    # **Three of these `clip_ax` values are not 0.5, and that is the whole
    # difference between a shot and a frame of wall.** Checked as real 9:16
    # crops: at the centred default, MOUTH is a black rectangle with a
    # sliver of chin up the right edge, PROFILE is black outright, and
    # CHEEK is an unreadable smudge. Every subject in this roster sits
    # right of centre or hard left in its landscape frame.
    Shot(clip=MOUTH, clip_at=0.5, clip_ax=0.85),
    Shot(clip=CHEW, clip_at=10.0, clip_ax=0.50),
    Shot(clip=KEYS, clip_at=0.0, clip_ax=0.50),
    Shot(clip=CHEEK, clip_at=0.5, clip_ax=0.25),
    Shot(graphic="steps",
         payload=([("Teeth apart", "\U0001F62E"),
                   ("Lips together", "\U0001F910"),
                   ("Tongue on the roof", "\U0001F446")],
                  "THE RESTING POSITION")),
    Shot(clip=PROFILE, clip_at=0.5, clip_ax=0.90),
    Shot(clip=HAND, clip_at=1.0, clip_ax=0.50),
    Shot(clip=KETTLE, clip_at=8.0, clip_ax=0.50),
    Shot(clip=CHEW, clip_at=19.0, clip_ax=0.50),
    # The outro card lands on this one and holds to the final frame.
    Shot(clip=STREET, clip_at=18.0, clip_ax=0.50),
]


def main() -> None:
    out = Path.home() / "Desktop/tmj-and-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.tmj-and-tinnitus-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, outro=OUTRO,
                                        # The pill lands on the last word of
                                        # the last line; the card is what the
                                        # viewer loops out of, so give it a
                                        # beat to be read.
                                        tail=2.6)

    # Same source and headline as the long form, in four short forced rows at
    # a raised size - the vertical renderer's size search is capped by the
    # longest row, so two full-width rows read small.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Can your jaw\nchange your\n[tinnitus?]", image=THUMB_PHOTO,
        accent="red", ax=0.45, zoom=1.0, at=0.34, band="bottom", size=240)
    # **`at=` is inert on this source and that is worth knowing.** The file
    # the user picked is 6000x4574, so a 9:16 cover crop uses its whole
    # height and keeps ~55% of its width: there is no vertical slack for
    # `at` to place, and only `ax` moves anything. It is the cost of a
    # landscape source on a vertical thumbnail, which is why the rule is to
    # fetch `orientation=portrait` for a Short; the crop lands on the eye,
    # cheek and jawline rather than the whole face.

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
