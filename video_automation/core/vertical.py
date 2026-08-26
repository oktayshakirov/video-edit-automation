"""Short-form vertical export — 9:16 with a text overlay.

This is the one place the project renders video. The "never render" rule was
scoped to the 4K YouTube pipeline, where the deliverable is an FCPXML timeline
to finish by hand. A TikTok/Shorts test clip has to be an actual file.

Two decisions worth stating:

* **The crop is native.** 3840x2160 -> 1080x1920 is a straight crop, no scaling,
  so nothing is softened. It keeps 28% of the width, which leaves 2760px of
  horizontal freedom — the single biggest quality decision in a vertical export,
  and the reason it is measured rather than left at centre.

* **Type is rendered with Pillow, not ffmpeg's drawtext.** The local ffmpeg has
  no libfreetype, and OpenCV only offers Hershey vector fonts. Pillow gives real
  font rendering, wrapping and alpha, composited as a single PNG.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from .frame import VERTICAL, Frame

# Kept as module constants, because most of what lives below is vertical by
# definition — the 4K native crop, and the ffmpeg burn-in chains over in
# `voiceover.py` — and threading a frame through those would be ceremony around
# a value that cannot vary. One source of truth all the same: they *are* the
# vertical frame's size, so there is nowhere for the two to drift apart.
OUT_W, OUT_H = VERTICAL.size
# SF Rounded is the closest system face to what the silent quote-card genre uses.
FONT_ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"
# Futura Medium — the caption face for narrated shorts, chosen on real frames
# against Avenir Next, Baskerville and Didot. Serif faces lose to the stroke:
# the border swallows the thin strokes and the type goes muddy. A .ttc, so the
# weight is selected by index rather than by a variation name.
FONT_CAPTION = "/System/Library/Fonts/Supplemental/Futura.ttc"
FONT_CAPTION_INDEX = 0
FONT_CAPTION_SIZE = 44

# Iowan Old Style Italic — the approved caption face for the drone channel's
# narrated *quote* shorts specifically (`render_narrated`/`render_narrated_stack`
# defaults), chosen over Futura on the Sunset Sea Stack cut and kept as the
# default for both the single-clip and stacked layouts. Distinct from
# FONT_CAPTION above, which crypto/tinnitus/longform still use — this
# constant only changes the drone quote pipeline's default.
FONT_QUOTE = "/System/Library/Fonts/Supplemental/Iowan Old Style.ttc"
FONT_QUOTE_INDEX = 2   # Italic
FONT_QUOTE_SIZE = 44

# TikTok and Shorts put their UI on the bottom band and right edge. The genre
# sits type near 40% height, well clear of both, and keeps the block narrow.
TEXT_MAX_W = 780


def interest_map(proxy: Path) -> np.ndarray | None:
    """Where the content is: edge energy plus saturation, averaged over the clip.

    Edge energy suppresses sky without special-casing it — smooth gradients
    score near zero — so the window is drawn toward buildings and terrain
    rather than empty air.
    """
    cap = cv2.VideoCapture(str(proxy))
    acc, n, idx = None, 0, 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        idx += 1
        if idx % 5:                      # every 5th proxy frame is plenty
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        sob = np.abs(cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)) + \
              np.abs(cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3))
        sat = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)[:, :, 1].astype(np.float32)
        m = sob + 0.5 * sat
        acc = m if acc is None else acc + m
        n += 1
    cap.release()
    return None if n == 0 else acc / n


def _search_box(m: np.ndarray | None, crop_w: int, crop_h: int,
                src_w: int, src_h: int) -> tuple[int, int, int, int]:
    """Slide a `crop_w` x `crop_h` window over the interest map, 2D.

    Shared by `pick_crop` (9:16) and `pick_crop_tile` (arbitrary aspect,
    the stacked layout's tiles) — the search itself doesn't care what
    aspect ratio the window is, only its size.
    """
    if m is None:
        return (src_w - crop_w) // 2, (src_h - crop_h) // 2, crop_w, crop_h

    ph, pw = m.shape
    wx = max(int(round(crop_w * pw / src_w)), 1)
    wy = max(int(round(crop_h * ph / src_h)), 1)

    # 2D box sums via an integral image.
    ii = cv2.integral(m.astype(np.float64))
    best, bxy = -1.0, (0, 0)
    for yy in range(0, ph - wy + 1, 2):
        for xx in range(0, pw - wx + 1, 2):
            s = (ii[yy + wy, xx + wx] - ii[yy, xx + wx]
                 - ii[yy + wy, xx] + ii[yy, xx])
            if s > best:
                best, bxy = s, (xx, yy)

    x = int(round(bxy[0] * src_w / pw))
    y = int(round(bxy[1] * src_h / ph))
    return (max(0, min(x, src_w - crop_w)),
            max(0, min(y, src_h - crop_h)), crop_w, crop_h)


def pick_crop(proxy: Path, zoom: float = 1.0,
              src_w: int = 3840, src_h: int = 2160) -> tuple[int, int, int, int]:
    """Place a 9:16 window over the frame — horizontally *and* vertically.

    Choosing x alone is not enough. On a wide landscape shot the interest sits
    in a horizontal band near the ground, so a full-height window spends more
    than half the frame on sky. `zoom` tightens the window (1.0 = full sensor
    height, higher = closer) and the vertical position is then searched too.

    At zoom 1.4 the window is 1543px tall and upscaled to 1920 — from a 4K
    source that stays sharp, and it fills the frame with subject instead of air.
    """
    crop_h = int(round(min(src_h, src_h / zoom)))
    crop_w = min(int(round(crop_h * OUT_W / OUT_H)), src_w)
    return _search_box(interest_map(proxy), crop_w, crop_h, src_w, src_h)


def stack_tile_size(band: int = 140) -> tuple[int, int]:
    """The size of one tile in the stacked two-clip layout.

    `band` is the black strip between the tiles that the caption sits in —
    approved at 140px on Sunset Sea Stack. Call this before `pick_crop_tile`
    for each clip so both tiles and the caller's `render_narrated_stack` call
    agree on the same split without repeating the arithmetic.
    """
    return OUT_W, (OUT_H - band) // 2


def pick_crop_tile(proxy: Path, tile_w: int, tile_h: int,
                   src_w: int = 3840, src_h: int = 2160) -> tuple[int, int, int, int]:
    """Place a window of an arbitrary aspect ratio — for a stacked-layout tile.

    Same search as `pick_crop`, but the window is sized to the tile's own
    aspect rather than derived from `zoom` against 9:16. A stack tile is wider
    and shorter than a 9:16 crop, so it keeps far more of the sensor width —
    enough that a `lateral` move can survive here where it would exit a 28%
    9:16 window.
    """
    crop_h = src_h
    crop_w = min(int(round(crop_h * tile_w / tile_h)), src_w)
    if crop_w == src_w:
        crop_h = min(int(round(crop_w * tile_h / tile_w)), src_h)
    return _search_box(interest_map(proxy), crop_w, crop_h, src_w, src_h)


def sample_bg_luma(src: Path, box: tuple[int, int, int, int], t: float) -> float:
    """Mean luminance of the band the text will sit in, 0-1.

    Drives the white-or-black decision. Sampling the actual crop at the actual
    timecode beats guessing from the clip average — a sunset clip can be bright
    sky at the top and near-black ground where the text lands.
    """
    x, y, w, h = box
    cap = cv2.VideoCapture(str(src))
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
    ok, frame = cap.read()
    cap.release()
    if not ok:
        return 0.5
    crop = frame[y:y + h, x:x + w]
    if crop.size == 0:
        return 0.5
    band = crop[int(h * 0.32):int(h * 0.62), :]     # where the type goes
    return float(cv2.cvtColor(band, cv2.COLOR_BGR2GRAY).mean() / 255.0)


def _wrap(draw, text, font, max_w):
    """Greedy wrap, then pull back a word so the last line is never a widow.

    A single orphaned word on the final line is the tell that separates a
    generated card from a hand-set one, and this genre lives or dies on looking
    native to the platform.
    """
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    while len(lines) > 1 and len(lines[-1].split()) < 2:
        prev = lines[-2].split()
        if len(prev) < 3:
            break
        lines[-2] = " ".join(prev[:-1])
        lines[-1] = f"{prev[-1]} {lines[-1]}"
    return lines


def _load_font(path: str, size: int, index: int = 0):
    font = ImageFont.truetype(path, size, index=index)
    if path == FONT_ROUNDED:
        try:                               # SF Rounded is variable; ask for Semibold
            font.set_variation_by_name("Semibold")
        except Exception:
            pass
    return font


def render_text_png(text: str, out: Path, size: int = 46,
                    bg_luma: float = 0.5, font_path: str = FONT_ROUNDED,
                    font_index: int = 0, y_frac: float = 0.40,
                    stroke: int = 0, max_w: int = TEXT_MAX_W,
                    frame: Frame = VERTICAL,
                    ink: tuple[int, int, int, int] | None = None) -> Path:
    """Quote card in the style the genre actually uses.

    Deliberately unlike a lower-third: small type, no scrim or box.

    Two legibility treatments, and which one is right depends on the footage:

    * **Halo** (`stroke=0`, the default) — a soft blurred shadow drawn from the
      glyphs, invisible until it is needed, with the ink following the
      background: white on dark, near-black on bright. Quiet, and the better
      look when the background under the type is uniform.
    * **Stroke** (`stroke>0`) — white ink with a solid black border. Louder, and
      the only one that survives type crossing a horizon, where a single ink
      colour is wrong for half the line. `bg_luma` is ignored, because the
      contrast no longer comes from the background.

    `ink` overrides the fill colour. Only worth reaching for on the stroked
    template, and only on the one word a quote turns on — the black border
    carries the legibility, so the fill is free to pick a colour out of the
    footage. Everything else stays white; two coloured words is a theme, not
    an accent.

    `y_frac` is the centre of the text block as a fraction of frame height.
    `max_w` is the wrap width; captions run wider than the silent quote card,
    because a spoken phrase broken across two lines reads as two thoughts.
    """
    font = _load_font(font_path, size, font_index)

    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = _wrap(probe, text, font, max_w)
    line_h = int(size * 1.34)
    block_h = line_h * len(lines)
    top = int(frame.h * y_frac) - block_h // 2

    if stroke:
        img = Image.new("RGBA", frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        y = top
        for ln in lines:
            w = d.textlength(ln, font=font)
            d.text(((frame.w - w) / 2, y), ln, font=font,
                   fill=ink or (255, 255, 255, 255),
                   stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
            y += line_h
        img.save(out)
        return out

    dark_text = bg_luma > 0.62
    ink = ink or ((18, 18, 18, 255) if dark_text else (255, 255, 255, 255))
    halo = (255, 255, 255, 128) if dark_text else (0, 0, 0, 150)

    layer = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = top
    for ln in lines:
        w = d.textlength(ln, font=font)
        d.text(((frame.w - w) / 2, y), ln, font=font, fill=ink)
        y += line_h

    # Soft halo from the glyphs themselves — reads as depth, not as a box.
    shadow = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    y = top
    for ln in lines:
        w = sd.textlength(ln, font=font)
        sd.text(((frame.w - w) / 2, y + 2), ln, font=font, fill=halo)
        y += line_h
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))

    img = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    img.alpha_composite(shadow)
    img.alpha_composite(layer)
    img.save(out)
    return out


def render_short(src: Path, out: Path, start: float, duration: float,
                 box: tuple[int, int, int, int], text_png: Path | None = None) -> Path:
    """Cut, crop to 9:16, scale to 1080x1920, burn the text card, drop audio.

    No fade to black. Shorts loop, and a fade spends the last half-second
    telling the viewer it is over — the loop point should land on picture.
    """
    x, y, w, h = box
    crop = f"crop={w}:{h}:{x}:{y},scale={OUT_W}:{OUT_H}:flags=lanczos"
    if text_png:
        vf = f"[0:v]{crop}[v];[v][1:v]overlay=0:0[o]"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-t", f"{duration}",
               "-i", str(src), "-i", str(text_png),
               "-filter_complex", vf, "-map", "[o]"]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-t", f"{duration}",
               "-i", str(src), "-vf", crop]
    cmd += ["-an", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out


def render_caption_karaoke(text: str, out: Path, active: int, size: int = 46,
                           font_path: str = FONT_ROUNDED, font_index: int = 0,
                           y_frac: float = 0.70, stroke: int = 4,
                           max_w: int = TEXT_MAX_W, frame: Frame = VERTICAL,
                           accent: tuple[int, int, int, int] = (255, 255, 255, 255),
                           grow: float = 1.08) -> Path:
    """One caption frame with word `active` lifted in colour and scale.

    The device every short-form platform's own captions use: the whole phrase
    stays on screen and the word being spoken right now is picked out. It is
    the cheapest thing that keeps an eye on the type instead of on the scroll
    gesture, which is the entire job of a burned caption.

    **The layout is measured at the base size and never re-flowed.** The
    active word is drawn larger about its own centre, inside the box the base
    font reserved for it, so no other word moves. Re-wrapping per frame — or
    even just re-measuring the line with one word enlarged — makes the
    sentence twitch sideways on every syllable, which is far worse than no
    highlight at all. That is the whole reason this cannot be done by calling
    `render_text_png` with a bigger font for one word.

    `active` is an index into `text.split()`. Out of range draws the phrase
    plain, which is what the trailing silence after the last word wants.

    **`grow` is 1.08 and it wants to stay small.** The enlarged word is
    centred inside the advance the base font reserved, so it overhangs its box
    by half the difference on each side — at 1.14 a long word like "always"
    visibly touched its neighbours, since the inter-word space is a single
    space at caption size. The colour is doing most of the work anyway; the
    scale is there to stop the highlight reading as flat.
    """
    font = _load_font(font_path, size, font_index)
    big = _load_font(font_path, max(size + 1, int(round(size * grow))),
                     font_index)

    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = _wrap(probe, text, font, max_w)
    line_h = int(size * 1.34)
    top = int(frame.h * y_frac) - line_h * len(lines) // 2

    img = Image.new("RGBA", frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Walk the words in the same order `_wrap` laid them out, so the index the
    # caller counted on `text.split()` lands on the right glyph run.
    wi, y = 0, top
    space = d.textlength(" ", font=font)
    for ln in lines:
        words = ln.split()
        widths = [d.textlength(w, font=font) for w in words]
        x = (frame.w - (sum(widths) + space * (len(words) - 1))) / 2
        for w, adv in zip(words, widths):
            hot = wi == active
            f_use = big if hot else font
            fill = accent if hot else (255, 255, 255, 255)
            # Centre the (possibly larger) glyph run on the box the base font
            # reserved, so the advance the next word starts from is unchanged.
            dx = (adv - d.textlength(w, font=f_use)) / 2
            dy = (size - f_use.size) / 2
            d.text((x + dx, y + dy), w, font=f_use, fill=fill,
                   stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
            x += adv + space
            wi += 1
        y += line_h

    img.save(out)
    return out


EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"
# Apple Color Emoji is a bitmap font and only loads at the sizes it has strikes
# for — 44 and 137 both raise "invalid pixel size". Render at 160 and scale
# down, which is the only size-independent way to use it.
EMOJI_STRIKE = 160

_EMOJI_CACHE: dict = {}


def emoji_image(char: str, height: int) -> "Image.Image":
    """One emoji as an RGBA image `height` px tall, cropped to its ink.

    The same bitmap-strike dance `add_caption_emoji` does — render at
    `EMOJI_STRIKE` and scale — factored out so a drawn beat can put an icon
    beside an item without going through a finished PNG. Cached by
    `(char, height)`: a `steps` beat draws the same five icons on every one of
    ~480 frames, and re-rendering a 160px glyph and LANCZOS-scaling it each
    time is pure waste.
    """
    key = (char, height)
    hit = _EMOJI_CACHE.get(key)
    if hit is not None:
        return hit
    font = ImageFont.truetype(EMOJI_FONT, EMOJI_STRIKE)
    big = Image.new("RGBA", (EMOJI_STRIKE * 2, EMOJI_STRIKE * 2), (0, 0, 0, 0))
    ImageDraw.Draw(big).text((EMOJI_STRIKE // 4, EMOJI_STRIKE // 4), char,
                             font=font, embedded_color=True)
    box = big.getbbox()
    if box is None:
        raise ValueError(f"emoji {char!r} rendered empty — not in the font")
    big = big.crop(box)
    w = max(1, int(big.width * height / big.height))
    img = big.resize((w, height), Image.LANCZOS)
    _EMOJI_CACHE[key] = img
    return img


def add_caption_emoji(png: Path, text: str, char: str, size: int,
                      y_frac: float, font_path: str, font_index: int,
                      gap: int = 16, frame: Frame = VERTICAL) -> None:
    """Set an emoji after a caption, in place, keeping the pair centred.

    Done as a second pass over the finished PNG rather than inside
    `render_text_png`: that template is shared with the drone shorts and is not
    to be redesigned. The whole text layer shifts left by half the emoji block
    and the emoji lands in the space that opens up, so the line reads as one
    centred unit rather than as type with something bolted to the end.

    Single-line captions only — which is what a caption worth an emoji is.
    """
    font = ImageFont.truetype(font_path, size, index=font_index)
    emoji_font = ImageFont.truetype(EMOJI_FONT, EMOJI_STRIKE)

    big = Image.new("RGBA", (EMOJI_STRIKE * 2, EMOJI_STRIKE * 2), (0, 0, 0, 0))
    ImageDraw.Draw(big).text((EMOJI_STRIKE // 4, EMOJI_STRIKE // 4), char,
                             font=emoji_font, embedded_color=True)
    big = big.crop(big.getbbox())
    h = int(size * 1.02)
    emoji = big.resize((max(1, int(big.width * h / big.height)), h),
                       Image.LANCZOS)

    layer = Image.open(png).convert("RGBA")
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = probe.textlength(text, font=font)
    dx = (emoji.width + gap) // 2

    shifted = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    shifted.paste(layer, (-dx, 0))

    line_h = int(size * 1.34)
    top = int(frame.h * y_frac) - line_h // 2
    shifted.alpha_composite(
        emoji, (int((frame.w - tw) / 2 - dx + tw + gap), top + (line_h - h) // 2))
    shifted.save(png)
