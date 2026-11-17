"""A cover is written once (2026-11-17).

`what-makes-tinnitus-worse` and `stablecoin-interest` both saved the picked
cover as `-thumb.jpg` and again as `-thumb-<style>.jpg` beside it, so every
pick sat on the Desktop twice and the editor found the duplicates after two
runs. A project's `thumbs()` writes the pick at `out`; other directions only
on request, and never the pick's own style.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_no_project_writes_its_picked_cover_twice():
    bad = []
    for p in sorted((ROOT / "projects").rglob("*.py")):
        src = p.read_text()
        # every direction, the pick included, written beside `out`
        if "for k in COVERS:" in src and 'out.with_name(f"{out.stem}-{k}' in src:
            bad.append(str(p.relative_to(ROOT)))
    assert not bad, f"these write the picked cover twice: {bad}"
