"""Render one stretch of an OktAI long form, to check a change before the
full build (2026-11-25, the editor: "just render 1 version of only this part
and I will verify it").

    PYTHONPATH=. .venv/bin/python tools/oktai_preview.py NAME [--section 0]
        [--from 0] [--to 9] [--speed 1.33]

Takes sentences `from`..`to` (exclusive) of one section of
`projects/oktai-long/NAME.py`, builds them with the recorded voice and
writes `~/Desktop/NAME-preview.mp4` - a minute, not a 25-minute render. The
full video, its subtitles and its report are untouched.

**The speed is the full video's.** A recording is sped up to
`oktai.TARGET_WPM` over the whole read, so a few lines alone come out at
another speed (1.21x against the full form's 1.17x). `--speed` pins it; by
default it is read off the full long form's last edit (`*.edl.json`) and
scaled to today's `TARGET_WPM` if that changed since.
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def _load(name: str):
    path = REPO / "projects/oktai-long" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _full_speed(name: str) -> float | None:
    """The speed the last full long form ran at: the rate of the edit list
    with the most segments next to the recording."""
    from video_automation.oktai import folder
    best = None
    for p in Path(folder(name)).glob("*.edl.json"):
        d = json.loads(p.read_text())
        segs = d if isinstance(d, list) else d.get("edl", d.get("segments", []))
        rates = [s["rate"] for s in segs if s.get("rate")]
        if rates and (best is None or len(segs) > best[0]):
            best = (len(segs), sum(rates) / len(rates), p.stat().st_mtime)
    return best[1] if best else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--section", type=int, default=0)
    ap.add_argument("--from", dest="start", type=int, default=0)
    ap.add_argument("--to", dest="end", type=int, default=None)
    ap.add_argument("--speed", type=float, default=None)
    a = ap.parse_args()

    L = _load(a.name)
    import video_automation.oktai.build as B
    speed = a.speed or _full_speed(a.name)
    if speed:
        rec = B.recording

        def fixed(*args, **kw):
            r = rec(*args, **kw)
            if r is not None:
                r.target_wpm, r.speed = None, speed
            return r
        B.recording = fixed
        print(f"preview: voice at {speed:.3f}x, the full video's")

    sec = copy.deepcopy(L.SECTIONS[a.section])
    end = a.end if a.end is not None else len(sec.sentences)
    sl = slice(a.start, end)
    sec.sentences, sec.shots = sec.sentences[sl], sec.shots[sl]
    if sec.gaps:
        sec.gaps = sec.gaps[sl]
    if a.start:                      # no chapter way in mid-section
        sec.lead, sec.lead_shot = None, None
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["OKTAI_OUT"] = tmp
        B.DESKTOP = Path(tmp)
        made = B.build_long([sec], L.NAME, face=[], hook=None, meta=L.META,
                            emblem="microphone", window=getattr(L, "WINDOW", None),
                            pins=getattr(L, "PINS", None), drops=getattr(L, "DROPS", None),
                            last=None)
        out = Path.home() / "Desktop" / f"{L.NAME}-preview.mp4"
        shutil.copy(made["video"], out)
    print(out)


if __name__ == "__main__":
    main()
