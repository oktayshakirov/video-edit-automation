"""Animated emoji for the beats' icons: Google's Noto Emoji Animation.

`grid`, `steps` and `diagram` draw an emoji as an item's icon
(`core.vertical.emoji_image`). With animated emoji on, an icon that has a Noto
animation plays it - the fire flickers, the lock clicks - looping in step
with the beat's own clock. **On by default since 2026-11-06** (the editor
asked why a diagram's icons were still static): `animated_emoji=False` on
`render_long` / `render_crypto_short` gives every frame as it always was.

    python -m video_automation emoji check 🔥 🔒 💰    # which ones animate
    python -m video_automation emoji fetch 🔥 🔒

**Only some emoji animate.** Noto animates about a thousand; 💰 and 📋 have
no animation (measured 2026-11-05). Those stay the static Apple glyph, which
is a different drawing style - so check a beat whose icons are mixed, or pick
icons that all animate (`emoji check`). A miss is remembered (`.none`) so it
is not asked for again on every frame of every build.

Files are fetched once into `~/.local/share/video-automation/emoji/` - 512px
animated WebP, ~200KB, 30ms a frame. **No credit line is added to a
video** for them - not to a long form's `Meta.credits`, not to a Short's
description (the editor's call, 2026-11-05).
"""

from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from PIL import Image

CDN = "https://fonts.gstatic.com/s/e/notoemoji/latest/{code}/512.webp"
DIR = Path(os.environ.get("VIDEO_AUTOMATION_EMOJI",
                          Path.home() / ".local/share/video-automation/emoji"))

_on = False
_clips: dict[str, "Clip | None"] = {}


@contextmanager
def enabled(on: bool = True):
    """Animated icons on for the duration of one build."""
    global _on
    before, _on = _on, bool(on)
    try:
        yield
    finally:
        _on = before


def active() -> bool:
    return _on


def code(char: str) -> str:
    """Noto's file name: codepoints in hex, joined by `_`, without VS16."""
    return "_".join(f"{ord(c):x}" for c in char if ord(c) != 0xFE0F)


def fetch(char: str) -> Path | None:
    """The animation for `char`, downloaded once; None if Noto has none."""
    DIR.mkdir(parents=True, exist_ok=True)
    p, miss = DIR / f"{code(char)}.webp", DIR / f"{code(char)}.none"
    if p.exists():
        return p
    if miss.exists():
        return None
    try:
        with urllib.request.urlopen(CDN.format(code=code(char)), timeout=20) as r:
            data = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            miss.touch()                    # no animation exists - remember
        return None
    except OSError as e:                    # offline: try again next build
        print(f"  ! emoji {char}: not fetched ({e}) - static glyph used",
              file=sys.stderr)
        return None
    tmp = p.with_suffix(".part")
    tmp.write_bytes(data)
    tmp.replace(p)
    return p


class Clip:
    """One animation's frames, cropped to the ink of *all* of them.

    Cropping each frame to its own ink would change its size frame to frame
    and the icon would breathe. One union box keeps it the same size and in
    the same place as it moves.
    """

    def __init__(self, path: Path):
        im = Image.open(path)
        frames, self.durations = [], []
        for i in range(getattr(im, "n_frames", 1)):
            im.seek(i)
            im.load()
            frames.append(np.asarray(im.convert("RGBA")))
            self.durations.append(max(10, int(im.info.get("duration") or 33)))
        alpha = np.max([f[:, :, 3] for f in frames], axis=0)
        ys, xs = np.nonzero(alpha > 8)
        box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1) if len(xs) else \
            (0, 0, alpha.shape[1], alpha.shape[0])
        self.frames = [Image.fromarray(f[box[1]:box[3], box[0]:box[2]], "RGBA")
                       for f in frames]
        self.ends = np.cumsum(self.durations) / 1000.0
        self.length = float(self.ends[-1])
        self._scaled: dict = {}

    def index(self, t: float) -> int:
        return int(np.searchsorted(self.ends, t % self.length, side="right")) \
            % len(self.frames)

    def at(self, t: float, height: int) -> Image.Image:
        i = self.index(t)
        key = (i, height)
        if key not in self._scaled:
            f = self.frames[i]
            w = max(1, int(f.width * height / f.height))
            self._scaled[key] = f.resize((w, height), Image.LANCZOS)
        return self._scaled[key]


def clip(char: str) -> Clip | None:
    if char not in _clips:
        p = fetch(char)
        _clips[char] = Clip(p) if p else None
    return _clips[char]


def frame(char: str, height: int, t: float) -> Image.Image | None:
    """The animated icon at time `t`, or None (off, or no animation)."""
    if not _on:
        return None
    c = clip(char)
    if c is None:
        return None
    return c.at(t, height)


def main(argv: list[str]) -> int:
    if len(argv) < 2 or argv[0] not in ("check", "fetch"):
        print("usage: emoji check|fetch EMOJI...", file=sys.stderr)
        return 1
    for ch in argv[1:]:
        p = fetch(ch)
        state = f"animated   {p}" if p else "static only (Noto has no animation)"
        print(f"  {ch}  {code(ch):18s} {state}")
    return 0
