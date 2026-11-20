"""`relay` - one address handed from screen to screen, wrong from the first.

**Built for `optimizely-hack` (2026-11-20), because nothing here drew a
check that passes on the wrong thing.** The Optimizely script rewrote the
wallet address *on the page*, before anyone copied it. So the copy, the
paste into a wallet app and the hardware wallet's own screen all show the
same attacker's address, and every "does it match?" says yes. `lookalike`
sets two addresses against each other; `blindsign` is a screen disagreeing
with what it signs. This is the other case: every screen agreeing, all of
them wrong. Reusable for any source poisoned upstream - a swapped QR code,
a hijacked deposit page, an invoice edited in transit.

A row of cards (a column in 9:16), one per place the address passes
through, the first being where it came from. Reveals, one caption chunk
each, `len(places) + 1` in all:

1. the source ("You copy the address from the page") - the first card
   arrives, the address the page *meant* types in, then scrambles into the
   attacker's and the card's tag turns red: SWAPPED;
2. ... one per further place ("paste it into your wallet app") - an arrow
   draws to the next card, the same address types in, its tag turns green:
   MATCHES;
3. the verdict ("Every screen matches") - every MATCHES pulses, and the
   verdict sets under the row, its second line in `brand.negative`.

payload: (meant, attacker, places, title, verdict)
  meant     the address the page should have shown (made up - say so)
  attacker  the address it showed instead (the real IOC, credited)
  places    [label, ...]  two to four, the source first
  title     the beat's kicker
  verdict   (line, under)  e.g. ("EVERY SCREEN MATCHES", "THE ATTACKER'S ADDRESS")

The two addresses must be the same chain's length class (both type into
the same box), and they must differ - a relay of the right address is not
a story.
"""

from __future__ import annotations

import random

from PIL import Image, ImageDraw, ImageFont

from ...core.draw import ease_out, partial
from .base import Beat, _display, _font, _round_corners, _smooth

MONO = "/System/Library/Fonts/SFNSMono.ttf"
TYPE_DUR = 0.55      # an address typing in
SWAP_AT = 0.75       # seconds after the source's reveal that the scramble starts
SWAP_DUR = 0.65      # the scramble itself
GLYPHS = "0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"


