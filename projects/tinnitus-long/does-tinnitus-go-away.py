"""Does tinnitus go away? — long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/does-tinnitus-go-away.mdx.

**The first tinnitus long-form video, and the first article video on a health
topic.** Everything structural is the crypto format — the arc, the beats, the
push transitions, no burned captions — and the differences are all about the
subject:

* **Nothing here is a claim about outcomes.** The post's own position is that
  temporary tinnitus often resolves, chronic tinnitus linked to hearing loss is
  *unlikely to disappear on its own*, and that there is no definitive cure that
  eliminates it for everyone. The script says exactly that and no more. It never
  promises relief, never implies a cure, and routes to a professional.
* **The red-flag list is quoted from the article, not invented.** One ear,
  pulsing with the heartbeat, getting louder, dizziness or hearing loss, lasting
  more than a few weeks. These are the reasons to see somebody and they are the
  most useful thirty seconds in the video, so they get the checklist.
* **`mia`, not `luna-calm`.** The user's call: the same reader as the crypto
  long-form. `luna-calm` is the sound-therapy voice — SOFT chain, unhurried, for
  a piece the listener is meant to breathe along with. An explainer wants the
  reader who explains.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/does-tinnitus-go-away.py

**Phonemes.** `tinnitus` is safe (`tˈɪnɪɾəs`). Avoided entirely: `ENT`, `CBT`,
`TMJ`, `presbycusis`, `Meniere's` — every one is either an initialism espeak
mangles or a word it guesses at. The script says "an ear specialist", "talking
therapy", "jaw problems", "certain inner-ear conditions" instead, which is what
those mean to this audience anyway.

**Pictures.** The library tops out at 1000px and only 27 images reach 900px, so
this leans on the picture column and on screened stock — a 900px source in the
660px column is a downscale, the same source full-frame at 1920 is not.
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

# Screened with `stock.screen`; trailing comment is luma/saturation.
HEAD = STOCK / "videos/headache-stress-tired-woman-dark"
WAVE = STOCK / "videos/sound-wave-visualization-dark"
SLEEP = STOCK / "videos/sleeping-night-calm-dark"
NEURONS = STOCK / "videos/brain-neurons-abstract-dark"
WATER = STOCK / "videos/calm-water-ripple-dark"
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # the crypto long-form reader, per the user.
MUSIC = "bright"                # warmer and less tense than `pulse`. This
                                # audience is frequently here *because* sound is
                                # a problem; the bed should not be one.

URL = "https://tinnitushelp.me/blog/does-tinnitus-go-away"
A = 16 / 9


SECTIONS = [
    # --- hook -----------------------------------------------------------
    Section(
        title="The wait",
        card=False,
        sentences=[
            ("Your ears have been ringing for days.",),
            ("And you are waiting for it to stop.",),
            ("Whether it will",
             "comes down to a single distinction,",
             "and almost nobody makes it."),
            ("By the end of this",
             "you will know which kind you are dealing with —",
             "and the five signs",
             "that mean you should see somebody."),
        ],
        shots=[
            # A face, moving, in the first frame. A still of the same idea
            # was there first and the user's note was that it is not an
            # engaging way in — a person visibly dealing with it reads
            # instantly and needs no caption.
            # `clip_at=1.6` — the first second of this clip is an ambiguous
            # half-smile and only reads as discomfort from about two seconds.
            Shot(clip=HEAD / "4587914.mp4", clip_at=1.6),   # L46 S22
            None,
            Shot(clip=WAVE / "34645273.mp4",         # L7 S2
                 payload=("", "DOES IT GO AWAY?")),
            Shot(image=IMG / "silence.jpg", zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.5),
        ],
    ),

    # --- reframe --------------------------------------------------------
    Section(
        title="Tinnitus is not a disease",
        spoken_title="First, tinnitus is not a disease.",
        sentences=[
            ("It is a symptom.",),
            ("A sound your hearing reports",
             "when nothing outside is making it."),
            ("Ringing, buzzing, hissing,",
             "sometimes a low roar."),
            ("The sound you hear is real.",
             "The source of it is not."),
            ("And that matters,",
             "because a symptom goes away",
             "when the thing underneath it does."),
        ],
        shots=[
            Shot(graphic="quote",
                 payload=("The sound is real. The source is not.",
                          "what tinnitus actually is"),
                 picture=IMG / "neurons.jpg"),
            None,
            Shot(clip=NEURONS / "29184317.mp4"),     # L26 S46
            Shot(image=IMG / "brain-research.jpg", zoom=1.11, pan=(0.02, 0.01),
                 aspect=A, bias=0.5),
            None,
        ],
    ),

    # --- the distinction ------------------------------------------------
    Section(
        title="There are two kinds",
        spoken_title="So there are two kinds, and they behave differently.",
        # **Exactly one caption chunk per column item, and no spare sentence in
        # front.** `compare` reveals its left column then its right, and the
        # reveals come from the caption starts of every sentence the shot spans.
        # A standalone lead-in sentence here ("They behave completely
        # differently") consumed reveal 0, which pushed the first *right* column
        # item onto the last *left* column line — the graphic a beat ahead of
        # the voice. Folded into the spoken title instead.
        sentences=[
            ("Temporary tinnitus follows a loud noise.",
             "It fades within hours or days.",
             "And nothing lasting is driving it."),
            ("Chronic tinnitus runs three to six months or longer.",
             "Usually there is hearing loss behind it.",
             "And it is managed rather than waited out."),
        ],
        shots=[
            Shot(graphic="compare",
                 payload=("Temporary",
                          ["Follows loud noise",
                           "Fades in hours or days",
                           "Nothing lasting behind it"],
                          "Chronic",
                          ["Three to six months or more",
                           "Usually hearing loss",
                           "Managed, not waited out"]),
                 backdrop=IMG / "megaphone-noise.jpg"),
            None,
        ],
    ),

    # --- the answer -----------------------------------------------------
    Section(
        title="So does it go away?",
        sentences=[
            ("If it is temporary, often yes.",),
            ("The ears recover and the sound fades.",
             "Earwax or an ear infection",
             "can do the same thing,",
             "and clear once they are treated."),
            ("Chronic is a different answer.",),
            ("If it is tied to hearing loss,",
             "or to the way the brain has adapted",
             "to hearing less,",
             "it is unlikely to disappear on its own."),
            ("That is not a verdict on you.",
             "It is a description of the cause."),
        ],
        shots=[
            Shot(clip=WATER / "11028763.mp4"),       # L27 S7
            Shot(image=IMG / "earwax-and-tinnitus.jpg", zoom=1.10,
                 pan=(0.02, -0.01), aspect=A, bias=0.5),
            Shot(graphic="stat",
                 payload=("3-6", "MONTHS OR MORE", "Where chronic begins."),
                 backdrop=IMG / "research.jpg"),
            Shot(image=IMG / "headphones.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
            None,
        ],
    ),

    # --- causes ---------------------------------------------------------
    Section(
        title="What is usually behind it",
        spoken_title="What is usually behind it?",
        sentences=[
            ("Most of it traces to a short list.",),
            ("Loud noise.",
             "Hearing loss.",
             "Earwax or an infection.",
             "Some medications.",
             "Or another health condition entirely."),
            ("The first three are often fixable.",
             "The others are usually managed",
             "rather than removed."),
        ],
        shots=[
            Shot(image=IMG / "audiologist.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="checklist",
                 payload=([("Loud noise", True),
                           ("Hearing loss", True),
                           ("Earwax or infection", True),
                           ("Some medications", True),
                           ("Another condition", True)],
                          "COMMON CAUSES",
                          True),                     # flow
                 picture=IMG / "research.jpg"),
            Shot(image=IMG / "therapy.jpg", zoom=1.11, pan=(-0.02, -0.01),
                 aspect=A, bias=0.5),
        ],
    ),

    # --- the red flags: the most useful part ----------------------------
    Section(
        title="When should you see someone?",
        sentences=[
            ("These are the five worth acting on.",),
            ("It has lasted more than a few weeks.",
             "It is getting louder.",
             "It is only in one ear.",
             "It pulses along with your heartbeat.",
             "Or it comes with dizziness or hearing loss."),
            ("Any one of those",
             "is a reason to see an ear specialist.",
             "Not to panic —",
             "to get the cause identified."),
        ],
        shots=[
            Shot(clip=SLEEP / "11956328.mp4"),       # L28 S4
            Shot(graphic="checklist",
                 payload=([("Lasted more than a few weeks", True),
                           ("Getting louder", True),
                           ("Only in one ear", True),
                           ("Pulses with your heartbeat", True),
                           ("With dizziness or hearing loss", True)],
                          "SEE A PROFESSIONAL IF",
                          True),                     # flow
                 picture=IMG / "doctor.jpg"),
            Shot(image=IMG / "cardiologist.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
        ],
    ),

    # --- the reframe that actually helps --------------------------------
    Section(
        title="For chronic tinnitus, the goal changes",
        spoken_title="And for chronic tinnitus, the goal changes.",
        sentences=[
            ("There is no treatment",
             "that reliably removes chronic tinnitus",
             "for everyone."),
            ("So the aim stops being silence.",),
            ("It becomes reducing how much room",
             "the sound takes up in your day."),
            ("Sound therapy makes it less noticeable.",
             "Talking therapy changes how much it bothers you.",
             "Hearing aids help when hearing loss is part of it."),
            ("None of that is a cure,",
             "and none of it is nothing.",
             "For most people it is the difference that matters."),
        ],
        shots=[
            Shot(graphic="quote",
                 payload=("The aim stops being silence.",
                          "how chronic tinnitus is actually managed"),
                 picture=IMG / "meditation.jpg"),
            None,
            Shot(clip=WATER / "36117653.mp4"),       # L28 S4
            Shot(graphic="checklist",
                 payload=([("Sound therapy", True),
                           ("Talking therapy", True),
                           ("Hearing aids", True)],
                          "WHAT ACTUALLY HELPS",
                          True),                     # flow
                 picture=IMG / "relaxing-woman.jpg"),
            Shot(image=IMG / "morning-routine.jpg", zoom=1.10, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
        ],
    ),

    # --- close ----------------------------------------------------------
    Section(
        title="So stop waiting, start naming it",
        spoken_title="So where does that leave you?",
        sentences=[
            ("If it started after one loud night",
             "and it is fading, you are probably fine."),
            ("If it has been weeks,",
             "or it is in one ear,",
             "or it pulses —",
             "book the appointment."),
            ("Because the useful question",
             "was never whether it goes away.",
             "It was which kind you have."),
            ("If that helped,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(image=IMG / "evening-routine.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="checklist",
                 payload=([("Weeks, not days", True),
                           ("Only one ear", True),
                           ("Pulsing with your heartbeat", True)],
                          "BOOK THE APPOINTMENT IF",
                          True),                     # flow
                 picture=IMG / "audiologist.jpg"),
            Shot(image=IMG / "happy.jpg", zoom=1.11, pan=(-0.02, -0.01),
                 aspect=A, bias=0.4),
            Shot(clip=SLEEP / "11956219.mp4"),       # L31 S6
        ],
        gaps=[0.34, 0.34, 0.90, 3.20],
    ),
]

META = Meta(
    title="Does Tinnitus Go Away? The Honest Answer",
    hook="Whether tinnitus goes away depends on one distinction almost nobody "
         "makes — and there are five signs that mean you should see somebody.",
    url=URL,
    summary="The difference between temporary and chronic tinnitus, what "
            "usually causes it, the five red flags worth acting on, and what "
            "management actually looks like when it does not go away.",
    tags=["tinnitus", "does tinnitus go away", "ringing in ears",
          "chronic tinnitus", "tinnitus causes"],
    cta=f"Full article, sources and the management guide: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: generated for this channel.",
             "",
             "This video is general information, not medical advice. If your "
             "tinnitus is persistent, one-sided, pulsing, worsening, or comes "
             "with dizziness or hearing loss, see a doctor or audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-does-it-go-away-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # The user's pick over "Which kind do you have?". The type auto-sizes
        # down until "GO AWAY?" fits on one line — see thumb.py; an accent that
        # wraps draws two plates and loses the focal point.
        thumb_headline="Does it ever [go away?]",
        thumb_image=IMG / "anxiety.jpg",
        thumb_accent="orange",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
