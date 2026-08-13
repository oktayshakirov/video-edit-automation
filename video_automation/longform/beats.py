"""Drawn beats, in landscape.

The shorts have exactly one drawn beat — `ChecklistShot` — and it carries a
single moment in a ten-shot piece. Long form inverts that: the arithmetic in
`docs/long-form-strategy.md` says a three-minute video needs about thirty shots
against two to five available photographs, so **drawn beats have to carry the
largest single share of the runtime**. That is also the only version of this
format worth making, because a drawn beat shows the argument instead of
illustrating it.

**The split layout is the reason this works at 1920x1080.** Every beat here puts
its content in a column on the left and, optionally, a photograph in a column on
the right. A 900px source — the median on thecrypto.wiki — dropped into a 660px
column is a *downscale*. The upscale problem that dominates the full-frame photo
case (see `core/frame.py`) does not arise at all here, so the more of the piece
these beats carry, the sharper the whole video is. That is a happy alignment and
worth not breaking.

Every beat reuses the two things the shorts' checklist paid for:

* **Two phases.** Content arrives on `reveals`, taken from the caption times of
  the sentence being spoken, so a line appears exactly as it is said. Verdicts,
  where a beat has them, land afterwards on `marks` — in the pause the script
  bought with a longer `gap`. Marking each item as it arrived answered the
  question before it had been asked.
* **Things draw on, they do not appear.** At this size an instant strike reads
  as a rendering glitch; a line that travels reads as something being crossed
  out.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ..core.brand import Brand
from ..core.draw import contain, cover, ease_out, mark, subpixel, wrap
from ..core.frame import LANDSCAPE, Frame
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

DRAW = 0.16                     # how long a mark or a strike takes to draw on
POP = 0.14                      # an item's entrance
RISE = 14                       # px an item travels on its way in


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)


class Beat:
    """Base for every drawn beat: a background, two columns, and timing.

    Subclasses implement `content(d, out, f, t)` and draw into the left column
    using `self.col`. The background, the picture column, the drifting grid and
    the reveal clock are all handled here so a new beat is a layout decision
    rather than a rendering one.
    """

    MARGIN = 100
    COL_W = 1000                # content column width at 1920
    PIC_X = 1160                # picture column left edge
    PIC_W = 660
    PIC_H = 760

    def __init__(self, brand: Brand, frame: Frame = LANDSCAPE,
                 backdrop: Path | None = None, picture: Path | None = None,
                 reveals: list[float] | None = None,
                 marks: list[float] | None = None,
                 start: float = 0.0, hold: float = 1.0):
        self.brand, self.frame = brand, frame
        self.reveals, self.marks = reveals, marks
        self.start, self.hold = start, hold

        # Scale the column geometry if the frame is not the 1920 reference.
        k = frame.w / 1920
        self.margin = int(self.MARGIN * k)
        self.col = (self.margin, int(self.COL_W * k))
        self.pic_box = (int(self.PIC_X * k), int(self.PIC_W * k),
                        int(self.PIC_H * frame.h / 1080))

        self.back = None
        if backdrop is not None and Path(backdrop).exists():
            # Prepared with headroom, so the backdrop can drift. In the shorts
            # this layer was static and a drifting grid supplied the motion;
            # here the grid is gone (see `background`) and the photograph moves
            # instead, which is both better motion and one less thing drawn.
            pad = 120
            im = cover(Image.open(backdrop).convert("RGB"),
                       frame.w + pad, frame.h + pad)
            im = im.filter(ImageFilter.GaussianBlur(30))
            # 0.42, not 0.3. Measured on real frames while building the shorts:
            # 0.3 was indistinguishable from flat black, which is the thing a
            # photographic backdrop exists to avoid. Brighter than the shorts'
            # 0.5 is wrong in the other direction — at 1920 a bright backdrop
            # competes with type that has twice as much of it to hold up.
            self.back = (np.asarray(im) * 0.42).astype(np.uint8)

        # The picture column, prepared once with headroom for a slow drift.
        self.pic = None
        if picture is not None and Path(picture).exists():
            pw, ph = self.pic_box[1], self.pic_box[2]
            src = Image.open(picture).convert("RGB")
            fitted = contain(src, int(pw * 1.10), int(ph * 1.10))
            # If the source was too small to fill the column even at 1:1, take
            # the column down to the picture rather than stretching it up.
            self.pic_w = min(pw, fitted.width)
            self.pic_h = min(ph, fitted.height)
            self.pic = np.asarray(fitted)

    # --- timing ---------------------------------------------------------

    def at(self, f: float) -> float:
        """Absolute time at `f`, which is what `reveals` and `marks` are in."""
        return self.start + f * self.hold

    def due(self, i: int, n: int, f: float) -> float:
        """How far item `i` has entered, 0..1. Falls back to even spacing."""
        t = self.at(f)
        when = (self.reveals[i] if self.reveals and i < len(self.reveals)
                else self.start + self.hold * (i / max(n, 1)) * 0.85)
        return ease_out((t - when) / POP) if t >= when else -1.0

    def marked(self, i: int, f: float) -> float:
        """How far item `i`'s verdict has drawn on, 0..1, or -1 if not due."""
        if not self.marks or i >= len(self.marks):
            return -1.0
        t = self.at(f)
        return ease_out((t - self.marks[i]) / DRAW) if t >= self.marks[i] else -1.0

    # --- painting -------------------------------------------------------

    def background(self, f: float) -> Image.Image:
        """A drifting photograph, or a flat panel with a drifting grid.

        **The grid is only drawn on the flat case, and that is a fix, not a
        simplification.** Its tint is a near-black chosen against the shorts'
        dark panel; over a bright blurred photograph the same lines are plainly
        visible and the beat reads as graph paper. The grid exists to stop a
        flat panel looking like the video has stopped — a photograph does not
        have that problem, so over one the grid is solving nothing and costing
        the look.
        """
        fr = self.frame
        if self.back is not None:
            # Opposed to nothing in particular, just slow — the type is the
            # subject here and a backdrop that pulls the eye is a bug.
            bx = (self.back.shape[1] - fr.w) * (0.5 + 0.34 * (f - 0.5))
            by = (self.back.shape[0] - fr.h) * (0.5 - 0.34 * (f - 0.5))
            return Image.fromarray(subpixel(self.back, bx, by, fr.w, fr.h))

        out = Image.new("RGB", fr.size, self.brand.bg)
        d = ImageDraw.Draw(out)
        step, off = 96, int((f * 40) % 96)
        for gx in range(-96 + off, fr.w + 96, step):
            d.line([(gx, 0), (gx, fr.h)], fill=self.brand.grid, width=2)
        for gy in range(-96 + off, fr.h + 96, step):
            d.line([(0, gy), (fr.w, gy)], fill=self.brand.grid, width=2)
        return out

    def emblem(self, out: Image.Image, f: float) -> None:
        """Concentric arcs in the picture column, slowly counter-rotating.

        Beats with a photograph get one; beats without had a dead right half —
        on a 16:9 frame that is 40% of the picture showing nothing, which the
        user flagged on the outro stat. This is deliberately abstract: it is
        there to balance the composition and give the eye something moving, not
        to mean anything. Low contrast, so it never competes with the number.
        """
        x0, w, h = self.pic_box
        cx, cy = x0 + w // 2, self.frame.h // 2
        d = ImageDraw.Draw(out, "RGBA")
        r0 = min(w, h) // 2
        for i, (rf, span, speed, alpha) in enumerate(
                ((1.00, 250, 1.0, 46), (0.78, 190, -1.4, 62),
                 (0.56, 300, 0.7, 52), (0.34, 140, -2.0, 78))):
            r = int(r0 * rf)
            a0 = (f * 34 * speed + i * 61) % 360
            d.arc([cx - r, cy - r, cx + r, cy + r], a0, a0 + span,
                  fill=self.brand.primary + (alpha,), width=5)
        # A filled dot at the centre, so the rings read as a system rather than
        # as four unrelated curves.
        d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11],
                  fill=self.brand.primary + (150,))

    def paint_picture(self, out: Image.Image, f: float) -> None:
        """The right-hand column: the post's own photograph, drifting slowly."""
        if self.pic is None:
            return
        x0, _, _ = self.pic_box
        w, h = self.pic_w, self.pic_h
        # Drift within the headroom prepared in __init__, subpixel as always.
        sx = max(0.0, (self.pic.shape[1] - w) * (0.35 + 0.30 * f))
        sy = max(0.0, (self.pic.shape[0] - h) * (0.65 - 0.30 * f))
        crop = Image.fromarray(subpixel(self.pic, sx, sy, w, h))

        y0 = (self.frame.h - h) // 2
        out.paste(crop, (x0, y0))
        # The same hairline the photo shots use, and for the same reason: it
        # reads as deliberate framing rather than as an image that failed to
        # fill its space.
        d = ImageDraw.Draw(out)
        d.rectangle([x0, y0, x0 + w, y0 + h], outline=self.brand.primary, width=3)

    def heading(self, out: Image.Image, text: str, f: float = 1.0,
                y: int = 214) -> int:
        """The beat's kicker, in the brand accent. Returns the y below it.

        **y=214, not 176.** The watermark sits upper-left at y=62 and a 34px
        kicker at 176 read as the second line of the logo lockup rather than as
        the beat's own heading — the two stacked into one block. Clearing the
        mark properly costs nothing; the content below is centred anyway.
        """
        if not text:
            return y
        d = ImageDraw.Draw(out)
        d.text((self.col[0], y), text.upper(), font=_font(34),
               fill=self.brand.primary)
        # The rule draws across as the beat opens, so even a beat whose content
        # arrives slowly has something moving in its first half second.
        e = ease_out(min(1.0, (self.at(f) - self.start) / 0.45))
        d.line([(self.col[0], y + 54), (self.col[0] + int(220 * e), y + 54)],
               fill=self.brand.primary, width=3)
        return y + 96

    def content(self, out: Image.Image, f: float) -> None:
        raise NotImplementedError

    # Beats that fill the right column with an abstract emblem when they have
    # no photograph. A checklist or a comparison already spans the frame; a
    # stat or a quote is a short block on the left and nothing on the right.
    EMBLEM = False

    def draw(self, f: float) -> Image.Image:
        out = self.background(f)
        if self.pic is not None:
            self.paint_picture(out, f)
        elif self.EMBLEM:
            self.emblem(out, f)
        self.content(out, f)
        return out


