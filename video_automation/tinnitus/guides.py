"""Breathing guides other than the ring, for sound-therapy sessions (E13).

Every session up to 2026-11-03 drew one guide: the ring that grows on the
inhale and shrinks on the exhale. Breathing channels that stand out on
YouTube draw the breath as a *shape the eye can read ahead*: a dot riding a
line that rises and falls, a dot tracing a square, a hand sweeping a dial.
The shape shows what is coming next, which a ring cannot - a ring only shows
now. Which guide keeps a viewer breathing longer is what E13 tests.

Three styles live here, chosen with `guide=` on `render_loop`,
`render_bookend`, `render_asmr_long`, `render_visual` and
`render_asmr_short`. `"ring"` keeps the original code path untouched, so
every shipped session renders exactly as before.

* **`path`** - a line scrolls right to left under a fixed dot. Each cycle is
  one rise (inhale), a flat top (hold), one fall (exhale) and a flat bottom
  (rest), with widths in proportion to the seconds, so 4-7-8 draws a short
  climb, a long plateau and a long descent. Each side carries its own
  "INHALE 4" label, so the pattern can be read before it is breathed.
* **`box`** - a square with one side per phase; the dot travels round it.
  Needs all four phases (box breathing, 6-6-6-6), and raises otherwise.
* **`clock`** - a dial cut into sectors in proportion to the seconds, with
  a hand that sweeps once per breath. The active sector lights up.

**Every guide is periodic in the breath**, so a loop that is a whole number
of cycles (which `render_loop` already enforces) closes without a jump.

The look is ours: the session's own tint, the ring's glow, our type. The
mechanics (a dot on a path, a dial) are generic breathing aids, not any one
channel's design.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

STYLES = ("ring", "path", "box", "clock")

# What the viewer reads. The rest after the exhale is a hold too.
WORD = {"inhale": "inhale", "hold": "hold", "exhale": "exhale", "rest": "hold"}
SS = 2          # supersampling for anything drawn once and reused


@dataclass(frozen=True)
class Pattern:
    """One breath: seconds of inhale, hold, exhale and the rest after it."""
    inhale: float
    hold: float
    exhale: float
    rest: float = 0.0

    @property
    def phases(self) -> list[tuple[str, float]]:
        return [(k, d) for k, d in (("inhale", self.inhale), ("hold", self.hold),
                                    ("exhale", self.exhale), ("rest", self.rest))
                if d > 0]

    @property
    def cycle(self) -> float:
        return self.inhale + self.hold + self.exhale + self.rest

    def at(self, t: float) -> tuple[int, str, float, float]:
        """Phase index, kind, fraction through it and seconds left, at `t`.

        `t` may be negative (an intro runs up to zero); `%` keeps it periodic.
        """
        p = t % self.cycle
        for i, (kind, d) in enumerate(self.phases):
            if p < d:
                return i, kind, p / d, d - p
            p -= d
        kind, d = self.phases[-1]
        return len(self.phases) - 1, kind, 1.0, 0.0


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)


def _text(draw: ImageDraw.ImageDraw, text: str, cx: float, y: float,
          font: ImageFont.FreeTypeFont, fill=(255, 255, 255, 235)) -> None:
    """Centred on `cx`, top at `y`, like the ring's own type."""
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    draw.text((cx - (x1 - x0) / 2 - x0, y - y0), text, font=font, fill=fill)


def _side_label(text: str, size: int, angle: float) -> Image.Image:
    """A segment's "INHALE 4", rotated to lie along it.

    White with a soft dark stroke: unlike the ring's count, these sit on the
    line and cross whatever the look draws behind it.
    """
    font = _font(size)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    x0, y0, x1, y1 = probe.textbbox((0, 0), text, font=font, stroke_width=3)
    im = Image.new("RGBA", (x1 - x0 + 8, y1 - y0 + 8), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((4 - x0, 4 - y0), text, font=font,
                            fill=(255, 255, 255, 235), stroke_width=3,
                            stroke_fill=(0, 0, 0, 90))
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)


def _paste_centred(dst: Image.Image, im: Image.Image, x: float, y: float) -> None:
    dst.alpha_composite(im, (int(round(x - im.width / 2)),
                             int(round(y - im.height / 2))))


