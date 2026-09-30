"""Vienna What My Drone Sees — the second in the POV/reveal format.

Built on `burgas-what-my-drone-sees.py`, which the channel's numbers liked.

1. **what i see** — a tight phone shot of the RC controller in hand, the live
   Donauinsel feed running on its screen. 2.07s of source, far too short to be
   a beat on its own.
2. **what my drone sees** — the Donauinsel from above, then the DC Towers.
   One shot at a time, full bleed, both at 2x.

**Donauinsel leads because it is the shot on the controller's screen.** That is
what makes the cut land: the viewer has already seen this exact view as a
postage stamp in beat one, and beat two hands it to them full frame. The
skyscrapers follow as the shot they have *not* been shown.

**The short source is boomeranged, not looped.** Two hard loops of a 1.15s clip
put a visible jump cut in the opening beat, which is the one place this format
cannot afford one — the whole bet is that frame one reads as an ordinary person
holding a controller. Forward then reversed instead: same length, and the join
is continuous because the reverse starts on the frame the forward pass ended on.
Same reasoning as the boomerang note in `drone-short.md`, reached from the
opposite direction — there a clip was too short for the narration, here too
short for the beat.

**Both crops are hand-set, and `pick_crop` was overruled on both.** It is
scoring an interest map, and on these two frames the densest texture is not the
subject:

* *Donauinsel* — it chose x=1632, which puts the island down the left edge and
  fills the right of the frame with the far skyline. The user asked for the
  island centred, and its axis actually sits at about x 0.47 of the sensor, so
  x=1198 runs it down the middle of the vertical frame with water either side.
  That symmetry is the whole reason the shot works in 9:16.
* *Skyscrapers* — it chose x=2616, dense residential blocks on the right, and
  lost the DC Towers out of frame completely. This is the `Hills Monument`
  failure in `drone-short.md` exactly: a lone subject against busy ground. The
  towers sit at about x 0.37, so x=950.

Both were checked at the *end* of their spans as well as the start, because
both moves are push-ins and a box that frames a subject at the in-point can
have walked off it eleven seconds of source later.

Full sensor height on both (no `zoom`): these are vistas, and the sky and the
receding horizon are the subject rather than dead air.

**Both drone clips are graded, and the numbers say why.** The user read them as
"faded, maybe underexposed"; `signalstats` says not underexposed at all — YAVG
145 and 138, if anything slightly bright, with YMAX up at 247 and 237. What is
actually wrong is two things at once:

* **Lifted blacks.** YLOW — the shadow end — sits at 58 and 61 where it should
  be near 16. That is the "missing shadows" half, and it is what makes summer
  haze read as a veil over the whole frame.
* **Low saturation.** SATAVG 15.3 and 21.6, against the 30-60 of footage that
  reads as punchy.

So the fix is a black-point pull plus saturation, not exposure — raising
brightness would have made it worse. The two clips get **different numbers**
because they start in different places: the island is the flatter of the two and
takes 0.12/1.32, the towers 0.10/1.22. One look applied to both would have
over-cooked the towers, whose orange riverbank goes lurid a step earlier than
anything in the island shot. `unsharp` is mild and is there for the haze, not
for resolution — neither clip is soft, and pushing it further only finds
artifacts along the tower edges.

**The controller clip is graded too, and it needed the opposite of a black
pull.** It is a full-range (`pc`/`yuvj420p`) phone file, not a `tv`-range drone
one, and it measures YLOW 31 against the drone clips' 58-61 — its shadows were
never lifted, so the 0.10-0.12 that rescued them would have crushed the grass
and the controller body flat. What it shares is the saturation problem, and
worse: SATAVG 10.1, the lowest of the three. Hence 0.03/1.45 — barely any black
move, the biggest saturation lift in the cut. Past about 1.5 the grey controller
body starts taking a warm cast from the grass around it, which is the tell that
the grade has stopped correcting and started tinting.

**Silent, and deliberately** — no audio track at all, so the TikTok trending
sound stays available and the user can lay their own track under it.
"""

import subprocess
from pathlib import Path

from video_automation.core.vertical import (OUT_H, OUT_W, render_text_png)

SOURCE_POST = None                      # off-site: a format piece, no article

POV = Path("~/Desktop/Drone Videos/Controller/"
           "3727005D-B301-4E52-9538-CDCD95F5A604.MOV").expanduser()
ISLAND = Path("~/Desktop/Drone Videos/Footage/Vienna/Donauinsel 2.mp4").expanduser()
TOWERS = Path("~/Desktop/Drone Videos/Footage/Vienna/"
              "Donauinsel Skyscrapers 1.mp4").expanduser()

OUT = Path("~/Desktop/vienna-what-my-drone-sees.mp4").expanduser()
WORK = Path("~/Desktop/.work-vienna-what-my-drone-sees").expanduser()

FPS = 30
TARGET_TOTAL = 14.0

# 2.07s of source at 1.8x is 1.153s a pass; two passes is forward-and-back.
POV_SPEED = 1.8
POV_PASSES = 2

# The controller is 1436x1916 (3:4-ish), not 9:16, so it is cropped rather than
# fitted: 1916 * 1080/1920 = 1078 wide, centred. That shaves the outer edge of
# both sticks and keeps the screen whole, which is the half that carries the
# joke. A blurred fill would have kept the sticks and cost the full bleed.
POV_CROP_W = 1078

