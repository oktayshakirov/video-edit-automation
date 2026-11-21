"""Draw the OktAI brand assets: the wordmark and the night-sky backdrop.

    .venv/bin/python tools/oktai_brand.py            # both
    .venv/bin/python tools/oktai_brand.py wordmark
    .venv/bin/python tools/oktai_brand.py backdrop

The look is the portfolio's (oktayshakirov.com): a near-black night sky,
light grey type, one gold gradient. "okt" in white, "AI" in the gold, in
Poppins SemiBold - the portfolio's own font files, copied into
`assets/brand/oktai/fonts` (Poppins is SIL Open Font Licence).

The wordmark is a stand-in until the logo from ChatGPT arrives
(`docs/oktai-brand-prompts.md`); `core.brand.OKTAI.logo` points at this file
either way, so swapping the PNG is the whole change.

**The backdrop is sparse on purpose.** The portfolio's sky is full of stars,
but `tinnitus-galaxy` was rejected as a background because a starfield is
high-frequency detail behind type. So this is the portfolio's sky turned down:
the near-black base, one soft gold bloom and one cool bloom drifting on closed
circles (`backdrop.aurora`), and a few dozen dim stars that twinkle on integer
cycles so the 12 s loop is seamless.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from video_automation.core import backdrop  # noqa: E402

BRAND_DIR = ROOT / "assets/brand/oktai"
FONT = BRAND_DIR / "fonts/poppins-600.woff2"
WORDMARK = BRAND_DIR / "wordmark.png"
BACKDROP = backdrop.BACKGROUNDS / "oktai-night.mp4"

WHITE = (255, 255, 255)
GOLD_A = (255, 219, 112)      # hsl(45, 100%, 72%) - the portfolio's accent
GOLD_B = (255, 192, 92)       # hsl(35, 100%, 68%) - the gradient's far end

NIGHT = dict(
    base=(6, 6, 9),           # between #050507 and #0a0a0f
    blobs=[
        # cx,   cy,   r,    turns, phase, colour,          strength, sigma
        (0.62, 0.40, 0.16,  1,     0.00,  (255, 200, 110), 0.060,    0.26),
        (0.30, 0.66, 0.18,  1,     0.50,  (40, 44, 70),    0.300,    0.32),
        (0.50, 0.50, 0.10,  2,     0.25,  (26, 26, 36),    0.400,    0.45),
    ],
)
STARS = 70                    # on a 512 square, so ~1 per 3700 px
STAR_PEAK = 0.34              # brightest a star gets, of white


def wordmark(height: int = 220) -> Path:
    """'okt' white + 'AI' gold gradient, transparent, trimmed."""
    font = ImageFont.truetype(str(FONT), height)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    w1 = probe.textlength("okt", font=font)
    w2 = probe.textlength("AI", font=font)
    pad = height // 4
    W, H = int(w1 + w2 + 2 * pad), int(height * 1.5)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((pad, pad // 2), "okt", font=font, fill=WHITE + (255,))

    # The AI as a mask, filled with a left-to-right gradient.
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).text((pad + w1, pad // 2), "AI", font=font, fill=255)
    x = np.linspace(0, 1, W, dtype=np.float32)[None, :, None]
    a = np.array(GOLD_A, np.float32)
    b = np.array(GOLD_B, np.float32)
    lo, hi = (pad + w1) / W, (pad + w1 + w2) / W
    t = np.clip((x - lo) / max(hi - lo, 1e-6), 0, 1)
    grad = (a + (b - a) * t).repeat(H, axis=0)
    gold = Image.fromarray(grad.astype(np.uint8), "RGB").convert("RGBA")
    gold.putalpha(mask)
    im.alpha_composite(gold)
    im = im.crop(im.getbbox())
    WORDMARK.parent.mkdir(parents=True, exist_ok=True)
    im.save(WORDMARK)
    return WORDMARK


def _stars(size: int, seed: int = 21):
    rng = np.random.default_rng(seed)
    xy = rng.uniform(0.04, 0.96, (STARS, 2)) * size
    peak = rng.uniform(0.35, 1.0, STARS) * STAR_PEAK
    turns = rng.integers(1, 4, STARS)          # integer: the loop closes
    phase = rng.uniform(0, 1, STARS)
    big = rng.uniform(0, 1, STARS) > 0.85      # a few slightly larger
    return xy, peak, turns, phase, big


def night_frame(t: float, size: int, stars) -> np.ndarray:
    out = backdrop.aurora(t, size, NIGHT["base"], NIGHT["blobs"])
    xy, peak, turns, phase, big = stars
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    for (sx, sy), p, n, ph, b in zip(xy, peak, turns, phase, big):
        tw = 0.55 + 0.45 * np.cos(2 * np.pi * (n * t / backdrop.LOOP + ph))
        r0, r1 = int(sy) - 4, int(sy) + 5
        c0, c1 = int(sx) - 4, int(sx) + 5
        d2 = (x[r0:r1, c0:c1] - sx) ** 2 + (y[r0:r1, c0:c1] - sy) ** 2
        sigma = 0.9 if b else 0.6
        out[r0:r1, c0:c1] += (p * tw * np.exp(-d2 / (2 * sigma ** 2)))[..., None]
    return np.clip(out, 0, 1)


def night(size: int = backdrop.SIZE, seconds: float = backdrop.LOOP,
          fps: int = backdrop.FPS) -> Path:
    """The looping backdrop, same format as every other generated one."""
    stars = _stars(size)
    n = int(round(seconds * fps))
    BACKDROP.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{size}x{size}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-crf", "14", "-preset", "slow",
         "-pix_fmt", "yuv420p", str(BACKDROP)], stdin=subprocess.PIPE)
    for i in range(n):
        frame = night_frame(i / fps, size, stars)
        proc.stdin.write((frame * 255).astype(np.uint8).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError(f"ffmpeg failed writing {BACKDROP}")
    return BACKDROP


def main() -> None:
    what = sys.argv[1:] or ["wordmark", "backdrop"]
    if "wordmark" in what:
        print(wordmark())
    if "backdrop" in what:
        print(night())


if __name__ == "__main__":
    main()
