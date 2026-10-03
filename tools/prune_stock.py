"""Drop the screening leftovers out of `assets/stock/`, keep what a build needs.

The cache reached **26 GB** — 24 GB of it video — because every long-form
video fetches a fresh pool and then *screens* it: a dozen candidates pulled
per slot, one cut, the rest left on disk. Those rejects are not worthless, but
what makes them valuable is the **verdict**, and the verdict lives in
`docs/video/footage.md` and in `manifest.json`, not in the bytes. The bytes are
re-fetchable by id from the manifest, which is the same argument `.gitignore`
already makes for not committing them.

So: **keep every file a project file on disk actually cuts, drop the rest.** On
the first run that was 525 files / 4.2 GB kept against 3375 files / 23.5 GB
dropped.

Two things the naive version of this gets wrong, both of which cost a clip:

1. **Constants are resolved, not grepped.** A project writes `V = STOCK /
   "videos"` and then `RISK = V / "tightrope-walker-balance-dark/10013469.mp4"`,
   or binds the folder (`WAVES = STOCK / "videos/abstract-dark-waves-motion"`)
   and joins the file at the use site. A regex that only matches one of those
   shapes silently marks the others for deletion.
2. **The same Pexels id lives under several query slugs.** `10241357` is
   cached under four padlock folders because four searches returned it. Only
   the path a project names is kept; the sibling copies are duplicate bytes.

    .venv/bin/python tools/prune_stock.py            # report, delete nothing
    .venv/bin/python tools/prune_stock.py --apply    # delete

`--apply` is required because this is not reversible from here: recovery is a
re-fetch from `manifest.json`, so a file that was never manifested is gone.
The exit code is non-zero if a project names a file that is *not* on disk,
which means someone pruned past a reference, or a fetch was never manifested.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOCK = ROOT / "assets/stock"

# Brand-level stock that recurs in every video by design, so no project has to
# name it for it to survive. Same exemption `tools/audit_assets.py` carries.
EXEMPT_FOLDERS = {"subscribe"}

_BASE = re.compile(
    r'^\s*([A-Z][A-Z0-9_]*)\s*=\s*(?:STOCK|CACHE)\s*/\s*"(videos|photos)"\s*$', re.M)
_FROM_STOCK = re.compile(
    r'^\s*([A-Z][A-Z0-9_]*)\s*=\s*(?:STOCK|CACHE)\s*/\s*"((?:videos|photos)/[^"]+)"', re.M)
_FROM_CONST = re.compile(
    r'^\s*([A-Z][A-Z0-9_]*)\s*=\s*([A-Z][A-Z0-9_]*)\s*/\s*"([^"]+)"', re.M)
_USE = re.compile(r'\b([A-Z][A-Z0-9_]*)\s*/\s*"([^"]+\.(?:mp4|jpg|jpeg|png))"')
_LITERAL = re.compile(r'"((?:videos|photos)/[^"]+\.(?:mp4|jpg|jpeg|png))"')
_IS_FILE = re.compile(r'\d+\.(?:mp4|jpg|jpeg|png)$')


def referenced(src: str) -> set[str]:
    """Stock-relative paths one module cuts, with its constants resolved."""
    env = {m.group(1): m.group(2) for m in _BASE.finditer(src)}
    env.update({m.group(1): m.group(2) for m in _FROM_STOCK.finditer(src)})
    # Two passes: a constant may be defined from another one defined later.
    for _ in range(2):
        for name, base, tail in (m.groups() for m in _FROM_CONST.finditer(src)):
            if base in env:
                env[name] = env[base].rstrip("/") + "/" + tail

    out = {m.group(1) for m in _LITERAL.finditer(src)}
    out |= {v for v in env.values()
            if _IS_FILE.search(v) and v.split("/")[0] in ("videos", "photos")}
    for name, filename in (m.groups() for m in _USE.finditer(src)):
        if name in env:                      # anything else is not stock
            out.add(env[name].rstrip("/") + "/" + filename)
    return {p for p in out if p.split("/")[0] in ("videos", "photos")}


def main(argv: list[str]) -> int:
    apply = "--apply" in argv[1:]

    wanted: set[str] = set()
    for src in sorted(ROOT.glob("projects/**/*.py")):
        wanted |= referenced(src.read_text(errors="ignore"))

    keep, missing = set(), sorted(p for p in wanted if not (STOCK / p).is_file())
    keep |= {(STOCK / p).resolve() for p in wanted if (STOCK / p).is_file()}
    for folder in EXEMPT_FOLDERS:
        for kind in ("videos", "photos"):
            keep |= {f.resolve() for f in (STOCK / kind / folder).glob("*")
                     if f.is_file()}

    drop = [f for kind in ("videos", "photos")
            for folder in sorted((STOCK / kind).glob("*")) if folder.is_dir()
            for f in sorted(folder.glob("*"))
            if f.is_file() and f.resolve() not in keep]

    gb = lambda fs: sum(f.stat().st_size for f in fs) / 1e9
    print(f"referenced by a project: {len(wanted)}")
    print(f"keep: {len(keep)} files, {gb(sorted(keep)):.2f} GB")
    print(f"drop: {len(drop)} files, {gb(drop):.2f} GB")

    for p in missing:
        print(f"  MISSING: a project cuts {p}, which is not on disk", file=sys.stderr)

    if not apply:
        print("\nreport only — pass --apply to delete")
        return 1 if missing else 0

    for f in drop:
        f.unlink()
    # A folder emptied of every candidate is noise; `manifest.json` still
    # records what was in it.
    for kind in ("videos", "photos"):
        for folder in sorted((STOCK / kind).glob("*")):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
    print(f"\ndeleted {len(drop)} files")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
