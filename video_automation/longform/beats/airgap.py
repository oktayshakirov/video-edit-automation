"""`airgap` - a request goes into a signing device; only a signature comes out.

**Built for `hardware-wallet` (2026-11-12), because the library drew a
signing flow as a `steps` track** - four boxes of words in a row, which is a
list, not a mechanism. The point of a hardware wallet is *where things are*:
the computer is online, the device is not, the transaction crosses the cable
one way, the signature crosses back, and the key never moves. That is a
picture of two places and what travels between them, and nothing here drew
it. Reusable for any signer kept apart from the network: a multisig
co-signer, an air-gapped QR wallet, a validator's remote signer, a passkey.

Two cards and a cable. Four reveals, four caption chunks in this order:

1. the request ("Your computer prepares the transaction") - both cards
   arrive, the transaction slip types onto the computer;
2. the crossing ("the device shows it on its own screen") - a TRANSACTION
   chip travels the cable, the device's screen lights with the same lines;
3. the approval ("you check it and press the button") - the device's button
   is pressed, its screen says APPROVED;
4. the return ("and only the signature comes back") - a SIGNATURE chip
   travels back, the key in the device gets its ring and NEVER LEAVES.

The chips move on `span_p`, so each crossing lasts as long as its phrase.

payload: (lines, title, labels)
  lines   [(key, value), ...]  up to three rows of the transaction
  title   the beat's kicker
  labels  optional (left, left_tag, right, right_tag, key_label, stays)
          default ("YOUR COMPUTER", "ONLINE", "HARDWARE WALLET", "OFFLINE",
          "PRIVATE KEY", "NEVER LEAVES")

Landscape sets the cards side by side; portrait stacks them, computer on
top, and the cable runs down.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _round_corners, _smooth

LABELS = ("YOUR COMPUTER", "ONLINE", "HARDWARE WALLET", "OFFLINE",
          "PRIVATE KEY", "NEVER LEAVES")


class Airgap(Beat):

    EMBLEM = False

    def __init__(self, lines: list, title: str = "",
                 labels: tuple | None = None, **kw):
        super().__init__(**kw)
        if not 1 <= len(lines) <= 3:
            raise ValueError("airgap wants one to three transaction rows")
        self.lines, self.title = [tuple(x) for x in lines], title
        self.labels = tuple(labels) if labels else LABELS
        if len(self.labels) != 6:
            raise ValueError("airgap labels are (left, left_tag, right, "
                             "right_tag, key_label, stays)")
        fr, p = self.frame, self.portrait
        if p:
            cw, ch = fr.w - 2 * 90, 470
            x = 90
            top = self.head_y + 120
            self.A = (x, top, x + cw, top + ch)
            self.B = (x, top + ch + 170, x + cw, top + 2 * ch + 170 + 60)
        else:
            cw, ch = 690, 560
            top = self.head_y + 110
            self.A = (self.margin + 20, top, self.margin + 20 + cw, top + ch)
            bx = fr.w - self.margin - 20 - cw
            self.B = (bx, top, bx + cw, top + ch)
        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        vf = _font(48 if p else 46)
        for k, v in self.lines:
            if d.textlength(v, font=vf) > (self.A[2] - self.A[0]) - 150:
                raise ValueError(f"airgap value {v!r} is too wide for the slip")

    # --- clocks -------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        rv = self.reveals or []
        when = (rv[i] if i < len(rv)
                else self.start + self.hold * (i / 4) * 0.85)
        return self.at(f) - when

    # --- pieces -------------------------------------------------------------

    def _card(self, d, box, label, tag, online: bool, enter: float) -> None:
        br = self.brand
        x0, y0, x1, y1 = box
        d.rounded_rectangle(box, radius=28, fill=(16, 16, 16, int(238 * enter)))
        mx = (x0 + x1) / 2
        pts = _round_corners([(mx, y0), (x1, y0), (x1, y1), (x0, y1),
                              (x0, y0), (mx + 0.5, y0)], 28, seg=10)
        partial(d, pts, max(0.001, _smooth(enter)),
                br.negative if online else br.primary, 4)
        a = int(255 * enter)
        lf = _font(32 if self.portrait else 30)
        d.text((x0 + 36, y0 + 30), label, font=lf, fill=(205, 205, 205, a))
        # the tag pill, top right, with a dot
        tf = _display(30 if self.portrait else 28)
        tb = d.textbbox((0, 0), tag, font=tf)
        tw = tb[2] - tb[0]
        col = br.negative if online else br.primary
        px1 = x1 - 30
        px0 = px1 - tw - 62
        d.rounded_rectangle([px0, y0 + 24, px1, y0 + 74], radius=25,
                            outline=col + (a,), width=3)
        d.ellipse([px0 + 16, y0 + 41, px0 + 32, y0 + 57], fill=col + (a,))
        d.text((px0 + 44 - tb[0], y0 + 49 - (tb[3] - tb[1]) / 2 - tb[1]), tag,
               font=tf, fill=col + (a,))

    def _slip(self, d, box, shown: float, head: str, col, alpha: float,
              verdict: str = "", vp: float = 0.0) -> None:
        """The transaction, as rows of key and value. `shown` 0..1 types the
        rows in; `verdict` replaces the head once `vp` > 0."""
        x0, y0, x1, y1 = box
        a = int(255 * alpha)
        if a <= 0:
            return
        d.rounded_rectangle(box, radius=16, fill=(6, 6, 6, a),
                            outline=col + (a,), width=3)
        hf = _display(30 if self.portrait else 28)
        kf = _font(28 if self.portrait else 26)
        vf = _font(48 if self.portrait else 46)
        htxt, hcol = head, (150, 150, 150)
        if verdict and vp > 0:
            htxt, hcol = verdict, self.brand.positive
        d.text((x0 + 26, y0 + 20), htxt, font=hf, fill=hcol + (a,))
        n = len(self.lines)
        row_h = (y1 - y0 - 78) / n
        chars = sum(len(v) for _, v in self.lines)
        budget = int(round(chars * min(1.0, shown)))
        for i, (k, v) in enumerate(self.lines):
            ry = y0 + 70 + i * row_h
            take = max(0, min(len(v), budget))
            budget -= take
            if take <= 0 and shown < 1:
                continue
            d.text((x0 + 26, ry), k.upper(), font=kf, fill=(130, 130, 130, a))
            d.text((x0 + 26, ry + 32), v[:take], font=vf,
                   fill=self.brand.ink + (a,))

    def _key(self, d, cx: float, cy: float, s: float, col, a: int) -> None:
        """A key in line art: a ring, a shaft, two teeth."""
        r = s * 0.42
        w = max(4, int(s * 0.12))
        d.ellipse([cx - s - r, cy - r, cx - s + r, cy + r],
                  outline=col + (a,), width=w)
        d.line([(cx - s + r, cy), (cx + s, cy)], fill=col + (a,), width=w)
        for tx in (cx + s * 0.45, cx + s * 0.85):
            d.line([(tx, cy), (tx, cy + s * 0.42)], fill=col + (a,), width=w)

    def _chip(self, d, x: float, y: float, text: str, col, a: int) -> None:
        f = _display(30 if self.portrait else 28)
        b = d.textbbox((0, 0), text, font=f)
        w, h = b[2] - b[0], b[3] - b[1]
        d.rounded_rectangle([x - w / 2 - 22, y - h / 2 - 16, x + w / 2 + 22,
                             y + h / 2 + 16], radius=12, fill=col + (a,))
        d.text((x - w / 2 - b[0], y - h / 2 - b[1]), text, font=f,
               fill=(12, 12, 12, a))

    # --- the frame ----------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        s0 = self._since(0, f)
        if s0 < 0:
            return
        br, p = self.brand, self.portrait
        prim, neg = br.primary, br.negative
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        s1, s2, s3 = (self._since(i, f) for i in (1, 2, 3))
        enter = min(1.0, max(0.0, s0 / 0.6))
        L, T, R, TG, KEY, STAYS = self.labels
        A, B = self.A, self.B

        # The cable between the cards, drawn as the cards arrive.
        if p:
            cx = (A[0] + A[2]) / 2
            c0, c1 = (cx, A[3]), (cx, B[1])
        else:
            cy = A[1] + (A[3] - A[1]) * 0.50
            c0, c1 = (A[2], cy), (B[0], cy)
        partial(d, [c0, c1], _smooth((s0 - 0.25) / 0.6), (110, 110, 110), 6)
        for q in (c0, c1):
            if s0 > 0.5:
                d.ellipse([q[0] - 9, q[1] - 9, q[0] + 9, q[1] + 9],
                          fill=(110, 110, 110, 255))

        self._card(d, A, L, T, True, enter)
        self._card(d, B, R, TG, False, enter)

        # The computer's slip: the transaction typing in.
        ax0, ay0, ax1, ay1 = A
        slip_a = [ax0 + 36, ay0 + 104, ax1 - 36, ay1 - 36]
        typed = min(1.0, max(0.0, (s0 - 0.30) / 0.9))
        self._slip(d, slip_a, typed, "TRANSACTION", (90, 90, 90),
                   enter, "SIGNED - SENT TO THE NETWORK",
                   1.0 if s3 > 0 and self.span_p(3, f) >= 0.98 else 0.0)

        # The device: a screen, a button, and the key under them.
        bx0, by0, bx1, by1 = B
        key_h = 120 if p else 128
        scr = [bx0 + 36, by0 + 104, bx1 - 150, by1 - 36 - key_h]
        on = max(0.0, min(1.0, (self.span_p(1, f) - 0.85) / 0.15)) if s1 >= 0 else 0.0
        d.rounded_rectangle(scr, radius=16, fill=(6, 6, 6, int(255 * enter)),
                            outline=prim + (int(255 * enter),), width=3)
        if on > 0:
            self._slip(d, scr, 1.0, "CONFIRM?", prim, on, "APPROVED",
                       1.0 if s2 > 0.25 else 0.0)
        # the button, right of the screen
        bcx = bx1 - 84
        bcy = (scr[1] + scr[3]) / 2
        br_ = 40
        press = ease_out(min(1.0, max(0.0, s2 / 0.3))) if s2 >= 0 else 0.0
        d.ellipse([bcx - br_, bcy - br_, bcx + br_, bcy + br_],
                  outline=prim + (int(255 * enter),), width=4,
                  fill=prim + (int(255 * press),) if press > 0 else None)
        if 0 < s2 < 0.9:
            g = s2 / 0.9
            rr = br_ + 46 * g
            d.ellipse([bcx - rr, bcy - rr, bcx + rr, bcy + rr],
                      outline=prim + (int(220 * (1 - g)),), width=4)
        bf = _font(22)
        bb = d.textbbox((0, 0), "BUTTON", font=bf)
        d.text((bcx - (bb[2] - bb[0]) / 2, bcy + br_ + 14), "BUTTON", font=bf,
               fill=(150, 150, 150, int(255 * enter)))

        # the key row
        ky = by1 - 36 - key_h / 2 + 6
        kx = bx0 + 36 + 54
        stay = _smooth(s3 / 0.6) if s3 >= 0 else 0.0
        kcol = prim
        self._key(d, kx, ky, 34, kcol, int(255 * enter))
        kf = _display(34 if p else 32)
        d.text((kx + 60, ky - 22), KEY, font=kf, fill=prim + (int(255 * enter),))
        if stay > 0:
            kb = d.textbbox((0, 0), KEY, font=kf)
            x_end = kx + 60 + kb[2] - kb[0]
            ring = [kx - 62, ky - 44, x_end + 22, ky + 44]
            pts = _round_corners([(ring[0], ring[1]), (ring[2], ring[1]),
                                  (ring[2], ring[3]), (ring[0], ring[3]),
                                  (ring[0], ring[1])], 22, seg=8)
            partial(d, pts, stay, prim, 4)
            sf = _display(34 if p else 27)
            sa = int(255 * _smooth((s3 - 0.35) / 0.5))
            if sa > 0:
                shadow_text(d, (x_end + 38, ky - (22 if p else 18)), STAYS, sf,
                            (255, 255, 255, sa), alpha=sa)

        # The travelling chips.
        def along(q: float) -> tuple[float, float]:
            return (c0[0] + (c1[0] - c0[0]) * q, c0[1] + (c1[1] - c0[1]) * q)

        if s1 >= 0:
            q = self.span_p(1, f, cap=1.6)
            if 0 < q < 1:
                x, y = along(q)
                self._chip(d, x, y, "TRANSACTION", (235, 235, 235), 255)
        if s3 >= 0:
            q = self.span_p(3, f, cap=1.6)
            if 0 < q < 1:
                x, y = along(1 - q)
                self._chip(d, x, y, "SIGNATURE", prim, 255)

        rise = int(22 * (1 - ease_out(enter)))
        out.paste(layer, (0, rise), layer)
