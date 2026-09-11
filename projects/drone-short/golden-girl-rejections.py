"""Golden Girl / 100 Rejections — stacked vertical quote, two Golden Girl clips.

The user's overheard line, built straight in the approved Sunset Sea Stack
layout: two golden-hour drone clips stacked into one 9:16 frame, the quote read
on the black band between them.

Two set-piece words rather than the usual one, on the user's call: `excited`
and `no` both take the 88px size against the 44px body and each get their own
caption to hold the beat. They are the two turns in the line — the reframe
(`excited`) and the word it reframes (`no`).

`band` is 100 (the drone stack default since this cut). The band stays centred,
so the caption stays centred.

`Golden Girl Night Hyperlapse 3` is only 9.4s and `Golden Girl Night` 17.2s
against a ~19s read, so both tiles carry a `slow` factor computed from the
measured narration length.
"""

from pathlib import Path

from video_automation.core.media import build_proxy
from video_automation.core.vertical import (FONT_QUOTE, FONT_QUOTE_INDEX,
                                            pick_crop_tile, stack_tile_size)
from video_automation.core.voiceover import (build_narration_aligned,
                                             render_narrated_stack,
                                             profile_args)

SOURCE_POST = None                      # off-site: an overheard quote, no article

TOP = Path("~/Desktop/Golden Girl Night Hyperlapse 3.mp4").expanduser()
BOTTOM = Path("~/Desktop/Golden Girl Night.mp4").expanduser()
OUT = Path("~/Desktop/golden-girl-rejections.mp4").expanduser()
WORK = Path("~/Desktop/.work-golden-girl-rejections").expanduser()

START_TOP, START_BOTTOM = 0.3, 0.3

BAND = 100                              # drone stack default (multiple of 4 so
                                        # both tiles stay even)

GAP = [0.6, 0.7, 0.6]
TAIL = 1.2

SENTENCES = [
    [("i heard someone say", "i heard someone say,")],
    [("“if you know you were", "if you know you were"),
     ("100 rejections away", "one hundred rejections away"),
     ("from your dream,", "from your dream,"),
     ("think how", "think how"),
     ("excited", "excited"),
     ("you'd be every time", "you'd be every time"),
     ("someone told you", "someone told you"),
     ("no”", "no.")],
    [("and then it", "and then it"),
     ("stuck with me", "stuck with me.")],
]

BIG = {"excited", "no”"}                 # both take the 88px set-piece size


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h = stack_tile_size(BAND)

    boxes = []
    for tag, src in (("top", TOP), ("bot", BOTTOM)):
        proxy = WORK / f"{tag}.proxy.mp4"
        if not proxy.exists():
            build_proxy(src, proxy)
        boxes.append(pick_crop_tile(proxy, tile_w, tile_h))
    box_top, box_bottom = boxes

    probe = WORK / "probe"
    probe.mkdir(exist_ok=True)
    _, _, total = build_narration_aligned(
        SENTENCES, probe, gap=GAP, tail=TAIL, **profile_args("leo"))

    def slow(src: Path, start: float) -> float:
        import subprocess
        dur = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(src)],
            check=True, capture_output=True, text=True).stdout.strip())
        # 0.15s of headroom: -shortest truncates silently, so never land exact.
        return max(1.0, total / (dur - start - 0.15))

    out, total_r = render_narrated_stack(
        (TOP, START_TOP, box_top, slow(TOP, START_TOP)),
        (BOTTOM, START_BOTTOM, box_bottom, slow(BOTTOM, START_BOTTOM)),
        OUT, SENTENCES, WORK,
        band=BAND,
        font_path=FONT_QUOTE, font_index=FONT_QUOTE_INDEX,
        font_size=lambda c: 88 if c in BIG else 44,
        gap=GAP, tail=TAIL,
        **profile_args("leo"))
    print(f"{out}  {total_r:.2f}s")


if __name__ == "__main__":
    main()
