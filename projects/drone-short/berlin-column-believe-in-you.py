"""Berlin Column / Believe In You — stacked vertical quote, box-karaoke trial.

The user's own affirmation, read over two Victory Column aerials: a
long-exposure night pass on top (light trails, the golden angel lit warm) and
a sunset pass on the bottom (the same column against a coral-and-gold sky).
Same landmark, two times of day — the contrast is the point, same instinct as
the Berlin map/way-home stack.

This is the first render of the "box karaoke" caption style: a rounded
rectangle in the accent colour behind the active word instead of colouring
its ink, on a bold all-caps face (`FONT_KARAOKE_BOX`) rather than the usual
Iowan Old Style italic. Trial only — see `render_caption_karaoke`'s `box=`
and `upper=` in `core/vertical.py`. If it holds up, promote it past this one
cut.

The top clip is a boomerang, not a slow-motion stretch. The narration needs
~14s and the source is only 7.0s — the first cut covered the gap with a
~2.8x `slow`, and the user's call was that it reads as laggy. `_build_boomerang`
plays the clip forward, then the same span reversed, both at native speed:
motion stays real, and the reverse half reads as the drone drifting back
rather than a loop trick. Built once at full 4K into `WORK`, upstream of the
crop, so `render_narrated_stack` treats it like any other source file.

Because a boomerang shows the *entire* clip in both directions, `BOX_TOP`'s
crop has to stay safe for the full 7s, not just the fraction a slow factor
would have consumed — checked frame-by-frame against the source, x=800 clears
the base plinth all the way to t=6.98s (the last frame either half plays);
`pick_crop_tile`'s own answer here was similar but this is hand-verified
rather than trusted blind, per the crop-picking doc's own warning about that.

`accent="auto"` — the footage is what should pick the box colour, not a
hand-set one. Both clips are warm (traffic light-trails / golden hour), so the
auto colour should land somewhere in the same range the reference used.

`hold_last_caption=True` keeps "I believe in you" up (unhighlighted) once the
karaoke reaches it, and `fade_out` fades the picture to black under it — a
one-off pair for this cut, so the user can drop their own sound in after the
quote. `TAIL`/`FADE_OUT` are deliberately short here: a quick fade and a small
gap were the ask on the second pass, not the ~3.5s runway the first pass gave.
"""

from pathlib import Path
import subprocess

from video_automation.core.media import build_proxy
from video_automation.core.vertical import (FONT_KARAOKE_BOX,
                                            FONT_KARAOKE_BOX_INDEX,
                                            pick_crop_tile, stack_tile_size)
from video_automation.core.voiceover import (render_narrated_stack,
                                             profile_args)

SOURCE_POST = None                      # off-site: the user's own line, no article

TOP = Path("~/Desktop/1.mp4").expanduser()       # night pass, light trails
BOTTOM = Path("~/Desktop/2.mp4").expanduser()    # sunset pass
OUT = Path("~/Desktop/berlin-column-believe-in-you.mp4").expanduser()
WORK = Path("~/Desktop/.work-berlin-column-believe-in-you").expanduser()

START_TOP, START_BOTTOM = 0.0, 0.0

BOX_TOP = (800, 0, 2564, 2160)   # hand-set — see module docstring

GAP = [0.6, 0.65, 0.85, 0.6]
TAIL = 1.0              # small gap after the quote for the user's own sound
FADE_OUT = 0.8           # quick fade to black over that gap

SENTENCES = [
    [("i hope you become the light", "i hope you become the light"),
     ("you've always been searching for,", "you've always been searching for,")],
    [("find your way through", "find your way through"),
     ("every dark season,", "every dark season,")],
    [("and eventually stand somewhere", "and eventually stand somewhere"),
     ("you once thought was impossible to reach.",
      "you once thought was impossible to reach.")],
    [("i believe in you", "i believe in you")],
]


def _build_boomerang(src: Path, half_dur: float, out: Path) -> Path:
    """Forward `[0, half_dur]` then the same span reversed — native speed.

    One ffmpeg call, two trims of the same input (cheap: the source has a
    single keyframe at t=0, so any read already decodes from the start).
    `reverse` buffers the trimmed span in memory, fine at 4K for a span this
    short.
    """
    if out.exists():
        return out
    vf = (f"[0:v]trim=start=0:end={half_dur:.3f},setpts=PTS-STARTPTS[fwd];"
          f"[0:v]trim=start=0:end={half_dur:.3f},setpts=PTS-STARTPTS,reverse[rev];"
          f"[fwd][rev]concat=n=2:v=1:a=0[outv]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(src),
           "-filter_complex", vf, "-map", "[outv]",
           "-c:v", "libx264", "-crf", "16", "-preset", "slow",
           "-pix_fmt", "yuv420p", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    tile_w, tile_h = stack_tile_size()

    bot_proxy = WORK / "bot.proxy.mp4"
    if not bot_proxy.exists():
        build_proxy(BOTTOM, bot_proxy)
    box_top = BOX_TOP
    box_bottom = pick_crop_tile(bot_proxy, tile_w, tile_h)

    # Narration measured once at 13.9526s against a 7.0s top / 9.4333s bottom.
    total_estimate = 13.9526
    half_dur = total_estimate / 2   # 6.976s — under the 7.0s the source has
    top_src = _build_boomerang(TOP, half_dur, WORK / "top.boomerang.mp4")

    # Bottom tile still runs slow, same as before — only the top clip was
    # flagged as laggy. 99%-of-length margin: a same-length match leaves zero
    # slack against float rounding in the ffmpeg -t.
    slow_bottom = round(total_estimate / (9.4333 * 0.99), 3)

    out, total = render_narrated_stack(
        (top_src, START_TOP, box_top),
        (BOTTOM, START_BOTTOM, box_bottom, slow_bottom),
        OUT, SENTENCES, WORK,
        font_path=FONT_KARAOKE_BOX, font_index=FONT_KARAOKE_BOX_INDEX,
        stroke=5,
        karaoke_box=True, karaoke_upper=True,
        accent="auto", gap=GAP, tail=TAIL,
        hold_last_caption=True, fade_out=FADE_OUT,
        **profile_args("leo"))
    print(f"{out}  {total:.2f}s  slow_bottom={slow_bottom}")


if __name__ == "__main__":
    main()
