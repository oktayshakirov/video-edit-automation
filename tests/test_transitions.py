"""The transition vocabulary, and the one promise it has to keep.

**`push` must stay byte-identical.** The shorts are reproducible against a
baseline and long form has shipped on `push` since it existed, so moving that
code into `core/transitions.py` was only safe because it was verified frame by
frame first. This is that verification, kept, so the next edit to the module
cannot quietly change a shipped video.
"""

from __future__ import annotations

import numpy as np
import pytest
from PIL import Image

from video_automation.core import transitions
from video_automation.core.brand import CRYPTO
from video_automation.core.frame import LANDSCAPE as F
from video_automation.crypto.shots import Shot

STEPS = [i / 40 for i in range(41)]


@pytest.fixture(scope="module")
def pair():
    """Two frames of noise. Noise rather than flat colour on purpose: a
    transition that drops or duplicates a region is invisible against a solid
    fill and obvious against this."""
    rng = np.random.default_rng(3)
    return (Image.fromarray(rng.integers(0, 255, (F.h, F.w, 3), dtype=np.uint8)),
            Image.fromarray(rng.integers(0, 255, (F.h, F.w, 3), dtype=np.uint8)))


def _shipped_push(a, b, p):
    """The exact code `render_shots` ran inline before the module existed."""
    e = p * p * (3 - 2 * p)
    dx = int(round(F.w * e))
    c = Image.new("RGB", F.size, (0, 0, 0))
    c.paste(a, (-dx, 0))
    c.paste(b, (F.w - dx, 0))
    return c


@pytest.mark.parametrize("p", STEPS)
def test_push_is_byte_identical_to_the_shipped_code(pair, p):
    a, b = pair
    got = transitions.apply("push", a, b, p, F)
    assert np.array_equal(np.asarray(got), np.asarray(_shipped_push(a, b, p)))


@pytest.mark.parametrize("mode", sorted(transitions._MODES))
@pytest.mark.parametrize("p", [0.0, 0.25, 0.5, 0.75, 1.0])
def test_every_mode_returns_a_full_frame(pair, mode, p):
    a, b = pair
    got = transitions.apply(mode, a, b, p, F, CRYPTO)
    assert got.size == F.size and got.mode == "RGB"


@pytest.mark.parametrize("mode", sorted(transitions._MODES))
def test_a_mode_ends_where_it_should(pair, mode):
    """At p=1 the incoming shot owns the frame. A move that has not finished
    travelling by the end of its own window shows a seam on the cut - which is
    exactly the fault a transition is supposed to hide."""
    a, b = pair
    end = np.asarray(transitions.apply(mode, a, b, 1.0, F, CRYPTO))
    # Not equality: `punch` is still scaled at its last frame by design, and
    # `glitch` may hold a displaced slice. The claim is weaker and the one
    # that matters - the outgoing shot is gone.
    assert np.abs(end.astype(int) - np.asarray(b).astype(int)).mean() < \
        np.abs(end.astype(int) - np.asarray(a).astype(int)).mean()


def test_an_unknown_mode_falls_back_rather_than_raising(pair):
    """Called once per frame inside the encoder: a typo in a shot list should
    cost a soft-looking cut, not a half-written MP4."""
    a, b = pair
    got = transitions.apply("nonesuch", a, b, 0.5, F, CRYPTO)
    assert np.array_equal(np.asarray(got), np.asarray(Image.blend(a, b, 0.5)))


def test_every_mode_has_a_length():
    """`XF` is what a caller reads instead of guessing an xfade."""
    assert set(transitions._MODES) | {"dissolve"} == set(transitions.XF)
    assert all(0.1 <= v <= 1.0 for v in transitions.XF.values())


def test_the_silent_moves_stay_silent():
    """A sound on every cut in a three-minute video is worse than none."""
    assert "push" not in transitions.CUES
    assert "dissolve" not in transitions.CUES


def test_cues_land_before_the_cut_not_after():
    shots = [Shot(graphic="stat", payload=("9", "", ""), start=0.0, hold=10.0,
                  transition="whip", xfade=transitions.XF["whip"]),
             Shot(graphic="stat", payload=("8", "", ""), start=10.0, hold=5.0)]
    (at, kind), = transitions.cues(shots)
    assert kind == "whoosh"
    # Inside the transition window, and ahead of the cut - a whoosh peaks
    # after its own transient, so firing it on the cut lands it late.
    assert 10.0 - transitions.XF["whip"] - 0.2 < at < 10.0


def test_the_last_shot_contributes_no_cue():
    """There is nothing to transition into, and a cue past the end of the
    track is silently dropped by the mixer rather than reported."""
    shots = [Shot(graphic="stat", payload=("9", "", ""), start=0.0, hold=10.0,
                  transition="flash", xfade=transitions.XF["flash"])]
    assert transitions.cues(shots) == []


def test_a_cut_contributes_no_cue():
    """`xfade=0` is a hard cut; there is no move for a sound to cover."""
    shots = [Shot(graphic="stat", payload=("9", "", ""), start=0.0, hold=10.0,
                  transition="whip", xfade=0.0),
             Shot(graphic="stat", payload=("8", "", ""), start=10.0, hold=5.0)]
    assert transitions.cues(shots) == []