# Both Vienna clips are slow push-ins over open landscape. 2x is what makes the
# back half feel like a reveal rather than a postcard.
DRONE_SPEED = 2.0

# (source, in-point, crop box) — see the module docstring on the boxes.
ISLAND_START, ISLAND_BOX = 30.0, (1198, 0, 1215, 2160)
TOWERS_START, TOWERS_BOX = 4.0, (950, 0, 1215, 2160)

# Grade: (black point, saturation, contrast). See the docstring section on why
# these are per-clip rather than one look applied to both.
ISLAND_GRADE = (0.12, 1.32, 1.08)
TOWERS_GRADE = (0.10, 1.22, 1.06)
POV_GRADE = (0.03, 1.45, 1.08)
SHARPEN = "unsharp=5:5:0.9:5:5:0"

# The island gets the longer half: it is the shot beat one has already promised.
ISLAND_DUR = 6.20

# "Very small text in the middle", carried over from the Burgas cut — but the
# POV label is a size up on the user's call, since a controller filling the
# frame gives the type more to fight than open water did.
POV_LABEL_SIZE = 42
DRONE_LABEL_SIZE = 34
LABEL_LUMA = 0.0                        # white ink, dark halo

# Beat one does not get 0.50. This controller fills the frame, and dead centre
# is the C/N/S switch and the screen bezel — the label landed on both and read
# as clutter. 0.62 is the one clean band in the shot, the open sky of the feed
# on the controller's own screen. `y_frac` follows the frame, not a number.
POV_LABEL_Y = 0.62
DRONE_LABEL_Y = 0.50

LABEL_POV = "what i see"
LABEL_DRONE = "what my drone sees"

# Clears inside the island shot, so the cut to the towers lands on clean
# picture rather than pulling the type off mid-thought. Pulled in a second on
# the user's call — three seconds is long enough to read four small words.
LABEL_OUT = 3.20


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def _probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def _segment_pov(dst: Path, label: Path) -> Path:
    """Beat one: crop to 9:16, speed up, boomerang to length, burn the label.

    `split` then `reverse` off the same sped-up stream, so the two directions
    are guaranteed to be the same frames and the join cannot drift.
    """
    x = (1436 - POV_CROP_W) // 2
    black, sat, contrast = POV_GRADE
    chain = (f"crop={POV_CROP_W}:1916:{x}:0,"
             f"scale={OUT_W}:{OUT_H}:flags=lanczos,"
             f"colorlevels=rimin={black}:gimin={black}:bimin={black},"
             f"eq=saturation={sat}:contrast={contrast},{SHARPEN},"
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
    parts.append("[loop][1:v]overlay=0:0[o]")

    _run(["ffmpeg", "-v", "error", "-y", "-i", str(POV), "-i", str(label),
          "-filter_complex", ";".join(parts), "-map", "[o]", "-an",
          "-c:v", "libx264", "-crf", "18", "-preset", "slow",
          "-pix_fmt", "yuv420p", str(dst)])
    return dst


def _segment_drone(dst: Path, src: Path, start: float, dur: float,
                   box: tuple[int, int, int, int],
                   grade: tuple[float, float, float],
                   label: Path | None = None) -> Path:
    """One full-bleed 9:16 shot, graded, sharpened, sped up, optional label.

    The grade goes *after* the downscale so `unsharp` is working on the pixels
    that ship, not on 4K detail that the scale is about to throw away.
    """
    x, y, w, h = box
    black, sat, contrast = grade
    chain = (f"[0:v]crop={w}:{h}:{x}:{y},"
             f"scale={OUT_W}:{OUT_H}:flags=lanczos,"
             f"colorlevels=rimin={black}:gimin={black}:bimin={black},"
             f"eq=saturation={sat}:contrast={contrast},{SHARPEN},"
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
          "-pix_fmt", "yuv420p", str(dst)])
    return dst


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)

    pov_png = render_text_png(LABEL_POV, WORK / "label-pov.png",
                              size=POV_LABEL_SIZE, y_frac=POV_LABEL_Y,
                              bg_luma=LABEL_LUMA)
    drone_png = render_text_png(LABEL_DRONE, WORK / "label-drone.png",
                                size=DRONE_LABEL_SIZE, y_frac=DRONE_LABEL_Y,
                                bg_luma=LABEL_LUMA)

    pov_dur = _probe(POV) / POV_SPEED * POV_PASSES
    towers_dur = round(TARGET_TOTAL - pov_dur - ISLAND_DUR, 3)

    parts = [
        _segment_pov(WORK / "a.mp4", pov_png),
        _segment_drone(WORK / "b.mp4", ISLAND, ISLAND_START, ISLAND_DUR,
                       ISLAND_BOX, ISLAND_GRADE, drone_png),
        _segment_drone(WORK / "c.mp4", TOWERS, TOWERS_START, towers_dur,
                       TOWERS_BOX, TOWERS_GRADE),
    ]

    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    _run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(OUT)])

    print(f"{OUT}  {_probe(OUT):.2f}s  "
          f"pov={pov_dur:.2f}s island={ISLAND_DUR:.2f}s towers={towers_dur:.2f}s")


if __name__ == "__main__":
    main()
