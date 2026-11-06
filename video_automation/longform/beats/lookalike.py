"""`lookalike` - two addresses that match where people look, and nowhere else.

**Built for `random-crypto-in-your-wallet` (2026-11-05), because the library
could not draw address poisoning.** The scam is a picture: a scammer
generates addresses until the first and last few characters match the
victim's, sends a tiny transfer from it so it sits in their history, and
waits for a copy-paste. Narrated over a phone it is a sentence the viewer has
to picture; drawn, it is two strings that light up as the same at both ends
and then turn out to be different in the middle. `blindsign` is a screen
disagreeing with its payload, `post` a quoted line; neither sets two strings
against each other character by character, which is the one thing this beat
is for. Reusable for any look-alike: a clipboard swap, a spoofed domain, a
vanity address.

Four reveals, four caption chunks in this order: the real address ("Your
real address."), the look-alike under it ("Their look-alike."), the ends
lighting up on both rows ("The same start, the same end."), and the middle
of the look-alike turning `brand.negative` wherever it differs ("And a
different middle, where nobody looks."). Each address types in on its own
reveal; the ends sit in a band of `Brand.band`; on the last reveal a bracket
opens under the middle with DIFFERENT on it.

**Our card, not a wallet's interface** - drawn in the channel's type.

payload: (real, fake, title, ends, labels)
  real    the real address, `0x` and hex, any length up to 42
  fake    the look-alike, the same length
  title   the beat's kicker
  ends    (head, tail) - how many characters after `0x` match at the front
          and at the back. Default (4, 4); `__init__` raises if the two
          strings do not actually match there.
  labels  (real label, fake label), default ("YOUR ADDRESS", "THEIR LOOK-ALIKE")

**Portrait** breaks each address into two rows of equal length, so 42
characters stay at a phone-readable size.
"""

from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth

MONO = "/System/Library/Fonts/SFNSMono.ttf"
TYPE_DUR = 0.55          # seconds for an address to type in
LIGHT_DUR = 0.45         # the ends' band, and the middle turning