class ChapterCard(Beat):
    """The turn between sections: one line, centred, spoken as it appears.

    **No number, and that is the point.** The first build set a `02` in 150px
    gold above every title, which turned the video into a slide deck — a
    numbered agenda is the visual language of a presentation, and it tells the
    viewer they are being lectured rather than told something. It also exposed
    an off-by-one nobody would otherwise have seen: numbering ran from the
    section index, and since the opening section carries no card, the first one
    on screen read "02".

    **Usually a question, not always.** A question is the strongest form here
    because it makes the next twenty seconds an answer the viewer is waiting
    for. But a section that resolves something wants a statement, and forcing
    "What did that turn it into?" onto a conclusion is worse than just saying
    it. The beat does not care which; write whichever the moment is.

    Centred on both axes, because it is the only beat with nothing else in the
    frame, and left-aligned type in an empty 16:9 frame reads as a slide with a
    missing bullet list.

    payload: (title,)
    """

    SIZE = 108

    def __init__(self, title: str, **kw):
        super().__init__(**kw)
        self.title = title

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        w = self.frame.w - 2 * self.margin
        font = _font(self.SIZE)
        lines = wrap(d, self.title, font, w)

        line_h = int(self.SIZE * 1.26)
        block = len(lines) * line_h
        e = ease_out(min(1.0, (self.at(f) - self.start) / 0.5))
        y = (self.frame.h - block) // 2 + int(round(26 * (1.0 - e)))

        # A short rule above the line, opening outward from the centre as the
        # card settles. It gives the eye something to follow through a beat that
        # is otherwise a static piece of type, and it centres the composition
        # without needing a second line of text to balance it.
        rule_w = int(180 * e)
        rule_y = y - 54
        if rule_w > 2:
            cx = self.frame.w // 2
            d.line([(cx - rule_w, rule_y), (cx + rule_w, rule_y)],
                   fill=self.brand.primary, width=4)

        for ln in lines:
            tw = d.textlength(ln, font=font)
            d.text(((self.frame.w - tw) / 2, y), ln, font=font,
                   fill=self.brand.ink, stroke_width=4, stroke_fill=(0, 0, 0))
            y += line_h


