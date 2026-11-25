"""`lesson` - one statement or one number on a card: the problem, the fix,
what was learned, or a count.

**Why (2026-11-23, the OktAI editor on the second recorded cut):** the
`stat` screens ("5 / that mattered most", "1 / for every video") were "still
not good - try a different layout and some sfx, use the other dark background
with the lines", and a pull quote marked with a green tick for "Keep the
answer for later" should be "a better screen for those sections - like a
lesson, or what we learned - reused where it makes sense; the same screen in
a different version shows the problem, so it fits together".

So one card in three colours, on the ruled ground (`grid_ground`):

* `problem` - a red label, "THE PROBLEM": what made the videos slop.
* `fix` - green, "THE FIX": what replaced it.
* `learned` / `count` - the brand gold: a rule, or a number with its units
  shown as pips lighting as it counts.

The card rises in, its label pops, the words arrive one by one (a number
counts up instead), and the video's 3D emblem breaks out over the card's
top-right corner - the depth that keeps it from reading as a slide. The
sounds are in `longform.build`'s cue list: the card set down, a pip a unit.

payload: (kind, text, note, value, pips, label)
    kind  - "problem" | "fix" | "learned" | "count"
    text  - the statement (for a count: what the number counts, "mistakes")
    note  - a smaller line under it
    value - a number to count up to ("5"), for a count
    pips  - True or an emoji: one chip per unit of `value` (2..30)
    label - the pill's own words instead of the kind's
"""

from __future__ import annotations

import math

from PIL import Image, ImageDraw, ImageFilter

from ...core.draw import ease_out, wrap
from .base import Beat, _display, _font

RED = (235, 64, 52)
GREEN = (74, 200, 120)
LABELS = {"problem": "THE PROBLEM", "fix": "THE FIX", "learned": "WHAT I LEARNED",
          "count": ""}


