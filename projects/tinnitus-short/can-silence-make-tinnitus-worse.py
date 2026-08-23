"""Does silence make tinnitus worse. ~45s tinnitus short.

Source: tinnitus-blog/content/posts/can-silence-make-tinnitus-worse.mdx, the
same post as the `tinnitus-silence-long` explainer.

**It does not compress the long cut.** That video walks the whole mechanism -
auditory gain, the loss of natural masking, attention turning inward, the
comparison between a silent room and a quiet one, the volume rule, the red
flags. None of that fits in forty-five seconds and trying would produce a
trailer for a video nobody has watched.

What survives is **the gain, the trap, and the setting**: your hearing turns
itself up when there is nothing coming in; making the room quieter still is
the instinct and it goes the wrong way; and the sound goes *just below* the
ringing rather than over it. The gain is the part a viewer has not heard
before, which is what stops the scroll on a topic this crowded.

**Two drawn beats, two silhouettes**: `checklist` with `flow=True` for the
trap, `steps` for the fix. The narration delivers each verdict itself ("so
earplugs make it stand out more"), so holding the crosses back four seconds
would put the picture behind the voice. A vertical track and a column of
ticked rows are genuinely different outlines, which is the whole point of
using two beats rather than one twice.

**Watch the tick on the checklist.** The brand accent is a pale peach and it
carries less contrast against white item text than the crypto gold does, so
the payoff mark can read weaker than the crosses in front of it. Looked at
before shipping.

**No `compare`.** The long cut draws the silent room against the quiet one
with it, and only `checklist`, `grid`, `steps` and `bars` are wired for 9:16 -
`compare` raises rather than falling through, which is the right failure. It
would be wrong here anyway: three items a side stacks into six rows of type on
a phone.

**No site photographs.** Screened for the long cut and the library fails this
post the same way it failed the sleep one - `silence.jpg`, the article's own
hero, is a teal studio "shh" shot at L138 / S87. In 9:16 the crop is tighter
and the problem is worse, so this cut is stock clips and the two beats.

**No medical claims.** Sound is described as covering the ringing and changing
how much of the room it takes up, never as treating it. The close asks them to
do the thing, not to save the video.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/can-silence-make-tinnitus-worse.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Screened across their length by the long-form build from this post; the
# trailing comment is the luma/saturation range over the whole clip.
# **The old `woman-sitting-alone.../6073058` is out.** It screened as an
# empty dark room and plays as a woman shaving her head; the user caught it at
# 0:04. Screen a clip by watching it, not by looking at one frame of it.
ALONE = STOCK / "videos/man-sitting-alone-dark-apartment-night"
MEDIT = STOCK / "videos/man-meditating-dark-room-calm"
LIBRARY = STOCK / "videos/quiet-library-reading-dark"
FAN = STOCK / "videos/electric-fan-spinning-dark-room"
NEURON = STOCK / "videos/brain-neurons-abstract-dark"
CEIL = STOCK / "videos/ceiling-dark-bedroom-night-calm"
CURT = STOCK / "videos/curtains-window-night-moonlight-dark"
LISTEN = STOCK / "videos/man-listening-music-dark-room-night"
TIREDW = STOCK / "videos/tired-woman-hands-on-face-dark-studio-portrait"
SOUND = STOCK / "videos/sound-wave-visualization-dark"
RAIN = STOCK / "videos/rain-on-window-at-night-dark"

# **Same source as the long form's thumbnail**, per the standing rule that one
# picture serves both aspects. Portrait 4000x6000, L22 S20. Her face sits in
# the upper half of the 9:16 crop, which is why the type goes in the bottom
# band rather than the default top one.
THUMB_PHOTO = STOCK / ("photos/woman-silence-dark-background-portrait-portrait"
                       "/7041828.jpg")

VOICE = "mia"                   # af_heart, the same reader as the long form
                                # from this post - a short and a long video on
                                # one channel in two voices is two channels.
                                # Candidate.

MUSIC = music.track("night-drift")

SENTENCES = [
    # **Every short opens by asking its own title question.** The user's
    # standing note: without it a short starts mid-thought and reads as
    # random, because a Short has no title card, no thumbnail on screen and
    # no chapter list - the viewer arrives with nothing. One line, spoken
    # over the opening face, and the next forty seconds are an answer.
    ("Does silence make tinnitus worse?",),

    ("You get somewhere quiet",
     "and the ringing gets louder.",),

    ("It did not.",),

    ("Your hearing has a volume control",
     "you do not operate."),

    ("With nothing coming in from outside,",
     "it turns its own sensitivity up."),

    ("And it turns the ringing up with it.",),

    # The trap - the counterintuitive turn, and the reason to stay past the
    # mechanism.
    ("So the instinct is",
     "to make the room quieter still."),

    # The beat. One caption chunk per row, in row order, nothing else in the
    # span - a drawn beat times its reveals off the caption starts of its own
    # sentence, so a spare line here would eat reveal zero.
    ("So earplugs make it stand out more.",
     "A soundproofed room does the same.",
     "So does sitting still and waiting.",
     "Low steady sound in the room",
     "is the only one that helps."),

    ("A fan. Rain. White or brown noise.",),

    ("Do not turn it up",
     "until the ringing disappears."),

    ("Set it just below.",
     "Quiet enough that you can still hear it underneath."),

    ("Stop aiming for silence.",
     "One steady sound, no words.",
     "Just below the ringing."),

    ("Silence is not neutral.",
     "Try it in the next quiet room."),
]

# One float per sentence. **A default-0.34 script is a first draft** - pace is
# the only prosody a synthesiser has. The load-bearing ones here: 0.85 in front
# of "It did not", because the reversal needs the silence to reverse into; 0.85
# after "And it turns the ringing up with it", which is the mechanism landing;
# and 0.85 after the two-word refusal "Do not turn it up", so the setting that
# follows reads as the answer rather than as a continuation.
GAPS = [0.70,
        0.60, 0.85, 0.45, 0.55, 0.85,
        0.34, 0.60, 0.70, 0.85,
        0.70, 0.70, 0.55]

SHOTS = [
    # The opening question rides the same face as the line after it - the
    # question is the hook, not a card.
    # 1 - motion on frame one, and a face. A Short is judged in its first
    # second and this reads as "the ringing is the only thing in the room" in
    # a fifth of one.
    Shot(clip=TIREDW / "4867379.mp4", clip_ax=0.38),  # her face at .42

    # The man is seated at .60 of the source; centred, the crop kept the
    # empty reflected wall and left him at the edge.
    Shot(clip=ALONE / "38136563.mp4", clip_ax=0.65),

    Shot(clip=TIREDW / "7676122.mp4", clip_at=2.0, clip_ax=0.25),

    Shot(clip=NEURON / "29184317.mp4"),              # L23-26 S42-47

    Shot(clip=SOUND / "34645273.mp4"),               # L7 S2

    Shot(clip=NEURON / "29184317.mp4", clip_at=5.0),

    Shot(clip=CURT / "10813036.mp4", clip_ax=0.43),  # the window at .45

    Shot(graphic="checklist",
         payload=([("Earplugs in a quiet room", False),
                   ("Soundproofing the bedroom", False),
                   ("Sitting still, waiting it out", False),
                   ("Low steady sound in the room", True)],
                  "WHAT CHASING QUIET DOES",
                  True)),                            # flow

    Shot(clip=FAN / "3069096.mp4", clip_ax=0.30),    # the hub at .36

    Shot(clip=LISTEN / "7948198.mp4"),               # L42 S7-8

    Shot(clip=RAIN / "4458918.mp4"),                 # L20-21 S16-23

    Shot(graphic="steps",
         payload=(["Stop aiming for silence",
                   "One steady sound, no words",
                   "Just below the ringing"],
                  "IN A QUIET ROOM")),

    # **The worst of them.** He stands at .80 of the source and the
    # centred crop showed a brick wall and a plant with his shoulder
    # clipped at the edge - the closing shot of the video.
    Shot(clip=MEDIT / "6447702.mp4", clip_at=3.0, clip_ax=0.95),
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-silence-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-silence-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)
    # **Same headline as the long form from this post**, so the pair reads as
    # one. It points at the part of the answer the viewer does not have rather
    # than answering the title - "not neutral" cannot be acted on without
    # watching.
    #
    # **`band="bottom"`, not the default `"top"`**, because her face is in the
    # top half of this crop. The renderer's bottom band already sits 20px
    # higher than the type's own margin would put it, to clear the play count
    # YouTube draws across the bottom of a Short's grid tile - do not add more
    # here.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Does silence make tinnitus [worse?]", image=THUMB_PHOTO,
        accent="red",
        ax=0.50, zoom=1.0, band="bottom")

    # **A Short needs a 16:9 thumbnail as well, and YouTube gets that one.**
    # The vertical file is the Reel cover on Instagram and Facebook. Handing
    # it to YouTube instead is what shipped here first, and YouTube letterboxes
    # a 9:16 upload into its 1280x720 slot with a blurred, zoomed copy of the
    # same image either side - so the live thumbnail was a narrow strip of
    # picture with "DOES ... NCE" bleeding across the bottom in huge soft
    # letters, and the user had to replace it by hand. Same headline, same
    # source, same treatment, correct shape.
    yt = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), TINNITUS,
        "Does silence make tinnitus [worse?]", image=THUMB_PHOTO,
        accent="red", side="left", crop_at=(0.86, 0.0), crop_zoom=0.50)

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Reel cover (Instagram, Facebook)")
    print(f"{yt}   <- YouTube thumbnail")


if __name__ == "__main__":
    main()
