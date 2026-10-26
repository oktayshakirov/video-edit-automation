"""Why was half of all bitcoin mined in its first four years? ~45s crypto short.

Source: crypto-wiki/content/posts/the-bitcoin-halving.mdx - the same post as
the `bitcoin-halving` long form, written in the same pass.

**The single move.** The long form walks what the halving is, the schedule,
the miners' difficulty loop and what the code does not promise. The Short
does the one move all of that rests on: a reward cut in half every four
years front-loads the supply - half of all bitcoin in the first four years,
nineteen of every twenty already out - and stretches the rest past 2140. Its
title is a different search angle from the long form's "what is the bitcoin
halving".

**Opener: `Counter`**, spinning to 2140 under the title question and landing
as sentence 2 says it. Last three crypto Shorts ran Stamp / hook / Search;
the long form runs a `Counter` too, so the pair is recognised as a pair.

**Sentence 2 is a reversal, not the answer** (`narration.md`, 2026-09-21):
half in four years, *and* the last one not until 2140 - true on its own, and
the question it opens (how can both be true?) is what the halving answers.

**Two beats:** `bars` (the reward, halving five times) and `chart` (every
bitcoin ever mined: a near-vertical climb, then flat for a century, with the
marker where we are). Not the market-cap Short's `bars` + `chapter`.

**Cold close**, recontextualising the opening question instead of asking
one; `outro=` holds it to the last frame so the piece loops back into "why
was half...". **No disclaimer** - the long form carries it. **No financial
advice:** no price is mentioned at all.

**Figures** are the article's or arithmetic on them: 210,000 x 50 = 10.5M,
half the 21M cap; 19.7M by the 2024 halving plus ~450 a day since puts more
than 95% out by 2026, so "nineteen of every twenty" is true now and stays
true; the last fraction around 2140.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/bitcoin-halving.py
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
from video_automation.longform.openers import Counter

SOURCE_POST = "the-bitcoin-halving"

V = STOCK / "videos"
P = STOCK / "photos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# The long form's roster - screened there, see its header.
CAL = V / "marking-date-on-calendar/9057559.mp4"                 # 11s, a red marker circling a date - the pair's shared opening shot
COINS = V / "bitcoin-coin-close-up-dark/4406964.mp4"             # 14s, gold bitcoins filling the frame
TERM = V / "command-line-terminal-screen/35475096.mp4"           # 22s, a terminal scrolling
GPU = V / "graphics-card-mining-rig/7380236.mp4"                 # 15s, a man turning a graphics card over
HOUR2 = V / "hourglass-sand-falling-dark/1196530.mp4"            # 10s, an hourglass, violet sand
HOUR = V / "hourglass-sand-falling-dark/39488458.mp4"            # 17s, an hourglass running, pink sand on blue

SOIL = P / "single-gold-bitcoin-dark/5980926.jpg"                # 6638x4425, a bitcoin half-buried in soil
BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

# Cumulative supply, one point per four-year epoch from 2009 to ~2141: 1 -
# 0.5^k. The first segment climbs to half; the remaining thirty-two are the
# century of thinner and thinner slices. Marker at k=4 (~2025, 94%).
SUPPLY = [1 - 0.5 ** k for k in range(34)]

SENTENCES = [
    # The title question, plainly.
    ("Why was half of all bitcoin mined in its first four years?",),

    # The reversal - the Counter lands on "2140".
    (("And the last one is not due until 2140.",
      "And the last one is not due until twenty-one forty."),),

    ("Both come from one rule, called the halving.",),

    (("Every 210,000 blocks, about every four years,",
      "Every two hundred and ten thousand blocks, about every four years,"),
     "the new bitcoin paid to miners is cut in half."),
    # No separate hinge: the sentence above already says what the bars
    # show, which is the case `shorts.md` exempts.

    # The bars' own sentence - one chunk per row.
    ("Fifty a block in 2009.",
     "Twenty-five in 2012.",
     "Twelve and a half in 2016.",
     "Six point two five in 2020.",
     "Three point one two five in 2024."),

    ("So every four years mints half as much as the four before.",),

    ("The first four years made ten and a half million coins.",
     "Half of the twenty-one million there will ever be."),

    # The chart's own sentence: the line first, the marked moment second.
    ("Draw every bitcoin ever mined, and the line shoots up, then goes flat.",
     "Nineteen of every twenty already exist."),

    # Cold close. It answers the opening question instead of re-asking it.
    ("Half took four years. The rest takes over a century.",),
]

SHOTS = [
    Shot(clip=CAL, clip_at=0.5, clip_ax=0.55),
    Shot(clip=COINS, clip_at=1.0, clip_ax=0.50),
    Shot(clip=TERM, clip_at=2.0, clip_ax=0.40),
    Shot(clip=GPU, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="bars", backdrop=BEATGROUND,
         payload=([("2009", 0.92, "50 BTC"),
                   ("2012", 0.46, "25"),
                   ("2016", 0.23, "12.5"),
                   ("2020", 0.115, "6.25"),
                   ("2024", 0.0575, "3.125")],
                  "NEW BITCOIN PER BLOCK")),
    Shot(clip=HOUR2, clip_at=0.5, clip_ax=0.50),
    Shot(image=SOIL),
    Shot(graphic="chart", backdrop=BEATGROUND,
         payload=(SUPPLY, "EVERY BITCOIN EVER MINED", 4,
                  "19 of every 20 already mined")),
    Shot(clip=HOUR, clip_at=1.0, clip_ax=0.45),
]

GAPS = [0.70, 0.80, 0.60, 0.60, 1.30, 0.70, 0.85, 1.40, 1.20]

# The long form's words (re-done 2026-10-26): this Short's own fact.
HEADLINE = "Half of it\nmined in\n[4 years]"


def thumbs(out: Path) -> Path:
    """The 9:16 cover: a 3:4 cut round the coin, scaled to the width on the
    bottom of the frame, the soil continued above as a blur, and the rows
    on it. The old straight 9:16 cut started the coin's rim ~29% down and
    left the headline only a fifth of the frame, so it set small."""
    w, h = Image.open(SOIL).size
    src = Image.open(SOIL).convert("RGB")
    cw = int(h * 0.75)
    x0 = int(w * 0.47 - cw / 2)
    im = T.bleed_portrait(src.crop((x0, 0, x0 + cw, h)), feather=160,
                          fill="blur")
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE, 240, 1080 - 2 * 52, 52, fill, ink, max_lines=4,
                max_block=1920 * 0.36, leading=1.02, band="top",
                margin=int(1920 * 0.13), shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out

def main() -> None:
    out = Path.home() / "Desktop/bitcoin-halving-short.mp4"
    work = Path.home() / "Desktop/.bitcoin-halving-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The payoff is a number. Enters when the voice says "the last one"
        # and lands on "2140" - the user's note was that a counter spinning
        # from frame one under the title question took too long.
        opener=Counter("2140", "THE LAST BITCOIN", at_word="2140",
                       enter_word="last"),
        outro="Half took four years. The rest takes over a [century].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/bitcoin-halving-short-thumb.jpg"))
    else:
        main()
