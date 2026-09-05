"""4-7-8 breathing + white noise — vertical Short, the long form's companion.

**The Short version of `tinnitus-long/478-breathing-white-noise-20min.py`,
not a trailer for it.** Same pattern (4-7-8), same generated white-noise bed,
same blue nebula palette, same seed — a viewer who has seen one recognises
the other as the same piece at a different length, the way the format's own
rule for an article pair works.

**First real build of `render_asmr_short`'s generated-bed path.** The function
only knew `(low, high)` — the brand's own album MP3s, layered by `render_bed`
— and both files are gone from disk (confirmed: neither exists on the
Desktop any more), so a fresh ASMR short could not be rendered at all before
this. `render_asmr_short` now also takes `bed: soundbed.Bed | None`, generated
and loudness-matched (`loudnorm=I=-23`, the same fade lengths `render_bed`
uses) so the sidechain duck against the voice behaves identically either way.
`render_visual` also takes the same `palette` the long form does, so the two
share a nebula colour instead of the short defaulting back to purple.

* **`cycles=2` at 4-7-8** — a 38s breathing block, the natural length for a
  ~55-60s short; three cycles (57s) would leave no room for the intro/outro.
* **The intro's "4-7-8" is a `(caption, spoken)` pair**, same fix as the long
  form: Kokoro/espeak reads a bare `4-7-8` as "four dash seven dash eight".
* **No CTA.** A piece built to lower arousal doesn't end by asking for
  something — the outro just points at the full session on the channel.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/478-breathing-white-noise-short.py
"""

from pathlib import Path

from video_automation.core import soundbed
from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short
from video_automation.tinnitus.asmr import render_asmr_short

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "4-7-8 Breathing + White Noise for Tinnitus (Short).mp4"

BED = soundbed.Bed(colour="white", breathe=0.10, breathe_period=19.0)

INHALE, HOLD, EXHALE, CYCLES = 4.0, 7.0, 8.0, 2

# Same seed and palette as the long form, so this reads as the same video at
# a different length rather than a re-skin.
SEED = 42
PALETTE = ((8, 14, 24), (24, 64, 102), (150, 220, 255), (150, 220, 255))

# Opens on the hook, no lead-in silence. The caption keeps "4-7-8"; the voice
# gets "four, seven, eight" — see the module docstring.
INTRO = [
    (("4-7-8 breathing,", "Four, seven, eight breathing,"),
     "with white noise underneath.",),
    ("Set it just below your tinnitus,",
     "so you can still hear it faintly.",),
]

# One closing line, nothing after it — not a subscribe card.
OUTRO = [
    ("There's a full twenty-minute version",
     "of this on the channel.",),
]

if __name__ == "__main__":
    out, total = render_asmr_short(
        INTRO, OUTRO, OUT, Path("/tmp/tinnitus-short-asmr-478-white"),
        bed=BED,
        cycles=CYCLES, inhale=INHALE, hold=HOLD, exhale=EXHALE,
        seed=SEED, palette=PALETTE,
    )
    print(out, f"{total:.1f}s")

    minutes = max(1, round(total / 60))
    thumb = render_session_thumb_short(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=minutes,
        headline="4-7-8 Breathing", pattern="4 in / 7 hold / 8 out",
        seed=SEED, palette=PALETTE, accent="orange")
    print(thumb)
