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
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ..core import backdrop
from ..core.brand import Brand
from ..core.draw import contain, cover, ease_out, mark, subpixel, wrap
from ..core.frame import LANDSCAPE, Frame
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

DRAW = 0.16                     # how long a mark or a strike takes to draw on
POP = 0.14                      # an item's entrance
RISE = 14                       # px an item travels on its way in


def _font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)


# The thumbnail's display face, so a chapter card and the thumbnail of the same
# video are set in one voice. Imported by path rather than from `thumb` to keep
# the beats module free of a dependency on the thumbnail renderer.
FONT_DISPLAY = "/System/Library/Fonts/Supplemental/Arial Black.ttf"


def _display(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_DISPLAY, size)


@lru_cache(maxsize=8)
def _mark_bottom(name: str, width: int, top: int) -> int:
    """Where the watermark ends, so a kicker can clear it.

    **This cannot be a constant.** thecrypto.wiki's mark is a wide, short
    wordmark; tinnitushelp.me's is a mascot with the domain under it and is
    four times taller at the same width. A kicker at a fixed y=214 cleared
    the first and landed inside the second — the wordmark and the beat's
    heading printed over each other.
    """
    from ..core.brand import BRANDS
    mark = BRANDS[name].mark(width)
    return top + (mark.height if mark is not None else 0)


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
        self.head_y = _mark_bottom(brand.name,
                                   int(frame.logo_w * brand.mark_scale),
                                   frame.logo_at[1]) + 46

        # Scale the column geometry if the frame is not the 1920 reference.
        k = frame.w / 1920
        # **Portrait is not landscape scaled down.** `MARGIN * k` is 56px on a
        # 1080-wide frame, which is tighter than anything else in the vertical
        # format — `ChecklistShot` sets its items from x=200. A margin is about
        # the edge of a phone screen, not about a fraction of the design width.
        self.portrait = frame.h > frame.w
        self.margin = 96 if self.portrait else int(self.MARGIN * k)
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
        """A drifting photograph, or the brand's own moving background.

        **The drifting grid this used to draw is gone.** It stepped a whole
        pixel at a time (`int((f * 40) % 96)` on a layer moving 40 px/s), which
        is the judder every other moving element in this repo was fixed for
        years ago, and it was worst on exactly the long beats where the eye has
        time to lock onto a ruled line. It was also the same graph paper behind
        every beat of every video on both channels.

        `core.backdrop` replaces it with a looping asset per brand — a
        generated purple mesh gradient for tinnitushelp.me, black water for
        thecrypto.wiki. See that module for why they are square and why they
        are sampled by timeline seconds rather than by `f`.

        The flat `brand.bg` panel remains the fallback, so a brand with no
        background declared still renders.
        """
        fr = self.frame
        if self.back is not None:
            # Opposed to nothing in particular, just slow — the type is the
            # subject here and a backdrop that pulls the eye is a bug.
            bx = (self.back.shape[1] - fr.w) * (0.5 + 0.34 * (f - 0.5))
            by = (self.back.shape[0] - fr.h) * (0.5 - 0.34 * (f - 0.5))
            return Image.fromarray(subpixel(self.back, bx, by, fr.w, fr.h))

        bg = backdrop.get(self.brand.backdrop)
        if bg is not None:
            # **Timeline seconds, not `f`.** Sampling by beat progress would
            # run the whole loop inside every beat, so the background would
            # change speed at every cut.
            return Image.fromarray(bg.at(self.at(f), fr.w, fr.h))

        return Image.new("RGB", fr.size, self.brand.bg)

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
                y: int | None = None) -> int:
        """The beat's kicker, in the brand accent. Returns the y below it.

        **y=214, not 176.** The watermark sits upper-left at y=62 and a 34px
        kicker at 176 read as the second line of the logo lockup rather than as
        the beat's own heading — the two stacked into one block. Clearing the
        mark properly costs nothing; the content below is centred anyway.
        """
        y = self.head_y if y is None else y
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

    # **Arial Black, the thumbnail's face, not the caption face.** The user's
    # call: a chapter card is the one moment the video is showing a headline
    # rather than speaking a sentence, and it should look like the headline on
    # the thumbnail. Futura Medium is a light wide geometric that goes weak at
    # display size, which is the identical reason it lost the thumbnail.
    #
    # It does **not** take the thumbnail's accent plate. A coloured box exists
    # to win a fight for attention in a grid of competing thumbnails; there is
    # nothing else in this frame to compete with, so the box would be shouting
    # in an empty room.
    #
    # **The sizes came down when the face changed.** Arial Black is far wider
    # per character than Futura Medium, so the old 108/148 wrapped titles that
    # used to set on one line. These are the sizes at which the same titles
    # occupy the same block.
    SIZE = 88
    SIZE_PORTRAIT = 118

    def __init__(self, title: str, **kw):
        super().__init__(**kw)
        self.title = title

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        w = self.frame.w - 2 * self.margin
        size = self.SIZE_PORTRAIT if self.portrait else self.SIZE
        font = _display(size)
        lines = wrap(d, self.title, font, w)

        line_h = int(size * 1.26)
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
                 right_title: str, right_items: list[str],
                 name_columns: bool = False, **kw):
        super().__init__(**kw)
        self.lt, self.li = left_title, left_items
        self.rt, self.ri = right_title, right_items
        # **`name_columns` makes each heading a revealed item of its own**, so
        # the narration can say "Centralized." and have the word appear, then
        # read that column, then say "Decentralized." and have the other
        # appear. Both headings used to be painted at f=0, which left the
        # viewer to work out which list the voice was on — the user's note was
        # that a comparison must not ask them to interpret, and they are right:
        # a two-column graphic where both labels are already up is a table you
        # are expected to read, not a thing being explained to you.
        #
        # Opt-in, because it changes the reveal count and the shipped
        # mining-rig cut is written against the old one.
        self.name_columns = name_columns

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

        # Reveal indices. With named columns the order is: left heading, the
        # left items, right heading, the right items — which is exactly the
        # order a script reads them in.
        nl, nr = len(self.li), len(self.ri)
        total = nl + nr + (2 if self.name_columns else 0)
        for side, (title, items) in enumerate(((self.lt, self.li),
                                               (self.rt, self.ri))):
            x = self.margin if side == 0 else mid + 40
            if self.name_columns:
                head_k = 0 if side == 0 else nl + 1
                eh = self.due(head_k, total, f)
            else:
                eh = 1.0
            if eh >= 0:
                d.text((x, top + int(round(RISE * (1.0 - min(1.0, eh))))),
                       title.upper(), font=title_font,
                       fill=self.brand.primary, stroke_width=3,
                       stroke_fill=(0, 0, 0))
            y = top + 120
            for i, text in enumerate(items):
                # **Sequential, not interleaved: the whole left column, then
                # the whole right one.** The first version alternated sides so
                # they would "build against each other", which cannot ever match
                # the voice — a script covers one column and then the other,
                # because you cannot narrate two things at once. Interleaving
                # meant a chronic item appeared while the narration was still on
                # temporary, and a viewer reads that as the graphic being out of
                # sync with the words. It is the reason this beat looked
                # confusing rather than any layout problem.
                if self.name_columns:
                    k = 1 + i if side == 0 else nl + 2 + i
                else:
                    k = i if side == 0 else nl + i
                ev = self.due(k, total, f)
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


