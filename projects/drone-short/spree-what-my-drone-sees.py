"""Spree What My Drone Sees — the fourth in the POV/reveal format, the first
shipped in HDR, and the first with sound and a built loop.

Built on `golden-girl-what-my-drone-sees.py`.

1. **what i see** — a phone clip of the RC controller held over a dry field,
   the sunset over the Spree running on its screen.
2. **what my drone sees** — the locked-off sunset hyperlapse down the river,
   the Fernsehturm behind. It is the frame on the controller's screen, so it
   leads the air half, which is the format's own rule.
3. **then the orbit** — `Spree Buildings 9` at 2x, the drone circling the
   Treptowers as the sun passes behind it, the Molecule Man in the river. It
   holds one silent second after the music before the loop restarts.

## The loop: four phrases of the track, a cut on every phrase

**The user's brief:** a perfect loop to the sound from a TikTok they supplied,
which breaks the format's silent-always rule on their call. It took four
versions: 10s, then cuts on the beat's own repeats with one more phrase and
Buildings 9 filling it (~13.4s), then this order with a silent second on the
end (14.37s).

**The track is one phrase repeated.** Each phrase opens on a hit after a ~70ms
dip to -55 dB. Measured at the sample, the hits rise at 3.3454, 6.6905 and
10.0354s, which is a period of 3.345s to the millisecond. The file only holds
three clean phrases after the first (the fourth ends in an outro crash), so
the bed is phrases two and three, `AUDIO_IN`-`AUDIO_OUT`, played twice.
Every join, including the loop's own wrap, is hit-onset to hit-onset after the
same near-silence the track has between its phrases, so none of them is a seam.

**Every cut is on a phrase hit.** The bed opens on one, so frame one is a hit
too:

| beat | phrases | frames | out | hit at |
|---|---|---|---|---|
| controller | 1 | 100 | 0.00-3.33 | 0.000 |
| hyperlapse | 1 | 101 | 3.33-6.70 | 3.345 |
| Buildings 9 | 2 + 1s | 230 | 6.70-14.37 | 6.690 (10.035 mid-shot) |

Whole-frame cuts sit within 12ms of the hits, under half a frame.

**The last second is silent, on the user's call, and it is what makes the
loop.** The music ends at 13.38s on the near-silence before the next phrase's
hit, and the orbit runs one more second with no sound. The wrap then lands on
frame one and the phrase hit together: the restart reads as the beat coming
back in, not as a track looping under the picture. `TAIL` is that second;
`apad` fills it with true silence rather than more of the track.

**The controller clip is still used whole**, at 1.2x to fill its phrase. The
hyperlapse gives one phrase from 8.0s in, the sun at its lowest. Buildings 9
gives 15.4s of source from the top at 2x. A fixed box loses the tower over that
span as the orbit carries it ~890px left, so the crop tracks it at
`BUILDINGS_DRIFT` px per source second, which holds it centred to within 20px,
measured at four points. The sun goes behind it early in the shot.

## Colour

**The controller is lifted to sit with the drone shots, on the user's call:
"pop colors a bit more like the second video".** In the tone-mapped check its
SATAVG was 15 against the hyperlapse's 28. `eq` saturation 1.55 and contrast
1.06 take it to ~24. At 1.70 (SATAVG 27) the grey controller body starts to
pick up a cast off the grass, which is the stop sign from the Vienna cut. `eq`
works in YUV, so it is safe on HLG where `colorlevels` is not.

**The two drone clips get the same SDR-to-HLG conversion and no grade.**

**Denoise.** The hyperlapse shows no flicker (frame-to-frame YAVG change mean
0.04, worst 0.21). It does show temporal shimmer in the shadows, mean
frame-difference 1.88 in a dark block, and `hqdn3d=2:1.5:6:6` takes that to
1.20 with no visible softening. It is locked-off, so a temporal denoise has no
motion to smear. Buildings 9 is an orbit and gets none.

**Crops are hand-set.** Hyperlapse x=1043 holds the sun, the Fernsehturm and
both towers. Buildings 9 tracks, as above.

## HDR, and the three renders it took

The controller clip is iPhone HLG (BT.2020, `arib-std-b67`, 10-bit). The
hyperlapse is SDR BT.709, 8-bit. One file cannot be both, so one of them has
to be converted, and the direction is what the three renders were about.

1. **SDR file, HLG tags leaking.** Encoded as 8-bit 709, but segment a carried
   its HLG tags through the filter graph despite the `-color_*` output flags,
   and the concat stamped them on the whole file. Players read the untouched
   709 hyperlapse as BT.2020 HLG and the user saw it oversaturated.
2. **SDR file, tagged right.** `setparams` fixed the tags. The hyperlapse
   looked right, and the controller now looked drained: HLG pixels shown as
   709 with no tone map are flat and grey, which is what "the colours were
   removed" was. There is no `zscale` in this ffmpeg to tone-map it down.
3. **HLG file (this one), the user's call: keep the HDR.** The controller
   clip stays native HLG and is not touched beyond the scale. The hyperlapse
   is brought *up* into HLG, and that took two tries of its own.

**SDR into HLG: what did not work, and what did.** The check for each is the
one an iPhone or Mac does on an SDR screen: VideoToolbox's `scale_vt` tone-maps
the HLG output back to 709, and that is compared with the source frame. The
same check on the controller clip gives back its own source within a point
(YAVG 117 / 117, SATAVG 15 / 14), so it is a fair judge.

| SDR to HLG | tone-mapped back, YAVG / SATAVG | source 137 / 27 |
|---|---|---|
| BT.2408 3D LUT (white at HLG 75%) | 89 / 20, grey sun | dull and dark |
| primaries only, 709 to 2020 | 120 / 37 | render 1's oversaturation again |
| primaries, `eq` saturation 0.66, gamma 1.20 | **132 / 28** | the source |

The textbook mapping parks SDR white at reference white, which is right on an
HDR screen next to other reference-graded HDR material, but iPhone HLG sits
well above that, and next to it the drone half went dim. Placing the SDR
signal straight into BT.2020 primaries, the BBC's "SDR is near-compatible"
route, holds the brightness. HLG's system gamma then adds saturation on the
way back, and the `eq` pre-trim takes it out again. The trim is a match, not a
grade. Its only job is to make the converted file look like the source.

**The labels are dimmed to 85%.** At 100% a white PNG lands at HLG peak and
reads as a glare on an HDR screen. BT.2408's 75% looked grey after tone
mapping, so they go in at 85%.

**Labels sit dead centre, on the user's call**, and are only on the first
two beats. The orbit runs unlabelled.
"""

