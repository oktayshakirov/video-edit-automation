"""The thumbnail, 1280x720.

For a Short the thumbnail barely exists — the feed autoplays and the first frame
is the hook. For long form it is the single highest-leverage artifact in the
pipeline: it and the title are the entire click decision, and a video nobody
clicks has no retention curve to improve.

So this is generated rather than grabbed from a frame. A frame grab is a picture
of the video; a thumbnail is an argument for watching it, and the two want
different type sizes by a factor of three.

**The subject is found, not assumed.** The previous version took a `zoom` and a
`focus` per video and the operator had to eyeball whether the type cleared the
face. That works until it does not, and it fails silently — the file looks fine
at full size and the face is behind a word at feed size. `subject_box` runs
OpenCV's face cascades, falls back to edge-energy saliency when there is no
face, and `_layout` then pans the picture so the subject sits wholly in one half
and puts the type in the other. The overlap is *checked*, and the type shrinks
until it clears.

Four rules, all about the fact that it is looked at small:

* **One accent phrase in a solid vibrant box.** Mark it in the headline with
  brackets: `"8 hours of sleep is a [lie]"`. Every reference thumbnail that
  works does this — the box is what the eye lands on first, and a headline with
  no focal word is a wall.
* **Three to six words.** The title beside it carries the detail. At feed size a
  thumbnail is ~360px wide and anything below ~90px of type is unreadable.
* **The type must not need the image to be legible.** Heavy stroke plus a
  gradient scrim, because the same file is shown against a white and a dark page
  and over a photograph whose brightness nobody controls.
* **No watermark.** The channel name is already under the thumbnail everywhere
  it appears, and a mark on the image is a tell of a template rather than a
  channel. Removed deliberately.
"""

from __future__ import annotations

import re
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

from ..core.brand import Brand
from ..core.draw import wrap
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

W, H = 1280, 720                # what YouTube wants; also under the 2MB limit

# Vibrant accents, deliberately **not** the brand palette. thecrypto.wiki's gold
# and tinnitushelp.me's peach are both low-contrast against their own dark
# imagery — fine inside a video where they read as the house colour, wrong on a
# thumbnail competing in a grid. These are the colours the reference thumbnails
# actually use.
ACCENTS = {
    "red": ((222, 32, 40), (255, 255, 255)),
    "yellow": ((255, 199, 0), (16, 16, 16)),
    "orange": ((255, 106, 0), (255, 255, 255)),
    "blue": ((26, 128, 226), (255, 255, 255)),
    "cyan": ((0, 176, 208), (255, 255, 255)),
}