def _mono(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(MONO, size)


class Lookalike(Beat):

    EMBLEM = False

    def __init__(self, real: str, fake: str, title: str = "",
                 ends: tuple = (4, 4), labels: tuple | None = None, **kw):
        super().__init__(**kw)
        if len(real) != len(fake):
            raise ValueError(f"lookalike wants two addresses of one length, "
                             f"got {len(real)} and {len(fake)}")
        pre = 2 if real.lower().startswith("0x") else 0
        h, t = ends
        if pre + h + t >= len(real):
            raise ValueError("lookalike ends cover the whole address - "
                             "nothing is left to differ")
        if (real[:pre + h] != fake[:pre + h]
                or real[len(real) - t:] != fake[len(fake) - t:]):
            raise ValueError(f"lookalike: {real!r} and {fake!r} do not match "
                             f"on their first {h} and last {t} characters")
        if real[pre + h:len(real) - t] == fake[pre + h:len(fake) - t]:
            raise ValueError("lookalike: the two middles are identical")
        self.real, self.fake, self.title = real, fake, title
        self.pre, self.h, self.t = pre, h, t
        self.labels = labels or ("YOUR ADDRESS", "THEIR LOOK-ALIKE")

        fr = self.frame
        p = self.portrait
        n = len(real)
        # Portrait: two rows per address, split at the middle character.
        self.split = (n + 1) // 2 if p else n
        self.size = 60 if p else 54
        mf = _mono(self.size)
        self.adv = mf.getlength("0")
        self.cw = fr.w - 2 * 70 if p else 1560
        self.x0 = (fr.w - self.cw) // 2
        self.pad = 52 if p else 64
        line = self.adv * self.split
        if line > self.cw - 2 * self.pad:
            raise ValueError(f"lookalike: a {self.split}-character row is "
                             f"{line:.0f}px and the card has "
                             f"{self.cw - 2 * self.pad}px")
        self.tx = self.x0 + (self.cw - line) / 2
        rows = 2 if p else 1
        self.line_h = int(self.size * 1.5)
        self.lab_h = 64 if p else 58
        self.block_h = self.lab_h + rows * self.line_h
        self.gap = 70 if p else 64
        self.bracket_h = 120 if p else 104
        self.ch = (2 * self.pad + 2 * self.block_h + self.gap
                   + self.bracket_h)
        top = self.head_y + 110
        self.y0 = max(top, (fr.h - self.ch) // 2 + (20 if p else 30))

        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        for lab in self.labels:
            if d.textlength(lab, font=_font(30)) > self.cw - 2 * self.pad:
                raise ValueError(f"lookalike label {lab!r} is too wide")

    # --- geometry -----------------------------------------------------------

    def _pos(self, i: int, block_y: float) -> tuple[float, float]:
        """Top-left of character `i` in an address block."""
        row, col = divmod(i, self.split)
        return (self.tx + col * self.adv,
                block_y + self.lab_h + row * self.line_h)

    def _end(self, i: int) -> bool:
        n = len(self.real)
        return i < self.pre + self.h or i >= n - self.t

    def _middle(self) -> range:
        return range(self.pre + self.h, len(self.real) - self.t)

    # --- clocks -------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        t = self.at(f)
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (i / 4) * 0.85)
        return t - when

    # --- the frame ----------------------------------------------------------

    def _block(self, d: ImageDraw.ImageDraw, text: str, label: str,
               y: float, typed: float, ends: float, middle: float,
               fake: bool) -> None:
        br = self.brand
        prim, ink, neg = br.primary, br.ink, br.negative
        band, band_ink = br.band or br.primary, br.band_ink
        a = int(255 * min(1.0, typed * 3))
        lf = _font(30)
        d.text((self.tx, y + 6), label, font=lf, fill=(150, 150, 150, a))
        mf = _mono(self.size)
        shown = int(round(len(text) * typed))
        b = d.textbbox((0, 0), "0", font=mf)
        gh = b[3] - b[1]

        # The ends' band, drawn behind the characters, one rounded box per
        # run per row so a portrait split never draws one box across rows.
        if ends > 0:
            runs = []
            for i in range(len(text)):
                if not self._end(i):
                    continue
                x, cy = self._pos(i, y)
                if runs and runs[-1][2] == cy and abs(runs[-1][1] - x) < 1:
                    runs[-1][1] = x + self.adv
                else:
                    runs.append([x, x + self.adv, cy])
            for x0, x1, cy in runs:
                w = (x1 - x0) * ease_out(min(1.0, ends))
                d.rounded_rectangle([x0 - 8, cy - 10, x0 + w + 8,
                                     cy + gh + b[1] + 14], radius=10,
                                    fill=band + (int(235 * min(1.0, ends)),))

        for i, ch in enumerate(text[:shown]):
            x, cy = self._pos(i, y)
            col = ink
            if ends > 0 and self._end(i):
                col = tuple(int(c0 + (c1 - c0) * min(1.0, ends))
                            for c0, c1 in zip(ink, band_ink))
            elif fake and middle > 0 and i in self._middle() \
                    and ch != self.real[i]:
                col = tuple(int(c0 + (c1 - c0) * min(1.0, middle))
                            for c0, c1 in zip(ink, neg))
            elif not fake and middle > 0 and i in self._middle():
                # The real middle dims, so the eye goes to the fake one.
                col = tuple(int(c * (1 - 0.45 * min(1.0, middle))) for c in ink)
            d.text((x, cy), ch, font=mf, fill=col + (a,))
        # The caret while it types.
        if 0 < typed < 1:
            x, cy = self._pos(min(shown, len(text) - 1), y)
            if shown >= len(text):
                x += self.adv
            d.rectangle([x + 2, cy + b[1], x + 6, cy + b[3]],
                        fill=prim + (a,))

    def _bracket(self, d: ImageDraw.ImageDraw, y_line: float,
                 p: float) -> None:
        """A bracket under the look-alike's middle, DIFFERENT on it."""
        if p <= 0:
            return
        neg = self.brand.negative
        mid = list(self._middle())
        # In portrait the middle spans two rows; bracket the last row's part.
        last_row = max(divmod(i, self.split)[0] for i in mid)
        cols = [divmod(i, self.split)[1] for i in mid
                if divmod(i, self.split)[0] == last_row]
        x0 = self.tx + min(cols) * self.adv
        x1 = self.tx + (max(cols) + 1) * self.adv
        y = y_line + 16
        pts = [(x0, y), (x0, y + 22), (x1, y + 22), (x1, y)]
        partial(d, pts, min(1.0, p * 1.3), neg, 4)
        a = int(255 * _smooth((p - 0.3) / 0.7))
        if a <= 0:
            return
        lf = _display(40 if self.portrait else 34)
        lab = "DIFFERENT"
        lb = d.textbbox((0, 0), lab, font=lf)
        lx = (x0 + x1) / 2 - (lb[2] - lb[0]) / 2 - lb[0]
        shadow_text(d, (lx, y + 40 - lb[1]), lab, lf, neg + (a,), alpha=a)

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        if self.due(0, 4, f) < 0:
            return
        fr, br = self.frame, self.brand
        prim = br.primary
        layer = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")

        s0 = self._since(0, f)
        enter = min(1.0, max(0.0, s0 / 0.6))
        x0, y0, cw, ch = self.x0, self.y0, self.cw, self.ch
        x1, y1 = x0 + cw, y0 + ch
        d.rounded_rectangle([x0, y0, x1, y1], radius=26,
                            fill=(16, 16, 16, int(236 * enter)))
        mx = (x0 + x1) / 2
        pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                              (x0, y0), (mx + 0.5, y0)], 26, seg=10)
        partial(d, pts, max(0.001, _smooth(s0 / 0.7)), prim, 4)

        s1, s2, s3 = (self._since(i, f) for i in (1, 2, 3))
        typed_r = min(1.0, max(0.0, (s0 - 0.15) / TYPE_DUR))
        typed_f = min(1.0, max(0.0, (s1 - 0.10) / TYPE_DUR))
        ends = max(0.0, s2 / LIGHT_DUR)
        middle = max(0.0, s3 / LIGHT_DUR)

        ry = y0 + self.pad
        fy = ry + self.block_h + self.gap
        self._block(d, self.real, self.labels[0], ry, typed_r, ends, middle,
                    False)
        if s1 >= 0:
            self._block(d, self.fake, self.labels[1], fy, typed_f, ends,
                        middle, True)
        rows = 2 if self.portrait else 1
        self._bracket(d, fy + self.lab_h + rows * self.line_h - 18,
                      max(0.0, (s3 - 0.1) / 0.6))
        rise = int(22 * (1 - ease_out(enter)))
        out.paste(layer, (0, rise), layer)
