"""Can AirPods cause tinnitus? — long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/airpods-and-tinnitus.mdx.

**Why this post.** It is the highest-intent query on the site and the only one
carrying a brand name people actively search - "can AirPods cause tinnitus",
"why do my ears ring after AirPods". It is also safe ground: exposure limits and
device settings, not diagnosis, so almost nothing needs hedging. And it owns a
real table of figures (level against safe weekly time), which is the `bars` beat
this site's posts keep earning.

**The voice is `sam`, from the crypto roster, and the tinnitus male profiles
are not usable for this.** The first cut used `elias` and the user's note was
that `elias`, `felix` and `jonas` are all ASMR voices - which is exactly what
they are by construction: every "male" profile on this channel is `af_nicole`
pitched down through the SOFT chain, the chain that exists for sound therapy.
`caspar` was excluded first for the same reason the roster already records. So
the whole tinnitus male set is the wrong instrument for an explainer, not just
the one profile named in it.

`sam` is `am_puck` through ENERGETIC - a real male voice rather than a
processed one, and the roster's note is "graded C+ with hours of data, the
steadiest American male". `theo` (`am_adam`) is the alternative and reads 9%
faster; it is graded F on the model card and shortlisted by ear, which is a
fine reason to try it but not the one to default to on a health topic where
steadiness is the point.

**This changed the word budget in both directions and the script was rewritten
for it.** Measured on this script's own opening lines: `elias` 1.97 words/sec,
`sam` 3.31, `theo` 3.60. The `elias` cut was deliberately held to 400 words to
land under four minutes; at `sam`'s pace those same 400 words come in at about
2:26, under the format's own floor. So the material trimmed for the slow read
is back - the flight and the train in the opening, the safe-week framing, the
pressure sensation, the hearing aid licensing, sudden hearing loss - and the
script is ~620 words, which is the normal 440-700 range this format was
designed around.

**Beat variety was chosen before the script was written.** Seven sections, seven
shapes, no repeats: `stat`, `compare` (name_columns), `bars`, `quote`, `steps`,
`grid`, `checklist`. `bars` carries the piece - the article's decibel table is a
weekly budget, and a budget is a proportion, which is the one thing narration
cannot say.

**The medical line.** Everything factual is the article's own: 80 dB for 40
hours a week, safe time halving every 3 dB, the temporary threshold shift, the
occlusion and noise-cancellation illusions, the three hearing features, the red
flags. Nothing promises relief. The hearing features are described as what they
are - a hearing loss tool, explicitly *not* a tinnitus treatment, which is the
article's own wording and the line that matters most here. Disclaimer in
`Meta.credits`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/airpods-and-tinnitus.py

**Phonemes**, checked with `espeak-ng -v en-us -q --ipa`: `AirPods` comes back
`ˈɛɹ pˈɑːdz`, which is correct, so it needs no respelling. Avoided as
initialisms: `dB`, `ANC`, `iOS`, `OTC`, `WHO`. The narration says "decibels",
"noise cancelling", "recent AirPods Pro". Figures are spelled out in the spoken
half and left as digits on screen.

**Pictures.** The site library is very bright here - the two AirPods product
shots measure L185 and L231 and are near-white, so neither is usable even in a
picture column against a near-black frame. This cut is therefore carried by
screened stock clips and the drawn beats, with no site photograph at full
frame. Clips screened at 0.5/3/6/9s; the trailing comment on each is the range.
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

TRAIN = STOCK / "videos/man-commuting-train-headphones-night"
BUDS = STOCK / "videos/person-putting-in-earbuds-dark"
PHONE = STOCK / "videos/smartphone-in-hand-dark-night-screen"
SILH = STOCK / "videos/young-man-headphones-listening-dark"
CITY = STOCK / "videos/city-traffic-night-bus-street"
# **No ear close-ups.** `human-ear-close-up-dark` and
# `audiologist-hearing-test-ear` were both in the first cut and both were cut
# on review: at full frame a macro of an ear canal is unpleasant to look at,
# and the clinic one is a backlit red ear against grass at L140-156, so it was
# glaring as well. A video about hearing does not have to show an ear - the
# subject is a person listening, which every clip above already carries.
TIRED = STOCK / "videos/headache-stress-tired-woman-dark"
FADER = STOCK / "videos/hand-adjusting-phone-volume-dark"
CARRIAGE = STOCK / "videos/train-window-night-passing-city-dark"
CONCERT = STOCK / "videos/concert-crowd-night-stage-lights"
CROWD = STOCK / "videos/live-music-gig-audience-dark"
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

# **The thumbnail's source is stock, portrait, and shared with the Short** -
# the pairing rule, so a viewer who sees both recognises the second. Every site
# image scored "busy" under `_layout` and the two that did not are not about
# earbuds, so a batch was fetched and scored instead.
#
# It is portrait because the Short cannot crop a landscape photo of an ear to
# 9:16 without throwing away the subject's long axis. That makes the *landscape*
# crop the hand-placed one: `crop_at=(0.5, 0.7)` bypasses `_layout`, which
# optimises for empty space rather than for the earbud being visible. Swept
# 0.0 / 0.35 / 0.7 and looked at the renders - 0.7 is the one that puts the
# whole earbud in frame with the type on the dark jaw beside it.
THUMB_PHOTO = (STOCK / "photos/man-wireless-earbuds-vertical-portrait-portrait"
               / "6857209.jpg")

VOICE = "sam"                   # am_puck through ENERGETIC - a real male voice,
                                # not a pitched-down female one. Candidate.
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/airpods-and-tinnitus"
A = 16 / 9


SECTIONS = [
    # --- hook: the thing everyone has done and dismissed -----------------
    #
    # **The gaps in this section are the whole fix from the review.** The first
    # cut ran the opening at 0.50-0.60 throughout and the note was that the
    # breaks are missing in exactly the spots that carry the meaning: the
    # reversal after "so you forgot about it", the landing after "do not", and
    # the turn before the promise. Every one of those is a place where the
    # sense changes direction, which is the rule the skill now carries.
    Section(
        title="The ringing you forgot about",
        card=False,
        sentences=[
            ("Your ears rang after listening to music.",),
            ("Maybe after a flight.",),
            ("Maybe after a long train ride",
             "with the volume up."),
            ("It faded within the hour.",
             "So you forgot about it."),
            # The contradiction. It gets the longest gap in the section on the
            # line before it, and a long one of its own, because a two-word
            # imperative either lands in silence or it does not land.
            ("Do not.",),
            ("That is the whole warning,",
             "and almost everybody throws it away."),
            # The title stamp, on the promise rather than the opening frame.
            ("Your AirPods are not giving you tinnitus.",),
            ("The volume is.",
             "And there is a number for it",
             "that almost nobody has been told."),
            ("Stay to the end",
             "and you will know how loud you can play them,",
             "and for exactly how long."),
            ("Plus the ten minutes of settings",
             "that cap it for good."),
        ],
        shots=[
            # A face, moving, on frame one - the standing note for this
            # channel. A man on a train with headphones round his neck reads
            # as the subject in about a fifth of a second.
            Shot(clip=TRAIN / "7251021.mp4"),            # L52-54 S14-16
            Shot(clip=CARRIAGE / "36244106.mp4"),        # L19-22 S12-14
            Shot(clip=CARRIAGE / "36111567.mp4"),        # L18-19 S10-12
            None,
            Shot(clip=SILH / "5686036.mp4"),
            None,
            Shot(clip=BUDS / "5008497.mp4",              # L59-64 S18-22
                 payload=("", "CAN AIRPODS CAUSE TINNITUS?")),
            Shot(clip=PHONE / "28828935.mp4"),           # L17-21 S6-8
            Shot(clip=TRAIN / "7251750.mp4"),            # L65-79 S21-23
            Shot(clip=FADER / "12213087.mp4"),           # L11-17 S6-7
        ],
        #      music  flight  train  forgot  DO NOT  warning  stamp  volume
        gaps=[0.60, 0.55, 0.60, 0.90, 0.95, 0.80, 0.85, 0.60, 0.55, 0.70],
    ),

    # --- the direct answer, and the number under it ----------------------
    Section(
        title="It was never the earbud",
        # A discourse marker and a question mark: the two levers that make a
        # synthesiser open a chapter rather than continue a paragraph.
        spoken_title="So what is actually doing the damage?",
        sentences=[
            ("Well, no headphone is inherently dangerous.",
             "And no headphone is inherently safe."),
            ("What damages hearing",
             "is sound energy over time.",
             "Level, multiplied by duration."),
            ("A safe week is about eighty decibels,",
             "spread across forty hours."),
            ("Here is the part that catches people.",),
            ("Every three decibels louder",
             "halves the time you can listen safely."),
            ("Three decibels is one nudge on a slider.",
             "It costs you half your week."),
            ("That is not a gentle curve.",
             "It collapses."),
        ],
        shots=[
            Shot(clip=SILH / "7948198.mp4"),             # L42 S8
            Shot(clip=BUDS / "5008497.mp4", clip_at=6.0),
            # A spoken figure the viewer should keep, on a shot that is not
            # otherwise carrying one. See the skill's "a number that is spoken
            # must also be seen".
            Shot(clip=CARRIAGE / "36244106.mp4",
                 note=("80 dB", "a loud restaurant, 40 hours a week")),
            None,
            Shot(graphic="stat",
                 payload=("3", "DECIBELS",
                          "Every three decibels halves your safe time.")),
            Shot(clip=FADER / "12213087.mp4", clip_at=4.0,
                 note=("+3 dB", "half the safe time, one nudge")),
            Shot(clip=CARRIAGE / "36111567.mp4", clip_at=4.0),
        ],
        gaps=[0.55, 0.60, 0.70, 0.75, 1.10, 0.70, 0.85],
    ),

    # --- why an earbud, specifically: an A vs B, so `compare` ------------
    Section(
        title="A concert ends. Your commute does not",
        spoken_title="So why is an earbud worse than a concert?",
        sentences=[
            ("Picture a concert.",
             "It is loud,",
             "and then you go home."),
            ("Two hours, once or twice a year.",
             "That is the one everybody worries about."),
            ("Now put the two side by side.",),
            # **Eight chunks, and the fourth one is a hinge.** The first cut
            # opened the right-hand column with the bare heading "Your
            # earbuds." and the review called that stretch quick, unbroken and
            # read rather than spoken - correctly, because a column heading is
            # a label and a person changing subject says so out loud. "Now
            # compare that with your earbuds" is the same single chunk and the
            # same reveal, written the way somebody would actually turn.
            ("Take a concert.",
             "Two hours, and it is over.",
             "You step outside into quiet.",
             "Twice a year, if that.",
             "Now compare that with your earbuds.",
             "Eight hours, most days.",
             "Sealed into the ear canal.",
             "And turned up to beat the traffic."),
            ("So the earbud is not more dangerous than the speaker.",
             "You just never take it out."),
            ("Eight hours at a moderate volume",
             "can carry more total exposure",
             "than twenty minutes at a loud one."),
        ],
        shots=[
            # **The concert line gets a concert.** The first cut ran an empty
            # night street here and the picture illustrated nothing. Screened
            # dark and purple-lit; the two green-lit gig clips in the same
            # batch were rejected on hue.
            Shot(clip=CONCERT / "13082773.mp4",          # L20-32 S9-13
                 note=("110 dB", "a loud gig, under 3 minutes a week")),
            Shot(clip=CROWD / "26744501.mp4"),           # L27-32 S15-22
            None,
            Shot(graphic="compare",
                 payload=("A concert",
                          ["Two hours, then it is over",
                           "You step outside into quiet",
                           "Twice a year, if that"],
                          "Your earbuds",
                          ["Eight hours, most days",
                           "Sealed into the ear canal",
                           "Turned up to beat the traffic"],
                          True)),                        # name_columns
            Shot(clip=TRAIN / "7251750.mp4", clip_at=5.0),
            Shot(clip=CONCERT / "13082773.mp4", clip_at=10.0),
        ],
        gaps=[0.55, 0.70, 0.80, 0.70, 0.70, 0.85],
    ),

    # --- the numbers: a budget, so `bars` --------------------------------
    Section(
        title="What the volume actually costs",
        spoken_title="So what does all that actually buy you?",
        sentences=[
            ("Think of safe listening as a weekly budget.",),
            ("Eighty decibels, forty hours.",
             "Eighty six, ten hours.",
             "Ninety two, under three.",
             "Ninety eight, under one."),
            ("Ninety two is the one that catches people.",),
            ("That is not an unreasonable volume.",
             "It is just music, enjoyable, over a train."),
            ("Two commutes a day",
             "and your week is spent by Wednesday."),
            ("Which is why noise cancellation helps here.",
             "You stop competing with the engine,",
             "so the volume you pick is lower."),
        ],
        shots=[
            Shot(clip=PHONE / "5617952.mp4"),            # L18 S13-15
            Shot(graphic="bars",
                 # Hours per week over forty, scaled by 0.9. The value text
                 # travels with the end of its bar, so a full-width top row
                 # pushes its own label off frame; scaling the whole set by
                 # one factor leaves the proportions exact, which is the only
                 # thing this beat claims.
                 payload=([("80 dB · loud restaurant", 0.90, "40 hours"),
                           ("86 dB · city traffic", 0.225, "10 hours"),
                           ("92 dB · music on a train", 0.0675, "under 3h"),
                           ("98 dB · motorbike, loud gig", 0.0225, "under 1h")],
                          "SAFE LISTENING PER WEEK")),
            Shot(clip=CARRIAGE / "36111567.mp4", clip_at=6.0,
                 note=("92 dB", "music over a train")),
            Shot(clip=CARRIAGE / "36244106.mp4", clip_at=4.0),
            Shot(clip=TRAIN / "7251021.mp4", clip_at=7.0),
            Shot(clip=SILH / "7948198.mp4", clip_at=6.0),
        ],
        gaps=[0.75, 0.60, 0.80, 0.60, 0.80, 0.85],
    ),

    # --- the twist: it feels worse and nothing got worse ------------------
    Section(
        title="Why does it feel worse with them in?",
        spoken_title="But does it make tinnitus you already have worse?",
        sentences=[
            ("Usually not.",),
            ("Though it will absolutely feel that way.",),
            ("A silicone tip seals your ear canal.",),
            ("And noise cancellation strips out the low hum",
             "you were leaning on without knowing it."),
            ("So here is what is really happening.",),
            ("Your tinnitus did not grow.",
             "Everything it was hiding behind went away."),
            ("Some people feel a pressure sensation too.",
             "That is worth switching out of.",
             "It is not damaging anything."),
            ("So use transparency mode indoors.",
             "Save noise cancellation for genuinely loud places,",
             "where it stops you reaching for the volume."),
        ],
        shots=[
            Shot(clip=TIRED / "4588228.mp4"),            # L30-32 S14
            None,
            Shot(clip=BUDS / "5008497.mp4", clip_at=11.0),
            Shot(clip=PHONE / "28828935.mp4", clip_at=8.0),
            None,
            Shot(graphic="quote",
                 payload=("Nothing got louder. The room got quieter.",
                          "why it feels worse")),
            Shot(clip=SILH / "7948198.mp4", clip_at=12.0),
            # "Save noise cancellation for genuinely loud places" - so show
            # one. A gig crowd is the actual referent of the line.
            Shot(clip=CROWD / "26744501.mp4", clip_at=6.0),
        ],
        gaps=[0.85, 0.60, 0.55, 0.70, 0.80, 1.10, 0.70, 0.85],
    ),

    # --- the fix: a procedure, then the set of features -------------------
    Section(
        title="Ten minutes of settings, once",
        spoken_title="So what do you actually change tonight?",
        sentences=[
            ("Five changes. Ten minutes. Once.",),
            ("Cap the volume in headphone safety.",
             "Check your seven day exposure.",
             "Take the hearing test.",
             "Noise cancellation outside, transparency mode inside.",
             "And at night, a speaker, not an earbud."),
            ("That hearing test matters more than it looks.",),
            ("Five minutes, from your own phone.",
             "Amplification tuned to whatever it finds.",
             "And a log of how loud you really listen."),
            ("In some countries",
             "that middle one is licensed",
             "as an actual hearing aid."),
            ("But be clear about what that is.",),
            ("None of it treats tinnitus.",),
            ("What it does is find hearing loss.",
             "And most lasting tinnitus",
             "sits beside some hearing loss,",
             "which most people have never been tested for."),
        ],
        shots=[
            Shot(clip=PHONE / "28828935.mp4", clip_at=6.0),
            Shot(graphic="steps",
                 payload=(["Cap the volume at 80 dB",
                           "Check your 7 day exposure",
                           "Take the hearing test",
                           "Cancellation out, transparency in",
                           "A speaker at night"],
                          "THE TEN MINUTE SETUP")),
            Shot(clip=PHONE / "5617952.mp4", clip_at=6.0),
            Shot(graphic="grid",
                 payload=([("Hearing test",
                            "Five minutes, run from the phone"),
                           ("Hearing aid mode",
                            "Amplified to your own profile"),
                           ("Exposure log",
                            "Seven days of how loud you listen")],
                          "WHAT THEY ACTUALLY OFFER")),
            Shot(clip=SILH / "5686036.mp4", clip_at=2.0),
            None,
            Shot(clip=TIRED / "4588228.mp4", clip_at=3.0),
            Shot(clip=FADER / "12213087.mp4", clip_at=2.0),
        ],
        gaps=[0.75, 0.60, 0.80, 0.60, 0.75, 0.80, 0.95, 0.85],
    ),

    # --- when it is not a settings problem, and the echo ------------------
    Section(
        title="When is it not a settings problem?",
        spoken_title="And when is none of this a settings problem?",
        sentences=[
            ("Because some of this is not about volume at all.",),
            ("New, and only in one ear.",
             "Pulsing in time with your heartbeat.",
             "Arriving with hearing loss or dizziness.",
             "Or following one loud night, and not settling."),
            ("Any of those is an appointment,",
             "not a setting."),
            ("Sudden hearing loss especially.",
             "That one is treated in days, not weeks."),
            ("Because the earbuds were never the villain.",),
            ("The volume was.",
             "And the volume is the one part you own."),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(clip=TIRED / "4588228.mp4", clip_at=8.0),
            Shot(graphic="checklist",
                 # `flow=True`: the narration is already naming each flag as
                 # it lands, so holding the marks back would put the picture
                 # behind the voice.
                 payload=([("New, and in one ear only", True),
                           ("Pulsing with your heartbeat", True),
                           ("With hearing loss or dizziness", True),
                           ("After one loud night, not settling", True)],
                          "SEE SOMEONE IF",
                          True),
                 # **A site photograph, in the picture column, not a clip.**
                 # Every clinic clip screened between L137 and L184 - a
                 # consulting room is a bright white box and there is no dark
                 # one to be had. Downscaled into the 660px column it sits
                 # where a full-frame version would glare.
                 picture=IMG / "audiologist.jpg"),
            Shot(clip=SILH / "7948198.mp4", clip_at=18.0),
            Shot(clip=TRAIN / "7251750.mp4", clip_at=8.0),
            Shot(clip=BUDS / "5008497.mp4", clip_at=3.0),
            None,
            Shot(clip=CONCERT / "13082773.mp4", clip_at=16.0),
        ],
        gaps=[0.80, 2.40, 0.90, 0.85, 0.90, 0.85, 2.60],
    ),
]
META = Meta(
    title="Can AirPods Cause Tinnitus?",
    hook="AirPods do not cause tinnitus - volume does, and every three "
         "decibels halves how long you can safely listen. Here is what your "
         "weekly budget actually looks like, why it feels worse with them in, "
         "and the ten minutes of settings that fix it.",
    url=URL,
    summary="Why an earbud is a bigger hearing risk than a concert, what the "
            "safe listening table really buys you per week, the ringing "
            "after listening that everybody dismisses, why sealing your ear "
            "makes existing tinnitus feel louder without anything getting "
            "worse, and where the AirPods Pro hearing features genuinely "
            "help.",
    tags=["airpods and tinnitus", "can airpods cause tinnitus", "tinnitus",
          "safe listening", "headphone volume", "ringing in ears",
          "hearing loss", "airpods pro hearing test"],
    cta=f"Full guide, the decibel table and sources: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. It is "
             "not affiliated with or endorsed by Apple. If your tinnitus is "
             "new, persistent, in one ear only, pulses with your heartbeat, "
             "or comes with hearing loss or dizziness, see a doctor or "
             "audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-airpods-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-airpods-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # The title carries the search phrase and asks the question, so the
        # thumbnail answers it - which is the pairing that costs the click
        # decision nothing.
        # **The thumbnail must not answer the title.** "Not the earbuds. The
        # volume." was the first pass and it gave the whole video away in five
        # words - a viewer who reads it has no reason to press play. The title
        # asks the search question; the thumbnail points at the part of the
        # answer they do not have, which is that the ringing afterwards was
        # information and they threw it away.
        thumb_headline="The warning [everyone ignores]",
        thumb_image=THUMB_PHOTO,
        thumb_accent="red",
        thumb_side="right",
        thumb_crop_at=(0.5, 0.7),
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
