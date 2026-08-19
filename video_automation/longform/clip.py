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

import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from ..core.brand import Brand
from ..core.frame import LANDSCAPE, Frame

# The thumbnail and chapter-card display face, so a figure drawn over footage
# is set in the same voice as the headline type everywhere else.
FONT_DISPLAY = "/System/Library/Fonts/Supplemental/Arial Black.ttf"

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
                 note: tuple[str, str] | None = None,
                 begin: float = 0.0,
                 fps: int = 30, speed_limit: bool = True):
        self.frame, self.brand, self.zoom = frame, brand, zoom
        self.label = label
        self.note = note
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
        # `begin` skips into the clip. Stock rarely opens on its own best
        # moment — this one spends its first second on an ambiguous
        # half-smile before the discomfort reads.
        first = max(0, int(round(begin * src_fps)))
        last = src_n - 1
        if src_len - begin > want:
            last = max(first, first + int(round(want * src_fps)) - 1)
        elif speed_limit and src_len and (src_len - begin) / want < SLOWEST:
            cap.release()
            raise ValueError(
                f"{path.name} is only {src_len:.1f}s for a {want:.1f}s shot — "
                f"filling it needs {want / src_len:.2f}x slow motion, past the "
                f"{1 / SLOWEST:.2f}x limit. Use a longer clip or split the shot.")

        # Sample the source across the slot. Reading sequentially and keeping
        # the frames we want beats seeking, which is not frame-accurate on every
        # codec and is far slower on all of them.
        #
        # **Sampled at fractional positions and blended, not rounded.** Stock is
        # almost always 25fps against this 30fps timeline, so a rounded sample
        # repeats every sixth frame — and a repeat is a *dead* frame: the motion
        # stops for one frame in six and the eye reads it as a stutter. Blending
        # the two neighbouring source frames instead keeps the motion continuous
        # through the mismatch. Measured on the opener, the repeated frames went
        # from 0.00 to 0.20 to 1.1 mean delta against ~1.3 for a real frame.
        #
        # The blend weight never exceeds 0.5 at 25->30, so the ghosting a full
        # frame-interpolation would risk does not arise here.
        n_out = max(1, int(round(want * fps)))
        pos = np.linspace(first, max(last, first), n_out)
        lo = np.floor(pos).astype(int)
        hi = np.minimum(lo + 1, max(last, first))
        frac = (pos - lo).astype(np.float32)
        need = set(lo.tolist()) | set(hi.tolist())

        keep, cache, idx, cursor = [], {}, 0, 0
        while idx < src_n and cursor < n_out:
            ok, bgr = cap.read()
            if not ok:
                break
            if idx in need:
                cache[idx] = self._prepare(bgr, dim, saturation)
            while cursor < n_out and hi[cursor] <= idx:
                a, b, w = cache[lo[cursor]], cache[hi[cursor]], float(frac[cursor])
                keep.append(a if w < 1e-3 else
                            cv2.addWeighted(a, 1.0 - w, b, w, 0.0))
                cursor += 1
                # Positions are monotonic, so anything before the next `lo` is
                # finished with. Without this the cache is the whole clip.
                if cursor < n_out:
                    for k in [k for k in cache if k < lo[cursor]]:
                        del cache[k]
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
        # **Ceil, and never smaller than the crop.** `int(sw * s)` truncates,
        # and when the source is exactly the frame's aspect that lands one pixel
        # *under* the target — `x0` goes to -1, the negative index wraps, and the
        # crop silently comes back one pixel wide. It only bites at some zoom
        # values (1.06 collapses, 1.12 does not), which is the worst kind of
        # latent bug: invisible until someone changes a default.
        nw = max(w, math.ceil(sw * s))
        nh = max(h, math.ceil(sh * s))
        bgr = cv2.resize(bgr, (nw, nh),
                         interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_LANCZOS4)
        y0 = max(0, (nh - h) // 2)
        x0 = max(0, (nw - w) // 2)
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
        #
        # **The crop is subpixel, and on a video shot that matters more than
        # anywhere else in the repo.** Everything else here already knew integer
        # crops judder; this path was written with `int()` on the crop box and a
        # `//2` origin, so the push moved in whole-pixel steps. On a still that
        # is a mild stutter. On stock footage it is a visible glitch, because
        # the sources are 25fps against a 30fps timeline — every sixth output
        # frame repeats a source frame, and with an integer crop those repeats
        # are *pixel-identical*, so the picture freezes and then jumps. One
        # float warp does the crop and the scale together and keeps the push
        # continuous through the duplicates.
        k = 1.0 - (1.0 - 1.0 / self.zoom) * f
        cw = buf.shape[1] * k
        ch = buf.shape[0] * k
        x0 = (buf.shape[1] - cw) / 2.0
        y0 = (buf.shape[0] - ch) / 2.0
        sc = fr.w / cw
        m = np.float32([[sc, 0.0, -x0 * sc], [0.0, sc, -y0 * sc]])
        out = Image.fromarray(cv2.warpAffine(
            buf, m, fr.size, flags=cv2.INTER_LANCZOS4,
            borderMode=cv2.BORDER_REPLICATE))

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

        out = self._note(out, f)
        return out

    def _note(self, out: "Image.Image", f: float) -> "Image.Image":
        """A small figure card in the lower left — "92 dB / music on a train".

        **A number that is only spoken is a number the viewer does not keep.**
        The AirPods cut says eight decibel figures out loud and drew exactly
        four of them, in one `bars` beat forty seconds away from where most of
        them are said. The user's note was to put them on screen as notes,
        clean and easy to understand, and this is that: the figure large in the
        brand accent, one plain-English line under it saying what that level
        actually sounds like, on a short rule.

        **It is deliberately not `label`.** That treatment is 96px and centred
        and it *is* the statement the shot exists for — two of those in one
        section would fight. A note annotates: it sits out of the way in the
        lower left, it is small, and the footage stays the picture. This is the
        corner label the big statement replaced, brought back for the one job
        it was always right for, which is a unit of measurement.

        Lower left rather than lower third centre because burned captions are
        centred at mid-frame in the shorts and the SRT sits at the bottom of a
        YouTube player — a note in the middle would collide with both.
        """
        if not self.note or self.brand is None:
            return out
        from PIL import ImageFont

        from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

        figure, gloss = self.note
        fr = self.frame
        k = fr.w / 1920

        # Settles in over the first third of a second and never leaves. A note
        # that animated out would be a second thing moving in a frame whose
        # whole job is to be footage.
        e = min(1.0, (f * self.hold_s) / 0.34) if self.hold_s else 1.0
        e = 1.0 - (1.0 - e) ** 2

        fig_size = max(28, int(72 * k))
        gloss_size = max(16, int(32 * k))
        ff = ImageFont.truetype(FONT_DISPLAY, fig_size)
        gf = ImageFont.truetype(FONT_CAPTION, gloss_size,
                                index=FONT_CAPTION_INDEX)

        x = int(96 * k)
        # Off the floor by more than it looks: a 16:9 player puts its scrubber
        # and an SRT line across the bottom, and 9:16 puts the caption block at
        # SAFE_BOTTOM. Measured from the bottom so it holds in either frame.
        base = fr.h - int(150 * k)

        out = out.convert("RGBA")
        d = ImageDraw.Draw(out)

        fig_h = fig_size
        gloss_h = gloss_size
        block_h = fig_h + int(gloss_h * 1.5)
        top = base - block_h + int(round(14 * (1.0 - e)))

        # A scrim only under the block, and a soft one. Footage is dimmed
        # already; a hard panel here would read as a lower-third graphic from a
        # news broadcast, which is not this format.
        pad = int(22 * k)
        wfig = d.textlength(figure, font=ff)
        wgl = d.textlength(gloss, font=gf) if gloss else 0
        bw = int(max(wfig, wgl)) + 2 * pad + int(10 * k)
        scrim = Image.new("RGBA", (bw, block_h + 2 * pad), (0, 0, 0, 118))
        out.alpha_composite(scrim, (x - pad, top - pad))
        d = ImageDraw.Draw(out)

        # The rule is vertical here, not horizontal. A horizontal rule above
        # the figure is the chapter card's move and this must not read as a
        # chapter card; a vertical rule down the left edge reads as a margin
        # note, which is exactly what it is.
        rule_h = int(block_h * e)
        if rule_h > 2:
            rx = x - int(16 * k)
            d.line([(rx, top), (rx, top + rule_h)],
                   fill=self.brand.primary, width=max(2, int(5 * k)))

        d.text((x, top), figure, font=ff, fill=self.brand.primary)
        if gloss:
            d.text((x, top + int(fig_h * 1.16)), gloss, font=gf,
                   fill=(238, 238, 238))
        return out.convert("RGB")
