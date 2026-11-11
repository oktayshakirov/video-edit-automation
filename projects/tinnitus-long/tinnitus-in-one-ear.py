"""Tinnitus in one ear - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tinnitus-in-one-ear.mdx - what usually
causes ringing on one side, the one sign that makes it same-day care, what
the clinical guideline says, and what a check involves.

**The angle** (`demand/teardowns/tinnitus-in-one-ear.md`): Treble Health's
"Should You Ring The Alarm For Tinnitus In One Ear?" (68k, 11.1x) and
MindEar's "One-Sided Tinnitus: Possible Causes" (20k, 33.1x). The promise
that wins is *whether to worry and when to act*; the heatmap's peak is the
causes list; the comments are people sorting their own case. Theirs spends
its first 40 seconds on a plan, a plug and a "what is tinnitus" recap, and
that is the trough. Ours gives the verdict - usually ordinary, still the
pattern worth checking - by 0:15, and promises the two lists.

**Title is the search** (`longform.md`): "Why Is My Tinnitus Only in One
Ear?" - the article's first heading, the typed question - with the
promise "When to Get It Checked" under it on the slate. The Short takes the
other query, "is tinnitus in one ear serious".

**Three chapters, 2:30-3:00 (E18)**: what causes it, when it is urgent, what
a check involves; then the echo.

## The beats

Last three tinnitus long forms: is-tinnitus-in-the-ear-or-the-brain (reel /
gain / diagram loop), what-does-tinnitus-sound-like (samples / grid),
how-to-manage-a-tinnitus-spike (steps / checklist / diagram).

* `compare` - common against less common, the article's own two groups.
* `checklist` - the note card: the four same-day signs, said as they type.
* `dial` - how fast to act, no needle (a needle is a claim about a reading).
* `steps` - the appointment, in its order.
* `audiogram` - new for this pair: the chart a hearing test produces, one
  line per ear, the gap shading in. Titled as an example.
* `behind` - ORDINARY over a woman at a window, word on top.

**Required toolbox** (`workflow.md`, 2026-11-06): NIDCD's sudden-deafness
page captured (`screencap`, the "medical emergency" line ringed, captured
2026-11-10); the guideline's page address on a `window=("browser")`;
photographs moved (`parallax`, `behind`); `aberration` on the "But
treatment works best early" cut. The disclaimer sits on headphones under a
desk lamp (`stillclip`), not weather. The site's cover is the thumbnail
only.

**Footage: the act, not a portrait of suffering** - a woman reading her
phone in bed, a man on the edge of his bed, headphones going on, a driver with the window at his
ear, a phone call, a countdown, and a hand writing
notes. Fetched fresh 2026-11-10, screened
(luma at 0.5/3/6/9s) and contact-sheeted; none is in another video.

**No medical claims** (`projects/tinnitus.md`): nothing says the ringing
will stop; the growth is named once, as rare and benign, as the article
does; "most come away with an ordinary explanation" is the article's own
line about the *test*, not about the tinnitus. Red flags are on screen.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tinnitus-in-one-ear.py
"""

import sys
from pathlib import Path

from video_automation.core import music, stillclip
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "tinnitus-in-one-ear"
DEMAND = ("'tinnitus in one ear': Treble 'Should You Ring The Alarm For "
          "Tinnitus In One Ear?' 68k (11.1x), MindEar 'One-Sided Tinnitus: "
          "Possible Causes' 20k (33.1x); teardowns/tinnitus-in-one-ear.md")
COVER_STYLE = "text"

ROOT = Path(__file__).resolve().parents[2]
V = STOCK / "videos"

# Fetched fresh 2026-11-10, luma at 0.5/3/6/9s, contact-sheeted at 15/50/85%.
# Screened on the set, not the person (`tools/stock_sheet.py`, B = luma with
# the subject masked out), and cast by eye across the whole video: one clip
# per person, no single group carrying the cut (2026-11-11 re-cut).
PHONE = V / "woman-in-bed-looking-at-phone-at-night/6466354.mp4"        # 28s, B28-36, a woman under a blanket reading her phone - opens and closes
BEDSIDE = V / "man-sitting-on-bed-at-night/7280519.mp4"                # 18s, B30-32, a man on the edge of his bed, phone in hand (from 11s)
LISTEN = V / "headphones-listening-dark-room/6614768.mp4"              # 30s, L42-53, a man putting headphones on, both hands at his ears
DRIVER = V / "driving-car-at-night-window/8470705.mp4"                 # 18s, L28-34, a driver at night, the window at his ear
CALL = V / "woman-sitting-on-bed-with-phone-night/7698902.mp4"         # 17s, L32-36, a woman on her bed, looks at her phone, then calls
COUNTDOWN = V / "clock-ticking-dark/29527767.mp4"                      # 11s, L6-7, a digital countdown, 0:09 to 0:01
NOTES = V / "hand-booking-appointment-phone-dark/4100690.mp4"          # 19s, L40-55, a hand writing in a notebook - in a window
ENDCARD = V / "subscribe/4928934.mp4"

