"""`behind` - one word set between a photograph's room and its subject.

The subject is cut out (`core.vision.matte`, or the alpha of a cutout PNG),
the hole they leave in the room is filled, and the word is set between the
two layers: the head crosses the word instead of the word sitting on the
picture. A slow push moves the subject a little faster than the word and the
word a little faster than the room, so the three read as depth.

Built 2026-11-05 from the prototype on Vitalik Buterin's TechCrunch portrait
("ETHEREUM" behind his head). Use it where a person or an object *is* the
subject of the line - the name of the thing they made, the stake, the one
word the chapter turns on. A face over a room, not a crowd.

**The word is placed, not typed where the script guessed.** Its height is
searched: the head should cover part of it - that is the effect - but never
more than `MAX_COVER` of its ink, or the word stops being readable. The
search runs from under the watermark down and keeps the *highest* position
where the subject covers between `MIN_COVER` and `MAX_COVER`, which puts the
word across the top of the head; a subject so large that every position
hides too much gets the least-covered one.

payload: (image, word, line="") - `image` is a photo (cut out by the model)
or an RGBA PNG (its alpha used as given). `line`, if set, is a second reveal:
a band label in front of everything, low in the frame.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ...core import vision
from ...core.draw import ease_out
from .base import Beat, _smooth

FONT_WORD = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
_LAYERS: dict = {}


class Behind(Beat):
    """payload: (image, word, line="")."""

    RISE = 0.55             # the word's arrival
    # Most of the word's ink the subject may hide. Measured, not guessed: the
    # prototype frame that read well ("ETH..EUM" behind Buterin's hair) hid
    # 0.37; at 0.30 the search could only clear it across his mouth.
    MAX_COVER = 0.38
    MIN_COVER = 0.04        # ...and the least, or it is not behind anything
    PUSH = (0.030, 0.050, 0.085)    # room, word, subject: zoom over the beat
    ROOM_DIM = 0.62

    def __init__(self, image, word, line="", **kw):
        super().__init__(**kw)
        self.word, self.line = word.upper(), line
        key = (str(image), Path(image).stat().st_mtime_ns, self.frame.size)
        if key not in _LAYERS:
            _LAYERS.clear()             # one picture at a time is plenty
            _LAYERS[key] = self._layers(image)
        self.person, self.room, alpha, self.ox, self.oy = _LAYERS[key]
        self.text, self.text_y = self._place_word(alpha)
        self.label = self._label(line) if line else None

    # --- the layers ---------------------------------------------------------

    def _layers(self, image):
        """Subject, room and placement for this picture at this frame size.

        Memoised per process (`_LAYERS`): the room fill is the slow part, and
        a beat is built more than once for the same picture - a preview, a
        portrait and a landscape cut of one line, the tests.
        """
        W, H = self.frame.size
        pil = Image.open(image)
        alpha = vision.alpha_of(pil)
        rgb = vision.as_rgb(pil)
        if alpha is None:
            alpha = vision.matte(rgb)

        # Cover the frame with headroom for the push, the subject centred
        # across it: a landscape photo in 9:16 keeps the person, not the
        # middle of the room.
        ih, iw = rgb.shape[:2]
        k = max(W / iw, H / ih) * 1.10
        sw, sh = int(round(iw * k)), int(round(ih * k))
        rgb = cv2.resize(rgb, (sw, sh), interpolation=cv2.INTER_AREA)
        alpha = cv2.resize(alpha, (sw, sh), interpolation=cv2.INTER_LINEAR)
        cols = np.nonzero((alpha > 0.5).any(axis=0))[0]
        cx = (cols[0] + cols[-1]) / 2 if len(cols) else sw / 2
        ox = float(np.clip(W / 2 - cx, W - sw, 0))
        oy = float((H - sh) / 2)
        person = np.dstack([rgb, (alpha * 255).astype(np.uint8)])
        return person, self._room(rgb, alpha), alpha, ox, oy

    def _room(self, rgb, alpha):
        """The picture without its subject: the hole filled, then stepped back.

        Inpainted at ~480px wide - the room is softened and dimmed anyway,
        and Telea on a full-size hole costs seconds for no visible gain.
        """
        sh, sw = alpha.shape
        hole = (alpha > 0.06).astype(np.uint8)
        grow = max(3, int(sw * 0.018)) | 1
        hole = cv2.dilate(hole, np.ones((grow, grow), np.uint8))
        q = max(1, sw // 480)
        small = cv2.resize(rgb, (sw // q, sh // q), interpolation=cv2.INTER_AREA)
        sh_hole = cv2.resize(hole, (sw // q, sh // q),
                             interpolation=cv2.INTER_NEAREST) * 255
        filled = cv2.inpaint(small, sh_hole, max(3, 36 // q), cv2.INPAINT_TELEA)
        filled = cv2.GaussianBlur(filled, (0, 0), 2.0)
        filled = cv2.resize(filled, (sw, sh), interpolation=cv2.INTER_CUBIC)
        room = np.where(hole[:, :, None] > 0, filled, rgb)
        room = cv2.GaussianBlur(room, (0, 0), max(1.0, sw * 0.0015))
        return (room.astype(np.float32) * self.ROOM_DIM).astype(np.uint8)

    def _font(self, size):
        return ImageFont.truetype(FONT_WORD, size)

    def _word_layer(self, size, y):
        """The word at `size`, top at `y`, on a frame-sized RGBA layer."""
        W, H = self.frame.size
        f = self._font(size)
        track = size * 0.02
        widths = [f.getlength(c) for c in self.word]
        tw = sum(widths) + track * (len(self.word) - 1)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ds, d = ImageDraw.Draw(shadow), ImageDraw.Draw(layer)
        x = (W - tw) / 2
        for c, cw in zip(self.word, widths):
            ds.text((x, y + size * 0.03), c, font=f, fill=(0, 0, 0, 175))
            d.text((x, y), c, font=f, fill=(*self.brand.primary, 255))
            x += cw + track
        shadow = shadow.filter(ImageFilter.GaussianBlur(max(2, size * 0.06)))
        shadow.alpha_composite(layer)
        return shadow, layer

    def _place_word(self, alpha):
        """Size the word to the frame, then search its height (see module)."""
        W, H = self.frame.size
        size = int(H * (0.17 if self.portrait else 0.34))
        f = self._font(size)
        while sum(f.getlength(c) for c in self.word) * 1.02 > W * 0.92 and size > 24:
            size = int(size * 0.94)
            f = self._font(size)
        self.size = size

        # The subject as it sits on screen at the start of the beat.
        m = np.float32([[1, 0, self.ox], [0, 1, self.oy]])
        on = cv2.warpAffine(alpha, m, (W, H), flags=cv2.INTER_LINEAR) > 0.5

        bb = f.getbbox(self.word)
        ink_h = bb[3] - bb[1]
        lo, hi = self.head_y - bb[1], int(H * 0.62) - bb[3]
        # The glyphs once, at y=0: every candidate height is the same mask
        # slid down, so the search is array slicing, not ~45 full renders.
        _, glyphs = self._word_layer(size, 0)
        ink = np.asarray(glyphs.getchannel("A")) > 128
        rows = np.nonzero(ink.any(axis=1))[0]
        r0, r1 = (int(rows[0]), int(rows[-1]) + 1) if len(rows) else (0, 1)
        ink = ink[r0:r1]
        n = int(ink.sum())
        best = None
        for y in range(int(lo), max(int(lo) + 1, int(hi)), max(4, size // 24)):
            a, b = y + r0, y + r1
            if n == 0 or a < 0 or b > H:
                continue
            cover = float((ink & on[a:b]).sum()) / n
            # The highest readable position where the subject actually
            # crosses the word: across the top of the head, never the mouth
            # (the first build aimed at a cover figure and found the face).
            # Failing that, the least-covered position anywhere.
            ok = self.MIN_COVER <= cover <= self.MAX_COVER
            score = (0, y) if ok else (1, cover)
            if best is None or score < best[0]:
                best = (score, y, cover)
        y = best[1] if best else int(lo)
        self.cover = best[2] if best else 0.0
        layer, _ = self._word_layer(size, y)
        self.ink_h = ink_h
        return np.asarray(layer), y

    def _label(self, text):
        """The band label: brand band, band ink, tracked caps - `spotlight`'s."""
        W, H = self.frame.size
        text = text.upper()
        size = int(W * (0.050 if self.portrait else 0.030))
        while True:             # shrink to fit: a label never leaves the frame
            f = self._font(size)
            track = f.size * 0.12
            tw = sum(f.getlength(c) for c in text) + track * (len(text) - 1)
            if tw + f.size * 1.1 <= W * 0.90 or size <= 18:
                break
            size = int(size * 0.92)
        bb = f.getbbox("H")
        cap = bb[3] - bb[1]
        pw, ph = int(tw + f.size * 1.1), int(cap + f.size * 0.75)
        im = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        fill = self.brand.band or self.brand.primary
        d.rounded_rectangle([0, 0, pw - 1, ph - 1], radius=int(ph * 0.22),
                            fill=(*fill, 255))
        x = (pw - tw) / 2
        for c in text:
            d.text((x, (ph - cap) / 2 - bb[1]), c, font=f,
                   fill=(*self.brand.band_ink, 255))
            x += f.getlength(c) + track
        return im

    # --- drawing ------------------------------------------------------------

    def _reveal(self, i: int, default: float) -> float:
        rv = list(self.reveals or [])
        return rv[i] if i < len(rv) else self.start + default * self.hold

    def _zoom(self, z: float):
        """Zoom by `z` about the frame's centre, as an affine on frame coords."""
        W, H = self.frame.size
        return np.float32([[z, 0, (1 - z) * W / 2], [0, z, (1 - z) * H / 2]])

    def _over(self, base, rgba, fade=1.0):
        a = rgba[:, :, 3:4].astype(np.float32) * (fade / 255.0)
        return base * (1.0 - a) + rgba[:, :, :3] * a

    def draw(self, f: float) -> Image.Image:
        W, H = self.frame.size
        t = self.at(f)
        e = _smooth(f)
        zr, zw, zp = (1.0 + p * e for p in self.PUSH)

        def placed(layer, z, dx=0.0):
            m = self._zoom(z)
            m[0, 2] += m[0, 0] * self.ox + dx
            m[1, 2] += m[1, 1] * self.oy
            border = cv2.BORDER_REFLECT if layer.shape[2] == 3 else cv2.BORDER_CONSTANT
            return cv2.warpAffine(layer, m, (W, H), flags=cv2.INTER_LINEAR,
                                  borderMode=border)

        out = placed(self.room, zr, -W * 0.006 * e).astype(np.float32)

        p = ease_out(min(1.0, max(0.0, (t - self._reveal(0, 0.06)) / self.RISE)))
        if p > 0:
            word = cv2.warpAffine(self.text, self._zoom(zw), (W, H),
                                  flags=cv2.INTER_LINEAR)
            if p < 1.0:
                rise = self.size * 0.08 * (1.0 - p)
                word = cv2.warpAffine(word, np.float32([[1, 0, 0], [0, 1, rise]]),
                                      (W, H), flags=cv2.INTER_LINEAR)
            out = self._over(out, word, p)

        out = self._over(out, placed(self.person, zp, W * 0.005 * e))
        img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

        if self.label is not None:
            q = ease_out(min(1.0, max(0.0, (t - self._reveal(1, 0.45)) / 0.35)))
            if q > 0:
                lab = self.label.copy()
                lab.putalpha(lab.getchannel("A").point(lambda v: int(v * q)))
                y = int(H * (0.80 if self.portrait else 0.84) + (1 - q) * 18)
                img.paste(lab, ((W - lab.width) // 2, y), lab)
        return img
