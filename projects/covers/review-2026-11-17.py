"""New covers for seven older long forms, from the 2026-11-17 review.

The review (`videos-performance/history/2026-11-17.md`) found the
tinnitus explainers shown thousands of times and clicked under 1%, every
cover a stock person holding their head with the title repeated on it, and
retitled 17 videos the same day. These covers follow the rule written then
(`thumbnails.md`, "The cover adds to the title; it does not repeat it"): the
cover asks the second half of the question, a list cover carries its number,
no head-holding stock on tinnitus.

Each keeps its video's own picture and crop where that picture was not the
problem (the bedroom, the jaw, the dog, the hooded figure) and changes the
words; the two head-holder covers get a new picture.

    PYTHONPATH=. .venv/bin/python projects/covers/review-2026-11-17.py [key ...]

writes `~/Desktop/covers-2026-11-17/<key>.jpg`. Celebrities was left as it
is: it already shows Kirk and Spock with a question its title does not ask.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))

from video_automation.core.brand import CRYPTO, TINNITUS          # noqa: E402
from video_automation.core.stock import CACHE as STOCK              # noqa: E402
from video_automation.crypto.shots import SITE_IMAGES               # noqa: E402
from video_automation.longform import thumb as T                    # noqa: E402

OUT = Path.home() / "Desktop/covers-2026-11-17"
P = STOCK / "photos"

# video id -> (key, what it was, why it changed)
VIDEOS = {
    "new-tinnitus": "3n3KPmdA-GU",
    "sleep": "VdblYzRqvog",
    "spike": "hZyBrsZdeRc",
    "eight-suspects": "0UR3tplqSg0",
    "jaw": "9RsZalv6zC8",
    "meme": "TInwuo0aYrs",
    "rug-pull": "3OEIkWZNxN0",
}


def _module(rel: str):
    path = REPO / "projects" / rel
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def new_tinnitus(out: Path) -> Path:
    # Title: "Ringing in Your Ears That Won't Stop? What to Do in the First
    # Week". The man holding his head goes; the night that usually starts it
    # comes in. The cover asks when it began, the title what to do.
    return T.render_thumb(out, TINNITUS, "Ringing\nsince last\n[night?]",
                          image=P / "concert-crowd-phone-lights-dark/10063270.jpg",
                          accent="red", side="left", crop_at=(0.6, 0.5))


def sleep(out: Path) -> Path:
    # Title: "How to Sleep With Tinnitus: Why Is It Worse at Night?". The old
    # words were an instruction - the answer. Same bedroom, same crop.
    return T.render_thumb(out, TINNITUS, "Quieter room,\nlouder\n[ringing?]",
                          image=P / "woman-sleeping-beside-smartphone/9787924.jpg",
                          accent="red", side="left", crop_at=(0.0, 0.0))


def spike(out: Path) -> Path:
    # Title: "Why Does Tinnitus Suddenly Get Louder? Tinnitus Spikes
    # Explained". No person: a calm line with one red spike, drawn - the
    # subject is invisible, so it is drawn (`projects/tinnitus.md`).
    W, H = 1280, 720
    im = Image.new("RGB", (W, H), (10, 11, 15))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(glow)
    d.ellipse([820, 60, 1240, 480], fill=(70, 12, 14))
    im = Image.blend(im, glow.filter(ImageFilter.GaussianBlur(120)), 0.9)
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    for y in range(140, 680, 90):                       # a faint ruled ground
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 18), width=1)
    base_y = 560
    calm = [(x, base_y + (6 if (x // 40) % 2 else -6)) for x in range(820, 960, 20)]
    spike_pts = [(960, base_y), (1000, base_y - 30), (1030, 130), (1062, base_y + 40),
                 (1095, base_y - 10), (1125, base_y)]
    tail = [(x, base_y + (5 if (x // 40) % 2 else -5)) for x in range(1145, W + 20, 20)]
    d.line(calm, fill=(235, 235, 240, 255), width=9, joint="curve")
    d.line([calm[-1]] + spike_pts + tail[:1], fill=(255, 62, 48, 255), width=11, joint="curve")
    d.line(tail, fill=(235, 235, 240, 255), width=9, joint="curve")
    blur = lay.filter(ImageFilter.GaussianBlur(10))
    im = im.convert("RGBA")
    im.alpha_composite(blur)
    im.alpha_composite(lay)
    im = im.convert("RGB")
    fill, ink = T.ACCENTS["red"]
    T._headline(im, "Louder\nfor no\n[reason?]", 132, 560, 56, fill, ink,
                max_lines=3, band="middle", margin=40, shadow=12, drop=(5, 7))
    im.save(out, quality=92)
    return out


def eight_suspects(out: Path) -> Path:
    # Title: "8 Things Blamed for Making Tinnitus Worse - Most Are Innocent".
    # The editor's line-up format (`thumb.lineup_cover`, kept 2026-11-13 "for
    # future videos"), with the number on the plate. Same suspects as the
    # video's own runner-up: the mug, the "?" silhouette, the wine glass.
    m = _module("tinnitus-long/what-makes-tinnitus-worse.py")
    suspects = [(m._cut(m.MUG), 0.40), (None, 0.62), (m._wine_glass(), 0.74)]
    T.lineup_cover(suspects, "Tinnitus:\n[8 suspects]").convert("RGB").save(out, quality=92)
    return out


def jaw(out: Path, cut: float = 0.22, feather: int = 90) -> Path:
    # The editor's pick (2026-11-17, replacing a side-on man the same day):
    # a woman running a facial roller along her jawline (Pexels 6762719, Tima
    # Miroshnichenko). The jaw is literally the subject, nobody holds their
    # head. The photo is height-fitted, its left `cut` (hair) trimmed, set
    # against the right edge, and its own light-grey wall continues across
    # the left for dark rows - the flat-light-ground rule in thumbnails.md.
    import numpy as np
    photo = P / "woman-facial-roller-jaw/6762719.jpg"
    src = Image.open(photo).convert("RGB")
    src = src.resize((int(src.width * 720 / src.height), 720), Image.LANCZOS)
    src = src.crop((int(src.width * cut), 0, src.width, 720))
    wall = np.asarray(src.crop((src.width - 60, 20, src.width - 10, 200))).reshape(-1, 3).mean(0)
    ground = Image.new("RGB", (1280, 720), tuple(int(v) for v in wall))
    x = 1280 - src.width
    im = ground.copy()
    im.paste(src, (x, 0))
    m = np.zeros((1, 1280), np.float32)
    m[0, :x] = 1.0
    m[0, x:x + feather] = np.linspace(1.0, 0.0, feather)
    mask = Image.fromarray((np.repeat(m, 720, 0) * 255).astype("uint8"))
    im = Image.composite(ground, im, mask)
    fill, ink = T.ACCENTS["red"]
    T._headline(im, "Clench\nyour\njaw.\n[Louder?]", 170, x - 100, 40,
                fill, ink, max_lines=4, band="middle", margin=36, shadow=0,
                drop=(0, 0), text=(20, 20, 20))
    im.save(out, quality=92)
    return out

def meme(out: Path) -> Path:
    # Title: "Why Is Dogecoin Worth Billions? How Meme Coins Get Their Price".
    # The grinning Shiba stays; the words carry the number from the video's
    # own opener ($90B, Dogecoin at its peak, May 2021).
    m = _module("crypto-long/what-are-memecoins.py")
    m.HEADLINE = "$90 billion\nfor a\n[joke?]"
    return m.thumbs(out)


def rug_pull(out: Path) -> Path:
    # Title: "What Is a Rug Pull? How to Spot One Before Your Money Vanishes".
    # Same hooded figure and crop; the cover carries the stake, not the
    # title's question.
    return T.render_thumb(out, CRYPTO, "Gone in\n[minutes?]",
                          image=SITE_IMAGES / "posts/hacker.jpg",
                          accent="yellow", side="left", crop_at=(0.70, 0.32))


COVERS = {
    "new-tinnitus": new_tinnitus,
    "sleep": sleep,
    "spike": spike,
    "eight-suspects": eight_suspects,
    "jaw": jaw,
    "meme": meme,
    "rug-pull": rug_pull,
}


def main(keys: list[str]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for k in keys or list(COVERS):
        print(COVERS[k](OUT / f"{k}.jpg"))


if __name__ == "__main__":
    main(sys.argv[1:])
