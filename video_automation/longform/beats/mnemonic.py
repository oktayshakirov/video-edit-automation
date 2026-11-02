"""`mnemonic` - 128 random bits becoming twelve words.

**Built for `what-is-a-seed-phrase` (2026-11-02), because the library could
not draw how a seed phrase is made.** The standout on the subject (CoinGecko,
"What Is A SEED Phrase?? How It Is Generated") is most replayed exactly where
it walks the bits into words, and its top comments are "confusing" and "can't
a hacker just try the words?" - the step a sentence cannot make vivid. Nothing
here drew a number becoming a word: `steps` is a procedure, `diagram` a chain
of boxes, `grid` a set.

Four reveals, four caption chunks in this order: the bits ("your wallet
flips a hundred and twenty-eight coins"), the checksum ("it adds four more
bits as a check, and cuts the line into twelve groups"), the numbers ("each
group is a number from zero to two thousand and forty-seven"), the words
("and each number picks one word from a fixed list"). On the first the grid
fills with flickering coin flips that settle row by row into the real bits;
on the second the four checksum cells set in white; on the third each row
reads out its number; on the fourth each number picks its word, row after
row.

**The phrase is real BIP39, never drawn by hand.** The payload is 32 hex
characters of entropy; the checksum, the indices and the words are computed
from the official English list (`assets/crypto/seed-phrase/`, its hash in
the CREDITS.md there), so every number on screen is the right one for its
word. A sceptical viewer can check it, and some will.

Same template as `quorum`, `blindsign` and `sweep`: line art in the brand
colour, one object per spoken phrase, one state change per phrase.

payload: (entropy, title)
  entropy  32 hex characters - 128 bits, a 12-word phrase
  title    the beat's kicker
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageDraw

from ...core.draw import ease_out, partial, shadow_text
from .base import Beat, _display, _font, _smooth

WORDLIST = (Path(__file__).resolve().parents[3]
            / "assets/crypto/seed-phrase/bip39-english.txt")

SETTLE_LEAD, SETTLE = 0.15, 1.70   # the flips settling: delay, length
ROW_LEAD, ROW_STEP = 0.15, 0.09    # a row's number or word: delay, stagger
FLICK = 0.07                       # how often an unsettled cell re-flips
CHECK = (232, 232, 232)            # the checksum cells - not a random bit


def settle_span(reveal: float) -> tuple[float, float]:
    """When the coin flips start settling and when the last one has."""
    t0 = reveal + SETTLE_LEAD
    return t0, t0 + SETTLE


def row_times(reveal: float, n: int = 12) -> list[float]:
    """When each row's number (or word) lands - shared with the cues."""
    return [reveal + ROW_LEAD + ROW_STEP * j for j in range(n)]


def phrase(entropy: str) -> tuple[str, list[int], list[str]]:
    """The 132 bits, the twelve indices and the twelve words for 128 bits of
    entropy, by BIP39: the checksum is the first 4 bits of its SHA-256."""
    raw = bytes.fromhex(entropy)
    if len(raw) != 16:
        raise ValueError(f"mnemonic wants 128 bits (32 hex), got {len(raw) * 8}")
    words = WORDLIST.read_text().split()
    if len(words) != 2048:
        raise ValueError(f"{WORDLIST} has {len(words)} words, not 2048")
    bits = "".join(f"{b:08b}" for b in raw)
    bits += f"{hashlib.sha256(raw).digest()[0]:08b}"[:4]
    idx = [int(bits[k:k + 11], 2) for k in range(0, 132, 11)]
    return bits, idx, [words[i] for i in idx]


