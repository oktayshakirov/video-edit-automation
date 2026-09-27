"""Instruments: a magnitude read against a scale.

Bars compare several magnitudes at one moment, a gauge puts one value on a
track against a threshold, and a dial puts it in a named band. The question
each answers is different - 'which is bigger', 'how far along', 'which band
is it in' - and picking the wrong one is the usual reason a number beat
reads as decoration."""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from ...core.draw import shadow_text, wrap
from .base import RISE, Beat, _display, _font, _hex

class Bars(Beat):
    """A horizontal bar chart that grows on the voice.

    The beat that was missing. `stat` shows one number and `compare` shows two
    lists, but neither can show a *proportion* — and a proportion is the one
    thing a spoken number cannot convey. "One point one million coins" means
    nothing to a viewer who does not know the supply; the same figure drawn
    against 21 million is instantly legible and needs no second sentence.

    Bars grow from the left with an ease-out, so the eye follows the end of the
    bar rather than watching a rectangle appear. The value sits at the end of
    its own bar and travels with it.

    **The track is shortened by the widest value in the payload**, because a
    bar at fraction 1.000 fills it and leaves its own label nowhere to go. The
    first version clamped the label's start x to just inside the track - a
    clamp on the anchor rather than on the extent - so a full-length row
    printed "50 BTC" as "50 BT" off the edge of the frame, unclipped and
    unraised. Setting that one label inside the bar was tried and is worse: the
    value font is 46px against a 30px bar, and one row treated unlike the other
    four reads as a fault. Reserving the column costs a few percent of every
    bar, which is invisible because bars are read against each other.

    payload: (rows, title) where rows is [(label, fraction, value_text), ...]
    """

    EMBLEM = False

    def __init__(self, rows: list[tuple[str, float, str]], title: str = "",
                 **kw):
        super().__init__(**kw)
        self.rows, self.title = rows, title

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        x, _ = self.col
        top = self.heading(out, self.title, f)

        # Full width — a bar chart squeezed into the left column wastes the one
        # dimension it actually needs.
        w = self.frame.w - 2 * self.margin
        label_font, value_font = _font(42), _font(46)
        # **Reserve the value column before laying out the track.** A bar at
        # fraction 1.000 fills the track by definition, so its value has
        # nowhere to go: the halving chart's top row printed "50 BTC" as
        # "50 BT" against the frame edge, and nothing clipped it or raised.
        # Putting that one label *inside* the bar was tried and is worse — the
        # value font is 46px against a 30px bar, so a centred label is cut off
        # top and bottom, and one row treated differently from the rest reads
        # as a fault rather than as a rule. Shortening the track for every row
        # keeps one treatment and costs a few percent of bar length, which is
        # invisible because the bars are read against each other.
        vw = max((d.textlength(v, font=value_font)
                  for _, _, v in self.rows if v), default=0.0)
        if vw:
            w -= int(vw) + 44
        n = len(self.rows)
        pitch = 132
        top = max(top + 20, (self.frame.h - n * pitch) // 2)

        for i, (label, frac, value) in enumerate(self.rows):
            e = self.due(i, n, f)
            if e < 0:
                continue
            y = top + i * pitch
            # The bar grows across its own phrase (`span_p`), not a fixed
            # 0.85s — so a row spoken slowly fills slowly, and the value at
            # its tip tracks the voice instead of racing ahead of it.
            g = self.span_p(i, f, lead=0.06, cap=1.6)

            shadow_text(d, (x, y), label, label_font, self.brand.ink)

            by = y + 58
            bh = 30
            # The track, so an unfilled bar still reads as "out of something".
            d.rectangle([x, by, x + w, by + bh], fill=(255, 255, 255, 26))
            bw = int(w * max(0.0, min(1.0, frac)) * g)
            if bw > 1:
                d.rectangle([x, by, x + bw, by + bh],
                            fill=self.brand.primary + (235,))
            if value:
                shadow_text(d, (x + bw + 22, by - 8), value, value_font,
                            self.brand.primary)


class Gauge(Beat):
    """One value on a scale, against a threshold. The beat for "how much is too much".

    **`stat` shows a bare number and `bars` shows proportions of a whole;
    neither can show a *limit*.** "Eighty-five decibels" is a figure with no
    meaning attached, and drawing it larger does not give it one — the fact
    the viewer needs is that it sits past the line where damage starts. That
    is a different claim from a proportion (`bars`) and a different graphic
    from a number in an empty half-frame (`stat`), and on both of these sites
    it is one of the commonest claims there is: decibels against safe
    exposure, a caffeine dose against a threshold, leverage against a
    liquidation point.

    It replaces the weakest `stat` uses rather than adding to them. A `stat`
    whose figure only means something relative to some other figure was
    always the wrong beat; there simply was not a right one.

    **The silhouette is one track, not several.** `bars` stacks rows down the
    left with labels beside them and reads as a chart; this is a single thick
    scale across the middle of the frame with a flag above it, and at a glance
    the two are not the same graphic. Keeping it to one row is the whole
    point — the moment a second row appears it is a bar chart.

    Two reveals, in this order:

    0. **The scale and the threshold.** The track draws across, the threshold
       uprights, and its label sets. This is the sentence that says what the
       limit is: "Eight hours a day is safe at eighty decibels."
    1. **The value.** The marker travels along the track to its position and
       the figure counts up over it. This is the sentence that says where the
       thing actually sits: "A hairdryer is ninety-five."

    So write the beat as **two caption chunks**, limit first and value second.
    Written the other way round the marker lands before there is a line for it
    to sit past, which is the "say the point, then show the graphic" rule
    inside a single beat.

    `frac` and `threshold` are fractions of the track, 0..1 — they are
    *positions*, not data, and it is the author's job to place them honestly.
    A logarithmic quantity (decibels, and most of what this beat is for) does
    not go on a linear track by dividing one number by another; place the
    ticks where the scale actually falls and put the real values in
    `scale_labels`.

    payload: (value, frac, label, threshold, threshold_label, title)
      value            "95 dB"      the figure, drawn on the flag
      frac             0.0..1.0     where the marker sits on the track
      label            "A HAIRDRYER"  what the value is, under the flag
      threshold        0.0..1.0 or None
      threshold_label  "SAFE FOR 8 HOURS"
      title            the beat's kicker
    """

    EMBLEM = False
    TRACK_H = 34

    def __init__(self, value: str, frac: float, label: str = "",
                 threshold: float | None = None, threshold_label: str = "",
                 title: str = "", **kw):
        super().__init__(**kw)
        self.value, self.frac, self.label = value, float(frac), label
        self.threshold = None if threshold is None else float(threshold)
        self.threshold_label, self.title = threshold_label, title

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr = self.frame
        top0 = self.heading(out, self.title, f)

        x0 = self.margin
        w = fr.w - 2 * self.margin
        # A 34px track across 1080 reads as a hairline where the same track
        # across 1920 reads as a bar. Portrait is not landscape scaled down,
        # which is the note `Beat.__init__` already makes about the margin.
        track_h = self.TRACK_H if not self.portrait else 46
        # Room for the flag above and the threshold label below, rather
        # than the frame's own middle — a track centred at h/2 put the
        # figure high and left the bottom third of the frame empty.
        cy = max(top0 + 260, int(fr.h * 0.52))
        big = _display(132 if not self.portrait else 108)
        flag_font = _font(40 if not self.portrait else 44)
        thr_font = _font(34 if not self.portrait else 38)

        # --- reveal 0: the track and the threshold ------------------------
        e0 = self.due(0, 2, f)
        if e0 < 0:
            return
        # Drawn across the limit sentence, not in a fixed 0.55s — the same
        # voice-synced clock the diagram's connectors use, so the track is
        # still extending while "eight hours a day is safe at eighty
        # decibels" is being said.
        draw_e = self.span_p(0, f, lead=0.05, cap=1.6)
        # The empty track, drawn across as the beat opens — the same device
        # `steps` and `compare` use, so the shape of the claim is established
        # before any value is in it.
        d.rounded_rectangle([x0, cy, x0 + w * draw_e, cy + track_h],
                            radius=track_h // 2,
                            fill=(255, 255, 255, 26))

        if self.threshold is not None:
            tx = x0 + w * max(0.0, min(1.0, self.threshold))
            if draw_e * w >= (tx - x0):
                # An upright through the track, and the region past it shaded
                # — the shading is what says "this side is the problem"
                # without a word of type doing it.
                d.rectangle([tx, cy, x0 + w, cy + track_h],
                            fill=self.brand.negative + (40,))
                d.line([(tx, cy - 54), (tx, cy + track_h + 54)],
                       fill=self.brand.ink + (150,), width=3)
                if self.threshold_label:
                    ty = cy + track_h + 70
                    for ln in wrap(d, self.threshold_label.upper(), thr_font,
                                   min(w * 0.42, w - (tx - x0) + 120)):
                        shadow_text(d, (tx + 16, ty), ln, thr_font,
                                    self.brand.ink + (170,))
                        ty += 42

        # --- reveal 1: the value travels ----------------------------------
        e1 = self.due(1, 2, f)
        if e1 < 0:
            return
        # The marker travels across the value sentence — "a hairdryer is
        # ninety-five" — so the figure arrives at its mark as the sentence
        # names it, not a fixed beat later.
        g = self.span_p(1, f, lead=0.05, cap=1.5)
        vx = x0 + w * max(0.0, min(1.0, self.frac)) * g
        # **The fill changes colour where it crosses the line.** The first
        # version drew one primary-coloured fill straight over the shaded
        # danger zone, which hid the shading completely and left the whole
        # claim resting on a thin upright — on a rendered frame the bar simply
        # read as "quite full", not as "past the limit". Two colours say it
        # without a word of type: the beat is *about* the crossing, so the
        # crossing is the thing that has to be visible.
        over = (self.threshold is not None
                and self.frac > self.threshold)
        tx = x0 + w * (self.threshold or 0.0)
        d.rounded_rectangle([x0, cy, max(x0 + 1, min(vx, tx) if over else vx),
                             cy + track_h],
                            radius=track_h // 2,
                            fill=self.brand.primary + (235,))
        if over and vx > tx:
            d.rounded_rectangle([tx, cy, vx, cy + track_h],
                                radius=track_h // 2,
                                fill=self.brand.negative + (240,))
        head = self.brand.negative if over else self.brand.primary
        # **The marker is filled with the ink, ringed in the fill's colour.**
        # Filled with `head` it was the same colour as the bar it sits on and
        # disappeared into it — the one element that has to say *where* was
        # the least visible thing on the frame.
        d.ellipse([vx - 24, cy + track_h // 2 - 24,
                   vx + 24, cy + track_h // 2 + 24],
                  fill=self.brand.ink, outline=head, width=6)

        # The flag above the marker: the figure, and the label under it.
        #
        # **The label is placed off the figure's measured box, not off a
        # constant.** The first version set the value at `cy - 96` and the
        # label at `cy - 78`, which are 18px apart while the figure itself is
        # 132px tall — so "A HAIRDRYER" printed straight through "95 dB" on
        # the very first rendered frame. Nothing raises on overlapping type;
        # the only way to catch it is to look.
        a = int(255 * min(1.0, e1))
        tb = d.textbbox((0, 0), self.value, font=big)
        bw, bh = tb[2] - tb[0], tb[3] - tb[1]
        lab = self.label.upper() if self.label else ""
        lh = 52 if lab else 0
        rise = int(round(RISE * (1.0 - min(1.0, e1))))
        # Bottom of the whole flag sits a clear gap above the track.
        fy = cy - 46 - lh - bh + rise
        fx = min(max(vx - bw / 2 - tb[0], x0), x0 + w - bw)
        shadow_text(d, (fx, fy - tb[1]), self.value, big, head + (a,), alpha=a)
        if lab:
            lw = d.textlength(lab, font=flag_font)
            shadow_text(d, (min(max(vx - lw / 2, x0), x0 + w - lw),
                            fy + bh + 10), lab, flag_font,
                        self.brand.ink + (a,), alpha=a)


class Dial(Beat):
    """A semicircular gauge: coloured bands around an arc, and a needle.

    **The beat for a named scale, which `gauge` is not.** `gauge` draws one
    value against one *threshold* — a dose past a safe limit, decibels past
    where damage starts — and its whole silhouette is a single straight track
    with a flag on it. This draws a *graduated scale with named regions*: 0 to
    100 with five bands, a severity ladder, a risk register. The difference is
    not decoration. On a `gauge` the question is "which side of the line is
    it on"; here the question is "which band is it in", and a linear track
    with five colours on it reads as a stacked bar chart rather than as an
    instrument.

    It was built for the Crypto Fear & Greed Index, where the dial *is* the
    subject — the site publishes the scale, the five band names and their
    colours, and the video had no way to show any of it except by filming a
    person looking worried. That is the failure this beat exists to end: an
    abstract topic whose nouns are "a number", "a score" and "a scale" has no
    photographic referent at all, so stock footage under it is always going to
    be mood rather than meaning. Draw the noun.

    **Radial, and that is the point.** Every other beat in this library lays
    type in rows; this one is the only circular object in the set, so it can
    never be mistaken at a glance for a list. It is also the one shape that
    reads *better* in portrait than in landscape — a dial is as tall as it is
    wide, where `gauge`'s horizontal track wastes a 9:16 frame.

    Two reveals, in this order:

    0. **The scale.** The arc sweeps left to right, the bands colour in behind
       it, the boundary ticks and their numbers set. This is the sentence that
       says what the scale *is*: "It runs from zero to a hundred."
    1. **The needle.** It travels from the low end to its position while the
       figure counts up under it. This is the sentence that says where
       something sits.

    So write it as **two caption chunks, scale first and needle second** — the
    same "say the point, then show the graphic" rule the other beats follow
    inside a single beat. Pass `value=None` for a scale with no needle at all,
    which is one reveal and is the honest graphic for a line that describes
    the instrument rather than a reading on it. In a YMYL niche that
    distinction is the difference between explaining an index and appearing to
    call one, so it is a payload option rather than something a script has to
    fake by parking the needle somewhere.

    **The vector layer is supersampled; the type is not.** PIL draws neither
    arcs nor polygons antialiased, and a 46px band with a stair-stepped edge
    at 1920 reads as a rendering fault rather than as an instrument — the same
    objection this file already makes to whole-pixel motion and to instant
    strike-throughs. The arc, the ticks and the needle are drawn at `SS` times
    final size into their own RGBA layer and downscaled with LANCZOS; the
    numerals go on afterwards at full resolution through `shadow_text`, so
    they keep the crispness every other beat's type has.

    payload: (bands, value, label, title)
      bands  [(name, upto, "#rrggbb"), ...] — `upto` is the band's far edge as
             a fraction of the scale, ascending, ending at 1.0. The first and
             last names are drawn under the arc's ends as the poles.
      value  0.0..1.0, or None for a scale with no needle
      label  what the needle position is called, under the figure
      title  the beat's kicker
    """

    EMBLEM = False
    SS = 2                      # supersample factor for the vector layer
    NEEDLE_W = 15               # half-width of the needle at the hub
    TICKS = (0.0, 0.25, 0.5, 0.75, 1.0)

    def __init__(self, bands: list, value: float | None = None,
                 label: str = "", title: str = "", **kw):
        super().__init__(**kw)
        self.bands = [(str(b[0]), float(b[1]), b[2]) for b in bands]
        self.value = None if value is None else float(value)
        self.label, self.title = label, title

    def _geom(self) -> tuple[int, int, int, int, int]:
        """cx, cy, radius, band thickness, hub radius."""
        fr = self.frame
        if self.portrait:
            return fr.w // 2, int(fr.h * 0.46), 386, 56, 30
        return fr.w // 2, int(fr.h * 0.63), 352, 46, 26

    def _vector(self, R: int, th: int, hub_r: int, sweep: float,
                needle: float | None) -> tuple[Image.Image, int, int]:
        """The arc, its ticks and the needle, drawn big and brought back down.

        Returns the layer and the offset of its own centre inside it, so the
        caller can paste it against the dial's centre without re-deriving the
        padding.
        """
        S, pad = self.SS, 36
        outer = R + th // 2 + pad
        w, h = 2 * outer, outer + hub_r + pad
        im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy, rr = outer * S, outer * S, R * S
        box = [cx - rr, cy - rr, cx + rr, cy + rr]
        limit = 180.0 + 180.0 * max(0.0, min(1.0, sweep))

        # The unlit track first, so the scale has a shape before it has
        # colour — the same reason `gauge` draws an empty track and `steps`
        # draws its rail before any node lands on it.
        if sweep > 0:
            d.arc(box, 180, 360, fill=(255, 255, 255, 30), width=th * S)
        lo = 0.0
        for _, upto, col in self.bands:
            a0, a1 = 180.0 + 180.0 * lo, min(180.0 + 180.0 * upto, limit)
            if a1 > a0:
                d.arc(box, a0, a1, fill=_hex(col) + (255,), width=th * S)
            lo = upto

        # Ticks on the round quarters, not on the band edges. The index's own
        # bands break at 25 / 50 / 55 / 75, and a tick at both 50 and 55 is
        # two marks four pixels apart that the eye reads as a printing error.
        # An instrument graduates its scale evenly and lets the colour say
        # where the regions are.
        r0, r1 = (R + th // 2 + 8) * S, (R + th // 2 + 24) * S
        for e in self.TICKS:
            if 180.0 + 180.0 * e > limit:
                continue
            a = math.radians(180.0 + 180.0 * e)
            d.line([(cx + r0 * math.cos(a), cy + r0 * math.sin(a)),
                    (cx + r1 * math.cos(a), cy + r1 * math.sin(a))],
                   fill=self.brand.ink + (150,), width=3 * S)

        if needle is not None:
            a = math.radians(180.0 + 180.0 * max(0.0, min(1.0, needle)))
            L = (R - th // 2 - 20) * S
            tip = (cx + L * math.cos(a), cy + L * math.sin(a))
            # Perpendicular at the hub, so the needle tapers rather than
            # being a bar with a point stuck on it.
            px, py = -math.sin(a), math.cos(a)
            bw = self.NEEDLE_W * S
            # **Ink, not the band's own colour.** `gauge` records this from
            # the other direction: a marker filled with the colour of the
            # thing it sits on is the least visible element on the frame, and
            # the needle is the one element whose entire job is to say where.
            d.polygon([tip, (cx + px * bw, cy + py * bw),
                       (cx - px * bw, cy - py * bw)],
                      fill=self.brand.ink + (255,))
            d.ellipse([cx - hub_r * S, cy - hub_r * S,
                       cx + hub_r * S, cy + hub_r * S],
                      fill=self.brand.primary + (255,))
            k = int(hub_r * 0.42) * S
            d.ellipse([cx - k, cy - k, cx + k, cy + k],
                      fill=self.brand.bg + (255,))

        return im.resize((w, h), Image.LANCZOS), outer, outer

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        self.heading(out, self.title, f)
        cx, cy, R, th, hub_r = self._geom()

        e0 = self.due(0, 2 if self.value is not None else 1, f)
        if e0 < 0:
            return
        sweep = self.span_p(0, f, lead=0.05, cap=1.7)

        needle = None
        travel = 0.0
        if self.value is not None:
            e1 = self.due(1, 2, f)
            if e1 >= 0:
                travel = self.span_p(1, f, lead=0.05, cap=1.5)
                needle = self.value * travel

        layer, ox, oy = self._vector(R, th, hub_r, sweep, needle)
        out.paste(layer, (cx - ox, cy - oy), layer)

        # --- type, at full resolution -------------------------------------
        tick_font = _font(32 if not self.portrait else 36)
        rt = R + th // 2 + 58
        for e in self.TICKS:
            txt = str(int(round(e * 100)))
            if e > sweep:
                continue
            a = math.radians(180.0 + 180.0 * e)
            tx, ty = cx + rt * math.cos(a), cy + rt * math.sin(a)
            bb = d.textbbox((0, 0), txt, font=tick_font)
            shadow_text(d, (tx - (bb[2] - bb[0]) / 2, ty - (bb[3] - bb[1]) / 2),
                        txt, tick_font, self.brand.ink + (190,))

        # The poles, under the two ends of the arc — "fear on one end, greed
        # on the other" is a line this beat can say without narration.
        if sweep > 0.98 and len(self.bands) >= 2:
            pole = _font(34 if not self.portrait else 38)
            ly, lx = cy + 30, cx - R - th // 2
            shadow_text(d, (lx, ly), self.bands[0][0].upper(), pole,
                        _hex(self.bands[0][2]))
            rtxt = self.bands[-1][0].upper()
            bb = d.textbbox((0, 0), rtxt, font=pole)
            shadow_text(d, (cx + R + th // 2 - (bb[2] - bb[0]), ly), rtxt,
                        pole, _hex(self.bands[-1][2]))

        # The figure and its band name go **below the hub**, which is the one
        # region of the frame a semicircular needle can never enter. The first
        # cut set them inside the arc, where an instrument normally puts them,
        # and the needle drew straight through the numeral on every reading
        # near the middle of the scale — which is most of them. Geometry
        # settles this, not taste: the needle sweeps 180..360 degrees, so
        # everything under the hub is permanently clear.
        if needle is not None and travel > 0:
            big = _display(150 if not self.portrait else 132)
            txt = str(int(round(self.value * 100 * travel)))
            bb = d.textbbox((0, 0), txt, font=big)
            fy = cy + (104 if not self.portrait else 118)
            shadow_text(d, (cx - (bb[2] - bb[0]) / 2, fy), txt, big,
                        self.brand.ink)
            if self.label and travel > 0.92:
                lf = _font(44 if not self.portrait else 48)
                bb2 = d.textbbox((0, 0), self.label.upper(), font=lf)
                shadow_text(d, (cx - (bb2[2] - bb2[0]) / 2,
                                fy + (bb[3] - bb[1]) + 46),
                            self.label.upper(), lf, self.brand.primary)


