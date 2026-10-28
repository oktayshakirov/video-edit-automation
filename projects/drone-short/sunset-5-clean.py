"""Sunset 5, clean — the vertical crop with no text and no voice.

The editor rejected both the narrated and the silent-card cuts of Next Trick
and will add their own text and audio in-app. Same 9:16 window as
next-trick.py, ~13.5s, ungraded, no audio track.
"""

from pathlib import Path

from video_automation.core.vertical import render_short

FOOT = Path("~/Desktop/Drone Videos/Footage/Berlin 26 1:4").expanduser()
SRC = FOOT / "Sunset 5.mp4"
OUT = Path("~/Desktop/sunset-5-vertical.mp4").expanduser()

BOX = (1744, 0, 1216, 2160)             # 9:16 full height, sun at x~2350
START, DURATION = 0.0, 13.5


def main() -> None:
    render_short(SRC, OUT, START, DURATION, BOX, None)
    print(OUT)


if __name__ == "__main__":
    main()
