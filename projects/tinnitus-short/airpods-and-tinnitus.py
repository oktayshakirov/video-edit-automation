"""It is not the AirPods, it is the volume. ~45s tinnitus short.

Source: tinnitus-blog/content/posts/airpods-and-tinnitus.mdx, the same post as
the `tinnitus-airpods-long` explainer.

**It does not reuse the long form's shape.** That video walks the whole guide:
the exposure arithmetic, why an earbud beats a concert for total dose, the
occlusion illusion, the hearing features, the red flags. None of that
compresses. What survives at forty-five seconds is the one number nobody knows
- **every three decibels halves your safe listening time, and ninety two
decibels is music over a train** - plus the reframe that the ringing afterwards
was the warning. A viewer who sees both gets the guide and the number, not the
same script twice.

**Two drawn beats, two silhouettes.** `checklist` for the argument and `bars`
for the budget. The gaming short paired `bars` with `steps`, so this one
deliberately takes the other portrait beat: the piece's whole claim is a set of
verdicts - not the earbuds, not the cancelling, the volume - which is precisely
what a checklist is for and what a list of steps is not. `flow=True`, because
the narration says each verdict as it lands.

**The tick is the payoff and it was checked on the frame.** This skill's own
warning: the brand accent `#ffdab9` carries less contrast against white item
text than crypto's gold, so the final tick can read weaker than the two crosses
before it. Looked at, not assumed.

**Voice is `sam`**, matching the long form from this post - a short and a long
on one channel in two voices is two channels. The first cut used `elias` and
the user's note was that `elias`, `felix` and `jonas` are all ASMR voices,
which is what they are by construction: every "male" profile on this channel is
`af_nicole` pitched down through the SOFT chain. `sam` is `am_puck` from the
crypto roster - a real male voice, not a processed one.

That reset the word budget: `elias` reads 1.97 words/sec, `sam` 3.31, so the
88-word `elias` script came in at 27s here. This one is ~135 words.

**No medical claims, and short form is where that is hardest** because there is
no room to qualify anything. Every figure is the article's own. The close is an
action from the article - a volume ceiling - never a promise about the result.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/airpods-and-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Screened across their length by the long-form build from this post; the
# trailing comment on each is the luma/saturation range.
TRAIN = STOCK / "videos/man-commuting-train-headphones-night"
BUDS = STOCK / "videos/person-putting-in-earbuds-dark"
PHONE = STOCK / "videos/smartphone-in-hand-dark-night-screen"
SILH = STOCK / "videos/young-man-headphones-listening-dark"
FADER = STOCK / "videos/hand-adjusting-phone-volume-dark"
CARRIAGE = STOCK / "videos/train-window-night-passing-city-dark"

# One source for both aspects - the long form crops this same portrait photo to
# 16:9 by hand with `crop_at=(0.5, 0.7)`.
THUMB_PHOTO = (STOCK / "photos/man-wireless-earbuds-vertical-portrait-portrait"
               / "6857209.jpg")

VOICE = "mia"                   # was `sam`, matching the long form from this
                                # post - retired from the roster on 2026-08-28.
                                # Points at the channel's default so a re-cut
                                # still runs; it would not reproduce the
                                # shipped audio.

# **Shorts get a music bed now**, the same track as the long form from this
# post. It was a standing gap rather than a decision - both short skills
# recorded it as "requested and not yet built" - and `render_crypto_short`
# takes `music`/`music_gain` from here on, exactly as `render_long` always did.
#
# Slightly under the long form's gain: a short is watched on a phone speaker
# with the voice carrying all the information, and the bed is there to stop
# forty seconds of synthesised speech sounding like a voice memo.
#
# **The uploaded cut of this Short predates the bed** - it was rendered before
# this was wired, and it is not worth a re-upload for. Re-running this file
# produces the version with music.
MUSIC = music.track("night-drift")
MUSIC_GAIN = 0.85

SENTENCES = [
    # "after listening" alone did not say listening to *what* - the review
    # note. Two syllables fixes it.
    ("Your ears rang after listening to music.",),

    # Its own sentence, so the gap after it is a real one. As a comma clause
    # inside the line above, the voice ran the two together.
    ("Maybe after a flight.",),

    ("Maybe after a long train ride.",),

    ("It faded within the hour,",
     "so you forgot about it."),

    ("That is the one warning you get.",),

    ("And it is not the earbuds.",
     "So what is?"),

    # **Written as speech, not as a list read aloud.** The first cut set these
    # three chunks as "Not the earbuds. / Not the noise cancelling. / The
    # volume." and the note was that it does not flow. Same three chunks, same
    # three reveals, same sync with the beat - the only change is that a person
    # would actually say it this way, and the pause before the payoff is
    # written into the gap rather than left to chance.
    ("It is not the earbuds.",
     "It is not the noise cancellation.",
     "It is the volume."),

    ("And every three decibels louder",
     "halves how long you can safely listen."),

    ("Three decibels is one nudge on a slider.",),

    ("So here is what that buys you.",),

    ("Eighty decibels, forty hours a week.",
     "Ninety two, under three.",
     "Ninety eight, under one."),

    ("And ninety two is just music over a train.",),

    ("Two commutes a day",
     "and your week is gone by Wednesday."),

    # **One closing instruction, said once.** The first ending stacked four
    # short sentences into eight seconds - the instruction, the reassurance and
    # the call to action all landing on top of each other, which the review
    # called messy. This is the instruction, with a real pause in front of it,
    # and nothing after it competing.
    ("So tonight, open headphone safety",
     "and cap it at eighty."),
]

SHOTS = [
    # Motion on frame one, and a face. A Short is judged in its first second.
    #
    # **No ear close-up as shot two.** The first cut put `human-ear-close-up-
    # dark` here and it was rejected on sight - a macro of an ear canal is
    # unpleasant and tells the viewer nothing they did not know. A video about
    # hearing shows a person listening.
    Shot(clip=TRAIN / "7251021.mp4"),                # L52-54 S14-16

    Shot(clip=CARRIAGE / "36244106.mp4"),            # L19-22 S12-14

    Shot(clip=CARRIAGE / "36111567.mp4"),            # L18-19 S10-12

    Shot(clip=SILH / "5686036.mp4"),

    Shot(clip=TRAIN / "7251750.mp4"),                # L65-79 S21-23

    Shot(clip=BUDS / "5008497.mp4"),                 # L59-64 S18-22

    # The argument, as verdicts. `flow=True` - the narration is already saying
    # "it is not the earbuds" as each row lands, so holding the marks back
    # would put the picture behind the voice.
    Shot(graphic="checklist",
         payload=([("The earbuds", False),
                   ("Noise cancellation", False),
                   ("The volume", True)],
                  "WHAT ACTUALLY COSTS YOU",
                  True)),

    Shot(clip=FADER / "12213087.mp4"),               # L11-17 S6-7

    Shot(clip=FADER / "12213087.mp4", clip_at=5.0,
         note=("+3 dB", "half the safe time")),

    Shot(clip=PHONE / "5617952.mp4"),                # L18 S13-15

    # The budget. Fractions are hours-per-week over forty, times 0.60. The
    # value text travels with the end of its own bar, so a long top bar pushes
    # "40 hours" off the right edge - and the factor that clears it is
    # frame-dependent, not a property of the data: 0.90 fits at 1920 and has to
    # come down to 0.60 at 1080. One factor across the set leaves the
    # proportions between rows exact, which is all this beat claims.
    Shot(graphic="bars",
         payload=([("80 dB · restaurant", 0.60, "40 hours"),
                   ("92 dB · train music", 0.045, "under 3h"),
                   ("98 dB · loud gig", 0.015, "under 1h")],
                  "SAFE TIME PER WEEK")),

    Shot(clip=CARRIAGE / "36111567.mp4", clip_at=4.0,
         note=("92 dB", "music over a train")),

    Shot(clip=PHONE / "28828935.mp4"),               # L17-21 S6-8

    # **A person, not a phone screen, and it echoes the opening shot.** Two
    # phone clips were tried here first and both fight the line: a folder named
    # `hand-adjusting-phone-volume-dark` is the search query, not the contents,
    # so 17643375 is a photo editor with its sliders open and 5617952 is a
    # messaging keyboard. Under "cap it at eighty" a viewer reads the UI and it
    # is the wrong screen, every time. The commuter from frame one closes the
    # loop instead - he is who the instruction is addressed to.
    Shot(clip=TRAIN / "7251750.mp4", clip_at=4.0),
]

# Silence is punctuation. 0.34 inside a thought, longer at the end of one, and
# a real pause in front of the two beats so the verdicts and the bars have
# somewhere to land.
# Silence is punctuation - see the long skill's narration section. The pause
# before "It is the volume" is inside the beat's own sentence, so it is the
# 0.80 on the line before it that buys the payoff its landing.
GAPS = [0.60, 0.55, 0.80, 0.75, 0.90, 0.70,
        0.55, 0.70, 0.80, 0.60, 0.60, 0.75, 0.80, 0.45]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-airpods-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-airpods-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=MUSIC_GAIN)

    # Same source and same headline as the long form from this post - the
    # pairing rule. `band="bottom"`: the ear and the earbud sit in the upper
    # half of the 9:16 crop, which is exactly where the default top band would
    # print the type.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        # **It must not answer the title.** "Not the earbuds. The volume."
        # shipped first and gives the whole video away in five words - there is
        # no reason to press play on a thumbnail that has already told you.
        "The warning [everyone ignores]", image=THUMB_PHOTO, accent="red",
        ax=0.5, zoom=1.0, band="bottom")
    print(f"{path}  {total:.1f}s")
    print(f"{thumb}")


if __name__ == "__main__":
    main()
