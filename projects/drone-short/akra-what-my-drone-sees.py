"""Akra What My Drone Sees — the POV/reveal format at Akra Castle, Sozopol.

Built on `spree-what-my-drone-sees.py`, but delivered in SDR — see *Colour*.
Cut to a TikTok sound the user supplied, every cut on one of its strong hits
(~2.527s apart); see `HITS`.

1. **what i see** — the first 4s of a phone clip of the RC controller held by
   the car, which then pans up to the Akra headland itself.
2. **what my drone sees** — `Coast 2`, the headland and the isthmus to
   Sozopol. It is the place the phone just panned to, so it leads the air half.
3. `Coast 8`, top-down along the cliffs.
4. `Castle Bulgarian Flag`, the ruins and the flag against the sunset.

The user's brief: first 4s of the controller, then parts of the other three
sped up, 15-20s overall. Revised on review: every shot at normal speed.

## Colour: SDR out, drone clips untouched

**The first six renders were HLG, like Spree, and the HLG step was the bug.**
The controller is iPhone HLG, so the file was HLG and the SDR drone clips were
lifted into it with Spree's matched conversion (`eq` saturation 0.66, gamma
1.20, 709 to 2020 primaries). On the user's phone that conversion did not give
back the source: an ungraded clip came out drained ("missing colours"), and
grading against the drain overshot into a neon cyan sky and orange cliffs on
Coast 2. Every grading round was correcting the conversion, not the footage.
The untonemapped stills used for checking hid all of it.

**The fix runs the other way.** The controller clip is tone-mapped down to SDR
BT.709 once, with VideoToolbox (`scale_vt`, the same tone map an iPhone or Mac
applies on an SDR screen), and the file is plain 8-bit 709. The drone clips
are 709 already, so they go through with **no colour conversion and no
grade** — crop and scale only, and they look exactly as they came off the
drone.

The tone-mapped controller measures YLOW 45-60 / SATAVG 14-22 against the
drone shots' ~40-56 / 13-29, so it takes a small saturation lift to sit with
them; see `POV_GRADE`.

`scale_vt` wants the clip un-rotated (`-noautorotate`, then `transpose=1` for
the iPhone's -90) and downloads as `p010le`; `nv12` is refused.

## Motion

**Crops are hand-set and fixed.** The first cuts tracked the subject at 40-50
px/s, which is 1.3-1.7px a frame, and a yuv420 crop can only land on even
pixels. The box stepped 2, 2, 0 and the user saw it as lag; per-frame YDIF
showed the dip every third frame. At normal speed nothing leaves a fixed box
within its beat. If a pan is ever needed, it must not be an integer crop.

**60fps out.** The phone clip is 60fps and 30 made its pan judder; the 30fps
drone clips show each frame twice, which adds no judder of its own.
"""

import subprocess
from pathlib import Path

from video_automation.core.vertical import OUT_H, OUT_W, render_text_png

SOURCE_POST = None                      # off-site: a format piece, no article

POV = Path("~/Desktop/Drone Videos/Controller/IMG_1439.MOV").expanduser()
AKRA = Path("~/Desktop/Drone Videos/Footage/Akra Castle").expanduser()

OUT = Path("~/Desktop/akra-what-my-drone-sees.mp4").expanduser()
WORK = Path("~/Desktop/.work-akra-what-my-drone-sees").expanduser()

FPS = 60
CROP_W = 1215                           # 9:16 out of a 2160-line frame

POV_SPAN = 4.0                          # first 4s, real video, played straight
POV_GRADE = "eq=saturation=1.30:contrast=1.04"   # after the tone map
TONEMAP = ("scale_vt=w=1920:h=1080:color_matrix=bt709:color_primaries=bt709:"
           "color_transfer=bt709,hwdownload,format=p010le,transpose=1")

# The track: strong hits every ~2.527s. The bed starts AUDIO_IN so the first
# cut (end of the controller beat) lands on the 17.871 hit, and every later
# cut and the end land on the next hits, measured at a 3ms hop.
SOUND = Path("~/Downloads/v24044gl0000d34jdnvog65k02okpo0g.MP4").expanduser()
HITS = [17.871, 22.921, 27.974, 33.027]   # cut 1, cut 2, cut 3, end
AUDIO_IN = HITS[0] - POV_SPAN

# (file, in-point, crop x). Normal speed, fixed crop, no grade.
SHOTS = [
    ("Coast 2.mp4", 0.0, 1350),
    ("Coast 8.mp4", 0.0, 900),
    ("Castle Bulgarian Flag.mp4", 0.0, 2550),
]

