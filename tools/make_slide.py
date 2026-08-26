"""Compose a diagram onto a frame-sized slide, so it can never be cropped.

**Why this exists rather than a `Shot` parameter.** Both skills ban an
infographic from a full-frame Ken Burns shot, because the move crops the
diagram's own title off the top and its last row off the bottom. The ban is
about the *move*, so the obvious fix is a still shot — `zoom=1.0`, no pan, the
source's own aspect — and that is what the proof-of-stake cut tried first. It
still shipped with the title clipped.

The reason is the cover/fit boundary. `PhotoShot` scales a picture to *cover*
the frame and only falls back to a fitted panel when the source cannot reach
that size under `max_upscale`. The site's diagram is 1000x667: covering 1920
needs 1.92x against a 1.90 ceiling, which is close enough that the renderer
filled the width and then cropped ~90px off each of the top and bottom to make
the height fit. A source a little smaller would have rendered fitted; a source
a little larger would have covered cleanly. This one landed in the gap.

So the diagram is composited onto a 1920x1080 canvas **once**, ahead of the
render. The asset then bleeds off all four edges by construction, no crop is
possible, and it picks up a margin and the brand hairline on the way — which is
what a diagram wants anyway, since a diagram read at frame edges is a diagram
with nowhere to breathe.

    .venv/bin/python tools/make_slide.py \\
        ~/Coding/crypto-wiki/public/images/posts/proof-of-stake.jpg \\
        assets/brand/slides/proof-of-stake-slide.jpg --brand crypto
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw

from video_automation.core.brand import CRYPTO, TINNITUS
from video_automation.core.frame import LANDSCAPE

BRANDS = {"crypto": CRYPTO, "tinnitus": TINNITUS}


def border_colour(im: Image.Image, band: int = 24) -> tuple[int, int, int]:
    """The median colour of the source's outer border.

    **A canvas in the brand background does not always blend.** The GPU
    thumbnail's vertical slide shipped with a visible lighter rectangle where
    the photograph sat, because the photo's own surround is nearly black while
    `CRYPTO.bg` is a dark grey — two flat darks that read as one shape with a
    seam through it. Sampling the picture's own edge makes the join invisible
    without needing the photo to fill the frame.
    """
    import statistics
    px = []
    w, h = im.size
    for x in range(0, w, max(1, w // 64)):
        px.append(im.getpixel((x, 0)))
        px.append(im.getpixel((x, h - 1)))
    for y in range(0, h, max(1, h // 64)):
        px.append(im.getpixel((0, y)))
        px.append(im.getpixel((w - 1, y)))
    return tuple(int(statistics.median(c[i] for c in px)) for i in range(3))


def make_slide(src: Path, out: Path, brand=CRYPTO,
               frame=LANDSCAPE, margin: float = 0.06,
               rule: bool = True, bg: str = "brand") -> Path:
    """Centre `src` on a frame-sized canvas.

    `bg` is "brand" (the brand's own background — right for a diagram, which
    is a graphic sitting on the channel's ground) or "auto" (the source's own
    border colour — right for a photograph, where any mismatch shows as a
    rectangle around the picture).
    """
    im = Image.open(src).convert("RGB")
    w, h = frame.w, frame.h
    ground = border_colour(im) if bg == "auto" else brand.bg
    canvas = Image.new("RGB", (w, h), ground)

    # Fit inside the margins on both axes — never cover, never crop.
    s = min((h * (1 - 2 * margin)) / im.height,
            (w * (1 - 2 * margin)) / im.width)
    im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))),
                   Image.LANCZOS)
    x, y = (w - im.width) // 2, (h - im.height) // 2
    canvas.paste(im, (x, y))
    if rule:
        ImageDraw.Draw(canvas).rectangle(
            [x - 1, y - 1, x + im.width, y + im.height],
            outline=brand.primary, width=3)

    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=95)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--brand", default="crypto", choices=sorted(BRANDS))
    ap.add_argument("--margin", type=float, default=0.06)
    ap.add_argument("--bg", default="brand", choices=("brand", "auto"),
                    help="auto samples the source's own border colour")
    ap.add_argument("--no-rule", action="store_true")
    a = ap.parse_args()
    p = make_slide(a.src, a.out, brand=BRANDS[a.brand], margin=a.margin,
                   rule=not a.no_rule, bg=a.bg)
    print(p, Image.open(p).size)


if __name__ == "__main__":
    main()