def _mono(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(MONO, size)


class Relay(Beat):

    EMBLEM = False

    def __init__(self, meant: str, attacker: str, places: list,
                 title: str = "", verdict: tuple = ("EVERY SCREEN MATCHES",
                                                     "THE ATTACKER'S ADDRESS"),
                 **kw):
        super().__init__(**kw)
        if meant == attacker:
            raise ValueError("relay wants two different addresses")
        if not 2 <= len(places) <= 4:
            raise ValueError("relay wants two to four places, the source first")
        self.meant, self.attacker = meant, attacker
        self.places = [str(p).upper() for p in places]
        self.title, self.verdict = title, tuple(verdict)
        n = len(self.places)
        fr, p = self.frame, self.portrait
        L = max(len(meant), len(attacker))
        rows = 2 if p else 3
        self.per_row = -(-L // rows)
        if p:
            cw = fr.w - 2 * 90
            gap = 56
            top = self.head_y + 100
            x0, x1 = 90, 90 + cw
        else:
            gap = 96
            cw = int((fr.w - 2 * self.margin - (n - 1) * gap) / n)
            top = self.head_y + 140
        box_w = cw - 2 * 30 - 2 * 28
        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        self.size = 46 if p else 60
        while d.textlength("0" * self.per_row, font=_mono(self.size)) > box_w:
            self.size -= 2
            if self.size < 30:
                raise ValueError(f"relay: {self.per_row} characters a row do "
                                 f"not fit a {box_w}px card")
        self.adv = d.textlength("0", font=_mono(self.size))
        b = d.textbbox((0, 0), "0", font=_mono(self.size))
        self.lh = (b[3] - b[1]) + int(self.size * 0.5)
        ch = 92 + 26 + rows * self.lh + 60
        if p:
            self.cards = [(x0, top + i * (ch + gap), x1, top + i * (ch + gap) + ch)
                          for i in range(n)]
        else:
            self.cards = [(self.margin + i * (cw + gap), top,
                           self.margin + i * (cw + gap) + cw, top + ch)
                          for i in range(n)]
        self.verdict_y = self.cards[-1][3] + (70 if p else 100)
        # The scramble's noise is fixed per beat, so a re-render is identical.
        rng = random.Random(meant + attacker)
        self.noise = ["".join(rng.choice(GLYPHS) for _ in range(L))
                      for _ in range(8)]

    # --- clocks -------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        n = len(self.places) + 1
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (i / n) * 0.85)
        return self.at(f) - when

    # --- pieces -------------------------------------------------------------

    def _address(self, d, box, text: str, typed: float, col, a: int,
                 scramble: float = 0.0, noise: str = "") -> None:
        """The address in mono, rows of `per_row`, typing in behind a caret.
        `scramble` 0..1 swaps characters from left to right through noise."""
        x0, y0, x1, y1 = box
        mf = _mono(self.size)
        b = d.textbbox((0, 0), "0", font=mf)
        lh = self.lh
        shown = int(round(len(text) * min(1.0, typed)))
        rows = (len(text) + self.per_row - 1) // self.per_row
        block_w = self.adv * min(self.per_row, len(text))
        tx = x0 + (x1 - x0 - block_w) / 2
        ty = y0 + (y1 - y0 - rows * lh) / 2 + 4
        for i, ch in enumerate(text[:shown]):
            r, c = divmod(i, self.per_row)
            if 0 < scramble < 1 and noise:
                edge = scramble * (len(text) + 6)
                if i > edge:
                    ch = self.meant[i] if i < len(self.meant) else ""
                elif i > edge - 6:
                    ch = noise[i % len(noise)]
            d.text((tx + c * self.adv, ty + r * lh), ch, font=mf, fill=col + (a,))
        if 0 < typed < 1:
            r, c = divmod(min(shown, len(text) - 1), self.per_row)
            cx = tx + c * self.adv
            d.rectangle([cx + 2, ty + r * lh + b[1], cx + 6, ty + r * lh + b[3]],
                        fill=self.brand.primary + (a,))

    def _tag(self, d, box, text: str, col, a: int, pulse: float = 0.0) -> None:
        """A pill straddling the card's bottom edge, centred."""
        x0, y0, x1, y1 = box
        tf = _display(32 if self.portrait else 30)
        tb = d.textbbox((0, 0), text, font=tf)
        tw, th = tb[2] - tb[0], tb[3] - tb[1]
        cx, cy = (x0 + x1) / 2, y1
        grow = 6 * pulse
        w2, h2 = tw / 2 + 26 + grow, 27 + grow
        d.rounded_rectangle([cx - w2, cy - h2, cx + w2, cy + h2], radius=h2,
                            fill=col + (a,))
        d.text((cx - tw / 2 - tb[0], cy - th / 2 - tb[1]), text, font=tf,
               fill=(14, 14, 14, a))

    def _card(self, d, box, label: str, enter: float, edge) -> None:
        x0, y0, x1, y1 = box
        a = int(255 * enter)
        d.rounded_rectangle(box, radius=26, fill=(16, 16, 16, int(238 * enter)))
        mx = (x0 + x1) / 2
        pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                              (x0, y0), (mx + 0.5, y0)], 26, seg=10)
        partial(d, pts, max(0.001, _smooth(enter)), edge, 4)
        lf = _font(30 if self.portrait else 28)
        d.text((x0 + 32, y0 + 32), label, font=lf, fill=(205, 205, 205, a))

    def _arrow(self, d, a_box, b_box, p: float) -> None:
        if p <= 0:
            return
        col = (150, 150, 150)
        if self.portrait:
            x = (a_box[0] + a_box[2]) / 2
            s, e = (x, a_box[3] + 14), (x, b_box[1] - 14)
        else:
            y = (a_box[1] + a_box[3]) / 2
            s, e = (a_box[2] + 14, y), (b_box[0] - 14, y)
        q = _smooth(p)
        tip = (s[0] + (e[0] - s[0]) * q, s[1] + (e[1] - s[1]) * q)
        d.line([s, tip], fill=col + (255,), width=6)
        if q > 0.6:
            if self.portrait:
                h = [(tip[0] - 16, tip[1] - 18), (tip[0] + 16, tip[1] - 18), tip]
            else:
                h = [(tip[0] - 18, tip[1] - 16), (tip[0] - 18, tip[1] + 16), tip]
            d.polygon(h, fill=col + (255,))

    # --- the frame ----------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        s0 = self._since(0, f)
        if s0 < 0:
            return
        br = self.brand
        n = len(self.places)
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        sv = self._since(n, f)
        pulse = 0.0
        if sv >= 0:
            pulse = max(0.0, 1.0 - abs(sv - 0.35) / 0.35)

        for i, (box, label) in enumerate(zip(self.cards, self.places)):
            si = self._since(i, f)
            if si < 0:
                continue
            enter = min(1.0, si / 0.5)
            ib = (box[0] + 30, box[1] + 92, box[2] - 30, box[3] - 44)
            if i == 0:
                swap = min(1.0, max(0.0, (si - SWAP_AT) / SWAP_DUR))
                edge = br.negative if swap >= 1 else (110, 110, 110)
                self._card(d, box, label, enter, edge)
                d.rounded_rectangle(ib, radius=14, fill=(6, 6, 6, int(255 * enter)))
                typed = min(1.0, max(0.0, (si - 0.15) / TYPE_DUR))
                if swap <= 0:
                    self._address(d, ib, self.meant, typed, br.ink, int(255 * enter))
                else:
                    col = br.ink if swap < 1 else br.ink
                    self._address(d, ib, self.attacker, 1.0, col, 255,
                                  scramble=swap if swap < 1 else 0.0,
                                  noise=self.noise[int(si * 20) % len(self.noise)])
                if swap >= 1:
                    ta = int(255 * min(1.0, (si - SWAP_AT - SWAP_DUR) / 0.25))
                    self._tag(d, box, "SWAPPED", br.negative, ta)
            else:
                self._arrow(d, self.cards[i - 1], box, si / 0.45)
                cin = min(1.0, max(0.0, (si - 0.25) / 0.45))
                if cin <= 0:
                    continue
                done = si > 0.25 + TYPE_DUR + 0.2
                self._card(d, box, label, cin,
                           br.positive if done else (110, 110, 110))
                d.rounded_rectangle(ib, radius=14, fill=(6, 6, 6, int(255 * cin)))
                typed = min(1.0, max(0.0, (si - 0.35) / TYPE_DUR))
                self._address(d, ib, self.attacker, typed, br.ink, int(255 * cin))
                if done:
                    ta = int(255 * min(1.0, (si - 0.25 - TYPE_DUR - 0.2) / 0.25))
                    self._tag(d, box, "MATCHES", br.positive, ta, pulse)

        if sv >= 0:
            va = int(255 * min(1.0, sv / 0.4))
            rise = int(18 * (1 - ease_out(min(1.0, sv / 0.4))))
            line, under = (self.verdict + ("",))[:2]
            vf = _display(64 if self.portrait else 60)
            uf = _display(48 if self.portrait else 44)
            W = self.frame.w
            lb = d.textbbox((0, 0), line, font=vf)
            d.text(((W - (lb[2] - lb[0])) / 2 - lb[0], self.verdict_y + rise),
                   line, font=vf, fill=(255, 255, 255, va))
            if under:
                ua = int(255 * min(1.0, max(0.0, (sv - 0.35) / 0.4)))
                ub = d.textbbox((0, 0), under, font=uf)
                uy = self.verdict_y + (lb[3] - lb[1]) + 34
                d.text(((W - (ub[2] - ub[0])) / 2 - ub[0], uy), under, font=uf,
                       fill=br.negative + (ua,))
        out.paste(layer, (0, 0), layer)


def swap_time(reveals: list) -> float | None:
    """When the source address finishes scrambling - the glitch cue."""
    return reveals[0] + SWAP_AT + 0.1 if reveals else None
