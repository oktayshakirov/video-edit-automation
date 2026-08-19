"""ASMR / sound-therapy shorts — a masking bed, a breathing guide, a voice.

The format exists because a tinnitus short has something almost no other
wellness short has: the audio *is* the product. A talking head explaining
tinnitus competes with a million others; a sixty-second piece the viewer
actually listens to with headphones on does not.

Three layers, and they are built in this order because each one's timing
depends on the one before it:

1. **Narration** — `core.voiceover.build_narration_aligned`, same aligned-
   sentence machinery as the drone quotes. It returns measured caption spans,
   so the visual can be cut to the voice rather than the other way round.
2. **The breathing block** — a fixed pattern of phases dropped into a gap the
   narration leaves. Its captions are generated, not spoken: during the breath
   the voice is silent and the bed carries the piece.
3. **The picture** — a procedural nebula with a breathing ring drawn over it,
   piped frame by frame into ffmpeg.

Why procedural rather than stock: the brand's own sound album is *Quiet
Universe* and its artwork is space, so the visual is on-brand by construction,
there is no licence attached to it, and it can be regenerated at any length.
A drifting starfield also gives the eye something slow to track, which is the
opposite of what most short-form does and the right choice for a piece whose
whole purpose is to lower arousal.

**Nothing here makes a medical claim.** Partial masking and paced breathing are
described the way the blog describes them — as things people do, not as
treatment — and the copy never implies a cure.
"""

from __future__ import annotations

import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from ..core.frame import VERTICAL
from ..crypto.shots import roam_anchors
from ..core.vertical import (FONT_CAPTION, FONT_CAPTION_INDEX, OUT_H, OUT_W,
                             add_caption_emoji)

# tinnitushelp.me's own palette, straight from the app's `constants/Colors`.
# Using it means a short scrolled past on TikTok and the app's first screen
# read as the same product.
BG_DEEP = (18, 10, 26)          # near-black, the void behind everything
NEBULA_A = (91, 57, 100)        # #5B3964 — the app background
NEBULA_B = (255, 218, 185)      # #ffdab9 — the app highlight
RING = (255, 210, 166)          # #ffd2a6 — the app's active tint


@dataclass
class Phase:
    """One breath instruction: what to show, and the span it owns."""
    label: str
    start: float
    end: float
    kind: str                   # "inhale" | "hold" | "exhale"


def breathing_phases(start: float, cycles: int, inhale: float,
                     hold: float, exhale: float) -> list[Phase]:
    """Lay out a paced-breathing block.

    The default elsewhere in wellness content is box breathing (4-4-4-4). This
    uses a longer exhale than inhale, which is the pattern paced-breathing
    guidance generally favours — and it also happens to fit a short better,
    because the slow half is the half the viewer is watching the ring shrink.
    """
    phases: list[Phase] = []
    t = start
    for _ in range(cycles):
        for label, dur, kind in (("inhale", inhale, "inhale"),
                                 ("hold", hold, "hold"),
                                 ("exhale", exhale, "exhale")):
            if dur > 0:
                phases.append(Phase(label, t, t + dur, kind))
                t += dur
    return phases


def _ease(x: float) -> float:
    """Cosine ease. A linear ring looks mechanical; breath is not linear."""
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, x)))


def ring_radius(phases: list[Phase], t: float,
                r_min: float, r_max: float) -> tuple[float, str, float]:
    """Radius, label and seconds-remaining at time `t`.

    Returns r_min and an empty label outside the block, so the caller can draw
    the same ring code over the whole timeline without special-casing.
    """
    for p in phases:
        if p.start <= t < p.end:
            f = (t - p.start) / (p.end - p.start)
            if p.kind == "inhale":
                r = r_min + (r_max - r_min) * _ease(f)
            elif p.kind == "exhale":
                r = r_max - (r_max - r_min) * _ease(f)
            else:
                r = r_max
            return r, p.label, p.end - t
    return r_min, "", 0.0


# --- picture -------------------------------------------------------------

