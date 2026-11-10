"""`Shot(window=)` puts a shot inside a browser, player or terminal window.

The checks are geometric and on synthetic pictures: the window stays inside
each frame's safe box, the inner picture's edges never show, the player's
progress grows across the shot, and nothing changes for a shot without one.
"""

from __future__ import annotations

import numpy as np
import pytest
from PIL import Image

from video_automation.core import window
from video_automation.core.brand import CRYPTO, TINNITUS
from video_automation.core.frame import LANDSCAPE, VERTICAL
from video_automation.crypto.shots import Shot


class Flat:
    """An inner shot: one flat colour with a 4px brand-yellow border."""

    def __init__(self, frame, colour=(30, 90, 160)):
        im = np.zeros((frame.h, frame.w, 3), np.uint8)
        im[:] = colour
        im[:4], im[-4:], im[:, :4], im[:, -4:] = (229, 194, 0), (229, 194, 0), \
            (229, 194, 0), (229, 194, 0)
        self.im = Image.fromarray(im)

    def draw(self, f):
        return self.im


def test_a_spec_reads_two_ways():
    assert window.parse("browser") == ("browser", "")
    assert window.parse(("player", "Keynote")) == ("player", "Keynote")
    with pytest.raises(ValueError, match="unknown window"):
        window.parse("tablet")


def test_a_shot_has_no_window_unless_it_asks():
    assert Shot().window is None


@pytest.mark.parametrize("frame", [LANDSCAPE, VERTICAL], ids=lambda f: f.name)
def test_the_window_sits_inside_the_safe_box(frame):
    L = window.layout(frame)
    assert 0 < L.x and L.x + L.w < frame.w
    assert L.y > frame.logo_at[1]                  # under the watermark's top
    assert L.y + L.h <= frame.safe_bottom          # above the captions / UI


@pytest.mark.parametrize("kind", window.KINDS)
@pytest.mark.parametrize("frame", [LANDSCAPE, VERTICAL], ids=lambda f: f.name)
def test_it_draws_a_full_frame_and_hides_the_inner_border(kind, frame):
    w = window.WindowShot(Flat(frame), (kind, "example.com/page"), 3.0, 4.0,
                          frame, TINNITUS)
    out = np.asarray(w.draw(0.5))
    assert out.shape == (frame.h, frame.w, 3)
    L = w.L
    # The content area's middle row is the inner colour edge to edge: the
    # inner shot's yellow border was trimmed, not scaled into the window.
    top = 0 if kind == "player" else L.bar
    row = out[int(L.y + top + L.ch * 0.6), int(L.x + L.w * 0.02):int(L.x + L.w * 0.98)]
    yellow = np.all(np.abs(row.astype(int) - (229, 194, 0)) < 40, axis=1)
    assert not yellow.any()


def test_the_player_progress_grows_with_the_shot():
    fr = LANDSCAPE

    def filled(f):
        w = window.WindowShot(Flat(fr, (0, 0, 0)), "player", 0.0, 8.0, fr, CRYPTO)
        out = np.asarray(w.draw(f)).astype(int)
        L = w.L
        strip = out[int(L.y + L.ch):int(L.y + L.h), int(L.x):int(L.x + L.w)]
        return int(np.sum(np.all(np.abs(strip - CRYPTO.primary) < 30, axis=2)))

    a, b, c = filled(0.1), filled(0.5), filled(0.95)
    assert a < b < c
