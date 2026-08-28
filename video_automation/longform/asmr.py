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
import shutil
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..core import soundbed
from ..core.brand import Brand
from ..core.voiceover import build_narration_aligned, profile_args
from . import audio as audio_mod
from ..core.draw import subpixel, wrap
from ..core.frame import LANDSCAPE, Frame
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX
from ..tinnitus import asmr as short_asmr
from ..tinnitus.asmr import _ring_sprite, nebula_canvas

# The ring breathes on a 4-in / 6-out cycle, the pattern paced-breathing
# guidance generally favours over box breathing — and the slow half is the half
# a viewer is watching the ring shrink through.
INHALE, EXHALE = 4.0, 6.0
BREATH = INHALE + EXHALE


def _ease(x: float) -> float:
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, x)))


def _breath(t: float, r_min: float, r_max: float) -> tuple[float, str, int]:
    """Radius, label and seconds remaining at `t`, closing exactly at `BREATH`.

    The label and the count are not decoration — they are what makes this a
    breathing video rather than a screensaver with a circle on it. The short
    has them and the first long cut did not, which is the whole difference
    between "follow this" and "watch this".

    The count is `ceil`, not the short's `int(left) + 1`. Both give 4,3,2,1
    across a 4s phase, but `int + 1` reads 5 when `left` is exactly 4.0 — an
    edge case the short never hits and this does, because the loop starts at
    t=0, which is exactly a phase boundary, so frame one of every repetition
    would flash a number the pattern does not contain.
    """
    p = t % BREATH
    if p < INHALE:
        r = r_min + (r_max - r_min) * _ease(p / INHALE)
        left = INHALE - p
        return r, "inhale", max(1, math.ceil(left))
    r = r_max - (r_max - r_min) * _ease((p - INHALE) / EXHALE)
    left = BREATH - p
    return r, "exhale", max(1, math.ceil(left))


def _drift(t: float, loop: float, cw: int, ch: int,
           frame: Frame) -> tuple[float, float]:
    """Where the nebula sits at `t`, on the closed circle the loop needs.

    Shared by the loop and the bookends so the drift is one continuous motion
    across all three segments. The bookends pass a `t` measured from the body's
    first frame — negative through the intro, positive through the outro — so
    both joins land on the same angle the loop starts and ends at. Give the
    intro its own clock and the background jumps at the cut, which is the one
    thing this whole architecture exists to avoid.
    """
    a = 2 * math.pi * (t / loop)
    rad = 260 / 2.0 - 4
    return ((cw - frame.w) / 2 + rad * math.cos(a),
            (ch - frame.h) / 2 + rad * math.sin(a))


def _mark_at(img: Image.Image, mark: Image.Image, t: float,
             logo_at: tuple[int, int], travel: float, period: float) -> None:
    """Composite the levitating watermark. Subpixel, on the shared clock."""
    fy = logo_at[1] + travel * math.sin(2 * math.pi * t / period)
    iy = math.floor(fy)
    img.alpha_composite(
        mark.transform(mark.size, Image.AFFINE, (1, 0, 0, 0, 1, iy - fy),
                       resample=Image.BILINEAR),
        (logo_at[0], iy))


