"""Tinnitus treatments ranked by the 2026 guideline - long-form 16:9, an E26
ranking.

Source: tinnitus-blog/content/posts/tinnitus-guideline-2026.mdx - the 2026
AAO-HNSF Clinical Practice Guideline: Tinnitus Update, its 16 key action
statements and their grades, what changed since 2014, the warning signs,
and the questions to take to an appointment.

**The angle** (`demand/teardowns/tinnitus-treatments-ranked.md`): the
treatment rankings stand out (HearingTracker "Four BEST Tinnitus
Treatments" 402k, 109x; Doctor Cliff "The 4 BEST Tinnitus Treatments" 30.6x;
the adjacent "Surgeons Rank 11 Supplements" 97x), and "tinnitus guideline
2026" is a five-week-old search term with almost no answers (Timpanogos
~3x, the rest under 300 views). Theirs rank by an audiologist's say-so; ours
ranks by the guideline panel's own grades, so **we rank nothing ourselves:
the rows are the panel's grades**, worst first, best last, and the twist is
the top row, which holds no treatment at all.

**E26: `FORMAT = "ranking"`, 5-8 minutes.** One chapter per row of the
board, then the top grade, the warning signs, the echo.

**Every grade checked against the abstract** (Adams et al., 2026,
doi 10.1002/ohn.70417, read on Europe PMC 2026-11-19): strong for KAS 2, 3
and 6; recommendations for KAS 1, 5, 7, 8, 9, 11, 15; against for KAS 12,
13, 14A; options for KAS 4, 10, 14B. The article's "362 trials" figure is
not in any primary page that could be read, so it is not said.

## The beats

Last tinnitus article long forms: tinnitus-in-one-ear (compare / checklist /
dial / steps / audiogram / behind), what-makes-tinnitus-worse (steps / diary
/ diagram / chart / checklist / spotlight / callout / bars).

* `tiers` - **new, built for this video.** The guideline's four grades as
  rows; each chapter drops its treatments into its row, and the board comes
  back holding what it already has. The top row stays empty.
* `post` - the guideline's own sentence on supplements (KAS 13), and its
  citation.
* `callout` - the site's bimodal photograph: sound in the headphones, the
  pulses on the tongue.
* `spotlight` - the site's hearing aid.
* `grid` - the three things CBT works on; the three strong grades.
* `checklist` - the warning signs, the note card.
* `steps` - the questions to ask.

**Real pages:** the AAO-HNS release page forbids copying its content into
software or websites (its own terms, read 2026-11-19), PubMed answers a
headless browser with a cookie wall and Europe PMC timed out - so the
guideline's wording goes on `post` cards, quoted from the abstract.

**No medical claims** (`projects/tinnitus.md`): the rows grade the panel's
recommendation, never relief. "Advised against" is said with its own key
words, "for tinnitus itself", and with "never stop a prescribed medicine
without the doctor who prescribed it" on screen. Spoken: no CBT, rTMS, ENT.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tinnitus-treatments-ranked.py
"""

import sys
from pathlib import Path

from video_automation.core import music, stillclip
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Split

SOURCE_POST = "tinnitus-guideline-2026"
DEMAND = ("HearingTracker 'Four BEST Tinnitus Treatments' 402k (109x); Doctor "
          "Cliff 'The 4 BEST Tinnitus Treatments' 30.6x; 'tinnitus guideline "
          "2026' a new term (Timpanogos ~3x, rest <300); "
          "teardowns/tinnitus-treatments-ranked.md")
FORMAT = "ranking"
COVER_STYLE = "tiers"

ROOT = Path(__file__).resolve().parents[2]
V = STOCK / "videos"
SITE = Path.home() / "Coding/tinnitus-blog/public/images"

