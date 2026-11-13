"""Log a built video in the ledger the reviews read: one row per video.

    PYTHONPATH=. .venv/bin/python tools/video_log.py projects/crypto-long/x.py projects/crypto-short/x.py
    PYTHONPATH=. .venv/bin/python tools/video_log.py --print projects/crypto-long/x.py

The ledger is `.claude/skills/video-performance-review/videos.md`. A build
run appends its rows at the handoff (`workflow.md` step 5); a review run
fills in the result and the verdict. The point is one place that says, per
video, *how it was built* and *how it did* - so the next topic and the next
script are chosen from what worked, not from memory.

The build tags are read from the script, never typed: how much of it is
drawn, which beats, which opener, the cover style, the voice, the demand
evidence. A row is written once; running this again on a logged script
changes nothing unless `--replace` is given.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))
import script_check as sc                                   # noqa: E402

LEDGER = REPO / ".claude/skills/video-performance-review/videos.md"
MARK = "<!-- rows: newest last; tools/video_log.py appends here -->"


def tags(path: Path) -> dict:
    s = sc.load(path)
    shots = sc.shots_of(s.mod)
    n = len(shots) or 1
    drawn = sum(1 for sh in shots if not sc.is_full_frame(sh))
    stock = sum(1 for sh in shots if sc.is_plain_stock(sh))
    beats = []
    for sh in shots:
        g = getattr(sh, "graphic", None)
        if g and g != "chapter" and g not in beats:
            beats.append(g)
    src = path.read_text(errors="replace")
    doc = getattr(s.mod, "__doc__", "") or ""
    code = src.replace(doc, "", 1)
    # `opener=Stamp(` inline, or `OPENER = Stamp(` at module level.
    m = re.search(r"opener\s*=\s*([A-Z][A-Za-z]+)\(", code, re.I)
    demand = getattr(s.mod, "DEMAND", None)
    return {
        "date": dt.date.today().isoformat(),
        "channel": s.channel, "fmt": s.fmt, "slug": path.stem,
        "source": getattr(s.mod, "SOURCE_POST", None) or "-",
        "demand": (demand[:70] + "...") if demand and len(demand) > 73
                  else (demand or "no evidence"),
        "drawn": f"{drawn}/{n}", "stock": f"{stock}/{n}",
        "beats": ", ".join(beats) or "-",
        "opener": m.group(1) if m else "-",
        "cover": getattr(s.mod, "COVER_STYLE", None) or "-",
        "voice": getattr(s.mod, "VOICE", None) or "-",
    }


def row(t: dict) -> str:
    build = (f"drawn {t['drawn']}, stock {t['stock']}; {t['beats']}; "
             f"opener {t['opener']}; cover {t['cover']}; voice {t['voice']}")
    return (f"| {t['date']} | {t['channel']} {t['fmt']} | `{t['slug']}` | "
            f"{t['demand'].replace('|', '/')} | {build} | - | too early | - |")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="+", type=Path)
    ap.add_argument("--print", action="store_true", dest="show",
                    help="print the rows, write nothing")
    ap.add_argument("--replace", action="store_true",
                    help="rewrite the row of a script already logged")
    a = ap.parse_args()
    text = LEDGER.read_text() if LEDGER.exists() else ""
    out = []
    for p in a.paths:
        t = tags(p.resolve())
        key = f"| {t['channel']} {t['fmt']} | `{t['slug']}` |"
        r = row(t)
        if a.show:
            print(r)
            continue
        old = next((ln for ln in text.splitlines() if key in ln), None)
        if old and not a.replace:
            print(f"already logged: {t['channel']} {t['fmt']} {t['slug']}")
            continue
        if old:
            # keep the date, the result, the verdict and the lesson
            cells = old.split(" | ")
            new = r.split(" | ")
            new[0] = cells[0]
            new[-3:] = cells[-3:]
            text = text.replace(old, " | ".join(new))
        else:
            out.append(r)
    if a.show:
        return
    if MARK not in text:
        sys.exit(f"{LEDGER} has no row marker - not writing")
    if out:
        text = text.rstrip("\n") + "\n" + "\n".join(out) + "\n"
    LEDGER.write_text(text)
    for r in out:
        print("logged:", r[:110])


if __name__ == "__main__":
    main()
