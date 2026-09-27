"""Beats that span the full frame instead of a column.

A set of cards, a lineup of brand tiles, a numbered track, and a whole
divided into its parts. What they have in common is that the layout needs
the width - a `grid` squeezed into the left column is a list, and a `split`
without room either side is not a division of anything."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from ...core.draw import cover, ease_out, mark, partial, shadow_text, wrap
from .base import RISE, Beat, _display, _font

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
                from ...core.vertical import emoji_image
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
            from ...core.vertical import emoji_image
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
        # the horizontal version and the comparison's divider use, on the same
        # `open_p` clock so the scaffolding glides at the rate its nodes do.
        e = self.open_p(f, 1.1)
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

        # The track first, drawn across as the beat opens, on `open_p` so it
        # glides at the same rate as the nodes that populate it.
        e = self.open_p(f, 1.1)
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


class Split(Beat):
    """One whole thing, divided into many equal claims on it.

    **Built for real-world asset tokenization (2026-09-18), because the library
    could not draw its central noun.** "A twelve-million-dollar building split
    into a hundred and twenty thousand tokens" is a *division*, and nothing
    else here shows one: `bars` shows proportions of a whole but never the
    whole being cut, `grid` is a set of different things, and a stock clip of
    a tower says "building" and nothing about who owns it. Reusable for any
    fractional claim - shares of a fund, a supply divided among holders, a
    royalty stream split by stake.

    Two reveals, in this order:

    0. **The whole.** A block outline draws round its perimeter against the
       voice and fills dimly, with its name and value inside. "One building,
       worth twelve million dollars."
    1. **The split.** Grid lines draw across the block, then every cell lights
       a small coin in a diagonal wave, and the part's label sets under it.
       "Split into a hundred and twenty thousand tokens, a hundred dollars
       each."

    **The cell count is a picture, not the figure.** 160 cells stand in for
    120,000; the real numbers are in the labels. Drawing the true count would
    be a grey haze, which is the opposite of "many equal pieces".

    Vector layer supersampled like `Dial` - the coins are small circles and
    PIL does not antialias them.

    payload: (whole, whole_note, part, part_note, title)
    """

    EMBLEM = False
    SS = 2

    def __init__(self, whole: str, whole_note: str = "", part: str = "",
                 part_note: str = "", title: str = "", **kw):
        super().__init__(**kw)
        self.whole, self.whole_note = whole, whole_note
        self.part, self.part_note = part, part_note
        self.title = title

        # **Raise on a name too wide for the frame**, the same guard `Bars`
        # carries for an over-long value. `whole` and `part` are set in the
        # display face at 80px (portrait) / 72px and are drawn *centred with
        # no wrap and no fit*, so an over-long one runs off both edges of the
        # frame - unclipped, unraised and invisible until the render is
        # looked at. "MILLIONS OF CUSTOMERS" measures 1176px against a 1080px
        # portrait frame and shipped into a cut that way (crypto-whale,
        # 2026-09-24); the shipped payloads that work are 14-15 characters.
        # Checked here rather than at draw time so the script fails in a
        # second instead of twelve minutes into a render.
        from PIL import Image as _Im, ImageDraw as _Dr
        d = _Dr.Draw(_Im.new("RGB", (10, 10)))
        for label, name in ((self.whole, "whole"), (self.part, "part")):
            if not label:
                continue
            f = _display(80 if self.frame.h > self.frame.w else 72)
            w = d.textlength(label, font=f)
            if w > self.frame.w - 2 * 40:
                raise ValueError(
                    f"split {name}={label!r} is {w:.0f}px wide and the frame "
                    f"is {self.frame.w}px - it will draw off both edges. "
                    f"Shorten it to about 15 characters.")

    def _geom(self) -> tuple[int, int, int, int, int, int]:
        """x, y, w, h of the block, and its cols, rows."""
        fr = self.frame
        if self.portrait:
            w, h = 860, 860
            return (fr.w - w) // 2, 560, w, h, 11, 11
        w, h = 1080, 450
        return (fr.w - w) // 2, 400, w, h, 20, 8

    def content(self, out: Image.Image, f: float) -> None:
        d = ImageDraw.Draw(out, "RGBA")
        self.heading(out, self.title, f)
        x, y, w, h, cols, rows = self._geom()
        prim = self.brand.primary

        e0 = self.due(0, 2, f)
        if e0 < 0:
            return
        outline = self.span_p(0, f, lead=0.05, cap=1.4)
        e1 = self.due(1, 2, f)
        lines = self.span_p(1, f, lead=0.05, cap=1.2) if e1 >= 0 else 0.0
        # The coin wave starts as the grid finishes and runs its own clock:
        # it is a consequence of the split, not a thing the voice names.
        wave = 0.0
        if e1 >= 0 and self.reveals and len(self.reveals) > 1:
            wave = max(0.0, (self.at(f) - self.reveals[1] - 0.9) / 1.3)

        S = self.SS
        layer = Image.new("RGBA", ((w + 20) * S, (h + 20) * S), (0, 0, 0, 0))
        v = ImageDraw.Draw(layer)
        o = 10 * S
        W, H = w * S, h * S

        # The fill arrives with the outline, dim, so the whole reads as one
        # object before it is cut.
        v.rectangle([o, o, o + W, o + H],
                    fill=prim + (int(38 * min(1.0, outline * 1.4)),))
        # Perimeter, drawn as one travelling line from the top-left corner.
        per = [(o, o), (o + W, o), (o + W, o + H), (o, o + H), (o, o)]
        partial(v, per, outline, prim + (255,), 5 * S)

        if lines > 0:
            # Verticals sweep down, horizontals sweep across, both on one clock.
            for c in range(1, cols):
                cx = o + W * c / cols
                v.line([(cx, o), (cx, o + H * lines)],
                       fill=prim + (150,), width=2 * S)
            for r in range(1, rows):
                cy = o + H * r / rows
                v.line([(o, cy), (o + W * lines, cy)],
                       fill=prim + (150,), width=2 * S)

        if wave > 0:
            cw, ch = W / cols, H / rows
            rad = min(cw, ch) * 0.28
            span = cols + rows - 2
            for r in range(rows):
                for c in range(cols):
                    k = min(1.0, max(0.0, wave * 1.6 - 0.6 * (c + r) / span))
                    if k <= 0:
                        continue
                    cx, cy = o + cw * (c + 0.5), o + ch * (r + 0.5)
                    rr = rad * (0.6 + 0.4 * ease_out(k))
                    v.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                              fill=prim + (int(230 * k),))

        layer = layer.resize((w + 20, h + 20), Image.LANCZOS)
        out.paste(layer, (x - 10, y - 10), layer)

        # --- type -----------------------------------------------------------
        # The whole's name sits centred inside the block until the coins
        # reach the middle, then leaves - the object has become its parts.
        name_f = _display(96 if self.portrait else 88)
        note_f = _font(48 if self.portrait else 44)
        fade = 1.0 - min(1.0, wave * 1.8)
        a = int(255 * min(1.0, e0) * fade)
        if a > 0:
            bb = d.textbbox((0, 0), self.whole, font=name_f)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            nb = d.textbbox((0, 0), self.whole_note, font=note_f)
            block = th + (28 + nb[3] - nb[1] if self.whole_note else 0)
            ty = y + (h - block) // 2 - bb[1]
            shadow_text(d, (x + (w - tw) // 2, ty), self.whole, name_f,
                        self.brand.ink + (a,), alpha=a)
            if self.whole_note:
                shadow_text(d, (x + (w - (nb[2] - nb[0])) // 2,
                                ty + bb[3] + 28 - nb[1]),
                            self.whole_note, note_f, prim + (a,), alpha=a)

        # After the wave, the whole's name moves above the block in small
        # type so the figure it was worth stays on screen beside the parts.
        if wave > 0.4 and self.whole_note:
            k = min(1.0, (wave - 0.4) * 2.0)
            small = f"{self.whole}  ·  {self.whole_note}"
            sb = d.textbbox((0, 0), small, font=note_f)
            shadow_text(d, (x + (w - (sb[2] - sb[0])) // 2,
                            y - 36 - (sb[3] - sb[1]) + int(RISE * (1 - k))),
                        small, note_f, self.brand.ink + (int(220 * k),),
                        alpha=int(255 * k))

        if wave > 0.5 and self.part:
            k = min(1.0, (wave - 0.5) * 2.0)
            part_f = _display(80 if self.portrait else 72)
            pb = d.textbbox((0, 0), self.part, font=part_f)
            py = y + h + 40 + int(RISE * (1 - k))
            shadow_text(d, (x + (w - (pb[2] - pb[0])) // 2, py - pb[1]),
                        self.part, part_f, prim + (int(255 * k),),
                        alpha=int(255 * k))
            if self.part_note:
                qb = d.textbbox((0, 0), self.part_note, font=note_f)
                shadow_text(d, (x + (w - (qb[2] - qb[0])) // 2,
                                py + (pb[3] - pb[1]) + 22 - qb[1]),
                            self.part_note, note_f,
                            self.brand.ink + (int(230 * k),),
                            alpha=int(255 * k))


