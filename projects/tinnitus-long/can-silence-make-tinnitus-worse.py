"""Does silence make tinnitus worse — long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/can-silence-make-tinnitus-worse.mdx.

**Why this post, and how it is not the sleep cut.** `tinnitus-and-sleep`
already shipped the "your room got quieter" reframe, and the first sketch of
this script was that video with the bedroom taken out. What makes this a
separate video is the **mechanism**: the sleep cut says the masking went away,
and this one says the brain then *turns its own gain up* to look for the sound
that is missing. That is the article's own first heading and it is a different
claim — one is about the room, the other is about the listener. The bedroom
appears here as one example among several rather than as the subject.

**Beat variety chosen before the script**, per the crypto skill's silhouette
rule. Five beats, five different outlines, each used once:

    quote -> compare -> grid -> checklist -> steps

`compare` carries the mechanism because a silent room against a room with a low
sound in it is literally an A/B, and 16:9 is the right shape for one. It runs
`name_columns=True`, so each heading is its own revealed item and the graphic
follows the voice instead of asking the viewer to work out which side is being
described.

**No `stat` and no `bars`.** This article carries no figures at all — no
decibel table, no prevalence number, nothing against a limit. The gaming cut
earned a `bars` because its post had a real proportion in it; inventing a
scale to fill a beat slot is the one thing that beat must never do, and a
`stat` on a made-up count is the same fault in a smaller frame. Five
silhouettes without either is still five silhouettes.

**The one full-frame site photograph is `neurons.jpg` at L24.** It is the only
image in the library that is both inside the ~L82 ceiling and on the subject of
the section it sits under. Everything else screened bright, exactly as the
sleep and gaming cuts found: `silence.jpg` — the article's own hero — is a
teal studio "shh" shot at **L138 / S87**, `meditation.jpg` L106,
`therapy.jpg` L143, `audiologist.jpg` L179. The last two are used, but only in
a beat's picture column where they are downscaled to 660px and small.

**Stock screened across its length, ids read off a labelled contact sheet.**
Keepers and their range: a woman alone under one bulb in an empty room
(L13-14 S8), a man sitting still in a bare room (L41 S5), a man alone in a
library (L36-37 S11), a dark fan (L4-7 S5-7), the neuron abstract (L23-26).
Rejected on hue or brightness: every clip in `person-covering-ears-noise`
(L99-167, and two of the three are ear close-ups, which are banned here on
sight), the whole `hearing-clinic` and `doctor-consultation` folders (L137-184
of white clinic wall), and `curtains-window-night-moonlight/9902187` at L81 —
a good shot of a man at a window with a static television, and 33 points over
the box.

**The medical line.** Every mechanism is the article's own: increased central
gain in the absence of input, the brain becoming more attuned to the signal
after reduced input, attention turning inward, and the loss of the natural
masking that ordinary rooms provide. Sound is described as making tinnitus
less noticeable and less distinct — never as treating, reducing or curing it.
The article's own myth section is where "masking will eventually cure it" is
refused, and the script refuses it in the same words. Red flags and the route
to a professional come from the post. Disclaimer in `Meta.credits`.

**Phonemes.** Avoided: `ENT`, `TRT`, `CBT`, `anechoic`. The narration says "an
ear specialist", "a structured sound therapy programme" and "a room built to
have no echo in it at all" — which is what each of them means to this
audience, and none of which espeak has to guess at.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/can-silence-make-tinnitus-worse.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

# Screened with `stock.screen` at 0.5/3/6/9s; the trailing comment is the range
# across the whole clip, not one frame.
# **`woman-sitting-alone-dark-room-thinking/6073058` is out of both cuts.**
# It screens beautifully - L13-14 S8, an empty dark room under one bulb - and
# on a contact sheet at 1s that is all it is. Played, the woman in the chair
# is shaving her head, which is a specific and arresting thing to be doing
# under a line about a quiet room, and the user caught it at 0:05. The luma
# box cannot see subject and neither can a single frame: **screen a clip by
# watching a few seconds of it, not by looking at one thumbnail of it.**
ALONE = STOCK / "videos/man-sitting-alone-dark-apartment-night"
SOFA = STOCK / "videos/person-sitting-on-sofa-dark-room-night"
WINDOWS = STOCK / "videos/empty-dark-living-room-night-interior"
MEDIT = STOCK / "videos/man-meditating-dark-room-calm"
LIBRARY = STOCK / "videos/quiet-library-reading-dark"
FAN = STOCK / "videos/electric-fan-spinning-dark-room"
NEURON = STOCK / "videos/brain-neurons-abstract-dark"
CEIL = STOCK / "videos/ceiling-dark-bedroom-night-calm"
CURT = STOCK / "videos/curtains-window-night-moonlight-dark"
TRAFFIC = STOCK / "videos/city-traffic-night-bus-street"
LISTEN = STOCK / "videos/man-listening-music-dark-room-night"
TIREDW = STOCK / "videos/tired-woman-hands-on-face-dark-studio-portrait"
SOUND = STOCK / "videos/sound-wave-visualization-dark"
RAIN = STOCK / "videos/rain-on-window-at-night-dark"
WATER = STOCK / "videos/calm-water-ripple-dark"
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

# **The same source as the Short's thumbnail** — the standing rule is one
# picture for both aspects. Portrait (4000x6000), L22 S20, a woman in a dark
# room with her head lowered and her face lit from one side. Fetched with
# `orientation=portrait` because a landscape source cover-cropped to 9:16
# throws away the subject's long axis.
#
# `crop_at=(0.30, 0.06)` places the landscape crop by hand. A 2:3 source
# cover-cropped to 16:9 is constrained by height, so there is real horizontal
# slack and `_layout` spent it hunting for the quietest patch — which on this
# picture is the empty dark wall with her out of frame entirely. `ax=0.30`
# keeps her whole head in the right of the frame and leaves the wall on the
# left for the type; `ay=0.06` trims the ceiling rather than her chin.
# The full-frame picture in the auditory-gain section, 6000x4000 at L36 S16 -
# glowing filaments on near-black, which is what the line is about and which
# is large enough to bleed off every edge. It replaced the site's own
# `neurons.jpg`; see the shot for why that one could not stay.
GAIN_PHOTO = STOCK / "photos/neuron-synapse-brain-abstract-dark/14506024.jpg"

THUMB_PHOTO = STOCK / ("photos/woman-silence-dark-background-portrait-portrait"
                       "/7041828.jpg")

VOICE = "mia"                   # af_heart. The channel's explainer reader at
                                # its normal pace — `mia-calm` belongs to the
                                # sleep pair, where an unhurried bedtime read
                                # was the point. This video argues a
                                # mechanism, and 9% slower reads as hesitant
                                # rather than calm on an argument. Candidate.

MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/can-silence-make-tinnitus-worse"
A = 16 / 9


SECTIONS = [
    # --- hook: the moment everybody recognises ---------------------------
    Section(
        title="The quiet room",
        card=False,
        sentences=[
            ("You finally get somewhere quiet.",
             "No traffic. No television. Nobody talking."),
            ("And the ringing walks straight to the front of the room.",),
            ("It did not.",
             "Something else changed,",
             "and it was not your ears."),
            ("Stay with this",
             "and you will know why quiet rooms do that,",
             "what to put in one instead,",
             "and the volume setting almost everybody gets wrong."),
        ],
        shots=[
            # A face, moving, on frame one. The note from the first tinnitus
            # cut was that a still of a worried woman is not an engaging way
            # in; a clip of someone visibly dealing with it needs no caption.
            Shot(clip=TIREDW / "4867379.mp4"),           # L25-29 S8-9
            Shot(clip=ALONE / "38136563.mp4"),           # L35 S8
            # The title stamp, on the turn rather than the opening frame.
            Shot(clip=ALONE / "36244102.mp4", clip_at=8.0,   # L33 S10
                 payload=("", "DOES SILENCE MAKE IT WORSE?")),
            Shot(clip=CEIL / "11956219.mp4"),            # L31 S6
        ],
        # 0.85 in front of "It did not." - the reversal is the whole opening
        # and it needs the silence to reverse into. 0.90 on the last line so
        # the first chapter card does not land on top of the promise.
        gaps=[0.45, 0.85, 0.60, 0.90],
    ),

    # --- reframe: it was never heard on its own --------------------------
    Section(
        title="Why does quiet make it louder?",
        spoken_title="So why does quiet make it louder?",
        sentences=[
            ("Tinnitus is never heard on its own.",
             "It is heard against whatever else is in the room."),
            ("And an ordinary room is never actually silent.",
             "A fridge next door. Air in a vent.",
             "Traffic two streets away."),
            ("None of it is loud enough to notice.",
             "All of it is covering part of the sound."),
        ],
        shots=[
            Shot(graphic="quote",
                 payload=("Silence is not nothing. It is the removal of "
                          "everything that was covering it.",
                          "what actually changes in a quiet room")),
            # **Not the traffic clip here.** It is only 6.0s and this slot
            # runs 6.9s; it moved to the shorter sentence below, where it
            # also sits under the line it actually illustrates.
            Shot(clip=SOUND / "34645273.mp4", clip_at=12.0),  # L7 S2
            Shot(clip=TRAFFIC / "16657010.mp4"),         # L32 S5
        ],
        gaps=[0.55, 0.34, 0.90],
    ),

    # --- the mechanism the sleep cut does not have -----------------------
    Section(
        title="Your brain turns itself up",
        spoken_title="But something else is happening, and it is the part "
                     "people never hear about.",
        sentences=[
            ("Your hearing has a volume control of its own,",
             "and you do not operate it."),
            ("With less coming in from outside,",
             "it turns its own sensitivity up",
             "to go looking for faint sound."),
            ("Researchers call that auditory gain.",),
            ("But it does not only amplify the room.",
             "It amplifies the background activity",
             "the ringing is made of."),
        ],
        shots=[
            Shot(clip=NEURON / "29184317.mp4"),          # L23-26 S42-47
            Shot(clip=SOUND / "34645273.mp4"),           # L7 S2
            # **Not `neurons.jpg`.** At 900x599 it cannot reach 1920 under
            # `max_upscale=1.90`, so it rendered *fitted* - a letterboxed
            # panel with a hairline and black bands above and below it - and
            # the user's note was to drop that treatment entirely and show
            # the picture full screen the way the portrait at 3:27 is. A
            # photograph in this format either bleeds off every edge or it
            # does not belong in a full-frame shot; the site library is too
            # small to bleed, which is what the beats' picture column is for.
            Shot(image=GAIN_PHOTO, zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.45),                   # L36 S16
            Shot(clip=MEDIT / "34535504.mp4"),           # L27-29 S18-19
        ],
        gaps=[0.60, 0.55, 0.70, 0.90],
    ),

    # --- the three things stacking ---------------------------------------
    Section(
        title="Three things at once",
        spoken_title="And there are three of these stacking up together.",
        sentences=[
            # One caption chunk per grid card, in card order, nothing else in
            # the span.
            ("First, the gain we just talked about.",
             "Second, the covering sound is gone,",
             "so there is nothing left to blend into."
             " And third, with nothing else asking for your attention,"
             " your attention goes inward."),
        ],
        shots=[
            Shot(graphic="grid",
                 payload=([("Auditory gain",
                            "Less input, so the system turns itself up"),
                           ("No natural masking",
                            "Ordinary room sound was blending with it"),
                           ("Attention turns inward",
                            "Nothing else is asking for it")],
                          "WHY A QUIET ROOM IS DIFFERENT")),
        ],
        gaps=[0.90],
    ),

    # --- the twist: the instinct is backwards ----------------------------
    Section(
        title="So why does chasing quiet backfire?",
        sentences=[
            ("Which makes the obvious move the wrong one.",
             "If it is worse when it is quiet,",
             "the instinct is to make it quieter still."),
            ("There is a laboratory version of that.",
             "A room built to have no echo in it at all,",
             "where people with completely normal hearing",
             "start hearing their own body within minutes."),
            # `flow=True`: the narration is delivering each verdict itself, so
            # holding the marks back would put the picture behind the voice.
            # One chunk per row, in row order.
            ("So earplugs make it stand out more.",
             "A soundproofed room does the same.",
             "So does sitting still and waiting.",
             "Low, steady sound in the room",
             "is the only one that goes the other way."),
            ("Silence is not the goal.",
             "It is the condition the sound is loudest in."),
        ],
        shots=[
            Shot(clip=SOFA / "7856538.mp4"),             # L38-40 S7-8
            Shot(clip=MEDIT / "6447702.mp4"),            # L41 S5-6
            Shot(graphic="checklist",
                 payload=([("Earplugs in a quiet room", False),
                           ("Soundproofing the bedroom", False),
                           ("Sitting still, waiting it out", False),
                           ("Low steady sound in the room", True)],
                          "WHAT CHASING QUIET ACTUALLY DOES",
                          True),                     # flow
                 picture=IMG / "meditation.jpg"),
            Shot(clip=LIBRARY / "6549982.mp4", clip_at=12.0),
        ],
        gaps=[0.60, 0.85, 0.34, 0.90],
    ),

    # --- what goes in the room -------------------------------------------
    Section(
        title="So what goes in the room instead?",
        sentences=[
            ("Something steady that your attention slides off.",
             "A fan. An air purifier. Rain.",
             "White noise, or brown noise if hiss irritates you."),
            ("And here is the comparison that matters.",),
            # `name_columns=True` - each heading is its own revealed item, so
            # the order on screen is the order in the mouth. Eight chunks:
            # heading, three items, heading, three items. Both headings are
            # written as hinge sentences rather than as bare labels.
            ("Take a completely silent room.",
             "The ringing has nothing to blend into.",
             "Your hearing turns its own gain up.",
             "Your attention has nowhere else to go.",
             "Now compare that with a room with a low sound in it.",
             "The edges of the ringing blur.",
             "There is something else to listen to.",
             "And your attention has somewhere to sit."),
            ("Notice what is not in that second column.",
             "The tinnitus is still there.",
             "Sound in a room does not treat it.",
             "It changes how much of the room it takes up."),
        ],
        shots=[
            Shot(clip=FAN / "3069096.mp4"),              # L4-7 S5-7
            Shot(clip=RAIN / "4458918.mp4"),             # L20-21 S16-23
            Shot(graphic="compare",
                 # **"A room with quiet sound in it" ran off the frame.**
                 # A `compare` heading is set at display weight in half the
                 # frame's width, and at 27 characters the right-hand one
                 # clipped mid-word at the edge - visible at 2:22 in the
                 # first render. Roughly 18 characters is the ceiling for a
                 # heading here. The spoken hinge is unchanged and still says
                 # the whole thing ("a room with a low sound in it"); only
                 # the label on screen is shortened.
                 payload=("A silent room",
                          ["Nothing for it to blend into",
                           "Hearing turns its own gain up",
                           "Attention has nowhere else to go"],
                          "A room with sound",
                          ["The edges of it blur",
                           "Something else to listen to",
                           "Attention has somewhere to sit"],
                          True)),                        # name_columns
            Shot(clip=WATER / "11028763.mp4",            # L28-31 S6-7
                 payload=("", "It changes the room, not the ringing.")),
        ],
        gaps=[0.55, 0.70, 0.34, 0.90],
    ),

    # --- the volume rule --------------------------------------------------
    Section(
        title="How loud should it be?",
        spoken_title="So how loud should it actually be?",
        sentences=[
            ("The instinct is to turn it up",
             "until the ringing disappears completely."),
            ("Do not make that mistake.",),
            ("Set it just below your tinnitus.",
             "Quiet enough that you can still",
             "faintly hear the ringing underneath it."),
            ("Just underneath",
             "is where the contrast is smallest,",
             "and contrast was the whole problem."),
        ],
        shots=[
            Shot(clip=SOUND / "34645273.mp4", clip_at=6.0),
            None,
            Shot(clip=RAIN / "15161525.mp4",             # L31 S13
                 payload=("", "Just below. Not on top.")),
            Shot(clip=LISTEN / "7948198.mp4", clip_at=14.0),
        ],
        # 0.90 after the two-word imperative - "Do not." lands or it does not,
        # and a 0.34 runs the next sentence straight over the top of it.
        gaps=[0.55, 0.90, 0.70, 0.90],
    ),

    # --- the procedure ----------------------------------------------------
    Section(
        title="Four things, today",
        spoken_title="So what does that actually look like today?",
        sentences=[
            ("Four things, and they take a minute to set up.",),
            ("Stop treating quiet as the target.",
             "Put one steady, wordless sound in the room.",
             "Set it just below the ringing, not over it.",
             "And leave it running before you notice the ringing,"
             " not after."),
        ],
        shots=[
            Shot(clip=CEIL / "11956328.mp4"),            # L28 S4-5
            Shot(graphic="steps",
                 payload=(["Stop aiming for silence",
                           "One steady, wordless sound",
                           "Just below the ringing",
                           "Running before you notice it"],
                          "TODAY")),
        ],
        gaps=[0.60, 0.90],
    ),

    # --- when it is more than the quiet -----------------------------------
    Section(
        title="When is it more than the quiet?",
        sentences=[
            ("Sound in the room changes the contrast.",
             "It does not tell you where the ringing came from."),
            ("If it is new, or getting louder,",
             "or only in one ear,",
             "or pulsing along with your heartbeat,",
             "or arrives with dizziness or a drop in hearing -"),
            ("that is a reason to see",
             "an audiologist or an ear specialist.",
             "Not to panic. To get the cause named."),
        ],
        shots=[
            Shot(graphic="quote",
                 payload=("Sound changes the room. "
                          "It does not explain the sound.",
                          "two different questions"),
                 picture=IMG / "therapy.jpg"),
            Shot(clip=TIREDW / "7676122.mp4"),           # L17-18 S2-3
            Shot(image=THUMB_PHOTO, zoom=1.08, pan=(-0.02, 0.01),
                 aspect=A, bias=0.50),
        ],
        gaps=[0.60, 0.34, 0.90],
    ),

    # --- close: the echo --------------------------------------------------
    Section(
        title="Silence is not neutral",
        spoken_title="So where does that leave the quiet room?",
        sentences=[
            ("You were never in a fight with a loud sound.",
             "You were sitting in the one condition",
             "that makes a quiet one impossible to ignore."),
            ("So stop chasing the quiet.",
             "Give the room one small thing to say,",
             "and keep it underneath."),
            ("Silence is not neutral.",
             "It is the loudest room you own."),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(clip=WINDOWS / "7292659.mp4"),          # L13-14 S10
            Shot(clip=CEIL / "11956219.mp4", clip_at=14.0),
            Shot(clip=CEIL / "11956328.mp4", clip_at=6.0),
            Shot(clip=LIBRARY / "6549982.mp4", clip_at=4.0),
        ],
        # The endcard sting runs its own 7s over the outro, so the tail does
        # not also need three seconds of silence after the last line.
        gaps=[0.55, 0.34, 0.90, 2.00],
    ),
]



META = Meta(
    title="Does Silence Make Tinnitus Worse?",
    hook="In a completely quiet room your tinnitus is not louder - your "
         "hearing is turning its own gain up to look for the sound that is "
         "missing. Here is what to put in the room, and the volume setting "
         "almost everybody gets wrong.",
    url=URL,
    summary="Why tinnitus stands out the moment a room goes quiet, the three "
            "things happening at once - auditory gain, the loss of natural "
            "masking, and attention turning inward - why earplugs and "
            "soundproofing make it stand out more rather than less, what "
            "kind of steady sound to put in the room instead, and the "
            "counterintuitive volume rule: set it just below the ringing "
            "rather than loud enough to bury it.",
    tags=["tinnitus", "does silence make tinnitus worse", "silence and tinnitus",
          "tinnitus in quiet rooms", "sound therapy", "sound enrichment",
          "white noise", "brown noise", "tinnitus masking", "auditory gain",
          "ringing in ears", "tinnitus help", "tinnitus management"],
    cta=f"Full guide, the strategies and sources: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: night-drift.",
             "",
             "This video is general information, not medical advice. If your "
             "tinnitus is new, persistent, in one ear only, pulses with your "
             "heartbeat, or comes with hearing loss or dizziness, see a "
             "doctor or audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-silence-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-silence-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # Same headline and same treatment as the Short from this post - they
        # are published as a pair and should look like one. It does not
        # answer the title's question: "not neutral" is a claim the viewer
        # cannot act on without the video, which is the whole job of the line.
        # **The headline is the video's own title now.** "Silence is not
        # neutral" was written to the old rule that a thumbnail must not
        # answer its own title, and the user's call is that it reads as
        # boring - the question is what makes somebody curious enough to
        # click. Asking the title is not the fault that rule was about;
        # answering it is.
        #
        # **And it is the panel layout, not a cover crop.** Her head spans
        # 1036px of the scaled source against a 720px window, so every `ay`
        # cut her hair or her chin - which is what "zoomed in too much" was.
        # `crop_zoom=0.50` drops the cover requirement, `ax=0.86` sets the
        # panel against the right edge, and the type gets real black.
        thumb_headline="Does silence make tinnitus [worse?]",
        thumb_image=THUMB_PHOTO,
        thumb_accent="red",
        thumb_side="left",
        thumb_crop_at=(0.86, 0.0),
        thumb_crop_zoom=0.50,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
