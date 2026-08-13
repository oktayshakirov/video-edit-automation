"""The thumbnail, 1280x720.

For a Short the thumbnail barely exists — the feed autoplays and the first frame
is the hook. For long form it is the single highest-leverage artifact in the
pipeline: it and the title are the entire click decision, and a video nobody
clicks has no retention curve to improve.

So this is generated rather than grabbed from a frame. A frame grab is a picture
of the video; a thumbnail is an argument for watching it, and the two want
different type sizes by a factor of three.

Four rules, all of them about the fact that it is looked at small:

* **Three or four words in the headline, set enormous.** The title beside it
  carries the detail. At feed size a thumbnail is roughly 360px wide and
  anything below ~90px of type here is unreadable there.
* **A second line, smaller, for the hook the headline cannot hold.** The
  headline names the subject; the subline is the reason to click.
* **The type must not need the image to be legible.** Heavy stroke plus a
  gradient scrim, because the same file is shown against both a white and a
  dark page, and over a photograph whose brightness nobody controls.
* **Type on one side, subject on the other.** A full-width band across the
  middle is the easy layout and it covers the subject — on the Satoshi image it
  landed exactly on the Bitcoin, which is the one object a viewer needs to see
  to know what the video is about. `zoom` and `focus` exist to move the subject
  clear of the type rather than the other way round.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from ..core.brand import Brand
from ..core.draw import wrap
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

W, H = 1280, 720                # what YouTube wants; also under the 2MB limit


def _place(image: Path, zoom: float, focus: tuple[float, float]) -> Image.Image:
    """Cover the frame at `zoom`, then choose which part of the slack to keep.

    `focus` is 0..1 on each axis over the headroom the zoom created: `(0, 0.84)`
    keeps the left edge and most of the bottom. This is how the subject is moved
    out from under the type — cropping the picture, not shrinking the words.
    """
    src = Image.open(image).convert("RGB")
    tw, th = int(W * zoom), int(H * zoom)
    s = max(tw / src.width, th / src.height)
    r = src.resize((max(1, int(src.width * s)), max(1, int(src.height * s))),
                   Image.LANCZOS)
    x = int((r.width - W) * min(max(focus[0], 0.0), 1.0))
    y = int((r.height - H) * min(max(focus[1], 0.0), 1.0))
    return r.crop((x, y, x + W, y + H))


def render_thumb(out: Path, brand: Brand, headline: str,
                 image: Path | None = None, kicker: str = "",
                 subline: str = "", size: int = 128, sub_size: int = 54,
                 logo_w: int = 230, zoom: float = 1.0,
                 focus: tuple[float, float] = (0.5, 0.5),
                 text_w: float = 0.56) -> Path:
    """One thumbnail: photograph, gradient scrim, headline, subline, mark.

    `headline` is the three or four words, set as large as they will go.
    `subline` is the smaller second line under it. `kicker` still works as a
    small line *above* the headline for a date or a source.

    `text_w` is the fraction of the width the type block occupies; the scrim
    fades out just past it, so whatever is on the other side stays visible.
    """
    if image is not None and Path(image).exists():
        base = _place(Path(image), zoom, focus)
        # A gentle blur and dim: the photograph's job is to say what the subject
        # is at a glance, not to be looked at.
        base = base.filter(ImageFilter.GaussianBlur(1.4))
        base = ImageEnhance.Brightness(base).enhance(0.78)
    else:
        base = Image.new("RGB", (W, H), brand.bg)

    # A horizontal gradient scrim rather than a band across the middle. Solid
    # under the type, gone by the time it reaches the subject.
    edge = int(W * (text_w + 0.10))
    scrim = Image.new("L", (W, 1))
    px = scrim.load()
    for x in range(W):
        p = min(1.0, max(0.0, x / max(edge, 1)))
        px[x, 0] = int(226 * (1.0 - p ** 1.7))
    mask = scrim.resize((W, H))
    base = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), base, mask)

    d = ImageDraw.Draw(base)
    margin = 62
    col = int(W * text_w) - margin

    font = ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)
    lines = wrap(d, headline.upper(), font, col)
    # Shrink to fit rather than overflow: a headline that runs off the edge is
    # worse than one a size smaller, and nobody checks before uploading.
    while len(lines) > 3 and size > 72:
        size -= 8
        font = ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)
        lines = wrap(d, headline.upper(), font, col)

    line_h = int(size * 1.06)
    sub_font = ImageFont.truetype(FONT_CAPTION, sub_size,
                                  index=FONT_CAPTION_INDEX)
    sub_lines = wrap(d, subline, sub_font, col) if subline else []
    sub_h = int(sub_size * 1.24)

    block = len(lines) * line_h + (len(sub_lines) * sub_h + 26 if sub_lines else 0)
    if kicker:
        block += 62
    y = (H - block) // 2 + 30

    if kicker:
        kf = ImageFont.truetype(FONT_CAPTION, 40, index=FONT_CAPTION_INDEX)
        d.text((margin, y), kicker.upper(), font=kf, fill=brand.primary,
               stroke_width=3, stroke_fill=(0, 0, 0))
        y += 62

    for ln in lines:
        d.text((margin, y), ln, font=font, fill=brand.ink,
               stroke_width=9, stroke_fill=(0, 0, 0))
        y += line_h

    if sub_lines:
        y += 26
        # A short rule between the two sizes, so the subline reads as attached
        # to the headline rather than as a stray caption.
        d.line([(margin, y - 14), (margin + 150, y - 14)],
               fill=brand.primary, width=5)
        for ln in sub_lines:
            d.text((margin, y), ln, font=sub_font, fill=brand.primary,
                   stroke_width=5, stroke_fill=(0, 0, 0))
            y += sub_h

    mark = brand.mark(logo_w)
    if mark is not None:
        top = 42
        room = max(1, (H - block) // 2 - 24)
        if mark.height > room:
            w = max(1, int(mark.width * room / mark.height))
            mark = mark.resize((w, room), Image.LANCZOS)
        base.paste(mark, (margin, top), mark)

    out.parent.mkdir(parents=True, exist_ok=True)
    base.save(out, quality=92)
    return out
