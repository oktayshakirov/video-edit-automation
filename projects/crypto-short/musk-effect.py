"""Can one post move a crypto price? ~47s crypto short.

Source: crypto-wiki/content/crypto-ogs/elon-musk.mdx - the same page as the
`musk-effect` long form, written in the same pass. There is no `posts/` article
for this, so `SOURCE_POST` is None and the OG bio is the source of every fact.

**The angle, and the one it deliberately refuses.** The obvious Elon video is a
profile: what he said, when, and what it did to a price. That video is a
direction claim wearing a story, and this channel does not make those. So the
pair takes the mechanism the bio's "Musk Effect" section rests on and never
states - **a post is not a purchase**. Nothing about a coin changes when a post
lands; what changes is how many people reach the same short queue of offers in
the same few minutes. That is a fact about market depth, not about the man, and
it is the one framing under which this topic is safe *and* more interesting.

**The single move.** The long form walks the order book, the fade, the 2021
sequence in both directions, and why depth decides the size of the reaction.
The Short does the one thing all of that rests on: the supply, the code and
what the coin can do are all unchanged, and only the number of people watching
moved.

**He is in the cut and on the thumbnail, at the user's direction** (the first
pass had neither, on the reasoning that the subject is a queue of offers).
The constraint that survives is licensing, not taste: a portrait of a named
individual comes from **Wikimedia Commons**, screened and credited in
`assets/crypto/musk/CREDITS.md`. **There is no usable video of him** - Commons'
only non-political clips are 500x374, a 3.8x upscale to fill a frame, so the
motion here is a Ken Burns move on a still. One portrait, placed under the
line that actually names him, rather than a face in every slot: the argument
is still the queue, and the other eight shots still carry it.

**Opener: statement mode, not a redaction.** The surprise is the proposition -
a post buys nothing and the price moves anyway - not a token inside a sentence,
which is exactly when `shorts.md` says to drop the brackets. A redaction here
would fail the cover-the-bar test twice over: "A post is not a [purchase]" is
handed to you by the grammar. The last three shorts on this channel ran
`Stamp` (whale), a redacted hook (scams) and no opener (satoshi), so statement
mode is also the rotation.

**Sentence 2 is a partial answer** (`narration.md`, revised 2026-09-21): "it
can, and nothing about the coin itself has to change" is new, true, and opens
the bigger question - then what *does* change? - instead of closing the loop at
five seconds.

**Two beats, two silhouettes, neither in the last three shorts.** `diagram`
without the loop (the chain from a post to the number on screen) and
`checklist` two-phase (what did not change). whale ran `split` + `steps`,
scams ran `grid` + `chapter`, satoshi ran `chapter` + `diagram` - this
diagram is the straight chain against that one's, and the pair's long form
takes the *looped* version, so the two files never draw the same object.

**The checklist is two-phase, not `flow`.** The narration reads three bare
claims with no verdict attached to any of them ("The supply. The code.") and
then reacts once on the fourth chunk, which is the shape `beats.md` says
`flow=False` is for. Its title is the question its marks answer, so no item has
to be interpreted against a noun-phrase heading.

**Cold close, no question** (`narration.md`, "A Short's ending loops"). The
last line answers the opening question instead of re-asking it, and `outro=`
holds it to the final frame so the piece loops into its own first frame.

**No disclaimer** - the long form carries it and shorts on this channel drop
it. **No financial advice:** no price, no level, no prediction, no coin named
as a thing to hold or avoid, and no claim about what any post will do next.
Every figure is structural, so nothing here can date.

**Clips** are the pair's own fetch - nothing in the cut is an asset another
crypto video already uses, and each clip appears exactly once here. No live
price, chart, ticker or broker name appears in any of them.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/musk-effect.py
"""

from pathlib import Path
from pathlib import Path as _P

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb

# No `posts/` article - the source is the crypto-og bio.
SOURCE_POST = None
SOURCE_OG = "elon-musk"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Screened across their length, then looked at on a labelled contact sheet.
# The trailing comment is the luma/saturation range over the whole clip. Eight
# candidates that passed the luma box were cut on the sheet: a green messaging
# UI legible on screen, an Instagram feed with the brand on it, a gavel that
# reads as a courtroom, red wine, a DAW timeline, a face in a cinema seat, and
# two near-empty frames (a moon on black, a distant moth).
DOMINOS = V / "domino-chain-falling-dark-background/9760429.mp4"         # 21s, L32-40 S8-13, a standing line of dominoes on a dark table
GATES = V / "turnstile-subway-gate-night/35722252.mp4"                  # 18s, L24-28 S23-29, a gateline of turnstiles, amber
ARENA = V / "audience-silhouettes-auditorium-dark/36499729.mp4"         # 37s, L30-33 S22-23, an arena of phone lights in the dark
STADIUM = V / "empty-stadium-seats-night-dark/19205377.mp4"             # 10s, L18-19 S3-4, empty stands under floodlights
CASCADE = V / "domino-chain-falling-dark-background/38003914.mp4"       # 10s, L11-17 S16-23, gold dominoes toppling on black

