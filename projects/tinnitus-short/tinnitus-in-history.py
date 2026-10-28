"""Is tinnitus a modern problem? ~45s Short.

Source: tinnitus-blog/content/posts/tinnitus-in-history.mdx, the same post as
the `tinnitus-in-history` long form.

**Sentence two overturns the title, plainly, and opens the next question.**
"That is a myth, and the oldest record of it is three and a half
thousand years old." answers the yes/no title with a *no*, which is the one case
`narration.md` ("Confirmed 2026-10-11") lets a yes/no title answer itself:
a reversal - and opens the next question in the same sentence: a record of
what, and what did they make of it? That is what the rest of the Short pays off.

**Not the long form compressed, and not only its twist.** The 2026-10-13 rule
(a twist-only Short is a sum) applies: the Short runs the plain story in the
order a viewer would ask it - how old, what each age blamed, where it is
really made - with a real picture for each age and one drawn beat.

**Opener: the long form's `Stamp`.** A pair may share its opener
(`shorts.md`, 2026-10-20). The last three tinnitus article Shorts opened on
Split, the hook and Counter, so a Stamp is also the rotation. MYTH is about
a claim ("tinnitus is a modern problem"), never an outcome.

**One drawn beat, and it is not `grid` or `steps`.** `diagram`, the brain
turning its own volume up, from the long form. The ages are carried by their
own pictures (Ebers plate, Hippocrates, the acupuncture woodcut), which in
9:16 are framed cards - all three are portrait sources.

**A cold close** that recontextualises the opener: it opens on "a modern
problem?" and ends on "a modern explanation". No question.

**No medical claims.** Nothing here says what helps. The routing line lives
in the long form and the description.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-in-history.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "tinnitus-in-history"

ROOT = Path(__file__).resolve().parents[2]
HIST = ROOT / "assets/tinnitus/history"
EBERS_PAGE = HIST / "ebers-page.jpg"
HIPPOCRATES = HIST / "hippocrates-1584.jpg"
ACUPUNCTURE = HIST / "acupuncture-head.jpg"

# Same roster as the long form - a pair is one video. A Short runs under a
# minute, so no clip appears twice in it.
V = STOCK / "videos"
EGYPT = V / "ancient-egypt-hieroglyphs-temple-night/7575359.mp4"
STELE = V / "ancient-egypt-hieroglyphs-temple-night/7492692.mp4"
INCENSE = V / "incense-smoke-burning-dark/4584731.mp4"
CANDLES = V / "church-candles-dark/6656868.mp4"
QUILL = V / "quill-pen-writing-ink/11137423.mp4"
SPARK = V / "electric-spark-dark/35048273.mp4"
LISTEN = V / "woman-listening-headphones-window-night/6688133.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")

# espeak would say "kai" for Qi and read years as thousands; neither is said
# here, so no respelling is needed.
OPENER = Stamp("Tinnitus is a modern problem", "MYTH", at_word="myth")

OUTRO = "Not a modern problem. A modern [explanation]."

SENTENCES = [
    # The title question.
    ("Is tinnitus a modern problem?",),
    # The reversal. The Stamp lands on "myth".
    ("That is a myth, and the oldest record of it is three and a half "
     "thousand years old.",),
    ("An Egyptian papyrus was already describing a humming in the ear.",),
    ("They blamed spirits, and put frankincense and myrrh in the ear to "
     "drive them out.",),
    ("The Greeks blamed the body's four humours, and tried bloodletting.",),
    ("In China, it was blocked energy, treated with acupuncture.",),
    ("In medieval Europe, it could be a sign from heaven.",),
    ("Same sound, every time. A different culprit.",),
    # The hinge into the diagram, its own sentence so it cannot eat reveal 0.
    ("Only in our own time did the answer move to the brain.",),
    # diagram - one caption chunk per node.
    ("When less sound reaches it,",
     "the brain can turn up its own volume,",
     "and a sound can appear that is not there."),
    # The cold close, drawn by `outro=`.
    ("Not a modern problem. Just a modern explanation.",),
]

GAPS = [0.70,   # into the reversal
        0.85,   # the stamp lands
        0.60,
        0.55,
        0.55,
        0.55,
        0.80,   # before the turn
        0.85,   # into the hinge
        0.70,
        1.00,   # the diagram closes
        0.34]   # cold close, nothing after it

SHOTS = [
    # The carved face sits low in the frame, clear of the stamp at 34%.
    Shot(clip=EGYPT, clip_at=0.5, clip_ax=0.30),
    # Not the same clip twice in a row (`shorts.md`): the carved relief.
    # At 0.45 the crop held only a hand and a staff (the editor's note on the
    # first cut); 0.88 is the carved figure's head and shoulders.
    Shot(clip=STELE, clip_at=2.0, clip_ax=0.88),
    # The plate is near-white, and a full card put the karaoke line on a
    # white page. As an inset at the top it stays clear of the caption.
    Shot(clip=EGYPT, clip_at=12.0, clip_ax=0.50, inset=(EBERS_PAGE, "top", 0.50)),
    Shot(clip=INCENSE, clip_at=2.0, clip_ax=0.55),
    Shot(image=HIPPOCRATES, aspect=2400 / 3034, zoom=1.04),
    Shot(image=ACUPUNCTURE, aspect=1984 / 2976, zoom=1.04),
    Shot(clip=CANDLES, clip_at=1.0, clip_ax=0.60),
    Shot(clip=QUILL, clip_at=1.0, clip_ax=0.70),
    Shot(clip=SPARK, clip_at=2.0, clip_ax=0.50),
    Shot(graphic="diagram",
         payload=([("Less sound arrives", "from the ear", "\U0001F442"),
                   ("The brain turns it up", "its own volume", "\U0001F9E0"),
                   ("A sound appears", "that is not there", "\U0001F514")],
                  "WHERE THE RINGING IS MADE", False)),
    # The outro card lands on this one and holds to the final frame.
    Shot(clip=LISTEN, clip_at=4.0, clip_ax=0.45),
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-in-history-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-in-history-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, outro=OUTRO,
                                        tail=2.0)

    # The long form's Hippocrates engraving, a real face from history; the
    # type sits low, under his face.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Is tinnitus\na modern\n[problem?]", image=HIPPOCRATES,
        accent="orange", ax=0.55, zoom=1.0, at=0.35, band="bottom", size=230)

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