POV_LABEL_SIZE = 42
DRONE_LABEL_SIZE = 34
LABEL_LUMA = 0.0                        # white ink, dark halo
POV_LABEL_Y = 0.38                      # above the controller in the hand
DRONE_LABEL_Y = 0.50
DRONE_LABEL_OUT = 2.5

LABEL_POV = "what i see"
LABEL_DRONE = "what my drone sees"

SDR_TAGS = ["-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709", "-color_range", "tv"]
X264 = ["-c:v", "libx264", "-crf", "16", "-preset", "slow",
        "-profile:v", "high", "-pix_fmt", "yuv420p"]


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def _probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def _encode(dst: Path, inputs: list[str], vf: str, frames: int) -> Path:
    _run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", vf,
          "-map", "[o]", "-frames:v", str(frames), "-an", *X264, *SDR_TAGS,
          str(dst)])
    return dst


def _segment_pov(dst: Path, label: Path, frames: int) -> Path:
    """Beat one: the first POV_SPAN seconds, tone-mapped to SDR, labelled."""
    vf = (f"[0:v]{TONEMAP},scale={OUT_W}:{OUT_H}:flags=lanczos,"
          f"format=yuv420p,{POV_GRADE},"
          f"setpts=PTS-STARTPTS,fps={FPS},setsar=1[v];"
          f"[v][1:v]overlay=0:0,format=yuv420p[o]")
    return _encode(dst, ["-noautorotate", "-hwaccel", "videotoolbox",
                         "-hwaccel_output_format", "videotoolbox_vld",
                         "-t", f"{POV_SPAN}", "-i", str(POV), "-i", str(label)],
                   vf, frames)


def _segment_drone(dst: Path, shot: tuple, frames: int,
                   label: Path | None) -> Path:
    """A drone shot: fixed crop and scale, nothing else, optional label."""
    name, start, x = shot
    chain = (f"[0:v]crop={CROP_W}:2160:{x}:0,scale={OUT_W}:{OUT_H}:flags=lanczos,"
             f"setpts=PTS-STARTPTS,fps={FPS},setsar=1")
    if label:
        vf = (f"{chain}[v];[v][1:v]overlay=0:0:"
              f"enable='lt(t,{DRONE_LABEL_OUT})'")
        extra = ["-i", str(label)]
    else:
        vf, extra = chain, []
    vf += ",format=yuv420p[o]"
    return _encode(dst, ["-ss", f"{start}", "-t", f"{frames / FPS + 0.5}",
                         "-i", str(AKRA / name), *extra], vf, frames)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)

    pov_png = render_text_png(LABEL_POV, WORK / "label-pov.png",
                              size=POV_LABEL_SIZE, y_frac=POV_LABEL_Y,
                              bg_luma=LABEL_LUMA)
    drone_png = render_text_png(LABEL_DRONE, WORK / "label-drone.png",
                                size=DRONE_LABEL_SIZE, y_frac=DRONE_LABEL_Y,
                                bg_luma=LABEL_LUMA)

    marks = [round((h - AUDIO_IN) * FPS) for h in HITS]
    frames = [marks[0]] + [b - a for a, b in zip(marks, marks[1:])]
    parts = [_segment_pov(WORK / "a.mp4", pov_png, frames[0])]
    for i, (shot, n) in enumerate(zip(SHOTS, frames[1:])):
        parts.append(_segment_drone(WORK / f"{'bcd'[i]}.mp4", shot, n,
                                    drone_png if i == 0 else None))

    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    silent = WORK / "video.mp4"
    _run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", str(listing), "-c", "copy", str(silent)])

    total = marks[-1] / FPS
    _run(["ffmpeg", "-v", "error", "-y", "-i", str(silent),
          "-ss", f"{AUDIO_IN}", "-t", f"{total}", "-i", str(SOUND),
          "-map", "0:v", "-map", "1:a", "-c:v", "copy",
          "-af", f"afade=t=out:st={total - 0.04:.3f}:d=0.04",
          "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
          "-t", f"{total}", "-movflags", "+faststart", str(OUT)])

    cuts = ", ".join(f"{m / FPS:.3f}s" for m in marks[:-1])
    print(f"{OUT}  {_probe(OUT):.3f}s  cuts at {cuts}, track in at "
          f"{AUDIO_IN:.3f}s")


if __name__ == "__main__":
    main()
