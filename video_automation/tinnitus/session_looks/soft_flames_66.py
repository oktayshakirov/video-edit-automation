"""The look for `soft-flames-66-breathing` (long + Short), and only that.

`FiresideBreeze`: a small campfire at night, low in the frame. Flame tongues
rise through two scrolling noise sheets and lean with a slow breeze, embers
drift up and sideways off the fire, a faint smoke haze hangs over it, and
the fire's light breathes softly on the dark ground around it. The path
guide's line runs over the dark air above the flames in both layouts;
in portrait the fire sits clear of the platforms' bottom UI.
Fully generated: no stock, no licence, no credit.

It answers the last session look (`ZenithSea`, cool silver sky over clouds)
with the opposite: warm, close, and lit from below.

**Seamless by construction.** The flame noise scrolls a whole number of
texture heights per period, every ember's rise time divides the period, and
every sway and flicker runs a whole number of cycles, so `at(t)` equals
`at(t + period)`.

The look does not read the breath: the path guide draws both phases.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.soft_flames_66 import FiresideBreeze
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Look, Mist, fbm, vignette


def _vtile(tex: np.ndarray, seam: int) -> np.ndarray:
    """Crossfade a texture's bottom onto its top so it wraps vertically."""
    ramp = np.linspace(0, 1, seam, dtype=np.float32)[:, None]
    out = tex.copy()
    out[:seam] = tex[:seam] * ramp + tex[-seam:] * (1 - ramp)
    return np.ascontiguousarray(out[:-seam])


def _lut() -> np.ndarray:
    """Flame heat (0-1) to colour: ember red, orange, gold, a pale core."""
    stops = [(0.00, (0, 0, 0)), (0.18, (70, 8, 0)), (0.38, (190, 52, 6)),
             (0.58, (244, 118, 20)), (0.78, (255, 182, 62)),
             (0.92, (255, 226, 150)), (1.00, (255, 246, 214))]
    x = np.linspace(0, 1, 256)
    return np.stack([np.interp(x, [s[0] for s in stops], [s[1][c] for s in stops])
                     for c in range(3)], 1).astype(np.float32)


