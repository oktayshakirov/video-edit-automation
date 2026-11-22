"""The breathing ring's phases, long form and Short, agree on every pattern.

`rest` (a hold after the exhale, box breathing's fourth side) is the newest
phase; with it at 0 both renderers must give exactly what they gave before.
"""

from __future__ import annotations

import pytest

from video_automation.longform.asmr import _breath
from video_automation.tinnitus.asmr import breathing_phases, ring_radius

R_MIN, R_MAX = 150, 330


@pytest.mark.parametrize("t,want", [
    (0.0, (R_MIN, "inhale", 4)),
    (5.0, (R_MAX, "hold", 3)),
    (8.0, (R_MAX, "exhale", 4)),
    (12.0, (R_MIN, "hold", 4)),
    (15.5, (R_MIN, "hold", 1)),
    (16.0, (R_MIN, "inhale", 4)),     # the cycle closes
])
def test_box_breathing_long(t, want):
    r, label, left = _breath(t, R_MIN, R_MAX, 4.0, 4.0, 4.0, 4.0)
    assert (round(r), label, left) == want


def test_rest_zero_is_the_old_pattern():
    for i in range(190):
        t = i / 10
        assert _breath(t, R_MIN, R_MAX, 4.0, 7.0, 8.0) == \
            _breath(t, R_MIN, R_MAX, 4.0, 7.0, 8.0, 0.0)
    assert breathing_phases(0.0, 2, 4.0, 7.0, 8.0) == \
        breathing_phases(0.0, 2, 4.0, 7.0, 8.0, 0.0)


def test_box_breathing_short():
    phases = breathing_phases(10.0, 2, 4.0, 4.0, 4.0, 4.0)
    assert [p.kind for p in phases[:4]] == ["inhale", "hold", "exhale", "rest"]
    assert [p.label for p in phases[:4]] == ["inhale", "hold", "exhale", "hold"]
    assert phases[-1].end == 42.0
    r, label, _ = ring_radius(phases, 23.0, R_MIN, R_MAX)
    assert (r, label) == (R_MIN, "hold")


# The physiological sigh (queue row 9): inhale 3, a 1s top-up, exhale 6.
R_IN = R_MIN + (R_MAX - R_MIN) * 0.6


@pytest.mark.parametrize("t,want", [
    (0.0, (R_MIN, "inhale", 3)),
    (3.0, (round(R_IN), "inhale again", 1)),
    (4.0, (R_MAX, "exhale", 6)),
    (9.5, (153, "exhale", 1)),
    (10.0, (R_MIN, "inhale", 3)),     # the cycle closes
])
def test_sigh_long(t, want):
    r, label, left = _breath(t, R_MIN, R_MAX, 3.0, 0.0, 6.0, 0.0, 1.0)
    assert (round(r), label, left) == want


def test_sigh_short_matches_long():
    phases = breathing_phases(0.0, 3, 3.0, 0.0, 6.0, 0.0, 1.0)
    assert [p.kind for p in phases[:3]] == ["inhale", "top", "exhale"]
    assert phases[-1].end == 30.0
    for i in range(300):
        t = i / 10
        r_s, label_s, _ = ring_radius(phases, t, R_MIN, R_MAX)
        r_l, label_l, _ = _breath(t, R_MIN, R_MAX, 3.0, 0.0, 6.0, 0.0, 1.0)
        assert abs(r_s - r_l) < 1e-6 and label_s == label_l


def test_sigh_guides_build():
    from video_automation.tinnitus import guides
    pat = guides.Pattern(3.0, 0.0, 6.0, 0.0, 1.0)
    assert pat.cycle == 10.0
    assert [k for k, _ in pat.phases] == ["inhale", "top", "exhale"]
    for style in ("path", "clock"):
        for w, h in ((1920, 1080), (1080, 1920)):
            g = guides.make(style, w, h, pat, (200, 220, 255))
            assert g.pattern.at(3.5)[1] == "top"
    with pytest.raises(ValueError):
        guides.make("box", 1920, 1080, pat, (200, 220, 255))
