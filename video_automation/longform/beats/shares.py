"""`shares` - a dollar split into YES and NO, priced, read as odds, settled.

**Built for `what-are-prediction-markets` (2026-10-28), because the library
could not draw the mechanism the whole topic rests on.** A prediction market
sells a pair of shares on one question: one pays $1 if it happens, the other
$1 if it does not, so the two prices add up to a dollar and the YES price
*is* the crowd's probability. Said over a stock clip of a phone it is
arithmetic the viewer holds in their head; drawn, it is one coin coming
apart. `split` divides a whole into equal claims, `bars` compares sizes,
`gauge` reads one value on a track; none of them shows a price turning into
a percentage. It follows `quorum`'s template: line art in the brand colour,
one object per phrase, one state change.

Reveals, one caption chunk each, in this order:

  0  the question card, and one coin reading "$1" under it
  1  the coin comes apart into a YES coin and a NO coin
  2  the price bar fills to the split, each coin's price counting up
  3  the YES price turns into a percentage, "THE CROWD'S ODDS" under the bar
  4  only with `outcome`: the winning coin fills and reads $1, the other
     greys to $0 and is struck

payload: (question, yes, title, outcome)
  question  the market's question, one or two short lines
  yes       the YES price in cents, 1-99; NO is 100 - yes
  title     the beat's kicker
  outcome   "YES", "NO" or None (four reveals instead of five)
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth

SPLIT = 0.80        # seconds the coins take to come apart
FILL = 0.90         # seconds the price bar takes to fill
MORPH = 0.60        # the price turning into a percentage
SETTLE = 0.60       # the outcome landing


def settle_time(reveal: float) -> float:
    """When the outcome lands - shared with the builders' cues."""
    return reveal + 0.10 + SETTLE * 0.6