class FiresideBreeze(Look):
    """A campfire at night, leaning in a breeze, embers rising off it."""

    ring = (255, 228, 196)
    LUT = _lut()

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        P = period
        portrait = h > w
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)

        # Where the fire sits: low, centred, below the path guide's band.
        self.FW = int(w * (0.62 if portrait else 0.30)) // 2 * 2
        self.FH = int(h * (0.22 if portrait else 0.30)) // 2 * 2
        # Portrait: the base sits at 0.82h so the flames clear the platforms'
        # bottom UI (SAFE_BOTTOM=1440) and stop just under the path's troughs.
        self.base = int(h * (0.82 if portrait else 0.965))
        self.cx = w // 2
        self.x0 = self.cx - self.FW // 2
        self.y0 = self.base - self.FH

        # Background: a dark night, warmer and a touch lighter near the ground.
        s = (yy / h)[..., None]
        top = np.array([5, 6, 14], np.float32)
        low = np.array([22, 12, 10], np.float32)
        bg = top * (1 - s) ** 1.5 + low * (1 - (1 - s) ** 1.5)
        # The ground: a darker band under a soft horizon, lit around the fire.
        yg = self.base - int(self.FH * 0.18)
        ground = np.clip((yy - yg) / (0.05 * h) + 0.5, 0, 1)[..., None]
        bg = bg * (1 - ground) + np.array([12, 7, 6], np.float32) * ground
        self.bg = bg

        # A few faint stars, high up, out of the fire's light.
        rng = np.random.default_rng(6606)
        st = np.zeros((h, w), np.float32)
        n = int(w * h / 9000)
        ys = rng.integers(0, int(h * 0.55), n)
        xs = rng.integers(0, w, n)
        st[ys, xs] = rng.uniform(0.15, 1.0, n) ** 2.2
        st = cv2.GaussianBlur(st, (0, 0), 0.8) * 2.4
        far = np.sqrt(((xx - self.cx) / w) ** 2 + ((yy - self.base) / h) ** 2)
        self.stars = (np.clip(st, 0, 1) * np.clip((far - 0.35) * 2.0, 0, 1)
                      )[..., None] * np.array([190, 196, 220], np.float32)
        self.twk = rng.uniform(0, TAU, 3)

        # The fire's light: on the ground and the air around it.
        d = np.sqrt(((xx - self.cx) / (0.42 * w if not portrait else 0.75 * w)) ** 2
                    + ((yy - (self.base - self.FH * 0.35)) / (0.55 * h)) ** 2)
        self.light = (np.exp(-d ** 2 * 2.2)[..., None]
                      * np.array([150, 62, 18], np.float32))

        # Logs: two dark rounded bars crossed under the flames, edges lit.
        logs = np.zeros((h, w), np.float32)
        lw = max(4, int(self.FH * 0.045))
        for ang, dx, k in ((-9, -0.12, 0.50), (10, 0.12, 0.50), (2, 0.0, 0.40)):
            L = int(self.FW * k)
            c = (self.cx + int(dx * self.FW), self.base - int(lw * 1.6))
            a = math.radians(ang)
            p1 = (int(c[0] - L / 2 * math.cos(a)), int(c[1] - L / 2 * math.sin(a)))
            p2 = (int(c[0] + L / 2 * math.cos(a)), int(c[1] + L / 2 * math.sin(a)))
            cv2.line(logs, p1, p2, 1.0, lw * 2, cv2.LINE_AA)
            cv2.circle(logs, p1, lw, 1.0, -1, cv2.LINE_AA)
            cv2.circle(logs, p2, lw, 1.0, -1, cv2.LINE_AA)
        self.logs = cv2.GaussianBlur(logs, (0, 0), 1.2)[..., None]
        edge = np.clip(self.logs[..., 0] - cv2.GaussianBlur(
            np.roll(logs, int(lw * 0.6), 0), (0, 0), 2), 0, 1)
        self.logedge = edge[..., None]

        # Ember bed: hot specks along the base of the fire.
        bed = fbm(h, w, 5, np.random.default_rng(66))
        band = np.exp(-((yy - (self.base - lw * 1.2)) / (lw * 1.4)) ** 2
                      - ((xx - self.cx) / (self.FW * 0.36)) ** 6)
        self.bed = (np.clip((bed - 0.52) * 4.0, 0, 1) * band)[..., None]

        # Flame noise at half resolution: two vertically wrapping sheets.
        self.fw, self.fh = self.FW // 2, self.FH // 2
        seam = 48
        self.tex = []
        for seed, kx in ((601, 2.6), (602, 3.8)):
            tw, th = self.fw, int(self.fh * 1.6) + seam
            t = fbm(th, int(tw * kx), 5, np.random.default_rng(seed))
            t = cv2.resize(t, (tw, th))
            self.tex.append(_vtile(t, seam))
        # Whole texture heights per period, so the scroll closes on itself.
        self.k = (int(round(P * 2.9)), int(round(P * 4.3)))
        u = (np.arange(self.fw, dtype=np.float32) - self.fw / 2) / (self.fw / 2)
        v = 1 - (np.arange(self.fh, dtype=np.float32) + 0.5) / self.fh  # 0 at base
        self.u, self.v = np.meshgrid(u, v)
        hmax = 0.22 + 0.78 * np.exp(-(self.u / 0.34) ** 2)
        self.shape = np.clip(1 - self.v / hmax, 0, 1) * np.clip(
            1 - (self.u / 0.8) ** 2, 0, 1) * np.clip(self.v / 0.10, 0, 1)
        # (the last line fades the very bottom rows, which show under the logs)
        self.gx = np.tile(np.arange(self.fw, dtype=np.float32), (self.fh, 1))
        self.gy = np.tile(np.arange(self.fh, dtype=np.float32)[:, None], (1, self.fw))

        # Smoke: a faint warm-grey haze over the fire, rising out of the light.
        self.smoke = Mist(w, h, 607, octaves=4, lo=0.50, gain=1.8,
                          pad=(max(8, w // 4), max(8, h // 4)))
        col = np.exp(-((xx - self.cx) / (self.FW * 0.9)) ** 2)
        rise = np.clip((self.base - yy) / (h * 0.7), 0, 1)
        self.smask = (col * np.sin(np.pi * np.clip(rise, 0, 1)) * (rise > 0.1)
                      )[..., None].astype(np.float32)

        # Embers: each rises in a time that divides the period, drifts with
        # the breeze to the right, and fades as it cools.
        self.embers = []
        for _ in range(46 if portrait else 40):
            n = int(rng.choice([5, 6, 6, 8, 10]))
            self.embers.append(dict(
                Tr=P / n, ph=rng.uniform(0, 1),
                x=self.cx + rng.normal(0, self.FW * 0.15),
                y=self.base - self.FH * rng.uniform(0.25, 0.6),
                H=h * rng.uniform(0.35, 0.75 if portrait else 0.8),
                drift=w * rng.uniform(0.02, 0.10) * (1 if portrait else 1.4),
                sa=rng.uniform(6, 22), sm=int(rng.integers(3, 9)),
                sp=rng.uniform(0, TAU), fk=int(rng.integers(20, 50)),
                b=rng.uniform(0.5, 1.0), r=int(rng.integers(0, 3))))
        self.sprites = []
        for rad in (1.2, 1.8, 2.6):
            sz = int(rad * 8) | 1
            g = np.zeros((sz, sz), np.float32)
            cv2.circle(g, (sz // 2, sz // 2), 1, 1.0, -1)
            g = cv2.GaussianBlur(g, (0, 0), rad * 0.6) + cv2.GaussianBlur(
                g, (0, 0), rad * 1.8) * 0.5
            g /= g.max()
            self.sprites.append(g[..., None] * np.array([255, 150, 50], np.float32))
        self.vig = vignette(w, h, 0.50)

    # -- one frame ------------------------------------------------------------

    def _flicker(self, t: float) -> float:
        P = self.period
        return (1.0 + 0.07 * math.sin(TAU * 3 * t / P)
                + 0.05 * math.sin(TAU * 11 * t / P + 1.3)
                + 0.035 * math.sin(TAU * 23 * t / P + 2.1)
                + 0.02 * math.sin(TAU * 41 * t / P + 0.4))

    def _fire(self, t: float) -> np.ndarray:
        P = self.period
        v, u = self.v, self.u
        # The breeze: a slow lean with gusts, stronger towards the tips.
        lean = (0.55 + 0.45 * math.sin(TAU * 2 * t / P)) * 0.18
        flut = (np.sin(TAU * 9 * t / P + v * 9 + u * 2) * 0.05
                + np.sin(TAU * 17 * t / P + v * 15) * 0.025)
        dx = (lean + flut) * (v ** 1.4) * self.fw
        out = []
        for tex, k in zip(self.tex, self.k):
            th = tex.shape[0]
            sy = (th * k * t / P) % th
            out.append(cv2.remap(tex, (self.gx - dx) % self.fw,
                                 (self.gy + sy) % th, cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_WRAP))
        n = 0.62 * out[0] + 0.38 * out[1]
        heat = self.shape * (0.25 + 1.6 * n) - 0.30 - 0.32 * v
        # Clip after the flicker: heat over 1 would wrap the LUT index to black.
        heat = np.clip(heat * 1.55 * (0.92 + 0.08 * self._flicker(t)), 0, 1)
        heat = cv2.resize(heat, (self.FW, self.FH), interpolation=cv2.INTER_LINEAR)
        return self.LUT[(heat * 255).astype(np.uint8)]

    def at(self, t):
        P = self.period
        t = t % P          # exact: at(t) and at(t + period) are the same frame
        fl = self._flicker(t)
        f = self.bg.copy()
        tw = 0.8 + 0.2 * math.sin(TAU * 4 * t / P + self.twk[0])
        f += self.stars * tw
        f += self.light * (0.6 * fl)

        # Smoke drifts and is lit warm from below.
        sm = self.smoke.at(t, P, 1, 70)[..., None] * self.smask
        f += sm * np.array([46, 36, 32], np.float32) * (0.8 + 0.2 * fl)

        # The flames, additive, with a soft bloom round them.
        fire = self._fire(t)
        bloom = cv2.GaussianBlur(fire, (0, 0), max(6, self.FW / 30))
        y0, x0 = self.y0, self.x0
        f[y0:y0 + self.FH, x0:x0 + self.FW] += fire * 0.95 + bloom * 0.55

        # Logs in front of the flames' base, edges lit, the ember bed on them.
        f = f * (1 - self.logs * 0.92) + self.logs * np.array([14, 8, 6], np.float32)
        f += self.logedge * np.array([200, 74, 14], np.float32) * fl
        pulse = 0.75 + 0.25 * math.sin(TAU * 5 * t / P + 0.7)
        f += self.bed * np.array([255, 110, 24], np.float32) * pulse * 0.9

        # Embers.
        for e in self.embers:
            fr = ((t / e["Tr"]) + e["ph"]) % 1.0
            x = (e["x"] + e["drift"] * fr ** 1.3
                 + e["sa"] * math.sin(TAU * e["sm"] * t / P + e["sp"]))
            y = e["y"] - e["H"] * fr
            life = min(1.0, fr * 12) * (1 - fr) ** 1.6
            lum = life * e["b"] * (0.7 + 0.3 * math.sin(TAU * e["fk"] * t / P + e["sp"]))
            if lum < 0.01:
                continue
            spr = self.sprites[e["r"]]
            s = spr.shape[0]
            xa0, ya0 = int(x) - s // 2, int(y) - s // 2
            xa, ya = max(0, xa0), max(0, ya0)
            xb, yb = min(self.w, xa0 + s), min(self.h, ya0 + s)
            if xa < xb and ya < yb:
                f[ya:yb, xa:xb] += spr[ya - ya0:yb - ya0, xa - xa0:xb - xa0] * lum
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
