"""Will GTA 6 have crypto? ~45s crypto short.

Source: crypto-wiki/content/posts/grand-theft-auto-crypto.mdx - the same post
as the `gta-6-crypto` long form, written in the same pass.

**Not a trailer for the long form.** The long form walks the rumor's history,
why Rockstar stays away and the leak coin's loop. This answers in the order a
viewer would ask it (`shorts.md`, 2026-10-13): is there crypto in it (a fake
coin), what about everything else people said (a judged list), and where the
real money is (outside the game, a leaker's pump and dump). No sum is said
aloud; the one figure is a full-screen card.

**The title is the article's yes/no question**, which `narration.md` flags
as a trap - but the honest answer is *no*, so sentence 2 is a plain reversal
("Not real crypto.") that opens the next question in the same breath ("a fake
coin, hidden in the final trailer" - which coin?). The coin's name is kept
back to sentence 3.

**Three beats, three silhouettes:** `checklist` (flow), `chart`, and a
full-screen `chapter`. The last three crypto Shorts ran replicate / chapter /
diagram, bars / diagram / steps and bars / chart; `chapter` and `chart` each
repeat one video apart, with a different subject.

**Opener: `Stamp`, the long form's own** - RUMOR over "GTA 6 pays you in
Bitcoin", landing on "rumor" in sentence 2. The first cut ran `Search`; the
editor asked for the long form's opener so the pair reads as one.

**Cold close**, the long form's middle line made the whole verdict - held to
the last frame by `outro=` so it loops back into the title question. **No
disclaimer** (the long form carries it). **No financial advice:** both real
tokens are history with dates, unaffiliated, never a direction.

**Clips** are the long form's roster, each once here; the opening gamepad is
the long form's first shot too, shared on purpose. No game footage.

    PYTHONPATH=. .venv/bin/python projects/crypto-short/gta-6-crypto.py
"""

import subprocess
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
from video_automation.longform.openers import Stamp

SOURCE_POST = "grand-theft-auto-crypto"

V = STOCK / "videos"
ROOT = _P(__file__).resolve().parents[2]
BRAND = ROOT / "assets/brand"

# The long form's roster - screened there, see its header.
PAD = V / "playing-video-game-controller-dark/16628557.mp4"    # 14s, hands on a gamepad - the long form's first shot
AVENUE = V / "palm-trees-neon-night/40175608.mp4"              # 11s, a palm avenue between towers, centred
LAPTOP = V / "laptop-screen-dark-room/7272375.mp4"             # 20s, hands at a laptop in the dark

# Real references, the long form's set - see its header.
PRESS = ROOT / "assets/stock/press/gta6"
LOGO = PRESS / "img/poster_logo.0m-7c805zusl7.png"            # GTA VI lockup, RGBA
VICENIGHT = PRESS / "img/desktop.00.5pzu2sm-z4.jpg"            # Vice City at night, in-game
LAUNCH = PRESS / "img/launch-trailer.0_q-sdrgufc.s.jpg"        # the pair at a red car
HIGHWAY = PRESS / "img/o3982oa93a23k4.05jwq4z-sjai_.jpg"       # Vice City traffic, in-game
PLANE = PRESS / "news/sg.png"                                  # the DacityCoin plane, launch trailer
KEYART_V = PRESS / "img/extended-look.0f0-3vo3w9u26.jpg"      # the key art, portrait cut
BUG = (LOGO, "tr", 0.22)

from video_automation.longform.overlay import ticker_card  # noqa: E402
CARD_LEAK = ticker_card("cyberleek", "Leak meme coin, Aug 2026",
                        "not affiliated with Rockstar", CRYPTO,
                        PRESS / "cards/cyberleek.png")

BEATGROUND = BRAND / "beat-ground-crypto.jpg"

VOICE = "mia"
MUSIC = music.track("night-drift")

# The leak coin's shape - the long form's series, same claim in both cuts.
LEAK = [0.2, 0.6, 3, 8, 14, 20, 25, 22, 20, 19, 14, 7, 5, 3, 1.5]
SALE = 10

