"""The docs and skills still describe the repo that exists.

`docs/video/README.md` sets the rule: one lesson, one doc, and a link rather
than a second copy. Nothing checked it. By 2026-11-05 the two article skills
carried the same 56-line block twice (edited together in eight commits),
`tests/README.md` listed 5 of 19 test files, the docs index said four build
skills where there were five, and `projects/tinnitus.md` pointed at
`.claude/skills/docs/video/longform.md`, which has never existed. These are
cheap to keep true and invisible until someone follows a dead link.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
DOCS = REPO / "docs/video"
SKILLS = sorted((REPO / ".claude/skills").glob("*/SKILL.md"))
PROSE = SKILLS + sorted(DOCS.rglob("*.md")) + [REPO / "README.md",
                                               REPO / "tests/README.md"]

# A backticked path into the repo: `docs/...`, `tools/x.py`, `projects/crypto.md`
# (docs-relative). Placeholders (<name>, *, {a,b}) are patterns, not paths.
PATH = re.compile(r"`((?:docs|tools|projects|video_automation|assets|tests|"
                  r"\.claude|\.github)/[^`\s]+)`")


def ignored(rel: str) -> bool:
    """Gitignored on purpose - the brand sfx, the stock bytes."""
    r = subprocess.run(["git", "-C", str(REPO), "check-ignore", "-q", rel],
                       capture_output=True)
    return r.returncode == 0


# Folders the docs name whose every file is gitignored, so on a fresh clone
# the folder itself is absent. Named here rather than guessed at: a probe for
# "would a file in here be ignored" passes any missing folder, since `*.mp3`
# is ignored everywhere.
LOCAL_ONLY = {
    "assets/brand/sfx/",      # the title and chapter sounds (*.mp3)
    "assets/stock/photos/",   # Pexels stills, re-fetched from the manifest
}


def resolves(ref: str, where: Path) -> bool:
    ref = ref.rstrip(".,:;)").split("#")[0].split("::")[0]
    if ref in LOCAL_ONLY:
        return True
    for base in (REPO, DOCS, where.parent):
        if (base / ref).exists():
            return True
    return ignored(ref)


def refs():
    for f in PROSE:
        for m in PATH.finditer(f.read_text()):
            ref = m.group(1)
            if not any(c in ref for c in "<*{$"):
                yield f, ref


@pytest.mark.parametrize("f,ref", list(refs()),
                         ids=lambda x: x if isinstance(x, str) else
                         x.relative_to(REPO).as_posix())
def test_a_path_in_the_docs_exists(f, ref):
    assert resolves(ref, f), f"{f.relative_to(REPO)} names {ref}, which is not there"


def test_every_test_file_is_in_the_tests_readme():
    text = (REPO / "tests/README.md").read_text()
    missing = [p.name for p in sorted((REPO / "tests").glob("test_*.py"))
               if f"`{p.name}`" not in text]
    assert not missing, f"tests/README.md does not list {missing}"


def test_every_doc_is_on_the_map():
    text = (DOCS / "README.md").read_text()
    missing = [p.relative_to(DOCS).as_posix() for p in sorted(DOCS.rglob("*.md"))
               if p.name != "README.md" or p.parent != DOCS]
    missing = [d for d in missing if not d.startswith("demand/teardowns/")
               and d != "README.md" and f"`{d}`" not in text]
    assert not missing, f"docs/video/README.md's map is missing {missing}"


def test_every_skill_is_named_in_the_docs_index():
    text = (DOCS / "README.md").read_text()
    missing = [s.parent.name for s in SKILLS if f"/{s.parent.name}`" not in text]
    assert not missing, f"docs/video/README.md does not name {missing}"


def test_every_beat_has_its_entry_in_beats_md():
    from video_automation.longform.beats import BEATS
    text = (DOCS / "beats.md").read_text()
    missing = [b for b in BEATS if f"`{b}`" not in text]
    assert not missing, f"beats.md never names {missing}"


def paragraphs(f: Path):
    for p in re.split(r"\n\s*\n", f.read_text()):
        n = " ".join(p.split())
        if len(n) >= 300:
            yield n


def test_no_skill_repeats_another_skills_paragraph():
    """The rule in `docs/video/README.md`: link, never copy. A paragraph long
    enough to be a rule, word for word in two skills, is the drift the docs
    were rebuilt to stop. Put it in the narrowest doc and link to it."""
    seen: dict[str, str] = {}
    dupes = []
    for f in SKILLS:
        for n in paragraphs(f):
            if n in seen and seen[n] != f.parent.name:
                dupes.append((seen[n], f.parent.name, n[:80]))
            seen.setdefault(n, f.parent.name)
    assert not dupes, dupes
