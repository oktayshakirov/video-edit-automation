"""The film surface's arrangement (`core/filmfx.py`).

The editor's rules: a couple of clean clips per video, some with one layer only,
not everything everywhere - and no texture on drawn data beats.
"""

from video_automation.core.filmfx import RECIPES, plan
from video_automation.crypto.shots import Shot

CLIP = "clip.mp4"


def foot(payload=()):
    return Shot(clip=CLIP, payload=payload)


def test_first_shot_is_clean():
    assert plan([foot(), foot()])[0] == "clean"


def test_beats_get_nothing_and_chapters_their_own():
    r = plan([foot(), Shot(graphic="checklist", payload=([],)),
              Shot(graphic="chapter", payload=("A turn",))])
    assert r[1:] == ["beat", "chapter"]
    assert RECIPES["beat"] == {}


def test_section_opens_full_after_a_card():
    r = plan([foot(), Shot(graphic="chapter", payload=("A turn",)), foot()])
    assert r[2] == "full"


def test_disclaimer_clean_statement_grain_only():
    r = plan([foot(), foot(("", "This is not financial advice.")),
              foot(("", "A statement the footage illustrates."))])
    assert r[1] == "clean" and r[2] == "grain"


def test_a_long_run_mixes_clean_single_and_full_without_repeats():
    r = plan([foot() for _ in range(20)])
    assert r.count("clean") >= 3
    assert "grain" in r and "dust" in r and "full" in r
    assert all(a != b for a, b in zip(r, r[1:]))


def test_no_vertical_scratch_in_dust():
    import inspect
    from video_automation.core import filmfx
    assert "scratch" not in inspect.getsource(filmfx.dust).lower()
