"""`voice`: voices compared by ear - each row a voice, its waveform playing
as its example plays (2026-11-21, the OktAI opener).

payload: (rows,) with rows = [(label, note, sample), ...]

`sample` is a name registered with `core.samples.register` (the audio file
of that voice reading a line), played in the pause after the row's sentence
by the same cue that plays the tinnitus samples. A row with no sample is
the narration itself (Oktay, reading it): its strip moves while he speaks.

The playhead's clock is the sample cue's own: a sample ends `samples.LEAD`
before the next caption, which is the next row's reveal - so write one
caption per row's sentence, and give that sentence a gap long enough for
the clip (`Section.gaps`, at least the clip's length plus half a second).
"""

from __future__ import annotations


import numpy as np
from PIL import Image, ImageDraw

from ...core import samples
from ...core.draw import ease_out
from .base import Beat, _font

BARS = 64


class Voice(Beat):

    def __init__(self, rows, **kw):
        super().__init__(**kw)
        self.rows = [tuple(r) + (None,) * (3 - len(r)) for r in rows]
        self.env = [self._envelope(r[2]) for r in self.rows]

    @staticmethod
    def _envelope(name):
        if not name:
            return None
        key = f"sample_{name}"
        if key not in samples.MAKERS:
            return None
        x = np.abs(samples.MAKERS[key](samples.SR))
        bins = np.array_split(x, BARS)
        e = np.array([np.sqrt(np.mean(b ** 2)) if len(b) else 0 for b in bins])
        return e / (e.max() + 1e-9)

    def _window(self, i: int):
        """(start, end) in absolute seconds while row `i`'s clip plays."""
        name = self.rows[i][2]
        if not name or name not in samples.DUR:
            return None
        rv = self.reveals or []
        nxt = rv[i + 1] if i + 1 < len(rv) else self.start + self.hold
        end = nxt - samples.LEAD
        return end - samples.DUR[name], end

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        W, H = self.frame.size
        n = len(self.rows)
        x0 = self.margin
        full = W - 2 * x0
        if self.portrait:
            # A fixed top, so the rows stay put as a Short adds one per shot.
            row_h, top = 400, int(H * 0.20)
        else:
            row_h = min(260, int((H - 220) / max(n, 1)))
            top = int((H - row_h * n) / 2)
        t = self.at(f)
        big, small = _font(84 if self.portrait else 58), _font(42 if self.portrait else 30)
        for i, (label, note, _) in enumerate(self.rows):
            p = self.due(i, n, f)
            if p < 0:
                continue
            y = top + i * row_h + int((1 - p) * 14)
            a = int(255 * min(1.0, p))
            win = self._window(i)
            live = (win is not None and win[0] <= t <= win[1]) or (
                win is None and self.rows[i][2] is None and self._speaking(i, t))
            col = self.brand.primary if live else (235, 235, 240)
            if self.portrait:
                d.text((x0, y), label, font=big, fill=(*col, a))
                d.text((x0, y + 100), note, font=small, fill=(150, 150, 160, a))
                strip = (x0, y + 170, full, 170)
            else:
                lw = int(full * 0.42)
                d.text((x0, y + 30), label, font=big, fill=(*col, a))
                d.text((x0, y + 108), note, font=small, fill=(150, 150, 160, a))
                strip = (x0 + lw, y + 20, full - lw, row_h - 70)
            self._strip(d, strip, i, t, p)

    def _speaking(self, i: int, t: float) -> bool:
        rv = self.reveals or []
        if i >= len(rv):
            return False
        nxt = rv[i + 1] if i + 1 < len(rv) else self.start + self.hold
        return rv[i] <= t < nxt

    def _strip(self, d, box, i: int, t: float, p: float) -> None:
        x, y, w, h = box
        cy = y + h / 2
        env = self.env[i]
        win = self._window(i)
        if env is None:
            # The narration itself: a calm level that breathes while it is
            # spoken, flat otherwise.
            k = np.arange(BARS)
            on = self._speaking(i, t)
            env = 0.25 + 0.55 * np.abs(np.sin(k * 0.7 + t * 9.0) *
                                      np.sin(k * 0.23 + t * 3.1)) if on else \
                np.full(BARS, 0.06)
            head = 1.0 if on else 0.0
        else:
            head = 0.0 if win is None else min(1.0, max(0.0, (t - win[0]) /
                                                         (win[1] - win[0])))
        step = w / BARS
        bw = max(3, int(step * 0.55))
        grow = ease_out(min(1.0, max(0.0, p)))
        for k, v in enumerate(env):
            bx = x + k * step
            bh = max(4, v * h * 0.92 * grow)
            played = (k + 0.5) / BARS <= head
            colr = self.brand.primary if played else (90, 90, 100)
            d.rounded_rectangle([bx, cy - bh / 2, bx + bw, cy + bh / 2],
                                radius=bw // 2, fill=colr)
        if 0 < head < 1 and self.env[i] is not None:
            hx = x + head * w
            d.line([(hx, y - 6), (hx, y + h + 6)], fill=(255, 255, 255), width=3)
