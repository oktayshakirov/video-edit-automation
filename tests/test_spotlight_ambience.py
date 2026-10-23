"""The spotlight's box fits the content, and place-sound stays restrained."""

import numpy as np
import pytest

from video_automation.core import ambience
from video_automation.crypto.shots import Shot
from video_automation.longform.beats.spotlight import snap


def _page():
    """A white page with one long line of 'text' and a block below it."""
    im = np.full((600, 1000, 3), 255, np.uint8)
    for x in range(40, 960, 26):                # 'letters' along one line
        im[200:230, x:x + 18] = (20, 40, 110)
    im[350:560, 600:900] = (120, 90, 60)        # a photo block
    return im


def test_a_box_cutting_a_line_grows_to_the_whole_line():
    x0, y0, x1, y1 = snap(_page(), (0.30, 0.32, 0.55, 0.40))
    assert x0 <= 0.045 and x1 >= 0.955          # the line runs 40..958px
    assert y0 <= 200 / 600 and y1 >= 230 / 600


def test_a_block_snaps_to_its_own_edges():
    x0, y0, x1, y1 = snap(_page(), (0.62, 0.60, 0.88, 0.92))
    assert x0 == pytest.approx(0.60, abs=0.005)
    assert x1 == pytest.approx(0.90, abs=0.005)


def test_a_photograph_with_no_plain_ground_is_left_as_given():
    noisy = np.random.default_rng(0).integers(0, 255, (400, 400, 3), np.uint8)
    r = (0.2, 0.2, 0.5, 0.5)
    assert snap(noisy, r) == r


def _shot(start, hold, **kw):
    sh = Shot(**kw)
    sh.start, sh.hold = start, hold
    return sh


RAIN = "assets/stock/videos/rain-on-window-at-night-dark/a.mp4"
CITY = "assets/stock/videos/city-traffic-night-bus-street/b.mp4"
HANDS = "assets/stock/videos/hand-holding-jaw-pain-dark/c.mp4"


def test_beds_only_where_a_place_is_shown_long_enough():
    shots = [_shot(0, 4, clip=RAIN), _shot(4, 3, clip=RAIN),     # one run
             _shot(7, 2, clip=CITY),                              # too short
             _shot(9, 5, graphic="stat", payload=("1", "a", "b")),
             _shot(14, 5, clip=HANDS),                            # no place
             _shot(19, 4, clip=CITY)]
    assert ambience.plan(shots) == [(0, 7, "rain"), (19, 23, "city")]


def test_the_track_is_silent_outside_the_beds():
    shots = [_shot(0, 2, graphic="stat", payload=("1", "a", "b")),
             _shot(2, 4, clip=RAIN)]
    tr = ambience.track(shots, 6.0)
    sr = ambience.SR
    assert np.abs(tr[: int(1.5 * sr)]).max() == 0.0
    assert np.abs(tr[int(3 * sr): int(5 * sr)]).max() > 0.1
