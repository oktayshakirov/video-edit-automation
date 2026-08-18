"""The moving background behind a drawn beat.

**What this replaces.** A flat panel with a drifting grid, drawn in
`longform.beats.Beat.background`. Two things were wrong with it and only one
was fixable:

* **It juddered.** The offset was `int((f * 40) % 96)` — a whole-pixel step, on
  a layer that moves 40 px/s. The rest of this repo has known since the drone
  shorts that motion must be subpixel; the grid was the one moving element that
  never got the memo, and it showed worst on long beats where the eye has time
  to lock onto the lines.
* **It was a grid.** Even drawn smoothly, ruled lines behind type read as
  graph paper, and every beat in every video on both channels shared them. That
  is the templated sameness the strategy doc says gets a channel suppressed.

So the fix is not a smoother grid. It is a different object.

## Backgrounds are square loops, and that is the whole trick

One asset has to serve a 1920x1080 beat and a 1080x1920 one. Storing a
landscape loop and cropping it to portrait throws away two thirds of the frame;
storing both doubles the library and lets them drift apart.

**Square, scaled to fill and centre-cropped**, works for either aspect from one
file. It is only viable because these are soft, low-frequency images: there is
no fine detail for the crop to lose and none for the upscale to blur. A
background with legible content in it would not survive this and does not belong
here anyway — the type is the subject, and a backdrop that pulls the eye is a
bug.

## Sampled by absolute time, not by beat progress

`Beat` hands its painters `f`, its own 0..1 progress. Sampling the loop by `f`
would play the entire loop inside every beat, so a 2.7s stat would run it four
times faster than a 10s compare — the background would visibly change speed at
every cut.

`at(t)` takes **timeline seconds** and wraps them modulo the loop, so motion
runs at one constant rate across the whole video and carries through a cut
rather than restarting. Consecutive beats look like one continuous background
with graphics on top of it, which is what a background is for.

## A loop is a loop because it was made one

Generated backgrounds move every element on a **closed circular path** whose
period divides the loop exactly, so frame N and frame 0 are the same image by
construction — the same rule `longform.asmr` follows for its nebula. Footage
backgrounds cannot do that, so `pingpong()` makes them seamless the other way:
forward, then reversed. Water, smoke and cloth all reverse invisibly, which is
what makes them the footage worth reaching for here.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

BACKGROUNDS = Path(__file__).resolve().parents[2] / "assets/brand/backgrounds"

SIZE = 512          # square, and deliberately small — see the module docstring
LOOP = 12.0         # seconds
FPS = 25


# --------------------------------------------------------------------------
# generating one
# --------------------------------------------------------------------------

def aurora(t: float, size: int, base: tuple, blobs: list) -> np.ndarray:
    """One frame of a drifting mesh gradient, as float RGB in 0..1.

    Each blob is a soft radial falloff whose centre travels a circle. `turns`
    is how many full circuits it makes per loop and **must be an integer** —
    that is the only reason the last frame matches the first.

    Computed at `size` and upscaled by the caller. A gaussian field has no
    high-frequency content, so resolution buys nothing but time: the whole
    point of a mesh gradient is that it is smooth everywhere.
    """
    y, x = np.mgrid[0:size, 0:size].astype(np.float32) / size
    out = np.zeros((size, size, 3), np.float32)
    out[:] = np.array(base, np.float32) / 255.0

    for cx, cy, radius, turns, phase, colour, strength, sigma in blobs:
        a = 2.0 * np.pi * (turns * t / LOOP + phase)
        # The path is a circle, so the blob returns to where it started. An
        # ellipse or a Lissajous with integer terms would do as well; a linear
        # drift would not, which is the constraint the whole format inherits
        # from the ASMR loop.
        px = cx + radius * np.cos(a)
        py = cy + radius * np.sin(a)
        d2 = (x - px) ** 2 + (y - py) ** 2
        # **Per-blob sigma, not one constant.** At a shared 0.34 every blob was
        # wider than the frame, so they summed into a single lavender wash with
        # no shape in it — and far too bright to sit under white type. Mixed
        # radii give the field an actual composition.
        fall = np.exp(-d2 / (2.0 * sigma ** 2))
        out += (np.array(colour, np.float32) / 255.0
                * strength * fall[..., None])

    # A vignette, so the corners stay dark and the type in the middle of the
    # frame always has the quietest ground under it.
    r2 = (x - 0.5) ** 2 + (y - 0.5) ** 2
    out *= (1.0 - 0.55 * np.clip(r2 * 2.4, 0, 1))[..., None]
    return np.clip(out, 0, 1)


# The tinnitus background. Purples out of the app's own palette — `panel`
# #5B3964 and the void it sits in — with one peach blob at low strength so the
# brand's highlight appears somewhere in the field rather than only on the type.
# Five blobs on coprime turn counts (1, 2, 3), so the composition genuinely
# changes across the loop rather than sliding back and forth.
TINNITUS_AURORA = dict(
    base=(10, 6, 15),
    blobs=[
        # cx    cy   radius turns phase  colour           strength sigma
        (0.32, 0.36, 0.20,  1,   0.00, (96, 60, 106),    0.26,  0.26),
        (0.70, 0.60, 0.24,  1,   0.50, (72, 42, 94),     0.24,  0.30),
        (0.52, 0.24, 0.17,  2,   0.25, (128, 78, 136),   0.14,  0.19),
        (0.24, 0.72, 0.21,  2,   0.70, (54, 32, 74),     0.19,  0.23),
        (0.78, 0.30, 0.15,  3,   0.10, (255, 218, 185),  0.035, 0.15),
        (0.44, 0.78, 0.13,  3,   0.62, (140, 88, 150),   0.065, 0.14),
    ],
)


def generate(out: Path, spec: dict, size: int = SIZE,
             seconds: float = LOOP, fps: int = FPS) -> Path:
    """Render a generated background to a looping mp4."""
    out.parent.mkdir(parents=True, exist_ok=True)
    n = int(round(seconds * fps))
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{size}x{size}", "-r", str(fps), "-i", "-",
         # CRF 14: this is a source asset that gets upscaled 3-4x at draw
         # time, so banding in a smooth gradient is the one artifact that
         # would actually show.
         "-c:v", "libx264", "-crf", "14", "-preset", "slow",
         "-pix_fmt", "yuv420p", str(out)],
        stdin=subprocess.PIPE)
    for i in range(n):
        frame = aurora(i / fps, size, spec["base"], spec["blobs"])
        proc.stdin.write((frame * 255).astype(np.uint8).tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError(f"ffmpeg failed writing {out}")
    return out


def pingpong(src: Path, out: Path, start: float, seconds: float,
             size: int = SIZE, dim: float = 1.0,
             saturation: float = 1.0) -> Path:
    """A square, seamless loop cut from real footage.

    Forward then reversed, so the join is exact without any blending. This is
    only invisible on subjects with no arrow of time — water, smoke, cloth,
    drifting particles. Do not point it at anything with a direction.

    `dim` and `saturation` exist because footage arrives graded for being the
    subject, and here it is the ground underneath type.
    """
    out.parent.mkdir(parents=True, exist_ok=True)
    # **`dim` multiplies, it does not offset.** ffmpeg's `eq=brightness` adds a
    # constant, so dimming already-dark footage by "0.72" subtracted 71 levels
    # and returned pure black — measured at mean luma 0.0. `colorchannelmixer`
    # scales each channel, which is what dimming means.
    vf = (f"crop='min(iw,ih)':'min(iw,ih)',scale={size}:{size},"
          f"eq=saturation={saturation:.3f},"
          f"colorchannelmixer=rr={dim:.3f}:gg={dim:.3f}:bb={dim:.3f}")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(seconds),
         "-i", str(src), "-an", "-filter_complex",
         f"[0:v]{vf},split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1:a=0",
         # Forced to the module's own fps: the source is 60p and a background
         # nobody looks at directly does not need 720 frames held in memory.
         "-r", str(FPS),
         "-c:v", "libx264", "-crf", "14", "-preset", "slow",
         "-pix_fmt", "yuv420p", str(out)], check=True)
    return out


# --------------------------------------------------------------------------
# using one
# --------------------------------------------------------------------------

@dataclass
class Backdrop:
    """A looping background, sampled by timeline seconds.

    Frames are decoded once into memory. At 512x512 a twelve second loop is
    ~236 MB as float, so they are kept as uint8 (~79 MB) and the scale-and-crop
    happens per draw — which is one `cv2.resize` on a small image and costs
    less than the gradient it replaced cost to draw.
    """

    name: str
    frames: list
    fps: float

    @classmethod
    def load(cls, name: str) -> "Backdrop | None":
        path = BACKGROUNDS / f"{name}.mp4"
        if not path.exists():
            return None
        cap = cv2.VideoCapture(str(path))
        fps = cap.get(cv2.CAP_PROP_FPS) or FPS
        frames = []
        while True:
            ok, fr = cap.read()
            if not ok:
                break
            frames.append(cv2.cvtColor(fr, cv2.COLOR_BGR2RGB))
        cap.release()
        if not frames:
            return None
        return cls(name=name, frames=frames, fps=fps)

    def at(self, t: float, w: int, h: int) -> np.ndarray:
        """The frame for timeline second `t`, filled and cropped to `w`x`h`."""
        i = int(t * self.fps) % len(self.frames)
        src = self.frames[i]
        s = max(w / src.shape[1], h / src.shape[0])
        big = cv2.resize(src, (int(np.ceil(src.shape[1] * s)),
                               int(np.ceil(src.shape[0] * s))),
                         interpolation=cv2.INTER_CUBIC)
        y0 = (big.shape[0] - h) // 2
        x0 = (big.shape[1] - w) // 2
        return big[y0:y0 + h, x0:x0 + w]


_CACHE: dict[str, Backdrop | None] = {}


def get(name: str | None) -> Backdrop | None:
    """Load a background by name, once per process."""
    if not name:
        return None
    if name not in _CACHE:
        _CACHE[name] = Backdrop.load(name)
    return _CACHE[name]
