"""Type-on titles: one character schedule for the picture and the sound.

A chapter card or an opener title types itself out behind a caret, the way a
terminal or a code tutorial does, with a soft digital key click under every
character. The narration still reads the line as before - the typing is a
picture of the sentence arriving, not a replacement for saying it.

**The schedule is the whole contract.** The beat that draws the type and the
cue list that places the clicks both call `schedule()` with the same text and
the same start, so a click cannot land on a frame where nothing appeared. That
is the rule `_cues` already follows for marks and reveals, applied per glyph.

The rhythm is even with a small fixed jitter rather than metronomic: a perfectly
regular click train reads as a machine gun, and a random one reads as a person.
The jitter is seeded from the text, so a re-render is byte-identical.
"""

from __future__ import annotations

import zlib

import numpy as np

CPS = 24.0              # characters per second at full speed
MIN_DUR = 0.45          # a two-word card still reads as typing, not a pop
JITTER = 0.28           # +- fraction of one interval
PAUSE = {" ": 1.0, ",": 2.2, ".": 2.6, "?": 2.6, "!": 2.6, ":": 2.0, "-": 1.4}
BLINK = 1.06            # the caret's period once typing is done (530ms on/off)
KEY_VARIANTS = 4        # `sfx.key0`..`key3`, cycled so no two neighbours match


def schedule(text: str, start: float, max_dur: float | None = None,
             cps: float = CPS) -> list[float]:
    """When each character of `text` appears, in absolute seconds.

    `max_dur` caps the whole run: a long title types faster rather than
    overrunning the window it has. A short one types at `cps`, never slower,
    so short and long cards share one speed wherever they can.
    """
    if not text:
        return []
    rng = np.random.default_rng(zlib.crc32(text.encode()))
    weights = []
    for i, ch in enumerate(text):
        # A pause belongs *after* punctuation, so it is charged to the next
        # character rather than delaying the comma itself.
        w = PAUSE.get(text[i - 1], 1.0) if i else 1.0
        weights.append(w * (1.0 + rng.uniform(-JITTER, JITTER)))
    w = np.array(weights)
    w[0] = 0.0                                  # first glyph on the start
    dur = max(MIN_DUR, (len(text) - 1) / cps) if len(text) > 1 else 0.0
    if max_dur is not None:
        dur = min(dur, max(0.0, max_dur))
    steps = np.cumsum(w)
    if steps[-1] > 0:
        steps *= dur / steps[-1]
    return [start + float(s) for s in steps]


def shown(times: list[float], t: float) -> int:
    """How many characters are on screen at `t`."""
    return int(np.searchsorted(np.asarray(times), t, side="right"))


def caret_on(times: list[float], t: float) -> bool:
    """Solid while typing, then blinking - the cursor waiting for more."""
    if not times or t < times[0]:
        return False
    done = times[-1]
    if t <= done + 0.12:
        return True
    return ((t - done) % BLINK) < BLINK / 2


def cues(text: str, times: list[float]) -> list[tuple[float, str]]:
    """A key click per visible character. Spaces are silent - a real spacebar
    is a thud, and a thud every word is the part that would nag."""
    out, k = [], 0
    for ch, t in zip(text, times):
        if ch.isspace():
            continue
        out.append((t, f"key{k % KEY_VARIANTS}"))
        k += 1
    return out


# --- the two uses -----------------------------------------------------------

CARD_LEAD = 0.10        # after the card's own cut, so the click is on a frame
CARD_SHARE = 0.62       # of the card's window the typing may take, at most


# The band card opens its band before any type, so it starts typing later.
LEADS = {"type": CARD_LEAD, "band": 0.42}


def card_schedule(title: str, start: float, hold: float,
                  style: str = "type") -> list[float]:
    """The chapter card's schedule, shared by `ChapterCard` and `_cues`."""
    lead = LEADS.get(style, CARD_LEAD)
    return schedule(title, start + lead, max_dur=hold * CARD_SHARE - lead
                    + CARD_LEAD)


def card_cues(payload: tuple, start: float, hold: float) -> list:
    """Key clicks for a chapter shot, read off its payload the way the beat
    reads it: `(title, number, style, index)`, the last two optional."""
    title = payload[0]
    style = payload[2] if len(payload) > 2 and payload[2] else "type"
    return cues(title, card_schedule(title, start, hold, style))


def lines_shown(lines: list[str], n: int) -> list[str]:
    """`n` characters of the source text, split back onto wrapped lines.

    `wrap` breaks on single spaces and drops them, so each line boundary
    consumes one source character. Counting against the source string - not
    the joined lines - is what keeps the schedule and the cues independent of
    how the title happened to wrap.
    """
    out = []
    for i, ln in enumerate(lines):
        if n <= 0:
            break
        out.append(ln[:n])
        n -= len(ln) + (1 if i < len(lines) - 1 else 0)
    return out
