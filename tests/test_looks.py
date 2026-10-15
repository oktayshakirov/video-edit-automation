"""Session looks are loops, and a loop has to close.

A long session renders one `loop` of picture and repeats it, and the bookends
run the same clock below zero, so every look must give the same frame at `t`,
`t + period` and `t - period`. A look that drifts by a pixel per loop is a jump
every minute for twenty minutes, which nobody catches in review and everybody
sees in playback.

Covers the shelf and every used look under `tinnitus/session_looks/`, so a
look moved off the shelf keeps being held to this.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil

import numpy as np
import pytest

from video_automation.core import looks
from video_automation.tinnitus import session_looks

SIZES = [(320, 180), (180, 320)]          # landscape and portrait layouts


def _used() -> list[type[looks.Look]]:
    out = []
    for m in pkgutil.iter_modules(session_looks.__path__):
        mod = importlib.import_module(f"{session_looks.__name__}.{m.name}")
        out += [c for _, c in inspect.getmembers(mod, inspect.isclass)
                if issubclass(c, looks.Look) and c.__module__ == mod.__name__]
    return out


ALL = list(looks.SHELF.values()) + _used()


def _available(cls) -> bool:
    src = getattr(cls, "SRC", None)
    return src is None or src.exists()


@pytest.mark.parametrize("w,h", SIZES)
@pytest.mark.parametrize("cls", ALL, ids=lambda c: c.__name__)
def test_a_look_closes_on_its_period(cls, w, h):
    if not _available(cls):
        pytest.skip(f"{cls.__name__}: stock source not in the local Pexels cache")
    look = looks.make(cls, w, h, 57.0, (4.0, 7.0, 8.0))
    for t in (0.0, 13.3, -4.0):
        a = look.at(t)
        assert a.shape == (h, w, 3) and a.dtype == np.uint8
        assert np.array_equal(a, look.at(t + 57.0)), f"{cls.__name__} jumps at t={t}"


def test_a_used_look_is_not_on_the_shelf():
    shelf = set(looks.SHELF.values())
    names = {c.__name__ for c in shelf}
    for cls in _used():
        assert cls not in shelf and cls.__name__ not in names, (
            f"{cls.__name__} is used by a video and still offered on the shelf")


def test_fern_breath_refuses_a_period_the_breath_does_not_divide():
    if not _available(looks.SHELF["fern-breath"]):
        pytest.skip("fern-breath: stock source not in the local Pexels cache")
    with pytest.raises(ValueError):
        looks.make("fern-breath", 320, 180, 60.0, (4.0, 7.0, 8.0))


def test_an_unknown_look_names_the_shelf():
    with pytest.raises(ValueError, match="cascade-still"):
        looks.make("jungle", 320, 180, 57.0)