class Lesson(Beat):
    EMBLEM = False          # the emblem sits on the card, drawn in `content`
    COUNT = 0.85            # seconds a value takes to count up
    WORDS = 1.0             # seconds the words take to arrive

    def __init__(self, kind: str, text: str = "", note: str = "",
                 value: str | None = None, pips=None, label: str | None = None,
                 **kw):
        kw.setdefault("ground", "grid")
        super().__init__(**kw)
        if kind not in LABELS:
            raise ValueError(f"lesson kind {kind!r} - one of {', '.join(LABELS)}")
        self.kind, self.text, self.note = kind, text, note
        self.value, self.pips = value, pips
        self.label = label if label is not None else LABELS[kind]
        self.accent = {"problem": RED, "fix": GREEN}.get(kind, self.brand.primary)

    # --- geometry ------------------------------------------------------------

    def _card(self) -> tuple[int, int, int, int]:
        """The card, as tall as what it holds, centred."""
        W, H = self.frame.size
        w = W - 2 * 70 if self.portrait else int(W * 0.70)
        h = self._content_h(w)
        x = 70 if self.portrait else (W - w) // 2 - int(W * 0.02)
        return x, (H - h) // 2 + int(H * 0.03), w, h

    def _content_h(self, w: int) -> int:
        if not hasattr(self, "_h"):
            d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
            pad = 70
            h = 2 * pad + (int(34 * 1.55) + 40 if self.label else 0)
            text_w = w - 2 * pad - (int(w * 0.20) if not self.portrait else 0)
            if self.kind == "count" and self.value:
                h += 220 + (130 if self.pips else 0)
            else:
                size = 78 if not self.portrait else 84
                lines = wrap(d, self.text, _display(size), text_w)
                h += int(size * 1.18) * len(lines)
                if self.note:
                    nf = _font(42 if not self.portrait else 46)
                    h += int(size * 0.25) + int(nf.size * 1.3) * len(wrap(d, self.note, nf, text_w))
            self._h = h
        return self._h

    def _t0(self) -> float:
        return self.reveals[0] if self.reveals else self.start

    # --- drawing -------------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        t = self.at(f)
        t0 = self._t0()
        e = ease_out(min(1.0, max(0.0, (t - self.start) / 0.45)))
        if e <= 0:
            return
        x, y, w, h = self._card()
        lift = int(36 * (1 - e))
        y += lift
        a = int(255 * e)

        # The card: a dark glass panel with its shadow, a hairline in the
        # kind's colour, and an accent bar down its left edge.
        layer = Image.new("RGBA", out.size, (0, 0, 0, 0))
        sh = Image.new("L", out.size, 0)
        ImageDraw.Draw(sh).rounded_rectangle([x, y + 18, x + w, y + h + 18],
                                             radius=30, fill=int(150 * e))
        sh = sh.filter(ImageFilter.GaussianBlur(28))
        layer.paste((0, 0, 0, 255), (0, 0), sh)
        d = ImageDraw.Draw(layer)
        d.rounded_rectangle([x, y, x + w, y + h], radius=30,
                            fill=(16, 17, 26, int(232 * e)),
                            outline=self.accent + (int(110 * e),), width=2)
        d.rounded_rectangle([x, y + 34, x + 9, y + h - 34], radius=4,
                            fill=self.accent + (a,))
        base = out.convert("RGBA")
        base.alpha_composite(layer)
        out.paste(base.convert("RGB"))
        d = ImageDraw.Draw(out, "RGBA")

        pad = 70
        tx = x + pad
        ty = y + pad

        # The label, popping.
        if self.label:
            p = ease_out(min(1.0, max(0.0, (t - (self.start + 0.15)) / 0.3)))
            if p > 0:
                lf = _font(34 if not self.portrait else 40)
                lw = d.textlength(self.label, font=lf)
                ph = lf.size * 1.55
                s = 0.85 + 0.15 * p
                d.rounded_rectangle([tx, ty, tx + (lw + lf.size * 1.4) * s, ty + ph * s],
                                    radius=int(ph * 0.5 * s),
                                    fill=self.accent + (int(255 * p),))
                ink = (14, 14, 20) if self.kind not in ("problem",) else (255, 255, 255)
                d.text((tx + lf.size * 0.7 * s, ty + ph * s / 2), self.label,
                       font=lf.font_variant(size=int(lf.size * s)), anchor="lm",
                       fill=ink + (int(255 * p),))
            ty += int(34 * 1.55) + 40

        text_w = w - 2 * pad - (int(w * 0.20) if not self.portrait else 0)
        if self.kind == "count" and self.value:
            self._count(out, d, tx, ty, text_w, t, t0)
        else:
            self._statement(d, tx, ty, text_w, t, t0)

        # The emblem, breaking out over the card's top-right corner.
        from ...core import emblem3d
        name = self.emblem_name or emblem3d.CURRENT
        if name and name != "arcs" and emblem3d.available():
            side = int(self.frame.h * (0.36 if not self.portrait else 0.20))
            bx = x + w - side * 0.70
            by = y - side * 0.42
            emblem3d.draw(out, name, self.brand.primary, t,
                          (bx, by, side, side), alpha=e)

    def _statement(self, d, x, y, w, t, t0) -> None:
        size = 78 if not self.portrait else 84
        font = _display(size)
        lines = wrap(d, self.text, font, w)
        while len(lines) > 3 and size > 48:
            size -= 6
            font = _display(size)
            lines = wrap(d, self.text, font, w)
        words = self.text.split()
        n = max(1, len(words))
        start = t0 + 0.25
        k = 0
        for ln in lines:
            cx = x
            for word in ln.split():
                p = min(1.0, max(0.0, (t - (start + self.WORDS * k / n)) / 0.22))
                if p > 0:
                    d.text((cx, y + int(14 * (1 - p))), word, font=font,
                           fill=(245, 245, 250, int(255 * p)))
                cx += d.textlength(word + " ", font=font)
                k += 1
            y += int(size * 1.18)
        if self.note:
            p = min(1.0, max(0.0, (t - (start + self.WORDS + 0.1)) / 0.3))
            nf = _font(42 if not self.portrait else 46)
            y += int(size * 0.25)
            for ln in wrap(d, self.note, nf, w):
                d.text((x, y), ln, font=nf, fill=self.accent + (int(235 * p),))
                y += int(nf.size * 1.3)

    def _count(self, out, d, x, y, w, t, t0) -> None:
        target = float(str(self.value).replace(",", ""))
        p = ease_out(min(1.0, max(0.0, (t - (t0 + 0.25)) / self.COUNT)))
        shown = str(self.value) if p >= 1 else f"{target * p:.0f}"
        big = _display(250 if not self.portrait else 220)
        d.text((x, y - 48), shown, font=big, fill=self.brand.primary + (255,))
        nx = x + max(d.textlength(str(self.value), font=big), 120) + 50
        tf = _display(64 if not self.portrait else 60)
        ty = y + 40
        for ln in wrap(d, self.text, tf, w - (nx - x)):
            d.text((nx, ty), ln, font=tf, fill=(245, 245, 250, 255))
            ty += int(tf.size * 1.15)
        if self.note:
            nf = _font(42)
            for ln in wrap(d, self.note, nf, w - (nx - x)):
                d.text((nx, ty + 8), ln, font=nf, fill=(190, 190, 200, 255))
                ty += int(nf.size * 1.3)
        if self.pips and target.is_integer() and 1 < target <= 30:
            self._pips(out, x, y + 250, int(target), t, t0)

    def _pips(self, out, x, y, n, t, t0) -> None:
        s = 86 if n <= 6 else 62 if n <= 13 else 50
        gap = int(s * 0.3)
        per = 13
        d = ImageDraw.Draw(out, "RGBA")
        icon = self.pips if isinstance(self.pips, str) else None
        for i in range(n):
            r, c = divmod(i, per)
            cx = x + c * (s + gap) + s / 2
            cy = y + r * (s + gap) + s / 2
            lit = (t - (t0 + 0.25)) - self.COUNT * (i + 1) / n
            a = max(0.0, min(1.0, lit / 0.15 + 1.0))
            pop = 1.0 + 0.2 * math.sin(math.pi * a)
            half = s * pop / 2
            d.rounded_rectangle([cx - half, cy - half, cx + half, cy + half],
                                radius=int(s * 0.26),
                                fill=self.accent + (int(30 + 70 * a),),
                                outline=self.accent + (int(80 + 175 * a),), width=3)
            if icon and a > 0:
                from ...core.vertical import emoji_image
                im = emoji_image(icon, int(s * 0.6), getattr(self, "t_now", None))
                if a < 1:
                    im = im.copy()
                    im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
                out.paste(im, (int(cx - im.width / 2), int(cy - im.height / 2)), im)

    def pip_times(self) -> list[float]:
        """When each pip lights - for its sound (`longform.build`)."""
        if not (self.kind == "count" and self.pips and self.value):
            return []
        target = float(str(self.value).replace(",", ""))
        if not target.is_integer() or not 1 < target <= 30:
            return []
        n = int(target)
        return [self._t0() + 0.25 + self.COUNT * (i + 1) / n - 0.05 for i in range(n)]


def extra_cues(sh, lesson: bool = True) -> list:
    """Sounds for the OktAI pieces, shared by the long form and the Shorts
    (2026-11-24, the editor: "add more sfx where it makes sense"): a lesson
    card set down, its label marked, a pip a unit; a soft whoosh as one of
    our videos or an example comes up in its window; a drop per phone."""
    from ...core.brand import OKTAI
    cues = []
    if lesson and sh.graphic == "lesson":
        cues.append((sh.start + 0.12, "drop"))
        kind = sh.payload[0] if sh.payload else ""
        if kind in ("problem", "fix"):
            cues.append((sh.start + 0.2, "cross" if kind == "problem" else "tick"))
        beat = Lesson(*sh.payload, brand=OKTAI, start=sh.start, hold=sh.hold,
                      reveals=sh.reveals)
        cues += [(t, f"pip{min(k, 7)}") for k, t in enumerate(beat.pip_times())]
    if sh.graphic == "phones":
        cues += [(t, "drop") for t in (sh.reveals or [])[:3]]
    win = getattr(sh, "window", None)
    kind = win if isinstance(win, str) else (win[0] if win else None)
    if kind in ("youtube", "player"):
        cues.append((sh.start - 0.05, "pan"))
    return cues
