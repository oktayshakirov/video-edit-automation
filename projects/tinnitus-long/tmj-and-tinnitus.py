"""Can TMJ cause tinnitus? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tmj-and-tinnitus-the-jaw-connection.mdx.

**Why this post.** "Can TMJ cause tinnitus" is a phrase people type, the
answer is a reversal a viewer can act on (the jaw does not start it; for a
subset it moves the volume), and - the part that decided it - the subject is
a *part of a thing*, which is the one case this channel has never been able
to photograph and can now draw.

**The beats, and why these five.** The last pair (`can-neck-tension-cause-
tinnitus`) ran `diagram(loop)`, `compare`, `callout`, `steps`, `grid`. Three
of the five here are different shapes, and the two that repeat are the two
the content genuinely is:

- `anatomy` - the beat built for exactly this script. It names four parts
  and the picture shows which is which; nothing else in the library can.
  It carries a real photograph now, see below.
- `checklist` in `flow` mode - the fingerprints, marked as the narration
  says each verdict. Three ticks and one cross, and the cross is the safety
  message: a sound that keeps time with your pulse is not a jaw sign.
- `chapter` - the turn, full screen. Used seven times across nineteen
  scripts on both channels, so it is the under-used shape `beats.md` says
  to reach for before a fourth list.
- `steps` - the routine, which has a real order.
- `grid` - the red flags, on screen as the medical rule requires.

**`anatomy` had to be fixed before it could be used.** Its docstring said a
caller-supplied `picture=` is annotated; `Beat.draw` painted that picture
into the split layout's *right* column while the callouts pointed at an
empty box in the middle. It now lays the panel out itself, the same way
`callout` does, and the fractions in the payload are fractions of the
photograph. See `beats.md`.

**Footage is the act, not the emotion.** A hand at the jaw, a mouth opening,
somebody chewing, hands going still on a keyboard, a kettle. No ear
close-ups and no portraits of somebody suffering. Every clip was contact-
sheeted at three points and screened across its length; the rejects are
listed below the roster.

**The medical line.** Nothing is diagnosed and nothing is promised. The
routine is described as what people do, never as relief; the strongest claim
in the script is "part of the volume"; the red flags are spoken, drawn and
routed to a clinician.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tmj-and-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "tmj-and-tinnitus-the-jaw-connection"

V = STOCK / "videos"
# Contact-sheeted at 12/50/85% of each clip; duration and luma in the comment.
# Every one of these is fetched for this video: an inventory of the other
# projects' ids came first, and anything already spent elsewhere was dropped
# rather than re-used (`footage.md`, "An asset used in another video").
JAWHANDS = V / "hand-holding-jaw-pain-dark/19149084.mp4"                    # 29.2s, L15-22, hands coming up to the jaw and holding it
CHEEK = V / "close-up-hand-on-cheek-jaw-dark-low-key/5119257.mp4"           # 15.4s, L32-35, a hand over the mouth and jaw, close
PROFILE = V / "close-up-hand-on-cheek-jaw-dark-low-key/34725795.mp4"        # 15.3s, L15, a jaw in profile, near black
MOUTH = V / "man-stretching-mouth-opening-jaw-dark/6144020.mp4"            # 14.5s, L20, a mouth and jaw opening, profile, near black
DESK = V / "hand-on-desk-pause-break-office-night-dark/5473794.mp4"         # 28.0s, L41-44, hands on a keyboard at a lit desk, then still
KEYS = V / "tired-office-worker-late-night-screen-glow-dark/34771086.mp4"   # 8.5s, L18, a hand resting beside a laptop, very dark
CHEW = V / "person-chewing-food-dark-low-light/7801573.mp4"                 # 27.0s, L47-55, someone eating by a window, profile
KETTLE = V / "steam-kettle-hot-water-night-dark-kitchen/35674426.mp4"       # 16.2s, L39-51, a kettle poured into a mug, warm kitchen
STREET = V / "man-walking-home-late-night-empty-street/7251411.mp4"         # 27.5s, L46-48, a man waiting on a quiet street at night
ALARM = V / "phone-alarm-on-nightstand-dark-bedroom/1190185.mp4"            # 28.0s, L0-21, a phone alarm reading 5:00 AM on black
DARKROOM = V / "man-clenching-jaw-night-dark-low-light/5617895.mp4"         # 13.7s, L6-18, a man sitting in an unlit room
TRACKPAD = V / "hand-on-laptop-trackpad-night-dark-close/39425747.mp4"      # 19.0s, L21-23, a hand hovering over a keyboard, warm
LAPTOP = V / "man-closing-laptop-end-of-day-dark-office/5495841.mp4"        # 17.2s, L24-27, a man at a laptop under one hanging bulb
WINDOW = V / "person-looking-out-window-night-city-dark-room/8591730.mp4"   # 25.4s, L30-38, someone at a window over a lit city
REST = V / "woman-resting-head-hand-evening-dark-room/6466353.mp4"          # 22.3s, L24-36, a head resting on a hand, warm lamp
DRIVE = V / "commuter-car-driving-at-night-dark-interior/35220997.mp4"      # 23.4s, L29-42, a windscreen on a wet road at night
HAND = V / "close-up-hands-stretching-fingers-night-dark/7298371.mp4"       # 14.3s, L19-21, one hand opening slowly on near-black
BALCONY = V / "person-looking-out-window-night-city-dark-room/38380402.mp4" # 12.4s, L51, a man on a balcony over a lit city. The one
                                                                           # clip in the roster over the L48 stock ceiling, and it is
                                                                           # over it by being a *city at night* - the light is in the
                                                                           # towers behind the subject, not on him.
ENDCARD = V / "subscribe/4928934.mp4"

# **Nine clips were cut on the sheet, none of them catchable by a number.**
# `man-clenching-jaw-.../10577436` is lit hard teal, which is the one hue that
# cuts worst against peach; `person-chewing-food/10473646` is a man being fed
# behind prison bars; `dentist-mouth-guard-.../6763249` is dental surgery
# inside an open mouth, the same reject the neck pair recorded;
# `physiotherapist-face-jaw-massage/6629856` is a topless spa treatment and
# reads as an advert; `woman-massaging-jawline/6443762` is a jade roller in a
# white room at L155; `warm-compress-face-dark/19224471` is a hand dragging
# down a face in purple light; `person-sitting-quietly/6470619` is lit violet;
# `hand-holding-jaw-pain/4588244` is hands over the face and reads as crying;
# `person-soft-food-bowl/38637309` is a pot on a camp fire.

# The `anatomy` beat's photograph: a head in profile on a near-black ground,
# fetched for this beat. L37/S3. The four callout coordinates below were read
# off a decile grid on this file, so they are fractions of *it*, not of the
# frame - which is what the fixed beat now lays out.
PROFILE_PHOTO = (STOCK / "photos/man-face-profile-side-view-dark-black-background-landscape"
                 / "7248190.jpg")

# One source for both aspects. **The user picked this file by URL** after the
# first cut, replacing a near-black portrait: a jaw and cheek in three-quarter
# profile, filling the frame. It is far brighter than this channel's usual
# thumbnail source (L124/S27 against L20), which is a deliberate break - the
# stock luma box is about footage cutting against the brand *inside* a video,
# and a thumbnail competes in a grid instead.
THUMB_PHOTO = (STOCK / "photos/close-up-shot-of-a-pretty-woman-10648949"
               / "10648949.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/tmj-and-tinnitus-the-jaw-connection"


SECTIONS = [
    # --- hook: the question, then a partial answer that names a part --------
    Section(
        title="Your jaw and your tinnitus",
        card=False,
        sentences=[
            # Subject named in sentence one, and it is the phrase the title
            # is built from - the Search opener is typing the same words.
            ("Can your jaw really change your tinnitus?",),
            # Sentence two gives something new and opens a bigger question:
            # there is a joint you can feel, and it is closer to your ear
            # than you think. It does not hand over the verdict.
            ("For a lot of people it can -",
             "and you can feel the reason with two fingers,",
             "right in front of your ear."),
            ("That is the jaw joint, the T M J,",
             "and it is one of the most overlooked things on this whole "
             "subject."),
            ("By the end you will know the signs that say yours has a jaw "
             "component,",
             "what calms a clenched jaw,",
             "and what belongs to a doctor instead."),
        ],
        shots=[
            # The opening slot is the tightest shot in the cut, and it is on
            # the noun: a hand coming up to the jaw. It comes back at the
            # close as the bookend, which is its second and last use.
            Shot(clip=JAWHANDS, clip_at=12.0),
            None,                                  # hold it through the answer
            Shot(clip=DESK, clip_at=2.0),
            Shot(clip=LAPTOP, clip_at=2.0),
        ],
        gaps=[0.90, 0.85, 0.80, 0.85],
    ),

    # --- the mechanism: which part is where ---------------------------------
    Section(
        title="How can your jaw reach your ears?",
        spoken_title="So how can a jaw joint reach your ears?",
        sentences=[
            ("It is a question of neighbours.",),
            # anatomy - one caption chunk per callout, in payload order.
            ("The joint itself sits a finger's width in front of your ear "
             "canal.",
             "Your ear canal is right behind it.",
             "The big chewing muscle runs down your cheek to the jaw.",
             "And another one fans out across your temple."),
            ("All of it runs into the same nerve branches, and those "
             "branches report to the part of the brainstem that handles "
             "sound.",),
            ("So a jaw clenched all day feeds a constant signal into a "
             "system that is already listening.",),
            ("That crossover has a name - somatosensory modulation.",
             "Body input, changing how loud a sound feels."),
        ],
        shots=[
            Shot(clip=CHEEK, clip_at=0.5),
            Shot(graphic="anatomy",
                 picture=PROFILE_PHOTO,
                 payload=([("The jaw joint", 0.652, 0.450, "l"),
                           ("Your ear canal", 0.700, 0.425, "r"),
                           ("Masseter", 0.628, 0.575, "l"),
                           ("Temporalis", 0.640, 0.285, "r")],
                          "THE NEIGHBOURHOOD")),
            Shot(clip=TRACKPAD, clip_at=2.0),
            None,                                  # one picture, two sentences
            Shot(clip=HAND, clip_at=1.0),
        ],
        gaps=[0.70, 1.00, 0.85, 0.80, 0.90],
    ),

    # --- the fingerprints, judged -------------------------------------------
    Section(
        title="Is your tinnitus jaw-related?",
        spoken_title="But is your tinnitus actually jaw-related?",
        sentences=[
            ("Jaw-driven tinnitus leaves fingerprints, so here are four to "
             "check.",),
            # checklist, flow=True - the narration carries each verdict, so
            # the marks land on the words rather than in a held pause.
            ("The sound changes when you open wide. That counts.",
             "Your jaw clicks or pops when you chew. That counts too.",
             "You wake up with a tight jaw or an ache at your temple. Also "
             "counts.",
             "But a sound that keeps time with your heartbeat is not a jaw "
             "sign at all."),
            ("If moving your jaw changes the sound, even for a second,",
             "your jaw is part of the volume."),
            ("Which is not the same as saying it started there.",),
        ],
        shots=[
            Shot(clip=DARKROOM, clip_at=5.0),
            Shot(graphic="checklist",
                 payload=([("Changes when you open wide", True),
                           ("Clicks or pops when you chew", True),
                           ("Tight jaw in the morning", True),
                           ("Keeps time with your pulse", False)],
                          "DOES YOURS DO THIS?", True)),
            Shot(clip=REST, clip_at=2.0),
            Shot(clip=ALARM, clip_at=14.0),
        ],
        gaps=[0.90, 1.20, 0.90, 0.85],
    ),

    # --- what is doing the clenching ----------------------------------------
    Section(
        title="What is clenching it all day?",
        spoken_title="So what is clenching it in the first place?",
        sentences=[
            ("Mostly nothing dramatic.",),
            ("Your teeth are only meant to touch when you chew or swallow -",
             "and for a lot of people they are together all day."),
            ("A hard email, a long drive, a deadline, and the molars quietly "
             "go and stay there.",),
            ("Then there is the night shift: grinding, which most people "
             "only hear about from a partner or a dentist.",),
        ],
        shots=[
            Shot(clip=KEYS, clip_at=0.0),
            Shot(clip=DESK, clip_at=16.0),
            Shot(clip=DRIVE, clip_at=2.0),
            Shot(clip=WINDOW, clip_at=2.0),
        ],
        gaps=[0.80, 0.90, 0.80, 0.90],
    ),

    # --- the turn, full screen ----------------------------------------------
    Section(
        title="One thing worth being clear about",
        card=False,
        sentences=[
            ("So before the routine, one thing worth being clear about.",),
            # chapter - the statement the section has been building to. The
            # card burns no caption; the spoken half is the sentence.
            ("Your jaw is not the cause of your tinnitus. It can be part of "
             "the volume.",),
            ("Which is the useful half: a volume control is something you "
             "can put your hands on.",),
        ],
        shots=[
            Shot(clip=STREET, clip_at=2.0),
            Shot(graphic="chapter",
                 payload=("NOT THE CAUSE.\nPART OF THE VOLUME.",)),
            Shot(clip=BALCONY, clip_at=0.5),
        ],
        gaps=[0.85, 1.30, 0.90],
    ),

    # --- the routine ---------------------------------------------------------
    Section(
        title="What calms a tight jaw?",
        spoken_title="So what actually calms it down?",
        sentences=[
            ("Small and frequent beats big and occasional, and it has an "
             "order.",),
            # steps - one caption chunk per node.
            ("First, the resting position: teeth apart, lips together, the "
             "tip of your tongue on the roof of your mouth.",
             "Then heat - ten to fifteen minutes on the cheek and temple "
             "before you move anything.",
             "Then eat softer for a couple of weeks. No gum, nothing chewy.",
             "And through the day, unglue your molars every half hour."),
            ("And when you yawn, let your mouth open straight down rather "
             "than wide and off to one side.",),
            ("None of that is a treatment, and none of it is quick.",),
            ("It is what people do to take the load off a joint that has "
             "been working overtime.",),
        ],
        shots=[
            Shot(clip=KETTLE, clip_at=0.5),
            Shot(graphic="steps",
                 payload=([("Teeth apart", "\U0001F62E"),
                           ("Heat, then move", "\U0001F525"),
                           ("Chew softer", "\U0001F944"),
                           ("Unclench hourly", "\U000023F0")],
                          "IN THIS ORDER")),
            Shot(clip=MOUTH, clip_at=6.0),
            Shot(clip=TRACKPAD, clip_at=10.0),
            Shot(clip=LAPTOP, clip_at=9.0),
        ],
        gaps=[0.85, 1.00, 0.85, 0.80, 0.90],
    ),

    # --- red flags, spoken and drawn -----------------------------------------
    Section(
        title="When is it more than the jaw?",
        spoken_title="But when is it more than the jaw?",
        sentences=[
            ("Some things are not a jaw problem, and they are worth knowing "
             "by heart.",),
            # grid - one caption chunk per card.
            ("Hearing that drops suddenly.",
             "A whooshing that keeps time with your pulse.",
             "A jaw that locks, or severe pain after a blow to the head.",
             "Ear pain, pressure or fluid, especially with a fever."),
            ("Those are questions for a doctor the same day, not a "
             "stretch.",),
            ("And if your jaw clicks and aches most days, ask a dentist "
             "trained in orofacial pain, or a physical therapist who works "
             "on jaws.",),
        ],
        shots=[
            Shot(clip=DRIVE, clip_at=12.0),
            Shot(graphic="grid",
                 payload=([("Sudden hearing loss", "same day", "\U0001F515"),
                           ("Whooshing with your pulse", "same day",
                            "\U0001FAC0"),
                           ("A locked or injured jaw", "same day",
                            "\U0001F915"),
                           ("Ear pain or fluid", "soon", "⚠️")],
                          "NOT A JAW PROBLEM")),
            Shot(clip=DARKROOM, clip_at=5.0),
            Shot(clip=REST, clip_at=11.0),
        ],
        gaps=[0.85, 1.00, 0.85, 0.90],
    ),

    # --- close: echo the opening, then the question ---------------------------
    Section(
        title="Two fingers in front of your ear",
        sentences=[
            ("So, back to the two fingers in front of your ear.",),
            ("If the sound moves when your jaw moves, you have found "
             "something you can actually work on.",),
            ("Not a cause. A control.",),
            ("So,",
             "check it now: are your teeth touching, right at this moment?"),
        ],
        shots=[
            # The close comes back to the jaw the video opened on - a
            # different shot of the same subject rather than a third use of
            # the opening clip, which the reuse budget spends on the Short.
            Shot(clip=PROFILE, clip_at=0.5),
            None,
            Shot(clip=STREET, clip_at=18.0),
            Shot(clip=BALCONY, clip_at=3.0),
        ],
        gaps=[0.85, 0.85, 0.90, 3.00],
    ),
]

META = Meta(
    title="Can TMJ Cause Tinnitus?",
    hook="Your jaw joint sits a finger's width in front of your ear canal, "
         "and for a lot of people a clenched jaw moves the volume on their "
         "tinnitus. Here is how jaw input reaches the hearing system, the "
         "signs that say yours has a jaw component, what calms a tight jaw, "
         "and the symptoms that need a doctor instead.",
    url=URL,
    summary="How the jaw joint, the chewing muscles and the nerves they "
            "share reach the same brainstem hubs that handle sound, the "
            "fingerprints that separate jaw-related tinnitus from other "
            "kinds, what keeps a jaw clenched through an ordinary day, a "
            "four-part routine (resting jaw position, heat, softer chewing, "
            "hourly unclenching), and the red flags that need same-day care.",
    tags=["can tmj cause tinnitus", "tmj tinnitus", "jaw and tinnitus",
          "somatosensory tinnitus", "jaw clenching tinnitus",
          "teeth grinding tinnitus", "tinnitus", "ringing in ears"],
    cta=f"Full article, with the whole routine: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. Sudden "
             "hearing loss, tinnitus that keeps time with your pulse, a "
             "locked jaw or severe pain after a head injury, and ear pain, "
             "pressure or fluid with a fever all need care the same day. A "
             "jaw that clicks and aches most days is worth taking to a "
             "dentist trained in orofacial pain or a physical therapist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tmj-and-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.tmj-and-tinnitus-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
        # **The opener rotates.** The last three scripts on this channel all
        # opened on the redacted hook, which is the template look the opener
        # set exists to break. `Search` is the right one here rather than a
        # free choice: the long-form title *is* the phrase somebody types,
        # so the opener shows the viewer their own question being asked. It
        # shows no answer - that is the video.
        opener=Search("can tmj cause tinnitus"),
        # Same source and headline as the Short. It asks the title's own
        # question and answers nothing.
        thumb_headline="Can your jaw change your [tinnitus?]",
        thumb_image=THUMB_PHOTO, thumb_accent="red",
        # The subject fills the source, so the crop is about which part of
        # her survives it: at y=0.34 the chin and jawline - the noun the
        # headline names - fall off the bottom. y=0.50 keeps the jaw and an
        # eye, and the type sits on the dark hair to the left.
        thumb_crop_at=(0.55, 0.50), thumb_crop_zoom=1.0, thumb_side="left",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
