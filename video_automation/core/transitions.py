"""The shot-to-shot move, chosen by what the cut *means*.

`render_shots` has had exactly two moves since the shorts were built: a
dissolve, and the `push` long form opted into. Both are good and neither says
anything — every cut in a three-minute video is the same gesture, so the cut
stops being punctuation and becomes wallpaper. This module is the same idea as
`openers.py` one level down: a small vocabulary, **chosen by the relationship
between the two shots** rather than by taste.

| mode | the cut it is for |
| --- | --- |
| `dissolve` | a topic change. The slow one. Two photographs only. |
| `push` | the default. Continuation - still on the same argument. |
| `whip` | into a chapter card. A turn, and it should feel like one. |
| `glitch` | a contradiction. The claim, then the thing that breaks it. |
| `flash` | a reveal. The number, the verdict, the payoff. |
| `wipe` | a comparison. The band crossing *is* the "versus". |
| `punch` | escalation. Same subject, closer in. |

**Two rules carried over from `render_shots`' own comments, and they are not
style preferences.** A dissolve between two *drawn* beats cross-fades two sets
of type through each other and reads as a fault, which is why long form already
sets `xfade=0` between beats - every mode here except `dissolve` keeps each
pixel showing exactly one shot, or shows neither, so all of them are safe
between beats. And everything is eased: a linear travel reads as a scroll.

`XF` is the length each mode wants. A whip has to be *fast* to read as a whip
(0.22s) and a dissolve has to be slow to read as one at all (0.60s), so a
single `xfade=0.34` for the whole video is wrong for five of the seven. The
caller reads this rather than guessing - see `Shot.xfade`.
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageFilter

# How long each move wants to be. Set on the shot *leaving*, as `Shot.xfade`.
XF = {
    "dissolve": 0.60,
    "push": 0.34,
    "whip": 0.22,
    "glitch": 0.18,
    "flash": 0.20,
    "wipe": 0.40,
    "punch": 0.26,
}

# The sound each move wants under it, and how far ahead of the cut it fires.
# A whoosh peaks after its transient, so a whip's whoosh starts *before* the
# picture moves or the sound arrives late; a flash's pop is on the frame.
CUES = {
    "whip": ("whoosh", -0.10),
    "glitch": ("hook_glitch", -0.02),
    "flash": ("hook_pop", -0.04),
    "wipe": ("hook_swish", -0.08),
    "punch": ("impact", -0.03),
}


def _smooth(p: float) -> float:
    """Smoothstep. Eased at both ends, unlike `ease_out`."""
    return p * p * (3 - 2 * p)


def _blur_x(im: Image.Image, px: float) -> Image.Image:
    """Horizontal-only blur, which is what a fast pan actually does to a frame.

    PIL has no directional blur, so this is a box blur on a squashed copy:
    scaling x down by `k`, blurring, and scaling back spreads each pixel across
    `k` of its neighbours horizontally and leaves y untouched. Cheaper than a
    convolution and, at the 1-2 frame durations this is visible for, identical
    to the eye.
    """
    if px < 1.5:
        return im
    k = max(1, int(px / 3))
    w, h = im.size
    small = im.resize((max(1, w // k), h), Image.BILINEAR)
    return small.filter(ImageFilter.GaussianBlur(1.2)).resize((w, h),
                                                              Image.BILINEAR)


def _push(out: Image.Image, inc: Image.Image, p: float, frame) -> Image.Image:
    """The shipped push, unchanged - see `render_shots` for why it exists.

    Lifted verbatim so the existing long-form videos render identically
    through this module. Do not "improve" it; the shorts are reproducible
    against a baseline and this is on their path.
    """
    e = _smooth(p)
    dx = int(round(frame.w * e))
    canvas = Image.new("RGB", frame.size, (0, 0, 0))
    canvas.paste(out, (-dx, 0))
    canvas.paste(inc, (frame.w - dx, 0))
    return canvas


def _whip(out: Image.Image, inc: Image.Image, p: float, frame) -> Image.Image:
    """A push with the travel smeared - the pan a camera operator would make.

    The blur is keyed to the *speed* of the travel, not to `p`, so it builds
    into the middle of the move and is gone by the time either frame is
    readable. That is the whole trick: a whip with constant blur reads as an
    out-of-focus slide, and a whip with none reads as a push played too fast.
    """
    e = _smooth(p)
    speed = 1.0 - abs(2 * p - 1)            # 0 at both ends, 1 in the middle
    blur = 46 * speed
    dx = int(round(frame.w * e))
    canvas = Image.new("RGB", frame.size, (0, 0, 0))
    canvas.paste(out, (-dx, 0))
    canvas.paste(inc, (frame.w - dx, 0))
    return _blur_x(canvas, blur)


def _glitch(out: Image.Image, inc: Image.Image, p: float, frame) -> Image.Image:
    """A hard cut, wrapped in two frames of broken signal.

    **It is a cut, not a blend.** The incoming shot is on screen from halfway,
    full strength - what makes it read as a transition is that the frames
    either side are torn. Horizontal slices are displaced by a random amount
    that decays away from the cut, and the red and blue channels are pulled
    apart. For a contradiction: the claim, then the thing that breaks it.
    """
    src = out if p < 0.5 else inc
    amt = 1.0 - abs(2 * p - 1)              # peaks exactly on the cut
    if amt < 0.05:
        return src

    a = np.asarray(src).copy()
    h, w, _ = a.shape
    # A fixed generator: the same cut renders the same way on every re-run,
    # which is the difference between a designed effect and a flickering one.
    rng = np.random.default_rng(int(p * 997) + 11)
    for _ in range(int(3 + 9 * amt)):
        y0 = int(rng.integers(0, h - 8))
        y1 = min(h, y0 + int(rng.integers(6, 46)))
        a[y0:y1] = np.roll(a[y0:y1], int(rng.integers(-1, 2) * 60 * amt), axis=1)

    # Chromatic split. Red one way, blue the other, green held - anything else
    # reads as a colour cast rather than as a signal fault.
    shift = int(round(13 * amt))
    if shift:
        a[:, :, 0] = np.roll(a[:, :, 0], shift, axis=1)
        a[:, :, 2] = np.roll(a[:, :, 2], -shift, axis=1)
    return Image.fromarray(a)


def _flash(out: Image.Image, inc: Image.Image, p: float, frame,
           colour: tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    """A cut through a bloom of the brand's own colour. For a payoff.

    Also a hard cut underneath - the wash is what the eye reads, and it hides
    the join completely, so this is the one move that can put two unrelated
    pictures next to each other without the seam showing.

    Short by construction. `XF["flash"]` is 0.20s; past about a quarter of a
    second a flash stops reading as an impact and starts reading as a fault in
    the encode.
    """
    src = out if p < 0.5 else inc
    amt = 1.0 - abs(2 * p - 1)
    if amt < 0.02:
        return src
    wash = Image.new("RGB", frame.size, colour)
    return Image.blend(src, wash, min(0.92, amt ** 0.7))


def _wipe(out: Image.Image, inc: Image.Image, p: float, frame,
          colour: tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
    """A hard-edged band travels across, and the incoming shot is behind it.

    The band is the brand accent and it is the point: for a comparison, the
    crossing *is* the word "versus". Slightly sheared, because a vertical edge
    at 1920 reads as a rendering artifact and a raked one reads as a wipe.
    """
    e = _smooth(p)
    band = int(frame.w * 0.11)
    # Travel far enough that the band itself has fully left at p=1.
    x = int(e * (frame.w + band * 2)) - band

    canvas = Image.new("RGB", frame.size)
    canvas.paste(inc, (0, 0))
    # Everything to the right of the band is still the outgoing shot.
    if x + band < frame.w:
        canvas.paste(out.crop((x + band, 0, frame.w, frame.h)), (x + band, 0))

    a = np.asarray(canvas).copy()
    rake = int(frame.h * 0.06)
    for y in range(frame.h):
        # The shear: the band leans forward at the top.
        off = int(rake * (0.5 - y / frame.h) * 2)
        x0 = max(0, min(frame.w, x + off))
        x1 = max(0, min(frame.w, x + off + band))
        if x1 > x0:
            a[y, x0:x1] = colour
    return Image.fromarray(a)


def _punch(out: Image.Image, inc: Image.Image, p: float, frame) -> Image.Image:
    """The outgoing shot rushes at the camera; the incoming settles back.

    For escalation - the same subject, closer in. Both halves move, which is
    what separates this from a zoom-and-dissolve: the outgoing accelerates away
    from its own scale and the incoming decelerates into rest, so the cut has a
    direction. Crops are computed on the source and resized back to the frame,
    so nothing is ever upscaled past the shot's own resolution by more than the
    1.14 headroom here.
    """
    e = _smooth(p)
    w, h = frame.w, frame.h

    def scaled(im: Image.Image, k: float) -> Image.Image:
        if k <= 1.001:
            return im
        cw, ch = int(w / k), int(h / k)
        x0, y0 = (w - cw) // 2, (h - ch) // 2
        return im.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.BICUBIC)

    if p < 0.5:
        return scaled(out, 1.0 + 0.14 * (e * 2))
    return scaled(inc, 1.0 + 0.14 * (1.0 - (e - 0.5) * 2))


_MODES = {
    "push": _push,
    "whip": _whip,
    "glitch": _glitch,
    "flash": _flash,
    "wipe": _wipe,
    "punch": _punch,
}

# The moves that paint in the brand's accent rather than in white.
_BRANDED = {"flash", "wipe"}


def apply(mode: str, out: Image.Image, inc: Image.Image, p: float, frame,
          brand=None) -> Image.Image:
    """The frame partway through a transition, `p` from 0 (all `out`) to 1.

    An unknown mode falls back to a dissolve rather than raising: this is
    called once per frame inside the encoder, and a typo in a shot list should
    cost a soft-looking cut, not a half-written MP4.
    """
    fn = _MODES.get(mode)
    if fn is None:
        return Image.blend(out, inc, p)
    if mode in _BRANDED:
        col = brand.primary if brand is not None else (255, 255, 255)
        return fn(out, inc, p, frame, col)
    return fn(out, inc, p, frame)


def cues(shots) -> list[tuple[float, str]]:
    """The sound each transition wants, from a planned shot list.

    Returned in `sfx.mix`'s own `(at, kind)` shape so a caller can concatenate
    it with the beat cues. A shot whose mode has no sound contributes nothing -
    a push and a dissolve are deliberately silent, because a sound on every cut
    in a three-minute video is worse than a sound on none.
    """
    out = []
    for i, s in enumerate(shots[:-1]):
        mode = s.transition
        if mode not in CUES:
            continue
        xf = XF.get(mode, 0.34) if s.xfade is None else s.xfade
        if xf <= 0:
            continue
        kind, lead = CUES[mode]
        at = s.start + s.hold - xf + lead
        if at > 0:
            out.append((at, kind))
    return out
