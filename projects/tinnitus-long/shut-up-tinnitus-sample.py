"""Shut Up, Tinnitus - the audiobook's retail sample as a YouTube read-along.

The Spotify sample (introduction plus chapter one, unbroken) over the cover,
with karaoke captions. **No new narration**: the audio is the delivered MP3,
lifted to the channel's loudness and nothing else. See `longform/readalong.py`
for why this is its own build type rather than a `render_long` flag.

**The text is read from the audiobook repo at build time, never copied
here.** The manuscript is a paid product and is git-ignored over there on
purpose; this script only knows where it lives. The same goes for the pacing
gaps and the lexicon: they are imported from the code that rendered the audio,
so the segmentation is scored against what was actually scripted, and the
alignment references are synthesised with the respellings the narrator used.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/shut-up-tinnitus-sample.py
"""

import importlib.util
import sys
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.meta import Meta
from video_automation.longform.readalong import Part, align, render_readalong

BOOK_REPO = Path.home() / "Coding/audio-book-automation"
sys.path.insert(0, str(BOOK_REPO))
from audiobook_automation.core import pacing, pronounce, render, voices  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "shut_up_tinnitus", BOOK_REPO / "projects/tinnitus/shut-up-tinnitus.py")
recipe = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(recipe)

DESKTOP = Path.home() / "Desktop"
SRC = DESKTOP / "audiobook"
AUDIO = SRC / "Shut-Up-Tinnitus-sample-spotify.mp3"
COVER = SRC / "cover-3000.png"
BADGES = [Path.home() / "Coding/tinnitus-blog/public/spotify-badge.png",
          Path.home() / "Coding/tinnitus-blog/public/google-play-badge.png"]

OUT = DESKTOP / "shut-up-tinnitus-sample-long.mp4"
THUMB = DESKTOP / "shut-up-tinnitus.png"     # the editor's own, not rendered here
WORK = DESKTOP / ".shut-up-tinnitus-sample-work"

# The book's page on the site, which carries the streaming links and this
# video. One word, like the site's other routes (/zen, /videos, /faq).
PAGE = "https://tinnitushelp.me/audiobook"
# From tinnitus-blog/src/const/audiobook.ts, the one place the site keeps them.
SPOTIFY = "https://open.spotify.com/show/1qdS3WtgeMVxABswacmtC7"
GOOGLE_PLAY = "https://play.google.com/store/audiobooks/details?id=AQAAAEBGqBToQM"

# The heading each track gets on the panel and in the description.
CHAPTERS = {
    "01-intro.mp3": "Introduction: The Sound Is Not the Problem",
    "02-ch01.mp3": "Chapter 1: Beethoven's Letter from Vienna",
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
    title="Shut Up, Tinnitus - Free Audiobook Sample (Introduction and Chapter 1)",
    hook=("The first eight minutes of Shut Up, Tinnitus: why your ears ring, "
          "why it gets louder, and why the volume and the suffering are two "
          "different things."),
    url=PAGE,
    cta=f"The full audiobook, where to stream it and more about the book: {PAGE}",
    summary=(f"Spotify: {SPOTIFY}\n"
             f"Google Play Books: {GOOGLE_PLAY}"),
    tags=["tinnitus audiobook", "shut up tinnitus", "tinnitus", "ringing in ears",
          "living with tinnitus", "tinnitus habituation", "audiobook sample",
          "tinnitus help"],
    credits=["Narration: Kokoro (AI voice). Written by Oktay Shakirov.",
             "",
             "This audiobook is general information, not medical advice. If "
             "your tinnitus lasts more than a few weeks, keeps getting louder, "
             "is in one ear only, pulses with your heartbeat, or comes with "
             "dizziness or hearing loss, please see a doctor or an "
             "audiologist."],
)


def main() -> None:
    narrator = voices.get("atlas")
    captions, chapters, total = align(
        AUDIO, parts(), WORK, voice=narrator.voice, speed=narrator.speed,
        tail=render.TAIL_SILENCE, spoken=pronounce.say)
    made = render_readalong(
        AUDIO, COVER, captions, chapters, total, OUT, WORK, TINNITUS,
        badges=BADGES, meta=META, thumb=THUMB)
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
