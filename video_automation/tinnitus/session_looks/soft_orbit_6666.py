"""The look for `soft-orbit-6666-breathing` (long + Short), and only that.

`RingedWorld`: a warm ringed planet low in the frame, lit from the upper
left, its cloud bands turning once per loop and its rings turning with them,
and a small moon on a closed orbit in the ring plane - one orbit per loop,
passing in front of the rings and behind the planet. The bed is "Soft Orbit"
from the Quiet Universe album, so the picture is the title: a soft orbit.
It answers `LowOrbit` (the album's previous session) on purpose - amber
against that one's blue, a whole world with rings against a planet's limb -
and keeps the centre dark for the clock guide. Fully generated: no stock, no
licence, no credit.

The look does not read the breath: the clock guide draws all four phases.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.soft_orbit_6666 import RingedWorld
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Fireflies, Look, Mist, fbm, orbit, vignette


def _smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


class RingedWorld(Look):
    """Stars, a banded ringed planet and one small moon on a closed orbit."""

    ring = (255, 232, 200)
    DEEP = np.array([5, 4, 14], np.float32)
    HAZE = np.array([70, 40, 80], np.float32)          # dusky rose nebula
    RINGC = np.array([232, 210, 170], np.float32)
    BANDS = np.array([[120, 72, 40], [214, 170, 112], [168, 112, 62],
                      [236, 206, 152], [150, 96, 54], [222, 184, 128],
                      [132, 84, 48]], np.float32)
    TILT = math.radians(-13.0)          # ring plane rotation on screen
    K = 0.24                            # ring ellipse minor / major
    MOON_ORBIT = 2.35                   # in planet radii
    MOON_TILT = math.radians(-24.0)     # its own plane, steeper than the rings
    MOON_K = 0.42

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        rng = np.random.default_rng(6666)
        S = min(w, h)
        if w >= h:
            self.cx, self.cy, R = w * 0.79, h * 0.90, 0.37 * S
        else:
            self.cx, self.cy, R = w * 0.68, h * 0.86, 0.40 * S
        self.R = R

        # Stars on a closed drift, as the album's last look did.
        pad = 120
        big = np.zeros((h + 2 * pad, w + 2 * pad), np.float32)
        n = int(big.size / 2100)
        ys = rng.integers(0, big.shape[0], n)
        xs = rng.integers(0, big.shape[1], n)
        big[ys, xs] = rng.uniform(0.12, 1.0, n) ** 2.4
        stars = cv2.GaussianBlur(big, (0, 0), 0.7) * 3.0
        stars += cv2.GaussianBlur(big, (0, 0), 2.0) * 1.5
        self.stars = (np.clip(stars, 0, 1) * 255).astype(np.uint8)
        self.haze = Mist(w, h, 61, octaves=5, lo=0.42, gain=1.5, pad=(300, 200))
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        # The haze sits upper left, where the light comes from.
        hd = np.sqrt(((xx - w * 0.18) / max(w, h)) ** 2
                     + ((yy - h * 0.12) / max(w, h)) ** 2)
        self.hazemask = np.exp(-(hd / 0.45) ** 2)[..., None]

        dx, dy = xx - self.cx, yy - self.cy
        c, s = math.cos(self.TILT), math.sin(self.TILT)
        u = dx * c + dy * s                 # along the ring plane
        v = -dx * s + dy * c                # across it (screen-down positive)

        # Planet: a sphere, lit from the upper left.
        d = np.sqrt(dx ** 2 + dy ** 2)
        self.disc = np.clip(R + 0.5 - d, 0, 1)[..., None]
        nx, ny = dx / R, dy / R
        nz = np.sqrt(np.clip(1 - nx ** 2 - ny ** 2, 0, 1))
        L = np.array([-0.78, -0.42, 0.40]); L /= np.linalg.norm(L)
        lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
        self.shade = (0.03 + 0.97 * lam ** 0.85)[..., None]
        self.limb = (np.exp(-np.clip(R - d, 0, None) / (0.035 * R))
                     * np.clip(0.2 + lam * 1.4, 0, 1) * (d < R + 1))[..., None]
        glow = np.clip(d - R, 0, None)
        self.atmo = (np.exp(-glow / (0.05 * R)) * (d >= R)
                     * np.clip(0.15 + 0.85 * (-(nx * 0.62 + ny * 0.5)), 0, 1)
                     )[..., None]
        # Latitude across the band direction, longitude for the turning.
        lat = np.clip(v / R, -1, 1)
        coslat = np.sqrt(np.clip(1 - lat ** 2, 1e-4, 1))
        lon = np.arcsin(np.clip(u / (R * coslat), -1, 1))   # -pi/2..pi/2
        # Band texture: rows by latitude, columns by longitude, wrapping.
        TH, TW = 512, 1024
        base = fbm(TH, TW, 5, np.random.default_rng(71))
        warp = (fbm(TH, TW, 4, np.random.default_rng(72)) - 0.5) * 0.18
        rows = np.linspace(-1, 1, TH, dtype=np.float32)[:, None] + warp
        idx = (rows * 3.1 + 3.1) % len(self.BANDS)
        i0 = np.floor(idx).astype(int) % len(self.BANDS)
        i1 = (i0 + 1) % len(self.BANDS)
        fr = (idx - np.floor(idx))[..., None]
        col = self.BANDS[i0] * (1 - fr) + self.BANDS[i1] * fr
        col *= (0.72 + 0.56 * base)[..., None]
        # Wrap the texture horizontally so the turning closes on the loop.
        seam = 64
        col[:, :seam] = (col[:, :seam] * np.linspace(0, 1, seam)[None, :, None]
                         + col[:, TW - seam:] * np.linspace(1, 0, seam)[None, :, None])
        self.bandtex = np.ascontiguousarray(col[:, :TW - seam]).astype(np.float32)
        self.TW = TW - seam
        self.pmapy = ((lat + 1) / 2 * (TH - 1)).astype(np.float32)
        self.pmapx0 = ((lon / math.pi + 0.5) * 0.5 * self.TW).astype(np.float32)

        # Rings: radius in the ring plane, in planet radii.
        rr = np.sqrt(u ** 2 + (v / self.K) ** 2) / R
        th = np.arctan2(v / self.K, u)
        prof_r = np.linspace(1.0, 2.4, 2048, dtype=np.float32)
        fine = cv2.GaussianBlur(rng.random((1, 2048)).astype(np.float32),
                                (0, 0), 3)[0]
        fine = (fine - fine.min()) / (fine.max() - fine.min())
        prof = (_smooth(1.28, 1.36, prof_r) * (1 - _smooth(2.12, 2.20, prof_r))
                * (1 - 0.92 * _smooth(1.86, 1.88, prof_r)
                   * (1 - _smooth(1.92, 1.94, prof_r)))
                * (0.45 + 0.55 * fine)
                * (0.55 + 0.45 * _smooth(1.40, 1.60, prof_r)))
        self.prof_r, self.prof = prof_r, prof
        ring_a = np.interp(rr.ravel(), prof_r, prof, left=0, right=0)
        self.ring_a = ring_a.reshape(h, w).astype(np.float32)
        # Clumps that turn with the ring, one turn per loop.
        AW = 1024
        clump = fbm(64, AW, 4, np.random.default_rng(73))
        clump[:, :64] = (clump[:, :64] * np.linspace(0, 1, 64)[None]
                         + clump[:, -64:] * np.linspace(1, 0, 64)[None])
        self.clump = np.ascontiguousarray(clump[:, :AW - 64]).astype(np.float32)
        self.AW = AW - 64
        self.rmapy = (np.clip((rr - 1.0) / 1.4, 0, 1) * 63).astype(np.float32)
        self.rmapx0 = ((th / TAU + 0.5) * self.AW).astype(np.float32)
        self.front = (v > 0)[..., None].astype(np.float32)
        # The planet's shadow falls on the rings away from the sun.
        lx, ly = 0.62 / math.hypot(0.62, 0.5), 0.5 / math.hypot(0.62, 0.5)
        along = dx * lx + dy * ly
        perp = np.abs(dx * ly - dy * lx)
        shadow = (along > 0) * (1 - _smooth(R * 0.94, R * 1.02, perp))
        shadow = shadow * (v < 0)          # cast away from us: back half only
        self.ringshadow = (1 - 0.8 * shadow).astype(np.float32)[..., None]
        # Bounding box of planet + rings, so per-frame work stays local.
        ys_, xs_ = np.nonzero((self.ring_a > 0.002) | (self.disc[..., 0] > 0)
                              | (self.atmo[..., 0] > 0.01))
        self.box = (ys_.min(), ys_.max() + 1, xs_.min(), xs_.max() + 1)

        # The moon: a small lit sphere, shaded from the same sun.
        mr = max(7.0, 0.065 * R)
        ms = int(mr * 6) | 1
        my, mx = np.mgrid[0:ms, 0:ms].astype(np.float32) - ms // 2
        md = np.sqrt(mx ** 2 + my ** 2)
        mnz = np.sqrt(np.clip(1 - (mx / mr) ** 2 - (my / mr) ** 2, 0, 1))
        mlam = np.clip((mx / mr) * L[0] + (my / mr) * L[1] + mnz * L[2], 0, 1)
        body = np.clip(mr + 0.5 - md, 0, 1)
        self.moon_a = body.astype(np.float32)
        self.moon_c = ((12 + 228 * mlam ** 0.9)[..., None]
                       * np.array([1.0, 0.97, 0.92], np.float32)).astype(np.float32)
        self.moon_glow = (np.exp(-np.clip(md - mr, 0, None) / (0.6 * mr))
                          * (md >= mr) * 0.35).astype(np.float32)
        self.ms = ms

        self.dust = Fireflies(w, h, 10, 91, color=(255, 214, 170),
                              margin=(0.05, 0.08), r=(2, 4))
        self.vig = vignette(w, h, 0.45)

    # -- per frame ------------------------------------------------------------

    def _moon(self, t):
        a = TAU * t / self.period + 2.2
        u = self.MOON_ORBIT * self.R * math.cos(a)
        v = self.MOON_K * self.MOON_ORBIT * self.R * math.sin(a)
        c, s = math.cos(self.MOON_TILT), math.sin(self.MOON_TILT)
        x = self.cx + u * c - v * s
        y = self.cy + u * s + v * c
        return x, y, v > 0

    def _stamp(self, f, x, y, img, alpha):
        """Blend `img` with `alpha` centred at subpixel (x, y); add it if None."""
        s = img.shape[0]
        x0, y0 = int(math.floor(x)) - s // 2, int(math.floor(y)) - s // 2
        fx, fy = x - math.floor(x), y - math.floor(y)
        M = np.float32([[1, 0, fx], [0, 1, fy]])
        im = cv2.warpAffine(img, M, (s, s), flags=cv2.INTER_LINEAR)
        xa, ya = max(0, x0), max(0, y0)
        xb, yb = min(self.w, x0 + s), min(self.h, y0 + s)
        if xa >= xb or ya >= yb:
            return
        im = im[ya - y0:yb - y0, xa - x0:xb - x0]
        if im.ndim == 2:
            im = im[..., None]
        if alpha is None:                       # additive (a glow)
            f[ya:yb, xa:xb] += im
            return
        a = cv2.warpAffine(alpha, M, (s, s), flags=cv2.INTER_LINEAR)
        a = a[ya - y0:yb - y0, xa - x0:xb - x0][..., None]
        f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - a) + im * a

    def at(self, t):
        P = self.period
        t = t % P          # exact: at(t) and at(t + P) are the same frame
        st = orbit(self.stars, self.w, self.h, t, P, 26).astype(np.float32)
        f = self.DEEP + st[..., None] * 0.80
        hz = self.haze.at(t, P, 1, 80, 0.4)[..., None]
        f += self.hazemask * hz * self.HAZE * 0.75
        self.dust.draw(f, t, P, 0.35)

        mx, my, mfront = self._moon(t)
        y0, y1, x0, x1 = self.box
        sub = f[y0:y1, x0:x1]
        sl = (slice(y0, y1), slice(x0, x1))

        # Rings: the turning clumps, brightness from the radial profile.
        shift = self.AW * (t / P)
        cl = cv2.remap(self.clump, (self.rmapx0[sl] + shift) % self.AW,
                       self.rmapy[sl], cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_WRAP)
        ra = (self.ring_a[sl] * (0.7 + 0.6 * cl))[..., None]
        ra = np.clip(ra * 0.95, 0, 0.92)
        ringcol = self.RINGC * self.ringshadow[sl]
        back = ra * (1 - self.front[sl])
        front = ra * self.front[sl]

        if not mfront:
            self._stamp(f, mx, my, self.moon_c, self.moon_a)
        sub[:] = sub * (1 - back) + ringcol * back
        # Planet over the back half of the rings.
        pshift = self.TW * (t / P)
        bands = cv2.remap(self.bandtex, (self.pmapx0[sl] + pshift) % self.TW,
                          self.pmapy[sl], cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_WRAP)
        planet = bands * self.shade[sl] + self.limb[sl] * np.array(
            [255, 200, 140], np.float32) * 0.35
        dsc = self.disc[sl]
        sub[:] = sub * (1 - dsc) + planet * dsc
        sub += self.atmo[sl] * np.array([255, 170, 110], np.float32) * 0.30
        # Front half of the rings over the planet, slightly dimmed where it
        # crosses the night side so it does not glow in the dark.
        dim = 1 - dsc * (1 - np.clip(self.shade[sl] * 1.6, 0.35, 1))
        sub[:] = sub * (1 - front) + ringcol * dim * front
        if mfront:
            self._stamp(f, mx, my, self.moon_c, self.moon_a)
        # The moon's faint halo, added, unless the planet hides the moon.
        hidden = (not mfront) and math.hypot(mx - self.cx, my - self.cy) < self.R
        if not hidden:
            g = self.moon_glow[..., None] * np.array([230, 220, 200], np.float32)
            self._stamp(f, mx, my, g, None)
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
