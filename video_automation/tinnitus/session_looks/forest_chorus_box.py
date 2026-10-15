"""The look for `forest-chorus-box-breathing` (long + Short), and only that.

`canopy-fog` from the 2026-10-15 test round: misty jungle-canopy footage,
forward then reversed, graded down, a few fireflies. Pexels 19366762 by
Florian Delee (https://www.pexels.com/video/fog-tropic-jungle-latin-america-19366762/),
read from the stock cache, which is not in git - re-pull by that id if it is
missing (the 1920 rendition Pexels lists is served at 1280x720).

**Not for reuse.** Each session gets its own look in its own style; this file
exists so this one video can still be re-rendered, not as a library entry.
The reusable part is `core.looks` - start the next look from there.

    from video_automation.tinnitus.session_looks.forest_chorus_box import CanopyFog
"""

from __future__ import annotations

import subprocess

import numpy as np

from ...core.looks import Fireflies, Look, vignette
from ...core.stock import CACHE


class CanopyFog(Look):
    """Real footage, forward then reversed so the join is exact.

    The ping-pong cycle has to divide `period`, and the source is only so
    long, so the cycle is `period / k` for the smallest whole `k` the clip can
    cover. Fog has no arrow of time, which is why it reverses invisibly. The
    source is 1280x720, so a portrait crop is a ~2.7x upscale — soft, which fog
    forgives and almost nothing else would.
    """

    ring = (210, 240, 214)
    SRC = CACHE / "videos/jungle-canopy-fog/19366762.mp4"

    def __init__(self, w, h, period, pattern=None, fps: int = 30,
                 start: float = 1.0):
        super().__init__(w, h, period, pattern)
        if not self.SRC.exists():
            raise FileNotFoundError(
                f"{self.SRC} — re-pull Pexels 19366762 into this path")
        have = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(self.SRC)], capture_output=True,
            text=True, check=True).stdout) - start - 0.3
        k = 1
        while period / k / 2 > have:
            k += 1
        self.cycle = period / k
        half = int(round(self.cycle / 2 * fps))
        self.fps = fps
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(start), "-t",
             f"{self.cycle / 2 + 0.3:.3f}", "-i", str(self.SRC), "-vf",
             f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,"
             f"crop={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
            capture_output=True, check=True).stdout
        self.frames = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)[:half + 1]
        n = len(self.frames)
        # every source frame once except the two extremes (core.backdrop.pingpong)
        self.seq = list(range(n)) + list(range(n - 2, 0, -1))
        self.grade = (0.62 * np.array([0.80, 0.98, 0.90], np.float32)
                      * vignette(w, h, 0.6))
        self.ff = Fireflies(w, h, 18, 3, margin=(0.05, 0.32), r=(2, 5))

    def at(self, t):
        i = int(round((t % self.cycle) * self.fps)) % len(self.seq)
        f = self.frames[self.seq[i]].astype(np.float32) * self.grade
        self.ff.draw(f, t, self.period, 0.55)
        return np.clip(f, 0, 255).astype(np.uint8)
