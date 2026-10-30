"""`sweep` - a wallet handed to someone else's code, drained, then left open.

**Built for the Binance hack (2026-10-30), because the library could not draw
the heist's mechanism.** According to TRM Labs, one transaction carried fifty
pre-signed authorizations from a Binance hot wallet on Ethereum, which pointed
the wallet at an attacker's sweeper contract. The wallet was empty in about
three and a half minutes, and because the delegation stayed in place, every
deposit that arrived for hours afterwards was swept straight out. `blindsign`
draws a screen disagreeing with what was signed; nothing drew a wallet whose
own code now works for someone else, and the "it kept happening" half of the
story is the part a sentence cannot make vivid. Reusable for any drainer, a
hijacked delegation or a compromised hot wallet.

Four reveals, four caption chunks in this order: the wallet ("one transaction
hit Binance's hot wallet"), the hand-over ("it carried fifty signed
authorizations..."), the drain ("...the wallet was empty"), the deposits
("every new deposit was swept straight out"). On the first the wallet card
draws round with a full balance; on the second the attacker's card arrives,
a line draws from the wallet into it with the link label on it, and the
wallet turns `brand.negative`; on the third the balance runs out along that
line; on the fourth each deposit lights its time in the log, travels into the
wallet and on out to the attacker, one after another.

Same template as `quorum` and `blindsign`: line art in the brand colour, one
object per spoken phrase, one state change per phrase.

payload: (wallet, attacker, link, drained, deposits, title)
  wallet    (name, sub) - "BINANCE HOT WALLET", "ETHEREUM"
  attacker  (name, sub) - "ATTACKER CONTRACT", "SWEEPER"
  link      the label on the hand-over line - "50 SIGNED AUTHORIZATIONS"
  drained   what the balance line reads once empty - "EMPTY IN 3 MIN 24 S"
  deposits  the log, three to eight short strings - times, "20:41 UTC"
  title     the beat's kicker
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth

HAND_LEAD = 0.20                 # the hand-over after its caption starts
DRAIN_LEAD, DRAIN = 0.15, 1.60   # the balance running out: delay, length
DEP_LEAD, DEP_STEP = 0.30, 0.48  # the first deposit, then the gap between
HOP = 0.34                       # one leg of a deposit's trip


def hand_time(reveal: float) -> float:
    """When the wallet turns - shared with the builders' cues."""
    return reveal + HAND_LEAD


def drain_span(reveal: float) -> tuple[float, float]:
    """When the balance starts running out, and when it is empty."""
    t0 = reveal + DRAIN_LEAD
    return t0, t0 + DRAIN


def deposit_times(reveal: float, n: int) -> list[float]:
    """When each deposit lands in the log - shared with the tick cues."""
    return [reveal + DEP_LEAD + DEP_STEP * j for j in range(n)]


