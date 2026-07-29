"""Per-video project files.

A project pins the footage folder, the track, and any tuning that differs from
the defaults, so each video is reproducible from one file and the shared
defaults in config.py never have to be edited per shoot.

    dronecut build --project projects/plovdiv.toml

Overrides are applied to the config module before the edit modules import it,
which is why cli.py imports those lazily. They therefore affect phases 2-4
(music, edit decisions, export). Changing an indexing constant needs a
`dronecut index --reanalyze` instead, because the clip index is already built.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent / "projects"


@dataclass
class Project:
    name: str
    footage: Path
    music: Path
    profile: str = "youtube"
    out: Path | None = None
    overrides: dict = field(default_factory=dict)


def resolve(ref: str) -> Path:
    """Accept 'plovdiv', 'plovdiv.toml' or a full path."""
    p = Path(ref).expanduser()
    if p.is_file():
        return p
    for cand in (PROJECT_DIR / ref, PROJECT_DIR / f"{ref}.toml"):
        if cand.is_file():
            return cand
    raise FileNotFoundError(
        f"No project '{ref}'. Looked in {PROJECT_DIR} and as a literal path.")


def load(ref: str) -> Project:
    path = resolve(ref)
    data = tomllib.loads(path.read_text(encoding="utf-8"))

    missing = [k for k in ("footage", "music") if k not in data]
    if missing:
        raise KeyError(f"{path.name} is missing required key(s): {', '.join(missing)}")

    return Project(
        name=data.get("name", path.stem),
        footage=Path(data["footage"]).expanduser(),
        music=Path(data["music"]).expanduser(),
        profile=data.get("profile", "youtube"),
        out=Path(data["out"]).expanduser() if data.get("out") else None,
        overrides=data.get("overrides", {}),
    )


def apply_overrides(overrides: dict) -> list[str]:
    """Write project overrides onto the config module. Returns what changed.

    Unknown keys are an error rather than a silent no-op — a typo in a project
    file should not quietly leave the default in place and send you hunting
    through the edit for why nothing moved.
    """
    from . import config

    applied = []
    for key, value in overrides.items():
        if not hasattr(config, key):
            raise KeyError(f"unknown config key in project overrides: {key}")
        old = getattr(config, key)
        if old != value:
            setattr(config, key, value)
            applied.append(f"{key}: {old!r} -> {value!r}")
    return applied
