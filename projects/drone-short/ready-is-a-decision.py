"""Ready Is a Decision — stacked vertical quote, one Berlin sunset clip.

A test of a smaller caption: the editor noticed the quote shorts with smaller
type pull more views, so this is You Are the Problem's ink karaoke (Iowan
italic, the spoken word tinted, leo) with the body at 36px instead of 44 and
no set-piece word, so nothing on screen is set larger than the test size.

One clip, two tiles: Sunset 5 is a slow push over the Havel at sundown, so
the top tile takes the pink cloud field on the left and the bottom tile the
sun on the horizon with the lake to its right. The regions do not overlap,
so it reads as two pictures rather than one picture twice.

Ungraded, like the other Berlin 26 sunset cuts: the footage is already rich.
"""

from pathlib import Path

from video_automation.core.voiceover import render_narrated_stack, profile_args

SOURCE_POST = None                      # off-site: the editor's own line, no article

FOOT = Path("~/Desktop/Drone Videos/Footage/Berlin 26 1:4").expanduser()
SRC = FOOT / "Sunset 5.mp4"
OUT = Path("~/Desktop/ready-is-a-decision.mp4").expanduser()
WORK = Path("~/Desktop/.work-ready-is-a-decision").expanduser()

# 1080x910 tile aspect, (x, y, w, h) in 4K source pixels
BOX_TOP = (200, 0, 1400, 1180)          # clouds only; horizon sits at y~1215
BOX_BOTTOM = (1700, 900, 1400, 1180)    # sun at x~2350, y~1215; lake on the right

SIZE = 36                               # the test: down from FONT_QUOTE_SIZE 44

GAP = [0.8, 1.0, 0.65]         # longest beat lands before the kicker
TAIL = 1.2

SENTENCES = [
    [("you'll never feel ready,", "you'll never feel ready,")],
    [("because ready", "because ready"),
     ("isn't a feeling.", "isn't a feeling.")],
    [("it's a decision.", "it's a decision.")],
]


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    out, total = render_narrated_stack(
        (SRC, 0.0, BOX_TOP), (SRC, 0.0, BOX_BOTTOM),
        OUT, SENTENCES, WORK,
        font_size=SIZE,
        gap=GAP, tail=TAIL, **profile_args("leo"))
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
