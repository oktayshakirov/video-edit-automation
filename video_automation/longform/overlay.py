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
from PIL import Image, ImageDraw, ImageFilter

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


# --------------------------------------------------------------------------
# The title sequence
# --------------------------------------------------------------------------

FONT_TITLE = "/System/Library/Fonts/SFNS.ttf"     # SF Pro, variable


def _sf(size: int, weight: str = "Bold") -> "ImageFont.FreeTypeFont":
    """SF Pro at a weight. Futura is the caption face; this is the display one.

    The title used to be set in Futura Medium at 96px, centred on a hard scrim
    band. Futura is a light, wide geometric: it is right for a caption sitting
    over footage and weak as a display face, which is most of why that
    treatment read as dated. SF Pro carries a real Heavy, and a heavy grotesque
    left-aligned is the current look on every channel that spends money on
    titles.
    """
    from PIL import ImageFont
    f = ImageFont.truetype(FONT_TITLE, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:                       # a static build, or an old Pillow
        pass
    return f


def _tracked(d: "ImageDraw.ImageDraw", xy: tuple[float, float], text: str,
             font, fill, track: float) -> float:
    """Draw `text` with letter spacing, returning the width it took.

    PIL has no tracking. An eyebrow label set without it is just small type;
    set with it, it reads as a label, which is the whole job of the line.
    """
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x - xy[0] - (track if text else 0)


class TitleOverlay:
    """The video's own title, as an animated lower third over the opening shot.

    **This replaces the centred statement the title stamp used to borrow.**
    That treatment is `Shot(payload=)`: a 96px line centred inside a flat black
    band across the middle third of the frame. It is the right device for *a
    statement the footage illustrates* — "This is not financial advice" over
    rain on a window — and the wrong one for a title, for three reasons the
    user named on the noise-canceling cut: the hard-edged band is a rectangle
    of black sitting on top of the picture rather than part of it, centred caps
    in a light geometric is the visual language of a 2012 slideshow, and
    nothing moves, so the one moment the video says what it is has no more
    weight than a caption.

    What this draws instead, and every part of it is doing a job:

    * **A gradient scrim, not a band.** Alpha ramps from nothing at 55% height
      to near-opaque at the bottom edge, so there is no line where the
      treatment starts. Footage stays footage; the type still reads over a
      bright frame.
    * **Bottom-left, not centred.** A left-aligned lower third is where a
      viewer's eye already expects a name to appear, and it leaves the middle
      of the frame — where the footage's own subject is — alone.
    * **An accent bar in the brand's own colour**, growing top to bottom before
      the words arrive. It is the only element that is pure brand, and it is
      what makes the tinnitus cut and the crypto cut read as the same channel
      family without either one borrowing the other's palette.
    * **The lines rise into view behind a mask**, staggered. Each line is drawn
      into a box exactly its own height and slid up into it, so the glyphs are
      cut off by the box's edge on the way in. That is the reveal every motion
      package sells and it costs one `Image.new` per line per frame.
    * **It leaves.** The block fades and drifts up over the last half second
      rather than cutting, so the shot it sits on carries on cleanly.

    Timing is in absolute seconds against the finished timeline, same as every
    other overlay here. `hold` is the whole window including both ramps.
    """

    LEAD = 0.34             # scrim and accent bar, before any type
    STAGGER = 0.10          # between one title line and the next
    RISE = 0.50             # one line's own reveal
    OUT = 0.55              # the exit ramp

    def __init__(self, title: str, start: float, hold: float, brand,
                 frame: Frame = LANDSCAPE, eyebrow: str | None = None,
                 y_frac: float = 0.86, max_lines: int = 3):
        from ..core.draw import wrap

        self.start, self.end = start, start + hold
        self.brand, self.frame = brand, frame
        self.eyebrow = (eyebrow if eyebrow is not None
                        else (brand.site or brand.name)).upper()

        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        self.margin = int(round(frame.w * 0.072))
        self.bar_w = max(4, int(round(frame.w * 0.0045)))
        self.gap = int(round(frame.w * 0.024))
        col = int(frame.w * (0.60 if frame.w >= frame.h else 0.74))

        # Fit the title: the largest size that still wraps inside `max_lines`.
        # A title is one to six words and almost always fits at the top of the
        # range; the search exists so a long one degrades by getting smaller
        # rather than by running off the frame.
        hi = int(frame.w * 0.058)
        lo = int(frame.w * 0.028)
        size, lines = lo, [title]
        for s in range(hi, lo - 1, -2):
            f = _sf(s, "Bold")
            ls = wrap(probe, title, f, col)
            if len(ls) <= max_lines:
                size, lines = s, ls
                break
        self.size, self.lines = size, lines
        self.font = _sf(size, "Bold")
        self.line_h = int(round(size * 1.16))
        self.eb_font = _sf(max(15, int(round(size * 0.26))), "Semibold")
        self.eb_track = max(1.0, size * 0.045)
        self.eb_h = int(round(size * 0.52))

        block_h = self.line_h * len(lines) + self.eb_h
        self.block_bottom = int(frame.h * y_frac)
        self.block_top = self.block_bottom - block_h
        self.text_x = self.margin + self.bar_w + self.gap
        self.col = col

        # The scrim is one image, built once. Its alpha is scaled per frame.
        top = int(frame.h * 0.45)
        ramp = np.zeros((frame.h, 1), np.float32)
        span = max(1, frame.h - top)
        k = np.linspace(0.0, 1.0, span, dtype=np.float32)
        ramp[top:, 0] = k * k * 210.0
        self.scrim = np.repeat(ramp, frame.w, axis=1)

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return pic
        e = t - self.start
        life = self.end - self.start

        # One global ramp for the exit: everything fades and drifts up
        # together, so the block reads as one object leaving rather than as
        # five elements each ending on their own clock.
        out_p = max(0.0, (e - (life - self.OUT)) / self.OUT)
        a_all = 1.0 - out_p * out_p
        if a_all <= 0.004:
            return pic
        drift = int(round(-18 * out_p * out_p))

        from ..core.draw import ease_out

        base = np.asarray(pic).astype(np.float32)
        s = (self.scrim * a_all)[:, :, None] / 255.0
        base *= (1.0 - s)
        pic = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))

        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)

        # The bar grows downward, and it is first — the brand arrives before
        # the sentence does.
        bp = ease_out(min(1.0, e / self.LEAD))
        if bp > 0.01:
            y0 = self.block_top + drift
            y1 = y0 + int((self.block_bottom - self.block_top) * bp)
            r = self.bar_w / 2
            d.rounded_rectangle([self.margin, y0, self.margin + self.bar_w, y1],
                                radius=r, fill=(*self.brand.primary, 255))

        # The eyebrow slides in from the bar, a beat after it.
        ep = ease_out(max(0.0, min(1.0, (e - 0.18) / 0.42)))
        if ep > 0.01 and self.eyebrow:
            ex = self.text_x - int(round(16 * (1.0 - ep)))
            ey = self.block_top + drift + int(round(self.eb_h * 0.12))
            _tracked(d, (ex, ey), self.eyebrow, self.eb_font,
                     (*self.brand.primary, int(255 * ep)), self.eb_track)

        for i, ln in enumerate(self.lines):
            lp = ease_out(max(0.0, min(1.0, (e - (self.LEAD + i * self.STAGGER))
                                       / self.RISE)))
            if lp <= 0.01:
                continue
            # The slot is exactly one line tall, and the type starts below it.
            # Anything still below the slot's own edge is simply not drawn —
            # which is the mask, without a mask image.
            slot = Image.new("RGBA", (self.col + self.size, self.line_h),
                             (0, 0, 0, 0))
            sd = ImageDraw.Draw(slot)
            off = int(round(self.line_h * 0.92 * (1.0 - lp)))
            sd.text((0, off - int(self.size * 0.06)), ln, font=self.font,
                    fill=(255, 255, 255, 255))
            if lp < 1.0 or a_all < 1.0:
                al = slot.getchannel("A").point(
                    lambda v: int(v * lp * a_all))
                slot.putalpha(al)
            y = self.block_top + self.eb_h + i * self.line_h + drift
            layer.alpha_composite(slot, (self.text_x, y))

        # A soft drop shadow under the whole block, from the block's own alpha.
        sh = layer.getchannel("A").filter(ImageFilter.GaussianBlur(9))
        shadow = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        shadow.putalpha(sh.point(lambda v: int(v * 0.55)))
        out = pic.convert("RGBA")
        out.alpha_composite(shadow, (0, 5))
        out.alpha_composite(layer)
        return out.convert("RGB")
