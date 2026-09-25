"""The long-form navigation layer: a ticked progress bar and "3 of 5".

Chapters already exist twice over: `Section` renders a `ChapterCard`, and
`meta.py` writes the timestamps YouTube turns into a labelled scrubber. What
neither does is tell the viewer *while they are watching* where they are.
Between two cards there is nothing on screen that says a three-minute video
has five parts and this is the third of them, and the retention curves in
`docs/video/projects/` keep measuring the drop in exactly that dead middle.

Two pieces, both deliberately tiny:

* `ProgressBar` - a 5px rule along the bottom, with a tick at each chapter
  boundary. It is the video's spine, made visible. It is **not** a substitute
  for the player's own scrubber, which is hidden on mobile and during
  playback: this one is always there and costs 5 pixels of a 1080 frame.
* `ChapterCount` - "3 of 5", set under a chapter card's title for the second
  it is on screen.

**The argument against both is real and was weighed.** A progress bar
tells a viewer at 0:20 that there are two and a half minutes left, and some of
them will leave *because* of that. The counter-argument, and the reason this
is worth testing rather than assuming: an unmarked middle gives them no reason
to stay either, and a visible structure is the thing that makes "there are two
parts left" read as a promise rather than as a sentence. That is an A/B
question, not a design question, which is why this is one overlay that can be
switched off with one argument rather than something woven into the beats -
if the retention curves say it costs more than it pays, drop the overlay and
nothing else changes.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from ..core.brand import Brand
from ..core.draw import ease_out
from ..core.frame import Frame


class ProgressBar:
    """A hairline along the bottom edge, ticked at every chapter boundary.

    An overlay in `render_shots`' sense: `draw(pic, t)` and nothing else, so it
    composites over the watermark and under nothing.

    `bounds` is the chapter start times in seconds, `total` the runtime. The
    filled part is drawn in the brand accent over an unfilled track at low
    alpha - a bar with no visible track shows progress but not how much is
    left, which is half the information and the annoying half.
    """

    H = 5                      # the filled rule
    TICK = 13                  # a boundary mark, drawn up from the baseline

    def __init__(self, bounds: list[float], total: float, brand: Brand,
                 frame: Frame, fade_in: float = 1.2):
        self.bounds, self.total = bounds, total
        self.brand, self.frame, self.fade_in = brand, frame, fade_in

    def cues(self) -> list[tuple[float, str]]:
        """No sound. Here so it is interchangeable with the other overlays."""
        return []

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        fr, br = self.frame, self.brand
        # It fades in rather than being there from frame zero: over the hook,
        # the only thing on screen should be the hook.
        a = ease_out(min(1.0, t / self.fade_in)) if self.fade_in else 1.0
        if a <= 0.01:
            return pic

        out = pic.convert("RGBA")
        d = ImageDraw.Draw(out, "RGBA")
        y = fr.h - self.H
        d.rectangle([0, y, fr.w, fr.h], fill=br.primary + (int(46 * a),))

        p = max(0.0, min(1.0, t / self.total)) if self.total else 0.0
        d.rectangle([0, y, int(fr.w * p), fr.h], fill=br.primary + (int(230 * a),))

        # The ticks sit *above* the rule, so a passed boundary is still
        # visible against the filled bar rather than being painted over by it.
        for b in self.bounds:
            if b <= 0 or b >= self.total:
                continue
            bx = int(fr.w * b / self.total)
            passed = t >= b
            d.rectangle([bx - 1, y - self.TICK, bx + 1, y],
                        fill=br.primary + (int((215 if passed else 96) * a),))
        return out.convert("RGB")


class ChapterCount:
    """"3 of 5", under a chapter card's title, for as long as the card is up.

    Deliberately not a numeral *on* the title - `ChapterCard`'s own docstring
    bans that, and it is right: a numbered agenda tells the viewer they are
    being lectured. "3 of 5" is a different statement. It does not number the
    content, it says how much is left, which is the one piece of information a
    viewer who is deciding whether to stay actually wants.

    Set small and in the accent at 60% - it is a footnote to the card, and if
    it competes with the title the card has stopped working.
    """

    def __init__(self, index: int, count: int, at: float, hold: float,
                 brand: Brand, frame: Frame):
        self.index, self.count = index, count
        self.at, self.hold = at, hold
        self.brand, self.frame = brand, frame

    def cues(self) -> list[tuple[float, str]]:
        return []

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.at <= t < self.at + self.hold):
            return pic
        from .beats import _font

        fr, br = self.frame, self.brand
        # In on the card's own entrance, out with it. A label that outlives
        # the card it annotates reads as a stuck overlay.
        p = min(1.0, (t - self.at) / 0.4)
        q = min(1.0, (self.at + self.hold - t) / 0.4)
        a = int(255 * 0.6 * ease_out(min(p, q)))
        if a <= 2:
            return pic

        out = pic.convert("RGBA")
        d = ImageDraw.Draw(out, "RGBA")
        d.text((fr.w // 2, int(fr.h * 0.68)),
               f"{self.index} OF {self.count}", font=_font(34),
               fill=br.primary + (a,), anchor="ma")
        return out.convert("RGB")
