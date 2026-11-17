"""`reserve` - a dollar handed to an issuer, lent on, and who keeps the interest.

**Built for `stablecoin-interest` (2026-11-16), because the library could
not draw the one fact the whole pair turns on**: a stablecoin dollar is
lent to the US government, the loan pays interest, and the person who
handed over the dollar gets none of it. `pile` is money pooling in one
place, `sweep` is a wallet drained, `diagram` is a chain of words. None of
them shows a payment flowing one way while the line back to you is
blocked. Reusable for any "your money earns, someone else is paid" claim:
a bank deposit, an exchange's balance, a money market fund's fee.

Three cards - you, the issuer, the bill - and the lines between them.
Four reveals, four caption chunks in this order:

1. the deposit ("You hand the issuer a dollar,") - the cards arrive, a
   `$1` chip travels from you to the issuer and a token chip travels back;
   your card now reads the token;
2. the loan ("and it lends that dollar to the US government.") - the `$1`
   travels on to the bill, which lights as LENT;
3. the interest ("The bill pays interest, and the issuer keeps it.") -
   small coins stream from the bill back to the issuer for the rest of the
   shot, and the issuer's card sets `kept`;
4. yours ("Your share is zero.") - a line starts from the issuer back
   toward you, stops at a barrier halfway with a cross, your card's figure
   turns to `yours` in the negative colour and `verdict` sets under it.

The chips and the blocked line move on `span_p`, so each lasts its phrase;
the stream of coins runs on the shot's own clock and never stops - the
interest keeps coming, which is the point.

payload: (you, issuer, bill, kept, yours, verdict, title, coin, token)
  you, issuer, bill  (name, sub)  the three cards
  kept     the issuer's line on reveal 3 ("KEEPS THE INTEREST")
  yours    your figure on reveal 4 ("$0")
  verdict  the label under it ("BANNED BY LAW")
  title    the beat's kicker
  coin     optional, the deposit chip ("$1")
  token    optional, the chip that comes back ("1 TOKEN")

Landscape lays the cards in a row, you on the left; portrait stacks them,
you on top. Portrait-safe.
"""

from __future__ import annotations

import math

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth


def flow_times(rv: list[float]) -> dict:
    """When the sounds land, from the beat's own reveals - one clock for
    picture and sound (`crypto/build.py`, `longform/build.py`)."""
    out = {}
    if rv:
        out["deposit"] = rv[0]
    if len(rv) > 1:
        out["lend"] = rv[1]
    if len(rv) > 2:
        out["interest"] = rv[2] + 0.15
    if len(rv) > 3:
        out["block"] = rv[3] + 0.75
    return out


