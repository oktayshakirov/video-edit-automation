"""Top-level dispatch: `python -m video_automation <project> <subcommand>`.

Project first, because the three projects share an engine but not a workflow —
drone indexes footage and cuts to music, crypto turns an article into a script,
tinnitus generates therapy audio. A single flat command space would have to
pretend those are variants of one operation, and they are not.

    python -m video_automation drone index ~/Desktop/Plovdiv
    python -m video_automation drone build --project plovdiv --dry-run
    python -m video_automation voices list
"""

from __future__ import annotations

import sys

PROJECTS = ("drone", "crypto", "tinnitus")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)

    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        print(f"\nprojects: {', '.join(PROJECTS)}\nalso: voices")
        return 0 if argv else 1

    name, rest = argv[0], argv[1:]

    if name == "voices":
        from .core.voices import main as voices_main
        return voices_main(rest)

    if name == "drone":
        from .drone.cli import main as drone_main
        return drone_main(rest)

    if name in PROJECTS:
        print(f"'{name}' has no CLI yet — the project is a stub. "
              f"Its voice profiles are registered; see `voices list`.",
              file=sys.stderr)
        return 1

    print(f"unknown project: {name}\nprojects: {', '.join(PROJECTS)}",
          file=sys.stderr)
    return 1
