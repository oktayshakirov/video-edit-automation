"""Pick a card: a quiz Short with no right answer.

Love Swipe's cards are things a couple *does*, not things a viewer gets right,
so this is the quiz format with the reveal taken out: two cards a round, the
viewer still commits during a countdown, and nothing is marked afterwards,
because nothing is wrong. It reuses the quiz's pacing (every gap at or above
`RUN_BREAK`, the `LEAD`/`TAIL` daylight around the ring, the whoosh ahead of
each round) and the quiz's ring, and draws its own beat.

**Two truths, not a truth and a dare (2026-10-27, the user's call on the first
cut).** A six-second countdown is time to *choose*, and a dare is not done in
six seconds - the first cut asked the viewer to pick a dare and then swiped it
away before anyone could stand up. A truth is answered out loud, so picking
one of two and answering it fits the wait; the title card tells the viewer to
pause if they need longer, and the ring repeats it on screen. `Round.labels`
still takes ("TRUTH", "DARE") if a later cut wants that pairing back.

**A round is two shots.** The first card is read, then the second ("Or, ..."),
then the ring runs between them in the second card's trailing gap, then both
cards swipe off - the first to the left, the second to the right, the gesture
the app itself is played with. The swipe is the round's exit and the next round's
whoosh lands inside it.

The card's label is never spoken. That is the quiz's `LETTER_SPOKEN` lesson
applied up front: a one-word label synthesised alone reads as clipped, and the
"Or" in front of the second card already says there is a choice.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ..core import backdrop
from ..core.brand import Brand
from ..core.draw import ease_out as _ease_out
from ..core.draw import shadow_text, wrap
from ..core.frame import VERTICAL, Frame
from ..core.vertical import FONT_CAPTION
from ..crypto.build import _short_factory, render_crypto_short
from ..crypto.shots import Shot
from .build import (COUNTDOWN, GAP, LEAD, MUSIC_LUFS, RUN_BREAK, TAIL,
                    TITLE_GAP, WHOOSH_LEAD)
from .cards import QuizShot

# The icon's two neons: cyan on the first card, pink on the second.
CARD_COLORS = ((80, 210, 255), (255, 90, 170))

CARD_GAP = 0.70          # after the first card, before the second
# The swipe-off after the ring's last tick. At least `WHOOSH_LEAD`, so the
# next round's whoosh sits inside it rather than over the last tick.
EXIT = 0.85

FONT_BOLD_INDEX = 2      # Futura Bold in Futura.ttc
FONT_MEDIUM_INDEX = 0


def _you(text: str) -> str:
    """The app's `{player1}`-to-`{player2}` wording, as said to a viewer.

    The app addresses the player whose turn it is about the other one; a
    viewer is "you" about "your partner". Raises on any placeholder this
    does not handle rather than putting a brace on screen.
    """
    t = text.replace("{player1} and {player2}", "You and your partner")
    if t.startswith("{player1}, "):
        t = t[len("{player1}, "):]
        t = t[0].upper() + t[1:]
    t = t.replace("{player2}'s", "your partner's")
    t = t.replace("{player2}", "your partner")
    if "{player" in t:
        raise ValueError(f"unhandled placeholder in {text!r}")
    return t


@dataclass
class Round:
    """Two app cards' texts and the labels their chips carry.

    Build it with `from_app`, which takes the deck's strings unchanged.
    """
    cards: tuple[str, str]
    labels: tuple[str, str] = ("TRUTH A", "TRUTH B")
    deck: str = ""
    countdown: float = COUNTDOWN

    @classmethod
    def from_app(cls, first: str, second: str, deck: str = "",
                 **kw) -> "Round":
        return cls((_you(first), _you(second)), deck=deck, **kw)

    def line(self, i: int) -> "str | tuple[str, str]":
        """The `(caption, spoken)` pair for card `i`.

        The second card is read as "Or, ..." so the choice is heard as well
        as seen. The first word is lower-cased after "Or," unless it is "I".
        """
        text = self.cards[i]
        spoken = text
        if i == 1:
            head, _, rest = text.partition(" ")
            if head not in ("I", "I'm", "I've", "I'd"):
                head = head[0].lower() + head[1:]
            spoken = f"Or, {head} {rest}".rstrip()
        if spoken[-1] not in ".!?":
            spoken += "."
        return text if spoken == text else (text, spoken)


class TruthDareShot:
    """One round: header, two cards, the ring, the swipe-off.

    Times are absolute timeline seconds, like `QuizShot`: `reveals` is when
    each card arrives, `countdown_at` when the ring starts, `exit_at` when
    the cards start leaving.
    """

    POP = 0.28
    PULL = 0.70          # how far a card travels on its entrance, in widths/10

    def __init__(self, rnd: Round, index: int, total: int,
                 reveals: list[float] | None = None,
                 countdown_at: float | None = None,
                 exit_at: float | None = None,
                 ask: str = "PICK ONE",
                 hint: str | None = "Pause if you need more time",
                 start: float = 0.0, hold: float = 1.0,
                 frame: Frame = VERTICAL, brand: Brand | None = None):
        self.rnd, self.index, self.total = rnd, index, total
        self.reveals = reveals
        self.countdown_at = countdown_at
        self.exit_at = exit_at
        self.ask, self.hint = ask, hint
        self.start, self.hold = start, hold
        self.frame, self.brand = frame, brand

        k = frame.w / 1080
        self.k = k
        self.h_font = ImageFont.truetype(FONT_CAPTION, int(50 * k),
                                         index=FONT_BOLD_INDEX)
        self.hint_font = ImageFont.truetype(FONT_CAPTION, int(34 * k),
                                            index=FONT_MEDIUM_INDEX)
        self.chip_font = ImageFont.truetype(FONT_CAPTION, int(34 * k),
                                            index=FONT_BOLD_INDEX)
        self.t_font = ImageFont.truetype(FONT_CAPTION, int(50 * k),
                                         index=FONT_MEDIUM_INDEX)

        # The safe box decides every number: the header clears the watermark
        # lockup, and the second card ends just inside `safe_bottom`.
        #
        # **The ring sits between the two cards, not under them** (the
        # user's note on the second cut, 2026-10-27). Under them it was the
        # thing holding the stack up: the ring's bottom had to clear
        # `safe_bottom`, so the cards could not come down and the header was
        # crowded while the bottom of the frame stayed empty. In the gap it
        # costs no height of its own, the cards drop to the bottom of the
        # safe box, and there is 70px+ between the pause hint and the first
        # card. Outside the countdown the gap carries the app's heart, the
        # same divider the app draws between its truth and its dare.
        self.h_top = int(440 * k)
        self.hint_y = int(512 * k)
        self.card_x = int(80 * k)
        self.card_w = frame.w - 2 * self.card_x
        self.card_h = int(320 * k)
        self.card_gap = int(170 * k)
        self.card_y = (int(620 * k), int(620 * k) + self.card_h
                       + self.card_gap)
        self.pad = int(34 * k)
        self.chip_h = int(58 * k)

        # The ring is the quiz's own, centred in the gap between the cards.
        gap_mid = self.card_y[0] + self.card_h + self.card_gap // 2
        self.ring = QuizShot(["", "", "", ""], countdown_at=countdown_at,
                             countdown=rnd.countdown, frame=frame, brand=brand)
        self.ring.ring_c = (frame.w // 2, gap_mid)

        self.heart = None
        if brand is not None and brand.mascot is not None \
                and brand.mascot.exists():
            im = Image.open(brand.mascot).convert("RGBA")
            im = im.crop(im.getbbox())
            hw = int(118 * k)
            self.heart = im.resize((hw, max(1, int(im.height * hw / im.width))),
                                   Image.LANCZOS)
            self.heart_at = (frame.w // 2 - self.heart.width // 2,
                             gap_mid - self.heart.height // 2)

        self._sprites: dict[int, Image.Image] = {}

    def at(self, f: float) -> float:
        return self.start + f * self.hold

    def text_lines(self, text: str) -> int:
        d = ImageDraw.Draw(Image.new("RGB", (8, 8)))
        return len(wrap(d, text, self.t_font, self.card_w - 2 * self.pad))

    # --- the card, drawn once and moved -----------------------------------

    def _sprite(self, i: int) -> Image.Image:
        """The whole card with its glow, rendered once per shot and cached.

        Every frame of a card's life is this image moved, faded or turned;
        nothing inside it changes. Blurring a glow per frame would cost a
        full-frame gaussian on every one of them for the same pixels.
        """
        if i in self._sprites:
            return self._sprites[i]
        br, k = self.brand, self.k
        colour = CARD_COLORS[i]
        glow = int(28 * k)
        w, h = self.card_w + 2 * glow, self.card_h + 2 * glow
        radius = int(30 * k)
        box = [glow, glow, glow + self.card_w, glow + self.card_h]

        # The neon: the border drawn thick, blurred, under the crisp one -
        # the same glow the app icon's two cards carry.
        halo = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(halo).rounded_rectangle(
            box, radius=radius, outline=colour + (255,), width=int(14 * k))
        halo = halo.filter(ImageFilter.GaussianBlur(int(16 * k)))

        im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        # Twice: one pass of a 16px blur spreads the line so thin it barely
        # reads as light on the plum ground.
        im.alpha_composite(halo)
        im.alpha_composite(halo)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle(box, radius=radius, fill=br.panel + (238,),
                            outline=colour + (255,), width=max(2, int(4 * k)))

        # The label chip, filled in the card's own neon, dark type on it.
        label = self.rnd.labels[i]
        lb = d.textbbox((0, 0), label, font=self.chip_font)
        cw = (lb[2] - lb[0]) + int(44 * k)
        cx0, cy0 = glow + self.pad, glow + self.pad
        d.rounded_rectangle([cx0, cy0, cx0 + cw, cy0 + self.chip_h],
                            radius=self.chip_h // 2, fill=colour + (255,))
        d.text((cx0 + (cw - (lb[2] - lb[0])) / 2 - lb[0],
                cy0 + (self.chip_h - (lb[3] - lb[1])) / 2 - lb[1]),
               label, font=self.chip_font, fill=br.bg)

        lines = wrap(d, self.rnd.cards[i], self.t_font,
                     self.card_w - 2 * self.pad)
        lh = self.t_font.size * 1.22
        ty = cy0 + self.chip_h + int(22 * k)
        for ln in lines[:3]:
            shadow_text(d, (glow + self.pad, ty), ln, self.t_font, br.ink)
            ty += lh

        self._sprites[i] = im
        return im

    def _draw_card(self, out: Image.Image, i: int, t: float) -> None:
        due = self.reveals[i] if self.reveals else self.at(0.1 + 0.3 * i)
        if t < due:
            return
        fr = self.frame
        sprite = self._sprite(i)
        glow = (sprite.width - self.card_w) // 2
        side = -1 if i == 0 else 1
        x = self.card_x - glow
        y = self.card_y[i] - glow

        # Entrance: slides in from its own side and fades up, so the pair
        # arrives the way it will leave.
        e = _ease_out(min(1.0, (t - due) / self.POP))
        x += int(round(side * fr.w * 0.1 * self.PULL * (1.0 - e)))
        alpha = e
        angle = 0.0

        # Exit: the swipe. Accelerates off its side with a turn, the way a
        # card thrown by a thumb does.
        if self.exit_at is not None and t >= self.exit_at:
            p = min(1.0, (t - self.exit_at) / EXIT)
            ease_in = p * p
            x += int(round(side * fr.w * 1.1 * ease_in))
            angle = -side * 14.0 * ease_in
            alpha *= 1.0 - 0.6 * ease_in

        img = sprite
        if angle:
            img = sprite.rotate(angle, resample=Image.BICUBIC, expand=True)
            x -= (img.width - sprite.width) // 2
            y -= (img.height - sprite.height) // 2
        if alpha < 0.999:
            a = img.getchannel("A").point(lambda v: int(v * alpha))
            img = img.copy()
            img.putalpha(a)
        _composite_clipped(out, img, x, y)

    def draw(self, f: float) -> Image.Image:
        fr, br = self.frame, self.brand
        t = self.at(f)
        bg = backdrop.get(br.backdrop)
        base = (Image.fromarray(bg.at(t, fr.w, fr.h)) if bg is not None
                else Image.new("RGB", fr.size, br.bg))
        out = base.convert("RGBA")

        if self.card_y[1] + self.card_h > fr.safe_bottom:
            raise ValueError(
                f"pick-a-card second card reaches y="
                f"{self.card_y[1] + self.card_h} past "
                f"{fr.name} safe_bottom={fr.safe_bottom}")

        # The header names the round until the ring starts, then asks - and
        # the pause hint sits under it for as long as the ring runs.
        d = ImageDraw.Draw(out)
        asking = (self.countdown_at is not None and t >= self.countdown_at)
        head = self.ask if asking else f"ROUND {self.index + 1} OF {self.total}"
        fr.check_top(self.h_top, "pick-a-card header")
        hb = d.textbbox((0, 0), head, font=self.h_font)
        shadow_text(d, ((fr.w - (hb[2] - hb[0])) / 2 - hb[0], self.h_top),
                    head, self.h_font, br.primary)
        if asking and self.hint and (self.exit_at is None
                                     or t < self.exit_at):
            e = _ease_out(min(1.0, (t - self.countdown_at) / 0.30))
            layer = Image.new("RGBA", out.size, (0, 0, 0, 0))
            ld = ImageDraw.Draw(layer)
            nb = ld.textbbox((0, 0), self.hint, font=self.hint_font)
            shadow_text(ld, ((fr.w - (nb[2] - nb[0])) / 2 - nb[0],
                             self.hint_y), self.hint, self.hint_font, br.ink,
                        alpha=int(230 * e))
            out.alpha_composite(layer)

        self._draw_card(out, 0, t)
        self._draw_card(out, 1, t)
        self._draw_heart(out, t)
        self.ring._draw_ring(out, t)
        return out.convert("RGB")


    def _draw_heart(self, out: Image.Image, t: float) -> None:
        """The divider: in with the first card, out for the ring, out with
        the swipe."""
        if self.heart is None:
            return
        due = self.reveals[0] if self.reveals else self.at(0.1)
        if t < due:
            return
        if self.countdown_at is not None and self.countdown_at <= t \
                <= self.countdown_at + self.rnd.countdown:
            return
        a = _ease_out(min(1.0, (t - due) / self.POP))
        if self.exit_at is not None and t >= self.exit_at:
            a *= max(0.0, 1.0 - (t - self.exit_at) / (EXIT * 0.4))
        if a <= 0:
            return
        img = self.heart
        if a < 0.999:
            img = img.copy()
            img.putalpha(img.getchannel("A").point(lambda v: int(v * a)))
        out.alpha_composite(img, self.heart_at)


def _composite_clipped(out: Image.Image, img: Image.Image, x: int, y: int
                       ) -> None:
    """`alpha_composite` for a sprite partly off-frame - PIL refuses those."""
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(out.width, x + img.width), min(out.height, y + img.height)
    if x1 <= x0 or y1 <= y0:
        return
    out.alpha_composite(img.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


def _check_fits(rounds: list[Round], frame: Frame, brand: Brand) -> None:
    """Raise on a card whose text needs a fourth line, before rendering."""
    probe = TruthDareShot(rounds[0], 0, len(rounds), frame=frame, brand=brand)
    for r in rounds:
        for i, text in enumerate(r.cards):
            n = probe.text_lines(text)
            if n > 3:
                raise ValueError(f"{r.labels[i]} needs {n} lines and a card "
                                 f"holds 3: {text!r}")


def render_truth_dare_short(rounds: list[Round], title: tuple, outro: tuple,
                            out: Path, workdir: Path, brand: Brand,
                            voice: str = "mia", frame: Frame = VERTICAL,
                            ask: str = "PICK ONE",
                            hint: str | None = "Pause if you need more time",
                            **kw) -> tuple[Path, float]:
    """One pick-a-card Short: a title card, `rounds`, an outro card.

    `title` is one sentence of `(caption, spoken)` chunks; the caption of the
    first is what the card shows, and the rest are spoken only - which is
    where the "pause if you need more time" instruction goes.
    """
    if not rounds:
        raise ValueError("a pick-a-card short needs at least one round")
    _check_fits(rounds, frame, brand)

    first = title[0]
    sentences: list[tuple] = [tuple(title)]
    shots: list[Shot] = [Shot(graphic="chapter", payload=(
        first if isinstance(first, str) else first[0], None))]
    gaps: list[float] = [TITLE_GAP]
    groups: list[tuple[Round, Shot, Shot]] = []
    state: dict[int, dict] = {}

    for n, r in enumerate(rounds):
        pair = []
        for i, g in ((0, CARD_GAP), (1, LEAD + r.countdown + TAIL + EXIT)):
            sh = Shot(graphic="truthdare", payload=([i],))
            sh.xfade = 0.0
            sentences.append((r.line(i),))
            shots.append(sh)
            gaps.append(g)
            state[id(sh)] = {"round": r, "index": n}
            pair.append(sh)
        groups.append((r, *pair))

    sentences.append(tuple(outro))
    shots.append(Shot(graphic="chapter", payload=(
        " ".join(c if isinstance(c, str) else c[0] for c in outro),)))
    gaps.append(GAP)

    cues: list[tuple[float, str]] = []

    def plan(planned: list[Shot], sents: list, captions: list) -> None:
        for n, (r, a, b) in enumerate(groups):
            reveals = [a.start, b.start]
            # The second card's trailing gap is LEAD + ring + TAIL + EXIT,
            # and its hold already runs to the next shot, so count back.
            exit_at = b.start + b.hold - EXIT
            countdown_at = exit_at - TAIL - r.countdown
            for sh in (a, b):
                state[id(sh)].update(reveals=reveals, exit_at=exit_at,
                                     countdown_at=countdown_at
                                     if sh is b else None)
            if n == 0:
                cues.append((max(0.0, a.start - WHOOSH_LEAD), "whoosh"))
            cues.append((a.start, "reveal"))
            cues.append((b.start, "reveal"))
            k = int(round(r.countdown))
            for j in range(k):
                cues.append((countdown_at + j,
                             "clock_final" if j == k - 1 else "clock"))
            cues.append((exit_at, "whoosh"))

    def factory(sh: Shot, fr: Frame):
        st = state.get(id(sh))
        if st is None:
            return _short_factory(sh, fr, brand)
        return TruthDareShot(st["round"], st["index"], len(rounds),
                             reveals=st.get("reveals"),
                             countdown_at=st.get("countdown_at"),
                             exit_at=st.get("exit_at"), ask=ask, hint=hint,
                             start=sh.start, hold=sh.hold, frame=fr,
                             brand=brand)

    kw.setdefault("music_lufs", MUSIC_LUFS)
    return render_crypto_short(
        sentences, shots, out, workdir, voice=voice, frame=frame, brand=brand,
        mark=brand.mark(int(frame.logo_w * brand.mark_scale)),
        gap=gaps, run_break=RUN_BREAK,
        factory=factory, plan_graphics=plan, cues=lambda planned: sorted(cues),
        **kw)
