"""Cingene What My Drone Sees - the POV/reveal format at sunset on the Cingene shore.

Built on `sinemorets-what-my-drone-sees.py`: HLG out, because the controller
clip is an iPhone HLG video, with the drone clip lifted by the exact
SDR-to-HLG LUT. Silent, no audio track - the editor lays the sound on the
platform.

1. **what i see** - `IMG_1430.MOV` 3-9s, the controller in the car with the
   sunset on its screen, a pan across the car, then the same sunset through
   the window. Real video, so played straight, no boomerang.
2. **what my drone sees** - `Sunset Sea 3` 0-9s at 1x, the sun and its track
   on the water centred. The clip is 30fps, every frame shown twice at 60.

The editor's brief: controller 0:03-0:09, then Sunset Sea 3 0:00-0:09.

## Grade

Measured at 3, 6 and 8.9s the controller reads YLOW ~180/1023, YAVG ~490 and
SATAVG ~36 (10-bit) - less lifted and darker than Sinemorets (360 / 612 / 43),
so a lighter version of that grade: less contrast, almost no brightness pull.

Sunset Sea 3 reads YLOW 64, YAVG 124, SATAVG 23.5 across the clip. The average
is grey water; the colour sits in the sky and the sun's track, and a lift
lands there as neon (the Golden Girl night lesson). No grade.
"""

import subprocess
import sys
from pathlib import Path

from video_automation.core.hdr import hlg_signal_of_white, write_sdr_to_hlg_cube
from video_automation.core.vertical import OUT_H, OUT_W, render_text_png

SOURCE_POST = None                      # off-site: a format piece, no article

POV = Path("~/Desktop/Drone Videos/Controller/IMG_1430.MOV").expanduser()
DRONE = Path("~/Desktop/Drone Videos/Footage/Cingene/Sunset Sea 3.mp4").expanduser()

# Two label inks, built side by side for the editor to pick one:
#   white - white ink, dark halo (bg_luma 0), the approved POV look
#   black - near-black ink, soft white halo (bg_luma 1, the renderer's own
#           dark-text mode), asked for 2026-11-07 against the bright sunset
INKS = {"white": (0.0, ""), "black": (1.0, "-black")}
INK = sys.argv[1] if len(sys.argv) > 1 else "white"
LABEL_LUMA, _SUFFIX = INKS[INK]

OUT = Path(f"~/Desktop/cingene-what-my-drone-sees{_SUFFIX}.mp4").expanduser()
WORK = Path("~/Desktop/.work-cingene-what-my-drone-sees").expanduser()

FPS = 60
CROP_W = 1215                           # 9:16 out of a 2160-line frame

POV_IN = 3.0
POV_SPAN = 6.0                          # 0:03-0:09, played straight
POV_GRADE = "eq=contrast=1.12:brightness=-0.03:saturation=1.4"

DRONE_IN = 0.0
DRONE_SPEED = 1.0
DRONE_SPAN = 9.0                        # 0:00-0:09, at 1x
DRONE_X = 1515                          # sun at x~2124 both ends, centred

DRONE_WHITE = 400                       # nits SDR white lands at in the HLG file
HLG_PARAMS = ("setparams=color_primaries=bt2020:color_trc=arib-std-b67:"
              "colorspace=bt2020nc:range=tv")

POV_LABEL_SIZE = 42
DRONE_LABEL_SIZE = 34
POV_LABEL_Y = 0.62                      # on the feed at 0:03
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
    """Beat one, native HLG: the controller span, graded, labelled."""
    k = hlg_signal_of_white(DRONE_WHITE)
    vf = (f"[0:v]scale={OUT_W}:{OUT_H}:flags=lanczos,{POV_GRADE},"
          f"setpts=PTS-STARTPTS,fps={FPS},format=yuv420p10le,setsar=1[v];"
          f"[1:v]format=rgba,colorchannelmixer=rr={k}:gg={k}:bb={k}[l];"
          f"[v][l]overlay=0:0:format=yuv420p10,format=yuv420p10le,"
          f"{HLG_PARAMS}[o]")
    return _encode(dst, ["-ss", f"{POV_IN}", "-t", f"{POV_SPAN + 0.5}",
                         "-i", str(POV), "-i", str(label)], vf, frames)


def _segment_drone(dst: Path, label: Path, frames: int, cube: Path) -> Path:
    """The air half: fixed crop, sped up, labelled, exact SDR to HLG."""
    vf = (f"[0:v]crop={CROP_W}:2160:{DRONE_X}:0,"
          f"scale={OUT_W}:{OUT_H}:flags=lanczos,"
          f"setpts=(PTS-STARTPTS)/{DRONE_SPEED},fps={FPS},setsar=1[v];"
          f"[v][1:v]overlay=0:0:enable='lt(t,{DRONE_LABEL_OUT})',"
          f"format=rgb48le,lut3d=file='{cube}':interp=tetrahedral,"
          f"scale=out_color_matrix=bt2020:out_range=tv,format=yuv420p10le,"
          f"{HLG_PARAMS}[o]")
    src = DRONE_SPAN * DRONE_SPEED + 1.0
    return _encode(dst, ["-ss", f"{DRONE_IN}", "-t", f"{src}",
                         "-i", str(DRONE), "-i", str(label)], vf, frames)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)

    pov_png = render_text_png(LABEL_POV, WORK / f"label-pov{_SUFFIX}.png",
                              size=POV_LABEL_SIZE, y_frac=POV_LABEL_Y,
                              bg_luma=LABEL_LUMA)
    drone_png = render_text_png(LABEL_DRONE, WORK / f"label-drone{_SUFFIX}.png",
                                size=DRONE_LABEL_SIZE, y_frac=DRONE_LABEL_Y,
                                bg_luma=LABEL_LUMA)

    cube = write_sdr_to_hlg_cube(WORK / f"sdr-to-hlg-{DRONE_WHITE}.cube",
                                 DRONE_WHITE)

    pov_frames = round(POV_SPAN * FPS)
    drone_frames = round(DRONE_SPAN * FPS)
    parts = [_segment_pov(WORK / f"a{_SUFFIX}.mp4", pov_png, pov_frames),
             _segment_drone(WORK / f"b{_SUFFIX}.mp4", drone_png, drone_frames, cube)]

    listing = WORK / f"concat{_SUFFIX}.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    _run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", str(listing), "-c", "copy", "-an", "-movflags", "+faststart",
          str(OUT)])

    print(f"{OUT}  {_probe(OUT):.3f}s  cut at {pov_frames / FPS:.3f}s")


if __name__ == "__main__":
    main()
