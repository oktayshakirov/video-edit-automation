"""What is proof of stake? ~48s crypto short.

Source: crypto-wiki/content/posts/what-is-proof-of-stake.mdx, the same post as
the `proof-of-stake-long` explainer.

**It narrows the long form's angle rather than repeating it.** That video walks
the whole mechanism - the energy swap, the five-step validator lottery,
slashing, and the wealth-concentration problem it did not solve. Fifty seconds
cannot walk all of that, so this one does the single concrete swap the long
form spends its first two chapters building toward: **proof of work makes
cheating expensive in electricity; proof of stake makes it expensive in your
own money, automatically, with no court involved.** Everything else in the long
form - the lottery mechanics, the wealth-concentration twist - is left out
rather than compressed, because a compressed version of a four-minute argument
is not a hook, it is a worse version of the long form.

**It opens by asking its own title question.** A Short has no title card, no
thumbnail on screen and no chapter list, so the first line has to be the
question the whole thing answers - "What is proof of stake?" - not the first
line of the argument.

**One drawn beat, deliberately not the one the companion long form used for
the same content.** The long form's slashing section is a `checklist`
(flow=True, all four items ticked as the narration states them). This short
uses `grid` for the same four triggers instead - a set with no per-item
verdict needed, since none of the four is a "wrong answer" being ruled out,
they are just facts - which also keeps the short from looking like a
compressed clip of its own companion video rather than its own piece.

**No financial advice.** The script describes a mechanism only: no level, no
prediction, no platform rated, and the closing line is a question about the
mechanism, not a recommendation.

**Every asset is fresh and shared only with this post's long form**, which is
the rule the first cut of this pair broke. The long form's docstring carries
the inventory that forced it and the list of what was screened and rejected.

**Concrete subjects, after the second cut read as wallpaper.** The note was
that the abstracts feel like a background rather than the footage and lose
attention - true of the long form and of this short, which shared the roster.
Most slots are now a person, a screen or hardware; the one abstract kept is the
final shot, because an outro wants an uncluttered frame for the ask.

**The site's own architecture diagram is laid over the second shot** rather
than replacing it, using `longform.overlay.ImageOverlay`. That class was
written for this: a 9:16 frame has real estate above the footage that 16:9
does not, and the note was to use the empty space rather than spend a whole
shot on a still. Placed at y=380 by hand - the class default of 0.16 of frame
height collides with the watermark at y=268.

**Vertical crop.** Every clip is a centred subject - a person at a screen, a
board, a run of dominoes, an industrial surface - so none loses its subject in
the ~32% of source width a 9:16 crop keeps. `clip_ax` and `clip_ay` are left at
the default 0.5 deliberately, same as `bitcoin-price-short`.

**Phonemes.** Same finding as the long form: `32 ETH` (digit form) reads
correctly as "thirty-two eth"; spelling the number out reads the letters
E-T-H instead. `proof of stake` and `proof of work` are said in full, never as
initialisms.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/crypto-short/proof-of-stake.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot
from video_automation.longform.overlay import ImageOverlay
from video_automation.longform.thumb import render_short_thumb

# **Fresh, and shared only with this post's long form.** See that file's
# docstring for the inventory that forced this: the channel had been recycling
# a pool of about fifteen assets across six videos.
NODES = STOCK / "videos/network-nodes-glowing-connections-dark/34994351.mp4"    # 10.0s L22-25 S26
SPHERE = STOCK / "videos/geometric-network-grid-gold-dark/34636451.mp4"         # 10.0s L24-30 S22-27
DOMINO = STOCK / "videos/dominoes-falling-dark/38003914.mp4"                    # 10.0s L11-17 S16-23
GOLDPART = STOCK / "videos/abstract-gold-particles-floating-dark/39038234.mp4"  # 10.0s L14-18 S11-12
TURBINE = STOCK / "videos/wind-turbine-silhouette-night/6279023.mp4"            # 24.8s L20-21 S4-5
CHESS = STOCK / "videos/chess-board-pieces-dark-moody/6599643.mp4"              # 20.9s L33-34 S15-16
PLANT = STOCK / "videos/power-plant-cooling-towers-night/6216703.mp4"           # 15.2s L11-12 S4-5
GOLDDUST = STOCK / "videos/gold-dust-particles-black-background/10296170.mp4"   # 20.4s L26-31 S29-37
SMOKE = STOCK / "videos/smoke-swirling-dark-gold-light/4320605.mp4"             # 30.1s L4-19 S4-10

MAN = STOCK / "videos/man-working-computer-dark-office-night/8311535.mp4"       # 23.0s L19-28 S10-13
CODER = STOCK / "videos/programmer-coding-screen-dark-night/13522186.mp4"       # 14.0s L35-37 S5-6
MONITORS = STOCK / "videos/programmer-coding-screen-dark-night/5240935.mp4"     # 23.0s L20-21 S25-29
FARM = STOCK / "videos/crypto-mining-farm-rows-of-machines/31710201.mp4"        # 20.0s L30-44 S0

PH = STOCK / "photos"
ETHCOINS = PH / "stack-of-coins-dark-moody/20534456.jpg"      # L27.6 S2.0
TRAILS = PH / "abstract-gold-light-trails-black/19253590.jpg"  # L20.2 S24.2
STRIPES = PH / "abstract-dark-gold-geometric/18415806.jpg"     # L17.5 S15.1
POLY = PH / "abstract-dark-gold-geometric/30869731.jpg"        # L30.6 S4.5
GPUCARDS = PH / "graphics-card-gpu-dark-background/8622912.jpg"   # L27.4 S4.3
GPUCOPPER = PH / "graphics-card-gpu-dark-background/34552790.jpg" # L31.6 S23.9
# **Thumbnail only - see the long form's docstring for the two-attempt story.**
# `GPUCARDS` needed `make_slide.py` and a pre-composed vertical canvas because
# it has black margins on every side and no crop of it fills a 9:16 frame.
# `GPUFANS` is a close-up that already bleeds edge to edge in any aspect ratio,
# so it needs neither a slide nor a forced crop - a plain cover crop fills both
# the 1080x1920 and the 1280x720 thumbnail at full sharpness. The user supplied
# this exact photo.
GPUFANS = PH / "gaming-graphics-card-fans-red-lighting/34552811.jpg"  # L47.5 S43.9
CASH = PH / "banknotes-low-key-photography/10149288.jpg"          # L67.1 S28.4
CHIPS = PH / "motherboard-chip-macro-dark/36169770.jpg"           # L36.0 S14.3

# The site's own architecture diagram, laid **over** the second shot rather
# than replacing it - see `longform.overlay.ImageOverlay`. A 9:16 frame has
# room above the footage that a 16:9 one does not.
DIAGRAM = SITE_IMAGES / "posts/proof-of-stake.jpg"

VOICE = "mia"                   # matches the long form from the same post

MUSIC = music.track("night-drift")

# One tuple per sentence; each string is one caption. A drawn beat must have
# exactly one caption per item - that is what times its reveals.
SENTENCES = [
    # The title question, over motion - a Short viewer has nothing else on
    # screen but this sentence.
    ("What is proof of stake?",),

    ("The way crypto stays honest",
     "without a single miner."),

    ("Proof of work burns electricity",
     "to prove you did not cheat."),

    ("Proof of stake spends money instead.",),

    ("Validators lock up a stake as collateral -",
     # espeak stresses `Ethereum` on the wrong syllable - see the long form's
     # docstring. The respell rides in the spoken half only.
     ("on Ethereum, that is 32 ETH.", "on Etheerium, that is 32 ETH.")),

    ("Behave, and you earn rewards.",),

    ("Lie, and the protocol takes the deposit itself.",
     "Automatically."),

    # The question goes here, not inside the beat - a beat times its reveals
    # off the caption starts of its own sentence.
    ("So what actually gets you slashed?",),

    # The beat. Four facts, no verdict needed - none of them is a wrong
    # answer being ruled out, so `grid` rather than `checklist`.
    ("Signing two conflicting blocks.",
     "Going offline too long.",
     "Proposing an invalid block.",
     "Rewriting old history."),

    ("Any one of those,",
     "and part of your stake is gone",
     "before you can argue about it."),

    # The hand-off into the card.
    ("So the whole model comes down to one swap.",),

    # A full-screen statement. `build` suppresses captions on any shot with a
    # graphic, so the on-screen wording can be capitals while the voice reads
    # a plain sentence - no `(caption, spoken)` pair needed since both read
    # the same here.
    ("NO ELECTRICITY. JUST MONEY YOU CAN LOSE.",),

    # **The caption keeps the hyphen; the spoken half gets an ellipsis.**
    # The note was that the outro wants a longer "soo would you rather" for a
    # more human close. Respelling the vowel does not work - espeak reads
    # `Soo` as `sˈuː` ("sue") and `Sooo` as `sˈuːoʊ`, both wrong. Measured in
    # Kokoro, `So -` runs straight through with no pause after "So" at all,
    # while `So...` holds ~170ms there with the vowel intact. The hold is what
    # reads as the drawn-out "so".
    (("So - would you rather burn power, or risk your own money?",
      "So... would you rather burn power, or risk your own money?"),),
]

SHOTS = [
    # 1 - a person at a screen, not an abstract. A Short is judged in its first
    # second and a human face-on-a-task is the most legible thing available.
    Shot(clip=MAN, clip_at=1.0),

    # 2 - **an abstract, deliberately.** This is the shot the diagram is laid
    # over, and it is the one place in the video where wallpaper is the right
    # answer: a diagram needs a quiet ground to be read against. The first cut
    # put the overlay over industrial footage and then a graphics card, and the
    # frame read as two competing pictures. Gold dust on black competes with
    # nothing.
    Shot(clip=GOLDDUST, clip_at=1.0),

    # 3 - "Proof of work burns electricity" on the card that burns it. The
    # overlay has cleared by now, so this shot is seen on its own.
    Shot(image=GPUCOPPER, zoom=1.11, pan=(0.02, 0.01), aspect=1.15, bias=0.5),

    # 4 - **"spends money" lands on fiat**, not on Ethereum coins. Same
    # correction as the long form: the voice says the generic word, so the
    # screen shows the generic thing.
    Shot(image=CASH, zoom=1.11, pan=(-0.02, 0.01), aspect=1.15, bias=0.5),

    Shot(clip=CHESS, clip_at=1.0),

    Shot(clip=MONITORS, clip_at=1.0),

    # 7 - the dominoes are the consequence, and they are literally gold.
    Shot(clip=DOMINO, clip_at=0.5),

    Shot(clip=CODER, clip_at=1.0),

    # 9 - the beat: four cards, one per trigger, revealed as spoken. Icons per
    # card, same reasoning as the long form's `steps` track.
    #
    # **The plug (U+1F50C) shipped once and had to be replaced**: it renders as
    # a dark grey object and all but vanished on a near-black card, which is
    # the exact failure the tinnitus skill records for the stethoscope glyph.
    # The sleeping face is bright yellow, sits with the gold, and says
    # "offline" more directly anyway. Screen an emoji against the card, not
    # against a white editor background.
    Shot(graphic="grid",
         payload=([("Signing two conflicting blocks",
                    "Double voting on the same slot", "\U0001F500"),
                   ("Going offline too long",
                    "Missing your duty repeatedly", "\U0001F634"),
                   ("Proposing an invalid block",
                    "Breaking the protocol's own rules", "\U0001F6AB"),
                   ("Rewriting old history",
                    "A long-range attack from an old key", "\U000023EA")],
                  "WHAT GETS YOU SLASHED"),
         backdrop=CHIPS),

    Shot(clip=FARM, clip_at=1.0),

    Shot(image=GPUCARDS, zoom=1.10, pan=(0.02, -0.01), aspect=1.15, bias=0.5),

    # 12 - the line, full screen.
    Shot(graphic="chapter",
         payload=("NO ELECTRICITY. JUST MONEY YOU CAN LOSE.",)),

    # 13 - the ask, back on the gold network the channel opened the long form
    # with. The one abstract kept, because an outro wants an uncluttered frame.
    Shot(clip=NODES, clip_at=0.5),
]

# One or two per script, where they add something.
EMOJI = {
    "Automatically.": "\U0001F512",                                    # lock
    "So - would you rather burn power, or risk your own money?": "⚡",  # bolt
}

# Pauses are punctuation: 0.34 inside a thought, 0.55-0.90 at the end of one,
# and the long gaps only where a beat needs room. The `grid` (index 8) is a
# flat set with no marks to land, so it takes 0.90 rather than a checklist's
# 2.10 - there is no verdict pause to buy. The statement card (index 11)
# takes 1.30, because a line filling the screen has to be allowed to sit.
GAPS = [0.75, 0.60, 0.55, 0.85, 0.60, 0.55, 0.90, 0.60, 0.90, 0.85,
        0.60, 1.30, 0.34]


def main() -> None:
    out = Path.home() / "Desktop/proof-of-stake-short.mp4"
    work = Path.home() / "Desktop/.proof-of-stake-short-work"
    # **The diagram, laid over the second shot.** Placed by hand rather than
    # centred: `ImageOverlay`'s default sits it at 0.16 of frame height, which
    # in 9:16 collides with the watermark at y=268. y=380 clears the mark, sits
    # above the photo band, and leaves the caption line at ~0.80 untouched.
    from PIL import Image

    from video_automation.core.frame import VERTICAL
    w = int(VERTICAL.w * 0.86)
    DIAGRAM_W, DIAGRAM_H = Image.open(DIAGRAM).size
    # **Centred on both axes.** It sat at y=380 to clear the watermark, which
    # it did, but the note was that it reads as pinned to the top of the frame.
    # A 9:16 frame is 1920 tall and the panel is ~620, so a true centre at
    # y=650 clears the mark at 268 with room to spare and still leaves the
    # caption line at ~0.80 untouched - there was never a reason to ride high.
    #
    # **Window checked against the render, not predicted.** The first pass ran
    # 3.0-7.8 and covered the whole of shot three as well, so the graphics card
    # that shot exists to show was never visible. 2.6-6.4 sits over shot two
    # alone.
    h = int(DIAGRAM_H * (w / DIAGRAM_W))
    overlays = [ImageOverlay(DIAGRAM, 2.6, 6.4, frame=VERTICAL, scale=0.86,
                             at=((VERTICAL.w - w) // 2,
                                 (VERTICAL.h - h) // 2))]
    out, total = render_crypto_short(SENTENCES, SHOTS, out, work,
                                     voice=VOICE, emoji=EMOJI, gap=GAPS,
                                     music=MUSIC, music_gain=0.85,
                                     overlays=overlays)

    # **One thumbnail: vertical, because a Short is a vertical video.** Same
    # source and headline as the long form.
    head = "What replaced the [miners?]"
    vert = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), CRYPTO, head,
        image=GPUFANS, accent="cyan", band="top")
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")
    print(f"{wide}")


if __name__ == "__main__":
    main()
