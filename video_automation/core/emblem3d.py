"""3D emblems: a lit, slowly swaying object in a beat's empty picture column,
in place of the four gold arcs (2026-11-21).

**Why.** The editor on the OktAI opener draft: "the graphics with the
circles which we also use in tinnitus and crypto is a little boring and
repetitive ... maybe instead of vectors we add something 3d or something
related and have different one for each video". The arcs (`Beat.emblem`)
were there to balance a `stat` or a `quote` and give the eye something
moving; they meant nothing and were the same in every video on both
channels.

**What.** Each object is built in Blender from primitives and curves by
`emblem3d_scene.py` (nothing downloaded), in two materials - the brand's
own metal and a dark gloss - lit from three sides, rendered as a 4.8 s loop
of transparent frames and cached (`CACHE`). The first use of an object in a
brand's colour renders it (about half a minute, four Blender processes);
after that it is a file read.

**Which one.** A shot names its own (`Shot(emblem="microphone")`), so a
script can put the microphone on the voice chapter's numbers and the chart
on the retention ones. A shot that does not falls back to the video's
emblem, picked once per render from the brand's set by the video's name -
so every video gets a different one with no script change, and the same
video always gets the same one. `emblem=None` on a shot keeps the old arcs.

Objects: microphone, headphones, coin, padlock, clapper, note, play, chart,
wave, bulb.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

BLENDER = Path(os.environ.get("BLENDER", "/Applications/Blender.app/Contents/MacOS/Blender"))
SCENE = Path(__file__).with_name("emblem3d_scene.py")
CACHE = Path(os.environ.get("VIDEO_AUTOMATION_EMBLEMS",
                            Path.home() / ".cache/video-automation/emblems"))
FRAMES = 120
FPS = 25
SIZE = 560
WORKERS = 4
VERSION = 1

OBJECTS = ("microphone", "headphones", "coin", "padlock", "clapper", "note",
           "play", "chart", "wave", "bulb")

# Each brand's set: the video's default emblem is picked from it by name.
SETS = {
    "crypto": ("coin", "padlock", "chart"),
    "tinnitus": ("headphones", "wave", "bulb"),
    "oktai": ("microphone", "play", "clapper", "chart", "bulb", "note"),
}

# Set per render by `use_for(brand, video_name)`; read by `Beat`.
CURRENT: str | None = None


def _linear(rgb) -> list[float]:
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return [round(lin(float(c)), 4) for c in rgb]


def folder(name: str, tint) -> Path:
    key = hashlib.sha1(json.dumps([VERSION, name, list(tint), FRAMES, SIZE,
                                   SCENE.read_text()]).encode()).hexdigest()[:10]
    return CACHE / f"{name}-{key}"


def render(name: str, tint=(255, 219, 112)) -> Path:
    """The loop's frame folder, rendered once."""
    if name not in OBJECTS:
        raise ValueError(f"unknown emblem {name!r} - one of {', '.join(OBJECTS)}")
    out = folder(name, tint)
    if (out / f"{FRAMES - 1:04d}.png").exists():
        return out
    if not BLENDER.exists():
        raise FileNotFoundError(f"Blender not found at {BLENDER} (set BLENDER=)")
    out.mkdir(parents=True, exist_ok=True)
    procs = []
    for w in range(WORKERS):
        args = {"name": name, "out": str(out), "frames": FRAMES, "size": SIZE,
                "tint": _linear(tint), "only": list(range(w, FRAMES, WORKERS))}
        procs.append(subprocess.Popen(
            [str(BLENDER), "-b", "--factory-startup", "--python", str(SCENE),
             "--", json.dumps(args)], stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL))
    for p in procs:
        p.wait()
    missing = [i for i in range(FRAMES) if not (out / f"{i:04d}.png").exists()]
    if missing:
        raise RuntimeError(f"emblem {name}: {len(missing)} frames did not render")
    return out


class Loop:
    """The frames in memory, premultiplied for compositing."""

    def __init__(self, path: Path):
        from PIL import Image
        self.frames = [Image.open(path / f"{i:04d}.png").convert("RGBA")
                       for i in range(FRAMES)]

    def at(self, t: float):
        return self.frames[int(t * FPS) % FRAMES]


_LOOPS: dict[tuple, Loop] = {}


def loop(name: str, tint) -> Loop:
    key = (name, tuple(tint))
    if key not in _LOOPS:
        _LOOPS[key] = Loop(render(name, tint))
    return _LOOPS[key]


def pick(brand_name: str, video: str) -> str | None:
    s = SETS.get(brand_name)
    if not s:
        return None
    return s[int(hashlib.sha1(video.encode()).hexdigest(), 16) % len(s)]


def use_for(brand_name: str, video: str, emblem: str | None = None) -> str | None:
    """Set this render's default emblem: `emblem` if given, else the brand's
    pick for `video`. Called by `render_long` and `render_crypto_short`."""
    global CURRENT
    CURRENT = emblem or pick(brand_name, video)
    return CURRENT


def draw(out, name: str, tint, t: float, box: tuple, alpha: float = 1.0) -> None:
    """Composite the emblem at timeline second `t`, centred in `box`
    (x, y, w, h), as large as the box's shorter side allows."""
    from PIL import Image
    x, y, w, h = box
    side = int(min(w, h) * 0.95)
    im = loop(name, tint).at(t).resize((side, side), Image.LANCZOS)
    if alpha < 1.0:
        im.putalpha(im.getchannel("A").point(lambda v: int(v * alpha)))
    out.paste(im, (int(x + (w - side) / 2), int(y + (h - side) / 2)), im)


def available() -> bool:
    return BLENDER.exists()

