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


def test_a_stacked_headline_stays_inside_its_box():
    """`thumb.stack_headline` sizes the block to its box, so a cover's text
    cannot run into the picture beside it (2026-11-20: the tier cover's
    plate ran into the board)."""
    from PIL import Image
    from video_automation.longform import thumb as T
    im = Image.new("RGB", (1280, 720))
    box = (34, 60, 536, 600)
    for rows in (["Tinnitus:", "What's", "[Top Tier?]"],
                 ["What's", "[Top Tier]", "For Tinnitus?"],
                 ["A Much Longer Row Than The Others", "[Here]"]):
        x0, y0, x1, y1 = T.stack_headline(im, rows, box)
        assert x0 >= box[0] - 1 and x1 <= box[0] + box[2] + 1
        assert y0 >= box[1] - 1 and y1 <= box[1] + box[3] + 1
