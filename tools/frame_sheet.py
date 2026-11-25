"""Frames of a video at the given seconds, on one sheet, time-stamped.

    .venv/bin/python tools/frame_sheet.py VIDEO.mp4 OUT.png [--cols 4] T1 T2 ...

16:9 tiles are 480 px wide, 9:16 tiles 270 - the shape is read off the
video. Made for reviewing a build at the editor's timestamps.
"""

import argparse
import io
import json
import subprocess

from PIL import Image, ImageDraw, ImageFont


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("out")
    ap.add_argument("times", nargs="+", type=float)
    ap.add_argument("--cols", type=int, default=4)
    a = ap.parse_args()
    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", a.video],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    w = 270 if probe["height"] > probe["width"] else 480
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
    tiles = []
    for t in a.times:
        png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", a.video,
                              "-frames:v", "1", "-vf", f"scale={w}:-1", "-f", "image2pipe",
                              "-vcodec", "png", "-"], capture_output=True, check=True).stdout
        if not png:
            continue                    # past the end
        im = Image.open(io.BytesIO(png)).convert("RGB")
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 62, 24], fill=(0, 0, 0))
        d.text((4, 2), f"{t:.1f}", font=font, fill=(255, 220, 0))
        tiles.append(im)
    h = tiles[0].height
    cols = min(a.cols, len(tiles))
    rows = -(-len(tiles) // cols)
    sheet = Image.new("RGB", (cols * w, rows * h), (40, 40, 40))
    for k, im in enumerate(tiles):
        sheet.paste(im, ((k % cols) * w, (k // cols) * h))
    sheet.save(a.out)
    print(a.out)


if __name__ == "__main__":
    main()
