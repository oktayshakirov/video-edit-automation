"""What does a blockchain actually do for AI? ~45s crypto short.

Source: crypto-wiki/content/posts/decentralized-ai-can-ai-run-on-the-blockchain.mdx -
the same post as the `decentralized-ai` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks the arithmetic, the
three ways an answer is trusted and what a proof cannot prove. This does one
move, in the order a viewer would ask it (`shorts.md`, 2026-10-13: Shorts
should be easy to follow): why the chain cannot do the thinking - thousands
of computers doing the same math - and the one job it does instead, which
is checking. No sum is said aloud; the one number is a full-screen card.

**The title is a "what" question, not the article's yes/no** (`narration.md`,
2026-10-11: a yes/no title invites "yes" or "no" in sentence 2). Sentence 2
overturns the assumption behind it - "not the thinking" - and keeps the
answer back by naming only its kind: "one job the AI cannot do for itself".
The hook hides `[one job]`, which is that kind, not the job.

**Three beats, three silhouettes:** `replicate` (new - one job fanning out
into identical node bars filling in lockstep), a full-screen `chapter` for
the one number, and a `diagram` of the check. The bear-market Short ran
bars / diagram / steps, so only the diagram repeats, and its chain here is
straight, not a loop.

**Opener: the redacted hook.** Last three crypto Shorts ran Search / Counter
/ Stamp.

**Cold close**, the long form's own last line - the blockchain does not run
the AI, it checks it - held to the last frame by `outro=` so it loops back
into the title question. **No disclaimer** (the long form carries it). **No
financial advice:** no price, no token, no project, no platform.

**Clips** are the long form's roster, each once here; the opening hands at a
laptop are the long form's first shot too, shared on purpose.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/decentralized-ai.py
"""

import sys
from pathlib import Path
from pathlib import Path as _P

from PIL import Image

from video_automation.core import music
from video_automation.core.brand import CRYPTO
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import Shot
from video_automation.longform import thumb as T

SOURCE_POST = "decentralized-ai-can-ai-run-on-the-blockchain"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# The long form's roster - screened there, see its header.
KEYS = V / "hands-typing-keyboard-dark/5495784.mp4"               # 18s, hands typing on a laptop in the dark - the long form's first shot
NET = V / "neural-network-visualization/37101560.mp4"             # 10s, a gold network of fibres - the model
CORRIDOR = V / "supercomputer/32386520.mp4"                       # 11s, a corridor between server racks, centred
COINS = V / "stack-of-coins-dark/5253412.mp4"                     # 27s, coins across a dark table
GPU = V / "graphics-card-close-up-dark/3147349.mp4"               # 20s, a graphics card's fan in a lit case
CHIP = V / "circuit-board-close-up-dark/6755158.mp4"              # 18s, one processor die on dark stone, centred
TOPDOWN = V / "hands-typing-keyboard-dark/5495845.mp4"            # 21s, top-down hands on a laptop, centred

BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # The title question, plainly, while the hook is up.
    ("What does a blockchain actually do for AI?",),

    # Overturns the assumption and names only the kind of answer.
    # "one job" sits in the first words of its second chunk so the reveal
    # lands by ~4s: as "It does one job..." it was spoken at 4.3s and the
    # hook fell back to revealing at 3.0s, ahead of the voice.
    ("Not the thinking.", "One job the AI cannot do for itself."),

    # The hinge gets its own sentence: inside the beat's span it would eat
    # reveal zero.
    ("A blockchain is not one computer. It is thousands, all checking each other.",),

    # The replicate beat's own sentence: the job, then the copies.
    ("Send it one job,", "and every one of them does the same math."),

    ("That makes it trustworthy, and it makes every step cost a fee.",),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("ONE WORD OF AI. HUNDREDS OF BLOCKS.",
      "One word from a mid-sized AI model would fill hundreds of blocks."),),

    ("So the model runs on ordinary graphics cards, off the chain.",),

    ("And the chain does the one job the AI cannot do for itself.",),

    # The diagram's own sentence - one chunk per node.
    ("The model sends its answer, with a proof.",
     "Every computer checks that proof, in under a second.",
     "And the contract pays it, or takes its deposit."),

    # Cold close: the long form's echo, held by `outro=`.
    ("The blockchain does not run the AI. It checks it.",),
]

