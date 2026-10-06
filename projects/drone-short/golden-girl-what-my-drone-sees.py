"""Golden Girl What My Drone Sees — the third in the POV/reveal format.

Built on `vienna-what-my-drone-sees.py`, which is the fuller reference.

1. **what i see** — a night phone clip of the RC controller in one hand and
   the weather app in the other, the Siegessäule feed running on the
   controller's screen.
2. **what my drone sees** — the same column from the air, a night hyperlapse
   with the traffic drawing light trails around the roundabout.

**The air shot is the one already on the controller's screen**, which is the
format's own rule and is as literal here as it gets: the postage stamp in beat
one and the full-frame reveal in beat two are the same monument from nearly the
same angle.

**Two things this cut does not do that the earlier two did.**

* **No crop decision on the air half.** `Golden Girl Night Hyperlapse 2.mp4` was
  shot vertical — 2160x3840 — so it scales straight to 1080x1920 with nothing
  thrown away. There is no `pick_crop` to overrule and no subject to re-centre;
  the column is already down the middle. The controller clip is an iPhone
  portrait file at the same aspect, so it needs no crop either. Both of the
  previous cuts spent most of their build on boxes, and this one spends none.
* **No speed on the air half.** `DRONE_SPEED` is 1.0 because the source is
  already a hyperlapse. The 2x that made Vienna's slow push-ins read as a
  reveal would take this to 3.5 seconds and strobe the light trails.

**No boomerang, because this one is real video.** Burgas and Vienna both
boomeranged their controller beats, and the reason was the source: a Live
Photo, a second or two of frames with nowhere else to go. This is a 17.7s
handheld clip, played straight at 1x. A boomerang on footage that has a real
forward direction reads as a stutter, not as a held moment.

**The beat is 5.0-9.0, the user's pick, and it took three tries to find.**
0.2-2.6 is the span where the controller sits whole in frame before the camera
drifts onto the phone, but at 2.4s it was too short. 11.0 to the end is a
6.7s push-in back onto the controller, which was long enough but opened on the
phone with the feed a sliver at the left edge. 5.0-9.0 is the middle: the
camera is coming back off the phone and settling onto the controller, both
screens in frame throughout, and four seconds of it.

**Grades are small here, and the measurements say to leave the exposure
alone.** Both clips are night, so the low YAVG that would be a fault in daylight
is the subject:

| clip | YLOW | YAVG | SATAVG | read as |
|---|---|---|---|---|
| controller, iPhone, 10-bit | 67 (≈17 of 255) | 135 (≈34) | 7.9 | shadows already where they belong; only the saturation is off |
| hyperlapse, 8-bit | 21 | 54 | 21.6 | blacks near clean, blue hour slightly flat |

**The hyperlapse ships ungraded, on the user's call, and the measurement did
not see it coming.** SATAVG 21.6 is inside the band that says "lift this", and
a 1.30 lift is what the Vienna cut would have done. On a night frame it is
wrong: the colour that is there is already concentrated in the few lit things —
the gold statue, the sodium street lights, the red tail-light trails — against
a sky that is most of the frame. Lifting saturation does not spread across the
picture the way it does in daylight, it loads the handful of saturated pixels
and the statue goes orange. The reading is an average over a frame that is
mostly dark sky, so it understates what the lit parts already have. **Treat a
night shot's SATAVG as unreliable and look at the lit areas instead.** Sharpen
comes off with it — there is nothing haze-bound to rescue and it would only
find the noise in the sky.

The controller file is 10-bit, so its numbers run on a 0-1023 scale — YMAX came
back at 950, which is the tell. Divided down, its blacks sit at about 17 of 255,
*not* the 58-61 that needed rescuing on the Vienna drone clips. A black pull of
the size that cut used would have swallowed the pavement and the controller
body whole. Both clips therefore get a token black move and a saturation lift,
and the hyperlapse gets slightly more of both because blue hour is the flatter
of the two. Nothing raises brightness: these are night shots and darkness is
what they are of.

**The controller clip is HLG, and that broke the first render.** It is tagged
`bt2020nc` / `arib-std-b67`, which no earlier source in this project was.
`colorlevels` is the only filter in the grade chain that leaves YUV for RGB,
and ffmpeg does that conversion on an HLG source without tone mapping — the
frame came back all but black, the controller a smear and the feed on its
screen the only thing still visible. `eq` works in YUV and was untouched by it,
which is what the bisect showed. So beat one grades with `eq` alone and its
black point is `None`; the pull it wanted was 0.01. The segments are then
tagged bt709 on the way out, because an 8-bit SDR encode still carrying its
source's HDR tags gets a display curve applied to a picture that no longer
needs one. There is no `zscale` in this ffmpeg build and `colorspace` does not
accept `arib-std-b67` as an input transfer, so a real tone map was not on the
table — and at a 0.01 black pull it was not worth one.

`unsharp` is mild on the hyperlapse and absent on the controller — a dark phone
file has visible noise, and sharpening a night frame finds the grain before it
finds the detail.

**Labels sit high, over the dark.** 0.50 is wrong on both frames in this cut:
on the air shot it lands on the golden statue, which is the one thing the
reveal is for, and on the controller it lands on the phone screen's text. The
open band on both is the top fifth — empty sky above the column, empty night
above the hands — so both labels go to 0.18. Same lesson as Vienna's 0.62,
reached on a different pair of frames: `y_frac` follows the picture.

**Silent, and deliberately** — no audio track at all, so the TikTok trending
sound stays available and the user can lay their own track under it.
"""

