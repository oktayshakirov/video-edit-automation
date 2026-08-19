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

# **One display face and one type treatment for both aspects.** The landscape
# thumbnail used to set Futura Medium with an 8px black stroke on every glyph.
# Reviewed against what large channels ship, both halves were wrong: Futura is
# a light, wide geometric that goes weak at feed size, and a hard outline round
# every letter is the clearest tell of an amateur thumbnail. Arial Black is the
# closest face on this machine to the Anton/Montserrat-ExtraBold weight the
# references use; Impact is heavier still and was rejected as meme-coded.
#
# `_headline` below is shared by `render_thumb` and `render_short_thumb` so a
# long video and the Short cut from the same post cannot drift apart. They are
# published as a pair and should look like one.
FONT_DISPLAY = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

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


def _layout(image: Path, col: float = 0.54, margin_px: int = 26,
            want_side: str | None = None
            ) -> tuple[Image.Image, str, str, float, bool]:
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

    # The type block is roughly this tall, so score the band it will actually
    # occupy rather than the whole column. Placing it dead centre and only
    # choosing a *side* was the previous version, and it ignored half the
    # question: on a subject who fills the lower frame, the space is up in the
    # corner, not beside them.
    BANDS = {"top": (0.04, 0.60), "middle": (0.20, 0.80), "bottom": (0.40, 0.96)}

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

        for side in ((want_side,) if want_side else ("left", "right")):
            lo = 58 if side == "left" else W - 58 - col_w
            hi = lo + col_w + margin_px
            for x0 in np.linspace(0, max(nw - W, 0), 9).astype(int):
                # The subject side, full height — the contrast term.
                if side == "left":
                    other = e_big[y0:y0 + H, x0 + hi:x0 + W]
                else:
                    other = e_big[y0:y0 + H, x0:x0 + max(lo - margin_px, 1)]
                busy = float(other.mean()) if other.size else 0.0

                for vband, (t0, t1) in BANDS.items():
                    band = e_big[y0 + int(H * t0):y0 + int(H * t1),
                                 x0 + max(lo - margin_px, 0):x0 + hi]
                    quiet = float(band.mean()) if band.size else 1.0
                    score = quiet - 0.6 * busy
                    for (fx, fy, fw, fh) in f_big:
                        if (fx - x0 < hi and fx + fw - x0 > lo
                                and fy - y0 < H * t1 and fy + fh - y0 > H * t0):
                            score += 1.0      # a face under the type is fatal
                        # **A face sliced by the crop edge is also fatal.** The
                        # scorer's only question used to be "is the type on
                        # quiet pixels", and the cheapest way to make a column
                        # quiet is to zoom until the subject is mostly outside
                        # the frame — so it did, and the crypto-exchanges
                        # thumbnail shipped with half a man's head against the
                        # left edge. A thumbnail is a promise about who the
                        # video is about, and half a face is not one.
                        #
                        # **Compared against the clamped box, not the raw
                        # one.** The cascade routinely returns a box running
                        # off the source — on `futuristic-crypto-exchange.jpg`
                        # it comes back at y=-53 — and testing the raw box made
                        # every candidate clipped, so the penalty fired
                        # uniformly and discriminated between nothing. What
                        # matters is only what *this crop* cuts that the source
                        # had.
                        cx0, cy0 = max(fx, 0), max(fy, 0)
                        cx1, cy1 = min(fx + fw, nw), min(fy + fh, nh)
                        if cx1 > cx0 and cy1 > cy0 and (
                                cx0 < x0 or cx1 > x0 + W
                                or cy0 < y0 or cy1 > y0 + H):
                            score += 1.0
                    # All else equal, take less zoom. Every step up is a step
                    # further into a 900px source that is already being
                    # upscaled to 1280, and the scorer has no other reason to
                    # prefer the tighter crop.
                    score += 0.02 * (zoom - 1.0)
                    cand = (score, zoom, sc, nw, nh, int(x0), y0, side, vband)
                    if best is None or score < best[0]:
                        best = cand

    score, zoom, sc, nw, nh, x0, y0, side, vband = best
    big = cv2.resize(src, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    crop = big[y0:y0 + H, x0:x0 + W]
    img = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
    # 0.20 of peak edge energy is about the level of a plain wall with soft
    # shading. Above it there is real detail under the words.
    # Negative means the subject side is meaningfully busier than the type
    # side, which is the composition this is after.
    return img, side, vband, score, score < 0.0


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


def _wrap_balanced(words: list[tuple[str, bool]], d: ImageDraw.ImageDraw,
                   font: ImageFont.FreeTypeFont, space: float, col_w: int
                   ) -> list[list[tuple[str, bool, float]]]:
    """Break `words` into lines minimizing raggedness, not first-fit greedy.

    **Greedy left-to-right fill is what put "IN" alone on its own row.** It
    places words until the next one would overflow the column, and stops —
    it never looks ahead to see that the *next* two words would sit together
    happily. On "Stop sleeping in silence" that produced four one-word lines,
    because SLEEPING nearly fills the column on its own and greedy never
    reconsiders once IN has already been placed alone.

    This is the standard minimum-raggedness line break (the algorithm behind
    CSS `text-wrap: balance`): a small DP over every possible split, scored by
    how much slack each line leaves against `col_w`, so lines that are nearly
    full are preferred over lines that leave a two-letter word rattling around
    on its own. A split that overflows the column is not forbidden — a single
    word wider than the column has nowhere else to go — but it is penalised
    heavily enough that the DP only reaches for it when there is truly no
    narrower arrangement.

    Cost, not a rule about word length, is what avoids the orphan: pairing a
    short connector onto the next line almost always leaves less slack than
    stranding it alone, so it falls out of minimising raggedness rather than a
    special case for "words under N letters".
    """
    n = len(words)
    widths = [d.textlength(w, font=font) for w, _ in words]

    def seg_width(i: int, j: int) -> float:
        seg = widths[i:j]
        return sum(seg) + space * (len(seg) - 1) if seg else 0.0

    INF = float("inf")
    cost = [0.0] + [INF] * n
    back = [0] * (n + 1)
    for j in range(1, n + 1):
        for i in range(j):
            w = seg_width(i, j)
            if w <= col_w:
                penalty = (col_w - w) ** 2
            elif j - i == 1:
                # A single word wider than the column has nowhere else to go
                # — allow it, at a cost steep enough that the DP only reaches
                # for it when nothing narrower exists.
                penalty = (w - col_w) * 1e6 + 1e12
            else:
                # **A multi-word line is never allowed to overflow.** The
                # first version penalised overflow by a near-constant 1e12
                # regardless of how far over it ran, which made "SLEEPING IN
                # SILENCE" on one line look almost as cheap as one genuinely
                # unavoidable overflowing word — and DP picked it, rendering
                # text past the right edge of the frame. Skipping the split
                # entirely is what a greedy wrap got right by construction and
                # this has to keep: a line's width is a hard limit, not
                # something to trade off against raggedness.
                continue
            if cost[i] + penalty < cost[j]:
                cost[j] = cost[i] + penalty
                back[j] = i

    idx, spans = n, []
    while idx > 0:
        i = back[idx]
        spans.append((i, idx))
        idx = i
    spans.reverse()

    return [[(w, hot, widths[k]) for k, (w, hot) in enumerate(words[i:j], start=i)]
            for i, j in spans]


def _headline(base: Image.Image, headline: str, size: int, col_w: int,
              x_text: int, fill, ink, max_lines: int = 4,
              max_block: float = 1e9, leading: float = 1.02,
              band: str = "middle", margin: int = 58,
              shadow: int = 14, drop: tuple = (6, 8)):
    """Lay out and paint the headline. Shared by both aspects on purpose.

    Returns the block height. `band` places it once the height is known, which
    is why placement lives here rather than in the callers.

    **Shrink until it fits and until the accent run lands whole on one line.**
    An accent that wraps draws two plates on two lines and loses the single
    focal point the device exists for. Try the largest size that keeps it
    intact; fall back to merely fitting if no size does.

    **The shadow is a blurred layer, not a stroke.** A stroke traces every
    glyph at a constant width and reads as an outline; a blurred offset copy
    reads as the type sitting above the picture. That difference is most of
    what separates these from a template.

    **Plates are sized from the cap band, not the line box.** A font's line box
    carries ascender and descender room that uppercase never uses, and padding
    it leaves the words riding high in the plate.
    """
    d = ImageDraw.Draw(base)
    words = _split(headline.upper())

    def orphan(lines) -> bool:
        # A lone word of three letters or fewer stranded on its own row - the
        # exact "IN" on its own line" complaint. Bigger words are legitimate
        # single-word lines; connectors this short read as a layout mistake.
        return any(len(ln) == 1 and len(ln[0][0]) <= 3 for ln in lines)

    fallback = fallback_ok = None
    for _ in range(16):
        font = ImageFont.truetype(FONT_DISPLAY, size)
        space = d.textlength(" ", font=font)
        lines = _wrap_balanced(words, d, font, space, col_w)
        line_h = int(size * leading)
        block = len(lines) * line_h
        fits = len(lines) <= max_lines and block < max_block
        hot_lines = {i for i, ln in enumerate(lines) if any(h for _, h, _ in ln)}
        if fits and fallback is None:
            fallback = (size, font, space, lines, line_h, block)
        if fits and len(hot_lines) <= 1:
            if fallback_ok is None:
                fallback_ok = (size, font, space, lines, line_h, block)
            # **Do not stop at the first size that merely fits.** The largest
            # size clears `max_lines` almost immediately - one word per line
            # is always short enough - which is exactly the layout that
            # stranded "IN" alone: nothing forced a look at a slightly smaller
            # size where it pairs with the next word. Keep shrinking past a
            # "fits" size while a short word is still stuck on its own row.
            if not orphan(lines):
                break
        size -= 8
    else:
        # Ran out of sizes without an orphan-free fit. Prefer the smallest
        # size that still satisfied the one-accent-line rule over the largest
        # size that merely fit at all - a slightly smaller, well-paired
        # headline beats a maximal one with a stray word on it.
        chosen = fallback_ok or fallback
        if chosen is not None:
            size, font, space, lines, line_h, block = chosen

    Wf, Hf = base.size
    y = {"top": margin,
         "middle": (Hf - block) // 2,
         "bottom": Hf - margin - block}[band]

    asc, _ = font.getmetrics()
    cap_h = font.getbbox("H")[3] - font.getbbox("H")[1]
    pad_x, pad_v = 18, int(size * 0.13)

    plates, glyphs = [], []
    yy = y
    for line in lines:
        base_y = yy + asc
        x = x_text
        # One plate per *run* of accent words, not one per word. Boxing each
        # word separately leaves a seam of background between them, which reads
        # as a rendering fault rather than a highlight.
        runs, start, width = [], None, 0.0
        for word, hot, ww in line:
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
            plates.append([rx - pad_x, base_y - cap_h - pad_v,
                           rx + rw + pad_x, base_y + pad_v])
        x = x_text
        for word, hot, ww in line:
            glyphs.append((x, yy, word, hot))
            x += ww + space
        yy += line_h

    dx, dy = drop
    lay = Image.new("L", base.size, 0)
    ld = ImageDraw.Draw(lay)
    for b in plates:
        ld.rectangle([b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy], fill=190)
    for gx, gy, word, hot in glyphs:
        if not hot:
            ld.text((gx + dx, gy + dy), word, font=font, fill=210)
    lay = lay.filter(ImageFilter.GaussianBlur(shadow))
    base.paste(Image.composite(Image.new("RGB", base.size, (0, 0, 0)),
                               base, lay), (0, 0))

    d = ImageDraw.Draw(base)
    for b in plates:
        d.rectangle(b, fill=fill)
    for gx, gy, word, hot in glyphs:
        d.text((gx, gy), word, font=font, fill=ink if hot else (255, 255, 255))
    return block


def render_thumb(out: Path, brand: Brand, headline: str,
                 image: Path | None = None, accent: str = "red",
                 size: int = 118, side: str | None = None,
                 arrow_to: tuple[float, float] | None = None,
                 crop_at: tuple[float, float] | None = None,
                 crop_zoom: float = 1.0, crop_band: str = "middle",
                 **_ignored) -> Path:
    """One thumbnail: photograph, scrim, headline with a boxed accent phrase.

    `headline` marks its accent with brackets — `"Nobody has [passed it]"`.
    `arrow_to` is a fractional point on the frame; when given, a hand-drawn
    style arrow curves from the type toward it. Use it only when there is
    something specific to point at.

    **`_layout`'s scorer optimises for empty space, not for the subject being
    visible.** It found this while pairing a portrait source with the long
    form's landscape thumbnail: the crop it chose was a towel and a shoulder,
    because that band of the frame is quieter than the one with her face and
    the phone's glow in it — exactly the failure the shorts skill already
    named ("the scorer loses to the subject") arriving at this renderer too.
    **`crop_at`, as `(ax, ay)` fractions of the leftover crop space, bypasses
    the scorer entirely** and places the picture by hand, the same escape
    hatch `render_short_thumb` already has via `ax`/`zoom`. `side` still
    chooses which half carries the type; pass it explicitly since there is no
    scorer run to infer one from.

    Extra keyword arguments are ignored, so the older `zoom`/`focus`/`kicker`
    call sites keep working while the layout is chosen automatically.
    """
    box = None
    if crop_at is not None and image is not None and Path(image).exists():
        src = cv2.imread(str(Path(image)))
        sh, sw = src.shape[:2]
        s = max(W / sw, H / sh) * crop_zoom
        nw, nh = int(np.ceil(sw * s)), int(np.ceil(sh * s))
        big = cv2.resize(src, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
        ax, ay = crop_at
        x0 = int(np.clip((nw - W) * ax, 0, max(nw - W, 0)))
        y0 = int(np.clip((nh - H) * ay, 0, max(nh - H, 0)))
        crop = big[y0:y0 + H, x0:x0 + W]
        base = Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB))
        side, vband = side or "left", crop_band
        base = base.filter(ImageFilter.GaussianBlur(1.2))
        luma = np.asarray(base.convert("L")).mean()
        base = ImageEnhance.Brightness(base).enhance(
            float(np.clip(74.0 / max(luma, 1.0), 0.62, 1.12)))
    elif image is not None and Path(image).exists():
        base, found, vband, score, clear = _layout(Path(image), want_side=side)
        side = side or found
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
        base, side, vband = Image.new("RGB", (W, H), brand.bg), side or "left", "middle"

    # A scrim on the type's side only, fading out before the subject.
    grad = Image.new("L", (W, 1))
    px = grad.load()
    for x in range(W):
        p = x / (W - 1)
        p = p if side == "left" else 1.0 - p
        px[x, 0] = int(232 * max(0.0, 1.0 - (p / 0.66) ** 1.7))
    base = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)),
                           base, grad.resize((W, H)))

    margin = 58
    col_w = int(W * 0.54)
    x_text = margin if side == "left" else W - margin - col_w
    fill, ink = ACCENTS.get(accent, ACCENTS["red"])

    block = _headline(base, headline, size, col_w, x_text, fill, ink,
                      max_lines=4, max_block=H - 2 * margin, leading=1.06,
                      band=vband, margin=margin, shadow=11, drop=(5, 6))
    y = {"top": margin, "middle": (H - block) // 2,
         "bottom": H - margin - block}[vband] + block
    d = ImageDraw.Draw(base)

    if arrow_to is not None:
        _arrow(d, (x_text + col_w * 0.5, y + 20),
               (arrow_to[0] * W, arrow_to[1] * H), fill)

    out.parent.mkdir(parents=True, exist_ok=True)
    base.save(out, quality=92)
    return out


