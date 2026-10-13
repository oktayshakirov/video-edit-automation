"""Drop render work folders nobody is going to open again.

Every build renders through a scratch folder on the Desktop - `.<name>-work`
for the article builds, `.work-<name>` for drone, glitch and quiz shorts - full
of per-run wavs, caption sprites, proxies and a `picture.mp4`. The article
builds delete theirs on success; a failed or interrupted render leaves it
behind, and the drone and glitch scripts never delete theirs at all. On
2026-10-14 there were 21 of them holding **6.5 GB**, the oldest from August,
most of them for a video long since published or abandoned.

None of it is source. The script is committed, the narration is cached in
`~/.cache/video-automation/narration`, and stock is re-fetchable from
`assets/stock/manifest.json` - so a work folder is only worth keeping while
someone is still re-cutting that video. **Age is the test**: a folder whose
newest file is older than `--days` (default 3) is dropped. A re-cut loop
touches its folder every run, so an active one is never old.

    .venv/bin/python tools/prune_work.py              # report, delete nothing
    .venv/bin/python tools/prune_work.py --apply      # delete
    .venv/bin/python tools/prune_work.py --days 0     # everything, active or not
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import time
from pathlib import Path

DESKTOP = Path.home() / "Desktop"
TMP = Path(tempfile.gettempdir())


def candidates() -> list[Path]:
    found = list(DESKTOP.glob(".work-*")) + list(DESKTOP.glob(".*-work"))
    # `preflight` used a fixed /tmp/preflight until 2026-10-13 and makes and
    # removes its own `preflight-<stem>-*` per run since; a killed run leaves one.
    found += list(Path("/tmp").glob("preflight*")) + list(TMP.glob("preflight-*"))
    return sorted({p for p in found if p.is_dir() and not p.is_symlink()})


def newest(folder: Path) -> float:
    stamps = [folder.stat().st_mtime]
    stamps += [f.stat().st_mtime for f in folder.rglob("*")
               if f.is_file() and not f.is_symlink()]
    return max(stamps)


def size(folder: Path) -> int:
    return sum(f.stat().st_size for f in folder.rglob("*")
               if f.is_file() and not f.is_symlink())


def main(argv: list[str]) -> int:
    apply = "--apply" in argv[1:]
    days = 3.0
    if "--days" in argv:
        days = float(argv[argv.index("--days") + 1])
    cutoff = time.time() - days * 86400

    drop, keep = [], []
    for folder in candidates():
        (drop if newest(folder) < cutoff else keep).append(folder)

    gb = lambda fs: sum(size(f) for f in fs) / 1e9
    for f in keep:
        print(f"  keep (touched in the last {days:g} days): {f}")
    for f in drop:
        print(f"  drop: {f}  {size(f) / 1e6:.0f} MB")
    print(f"keep: {len(keep)} folders, {gb(keep):.2f} GB")
    print(f"drop: {len(drop)} folders, {gb(drop):.2f} GB")

    if not apply:
        print("\nreport only — pass --apply to delete")
        return 0
    for f in drop:
        shutil.rmtree(f)
    print(f"\ndeleted {len(drop)} folders")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