class Sweep(Beat):

    EMBLEM = False

    def __init__(self, wallet: tuple, attacker: tuple, link: str,
                 drained: str, deposits: list, title: str = "", **kw):
        super().__init__(**kw)
        if not 3 <= len(deposits) <= 8:
            raise ValueError(f"sweep wants 3-8 deposits, got {len(deposits)}")
        self.wallet, self.attacker = tuple(wallet), tuple(attacker)
        self.link, self.drained = link, drained
        self.deposits, self.title = list(deposits), title

        fr, p = self.frame, self.portrait
        # Three boxes: the deposit log, the wallet under it, the attacker.
        # Portrait runs all three down the frame, because 9:16 has height to
        # spare. Landscape keeps the log over the wallet and puts the
        # attacker to the right, so the hand-over line has room for its
        # label - a single row of three cards left it ~190px and the label
        # sat on both cards.
        if p:
            cx = fr.w // 2
            self.log = (cx - 450, 430, 900, 250)
            self.box = (cx - 380, 800, 760, 290)
            self.atk = (cx - 380, 1380, 760, 170)
        else:
            # Sized up after the first cut: at 540px cards the beat sat
            # small and low with half the frame empty.
            self.log = (120, 300, 640, 220)
            self.box = (120, 600, 640, 290)
            self.atk = (1270, 665, 600, 160)
        self.tsize = 46 if p else 40
        self.ssize = 30 if p else 27

        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        for (x, y, w, h), name in ((self.box, self.wallet[0]),
                                   (self.atk, self.attacker[0])):
            tw = d.textlength(name, font=_display(self.tsize))
            if tw > w - 2 * 40:
                raise ValueError(f"sweep name {name!r} is {tw:.0f}px wide and "
                                 f"its card has {w - 80}px. Shorten it.")
        for s in (self.link, self.drained):
            tw = d.textlength(s, font=_display(self.ssize))
            room = self.box[2] if p else self.atk[0] - (self.box[0] + self.box[2])
            if tw > room:
                raise ValueError(f"sweep label {s!r} is {tw:.0f}px wide. "
                                 f"Shorten it.")

    # --- geometry ------------------------------------------------------------

    def _ports(self):
        """Where a deposit leaves the log, enters and leaves the wallet, and
        reaches the attacker."""
        lx, ly, lw, lh = self.log
        bx, by, bw, bh = self.box
        ax, ay, aw, ah = self.atk
        c = bx + bw / 2
        if self.portrait:
            return (c, ly + lh), (c, by), (c, by + bh), (c, ay)
        return ((c, ly + lh), (c, by), (bx + bw, by + bh / 2),
                (ax, ay + ah / 2))

    @staticmethod
    def _lerp(a, b, p):
        return (a[0] + (b[0] - a[0]) * p, a[1] + (b[1] - a[1]) * p)

    # --- pieces --------------------------------------------------------------

    def _card(self, d, box, e, edge, name, sub, f):
        """A rounded card drawing its outline round as it arrives (`e` 0..1)."""
        x, y, w, h = box
        a = int(255 * min(1.0, e))
        d.rounded_rectangle([x, y, x + w, y + h], radius=24,
                            fill=(16, 16, 16, int(236 * min(1.0, e))))
        mx = x + w / 2
        pts = _round_corners([(mx, y), (x + w, y), (x + w, y + h), (x, y + h),
                              (x, y), (mx + 0.5, y)], 24, seg=10)
        partial(d, pts, max(0.001, min(1.0, e / 0.8)), edge, 4)
        tf, sf = _display(self.tsize), _font(self.ssize)
        tb = d.textbbox((0, 0), name, font=tf)
        sb = d.textbbox((0, 0), sub, font=sf)
        top = y + (36 if self.portrait else 32)
        shadow_text(d, (x + (w - (tb[2] - tb[0])) / 2 - tb[0], top - tb[1]),
                    name, tf, edge + (a,), alpha=a)
        d.text((x + (w - (sb[2] - sb[0])) / 2 - sb[0],
                top + (tb[3] - tb[1]) + 18 - sb[1]),
               sub.upper(), font=sf, fill=(150, 150, 150, a))
        return top + (tb[3] - tb[1]) + 18 + (sb[3] - sb[1])

    def _balance(self, d, below, level, edge, label, lab_col, a):
        """The wallet's balance bar, `level` 0..1 of full."""
        x, y, w, h = self.box
        pad = 48
        by = below + (40 if self.portrait else 30)
        bh = 34 if self.portrait else 28
        d.rounded_rectangle([x + pad, by, x + w - pad, by + bh], radius=bh // 2,
                            outline=(255, 255, 255, int(60 * a / 255)), width=2)
        if level > 0.004:
            d.rounded_rectangle([x + pad + 4, by + 4,
                                 x + pad + 4 + (w - 2 * pad - 8) * level,
                                 by + bh - 4], radius=(bh - 8) // 2,
                                fill=edge + (a,))
        lf = _display(self.ssize)
        lb = d.textbbox((0, 0), label, font=lf)
        shadow_text(d, (x + (w - (lb[2] - lb[0])) / 2 - lb[0],
                        by + bh + 22 - lb[1]), label, lf, lab_col + (a,),
                    alpha=a)

    def _log(self, d, e, lit, f):
        """The deposit log: a header and one row per deposit, lit as each
        arrives."""
        x, y, w, h = self.log
        prim, ink = self.brand.primary, self.brand.ink
        a = int(255 * min(1.0, e))
        d.rounded_rectangle([x, y, x + w, y + h], radius=24,
                            fill=(16, 16, 16, int(220 * min(1.0, e))),
                            outline=(255, 255, 255, int(70 * min(1.0, e))),
                            width=2)
        hf = _font(self.ssize)
        head = "NEW DEPOSITS"
        hb = d.textbbox((0, 0), head, font=hf)
        d.text((x + (w - (hb[2] - hb[0])) / 2 - hb[0], y + 26 - hb[1]), head,
               font=hf, fill=(150, 150, 150, a))
        rf = _display(self.ssize + (6 if self.portrait else 2))
        n = len(self.deposits)
        top = 80 if self.portrait else 66
        cols = (n + 1) // 2
        cw, rh = w / cols, (h - top) / 2
        cells = [(x + cw * (j % cols) + cw / 2, y + top + rh * (j // cols)
                  + rh / 2) for j in range(n)]
        for j, (cx, cy) in enumerate(cells):
            p = lit[j]
            col = prim if p > 0 else (90, 90, 90)
            ra = int(a * (0.55 + 0.45 * p))
            s = self.deposits[j]
            b = d.textbbox((0, 0), s, font=rf)
            shadow_text(d, (cx - (b[2] - b[0]) / 2 - b[0],
                            cy - (b[3] - b[1]) / 2 - b[1]), s, rf, col + (ra,),
                        alpha=ra)

    # --- the frame -------------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        rv = self.reveals or []
        if not rv:
            rv = [self.start + self.hold * k * 0.2 for k in range(4)]
        t = self.at(f)
        if t < rv[0]:
            return
        br = self.brand
        prim, neg, ink = br.primary, br.negative, br.ink
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        S, Win, Wout, A = self._ports()

        # 0 - the wallet, full.
        e0 = min(1.0, (t - rv[0]) / 0.9)
        # 1 - the hand-over: the attacker's card, the line, the wallet turns.
        th = hand_time(rv[1]) if len(rv) > 1 else None
        e1 = min(1.0, max(0.0, (t - th) / 0.6)) if th is not None else 0.0
        turned = _smooth((t - th) / 0.25) if th is not None and t >= th else 0.0
        # 2 - the drain.
        level, drained = 1.0, False
        if len(rv) > 2 and t >= drain_span(rv[2])[0]:
            d0, d1 = drain_span(rv[2])
            q = _smooth((t - d0) / (d1 - d0))
            level, drained = 1.0 - q, q >= 1.0
        # 3 - the deposits.
        dep = deposit_times(rv[3], len(self.deposits)) if len(rv) > 3 else []
        e3 = min(1.0, max(0.0, (t - rv[3]) / 0.5)) if len(rv) > 3 else 0.0

        if e1 > 0:
            # The line from the wallet into the attacker, drawn on, with the
            # link label riding over its middle.
            partial(d, [Wout, A], _smooth(e1), neg, 5)
            if e1 >= 1.0:
                self._head(d, Wout, A, neg, 22)
            self._card(d, self.atk, e1, neg, *self.attacker, f)

        if e3 > 0:
            lit = [_smooth((t - w) / 0.2) if t >= w else 0.0 for w in dep]
            self._log(d, e3, lit, f)

        # The wallet itself, gold until it turns.
        edge = tuple(int(prim[k] + (neg[k] - prim[k]) * turned) for k in range(3))
        below = self._card(d, self.box, e0, edge, *self.wallet, f)
        # A deposit sitting in the wallet for an instant before it is swept.
        blip = 0.0
        for w in dep:
            u = t - (w + HOP)
            if 0 <= u < HOP:
                blip = max(blip, 0.14 * (1 - u / HOP))
        if drained:
            label, lab_col = self.drained, neg
        else:
            label, lab_col = "BALANCE", (150, 150, 150)
        self._balance(d, below, max(level, blip), edge, label, lab_col,
                      int(255 * min(1.0, e0)))

        # Value leaving: a stream along the line while the drain runs, and
        # one dot per deposit, log -> wallet -> attacker.
        if len(rv) > 2 and 0 < level < 1:
            for k in range(6):
                p = ((t * 1.6) + k / 6) % 1.0
                x, y = self._lerp(Wout, A, p)
                d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=prim + (230,))
        for w in dep:
            u = t - w
            if 0 <= u < 2 * HOP:
                if u < HOP:
                    x, y = self._lerp(S, Win, _smooth(u / HOP))
                else:
                    x, y = self._lerp(Wout, A, _smooth((u - HOP) / HOP))
                d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=prim + (255,))

        # The link label last, so nothing travelling the line covers it.
        if e1 > 0:
            la = int(255 * ease_out(min(1.0, max(0.0, (t - th - 0.3) / 0.4))))
            if la:
                lf = _display(self.ssize)
                lb = d.textbbox((0, 0), self.link, font=lf)
                mx, my = self._lerp(Wout, A, 0.5)
                lw, lh = lb[2] - lb[0], lb[3] - lb[1]
                bx0 = mx - lw / 2 - 18 - (4 if self.portrait else 0)
                by0 = my - lh / 2 - 15 if self.portrait else my - lh - 58
                d.rounded_rectangle([bx0, by0, bx0 + lw + 36 + (8 if self.portrait else 0),
                                     by0 + lh + 30], radius=10,
                                    fill=neg + (int(la * 0.92),))
                d.text((bx0 + 18 + (4 if self.portrait else 0) - lb[0],
                        by0 + 15 - lb[1]), self.link, font=lf,
                       fill=(255, 255, 255, la))

        rise = int(20 * (1 - ease_out(e0)))
        out.paste(layer, (0, rise), layer)
