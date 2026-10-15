"""The look for `jungle-waterfall-478-breathing` (long + Short), and only that.

Drawn fern silhouettes swaying round the edges of the frame, a moonlit green
glow, two sheets of mist and fireflies — the `night-fronds` test look, picked
from five on 2026-10-15. Generated, so no licence and no stock credit.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` — start the next look from there.

    from video_automation.tinnitus.session_looks.jungle_waterfall_478 import NightFronds
"""

from __future__ import annotations

import math

import cv2
import numpy as np
from PIL import Image, ImageDraw

from ...core.looks import TAU, Fireflies, Look, Mist


def _frond_mask(length: int, seed: int) -> np.ndarray:
    """A fern frond as an alpha mask, base at the centre, pointing +x.

    Narrow tapered leaflets, angled toward the tip, each drooping a little;
    the spine stops where the leaflets do. The first draft used wide straight
    triangles and read as saw blades — the narrowness is what makes it a fern.
    """
    rng = np.random.default_rng(seed)
    S = int(length * 2.3)
    im = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(im)
    c = S // 2
    bend = rng.uniform(-0.28, 0.28)
    spine = [(c + u * length, c + bend * length * u * u)
             for u in np.linspace(0, 1, 120)]
    n = int(rng.integers(22, 30))
    for j in range(3, n + 1):
        u = j / (n + 1)
        x, y = spine[int(u * 119)]
        tang = math.atan2(2 * bend * u, 1)
        leaf = length * 0.27 * math.sin(math.pi * (0.1 + 0.88 * u)) ** 0.8
        for side in (-1, 1):
            ang = tang + side * (1.05 - 0.5 * u) + rng.uniform(-0.06, 0.06)
            droop = side * rng.uniform(0.10, 0.22) * (1 if bend >= 0 else -1)
            wmax = leaf * 0.07
            left, right = [], []
            for v in np.linspace(0, 1, 9):
                a2 = ang + droop * v * v
                px = x + leaf * v * math.cos(ang) + leaf * 0.12 * v * v * math.cos(a2 + side * 1.57)
                py = y + leaf * v * math.sin(ang) + leaf * 0.12 * v * v * math.sin(a2 + side * 1.57)
                wv = wmax * math.sin(math.pi * min(1.0, v * 1.02)) ** 0.7
                nx, ny = -math.sin(ang) * wv, math.cos(ang) * wv
                left.append((px + nx, py + ny))
                right.append((px - nx, py - ny))
            d.polygon(left + right[::-1], fill=255)
    d.line(spine[:int(119 * (n / (n + 1)))], fill=255,
           width=max(3, int(length * 0.009)))
    return np.asarray(im, np.float32) / 255.0


# (anchor x, anchor y, angle deg, length) — in fractions of the frame, length
# in fractions of the frame's *short* side. Near layer is near-black and sharp,
# far layer is green and blurred. Landscape frames the left and right edges;
# portrait has no sides to spare, so it hangs fronds from the top corners and
# raises a few from the bottom, leaving the middle band (ring and captions)
# open.
_FRONDS = {
    "landscape": {
        "near": [(-0.03, 0.08, 14, 0.65), (-0.04, 0.65, -16, 0.70),
                 (0.06, 1.07, -60, 0.57), (1.03, 0.04, 168, 0.67),
                 (1.04, 0.74, 196, 0.72), (0.92, 1.08, 238, 0.56)],
        "far": [(0.36, -0.07, 95, 0.48), (0.68, -0.06, 80, 0.52),
                (-0.02, 0.35, 5, 0.57), (1.02, 0.39, 178, 0.56),
                (0.51, 1.09, 268, 0.44)],
    },
    "portrait": {
        "near": [(-0.05, 0.02, 38, 0.78), (1.05, 0.03, 142, 0.80),
                 (-0.06, 0.26, 12, 0.62), (1.06, 0.22, 170, 0.60),
                 (-0.04, 1.02, -40, 0.74), (1.04, 1.01, 218, 0.76)],
        "far": [(0.50, -0.04, 92, 0.55), (-0.04, 0.80, -8, 0.55),
                (1.04, 0.78, 186, 0.55), (0.45, 1.04, 272, 0.50)],
    },
}