class Checklist(Beat):
    """The shorts' beat, relaid for a wide frame.

    The vertical version sets its items from `x=200` with a fixed row pitch,
    which fills 1080 and leaves roughly 60% of 1920 empty. Here the list owns
    the left column and a photograph owns the right, which is both a better use
    of the frame and the layout that keeps every source image a downscale.

    **Two timing modes, and they are different instruments.**

    `flow=False` is the shorts' original: every item appears unmarked, so for a
    few seconds the list is a genuine open question, and only then do the
    verdicts land one at a time. It has a payoff and it needs a written pause to
    land in.

    `flow=True` marks each item as it is spoken. It exists because the script
    can carry the verdict itself — "Not a court ruling." "Not writing style." —
    and when it does, holding the cross back for four seconds puts the picture
    behind the voice rather than with it. Use flow when the narration says no,
    and the two-phase mode when the narration asks.

    payload: (items, title, flow) where items is [(text, ok), ...]
    """

    FLOW_LAG = 0.30             # a mark lands just after the word that earns it

    def __init__(self, items: list[tuple[str, bool]], title: str = "",
                 flow: bool = False, **kw):
        super().__init__(**kw)
        self.items, self.title, self.flow = items, title, flow

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        x, w = self.col
        top = self.heading(out, self.title, f)

        font = _font(52)
        n = len(self.items)
        pitch = 118
        # Centre the block in what is left below the heading.
        top = max(top, (self.frame.h - n * pitch) // 2)
        gutter = 84

        for i, (text, ok) in enumerate(self.items):
            e = self.due(i, n, f)
            if e < 0:
                continue
            y = top + i * pitch
            y_in = y + int(round(RISE * (1.0 - e)))

            # White ink for every item, struck or not. Grey-on-dark was shipped
            # once and was not readable on a phone — the strike already says
            # "this does not count".
            d.text((x + gutter, y_in), text, font=font, fill=self.brand.ink,
                   stroke_width=3, stroke_fill=(0, 0, 0))

            m = self.marked(i, f)
            if m < 0:
                continue
            colour = self.brand.primary if ok else self.brand.negative
            mark(d, x, y + 14, 44, ok, colour, progress=m)
            if not ok:
                bbox = d.textbbox((x + gutter, y), text, font=font)
                mid = (bbox[1] + bbox[3]) // 2
                # Drawn from the left and arriving a touch after the cross, so
                # the eye reads mark-then-strike rather than both at once.
                s = ease_out(min(1.0, (self.at(f) - self.marks[i] - 0.05) / DRAW))
                if s > 0:
                    d.line([(x + gutter, mid),
                            (x + gutter + (bbox[2] - x - gutter) * s, mid)],
                           fill=self.brand.negative, width=5)


class Stat(Beat):
    """One number, held. The cheapest beat to build and the best value per second.

    A figure spoken and not shown is a figure not remembered, and a figure set
    at 200px is the only thing on screen that can compete with a photograph for
    attention. Use it for the number the script actually wants to land, not for
    every number in the paragraph.

    payload: (value, label, note)
    """

    COUNT = 0.75                # how long a numeric value takes to count up
    EMBLEM = True

    def __init__(self, value: str, label: str = "", note: str = "", **kw):
        super().__init__(**kw)
        self.value, self.label, self.note = value, label, note
        # A value that is *mostly* digits counts up; one that is a word does
        # not. Splitting on that rather than on a flag means a script never has
        # to think about it — "1.1M" animates, "YES / NO" holds.
        m = re.match(r"^(\D*?)([\d,.]+)(\D*)$", value.strip())
        self.count = None
        # **A year never counts up.** "2009" racing from zero spends most of the
        # beat displaying 1200, 1780, 2001 — all plausible years, all wrong, and
        # a viewer reads the wrong one as an error rather than as an animation.
        # Counting is for magnitudes, where the intermediate values are
        # obviously partial.
        bare = value.strip()
        is_year = bare.isdigit() and len(bare) == 4 and 1900 <= int(bare) <= 2100
        if m and not is_year and any(c.isdigit() for c in m.group(2)):
            body = m.group(2).replace(",", "")
            try:
                self.count = (m.group(1), float(body), m.group(3),
                              len(body.split(".")[1]) if "." in body else 0,
                              "," in m.group(2))
            except ValueError:
                self.count = None

    def _value(self, f: float) -> str:
        """The value at `f` — counted up if numeric, held if not.

        A number that lands whole is a caption. A number that races to its
        value is the one thing on a static beat the eye cannot leave, and it
        costs three quarters of a second of a shot that was going to be held
        anyway.
        """
        if self.count is None or not self.reveals:
            return self.value
        pre, target, post, dp, group = self.count
        p = ease_out((self.at(f) - self.reveals[0]) / self.COUNT)
        if p >= 1.0:
            return self.value
        n = target * max(0.0, p)
        s = f"{n:,.{dp}f}" if group else f"{n:.{dp}f}"
        return f"{pre}{s}{post}"

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        x, w = self.col
        top = self.heading(out, self.label, f)

        e = self.due(0, 1, f)
        if e < 0:
            return
        y = max(top + 40, int(self.frame.h * 0.36))
        # Settles from 92% with a slight overshoot — the same trick the caption
        # sprites use. A linear scale-in reads as a zoom; one that passes its
        # mark and comes back reads as being placed.
        scale = 0.92 + 0.08 * e + 0.03 * math.sin(math.pi * e)
        big = _font(max(12, int(200 * scale)))
        d.text((x, y + int(round(RISE * 2 * (1.0 - e)))), self._value(f),
               font=big, fill=self.brand.primary,
               stroke_width=4, stroke_fill=(0, 0, 0))

        if self.note:
            note_font = _font(46)
            ny = y + int(200 * 1.25)
            for ln in wrap(d, self.note, note_font, w):
                d.text((x, ny), ln, font=note_font, fill=self.brand.ink,
                       stroke_width=3, stroke_fill=(0, 0, 0))
                ny += int(46 * 1.34)


class Compare(Beat):
    """Two columns, side by side. The beat the frame was made for.

    16:9 is a bad shape for a list and a very good one for a comparison — which
    is convenient, because comparison is what both sites' best-performing pages
    are: brown noise against white, spot ETFs against futures, one exchange
    against another. This is the beat to reach for first when the article has an
    "A vs B" in its title.

    payload: (left_title, left_items, right_title, right_items)
    """

    def __init__(self, left_title: str, left_items: list[str],
                 right_title: str, right_items: list[str], **kw):
        super().__init__(**kw)
        self.lt, self.li = left_title, left_items
        self.rt, self.ri = right_title, right_items

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        fr = self.frame
        mid = fr.w // 2
        col_w = mid - self.margin - 40
        title_font, item_font = _font(60), _font(44)

        # Measure both columns first so the pair can be centred as one block.
        # Laying them out from a fixed top left two thirds of the frame empty.
        item_h, pad = int(44 * 1.30), 26
        wrapped = [[wrap(d, f"— {t}", item_font, col_w) for t in items]
                   for items in (self.li, self.ri)]
        tallest = max(sum(len(ls) * item_h + pad for ls in col)
                      for col in wrapped)
        block = 110 + tallest
        top = max(180, (fr.h - block) // 2)

        # A dividing rule that draws down as the beat opens, so the split is
        # established before either side has anything in it. Spanning the block
        # rather than the frame — a rule running into empty space below the last
        # item is the thing that made the first build look unfinished.
        e = ease_out(min(1.0, (self.at(f) - self.start) / 0.5))
        d.line([(mid, top), (mid, top + int(block * e))],
               fill=self.brand.primary, width=3)

        n = max(len(self.li), len(self.ri))
        for side, (title, items) in enumerate(((self.lt, self.li),
                                               (self.rt, self.ri))):
            x = self.margin if side == 0 else mid + 40
            d.text((x, top), title.upper(), font=title_font,
                   fill=self.brand.primary, stroke_width=3,
                   stroke_fill=(0, 0, 0))
            y = top + 120
            for i, text in enumerate(items):
                # Interleave the reveal order — left, right, left, right — so
                # the two sides build against each other rather than one
                # finishing before the other starts.
                k = i * 2 + side
                ev = self.due(k, n * 2, f)
                lines = wrapped[side][i]
                if ev < 0:
                    y += len(lines) * item_h + pad
                    continue
                y_in = y + int(round(RISE * (1.0 - ev)))
                for ln in lines:
                    d.text((x, y_in), ln, font=item_font, fill=self.brand.ink,
                           stroke_width=3, stroke_fill=(0, 0, 0))
                    y_in += item_h
                y += len(lines) * item_h + pad


class Quote(Beat):
    """A pull quote with its attribution.

    Built for the tinnitus posts, whose frontmatter carries a `sources` block
    with a title, a publisher and a URL. Putting the publisher on screen is the
    cheapest credibility signal available in a YMYL niche, and it costs nothing
    because the data is already written.

    payload: (text, attribution)
    """

    EMBLEM = True

    def __init__(self, text: str, attribution: str = "", **kw):
        super().__init__(**kw)
        self.text, self.attribution = text, attribution

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        x, w = self.col
        if self.pic is None:
            w = self.frame.w - 2 * self.margin

        e = self.due(0, 1, f)
        if e < 0:
            return
        font = _font(62)
        lines = wrap(d, f"“{self.text}”", font, w)
        block = len(lines) * int(62 * 1.34)
        y = (self.frame.h - block) // 2 + int(round(RISE * (1.0 - e)))

        # A heavy rule down the left, the typographic mark for a quotation, and
        # it draws down rather than appearing.
        d.line([(x - 34, y), (x - 34, y + int(block * min(1.0, e * 1.2)))],
               fill=self.brand.primary, width=6)
        for ln in lines:
            d.text((x, y), ln, font=font, fill=self.brand.ink,
                   stroke_width=3, stroke_fill=(0, 0, 0))
            y += int(62 * 1.34)

        if self.attribution:
            d.text((x, y + 20), f"— {self.attribution}", font=_font(38),
                   fill=self.brand.primary)


class Bars(Beat):
    """A horizontal bar chart that grows on the voice.

    The beat that was missing. `stat` shows one number and `compare` shows two
    lists, but neither can show a *proportion* — and a proportion is the one
    thing a spoken number cannot convey. "One point one million coins" means
    nothing to a viewer who does not know the supply; the same figure drawn
    against 21 million is instantly legible and needs no second sentence.

    Bars grow from the left with an ease-out, so the eye follows the end of the
    bar rather than watching a rectangle appear. The value sits at the end of
    its own bar and travels with it.

    payload: (rows, title) where rows is [(label, fraction, value_text), ...]
    """

    GROW = 0.85                 # how long a bar takes to reach its length
    EMBLEM = False

    def __init__(self, rows: list[tuple[str, float, str]], title: str = "",
                 **kw):
        super().__init__(**kw)
        self.rows, self.title = rows, title

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        x, _ = self.col
        top = self.heading(out, self.title, f)

        # Full width — a bar chart squeezed into the left column wastes the one
        # dimension it actually needs.
        w = self.frame.w - 2 * self.margin
        label_font, value_font = _font(42), _font(46)
        n = len(self.rows)
        pitch = 132
        top = max(top + 20, (self.frame.h - n * pitch) // 2)

        for i, (label, frac, value) in enumerate(self.rows):
            e = self.due(i, n, f)
            if e < 0:
                continue
            y = top + i * pitch
            g = ease_out(min(1.0, (self.at(f) - self.reveals[i]) / self.GROW)
                         if self.reveals and i < len(self.reveals) else 1.0)

            d.text((x, y), label, font=label_font, fill=self.brand.ink,
                   stroke_width=3, stroke_fill=(0, 0, 0))

            by = y + 58
            bh = 30
            # The track, so an unfilled bar still reads as "out of something".
            d.rectangle([x, by, x + w, by + bh], fill=(255, 255, 255, 26))
            bw = int(w * max(0.0, min(1.0, frac)) * g)
            if bw > 1:
                d.rectangle([x, by, x + bw, by + bh],
                            fill=self.brand.primary + (235,))
            if value:
                vx = min(x + bw + 22, x + w - 10)
                d.text((vx, by - 8), value, font=value_font,
                       fill=self.brand.primary, stroke_width=3,
                       stroke_fill=(0, 0, 0))


BEATS = {
    "chapter": ChapterCard,
    "checklist": Checklist,
    "stat": Stat,
    "compare": Compare,
    "quote": Quote,
    "bars": Bars,
}

# How many things a beat reveals, which is what its `reveals` list has to be as
# long as. A chapter card reveals nothing on a clock — it settles as one block.
_COUNT = {
    "chapter": lambda p: 0,
    "checklist": lambda p: len(p[0]),
    "stat": lambda p: 1,
    "compare": lambda p: max(len(p[1]), len(p[3])) * 2,
    "quote": lambda p: 1,
    "bars": lambda p: len(p[0]),
}


def item_count(graphic: str, payload: tuple) -> int:
    """Reveal count for a beat, so `build` can size its `reveals` list."""
    try:
        return _COUNT[graphic](payload)
    except KeyError:
        raise ValueError(f"unknown beat {graphic!r} — "
                         f"known: {', '.join(sorted(BEATS))}") from None


def make_beat(shot, brand: Brand, frame: Frame):
    """Build the prepared object for a `Shot` that is not a still photograph.

    This is the factory `render_shots` takes, which is what lets the long-form
    vocabulary — the drawn beats and video clips — extend the shorts' engine
    without the shorts knowing either exists.
    """
    if shot.clip is not None:
        from .clip import VideoShot
        return VideoShot(shot.clip, shot.hold, frame=frame, brand=brand,
                         zoom=shot.zoom if shot.zoom > 1.0 else 1.06,
                         label=shot.payload or None)
    if shot.graphic is None:
        return None
    try:
        cls = BEATS[shot.graphic]
    except KeyError:
        raise ValueError(f"unknown beat {shot.graphic!r} — "
                         f"known: {', '.join(sorted(BEATS))}") from None
    return cls(*shot.payload, brand=brand, frame=frame,
               backdrop=shot.backdrop, picture=getattr(shot, "picture", None),
               reveals=shot.reveals, marks=shot.marks,
               start=shot.start, hold=shot.hold)
