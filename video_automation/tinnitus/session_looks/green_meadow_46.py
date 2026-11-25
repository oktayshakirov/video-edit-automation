"""The look for `green-noise-46-breathing` (long + Short), and only that.

`WindMeadow`: a meadow at blue hour, seen from down in the grass. A teal
sky fades to a pale mint glow at the horizon under a thin crescent moon and
a few slow stars, a far tree line sits in a band of mist, and the field
runs towards the viewer in deepening greens. Gusts roll across it as long
pale bands - grass bent by the wind shows its lighter side - and tall
blades in the foreground sway as each gust reaches them. Fireflies drift
low over the field. Fully generated: no stock, no licence, no credit.

It answers the bed and the last looks: the track is *Green Meadow* (green
noise, Colors of Calm), so the picture is a green field moving in the
wind; `AmberDusk` (`brown-noise-478`) was hills seen from far off,
`RoseMere` (`pink-noise-box`) a lake and `EtherealSigh`
(`white-noise-sigh`) an abstract shimmer, so this is the first session
picture set inside a field.

The look does not read the breath: the clock guide draws every phase, and
a look that ignores `pattern` builds for the thumbnail without one. Every
motion runs a whole number of times per period on `t % period`.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.green_meadow_46 import WindMeadow
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Fireflies, Look, Mist, fbm, vignette


class WindMeadow(Look):
    """A meadow at blue hour: wind across the grass, swaying blades, fireflies."""

    ring = (232, 250, 236)
    TOP = np.array([14, 34, 46], np.float32)          # deep teal overhead
    MID = np.array([36, 84, 88], np.float32)          # sea green
    LOW = np.array([176, 214, 184], np.float32)       # pale mint glow
    MOON = np.array([236, 246, 226], np.float32)
    TREES = np.array([22, 46, 42], np.float32)
    MIST = np.array([196, 226, 204], np.float32)
    FAR = np.array([92, 132, 98], np.float32)         # the field at the horizon
    NEAR = np.array([18, 44, 26], np.float32)         # the field at your feet
    SHEEN = np.array([196, 228, 186], np.float32)     # grass bent by a gust
    BLADE = np.array([8, 22, 14], np.float32)

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        land = w >= h
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        rng = np.random.default_rng(461)
        self.H = H = (0.60 if land else 0.56) * h            # the horizon

        # The sky: three stops, eased, a faint stretched cloud texture.
        v = np.clip(yy / H, 0, 1)[..., None]
        lo, hi = np.clip(v / 0.55, 0, 1), np.clip((v - 0.55) / 0.45, 0, 1)
        sky = np.where(v < 0.55, self.TOP + (self.MID - self.TOP) * lo ** 1.1,
                       self.MID + (self.LOW - self.MID) * hi ** 1.6)
        cloud = fbm(h // 4, w // 4, 5, np.random.default_rng(462))
        cloud = cv2.resize(cloud, (w, h), interpolation=cv2.INTER_CUBIC)
        cloud = np.clip((cloud - 0.52) * 2.2, 0, 1)
        cloud = cv2.resize(cv2.resize(cloud, (w, max(8, h // 7))), (w, h))
        cloud = cv2.GaussianBlur(cloud, (0, 0), 6)
        sky = sky * (1 + 0.07 * cloud[..., None] * v)

        # A thin crescent moon, high on the left, with a soft halo.
        mx, my = (0.22 if land else 0.24) * w, (0.17 if land else 0.13) * h
        mr = 0.022 * min(w, h) * (1.0 if land else 1.3)
        d = np.sqrt((xx - mx) ** 2 + (yy - my) ** 2)
        d2 = np.sqrt((xx - mx - 0.42 * mr) ** 2 + (yy - my + 0.18 * mr) ** 2)
        disc = np.clip(mr - d + 0.8, 0, 1) * (1 - np.clip(mr * 0.96 - d2 + 0.8, 0, 1))
        halo = np.exp(-(d / (6.0 * mr)) ** 2) * 0.20
        sky = sky + (self.MOON - sky) * np.clip(disc + halo, 0, 1)[..., None]

        # The far shore: a low ragged tree line on the horizon.
        x = np.arange(w, dtype=np.float32) / w
        top = np.zeros(w, np.float32)
        # Crowns: the fine terms are set per pixel, not per width, so the
        # line reads as trees on both frames rather than as hills.
        px = np.arange(w, dtype=np.float32)
        for k, a in ((0.8, 1.0), (2.3, 0.5), (6.1, 0.3), (19.0, 0.14)):
            top += a * np.sin(TAU * k * x + rng.uniform(0, TAU))
        for lam, a in ((38.0, 0.16), (17.0, 0.10), (7.0, 0.05)):
            top += a * np.abs(np.sin(TAU * px / lam + rng.uniform(0, TAU)))
        top = H - (0.030 + 0.016 * top / 2.4) * h
        tree = np.clip((yy - top[None, :]) / 1.5, 0, 1) * (yy <= H + 2)
        sky = sky * (1 - tree[..., None]) + self.TREES * tree[..., None]
        self.sky = sky.astype(np.float32)
        self.above = (yy <= H)[..., None].astype(np.float32)

        # Stars: a few, upper sky only, each twinkling a whole number of
        # times a period.
        n = 46
        self.stars = [dict(x=int(rng.uniform(0, w)), y=int(rng.uniform(0, 0.42 * h)),
                           k=int(rng.integers(1, 4)), ph=rng.uniform(0, TAU),
                           b=rng.uniform(0.25, 0.8)) for _ in range(n)]

        # The field: depth 0 at the horizon, 1 at the bottom edge. Ground
        # distance falls off as 1/depth, which is what makes the gust bands
        # bunch up towards the horizon and spread out at your feet.
        depth = np.clip((yy - H) / (h - H), 0, 1)
        dist = 1.0 / (depth + 0.06)
        gx = (xx - w / 2) / w * dist
        self.field = (yy > H)[..., None].astype(np.float32)
        base = self.FAR + (self.NEAR - self.FAR) * (depth ** 0.55)[..., None]
        # Grass texture: fine noise stretched tall, so it reads as stems.
        g = np.random.default_rng(463).random(((h + 7) // 8, (w + 1) // 2),
                                              dtype=np.float32)
        g = cv2.resize(g, (w, h), interpolation=cv2.INTER_LINEAR)
        g = cv2.GaussianBlur(g, (0, 0), 0.8)
        self.base = (base * (0.86 + 0.28 * g * (0.3 + 0.7 * depth))[..., None]
                     ).astype(np.float32)
        # Gust coordinates: bands run at a slant across the ground.
        self.wave = (0.80 * dist + 0.55 * gx).astype(np.float32)
        patch = fbm(h // 8, w // 8, 3, np.random.default_rng(464))
        patch = cv2.resize(patch, (w, h), interpolation=cv2.INTER_CUBIC)
        self.patch = (0.35 + 0.65 * np.clip((patch - 0.40) * 2.6, 0, 1)
                      ).astype(np.float32)
        self.fade = np.clip(depth * 6, 0, 1).astype(np.float32)   # flat at the horizon

        # Mist over the far field and the tree line.
        self.band = np.exp(-((yy - H) / (0.07 * h)) ** 2).astype(np.float32)
        self.mist_a = Mist(w, h, 465, octaves=4, lo=0.42, gain=1.8, pad=(420, 200))
        self.mist_b = Mist(w, h, 466, octaves=3, lo=0.46, gain=2.0, pad=(420, 200))

        # Foreground blades: rooted below the frame, leaning a little with
        # the wind, each swaying as the gust crosses its x.
        nb = 150 if land else 110
        self.blades = []
        for _ in range(nb):
            bx = rng.uniform(-0.03, 1.03) * w
            tall = rng.uniform(0.10, 0.30) if rng.random() < 0.85 else rng.uniform(0.30, 0.42)
            self.blades.append(dict(
                x=bx, len=tall * h * (0.85 if land else 0.6),
                width=rng.uniform(4, 10) * (w / 1920 if land else w / 1080 * 0.8),
                lean=rng.uniform(-0.10, 0.30), sway=rng.uniform(0.04, 0.09),
                ph=TAU * 1.7 * bx / w + rng.uniform(-0.5, 0.5),
                head=rng.random() < 0.12))
        self.blades.sort(key=lambda b: b["len"])

        # Fireflies, kept to the field below the mist.
        self.flies = Fireflies(w, h, 16 if land else 14, 467, color=(208, 255, 150),
                               r=(3, 6))
        for q in self.flies.p:
            q["y"] = rng.uniform(H + 0.06 * h, h - 0.20 * h)
        # The shared sprite's wide blur is cut off at its box, which shows as
        # a faint square on a mid-tone field; take the edge level off.
        self.flies.sprites = [np.clip(s - s[0].max(axis=0, keepdims=True).max(), 0, None)
                              for s in self.flies.sprites]

        self.vig = vignette(w, h, 0.60)

    def _blades(self, f, ph):
        h = self.h
        mask = np.zeros((h, self.w), np.float32)
        for b in self.blades:
            # Two sway terms, both whole cycles a period; the gust term
            # travels along x so neighbouring blades move a beat apart.
            s = (b["sway"] * math.sin(3 * ph - b["ph"])
                 + 0.4 * b["sway"] * math.sin(7 * ph + 2.3 * b["ph"]))
            ang = b["lean"] + s
            L, x0 = b["len"], b["x"]
            pts_l, pts_r = [], []
            for i in range(9):
                u = i / 8
                bend = ang * u ** 1.6
                cx = x0 + L * math.sin(bend) * u * 1.2
                cy = h + 4 - L * u * math.cos(bend)
                half = b["width"] * (1 - u) ** 0.9 * 0.5 + 0.4
                pts_l.append((cx - half, cy))
                pts_r.append((cx + half, cy))
            poly = np.array(pts_l + pts_r[::-1], np.float32)
            cv2.fillPoly(mask, [np.round(poly * 4).astype(np.int32)], 1.0,
                         lineType=cv2.LINE_AA, shift=2)
            if b["head"]:
                tx, ty = pts_l[-1]
                # A loose seed head: a few small grains up the last stretch.
                for j in range(6):
                    u = 0.80 + 0.04 * j
                    bend = ang * u ** 1.6
                    gx_ = x0 + L * math.sin(bend) * u * 1.2
                    gy_ = h + 4 - L * u * math.cos(bend)
                    side = 1 if j % 2 else -1
                    cv2.ellipse(mask, (int((gx_ + side * 2.2) * 4), int(gy_ * 4)),
                                (int(b["width"] * 4 * 0.32), int(b["width"] * 4 * 0.9)),
                                math.degrees(ang) + side * 22, 0, 360, 1.0, -1,
                                cv2.LINE_AA, 2)
        k = mask[..., None]
        return f * (1 - k) + self.BLADE * k

    def at(self, t):
        t = t % self.period
        P = self.period
        ph = TAU * t / P

        # Stars twinkle in the sky only.
        sky = self.sky.copy()
        for s in self.stars:
            lum = s["b"] * (0.55 + 0.45 * math.sin(s["k"] * ph + s["ph"]))
            y, x = s["y"], s["x"]
            sky[y, x] += 170 * lum
            sky[max(0, y - 1):y + 2, max(0, x - 1):x + 2] += 40 * lum

        # Gusts: two trains of pale bands rolling away across the field,
        # each a whole number of cycles a period, brightest in patches.
        w1 = np.sin(1.9 * self.wave - 2 * ph)
        w2 = np.sin(3.3 * self.wave - 3 * ph + 1.1)
        gust = np.clip(0.65 * w1 + 0.35 * w2, 0, 1) ** 2 * self.patch * self.fade
        field = self.base + (self.SHEEN - self.base) * (0.42 * gust)[..., None]

        f = sky * self.above + field * (1 - self.above)

        # Mist: two sheets, opposite ways, over the horizon band.
        m = (self.mist_a.at(t, P, 1, 140) * 0.55
             + self.mist_b.at(t, P, -1, 100, phase=math.pi) * 0.45)
        k = (m * self.band * 0.50)[..., None]
        f = f * (1 - k) + self.MIST * k

        self.flies.draw(f, t, P, gain=1.5)
        f = self._blades(f, ph)
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
