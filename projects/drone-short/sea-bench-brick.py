"""Sea Bench Brick — stacked dark-humour one-liner over two Sinemorets bench clips.

No opener, no quote marks, no karaoke (user's call): "this", a short beat, then
the whole punchline on the band as one caption.
"""

from pathlib import Path

from video_automation.core.media import build_proxy
from video_automation.core.vertical import pick_crop_tile, stack_tile_size
from video_automation.core.voiceover import render_narrated_stack, profile_args

SOURCE_POST = None

FOOT = Path("~/Desktop/Drone Videos/Footage/Sinemorets").expanduser()
TOP = FOOT / "Sea Bench 1.mp4"
BOTTOM = FOOT / "Sea Coast 3.mp4"
OUT = Path("~/Desktop/sea-bench-brick.mp4").expanduser()
WORK = Path("~/Desktop/.work-sea-bench-brick").expanduser()

GAP = [1.1, 0.8]   # >= RUN_BREAK_GAP so the beat after "this" is real silence
TAIL = 1.5

SENTENCES = [
    [("this view", "this view.")],
    [("& you hit me in the back of the head with a brick",
      "and you hit me in the back of the head with a brick.")],
]


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h = stack_tile_size()
    boxes = []
    for name, src in (("top", TOP), ("bot", BOTTOM)):
        proxy = WORK / f"{name}.proxy.mp4"
        if not proxy.exists():
            build_proxy(src, proxy)
        boxes.append(pick_crop_tile(proxy, tile_w, tile_h))
    print("boxes", boxes)
    out, total = render_narrated_stack(
        (TOP, 0.0, boxes[0]), (BOTTOM, 0.0, boxes[1]),
        OUT, SENTENCES, WORK,
        karaoke=False, karaoke_box=False, karaoke_upper=False,
        gap=GAP, tail=TAIL, **profile_args("leo"))
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
