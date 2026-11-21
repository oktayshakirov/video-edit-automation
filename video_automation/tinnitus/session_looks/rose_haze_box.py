"""The look for `pink-noise-box-breathing` (long + Short), and only that.

`RoseMere`: a still lake at a pink dawn. The sky runs from a dusky violet
overhead to rose and a pale peach at the horizon, a low sun glows behind a
far line of trees, and the lake below mirrors all of it - sky, sun and the
dark tree line - broken by slow ripples that travel towards the viewer and
a column of glints under the sun. Two sheets of rose haze drift over the
water in opposite directions. Fully generated: no stock, no licence, no
credit.

It answers the bed and the last two looks: the track is *Rose Haze* (pink
noise, Colors of Calm), so the picture is a pink haze; `AmberDusk`
(`brown-noise-478`) was hills under a warm sky and `NightDraft`
(`fan-noise-444`) a room at night, so this is open water at first light,
the first session picture on the channel built around a lake.

The look does not read the breath: the box guide draws every phase, and a
look that ignores `pattern` builds for the thumbnail without one. Every
motion runs a whole number of times per period on `t % period`.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.rose_haze_box import RoseMere
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Look, Mist, fbm, vignette


class RoseMere(Look):
    """A pink dawn over a still lake, mirrored, rippling, under drifting haze."""

    ring = (255, 236, 240)
    TOP = np.array([44, 34, 70], np.float32)          # dusky violet overhead
    MID = np.array([150, 92, 124], np.float32)        # rose
    LOW = np.array([238, 178, 168], np.float32)       # pale peach at the horizon
    SUN = np.array([255, 222, 196], np.float32)
    TREES = np.array([58, 38, 58], np.float32)        # far shore, hazy plum
    HAZE = np.array([244, 196, 206], np.float32)
    WATER = np.array([0.80, 0.84, 0.96], np.float32)  # the mirror is cooler, darker

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        land = w >= h
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        rng = np.random.default_rng(71)
        self.H = H = (0.56 if land else 0.54) * h            # the horizon
        self.sx = sx = (0.72 if land else 0.70) * w          # the sun
        sy = H - 0.035 * h

        # The sky: three stops, eased, plus a faint cloud texture.
        v = np.clip(yy / H, 0, 1)[..., None]
        lo, hi = np.clip(v / 0.6, 0, 1), np.clip((v - 0.6) / 0.4, 0, 1)
        sky = np.where(v < 0.6, self.TOP + (self.MID - self.TOP) * lo ** 1.2,
                       self.MID + (self.LOW - self.MID) * hi ** 0.9)
        cloud = fbm(h // 4, w // 4, 5, np.random.default_rng(72))
        cloud = cv2.resize(cloud, (w, h), interpolation=cv2.INTER_CUBIC)
        cloud = np.clip((cloud - 0.5) * 2.4, 0, 1)
        cloud = cv2.resize(cv2.resize(cloud, (w, max(8, h // 6))), (w, h))  # stretch wide
        sky = sky * (1 + 0.10 * cloud[..., None] * (1 - v))

        # The sun: a soft glow and a small bright core, half behind the trees.
        d = np.sqrt(((xx - sx) / w) ** 2 + ((yy - sy) / w) ** 2)
        glow = (np.exp(-(d / 0.20) ** 2) * 0.55 + np.exp(-(d / 0.045) ** 2) * 0.45
                + np.exp(-(d / 0.012) ** 2) * 0.6)
        sky = sky + (self.SUN - sky) * np.clip(glow, 0, 1)[..., None]

        # The far shore: a low tree line, ragged on top, lightest where the
        # sun is behind it. Drawn into the sky so the mirror carries it.
        x = np.arange(w, dtype=np.float32) / w
        top = np.zeros(w, np.float32)
        for k, a in ((1.1, 1.0), (2.9, 0.45), (7.3, 0.25), (23.0, 0.12),
                     (61.0, 0.07), (139.0, 0.04)):
            top += a * np.sin(TAU * k * x + rng.uniform(0, TAU))
        top = H - (0.028 + 0.012 * top / 1.9) * h
        tree = np.clip((yy - top[None, :]) / 1.5, 0, 1) * (yy <= H)
        lift = np.exp(-((xx - sx) / (0.25 * w)) ** 2)[..., None]
        trees = self.TREES + (self.LOW - self.TREES) * 0.25 * lift
        sky = sky * (1 - tree[..., None]) + trees * tree[..., None]
        self.sky = np.clip(sky, 0, 255).astype(np.float32)

        # The water: how far below the horizon (0 at the shore, 1 at the
        # bottom edge) drives perspective - ripples grow towards the viewer.
        depth = np.clip((yy - H) / (h - H), 0, 1)
        self.depth = depth
        self.water = (yy > H)[..., None].astype(np.float32)
        self.shore = np.exp(-((yy - H) / 4.0) ** 2)[..., None].astype(np.float32)
        self.mirror_y = np.clip(2 * H - yy, 0, H - 1).astype(np.float32)
        self.xx = xx

        # Glints: a texture stretched very wide, so it breaks into short
        # horizontal streaks, brightest in a column under the sun.
        # Fine random cells stretched to ~36x3px, kept only where they are
        # brightest, give sparse short streaks rather than blobs.
        cells = np.random.default_rng(73).random(((h + 80) // 3, (w + 240) // 36),
                                                 dtype=np.float32)
        g = cv2.resize(cells, (w + 240, h + 80), interpolation=cv2.INTER_LINEAR)
        g = cv2.GaussianBlur(np.clip((g - 0.80) * 5.0, 0, 1), (0, 0), 1.2)
        self.glint = g.astype(np.float32)
        col = np.exp(-((xx - sx) / (0.035 * w + 0.16 * w * depth)) ** 2)
        self.column = (col * (depth > 0)).astype(np.float32)

        # Ripple lines: the light and dark bands a breeze draws on still
        # water, thin near the shore and wider towards the viewer. A fixed
        # noise bends each band so none runs the full width.
        bend = fbm(h // 4, w // 16, 3, np.random.default_rng(76))
        self.bend = cv2.resize(bend, (w, h), interpolation=cv2.INTER_CUBIC)
        # ...and the breeze only touches the water in patches (catspaws).
        patch = fbm(h // 8, w // 8, 3, np.random.default_rng(77))
        patch = cv2.resize(patch, (w, h), interpolation=cv2.INTER_CUBIC)
        self.patch = (0.25 + 0.75 * np.clip((patch - 0.42) * 3.0, 0, 1)).astype(np.float32)

        # Haze over the water, held to a band either side of the horizon.
        band = np.exp(-((yy - H) / (0.10 * h)) ** 2)
        self.band = band.astype(np.float32)
        self.mist_a = Mist(w, h, 74, octaves=4, lo=0.42, gain=1.8, pad=(420, 200))
        self.mist_b = Mist(w, h, 75, octaves=3, lo=0.46, gain=2.0, pad=(420, 200))

        self.vig = vignette(w, h, 0.55)

    def at(self, t):
        t = t % self.period
        P, h, w = self.period, self.h, self.w
        d = self.depth

        # Ripples: three wave trains with whole numbers of cycles a period,
        # travelling down the water (towards the viewer), amplitude growing
        # with nearness.
        ph = TAU * t / P
        dx = (np.sin(3 * ph - 38.0 * d ** 0.6) * 0.6
              + np.sin(5 * ph - 71.0 * d ** 0.6 + 1.3) * 0.3
              + np.sin(8 * ph - 120.0 * d ** 0.6 + 2.1) * 0.15)
        dy = np.sin(4 * ph - 55.0 * d ** 0.6 + 0.7)
        amp = 2.0 + 26.0 * d ** 1.5
        map_x = (self.xx + dx * amp).astype(np.float32)
        map_y = np.clip(self.mirror_y + dy * (0.6 + 8.0 * d ** 1.5), 0,
                        self.H - 1).astype(np.float32)
        refl = cv2.remap(self.sky, map_x, map_y, cv2.INTER_LINEAR,
                         borderMode=cv2.BORDER_REFLECT)
        refl = refl * self.WATER * (0.95 - 0.30 * d[..., None])
        lines = np.sin(4 * ph - 150.0 * d ** 0.55 + 14.0 * self.bend)
        lines = np.sign(lines) * np.abs(lines) ** 3            # thin crests
        refl = refl * (1 + 0.11 * d ** 0.8 * self.patch * lines)[..., None]

        # Glints slide sideways on a closed circle and shimmer.
        a = ph
        gx = 120 + 90 * math.cos(a)
        gy = 40 + 30 * math.sin(2 * a)
        M = np.float32([[1, 0, -gx], [0, 1, -gy]])
        gl = cv2.warpAffine(self.glint, M, (w, h), flags=cv2.INTER_LINEAR)
        shimmer = 0.75 + 0.25 * math.sin(6 * ph)
        refl = refl + (self.SUN * 0.85) * (gl * self.column * shimmer)[..., None]
        refl = refl + self.SUN * 0.10 * (gl * (1 - self.column) * d)[..., None]

        f = self.sky * (1 - self.water) + refl * self.water
        f = f * (1 - self.shore) + cv2.GaussianBlur(f, (0, 0), 2.5) * self.shore

        # The light comes up a touch and settles, once a loop.
        f = f * (0.96 + 0.04 * math.cos(ph))

        # Rose haze: two sheets, opposite ways, over the horizon band.
        m = (self.mist_a.at(t, P, 1, 150) * 0.55
             + self.mist_b.at(t, P, -1, 110, phase=math.pi) * 0.45)
        k = (m * self.band * 0.55)[..., None]
        f = f * (1 - k) + self.HAZE * k

        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
