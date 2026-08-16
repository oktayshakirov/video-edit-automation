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

from ..core.draw import cover as _cover
from ..core.draw import ease_out as _ease_out
from ..core.draw import mark as _mark
from ..core.draw import partial as _partial
from ..core.draw import subpixel as _subpixel
from ..core.frame import VERTICAL, Frame
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

# thecrypto.wiki's palette, from the site's `config/theme.json`.
GOLD = (229, 194, 0)            # #e5c200 — primary and border
BODY = (23, 23, 23)             # #171717
PANEL = (47, 47, 47)            # #2f2f2f

SITE_IMAGES = Path.home() / "Coding/crypto-wiki/public/images"
LOGO = SITE_IMAGES / "logo.png"

# Everything below takes a `frame` and defaults to VERTICAL, so the shipped
# shorts are untouched while the same code can render 16:9 for long form. The
# safe box, the caption floor and the watermark placement all live on the frame
# — they are properties of the platform the piece is going to, not of this
# module, and hardcoding the vertical ones here is what made them look like
# constants of the format.

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
    picture: Path | None = None         # photo *beside* one, in the landscape
                                        # split layout — see longform/beats.py
    clip: Path | None = None            # a video file — see longform/clip.py
    clip_at: float = 0.0                # seconds to skip into that clip
    reveals: list[float] | None = None  # absolute times, one per checklist item
    marks: list[float] | None = None    # when each item's verdict lands
    zoom: float = 1.12                  # Ken Burns travel over the whole shot
    pan: tuple[float, float] = (0.0, 0.0)
    aspect: float = 1.15                # target crop shape, w:h
    bias: float = 0.5                   # vertical crop position, 0 top 1 bottom
    start: float = 0.0
    hold: float = 0.0
    xfade: float | None = None          # override the transition length out of
                                        # this shot; 0.0 cuts.
    transition: str | None = None       # "dissolve" | "push". See `render_shots`.


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


