"""Drawing primitives shared by every format.

These were private helpers inside `crypto/shots.py`, which was the right home
while the crypto short was the only thing that drew anything. The long-form
engine needs all of them and must not import from a sibling project to get
them, so they live here now. `crypto/shots.py` re-exports the private names it
used, so nothing that referenced them had to change.

The two that carry real hard-won behaviour are `subpixel` and `partial`:

* **`subpixel`** is why a slow move reads as a move. At the speeds used here a
  layer travels tens of pixels a second, so an integer crop jumps a whole pixel
  every few frames and holds still in between — the user's word for the first
  build that did it was "laggy".

* **`partial`** draws the first fraction of a polyline. Marks are built from
  line segments rather than set as glyphs because Futura has neither a tick nor
  a cross and PIL renders both as tofu — invisible in review, obvious in the
  frame. The side effect is that a path can be drawn *partially*, which is what
  lets a mark travel on instead of blinking into existence.
"""

from __future__ import annotations

import math

import cv2
import numpy as np
from PIL import Image, ImageDraw


def ease_out(p: float) -> float:
    """Quadratic ease-out. Fast off the mark, settling — the shape of a UI."""
    p = min(1.0, max(0.0, p))
    return 1.0 - (1.0 - p) ** 2


def cover(img: Image.Image, w: int, h: int) -> Image.Image:
    """Scale-and-crop to fill exactly, preserving aspect."""
    s = max(w / img.width, h / img.height)
    r = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))),
                   Image.LANCZOS)
    return r.crop(((r.width - w) // 2, (r.height - h) // 2,
                   (r.width - w) // 2 + w, (r.height - h) // 2 + h))


def contain(img: Image.Image, w: int, h: int) -> Image.Image:
    """Scale to fit inside a box, preserving aspect. Never upscales.

    The long-form counterpart to `cover`, and the reason the split layout works:
    a 900px photograph dropped into a 700px column is a *downscale*, so the
    resolution problem that dominates the full-frame case disappears entirely.
    """
    s = min(w / img.width, h / img.height, 1.0)
    return img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))),
                      Image.LANCZOS)


def subpixel(arr: np.ndarray, x: float, y: float, w: int, h: int) -> np.ndarray:
    """Crop at a fractional offset. Integer crops judder; this does not."""
    ix, iy = int(x), int(y)
    m = np.float32([[1, 0, ix - x], [0, 1, iy - y]])
    win = arr[iy:iy + h + 1, ix:ix + w + 1]
    return cv2.warpAffine(win, m, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)


def partial(d: ImageDraw.ImageDraw, pts: list[tuple[float, float]], p: float,
            colour: tuple[int, int, int], w: int) -> None:
    """Draw the first `p` of a polyline, measured along its real length."""
    if p <= 0:
        return
    segs = [((pts[i], pts[i + 1]),
             math.dist(pts[i], pts[i + 1])) for i in range(len(pts) - 1)]
    want = sum(L for _, L in segs) * min(1.0, p)
    drawn = [pts[0]]
    for (a, b), L in segs:
        if want >= L:
            drawn.append(b)
            want -= L
            continue
        k = want / L if L else 0.0
        drawn.append((a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k))
        break
    if len(drawn) > 1:
        d.line(drawn, fill=colour, width=w, joint="curve")


def mark(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
         ok: bool, colour: tuple[int, int, int], progress: float = 1.0,
         width: int = 7) -> None:
    """A tick or a cross, drawn from line segments so it can travel on."""
    p = min(1.0, max(0.0, progress))
    if p <= 0:
        return
    if ok:
        # One polyline, so the tick draws in a single stroke: down, then up.
        partial(d, [(x, y + s * 0.55), (x + s * 0.38, y + s * 0.92),
                    (x + s, y + s * 0.08)], p, colour, width)
    else:
        # Two strokes over the same window, the second starting halfway, so the
        # cross reads as two deliberate slashes rather than one shape appearing.
        partial(d, [(x, y), (x + s, y + s)], min(1.0, p * 2), colour, width)
        partial(d, [(x + s, y), (x, y + s)], max(0.0, p * 2 - 1), colour, width)


def wrap(d: ImageDraw.ImageDraw, text: str, font, max_w: float) -> list[str]:
    """Greedy wrap, then pull back a word so the last line is never a widow.

    A single orphaned word on the final line is the tell that separates a
    generated card from a hand-set one.
    """
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    while len(lines) > 1 and len(lines[-1].split()) < 2:
        prev = lines[-2].split()
        if len(prev) < 3:
            break
        lines[-1] = f"{prev[-1]} {lines[-1]}"
        lines[-2] = " ".join(prev[:-1])
    return lines
