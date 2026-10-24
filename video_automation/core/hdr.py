"""SDR footage into an HLG file without changing how it looks on an HDR screen.

The conversion is exact in display light (BT.2408's display-referred route):
BT.1886 decode, scale so SDR white sits at `white` nits, BT.709 to BT.2020
primaries, then the inverse HLG OOTF and OETF for a 1000-nit display. Every
colour keeps its display-light ratios, so saturation survives; only the
brightness scale is a choice.

It is baked into a .cube for ffmpeg's `lut3d`, since this ffmpeg has no
`zscale`. Use the chain from

    `sdr_to_hlg_vf(cube)` - which also carries the swscale precision flags;
    without them the matrix steps alone cost ~10% brightness on graphics.

`hlg_display` and `sdr_display` model what a screen shows, for checking a
render against its source. Check on that model, not on a `scale_vt` tone map
back to SDR: the tone map was what the Spree trim was matched on, and the
trim it produced drains colour on the HDR phone the video is watched on.
"""

import subprocess
from pathlib import Path

import numpy as np

from . import guard

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


# ---------------------------------------------------------------------------
# When a short goes HDR, and the pass that makes it.
#
# **Only when a source is natively HDR** - an iPhone clip (HLG), or drone
# footage recorded in HLG. Decided 2026-10-20 after Akra. Converting SDR
# footage up adds brightness and nothing else: no highlight range, no colour.
# Explanatory crypto/tinnitus shorts and quizzes stay SDR (white cards glare,
# brand colours stop matching the thumbnails and site); zen sessions stay SDR
# (watched at night, the point is calm); SDR-only drone quote shorts stay SDR
# unless the user asks. Untested risk on every HDR upload: an upload path
# (n8n Reels, the TikTok API) that drops the HLG tags shows the file
# washed-out, and nothing in the build can see that.
HDR_WHITE = 400                         # nits SDR white lands at; see Akra

SAT_TOLERANCE = 0.02                    # display-light saturation, absolute
NITS_TOLERANCE = 0.05                   # mean display luminance, relative,
NITS_FLOOR = 1.5                        # or absolute: swscale's ~1-level rounding
                                        # bias is 7% of a 12-nit near-black card
                                        # (under 1 nit) and 2% on daylight footage
_Y709 = np.array([0.2126, 0.7152, 0.0722])

# swscale converts YUV<->RGB at 8-bit-ish precision by default: ~4 levels of
# 255 on flat patches, ~10% brightness on a graphics-heavy frame. These flags
# take it to ~1-2 levels. Every matrix conversion in this module carries them.
SWS = "accurate_rnd+full_chroma_int+full_chroma_inp"

X265_HLG = ["-c:v", "libx265", "-crf", "18", "-preset", "slow", "-tag:v", "hvc1",
            "-pix_fmt", "yuv420p10le",
            "-x265-params", "log-level=error:colorprim=bt2020:"
                            "transfer=arib-std-b67:colormatrix=bt2020nc:range=limited",
            "-color_primaries", "bt2020", "-color_trc", "arib-std-b67",
            "-colorspace", "bt2020nc", "-color_range", "tv"]


def _probe(path: Path, entries: str) -> str:
    return subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         entries, "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()


def is_hlg(path: Path) -> bool:
    """True for an HLG source - an iPhone HDR clip, or HLG drone footage.

    A file ffprobe cannot read is not HLG; the renderer will fail on it with
    its own, clearer error.
    """
    try:
        return _probe(Path(path), "stream=color_transfer") == "arib-std-b67"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def wants_hdr(sources) -> bool:
    """A cut goes HDR when, and only when, one of its sources is HLG."""
    return any(is_hlg(p) for p in sources)


def refuse_hlg(*sources) -> None:
    """For the SDR renderers: an HLG clip through an SDR chain comes out grey.

    They crop, overlay and encode as 8-bit BT.709, which reads HLG pixels as
    SDR with no tone map - the drained look of Spree's second render. A cut
    with an HLG source is built the way `akra-what-my-drone-sees.py` is.
    """
    bad = [str(p) for p in sources if p is not None and is_hlg(Path(p))]
    if bad:
        raise ValueError(
            "HLG source in an SDR renderer, it would come out grey: "
            + ", ".join(bad) + ". Build the cut in HLG like "
            "projects/drone-short/akra-what-my-drone-sees.py, converting the "
            "SDR clips with core.hdr.sdr_to_hlg_vf.")


def _sdr_matrix(path: Path) -> str:
    """How players decode this SDR file: its tag, or BT.709 when untagged.

    The renderers write untagged yuv420p, and the players these are watched
    in read untagged HD as BT.709 - so that is "how it looks now".
    """
    tag = _probe(path, "stream=color_space")
    return {"bt470bg": "bt601", "smpte170m": "bt601"}.get(tag, "bt709")


