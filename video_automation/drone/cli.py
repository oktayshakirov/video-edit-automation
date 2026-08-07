"""Command line entry point.

    python -m video_automation drone index  ~/Desktop/Plovdiv
    python -m video_automation drone index  ~/Desktop/Plovdiv --reanalyze   # keep proxies, redo metrics
    python -m video_automation drone report ~/Desktop/Plovdiv

Subcommands rather than flags, because Phase 2-4 add `music`, `edit` and
`export` alongside these.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .analysis import analyze_proxy
from .config import LOW_CONFIDENCE, PROXY_DIRNAME
from .db import open_db, upsert
from ..core.media import (ToolMissing, build_proxy, ffprobe_meta, is_clip,
                          quick_hash, require_tools)
from .report import print_report


def cmd_index(root: Path, reanalyze: bool) -> int:
    require_tools()

    conn = open_db(root)
    cache = root / PROXY_DIRNAME

    clips = sorted(
        p for p in root.rglob("*")
        if is_clip(p) and PROXY_DIRNAME not in p.parts
    )
    if not clips:
        print("No video files found.", file=sys.stderr)
        return 1

    known = {r[0] for r in conn.execute("SELECT hash FROM clips")}
    print(f"Found {len(clips)} clips in {root}\n")

    for i, src in enumerate(clips, 1):
        h = quick_hash(src)
        label = f"[{i}/{len(clips)}] {src.name}"

        if h in known and not reanalyze:
            print(f"{label} — cached")
            continue

        meta = ffprobe_meta(src)
        if meta is None:
            print(f"{label} — SKIPPED (unreadable)")
            continue

        proxy = cache / f"{h}.mp4"
        if not proxy.exists():
            print(f"{label} — building proxy...", end=" ", flush=True)
            if not build_proxy(src, proxy):
                print("FAILED")
                continue
        else:
            print(f"{label} —", end=" ", flush=True)

        metrics = analyze_proxy(proxy)
        if metrics is None:
            print("FAILED (analysis)")
            continue

        upsert(conn, {
            "hash": h,
            "path": str(src),
            "filename": src.name,
            **meta,
            **metrics,
        })
        conn.commit()

        warn = "  [low confidence]" if metrics["confidence"] < LOW_CONFIDENCE else ""
        print(f"{metrics['move_type']}, energy {metrics['motion_energy']:.3f}, "
              f"{meta['duration']:.1f}s{warn}")

    print()
    print_report(conn)
    return 0


def cmd_report(root: Path) -> int:
    print_report(open_db(root))
    return 0


def cmd_build(root: Path, music: Path, out: Path | None, dry_run: bool,
              click: bool = False, lock: list[dict] | None = None,
              lock_out: Path | None = None) -> int:
    """Music -> bar grid -> edit decisions -> FCPXML."""
    require_tools()

    from . import edit as edit_mod
    from . import fcpxml as fcpxml_mod
    from . import music as music_mod
    from .config import DB_NAME, HEAD_TRIM

    db_path = root / PROXY_DIRNAME / DB_NAME
    if not db_path.exists():
        print(f"No index at {db_path}. Run `video_automation drone index` first.", file=sys.stderr)
        return 1

    clips = edit_mod.load_clips(db_path)
    if not clips:
        print("Index is empty.", file=sys.stderr)
        return 1

    # The timeline inherits the footage's format. Mixed formats would need a
    # conform decision; refuse rather than silently pick one.
    formats = {(c.fps,) for c in clips}
    if len(formats) > 1:
        print(f"Mixed frame rates in the index: {sorted(formats)}. "
              "Conform the footage first.", file=sys.stderr)
        return 1
    fps = int(round(clips[0].fps))

    conn = open_db(root)
    width, height = conn.execute(
        "SELECT width, height FROM clips LIMIT 1").fetchone()

    from .config import (MUSIC_LOOP, MUSIC_LOOP_CROSSFADE_BARS,
                         MUSIC_LOOP_HANDOFF_BAR, MUSIC_LOOP_RETURN_BAR,
                         PHRASE_BARS)

    print(f"Analysing {music.name} ...")
    track = music_mod.analyze_track(music)

    if MUSIC_LOOP:
        # Default handoff is the last phrase line of the song, so pass 1 runs as
        # far as it can before handing over.
        handoff = MUSIC_LOOP_HANDOFF_BAR
        if handoff is None:
            handoff = (track.n_bars // PHRASE_BARS) * PHRASE_BARS
        ret = MUSIC_LOOP_RETURN_BAR
        if ret is None:
            ret = PHRASE_BARS
        track = music_mod.extend_with_loop(
            track, handoff, ret, MUSIC_LOOP_CROSSFADE_BARS)

    print()
    print(music_mod.describe(track))
    print()

    if click:
        wav = root / f"{music.stem} (bar grid check).wav"
        music_mod.write_click_track(track, wav)
        print(f"Click track: {wav}")
        print("  high click = bar 1. If those land on the snare instead of the kick,")
        print("  the downbeat phase is off by two beats and every cut inherits it.")
        print()

    edit_mod.reset(clips, fps)
    if lock:
        print(f"Replaying locked edit — {len(lock)} slots, scorer bypassed.")
        cuts = edit_mod.build_locked(track, clips, fps, lock)
    else:
        cuts = edit_mod.build_edit(track, clips, fps)
    print(edit_mod.describe(cuts, fps))
    print()

    if lock_out:
        lock_out.write_text(edit_mod.dump_lock(cuts), encoding="utf-8")
        print(f"Wrote lock: {lock_out}  ({len(cuts)} slots)")
        print()

    dupes = edit_mod.overlapping_slices(cuts)
    if dupes:
        print(f"  {len(dupes)} REPEATED SOURCE RANGE(S) — the same footage appears twice:")
        for d in dupes:
            print(f"    - {d}")
        print()

    if dry_run:
        print("Dry run — no FCPXML written.")
        return 0

    xml = fcpxml_mod.render(
        cuts, music, fps=fps, width=width, height=height,
        project_name=root.name, track=track,
    )
    out = out or (root / f"{root.name}.fcpxml")
    out.write_text(xml, encoding="utf-8")

    from .validate import check, summarise
    problems = check(out)
    print(f"Wrote {out}  ({len(xml)/1024:.1f} KB)")
    print(f"  {summarise(out)}")
    if problems:
        print(f"  {len(problems)} STRUCTURAL PROBLEM(S):")
        for p in problems[:20]:
            print(f"    - {p}")
        return 2
    from .validate import find_dtd
    dtd = find_dtd("1.10")
    print(f"  validated: {'DTD (Final Cut 1.10), ' if dtd else ''}"
          "spine continuous, source ranges in bounds, media online")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="video_automation drone", description="Drone Automation — beat-driven editor for drone selects."
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="scan a footage folder and build the clip index")
    p_index.add_argument("folder", type=Path)
    p_index.add_argument("--reanalyze", action="store_true",
                         help="reuse cached proxies, recompute metrics")

    p_report = sub.add_parser("report", help="print the existing index and exit")
    p_report.add_argument("folder", type=Path)

    p_build = sub.add_parser("build", help="cut the index to a music track, write FCPXML")
    p_build.add_argument("folder", type=Path, nargs="?",
                         help="footage folder (omit when using --project)")
    p_build.add_argument("--project", default=None,
                         help="project name or .toml path under projects/")
    p_build.add_argument("--music", type=Path, default=None)
    p_build.add_argument("--out", type=Path, default=None)
    p_build.add_argument("--dry-run", action="store_true",
                         help="print the edit list without writing FCPXML")
    p_build.add_argument("--click", action="store_true",
                         help="also write a click-track WAV to check the bar grid by ear")
    p_build.add_argument("--lock-out", type=Path, default=None,
                         help="write this edit's assignment to a lock file")
    p_build.add_argument("--no-lock", action="store_true",
                         help="ignore the project's lock and re-run the scorer")

    args = ap.parse_args(argv)

    out = getattr(args, "out", None)
    music = getattr(args, "music", None)
    lock = None

    try:
        # A project file supplies footage, music and tuning in one place, and
        # its overrides must land on config before the edit modules import it.
        if getattr(args, "project", None):
            from . import project as project_mod
            proj = project_mod.load(args.project)
            changed = project_mod.apply_overrides(proj.overrides)
            print(f"Project: {proj.name}  ({proj.profile})")
            for line in changed:
                print(f"  override  {line}")
            root, music, out = proj.footage, proj.music, out or proj.out
            if not getattr(args, "no_lock", False):
                lock = proj.load_lock()
        elif args.cmd == "build" and args.folder is None:
            print("build needs either a footage folder or --project", file=sys.stderr)
            return 1
        else:
            root = args.folder

        root = Path(root).expanduser().resolve()
        if not root.is_dir():
            print(f"Not a directory: {root}", file=sys.stderr)
            return 1

        if args.cmd == "index":
            return cmd_index(root, args.reanalyze)
        if args.cmd == "build":
            if music is None:
                print("build needs --music (or a project file)", file=sys.stderr)
                return 1
            music = Path(music).expanduser().resolve()
            if not music.is_file():
                print(f"Music file not found: {music}", file=sys.stderr)
                return 1
            return cmd_build(root, music, out, args.dry_run, args.click,
                             lock, args.lock_out)
        return cmd_report(root)
    except (ToolMissing, FileNotFoundError, KeyError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
