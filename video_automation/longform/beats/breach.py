"""`breach` - a field of locked addresses, emptied wave by wave.

**Built for `hardware-wallet` (2026-11-12), because `pile` had become the
channel's answer to every sum of money** - the editor: "we are using the
animation with the physics coins too often, we need to create different
ones". A pile shows money going *into* one place and out of it. A breach of
many wallets is the opposite picture: the money is spread over thousands of
separate addresses, and they fall in waves. Reusable for any many-victim
loss: a leaked key batch, a drained protocol's depositors, a bridge's users.

A grid of squares, each standing for the same number of addresses (the
legend says how many). Two reveals, two caption chunks in this order:

1. the field ("Coins sat in more than five thousand addresses") - the
   squares arrive in a diagonal sweep, in the brand colour, under the label;
2. the loss ("about eighteen hundred bitcoin were drained, in four waves") -
   each wave spreads out from its own point and turns its squares hollow and
   `brand.negative`, the figure counts up with the squares, WAVE k OF n
   tracks it, and the verdict lands when the last square has gone.

The count-up is honest: the figure at any instant is the share of squares
already emptied. It is a running total, not a fact the viewer could misread
(`beats.md`, "A year never counts up").

payload: (cells_label, figure, unit, waves, title, verdict, legend)
  cells_label  "5,200+ ADDRESSES"   the label over the field
  figure       1816                 an int, counted up
  unit         "BTC"
  waves        4
  title        the beat's kicker
  verdict      "DRAINED"            lands at the end, default ""
  legend       "1 square = 25 addresses", default ""
  after        "0 DEVICES TOUCHED" - an optional third reveal: a line set
               under the verdict, for the sentence that follows the loss
               ("nobody touched a single device"). A Short cannot hold a
               shot, so this is how the field stays up under that line.

Landscape: the field at the left (16 x 13), the figure at the right.
Portrait: the figure above the same field.
"""

from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw

from ...core.draw import ease_out, shadow_text
from .base import Beat, _display, _font, _smooth

FILL_DUR = 0.9           # the field's arriving sweep
FLIP = 0.22              # one square turning