# Fetched 2026-11-19 (`tools/stock_sheet.py`), B = the set's luma at
# 0.5/3/6/9s, contact-sheeted and watched to the end. None is in another video.
READER = V / "woman-reading-tablet-at-night-dark/7198399.mp4"            # 22s, B11, a woman in glasses reading a tablet, purple light - opens
LAPTOP = V / "woman-looking-out-window-at-night-city/7988267.mp4"         # 7s, B26-30, a woman at a laptop by a night window
CAPSULES = V / "supplement-capsules-in-hand-dark/5453702.mp4"             # 11s, B70-78, two hands full of capsules - in a window
DOCPILLS = V / "prescription-pill-bottle-dark-table/8731104.mp4"          # 13s, B144-155, a doctor's hands, pills and a bottle - in a window
PILLS = V / "prescription-pill-bottle-dark-table/9902348.mp4"             # 10s, B84-108, blister packs and a bottle on a table - in a window
BEDLAMP = V / "white-noise-machine-bedroom/7505575.mp4"                   # 10s, B78, a woman settling into bed by a lamp - in a window
RADIO = V / "hand-turning-dial-speaker-dark/29570736.mp4"                 # 11s, B113-116, two hands turning a small radio's dial - in a window
SOFA = V / "man-reading-phone-on-sofa-at-night/7924404.mp4"               # 15s, B79-84, an older man with a tablet on a sofa
WRITING = V / "writing-notes-notebook-night-lamp/39425735.mp4"            # 10s, B86-90, a hand writing in a notebook by a lamp - in a window
MRI = V / "mri-scanner-hospital/7088463.mp4"                              # 26s, B116-124, an empty scanner room - in a window
BLOOD = V / "blood-test-tube-lab-dark/8534603.mp4"                          # 14s, B115-122, a gloved hand lifting a blood tube - in a window
JOURNAL = V / "woman-writing-in-journal-in-bed-night/6639799.mp4"        # 21s, B22-50, a woman writing in a journal at night
SILHOUETTE = V / "man-looking-out-window-at-night-thinking/34535507.mp4" # 16s, B32-61, a man at a window, a silhouette
ENDCARD = V / "subscribe/4928934.mp4"

# The site's own pictures (screened by eye 2026-11-19).
GUIDE = SITE / "tinnitus-guideline-2026.jpg"            # a woman in glasses with a tablet at a window
GINKGO = SITE / "ginkgo-biloba-and-tinnitus.jpg"        # ginkgo leaves, autumn yellow
BIMODAL = SITE / "bimodal-neuromodulation-for-tinnitus.jpg"  # a man in headphones, a device's tip at his lips
HEARING_AID = SITE / "hearing-aid.jpg"                  # fingers holding a behind-the-ear hearing aid
THERAPY = SITE / "therapy-2.jpg"                        # a therapist and a client in armchairs
DISCLAIMER_BG = stillclip.path(GUIDE, focus=(0.62, 0.40))

VOICE = "mia"
MUSIC = music.track("night-drift")
URL = "https://tinnitushelp.me/blog/tinnitus-guideline-2026"
CITE = "Clinical Practice Guideline: Tinnitus Update"

# The board. The rows are the guideline's own grades, top to bottom; the
# items are every treatment it grades, in the order the video names them.
ROWS = [("Strong yes", "the panel's top grade"),
        ("Recommended", "a firm should"),
        ("An option", "doctors may offer it"),
        ("Advised against", "not for tinnitus itself")]
# The top row's empty line goes on only when the video says so.
ROWS_EMPTY = [ROWS[0] + (None, "No treatment got this grade")] + ROWS[1:]
ITEMS = [(3, "Supplements", "\U0001F48A"),
         (3, "Magnetic brain stimulation", "\U0001F9F2"),
         (3, "Medicines for the ringing", "\U0001F489"),
         (2, "Sound enrichment", "\U0001F30A"),
         (2, "Bimodal devices", "\U0001F3A7"),
         (1, "Explaining it", "\U0001F4A1"),
         (1, "Hearing aids", "\U0001F9BB"),
         (1, "Cochlear implant check", "\U0001F442"),
         (1, "CBT", "\U0001F4AC")]
BOARD = "THE 2026 GUIDELINE"


def board(shown: int, until: int | None = None, empty: bool = False) -> Shot:
    return Shot(graphic="tiers", ground="grid",
                payload=(ROWS_EMPTY if empty else ROWS, ITEMS, BOARD,
                         shown, until))


