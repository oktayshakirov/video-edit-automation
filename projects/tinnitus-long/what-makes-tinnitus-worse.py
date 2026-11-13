"""What makes tinnitus worse? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tinnitus-trigger-tracking.mdx - why
memory picks the wrong culprit (recall bias, reverse causation, regression
to the mean), which suspects the evidence backs, and how a four-week diary
finds your own.

**The angle** (`demand/teardowns/what-makes-tinnitus-worse.md`): Doctor
Cliff's "5 Things That are Making your Tinnitus LOUDER" (1.5M, 138x),
Treble's "Tinnitus Getting Worse? STOP These 7 Mistakes" (202k, ~19x),
Timpanogos "Are You Making Tinnitus WORSE Without Realizing it?!" (~9x).
A counted list wins; one named cause loses. Theirs presents the list as
settled, and its comments say "everything under the sun causes it". Ours
sorts the list - two suspects hold up, two do not, three are not for home
testing - and shows why everyone's own list is unreliable.

**Title is the search** (`longform.md`): "What Makes Tinnitus Worse?" The
Short takes the other angle, a named suspect ("Coffee, wine, salt...").

**Three chapters, 2:30-3:00 (E18)**: the memory trap, the evidence, the
four-week diary; then the echo.

## The picture, written first (`workflow.md`, 2026-11-12)

Last three tinnitus long forms: tinnitus-in-one-ear (compare / checklist /
dial / steps / audiogram / behind), is-tinnitus-in-the-ear-or-the-brain
(reel / dial / diagram), what-does-tinnitus-sound-like (spectrum / diagram /
grid). So no `reel`, `behind` or `post` (signature beats resting), no
`dial`.

| sentence | on screen | tool |
| --- | --- | --- |
| everyone blames something | coffee poured into a dark mug; the quote enters on "blames", right of the mug, UNTESTED on "tested" | clip + `Stamp` |
| the suspects | coffee, wine, salt, a late night | `grid` |
| some hold up | a crowd under red stage light | clip |
| some never shown a link | salt pouring onto black, in a player frame | clip `window=` |
| by the end you will know | why memory lies / what holds up / how to test yours | `steps`, ruled ground |
| it moves on its own | a woman sitting up awake on her bed | clip |
| the month | 28 squares, wine glasses on the wine days, rings in turn | `diary` |
| it runs backwards | an alarm clock in the dark, the cut glitched | clip `aberration` |
| louder day, on edge, less sleep | the loop | `diagram(loop=True)`, ruled ground |
| the worst day gets the credit | a line, its peak marked | `chart`, ruled ground |
| which hold up | sleep, stress yes; caffeine, salt no | `checklist` note card |
| alcohol | a glass filled on black | clip |
| jaw or head | clench your jaw / turn your head / tell a clinician | `grid`, ruled ground |
| loud noise | the crowd again, later in the clip | clip |
| a new medicine | pills, in our ototoxic page's browser window | clip `window=` |
| keep a diary | a notebook on a dark desk, ringed | `spotlight` |
| what to write | the site's own journaling photo, labelled | `callout` |
| an example month | loudness flat, bother halving | `bars`, ruled ground |
| the bother is the part treatments work on | the woman at the window, in depth | photo `parallax` |
| how to read it | three steps, held | `steps`, ruled ground |
| then stop | the window photo, the figure ringed | `spotlight` |
| the echo / the question | the coffee; the suspects again | clip, `grid` |

Chapter cards are the dark ruled `grid` card.

**Drawn or framed: well over half** (`script_check`'s `drawn-share`).

**No medical claims** (`projects/tinnitus.md`): nothing says cutting a
trigger quietens anything; the verbs are the article's - test, log, ask.
Medication is "ask your prescriber", never "stop". The jaw line is "tell a
clinician", not a promise it is treatable. The diary and the bars are both
titled as examples.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/what-makes-tinnitus-worse.py
    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/what-makes-tinnitus-worse.py --thumb
"""

import sys
from pathlib import Path

from video_automation.core import music, stillclip
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Stamp

SOURCE_POST = "tinnitus-trigger-tracking"
DEMAND = ("Doctor Cliff '5 Things That are Making your Tinnitus LOUDER' 1.5M "
          "(138x), Treble 'Tinnitus Getting Worse? STOP These 7 Mistakes' "
          "202k (~19x); teardowns/what-makes-tinnitus-worse.md")
COVER_STYLE = "cutout"     # picked by the editor, 2026-11-13