def sdr_to_hlg_vf(cube: Path, matrix: str = "bt709") -> str:
    """The filter chain from SDR yuv to HLG yuv420p10le, tags set.

    Append it to a chain whose last step is still SDR; nothing may follow it
    but the encode. `cube` comes from `write_sdr_to_hlg_cube`.
    """
    return (f"scale=in_color_matrix={matrix}:in_range=tv:flags={SWS},"
            f"format=rgb48le,lut3d=file='{cube}':interp=tetrahedral,"
            f"scale=out_color_matrix=bt2020:out_range=tv:flags={SWS},"
            "format=yuv420p10le,"
            "setparams=color_primaries=bt2020:color_trc=arib-std-b67:"
            "colorspace=bt2020nc:range=tv")


def _rgb(path: Path, t: float, matrix: str, w: int = 270, h: int = 480) -> np.ndarray:
    vf = (f"scale={w}:{h}:in_color_matrix={matrix}:in_range=tv:out_range=pc:"
          f"flags=area+{SWS},format=rgb48le")
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-ss", f"{t}", "-i", str(path), "-frames:v", "1",
         "-vf", vf, "-f", "rawvideo", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, "<u2").reshape(h, w, 3) / 65535


def _sat(d: np.ndarray) -> float:
    """Mean display-light saturation, weighted by luminance so near-black
    noise, where min/max is meaningless, does not dominate."""
    mx, mn = d.max(-1), d.min(-1)
    s = np.where(mx > 0, 1 - mn / np.maximum(mx, 1e-9), 0)
    w = d @ _Y709
    return float((s * w).sum() / max(w.sum(), 1e-9))


def check_hlg(sdr: Path, hlg: Path, white: float = HDR_WHITE,
              samples: int = 5) -> list[dict]:
    """Compare an HLG render with its SDR master as an HDR screen shows them.

    Raises if any sampled frame drifts past `SAT_TOLERANCE` or
    `NITS_TOLERANCE`. This is the check the first Akra renders never had:
    stills and a `scale_vt` tone map both looked fine while the phone showed
    the colour drained.
    """
    dur = float(_probe(sdr, "format=duration"))
    matrix = _sdr_matrix(sdr)
    rows = []
    for k in range(samples):
        t = dur * (k + 0.5) / samples
        s = sdr_display(_rgb(sdr, t, matrix), white)
        o = hlg_display(_rgb(hlg, t, "bt2020"))
        sn, on = float((s @ _Y709).mean()), float((o @ _Y709).mean())
        row = {"t": round(t, 2), "sat_sdr": _sat(s), "sat_hlg": _sat(o),
               "nits_sdr": sn, "nits_hlg": on}
        rows.append(row)
        bad_sat = abs(row["sat_hlg"] - row["sat_sdr"]) > SAT_TOLERANCE
        bad_nits = (abs(on - sn) > NITS_FLOOR
                    and abs(on / max(sn, 1e-9) - 1) > NITS_TOLERANCE)
        if bad_sat or bad_nits:
            raise ValueError(f"HLG colour drift at {t:.2f}s in {hlg.name}: {row}")
    return rows


def finish_hdr(out: Path, white: float = HDR_WHITE,
               workdir: Path | None = None) -> Path:
    """Turn a finished SDR file into HLG in place, keeping `<stem>-sdr.mp4`.

    For an SDR-only cut the user has asked to ship in HDR. It runs on the
    finished file, after every grade, overlay and caption, so nothing can
    touch the picture once it is HLG. Audio is copied. The SDR master stays
    beside it as the fallback for any platform that mishandles HDR. Fails,
    leaving the SDR file at `out`, if `check_hlg` sees drift.
    """
    sdr = out.with_name(f"{out.stem}-sdr{out.suffix}")
    out.replace(sdr)
    cube_dir = workdir or out.parent
    cube_dir.mkdir(parents=True, exist_ok=True)
    cube = write_sdr_to_hlg_cube(cube_dir / f".sdr-to-hlg-{int(white)}.cube", white)
    try:
        guard.run(
            ["ffmpeg", "-v", "error", "-y", "-i", str(sdr), "-map", "0:v",
             "-map", "0:a?", "-vf", sdr_to_hlg_vf(cube, _sdr_matrix(sdr)),
             *X265_HLG, "-c:a", "copy", "-movflags", "+faststart", str(out)],
            out, capture_output=True)
        check_hlg(sdr, out, white)
    except Exception:
        out.unlink(missing_ok=True)
        sdr.replace(out)
        raise
    finally:
        if workdir is None:
            cube.unlink(missing_ok=True)
    return out