def sections() -> list:
    return [
    # --- hook. No card. ------------------------------------------------------
    Section(
        title="Tinnitus treatments, ranked",
        card=False,
        sentences=[
            ("The US guideline for treating tinnitus has just been rewritten.",),
            ("It is the first update in twelve years, and it grades every treatment you have probably been offered.",),
            ("Some it recommends. Some it tells doctors not to recommend at all.",),
            ("And the one most people try first, a supplement, is on that second list.",),
            ("Here is all of it, ranked, from what it advises against up to what it recommends.",),
            ("Stay to the end for the one grade no treatment reached.",),
        ],
        shots=[
            Shot(clip=READER, clip_at=1.0),
            Shot(image=GUIDE, parallax=0.5, note=("12 YEARS", "since the last update, in 2014")),
            Shot(clip=LAPTOP, clip_at=0.5),
            Shot(clip=CAPSULES, clip_at=1.0, window=("player", "Supplements, the first thing many try")),
            Shot(image=GINKGO, parallax=0.6),
            Shot(clip=SILHOUETTE, clip_at=1.0, window=("player", "One grade, and no treatment in it")),
        ],
        gaps=[0.70, 0.80, 0.90, 0.85, 0.80, 0.90],
    ),

    # --- what it is, and the grades -------------------------------------------
    Section(
        title="What is the 2026 tinnitus guideline?",
        spoken_title="So what is the new tinnitus guideline?",
        kicker="THE GUIDELINE",
        sentences=[
            # post: the card, then the highlight on the title.
            ("It is the clinical practice guideline from America's ear, nose and throat surgeons,",
             "the Tinnitus Update, published in October."),
            ("It is written for the people who treat you: family doctors, ear specialists, audiologists and psychologists.",),
            ("And it is about adults whose tinnitus has lasted six months or more, and bothers them.",),
            ("Each of its sixteen recommendations carries a grade, and there are four.",),
            # tiers, rows only: one chunk per grade.
            ("A strong recommendation, the panel's top grade,",
             "a recommendation, which is a firm should,",
             "an option, which a doctor may offer, on less certain evidence,",
             "and a recommendation against."),
            ("So start at the bottom of the board.",),
        ],
        shots=[
            Shot(graphic="post",
                 payload=("headline",
                          {"source": "Otolaryngology-Head and Neck Surgery",
                           "date": "October 2026",
                           "headline": "Clinical Practice Guideline: [Tinnitus Update]"},
                          "")),
            Shot(image=THERAPY, window=("player", "The people who treat it")),
            Shot(clip=SOFA, clip_at=2.0, note=("6 MONTHS+", "and it bothers you")),
            None,
            Shot(graphic="tiers", ground="grid", payload=(ROWS, [], BOARD)),
            None,
        ],
        gaps=[0.80, 0.70, 0.80, 0.70, 1.40, 0.90],
    ),

    # --- advised against ------------------------------------------------------
    Section(
        title="What does the guideline advise against?",
        spoken_title="So what does the guideline advise against?",
        kicker="ADVISED AGAINST",
        card_gap=1.20,
        sentences=[
            ("These are the treatments doctors are told not to recommend for tinnitus itself.",),
            # tiers: the bottom row, one chunk per card.
            ("Dietary supplements,",
             "magnetic brain stimulation,",
             "and medicines given to treat the ringing itself."),
            ("The supplement line is the one that surprises people most.",),
            # post: the lead-in, then the guideline's own words.
            ("In its own words, clinicians should not recommend",
             "dietary supplements for persistent, bothersome tinnitus."),
            # "ginkgo" reads with a soft J (espeak dʒˈɪŋkɡoʊ); "Ghinko" is
            # GINK-oh. The shipped render was patched with tools/revoice.py
            # (2026-11-20); the pair is here for the next full build.
            (("The 2014 version had already named ginkgo, melatonin and zinc, and the new patient guide still uses ginkgo as its example.",
              "The 2014 version had already named Ghinko, melatonin and zinc, and the new patient guide still uses Ghinko as its example."),),
            ("A blood test that finds a real deficiency is a separate question, for your doctor.",),
            # diagram: one chunk per node.
            ("Magnetic brain stimulation holds a magnetic coil against the scalp,",
             "and sends pulses into the brain."),
            # grid: one chunk per year.
            ("In 2014 it was advised against for routine use.",
             "In 2026, the word routine is gone."),
            ("The medicines are antidepressants, anti-seizure drugs, anti-anxiety drugs, and injections through the eardrum.",),
            ("Actually, the key words are for tinnitus itself.",),
            ("If you also have depression or anxiety, treating that is a separate decision.",),
            ("And never stop a prescribed medicine without the doctor who prescribed it.",),
        ],
        shots=[
            board(0, 0),
            board(0, 3),
            Shot(clip=CAPSULES, clip_at=6.0, window=("player", "Ginkgo, melatonin, zinc")),
            Shot(graphic="post",
                 payload=("headline",
                          {"source": CITE, "date": "Key action statement 13, 2026",
                           "headline": "Clinicians should not recommend [dietary "
                                       "supplements for the primary indication of "
                                       "persistent, bothersome tinnitus.]"},
                          "")),
            Shot(image=GINKGO, parallax=0.5, note=("GINKGO", "the patient guide's example")),
            Shot(clip=BLOOD, clip_at=1.0, window=("player", "A deficiency is a separate question")),
            Shot(graphic="diagram", ground="grid",
                 payload=([("A magnetic coil", "held against the scalp", "\U0001F9F2"),
                           ("Pulses into the brain", "to change its activity", "\U0001F9E0")],
                          "MAGNETIC BRAIN STIMULATION", False)),
            Shot(graphic="grid", ground="grid",
                 payload=([("2014", "advised against routine use", "\U0001F4C5"),
                           ("2026", "advised against, no 'routine'", "\U0001F6AB")],
                          "MAGNETIC BRAIN STIMULATION")),
            Shot(clip=DOCPILLS, clip_at=1.0, window=("player", "Medicines given for the ringing")),
            Shot(clip=PILLS, clip_at=2.0, window=("player", "For tinnitus itself"),
                 shader="aberration"),
            None,
            Shot(clip=SOFA, clip_at=8.0,
                 payload=("", "Never stop a prescribed medicine on your own.")),
        ],
        gaps=[0.70, 1.40, 0.60, 1.20, 0.80, 0.90, 1.10, 1.10, 0.85, 0.80, 0.70, 0.95],
    ),

    # --- an option --------------------------------------------------------------
    Section(
        title="Which treatments are only an option?",
        spoken_title="So which treatments are only an option?",
        kicker="AN OPTION",
        sentences=[
            ("One row up are the options: things a doctor may offer, where the evidence is less certain.",),
            # tiers: one chunk per card.
            ("Sound enrichment,",
             "and bimodal neuromodulation."),
            ("Sound enrichment is what the 2014 version called sound therapy.",),
            ("It means adding gentle sound to a quiet room: a fan, soft music, or a steady sound like white noise.",),
            ("Bimodal neuromodulation is new to the guideline.",),
            # callout: one chunk per label.
            ("It pairs sound in headphones",
             "with mild pulses on the tongue."),
            ("One device that works this way is called Lenire.",),
            ("As an option, it is something you might be offered, not something to expect first.",),
        ],
        shots=[
            Shot(clip=BEDLAMP, clip_at=1.0, window=("player", "A quiet room")),
            board(3, 5),
            None,
            Shot(clip=RADIO, clip_at=1.0, window=("player", "Gentle sound in a quiet room")),
            Shot(clip=READER, clip_at=6.0),
            Shot(graphic="callout",
                 payload=(BIMODAL, [("Sound, in headphones", 0.30, 0.20),
                                    ("Mild pulses, on the tongue", 0.70, 0.36)],
                          "BIMODAL NEUROMODULATION")),
            None,
            None,
        ],
        gaps=[0.70, 1.20, 0.60, 0.85, 0.60, 1.20, 0.80, 0.95],
    ),

    # --- recommended ------------------------------------------------------------
    Section(
        title="What does the guideline recommend?",
        spoken_title="So what does the guideline recommend?",
        kicker="RECOMMENDED",
        sentences=[
            ("The row it recommends has four in it.",),
            # tiers: one chunk per card.
            ("Explaining what tinnitus is,",
             "hearing aids when hearing is a struggle,",
             "a cochlear implant check when hearing loss is severe,",
             "and cognitive behavioral therapy."),
            ("The first sounds too simple to count.",),
            ("But doctors should explain what tinnitus is, how it tends to behave over time, and what you can do about it.",),
            ("Hearing aids used to need a documented hearing loss. Now it is anyone who struggles to hear, with tinnitus that stays and bothers them.",),
            ("Making the sounds around you louder is how they make the ringing less noticeable.",),
            ("And for hearing loss that is severe enough, a referral to check for a cochlear implant is new this year.",),
            ("Cognitive behavioral therapy does not aim to switch the sound off.",),
            # grid: one chunk per card.
            ("It works on how you react to it: the worry,",
             "the attention it grabs,",
             "and what it does to your sleep and mood."),
            ("It is one of only a handful of treatments the guideline actively recommends.",),
        ],
        shots=[
            Shot(clip=READER, clip_at=16.0),
            board(5, 9),
            None,
            Shot(image=THERAPY, parallax=0.4),
            Shot(graphic="spotlight",
                 payload=(HEARING_AID, [((0.30, 0.30, 0.78, 0.78), "A HEARING AID")],
                          "", False)),
            None,
            Shot(clip=SOFA, clip_at=4.0, note=("NEW IN 2026", "a cochlear implant check")),
            Shot(clip=LAPTOP, clip_at=1.5),
            Shot(graphic="grid", ground="grid",
                 payload=([("The worry", "", "\U0001F914"),
                           ("The attention it grabs", "", "\U0001F300"),
                           ("Sleep and mood", "", "\U0001F634")],
                          "WHAT CBT WORKS ON")),
            Shot(image=THERAPY, window=("player", "Cognitive behavioral therapy")),
        ],
        gaps=[0.70, 1.50, 0.60, 0.85, 0.80, 0.85, 0.85, 0.70, 1.30, 0.95],
    ),

    # --- the top grade ----------------------------------------------------------
    Section(
        title="So what got the top grade?",
        spoken_title="So what got the top grade?",
        kicker="THE TOP GRADE",
        card_gap=1.30,
        sentences=[
            ("Look at the top row again.",),
            ("Not one treatment is in it.",),
            ("The strongest grades went to the appointment itself, and there are three.",),
            # grid: one chunk per card.
            ("Tell bothersome tinnitus apart from the kind that is not,",
             "ask about your mood, including any thoughts of self-harm,",
             "and skip the brain scan unless there is a warning sign."),
            ("That is the shift since 2014: more attention on the person, and less on pills and scans.",),
            ("If the ringing has worn your mood down that far, say so. It is now part of the exam.",),
        ],
        shots=[
            board(9, 9, empty=True),
            None,
            Shot(clip=JOURNAL, clip_at=8.0),
            Shot(graphic="grid", ground="grid",
                 payload=([("Is it bothering you?", "bothersome or not", "\U0001F914"),
                           ("How is your mood?", "including self-harm", "\U0001F5E3"),
                           ("No scan without a sign", "a strong no", "\U0001F9E0")],
                          "THE THREE STRONG GRADES")),
            Shot(image=GUIDE, parallax=0.4),
            Shot(clip=READER, clip_at=8.0, window=("player", "Now part of the exam")),
        ],
        gaps=[0.70, 1.10, 0.70, 1.40, 0.85, 0.95],
    ),

    # --- the warning signs, and the questions ----------------------------------
    Section(
        title="When do you still need more tests?",
        spoken_title="So when do you still need more tests?",
        kicker="THE WARNING SIGNS",
        sentences=[
            ("Fewer scans does not mean ignoring the rare serious cause.",),
            ("The patient guide lists these as reasons for more tests, or prompt care.",),
            # checklist, the note card: one chunk per sign.
            ("Ringing in one ear only.",
             "Ringing that pulses with your heartbeat.",
             "Hearing loss in one ear, or hearing that drops suddenly.",
             "New dizziness, weakness or numbness."),
            ("Hearing that drops suddenly needs care the same day.",),
            ("And the guideline gives you questions worth taking to your next appointment.",),
            # steps: one chunk per question.
            ("Can I have a full hearing test?",
             "Would a hearing aid help me?",
             "Can you refer me for cognitive behavioral therapy?",
             "And how will we know if it is working?"),
            ("That last one is new too: doctors are now asked to measure whether a treatment is helping.",),
        ],
        shots=[
            Shot(clip=MRI, clip_at=12.0, window=("player", "A scan: kept for the warning signs")),
            None,
            Shot(graphic="checklist",
                 payload=([("Ringing in one ear only", True),
                           ("Pulses with your heartbeat", True),
                           ("Hearing loss in one ear", True),
                           ("New dizziness or numbness", True)],
                          "GET IT CHECKED IF", True)),
            Shot(clip=SOFA, clip_at=10.0, note=("SAME DAY", "if hearing drops suddenly")),
            Shot(clip=WRITING, clip_at=1.0, window=("player", "Questions for the appointment")),
            Shot(graphic="steps", ground="grid",
                 payload=(["A full hearing test?", "Would a hearing aid help?",
                           "A referral for CBT?", "How will we know it works?"],
                          "ASK AT YOUR APPOINTMENT")),
            Shot(clip=JOURNAL, clip_at=14.0, window=("player", "Measured, not guessed")),
        ],
        gaps=[0.70, 0.60, 2.40, 0.85, 0.60, 1.40, 0.95],
    ),

    # --- close: the echo --------------------------------------------------------
    Section(
        title="So what does it change for you?",
        spoken_title="So, what does it change for you?",
        kicker="THE ANSWER",
        sentences=[
            ("The guideline that took twelve years to rewrite has no cure in it, and it does not pretend to.",),
            ("What it has is a clearer standard: a proper hearing test, real attention to mood, hearing devices and therapy where they fit, and fewer pills, supplements and scans.",),
            ("This video is general information, not medical advice.",),
            ("So, which row is the treatment you were offered in?",),
        ],
        shots=[
            Shot(clip=SILHOUETTE, clip_at=7.0),
            board(9, 9, empty=True),
            Shot(clip=DISCLAIMER_BG, clip_at=0.5,
                 payload=("", "General information, not medical advice.")),
            board(9, 9, empty=True),
        ],
        gaps=[0.80, 1.00, 1.10, 2.30],
    ),
    ]


