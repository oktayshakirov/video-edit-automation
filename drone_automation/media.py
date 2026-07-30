"""Everything that shells out to ffmpeg/ffprobe, plus clip identity.

Source files are only ever read for hashing (2MB) and proxy generation.
No CV ever touches them.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from .config import PROXY_FPS, PROXY_WIDTH, VIDEO_EXTS


class ToolMissing(RuntimeError):
    pass


def require_tools() -> None:
    """Fail loudly and early rather than mid-scan with a cryptic skip."""
    missing = [t for t in ("ffmpeg", "ffprobe") if shutil.which(t) is None]
    if missing:
        raise ToolMissing(
            f"{' and '.join(missing)} not found on PATH. Install with: brew install ffmpeg"
        )


def is_clip(path: Path) -> bool:
    """Real video file, not macOS metadata cruft.

    AppleDouble sidecars ('._City 1.mp4') carry a video extension and a 4KB
    resource fork. Without this filter they get probed, fail, and pad the scan
    with false skips.
    """
    if path.suffix.lower() not in VIDEO_EXTS:
        return False
    return not path.name.startswith("._") and not path.name.startswith(".")


def quick_hash(path: Path) -> str:
    """Cheap stable ID: size + first and last 1MB. Avoids hashing 4K files."""
    size = path.stat().st_size
    h = hashlib.sha256()
    h.update(str(size).encode())
    chunk = 1 << 20
    with path.open("rb") as f:
        h.update(f.read(chunk))
        if size > chunk * 2:
            f.seek(-chunk, os.SEEK_END)
            h.update(f.read(chunk))
    return h.hexdigest()[:16]


def ffprobe_meta(path: Path) -> dict | None:
    cmd = [
        "ffprobe", "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path),
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

    data = json.loads(out)
    video = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    if video is None:
        return None

    num, _, den = video.get("r_frame_rate", "0/1").partition("/")
    try:
        fps = float(num) / float(den) if float(den) else 0.0
    except ValueError:
        fps = 0.0

    duration = float(data.get("format", {}).get("duration") or video.get("duration") or 0.0)

    return {
        "duration": duration,
        "fps": fps,
        "width": int(video.get("width") or 0),
        "height": int(video.get("height") or 0),
        "codec": video.get("codec_name", ""),
        "created": data.get("format", {}).get("tags", {}).get("creation_time", ""),
    }


def build_proxy(src: Path, dst: Path) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-v", "error", "-y",
        "-i", str(src),
        "-vf", f"fps={PROXY_FPS},scale={PROXY_WIDTH}:-2",
        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
        "-pix_fmt", "yuv420p",
        str(dst),
    ]
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return dst.exists() and dst.stat().st_size > 0
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
