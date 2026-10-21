"""Typed titles: the opener title and two chapter cards, per site. **Not a
publishable video.**

The reel for `core/typewriter.py` - the chapter card and the opener's lower
third typing themselves on behind a caret, with a key click per character.
Unlike `format-upgrades.py` this one **is narrated**, through the real
`render_long` path, because the point is to hear the clicks sit under the voice
reading the same line.

    PYTHONPATH=. .venv/bin/python projects/demo/typewriter-titles.py [crypto|tinnitus] [band]
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import CRYPTO, TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Section, render_long

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects/demo/out"
V = STOCK / "videos"

CRYPTO_SECTIONS = [
    Section(
        title="Ethereum started as a complaint",
        card=False,
        sentences=[
            ("Ethereum started as a complaint about Bitcoin.",),
            ("Its founder wanted a blockchain that could run any program.",),
            ("He was nineteen, and he took the idea to the people who ran Bitcoin.",),
            ("What they said next is why Ethereum exists at all.",),
        ],
        shots=[Shot(clip=V / "digital-network-grid-gold-dark/28561594.mp4"),
               Shot(clip=V / "blockchain-blocks-chain-digital-dark/34127877.mp4"),
               None, None],
    ),
    Section(
        title="Why did Bitcoin say no?",
        kicker="The rejection",
        sentences=[("The developers who maintain Bitcoin turned the idea down.",)],
        shots=[Shot(clip=V / "abstract-flowing-data-network-dark-blue/28561463.mp4")],
    ),
    Section(
        title="Who controls Ethereum today?",
        sentences=[("The answer is nobody, and that was the point.",),
                   ("Nothing in this video is financial advice.",),
                   ("If this helped, like the video and subscribe for the next one.",)],
        shots=[Shot(clip=V / "digital-network-grid-gold-dark/34645139.mp4"),
               Shot(clip=V / "abstract-flowing-data-network-dark-blue/28561463.mp4",
                    clip_at=4.0, payload=("", "This is not financial advice.")),
               Shot(clip=V / "digital-network-grid-gold-dark/28561594.mp4", clip_at=6.0)],
        gaps=[0.45, 0.60, 2.4],
    ),
]

TINNITUS_SECTIONS = [
    Section(
        title="Can your jaw change your tinnitus?",
        card=False,
        sentences=[
            ("Can your jaw really change your tinnitus?",),
            ("For a lot of people it can, and the reason sits right in front of your ear.",),
            ("Put two fingers there and open your mouth.",),
            ("That small joint moving under your fingers is where this starts.",),
        ],
        shots=[Shot(clip=V / "hand-holding-jaw-pain-dark/19149084.mp4", clip_at=12.0),
               Shot(clip=V / "hand-on-desk-pause-break-office-night-dark/5473794.mp4",
                    clip_at=2.0), None, None],
    ),
    Section(
        title="Why does the jaw affect the ear?",
        kicker="The connection",
        sentences=[("The jaw joint and the ear share nerves and muscles.",)],
        shots=[Shot(clip=V / "city-window-night-quiet-room/8591726.mp4")],
    ),
    Section(
        title="What you can do tonight",
        sentences=[("Nothing in this video is medical advice.",),
                   ("If this helped, like the video and subscribe for the next one.",)],
        shots=[Shot(clip=V / "city-window-night-quiet-room/8591726.mp4", clip_at=6.0,
                    payload=("", "This is not medical advice.")),
               Shot(clip=V / "hand-on-desk-pause-break-office-night-dark/5473794.mp4",
                    clip_at=12.0)],
        gaps=[0.60, 2.4],
    ),
]

SITES = {
    "crypto": (CRYPTO, CRYPTO_SECTIONS, "Ethereum: Who Really Controls It?"),
    "tinnitus": (TINNITUS, TINNITUS_SECTIONS, "Can TMJ Cause Tinnitus?"),
}


def main(site: str, style: str | None = None) -> None:
    brand, sections, title = SITES[site]
    name = f"{site}-typewriter" + (f"-{style}" if style else "")
    made = render_long(
        sections, OUT / f"{name}.mp4", OUT / f"{name}-work",
        brand=brand, voice="mia", music=music.track("night-drift"),
        callouts=None, title_at=2.2, title=title, title_hold=4.6,
        chapter_style=style, endcard=True, endcard_lead=5.0)
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    args = sys.argv[1:]
    style = "band" if "band" in args else None
    for s in ([a for a in args if a in SITES] or ["crypto", "tinnitus"]):
        main(s, style)
