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
