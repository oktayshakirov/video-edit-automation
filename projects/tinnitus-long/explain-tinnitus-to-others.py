"""How to explain tinnitus to others - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/explain-tinnitus-to-others.mdx.

**Why this post.** Nearly every viewer has had the blank stare, and the
article's honest answer is a reversal: describing the sound is the part that
never lands, because nobody else can hear it. What works is short - what it
is, why it changes, one request.

**The subject is invisible, so it is drawn.** Five beats, no two sharing an
outline, and the channel's standing `grid`+`steps`+`compare` recipe is broken
up by the two shapes that can draw something stock cannot:

- `diagram` (straight chain) - why nobody else can hear it.
- `dial`, `value=None` - "invisible does not mean mild": the range, with no
  needle parked on anybody's reading.
- `steps` - the one-minute explanation, in its three parts.
- `grid` - the article's four comparisons.
- `compare` with `name_columns` - the red flags, split same-day / soon, the
  way the article splits them.

**Footage is the act: two people talking.** A sofa, a kitchen, a meeting
table, a patio, a loud bar. `woman-explaining-to-friend-sofa-evening/6973991`
was cut: it is a champagne bottle being opened for its whole length. All fetched fresh for this pair (nothing reused
from another video) and contact-sheeted at three points. No ear close-ups.

**The medical line.** No relief promised. "What helps" is only ever the
viewer's own request to somebody else, which is the article's framing. Red
flags are on screen and spoken, and routed to a clinician.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/explain-tinnitus-to-others.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "explain-tinnitus-to-others"

V = STOCK / "videos"
# Contact-sheeted at 10/50/85% of each clip; duration and luma in the comment.
SILHOUETTE = V / "man-and-woman-talking-night-window-silhouette/10627044.mp4"  # 30s, L37-41, two figures talking in a dark hall
KITCHEN = V / "couple-talking-kitchen-night-dark/7669064.mp4"               # 12s, L26-31, two people talking in a dim kitchen
KITCHEN_2 = V / "couple-talking-kitchen-night-dark/6718229.mp4"             # 8s, L50-54, two women in a doorway, talking
WALK_TWO = V / "friends-walking-together-night-street/8101864.mp4"          # 16s, L23-34, a couple walking a night street
WALK_LIGHTS = V / "friends-walking-together-night-street/7645077.mp4"       # 9s, L39-43, three friends under string lights
STATIC_TV = V / "tv-static-noise-screen-dark/6955107.mp4"                   # 12s, L37-53, an old TV full of static
STATIC_FULL = V / "tv-static-noise-screen-dark/10487961.mp4"                # 6s, L13-14, static, full frame
COUPLE_SOFA = V / "couple-conversation-sofa-lamp-night/6970293.mp4"         # 16s, L47-49, a couple at a coffee table, one lamp
CAMPFIRE = V / "people-talking-campfire-night/15327197.mp4"                 # 20s, L32, friends round a fire
CAMPFIRE_2 = V / "people-talking-campfire-night/8976330.mp4"                # 13s, L30-32, two people talking by a fire
MUG = V / "hands-holding-mug-talking-dark/6245131.mp4"                      # 13s, L51-60, hands round a cup, talking
SHOULDER = V / "hand-on-shoulder-comfort-dark/4763989.mp4"                  # 11s, L30-33, a hand on a shoulder
OFFICE = V / "coworkers-talking-office-meeting-evening-dark/7668496.mp4"    # 11s, L13-15, two coworkers at a meeting table
PATIO_FIRE = V / "friends-sitting-outdoor-patio-night-talking/4594203.mp4"  # 9s, L22-23, a quiet patio with a fire pit
PATIO = V / "friends-sitting-outdoor-patio-night-talking/7645075.mp4"       # 17s, L46-48, friends on a patio
BEDTIME = V / "father-talking-to-child-bedtime-dark/7641190.mp4"            # 37s, L58, a father and child on a bed
BAR = V / "crowded-loud-bar-night-dark/9429656.mp4"                         # 28s, L14-15, a packed, loud bar
CAFE_RED = V / "cafe-terrace-night-lights-people/32201484.mp4"              # 10s, L17-18, a cafe terrace, red lanterns
CAFE_FRONT = V / "cafe-terrace-night-lights-people/10882093.mp4"            # 31s, L36-37, a lit cafe front at night
ENDCARD = V / "subscribe/4928934.mp4"

# Two people talking in a dim bar, dark ceiling above them for the type.
THUMB_PHOTO = (STOCK / "photos/woman-talking-to-friend-evening-lamp-dark-portrait"
               / "6017586.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/explain-tinnitus-to-others"

BANDS = [("Barely there", 0.30, "#ffdab9"),
         ("Distracting", 0.60, "#f2b36b"),
         ("Life-disrupting", 1.00, "#e87878")]


SECTIONS = [
    # --- hook: the reversal, tinnitus named in sentence one -----------------
    Section(
        title="Explaining tinnitus",
        card=False,
        sentences=[
            ("Most people explain tinnitus by describing the sound.",),
            # Says the hook's hidden word, "wrong", ~5s in.
            ("And that is exactly where it goes wrong -",
             "nobody else can hear it."),
            ("What works is shorter:",
             "what it is, why it changes, and one thing they can do."),
            ("By the end you will have a one-minute script,",
             "four comparisons that click,",
             "and the words for home, work and friends."),
        ],
        shots=[
            Shot(clip=SILHOUETTE, clip_at=1.0),
            Shot(clip=COUPLE_SOFA, clip_at=1.0),
            Shot(clip=KITCHEN, clip_at=0.5),
            Shot(clip=WALK_TWO, clip_at=0.5),
        ],
        gaps=[0.90, 0.85, 0.70, 0.85],
    ),

    # --- the mechanism: diagram, then the dial ------------------------------
    Section(
        title="Why can nobody else hear it?",
        spoken_title="So why can nobody else hear it?",
        sentences=[
            ("Because tinnitus is a sound with no source in the room.",),
            # diagram - one caption chunk per node.
            ("There is nothing outside to hear.",
             "Your brain produces a signal of its own.",
             "So it is real to you, and silent to everyone next to you."),
            ("That is why a blank stare is not disbelief.",
             "There is simply nothing for them to notice."),
            ("And invisible does not mean mild.",),
            # dial, value=None - one chunk, one reveal.
            ("It can run from barely there to life-disrupting, and none of it "
             "shows on your face.",),
        ],
        shots=[
            Shot(clip=STATIC_TV, clip_at=1.0),
            Shot(graphic="diagram",
                 payload=([("No sound in the room", "nothing outside to hear",
                            "\U0001F507"),
                           ("Your brain makes a signal", "a sound of its own",
                            "\U0001F9E0"),
                           ("Only you can hear it", "real, but invisible",
                            "\U0001F464")],
                          "WHY THEY CANNOT HEAR IT", False)),
            Shot(clip=BEDTIME, clip_at=22.0),
            Shot(clip=CAMPFIRE, clip_at=1.0),
            Shot(graphic="dial",
                 payload=(BANDS, None, "", "HOW MUCH IT CAN TAKE OVER")),
        ],
        gaps=[0.70, 0.90, 0.85, 0.80, 0.90],
    ),

    # --- the one-minute explanation: steps ----------------------------------
    Section(
        title="What do you actually say?",
        spoken_title="So what do you actually say?",
        sentences=[
            ("Keep it under a minute, in three parts.",),
            # steps - one caption chunk per node.
            ("First, what it is: a sound I hear that is not in the room.",
             "Then why it changes: quiet rooms make it stand out, and stress "
             "can turn it up.",
             "Then one request: could we keep some soft sound on?"),
            ("End on the request, every time.",),
            ("It gives them something to do, instead of something to "
             "imagine.",),
            ("And keep it calm and short.",
             "Your medical history can wait until they ask."),
        ],
        shots=[
            Shot(clip=MUG, clip_at=0.5),
            Shot(graphic="steps",
                 payload=([("What it is", "\U0001F514"),
                           ("Why it changes", "\U0001F92B"),
                           ("One request", "\U0001F64F")],
                          "THE ONE-MINUTE VERSION")),
            Shot(clip=KITCHEN_2, clip_at=0.3),
            Shot(clip=SHOULDER, clip_at=0.5),
            Shot(clip=CAFE_FRONT, clip_at=14.0),
        ],
        gaps=[0.80, 0.90, 0.60, 0.85, 0.85],
    ),

    # --- the comparisons: grid ----------------------------------------------
    Section(
        title="What if they still cannot picture it?",
        spoken_title="But what if they still cannot picture it?",
        sentences=[
            ("Then give them a comparison.",),
            # grid - one caption chunk per card.
            ("A TV with a little static that never fully mutes.",
             "A smoke alarm chirping, when you know there is no fire.",
             "A sunburn of hearing, where quiet moments feel harsher.",
             "Or feeling your phone buzz, when it did not."),
            ("Pick the one that fits the person.",
             "Static for a coworker, the smoke alarm for family."),
            ("A good one makes the sound real,",
             "and explains why you are asking for background sound."),
        ],
        shots=[
            Shot(clip=STATIC_FULL, clip_at=0.3),
            Shot(graphic="grid",
                 payload=([("TV static", "that never fully mutes",
                            "\U0001F4FA"),
                           ("A smoke alarm chirp", "with no fire",
                            "\U0001F6A8"),
                           ("A sunburn of hearing", "quiet feels harsher",
                            "\U0001F31E"),
                           ("A phantom buzz", "a phone that did not ring",
                            "\U0001F4F3")],
                          "COMPARISONS THAT CLICK")),
            Shot(clip=CAMPFIRE_2, clip_at=0.5),
            Shot(clip=PATIO_FIRE, clip_at=0.3),
        ],
        gaps=[0.80, 0.90, 0.60, 0.85],
    ),

    # --- the asks, per listener ---------------------------------------------
    Section(
        title="What do you ask for?",
        spoken_title="So what do you actually ask for?",
        sentences=[
            ("The ask changes with the person, so keep one ready for each.",),
            ("At home: a fan on low at night,",
             "so the bedroom is never fully silent."),
            ("At work: a meeting room with a little background hum,",
             "instead of a dead-quiet one."),
            ("With friends: the patio or the cafe,",
             "not the loud bar that spikes it later."),
            ("And if someone pushes back, say it once more,",
             "then offer another option."),
            ("You are not overreacting.",
             "You are avoiding the spike later."),
        ],
        shots=[
            Shot(clip=WALK_TWO, clip_at=7.0),
            Shot(clip=BEDTIME, clip_at=4.0),
            Shot(clip=OFFICE, clip_at=0.5),
            Shot(clip=PATIO, clip_at=1.0),
            Shot(clip=SILHOUETTE, clip_at=15.0),
            Shot(clip=BAR, clip_at=2.0),
        ],
        gaps=[0.70, 0.55, 0.55, 0.85, 0.80, 0.90],
    ),

    # --- red flags, on screen as the medical rule requires -------------------
    Section(
        title="When is it more than something to explain?",
        spoken_title="But when is it more than something to explain?",
        sentences=[
            ("Explaining it is also a chance to say when you would get it "
             "looked at.",),
            # compare, name_columns - 8 chunks for 3 + 3, heading first.
            ("Some things need care the same day.",
             "Sudden hearing loss.",
             "A pounding that keeps time with your pulse.",
             "Tinnitus after a head injury.",
             "And some need a clinician soon.",
             "New tinnitus in one ear.",
             "Ear pain, pressure or drainage.",
             "Or dizziness that comes with it."),
            ("Tell the people close to you,",
             "and they know what to watch for too."),
        ],
        shots=[
            Shot(clip=MUG, clip_at=4.0),
            Shot(graphic="compare",
                 payload=("Same day",
                          ["Sudden hearing loss",
                           "Pounding with your pulse",
                           "After a head injury"],
                          "See someone soon",
                          ["New, in one ear",
                           "Ear pain or drainage",
                           "With dizziness"],
                          True)),
            Shot(clip=CAMPFIRE, clip_at=10.0),
        ],
        gaps=[0.85, 1.00, 0.85],
    ),

    # --- close: echo the opening, then the question -------------------------
    Section(
        title="Short, kind, and one request",
        sentences=[
            ("So you do not have to make anyone hear it.",),
            ("You need them to know what it is, and what helps.",),
            ("One minute. One comparison. One request.",),
            ("So,",
             "who is the first person you would say it to?"),
        ],
        shots=[
            Shot(clip=WALK_LIGHTS, clip_at=0.5),
            Shot(clip=KITCHEN, clip_at=3.5),
            Shot(clip=CAFE_RED, clip_at=0.5),
            Shot(clip=CAFE_FRONT, clip_at=2.0),
        ],
        gaps=[0.80, 0.85, 0.90, 3.00],
    ),
]

META = Meta(
    title="How to Explain Tinnitus to Family, Friends and Work",
    hook="Nobody else can hear your tinnitus, so describing the sound rarely "
         "lands. Here is a one-minute way to explain it, four comparisons "
         "people actually get, what to ask for at home, at work and with "
         "friends, and the signs that mean get it checked.",
    url=URL,
    summary="Why nobody else can hear tinnitus, why invisible does not mean "
            "mild, a three-part one-minute explanation that ends on a "
            "request, four comparisons (TV static, a smoke alarm chirp, a "
            "sunburn of hearing, a phantom phone buzz), what to ask for at "
            "home, at work and with friends, and the red flags that need a "
            "same-day visit or a clinician soon.",
    tags=["how to explain tinnitus", "explain tinnitus to others",
          "explaining tinnitus to family", "tinnitus at work",
          "living with tinnitus", "tinnitus", "ringing in ears",
          "tinnitus support"],
    cta=f"Full article, with scripts for every situation: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. Sudden "
             "hearing loss, tinnitus that pounds with your pulse, or "
             "tinnitus after a head injury needs care the same day. New "
             "one-sided tinnitus, ear pain, pressure or drainage, or "
             "dizziness with it should be seen by a clinician soon."],
)


def main() -> None:
    out = Path.home() / "Desktop/explain-tinnitus-to-others-long.mp4"
    work = Path.home() / "Desktop/.explain-tinnitus-to-others-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
        # Redacted opening hook; "wrong" is said in sentence two.
        hook="Describing the sound is where it goes [wrong]",
        # Same source and headline as the Short.
        thumb_headline="HOW DO YOU\nEXPLAIN\n[TINNITUS?]",
        thumb_image=THUMB_PHOTO, thumb_accent="red",
        # The two faces sit in the bottom of the portrait source; 0.6 cropped
        # them out and left a ceiling. Type goes on the dark bar at the right.
        thumb_crop_at=(0.5, 0.95), thumb_crop_zoom=1.0, thumb_side="right",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
