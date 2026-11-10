"""A shot shown inside a window: a browser tab, a video player, a terminal.

The editor (2026-11-10): the videos look better with fewer plain stock clips
and more custom screens, and stock footage can sometimes sit in "a terminal
or player type look as if it's shown in a window or tab or browser". A clip
that fills the frame reads as stock; the same clip inside a window over the
brand's own background reads as something the video is *showing you* - a
page someone opened, a recording someone played. It also gives the frame
two layers that move apart, which a full-bleed clip does not have.

    Shot(clip=..., window="browser")
    Shot(clip=..., window=("browser", "binance.com/en/support/announcement"))
    Shot(clip=..., window=("player", "Robinhood keynote, 2025"))
    Shot(clip=..., window=("terminal", "$ whois tesla-token.xyz"))

It wraps any prepared shot - a clip, a photograph, a drawn beat - the same
way `Shot(shader=)` does: the inner shot draws its full frame as always, and
`WindowShot` cover-crops that frame into the window's content area. Nothing
here runs unless a shot asks for it, so every shipped video renders as it
did.

**Three kinds, one family:**

* `browser` - a title bar with three dots and an address pill. The text is
  the address; give it the page the line is about, never a made-up one.
* `player` - the picture with a control strip under it: play mark, a
  progress track in the brand colour that fills across the shot, a running
  time. The text is the recording's caption, top left.
* `terminal` - a dark title bar and a prompt line typed over the picture's
  top. The text is the command; it types on over the first 40% of the shot.

The window drifts from 96.5% to 100% of its size over the shot, eased, so a
held window is never a dead frame. The backdrop is the brand's own loop
(`core/backdrop.py`), dimmed, sampled by timeline seconds like every beat.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import backdrop as _backdrop
from .brand import CRYPTO, Brand
from .draw import ease_out
from .frame import Frame

KINDS = ("browser", "player", "terminal")

SANS = "/System/Library/Fonts/SFNS.ttf"
MONO = "/System/Library/Fonts/SFNSMono.ttf"

CHROME = (36, 36, 40)          # title bar and control strip
CHROME_LINE = (58, 58, 64)     # the hairline between bar and content
PILL = (22, 22, 25)            # the address field
TEXT = (210, 210, 215)
DIM = (140, 140, 148)
LIGHTS = ((255, 95, 87), (254, 188, 46), (40, 200, 64))
TERM_INK = (120, 230, 140)     # the prompt's text


def parse(spec) -> tuple[str, str]:
    """`"browser"` or `("browser", "text")` -> (kind, text)."""
    if spec is None:
        raise ValueError("no window spec")
    kind, text = (spec, "") if isinstance(spec, str) else (spec[0], spec[1] if len(spec) > 1 else "")
    if kind not in KINDS:
        raise ValueError(f"unknown window {kind!r} - known: {', '.join(KINDS)}")
    return kind, str(text)


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default(size=size)


@dataclass(frozen=True)
class Layout:
    x: int          # the window's left edge at full size
    y: int          # its top edge
    w: int
    bar: int        # title bar (browser, terminal) or control strip (player)
    ch: int         # content height
    radius: int

    @property
    def h(self) -> int:
        return self.bar + self.ch


def layout(frame: Frame) -> Layout:
    """Where the window sits in this frame.

    Landscape: 70% of the width, 16:9 content, centred but kept above the
    player's control bar; at that width the window's left edge clears the
    top-left watermark. Vertical:
    90% of the width, a near-square content area, its top under the
    watermark and its bottom above `safe_bottom`, where the captions start.
    """
    if frame.w >= frame.h:
        w = int(frame.w * 0.70)
        ch = int(w * 9 / 16)
        bar = int(w * 0.034)
        y = int((frame.h - ch - bar) / 2 + frame.h * 0.03)
        # Above the player's own control bar, which a paused 16:9 video
        # draws over its bottom (`safe_bottom`).
        y = min(y, frame.safe_bottom - ch - bar - 10)
    else:
        w = int(frame.w * 0.90)
        bar = int(w * 0.066)
        ch = int(w * 0.92)
        y = frame.logo_at[1] + 150
        y = min(y, frame.safe_bottom - ch - bar - 20)
    x = (frame.w - w) // 2
    return Layout(x, y, w, bar, ch, radius=max(10, int(w * 0.014)))


def _rounded_mask(w: int, h: int, r: int) -> np.ndarray:
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    return np.asarray(m).astype(np.float32) / 255.0


def _fit(text: str, font, width: float) -> str:
    probe = ImageDraw.Draw(Image.new("RGB", (4, 4)))
    if probe.textlength(text, font=font) <= width:
        return text
    while text and probe.textlength(text + "...", font=font) > width:
        text = text[:-1]
    return text + "..."


class WindowShot:
    """A prepared shot drawn inside a window. Everything else passes through."""

    GROW = 0.035          # 96.5% -> 100% over the shot
    TYPE_FOR = 0.40       # a terminal command types on over this share

    def __init__(self, inner, spec, start: float, hold: float, frame: Frame,
                 brand: Brand = CRYPTO):
        self.kind, self.text = parse(spec)
        self.inner, self.start, self.hold = inner, start, hold
        self.frame, self.brand = frame, brand
        self.L = layout(frame)
        L = self.L
        self.bg = _backdrop.get(brand.backdrop)
        self.mask = _rounded_mask(L.w, L.h, L.radius)
        self.font = _font(SANS, max(14, int(L.bar * 0.42)))
        self.mono = _font(MONO, max(14, int(L.bar * 0.44)))
        self.chrome = self._chrome()
        # The drop shadow is static: drawn once at full size, scaled with the
        # window, and cheap to warp.
        pad = int(L.w * 0.05)
        sh = Image.new("L", (L.w + 2 * pad, L.h + 2 * pad), 0)
        ImageDraw.Draw(sh).rounded_rectangle(
            [pad, pad + int(pad * 0.25), pad + L.w, pad + L.h + int(pad * 0.25)],
            radius=L.radius, fill=200)
        self.shadow = np.asarray(sh.filter(ImageFilter.GaussianBlur(pad * 0.45))
                                 ).astype(np.float32) / 255.0
        self.pad = pad

    # -- the static parts ------------------------------------------------

    def _lights(self, d: ImageDraw.ImageDraw, cy: float) -> float:
        L = self.L
        r = L.bar * 0.17
        x = L.bar * 0.55
        for c in LIGHTS:
            d.ellipse([x - r, cy - r, x + r, cy + r], fill=c)
            x += r * 3.2
        return x

    def _chrome(self) -> Image.Image:
        """The window without its picture: bar, strip, address, title."""
        L = self.L
        im = Image.new("RGB", (L.w, L.h), CHROME)
        d = ImageDraw.Draw(im)
        if self.kind == "player":
            # The control strip is under the content; the bar's space is it.
            top = L.ch
            d.line([(0, top), (L.w, top)], fill=CHROME_LINE, width=1)
            return im
        cy = L.bar / 2
        after = self._lights(d, cy)
        d.line([(0, L.bar - 1), (L.w, L.bar - 1)], fill=CHROME_LINE, width=1)
        if self.kind == "browser":
            pw = L.w * 0.56
            px = (L.w - pw) / 2
            ph = L.bar * 0.64
            d.rounded_rectangle([px, cy - ph / 2, px + pw, cy + ph / 2],
                                radius=ph / 2, fill=PILL)
            # A small lock, drawn rather than typed: no emoji font needed.
            lx, ly, s = px + ph * 0.55, cy, ph * 0.18
            d.rounded_rectangle([lx - s, ly - s * 0.2, lx + s, ly + s * 1.3],
                                radius=s * 0.3, fill=DIM)
            d.arc([lx - s * 0.7, ly - s * 1.3, lx + s * 0.7, ly + s * 0.3],
                  180, 360, fill=DIM, width=max(1, int(s * 0.35)))
            text = _fit(self.text or "", self.font, pw - ph * 1.6)
            tw = d.textlength(text, font=self.font)
            bb = d.textbbox((0, 0), "Hg", font=self.font)
            d.text((px + (pw - tw) / 2, cy - (bb[1] + bb[3]) / 2), text,
                   font=self.font, fill=TEXT)
        else:  # terminal
            title = "zsh"
            tw = d.textlength(title, font=self.mono)
            bb = d.textbbox((0, 0), "Hg", font=self.mono)
            d.text(((L.w - tw) / 2, cy - (bb[1] + bb[3]) / 2), title,
                   font=self.mono, fill=DIM)
        return im

    # -- per frame ---------------------------------------------------------

    def _content(self, f: float) -> np.ndarray:
        """The inner shot's frame, cover-cropped into the content area."""
        L = self.L
        pic = np.asarray(self.inner.draw(f).convert("RGB"))
        # Trim the inner frame's own edges first: a clip or photo draws the
        # brand hairline along them, which would show as a coloured rule
        # just inside the window.
        e = max(4, int(min(pic.shape[:2]) * 0.006))
        pic = pic[e:-e, e:-e]
        H, W = pic.shape[:2]
        want = L.w / L.ch
        if W / H > want:
            cw = int(round(H * want))
            x0 = (W - cw) // 2
            pic = pic[:, x0:x0 + cw]
        else:
            chh = int(round(W / want))
            y0 = (H - chh) // 2
            pic = pic[y0:y0 + chh]
        return cv2.resize(pic, (L.w, L.ch), interpolation=cv2.INTER_AREA)

    def _window(self, f: float) -> np.ndarray:
        L = self.L
        win = np.array(self.chrome)
        content = self._content(f)
        top = 0 if self.kind == "player" else L.bar
        win[top:top + L.ch] = content
        if self.kind == "player":
            self._strip(win, f)
        elif self.kind == "terminal" and self.text:
            self._prompt(win, f)
        return win

    def _strip(self, win: np.ndarray, f: float) -> None:
        """Play mark, progress, running time - drawn into the strip."""
        L = self.L
        strip = Image.fromarray(win[L.ch:])
        d = ImageDraw.Draw(strip)
        cy = L.bar / 2
        s = L.bar * 0.22
        x = L.bar * 0.6
        d.polygon([(x - s * 0.6, cy - s), (x - s * 0.6, cy + s), (x + s, cy)], fill=TEXT)
        secs = max(1.0, self.hold)
        now = f * secs
        stamp = f"{int(now // 60)}:{int(now % 60):02d} / {int(secs // 60)}:{int(round(secs % 60)):02d}"
        tw = d.textlength(stamp, font=self.font)
        bb = d.textbbox((0, 0), "0", font=self.font)
        d.text((L.w - tw - L.bar * 0.5, cy - (bb[1] + bb[3]) / 2), stamp,
               font=self.font, fill=DIM)
        t0, t1 = x + L.bar * 0.6, L.w - tw - L.bar * 1.0
        th = max(3, int(L.bar * 0.09))
        d.rounded_rectangle([t0, cy - th / 2, t1, cy + th / 2], radius=th, fill=(70, 70, 76))
        fx = t0 + (t1 - t0) * f
        d.rounded_rectangle([t0, cy - th / 2, fx, cy + th / 2], radius=th,
                            fill=self.brand.primary)
        d.ellipse([fx - th * 1.4, cy - th * 1.4, fx + th * 1.4, cy + th * 1.4],
                  fill=self.brand.primary)
        win[L.ch:] = np.asarray(strip)
        if self.text:
            # The recording's caption, top left, on a soft shade.
            top = Image.fromarray(win[:int(L.bar * 1.6)])
            shade = np.asarray(top).astype(np.float32)
            ramp = np.linspace(0.45, 1.0, shade.shape[0], dtype=np.float32)[:, None, None]
            top = Image.fromarray((shade * ramp).astype(np.uint8))
            dd = ImageDraw.Draw(top)
            dd.text((L.bar * 0.5, L.bar * 0.35),
                    _fit(self.text, self.font, L.w * 0.8), font=self.font, fill=(255, 255, 255))
            win[:top.height] = np.asarray(top)

    def _prompt(self, win: np.ndarray, f: float) -> None:
        """`$ command` typed over the picture's top, with a block cursor."""
        L = self.L
        n = len(self.text)
        shown = self.text[:int(math.ceil(n * min(1.0, f / self.TYPE_FOR)))]
        lh = int(L.bar * 1.25)
        band = win[L.bar:L.bar + lh].astype(np.float32) * 0.28
        band = Image.fromarray(band.astype(np.uint8))
        d = ImageDraw.Draw(band)
        bb = d.textbbox((0, 0), "Hg", font=self.mono)
        x, y = L.bar * 0.5, (lh - (bb[1] + bb[3])) / 2
        d.text((x, y), shown, font=self.mono, fill=TERM_INK)
        t = self.start + f * self.hold
        if shown != self.text or int(t * 2) % 2 == 0:
            cx = x + d.textlength(shown, font=self.mono) + 4
            d.rectangle([cx, y + bb[1], cx + L.bar * 0.22, y + bb[3]], fill=TERM_INK)
        win[L.bar:L.bar + lh] = np.asarray(band)

    def draw(self, f: float) -> Image.Image:
        fr, L = self.frame, self.L
        t = self.start + f * self.hold
        if self.bg is not None:
            canvas = (self.bg.at(t, fr.w, fr.h).astype(np.float32) * 0.62)
        else:
            canvas = np.empty((fr.h, fr.w, 3), np.float32)
            canvas[:] = self.brand.bg
        k = 1.0 - self.GROW * (1.0 - ease_out(f))
        cx, cy = L.x + L.w / 2, L.y + L.h / 2

        # Shadow, then the window, both through one float affine so they
        # move together at subpixel precision.
        def place(src_w, src_h, ox, oy):
            return np.float32([[k, 0, cx - k * (src_w / 2 - ox)],
                               [0, k, cy - k * (src_h / 2 - oy)]])

        sh = self.shadow
        m = place(L.w, L.h, self.pad, self.pad)
        a = cv2.warpAffine(sh, m, fr.size, flags=cv2.INTER_LINEAR)
        canvas *= (1.0 - 0.65 * a)[..., None]

        win = self._window(f).astype(np.float32)
        m = place(L.w, L.h, 0, 0)
        w_px = cv2.warpAffine(win, m, fr.size, flags=cv2.INTER_LINEAR)
        w_a = cv2.warpAffine(self.mask, m, fr.size, flags=cv2.INTER_LINEAR)[..., None]
        canvas = canvas * (1.0 - w_a) + w_px * w_a
        return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))

    def __getattr__(self, name):
        return getattr(self.inner, name)