# Portraits of a named individual come from Wikimedia Commons, not stock.
# Screened and credited in `assets/crypto/musk/CREDITS.md`.
MUSK = ROOT / "assets/crypto/musk"
MIC = MUSK / "elon-musk-33377877458.jpg"                                # 4318x2879 r1.50, L45 S26, at a microphone - CC BY 2.0
ARMS = MUSK / "elon-musk-april-2022.jpg"                                # 2428x2636 r0.92, arms crossed - public domain

THUMB = ARMS
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly. A Short arrives with no title card and no
    # thumbnail on screen, so the first line is what turns the next forty
    # seconds into an answer somebody is waiting for.
    ("Can one post really move a crypto price?",),

    # The partial answer: true, new, and it opens the bigger question rather
    # than closing the loop.
    ("It can.",
     "And nothing about the coin itself has to change for that to happen."),

    ("People call it the Musk effect.",
     "But the mechanism is not the man."),

    ("A price is only the last offer somebody actually filled.",),

    # The diagram's own sentence - one chunk per node, plus a trailing
    # reaction chunk, which claims no reveal slot.
    ("A post reaches millions of people at once.",
     "A few of them buy inside the same few minutes.",
     "They take the cheapest offers, one after another.",
     "Nobody had to believe anything - they only had to arrive together."),

    # Hinge into the checklist. Its own sentence, because a leading hinge
    # inside the beat's span eats reveal zero.
    ("Now look at what never changed.",),

    # The checklist's own sentence - one chunk per item. The first three are
    # bare claims with no verdict spoken, so the marks land together in the
    # pause after the last one. That is two-phase, not `flow`.
    ("The supply.",
     "The code.",
     "What the coin can actually do.",
     "How many people were watching at once - that is the only thing that moved."),

    # Cold close. It answers the opening question instead of re-asking it, so
    # the viewer's last thought and first thought are the same thought.
    ("A post is not a purchase.",
     "It only changes who shows up."),
]

SHOTS = [
    # **The opening slot was re-cast after looking at the real 9:16 crop**, not
    # the landscape frame. A phone-on-a-table clip was here first and the
    # vertical crop is a wooden table with a sliver of phone edge - the exact
    # "cropping the main part and showing the empty part" fault `shorts.md`
    # records. This is the most legible frame in the roster: the stands are
    # dark where the hook band sits and the phone lights fill the lower half,
    # so the picture says "everyone looking at one thing" in the one second
    # that decides the swipe.
    Shot(clip=ARENA, clip_at=2.0, clip_ax=0.50),
    Shot(clip=DOMINOS, clip_at=1.0, clip_ax=0.50),
    # He is the shot under the line that names him. **`aspect` is the
    # source's own ratio**, so the crop is a no-op and the face is
    # letterboxed into the blurred fill rather than cut into - the default
    # 1.15 crop target takes the top of the head off, and `bias` cannot fix
    # that because it only slides the same-sized window.
    Shot(image=MIC, aspect=4318 / 2879, zoom=1.06),
    # 9.5s, not 1.0s: at the head of the clip the vertical crop is one hooded
    # back filling the frame. Here somebody is actually passing through the
    # gateline, which is the noun the sentence says.
    Shot(clip=GATES, clip_at=9.5, clip_ax=0.40),
    Shot(graphic="diagram", backdrop=BEATGROUND,
         payload=([("A post lands", "millions read it in one minute"),
                   ("They arrive together", "inside the same few minutes"),
                   ("The queue empties", "the cheapest offers go first"),
                   ("The number moves", "and everybody sees it")],
                  "WHAT A POST ACTUALLY DOES", False)),
    Shot(clip=STADIUM, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="checklist", backdrop=BEATGROUND,
         payload=([("The supply", False),
                   ("The code", False),
                   ("What it can do", False),
                   ("How many were watching", True)],
                  "DID ANY OF THIS CHANGE?")),
    Shot(clip=CASCADE, clip_at=0.5, clip_ax=0.50),
]

# 2.20 on the checklist buys the silence its verdicts land in; 1.30 on the
# diagram gives four nodes room to be read.
GAPS = [0.70, 0.90, 0.85, 0.90, 1.30, 0.70, 2.20, 1.30]


def main() -> None:
    out = Path.home() / "Desktop/musk-effect-short.mp4"
    work = Path.home() / "Desktop/.musk-effect-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # Statement mode: no brackets. The surprise is the proposition, and
        # any word worth hiding here is handed to you by the sentence's own
        # grammar - the cover-the-bar test in `shorts.md`.
        hook="A post is not a purchase",
        outro="A post is not a purchase. It only changes [who shows up].")
    # A pair shares its thumbnail. Four short forced rows and a raised size:
    # the size search is capped by the longest row, so short rows clear the
    # column early and it keeps climbing. `[queue]` sits on its own row, which
    # is what gives the accent plate room from the word in front of it.
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "This is\nthe [Musk]\neffect",
        image=THUMB, accent="yellow", band="bottom", size=240, at=0.30)
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
