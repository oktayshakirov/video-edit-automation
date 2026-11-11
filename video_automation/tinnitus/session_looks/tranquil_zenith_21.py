"""The look for `tranquil-zenith-21-breathing` (long + Short), and only that.

`ZenithSea`: a night sky over a sea of clouds. Stars thin out towards the
horizon, a faint light falls from straight overhead (the zenith the track is
named for), and below the horizon two sheets of cloud, drawn in perspective,
sway round closed circles in opposite phase, silver-blue on top and dark in
the gaps, fading into a pale band where they meet the sky. The horizon sits
below the path guide's line in both layouts, so the line runs over dark sky.
Fully generated: no stock, no licence, no credit.

It answers the album's last session look (the nebula, `nebula-pulse-478`):
a quiet landscape instead of deep space, and cool silver instead of purple.

The look does not read the breath: the path guide draws both phases.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.tranquil_zenith_21 import ZenithSea
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Fireflies, Look, Mist, fbm, orbit, vignette


class ZenithSea(Look):
    """Stars and a zenith glow over a perspective sea of swaying clouds."""

    ring = (226, 236, 255)
    ZEN = np.array([6, 8, 26], np.float32)            # straight up
    MID = np.array([18, 24, 60], np.float32)
    LOW = np.array([62, 64, 112], np.float32)         # just above the horizon
    GLOW = np.array([150, 158, 210], np.float32)      # the horizon band
    CLOUD = np.array([176, 188, 226], np.float32)     # moonlit tops
    GAP = np.array([16, 20, 46], np.float32)          # between the clouds

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        self.yh = int(h * (0.67 if w >= h else 0.64))
        yh = self.yh
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

        # Sky: zenith to horizon, a soft band of light where the clouds meet it.
        s = np.clip(yy / max(yh, 1), 0, 1)[..., None]
        sky = (self.ZEN * (1 - s) ** 2 + self.MID * 2 * s * (1 - s)
               + self.LOW * s ** 2)
        band = np.exp(-((yy - yh) / (0.06 * h)) ** 2)[..., None]
        sky += band * (self.GLOW - sky) * 0.45
        # Light from straight overhead: a wide soft fall from the top centre.
        zg = np.exp(-(((xx - w / 2) / (0.55 * w)) ** 2
                      + (yy / (0.55 * h)) ** 2))[..., None]
        sky += zg * np.array([34, 40, 74], np.float32)
        self.sky = sky.astype(np.float32)

        # Stars, fewer and dimmer towards the horizon, on a closed drift.
        rng = np.random.default_rng(2121)
        pad = 60
        big = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
        n = max(8, int(big.size / 1900))
        ys = rng.integers(0, big.shape[0], n)
        xs = rng.integers(0, big.shape[1], n)
        big[ys, xs] = rng.uniform(0.10, 1.0, n) ** 2.6
        stars = cv2.GaussianBlur(big, (0, 0), 0.7) * 3.0
        stars += cv2.GaussianBlur(big, (0, 0), 2.0) * 1.4
        self.stars = (np.clip(stars, 0, 1) * 255).astype(np.uint8)
        self.starmask = (np.clip(1 - yy / max(yh * 0.92, 1), 0, 1) ** 0.8
                         )[..., None].astype(np.float32)
        self.veil = Mist(w, h, 41, octaves=5, lo=0.50, gain=1.6,
                         pad=(max(8, w // 6), max(8, h // 6)))

        # Clouds: a ground plane seen from just above it. A screen row `dy`
        # pixels under the horizon lies at depth 1/dy, so the texture is read
        # at u = x/dy, v = 1/dy - flattened near the horizon, as a real sea
        # of cloud is. Both textures wrap both ways, so the far rows can run
        # past the texture without a seam.
        rows = h - yh
        dy = np.arange(rows, dtype=np.float32) + 3.0
        T, seam = 1024, 96
        self.T = T - seam
        self.layers = []
        for seed in (51, 52):
            tex = fbm(T, T, 5, np.random.default_rng(seed))
            ramp = np.linspace(0, 1, seam, dtype=np.float32)
            tex[:, :seam] = tex[:, :seam] * ramp[None] + tex[:, T - seam:] * (1 - ramp[None])
            tex[:seam] = tex[:seam] * ramp[:, None] + tex[T - seam:] * (1 - ramp[:, None])
            self.layers.append(np.ascontiguousarray(tex[:T - seam, :T - seam]))
        near = 0.42 * 1920 / max(w, h)                # texture px per screen px
        A = near * (rows + 3.0)
        F = 0.85 * max(w, h)                          # focal length, px
        self.mapx0 = (self.T / 2 + (xx[yh:] - w / 2) * (A / dy)[:, None]
                      ).astype(np.float32)
        self.mapy0 = np.repeat(((A * F) / dy)[:, None], w, 1).astype(np.float32)
        d = (dy - 3.0) / rows                         # 0 at the horizon
        self.fog = np.exp(-d / 0.13)[:, None, None].astype(np.float32)
        self.lit = (0.62 + 0.38 * d)[:, None, None].astype(np.float32)

        self.dust = Fireflies(w, max(8, int(yh * 0.8)), 9, 23,
                              color=(220, 230, 255), margin=(0.06, 0.08),
                              r=(1, 3))
        self.vig = vignette(w, h, 0.42)

    def _sheet(self, i, t, k_phase, rad):
        P = self.period
        a = TAU * t / P + k_phase
        du = rad * math.cos(a)
        dv = rad * 0.35 * math.sin(a)
        return cv2.remap(self.layers[i], (self.mapx0 + du) % self.T,
                         (self.mapy0 + dv) % self.T, cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_WRAP)

    def at(self, t):
        P = self.period
        t = t % P          # exact: at(t) and at(t + P) are the same frame
        f = self.sky.copy()
        st = orbit(self.stars, self.w, self.h, t, P, 14).astype(np.float32)
        tw = 0.85 + 0.15 * math.sin(TAU * 3 * t / P)
        f += st[..., None] * self.starmask * 0.85 * tw
        f += (self.veil.at(t, P, 1, 40)[..., None] * self.starmask
              * np.array([40, 46, 90], np.float32) * 0.35)
        self.dust.draw(f[:self.dust.h], t, P, 0.30)

        # Two sheets in opposite phase, so the sea seems to roll rather than
        # slide, and both are back where they started at the end of the loop.
        a = self._sheet(0, t, 0.0, 46)
        b = self._sheet(1, t, math.pi, 64)
        dens = np.clip((0.62 * a + 0.48 * b - 0.34) * 2.2, 0, 1)[..., None]
        relief = np.clip((a - b) * 1.6 + 0.6, 0.25, 1.0)[..., None]
        sea = self.GAP * (1 - dens) + self.CLOUD * relief * self.lit * dens
        horizon = f[self.yh:self.yh + 1]
        sea = sea * (1 - self.fog) + (horizon * 0.6 + self.GLOW * 0.4) * self.fog
        f[self.yh:] = sea
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