def _dot(r: int, tint: tuple) -> Image.Image:
    """The rider: a solid disc in the tint with the ring's glow round it."""
    s = r * 2 + 60
    c = s / 2
    glow = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse([c - r, c - r, c + r, c + r],
                                 fill=tint + (200,))
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    core = Image.new("RGBA", (s * SS, s * SS), (0, 0, 0, 0))
    ImageDraw.Draw(core).ellipse([(c - r) * SS, (c - r) * SS,
                                  (c + r) * SS, (c + r) * SS],
                                 fill=tint + (255,),
                                 outline=(255, 255, 255, 230), width=3 * SS)
    glow.alpha_composite(core.resize((s, s), Image.LANCZOS))
    return glow


def _glow_line(size: tuple[int, int], points: list, tint: tuple,
               width: int, closed: bool = False) -> Image.Image:
    """A line with the ring's rim glow, drawn at `SS`x and brought down once."""
    w, h = size
    pts = [(x * SS, y * SS) for x, y in points]
    if closed:
        pts.append(pts[0])
    glow = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(glow).line(pts, fill=tint + (150,), width=width * 3 * SS,
                              joint="curve")
    glow = glow.filter(ImageFilter.GaussianBlur(9 * SS))
    core = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    ImageDraw.Draw(core).line(pts, fill=tint + (255,), width=width * SS,
                              joint="curve")
    glow.alpha_composite(core)
    return glow.resize((w, h), Image.LANCZOS)


def _fade(im: Image.Image, alpha: float) -> Image.Image:
    if alpha >= 0.999:
        return im
    out = im.copy()
    out.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    return out


class Guide:
    """Draws the breath at `t` onto an RGBA frame. Subclasses lay it out."""

    def __init__(self, w: int, h: int, pattern: Pattern, tint: tuple):
        self.w, self.h, self.pattern, self.tint = w, h, pattern, tuple(tint)
        self.portrait = h > w
        self.cx, self.cy = w // 2, h // 2

    def draw(self, img: Image.Image, t: float, alpha: float = 1.0) -> None:
        """Composite the guide at `t`. `alpha` < 1 fades it (entrances)."""
        if alpha <= 0.004:
            return
        if alpha >= 0.999:
            self._draw(img, t)
            return
        layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
        self._draw(layer, t)
        img.alpha_composite(_fade(layer, alpha))

    def _draw(self, img: Image.Image, t: float) -> None:
        raise NotImplementedError

    def _count(self, left: float) -> str:
        # Seconds remaining, rounded up: a 4s phase counts 4, 3, 2, 1.
        return str(max(1, math.ceil(left - 1e-6)))


class PathGuide(Guide):
    """A line that rises and falls, scrolling under a fixed dot."""

    def __init__(self, w, h, pattern, tint):
        super().__init__(w, h, pattern, tint)
        p = self.portrait
        self.cycle_w = int(w * (0.92 if p else 0.78))
        self.dot_x = int(w * (0.30 if p else 0.40))
        amp = 220 if p else 160
        mid = self.cy + (0 if p else 50)
        self.yt, self.yb = mid - amp, mid + amp
        margin = 110
        self.top = self.yt - margin
        band_h = self.yb - self.yt + 2 * margin
        # Two cycles to the left of the window's start, and enough after it to
        # cover the frame - the crop moves through the first cycle only.
        k = 3 + math.ceil((w - self.dot_x) / self.cycle_w)
        pts, segs = [], []
        x = 0.0
        y_of = {"inhale": (self.yb, self.yt), "hold": (self.yt, self.yt),
                "exhale": (self.yt, self.yb), "rest": (self.yb, self.yb)}
        for _ in range(k):
            for kind, d in pattern.phases:
                x1 = x + self.cycle_w * d / pattern.cycle
                y0, y1 = (v - self.top for v in y_of[kind])
                if not pts:
                    pts.append((x, y0))
                pts.append((x1, y1))
                segs.append((kind, d, x, y0, x1, y1))
                x = x1
        self.strip = _glow_line((int(x) + 2, band_h), pts, self.tint, 7)
        size = 40 if p else 38
        for kind, d, x0, y0, x1, y1 in segs:
            dx, dy = x1 - x0, y1 - y0
            ln = math.hypot(dx, dy)
            nx, ny = dy / ln, -dx / ln            # one normal of the segment
            if ny > 0:
                nx, ny = -nx, -ny                 # the one pointing up
            label = _side_label(f"{WORD[kind].upper()} {d:g}", size,
                                -math.degrees(math.atan2(dy, dx)))
            _paste_centred(self.strip, label, (x0 + x1) / 2 + nx * 40,
                           (y0 + y1) / 2 + ny * 40)
        self.dot = _dot(26 if p else 24, self.tint)
        self.word_font, self.count_font = _font(52), _font(96)
        self.word_y = self.top - (250 if p else 200)

    def _draw(self, img, t):
        pat = self.pattern
        i, kind, f, left = pat.at(t)
        p = (t % pat.cycle) / pat.cycle * self.cycle_w
        off = self.cycle_w + p - self.dot_x
        band = self.strip.transform((self.w, self.strip.height), Image.AFFINE,
                                    (1, 0, off, 0, 1, 0),
                                    resample=Image.BILINEAR)
        img.alpha_composite(band, (0, self.top))
        y = {"inhale": self.yb + (self.yt - self.yb) * f,
             "hold": self.yt,
             "exhale": self.yt + (self.yb - self.yt) * f,
             "rest": self.yb}[kind]
        _paste_centred(img, self.dot, self.dot_x, y)
        d = ImageDraw.Draw(img)
        _text(d, WORD[kind], self.cx, self.word_y, self.word_font)
        _text(d, self._count(left), self.cx, self.word_y + 66, self.count_font)


