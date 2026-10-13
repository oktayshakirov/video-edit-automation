"""Spree What My Drone Sees, datamosh test. Test only, silent, two variants:

    cut1  controller -> hyperlapse, the controller bent by the orbit's motion
    cut2  hyperlapse -> orbit, the textbook mosh on the orbit's own motion

The approved cut, `spree-what-my-drone-sees.py`, is locked and untouched. This
imports its segments, cuts and colour and replaces one segment. The technique
is `core/datamosh.py`.

**Why the orbit's motion.** The effect is A's pixels pushed into B's shapes,
and the shapes come from the edges in B's motion field: parallax, near towers
moving against the sky. The hyperlapse is locked-off and has none. The
push-in tried before it had motion but no edges, so the controller only
zoomed, which the user called "unrelated". `Spree Buildings 9` orbits the
Treptowers, so its field is shaped like them.

**Out:** the last `HEAL_FRAMES` heal block by block, B's dark structure first,
so the towers resolve out of the mosh before the sky. A 4-frame snap read as
the controller "just disappears".

**HDR.** All segments are HLG 10-bit; the mosh window keeps the HLG code values
at 8 bits and is tagged HLG again. Labels go on after the mosh.
"""

import importlib.util
import sys
from pathlib import Path

from video_automation.core import datamosh

_spec = importlib.util.spec_from_file_location(
    "spree", Path(__file__).with_name("spree-what-my-drone-sees.py"))
S = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(S)

SOURCE_POST = None

WORK = Path("~/Desktop/.work-spree-what-my-drone-sees-mosh").expanduser()

MOSH_FRAMES = 54                        # incoming frames the transition takes
HEAL_FRAMES = 24                        # of which the last ones heal to clean
BLOOM_AT, BLOOM_N = 6, 10               # repeat this P-frame to grow the smear


def _moshed(a: Path, motion: Path, clean: Path, frames: int,
            label: Path | None, name: str) -> Path:
    """`clean`, its opening turned into a mosh out of `a` and healed back."""
    size = (S.OUT_W, S.OUT_H)
    m = datamosh.mosh(a, motion, WORK / f"{name}-mosh.mkv",
                      frames=MOSH_FRAMES, fps=S.FPS, size=size,
                      bloom_at=BLOOM_AT, bloom_n=BLOOM_N)
    healed = datamosh.heal(m, MOSH_FRAMES, clean, WORK / f"{name}-healed.mkv",
                           frames=frames, heal_frames=HEAL_FRAMES, size=size,
                           fps=S.FPS, out_args=["-c:v", "ffv1"])
    if label:
        vf = (f"[0:v]setsar=1[v];{S._dim('[1:v]')}[l];"
              f"[v][l]overlay=0:0:format=yuv420p10:"
              f"enable='lt(t,{S.DRONE_LABEL_OUT})',format=yuv420p10le,"
              f"{S.HLG_PARAMS}[o]")
        inputs = ["-i", str(healed), "-i", str(label)]
    else:
        vf = f"[0:v]setsar=1,format=yuv420p10le,{S.HLG_PARAMS}[o]"
        inputs = ["-i", str(healed)]
    return S._encode(WORK / f"{name}.mp4", inputs, vf, frames)


def main(variant: str) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    out = Path(f"~/Desktop/spree-what-my-drone-sees-mosh-{variant}.mp4") \
        .expanduser()

    pov_png = S.render_text_png(S.LABEL_POV, WORK / "label-pov.png",
                                size=S.POV_LABEL_SIZE, y_frac=S.LABEL_Y,
                                bg_luma=S.LABEL_LUMA)
    drone_png = S.render_text_png(S.LABEL_DRONE, WORK / "label-drone.png",
                                  size=S.DRONE_LABEL_SIZE, y_frac=S.LABEL_Y,
                                  bg_luma=S.LABEL_LUMA)

    c1, c2, music_end = S._cuts()
    end = music_end + round(S.TAIL * S.FPS)
    w, h, x, y = S.SPREE_CROP
    x0, drift = S.BUILDINGS_X0, S.BUILDINGS_DRIFT
    spree = (S.SPREE, S.SPREE_START, c2 - c1, f"crop={w}:{h}:{x}:{y}", 1.0,
             f"{S.SPREE_DENOISE},")

    a = S._segment_pov(WORK / "a.mp4", pov_png, c1)
    orbit = S._segment_sdr(WORK / "c.mp4", S.BUILDINGS, S.BUILDINGS_START,
                           end - c2,
                           f"crop={S.BUILDINGS_W}:2160:'{x0}-{drift}*t':0",
                           S.BUILDINGS_SPEED, "", None)
    if variant == "cut1":
        clean = S._segment_sdr(WORK / "b-clean.mp4", *spree, None)
        parts = (a, _moshed(a, orbit, clean, c2 - c1, drone_png, "cut1"), orbit)
        at = c1
    else:
        b = S._segment_sdr(WORK / "b.mp4", *spree, drone_png)
        parts = (a, b, _moshed(b, orbit, orbit, end - c2, None, "cut2"))
        at = c2

    listing = WORK / f"concat-{variant}.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    S._run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
            "-i", str(listing), "-c", "copy", "-movflags", "+faststart",
            str(out)])

    heal_at = at + MOSH_FRAMES - HEAL_FRAMES
    print(f"{out}  {S._probe(out):.3f}s silent  mosh {at / S.FPS:.3f}s, "
          f"heal {heal_at / S.FPS:.3f}-{(at + MOSH_FRAMES) / S.FPS:.3f}s")


if __name__ == "__main__":
    for v in sys.argv[1:] or ["cut1", "cut2"]:
        main(v)