SECTIONS = sections()

META = Meta(
    title="Tinnitus Treatments Ranked by the New 2026 Guideline",
    hook="The US tinnitus guideline has been rewritten for the first time in "
         "twelve years, and it grades every treatment. Here is all of it, "
         "ranked by the panel's own grades: what it advises against "
         "(supplements, magnetic brain stimulation, medicines for the ringing "
         "itself), what it lists as an option (sound enrichment, bimodal "
         "neuromodulation), what it recommends (hearing aids, cochlear implant "
         "checks, cognitive behavioral therapy), and the one grade no "
         "treatment reached.",
    url=URL,
    summary="The 2026 AAO-HNSF Clinical Practice Guideline: Tinnitus Update "
            "(published October 2026, replacing the 2014 version) for adults "
            "with tinnitus that has lasted six months or more and bothers "
            "them, its 16 key action statements ranked by grade. Advised "
            "against for tinnitus itself: dietary supplements (ginkgo, "
            "melatonin, zinc), repetitive transcranial magnetic stimulation "
            "(rTMS), and routine antidepressants, anticonvulsants, anxiolytics "
            "or intratympanic medications. Options: sound enrichment and "
            "bimodal neuromodulation (such as Lenire). Recommended: education, "
            "hearing aid evaluation for anyone with hearing difficulties, "
            "cochlear implant referral when criteria are met, cognitive "
            "behavioral therapy (CBT), and measuring whether treatment works. "
            "Strong recommendations: telling bothersome tinnitus apart, asking "
            "about self-harm risk, and no imaging without warning signs. Plus "
            "the warning signs that still need tests or prompt care, and the "
            "questions to take to your appointment.",
    tags=["tinnitus guideline 2026", "tinnitus treatments ranked",
          "best tinnitus treatment", "tinnitus treatment", "new tinnitus "
          "guidelines", "tinnitus cbt", "hearing aids for tinnitus",
          "lenire", "bimodal neuromodulation", "tinnitus supplements",
          "ginkgo biloba tinnitus", "sound therapy for tinnitus",
          "tinnitus", "ringing in ears"],
    cta=f"All 16 recommendations in one table, what changed since 2014 and the "
        f"questions to take to your appointment: {URL}",
    credits=["This video is general information, not medical advice. Never "
             "stop a prescribed medicine without talking to the doctor who "
             "prescribed it. If your hearing dropped suddenly, the sound beats "
             "with your pulse, or you have new dizziness, weakness or "
             "numbness, seek care promptly.",
             "If you are having thoughts of harming yourself, please reach out "
             "today: in the US call or text 988, in the UK and Ireland call "
             "Samaritans on 116 123, or contact your local emergency services.",
             "Source: Adams ME et al., Clinical Practice Guideline: Tinnitus "
             "Update, Otolaryngology-Head and Neck Surgery, 2026 "
             "(doi 10.1002/ohn.70417), and the AAO-HNSF patient guide."],
)

