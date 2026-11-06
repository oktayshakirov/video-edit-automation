"""`behind` - one word set between a photograph's room and its subject.

The subject is cut out (`core.vision.matte`, or the alpha of a cutout PNG),
the hole they leave in the room is filled, and the word ends up set between
the two layers: the head crosses the word instead of the word sitting on the
picture. A slow push moves the subject a little faster than the word and the
word a little faster than the room, so the three read as depth.

**It gets there through a phase where the whole word is read.** The word
flies in from the camera in front of the subject, holds there (`READ`), then
recedes behind the subject, which steps forward over it (`TUCK`). A beat
that only ever showed the word behind the head showed "ETH..EUM" from first
frame to last (2026-11-05).

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

payload: (image, word, line="", entry="fly", room=None, cut=True) - `image`
is a photo (cut out by the model) or an RGBA PNG (its alpha used as given).
`line`, if set, is a second reveal: a band label in front of everything, low
in the frame.

**`cut=False`: no cutout, the word stays on top** (2026-11-06). The editor on
the random-tokens Ledger: "Use the original image without the cutout effect
and the same big yellow font saying offline on top of it ... the hands dont
work that well." A matte round fingers holding a small device is ragged, and
the depth trick is worth nothing if its edge shows. With `cut=False` the
photograph is shown whole, only lightly dimmed (`PLAIN_DIM`), no model runs,
and the word flies in exactly as before, settles to its size and never
tucks. Use it whenever the subject is hands, hair against a busy room, or
anything the matte frays on.
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
    """payload: (image, word, line="", entry="fly", room=None)."""

    # Most of the word's ink the subject may hide. Measured, not guessed: the
    # prototype frame that read well ("ETH..EUM" behind Buterin's hair) hid
    # 0.37; at 0.30 the search could only clear it across his mouth.
    MAX_COVER = 0.38
    MIN_COVER = 0.04        # ...and the least, or it is not behind anything
    # A height where the subject hides this little is taken before any other,
    # however low: the word then reads almost whole even once it is behind.
    LIGHT_COVER = 0.20
    PUSH = (0.030, 0.050, 0.085)    # room, word, subject: zoom over the beat
    ROOM_DIM = 0.62

    # **The word is read whole before the subject covers it** (the editor's
    # note on the first Mac demo, 2026-11-05: ETHEREUM sat behind Buterin's
    # face for the whole beat and was never once on screen entire). It flies
    # in from the camera *in front of* the subject, settles and holds with
    # every letter showing, then recedes past the subject, which steps
    # forward over it. The depth order is the motion: bigger and in front,
    # then smaller and behind.
    ARRIVE = 0.45           # s: from the camera to its reading size, in front
    READ = 0.80             # s: settled in front, the whole word on screen
    TUCK = 0.50             # s: receding behind the subject
    FLY_FROM = 1.35         # the word's scale as it arrives, fading in
    FRONT = 1.08            # its scale while read - capped to fit the frame
    STEP = 0.03             # how far the subject comes forward as it passes
    SWAP = (0.35, 0.30)     # the depth order flips over this share of the tuck

    # **`entry="rise"`: the word is there first, the subject comes up into
    # it.** The editor's second version (2026-11-05): the word lands on the
    # empty room, is read whole, then the subject rises from below the frame
    # and settles in front of it. Same three phases; the subject moves
    # instead of the word.
    ENTRIES = ("fly", "rise")
    RISE_IN = 0.70          # s: the subject from below the frame to its place
    LAND = 0.10             # the word's small upward drift as it lands (x size)

    PLAIN_DIM = 0.88        # `cut=False`: the photo whole, a touch darker for the word

    def __init__(self, image, word, line="", entry="fly", room=None, cut=True,
                 **kw):
        if entry not in self.ENTRIES:
            raise ValueError(f"behind: entry={entry!r}, not one of {self.ENTRIES}")
        if not cut and (entry != "fly" or room is not None):
            raise ValueError("behind: cut=False has no subject to rise or to "
                             "stand in front of a room= - use entry='fly'")
        self.entry, self.cut = entry, bool(cut)
        super().__init__(**kw)
        self.word, self.line = word.upper(), line
        key = (str(image), Path(image).stat().st_mtime_ns, self.frame.size,
               self.cut)
        if key not in _LAYERS:
            _LAYERS.clear()             # one picture at a time is plenty
            _LAYERS[key] = self._layers(image)
        self.person, self.room, alpha, self.ox, self.oy = _LAYERS[key]
        # **`room=`: a different picture behind the subject.** The filled hole
        # is never perfect - the subject leaves traces, and `entry="rise"`
        # shows the room empty for over a second, so the blurred silhouette
        # read (the editor's call, 2026-11-05). A separate background, sized
        # to the subject's layer and stepped back the same way, has no hole.
        if room is not None:
            self.room = self._backdrop(room, self.person.shape[1],
                                       self.person.shape[0])
        elif entry == "rise":
            print(f"  ! behind rise on {Path(image).name} without room= - the "
                  f"filled hole may show the subject's traces (beats.md)")
        rows = np.nonzero((alpha > 0.5).any(axis=1))[0]
        # The subject's top edge on screen - where a rise has to start under.
        self.subject_top = float(rows[0] + self.oy) if len(rows) else 0.0
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
        if not self.cut:
            # No subject: the whole picture is the room, nothing goes in front.
            alpha = np.zeros(rgb.shape[:2], np.float32)
        elif alpha is None:
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
        if not self.cut:
            room = (rgb.astype(np.float32) * self.PLAIN_DIM).astype(np.uint8)
            return person, room, alpha, ox, oy
        return person, self._room(rgb, alpha), alpha, ox, oy

    def _backdrop(self, path, sw, sh):
        """A separate room picture covering the subject layer's size, softened
        and dimmed exactly as the filled room is."""
        src = vision.as_rgb(Image.open(path))
        ih, iw = src.shape[:2]
        k = max(sw / iw, sh / ih)
        rgb = cv2.resize(src, (max(sw, int(round(iw * k))), max(sh, int(round(ih * k)))),
                         interpolation=cv2.INTER_AREA)
        y0, x0 = (rgb.shape[0] - sh) // 2, (rgb.shape[1] - sw) // 2
        rgb = rgb[y0:y0 + sh, x0:x0 + sw]
        room = cv2.GaussianBlur(rgb.astype(np.float32), (0, 0), max(1.0, sw * 0.004))
        return (room * self.ROOM_DIM).astype(np.uint8)

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
        # **Filled from the surroundings' colours, not streaked in from the
        # edges.** Telea dragged the hole's rim inward, which nobody saw while
        # the subject stood in front of it - but `entry="rise"` shows the
        # empty room first, and Saylor's hole read as a dark blob filling a
        # 9:16 frame (2026-11-05). A normalised blur gives each hole pixel the
        # weighted mean of the room around it: a smooth wash of the place.
        # Mostly sideways: a room is horizontal bands (wall, stage, desk), and
        # a round blur pulled Saylor's lit podium up into the dark wall as a
        # pale mound. The seam is feathered so no outline of the subject stays.
        keep = (sh_hole == 0).astype(np.float32)
        sx = max(4.0, small.shape[1] * 0.12)
        sy = max(2.0, small.shape[0] * 0.012)
        num = cv2.GaussianBlur(small.astype(np.float32) * keep[:, :, None],
                               (0, 0), sigmaX=sx, sigmaY=sy)
        den = cv2.GaussianBlur(keep, (0, 0), sigmaX=sx, sigmaY=sy)[:, :, None]
        # Where a row is nearly all subject, fall back to the room around it
        # in every direction - still never the subject's own pixels (a wide
        # plain blur pulled Buterin's shirt into the floor of the hole).
        num2 = cv2.GaussianBlur(small.astype(np.float32) * keep[:, :, None], (0, 0), sx * 2)
        den2 = cv2.GaussianBlur(keep, (0, 0), sx * 2)[:, :, None]
        wide = num2 / np.maximum(den2, 1e-3)
        wash = np.where(den > 0.02, num / np.maximum(den, 1e-3), wide)
        wash = cv2.GaussianBlur(wash, (0, 0), sy * 1.5)
        soft = cv2.GaussianBlur((sh_hole > 0).astype(np.float32), (0, 0),
                                max(2.0, small.shape[1] * 0.012))[:, :, None]
        # Fully the wash inside the hole (no subject pixel may leak back in),
        # fading out only beyond its edge.
        soft = np.maximum(soft, (sh_hole > 0)[:, :, None].astype(np.float32))
        filled = np.clip(wash * soft + small * (1.0 - soft), 0, 255).astype(np.uint8)
        soft_full = cv2.resize(soft[:, :, 0], (sw, sh), interpolation=cv2.INTER_LINEAR)
        filled = cv2.resize(filled, (sw, sh), interpolation=cv2.INTER_CUBIC)
        # The feathered mask, not the hard one: the hard edge here threw the
        # feather away and left the subject's outline cut into the room.
        k = np.maximum(soft_full, (hole > 0).astype(np.float32))[:, :, None]
        room = (filled.astype(np.float32) * k + rgb.astype(np.float32) * (1 - k))
        # Defocused more than a plain backdrop would need: the fill is a smooth
        # wash on a patterned wall, and only depth of field hides the patch
        # while `entry="rise"` shows the room empty.
        room = cv2.GaussianBlur(room, (0, 0), max(1.0, sw * 0.004))
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
            # The highest *light* position first - the subject crosses the
            # word but hides at most `LIGHT_COVER` of it. Then the highest
            # readable one: across the top of the head, never the mouth (the
            # first build aimed at a cover figure and found the face).
            # Failing both, the least-covered position anywhere.
            light = self.MIN_COVER <= cover <= self.LIGHT_COVER
            ok = self.MIN_COVER <= cover <= self.MAX_COVER
            score = (0, y) if light else (1, y) if ok else (2, cover)
            if best is None or score < best[0]:
                best = (score, y, cover)
        y = best[1] if best else int(lo)
        self.cover = best[2] if best else 0.0
        layer, _ = self._word_layer(size, y)
        self.ink_h = ink_h
        # Where the ink sits, for the fly-in: it scales about its own centre,
        # and while it is read in front it must fit the frame whole.
        cols = np.nonzero(ink.any(axis=0))[0]
        ink_w = float(cols[-1] - cols[0] + 1) if len(cols) else float(W)
        self.ink_cy = y + (r0 + r1) / 2.0
        self.front = max(1.0, min(self.FRONT,
                                  0.94 * W / (ink_w * (1.0 + self.PUSH[1]))))
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

    def _phases(self) -> tuple[float, float]:
        """When the word arrives, and when it starts to recede (beat clock).

        The tuck starts after the full read, but never so late that it is
        still moving when the beat ends: on a short beat the read shortens,
        never the arrival.
        """
        r0 = self._reveal(0, 0.06)
        end = self.start + self.hold
        ts = min(r0 + self.ARRIVE + self.READ, end - self._move() - 0.3)
        return r0, max(r0 + self.ARRIVE, ts)

    def _move(self) -> float:
        """How long the third phase takes: the word's tuck or the rise."""
        return self.RISE_IN if self.entry == "rise" else self.TUCK

    def _word_affine(self, s: float, zw: float):
        """Scale `s` about the word's own centre, then the beat's push."""
        cx, cy = self.frame.w / 2.0, self.ink_cy
        a = np.array([[s, 0, (1 - s) * cx], [0, s, (1 - s) * cy], [0, 0, 1]])
        b = np.vstack([self._zoom(zw), [0, 0, 1]])
        return (b @ a)[:2].astype(np.float32)

    def _over(self, base, rgba, fade=1.0):
        a = rgba[:, :, 3:4].astype(np.float32) * (fade / 255.0)
        return base * (1.0 - a) + rgba[:, :, :3] * a

    def draw(self, f: float) -> Image.Image:
        W, H = self.frame.size
        t = self.at(f)
        e = _smooth(f)
        zr, zw, zp = (1.0 + p * e for p in self.PUSH)

        def placed(layer, z, dx=0.0, dy=0.0):
            m = self._zoom(z)
            m[0, 2] += m[0, 0] * self.ox + dx
            m[1, 2] += m[1, 1] * self.oy + dy
            border = cv2.BORDER_REFLECT if layer.shape[2] == 3 else cv2.BORDER_CONSTANT
            return cv2.warpAffine(layer, m, (W, H), flags=cv2.INTER_LINEAR,
                                  borderMode=border)

        room = placed(self.room, zr, -W * 0.006 * e).astype(np.float32)
        r0, ts = self._phases()
        if self.entry == "rise":
            out = self._draw_rise(room, t, r0, ts, zw, zp, placed, e)
            return self._with_label(out, t)
        k = min(1.0, max(0.0, (t - ts) / self.TUCK))
        tuck = _smooth(k)
        # The depth order swaps quickly, in the middle of the recede: over
        # the whole tuck the letters sat half-through the face like a double
        # exposure (first Mac render, 2026-11-05). The motion carries the swap.
        swap = _smooth(min(1.0, max(0.0, (k - self.SWAP[0]) / self.SWAP[1])))
        person = placed(self.person, zp * (1.0 + self.STEP * tuck), W * 0.005 * e)

        if t < r0:
            out = self._over(room, person)
        else:
            arrive = ease_out(min(1.0, (t - r0) / self.ARRIVE))
            fade = _smooth(min(1.0, (t - r0) / (self.ARRIVE * 0.7)))
            if arrive < 1.0:
                s = self.FLY_FROM + (self.front - self.FLY_FROM) * arrive
            else:
                s = self.front + (1.0 - self.front) * tuck
            word = cv2.warpAffine(self.text, self._word_affine(s, zw), (W, H),
                                  flags=cv2.INTER_LINEAR)
            # In front until the tuck, behind after it; during it the two
            # orders cross-fade, which only differs where word and subject
            # overlap - the letters dissolve into the subject as it passes.
            front = (self._over(self._over(room, person), word, fade)
                     if swap < 1.0 else None)
            behind = (self._over(self._over(room, word, fade), person)
                      if swap > 0.0 else None)
            if front is None:
                out = behind
            elif behind is None:
                out = front
            else:
                out = front * (1.0 - swap) + behind * swap
        return self._with_label(out, t)

    def _draw_rise(self, room, t, r0, ts, zw, zp, placed, e):
        """`entry="rise"`: the word lands on the empty room and is read whole,
        then the subject comes up from below the frame in front of it."""
        W, H = self.frame.size
        out = room
        if t >= r0:
            arrive = ease_out(min(1.0, (t - r0) / self.ARRIVE))
            fade = _smooth(min(1.0, (t - r0) / (self.ARRIVE * 0.7)))
            word = cv2.warpAffine(self.text, self._word_affine(1.0, zw), (W, H),
                                  flags=cv2.INTER_LINEAR)
            if arrive < 1.0:
                drop = self.size * self.LAND * (1.0 - arrive)
                word = cv2.warpAffine(word, np.float32([[1, 0, 0], [0, 1, drop]]),
                                      (W, H), flags=cv2.INTER_LINEAR)
            out = self._over(out, word, fade)
        k = min(1.0, max(0.0, (t - ts) / self.RISE_IN))
        if k > 0.0:
            # From just below the frame: the head's top starts under the
            # bottom edge, so nothing of the subject shows before the rise.
            # The push zooms about the frame's centre, which lifts the top.
            top = max(0.0, H / 2 + (self.subject_top - H / 2) * zp)
            travel = (H - top + H * 0.02) * (1.0 - ease_out(k))
            out = self._over(out, placed(self.person, zp, W * 0.005 * e, travel))
        return out

    def _with_label(self, out, t):
        W, H = self.frame.size
        img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
        if self.label is not None:
            q = ease_out(min(1.0, max(0.0, (t - self._reveal(1, 0.45)) / 0.35)))
            if q > 0:
                lab = self.label.copy()
                lab.putalpha(lab.getchannel("A").point(lambda v: int(v * q)))
                y = int(H * (0.80 if self.portrait else 0.84) + (1 - q) * 18)
                img.paste(lab, ((W - lab.width) // 2, y), lab)
        return img
