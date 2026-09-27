"""Beats that point at something.

A photograph with labels on it, a causal chain, pins on a plate, and
callouts onto a drawing. The shared idea is a leader that *travels* from
the thing to its label on the clause that names it; a label already joined
to its subject when the shot cuts in has skipped the only moment that
showed the viewer which part was meant."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text, wrap
from .base import RISE, Beat, _font, _round_corners, _smooth

class Callout(Beat):
    """A photograph in the middle, a column of labels each side pointing in.

    **This is the beat that changes the shots the other beats never touch.**
    Drawn beats are four to nine shots out of thirty-odd; the rest of every
    video is a stock clip or a Ken Burns still with nothing on it. A beat
    *replaces* a photograph, so no new beat shape moves that number. This one
    explains one instead — a shot that was connective texture starts carrying
    an argument.

    **Nothing lands inside the photo — the leaders stop at the frame.** Three
    versions failed before this one: text on the image fought the picture; a
    disc pinned on a chosen pixel looked arbitrary and defacing; an arrow
    reaching in to the detail still "pointed at the exact word". The user's
    call, and it is right: the label sits in a margin column, and its leader
    runs to a small dot **on the image border** — nothing crosses the edge.
    The dot sits roughly level with the thing it names (`y` places it along
    that edge) but it marks a place on the frame, not a point in the picture,
    so being a little off reads as "over here" rather than as a mistake.

    `x` picks the side; within a side the dots are placed by `y` and nudged
    apart so a cluster does not overlap, while the labels themselves stay
    evenly spaced down the column so the text block is always tidy.

    **The leader draws across the phrase, not in a pop** (`span_p`): the line
    travels from the label out to its dot on the frame while the phrase is
    spoken, the dot pulses and the label settles as it arrives. Same
    voice-synced clock as the diagram's connectors.

    **Coordinates are fractions of the photo** (0..1 from its top-left), not
    of the frame — the photo is fitted, so where it sits depends on its aspect
    ratio. Read them off the source file.

    Landscape only in practice. In portrait there is no width for side
    columns; the labels fall to a row under the image and the beat loses the
    thing that makes it work — in 9:16 the answer is `ImageOverlay` over
    moving footage, see `shorts.md`.

    payload: (photo, items, title)
      photo   Path to the image. Named `photo` not `picture` because
              `make_beat` passes `picture=` to every beat for the split
              layout and the two would collide — see `__init__`.
      items   [(label, x, y), ...] — x, y are fractions of the photo. `x`
              picks the side; `y` (and `x` in portrait) places the dot along
              that edge, roughly level with the thing. Nothing lands inside
              the image.
      title   the beat's kicker
    """

    EMBLEM = False
    DIM = 0.58
    DOT = 8                   # the marker where the leader meets the frame
    GUTTER = 360              # label column width each side, at 1920
    RAIL = 40                # px the label column sits off the image edge

    def __init__(self, photo: Path, items: list[tuple[str, float, float]],
                 title: str = "", **kw):
        # **The argument is `photo`, not `picture`, and it has to be.**
        # `make_beat` passes `picture=` to every beat as a keyword — the split
        # layout's right-hand column — so a first positional of that name
        # collides with it and every callout raises. Found by building one.
        kw.pop("picture", None)
        super().__init__(**kw)
        self.items, self.title = items, title
        src = Path(photo)
        if not src.exists():
            raise FileNotFoundError(f"callout photo not found: {src}")
        fr = self.frame
        self.top_band = (self.head_y + 74) if title else fr.logo_at[1] + 60
        bottom = fr.h - 56
        im = Image.open(src).convert("RGB")
        if im.width * im.height == 0:
            raise ValueError(f"callout photo is empty: {src}")

        if self.portrait:
            # No width for gutters — the photo takes the upper half and the
            # labels stack below it. Documented as the weak orientation.
            box_w = fr.w - 2 * self.margin
            box_h = int((bottom - self.top_band) * 0.52)
            self._below = True
        else:
            g = int(self.GUTTER * fr.w / 1920)
            box_w = fr.w - 2 * (self.margin + g)
            box_h = bottom - self.top_band
            self._below = False
        # Fitted, never covered: a crop moves the subject out from under
        # coordinates measured on the source, and covering 1920 from a ~900px
        # median source is the upscale the split layout exists to dodge.
        k = min(box_w / im.width, box_h / im.height, fr.max_upscale)
        self.pw, self.ph = int(im.width * k), int(im.height * k)
        panel = im.resize((self.pw, self.ph), Image.LANCZOS)
        self.panel = (np.asarray(panel) * self.DIM).astype(np.uint8)
        self.px = (fr.w - self.pw) // 2
        self.py = self.top_band + (
            0 if self._below else (box_h - self.ph) // 2)

        # Assign side/order and the edge contact points, once, in __init__ —
        # the layout must not shift as items reveal.
        idx = list(range(len(items)))
        if self._below:
            # Portrait: a plain vertical list under the image, each row's dot
            # on the bottom border at the item's x. Documented weak
            # orientation — this only has to be unambiguous, not elegant.
            order = sorted(idx, key=lambda j: items[j][1])
            self._sides = {i: ("below", k) for k, i in enumerate(order)}
            lo, hi = self.px + 30, self.px + self.pw - 30
            xs = self._spread([items[i][1] for i in order], lo, hi, 90)
            self._contact = {i: (x, self.py + self.ph)
                             for i, x in zip(order, xs)}
        else:
            left = [i for i in idx if items[i][1] < 0.5]
            right = [i for i in idx if i not in left]
            self._sides, self._contact = {}, {}
            for name, edge_x, group in (("left", self.px, left),
                                        ("right", self.px + self.pw, right)):
                order = sorted(group, key=lambda j: items[j][2])
                for k, i in enumerate(order):
                    self._sides[i] = (name, k)
                lo, hi = self.py + 26, self.py + self.ph - 26
                ys = self._spread([items[i][2] for i in order], lo, hi, 48)
                for i, y in zip(order, ys):
                    self._contact[i] = (edge_x, y)
            self._counts = {"left": len(left), "right": len(right)}

    @staticmethod
    def _spread(fracs: list[float], lo: float, hi: float,
                gap: float) -> list[float]:
        """Place each fraction between `lo` and `hi`, in order, nudged apart so
        no two contact points sit closer than `gap`. Keeps the dots roughly
        level with their features without letting a cluster overlap."""
        out: list[float] = []
        for fr in fracs:
            v = lo + (hi - lo) * max(0.0, min(1.0, fr))
            if out and v - out[-1] < gap:
                v = out[-1] + gap
            out.append(v)
        if out and out[-1] > hi:                      # slid off the end
            shift = out[-1] - hi
            out = [v - shift for v in out]
        if out and out[0] < lo:                       # now too tight to fit
            step = (hi - lo) / max(1, len(out) - 1)
            out = [lo + step * k for k in range(len(out))]
        return out

    def _label_y(self, i: int) -> tuple[str, float]:
        """(side, y) of item `i`'s label — evenly spaced down the column so the
        text block stays tidy even where the contact dots cluster."""
        side, slot = self._sides[i]
        if side == "below":
            return side, self.py + self.ph + 74 + slot * 60
        c = self._counts[side]
        top, span = self.py + 54, self.ph - 108
        return side, top + (span * (slot + 0.5) / c if c else span / 2)

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        self.heading(out, self.title, f)
        out.paste(Image.fromarray(self.panel), (self.px, self.py))
        d.rectangle([self.px, self.py, self.px + self.pw, self.py + self.ph],
                    outline=self.brand.primary, width=3)
        col = self.brand.primary

        n = len(self.items)
        font = _font(40 if not self.portrait else 44)
        for i, (label, fx, fy) in enumerate(self.items):
            e = self.due(i, n, f)
            if e < 0:
                continue
            draw = self.span_p(i, f, lead=0.10, cap=1.4)
            side, ly = self._label_y(i)
            cxp, cyp = self._contact[i]

            # The leader: from beside the label, out to a rail just off the
            # image, along it to the contact height, then a short stub to a
            # dot **on the frame**. Nothing crosses into the picture — the
            # dot marks a place on the border, it does not point at a pixel.
            if side == "below":
                bullet_x = self.margin + 4
                path = [(bullet_x, ly), (cxp, ly), (cxp, cyp)]
            else:
                rail_x = (self.px - self.RAIL if side == "left"
                          else self.px + self.pw + self.RAIL)
                path = [(rail_x, ly), (rail_x, cyp), (cxp, cyp)]
            partial(d, _round_corners(path, 13), draw, col, 3)

            # The dot on the frame, with one expanding pulse as it lands.
            if draw >= 0.6:
                pr = min(1.0, (draw - 0.6) / 0.4)
                if pr < 1.0:
                    rr = self.DOT + int(15 * pr)
                    d.ellipse([cxp - rr, cyp - rr, cxp + rr, cyp + rr],
                              outline=col + (int(200 * (1 - pr)),), width=3)
                d.ellipse([cxp - self.DOT, cyp - self.DOT,
                           cxp + self.DOT, cyp + self.DOT], fill=col)

            # The label, settling as the leader completes.
            if draw < 0.5:
                continue
            a = int(255 * min(1.0, (draw - 0.5) / 0.4))
            rise = int(round(RISE * (1.0 - a / 255)))
            if side == "below":
                shadow_text(d, (self.margin + 34, ly + 12), label, font,
                            self.brand.ink + (a,), alpha=a)
                continue
            g = int(self.GUTTER * self.frame.w / 1920)
            rail_x = (self.px - self.RAIL if side == "left"
                      else self.px + self.pw + self.RAIL)
            lines = wrap(d, label, font, g - 46)
            lty = ly - (len(lines) * 52) // 2 + rise
            for ln in lines:
                tw = d.textlength(ln, font=font)
                lx = (rail_x - 20 - tw if side == "left" else rail_x + 20)
                shadow_text(d, (lx, lty), ln, font, self.brand.ink + (a,),
                            alpha=a)
                lty += 52


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

    One reveal per node. Write **one caption chunk per node**, like every
    other beat here.

    **The connectors are drawn against the voice, not popped in.** The first
    version drew every arrow in a fixed 0.28s the instant its node's caption
    began, so the whole diagram was a burst of movement at the top of each
    phrase and then dead air. Now the connector between node `k` and node
    `k+1` draws *slowly, across the phrase that bridges them* — it starts a
    breath after box `k` lands and travels the whole gap until box `k+1`
    appears on its far end. The line grows while the narrator speaks the
    causal link; the box lands as the line reaches it. That is the synced
    animation the user asked for, and it is the whole reason the beat is worth
    more than a bulleted list.

    Three or four nodes. Five sets the labels too narrow to wrap decently
    across 1920, and a five-link causal chain is usually two mechanisms that
    want two beats.

    **In portrait the chain runs down**, for the reason `steps` records for
    its own track: four boxes across 1080 is a 270px slot, which cannot hold a
    wrapped label at phone-readable size.

    **The feedback arrow (`loop=True`) is its own gesture.** It stands well
    clear of the boxes — a wide return channel, not a line hugging the row —
    is drawn heavier than the forward connectors, and takes its time: it draws
    across the closing sentence that describes the mechanism turning back on
    itself, not in a snap after the last box. The first version ran a thin
    line ~90px under the row with square corners and it read as a stray
    underline rather than as "and round it goes again".

    payload: (nodes, title, loop)
      nodes  [(label, note | None, emoji | None) | (label, note) | label, ...]
      title  the beat's kicker
      loop   draw the feedback arrow from the last node back to the first
    """

    EMBLEM = False
    FLOW_W = 5                  # forward connector stroke
    LOOP_W = 7                  # the feedback arrow, drawn heavier
    LOOP_DROP = 150             # px the return channel stands off the row
    LOOP_CAP = 2.4             # the feedback arrow never crawls longer

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
               p: float, w: int | None = None,
               colour: tuple | None = None) -> None:
        """A connector that draws from `a` to `b`, head last."""
        if p <= 0:
            return
        col = colour or self.brand.primary
        partial(d, [a, b], p, col, w or self.FLOW_W)
        # The head only lands once the shaft has arrived, so the arrow reads
        # as travelling rather than as a shape fading up.
        if p >= 0.999:
            self._head(d, a, b, col)

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
            from ...core.vertical import emoji_image
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

        # A loop needs a clear return channel. In portrait it runs down the
        # left, so the boxes give it room by insetting from that edge rather
        # than the line hugging them — the "too close to the boxes" note.
        loop_inset = 108 if (self.loop and self.portrait) else 0

        if self.portrait:
            bw = fr.w - 2 * self.margin - loop_inset
            bx0 = self.margin + loop_inset
            laid, bh = self._measure(d, bw, label_font, note_font)
            # **The gap is what fills a 9:16 frame, not the boxes.** At a
            # fixed 108 a three-node chain ended around 1300 of 1920 and left
            # the bottom third of the frame empty — and a drawn beat burns no
            # caption there, so nothing else was ever going to fill it.
            # Boxes stay the size their content needs; the space between them
            # takes up the slack, within limits, so two chains of different
            # lengths still look like the same graphic.
            room = fr.h - top0 - 120 - (self.LOOP_DROP if self.loop else 0)
            gap = int(max(104, min(220, (room - n * bh) / max(1, n - 1))))
            block = n * bh + (n - 1) * gap
            top = max(top0, (fr.h - block) // 2)
            boxes = [(bx0, top + i * (bh + gap),
                      bx0 + bw, top + i * (bh + gap) + bh)
                     for i in range(n)]
            ends = [((bx0 + bw // 2, b[3]),
                     (bx0 + bw // 2, b[3] + gap)) for b in boxes[:-1]]
        else:
            usable = fr.w - 2 * self.margin
            gap = 96
            bw = int((usable - (n - 1) * gap) / n)
            laid, bh = self._measure(d, bw, label_font, note_font)
            if self.loop:
                # Centre the whole gesture — row plus return channel — in the
                # band under the title, not just the row.
                lo, hi = top0 + 20, fr.h - 56
                group = bh + self.LOOP_DROP + 30
                top = lo + max(0, (hi - lo - group) // 2)
            else:
                top = max(top0 + 20, (fr.h - bh) // 2)
            boxes = [(self.margin + i * (bw + gap), top,
                      self.margin + i * (bw + gap) + bw, top + bh)
                     for i in range(n)]
            ends = [((b[2], top + bh // 2), (b[2] + gap, top + bh // 2))
                    for b in boxes[:-1]]

        # The forward connectors — drawn slowly against the voice (`span_p`),
        # so each line is still travelling while its bridging phrase is spoken
        # and arrives as the next box lands. Drawn before the box it points at,
        # so the opaque box covers the head where it meets it.
        for i in range(n):
            e = self.due(i, n, f)
            if i > 0:
                p = self.span_p(i - 1, f, cap=self.LOOP_CAP)
                if p > 0:
                    self._arrow(d, ends[i - 1][0], ends[i - 1][1], p)
            if e >= 0:
                self._box(out, d, boxes[i], laid[i], e, label_font, note_font)

        # The feedback arrow: it starts once the last box is essentially up
        # and draws across the closing sentence, heavier and well clear of the
        # row. `LOOP_CAP` keeps it from crawling if that sentence is long.
        if self.loop and n > 1 and self.due(n - 1, n, f) >= 0.55:
            rv = self.reveals or []
            last = rv[n - 1] if len(rv) >= n else self.start
            t0 = last + 0.30
            dur = min(self.LOOP_CAP,
                      max(0.9, (self.start + self.hold) - t0 - 0.20))
            p = _smooth((self.at(f) - t0) / dur) if self.at(f) >= t0 else 0.0
            if p > 0:
                col = self.brand.primary + (235,)
                if self.portrait:
                    rx = self.margin + 30
                    sy = (boxes[-1][1] + boxes[-1][3]) // 2
                    ty = (boxes[0][1] + boxes[0][3]) // 2
                    pts = [(boxes[-1][0], sy), (rx, sy),
                           (rx, ty), (boxes[0][0], ty)]
                else:
                    y = boxes[0][3] + self.LOOP_DROP
                    sx = (boxes[-1][0] + boxes[-1][2]) // 2
                    dx = (boxes[0][0] + boxes[0][2]) // 2
                    pts = [(sx, boxes[-1][3]), (sx, y),
                           (dx, y), (dx, boxes[0][3])]
                pts = _round_corners(pts, 40)
                partial(d, pts, p, col, self.LOOP_W)
                if p >= 0.999:
                    self._head(d, pts[-2], pts[-1], col)


class Map(Beat):
    """Pins dropping onto a plate. For *where*, and for how spread out.

    The repo already owns `assets/pins` and a pin animation source, and long
    form has never used either. Both channels have a geography: crypto's is
    regulation and exchange domicile, tinnitus' is prevalence and where care
    is available. A list of country names cannot show clustering; a plate can.

    **It is a schematic, not a map.** No coastlines, no borders, no
    projection - an accurate world map at 1920 is either unreadable or a
    licensing question, and neither is worth it for a beat whose job is to say
    "these three are in Europe and this one is not". Positions are given as
    fractions of the plate, so the script places them by eye.

    Pins drop with a bounce and cast a ring, which is what makes several of
    them read as a sequence rather than as a scatter that was always there.

    payload: (pins, title) where pins is [(label, x, y), ...] with x, y in 0..1
    """

    EMBLEM = False

    def __init__(self, pins: list, title: str = "", **kw):
        super().__init__(**kw)
        self.pins = [(str(l), float(x), float(y)) for l, x, y in pins]
        self.title = title

    def _plate(self, out: Image.Image, box: tuple, e: float) -> None:
        """The graticule. Drawn, not photographed - see the class docstring."""
        x0, y0, x1, y1 = box
        d = ImageDraw.Draw(out, "RGBA")
        d.rectangle([x0, y0, x1, y1], outline=self.brand.primary + (70,),
                    width=3)
        cols, rows = 12, 7
        for i in range(1, cols):
            gx = x0 + (x1 - x0) * i / cols
            d.line([(gx, y0), (gx, y0 + (y1 - y0) * e)],
                   fill=self.brand.primary + (26,), width=1)
        for j in range(1, rows):
            gy = y0 + (y1 - y0) * j / rows
            d.line([(x0, gy), (x0 + (x1 - x0) * e, gy)],
                   fill=self.brand.primary + (26,), width=1)

    def content(self, out: Image.Image, f: float) -> None:
        fr, br = self.frame, self.brand
        top = self.heading(out, self.title, f)
        x0, x1 = self.margin, fr.w - self.margin
        y0 = top + 20
        y1 = fr.h - int(fr.h * 0.10)
        self._plate(out, (x0, y0, x1, y1), self.open_p(f, 0.8))

        d = ImageDraw.Draw(out, "RGBA")
        label_font = _font(36)
        for i, (label, fx, fy) in enumerate(self.pins):
            p = self.due(i, len(self.pins), f)
            if p < 0:
                continue
            e = ease_out(min(1.0, p))
            a = int(255 * min(1.0, p))
            px = x0 + (x1 - x0) * fx
            py = y0 + (y1 - y0) * fy

            # The drop: the pin falls the last 90px into place.
            fall = (1.0 - e) * 90
            # A settle, not a bounce - it overshoots *below* the resting
            # point late in the drop and eases back up. `sin(p * pi)` was
            # wrong twice over: it peaks mid-flight, so the pin rose while it
            # was still falling, and it returns to zero at p=1, so there was
            # no settle at the end at all.
            settle = 0.0
            if p > 0.62:
                q = (min(1.0, p) - 0.62) / 0.38
                settle = -math.sin(q * math.pi) * 7 * (1.0 - q)

            # **`py` is the pin's point, and everything is measured up from
            # it.** The first render drew the teardrop from `py` downward, so
            # the tip landed 34px *below* the position it was marking and the
            # pin sat outside the ring it cast. The tip is the whole reason
            # this shape is a pin rather than a dot, so it is the anchor: the
            # triangle's apex is at `py`, the body stacks above it, and the
            # ring is concentric with the apex.
            tip = py - fall - settle
            r = 20
            base = tip - 30                # where the triangle meets the disc
            cy = base - 14                 # the disc's own centre

            # The ring it casts, centred on the point and expanding past the
            # landing. This is the whole reason a sequence of pins reads as a
            # sequence rather than as a scatter that was always there - and it
            # is drawn before the pin so the pin is never behind it.
            if p > 0.3:
                q = min(1.0, (p - 0.3) / 0.9)
                rr = 18 + 104 * q
                # Flattened, because the plate is read as a surface seen at an
                # angle and a circular ring on it reads as a halo.
                d.ellipse([px - rr, py - rr * 0.4, px + rr, py + rr * 0.4],
                          outline=br.primary + (int(120 * (1 - q)),), width=3)

            # The pin: a disc over a triangle, so it has a point that actually
            # indicates a position.
            d.polygon([(px, tip), (px - 15, base), (px + 15, base)],
                      fill=br.primary + (a,))
            d.ellipse([px - r, cy - r, px + r, cy + r], fill=br.primary + (a,))
            # The hole, concentric with the disc rather than offset down it.
            d.ellipse([px - 8, cy - 8, px + 8, cy + 8], fill=br.bg + (a,))

            # Below the point, clear of both the pin and the ring's near edge.
            d.text((px, py + 30), label, font=label_font,
                   fill=br.ink + (a,), anchor="ma")


class Anatomy(Beat):
    """Callouts onto a drawing, fired one per spoken clause.

    The tinnitus channel's subject is a **part of a thing** - the cochlea, the
    auditory nerve, the jaw joint - and it has been carrying that on stock
    photographs of people looking uncomfortable, which show none of it. The
    existing `callout` beat annotates a photograph; this differs in that the
    subject is *drawn*, so there is something worth pointing at.

    The drawing is a caller-supplied image with a dark ground (`picture=`),
    or, with none, the schematic ear this class draws itself - pinna, canal,
    eardrum, ossicles, cochlea and auditory nerve, each a distinct shape in
    the right place relative to the others, assembling in the order sound
    travels. It is deliberately a diagram and not an illustration: flat line
    work in the brand accent, no shading, no tissue.

    **Use `LANDMARKS` for the fallback's coordinates** rather than measuring
    them off a screenshot - `Anatomy.LANDMARKS["cochlea"]` is where the coil
    actually is. With a `picture=`, the fractions are of that image instead.

    **The picture is drawn by this beat, into its own centred box** - which
    is what the paragraph above always claimed and what the code did not do.
    `Beat.draw` paints `picture=` into the split layout's *right column*
    (`PIC_X`), so a caller who supplied one got the photograph over on the
    right and four leader lines pointing into empty space in the middle. The
    fix is the same one `callout` already makes for the same collision: take
    the keyword before the base sees it, and lay the panel out here.
    Fitted, never cover-cropped - a crop slides the subject out from under
    coordinates that were read off the source.

    Each callout is a leader line that *travels* from the part to its label,
    on the span of the clause naming it. A label that appears with its line
    already drawn is the thing the whole library's second rule exists to stop.

    payload: (parts, title) where parts is [(label, x, y, side), ...],
    x/y fractions of **the picture** (or of the drawing box, with none) and
    side "l"/"r".
    """

    EMBLEM = False
    DIM = 0.62                  # the panel sits under the type, not beside it
    BOX_W = 0.52                # fraction of frame width, against 0.34 drawn

    def __init__(self, parts: list, title: str = "", **kw):
        # Same collision `callout` records: `make_beat` hands `picture=` to
        # every beat for the split layout, and this beat needs it centred.
        src = kw.pop("picture", None)
        super().__init__(**kw)
        self.parts = [(str(l), float(x), float(y), s) for l, x, y, s in parts]
        self.title = title
        self.panel = None
        if src is not None and Path(src).exists():
            im = Image.open(src).convert("RGB")
            fr = self.frame
            box_w = int(fr.w * self.BOX_W)
            box_h = fr.h - (self.head_y + 126) - 120
            k = min(box_w / im.width, box_h / im.height, fr.max_upscale)
            self.pw, self.ph = int(im.width * k), int(im.height * k)
            self.panel = (np.asarray(im.resize((self.pw, self.ph),
                                               Image.LANCZOS))
                          * self.DIM).astype(np.uint8)

    # The fallback drawing's own coordinate system: fractions of the box, so
    # the parts a script points at line up with what is drawn. **These are the
    # x/y a `parts` entry should use when no `picture=` is supplied** - they
    # are listed here rather than left to be measured off a screenshot.
    # The fallback drawing's own coordinate system: fractions of the box, so
    # the parts a script points at line up with what is drawn. **These are the
    # x/y a `parts` entry should use when no `picture=` is supplied.**
    LANDMARKS = {
        "pinna": (0.09, 0.40),
        "canal": (0.25, 0.50),
        "eardrum": (0.40, 0.52),
        "ossicles": (0.50, 0.36),
        "cochlea": (0.70, 0.64),
        "nerve": (0.89, 0.76),
    }

    @staticmethod
    def _bez(pts: list, n: int = 48) -> list:
        """Sample a cubic Bezier. Four control points in, a polyline out.

        `partial` travels polylines, so every curve in the drawing has to be
        one - and an ear is all curves. Chained end to end these give a
        continuous outline the reveal clock can draw on.
        """
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pts
        out = []
        for i in range(n + 1):
            t = i / n
            u = 1 - t
            out.append((u * u * u * x0 + 3 * u * u * t * x1
                        + 3 * u * t * t * x2 + t * t * t * x3,
                        u * u * u * y0 + 3 * u * u * t * y1
                        + 3 * u * t * t * y2 + t * t * t * y3))
        return out

    def _schematic(self, out: Image.Image, box: tuple, e: float) -> None:
        """A line drawing of an ear, in the order sound travels through it.

        **Three versions were rejected before this one**, and the notes on
        them are the whole design rationale:

        1. Three concentric arcs and a spiral. Read as an abstract spiral.
        2. A canal and an ossicle chain added, but a plain arc for the outer
           ear. Still "confusing" - because the arc was not an ear.
        3. A proper pinna, plus the semicircular canals for context. The
           canals read as a plant growing out of the picture and collided
           with the stirrup.

        Two lessons, both worth keeping. **The pinna is the recognition cue**:
        a viewer who sees an ear shape reads everything downstream of it as
        ear anatomy, and a viewer who does not is looking at abstract geometry
        however correct the rest is. And **anything a script never points at
        is a liability** - the semicircular canals and the tragus were both
        drawn, both anatomically right, and both cut for reading as noise.

        What is left is one continuous chain: pinna, canal, eardrum, ossicles,
        oval window, cochlea, nerve - exactly the parts a tinnitus script
        names, and nothing else. Everything travels on `e` in anatomical
        order, so the drawing builds the way the narration walks it, and line
        weight carries the hierarchy: the parts pointed at are heavier than
        the scaffolding.
        """
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        d = ImageDraw.Draw(out, "RGBA")
        col = self.brand.primary

        def P(fx, fy):
            return (x0 + w * fx, y0 + h * fy)

        def curve(*fracs, n=48):
            return self._bez([P(*f) for f in fracs], n)

        def phase(a, b):
            return max(0.0, min(1.0, (e - a) / (b - a)))

        # --- 1. the pinna -------------------------------------------------
        # **A C opening toward the head, not a closed oval and not a hook.**
        # The canal runs right, into the skull, so the flap's rim is on the
        # left and its opening faces right - that is the view every textbook
        # cross-section uses. The first attempt at this curled the rim back on
        # itself at the lobe and read as a question mark.
        #
        # Three strokes do the whole job: the outer rim from the top round to
        # the lobe, an inner ridge parallel to it, and the little flap at the
        # opening. Any more detail is lost at this size.
        p1 = phase(0.0, 0.30)
        helix = (curve((0.168, 0.212), (0.098, 0.192), (0.040, 0.272), (0.038, 0.382))
                 + curve((0.036, 0.482), (0.056, 0.592), (0.104, 0.648), (0.104, 0.648))
                 + curve((0.104, 0.648), (0.136, 0.692), (0.168, 0.662), (0.170, 0.606)))
        partial(d, helix, p1, col + (230,), 7)

        # The antihelix: an inner ridge echoing the rim. This is the single
        # line that stops the pinna reading as a plain crescent.
        p1b = phase(0.10, 0.34)
        anti = (curve((0.152, 0.298), (0.100, 0.312), (0.078, 0.398), (0.086, 0.470))
                + curve((0.086, 0.470), (0.094, 0.540), (0.126, 0.576), (0.156, 0.574)))
        partial(d, anti, p1b, col + (145,), 5)

        # **No tragus.** It was drawn, it is correct, and at this size it read
        # as a stray mark floating between the flap and the canal - the third
        # element cut for reading as noise rather than as anatomy. The concha
        # is instead shown by the canal walls running back to meet the ridge,
        # which is the same information and one fewer disconnected stroke.

        # --- 2. the canal ---------------------------------------------------
        # A tube, not a line: two walls converging slightly toward the drum.
        p2 = phase(0.26, 0.48)
        partial(d, curve((0.108, 0.412), (0.210, 0.428), (0.310, 0.450),
                         (0.392, 0.468)), p2, col + (190,), 6)
        partial(d, curve((0.104, 0.548), (0.210, 0.550), (0.310, 0.556),
                         (0.392, 0.570)), p2, col + (190,), 6)

        # --- 3. the eardrum --------------------------------------------------
        # The membrane closing the canal, set at its real oblique angle.
        p3 = phase(0.42, 0.58)
        partial(d, [P(0.392, 0.462), P(0.400, 0.578)], p3, col + (245,), 8)

        # --- 4. the ossicles --------------------------------------------------
        # Hammer, anvil, stirrup. Drawn as a jointed chain with a stirrup ring
        # at the far end - the ring is what makes it read as three linked
        # bones rather than as a zigzag.
        p4 = phase(0.52, 0.72)
        chain = [P(0.405, 0.470), P(0.452, 0.380), P(0.508, 0.352),
                 P(0.545, 0.412)]
        partial(d, chain, p4, col + (215,), 6)
        for i, pt in enumerate(chain[1:3]):
            q = max(0.0, min(1.0, p4 * 2.4 - i * 0.7))
            if q <= 0:
                continue
            r = 8 * ease_out(q)
            d.ellipse([pt[0] - r, pt[1] - r, pt[0] + r, pt[1] + r],
                      fill=col + (int(230 * q),))
        if p4 > 0.8:
            q = (p4 - 0.8) / 0.2
            cx, cy = P(0.556, 0.432)
            rx, ry = w * 0.016, h * 0.026
            d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry],
                      outline=col + (int(215 * q),), width=5)

        # **The semicircular canals are deliberately not drawn.** Two versions
        # of them were tried, on the theory that three loops make a viewer
        # read the right-hand side as an inner ear. Both read as a plant
        # growing out of the picture, and the second collided with the
        # stirrup. They are balance organs, no tinnitus script points at one,
        # and the beat's whole job is that a viewer knows which part is meant
        # - so they were costing the thing they were supposed to buy. Left
        # out, the drawing is a single chain from the pinna to the nerve,
        # which is exactly what the narration walks.

        # --- 6. the cochlea ----------------------------------------------------
        # A snail, wound outward from the apex, so it reads as a shell with a
        # mouth rather than as a flat spiral. The tube thickens as it unwinds,
        # which is both true and what sells the shape.
        # The oval window: the short link from the stirrup into the coil. It
        # is two pixels of drawing and it is what turns a chain that stops in
        # mid-air into one continuous path from the pinna to the nerve.
        p6a = phase(0.66, 0.78)
        partial(d, [P(0.570, 0.444), P(0.596, 0.492)], p6a, col + (200,), 5)

        p6 = phase(0.72, 0.94)
        ccx, ccy = P(0.715, 0.620)
        rr = min(w, h) * 0.175
        coil, weights = [], []
        for i in range(240):
            q = i / 239
            ang = math.pi * 0.55 + q * 2.65 * 2 * math.pi
            r = rr * (0.16 + 0.84 * q)
            coil.append((ccx + r * math.cos(ang), ccy + r * math.sin(ang) * 0.96))
            weights.append(3 + 5 * q)
        # Drawn in graded segments rather than one `partial`, so the tube can
        # thicken; each segment is its own travelled polyline.
        n = max(2, int(len(coil) * p6))
        step = 12
        for i in range(0, n - 1, step):
            seg = coil[i:min(n, i + step + 1)]
            if len(seg) > 1:
                d.line(seg, fill=col + (235,), width=int(weights[i]),
                       joint="curve")

        # --- 7. the auditory nerve ----------------------------------------------
        # Leaving the coil's base for the brain, as a bundle of strands.
        p7 = phase(0.86, 1.0)
        for off, a in ((0.000, 185), (0.030, 135), (0.060, 95)):
            partial(d, curve((0.782, 0.700 + off), (0.838, 0.744 + off),
                             (0.898, 0.774 + off), (0.975, 0.786 + off), n=24),
                    p7, col + (a,), 5)

    ROW = 62                    # the least vertical space two labels need

    def _label_rows(self, box: tuple) -> list[float]:
        """A y for every label, spread so no two on the same side collide.

        Each label wants to sit at its own part's height and most of them can.
        Where two on one side are closer than `ROW`, they are pushed apart
        around their midpoint - in part order, so the pair still reads top to
        bottom the way the narration names them.

        This is the same bug the map pin had, one level up: a thing drawn at
        the coordinate it refers to, without asking what else is already
        there. Anatomy makes it certain rather than likely, because the parts
        of an ear genuinely are stacked within a few percent of each other.
        """
        y0, h = box[1], box[3] - box[1]
        rows = [y0 + h * fy for _, _, fy, _ in self.parts]

        for side in ("l", "r"):
            idx = [i for i, pt in enumerate(self.parts) if pt[3] == side]
            # Solve in screen order, not part order: pushing the *upper* label
            # up is only correct if it is actually the upper one.
            idx.sort(key=lambda i: rows[i])
            for a_i, b_i in zip(idx, idx[1:]):
                gap = rows[b_i] - rows[a_i]
                if gap >= self.ROW:
                    continue
                push = (self.ROW - gap) / 2
                rows[a_i] -= push
                rows[b_i] += push
            # Keep the whole column inside the box even after pushing.
            if idx:
                lo, hi = min(rows[i] for i in idx), max(rows[i] for i in idx)
                if lo < y0:
                    for i in idx:
                        rows[i] += y0 - lo
                elif hi > box[3]:
                    for i in idx:
                        rows[i] -= hi - box[3]
        return rows

    def content(self, out: Image.Image, f: float) -> None:
        fr, br = self.frame, self.brand
        top = self.heading(out, self.title, f)

        # The drawing sits centred, with the callout labels in the margins
        # either side - which is the silhouette this beat is for. Nothing in
        # the library puts its subject in the middle.
        if self.panel is not None:
            # The coordinate space is the photograph itself, not the box it
            # sits in: the fractions were read off the source file.
            px0 = (fr.w - self.pw) // 2
            py0 = top + 30 + max(0, (fr.h - 120 - (top + 30) - self.ph) // 2)
            out.paste(Image.fromarray(self.panel), (px0, py0))
            box = (px0, py0, px0 + self.pw, py0 + self.ph)
            d0 = ImageDraw.Draw(out, "RGBA")
            d0.rectangle([box[0], box[1], box[2] - 1, box[3] - 1],
                         outline=br.primary + (110,), width=2)
        else:
            bw = int(fr.w * 0.42)
            box = ((fr.w - bw) // 2, top + 30, (fr.w + bw) // 2, fr.h - 120)
            self._schematic(out, box, self.open_p(f, 1.2))

        d = ImageDraw.Draw(out, "RGBA")
        label_font = _font(38)
        label_y = self._label_rows(box)
        for i, (label, fx, fy, side) in enumerate(self.parts):
            p = self.due(i, len(self.parts), f)
            if p < 0:
                continue
            a = int(255 * min(1.0, p))
            px = box[0] + (box[2] - box[0]) * fx
            py = box[1] + (box[3] - box[1]) * fy
            ly = label_y[i]

            # The leader travels on the clause's own span, elbowed rather than
            # diagonal: a right-angled leader reads as an annotation, a
            # diagonal one reads as an arrow pointing somewhere.
            #
            # **The elbow steps to the label's row, which is not always the
            # part's own height.** The eardrum sits 4% of the box below the
            # canal it closes - anatomically correct and, at 38px type, two
            # labels overlapping each other. `_label_rows` spreads them; the
            # leader's dog-leg is what keeps each one attached to the right
            # part while it does.
            out_x = self.margin + 300 if side == "l" else fr.w - self.margin - 300
            knee = out_x + (90 if side == "l" else -90)
            travel = self.span_p(i, f, cap=1.4)
            partial(d, [(px, py), (knee, py), (knee, ly), (out_x, ly)], travel,
                    br.primary + (a,), 3)

            d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=br.primary + (a,))
            if travel > 0.86:
                la = int(a * min(1.0, (travel - 0.86) / 0.14))
                anchor = "rs" if side == "l" else "ls"
                dx = -16 if side == "l" else 16
                d.text((out_x + dx, ly + 12), label, font=label_font,
                       fill=br.ink + (la,), anchor=anchor)


