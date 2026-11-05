"""What a still can do besides a flat Ken Burns: move in depth, dim its room,
let its subject break the frame.

`crypto.shots.PhotoShot` is the one place every still in both formats is
drawn, and these are its three options (`Shot(parallax=, isolate=, pop=)`).
They live here so that file only gains the branches that switch them on: with
all three off, `PhotoShot.draw` runs the exact path it always did, which is
what keeps every approved cut byte for byte the same.

**Depth, not a second affine.** The Ken Burns scales and slides the whole
photograph as one sheet. `DepthMove` gives every pixel its own move from
`vision.depth`: the far plane stays nearly put, near things grow faster and
slide further, so the shot reads as a camera moving through the place rather
than a print being zoomed. Measured in the prototype on the NYC skyline
(2026-11-05): ~70ms a frame at 1080p on top of the plain warp.
"""

from __future__ import annotations

import cv2
import numpy as np

# The depth move, at `parallax=1.0`. Near planes zoom this share of the
# shot's own Ken Burns travel on top of it, and slide this share of the
# photo's width across the shot.
PUSH_SHARE = 0.6
SLIDE = 0.022
# The plane that stays put: this percentile of the picture's depth. Below the
# median, so the background holds and the subject is what moves.
ANCHOR_PCT = 40


def prepare_depth(d: np.ndarray) -> np.ndarray:
    """Smooth a depth map for warping, and grow near regions outward.

    A raw map has a hard step at every silhouette; warped as it is, the step
    tears the edge. Softening it a little and dilating the near side means a
    foreground edge moves as one piece and the stretch lands on the
    background just behind it, where it reads as parallax, not as damage.
    """
    w = d.shape[1]
    d = cv2.GaussianBlur(d, (0, 0), max(1.0, w * 0.0016))
    k = max(3, int(w * 0.005)) | 1
    return np.maximum(d, cv2.dilate(d, np.ones((k, k), np.uint8)) * 0.92)


class DepthMove:
    """Per-pixel source coordinates for a still that moves in depth.

    `sample(xs, ys, f)` takes frame-pixel coordinates already mapped into the
    photograph's own pixels by the shot's affine (the flat Ken Burns) and
    returns where each should really sample from. Two refinement passes look
    the depth up at the *source* point rather than the output point, which is
    what keeps a moving edge from smearing.
    """

    def __init__(self, depth: np.ndarray, amount: float, zoom: float,
                 pan: tuple[float, float]):
        self.d = prepare_depth(depth.astype(np.float32))
        self.d0 = float(np.percentile(self.d, ANCHOR_PCT))
        self.h, self.w = self.d.shape
        self.amount = float(amount)
        self.push = PUSH_SHARE * (zoom - 1.0) * self.amount
        # Slide the way the Ken Burns pans, or rightward if it does not.
        sx = np.sign(pan[0]) if pan[0] else 1.0
        self.slide = SLIDE * self.w * self.amount * sx
        self.slide_y = SLIDE * self.h * self.amount * np.sign(pan[1]) * 0.5 \
            if pan[1] else 0.0

    def sample(self, u0: np.ndarray, v0: np.ndarray, f: float):
        cu, cv = self.w / 2.0, self.h / 2.0
        tx = self.slide * (f - 0.5)
        ty = self.slide_y * (f - 0.5)
        u, v = u0, v0
        for _ in range(2):
            dd = cv2.remap(self.d, u, v, cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_REFLECT) - self.d0
            zz = 1.0 + self.push * f * dd
            u = cu + (u0 - cu) / zz - tx * dd
            v = cv + (v0 - cv) / zz - ty * dd
        return u.astype(np.float32), v.astype(np.float32)


def isolate_room(rgb: np.ndarray) -> np.ndarray:
    """The room behind an isolated subject: softened and stepped down.

    Precomputed once per shot; `isolate_blend` mixes toward it per frame.
    """
    w = rgb.shape[1]
    soft = cv2.GaussianBlur(rgb, (0, 0), max(1.0, w * 0.006))
    return (soft.astype(np.float32) * 0.48).astype(np.uint8)


def isolate_blend(rgb: np.ndarray, room: np.ndarray, alpha: np.ndarray,
                  w: float) -> np.ndarray:
    """`rgb` with everything but the subject `w` of the way to `room`.

    `cv2.blendLinear` does the per-pixel mix in one SIMD pass; the numpy form
    of the same arithmetic cost ~70ms a frame on a 2000px picture.
    """
    if w <= 0.001:
        return rgb
    k = np.ascontiguousarray(w * (1.0 - alpha), np.float32)
    return cv2.blendLinear(rgb, room, 1.0 - k, k)


def isolate_weight(f: float, amount: float) -> float:
    """Ramps in over the first 40% of the shot, then holds."""
    p = min(1.0, max(0.0, f / 0.4))
    return amount * p * p * (3 - 2 * p)


def pop_cut(alpha: np.ndarray, share: float = 0.38) -> int | None:
    """Where to drop a framed photo's top edge so the subject's head pops out.

    The edge moves down to `share` of the way through the subject's height,
    clamped to 12-45% of the picture: the head and shoulders break the frame,
    the body stays inside it. None when there is no subject to pop (an empty
    matte, or one that already starts well inside the picture's lower half).
    """
    h = alpha.shape[0]
    rows = np.nonzero((alpha > 0.5).sum(axis=1) > max(3, alpha.shape[1] * 0.01))[0]
    if len(rows) == 0:
        return None
    top, bottom = int(rows[0]), int(rows[-1])
    if top > h * 0.5:
        return None
    cut = int(top + share * (bottom - top))
    return int(min(max(cut, h * 0.12), h * 0.45))
