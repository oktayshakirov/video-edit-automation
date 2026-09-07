"""The quiz beat: a question, a 2x2 of answer cards, a countdown, a verdict.

**This is a drawn beat, not a photographed one, and that is the whole format.**
Every other short in this repo buys its seconds with a picture; this one buys
them with a question the viewer is actually trying to answer. A photograph
behind the cards would compete with the only thing on screen that matters,
which is why there is no `PhotoShot` anywhere near it — the brand's own looping
background is the ground, the same one `ChecklistShot` sits on.

**Cards carry type, not photographs.** Considered and rejected: four licensed
stock images per question is twelve to twenty images a video, most answers have
no photographable subject at all ("the exchange owes it to you"), and a
photograph large enough to read at phone size leaves no room for the words that
say what it is. A card is a letter, a rule and an answer, and it renders in
milliseconds from nothing.

**Three phases, and the split is the format.** They matter in the same way
`ChecklistShot`'s two phases do, and for a stricter reason: here the viewer is
being asked to commit.

1. *Ask.* The question sets, then the four cards arrive one at a time on the
   caption starts of the options as they are read. Nothing is marked. Nobody is
   told anything.
2. *Wait.* The narration stops. A ring depletes around a number counting down,
   one clock tick a second, and the cards sit there. This silence is the beat —
   a quiz that answers itself immediately is a list with a question mark.
3. *Reveal.* The three wrong cards go red and dim together; a moment later the
   right one goes green, scales up and takes a tick. Together-then-one, not
   four in sequence: staggering the wrongs makes the viewer read three
   verdicts before the one they came for, and the payoff arrives fourth.

`QuizShot` renders all three from one `f`, so a question is one object and its
timings cannot drift apart the way they would across three shots.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ..core import backdrop
from ..core.brand import CRYPTO, Brand
from ..core.draw import ease_out as _ease_out
from ..core.draw import mark as _mark
from ..core.draw import shadow_text, wrap
from ..core.frame import VERTICAL, Frame
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX

LETTERS = ("A", "B", "C", "D")


def _rgba(c: tuple[int, int, int], a: int) -> tuple[int, int, int, int]:
    return (c[0], c[1], c[2], a)


def _mix(a, b, t: float):
    """Blend two RGB triples. Used only for the dim on a wrong card."""
    return tuple(int(round(x + (y - x) * t)) for x, y in zip(a, b))


class QuizShot:
    """One question, start to finish.

    Times are absolute timeline seconds, taken from the measured narration,
    because every one of them has to land on a syllable or a tick and none of
    them can be a fraction of the shot. `reveals[i]` is when card *i* arrives,
    `countdown_at` is when the ring starts, `mark_at` is when the wrong cards
    turn, and the tick on the right one follows `MARK_LAG` later.

    A question with no `countdown_at` renders as ask-then-reveal with no wait —
    which is what the *last* question wants if the video is running long, and
    what nothing else should ever want.
    """

    POP = 0.22                  # a card's entrance
    DRAW = 0.20                 # a verdict badge drawing on
    MARK_LAG = 0.45             # right answer lands after the wrongs
    GROW = 0.10                 # how much the correct card scales up

    def __init__(self, options: list[str], question: str = "",
                 correct: int = 0,
                 reveals: list[float] | None = None,
                 countdown_at: float | None = None,
                 countdown: float = 8.0,
                 mark_at: float | None = None,
                 answer: str | None = None,
                 start: float = 0.0, hold: float = 1.0,
                 font_path: str = FONT_CAPTION,
                 font_index: int = FONT_CAPTION_INDEX,
                 frame: Frame = VERTICAL,
                 brand: Brand = CRYPTO):
        if len(options) != 4:
            raise ValueError(f"a quiz card grid is four options, got "
                             f"{len(options)} — three reads as a missing card "
                             f"and five does not fit the 2x2")
        if not 0 <= correct < 4:
            raise ValueError(f"correct must index one of the four options, "
                             f"got {correct}")
        self.options = list(options)
        self.question = question
        self.correct = correct
        self.reveals = reveals
        self.countdown_at = countdown_at
        self.countdown = countdown
        self.mark_at = mark_at
        self.answer = answer
        self.start, self.hold = start, hold
        self.frame = frame
        self.brand = brand

        # **Every number here is dictated by the safe box, not by taste.** The
        # vertical frame gives this beat y=230 to y=1440, and the watermark
        # takes the top of that — so the usable band is about 1040px and it has
        # to hold a three-line question, four cards and a timer. The first
        # layout used 320px cards on a 880px grid line and looked right in
        # isolation; on a phone the bottom row and the whole ring sat under the
        # Shorts title block and the timer was invisible in the app while being
        # perfectly visible in review. That is the failure mode `Frame` exists
        # to catch, so the ring is bounds-checked in `draw` rather than trusted.
        #
        # Sizes scale with `frame.w`, so the object renders in 16:9 without a
        # second set of numbers — but the *stack* is portrait-shaped and this
        # format has no long form. See `docs/video/projects/quiz.md`.
        k = frame.w / 1080
        self.k = k
        self.q_font = ImageFont.truetype(font_path, int(54 * k), index=font_index)
        self.a_font = ImageFont.truetype(font_path, int(42 * k), index=font_index)
        self.l_font = ImageFont.truetype(font_path, int(36 * k), index=font_index)
        self.c_font = ImageFont.truetype(font_path, int(76 * k), index=font_index)
        self.ans_font = ImageFont.truetype(font_path, int(44 * k),
                                           index=font_index)

        self.q_top = int(430 * k)           # clears the watermark's lower edge
        self.card_w = int(460 * k)
        self.card_h = int(260 * k)
        self.gutter = int(32 * k)
        self.pad = int(24 * k)
        self.chip = int(46 * k)
        self.grid_x = (frame.w - (2 * self.card_w + self.gutter)) // 2
        self.grid_y = int(668 * k)
        self.ring_r = int(68 * k)
        self.ring_c = (frame.w // 2,
                       self.grid_y + 2 * self.card_h + self.gutter
                       + int(44 * k) + self.ring_r)

    # --- timing ---------------------------------------------------------

    def at(self, f: float) -> float:
        """This beat's `f` as an absolute timeline second."""
        return self.start + f * self.hold

    def _due(self, i: int) -> float:
        if self.reveals:
            return self.reveals[i]
        return self.start + self.hold * (0.15 + 0.12 * i)

    # **No `cues()` method here.** It used to live on this class, deriving the
    # clock ticks from `self.countdown_at` — correct for a question that was
    # one ask shot, wrong now that an ask phase is nine shots sharing one
    # `countdown_at`: asking every one of them for its own cues would mix the
    # same eight ticks nine times over. `quiz.build.render_quiz_short` is the
    # one place that already knows which of the nine shots owns the timing,
    # so it is the one place the sound is derived from now.

    # --- drawing --------------------------------------------------------

    def _card_box(self, i: int) -> tuple[int, int, int, int]:
        col, row = i % 2, i // 2
        x = self.grid_x + col * (self.card_w + self.gutter)
        y = self.grid_y + row * (self.card_h + self.gutter)
        return x, y, x + self.card_w, y + self.card_h

    def _draw_card(self, out: Image.Image, i: int, t: float) -> None:
        br, k = self.brand, self.k
        due = self._due(i)
        if t < due:
            return

        x0, y0, x1, y1 = self._card_box(i)
        e = _ease_out(min(1.0, (t - due) / self.POP))

        ok = (i == self.correct)
        marked = self.mark_at is not None and t >= self.mark_at + (
            self.MARK_LAG if ok else 0.0)
        m = 0.0
        if marked:
            m = _ease_out(min(1.0, (t - (self.mark_at + (self.MARK_LAG if ok
                                                         else 0.0))) / self.DRAW))

        # The right card grows into its verdict. Nothing else moves, so the
        # growth *is* the answer — a viewer catches it before they read either
        # colour, which is what makes the beat work with the sound off.
        grow = 1.0 + (self.GROW * m if ok and marked else 0.0)
        cw, ch = (x1 - x0) * grow, (y1 - y0) * grow
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        bx0, by0 = cx - cw / 2, cy - ch / 2
        bx1, by1 = cx + cw / 2, cy + ch / 2

        # The entrance: the card rises the last few pixels and fades in, tied
        # to the syllable that names it — same move as a checklist item.
        dy = int(round(20 * k * (1.0 - e)))
        by0 += dy
        by1 += dy

        border = br.ink
        fill = br.panel
        if marked:
            target = br.positive if ok else br.negative
            border = _mix(br.ink, target, m)
            # A wrong card is dimmed *towards the background* rather than
            # tinted red: three red-filled cards next to one green one is a
            # traffic light, and the eye goes to the red because there is more
            # of it. Dimming makes the right card the only lit object.
            # 0.35 rather than the 0.22 this started at. On crypto's near
            # black panel 0.22 already read green; on tinnitus' purple panel
            # (91,57,100) it lands on a grey-lavender and the fill stopped
            # carrying any of the verdict — the border, chip and tick were
            # doing all of it. The higher mix reads on both.
            fill = _mix(br.panel, br.bg, 0.55 * m) if not ok else \
                _mix(br.panel, target, 0.35 * m)

        layer = Image.new("RGBA", out.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        radius = int(28 * k)
        d.rounded_rectangle([bx0, by0, bx1, by1], radius=radius,
                            fill=_rgba(fill, int(235 * e)),
                            outline=_rgba(border, int(255 * e)),
                            width=max(2, int((4 + 4 * m) * k)))
        out.alpha_composite(layer)

        d = ImageDraw.Draw(out)
        pad, chip = self.pad, self.chip

        # The letter, in its own chip. It is what the narration says ("A —
        # the exchange owes it to you") and what a comment quotes back, so it
        # has to be findable without reading the card.
        d.rounded_rectangle([bx0 + pad, by0 + pad, bx0 + pad + chip,
                             by0 + pad + chip],
                            radius=int(12 * k),
                            fill=(br.positive if (marked and ok) else
                                  br.negative if marked else br.primary))
        lb = d.textbbox((0, 0), LETTERS[i], font=self.l_font)
        d.text((bx0 + pad + (chip - (lb[2] - lb[0])) / 2 - lb[0],
                by0 + pad + (chip - (lb[3] - lb[1])) / 2 - lb[1]),
               LETTERS[i], font=self.l_font, fill=br.bg)

        # The verdict badge, opposite the letter. `core.draw.mark` is the same
        # cross and tick the checklist draws, so the two beats' verdicts are
        # visibly one vocabulary rather than two.
        if marked and m > 0:
            _mark(d, int(bx1 - pad - 40 * k), int(by0 + pad + 4 * k),
                  int(40 * k), ok, br.positive if ok else br.negative,
                  progress=m)

        # The answer text, wrapped, sitting under the chip row.
        ink = br.ink if (not marked or ok) else _mix(br.ink, br.panel, 0.45 * m)
        lines = wrap(d, self.options[i], self.a_font, cw - 2 * pad)
        lh = self.a_font.size * 1.22
        ty = by0 + pad + chip + int(18 * k)
        # Three lines is what the card holds. A fourth is not clipped quietly —
        # an answer that long is the script's problem and the writer has to see
        # it, so `render_quiz_short` measures every option up front.
        for ln in lines[:3]:
            shadow_text(d, (bx0 + pad, ty), ln, self.a_font, ink)
            ty += lh

    def _draw_ring(self, out: Image.Image, t: float) -> None:
        """The countdown: a depleting arc and the whole seconds inside it."""
        if self.countdown_at is None:
            return
        elapsed = t - self.countdown_at
        if elapsed < 0 or elapsed > self.countdown:
            return

        br, k = self.brand, self.k
        cx, cy, r = *self.ring_c, self.ring_r
        box = [cx - r, cy - r, cx + r, cy + r]
        left = 1.0 - elapsed / self.countdown

        layer = Image.new("RGBA", out.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.ellipse(box, fill=_rgba(br.bg, 190))
        d.arc(box, 0, 360, fill=_rgba(br.panel, 255), width=int(10 * k))
        if left > 0:
            # **Clockwise from twelve.** The remaining arc runs the way a hand
            # sweeps, so what is left of it *is* what is left of the time. The
            # first version drew it anticlockwise — which drains, but leaves the
            # remainder sitting in the upper left, and at "2" it read as a
            # progress bar that had gone backwards.
            d.arc(box, -90, -90 + 360 * left,
                  fill=_rgba(br.primary, 255), width=int(10 * k))
        out.alpha_composite(layer)

        # Whole seconds remaining, rounded up so it reads 8 for the first
        # second and 1 for the last. A zero is never shown: the number leaves
        # and the verdict arrives, which is one event rather than two.
        n = max(1, math.ceil(self.countdown - elapsed))
        s = str(n)

        # A pulse on each whole second — the visual half of the tick, and the
        # reason the countdown reads as time passing rather than as a number
        # that changes. It is a real scale: the digit is drawn to its own layer
        # and resized, because scaling a *position* the way the first version
        # did moves the glyph a few pixels and looks like jitter.
        frac = (self.countdown - elapsed) % 1.0
        pulse = 1.0 + 0.14 * (1.0 - _ease_out(min(1.0, (1.0 - frac) / 0.22)))

        digit = Image.new("RGBA", (self.ring_r * 2, self.ring_r * 2),
                          (0, 0, 0, 0))
        dd = ImageDraw.Draw(digit)
        b = dd.textbbox((0, 0), s, font=self.c_font)
        dd.text((digit.width / 2 - (b[2] - b[0]) / 2 - b[0],
                 digit.height / 2 - (b[3] - b[1]) / 2 - b[1]),
                s, font=self.c_font, fill=_rgba(br.primary, 255))
        if pulse > 1.001:
            w = int(digit.width * pulse)
            digit = digit.resize((w, w), Image.LANCZOS)
        out.alpha_composite(digit, (int(cx - digit.width / 2),
                                    int(cy - digit.height / 2)))

    def _draw_answer(self, out: Image.Image, t: float) -> None:
        """The *because*, in the space the countdown vacated.

        **The reveal used to be silent on screen and that was a real hole.**
        A shot with a `graphic` burns no captions — right for every other
        drawn beat, whose items already are the type — so the answer line was
        spoken over four marked cards and nothing else. Most of this audience
        watches muted; they got the colours and never got the reason, which is
        the only part of the beat carrying the article.

        It sets under the grid rather than over it, in the band the ring is
        using during the countdown. Nothing is ever on screen at the same time
        as the timer, so the two share the space instead of competing for it.
        """
        if not self.answer or self.mark_at is None:
            return
        due = self.mark_at + self.MARK_LAG
        if t < due:
            return

        br, k, fr = self.brand, self.k, self.frame
        e = _ease_out(min(1.0, (t - due) / 0.30))

        layer = Image.new("RGBA", out.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        lines = wrap(d, self.answer, self.ans_font, fr.w - int(160 * k))
        lh = self.ans_font.size * 1.22
        # Anchored to the top of the timer band and rising into place, so it
        # arrives from where the countdown was rather than from nowhere.
        y = (self.grid_y + 2 * self.card_h + self.gutter + int(30 * k)
             + int(round(16 * k * (1.0 - e))))
        for ln in lines[:2]:
            shadow_text(d, (int(80 * k), y), ln, self.ans_font, br.ink,
                        alpha=int(255 * e))
            y += lh
        out.alpha_composite(layer)

    def draw(self, f: float) -> Image.Image:
        fr, br, k = self.frame, self.brand, self.k
        bg = backdrop.get(br.backdrop)
        if bg is not None:
            # Sampled by timeline seconds, like every other drawn beat, so the
            # loop runs at one rate across the video instead of restarting
            # inside each question.
            base = Image.fromarray(bg.at(self.at(f), fr.w, fr.h))
        else:
            base = Image.new("RGB", fr.size, br.bg)
        out = base.convert("RGBA")

        t = self.at(f)
        d = ImageDraw.Draw(out)

        # The timer is the one element with nothing below it to push, so it is
        # the one that silently leaves the safe box when a size changes. Checked
        # every frame, which costs nothing and is the difference between a
        # failed render and a shipped video whose countdown is under the app's
        # own title block.
        if self.countdown_at is not None and \
                self.ring_c[1] + self.ring_r > fr.safe_bottom:
            raise ValueError(
                f"quiz countdown ring reaches y="
                f"{self.ring_c[1] + self.ring_r} past {fr.name} safe_bottom="
                f"{fr.safe_bottom} — it would sit under the platform's caption "
                f"block")

        if self.question:
            lines = wrap(d, self.question, self.q_font, fr.w - int(160 * k))
            y = self.q_top
            fr.check_top(y, "quiz question")
            for ln in lines[:3]:
                shadow_text(d, (int(80 * k), y), ln, self.q_font, br.primary)
                y += self.q_font.size * 1.20

        for i in range(4):
            self._draw_card(out, i, t)
        self._draw_ring(out, t)
        self._draw_answer(out, t)

        return out.convert("RGB")
