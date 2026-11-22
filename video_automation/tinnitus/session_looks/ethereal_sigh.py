"""The look for `white-noise-sigh-breathing` (long + Short), and only that.

`AuroraSnow`: a winter night in the mountains. A deep blue sky full of
faint stars, two curtains of aurora - green at their lower hem, fading to
teal and a little violet as they rise - folding slowly across it, a far
snowy range lit pale by them, a darker near ridge, and snow falling through
all of it in two depths, the near flakes larger and quicker. Fully
generated: no stock, no licence, no credit.

It answers the bed and the last three looks: the track is *Ethereal
Resonance* (the white-noise album), so the picture is white and ethereal -
snow and an aurora; `AmberDusk` (`brown-noise-478`) was hills at dusk,
`NightDraft` (`fan-noise-444`) a room at night and `RoseMere`
(`pink-noise-box`) a lake at dawn, so this is the first winter picture on
the channel, and the first aurora.

The look does not read the breath: the path guide draws every phase, and a
look that ignores `pattern` builds for the thumbnail without one. Every
motion runs a whole number of times per period on `t % period`.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.ethereal_sigh import AuroraSnow
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Look, fbm, vignette


class AuroraSnow(Look):
    """An aurora over a snowy range, with snow falling in two depths."""

    ring = (236, 250, 246)
    TOP = np.array([6, 10, 28], np.float32)           # deep night overhead
    LOW = np.array([22, 44, 74], np.float32)          # blue towards the peaks
    GREEN = np.array([96, 255, 170], np.float32)      # the aurora's hem
    TEAL = np.array([60, 190, 220], np.float32)
    VIOLET = np.array([150, 110, 230], np.float32)    # its upper fringe
    FAR = np.array([150, 176, 206], np.float32)       # far range, snow lit pale
    NEAR = np.array([22, 30, 48], np.float32)         # near ridge, in shadow
    SNOW = np.array([236, 244, 255], np.float32)

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        land = w >= h
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        rng = np.random.default_rng(81)
        x = np.arange(w, dtype=np.float32) / w

        # The sky, and stars that twinkle a whole number of times a period.
        v = (yy / h)[..., None]
        self.sky = (self.TOP + (self.LOW - self.TOP) * np.clip(v / 0.75, 0, 1) ** 1.3)
        n = int(w * h / 5200)
        self.stars = np.stack([rng.uniform(0, w, n), rng.uniform(0, 0.62 * h, n),
                               rng.uniform(0.25, 1.0, n), rng.integers(1, 4, n),
                               rng.uniform(0, TAU, n)], 1).astype(np.float32)

        # Two ridges. Heights as a fraction of h from the top.
        def ridge(seed, base, amp, keys):
            r = np.random.default_rng(seed)
            y = np.zeros(w, np.float32)
            for k, a in keys:
                # 1 - |sin| has a cusp at every crest: peaks, not hills
                y += a * (1 - np.abs(np.sin(math.pi * k * x + r.uniform(0, TAU))))
            y = y / sum(a for _, a in keys)
            return (base - amp * (y - 0.5) * 2) * h

        far_base = 0.70 if land else 0.66
        near_base = 0.84 if land else 0.80
        self.far_top = ridge(82, far_base, 0.13 if land else 0.08, ((1.3, 1.0), (3.1, 0.5), (7.7, 0.25),
                                                  (19.0, 0.10), (47.0, 0.04)))
        self.near_top = ridge(83, near_base, 0.07 if land else 0.045, ((0.9, 1.0), (2.3, 0.6), (5.9, 0.3),
                                                    (17.0, 0.10), (41.0, 0.05)))
        far = np.clip((yy - self.far_top[None, :]) / 1.5, 0, 1)
        near = np.clip((yy - self.near_top[None, :]) / 1.5, 0, 1)
        # The far range: snow, brightest near its crest, with soft ridged
        # shading from a noise stretched tall.
        below = np.clip((yy - self.far_top[None, :]) / (0.16 * h), 0, 1)
        shade = fbm(h // 4, w // 4, 4, np.random.default_rng(84))
        shade = cv2.resize(cv2.resize(shade, (w // 6, h // 2)), (w, h))
        farcol = (self.FAR * (1.0 - 0.62 * below[..., None] ** 0.8)
                  * (0.70 + 0.50 * shade[..., None]))
        nearcol = self.NEAR * (0.9 + 0.25 * shade[..., None])
        # A rim of snow on the near ridge's crest, catching the aurora.
        rim = np.exp(-((yy - self.near_top[None, :] - 3) / 5.0) ** 2)
        nearcol = nearcol + (self.FAR * 0.45 - nearcol) * rim[..., None]
        self.land_far = far[..., None].astype(np.float32)
        self.land_near = near[..., None].astype(np.float32)
        self.farcol = farcol.astype(np.float32)
        self.nearcol = nearcol.astype(np.float32)

        # The aurora is soft, so it is computed at quarter scale.
        self.sw, self.sh = w // 4, h // 4
        sy, sx = np.mgrid[0:self.sh, 0:self.sw].astype(np.float32)
        self.ax = sx / self.sw
        self.ay = sy / self.sh
        # The rays: two profiles across the width, each a sum of whole-number
        # sines so it wraps seamlessly, blended from the hem upwards. The
        # texture must be exactly one frame wide and periodic: an fbm twice
        # the width snapped the rays at every loop join (2026-11-22).
        xs = np.arange(self.sw, dtype=np.float32) / self.sw
        r2 = np.random.default_rng(85)

        def profile():
            p = np.zeros(self.sw, np.float32)
            for k in range(3, 64):
                p += r2.normal() / k ** 0.6 * np.sin(TAU * k * xs + r2.uniform(0, TAU))
            p = (p - p.min()) / (p.max() - p.min())
            return np.clip((p - 0.35) * 1.8, 0.15, 1)

        rays = profile()[None, :] * (1 - self.ay) + profile()[None, :] * self.ay
        self.rays = rays.astype(np.float32)
        self.cur = [dict(base=0.40 if land else 0.36, amp=0.06, k=(1.0, 2.3), drift=1,
                         gain=1.0, ph=rng.uniform(0, TAU)),
                    dict(base=0.30 if land else 0.27, amp=0.05, k=(1.6, 3.1), drift=-1,
                         gain=0.6, ph=rng.uniform(0, TAU))]
        self.glow_y = np.exp(-((yy / h - (far_base - 0.10)) / 0.18) ** 2)[..., None]

        # Snow: flakes on wrapping falls, two depths. Each falls a whole
        # number of frame heights a period and sways a whole number of times.
        self.flakes = []
        for depth, count, k, r in ((0, int(160 * w * h / 2073600), 1, 1.6),
                                   (1, int(70 * w * h / 2073600), 2, 3.2)):
            for _ in range(count):
                self.flakes.append((rng.uniform(0, w), rng.uniform(0, 1), k,
                                    rng.uniform(8, 30) * (1 + depth),
                                    int(rng.integers(1, 4)), rng.uniform(0, TAU),
                                    depth, rng.uniform(0.55, 1.0)))
        self.sprites = []
        for r in (1.6, 3.2):
            s = int(r * 6) | 1
            g = np.zeros((s, s), np.float32)
            cv2.circle(g, (s // 2, s // 2), max(1, int(r / 2)), 1.0, -1)
            g = cv2.GaussianBlur(g, (0, 0), r * 0.7)
            self.sprites.append(g / g.max())

        self.vig = vignette(w, h, 0.50)

    def _aurora(self, ph: float) -> np.ndarray:
        """Curtain light at quarter scale, (sh, sw, 3)."""
        out = np.zeros((self.sh, self.sw, 3), np.float32)
        X, Y = self.ax, self.ay
        for c in self.cur:
            k1, k2 = c["k"]
            hem = (c["base"]
                   + c["amp"] * np.sin(TAU * k1 * X[0] + ph * c["drift"] + c["ph"])
                   + 0.4 * c["amp"] * np.sin(TAU * k2 * X[0] - 2 * ph * c["drift"]))
            above = hem[None, :] - Y                     # >0 above the hem
            lit = np.where(above > 0, np.exp(-above / 0.16),
                           np.exp(-(above / 0.035) ** 2))
            # The rays slide along the curtain, once round a period.
            shift = (ph / TAU * self.sw * c["drift"]) % self.sw
            M = np.float32([[1, 0, -shift], [0, 1, 0]])
            rays = cv2.warpAffine(self.rays, M, (self.sw, self.sh),
                                  flags=cv2.INTER_LINEAR,
                                  borderMode=cv2.BORDER_WRAP)
            # Brightness wanders along the curtain so it never reads as a band.
            along = 0.55 + 0.45 * np.sin(TAU * 1.0 * X[0] - ph * c["drift"] + c["ph"]) ** 2
            a = (lit * rays * along[None, :] * c["gain"])[..., None]
            u = np.clip(above / 0.28, 0, 1)[..., None]
            col = np.where(u < 0.5, self.GREEN + (self.TEAL - self.GREEN) * (u * 2),
                           self.TEAL + (self.VIOLET - self.TEAL) * (u * 2 - 1))
            out += col * a
        return out

    def at(self, t):
        t = t % self.period
        P, h, w = self.period, self.h, self.w
        ph = TAU * t / P

        f = self.sky.copy()
        # Stars, behind everything.
        st = self.stars
        lum = st[:, 2] * (0.6 + 0.4 * np.sin(st[:, 3] * ph + st[:, 4]))
        xs, ys = st[:, 0].astype(int), st[:, 1].astype(int)
        f[ys, xs] += lum[:, None] * 170

        aur = cv2.resize(self._aurora(ph), (w, h), interpolation=cv2.INTER_CUBIC)
        aur = cv2.GaussianBlur(aur, (0, 0), 3)
        f = f + aur * 0.85
        # A faint wash of its light over the far snow.
        wash = aur.mean(axis=(0, 1), keepdims=True)

        f = f * (1 - self.land_far) + (self.farcol + wash * 0.8 * self.glow_y) * self.land_far
        f = f * (1 - self.land_near) + self.nearcol * self.land_near

        # Snow, falling in front of everything.
        for x0, y0, k, sway, m, sp, depth, a in self.flakes:
            spr = self.sprites[depth]
            s = spr.shape[0]
            span = h + 2 * s
            y = (y0 * span + k * span * t / P) % span - s
            x = x0 + sway * math.sin(m * ph + sp)
            x = x % w
            xi, yi = int(x) - s // 2, int(y) - s // 2
            xa, ya = max(0, xi), max(0, yi)
            xb, yb = min(w, xi + s), min(h, yi + s)
            if xa < xb and ya < yb:
                f[ya:yb, xa:xb] += (spr[ya - yi:yb - yi, xa - xi:xb - xi, None]
                                    * self.SNOW * (0.55 * a * (1.0 + 0.4 * depth)))

        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
