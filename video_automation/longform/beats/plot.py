"""Beats that draw a curve or a series against an axis.

Time, trajectory and frequency. All three draw *onto* an axis that is
established first, and all three travel while the sentence that describes
them is being spoken - a plot that is simply present when the shot cuts in
reads as a screenshot."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, wrap
from .base import Beat, _font

class Timeline(Beat):
    """Dated events along a horizontal axis, **spaced by their real dates**.

    This is the difference between this and `steps`, and it is the whole
    reason the beat exists: `steps` puts four nodes at equal intervals because
    a procedure has no duration between its steps. A history does. "2009,
    2017, 2021, 2024" on an even track tells the viewer those gaps were the
    same size, which on the two subjects this channel covers is actively
    false - crypto's interesting years are clustered and tinnitus research
    has decade-long silences in it.

    So positions come from the numbers. The axis spans the first and last
    date, every other node lands where it actually falls, and a cluster looks
    like a cluster. A label collides with its neighbour when two dates are
    close, which is why labels alternate above and below the axis.

    payload: (events, title) where events is [(date, text), ...]

    `date` is whatever the script says out loud - "2009", "March 2020", "1st
    century". It is parsed for its first four-digit year to place the node and
    **printed verbatim**, so an approximate date reads as approximate.
    """

    EMBLEM = False
    R = 15                              # node radius

    def __init__(self, events: list, title: str = "", **kw):
        super().__init__(**kw)
        self.events = [(str(d), t) for d, t in events]
        self.title = title
        years = [self._year(d) for d, _ in self.events]
        lo, hi = min(years), max(years)
        span = (hi - lo) or 1
        # 8% of padding at each end, so the first and last node are not welded
        # to the edge of the rule.
        self.pos = [0.08 + 0.84 * (y - lo) / span for y in years]

    @staticmethod
    def _year(date: str) -> float:
        import re
        m = re.search(r"(\d{4})", date)
        return float(m.group(1)) if m else 0.0

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr, br = self.frame, self.brand
        top = self.heading(out, self.title, f)

        x0, x1 = self.margin, fr.w - self.margin
        cy = top + int((fr.h - top) * 0.46)

        # The axis draws across first, ahead of any node - the same gesture the
        # comparison's dividing rule makes, and for the same reason: the shape
        # of the argument is established before it has any content in it.
        e = self.open_p(f, 0.9)
        d.line([(x0, cy), (x0 + (x1 - x0) * e, cy)], fill=br.primary + (150,),
               width=4)

        date_font, label_font = _font(40), _font(34)
        for i, (date, text) in enumerate(self.events):
            p = self.due(i, len(self.events), f)
            if p < 0:
                continue
            a = int(255 * min(1.0, p))
            cx = x0 + (x1 - x0) * self.pos[i]
            # Alternating sides. Two adjacent dates in the same decade would
            # otherwise set their labels on top of each other, and this is
            # cheaper and more legible than collision detection.
            up = i % 2 == 0
            rr = int(self.R * ease_out(min(1.0, p)))

            # A tick down to the axis, so a node far from its label still reads
            # as belonging to a point in time rather than floating.
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                      fill=br.bg + (255,), outline=br.primary + (a,), width=4)
            d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=br.primary + (a,))

            stem = 96
            sy = cy - stem if up else cy + stem
            d.line([(cx, cy - self.R if up else cy + self.R), (cx, sy)],
                   fill=br.primary + (int(a * 0.6),), width=3)

            ty = sy - 96 if up else sy + 10
            # **The label is centred on the node, but clamped to the
            # margins.** The first and last node sit 8% in from each end,
            # which is not half a label's width - the 2024 label ran off the
            # right edge on the first render. Clamping rather than shrinking
            # the axis padding: a label that is 30px off-centre from its own
            # stem still reads as belonging to it, and a timeline squeezed
            # into the middle 60% of the frame does not.
            lines = wrap(d, text, label_font, 300)[:3]
            half = max([d.textlength(ln, font=label_font) for ln in lines]
                       + [d.textlength(date, font=date_font)]) / 2 + 8
            tx = max(self.margin + half, min(fr.w - self.margin - half, cx))
            d.text((tx, ty), date, font=date_font, fill=br.primary + (a,),
                   anchor="ma")
            for j, ln in enumerate(lines):
                d.text((tx, ty + 52 + j * 40), ln, font=label_font,
                       fill=br.ink + (a,), anchor="ma")


class Chart(Beat):
    """A line drawing itself left to right, with the turn marked.

    The beat the crypto channel has been missing since the first video. `bars`
    compares magnitudes at one moment; it cannot show a **trajectory**, and a
    trajectory is what almost every crypto sentence is about. Drawing it as a
    line that travels means the shape arrives in the same order the sentence
    describes it, which a static chart image can never do.

    **It is deliberately unlabelled on the y axis.** A chart with numbers up
    the side is a claim about magnitude that dates the video the moment it is
    uploaded; a chart with a shape is a claim about *behaviour*, which does
    not. If the script needs the number, that is a `stat`. This is the same
    rule the whole channel follows about dated figures, applied to a graphic.

    `marker` is the one moment the sentence is about - an index into the
    series. It lands on its own reveal, after the line has travelled past it,
    with a dropped rule to the axis and a caption. That second phase is the
    beat's whole payload: the line is context, the marker is the point.

    payload: (series, title, marker, note)
      series - [float, ...], any scale; it is normalised
      marker - index into `series`, or None for a line with no marked moment
    """

    EMBLEM = False

    def __init__(self, series: list, title: str = "", marker: int | None = None,
                 note: str = "", **kw):
        super().__init__(**kw)
        self.series = [float(v) for v in series]
        self.title, self.marker, self.note = title, marker, note

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr, br = self.frame, self.brand
        top = self.heading(out, self.title, f)

        x0, x1 = self.margin, fr.w - self.margin
        y1 = fr.h - int(fr.h * 0.16)
        y0 = top + 40
        if fr.h > fr.w:
            # **Portrait: fix the plot box and centre it, rather than letting
            # it fill the band.** A 9:16 frame leaves ~1300px of height against
            # a 1080px width, so the landscape geometry draws a chart half
            # again taller than it is wide — and a trajectory read on a box
            # that shape stops reading as a trajectory at all: the same climb
            # becomes a near-vertical wall and the drain becomes a cliff, which
            # is a different claim about behaviour from the one the series
            # makes. The box is pinned to 0.66 of its own width (a little
            # flatter than 3:2) and centred in whatever the heading leaves, so
            # the *shape* is the same shape the long form draws. The slack goes
            # above and below, where a drawn beat burns no caption anyway.
            #
            # Landscape is untouched — `fr.h > fr.w` is false there, so every
            # shipped 16:9 render is byte-identical.
            ph = min(y1 - y0, int((x1 - x0) * 0.66))
            mid = (y0 + y1) / 2
            y0, y1 = int(mid - ph / 2), int(mid + ph / 2)
        lo, hi = min(self.series), max(self.series)
        rng = (hi - lo) or 1.0
        pts = [(x0 + (x1 - x0) * i / (len(self.series) - 1),
                y1 - (y1 - y0) * (v - lo) / rng)
               for i, v in enumerate(self.series)]

        # The plate: an axis and three hairlines, in before the line arrives.
        e = self.open_p(f, 0.7)
        for k in (0.0, 0.5, 1.0):
            gy = y1 - (y1 - y0) * k
            d.line([(x0, gy), (x0 + (x1 - x0) * e, gy)],
                   fill=br.primary + (34,), width=2)
        d.line([(x0, y0), (x0, y1)], fill=br.primary + (90,), width=3)
        d.line([(x0, y1), (x0 + (x1 - x0) * e, y1)],
               fill=br.primary + (90,), width=3)

        # The line itself travels on the first reveal's span, so it is drawing
        # while the sentence that describes it is being spoken.
        p = self.span_p(0, f, cap=2.6)
        if p <= 0:
            return
        partial(d, pts, p, br.primary, 6)

        # A soft fill under the travelled part. Not decoration - it is what
        # separates "a line" from "a quantity over time" at a glance.
        n = max(2, int(len(pts) * p))
        if n >= 2:
            poly = pts[:n] + [(pts[n - 1][0], y1), (pts[0][0], y1)]
            shade = Image.new("RGBA", fr.size, (0, 0, 0, 0))
            ImageDraw.Draw(shade).polygon(poly, fill=br.primary + (46,))
            out.paste(Image.alpha_composite(out.convert("RGBA"), shade
                                            ).convert("RGB"), (0, 0))
            d = ImageDraw.Draw(out, "RGBA")
            partial(d, pts, p, br.primary, 6)

        if self.marker is None:
            return
        # Phase two: the marked moment, on its own reveal and only once the
        # line has actually reached it.
        mp = self.due(1, 2, f)
        reached = p >= self.marker / (len(pts) - 1)
        if mp < 0 or not reached:
            return
        mx, my = pts[self.marker]
        a = int(255 * min(1.0, mp))
        rr = int(16 * ease_out(min(1.0, mp)))
        d.line([(mx, my), (mx, y1)], fill=br.primary + (int(a * 0.55),), width=3)
        d.ellipse([mx - rr - 6, my - rr - 6, mx + rr + 6, my + rr + 6],
                  fill=br.bg + (220,))
        d.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=br.primary + (a,))
        if self.note:
            nf = _font(40)
            # Flip the caption to the left of the marker when it would run off
            # the right edge - a note clipped by the frame is worse than none.
            anchor = "ls" if mx < fr.w * 0.62 else "rs"
            dx = 34 if anchor == "ls" else -34
            d.text((mx + dx, my - 34), self.note, font=nf,
                   fill=br.ink + (a,), anchor=anchor)


class Spectrum(Beat):
    """A live frequency plot, with a band marked. The sound, made visible.

    This is the beat tinnitus long form should have had from the start, and
    the argument for it is not visual: `core/soundbed.py` already **generates**
    notched noise, so the notch it cuts is a real number this repo owns. A
    video that says "the notch is cut around your own tone" over a stock photo
    is describing its own audio track without showing it.

    The plot is synthesized rather than analysed - a smooth 1/f curve with a
    notch or a peak rendered into it at `band`. Analysing the actual bed would
    tie a beat's render to an audio file and gain nothing a viewer can see.

    The x axis is logarithmic and **labelled in Hz**, because unlike the
    chart's y axis this is not a dated magnitude - 4 kHz is 4 kHz forever, and
    it is the number a tinnitus viewer is looking for.

    payload: (band, title, note, mode) where
      band - (low_hz, high_hz), the marked region
      mode - "notch" (cut out of the curve) or "peak" (raised)
    """

    EMBLEM = False
    LO, HI = 100.0, 16000.0

    def __init__(self, band: tuple, title: str = "", note: str = "",
                 mode: str = "notch", **kw):
        super().__init__(**kw)
        self.band, self.title, self.note, self.mode = band, title, note, mode

    def _x(self, hz: float, x0: int, x1: int) -> float:
        lo, hi = math.log10(self.LO), math.log10(self.HI)
        q = (math.log10(max(self.LO, min(self.HI, hz))) - lo) / (hi - lo)
        return x0 + (x1 - x0) * q

    def content(self, out: Image.Image, f: float) -> None:
        fr, br = self.frame, self.brand
        top = self.heading(out, self.title, f)
        x0, x1 = self.margin, fr.w - self.margin
        y0, y1 = top + 40, fr.h - int(fr.h * 0.16)

        d = ImageDraw.Draw(out, "RGBA")
        e = self.open_p(f, 0.7)
        d.line([(x0, y1), (x0 + (x1 - x0) * e, y1)],
               fill=br.primary + (90,), width=3)

        tick_font = _font(28)
        for hz in (100, 500, 1000, 2000, 4000, 8000, 16000):
            gx = self._x(hz, x0, x1)
            d.line([(gx, y0), (gx, y1)], fill=br.primary + (24,), width=1)
            lbl = f"{hz // 1000}k" if hz >= 1000 else str(hz)
            d.text((gx, y1 + 14), lbl, font=tick_font,
                   fill=br.ink + (int(150 * e),), anchor="ma")

        # The curve. Moving, always - a still spectrum reads as a screenshot,
        # and the one thing a viewer knows about a frequency plot is that it
        # dances. The jitter is per-band and slow enough not to strobe.
        t = self.at(f)
        n = 240
        notch_p = self.due(1, 2, f)
        lo_hz, hi_hz = self.band
        ys, xs = [], []
        for i in range(n + 1):
            q = i / n
            hz = self.LO * (self.HI / self.LO) ** q
            # 1/f rolloff, which is what broadband noise actually looks like.
            v = 0.72 - 0.40 * q
            v += 0.05 * math.sin(t * 1.7 + q * 22) + 0.03 * math.sin(t * 2.9 + q * 51)
            if notch_p > 0 and lo_hz <= hz <= hi_hz:
                # The notch or the peak, eased in on its own reveal so the
                # shape changes exactly when the voice says it does.
                mid = (math.log10(hz) - math.log10(lo_hz)) / max(
                    1e-6, math.log10(hi_hz) - math.log10(lo_hz))
                depth = math.sin(mid * math.pi) * ease_out(min(1.0, notch_p))
                v += depth * (0.62 if self.mode == "peak" else -0.46)
            xs.append(x0 + (x1 - x0) * q)
            ys.append(y1 - (y1 - y0) * max(0.02, v))

        pts = list(zip(xs, ys))
        p = self.span_p(0, f, cap=2.2)
        if p <= 0:
            return

        k = max(2, int(len(pts) * p))
        fill = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        ImageDraw.Draw(fill).polygon(
            pts[:k] + [(pts[k - 1][0], y1), (pts[0][0], y1)],
            fill=br.primary + (54,))
        out.paste(Image.alpha_composite(out.convert("RGBA"), fill
                                        ).convert("RGB"), (0, 0))
        d = ImageDraw.Draw(out, "RGBA")
        partial(d, pts, p, br.primary, 5)

        if notch_p <= 0:
            return
        # The marked band: two uprights and the label between them. Drawn over
        # the curve, because it is the thing the sentence is about.
        a = int(255 * min(1.0, notch_p))
        bx0, bx1 = self._x(lo_hz, x0, x1), self._x(hi_hz, x0, x1)
        for bx in (bx0, bx1):
            d.line([(bx, y0), (bx, y1)], fill=br.primary + (int(a * 0.7),),
                   width=3)
        if self.note:
            d.text(((bx0 + bx1) / 2, y0 - 6), self.note, font=_font(38),
                   fill=br.ink + (a,), anchor="ma")


