"""An old-film surface over chosen parts of a video: grain, dust, a light leak.

The user's note (2026-10-21), from a documentary channel: a very slight grainy
overlay with particles, "reminding of old movie" - and **placed strategically,
not over the whole video**. So this is four independent layers, each with its
own strength, and a policy that decides per shot which ones apply:

* **grain** - fine, moving, monochrome noise, weighted toward the mid-tones
  the way film grain reads (black stays black, highlights stay clean). Drawn
  at half resolution and scaled up, so it clumps like grain rather than
  fizzing like digital sensor noise.
* **dust** - white specks and short streaks that live one frame, and the odd
  hair. This is the "particles" in the reference. (A wandering vertical
  scratch was in the first version; the user disliked it and it is gone.)
* **leak** - a soft warm glow breathing up from the bottom edge, the bloom in
  the reference frame. Slow, so it reads as light, not as an effect.
* **flicker** - the exposure wavering by a percent or two.

**Generated, not sourced**, for the same reasons as `sfx`: ours to license on
every platform, no 4K overlay files in a public repo, and parameterised so the
strength can be judged and tuned rather than swapped. Every random draw is
seeded from the frame number, so a re-render is byte-identical.

**Where it goes is the point** (`plan`, `RECIPES`): not a blanket over the
video but an arrangement - clean shots, single-layer shots and full shots in
rotation across the footage, dust and the leak on the dark title, chapter and
end frames, and nothing on drawn data beats.
"""

from __future__ import annotations

import math

import cv2
import numpy as np
from PIL import Image

# Layer strengths per recipe. 0 / missing = off. Tuned against the reference
# frame: present when looked for, invisible when not.
RECIPES = {
    "clean": {},
    "grain": {"grain": 1.0},
    "dust": {"dust": 0.8},
    "full": {"grain": 1.0, "flicker": 1.0, "dust": 0.45},
    "chapter": {"grain": 0.7, "dust": 1.0, "leak": 1.0, "flicker": 0.6},
    "title": {"grain": 0.8, "dust": 1.0, "leak": 0.8},
    "end": {"grain": 0.8, "dust": 1.0, "leak": 1.0},
    "beat": {},
}
POLICY = RECIPES                # the old name, kept for callers

# The footage rotation after a section's first shot. Grain-only, clean,
# dust-only, full: no two neighbours alike, a clean shot every fourth, and
# both single-layer recipes in every cycle.
ROTATION = ("grain", "clean", "dust", "full")


def plan(shots) -> list[str]:
    """A recipe per shot - the arrangement, not a blanket.

    The user's note (2026-10-21): a couple of clips per video with no
    overlay, some with just one layer, not all of them with everything. The
    rules, in order:

    * **Drawn beats get nothing** - grain over a chart's numbers costs
      legibility for no mood.
    * **Chapter cards get their own recipe** - dust and the leak, on the dark
      frames where specks read best.
    * **The very first shot is clean.** The hook's first frame has to be
      crisp; texture can arrive once the viewer is in.
    * **A disclaimer clip is clean** - a legal note should look like one -
      and **a clip carrying a statement gets grain only**, so no speck lands
      in the type.
    * **A section's first footage shot gets the full look**, re-establishing
      the mood after the card.
    * **Every other footage shot takes the next step of `ROTATION`**, counted
      across the whole video so the clean shots spread out.
    """
    from ..longform.meta import is_notice

    out, k, fresh, first, prev = [], 0, False, True, None
    for sh in shots:
        kd = kind(sh)
        if kd == "beat":
            out.append("beat")
            continue
        if kd == "chapter":
            out.append("chapter")
            fresh = True
            continue
        payload = getattr(sh, "payload", ()) or ()
        line = payload[1] if len(payload) > 1 else ""
        if first:
            r = "clean"
        elif line and is_notice(payload):
            r = "clean"
        elif line:
            r = "grain"
        elif fresh:
            r = "full"
        else:
            r = ROTATION[k % len(ROTATION)]
            k += 1
            # Never the same recipe twice in a row: an override above may
            # just have produced what the rotation would say next.
            if r == prev:
                r = ROTATION[k % len(ROTATION)]
                k += 1
        out.append(r)
        prev = r
        first = fresh = False
    return out

GRAIN = 9.0          # grain std-dev in 8-bit levels at strength 1, mid-grey
FLICKER = 0.018      # exposure wobble at strength 1
DUST_RATE = 2.2      # specks per frame at strength 1


def _rng(frame: int, salt: int) -> np.random.Generator:
    return np.random.default_rng((frame * 7919 + salt) & 0xFFFFFFFF)


