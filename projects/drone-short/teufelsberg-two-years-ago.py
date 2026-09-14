"""Teufelsberg Two Years Ago — stacked vertical quote, two Teufelsberg clips.

The user's overheard line, built in the approved Sunset Sea Stack layout: two
golden-hour Teufelsberg drone clips (the abandoned listening station, radar
domes lit by the setting sun) stacked into one 9:16 frame, the quote read on
the black band between them.

`wonderful` is where the line turns — from measuring the distance still to
go, to noticing the distance already covered — so it takes the set-piece size
(88px against the 44px body) on its own caption.

Both clips run long against the read (18.9s and 16.8s) so neither needs a
`slow` factor — simply in-pointed and let run. `accent` is left on `"auto"`:
both clips share the same golden-hour palette, so sampling pulls a consistent
warm orange rather than averaging two different scenes.
"""

from pathlib import Path

from video_automation.core.media import build_proxy
from video_automation.core.vertical import (FONT_QUOTE, FONT_QUOTE_INDEX,
                                            pick_crop_tile, stack_tile_size)
from video_automation.core.voiceover import (render_narrated_stack,
                                             profile_args)

SOURCE_POST = None                      # off-site: an overheard quote, no article

TOP = Path("~/Desktop/Teufelsberg 1.mp4").expanduser()
BOTTOM = Path("~/Desktop/Teufelsberg 2.mp4").expanduser()
OUT = Path("~/Desktop/teufelsberg-two-years-ago.mp4").expanduser()
WORK = Path("~/Desktop/.work-teufelsberg-two-years-ago").expanduser()

START_TOP, START_BOTTOM = 1.0, 0.5

GAP = [1.05, 0.85, 0.6]
TAIL = 1.2

SENTENCES = [
    [("i came across these words today", "i came across these words today.")],
    [("“i'm not everything", "i'm not everything"),
     ("i want to be yet,", "i want to be yet,"),
     ("but i'm a lot of things", "but i'm a lot of things"),
     ("i wanted to be", "i wanted to be"),
     ("two years ago.”", "two years ago.")],
    [("and what a", "and what a"),
     ("wonderful", "wonderful"),
     ("thing it is", "thing it is"),
     ("to realize that.", "to realize that.")],
]

BIG = "wonderful"


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h = stack_tile_size()

    boxes = []
    for tag, src in (("top", TOP), ("bot", BOTTOM)):
        proxy = WORK / f"{tag}.proxy.mp4"
        if not proxy.exists():
            build_proxy(src, proxy)
        boxes.append(pick_crop_tile(proxy, tile_w, tile_h))
    box_top, box_bottom = boxes

    out, total = render_narrated_stack(
        (TOP, START_TOP, box_top), (BOTTOM, START_BOTTOM, box_bottom),
        OUT, SENTENCES, WORK,
        font_path=FONT_QUOTE, font_index=FONT_QUOTE_INDEX,
        font_size=lambda c: 88 if c == BIG else 44,
        gap=GAP, tail=TAIL,
        **profile_args("leo"))
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
