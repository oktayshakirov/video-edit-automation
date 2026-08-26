"""Overlays composited on top of a finished shot — the subscribe sting.

Everything else in this package *is* a shot. This is the one thing that has to
sit **over** whatever the picture is doing, because the end-screen ask belongs
on the outro footage rather than replacing it.

**Black background, not green.** The obvious asset for this is a green-screen
subscribe animation, and the library is full of them. A black-background one is
strictly better for these two channels and it is worth being explicit about why:

* A screen blend over a dark palette is *exact*. `out = 1-(1-a)(1-b)` leaves
  pure black completely transparent with no threshold to tune, no spill
  suppression, and no edge fringing — the three things that make keyed footage
  look cheap.
* Chroma keying a hard green against gold-on-near-black also tints every
  antialiased edge green, and at 1080p on a button with a drop shadow that is
  plainly visible.

The cost is that a screen blend cannot darken, so a black-background asset can
only ever *add* light. For a glowing button on black that is exactly right.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from ..core.frame import LANDSCAPE, Frame


class ClipOverlay:
    """A clip screen-blended over the picture between `start` and `end`.

    `scale` and `at` place it; `at=None` centres it. `fade` is the ramp at each
    end, so the sting arrives and leaves rather than snapping.

    `crop` is fractional `(left, top, right, bottom)` on the source. Stock
    stings are frequently laid out as a strip with divider bars between
    states, and those bars screen-blend into the frame as bright vertical
    lines that look like a rendering fault. Crop to the artwork.
    """

    def __init__(self, path: Path, start: float, end: float,
                 frame: Frame = LANDSCAPE, scale: float = 1.0,
                 at: tuple[int, int] | None = None, fade: float = 0.45,
                 gain: float = 1.0,
                 crop: tuple[float, float, float, float] | None = None,
                 fps: int = 30):
        self.start, self.end, self.fade, self.gain = start, end, fade, gain
        self.frame = frame

        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            raise ValueError(f"cannot open overlay clip {path}")
        src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

        want = max(end - start, 1e-3)
        n_out = max(1, int(round(want * fps)))
        src_n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        # Play it at natural speed and hold the last frame if the window is
        # longer than the clip. A subscribe animation that loops looks like a
        # stutter; one that finishes and rests looks finished.
        last = min(src_n - 1, int(round(want * src_fps)) - 1) if src_n else 0
        wanted = np.linspace(0, max(last, 0), n_out).astype(int)

        # `scale` is a fraction of frame *width*; the height follows the crop's
        # own aspect. Forcing 16:9 was the first version and it stretched a
        # 3.6:1 button strip into a smear.
        w = int(frame.w * scale)
        h = None
        keep, idx, cursor = [], 0, 0
        while idx < src_n and cursor < len(wanted):
            ok, bgr = cap.read()
            if not ok:
                break
            while cursor < len(wanted) and wanted[cursor] == idx:
                # Crop into a new name: reassigning `bgr` here double-crops
                # whenever one source frame is sampled twice, which happens
                # any time the overlay window is longer than the clip.
                src = bgr
                if crop:
                    sh, sw = src.shape[:2]
                    l, t0, r, b = crop
                    src = src[int(t0 * sh):int(b * sh), int(l * sw):int(r * sw)]
                if h is None:
                    h = max(1, int(w * src.shape[0] / src.shape[1]))
                small = cv2.resize(src, (w, h), interpolation=cv2.INTER_AREA)
                keep.append(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
                cursor += 1
            idx += 1
        cap.release()
        if not keep:
            raise ValueError(f"decoded no frames from {path}")
        while len(keep) < n_out:
            keep.append(keep[-1])
        self.frames = keep

        h = h or int(frame.h * scale)
        if at is None:
            at = ((frame.w - w) // 2, (frame.h - h) // 2)
        self.at = at
        self.size = (w, h)

    def draw(self, img: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return img
        p = (t - self.start) / max(self.end - self.start, 1e-6)
        i = min(len(self.frames) - 1,
                max(0, int(round(p * (len(self.frames) - 1)))))

        a = min((t - self.start) / self.fade,
                (self.end - t) / self.fade, 1.0)
        if a <= 0.004:
            return img
        alpha = float(a) * self.gain

        x, y = self.at
        w, h = self.size
        base = np.asarray(img).astype(np.float32)
        over = self.frames[i].astype(np.float32) * alpha

        region = base[y:y + h, x:x + w]
        # Screen: black in the overlay leaves the base untouched, and anything
        # bright adds without ever clipping past white.
        blended = 255.0 - (255.0 - region) * (255.0 - over) / 255.0
        base[y:y + h, x:x + w] = blended
        return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


class ImageOverlay:
    """A still image laid **over** the picture for a window, as a panel.

    Built for the proof-of-stake short, where the user's note was that the
    opening shot has empty space above the footage and the site's own
    architecture diagram should sit in it. Everything else in this format
    either *is* the shot or replaces it; this is the one way to have a diagram
    and moving footage at the same time, which is what a vertical frame has the
    room for and a landscape one does not.

    **Composited opaque, not screen-blended**, which is the opposite of
    `ClipOverlay`'s choice and for a good reason. A screen blend leaves pure
    black transparent, which is perfect for a glowing button on black — but a
    diagram's background is a dark *grey*, not black, so screen-blending one
    lifts the footage underneath it by that grey everywhere the diagram sits
    and prints a visible washed rectangle. An opaque panel with the brand's
    own hairline reads as a deliberate inset instead.

    `at` is the top-left in pixels; `None` centres horizontally and sits the
    panel in the upper third, which is where a 9:16 frame has room. `scale` is
    a fraction of frame width.
    """

    def __init__(self, path: Path, start: float, end: float,
                 frame: Frame = LANDSCAPE, scale: float = 0.92,
                 at: tuple[int, int] | None = None, fade: float = 0.35,
                 rule: bool = True):
        self.start, self.end, self.fade = start, end, fade
        self.frame = frame

        im = Image.open(path).convert("RGB")
        w = int(frame.w * scale)
        h = max(1, int(round(im.height * w / im.width)))
        self.im = im.resize((w, h), Image.LANCZOS)
        if rule:
            d = ImageDraw.Draw(self.im)
            d.rectangle([0, 0, w - 1, h - 1], outline=(229, 194, 0), width=3)
        if at is None:
            at = ((frame.w - w) // 2, int(frame.h * 0.16))
        self.at = at

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return pic
        # Ramp in and out so the panel arrives rather than snapping.
        a = min(1.0, (t - self.start) / self.fade) if self.fade else 1.0
        a = min(a, max(0.0, (self.end - t) / self.fade) if self.fade else 1.0)
        if a <= 0:
            return pic
        if a >= 1.0:
            pic.paste(self.im, self.at)
            return pic
        base = pic.crop((self.at[0], self.at[1],
                         self.at[0] + self.im.width, self.at[1] + self.im.height))
        pic.paste(Image.blend(base, self.im, a), self.at)
        return pic