class PhotoShot:
    """A prepared image shot. Layers are built once; frames are cheap crops."""

    # How much clear air the photo's gold hairline leaves under the watermark
    # when it has to dodge it. Small on purpose: this is a nudge, not a layout.
    LOGO_CLEAR = 16

    def __init__(self, path: Path, zoom: float, pan: tuple[float, float],
                 aspect: float = 1.15, bias: float = 0.5,
                 frame: Frame = VERTICAL,
                 logo_box: tuple[int, int, int, int] | None = None):
        src = Image.open(path).convert("RGB")
        self.zoom, self.pan = zoom, pan
        self.frame = frame
        # Per-frame, not per-class: the ceiling is about how large the frame is
        # actually drawn on a phone, and 16:9 is drawn at roughly half the
        # linear size of 9:16. See `core/frame.py`.
        self.MAX_UPSCALE = frame.max_upscale

        # Backdrop: cover the frame with headroom for the move, then blur hard
        # enough that the upscale is invisible. The blur radius scales with the
        # upscale factor, because a 400px source stretched to 1080 needs far
        # more hiding than a 1200px one.
        pad = int(200 * zoom)
        up = max(1.0, (frame.w + pad) / src.width)
        back = _cover(src, frame.w + pad, frame.h + pad)
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
        #
        # **In a landscape frame this pressure mostly disappears**, and `aspect`
        # wants to be near `frame.aspect` (1.78) rather than the vertical 1.15 —
        # cropping a landscape source *taller* than the frame it is going into
        # would reintroduce the very blur band the crop exists to remove.
        crop_w = min(src.width, src.height * aspect)
        crop_w = min(src.width, max(crop_w, frame.w / self.MAX_UPSCALE))
        crop_h = min(src.height, crop_w / aspect)
        left = (src.width - crop_w) / 2
        top = (src.height - crop_h) * bias
        crop = src.crop((int(left), int(top),
                         int(left + crop_w), int(top + crop_h)))

        target_w = min(int(frame.w * zoom), int(crop.width * self.MAX_UPSCALE))
        self.sharp = crop.resize(
            (target_w, max(1, int(crop.height * target_w / crop.width))),
            Image.LANCZOS)

        self.dy = self._dodge(logo_box, frame)
        # After the dodge, which may have resized it. `draw` warps this array
        # directly rather than resizing a PIL image per frame.
        self.sharp_px = np.ascontiguousarray(np.asarray(self.sharp))

    def _dodge(self, logo_box, frame: Frame) -> float:
        """How far to push the whole shot down to clear the watermark.

        **A photograph that does not fill the frame carries a gold hairline
        along its top edge, and that line ran straight under the wordmark** —
        two graphics crossing, which reads as a mistake rather than as framing.
        A photo big enough to bleed off the top has no line up there at all, so
        it needs nothing: that is the "leave the full screen as it is" half of
        the rule.

        Two things this deliberately does *not* do:

        * **It is a constant offset, not a per-frame clamp.** `y` travels across
          the shot, so clamping each frame would hold the picture still against
          the floor and then release it — a stutter in the middle of a Ken Burns
          move. The offset is computed from the extreme of the travel and the
          motion is preserved exactly.
        * **It only fires when the photo actually reaches the mark**, in both
          axes. A shot whose top edge is already below the wordmark, or whose
          picture sits to the right of it, is left byte-for-byte alone — which
          is what keeps the shipped vertical shorts reproducible, since a 9:16
          frame puts its mark at y=268 and its photograph 200px below that.

        **A photo too tall to fit under the mark is shrunk, not shoved.** A pure
        translation, on a picture that already reached within 60px of the frame
        edge, pushes its lower edge off screen — so the bottom hairline vanishes
        part-way through the shot, which is a second artifact traded for the
        first. Scaling into the band that is actually available keeps both edges
        drawn for the whole shot, and it costs a few percent of size on what is
        a downscale of the source either way.
        """
        if logo_box is None:
            return 0.0
        lx, ly, lw, lh = logo_box
        floor = ly + lh + self.LOGO_CLEAR

        def extremes():
            # x, y and h all travel with `f`, and not necessarily together, so
            # sample rather than assuming the extreme sits at an endpoint.
            boxes = [self._place(i / 10) for i in range(11)]
            return (min(y for _, y, _, _ in boxes),
                    max(y + h for _, y, _, h in boxes),
                    min(x for x, _, _, _ in boxes),
                    max(x + w for x, _, w, _ in boxes),
                    max(h for _, _, _, h in boxes))

        top, bottom, left, right, tall = extremes()
        if top <= 0 or top >= floor:        # bleeds off the top, or already clear
            return 0.0
        if right <= lx or left >= lx + lw:  # the mark is not over the picture
            return 0.0

        # Less the hairline's own width: a bottom edge landing exactly on
        # `frame.h` fails the `edge < fr.h` test and the line is not drawn at
        # all, which is the artifact this branch exists to prevent.
        band = frame.h - floor - 3
        if tall > band:
            k = band / tall
            self.sharp = self.sharp.resize(
                (max(1, int(self.sharp.width * k)),
                 max(1, int(self.sharp.height * k))), Image.LANCZOS)
            top, bottom, left, right, tall = extremes()

        # Never trade the bottom edge for the top one: if a shot still cannot
        # fit, take the largest push that keeps the lower hairline on screen.
        return max(0.0, min(floor - top, frame.h - bottom))

    def _place(self, f: float) -> tuple[float, float, float, float]:
        """The photograph's box at `f`, before the watermark dodge."""
        k = 1.0 + (self.zoom - 1.0) * f
        w = self.sharp.width / self.zoom * k
        h = self.sharp.height / self.zoom * k
        x = (self.frame.w - w) / 2 + self.pan[0] * (f - 0.5) * self.frame.w
        y = (self.frame.h - h) / 2 + self.pan[1] * (f - 0.5) * self.frame.h
        return x, y, w, h

    def photo_box(self, f: float = 0.5) -> tuple[float, float, float, float]:
        """Where the sharp photograph sits at `f`. Captions key off this."""
        x, y, w, h = self._place(f)
        return x, y + self.dy, w, h

    def draw(self, f: float) -> Image.Image:
        """`f` runs 0..1 across the shot.

        **The sharp layer's scale and translation are one float affine.** They
        used to be three separate integer steps — `int()` on the width, `int()`
        on the height, `round()` on the paste — and the two axes therefore
        crossed their rounding boundaries on *different frames*. The picture
        grew a pixel taller on one frame and a pixel wider three frames later,
        which is visible as a stutter and reads as the image lagging its own
        move. It is the same fault the video path had, and it has the same fix:
        `warpAffine` does the scale and the offset together, at subpixel
        precision, so both edges move continuously and in step.

        It was latent for as long as the photographs bled off the frame — an
        edge you cannot see cannot be seen to jump. Bringing both edges inside
        the frame, so the hairline clears the watermark, is what exposed it.
        """
        # Backdrop drifts one way, sharp layer the other. Opposed moves at
        # different rates is what makes a still photograph read as a shot.
        fr = self.frame
        bx = (self.back.shape[1] - fr.w) * (0.5 + 0.42 * (f - 0.5))
        by = (self.back.shape[0] - fr.h) * (0.5 - 0.42 * (f - 0.5))
        canvas = np.ascontiguousarray(_subpixel(self.back, bx, by, fr.w, fr.h))

        # The sharp copy zooms slightly and slides along `pan`, in floats.
        x, y, w, h = self.photo_box(f)
        s = w / self.sharp_px.shape[1]
        m = np.float32([[s, 0.0, x], [0.0, s, y]])
        # BORDER_TRANSPARENT leaves the backdrop untouched outside the photo,
        # so this composites in one pass with no mask and no integer paste.
        cv2.warpAffine(self.sharp_px, m, fr.size, dst=canvas,
                       flags=cv2.INTER_LANCZOS4,
                       borderMode=cv2.BORDER_TRANSPARENT)

        # A hairline in the site's gold along the photo's edges, which reads as
        # deliberate framing rather than as an image that failed to fill.
        # Drawn with `shift`, which is cv2's fixed-point subpixel form: a line
        # snapped to whole pixels under a picture that is not would reintroduce
        # exactly the judder the warp just removed.
        SH, u = 4, 16.0
        for edge in (y, y + h):
            if 0 < edge < fr.h:
                # Only across the photograph, not the whole frame. Drawn full
                # width it read as a band the picture was supposed to fill, which
                # made a narrow source look like a rendering bug.
                cv2.line(canvas,
                         (int(round(x * u)), int(round(edge * u))),
                         (int(round((x + w) * u)), int(round(edge * u))),
                         GOLD, 3, lineType=cv2.LINE_AA, shift=SH)
        return Image.fromarray(canvas)



