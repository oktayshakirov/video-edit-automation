"""`ponzi` - who pays whom: the same three cards with and without someone in
the middle.

**Built for `is-bitcoin-a-ponzi` (2026-11-25), because the pair's whole
argument is one picture drawn twice**: in a Ponzi scheme the money runs
through someone in the middle - new investors pay in, the operator pays the
earlier ones their "returns" out of it, and when the new money stops the
payouts stop. In a market, the buyer's money goes to whoever sold, and the
middle card is empty. `reserve` is a deposit lent on, `pile` is money
pooling, `pool` is a trading pool, `diagram` is a chain of words; none of
them shows money passing *through* a middle that is then taken away.
Reusable for any "is it a Ponzi?" claim - a yield product, a referral
scheme, an exchange paying "interest" from deposits.

Three cards in a row (portrait: stacked), left to right: who is paid,
the middle, who pays in. Three reveals, three caption chunks.

`mode="ponzi"`:
  1. in - coins stream from the right card into the middle, for good;
  2. out - coins stream from the middle to the left card, `label` over
     the lane ("'RETURNS'");
  3. stop - the inflow is crossed out and dries up, the outflow dries up
     after it, the middle card turns to `$0` with `verdict` ("COLLAPSES").

`mode="market"`:
  The middle card is drawn dashed and dim from the start - nobody is in it.
  1. the trade - `$` coins run from the right card straight through the
     empty middle to the left one, and `coin` chips run back;
  2. `label` sets on the middle card ("HOLDS NO MONEY");
  3. `verdict` sets under it ("PROMISES NO RETURN").

payload: (mode, left, middle, right, label, verdict, title[, coin])
  left, middle, right  (name, sub)
  label    ponzi: the returns lane's word; market: the middle card's line
  verdict  ponzi: the middle card's last line; market: its second line
  title    the beat's kicker
  coin     market only, the chip that comes back ("BTC")

Portrait-safe. Cues: `pan` on the first two reveals, `cross` on the
collapse (ponzi) or `reveal` on the lines (market) - `flow_times`.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth


def flow_times(rv: list[float], mode: str = "ponzi") -> dict:
    """When the sounds land, from the beat's own reveals."""
    out = {}
    if rv:
        out["first"] = rv[0]
    if len(rv) > 1:
        out["second"] = rv[1]
    if len(rv) > 2:
        out["third"] = rv[2] + (0.55 if mode == "ponzi" else 0.25)
    return out


