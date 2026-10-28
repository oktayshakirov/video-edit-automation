"""Akra What My Drone Sees — the POV/reveal format at Akra Castle, Sozopol.

Built on `spree-what-my-drone-sees.py`. HLG out, like Spree, but with an
exact SDR-to-HLG conversion — see *Colour*.
Cut to a TikTok sound the editor supplied, every cut on one of its strong hits
(~2.527s apart); see `HITS`.

1. **what i see** — the first 4s of a phone clip of the RC controller held by
   the car, which then pans up to the Akra headland itself.
2. **what my drone sees** — `Coast 2`, the headland and the isthmus to
   Sozopol. It is the place the phone just panned to, so it leads the air half.
3. `Coast 8`, top-down along the cliffs.
4. `Castle Bulgarian Flag`, the ruins and the flag against the sunset.

The editor's brief: first 4s of the controller, then parts of the other three
sped up, 15-20s overall. Revised on review: every shot at normal speed.

## Colour: HLG out, drone clips converted exactly

**The first six renders were HLG with Spree's conversion, and it was the
bug.** Spree lifts SDR into HLG with a pre-trim (`eq` saturation 0.66, gamma
1.20) matched by tone-mapping the result back to SDR with `scale_vt`. That is
what an SDR screen shows. The user watches on an HDR phone, which shows the
HLG as it is, and there the trim stays in: modelled on a 1000-nit HLG
display, Coast 2's display-light saturation went 0.80 to 0.66 — "missing
colours". Grading against that overshot into a neon sky and orange cliffs.

**Render seven went SDR** — controller tone-mapped with `scale_vt`, drone
clips untouched — and fixed the colour, but gave up the HDR.

**This one is HLG with an exact conversion** (`video_automation/core/hdr.py`):
BT.1886 decode, SDR white at `DRONE_WHITE` nits, 709 to 2020 primaries,
inverse HLG OOTF and OETF, baked to a 65-point .cube for `lut3d`. On the same
display model Coast 2 comes out at 0.798 saturation against 0.800 in the
source, at the source's brightness. The drone clips get no grade.

**`DRONE_WHITE` is 400 nits.** The old conversion put drone midtones at about
the brightness of a 260-nit white and highlights near 1000; 400 keeps the
brightness the editor had seen (mean 83 nits on Coast 2 against the old 93)
without pushing the sky into the peak. The iPhone clip runs brighter, ~180
nits mean, which is the phone's HDR look; raise `DRONE_WHITE` to close the gap.

The controller clip stays native HLG with the grade the editor approved in
round two. Labels: the drone label goes through the LUT with the picture, so
its white lands at `DRONE_WHITE`; the controller label is dimmed to the same
HLG signal.

## Motion

**Crops are hand-set and fixed.** The first cuts tracked the subject at 40-50
px/s, which is 1.3-1.7px a frame, and a yuv420 crop can only land on even
pixels. The box stepped 2, 2, 0 and the editor saw it as lag; per-frame YDIF
showed the dip every third frame. At normal speed nothing leaves a fixed box
within its beat. If a pan is ever needed, it must not be an integer crop.

**60fps out.** The phone clip is 60fps and 30 made its pan judder; the 30fps
drone clips show each frame twice, which adds no judder of its own.
"""

import subprocess
from pathlib import Path

from video_automation.core.hdr import hlg_signal_of_white, write_sdr_to_hlg_cube
from video_automation.core.vertical import OUT_H, OUT_W, render_text_png

SOURCE_POST = None                      # off-site: a format piece, no article

POV = Path("~/Desktop/Drone Videos/Controller/IMG_1439.MOV").expanduser()
AKRA = Path("~/Desktop/Drone Videos/Footage/Akra Castle").expanduser()

OUT = Path("~/Desktop/akra-what-my-drone-sees.mp4").expanduser()
WORK = Path("~/Desktop/.work-akra-what-my-drone-sees").expanduser()

FPS = 60
CROP_W = 1215                           # 9:16 out of a 2160-line frame

POV_SPAN = 4.0                          # first 4s, real video, played straight
POV_GRADE = "eq=contrast=1.25:brightness=-0.08:gamma=0.95:saturation=1.5"

DRONE_WHITE = 400                       # nits SDR white lands at in the HLG file
HLG_PARAMS = ("setparams=color_primaries=bt2020:color_trc=arib-std-b67:"
              "colorspace=bt2020nc:range=tv")

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

HLG_TAGS = ["-color_primaries", "bt2020", "-color_trc", "arib-std-b67",
            "-colorspace", "bt2020nc", "-color_range", "tv"]
X265 = ["-c:v", "libx265", "-crf", "18", "-preset", "slow", "-tag:v", "hvc1",
        "-pix_fmt", "yuv420p10le",
        "-x265-params", "log-level=error:colorprim=bt2020:"
                        "transfer=arib-std-b67:colormatrix=bt2020nc:range=limited"]


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
          "-map", "[o]", "-frames:v", str(frames), "-an", *X265, *HLG_TAGS,
          str(dst)])
    return dst


def _segment_pov(dst: Path, label: Path, frames: int) -> Path:
    """Beat one, native HLG: the first POV_SPAN seconds, graded, labelled."""
    k = hlg_signal_of_white(DRONE_WHITE)
    vf = (f"[0:v]scale={OUT_W}:{OUT_H}:flags=lanczos,{POV_GRADE},"
          f"setpts=PTS-STARTPTS,fps={FPS},format=yuv420p10le,setsar=1[v];"
          f"[1:v]format=rgba,colorchannelmixer=rr={k}:gg={k}:bb={k}[l];"
          f"[v][l]overlay=0:0:format=yuv420p10,format=yuv420p10le,"
          f"{HLG_PARAMS}[o]")
    return _encode(dst, ["-t", f"{POV_SPAN}", "-i", str(POV), "-i", str(label)],
                   vf, frames)


def _segment_drone(dst: Path, shot: tuple, frames: int,
                   label: Path | None, cube: Path) -> Path:
    """A drone shot: fixed crop and scale, optional label, exact SDR to HLG."""
    name, start, x = shot
    chain = (f"[0:v]crop={CROP_W}:2160:{x}:0,scale={OUT_W}:{OUT_H}:flags=lanczos,"
             f"setpts=PTS-STARTPTS,fps={FPS},setsar=1")
    if label:
        vf = (f"{chain}[v];[v][1:v]overlay=0:0:"
              f"enable='lt(t,{DRONE_LABEL_OUT})'")
        extra = ["-i", str(label)]
    else:
        vf, extra = chain, []
    vf += (f",format=rgb48le,lut3d=file='{cube}':interp=tetrahedral,"
           f"scale=out_color_matrix=bt2020:out_range=tv,format=yuv420p10le,"
           f"{HLG_PARAMS}[o]")
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

    cube = write_sdr_to_hlg_cube(WORK / f"sdr-to-hlg-{DRONE_WHITE}.cube",
                                 DRONE_WHITE)

    marks = [round((h - AUDIO_IN) * FPS) for h in HITS]
    frames = [marks[0]] + [b - a for a, b in zip(marks, marks[1:])]
    parts = [_segment_pov(WORK / "a.mp4", pov_png, frames[0])]
    for i, (shot, n) in enumerate(zip(SHOTS, frames[1:])):
        parts.append(_segment_drone(WORK / f"{'bcd'[i]}.mp4", shot, n,
                                    drone_png if i == 0 else None, cube))

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
