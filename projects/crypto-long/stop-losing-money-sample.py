"""Stop Losing Money in Crypto - the audiobook's retail sample as a YouTube read-along.

The second read-along, after `tinnitus-long/shut-up-tinnitus-sample.py`, and
built the same way: the Spotify sample (introduction plus chapter one,
unbroken) over the cover, with karaoke captions. **No new narration**: the
audio is the delivered MP3, lifted to the channel's loudness and nothing else.

**The text is read from the audiobook repo at build time, never copied
here.** The manuscript is a paid product and is git-ignored over there on
purpose; this script only knows where it lives. The pacing gaps and the
lexicon are imported from the code that rendered the audio, so the
segmentation is scored against what was actually scripted.

The sample is rebuilt from the chapter files, so if the upload kit has gone
from the Desktop, re-render first, in the audiobook repo:

    python projects/crypto/stop-losing-money.py --track 01-intro.md 02-ch01.md
    python projects/crypto/stop-losing-money.py --preview spotify

    PYTHONPATH=. .venv/bin/python projects/crypto-long/stop-losing-money-sample.py
"""

import importlib.util
import sys
from pathlib import Path

from PIL import Image

from video_automation.core.brand import CRYPTO
from video_automation.longform.meta import Meta
from video_automation.longform.readalong import Part, align, render_readalong

BOOK_REPO = Path.home() / "Coding/audio-book-automation"
sys.path.insert(0, str(BOOK_REPO))
from audiobook_automation.core import pacing, pronounce, render  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "stop_losing_money", BOOK_REPO / "projects/crypto/stop-losing-money.py")
recipe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(recipe)

DESKTOP = Path.home() / "Desktop"
AUDIO = recipe.OUT / f"{recipe.SLUG}-sample-spotify.mp3"
# The 3000px master cover. It is a ChatGPT export with an alpha channel, so it
# is flattened onto black in the work dir before it becomes the still.
COVER_SRC = BOOK_REPO / "projects/crypto/book/cover.png"
SITE = Path.home() / "Coding/crypto-wiki/public"
BADGES = [SITE / "spotify-badge.png", SITE / "google-play-badge.png"]

OUT = DESKTOP / "stop-losing-money-sample-long.mp4"
WORK = DESKTOP / ".stop-losing-money-sample-work"

# The book's page on the site, which carries the streaming links and this
# video once it is uploaded.
PAGE = "https://www.thecrypto.wiki/audiobook"
# From crypto-wiki/config/audiobook.js, the one place the site keeps them.
SPOTIFY = "https://open.spotify.com/show/5L3CgtyFC83zbayVI9LSKU"
GOOGLE_PLAY = "https://play.google.com/store/audiobooks/details?id=AQAAAEBGeRs5TM"

# The heading each track gets on the panel and in the description.
CHAPTERS = {
    "01-intro.mp3": "Introduction: The Price Is Not What Takes Your Money",
    "02-ch01.mp3": "Chapter 1: The Man Who Took the Keys to His Grave",
}


def parts() -> list[Part]:
    """Every synthesiser call in the sample, with the silence before it.

    Mirrors `recipe.preview`: each track carries LEAD/TAIL silence, and the
    tracks are joined with PREVIEW_GAP between them.
    """
    tracks, _, _ = recipe.PREVIEWS["spotify"]
    out: list[Part] = []
    for i, mp3 in enumerate(tracks):
        t = pacing.parse(recipe.MANUSCRIPT / mp3.replace(".mp3", ".md"))
        lead = render.LEAD_SILENCE
        if i:
            lead += render.TAIL_SILENCE + recipe.PREVIEW_GAP
        out.append(Part(t.title, lead, CHAPTERS[mp3]))
        out += [Part(p, g) for g, p in pacing.plan(t)]
    return out


META = Meta(
    title="Stop Losing Money in Crypto - Free Audiobook Sample (Introduction and Chapter 1)",
    hook=("The first nine minutes of Stop Losing Money in Crypto: why the price "
          "is not what takes your money, and the real story of QuadrigaCX, the "
          "exchange whose founder supposedly took the keys to his grave."),
    url=PAGE,
    cta=f"The full audiobook, where to stream it and more about the book: {PAGE}",
    summary=(f"Spotify: {SPOTIFY}\n"
             f"Google Play Books: {GOOGLE_PLAY}"),
    tags=["crypto audiobook", "stop losing money in crypto", "crypto scams",
          "quadrigacx", "gerald cotten", "crypto security", "audiobook sample",
          "crypto for beginners"],
    credits=["Narration: Kokoro (AI voice). Written by Oktay Shakirov.",
             "",
             "This audiobook is general information, not financial advice. It "
             "makes no price predictions and recommends no coins."],
)


def cover(work: Path) -> Path:
    work.mkdir(parents=True, exist_ok=True)
    out = work / "cover-3000.png"
    im = Image.open(COVER_SRC)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        flat = Image.new("RGB", im.size, (0, 0, 0))
        flat.paste(im, mask=im.split()[3])
        im = flat
    im.save(out)
    return out


def main() -> None:
    narrator = recipe.NARRATOR_PROFILE
    captions, chapters, total = align(
        AUDIO, parts(), WORK, voice=narrator.voice, speed=narrator.speed,
        tail=render.TAIL_SILENCE, spoken=pronounce.say)
    made = render_readalong(
        AUDIO, cover(WORK), captions, chapters, total, OUT, WORK, CRYPTO,
        badges=BADGES, meta=META)
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
