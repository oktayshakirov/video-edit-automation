"""The look for `brown-noise-478-breathing` (long + Short), and only that.

`AmberDusk`: a warm dusk over layered hills. The sky runs from a deep
plum-brown overhead to amber at the horizon, a low sun sits half behind the
farthest ridge, and long bands of cloud - stretched wide, lit gold on the
sun's side and dusky mauve away from it - sway round closed circles at two
speeds. Three ridges of hills step down in front, each darker and less hazy
than the one behind it, with a slow mist lying in the valleys. A few stars
come through at the top. Fully generated: no stock, no licence, no credit.

It answers the last cloud look (`ZenithSea`, `tranquil-zenith-21`): warm
brown and amber at dusk instead of cool silver at night, and land under the
sky instead of a sea of cloud - brown, for the brown noise the session leads
with (the bed is *Cloudscape Serenity*, White Noise Therapy album).

The look does not read the breath: the clock guide draws every phase, and a
look that ignores `pattern` builds for the thumbnail without one.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.cloudscape_478 import AmberDusk
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Look, fbm, vignette


def _ridge(w: int, rng: np.random.Generator, base: float, amp: float,
           h: int) -> np.ndarray:
    """A hill profile: y of the ridge top for every column, a few soft sines."""
    x = np.arange(w, dtype=np.float32) / w
    y = np.zeros(w, np.float32)
    for k, a in ((1.3, 1.0), (2.7, 0.5), (5.9, 0.22), (11.0, 0.08)):
        y += a * np.sin(TAU * k * x + rng.uniform(0, TAU))
    return base * h - amp * h * y / 1.8


class _Bands:
    """Cloud bands: fbm stretched wide, sliding round a circle `k` times a period."""

    def __init__(self, w, h, seed, stretch=3.0, lo=0.47, gain=2.2, pad=(420, 160)):
        self.w, self.h = w, h
        tw, th = w + pad[0], h + pad[1]
        tex = fbm(th, max(8, int(tw / stretch)), 5, np.random.default_rng(seed))
        tex = cv2.resize(tex, (tw, th), interpolation=cv2.INTER_CUBIC)
        self.tex = np.clip((tex - lo) * gain, 0, 1).astype(np.float32)

    def at(self, t, period, k, rad, phase=0.0):
        a = TAU * k * t / period + phase
        dx = (self.tex.shape[1] - self.w) / 2 + rad * math.cos(a)
        dy = (self.tex.shape[0] - self.h) / 2 + rad * 0.25 * math.sin(a)
        M = np.float32([[1, 0, -dx], [0, 1, -dy]])
        return cv2.warpAffine(self.tex, M, (self.w, self.h), flags=cv2.INTER_LINEAR)


class AmberDusk(Look):
    """A low sun, banded cloud and three ridges of hills at a warm dusk."""

    ring = (255, 236, 214)
    TOP = np.array([30, 18, 34], np.float32)          # plum-brown overhead
    MID = np.array([96, 50, 52], np.float32)          # dusky rose
    LOW = np.array([214, 128, 66], np.float32)        # amber at the horizon
    SUN = np.array([255, 228, 172], np.float32)
    CLOUD_LIT = np.array([255, 196, 132], np.float32)  # gold, sun side
    CLOUD_DIM = np.array([150, 96, 104], np.float32)    # mauve, away from it
    RIDGES = (np.array([120, 70, 62], np.float32),    # far, hazy
              np.array([66, 38, 36], np.float32),
              np.array([26, 15, 16], np.float32))     # near, almost black

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        land = w >= h
        self.yh = yh = int(h * (0.70 if land else 0.72))
        self.sx = sx = w * (0.74 if land else 0.5)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

        # Sky: overhead to horizon, warmer and brighter towards the sun.
        s = np.clip(yy / max(yh, 1), 0, 1)[..., None]
        sky = (self.TOP * (1 - s) ** 2 + self.MID * 2 * s * (1 - s)
               + self.LOW * s ** 2)
        d = np.sqrt(((xx - sx) / (0.42 * w)) ** 2 + ((yy - yh) / (0.38 * h)) ** 2)
        self.sun_glow = np.exp(-d ** 2)[..., None].astype(np.float32)
        sky += self.sun_glow * np.array([60, 40, 10], np.float32)
        self.sky = sky.astype(np.float32)

        # The sun disc, half behind the far ridge.
        r = 0.055 * min(w, h) * (1.0 if land else 1.6)
        ds = np.sqrt((xx - sx) ** 2 + (yy - (yh - r * 0.15)) ** 2)
        self.disc = (np.clip((r - ds) / 3.0 + 0.5, 0, 1)
                     + 0.5 * np.exp(-(ds / (r * 2.2)) ** 2))[..., None].astype(np.float32)

        # Cloud bands live above the horizon, thinning towards the top.
        band_mask = (np.clip((yy - 0.06 * h) / (0.18 * h), 0, 1)
                     * np.clip((yh - 0.02 * h - yy) / (0.10 * h), 0, 1))
        self.band_mask = band_mask.astype(np.float32)
        # How lit a cloud is: by its distance from the sun, and lower = warmer.
        lit = np.clip(0.35 + 0.65 * np.exp(-(((xx - sx) / (0.6 * w)) ** 2))
                      * (0.35 + 0.65 * s[..., 0]), 0, 1)[..., None]
        self.cloud_col = (self.CLOUD_DIM + (self.CLOUD_LIT - self.CLOUD_DIM) * lit
                          ).astype(np.float32)
        self.b1 = _Bands(w, h, 31, stretch=3.4, lo=0.47, gain=3.0)
        self.b2 = _Bands(w, h, 32, stretch=2.6, lo=0.46, gain=1.8)

        # Three ridges, back to front; each ridge's alpha is a soft edge.
        rng = np.random.default_rng(47)
        self.ridges = []
        for i, (base, amp) in enumerate(((0.71, 0.05), (0.79, 0.07), (0.90, 0.08))):
            top = _ridge(w, rng, base if land else base + 0.01, amp, h)
            a = np.clip((yy - top[None, :]) / 1.5 + 0.5, 0, 1)
            # Haze: each ridge lightens towards its own top.
            haze = np.clip(1 - (yy - top[None, :]) / (0.12 * h), 0, 1) * (0.35 - 0.1 * i)
            self.ridges.append((a[..., None].astype(np.float32),
                                haze[..., None].astype(np.float32),
                                top))
        # Valley mist sits just above the two front ridges.
        vm = np.zeros((h, w), np.float32)
        for _, _, top in self.ridges[1:]:
            vm = np.maximum(vm, np.exp(-((yy - (top[None, :] - 0.01 * h))
                                         / (0.035 * h)) ** 2))
        self.valley = vm
        self.vtex = _Bands(w, h, 33, stretch=4.0, lo=0.40, gain=1.6)

        # A few stars at the top, fixed, twinkling a whole number of times.
        srng = np.random.default_rng(53)
        self.stars = [(int(np.clip(srng.uniform(0.03, 0.97) * w, 5, w - 6)),
                       int(np.clip(srng.uniform(0.01, 0.20) * h, 5, h - 6)),
                       srng.uniform(0.35, 1.0), int(srng.integers(2, 6)),
                       srng.uniform(0, TAU)) for _ in range(34)]
        g = np.zeros((9, 9), np.float32)
        g[4, 4] = 1.0
        g = cv2.GaussianBlur(g, (0, 0), 1.1)
        self.star = (g / g.max())[..., None] * np.array([255, 236, 210], np.float32)
        self.vig = vignette(w, h, 0.5)

    def at(self, t):
        P = self.period
        f = self.sky.copy()

        # Stars, faded out towards the horizon by where they sit.
        for x, y, b, k, ph in self.stars:
            lum = b * (0.45 + 0.55 * math.sin(TAU * k * t / P + ph) ** 2)
            fade = max(0.0, 1 - y / (0.22 * self.h))
            f[y - 4:y + 5, x - 4:x + 5] += self.star * (0.55 * lum * fade)

        # The sun breathes its glow once a loop, very slightly.
        pulse = 0.5 + 0.5 * math.cos(TAU * t / P)
        f += self.sun_glow * (14 + 10 * pulse)
        f += (self.SUN - f) * np.clip(self.disc, 0, 1) * 0.92

        # Cloud: two banded layers in opposite phase.
        c = (0.62 * self.b1.at(t, P, 1, 120)
             + 0.42 * self.b2.at(t, P, 2, 90, math.pi)) * self.band_mask
        c = np.clip(c, 0, 1)[..., None]
        f += (self.cloud_col - f) * c * 0.75

        # Ridges, back to front, with the valley mist between them.
        for i, (a, haze, _) in enumerate(self.ridges):
            col = self.RIDGES[i] + (self.LOW - self.RIDGES[i]) * haze
            f += (col - f) * a
            if i == 1:
                m = (self.vtex.at(t, P, 1, 140, 0.7) * self.valley)[..., None]
                f += (np.array([196, 140, 112], np.float32) - f) * m * 0.22
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
