"""The shared scaffolding every beat is built on.

`Beat` handles the background, the picture column, the reveal clock and
the heading, so a new beat is a layout decision rather than a rendering
one. The constants and the private helpers here are the vocabulary the
families share - the two fonts, the rounded-corner path, the watermark
clearance - and they live at the bottom of the package so no family
module has to import from another.
"""

from __future__ import annotations

import math
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ...core import backdrop
from ...core.brand import Brand
from ...core.draw import contain, cover, ease_out, subpixel
from ...core.frame import LANDSCAPE, Frame
from ...core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

DRAW = 0.16                     # how long a mark or a strike takes to draw on
POP = 0.14                      # an item's entrance
RISE = 14                       # px an item travels on its way in


def _smooth(p: float) -> float:
    """Smoothstep — eased at both ends, so a long slow draw neither jumps off
    the mark nor stalls into the target. `ease_out` is right for a fast pop
    and wrong for a line travelling for a second and a half against the
    voice."""
    p = min(1.0, max(0.0, p))
    return p * p * (3.0 - 2.0 * p)


def _unit(a: tuple, b: tuple) -> tuple:
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1.0
    return dx / L, dy / L


def _round_corners(pts: list, r: float, seg: int = 7) -> list:
    """Fillet every interior vertex of a polyline with a quadratic curve of
    radius ~`r`, so `partial` draws rounded bends instead of hard mitres — a
    feedback arrow with square corners reads as a stray underline, not a
    loop."""
    if len(pts) < 3:
        return [tuple(p) for p in pts]
    out = [tuple(pts[0])]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        u1, u2 = _unit(b, a), _unit(b, c)
        d = min(r, math.dist(a, b) * 0.5, math.dist(b, c) * 0.5)
        p1 = (b[0] + u1[0] * d, b[1] + u1[1] * d)
        p2 = (b[0] + u2[0] * d, b[1] + u2[1] * d)
        out.append(p1)
        for s in range(1, seg):
            tt = s / seg
            out.append((
                (1 - tt) ** 2 * p1[0] + 2 * (1 - tt) * tt * b[0] + tt ** 2 * p2[0],
                (1 - tt) ** 2 * p1[1] + 2 * (1 - tt) * tt * b[1] + tt ** 2 * p2[1]))
        out.append(p2)
    out.append(tuple(pts[-1]))
    return out


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)


# The thumbnail's display face, so a chapter card and the thumbnail of the same
# video are set in one voice. Imported by path rather than from `thumb` to keep
# the beats module free of a dependency on the thumbnail renderer.
FONT_DISPLAY = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def _display(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_DISPLAY, size)


@lru_cache(maxsize=8)
def _mark_bottom(name: str, width: int, top: int) -> int:
    """Where the watermark ends, so a kicker can clear it.

    **This cannot be a constant.** thecrypto.wiki's mark is a wide, short
    wordmark; tinnitushelp.me's is a mascot with the domain under it and is
    four times taller at the same width. A kicker at a fixed y=214 cleared
    the first and landed inside the second — the wordmark and the beat's
    heading printed over each other.
    """
    from ...core.brand import BRANDS
    mark = BRANDS[name].mark(width)
    return top + (mark.height if mark is not None else 0)


