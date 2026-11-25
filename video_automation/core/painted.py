"""Backgrounds drawn at the frame's own size, every frame - no rings.

**Why (2026-11-21, the editor's note on the OktAI opener):** "the background
is good but there are some circles which ruin the quality, the animation is
not so good with the circle movement" - and the tinnitus purple has the same
fault. Measured on a frame of the draft: the centre glow spans luminance 12
to 37, so 25 flat 8-bit steps, each a visible ring. Three things made them:

1. **The loop is a 512 px 8-bit video stretched 3.75x.** Its glow was
   already quantised to whole levels, and stretching a step makes it wider,
   not smoother.
2. **The dither that was meant to hide them changes every frame**
   (`Backdrop._dither`, +-1.5 levels of per-pixel noise). Fine noise that
   changes every frame is the first thing an encoder throws away: at crf 18
   the final video had the rings back.
3. **The glows travelled on circles**, so the rings crawled across the
   frame - the movement the note was about.

So a painted background is computed in float at the output size, its glows
**hold still**, and the grain that breaks the steps is **static** and
slightly soft (a 1 px blur): an encoder keeps a texture that does not change
between frames, and does not keep one that does. Motion comes from what
cannot band - small stars twinkling and drifting a few pixels - and from
the beats themselves.

Same interface as `backdrop.Backdrop` (`at(t, w, h)`), and `backdrop.get`
returns one of these for any name in `PAINTED`, so a brand changes nothing.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

LOOP = 24.0            # seconds; every motion completes whole cycles in it
GRAIN = 1.6            # static grain, std in 8-bit levels, after its blur
FLICKER = 0.6          # a little per-frame noise on top, half-level scale


@dataclass
class Glow:
    cx: float              # centre, as fractions of the frame's width and height
    cy: float
    sigma: float           # falloff, as a fraction of the frame's diagonal
    colour: tuple          # RGB 0..255, added at `strength`
    strength: float


@dataclass
class Spec:
    base: tuple                     # RGB of the ground
    glows: list
    stars: int = 0                  # per 1920x1080 frame
    star_peak: float = 0.30         # of white
    vignette: float = 0.35
    drift: tuple = (14.0, -6.0)     # px the star layer travels per loop
    # Falling stars, the portfolio's: (x, y as fractions, second in the loop
    # it starts). Each streaks down-left at -35 degrees for ~1.2 s.
    shooting: tuple = ()
    grain: float = GRAIN            # static grain std, 8-bit levels
    flicker: float = FLICKER        # per-frame noise, half-level scale


@dataclass
class Painted:
    name: str
    spec: Spec
    _ground: dict = field(default_factory=dict)
    _stars: dict = field(default_factory=dict)
    _flick: dict = field(default_factory=dict)
    _tick: int = 0

    # -- the still part, once per size ------------------------------------

    def _make_ground(self, w: int, h: int) -> np.ndarray:
        s = self.spec
        y, x = np.mgrid[0:h, 0:w].astype(np.float32)
        diag = math.hypot(w, h)
        out = np.zeros((h, w, 3), np.float32)
        out[:] = np.array(s.base, np.float32)
        for g in s.glows:
            # Placed against the frame's long side, so a 9:16 frame gets
            # the same glow standing up rather than a squashed one.
            gx, gy = (g.cx * w, g.cy * h)
            d2 = (x - gx) ** 2 + (y - gy) ** 2
            fall = np.exp(-d2 / (2.0 * (g.sigma * diag) ** 2))
            out += np.array(g.colour, np.float32) * g.strength * fall[..., None]
        r2 = ((x / w - 0.5) ** 2 + (y / h - 0.5) ** 2)
        out *= (1.0 - s.vignette * np.clip(r2 * 1.6, 0, 1))[..., None]
        # Static grain: soft enough not to read as dirt, still enough for an
        # encoder to keep. Same field in all three channels (luma grain).
        import cv2
        rng = np.random.default_rng(11)
        g = rng.normal(0, 1, (h, w)).astype(np.float32)
        g = cv2.GaussianBlur(g, (0, 0), 0.8)
        g *= s.grain / (g.std() + 1e-6)
        out += g[..., None]
        return out

    def _make_stars(self, w: int, h: int):
        s = self.spec
        n = int(round(s.stars * (w * h) / (1920 * 1080)))
        rng = np.random.default_rng(21)
        # Three sizes, like the portfolio's three layers: mostly dust-fine,
        # some medium, a few large and bright.
        size = rng.uniform(0, 1, n)
        return dict(
            xy=rng.uniform(0, 1, (n, 2)) * (w, h),
            peak=rng.uniform(0.35, 1.0, n) * s.star_peak * 255
            * np.where(size > 0.93, 1.5, np.where(size > 0.7, 1.15, 0.8)),
            turns=rng.integers(1, 4, n),
            phase=rng.uniform(0, 1, n),
            sigma=np.where(size > 0.93, 1.4, np.where(size > 0.7, 0.95, 0.6)),
        )

    # -- per frame ----------------------------------------------------------

    def at(self, t: float, w: int, h: int) -> np.ndarray:
        key = (w, h)
        if key not in self._ground:
            self._ground[key] = self._make_ground(w, h)
            self._stars[key] = self._make_stars(w, h)
            rng = np.random.default_rng(5)
            fl = self.spec.flicker
            self._flick[key] = [rng.uniform(-fl, fl, (h, w, 1)
                                            ).astype(np.float32) for _ in range(6)]
        out = self._ground[key].copy()
        st = self._stars[key]
        if len(st["peak"]):
            p = (t % LOOP) / LOOP
            dx, dy = self.spec.drift
            for (sx, sy), pk, n, ph, sg in zip(st["xy"], st["peak"], st["turns"],
                                               st["phase"], st["sigma"]):
                x = (sx + dx * p) % w
                y = (sy + dy * p) % h
                tw = 0.55 + 0.45 * math.cos(2 * math.pi * (n * p + ph))
                x0, y0 = int(x) - 3, int(y) - 3
                x1, y1 = min(w, x0 + 7), min(h, y0 + 7)
                x0, y0 = max(0, x0), max(0, y0)
                if x1 <= x0 or y1 <= y0:
                    continue
                yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
                d2 = (xx - x) ** 2 + (yy - y) ** 2
                out[y0:y1, x0:x1] += (pk * tw * np.exp(-d2 / (2 * sg * sg)))[..., None]
        for sx, sy, at in self.spec.shooting:
            self._shoot(out, t, sx * w, sy * h, at, h / 1080)
        out += self._flick[key][self._tick % 6]
        self._tick += 1
        return np.clip(out + 0.5, 0, 255).astype(np.uint8)

    # The portfolio's shooting star (`portfolio/assets/css/starry-night.css`):
    # a 170 px streak, warm white, its head a glowing dot, travelling 520 px
    # along -35 degrees over 4.5% of a 27 s cycle (~1.2 s), fading in fast
    # and out as it goes. Sizes are at 1440 px CSS width, scaled to 1080p.
    SHOOT_TIME = 1.2
    SHOOT_TRAVEL = 700.0
    SHOOT_TAIL = 230.0

    def _shoot(self, out: np.ndarray, t: float, x0: float, y0: float,
               at: float, k: float) -> None:
        e = (t % LOOP) - at
        if not 0.0 <= e <= self.SHOOT_TIME:
            return
        q = e / self.SHOOT_TIME
        alpha = min(1.0, q / 0.11) * (1.0 - max(0.0, (q - 0.66) / 0.34))
        ang = math.radians(180 + 35)               # down and to the left
        ux, uy = math.cos(ang), -math.sin(ang)
        hx = x0 + ux * self.SHOOT_TRAVEL * k * q
        hy = y0 + uy * self.SHOOT_TRAVEL * k * q
        h, w = out.shape[:2]
        tail = self.SHOOT_TAIL * k
        warm = np.array((255, 246, 222), np.float32)

        def dot(x, y, sigma, amp):
            r = int(sigma * 3) + 1
            xa, ya = int(x) - r, int(y) - r
            xb, yb = min(w, xa + 2 * r + 1), min(h, ya + 2 * r + 1)
            xa, ya = max(0, xa), max(0, ya)
            if xb <= xa or yb <= ya:
                return
            yy, xx = np.mgrid[ya:yb, xa:xb].astype(np.float32)
            g = np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * sigma * sigma))
            out[ya:yb, xa:xb] += (amp * g)[..., None] * warm / 255.0

        n = max(48, int(tail / 0.8))          # under a pixel apart: one line
        for i in range(n):
            f = i / n
            dot(hx - ux * tail * f, hy - uy * tail * f, 0.9 * k + 0.25,
                70.0 * alpha * (1.0 - f) ** 1.6)
        dot(hx, hy, 2.2 * k, 255.0 * alpha)          # the head
        dot(hx, hy, 9.0 * k, 55.0 * alpha)           # its glow


# The OktAI sky, the portfolio's (2026-11-23, the editor: "test a dark
# screen with stars and a couple of falling stars like in my portfolio, so it
# matches"): its near-black ground (#050507 to #08090d), a faint navy glow
# where the type sits, a starfield in three sizes and three falling stars a
# loop, one every eight seconds, high in the frame and clear of the type.
OKTAI_NIGHT = Spec(
    base=(5, 5, 8),
    glows=[Glow(0.50, 0.46, 0.30, (30, 34, 56), 0.50),
           Glow(0.78, 0.22, 0.16, (255, 200, 110), 0.03)],
    stars=280, star_peak=0.55,
    # One every four seconds (the editor, 2026-11-23: "a bit more often").
    shooting=((0.80, 0.08, 1.5), (0.40, 0.05, 5.5), (0.62, 0.14, 9.5),
              (0.92, 0.03, 13.5), (0.30, 0.12, 17.5), (0.72, 0.06, 21.5)),
    # "Real dark space, and the stars inside it" - no dust (2026-11-23). A
    # trace of static dither stays only so the faint glow cannot band.
    grain=0.45, flicker=0.0,
)

# Tinnitus: PLUM's colours, still.
TINNITUS_PLUM = Spec(
    base=(14, 8, 24),
    glows=[Glow(0.42, 0.46, 0.30, (70, 40, 100), 0.34),
           Glow(0.64, 0.56, 0.34, (50, 26, 82), 0.30)],
)

PAINTED = {"oktai-night": OKTAI_NIGHT, "tinnitus-plum": TINNITUS_PLUM}