ROOT = Path(__file__).resolve().parents[2]
V = STOCK / "videos"
P = STOCK / "photos"
SITE = Path.home() / "Coding/tinnitus-blog/public/images"

# Fetched fresh 2026-11-13, screened with `tools/stock_sheet.py` (B = luma
# with the subject masked out) and watched to their ends; none is in
# another video.
COFFEE = V / "coffee-pouring-into-mug-dark/19157857.mp4"            # 18s, B49, coffee poured into a dark mug over beans
AWAKE = V / "insomnia-bed-night-dark/6951594.mp4"                   # 30s, B45-49, a woman sitting up awake on her bed, phone in hand
CLOCK = V / "alarm-clock-night-dark/30039319.mp4"                   # 13s, B11-21, an alarm clock in the dark
WINE = V / "pouring-red-wine-glass-dark/7686970.mp4"                # 25s, B2, a glass filled on black
LOUD = V / "concert-crowd-dark-stage-lights/39204687.mp4"           # 16s, B18-36, a crowd under red stage light
PILLS = V / "pills-in-hand-dark/5867890.mp4"                        # 26s, B55-68 - in a window, never full frame
SALT = V / "salt-shaker-sprinkling-dark-background/7152168.mp4"     # 19s, B1-13, salt pouring onto black (the stream from ~6s)
ENDCARD = V / "subscribe/4928934.mp4"

PROFILE = P / "man-profile-portrait-dark-background/19068090.jpg"    # L8, a clean profile: jaw and neck
WINDOW = P / "woman-sitting-by-window-evening-dark/13262521.jpg"     # L17, a silhouette at a red-curtained window
DESK = P / "notebook-and-pen-on-table-dark/5717627.jpg"              # a notebook and a closed laptop on a dark desk
DISCLAIMER_BG = stillclip.path(DESK, focus=(0.45, 0.40))
# Rejected 2026-11-13 on the sheet: every earplug and jaw clip (lit white,
# B88-205, and faces), both notebook-closing clips and all three writing
# clips (B86-137), the bright coffee pours, a lit clock face (855782), a
# woman asleep rather than awake (8486623).

# The site's own photograph: a girl at a table with a phone and a notebook.
JOURNAL = SITE / "journaling.jpg"

# Our own page, in the browser window under the medication line - the
# article's "check anything new against the ototoxic list" links it.
OTOTOXIC = ("browser", "tinnitushelp.me/blog/ototoxic-medications-and-tinnitus")

# The month the `diary` draws: 28 days, Monday first, loudness 0-10. Wine on
# four days - one bad, three fine - and four more bad days with none. An
# illustration of the article's recall-bias paragraph, titled as one.
MONTH = [5, 4, 6, 9, 5, 4, 5,
         3, 5, 8, 6, 4, 3, 5,
         6, 4, 5, 9, 5, 4, 6,
         5, 8, 4, 6, 5, 9, 4]
WINE_DAYS = [3, 7, 12, 19]
GROUPS = [("Remembered", "the bad night after wine", [3]),
          ("Forgotten", "four bad nights, no wine", [9, 17, 22, 26]),
          ("Forgotten", "wine before a fine night", [7, 12, 19])]

VOICE = "mia"           # the noah test closed 2026-11-12: mia for every pair
MUSIC = music.track("night-drift")
URL = "https://tinnitushelp.me/blog/tinnitus-trigger-tracking"

# The editor (2026-11-13): "its the coffee" stayed too long - it sat on
# screen from frame one to the stamp. Now the pour plays clean for the first
# line, the quote enters on "louder", the stamp lands on "tested". And it
# sits in the right half: the mug is on the left of this shot.
OPENER = Stamp("It's the coffee.", "UNTESTED", at_word="tested",
               enter_word="louder", centre_x=0.68)


