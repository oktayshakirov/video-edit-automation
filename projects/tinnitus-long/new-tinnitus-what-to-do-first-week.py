"""New tinnitus, the first week - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/new-tinnitus-what-to-do-first-week.mdx.

**Why this post.** It is the highest-distress, highest-intent page on the site:
somebody whose tinnitus started this week, searching at 1am. The honest answer
is also the counterintuitive one - the first week is about lowering distress,
not forcing silence - so the video has a real reversal to open on rather than a
mood piece.

**The subject is invisible, so it is drawn.** Five drawn graphics in ~34 shots,
chosen before the script and no two sharing an outline:

- `diagram(loop=True)` - the threat loop the article describes. Nothing else in
  the library can draw a cycle, and a list makes this one actively harder to
  follow because a list ends and the loop does not.
- `steps` - the four things to do in the seven days, in order.
- `callout` - the room set up for the night, labelled on a photograph. First
  use of this beat on the channel.
- `checklist`, two-phase, every item struck - what not to do in week one,
  titled as the question its crosses answer.
- `compare` with `name_columns` - the red flags, split same-day / within two
  weeks, which is how the article itself splits them.

**Beat rotation.** `grid` appears in all four of the most recent tinnitus long
forms and is deliberately absent here; `callout` and `checklist` have not run
on this channel recently. `diagram` and `compare` also ran on the concert cut,
which is two shapes of five shared - `loop=True` is a different silhouette from
that cut's straight chain, and no other beat draws a cycle.

**Footage: rooms, hands, windows and screens - not portraits of suffering.**
Every clip was contact-sheeted at three timestamps before it went in the list,
which killed most of the obvious picks: every `earplugs-in-hand-dark` result is
a match, a balloon, a car dashboard or a red abstract; `calendar-days-passing`
is a passing train; every hearing-clinic and audiologist clip screens L104-193.
So protection and the hearing check are carried by words and by the drawn
beats, and the clips that remain are the act - a dark room, a hand on a phone,
a window being opened, somebody writing at a lamp. No ear close-ups.

`OPEN_WIN` lives under `pharmacy-shelf-dark/` and is not a pharmacy: it is a
pair of hands opening a window at night, which is the literal picture of
"let normal life sound in".

**The medical line.** Nothing here promises the tinnitus will stop. Every claim
is the article's own, with its hedges intact ("often", "most people"), the red
flags are on screen as well as spoken, and the routing to a professional
happens twice. No initialisms are spoken.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/new-tinnitus-what-to-do-first-week.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "new-tinnitus-what-to-do-first-week"

# Contact-sheeted at three points across each clip; luma range in the comment.
SIT_UP = STOCK / "videos/woman-sleeping-dark-bedroom-night/11956220.mp4"      # 19.5s, L26-29, sitting up on a bed
BEDROOM = STOCK / "videos/woman-sleeping-dark-bedroom-night/11956219.mp4"     # 28.5s, L30, dim bedroom
QUIET = STOCK / "videos/quiet-bedroom-night-window-silence-dark/11956317.mp4"  # 24.0s, L25, near-black room
SOUND_RM = STOCK / "videos/sound-machine-nightstand-dark-bedroom-ambient/30285726.mp4"  # 22.0s, L23, dim bedroom
CURTAINS = STOCK / "videos/closing-curtains-at-night-dark-room/6944065.mp4"   # 20.7s, L14-26, a lit bedroom, curtains drawn
BULB = STOCK / "videos/hand-switching-off-bedside-lamp-night/853772.mp4"      # 13.4s, L0-30, a filament on black
FAN = STOCK / "videos/ceiling-fan-spinning-dark-room-night/3069096.mp4"       # 15.3s, L4-8, a fan turning in the dark
SOUND_BOX = STOCK / "videos/hand-switching-off-bedside-lamp-night/25951436.mp4"  # 33.6s, L22-23 at the ends, a hand on a bedside sound box with a lit clock
WALK_NIGHT = STOCK / "videos/walking-quiet-street-early-morning-dark/11839732.mp4"  # 22.5s, L20-24, a figure on a lamplit street
PHONE_DK = STOCK / "videos/man-scrolling-social-media-phone-dark/13358555.mp4"  # 14.5s, L14, hands on a phone, screen an indistinct glow
CALL = STOCK / "videos/man-checking-phone-anxious-dark-room/7280528.mp4"      # 18.1s, L42, on a phone call
JOURNAL = STOCK / "videos/woman-writing-journal-notebook-night-lamp-dark/6037421.mp4"  # 22.0s, L27-56, hands writing by a lamp
BREATHE = STOCK / "videos/woman-relaxing-breathing-eyes-closed-dark-room/7191271.mp4"  # 17.6s, L33, slow breathing on a mat
WINDOW_SIT = STOCK / "videos/person-sitting-alone-window-night-dark-room/38136563.mp4"  # 10.6s, L35, sitting in a lit window
LAPTOP = STOCK / "videos/person-relaxing-headphones-sofa-evening-dark/5708839.mp4"  # 15.8s, L36, a laptop on a sofa, one lamp
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

# A man at the window of a lit bedroom, the bed across the foreground and a
# lamp at the right. Landscape, so the beat's fitted photo fills its column
# rather than sitting in it as a narrow stamp.
NIGHT_ROOM = (STOCK / "photos/man-sitting-on-edge-of-bed-at-night-dark-room"
              / "6943996.jpg")                       # 6186x4124, L33/S43

# The Short's source too, picked by the user: a man with his hands at his
# temples, eyes closed, on a plain studio ground. 5760x3840, L139/S17 - far
# brighter than this channel's usual stock, which `render_thumb` normalises,
# and the plain ground is what lets the type sit anywhere.
THUMB_PHOTO = (STOCK / "photos/man-in-black-shirt-user-picked"
               / "8638769.jpg")                      # Pavel Danilyuk, Pexels

VOICE = "mia"                       # same reader as the Short. Candidate.
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/new-tinnitus-what-to-do-first-week"


SECTIONS = [
    # --- hook: the reversal in sentence one, tinnitus named in sentence one --
    Section(
        title="New tinnitus, week one",
        card=False,
        sentences=[
            ("New tinnitus is not a sound you have to fight.",),
            ("The first week is about lowering your distress,",
             "not forcing silence."),
            ("And silence is the one thing that makes it stand out more.",),
            ("By the end you will have a plan for tonight,",
             "four things worth doing this week,",
             "and the signs that mean do not wait."),
        ],
        shots=[
            Shot(clip=CURTAINS, clip_at=2.0),
            Shot(clip=SIT_UP),
            Shot(clip=QUIET),
            Shot(clip=BEDROOM),
        ],
        # 0.85 in front of the contradiction in sentence three - it reverses
        # the two lines before it and needs the silence to reverse into.
        gaps=[0.85, 0.85, 0.85, 0.85],
    ),

    # --- the mechanism: the loop the first week can teach --------------------
    Section(
        title="Why does the first week matter?",
        spoken_title="So why does the first week matter so much?",
        sentences=[
            ("Your brain is very good at learning patterns.",
             "In these first days it decides whether this sound is a threat, "
             "or just background."),
            ("And when it settles on threat, it starts a loop.",),
            # diagram, loop=True - one caption chunk per node, and the last
            # chunk is what the return arrow draws across.
            ("A new sound turns up that you cannot place.",
             "Your brain marks it as something to watch.",
             "So your attention locks onto it, every quiet moment of the day.",
             "It feels louder for being watched, and your sleep takes the hit."),
            ("None of that means anything is getting worse.",
             "It means the loop is running."),
        ],
        shots=[
            Shot(clip=WINDOW_SIT),
            # A filament coming up, and again at the close as a bookend.
            Shot(clip=BULB, clip_at=5.0),
            Shot(graphic="diagram",
                 payload=([("A sound you cannot place", "and it is new",
                            "\U0001F514"),
                           ("Your brain marks it a threat", "so it keeps watch",
                            "\U0001F6A8"),
                           ("Your attention locks on", "every quiet moment",
                            "\U0001F3AF"),
                           ("It feels louder", "and sleep takes the hit",
                            "\U0001F319")],
                          "THE LOOP THE FIRST WEEK CAN TEACH", True)),
            Shot(clip=SOUND_RM, clip_at=11.0),
        ],
        gaps=[0.70, 0.85, 0.90, 0.85],
    ),

    # --- the week's four moves: steps ---------------------------------------
    Section(
        title="What do you do this week?",
        spoken_title="So what do you actually do, in the first seven days?",
        sentences=[
            # steps - one caption chunk per node. The card is the hinge, so
            # there is no lead-in sentence in front of it.
            ("Keep gentle sound in the room, so it is never fully quiet.",
             "Set one wind-down, and keep your wake time the same.",
             "Book a hearing check this week.",
             "And write down what changed."),
            ("A fan, soft music, rain - anything steady and low.",),
            ("Book the hearing check even if it feels mild.",
             "It is how earwax, an infection or a hearing change gets ruled out."),
            ("Keep the notes light - new medicines, a loud night, "
             "a stressful stretch.",),
        ],
        shots=[
            Shot(graphic="steps",
                 payload=([("Sound in the room, kept low", "\U0001F30A"),
                           ("One wind-down, same wake time", "\U0001F319"),
                           ("Book a hearing check", "\U0001F4C5"),
                           ("Note what changed", "\U0001F4DD")],
                          "THE FIRST SEVEN DAYS")),
            Shot(clip=FAN),
            Shot(clip=CALL),
            Shot(clip=JOURNAL, clip_at=1.0),
        ],
        gaps=[0.90, 0.70, 0.75, 0.85],
    ),

    # --- the night: callout on the room itself -------------------------------
    Section(
        title="How do you get through the night?",
        spoken_title="So how do you get through the first night?",
        sentences=[
            ("Night is when the room goes quiet,",
             "and the contrast is sharpest."),
            ("So set the room up before you are in it.",),
            # callout - one caption chunk per label.
            ("Lights down, about forty minutes before bed.",
             "Screens away.",
             "Soft sound on, and kept low.",
             "And the same wake time tomorrow, whatever kind of night it was."),
            ("Keep it just below the tinnitus -",
             "low enough that you can still faintly hear it."),
            ("And if you wake at three in the morning,",
             "do not lie there fighting it."),
            ("Sit up, five slow breaths, a few minutes of calm audio, "
             "then back.",),
        ],
        shots=[
            Shot(clip=CURTAINS, clip_at=12.0),
            Shot(clip=BEDROOM, clip_at=14.0),
            Shot(graphic="callout",
                 payload=(NIGHT_ROOM,
                          [("Screens away", 0.28, 0.32),
                           ("Soft sound, low", 0.16, 0.58),
                           ("Lights down", 0.84, 0.40),
                           ("Same wake time", 0.76, 0.78)],
                          "THE ROOM, SET UP FIRST")),
            Shot(clip=QUIET, clip_at=10.0),
            Shot(clip=SOUND_BOX),
            Shot(clip=BREATHE),
        ],
        gaps=[0.75, 0.90, 0.90, 0.75, 0.85, 0.85],
    ),

    # --- the twist: protect, do not overprotect ------------------------------
    Section(
        title="Should you wear earplugs all day?",
        spoken_title="But should you wear earplugs all day?",
        sentences=[
            ("No.",),
            ("Carry them for genuinely loud places - a concert, a club, "
             "power tools.",
             "But in an ordinary room, let normal life sound in."),
            ("Long stretches of silence, and all-day ear protection, push "
             "your hearing system to turn its own gain up,",
             "and that usually makes tinnitus feel louder, not quieter."),
            ("Same with headphones.",
             "Keep them low, and do not turn them up to drown it out."),
        ],
        shots=[
            Shot(clip=WINDOW_SIT, clip_at=1.5),
            Shot(clip=FAN, clip_at=7.0),
            Shot(clip=SIT_UP, clip_at=10.0),
            Shot(clip=LAPTOP),
        ],
        gaps=[1.10, 0.90, 0.90, 0.85],
    ),

    # --- what not to do: checklist, all struck, titled as its own question ---
    Section(
        title="What should you not do this week?",
        spoken_title="So what should you not do in week one?",
        sentences=[
            # checklist, two-phase - the narration reads the four flat and
            # reacts once, so the crosses land together in the 2.40 pause.
            # The fifth chunk claims no reveal slot; it is the reaction.
            ("Chasing silence.",
             "Wearing earplugs in a quiet room.",
             "Reading tinnitus forums at midnight.",
             "Judging it minute by minute.",
             "Every one of those keeps your attention pointed at the sound."),
            ("Reading other people's worst weeks at midnight is not "
             "information.",),
            ("Give your attention a job instead -",
             "a walk, a chore, something playing quietly next door."),
        ],
        shots=[
            Shot(graphic="checklist",
                 payload=([("Chasing silence", False),
                           ("Earplugs in a quiet room", False),
                           ("Forums at midnight", False),
                           ("Judging it minute by minute", False)],
                          "SHOULD YOU DO ANY OF THESE?")),
            Shot(clip=PHONE_DK),
            Shot(clip=WALK_NIGHT),
        ],
        gaps=[2.40, 0.85, 0.85],
    ),

    # --- red flags, on screen as the medical rule requires -------------------
    Section(
        title="When should you get it checked?",
        spoken_title="But when should you get it checked?",
        sentences=[
            ("Most of this you can do at home.",
             "Some of it you cannot."),
            # compare, name_columns - 8 chunks for 3 + 3, each heading first.
            ("Some of it needs a same-day visit.",
             "Sudden hearing loss in one ear.",
             "Severe dizziness, facial weakness, or ear discharge with a "
             "fever.",
             "Or a whooshing that keeps time with your pulse.",
             "And some of it can wait a week or two.",
             "Any new tinnitus that is still there.",
             "Tinnitus that is wrecking your sleep or your work.",
             "Or anxiety you cannot get on top of."),
            ("Either way, get the hearing test booked.",),
        ],
        shots=[
            Shot(clip=SOUND_RM),
            Shot(graphic="compare",
                 payload=("Same day",
                          ["Sudden hearing loss, one ear",
                           "Severe dizziness or vertigo",
                           "Whooshing with your pulse"],
                          "Within 2 weeks",
                          ["New tinnitus that persists",
                           "Sleep or work suffering",
                           "Anxiety you cannot settle"],
                          True)),
            Shot(clip=CALL, clip_at=9.0),
        ],
        gaps=[0.85, 1.00, 0.85],
    ),

    # --- close: echo the opening, then the question --------------------------
    Section(
        title="Your first week sets the tone, not the future",
        sentences=[
            ("So the first week is not about making it stop.",),
            ("It is about keeping the room from going silent,",
             "protecting your sleep,",
             "and getting one appointment in the diary."),
            ("Most people find it settles over the weeks that follow.",
             "You are not stuck with today."),
            ("So tonight,",
             "what is the one thing you will change in your room?"),
        ],
        shots=[
            Shot(clip=BREATHE, clip_at=9.0),
            Shot(clip=JOURNAL, clip_at=12.0),
            Shot(clip=BULB, clip_at=5.0),
            Shot(clip=SOUND_BOX, clip_at=25.0),
        ],
        gaps=[0.85, 0.80, 0.85, 3.00],
    ),
]

META = Meta(
    title="New Tinnitus? What To Do In The First Week",
    hook="Tinnitus started this week? The first seven days are about lowering "
         "distress, not forcing silence. Here is why the first week matters, "
         "the four things worth doing, how to set the room up for the night, "
         "what to avoid, and the signs that mean see someone now.",
    url=URL,
    summary="Why the first week with new tinnitus is the week your brain "
            "decides whether the sound is a threat or background, the four "
            "things to do in the first seven days, how to set a room up for "
            "the first night, why all-day earplugs and chasing silence "
            "backfire, what not to do in week one, and the red flags that "
            "need a same-day visit or a hearing test within two weeks.",
    tags=["new tinnitus", "tinnitus just started", "what to do first week "
          "tinnitus", "tinnitus first week", "tinnitus", "ringing in ears",
          "tinnitus sleep", "tinnitus advice"],
    cta=f"Full article and sources: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. If you "
             "have sudden hearing loss in one ear, severe dizziness, facial "
             "weakness, ear discharge with a fever, a whooshing that keeps "
             "time with your pulse, a recent head injury or the worst "
             "headache of your life, get seen the same day. Any new tinnitus "
             "that persists needs a hearing test within one to two weeks."],
)


def main() -> None:
    out = Path.home() / "Desktop/new-tinnitus-first-week-long.mp4"
    work = Path.home() / "Desktop/.new-tinnitus-first-week-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # The animated lower third, on the promise line rather than frame one.
        title_at=8.5, title_hold=5.4,
        # Same source and headline as the Short. The rows are forced rather
        # than wrapped, so no phrase is torn across a break, and three short
        # rows let the size search run much larger. The source is landscape
        # and the subject sits in its left third, so `_layout` is left to
        # place the type - no `crop_at`, and therefore no `side` either.
        thumb_headline="NEW TINNITUS.\nWHAT DO YOU\nDO [FIRST?]",
        thumb_image=THUMB_PHOTO, thumb_accent="red",
        # `crop_zoom` 1.0 keeps the full width so the subject is not cut -
        # the auto-scorer zooms in hunting for quiet space and takes half his
        # face with it - and `shift` slides him left to uncover real black for
        # the type rather than laying a scrim over the studio ground.
        thumb_crop_at=(0.5, 0.45), thumb_crop_zoom=1.0,
        thumb_side="right", thumb_shift=0.20,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
