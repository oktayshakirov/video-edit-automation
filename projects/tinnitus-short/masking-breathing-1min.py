"""Thumbnail for the 1-minute masking + breathing short.

**This file only builds the thumbnail.** The short itself
(`VI_CrobXOFk`, "Tinnitus Masking Sound + Paced Breathing (1 Minute)") is
already live and predates the thumbnail work entirely — there is no local
build script for the video, only the shipped upload. What was missing was a
thumbnail to match `tinnitus-long/masking-breathing-5min.py`'s.

**Same materials as the long, reflowed to 9:16** via
`thumb.render_session_thumb_short` — the vertical sibling of
`render_session_thumb`. Same nebula seed, same headline
("Tinnitus Masking Sound"), same pattern chip ("4 in / 6 out"), same ring
device. Only the duration and its unit change: `minutes=1` prints "1 MINUTE",
singular, where the long form's "5" prints "MINUTES".

This is the session style, not the article-short style
(`render_short_thumb`, Arial Black, drop shadow, a bracketed accent phrase)
— a session has no photograph to crop, so the pairing rule here is "same
nebula and same ring", the session format's own equivalent of "same photo
and same headline".

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/masking-breathing-1min.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.thumb import render_session_thumb_short

OUT = Path.home() / "Desktop/tinnitus-masking-breathing-1min-thumb.jpg"

if __name__ == "__main__":
    thumb = render_session_thumb_short(
        OUT, TINNITUS, minutes=1,
        headline="Tinnitus Masking Sound", pattern="4 in / 6 out", seed=7)
    print(thumb)
