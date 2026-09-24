"""Overlays composited on top of a finished shot — the subscribe sting.

Everything else in this package *is* a shot. This is the one thing that has to
sit **over** whatever the picture is doing, because the end-screen ask belongs
on the outro footage rather than replacing it.

**Black background, not green.** The obvious asset for this is a green-screen
subscribe animation, and the library is full of them. A black-background one is
strictly better for these two channels and it is worth being explicit about why:

* A screen blend over a dark palette is *exact*. `out = 1-(1-a)(1-b)` leaves
  pure black completely transparent with no threshold to tune, no spill
  suppression, and no edge fringing — the three things that make keyed footage
  look cheap.
* Chroma keying a hard green against gold-on-near-black also tints every
  antialiased edge green, and at 1080p on a button with a drop shadow that is
  plainly visible.

The cost is that a screen blend cannot darken, so a black-background asset can
only ever *add* light. For a glowing button on black that is exactly right.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from ..core.frame import LANDSCAPE, Frame


class ClipOverlay:
    """A clip screen-blended over the picture between `start` and `end`.

    `scale` and `at` place it; `at=None` centres it. `fade` is the ramp at each
    end, so the sting arrives and leaves rather than snapping.

    `crop` is fractional `(left, top, right, bottom)` on the source. Stock
    stings are frequently laid out as a strip with divider bars between
    states, and those bars screen-blend into the frame as bright vertical
    lines that look like a rendering fault. Crop to the artwork.
    """

    def __init__(self, path: Path, start: float, end: float,
                 frame: Frame = LANDSCAPE, scale: float = 1.0,
                 at: tuple[int, int] | None = None, fade: float = 0.45,
                 gain: float = 1.0,
                 crop: tuple[float, float, float, float] | None = None,
                 fps: int = 30):
        self.start, self.end, self.fade, self.gain = start, end, fade, gain
        self.frame = frame

        cap = cv2.VideoCapture(str(path))
        if not cap.isOpened():
            raise ValueError(f"cannot open overlay clip {path}")
        src_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

        want = max(end - start, 1e-3)
        n_out = max(1, int(round(want * fps)))
        src_n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        # Play it at natural speed and hold the last frame if the window is
        # longer than the clip. A subscribe animation that loops looks like a
        # stutter; one that finishes and rests looks finished.
        last = min(src_n - 1, int(round(want * src_fps)) - 1) if src_n else 0
        wanted = np.linspace(0, max(last, 0), n_out).astype(int)

        # `scale` is a fraction of frame *width*; the height follows the crop's
        # own aspect. Forcing 16:9 was the first version and it stretched a
        # 3.6:1 button strip into a smear.
        w = int(frame.w * scale)
        h = None
        keep, idx, cursor = [], 0, 0
        while idx < src_n and cursor < len(wanted):
            ok, bgr = cap.read()
            if not ok:
                break
            while cursor < len(wanted) and wanted[cursor] == idx:
                # Crop into a new name: reassigning `bgr` here double-crops
                # whenever one source frame is sampled twice, which happens
                # any time the overlay window is longer than the clip.
                src = bgr
                if crop:
                    sh, sw = src.shape[:2]
                    l, t0, r, b = crop
                    src = src[int(t0 * sh):int(b * sh), int(l * sw):int(r * sw)]
                if h is None:
                    h = max(1, int(w * src.shape[0] / src.shape[1]))
                small = cv2.resize(src, (w, h), interpolation=cv2.INTER_AREA)
                keep.append(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
                cursor += 1
            idx += 1
        cap.release()
        if not keep:
            raise ValueError(f"decoded no frames from {path}")
        while len(keep) < n_out:
            keep.append(keep[-1])
        self.frames = keep

        h = h or int(frame.h * scale)
        if at is None:
            at = ((frame.w - w) // 2, (frame.h - h) // 2)
        self.at = at
        self.size = (w, h)

    def draw(self, img: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return img
        p = (t - self.start) / max(self.end - self.start, 1e-6)
        i = min(len(self.frames) - 1,
                max(0, int(round(p * (len(self.frames) - 1)))))

        a = min((t - self.start) / self.fade,
                (self.end - t) / self.fade, 1.0)
        if a <= 0.004:
            return img
        alpha = float(a) * self.gain

        x, y = self.at
        w, h = self.size
        base = np.asarray(img).astype(np.float32)
        over = self.frames[i].astype(np.float32) * alpha

        region = base[y:y + h, x:x + w]
        # Screen: black in the overlay leaves the base untouched, and anything
        # bright adds without ever clipping past white.
        blended = 255.0 - (255.0 - region) * (255.0 - over) / 255.0
        base[y:y + h, x:x + w] = blended
        return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))


class ImageOverlay:
    """A still image laid **over** the picture for a window, as a panel.

    Built for the proof-of-stake short, where the user's note was that the
    opening shot has empty space above the footage and the site's own
    architecture diagram should sit in it. Everything else in this format
    either *is* the shot or replaces it; this is the one way to have a diagram
    and moving footage at the same time, which is what a vertical frame has the
    room for and a landscape one does not.

    **Composited opaque, not screen-blended**, which is the opposite of
    `ClipOverlay`'s choice and for a good reason. A screen blend leaves pure
    black transparent, which is perfect for a glowing button on black — but a
    diagram's background is a dark *grey*, not black, so screen-blending one
    lifts the footage underneath it by that grey everywhere the diagram sits
    and prints a visible washed rectangle. An opaque panel with the brand's
    own hairline reads as a deliberate inset instead.

    `at` is the top-left in pixels; `None` centres horizontally and sits the
    panel in the upper third, which is where a 9:16 frame has room. `scale` is
    a fraction of frame width.
    """

    def __init__(self, path: Path, start: float, end: float,
                 frame: Frame = LANDSCAPE, scale: float = 0.92,
                 at: tuple[int, int] | None = None, fade: float = 0.35,
                 rule: bool = True):
        self.start, self.end, self.fade = start, end, fade
        self.frame = frame

        im = Image.open(path).convert("RGB")
        w = int(frame.w * scale)
        h = max(1, int(round(im.height * w / im.width)))
        self.im = im.resize((w, h), Image.LANCZOS)
        if rule:
            d = ImageDraw.Draw(self.im)
            d.rectangle([0, 0, w - 1, h - 1], outline=(229, 194, 0), width=3)
        if at is None:
            at = ((frame.w - w) // 2, int(frame.h * 0.16))
        self.at = at

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return pic
        # Ramp in and out so the panel arrives rather than snapping.
        a = min(1.0, (t - self.start) / self.fade) if self.fade else 1.0
        a = min(a, max(0.0, (self.end - t) / self.fade) if self.fade else 1.0)
        if a <= 0:
            return pic
        if a >= 1.0:
            pic.paste(self.im, self.at)
            return pic
        base = pic.crop((self.at[0], self.at[1],
                         self.at[0] + self.im.width, self.at[1] + self.im.height))
        pic.paste(Image.blend(base, self.im, a), self.at)
        return pic


# --------------------------------------------------------------------------
# The title sequence
# --------------------------------------------------------------------------

FONT_TITLE = "/System/Library/Fonts/SFNS.ttf"     # SF Pro, variable


def _sf(size: int, weight: str = "Bold") -> "ImageFont.FreeTypeFont":
    """SF Pro at a weight. Futura is the caption face; this is the display one.

    The title used to be set in Futura Medium at 96px, centred on a hard scrim
    band. Futura is a light, wide geometric: it is right for a caption sitting
    over footage and weak as a display face, which is most of why that
    treatment read as dated. SF Pro carries a real Heavy, and a heavy grotesque
    left-aligned is the current look on every channel that spends money on
    titles.
    """
    from PIL import ImageFont
    f = ImageFont.truetype(FONT_TITLE, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:                       # a static build, or an old Pillow
        pass
    return f


def _tracked(d: "ImageDraw.ImageDraw", xy: tuple[float, float], text: str,
             font, fill, track: float) -> float:
    """Draw `text` with letter spacing, returning the width it took.

    PIL has no tracking. An eyebrow label set without it is just small type;
    set with it, it reads as a label, which is the whole job of the line.
    """
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + track
    return x - xy[0] - (track if text else 0)


class TitleOverlay:
    """The video's own title, as an animated lower third over the opening shot.

    **This replaces the centred statement the title stamp used to borrow.**
    That treatment is `Shot(payload=)`: a 96px line centred inside a flat black
    band across the middle third of the frame. It is the right device for *a
    statement the footage illustrates* — "This is not financial advice" over
    rain on a window — and the wrong one for a title, for three reasons the
    user named on the noise-canceling cut: the hard-edged band is a rectangle
    of black sitting on top of the picture rather than part of it, centred caps
    in a light geometric is the visual language of a 2012 slideshow, and
    nothing moves, so the one moment the video says what it is has no more
    weight than a caption.

    What this draws instead, and every part of it is doing a job:

    * **A gradient scrim, not a band.** Alpha ramps from nothing at 55% height
      to near-opaque at the bottom edge, so there is no line where the
      treatment starts. Footage stays footage; the type still reads over a
      bright frame.
    * **Bottom-left, not centred.** A left-aligned lower third is where a
      viewer's eye already expects a name to appear, and it leaves the middle
      of the frame — where the footage's own subject is — alone.
    * **An accent bar in the brand's own colour**, growing top to bottom before
      the words arrive. It is the only element that is pure brand, and it is
      what makes the tinnitus cut and the crypto cut read as the same channel
      family without either one borrowing the other's palette.
    * **The lines rise into view behind a mask**, staggered. Each line is drawn
      into a box exactly its own height and slid up into it, so the glyphs are
      cut off by the box's edge on the way in. That is the reveal every motion
      package sells and it costs one `Image.new` per line per frame.
    * **It leaves.** The block fades and drifts up over the last half second
      rather than cutting, so the shot it sits on carries on cleanly.

    Timing is in absolute seconds against the finished timeline, same as every
    other overlay here. `hold` is the whole window including both ramps.
    """

    LEAD = 0.34             # scrim and accent bar, before any type
    STAGGER = 0.10          # between one title line and the next
    RISE = 0.50             # one line's own reveal
    OUT = 0.55              # the exit ramp

    def __init__(self, title: str, start: float, hold: float, brand,
                 frame: Frame = LANDSCAPE, eyebrow: str | None = None,
                 y_frac: float = 0.86, max_lines: int = 3):
        from ..core.draw import wrap

        self.start, self.end = start, start + hold
        self.brand, self.frame = brand, frame
        self.eyebrow = (eyebrow if eyebrow is not None
                        else (brand.site or brand.name)).upper()

        probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        self.margin = int(round(frame.w * 0.072))
        self.bar_w = max(4, int(round(frame.w * 0.0045)))
        self.gap = int(round(frame.w * 0.024))
        col = int(frame.w * (0.60 if frame.w >= frame.h else 0.74))

        # Fit the title: the largest size that still wraps inside `max_lines`.
        # A title is one to six words and almost always fits at the top of the
        # range; the search exists so a long one degrades by getting smaller
        # rather than by running off the frame.
        hi = int(frame.w * 0.058)
        lo = int(frame.w * 0.028)
        size, lines = lo, [title]
        for s in range(hi, lo - 1, -2):
            f = _sf(s, "Bold")
            ls = wrap(probe, title, f, col)
            if len(ls) <= max_lines:
                size, lines = s, ls
                break
        self.size, self.lines = size, lines
        self.font = _sf(size, "Bold")
        self.line_h = int(round(size * 1.16))
        self.eb_font = _sf(max(15, int(round(size * 0.26))), "Semibold")
        self.eb_track = max(1.0, size * 0.045)
        self.eb_h = int(round(size * 0.52))

        block_h = self.line_h * len(lines) + self.eb_h
        self.block_bottom = int(frame.h * y_frac)
        self.block_top = self.block_bottom - block_h
        self.text_x = self.margin + self.bar_w + self.gap
        self.col = col

        # The scrim is one image, built once. Its alpha is scaled per frame.
        top = int(frame.h * 0.45)
        ramp = np.zeros((frame.h, 1), np.float32)
        span = max(1, frame.h - top)
        k = np.linspace(0.0, 1.0, span, dtype=np.float32)
        ramp[top:, 0] = k * k * 210.0
        self.scrim = np.repeat(ramp, frame.w, axis=1)

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return pic
        e = t - self.start
        life = self.end - self.start

        # One global ramp for the exit: everything fades and drifts up
        # together, so the block reads as one object leaving rather than as
        # five elements each ending on their own clock.
        out_p = max(0.0, (e - (life - self.OUT)) / self.OUT)
        a_all = 1.0 - out_p * out_p
        if a_all <= 0.004:
            return pic
        drift = int(round(-18 * out_p * out_p))

        from ..core.draw import ease_out

        base = np.asarray(pic).astype(np.float32)
        s = (self.scrim * a_all)[:, :, None] / 255.0
        base *= (1.0 - s)
        pic = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))

        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)

        # The bar grows downward, and it is first — the brand arrives before
        # the sentence does.
        bp = ease_out(min(1.0, e / self.LEAD))
        if bp > 0.01:
            y0 = self.block_top + drift
            y1 = y0 + int((self.block_bottom - self.block_top) * bp)
            r = self.bar_w / 2
            d.rounded_rectangle([self.margin, y0, self.margin + self.bar_w, y1],
                                radius=r, fill=(*self.brand.primary, 255))

        # The eyebrow slides in from the bar, a beat after it.
        ep = ease_out(max(0.0, min(1.0, (e - 0.18) / 0.42)))
        if ep > 0.01 and self.eyebrow:
            ex = self.text_x - int(round(16 * (1.0 - ep)))
            ey = self.block_top + drift + int(round(self.eb_h * 0.12))
            _tracked(d, (ex, ey), self.eyebrow, self.eb_font,
                     (*self.brand.primary, int(255 * ep)), self.eb_track)

        for i, ln in enumerate(self.lines):
            lp = ease_out(max(0.0, min(1.0, (e - (self.LEAD + i * self.STAGGER))
                                       / self.RISE)))
            if lp <= 0.01:
                continue
            # The slot is exactly one line tall, and the type starts below it.
            # Anything still below the slot's own edge is simply not drawn —
            # which is the mask, without a mask image.
            slot = Image.new("RGBA", (self.col + self.size, self.line_h),
                             (0, 0, 0, 0))
            sd = ImageDraw.Draw(slot)
            off = int(round(self.line_h * 0.92 * (1.0 - lp)))
            sd.text((0, off - int(self.size * 0.06)), ln, font=self.font,
                    fill=(255, 255, 255, 255))
            if lp < 1.0 or a_all < 1.0:
                al = slot.getchannel("A").point(
                    lambda v: int(v * lp * a_all))
                slot.putalpha(al)
            y = self.block_top + self.eb_h + i * self.line_h + drift
            layer.alpha_composite(slot, (self.text_x, y))

        # A soft drop shadow under the whole block, from the block's own alpha.
        sh = layer.getchannel("A").filter(ImageFilter.GaussianBlur(9))
        shadow = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        shadow.putalpha(sh.point(lambda v: int(v * 0.55)))
        out = pic.convert("RGBA")
        out.alpha_composite(shadow, (0, 5))
        out.alpha_composite(layer)
        return out.convert("RGB")


# --------------------------------------------------------------------------
# The first-second hook: a redacted headline
# --------------------------------------------------------------------------

def _ease_out_back(x: float, k: float = 1.9) -> float:
    x = min(max(x, 0.0), 1.0) - 1.0
    return 1.0 + (k + 1.0) * x ** 3 + k * x ** 2


def _ease_out(x: float) -> float:
    x = min(max(x, 0.0), 1.0)
    return 1.0 - (1.0 - x) ** 3


class HookOverlay:
    """The opening hook: a centred headline with its key word **redacted**,
    revealed on the frame the voice says it.

    Every Short on both channels lost 13-27 points at ~5s. A static headline
    (the first version of this class) was rejected as a caption on a frame,
    and the second, top-left version as badly placed. This one is centred on
    the screen and built on three mechanisms, each with its own sound:

    1. **Pattern interrupt, t=0.** The picture punches in (1.14 -> 1.0) and
       the headline slams in with overshoot on `hook_slam`, an 808-style drop.
    2. **Curiosity gap, t=0.3 -> reveal.** The `[bracketed]` word is a bar
       the width of the word, full of animated static in the brand's tones.
       Two or three times the headline *tears* - a horizontal slice glitch for
       a few frames - on a `hook_glitch` blip, and a `hook_swell` (a reverse
       cymbal) sucks up into the reveal. The bar's width is a clue; an open
       question the viewer can almost close is what they wait for.
    3. **The close lands on the cliff.** The bar wipes off on the frame the
       narration says the word (`reveal_at`, from the caption timings), on
       `hook_pop` - a glitch resolving into a two-note chime - with a pop and
       a small shake. Written so the word is spoken at ~3.5-5s, the gap
       closes exactly where the audience used to leave.

    Then it holds `hold` seconds and leaves upward on `hook_swish`.

    **Centred, not corner-anchored.** Every line is centred and the block
    sits on the frame's vertical axis. In 9:16 its centre is at 34% of the
    height: clear of the watermark above, of the platforms' right-hand
    button rail (which starts around 45%) and of the caption line below. In
    16:9 it sits higher (24%) so a centred face stays visible. A soft dark
    band behind it - not a top-down gradient - keeps white type legible on
    any footage.

    Type is the karaoke captions' own - Arial Black, upper case, the brand's
    pill behind the key word - so the hook reads as part of the video's
    system. `cues()` returns the sound cues; the renderer mixes them.
    """

    PUNCH = 0.35      # camera punch-in duration
    SLAM = 0.30       # headline entrance
    WIPE = 0.20       # the bar wiping off
    EXIT = 0.28
    TEAR = 0.10       # one glitch tear

    def __init__(self, text: str, reveal_at: float = 3.0,
                 frame: Frame = LANDSCAPE, start_at: float = 0.0,
                 leave: bool = True,
                 accent: tuple[int, int, int] = (229, 194, 0),
                 ink_on_accent: tuple[int, int, int] = (14, 14, 14),
                 centre_y: float | None = None, max_w: int | None = None,
                 size: int = 92, max_lines: int = 3, hold: float = 0.9,
                 punch: bool = True, upper: bool = True,
                 statement_hold: float = 2.2):
        from PIL import ImageFont
        from ..core.vertical import FONT_KARAOKE_BOX, FONT_KARAOKE_BOX_INDEX

        self.frame, self.punch = frame, punch
        self.reveal_at = max(0.6, reveal_at)
        # **Statement mode: a hook with no `[brackets]` waits for nothing.**
        # The redaction is worth its seconds only when the hidden token cannot
        # be guessed from the rest of the line (`shorts.md`). When it can -
        # every direction word this channel has hidden, `[up]`, `[louder]`,
        # `[worse]` - the viewer fills it in within half a second and then
        # waits for the video to catch up, which is what the user reported on
        # the neck-tension pair. Writing the line without brackets keeps the
        # slam, the band and the type and drops the bar, the static, the tear
        # and the swell: the stake is on frame zero, muted, and the piece
        # moves on.
        self.redacted = "[" in text and "]" in text
        if self.redacted:
            self.exit_at = self.reveal_at + self.WIPE + hold
        else:
            self.exit_at = self.SLAM + statement_hold
        # **`start_at` shifts the whole clock**, which is what lets the same
        # object be an outro as well as an opener: `draw` and `cues` work in
        # the overlay's own time and the renderer's `t` is offset once, here.
        # `leave=False` holds the block to the end instead of sliding it off -
        # a closing statement that exits has the video finishing on an empty
        # frame, which is the opposite of a loop.
        self.start_at, self.leave = start_at, leave
        if not leave:
            self.exit_at = 1e9
        self.start = start_at
        self.end = start_at + (self.exit_at + self.EXIT if leave else 1e9)
        vertical = frame.h > frame.w
        max_w = max_w or (frame.w - 180 if vertical else int(frame.w * 0.62))
        cy = frame.h * (centre_y if centre_y is not None else (0.34 if vertical else 0.24))

        # **One glitch tear, not a train of them.** This used to fire every
        # ~0.8s from 0.7s, so a reveal at 5.3s drew four tears with a blip on
        # each - and with the karaoke line running underneath, the opening
        # seconds had more happening in them than the video did. One tear
        # says the bar is unstable; four say the render is. It lands in the
        # middle of the hidden window, clear of the slam and of the swell.
        mid = (0.7 + max(0.7, self.reveal_at - 1.0)) / 2
        self.glitches = ([round(mid, 2)]
                         if self.redacted and self.reveal_at > 1.7 else [])

        words, acc, run = [], False, 0
        for raw in text.replace("[", " [ ").replace("]", " ] ").split():
            if raw == "[":
                acc = True
                run += 1
            elif raw == "]":
                acc = False
            else:
                words.append((raw.upper() if upper else raw, acc,
                              run if acc else 0))
        self.hidden = [w for w, a, _ in words if a]

        # **A redacted run must land whole on one line.** `[30 seconds]` wrapped
        # across two rows draws as *two* bars, and after the wipe as two
        # separate pills - so the one thing the frame is asking about reads as
        # two things, and the bar's width stops being the clue it is supposed
        # to be. It shipped that way on the neck-tension Short. Same rule the
        # thumbnail layout already enforces on its accent runs (`thumb.py`,
        # `runs_intact`); shrink until it holds, and stop at 56 either way.
        while True:
            font = ImageFont.truetype(FONT_KARAOKE_BOX, size, index=FONT_KARAOKE_BOX_INDEX)
            space = font.getlength(" ")
            lines, cur, cur_w = [], [], 0.0
            runs: dict[int, set] = {}
            for w, a, r in words:
                ww = font.getlength(w)
                if cur and cur_w + space + ww > max_w:
                    lines.append((cur, cur_w))
                    cur, cur_w = [], 0.0
                cur_w += (space if cur else 0) + ww
                cur.append((w, a, ww))
                if r:
                    runs.setdefault(r, set()).add(len(lines))
            if cur:
                lines.append((cur, cur_w))
            whole = all(len(v) == 1 for v in runs.values())
            if (len(lines) <= max_lines and whole) or size <= 56:
                break
            size -= 6

        pad_x, pad_y = max(10, size // 7), max(4, size // 14)
        lh = int(size * 1.22)
        stroke = max(4, size // 14)
        inner_w = int(max(w for _, w in lines))
        block_w = inner_w + pad_x * 2 + stroke * 2 + 16
        block_h = lh * len(lines) + pad_y * 2 + stroke * 2 + 8
        oy = pad_y + stroke + 4

        base = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))
        words_l = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))
        bars_l = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))
        reveal_l = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))
        dw, db, dr = (ImageDraw.Draw(words_l), ImageDraw.Draw(bars_l),
                      ImageDraw.Draw(reveal_l))
        self.bars: list[tuple[int, int, int, int]] = []
        asc = font.getbbox("A")[1]
        cap_h = font.getbbox("A")[3] - asc
        radius = max(8, size // 7)
        y = oy
        for ln, ln_w in lines:
            x = (block_w - ln_w) / 2          # centred line
            for w, a, ww in ln:
                if a:
                    box = (int(x - pad_x), int(y + asc - pad_y * 2),
                           int(x + ww + pad_x), int(y + asc + cap_h + pad_y * 2))
                    self.bars.append(box)
                    db.rounded_rectangle(box, radius=radius, fill=accent + (255,))
                    dr.rounded_rectangle(box, radius=radius, fill=accent + (255,))
                    dr.text((x, y), w, font=font, fill=ink_on_accent + (255,))
                else:
                    dw.text((x, y), w, font=font, fill=(255, 255, 255, 255),
                            stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
                x += ww + space
            y += lh

        shadow_src = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))
        shadow_src.alpha_composite(words_l)
        shadow_src.alpha_composite(bars_l)
        sh = shadow_src.split()[3].filter(ImageFilter.GaussianBlur(9))
        shadow = Image.new("RGBA", (block_w, block_h), (0, 0, 0, 0))
        shadow.putalpha(sh.point(lambda v: int(v * 0.65)))
        base.alpha_composite(shadow, (0, 5))
        base.alpha_composite(words_l)
        self.base, self.bars_l, self.reveal_l = base, bars_l, reveal_l
        self.block_w, self.block_h = block_w, block_h
        self.accent = accent
        self.left = (frame.w - block_w) // 2
        self.top = int(cy - block_h / 2)

        # A soft dark band behind the block, full width, fading out above and
        # below - legibility without a panel and without darkening the frame.
        spread = 150
        band_h = block_h + spread * 2
        yy = np.linspace(-1.0, 1.0, band_h)
        core = block_h / band_h
        a = np.clip((1 - np.abs(yy)) / max(1e-6, 1 - core), 0, 1) ** 1.3 * 125
        self.band = Image.new("RGBA", (frame.w, band_h), (0, 0, 0, 255))
        self.band.putalpha(Image.fromarray(np.repeat(a.astype(np.uint8)[:, None], frame.w, 1), "L"))
        self.band_top = self.top - spread

    def cues(self) -> list[tuple[float, str]]:
        return [(self.start_at + t, n) for t, n in self._cues()]

    def _cues(self) -> list[tuple[float, str]]:
        # Statement mode has nothing to resolve, so it carries the two cues
        # that mark the block arriving and leaving - no pop, no swell, no
        # blip. Five effects in three seconds is a sound-effects reel.
        if not self.redacted:
            out = [(0.0, "hook_slam")]
            if self.leave:
                out.append((self.exit_at, "hook_swish"))
            return out
        r = self.reveal_at
        out = [(0.0, "hook_slam"), (r, "hook_pop")]
        if self.leave:
            out.append((self.exit_at, "hook_swish"))
        out += [(g, "hook_glitch") for g in self.glitches]
        if r - 1.0 > 0.35:
            out.append((r - 1.0, "hook_swell"))
        return out

    def _block(self, t: float) -> Image.Image:
        blk = self.base.copy()
        r = self.reveal_at
        if t < r:
            # Censored, not empty: animated static in the brand's tones inside
            # each bar (re-rolled every other frame), a light sweep across it,
            # and a slow breathing pulse.
            bars = self.bars_l.copy()
            rng = np.random.default_rng(int(t * 15))
            acc = np.array(self.accent, dtype=np.float32)
            pulse = 0.85 + 0.15 * np.sin(t * 2 * np.pi / 1.3)
            arr = np.asarray(bars).copy()
            phase = (t % 1.1) / 1.1
            for x0, y0, x1, y1 in self.bars:
                h, w = y1 - y0, x1 - x0
                n = rng.random((h // 3 + 1, w // 3 + 1)).repeat(3, 0).repeat(3, 1)[:h, :w]
                tone = acc * (0.45 + 0.55 * n[..., None]) * pulse
                xs = np.arange(w)[None, :]
                ys = np.arange(h)[:, None]
                cx = -w * 0.4 + phase * w * 1.8
                band = np.clip(1 - np.abs((xs - cx) + (ys - h / 2) * 0.6) / 26, 0, 1)
                tone = tone + band[..., None] * 90
                region = arr[y0:y1, x0:x1]
                mask = region[..., 3:4] > 0
                region[..., :3] = np.where(mask, np.clip(tone, 0, 255), region[..., :3])
                arr[y0:y1, x0:x1] = region
            blk.alpha_composite(Image.fromarray(arr, "RGBA"))
        else:
            p = _ease_out((t - r) / self.WIPE)
            blk.alpha_composite(self.bars_l)
            if p >= 1.0:
                blk.alpha_composite(self.reveal_l)
            else:
                mask = Image.new("L", (self.block_w, self.block_h), 0)
                md = ImageDraw.Draw(mask)
                for x0, y0, x1, y1 in self.bars:
                    md.rectangle((x0, y0, x0 + (x1 - x0) * p, y1), fill=255)
                rv = self.reveal_l.copy()
                rv.putalpha(Image.fromarray(np.minimum(np.asarray(rv.split()[3]), np.asarray(mask))))
                blk.alpha_composite(rv)

        # A glitch tear: slices of the block jump sideways for a few frames,
        # with an RGB split, on the same tick as the `hook_glitch` blip.
        for g in self.glitches:
            if g <= t < g + self.TEAR:
                rng = np.random.default_rng(int(g * 100) + int((t - g) * 60))
                arr = np.asarray(blk).copy()
                h = arr.shape[0]
                for _ in range(3):
                    y0 = int(rng.integers(0, max(1, h - 12)))
                    y1 = min(h, y0 + int(rng.integers(8, max(9, h // 4))))
                    arr[y0:y1] = np.roll(arr[y0:y1], int(rng.integers(-26, 27)), axis=1)
                split = np.roll(arr[..., 0], 6, axis=1)
                arr[..., 0] = np.maximum(arr[..., 0], split)
                blk = Image.fromarray(arr, "RGBA")
                break
        return blk

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return pic
        t -= self.start_at          # overlay-local time from here down
        W, H = self.frame.w, self.frame.h

        if self.punch and t < self.PUNCH:
            z = 1.14 - 0.14 * _ease_out(t / self.PUNCH)
            cw, ch = int(W / z), int(H / z)
            pic = pic.crop(((W - cw) // 2, (H - ch) // 2,
                            (W - cw) // 2 + cw, (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)

        out = pic.convert("RGBA")

        a, dy = 1.0, 0
        if t >= self.exit_at:
            q = _ease_out((t - self.exit_at) / self.EXIT)
            a, dy = 1.0 - q, -int(70 * q)

        band = self.band
        if a < 1.0:
            band = band.copy()
            band.putalpha(band.split()[3].point(lambda v: int(v * a)))
        out.alpha_composite(band, (0, max(0, self.band_top + dy)))

        blk = self._block(t)
        s = 1.0
        if t < self.SLAM:
            s = 1.12 - 0.12 * _ease_out_back(t / self.SLAM)
        r = self.reveal_at + self.WIPE
        if self.redacted and r <= t < r + 0.22:
            s *= 1.0 + 0.05 * (1 - (t - r) / 0.22)
        if abs(s - 1.0) > 1e-3:
            nw, nh = int(self.block_w * s), int(self.block_h * s)
            blk = blk.resize((nw, nh), Image.BILINEAR)
        else:
            nw, nh = self.block_w, self.block_h
        jx = jy = 0
        if self.redacted and self.reveal_at <= t < self.reveal_at + 0.25:
            k = 1 - (t - self.reveal_at) / 0.25
            jx = int(round(7 * k * np.sin(t * 90)))
            jy = int(round(5 * k * np.cos(t * 70)))
        if a < 1.0:
            blk.putalpha(blk.split()[3].point(lambda v: int(v * a)))
        x = (W - nw) // 2 + jx
        y = self.top + (self.block_h - nh) // 2 + dy + jy
        out.alpha_composite(blk, (max(0, x), max(0, y)))
        return out.convert("RGB")
