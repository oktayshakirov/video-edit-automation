"""How long does tinnitus last after a concert - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tinnitus-after-a-concert.mdx.

**Why this post.** "How long does ringing last after a concert" is the post's
own first FAQ and a query people type at 1am on the way home from a gig. The
honest answer is reassuring and specific - usually hours, almost always under
three days - and the post carries two tables (protection by dB, temporary vs
persistent) and a red-flag list, so it has figures to draw rather than film.

**The subject is invisible, so it is drawn.** Six drawn graphics in ~30 shots,
chosen before the script and no two sharing an outline:

- `gauge` - 100 dB against its 15-minute safe limit, the article's own figure.
- `diagram` (no loop) - tired hair cells, less detail, the brain raising its
  gain, the ring. The mechanism is a chain, not a cycle, so no return arrow.
- `dial` with `value=None` - the recovery clock as three named bands. No
  needle: a needle parked on a band is a claim about the viewer's ears.
- `compare` with `name_columns` - what to do / what to hold off on.
- `grid` - the four red flags, each card saying same day or this week.
- `bars` - how many dB foam, earmuffs and musician plugs take off.

The clips that remain are the act: a crowd with phones up, hands on a sound
desk's faders, somebody walking home, somebody in bed on a phone. No ear
close-ups, and no clip of somebody holding their head.

**The medical line.** Nothing promises the ringing will stop. The script says
what the article says - usually temporary, usually within three days - and
routes to a professional twice, with the red flags on screen. No initialisms
are spoken ("temporary threshold shift" is said in full).

**Footage.** The concert roster is unused anywhere else on the channel
(checked against every project file). The earplug stock fetched for the
protection section was all mislabelled - a balloon, a car dashboard, a match -
so protection is drawn as `bars` and the one photograph is a pair of earmuffs.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tinnitus-after-a-concert.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "tinnitus-after-a-concert"

# Contact-sheeted at three points across each clip; luma range in the comment.
PHONES_UP = STOCK / "videos/concert-crowd-stage-lights-dark/12719510.mp4"     # 9s, phones at a stage
PHONE_REC = STOCK / "videos/concert-crowd-stage-lights-dark/12695730.mp4"     # 8s, one phone filming, blue
GIG_PURPLE = STOCK / "videos/crowd-cheering-hands-raised-night/37944732.mp4"  # 11s, faces lit purple
GIG_SMALL = STOCK / "videos/live-music-gig-audience-dark/852304.mp4"          # 17s, silhouettes at a small gig
CROWD_PINK = STOCK / "videos/concert-crowd-night-stage-lights/9481013.mp4"    # 16s, silhouettes, pink screen
HANDS_BLUE = STOCK / "videos/music-festival-crowd-silhouette-dark/7722221.mp4"  # 9s, hands up, blue beams
HANDS_STAGE = STOCK / "videos/crowd-hands-raised-concert-silhouette-dark/34594434.mp4"  # 8s
ARENA_RED = STOCK / "videos/arena-concert-audience-wide-dark/29361041.mp4"    # 7s, red-lit arena
CLUB = STOCK / "videos/music-festival-crowd-silhouette-dark/9429656.mp4"     # 28s, dark club floor
AMP = STOCK / "videos/concert-speaker-stack-stage/8513956.mp4"               # 18s, guitarist and amp stack
STAGE_FOG = STOCK / "videos/loudspeakers-concert-dark/3792295.mp4"           # 34s, dim foggy stage
FADERS = STOCK / "videos/sound-engineer-mixing-desk-concert/7586162.mp4"     # 11s, hands on a desk's faders
MIXER = STOCK / "videos/hand-adjusting-phone-volume-dark/12213086.mp4"       # 8s, hand on a mixing desk
WALK_HOME = STOCK / "videos/walking-home-after-concert-night-street/11790102.mp4"  # 11s, amber fog street
WALK_ALONE = STOCK / "videos/man-walking-alone-night-street-dark/11792115.mp4"     # 22s, figure in fog
PHONE_HANDS = STOCK / "videos/hand-holding-phone-booking-appointment-at-night-dark/8102793.mp4"  # 23s, screen indistinct
QUIET_BED = STOCK / "videos/bedroom-fan-night/11956221.mp4"                  # 10s, empty dark bedroom
BED_PHONE = STOCK / "videos/woman-lying-in-bed-at-night-cant-sleep-dark/7986744.mp4"  # 11s, face lit by a phone
EXHALE = STOCK / "videos/person-exhaling-relief-night-dark-room/38917906.mp4"  # 25s, slow breath out
SITTING = STOCK / "videos/ringing-ears-after-concert/30815457.mp4"           # 21s, dark profile, still
EARMUFFS = STOCK / "photos/earplugs/5202427.jpg"                             # 6720px, L61, red earmuffs
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

THUMB_PHOTO = (STOCK / "photos/concert-crowd-silhouette-stage-lights-dark"
               / "17905270.jpg")   # one silhouette among phone lights, L32

VOICE = "mia"                       # same reader as the Short. Candidate.
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/tinnitus-after-a-concert"

# Recovery clock: peach for the common case, amber, then the brand's negative.
BANDS = [("Hours to a day", 0.45, "#ffdab9"),
         ("1 to 3 days", 0.75, "#f2b36b"),
         ("Past a week", 1.00, "#e87878")]


SECTIONS = [
    # --- hook: the answer first, tinnitus-after-a-concert named in line one --
    Section(
        title="Ringing after a concert",
        card=False,
        sentences=[
            ("Ringing ears after a concert usually fade within three days.",),
            ("For most people, it is gone in a few hours.",),
            ("It is still worth taking seriously,",
             "because that ringing is your ears saying the show was louder "
             "than they could handle."),
            ("By the end, you will know how long yours should last,",
             "what actually helps in the first seventy-two hours,",
             "and the signs that mean do not wait."),
        ],
        shots=[
            Shot(clip=PHONES_UP),
            Shot(clip=GIG_PURPLE),
            Shot(clip=GIG_SMALL),
            Shot(clip=CROWD_PINK),
        ],
        # 0.85 before the turn in sentence three - it contradicts the calm of
        # the two lines before it and needs the silence to turn into.
        gaps=[0.55, 0.85, 0.60, 0.85],
    ),

    # --- the mechanism: gauge, then diagram ------------------------------
    Section(
        title="Why do your ears ring after a show?",
        spoken_title="So why do your ears ring after a show at all?",
        sentences=[
            ("A loud show runs at ninety-five to a hundred and ten decibels.",),
            # gauge - the limit first, the value second.
            ("At a hundred decibels, the safe limit can be as short as "
             "fifteen minutes.",
             "And a full show runs for hours."),
            ("So what does that much sound actually do?",),
            # diagram - one caption chunk per node.
            ("The tiny hair cells in your inner ear get worn out.",
             "So less detail reaches your brain.",
             "Your brain turns up its own volume to make up for it,",
             "and that extra gain is the ringing you hear."),
            ("It even has a name, a temporary threshold shift,",
             "and temporary is the word that matters."),
        ],
        shots=[
            Shot(clip=HANDS_BLUE, note=("95-110 dB", "a typical loud show")),
            Shot(graphic="gauge",
                 payload=("HOURS", 0.92, "a full show", 0.14,
                          "15 min at 100 dB",
                          "HOW LONG IS SAFE AT 100 dB?")),
            Shot(clip=HANDS_STAGE),
            Shot(graphic="diagram",
                 payload=([("Hair cells tire out", "after hours of loud sound",
                            "\U0001F50A"),
                           ("Less detail gets through",
                            "sounds feel muffled", "\U0001F32B️"),
                           ("Your brain turns up the gain", "to fill the gap",
                            "\U0001F9E0"),
                           ("You hear the ringing", "your own neural noise",
                            "\U0001F514")],
                          "WHY YOUR EARS RING", False)),
            Shot(clip=ARENA_RED),
        ],
        gaps=[0.55, 0.85, 0.70, 0.85, 0.85],
    ),

    # --- the recovery clock: dial ---------------------------------------
    Section(
        title="How long does the ringing last?",
        spoken_title="So how long does the ringing actually last?",
        sentences=[
            # dial, value=None - one reveal, so one chunk.
            ("Most cases settle within a few hours to a day, some take up to "
             "three days, and past a week is the point to get it checked.",),
            ("A muffled, stuffed-up feeling often comes with it,",
             "and it usually fades on the same clock."),
            ("If either one is still there after a week,",
             "book a hearing test."),
        ],
        shots=[
            Shot(graphic="dial",
                 payload=(BANDS, None, "", "HOW LONG IT USUALLY LASTS")),
            Shot(clip=WALK_HOME),
            Shot(clip=PHONE_HANDS),
        ],
        gaps=[0.85, 0.55, 0.85],
    ),

    # --- the first 72 hours: compare, then the silence twist -------------
    Section(
        title="What helps in the first 72 hours?",
        spoken_title="So what actually helps in the first seventy-two hours?",
        sentences=[
            # compare, name_columns - 8 chunks for 3 + 3, heading first.
            ("Start with what helps.",
             "Give your ears a few quiet days.",
             "Keep soft sound in the background.",
             "Sleep, and drink water as normal.",
             "Now, what to hold off on.",
             "Another loud venue.",
             "Turning headphones up to drown it out.",
             "And sitting in total silence."),
            ("That last one surprises people.",),
            ("In silence, there is nothing for the ringing to hide behind,",
             "so it stands out more."),
            ("So keep the sound soft,",
             "just below the ringing, so you can still faintly hear it."),
            ("And try not to spend the night reading forums about it.",),
            ("If you feel anxious, slow your breathing for a few minutes.",
             "A calmer body tends to notice the ringing less."),
        ],
        shots=[
            Shot(graphic="compare",
                 payload=("Do this",
                          ["A few quiet days",
                           "Soft background sound",
                           "Sleep and water, as normal"],
                          "Hold off on",
                          ["Another loud venue",
                           "Headphones turned up",
                           "Total silence"],
                          True)),
            Shot(clip=QUIET_BED),
            None,   # the empty room holds through the reason
            Shot(clip=FADERS),
            Shot(clip=BED_PHONE),
            Shot(clip=EXHALE),
        ],
        gaps=[1.00, 0.55, 0.60, 0.70, 0.60, 0.85],
    ),

    # --- red flags: grid, on screen as the medical rule requires ----------
    Section(
        title="When should you get it checked?",
        spoken_title="But when should you get it checked?",
        sentences=[
            ("Most concert ringing settles on its own.",
             "These four signs are the exception."),
            # grid - one caption chunk per card.
            ("Sudden hearing loss.",
             "Dizziness, or the room spinning.",
             "Ear pain or discharge.",
             "Or ringing that is no better after three to seven days, "
             "or sits in one ear only."),
            ("The first three, get seen the same day.",
             "The last one, book a hearing test."),
        ],
        shots=[
            Shot(clip=WALK_ALONE),
            Shot(graphic="grid",
                 payload=([("Sudden hearing loss", "get seen the same day"),
                           ("Dizziness or spinning", "get seen the same day"),
                           ("Ear pain or discharge", "get seen the same day"),
                           ("No better in 3-7 days",
                            "or one ear only - book a hearing test")],
                          "DO NOT WAIT ON THESE")),
            Shot(clip=SITTING),
        ],
        gaps=[0.70, 0.90, 0.85],
    ),

    # --- protection next time: bars ---------------------------------------
    Section(
        title="How do you protect your ears next time?",
        spoken_title="So how do you protect your ears at the next show, "
                     "without losing the music?",
        sentences=[
            # bars - one caption chunk per row. Fractions are each row's upper
            # figure over 33 dB, times 0.85 so the top value text stays in
            # frame; one factor keeps the proportions exact.
            ("Foam plugs cut about twenty to thirty-three decibels,",
             "earmuffs about twenty to thirty,",
             "and musician plugs about ten to twenty-five."),
            ("Musician plugs cut less,",
             "but they lower everything evenly, so it sounds like the same "
             "mix, just quieter."),
            ("Earmuffs are the easiest on and off, which is why they suit "
             "festivals.",),
            ("Stand away from the speaker stacks, because even a few metres "
             "matter.",),
            ("And take quiet breaks between sets.",
             "Your ears recover across the night."),
        ],
        shots=[
            Shot(graphic="bars",
                 payload=([("Foam plugs", 0.85, "20-33 dB"),
                           ("Earmuffs", 0.77, "20-30 dB"),
                           ("Musician plugs", 0.64, "10-25 dB")],
                          "HOW MUCH THEY CUT")),
            Shot(clip=CLUB, clip_at=2.0),
            Shot(image=EARMUFFS, zoom=1.08, pan=(0.02, 0.0), aspect=16 / 9),
            Shot(clip=AMP, clip_at=1.0),
            Shot(clip=STAGE_FOG, clip_at=14.0),
        ],
        gaps=[0.85, 0.60, 0.55, 0.55, 0.85],
    ),

    # --- close: echo the opening, then the question -----------------------
    Section(
        title="So your ears are ringing tonight",
        sentences=[
            ("It is usually temporary,",
             "and it usually fades within three days."),
            ("Give your ears quiet, keep soft sound around you, "
             "and let them recover.",),
            ("And if any of those four signs show up,",
             "do not wait it out."),
            ("The ringing is the warning.",
             "So at the next show,",
             "will you bring earplugs?"),
        ],
        shots=[
            Shot(clip=PHONE_REC),
            Shot(clip=MIXER),
            Shot(clip=GIG_SMALL, clip_at=8.0),
            Shot(clip=CROWD_PINK, clip_at=7.0),
        ],
        gaps=[0.60, 0.80, 0.90, 3.00],
    ),
]

META = Meta(
    title="How Long Does Tinnitus Last After a Concert?",
    hook="Ears ringing after a concert? For most people it fades within "
         "hours, and almost always within three days. Here is why a loud "
         "show makes your ears ring, what helps in the first 72 hours, the "
         "signs that mean do not wait, and how to protect your ears next "
         "time.",
    url=URL,
    summary="Why concerts at 95 to 110 dB leave your ears ringing - tired "
            "hair cells and the brain turning up its own gain - how long a "
            "temporary threshold shift usually lasts, what to do and avoid "
            "in the first 72 hours, the red flags that need a same-day "
            "visit or a hearing test, and how much foam plugs, earmuffs and "
            "musician earplugs actually cut.",
    tags=["tinnitus after concert", "ears ringing after concert",
          "how long does ringing in ears last after a concert",
          "tinnitus", "ringing in ears", "concert hearing damage",
          "musician earplugs", "temporary threshold shift"],
    cta=f"Full article and sources: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. If you "
             "have sudden hearing loss, dizziness, ear pain or discharge, "
             "get seen the same day. If the ringing or muffled hearing has "
             "not improved after three to seven days, or is in one ear only, "
             "see an audiologist or doctor."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-after-a-concert-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-after-a-concert-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # The animated lower third, on the promise line rather than frame one.
        title_at=8.5, title_hold=5.4,
        # Same source and headline as the Short. The photo has no face to
        # fight - one silhouette in a field of phone lights, with black above
        # for the type.
        thumb_headline="Ears ringing after a [concert?]",
        thumb_image=THUMB_PHOTO, thumb_accent="red",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
