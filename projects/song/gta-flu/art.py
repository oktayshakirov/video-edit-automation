"""Thumbnails and the release cover for "GTA Flu".

    .venv/bin/python projects/song/gta-flu/art.py

Writes to ~/Desktop/songs/art/:
  thumb-long.jpg    1280x720, YouTube
  thumb-short.jpg   1080x1920, the Short's cover (YouTube, TikTok)
  cover-3000.jpg    3000x3000 RGB, the DistroKid release cover

Drawn with the video's own pieces (thermometer, plates, palette) so the art and the
video are one look. Thumbnail rules are `docs/video/thumbnails.md`: big rows,
one accent plate, no subline, no watermark, words the title does not say.

**The cover carries no emoji and no logo.** The static emoji glyphs are
Apple's artwork and a store release is commercial use; the game's mark and art are
ruled out by the song repo's `docs/originality.md`. Its only text is the
title, which is what DistroKid allows text on a cover to be.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import video as V  # noqa: E402

OUT = Path.home() / "Desktop/songs/art"


def canvas(w, h, t=0.0, kick=0.35, glow=(0.5, 0.45), hue=V.ACCENT):
    frame = SimpleNamespace(w=w, h=h, name=f"art{w}x{h}", safe_top=0, safe_right=w)
    ctx = V.Ctx(frame, t, kick)
    return ctx, V.background(ctx, hue, glow)


def plate(img, ctx, s, cx, cy, size, fill, ink=(255, 255, 255), rot=0.0, font=V.F_COND):
    """A word on a solid plate, sized from the cap band so caps sit centred."""
    f = V.font(font, size)
    l, top, r, bot = f.getbbox(s.upper() if s.isupper() else s, anchor="ls")
    w = r - l
    cap = -top
    pad_x, pad_y = size * 0.22, size * 0.16
    lab = Image.new("RGBA", (int(w + 2 * pad_x), int(cap + 2 * pad_y)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lab)
    V.rounded(d, (0, 0, lab.width - 1, lab.height - 1), size * 0.12, (*fill, 255))
    d.text((pad_x - l, pad_y + cap), s, font=f, fill=(*ink, 255), anchor="ls")
    V.paste(img, lab, cx, cy, 1.0, rot)
    return lab.size


def row(img, s, cx, cy, size, color=V.INK, font=V.F_COND):
    d = ImageDraw.Draw(img)
    f = V.font(font, size)
    l, top, r, bot = f.getbbox(s, anchor="ls")
    d.text((cx - (r - l) / 2 - l, cy - top / 2), s, font=f, fill=(*color, 255), anchor="ls")
    return r - l


def thumb_long():
    W, H = 1920, 1080
    ctx, img = canvas(W, H, glow=(0.26, 0.5), kick=0.5)
    tx, ty, th = W * 0.20, H * 0.52, 820
    V.thermometer(img, ctx, tx, ty, th, 0.97, hot=True)
    cx = W * 0.64
    bw = row(img, "BOSS,", cx, H * 0.27, 215)
    # the sick face sits with the words it says, not on the thermometer
    with V.emoji_anim.enabled(False):
        V.paste(img, V.emoji("🤒", 230, 0), cx + bw / 2 + 170, H * 0.22, 1.0, -10)
    plate(img, ctx, "I'M SICK", cx, H * 0.53, 235, V.RED, rot=-3)
    row(img, "THE GTA FLU", cx, H * 0.80, 170, V.ACCENT)
    return img.convert("RGB").resize((1280, 720), Image.LANCZOS)


def thumb_short():
    W, H = 1080, 1920
    ctx, img = canvas(W, H, glow=(0.5, 0.5), kick=0.5)
    cx = W / 2
    row(img, "BOSS,", cx, 420, 300)
    plate(img, ctx, "I'M SICK", cx, 720, 250, V.RED, rot=-3)
    V.thermometer(img, ctx, cx, 1200, 620, 0.97, hot=True)
    with V.emoji_anim.enabled(False):
        V.paste(img, V.emoji("🤒", 210, 0), cx + 230, 1350, 1.0, -10)
    row(img, "THE GTA FLU", cx, 1640, 130, V.ACCENT)
    return img.convert("RGB")


def cover():
    W = H = 3000
    ctx, img = canvas(W, H, glow=(0.5, 0.56), kick=0.6)
    cx = W / 2
    row(img, "GTA", cx, 640, 620)
    row(img, "FLU", cx, 1200, 620, V.ACCENT)
    V.thermometer(img, ctx, cx, 2160, 1250, 0.97, hot=True)
    return img.convert("RGB")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn, q in (("thumb-long.jpg", thumb_long, 92), ("thumb-short.jpg", thumb_short, 92),
                        ("cover-3000.jpg", cover, 95)):
        im = fn()
        p = OUT / name
        im.save(p, quality=q, subsampling=0)
        print(f"{p}  {im.size[0]}x{im.size[1]}  {p.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