import subprocess
from pathlib import Path

from video_automation.core.vertical import OUT_H, OUT_W, render_text_png

SOURCE_POST = None                      # off-site: a format piece, no article

POV = Path("~/Desktop/Drone Videos/Controller/IMG_3413.MOV").expanduser()
COLUMN = Path("~/Desktop/Drone Videos/Footage/Berlin 26 1:4/"
              "Golden Girl Night Hyperlapse 2.mp4").expanduser()

OUT = Path("~/Desktop/golden-girl-what-my-drone-sees.mp4").expanduser()
WORK = Path("~/Desktop/.work-golden-girl-what-my-drone-sees").expanduser()

FPS = 30

# The user's span. Played straight: real video, no boomerang.
POV_START, POV_SPAN = 5.0, 4.0
POV_SPEED = 1.0
POV_PASSES = 1

# Already a hyperlapse. See the docstring — speeding it again strobes the
# traffic trails and costs nine seconds of the only air shot in the cut.
DRONE_SPEED = 1.0
COLUMN_START, COLUMN_DUR = 0.0, 7.0

# Grade: (black point, saturation, contrast). Small on purpose; see above.
# The controller clip's black point is `None` and that is not a rounding of
# "small" — see the HLG section in the docstring. `colorlevels` is the one
# filter in this chain that leaves YUV for RGB, and on an HLG source ffmpeg
# does that conversion without tone mapping, so the frame comes back all but
# black. `eq` stays in YUV and is unaffected. The pull was 0.01 anyway.
POV_GRADE = (None, 1.25, 1.04)
COLUMN_GRADE = None                     # night: see the docstring
POV_SHARPEN = ""                        # dark phone file: sharpening finds grain
COLUMN_SHARPEN = ""

POV_LABEL_SIZE = 42
DRONE_LABEL_SIZE = 34
LABEL_LUMA = 0.0                        # white ink, dark halo
LABEL_Y = 0.18                          # the clean band on both frames

LABEL_POV = "what i see"
LABEL_DRONE = "what my drone sees"

# Both labels clear and let the picture run on unlabelled — that silence is
# the shot doing the talking. Beat one needs the out as much as beat two: four
# small words held for a whole four-second beat read as a watermark.
LABEL_OUT = 3.20


# The controller source is tagged bt2020 / HLG. The segment is encoded as 8-bit
# SDR, so it has to be tagged as such or a player applies an HDR display curve
# to a picture that has already been flattened into 709 and shows it washed out.
# Carried on both segments: a concat takes the first stream's tags.
SDR_TAGS = ["-color_primaries", "bt709", "-color_trc", "bt709",
            "-colorspace", "bt709"]


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def _probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def _grade(grade: tuple[float | None, float, float] | None,
           sharpen: str) -> str:
    """Black pull plus saturation, as a filter fragment.

    A `None` grade is ungraded and a `None` black point skips `colorlevels`.
    Returns "" when there is nothing to do, and the callers drop the comma.
    """
    chain = ""
    if grade is not None:
        black, sat, contrast = grade
        if black is not None:
            chain = f"colorlevels=rimin={black}:gimin={black}:bimin={black},"
        chain += f"eq=saturation={sat}:contrast={contrast}"
    return ",".join(part for part in (chain, sharpen) if part)


