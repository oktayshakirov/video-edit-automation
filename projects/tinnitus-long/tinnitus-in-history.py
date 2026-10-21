"""The history of tinnitus - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tinnitus-in-history.mdx.

**Why this post, and why it is the rare easy one to picture.** Every other
video on this channel fights the same problem: tinnitus cannot be
photographed. A history can. The Ebers Papyrus, Hippocrates, a chart of the
four humours, a Chinese acupuncture woodcut, Vesalius's *Fabrica* and a
Victorian ear trumpet are all public domain or CC BY on Wikimedia Commons
(Wellcome Collection, mostly), so every named thing in the script is on
screen as itself - `footage.md`, "When the subject is a real thing". Stock
carries the motion (a temple at night, incense, candles, a quill) and the
real pictures ride over it as insets, or fill the frame when they are
landscape and large enough. Credits in `assets/tinnitus/history/CREDITS.md`.

**The title is the search.** "History of tinnitus" is the phrase. The Short
takes the teasing angle ("Is tinnitus a modern problem?").

**The spine, and the twist.** Every age heard the same sound and blamed
something different - spirits, humours, too much air, blocked energy, a
message from God - and almost every remedy went *into the ear*. The twist
is the modern answer: much of the sound is shaped further along, in the
brain. `timeline` makes it visible: 3,500 years of guesses, and the science
in the last sliver of the line.

**Fact-checked, not copied.** Cut from the article: Julius Caesar (the
article's own "definitive historical proof is elusive"), Cardano (no source
I could tie to tinnitus), Pythagoras (philosophy of sound, not ear noises),
Ginkgo (the post still carries a generator's "if discussed in your nutrition
article" note), and Vesalius drawing the cochlea (his ear plates are of the
middle ear; the script says "the body as it is"). Added from the post's own
description, which promises it and whose body never delivers: the name is
from a Latin verb meaning to ring.

**The beats.** The last three long forms ran
`dial`/`diagram`/`bars`/`compare`/`steps` (stress), and
`anatomy`/`checklist`/`chapter`/`steps`/`grid` (tmj). Four here, and the
real pictures do the rest:

- `quote` - "A humming in the ear", the Ebers page in the picture column.
- `grid` - the five culprits, no icons (`beats.md`: five is better bare).
- `timeline` - c. 1550 BC to today, spaced by real dates. `Timeline._year`
  learned BC dates for this video; read the old way the papyrus sat at AD
  1550.
- `diagram` - less sound reaching the brain, the brain turning its own
  volume up, a sound that is not there. From the site's
  `what-role-does-the-brain-play-in-tinnitus`. A chain, not a loop.

**The medical line.** A history makes no promise and this one does not
start. Old remedies are described as what people did. The modern tools are
named for what they are built around, never for what they do. The one
routing line is the channel's standing "new or changed ringing - get it
checked", on screen as the voice says it. The post itself carries no red
flags, so none are invented.

**Phonemes**, checked with espeak-ng: Hippocrates, Galen, Celsus, phlegm,
myrrh, frankincense, otology, Vesalius, mistletoe are fine. Respelled in the
spoken half only (`es()`): the years (espeak reads 1543 as "one thousand
five hundred..."), Ayurveda, Vata and Qi (espeak says "kai").

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tinnitus-in-history.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Stamp

SOURCE_POST = "tinnitus-in-history"

ROOT = Path(__file__).resolve().parents[2]
HIST = ROOT / "assets/tinnitus/history"
# Wikimedia Commons, credited in CREDITS.md. Portrait sources go in as insets
# or picture columns, never full frame (`footage.md`).
EBERS_PAGE = HIST / "ebers-page.jpg"                # 2950x3741, L203, 1875 facsimile plate - quote column
EBERS_WIDE = HIST / "ebers-wide.jpg"                # 3840x2837, L194, a second plate - inset
HIPPOCRATES = HIST / "hippocrates-1584.jpg"         # 2400x3034, L137, the 1584 engraving - inset
HUMOURS = HIST / "four-humours.jpg"                 # 3254x2720, L36, the four humours chart - full frame
CELSUS = HIST / "celsus-1465.jpg"                   # 2922x4253, L199, De medicina, 1465 - inset
CHARAKA = HIST / "charaka-samhita.jpg"              # 3462x2726, L150, the Charaka Samhita - full frame
ACUPUNCTURE = HIST / "acupuncture-head.jpg"         # 1984x2976, L154, points on the side of the head - inset
BRONZE = HIST / "ming-bronze.jpg"                   # 3456x5184, L125, CC0, Ming acupuncture figure - inset
HERBAL = HIST / "carrara-herbal.jpg"                # 999x1500, L155, the Carrara Herbal, c. 1400 - inset
VESALIUS = HIST / "vesalius-frontispiece.jpg"       # 1461x2072, L124, Fabrica, 1543 - inset
VESALIUS_P = HIST / "vesalius-portrait.jpg"         # 736x1022, L138, his portrait from the Fabrica - inset
TRUMPET = HIST / "ear-trumpet-horn.jpg"             # 3840x2555, L68, a horn ear trumpet - full frame

V = STOCK / "videos"
# Fetched 2026-10-21, contact-sheeted at 5/35/65/95%. None of these ids is cut
# by another project. Duration, luma, what is in the frame.
EGYPT = V / "ancient-egypt-hieroglyphs-temple-night/7575359.mp4"     # 29.5s, L17-31, a dark carved Egyptian figure, hieroglyphs
STELE = V / "ancient-egypt-hieroglyphs-temple-night/7492692.mp4"     # 22.0s, L95-116, a carved relief, lit. Bright, on the noun
INCENSE = V / "incense-smoke-burning-dark/4584731.mp4"               # 20.0s, L13-14, one stick, smoke on black
INCENSE_H = V / "incense-smoke-burning-dark/6448157.mp4"             # 15.2s, L46-47, a hand holding a burning stick
TEMPLE = V / "greek-temple-columns-night/37903218.mp4"               # 16.8s, L8-13, a Greek temple lit at night, aerial
COLOSSEUM = V / "colosseum-rome-night/4840456.mp4"                   # 11.9s, L59, the Colosseum at night
ARENA = V / "colosseum-rome-night/38405572.mp4"                      # 8.8s, L26-29, its arches lit, wider
MORTAR = V / "mortar-pestle-herbs-dark/5480204.mp4"                  # 20.2s, L112-122, herbs into a mortar. Bright; the act
CANDLES = V / "church-candles-dark/6656868.mp4"                      # 13.8s, L31-32, hands lighting church candles
CANDLEWALL = V / "church-candles-dark/31799466.mp4"                  # 10.9s, L38-40, rows of church candles
QUILL = V / "quill-pen-writing-ink/11137423.mp4"                     # 20.4s, L39-41, a quill writing by a candle
BOOKS = V / "old-anatomy-book/11765182.mp4"                          # 13.8s, L27-37, old leather spines, a red curtain
SHELF = V / "old-anatomy-book/11769112.mp4"                          # 9.2s, L37-43, a hand drawing an old book out
STUDY = V / "old-library-dark-books/10425839.mp4"                    # 11.5s, L21-23, a candle beside an open book
SPARK = V / "electric-spark-dark/35048273.mp4"                       # 10.0s, L15-32, a violet electric discharge
LANTERN = V / "paper-lantern-night-dark/10746313.mp4"                     # 22.3s, L27-30, a paper lantern glowing on black
INKSTONE = V / "chinese-calligraphy-brush-ink/9478320.mp4"               # 11.3s, L110-120, a brush into an inkstone. Bright
PAGES = V / "candle-flame-book-dark/5873673.mp4"                         # 15.9s, L32-33, a candle by an open illustrated book
TAPER = V / "candle-flame-book-dark/6961945.mp4"                         # 9.4s, L35-37, a taper lit beside someone at a desk
LISTEN = V / "woman-listening-headphones-window-night/6688133.mp4"   # 30.4s, L34-36, a woman in headphones, at ease
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/tinnitus-in-history"

# espeak reads a four-digit year as "one thousand five hundred...", Ayurveda
# as "I-er-veda" and Qi as "kai". Respell in the spoken half only; the SRT
# keeps the real spelling.
_RESPELL = {"1550": "fifteen fifty", "1543": "fifteen forty-three",
            "1800s": "eighteen hundreds", "Ayurveda": "Eye-yur-vay-dah",
            "Vata": "Vahta", "Qi": "chee"}


def es(text: str) -> tuple[str, str] | str:
    spoken = text
    for k, v in _RESPELL.items():
        spoken = spoken.replace(k, v)
    return text if spoken == text else (text, spoken)


def S(*chunks: str) -> tuple:
    return tuple(es(c) for c in chunks)


SECTIONS = [
    # --- hook ---------------------------------------------------------------
    Section(
        title="The history of tinnitus",
        card=False,
        sentences=[
            # The subject in sentence one, and the belief the Stamp overturns.
            S("You might think tinnitus is a modern problem."),
            # The Stamp lands on "myth".
            S("It is a myth."),
            S("Three and a half thousand years ago, Egyptian doctors were "
              "already writing about a bewitched ear."),
            S("Since then, every age has heard the same sound, and blamed "
              "something completely different."),
            # The retention promise - paid off in Rome, in the timeline and
            # in the brain section, and echoed in the close.
            S("By the end, you will know where the name comes from, where "
              "almost every old cure went wrong, and where the sound is "
              "really made."),
        ],
        shots=[
            Shot(clip=EGYPT, clip_at=0.5),
            None,                                       # hold the carved face
            Shot(clip=EGYPT, clip_at=9.0, inset=(EBERS_WIDE, "right", 0.30)),
            Shot(clip=INCENSE, clip_at=2.0),
            Shot(clip=QUILL, clip_at=1.0),
        ],
        gaps=[0.45, 0.90, 0.70, 0.80, 0.90],
    ),

    # --- Egypt --------------------------------------------------------------
    Section(
        title="What did the Egyptians blame?",
        spoken_title="So what did the Egyptians think it was?",
        kicker="THE PAPYRUS",
        sentences=[
            S("The oldest record is the Ebers Papyrus, a medical scroll from "
              "around 1550 BC."),
            # quote - one chunk.
            S("It describes a humming in the ear."),
            S("And the explanation was spirits, something foreign that had "
              "got inside."),
            S("So the remedy was to drive it out, with oils, frankincense "
              "and myrrh, often alongside a spell."),
            # The article's own reading: they took it seriously.
            S("It sounds strange now."),
            S("But it means someone, that long ago, took the sound "
              "seriously enough to write it down."),
        ],
        shots=[
            Shot(clip=STELE, clip_at=2.0),
            Shot(graphic="quote", picture=EBERS_PAGE,
                 payload=("A humming in the ear.",
                          "THE EBERS PAPYRUS, c. 1550 BC")),
            Shot(clip=EGYPT, clip_at=18.0),
            Shot(clip=INCENSE_H, clip_at=1.0),
            Shot(clip=INCENSE, clip_at=11.0),
            None,                                       # hold the smoke
        ],
        gaps=[0.70, 1.10, 0.60, 0.80, 0.55, 0.90],
    ),

    # --- Greece and Rome ----------------------------------------------------
    Section(
        title="Was it in the blood?",
        spoken_title="Then the Greeks asked: was it in the blood?",
        kicker="THE HUMOURS",
        sentences=[
            S("Hippocrates, often called the father of medicine, described "
              "ringing in the ears."),
            S("He, and later Galen, blamed an imbalance of the four humours: "
              "blood, phlegm, yellow bile and black bile."),
            S("So the fix was to rebalance them, with diet, exercise, and "
              "sometimes bloodletting."),
            S("Rome took that medicine and kept it."),
            S("The writer Celsus suggested rose extract, dropped into the "
              "ear."),
            # The name - the promise from the hook, paid.
            S("And the word itself comes from Latin: tinnitus, from a verb "
              "that means to ring."),
            S("A Roman soldier, standing in the noise of battle, may well "
              "have gone home ringing, with no record of it at all."),
        ],
        shots=[
            Shot(clip=TEMPLE, clip_at=1.0, inset=(HIPPOCRATES, "right", 0.24)),
            Shot(image=HUMOURS, zoom=1.08, pan=(0.0, -0.01)),
            Shot(clip=MORTAR, clip_at=3.0),
            Shot(clip=COLOSSEUM, clip_at=1.0),
            Shot(clip=STUDY, clip_at=1.0, inset=(CELSUS, "right", 0.22)),
            # The one payload in the section: the word on screen as it is
            # explained.
            Shot(clip=QUILL, clip_at=9.0,
                 payload=("", "tinnire: to ring")),
            Shot(clip=ARENA, clip_at=0.5),
        ],
        gaps=[0.60, 0.70, 0.85, 0.55, 0.70, 0.85, 0.90],
    ),

    # --- India and China ----------------------------------------------------
    Section(
        title="What did the East see in it?",
        spoken_title="And further east, what did they see in it?",
        kicker="THE ENERGY",
        sentences=[
            S("In India, Ayurveda gave the ear noises a name of their own."),
            S("It blamed too much Vata, the body's energy of air and "
              "movement."),
            S("So warm herbal oils went into the ear, alongside cleansing "
              "and a change of diet."),
            S("In China, the explanation was blocked Qi, the energy said to "
              "flow through the body."),
            S("The ears were thought to depend on the kidneys, so "
              "acupuncture and herbs aimed to get that flow moving again."),
        ],
        shots=[
            Shot(image=CHARAKA, zoom=1.08, pan=(0.01, 0.0)),
            None,                                       # hold the manuscript
            Shot(clip=MORTAR, clip_at=12.0),
            Shot(clip=LANTERN, clip_at=1.0, inset=(ACUPUNCTURE, "right", 0.22)),
            Shot(clip=INKSTONE, clip_at=1.0, inset=(BRONZE, "right", 0.18)),
        ],
        gaps=[0.55, 0.70, 0.85, 0.60, 0.90],
    ),

    # --- Medieval Europe ----------------------------------------------------
    Section(
        title="A message from God?",
        spoken_title="But in medieval Europe, was it a message from God?",
        kicker="THE OMEN",
        sentences=[
            S("For some, it was."),
            S("A ringing in the ears could be read as a sign from heaven, "
              "or a warning."),
            S("Monks kept the old herbal remedies alive, with plants like "
              "mistletoe and plantain."),
            # The hinge into the turn.
            S("And then the whole story changed, with a book of drawings."),
        ],
        shots=[
            Shot(clip=CANDLES, clip_at=1.0),
            Shot(clip=CANDLEWALL, clip_at=1.0),
            Shot(clip=BOOKS, clip_at=1.0, inset=(HERBAL, "right", 0.22)),
            Shot(clip=SHELF, clip_at=0.5),
        ],
        gaps=[0.60, 0.80, 0.70, 0.90],
    ),

    # --- Vesalius to otology ------------------------------------------------
    Section(
        title="When did it become science?",
        spoken_title="So when did tinnitus become a question for science?",
        kicker="THE TURN",
        sentences=[
            S("In 1543, the anatomist Andreas Vesalius published the most "
              "detailed atlas of the human body anyone had seen."),
            S("For the first time, doctors could study the ear as it really "
              "is, instead of guessing."),
            S("By the 1800s, the ear had a medical field of its own, called "
              "otology."),
            S("Doctors tried syringing, electric currents, and the first "
              "hearing devices."),
        ],
        shots=[
            Shot(clip=PAGES, clip_at=1.0, inset=(VESALIUS, "right", 0.24)),
            Shot(clip=STUDY, clip_at=3.0, inset=(VESALIUS_P, "right", 0.22)),
            Shot(clip=SHELF, clip_at=4.0),
            Shot(image=TRUMPET, zoom=1.08, pan=(-0.01, 0.0)),
        ],
        gaps=[0.70, 0.85, 0.60, 0.90],
    ),

    # --- the twist ----------------------------------------------------------
    Section(
        title="Where were they all looking?",
        spoken_title="But where were they all looking?",
        kicker="THE TWIST",
        sentences=[
            # grid - one chunk per culprit.
            S("Spirits.", "Bad humours.", "Too much air.", "Blocked energy.",
              "A message from God."),
            S("Five explanations, and almost every remedy went into the "
              "ear."),
            # The hinge into the timeline.
            S("Put the whole story on one line, and something stands out."),
            # timeline - one chunk per event.
            S("A bewitched ear, around 1550 BC.",
              "The four humours, a thousand years later.",
              "The body, drawn as it is, in 1543.",
              "And only in our own time, the brain."),
            S("For almost all of that line, people were guessing."),
        ],
        shots=[
            Shot(graphic="grid",
                 payload=([("Spirits", "Egypt"),
                           ("Bad humours", "Greece and Rome"),
                           ("Too much air", "India"),
                           ("Blocked energy", "China"),
                           ("A message from God", "medieval Europe")],
                          "WHAT EACH AGE BLAMED")),
            Shot(clip=INCENSE_H, clip_at=8.0),
            Shot(clip=QUILL, clip_at=15.0),
            Shot(graphic="timeline",
                 payload=([("c. 1550 BC", "A bewitched ear"),
                           ("c. 400 BC", "The four humours"),
                           ("1543", "The body, drawn"),
                           ("Today", "The brain")],
                          "3,500 YEARS OF ONE SOUND")),
            Shot(clip=LANTERN, clip_at=12.0),
        ],
        gaps=[1.20, 0.80, 0.80, 1.20, 0.90],
    ),

    # --- the brain ----------------------------------------------------------
    Section(
        title="Where is the sound really made?",
        spoken_title="So where is the sound really made?",
        kicker="THE ANSWER",
        sentences=[
            S("Today, research points further along, to the brain."),
            # diagram - one chunk per node.
            S("When less sound reaches it,",
              "the brain can turn up its own volume,",
              "and a sound can appear that is not really there."),
            S("That is why pouring something into the ear so rarely reached "
              "it."),
            S("So the tools today are built around the brain's side of it: "
              "sound therapy, hearing aids, and talking therapy."),
        ],
        shots=[
            Shot(clip=SPARK, clip_at=2.0),
            Shot(graphic="diagram",
                 payload=([("Less sound arrives", "from the ear", "\U0001F442"),
                           ("The brain turns it up", "its own volume",
                            "\U0001F9E0"),
                           ("A sound appears", "that is not there",
                            "\U0001F514")],
                          "WHERE THE RINGING IS MADE", False)),
            Shot(clip=TAPER, clip_at=1.0),
            Shot(clip=LISTEN, clip_at=4.0),
        ],
        gaps=[0.80, 1.20, 0.80, 0.90],
    ),

    # --- close: echo the opening, then the question --------------------------
    Section(
        title="Back to that papyrus",
        spoken_title="So, back to that papyrus.",
        sentences=[
            S("Three and a half thousand years, and the sound has not "
              "changed."),
            S("What changed is where we look for it."),
            # The channel's standing routing line, on screen as it is said -
            # on the notice card (the NOTICE kicker), not the statement band.
            S("If your own ringing is new, or has changed, it is worth "
              "getting your hearing checked."),
            S("And if you could ask that Egyptian doctor one question, what "
              "would it be?"),
        ],
        shots=[
            Shot(clip=EGYPT, clip_at=22.0),
            Shot(clip=LISTEN, clip_at=16.0),
            Shot(clip=CANDLEWALL, clip_at=0.5,
                 payload=("NOTICE", "New ringing, or ringing that changed? "
                              "Get it checked.")),
            Shot(clip=STELE, clip_at=12.0),
        ],
        gaps=[0.80, 0.90, 0.90, 3.00],
    ),
]

META = Meta(
    title="The History of Tinnitus: 3,500 Years of Ringing Ears",
    hook="Tinnitus is not a modern problem. Three and a half thousand years "
         "ago, Egyptian doctors were already writing about a bewitched ear, "
         "and every age since has heard the same sound and blamed something "
         "different - spirits, humours, blocked energy, a message from God. "
         "Here is the whole history, where the name comes from, and where "
         "the sound is really made.",
    url=URL,
    summary="The history of tinnitus from the Ebers Papyrus to today: the "
            "Egyptian bewitched ear, Hippocrates and the four humours, "
            "Celsus in Rome, Ayurveda and Traditional Chinese Medicine, "
            "medieval omens and herbs, Vesalius in 1543, the birth of "
            "otology, and the modern understanding of the brain's role.",
    tags=["history of tinnitus", "tinnitus history", "tinnitus in history",
          "ancient tinnitus", "ancient tinnitus treatment", "ebers papyrus",
          "hippocrates tinnitus", "where does the word tinnitus come from",
          "tinnitus", "ringing in ears"],
    cta=f"The full article: {URL}",
    credits=["Images via Wikimedia Commons. Ebers Papyrus plates, "
             "Hippocrates engraving (1584), the four humours chart, the "
             "Charaka Samhita, a Chinese acupuncture woodcut and a horn ear "
             "trumpet: Wellcome Collection, CC BY 4.0. Celsus, De medicina "
             "(1465), Bayerische Staatsbibliothek; the Carrara Herbal; "
             "Vesalius, De humani corporis fabrica (1543): public domain. "
             "Ming bronze acupuncture figure: CC0.",
             "",
             "This video is general history, not medical advice. If your "
             "ringing is new, has changed, or comes with hearing loss or "
             "dizziness, please see a doctor or an audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-in-history-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-in-history-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=11.5, title_hold=5.4,
        # A belief to overturn, and a claim rather than an outcome - the
        # channel's limit on a verdict stamp. Shared with the Short.
        opener=Stamp("Tinnitus is a modern problem", "MYTH", at_word="myth"),
        # The Hippocrates engraving: a real face from history.
        # The Short's own question, so the pair reads as one (the user's
        # call on the first cut).
        thumb_headline="Is tinnitus\na modern\n[problem?]",
        thumb_image=HIPPOCRATES, thumb_accent="orange",
        thumb_crop_at=(0.55, 0.30), thumb_crop_zoom=0.70, thumb_side="left",
        # Three rows reach his face at no shift; 0.28 clears it.
        thumb_shift=0.28,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
