"""Fetch stock clips for a few queries, screen them, and draw a contact sheet.

The step every build does by hand before writing a shot list (`footage.md`):
fetch, drop anything another video already uses, measure brightness across
the clip, and look at it at 15/50/85% before trusting the folder name.

Two luma readings per clip, at 0.5/3/6/9s:

- `L` - the whole frame, as `stock.screen` always measured it;
- `B` - the set only, the person masked out (`screen(background=True)`).

**Screen on `B`.** A pale face on a dark set reads brighter on `L` than a
dark face on the same set, so screening on `L` quietly picked the casting
(`footage.md`, "Screening for brightness is not screening for who is in the
shot"). `B` asks the question the box was for - is this a dark picture.
Who is in the clip is then judged by eye on the sheet, against the rest of
the video's casting.

    PYTHONPATH=. .venv/bin/python tools/stock_sheet.py OUT.jpg "query one" "query two"
    PYTHONPATH=. .venv/bin/python tools/stock_sheet.py OUT.jpg --clips folder/123.mp4 ...
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from video_automation.core import stock

ROOT = Path(__file__).resolve().parents[1]
V = stock.CACHE / "videos"


def used_ids() -> set[str]:
    """Pexels ids any project script already names - unavailable here."""
    ids = set()
    for f in (ROOT / "projects").rglob("*.py"):
        ids |= set(re.findall(r'/(\d{5,})\.mp4', f.read_text()))
    return ids


def _dur(p: Path) -> float:
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)]))


def readings(p: Path) -> tuple[list[int], list[int], int]:
    d = _dur(p)
    ts = [t for t in (0.5, 3, 6, 9) if t < d]
    whole = [round(stock.screen(p, at=t)[0]) for t in ts]
    bg = [round(stock.screen(p, at=t, background=True)[0]) for t in ts]
    return whole, bg, round(stock.screen(p, at=1.0, background=True)[1])


def sheet(clips: list[str], out: Path, notes: dict[str, str]) -> Path:
    W, H = 400, 225
    im = Image.new("RGB", (W * 3, (H + 26) * len(clips)), (40, 40, 40))
    d = ImageDraw.Draw(im)
    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 17)
    for i, c in enumerate(clips):
        p, dur = V / c, _dur(V / c)
        for j, fr in enumerate((0.15, 0.5, 0.85)):
            tmp = Path(tempfile.mktemp(suffix=".jpg"))
            subprocess.run(["ffmpeg", "-v", "error", "-ss", str(dur * fr), "-i",
                            str(p), "-frames:v", "1", "-vf", f"scale={W}:{H}",
                            "-strict", "unofficial", str(tmp)], check=True)
            im.paste(Image.open(tmp), (j * W, i * (H + 26) + 26))
            tmp.unlink()
        d.text((6, i * (H + 26) + 3), f"{i}: {c}  {dur:.0f}s  {notes.get(c, '')}",
               fill=(255, 220, 120), font=font)
    im.save(out, quality=80)
    return out


def main(argv: list[str]) -> None:
    out = Path(argv[0])
    clips: list[str] = []
    if argv[1:2] == ["--clips"]:
        clips = argv[2:]
    else:
        used = used_ids()
        for q in argv[1:]:
            for a in stock.videos(q, n=4):
                rel = f"{a.path.parent.name}/{a.path.name}"
                if a.path.stem in used:
                    print(f"used elsewhere  {rel}")
                    continue
                clips.append(rel)
    notes = {}
    for c in clips:
        whole, bg, sat = readings(V / c)
        ok = max(bg) <= stock.MAX_LUMA and sat <= stock.MAX_SAT
        notes[c] = f"B{bg}"
        print(f"{'ok  ' if ok else 'over'}  {c:66s} L{whole} B{bg} S{sat}")
    print(sheet(clips, out, notes))


if __name__ == "__main__":
    main(sys.argv[1:])