import subprocess
from pathlib import Path

from video_automation.core.vertical import OUT_H, OUT_W, render_text_png

SOURCE_POST = None                      # off-site: a format piece, no article

CONTROLLER = Path("~/Desktop/Drone Videos/Controller").expanduser()
POV = CONTROLLER / "IMG_1979.MOV"
SPREE = CONTROLLER / "Spree Hyperlapse 3.mp4"
BUILDINGS = CONTROLLER / "Spree Buildings 9.mp4"
SOUND = Path("~/Desktop/v12044gd0000d8o26uvog65tm0poamcg.MP4").expanduser()

OUT = Path("~/Desktop/spree-what-my-drone-sees.mp4").expanduser()
WORK = Path("~/Desktop/.work-spree-what-my-drone-sees").expanduser()

FPS = 30

# The bed: phrases two and three of the track, hit to hit, played twice.
AUDIO_IN, AUDIO_OUT = 3.3454, 10.0354
PHRASE = (AUDIO_OUT - AUDIO_IN) / 2

# Beat lengths in whole phrases. Frames are rounded from the hit times.
POV_PHRASES, SPREE_PHRASES, BUILDINGS_PHRASES = 1, 1, 2
TAIL = 1.0                              # silent hold on the last shot

# Whole controller clip, sped to fit its phrase. Real video: no boomerang.
POV_SPAN = 4.0
POV_GRADE = "eq=saturation=1.55:contrast=1.06"

BUILDINGS_START = 0.0
BUILDINGS_SPEED = 2.0
BUILDINGS_X0 = 1608                     # tracking crop: x at the in-point
BUILDINGS_DRIFT = 57.9                  # and px per source second, leftward
BUILDINGS_W = 1215

SPREE_START = 8.0
SPREE_CROP = (1215, 2160, 1043, 0)      # w, h, x, y
SPREE_DENOISE = "hqdn3d=2:1.5:6:6"      # temporal shimmer in the shadows

# SDR to HLG: pre-trim, then BT.709 to BT.2020 primaries, tagged HLG. Matched
# by tone-mapping back; see the docstring.
SDR_TO_HLG = ("eq=saturation=0.66:gamma=1.20,"
              "colorspace=all=bt2020:trc=bt2020-10:iall=bt709:itrc=bt709:"
              "format=yuv420p10:fast=0")
HLG_PARAMS = ("setparams=color_primaries=bt2020:color_trc=arib-std-b67:"
              "colorspace=bt2020nc:range=tv")

POV_LABEL_SIZE = 42
DRONE_LABEL_SIZE = 34
LABEL_LUMA = 0.0                        # white ink, dark halo
LABEL_Y = 0.50                          # the user's call: centred
HLG_WHITE = 0.85                        # labels: below HLG peak, see above
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


def _dim(label: str) -> str:
    """A label stream scaled below HLG peak, alpha untouched."""
    k = HLG_WHITE
    return f"{label}format=rgba,colorchannelmixer=rr={k}:gg={k}:bb={k}"