# Three rows, Title Case, one centred block (`thumb.stack_headline`; the
# editor, 2026-11-20, after Diary of a CEO's covers).
HEADLINE_ROWS = ["Tinnitus:", "What's", "[Top Tier?]"]
THUMB_HEADLINE = "\n".join(HEADLINE_ROWS)
# The editor picked the tier board (2026-11-20); the cut-out direction (a
# supplement bottle crossed, a hearing aid ticked) was deleted with its code.
COVERS = ("tiers",)
COVER_HEADLINES = {"tiers": HEADLINE_ROWS}


def _ground(W, H):
    """The tier board's own dark ruled ground, frozen."""
    from PIL import Image
    from video_automation.longform.beats.base import grid_ground
    return Image.fromarray(grid_ground(W, H, 3.0, TINNITUS.primary)).convert("RGBA")


def _card_lines(label, room, size):
    """`label` wrapped into `room` px at `size`, or None past two lines."""
    from PIL import Image, ImageDraw
    from video_automation.longform.beats.base import _font
    d, f = ImageDraw.Draw(Image.new("L", (8, 8))), _font(size)
    lines, cur = [], ""
    for word in label.split():
        t = f"{cur} {word}".strip()
        if d.textlength(t, font=f) <= room:
            cur = t
        elif cur and d.textlength(word, font=f) <= room:
            lines.append(cur)
            cur = word
        else:
            return None
    lines.append(cur)
    return lines if len(lines) <= 2 else None