class Breach(Beat):

    EMBLEM = False

    def __init__(self, cells_label: str, figure: int, unit: str = "",
                 waves: int = 4, title: str = "", verdict: str = "",
                 legend: str = "", after: str = "", **kw):
        super().__init__(**kw)
        if waves < 1:
            raise ValueError("breach wants at least one wave")
        self.cells_label, self.figure, self.unit = cells_label, int(figure), unit
        self.waves, self.title = waves, title
        self.verdict, self.legend, self.after = verdict, legend, after
        fr, p = self.frame, self.portrait
        self.cols, self.rows = 16, 13
        self.pitch = 52 if p else 50
        self.cell = self.pitch - (12 if p else 10)
        gw, gh = self.cols * self.pitch, self.rows * self.pitch
        if p:
            self.gx = (fr.w - gw) // 2
            self.gy = self.head_y + (560 if after else 450)
        else:
            self.gx = self.margin + 40
            self.gy = self.head_y + 150
        self.gw, self.gh = gw, gh

        # Each wave spreads from its own point: a square belongs to the
        # nearest point, and falls in order of its distance from it.
        rng = random.Random(len(cells_label) * 131 + self.figure)
        seeds = []
        for k in range(waves):
            seeds.append((rng.uniform(0.12, 0.88) * self.cols,
                          (k + 0.5) / waves * self.rows
                          + rng.uniform(-1.2, 1.2)))
        rng.shuffle(seeds)
        self.order = {}            # (c, r) -> (wave, 0..1 inside the wave)
        by_wave: dict[int, list] = {k: [] for k in range(waves)}
        for r in range(self.rows):
            for c in range(self.cols):
                k = min(range(waves),
                        key=lambda i: math.dist((c, r), seeds[i]))
                by_wave[k].append((math.dist((c, r), seeds[k])
                                   + rng.uniform(0, 0.9), c, r))
        self.wave_n = []
        for k in range(waves):
            cells = sorted(by_wave[k])
            self.wave_n.append(len(cells))
            for i, (_, c, r) in enumerate(cells):
                self.order[(c, r)] = (k, i / max(1, len(cells) - 1))
        self.total = self.cols * self.rows

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (0.0 if i == 0 else 0.38))
        return self.at(f) - when

    def _drain_window(self) -> tuple[float, float]:
        """Seconds, from reveal 1, the waves take - most of what is left of
        the shot, so the last square goes before the cut, not on it."""
        rv = self.reveals or []
        t1 = rv[1] if len(rv) > 1 else self.start + self.hold * 0.38
        end = rv[2] + 1.1 if len(rv) > 2 else self.start + self.hold
        left = end - t1
        return 0.25, max(1.6, min(6.0, left - 1.1))

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        s0 = self._since(0, f)
        if s0 < 0:
            return
        br, p = self.brand, self.portrait
        prim, neg, ink = br.primary, br.negative, br.ink
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")

        s1 = self._since(1, f)
        lead, dur = self._drain_window()
        wave_len = dur / self.waves
        drained = 0.0
        cur_wave = 0
        for (c, r), (k, q) in self.order.items():
            # arrive: a diagonal sweep
            arrive = (c + r) / (self.cols + self.rows) * FILL_DUR
            a = ease_out(min(1.0, max(0.0, (s0 - arrive) / 0.25)))
            if a <= 0:
                continue
            x = self.gx + c * self.pitch + (self.pitch - self.cell) / 2
            y = self.gy + r * self.pitch + (self.pitch - self.cell) / 2
            flip = -1.0
            if s1 >= 0:
                when = lead + k * wave_len + q * wave_len * 0.82
                flip = (s1 - when) / FLIP
            if flip >= 0:
                cur_wave = max(cur_wave, k + 1)
            if flip >= 1.0:
                drained += 1
                d.rounded_rectangle([x, y, x + self.cell, y + self.cell],
                                    radius=7, fill=(18, 14, 14, 255),
                                    outline=neg + (230,), width=3)
            elif flip >= 0:
                drained += flip
                # the flash: white, shrinking into the hollow red square
                g = 1.0 - flip
                col = tuple(int(255 * g + n * (1 - g)) for n in neg)
                grow = 5 * g
                d.rounded_rectangle([x - grow, y - grow, x + self.cell + grow,
                                     y + self.cell + grow], radius=7,
                                    fill=col + (255,))
            else:
                s = self.cell * (0.6 + 0.4 * a)
                o = (self.cell - s) / 2
                d.rounded_rectangle([x + o, y + o, x + o + s, y + o + s],
                                    radius=7, fill=prim + (int(235 * a),))

        # The label over the field.
        la = int(255 * _smooth(s0 / 0.5))
        lf = _display(46 if p else 40)
        lb = d.textbbox((0, 0), self.cells_label, font=lf)
        lw = lb[2] - lb[0]
        lx = self.gx + (self.gw - lw) / 2 if p else self.gx
        ly = self.gy - (lb[3] - lb[1]) - 34
        shadow_text(d, (lx - lb[0], ly - lb[1]), self.cells_label, lf,
                    ink + (la,), alpha=la)
        if self.legend:
            gf = _font(28 if p else 26)
            gb = d.textbbox((0, 0), self.legend, font=gf)
            gx = (self.gx + (self.gw - (gb[2] - gb[0])) / 2 if p else self.gx)
            d.text((gx, self.gy + self.gh + 18), self.legend, font=gf,
                   fill=(165, 165, 165, la))

        # The figure, counted up with the squares.
        if s1 >= 0:
            share = min(1.0, drained / self.total)
            val = int(round(self.figure * share))
            ea = int(255 * _smooth(s1 / 0.4))
            ff = _display(170 if p else 190)
            uf = _display(64 if p else 70)
            sf = _font(34 if p else 32)
            num = f"{val:,}"
            full = f"{self.figure:,}"
            fb = d.textbbox((0, 0), full, font=ff)
            fw, fh = fb[2] - fb[0], fb[3] - fb[1]
            ub = d.textbbox((0, 0), self.unit, font=uf)
            uw = ub[2] - ub[0]
            if p:
                bx = (self.frame.w - (fw + 24 + uw)) / 2
                by = self.head_y + 96
            else:
                bx = self.gx + self.gw + 110
                by = self.gy + self.gh / 2 - fh / 2 - 60
            col = neg if share > 0 else ink
            shadow_text(d, (bx - fb[0], by - fb[1]), num, ff, col + (ea,),
                        alpha=ea)
            shadow_text(d, (bx + fw + 24 - ub[0], by + fh - (ub[3] - ub[1])
                            - ub[1]), self.unit, uf, col + (ea,), alpha=ea)
            wl = f"WAVE {max(1, min(self.waves, cur_wave))} OF {self.waves}"
            done = share >= 0.999
            if done and self.verdict:
                wl = self.verdict.upper()
            wy = by + fh + (30 if p else 36)
            if done and self.verdict:
                vf = _display(58 if p else 60)
                vb = d.textbbox((0, 0), wl, font=vf)
                pad = 18
                d.rounded_rectangle([bx - 4, wy, bx - 4 + vb[2] - vb[0]
                                     + 2 * pad, wy + vb[3] - vb[1] + 2 * pad],
                                    radius=10, fill=neg + (ea,))
                d.text((bx - 4 + pad - vb[0], wy + pad - vb[1]), wl, font=vf,
                       fill=(255, 255, 255, ea))
                s2 = self._since(2, f) if self.after and len(self.reveals or []) > 2 else -1
                if s2 >= 0:
                    af = _display(46 if p else 54)
                    aa = int(255 * _smooth(s2 / 0.35))
                    ax = bx - 4
                    ay = wy + vb[3] - vb[1] + 2 * pad + (22 if p else 30)
                    shadow_text(d, (ax, ay), self.after.upper(), af,
                                (255, 255, 255, aa), alpha=aa)
            else:
                d.text((bx, wy), wl, font=sf, fill=(170, 170, 170, ea))
                # a thin track under it, one segment per wave
                ty = wy + 54
                seg = (fw + 24 + uw) / self.waves
                for k in range(self.waves):
                    on = k < cur_wave
                    d.rounded_rectangle([bx + k * seg, ty,
                                         bx + (k + 1) * seg - 10, ty + 8],
                                        radius=4,
                                        fill=(neg + (ea,)) if on
                                        else (70, 70, 70, ea))
        out.paste(layer, (0, 0), layer)
