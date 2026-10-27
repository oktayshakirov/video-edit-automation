"""How to manage a tinnitus spike - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/why-does-tinnitus-spike.mdx - the same
article as the 2026-08-28 `why-does-tinnitus-spike` pair, **re-angled**.

**Why a second pair from one article (2026-10-27, E11).** The first pair
was built around *why* spikes happen and took 26 views. The
`youtube-audit outliers "tinnitus spikes"` search on 10-25 found five
channels standing out on *what to do during one* (Treble Health 5.8x its
median, Still Tinnitus 3.9x, Alice Moyle 7x, Caris Lount 3.5x, Julian Cowan
Hill 44x), while every "explained", "prevent" and "why" video on the same
page sat under 1x. Same subject, different promise. The teardown is
`docs/video/demand/teardowns/manage-a-tinnitus-spike.md`; this script takes
its shape (the promise in sentence one, the core idea by ~15s, reassurance
early, a short list where every step has a reason, red flags, an end that
offers the next useful thing) and none of its words.

**The title is the search.** "How to manage a tinnitus spike" is the exact
phrase three of those channels rank on, so the opener is `Search` typing it.
The Short takes "what to do during a tinnitus spike". "Manage" means what to
do and how to get through it - never a promise that the volume drops.

**The spine.** The two things most people do (a quiet room, a close listen)
are the two that make the brain listen harder; a spike is the brain on
alert; so every step calms the alert, not the sound. Then the first ten
minutes, how loud the sound should be, the rest of the day and the night,
the log that finds where a spike came from, the red flags, and the echo:
do the opposite of what most people do.

**The beats.** The last three tinnitus long forms ran post/checklist/bars/
diagram/spotlight (Beethoven), timeline/diagram/grid/quote (history) and
dial/bars/diagram (stress). The old spike pair used `steps` for the same
five actions, so here:

- `diagram(loop=True)` - alert, gain, listening harder, back to alert. The
  article's mechanism, and a loop is the one thing a list cannot draw.
- `reel` - the five steps as a strip of real acts, one card per sentence.
- `dial`, needle on - how loud the sound should be: between silence and
  drowning it out, just below the ringing. A needle is a claim, and this
  one is the article's own rule (`beats.md`, "dial").
- `grid` - what to write in the log.
- the notice card for the red flags.

**The medical line.** Nothing here says a step lowers the ringing. Each
step is described by what the article says it does - calms the nervous
system, stops the monitoring - and the red flags are the article's own,
on the notice card as they are said. "Ear specialist" and initialisms are
never spoken.

**Footage.** Fetched fresh on 2026-10-27, none cut by another project, each
contact-sheeted at 15/50/85% (verdicts in `docs/video/footage.md`). The
subject cannot be photographed, so the clips are the acts: a lamp going off,
headphones going on, a hand on faders, breathing, a notebook, water.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/how-to-manage-a-tinnitus-spike.py
    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/how-to-manage-a-tinnitus-spike.py --thumb
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "why-does-tinnitus-spike"
DEMAND = ("re-angle: 'how to manage a tinnitus spike' stands out on 5 channels "
          "(Treble Health 5.8x, Still Tinnitus 3.9x, Alice Moyle 7.0x); "
          "teardowns/manage-a-tinnitus-spike.md")

ROOT = Path(__file__).resolve().parents[2]
V = STOCK / "videos"
# Duration, luma, what is in the frame. All fetched 2026-10-27.
SITTER = V / "person-sitting-still-in-quiet-dark-room/8860237.mp4"     # 30s, L50, an old man in a dark bedroom by a window
LAMP = V / "turning-off-lamp-bedroom-night/8810535.mp4"                # 13s, L42, from above: a woman in bed reaches for the lamp
SPEAKER = V / "bluetooth-speaker-on-table-dark/29594574.mp4"           # 11s, L32, a speaker cone, close
FADERS = V / "audio-equalizer-lights-dark/7087627.mp4"                 # 9s, L51, a hand on a mixing desk's faders
BREATHE_W = V / "woman-breathing-slowly-eyes-closed-dark-room/5114850.mp4"  # 8s, L48, a woman, head back, eyes closed
PHONES = V / "putting-on-headphones-dark-room/6890229.mp4"             # 38s, L54, headphones picked up and put on, a fire behind
JAW = V / "woman-touching-jaw-tension/4862833.mp4"                     # 29s, L35, a woman, hands to her face and jaw, black ground
WALK = V / "walking-alone-street-at-night-calm/6449986.mp4"            # 29s, L24, a figure walking past city bokeh
PEN = V / "hand-writing-in-journal-dark-moody/7612023.mp4"             # 38s, L32, a hand writing in a small notebook
PEN2 = V / "hand-writing-in-journal-dark-moody/7266478.mp4"            # 29s, L55, a hand writing in an open notebook
WATER = V / "drinking-glass-of-water-close-up-dark/10631942.mp4"       # 12s, L65, a glass being filled
PHONE = V / "typing-notes-on-phone-at-night/6414098.mp4"               # 19s, L38, a phone in a hand in the dark
BEDS = V / "dim-bedroom-at-night-bed-lamp/10387631.mp4"                # 13s, L47, two beds in a blue night room
AWAKE = V / "dim-bedroom-at-night-bed-lamp/10387906.mp4"               # 26s, L46, an old woman sitting up in bed, clocks
CUP = V / "steam-rising-from-tea-cup-dark/9534789.mp4"                 # 21s, L7, a steaming cup on black
LYING = V / "woman-lying-awake-in-bed-at-night/8376628.mp4"            # 21s, L30, from above: somebody lying awake
BAR = V / "loud-bar-crowd-night/6531530.mp4"                           # 33s, L45, a crowded bar, red light
RAIN = V / "rain-on-window-night/34977302.mp4"                         # 10s, L15, rain on glass, a lit window beyond
SHOULDERS = V / "woman-massaging-her-own-shoulders/5978076.mp4"       # 16s, L75, hands easing a woman's shoulders
SOFA = V / "woman-relaxing-on-sofa-evening-lamp/6264055.mp4"           # 28s, L75, a woman reading on a sofa
SCREEN = V / "white-noise-machine-bedside-night/7988262.mp4"           # 16s, L29, a man in bed lit by his phone
LAKE = V / "calm-lake-at-dusk-slow/5911037.mp4"                        # 25s, L57, still water and reeds at dusk
DAWN = V / "calm-lake-at-dusk-slow/27671875.mp4"                       # 9s, L40, a lake at first light, a tree in silhouette
CURTAIN = V / "dawn-light-through-window-curtains/15671645.mp4"       # 27s, L11, a woman draws a curtain on daylight
SITTING = V / "man-meditating-eyes-closed-dark-room/6447702.mp4"       # 14s, L42, a man seated, eyes closed, breathing
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"          # the noah test, pair 2 of 5 (`projects/tinnitus.md`)
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/why-does-tinnitus-spike"

BANDS = [("Silence", 0.25, "#ffdab9"),
         ("Just under it", 0.65, "#f4a261"),
         ("Drowning it out", 1.00, "#e76f51")]

# Thumbnail - the video's own question, never its answer. The plate is on
# the word that tells a sufferer the video is for them. The user's pick
# (2026-10-27): Pexels 5908779, a woman in headphones at a laptop, fingers
# to her temples (Kaboompics) - one source for both aspects.
THUMB_HEADLINE = "Tinnitus\n[spike?]\nDo this\nfirst"
THUMB_PHOTO = STOCK / "photos/user-pick-woman-laptop/5908779.jpg"


SECTIONS = [
    # --- hook ---------------------------------------------------------------
    Section(
        title="How do you manage a tinnitus spike?",
        card=False,
        sentences=[
            # The Search opener types this as it is said.
            ("How do you manage a tinnitus spike?",),
            # The reversal: what most people do is the problem.
            ("Most people do two things that make the brain listen harder: "
             "they find a quiet room, and they check on the ringing.",),
            # The core idea, by ~15s.
            ("A spike is your brain on alert, turning up the volume on its "
             "own signals.",),
            ("So every step here does one job: it tells your brain there is "
             "no threat.",),
            # The promise - paid off by the sections, in this order.
            ("By the end, you will have a plan for the first ten minutes, "
             "for tonight, and for knowing when a spike needs a doctor.",),
        ],
        shots=[
            Shot(clip=SITTER, clip_at=0.5),
            Shot(clip=LAMP, clip_at=0.5),
            Shot(clip=SPEAKER, clip_at=0.5),
            Shot(clip=LAKE, clip_at=1.0),
            # The title rides here.
            Shot(clip=LYING, clip_at=1.0),
        ],
        gaps=[1.00, 0.70, 0.60, 0.80, 0.90],
    ),

    # --- the fear -----------------------------------------------------------
    Section(
        title="Is a spike new damage?",
        spoken_title="First, is a spike new damage?",
        kicker="THE FEAR",
        sentences=[
            ("A spike is a short-term rise in how loud, how sharp, or how "
             "intrusive your tinnitus feels.",),
            ("It can follow a trigger by hours, or even a day, so it often "
             "seems to come from nowhere.",),
            ("Most spikes settle within hours to a few days.",),
            ("After a bigger trigger, like a loud concert or an illness, some "
             "last one to three weeks.",),
            ("But a spike is usually reversible. It does not automatically "
             "mean new damage.",),
        ],
        shots=[
            Shot(clip=AWAKE, clip_at=1.0),
            Shot(clip=BAR, clip_at=3.0),
            Shot(clip=RAIN, clip_at=0.5,
                 note=("Hours to days", "how long most spikes last")),
            Shot(clip=BEDS, clip_at=0.5),
            Shot(clip=CURTAIN, clip_at=8.0),
        ],
        gaps=[0.55, 0.70, 0.80, 0.80, 0.90],
    ),

    # --- the alarm ----------------------------------------------------------
    Section(
        title="Why does it get louder?",
        spoken_title="So why does it get louder at all?",
        kicker="THE ALARM",
        sentences=[
            ("Think of a spike as a stress response, inside your hearing.",),
            # diagram, loop=True - one chunk per node; the third closes it.
            ("Something puts your brain on alert: stress, a loud evening, a "
             "short night.",
             "On alert, it turns up the gain on every signal, the ringing "
             "included.",
             "So you notice it, and listen harder, which keeps the alert "
             "going."),
            ("So the steps do not fight the sound. They calm the alert "
             "underneath it.",),
        ],
        shots=[
            # From 15s: a hand at her jaw. Before it she drags her face down,
            # which reads as anguish under a line about a stress response.
            Shot(clip=JAW, clip_at=15.0),
            Shot(graphic="diagram",
                 payload=([("On alert", "stress, noise, a short night",
                            "\U0001F6A8"),
                           ("The gain goes up", "the ringing stands out",
                            "\U0001F50A"),
                           ("You listen harder", "and check on it",
                            "\U0001F50D")],
                          "THE LOOP BEHIND A SPIKE", True)),
            Shot(clip=SITTING, clip_at=1.0),
        ],
        gaps=[0.70, 1.20, 0.90],
    ),

    # --- the first ten minutes ----------------------------------------------
    Section(
        title="What do you do in the first ten minutes?",
        spoken_title="So what do you do in the first ten minutes?",
        kicker="TEN MINUTES",
        sentences=[
            ("Five steps, and each one has a reason.",),
            # reel - one card per sentence, held with None.
            ("One. Name it a flare-up, not a setback, because fear is one "
             "more alarm.",),
            ("Two. Breathe in for four, and out for six to eight, for a few "
             "minutes.",),
            ("Three. Put on a gentle sound, because silence gives your brain "
             "a reason to listen harder.",),
            ("Four. Drop your shoulders and unclench your jaw, because tension "
             "there can feed the volume.",),
            ("Five. Do something absorbing, a walk or a book, so you stop "
             "checking on it.",),
            ("How loud should that sound be?",),
            # dial - scale first, then the needle.
            ("Somewhere between silence and drowning it out.",
             "Just below your tinnitus, or level with it."),
            ("Enough to blend with the ringing, never so loud it hides the "
             "world.",),
        ],
        shots=[
            Shot(clip=DAWN, clip_at=0.5),
            Shot(graphic="reel",
                 payload=([(None, "NAME IT"),
                           (BREATHE_W, "BREATHE OUT LONGER"),
                           (PHONES, "A GENTLE SOUND", 8.0),
                           (SHOULDERS, "SHOULDERS DOWN"),
                           (SOFA, "SOMETHING ELSE")],
                          "THE FIRST TEN MINUTES")),
            None,
            None,
            None,
            None,
            Shot(clip=FADERS, clip_at=0.5),
            Shot(graphic="dial",
                 # top=0: the scale is the viewer's own ringing, so no
                 # numerals and no figure - only where the needle sits.
                 payload=(BANDS, 0.45, "just below the ringing",
                          "HOW LOUD SHOULD THE SOUND BE?", 0)),
            Shot(clip=WALK, clip_at=2.0),
        ],
        gaps=[0.80, 0.70, 0.70, 0.70, 0.70, 0.90, 0.80, 1.20, 0.90],
    ),

    # --- the rest of the day ------------------------------------------------
    Section(
        title="What about tonight?",
        spoken_title="And what about tonight?",
        kicker="TONIGHT",
        sentences=[
            ("Drink some water, and go easy on salt today.",),
            ("Hold off on extra coffee, if you are sensitive to it.",),
            ("Tonight, protect your sleep: the same bedtime, dim lights, and "
             "screens out of bed.",),
            ("And a gentle sound in the room, instead of silence.",),
            ("A short night lowers your resilience, and the next day the "
             "ringing can feel louder.",),
        ],
        shots=[
            Shot(clip=WATER, clip_at=1.0),
            Shot(clip=CUP, clip_at=2.0),
            Shot(clip=SCREEN, clip_at=2.0),
            Shot(clip=LAKE, clip_at=12.0),
            Shot(clip=LYING, clip_at=12.0),
        ],
        gaps=[0.55, 0.70, 0.60, 0.80, 0.90],
    ),

    # --- the pattern --------------------------------------------------------
    Section(
        title="Where did this one come from?",
        spoken_title="So where did this one actually come from?",
        kicker="THE PATTERN",
        sentences=[
            ("While it is fresh, write a short note.",),
            # grid - one chunk per card.
            ("How you slept,", "your stress, out of ten,", "any loud noise,",
             "and how much caffeine."),
            ("Do it for two to four weeks, and a pattern often shows up.",),
            ("A spike on Tuesday can turn out to have started with a short "
             "night on Sunday.",),
            ("And a spike you can trace is far less frightening.",),
        ],
        shots=[
            Shot(clip=PEN, clip_at=2.0),
            Shot(graphic="grid",
                 payload=([("Sleep", "how many hours", "\U0001F634"),
                           ("Stress", "out of ten", "\U0001F4CA"),
                           ("Noise", "anything loud", "\U0001F50A"),
                           ("Caffeine", "how many cups", "☕")],
                          "WHAT TO WRITE DOWN")),
            Shot(clip=PEN2, clip_at=3.0),
            Shot(clip=AWAKE, clip_at=14.0),
            Shot(clip=CURTAIN, clip_at=16.0),
        ],
        gaps=[0.60, 1.10, 0.70, 0.80, 0.90],
    ),

    # --- the red flags ------------------------------------------------------
    Section(
        title="When is it more than a spike?",
        spoken_title="But when is it more than a spike?",
        kicker="THE RED FLAGS",
        sentences=[
            ("Most spikes are harmless. A few signs need a doctor within a "
             "day or two.",),
            # The article's urgent list, on the notice card as it is said.
            ("A sudden drop in hearing, a new sound that pulses with your "
             "heartbeat, severe ear pain, discharge, or a fever.",),
            ("And book a check if it stays in one ear, gets worse over weeks, "
             "or the worry is wearing you down.",),
        ],
        shots=[
            Shot(clip=PHONE, clip_at=1.0),
            Shot(clip=RAIN, clip_at=0.5,
                 payload=("NOTICE", "Sudden hearing loss, a pulsing sound, "
                                    "pain or fever? See a doctor soon.")),
            Shot(clip=SITTER, clip_at=14.0),
        ],
        gaps=[0.80, 0.90, 0.90],
    ),

    # --- close: echo the opening, then the question -------------------------
    Section(
        title="So the next time it spikes",
        spoken_title="So, the next time it spikes.",
        kicker="THE ECHO",
        sentences=[
            ("Do the opposite of what most people do.",),
            ("Not a silent room and a close listen, but a gentle sound, a "
             "long breath out, and your shoulders down.",),
            ("It is a flare-up, and flare-ups usually settle.",),
            ("Which of the five will you try first?",),
        ],
        shots=[
            Shot(clip=LAMP, clip_at=3.0),
            Shot(clip=SITTING, clip_at=6.0),
            Shot(clip=WALK, clip_at=14.0),
            Shot(clip=BEDS, clip_at=4.0),
        ],
        gaps=[0.70, 0.90, 0.90, 3.00],
    ),
]

META = Meta(
    title="How to Manage a Tinnitus Spike",
    hook="A tinnitus spike is your brain on alert, turning up the volume on "
         "its own signals. Here is what to do in the first ten minutes, how "
         "loud a background sound should be, what to do tonight, how to find "
         "where a spike came from, and which signs mean you should see a "
         "doctor.",
    url=URL,
    summary="What a tinnitus spike is and how long most last, why the brain "
            "turns the volume up, five steps for the first ten minutes "
            "(name it, slow breathing, gentle sound instead of silence, "
            "shoulders and jaw, something absorbing), how loud the sound "
            "should be, the rest of the day and the night, a simple log, "
            "and the red flags.\n\n"
            "Gentle sounds to play during a spike, free: "
            "https://tinnitushelp.me/zen",
    tags=["how to manage a tinnitus spike", "tinnitus spike",
          "what to do during a tinnitus spike", "tinnitus spikes",
          "tinnitus flare up", "tinnitus suddenly louder",
          "tinnitus spike relief sounds", "tinnitus and stress",
          "tinnitus", "ringing in ears"],
    cta=f"The full article, with a trigger-by-trigger table and every red "
        f"flag: {URL}",
    credits=["This video is general information, not medical advice. If you "
             "have a sudden drop in hearing, a new sound that pulses with "
             "your heartbeat, severe ear pain, discharge or a fever, please "
             "see a doctor promptly."],
)


def thumbs(out: Path) -> Path:
    """Scaled 1.15x and anchored left so she sits right, face and hands
    whole; four rows in dark ink on the light room, ending clear of her
    raised hand. The left side is blurred and lifted a little so the black
    type reads, easing back to sharp before her hand (the user's note on the
    first cover: hard to read on the busy shelves)."""
    import numpy as np
    from PIL import Image, ImageFilter
    from video_automation.longform import thumb as T
    src = Image.open(THUMB_PHOTO).convert("RGB")
    w = int(1280 * 1.15)
    h = int(src.height * w / src.width)
    src = src.resize((w, h), Image.LANCZOS)
    y0 = int((h - 720) * 0.25)
    im = src.crop((0, y0, 1280, y0 + 720))
    soft = Image.blend(im.filter(ImageFilter.GaussianBlur(22)),
                       Image.new("RGB", im.size, (245, 245, 245)), 0.15)
    # Full blur to x=520, smoothstepped back to sharp by x=760.
    t = np.clip((760 - np.arange(1280, dtype=np.float32)) / 240, 0, 1)
    t = t * t * (3 - 2 * t)
    mask = Image.fromarray((np.tile(t, (720, 1)) * 255).astype(np.uint8), "L")
    im = Image.composite(soft, im, mask)
    fill, ink = T.ACCENTS["red"]
    # 460, not wider: rows with their own breaks widen the column by 1.38x,
    # and anything past ~640px runs into her hand.
    T._headline(im, THUMB_HEADLINE, 220, 460, 40, fill, ink, max_lines=4,
                leading=1.02, band="middle", margin=36, shadow=11,
                drop=(5, 6), text=(20, 20, 20))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/how-to-manage-a-tinnitus-spike-long.mp4"
    work = Path.home() / "Desktop/.how-to-manage-a-tinnitus-spike-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # On the promise (~18s); its hold ends at 23.4, clear of the first
        # card at 0:25.
        title_at=18.0, title_hold=5.4,
        # The long form's title is the search, so the opener types it.
        opener=Search("how to manage a tinnitus spike"),
        emphasis=["listen harder", "reversible", "Tuesday"],
        thumb_headline=THUMB_HEADLINE, thumb_image=THUMB_PHOTO,
        thumb_accent="red",
    )
    # `render_long`'s own thumbnail is replaced by the hand-built one.
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home()
                     / "Desktop/how-to-manage-a-tinnitus-spike-long-thumb.jpg"))
    else:
        main()