# --- session thumbnails --------------------------------------------------
#
# A different layout, because a sound-therapy session breaks every assumption
# `render_thumb` is built on. There is no photograph, so there is no subject to
# find and no empty half to pan the type into; a frame grab would be a dark
# nebula with a thin circle on it, which at 360px wide is a black rectangle.
#
# What a session thumbnail has to sell is not an argument, it is a *spec*: how
# long, what sound, what breath pattern. People search "10 minute breathing" and
# scan a grid for the number, so **the duration is the accent** — it takes the
# role the boxed phrase takes on an article thumbnail.
#
# It is also a series template on purpose. The same ring in the same place with
# a different number reads as one shelf of videos rather than five unrelated
# ones, and that is worth more than making each thumbnail individually clever.

def render_session_thumb(out: Path, brand: Brand, minutes: int,
                         headline: str, pattern: str | None = None,
                         accent: str = "cyan", seed: int = 7,
                         size: int = 104) -> Path:
    """Thumbnail for a sound-therapy session: nebula, ring, duration, spec.

    `headline` is two or three words, no brackets — the accent here is the
    duration, so a second highlight would only compete with it. `pattern` is
    the breath spec ("4 IN / 6 OUT"), drawn as a chip under the headline.

    The nebula comes from the video's own generator at the same `seed`, so the
    thumbnail is a picture of this video rather than of the format.
    """
    from ..tinnitus.asmr import _ring_sprite, nebula_canvas

    # Generated a good deal larger and downsampled. The nebula's stars are
    # single pixels; rendering at 1280 wide and saving as JPEG turns them into
    # mush, where rendering at 2x and resizing keeps them as points.
    base = Image.fromarray(nebula_canvas(W * 2, H * 2, seed)).resize(
        (W, H), Image.LANCZOS).convert("RGB")
    # Lift it. In the video the nebula is a backdrop nobody looks at directly;
    # in a grid it is competing, and the same pixels read as an empty black box.
    base = ImageEnhance.Brightness(base).enhance(1.22)

    # Scrim under the headline column, same device as `render_thumb`. Lifting
    # the nebula is what makes the thumbnail read at all, and it is also what
    # puts a blown-out cloud behind the type — at seed 7 there is a near-white
    # one in the top-left corner, exactly where the headline goes. The stroke
    # alone survives it; the headline stops being *quiet*, which is the one
    # quality this format is selling.
    grad = Image.new("L", (W, 1))
    px = grad.load()
    for x in range(W):
        px[x, 0] = int(224 * max(0.0, 1.0 - ((x / (W - 1)) / 0.60) ** 1.7))
    base = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)),
                           base, grad.resize((W, H)))

    fill, ink = ACCENTS.get(accent, ACCENTS["cyan"])
    d = ImageDraw.Draw(base)

    # --- the ring, right of centre, holding the number -------------------
    r = 232
    cx, cy = int(W * 0.735), H // 2
    k = int(r * 2 + 80)
    ring = _ring_sprite(r).resize((k, k), Image.LANCZOS)
    base = base.convert("RGBA")
    base.alpha_composite(ring, (cx - k // 2, cy - k // 2))
    d = ImageDraw.Draw(base)

    # The number sits where the countdown sits in the video. That echo is the
    # point: someone who has seen one of these knows what the circle does.
    num_font = ImageFont.truetype(FONT_CAPTION, 250, index=FONT_CAPTION_INDEX)
    unit_font = ImageFont.truetype(FONT_CAPTION, 60, index=FONT_CAPTION_INDEX)
    _mid(d, str(minutes), cx, cy - 40, num_font, fill=fill, stroke=10)
    _mid(d, "MINUTES", cx, cy + 128, unit_font, fill=(255, 255, 255), stroke=7)

    # --- headline, left column ------------------------------------------
    margin, col_w = 62, int(W * 0.44)
    words = headline.upper().split()
    for _ in range(12):
        font = ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)
        space = d.textlength(" ", font=font)
        lines, cur, cw = [], [], 0.0
        for word in words:
            ww = d.textlength(word, font=font)
            if cur and cw + space + ww > col_w:
                lines.append(cur)
                cur, cw = [], 0.0
            cur.append((word, ww))
            cw += ww + (space if len(cur) > 1 else 0)
        if cur:
            lines.append(cur)
        if len(lines) <= 3:
            break
        size -= 8

    line_h = int(size * 1.10)
    block = len(lines) * line_h + (int(size * 1.05) if pattern else 0)
    y = (H - block) // 2
    for line in lines:
        x = margin
        for word, ww in line:
            d.text((x, y), word, font=font, fill=(255, 255, 255),
                   stroke_width=8, stroke_fill=(0, 0, 0))
            x += ww + space
        y += line_h

    # The breath spec as a plate. It is the one piece of information that
    # separates this from a plain noise video, and it is short enough to box.
    if pattern:
        chip = ImageFont.truetype(FONT_CAPTION, int(size * 0.50),
                                  index=FONT_CAPTION_INDEX)
        text = pattern.upper()
        tw = d.textlength(text, font=chip)
        cap = chip.getbbox("H")[3] - chip.getbbox("H")[1]
        asc, _ = chip.getmetrics()
        pad_x, pad_v = 18, int(size * 0.13)
        by = y + 14 + asc
        d.rectangle([margin - pad_x, by - cap - pad_v,
                     margin + tw + pad_x, by + pad_v], fill=fill)
        d.text((margin, y + 14), text, font=chip, fill=ink)

    out.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out, quality=92)
    return out


