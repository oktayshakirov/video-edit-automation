"""Next Trick, silent — the same line as a small quote card, no voice.

The user found leo too chill for this line and pointed at a TikTok reference
(122K likes): a small block of plain white type, four or five short lines,
centred, no box and no stroke, over a calm landscape. This is that card on
the same Sunset 5 crop as next-trick.py, cut to ~6.5s.

White is forced (`bg_luma=0` picks white ink with the dark halo) because the
reference is white; the halo is what holds it over the bright sky.
"""

from pathlib import Path

from video_automation.core.vertical import FONT_SIMPLE, render_short, render_text_png

SOURCE_POST = None                      # off-site: the user's own line, no article

FOOT = Path("~/Desktop/Drone Videos/Footage/Berlin 26 1:4").expanduser()
SRC = FOOT / "Sunset 5.mp4"
OUT = Path("~/Desktop/next-trick-silent.mp4").expanduser()
WORK = Path("~/Desktop/.work-next-trick-silent").expanduser()

BOX = (1744, 0, 1216, 2160)             # same 9:16 window as next-trick.py
START, DURATION = 0.0, 6.5

TEXT = ("And for my next trick, I’m going to set a goal, achieve it, "
        "feel nothing and immediately proceed to set another one.")

SIZE = 32                               # the reference's ~28px, a touch up for 1080
MAX_W = 330                             # narrow block: five or six short lines
Y_FRAC = 0.30                           # the cloud band; at 0.40 the last lines washed into the glow
FONT_INDEX = 5                          # Avenir Next Medium, lighter than the karaoke Demi Bold


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    png = render_text_png(TEXT, WORK / "card.png", size=SIZE, bg_luma=0.0,
                          font_path=FONT_SIMPLE, font_index=FONT_INDEX,
                          y_frac=Y_FRAC, max_w=MAX_W)
    render_short(SRC, OUT, START, DURATION, BOX, png)
    print(OUT)


if __name__ == "__main__":
    main()
