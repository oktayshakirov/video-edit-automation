"""`spotlight` - zoom into part of a photograph, one detail per sentence.

A still usually gets a slow, generic Ken Burns. This directs it (the editor's
pick after a demo, 2026-10-23): the camera starts on the whole picture,
glides into the part the voice is talking about, dims everything else under
a soft spotlight and rings the detail in the brand colour with a band-style
label - then moves to the next detail, and can pull back out at the end.

**The ring is snapped to the content, never drawn where the script guessed.**
The demo's charges box was typed by hand and cut through a line of text that
ran on past it; the editor's note was that this must not happen. `snap()`
finds what the given region actually covers - the ink that differs from the
picture's plain ground, letters joined into lines - and fits the box to it,
widening the search until a line that runs off the edge is whole. On a
photograph with no plain ground (a face, a street) it leaves the region as
given, because there is no "content" to find there.

payload: (image, regions, title) - `regions` is one entry per reveal:
((x0, y0, x1, y1) as fractions of the image, label), or (None, "") to frame
the whole picture (to open on it, or to pull back out at the end).
"""

from __future__ import annotations

import math

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ...core.draw import cover, ease_out
from .base import Beat, _smooth

FONT_LABEL = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"


def snap(src: np.ndarray, region, max_iter: int = 10):
    """Fit `region` (fractions) to the content it covers; fractions back.

    The ground is the median colour of the search area's border. Ink is any
    pixel well away from it; a dilation joins letters into words and lines
    into a paragraph, and every joined block the region touches is kept. If
    the kept blocks reach the search area's edge, the area grows and the
    search runs again, so a line is never cut where the script's box ended.
    """
    ih, iw = src.shape[:2]
    rx0, ry0, rx1, ry1 = (region[0] * iw, region[1] * ih,
                          region[2] * iw, region[3] * ih)
    box = (rx0, ry0, rx1, ry1)
    # Wide horizontally, so letters join into words and words into a line:
    # at 1.2% the "V" and "A" of a kerned word joined only at their tips -
    # wide top against wide bottom - and the box ended mid-word. Narrow
    # vertically, so a paragraph's lines join but a separate line does not.
    kx = max(3, int(iw * 0.03)) | 1
    ky = max(3, int(ih * 0.012)) | 1
    for _ in range(max_iter):
        bx0, by0, bx1, by1 = box
        px = 0.30 * (bx1 - bx0) + 0.03 * iw
        py = 0.40 * (by1 - by0) + 0.015 * ih
        cx0, cy0 = max(0, int(bx0 - px)), max(0, int(by0 - py))
        cx1, cy1 = min(iw, int(bx1 + px)), min(ih, int(by1 + py))
        crop = src[cy0:cy1, cx0:cx1].astype(np.int16)
        if crop.size == 0:
            break
        edge = np.concatenate([crop[0], crop[-1], crop[:, 0], crop[:, -1]])
        ground = np.median(edge, axis=0)
        ink = (np.abs(crop - ground).max(axis=2) > 48).astype(np.uint8)
        if ink.mean() > 0.55:
            return region                   # no plain ground: a photograph
        joined = cv2.dilate(ink, np.ones((ky, kx), np.uint8))
        n, lab, stats, _ = cv2.connectedComponentsWithStats(joined)
        keep = np.zeros_like(ink, bool)
        for i in range(1, n):
            x, y, w, h, _a = stats[i]
            ox = max(0, min(x + w, rx1 - cx0) - max(x, rx0 - cx0))
            oy = max(0, min(y + h, ry1 - cy0) - max(y, ry0 - cy0))
            if ox * oy > 0:
                keep |= lab == i
        ys, xs = np.nonzero(keep & (ink > 0))
        if len(xs) == 0:
            return region
        nb = (cx0 + xs.min(), cy0 + ys.min(), cx0 + xs.max() + 1,
              cy0 + ys.max() + 1)
        hit = keep.any(axis=0)
        hity = keep.any(axis=1)
        grows = ((hit[0] and cx0 > 0) or (hit[-1] and cx1 < iw)
                 or (hity[0] and cy0 > 0) or (hity[-1] and cy1 < ih))
        box = nb
        if not grows:
            break
    return (box[0] / iw, box[1] / ih, box[2] / iw, box[3] / ih)


