"""4-7-8 breathing + white noise, 20 minutes — long-form 16:9 sound therapy.

**A different breathing pattern from every other session on the channel, not
just a different bed.** `masking-breathing-5min.py` and the standard build are
both 4-in/6-out; this is 4-7-8 (inhale, hold, exhale) — Dr. Andrew Weil's
pattern, the one most people already know by name if they know any. Same
white-noise bed as the rejected 20-minute cut, same engine, but the pattern
itself is now what tells this session apart from the rest of the shelf rather
than the bed colour doing that work alone.

**This needed an engine change, not just new arguments at the call site.**
`longform/asmr.py`'s `_breath`/`render_loop`/`render_asmr_long` only knew
4-in/6-out — `INHALE`/`EXHALE` were module constants baked into the loop math,
with no hold phase at all. The short's engine already had a parameterised
`breathing_phases(cycles, inhale, hold, exhale)`; the long form's continuous
loop needed the same shape, so `_breath` now takes `inhale`/`hold`/`exhale`
(defaulting to 4/0/6, so every session built before this is byte-identical),
and a `hold` phase pins the ring at `r_max` with its own label, the same
inhale-hold-exhale order the short uses.

* **`inhale=4.0, hold=7.0, exhale=8.0`** — a 19s cycle, not the usual 10s.
* **`loop=57.0`** (three 19s cycles) instead of the usual 60s default — `loop`
  has to divide evenly by the pattern's own cycle length, and 57 does not
  divide by 60/10 conveniences the old default assumed away.
* **20 minutes: 30s intro, 1140s body, 30s outro.** The body is exactly twenty
  57s loops.
* **Generated white noise**, `soundbed.Bed(colour="white")` — 67% of its
  energy sits above 8 kHz, the band a high whistling tinnitus actually
  occupies, per `docs/video/projects/tinnitus.md`.
* **No medical claims.** The intro names the pattern and says how to set the
  level; it never promises what either one will do.

**The caption reads "4-7-8"; the voice does not.** Kokoro/espeak phonemizes
`4-7-8` literally — `espeak-ng --ipa "4-7-8"` returns `fˈɔːɹ dˈæʃ sˈɛvən dˈæʃ
ˈeɪt`, a spoken "dash" between every number. The intro's first line is a
`(caption, spoken)` pair so the on-screen text keeps the numerals and the
voice gets "four, seven, eight" instead — the same device `voice.md` documents
for `Binance`/`Bynanse` and for holding a word with punctuation rather than
respelling it.

**A second engine change: `nebula_canvas`/`_ring_sprite`/`render_loop`/
`render_bookend`/`render_asmr_long`/`render_session_thumb` all take an
optional `palette`.** Every session so far has used the app's own
purple/peach, hard-coded as module constants — fine for one session, wrong
once there is a shelf of them, because a viewer scanning the channel should
be able to tell two sessions apart without reading the title. `palette` is
`(bg_deep, nebula_a, nebula_b, ring)`; `None` keeps the exact colours every
prior build shipped with. This session passes a blue-toned alternative so it
reads as its own video rather than the purple one with a different number on
the ring.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/478-breathing-white-noise-20min.py
"""

from pathlib import Path

from video_automation.core import soundbed
from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb

DESKTOP = Path.home() / "Desktop"

MINUTES = 20.0
OUT = DESKTOP / "4-7-8 Breathing + White Noise for Tinnitus (20 Minutes).mp4"

BED = soundbed.Bed(colour="white", breathe=0.10, breathe_period=19.0)

INHALE, HOLD, EXHALE = 4.0, 7.0, 8.0
LOOP = INHALE + HOLD + EXHALE  # 19.0 — one full cycle

# Every other session on the channel defaults to seed 7 (the 5-minute masking
# cut included), which is the same nebula every time. A different seed is a
# different star field and cloud layout; the palette below is what actually
# changes the colour.
SEED = 42

# (bg_deep, nebula_a, nebula_b, ring) — a cool blue instead of the app's
# purple/peach, so this session is a different colour on sight, not just a
# different number on the same purple ring. bg_deep keeps roughly the same
# near-black luminance as the default so the "mostly void" composition in
# `nebula_canvas` still reads; nebula_a/b move the mid and bright clouds from
# violet to blue; ring is a pale ice-blue rather than peach.
PALETTE = ((8, 14, 24), (24, 64, 102), (150, 220, 255), (150, 220, 255))

# What the sound is, the one setting that matters, then the pattern by name
# and by count — a viewer who already knows 4-7-8 recognises it immediately,
# one who doesn't gets the numbers before the ring starts asking for them.
# The pattern's caption keeps the numerals; the spoken half drops the hyphens
# so Kokoro doesn't read "4-7-8" as "four dash seven dash eight" — see the
# module docstring.
INTRO = [
    ("Twenty minutes of white noise,",
     ("with 4-7-8 breathing.", "with four, seven, eight breathing.")),
    ("Set the volume just below your tinnitus.",),
    ("You should still hear it",
     "faintly underneath. That is the point.",),
    ("Then follow the circle.",
     "Four seconds in, hold for seven,",
     "eight seconds out.",),
]

# Not a subscribe card. A piece built to lower arousal cannot end by asking
# for something. No call to action, no music sting.
OUTRO = [
    ("That is twenty minutes.",),
    ("If it helped, start it again",
     "and take another round.",),
    ("There are other patterns and lengths",
     "on the channel for when you want them.",),
]

if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=Path("/tmp/tinnitus-long-asmr-478-white-20min"),
        brand=TINNITUS,
        minutes=MINUTES,
        bed=BED,
        intro=INTRO,
        outro=OUTRO,
        intro_len=34.0,
        outro_len=26.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE,
        seed=SEED, palette=PALETTE,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # `render_session_thumb`, not `render_thumb` — a session has no photograph.
    # Same seed and palette as the video, so it is a picture of this one.
    # Orange accent (not the format's usual cyan) reads against a blue nebula
    # the way peach read against purple — a warm number on a cool field.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="4-7-8 Breathing", pattern="4 in / 7 hold / 8 out",
        seed=SEED, palette=PALETTE, accent="orange")
    print(thumb)
