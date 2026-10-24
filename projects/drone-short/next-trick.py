"""Next Trick — single-clip vertical quote, Berlin sunset.

A deadpan line: it opens like a stage magician's flourish and lands on the
treadmill of chasing goals. Kokoro has no emotion parameter, so the delivery
is built from timing: a showman's beat after "next trick", then the longest
gap after "feel nothing" so the flat line hangs before the punchline rushes
out in one breath.

The first cut of this test (Ready Is a Decision) was a stack with the same
clip in both tiles. Its user notes set the rules this cut follows: one clip
means no black band, a plain sans instead of the Iowan italic, sentence case.

Sunset 5 is a slow push toward the sun over the Havel; the 9:16 window is the
full height centred on the sun, which holds near the middle the whole clip.
Ungraded, like the other Berlin 26 sunset cuts.
"""

from pathlib import Path

from video_automation.core.voiceover import render_narrated, profile_args

SOURCE_POST = None                      # off-site: the user's own line, no article

FOOT = Path("~/Desktop/Drone Videos/Footage/Berlin 26 1:4").expanduser()
SRC = FOOT / "Sunset 5.mp4"
OUT = Path("~/Desktop/next-trick.mp4").expanduser()
WORK = Path("~/Desktop/.work-next-trick").expanduser()

BOX = (1744, 0, 1216, 2160)             # 9:16 full height, sun at x~2350
START = 0.0

SIZE = 36                               # the smaller-caption test carries over

GAP = [0.7, 1.0, 0.65]     # the long one is the deadpan beat after "feel nothing"
TAIL = 1.2

SENTENCES = [
    [("And for my next trick,", "and for my next trick,")],
    [("I'm going to set a goal,", "i'm going to set a goal,"),
     ("achieve it,", "achieve it,"),
     ("feel nothing,", "feel nothing,")],
    [("and immediately proceed", "and immediately proceed"),
     # Spoken with a comma, not a full stop: Kokoro's sentence-final fall
     # drops "one." into creaky voice that reads as a glitch (voice.md).
     ("to set another one.", "to set another one,")],
]


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    out, total = render_narrated(
        SRC, OUT, START, BOX, text="", workdir=WORK,
        sentences=SENTENCES, font_size=SIZE,
        gap=GAP, tail=TAIL, **profile_args("leo"))
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
