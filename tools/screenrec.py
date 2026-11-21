"""Record the Mac screen for a video, and preview the auto-zoomed cut.

    PYTHONPATH=. .venv/bin/python tools/screenrec.py record NAME FILE [--secs N]
    PYTHONPATH=. .venv/bin/python tools/screenrec.py render NAME FILE [--vertical]
        [--zoom 1.8] [--idle 4] [--crop x0,y0,x1,y1] [--blur x0,y0,x1,y1 ...]

`record` saves `~/Movies/OktAI/NAME/screens/FILE.mov` and, beside it,
`FILE.events.json` - the cursor, and *when* each click, key press and scroll
happened (never which key). Three seconds to get ready, then it records the
whole main screen until Ctrl+C. The terminal running it needs Screen
Recording permission once (System Settings > Privacy & Security).

`render` makes the cut a video will use - idle sped up, the camera zoomed to
the work, click ripples, private areas blurred - and a contact sheet, and
prints both paths. A project does this itself through `oktai.screen()`; this
is for looking before writing the script around it. Coordinates are
fractions of the screen: `--crop 0,0.08,1,1` drops a browser's tab bar,
`--blur 0.7,0,1,0.05` hides the menu-bar clock and icons.

NAME may also be a path to a recording anywhere.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from video_automation.core import screenrec  # noqa: E402
from video_automation.oktai import folder  # noqa: E402


def _src(name: str, file: str | None) -> Path:
    p = Path(name).expanduser()
    if p.suffix and p.exists():
        return p
    d = folder(name) / "screens"
    for ext in (".mov", ".mp4", ".m4v"):
        if (d / f"{file}{ext}").exists():
            return d / f"{file}{ext}"
    raise SystemExit(f"no {d}/{file}.mov")


def _box(text: str) -> tuple:
    v = tuple(float(x) for x in text.split(","))
    if len(v) not in (4, 6):
        raise argparse.ArgumentTypeError("x0,y0,x1,y1 or x0,y0,x1,y1,t0,t1")
    return v


def record(a) -> int:
    out = folder(a.name) / "screens" / f"{a.file}.mov"
    if out.exists() and not a.force:
        print(f"{out} exists - pick another name or pass --force")
        return 1
    print(f"recording the screen to {out}")
    print("close anything private first: mail, messages, keys, balances")
    for i in (3, 2, 1):
        print(f"  {i}...", flush=True)
        time.sleep(1)
    print("RECORDING - Ctrl+C to stop" + (f" (or {a.secs:g}s)" if a.secs else ""),
          flush=True)
    screenrec.record(out, secs=a.secs)
    ev = json.loads(screenrec.events_path(out).read_text())
    W, H, dur = screenrec.probe(out)
    print(f"saved {out.name}: {dur:.1f}s at {W}x{H}, {len(ev['clicks'])} clicks, "
          f"{len(ev['keys'])} key presses, {len(ev['scrolls'])} scroll ticks")
    print(f"preview: tools/screenrec.py render {a.name} {a.file}")
    return 0


def render(a) -> int:
    src = _src(a.name, a.file)
    spec = screenrec.Spec(src, vertical=a.vertical, zoom=a.zoom, idle=a.idle,
                          crop=a.crop, blur=tuple(a.blur or ()))
    out = spec.out()
    if out.exists() and not a.force:
        print(f"cached: {out}")
    else:
        screenrec.render(spec, out)
    info = json.loads(out.with_suffix(".json").read_text())
    print(f"{info['seconds_in']}s recorded -> {info['seconds_out']}s cut, "
          f"zoomed in {info['zoomed_share']:.0%} of it"
          + ("" if info["log"] else " (no event log: following screen changes)"))
    sheet = out.with_suffix(".sheet.png")
    n = max(1, int(info["seconds_out"] * screenrec.FPS))
    picks = "+".join(f"eq(n\\,{int(n * k / 12)})" for k in range(12))
    tile, w = ("6x2", 320) if a.vertical else ("3x4", 640)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-vf",
                    f"select='{picks}',scale={w}:-1,tile={tile}", "-frames:v",
                    "1", str(sheet)], check=True)
    print(out)
    print(sheet)
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record")
    r.add_argument("name")
    r.add_argument("file")
    r.add_argument("--secs", type=float)
    r.add_argument("--force", action="store_true")
    v = sub.add_parser("render")
    v.add_argument("name")
    v.add_argument("file", nargs="?")
    v.add_argument("--vertical", action="store_true")
    v.add_argument("--zoom", type=float)
    v.add_argument("--idle", type=float, default=4.0)
    v.add_argument("--crop", type=_box)
    v.add_argument("--blur", type=_box, action="append")
    v.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    return record(a) if a.cmd == "record" else render(a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
