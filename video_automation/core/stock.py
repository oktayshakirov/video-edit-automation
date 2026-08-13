"""Pexels photos and video clips, cached on disk.

**This reverses a rule both short skills state**, so it is worth being explicit
about what changed rather than quietly contradicting them. Their rule is: do not
reach for a stock API, because an AI voice read over generic stock loops is
exactly the pattern the platforms suppress. That reasoning is still correct and
still applies to a thirty-second short built from three pictures.

What is different here is arithmetic, not taste. A three-minute video needs
about thirty shots and a post owns three to five images, so **every long-form
video built only from the site library will contain most of the same
photographs as every other one** — which is its own kind of sameness, and the
one the user actually noticed. The rule that survives is the real one:

> Stock is a *supporting* layer. The site's own images and the drawn beats lead.

A video that is wall-to-wall stock loops is the failure the short skills
describe. A video whose argument is carried by drawn beats and the site's own
pictures, with stock filling the gaps and supplying motion, is not.

Key: the same `.pexels-api-key` the `publish-content` skill uses. Pexels needs
no attribution and permits commercial use, so nothing here has to be credited —
but the manifest keeps the photographer and URL anyway, because the moment that
licence changes we want to know what came from where.

Downloads are cached under `assets/stock/<kind>/<slug>/` and committed
deliberately, exactly as `assets/README.md` already argues for the drone
project's location pin: a build that silently re-downloads is a build that
cannot be reproduced once a photographer deletes their upload.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path

KEY_PATH = Path.home() / "Coding/crypto-wiki-automation/.pexels-api-key"
CACHE = Path(__file__).resolve().parents[2] / "assets/stock"

PHOTO_API = "https://api.pexels.com/v1/search"
VIDEO_API = "https://api.pexels.com/videos/search"


def _key() -> str:
    if not KEY_PATH.exists():
        raise RuntimeError(
            f"no Pexels key at {KEY_PATH}. It is gitignored; create it with a "
            f"free key from https://www.pexels.com/api/ — the publish-content "
            f"skill uses the same file.")
    return KEY_PATH.read_text().strip()


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


# Pexels 403s urllib's default `Python-urllib/3.x` User-Agent on both the API
# and the CDN, while the identical request from curl succeeds. Every call here
# has to carry a browser-ish UA or it fails with a bare Forbidden and no hint.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def _get(url: str, params: dict) -> dict:
    req = urllib.request.Request(
        f"{url}?{urllib.parse.urlencode(params)}",
        headers={"Authorization": _key(), "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


@dataclass
class Asset:
    """One cached file, plus where it came from."""
    path: Path
    kind: str                   # "photo" | "video"
    width: int
    height: int
    credit: str
    url: str
    duration: float = 0.0


def _download(src: str, dest: Path) -> Path:
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    req = urllib.request.Request(src, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r, open(tmp, "wb") as f:
        while chunk := r.read(1 << 16):
            f.write(chunk)
    tmp.rename(dest)
    return dest


def photos(query: str, n: int = 3, min_w: int = 1600,
           cache: Path = CACHE) -> list[Asset]:
    """Landscape photographs for `query`, cached.

    `min_w` is 1600 rather than the 750 the vertical format needs. A long-form
    frame is 1920 wide and a stock library has no reason to make us upscale —
    unlike the site's own archive, where the small sources are simply the
    pictures that exist.
    """
    out, slug = [], _slug(query)
    data = _get(PHOTO_API, {"query": query, "per_page": max(n * 3, 9),
                            "orientation": "landscape", "size": "large"})
    for p in data.get("photos", []):
        if p["width"] < min_w:
            continue
        dest = cache / "photos" / slug / f"{p['id']}.jpg"
        out.append(Asset(_download(p["src"]["original"], dest), "photo",
                         p["width"], p["height"],
                         p.get("photographer", ""), p.get("url", "")))
        if len(out) >= n:
            break
    return out


def videos(query: str, n: int = 2, min_w: int = 1920,
           max_dur: float = 30.0, cache: Path = CACHE) -> list[Asset]:
    """Landscape video clips for `query`, cached.

    Prefers the smallest file at or above `min_w`. Pexels serves several
    renditions per clip and the 4K one is frequently 80 MB for six seconds of
    footage that is going to be scaled to 1080 and dimmed — the highest
    resolution available is almost never the right choice here.
    """
    out, slug = [], _slug(query)
    data = _get(VIDEO_API, {"query": query, "per_page": max(n * 3, 9),
                            "orientation": "landscape", "size": "medium"})
    for v in data.get("videos", []):
        if v.get("duration", 0) > max_dur:
            continue
        files = [f for f in v.get("video_files", [])
                 if (f.get("width") or 0) >= min_w and f.get("file_type") == "video/mp4"]
        if not files:
            continue
        pick = min(files, key=lambda f: f["width"])
        dest = cache / "videos" / slug / f"{v['id']}.mp4"
        out.append(Asset(_download(pick["link"], dest), "video",
                         pick["width"], pick["height"],
                         (v.get("user") or {}).get("name", ""),
                         v.get("url", ""), float(v.get("duration", 0))))
        if len(out) >= n:
            break
    return out


# Both sites are dark palettes — gold on near-black, peach on near-black. Stock
# brighter or more saturated than this cuts *out* of the video rather than into
# it, and the grade in `VideoShot` can only pull so far. Measured on real
# candidates: the rejects were a bitcoin sticker on a pine table (L86 S44), a
# green "matrix" rain (L36 S94) and a novelty dinosaur (L91 S62); the keepers
# were a wireframe wave (L4 S5), a numeral tunnel (L14 S6) and a circuit macro
# (L41 S20).
MAX_LUMA, MAX_SAT = 48.0, 50.0


def screen(path: Path, at: float = 1.0) -> tuple[float, float]:
    """Mean luminance and mean saturation of a frame, both 0-255.

    Cheap, and the single most useful number when picking stock for a dark
    channel — far more reliable than the search query, which returns whatever
    the platform's popularity ranking feels like that day.
    """
    import cv2
    import numpy as np

    if path.suffix.lower() in (".mp4", ".mov", ".webm"):
        cap = cv2.VideoCapture(str(path))
        cap.set(cv2.CAP_PROP_POS_MSEC, at * 1000)
        ok, bgr = cap.read()
        cap.release()
        if not ok:
            return 255.0, 255.0
    else:
        bgr = cv2.imread(str(path))
        if bgr is None:
            return 255.0, 255.0
    a = bgr.astype(np.float32)
    return float(a.mean()), float((a.max(2) - a.min(2)).mean())


def keep(path: Path, max_luma: float = MAX_LUMA,
         max_sat: float = MAX_SAT) -> bool:
    """Whether an asset is dark and desaturated enough to cut into these videos."""
    lum, sat = screen(path)
    return lum <= max_luma and sat <= max_sat


def manifest(assets: list[Asset], out: Path) -> Path:
    """Write what was pulled and from where, next to the cache."""
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(
        [{"path": str(a.path.relative_to(CACHE)), "kind": a.kind,
          "size": [a.width, a.height], "duration": a.duration,
          "credit": a.credit, "url": a.url} for a in assets],
        indent=2), encoding="utf-8")
    return out
