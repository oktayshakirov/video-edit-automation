"""The look for `low-gravity-box-breathing` (long + Short), and only that.

`LowOrbit`: the view from a slow orbit. A star field on a closed drift, the
dark limb of a planet across the bottom of the frame with a thin blue
atmosphere glowing along its edge, cloud bands sliding across its face, and
a few motes of dust floating as if nothing pulls them down. The bed is "Low
Gravity" from the Quiet Universe album, so the picture is space - but not the
channel's nebula and not `StarPulse`'s centre glow: the light here lives on
the horizon, under the box guide, and the centre stays dark for it. Fully
generated: no stock, no licence, no credit.

The look does not read the breath. The box guide draws all four phases, and
`looks.make` passes only `(inhale, hold, exhale)`, so a look that validated
the period against that sum would raise on box breathing's `rest`.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.low_gravity_box import LowOrbit
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Fireflies, Look, Mist, orbit, vignette


class LowOrbit(Look):
    """Stars, a planet's limb with its atmosphere, drifting cloud and dust."""

    ring = (222, 234, 255)
    DEEP = np.array([3, 6, 15], np.float32)
    SURFACE = np.array([14, 30, 52], np.float32)       # night side
    LIT = np.array([70, 120, 170], np.float32)         # sunlit crescent
    CLOUD = np.array([150, 175, 210], np.float32)
    AIR = np.array([90, 150, 255], np.float32)         # atmosphere glow
    GALAXY = np.array([70, 62, 110], np.float32)       # muted violet band
    DAWN = np.array([150, 170, 230], np.float32)

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        rng = np.random.default_rng(1024)
        pad = 120
        big = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
        n = int(big.size / 2300)
        ys = rng.integers(0, big.shape[0], n)
        xs = rng.integers(0, big.shape[1], n)
        big[ys, xs] = rng.uniform(0.12, 1.0, n) ** 2.4
        stars = cv2.GaussianBlur(big, (0, 0), 0.7) * 3.0
        stars += cv2.GaussianBlur(big, (0, 0), 2.0) * 1.6
        self.stars = (np.clip(stars, 0, 1) * 255).astype(np.uint8)

        # The limb: a circle far larger than the frame, its top at 80% height.
        R = 1.25 * max(w, h)
        cx, cy = w * 0.5, h * 0.80 + R
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) - R    # <0 inside
        self.inside = np.clip(0.5 - d / 2.0, 0, 1)[..., None]
        depth = np.clip(-d, 0, None)
        s = 0.12 * h
        # Lit from upper left: the crescent is brightest left of centre.
        side = np.clip(0.55 - 0.45 * (xx - w * 0.35) / w, 0.15, 1.0)
        self.lit = (np.exp(-depth / s) * side)[..., None]
        self.cloudmask = ((0.35 + 0.65 * np.exp(-depth / (0.30 * h))) * side
                          )[..., None] * self.inside
        above = np.clip(d, 0, None)
        self.air = (np.exp(-above / (0.045 * h)) * (0.4 + 0.6 * side)
                    * (1 - self.inside[..., 0]))[..., None]
        self.rim = (np.exp(-np.abs(d) / (0.006 * h)) * side)[..., None]
        # Stars stop at the planet; the far side of it has none.
        self.sky = 1 - self.inside
        # Dawn just past the limb, left of centre, where the light comes from.
        sx, sy = w * 0.30, h * 0.80 + R - math.sqrt(R ** 2 - (w * 0.20) ** 2)
        sd = np.sqrt(((xx - sx) / (0.55 * max(w, h))) ** 2
                     + ((yy - sy) / (0.16 * max(w, h))) ** 2)
        self.dawn = np.exp(-sd ** 2 * 3.0)[..., None] * self.sky
        # A faint band of the galaxy, corner to corner, behind the stars.
        diag = ((xx - w * 0.5) * 0.45 + (yy - h * 0.35)) / max(w, h)
        self.band = np.exp(-(diag / 0.16) ** 2)[..., None] * self.sky
        self.g = Mist(w, h, 43, octaves=5, lo=0.40, gain=1.6, pad=(300, 200))

        self.c1 = Mist(w, h, 41, octaves=5, lo=0.46, gain=2.0, pad=(500, 200))
        self.c2 = Mist(w, h, 42, octaves=4, lo=0.50, gain=2.2, pad=(400, 200))
        self.dust = Fireflies(w, h, 16, 77, color=(190, 210, 255),
                              margin=(0.05, 0.08), r=(2, 5))
        self.vig = vignette(w, h, 0.5)

    def at(self, t):
        P = self.period
        st = orbit(self.stars, self.w, self.h, t, P, 30).astype(np.float32)
        f = self.DEEP + st[..., None] * 0.85 * self.sky
        f = f * (1 - self.inside) + self.inside * (
            self.SURFACE + self.lit * (self.LIT - self.SURFACE))
        cloud = (0.55 * self.c1.at(t, P, 1, 220)
                 + 0.35 * self.c2.at(t, P, 1, 160, math.pi))[..., None]
        f += np.clip(cloud * 1.4 - 0.25, 0, 1) * self.cloudmask \
            * (self.CLOUD - f) * 0.75
        gal = self.g.at(t, P, 1, 90, 0.7)[..., None]
        f += self.band * (0.25 + 0.75 * gal) * self.GALAXY * 0.45
        f += self.dawn * self.DAWN * 0.35
        shimmer = 0.92 + 0.08 * math.sin(TAU * 2 * t / P)
        f += self.air * self.AIR * 0.55 * shimmer
        f += self.rim * np.array([200, 225, 255], np.float32) * 0.55
        self.dust.draw(f, t, P, 0.45)
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