def render_session_thumb_short(out: Path, brand: Brand, minutes: int,
                               headline: str, pattern: str | None = None,
                               accent: str = "cyan", seed: int = 7,
                               size: int = 88) -> Path:
    """A 9:16 companion to `render_session_thumb`, for a session's own Short.

    Same materials, reflowed — the nebula at this seed, the ring-and-count
    device, the headline-plus-pattern-chip block. Landscape has room to put
    the headline in a left column beside the ring; there is no side to spare
    at 9:16, so the headline stacks above the ring instead and centres rather
    than ranging left, and the scrim follows that split top-to-bottom instead
    of left-to-right.

    Deliberately not routed through `_headline`/`FONT_DISPLAY` — that pairing
    is the article-thumbnail treatment (Arial Black, drop shadow, an accent
    phrase in brackets). A session thumbnail has never used it and this is a
    vertical cut of the *session* style, not a new one: same Futura stroke,
    same nebula, same ring, just reflowed.
    """
    from ..tinnitus.asmr import _ring_sprite, nebula_canvas

    base = Image.fromarray(nebula_canvas(VW * 2, VH * 2, seed)).resize(
        (VW, VH), Image.LANCZOS).convert("RGB")
    base = ImageEnhance.Brightness(base).enhance(1.22)

    # Scrim over the top band, where the headline sits now — the landscape
    # version's left-to-right fade rotated to how 9:16 actually splits the
    # two elements: headline above, ring below.
    grad = Image.new("L", (1, VH))
    px = grad.load()
    for y in range(VH):
        p = y / (VH - 1)
        px[0, y] = int(224 * max(0.0, 1.0 - (p / 0.40) ** 1.7))
    base = Image.composite(Image.new("RGB", (VW, VH), (0, 0, 0)),
                           base, grad.resize((VW, VH)))

    fill, ink = ACCENTS.get(accent, ACCENTS["cyan"])
    base = base.convert("RGBA")

    # --- the ring, centred, low enough to clear the headline block --------
    r = 300
    cx, cy = VW // 2, int(VH * 0.56)
    k = int(r * 2 + 90)
    ring = _ring_sprite(r).resize((k, k), Image.LANCZOS)
    base.alpha_composite(ring, (cx - k // 2, cy - k // 2))
    d = ImageDraw.Draw(base)

    # The number echoes the countdown inside the video, same as landscape.
    num_font = ImageFont.truetype(FONT_CAPTION, 260, index=FONT_CAPTION_INDEX)
    unit_font = ImageFont.truetype(FONT_CAPTION, 62, index=FONT_CAPTION_INDEX)
    _mid(d, str(minutes), cx, cy - 42, num_font, fill=fill, stroke=10)
    _mid(d, "MINUTE" if minutes == 1 else "MINUTES", cx, cy + 134,
         unit_font, fill=(255, 255, 255), stroke=7)

    # --- headline, centred, top band ---------------------------------------
    margin, col_w = 64, VW - 128
    words = headline.upper().split()
    space = 0.0
    for _ in range(12):
        font = ImageFont.truetype(FONT_CAPTION, size, index=FONT_CAPTION_INDEX)
        space = d.textlength(" ", font=font)
        lines, cur, cw = [], [], 0.0
        for word in words:
            ww = d.textlength(word, font=font)
            if cur and cw + space + ww > col_w:
                lines.append(cur)
                cur, cw = [], 0.0
            cur.append((word, ww))
            cw += ww + (space if len(cur) > 1 else 0)
        if cur:
            lines.append(cur)
        if len(lines) <= 3:
            break
        size -= 6

    line_h = int(size * 1.10)
    y = int(VH * 0.07)
    for line in lines:
        lw = sum(ww for _, ww in line) + space * (len(line) - 1)
        x = (VW - lw) / 2
        for word, ww in line:
            d.text((x, y), word, font=font, fill=(255, 255, 255),
                   stroke_width=8, stroke_fill=(0, 0, 0))
            x += ww + space
        y += line_h

    # The breath spec as a centred plate, same device as landscape.
    if pattern:
        chip = ImageFont.truetype(FONT_CAPTION, int(size * 0.52),
                                  index=FONT_CAPTION_INDEX)
        text = pattern.upper()
        tw = d.textlength(text, font=chip)
        cap = chip.getbbox("H")[3] - chip.getbbox("H")[1]
        asc, _ = chip.getmetrics()
        pad_x, pad_v = 18, int(size * 0.14)
        by = y + 14 + asc
        cxm = VW / 2
        d.rectangle([cxm - tw / 2 - pad_x, by - cap - pad_v,
                     cxm + tw / 2 + pad_x, by + pad_v], fill=fill)
        d.text((cxm - tw / 2, y + 14), text, font=chip, fill=ink)

    out.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(out, quality=92)
    return out


def _mid(d: ImageDraw.ImageDraw, text: str, cx: int, cy: int,
         font: ImageFont.FreeTypeFont, fill: tuple[int, int, int],
         stroke: int) -> None:
    """Draw `text` centred on both axes at (cx, cy).

    Stroked, unlike the ring type inside the video. The video's background is
    one this module generated and the contrast is known; a thumbnail is shown
    at 360px against a white page and a dark page and next to whatever else is
    in the grid, so the type has to carry its own contrast.
    """
    x0, y0, x1, y1 = d.textbbox((0, 0), text, font=font)
    d.text((cx - (x1 - x0) // 2 - x0, cy - (y1 - y0) // 2 - y0), text,
           font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))


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


# --- vertical thumbnails, for Shorts -------------------------------------

VW, VH = 1080, 1920


def render_short_thumb(out: Path, brand: Brand, headline: str,
                       image: Path | None = None, accent: str = "red",
                       size: int = 168, at: float = 0.34, ax: float = 0.5,
                       zoom: float = 1.0, band: str = "top") -> Path:
    """A 9:16 thumbnail for a Short.

    **This does not share `render_thumb`'s type treatment, and that is the
    point.** The landscape version sets Futura Medium with an 8px black stroke
    on every letter. Reviewed against what large channels actually ship, two
    things were wrong with it: Futura is a light, wide geometric face that goes
    weak at feed size, and a hard stroke around every glyph is the single
    clearest tell of an amateur thumbnail. The user's words were "the font is
    not good and looks very generic" and "our solid color borders make it look
    very unprofessional".

    So:

    * **A heavy grotesque, not a geometric.** `Arial Black` is the closest face
      on this machine to the Anton/Montserrat-ExtraBold weight the reference
      thumbnails use. Impact is heavier still and was rejected as meme-coded.
    * **A soft drop shadow, not a stroke.** The shadow is rendered on its own
      layer and blurred, so it separates the type from the picture without
      drawing a hard outline around it. That is what the references do and it
      is the whole difference in feel.
    * **One accent run on a solid plate**, with tighter padding than the
      landscape version — the reference plates hug their words.

    **`band` picks which half carries the type**, default `"top"` because the
    Shorts player usually puts the title, channel and buttons across the
    bottom and a rail of buttons up the right. That default is wrong the
    moment the subject's face is in the top half of the crop and the bottom is
    empty pillow or wall — text over a face reads as a mistake regardless of
    how correct the platform-safe-area reasoning is. Set `band="bottom"` when
    the picture itself has the empty half at the bottom; the scrim follows.
    """
    fill, ink = ACCENTS.get(accent, ACCENTS["red"])

    if image is not None and Path(image).exists():
        src = Image.open(image).convert("RGB")
        s = max(VW / src.width, VH / src.height) * zoom
        src = src.resize((int(np.ceil(src.width * s)),
                          int(np.ceil(src.height * s))), Image.LANCZOS)
        # **`at` and `ax` place the crop; only one of them usually does
        # anything.** Cover-cropping a landscape source to 9:16 is constrained
        # by width, so there is no vertical slack left and `at` is inert — the
        # subject is positioned with `ax` instead. `zoom` above 1.0 buys slack
        # in both axes, which is what a wide source needs to put a face at
        # thumbnail size.
        x0 = int((src.width - VW) * ax)
        y0 = int((src.height - VH) * at)
        base = src.crop((x0, y0, x0 + VW, y0 + VH))
        luma = np.asarray(base.convert("L")).mean()
        base = ImageEnhance.Brightness(base).enhance(
            float(np.clip(78.0 / max(luma, 1.0), 0.55, 1.15)))
    else:
        base = Image.new("RGB", (VW, VH), brand.bg)

    # A scrim on the type's half only, so the type has ground under it and the
    # picture still reads underneath. Fades from whichever edge `band` puts
    # the type against.
    grad = Image.new("L", (1, VH))
    px = grad.load()
    for y in range(VH):
        p = y / (VH - 1)
        p = p if band == "top" else 1.0 - p
        px[0, y] = int(215 * max(0.0, 1.0 - (p / 0.62) ** 1.6))
    base = Image.composite(Image.new("RGB", (VW, VH), (0, 0, 0)),
                           base, grad.resize((VW, VH)))

    # Narrow margins on purpose. A Short is judged at roughly 200px wide in a
    # feed, so the type has to run nearly edge to edge; the landscape
    # thumbnail's 58px on a 1280 frame is a much larger share of the width than
    # it looks. The bottom margin is bigger than the top one — it has to clear
    # the Shorts player's own title/channel bar, which the top edge never has
    # to share with anything.
    margin = 52
    edge_margin = int(VH * 0.13) if band == "top" else int(VH * 0.16)
    _headline(base, headline, size, VW - 2 * margin, margin, fill, ink,
              max_lines=4, max_block=VH * 0.5, leading=1.02,
              band=band, margin=edge_margin, shadow=14, drop=(6, 8))

    out.parent.mkdir(parents=True, exist_ok=True)
    base.save(out, quality=92)
    return out
