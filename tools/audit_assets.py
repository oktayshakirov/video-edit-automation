"""Preflight for a shot list: asset reuse across videos, and clip arithmetic.

Two faults kept costing a full twelve-minute render to discover, and both are
answerable statically:

1. **A clip too short for the slot it is given.** `VideoShot` will not stretch
   past 1.33x, so a shot needs `clip_at + shot_length` to fit inside the file.
   `server-racks-blue-light-dark` (9.2s, `clip_at` up to 12.0) and
   `dominoes-falling-dark` (10.0s at `clip_at=7.5`) each killed a build.
2. **An asset already used by another video.** The channel was found recycling
   a pool of ~15 files across six videos — `security-combination-lock.jpg` in
   nine of them — which is the templated sameness the strategy doc says gets a
   channel suppressed.

Neither needs the narration to be synthesised, so both are cheap:

    .venv/bin/python tools/audit_assets.py                 # whole channel
    .venv/bin/python tools/audit_assets.py proof-of-stake  # one video

`HEADROOM` is deliberately generous. The real requirement is the *longest shot
in this video*, which is not known until the voice is measured, so the check
uses a fixed budget that comfortably covers a long sentence instead.
"""

from __future__ import annotations

import collections
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOCK = ROOT / "assets/stock"
PROJECTS = ROOT / "projects"

HEADROOM = 8.0          # seconds a clip must have left after `clip_at`
MAX_USES = 2            # per video, per asset
MIN_APART = 5           # slots between two uses of one clip

# Brand-level assets that are *meant* to recur in every video.
EXEMPT = {"subscribe"}


def duration(path: Path) -> float | None:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True).stdout.strip()
        return float(out)
    except Exception:
        return None


def assets_of(src: str) -> dict[str, str]:
    """name -> relative stock path, from the module-level constants."""
    return dict(re.findall(r'^(\w+) = (?:STOCK|PH) / "([^"]+)"', src, re.M))


def audit(path: Path) -> list[str]:
    src = path.read_text()
    names = assets_of(src)
    problems: list[str] = []

    slots = [(m.group(1), float(m.group(2)))
             for m in re.finditer(r"clip=(\w+), clip_at=([\d.]+)", src)]
    uses: dict[str, list[int]] = collections.defaultdict(list)
    for i, (name, at) in enumerate(slots):
        uses[name].append(i)
        rel = names.get(name)
        if not rel:
            continue
        p = STOCK / rel if not rel.startswith("photos") else STOCK / rel
        d = duration(p)
        if d is None:
            problems.append(f"{name}: cannot probe {rel}")
        elif d - at < HEADROOM:
            problems.append(
                f"{name}@{at} has only {d - at:.1f}s left of {d:.1f}s "
                f"(want >={HEADROOM:.0f}s) - the render will refuse it")

    for name, idxs in uses.items():
        if len(idxs) > MAX_USES:
            problems.append(f"{name} used {len(idxs)}x (max {MAX_USES})")
        for a, b in zip(idxs, idxs[1:]):
            if b - a < MIN_APART:
                problems.append(
                    f"{name} reused only {b - a} slots apart (want >={MIN_APART})")
    return problems


def channel_reuse(prefix: str = "crypto") -> dict[tuple[str, str], list[str]]:
    """Which assets appear in more than one video."""
    use: dict[tuple[str, str], list[str]] = collections.defaultdict(list)
    for p in sorted(PROJECTS.rglob("*.py")):
        if "__pycache__" in str(p) or prefix not in str(p):
            continue
        video = p.stem   # a long/short pair from one post is one video
        src = p.read_text()
        for rel in re.findall(r'(?:STOCK|PH) / "([^"]+)"', src):
            folder = rel.split("/")[1] if rel.startswith(("videos/", "photos/")) else rel
            if folder in EXEMPT:
                continue
            use[("stock", folder)].append(video)
        for rel in re.findall(r'POSTS / "([^"]+)"', src):
            use[("site", rel)].append(video)
    return use


def main() -> int:
    argv = sys.argv[1:]
    bad = 0

    targets = [p for p in PROJECTS.rglob("*.py")
               if "__pycache__" not in str(p) and (not argv or argv[0] in p.stem)]
    for p in sorted(targets):
        probs = audit(p)
        if probs:
            bad += len(probs)
            print(f"\n{p.relative_to(ROOT)}")
            for x in probs:
                print(f"  ! {x}")

    if not argv:
        print("\nassets shared by more than one crypto video:")
        shared = {k: v for k, v in channel_reuse().items() if len(set(v)) > 1}
        for (kind, a), vids in sorted(shared.items(),
                                      key=lambda kv: -len(set(kv[1]))):
            print(f"  {len(set(vids)):2d}x {kind:5s} {a}")
        if not shared:
            print("  (none)")

    print(f"\n{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
