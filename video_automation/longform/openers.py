"""Opening variants, so every video does not open the same way.

`overlay.HookOverlay` (the redacted headline) is the default and the control.
These four are the alternatives, chosen by the **shape of the topic** rather
than by taste - see `docs/video/shorts.md`, "Choosing the opener".

| class | opens on | the topic it fits |
| --- | --- | --- |
| `Counter` | a figure spinning and slamming to a stop | the payoff is a number or a scale |
| `Stamp` | a belief quoted, then stamped with a verdict | a claim that is wrong, half true, or confirmed |
| `Split` | two options either side of a divider | a comparison |
| `Search` | the query typing itself into a search bar | a search-intent question |
| `Flash` | a second of a later moment, then a rewind | the payoff is a strong *picture* later in the cut |

They share the shipped hook's language on purpose - Arial Black upper case,
the brand pill, the camera punch-in, the `hook_*` sound kit - so the channel
still reads as one thing while the first two seconds differ.

**Timing comes from the narration, not from a guess.** Anything that lands
(the number, the stamp, the verdict) takes `at_word=`: the renderer finds when
that word is spoken and lands the beat on that frame, exactly as the redacted
hook reveals on its own word. `at=` forces a second instead.

Each class is built in two steps: the script constructs it with content only,
and the renderer calls `build(frame, brand, captions)` once the narration has
been measured. After that it is an overlay like any other - `.draw(pic, t)`,
`.cues()`, `.end`.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..core.frame import VERTICAL, Frame
from .overlay import _ease_out, _ease_out_back

# Verdict words that read as a refutation rather than a confirmation. The
# stamp colours itself from this rather than asking the script to pick a
# colour, so "MYTH" is never accidentally green.
NEGATIVE = {"MYTH", "FALSE", "WRONG", "SCAM", "HYPE", "NOPE", "BUSTED", "NOT TRUE"}
POSITIVE = {"TRUE", "VERIFIED", "REAL", "CONFIRMED", "FACT", "LEGIT", "YES"}


def _font(size: int):
    from ..core.vertical import FONT_KARAOKE_BOX, FONT_KARAOKE_BOX_INDEX
    return ImageFont.truetype(FONT_KARAOKE_BOX, size, index=FONT_KARAOKE_BOX_INDEX)


def word_time(word: str, captions: list, fallback: float,
              earliest: float = 1.0, latest: float = 7.0) -> float:
    """When the narration says `word`. Falls back with a printed warning.

    The same machinery the redacted hook uses, factored out: caption spans are
    real timestamps and the per-word split inside one is proportional, which
    is accurate to well under a frame at this chunk length.
    """
    import re
    from ..crypto.build import _word_spans          # lazy: avoids a cycle

    key = re.sub(r"[^a-z0-9]", "", word.split()[0].lower())
    for c in captions:
        for w, (t0, _t1) in zip(c.text.split(),
                                _word_spans(c.text, c.start, c.end, c.speech_end)):
            if t0 >= earliest and re.sub(r"[^a-z0-9]", "", w.lower()) == key:
                if t0 <= latest:
                    return t0
                break
    print(f"opener: '{key}' is not spoken between {earliest:.1f}s and "
          f"{latest:.0f}s - landing at {fallback:.1f}s instead. Say it in "
          f"sentence 2 so the beat lands on the word.")
    return fallback


class _Opener:
    """Shared scaffolding: the punch-in, the band, the entrance and the exit.

    Subclasses implement `_content(t)` - a full-frame RGBA layer - and set
    `self.block_h` / `self.centre` so the band fits what they drew.
    """

    PUNCH = 0.35
    SLAM = 0.30
    EXIT = 0.28

    land: float = 2.6
    hold: float = 0.9
    punch: bool = True

    def __init__(self, *, at_word: str | None = None, at: float | None = None,
                 hold: float = 0.9, punch: bool = True):
        self.at_word, self.at_fixed, self.hold, self.punch = at_word, at, hold, punch
        self.frame: Frame = VERTICAL
        self.accent = (229, 194, 0)
        self.built = False

    # -- construction ----------------------------------------------------
    def build(self, frame: Frame, brand, captions: list):
        self.frame = frame
        self.accent = brand.primary
        self.brand = brand
        fallback = self.at_fixed if self.at_fixed is not None else 2.6
        self.land = (self.at_fixed if self.at_fixed is not None
                     else word_time(self.at_word, captions, fallback)
                     if self.at_word else fallback)
        self.exit_at = self.land + self.hold
        self.start, self.end = 0.0, self.exit_at + self.EXIT
        self._layout()
        self.built = True
        return self

    def _layout(self) -> None:
        self.centre = self.frame.h * (0.34 if self.frame.h > self.frame.w else 0.26)
        self.block_h = 360

    # -- drawing ---------------------------------------------------------
    def _band(self) -> tuple[Image.Image, int]:
        spread = 150
        bh = int(self.block_h) + spread * 2
        yy = np.linspace(-1, 1, bh)
        core = self.block_h / bh
        a = np.clip((1 - np.abs(yy)) / max(1e-6, 1 - core), 0, 1) ** 1.3 * 125
        im = Image.new("RGBA", (self.frame.w, bh), (0, 0, 0, 255))
        im.putalpha(Image.fromarray(
            np.repeat(a.astype(np.uint8)[:, None], self.frame.w, 1), "L"))
        return im, int(self.centre - self.block_h / 2) - spread

    def _entrance_scale(self, t: float) -> float:
        return 1.0 if t >= self.SLAM else 1.12 - 0.12 * _ease_out_back(t / self.SLAM)

    def cues(self) -> list[tuple[float, str]]:
        return [(0.0, "hook_slam"), (self.land, "hook_pop"),
                (self.exit_at, "hook_swish")]

    def _content(self, t: float) -> Image.Image:
        raise NotImplementedError

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return pic
        W, H = self.frame.w, self.frame.h
        if self.punch and t < self.PUNCH:
            z = 1.14 - 0.14 * _ease_out(t / self.PUNCH)
            cw, ch = int(W / z), int(H / z)
            pic = pic.crop(((W - cw) // 2, (H - ch) // 2, (W - cw) // 2 + cw,
                            (H - ch) // 2 + ch)).resize((W, H), Image.BILINEAR)
        out = pic.convert("RGBA")

        a, dy = 1.0, 0
        if t >= self.exit_at:
            q = _ease_out((t - self.exit_at) / self.EXIT)
            a, dy = 1.0 - q, -int(70 * q)

        band, band_top = self._band()
        if a < 1.0:
            band = band.copy()
            band.putalpha(band.split()[3].point(lambda v: int(v * a)))
        out.alpha_composite(band, (0, max(0, band_top + dy)))

        layer = self._content(t)
        if a < 1.0:
            layer.putalpha(layer.split()[3].point(lambda v: int(v * a)))
            shifted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            shifted.paste(layer, (0, dy))      # slide up; never wrap
            layer = shifted
        out.alpha_composite(layer)
        return out.convert("RGB")

    # -- helpers for subclasses -----------------------------------------
    def _lines(self, img, lines, cy, size, *, pill=(), colour=(255, 255, 255)):
        d = ImageDraw.Draw(img)
        f = _font(size)
        lh = int(size * 1.22)
        top = cy - lh * len(lines) / 2
        stroke = max(4, size // 14)
        for i, ln in enumerate(lines):
            w = d.textlength(ln, font=f)
            x, y = (self.frame.w - w) / 2, top + i * lh
            if i in pill:
                asc = f.getbbox("A")[1]
                cap = f.getbbox("A")[3] - asc
                pad = max(10, size // 7)
                d.rounded_rectangle((x - pad, y + asc - pad * 0.7, x + w + pad,
                                     y + asc + cap + pad * 0.7),
                                    radius=max(8, size // 7), fill=self.accent + (255,))
                d.text((x, y), ln, font=f, fill=(14, 14, 14, 255))
            else:
                d.text((x, y), ln, font=f, fill=colour + (255,),
                       stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        return img


class Counter(_Opener):
    """A figure spins and slams to a stop on the number that matters.

    For a topic whose payoff *is* a number - four billion dollars with no
    blockchain, ninety two decibels, three days of ringing. The spin is the
    open loop and it is very short: the digits are unreadable, which is the
    point, and the moment they stop is the answer.
    """

    def __init__(self, final: str, caption: str = "", *, spin_from: str = "",
                 **kw):
        super().__init__(**kw)
        self.final, self.caption, self.spin_from = final, caption, spin_from

    def _layout(self):
        super()._layout()
        self.block_h = 300 if not self.caption else 380

    def cues(self):
        c = super().cues()
        # A tick per spin frame group: the sound of a counter running.
        c += [(0.45 + i * 0.16, "clock") for i in range(int((self.land - 0.6) / 0.16))]
        return c

    def _content(self, t):
        lay = Image.new("RGBA", (self.frame.w, self.frame.h), (0, 0, 0, 0))
        size = 104 if self.frame.h > self.frame.w else 120
        if t < self.land:
            rng = np.random.default_rng(int(t * 24))
            digits = "".join(str(rng.integers(0, 10)) if ch.isdigit() else ch
                             for ch in (self.spin_from or self.final))
            self._lines(lay, [digits], self.centre - 40,
                        int(size * self._entrance_scale(t)))
            if self.caption:
                self._lines(lay, [self.caption.upper()], self.centre + 110, 52)
        else:
            k = min(1.0, (t - self.land) / 0.22)
            jx = int(8 * (1 - k) * np.sin(t * 90))
            tmp = Image.new("RGBA", (self.frame.w, self.frame.h), (0, 0, 0, 0))
            self._lines(tmp, [self.final], self.centre - 40,
                        int(size * (1.0 + 0.10 * (1 - k))), pill=(0,))
            if self.caption:
                self._lines(tmp, [self.caption.upper()], self.centre + 110, 52)
            lay.alpha_composite(tmp, (jx, 0))
        return lay


class Stamp(_Opener):
    """A belief, quoted - then a verdict stamped across it.

    The channel's best-performing format made visible: name the thing the
    viewer believes, then overturn it. The verdict word is free text, so the
    same opener serves a refutation ("MYTH", "WRONG", "SCAM") and a
    confirmation ("TRUE", "VERIFIED") - the colour follows the word, from
    `NEGATIVE` / `POSITIVE` above, and `tone=` overrides it.

    **On the tinnitus channel a verdict must be about a claim, never about an
    outcome** - stamping "TRUE" over "it never goes away" is a prognosis.
    """

    def __init__(self, quote: str, verdict: str = "MYTH", *,
                 tone: str | None = None, **kw):
        super().__init__(**kw)
        self.quote, self.verdict = quote, verdict.upper()
        self.tone = tone

    def _layout(self):
        super()._layout()
        f = _font(78)
        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        words, line, self.quote_lines = self.quote.upper().split(), "", []
        for w in words:
            trial = (line + " " + w).strip()
            if d.textlength(f'"{trial}"', font=f) > self.frame.w - 190 and line:
                self.quote_lines.append(line)
                line = w
            else:
                line = trial
        if line:
            self.quote_lines.append(line)
        self.quote_lines[0] = '"' + self.quote_lines[0]
        self.quote_lines[-1] = self.quote_lines[-1] + '"'
        self.block_h = 78 * 1.22 * len(self.quote_lines) + 240

        colour = (self.brand.positive if (self.tone == "positive" or
                  (self.tone is None and self.verdict in POSITIVE))
                  else self.brand.negative)
        # **Measure the text, then draw the box around it.** The first cut
        # drew a fixed box and centred the word inside it separately, so the
        # word hung outside its own border - which the user caught.
        fs = _font(120)
        tw = d.textlength(self.verdict, font=fs)
        bbox = fs.getbbox(self.verdict)
        th = bbox[3] - bbox[1]
        pad_x, pad_y = 56, 40
        w, h = int(tw + pad_x * 2), int(th + pad_y * 2)
        st = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
        ds = ImageDraw.Draw(st)
        ds.rounded_rectangle((20, 20, 20 + w, 20 + h), radius=16,
                             outline=colour + (255,), width=12)
        ds.text((20 + pad_x, 20 + pad_y - bbox[1]), self.verdict, font=fs,
                fill=colour + (255,))
        self.stamp = st.rotate(11, resample=Image.BICUBIC, expand=True)

    def cues(self):
        return [(0.0, "hook_slam"), (max(0.3, self.land - 1.0), "hook_swell"),
                (self.land, "impact"), (self.land + 0.02, "hook_pop"),
                (self.exit_at, "hook_swish")]

    def _content(self, t):
        lay = Image.new("RGBA", (self.frame.w, self.frame.h), (0, 0, 0, 0))
        quote_cy = self.centre - 70
        self._lines(lay, self.quote_lines, quote_cy,
                    int(78 * self._entrance_scale(t)))
        if t >= self.land:
            k = _ease_out(min(1.0, (t - self.land) / 0.18))
            sc = (2.4 - 1.4 * k) * 0.92
            st = self.stamp
            nw, nh = int(st.width * sc), int(st.height * sc)
            st = st.resize((max(1, nw), max(1, nh)), Image.BILINEAR)
            if k < 1.0:
                st.putalpha(st.split()[3].point(lambda v: int(v * (0.35 + 0.65 * k))))
            # Below the quote, never across it.
            y = int(quote_cy + 78 * 1.22 * len(self.quote_lines) / 2 + 40)
            lay.alpha_composite(st, ((self.frame.w - nw) // 2, y))
        return lay


class Split(_Opener):
    """Two options, a divider, and a question that stays open.

    For comparisons. The verdict is **not** given here - it lands later, on
    `at_word`, when the narration names the winner, which is what keeps the
    opener from answering its own question in two seconds (the fault the
    sentence-2 rule records). Pass `winner="left"` or `"right"` with the word
    that names it; omit both to leave it open for the whole video.
    """

    def __init__(self, left: str, right: str, question: str = "",
                 *, winner: str | None = None, **kw):
        super().__init__(**kw)
        self.left, self.right, self.question = left.upper(), right.upper(), question
        self.winner = winner

    def _layout(self):
        super()._layout()
        self.block_h = 460

    def cues(self):
        c = [(0.0, "hook_slam"), (0.25, "hook_swish"), (0.45, "hook_swish"),
             (self.exit_at, "hook_swish")]
        if self.winner:
            c += [(self.land, "hook_pop")]
        return c

    def _content(self, t):
        W = self.frame.w
        lay = Image.new("RGBA", (W, self.frame.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        k = _ease_out(min(1.0, t / 0.45))
        cy = self.centre
        d.line((W / 2, cy - 250 * k, W / 2, cy + 250 * k),
               fill=(255, 255, 255, 200), width=5)
        f = _font(64)
        for label, side in ((self.left, -1), (self.right, 1)):
            won = (self.winner == ("left" if side < 0 else "right")
                   and t >= self.land)
            for i, word in enumerate(label.split()):
                w = d.textlength(word, font=f)
                x = W / 2 + side * (W / 4) - w / 2 + side * (1 - k) * 260
                y = cy - 170 + i * 78
                if won:
                    pad = 16
                    asc = f.getbbox("A")[1]
                    cap = f.getbbox("A")[3] - asc
                    d.rounded_rectangle((x - pad, y + asc - 10, x + w + pad,
                                         y + asc + cap + 10), radius=12,
                                        fill=self.accent + (255,))
                    d.text((x, y), word, font=f, fill=(14, 14, 14, 255))
                else:
                    d.text((x, y), word, font=f, fill=(255, 255, 255, 255),
                           stroke_width=5, stroke_fill=(0, 0, 0, 255))
        fv = _font(56)
        vw = d.textlength("VS", font=fv)
        r = int(74 * (1.0 + 0.05 * np.sin(t * 5)))
        d.ellipse((W / 2 - r, cy - r, W / 2 + r, cy + r), fill=(14, 14, 14, 235),
                  outline=self.accent + (255,), width=6)
        d.text((W / 2 - vw / 2, cy - 32), "VS", font=fv, fill=self.accent + (255,))
        if self.question:
            self._lines(lay, [self.question.upper()], cy + 200, 54)
        return lay


class Search(_Opener):
    """The query types itself into a search bar. **The question only.**

    Most of the best titles on both channels already *are* the phrase someone
    types, so this shows the viewer their own question being asked. It shows
    no answer and no autocomplete suggestion - the answer is the video, and
    putting it on screen in the first two seconds is the "complete answer in
    sentence 2" mistake in picture form (the user's call, 2026-09-24).
    """

    CPS = 0.085          # seconds per character

    def __init__(self, query: str, **kw):
        super().__init__(**kw)
        self.query = query

    def _layout(self):
        super()._layout()
        self.block_h = 260
        # **Size the type to the bar, not the other way round.** The query is
        # a real search phrase and the longest ones ran under the magnifier;
        # the icon's column is reserved before the font is chosen.
        avail = (self.frame.w - 180) - 52 - 120
        self.size = 40
        while self.size > 24:
            f = _font(self.size)
            if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(
                    self.query.upper(), font=f) <= avail:
                break
            self.size -= 2
        # Type the whole query, then hold it; the land is the last keystroke
        # unless the script pinned one.
        typed = 0.3 + len(self.query) * self.CPS
        if self.at_word is None and self.at_fixed is None:
            self.land = typed
            self.exit_at = self.land + self.hold
            self.end = self.exit_at + self.EXIT

    def cues(self):
        n = int(len(self.query) / 3)
        c = [(0.0, "hook_slam"), (self.exit_at, "hook_swish")]
        c += [(0.35 + i * self.CPS * 3, "reveal") for i in range(n)]
        return c

    def _content(self, t):
        W = self.frame.w
        lay = Image.new("RGBA", (W, self.frame.h), (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        x0, x1 = 90, W - 90
        h = 110
        y = int(self.centre - h / 2)
        d.rounded_rectangle((x0, y, x1, y + h), radius=h // 2,
                            fill=(245, 245, 245, 245))
        f = _font(self.size)
        n = int(max(0.0, t - 0.3) / self.CPS)
        typed = self.query[:n].upper()
        d.text((x0 + 52, y + (h - self.size) / 2 - 4), typed, font=f,
               fill=(20, 20, 20, 255))
        if t % 0.7 < 0.35:
            cw = d.textlength(typed, font=f)
            d.rectangle((x0 + 56 + cw, y + 30, x0 + 60 + cw, y + h - 30),
                        fill=(20, 20, 20, 255))
        d.ellipse((x1 - 96, y + 34, x1 - 54, y + 76), outline=(90, 90, 90, 255), width=7)
        d.line((x1 - 60, y + 72, x1 - 42, y + 90), fill=(90, 90, 90, 255), width=7)
        return lay


class Flash(_Opener):
    """A second of a later moment, a rewind, then the line.

    For a cut whose payoff is a *picture* - a diagram, a dial, a bar chart.
    `image` is that moment: a site image, a rendered beat, or a frame grabbed
    from the footage. It plays for `flash` seconds behind a scrim, tears into
    a rewind, and the opening line lands after it.

    Use it sparingly. It spends a second of the first two on something the
    viewer cannot yet understand, which only pays if the picture is striking
    on its own.
    """

    CUT = 0.85
    BACK = 1.15

    def __init__(self, image: Path, line: str, tag: str = "LATER IN THIS VIDEO",
                 **kw):
        super().__init__(**kw)
        self.image, self.line, self.tag = Path(image), line, tag

    def _layout(self):
        super()._layout()
        self.block_h = 320
        # The line is not a reveal: it simply arrives once the rewind lands,
        # so the shared timings run from `BACK` rather than from zero.
        self.land = 0.0
        self.exit_at = 1.8
        self.end = self.BACK + self.exit_at + self.EXIT
        im = Image.open(self.image).convert("RGB")
        W, H = self.frame.w, self.frame.h
        scale = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
        self.flash_im = im.crop(((im.width - W) // 2, (im.height - H) // 2,
                                 (im.width - W) // 2 + W, (im.height - H) // 2 + H))
        f = _font(80)
        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        words, line, self.lines = self.line.upper().split(), "", []
        for w in words:
            trial = (line + " " + w).strip()
            if d.textlength(trial, font=f) > W - 180 and line:
                self.lines.append(line)
                line = w
            else:
                line = trial
        if line:
            self.lines.append(line)

    def cues(self):
        return [(0.0, "hook_pop"), (self.CUT, "hook_swish"),
                (self.BACK, "hook_slam"),
                (self.BACK + self.exit_at, "hook_swish")]

    def draw(self, pic: Image.Image, t: float) -> Image.Image:
        if not (self.start <= t < self.end):
            return pic
        W, H = self.frame.w, self.frame.h
        if t < self.CUT:
            out = self.flash_im.convert("RGBA")
            out.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 70)))
            chip = Image.new("RGBA", (560, 64), (0, 0, 0, 0))
            dc = ImageDraw.Draw(chip)
            dc.rounded_rectangle((0, 0, 559, 63), radius=32, fill=(14, 14, 14, 215))
            fw = dc.textlength(self.tag, font=_font(32))
            dc.text(((560 - fw) / 2, 14), self.tag, font=_font(32),
                    fill=(255, 255, 255, 235))
            out.alpha_composite(chip, ((W - 560) // 2, int(H * 0.18)))
            return out.convert("RGB")
        if t < self.BACK:
            k = (t - self.CUT) / (self.BACK - self.CUT)
            arr = np.asarray(pic.convert("RGBA")).copy()
            for i in range(6):
                rng = np.random.default_rng(int(t * 200) + i)
                y0 = int(rng.integers(0, H - 60))
                y1 = y0 + int(rng.integers(20, 160))
                arr[y0:y1] = np.roll(arr[y0:y1], int(rng.integers(-180, 180)), axis=1)
            arr[..., 0] = np.roll(arr[..., 0], 14, axis=1)
            out = Image.fromarray(arr, "RGBA")
            d = ImageDraw.Draw(out)
            fw = d.textlength("<<", font=_font(120))
            d.text(((W - fw) / 2, H * 0.32), "<<", font=_font(120),
                   fill=(255, 255, 255, int(255 * (1 - k))))
            return out.convert("RGB")
        return super().draw(pic, t - self.BACK)

    def _content(self, t):
        lay = Image.new("RGBA", (self.frame.w, self.frame.h), (0, 0, 0, 0))
        self._lines(lay, self.lines, self.centre, int(80 * self._entrance_scale(t)))
        return lay