def _energy(bgr: np.ndarray) -> np.ndarray:
    """A per-pixel map of "there is something here worth not covering".

    Edge energy, blurred wide. It answers the question that actually matters,
    which is **not** where the person is — it is where the picture is empty
    enough to take type. Chasing the person was the first two attempts and both
    failed for the same reason: a face cascade finds a head, and no multiple of
    a head reliably describes the arms, hair and torso that collide with words.
    """
    grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
    gx = cv2.Sobel(cv2.GaussianBlur(grey, (5, 5), 0), cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(cv2.GaussianBlur(grey, (5, 5), 0), cv2.CV_32F, 0, 1)
    e = cv2.blur(np.sqrt(gx * gx + gy * gy), (81, 81))
    return e / (e.max() or 1.0)


def face_boxes(bgr: np.ndarray) -> list[tuple[int, int, int, int]]:
    """Faces, which type must never cover whatever the energy map says.

    A face in shadow can be *low* energy — smooth skin against a dark ground —
    so the map alone will happily put a word across someone's eyes. This is the
    hard constraint on top of it.
    """
    grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    h, w = grey.shape
    out = []
    for name in ("haarcascade_frontalface_default.xml",
                 "haarcascade_profileface.xml"):
        c = cv2.CascadeClassifier(cv2.data.haarcascades + name)
        for (x, y, fw, fh) in c.detectMultiScale(
                grey, 1.1, 6, minSize=(int(w * 0.06), int(h * 0.06))):
            # Generous, because hair and chin sit outside the cascade's box.
            out.append((int(x - fw * 0.45), int(y - fh * 0.6),
                        int(fw * 1.9), int(fh * 2.2)))
    return out


def _layout(image: Path, col: float = 0.54, margin_px: int = 26
            ) -> tuple[Image.Image, str, float, bool]:
    """Place the picture so the type sits on the quietest part of it.

    Searches zoom x pan x side and scores each candidate by the mean content
    energy inside the type column, with a face anywhere in that column treated
    as disqualifying. Returns the crop, the side for the type, the achieved
    score, and whether it is clean enough to ship.
    """
    src = cv2.imread(str(image))
    sh, sw = src.shape[:2]
    energy = _energy(src)
    faces = face_boxes(src)
    col_w = int(W * col)

    best = None
    for zoom in [1.0 + i * 0.08 for i in range(9)]:          # 1.00 .. 1.64
        tw, th = int(W * zoom), int(H * zoom)
        sc = max(tw / sw, th / sh)
        nw = max(tw, int(np.ceil(sw * sc)))
        nh = max(th, int(np.ceil(sh * sc)))
        e_big = cv2.resize(energy, (nw, nh), interpolation=cv2.INTER_LINEAR)
        f_big = [(int(x * sc), int(y * sc), int(fw * sc), int(fh * sc))
                 for (x, y, fw, fh) in faces]
        y0 = int(np.clip(nh * 0.42 - H * 0.42, 0, nh - H))

        for side in ("left", "right"):
            lo = 58 if side == "left" else W - 58 - col_w
            hi = lo + col_w + margin_px
            for x0 in np.linspace(0, max(nw - W, 0), 9).astype(int):
                band = e_big[y0:y0 + H, x0 + max(lo - margin_px, 0):x0 + hi]
                # The other half, which is where the subject has to be. Scoring
                # only the type column drove the search toward near-empty frames
                # — technically clean, and a thumbnail with nothing in it. The
                # goal is contrast: quiet under the words, busy beside them.
                if side == "left":
                    other = e_big[y0:y0 + H, x0 + hi:x0 + W]
                else:
                    other = e_big[y0:y0 + H, x0:x0 + max(lo - margin_px, 1)]
                quiet = float(band.mean()) if band.size else 1.0
                busy = float(other.mean()) if other.size else 0.0
                score = quiet - 0.6 * busy
                for (fx, fy, fw, fh) in f_big:
                    if (fx - x0 < hi and fx + fw - x0 > lo
                            and fy - y0 < H and fy + fh - y0 > 0):
                        score += 1.0          # a face in the column is fatal
                cand = (score, zoom, sc, nw, nh, int(x0), y0, side)
                if best is None or score < best[0]:
                    best = cand

    score, zoom, sc, nw, nh, x0, y0, side = best
    big = cv2.resize(src, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    crop = big[y0:y0 + H, x0:x0 + W]
    img = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    # 0.20 of peak edge energy is about the level of a plain wall with soft
    # shading. Above it there is real detail under the words.
    # Negative means the subject side is meaningfully busier than the type
    # side, which is the composition this is after.
    return img, side, score, score < 0.0


def _split(headline: str) -> list[tuple[str, bool]]:
    """Split `"a [b] c"` into [(word, is_accent), ...]."""
    out = []
    for chunk in re.split(r"(\[[^\]]*\])", headline):
        if not chunk:
            continue
        hot = chunk.startswith("[") and chunk.endswith("]")
        for word in chunk.strip("[]").split():
            out.append((word, hot))
    return out


def render_thumb(out: Path, brand: Brand, headline: str,
                 image: Path | None = None, subline: str = "",
                 accent: str = "red", size: int = 118, sub_size: int = 46,
                 arrow_to: tuple[float, float] | None = None,
                 **_ignored) -> Path:
    """One thumbnail: photograph, scrim, headline with a boxed accent phrase.

    `headline` marks its accent with brackets — `"Nobody has [passed it]"`.
    `arrow_to` is a fractional point on the frame; when given, a hand-drawn
    style arrow curves from the type toward it. Use it only when there is
    something specific to point at.

    Extra keyword arguments are ignored, so the older `zoom`/`focus`/`kicker`
    call sites keep working while the layout is chosen automatically.
    """
    box = None
    if image is not None and Path(image).exists():
        base, side, score, clear = _layout(Path(image))
        if not clear:
            # Say so rather than ship it. A subject that cannot be moved
            # clear of the type at any zoom means the source is framed too
            # tight and centred for this layout — pick another picture.
            print(f'  thumb: busiest-case score {score:.2f} in '
                  f'{Path(image).name} — the type sits on real detail; '
                  f'consider a source with more empty space')
        base = base.filter(ImageFilter.GaussianBlur(1.2))
        # Dim toward a target rather than by a fixed factor. A flat 0.80 crushed
        # the already-dark portraits this now selects for into near-black.
        luma = np.asarray(base.convert("L")).mean()
        base = ImageEnhance.Brightness(base).enhance(
            float(np.clip(74.0 / max(luma, 1.0), 0.62, 1.12)))
    else:
        base, side = Image.new("RGB", (W, H), brand.bg), "left"

    # A scrim on the type's side only, fading out before the subject.
    grad = Image.new("L", (W, 1))
    px = grad.load()
    for x in range(W):
        p = x / (W - 1)
        p = p if side == "left" else 1.0 - p
        px[x, 0] = int(232 * max(0.0, 1.0 - (p / 0.66) ** 1.7))
    base = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)),
                           base, grad.resize((W, H)))

    d = ImageDraw.Draw(base)
    margin = 58
    col_w = int(W * 0.54)
    x_text = margin if side == "left" else W - margin - col_w

    fill, ink = ACCENTS.get(accent, ACCENTS["red"])
    words = _split(headline.upper())

    # Lay the words out, shrinking until they fit the column *and* clear the
    # subject. This is the check the old version left to the eye.
    for _ in range(14):
        font = ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)
        space = d.textlength(" ", font=font)
        lines, cur, cw = [], [], 0.0
        for word, hot in words:
            ww = d.textlength(word, font=font)
            if cur and cw + space + ww > col_w:
                lines.append(cur)
                cur, cw = [], 0.0
            cur.append((word, hot, ww))
            cw += ww + (space if len(cur) > 1 else 0)
        if cur:
            lines.append(cur)
        line_h = int(size * 1.10)
        block = len(lines) * line_h
        if len(lines) <= 4 and block < H - 2 * margin - (86 if subline else 0):
            break
        size -= 8

    sub_font = ImageFont.truetype(FONT_CAPTION, sub_size,
                                  index=FONT_CAPTION_INDEX)
    sub_lines = wrap(d, subline, sub_font, col_w) if subline else []
    sub_h = int(sub_size * 1.26)
    total = block + (len(sub_lines) * sub_h + 30 if sub_lines else 0)
    y = (H - total) // 2

    pad_x, pad_y = 14, 8
    for line in lines:
        # **One box per run of accent words, not one per word.** Boxing each
        # word separately leaves a gap of background between them — "PASSED IT"
        # came out as two plates with a seam down the middle, which reads as a
        # rendering fault rather than a highlight. Measure the run, draw one
        # rectangle, then set the words on top of it.
        x = x_text
        runs, start, width = [], None, 0.0
        for i, (word, hot, ww) in enumerate(line):
            if hot and start is None:
                start, width = x, ww
            elif hot:
                width = x + ww - start
            elif start is not None:
                runs.append((start, width))
                start = None
            x += ww + space
        if start is not None:
            runs.append((start, width))
        for rx, rw in runs:
            d.rectangle([rx - pad_x, y - pad_y + 6,
                         rx + rw + pad_x, y + line_h - pad_y], fill=fill)

        x = x_text
        for word, hot, ww in line:
            if hot:
                d.text((x, y), word, font=font, fill=ink)
            else:
                d.text((x, y), word, font=font, fill=(255, 255, 255),
                       stroke_width=8, stroke_fill=(0, 0, 0))
            x += ww + space
        y += line_h

    if sub_lines:
        y += 30
        for ln in sub_lines:
            d.text((x_text, y), ln, font=sub_font, fill=(255, 255, 255),
                   stroke_width=5, stroke_fill=(0, 0, 0))
            y += sub_h

    if arrow_to is not None:
        _arrow(d, (x_text + col_w * 0.5, y + 26),
               (arrow_to[0] * W, arrow_to[1] * H), fill)

    out.parent.mkdir(parents=True, exist_ok=True)
    base.save(out, quality=92)
    return out


