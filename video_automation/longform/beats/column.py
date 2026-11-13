"""Beats that set a content column on the left and a picture on the right.

The original five, and still the ones that carry a normal sentence: a turn
between sections, a list with verdicts, a single number, a comparison, and
a quotation. `beats.md` warns that three of these share one silhouette -
read that before reaching for a third list in one video."""

from __future__ import annotations

import math
import re

from PIL import Image, ImageDraw

from ...core import typewriter
from ...core.draw import ease_out, mark, shadow_text, wrap
from .base import DRAW, RISE, Beat, _display, _font

class ChapterCard(Beat):
    """The turn between sections: one line, centred, spoken as it appears.

    **Typed on behind a caret, with a key click per character** (2026-10-20,
    the editor's call, after a code-tutorial reference). The narration still
    reads the title; the typing only changes how the type arrives. See
    `core/typewriter.py`.

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

    # **Arial Black, the thumbnail's face, not the caption face.** The editor's
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

    def __init__(self, title: str, number: int | None = None,
                 style: str | None = None, index: int | None = None,
                 label: str | None = None, **kw):
        super().__init__(**kw)
        self.title, self.number = title, number
        self.style, self.index = style or "type", index
        self.label = label
        if self.style == "grid":
            self.ground = "grid"

    def content(self, out: Image.Image, f: float) -> None:
        if self.style == "band":
            return self.band(out, f)
        if self.style == "grid":
            return self.gridcard(out, f)
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
        # **No rise any more: the title types on in place** (2026-10-20). A
        # caret travelling along a line that is also sliding up reads as two
        # animations fighting; the rule and the numeral still settle.
        y = (self.frame.h - block - extra) // 2 + extra

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

        # Typed, not set. Each line is placed where its *finished* centred
        # position will be and grows rightward from there - centring the
        # partial string would slide the whole line left on every keystroke.
        # The schedule is `typewriter.card_schedule`, the same one `_cues`
        # places the key clicks from.
        t = self.at(f)
        times = typewriter.card_schedule(self.title, self.start, self.hold)
        parts = typewriter.lines_shown(lines, typewriter.shown(times, t))
        caret = None
        for i, ln in enumerate(lines):
            x0 = (self.frame.w - d.textlength(ln, font=font)) / 2
            part = parts[i] if i < len(parts) else None
            if part:
                shadow_text(d, (x0, y), part, font,
                            self.brand.ink, blur=10, drop=(4, 6))
            if part is not None:
                caret = (x0 + d.textlength(part, font=font), y)
            y += line_h
        if caret is not None and typewriter.caret_on(times, t):
            self.caret(d, caret, size)

    def caret(self, d: ImageDraw.ImageDraw, at: tuple[float, float],
              size: int) -> None:
        """The `|` - a bar in the brand colour, not a glyph, so it has the
        cap height of the face and the weight of the rule above it."""
        x = at[0] + size * 0.08
        top = at[1] + size * 0.20
        w = max(4, int(round(size * 0.075)))
        d.rectangle([x, top, x + w, top + size * 0.86],
                    fill=self.brand.primary)


    # --- the band style (experimental, 2026-10-20) -----------------------
    #
    # After a documentary-channel reference the editor liked: a small glowing
    # "CHAPTER 2" over a solid band in the brand colour, the title in widely
    # tracked condensed caps inside it. No radial glow behind it - the beat's
    # own moving background stays. The band opens from the centre, the title
    # types into it on the same key clicks, and the whole card closes back to
    # the centre and fades before the cut.
    #
    # **The label is the one numeral this card has ever shown by default.**
    # The docstring above records why a numbered agenda was dropped; this is
    # the editor's call to try it again in a different treatment. If the band
    # ships, that paragraph needs revisiting rather than both standing.

    BAND_OPEN = 0.38
    BAND_CLOSE = 0.40
    FONT_BAND = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"

    def _band_layout(self, text: str):
        """Font, tracking and lines for the band, fitted once per card.

        One line wherever it stays big enough to read; a 9:16 frame takes a
        long title onto two lines rather than shrinking it to caption size.
        """
        from PIL import ImageFont
        W, H = self.frame.size
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        avail = W * (0.86 if self.portrait else 0.88)
        floor = W * (0.078 if self.portrait else 0.050)

        def width(s, font, track):
            return (sum(probe.textlength(c, font=font) for c in s)
                    + track * max(0, len(s) - 1))

        def fit(lines, top):
            size = top
            while size > 28:
                font = ImageFont.truetype(self.FONT_BAND, size)
                track = size * 0.16
                if max(width(ln, font, track) for ln in lines) <= avail:
                    return size, font, track
                size -= 2
            font = ImageFont.truetype(self.FONT_BAND, size)
            return size, font, size * 0.16

        top = int(H * (0.060 if self.portrait else 0.105))
        lines = [text]
        size, font, track = fit(lines, top)
        if size < floor and " " in text:
            words = text.split(" ")
            best = min(range(1, len(words)), key=lambda i: abs(
                len(" ".join(words[:i])) - len(" ".join(words[i:]))))
            lines = [" ".join(words[:best]), " ".join(words[best:])]
            size, font, track = fit(lines, top)
        # **Centre on the ink, not on the advance widths.** `textlength`
        # carries each glyph's side bearings and the tracking after the last
        # letter, so a line centred on it sits visibly right of the band's
        # middle - the editor caught it on the first band render. Each line is
        # drawn once here and measured by its real pixel extent.
        inks = []
        for ln in lines:
            im = Image.new("L", (int(width(ln, font, track) + size * 2),
                                 int(size * 2)), 0)
            dd = ImageDraw.Draw(im)
            x = size * 0.5
            for c in ln:
                dd.text((x, size * 0.5), c, font=font, fill=255)
                x += dd.textlength(c, font=font) + track
            l, t, r, b = im.getbbox()
            inks.append((l - size * 0.5, t - size * 0.5,
                         r - size * 0.5, b - size * 0.5))
        return lines, size, font, track, inks

    def band(self, out: Image.Image, f: float) -> None:
        from PIL import ImageFilter
        from .base import _smooth

        W, H = self.frame.size
        t = self.at(f)
        e = t - self.start
        fill = self.brand.band or self.brand.primary
        ink = self.brand.band_ink

        opening = ease_out(min(1.0, e / self.BAND_OPEN))
        closing = _smooth(max(0.0, (e - (self.hold - self.BAND_CLOSE))
                              / self.BAND_CLOSE))
        width_k = opening * (1.0 - closing)
        alpha = 1.0 - closing
        if width_k <= 0.002:
            return

        if not hasattr(self, "_band"):
            self._band = self._band_layout(self.title.upper())
        lines, size, font, track, inks = self._band
        text = " ".join(lines)

        # The band hugs the title, so a short title is not a thin word in a
        # frame-wide stripe.
        pad = size * 0.55
        band_w = max(r - l for l, _, r, _ in inks) + 2 * pad
        line_h = int(size * 1.08)
        # The ink block: first line's cap top to last line's baseline. The
        # band is that plus equal padding above and below.
        ink_top = inks[0][1]
        ink_h = (len(lines) - 1) * line_h + inks[-1][3] - ink_top
        vpad = size * 0.30
        band_h = int(ink_h + 2 * vpad)
        cy = int(H * (0.50 if self.portrait else 0.56))
        y0 = cy - band_h // 2
        cx = W / 2
        a8 = int(255 * alpha)

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        half = band_w * width_k / 2
        d.rectangle([cx - half, y0, cx + half, y0 + band_h], fill=(*fill, a8))

        # Typed into the band, each line from its finished left edge.
        times = typewriter.card_schedule(self.title, self.start, self.hold,
                                         "band")
        parts = typewriter.lines_shown(lines, typewriter.shown(times, t))
        caret = None
        for i, part in enumerate(parts):
            l, _, r, _ = inks[i]
            x = cx - (l + r) / 2
            ty = y0 + vpad - ink_top + i * line_h
            for ch in part:
                d.text((x, ty), ch, font=font, fill=(*ink, a8))
                x += d.textlength(ch, font=font) + track
            caret = (x - (track if part else 0), ty + ink_top)
        if caret and typewriter.caret_on(times, t) and closing == 0.0:
            cxr = caret[0] + size * 0.06
            cap = inks[0][3] - inks[0][1]
            d.rectangle([cxr, caret[1] - cap * 0.06,
                         cxr + max(4, size * 0.06), caret[1] + cap * 1.06],
                        fill=(*ink, a8))

        # The title lives inside the band: as the band closes, the letters are
        # cut by its edges rather than left hanging in the air beside it.
        if width_k < 1.0:
            clip = Image.new("L", (W, H), 0)
            ImageDraw.Draw(clip).rectangle(
                [cx - half, 0, cx + half, H], fill=255)
            layer.putalpha(Image.composite(layer.getchannel("A"),
                                           Image.new("L", (W, H), 0), clip))

        # The band's bloom: its own colour, blurred, under it.
        glow = layer.filter(ImageFilter.GaussianBlur(int(size * 0.45)))
        glow.putalpha(glow.getchannel("A").point(lambda v: min(255, int(v * 1.1))))

        # The label: white, with a white bloom of its own - the part of the
        # reference that reads as light rather than as type.
        lab_layer = None
        # The label: the section's kicker when the script wrote one, else
        # "CHAPTER n" in the long form. A Short takes no numeral - one
        # argument in sixty seconds has no chapters to count.
        lab = (self.label or "").upper() or (
            f"CHAPTER {self.index}"
            if self.index is not None and not self.portrait else "")
        if lab:
            lf = _display(int(size * 0.66))
            lab_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            ld = ImageDraw.Draw(lab_layer)
            lw = ld.textlength(lab, font=lf)
            ly = (y0 - int(size * 1.02)
                  + int(round(16 * (1.0 - opening))))
            la = alpha * ease_out(min(1.0, max(0.0, e - 0.10) / 0.45))
            ld.text(((W - lw) / 2, ly), lab, font=lf,
                    fill=(255, 255, 255, int(255 * la)))

        base = out.convert("RGBA")
        base.alpha_composite(glow)
        if lab_layer is not None:
            for r, k in ((int(size * 0.40), 1.3), (int(size * 0.12), 0.9)):
                g = lab_layer.filter(ImageFilter.GaussianBlur(r))
                g.putalpha(g.getchannel("A").point(
                    lambda v, k=k: min(255, int(v * k))))
                base.alpha_composite(g)
        base.alpha_composite(layer)
        if lab_layer is not None:
            base.alpha_composite(lab_layer)
        out.paste(base.convert("RGB"))


    # --- the grid style (2026-11-13) ---------------------------------------
    #
    # The editor on the band card: "lets try different overlay for the title
    # sections, the current one doesnt fit that well". The band is a slab of
    # brand colour over the moving gradient; this one sits on the dark ruled
    # ground (`base.grid_ground`) the explaining beats now use, so a chapter
    # reads as the next page of the same notebook rather than as a banner:
    #
    # * an eyebrow - "02  /  THE MEMORY TRAP" (number and kicker), small,
    #   tracked, in the brand colour - with a hairline drawing out from the
    #   middle under it;
    # * the title in the display face, white, typed behind the caret on the
    #   same clicks as every card (`typewriter`, lead "grid");
    # * four corner brackets closing in on the title block, the one element
    #   that moves on its own, like a viewfinder finding focus;
    # * the whole card lifts and fades out in its last 0.4s.

    GRID_OPEN = 0.45
    GRID_CLOSE = 0.40

    def _grid_layout(self):
        W, H = self.frame.size
        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        text = self.title
        avail = W * (0.84 if self.portrait else 0.74)
        size = int((self.SIZE_PORTRAIT if self.portrait else self.SIZE) * 1.15)
        floor = int(size * 0.62)
        lines = [text]
        while True:
            font = _display(size)
            if max(probe.textlength(ln, font=font) for ln in lines) <= avail:
                break
            if len(lines) == 1 and " " in text and size <= size + 0:
                words = text.split(" ")
                best = min(range(1, len(words)), key=lambda i: abs(
                    len(" ".join(words[:i])) - len(" ".join(words[i:]))))
                trial = [" ".join(words[:best]), " ".join(words[best:])]
                if max(probe.textlength(ln, font=font) for ln in trial) <= avail:
                    lines = trial
                    break
            size -= 4
            if size < floor:
                font = _display(size)
                break
        widths = [probe.textlength(ln, font=font) for ln in lines]
        asc = font.getbbox("H")
        cap = asc[3] - asc[1]
        return lines, font, size, widths, asc[1], cap

    def gridcard(self, out: Image.Image, f: float) -> None:
        from PIL import ImageFilter
        from .base import _smooth

        W, H = self.frame.size
        t = self.at(f)
        e = t - self.start
        if not hasattr(self, "_grid"):
            self._grid = self._grid_layout()
        lines, font, size, widths, top_bear, cap = self._grid
        prim = self.brand.primary

        opening = ease_out(min(1.0, e / self.GRID_OPEN))
        closing = _smooth(max(0.0, (e - (self.hold - self.GRID_CLOSE))
                              / self.GRID_CLOSE))
        alpha = 1.0 - closing
        lift = -int(40 * closing)
        a8 = int(255 * alpha)

        line_h = int(size * 1.12)
        block_h = (len(lines) - 1) * line_h + cap
        cy = int(H * (0.50 if self.portrait else 0.54)) + lift
        y_top = cy - block_h // 2
        block_w = max(widths)
        cx = W / 2

        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)

        # Eyebrow: "02  /  KICKER", with a hairline drawing out under it.
        lab = (self.label or "").upper()
        num = (f"{self.index:02d}" if self.index is not None
               and not self.portrait else "")
        eyebrow = "  /  ".join(x for x in (num, lab) if x)
        padx, pady = size * 0.70, size * 0.55
        ey = int(cy - block_h / 2 - pady - size * 0.82)
        if eyebrow:
            ef = _display(int(size * 0.34))
            track = ef.size * 0.22
            ew = (sum(d.textlength(c, font=ef) for c in eyebrow)
                  + track * (len(eyebrow) - 1))
            ea = alpha * ease_out(min(1.0, max(0.0, e - 0.08) / 0.40))
            x = cx - ew / 2
            for c in eyebrow:
                d.text((x, ey + int(10 * (1 - ea))), c, font=ef,
                       fill=(*prim, int(255 * ea)))
                x += d.textlength(c, font=ef) + track
            rule_w = max(ew, block_w * 0.55) * opening
            ry = ey + ef.size * 1.45
            d.rectangle([cx - rule_w / 2, ry, cx + rule_w / 2, ry + 2],
                        fill=(*prim, int(170 * alpha)))

        # The title, typed.
        times = typewriter.card_schedule(self.title, self.start, self.hold,
                                         "grid")
        parts = typewriter.lines_shown(lines, typewriter.shown(times, t))
        caret = None
        for i, part in enumerate(parts):
            x = cx - widths[i] / 2
            ty = y_top - top_bear + i * line_h
            d.text((x, ty), part, font=font, fill=(255, 255, 255, a8))
            caret = (x + d.textlength(part, font=font), ty + top_bear)
        if caret and typewriter.caret_on(times, t) and closing == 0.0:
            d.rectangle([caret[0] + size * 0.05, caret[1] - cap * 0.05,
                         caret[0] + size * 0.05 + max(4, size * 0.07),
                         caret[1] + cap * 1.05], fill=(*prim, a8))

        # Corner brackets, closing in from wide to the block.
        far = 1.0 + 0.35 * (1.0 - opening)
        bx0 = cx - (block_w / 2 + padx) * far
        bx1 = cx + (block_w / 2 + padx) * far
        by0 = cy - (block_h / 2 + pady) * far
        by1 = cy + (block_h / 2 + pady) * far
        arm, wgt = size * 0.42, max(3, int(size * 0.045))
        ba = int(230 * alpha * opening)
        col = (*prim, ba)
        for (x, y, sx, sy) in ((bx0, by0, 1, 1), (bx1, by0, -1, 1),
                               (bx0, by1, 1, -1), (bx1, by1, -1, -1)):
            d.rectangle(sorted_box(x, y, x + sx * arm, y + sy * wgt), fill=col)
            d.rectangle(sorted_box(x, y, x + sx * wgt, y + sy * arm), fill=col)

        glow = layer.filter(ImageFilter.GaussianBlur(int(size * 0.35)))
        glow.putalpha(glow.getchannel("A").point(lambda v: int(v * 0.45)))
        base = out.convert("RGBA")
        base.alpha_composite(glow)
        base.alpha_composite(layer)
        out.paste(base.convert("RGB"))


def sorted_box(x0, y0, x1, y1):
    return [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]


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

    # --- the note card (2026-11-06) ----------------------------------------
    #
    # The editor's note on `random-tokens-in-wallet`: the list "is visually not
    # appealing - use bigger font, center them on the screen, make it look like
    # notes or use the typing effect". So with no picture column the list is a
    # note card centred on the frame: a dark sheet with faint ruled lines and a
    # margin rule in the brand colour, each item typed in at 96px behind a
    # caret, on the chapter card's key clicks, its verdict landing in the
    # margin. A checklist given a `picture=` keeps the column layout below.
    NOTE_SIZE = 96
    NOTE_PITCH = 160
    NOTE_PAD = 64               # card edge to the margin marks
    NOTE_MARGIN = 112           # card edge to the margin rule
    NOTE_LEAD = 0.05            # typing starts just after the caption does
    NOTE_SHARE = 0.75           # of the time to the next item the typing may take

    def __init__(self, items: list[tuple[str, bool]], title: str = "",
                 flow: bool = False, **kw):
        super().__init__(**kw)
        self.items, self.title, self.flow = items, title, flow
        self.note = self.pic is None and not self.portrait

    def type_times(self, i: int) -> list[float]:
        """When each character of item `i` appears - shared with the key-click
        cues in the builder, so a click never lands on an empty frame."""
        return note_type_times(self.items, self.reveals, self.start,
                               self.hold, i)

    def content(self, out: Image.Image, f: float) -> None:
        if self.note:
            return self._note(out, f)
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

    def _note(self, out: Image.Image, f: float) -> None:
        fr, br = self.frame, self.brand
        top = self.heading(out, self.title, f)
        font = _font(self.NOTE_SIZE)
        n = len(self.items)
        probe = ImageDraw.Draw(out)
        text_w = max(probe.textlength(t, font=font) for t, _ in self.items)
        cw = int(min(fr.w - 2 * 80, self.NOTE_MARGIN + 44 + text_w + 90))
        ch = n * self.NOTE_PITCH + 56 + 30
        x0 = (fr.w - cw) // 2
        y0 = max(top + 30, (fr.h - ch) // 2 + 20)
        t = self.at(f)
        enter = min(1.0, max(0.0, (t - self.start) / 0.45))
        if enter <= 0:
            return
        e = ease_out(enter)
        rise = int(26 * (1 - e))

        layer = Image.new("RGBA", fr.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")
        d.rounded_rectangle([x0, y0 + rise, x0 + cw, y0 + ch + rise],
                            radius=22, fill=(18, 18, 18, int(232 * e)),
                            outline=br.primary + (int(70 * e),), width=2)
        # Ruled lines under every row, and the margin rule.
        for i in range(n):
            ly = y0 + rise + 56 + i * self.NOTE_PITCH + self.NOTE_SIZE + 22
            d.line([(x0 + 24, ly), (x0 + cw - 24, ly)],
                   fill=(255, 255, 255, int(22 * e)), width=2)
        mx = x0 + self.NOTE_MARGIN
        d.line([(mx, y0 + rise + 20), (mx, y0 + ch + rise - 20)],
               fill=br.primary + (int(150 * e),), width=3)

        tx = mx + 44
        caret_at = None
        for i, (text, ok) in enumerate(self.items):
            times = self.type_times(i)
            k = typewriter.shown(times, t)
            if k <= 0:
                continue
            y = y0 + rise + 56 + i * self.NOTE_PITCH
            part = text[:k]
            shadow_text(d, (tx, y), part, font, br.ink + (255,), alpha=255)
            # Only the line typed last owns the caret: a finished line's
            # blink must not outlive the next line starting (it sat after
            # "history" on the first render, 2026-11-06).
            caret_at = (tx + d.textlength(part, font=font), y, times, k,
                        len(text))
            m = self.marked(i, f)
            if m < 0:
                continue
            colour = br.primary if ok else br.negative
            mark(d, x0 + self.NOTE_PAD - 22, y + 26, 56, ok,
                 colour + (255,), progress=m)
            if not ok:
                bb = d.textbbox((tx, y), text, font=font)
                mid = (bb[1] + bb[3]) // 2
                s = ease_out(min(1.0, (t - self.marks[i] - 0.05) / DRAW))
                if s > 0:
                    d.line([(tx, mid), (tx + (bb[2] - tx) * s, mid)],
                           fill=br.negative + (255,), width=6)
        # One caret, on the line being typed - or blinking after it once it
        # is done, until the next line starts.
        if caret_at is not None:
            x, y, times, k, L = caret_at
            if k < L or typewriter.caret_on(times, t):
                cx = x + self.NOTE_SIZE * 0.08
                d.rectangle([cx, y + self.NOTE_SIZE * 0.18,
                             cx + 5, y + self.NOTE_SIZE * 1.0],
                            fill=br.primary + (255,))
        out.paste(layer, (0, 0), layer)


def note_type_times(items: list, reveals: list | None, start: float,
                    hold: float, i: int) -> list[float]:
    """The note checklist's typing schedule for item `i`: it starts on the
    item's caption and takes at most `NOTE_SHARE` of the time to the next
    one (or to the shot's end), so a short sentence types fast rather than
    running over the next item."""
    n = len(items)
    rv = reveals or [start + hold * (j / max(n, 1)) * 0.85 for j in range(n)]
    s0 = rv[i] + Checklist.NOTE_LEAD
    nxt = rv[i + 1] if i + 1 < len(rv) else start + hold
    return typewriter.schedule(items[i][0], s0,
                               max_dur=max(0.3, (nxt - s0) * Checklist.NOTE_SHARE))


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
        # viewer to work out which list the voice was on — the editor's note was
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


