"""Can neck tension cause tinnitus? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/can-neck-tension-cause-tinnitus.mdx.

**Why this post.** The title is already a search query, and the honest answer
is a reversal a viewer can act on: the neck does not start tinnitus, but for a
subset of people it moves the volume - and there is a test that tells you
whether you are one of them.

**The beats, and why these five.** `compare` and `steps` are in all four of
the last tinnitus long forms, so the recipe is broken where it can be: the two
shapes carrying the argument here are ones this channel has barely used.

- `diagram(loop=True)` - neck and jaw input into the shared brainstem hub,
  the gain going up, the tension feeding it again. A loop is the one thing a
  list cannot draw, and the article describes exactly this cycle.
- `compare` with `name_columns` - the article's own table, neck/jaw clues
  against ear-driven clues. Kept despite the recipe note because the content
  genuinely is two columns and the split is the safety message.
- `callout` - a photograph of somebody at a desk, labelled. The first use on
  this channel of the beat built for the three quarters of a video that is
  neither a drawn beat nor a site image.
- `steps` - the routine, which has a real order (heat, then movement, then
  micro-breaks, then the setup).
- `grid` - the red flags, on screen as the medical rule requires.

**Footage is the act, not the emotion.** Desks, keyboards, a stretch, a
therapist's hands, steam, a walk. No ear close-ups and no portraits of
somebody suffering. Every clip contact-sheeted at three points before it was
written into a slot; `person-stretching-neck-shoulders-.../36623781` is a
basement gym with dumbbells, `person-adjusting-office-chair-.../4389426` and
`man-sitting-at-computer-.../8212373` are green-lit, `teeth-grinding-...`
is dental surgery in a mouth - all four rejected on the sheet.

**The medical line.** Nothing is diagnosed and nothing is promised. The
routine is described as what people do, never as relief; the red flags are
spoken and on screen and routed to a clinician.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/can-neck-tension-cause-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "can-neck-tension-cause-tinnitus"

V = STOCK / "videos"
# Contact-sheeted at 12/50/85% of each clip; duration and luma in the comment.
HUNCH = V / "person-hunched-over-desk-laptop-night-low-light/13375774.mp4"       # 30s, L7, a head in silhouette bent over a laptop
KEYS = V / "man-working-late-laptop-desk-night-dark-silhouette/34771069.mp4"     # 8s, L21-24, hands on a keyboard, top down
DESK_LAMP = V / "man-working-late-laptop-desk-night-dark-silhouette/32788087.mp4"  # 16s, L35-39, a man at a desk under one lamp, from behind
MONITOR = V / "man-working-late-laptop-desk-night-dark-silhouette/34492301.mp4"  # 9s, L41-43, a man at a monitor, city window behind
STICKY = V / "office-worker-night-desk-lamp-silhouette/20563164.mp4"             # 11s, L16-17, a silhouette at a laptop, notes on the wall
STRETCH = V / "man-stretching-neck-shoulders-at-desk-office-evening-dark/35331903.mp4"  # 13s, L62-64, a man stretching his arms and neck at his desk
THERAPIST = V / "physical-therapist-neck-massage-treatment-dark/6186698.mp4"     # 20s, L56-53, a therapist working on somebody's neck
STEAM = V / "steam-rising-hot-water-dark-night/29686188.mp4"                     # 18s, L18-23, steam rising on black
PHONE = V / "person-turning-head-slowly-dark-room-night/7555163.mp4"             # 13s, L31-34, a lit phone held in one hand, dark room
WALK_ST = V / "woman-walking-at-night-calm-street-dark/11839716.mp4"             # 16s, L21-22, someone walking a quiet night street
CANAL = V / "person-walking-away-quiet-street-night-lamps-dark/9897055.mp4"      # 15s, L16-17, a figure walking a canal path, autumn lamps
NEON = V / "person-walking-away-quiet-street-night-lamps-dark/4121893.mp4"       # 12s, L9-16, a figure on a city street, neon behind
SOFA = V / "woman-sitting-quietly-on-sofa-dark-room-night/5617977.mp4"           # 28s, L12-42, two people on a sofa in a lamp-lit room

# **`person-stretching-neck-shoulders-.../7801731` was cut after it rendered.**
# It is genuinely a woman doing neck and shoulder stretches, which is the act
# this video is about - but the whole clip is framed chest-up on a crop top,
# so every timestamp puts her bust in the middle of the 9:16 band and the
# landscape frame is not much better. Scanning nine timestamps found no usable
# moment: the fault is the framing of the shoot, not the moment chosen. The
# desk stretch above is the same act with the workstation in shot, which is
# also closer to what the script is actually describing.
#
# **Four more clips that passed the luma box were cut on the contact sheet**, all
# of them fetched for these slots and none catchable by a number:
# `16379917` is a hooded figure in sunglasses with papers flying past,
# `3795117` is a parked car outside a lit house with barely a person in it,
# `4029316` is a small lit window in an otherwise empty black frame (L4 by
# being empty, not by being dark), and `16835000` is a green-lit room with a
# shrine in it. The replacements above all have a subject a viewer can name.
BEDROOM = V / "quiet-empty-bedroom-night-dark/11956328.mp4"                      # 15s, L28, somebody sitting up on a bed, one lamp
BED_LAMP = V / "quiet-empty-bedroom-night-dark/11956329.mp4"                     # 9s, L26, an empty bed under a bedside lamp
KEYBOARD = V / "hands-stretching-fingers-desk-night-dark/36392564.mp4"           # 9s, L27-30, a hand working a keyboard, warm lamp
THINK = V / "man-sitting-at-desk-night-close-up-thinking-dark/9618041.mp4"       # 30s, L48-53, a man at a desk, close, hand to his glasses
ENDCARD = V / "subscribe/4928934.mp4"

# The callout's photograph: somebody in profile at a desk, two monitors, dark
# room. Picked for its geometry - head, shoulders, screen and keyboard are all
# readable, which is what the margin labels have to point at. L23.
DESK_PHOTO = (STOCK / "photos/person-at-computer-desk-night-low-light-silhouette-side"
              / "8100048.jpg")

# One source for both aspects: a hand on the back of the neck, in profile,
# near-black. On the noun, no face to the camera, and no ear in frame. L7.
THUMB_PHOTO = (STOCK / "photos/woman-holding-her-neck-pain-dark-portrait-portrait"
               / "12572742.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/can-neck-tension-cause-tinnitus"


SECTIONS = [
    # --- hook: the reversal, tinnitus named in sentence one -----------------
    Section(
        title="Neck tension and tinnitus",
        card=False,
        sentences=[
            # **The long form opens on the Short's own question**, so the pair
            # reads as one piece and the hook's promise is the same promise in
            # both. The reversal that used to open ("tinnitus does not start
            # in your neck") is still here, one sentence later, where it is
            # the answer rather than the greeting.
            ("Can a tight neck really change your tinnitus?",),
            # Says the hook's hidden token, "30", at ~3s - early enough that
            # the gap closes before the opening cliff rather than on it, and
            # a number is the kind of thing a viewer cannot fill in for
            # themselves.
            ("30 seconds is enough to find out -",
             "and for a lot of people, the answer is yes."),
            ("Your neck does not start tinnitus.",
             "But it can move the volume, and that has a name:",
             "somatosensory tinnitus."),
            ("By the end you will know the test that says whether yours has "
             "a neck component,",
             "what tightens the neck,",
             "and the four things that calm it down."),
        ],
        shots=[
            # **The opening section takes the clearest pictures in the cut.**
            # It used to run the hunched silhouette and the sticky-note desk
            # here, and both are near-black frames with the subject in a
            # corner - the same fault the Short was re-cast for, and it sits
            # in the fifteen seconds that decide whether anybody stays. Both
            # still appear later, where a dark frame is a change of pace
            # rather than the video failing to start.
            Shot(clip=STRETCH, clip_at=1.0),
            Shot(clip=THINK, clip_at=4.0),
            Shot(clip=KEYBOARD, clip_at=1.0),
            Shot(clip=DESK_LAMP, clip_at=1.0),
        ],
        gaps=[0.90, 0.85, 0.80, 0.85],
    ),

    # --- the mechanism: the loop --------------------------------------------
    Section(
        title="How does your neck reach your ears?",
        spoken_title="So how does your neck reach your ears?",
        sentences=[
            ("Your neck and jaw are packed with muscles, joints and nerves "
             "that tell your brain where your head is.",),
            # diagram, loop=True - one caption chunk per node.
            ("Those signals land in the same brainstem hubs that handle "
             "sound.",
             "When the neck is tight, that input gets louder and more "
             "erratic.",
             "And the brain answers by turning the gain up on what you "
             "already hear."),
            ("Then the ringing keeps you tense,",
             "and the tension feeds it again."),
            ("It is the same set of controls stress pulls on,",
             "which is why a hard week and a long laptop day land together."),
        ],
        shots=[
            Shot(clip=SOFA, clip_at=1.0),
            Shot(graphic="diagram",
                 payload=([("Neck and jaw signals", "muscles, joints, nerves",
                            "\U0001F4A2"),
                           ("A shared brainstem hub", "touch meets hearing",
                            "\U0001F9E0"),
                           ("The gain goes up", "the ringing stands out more",
                            "\U0001F50A")],
                          "THE LOOP THE ARTICLES DESCRIBE", True)),
            Shot(clip=PHONE, clip_at=1.0),
            Shot(clip=MONITOR, clip_at=0.5),
        ],
        gaps=[0.70, 0.90, 0.85, 0.85],
    ),

    # --- is it neck-related? the article's own table -------------------------
    Section(
        title="Is your tinnitus neck-related?",
        spoken_title="But is your tinnitus actually neck-related?",
        sentences=[
            ("There is a quick way to sort the signals, and the article lays "
             "them out in two groups.",),
            # compare, name_columns - 8 chunks for 3 + 3, each heading first.
            ("Take the neck and jaw clues first.",
             "Turning your head changes the pitch.",
             "Pressing a tender spot moves it.",
             "Stiff shoulders, clenching, tension headaches.",
             "Now compare that with the more ear-driven side.",
             "One ear only, with a new hearing change.",
             "Ear fullness, pain or drainage.",
             "Or it started right after loud noise."),
            ("If moving your head or jaw changes the sound, even for a "
             "second,",
             "your neck is part of the volume."),
            ("That does not make it the only cause.",),
            ("Most people have some of both.",),
        ],
        shots=[
            Shot(clip=HUNCH, clip_at=14.0),
            Shot(graphic="compare",
                 payload=("Neck and jaw clues",
                          ["Changes when you turn",
                           "Moves under pressure",
                           "Stiffness and headaches"],
                          "More ear-driven clues",
                          ["One ear, new hearing change",
                           "Fullness, pain, drainage",
                           "Started after loud noise"],
                          True)),
            Shot(clip=THERAPIST, clip_at=2.0),
            Shot(clip=CANAL, clip_at=1.0),
            Shot(clip=BED_LAMP, clip_at=0.5),
        ],
        gaps=[0.85, 1.00, 0.90, 0.80, 0.85],
    ),

    # --- what tightens it: the labelled photograph ---------------------------
    Section(
        title="What is tightening your neck?",
        spoken_title="So what is actually tightening it?",
        sentences=[
            ("Mostly the ordinary shape of your day.",),
            # callout - one caption chunk per label.
            ("The screen sits off to one side, so the head turns and stays "
             "turned.",
             "The chin drifts forward toward it.",
             "The shoulders creep up and stay there.",
             "And the keyboard sits far enough away to pull on all of it."),
            ("A head held forward loads the muscles at the base of the skull "
             "for hours at a time.",),
            ("Sleep adds to it.",
             "A pillow too high or too flat, and you wake up stiff."),
            ("So does a fall, a crash, or a week the body never lets go.",),
        ],
        shots=[
            Shot(clip=KEYS, clip_at=0.0),
            Shot(graphic="callout",
                 # Read off a decile grid on the source, in the order the
                 # narration names them: monitor right, head and shoulders
                 # left, keyboard right.
                 payload=(DESK_PHOTO,
                          [("Screen to one side", 0.82, 0.30),
                           ("Chin forward", 0.42, 0.22),
                           ("Shoulders up", 0.33, 0.56),
                           ("Keyboard pushed away", 0.68, 0.84)],
                          "THE SHAPE OF A LONG DAY")),
            Shot(clip=STICKY, clip_at=3.0),
            Shot(clip=BEDROOM, clip_at=1.0),
            Shot(clip=NEON, clip_at=1.0),
        ],
        gaps=[0.80, 0.90, 0.85, 0.60, 0.85],
    ),

    # --- the routine ---------------------------------------------------------
    Section(
        title="What actually calms it down?",
        spoken_title="So what actually calms it down?",
        sentences=[
            ("Small and frequent beats big and occasional.",),
            # steps - one caption chunk per node.
            ("Start with heat: ten to fifteen minutes on the neck before you "
             "stretch anything.",
             "Then slow range of motion - turn, tilt and nod, well inside a "
             "pain-free range.",
             "Through the day, posture breaks: sit tall, tuck the chin "
             "gently, let the shoulders drop.",
             "Then the setup: screen up, keyboard close, a pillow that keeps "
             "your head in line."),
            ("Move like you are oiling a hinge, not forcing it.",),
            ("A lot of people pair it with soft background sound, so the "
             "room is never fully silent.",),
            ("And if any of it brings on dizziness, stop,",
             "and ask a professional before you carry on."),
        ],
        shots=[
            Shot(clip=STEAM, clip_at=1.0),
            Shot(graphic="steps",
                 payload=([("Heat first", "\U0001F525"),
                           ("Slow movement", "\U0001F504"),
                           ("Posture breaks", "\U0001FA91"),
                           ("Fix the setup", "\U0001F5A5")],
                          "IN THIS ORDER")),
            Shot(clip=STRETCH, clip_at=4.0),
            Shot(clip=SOFA, clip_at=14.0),
            Shot(clip=CANAL, clip_at=6.0),
        ],
        gaps=[0.80, 0.90, 0.85, 0.85, 0.90],
    ),

    # --- red flags, on screen as the medical rule requires --------------------
    Section(
        title="When is it more than tension?",
        spoken_title="But when is it more than tension?",
        sentences=[
            ("Some things are not a neck problem, and they are worth knowing "
             "by heart.",),
            # grid - one caption chunk per card.
            ("Sudden hearing loss.",
             "A whooshing that keeps time with your pulse.",
             "Severe pain after a blow to the head or neck.",
             "Dizziness that will not settle, or new facial weakness."),
            ("Those are same-day questions for a doctor, not a stretch.",),
            ("New tinnitus in one ear, or ear pain, pressure or drainage, "
             "should be seen soon.",),
            ("For everything else, an audiologist and a physical therapist "
             "with neck and jaw experience are the two to ask.",),
        ],
        shots=[
            Shot(clip=MONITOR, clip_at=0.0),
            Shot(graphic="grid",
                 payload=([("Sudden hearing loss", "same day",
                            "\U0001F515"),
                           ("Whooshing with your pulse", "same day",
                            "\U0001FAC0"),
                           ("After a head injury", "same day",
                            "\U0001F915"),
                           ("Dizziness or weakness", "same day",
                            "⚠️")],
                          "NOT A NECK PROBLEM")),
            Shot(clip=WALK_ST, clip_at=1.0),
            Shot(clip=THERAPIST, clip_at=5.0),
            Shot(clip=DESK_LAMP, clip_at=7.0),
        ],
        gaps=[0.85, 1.00, 0.85, 0.85, 0.90],
    ),

    # --- close: echo the opening, then the question ---------------------------
    Section(
        title="One slider you can reach",
        sentences=[
            ("So your neck does not cause tinnitus.",),
            ("For a lot of people it is one of the sliders that decides how "
             "loud it feels.",),
            ("And a slider is something you can reach.",),
            ("So,",
             "what would you change first: the screen, the pillow, or the ten "
             "minutes before bed?"),
        ],
        shots=[
            Shot(clip=NEON, clip_at=3.0),
            Shot(clip=BED_LAMP, clip_at=0.5),
            Shot(clip=KEYS, clip_at=0.0),
            Shot(clip=WALK_ST, clip_at=8.0),
        ],
        gaps=[0.80, 0.85, 0.90, 3.00],
    ),
]

META = Meta(
    title="Can Neck Tension Cause Tinnitus?",
    hook="A tight neck does not start tinnitus, but for a lot of people it "
         "moves the volume. Here is how neck and jaw input reaches the "
         "hearing system, the test that says whether yours has a neck "
         "component, what tightens the neck in the first place, what calms "
         "it down, and the signs that need a doctor instead.",
    url=URL,
    summary="How neck and jaw signals reach the same brainstem hubs that "
            "handle sound and turn the gain up, the clues that separate "
            "neck-related tinnitus from more ear-driven tinnitus, what "
            "tightens the neck during an ordinary day, a four-part routine "
            "(heat, slow range of motion, posture breaks, the workstation "
            "and pillow), and the red flags that need same-day care.",
    tags=["can neck tension cause tinnitus", "neck tension tinnitus",
          "somatosensory tinnitus", "neck and tinnitus", "posture tinnitus",
          "jaw clenching tinnitus", "tinnitus", "ringing in ears"],
    cta=f"Full article, with the whole routine: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. Sudden "
             "hearing loss, tinnitus that keeps time with your pulse, severe "
             "pain after a head or neck injury, dizziness that will not "
             "settle or new facial weakness need care the same day. New "
             "one-sided tinnitus, ear pain, pressure or drainage should be "
             "seen by a clinician soon."],
)


def main() -> None:
    out = Path.home() / "Desktop/can-neck-tension-cause-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.can-neck-tension-cause-tinnitus-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
        # Redacted opening hook; "30" is said early in sentence two.
        hook="It takes [30 seconds] to find out",
        # Same source and headline as the Short. The headline does not answer
        # the title - it names the part of the answer the viewer has not got.
        thumb_headline="THE\n30-SECOND\n[NECK TEST]",
        thumb_image=THUMB_PHOTO, thumb_accent="red",
        # The hand and the neck sit in the middle of the portrait source; the
        # type goes on the black to the left.
        thumb_crop_at=(0.5, 0.55), thumb_crop_zoom=1.0, thumb_side="left",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