SHOTS = [
    Shot(clip=KEYS, clip_at=1.0, clip_ax=0.50),
    Shot(clip=NET, clip_at=0.5, clip_ax=0.50),
    Shot(clip=CORRIDOR, clip_at=0.5, clip_ax=0.50),
    Shot(graphic="replicate", backdrop=BEATGROUND,
         payload=("ONE JOB", "a single word from an AI",
                  "x THOUSANDS", "every computer, the same math",
                  "WHO DOES THE MATH?")),
    Shot(clip=COINS, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="chapter", payload=("ONE WORD OF AI. HUNDREDS OF BLOCKS.",)),
    Shot(clip=GPU, clip_at=1.0, clip_ax=0.45),
    Shot(clip=CHIP, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="diagram", backdrop=BEATGROUND,
         payload=([("Answer + proof", "from the graphics cards"),
                   ("Proof checked", "by every computer, in under a second"),
                   ("Paid, or penalised", "it loses its deposit if it lied")],
                  "WHAT THE CHAIN DOES")),
    Shot(clip=TOPDOWN, clip_at=1.0, clip_ax=0.50),
]

GAPS = [0.50, 0.85, 0.60, 1.30, 0.70, 1.10, 0.55, 0.60, 1.40, 1.20]

# The long form's headline. The vertical cover forces phrase-shaped rows.
HEADLINE = "Can AI run on a [blockchain?]"
HEADLINE_V = "Can AI\nrun on a\n[blockchain?]"


def thumbs(out: Path) -> Path:
    """The 9:16 cover, re-cut 2026-10-20: the long form's bionic-hand photo,
    cropped to the two hands at full width and set at the bottom, the studio
    grey extended upward with a dark fade under the headline.

    A cover crop (`render_short_thumb`) of a landscape source is a third of
    its width, and the editor rejected it: the hands were lost. Fitting the
    width keeps both hands and the touch whole; the photo's backdrop is a
    flat grey, so the extension has no seam. Replaced the drawn beat in
    `thumbs_beat`.
    """
    import numpy as np
    src = Image.open("assets/stock/photos/bionic-hand/6153354.jpg").convert("RGB")
    c = src.crop((800, 200, 3450, 2731))
    a = np.asarray(c.resize((1080, round(c.height * 1080 / c.width)),
                            Image.LANCZOS)).astype(float)
    ph = a.shape[0]
    y0 = 1920 - ph - 40
    can = np.zeros((1920, 1080, 3))
    can[:y0] = a[:30].mean((0, 1))
    can[y0 + ph:] = a[-30:].mean((0, 1))
    can[y0:y0 + ph] = a
    yy = np.arange(1920)[:, None]
    m = np.clip((820 - yy) / 820, 0, 1) ** 1.3 * 0.9
    im = Image.fromarray((can * (1 - m[..., None])).astype("uint8"))
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE_V, 240, 1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.24, leading=1.02, band="top",
                margin=int(1920 * 0.07), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def thumbs_beat(out: Path) -> Path:
    """The original 9:16 cover: the `replicate` beat drawn in portrait, all copies
    lit, with the long form's headline in the room above the card."""
    from video_automation.core.frame import VERTICAL
    from video_automation.longform.beats import Replicate
    b = Replicate("ONE JOB", "a single word from an AI",
                  "x THOUSANDS", "every computer, the same math", "",
                  brand=CRYPTO, frame=VERTICAL, reveals=[0.0, 0.2],
                  start=0.0, hold=10.0)
    # The content alone, on black - the long form's thumbnail does the same,
    # so the pair share one ground and no water seam is possible.
    im = Image.new("RGB", VERTICAL.size, (0, 0, 0))
    b.content(im, 1.0)
    canvas = Image.new("RGB", VERTICAL.size, (0, 0, 0))
    # The beat sits from y=470; push it down so the headline has the top.
    canvas.paste(im.crop((0, 300, 1080, 1660)), (0, 560))
    fill, ink = T.ACCENTS["yellow"]
    T._headline(canvas, HEADLINE_V, 240,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.24, leading=1.02, band="top",
                margin=int(1920 * 0.07), shadow=14, drop=(6, 8))
    canvas.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/decentralized-ai-short.mp4"
    work = Path.home() / "Desktop/.decentralized-ai-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The kind of answer, said in sentence 2 - not the job itself.
        hook="The blockchain does [one job] for AI",
        outro="The blockchain does not run the AI. It [checks] it.")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/decentralized-ai-short-thumb.jpg"))
    else:
        main()
