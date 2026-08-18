"""Why tinnitus is worse at night. ~50s tinnitus short.

Source: tinnitus-blog/content/posts/tinnitus-and-sleep.mdx, the same post as
the `tinnitus-sleep-long` explainer.

**It does not compress the long cut.** That video walks the whole guide — the
contrast mechanism, why chasing quiet backfires, what to play, the volume rule,
the twenty-minute rule, when to see somebody. None of that fits in a short and
trying would produce a trailer for a video nobody has watched.

What survives is the **reframe, the trap, and the setting**: your room got
quieter; making it quieter still is the instinct and it backfires; and the
sound goes *just below* the ringing rather than on top of it. The reframe stops
the scroll, the trap is the counterintuitive turn that keeps it, and the
setting is the thing they can act on tonight.

**Two drawn beats, two silhouettes**: `grid` for the two rooms and `steps` for
the three things to do. Cards against a numbered track are genuinely different
outlines; the fix has an order, which is what `steps` shows and a list does not.
Neither is a `checklist` — that beat still carries thecrypto.wiki's gold as a
module constant and renders off-brand here.

**The long cut draws the two rooms with `compare` and this one cannot.** Only
`grid`, `steps` and `bars` are wired for 9:16 — `compare` raises rather than
falling through, which is the right failure. It is no loss here: `compare`
wants three items a side and the portrait layout stacks the columns, so three
and three would be six rows of type on a phone. Two `grid` cards with a second
line each carry the same contrast in half the height.

**Rain rather than water.** The first cut leaned on the calm-water stock twice
and it illustrated nothing — the script is about bedrooms. Rain on a window is
one of the sounds the post actually recommends, so the footage is now the
subject rather than wallpaper. One water shot survives, under the line it
belongs to.

**No site photographs at all.** The long-form module docstring has the full
screening — the library's sleep images are a daylight hammock, a woman cheering
at a television, and a sleeping child at L220. In 9:16 the crop is tighter and
the problem is worse, so this cut is stock clips and the two beats.

**No medical claims**, and short form is where that is hardest because there is
no room to qualify anything. The sound is described as covering the ringing,
never as treating it. **The close asks them to try it, not to save it** — the
first cut said "save this for tonight", and saving a video is not the action
the video is about.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus/tinnitus-and-sleep.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Screened across their length by the long-form build from this post; the
# trailing comment is the luma/saturation range over the whole clip.
AWAKE = STOCK / "videos/insomnia-awake-night-bed"
NIGHT = STOCK / "videos/sleeping-night-calm-dark"
WATER = STOCK / "videos/calm-water-ripple-dark"
SOUND = STOCK / "videos/sound-wave-visualization-dark"
RAIN = STOCK / "videos/rain-on-window-at-night-dark"
LAMP = STOCK / "videos/bedside-lamp-dark-bedroom-night"
TIREDM = STOCK / "videos/tired-man-rubbing-temples-dark"
BEDW = STOCK / "videos/caucasian-woman-awake-in-bed-night-dark-bedroom"
TIREDP = STOCK / "videos/stressed-man-dark-studio-portrait-grey"

# **Same source the long form uses, and back to the user's original pick.**
# It is landscape (6720x4480), which the earlier version of this file called
# structurally unworkable for 9:16 — that turned out to be true for a
# different landscape photo (a woman lying fully horizontal, so the crop had
# to throw away her whole body) and not for this one, where she is shot from
# directly overhead: her face sits high and off-centre rather than spanning
# the frame, so a portrait crop only has to pick a horizontal slice, not
# recover a lost axis. `ax=0.10` centres that slice on her face and the phone.
THUMB_PHOTO = STOCK / "photos/woman-sleeping-beside-smartphone/9787924.jpg"

VOICE = "mia-calm"              # af_heart at 1.00, the same reader as the long
                                # form from this post — a short and a long
                                # video on one channel in two voices is two
                                # channels. `ivy` was tried and cut. Candidate.

SENTENCES = [
    ("Your tinnitus is not worse at night.",),

    ("Your room is.",),

    # **The lead-in goes here, not inside the beat.** A drawn beat times its
    # reveals off the caption starts of its own sentence, so a spare line in
    # that span eats reveal zero and shunts every row one line late.
    ("All day, traffic and voices",
     "cover part of the sound.",
     "Then you turn everything off."),

    # The beat. One caption chunk per card, in card order, nothing else in
    # the span.
    ("All day, something is covering it.",
     "At night, nothing is."),

    # The trap — the counterintuitive turn, and the reason to keep watching
    # past the reframe.
    ("So the instinct is",
     "to make it quieter still.",
     "Earplugs. Thicker curtains."),

    ("Every one of those",
     "removes more of the sound",
     "that was covering it."),

    ("So do not sleep in silence.",
     "Put steady sound in the room."),

    ("Rain, a fan, or brown noise.",
     "On a speaker, not in your ears."),

    ("And here is the part",
     "almost everybody gets wrong."),

    ("Do not turn it up",
     "until the ringing disappears."),

    ("Set it just below.",
     "Quiet enough that you can still",
     "faintly hear it underneath."),

    # The fix as a vertical track — a completely different silhouette from
    # the cards, which is the point of using two beats at all.
    ("On a speaker, not earbuds.",
     "Just below the ringing.",
     "Up if you are still awake in twenty minutes."),

    ("Try it tonight.",
     "Just below, not on top."),
]

SHOTS = [
    # 1 — motion on frame one, and a face. A Short is judged in its first
    # second and this reads as "awake at 3am" in a fifth of one.
    Shot(clip=BEDW / "30285719.mp4"),                # L24 S10

    Shot(clip=LAMP / "10387906.mp4"),                # L36-46 S23-29

    Shot(clip=SOUND / "34645273.mp4"),               # L7 S2

    Shot(graphic="grid",
         payload=([("Your day",
                    "Traffic, voices, something to do"),
                   ("Your bedroom at 11pm",
                    "Silence, and nothing but the ringing")],
                  "SAME EARS, DIFFERENT ROOM")),

    Shot(clip=TIREDP / "6415592.mp4"),               # L18-19 S6

    Shot(clip=AWAKE / "8376628.mp4", clip_at=2.0),   # L25-30 S13-17

    Shot(clip=RAIN / "4458918.mp4"),                 # L20-21 S16-23

    # **Not 34977302.** It screens at L15 S17 and passes the box, and it is a
    # green-lit apartment block — the one hue that cuts hardest against this
    # palette. The box measures brightness; hue against the brand is a separate
    # judgement it does not make for you.
    Shot(clip=RAIN / "15161525.mp4"),                # L31 S13

    Shot(clip=NIGHT / "11956219.mp4"),               # L29-31 S6

    Shot(clip=SOUND / "34645273.mp4", clip_at=8.0),

    # The one water shot. In a short every shot carries a burned caption, so
    # the "only with text over it" rule is satisfied by construction — but it
    # still only earns a place under the line it actually illustrates.
    Shot(clip=WATER / "11028763.mp4"),               # L28-31 S6-7

    Shot(graphic="steps",
         payload=(["On a speaker, not earbuds",
                   "Just below the ringing",
                   "Up after 20 minutes awake"],
                  "TONIGHT")),

    Shot(clip=NIGHT / "11956328.mp4", clip_at=4.0),  # L28 S4-5
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-sleep-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-sleep-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE)
    # **Same headline as the long form from this post**, so the pair reads as
    # one. "Your room got quieter" was tried and the user kept this one.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Stop sleeping in [silence]", image=THUMB_PHOTO, accent="red",
        ax=0.10, zoom=1.0)
    print(f"{path}  {total:.1f}s")
    print(f"{thumb}")


if __name__ == "__main__":
    main()