def sections() -> list:
    return [
    # --- hook. No card. The stamp lands on "tested". -------------------------
    Section(
        title="What makes tinnitus worse",
        card=False,
        sentences=[
            ("Almost everyone with tinnitus blames something for the louder days.",),
            ("Almost nobody has tested it.",),
            # grid - one chunk per card.
            ("The coffee,",
             "the glass of wine,",
             "the salty dinner,",
             "the late night."),
            # Two moving shots, then the roadmap: one still photo under both
            # lines held ten seconds at 0:10, "nothing happens" (the editor,
            # 2026-11-13).
            ("Some of those hold up in the research.",),
            ("Some have never shown a link at all.",),
            # steps - one chunk per stop.
            ("By the end, you will know why memory gets it wrong,",
             "which suspects hold up,",
             "and how to test yours."),
        ],
        shots=[
            Shot(clip=COFFEE, clip_at=0.5),
            None,
            Shot(graphic="grid",
                 payload=([("Coffee", "", "☕"),
                           ("A glass of wine", "", "\U0001F377"),
                           ("A salty dinner", "", "\U0001F9C2"),
                           ("A late night", "", "\U0001F971")],
                          "THE USUAL SUSPECTS")),
            Shot(clip=LOUD, clip_at=7.0),
            Shot(clip=SALT, clip_at=6.0, window="player"),
            Shot(graphic="steps", ground="grid",
                 payload=(["Why memory lies", "What holds up",
                           "How to test yours"],
                          "IN THIS VIDEO")),
        ],
        gaps=[0.55, 0.85, 1.00, 0.45, 0.60, 0.90],
    ),

    # --- the memory trap --------------------------------------------------------
    Section(
        title="Why does memory pick the wrong culprit?",
        spoken_title="So why does your memory pick the wrong culprit?",
        kicker="THE MEMORY TRAP",
        sentences=[
            ("Tinnitus goes up and down from day to day, often for no reason anyone can find.",),
            # diary - the month, then one chunk per ringed group.
            ("Here is a month of it, one square a day.",
             "You remember the bad night after the wine.",
             "You forget the four bad nights without any.",
             "And the wine before a night that was fine."),
            ("Actually, it runs the other way too. You assume stress made it loud, when often the loud day made you stressed.",),
            # diagram, loop - one chunk per box.
            ("A louder day puts you on edge.",
             "Being on edge costs you sleep.",
             "And a short night makes the next day louder."),
            # chart - the line, then the marked peak.
            ("Then there are the worst days.",
             "Whatever you tried on one gets the credit for a drop that was coming anyway."),
        ],
        shots=[
            Shot(clip=AWAKE, clip_at=1.0),
            Shot(graphic="diary",
                 payload=(MONTH, WINE_DAYS, GROUPS, "ONE MONTH - AN EXAMPLE",
                          ("a glass of wine", "brighter = louder"),
                          "\U0001F377")),
            Shot(clip=CLOCK, clip_at=1.0, shader="aberration"),
            Shot(graphic="diagram", ground="grid",
                 payload=([("A louder day", "you listen for it", "\U0001F623"),
                           ("On edge", "stress climbs", "\U0001F630"),
                           ("Less sleep", "a shorter night", "\U0001F971")],
                          "THE LOOP", True)),
            Shot(graphic="chart", ground="grid",
                 payload=([5, 6, 5, 6, 9, 7, 5, 6, 5, 6], "DAY BY DAY", 4,
                          "you try something new")),
        ],
        gaps=[0.80, 1.40, 0.85, 1.20, 0.90],
    ),

    # --- the evidence -----------------------------------------------------------
    Section(
        title="Which triggers actually hold up?",
        spoken_title="So which triggers actually hold up?",
        kicker="THE EVIDENCE",
        sentences=[
            # the note card, flow - each chunk says its own verdict.
            ("Sleep holds up, the most consistent link of all.",
             "Stress holds up, and it is the same loop.",
             "Caffeine: population studies have not found a link.",
             "Salt mostly matters in one inner-ear condition, not tinnitus in general."),
            ("Alcohol gets blamed a lot, but it probably works through the sleep it costs you.",),
            # grid - one chunk per card. Not labels on a photo: a pointer to
            # "the jaw" on a face says nothing the word does not (the
            # editor, 2026-11-13); the check is two actions and a step.
            ("If the sound changes when you clench your jaw,",
             "or when you turn your head,",
             "tell a clinician about it."),
            ("Loud noise is one you never test. It is a real risk to your hearing, so protect your ears regardless.",),
            ("And check a new medicine against the list of drugs that can affect hearing, then ask your prescriber before stopping anything.",),
        ],
        shots=[
            Shot(graphic="checklist",
                 payload=([("Sleep", True), ("Stress", True),
                           ("Caffeine", False), ("Salt", False)],
                          "DOES IT HOLD UP?", True)),
            Shot(clip=WINE, clip_at=1.0),
            Shot(graphic="grid", ground="grid",
                 payload=([("Clench your jaw", "does the sound change?", "\U0001F62C"),
                           ("Turn your head", "does it change?", "\U0001F504"),
                           ("Tell a clinician", "if it does", "\U0001FA7A")],
                          "A TWO-SECOND CHECK")),
            Shot(clip=LOUD, clip_at=1.0),
            Shot(clip=PILLS, clip_at=1.0, window=OTOTOXIC),
        ],
        gaps=[2.00, 0.85, 1.00, 0.85, 0.90],
    ),

    # --- the four-week diary ----------------------------------------------------
    Section(
        title="How do you find your own triggers?",
        spoken_title="So how do you find your own?",
        kicker="FOUR WEEKS",
        sentences=[
            ("Keep a diary for four weeks: thirty seconds, once a day, at about the same time.",),
            # callout on the site's photo - one chunk per label.
            ("Write down how loud it was,",
             "and, separately, how much it bothered you,",
             "how long you slept,",
             "and your stress, drinks and loud noise."),
            # bars - one chunk per row.
            ("In this example month, loudness starts at six,",
             "and ends at about six.",
             "Bother starts at six too,",
             "and ends at three and a half."),
            ("Loudness barely moved. Bother almost halved, and sleep moved with it.",),
            ("That sounds like bad news. But the bother is the part most treatments work on.",),
            # steps - one chunk per stop.
            ("When the month is up, compare averages, not single bad days,",
             "look one day back,",
             "and count how often your suspect turns up on the good days too."),
            ("Most suspects come out innocent, which means you can stop giving things up for nothing.",),
            ("Then stop logging, because watching it every day keeps it in front of you.",),
        ],
        shots=[
            Shot(graphic="spotlight",
                 # Wide and shallow, and not snapped: a dark photo snaps to
                 # the whole picture, and a frame-shaped ring puts its label
                 # up against the watermark (first cut).
                 payload=(DESK, [((0.26, 0.28, 0.84, 0.50), "Thirty seconds a day")],
                          "", False)),
            Shot(graphic="callout",
                 payload=(JOURNAL, [("How loud", 0.82, 0.62),
                                    ("How bothered", 0.82, 0.80),
                                    ("Hours slept", 0.18, 0.62),
                                    ("Stress, drinks, noise", 0.18, 0.80)],
                          "ONCE A DAY")),
            Shot(graphic="bars", ground="grid",
                 payload=([("Loudness, week 1", 0.61, "6.1"),
                           ("Loudness, week 4", 0.58, "5.8"),
                           ("Bother, week 1", 0.58, "5.8"),
                           ("Bother, week 4", 0.35, "3.5")],
                          "AN EXAMPLE MONTH, OUT OF 10")),
            None,
            Shot(image=WINDOW, parallax=0.5),
            Shot(graphic="steps", ground="grid",
                 payload=(["Compare averages", "Look one day back",
                           "Check the good days"],
                          "READING THE MONTH")),
            None,
            Shot(graphic="spotlight",
                 payload=(WINDOW, [((0.22, 0.18, 0.95, 0.52), "Then stop logging")],
                          "", False)),
        ],
        gaps=[0.80, 1.30, 1.30, 0.85, 0.90, 1.20, 0.80, 0.90],
    ),

    # --- close: the echo --------------------------------------------------------
    Section(
        title="So what is making yours worse?",
        spoken_title="So, what is making yours worse?",
        kicker="THE VERDICT",
        sentences=[
            ("Maybe the thing you blame really is guilty. Give it four weeks before you convict it.",),
            ("This video is general information, not medical advice.",),
            ("So, which suspect would you put on trial first?",),
        ],
        shots=[
            Shot(clip=COFFEE, clip_at=10.0),
            Shot(clip=DISCLAIMER_BG, clip_at=0.5,
                 payload=("", "General information, not medical advice.")),
            # The suspects again, for "which suspect": a callback to the
            # hook's line-up rather than a held clip under the last line.
            Shot(graphic="grid",
                 payload=([("Coffee", "", "\u2615"),
                           ("A glass of wine", "", "\U0001F377"),
                           ("A salty dinner", "", "\U0001F9C2"),
                           ("A late night", "", "\U0001F971")],
                          "WHICH ONE GOES ON TRIAL?")),
        ],
        gaps=[1.00, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="What Makes Tinnitus Worse? The Triggers Worth Testing",
    hook="Almost everyone with tinnitus blames something for the louder days, "
         "and almost nobody has tested it. Here is why memory picks the wrong "
         "culprit, which suspects the evidence actually backs, and how a "
         "four-week diary finds your own.",
    url=URL,
    summary="What makes tinnitus worse, sorted by the evidence: why your "
            "intuition about triggers is unreliable (recall bias, reverse "
            "causation, regression to the mean); sleep and stress as the two "
            "influences that hold up, and the loop between them; caffeine, "
            "where population studies have not found a link; salt, mostly "
            "relevant to Meniere's disease; alcohol, probably through "
            "disrupted sleep; three things not to test at home (loud noise, "
            "somatic tinnitus that changes with the jaw or neck, and "
            "ototoxic medication); and how to keep a four-week tinnitus "
            "diary that rates loudness and bother separately.",
    tags=["what makes tinnitus worse", "tinnitus triggers",
          "things that make tinnitus worse", "tinnitus getting worse",
          "tinnitus diary", "does caffeine make tinnitus worse",
          "does alcohol make tinnitus worse", "tinnitus and sleep",
          "tinnitus and stress", "tinnitus louder", "tinnitus",
          "ringing in ears"],
    cta=f"The full diary template, how to read a month of it, and what the "
        f"evidence says on each trigger: {URL}",
    credits=["This video is general information, not medical advice. Talk "
             "to your prescriber before stopping any medication, and see a "
             "clinician if your tinnitus is new, one-sided, pulsing, or "
             "comes with hearing loss or dizziness."],
)

THUMB_HEADLINE = "What makes tinnitus\n[worse?]"

# --- the covers (2026-11-13) ---------------------------------------------------
#
# The editor turned down the ring-and-arrow mug: "the circle and arrow is
# being overused, its 3rd video with such thumbnail in a row, we need more
# variations to see what works. Try different approaches, view competitors".
# The top of this search (`demand/teardowns/what-makes-tinnitus-worse.md`):
# Dr. Berg 2.2M (red waves into an ear), Doctor Cliff 1.5M (a face, "YOU'RE
# MAKING YOUR TINNITUS WORSE!"), Dr. Berg 1.1M (a woman holding her ear, red
# glow). What wins is a person in discomfort, a red ringing cue and one huge
# word; the coffee-specific covers sit at 7-17k. Three directions, built for
# both formats:
#
#   "cutout" - a woman holding her head, cut out (`core.vision.cutout`), red
#              rings radiating from her head, WHAT MAKES / TINNITUS / WORSE?
#              with WORSE? as extruded red type (`thumb.extrude_text`)
#   "lineup" - a police line-up: the mug, a "?" silhouette, the glass of
#              wine against a height chart. TINNITUS: WHO'S THE [CULPRIT?]
#
# The verdict (2026-11-13): the cutout ships; the line-up is "very good
# too, keep for future videos as format" (`thumb.lineup_cover`); a third,
# the mug beside extruded NOT THE / COFFEE?, was "not that impressive" and
# is gone.
#
# The cover's pictures are none of the video's shots.
MUG = P / "coffee-cup-on-black-background/39529656.jpg"
HEAD = P / "woman-holding-ear-in-pain-dark-background/3812745.jpg"
WINE_CLIP = V / "pouring-red-wine-glass-dark/7686970.mp4"     # a frame at 22s, the glass full
COVERS = ("cutout", "lineup")


def _cut(src, *, crop_rows=None, brighten=1.0):
    """The subject of `src` (a path or an image) as RGBA, cropped to it."""
    import numpy as np
    from PIL import Image, ImageEnhance
    from video_automation.core import vision
    im = src if isinstance(src, Image.Image) else Image.open(src)
    im = im.convert("RGB")
    im.thumbnail((1800, 1800))
    if brighten != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brighten)
    a = np.asarray(vision.cutout(im)).copy()
    if crop_rows:
        a[:int(a.shape[0] * crop_rows[0]), :, 3] = 0
        a[int(a.shape[0] * crop_rows[1]):, :, 3] = 0
    c = Image.fromarray(a)
    return c.crop(c.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox())


def _wine_glass():
    import subprocess
    import tempfile
    from PIL import Image
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "w.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", "22",
                        "-i", str(WINE_CLIP), "-frames:v", "1", str(f)], check=True)
        frame = Image.open(f).convert("RGB")
        # The pour above the rim and the reflection under the foot go.
        return _cut(frame, crop_rows=(0.205, 0.92), brighten=2.2)