# --- the drawn beat ------------------------------------------------------

class ChecklistShot:
    """A list that fills in on the voice, then gets judged.

    The one beat that is drawn rather than photographed, and the reason the
    format is not stock-footage-with-narration: it shows the argument instead of
    illustrating it.

    **Two phases, and the split is what makes it play rather than just read.**
    Items appear as plain white options on `reveals` — absolute times taken from
    the caption spans, so a line appears exactly as it is spoken. Nothing is
    marked yet, so for those few seconds the list is a genuine open question.
    Then, in the pause after the last option, the verdicts land one at a time on
    `marks`: cross, cross, cross, tick. Marking each item as it arrived answered
    the question before it had been asked, and the beat had no payoff.

    Both the strike-through and the marks *draw on* over ~0.16s rather than
    appearing whole. At this size an instant strike reads as a rendering glitch;
    a line that travels reads as something being crossed out.

    It draws over a photograph, dimmed and blurred, rather than over flat black.
    A flat panel for six seconds in the middle of a photo-driven piece reads as
    the video having stopped, and it left the frame mostly empty.
    """

    DRAW = 0.16                 # how long a mark or a strike takes to draw on
    POP = 0.14                  # an item's entrance

    def __init__(self, items: list[tuple[str, bool]], title: str = "",
                 flow: bool = False,
                 backdrop: Path | None = None,
                 reveals: list[float] | None = None,
                 marks: list[float] | None = None,
                 start: float = 0.0, hold: float = 1.0,
                 font_path: str = FONT_CAPTION,
                 font_index: int = FONT_CAPTION_INDEX,
                 frame: Frame = VERTICAL):
        self.items = items
        self.title = title
        # `flow` changes nothing here — the drawing only ever reads `marks`.
        # It is accepted so it can travel as the payload's third element, and
        # `build.py` turns it into a `marks` list that lands each verdict just
        # after the word that earns it instead of all of them in a later pause.
        # Use it when the narration says the verdict itself ("Not the graphics
        # cards"), and leave it off when the narration only asks.
        self.flow = flow
        self.reveals = reveals
        self.marks = marks
        self.start, self.hold = start, hold
        self.frame = frame
        self.font = ImageFont.truetype(font_path, 54, index=font_index)
        self.title_font = ImageFont.truetype(font_path, 40, index=font_index)

        self.back = None
        if backdrop is not None and Path(backdrop).exists():
            im = _cover(Image.open(backdrop).convert("RGB"), frame.w, frame.h)
            im = im.filter(ImageFilter.GaussianBlur(30))
            # 0.30 was measured against the real frame and came out barely
            # distinguishable from flat black, which was the thing this backdrop
            # exists to avoid. The white type carries a 3px stroke, so it can
            # afford a backdrop with something visible in it.
            self.back = (np.asarray(im) * 0.5).astype(np.uint8)

    def draw(self, f: float) -> Image.Image:
        fr = self.frame
        if self.back is not None:
            out = Image.fromarray(self.back.copy())
        else:
            out = Image.new("RGB", fr.size, BODY)
        d = ImageDraw.Draw(out)

        # A faint gold grid, drifting, so the beat still has motion in it.
        step, off = 96, int((f * 40) % 96)
        for gx in range(-96 + off, fr.w + 96, step):
            d.line([(gx, 0), (gx, fr.h)], fill=(40, 38, 26), width=2)
        for gy in range(-96 + off, fr.h + 96, step):
            d.line([(0, gy), (fr.w, gy)], fill=(40, 38, 26), width=2)

        n = len(self.items)
        top = fr.h // 2 - (n * 124) // 2
        if self.title:
            d.text((110, top - 104), self.title, font=self.title_font, fill=GOLD)

        t = self.start + f * self.hold
        for i, (text, ok) in enumerate(self.items):
            due = (self.reveals[i] if self.reveals
                   else self.start + self.hold * (i / n) * 0.85)
            if t < due:
                continue
            y = top + i * 124

            # The item's own entrance: it slides up the last few pixels as it
            # arrives, which ties it to the syllable that named it.
            e = _ease_out(min(1.0, (t - due) / self.POP))
            y_in = y + int(round(14 * (1.0 - e)))

            # White for every item, struck or not. Grey-on-dark was measured
            # against the real frame and was not readable on a phone — the
            # strike-through already says "this one does not count", so the ink
            # does not have to say it a second time by being harder to read.
            d.text((200, y_in), text, font=self.font, fill=(255, 255, 255),
                   stroke_width=3, stroke_fill=(0, 0, 0))

            # Phase two. Until its verdict is due the item is just an option,
            # with the gutter left empty so the reveal has somewhere to land.
            due_mark = (self.marks[i] if self.marks else due)
            if t < due_mark:
                continue
            m = _ease_out(min(1.0, (t - due_mark) / self.DRAW))
            colour = GOLD if ok else (196, 84, 84)
            _mark(d, 110, y + 16, 44, ok, colour, progress=m)
            if not ok:
                bbox = d.textbbox((200, y), text, font=self.font)
                mid = (bbox[1] + bbox[3]) // 2
                # Drawn from the left, arriving a touch after the cross, so the
                # eye reads mark-then-strike rather than both at once.
                s = _ease_out(min(1.0, (t - due_mark - 0.05) / self.DRAW))
                if s > 0:
                    d.line([(200, mid), (200 + (bbox[2] - 200) * s, mid)],
                           fill=(230, 96, 96), width=5)
        return out





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


