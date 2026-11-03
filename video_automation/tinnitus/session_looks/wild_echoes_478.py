"""The look for `wild-echoes-478-breathing` (long + Short), and only that.

`fern-breath` from the 2026-10-15 test round: a dark jungle-palm photograph
that zooms in and comes into focus on the inhale, with fireflies. Pexels
27286261 by Nothing Ahead
(https://www.pexels.com/photo/a-close-up-of-a-jungle-with-green-leaves-27286261/),
read from the stock cache, which is not in git - re-pull by that id if it is
missing.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.wild_echoes_478 import FernBreath
"""

from __future__ import annotations

import cv2
import numpy as np

from ...core.looks import Fireflies, Look, cover, ease, orbit, vignette
from ...core.stock import CACHE


class FernBreath(Look):
    """A dark fern photograph that breathes with the ring.

    It zooms in 4.5% and comes into focus on the inhale, holds, and eases back
    out on the exhale — the whole picture follows the pattern, so it needs the
    pattern: `period` must be a whole number of `inhale + hold + exhale`.
    """

    ring = (236, 250, 206)
    SRC = CACHE / "photos/dark-jungle-leaves/27286261.jpg"

    def __init__(self, w, h, period, pattern=(4.0, 0.0, 6.0)):
        super().__init__(w, h, period, pattern or (4.0, 0.0, 6.0))
        inhale, hold, exhale = self.pattern
        breath = inhale + hold + exhale
        if abs(period / breath - round(period / breath)) > 1e-6:
            raise ValueError(f"period {period}s is not a whole number of "
                             f"{breath}s breaths")
        img = cv2.cvtColor(cv2.imread(str(self.SRC)), cv2.COLOR_BGR2RGB)
        big = cover(img, int(w * 1.12), int(h * 1.12)).astype(np.float32)
        big *= 0.72 * np.array([0.9, 1.0, 0.95], np.float32)
        self.big = np.clip(big, 0, 255).astype(np.uint8)
        self.soft = cv2.GaussianBlur(self.big, (0, 0), 6)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        pool = 1 - 0.45 * np.exp(-(((xx - w / 2) / 520) ** 2 + ((yy - h / 2) / 420) ** 2))
        self.shade = vignette(w, h, 0.65) * pool[..., None]
        self.ff = Fireflies(w, h, 22, 13, color=(255, 236, 170), r=(2, 6))

    def _r(self, t):
        i, hd, e = self.pattern
        p = t % (i + hd + e)
        if p < i:
            return ease(p / i)
        if p < i + hd:
            return 1.0
        return 1.0 - ease((p - i - hd) / e)

    def at(self, t):
        r = self._r(t)
        z = 1.0 + 0.045 * r
        f = orbit(self.big, self.w, self.h, t, self.period, 22, z).astype(np.float32)
        b = orbit(self.soft, self.w, self.h, t, self.period, 22, z).astype(np.float32)
        f = (b + (f - b) * (0.45 + 0.55 * r)) * self.shade
        self.ff.draw(f, t, self.period, 0.7)
        return np.clip(f, 0, 255).astype(np.uint8)
