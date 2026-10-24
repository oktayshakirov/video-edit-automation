"""`reel` - a strip of cards the camera travels along.

From a reference the user liked (2026-10-22): the "extended screen" move,
where the frame is a window onto a wider surface and the camera follows a row
of cards - clips, photographs or plain text - each with a label, gliding from
one to the next as the voice reaches it. Our own version, in the brand's
pieces:

* **The surface moves, not just the cards.** A faint dot grid on the beat's
  own backdrop travels with the camera. Without it the cards would slide
  over a still background and read as a carousel; with it the frame reads as
  a camera moving over something larger than itself.
* **The camera is voice-led.** Card `i` is brought to centre on reveal `i` -
  the caption that names it - in a smoothstepped travel that pulls back a
  little in the middle and settles. Horizontal motion blur scales with the
  camera's speed, so the travel smears and the settle is sharp.
* **Focus by distance.** Cards dim as they leave the centre; the next card
  peeking in at the edge is a promise, not a distraction.
* **Labels are the band card's**: a pill in `Brand.band` with condensed
  tracked caps, popping in when its card is named.
* **A slight barrel curve** over the whole frame - the bulge of the
  reference - and a vignette.

**It can be entered and left through a card** (2026-10-22). `enter=True`:
the camera dives into the last card until it fills the frame and the reel
cuts to the next shot - seamless when that shot is the same clip, which
`link_reels` continues from the card's own frame; into a chapter card it
reads as going through the card. `emerge=True` is the reverse: the reel opens
full-frame on its first card - continuing the previous clip when it is the
same file - and pulls back to the strip. The grid, the other cards, the
labels, the shadow and the curve all fade with the dive, so the last frame of
an enter is plain footage.

payload: (items, title, enter, emerge) where items is
[(media, label[, offset]), ...]. `media` is an image path, a video path
(played from `offset` seconds, looping) or None for a text card that shows the
label large. `title` is an optional kicker, fixed.
"""

from __future__ import annotations

import math
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ...core.draw import ease_out
from .base import Beat, _smooth

VIDEO = {".mp4", ".mov", ".m4v", ".webm"}
FONT_LABEL = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"


def _norm(item) -> tuple:
    """(media, label, offset) from a card given as 1, 2 or 3 values."""
    it = tuple(item)
    m, lab, off = (it + (None, "", 0.0)[len(it):])[:3]
    return m, lab or "", float(off or 0.0)


# The grade `clip.VideoShot` gives footage. A card that a cut continues as
# a full-frame clip has to match it, or the cut shows as a colour jump.
DIM, SAT = 0.86, 0.82


