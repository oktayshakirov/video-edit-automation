"""Depth and subject mattes from one photograph.

Two local models, both run through the onnxruntime already pinned for Kokoro:

* **depth** - Depth Anything V2 *Small* (Apache-2.0). How near each pixel is,
  which is what lets a still move in depth (`Shot(parallax=)`) instead of as
  one flat affine. Only the Small checkpoint is Apache-2.0; Base, Large and
  Giant are CC-BY-NC-4.0 and must never be swapped in here.
* **matte** - BiRefNet, general, Swin-tiny "lite" (MIT). The subject's alpha,
  hair included: the cutout behind `behind`, `Shot(isolate=)`, `Shot(pop=)`
  and `thumb.subject_front`.

    python -m video_automation vision fetch     # ~320MB, once
    python -m video_automation vision status
    python -m video_automation vision preview photo.jpg

**Both are cached by image content**, like the narration. A matte costs ~17s
on a CPU and a re-cut changes the shot list, not the photograph, so the model
runs once per picture, ever. The cache holds the model's raw output at model
resolution (float16, 0.5-2MB); resizing back to the picture is deterministic
and cheap, so a change of crop, zoom or frame never misses.

The weights are pinned by SHA-256, for the reason the TTS pins are exact in
`requirements.txt`: a different checkpoint is a different picture, and a cache
keyed on a file name would serve the old one's output to the new.
"""

from __future__ import annotations

import hashlib
import os
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

MODELS_DIR = Path(os.environ.get(
    "VIDEO_AUTOMATION_MODELS", Path.home() / ".local/share/video-automation/models"))
CACHE = Path(os.environ.get(
    "VIDEO_AUTOMATION_VISION_CACHE", Path.home() / ".cache/video-automation/vision"))

_MEAN = np.array([0.485, 0.456, 0.406], np.float32)
_STD = np.array([0.229, 0.224, 0.225], np.float32)


@dataclass(frozen=True)
class Model:
    file: str
    url: str
    sha256: str
    size: int           # square input side
    license: str


MODELS = {
    "depth": Model(
        "depth-anything-v2-small.onnx",
        "https://github.com/fabio-sim/Depth-Anything-ONNX/releases/download/"
        "v2.0.0/depth_anything_v2_vits.onnx",
        "d2b11a11c1d4a12b47608fa65a17ee9a4c605b55ee1730c8e3b526304f2562be",
        518, "Apache-2.0 (Small only)"),
    "matte": Model(
        "birefnet-general-lite.onnx",
        "https://github.com/danielgatis/rembg/releases/download/v0.0.0/"
        "BiRefNet-general-bb_swin_v1_tiny-epoch_232.onnx",
        "5600024376f572a557870a5eb0afb1e5961636bef4e1e22132025467d0f03333",
        1024, "MIT"),
}

_sessions: dict = {}


class MissingModel(FileNotFoundError):
    pass


def model_path(name: str) -> Path:
    return MODELS_DIR / MODELS[name].file


def _session(name: str):
    if name in _sessions:
        return _sessions[name]
    p = model_path(name)
    if not p.exists():
        raise MissingModel(
            f"the {name} model is not installed ({p}). Run "
            f"`python -m video_automation vision fetch` - it downloads "
            f"{MODELS[name].file} once and checks its hash.")
    import onnxruntime as ort
    _sessions[name] = ort.InferenceSession(str(p),
                                           providers=["CPUExecutionProvider"])
    return _sessions[name]


def as_rgb(img) -> np.ndarray:
    """A Path, a PIL image or an array, as contiguous RGB uint8."""
    if isinstance(img, (str, Path)):
        img = Image.open(img)
    if isinstance(img, Image.Image):
        img = np.asarray(img.convert("RGB"))
    img = np.asarray(img)
    if img.ndim == 2:
        img = np.stack([img] * 3, axis=2)
    return np.ascontiguousarray(img[:, :, :3], np.uint8)


def cache_key(name: str, rgb: np.ndarray) -> str:
    """The model's own hash and every pixel: either changing is a miss."""
    h = hashlib.sha256()
    h.update(MODELS[name].sha256.encode())
    h.update(str(rgb.shape).encode())
    h.update(rgb.tobytes())
    return h.hexdigest()


