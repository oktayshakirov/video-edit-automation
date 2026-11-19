"""`tiers` - a tier board: graded rows, and each item dropping into its row.

**Built for `tinnitus-treatments-ranked` (2026-11-19), the channel's first
E26 ranking.** The 2026 tinnitus guideline grades every treatment it covers
- recommended, an option, advised against - and a ranking's whole claim is
*which row a thing sits in*. `grid` sets a flat set, `checklist` gives each
item a verdict but no tier, `compare` has two columns, not four graded rows.
None of them shows a board filling up, which is what a ranking is.

The board comes back across a video and keeps what it already holds: the
first appearance fills the bottom row, the next one opens with that row
already set (`shown`) and fills the next, and so on up. The rows the voice
is on stay lit; the rest step back while new items land.

Reusable for any graded ranking on either channel: treatments by the
evidence, supplements by the evidence, wallets by custody, exchanges by
proof of reserves. **The rows grade the evidence or the rule, never the
relief** on the health channel (`projects/tinnitus.md`, E26).

payload: (rows, items, title, shown=0, until=None)
  rows    [(label, sub), ...] top to bottom; a third element is an (r, g, b)
          colour, a fourth a line shown in the row while it has no items
          ("No treatment got this grade")
  items   [(row, label, emoji), ...] in the order they are named; `emoji`
          may be "". Every item a script will ever place goes in, so the
          layout never moves between appearances.
  title   the beat's kicker
  shown   how many of `items` are already on the board when the beat opens
  until   how many are on it when the beat ends (default: all of them) -
          the items after it are laid out but not placed yet

Reveals: one caption chunk per item after `shown`. With nothing new to
place (`shown == len(items)`), one reveal, which lights the whole board.
With no items at all, one reveal per row: the grades themselves, each row
sliding in as it is named - the board explained before anything is on it.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ...core.draw import ease_out
from .base import Beat, _display, _font, _smooth

DROP = 0.42              # an item's fall into its row
GLOW = 0.9               # the ring round a card that just landed
INK = (22, 14, 30)       # type on a lit tier block


def _back(p: float) -> float:
    """Ease out with a small overshoot, so a card settles into its row."""
    p = min(1.0, max(0.0, p))
    c = 1.4
    return 1 + (c + 1) * (p - 1) ** 3 + c * (p - 1) ** 2


class Tiers(Beat):

    EMBLEM = False

    def __init__(self, rows: list, items: list, title: str = "",
                 shown: int = 0, until: int | None = None, **kw):
        super().__init__(**kw)
        if not rows:
            raise ValueError("tiers wants at least one row")
        self.rows = [tuple(r) + (None, None)[: max(0, 4 - len(r))]
                     for r in rows]
        self.items = [tuple(i) + ("",) * max(0, 3 - len(i)) for i in items]
        for i, it in enumerate(self.items):
            if not 0 <= it[0] < len(self.rows):
                raise ValueError(f"tiers item {it[1]!r} names row {it[0]}, "
                                 f"there are {len(self.rows)}")
        self.title = title
        self.shown = max(0, min(int(shown), len(self.items)))
        self.until = (len(self.items) if until is None
                      else max(self.shown, min(int(until), len(self.items))))
        self.new = list(range(self.shown, self.until))
        self.active = {self.items[i][0] for i in self.new}
        self._layout()

    # -- geometry ---------------------------------------------------------------

    def _per_row(self) -> list[list[int]]:
        out = [[] for _ in self.rows]
        for i, it in enumerate(self.items):
            out[it[0]].append(i)
        return out

    def _layout(self) -> None:
        fr, p = self.frame, self.portrait
        self.by_row = self._per_row()
        width = fr.w - 2 * self.margin
        self.label_f = _display(40 if p else 36)
        self.sub_f = _font(26 if p else 25)
        self.card_f = _font(32 if p else 29)
        self.empty_f = _font(30 if p else 30)
        if p:
            # A band per row, the cards under it two to a line.
            self.band_h = 76
            self.card_w = (width - 18) // 2
            self.card_h = 104
            gap = 18
            y = self.head_y + 104
            self.row_box, self.card_xy = [], {}
            for r, idx in enumerate(self.by_row):
                lines = max(1, (len(idx) + 1) // 2)
                h = self.band_h + 12 + (lines * (self.card_h + 12)
                                        if idx else 64)
                self.row_box.append((self.margin, y, width, h))
                for k, i in enumerate(idx):
                    cx = self.margin + (k % 2) * (self.card_w + 18)
                    cy = y + self.band_h + 12 + (k // 2) * (self.card_h + 12)
                    self.card_xy[i] = (cx, cy)
                y += h + gap
        else:
            self.block_w = 420
            n = len(self.rows)
            top = self.head_y + 110
            room = fr.h - 60 - top
            pitch = min(190, room // n)
            self.row_h = pitch - 16
            most = max([len(i) for i in self.by_row] + [1])
            track = width - self.block_w - 20
            self.card_w = min(330, (track - 16 * (most - 1)) // max(most, 3))
            self.card_h = min(132, self.row_h - 22)
            self.row_box, self.card_xy = [], {}
            for r, idx in enumerate(self.by_row):
                y = top + r * pitch
                self.row_box.append((self.margin, y, width, self.row_h))
                for k, i in enumerate(idx):
                    cx = self.margin + self.block_w + 20 + k * (self.card_w + 16)
                    cy = y + (self.row_h - self.card_h) // 2
                    self.card_xy[i] = (cx, cy)
        # Fail on type that cannot fit, rather than drawing it over an edge.
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        self.text_lim = self.card_w - 36 - (66 if p else 68)
        for it in self.items:
            self._wrap(it[1])
        blim = (self.row_box[0][2] - 40) if p else self.block_w - 36
        for r in self.rows:
            if probe.textlength(r[0].upper(), font=self.label_f) > blim:
                raise ValueError(f"tiers row {r[0]!r} is wider than its "
                                 f"block ({blim}px)")

    def _wrap(self, text: str) -> list[str]:
        """Greedy word wrap by measured width, at most two lines."""
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        lines, cur = [], ""
        for word in text.split():
            trial = f"{cur} {word}".strip()
            if probe.textlength(trial, font=self.card_f) <= self.text_lim:
                cur = trial
                continue
            if not cur:
                raise ValueError(f"tiers card word {word!r} is wider than "
                                 f"{self.text_lim}px")
            lines.append(cur)
            cur = word
            if probe.textlength(cur, font=self.card_f) > self.text_lim:
                raise ValueError(f"tiers card word {word!r} is wider than "
                                 f"{self.text_lim}px")
        if cur:
            lines.append(cur)
        if len(lines) > 2:
            raise ValueError(f"tiers card {text!r} runs past two lines "
                             f"at {self.text_lim}px")
        return lines

    def _colour(self, r: int) -> tuple:
        c = self.rows[r][2]
        if c:
            return tuple(c)
        n = len(self.rows)
        # Top to bottom: the best grade, the good, the middle, the against.
        ramp = [(255, 204, 102), self.brand.positive, self.brand.primary,
                self.brand.negative]
        if n <= 3:
            ramp = ramp[1:]
        return ramp[min(r, len(ramp) - 1)] if r < n - 1 else ramp[-1]

    # -- clock ------------------------------------------------------------------

    def _since(self, i: int, f: float) -> float:
        """Seconds since item `i` (absolute index) was named; already-shown
        items count as long since."""
        if i < self.shown:
            return 99.0
        k = i - self.shown
        rv = self.reveals or []
        n = max(1, len(self.new))
        when = (rv[k] if k < len(rv)
                else self.start + self.hold * (k / n) * 0.85)
        return self.at(f) - when

    # -- drawing ----------------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        p = self.portrait
        opened = self.open_p(f, 0.7)
        # Once a new item is falling, the rows the voice is not on step back.
        first = min((self._since(i, f) for i in self.new), default=-1)
        focus = _smooth(first / 0.4) if self.new and first > 0 else 0.0
        whole = (self.items and not self.new and self.reveals
                 and self.at(f) >= self.reveals[0])

        for r, (x, y, w, h) in enumerate(self.row_box):
            col = self._colour(r)
            dim = 1.0 if (r in self.active or not self.new) else 1 - 0.5 * focus
            a = opened * dim
            if self.items:
                # The row slides in from the left, top row first.
                s = _smooth((opened * 1.6) - r * 0.12)
            else:
                # The grades alone: each row arrives as the voice names it.
                rv = self.reveals or []
                when = (rv[r] if r < len(rv)
                        else self.start + self.hold * (r / len(self.rows)) * 0.85)
                s = _smooth((self.at(f) - when) / 0.45)
                a = 1.0
            dx = -40 * (1 - s)
            if s <= 0:
                continue
            d.rounded_rectangle([x + dx, y, x + dx + w, y + h], radius=18,
                                fill=col + (int(26 * a * s),),
                                outline=col + (int(90 * a * s),), width=2)
            if p:
                bx0, by0, bx1, by1 = x + dx, y, x + dx + w, y + self.band_h
            else:
                bx0, by0, bx1, by1 = x + dx, y, x + dx + self.block_w, y + h
            d.rounded_rectangle([bx0, by0, bx1, by1], radius=18,
                                fill=col + (int(240 * a * s),))
            label, sub = self.rows[r][0].upper(), self.rows[r][1] or ""
            ink = INK + (int(255 * a * s),)
            if p:
                # Label and subline share one baseline, so the small words
                # read as the label's tail rather than a line dropped under it.
                base = (by0 + by1) / 2 + self.label_f.size * 0.36
                d.text((bx0 + 24, base), label, font=self.label_f, fill=ink,
                       anchor="ls")
                if sub:
                    lw = d.textlength(label, font=self.label_f)
                    d.text((bx0 + 24 + lw + 18, base), sub,
                           font=self.sub_f, fill=INK + (int(200 * a * s),),
                           anchor="ls")
            else:
                cy = (by0 + by1) / 2
                d.text((bx0 + 26, cy - (16 if sub else 0)), label,
                       font=self.label_f, fill=ink, anchor="lm")
                if sub:
                    d.text((bx0 + 26, cy + 30), sub, font=self.sub_f,
                           fill=INK + (int(200 * a * s),), anchor="lm")
            # A row that holds nothing says so.
            empty = self.rows[r][3]
            if empty and not [i for i in self.by_row[r] if i < self.until]:
                ex = (x + dx + 26) if p else (bx1 + 30)
                ey = (y + self.band_h + 12 + 30) if p else (y + h / 2)
                d.text((ex, ey), empty, font=self.empty_f,
                       fill=(225, 225, 230, int(170 * a * s)), anchor="lm")

        for i in range(self.until):
            since = self._since(i, f)
            if since < 0:
                continue
            row, label, emoji = self.items[i]
            dim = (1.0 if (row in self.active or not self.new)
                   else 1 - 0.5 * focus)
            if i < self.shown:
                q, a = 1.0, opened * dim
            else:
                q = _back(since / DROP)
                a = min(1.0, since / (DROP * 0.5)) * dim
            if a <= 0:
                continue
            self._card(layer, d, i, label, emoji, q, a, since, row)

        if whole:
            # Nothing new: the board itself is the point - every row glows.
            t = self.at(f) - self.reveals[0]
            g = _smooth(t / 0.5) * (1 - _smooth((t - 1.2) / 0.8))
            for r, (x, y, w, h) in enumerate(self.row_box):
                d.rounded_rectangle([x - 4, y - 4, x + w + 4, y + h + 4],
                                    radius=22, outline=self._colour(r)
                                    + (int(180 * g),), width=4)
        out.paste(layer, (0, 0), layer)

    def _card(self, layer: Image.Image, d: ImageDraw.ImageDraw, i: int,
              label: str, emoji: str, q: float, a: float, since: float,
              row: int) -> None:
        p = self.portrait
        x, y = self.card_xy[i]
        y = y - 70 * (1 - q)
        w, h = self.card_w, self.card_h
        col = self._colour(row)
        d.rounded_rectangle([x, y, x + w, y + h], radius=16,
                            fill=(24, 16, 32, int(232 * a)),
                            outline=col + (int(150 * a),), width=2)
        # A ring that fades after landing, so the eye finds the new card.
        if 0 <= since < GLOW and i >= self.shown:
            g = 1 - since / GLOW
            d.rounded_rectangle([x - 6, y - 6, x + w + 6, y + h + 6],
                                radius=20, outline=col + (int(220 * g * a),),
                                width=4)
        ix = x + 18
        if emoji:
            from ...core.vertical import emoji_image
            box = 56 if p else 58
            im = emoji_image(emoji, box,
                             t=getattr(self, "t_now", None)).copy()
            # Some glyphs are wider than tall (an open book): fit the box.
            if im.width > box:
                im = im.resize((box, max(1, int(im.height * box / im.width))),
                               Image.LANCZOS)
            if a < 1:
                im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
            layer.alpha_composite(im, (int(ix + (box - im.width) / 2),
                                       int(y + (h - im.height) / 2)))
            ix += (66 if p else 68)
        lines = self._wrap(label)
        lh = self.card_f.size + 6
        ty = y + h / 2 - lh * len(lines) / 2 + 2
        for k, line in enumerate(lines):
            d.text((ix, ty + k * lh), line, font=self.card_f,
                   fill=(245, 245, 245, int(255 * a)))


def drop_times(reveals: list) -> list:
    """When each new card lands, for the build's sound cues."""
    return [t + DROP * 0.8 for t in (reveals or [])]
