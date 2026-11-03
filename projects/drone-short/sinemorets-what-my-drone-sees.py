"""Sinemorets What My Drone Sees - the POV/reveal format on the Sinemorets coast.

Built on `akra-what-my-drone-sees.py`: HLG out, because the controller clip is
an iPhone HLG video, with the drone clip lifted by the exact SDR-to-HLG LUT.
Silent, no audio track - the editor lays the sound on the platform.

1. **what i see** - `IMG_1339.MOV` 6-10s, the controller in the car with the
   coastline on its screen. Real video, so played straight, no boomerang.
2. **what my drone sees** - `Sea Coast 10`, the push along the beach towards
   Sinemorets, at 2x. The clip is 30fps, so 2x at 60fps out keeps every frame.

The editor's brief: controller 0:06-0:10, colours popped and exposure fixed,
then Sea Coast 10 at 2x or 3x, 11-12s overall.

## Grade

Measured at 6, 8 and 9.8s the controller reads YLOW ~360/1023, YAVG ~612 and
SATAVG ~43 (10-bit) - lifted, bright off the car window, and grey. Akra's
approved controller grade fits the same reading, so it starts there.

Sea Coast 10 reads YLOW 71, YAVG 113, SATAVG 64 across the clip: already
saturated, sky near cyan. No grade - any lift goes neon (the Akra lesson).
"""

import subprocess
from pathlib import Path

from video_automation.core.hdr import hlg_signal_of_white, write_sdr_to_hlg_cube
from video_automation.core.vertical import OUT_H, OUT_W, render_text_png

SOURCE_POST = None                      # off-site: a format piece, no article

POV = Path("~/Desktop/Drone Videos/Controller/IMG_1339.MOV").expanduser()
DRONE = Path("~/Desktop/Drone Videos/Footage/Sinemorets/Sea Coast 10.mp4").expanduser()

OUT = Path("~/Desktop/sinemorets-what-my-drone-sees.mp4").expanduser()
WORK = Path("~/Desktop/.work-sinemorets-what-my-drone-sees").expanduser()

FPS = 60
CROP_W = 1215                           # 9:16 out of a 2160-line frame

POV_IN = 6.0
POV_SPAN = 4.0                          # 0:06-0:10, played straight
POV_GRADE = "eq=contrast=1.25:brightness=-0.08:gamma=0.95:saturation=1.5"

DRONE_IN = 5.0
DRONE_SPEED = 2.0
DRONE_SPAN = 7.5                        # seconds on screen
DRONE_X = 1500                          # village and beach centred, both ends

DRONE_WHITE = 400                       # nits SDR white lands at in the HLG file
HLG_PARAMS = ("setparams=color_primaries=bt2020:color_trc=arib-std-b67:"
              "colorspace=bt2020nc:range=tv")

POV_LABEL_SIZE = 42
DRONE_LABEL_SIZE = 34
LABEL_LUMA = 0.0                        # white ink, dark halo
POV_LABEL_Y = 0.62                      # on the feed; 0.38 lands on the sticks
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

    pov_png = render_text_png(LABEL_POV, WORK / "label-pov.png",
                              size=POV_LABEL_SIZE, y_frac=POV_LABEL_Y,
                              bg_luma=LABEL_LUMA)
    drone_png = render_text_png(LABEL_DRONE, WORK / "label-drone.png",
                                size=DRONE_LABEL_SIZE, y_frac=DRONE_LABEL_Y,
                                bg_luma=LABEL_LUMA)

    cube = write_sdr_to_hlg_cube(WORK / f"sdr-to-hlg-{DRONE_WHITE}.cube",
                                 DRONE_WHITE)

    pov_frames = round(POV_SPAN * FPS)
    drone_frames = round(DRONE_SPAN * FPS)
    parts = [_segment_pov(WORK / "a.mp4", pov_png, pov_frames),
             _segment_drone(WORK / "b.mp4", drone_png, drone_frames, cube)]

    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    _run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", str(listing), "-c", "copy", "-an", "-movflags", "+faststart",
          str(OUT)])

    print(f"{OUT}  {_probe(OUT):.3f}s  cut at {pov_frames / FPS:.3f}s")


if __name__ == "__main__":
    main()
