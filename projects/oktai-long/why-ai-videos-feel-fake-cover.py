"""The cover of "My 89 AI Videos Were Slop. Here's What Fixed Them." -
a before/after split (the concept agreed 2026-11-23, picked again
2026-11-25): the slop on the left, drained of colour under a red cross;
the fix on the right, bright, under a green tick; his cut-out between them,
looking at the slop with a wince (his photo, 2026-11-25); a short line on
top.

    PYTHONPATH=. .venv/bin/python projects/oktai-long/why-ai-videos-feel-fake-cover.py

Writes one cover per text option to `~/Desktop/<name>-cover-<n>.jpg` and a
sheet of all of them, for his pick. The panels are drawn from the video's
own pieces at full size: the stock clip with its big label (the slop he
made) and the voice waveforms (what he made instead).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from video_automation.core.brand import OKTAI  # noqa: E402
from video_automation.core.frame import LANDSCAPE  # noqa: E402
from video_automation.crypto.shots import Shot  # noqa: E402
from video_automation.longform.beats import make_beat  # noqa: E402
from video_automation.longform.thumb import stack_headline  # noqa: E402
from video_automation.oktai import folder  # noqa: E402

W, H = 1280, 720
RED, GREEN = (235, 64, 52), (74, 200, 120)
# His options to pick from (2026-11-25: "give me more options for the text
# instead of 'mine was slop'"). `[bracket]` sets a word on a plate.
TEXTS = ["MINE WAS [SLOP]", "[SLOP] TO THIS", "WHAT FIXED IT", "89 VIDEOS OF [SLOP]",
         "I MADE [SLOP]", "5 FIXES"]


def _long():
    p = Path(__file__).with_name("why-ai-videos-feel-fake.py")
    spec = importlib.util.spec_from_file_location("long", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _frame(shot: Shot, hold: float = 3.0, at: float = 0.8, reveals=None) -> Image.Image:
    shot.start, shot.hold = 0.0, hold
    shot.reveals = reveals
    beat = make_beat(shot, OKTAI, LANDSCAPE)
    return beat.draw(at).convert("RGB")


def _cover(img: Image.Image, w: int, h: int, ax: float = 0.5) -> Image.Image:
    k = max(w / img.width, h / img.height)
    im = img.resize((int(img.width * k) + 1, int(img.height * k) + 1), Image.LANCZOS)
    x = int((im.width - w) * ax)
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def _slop(panel: Image.Image) -> Image.Image:
    """Drained of colour and tinted red, a cross over it."""
    a = np.asarray(panel).astype(np.float32)
    grey = a.mean(axis=2, keepdims=True)
    a = grey * 0.62 + np.array(RED, np.float32) * 0.16
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(out)
    cx, cy, r = out.width * 0.42, out.height * 0.56, out.height * 0.24
    w = int(out.height * 0.05)
    for p, q in (((cx - r, cy - r), (cx + r, cy + r)), ((cx + r, cy - r), (cx - r, cy + r))):
        d.line([p, q], fill=RED, width=w)
        for x, y in (p, q):
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=RED)
    return out


def _fixed(panel: Image.Image) -> Image.Image:
    """Bright, a tick in a ring."""
    a = np.asarray(panel).astype(np.float32) * 1.25 + 8
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(out, "RGBA")
    cx, cy, r = out.width * 0.80, out.height * 0.30, out.height * 0.13
    w = int(out.height * 0.035)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*GREEN, 70), outline=GREEN, width=w)
    pts = [(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.10, cy + r * 0.36), (cx + r * 0.50, cy - r * 0.32)]
    d.line(pts, fill=GREEN, width=w, joint="curve")
    return out


def build(text: str, out: Path, L, face: Image.Image) -> Path:
    # The slop: the overcorrection's stock clip with its big label.
    slop = _frame(Shot(clip=L.CODE, payload=("", "QUANTUM COMPUTERS")), at=0.9)
    # The fix: his voice as waveforms, both rows lit.
    voice = Shot(graphic="voice", ground="grid", payload=(L.VOICES[:2],))
    fix = _frame(voice, hold=10.0, at=0.95, reveals=[0.2, 1.0])

    half = W // 2
    base = Image.new("RGB", (W, H), OKTAI.bg)
    base.paste(_slop(_cover(slop, half, H, 0.45)), (0, 0))
    base.paste(_fixed(_cover(fix, half, H, 0.75)), (half, 0))
    d = ImageDraw.Draw(base)
    d.rectangle([half - 3, 0, half + 3, H], fill=(10, 10, 14))

    # A dark band at the top for the line.
    band = Image.new("L", (W, H), 0)
    bd = ImageDraw.Draw(band)
    for y in range(240):
        bd.line([(0, y), (W, y)], fill=int(210 * (1 - y / 240) ** 1.4))
    base.paste(Image.new("RGB", (W, H), (6, 6, 10)), (0, 0), band)

    # Him, between the two, looking at the slop.
    fh = int(H * 0.86)
    f = face.resize((int(face.width * fh / face.height), fh), Image.LANCZOS)
    glow = Image.new("RGBA", (f.width + 80, f.height + 80), (0, 0, 0, 0))
    glow.paste((0, 0, 0, 255), (40, 40), f.getchannel("A"))
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    fx = half - f.width // 2 + int(W * 0.04)
    fy = H - f.height + 6
    base.paste(glow, (fx - 40, fy - 30), glow)
    base.paste(f, (fx, fy), f)

    stack_headline(base, [text], (40, 18, W - 80, 150), max_size=120, weight=900)
    base.save(out, quality=92)
    return out


def main() -> None:
    L = _long()
    face = Image.open(folder(L.NAME) / "cover" / "oktay-cutout.png").convert("RGBA")
    desk = Path.home() / "Desktop"
    outs = [build(t, desk / f"{L.NAME}-cover-{i + 1}.jpg", L, face)
            for i, t in enumerate(TEXTS)]
    sheet = Image.new("RGB", (W, (H // 2) * -(-len(outs) // 2)), (30, 30, 30))
    for i, p in enumerate(outs):
        im = Image.open(p).resize((W // 2, H // 2))
        sheet.paste(im, ((i % 2) * (W // 2), (i // 2) * (H // 2)))
    sheet.save(desk / f"{L.NAME}-covers.jpg", quality=88)
    print(desk / f"{L.NAME}-covers.jpg")


if __name__ == "__main__":
    main()
