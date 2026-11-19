"""`honeypot` - a token anyone can buy and only its creators can sell.

**Built for `squid-game-token` (2026-11-19), because the library could not
draw the one fact the pair turns on**: SQUID's buyers paid in and the price
climbed, but a rule in the token blocked every sale except its creators'.
`pool` drains a pool, `sweep` empties a wallet, `blindsign` is a screen
disagreeing with a signature. None of them shows the same door letting one
direction through, refusing the other, and waving one wallet past. Reusable
for any honeypot token, a transfer blacklist, a "trading not enabled yet"
flag, a withdrawal freeze on an exchange.

Four cards and a gate: you and the creators on the source side, the
contract as a gate across the lanes, the pool on the far side. Three lanes:
your buy, your sell, the creators' sell. Four reveals, four caption chunks:

1. the buy ("Anyone could buy it.") - your `pay` chip runs through the gate
   to the pool, the lane's ring ticks, a `token` chip runs back;
2. your sell ("But when you tried to sell,") - your token chip runs at the
   gate on the middle lane, stops dead against it, a cross lands and `rule`
   sets beside it in the negative colour; the chip slides back home;
3. the rule ("you needed marbles from a game that did not exist.") -
   `note` sets under the rule and the rule's ring stays shut;
4. the creators ("Its creators needed nothing.") - their card lights, their
   token chip runs the bottom lane straight through, a tick, `exempt` sets.

payload: (you, owner, pool, rule, note, exempt, title, pay, token)
  you, owner, pool  (name, sub) the three cards
  rule     the refusal, by the cross ("NEEDS MARBLES")
  note     the line under it on reveal 3 ("FROM A GAME THAT NEVER CAME")
  exempt   the creators' line on reveal 4 ("NO RULE FOR THEM")
  title    the beat's kicker
  pay      optional, the money chip ("BNB")
  token    optional, the token chip ("SQUID")

Landscape runs the flow left to right; portrait runs it top to bottom,
you and the creators side by side above the gate. Portrait-safe.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth


def gate_times(rv: list[float]) -> dict:
    """When the sounds land, from the beat's own reveals - one clock for
    picture and sound (`crypto/build.py`, `longform/build.py`)."""
    out = {}
    if rv:
        out["buy"] = rv[0] + 0.12
    if len(rv) > 1:
        # the chip reaches the gate halfway through its phrase's travel
        out["block"] = rv[1] + 0.62
    if len(rv) > 2:
        out["rule"] = rv[2] + 0.10
    if len(rv) > 3:
        out["exempt"] = rv[3] + 0.70
    return out


class Honeypot(Beat):

    EMBLEM = False

    def __init__(self, you: tuple, owner: tuple, pool: tuple, rule: str,
                 note: str, exempt: str, title: str = "", pay: str = "BNB",
                 token: str = "SQUID", **kw):
        super().__init__(**kw)
        self.you, self.owner, self.pool = tuple(you), tuple(owner), tuple(pool)
        self.rule, self.note, self.exempt = rule, note, exempt
        self.title, self.pay, self.token = title, pay, token
        fr, p = self.frame, self.portrait
        if p:
            top = self.head_y + 170
            cw, ch = (fr.w - 2 * self.margin - 40) // 2, 250
            x0 = self.margin
            self.you_box = (x0, top, x0 + cw, top + ch)
            self.own_box = (fr.w - x0 - cw, top, fr.w - x0, top + ch)
            gy = top + ch + 260
            self.gate = (x0 - 20, gy, fr.w - x0 + 20, gy + 120)
            py = gy + 120 + 290
            self.pool_box = (x0, py, fr.w - x0, py + 260)
            # three lanes, x positions: buy and sell from your card, the
            # creators' from theirs.
            ya, yb = self.you_box[3], self.pool_box[1]
            xb, xs = x0 + cw * 0.30, x0 + cw * 0.72
            xo = (self.own_box[0] + self.own_box[2]) / 2
            self.lanes = [((xb, ya), (xb, yb)), ((xs, ya), (xs, yb)),
                          ((xo, ya), (xo, yb))]
        else:
            top = self.head_y + 90
            cw = 360
            x0 = self.margin
            bottom = fr.h - 110
            h = bottom - top
            self.you_box = (x0, top, x0 + cw, top + int(h * 0.56))
            self.own_box = (x0, top + int(h * 0.66), x0 + cw, bottom)
            gx = fr.w // 2 - 70
            self.gate = (gx, top - 10, gx + 140, bottom + 10)
            self.pool_box = (fr.w - x0 - cw, top + int(h * 0.12),
                             fr.w - x0, bottom - int(h * 0.12))
            ys = self.you_box
            yb_ = ys[1] + (ys[3] - ys[1]) * 0.36
            ys_ = ys[1] + (ys[3] - ys[1]) * 0.80
            yo = (self.own_box[1] + self.own_box[3]) / 2
            xa, xz = ys[2], self.pool_box[0]
            self.lanes = [((xa, yb_), (xz, yb_)), ((xa, ys_), (xz, ys_)),
                          ((self.own_box[2], yo), (xz, yo))]
        self._d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        self._fit_cache: dict = {}
        nf, sf, lf = self._fonts()
        for box, (name, sub) in ((self.you_box, self.you),
                                 (self.own_box, self.owner),
                                 (self.pool_box, self.pool)):
            w = box[2] - box[0] - 40
            if self._fit(name, nf.size, w).size < nf.size * 0.7:
                raise ValueError(f"honeypot card name {name!r} is too wide")
            if self._d.textlength(sub, font=sf) > w:
                raise ValueError(f"honeypot card line {sub!r} is too wide")
        room = self._label_room()
        for txt, k in ((self.rule, 1.0), (self.note, self._small()),
                       (self.exempt, self._small())):
            size = int(lf.size * k)
            if self._fit(txt, size, room).size < size * 0.7:
                raise ValueError(f"honeypot label {txt!r} is too wide")

    # --- type ---------------------------------------------------------------

    def _fonts(self):
        p = self.portrait
        return (_display(46 if p else 42), _font(28 if p else 26),
                _display(40 if p else 34))

    def _fit(self, text: str, size: int, maxw: float):
        key = (text, size, int(maxw))
        if key not in self._fit_cache:
            f = _display(size)
            while size > 12 and self._d.textlength(text, font=f) > maxw:
                size -= 1
                f = _display(size)
            self._fit_cache[key] = f
        return self._fit_cache[key]

    def _small(self) -> float:
        """The note and the exemption set a step under the rule."""
        return 0.78 if self.portrait else 0.80

    def _label_room(self) -> float:
        """How wide a gate label may run: in landscape the gap between the
        gate and the pool; in portrait the frame inside its margins."""
        if self.portrait:
            return self.frame.w - 2 * self.margin
        return self.pool_box[0] - self.gate[2] - 60

    # --- clocks -------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (i / 4) * 0.85)
        return self.at(f) - when

    @staticmethod
    def _along(p0, p1, q: float):
        return (p0[0] + (p1[0] - p0[0]) * q, p0[1] + (p1[1] - p0[1]) * q)

    def _gate_point(self, lane: int):
        """Where a lane crosses the gate's near face."""
        (a, b) = self.lanes[lane]
        if self.portrait:
            return (a[0], self.gate[1])
        return (self.gate[0], a[1])

    def _gate_mid(self, lane: int):
        (a, b) = self.lanes[lane]
        if self.portrait:
            return (a[0], (self.gate[1] + self.gate[3]) / 2)
        return ((self.gate[0] + self.gate[2]) / 2, a[1])

    # --- pieces -------------------------------------------------------------

    def _card(self, d, box, name, sub, lit: float, enter: float):
        br = self.brand
        x0, y0, x1, y1 = box
        a = int(255 * enter)
        d.rounded_rectangle(box, radius=24, fill=(14, 14, 14, int(236 * enter)))
        mx = (x0 + x1) / 2
        pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                              (x0, y0), (mx + 0.5, y0)], 24, seg=10)
        edge = tuple(int(90 + (c - 90) * lit) for c in br.primary)
        partial(d, pts, max(0.001, _smooth(enter)), edge, 4)
        nf0, sf, _ = self._fonts()
        nf = self._fit(name, nf0.size, x1 - x0 - 40)
        nb = d.textbbox((0, 0), name, font=nf)
        sb = d.textbbox((0, 0), sub, font=sf)
        block = (nb[3] - nb[1]) + 16 + (sb[3] - sb[1])
        ty = (y0 + y1) / 2 - block / 2
        col = tuple(int(150 + (c - 150) * lit) for c in br.primary)
        d.text((mx - (nb[2] - nb[0]) / 2 - nb[0], ty - nb[1]), name, font=nf,
               fill=col + (a,))
        d.text((mx - (sb[2] - sb[0]) / 2 - sb[0], ty + (nb[3] - nb[1]) + 16 - sb[1]),
               sub, font=sf, fill=(170, 170, 170, a))

    def _chip(self, d, x, y, text, col, alpha: float = 1.0,
              ink=(12, 12, 12)):
        f = _display(30 if self.portrait else 28)
        b = d.textbbox((0, 0), text, font=f)
        w, h = b[2] - b[0], b[3] - b[1]
        a = int(255 * max(0.0, min(1.0, alpha)))
        d.rounded_rectangle([x - w / 2 - 18, y - h / 2 - 12, x + w / 2 + 18,
                             y + h / 2 + 12], radius=12, fill=col + (a,))
        d.text((x - w / 2 - b[0], y - h / 2 - b[1]), text, font=f, fill=ink + (a,))

    def _ring(self, d, c, state: str, p: float):
        """A disc where a lane meets the gate: open (grey), tick, or cross."""
        br = self.brand
        r = 30
        x, y = c
        if state == "open":
            d.ellipse([x - r, y - r, x + r, y + r], fill=(24, 24, 24, 255),
                      outline=(110, 110, 110, 255), width=4)
            return
        col = br.primary if state == "tick" else br.negative
        k = ease_out(p)
        rr = r * (0.6 + 0.4 * k)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=col + (255,))
        ink = (12, 12, 12)
        if state == "tick":
            partial(d, [(x - 13, y + 1), (x - 3, y + 11), (x + 14, y - 10)],
                    max(0.001, _smooth((p - 0.2) / 0.6)), ink, 6)
        else:
            s = 11
            partial(d, [(x - s, y - s), (x + s, y + s)],
                    max(0.001, _smooth((p - 0.2) / 0.4)), (245, 245, 245), 6)
            partial(d, [(x + s, y - s), (x - s, y + s)],
                    max(0.001, _smooth((p - 0.5) / 0.4)), (245, 245, 245), 6)

    def _label(self, d, anchor, text, col, a: float, size_from: int,
               below: bool = False):
        """A label beside a ring: right of the gate in landscape, centred
        under the gate in portrait."""
        if a <= 0:
            return
        f = self._fit(text, size_from, self._label_room())
        b = d.textbbox((0, 0), text, font=f)
        w, h = b[2] - b[0], b[3] - b[1]
        x, y = anchor
        if self.portrait:
            tx = self.frame.w / 2 - w / 2 - b[0]
            ty = y - b[1]
        else:
            tx = x - b[0]
            ty = y - h / 2 - b[1] + (h + 14 if below else 0)
        rise = 10 * (1 - a)
        shadow_text(d, (tx, ty + rise), text, f, col + (int(255 * a),),
                    alpha=int(255 * a))

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
        grey = (95, 95, 95)

        # The lanes, drawn as the cards arrive.
        lp = _smooth((s0 - 0.15) / 0.6)
        for k, (a, b) in enumerate(self.lanes):
            if k == 2 and s3 < 0:
                partial(d, [a, b], lp, (60, 60, 60), 4)
            else:
                partial(d, [a, b], lp, grey, 5)

        # The gate: the contract, across every lane.
        gx0, gy0, gx1, gy1 = self.gate
        ga = int(255 * enter)
        d.rounded_rectangle(self.gate, radius=18, fill=(20, 20, 20, int(245 * enter)),
                            outline=prim + (ga,), width=4)
        gf = _display(30 if self.portrait else 26)
        gl = "THE CONTRACT"
        gb = d.textbbox((0, 0), gl, font=gf)
        if self.portrait:
            d.text(((gx0 + gx1) / 2 - (gb[2] - gb[0]) / 2 - gb[0],
                    gy0 - (gb[3] - gb[1]) - 22 - gb[1]), gl, font=gf,
                   fill=prim + (ga,))
        else:
            d.text(((gx0 + gx1) / 2 - (gb[2] - gb[0]) / 2 - gb[0],
                    gy0 - (gb[3] - gb[1]) - 18 - gb[1]), gl, font=gf,
                   fill=prim + (ga,))

        # Lane words on the source side of the gate: BUY, SELL, SELL.
        wf = _display(26 if self.portrait else 24)
        for k, word in enumerate(("BUY", "SELL", "SELL")):
            if k == 2 and s3 < 0:
                continue
            a, _ = self.lanes[k]
            g = self._gate_point(k)
            m = self._along(a, g, 0.5)
            wb = d.textbbox((0, 0), word, font=wf)
            if self.portrait:
                pos = (m[0] - (wb[2] - wb[0]) / 2 - wb[0], m[1] - (wb[3] - wb[1]) / 2 - wb[1])
                d.rectangle([pos[0] + wb[0] - 8, pos[1] + wb[1] - 6,
                             pos[0] + wb[2] + 8, pos[1] + wb[3] + 6],
                            fill=(14, 14, 14, ga))
            else:
                pos = (m[0] - (wb[2] - wb[0]) / 2 - wb[0], m[1] - (wb[3] - wb[1]) - 18 - wb[1])
            d.text(pos, word, font=wf, fill=(190, 190, 190, ga))

        # 1. the buy: pay through to the pool, the token back.
        q0 = self.span_p(0, f, cap=1.6)
        a0, b0 = self.lanes[0]
        if 0 < q0 < 1:
            if q0 < 0.55:
                x, y = self._along(a0, b0, ease_out(q0 / 0.55))
                self._chip(d, x, y, self.pay, prim)
            else:
                x, y = self._along(b0, a0, ease_out((q0 - 0.55) / 0.45))
                self._chip(d, x, y, self.token, (235, 235, 235))
        buy_tick = _smooth((q0 - 0.2) / 0.3) if q0 > 0.2 else 0.0

        # 2. your sell: runs at the gate, stops, and slides back.
        q1 = self.span_p(1, f, cap=1.6) if s1 >= 0 else 0.0
        a1, _ = self.lanes[1]
        g1 = self._gate_point(1)
        hit = 0.45
        if s1 >= 0 and q1 < 1:
            if q1 < hit:
                x, y = self._along(a1, g1, ease_out(q1 / hit) * 0.92)
                self._chip(d, x, y, self.token, (235, 235, 235))
            else:
                back = (q1 - hit) / (1 - hit)
                # a shudder against the gate, then home
                if back < 0.25:
                    jit = 6 * (1 - back / 0.25) * (1 if int(back * 60) % 2 else -1)
                    x, y = self._along(a1, g1, 0.92)
                    if self.portrait:
                        y += jit
                    else:
                        x += jit
                else:
                    x, y = self._along(g1, a1, 0.08 + 0.92 * ease_out((back - 0.25) / 0.75))
                self._chip(d, x, y, self.token, (235, 235, 235))
        block_p = _smooth((q1 - hit) / 0.2) if q1 > hit else 0.0

        # 4. the creators' sell, straight through.
        q3 = self.span_p(3, f, cap=1.6) if s3 >= 0 else 0.0
        a2, b2 = self.lanes[2]
        if s3 >= 0 and 0 < q3 < 1:
            x, y = self._along(a2, b2, ease_out(q3))
            self._chip(d, x, y, self.token, (235, 235, 235))
        own_tick = _smooth((q3 - 0.4) / 0.3) if q3 > 0.4 else 0.0

        # The cards, over the lanes.
        self._card(d, self.you_box, *self.you, 1.0, enter)
        self._card(d, self.own_box, *self.owner,
                   1.0 if s3 >= 0 else 0.25, enter)
        self._card(d, self.pool_box, *self.pool, 1.0 if q0 > 0.5 else 0.5, enter)

        # The rings where each lane meets the gate.
        for k in range(3):
            c = self._gate_mid(k)
            if k == 0:
                self._ring(d, c, "tick" if buy_tick > 0 else "open", buy_tick)
            elif k == 1:
                self._ring(d, c, "cross" if block_p > 0 else "open", block_p)
            elif s3 >= 0 or k < 2:
                self._ring(d, c, "tick" if own_tick > 0 else "open", own_tick)
            elif enter > 0:
                self._ring(d, c, "open", 0)

        # The labels: the rule, its note, the exemption.
        _, _, lf = self._fonts()
        if self.portrait:
            ly = self.gate[3] + 34
            self._label(d, (0, ly), self.rule, neg, block_p, lf.size)
            self._label(d, (0, ly + 62), self.note, ink,
                        _smooth(s2 / 0.45) if s2 >= 0 else 0.0,
                        int(lf.size * self._small()))
            # the exemption sits above the pool, in the space under the note
            self._label(d, (0, ly + 124), self.exempt, prim,
                        own_tick, int(lf.size * self._small()))
        else:
            lx = self.gate[2] + 40
            r1 = self._gate_mid(1)[1]
            self._label(d, (lx, r1 - 24), self.rule, neg, block_p, lf.size)
            self._label(d, (lx, r1 + 34), self.note, ink,
                        _smooth(s2 / 0.45) if s2 >= 0 else 0.0,
                        int(lf.size * self._small()))
            r2 = self._gate_mid(2)[1]
            self._label(d, (lx, r2 + 46), self.exempt, prim, own_tick,
                        int(lf.size * self._small()))

        rise = int(22 * (1 - ease_out(enter)))
        out.paste(layer, (0, rise), layer)
