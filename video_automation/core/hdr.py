"""SDR footage into an HLG file without changing how it looks on an HDR screen.

The conversion is exact in display light (BT.2408's display-referred route):
BT.1886 decode, scale so SDR white sits at `white` nits, BT.709 to BT.2020
primaries, then the inverse HLG OOTF and OETF for a 1000-nit display. Every
colour keeps its display-light ratios, so saturation survives; only the
brightness scale is a choice.

It is baked into a .cube for ffmpeg's `lut3d`, since this ffmpeg has no
`zscale`. Apply it on full-range RGB and convert out with the BT.2020 matrix:

    format=rgb48le,lut3d=file=X.cube:interp=tetrahedral,
    scale=out_color_matrix=bt2020:out_range=tv,format=yuv420p10le

`hlg_display` and `sdr_display` model what a screen shows, for checking a
render against its source. Check on that model, not on a `scale_vt` tone map
back to SDR: the tone map was what the Spree trim was matched on, and the
trim it produced drains colour on the HDR phone the video is watched on.
"""

from pathlib import Path

import numpy as np

_A, _B, _C = 0.17883277, 0.28466892, 0.55991073
LW, GAMMA = 1000.0, 1.2                 # nominal HLG display: peak, system gamma
_M709_2020 = np.array([[0.6274, 0.3293, 0.0433],
                       [0.0691, 0.9195, 0.0114],
                       [0.0164, 0.0880, 0.8956]])
_M2020_709 = np.linalg.inv(_M709_2020)
_Y2020 = np.array([0.2627, 0.6780, 0.0593])


def _oetf(e: np.ndarray) -> np.ndarray:
    e = np.clip(e, 0, 1)
    return np.where(e <= 1 / 12, np.sqrt(3 * e),
                    _A * np.log(np.maximum(12 * e - _B, 1e-12)) + _C)


def _oetf_inv(v: np.ndarray) -> np.ndarray:
    v = np.clip(v, 0, 1)
    return np.where(v <= 0.5, v * v / 3, (np.exp((v - _C) / _A) + _B) / 12)


def sdr_display(rgb709: np.ndarray, white: float) -> np.ndarray:
    """Full-range BT.709 RGB in [0,1] to display nits, SDR white at `white`."""
    return (np.clip(rgb709, 0, 1) ** 2.4) * white


def sdr_to_hlg(rgb709: np.ndarray, white: float) -> np.ndarray:
    """Full-range BT.709 RGB in [0,1] to an HLG BT.2020 signal in [0,1]."""
    fd = sdr_display(rgb709, white) @ _M709_2020.T
    ys = (np.maximum(fd @ _Y2020, 1e-9) / LW) ** (1 / GAMMA)
    return _oetf(fd / (LW * ys[..., None] ** (GAMMA - 1)))


def hlg_display(sig2020: np.ndarray) -> np.ndarray:
    """HLG BT.2020 signal to display nits in BT.709 primaries."""
    e = _oetf_inv(sig2020)
    ys = np.maximum(e @ _Y2020, 1e-12)
    return (LW * ys[..., None] ** (GAMMA - 1) * e) @ _M2020_709.T


def hlg_signal_of_white(white: float) -> float:
    """The HLG signal level SDR white lands on, for dimming overlays to match."""
    return float(sdr_to_hlg(np.ones(3), white)[0])


def write_sdr_to_hlg_cube(path: Path, white: float, size: int = 65) -> Path:
    g = np.linspace(0, 1, size)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")     # .cube order: red fastest
    out = sdr_to_hlg(np.stack([r, gg, b], -1).reshape(-1, 3), white)
    with open(path, "w") as f:
        f.write(f"LUT_3D_SIZE {size}\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n")
        np.savetxt(f, out, fmt="%.6f")
    return path
