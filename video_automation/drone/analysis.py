"""Per-frame CV on the cached proxy, reduced to clip-level stats.

Motion comes from sparse Lucas-Kanade tracking with a RANSAC partial-affine
fit — not dense Farneback. LK is faster and far more robust on the smooth sky
and water that dominate drone frames.

The affine matrix is read directly:
    translation term -> pans and lateral moves
    rotation term    -> image roll
    scale term       -> push-ins and pullbacks
"""

from __future__ import annotations

import math
from pathlib import Path

import cv2
import numpy as np

from .config import (
    FEATURE_QUALITY,
    HOVER_PAN_MAX,
    HOVER_ROT_MAX,
    HOVER_ZOOM_MAX,
    MAX_FEATURES,
    MIN_FEATURE_DIST,
    MIN_TRACKED_FOR_FIT,
    PROXY_FPS,
    PROXY_WIDTH,
    REDETECT_BELOW,
    W_PAN,
    W_ROT,
    W_ZOOM,
)


def analyze_proxy(proxy: Path) -> dict | None:
    cap = cv2.VideoCapture(str(proxy))
    if not cap.isOpened():
        return None

    sharpness, hi_clip, lo_clip = [], [], []
    hues, sats, vals = [], [], []
    trans, rots, scales = [], [], []
    low_conf_frames = 0

    prev_gray = None
    p0 = None
    frame_count = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break
        frame_count += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- quality ---
        sharpness.append(float(cv2.Laplacian(gray, cv2.CV_64F).var()))
        total = gray.size
        hi_clip.append(float(np.count_nonzero(gray >= 250)) / total)
        lo_clip.append(float(np.count_nonzero(gray <= 5)) / total)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # circular mean of hue, weighted by saturation, so grey pixels don't vote
        h = hsv[:, :, 0].astype(np.float32) * (2 * math.pi / 180.0)
        s = hsv[:, :, 1].astype(np.float32) / 255.0
        if s.sum() > 0:
            hues.append((float((np.cos(h) * s).sum() / s.sum()),
                         float((np.sin(h) * s).sum() / s.sum())))
        sats.append(float(s.mean()))
        vals.append(float(hsv[:, :, 2].mean()) / 255.0)

        # --- motion ---
        if prev_gray is not None:
            if p0 is None or len(p0) < REDETECT_BELOW:
                p0 = cv2.goodFeaturesToTrack(
                    prev_gray, maxCorners=MAX_FEATURES,
                    qualityLevel=FEATURE_QUALITY, minDistance=MIN_FEATURE_DIST,
                )

            if p0 is not None and len(p0) >= MIN_TRACKED_FOR_FIT:
                p1, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, p0, None)
                if p1 is not None:
                    good_new = p1[status.ravel() == 1]
                    good_old = p0[status.ravel() == 1]

                    if len(good_new) >= MIN_TRACKED_FOR_FIT:
                        M, _ = cv2.estimateAffinePartial2D(
                            good_old, good_new, method=cv2.RANSAC, ransacReprojThreshold=2.0
                        )
                        if M is not None:
                            a, b = M[0, 0], M[1, 0]
                            scale = math.hypot(a, b)
                            rot = math.degrees(math.atan2(b, a))
                            tx = M[0, 2] / PROXY_WIDTH   # as fraction of frame width
                            ty = M[1, 2] / PROXY_WIDTH
                            trans.append((tx, ty))
                            rots.append(rot)
                            scales.append(scale)
                        else:
                            low_conf_frames += 1
                    else:
                        low_conf_frames += 1
                    p0 = good_new.reshape(-1, 1, 2)
                else:
                    low_conf_frames += 1
                    p0 = None
            else:
                low_conf_frames += 1
                p0 = None

        prev_gray = gray

    cap.release()

    if frame_count < 3:
        return None

    def med(xs, default=0.0):
        return float(np.median(xs)) if len(xs) else default

    # Per-second rates. Translation is in frame-widths, rotation in degrees,
    # scale as fractional zoom (positive = pushing in).
    tx_rate = med([t[0] for t in trans]) * PROXY_FPS
    ty_rate = med([t[1] for t in trans]) * PROXY_FPS
    rot_rate = med(rots) * PROXY_FPS
    zoom_rate = (med(scales, 1.0) - 1.0) * PROXY_FPS

    pan_mag = math.hypot(tx_rate, ty_rate)

    # Single scalar for matching against musical energy. Weights are the first
    # thing to tune once you compare output against your own past edits.
    motion_energy = pan_mag * W_PAN + abs(rot_rate) * W_ROT + abs(zoom_rate) * W_ZOOM

    hue_deg = 0.0
    if hues:
        hx = float(np.mean([h[0] for h in hues]))
        hy = float(np.mean([h[1] for h in hues]))
        hue_deg = (math.degrees(math.atan2(hy, hx)) + 360.0) % 360.0

    return {
        "sharpness": med(sharpness),
        "sharpness_low": float(np.percentile(sharpness, 10)) if sharpness else 0.0,
        "highlight_clip": med(hi_clip),
        "shadow_clip": med(lo_clip),
        "hue": hue_deg,
        "saturation": med(sats),
        "brightness": med(vals),
        "pan_rate": pan_mag,
        "tx_rate": tx_rate,
        "ty_rate": ty_rate,
        "rot_rate": rot_rate,
        "zoom_rate": zoom_rate,
        "motion_energy": motion_energy,
        "confidence": 1.0 - (low_conf_frames / max(frame_count - 1, 1)),
        "move_type": classify_move(pan_mag, tx_rate, ty_rate, rot_rate, zoom_rate),
    }


def classify_move(pan, tx, ty, rot, zoom) -> str:
    """Label the dominant camera move. Thresholds are per-second and deliberately
    loose — retune them against clips whose move you already know."""
    if pan < HOVER_PAN_MAX and abs(rot) < HOVER_ROT_MAX and abs(zoom) < HOVER_ZOOM_MAX:
        return "hover"

    candidates = {
        "push_in" if zoom > 0 else "pull_back": abs(zoom) * W_ZOOM,
        "orbit": abs(rot) * W_ROT,
        "vertical" if abs(ty) > abs(tx) else "lateral": pan * W_PAN,
    }
    return max(candidates.items(), key=lambda kv: kv[1])[0]
