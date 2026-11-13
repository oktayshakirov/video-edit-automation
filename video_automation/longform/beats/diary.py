"""`diary` - a month of days, one square each, and the days memory keeps.

**Built for `what-makes-tinnitus-worse` (2026-11-13), because the library
could not draw recall bias.** The article's first argument is that a symptom
which moves on its own always finds a culprit: you remember the bad night
after the wine, and forget the bad nights without it and the wine before a
fine night. That is a claim about *which days of a month you look at*, so
the picture is the month - a calendar of squares, brighter on louder days,
with a dot on the days the suspect was there - and then rings round the
days the voice names, one group at a time. A list of the three traps says
the same words and shows nothing.

Reusable for any "track it before you blame it" subject on either channel:
a diary of spikes, of sleep, of trades made on a feeling.

Reveals, one caption chunk each, in this order:

0. the month - the squares arrive in a diagonal sweep, shaded by level,
   the suspect's dots popping in after them;
1..n. one per group - its days ringed in the group's colour, its line set
   in the list beside the month (under it in 9:16), and every day outside
   the rings already shown stepping back so the eye goes where the voice is.

payload: (levels, flagged, groups, title, legend, icon)
  levels   [0..10, ...] one per day, Monday first; 28 is four weeks
  flagged  [day index, ...] the days the suspect was present (the dot)
  groups   [(head, line, [day index, ...]), ...] - optionally a fourth
           element, an (r, g, b) ring colour
  title    the beat's kicker - always say it is an example
  legend   (dot_label, shade_label), e.g. ("a glass of wine",
           "brighter = louder"); either may be ""
  icon     optional emoji drawn on the flagged days and in the legend in
           place of the dot, e.g. "\U0001F377" for a glass of wine

**Title it as an example.** A drawn month with no such word reads as
somebody's real diary, and on a health channel that is a case history.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out, shadow_text
from .base import Beat, _display, _font, _smooth

SWEEP = 0.9              # the month's arriving sweep
RING_STAGGER = 0.16      # between two rings of one group
DAYS = "MTWTFSS"


class Diary(Beat):

    EMBLEM = False
    LOW = (78, 52, 104)              # a quiet day: the plum, lifted
    BACK = (36, 22, 50)              # what a day outside the rings fades toward
    WINE = (176, 46, 86)             # the suspect's dot
    COOL = (143, 184, 255)           # the second group's ring (audiogram's X ear)

    def __init__(self, levels: list, flagged: list = (), groups: list = (),
                 title: str = "", legend: tuple = ("", ""), icon: str = "",
                 **kw):
        super().__init__(**kw)
        # The suspect as an emoji on its days (the editor, 2026-11-13: "at
        # the calendar where we mark wine use wine emoji glass"). A plain dot
        # needed the legend to say what it was; the glass says it itself.
        self.icon = icon
        if not levels:
            raise ValueError("diary wants at least one day")
        self.levels = [max(0.0, min(10.0, float(v))) for v in levels]
        self.flagged = set(flagged)
        self.groups = [tuple(g) for g in groups]
        for g in self.groups:
            bad = [i for i in g[2] if not 0 <= i < len(self.levels)]
            if bad:
                raise ValueError(f"diary group {g[0]!r} names days {bad} "
                                 f"outside the month")
        self.title = title
        self.legend = tuple(legend) + ("", "")
        fr, p = self.frame, self.portrait
        self.cols = 7
        self.rows = (len(self.levels) + 6) // 7
        self.pitch = 124 if p else 118
        self.cell = self.pitch - 16
        self.gw, self.gh = self.cols * self.pitch, self.rows * self.pitch
        if p:
            self.gx = (fr.w - self.gw) // 2
            self.gy = self.head_y + 150
        else:
            self.gx = self.margin + 30
            self.gy = self.head_y + 190

    # -- clock -----------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        n = 1 + len(self.groups)
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (i / max(1, n)) * 0.85)
        return self.at(f) - when

    def _colour(self, i: int) -> tuple:
        g = self.groups[i]
        if len(g) > 3 and g[3]:
            return tuple(g[3])
        return (self.brand.negative, self.COOL, self.brand.ink)[min(i, 2)]

    def _xy(self, day: int) -> tuple[float, float]:
        c, r = day % 7, day // 7
        x = self.gx + c * self.pitch + (self.pitch - self.cell) / 2
        y = self.gy + r * self.pitch + (self.pitch - self.cell) / 2
        return x, y

    # -- drawing ---------------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        s0 = self._since(0, f)
        if s0 < 0:
            return
        br, p = self.brand, self.portrait
        prim = br.primary
        layer = self._layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")

        # Which groups are up, and how far in.
        shown = []
        for k in range(len(self.groups)):
            s = self._since(k + 1, f)
            if s >= 0:
                shown.append((k, s))
        ringed = {day for k, _ in shown for day in self.groups[k][2]}
        focus = _smooth(shown[0][1] / 0.5) if shown else 0.0

        # Weekday letters over the columns.
        wa = int(150 * _smooth(s0 / 0.5))
        wf = _font(30 if p else 28)
        for c, ch in enumerate(DAYS):
            cx = self.gx + c * self.pitch + self.pitch / 2
            d.text((cx, self.gy - 16), ch, font=wf, fill=(200, 200, 200, wa),
                   anchor="mb")

        for day, lvl in enumerate(self.levels):
            c, r = day % 7, day // 7
            arrive = (c + r) / (self.cols + self.rows) * SWEEP
            a = ease_out(min(1.0, max(0.0, (s0 - arrive) / 0.3)))
            if a <= 0:
                continue
            x, y = self._xy(day)
            t = lvl / 10.0
            t = t * t * (3 - 2 * t)            # louder days pull away
            col = tuple(int(lo + (hi - lo) * t)
                        for lo, hi in zip(self.LOW, prim))
            # Outside the rings, once a group is up, a day steps back.
            dim = 1.0 - 0.6 * focus * (0 if day in ringed else 1)
            col = tuple(int(b + (v - b) * dim) for v, b in zip(col, self.BACK))
            s = self.cell * (0.62 + 0.38 * a)
            o = (self.cell - s) / 2
            d.rounded_rectangle([x + o, y + o, x + o + s, y + o + s],
                                radius=14, fill=col + (int(250 * a),))
            # The suspect's dot, after its square.
            if day in self.flagged and self.icon:
                da = ease_out(min(1.0, max(0.0, (s0 - arrive - 0.35) / 0.25)))
                if da > 0:
                    self._icon(layer, x + self.cell / 2, y + self.cell / 2,
                               int(60 * (0.5 + 0.5 * da)), da * dim)
            elif day in self.flagged:
                da = ease_out(min(1.0, max(0.0, (s0 - arrive - 0.35) / 0.25)))
                if da > 0:
                    rr = 13 * da
                    cx, cy = x + self.cell - 22, y + 22
                    d.ellipse([cx - rr - 4, cy - rr - 4, cx + rr + 4,
                               cy + rr + 4], fill=(14, 10, 16, int(230 * dim)))
                    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                              fill=tuple(int(v * dim) for v in self.WINE)
                              + (255,))

        # The rings, each group in its own colour, staggered day by day.
        for k, s in shown:
            colour = self._colour(k)
            for j, day in enumerate(self.groups[k][2]):
                q = (s - j * RING_STAGGER) / 0.32
                if q <= 0:
                    continue
                e = ease_out(min(1.0, q))
                grow = 26 * (1 - e)
                x, y = self._xy(day)
                pad = 7 + grow
                d.rounded_rectangle([x - pad, y - pad, x + self.cell + pad,
                                     y + self.cell + pad], radius=18,
                                    outline=colour + (int(255 * e),), width=6)

        self._legend(d, s0)
        self._groups(d, shown)
        out.paste(layer, (0, 0), layer)

    def _icon(self, layer: Image.Image, cx: float, cy: float, h: int,
              alpha: float) -> None:
        """The suspect's emoji centred on (cx, cy), `alpha` 0..1."""
        from ...core.vertical import emoji_image
        im = emoji_image(self.icon, max(8, h)).copy()
        if alpha < 1:
            a = im.getchannel("A").point(lambda v: int(v * max(0.0, alpha)))
            im.putalpha(a)
        layer.alpha_composite(im, (int(cx - im.width / 2),
                                   int(cy - im.height / 2)))

    def _legend(self, d: ImageDraw.ImageDraw, s0: float) -> None:
        dot, shade = self.legend[0], self.legend[1]
        a = int(220 * _smooth((s0 - 0.6) / 0.5))
        if a <= 0:
            return
        lf = _font(30 if self.portrait else 28)
        y = self.gy + self.gh + 22
        x = self.gx
        if dot and self.icon:
            self._icon(self._layer, x + 14, y + 16, 34, a / 255)
            d.text((x + 36, y), dot, font=lf, fill=(210, 210, 210, a))
            x += 36 + d.textlength(dot, font=lf) + 48
        elif dot:
            d.ellipse([x, y + 4, x + 24, y + 28], fill=self.WINE + (a,))
            d.text((x + 36, y), dot, font=lf, fill=(210, 210, 210, a))
            x += 36 + d.textlength(dot, font=lf) + 48
        if shade:
            # a three-step swatch, quiet to loud
            for i in range(3):
                t = i / 2
                col = tuple(int(lo + (hi - lo) * t)
                            for lo, hi in zip(self.LOW, self.brand.primary))
                d.rounded_rectangle([x + i * 30, y + 4, x + i * 30 + 24,
                                     y + 28], radius=6, fill=col + (a,))
            d.text((x + 100, y), shade, font=lf, fill=(210, 210, 210, a))

    def _groups(self, d: ImageDraw.ImageDraw, shown: list) -> None:
        """Each group's line, set as it is named: beside the month in 16:9,
        under it in 9:16."""
        p = self.portrait
        hf = _display(40 if p else 46)
        lf = _font(32 if p else 34)
        if p:
            x0 = self.gx
            y = self.gy + self.gh + 84
            step = 98
        else:
            x0 = self.gx + self.gw + 90
            y = self.gy + 20
            step = 150
        for k, s in shown:
            head, line = self.groups[k][0], self.groups[k][1]
            a = int(255 * _smooth(s / 0.35))
            slide = 24 * (1 - ease_out(min(1.0, s / 0.35)))
            colour = self._colour(k)
            yy = y + k * step
            d.rounded_rectangle([x0 + slide, yy + 6, x0 + slide + 10,
                                 yy + (84 if p else 92)], radius=5,
                                fill=colour + (a,))
            shadow_text(d, (x0 + 30 + slide, yy), head.upper(), hf,
                        colour + (a,), alpha=a)
            d.text((x0 + 30 + slide, yy + (48 if p else 56)), line, font=lf,
                   fill=(235, 235, 235, a))
