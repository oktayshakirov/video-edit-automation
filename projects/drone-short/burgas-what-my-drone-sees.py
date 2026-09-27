"""Burgas What My Drone Sees — silent two-beat POV/reveal short.

A new format for this channel and the first one built from a phone clip rather
than from graded drone selects. Two beats, no tag:

1. **what i see** — an iPhone POV of the RC controller in hand on the balcony,
   the live drone feed running on its screen, tilting up to the ordinary
   eye-level view of the beach. Frame one already contains the reveal in
   miniature, which is what buys the second beat.
2. **what my drone sees** — the same beach top-down at 4K, surf line running
   down the 9:16 frame. Same place, same minute, nothing in common to look at.

**A rotate-phone tag was cut after the first review**, which puts this back in
line with `drone-short.md`'s standing "never use rotate your phone". The first
build argued the rule only bites in the opening second and ran the graphic as a
closing pointer to a landscape cut; the user's verdict on seeing it was to drop
it. Worth knowing if the idea comes back: the black-background key that made it
work was `lumakey=0.04:0.16:0`, which holds the glyph antialiasing a `colorkey`
would chew off, and the graphic needed a blurred dark halo under it or the white
outline vanished against sunlit foam.

**Silent, and deliberately.** No narration, so the TikTok trending-sound lever
stays available (`drone-short.md`, *Audio strategy*), and `-an` means no audio
track at all rather than a silent one.

The two sources disagree on everything — 59.94fps HLG 10-bit portrait against
30fps SDR 4K landscape — so each segment is normalised to 1080x1920 / 30fps /
yuv420p on its own before `concat`, which demands they already match.
"""

import subprocess
from pathlib import Path

from video_automation.core.media import build_proxy
from video_automation.core.vertical import (OUT_H, OUT_W, pick_crop,
                                            render_text_png)

SOURCE_POST = None                      # off-site: a format test, no article

POV = Path("~/Desktop/Drone Videos/Controller/IMG_1325.MOV").expanduser()
AERIAL = Path("~/Desktop/Drone Videos/Footage/Burgas/Beach Waves 2.mp4").expanduser()

OUT = Path("~/Desktop/burgas-what-my-drone-sees.mp4").expanduser()
WORK = Path("~/Desktop/.work-burgas-what-my-drone-sees").expanduser()

FPS = 30

# Both durations are set by the track the user is laying under this, not by the
# footage — the cut has to land on 3.50s. That is a second past where the tilt
# settles and leaves the static balcony tail on the floor.
POV_START, POV_DUR = 0.20, 3.50

# The aerial is a 44s lateral drift and the water reads most turquoise late in
# it. 26s in, the surf line is centred and the colour is at its best, and the
# crop was checked out to 39.0s — the far end of this span — rather than only
# at the in-point, because a lateral drift can walk its subject out of frame.
AERIAL_START, AERIAL_DUR = 26.0, 13.00

# The label clears early and the water runs on unlabelled. Over a 6.5s shot that
# would have been dead air; over 13s it is the shot doing the talking, which is
# the half of the joke that does not need a caption.
LABEL_OUT = 5.20

# "Very small text in the middle" — down from the 46px silent-card default, and
# centred on the frame rather than the card's usual 0.40.
LABEL_SIZE = 34
LABEL_Y = 0.50
LABEL_LUMA = 0.0                        # white ink, dark halo — see main()

LABEL_POV = "what i see"
LABEL_AERIAL = "what my drone sees"


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True, capture_output=True)


def _probe(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def _segment_pov(dst: Path, label: Path) -> Path:
    """Beat one. The source carries a -90 display matrix, so ffmpeg hands us
    1080x1920 already — no crop, only a normalise and the label burn."""
    vf = (f"[0:v]scale={OUT_W}:{OUT_H}:flags=lanczos,fps={FPS},"
          f"format=yuv420p,setsar=1[v];[v][1:v]overlay=0:0[o]")
    _run(["ffmpeg", "-v", "error", "-y",
          "-ss", f"{POV_START}", "-t", f"{POV_DUR}", "-i", str(POV),
          "-i", str(label),
          "-filter_complex", vf, "-map", "[o]", "-an",
          "-c:v", "libx264", "-crf", "18", "-preset", "slow",
          "-pix_fmt", "yuv420p", str(dst)])
    return dst


def _segment_aerial(dst: Path, box: tuple[int, int, int, int],
                    label: Path) -> Path:
    """Beat two. The label clears before the end so the shot loops on picture."""
    x, y, w, h = box

    vf = (
        f"[0:v]crop={w}:{h}:{x}:{y},scale={OUT_W}:{OUT_H}:flags=lanczos,"
        f"fps={FPS},format=yuv420p,setsar=1[bg];"
        f"[bg][1:v]overlay=0:0:enable='lt(t,{LABEL_OUT})'[o]"
    )
    _run(["ffmpeg", "-v", "error", "-y",
          "-ss", f"{AERIAL_START}", "-t", f"{AERIAL_DUR}", "-i", str(AERIAL),
          "-i", str(label),
          "-filter_complex", vf, "-map", "[o]", "-an",
          "-c:v", "libx264", "-crf", "18", "-preset", "slow",
          "-pix_fmt", "yuv420p", str(dst)])
    return dst


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=True)

    proxy = WORK / "aerial.proxy.mp4"
    if not proxy.exists():
        build_proxy(AERIAL, proxy)
    # Top-down footage carries no sky, so there is nothing for `zoom` to pull
    # away from — 1.0 keeps full sensor height and the whole surf line.
    box = pick_crop(proxy, zoom=1.0)

    # White on both beats, the user's call over the template's own sampled ink.
    # `bg_luma` is pinned dark rather than measured: it is the only control over
    # the halo, and at a sampled value above 0.62 the halo turns white too and
    # erases white type. Low luma is what keeps the halo black.
    pov_png = render_text_png(
        LABEL_POV, WORK / "label-pov.png", size=LABEL_SIZE, y_frac=LABEL_Y,
        bg_luma=LABEL_LUMA)
    aerial_png = render_text_png(
        LABEL_AERIAL, WORK / "label-aerial.png", size=LABEL_SIZE, y_frac=LABEL_Y,
        bg_luma=LABEL_LUMA)

    parts = [_segment_pov(WORK / "a.mp4", pov_png),
             _segment_aerial(WORK / "b.mp4", box, aerial_png)]

    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p}'\n" for p in parts))
    _run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
          "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(OUT)])

    print(f"{OUT}  {_probe(OUT):.2f}s  crop={box}")


if __name__ == "__main__":
    main()
