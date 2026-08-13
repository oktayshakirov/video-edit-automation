"""Video shots — the first moving picture this repo composites itself.

The drone project cuts video, but it does it by writing an FCPXML timeline and
letting Final Cut do the work. Everything the Python renderer has drawn until
now has been a still. A `VideoShot` decodes frames and hands them to the same
per-frame loop `PhotoShot` and the drawn beats use, so a clip crossfades,
carries captions and sits under the watermark exactly like anything else.

Three decisions worth stating:

* **Decode once, into memory, at output size.** A six-second 1080p clip at the
  shot's own length is a few hundred frames; holding them as uint8 is ~100 MB at
  worst and makes every frame lookup free. Seeking per frame through a
  compressed stream is both slower and, on some codecs, not frame-accurate.

* **Trim when long, stretch gently when short, never loop.** A shot's length
  comes from the narration, so a clip almost never matches it. Longer than the
  slot is easy — play the part that fits at natural speed. Shorter needs a
  stretch, capped at 1.33x by `SLOWEST`, because slow motion reads as a mistake
  (the drone skill's rule, for the same reason). Looping is never right: a loop
  point in real footage is instantly visible, since motion either reverses or
  teleports.

* **They are graded to sit with the stills.** Untouched stock is brighter and
  more saturated than this site's own library and the cut to it is jarring —
  the eye reads "different video". A dim and a desaturation, plus the same gold
  hairline the photo shots carry, makes it the same piece.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from ..core.brand import Brand
from ..core.frame import LANDSCAPE, Frame

# The shortest a clip may be relative to its slot before filling it needs
# visible slow motion. 0.75 allows a 1.33x stretch, which on the drifting
# abstractions this pulls is invisible; below that it is a slideshow. There is
# no upper limit, because a clip longer than its slot is trimmed, not sped up.
SLOWEST = 0.75


class VideoShot:
    """A stock clip, decoded and retimed to fill its slot exactly."""

    def __init__(self, path: Path, hold: float, frame: Frame = LANDSCAPE,
                 brand: Brand | None = None, zoom: float = 1.06,
                 dim: float = 0.86, saturation: float = 0.82,
                 label: tuple[str, str] | None = None,
                 fps: int = 30, speed_limit: bool = True):
        self.frame, self.brand, self.zoom = frame, brand, zoom
        self.label = label
        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            raise ValueError(f"cannot open clip {path}")

        src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        src_n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        src_len = src_n / src_fps if src_n else 0.0
        want = max(hold, 1e-3)

        # **A clip longer than its slot is not retimed at all — it is trimmed.**
        # The first version stretched every clip to fill its shot in both
        # directions, which meant a 14s clip in a 5s slot played at 2.8x and was
        # refused as too fast. There was never a reason to speed it up: play five
        # seconds of it at natural speed and the other nine are simply unused.
        # Retiming is only ever needed when the clip is *shorter* than the slot,
        # and then only gently — slow motion reads as a mistake, which is the
        # drone skill's rule too.
        last = src_n - 1
        if src_len > want:
            last = max(0, int(round(want * src_fps)) - 1)
        elif speed_limit and src_len and src_len / want < SLOWEST:
            cap.release()
            raise ValueError(
                f"{path.name} is only {src_len:.1f}s for a {want:.1f}s shot — "
                f"filling it needs {want / src_len:.2f}x slow motion, past the "
                f"{1 / SLOWEST:.2f}x limit. Use a longer clip or split the shot.")

        # Sample the source evenly across the slot. Reading sequentially and
        # keeping the frames we want beats seeking, which is not frame-accurate
        # on every codec and is far slower on all of them.
        n_out = max(1, int(round(want * fps)))
        wanted = np.linspace(0, max(last, 0), n_out).astype(int)
        keep, idx, cursor = [], 0, 0
        while idx < src_n and cursor < len(wanted):
            ok, bgr = cap.read()
            if not ok:
                break
            while cursor < len(wanted) and wanted[cursor] == idx:
                keep.append(self._prepare(bgr, dim, saturation))
                cursor += 1
            idx += 1
        cap.release()
        if not keep:
            raise ValueError(f"decoded no frames from {path}")
        # A short read (a truncated download, a lying frame count) pads with the
        # last frame rather than raising — a held final frame is survivable, a
        # crash three minutes into a ten-minute render is not.
        while len(keep) < n_out:
            keep.append(keep[-1])
        self.frames = keep
        self.hold_s = want

    def _prepare(self, bgr: np.ndarray, dim: float, sat: float) -> np.ndarray:
        """Cover the frame with zoom headroom, then grade toward the stills."""
        fr = self.frame
        w, h = int(fr.w * self.zoom), int(fr.h * self.zoom)
        sh, sw = bgr.shape[:2]
        s = max(w / sw, h / sh)
        bgr = cv2.resize(bgr, (max(1, int(sw * s)), max(1, int(sh * s))),
                         interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LANCZOS4)
        y0 = (bgr.shape[0] - h) // 2
        x0 = (bgr.shape[1] - w) // 2
        bgr = bgr[y0:y0 + h, x0:x0 + w]

        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB).astype(np.float32)
        grey = rgb.mean(axis=2, keepdims=True)
        rgb = (grey + (rgb - grey) * sat) * dim
        return np.clip(rgb, 0, 255).astype(np.uint8)

    def draw(self, f: float) -> Image.Image:
        fr = self.frame
        i = min(len(self.frames) - 1, max(0, int(round(f * (len(self.frames) - 1)))))
        buf = self.frames[i]

        # A slow push in across the shot, using the zoom headroom decoded above.
        # Stock clips already move, so this is deliberately gentler than the
        # stills' Ken Burns — it exists to tie the clip to the rest of the cut,
        # not to add motion the footage already has.
        k = 1.0 - (1.0 - 1.0 / self.zoom) * f
        cw, ch = int(buf.shape[1] * k), int(buf.shape[0] * k)
        x0 = (buf.shape[1] - cw) // 2
        y0 = (buf.shape[0] - ch) // 2
        crop = buf[y0:y0 + ch, x0:x0 + cw]
        out = Image.fromarray(crop).resize(fr.size, Image.LANCZOS)

        if self.brand is not None:
            d = ImageDraw.Draw(out)
            d.rectangle([1, 1, fr.w - 2, fr.h - 2],
                        outline=self.brand.primary, width=3)

        # **A clip carries its line big and centred, not tucked in a corner.**
        # The first build set a 34px kicker and a 58px line in the lower left,
        # which the user called boring and confusing — and it was both, because
        # a small label in a corner reads as a caption for footage that does not
        # need captioning. Set large and centred, the same line stops being a
        # label and becomes a statement the footage is illustrating: it lands
        # like a chapter card, holds the eye in the middle of the frame where
        # the motion is, and carries the viewer into the section rather than
        # annotating it.
        if self.label and self.brand is not None:
            from PIL import ImageFont

            from ..core.draw import wrap
            from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

            kicker, line = self.label
            e = min(1.0, (f * self.hold_s) / 0.42) if self.hold_s else 1.0
            e = 1.0 - (1.0 - e) ** 2

            # A scrim, because stock footage has no idea where the type is going
            # and a bright frame under white type is unreadable. Sized to the
            # band the type occupies rather than the whole frame, so the footage
            # stays visible above and below it.
            band_h = int(fr.h * 0.34)
            band_y = (fr.h - band_h) // 2
            scrim = Image.new("RGBA", (fr.w, band_h), (0, 0, 0, 130))
            out = out.convert("RGBA")
            out.alpha_composite(scrim, (0, band_y))
            d = ImageDraw.Draw(out)

            font = ImageFont.truetype(FONT_CAPTION, 96, index=FONT_CAPTION_INDEX)
            margin = int(140 * fr.w / 1920)
            lines = wrap(d, line, font, fr.w - 2 * margin)
            line_h = int(96 * 1.24)
            y = (fr.h - len(lines) * line_h) // 2 + int(round(24 * (1.0 - e)))

            if kicker:
                kf = ImageFont.truetype(FONT_CAPTION, 34,
                                        index=FONT_CAPTION_INDEX)
                kw = d.textlength(kicker.upper(), font=kf)
                d.text(((fr.w - kw) / 2, y - 76), kicker.upper(), font=kf,
                       fill=self.brand.primary)

            # The rule opens outward from the centre as the line settles, the
            # same move the chapter cards make — so a statement over footage and
            # a statement on a panel read as the same object.
            rw = int(180 * e)
            if rw > 2:
                d.line([(fr.w // 2 - rw, y - 28), (fr.w // 2 + rw, y - 28)],
                       fill=self.brand.primary, width=4)

            for ln in lines:
                tw = d.textlength(ln, font=font)
                d.text(((fr.w - tw) / 2, y), ln, font=font,
                       fill=(255, 255, 255), stroke_width=4,
                       stroke_fill=(0, 0, 0))
                y += line_h
            out = out.convert("RGB")
        return out
