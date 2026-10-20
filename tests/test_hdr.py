"""The SDR-to-HLG conversion keeps colour, and the SDR renderers refuse HLG.

What these cover is exactly what Akra got wrong for six renders and nothing
on screen could show: saturation surviving the trip into HLG as an HDR
screen displays it.
"""

import subprocess

import numpy as np
import pytest

from video_automation.core.hdr import (hlg_display, is_hlg, refuse_hlg,
                                       sdr_display, sdr_to_hlg,
                                       write_sdr_to_hlg_cube)

RNG = np.random.default_rng(7)


def _sat(d):
    mx, mn = d.max(-1), d.min(-1)
    return np.where(mx > 1e-6, 1 - mn / np.maximum(mx, 1e-9), 0)


@pytest.mark.parametrize("white", [203, 400, 600])
def test_display_light_is_exact(white):
    rgb = RNG.uniform(0.02, 1.0, (2000, 3))
    want = sdr_display(rgb, white)
    got = hlg_display(sdr_to_hlg(rgb, white))
    assert np.allclose(got, want, rtol=1e-6, atol=1e-6)


def test_saturation_survives():
    rgb = RNG.uniform(0.05, 1.0, (2000, 3))
    want = _sat(sdr_display(rgb, 400))
    got = _sat(hlg_display(sdr_to_hlg(rgb, 400)))
    assert np.abs(got - want).max() < 1e-6


def test_white_lands_on_its_nits():
    for white in (203, 400):
        nits = hlg_display(sdr_to_hlg(np.ones(3), white))
        assert np.allclose(nits, white, rtol=1e-6)


def test_cube_matches_the_maths(tmp_path):
    cube = write_sdr_to_hlg_cube(tmp_path / "c.cube", 400, size=9)
    rows = np.loadtxt(cube, skiprows=3)
    assert rows.shape == (9 ** 3, 3)
    g = np.linspace(0, 1, 9)
    # .cube order: red fastest - entry 1 is (g[1], 0, 0), entry 9 is (0, g[1], 0)
    assert np.allclose(rows[1], sdr_to_hlg(np.array([g[1], 0, 0]), 400), atol=1e-6)
    assert np.allclose(rows[9], sdr_to_hlg(np.array([0, g[1], 0]), 400), atol=1e-6)


def _clip(path, transfer):
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
         "color=c=gray:s=64x64:d=0.1", "-c:v", "libx265", "-pix_fmt", "yuv420p10le",
         "-x265-params", f"log-level=error:transfer={transfer}",
         "-color_trc", transfer, str(path)],
        check=True, capture_output=True)
    return path


def test_refuse_hlg(tmp_path):
    hlg = _clip(tmp_path / "hlg.mp4", "arib-std-b67")
    sdr = _clip(tmp_path / "sdr.mp4", "bt709")
    assert is_hlg(hlg) and not is_hlg(sdr)
    assert not is_hlg(tmp_path / "missing.mp4")
    refuse_hlg(sdr, None)
    with pytest.raises(ValueError, match="HLG source"):
        refuse_hlg(sdr, hlg)
