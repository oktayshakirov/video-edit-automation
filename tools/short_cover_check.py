"""Check 9:16 Short covers against TikTok's 3:4 profile-grid crop, any channel.

    PYTHONPATH=. .venv/bin/python tools/short_cover_check.py COVER.jpg [...]

TikTok's profile grid shows a 9:16 cover cut to 3:4: on a 1080x1920 cover the
top 240 px and the bottom 240 px are gone (the editor, 2026-11-25: "in tiktok
the thumbnails are shorter than youtube so we need to position them always in
a way that we dont crop the text and important graphics"). Headline, card,
subject and badges belong in the band between (`thumb.SAFE_TOP`,
`thumb.SAFE_BOTTOM`); only background, or the body below a face, may run out.

For each cover this flags headline colours (white type, red and yellow
plates) in the two outer bands and writes `<cover>-tiktok-crop.jpg` beside it: the full cover
with the crop lines, next to the 3:4 view TikTok shows. Look at that sheet
before any Short is uploaded or scheduled - TikTok refuses edits to a
scheduled post, so a cut cover means deleting the post and scheduling again.
Exit code 1 when any cover is flagged.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

# The share of a band's pixels in type and plate colours (near-white, the red
# and yellow plates) above which the band holds a headline or badge.
# Calibrated 2026-11-25 on the six OktAI Short covers: the safe layout's outer
# bands measured 0-0.06%, the same covers lifted 180 px into the old layout
# 13-20%. Hard edges were tried first and fail: a background grid is all edge.
INK_LIMIT = 0.02


def bands(h: int, w: int) -> tuple[int, int]:
    """(top, bottom) of the 3:4 band TikTok's grid keeps, for this cover."""
    keep = round(w * 4 / 3)
    top = max(0, (h - keep) // 2)
    return top, top + min(keep, h)


def ink_share(im: Image.Image) -> float:
    """Share of pixels in headline colours: near-white type, red or yellow plates."""
    if im.height < 1:
        return 0.0
    a = np.asarray(im.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    white = np.minimum(np.minimum(r, g), b) > 215
    red = (r > 170) & (g < 90) & (b < 90)
    yellow = (r > 210) & (g > 160) & (b < 70)
    return float((white | red | yellow).mean())


def check(path: Path) -> list[str]:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    top, bot = bands(h, w)
    problems = []
    for name, box in (("top", (0, 0, w, top)), ("bottom", (0, bot, w, h))):
        share = ink_share(im.crop(box))
        if share > INK_LIMIT:
            problems.append(f"{name} band ({box[1]}-{box[3]}px) holds type or "
                            f"plates ({share:.1%} of it) - TikTok's grid cuts it off")

    sheet = Image.new("RGB", (w + w + 40, h), (30, 30, 30))
    full = im.copy()
    d = ImageDraw.Draw(full)
    for y in (top, bot):
        d.line([(0, y), (w, y)], fill=(0, 220, 255), width=6)
    sheet.paste(full, (0, 0))
    sheet.paste(im.crop((0, top, w, bot)), (w + 40, top))
    out = path.with_name(path.stem + "-tiktok-crop.jpg")
    sheet.resize((sheet.width // 3, sheet.height // 3)).save(out, quality=85)
    return problems


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    bad = 0
    for a in argv:
        p = Path(a).expanduser()
        problems = check(p)
        if problems:
            bad += 1
            print(f"FLAG {p.name}")
            for x in problems:
                print(f"     {x}")
        else:
            print(f"ok   {p.name}")
    print(f"\nCrop sheets written beside each cover (*-tiktok-crop.jpg).")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
