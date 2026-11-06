"""A still turned into a slow-push clip, for the slots that only take a clip.

**Built for the disclaimer (2026-11-06).** The compliance line's notice card
is drawn by `longform.clip.VideoShot._notice`, so it has to ride on a clip,
and every long form on the channel had put it over the same rain on a
window. The editor's note: "the final disclaimer screen always has rain on
the background which is not relevant to crypto, it should be relevant to
each video". The picture the video is *about* is usually a still - the
cover's image, a site photograph, a real object - so this turns one into a
clip the notice can sit on:

    from video_automation.core import stillclip
    BG = stillclip.make(ROOT / "assets/crypto/random-tokens/stranger.jpg")
    Shot(clip=BG, clip_at=0.5, payload=("", "This is not financial advice."))

A gentle centred push (`zoom` over `secs`), rendered once from a 2x
upscale so the zoompan's integer stepping never shows, and cached next to
the stock as `assets/stock/stills/<stem>-<hash>.mp4` (gitignored, like the
rest of the stock bytes: the still it came from is the record).
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

from .stock import CACHE

OUT = CACHE / "stills"


def path(image: Path, secs: float = 14.0, zoom: float = 1.10,
         size: tuple[int, int] = (1920, 1080), fps: int = 30,
         focus: tuple[float, float] = (0.5, 0.5)) -> Path:
    """Where `make` puts the clip for these arguments - without making it.

    A script's shot list names the clip with this, and its `main()` calls
    `make`, so a gate that imports the script never renders anything
    (`workflow.md`, "A script draws its generated files in a function")."""
    image = Path(image)
    key = hashlib.sha1(
        f"{image.resolve()}|{image.stat().st_size}|{secs}|{zoom}|{size}|{fps}|"
        f"{focus}".encode()).hexdigest()[:10]
    return OUT / f"{image.stem}-{key}.mp4"


def make(image: Path, secs: float = 14.0, zoom: float = 1.10,
         size: tuple[int, int] = (1920, 1080), fps: int = 30,
         focus: tuple[float, float] = (0.5, 0.5)) -> Path:
    """The clip for `image`, rendering it the first time it is asked for.

    `focus` is where the push heads, as fractions of the picture - (0.5, 0.3)
    pushes toward a face in the upper middle."""
    image = Path(image)
    out = path(image, secs, zoom, size, fps, focus)
    if out.exists():
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    w, h = size
    n = int(round(secs * fps))
    fx, fy = focus
    # Cover-crop to the frame's shape at 2x, the crop leaning toward `focus`
    # (a centred crop cut the stranger's hairline), then push in. zoompan's x/y are
    # the top-left of the window; centre it on `focus`, clamped to the image.
    vf = (f"scale={2 * w}:{2 * h}:force_original_aspect_ratio=increase,"
          f"crop={2 * w}:{2 * h}:'(iw-{2 * w})*{fx}':'(ih-{2 * h})*{fy}',"
          f"zoompan=z='1+({zoom}-1)*on/{max(1, n - 1)}':"
          f"x='max(0,min(iw-iw/zoom,iw*{fx}-iw/zoom/2))':"
          f"y='max(0,min(ih-ih/zoom,ih*{fy}-ih/zoom/2))':"
          f"d={n}:s={w}x{h}:fps={fps},format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i",
                    str(image), "-vf", vf, "-frames:v", str(n),
                    "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                    str(out)], check=True)
    return out
