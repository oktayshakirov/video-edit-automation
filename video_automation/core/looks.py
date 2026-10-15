"""Session looks: the format for the picture behind a sound-therapy ring.

The nebula (`tinnitus.asmr.nebula_canvas`) was the only background a session
had, so every session on the channel read as the same video re-tinted. A look
is a whole picture instead, and **each one is used by exactly one video** —
rain, fireplace, jungle, each built fresh in its own style. What is reused is
the format, which is this module:

* **`Look`** — the contract. `at(t)` returns an (h, w, 3) uint8 frame and must
  equal `at(t + period)`, negative `t` included, because the long form renders
  one loop and repeats it and the bookends run the clock below zero
  (`tests/test_looks.py` holds every look to it).
* **The pieces a look is made from**, all closed over `period`: `Mist` (fbm
  sheets on a circle), `Fireflies` (glow points on closed orbits), `orbit`
  (a window on a still, drifting round a circle), `vignette`, `cover`,
  `fbm`, `ease`.
* **The shelf** (`SHELF`) — looks built and approved but not yet used. When
  a video takes one, its class moves out of this file into that video's own
  module under `tinnitus/session_looks/`, so the shelf only ever offers looks
  no video has, and the video that used it still re-renders.

| on the shelf | what it is | material |
| --- | --- | --- |
| `canopy-fog` | misty-forest footage, ping-ponged, graded down, a few fireflies | Pexels 19366762 |
| `cascade-still` | a waterfall photograph on a slow orbit, drifting mist, pulsing light shafts | Pexels 12321837 |
| `fern-breath` | a dark fern photograph that zooms and sharpens with the inhale | Pexels 27286261 |

**Frame-size agnostic.** A look is built at 1920x1080 for the long form and at
1080x1920 for its Short, so the pair match; anything placed by the edges needs
a portrait arrangement of its own, and photographs are cover-cropped.

The photo and footage looks read the Pexels cache (`core.stock.CACHE`), which
is not in git. If a file is missing, re-pull it with `stock.videos` or
`stock.photos`; the id is in the table above.
"""

from __future__ import annotations

import math
import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from .stock import CACHE

TAU = 2 * math.pi


# --- shared pieces -----------------------------------------------------------

def fbm(h: int, w: int, octaves: int, rng: np.random.Generator) -> np.ndarray:
    """Fractal value noise, same construction as the nebula's."""
    out = np.zeros((h, w), np.float32)
    amp, total = 1.0, 0.0
    for o in range(octaves):
        n = 4 * 2 ** o
        grid = rng.random((n, int(n * w / h) + 1), dtype=np.float32)
        out += amp * cv2.resize(grid, (w, h), interpolation=cv2.INTER_CUBIC)
        total += amp
        amp *= 0.55
    return out / total


def cover(img: np.ndarray, w: int, h: int) -> np.ndarray:
    ih, iw = img.shape[:2]
    s = max(w / iw, h / ih)
    r = cv2.resize(img, (math.ceil(iw * s), math.ceil(ih * s)),
                   interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    y, x = (r.shape[0] - h) // 2, (r.shape[1] - w) // 2
    return r[y:y + h, x:x + w]


def ease(x: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, x)))


class Mist:
    """A soft fbm sheet sliding round a circle `k` times per period."""

    def __init__(self, w, h, seed, octaves=4, lo=0.45, gain=2.0, pad=(400, 300)):
        self.w, self.h = w, h
        tex = fbm(h + pad[1], w + pad[0], octaves, np.random.default_rng(seed))
        self.tex = np.clip((tex - lo) * gain, 0, 1).astype(np.float32)

    def at(self, t, period, k, rad, phase=0.0):
        a = TAU * k * t / period + phase
        dx = (self.tex.shape[1] - self.w) / 2 + rad * math.cos(a)
        dy = (self.tex.shape[0] - self.h) / 2 + rad * 0.5 * math.sin(a)
        M = np.float32([[1, 0, -dx], [0, 1, -dy]])
        return cv2.warpAffine(self.tex, M, (self.w, self.h), flags=cv2.INTER_LINEAR)


