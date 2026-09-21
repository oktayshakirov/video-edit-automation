"""Medicine or Poison — stacked vertical quote over two sunset clips.

Sinemorets field hyperlapse on top, Akra Castle sea horizon below. Both
sources (10.0s / 11.4s) are shorter than the read, so each is a full-length
boomerang — forward, then reversed, native speed — per the user's ask that the
footage "goes back to the beginning" rather than slowing down. Built at 4K
upstream of the crop, so the crop has to hold for the whole clip.
"""

from pathlib import Path
import subprocess

from video_automation.core.media import build_proxy
from video_automation.core.vertical import pick_crop_tile, stack_tile_size
from video_automation.core.voiceover import render_narrated_stack, profile_args

SOURCE_POST = None

FOOT = Path("~/Desktop/Drone Videos/Footage").expanduser()
TOP = FOOT / "Sinemorets/Field Sunset Hyperlapse.mp4"
BOTTOM = FOOT / "Akra Castle/Sea Sunset Horizon 2.mp4"
OUT = Path("~/Desktop/medicine-or-poison.mp4").expanduser()
WORK = Path("~/Desktop/.work-medicine-or-poison").expanduser()

BOX_BOTTOM = (1276, 0, 2564, 2160)   # hand-set: keep the sun in frame

GAP = [0.65, 0.65, 0.65]
TAIL = 1.2

SENTENCES = [
    [("i read a quote that said", "i red a quote that said,")],
    [("“the people around you", "the people around you"),
     ("are either medicine", "are either medicine,"),
     ("or poison.”", "or poison.")],
    [("some people bring peace to your mind,", "some people bring peace to your mind,"),
     ("while others slowly drain", "while others slowly drain"),
     ("everything good out of you.", "everything good out of you.")],
]


def _build_boomerang(src: Path, out: Path) -> Path:
    """Whole clip forward, then reversed, native speed."""
    if out.exists():
        return out
    vf = ("[0:v]split[a][b];[a]setpts=PTS-STARTPTS[fwd];"
          "[b]setpts=PTS-STARTPTS,reverse[rev];[fwd][rev]concat=n=2:v=1:a=0[outv]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
                    "-filter_complex", vf, "-map", "[outv]",
                    "-c:v", "libx264", "-crf", "16", "-preset", "slow",
                    "-pix_fmt", "yuv420p", str(out)], check=True)
    return out


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h = stack_tile_size()
    boxes = []
    for name, src in (("top", TOP), ("bot", BOTTOM)):
        proxy = WORK / f"{name}.proxy.mp4"
        if not proxy.exists():
            build_proxy(src, proxy)
        boxes.append(pick_crop_tile(proxy, tile_w, tile_h))
    boxes[1] = BOX_BOTTOM   # pick_crop_tile chose x=0 and cut the sun off the right edge
    print("boxes", boxes)
    top_src = _build_boomerang(TOP, WORK / "top.boomerang.mp4")
    bot_src = _build_boomerang(BOTTOM, WORK / "bot.boomerang.mp4")
    out, total = render_narrated_stack(
        (top_src, 0.0, boxes[0]), (bot_src, 0.0, boxes[1]),
        OUT, SENTENCES, WORK,
        gap=GAP, tail=TAIL, **profile_args("leo"))
    print(f"{out}  {total:.2f}s")


if __name__ == "__main__":
    main()
