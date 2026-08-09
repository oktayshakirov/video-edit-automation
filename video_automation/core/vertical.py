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

OUT_W, OUT_H = 1080, 1920
# SF Rounded is the closest system face to what the silent quote-card genre uses.
FONT_ROUNDED = "/System/Library/Fonts/SFNSRounded.ttf"
# Futura Medium — the caption face for narrated shorts, chosen on real frames
# against Avenir Next, Baskerville and Didot. Serif faces lose to the stroke:
# the border swallows the thin strokes and the type goes muddy. A .ttc, so the
# weight is selected by index rather than by a variation name.
FONT_CAPTION = "/System/Library/Fonts/Supplemental/Futura.ttc"
FONT_CAPTION_INDEX = 0
FONT_CAPTION_SIZE = 44

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
    crop_w = int(round(crop_h * OUT_W / OUT_H))
    crop_w = min(crop_w, src_w)

    m = interest_map(proxy)
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
                    stroke: int = 0, max_w: int = TEXT_MAX_W) -> Path:
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

    `y_frac` is the centre of the text block as a fraction of frame height.
    `max_w` is the wrap width; captions run wider than the silent quote card,
    because a spoken phrase broken across two lines reads as two thoughts.
    """
    font = _load_font(font_path, size, font_index)

    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    lines = _wrap(probe, text, font, max_w)
    line_h = int(size * 1.34)
    block_h = line_h * len(lines)
    top = int(OUT_H * y_frac) - block_h // 2

    if stroke:
        img = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        y = top
        for ln in lines:
            w = d.textlength(ln, font=font)
            d.text(((OUT_W - w) / 2, y), ln, font=font, fill=(255, 255, 255, 255),
                   stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
            y += line_h
        img.save(out)
        return out

    dark_text = bg_luma > 0.62
    ink = (18, 18, 18, 255) if dark_text else (255, 255, 255, 255)
    halo = (255, 255, 255, 128) if dark_text else (0, 0, 0, 150)

    layer = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = top
    for ln in lines:
        w = d.textlength(ln, font=font)
        d.text(((OUT_W - w) / 2, y), ln, font=font, fill=ink)
        y += line_h

    # Soft halo from the glyphs themselves — reads as depth, not as a box.
    shadow = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    y = top
    for ln in lines:
        w = sd.textlength(ln, font=font)
        sd.text(((OUT_W - w) / 2, y + 2), ln, font=font, fill=halo)
        y += line_h
    shadow = shadow.filter(ImageFilter.GaussianBlur(7))

    img = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
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


EMOJI_FONT = "/System/Library/Fonts/Apple Color Emoji.ttc"
# Apple Color Emoji is a bitmap font and only loads at the sizes it has strikes
# for — 44 and 137 both raise "invalid pixel size". Render at 160 and scale
# down, which is the only size-independent way to use it.
EMOJI_STRIKE = 160


def add_caption_emoji(png: Path, text: str, char: str, size: int,
                      y_frac: float, font_path: str, font_index: int,
                      gap: int = 16) -> None:
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
    top = int(OUT_H * y_frac) - line_h // 2
    shifted.alpha_composite(
        emoji, (int((OUT_W - tw) / 2 - dx + tw + gap), top + (line_h - h) // 2))
    shifted.save(png)
