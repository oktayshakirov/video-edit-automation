"""`pile`'s physics: the same every time, inside the container, out on a drain.

The simulation runs once at build time with a fixed seed and `draw` only
looks positions up, so these read the recorded track directly.
"""

from __future__ import annotations

import numpy as np

from video_automation.core.brand import CRYPTO
from video_automation.core.frame import LANDSCAPE, VERTICAL
from video_automation.longform.beats import BEATS


START = 10.0


def pile(drain="", frame=LANDSCAPE, reveals=(0.5, 2.0, 4.0)):
    """Reveals are absolute times, so a beat that does not start at zero is
    the case worth testing - local times were the first test's own bug."""
    return BEATS["pile"]([(25, "In", "$"), (20, "More")], "T", drain,
                         brand=CRYPTO, frame=frame,
                         reveals=[START + r for r in reveals],
                         start=START, hold=7.0)


def test_the_physics_is_the_same_every_build():
    a, b = pile(), pile()
    assert np.array_equal(a.pos, b.pos, equal_nan=True)
    # The coins, on a plain ground: the brand backdrop is a video loop and
    # not this beat's to keep still.
    from PIL import Image
    ca, cb = (Image.new("RGB", LANDSCAPE.size), Image.new("RGB", LANDSCAPE.size))
    a.content(ca, 0.8)
    b.content(cb, 0.8)
    assert np.array_equal(np.asarray(ca), np.asarray(cb))


def test_coins_due_all_at_once_still_stay_in():
    """Reveals before the beat's start (a script slip) clamp to its start
    and still drop in separate lanes - nothing is flung out."""
    p = BEATS["pile"]([(40, "In")], "T", brand=CRYPTO, frame=LANDSCAPE,
                      reveals=[0.0], start=START, hold=6.0)
    end, _ = p._sample(p.hold)
    x0, x1 = p.cx - p.cw / 2, p.cx + p.cw / 2
    assert (end[:, 0] > x0).all() and (end[:, 0] < x1).all()


def test_every_coin_settles_inside_the_container():
    for frame in (LANDSCAPE, VERTICAL):
        p = pile(frame=frame)
        end, _ = p._sample(p.hold)
        x0, x1 = p.cx - p.cw / 2, p.cx + p.cw / 2
        assert p.n == 45 and not np.isnan(end).any()
        assert (end[:, 0] > x0).all() and (end[:, 0] < x1).all()
        assert (end[:, 1] < p.bottom).all()


def test_a_drain_empties_it():
    p = pile(drain="Liquidity pulled")
    end, _ = p._sample(p.hold)
    assert (end[:, 1] > p.bottom).mean() > 0.9


def test_nothing_falls_before_its_reveal():
    p = pile()
    before, _ = p._sample(0.45)                 # reveals are beat-local 0.5s on
    assert np.isnan(before).all()
    second, _ = p._sample(1.95)                 # only the first batch so far
    assert (~np.isnan(second[:, 0])).sum() == 25
