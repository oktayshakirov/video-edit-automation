"""A picture put onto a clip's blank, lit screen - a screen replacement.

**Built for `random-tokens-in-wallet` (2026-11-06).** Stock that shows
someone at a laptop or a phone mostly shows either an unrelated app (a feed,
a calendar, a chat) or an empty white screen, and the editor's note on the
white one was "the laptop at 1:02 have empty white screen, either replace
the clip or add something on top of the clip". A blank screen is the best
case: it is the one thing in the frame we can find exactly, so the page the
narration talks about (a claim site, a wallet prompt, a captured page) can
be put *on* it, in the clip's own perspective and light.

    from video_automation.core import screenfill
    LAPTOP_SITE = screenfill.path(LAPTOP, SITE)       # in the shot list
    screenfill.make(LAPTOP, SITE)                     # in main()

Per frame: threshold the bright pixels inside `search` (a box, as fractions
of the frame, that keeps the keyboard and a lit palm rest out), take the
largest blob, fit it to four corners, smooth those corners over time so the
picture does not shiver, warp the picture into them and lay it in with a
2px feathered edge, multiplied by the screen's own falloff so the panel's
vignette and glare stay. **The screen must not be crossed** by a hand or an
object - nothing here keys around an occluder; pick a clip where it is not.

`picture` should have the screen's real shape (16:10 for a laptop, about
9:19.5 for a phone), not the foreshortened shape seen in the clip - the
warp does the foreshortening. Cached as
`assets/stock/screens/<clip>-<hash>.mp4` (gitignored, like the stock).
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import numpy as np

from .stock import CACHE

OUT = CACHE / "screens"
GROW = 5.0     # px each corner moves outward - see `make`


def path(clip: Path, picture: Path, search=(0.0, 0.0, 1.0, 0.6),
         threshold: int = 140) -> Path:
    """Where `make` puts the clip - without making it, so a gate that
    imports a script renders nothing."""
    clip, picture = Path(clip), Path(picture)
    key = hashlib.sha1(
        f"{clip.resolve()}|{picture.resolve()}|{picture.stat().st_size}|"
        f"{search}|{threshold}|{GROW}".encode()).hexdigest()[:10]
    return OUT / f"{clip.stem}-{picture.stem}-{key}.mp4"


def corners(gray: np.ndarray, search, threshold: int) -> np.ndarray | None:
    """The four corners (tl, tr, br, bl) of the largest bright blob inside
    `search`, or None when there is none worth calling a screen."""
    import cv2
    h, w = gray.shape
    x0, y0, x1, y1 = (int(search[0] * w), int(search[1] * h),
                      int(search[2] * w), int(search[3] * h))
    m = np.zeros_like(gray, np.uint8)
    m[y0:y1, x0:x1] = (gray[y0:y1, x0:x1] > threshold).astype(np.uint8) * 255
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cs:
        return None
    c = max(cs, key=cv2.contourArea)
    if cv2.contourArea(c) < 0.02 * w * h:
        return None
    hull = cv2.convexHull(c)
    q = None
    for eps in np.linspace(0.01, 0.08, 15):
        a = cv2.approxPolyDP(hull, eps * cv2.arcLength(hull, True), True)
        if len(a) == 4:
            q = a.reshape(4, 2).astype(np.float32)
            break
    if q is None:
        rect = cv2.minAreaRect(c)
        q = cv2.boxPoints(rect).astype(np.float32)
    # Order tl, tr, br, bl.
    s, d = q.sum(1), q[:, 0] - q[:, 1]
    return np.array([q[s.argmin()], q[d.argmax()], q[s.argmax()],
                     q[d.argmin()]], np.float32)


def make(clip: Path, picture: Path, search=(0.0, 0.0, 1.0, 0.6),
         threshold: int = 140, smooth: int = 9) -> Path:
    """Render the clip with `picture` on its screen, the first time asked."""
    import cv2
    from PIL import Image
    clip, picture = Path(clip), Path(picture)
    out = path(clip, picture, search, threshold)
    if out.exists():
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(clip))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    frames, quads = [], []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        frames.append(fr)
        quads.append(corners(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY),
                             search, threshold))
    cap.release()
    if not frames:
        raise ValueError(f"screenfill: no frames in {clip}")
    good = [q for q in quads if q is not None]
    if len(good) < 0.8 * len(quads):
        raise ValueError(f"screenfill: found a screen in only {len(good)} of "
                         f"{len(quads)} frames of {clip.name} - check `search`")
    # Fill gaps with the last good quad, then a centred moving average.
    last = good[0]
    for i, q in enumerate(quads):
        if q is None:
            quads[i] = last
        else:
            last = q
    arr = np.stack(quads)
    k = max(1, smooth)
    pad = np.concatenate([arr[:1].repeat(k // 2, 0), arr,
                          arr[-1:].repeat(k // 2, 0)])
    arr = np.stack([pad[i:i + k].mean(0) for i in range(len(quads))])
    # The threshold stops a few pixels inside the panel's dimmer edge, which
    # left a white rim round the picture: push each corner out by `grow` px.
    ctr = arr.mean(1, keepdims=True)
    vec = arr - ctr
    arr = arr + GROW * vec / np.linalg.norm(vec, axis=2, keepdims=True)

    pic = np.asarray(Image.open(picture).convert("RGB"))[:, :, ::-1]
    ph, pw = pic.shape[:2]
    src = np.array([[0, 0], [pw, 0], [pw, ph], [0, ph]], np.float32)
    h, w = frames[0].shape[:2]
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24",
         "-s", f"{w}x{h}", "-r", f"{fps}", "-i", "-", "-c:v", "libx264",
         "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", str(out)],
        stdin=subprocess.PIPE)
    for fr, q in zip(frames, arr):
        m = cv2.getPerspectiveTransform(src, q)
        warped = cv2.warpPerspective(pic, m, (w, h), flags=cv2.INTER_LINEAR)
        mask = cv2.warpPerspective(np.full((ph, pw), 255, np.uint8), m, (w, h))
        # Shrink 1px so no white rim shows, then feather 2px.
        mask = cv2.erode(mask, np.ones((3, 3), np.uint8))
        mask = cv2.GaussianBlur(mask, (5, 5), 0).astype(np.float32) / 255
        # The panel's own light: its luminance over its brightest level,
        # blurred, so the vignette and glare carry onto the picture.
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).astype(np.float32)
        inside = mask > 0.5
        ref = np.percentile(g[inside], 95) if inside.any() else 255
        light = np.clip(cv2.GaussianBlur(g, (0, 0), 25) / max(ref, 1), 0.6, 1.0)
        lit = warped.astype(np.float32) * light[:, :, None]
        a = mask[:, :, None]
        comp = fr.astype(np.float32) * (1 - a) + lit * a
        proc.stdin.write(np.clip(comp, 0, 255).astype(np.uint8).tobytes())
    proc.stdin.close()
    if proc.wait() != 0:
        out.unlink(missing_ok=True)
        raise RuntimeError(f"screenfill: ffmpeg failed for {clip.name}")
    return out