def _card_room(w, h):
    """The icon's box and the label's width. Icon and padding scale with
    the card's width as well as its height: the 9:16 rows are tall, and
    sized off the height the icon ate the label's room."""
    u = min(h, w * 0.42)
    ib = int(u * 0.42)
    return ib, w - u * 0.14 - ib - u * 0.12 - u * 0.10


def _cover_card(W, H, box, label, emoji, col, size, blur=0.0):
    """One of the video's tier cards (`beats.tiers`) at cover size, on its
    own layer: the dark card, the row's colour round it, the icon and the
    label, at the one `size` every card on the cover shares."""
    from PIL import Image, ImageDraw, ImageFilter
    from video_automation.core.vertical import emoji_image
    from video_automation.longform.beats.base import _font
    x, y, w, h = box
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay, "RGBA")
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(h * 0.14),
                        fill=(24, 16, 32, 240), outline=col + (200,),
                        width=max(2, h // 40))
    ib, room = _card_room(w, h)
    u = min(h, w * 0.42)
    g = emoji_image(emoji, ib)
    if g.width > ib:
        g = g.resize((ib, max(1, int(g.height * ib / g.width))), Image.LANCZOS)
    lay.alpha_composite(g, (int(x + u * 0.14 + (ib - g.width) / 2),
                            int(y + (h - g.height) / 2)))
    tx = x + u * 0.14 + ib + u * 0.12
    f = _font(size)
    lines = _card_lines(label, room, size) or [label]
    lh = size * 1.12
    ty = y + h / 2 - lh * len(lines) / 2
    for k, line in enumerate(lines):
        d.text((tx, ty + k * lh), line, font=f, fill=(245, 245, 245, 255))
    if blur:
        lay = lay.filter(ImageFilter.GaussianBlur(blur))
    return lay


def _board_cover(W, H, portrait):
    """Four graded rows holding the video's own labelled cards (the editor,
    2026-11-20: "change the emojis with the cubes from the video with the
    text"), two sharp per row and a third peeking blurred where the row
    holds more; the top row empty with a "?"."""
    from PIL import Image, ImageDraw
    from video_automation.longform.beats.base import _display
    im = _ground(W, H)
    # Rows on their own layer: drawing translucent fills straight onto an
    # RGBA image replaces its alpha instead of blending, and every row came
    # out solid - the top row's "?" vanished into its own yellow.
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    rows = [("STRONG", (255, 204, 102), []),
            ("YES", TINNITUS.positive,
             [("Hearing aids", "\U0001F9BB"), ("CBT", "\U0001F4AC"),
              ("Implant check", "\U0001F442")]),
            ("MAYBE", TINNITUS.primary,
             [("Sound enrichment", "\U0001F30A"), ("Bimodal devices", "\U0001F3A7")]),
            ("NO", TINNITUS.negative,
             [("Supplements", "\U0001F48A"), ("Magnetic stimulation", "\U0001F9F2"),
              ("Medicines", "\U0001F489")])]
    if portrait:
        x0, top, row_h, gap, block_w, lab = 40, 700, 250, 22, 250, 46
    else:
        x0, top, row_h, gap, block_w, lab = 600, 40, 150, 12, 180, 32
    x1 = W - (40 if portrait else 30)
    f = _display(lab)
    for i, (name, col, cards) in enumerate(rows):
        y = top + i * (row_h + gap)
        d.rounded_rectangle([x0, y, x1, y + row_h], radius=22,
                            fill=col + (34,), outline=col + (120,), width=3)
        d.rounded_rectangle([x0, y, x0 + block_w, y + row_h], radius=22,
                            fill=col + (255,))
        d.text((x0 + block_w / 2, y + row_h / 2), name, font=f,
               fill=(22, 14, 30, 255), anchor="mm")
    im.alpha_composite(layer)
    pad = 14 if not portrait else 18
    tx0 = x0 + block_w + pad
    cw = int((x1 - tx0 - 2 * pad) / 2.2)
    ch = row_h - 2 * pad
    # One label size for every card: the largest that sets each sharp card's
    # label in two lines (a single long word, "Supplements", decides it).
    _, room = _card_room(cw, ch)
    size = next(z for z in range(int(min(ch * 0.30, 48)), 10, -1)
                if all(_card_lines(l, room, z) for _, _, c in rows
                       for l, _ in c[:2]))
    for i, (name, col, cards) in enumerate(rows):
        y = top + i * (row_h + gap)
        if not cards:
            qf = _display(int(row_h * 0.78))
            ImageDraw.Draw(im).text((tx0 + (x1 - tx0) / 2, y + row_h / 2), "?",
                                    font=qf, fill=(255, 204, 102, 255), anchor="mm")
            continue
        for k, (label, emoji) in enumerate(cards):
            cx = tx0 + k * (cw + pad)
            card = _cover_card(W, H, (cx, y + pad, cw, ch), label, emoji, col,
                               size, blur=6.0 if k >= 2 else 0.0)
            if k >= 2:
                # Clip the peeking card to the row, so it reads as more
                # cards further along rather than one falling off the board.
                mask = Image.new("L", (W, H), 0)
                ImageDraw.Draw(mask).rounded_rectangle(
                    [x0, y, x1 - 3, y + row_h], radius=22, fill=255)
                a = card.getchannel("A")
                card.putalpha(Image.composite(a, mask, mask).point(
                    lambda v: int(v * 0.75)))
            im.alpha_composite(card)
    return im


def cover(kind: str, portrait: bool = False):
    """One cover, 1280x720 or (`portrait`) 1080x1920, as an RGB image.

    `tiers`: the guideline's grades as a tier board holding the video's
    labelled cards, the top row empty with a "?" - TINNITUS [TOP TIER?]. The title says ranked;
    the cover asks what reached the top, which the video answers last."""
    from PIL import Image
    from video_automation.longform import thumb as T
    W, H = (1080, 1920) if portrait else (1280, 720)
    fill, ink = T.ACCENTS["red"]
    head = COVER_HEADLINES[kind]
    if kind == "tiers":
        im = _board_cover(W, H, portrait).convert("RGB")
        # The headline's box ends where the board starts, with a gutter, so
        # the text can never run into it (the first cut's plate did).
        box = (60, 200, W - 120, 470) if portrait else (34, 60, 600 - 34 - 30, 600)
        T.stack_headline(im, head, box)
        return im
    raise ValueError(f"unknown cover {kind!r} - {COVERS}")


def thumbs(out: Path, portrait: bool = False, variants: bool = False) -> list[Path]:
    """The picked cover (the first of COVERS) at `out`, and nothing else;
    `variants=True` (`--thumb-variants`) writes the other directions as
    `-<style>` beside it, for choosing."""
    cover(COVERS[0], portrait).save(out, quality=92)
    made = [out]
    if variants:
        for k in COVERS[1:]:
            q = out.with_name(f"{out.stem}-{k}{out.suffix}")
            cover(k, portrait).save(q, quality=92)
            made.append(q)
    return made


def main() -> None:
    stillclip.make(GUIDE, focus=(0.62, 0.40))
    out = Path.home() / "Desktop/tinnitus-treatments-ranked-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-treatments-ranked-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # A ranking is two sides of one question; the answer stays open
        # until the board fills (no `winner=`). Not three running: the last
        # three tinnitus article long forms opened Search, Search, Split.
        opener=Split("Recommended", "Advised against", "Which side is yours on?",
                     enter_word="grades"),
        emphasis=["for tinnitus itself", "Not one treatment", "the person"],
        thumb_headline=THUMB_HEADLINE, thumb_image=GUIDE,
        thumb_accent="red",
    )
    made["thumb"] = thumbs(Path(made["thumb"]))[0]
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv or "--thumb-variants" in sys.argv:
        for q in thumbs(Path.home() / "Desktop/tinnitus-treatments-ranked-long-thumb.jpg",
                        variants="--thumb-variants" in sys.argv):
            print(q)
    else:
        main()