def _encode(dst: Path, inputs: list[str], vf: str, frames: int) -> Path:
    _run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", vf,
          "-map", "[o]", "-frames:v", str(frames), "-an", *X265, *HLG_TAGS,
          str(dst)])
    return dst


def _cuts() -> list[int]:
    """Frame of each phrase boundary, from the first cut to the music's end."""
    marks, n = [], 0
    for phrases in (POV_PHRASES, SPREE_PHRASES, BUILDINGS_PHRASES):
        n += phrases
        marks.append(round(n * PHRASE * FPS))
    return marks


def _segment_pov(dst: Path, label: Path, frames: int) -> Path:
    """Beat one, native HLG: the whole clip sped to fit, lifted, labelled."""
    speed = POV_SPAN / (frames / FPS)
    vf = (f"[0:v]scale={OUT_W}:{OUT_H}:flags=lanczos,{POV_GRADE},"
          f"setpts=(PTS-STARTPTS)/{speed},fps={FPS},format=yuv420p10le,"
          f"setsar=1[v];{_dim('[1:v]')}[l];"
          f"[v][l]overlay=0:0:format=yuv420p10,format=yuv420p10le,"
          f"{HLG_PARAMS}[o]")
    return _encode(dst, ["-t", f"{POV_SPAN}", "-i", str(POV), "-i", str(label)],
                   vf, frames)


def _segment_sdr(dst: Path, src: Path, start: float, frames: int,
                 crop: str, speed: float, pre: str,
                 label: Path | None) -> Path:
    """An SDR drone shot: crop, optional denoise and label, lifted into HLG.

    `crop` is a whole `crop=` filter, so a tracking box can pass an expression.
    """
    chain = (f"[0:v]{crop},scale={OUT_W}:{OUT_H}:flags=lanczos,"
             f"{pre}setpts=(PTS-STARTPTS)/{speed},fps={FPS},setsar=1")
    if label:
        vf = (f"{chain}[v];{_dim('[1:v]')}[l];"
              f"[v][l]overlay=0:0:enable='lt(t,{DRONE_LABEL_OUT})'")
        extra = ["-i", str(label)]
    else:
        vf, extra = chain, []
    vf += f",format=yuv420p,{SDR_TO_HLG},{HLG_PARAMS}[o]"
    span = frames / FPS * speed + 0.5
    return _encode(dst, ["-ss", f"{start}", "-t", f"{span}", "-i", str(src),
                         *extra], vf, frames)


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)

    pov_png = render_text_png(LABEL_POV, WORK / "label-pov.png",
                              size=POV_LABEL_SIZE, y_frac=LABEL_Y,
                              bg_luma=LABEL_LUMA)
    drone_png = render_text_png(LABEL_DRONE, WORK / "label-drone.png",
                                size=DRONE_LABEL_SIZE, y_frac=LABEL_Y,
                                bg_luma=LABEL_LUMA)

    c1, c2, music_end = _cuts()
    end = music_end + round(TAIL * FPS)
    w, h, x, y = SPREE_CROP
    x0, drift = BUILDINGS_X0, BUILDINGS_DRIFT
    parts = [
        _segment_pov(WORK / "a.mp4", pov_png, c1),
        _segment_sdr(WORK / "b.mp4", SPREE, SPREE_START, c2 - c1,
                     f"crop={w}:{h}:{x}:{y}", 1.0, f"{SPREE_DENOISE},",
                     drone_png),
        _segment_sdr(WORK / "c.mp4", BUILDINGS, BUILDINGS_START, end - c2,
                     f"crop={BUILDINGS_W}:2160:'{x0}-{drift}*t':0",
                     BUILDINGS_SPEED, "", None),
    ]

    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    silent = WORK / "video.mp4"
    _run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", str(listing), "-c", "copy", str(silent)])

    # The bed, twice, joined sample-exact on a hit onset.
    total = end / FPS
    bed = AUDIO_OUT - AUDIO_IN
    _run(["ffmpeg", "-v", "error", "-y", "-i", str(silent),
          "-ss", f"{AUDIO_IN}", "-t", f"{bed}", "-i", str(SOUND),
          "-filter_complex",
          "[1:a]asplit=2[x][y];[x][y]concat=n=2:v=0:a=1,apad[a]",
          "-map", "0:v", "-map", "[a]", "-c:v", "copy",
          "-c:a", "aac", "-b:a", "192k", "-t", f"{total}",
          "-movflags", "+faststart", str(OUT)])

    print(f"{OUT}  {_probe(OUT):.3f}s  cuts at {c1 / FPS:.3f}s and "
          f"{c2 / FPS:.3f}s, music ends {music_end / FPS:.3f}s, phrase hits at "
          + ", ".join(f"{k * PHRASE:.3f}" for k in range(4)))


if __name__ == "__main__":
    main()