class Spotlight(Beat):
    """payload: (image, regions, title). `regions` is a list of
    ((x0, y0, x1, y1) as fractions of the image, label) - or (None, "") to
    pull back to the whole picture. One region per reveal."""

    MOVE = 0.85             # one glide between framings
    FILL = 0.80             # how much of the frame a region takes, at most
    DIM = 0.72              # how dark the spotlight makes the rest

    def __init__(self, image, regions, title="", **kw):
        super().__init__(**kw)
        src = Image.open(image).convert("RGB")
        self.src = np.asarray(src)
        self.regions = [(snap(self.src, tuple(r)) if r else None, lab)
                        for r, lab in regions]
        self.title = title
        self.ih, self.iw = self.src.shape[:2]
        W, H = self.frame.size
        # Behind the picture: itself, covered, blurred and dark - so a
        # picture that does not fill the frame sits on its own colours.
        back = cover(src, W, H).filter(ImageFilter.GaussianBlur(40))
        self.back = (np.asarray(back) * 0.30).astype(np.uint8)
        self.font = ImageFont.truetype(
            FONT_LABEL, int(W * (0.050 if self.portrait else 0.030)))

    # --- the camera -------------------------------------------------------

    def _framing(self, region):
        """(centre x, centre y, scale) in image pixels / screen px per px."""
        W, H = self.frame.size
        if region is None:
            s = min(W / self.iw, H / self.ih) * 0.94
            return self.iw / 2, self.ih / 2, s
        x0, y0, x1, y1 = region
        rw, rh = (x1 - x0) * self.iw, (y1 - y0) * self.ih
        s = min(W * self.FILL / rw, H * self.FILL / rh)
        # Never closer than 2.6x the source: past that a still turns to mush.
        s = min(s, 2.6)
        return (x0 + x1) / 2 * self.iw, (y0 + y1) / 2 * self.ih, s

    def _times(self):
        rv = list(self.reveals or [])
        n = len(self.regions)
        return [rv[i] if i < len(rv) else
                self.start + self.hold * (0.15 + 0.8 * i / max(n, 1))
                for i in range(n)]

    def camera(self, t):
        """(cx, cy, scale, focus region or None, focus strength 0..1)."""
        cx, cy, s = self._framing(None)
        focus, strength = None, 0.0
        since = t - self.start
        for r, ti in zip(self.regions, self._times()):
            p = _smooth((t - ti + 0.05) / self.MOVE)
            if p <= 0:
                break
            since = t - ti
            tx, ty, ts = self._framing(r[0])
            # Interpolate scale in log space, so a zoom feels even.
            cx, cy = cx + (tx - cx) * p, cy + (ty - cy) * p
            s = math.exp(math.log(s) + (math.log(ts) - math.log(s)) * p)
            if r[0] is None:
                strength *= 1.0 - p
            else:
                focus, strength = r, p
        # A slow push while it holds keeps the still alive - restarted at
        # every move, or the final pull-back ends too tight and crops.
        s *= 1.0 + 0.012 * max(0.0, since)
        return cx, cy, s, focus, strength

    # --- drawing ----------------------------------------------------------

    def _label(self, d, text, x, y):
        f = self.font
        track = f.size * 0.12
        text = text.upper()
        tw = sum(d.textlength(c, font=f) for c in text) + track * (len(text) - 1)
        bb = d.textbbox((0, 0), "H", font=f)
        cap = bb[3] - bb[1]
        pw, ph = tw + f.size * 1.1, cap + f.size * 0.75
        fill = self.brand.band or self.brand.primary
        d.rounded_rectangle([x, y, x + pw, y + ph], radius=int(ph * 0.22),
                            fill=(*fill, 255))
        cx = x + (pw - tw) / 2
        for c in text:
            d.text((cx, y + (ph - cap) / 2 - bb[1]), c, font=f,
                   fill=(*self.brand.band_ink, 255))
            cx += d.textlength(c, font=f) + track

    def content(self, out, f):
        W, H = self.frame.size
        t = self.at(f)
        cx, cy, s, focus, strength = self.camera(t)
        m = np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]])
        pic = cv2.warpAffine(self.src, m, (W, H), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT,
                             borderValue=(0, 0, 0))
        inside = cv2.warpAffine(np.full((self.ih, self.iw), 255, np.uint8),
                                m, (W, H), flags=cv2.INTER_LINEAR)
        a = (inside.astype(np.float32) / 255.0)[:, :, None]
        frame = pic * a + self.back * (1.0 - a)

        if focus is not None and strength > 0.01:
            (x0, y0, x1, y1), label = focus
            # The region in screen pixels, with a little air.
            sx0 = W / 2 + (x0 * self.iw - cx) * s
            sy0 = H / 2 + (y0 * self.ih - cy) * s
            sx1 = W / 2 + (x1 * self.iw - cx) * s
            sy1 = H / 2 + (y1 * self.ih - cy) * s
            pad = W * 0.012
            q = 4
            mask = Image.new("L", (W // q, H // q), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                [(sx0 - pad) / q, (sy0 - pad) / q, (sx1 + pad) / q,
                 (sy1 + pad) / q], radius=W * 0.01 / q, fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(W * 0.012 / q))
            mask = np.asarray(mask.resize((W, H), Image.BILINEAR),
                              np.float32)[:, :, None] / 255.0
            frame = frame * (1.0 - self.DIM * strength * (1.0 - mask))

            img = Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8))
            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            d = ImageDraw.Draw(layer)
            ring = ease_out(min(1.0, strength * 1.3))
            grow = (1.0 - ring) * W * 0.02
            col = (*self.brand.primary, int(255 * ring))
            d.rounded_rectangle([sx0 - pad - grow, sy0 - pad - grow,
                                 sx1 + pad + grow, sy1 + pad + grow],
                                radius=int(W * 0.01), outline=col,
                                width=max(3, int(W / 480)))
            if label and strength > 0.6:
                ly = sy1 + pad + W * 0.012
                if ly > H * 0.86:                   # no room under: go above
                    ly = sy0 - pad - W * 0.012 - self.font.size * 1.2
                self._label(d, label, sx0 - pad, ly)
            img = img.convert("RGBA")
            img.alpha_composite(layer)
            out.paste(img.convert("RGB"))
        else:
            out.paste(Image.fromarray(np.clip(frame, 0, 255).astype(np.uint8)))
        if self.title:
            self.heading(out, self.title, f)


