"""`post` - a pulled-out post, headline or transaction, highlighted as read.

The documentary channels' most-used device (the editor's pick, 2026-10-22):
the thing someone actually wrote - a post, a news headline, an on-chain
transaction - lifted out of the video onto its own card, with the line that
matters highlighted as the voice reads it. Three kinds, one grammar:

* `"post"` - a social post: avatar, name, handle, date, the text.
* `"headline"` - a news clipping: masthead, a serif headline, date, a
  standfirst, on paper.
* `"tx"` - a transaction: rows of monospace fields (hash, from, to, value,
  block), one of them the point.
* `"letter"` - a line from a letter (2026-10-24): on paper, the writer and
  recipient over a hairline, the quoted line in Georgia, the place and date
  under it. Built for Beethoven's 1801 letter to Wegeler, which as a `post`
  read as a social feed and as a `headline` as a newspaper.

**Our card, not a platform's interface.** It is drawn in the channel's own
type and colours and carries the source line the script gives it. It quotes;
it does not imitate a screenshot - so `fields` must be the real wording,
sourced like any other quote in the script.

**The move.** The card floats in over the moving dot grid, tilted a little in
depth and settling flat (a perspective warp, not a slide). On reveal 1 the
`[bracketed]` part of the text - or the tx row marked `"*"` - is swept by a
highlighter in `Brand.band`, its words turning `band_ink` as it passes, and
the camera pushes in toward it.

payload: (kind, fields, title) - `fields` is a dict:

    post:     name, handle, date, text, avatar (image path, optional)
    headline: source, headline, date, text (optional)
    tx:       label (optional), rows [(key, value), ...]; a key starting
              with "*" is the highlighted row
    letter:   name, to, text, date, avatar (image path, optional)
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ...core.draw import cover, ease_out
from .base import Beat, _smooth

SF = "/System/Library/Fonts/SFNS.ttf"
SERIF = "/System/Library/Fonts/NewYork.ttf"
# The letter's line. New York italic was the first pick and the editor found it
# hard to read on a phone: at display size it takes its high-contrast optical
# cut, hairlines vanish and the italic joins up. Georgia was drawn for
# screens; Charter was tried too and showed seams inside the highlight.
LETTER = "/System/Library/Fonts/Supplemental/Georgia.ttf"
MONO = "/System/Library/Fonts/SFNSMono.ttf"

PAPER = (238, 233, 222)
CARD = (246, 246, 247)
INK = (22, 22, 24)
MUTED = (110, 112, 118)


def _font(path: str, size: int, weight: str | None = None):
    f = ImageFont.truetype(path, size)
    if weight:
        try:
            f.set_variation_by_name(weight)
        except Exception:
            pass
    return f


def _words(text: str) -> list[tuple[str, bool]]:
    """`"a [b c] d"` -> [("a", False), ("b", True), ("c", True), ("d", False)]."""
    out = []
    for chunk in re.split(r"(\[[^\]]*\])", text):
        mark = chunk.startswith("[")
        for w in chunk.strip("[]").split():
            out.append((w, mark))
    return out


class Post(Beat):
    ARRIVE = 0.75           # float-in and settle
    SWEEP = 0.85            # the highlighter across the marked run
    PUSH = 1.30             # the camera's push toward it
    PUSH_TO = 1.16          # how far in

    def __init__(self, kind: str, fields: dict, title: str = "", **kw):
        super().__init__(**kw)
        self.kind, self.fields, self.title = kind, dict(fields), title
        W, H = self.frame.size
        self.card_w = int(W * (0.88 if self.portrait else 0.60))
        # Type scale against an 1100px card - and a narrower reference in
        # 9:16, so a phone gets bigger type, not the desktop's shrunk.
        self.s = self.card_w / (780.0 if self.portrait else 1100.0)
        self._avatar = None
        av = self.fields.get("avatar")
        if av and Path(av).exists():
            d = int(96 * self.s)
            im = cover(Image.open(av).convert("RGB"), d, d)
            mask = Image.new("L", (d, d), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, d - 1, d - 1], fill=255)
            im.putalpha(mask)
            self._avatar = im

    # --- timing -----------------------------------------------------------

    def _times(self) -> tuple[float, float]:
        rv = list(self.reveals or [])
        arrive = rv[0] if rv else self.start + 0.1
        mark = rv[1] if len(rv) > 1 else self.start + self.hold * 0.45
        return arrive, mark

    # --- the card ---------------------------------------------------------

    def _paint_words(self, d, words, font, x0, y, width, line_h, sweep,
                     ink, hi_fill, hi_ink):
        """Wrap and draw `words`; the marked run is highlighted up to
        `sweep` (0..1 of its total width). Returns the y below the text."""
        space = d.textlength(" ", font=font)
        lines, cur, cw = [], [], 0.0
        for w, m in words:
            ww = d.textlength(w, font=font)
            if cur and cw + space + ww > width:
                lines.append(cur)
                cur, cw = [], 0.0
            cur.append((w, m, ww))
            cw += (space if len(cur) > 1 else 0) + ww
        if cur:
            lines.append(cur)

        marked = sum(ww + space for ln in lines for w, m, ww in ln if m)
        done = marked * sweep
        asc = font.getbbox("Hg")
        pad = int(line_h * 0.10)
        self._mark_box = None
        for ln in lines:
            x = x0
            for w, m, ww in ln:
                fill = ink
                if m and done > 0:
                    run = min(ww + space, done)
                    hx0, hx1 = x - pad * 0.6, x + run - space * 0.4
                    if hx1 > hx0:            # the sweep's first sliver
                        d.rectangle([hx0, y + asc[1] - pad,
                                     hx1, y + asc[3] + pad], fill=hi_fill)
                    if run >= ww * 0.6:
                        fill = hi_ink
                    done -= ww + space
                if m:
                    bx = (x, y, x + ww, y + line_h)
                    mb = self._mark_box
                    self._mark_box = bx if mb is None else (
                        min(mb[0], bx[0]), min(mb[1], bx[1]),
                        max(mb[2], bx[2]), max(mb[3], bx[3]))
                d.text((x, y), w, font=font, fill=fill)
                x += ww + space
            y += line_h
        return y

    def _card(self, sweep: float) -> Image.Image:
        s, W = self.s, self.card_w
        f = self.fields
        hi_fill = self.brand.band or self.brand.primary
        hi_ink = self.brand.band_ink
        pad = int(64 * s)
        H = int(W * 1.4)                        # cropped to content below
        bg = PAPER if self.kind in ("headline", "letter") else CARD
        im = Image.new("RGB", (W, H), bg)
        d = ImageDraw.Draw(im)
        self._mark_box = None
        y = pad

        if self.kind == "post":
            x = pad
            if self._avatar is not None:
                im.paste(self._avatar, (x, y), self._avatar)
                x += self._avatar.width + int(24 * s)
            else:
                r = int(48 * s)
                d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=hi_fill)
                ini = (f.get("name") or "?")[:1].upper()
                fi = _font(SF, int(44 * s), "Bold")
                bb = d.textbbox((0, 0), ini, font=fi)
                d.text((x + r - (bb[0] + bb[2]) / 2, y + r - (bb[1] + bb[3]) / 2),
                       ini, font=fi, fill=hi_ink)
                x += 2 * r + int(24 * s)
            d.text((x, y + int(6 * s)), f.get("name", ""),
                   font=_font(SF, int(40 * s), "Bold"), fill=INK)
            sub = " · ".join(v for v in (f.get("handle"), f.get("date")) if v)
            d.text((x, y + int(54 * s)), sub,
                   font=_font(SF, int(32 * s), "Regular"), fill=MUTED)
            y += int(140 * s)
            y = self._paint_words(d, _words(f.get("text", "")),
                                  _font(SF, int(50 * s), "Medium"), pad, y,
                                  W - 2 * pad, int(68 * s), sweep, INK,
                                  hi_fill, hi_ink)

        elif self.kind == "headline":
            src = (f.get("source") or "").upper()
            d.text((pad, y), src, font=_font(SERIF, int(36 * s), "Bold"),
                   fill=INK)
            y += int(56 * s)
            d.line([(pad, y), (W - pad, y)], fill=INK, width=max(2, int(3 * s)))
            y += int(34 * s)
            y = self._paint_words(d, _words(f.get("headline", "")),
                                  _font(SERIF, int(66 * s), "Bold"), pad, y,
                                  W - 2 * pad, int(80 * s), sweep, INK,
                                  hi_fill, hi_ink)
            if f.get("text"):
                y += int(10 * s)
                y = self._paint_words(d, _words(f["text"]),
                                      _font(SERIF, int(36 * s), "Regular"),
                                      pad, y, W - 2 * pad, int(50 * s), 0.0,
                                      (60, 58, 54), hi_fill, hi_ink)
            if f.get("date"):
                y += int(12 * s)
                d.text((pad, y), f["date"],
                       font=_font(SF, int(28 * s), "Medium"), fill=MUTED)
                y += int(40 * s)

        elif self.kind == "letter":
            x = pad
            if self._avatar is not None:
                im.paste(self._avatar, (x, y), self._avatar)
                x += self._avatar.width + int(24 * s)
            d.text((x, y + int(6 * s)), f.get("name", ""),
                   font=_font(SERIF, int(40 * s), "Bold"), fill=INK)
            if f.get("to"):
                d.text((x, y + int(56 * s)), f["to"],
                       font=_font(SF, int(30 * s), "Regular"), fill=MUTED)
            y += int(124 * s) if self._avatar is not None else int(104 * s)
            d.line([(pad, y), (W - pad, y)], fill=(196, 188, 172),
                   width=max(1, int(2 * s)))
            y += int(40 * s)
            y = self._paint_words(d, _words(f.get("text", "")),
                                  _font(LETTER, int(54 * s)),
                                  pad, y, W - 2 * pad, int(76 * s), sweep,
                                  INK, hi_fill, hi_ink)
            if f.get("date"):
                y += int(18 * s)
                d.text((pad, y), f["date"],
                       font=_font(LETTER, int(30 * s)),
                       fill=MUTED)
                y += int(40 * s)

        else:                                    # tx
            if f.get("label"):
                d.text((pad, y), f["label"].upper(),
                       font=_font(SF, int(30 * s), "Bold"), fill=MUTED)
                y += int(58 * s)
            kf = _font(SF, int(30 * s), "Semibold")
            vf = _font(MONO, int(34 * s))
            row_h = int(70 * s)
            for key, val in f.get("rows", []):
                star = key.startswith("*")
                key = key.lstrip("*")
                d.text((pad, y + int(14 * s)), key.upper(), font=kf, fill=MUTED)
                vx = pad + int(220 * s)
                if star:
                    tw = d.textlength(val, font=vf)
                    run = tw * sweep
                    if run > 1:
                        d.rectangle([vx - 8 * s, y + 4 * s, vx + run + 8 * s,
                                     y + row_h - 8 * s], fill=hi_fill)
                    self._mark_box = (vx, y, vx + tw, y + row_h)
                d.text((vx, y + int(12 * s)), val, font=vf,
                       fill=hi_ink if star and sweep > 0.6 else INK)
                y += row_h
                d.line([(pad, y - 2), (W - pad, y - 2)], fill=(222, 222, 226),
                       width=1)

        y += pad
        im = im.crop((0, 0, W, min(H, y)))
        # Rounded corners on the card.
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, im.width - 1, im.height - 1], radius=int(26 * s), fill=255)
        im.putalpha(mask)
        return im

    # --- the frame --------------------------------------------------------

    @staticmethod
    def _warp(card: Image.Image, angle: float, scale: float,
              centre: tuple[float, float], anchor: tuple[float, float],
              size: tuple[int, int]) -> Image.Image:
        """The card rotated `angle` degrees about its vertical axis, scaled,
        and placed so its point `anchor` lands on `centre`."""
        w, h = card.size
        a = math.radians(angle)
        f = w * 2.2                              # focal length: a gentle lens
        pts = []
        for x, y in ((0, 0), (w, 0), (w, h), (0, h)):
            X, Y = (x - w / 2), (y - h / 2)
            Z = X * math.sin(a)
            X = X * math.cos(a)
            k = f / (f + Z)
            pts.append((X * k, Y * k))
        ax = (anchor[0] - w / 2) * math.cos(a)
        az = (anchor[0] - w / 2) * math.sin(a)
        ka = f / (f + az)
        off = (ax * ka, (anchor[1] - h / 2) * ka)
        dst = np.float32([(centre[0] + (px - off[0]) * scale,
                           centre[1] + (py - off[1]) * scale) for px, py in pts])
        src = np.float32([(0, 0), (w, 0), (w, h), (0, h)])
        m = cv2.getPerspectiveTransform(src, dst)
        out = cv2.warpPerspective(np.asarray(card), m, size,
                                  flags=cv2.INTER_LINEAR,
                                  borderMode=cv2.BORDER_CONSTANT,
                                  borderValue=(0, 0, 0, 0))
        return Image.fromarray(out)

    def content(self, out: Image.Image, f: float) -> None:
        from .reel import dot_grid

        W, H = self.frame.size
        t = self.at(f)
        arrive, mark = self._times()
        ap = _smooth(min(1.0, max(0.0, (t - arrive + 0.05) / self.ARRIVE)))
        if ap <= 0.0:
            dot_grid(out, 0.0, 1.0, self.brand, self.frame)
            return
        sweep = _smooth(min(1.0, max(0.0, (t - mark) / self.SWEEP)))
        push = _smooth(min(1.0, max(0.0, (t - mark + 0.1) / self.PUSH)))

        card = self._card(sweep)
        cw, ch = card.size
        # Where the camera looks: the card's centre, drifting to the marked
        # run as it pushes in.
        tx, ty = cw / 2, ch / 2
        if self._mark_box is not None:
            mx = (self._mark_box[0] + self._mark_box[2]) / 2
            my = (self._mark_box[1] + self._mark_box[3]) / 2
            # Mostly vertical: steering hard sideways toward a highlight at
            # one end of a line slid the whole card off a 9:16 frame.
            tx += (mx - tx) * push * 0.25
            ty += (my - ty) * push * 0.5
        drift = (t - arrive) * 0.012
        zoom = (0.94 + 0.06 * ap) * (1.0 + (self.PUSH_TO - 1.0) * push) + drift
        # The card always fits the width, with a margin...
        zoom = min(zoom, W * 0.94 / cw)
        # ...and is never pushed past either edge.
        left = W / 2 - tx * zoom
        if left < W * 0.03:
            tx = (W / 2 - W * 0.03) / zoom
        elif left + cw * zoom > W * 0.97:
            tx = (W / 2 - (W * 0.97 - cw * zoom)) / zoom
        angle = 14.0 * (1.0 - ap) + 3.0 * (1.0 - push)
        cy = H * (0.54 if self.title else 0.50) + 40 * (1.0 - ap)

        dot_grid(out, (t - self.start) * 18.0, zoom * 0.9, self.brand,
                 self.frame)
        warped = self._warp(card, angle, zoom, (W / 2, cy), (tx, ty),
                            (W, H))
        if ap < 1.0:
            warped.putalpha(warped.getchannel("A").point(
                lambda v: int(v * ap)))
        sh = warped.getchannel("A")
        q = 4
        small = sh.resize((W // q, H // q), Image.BILINEAR).filter(
            ImageFilter.GaussianBlur(max(2, int(W * 0.012 / q))))
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        shadow.putalpha(small.resize((W, H), Image.BILINEAR).point(
            lambda v: int(v * 0.75)))
        layer = out.convert("RGBA")
        layer.alpha_composite(shadow, (0, int(18 * self.s)))
        layer.alpha_composite(warped)
        out.paste(layer.convert("RGB"))
        if self.title:
            self.heading(out, self.title, f)
