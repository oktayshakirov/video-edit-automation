"""Generate an oscillating-index band: a value wandering between two named zones.

**Why this is a generated asset and not a beat.** The drawn beats all animate
against the voice, and this is the one graphic that must *not* — it is a
history, so the whole shape has to be on screen at once for "again and again,
cycle after cycle" to mean anything. A beat that revealed it left to right
would be drawing a prediction, one peak at a time, which is the opposite of
the claim. It is also the second thing `assets/brand/graphics/` exists for,
after `rug-pull-chart.png`: a picture of a shape, composed once, with nothing
tradeable named in it.

**It is not a price chart, and the difference is load-bearing.** Both sites'
scripts refuse to show a price, a ticker, a broker or a live chart - see the
crypto project doc. What this draws is a *sentiment* index between a floor and
a ceiling it can never leave, with its zones labelled in words rather than an
axis in numbers. There is no instrument here to buy.

    .venv/bin/python tools/make_wave.py \\
        assets/brand/graphics/fear-greed-wave.png --brand crypto

`--vertical` writes the 1080x1920 cut instead, for a 9:16 shot.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

from video_automation.core.brand import CRYPTO, TINNITUS

BRANDS = {"crypto": CRYPTO, "tinnitus": TINNITUS}
SS = 2                                  # supersample; PIL will not antialias

FEAR = (248, 80, 50)                    # the site's own band colours
GREED = (86, 171, 48)


def series(n: int, seed: int = 7) -> list[float]:
    """A 0..1 walk that visits both extremes without looking periodic.

    Three sines at unrelated periods plus a little noise. A single sine reads
    as a decoration rather than as a record of anything, and pure noise reads
    as static - what a sentiment history actually looks like is a slow swing
    with faster wobble riding on it.
    """
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x = i / (n - 1)
        v = (0.50
             + 0.30 * math.sin(x * math.pi * 3.1 + 0.4)
             + 0.13 * math.sin(x * math.pi * 7.7 + 1.9)
             + 0.05 * math.sin(x * math.pi * 17.3))
        v += rnd.uniform(-0.012, 0.012)
        out.append(max(0.04, min(0.96, v)))
    return out


def make_wave(out: Path, brand=CRYPTO, w: int = 1920, h: int = 1080,
              seed: int = 7) -> Path:
    im = Image.new("RGB", (w * SS, h * SS), brand.bg)
    d = ImageDraw.Draw(im, "RGBA")
    W, H = w * SS, h * SS

    # The plot sits in the middle band of the frame, so a caption or a
    # payload line above it has somewhere to go.
    top, bot = int(H * 0.22), int(H * 0.78)
    left, right = int(W * 0.07), int(W * 0.93)
    span = bot - top

    # The two zones, as shaded regions rather than gridlines. A quarter of the
    # range at each end, which is where the index's own "extreme" bands sit.
    d.rectangle([left, top, right, top + span * 0.25], fill=GREED + (40,))
    d.rectangle([left, bot - span * 0.25, right, bot], fill=FEAR + (40,))

    # The midline, dashed - the only reference the picture needs.
    mid = top + span * 0.5
    x = left
    while x < right:
        d.line([(x, mid), (min(x + 26 * SS, right), mid)],
               fill=brand.ink + (70,), width=2 * SS)
        x += 46 * SS

    pts = series(260, seed)
    xy = [(left + (right - left) * i / (len(pts) - 1), bot - span * v)
          for i, v in enumerate(pts)]

    # A soft glow under the line, so it reads as lit rather than as ink on a
    # dark ground - the same reason the beats' type sits on a blurred shadow.
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).line(xy, fill=brand.primary + (90,), width=18 * SS,
                              joint="curve")
    im.paste(Image.alpha_composite(
        im.convert("RGBA"), glow.filter(ImageFilter.GaussianBlur(14 * SS))
    ).convert("RGB"), (0, 0))

    d = ImageDraw.Draw(im, "RGBA")
    d.line(xy, fill=brand.primary + (255,), width=6 * SS, joint="curve")

    # **The zones are named, and that is not decoration.** An unlabelled line
    # wandering between a red floor and a green ceiling is exactly what a
    # price chart looks like, and this channel shows no price, chart or
    # ticker at all. Two words in each band make it unmistakably a sentiment
    # scale, which is the one thing it is allowed to be.
    from video_automation.longform.beats import _font
    fnt = _font(34 * SS)
    d.text((left + 26 * SS, top + 22 * SS), "EXTREME GREED", font=fnt,
           fill=GREED + (215,))
    d.text((left + 26 * SS, bot - span * 0.25 + 22 * SS), "EXTREME FEAR",
           font=fnt, fill=FEAR + (215,))

    im = im.resize((w, h), Image.LANCZOS)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=95)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("out", type=Path)
    ap.add_argument("--brand", default="crypto", choices=sorted(BRANDS))
    ap.add_argument("--vertical", action="store_true")
    ap.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    w, h = (1080, 1920) if a.vertical else (1920, 1080)
    p = make_wave(a.out, brand=BRANDS[a.brand], w=w, h=h, seed=a.seed)
    print(p, Image.open(p).size)


if __name__ == "__main__":
    main()
