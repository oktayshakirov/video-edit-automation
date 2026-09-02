"""Berlin Map / Way Home — stacked vertical quote, two Spree clips.

A straight melancholic quote in the approved Sunset Sea Stack layout: two
drone clips over the Spree stacked into one 9:16 frame, the quote read on
the black band between them. No kicker, no turn — the line is a complete
thought, so it is built as given rather than forced into the reveal format.

`belong` is the word the quote lands on, so it gets the set-piece size (88px
against a 44px body) and drops its full stop on screen while the voice still
takes the beat.

`Spree Buildings 3` is 17.8s against the read, so both tiles carry a `slow`
factor computed from the measured narration length — aerial motion stretches
cleanly and a hard cut would have spent the payoff on a cut.
"""

from pathlib import Path

from video_automation.core.media import build_proxy
from video_automation.core.vertical import (FONT_QUOTE, FONT_QUOTE_INDEX,
                                            pick_crop_tile, stack_tile_size)
from video_automation.core.voiceover import (build_narration_aligned,
                                             render_narrated_stack,
                                             profile_args)

SOURCE_POST = None                      # off-site: a written quote, no article

TOP = Path("~/Desktop/Berlin 26 2_4/Spree Buildings 3.mp4").expanduser()
BOTTOM = Path("~/Desktop/Berlin 26 2_4/Spree Buildings 2.mp4").expanduser()
OUT = Path("~/Desktop/berlin-map-way-home.mp4").expanduser()
WORK = Path("~/Desktop/.work-berlin-map-way-home").expanduser()

START_TOP, START_BOTTOM = 0.4, 0.4

GAP = [0.55, 0.65, 0.9, 0.6]
TAIL = 1.2

SENTENCES = [
    [("i read a quote that said", "i red a quote that said,")],
    [("“you can have a map", "you can have a map"),
     ("to every corner of the world,", "to every corner of the world,"),
     ("and still not know", "and still not know"),
     ("the way home.”", "the way home.")],
    [("maybe the hardest kind of lost", "maybe the hardest kind of lost"),
     ("is knowing exactly where you are,", "is knowing exactly where you are,"),
     ("but nowhere feels like where you", "but nowhere feels like where you")],
    [("belong", "belong.")],
]

BIG = "belong"


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
        return max(1.0, total / (dur - start - 0.15))

    out, total_r = render_narrated_stack(
        (TOP, START_TOP, box_top, slow(TOP, START_TOP)),
        (BOTTOM, START_BOTTOM, box_bottom, slow(BOTTOM, START_BOTTOM)),
        OUT, SENTENCES, WORK,
        font_path=FONT_QUOTE, font_index=FONT_QUOTE_INDEX,
        font_size=lambda c: 88 if c == BIG else 44,
        gap=GAP, tail=TAIL,
        **profile_args("leo"))
    print(f"{out}  {total_r:.2f}s")


if __name__ == "__main__":
    main()