class Beat:
    """Base for every drawn beat: a background, two columns, and timing.

    Subclasses implement `content(d, out, f, t)` and draw into the left column
    using `self.col`. The background, the picture column, the drifting grid and
    the reveal clock are all handled here so a new beat is a layout decision
    rather than a rendering one.
    """

    MARGIN = 100
    COL_W = 1000                # content column width at 1920
    PIC_X = 1160                # picture column left edge
    PIC_W = 660
    PIC_H = 760

    def __init__(self, brand: Brand, frame: Frame = LANDSCAPE,
                 backdrop: Path | None = None, picture: Path | None = None,
                 reveals: list[float] | None = None,
                 marks: list[float] | None = None,
                 start: float = 0.0, hold: float = 1.0):
        self.brand, self.frame = brand, frame
        self.reveals, self.marks = reveals, marks
        self.start, self.hold = start, hold
        self.head_y = _mark_bottom(brand.name,
                                   int(frame.logo_w * brand.mark_scale),
                                   frame.logo_at[1]) + 46

        # Scale the column geometry if the frame is not the 1920 reference.
        k = frame.w / 1920
        # **Portrait is not landscape scaled down.** `MARGIN * k` is 56px on a
        # 1080-wide frame, which is tighter than anything else in the vertical
        # format — `ChecklistShot` sets its items from x=200. A margin is about
        # the edge of a phone screen, not about a fraction of the design width.
        self.portrait = frame.h > frame.w
        self.margin = 96 if self.portrait else int(self.MARGIN * k)
        self.col = (self.margin, int(self.COL_W * k))
        self.pic_box = (int(self.PIC_X * k), int(self.PIC_W * k),
                        int(self.PIC_H * frame.h / 1080))

        self.back = None
        if backdrop is not None and Path(backdrop).exists():
            # Prepared with headroom, so the backdrop can drift. In the shorts
            # this layer was static and a drifting grid supplied the motion;
            # here the grid is gone (see `background`) and the photograph moves
            # instead, which is both better motion and one less thing drawn.
            pad = 120
            im = cover(Image.open(backdrop).convert("RGB"),
                       frame.w + pad, frame.h + pad)
            im = im.filter(ImageFilter.GaussianBlur(30))
            # 0.42, not 0.3. Measured on real frames while building the shorts:
            # 0.3 was indistinguishable from flat black, which is the thing a
            # photographic backdrop exists to avoid. Brighter than the shorts'
            # 0.5 is wrong in the other direction — at 1920 a bright backdrop
            # competes with type that has twice as much of it to hold up.
            self.back = (np.asarray(im) * 0.42).astype(np.uint8)

        # The picture column, prepared once with headroom for a slow drift.
        self.pic = None
        if picture is not None and Path(picture).exists():
            pw, ph = self.pic_box[1], self.pic_box[2]
            src = Image.open(picture).convert("RGB")
            fitted = contain(src, int(pw * 1.10), int(ph * 1.10))
            # If the source was too small to fill the column even at 1:1, take
            # the column down to the picture rather than stretching it up.
            self.pic_w = min(pw, fitted.width)
            self.pic_h = min(ph, fitted.height)
            self.pic = np.asarray(fitted)

    # --- timing ---------------------------------------------------------

    def at(self, f: float) -> float:
        """Absolute time at `f`, which is what `reveals` and `marks` are in."""
        return self.start + f * self.hold

    def due(self, i: int, n: int, f: float) -> float:
        """How far item `i` has entered, 0..1. Falls back to even spacing."""
        t = self.at(f)
        when = (self.reveals[i] if self.reveals and i < len(self.reveals)
                else self.start + self.hold * (i / max(n, 1)) * 0.85)
        return ease_out((t - when) / POP) if t >= when else -1.0

    def marked(self, i: int, f: float) -> float:
        """How far item `i`'s verdict has drawn on, 0..1, or -1 if not due."""
        if not self.marks or i >= len(self.marks):
            return -1.0
        t = self.at(f)
        return ease_out((t - self.marks[i]) / DRAW) if t >= self.marks[i] else -1.0

    def span_p(self, i: int, f: float, *, lead: float = 0.12,
               cap: float = 2.0, tail: float = 0.06) -> float:
        """Progress 0..1 of an element that draws *across* the phrase that
        reveals item `i`.

        It starts `lead` seconds after item `i`'s caption begins and travels
        the whole way to item `i+1`'s caption (or the shot's end), capped at
        `cap` so a long scripted pause does not leave it crawling. This is the
        clock for a line or an arrow that has to track the voice — a fixed
        fast pop reads as movement detached from what is being said, which was
        the note on the first diagram cut. Smoothstepped, so a draw lasting a
        second and a half neither jumps nor stalls.
        """
        rv = self.reveals or []
        src = rv[i] if i < len(rv) else self.start
        nxt = rv[i + 1] if i + 1 < len(rv) else self.start + self.hold
        span = nxt - src
        if span <= 0.08:                    # reveals collapsed to one time
            dur, t0 = 0.44, src
        else:
            dur = min(cap, max(0.5, span - lead - tail))
            t0 = src + lead
        return _smooth((self.at(f) - t0) / dur) if self.at(f) >= t0 else 0.0

    def open_p(self, f: float, dur: float = 1.0) -> float:
        """Progress 0..1 of the beat's opening gesture — the scaffolding a beat
        draws before its items populate it: a comparison's dividing rule, a
        sequence's track. Anchored at the shot's start and smoothstepped, so it
        matches the voice-synced item draws instead of snapping in a quick
        `ease_out` while everything else glides."""
        return _smooth((self.at(f) - self.start) / dur)

    def _head(self, d: ImageDraw.ImageDraw, a: tuple, b: tuple,
              colour: tuple | None = None, s: int = 23) -> None:
        """An arrowhead at `b`, pointing away from `a` — drawn from a polygon
        so it can cap a line that `partial` has already travelled, or stand
        alone at the end of a rounded path. Shared by `diagram` and
        `callout`."""
        col = colour or self.brand.primary
        vx, vy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(vx, vy) or 1.0
        ux, uy = vx / L, vy / L
        d.polygon([b, (b[0] - ux * s - uy * s * 0.62,
                       b[1] - uy * s + ux * s * 0.62),
                   (b[0] - ux * s + uy * s * 0.62,
                    b[1] - uy * s - ux * s * 0.62)],
                  fill=col)

    # --- painting -------------------------------------------------------

    def background(self, f: float) -> Image.Image:
        """A drifting photograph, or the brand's own moving background.

        **The drifting grid this used to draw is gone.** It stepped a whole
        pixel at a time (`int((f * 40) % 96)` on a layer moving 40 px/s), which
        is the judder every other moving element in this repo was fixed for
        years ago, and it was worst on exactly the long beats where the eye has
        time to lock onto a ruled line. It was also the same graph paper behind
        every beat of every video on both channels.

        `core.backdrop` replaces it with a looping asset per brand — a
        generated purple mesh gradient for tinnitushelp.me, black water for
        thecrypto.wiki. See that module for why they are square and why they
        are sampled by timeline seconds rather than by `f`.

        The flat `brand.bg` panel remains the fallback, so a brand with no
        background declared still renders.
        """
        fr = self.frame
        if self.back is not None:
            # Opposed to nothing in particular, just slow — the type is the
            # subject here and a backdrop that pulls the eye is a bug.
            bx = (self.back.shape[1] - fr.w) * (0.5 + 0.34 * (f - 0.5))
            by = (self.back.shape[0] - fr.h) * (0.5 - 0.34 * (f - 0.5))
            return Image.fromarray(subpixel(self.back, bx, by, fr.w, fr.h))

        bg = backdrop.get(self.brand.backdrop)
        if bg is not None:
            # **Timeline seconds, not `f`.** Sampling by beat progress would
            # run the whole loop inside every beat, so the background would
            # change speed at every cut.
            return Image.fromarray(bg.at(self.at(f), fr.w, fr.h))

        return Image.new("RGB", fr.size, self.brand.bg)

    def emblem(self, out: Image.Image, f: float) -> None:
        """Concentric arcs in the picture column, slowly counter-rotating.

        Beats with a photograph get one; beats without had a dead right half —
        on a 16:9 frame that is 40% of the picture showing nothing, which the
        user flagged on the outro stat. This is deliberately abstract: it is
        there to balance the composition and give the eye something moving, not
        to mean anything. Low contrast, so it never competes with the number.
        """
        x0, w, h = self.pic_box
        cx, cy = x0 + w // 2, self.frame.h // 2
        d = ImageDraw.Draw(out, "RGBA")
        r0 = min(w, h) // 2
        for i, (rf, span, speed, alpha) in enumerate(
                ((1.00, 250, 1.0, 46), (0.78, 190, -1.4, 62),
                 (0.56, 300, 0.7, 52), (0.34, 140, -2.0, 78))):
            r = int(r0 * rf)
            a0 = (f * 34 * speed + i * 61) % 360
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + span,
                  fill=self.brand.primary + (alpha,), width=5)
        # A filled dot at the centre, so the rings read as a system rather than
        # as four unrelated curves.
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11],
                  fill=self.brand.primary + (150,))

    def paint_picture(self, out: Image.Image, f: float) -> None:
        """The right-hand column: the post's own photograph, drifting slowly."""
        if self.pic is None:
            return
        x0, _, _ = self.pic_box
        w, h = self.pic_w, self.pic_h
        # Drift within the headroom prepared in __init__, subpixel as always.
        sx = max(0.0, (self.pic.shape[1] - w) * (0.35 + 0.30 * f))
        sy = max(0.0, (self.pic.shape[0] - h) * (0.65 - 0.30 * f))
        crop = Image.fromarray(subpixel(self.pic, sx, sy, w, h))

        y0 = (self.frame.h - h) // 2
        out.paste(crop, (x0, y0))
        # The same hairline the photo shots use, and for the same reason: it
        # reads as deliberate framing rather than as an image that failed to
        # fill its space.
        d = ImageDraw.Draw(out)
        d.rectangle([x0, y0, x0 + w, y0 + h], outline=self.brand.primary, width=3)

    def heading(self, out: Image.Image, text: str, f: float = 1.0,
                y: int | None = None) -> int:
        """The beat's kicker, in the brand accent. Returns the y below it.

        **y=214, not 176.** The watermark sits upper-left at y=62 and a 34px
        kicker at 176 read as the second line of the logo lockup rather than as
        the beat's own heading — the two stacked into one block. Clearing the
        mark properly costs nothing; the content below is centred anyway.
        """
        y = self.head_y if y is None else y
        if not text:
            return y
        d = ImageDraw.Draw(out)
        d.text((self.col[0], y), text.upper(), font=_font(34),
               fill=self.brand.primary)
        # The rule draws across as the beat opens, so even a beat whose content
        # arrives slowly has something moving in its first half second.
        e = ease_out(min(1.0, (self.at(f) - self.start) / 0.45))
        d.line([(self.col[0], y + 54), (self.col[0] + int(220 * e), y + 54)],
               fill=self.brand.primary, width=3)
        return y + 96

    def content(self, out: Image.Image, f: float) -> None:
        raise NotImplementedError

    # Beats that fill the right column with an abstract emblem when they have
    # no photograph. A checklist or a comparison already spans the frame; a
    # stat or a quote is a short block on the left and nothing on the right.
    EMBLEM = False

    def draw(self, f: float) -> Image.Image:
        out = self.background(f)
        if self.pic is not None:
            self.paint_picture(out, f)
        elif self.EMBLEM:
            self.emblem(out, f)
        self.content(out, f)
        return out


def _hex(s: str) -> tuple[int, int, int]:
    """`"#f85032"` -> `(248, 80, 50)`. Bands are quoted from the source site."""
    t = s.lstrip("#")
    return tuple(int(t[i:i + 2], 16) for i in (0, 2, 4))


