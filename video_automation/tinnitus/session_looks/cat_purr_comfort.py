"""The re-cover for `cat-purr-comfort-20min` (2026-11-24), and only that.

The video itself still opens on the amber nebula it was rendered with; this
module is its **cover only**. The first cover was that nebula with a small
cat emoji, built before sessions got a picture of their sound (fire, birds,
a fan). The editor: "it doesn't really match the cat purr theme". A sleeping
cat is the sound's own picture, and a cute animal's face beats any stand-in
for it (`docs/video/thumbnails.md`, 2026-10-22).

The photograph: a tabby asleep under a knitted blanket, Pexels 4062842 by
Maria Sanchez,
https://www.pexels.com/photo/brown-tabby-cat-in-white-knit-hat-4062842/ -
read from the stock cache (not in git; re-pull with
`stock.photos("sleeping cat dark cozy")` if missing). The editor picked it
over a sleeping calico (Pexels 33855553), which was brighter at feed size;
the blanket says comfort, which is what the session is.

**Neutral type over a warm photo** (the editor: "change to better neutral
colour for the font"). Cyan fought the fur and the knit, so the plate and
the number are `accent="sand"` and the headline a soft cream
(`head_ink`), on one row (`max_rows=1`).

**The face is placed, not cropped to.** The session cover keeps its headline
in the upper left and the ring right of centre, so the photograph is scaled
no larger than cover size and the face set in the lower left, clear of both. Where
that leaves the frame short of picture, the edge is a blurred mirror of the
photo's own backdrop, never black. `render_session_thumb(block_y=,
scrim_to=)` lifts the headline and keeps the scrim off the face.
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import Look, vignette
from ...core.stock import CACHE


class _SleepingCat(Look):
    """A still photograph with the cat's face at `PLACE` in the frame."""

    ring = (250, 228, 190)          # the video's own soft gold
    SRC = None
    FACE = (0.5, 0.5)               # the face in the source, as a fraction
    PLACE = (0.27, 0.80)            # where it lands in the frame
    ZOOM = 0.8                      # times cover size; under 1 leaves room
    GAIN = 0.85

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        img = cv2.cvtColor(cv2.imread(str(self.SRC)), cv2.COLOR_BGR2RGB)
        ih, iw = img.shape[:2]
        k = max(w / iw, h / ih) * self.ZOOM
        r = cv2.resize(img, (math.ceil(iw * k), math.ceil(ih * k)),
                       interpolation=cv2.INTER_AREA).astype(np.float32)
        p = max(w, h)
        pad = cv2.copyMakeBorder(r, p, p, p, p, cv2.BORDER_REFLECT)
        blur = cv2.GaussianBlur(pad, (0, 0), 40)
        m = np.zeros(pad.shape[:2], np.float32)
        m[p:-p, p:-p] = 1
        m = cv2.GaussianBlur(m, (0, 0), 25)[..., None]
        pad = pad * m + blur * (1 - m)
        x0 = int(self.FACE[0] * r.shape[1] - self.PLACE[0] * w) + p
        y0 = int(self.FACE[1] * r.shape[0] - self.PLACE[1] * h) + p
        f = pad[y0:y0 + h, x0:x0 + w] * self.GAIN * vignette(w, h, 0.45)
        self.frame = np.clip(f, 0, 255).astype(np.uint8)

    def at(self, t):
        return self.frame


class BlanketThumb(_SleepingCat):
    SRC = CACHE / "photos/sleeping-cat-dark-cozy/4062842.jpg"
    FACE = (0.60, 0.62)
    PLACE = (0.30, 0.74)
    ZOOM = 1.0
    GAIN = 0.75