def _fbm(h: int, w: int, octaves: int, rng: np.random.Generator) -> np.ndarray:
    """Fractal value noise — the cloud structure of the nebula.

    Built by upsampling small random grids rather than with a noise library:
    cv2's cubic resize is the interpolation, and the repo already depends on it.
    """
    out = np.zeros((h, w), np.float32)
    amp = 1.0
    total = 0.0
    for o in range(octaves):
        n = 4 * 2 ** o
        grid = rng.random((n, int(n * w / h) + 1), dtype=np.float32)
        out += amp * cv2.resize(grid, (w, h), interpolation=cv2.INTER_CUBIC)
        total += amp
        amp *= 0.55
    return out / total


def nebula_canvas(w: int, h: int, seed: int = 7) -> np.ndarray:
    """One large still the video drifts across. RGB uint8."""
    rng = np.random.default_rng(seed)
    clouds = _fbm(h, w, 5, rng)
    # Push the midtones down so the frame is mostly void with a few bright
    # regions — an evenly lit nebula reads as fog and gives the drift nothing
    # to reveal.
    clouds = np.clip((clouds - 0.46) * 2.9, 0, 1) ** 1.9

    # A soft diagonal falloff, so brightness has a direction and the drift
    # actually changes the composition rather than sliding a uniform texture.
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    grad = 1.0 - np.clip(((xx / w) * 0.6 + (yy / h) * 0.7 - 0.15), 0, 1)
    clouds *= 0.35 + 0.65 * grad

    img = np.zeros((h, w, 3), np.float32)
    for c in range(3):
        img[..., c] = (BG_DEEP[c]
                       + clouds * (NEBULA_A[c] - BG_DEEP[c])
                       + np.clip(clouds - 0.55, 0, 1) * 1.9 * (NEBULA_B[c] - NEBULA_A[c]))

    # Stars last, so they sit on top of the cloud rather than being tinted by
    # it. Two populations. The faint ones give the drift something to measure
    # itself against; the bright ones are what actually reads on a phone. The
    # first pass at this used a cube law on the faint field and they vanished
    # entirely once the video was scaled down.
    stars = np.zeros((h, w), np.float32)
    ys, xs = rng.integers(0, h, 3200), rng.integers(0, w, 3200)
    stars[ys, xs] = 0.25 + 0.55 * rng.random(3200, dtype=np.float32)
    ys, xs = rng.integers(0, h, 160), rng.integers(0, w, 160)
    stars[ys, xs] = 1.0
    stars = cv2.GaussianBlur(stars, (0, 0), 0.9)
    stars /= stars.max()
    bloom = cv2.GaussianBlur(stars, (0, 0), 7.0) * 0.7
    img += ((stars * 1.15 + bloom) * 255)[..., None]

    return np.clip(img, 0, 255).astype(np.uint8)


def _ring_sprite(r_max: int) -> Image.Image:
    """The breathing disc at full size, drawn once and scaled per frame.

    Redrawing the glow every frame is the expensive way to do this and looks
    identical — the shape is radially symmetric, so a resize is exact.
    """
    s = r_max * 2 + 80
    c = s // 2
    box = [c - r_max, c - r_max, c + r_max, c + r_max]

    # The rim glows; the fill does not. Blurring a filled disc pushed a haze
    # over the whole circle and the nebula behind it went to mud — the disc has
    # to stay a window onto the background, not a lens cap.
    rim = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(rim).ellipse(box, outline=RING + (255,), width=7)
    sprite = rim.filter(ImageFilter.GaussianBlur(14))

    fill = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(fill).ellipse(box, fill=RING + (26,))
    sprite.alpha_composite(fill)
    sprite.alpha_composite(rim)
    return sprite


MASCOT = Path.home() / "Coding/tinnitus-app/assets/images/splash-icon.png"

# The union of what TikTok, Reels and Shorts each cover with their own UI, at
# 1080x1920. All three stack buttons down the right edge and text along the
# bottom; the top band carries tabs on TikTok and the Reels label on Instagram.
# Anything persistent has to live inside this box.
SAFE_TOP, SAFE_BOTTOM = VERTICAL.safe_top, VERTICAL.safe_bottom


