"""`peers` - bitcoins moving wallet to wallet, with no centre.

**Built for `bitcoin-ponzi` (2026-11-25), on the editor's note**: "replace
one of the later [stock clips] with custom screen of moving bitcoins". A
`pile` pours coins into one bin, which is the Ponzi's pot - the opposite
of the line it would sit under. This draws a loose field of wallets joined
to their neighbours, and coins with a drawn bitcoin sign travelling along
the links, peer to peer, for the whole shot. Nothing sits in the middle;
a wallet glints as a coin lands. Reusable under any line about a network
with no operator - "nobody runs it", "it keeps running", a closing
question about Bitcoin itself.

payload: (title, label)
  title  the beat's kicker ("" for none)
  label  optional band under the field, on the one reveal ("" for none)

One reveal: the field draws in on the shot's start, the label sets on the
reveal. Deterministic (a fixed seed), so a re-render is identical.
Portrait-safe.
"""

from __future__ import annotations

import math
import random

from PIL import Image, ImageDraw

from .base import Beat, _display, _smooth


def coin_sign(d: ImageDraw.ImageDraw, x: float, y: float, r: float, ink, a: int):
    """A bitcoin sign drawn, not set: a bold B with two short bars through
    its top and bottom - the display face has no U+20BF."""
    f = _display(max(8, int(r * 1.25)))
    b = d.textbbox((0, 0), "B", font=f)
    w, h = b[2] - b[0], b[3] - b[1]
    tx, ty = x - w / 2 - b[0] + r * 0.05, y - h / 2 - b[1]
    d.text((tx, ty), "B", font=f, fill=ink + (a,))
    bw = max(2, int(r * 0.13))
    for dx in (-r * 0.12, r * 0.14):
        cx = x + dx
        d.line([(cx, y - h / 2 - r * 0.22), (cx, y - h / 2 + r * 0.05)], fill=ink + (a,), width=bw)
        d.line([(cx, y + h / 2 - r * 0.05), (cx, y + h / 2 + r * 0.22)], fill=ink + (a,), width=bw)


class Peers(Beat):

    EMBLEM = False
    TRIP = 1.7          # seconds for a coin to cross one link
    COINS = 18          # coins in flight at once

    def __init__(self, title: str = "", label: str = "", **kw):
        super().__init__(**kw)
        self.title, self.label = title, label
        fr, p = self.frame, self.portrait
        rng = random.Random(2140)
        cols, rows = (3, 6) if p else (6, 3)
        top = self.head_y + (90 if p else 70)
        bottom = fr.h * (0.80 if p else 0.80)
        left, right = fr.w * 0.10, fr.w * 0.90
        self.nodes = []
        for j in range(rows):
            for i in range(cols):
                x = left + (right - left) * (i + 0.5 + rng.uniform(-0.28, 0.28)) / cols
                y = top + (bottom - top) * (j + 0.5 + rng.uniform(-0.28, 0.28)) / rows
                self.nodes.append((x, y))
        # each wallet linked to its three nearest neighbours
        edges = set()
        for a, (x, y) in enumerate(self.nodes):
            near = sorted(range(len(self.nodes)),
                          key=lambda b: (self.nodes[b][0] - x) ** 2 + (self.nodes[b][1] - y) ** 2)
            for b in near[1:4]:
                edges.add((min(a, b), max(a, b)))
        self.edges = sorted(edges)
        # a fixed schedule of trips: (start time offset, edge, direction)
        self.trips = []
        n = len(self.edges)
        for k in range(self.COINS * 12):
            e = self.edges[rng.randrange(n)]
            self.trips.append((k * self.TRIP / self.COINS + rng.uniform(0, 0.3),
                               e, rng.random() < 0.5))
        self.r_node = 18 if p else 15
        self.r_coin = 40 if p else 34

    def _coin(self, d, x, y, a):
        r = self.r_coin
        prim = self.brand.primary
        d.ellipse([x - r, y - r, x + r, y + r], fill=prim + (a,),
                  outline=(30, 24, 0, a), width=2)
        coin_sign(d, x, y, r, (25, 20, 0), a)

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        t = self.at(f) - self.start
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        prim = self.brand.primary
        enter = _smooth(t / 0.9)
        # links, drawn out from the first frame
        for (a, b) in self.edges:
            (x0, y0), (x1, y1) = self.nodes[a], self.nodes[b]
            q = enter
            d.line([(x0, y0), (x0 + (x1 - x0) * q, y0 + (y1 - y0) * q)],
                   fill=(120, 104, 40, int(190 * enter)), width=3)
        # landings, for the glint
        glint = [0.0] * len(self.nodes)
        for (t0, (a, b), rev) in self.trips:
            s = t - 0.6 - t0
            if s < 0 or s > self.TRIP + 0.5:
                continue
            src, dst = (b, a) if rev else (a, b)
            if s >= self.TRIP:
                glint[dst] = max(glint[dst], 1.0 - (s - self.TRIP) / 0.5)
        for k, (x, y) in enumerate(self.nodes):
            g = glint[k]
            r = self.r_node * (1 + 0.5 * g)
            col = tuple(int(70 + (c - 70) * (0.35 + 0.65 * g)) for c in prim)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(18, 18, 18, int(255 * enter)),
                      outline=col + (int(255 * enter),), width=3)
        # coins in flight
        for (t0, (a, b), rev) in self.trips:
            s = t - 0.6 - t0
            if s < 0 or s > self.TRIP:
                continue
            src, dst = (b, a) if rev else (a, b)
            q = s / self.TRIP
            q = q * q * (3 - 2 * q)
            (x0, y0), (x1, y1) = self.nodes[src], self.nodes[dst]
            fade = min(1.0, s / 0.15, (self.TRIP - s) / 0.15)
            self._coin(d, x0 + (x1 - x0) * q, y0 + (y1 - y0) * q, int(255 * fade))
        # the label, on the one reveal
        if self.label:
            rv = self.reveals or [self.start + 0.8]
            s = self.at(f) - rv[0]
            if s >= 0:
                la = _smooth(s / 0.5)
                lf = _display(52 if self.portrait else 46)
                lb = d.textbbox((0, 0), self.label, font=lf)
                w, h = lb[2] - lb[0], lb[3] - lb[1]
                cx = self.frame.w / 2
                cy = self.frame.h * (0.88 if self.portrait else 0.89)
                pad = 22
                d.rounded_rectangle([cx - w / 2 - pad, cy - h / 2 - pad * 0.7,
                                     cx + w / 2 + pad, cy + h / 2 + pad * 0.7],
                                    radius=10, fill=prim + (int(240 * la),))
                d.text((cx - w / 2 - lb[0], cy - h / 2 - lb[1]), self.label, font=lf,
                       fill=self.brand.band_ink + (int(255 * la),)
                       if isinstance(self.brand.band_ink, tuple) else (16, 16, 16, int(255 * la)))
        out.paste(layer, (0, 0), layer)