SENTENCES = [
    # The title question, plainly, under the long form's Stamp quote.
    ("Will GTA 6 have crypto?",),

    # "rumor" lands the stamp at ~3.5s; then a plain reversal that opens
    # "which coin?" in the same breath.
    ("The Bitcoin was a rumor. But the final trailer does hide a coin. A fake one.",),

    ("Fifty-five seconds in, a stunt plane flies past with DacityCoin painted on it.",),

    # The question goes in the sentence before the beat, never inside it.
    ("So what about everything else people said?",),

    # The checklist's own sentence: the voice says each verdict.
    ("Missions that pay in Bitcoin, scrapped.",
     "N F T cars and houses, never shown.",
     "An official GTA token, there is none.",
     "A made-up coin, for the story. That one is real."),

    ("But outside the game, the coins are real.",),

    ("In August, a leaker tied stolen GTA 6 clips to a meme coin.",),

    # The chart's own sentence: the climb, then the marked sale.
    ("It climbed to about twenty-five million dollars,",
     "then the creator sold, hours before Rockstar's own reveal."),

    # The chapter card: caps on screen, a sentence in the mouth.
    (("$250,000. CASHED OUT.",
      "An estimated quarter of a million dollars, cashed out."),),

    # Cold close, held by `outro=`.
    # "GTA 6's" leads, so the outro card cannot break between GTA and 6.
    ("GTA 6's only crypto is a joke.",),
]

SHOTS = [
    Shot(clip=PAD, clip_at=1.0, clip_ax=0.55),
    Shot(image=VICENIGHT, aspect=1.0),
    # The real frame, shown whole: a tighter crop cut "Dacity" off the left.
    Shot(image=PLANE, aspect=1200 / 900, zoom=1.06),
    Shot(clip=AVENUE, clip_at=0.5, clip_ax=0.50, inset=BUG),
    Shot(graphic="checklist", backdrop=BEATGROUND,
         payload=([("Missions paid in Bitcoin", False),
                   ("NFT cars and houses", False),
                   ("An official GTA token", False),
                   ("A made-up coin, as a joke", True)],
                  "IS IT IN GTA 6?", True)),
    Shot(image=HIGHWAY, aspect=1.0),
    # The hands sit at ~0.68 of the source; centred, the crop is all lid.
    Shot(clip=LAPTOP, clip_at=1.0, clip_ax=0.76,
         inset=(CARD_LEAK, "top", 0.80)),
    Shot(graphic="chart", backdrop=BEATGROUND,
         payload=(LEAK, "THE LEAK COIN", SALE, "the creator sells")),
    Shot(graphic="chapter", payload=("$250,000. CASHED OUT.",)),
    Shot(image=LAUNCH, aspect=0.9, bias=0.3),
]

# Ran 56.4s with a GTA Five parody line and longer hinges; both cut.
GAPS = [0.50, 0.85, 0.60, 0.60, 1.30, 0.60, 0.55, 1.30, 1.10, 1.20]

# The long form's headline. The vertical cover forces phrase-shaped rows.
HEADLINE_V = "Will GTA 6\nhave\n[crypto?]"


def thumbs(out: Path) -> Path:
    """The 9:16 cover: Rockstar's portrait cut of the same key art the long
    form uses, faces in the top half, the headline on three rows over a dark
    ramp at the bottom, clear of the view count."""
    import numpy as np
    src = Image.open(KEYART_V).convert("RGB")
    w = 1080
    src = src.resize((w, int(src.height * w / src.width)), Image.LANCZOS)
    im = Image.new("RGB", (1080, 1920), (0, 0, 0))
    im.paste(src, (0, 0))
    a = np.zeros((1920, 1), np.float32)
    a[900:1600, 0] = np.linspace(0, 1.0, 700)
    a[1600:, 0] = 1.0
    ramp = Image.fromarray((np.repeat(a, 1080, 1) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, (0, 0, 0)), im, ramp)
    fill, ink = T.ACCENTS["yellow"]
    T._headline(im, HEADLINE_V, 220,
                1080 - 2 * 52, 52, fill, ink, max_lines=3,
                max_block=1920 * 0.30, leading=1.02, band="bottom",
                margin=int(1920 * 0.16) + 20, shadow=14, drop=(6, 8))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/gta-6-crypto-short.mp4"
    work = Path.home() / "Desktop/.gta-6-crypto-short-work"
    out, total = render_crypto_short(
        SENTENCES, SHOTS, out, work,
        voice=VOICE, gap=GAPS,
        music=MUSIC, music_gain=0.85,
        # The long form's opener, so the pair reads as a pair (the editor's
        # call on the first cut). It lands on "rumor" in sentence 2.
        opener=Stamp("GTA 6 pays you in Bitcoin", "RUMOR", at_word="rumor"),
        outro="GTA 6's only crypto is a [joke].")
    vert = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{out}  {total:.2f}s")
    print(f"{vert}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/gta-6-crypto-short-thumb.jpg"))
    else:
        main()
