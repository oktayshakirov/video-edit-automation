"""He built digital money five years before Bitcoin - ~47s crypto short.

Source: crypto-wiki/content/crypto-ogs/hal-finney.mdx - the same page as the
`first-bitcoin-transaction` long form, written in the same pass. There is no
`posts/` article for this, so `SOURCE_POST` is None and the OG bio is the
source of every fact except the one noted below.

**The angle, and the one it refuses.** The obvious Hal Finney short is "was he
Satoshi?" - and `satoshi-nakamoto` already runs him as a struck item in its
candidates checklist, so that short would be this channel arguing the same
evidence list a third time. What is left is the mechanism: he is the one
person who sits on both sides of Bitcoin's central claim, because he built the
version that still needed a middleman.

**The single move.** The long form walks day one, who he was, why digital cash
kept failing, and what block 170 settled. The Short does the one thing all of
that rests on: **his own digital money worked, and it still ran every transfer
past one machine you had to trust.** The first Bitcoin payment is the same
sequence with that machine taken out.

**Opener: a redacted hook, and the token is a duration.** `shorts.md`'s
cover-the-bar test: "He built digital money ___ before Bitcoin" cannot be
filled in from the sentence's own grammar - a duration is one of the classes
the test passes, unlike the direction words this channel used to redact.
Sentence 2 says "five years" in its first five words, so the reveal lands
around three seconds rather than sitting in a holding pattern. Rotation: the
last three shorts here ran `Search` (musk), `Stamp` (whale) and a redacted
hook (scams), so this is the oldest of the three in use.

**Sentence 2 is a partial answer, not the verdict** (`narration.md`, revised
2026-09-21). "A cryptographer who, five years earlier, had already built
digital money of his own" is new, true, and opens the bigger question - then
why did his fail? - rather than closing the loop at five seconds. There is no
self-check to hand the viewer here, which is the stronger option the same doc
prefers; a crypto history has no task to perform, so this is the reversal case.

**Two beats, two silhouettes.** `steps` (4 nodes, the full-width track) and
`stat` (the column with its emblem). The last three shorts ran diagram / chart
/ checklist (musk), split / steps (whale) and grid / chapter (scams); `steps`
appears once in that set and `stat` in none of it. The long form takes the
*second*, three-node version of the same track as a deliberate rhyme, which is
a thing only that file does - the Short shows the four-step version once and
never draws the contrast, because forty-seven seconds cannot carry a rhyme.

**Cold close, no question** (`narration.md`, "A Short's ending loops"). The
last line answers the opening question instead of re-asking it - the viewer's
first thought and last thought become the same thought - and `outro=` holds it
to the final frame so the piece loops into its own opening.

**No disclaimer.** The long form carries it and shorts on this channel drop it
deliberately; the pair as a whole is never missing it.

**No financial advice:** no price, no level, no prediction, no platform rated,
nothing recommended. The whole argument is that the first payment was worth
nothing. No live price, chart, ticker or broker name appears in any shot.

**The one outside source**, as in the long form: the bio does not say what
reusable proof of work depended on, and the trusted-server fact is the hinge.
It comes from Finney's own RPOW page via the Nakamoto Institute - token
ownership "registered on a trusted server", on a coprocessor that can attest
which software it runs.

**No photograph of him is used here.** The only free image that exists is a
1972 newspaper photo of him as a teenager; it carries the thumbnail, where it
is a picture rather than a stand-in, and the long form puts it in a beat's
picture column under a line that dates it. Nobody stands in for him in the
cut.

**Clips** are the pair's own fetch, screened across their length and read off
a labelled contact sheet. The pair is one video for the reuse rule, so every
clip here is counted against the long form's roster too.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/first-bitcoin-transaction.py
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
SOURCE_OG = "hal-finney"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# Screened across their length, then looked at on a labelled contact sheet.
# The trailing comment is the luma/saturation range over the whole clip.
EMBERS = V / "embers-glowing-in-a-fire-close-up-dark/13220869.mp4"       # 22s, L3-4 S5, embers breathing in a dark grate
LIT = V / "candle-being-lit-in-the-dark-close-up/5767251.mp4"            # 31s, L2 S1, one candle burning on pure black
ROOM = V / "old-ledger-book-handwriting-candle-dark/10425839.mp4"        # 11s, L21-23 S21, a closed book and a candle in a dark room
GRID = V / "city-lights-from-above-at-night/9709111.mp4"                 # 12s, L38-39 S22, a lit street grid from above
CANOPY = V / "dark-forest-canopy-looking-up-night/27437296.mp4"          # 16s, L14-15 S20, a star field through branches
BRIDGE = V / "bridge-lights-at-night-long-exposure/30153497.mp4"         # 15s, L2 S0, a line of lamps receding into black
COIN = V / "coin-spinning-on-dark-table/35996676.mp4"                   # 9s,  L7 S0, a coin spinning and settling
CITY = V / "city-lights-from-above-at-night/8978968.mp4"                 # 36s, L7 S4, a dark city from high above

# The only free photograph of him that exists: aged 16, holding up a sheet of
# hand-lettered mathematics. Public domain, Daily News-Post staff photo, via
# Wikimedia Commons. Square, so `aspect` is set to the source's own ratio.
FINNEY = ROOT / "assets/crypto/finney/hal-finney-1972.jpg"               # 4677x4705 r0.99, L146 S0

THUMB = FINNEY
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly. A Short arrives with no title card and no
    # thumbnail on screen, so the first line is what turns the next forty
    # seconds into an answer somebody is waiting for.
    ("Who received the very first bitcoin ever sent?",),

    # The partial answer, and it carries the hook's hidden token as its
    # **first word**. Written "A cryptographer who, five years earlier..."
    # the token landed at 4.4s, past `hook_reveal_time`'s 4.2s ceiling, and
    # the render fell back to revealing at 3.0s on nothing - the bar came off
    # before the voice got there. Fronting it also pulls the caption mute in,
    # since captions resume at the first sentence starting after the hook
    # clears.
    ("Five years earlier, he had built digital money of his own.",),

    ("His name was Hal Finney.",
     "And his version worked."),

    ("You spent real computing time to make a token,",
     "and then you could pass that token on."),

    # The hinge into the beat. Its own sentence, because a leading hinge
    # inside the beat's span eats reveal zero.
    ("But look at what happened every time it moved.",),

    # The steps track's own sentence - one chunk per node, in reveal order.
    # The fourth is the whole point of the video.
    ("You make the token.",
     "You send it on.",
     "It gets checked against a register.",
     "And one machine keeps that register."),

    ("Trust that machine, or the money does not work.",),

    # The statement card's own sentence.
    ("Then, in January two thousand nine, "
     "Satoshi Nakamoto sent him ten bitcoins.",),

    ("Same idea.",
     "No machine in the middle."),

    # Cold close. It answers the opening question instead of re-asking it, so
    # the last thought and the first thought are the same thought.
    ("The first bitcoin ever sent",
     "went to the one man who already knew what was missing."),
]

SHOTS = [
    # **The opening slot clears the hook band.** The headline sits centred at
    # 34% of the height, and a candle's flame lands almost exactly there - so
    # the single-candle clip, which is the obvious opener for "the first one",
    # waits until shot two. The embers sit in the lower half and the frame is
    # black where the band goes.
    Shot(clip=EMBERS, clip_at=2.0, clip_ax=0.50),
    # **The pair shares a picture here rather than at frame one.**
    # `shorts.md` wants the two cuts to open on the same image so a viewer who
    # sees both recognises the second - but the long form opens on this coin,
    # and a 9s source has exactly one usable position, so sharing it at frame
    # one would spend the Short's opening slot on a clip that cannot also
    # clear the hook band. It lands on sentence two instead, which is the
    # nearest slot that keeps both rules.
    # **`clip_ax=0.91`, measured on the real 9:16 crop rather than the
    # landscape frame.** The coin sits at ~0.78 of the source width and the
    # lamp lighting it at ~0.29, so the centred default takes the empty table
    # between them: the first render of this shot was a black frame. 0.19
    # gives the bare lamp, which reads as a lightbulb and not as a coin.
    Shot(clip=COIN, clip_at=0.5, clip_ax=0.91),
    Shot(clip=ROOM, clip_at=2.5, clip_ax=0.45),
    Shot(clip=GRID, clip_at=3.0, clip_ax=0.50),
    Shot(clip=CANOPY, clip_at=8.0, clip_ax=0.50),
    Shot(graphic="steps", backdrop=BEATGROUND,
         # **`steps` takes a flat list of strings, not (label, note) pairs.**
         # A two-tuple is read as `(text, emoji)` and the second element is
         # pushed through `emoji_image`, which raises on any ordinary phrase.
         # `grid` is the beat with a second line; `steps` has none, so each
         # node has to say the whole thing itself.
         payload=(["Make a token",
                   "Send it on",
                   "Check it against a register",
                   "One machine keeps that register"],
                  "EVERY TIME IT MOVED")),
    # One flame in the dark, under "trust that machine". The only use of
    # this clip in either file, which is what the single-machine line wants.
    Shot(clip=LIT, clip_at=1.0, clip_ax=0.50),
    # **`chapter`, not `stat`, and that is a code fact rather than a choice.**
    # `stat` has no portrait layout - `crypto/build.py` refuses it outright,
    # along with `quote` and `compare`, because all three lay a content column
    # beside a picture column at 1920. (`shorts.md` calls `stat` "the better
    # vertical beat for a number that stands alone", which is wrong about this
    # engine; noted for the doc pass.) A full-screen statement is the right
    # vertical treatment for the one number anyway, and it is a completely
    # different silhouette from the track above it.
    Shot(graphic="chapter", payload=("TEN COINS. BLOCK 170.",)),
    Shot(clip=BRIDGE, clip_at=6.0, clip_ax=0.50),
    Shot(clip=CITY, clip_at=12.0, clip_ax=0.50),
]

# 2.10 on the steps sentence buys the silence its four nodes are read in;
# 1.30 lets the block number sit after it lands.
GAPS = [0.80, 0.85, 0.80, 0.75, 0.95, 2.10, 0.90, 1.30, 0.85, 1.20]


def main() -> None:
    out = Path.home() / "Desktop/first-bitcoin-transaction-short.mp4"
    work = Path.home() / "Desktop/.first-bitcoin-transaction-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The hidden token is a duration, which passes the cover-the-bar test:
        # the sentence's own grammar does not hand it to you. Sentence 2 says
        # it five words in.
        hook="He built digital money [five years] before Bitcoin",
        # A redacted hook *is* showing the spoken line, so a caption under it
        # burns the same sentence twice - mute it. The outro card is the
        # closing line, so its mute applies too; both follow the default here
        # because this is the hook case the flag was written for.
        outro="He already knew [what was missing].")
    # The pair shares its thumbnail. Four short forced rows and a raised size:
    # the size search is capped by the longest row, so short rows clear the
    # column early and it keeps climbing.
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO,
        "Who got\nthe first\n[bitcoin?]",
        # **`ax`, not `at` - a square source crops horizontally here.** A
        # 1:1 image covering a 9:16 frame scales to the frame's height and
        # overflows sideways, so `at` (vertical) does nothing and the
        # centred `ax` default took the middle of the picture: the first
        # render was a tie, two hands and the sheet, with his head outside
        # the frame entirely. 0.12 keeps his whole head without clipping it
        # on the left edge, and still carries a corner of the mathematics.
        # `band="bottom"` because his head is in the top half.
        image=THUMB, accent="yellow", band="bottom", size=240, ax=0.12)
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    main()