def _centred(draw: ImageDraw.ImageDraw, text: str, cx: int, y: int,
             font: ImageFont.FreeTypeFont) -> None:
    """Ring type, centred on `cx` and unstroked.

    Unstroked because this background is generated rather than footage, so the
    contrast behind the ring is known. The narration captions elsewhere carry a
    black border because they cross live video; here it would only make the
    numbers heavier than the moment wants.
    """
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    draw.text((cx - (x1 - x0) // 2 - x0, y - y0), text, font=font,
              fill=(255, 255, 255, 235))


def render_loop(out: Path, brand: Brand, loop: float = 60.0,
                frame: Frame = LANDSCAPE, fps: int = 30, seed: int = 7,
                r_min: int = 150, r_max: int = 330,
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

    # Type scaled off the ring, so the label and count keep the proportions the
    # short established (52 and 116 against r_max=330) at whatever radius a
    # landscape frame wants.
    k = r_max / 330.0
    label_font = ImageFont.truetype(FONT_CAPTION, max(12, int(52 * k)),
                                    index=FONT_CAPTION_INDEX)
    count_font = ImageFont.truetype(FONT_CAPTION, max(12, int(116 * k)),
                                    index=FONT_CAPTION_INDEX)
    label_dy, count_dy = int(-104 * k), int(4 * k)

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
    for i in range(n):
        t = i / fps
        bx, by = _drift(t, loop, cw, ch, frame)      # closes exactly at `loop`
        img = Image.fromarray(subpixel(canvas, bx, by, frame.w, frame.h))

        r, label, left = _breath(t, r_min, r_max)
        # `2r + 80`, the short's sizing, not `r / r_max * sprite.width`. The
        # sprite is the circle plus a fixed glow margin; scaling the whole
        # sprite by the radius ratio shrinks the glow too, so the hairline
        # thinned and dimmed at the bottom of every exhale. Adding the margin
        # back as a constant keeps the stroke the same weight at every size.
        s = max(2, int(r * 2 + 80))
        ring = sprite.resize((s, s), Image.LANCZOS)
        img = img.convert("RGBA")
        img.alpha_composite(ring, (cx - s // 2, cy - s // 2))

        d = ImageDraw.Draw(img)
        _centred(d, label, cx, cy + label_dy, label_font)
        _centred(d, str(left), cx, cy + count_dy, count_font)

        if mark is not None:
            _mark_at(img, mark, t, logo_at, logo_float, float_period)

        proc.stdin.write(img.convert("RGB").tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while encoding the ASMR loop")
    return out


def render_bookend(out: Path, brand: Brand, length: float, captions: list,
                   kind: str, loop: float = 60.0, frame: Frame = LANDSCAPE,
                   fps: int = 30, seed: int = 7, r_min: int = 150,
                   r_max: int = 330, reveal: float = 3.0,
                   caption_at: float = 0.0,
                   logo_w: int | None = None) -> Path:
    """The intro or the outro: instruction cards, and the ring's entrance.

    **The intro does not open on the circle.** A breathing ring is an
    instruction, and showing it before the viewer has been told what it means
    makes the first twenty seconds something to decode rather than something to
    read. So the intro is words on the nebula, and the ring *arrives* — scaled
    and faded up over `reveal` seconds, landing at exactly `r_min` on the frame
    the body begins. Its entrance is what says the exercise is starting, which
    is a cue the first cut had to spend a sentence of narration on.

    The outro runs it backwards: the ring shrinks away, then the closing lines.

    `captions` are `Caption` objects from `build_narration_aligned`, offset by
    `caption_at` — the same delay the voice is mixed in at, so the words on
    screen and the words in the ear are the same words.

    Both segments share the loop's drift clock via `_drift`, so the nebula and
    the watermark carry straight through both cuts. The intro's `t` runs
    negative up to zero; the outro's runs forward from zero, which is where the
    body left the circle.
    """
    if kind not in ("intro", "outro"):
        raise ValueError(f"kind must be 'intro' or 'outro', got {kind!r}")

    pad = 260
    cw, ch = frame.w + pad, frame.h + pad
    canvas = nebula_canvas(cw, ch, seed)
    sprite = _ring_sprite(r_max)
    mark = brand.mark(logo_w or int(frame.logo_w * brand.mark_scale))

    text_size = 68
    text_lead = int(text_size * 1.34)
    text_font = ImageFont.truetype(FONT_CAPTION, text_size,
                                   index=FONT_CAPTION_INDEX)
    float_period = loop / 10.0
    logo_at, logo_float = frame.logo_at, 8.0
    if mark is not None:
        frame.check_top(logo_at[1] - logo_float, "asmr watermark")

    n = int(round(length * fps))
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{frame.w}x{frame.h}", "-r", str(fps), "-i", "-",
         "-an", "-c:v", "libx264", "-crf", "20", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)

    cx, cy = frame.w // 2, frame.h // 2
    max_w = int(frame.w * 0.62)
    for i in range(n):
        u = i / fps
        # The shared clock: negative through the intro so it arrives at 0 on the
        # body's first frame, forward through the outro from the same angle the
        # body ended on.
        t = (u - length) if kind == "intro" else u
        bx, by = _drift(t, loop, cw, ch, frame)
        img = Image.fromarray(
            subpixel(canvas, bx, by, frame.w, frame.h)).convert("RGBA")

        # The ring's entrance, or its exit. Eased on the same cosine the breath
        # uses, so it reads as the same object rather than a transition effect
        # bolted on in front of one.
        if kind == "intro":
            f = _ease(max(0.0, (u - (length - reveal)) / reveal))
        else:
            f = _ease(max(0.0, 1.0 - u / reveal))
        if f > 0.004:
            s = max(2, int(r_min * f * 2 + 80 * f))
            ring = sprite.resize((s, s), Image.LANCZOS)
            if f < 0.999:
                # Fade the whole sprite, alpha and all. Scaling alone pops in at
                # full brightness the moment it is a pixel wide.
                a = ring.getchannel("A").point(lambda v: int(v * f))
                ring.putalpha(a)
            img.alpha_composite(ring, (cx - s // 2, cy - s // 2))

        # The instruction cards, on the narration's own boundaries.
        d = ImageDraw.Draw(img)
        for c in captions:
            if c.start + caption_at <= u < c.end + caption_at:
                lines = wrap(d, c.text, text_font, max_w)
                # Centred, and it can be: the guards in `render_asmr_long`
                # require the narration to finish before the intro's reveal
                # starts and to start after the outro's exit finishes, so the
                # cards and the ring are never on screen at the same time.
                # Setting the type high to dodge a ring that is not there yet
                # was the first version and it read as a subtitle.
                y = cy - (len(lines) * text_lead) // 2
                for ln in lines:
                    _centred(d, ln, cx, y, text_font)
                    y += text_lead
                break

        if mark is not None:
            _mark_at(img, mark, t, logo_at, logo_float, float_period)

        proc.stdin.write(img.convert("RGB").tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError(f"ffmpeg failed while encoding the {kind}")
    return out


def render_asmr_long(out: Path, workdir: Path, brand: Brand,
                     minutes: float = 10.0,
                     bed: soundbed.Bed | None = None,
                     bed_files: tuple[Path, Path] | None = None,
                     intro: list | None = None, outro: list | None = None,
                     voice: str = "luna",
                     intro_at: float = 3.0, outro_at: float = 4.5,
                     intro_len: float = 30.0, outro_len: float = 30.0,
                     reveal: float = 3.0,
                     loop: float = 60.0, fps: int = 30, seed: int = 7,
                     fade: float = 6.0, r_min: int = 150, r_max: int = 330,
                     keep_work: bool = False,
                     frame: Frame = LANDSCAPE) -> dict:
    """A full sound-therapy video: looped picture, generated bed, long fades.

    Returns the paths produced. `minutes` is the finished length; the picture is
    rendered once at `loop` seconds and repeated.

    **The picture is three segments, not one.** `intro_len` seconds of
    instruction cards with no ring, then `total - intro_len - outro_len`
    seconds of looped breathing body, then `outro_len` seconds of close. The
    body is still one rendered loop repeated, so cost is still fixed; the
    bookends are rendered once each and are the only frames that are not
    reused. The body length must be a whole number of `loop`s and this raises
    if it is not, for the same reason `render_loop` raises.

    `intro` and `outro` are spoken, read by `luna`, and both are also
    drawn on screen on their own narration boundaries. The intro says what the
    sound is, who it is from and how to set the level, then the ring arrives.
    The outro is not a subscribe card — it is an invitation to run it again,
    and it is deliberately the quietest thing in the video, because a piece
    whose whole purpose is to lower arousal cannot end by raising it.

    **`voice` is `luna`, not the article reader.** SOFT chain, unhurried,
    no pitch shift. The article videos use `mia` because an explainer wants the
    reader who explains; this wants the one the listener can settle under.

    **`bed_files=(low, high)` uses the brand's own album tracks instead of a
    generated bed.** It exists for one job: making a long version that is
    genuinely the *same piece* as an already-published short, which was built on
    those two MP3s. A generated bed is the better default and covers bands the
    album cannot reach — but a listener who liked the short came back for that
    sound, not for a spec. The tracks are layered by the short's own
    `render_bed`, so the mix is identical; the trade is that the honest limit
    travels with them (little energy above 4 kHz, so a high whistling tinnitus
    is not well covered) and the copy must not contradict it.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    total = minutes * 60.0
    bed = bed or soundbed.Bed(colour="pink", breathe=0.10,
                              breathe_period=BREATH)

    body = total - intro_len - outro_len
    if body <= 0 or abs(body / loop - round(body / loop)) > 1e-6:
        raise ValueError(
            f"body is {body:.1f}s after a {intro_len}s intro and a "
            f"{outro_len}s outro — it must be a whole number of {loop}s loops")

    picture = render_loop(workdir / "loop.mp4", brand, loop=loop,
                          frame=frame, fps=fps, seed=seed,
                          r_min=r_min, r_max=r_max)

    if bed_files is not None:
        low, high = bed_files
        # `render_bed` skips the tracks' own intros (60s / 45s in) before
        # trimming, so "long enough" means the piece plus that offset. Trimmed,
        # never looped — a seam in the thing being listened to is the one
        # repetition a listener does notice.
        for src, skip in ((low, 60.0), (high, 45.0)):
            if audio_mod.duration_of(src) < total + skip:
                raise ValueError(
                    f"{src.name} is too short: a {total:.0f}s piece needs "
                    f"{total + skip:.0f}s of track after the {skip:.0f}s skip")
        # Fades off here — the long therapy fades below are the ones that apply.
        wav = short_asmr.render_bed(low, high, workdir / "bed.wav", total,
                                    fade_in=0.0, fade_out=0.0)
    else:
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

    def narrate(lines: list, name: str) -> tuple[Path, list, float]:
        track, caps, dur = build_narration_aligned(
            [list(s) for s in lines], workdir / name, gap=0.55,
            **profile_args(voice))
        return track, caps, dur

    intro_track, intro_caps = None, []
    outro_track, outro_caps = None, []
    if intro:
        intro_track, intro_caps, dur = narrate(intro, "intro")
        # The cards have to finish before the ring's entrance begins, or the
        # last line is still on screen while the circle grows through it.
        room = intro_len - intro_at - reveal
        if dur > room:
            raise ValueError(
                f"the intro narration is {dur:.1f}s but only {room:.1f}s fits "
                f"before the ring reveal — shorten it or raise intro_len")
    if outro:
        outro_track, outro_caps, dur = narrate(outro, "outro")
        room = outro_len - outro_at
        if dur > room:
            raise ValueError(
                f"the outro narration is {dur:.1f}s but the outro is only "
                f"{outro_len:.1f}s from {outro_at:.1f}s in")

    # Both voice blocks go into one track first, then that ducks the bed once.
    # Sidechaining twice would compress the bed against itself in the overlap
    # region and step it down further than either pass intends.
    audio = faded
    if intro_track or outro_track:
        outro_voice_at = intro_len + body + outro_at
        ins, filt, tags = [], [], []
        for track, at in ((intro_track, intro_at),
                          (outro_track, outro_voice_at)):
            if track is None:
                continue
            i = len(tags)               # input index, not len(ins) — `ins`
            ins += ["-i", str(track)]   # grows by two entries per input
            filt.append(f"[{i}:a]adelay={int(at * 1000)}|{int(at * 1000)},"
                        f"apad=whole_dur={total}[v{i}]")
            tags.append(f"[v{i}]")
        chain = ";".join(filt)
        if len(tags) > 1:
            chain += f";{''.join(tags)}amix=inputs={len(tags)}:normalize=0[vo]"
        else:
            chain = chain.replace(tags[0], "[vo]")
        both = workdir / "voice.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", *ins,
                        "-filter_complex", chain, "-map", "[vo]",
                        "-ar", "48000", "-ac", "2", str(both)],
                       check=True, capture_output=True)
        audio = audio_mod.mix_voice_over_bed(faded, both, workdir / "mix.wav",
                                             total, voice_at=0.0)

    head = render_bookend(workdir / "intro.mp4", brand, intro_len, intro_caps,
                          "intro", loop=loop, frame=frame, fps=fps, seed=seed,
                          r_min=r_min, r_max=r_max, reveal=reveal,
                          caption_at=intro_at)
    tail = render_bookend(workdir / "outro.mp4", brand, outro_len, outro_caps,
                          "outro", loop=loop, frame=frame, fps=fps, seed=seed,
                          r_min=r_min, r_max=r_max, reveal=reveal,
                          caption_at=outro_at)

    # The body, as its own file — `-stream_loop` and the concat demuxer cannot
    # be combined in one pass, and re-encoding the loop N times to stitch it
    # would give back the saving the loop exists for. Both steps are stream
    # copies.
    mid = workdir / "body.mp4"
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-stream_loop",
         str(int(round(body / loop)) - 1), "-i", str(picture),
         "-t", f"{body:.3f}", "-c", "copy", str(mid)],
        check=True, capture_output=True)

    listing = workdir / "segments.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in (head, mid, tail)))
    silent = workdir / "picture.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", str(silent)],
                   check=True, capture_output=True)

    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(silent), "-i", str(audio),
         "-map", "0:v", "-map", "1:a", "-t", f"{total:.3f}",
         "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", str(out)],
        check=True, capture_output=True)
    made = {"video": out, "total": total}

    # Scratch. Everything else this function made - the picture loop, the bed,
    # the mixed audio, the two bookends - lives in `workdir` and is an
    # intermediate. A therapy bed is minutes of uncompressed WAV, so this is the
    # heaviest scratch the repo produces. Deleted on success; a failed run keeps
    # it for debugging. Set keep_work=True while iterating on a cut, and note
    # the intermediate paths are only returned when they still exist - handing
    # back a path into a deleted directory is worse than not returning it.
    if keep_work:
        made.update({"loop": picture, "bed": faded, "audio": audio,
                     "intro": head, "outro": tail})
    else:
        shutil.rmtree(workdir, ignore_errors=True)

    return made
