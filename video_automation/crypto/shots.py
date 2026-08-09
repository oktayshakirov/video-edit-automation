"""Photo-driven crypto shorts — the site's own images, cut to the narration.

The drone channel's one hard lesson is that the angle beats the footage, and the
crypto skill's is that volume is the failure mode. Both point the same way: the
picture here is not the product, but it is what buys the seconds the script needs
to land. Text on a gradient does not hold a viewer for thirty seconds.

Every image comes from `crypto-wiki/public/images` — already licensed, already on
brand, and already attached to the post the short is built from. Nothing is
fetched from a stock API. That also sidesteps the pattern both platforms suppress,
which is an AI voice read over generic stock loops.

**The site's images are small.** Most are 700-1200px wide and all are landscape,
so none of them can fill a 1080x1920 frame without a 3x upscale. The fix is the
blurred-fill layout: the same image scaled to cover the frame and heavily
blurred, with the sharp copy laid over it at its honest size. The frame is full
of picture, nothing is upscaled past about 1.4x, and the blur hides that the
backdrop is a stretch.

Motion comes from a slow Ken Burns on both layers at different rates, so the
sharp image and its own blurred backdrop separate. As everywhere else in this
repo, the moves are subpixel — at these speeds integer steps read as judder.
"""

from __future__ import annotations

import math
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX, OUT_H, OUT_W

# thecrypto.wiki's palette, from the site's `config/theme.json`.
GOLD = (229, 194, 0)            # #e5c200 — primary and border
BODY = (23, 23, 23)             # #171717
PANEL = (47, 47, 47)            # #2f2f2f

SITE_IMAGES = Path.home() / "Coding/crypto-wiki/public/images"
LOGO = SITE_IMAGES / "logo.png"

# Same union safe box as the tinnitus shorts: all three platforms stack buttons
# down the right edge and text along the bottom, and the top band carries tabs.
SAFE_TOP, SAFE_BOTTOM = 230, 1440

XFADE = 0.45                    # shot-to-shot crossfade


@dataclass
class Shot:
    """One beat of picture. Either an image from the site, or a drawn graphic.

    `hold` is filled in by `plan_shots` from the measured narration — a shot
    lasts exactly as long as the sentence it illustrates, so the picture can
    never drift out of step with the voice.
    """
    image: Path | None = None
    graphic: str | None = None          # "checklist", or None for a photo
    payload: tuple = ()
    backdrop: Path | None = None        # photo behind a drawn beat
    reveals: list[float] | None = None  # absolute times, one per checklist item
    zoom: float = 1.12                  # Ken Burns travel over the whole shot
    pan: tuple[float, float] = (0.0, 0.0)
    aspect: float = 1.15                # target crop shape, w:h
    bias: float = 0.5                   # vertical crop position, 0 top 1 bottom
    start: float = 0.0
    hold: float = 0.0


def plan_shots(shots: list[Shot], spans: list[tuple[float, float]]) -> list[Shot]:
    """Give each shot the span of the sentence it belongs to.

    One shot per sentence, not per caption. Cutting on every caption chunk is
    two or three cuts a second, which reads as a montage rather than as a piece
    with something to say.
    """
    if len(shots) != len(spans):
        raise ValueError(f"{len(shots)} shots for {len(spans)} sentences — "
                         f"they must correspond one to one")
    for shot, (a, b) in zip(shots, spans):
        shot.start, shot.hold = a, b - a
    return shots


# --- the frame -----------------------------------------------------------

