"""The look for `bird-chirps-55-breathing` (long + Short), and only that.

`SparrowBranch`: a sparrow on a curving branch against dark green, morning
light. Pexels 33104821 by 정규송 Nui MALAMA
(https://www.pexels.com/photo/sparrow-perched-on-tree-branch-in-natural-habitat-33104821/),
read from the stock cache, which is not in git - re-pull with
`stock.photos("small bird on branch morning bokeh")` if it is missing.

**The bird is placed, not centred.** The ring sits in the middle of the
frame and the label inside it, so the photograph is cropped to put the
sparrow in the left third of the landscape frame and below the ring in the
portrait one. The bluebird (10696286) was the prettier picture and was
dropped for exactly this: it is too big to keep its head out of the ring at
any crop.

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.bird_chirps_55 import SparrowBranch
"""

from __future__ import annotations

import math

import cv2
import numpy as np

from ...core.looks import Fireflies, Look, ease, orbit, vignette
from ...core.stock import CACHE


class SparrowBranch(Look):
    """A still photograph that comes into focus on the inhale.

    The picture eases from soft to sharp and zooms 3% as the breath comes in,
    and a warm light from the upper right swells with it, so the breathing
    part of the look reads the pattern: `period` must be a whole number of
    `inhale + hold + exhale`. With no pattern (the session thumbnails) the
    breath holds at its midpoint. The orbit and the motes close on `period`
    directly.
    """

    ring = (255, 238, 205)
    SRC = CACHE / "photos/small-bird-on-branch-morning-bokeh/33104821.jpg"
    BIRD = (0.415, 0.515)          # the sparrow in the source, as a fraction
    PAD = 60                       # room for the orbit and the zoom
    # Where the bird lands in the frame, and how much of the source shows:
    # left third in landscape, below the ring in portrait.
    LANDSCAPE = ((0.22, 0.60), 1.30)
    PORTRAIT = ((0.5, 0.79), 1.58)

    def __init__(self, w, h, period, pattern=None):
        super().__init__(w, h, period, pattern)
        if pattern:
            breath = sum(pattern)
            if abs(period / breath - round(period / breath)) > 1e-6:
                raise ValueError(f"period {period}s is not a whole number of "
                                 f"{breath}s breaths")
        img = cv2.cvtColor(cv2.imread(str(self.SRC)), cv2.COLOR_BGR2RGB)
        place, zoom = self.PORTRAIT if h > w else self.LANDSCAPE
        self.big = self._frame(img, place, zoom)
        self.soft = cv2.GaussianBlur(self.big, (0, 0), 5)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        # Darken the middle a little more, so the ring and its label sit on
        # an even field rather than on the brightest leaves.
        pool = 1 - 0.35 * np.exp(-(((xx - w / 2) / (0.28 * max(w, h))) ** 2
                                   + ((yy - h / 2) / (0.22 * max(w, h))) ** 2))
        self.shade = vignette(w, h, 0.55) * pool[..., None]
        lx, ly = (w * 0.9, h * 0.08)
        d = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2) / math.hypot(w, h)
        self.light = (np.exp(-(d / 0.45) ** 2)[..., None]
                      * np.array([255, 205, 140], np.float32))
        self.motes = Fireflies(w, h, 20, 21, color=(255, 230, 175), r=(2, 5),
                               margin=(0.06, 0.08))

    def _frame(self, img, place, zoom):
        """Crop the source so `BIRD` lands at `place`, with `PAD` to spare."""
        W, H = self.w + 2 * self.PAD, self.h + 2 * self.PAD
        ih, iw = img.shape[:2]
        k = max(W / iw, H / ih) * zoom
        r = cv2.resize(img, (math.ceil(iw * k), math.ceil(ih * k)),
                       interpolation=cv2.INTER_AREA)
        x0 = int(self.BIRD[0] * r.shape[1] - place[0] * self.w - self.PAD)
        y0 = int(self.BIRD[1] * r.shape[0] - place[1] * self.h - self.PAD)
        x0 = max(0, min(x0, r.shape[1] - W))
        y0 = max(0, min(y0, r.shape[0] - H))
        big = r[y0:y0 + H, x0:x0 + W].astype(np.float32)
        big *= 0.70 * np.array([0.95, 1.0, 0.92], np.float32)
        return np.clip(big, 0, 255).astype(np.uint8)

    def _r(self, t):
        if not self.pattern:
            return 0.5
        i, hd, e = self.pattern
        p = t % (i + hd + e)
        if p < i:
            return ease(p / i)
        if p < i + hd:
            return 1.0
        return 1.0 - ease((p - i - hd) / e)

    def at(self, t):
        r = self._r(t)
        z = 1.0 + 0.03 * r
        f = orbit(self.big, self.w, self.h, t, self.period, 16, z).astype(np.float32)
        b = orbit(self.soft, self.w, self.h, t, self.period, 16, z).astype(np.float32)
        f = (b + (f - b) * (0.4 + 0.6 * r)) * self.shade
        f += self.light * (0.10 + 0.08 * r)
        self.motes.draw(f, t, self.period, 0.5)
        return np.clip(f, 0, 255).astype(np.uint8)


class SparrowBranchThumb(SparrowBranch):
    """The long-form thumbnail's crop of the same picture.

    The session thumbnail puts its headline on the left, exactly where the
    video's landscape crop keeps the bird, so the first thumbnail had no bird
    in it. This one sets the sparrow low, under the pattern chip, with the
    branch curving up into the ring.
    """

    LANDSCAPE = ((0.44, 0.84), 1.6)