def _radial(size, centre, inner, outer, r):
    import numpy as np
    from PIL import Image
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    k = np.clip(np.sqrt((xx - centre[0]) ** 2 + (yy - centre[1]) ** 2) / r, 0, 1)[:, :, None]
    arr = np.array(inner, np.float32) * (1 - k) + np.array(outer, np.float32) * k
    return Image.fromarray(arr.astype(np.uint8)).convert("RGBA")


def _place(base, cut, h, x, y):
    from PIL import Image
    c = cut.resize((int(cut.width * h / cut.height), int(h)), Image.LANCZOS)
    if x is None:
        x = base.width - c.width - 30
    elif x == "centre":
        x = (base.width - c.width) // 2
    base.alpha_composite(c, (int(x), int(y)))


def _flat(im, text, size, xy, fill=(255, 255, 255)):
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
    from video_automation.longform import thumb as T
    f = ImageFont.truetype(T.FONT_DISPLAY, size)
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((xy[0] + 5, xy[1] + 7), text, font=f, fill=(0, 0, 0, 210))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    ImageDraw.Draw(im).text(xy, text, font=f, fill=fill)


def cover(kind: str, portrait: bool = False):
    """One cover, 1280x720 or (`portrait`) 1080x1920, as an RGB image."""
    from PIL import Image, ImageDraw, ImageFont
    from video_automation.longform import thumb as T
    W, H = (1080, 1920) if portrait else (1280, 720)
    red = (255, 62, 48)
    if kind == "cutout":
        head = _cut(HEAD)
        if portrait:
            im = _radial((W, H), (560, 1180), (110, 14, 20), (8, 4, 7), 1100)
            im.alpha_composite(T.sound_rings((W, H), (560, 1100), (255, 70, 50),
                               radii=(230, 330, 440, 560), width=12))
            _flat(im, "WHAT MAKES", 104, (70, 250))
            _flat(im, "TINNITUS", 150, (64, 370))
            im.alpha_composite(T.extrude_text((W, H), "WORSE?", (50, 560), 205,
                               face=red, side=(110, 10, 14), depth=20,
                               direction=(0.7, 1.0)))
            _place(im, head, 1130, "centre", H - 1130 + 40)
        else:
            im = _radial((W, H), (960, 260), (110, 14, 20), (8, 4, 7), 860)
            im.alpha_composite(T.sound_rings((W, H), (985, 215), (255, 70, 50),
                               radii=(160, 230, 305, 385), width=9))
            _flat(im, "WHAT MAKES", 74, (48, 70))
            _flat(im, "TINNITUS", 106, (44, 150))
            im.alpha_composite(T.extrude_text((W, H), "WORSE?", (36, 300), 168,
                               face=red, side=(110, 10, 14), depth=16,
                               direction=(0.7, 1.0)))
            _place(im, head, 700, 780, 20)
        return im.convert("RGB")

    if kind == "lineup":
        # The editor's runner-up, now a format (`thumb.lineup_cover`).
        suspects = [(_cut(MUG), 0.40), (None, 0.62), (_wine_glass(), 0.74)]
        return T.lineup_cover(suspects, "Tinnitus: who's\nthe [culprit?]",
                              portrait=portrait,
                              rows=["Tinnitus:", "who's the", "[culprit?]"])
    raise ValueError(f"unknown cover {kind!r} - {COVERS}")