def _prefix(fragment: str) -> str:
    """A filter fragment ready to splice mid-chain, or nothing at all."""
    return f"{fragment}," if fragment else ""


def _segment_pov(dst: Path, label: Path) -> Path:
    """Beat one: fit to 9:16, grade, burn the label.

    `POV_PASSES` is 1 here and the beat plays straight through — this source is
    real video, not a Live Photo. The boomerang machinery is kept because the
    format needs it whenever the controller clip is a Live Photo again: at
    `POV_PASSES` 2 it splits the stream and reverses the second pass, so the
    two directions are the same frames and the join cannot drift.
    """
    chain = (f"scale={OUT_W}:{OUT_H}:flags=lanczos,"
             f"{_prefix(_grade(POV_GRADE, POV_SHARPEN))}"
             f"setpts=PTS/{POV_SPEED},fps={FPS},format=yuv420p,setsar=1")

    splits = "".join(f"[s{i}]" for i in range(POV_PASSES))
    parts = [f"[0:v]{chain},split={POV_PASSES}{splits}"]
    order = ""
    for i in range(POV_PASSES):
        # even passes forward, odd reversed — so the beat ends where it began
        # when POV_PASSES is even, and on the far frame when it is odd.
        parts.append(f"[s{i}]{'null' if i % 2 == 0 else 'reverse'}[p{i}]")
        order += f"[p{i}]"
    parts.append(f"{order}concat=n={POV_PASSES}:v=1:a=0[loop]")
    parts.append(f"[loop][1:v]overlay=0:0:enable='lt(t,{LABEL_OUT})'[o]")

    _run(["ffmpeg", "-v", "error", "-y",
          "-ss", f"{POV_START}", "-t", f"{POV_SPAN}", "-i", str(POV),
          "-i", str(label),
          "-filter_complex", ";".join(parts), "-map", "[o]", "-an",
          "-c:v", "libx264", "-crf", "18", "-preset", "slow",
          "-pix_fmt", "yuv420p", *SDR_TAGS, str(dst)])
    return dst


def _segment_drone(dst: Path, src: Path, start: float, dur: float,
                   grade: tuple[float | None, float, float] | None,
                   label: Path | None = None) -> Path:
    """One full-bleed 9:16 shot, graded, sharpened, optional label.

    The grade goes *after* the downscale so `unsharp` is working on the pixels
    that ship, not on 4K detail that the scale is about to throw away.
    """
    chain = (f"[0:v]scale={OUT_W}:{OUT_H}:flags=lanczos,"
             f"{_prefix(_grade(grade, COLUMN_SHARPEN))}"
             f"setpts=PTS/{DRONE_SPEED},fps={FPS},format=yuv420p,setsar=1")

    if label:
        vf = f"{chain}[v];[v][1:v]overlay=0:0:enable='lt(t,{LABEL_OUT})'[o]"
        extra = ["-i", str(label)]
    else:
        vf = f"{chain}[o]"
        extra = []

    _run(["ffmpeg", "-v", "error", "-y",
          "-ss", f"{start}", "-t", f"{dur * DRONE_SPEED}", "-i", str(src),
          *extra, "-filter_complex", vf, "-map", "[o]", "-t", f"{dur}", "-an",
          "-c:v", "libx264", "-crf", "18", "-preset", "slow",
          "-pix_fmt", "yuv420p", *SDR_TAGS, str(dst)])
    return dst


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)

    pov_png = render_text_png(LABEL_POV, WORK / "label-pov.png",
                              size=POV_LABEL_SIZE, y_frac=LABEL_Y,
                              bg_luma=LABEL_LUMA)
    drone_png = render_text_png(LABEL_DRONE, WORK / "label-drone.png",
                                size=DRONE_LABEL_SIZE, y_frac=LABEL_Y,
                                bg_luma=LABEL_LUMA)

    pov_dur = POV_SPAN / POV_SPEED * POV_PASSES

    parts = [
        _segment_pov(WORK / "a.mp4", pov_png),
        _segment_drone(WORK / "b.mp4", COLUMN, COLUMN_START, COLUMN_DUR,
                       COLUMN_GRADE, drone_png),
    ]

    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    _run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(OUT)])

    print(f"{OUT}  {_probe(OUT):.2f}s  "
          f"pov={pov_dur:.2f}s column={COLUMN_DUR:.2f}s  "
          f"cut at {pov_dur:.2f}s")


if __name__ == "__main__":
    main()
