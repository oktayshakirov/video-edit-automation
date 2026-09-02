"""Why can you hear your heartbeat in your ear - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/pulsatile-tinnitus-why-you-hear-your-heartbeat.mdx

**Why this post.** The title is already the exact phrase people type into
YouTube at 2am, and the honest answer is counterintuitive and useful: this
specific kind of tinnitus usually has a physical, findable source - often
blood flow near the ear - which makes it the one type where chasing the
cause is on the table. That is the arc: name the fear, reframe it as
findable, walk the mechanism, then route hard to a doctor with the article's
own red flags on screen.

**Beat variety, chosen before the script** (silhouette rule): `compare` with
`name_columns` (normal tinnitus vs the pulsing kind), `stat` (how few people
hear this kind), `grid` (the four cause groups, with icons), `checklist` with
`flow` (the routine red flags), `steps` (what to do while you wait, with
icons). No two carded sections share an outline.

**The medical line - this is the scariest topic on the list.** Everything
factual is the article's own: subjective vs objective, turbulent flow
amplified by the middle ear, the four cause groups, the 4-10% figure, the red
flags, the "while you wait" tips. Nothing promises relief or a cure - the
article's own "often an identifiable, sometimes treatable cause" is stated as
what the article says and always paired with "get it evaluated". The close
routes to a doctor and puts the urgent red flags on screen as a statement
card. No initialisms are spoken - "pressure around the brain", "a scan",
"talking therapy".

**Footage.** Fresh dark roster - the channel's popular clips are already
recycled across the other six videos, and every site image for this topic is
medical stock shot on white (cardiologist L196, audiologist L179). Nothing
from the site library is dark enough, so the pair is stock plus the drawn
beats.

**Phonemes.** `pulsatile` -> "PULL-suh-tile", `carotid`, `vascular`,
`anemia`, `thyroid` all phonemize cleanly. No initialisms spoken.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/pulsatile-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "pulsatile-tinnitus-why-you-hear-your-heartbeat"

# Screened with `stock.screen` at 0.5/3/6/9s and then watched. Trailing comment
# is the luma range across the clip.
BED_M = STOCK / "videos/man-awake-in-bed-at-night-dark-bedroom-listening"    # 8376628 21s L24-27
BED_W = STOCK / "videos/woman-lying-in-bed-at-night-cant-sleep-dark"         # 11956219 29s L31 / 7986744 11s L21
WORRIED_M = STOCK / "videos/close-up-worried-man-face-dark-room"             # 7279026 30s / 8458651 19s L35-46
WORRIED_SOFA = STOCK / "videos/man-sitting-on-sofa-at-night-thinking-worried-dark"  # 7280528 18s L42
BED_W_UP = STOCK / "videos/woman-sitting-up-in-bed-at-night-worried-dark"    # 7280521 15s / 7698902 17s L34-39
WAKE = STOCK / "videos/person-waking-up-sitting-on-edge-of-bed-night-dark"   # 30285726 22s / 11956220 20s L23-29
LAMP = STOCK / "videos/bedside-table-lamp-dark-bedroom-night"               # 10387906 26s / 8631662 13s L35-46
BLOOD = STOCK / "videos/red-blood-cells-flowing-artery-medical-animation-dark"  # 35217626 / 35211221 10s L15-22
VEIN = STOCK / "videos/dark-abstract-vein-network-pulsing-red-black"        # 34127955 20s L7-10 / 37103859 10s L6-24
SCAN = STOCK / "videos/medical-scan-radiology-monitor-dark"                # 7088464 22s L37-40 S6
PHONE = STOCK / "videos/hand-holding-phone-booking-appointment-at-night-dark"  # 6414098 19s L30-38
BREATHE = STOCK / "videos/man-breathing-deeply-eyes-closed-dark-room-calm"  # 5495782 12s L33 S11
JOURNAL = STOCK / "videos/man-writing-in-journal-notebook-at-night-lamp-dark"  # 7062985 14s L48 S0
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "otis"                     # the male article reader (bare am_puck, ENERGETIC)
MUSIC = music.track("night-drift")  # the prepared track, shared with thecrypto.wiki

URL = "https://tinnitushelp.me/blog/pulsatile-tinnitus-why-you-hear-your-heartbeat"
A = 16 / 9


SECTIONS = [
    # --- hook: name pulsatile tinnitus by sentence three -----------------
    Section(
        title="A beat in your ear",
        card=False,
        sentences=[
            ("You lie down in a quiet room,",
             "and your ear starts keeping time with your heart.",
             "A soft whoosh, matched to your pulse."),
            ("That sound has a name.",
             "It is called pulsatile tinnitus."),
            ("It is a less common kind of tinnitus,",
             "and unlike the usual ringing,",
             "it often has a physical cause you can actually find."),
            ("Stay with this and you will know why you hear it,",
             "which signs mean see a doctor soon,",
             "and what helps in the meantime."),
        ],
        shots=[
            Shot(clip=BED_M / "8376628.mp4"),
            Shot(clip=WORRIED_M / "7279026.mp4"),
            None,
            # Title stamp on the promise line, ~8s in - a dark radiology
            # monitor, which reads as "find the cause".
            Shot(clip=SCAN / "7088464.mp4",
                 payload=("", "WHY CAN YOU HEAR YOUR HEARTBEAT?")),
        ],
        gaps=[0.55, 0.80, 0.55, 0.45],
    ),

    # --- reframe: subjective vs objective + the twist, so `compare` -----
    Section(
        title="What makes this kind different?",
        spoken_title="So what makes this kind different?",
        sentences=[
            ("Most tinnitus is subjective.",
             "Only you can hear it."),
            ("But some pulsatile tinnitus is objective.",
             "It is a real, physical sound,",
             "and a doctor can sometimes hear it too."),
            # 8 caption chunks: two headings plus three items a side, in the
            # order the voice says them. No lead-in sentence inside the span.
            ("Take the usual tinnitus.",
             "A steady ring or buzz.",
             "From hearing loss or noise.",
             "You manage the symptom.",
             "Now the pulsing kind.",
             "A whoosh timed to your pulse.",
             "Often from blood flow.",
             "And the cause can be treated."),
            ("So the pulsing kind often points to one findable thing,",
             "and that can sometimes be fixed."),
            ("That is the reason to get it checked.",
             "Not the reason to panic."),
        ],
        shots=[
            Shot(clip=WORRIED_SOFA / "7280528.mp4"),
            # No dark stethoscope/clinic clip exists - medical stock is all
            # shot on white (L80-175), and the first pick (a stethoscope at
            # L3-15) rendered as an almost-black frame. This reuses the hook's
            # worried-man face (L35-46, the brightest clip in the roster) as a
            # deliberate echo; the narration carries "a doctor".
            Shot(clip=WORRIED_M / "7279026.mp4", clip_at=6.0),
            Shot(graphic="compare",
                 payload=("The usual tinnitus",
                          ["A steady ring or buzz",
                           "From hearing loss or noise",
                           "You manage the symptom"],
                          "The pulsing kind",
                          ["A whoosh timed to your pulse",
                           "Often from blood flow",
                           "The cause can be treated"],
                          True)),
            Shot(clip=SCAN / "7088464.mp4", clip_at=8.0),
            Shot(clip=WORRIED_M / "8458651.mp4"),
        ],
        gaps=[0.55, 0.55, 0.34, 0.60, 0.85],
    ),

    # --- the science: turbulent flow, so `stat` ------------------------
    Section(
        title="So why is your pulse suddenly loud?",
        spoken_title="So why is your pulse suddenly loud?",
        sentences=[
            ("Your ears sit right next to a busy network of arteries and veins.",),
            ("If a vessel narrows, kinks, or comes under pressure,",
             "the blood flow turns turbulent,",
             "like water forced through a pinched hose."),
            ("That turbulence makes a sound,",
             "and your middle ear amplifies it",
             "into the whoosh you hear."),
            ("And across everyone with tinnitus,",
             "only about four to ten percent",
             "hear this pulsing kind."),
        ],
        shots=[
            Shot(clip=VEIN / "34127955.mp4"),
            Shot(clip=BLOOD / "35217626.mp4"),
            Shot(clip=BLOOD / "35211221.mp4"),
            Shot(graphic="stat",
                 payload=("4-10%", "HEAR THE PULSING KIND",
                          "Most tinnitus does not sync with your pulse.",
                          False)),
        ],
        gaps=[0.45, 0.34, 0.55, 0.80],
    ),

    # --- the four cause groups, so `grid` -----------------------------
    Section(
        title="So what is actually behind it?",
        spoken_title="So what is actually behind it?",
        sentences=[
            ("The causes fall into four groups.",),
            ("Blood flow changes near the ear.",
             "Pressure around the brain, more often in younger women.",
             "A middle ear problem, like fluid or a small growth.",
             "Whole-body factors, like anemia, thyroid trouble, or pregnancy."),
            ("Some are harmless.",
             "Some need attention soon.",
             "Which is why this kind is worth checking."),
        ],
        shots=[
            Shot(clip=WORRIED_SOFA / "7280528.mp4", clip_at=8.0),
            Shot(graphic="grid",
                 payload=([("Blood flow near the ear",
                            "Narrowed or turbulent vessels", "\U0001F493"),
                           ("Pressure around the brain",
                            "More often in younger women", "\U0001F9E0"),
                           ("A middle ear problem",
                            "Fluid, or a small growth", "\U0001F442"),
                           ("Whole-body factors",
                            "Anemia, thyroid, pregnancy, fever",
                            "\U0001F321️")],
                          "WHAT CAN CAUSE IT")),
            Shot(clip=BED_W_UP / "7280521.mp4"),
        ],
        gaps=[0.60, 0.34, 0.70],
    ),

    # --- red flags: `checklist` with flow, then a statement card -------
    Section(
        title="So when should you see someone?",
        spoken_title="So when should you actually see someone?",
        sentences=[
            ("Call your doctor if any of these fit.",),
            ("It started suddenly.",
             "It is only in one ear.",
             "It followed a head or neck injury.",
             "It changes when you move your head."),
            ("And treat it as urgent",
             "if it comes with headaches or vision changes,",
             "with severe neck pain,",
             "or with any weakness, facial droop, or slurred speech."),
            ("None of this is meant to scare you.",
             "Most causes are manageable.",
             "It is about getting the right one named."),
        ],
        shots=[
            Shot(clip=WAKE / "30285726.mp4"),
            Shot(graphic="checklist",
                 payload=([("It started suddenly", True),
                           ("It is only in one ear", True),
                           ("It followed a head or neck injury", True),
                           ("It changes when you move your head", True)],
                          "CALL YOUR DOCTOR IF",
                          True)),                       # flow
            Shot(clip=WAKE / "11956220.mp4",
                 payload=("SEEK CARE NOW IF",
                          "Headaches or vision changes, severe neck pain, "
                          "or any weakness, facial droop, or slurred speech.")),
            Shot(clip=BREATHE / "5495782.mp4"),
        ],
        gaps=[0.55, 0.34, 0.34, 0.85],
    ),

    # --- while you wait: a routine, so `steps` ------------------------
    Section(
        title="So what can you do tonight?",
        spoken_title="So what can you do tonight?",
        sentences=[
            ("While you wait for that appointment,",
             "a few things take the edge off."),
            ("Add soft sound at night, kept just below the whoosh.",
             "Raise the head of your bed a little.",
             "Keep caffeine to earlier in the day.",
             "Wind the stress down, with slow breathing or a few quiet minutes.",
             "And log what changes the sound, to show your doctor."),
            ("These do not fix the cause.",
             "They just make the wait easier."),
        ],
        shots=[
            Shot(clip=LAMP / "10387906.mp4"),
            Shot(graphic="steps",
                 payload=([("Soft sound, just below it", "\U0001F30A"),
                           ("Raise the head of the bed", "\U0001F634"),
                           ("Caffeine earlier in the day", "\U00002600\U0000FE0F"),
                           ("Slow the breathing", "\U0001FAC1"),
                           ("Track what changes it", "\U0001F4DD")],
                          "WHILE YOU WAIT")),
            Shot(clip=JOURNAL / "7062985.mp4"),
        ],
        gaps=[0.55, 0.34, 0.70],
    ),

    # --- close: the echo, then the routing --------------------------
    Section(
        title="So the drumbeat in your ear",
        sentences=[
            ("So, that whoosh in your ear",
             "is the sound of your pulse,",
             "carried to your hearing by blood flow nearby."),
            ("Usually it points to something a doctor can find,",
             "and often to something they can help."),
            ("Get it checked,",
             "especially if it is new, one-sided, or came on suddenly."),
            ("You do not have to let that drumbeat run the show.",),
            ("And if this helped,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(clip=VEIN / "37103859.mp4"),
            Shot(clip=PHONE / "6414098.mp4"),
            None,
            Shot(clip=WORRIED_M / "8458651.mp4", clip_at=8.0),
            Shot(clip=BREATHE / "5495782.mp4", clip_at=4.0),
        ],
        gaps=[0.60, 0.60, 0.80, 0.90, 3.00],
    ),
]

META = Meta(
    title="Why Can You Hear Your Heartbeat in Your Ear?",
    hook="A whooshing pulse in one ear is called pulsatile tinnitus. Unlike "
         "the usual ringing, this kind usually has a physical cause you can "
         "find - here is what is happening, the red flags that need a doctor, "
         "and what helps while you wait.",
    url=URL,
    summary="What pulsatile tinnitus is and how it differs from ordinary "
            "ringing, why turbulent blood flow near the ear gets amplified "
            "into a whoosh, the four groups of causes, when the pattern needs "
            "a doctor and when it is urgent, and practical steps to take the "
            "edge off while you wait for evaluation.",
    tags=["tinnitus", "pulsatile tinnitus", "heartbeat in ear",
          "whooshing sound in ear", "hear my pulse in my ear",
          "ringing in ears"],
    cta=f"Full article, the red flags and sources: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: night-drift.",
             "",
             "This video is general information, not medical advice. "
             "Pulsatile tinnitus - especially if it is new, one-sided, "
             "sudden, or comes with headaches, vision changes, neck pain, or "
             "neurological symptoms - should be evaluated by a doctor."],
)


def main() -> None:
    out = Path.home() / "Desktop/pulsatile-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.pulsatile-tinnitus-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # Same source and headline as the Short. A straight cover crop
        # (`crop_zoom=1.0`) - the source is wide and the woman is centred with
        # plain wall either side, so cover scale fills the frame at the least
        # possible zoom and loses only background. Type on the left.
        thumb_headline="Why can you hear your [pulse?]",
        thumb_image=STOCK / "photos"
        / "woman-holding-hands-on-her-chest" / "13419231.jpg",
        thumb_accent="red", thumb_side="left",
        thumb_crop_at=(0.5, 0.30), thumb_crop_zoom=1.0,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