class NightFronds(Look):
    """Drawn: moonlit glow, two mist sheets, fireflies, swaying fern silhouettes.

    Fronds are single-channel masks warped straight into frame coordinates with
    `cv2.warpAffine` (rotation about the frond's own base) — a PIL rotate of an
    RGBA sprite per frond per frame cost 1.3 s a frame, this costs ~0.15 s.
    """

    ring = (214, 255, 190)
    DEEP, MID, HI = (4, 14, 10), (18, 64, 44), (120, 196, 150)
    NEAR, FAR = (2, 8, 6), (10, 34, 24)
    MIST = (150, 200, 175)

    def __init__(self, w, h, period, pattern=None, seed: int = 4):
        super().__init__(w, h, period, pattern)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        portrait = h > w
        gx, gy = (0.5, 0.40) if portrait else (0.58, 0.38)
        d = np.sqrt(((xx - w * gx) / w) ** 2 + ((yy - h * gy) / h) ** 2)
        glow = np.exp(-(d / (0.55 if portrait else 0.42)) ** 2)
        base = np.zeros((h, w, 3), np.float32)
        for c in range(3):
            base[..., c] = (self.DEEP[c] + glow * (self.MID[c] - self.DEEP[c])
                            + glow ** 6 * (self.HI[c] - self.MID[c]) * 0.55)
        self.base = base
        self.m1 = Mist(w, h, seed + 17, lo=0.47, gain=2.2)
        self.m2 = Mist(w, h, seed + 18, octaves=3, lo=0.44, gain=1.8)
        self.ff = Fireflies(w, h, 34 if not portrait else 28, seed + 5)

        rng = np.random.default_rng(seed)
        short = min(w, h)
        layout = _FRONDS["portrait" if portrait else "landscape"]
        self.layers = []
        for li, (key, col) in enumerate((("far", self.FAR), ("near", self.NEAR))):
            fronds = []
            for k, (fx, fy, a, fl) in enumerate(layout[key]):
                L = int(fl * short)
                m = _frond_mask(L, 100 + seed * 31 + li * 50 + k)
                if key == "far":
                    m = cv2.GaussianBlur(m, (0, 0), 5)
                fronds.append(dict(
                    m=m, x=fx * w, y=fy * h, a=a,
                    amp=rng.uniform(1.6, 3.2) * (0.6 if key == "far" else 1.0),
                    k=int(rng.integers(3, 6)), ph=rng.uniform(0, TAU)))
            self.layers.append((np.array(col, np.float32), fronds))

    def at(self, t):
        f = self.base.copy()
        mist = (0.16 * self.m1.at(t, self.period, 1, 160)
                + 0.10 * self.m2.at(t, self.period, 2, 110, 2.0))
        f += (np.array(self.MIST, np.float32) - f) * mist[..., None]
        self.ff.draw(f, t, self.period, 0.9)
        for col, fronds in self.layers:
            alpha = np.zeros((self.h, self.w), np.float32)
            for q in fronds:
                ang = q["a"] + q["amp"] * math.sin(TAU * q["k"] * t / self.period + q["ph"])
                s = q["m"].shape[0]
                # rotate about the sprite centre (the frond's base), then put
                # that centre on the anchor
                M = cv2.getRotationMatrix2D((s / 2, s / 2), -ang, 1.0)
                M[0, 2] += q["x"] - s / 2
                M[1, 2] += q["y"] - s / 2
                m = cv2.warpAffine(q["m"], M, (self.w, self.h),
                                   flags=cv2.INTER_LINEAR, borderValue=0)
                np.maximum(alpha, m, out=alpha)
            f += (col - f) * alpha[..., None]
        return np.clip(f, 0, 255).astype(np.uint8)
