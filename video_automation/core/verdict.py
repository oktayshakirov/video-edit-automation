"""An editor's mark on a shot: a red cross for the wrong picture, a green
tick for the right one (2026-11-21, the editor's note on the OktAI opener:
"when talking about stock footage, show generic stock footage, then maybe
scratch it or mark it red as wrong - use more such creative approaches").

    Shot(clip=GENERIC, verdict=("wrong", "Says nothing"))
    Shot(image=REAL, verdict=("right", "Names the thing"), verdict_at=0.3)

The picture plays clean first, so the viewer has a moment to read it the
way they would have; at `verdict_at` (a fraction of the shot) a wrong one
drains of colour and takes a red tint while a cross draws across it in two
strokes, and the label stamps in under it. A right one keeps its colour and
gets a tick in a ring. Applied over everything the shot draws, a window
included, so it reads as a mark on the picture rather than part of it.
"""

from __future__ import annotations

import math

import numpy as np
from PIL import Image, ImageDraw, ImageFont

RED = (235, 64, 52)
GREEN = (74, 200, 120)
DRAW = 0.55            # seconds each stroke takes
FONT = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"


def _ease(p: float) -> float:
    p = min(1.0, max(0.0, p))
    return 1 - (1 - p) ** 3


class VerdictShot:
    def __init__(self, inner, spec, start: float, hold: float, frame,
                 at: float = 0.45):
        kind, label = (spec, "") if isinstance(spec, str) else (spec[0], spec[1])
        if kind not in ("wrong", "right"):
            raise ValueError(f"verdict must be 'wrong' or 'right', not {kind!r}")
        self.inner, self.kind, self.label = inner, kind, label
        self.start, self.hold, self.frame, self.at = start, hold, frame, at
        size = int(frame.h * (0.075 if frame.h > frame.w else 0.085))
        self.font = ImageFont.truetype(FONT, size)

    def draw(self, f: float) -> Image.Image:
        pic = self.inner.draw(f)
        t = (f - self.at) * self.hold           # seconds since the mark began
        if t <= 0:
            return pic
        W, H = pic.size
        img = pic.convert("RGB")
        colour = RED if self.kind == "wrong" else GREEN
        if self.kind == "wrong":
            # The picture loses its colour and takes the red, over 0.4 s.
            k = _ease(t / 0.4)
            a = np.asarray(img).astype(np.float32)
            grey = a.mean(axis=2, keepdims=True)
            tint = grey * 0.55 + np.array(RED, np.float32) * 0.18
            a = a * (1 - 0.8 * k) + tint * 0.8 * k
            img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(img, "RGBA")
        cx, cy = W / 2, H * 0.46
        r = min(W, H) * 0.20
        width = max(12, int(min(W, H) * 0.032))
        if self.kind == "wrong":
            for i, ((x0, y0), (x1, y1)) in enumerate(
                    (((cx - r, cy - r), (cx + r, cy + r)),
                     ((cx + r, cy - r), (cx - r, cy + r)))):
                p = _ease((t - i * DRAW * 0.8) / DRAW)
                if p <= 0:
                    continue
                d.line([(x0, y0), (x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)],
                       fill=colour + (240,), width=width)
        else:
            p = _ease(t / (DRAW * 1.4))
            d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour + (int(230 * p),),
                      width=max(6, width // 2))
            pts = [(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.10, cy + r * 0.36),
                   (cx + r * 0.50, cy - r * 0.34)]
            seg = p * 2
            if seg > 0:
                a1 = min(1.0, seg)
                d.line([pts[0], (pts[0][0] + (pts[1][0] - pts[0][0]) * a1,
                                 pts[0][1] + (pts[1][1] - pts[0][1]) * a1)],
                       fill=colour + (240,), width=width)
            if seg > 1:
                a2 = min(1.0, seg - 1)
                d.line([pts[1], (pts[1][0] + (pts[2][0] - pts[1][0]) * a2,
                                 pts[1][1] + (pts[2][1] - pts[1][1]) * a2)],
                       fill=colour + (240,), width=width)
        if self.label:
            p = _ease((t - DRAW * 1.3) / 0.25)
            if p > 0:
                text = self.label.upper()
                tw = d.textlength(text, font=self.font)
                bb = d.textbbox((0, 0), text, font=self.font)
                th = bb[3] - bb[1]
                pad = th * 0.45
                s = 1.25 - 0.25 * p                     # it stamps down
                bw, bh = (tw + 2 * pad) * s, (th + 2 * pad) * s
                bx, by = cx - bw / 2, cy + r + H * 0.05
                d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=int(bh * 0.18),
                                    fill=colour + (int(235 * p),))
                f2 = self.font.font_variant(size=int(self.font.size * s))
                bb2 = d.textbbox((0, 0), text, font=f2)
                d.text((cx - (bb2[2] - bb2[0]) / 2 - bb2[0],
                        by + (bh - (bb2[3] - bb2[1])) / 2 - bb2[1]), text,
                       font=f2, fill=(255, 255, 255, int(255 * p)))
        return img
