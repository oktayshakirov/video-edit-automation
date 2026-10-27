"""`blindsign` - the screen the signers approved, and what they really signed.

**Built for `how-does-north-korea-steal-crypto` (2026-10-27), because the
library could not draw the heist's mechanism.** Bybit's signers checked a
routine cold-to-hot transfer on their screens and approved it; the
transaction underneath handed control of the wallet to the attackers. Drift
and Bitget turned on the same gap. Spoken over a stock clip of a laptop it is
a sentence the viewer has to picture; drawn, it is a card that changes under
the approvals. `quorum` draws a threshold being met, `post` a quoted line;
neither shows a display and its payload disagreeing, which is the one thing
this beat is for. Reusable for any blind-signing story: a wallet drainer, an
unlimited token approval, a spoofed withdrawal.

Three reveals, three caption chunks in this order: the card ("The screen
asked for a routine transfer..."), the approvals ("Three signers approved
it..."), the truth ("But what they signed handed over the wallet."). On the
first the card draws round and its rows set; on the second each signer's
disc fills with a tick, 0.42s apart; on the third a scanline sweeps down the
card, tearing the rows it crosses, and everything above it is the real
transaction - its header and every changed value in `brand.negative`. The
ticks stay: they signed it.

**Our card, not a wallet's interface** - drawn in the channel's type, with
plain-English rows, like `post`.

payload: (shown, real, signers, title, heads)
  shown    [(key, value), ...] - what the screen displayed, two to four rows
  real     [(key, value), ...] - what was signed, the same number of rows
  signers  labels under the approval discs, one to four ("SIGNER", "CEO")
  title    the beat's kicker
  heads    (shown header, real header), default
           ("CONFIRM TRANSACTION", "WHAT WAS SIGNED")
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth

SIGN_STEP = 0.42                # seconds between one approval and the next
SIGN_LEAD = 0.15                # first approval after its caption starts
SWEEP_LEAD, SWEEP = 0.10, 1.10  # the scanline: delay, then its travel


def sign_times(reveal: float, n: int) -> list[float]:
    """When each approval lands - shared with the builders' tick cues."""
    return [reveal + SIGN_LEAD + SIGN_STEP * j for j in range(n)]


def sweep_span(reveal: float) -> tuple[float, float]:
    """When the scanline starts and lands - shared with the cues."""
    t0 = reveal + SWEEP_LEAD
    return t0, t0 + SWEEP


