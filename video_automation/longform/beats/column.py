"""Beats that set a content column on the left and a picture on the right.

The original five, and still the ones that carry a normal sentence: a turn
between sections, a list with verdicts, a single number, a comparison, and
a quotation. `beats.md` warns that three of these share one silhouette -
read that before reaching for a third list in one video."""

from __future__ import annotations

import math
import re

from PIL import Image, ImageDraw

from ...core.draw import ease_out, mark, shadow_text, wrap
from .base import DRAW, RISE, Beat, _display, _font

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
    VALUE_PX = 200              # the value's size when it fits the column
    VALUE_MIN = 96              # ...and the floor it will shrink to to fit
    EMBLEM = True

    def __init__(self, value: str, label: str = "", note: str = "",
                 count: bool = True, **kw):
        super().__init__(**kw)
        self.value, self.label, self.note = value, label, note
        self._px: int | None = None     # fitted lazily, once, in `_value_px`
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

    def _value_px(self, d: ImageDraw.ImageDraw, w: int) -> int:
        """The largest size at which the value fits the content column.

        **The value was drawn at a flat 200px and nothing checked the width**,
        so a long one ran straight out of its column and into the picture
        beside it — `BLOCK 170` with a portrait in the picture column, caught
        on `first-bitcoin-transaction` (2026-10-02). Every other beat that
        sets type across a fixed box already measures it; this one did not,
        and the overflow is silent because a `Beat` draws into the whole frame
        and the picture column is painted first.

        **Measured on the final value, not the current frame's**, and cached:
        a counting number is narrower on its way up, so fitting per frame
        would shrink the type and grow it again while the figure climbs —
        a resize animation nobody asked for on top of the count.
        """
        if self._px is None:
            size = self.VALUE_PX
            while size > self.VALUE_MIN and d.textlength(
                    self.value, font=_font(size)) > w:
                size -= 4
            self._px = size
        return self._px

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
        big = _font(max(12, int(self._value_px(d, w) * scale)))
        shadow_text(d, (x, y + int(round(RISE * 2 * (1.0 - e)))),
                    self._value(f), big, self.brand.primary,
                    blur=12, drop=(5, 7))

        if self.note:
            note_font = _font(46)
            ny = y + int(self._value_px(d, w) * 1.25)
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
        # **This beat has no picture column and cannot be given one.** Every
        # other split-layout beat keeps its content in the left half and the
        # photograph in `pic_box` on the right; a comparison uses *both*
        # halves by definition, so the right column's headings and items print
        # straight through the photograph. It rendered as a heading sitting on
        # top of a picture with items crossing it - "super messy", and rightly
        # so. Nothing raised, because `make_beat` passes `picture=` to every
        # beat and this one simply drew both. Refuse it instead: put the
        # picture on a neighbouring shot, where it is a shot rather than a
        # collision.
        if kw.get("picture") is not None:
            raise ValueError(
                "`compare` has no picture column - its right-hand column "
                "occupies exactly the space `picture=` would draw into, and "
                "the two print on top of each other. Give the photograph its "
                "own shot beside the beat.")
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
        # item is the thing that made the first build look unfinished. Drawn on
        # `open_p` so it glides at the same rate as the items that follow it,
        # rather than snapping in a fast `ease_out` while they ease.
        e = self.open_p(f, 1.0)
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