# The real page: NIDCD's sudden-deafness page, captured 2026-11-10
# (`screencap`, record in `captures/nidcd-sudden-deafness/`). The camera
# goes from the title to the ringed line, "...should consider sudden
# deafness symptoms a medical emergency and visit a doctor immediately."
NIDCD = STOCK / "captures/nidcd-sudden-deafness/nidcd-sudden-deafness-l.mp4"
GUIDELINE = ("browser", "entnet.org/resource/clinical-practice-guideline-tinnitus")

# The site's own cover, cut left of the ear: half a face behind a dark
# panel. **The thumbnail only** - the first cut also ran it three times
# inside the video, and the editor found the cover repeated in the picture
# boring (2026-11-11).
ONE_SIDE = ROOT / "assets/tinnitus/tinnitus-in-one-ear/one-side.jpg"

# Pexels photos, fetched 2026-11-11 (manifested).
P = STOCK / "photos"
WINDOW = P / "man-looking-out-window-at-night/31428994.jpg"             # a man at a window with a mug, from behind - "ordinary"
MORNING = P / "woman-by-window-at-night-thinking/7616813.jpg"          # a woman at a window with a mug, a dark room to her left - ORDINARY
DESKPHONES = P / "headphones-on-desk-at-night/18228473.jpg"             # headphones on a stand under a desk lamp - the disclaimer
DISCLAIMER_BG = stillclip.path(DESKPHONES, focus=(0.55, 0.50))

# The hearing test's chart, drawn (`audiogram`): an example, one ear flat
# near the top, the other sagging at the high pitches.
EAR_A = [10, 10, 15, 15, 20, 20]
EAR_B = [10, 15, 25, 45, 55, 60]

VOICE = "noah"          # the noah test, pair 5 of 5 (`projects/tinnitus.md`)
MUSIC = music.track("night-drift")
URL = "https://tinnitushelp.me/blog/tinnitus-in-one-ear"

URGENCY = [("In the coming weeks", 0.62, "#ffdab9"),
           ("Same day", 1.0, "#e0605a")]


