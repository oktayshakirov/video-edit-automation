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
from ..core.draw import (contain, cover, ease_out, mark, partial,
                         shadow_text, subpixel, wrap)
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

    **No number by default, and that is still the point.** The first build set
    a `02` in 150px gold above every title, which turned the video into a
    slide deck — a numbered agenda is the visual language of a presentation,
    and it tells the viewer they are being lectured rather than told
    something. It also exposed an off-by-one nobody would otherwise have
    seen: numbering ran from the section index, and since the opening section
    carries no card, the first one on screen read "02".

    **`number` is the one deliberate exception**, for a script that is
    genuinely counting something the narration also counts out loud ("myth
    one", "myth two"). That is not an agenda — an agenda numbers *chapters*,
    which the viewer did not ask for and does not care about; this numbers
    the *thing the video is about*, which the viewer is actively tracking.
    Pass it only when the narration itself says the number; a numeral with no
    matching word is right back to being a slide deck.

    **Usually a question, not always.** A question is the strongest form here
    because it makes the next twenty seconds an answer the viewer is waiting
    for. But a section that resolves something wants a statement, and forcing
    "What did that turn it into?" onto a conclusion is worse than just saying
    it. The beat does not care which; write whichever the moment is.

    Centred on both axes, because it is the only beat with nothing else in the
    frame, and left-aligned type in an empty 16:9 frame reads as a slide with a
    missing bullet list.

    payload: (title,) or (title, number)
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
    NUM_SCALE = 1.7          # the numeral, relative to the title size
    NUM_GAP = 34             # clear space between the numeral and the rule

    def __init__(self, title: str, number: int | None = None, **kw):
        super().__init__(**kw)
        self.title, self.number = title, number

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out)
        w = self.frame.w - 2 * self.margin
        size = self.SIZE_PORTRAIT if self.portrait else self.SIZE
        font = _display(size)
        lines = wrap(d, self.title, font, w)

        line_h = int(size * 1.26)
        block = len(lines) * line_h

        # The numeral sits above the rule, so it is charged to the same
        # vertical centring as the title block — otherwise adding it pushes
        # the whole card down rather than growing it around one centre.
        num_font, num_h, num_str = None, 0, ""
        if self.number is not None:
            num_size = int(size * self.NUM_SCALE)
            num_font = _display(num_size)
            num_str = str(self.number)
            num_h = int(num_size * 1.15)
        extra = (num_h + self.NUM_GAP) if self.number is not None else 0

        e = ease_out(min(1.0, (self.at(f) - self.start) / 0.5))
        y = ((self.frame.h - block - extra) // 2 + extra
             + int(round(26 * (1.0 - e))))

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

        if self.number is not None:
            ny = rule_y - self.NUM_GAP - num_h + int(round(26 * (1.0 - e)))
            tw = d.textlength(num_str, font=num_font)
            shadow_text(d, ((self.frame.w - tw) / 2, ny), num_str, num_font,
                        self.brand.primary, blur=10, drop=(4, 6))

        for ln in lines:
            tw = d.textlength(ln, font=font)
            shadow_text(d, ((self.frame.w - tw) / 2, y), ln, font,
                        self.brand.ink, blur=10, drop=(4, 6))
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
            shadow_text(d, (x + gutter, y_in), text, font, self.brand.ink)

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

    def __init__(self, value: str, label: str = "", note: str = "",
                 count: bool = True, **kw):
        super().__init__(**kw)
        self.value, self.label, self.note = value, label, note
        # A value that is *mostly* digits counts up; one that is a word does
        # not. Splitting on that rather than on a flag means a script never has
        # to think about it — "1.1M" animates, "YES / NO" holds.
        #
        # **`count=False` forces the hold**, for a magnitude whose partial
        # values read as real claims rather than as an animation — "$4B+"
        # racing up shows "$1B+", "$2B+", "$3B+", each a plausible wrong
        # figure. This is the year rule ("2009" counting through 1780) applied
        # by hand where the renderer cannot tell a partial from a fact.
        m = re.match(r"^(\D*?)([\d,.]+)(\D*)$", value.strip()) if count else None
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
        shadow_text(d, (x, y + int(round(RISE * 2 * (1.0 - e)))),
                    self._value(f), big, self.brand.primary,
                    blur=12, drop=(5, 7))

        if self.note:
            note_font = _font(46)
            ny = y + int(200 * 1.25)
            for ln in wrap(d, self.note, note_font, w):
                shadow_text(d, (x, ny), ln, note_font, self.brand.ink)
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
                shadow_text(d, (x, top + int(round(RISE
                                                    * (1.0 - min(1.0, eh))))),
                            title.upper(), title_font, self.brand.primary)
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
                    shadow_text(d, (x, y_in), ln, item_font,
                                self.brand.ink)
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
            shadow_text(d, (x, y), ln, font, self.brand.ink,
                        blur=9, drop=(4, 5))
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

    **The track is shortened by the widest value in the payload**, because a
    bar at fraction 1.000 fills it and leaves its own label nowhere to go. The
    first version clamped the label's start x to just inside the track - a
    clamp on the anchor rather than on the extent - so a full-length row
    printed "50 BTC" as "50 BT" off the edge of the frame, unclipped and
    unraised. Setting that one label inside the bar was tried and is worse: the
    value font is 46px against a 30px bar, and one row treated unlike the other
    four reads as a fault. Reserving the column costs a few percent of every
    bar, which is invisible because bars are read against each other.

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
        # **Reserve the value column before laying out the track.** A bar at
        # fraction 1.000 fills the track by definition, so its value has
        # nowhere to go: the halving chart's top row printed "50 BTC" as
        # "50 BT" against the frame edge, and nothing clipped it or raised.
        # Putting that one label *inside* the bar was tried and is worse — the
        # value font is 46px against a 30px bar, so a centred label is cut off
        # top and bottom, and one row treated differently from the rest reads
        # as a fault rather than as a rule. Shortening the track for every row
        # keeps one treatment and costs a few percent of bar length, which is
        # invisible because the bars are read against each other.
        vw = max((d.textlength(v, font=value_font)
                  for _, _, v in self.rows if v), default=0.0)
        if vw:
            w -= int(vw) + 44
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

            shadow_text(d, (x, y), label, label_font, self.brand.ink)

            by = y + 58
            bh = 30
            # The track, so an unfilled bar still reads as "out of something".
            d.rectangle([x, by, x + w, by + bh], fill=(255, 255, 255, 26))
            bw = int(w * max(0.0, min(1.0, frac)) * g)
            if bw > 1:
                d.rectangle([x, by, x + bw, by + bh],
                            fill=self.brand.primary + (235,))
            if value:
                shadow_text(d, (x + bw + 22, by - 8), value, value_font,
                            self.brand.primary)


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

    **A card may carry an icon** as a third element, `(label, note, emoji)`.
    This is the skill's long-standing open request ("an emoji beside each
    grid card... rain for rain, a white circle for white noise") and it is
    what makes a set of options readable at a glance instead of read as four
    lines of type. The glyph sits at the card's right edge, vertically
    centred, so the label and note keep their full column and the icon reads
    as the card's marker rather than as a bullet.

    payload: (items, title) where items is [(label, note) | (label, note, emoji), ...]
    """

    EMBLEM = False
    PAD = 30

    def __init__(self, items: list[tuple], title: str = "", **kw):
        super().__init__(**kw)
        self.items = [tuple(it) + (None,) if len(it) < 3 else tuple(it)
                      for it in items]
        self.title = title

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
        # An icon eats into the text column, so the wrap width has to know
        # about it before anything is measured — otherwise a label wraps to
        # the full card width and then gets a glyph laid over its last word.
        # **64 in landscape, not 46.** A two-column card at 1920 is ~880px
        # wide, and a 46px glyph in the corner of it read as a smudge rather
        # than as an icon — the point of the icon is to be legible before the
        # label is, which it was not.
        icon_h = (54 if self.portrait else 64) if any(
            e for _, _, e in self.items) else 0
        icon_col = int(icon_h * 1.55) if icon_h else 0
        inner = cw - 2 * self.PAD - icon_col
        # Measure every card first and take one height for all of them. Cards
        # of different heights on a grid read as a broken layout, not as
        # variety, and wrapping is what decides height — the same lesson the
        # other beats learned about centring.
        wrapped = [(wrap(d, lab, label_font, inner),
                    wrap(d, note, note_font, inner) if note else [])
                   for lab, note, _ in self.items]
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

            icon = self.items[i][2]
            if icon and icon_h:
                from ..core.vertical import emoji_image
                im = emoji_image(icon, icon_h)
                if a < 255:
                    im = im.copy()
                    im.putalpha(im.getchannel("A").point(
                        lambda v: v * a // 255))
                # `out` is RGB; hand the glyph's alpha in as the paste mask.
                out.paste(im, (x + cw - self.PAD - im.width,
                               y + (ch - im.height) // 2), im)


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

    **An item may carry an icon**, written as `(text, emoji)` instead of a
    bare string. The user's note on the myths cut was that a bare numbered
    track is "a list of words" and wanted something under each item; an emoji
    is the cheapest icon that is already licensed, already colour, and already
    solved — `core.vertical.emoji_image` does the Apple Color Emoji
    bitmap-strike dance and caches, which matters because a beat draws the
    same five glyphs on every one of its ~480 frames.

    The icon replaces the numeral inside the node rather than sitting beside
    the label. Two reasons: a number and an icon both competing inside one
    layout is two systems, and the node is the only element on the track with
    a fixed box to put a square glyph in. **Order is still legible** — the
    track itself is the sequence, which is what it was always for.

    payload: (steps, title) where steps is [text | (text, emoji), ...]
    """

    EMBLEM = False
    R = 46                      # node radius

    def __init__(self, steps: list, title: str = "", **kw):
        super().__init__(**kw)
        # Normalise to (text, icon-or-None) so both layouts read one shape.
        self.steps = [(s, None) if isinstance(s, str) else (s[0], s[1])
                      for s in steps]
        self.title = title

    def _node(self, out: Image.Image, d: ImageDraw.ImageDraw, cx: int, cy: int,
              rr: int, i: int, alpha: int, num_font) -> None:
        """The numbered — or iconned — disc on the track."""
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=self.brand.bg + (255,),
                  outline=self.brand.primary + (alpha,), width=4)
        icon = self.steps[i][1]
        if icon:
            from ..core.vertical import emoji_image
            im = emoji_image(icon, int(rr * 1.15))
            if alpha < 255:
                # Never mutate the cached glyph — fade a copy's alpha instead.
                im = im.copy()
                im.putalpha(im.getchannel("A").point(
                    lambda v: v * alpha // 255))
            # `out` is RGB (the background pass returns RGB), so the emoji's
            # own alpha has to be handed in as the paste mask rather than
            # composited — `alpha_composite` requires an RGBA target.
            out.paste(im, (cx - im.width // 2, cy - im.height // 2), im)
            return
        num = str(i + 1)
        tb = d.textbbox((0, 0), num, font=num_font)
        d.text((cx - (tb[2] - tb[0]) / 2 - tb[0],
                cy - (tb[3] - tb[1]) / 2 - tb[1]),
               num, font=num_font, fill=self.brand.primary + (alpha,))

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
        wrapped = [wrap(d, t, label_font, lw) for t, _ in self.steps]

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
            self._node(out, d, cx, cy, rr, i, a, num_font)

            ty = cy - (len(lines) * line_h) // 2 + int(round(RISE * (1.0 - ev)))
            for ln in lines:
                shadow_text(d, (lx, ty), ln, label_font,
                            self.brand.ink + (a,), alpha=a)
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
        wrapped = [wrap(d, s, label_font, lw) for s, _ in self.steps]

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
            self._node(out, d, int(cx), int(cy), rr, i, a, num_font)

            ty = cy + rr + 40 + int(round(RISE * (1.0 - ev)))
            for ln in lines:
                tb = d.textbbox((0, 0), ln, font=label_font)
                shadow_text(d, (cx - (tb[2] - tb[0]) / 2 - tb[0], ty),
                            ln, label_font, self.brand.ink + (a,), alpha=a)
                ty += 48


class Gauge(Beat):
    """One value on a scale, against a threshold. The beat for "how much is too much".

    **`stat` shows a bare number and `bars` shows proportions of a whole;
    neither can show a *limit*.** "Eighty-five decibels" is a figure with no
    meaning attached, and drawing it larger does not give it one — the fact
    the viewer needs is that it sits past the line where damage starts. That
    is a different claim from a proportion (`bars`) and a different graphic
    from a number in an empty half-frame (`stat`), and on both of these sites
    it is one of the commonest claims there is: decibels against safe
    exposure, a caffeine dose against a threshold, leverage against a
    liquidation point.

    It replaces the weakest `stat` uses rather than adding to them. A `stat`
    whose figure only means something relative to some other figure was
    always the wrong beat; there simply was not a right one.

    **The silhouette is one track, not several.** `bars` stacks rows down the
    left with labels beside them and reads as a chart; this is a single thick
    scale across the middle of the frame with a flag above it, and at a glance
    the two are not the same graphic. Keeping it to one row is the whole
    point — the moment a second row appears it is a bar chart.

    Two reveals, in this order:

    0. **The scale and the threshold.** The track draws across, the threshold
       uprights, and its label sets. This is the sentence that says what the
       limit is: "Eight hours a day is safe at eighty decibels."
    1. **The value.** The marker travels along the track to its position and
       the figure counts up over it. This is the sentence that says where the
       thing actually sits: "A hairdryer is ninety-five."

    So write the beat as **two caption chunks**, limit first and value second.
    Written the other way round the marker lands before there is a line for it
    to sit past, which is the "say the point, then show the graphic" rule
    inside a single beat.

    `frac` and `threshold` are fractions of the track, 0..1 — they are
    *positions*, not data, and it is the author's job to place them honestly.
    A logarithmic quantity (decibels, and most of what this beat is for) does
    not go on a linear track by dividing one number by another; place the
    ticks where the scale actually falls and put the real values in
    `scale_labels`.

    payload: (value, frac, label, threshold, threshold_label, title)
      value            "95 dB"      the figure, drawn on the flag
      frac             0.0..1.0     where the marker sits on the track
      label            "A HAIRDRYER"  what the value is, under the flag
      threshold        0.0..1.0 or None
      threshold_label  "SAFE FOR 8 HOURS"
      title            the beat's kicker
    """

    EMBLEM = False
    TRACK_H = 34
    GROW = 0.75                 # how long the marker takes to travel

    def __init__(self, value: str, frac: float, label: str = "",
                 threshold: float | None = None, threshold_label: str = "",
                 title: str = "", **kw):
        super().__init__(**kw)
        self.value, self.frac, self.label = value, float(frac), label
        self.threshold = None if threshold is None else float(threshold)
        self.threshold_label, self.title = threshold_label, title

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr = self.frame
        top0 = self.heading(out, self.title, f)

        x0 = self.margin
        w = fr.w - 2 * self.margin
        # A 34px track across 1080 reads as a hairline where the same track
        # across 1920 reads as a bar. Portrait is not landscape scaled down,
        # which is the note `Beat.__init__` already makes about the margin.
        track_h = self.TRACK_H if not self.portrait else 46
        # Room for the flag above and the threshold label below, rather
        # than the frame's own middle — a track centred at h/2 put the
        # figure high and left the bottom third of the frame empty.
        cy = max(top0 + 260, int(fr.h * 0.52))
        big = _display(132 if not self.portrait else 108)
        flag_font = _font(40 if not self.portrait else 44)
        thr_font = _font(34 if not self.portrait else 38)

        # --- reveal 0: the track and the threshold ------------------------
        e0 = self.due(0, 2, f)
        if e0 < 0:
            return
        draw_e = ease_out(min(1.0, (self.at(f) - (self.reveals[0]
                                                  if self.reveals else
                                                  self.start)) / 0.55))
        # The empty track, drawn across as the beat opens — the same device
        # `steps` and `compare` use, so the shape of the claim is established
        # before any value is in it.
        d.rounded_rectangle([x0, cy, x0 + w * draw_e, cy + track_h],
                            radius=track_h // 2,
                            fill=(255, 255, 255, 26))

        if self.threshold is not None:
            tx = x0 + w * max(0.0, min(1.0, self.threshold))
            if draw_e * w >= (tx - x0):
                # An upright through the track, and the region past it shaded
                # — the shading is what says "this side is the problem"
                # without a word of type doing it.
                d.rectangle([tx, cy, x0 + w, cy + track_h],
                            fill=self.brand.negative + (40,))
                d.line([(tx, cy - 54), (tx, cy + track_h + 54)],
                       fill=self.brand.ink + (150,), width=3)
                if self.threshold_label:
                    ty = cy + track_h + 70
                    for ln in wrap(d, self.threshold_label.upper(), thr_font,
                                   min(w * 0.42, w - (tx - x0) + 120)):
                        shadow_text(d, (tx + 16, ty), ln, thr_font,
                                    self.brand.ink + (170,))
                        ty += 42

        # --- reveal 1: the value travels ----------------------------------
        e1 = self.due(1, 2, f)
        if e1 < 0:
            return
        g = ease_out(min(1.0, (self.at(f) - self.reveals[1]) / self.GROW)
                     if self.reveals and len(self.reveals) > 1 else 1.0)
        vx = x0 + w * max(0.0, min(1.0, self.frac)) * g
        # **The fill changes colour where it crosses the line.** The first
        # version drew one primary-coloured fill straight over the shaded
        # danger zone, which hid the shading completely and left the whole
        # claim resting on a thin upright — on a rendered frame the bar simply
        # read as "quite full", not as "past the limit". Two colours say it
        # without a word of type: the beat is *about* the crossing, so the
        # crossing is the thing that has to be visible.
        over = (self.threshold is not None
                and self.frac > self.threshold)
        tx = x0 + w * (self.threshold or 0.0)
        d.rounded_rectangle([x0, cy, max(x0 + 1, min(vx, tx) if over else vx),
                             cy + track_h],
                            radius=track_h // 2,
                            fill=self.brand.primary + (235,))
        if over and vx > tx:
            d.rounded_rectangle([tx, cy, vx, cy + track_h],
                                radius=track_h // 2,
                                fill=self.brand.negative + (240,))
        head = self.brand.negative if over else self.brand.primary
        # **The marker is filled with the ink, ringed in the fill's colour.**
        # Filled with `head` it was the same colour as the bar it sits on and
        # disappeared into it — the one element that has to say *where* was
        # the least visible thing on the frame.
        d.ellipse([vx - 24, cy + track_h // 2 - 24,
                   vx + 24, cy + track_h // 2 + 24],
                  fill=self.brand.ink, outline=head, width=6)

        # The flag above the marker: the figure, and the label under it.
        #
        # **The label is placed off the figure's measured box, not off a
        # constant.** The first version set the value at `cy - 96` and the
        # label at `cy - 78`, which are 18px apart while the figure itself is
        # 132px tall — so "A HAIRDRYER" printed straight through "95 dB" on
        # the very first rendered frame. Nothing raises on overlapping type;
        # the only way to catch it is to look.
        a = int(255 * min(1.0, e1))
        tb = d.textbbox((0, 0), self.value, font=big)
        bw, bh = tb[2] - tb[0], tb[3] - tb[1]
        lab = self.label.upper() if self.label else ""
        lh = 52 if lab else 0
        rise = int(round(RISE * (1.0 - min(1.0, e1))))
        # Bottom of the whole flag sits a clear gap above the track.
        fy = cy - 46 - lh - bh + rise
        fx = min(max(vx - bw / 2 - tb[0], x0), x0 + w - bw)
        shadow_text(d, (fx, fy - tb[1]), self.value, big, head + (a,), alpha=a)
        if lab:
            lw = d.textlength(lab, font=flag_font)
            shadow_text(d, (min(max(vx - lw / 2, x0), x0 + w - lw),
                            fy + bh + 10), lab, flag_font,
                        self.brand.ink + (a,), alpha=a)


class Callout(Beat):
    """Labels and pointers drawn onto a photograph, one per line spoken.

    **This is the beat that changes the shots the other beats never touch.**
    Measured across the nineteen long-form scripts on these two channels,
    drawn beats are four to nine shots out of thirty to forty-five — the other
    three quarters of every video is a stock clip or a Ken Burns still with
    nothing on it but a slow push. No amount of new beat *shapes* moves that
    number, because a beat replaces a photograph rather than doing anything
    with one. This one puts the explanation **on** the picture, so a shot that
    was connective texture becomes a shot that carries an argument.

    It is also the vocabulary `longform.md` names as the reference channel's
    entire on-screen language — "nothing on screen but labels and arrows" —
    which this repo had quoted approvingly for a year and never built.

    Each item is a point on the picture and a short label beside it. A leader
    line draws from the point out to the label, and the dot pulses once as it
    lands, so the eye is taken to the place before it is given the word.

    **Coordinates are fractions of the picture, not of the frame** (0..1, from
    its top-left). That is the only workable choice: the picture is fitted, so
    where it sits in the frame depends on its own aspect ratio, and a fraction
    of the frame would move the label off the subject the moment the source
    changed. Read them off the source file.

    **The picture is fitted, never covered.** `PhotoShot` scales to cover and
    crops, which is right for a full-frame photograph and wrong here for two
    reasons: a crop moves the subject out from under coordinates that were
    measured on the source, and covering 1920 from the ~900px median source on
    these sites is the upscale the split layout exists to avoid. Fitted inside
    a margin, the median source is at or below 1:1 and the callouts land where
    they were placed. The picture carries the brand hairline, as every fitted
    photograph in this format does.

    The photograph is dimmed under the labels — `DIM`, 0.68. Type over an
    undimmed photograph is the legibility problem every other beat avoids by
    not having one, and a leader line disappears into a busy image entirely.

    payload: (picture, items, title)
      photo     Path to the image. Named `photo` rather than `picture`
                because `make_beat` already passes `picture=` to every beat
                for the split layout's right-hand column, and the two would
                collide — see `__init__`.
      items     [(label, x, y), ...] — x, y are fractions of the picture
      title     the beat's kicker
    """

    EMBLEM = False
    DIM = 0.68
    DOT = 13

    def __init__(self, photo: Path, items: list[tuple[str, float, float]],
                 title: str = "", **kw):
        # **The argument is `photo`, not `picture`, and it has to be.**
        # `make_beat` passes `picture=` to every beat as a keyword — it is the
        # split layout's right-hand column — so a first positional of that name
        # collides with it and every callout raises "multiple values for
        # argument 'picture'". Found by building one.
        kw.pop("picture", None)
        super().__init__(**kw)
        self.items, self.title = items, title
        src = Path(photo)
        if not src.exists():
            raise FileNotFoundError(f"callout picture not found: {src}")
        fr = self.frame
        # The panel: the frame less a margin, and a band off the top so the
        # kicker and the watermark are never drawn over.
        # **Reserve the heading band only when there is a heading.** The
        # first version always took `head_y + 96` off the top and a full
        # margin off the bottom, which on a 3:2 source left the picture
        # height-limited at ~1120px inside a 1920 frame with dead bands down
        # both sides. The picture is the subject of this beat; every pixel
        # spent not showing it is spent badly.
        self.top_band = (self.head_y + 74) if title else fr.logo_at[1] + 60
        pw = fr.w - 2 * self.margin
        ph = fr.h - self.top_band - 56
        im = Image.open(src).convert("RGB")
        if im.width * im.height == 0:
            raise ValueError(f"callout picture is empty: {src}")
        # Fitted, and never enlarged past the frame's own ceiling — the
        # coordinates were measured on the source and a cover-crop would move
        # the subject out from under them.
        k = min(pw / im.width, ph / im.height, fr.max_upscale)
        self.pw, self.ph = int(im.width * k), int(im.height * k)
        panel = im.resize((self.pw, self.ph), Image.LANCZOS)
        self.panel = (np.asarray(panel) * self.DIM).astype(np.uint8)
        self.px = (fr.w - self.pw) // 2
        self.py = self.top_band + (ph - self.ph) // 2

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        self.heading(out, self.title, f)
        out.paste(Image.fromarray(self.panel), (self.px, self.py))
        d.rectangle([self.px, self.py, self.px + self.pw, self.py + self.ph],
                    outline=self.brand.primary, width=3)

        n = len(self.items)
        font = _font(46 if not self.portrait else 50)
        for i, (label, fx, fy) in enumerate(self.items):
            e = self.due(i, n, f)
            if e < 0:
                continue
            a = int(255 * min(1.0, e))
            x = self.px + self.pw * max(0.0, min(1.0, float(fx)))
            y = self.py + self.ph * max(0.0, min(1.0, float(fy)))

            # The label goes to whichever side of the point has more room, so
            # a callout near the right edge does not run off the panel.
            right = x < self.px + self.pw * 0.55
            avail = ((self.px + self.pw) - x if right else x - self.px) - 120
            lines = wrap(d, label, font, max(220, avail))
            lw = max(d.textlength(ln, font=font) for ln in lines)
            leader = 96
            lx = x + leader + 18 if right else x - leader - 18 - lw
            ly = y - (len(lines) * 56) // 2

            # The leader draws out from the dot rather than appearing, which
            # is what takes the eye to the place before it is given the word.
            partial(d, [(x, y), (x + (leader if right else -leader), y)],
                    min(1.0, e * 1.6), self.brand.primary, 3)
            d.ellipse([x - self.DOT, y - self.DOT, x + self.DOT, y + self.DOT],
                      outline=self.brand.primary, width=4)
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=self.brand.primary)

            ty = ly + int(round(RISE * (1.0 - min(1.0, e))))
            for ln in lines:
                shadow_text(d, (lx, ty), ln, font, self.brand.ink + (a,),
                            alpha=a)
                ty += 56


class Diagram(Beat):
    """A mechanism: labelled nodes with arrows drawing between them.

    **The kind of beat this library did not have.** All nine existing beats
    are the same event — type arrives on a background, in the order it is
    spoken. None of them draws a *relationship*, so a video explaining how one
    thing causes another has only ever been able to show a bulleted summary of
    the causation next to a photograph. On channels whose whole subject is
    mechanism — how a transaction becomes a block, how noise damage becomes a
    phantom sound — that is the largest single gap in the format.

    **It is not `steps` with boxes.** `steps` is a numbered track: a
    *procedure*, where the numerals are the content and the viewer is being
    told what to do in what order. This is a causal chain: no numerals, boxes
    rather than discs, and an arrowhead between each pair that says *therefore*
    rather than *next*. The two are also different silhouettes at a glance,
    which is the test `beats.md` sets for a new shape.

    **`loop=True` is why this earns its place over a prettier `steps`.** A
    feedback cycle — the last node feeding back into the first — is not a
    sequence at all, and no other beat in the library can draw one. It is also
    exactly the mechanism the tinnitus articles keep describing (the quieter
    it gets, the more gain the brain applies, the louder the tone, the more
    you notice the quiet) and the one a list makes actively harder to follow,
    because a list has an end and the thing being described does not.

    One reveal per node. The connector into node `i` draws first and the node
    lands on it, so the arrow is already travelling while the sentence names
    where it is going. Write **one caption chunk per node**, like every other
    beat here.

    Three or four nodes. Five sets the labels too narrow to wrap decently
    across 1920, and a five-link causal chain is usually two mechanisms that
    want two beats.

    **In portrait the chain runs down**, for the reason `steps` records for
    its own track: four boxes across 1080 is a 270px slot, which cannot hold a
    wrapped label at phone-readable size.

    payload: (nodes, title, loop)
      nodes  [(label, note | None, emoji | None) | (label, note) | label, ...]
      title  the beat's kicker
      loop   draw the feedback arrow from the last node back to the first
    """

    EMBLEM = False
    ARROW = 0.28                # how long a connector takes to draw

    def __init__(self, nodes: list, title: str = "", loop: bool = False, **kw):
        super().__init__(**kw)
        norm = []
        for nd in nodes:
            if isinstance(nd, str):
                norm.append((nd, None, None))
            else:
                norm.append((nd[0],
                             nd[1] if len(nd) > 1 else None,
                             nd[2] if len(nd) > 2 else None))
        self.nodes, self.title, self.loop = norm, title, loop

    def _arrow(self, d: ImageDraw.ImageDraw, a: tuple, b: tuple,
               p: float) -> None:
        """A connector that draws from `a` to `b`, head last."""
        if p <= 0:
            return
        partial(d, [a, b], p, self.brand.primary, 4)
        # The head only lands once the shaft has arrived, so the arrow reads
        # as travelling rather than as a shape fading up.
        if p >= 0.999:
            self._head(d, a, b)

    def _head(self, d: ImageDraw.ImageDraw, a: tuple, b: tuple) -> None:
        """Just the arrowhead at `b`, pointing away from `a`.

        **Separate from `_arrow` because the loop needs a head with no shaft
        of its own.** The feedback arrow's shaft is the whole four-point
        polyline `partial` has already drawn; calling `_arrow` to cap it drew
        a second, straight 30px segment on top of the corner, which rendered
        as a stray tail hanging below the arrowhead. Visible on the first
        frame, invisible in the code.
        """
        vx, vy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(vx, vy) or 1.0
        ux, uy = vx / L, vy / L
        s = 20
        d.polygon([b, (b[0] - ux * s - uy * s * 0.6,
                       b[1] - uy * s + ux * s * 0.6),
                   (b[0] - ux * s + uy * s * 0.6,
                    b[1] - uy * s - ux * s * 0.6)],
                  fill=self.brand.primary)

    LINE, NOTE_LINE, PAD, ICON = 50, 40, 30, 74

    def _measure(self, d: ImageDraw.ImageDraw, w: int, label_font,
                 note_font) -> tuple[list, int]:
        """Wrap every node against a box `w` wide and return the height they
        all need.

        **Every box is as tall as the tallest one needs, not a constant.**
        The first version fixed `bh = 230`, and the four-node tinnitus chain
        put a two-line label and a two-line note in its third box: the note's
        second line printed straight through the bottom edge of the box.
        Nothing clips and nothing raises — a `rounded_rectangle` is drawn
        before the type and simply has type sitting outside it afterwards.
        Boxes of differing heights would be worse than the overflow, so the
        set is levelled up to whichever node needs the most.
        """
        laid = []
        for label, note, icon in self.nodes:
            lines = wrap(d, label, label_font, w - 44)
            nlines = wrap(d, note, note_font, w - 44) if note else []
            laid.append((lines, nlines, icon))
        need = max((self.ICON if ic else 0) + len(ln) * self.LINE
                   + len(nl) * self.NOTE_LINE + 2 * self.PAD
                   for ln, nl, ic in laid)
        return laid, need

    def _box(self, out: Image.Image, d: ImageDraw.ImageDraw,
             box: tuple[int, int, int, int], laid: tuple, e: float,
             label_font, note_font) -> None:
        x0, y0, x1, y1 = box
        a = int(255 * min(1.0, e))
        lines, note_lines, icon = laid
        # Filled with the page ground, like a `steps` node and for the same
        # reason: the connector runs behind it and a line crossing type is the
        # two-graphics-at-once fault the transitions doc warns about.
        d.rounded_rectangle([x0, y0, x1, y1], radius=18,
                            fill=self.brand.bg + (238,),
                            outline=self.brand.primary + (a,), width=3)
        block = ((self.ICON if icon else 0) + len(lines) * self.LINE
                 + len(note_lines) * self.NOTE_LINE)
        ty = (y0 + y1) // 2 - block // 2
        if icon:
            from ..core.vertical import emoji_image
            im = emoji_image(icon, 58)
            if a < 255:
                im = im.copy()
                im.putalpha(im.getchannel("A").point(lambda v: v * a // 255))
            out.paste(im, ((x0 + x1) // 2 - im.width // 2, ty), im)
            ty += self.ICON
        for ln in lines:
            tb = d.textbbox((0, 0), ln, font=label_font)
            shadow_text(d, ((x0 + x1) / 2 - (tb[2] - tb[0]) / 2 - tb[0], ty),
                        ln, label_font, self.brand.ink + (a,), alpha=a)
            ty += self.LINE
        for ln in note_lines:
            tb = d.textbbox((0, 0), ln, font=note_font)
            shadow_text(d, ((x0 + x1) / 2 - (tb[2] - tb[0]) / 2 - tb[0], ty),
                        ln, note_font, self.brand.primary + (a,), alpha=a)
            ty += self.NOTE_LINE

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        fr = self.frame
        n = len(self.nodes)
        top0 = self.heading(out, self.title, f)
        label_font = _font(42 if not self.portrait else 46)
        note_font = _font(32 if not self.portrait else 36)

        if self.portrait:
            bw = fr.w - 2 * self.margin
            laid, bh = self._measure(d, bw, label_font, note_font)
            # **The gap is what fills a 9:16 frame, not the boxes.** At a
            # fixed 108 a three-node chain ended around 1300 of 1920 and left
            # the bottom third of the frame empty — and a drawn beat burns no
            # caption there, so nothing else was ever going to fill it.
            # Boxes stay the size their content needs; the space between them
            # takes up the slack, within limits, so two chains of different
            # lengths still look like the same graphic.
            room = fr.h - top0 - 120 - (150 if self.loop else 0)
            gap = int(max(96, min(210, (room - n * bh) / max(1, n - 1))))
            block = n * bh + (n - 1) * gap
            top = max(top0, (fr.h - block - (150 if self.loop else 0)) // 2)
            boxes = [(self.margin, top + i * (bh + gap),
                      self.margin + bw, top + i * (bh + gap) + bh)
                     for i in range(n)]
            ends = [((self.margin + bw // 2, b[3]),
                     (self.margin + bw // 2, b[3] + gap)) for b in boxes[:-1]]
        else:
            usable = fr.w - 2 * self.margin
            gap = 86
            bw = int((usable - (n - 1) * gap) / n)
            laid, bh = self._measure(d, bw, label_font, note_font)
            top = max(top0 + 20, (fr.h - bh) // 2 - (40 if self.loop else 0))
            boxes = [(self.margin + i * (bw + gap), top,
                      self.margin + i * (bw + gap) + bw, top + bh)
                     for i in range(n)]
            ends = [((b[2], top + bh // 2), (b[2] + gap, top + bh // 2))
                    for b in boxes[:-1]]

        # Each connector belongs to the node it points *at*, so it is already
        # travelling while the sentence names where it is going.
        for i in range(n):
            e = self.due(i, n, f)
            if e < 0:
                continue
            if i > 0:
                t = self.at(f) - (self.reveals[i] if self.reveals
                                  and i < len(self.reveals) else self.start)
                self._arrow(d, ends[i - 1][0], ends[i - 1][1],
                            ease_out(min(1.0, max(0.0, t / self.ARROW))))
            self._box(out, d, boxes[i], laid[i], e, label_font, note_font)

        # The feedback arrow lands only once the whole chain is up — it is a
        # statement about the mechanism as a whole, not a step in it.
        if self.loop and n > 1 and self.due(n - 1, n, f) >= 1.0:
            last = self.reveals[n - 1] if self.reveals else self.start
            p = ease_out(min(1.0, max(0.0, (self.at(f) - last - self.ARROW)
                                      / 0.55)))
            if p > 0:
                if self.portrait:
                    x = self.margin + 40
                    y0, y1 = boxes[-1][3], boxes[0][1]
                    pts = [(boxes[-1][0], (boxes[-1][1] + y0) // 2),
                           (x - 60, (boxes[-1][1] + y0) // 2),
                           (x - 60, (y1 + boxes[0][3]) // 2),
                           (boxes[0][0], (y1 + boxes[0][3]) // 2)]
                else:
                    y = boxes[0][3] + 92
                    pts = [((boxes[-1][0] + boxes[-1][2]) // 2, boxes[-1][3]),
                           ((boxes[-1][0] + boxes[-1][2]) // 2, y),
                           ((boxes[0][0] + boxes[0][2]) // 2, y),
                           ((boxes[0][0] + boxes[0][2]) // 2, boxes[0][3])]
                partial(d, pts, p, self.brand.primary + (170,), 3)
                if p >= 0.999:
                    self._head(d, pts[-2], pts[-1])


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
    "gauge": Gauge,
    "callout": Callout,
    "diagram": Diagram,
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
    "gauge": lambda p: 2,
    "callout": lambda p: len(p[1]),
    "diagram": lambda p: len(p[0]),
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
                         begin=shot.clip_at,
                         ax=shot.clip_ax, ay=shot.clip_ay)
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
