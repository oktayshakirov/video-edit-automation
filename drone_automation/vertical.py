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
from PIL import Image, ImageDraw, ImageFont

OUT_W, OUT_H = 1080, 1920
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

# TikTok and Shorts overlay their own UI on the bottom band and right edge.
# Text lives above that, below centre.
TEXT_TOP = 1120
TEXT_MAX_W = 900


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


def _wrap(draw, text, font, max_w):
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
    return lines


def render_text_png(text: str, out: Path, size: int = 66) -> Path:
    """Text card with a scrim behind it.

    The channel's recurring legibility failure is light type over bright sky,
    which disappears at feed size. A gradient scrim plus a drop shadow keeps it
    readable over a blown-out sunset, which most of this footage is.
    """
    img = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, size)
    lines = _wrap(draw, text, font, TEXT_MAX_W)
    line_h = int(size * 1.28)
    block_h = line_h * len(lines)

    # Gradient scrim: transparent well above the text, ~62% opaque under it.
    scrim_top = max(TEXT_TOP - 220, 0)
    scrim_bot = min(TEXT_TOP + block_h + 220, OUT_H)
    grad = Image.new("RGBA", (OUT_W, scrim_bot - scrim_top), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    span = grad.height
    for i in range(span):
        a = int(158 * min(1.0, (i / span) * 1.9))
        gd.line([(0, i), (OUT_W, i)], fill=(0, 0, 0, a))
    img.alpha_composite(grad, (0, scrim_top))

    y = TEXT_TOP
    for ln in lines:
        w = draw.textlength(ln, font=font)
        x = (OUT_W - w) / 2
        draw.text((x + 3, y + 3), ln, font=font, fill=(0, 0, 0, 170))   # shadow
        draw.text((x, y), ln, font=font, fill=(255, 255, 255, 255))
        y += line_h

    img.save(out)
    return out


def render_short(src: Path, out: Path, start: float, duration: float,
                 box: tuple[int, int, int, int], text_png: Path | None = None,
                 fade_out: float = 0.4) -> Path:
    """Cut, crop to 9:16, scale to 1080x1920, burn the text card, drop audio."""
    x, y, w, h = box
    crop = f"crop={w}:{h}:{x}:{y},scale={OUT_W}:{OUT_H}:flags=lanczos"
    fade = f",fade=t=out:st={max(duration - fade_out, 0):.2f}:d={fade_out}"
    if text_png:
        vf = f"[0:v]{crop}[v];[v][1:v]overlay=0:0{fade}[o]"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-t", f"{duration}",
               "-i", str(src), "-i", str(text_png),
               "-filter_complex", vf, "-map", "[o]"]
    else:
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start}", "-t", f"{duration}",
               "-i", str(src), "-vf", crop + fade]
    cmd += ["-an", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out