def _mascot(height: int, opacity: int) -> Image.Image | None:
    """The app's mascot, trimmed to the face and dimmed.

    Taken from the live app rather than redrawn, so what a viewer sees is
    exactly the icon they will be looking for in the store. The splash asset
    carries a faint wordmark under the face and the alpha bounding box includes
    it, so the crop comes off the top 82% rather than straight from `getbbox`.
    """
    if not MASCOT.exists():
        return None
    im = Image.open(MASCOT).convert("RGBA")
    im = im.crop((0, 0, im.width, int(im.height * 0.82)))
    im = im.crop(im.getbbox())
    w = int(im.width * height / im.height)
    im = im.resize((w, height), Image.LANCZOS)
    im.putalpha(im.split()[-1].point(lambda v: int(v * opacity / 255)))
    return im


def brand_lockup(height: int, opacity: int, wordmark: str,
                 font_path: str, font_index: int,
                 word_size: int = 27) -> Image.Image | None:
    """Mascot with the domain under it, as one watermark.

    Sits in the **upper-left, inset below the chrome band** — not flush to the
    corner and not centred. Flush-to-the-corner is where TikTok's LIVE button
    and Instagram's camera/plus live; dead centre was tried and reads as part of
    the piece rather than as a mark. Inset to `brand_at` it is off to one side,
    which is what a watermark should be, and still inside every platform's safe
    area.

    Drawn at full opacity. A dimmed watermark is a watermark nobody can read,
    and the whole point of carrying the domain is that it is actionable — the
    site prompts for the app install on arrival, so one legible URL does the
    work an end card was doing.
    """
    face = _mascot(height, opacity)
    if face is None:
        return None
    font = ImageFont.truetype(font_path, word_size, index=font_index)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(probe.textlength(wordmark, font=font))
    gap = 12

    w = max(face.width, tw) + 8
    h = face.height + gap + int(word_size * 1.3) + 2
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.alpha_composite(face, ((w - face.width) // 2, 0))

    d = ImageDraw.Draw(out)
    y = face.height + gap
    # A one-pixel dark offset rather than a stroke: at 30px a stroke closes up
    # the counters, and the background is dark enough that this only has to
    # survive the occasional bright nebula patch.
    d.text(((w - tw) // 2 + 1, y + 1), wordmark, font=font,
           fill=(0, 0, 0, int(opacity * 0.55)))
    d.text(((w - tw) // 2, y), wordmark, font=font,
           fill=(255, 255, 255, min(255, int(opacity * 1.25))))
    return out


def render_visual(out: Path, duration: float, phases: list[Phase],
                  fps: int = 30, seed: int = 7,
                  r_min: int = 150, r_max: int = 330,
                  mascot_h: int = 100, mascot_opacity: int = 255,
                  wordmark: str = "TinnitusHelp.me",
                  brand_at: tuple[int, int] = (58, 292),
                  brand_float: float = 9.0, brand_period: float = 5.5,
                  brand_roam: bool = False, brand_hold: float = 13.0,
                  font_path: str = FONT_CAPTION,
                  font_index: int = FONT_CAPTION_INDEX) -> Path:
    """Drifting nebula with the breathing ring, straight into ffmpeg.

    Frames are piped as rawvideo rather than written out — a minute at 1080x1920
    is 1800 PNGs and none of them are wanted afterwards.

    `brand_roam` moves the lockup between `brand_at` and a lower-right anchor,
    cutting every `brand_hold` seconds — see `crypto.shots.roam_anchors` for
    why, and for how the second anchor is placed. Off by default, so the
    shipped sound-therapy shorts are unchanged.
    """
    pad_x, pad_y = 220, 320
    cw, ch = OUT_W + pad_x, OUT_H + pad_y
    canvas = nebula_canvas(cw, ch, seed)

    sprite = _ring_sprite(r_max)
    label_font = ImageFont.truetype(font_path, 52, index=font_index)
    count_font = ImageFont.truetype(font_path, 116, index=font_index)

    brand = brand_lockup(mascot_h, mascot_opacity, wordmark,
                         font_path, font_index)
    anchors = [tuple(brand_at)]
    if brand and brand_roam:
        anchors = roam_anchors(brand, VERTICAL, brand_at, brand_float)
    if brand and len(anchors) == 1:
        if brand_at[1] - brand_float < SAFE_TOP:
            raise ValueError(
                f"brand_at={brand_at} with float {brand_float} reaches "
                f"y={brand_at[1] - brand_float:.0f}, inside the platform UI band "
                f"(safe from {SAFE_TOP})")
    elif brand:
        # **Every anchor, not just the first.** The lower-right one is bounded
        # on two axes where the upper-left one is bounded on neither, so the
        # single top check that has always guarded `brand_at` would pass a mark
        # sitting squarely under the share button.
        for a in anchors:
            VERTICAL.check_mark(a[0], a[1] - brand_float, brand.width,
                                brand.height + 2 * brand_float, f"anchor {a}")

    # A little longer than asked. The final mux runs `-shortest` against the
    # audio, so a picture that lands a few frames short silently clips the end
    # card rather than erroring.
    n = int(round(duration * fps)) + fps // 2
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y",
         "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{OUT_W}x{OUT_H}", "-r", str(fps), "-i", "-",
         "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", str(out)],
        stdin=subprocess.PIPE)

    for i in range(n):
        t = i / fps
        # Subpixel translation, and it has to be subpixel. The drift is slow by
        # design — tens of pixels per second — so an integer crop jumps a whole
        # pixel every few frames and holds still in between. That reads as
        # judder, which is exactly the wrong quality for a piece whose purpose
        # is to lower arousal. warpAffine at INTER_LINEAR costs a few ms a
        # frame and the motion goes glassy. Two axes on different periods, so
        # the drift never visibly repeats inside a minute.
        fx = pad_x * (0.5 + 0.5 * math.sin(t / 19.0))
        fy = pad_y * (0.5 + 0.5 * math.sin(t / 29.0 + 1.1))
        ix, iy = int(fx), int(fy)
        m = np.float32([[1, 0, ix - fx], [0, 1, iy - fy]])
        frame = Image.fromarray(cv2.warpAffine(
            canvas[iy:iy + OUT_H + 1, ix:ix + OUT_W + 1], m, (OUT_W, OUT_H),
            flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE))

        r, label, left = ring_radius(phases, t, r_min, r_max)
        if label or brand is not None:
            frame = frame.convert("RGBA")
        if brand is not None:
            # Levitation. A static watermark in a corner is dead weight the
            # eye learns to skip in about two seconds; a slow bob on a period
            # sharing no factor with the 10s breathing cycle keeps it alive
            # without ever syncing up into a second thing to follow.
            #
            # Subpixel, for the same reason the background drift is: the bob
            # peaks around 10px/s, so rounding to whole pixels would make the
            # logo stutter against a background that no longer does.
            #
            # When it roams it **cuts** between anchors and keeps bobbing at
            # each one. A lockup sliding across the frame would be a second
            # travelling object competing with the ring, which is the one thing
            # the viewer is here to follow — the strongest reason of all to cut
            # in this format specifically. `brand_hold` shares no factor with
            # the breathing cycle either, so the jump never lands on the same
            # phase twice.
            ax, ay = anchors[int(t // brand_hold) % len(anchors)]
            by = ay + brand_float * math.sin(2 * math.pi * t / brand_period)
            iy = math.floor(by)
            frame.alpha_composite(
                brand.transform(brand.size, Image.AFFINE,
                                (1, 0, 0, 0, 1, iy - by),
                                resample=Image.BILINEAR),
                (ax, iy))
        if label:
            k = int(r * 2 + 80)
            frame.alpha_composite(sprite.resize((k, k), Image.LANCZOS),
                                  (OUT_W // 2 - k // 2, OUT_H // 2 - k // 2))
            d = ImageDraw.Draw(frame)
            _centred(d, label, OUT_H // 2 - 104, label_font)
            # +1 so a 4s phase counts 4,3,2,1 rather than 3,2,1,0 — the number
            # is the seconds remaining, and nobody breathes to a zero.
            _centred(d, str(int(left) + 1), OUT_H // 2 + 4, count_font)
        if frame.mode == "RGBA":
            frame = frame.convert("RGB")

        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    if proc.wait() != 0:
        raise RuntimeError("ffmpeg failed while encoding the visual")
    return out


def _centred(draw: ImageDraw.ImageDraw, text: str, y: int,
             font: ImageFont.FreeTypeFont) -> None:
    """Ring labels, drawn without the caption stroke.

    The narration captions are stroked because they cross live footage. These
    sit on a background this module generated, so the contrast is known and a
    black border would only make them heavier than the moment wants.
    """
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
    draw.text(((OUT_W - (x1 - x0)) // 2 - x0, y - y0), text,
              font=font, fill=(255, 255, 255, 235))


# --- sound ---------------------------------------------------------------

def render_bed(low: Path, high: Path, out: Path, duration: float,
               low_in: float = 60.0, high_in: float = 45.0,
               low_gain: float = 1.0, high_gain: float = 0.85,
               fade_in: float = 2.5, fade_out: float = 3.5) -> Path:
    """Mix the two source tracks into one masking bed.

    Both are needed, and measurement is why. Sampled at 30s: SpaceshipAmbience
    puts 87% of its energy below 200Hz and effectively nothing above 1kHz — a
    beautiful floor, but it masks nothing in the band most tinnitus actually
    sits in. NebulaPulse carries the mid and upper content. Layered, the bed has
    both a body and something that reaches the ringing.

    Honest limit, worth repeating to whoever writes the copy: even mixed, there
    is little energy above 4kHz, so a high whistling tinnitus will not be well
    covered. That is a property of these two tracks, not of the method.
    """
    filt = (
        f"[0:a]atrim=start={low_in}:duration={duration},asetpts=N/SR/TB,"
        f"volume={low_gain}[lo];"
        f"[1:a]atrim=start={high_in}:duration={duration},asetpts=N/SR/TB,"
        f"volume={high_gain}[hi];"
        f"[lo][hi]amix=inputs=2:duration=shortest:normalize=0,"
        f"loudnorm=I=-23:TP=-2:LRA=7,"
        f"afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={max(duration - fade_out, 0):.2f}:d={fade_out}[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(low), "-i", str(high),
                    "-filter_complex", filt, "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(out)],
                   check=True, capture_output=True)
    return out


def mix_voice_over_bed(bed: Path, voice: Path, out: Path, duration: float,
                       voice_at: float = 0.0) -> Path:
    """Lay the narration over the bed, ducking the bed under it.

    Sidechain rather than a fixed level: the bed should be at full strength
    during the breathing block, which is most of the piece, and only step back
    where there are words. A static mix has to choose one or the other.
    """
    filt = (
        f"[1:a]adelay={int(voice_at * 1000)}|{int(voice_at * 1000)},"
        f"apad=whole_dur={duration}[vo];"
        f"[vo]asplit=2[vo1][key];"
        f"[0:a][key]sidechaincompress=threshold=0.03:ratio=8:attack=15:"
        f"release=500:makeup=1[duck];"
        f"[duck][vo1]amix=inputs=2:duration=first:normalize=0,"
        f"alimiter=limit=0.95[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bed), "-i", str(voice),
                    "-filter_complex", filt, "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(out)],
                   check=True, capture_output=True)
    return out


# --- assembly ------------------------------------------------------------

def render_asmr_short(intro: list, outro: list, low: Path, high: Path,
                      out: Path, workdir: Path,
                      cycles: int = 3, inhale: float = 4.0,
                      hold: float = 0.0, exhale: float = 6.0,
                      voice: str = "luna-calm",
                      end_card: str | None = None, end_card_hold: float = 3.0,
                      emoji: dict[str, str] | None = None,
                      lead_in: float = 0.0, gap: float = 0.6,
                      font_size: int = 44, y_frac: float = 0.50,
                      fps: int = 30, seed: int = 7,
                      roam: bool = False, logo_hold: float = 13.0,
                      keep_work: bool = False) -> tuple[Path, float]:
    """Narration, breathing block, bed and picture into one vertical MP4.

    The two narration blocks are synthesised separately rather than as one call
    with a very long `gap`. `build_narration_aligned` holds each caption until
    the next one starts, which is right everywhere else and wrong here — it
    would leave "now breathe with the circle" on screen for the entire breathing
    block, on top of the ring. Two calls give both blocks natural caption ends
    and put the seam exactly where the breathing starts.
    """
    from ..core.vertical import render_text_png
    from ..core.voiceover import CAPTION_MAX_W
    from ..core.voiceover import build_narration_aligned, profile_args

    workdir.mkdir(parents=True, exist_ok=True)
    args = profile_args(voice)

    a_track, a_caps, a_total = build_narration_aligned(
        [list(s) for s in intro], workdir / "intro", gap=gap, tail=0.0, **args)
    b_track, b_caps, b_total = build_narration_aligned(
        [list(s) for s in outro], workdir / "outro", gap=gap,
        tail=end_card_hold if end_card else 1.2, **args)

    phases = breathing_phases(lead_in + a_total, cycles, inhale, hold, exhale)
    breath = cycles * (inhale + hold + exhale)
    total = lead_in + a_total + breath + b_total

    captions = [(c.text, lead_in + c.start, lead_in + c.end) for c in a_caps]
    off = lead_in + a_total + breath
    captions += [(c.text, off + c.start, off + c.end) for c in b_caps]
    if end_card:
        # The last spoken caption is held through the tail by
        # `build_narration_aligned`, and the tail is exactly where the end card
        # goes — without this clamp the two overlay on top of each other.
        card_at = total - end_card_hold
        text, s, e = captions[-1]
        captions[-1] = (text, s, min(e, card_at))
        captions.append((end_card, card_at, total))

    # Audio: lead-in silence, intro, the breathing block, outro.
    order = []
    for name, dur in (("lead", lead_in), ("breath", breath)):
        if dur <= 0:                       # lead_in is 0 by default; see above
            order.append(None)
            continue
        p = workdir / f"{name}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                        f"anullsrc=r=48000:cl=stereo:d={dur}", str(p)],
                       check=True, capture_output=True)
        order.append(p)
    listing = workdir / "voice.txt"
    listing.write_text("\n".join(
        f"file '{p}'" for p in (order[0], a_track, order[1], b_track)
        if p is not None), encoding="utf-8")
    narration = workdir / "narration.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", str(narration)],
                   check=True, capture_output=True)

    bed = render_bed(low, high, workdir / "bed.wav", total)
    audio = mix_voice_over_bed(bed, narration, workdir / "mix.wav", total)

    picture = render_visual(workdir / "picture.mp4", total, phases,
                            fps=fps, seed=seed,
                            brand_roam=roam, brand_hold=logo_hold)

    pngs = []
    for i, (text, _, _) in enumerate(captions):
        p = workdir / f"cap{i:02d}.png"
        # bg_luma 0 keeps the ink white: the nebula is dark by construction, so
        # there is nothing to sample and nothing that would justify black type.
        # CAPTION_MAX_W, not the default — that default is the silent quote
        # card's narrower 780px, and it wraps a caption that would otherwise
        # have set on one line.
        render_text_png(text, p, size=font_size, bg_luma=0.0,
                        font_path=FONT_CAPTION, font_index=FONT_CAPTION_INDEX,
                        y_frac=y_frac, stroke=4, max_w=CAPTION_MAX_W)
        if emoji and text in emoji:
            add_caption_emoji(p, text, emoji[text], font_size, y_frac,
                              FONT_CAPTION, FONT_CAPTION_INDEX)
        pngs.append(p)

    chain = []
    prev = "[0:v]"
    for n, (_, s, e) in enumerate(captions):
        dst = f"[v{n+1}]"
        chain.append(f"{prev}[{n+1}:v]overlay=0:0:"
                     f"enable='between(t,{s:.3f},{e:.3f})'{dst}")
        prev = dst
    filt = ";".join(chain) if chain else None

    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(picture)]
    for p in pngs:
        cmd += ["-i", str(p)]
    cmd += ["-i", str(audio)]
    if filt:
        cmd += ["-filter_complex", filt, "-map", prev]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-map", f"{len(pngs)+1}:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)

    # Scratch. Intermediates only - narration and bed WAVs, the silent picture
    # pass, per-shot PNGs. Deleted on success so a run leaves only what ships;
    # a failed run keeps everything needed to debug it. Set keep_work=True while
    # iterating on a cut.
    if not keep_work:
        shutil.rmtree(workdir, ignore_errors=True)

    return out, total
