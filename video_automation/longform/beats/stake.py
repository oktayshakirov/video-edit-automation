"""`stake` - a fortune drawn as a slice of a company, then the company re-valued.

**Built for `which-billionaires-own-crypto` (2026-11-04), because the
library could not draw the thing the whole topic turns on.** The largest
crypto fortunes are stakes in private companies - Binance, Tether - so a
"net worth" is an ownership share multiplied by somebody's guess at what the
company would sell for. Forbes and Bloomberg disagree about CZ by sixty
billion dollars without either being wrong. Said over a stock clip that is
arithmetic held in the head; drawn, it is one block getting bigger while the
slices on it stay the same share. `bars` compares sizes, `split` divides a
whole into equal claims, `gauge` reads one value; none of them shows a share
staying fixed while what it is a share *of* changes. `quorum`'s template:
line art in the brand colour, one object per phrase, one state change.

Reveals, one caption chunk each, in this order:

  0      the company: its block draws on, sized by the first valuation, with
         the valuation and what it is ("FORBES' VALUATION") at its right edge
  1..n   each holder: their slice fills, a leader drops to their name and the
         fortune that slice is worth (popped in, never counted - `$40B` on the
         way to `$89B` would read as a figure, `beats.md`)
  n+1..  each further valuation: the block grows (or shrinks) to it, the
         slices with it, and every fortune is recomputed as stake x value

payload: (company, valuations, holders, title)
  company     (name, sub) - "TETHER", "issuer of USDT"
  valuations  [(value, label, note), ...] - value a number in billions, label
              what is printed ("$200B"), note what it is ("FORBES' VALUATION")
  holders     [(name, stake, fortune), ...] - stake 0..1, fortune the printed
              figure at the first valuation (the source's own number, so it
              can differ a little from stake x value); later valuations print
              stake x value
  title       the beat's kicker
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth

ENTER = 0.70        # the block drawing on
FILL = 0.55         # a slice filling
GROW = 1.10         # the block re-sizing to a new valuation


def grow_span(reveal: float) -> tuple[float, float]:
    """When a re-valuation starts and settles - shared with the cues."""
    return reveal + 0.10, reveal + 0.10 + GROW


def _money(v: float) -> str:
    """Billions, the way the sources print them: $225B, $9.5B."""
    return f"${v:,.0f}B" if v >= 10 else f"${v:.1f}B"


class Stake(Beat):

    EMBLEM = False

    def __init__(self, company: tuple, valuations: list, holders: list,
                 title: str = "", **kw):
        super().__init__(**kw)
        if not valuations:
            raise ValueError("stake needs at least one valuation")
        if not 1 <= len(holders) <= 3:
            raise ValueError(f"stake draws one to three holders, got {len(holders)}")
        if sum(h[1] for h in holders) > 1.0 + 1e-9:
            raise ValueError("stake holders own more than 100% between them")
        self.company, self.valuations = company, list(valuations)
        self.holders, self.title = list(holders), title

        fr, p = self.frame, self.portrait
        self.max_w = fr.w - 2 * (self.margin + 20) if p else 1460
        self.block_h = 270 if p else 210
        self.vmax = max(v[0] for v in self.valuations)
        self.x0 = (fr.w - self.max_w) // 2 if p else 230
        # Portrait type is ~1.4x: at the landscape sizes the first 9:16
        # render was a strip of small print in the top quarter of a phone.
        self.name_f = _display(84 if p else 56)
        self.val_f = _display(96 if p else 62)
        self.note_f = _font(34 if p else 26)
        self.who_f = _font(46 if p else 34)
        self.fort_f = _display(100 if p else 66)
        self.at_f = _font(32 if p else 24)

        # Holder labels: a row under the block when the names fit their
        # columns, else a column (three holders in portrait). The valuation
        # has its own row above the company's name: on a block sized at 40%
        # of the frame the two could not share one (the first render
        # overprinted "TETHER" with "$200B").
        n = len(self.holders)
        top = self.head_y + (110 if p else 70)
        self.block_y = top + (230 if p else 210)
        if p:
            # Centre the whole group on the frame rather than hanging it off
            # the kicker: block, labels and the valuation row above it.
            group = 260 + self.block_h + 140 + 2 * 230
            self.block_y = max(self.block_y, int((fr.h - group) / 2 + 260))
        self.label_y = self.block_y + self.block_h + (140 if p else 120)
        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        widest = max(max(d.textlength(nm, font=self.who_f),
                         d.textlength(ft, font=self.fort_f))
                     for nm, _, ft in self.holders)
        row_w = min(520, self.max_w // n)
        if widest <= row_w - 48:
            self.label_w, self.label_dy = row_w, 0
        else:
            self.label_w, self.label_dy = self.max_w, (240 if p else 190)
        for name, _, fortune in self.holders:
            for txt, f in ((name, self.who_f), (fortune, self.fort_f)):
                w = d.textlength(txt, font=f)
                if w > self.label_w - 48:
                    raise ValueError(f"stake label {txt!r} is {w:.0f}px and the "
                                     f"column has {self.label_w - 48}px")
        for v, label, note in self.valuations:
            w = d.textlength(note.upper(), font=self.note_f)
            if w > (fr.w - 2 * self.margin) * 0.6:
                raise ValueError(f"stake note {note!r} is too wide ({w:.0f}px)")

    # --- clocks ---------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        if i >= len(rv):
            return -1.0
        t = self.at(f) - rv[i]
        return t if t >= 0 else -1.0

    def _value(self, f: float) -> tuple[float, int, float]:
        """The block's current value, the index of the valuation it is moving
        to, and how far along that move is (1.0 when settled)."""
        k0 = 1 + len(self.holders)
        value, idx, p = self.valuations[0][0], 0, 1.0
        for j in range(1, len(self.valuations)):
            t = self._since(k0 + j - 1, f)
            if t < 0:
                break
            a, b = grow_span(0.0)
            p = _smooth((t - a) / (b - a))
            value = self.valuations[j - 1][0] + (self.valuations[j][0]
                                                 - self.valuations[j - 1][0]) * p
            idx = j
        return value, idx, p

    # --- the frame ------------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        t0 = self._since(0, f)
        if t0 < 0:
            return
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        self._draw(d, f, t0)
        out.paste(layer, (0, 0), layer)

    def _draw(self, d, f, t0) -> None:
        br, p = self.brand, self.portrait
        prim, ink, grey = br.primary, br.ink, (150, 150, 150)
        enter = _smooth(t0 / ENTER)
        a = int(255 * min(1.0, t0 / 0.35))
        value, idx, gp = self._value(f)

        w = self.max_w * value / self.vmax
        x0, y0, h = self.x0, self.block_y, self.block_h
        x1, y1 = x0 + w, y0 + h

        # The company's name above the block's left edge.
        name, sub = self.company
        b = d.textbbox((0, 0), name.upper(), font=self.name_f)
        ny = y0 - 34 - (b[3] - b[1]) - b[1]
        shadow_text(d, (x0 - b[0], ny), name.upper(), self.name_f,
                    ink + (a,), alpha=a)
        if sub:
            sf = self.note_f
            sb = d.textbbox((0, 0), sub.upper(), font=sf)
            d.text((x0 + (b[2] - b[0]) + 26 - sb[0],
                    y0 - 34 - (sb[3] - sb[1]) - sb[1] - 6), sub.upper(),
                   font=sf, fill=grey + (a,))

        # The block: its outline draws round, then a dark fill comes up.
        d.rectangle([x0, y0, x1, y1], fill=(14, 14, 14, int(220 * enter)))
        pts = _round_corners([(x0, y0), (x1, y0), (x1, y1), (x0, y1),
                              (x0, y0 + 0.5)], 6, seg=4)
        partial(d, pts, max(0.001, enter), prim, 4)

        # The slices, left to right, each filling on its own reveal.
        cx = x0
        centres = []
        for i, (who, stake, fortune) in enumerate(self.holders):
            sw = w * stake
            t = self._since(1 + i, f)
            fp = _smooth(t / FILL) if t >= 0 else 0.0
            if fp > 0:
                alpha = 255 if i == 0 else 150
                d.rectangle([cx + 3, y0 + 3, cx + 3 + max(0.0, (sw - 6) * fp),
                             y1 - 3], fill=prim + (int(alpha * min(1.0, fp * 1.5)),))
                pct = f"{round(stake * 100)}%"
                pf = _display(52 if p else 50)
                pb = d.textbbox((0, 0), pct, font=pf)
                if sw - 20 > pb[2] - pb[0] and fp > 0.6:
                    pa = int(255 * (fp - 0.6) / 0.4)
                    d.text((cx + sw / 2 - (pb[2] - pb[0]) / 2 - pb[0],
                            y0 + h / 2 - (pb[3] - pb[1]) / 2 - pb[1]), pct,
                           font=pf, fill=(16, 16, 16, pa))
            # A divider where the slice ends, once it has filled.
            if fp >= 1.0:
                d.line([(cx + sw, y0 + 3), (cx + sw, y1 - 3)],
                       fill=(16, 16, 16, 255), width=4)
            centres.append((cx + sw / 2, fp, t))
            cx += sw

        # "Everyone else" in what is left, once every holder has been named.
        rest = x1 - cx
        tl = self._since(len(self.holders), f)
        if tl > 0.4 and rest > 260:
            ra = int(255 * min(1.0, (tl - 0.4) / 0.4))
            rb = d.textbbox((0, 0), "EVERYONE ELSE", font=self.note_f)
            d.text((cx + rest / 2 - (rb[2] - rb[0]) / 2 - rb[0],
                    y0 + h / 2 - (rb[3] - rb[1]) / 2 - rb[1]), "EVERYONE ELSE",
                   font=self.note_f, fill=grey + (ra,))

        # The valuation at the block's right edge, travelling with it, and
        # crossfading on a re-valuation (old out in the first half, new in
        # the second, so the two never overprint).
        def val_text(j, alpha):
            if alpha <= 0:
                return
            _, label, note = self.valuations[j]
            vb = d.textbbox((0, 0), label, font=self.val_f)
            nb = d.textbbox((0, 0), note.upper(), font=self.note_f)
            gap = 22
            total = (vb[2] - vb[0]) + gap + (nb[2] - nb[0])
            vx = max(x0, x1 - total)
            vy = y0 - (180 if p else 140) - (vb[3] - vb[1])
            shadow_text(d, (vx - vb[0], vy - vb[1]), label, self.val_f,
                        prim + (alpha,), alpha=alpha)
            d.text((vx + (vb[2] - vb[0]) + gap - nb[0],
                    vy + (vb[3] - vb[1]) - (nb[3] - nb[1]) - nb[1]),
                   note.upper(), font=self.note_f, fill=grey + (alpha,))
        if idx == 0:
            val_text(0, a)
        else:
            val_text(idx - 1, int(a * max(0.0, 1 - 2 * gp)))
            val_text(idx, int(a * max(0.0, 2 * gp - 1)))

        # The holders' labels, each with a leader from its slice.
        for i, (who, stake, fortune) in enumerate(self.holders):
            sx, fp, t = centres[i]
            if t < 0:
                continue
            la = int(255 * min(1.0, max(0.0, (t - 0.25) / 0.35)))
            lx = self.x0 + (0 if self.label_dy else i * self.label_w)
            ly = self.label_y + i * self.label_dy
            lead = _smooth((t - 0.15) / 0.45)
            # Leader: down from the slice, across to the label's column.
            mid = y1 + 44 + (0 if self.label_dy else i * 14)
            path = [(sx, y1 + 6), (sx, mid), (lx + 8, mid), (lx + 8, ly - 14)]
            if abs(sx - (lx + 8)) < 2:
                path = [(sx, y1 + 6), (sx, ly - 14)]
            partial(d, _round_corners(path, 14, seg=5), max(0.001, lead),
                    prim + (200,), 3)
            if la <= 0:
                continue
            rise = int(14 * (1 - ease_out(la / 255)))
            wb = d.textbbox((0, 0), who, font=self.who_f)
            d.text((lx + 28 - wb[0], ly + rise - wb[1]), who, font=self.who_f,
                   fill=ink + (la,))
            fy = ly + (wb[3] - wb[1]) + 18 + rise
            # The fortune: the source's figure at the first valuation, then
            # stake x value once the block has moved.
            def fort(txt, alpha, at_label):
                if alpha <= 0:
                    return
                fb = d.textbbox((0, 0), txt, font=self.fort_f)
                shadow_text(d, (lx + 28 - fb[0], fy - fb[1]), txt, self.fort_f,
                            prim + (alpha,), alpha=alpha)
                ab = d.textbbox((0, 0), at_label, font=self.at_f)
                d.text((lx + 28 - ab[0], fy + (fb[3] - fb[1]) + 16 - ab[1]),
                       at_label, font=self.at_f, fill=grey + (alpha,))
            def at(j):
                return f"AT {self.valuations[j][1]}"
            if idx == 0:
                fort(fortune, la, at(0))
            else:
                prev = (fortune if idx == 1
                        else _money(stake * self.valuations[idx - 1][0]))
                fort(prev, int(la * max(0.0, 1 - 2 * gp)), at(idx - 1))
                fort(_money(stake * self.valuations[idx][0]),
                     int(la * max(0.0, 2 * gp - 1)), at(idx))