def sections() -> list:
    return [
    # --- hook. No card. The Search types the question. -----------------------
    Section(
        title="Tinnitus in one ear",
        card=False,
        sentences=[
            ("Ringing in only one ear feels different from ringing in both.",),
            ("And if you searched it at night, the scariest answer was probably near the top.",),
            ("Actually, it usually has an ordinary cause.",),
            ("But it is also the one pattern the clinical guideline tells doctors to check promptly.",),
            ("Both are true. By the end, you will know which of two lists you are on.",),
        ],
        shots=[
            Shot(clip=PHONE, clip_at=1.0),
            None,
            Shot(image=WINDOW, parallax=0.5),
            None,
            Shot(clip=BEDSIDE, clip_at=11.0),
        ],
        gaps=[0.80, 0.85, 0.70, 0.80, 0.90],
    ),

    # --- what causes it --------------------------------------------------------
    Section(
        title="What causes tinnitus in one ear?",
        spoken_title="So what causes tinnitus in one ear?",
        kicker="TWO EARS",
        sentences=[
            ("Your two ears keep separate histories.",),
            ("Wax builds up on one side, an infection picks one ear, and noise rarely hits both the same.",),
            ("A driver's ear nearest the open window often hears worse than the other one.",),
            ("So the causes sort into two groups.",),
            # the compare's own sentence: a heading chunk per column, one per item.
            ("Most often, something ordinary.",
             "Wax against the eardrum.",
             "An infection, or fluid.",
             "More noise on one side, or the jaw.",
             "Less often,",
             "a sudden loss of hearing,",
             "an inner-ear condition,",
             "or a rare, benign growth on the hearing nerve."),
            ("And a sound that beats in time with your heartbeat is its own kind, with its own check.",),
        ],
        shots=[
            Shot(clip=LISTEN, clip_at=1.0),
            None,
            Shot(clip=DRIVER, clip_at=1.0),
            None,
            Shot(graphic="compare",
                 payload=("USUALLY",
                          ["Wax on the eardrum", "Infection or fluid",
                           "Uneven noise, or the jaw"],
                          "LESS OFTEN",
                          ["Sudden hearing loss", "An inner-ear condition",
                           "A rare, benign growth"],
                          True)),
            None,
        ],
        gaps=[0.55, 0.80, 0.80, 0.55, 1.40, 0.90],
    ),

    # --- when it is urgent ------------------------------------------------------
    Section(
        title="When is it urgent?",
        spoken_title="So when is it urgent?",
        kicker="THE ONE SIGN",
        card_gap=1.20,
        sentences=[
            ("Most of this can wait for a normal appointment. One thing cannot.",),
            ("If the ringing came with a sudden drop in hearing on that side, that is same-day care.",),
            # the capture: title, then the ring on the line read.
            ("The US hearing institute's own page says to treat sudden deafness as a medical emergency, and see a doctor immediately.",),
            ("It is easy to mistake for a blocked ear that will clear on its own.",),
            ("But treatment works best early, and after two to four weeks it is much less likely to bring the hearing back.",),
            ("So here is the first list.",),
            # the note card's own sentence: one chunk per row, all said as yes.
            ("Hearing that dropped suddenly.",
             "A sound that beats with your pulse.",
             "A weak or numb face.",
             "New dizziness or vertigo."),
            # the dial: one chunk, no needle.
            ("If none of those fit, you are on the second list: a hearing test, booked in the coming weeks.",),
            ("That covers new ringing in one ear, ringing that has stayed for weeks, or hearing on that side that feels even slightly different.",),
        ],
        shots=[
            Shot(clip=CALL, clip_at=0.5),
            None,
            Shot(clip=NIDCD, clip_at=0.0),
            None,
            Shot(clip=COUNTDOWN, clip_at=0.5, shader="aberration"),
            None,
            Shot(graphic="checklist",
                 payload=([("Hearing dropped suddenly", True),
                           ("Beats with your pulse", True),
                           ("A weak or numb face", True),
                           ("New dizziness or vertigo", True)],
                          "SAME DAY IF", True)),
            Shot(graphic="dial",
                 payload=(URGENCY, None, "", "HOW FAST TO ACT", 0)),
            None,
        ],
        gaps=[0.85, 0.80, 0.80, 0.85, 0.90, 0.55, 2.00, 0.90, 0.90],
    ),

    # --- what a check involves --------------------------------------------------
    Section(
        title="What happens when you get it checked?",
        spoken_title="So what happens when you get it checked?",
        kicker="THE HEARING TEST",
        sentences=[
            ("The guideline ear specialists follow is plain: one-sided tinnitus gets a prompt, full hearing test.",),
            ("Scans are kept for some cases, and even then the hearing test usually comes first.",),
            ("The appointment itself is simpler than most people expect.",),
            # steps: one chunk per stop on the track.
            ("Questions about when it started,",
             "a look in the ear, with any wax cleared,",
             "a hearing test, one ear at a time,",
             "and the two sides compared."),
            # the audiogram's own sentence: one chunk per ear.
            ("On the chart they draw, each ear gets its own line.",
             "When one line sags below the other, that gap is what they look for."),
            ("In most cases, that finds an ordinary explanation, or nothing alarming at all.",),
        ],
        shots=[
            Shot(clip=NOTES, clip_at=1.0, window=GUIDELINE),
            None,
            None,
            Shot(graphic="steps",
                 payload=(["When it started", "A look in the ear",
                           "One ear at a time", "The two sides compared"],
                          "THE APPOINTMENT")),
            Shot(graphic="audiogram",
                 payload=(EAR_A, EAR_B, "A HEARING TEST - AN EXAMPLE",
                          "the gap they look for")),
            None,
        ],
        gaps=[0.85, 0.80, 0.55, 1.40, 1.20, 0.90],
    ),

    # --- close: the echo --------------------------------------------------------
    Section(
        title="So should you worry?",
        spoken_title="So, should you worry?",
        kicker="THE ANSWER",
        sentences=[
            ("One-sided ringing is usually ordinary, and it is still the pattern worth checking.",),
            ("Same day if your hearing dropped. A hearing test in the coming weeks if it did not.",),
            ("This video is general information, not medical advice.",),
            ("So, how does the hearing in that ear compare to the other one?",),
        ],
        shots=[
            # The word on top, not tucked: tucked, the face hid the Y and it
            # read "ORDINAR" for most of the shot (first cut, 2026-11-10).
            Shot(graphic="behind",
                 payload=(MORNING, "ORDINARY", "Still worth a check", "fly",
                          None, False)),
            None,
            Shot(clip=DISCLAIMER_BG, clip_at=0.5,
                 payload=("", "General information, not medical advice.")),
            Shot(clip=PHONE, clip_at=18.0),
        ],
        gaps=[0.80, 1.00, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="Why Is My Tinnitus Only in One Ear? When to Get It Checked",
    hook="Tinnitus in one ear usually has an ordinary cause - and it is still "
         "the one pattern the clinical guideline says to check promptly. Here "
         "is what usually causes ringing on one side, the one sign that makes "
         "it same-day care, the other red flags, and what a hearing check "
         "actually involves.",
    url=URL,
    summary="Tinnitus in one ear, explained: why your two ears have separate "
            "histories (wax, infection or fluid, uneven noise such as a "
            "driver's window ear, the jaw); the less common causes (sudden "
            "sensorineural hearing loss, inner-ear conditions, a rare benign "
            "growth on the hearing nerve); pulsatile tinnitus as its own "
            "kind; why ringing with a sudden drop in hearing is same-day "
            "care, per the NIDCD; the other same-day signs (a sound that "
            "beats with your pulse, facial weakness or numbness, new "
            "dizziness or vertigo); what the AAO-HNSF clinical practice "
            "guideline recommends (a prompt hearing test for one-sided "
            "tinnitus, imaging only in some cases); and what to expect at "
            "the appointment.",
    tags=["tinnitus in one ear", "why is my tinnitus only in one ear",
          "ringing in one ear", "one sided tinnitus", "unilateral tinnitus",
          "is tinnitus in one ear serious", "tinnitus left ear",
          "tinnitus right ear", "sudden hearing loss", "when to see a doctor "
          "for tinnitus", "tinnitus", "ringing in ears"],
    cta=f"Both lists in full, the guideline's wording and what to expect at "
        f"the appointment: {URL}",
    credits=["This video is general information, not medical advice. If your "
             "hearing dropped suddenly, the sound beats with your pulse, or "
             "you have facial weakness, numbness or new dizziness, seek care "
             "the same day.",
             "Pages: NIDCD, \"Sudden Deafness\" (captured 10 Nov 2026); "
             "AAO-HNSF, Clinical Practice Guideline: Tinnitus."],
)

# The channel's word on the cover (2026-11-11): "tinnitus" is what the
# viewer typed, and the first cover's "Only in one ear?" never said it.
THUMB_HEADLINE = "Tinnitus\nin [one ear?]"


def thumbs(out: Path) -> Path:
    """The site's half-lit face (cut left of the ear) on the right of the
    frame, the question in two rows on the dark panel to its left."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(ONE_SIDE).convert("RGB")
    h = 720
    pic = src.resize((int(src.width * h / src.height), h), Image.LANCZOS)
    im = Image.new("RGB", (1280, 720), (8, 6, 6))
    im.paste(pic, (1280 - pic.width, 0))
    fill, ink = T.ACCENTS["red"]
    T._headline(im, THUMB_HEADLINE, 230, 700, 48, fill, ink,
                max_lines=2, leading=1.0, band="top", margin=170,
                shadow=12, drop=(5, 6))
    im.save(out, quality=92)
    return out


def main() -> None:
    stillclip.make(DESKPHONES, focus=(0.55, 0.50))
    out = Path.home() / "Desktop/tinnitus-in-one-ear-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-in-one-ear-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=10.0, title_hold=5.0,
        # The typed question. Last three tinnitus long forms opened Split /
        # Search / Search; the pair shares the opener type, not the query.
        opener=Search("why is my tinnitus only in one ear"),
        emphasis=["ordinary", "same-day care", "prompt, full hearing test"],
        thumb_headline=THUMB_HEADLINE, thumb_image=ONE_SIDE,
        thumb_accent="red",
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/tinnitus-in-one-ear-long-thumb.jpg"))
    else:
        main()