def grain(arr: np.ndarray, frame: int, k: float) -> np.ndarray:
    H, W = arr.shape[:2]
    rng = _rng(frame, 1)
    small = rng.normal(0.0, 1.0, (H // 2 + 1, W // 2 + 1)).astype(np.float32)
    noise = cv2.resize(small, (W, H), interpolation=cv2.INTER_LINEAR)[:H, :W]
    luma = arr.mean(axis=2, keepdims=True) / 255.0
    # Mid-tones carry it; deep black and clipped white barely do.
    weight = 0.25 + 3.0 * luma * (1.0 - luma)
    return arr + noise[:, :, None] * (GRAIN * k) * weight


def flicker(arr: np.ndarray, frame: int, k: float) -> np.ndarray:
    # Two incommensurate slow sines plus a per-frame jitter: an unsteady lamp,
    # not a strobe.
    w = (0.55 * math.sin(frame * 0.37) + 0.30 * math.sin(frame * 1.13 + 1.7)
         + 0.15 * _rng(frame, 2).uniform(-1, 1))
    return arr * (1.0 + FLICKER * k * w)


def dust(arr: np.ndarray, frame: int, k: float) -> np.ndarray:
    H, W = arr.shape[:2]
    rng = _rng(frame, 3)
    layer = np.zeros((H, W), np.float32)
    s = W / 1920.0

    # Specks: most are dots, some short streaks. Each lives one frame; the
    # eye fuses them into "dust" exactly as it does on a projected print.
    for _ in range(rng.poisson(DUST_RATE * k)):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        v = float(rng.uniform(140, 255))
        if rng.random() < 0.7:
            r = max(1, int(round(rng.uniform(0.6, 2.2) * s)))
            cv2.circle(layer, (int(x), int(y)), r, v, -1, cv2.LINE_AA)
        else:
            a = rng.uniform(0, math.pi)
            L = rng.uniform(4, 14) * s
            cv2.line(layer, (int(x), int(y)),
                     (int(x + L * math.cos(a)), int(y + L * math.sin(a))),
                     v, max(1, int(s)), cv2.LINE_AA)

    # A hair now and then: a thin curve, dimmer, a few frames at most.
    if rng.random() < 0.035 * k:
        x0, y0 = rng.uniform(0.1, 0.9) * W, rng.uniform(0.1, 0.9) * H
        pts = [(x0, y0)]
        a = rng.uniform(0, 2 * math.pi)
        for _ in range(14):
            a += rng.normal(0, 0.35)
            x0 += 6 * s * math.cos(a)
            y0 += 6 * s * math.sin(a)
            pts.append((x0, y0))
        cv2.polylines(layer, [np.int32(pts)], False, 120.0, max(1, int(s)),
                      cv2.LINE_AA)

    if layer.max() <= 0:
        return arr
    layer = cv2.GaussianBlur(layer, (0, 0), 0.6 * s + 0.3)
    return arr + layer[:, :, None] * 0.85


def leak(arr: np.ndarray, frame: int, k: float, t: float) -> np.ndarray:
    H, W = arr.shape[:2]
    # One soft blob below the bottom edge, drifting sideways and breathing.
    cx = W * (0.5 + 0.10 * math.sin(t * 0.21))
    cy = H * (1.04 + 0.02 * math.sin(t * 0.33))
    r = H * 0.62
    breathe = 0.75 + 0.25 * math.sin(t * 0.8)
    # Built at a quarter resolution: it is all low frequency.
    q = 4
    yy, xx = np.mgrid[0:H // q, 0:W // q].astype(np.float32)
    d2 = ((xx * q - cx) ** 2 + (yy * q - cy) ** 2) / (r * r)
    g = np.exp(-2.2 * d2) * (34.0 * k * breathe)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
    warm = np.array([1.0, 0.92, 0.80], np.float32)          # a warm white
    return arr + g[:, :, None] * warm


def apply(pic: Image.Image, t: float, layers: dict, fps: int = 30) -> Image.Image:
    """`layers` is a policy entry: {"grain": 1.0, "dust": 0.5, ...}."""
    if not layers:
        return pic
    frame = int(round(t * fps))
    arr = np.asarray(pic).astype(np.float32)
    if layers.get("leak"):
        arr = leak(arr, frame, layers["leak"], t)
    if layers.get("flicker"):
        arr = flicker(arr, frame, layers["flicker"])
    if layers.get("grain"):
        arr = grain(arr, frame, layers["grain"])
    if layers.get("dust"):
        arr = dust(arr, frame, layers["dust"])
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def kind(shot) -> str:
    """Which policy row a shot takes."""
    if shot is None:
        return "beat"
    if getattr(shot, "clip", None) is not None:
        return "footage"
    if shot.graphic == "chapter":
        return "chapter"
    if shot.graphic is None:
        return "photo"
    return "beat"


class FilmOverlay:
    """The film surface as a timeline overlay, choosing its layers per moment.

    Built from the laid-out shot list, arranged by `plan`, plus the windows
    of the opening title and the end card, which take their own recipes
    because they sit over footage the plan would otherwise decide.
    `strength` scales every layer, for an A/B or a channel that wants less.
    """

    def __init__(self, shots, total: float, windows=(), strength: float = 1.0,
                 policy: dict | None = None, fps: int = 30):
        self.total, self.fps = total, fps
        self.policy = policy or RECIPES
        self.strength = strength
        live = [s for s in shots if s is not None]
        self.spans = [(s.start, s.start + s.hold, r)
                      for s, r in zip(live, plan(live))]
        self.windows = list(windows)            # (start, end, kind)

    def layers_at(self, t: float) -> dict:
        row = "beat"
        for a, b, k in self.spans:
            if a <= t < b:
                row = k
        for a, b, k in self.windows:            # windows win over shots
            if a <= t < b:
                row = k
        return {n: v * self.strength
                for n, v in self.policy.get(row, {}).items() if v}

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        return apply(pic, t, self.layers_at(t), self.fps)
