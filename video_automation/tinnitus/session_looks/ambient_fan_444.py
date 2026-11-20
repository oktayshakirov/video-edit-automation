"""The look for `fan-noise-444-breathing` (long + Short), and only that.

`NightDraft`: a bedroom wall at night, a tall window behind sheer curtains,
and the curtains stirring in the air a fan pushes across the room. Moonlight
comes through the fabric cool and silver from the top right, a faint amber
streetlight glows low on the left, and the shadow of the window's frame
shows through the sheers as a soft cross. The cloth hangs still at the rod
and moves more towards the hem, in two slow swells that never line up, and
a few specks of dust drift through the light. Fully generated: no stock, no
licence, no credit.

It answers the last look (`AmberDusk`, `brown-noise-478`): indoors instead
of a landscape, cool moonlight instead of a warm dusk, and the one thing in
the picture that moves is moved by the air the bed is the sound of - the fan
in *Ambient Fan* (Background Blur album).

The look does not read the breath: the path guide draws every phase, and a
look that ignores `pattern` builds for the thumbnail without one.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.ambient_fan_444 import NightDraft
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import TAU, Fireflies, Look, fbm, vignette


class NightDraft(Look):
    """Sheer curtains over a moonlit window, stirring in a fan's draught."""

    ring = (228, 236, 255)
    WALL = np.array([10, 13, 22], np.float32)          # the room, near black
    MOON = np.array([172, 190, 222], np.float32)       # cool silver through cloth
    STREET = np.array([150, 104, 60], np.float32)      # a low amber glow
    PAD = 160                                          # fabric beyond the frame

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        land = w >= h
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        rng = np.random.default_rng(61)

        # The fabric, one row wide: fold transmission across x. Sheers gather
        # into uneven folds, so a few sines at irregular spacing plus a
        # finer ripple; the light shows through the thin parts.
        tw = w + 2 * self.PAD
        x = np.arange(tw, dtype=np.float32)
        n_folds = 15 if land else 10
        fold = np.zeros(tw, np.float32)
        for k, a in ((n_folds, 1.0), (n_folds * 1.63, 0.45), (n_folds * 3.1, 0.18)):
            fold += a * np.sin(TAU * k * x / tw + rng.uniform(0, TAU))
        fold = (fold - fold.min()) / (fold.max() - fold.min())
        self.fold = (0.55 + 0.45 * fold).astype(np.float32)

        # Where the light is behind the cloth: the moon up and to the right,
        # the streetlight low and to the left, both broad.
        mx, my = (0.70 * w, 0.24 * h) if land else (0.66 * w, 0.20 * h)
        dm = np.sqrt(((xx - mx) / (0.55 * w)) ** 2 + ((yy - my) / (0.62 * h)) ** 2)
        moon = np.exp(-dm ** 2 * 1.6)
        ds = np.sqrt(((xx - 0.12 * w) / (0.40 * w)) ** 2
                     + ((yy - 0.92 * h) / (0.42 * h)) ** 2)
        street = np.exp(-ds ** 2 * 2.0)
        self.moon = moon[..., None].astype(np.float32)
        self.street = street[..., None].astype(np.float32)

        # The window frame behind the sheers: one upright and one rail, a
        # soft cross of shadow, plus the outer edges of the opening.
        frame = np.zeros((h, w), np.float32)
        x0, x1 = (0.18 * w, 0.92 * w) if land else (0.08 * w, 0.94 * w)
        y0, y1 = 0.06 * h, (0.86 if land else 0.82) * h
        inside = ((xx > x0) & (xx < x1) & (yy > y0) & (yy < y1)).astype(np.float32)
        inside = cv2.GaussianBlur(inside, (0, 0), 0.03 * min(w, h))
        bar = max(6, int(0.012 * min(w, h)))
        cxm, cym = (x0 + x1) / 2, y0 + 0.42 * (y1 - y0)
        frame[:, int(cxm) - bar:int(cxm) + bar] = 1.0
        frame[int(cym) - bar:int(cym) + bar, :] = 1.0
        frame = cv2.GaussianBlur(frame, (0, 0), 0.02 * min(w, h)) * inside
        self.light = np.clip(inside * (1 - 0.55 * frame / max(frame.max(), 1e-6)),
                             0, 1)[..., None].astype(np.float32)

        # How far the cloth can move: nothing at the rod, most at the hem.
        self.hem = (0.90 if land else 0.88) * h
        self.sway = (np.clip(yy[:, :1] / self.hem, 0, 1) ** 1.6).astype(np.float32)
        self.xx, self.yy = xx, yy

        # The hem: the cloth ends a little above the sill, a soft dark edge.
        below = np.clip((yy - self.hem) / (0.02 * h), 0, 1)
        self.below = below[..., None].astype(np.float32)

        # Weave: a fixed, very fine grain, so the cloth reads as cloth.
        grain = fbm(h // 2, w // 2, 3, np.random.default_rng(62))
        grain = cv2.resize(grain, (w, h), interpolation=cv2.INTER_LINEAR)
        self.grain = (0.92 + 0.16 * grain)[..., None].astype(np.float32)

        self.dust = Fireflies(w, h, 22 if land else 18, 63,
                              color=(190, 200, 225), margin=(0.10, 0.08),
                              r=(2, 4))
        self.vig = vignette(w, h, 0.62)

    def _dx(self, t):
        """Horizontal displacement of the cloth at `t`, closed over the period."""
        P, w = self.period, self.w
        yn = self.yy[:, :1] / self.h
        a1 = TAU * 1 * t / P
        a2 = TAU * 2 * t / P
        a3 = TAU * 3 * t / P
        # A swell travelling down the cloth, and a slower billow across it.
        wave = (0.60 * np.sin(a1 + TAU * 1.2 * yn + TAU * self.xx[:1] / (0.9 * w))
                + 0.30 * np.sin(a2 + 1.7 + TAU * 2.1 * yn)
                + 0.12 * np.sin(a3 + 0.4 + TAU * self.xx[:1] / (0.35 * w)))
        return (self.sway * 58.0 * wave).astype(np.float32)

    def at(self, t):
        # Wrap first: sin(TAU * (t + P) / P) differs from sin(TAU * t / P) in
        # the last bits, and that rounds one channel a level off - a frame
        # that is not *equal* at the join (`tests/test_looks.py`).
        t = t % self.period
        dx = self._dx(t)
        # Sample the fold profile at the displaced x: the folds slide sideways
        # and bunch where the swell pushes them.
        sx = (self.xx + self.PAD + dx).astype(np.float32)
        fold = np.interp(sx.ravel(), np.arange(self.fold.size, dtype=np.float32),
                         self.fold).reshape(self.h, self.w)[..., None]
        # A billow catches more light where the cloth turns towards the room.
        lift = 1.0 + 0.10 * np.tanh(np.gradient(dx, axis=1) * 2.0)[..., None]

        P = self.period
        breathe = 0.5 + 0.5 * math.cos(TAU * t / P)    # the moon dims a touch
        glow = (self.MOON * self.moon * (0.86 + 0.08 * breathe)
                + self.STREET * self.street * 0.55)
        f = self.WALL + glow * self.light * fold * lift * self.grain
        # Below the hem: the sill and the wall, lit only by what spills down.
        f = f * (1 - self.below) + (self.WALL + glow * 0.18) * self.below
        self.dust.draw(f, t, P, gain=0.35)
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)