def _cover(img: Image.Image, w: int, h: int) -> Image.Image:
    """Scale-and-crop to fill exactly, preserving aspect."""
    s = max(w / img.width, h / img.height)
    r = img.resize((max(1, int(img.width * s)), max(1, int(img.height * s))),
                   Image.LANCZOS)
    return r.crop(((r.width - w) // 2, (r.height - h) // 2,
                   (r.width - w) // 2 + w, (r.height - h) // 2 + h))


class PhotoShot:
    """A prepared image shot. Layers are built once; frames are cheap crops."""

    MAX_UPSCALE = 1.45          # past this the blur stops covering for it

    def __init__(self, path: Path, zoom: float, pan: tuple[float, float],
                 aspect: float = 1.15, bias: float = 0.5):
        src = Image.open(path).convert("RGB")
        self.zoom, self.pan = zoom, pan

        # Backdrop: cover the frame with headroom for the move, then blur hard
        # enough that the upscale is invisible. The blur radius scales with the
        # upscale factor, because a 400px source stretched to 1080 needs far
        # more hiding than a 1200px one.
        pad = int(200 * zoom)
        up = max(1.0, (OUT_W + pad) / src.width)
        back = _cover(src, OUT_W + pad, OUT_H + pad)
        back = back.filter(ImageFilter.GaussianBlur(28 + 14 * up))
        self.back = np.asarray(back)
        # Dimmed, so the sharp copy sits forward instead of competing with a
        # full-brightness copy of itself.
        self.back = (self.back * 0.42).astype(np.uint8)

        # Crop toward a taller shape before scaling. Every image on the site is
        # landscape, so at full width the sharp strip is only about a third of a
        # 9:16 frame and the other two thirds are blur. Cropping in gives the
        # photograph half the frame or better.
        #
        # How far it can crop is bounded by resolution, not by taste: cropping
        # narrows the source, which raises the upscale needed to reach 1080.
        # `MAX_UPSCALE` is the real constraint and the aspect target yields to it.
        crop_w = min(src.width, src.height * aspect)
        crop_w = min(src.width, max(crop_w, OUT_W / self.MAX_UPSCALE))
        crop_h = min(src.height, crop_w / aspect)
        left = (src.width - crop_w) / 2
        top = (src.height - crop_h) * bias
        crop = src.crop((int(left), int(top),
                         int(left + crop_w), int(top + crop_h)))

        target_w = min(int(OUT_W * zoom), int(crop.width * self.MAX_UPSCALE))
        self.sharp = crop.resize(
            (target_w, max(1, int(crop.height * target_w / crop.width))),
            Image.LANCZOS)

    def photo_box(self, f: float = 0.5) -> tuple[float, float, float, float]:
        """Where the sharp photograph sits at `f`. Captions key off this."""
        k = 1.0 + (self.zoom - 1.0) * f
        w = self.sharp.width / self.zoom * k
        h = self.sharp.height / self.zoom * k
        x = (OUT_W - w) / 2 + self.pan[0] * (f - 0.5) * OUT_W
        y = (OUT_H - h) / 2 + self.pan[1] * (f - 0.5) * OUT_H
        return x, y, w, h

    def frame(self, f: float) -> Image.Image:
        """`f` runs 0..1 across the shot."""
        # Backdrop drifts one way, sharp layer the other. Opposed moves at
        # different rates is what makes a still photograph read as a shot.
        bx = (self.back.shape[1] - OUT_W) * (0.5 + 0.42 * (f - 0.5))
        by = (self.back.shape[0] - OUT_H) * (0.5 - 0.42 * (f - 0.5))
        out = Image.fromarray(_subpixel(self.back, bx, by, OUT_W, OUT_H))

        # The sharp copy zooms slightly and slides along `pan`.
        k = 1.0 + (self.zoom - 1.0) * f
        w = int(self.sharp.width / self.zoom * k)
        h = int(self.sharp.height / self.zoom * k)
        img = self.sharp.resize((w, h), Image.LANCZOS)
        x = (OUT_W - w) / 2 + self.pan[0] * (f - 0.5) * OUT_W
        y = (OUT_H - h) / 2 + self.pan[1] * (f - 0.5) * OUT_H
        out.paste(img, (int(round(x)), int(round(y))))

        # A hairline in the site's gold along the photo's edges, which reads as
        # deliberate framing rather than as an image that failed to fill.
        d = ImageDraw.Draw(out)
        x0, x1 = int(round(x)), int(round(x)) + w
        for edge in (int(round(y)), int(round(y)) + h):
            if 0 < edge < OUT_H:
                # Only across the photograph, not the whole frame. Drawn full
                # width it read as a band the picture was supposed to fill, which
                # made a narrow source look like a rendering bug.
                d.line([(x0, edge), (x1, edge)], fill=GOLD, width=3)
        return out


def _subpixel(arr: np.ndarray, x: float, y: float, w: int, h: int) -> np.ndarray:
    ix, iy = int(x), int(y)
    m = np.float32([[1, 0, ix - x], [0, 1, iy - y]])
    win = arr[iy:iy + h + 1, ix:ix + w + 1]
    return cv2.warpAffine(win, m, (w, h), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)


# --- the drawn beat ------------------------------------------------------

class ChecklistShot:
    """A struck-through list that fills in on the voice.

    The one beat that is drawn rather than photographed, and the reason the
    format is not stock-footage-with-narration: it shows the argument instead of
    illustrating it. Items land on `reveals` — absolute times taken from the
    caption spans — so a line appears exactly as it is spoken. Revealing them on
    even fractions of the shot looks synced until you watch it, and then every
    item is a beat early or late.

    It draws over a photograph, dimmed and blurred, rather than over flat black.
    A flat panel for six seconds in the middle of a photo-driven piece reads as
    the video having stopped, and it left the frame mostly empty.
    """

    def __init__(self, items: list[tuple[str, bool]], title: str = "",
                 backdrop: Path | None = None,
                 reveals: list[float] | None = None,
                 start: float = 0.0, hold: float = 1.0,
                 font_path: str = FONT_CAPTION,
                 font_index: int = FONT_CAPTION_INDEX):
        self.items = items
        self.title = title
        self.reveals = reveals
        self.start, self.hold = start, hold
        self.font = ImageFont.truetype(font_path, 54, index=font_index)
        self.title_font = ImageFont.truetype(font_path, 40, index=font_index)

        self.back = None
        if backdrop is not None and Path(backdrop).exists():
            im = _cover(Image.open(backdrop).convert("RGB"), OUT_W, OUT_H)
            im = im.filter(ImageFilter.GaussianBlur(30))
            # 0.30 was measured against the real frame and came out barely
            # distinguishable from flat black, which was the thing this backdrop
            # exists to avoid. The white type carries a 3px stroke, so it can
            # afford a backdrop with something visible in it.
            self.back = (np.asarray(im) * 0.5).astype(np.uint8)

    def frame(self, f: float) -> Image.Image:
        if self.back is not None:
            out = Image.fromarray(self.back.copy())
        else:
            out = Image.new("RGB", (OUT_W, OUT_H), BODY)
        d = ImageDraw.Draw(out)

        # A faint gold grid, drifting, so the beat still has motion in it.
        step, off = 96, int((f * 40) % 96)
        for gx in range(-96 + off, OUT_W + 96, step):
            d.line([(gx, 0), (gx, OUT_H)], fill=(40, 38, 26), width=2)
        for gy in range(-96 + off, OUT_H + 96, step):
            d.line([(0, gy), (OUT_W, gy)], fill=(40, 38, 26), width=2)

        n = len(self.items)
        top = OUT_H // 2 - (n * 124) // 2
        if self.title:
            d.text((110, top - 104), self.title, font=self.title_font, fill=GOLD)

        t = self.start + f * self.hold
        for i, (text, ok) in enumerate(self.items):
            due = (self.reveals[i] if self.reveals
                   else self.start + self.hold * (i / n) * 0.85)
            if t < due:
                continue
            y = top + i * 124
            colour = GOLD if ok else (196, 84, 84)
            _mark(d, 110, y + 16, 44, ok, colour)
            # White for every item, struck or not. Grey-on-dark was measured
            # against the real frame and was not readable on a phone — the
            # strike-through already says "this one does not count", so the ink
            # does not have to say it a second time by being harder to read.
            d.text((200, y), text, font=self.font, fill=(255, 255, 255),
                   stroke_width=3, stroke_fill=(0, 0, 0))
            if not ok:
                bbox = d.textbbox((200, y), text, font=self.font)
                mid = (bbox[1] + bbox[3]) // 2
                d.line([(200, mid), (bbox[2], mid)], fill=(230, 96, 96), width=5)
        return out


def _mark(d: ImageDraw.ImageDraw, x: int, y: int, s: int,
          ok: bool, colour: tuple[int, int, int]) -> None:
    """A tick or a cross, drawn from line segments."""
    w = 7
    if ok:
        d.line([(x, y + s * 0.55), (x + s * 0.38, y + s * 0.92),
                (x + s, y + s * 0.08)], fill=colour, width=w, joint="curve")
    else:
        d.line([(x, y), (x + s, y + s)], fill=colour, width=w)
        d.line([(x + s, y), (x, y + s)], fill=colour, width=w)


# --- watermark -----------------------------------------------------------

def logo_mark(width: int = 300, opacity: int = 255) -> Image.Image | None:
    """The site's wordmark, full opacity, no extra type.

    Unlike the tinnitus mascot this asset already contains the domain, so there
    is nothing to add under it.
    """
    if not LOGO.exists():
        return None
    im = Image.open(LOGO).convert("RGBA")
    im = im.crop(im.getbbox())
    im = im.resize((width, max(1, int(im.height * width / im.width))),
                   Image.LANCZOS)
    if opacity < 255:
        im.putalpha(im.split()[-1].point(lambda v: int(v * opacity / 255)))
    return im


# --- assembly ------------------------------------------------------------

def render_shots(out: Path, shots: list[Shot], total: float, fps: int = 30,
                 logo_at: tuple[int, int] = (58, 268), logo_w: int = 300,
                 logo_float: float = 8.0, logo_period: float = 6.5) -> Path:
    """Render the picture track: every shot, crossfaded, with the watermark."""
    prepared = []
    for s in shots:
        if s.image is not None:
            prepared.append(PhotoShot(s.image, s.zoom, s.pan, s.aspect, s.bias))
        else:
            prepared.append(ChecklistShot(*s.payload, backdrop=s.backdrop,
                                          reveals=s.reveals,
                                          start=s.start, hold=s.hold))

    mark = logo_mark(logo_w)
    if mark is not None and logo_at[1] - logo_float < SAFE_TOP:
        raise ValueError(f"logo_at={logo_at} floats above SAFE_TOP={SAFE_TOP}")

    n = int(round(total * fps)) + fps // 2
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{OUT_W}x{OUT_H}", "-r", str(fps), "-i", "-",
         "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)

    for i in range(n):
        t = i / fps
        idx = max(0, min(len(shots) - 1,
                         next((k for k, s in enumerate(shots)
                               if t < s.start + s.hold), len(shots) - 1)))
        s = shots[idx]
        f = 0.0 if s.hold <= 0 else min(1.0, max(0.0, (t - s.start) / s.hold))
        frame = prepared[idx].frame(f)

        # Crossfade into the next shot over its final XFADE seconds. Dissolves
        # rather than cuts: the piece is one continuous argument, and a hard cut
        # every five seconds fights the voice instead of following it.
        left = s.start + s.hold - t
        if idx + 1 < len(shots) and 0 < left < XFADE:
            nxt = shots[idx + 1]
            nf = 0.0 if nxt.hold <= 0 else max(0.0, (t - nxt.start) / nxt.hold)
            frame = Image.blend(frame, prepared[idx + 1].frame(nf),
                                1.0 - left / XFADE)

        if mark is not None:
            frame = frame.convert("RGBA")
            by = logo_at[1] + logo_float * math.sin(2 * math.pi * t / logo_period)
            iy = math.floor(by)
            frame.alpha_composite(
                mark.transform(mark.size, Image.AFFINE,
                               (1, 0, 0, 0, 1, iy - by), resample=Image.BILINEAR),
                (logo_at[0], iy))
            frame = frame.convert("RGB")

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while encoding the picture track")
    return out