class BoxGuide(Guide):
    """A square, one side per phase; the dot goes round it once a breath."""

    def __init__(self, w, h, pattern, tint):
        super().__init__(w, h, pattern, tint)
        if len(pattern.phases) != 4:
            raise ValueError(
                "guide='box' needs four phases (inhale, hold, exhale, rest), "
                f"got {[k for k, _ in pattern.phases]}")
        side = 720 if self.portrait else 560
        cx, cy = self.cx, self.cy + (60 if self.portrait else 10)
        l, r_, t_, b = cx - side / 2, cx + side / 2, cy - side / 2, cy + side / 2
        # Up the left side on the inhale, across the top on the hold, down the
        # right on the exhale, back along the bottom on the rest.
        self.corners = [(l, b), (l, t_), (r_, t_), (r_, b)]
        self.static = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.static.alpha_composite(
            _glow_line((w, h), self.corners, self.tint, 7, closed=True))
        size = 42 if self.portrait else 40
        for (kind, d), (a, z), ang, (nx, ny) in zip(
                pattern.phases,
                zip(self.corners, self.corners[1:] + self.corners[:1]),
                (90, 0, -90, 0), ((-1, 0), (0, -1), (1, 0), (0, 1))):
            label = _side_label(f"{WORD[kind].upper()} {d:g}", size, ang)
            _paste_centred(self.static, label, (a[0] + z[0]) / 2 + nx * 50,
                           (a[1] + z[1]) / 2 + ny * 50)
        self.dot = _dot(26, self.tint)
        self.word_font, self.count_font = _font(56), _font(150)
        self.box_cy = cy

    def _draw(self, img, t):
        i, kind, f, left = self.pattern.at(t)
        img.alpha_composite(self.static)
        (x0, y0), (x1, y1) = self.corners[i], self.corners[(i + 1) % 4]
        _paste_centred(img, self.dot, x0 + (x1 - x0) * f, y0 + (y1 - y0) * f)
        d = ImageDraw.Draw(img)
        _text(d, WORD[kind], self.cx, self.box_cy - 120, self.word_font)
        _text(d, self._count(left), self.cx, self.box_cy - 40, self.count_font)