class _Media:
    """One card's source picture at full resolution, graded like footage.

    Kept full-size rather than pre-fitted to the card, because a card the
    camera dives into ends up filling the frame - several times its resting
    size - and a pre-shrunk card would arrive soft.
    """

    def __init__(self, path, offset: float = 0.0):
        self.path = Path(path) if path else None
        self.offset = offset
        self.still = None
        self.cap = None
        if self.path is None or not self.path.exists():
            return
        if self.path.suffix.lower() in VIDEO:
            self._open()
        else:
            self.still = np.asarray(Image.open(self.path).convert("RGB"))

    def _open(self):
        self.cap = cv2.VideoCapture(str(self.path))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30.0
        self.count = max(1, int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.pos, self.last = -1, None


    def raw(self, t: float) -> np.ndarray | None:
        if self.still is not None:
            return self.still
        if self.cap is None:
            return None
        want = int(max(0.0, t + self.offset) * self.fps) % self.count
        if want < self.pos:                 # looped, or asked for an earlier frame
            self.cap.release()
            self._open()
        while self.pos < want:
            if not self.cap.grab():
                break
            self.pos += 1
        if self.last is None or self.last[0] != self.pos:
            ok, bgr = self.cap.retrieve()
            if ok:
                self.last = (self.pos, cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        return self.last[1] if self.last else None


def _grade(rgb: np.ndarray) -> np.ndarray:
    """`VideoShot._prepare`'s grade, the same function, so a dive's last frame and
    the clip's first agree. Applied to the on-screen crop only - grading the
    full source frame was most of the reel's render time."""
    from ..clip import grade
    return grade(rgb, DIM, SAT)


def _view(raw: np.ndarray, x0: float, y0: float, w: float, h: float,
          W: int, H: int, grade: bool = False):
    """The visible part of `raw` covered into the screen rect (x0, y0, w, h).

    Returns (image, (vx, vy)) or None. Only the part on screen is resampled,
    so a card scaled to four times the frame costs one frame of pixels.
    """
    rh, rw = raw.shape[:2]
    c = max(w / rw, h / rh)
    ox, oy = x0 + (w - rw * c) / 2, y0 + (h - rh * c) / 2
    vx0, vy0 = max(0, int(math.floor(x0))), max(0, int(math.floor(y0)))
    vx1, vy1 = min(W, int(math.ceil(x0 + w))), min(H, int(math.ceil(y0 + h)))
    if vx1 - vx0 < 2 or vy1 - vy0 < 2:
        return None
    src = raw
    if c < 0.9:                             # shrink first, cleanly
        src = cv2.resize(raw, (max(1, int(rw * c)), max(1, int(rh * c))),
                         interpolation=cv2.INTER_AREA)
        k = src.shape[1] / rw
        c, rw = c / k, src.shape[1]
    m = np.float32([[c, 0, ox - vx0], [0, c, oy - vy0]])
    out = cv2.warpAffine(src, m, (vx1 - vx0, vy1 - vy0),
                         flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return Image.fromarray(_grade(out) if grade else out), (vx0, vy0)


def dot_grid(out: Image.Image, cam: float, zoom: float, brand, frame) -> None:
    """The faint dot grid the camera beats move over, offset by the camera.

    Shared by `reel` and `post`: the surface moving is what makes a moving
    card read as a camera rather than a slide.
    """
    W, H = frame.size
    d = ImageDraw.Draw(out)
    g = W * 0.035 * zoom
    x0 = (W / 2 - cam * zoom) % g
    y0 = (H / 2) % g
    col = tuple(int(c * 0.45 + 40) for c in brand.primary)
    r = max(2, int(W / 900))
    y = y0
    while y < H:
        x = x0
        while x < W:
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
            x += g
        y += g


class Reel(Beat):
    TRAVEL = 0.62           # one card to the next
    LEAD = 0.10             # the travel starts just before the word
    PULL = 0.10             # how far the camera pulls back mid-travel
    CURVE = 0.045           # barrel strength
    ENTER = 0.80            # the dive into the last card
    EMERGE = 0.90           # the pull back out of the first

    def __init__(self, items: list, title: str = "", enter: bool = False,
                 emerge: bool = False, **kw):
        super().__init__(**kw)
        self.items = [_norm(it) for it in items]
        self.title, self.enter, self.emerge = title, bool(enter), bool(emerge)
        W, H = self.frame.size
        # **4:5 cards in 9:16.** A 16:9 card in a tall frame leaves two
        # thirds of a phone screen as empty backdrop; a portrait card fills
        # it and is a quarter the zoom to dive into. Footage is cover-cropped
        # to it, centred - the same crop a 9:16 clip shot takes.
        self.card_w = int(W * (0.84 if self.portrait else 0.44))
        self.card_h = int(self.card_w * (1.25 if self.portrait else 9 / 16))
        self.pitch = int(self.card_w * 1.12)
        self.radius = max(8, int(W * 0.010))
        # The zoom at which a card covers the whole frame.
        self.fill = max(W / self.card_w, H / self.card_h) * 1.004
        size = int(self.card_w * 0.073)
        self.lab_font = ImageFont.truetype(FONT_LABEL, size)
        self.lab_size = size
        self.big_font = ImageFont.truetype(
            FONT_LABEL, int(min(self.card_w * 9 / 16, self.card_h) * 0.52))
        self.media = [_Media(m, off) for m, _, off in self.items]
        self._text = {}
        self._maps = None

    def _text_card(self, label: str) -> np.ndarray:
        """A text card's picture, drawn at twice its resting size."""
        if label not in self._text:
            w, h = self.card_w * 2, self.card_h * 2
            im = Image.new("RGB", (w, h), tuple(int(c) for c in self.brand.panel))
            d = ImageDraw.Draw(im)
            bb = d.textbbox((0, 0), label.upper(), font=self.big_font)
            d.text(((w - (bb[2] - bb[0])) / 2 - bb[0],
                    (h - (bb[3] - bb[1])) / 2 - bb[1]),
                   label.upper(), font=self.big_font, fill=self.brand.ink)
            self._text[label] = np.asarray(im)
        return self._text[label]

    # --- the camera -----------------------------------------------------

    def _times(self) -> list[float]:
        n = len(self.items)
        rv = list(self.reveals or [])
        return [rv[i] if i < len(rv) else
                self.start + self.hold * (0.12 + 0.8 * i / max(n, 1))
                for i in range(n)]

    def camera(self, t: float) -> tuple[float, float, float]:
        """(world x at the frame's centre, zoom, immersion 0..1).

        Immersion is how far into a card the camera is - 1 when one card
        fills the frame - and everything that is not that card fades by it.
        """
        e = t - self.start
        if self.emerge:
            cam, zoom = 0.0, 1.0
        else:
            # Glide in from the left of the first card as the beat opens.
            g = 1.0 - _smooth(min(1.0, e / 0.9))
            cam, zoom = -0.45 * self.pitch * g, 1.0 + 0.05 * g
        for r in self._times()[1:]:
            p = _smooth((t - (r - self.LEAD)) / self.TRAVEL)
            cam += self.pitch * p
            zoom -= self.PULL * math.sin(math.pi * p)
        cam += 10.0 * e                     # a slow drift keeps it alive

        imm = 0.0
        if self.emerge:
            q = min(1.0, max(0.0, e / self.EMERGE))
            em = 1.0 - ease_out(q)
            # A clip's last frame sits at its own 1.06 Ken Burns zoom.
            zoom = zoom + (self.fill * 1.06 - zoom) * em
            cam *= 1.0 - em
            imm = max(imm, em)
        if self.enter:
            span = max(0.2, self.ENTER - 0.05)   # full before the last frame
            q = min(1.0, max(0.0, (t - (self.start + self.hold - self.ENTER))
                             / span))
            ep = q * q
            last = (len(self.items) - 1) * self.pitch
            cam = cam + (last - cam) * _smooth(q)
            zoom = zoom + (self.fill - zoom) * ep
            imm = max(imm, ep)
        return cam, zoom, imm

    # --- drawing ----------------------------------------------------------

    def _grid(self, out: Image.Image, cam: float, zoom: float) -> None:
        dot_grid(out, cam, zoom, self.brand, self.frame)

    def _label(self, layer: Image.Image, text: str, cx: float, top: float,
               s: float, a: float) -> None:
        if not text or s <= 0.01 or a <= 0.01:
            return
        d = ImageDraw.Draw(layer)
        f = self.lab_font
        track = self.lab_size * 0.12
        tw = (sum(d.textlength(c, font=f) for c in text.upper())
              + track * (len(text) - 1))
        bb = d.textbbox((0, 0), "H", font=f)
        cap = bb[3] - bb[1]
        pw, ph = tw + self.lab_size * 1.1, cap + self.lab_size * 0.75
        pill = Image.new("RGBA", (int(pw) + 2, int(ph) + 2), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pill)
        fill = self.brand.band or self.brand.primary
        pd.rounded_rectangle([0, 0, pw, ph], radius=int(ph * 0.22),
                             fill=(*fill, 255))
        x = (pw - tw) / 2
        for c in text.upper():
            pd.text((x, (ph - cap) / 2 - bb[1]), c, font=f,
                    fill=(*self.brand.band_ink, 255))
            x += pd.textlength(c, font=f) + track
        if abs(s - 1.0) > 0.01:
            pill = pill.resize((max(1, int(pill.width * s)),
                                max(1, int(pill.height * s))), Image.BILINEAR)
        if a < 1.0:
            pill.putalpha(pill.getchannel("A").point(lambda v: int(v * a)))
        layer.alpha_composite(pill, (int(cx - pill.width / 2),
                                     int(top - pill.height / 2)))

    def _curve(self, out: Image.Image) -> Image.Image:
        W, H = self.frame.size
        if self._maps is None:
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            nx, ny = (xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)
            r2 = nx * nx + ny * ny
            k = 1.0 - self.CURVE * (1.0 - r2 * 0.5)
            mx = (nx * k) * (W / 2) + W / 2
            my = (ny * k) * (H / 2) + H / 2
            vig = np.clip(1.0 - 0.28 * r2 ** 1.4, 0.0, 1.0)
            vig = np.repeat((vig * 255).astype(np.uint8)[:, :, None], 3, axis=2)
            m1, m2 = cv2.convertMaps(mx, my, cv2.CV_16SC2)
            self._maps = (m1, m2, vig)
        m1, m2, vig = self._maps
        a = cv2.remap(np.asarray(out), m1, m2, cv2.INTER_LINEAR,
                      borderMode=cv2.BORDER_REFLECT)
        return Image.fromarray(cv2.multiply(a, vig, scale=1 / 255))

    def content(self, out: Image.Image, f: float) -> None:
        from ...core.transitions import _blur_x

        W, H = self.frame.size
        t = self.at(f)
        e = t - self.start
        cam, zoom, imm = self.camera(t)
        speed = abs(self.camera(t + 1 / 30)[0] - cam) * zoom   # px a frame
        keep = 1.0 - imm                    # what is not the card fades by it

        if keep > 0.02:
            grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            self._grid(grid, cam, zoom)
            if keep < 1.0:
                grid.putalpha(grid.getchannel("A").point(
                    lambda v: int(v * keep)))
            base = out.convert("RGBA")
            base.alpha_composite(grid)
            out.paste(base.convert("RGB"))

        cw, ch = self.card_w * zoom, self.card_h * zoom
        cy0 = H * (0.52 if self.title else 0.50)
        cy = cy0 + (H / 2 - cy0) * imm
        times = self._times()
        rad = int(self.radius * zoom * keep)

        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cards = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        labels = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        cd = ImageDraw.Draw(cards)

        for i, (m, label, _) in enumerate(self.items):
            sx = W / 2 + (i * self.pitch - cam) * zoom
            x0, y0 = sx - cw / 2, cy - ch / 2
            if x0 + cw < -20 or x0 > W + 20:
                continue
            dist = min(1.0, abs(i * self.pitch - cam) / self.pitch)
            light = 1.0 - 0.55 * _smooth(dist)
            if keep > 0.02:
                sd.rounded_rectangle([x0, y0 + 14 * zoom, x0 + cw,
                                      y0 + ch + 14 * zoom], radius=rad,
                                     fill=(0, 0, 0, int(235 * keep)))
            raw = self.media[i].raw(max(0.0, e))
            video = raw is not None and self.media[i].cap is not None
            if raw is None:
                raw = self._text_card(label)
            got = _view(raw, x0, y0, cw, ch, W, H, grade=video)
            if got is None:
                continue
            pic, (vx, vy) = got
            if light < 0.999:
                pic = Image.eval(pic, lambda v, k=light: int(v * k))
            mask = Image.new("L", pic.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                [x0 - vx, y0 - vy, x0 - vx + cw - 1, y0 - vy + ch - 1],
                radius=rad, fill=255)
            cards.paste(pic, (vx, vy), mask)
            if keep > 0.02:
                cd.rounded_rectangle([x0, y0, x0 + cw - 1, y0 + ch - 1],
                                     radius=rad, width=3,
                                     outline=(255, 255, 255,
                                              int(150 * light * keep)))

            # The label pops when its card is named; a text card has none.
            if m is not None and label and keep > 0.02:
                lp = (t - (times[i] + 0.18)) / 0.32
                if lp > 0:
                    k = 1.7
                    x1 = min(1.0, lp) - 1.0
                    pop = 1.0 + (k + 1.0) * x1 ** 3 + k * x1 ** 2
                    self._label(labels, label, sx, y0 + ch, pop * zoom,
                                min(1.0, lp * 2.0) * (0.55 + 0.45 * light)
                                # Gone early in a dive - a label growing
                                # with the zoom reads as a fault.
                                * keep ** 4)

        if keep > 0.02:
            # Blurred at a quarter size: a soft shadow has no detail to lose,
            # and the full-frame blur was a third of the frame's cost.
            q = 4
            small = shadow.resize((W // q, H // q), Image.BILINEAR)
            small = small.filter(ImageFilter.GaussianBlur(
                max(2, int(W * 0.010 / q))))
            shadow = small.resize((W, H), Image.BILINEAR)
        # Labels ride on their cards, so they smear with them - a sharp pill
        # over a blurred card reads as detached from it.
        layer = out.convert("RGBA")
        layer.alpha_composite(shadow)
        layer.alpha_composite(cards)
        layer.alpha_composite(labels)
        frame = layer.convert("RGB")
        if speed > 4:
            frame = _blur_x(frame, min(70.0, speed * 1.4))
        # The curve fades with the dive, so the last frame of an enter is the
        # footage exactly as the next shot will show it.
        if keep > 0.002:
            curved = self._curve(frame)
            frame = curved if keep >= 0.999 else Image.blend(frame, curved, keep)
        if self.title and keep > 0.7:
            self.heading(frame, self.title, f)
        out.paste(frame)


def _clip_seconds(path) -> float:
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    n = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0
    cap.release()
    return n / fps if fps else 0.0


def link_reels(shots) -> None:
    """Join each entering or emerging reel to the clip beside it.

    Runs after the timeline is laid out (holds are final). For a reel with
    `enter`: the cut out of it is made hard, and when the next shot is the
    same clip as the last card, that shot is started at the card's own media
    time, so the dive lands on the frame the clip continues from. For
    `emerge`: the cut in is made hard and, when the previous shot is the same
    clip as the first card, the card starts where that shot stopped. If the
    clip is too short to continue, the cut is still hard - just not seamless.
    """
    for i, sh in enumerate(shots):
        if sh is None or sh.graphic != "reel":
            continue
        pl = tuple(sh.payload) + ("", False, False)[len(sh.payload) - 1:]
        items, title, enter, emerge = list(pl[0]), pl[1], pl[2], pl[3]
        norm = [_norm(it) for it in items]
        if enter and i + 1 < len(shots) and shots[i + 1] is not None:
            nxt = shots[i + 1]
            sh.xfade, sh.transition = 0.0, None
            m, _, off = norm[-1]
            if (m is not None and nxt.clip is not None
                    and Path(nxt.clip) == Path(m)):
                at = off + sh.hold
                if at + nxt.hold <= _clip_seconds(m):
                    nxt.clip_at = at
        if emerge and i > 0 and shots[i - 1] is not None:
            prv = shots[i - 1]
            prv.xfade, prv.transition = 0.0, None
            m, lab, off = norm[0]
            if (m is not None and prv.clip is not None
                    and Path(prv.clip) == Path(m)):
                norm[0] = (m, lab, prv.clip_at + prv.hold)
        sh.payload = (norm, title, enter, emerge)
