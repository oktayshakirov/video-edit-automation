"""Ocean Follow-Up Questions — stacked vertical quote with an absurd kicker.

Two clips stacked, quote read on the band between them, in the approved
Sunset Sea Stack layout. What is new here is the *turn*: the piece is a
straight melancholic quote for three sentences and then deflates into a dry
joke, and the joke is set in a different face and a different colour so the
register changes on screen a beat before the words land. A soft whoosh sits
on the same frame, so the change is heard as well as seen.

Both tiles are ocean, which is not decoration — the quote and the punchline
are both about the sea, so the footage is the vehicle rather than a backdrop.

`Island 1` is 13.2s against a ~22s read, so the tiles carry a `slow` factor.
Aerial motion is smooth enough to stretch; a hard cut to a second angle would
have spent the punchline's setup on a cut.
"""

from pathlib import Path

from video_automation.core.media import build_proxy
from video_automation.core.vertical import (FONT_ROUNDED, FONT_QUOTE,
                                            FONT_QUOTE_INDEX,
                                            pick_crop_tile, stack_tile_size)
from video_automation.core.voiceover import (build_narration_aligned,
                                             render_narrated_stack,
                                             profile_args)

SOURCE_POST = None                      # off-site: a written quote, no article

TOP = Path("~/Desktop/Bulgaria/Akutino/Island 1.mp4").expanduser()
BOTTOM = Path("~/Desktop/Bulgaria/Akra Castle/Coast 8.mp4").expanduser()
OUT = Path("~/Desktop/ocean-follow-up-questions.mp4").expanduser()
WORK = Path("~/Desktop/.work-ocean-follow-up").expanduser()

START_TOP, START_BOTTOM = 0.4, 0.4

# The turquoise of the shallow water in the bottom tile. The kicker's ink —
# one accent, pulled out of the footage, as the colour rule requires.
AQUA = (86, 222, 208, 255)

SENTENCES = [
    [("i read a quote that said", "i red a quote that said,")],
    [("“you can't calm the ocean", "you can't calm the ocean"),
     ("by arguing with the waves.”", "by arguing with the waves.")],
    [("some things get easier", "some things get easier"),
     ("when you stop trying to control", "when you stop trying to control"),
     ("what was never yours.", "what was never yours to control.")],
    # The turn. Different face, different colour, and a whoosh on the first
    # caption — the register changes before the sentence has finished.
    [("unfortunately,", "unfortunately,"),
     ("i have several follow-up questions", "i have several follow up questions"),
     ("for the ocean.", "for the ocean.")],
]

KICKER = {c for c, _ in SENTENCES[-1]}


def is_kicker(caption: str) -> bool:
    return caption in KICKER


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

    # Measure the read before rendering, so each tile is stretched by exactly
    # what it is short by rather than by a guessed factor. Kokoro is
    # deterministic, so the render's own synthesis lands on the same length.
    probe = WORK / "probe"
    probe.mkdir(exist_ok=True)
    _, _, total = build_narration_aligned(
        SENTENCES, probe, gap=[0.6, 0.6, 1.5, 0.6], tail=1.2,
        **profile_args("leo"))

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
        font_path=lambda c: FONT_ROUNDED if is_kicker(c) else FONT_QUOTE,
        font_index=lambda c: 0 if is_kicker(c) else FONT_QUOTE_INDEX,
        ink=lambda c: AQUA if is_kicker(c) else None,
        emoji=lambda c: "🌊" if c == "for the ocean." else None,
        sfx=lambda c: "whoosh" if c == "unfortunately," else None,
        sfx_gain=0.14,                  # slight, under the voice, not over it
        gap=[0.6, 0.6, 1.5, 0.6], tail=1.2,
        **profile_args("leo"))
    print(f"{out}  {total_r:.2f}s")


if __name__ == "__main__":
    main()