class Reserve(Beat):

    EMBLEM = False

    def __init__(self, you: tuple, issuer: tuple, bill: tuple, kept: str,
                 yours: str, verdict: str, title: str = "",
                 coin: str = "$1", token: str = "1 TOKEN", **kw):
        super().__init__(**kw)
        self.you, self.issuer, self.bill = tuple(you), tuple(issuer), tuple(bill)
        self.kept, self.yours, self.verdict = kept, yours, verdict
        self.title, self.coin, self.token = title, coin, token
        fr, p = self.frame, self.portrait
        if p:
            cw, ch = fr.w - 2 * 120, 310
            x = 120
            # The stack runs from under the heading to ~88% of the height,
            # clear of the platforms' own title band at the bottom.
            top = self.head_y + 110
            gap = (int(fr.h * 0.90) - top - 3 * ch) // 2
            self.cards = [(x, top + i * (ch + gap), x + cw, top + i * (ch + gap) + ch)
                          for i in range(3)]
        else:
            cw, ch = 390, 430
            gap = (fr.w - 2 * self.margin - 3 * cw) // 2
            top = (self.head_y + fr.h - ch) // 2 + 10
            x0 = self.margin
            self.cards = [(x0 + i * (cw + gap), top, x0 + i * (cw + gap) + cw, top + ch)
                          for i in range(3)]
        self._d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        self._fit_cache: dict = {}
        cw = self.cards[0][2] - self.cards[0][0]
        nf, sf, ff = self._fonts()
        # Labels in the display face shrink to the card (never below 70%);
        # past that the label is a script note, and it raises here rather
        # than drawing off the card.
        for txt in (self.you[0], self.issuer[0], self.bill[0], self.kept,
                    self.verdict, "PAYS INTEREST"):
            if self._fit(txt, nf.size, cw - 50).size < nf.size * 0.7:
                raise ValueError(f"reserve label {txt!r} is too wide for a card")
        for _, sub in (self.you, self.issuer, self.bill):
            if self._d.textlength(sub, font=sf) > cw - 50:
                raise ValueError(f"reserve card line {sub!r} is too wide")
        for txt in (self.coin, self.token, self.yours):
            if self._d.textlength(txt, font=ff) > cw - 50:
                raise ValueError(f"reserve figure {txt!r} is too wide")

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
        return (_display(46 if p else 40), _font(30 if p else 28),
                _display(80 if p else 62))

    # --- clocks -------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (i / 4) * 0.85)
        return self.at(f) - when

    # --- geometry -----------------------------------------------------------

    def _ports(self, a: int, b: int, lane: int):
        """The two ends of the line between card `a` and card `b`, in one of
        two lanes (0 the forward lane, 1 the return lane)."""
        A, B = self.cards[a], self.cards[b]
        if self.portrait:
            cx = (A[0] + A[2]) / 2 + (-150 if lane == 0 else 150)
            if a < b:
                return (cx, A[3]), (cx, B[1])
            return (cx, A[1]), (cx, B[3])
        cy = (A[1] + A[3]) / 2 + (-70 if lane == 0 else 80)
        if a < b:
            return (A[2], cy), (B[0], cy)
        return (A[0], cy), (B[2], cy)

    @staticmethod
    def _along(p0, p1, q: float):
        return (p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q)

    # --- pieces -------------------------------------------------------------

    def _card(self, d, box, name, sub, figure, fig_col, lit: float,
              enter: float, line: str = "", line_col=None, line_a: float = 0.0):
        br = self.brand
        x0, y0, x1, y1 = box
        a = int(255 * enter)
        d.rounded_rectangle(box, radius=26, fill=(14, 14, 14, int(236 * enter)))
        mx = (x0 + x1) / 2
        pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                              (x0, y0), (mx + 0.5, y0)], 26, seg=10)
        edge = tuple(int(90 + (c - 90) * lit) for c in br.primary)
        partial(d, pts, max(0.001, _smooth(enter)), edge, 4)
        nf0, sf, ff = self._fonts()
        nf = self._fit(name, nf0.size, x1 - x0 - 50)
        cx = mx
        nb = d.textbbox((0, 0), name, font=nf)
        d.text((cx - (nb[2] - nb[0]) / 2 - nb[0], y0 + 30), name, font=nf,
               fill=br.primary + (a,))
        sb = d.textbbox((0, 0), sub, font=sf)
        d.text((cx - (sb[2] - sb[0]) / 2 - sb[0], y0 + 86), sub, font=sf,
               fill=(170, 170, 170, a))
        if figure:
            fb = d.textbbox((0, 0), figure, font=ff)
            fy = y0 + (118 if self.portrait else 180)
            shadow_text(d, (cx - (fb[2] - fb[0]) / 2 - fb[0], fy), figure, ff,
                        fig_col + (a,), alpha=a)
        if line and line_a > 0:
            la = int(255 * line_a)
            lf = self._fit(line, nf0.size, x1 - x0 - 50)
            lb = d.textbbox((0, 0), line, font=lf)
            ly = y1 - (74 if self.portrait else 78)
            col = line_col or br.ink
            d.text((cx - (lb[2] - lb[0]) / 2 - lb[0], ly + 10 * (1 - line_a)),
                   line, font=lf, fill=col + (la,))

    def _chip(self, d, x, y, text, col, ink=(12, 12, 12)):
        f = _display(32 if self.portrait else 30)
        b = d.textbbox((0, 0), text, font=f)
        w, h = b[2] - b[0], b[3] - b[1]
        d.rounded_rectangle([x - w / 2 - 20, y - h / 2 - 14, x + w / 2 + 20,
                             y + h / 2 + 14], radius=12, fill=col + (255,))
        d.text((x - w / 2 - b[0], y - h / 2 - b[1]), text, font=f, fill=ink + (255,))

    def _coin(self, d, x, y, r, col, a):
        d.ellipse([x - r, y - r, x + r, y + r], fill=col + (a,),
                  outline=(20, 20, 20, a), width=2)
        f = _display(int(r * 1.3))
        b = d.textbbox((0, 0), "$", font=f)
        d.text((x - (b[2] - b[0]) / 2 - b[0], y - (b[3] - b[1]) / 2 - b[1]), "$",
               font=f, fill=(25, 25, 25, a))

    # --- the frame ----------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        s0 = self._since(0, f)
        if s0 < 0:
            return
        br = self.brand
        prim, neg, ink = br.primary, br.negative, br.ink
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        s1, s2, s3 = (self._since(i, f) for i in (1, 2, 3))
        enter = min(1.0, max(0.0, s0 / 0.6))

        # The lines, drawn as the cards arrive: forward lane (the dollar),
        # return lane (interest from the bill; the blocked line to you).
        fwd01 = self._ports(0, 1, 0)
        fwd12 = self._ports(1, 2, 0)
        ret21 = self._ports(2, 1, 1)
        ret10 = self._ports(1, 0, 1)
        grey = (100, 100, 100)
        lp = _smooth((s0 - 0.2) / 0.6)
        partial(d, list(fwd01), lp, grey, 5)
        partial(d, list(fwd12), lp, grey, 5)

        # 1. the deposit: $1 to the issuer, a token back.
        q0 = self.span_p(0, f, cap=1.8)
        half = 0.5
        if 0 < q0 < 1:
            if q0 < half:
                x, y = self._along(*fwd01, ease_out(q0 / half))
                self._chip(d, x, y, self.coin, prim)
            else:
                x, y = self._along(fwd01[1], fwd01[0], ease_out((q0 - half) / half))
                self._chip(d, x, y, self.token, (235, 235, 235))
        you_fig = self.coin if q0 < 1 else self.token
        you_col = ink
        # 4. yours: the figure turns.
        q3 = self.span_p(3, f, cap=1.4) if s3 >= 0 else 0.0
        if s3 >= 0 and q3 >= 0.98:
            you_fig, you_col = self.yours, neg

        # 2. the loan: $1 on to the bill.
        q1 = self.span_p(1, f, cap=1.6) if s1 >= 0 else 0.0
        if 0 < q1 < 1:
            x, y = self._along(*fwd12, ease_out(q1))
            self._chip(d, x, y, self.coin, prim)
        bill_lit = 1.0 if q1 >= 1 else 0.0
        bill_fig = self.coin if q1 >= 1 else ""

        # 3. the interest: a stream of coins, bill to issuer, for good.
        if s2 >= 0:
            partial(d, list(ret21), _smooth(s2 / 0.5), prim, 4)
            period, n = 1.4, 4
            r = 24 if self.portrait else 24
            for k in range(n):
                t = s2 - 0.35 - k * period / n
                if t < 0:
                    continue
                q = (t % period) / period
                fade = min(1.0, q / 0.12, (1 - q) / 0.12)
                x, y = self._along(*ret21, q)
                self._coin(d, x, y, r, prim, int(255 * max(0.0, fade)))
        kept_a = _smooth((s2 - 0.5) / 0.5) if s2 >= 0 else 0.0

        # 4. the line back to you, stopped at a barrier.
        if s3 >= 0:
            p0, p1 = ret10
            mid = self._along(p0, p1, 0.5)
            reach = min(1.0, q3 / 0.8)
            # dashed, out from the issuer to the barrier
            segs = 9
            for k in range(segs):
                a0, a1 = k / segs, (k + 0.55) / segs
                if a0 > reach:
                    break
                e0 = self._along(p0, mid, a0)
                e1 = self._along(p0, mid, min(a1, reach))
                d.line([e0, e1], fill=(150, 150, 150, 255), width=4)
            if reach >= 1:
                # the barrier, across the lane, and a cross on it
                bp = _smooth((q3 - 0.8) / 0.2)
                L = 46 if self.portrait else 44
                if self.portrait:
                    bar = [(mid[0] - L, mid[1]), (mid[0] + L, mid[1])]
                else:
                    bar = [(mid[0], mid[1] - L), (mid[0], mid[1] + L)]
                partial(d, bar, max(0.001, bp), neg, 9)
                xs = 22
                ox = 64 if self.portrait else 0
                oy = 0 if self.portrait else -74
                cxx, cyy = mid[0] + ox, mid[1] + oy
                partial(d, [(cxx - xs, cyy - xs), (cxx + xs, cyy + xs)],
                        max(0.001, bp), neg, 8)
                partial(d, [(cxx + xs, cyy - xs), (cxx - xs, cyy + xs)],
                        max(0.001, _smooth((q3 - 0.88) / 0.12)), neg, 8)
        verdict_a = _smooth((q3 - 0.9) / 0.1) if s3 >= 0 else 0.0

        # The cards, over the lines.
        A, B, C = self.cards
        self._card(d, A, *self.you, you_fig, you_col, 1.0 if s3 >= 0 else 0.4,
                   enter, self.verdict, neg, verdict_a)
        issuer_fig = self.coin if (q0 >= 1 and q1 <= 0) else ""
        self._card(d, B, *self.issuer, issuer_fig, prim, 1.0 if s2 >= 0 else 0.4,
                   enter, self.kept, prim, kept_a)
        self._card(d, C, *self.bill, bill_fig, prim, bill_lit if s1 >= 0 else 0.4,
                   enter, "PAYS INTEREST" if s2 >= 0 else "", ink,
                   _smooth(s2 / 0.4) if s2 >= 0 else 0.0)

        rise = int(22 * (1 - ease_out(enter)))
        out.paste(layer, (0, rise), layer)