class Mnemonic(Beat):

    EMBLEM = False

    def __init__(self, entropy: str, title: str = "", **kw):
        super().__init__(**kw)
        self.bits, self.idx, self.words = phrase(entropy)
        self.title = title
        p = self.portrait
        # One table, read left to right: row number, eleven bits, the number,
        # the word. Portrait keeps it inside x=940 - the platforms' button
        # rail starts past that on the lower half of the frame.
        if p:
            self.top, self.rh = 520, 84
            self.cell, self.pitch = 34, 40
            label_w, gap, num_w, self.word_w = 30, 26, 92, 236
            x0 = 96
            self.dsize, self.nsize, self.wsize, self.hsize = 20, 32, 36, 24
        else:
            self.top, self.rh = 318, 57
            self.cell, self.pitch = 42, 49
            label_w, gap, num_w, self.word_w = 44, 64, 112, 320
            x0 = (1920 - (label_w + 11 * 49 + 2 * gap + num_w + self.word_w)) // 2
            self.dsize, self.nsize, self.wsize, self.hsize = 24, 34, 38, 26
        self.lab_x = x0 + label_w - 14
        self.bit_x = x0 + label_w
        self.bit_end = self.bit_x + 11 * self.pitch - (self.pitch - self.cell)
        self.num_r = self.bit_end + gap + num_w
        self.word_x = self.num_r + gap

        d = ImageDraw.Draw(Image.new("RGB", (10, 10)))
        for w in self.words:
            tw = d.textlength(w, font=_display(self.wsize))
            if tw > self.word_w:
                raise ValueError(f"mnemonic word {w!r} is {tw:.0f}px and the "
                                 f"column has {self.word_w}px.")

    # --- pieces ----------------------------------------------------------------

    def _row_y(self, r: int) -> float:
        return self.top + r * self.rh

    def _cell(self, d, x, y, v, style, a):
        """One bit: `style` is 'set' (the real bit), 'flip' (still a coin in
        the air), 'check' (a checksum bit) or 'empty'."""
        s = self.cell
        prim = self.brand.primary
        df = _display(self.dsize)
        if style == "empty":
            d.rounded_rectangle([x, y, x + s, y + s], radius=7,
                                outline=(255, 255, 255, int(a * 0.18)), width=2)
            return
        if style == "flip":
            d.rounded_rectangle([x, y, x + s, y + s], radius=7,
                                outline=prim + (int(a * 0.55),), width=2)
            col = prim + (int(a * 0.70),)
        elif v == "1":
            fill = CHECK if style == "check" else prim
            d.rounded_rectangle([x, y, x + s, y + s], radius=7,
                                fill=fill + (a,))
            col = (18, 18, 18, a)
        else:
            edge = CHECK if style == "check" else (110, 110, 110)
            d.rounded_rectangle([x, y, x + s, y + s], radius=7,
                                outline=edge + (a,), width=2)
            col = edge + (a,)
        b = d.textbbox((0, 0), v, font=df)
        d.text((x + (s - (b[2] - b[0])) / 2 - b[0],
                y + (s - (b[3] - b[1])) / 2 - b[1]), v, font=df, fill=col)

    def _header(self, d, x, y, text, a, col=(150, 150, 150), right=False):
        hf = _font(self.hsize)
        if right:
            x -= d.textlength(text, font=hf)
        d.text((x, y), text, font=hf, fill=col + (a,))
        return x + d.textlength(text, font=hf)

    # --- the frame -------------------------------------------------------------

    def content(self, out: Image.Image, f: float) -> None:
        self.heading(out, self.title, f)
        rv = self.reveals or []
        if not rv:
            rv = [self.start + self.hold * k * 0.22 for k in range(4)]
        t = self.at(f)
        if t < rv[0]:
            return
        prim = self.brand.primary
        layer = Image.new("RGBA", self.frame.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer, "RGBA")

        e0 = min(1.0, (t - rv[0]) / 0.35)
        a0 = int(255 * e0)
        s0, s1 = settle_span(rv[0])
        # Settled cells sweep row by row; until then a cell is still a coin
        # in the air, re-flipped every FLICK seconds from a fixed hash so a
        # re-render draws the same flips.
        settled = int(128 * _smooth((t - s0) / (s1 - s0))) if t >= s0 else 0
        tick = int(t / FLICK)
        check_e = (min(1.0, max(0.0, (t - rv[1] - 0.15) / 0.3))
                   if len(rv) > 1 else 0.0)

        hy = self.top - (44 if self.portrait else 46)
        end = self._header(d, self.bit_x, hy, "RANDOM BITS", a0)
        if check_e > 0:
            self._header(d, end + 10, hy, "+ CHECKSUM", int(255 * check_e),
                         col=CHECK)

        lf = _font(self.hsize)
        for r in range(12):
            y = self._row_y(r)
            lab = str(r + 1)
            d.text((self.lab_x - d.textlength(lab, font=lf),
                    y + (self.cell - self.hsize) / 2 - 2), lab, font=lf,
                   fill=(120, 120, 120, a0))
            for c in range(11):
                k = r * 11 + c
                x = self.bit_x + c * self.pitch
                if k >= 128:
                    if check_e > 0:
                        self._cell(d, x, y, self.bits[k], "check",
                                   int(255 * check_e))
                    else:
                        self._cell(d, x, y, "", "empty", a0)
                elif k < settled:
                    self._cell(d, x, y, self.bits[k], "set", a0)
                else:
                    h = ((k * 73856093) ^ (tick * 19349663)) & 0xffffffff
                    h = ((h ^ (h >> 13)) * 1274126177) & 0xffffffff
                    v = str((h >> 16) & 1)
                    self._cell(d, x, y, v, "flip", a0)

        # 2 - the numbers, row by row.
        if len(rv) > 2 and t >= rv[2]:
            self._header(d, self.num_r, hy, "NUMBER", 255, right=True)
            nf = _display(self.nsize)
            for r, w in enumerate(row_times(rv[2])):
                if t < w:
                    continue
                e = ease_out((t - w) / 0.22)
                y = self._row_y(r) + self.cell / 2
                partial(d, [(self.bit_end + 10, y), (self.num_r - 104, y)],
                        e, (90, 90, 90), 2)
                s = str(self.idx[r])
                b = d.textbbox((0, 0), s, font=nf)
                shadow_text(d, (self.num_r - (b[2] - b[0]) - b[0],
                                y - (b[3] - b[1]) / 2 - b[1] + 8 * (1 - e)),
                            s, nf, (255, 255, 255, int(255 * e)),
                            alpha=int(255 * e))

        # 3 - the words: each number picks its word.
        if len(rv) > 3 and t >= rv[3]:
            self._header(d, self.word_x, hy, "WORD", 255)
            wf = _display(self.wsize)
            for r, w in enumerate(row_times(rv[3])):
                if t < w:
                    continue
                e = ease_out((t - w) / 0.24)
                y = self._row_y(r) + self.cell / 2
                partial(d, [(self.num_r + 10, y), (self.word_x - 12, y)],
                        e, prim, 3)
                s = self.words[r]
                b = d.textbbox((0, 0), s, font=wf)
                shadow_text(d, (self.word_x + 14 * (1 - e) - b[0],
                                y - (b[3] - b[1]) / 2 - b[1]),
                            s, wf, prim + (int(255 * e),), alpha=int(255 * e))

        rise = int(18 * (1 - ease_out(e0)))
        out.paste(layer, (0, rise), layer)