# --- captions ------------------------------------------------------------

CAP_IN, CAP_OUT = 0.13, 0.10    # entrance and exit, in seconds


@dataclass
class CaptionSprite:
    """One caption, cropped to its ink and animated onto the frame.

    Captions used to be burned by ffmpeg as full-frame PNG overlays gated with
    `enable='between(t,..)'`, which is a hard on and a hard off. Against a voice
    that is a real sentence contour, type that snaps on and snaps off is the one
    part of the piece that still reads as generated — the eye catches the
    discontinuity even when the timing is exactly right.

    Compositing here instead costs nothing (every frame is already being drawn
    in Python) and buys a per-frame entrance: the line fades up over `CAP_IN`
    while rising the last few pixels and settling from 94% with a slight
    overshoot. The overshoot is the whole trick — a linear scale-in reads as a
    zoom, a scale-in that passes its mark and comes back reads as something
    being *placed*.

    It also cross-dissolves into the next caption instead of cutting, which is
    what stops a four-caption sentence looking like four separate cards.
    """
    img: Image.Image            # cropped to the ink
    at: tuple[int, int]         # where that crop sat in the full frame
    start: float
    end: float

    def draw(self, frame: Image.Image, t: float) -> None:
        if not (self.start - 0.001 <= t < self.end):
            return
        p = _ease_out((t - self.start) / CAP_IN)
        left = self.end - t
        alpha = min(p, 1.0 if left > CAP_OUT else max(0.0, left / CAP_OUT))
        if alpha <= 0.004:
            return

        # 0.94 -> 1.0 with a ~1.5% overshoot on the way.
        scale = 0.94 + 0.06 * p + 0.022 * math.sin(math.pi * p)
        rise = 12.0 * (1.0 - p)

        w = max(1, int(round(self.img.width * scale)))
        h = max(1, int(round(self.img.height * scale)))
        im = self.img if (w, h) == self.img.size else \
            self.img.resize((w, h), Image.LANCZOS)
        if alpha < 0.999:
            im = im.copy()
            im.putalpha(im.split()[-1].point(lambda v: int(v * alpha)))

        # Scale about the block's own centre, so the line grows in place rather
        # than out of its top-left corner.
        x = self.at[0] + (self.img.width - w) // 2
        y = self.at[1] + (self.img.height - h) // 2 + int(round(rise))
        frame.alpha_composite(im, (x, y))


