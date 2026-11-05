"""GPU effects do what they say: bloom glows only what is bright, a leak never
darkens, aberration leaves the centre alone, a vignette keeps the middle.

Skips where no OpenGL 3.3 context can be made (a Linux box without EGL).
The checks are on synthetic frames whose answer is known, never a typeface.
"""

from __future__ import annotations

import numpy as np
import pytest
from PIL import Image

from video_automation.core import shaderfx


def _gl_ok() -> bool:
    try:
        shaderfx.context()
        return True
    except Exception:
        return False


def test_no_effect_never_touches_the_gpu(monkeypatch):
    def boom():
        raise AssertionError("a GL context was made for nothing")
    monkeypatch.setattr(shaderfx, "context", boom)
    im = Image.new("RGB", (32, 18), (10, 20, 30))
    assert shaderfx.parse(None) == []
    assert np.array_equal(np.asarray(shaderfx.apply(im, None, 0.0)), np.asarray(im))


def test_a_spec_reads_three_ways():
    assert shaderfx.parse("bloom") == [("bloom", 1.0)]
    assert shaderfx.parse(("leak", 0.5)) == [("leak", 0.5)]
    assert shaderfx.parse(["vignette", ("bloom", 0.3)]) == [("vignette", 1.0),
                                                            ("bloom", 0.3)]
    with pytest.raises(ValueError, match="unknown shader"):
        shaderfx.ShaderShot(None, "sparkle", 1.0)


gl = pytest.mark.skipif(not _gl_ok(), reason="no OpenGL 3.3 context here")
W, H = 320, 180


def grey(v):
    return Image.new("RGB", (W, H), (v, v, v))


@gl
def test_bloom_glows_around_bright_and_leaves_dark_alone():
    dark = grey(12)
    assert np.abs(np.asarray(shaderfx.apply(dark, "bloom", 0.0), np.int16)
                  - 12).max() <= 1
    bar = np.full((H, W, 3), 12, np.uint8)
    bar[85:95, 100:220] = 255
    out = np.asarray(shaderfx.apply(Image.fromarray(bar), "bloom", 0.0), np.int16)
    assert out[75, 160].mean() > 12 + 15      # just above the bar: lit
    assert out[5, 5].mean() < 12 + 4          # far corner: still dark


@gl
def test_a_leak_never_darkens_and_moves_with_time():
    im = Image.fromarray(np.random.default_rng(3).integers(0, 255, (H, W, 3), np.uint8))
    a = np.asarray(shaderfx.apply(im, "leak", 0.0), np.int16)
    b = np.asarray(shaderfx.apply(im, "leak", 4.0), np.int16)
    base = np.asarray(im, np.int16)
    assert (a >= base - 1).all()               # screen blend
    assert np.abs(a - b).mean() > 1            # it drifts
    assert np.array_equal(a, np.asarray(shaderfx.apply(im, "leak", 0.0), np.int16))


@gl
def test_aberration_splits_the_edges_not_the_centre():
    px = np.zeros((H, W, 3), np.uint8)
    px[:, ::16] = 255                          # thin white lines everywhere
    out = np.asarray(shaderfx.apply(Image.fromarray(px), "aberration", 0.0), np.int16)
    centre = out[H // 2 - 4:H // 2 + 4, W // 2 - 8:W // 2 + 8]
    edge = out[:, :24]
    assert np.abs(centre[..., 0] - centre[..., 2]).mean() < 8
    assert np.abs(edge[..., 0] - edge[..., 2]).mean() > 8


@gl
def test_a_vignette_keeps_the_middle_and_darkens_the_corners():
    out = np.asarray(shaderfx.apply(grey(200), "vignette", 0.0), np.int16)
    assert abs(out[H // 2, W // 2].mean() - 200) <= 2
    assert out[2, 2].mean() < 150


@gl
def test_a_shader_shot_draws_through_and_passes_the_rest_on():
    class Inner:
        released = False

        def draw(self, f):
            return grey(200)

        def release(self):
            Inner.released = True

    s = shaderfx.ShaderShot(Inner(), ["vignette", ("leak", 0.4)], hold=3.0)
    assert s.draw(0.5).size == (W, H)
    s.release()
    assert Inner.released