class BlindSign(Beat):

    EMBLEM = False

    def __init__(self, shown: list, real: list, signers: list,
                 title: str = "", heads: tuple | None = None, **kw):
        super().__init__(**kw)
        if not 2 <= len(shown) <= 4 or len(real) != len(shown):
            raise ValueError(f"blindsign wants 2-4 shown rows and as many "
                             f"real ones, got {len(shown)} and {len(real)}")
        if not 1 <= len(signers) <= 4:
            raise ValueError(f"blindsign wants 1-4 signers, got {len(signers)}")
        self.shown, self.real = list(shown), list(real)
        self.signers, self.title = list(signers), title
        self.heads = heads or ("CONFIRM TRANSACTION", "WHAT WAS SIGNED")

        fr = self.frame
        p = self.portrait
        self.cw = fr.w - 2 * 70 if p else 1120
        self.x0 = (fr.w - self.cw) // 2
        # **Portrait stacks each row**, the key small over its value: side
        # by side, a 940px card leaves a value ~630px, and "Replace wallet
        # code" at a phone-readable size does not fit in that.
        self.pad = 52 if p else 56
        self.key_w = 0 if p else 270
        self.head_h = 130 if p else 112
        self.row_h = 156 if p else 98
        self.sign_h = 290 if p else 200
        self.ch = self.head_h + self.row_h * len(shown) + self.sign_h
        top = self.head_y + 110
        # Centred on the frame: a drawn beat in a Short burns no caption,
        # so the lower half is the card's to use.
        self.y0 = max(top, (fr.h - self.ch) // 2 + (20 if p else 30))
        self.vsize = 56 if p else 44
        self.hsize = 40 if p else 34

        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        room = self.cw - 2 * self.pad - self.key_w
        for k, v in self.shown + self.real:
            w = d.textlength(v, font=_display(self.vsize))
            if w > room:
                raise ValueError(f"blindsign value {v!r} is {w:.0f}px wide and "
                                 f"a row has {room}px. Shorten it.")
        for h in self.heads:
            w = d.textlength(h, font=_display(self.hsize))
            if w > self.cw - 2 * self.pad:
                raise ValueError(f"blindsign header {h!r} is {w:.0f}px wide. "
                                 f"Shorten it.")

    # --- one state of the card -------------------------------------------

    def _card(self, f: float, real: bool, enter: float) -> Image.Image:
        """The whole card in one state, as an RGBA layer the size of the
        frame. `enter` is the arrival, 0..1."""
        fr, br = self.frame, self.brand
        prim, ink, neg = br.primary, br.ink, br.negative
        layer = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        x0, y0, cw, ch = self.x0, self.y0, self.cw, self.ch
        x1, y1 = x0 + cw, y0 + ch
        a = int(255 * min(1.0, enter))
        edge = neg if real else prim

        d.rounded_rectangle([x0, y0, x1, y1], radius=26,
                            fill=(16, 16, 16, int(236 * min(1.0, enter))))
        d.rounded_rectangle([x0, y0, x1, y0 + self.head_h], radius=26,
                            fill=edge + (int(34 * min(1.0, enter)),),
                            corners=(True, True, False, False))
        d.line([(x0, y0 + self.head_h), (x1, y0 + self.head_h)],
               fill=edge + (int(110 * min(1.0, enter)),), width=2)
        # Rounded like the fill, starting mid-top so the draw has no seam
        # at a corner.
        mx = (x0 + x1) / 2
        pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                              (x0, y0), (mx + 0.5, y0)], 26, seg=10)
        partial(d, pts, max(0.001, self.open_p(f, 0.7) if enter > 0 else 0),
                edge, 4)

        # The header: a status dot and the line.
        head = self.heads[1] if real else self.heads[0]
        hf = _display(self.hsize)
        b = d.textbbox((0, 0), head, font=hf)
        hy = y0 + (self.head_h - (b[3] - b[1])) / 2 - b[1]
        d.ellipse([x0 + self.pad, y0 + self.head_h / 2 - 9,
                   x0 + self.pad + 18, y0 + self.head_h / 2 + 9],
                  fill=edge + (a,))
        shadow_text(d, (x0 + self.pad + 38, hy), head, hf, edge + (a,),
                    alpha=a)

        # The rows. Each sets a beat after the one above it.
        rows = self.real if real else self.shown
        kf, vf = _font(30 if not self.portrait else 30), _display(self.vsize)
        for i, (k, v) in enumerate(rows):
            e = min(1.0, max(0.0, (enter - 0.25 - 0.12 * i) / 0.4))
            if e <= 0:
                continue
            ra = int(255 * ease_out(e))
            ry = y0 + self.head_h + i * self.row_h
            mid = ry + self.row_h / 2
            changed = real and v != self.shown[i][1]
            kb = d.textbbox((0, 0), k.upper(), font=kf)
            vb = d.textbbox((0, 0), v, font=vf)
            if self.portrait:
                ky = ry + 30 - kb[1]
                vy = ry + 74 - vb[1]
            else:
                ky = mid - (kb[3] - kb[1]) / 2 - kb[1]
                vy = mid - (vb[3] - vb[1]) / 2 - vb[1]
            d.text((x0 + self.pad, ky), k.upper(), font=kf,
                   fill=(150, 150, 150, ra))
            col = neg if changed else ink
            shadow_text(d, (x0 + self.pad + self.key_w, vy),
                        v, vf, col + (ra,), alpha=ra)
            if i < len(rows) - 1:
                d.line([(x0 + self.pad, ry + self.row_h),
                        (x1 - self.pad, ry + self.row_h)],
                       fill=(255, 255, 255, int(22 * ease_out(e))), width=1)
        return layer

    # --- the approvals, drawn over both states -----------------------------

    def _signers(self, d: ImageDraw.ImageDraw, f: float, enter: float) -> None:
        br = self.brand
        prim, ink = br.primary, br.ink
        n = len(self.signers)
        top = self.y0 + self.head_h + self.row_h * len(self.shown)
        a = int(255 * min(1.0, max(0.0, (enter - 0.5) / 0.4)))
        if a <= 0:
            return
        lf = _font(26 if not self.portrait else 32)
        lab = "SIGNATURES"
        b = d.textbbox((0, 0), lab, font=lf)
        d.text((self.x0 + self.cw / 2 - (b[2] - b[0]) / 2 - b[0], top + 22 - b[1]),
               lab, font=lf, fill=(150, 150, 150, a))
        R, step = (52, 250) if self.portrait else (36, 200)
        cy = top + (138 if self.portrait else 96)
        cx0 = self.x0 + self.cw / 2 - step * (n - 1) / 2
        rv = self.reveals or []
        when = sign_times(rv[1], n) if len(rv) > 1 else [None] * n
        t = self.at(f)
        for j, name in enumerate(self.signers):
            cx = cx0 + j * step
            p = (_smooth((t - when[j]) / 0.30) if when[j] is not None
                 and t >= when[j] else 0.0)
            d.ellipse([cx - R, cy - R, cx + R, cy + R],
                      outline=prim + (a,), width=4,
                      fill=prim + (int(255 * p),) if p > 0 else None)
            if p > 0:
                tick = [(cx - R * 0.42, cy + R * 0.02),
                        (cx - R * 0.10, cy + R * 0.34),
                        (cx + R * 0.46, cy - R * 0.32)]
                partial(d, tick, min(1.0, p * 1.4), (16, 16, 16), 7)
            nb = d.textbbox((0, 0), name.upper(), font=lf)
            col = ink if p > 0 else (150, 150, 150)
            d.text((cx - (nb[2] - nb[0]) / 2 - nb[0], cy + R + 18 - nb[1]),
                   name.upper(), font=lf, fill=col + (a,))

    # --- the frame -----------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        e0 = self.due(0, 3, f)
        if e0 < 0:
            return
        rv = self.reveals or []
        t = self.at(f)
        enter = min(1.0, max(0.0, (t - (rv[0] if rv else self.start)) / 0.9))
        s = 0.0
        if len(rv) > 2 and t >= sweep_span(rv[2])[0]:
            t0, t1 = sweep_span(rv[2])
            s = _smooth((t - t0) / (t1 - t0))

        rise = int(22 * (1 - ease_out(enter)))
        shown = self._card(f, False, enter) if s < 1.0 else None
        real = self._card(f, True, enter) if s > 0.0 else None
        if s <= 0.0:
            card = shown
        elif s >= 1.0:
            card = real
        else:
            card = self._sweep(shown, real, s, f)
        d = ImageDraw.Draw(card, "RGBA")
        self._signers(d, f, enter)
        out.paste(card, (0, rise), card)

    def _sweep(self, shown: Image.Image, real: Image.Image, s: float,
               f: float) -> Image.Image:
        """Real above the scanline, shown below, the rows it crosses torn."""
        y0, y1 = self.y0, self.y0 + self.ch
        sy = int(y0 + (y1 - y0) * s)
        A, B = np.asarray(shown).copy(), np.asarray(real)
        A[:sy] = B[:sy]
        # Tear a band around the line: slices shifted sideways, the colour
        # channels split. Seeded by the frame so a re-render is identical.
        rng = np.random.default_rng(int(f * 10000) + 7)
        band = 46
        lo, hi = max(y0, sy - band), min(y1, sy + band)
        x0, x1 = self.x0 - 40, self.x0 + self.cw + 40
        y = lo
        while y < hi:
            h = int(rng.integers(4, 14))
            dx = int(rng.integers(-38, 39))
            seg = A[y:y + h, x0:x1].copy()
            A[y:y + h, x0:x1] = np.roll(seg, dx, axis=1)
            if rng.random() < 0.5:
                A[y:y + h, x0:x1, 0] = np.roll(seg[..., 0], dx + 8, axis=1)
            y += h
        card = Image.fromarray(A, "RGBA")
        d = ImageDraw.Draw(card, "RGBA")
        neg = self.brand.negative
        d.rectangle([self.x0 - 10, sy - 2, self.x0 + self.cw + 10, sy + 2],
                    fill=neg + (255,))
        d.rectangle([self.x0 - 10, sy - 10, self.x0 + self.cw + 10, sy + 10],
                    fill=neg + (60,))
        return card