def _raw(name: str, rgb: np.ndarray) -> np.ndarray:
    """The model's output at model resolution, from the cache or a run."""
    key = cache_key(name, rgb)
    f = CACHE / name / f"{key[:2]}/{key}.npy"
    if f.exists():
        try:
            return np.load(f).astype(np.float32)
        except (OSError, ValueError):
            f.unlink(missing_ok=True)       # a torn write; run it again
    s = _session(name)
    size = MODELS[name].size
    x = cv2.resize(rgb, (size, size), interpolation=cv2.INTER_AREA)
    x = ((x.astype(np.float32) / 255.0 - _MEAN) / _STD).transpose(2, 0, 1)[None]
    y = np.asarray(s.run(None, {s.get_inputs()[0].name: x})[0],
                   np.float32).squeeze()
    f.parent.mkdir(parents=True, exist_ok=True)
    tmp = f.with_suffix(".part.npy")
    np.save(tmp, y.astype(np.float16))
    tmp.replace(f)
    return y


def depth(img) -> np.ndarray:
    """How near each pixel is, at the picture's size: 1.0 nearest, 0.0 farthest.

    Normalised on the 1st and 99th percentiles, so a few specular pixels do
    not flatten the rest of the range.
    """
    rgb = as_rgb(img)
    d = cv2.resize(_raw("depth", rgb), (rgb.shape[1], rgb.shape[0]),
                   interpolation=cv2.INTER_CUBIC)
    lo, hi = np.percentile(d, 1), np.percentile(d, 99)
    return np.clip((d - lo) / max(hi - lo, 1e-6), 0.0, 1.0).astype(np.float32)


def matte(img) -> np.ndarray:
    """The subject's alpha at the picture's size, 0..1.

    The logits are resized before the sigmoid, not after: resizing a hard
    0/1 mask softens every edge by the upscale factor, where resizing the
    logits keeps the transition as narrow as the model made it.
    """
    rgb = as_rgb(img)
    logit = cv2.resize(_raw("matte", rgb), (rgb.shape[1], rgb.shape[0]),
                       interpolation=cv2.INTER_CUBIC)
    return (1.0 / (1.0 + np.exp(-logit))).astype(np.float32)


def cutout(img) -> Image.Image:
    """The picture as RGBA, everything but the subject transparent."""
    rgb = as_rgb(img)
    a = (matte(rgb) * 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, a]), "RGBA")


def alpha_of(img) -> np.ndarray | None:
    """An RGBA picture's own alpha as 0..1, or None if it has none.

    A hand-made cutout is used as it is: the model never second-guesses a
    matte somebody drew.
    """
    if isinstance(img, (str, Path)):
        img = Image.open(img)
    if isinstance(img, Image.Image) and img.mode in ("RGBA", "LA"):
        a = np.asarray(img.getchannel("A"), np.float32) / 255.0
        return a if a.min() < 0.99 else None
    return None


# --- the command line ------------------------------------------------------


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(names=None) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for name in names or MODELS:
        m, p = MODELS[name], model_path(name)
        if p.exists() and _sha(p) == m.sha256:
            print(f"  {name:6s} ok       {p}")
            continue
        print(f"  {name:6s} fetching {m.url}")
        tmp = p.with_suffix(".part")
        urllib.request.urlretrieve(m.url, tmp)
        got = _sha(tmp)
        if got != m.sha256:
            tmp.unlink(missing_ok=True)
            raise SystemExit(f"{name}: hash mismatch ({got}) - not installed")
        tmp.replace(p)
        print(f"  {name:6s} ok       {p}  ({m.license})")


def main(argv: list[str]) -> int:
    cmd = argv[0] if argv else "status"
    if cmd == "fetch":
        fetch(argv[1:] or None)
        return 0
    if cmd == "status":
        for name, m in MODELS.items():
            p = model_path(name)
            state = "installed" if p.exists() else "missing - run `vision fetch`"
            print(f"  {name:6s} {state:30s} {m.file}  {m.license}")
        print(f"  cache  {CACHE}")
        return 0
    if cmd == "preview" and len(argv) > 1:
        src = Path(argv[1])
        rgb = as_rgb(src)
        out = Path.home() / "Desktop"
        d = (depth(rgb) * 255).astype(np.uint8)
        cv2.imwrite(str(out / f"{src.stem}-depth.png"),
                    cv2.applyColorMap(d, cv2.COLORMAP_INFERNO))
        cutout(rgb).save(out / f"{src.stem}-cutout.png")
        print(out / f"{src.stem}-depth.png")
        print(out / f"{src.stem}-cutout.png")
        return 0
    print("usage: vision fetch | status | preview IMAGE", file=sys.stderr)
    return 1
