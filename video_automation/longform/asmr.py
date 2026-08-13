"""Long-form sound therapy — the second kind of tinnitus video.

The short version of this format is 60 seconds and renders every frame. A
sound-therapy video worth uploading is ten minutes to an hour, and at 1920x1080
that is 18,000 to 108,000 frames of Python compositing. Rendering it straight
would take longer than the video.

**So the picture is a seamless loop.** One minute of frames is rendered, then
ffmpeg repeats it to length. That only works if the loop is genuinely seamless,
which is a constraint on every moving element:

* **The nebula drifts around a closed circle** rather than in a straight line,
  with the circle's period equal to the loop. A linear drift cannot return.
* **The breathing cycle must divide the loop.** 60s of picture at a 10-second
  breath is six whole cycles; 11 seconds would land mid-inhale at the cut.
* **So must the watermark's float.** Its period is set from the loop rather than
  inherited from the short's 5.5s, which does not divide 60.

Get any of those wrong and there is a visible jump every minute, which is worse
than no motion at all.

**The audio is not looped.** `core/soundbed.py` generates noise to the exact
length, so the one thing a listener would actually notice repeating — the
sound — never does. That asymmetry is the whole design: loop the thing nobody
watches closely, generate the thing they are listening to.

**Nothing here is a treatment.** The bed is the kind of sound people use; the
copy that goes with it must not promise relief. See the skill.
"""

from __future__ import annotations

import math
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

from ..core import soundbed
from ..core.brand import Brand
from ..core.voiceover import build_narration_aligned, profile_args
from . import audio as audio_mod
from ..core.draw import subpixel
from ..core.frame import LANDSCAPE, Frame
from ..tinnitus.asmr import _ring_sprite, nebula_canvas

# The ring breathes on a 4-in / 6-out cycle, the pattern paced-breathing
# guidance generally favours over box breathing — and the slow half is the half
# a viewer is watching the ring shrink through.
INHALE, EXHALE = 4.0, 6.0
BREATH = INHALE + EXHALE


def _ease(x: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, x)))


def _radius(t: float, r_min: float, r_max: float) -> float:
    """Ring radius at `t`, on a cycle that closes exactly at `BREATH`."""
    p = t % BREATH
    if p < INHALE:
        return r_min + (r_max - r_min) * _ease(p / INHALE)
    return r_max - (r_max - r_min) * _ease((p - INHALE) / EXHALE)


