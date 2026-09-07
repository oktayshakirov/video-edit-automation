"""Shumen Visitor / Own Past — stacked vertical quote, two Shumen clips.

The user's own line, built straight in the approved Sunset Sea Stack layout:
two Shumen drone clips stacked into one 9:16 frame, the quote read on the
black band between them. A complete thought with no turn, so no kicker and no
reveal format — the deflation is in the last word.

`gone` is where the line lands, so it takes the set-piece size (88px against
the 44px body) and drops its full stop on screen while the voice still takes
the beat.

Both clips run long against the read (26.8s and 18.5s), so neither needs a
`slow` factor — they are simply in-pointed and let run.

`pick_crop_tile` searches x only when the tile aspect already matches the full
sensor height, so on `Shumen 3` it returned the whole frame and the bottom tile
came back close to half white sky. `BOX_BOTTOM` is a hand-set 1820x1500 window
pulled down onto the blocks — a downscale into the 890px tile, so it costs no
sharpness — and puts the horizon a quarter of the way down.

The karaoke accent is pinned to the terracotta of the roofs rather than left on
`"auto"`, which averaged the two clips to a muddy blue.
"""

from pathlib import Path

from video_automation.core.media import build_proxy
from video_automation.core.vertical import (FONT_QUOTE, FONT_QUOTE_INDEX,
                                            pick_crop_tile, stack_tile_size)
from video_automation.core.voiceover import (render_narrated_stack,
                                             profile_args)

SOURCE_POST = None                      # off-site: a written quote, no article

TOP = Path("~/Desktop/Shumen 4.mp4").expanduser()
BOTTOM = Path("~/Desktop/Shumen 3.mp4").expanduser()
OUT = Path("~/Desktop/shumen-visitor-own-past.mp4").expanduser()
WORK = Path("~/Desktop/.work-shumen-visitor-own-past").expanduser()

START_TOP, START_BOTTOM = 0.4, 0.4

BOX_BOTTOM = (1024, 524, 1820, 1500)    # hand-set: off the sky, onto the blocks
ACCENT = (232, 122, 72, 255)            # terracotta, off the roofs

GAP = [0.55, 0.65, 0.9, 0.6]
TAIL = 1.2

SENTENCES = [
    [("i read a quote that said", "i red a quote that said,")],
    [("“you can walk down the street", "you can walk down the street"),
     ("where you grew up,", "where you grew up,"),
     ("and still feel like a visitor", "and still feel like a visitor"),
     ("in your own past.”", "in your own past.")],
    [("the places stay,", "the places stay,"),
     ("but somehow the person", "but somehow the person"),
     ("who belonged there is", "who belonged there is")],
    [("gone", "gone.")],
]

BIG = "gone"


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h = stack_tile_size()

    boxes = []
    for tag, src in (("top", TOP), ("bot", BOTTOM)):
        proxy = WORK / f"{tag}.proxy.mp4"
        if not proxy.exists():
            build_proxy(src, proxy)
        boxes.append(pick_crop_tile(proxy, tile_w, tile_h))
    box_top = boxes[0]
    box_bottom = BOX_BOTTOM

    out, total = render_narrated_stack(
        (TOP, START_TOP, box_top), (BOTTOM, START_BOTTOM, box_bottom),
        OUT, SENTENCES, WORK,
        font_path=FONT_QUOTE, font_index=FONT_QUOTE_INDEX,
        font_size=lambda c: 88 if c == BIG else 44,
        accent=ACCENT, gap=GAP, tail=TAIL,
        **profile_args("leo"))
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