def thumbs(out: Path, portrait: bool = False) -> list[Path]:
    """The shipped cover at `out` (the cutout), and both directions as
    `-cutout` and `-lineup` beside it."""
    made = []
    for k in COVERS:
        p = out.with_name(f"{out.stem}-{k}{out.suffix}")
        cover(k, portrait).save(p, quality=92)
        made.append(p)
    cover(COVERS[0], portrait).save(out, quality=92)
    return [out] + made


def main() -> None:
    stillclip.make(DESK, focus=(0.45, 0.40))
    out = Path.home() / "Desktop/what-makes-tinnitus-worse-long.mp4"
    work = Path.home() / "Desktop/.what-makes-tinnitus-worse-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        # The dark ruled card (`ChapterCard.gridcard`), 2026-11-13: "lets try
        # different overlay for the title sections".
        chapter_style="grid",
        endcard=ENDCARD, endcard_lead=7.0,
        # A belief overturned. Last three tinnitus long forms opened
        # Search / Split / Search; the pair shares this Stamp.
        opener=OPENER,
        # On clips and photos only: "tested" sat under the UNTESTED stamp
        # and the other two first picks fell on beats (first cut).
        emphasis=["the other way", "never test", "the bother"],
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        for p in thumbs(Path.home() / "Desktop/what-makes-tinnitus-worse-long-thumb.jpg"):
            print(p)
    else:
        main()