def render_loop(out: Path, brand: Brand, loop: float = 60.0,
                frame: Frame = LANDSCAPE, fps: int = 30, seed: int = 7,
                r_min: int = 170, r_max: int = 300,
                logo_w: int | None = None) -> Path:
    """One seamless loop of picture: drifting nebula, breathing ring, mark.

    `loop` must be a whole number of `BREATH` cycles or the ring jumps at the
    splice; this raises rather than shipping the jump, because a seam every
    minute for forty minutes is the kind of fault nobody spots in review and
    everybody spots in playback.
    """
    if abs(loop / BREATH - round(loop / BREATH)) > 1e-6:
        raise ValueError(
            f"loop={loop}s is {loop / BREATH:.2f} breathing cycles — it must be "
            f"a whole number of {BREATH}s cycles or the ring jumps at the splice")

    pad = 260
    cw, ch = frame.w + pad, frame.h + pad
    canvas = nebula_canvas(cw, ch, seed)
    sprite = _ring_sprite(r_max)
    mark = brand.mark(logo_w or int(frame.logo_w * brand.mark_scale))

    # The float period also has to divide the loop. Derived, not chosen.
    float_period = loop / 10.0
    logo_at, logo_float = frame.logo_at, 8.0
    if mark is not None:
        frame.check_top(logo_at[1] - logo_float, "asmr watermark")

    n = int(round(loop * fps))
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{frame.w}x{frame.h}", "-r", str(fps), "-i", "-",
         "-an", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)

    cx, cy = frame.w // 2, frame.h // 2
    rad = pad / 2.0 - 4
    for i in range(n):
        t = i / fps
        a = 2 * math.pi * (t / loop)                 # closes exactly at `loop`
        bx = (cw - frame.w) / 2 + rad * math.cos(a)
        by = (ch - frame.h) / 2 + rad * math.sin(a)
        img = Image.fromarray(subpixel(canvas, bx, by, frame.w, frame.h))

        r = _radius(t, r_min, r_max)
        s = max(2, int(round(r / r_max * sprite.width)))
        ring = sprite.resize((s, s), Image.LANCZOS)
        img = img.convert("RGBA")
        img.alpha_composite(ring, (cx - s // 2, cy - s // 2))

        if mark is not None:
            fy = logo_at[1] + logo_float * math.sin(2 * math.pi * t / float_period)
            iy = math.floor(fy)
            img.alpha_composite(
                mark.transform(mark.size, Image.AFFINE,
                               (1, 0, 0, 0, 1, iy - fy), resample=Image.BILINEAR),
                (logo_at[0], iy))

        proc.stdin.write(img.convert("RGB").tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while encoding the ASMR loop")
    return out


def render_asmr_long(out: Path, workdir: Path, brand: Brand,
                     minutes: float = 10.0,
                     bed: soundbed.Bed | None = None,
                     intro: list | None = None, voice: str = "luna-calm",
                     intro_at: float = 4.0,
                     loop: float = 60.0, fps: int = 30, seed: int = 7,
                     fade: float = 6.0,
                     frame: Frame = LANDSCAPE) -> dict:
    """A full sound-therapy video: looped picture, generated bed, long fades.

    Returns the paths produced. `minutes` is the finished length; the picture is
    rendered once at `loop` seconds and repeated.

    `intro` is an optional spoken opening — sentence tuples, the same shape as
    everywhere else — read by `luna-calm` and then never heard again. It exists
    because a forty-minute noise file with no voice is indistinguishable from
    every other one on the platform: the thirty seconds at the front are where
    the video says what the sound is for, who it is from, and how to set the
    level. After that the piece is the sound, and silence is correct.

    **`voice` is `luna-calm`, not the article reader.** SOFT chain, unhurried,
    no pitch shift. The article videos use `mia` because an explainer wants the
    reader who explains; this wants the one the listener can settle under.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    total = minutes * 60.0
    bed = bed or soundbed.Bed(colour="pink", breathe=0.10,
                              breathe_period=BREATH)

    picture = render_loop(workdir / "loop.mp4", brand, loop=loop,
                          frame=frame, fps=fps, seed=seed)

    wav = soundbed.write(workdir / "bed.wav", total, bed)
    # Long fades at both ends. A therapy bed that starts at full level is a
    # jolt, and one that stops dead wakes the listener it just settled.
    faded = workdir / "bed-faded.wav"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(wav),
         "-af", (f"afade=t=in:st=0:d={fade},"
                 f"afade=t=out:st={max(total - fade, 0):.2f}:d={fade},"
                 f"loudnorm=I=-20:TP=-2:LRA=5"),
         "-ar", "48000", "-ac", "2", str(faded)],
        check=True, capture_output=True)

    # The spoken intro, if there is one, ducks the bed under it exactly as the
    # article videos duck music under narration — sidechained, so the bed is at
    # full strength for the other thirty-nine minutes and steps back only where
    # there are words.
    audio = faded
    if intro:
        track, _, _ = build_narration_aligned(
            [list(s) for s in intro], workdir / "intro", gap=0.55,
            **profile_args(voice))
        audio = audio_mod.mix_voice_over_bed(faded, track, workdir / "mix.wav",
                                             total, voice_at=intro_at)

    reps = int(math.ceil(total / loop))
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y",
         "-stream_loop", str(reps), "-i", str(picture), "-i", str(audio),
         "-map", "0:v", "-map", "1:a", "-t", f"{total:.3f}",
         "-c:v", "libx264", "-crf", "20", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(out)],
        check=True, capture_output=True)
    return {"video": out, "total": total, "loop": picture, "bed": faded,
            "audio": audio}