class Shares(Beat):

    EMBLEM = False

    def __init__(self, question: str, yes: int, title: str = "",
                 outcome: str | None = None, **kw):
        super().__init__(**kw)
        if not 1 <= int(yes) <= 99:
            raise ValueError(f"shares wants a YES price of 1-99 cents, got {yes}")
        if outcome not in (None, "YES", "NO"):
            raise ValueError(f"shares outcome is 'YES', 'NO' or None, "
                             f"got {outcome!r}")
        self.question, self.yes = question, int(yes)
        self.title, self.outcome = title, outcome

        fr, p = self.frame, self.portrait
        self.qsize = 54 if p else 46
        self.card_w = fr.w - 2 * 70 if p else 1180
        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        lines = question.split("\n")
        for ln in lines:
            w = d.textlength(ln, font=_display(self.qsize))
            if w > self.card_w - 2 * 56:
                raise ValueError(f"shares question line {ln!r} is {w:.0f}px "
                                 f"wide and the card has "
                                 f"{self.card_w - 112}px. Break it with \\n.")
        self.lines = lines
        lh = int(self.qsize * 1.25)
        self.card_h = 2 * 40 + lh * len(lines)
        self.lh = lh

        # The layout, top to bottom: question card, coins, bar, odds line -
        # laid out from zero, then the whole block centred in the frame below
        # the kicker, so a one-line question does not leave the lower third
        # empty.
        self.R = 150 if p else 128
        self.coin_dx = 240 if p else 360
        self.bar_w = fr.w - 2 * 110 if p else 1180
        self.bar_h = 60 if p else 52
        coin_y = self.card_h + (300 if p else 200)
        bar_y = coin_y + self.R + (270 if p else 170)
        block = bar_y + self.bar_h + 90
        top = self.head_y + (110 if p else 80)
        y0 = max(top, (fr.h - block) // 2 + (40 if p else 30))
        self.card_y, self.coin_y, self.bar_y = y0, y0 + coin_y, y0 + bar_y

    # --- clocks ---------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        """Seconds since reveal `i`, or -1 if it has not happened."""
        rv = self.reveals or []
        if i >= len(rv):
            return -1.0
        t = self.at(f) - rv[i]
        return t if t >= 0 else -1.0

    # --- the frame ------------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        br, fr = self.brand, self.frame
        prim, ink = br.primary, br.ink
        grey = (150, 150, 150)
        # **Drawn on an RGBA layer, then composited.** On the RGB frame PIL
        # ignores a text fill's alpha, so every fade here snapped; shapes
        # blended and type did not. `blindsign` draws its card the same way.
        layer = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")

        t0 = self._since(0, f)
        if t0 < 0:
            return
        self._draw(d, layer, f, t0, prim, ink, grey)
        out.paste(layer, (0, 0), layer)

    def _draw(self, d, layer, f, t0, prim, ink, grey) -> None:
        br, fr = self.brand, self.frame
        enter = ease_out(t0 / 0.6)
        rise = int(20 * (1 - enter))

        # The question card.
        cx = fr.w // 2
        x0 = cx - self.card_w // 2
        y0 = self.card_y + rise
        a = int(255 * enter)
        d.rounded_rectangle([x0, y0, x0 + self.card_w, y0 + self.card_h],
                            radius=24, fill=(16, 16, 16, int(230 * enter)))
        mx = cx
        pts = _round_corners([(mx, y0), (x0 + self.card_w, y0),
                              (x0 + self.card_w, y0 + self.card_h),
                              (x0, y0 + self.card_h), (x0, y0),
                              (mx + 0.5, y0)], 24, seg=10)
        partial(d, pts, max(0.001, _smooth(t0 / 0.8)), prim, 4)
        qf = _display(self.qsize)
        for i, ln in enumerate(self.lines):
            b = d.textbbox((0, 0), ln, font=qf)
            ly = y0 + 40 + i * self.lh - b[1]
            shadow_text(d, (cx - (b[2] - b[0]) / 2 - b[0], ly), ln, qf,
                        ink + (a,), alpha=a)

        # The coins: one at the centre, then two moving apart.
        t1 = self._since(1, f)
        s = _smooth(t1 / SPLIT) if t1 >= 0 else 0.0
        cy = self.coin_y + rise
        t2 = self._since(2, f)
        fill_p = _smooth(t2 / FILL) if t2 >= 0 else 0.0
        t3 = self._since(3, f)
        morph = _smooth(t3 / MORPH) if t3 >= 0 else 0.0
        t4 = self._since(4, f) if self.outcome else -1.0
        settle = _smooth((t4 - 0.10) / SETTLE) if t4 >= 0.10 else 0.0

        R = self.R
        sides = (("YES", -1, self.yes), ("NO", 1, 100 - self.yes))
        for name, sign, cents in sides:
            x = cx + sign * self.coin_dx * s
            won = self.outcome == name
            lost = self.outcome is not None and not won
            col = prim if name == "YES" else ink
            # A coin's fill: the winner fills with the accent as it settles.
            fill = None
            if won and settle > 0:
                fill = prim + (int(255 * settle),)
            ring = col if not (lost and settle > 0) else tuple(
                int(c + (g - c) * settle) for c, g in zip(col, grey))
            d.ellipse([x - R, cy - R, x + R, cy + R], outline=ring + (a,),
                      width=6, fill=fill)
            d.ellipse([x - R + 16, cy - R + 16, x + R - 16, cy + R - 16],
                      outline=ring + (int(a * 0.45),), width=2)

            # The face: "$1" while whole, the side's name once apart, the
            # payout once settled.
            face_big = _display(int(R * 0.62))
            face_name = _display(int(R * 0.44))
            if s < 1 / 3 and sign == -1:
                # Only one "$1" is drawn while the coins overlap.
                fa = int(a * max(0.0, 1 - 3 * s))
                txt = "$1"
                b = d.textbbox((0, 0), txt, font=face_big)
                d.text((cx - (b[2] - b[0]) / 2 - b[0],
                        cy - (b[3] - b[1]) / 2 - b[1]), txt, font=face_big,
                       fill=prim + (fa,))
            if s > 0:
                if settle > 0 and (won or lost):
                    txt = "$1" if won else "$0"
                    tc = (16, 16, 16) if won else grey
                    na = int(255 * min(s, settle))
                    b = d.textbbox((0, 0), txt, font=face_big)
                    d.text((x - (b[2] - b[0]) / 2 - b[0],
                            cy - (b[3] - b[1]) / 2 - b[1]), txt,
                           font=face_big, fill=tc + (na,))
                    # The name fades as the payout lands.
                    na2 = int(255 * s * (1 - settle))
                else:
                    na2 = int(255 * s)
                if na2 > 0:
                    b = d.textbbox((0, 0), name, font=face_name)
                    d.text((x - (b[2] - b[0]) / 2 - b[0],
                            cy - (b[3] - b[1]) / 2 - b[1]), name,
                           font=face_name, fill=col + (na2,))
                if lost and settle > 0:
                    k = R * 0.80
                    partial(d, [(x - k, cy + k), (x + k, cy - k)],
                            settle, br.negative, 8)

                # Under the coin: what it pays, then its price.
                lf = _font(30 if self.portrait else 28)
                if fill_p <= 0:
                    sub = f"PAYS $1 IF {name}"
                    b = d.textbbox((0, 0), sub, font=lf)
                    d.text((x - (b[2] - b[0]) / 2 - b[0], cy + R + 26 - b[1]),
                           sub, font=lf, fill=grey + (int(255 * s),))
                else:
                    pf = _display(64 if self.portrait else 58)
                    shown = round(cents * fill_p)
                    price = f"{shown}¢"
                    pa = int(255 * fill_p * (1 - 0.6 * settle))
                    if name == "YES" and morph > 0:
                        # The price becomes the probability: the price is
                        # gone in the first half of the morph and the
                        # percentage rises into its place in the second, so
                        # the two never sit on top of each other (the first
                        # cut crossfaded them and "62c" ghosted under "62%").
                        pa = int(pa * max(0.0, 1 - 2 * morph))
                        m2 = max(0.0, 2 * morph - 1)
                        odds = f"{cents}%"
                        of = _display(int((64 if self.portrait else 58)
                                          * (1 + 0.35 * m2)))
                        b = d.textbbox((0, 0), odds, font=of)
                        oy = cy + R + 22 - b[1] + int(18 * (1 - ease_out(m2)))
                        oa = int(255 * m2 * (1 - 0.6 * settle))
                        if oa > 0:
                            shadow_text(d, (x - (b[2] - b[0]) / 2 - b[0], oy),
                                        odds, of, prim + (oa,), alpha=oa)
                    if pa > 0:
                        b = d.textbbox((0, 0), price, font=pf)
                        d.text((x - (b[2] - b[0]) / 2 - b[0],
                                cy + R + 22 - b[1]), price, font=pf,
                               fill=col + (pa,))

        # The price bar, under everything: YES from the left, NO from the
        # right, meeting at the split - the two prices are one dollar.
        if t2 >= 0:
            ba = int(255 * min(1.0, t2 / 0.3))
            bx0 = cx - self.bar_w // 2
            by0 = self.bar_y + rise
            bx1, by1 = bx0 + self.bar_w, by0 + self.bar_h
            d.rounded_rectangle([bx0, by0, bx1, by1], radius=self.bar_h // 2,
                                outline=(255, 255, 255, int(ba * 0.35)), width=2)
            yes_frac = self.yes / 100
            if settle > 0 and self.outcome:
                target = 1.0 if self.outcome == "YES" else 0.0
                yes_frac = yes_frac + (target - yes_frac) * settle
            split_x = bx0 + self.bar_w * yes_frac
            yx = bx0 + (split_x - bx0) * fill_p
            nx = bx1 - (bx1 - split_x) * fill_p
            if yx - bx0 > 6:
                d.rounded_rectangle([bx0 + 4, by0 + 4, max(bx0 + 10, yx - 3),
                                     by1 - 4], radius=self.bar_h // 2 - 4,
                                    fill=prim + (ba,))
            if bx1 - nx > 6:
                d.rounded_rectangle([min(bx1 - 10, nx + 3), by0 + 4, bx1 - 4,
                                     by1 - 4], radius=self.bar_h // 2 - 4,
                                    fill=(90, 90, 90, ba))
            lf = _font(28)
            for txt, x, anchor in (("$0", bx0, 0), ("$1", bx1, 1)):
                b = d.textbbox((0, 0), txt, font=lf)
                d.text((x - (b[2] - b[0]) * anchor, by1 + 16 - b[1]), txt,
                       font=lf, fill=grey + (ba,))

            if morph > 0:
                cap = "THE CROWD'S ODDS"
                cf = _font(34 if self.portrait else 32)
                b = d.textbbox((0, 0), cap, font=cf)
                ca = int(255 * morph * max(0.0, 1 - 2 * settle))
                if ca > 0:
                    d.text((cx - (b[2] - b[0]) / 2 - b[0],
                            by1 + 60 - b[1] + int(10 * (1 - morph))), cap,
                           font=cf, fill=prim + (ca,))
            if settle > 0.5:
                cap = f"RESOLVED {self.outcome}"
                cf = _font(34 if self.portrait else 32)
                b = d.textbbox((0, 0), cap, font=cf)
                d.text((cx - (b[2] - b[0]) / 2 - b[0], by1 + 60 - b[1]), cap,
                       font=cf, fill=prim + (int(255 * max(0.0, 2 * settle - 1)),))