class Grid(Beat):
    """Items as cards across the whole frame, two or three to a row.

    **This exists because every list looked the same.** `checklist` and
    `compare` both set type in a left column with a ragged right edge, so a
    four-item checklist and a three-a-side comparison read as the same graphic
    at a glance — and across a channel that is the templated sameness the
    strategy doc says gets suppressed. The fix is not a new typeface, it is a
    different *silhouette*: cards on a grid spanning the full width have no
    left column and no ragged edge, and the eye reads them as objects rather
    than as lines of a list.

    So this is the beat for a **set of things** — components, options, formats —
    where a checklist's implied verdict column would be meaningless anyway.
    Nothing here is ticked or struck; if items need verdicts, use `checklist`.

    Each card takes an optional second line, which is where the wide layout
    pays for itself: a checklist has room for a label and nothing else, and
    "8 GB of memory" is a great deal more useful with "enough for any mining
    OS" under it.

    Three to a row from five items up, two below that — a lone card on a
    three-wide final row reads as a mistake, and four in a 2x2 is a better
    shape than 3+1.

    payload: (items, title) where items is [(label, note), ...]
    """

    EMBLEM = False
    PAD = 30

    def __init__(self, items: list[tuple[str, str]], title: str = "", **kw):
        super().__init__(**kw)
        self.items, self.title = items, title

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr = self.frame
        n = len(self.items)
        top0 = self.heading(out, self.title, f)

        usable = fr.w - 2 * self.margin
        # **Three across is a landscape number.** At 1080 wide it is a 293px
        # card, which cannot hold a label and a note at readable size on a
        # phone. Portrait goes one column up to four items and two beyond that,
        # so the cards stay wide and the block grows downward — which is the
        # axis a 9:16 frame actually has to spare.
        #
        # **Three landscape cards go in one column, not 2+1.** A 2x2 grid with
        # its last cell empty reads as a layout that failed to fill rather than
        # as a set of three, and the user called it exactly that. One column of
        # full-width cards has no hole in it, and at 16:9 a card 1800px wide
        # with a label and a note is a better shape than a 880px one anyway.
        # Four still take the 2x2, which is a complete rectangle.
        if self.portrait:
            cols = 1 if n <= 4 else 2
        else:
            cols = 3 if n >= 5 else (2 if n == 4 else 1)
        rows = (n + cols - 1) // cols
        gap = 36
        cw = (usable - gap * (cols - 1)) // cols

        label_font, note_font = ((_font(54), _font(36)) if self.portrait
                                else (_font(46), _font(31)))
        inner = cw - 2 * self.PAD
        # Measure every card first and take one height for all of them. Cards
        # of different heights on a grid read as a broken layout, not as
        # variety, and wrapping is what decides height — the same lesson the
        # other beats learned about centring.
        wrapped = [(wrap(d, lab, label_font, inner),
                    wrap(d, note, note_font, inner) if note else [])
                   for lab, note in self.items]
        lh, nh = (66, 46) if self.portrait else (58, 40)
        ch = max(self.PAD * 2 + len(lw) * lh + (14 + len(nw) * nh if nw else 0)
                 for lw, nw in wrapped)

        block = rows * ch + gap * (rows - 1)
        top = max(top0, (fr.h - block) // 2)

        for i, (lw, nw) in enumerate(wrapped):
            e = self.due(i, n, f)
            if e < 0:
                continue
            r, c = divmod(i, cols)
            x = self.margin + c * (cw + gap)
            y = top + r * (ch + gap) + int(round(RISE * (1.0 - e)))
            a = int(255 * min(1.0, e))

            # A panel rather than an outline alone: on a photographic backdrop
            # an unfilled box lets the blur through and the type loses its
            # ground. 0.55 black is enough to seat it without reading as a
            # second, darker frame.
            d.rounded_rectangle([x, y, x + cw, y + ch], radius=14,
                                fill=(0, 0, 0, int(140 * min(1.0, e))),
                                outline=self.brand.primary + (a,), width=3)
            ty = y + self.PAD
            for ln in lw:
                d.text((x + self.PAD, ty), ln, font=label_font,
                       fill=self.brand.ink + (a,))
                ty += lh
            if nw:
                ty += 14
                for ln in nw:
                    d.text((x + self.PAD, ty), ln, font=note_font,
                           fill=self.brand.primary + (int(a * 0.86),))
                    ty += nh


class Logos(Beat):
    """Brand tiles for named platforms, revealed one per caption.

    **The narration names companies; the screen should show them.** A script
    that says "Coinbase. Binance. Crypto.com." over a stock photograph of a
    trading desk is asking the viewer to hold three names in their head with no
    help, and the names are the content. The user's note on the first
    crypto-exchanges cut was exactly this, and it is general: whenever a beat's
    items are *brands*, the brand mark is the strongest possible item art.

    **The site's exchange images are full-bleed brand cards, not transparent
    icons**, and that is what makes this cheap. `public/images/exchanges/` has
    27 of them at ~900x506 — a blue Coinbase card, a yellow Binance card, a
    black Uniswap card. Drawn as rounded tiles they read as a lineup of
    products, which is a silhouette no other beat in the vocabulary has: no
    column of type, no ragged edge, no list.

    They also solve the palette problem rather than causing it. A yellow
    Binance card next to a gold heading would clash if the tile were the
    subject, but at a third of the frame width on a black ground it reads as a
    logo, which is a thing a viewer expects to be its own colour.

    Landscape puts up to four across; portrait stacks them down the frame,
    which is the axis 9:16 has to spare. An optional second element is a short
    label under the tile — "Custodial", "Non-custodial" — for when the lineup
    is making a point rather than just naming names.

    **It can carry verdicts, and it should when the point is a verdict.** A
    third element per item turns the tile into a two-phase beat exactly like
    `checklist`: the tiles arrive as the voice names them, then in the pause a
    tick or a cross draws into each corner. That is what keeps the lineup an
    open question for a few seconds instead of a table — and losing that payoff
    is the one thing that would have made this beat worse than the checklist it
    replaces in the crypto-exchanges short.

    payload: (items, title) where items is
    [slug | (slug, label) | (slug, label, ok), ...] and `slug` is either an
    exchange slug resolved under `images/exchanges/` or a path to any image.
    """

    EMBLEM = False
    BADGE = 64                  # the tick/cross drawn into a tile's corner

    # The site's own exchange art. Resolved by slug so a script says
    # `"binance"` rather than carrying a path and an extension it has to keep
    # correct — the extensions are a mix of png, jpg and webp.
    DIR = Path.home() / "Coding/crypto-wiki/public/images/exchanges"

    def __init__(self, items: list, title: str = "",
                 groups: list[tuple[str, int]] | None = None, **kw):
        super().__init__(**kw)
        self.title = title
        # `groups` is [(heading, count), ...] summing to len(items). It puts a
        # centred heading above each run of tiles and forces a single column,
        # which is what a lineup needs the moment the *split* is the point
        # rather than the list: two crosses and two ticks in a 2x2 still leave
        # the viewer inferring what the sides mean.
        if groups and sum(c for _, c in groups) != len(items):
            raise ValueError(
                f"logos groups cover {sum(c for _, c in groups)} items but "
                f"{len(items)} were given")
        self.groups = groups
        norm = []
        for i in items:
            t = (i,) if isinstance(i, (str, Path)) else tuple(i)
            norm.append((t + ("", None))[:3] if len(t) < 3 else t)
        self.items = norm

    @classmethod
    def resolve(cls, slug: str | Path) -> Path | None:
        """An exchange slug or a path, as a file that exists."""
        p = Path(slug)
        if p.suffix and p.exists():
            return p
        for ext in (".png", ".jpg", ".jpeg", ".webp"):
            cand = cls.DIR / f"{p.stem}{ext}"
            if cand.exists():
                return cand
        return None

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr = self.frame
        n = len(self.items)
        top0 = self.heading(out, self.title, f)

        usable = fr.w - 2 * self.margin
        # Portrait stacks, but four *ungrouped* stacked tiles in 9:16 are 240px
        # tall each and the wordmarks stop being readable at arm's length, so
        # four go 2x2. **Grouped items always take one column**, whatever the
        # count: the group heading is the thing doing the explaining and a
        # heading over a 2x2 has to be read as covering both cells, which is
        # the ambiguity the grouping exists to remove.
        if self.groups:
            cols = 1 if self.portrait else min(max(c for _, c in self.groups), 4)
        else:
            cols = (1 if n <= 3 else 2) if self.portrait else min(n, 4)
        gap = 40 if not self.portrait else 30
        tw = (usable - gap * (cols - 1)) // cols
        # The cards are all near 16:9 and cropping them would cut the wordmark,
        # so the tile takes the card's own shape and the row takes its height.
        th = int(tw * 9 / 16)
        label_font = _font(46 if self.portrait else 38)
        head_font = _font(54 if self.portrait else 44)
        lab_h = 60 if any(lab for _, lab, _ in self.items) else 0
        head_h = 78 if self.groups else 0

        # One flat plan of what goes down the frame, so the fit and the draw
        # agree by construction: ("head", label, first_item_index) or
        # ("row", [item indices]).
        plan, i = [], 0
        for label, count in (self.groups or [("", n)]):
            if self.groups:
                plan.append(("head", label, i))
            for r in range(0, count, cols):
                plan.append(("row", None, list(range(i + r,
                                                     min(i + r + cols,
                                                         i + count)))))
            i += count

        def measure(t_h):
            cell = t_h + lab_h
            total = 0
            for k, (kind, _, _) in enumerate(plan):
                total += head_h if kind == "head" else cell
                if k:
                    total += gap
            return total, cell

        block, cell = measure(th)
        # **Width sets the tile size until height cannot take it.** Three
        # labelled tiles stacked in 9:16 come to 1737px against 1920 minus the
        # watermark band, so the last one ran off the bottom — the failure is
        # silent, because nothing in the pipeline knows the beat overflowed.
        # Shrink to fit rather than clip. Group headings are fixed height and
        # come out of the tiles' share, which is why this solves for `th`.
        room = fr.h - top0 - self.margin
        if block > room:
            fixed = sum(head_h for kind, _, _ in plan if kind == "head")
            fixed += gap * (len(plan) - 1) + lab_h * sum(
                1 for kind, _, _ in plan if kind == "row")
            rows = sum(1 for kind, _, _ in plan if kind == "row")
            th = max(60, int((room - fixed) / max(rows, 1)))
            tw = int(th * 16 / 9)
            block, cell = measure(th)

        y = max(top0, (fr.h - block) // 2)
        for k, (kind, label, payload) in enumerate(plan):
            if k:
                y += gap
            if kind == "head":
                # The heading arrives with its own first tile rather than at
                # f=0 — same reasoning as `compare(name_columns=True)`: a label
                # standing over an empty space is a table waiting to be read.
                e = self.due(payload, n, f)
                if e >= 0:
                    d.text((fr.w // 2, y + int(round(RISE * (1.0 - min(1.0, e))))),
                           label.upper(), font=head_font, anchor="ma",
                           fill=self.brand.primary + (int(255 * min(1.0, e)),))
                y += head_h
                continue

            row_w = len(payload) * tw + gap * (len(payload) - 1)
            for c, i in enumerate(payload):
                slug, lab, ok = self.items[i]
                e = self.due(i, n, f)
                if e < 0:
                    continue
                x = (fr.w - row_w) // 2 + c * (tw + gap)
                ty = y + int(round(RISE * (1.0 - e)))
                a = min(1.0, e)

                # **Raise rather than draw an empty box.** The site has 27
                # exchange cards and the first build of this beat drew a silent
                # empty tile for a name it did not have — the failure mode this
                # repo keeps rediscovering, where the log looks fine and the
                # frame is wrong. A missing logo is a script error, not a
                # render one.
                src = self.resolve(slug)
                if src is None:
                    raise FileNotFoundError(
                        f"no exchange logo for {slug!r} in {self.DIR} — the "
                        f"site has to own the brand card before a beat can "
                        f"show it")
                tile = cover(Image.open(src).convert("RGB"), tw, th)
                if a < 1.0:
                    tile = Image.blend(Image.new("RGB", tile.size,
                                                 self.brand.bg), tile, a)
                out.paste(tile, (x, ty))
                d.rounded_rectangle([x, ty, x + tw, ty + th], radius=12,
                                    outline=self.brand.primary + (int(255 * a),),
                                    width=3)
                if lab:
                    d.text((x + tw // 2, ty + th + 12), lab.upper(),
                           font=label_font, anchor="ma",
                           fill=self.brand.ink + (int(230 * a),))

                # Phase two: the verdict, drawn into the tile's top-right on a
                # black disc so it reads against a card of any colour — Binance
                # is yellow and Uniswap is black, and a gold tick has to
                # survive both.
                if ok is None:
                    continue
                m = self.marked(i, f)
                if m < 0:
                    continue
                b = self.BADGE
                cx, cy = x + tw - b // 2 - 14, ty + b // 2 + 14
                d.ellipse([cx - b // 2, cy - b // 2, cx + b // 2, cy + b // 2],
                          fill=(0, 0, 0, 210))
                colour = self.brand.primary if ok else self.brand.negative
                mark(d, cx - b // 4, cy - b // 4, b // 2, ok, colour,
                     progress=m)
            y += cell

class Steps(Beat):
    """A numbered sequence along a track. For a procedure, not a set.

    The one thing none of the other beats can show is **order**. A checklist of
    "install the drivers, install the miner, join a pool" is a set of unrelated
    facts; the same three on a track with arrows between them is a procedure,
    and a how-to video is mostly procedures. This is the layout the strategy
    doc listed as `timeline` and never built.

    **Numbers are correct here and wrong on a chapter card**, which is worth
    being explicit about because the chapter card's docstring bans them. A
    numbered agenda tells the viewer they are being lectured. A numbered
    *sequence* is the content — step three genuinely comes after step two, and
    hiding that would be withholding the thing the beat is for.

    The track draws left to right ahead of the nodes, so the shape of the
    sequence is established before any of it has content — the same trick the
    comparison's dividing rule uses, and for the same reason.

    Four or five steps. Six sets the labels too narrow to wrap decently at
    1920; split into two beats before going wider.

    **In portrait the track runs down, not across**, and that is the only
    honest way to do it: five nodes across 1080 is a 216px slot, which cannot
    hold a wrapped label at phone-readable size. Turning the track ninety
    degrees costs nothing and gains everything — a 9:16 frame has height to
    spare and no width at all, and a vertical sequence is if anything the more
    natural reading order. Three or four steps in portrait; five fits but sets
    the labels tight.

    payload: (steps, title) where steps is [text, ...]
    """

    EMBLEM = False
    R = 46                      # node radius

    def __init__(self, steps: list[str], title: str = "", **kw):
        super().__init__(**kw)
        self.steps, self.title = steps, title

    def content(self, out: Image.Image, f: float) -> None:
        if self.portrait:
            return self._vertical(out, f)
        return self._horizontal(out, f)

    def _vertical(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr = self.frame
        n = len(self.steps)
        top0 = self.heading(out, self.title, f)

        rr = int(self.R * 1.25)
        label_font, num_font = _font(52), _font(52)
        lx = self.margin + rr * 2 + 40
        lw = fr.w - lx - self.margin
        wrapped = [wrap(d, t, label_font, lw) for t in self.steps]

        # Rows are as tall as their own label needs, so a two-line step does
        # not force every other node apart.
        line_h, pad = 62, 54
        heights = [max(rr * 2, len(w) * line_h) + pad for w in wrapped]
        block = sum(heights) - pad
        top = max(top0, (fr.h - block) // 2)

        cx = self.margin + rr
        centres = []
        y = top
        for h in heights:
            centres.append(y + max(rr, (h - pad) // 2))
            y += h

        # The track first, drawn downward as the beat opens — the same trick
        # the horizontal version and the comparison's divider use.
        e = ease_out(min(1.0, (self.at(f) - self.start) / 0.55))
        y0, y1 = centres[0], centres[-1]
        d.line([(cx, y0), (cx, y0 + (y1 - y0) * e)],
               fill=self.brand.primary + (110,), width=3)

        for i, lines in enumerate(wrapped):
            ev = self.due(i, n, f)
            if ev < 0:
                continue
            cy = centres[i]
            a = int(255 * min(1.0, ev))
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                      fill=self.brand.bg + (255,),
                      outline=self.brand.primary + (a,), width=4)
            num = str(i + 1)
            tb = d.textbbox((0, 0), num, font=num_font)
            d.text((cx - (tb[2] - tb[0]) / 2 - tb[0],
                    cy - (tb[3] - tb[1]) / 2 - tb[1]),
                   num, font=num_font, fill=self.brand.primary + (a,))

            ty = cy - (len(lines) * line_h) // 2 + int(round(RISE * (1.0 - ev)))
            for ln in lines:
                d.text((lx, ty), ln, font=label_font,
                       fill=self.brand.ink + (a,),
                       stroke_width=3, stroke_fill=(0, 0, 0, a))
                ty += line_h

    def _horizontal(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr = self.frame
        n = len(self.steps)
        top0 = self.heading(out, self.title, f)

        usable = fr.w - 2 * self.margin
        slot = usable / n
        label_font, num_font = _font(38), _font(42)
        lw = int(slot - 46)
        wrapped = [wrap(d, s, label_font, lw) for s in self.steps]

        block = self.R * 2 + 40 + max(len(w) for w in wrapped) * 48
        top = max(top0, (fr.h - block) // 2)
        cy = top + self.R

        # The track first, drawn across as the beat opens.
        e = ease_out(min(1.0, (self.at(f) - self.start) / 0.55))
        x0 = self.margin + slot / 2
        x1 = self.margin + usable - slot / 2
        d.line([(x0, cy), (x0 + (x1 - x0) * e, cy)],
               fill=self.brand.primary + (110,), width=3)

        for i, lines in enumerate(wrapped):
            ev = self.due(i, n, f)
            if ev < 0:
                continue
            cx = self.margin + slot * (i + 0.5)
            a = int(255 * min(1.0, ev))
            rr = self.R

            # The node is filled with the page ground, not left transparent —
            # the track runs behind it and a line crossing a numeral is the
            # kind of two-graphics-at-once fault the transitions doc warns
            # about.
            d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                      fill=self.brand.bg + (255,),
                      outline=self.brand.primary + (a,), width=4)
            num = str(i + 1)
            tb = d.textbbox((0, 0), num, font=num_font)
            d.text((cx - (tb[2] - tb[0]) / 2 - tb[0],
                    cy - (tb[3] - tb[1]) / 2 - tb[1]),
                   num, font=num_font, fill=self.brand.primary + (a,))

            ty = cy + rr + 40 + int(round(RISE * (1.0 - ev)))
            for ln in lines:
                tb = d.textbbox((0, 0), ln, font=label_font)
                d.text((cx - (tb[2] - tb[0]) / 2 - tb[0], ty), ln,
                       font=label_font, fill=self.brand.ink + (a,),
                       stroke_width=3, stroke_fill=(0, 0, 0, a))
                ty += 48


BEATS = {
    "chapter": ChapterCard,
    "checklist": Checklist,
    "stat": Stat,
    "compare": Compare,
    "quote": Quote,
    "bars": Bars,
    "grid": Grid,
    "steps": Steps,
    "logos": Logos,
}

# How many things a beat reveals, which is what its `reveals` list has to be as
# long as. A chapter card reveals nothing on a clock — it settles as one block.
_COUNT = {
    "chapter": lambda p: 0,
    "checklist": lambda p: len(p[0]),
    "stat": lambda p: 1,
    "compare": lambda p: len(p[1]) + len(p[3]) + (2 if len(p) > 4 and p[4] else 0),
    "quote": lambda p: 1,
    "bars": lambda p: len(p[0]),
    "grid": lambda p: len(p[0]),
    "steps": lambda p: len(p[0]),
    "logos": lambda p: len(p[0]),
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
                         label=shot.payload or None,
                         note=shot.note,
                         begin=shot.clip_at)
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