class ClockGuide(Guide):
    """A dial in sectors sized by the seconds, and a hand that sweeps it."""

    def __init__(self, w, h, pattern, tint):
        super().__init__(w, h, pattern, tint)
        p = self.portrait
        self.R = R = 430 if p else 370
        self.dc = (self.cx, self.cy + 150) if p else (self.cx + 230, self.cy)
        self.word_at = (self.cx, self.cy - 610) if p else (self.cx - 520,
                                                           self.cy - 130)
        s = 2 * R + 40
        self.dials = [self._dial(R, s, active) for active in
                      range(len(pattern.phases))]
        hand = Image.new("RGBA", (s * SS, s * SS), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hand)
        c = s * SS / 2
        hd.line([(c, c), (c, c - R * 0.84 * SS)], fill=(255, 255, 255, 240),
                width=12 * SS)
        hd.ellipse([c - 6 * SS, c - R * 0.84 * SS - 6 * SS,
                    c + 6 * SS, c - R * 0.84 * SS + 6 * SS],
                   fill=(255, 255, 255, 240))
        hd.ellipse([c - 20 * SS, c - 20 * SS, c + 20 * SS, c + 20 * SS],
                   fill=(255, 255, 255, 245))
        self.hand = hand.resize((s, s), Image.LANCZOS)
        self.word_font, self.count_font = _font(64), _font(150)

    def _dial(self, R: int, s: int, active: int) -> Image.Image:
        pat = self.pattern
        im = Image.new("RGBA", (s * SS, s * SS), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        c = s * SS / 2
        box = [c - R * SS, c - R * SS, c + R * SS, c + R * SS]
        # A dark face first, so the sector tints read on a bright look too.
        d.ellipse(box, fill=(0, 0, 0, 70))
        a = -90.0
        bounds = []
        for i, (kind, dur) in enumerate(pat.phases):
            sweep = 360.0 * dur / pat.cycle
            d.pieslice(box, a, a + sweep,
                       fill=self.tint + ((120,) if i == active else (34,)))
            bounds.append(a)
            a += sweep
        for sec in range(int(round(pat.cycle))):
            ang = math.radians(-90 + 360 * sec / pat.cycle)
            r0 = R * (0.90 if any(abs(math.radians(b) - ang) < 1e-6
                                  for b in bounds) else 0.95)
            d.line([(c + math.cos(ang) * r0 * SS, c + math.sin(ang) * r0 * SS),
                    (c + math.cos(ang) * R * SS, c + math.sin(ang) * R * SS)],
                   fill=(255, 255, 255, 170), width=3 * SS)
        for b in bounds:
            ang = math.radians(b)
            d.line([(c, c), (c + math.cos(ang) * R * SS,
                             c + math.sin(ang) * R * SS)],
                   fill=(255, 255, 255, 90), width=2 * SS)
        im = im.resize((s, s), Image.LANCZOS)
        rim = _glow_line((s, s), [(s / 2 + math.cos(math.radians(k)) * R,
                                   s / 2 + math.sin(math.radians(k)) * R)
                                  for k in range(0, 360, 2)],
                         self.tint, 6, closed=True)
        im.alpha_composite(rim)
        # Sector labels in sentence case, at mid-angle, two-thirds out.
        a = -90.0
        font = _font(44 if self.portrait else 40)
        ld = ImageDraw.Draw(im)
        for kind, dur in pat.phases:
            sweep = 360.0 * dur / pat.cycle
            m = math.radians(a + sweep / 2)
            _text(ld, f"{WORD[kind].capitalize()} {dur:g}",
                  s / 2 + math.cos(m) * R * 0.6,
                  s / 2 + math.sin(m) * R * 0.6 - 20, font)
            a += sweep
        return im

    def _draw(self, img, t):
        pat = self.pattern
        i, kind, f, left = pat.at(t)
        dial = self.dials[i]
        _paste_centred(img, dial, *self.dc)
        deg = 360.0 * (t % pat.cycle) / pat.cycle
        hand = self.hand.rotate(-deg, resample=Image.BICUBIC)
        _paste_centred(img, hand, *self.dc)
        d = ImageDraw.Draw(img)
        x, y = self.word_at
        _text(d, WORD[kind], x, y, self.word_font)
        _text(d, self._count(left), x, y + 84, self.count_font)


def make(style: str, w: int, h: int, pattern: Pattern,
         tint: tuple) -> Guide | None:
    """The guide for `style`, or None for the ring (the callers' own code)."""
    if style not in STYLES:
        raise ValueError(f"guide must be one of {STYLES}, got {style!r}")
    if style == "ring":
        return None
    return {"path": PathGuide, "box": BoxGuide, "clock": ClockGuide}[style](
        w, h, pattern, tint)