def caption_sprite(png: Path, start: float, end: float) -> CaptionSprite | None:
    """Crop a rendered caption PNG down to its ink."""
    im = Image.open(png).convert("RGBA")
    box = im.getbbox()
    if box is None:
        return None
    # A couple of pixels of margin, so LANCZOS at 94% has something to sample
    # at the edges instead of hard-cutting the stroke.
    pad = 3
    box = (max(0, box[0] - pad), max(0, box[1] - pad),
           min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    return CaptionSprite(im.crop(box), (box[0], box[1]), start, end)


# --- assembly ------------------------------------------------------------

def render_shots(out: Path, shots: list[Shot], total: float, fps: int = 30,
                 captions: list[CaptionSprite] | None = None,
                 logo_at: tuple[int, int] | None = None,
                 logo_w: int | None = None,
                 logo_float: float = 8.0, logo_period: float = 6.5,
                 frame: Frame = VERTICAL, transition: str = "dissolve",
                 xfade: float = XFADE,
                 factory=None, mark: "Image.Image | None" = None,
                 overlays=None) -> Path:
    """Render the picture track: every shot, crossfaded, captions, watermark.

    `logo_at` and `logo_w` default to the frame's own values rather than to the
    vertical ones, because a 300px mark is 27.8% of a 1080-wide frame and 15.6%
    of a 1920-wide one — the same number is a different object in each.

    `factory` builds the prepared object for a drawn shot, given `(shot, frame)`,
    and anything it returns needs only a `draw(f)` method. It defaults to this
    module's own checklist. That indirection is what lets the long-form
    vocabulary — chapter cards, comparisons, stats, quotes — extend this engine
    without it having to know they exist, and without a second copy of the
    crossfade, caption and watermark loop that all of them need.

    `mark` overrides the watermark image, for the sites whose mark is a lockup
    built at render time rather than a file on disk.

    `transition` is the default shot-to-shot move. **"dissolve" here is not a
    preference, it is the shipped vertical behaviour** — the shorts are
    byte-reproducible and must stay that way, so long form opts into "push"
    rather than the default changing under them.
    """
    logo_at = frame.logo_at if logo_at is None else logo_at
    logo_w = frame.logo_w if logo_w is None else logo_w

    if mark is None:
        mark = logo_mark(logo_w)
    # The box the watermark occupies, float included, so a photograph's hairline
    # can dodge it. Resolved from the mark itself rather than assumed: the two
    # sites' marks differ by a factor of four in height at the same width.
    logo_box = (None if mark is None else
                (logo_at[0], int(logo_at[1] - logo_float),
                 mark.width, int(mark.height + 2 * logo_float)))

    prepared = []
    for s in shots:
        if s.image is not None:
            prepared.append(PhotoShot(s.image, s.zoom, s.pan, s.aspect, s.bias,
                                      frame=frame, logo_box=logo_box))
        elif factory is not None:
            prepared.append(factory(s, frame))
        else:
            prepared.append(ChecklistShot(*s.payload, backdrop=s.backdrop,
                                          reveals=s.reveals, marks=s.marks,
                                          start=s.start, hold=s.hold,
                                          frame=frame))

    if mark is not None:
        frame.check_top(logo_at[1] - logo_float, f"logo_at={logo_at}")

    n = int(round(total * fps)) + fps // 2
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{frame.w}x{frame.h}", "-r", str(fps), "-i", "-",
         "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)

    for i in range(n):
        t = i / fps
        idx = max(0, min(len(shots) - 1,
                         next((k for k, s in enumerate(shots)
                               if t < s.start + s.hold), len(shots) - 1)))
        s = shots[idx]
        f = 0.0 if s.hold <= 0 else min(1.0, max(0.0, (t - s.start) / s.hold))
        pic = prepared[idx].draw(f)

        # Crossfade into the next shot over its final XFADE seconds. Dissolves
        # rather than cuts: the piece is one continuous argument, and a hard cut
        # every five seconds fights the voice instead of following it.
        #
        # `s.xfade` overrides it, and 0.0 cuts. That exists because the rule
        # above is a rule about *photographs*. Dissolving one drawn beat into
        # another cross-fades two sets of type through each other, which does
        # not read as a transition at all — it reads as a rendering fault. Long
        # form sets it to 0 between drawn beats; see `longform/plan.py`.
        xf = xfade if s.xfade is None else s.xfade
        left = s.start + s.hold - t
        if idx + 1 < len(shots) and xf > 0 and 0 < left < xf:
            nxt = shots[idx + 1]
            nf = 0.0 if nxt.hold <= 0 else max(0.0, (t - nxt.start) / nxt.hold)
            incoming = prepared[idx + 1].draw(nf)
            mode = transition if s.transition is None else s.transition
            p = 1.0 - left / xf
            if mode == "push":
                # **A push, not a dissolve.** A cross-dissolve necessarily shows
                # both shots at once, and for a third of a second the outgoing
                # shot's type sits on top of the incoming picture — which is
                # what a viewer reads as a mistake rather than as a transition.
                # Sliding one frame out as the other comes in keeps every pixel
                # showing exactly one shot, and still reads as a deliberate
                # move. Eased at both ends, because a linear slide reads as a
                # scroll rather than a cut.
                e = p * p * (3 - 2 * p)
                dx = int(round(frame.w * e))
                canvas = Image.new("RGB", frame.size, (0, 0, 0))
                canvas.paste(pic, (-dx, 0))
                canvas.paste(incoming, (frame.w - dx, 0))
                pic = canvas
            else:
                pic = Image.blend(pic, incoming, p)

        pic = pic.convert("RGBA")
        for sprite in (captions or ()):
            sprite.draw(pic, t)

        if mark is not None:
            by = logo_at[1] + logo_float * math.sin(2 * math.pi * t / logo_period)
            iy = math.floor(by)
            pic.alpha_composite(
                mark.transform(mark.size, Image.AFFINE,
                               (1, 0, 0, 0, 1, iy - by), resample=Image.BILINEAR),
                (logo_at[0], iy))
        pic = pic.convert("RGB")
        # Overlays go on last, over the watermark: a subscribe sting is
        # the topmost thing in the frame by definition.
        for ov in (overlays or ()):
            pic = ov.draw(pic, t)

        proc.stdin.write(pic.tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while encoding the picture track")
    return out
