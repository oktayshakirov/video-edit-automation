"""The look for `nebula-pulse-478-breathing` (long + Short), and only that.

`StarPulse`: deep space that breathes. A star field drifting on a closed
orbit, two sheets of teal and blue dust sliding past at different rates, a
few brighter stars twinkling, and a soft amber core glow behind the ring that swells
on the inhale, holds, and fades on the exhale. The bed is the album's "Nebula
Pulse" track, so the picture is space - but not the channel's default nebula,
which every early session wore re-tinted. Fully generated: no stock, no
licence, no credit.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.nebula_pulse_478 import StarPulse
"""

from __future__ import annotations

import cv2
import numpy as np

from ...core.looks import Fireflies, Look, Mist, ease, orbit, vignette


class StarPulse(Look):
    """Stars, drifting dust and a core glow that follows the breath.

    The glow reads the pattern, so `period` must be a whole number of
    `inhale + hold + exhale`. Everything else closes on `period` directly.
    With no pattern (the session thumbnails build looks at a fixed 60s and
    pass none) the glow holds at its midpoint, which is all a still needs.
    """

    ring = (255, 236, 200)
    DEEP = np.array([4, 12, 18], np.float32)
    DUST_A = np.array([30, 130, 140], np.float32)     # teal
    DUST_B = np.array([40, 80, 150], np.float32)      # deep blue
    GLOW = np.array([255, 190, 120], np.float32)      # warm core

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        if pattern:
            breath = sum(pattern)
            if abs(period / breath - round(period / breath)) > 1e-6:
                raise ValueError(f"period {period}s is not a whole number of "
                                 f"{breath}s breaths")
        rng = np.random.default_rng(478)
        pad = 140
        big = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
        n = int(big.size / 2600)
        ys = rng.integers(0, big.shape[0], n)
        xs = rng.integers(0, big.shape[1], n)
        big[ys, xs] = rng.uniform(0.15, 1.0, n) ** 2.2
        stars = cv2.GaussianBlur(big, (0, 0), 0.7) * 3.0
        stars += cv2.GaussianBlur(big, (0, 0), 2.2) * 2.0
        self.stars = (np.clip(stars, 0, 1) * 255).astype(np.uint8)
        self.d1 = Mist(w, h, 31, octaves=5, lo=0.50, gain=2.2)
        self.d2 = Mist(w, h, 32, octaves=4, lo=0.47, gain=1.8)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        s = min(w, h)
        self.core = np.exp(-(((xx - w / 2) ** 2 + (yy - h / 2) ** 2)
                             / (2 * (0.30 * s) ** 2)))[..., None]
        self.vig = vignette(w, h, 0.6)
        self.tw = Fireflies(w, h, 26, 9, color=(235, 225, 255),
                            margin=(0.03, 0.04), r=(2, 4))

    def _r(self, t):
        if not self.pattern:
            return 0.5
        i, hd, e = self.pattern
        p = t % (i + hd + e)
        if p < i:
            return ease(p / i)
        if p < i + hd:
            return 1.0
        return 1.0 - ease((p - i - hd) / e)

    def at(self, t):
        P = self.period
        st = orbit(self.stars, self.w, self.h, t, P, 40).astype(np.float32)
        f = self.DEEP + st[..., None] * 0.9
        a = self.d1.at(t, P, 1, 160)[..., None]
        b = self.d2.at(t, P, 2, 110, 2.1)[..., None]
        f = f + a * self.DUST_A * 0.55 + b * self.DUST_B * 0.45
        r = self._r(t)
        f = f + self.core * self.GLOW * (0.10 + 0.16 * r)
        self.tw.draw(f, t, P, 0.8)
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