class Ponzi(Beat):

    EMBLEM = False
    PERIOD = 1.3        # seconds for one coin to cross a lane
    COINS = 4           # coins in a lane at once

    def __init__(self, mode: str, left: tuple, middle: tuple, right: tuple,
                 label: str, verdict: str, title: str = "",
                 coin: str = "BTC", **kw):
        super().__init__(**kw)
        if mode not in ("ponzi", "market"):
            raise ValueError(f"ponzi mode {mode!r} - 'ponzi' or 'market'")
        self.mode = mode
        self.left, self.middle, self.right = tuple(left), tuple(middle), tuple(right)
        self.label, self.verdict, self.title, self.coin = label, verdict, title, coin
        fr, p = self.frame, self.portrait
        if p:
            cw, ch = fr.w - 2 * 140, 280
            x = 140
            top = self.head_y + 110
            gap = (int(fr.h * 0.86) - top - 3 * ch) // 2
            self.cards = [(x, top + i * (ch + gap), x + cw, top + i * (ch + gap) + ch)
                          for i in range(3)]
        else:
            cw, ch = 390, 260
            gap = (fr.w - 2 * self.margin - 3 * cw) // 2
            top = (self.head_y + fr.h - ch) // 2 + 10
            x0 = self.margin
            self.cards = [(x0 + i * (cw + gap), top, x0 + i * (cw + gap) + cw, top + ch)
                          for i in range(3)]
        self._d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        self._fit_cache: dict = {}
        cw = self.cards[0][2] - self.cards[0][0]
        nf, sf, _ = self._fonts()
        lines = [self.left[0], self.middle[0], self.right[0]]
        if mode == "ponzi":
            lines.append(self.verdict)
        for txt in lines:
            if txt and self._fit(txt, nf.size, cw - 50).size < nf.size * 0.66:
                raise ValueError(f"ponzi label {txt!r} is too wide for a card")
        for _, sub in (self.left, self.middle, self.right):
            if self._d.textlength(sub, font=sf) > cw - 40:
                raise ValueError(f"ponzi card line {sub!r} is too wide")
        if mode == "ponzi":
            room = self.cards[1][0] - self.cards[0][2] if not p else cw
            if self._d.textlength(self.label, font=self._lane_font()) > room + 60:
                raise ValueError(f"ponzi lane label {self.label!r} is too wide")

    def _fit(self, text: str, size: int, maxw: float):
        key = (text, size, int(maxw))
        if key not in self._fit_cache:
            f = _display(size)
            while size > 12 and self._d.textlength(text, font=f) > maxw:
                size -= 1
                f = _display(size)
            self._fit_cache[key] = f
        return self._fit_cache[key]

    def _fonts(self):
        p = self.portrait
        return (_display(46 if p else 40), _font(30 if p else 27),
                _display(84 if p else 66))

    def _lane_font(self):
        return _display(36 if self.portrait else 27)

    # --- clocks -------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (i / 3) * 0.85)
        return self.at(f) - when

    # --- geometry -----------------------------------------------------------

    def _lane(self, a: int, b: int, off: float = 0.0):
        """From card `a` to card `b` (adjacent or not), at offset `off` from
        the cards' centre line."""
        A, B = self.cards[a], self.cards[b]
        if self.portrait:
            cx = (A[0] + A[2]) / 2 + off
            if a < b:
                return (cx, A[3]), (cx, B[1])
            return (cx, A[1]), (cx, B[3])
        cy = (A[1] + A[3]) / 2 + off
        if a < b:
            return (A[2], cy), (B[0], cy)
        return (A[0], cy), (B[2], cy)

    @staticmethod
    def _along(p0, p1, q: float):
        return (p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q)

    # --- pieces -------------------------------------------------------------

    def _card(self, d, box, name, sub, enter, lit, figure="", fig_col=None,
              lines=(), dashed=False):
        br = self.brand
        x0, y0, x1, y1 = box
        a = int(255 * enter)
        mx = (x0 + x1) / 2
        if dashed:
            col = (110, 110, 110, int(200 * enter))
            pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                                  (x0, y0), (mx + 0.5, y0)], 26, seg=10)
            dash, on, run = 18.0, True, 0.0
            for (ax, ay), (bx, by) in zip(pts, pts[1:]):
                seg = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5
                pos = 0.0
                while pos < seg:
                    step = min(dash - run, seg - pos)
                    if on:
                        q0, q1 = pos / seg, (pos + step) / seg
                        d.line([(ax + (bx - ax) * q0, ay + (by - ay) * q0),
                                (ax + (bx - ax) * q1, ay + (by - ay) * q1)],
                               fill=col, width=4)
                    pos += step
                    run += step
                    if run >= dash - 1e-6:
                        run, on = 0.0, not on
        else:
            d.rounded_rectangle(box, radius=26, fill=(14, 14, 14, int(236 * enter)))
            pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                                  (x0, y0), (mx + 0.5, y0)], 26, seg=10)
            edge = tuple(int(90 + (c - 90) * lit) for c in br.primary)
            if lit < 0:            # the collapse: the edge goes negative
                edge = br.negative
            partial(d, pts, max(0.001, _smooth(enter)), edge, 4)
        nf0, sf, ff = self._fonts()
        name_col = (130, 130, 130) if dashed else br.primary
        nf = self._fit(name, nf0.size, x1 - x0 - 50)
        nb = d.textbbox((0, 0), name, font=nf)
        d.text((mx - (nb[2] - nb[0]) / 2 - nb[0], y0 + 30), name, font=nf,
               fill=name_col + (a,))
        sb = d.textbbox((0, 0), sub, font=sf)
        d.text((mx - (sb[2] - sb[0]) / 2 - sb[0], y0 + 84), sub, font=sf,
               fill=(160, 160, 160, a))
        if figure:
            fb = d.textbbox((0, 0), figure, font=ff)
            fy = y0 + (118 if self.portrait else 104)
            shadow_text(d, (mx - (fb[2] - fb[0]) / 2 - fb[0], fy), figure, ff,
                        (fig_col or br.ink) + (a,), alpha=a)
        # lines from the bottom up: (text, colour, alpha)
        step = 56 if self.portrait else 54
        for k, (txt, col, la) in enumerate(reversed([l for l in lines if l[0]])):
            if la <= 0:
                continue
            lf = self._fit(txt, nf0.size - 4, x1 - x0 - 44)
            lb = d.textbbox((0, 0), txt, font=lf)
            ly = y1 - (68 if self.portrait else 54) - k * step
            d.text((mx - (lb[2] - lb[0]) / 2 - lb[0], ly + 10 * (1 - la)), txt,
                   font=lf, fill=col + (int(255 * la),))

    def _coin(self, d, x, y, a, col):
        r = 23
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,),
                  outline=(20, 20, 20, a), width=2)
        f = _display(30)
        b = d.textbbox((0, 0), "$", font=f)
        d.text((x - (b[2] - b[0]) / 2 - b[0], y - (b[3] - b[1]) / 2 - b[1]), "$",
               font=f, fill=(25, 25, 25, a))

    def _chip(self, d, x, y, a, text):
        f = _display(26 if self.portrait else 24)
        b = d.textbbox((0, 0), text, font=f)
        w, h = b[2] - b[0], b[3] - b[1]
        d.rounded_rectangle([x - w / 2 - 14, y - h / 2 - 10, x + w / 2 + 14,
                             y + h / 2 + 10], radius=10, fill=(232, 232, 232, a))
        d.text((x - w / 2 - b[0], y - h / 2 - b[1]), text, font=f,
               fill=(18, 18, 18, a))

    def _stream(self, d, p0, p1, t: float, stop: float | None, draw):
        """Coins along p0->p1, `t` seconds into the stream. With `stop` set
        (on the same clock), no coin is born after it and the lane empties."""
        if t < 0:
            return
        per, n = self.PERIOD, self.COINS
        for k in range(n):
            first = k * per / n
            if t < first:
                continue
            born = first + ((t - first) // per) * per
            if stop is not None and born > stop:
                if stop < first:
                    continue
                born = first + ((stop - first) // per) * per
            age = t - born
            if age > per:
                continue
            q = age / per
            fade = min(1.0, q / 0.1, (1 - q) / 0.1)
            x, y = self._along(p0, p1, q)
            draw(d, x, y, int(255 * max(0.0, fade)))

    # --- the frame ----------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        s0 = self._since(0, f)
        if s0 < 0:
            return
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        s1, s2 = self._since(1, f), self._since(2, f)
        enter = min(1.0, max(0.0, s0 / 0.6))
        if self.mode == "ponzi":
            self._ponzi(d, f, s0, s1, s2, enter)
        else:
            self._market(d, f, s0, s1, s2, enter)
        rise = int(22 * (1 - ease_out(enter)))
        out.paste(layer, (0, rise), layer)

    def _ponzi(self, d, f, s0, s1, s2, enter):
        br = self.brand
        prim, neg = br.primary, br.negative
        grey = (95, 95, 95)
        inl = self._lane(2, 1)
        outl = self._lane(1, 0)
        lp = _smooth((s0 - 0.15) / 0.5)
        partial(d, list(inl), lp, grey, 5)
        partial(d, list(outl), lp, grey, 5)
        # 1. in, for good - until the collapse (0.3s into reveal 3).
        self._stream(d, *inl, s0 - 0.25, (s0 - s2) + 0.05 if s2 >= 0 else None,
                     lambda dd, x, y, a: self._coin(dd, x, y, a, prim))
        # 2. out, labelled - it dries up ~0.8s after the inflow.
        if s1 >= 0:
            partial(d, list(outl), _smooth(s1 / 0.4), prim, 4)
            # it dries up ~0.8s after the inflow
            self._stream(d, *outl, s1 - 0.2,
                         (s1 - s2) + 0.9 if s2 >= 0 else None,
                         lambda dd, x, y, a: self._coin(dd, x, y, a, prim))
            la = _smooth(s1 / 0.5)
            lf = self._lane_font()
            (x0, y0), (x1, y1) = outl
            lb = d.textbbox((0, 0), self.label, font=lf)
            if self.portrait:
                lx = (x0 + x1) / 2 + 60
                ly = (y0 + y1) / 2 - (lb[3] - lb[1]) / 2 - lb[1]
            else:
                lx = (x0 + x1) / 2 - (lb[2] - lb[0]) / 2 - lb[0]
                ly = y0 - 70
            d.text((lx, ly), self.label, font=lf, fill=prim + (int(255 * la),))
        # 3. the collapse: a cross on the inflow, the middle to $0.
        collapse = 0.0
        if s2 >= 0:
            (x0, y0), (x1, y1) = inl
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2
            q = _smooth((s2 - 0.3) / 0.35)
            xs = 26
            partial(d, [(mx - xs, my - xs), (mx + xs, my + xs)], max(0.001, q), neg, 9)
            partial(d, [(mx + xs, my - xs), (mx - xs, my + xs)],
                    max(0.001, _smooth((s2 - 0.5) / 0.3)), neg, 9)
            collapse = _smooth((s2 - 1.1) / 0.4)
        A, B, C = self.cards
        self._card(d, A, *self.left, enter, 1.0 if s1 >= 0 else 0.4)
        self._card(d, B, *self.middle, enter,
                   -1 if collapse > 0.5 else (1.0 if s0 >= 0.3 else 0.4),
                   figure="$0" if collapse > 0.5 else "",
                   fig_col=neg, lines=[(self.verdict, neg, collapse)])
        self._card(d, C, *self.right, enter, 0.4 if s2 >= 0 else 1.0)

    def _market(self, d, f, s0, s1, s2, enter):
        br = self.brand
        prim = br.primary
        grey = (95, 95, 95)
        money = self._lane(2, 0, 22 if not self.portrait else -345)
        back = self._lane(0, 2, 80 if not self.portrait else 345)
        lp = _smooth((s0 - 0.15) / 0.6)
        partial(d, list(money), lp, grey, 4)
        partial(d, list(back), lp, grey, 4)
        A, B, C = self.cards
        # the middle first, so the trade passes over the empty card
        self._card(d, B, *self.middle, enter, 0.3, dashed=True)
        lf = _display(34 if self.portrait else 38)
        mx = (B[0] + B[2]) / 2
        for k, (txt, s) in enumerate(((self.label, s1), (self.verdict, s2))):
            if s < 0 or not txt:
                continue
            la = _smooth(s / 0.5)
            lb = d.textbbox((0, 0), txt, font=lf)
            if self.portrait:     # beside the stack's middle card, inside it
                ly = B[1] + 140 + k * 50
            else:
                ly = B[3] + 34 + k * 56
            d.text((mx - (lb[2] - lb[0]) / 2 - lb[0], ly + 10 * (1 - la)), txt,
                   font=lf, fill=br.ink + (int(255 * la),))
        t = s0 - 0.3
        self._stream(d, *money, t, None,
                     lambda dd, x, y, a: self._coin(dd, x, y, a, prim))
        self._stream(d, *back, t - self.PERIOD / 2, None,
                     lambda dd, x, y, a: self._chip(dd, x, y, a, self.coin))
        self._card(d, A, *self.left, enter, 1.0)
        self._card(d, C, *self.right, enter, 1.0)