def _arrow(d: ImageDraw.ImageDraw, start: tuple[float, float],
           end: tuple[float, float], colour: tuple[int, int, int]) -> None:
    """A curved arrow, drawn as a quadratic bezier with a solid head.

    Curved rather than straight because a straight line reads as a diagram and a
    curve reads as a hand pointing. The control point is offset perpendicular to
    the run, so the bow always opens away from the type.
    """
    (x0, y0), (x1, y1) = start, end
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    n = max((dx * dx + dy * dy) ** 0.5, 1.0)
    cx, cy = mx - dy / n * n * 0.22, my + dx / n * n * 0.22

    pts = []
    for i in range(41):
        t = i / 40
        u = 1 - t
        pts.append((u * u * x0 + 2 * u * t * cx + t * t * x1,
                    u * u * y0 + 2 * u * t * cy + t * t * y1))
    d.line(pts, fill=colour, width=11, joint="curve")

    ax, ay = pts[-1]
    bx, by = pts[-6]
    vx, vy = ax - bx, ay - by
    m = max((vx * vx + vy * vy) ** 0.5, 1.0)
    vx, vy = vx / m, vy / m
    s = 30
    d.polygon([(ax + vx * 8, ay + vy * 8),
               (ax - vx * s - vy * s * 0.6, ay - vy * s + vx * s * 0.6),
               (ax - vx * s + vy * s * 0.6, ay - vy * s - vx * s * 0.6)],
              fill=colour)
