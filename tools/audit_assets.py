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

**The shot list is read by importing the project, not by scanning its text.**
A regex cannot do this job. The one that used to sits on `clip=NAME,
clip_at=N` and so it saw a shot only when the shot skipped into its clip —
which is the minority — and it missed `clip=OCEAN / "5678004.mp4"` entirely.
Both failures land on the same check: with most shots unseen, two uses of one
clip that are ten slots apart come out adjacent in the index, and `MIN_APART`
calls a well-spaced cut a fault. Importing gives the real list in the real
order, with the real paths on it, so the index means what it says. The scan
survives only as the fallback for a module that will not import.
"""

from __future__ import annotations

import collections
import contextlib
import importlib.util
import io
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STOCK = ROOT / "assets/stock"
PROJECTS = ROOT / "projects"

# A project is read by importing it (see `load`), and every one of them imports
# `video_automation`. Running this file directly puts `tools/` on the path, not
# the repo root, so the projects would all fail to import and quietly fall back
# to the source scan the import is there to replace.
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HEADROOM = 8.0          # the slot a clip must be able to cover, in seconds
SLOWEST = 0.75          # `longform/clip.py` — a clip may be stretched to fill
                        # its slot, but no further than 1/0.75 = 1.33x
FLOOR = HEADROOM * SLOWEST   # so this much of the clip left is enough
MAX_USES = 2            # per video, per asset — the floor, see `cap`
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


def load(path: Path):
    """Import a project module without running it.

    Every project guards its `main()` behind `if __name__ == "__main__"`, so
    importing one is just the constants — the shot lists included. Each gets a
    private module name because two projects from one post (the long form and
    its Short) share a stem, and `projects/` is not a package.

    Import chatter goes to the void; a project that prints at import time is
    not this tool's problem and its noise would bury the findings.
    """
    name = "_audit_" + re.sub(r"\W", "_", f"{path.parent.name}/{path.stem}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"no loader for {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def shot_list(mod) -> list | None:
    """Every shot the render will lay down, in playback order.

    Shorts keep one flat `SHOTS`; long form splits it across `SECTIONS`, whose
    own `flatten` also inserts the chapter cards — those are slots on screen
    like any other, so the separation this tool measures is the real one. A
    `None` entry is a held shot, and it holds a slot too.
    """
    shots = getattr(mod, "SHOTS", None)
    if shots is not None:
        return list(shots)
    sections = getattr(mod, "SECTIONS", None)
    if sections is not None:
        from video_automation.longform.plan import flatten
        return list(flatten(sections)[1])
    return None


def cap(shots: int) -> int:
    """How many slots one clip may hold in a piece this long.

    A flat 2 is right for a Short, which is a dozen shots off half a dozen
    clips. It is arithmetic nonsense for a long form: `airpods-and-tinnitus`
    is 58 shots and 37 clip slots pulled from 13 folders, so *something* has
    to come back three times, and the shipped cut is none the worse for it.

    So the cap scales with the piece. `MIN_APART` already says two uses must
    sit five slots apart, which by itself bounds how often a clip can return;
    allowing one use per ten slots leaves that bound the binding one and keeps
    this check for the case it was written for, a clip that dominates.
    """
    return max(MAX_USES, shots // (MIN_APART * 2))


def slots_from_module(mod) -> list[tuple[str, float, int, Path]] | None:
    """(name, clip_at, slot index, file) for every clip the render will play.

    The index is the shot's own position in the list, so a clip that opens the
    video and comes back nine shots later reads as nine apart — which is what
    a viewer sees. Names come from the module's own constants rather than from
    the source text, and the path is the one the render will open, so there is
    nothing left to guess about where the file lives.
    """
    shots = shot_list(mod)
    if shots is None:
        return None
    named = {v: k for k, v in vars(mod).items()
             if isinstance(v, Path) and not k.startswith("_")}
    slots = []
    for i, shot in enumerate(shots):
        clip = getattr(shot, "clip", None) if shot is not None else None
        if clip is None:
            continue
        # Two styles in the projects, and both have to read back as a name a
        # person can grep for. Either the constant is the file itself, or it
        # is the folder and the shot picks a file out of it — the second is
        # what the source scan could not see at all, because `clip=OCEAN /
        # "5678004.mp4"` is not the bare identifier its regex wanted.
        if clip in named:
            name = named[clip]
        elif clip.parent in named:
            name = f"{named[clip.parent]}/{clip.name}"
        else:
            name = str(clip.relative_to(STOCK)) if clip.is_relative_to(STOCK) \
                else clip.name
        slots.append((name, float(shot.clip_at), i, clip))
    return slots


def slots_from_source(src: str, names: dict[str, str]
                      ) -> list[tuple[str, float, int, Path]]:
    """The old regex read, kept only for a module that will not import.

    It sees a shot only when the shot carries an explicit `clip_at=`, so the
    indexes it returns are positions in *that* subset and the gaps between them
    are shorter than the real ones. That is the whole reason the module is
    imported first; this is a floor, not a second opinion.
    """
    out = []
    for i, m in enumerate(re.finditer(r"clip=(\w+), clip_at=([\d.]+)", src)):
        name = m.group(1)
        rel = names.get(name)
        if rel:
            out.append((name, float(m.group(2)), i, STOCK / rel))
    return out


def audit(path: Path) -> list[str]:
    src = path.read_text()
    problems: list[str] = []

    try:
        mod = load(path)
    except Exception as exc:                       # noqa: BLE001 - report it
        problems.append(f"cannot import ({exc.__class__.__name__}: {exc}) - "
                        f"falling back to the source scan, which undercounts "
                        f"the gap between two uses of one clip")
        slots = slots_from_source(src, assets_of(src))
        # The scan sees only the shots that carry a `clip_at=`, so the length
        # it reports is not the piece's — fall back to the flat cap.
        total = 0
    else:
        slots = slots_from_module(mod)
        total = len(shot_list(mod) or [])
        if slots is None:
            # Sound-therapy pieces, quiz shorts and the drone cuts are built
            # from a noise bed, a question list or two Desktop files, not from
            # a shot list of stock. There is no slot order here to be wrong
            # about, so there is nothing for this tool to say.
            return []

    limit = cap(total)
    uses: dict[str, list[int]] = collections.defaultdict(list)
    for name, at, i, clip in slots:
        uses[name].append(i)
        d = duration(clip)
        if d is None:
            problems.append(f"{name}: cannot probe {clip}")
        elif d - at < FLOOR:
            problems.append(
                f"{name}@{at} has only {d - at:.1f}s left of {d:.1f}s - "
                f"a {HEADROOM:.0f}s shot would need "
                f"{HEADROOM / max(d - at, 1e-9):.2f}x slow motion, past the "
                f"{1 / SLOWEST:.2f}x the render allows")

    for name, idxs in uses.items():
        if len(idxs) > limit:
            problems.append(f"{name} used {len(idxs)}x (max {limit})")
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
