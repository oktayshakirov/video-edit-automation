"""`phones`: vertical videos playing side by side in phone frames - our own
Shorts shown as Shorts (2026-11-21, the OktAI opener: "more examples").

payload: (items, title) with items = [(clip, label, note), ...], up to three.

A 9:16 clip in a 16:9 card loses its top and bottom, which is where a Short
keeps its hook and its captions; a phone keeps all of it. Each phone arrives
on its own caption chunk and plays its clip from 0 (or `offset`, a fourth
value) for as long as the shot holds, looping. `label` sits under the phone
in the brand's colour (the number that matters - "half gone at 7.1s"),
`note` under it in grey. A missing file draws an empty phone with its label,
so a draft shows the layout before the clips exist.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from ...core.draw import ease_out
from .base import Beat, _font
from .reel import _Media


class Phones(Beat):

    def __init__(self, items, title: str = "", **kw):
        super().__init__(**kw)
        self.title = title
        self.items = []
        for it in list(items)[:3]:
            clip, label, note, off = (tuple(it) + ("", "", 0.0))[:4]
            self.items.append((_Media(clip if clip and Path(str(clip)).exists() else None,
                                      float(off or 0.0)), label or "", note or ""))

    def content(self, out: Image.Image, f: float) -> None:
        W, H = self.frame.size
        top = self.heading(out, self.title, f) if self.title else self.head_y
        n = len(self.items)
        # Landscape leaves the bottom band to the subtitles: the notes under
        # the phones ran into them (OktAI, 2026-11-23).
        ph = int((H - top - 300) if not self.portrait else H * 0.34)
        pw = int(ph * 9 / 19.5 + ph * 0.06)
        gap = int(pw * (0.45 if n == 2 else 0.25))
        total = n * pw + (n - 1) * gap
        x0 = (W - total) // 2
        y0 = top + (40 if not self.portrait else 120)
        d = ImageDraw.Draw(out, "RGBA")
        lab_f, note_f = _font(44 if not self.portrait else 52), _font(28 if not self.portrait else 34)
        t = self.at(f)
        rv = self.reveals or []
        for i, (media, label, note) in enumerate(self.items):
            start = rv[i] if i < len(rv) else self.start
            if t < start:
                continue
            p = ease_out(min(1.0, (t - start) / 0.35))
            x = x0 + i * (pw + gap)
            y = y0 + int((1 - p) * 24)
            bez = int(pw * 0.045)
            r = int(pw * 0.13)
            d.rounded_rectangle([x, y, x + pw, y + ph], radius=r,
                                fill=(18, 18, 22, int(255 * p)),
                                outline=self.brand.primary + (int(200 * p),), width=3)
            sx, sy, sw, sh = x + bez, y + bez, pw - 2 * bez, ph - 2 * bez
            frame = media.raw(max(0.0, t - start))
            if frame is not None:
                im = Image.fromarray(frame)
                # Cover the screen at 9:19.5, centred: a 9:16 Short loses a
                # sliver at the sides, never its top or bottom.
                s = max(sw / im.width, sh / im.height)
                im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.BILINEAR)
                cx, cy = (im.width - sw) // 2, (im.height - sh) // 2
                im = im.crop((cx, cy, cx + sw, cy + sh))
                mask = Image.new("L", (sw, sh), 0)
                ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=r - bez,
                                                       fill=int(255 * p))
                out.paste(im, (sx, sy), mask)
            if label:
                d.text((x + pw // 2, y + ph + 22), label, font=lab_f, anchor="ma",
                       fill=self.brand.primary + (int(255 * p),))
            if note:
                d.text((x + pw // 2, y + ph + 22 + int(lab_f.size * 1.25)), note,
                       font=note_f, anchor="ma", fill=(170, 170, 180, int(255 * p)))