class Fireflies:
    """Glow points on closed orbits, each pulsing a whole number of times."""

    def __init__(self, w, h, n, seed, color=(214, 255, 150), margin=(0.08, 0.15),
                 r=(3, 7)):
        rng = np.random.default_rng(seed)
        mx, my = int(w * margin[0]), int(h * margin[1])
        self.w, self.h = w, h
        self.p = [dict(x=rng.uniform(mx, w - mx), y=rng.uniform(my, h - my),
                       ax=rng.uniform(20, 90), ay=rng.uniform(15, 60),
                       k=int(rng.integers(1, 3)), ph=rng.uniform(0, TAU),
                       pk=int(rng.integers(2, 6)), pph=rng.uniform(0, TAU),
                       s=int(rng.integers(0, 3))) for _ in range(n)]
        self.sprites = []
        for rad in np.linspace(r[0], r[1], 3):
            rad = int(rad)
            s = rad * 6 + 1
            g = np.zeros((s, s), np.float32)
            cv2.circle(g, (s // 2, s // 2), max(1, rad // 2), 1.0, -1)
            g = (cv2.GaussianBlur(g, (0, 0), rad * 0.8)
                 + cv2.GaussianBlur(g, (0, 0), rad * 2) * 0.6)
            g /= g.max()
            self.sprites.append(g[..., None] * np.array(color, np.float32)[None, None])

    def draw(self, f: np.ndarray, t: float, period: float, gain=1.0):
        for q in self.p:
            a = TAU * q["k"] * t / period + q["ph"]
            x = q["x"] + q["ax"] * math.cos(a)
            y = q["y"] + q["ay"] * math.sin(2 * a + q["ph"])
            lum = max(0.0, math.sin(TAU * q["pk"] * t / period + q["pph"])) ** 2
            spr = self.sprites[q["s"]]
            s = spr.shape[0]
            x0, y0 = int(x) - s // 2, int(y) - s // 2
            xa, ya = max(0, x0), max(0, y0)
            xb, yb = min(self.w, x0 + s), min(self.h, y0 + s)
            if xa < xb and ya < yb:
                f[ya:yb, xa:xb] += (spr[ya - y0:yb - y0, xa - x0:xb - x0]
                                    * (gain * (0.15 + 0.85 * lum)))


def vignette(w, h, strength):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    return (1 - strength * np.clip(d - 0.35, 0, 1) ** 1.4)[..., None]


def orbit(big: np.ndarray, w, h, t, period, rad, zoom=1.0):
    """A w x h window of `big`, centred on a closed circle, optionally zoomed."""
    a = TAU * t / period
    cx = big.shape[1] / 2 + rad * math.cos(a)
    cy = big.shape[0] / 2 + rad * math.sin(a)
    sw, sh = w / zoom, h / zoom
    M = np.float32([[zoom, 0, -(cx - sw / 2) * zoom],
                    [0, zoom, -(cy - sh / 2) * zoom]])
    return cv2.warpAffine(big, M, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REFLECT)


class Look:
    """A background: `at(t)` -> (h, w, 3) uint8, closed over `period`."""

    ring: tuple = (226, 246, 220)

    def __init__(self, w: int, h: int, period: float,
                 pattern: tuple[float, float, float] | None = None):
        self.w, self.h, self.period = w, h, period
        self.pattern = pattern

    def at(self, t: float) -> np.ndarray:
        raise NotImplementedError

    def still(self, t: float = 0.0) -> Image.Image:
        """One frame as an image — what a thumbnail is built on."""
        return Image.fromarray(self.at(t))


# --- canopy-fog --------------------------------------------------------------

class CanopyFog(Look):
    """Real footage, forward then reversed so the join is exact.

    The ping-pong cycle has to divide `period`, and the source is only so
    long, so the cycle is `period / k` for the smallest whole `k` the clip can
    cover. Fog has no arrow of time, which is why it reverses invisibly. The
    source is 1280x720, so a portrait crop is a ~2.7x upscale — soft, which fog
    forgives and almost nothing else would.
    """

    ring = (210, 240, 214)
    SRC = CACHE / "videos/jungle-canopy-fog/19366762.mp4"

    def __init__(self, w, h, period, pattern=None, fps: int = 30,
                 start: float = 1.0):
        super().__init__(w, h, period, pattern)
        if not self.SRC.exists():
            raise FileNotFoundError(
                f"{self.SRC} — re-pull with stock.videos('jungle canopy fog')")
        have = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(self.SRC)], capture_output=True,
            text=True, check=True).stdout) - start - 0.3
        k = 1
        while period / k / 2 > have:
            k += 1
        self.cycle = period / k
        half = int(round(self.cycle / 2 * fps))
        self.fps = fps
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(start), "-t",
             f"{self.cycle / 2 + 0.3:.3f}", "-i", str(self.SRC), "-vf",
             f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,"
             f"crop={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True, check=True).stdout
        self.frames = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)[:half + 1]
        n = len(self.frames)
        # every source frame once except the two extremes (core.backdrop.pingpong)
        self.seq = list(range(n)) + list(range(n - 2, 0, -1))
        self.grade = (0.62 * np.array([0.80, 0.98, 0.90], np.float32)
                      * vignette(w, h, 0.6))
        self.ff = Fireflies(w, h, 18, 3, margin=(0.05, 0.32), r=(2, 5))

    def at(self, t):
        i = int(round((t % self.cycle) * self.fps)) % len(self.seq)
        f = self.frames[self.seq[i]].astype(np.float32) * self.grade
        self.ff.draw(f, t, self.period, 0.55)
        return np.clip(f, 0, 255).astype(np.uint8)


