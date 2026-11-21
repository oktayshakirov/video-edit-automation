"""`wall`: a grid of other beats, each playing in its own tile - the library
shown off in one shot (2026-11-21, the OktAI opener's graphics chapter: "we
need to be more visual, more examples").

payload: (tiles, title) with tiles = [(graphic, payload), ...], up to six.

Each tile is a real beat from `BEATS`, drawn at full size with its own
payload and scaled into the grid, so what the viewer sees is exactly what a
video of ours shows. A tile arrives on its own caption chunk (write one chunk
per tile, or the tiles share the sentence's first) and plays its animation
from that moment for `PLAY` seconds, then holds its last frame - which is
also what stops a six-tile wall costing six beats on every frame.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out
from ...core.frame import LANDSCAPE
from .base import Beat

PLAY = 4.5             # seconds a tile's own animation runs
GAP = 26


class Wall(Beat):

    def __init__(self, tiles, title: str = "", **kw):
        super().__init__(**kw)
        self.title = title
        self.specs = list(tiles)[:6]
        self._inner = [None] * len(self.specs)
        self._still = [None] * len(self.specs)

    def _tile(self, i: int, start: float):
        if self._inner[i] is None:
            from . import BEATS, item_count
            graphic, payload = self.specs[i]
            n = item_count(graphic, payload)
            rv = [start + 0.3 + k * min(0.45, 2.8 / max(n, 1)) for k in range(n)]
            self._inner[i] = BEATS[graphic](*payload, brand=self.brand, frame=LANDSCAPE,
                                            reveals=rv or None, start=start, hold=PLAY,
                                            emblem="arcs")
        return self._inner[i]

    def _grid(self):
        W, H = self.frame.size
        n = len(self.specs)
        cols = 2 if (self.portrait or n <= 4) else 3
        rows = (n + cols - 1) // cols
        top = self.head_y + (40 if self.title else 0)
        avail_w = W - 2 * self.margin
        avail_h = H - top - self.margin
        tw = (avail_w - GAP * (cols - 1)) / cols
        th = tw * 9 / 16
        if th * rows + GAP * (rows - 1) > avail_h:
            th = (avail_h - GAP * (rows - 1)) / rows
            tw = th * 16 / 9
        x0 = (W - (tw * cols + GAP * (cols - 1))) / 2
        y0 = top + (avail_h - (th * rows + GAP * (rows - 1))) / 2
        return [(int(x0 + (i % cols) * (tw + GAP)), int(y0 + (i // cols) * (th + GAP)),
                 int(tw), int(th)) for i in range(n)]

    def content(self, out: Image.Image, f: float) -> None:
        if self.title:
            self.heading(out, self.title, f)
        t = self.at(f)
        rv = self.reveals or []
        d = ImageDraw.Draw(out, "RGBA")
        for i, (x, y, w, h) in enumerate(self._grid()):
            start = rv[i] if i < len(rv) else self.start + 0.4 * i
            if t < start:
                continue
            p = ease_out(min(1.0, (t - start) / 0.35))
            if self._still[i] is not None:
                pic = self._still[i]
            else:
                inner = self._tile(i, start)
                fi = min(1.0, (t - start) / PLAY)
                pic = inner.draw(fi).convert("RGB").resize((w, h), Image.LANCZOS)
                if fi >= 1.0:
                    self._still[i] = pic
            if p < 1.0:
                s = 0.92 + 0.08 * p
                sw, sh = int(w * s), int(h * s)
                pic2 = pic.resize((sw, sh), Image.BILINEAR)
                mask = Image.new("L", (sw, sh), int(255 * p))
                out.paste(pic2, (x + (w - sw) // 2, y + (h - sh) // 2), mask)
            else:
                out.paste(pic, (x, y))
            d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                                outline=self.brand.primary + (int(200 * p),), width=3)