# --- cascade-still -----------------------------------------------------------

class CascadeStill(Look):
    """A still waterfall photograph, alive by orbit, mist and light only."""

    ring = (226, 246, 220)
    SRC = CACHE / "photos/jungle-waterfall/12321837.jpg"

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        img = cv2.cvtColor(cv2.imread(str(self.SRC)), cv2.COLOR_BGR2RGB)
        big = cover(img, w + 160, h + 160).astype(np.float32)
        big *= 0.58 * np.array([0.85, 1.0, 0.95], np.float32)
        self.big = np.clip(big, 0, 255).astype(np.uint8)
        self.m1 = Mist(w, h, 11, lo=0.48, gain=2.0)
        self.m2 = Mist(w, h, 12, octaves=3, lo=0.45, gain=1.6)
        self.shafts = self._shafts(5, -22)[..., None]
        self.vig = vignette(w, h, 0.55)

    def _shafts(self, seed, angle):
        rng = np.random.default_rng(seed)
        big = int(math.hypot(self.w, self.h)) + 700
        m = np.zeros((big, big), np.float32)
        for _ in range(7):
            x = int(rng.uniform(0.15, 0.85) * big)
            bw = int(rng.uniform(25, 110))
            m[:, x - bw // 2:x + bw // 2] += rng.uniform(0.35, 1.0)
        m = cv2.GaussianBlur(m, (0, 0), 30)
        m *= np.linspace(1.0, 0.15, big, dtype=np.float32)[:, None]
        m = cv2.warpAffine(m, cv2.getRotationMatrix2D((big / 2, big / 2), angle, 1.0),
                           (big, big))
        y0, x0 = (big - self.h) // 2 - 160, (big - self.w) // 2 + 200
        m = m[y0:y0 + self.h, x0:x0 + self.w]
        return np.clip(m / m.max(), 0, 1)

    def at(self, t):
        f = orbit(self.big, self.w, self.h, t, self.period, 50).astype(np.float32)
        mist = (0.22 * self.m1.at(t, self.period, 1, 150)
                + 0.14 * self.m2.at(t, self.period, 2, 120, 1.0))
        f += (235 - f) * mist[..., None]
        pulse = 0.5 + 0.5 * math.sin(TAU * 2 * t / self.period)
        f += self.shafts * (40 + 30 * pulse) * np.array([1.0, 1.0, 0.82], np.float32)
        return np.clip(f * self.vig, 0, 255).astype(np.uint8)


# --- fern-breath -------------------------------------------------------------

class FernBreath(Look):
    """A dark fern photograph that breathes with the ring.

    It zooms in 4.5% and comes into focus on the inhale, holds, and eases back
    out on the exhale — the whole picture follows the pattern, so it needs the
    pattern: `period` must be a whole number of `inhale + hold + exhale`.
    """

    ring = (236, 250, 206)
    SRC = CACHE / "photos/dark-jungle-leaves/27286261.jpg"

    def __init__(self, w, h, period, pattern=(4.0, 0.0, 6.0)):
        super().__init__(w, h, period, pattern or (4.0, 0.0, 6.0))
        inhale, hold, exhale = self.pattern
        breath = inhale + hold + exhale
        if abs(period / breath - round(period / breath)) > 1e-6:
            raise ValueError(f"period {period}s is not a whole number of "
                             f"{breath}s breaths")
        img = cv2.cvtColor(cv2.imread(str(self.SRC)), cv2.COLOR_BGR2RGB)
        big = cover(img, int(w * 1.12), int(h * 1.12)).astype(np.float32)
        big *= 0.72 * np.array([0.9, 1.0, 0.95], np.float32)
        self.big = np.clip(big, 0, 255).astype(np.uint8)
        self.soft = cv2.GaussianBlur(self.big, (0, 0), 6)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        pool = 1 - 0.45 * np.exp(-(((xx - w / 2) / 520) ** 2 + ((yy - h / 2) / 420) ** 2))
        self.shade = vignette(w, h, 0.65) * pool[..., None]
        self.ff = Fireflies(w, h, 22, 13, color=(255, 236, 170), r=(2, 6))

    def _r(self, t):
        i, hd, e = self.pattern
        p = t % (i + hd + e)
        if p < i:
            return ease(p / i)
        if p < i + hd:
            return 1.0
        return 1.0 - ease((p - i - hd) / e)

    def at(self, t):
        r = self._r(t)
        z = 1.0 + 0.045 * r
        f = orbit(self.big, self.w, self.h, t, self.period, 22, z).astype(np.float32)
        b = orbit(self.soft, self.w, self.h, t, self.period, 22, z).astype(np.float32)
        f = (b + (f - b) * (0.45 + 0.55 * r)) * self.shade
        self.ff.draw(f, t, self.period, 0.7)
        return np.clip(f, 0, 255).astype(np.uint8)


# The shelf: looks built and approved but not yet used. A look is used once —
# when a video takes one, its class moves out of here into that video's own
# module under `tinnitus/session_looks/`, so the shelf only ever offers looks
# no published video has.
SHELF = {"canopy-fog": CanopyFog, "cascade-still": CascadeStill,
         "fern-breath": FernBreath}


def make(look: "str | type[Look]", w: int, h: int, period: float,
         pattern: tuple[float, float, float] | None = None) -> Look:
    """Build a look for one frame size and loop period.

    `look` is a shelf name or a `Look` subclass — the latter is how a video
    uses the look that belongs to it. `pattern` is `(inhale, hold, exhale)`;
    only a look that moves with the breath reads it, but the renderers always
    pass it so a caller never has to know which looks those are.
    """
    if isinstance(look, type) and issubclass(look, Look):
        return look(w, h, period, pattern)
    try:
        cls = SHELF[look]
    except (KeyError, TypeError):
        raise ValueError(f"unknown look {look!r}; the shelf has {sorted(SHELF)} "
                         f"(a used look is passed as its class)") from None
    return cls(w, h, period, pattern)
