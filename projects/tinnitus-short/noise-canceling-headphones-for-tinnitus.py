"""Do noise-canceling headphones help tinnitus - ~45s vertical Short.

Source: tinnitus-blog/content/posts/noise-canceling-headphones-for-tinnitus.mdx,
the same post as the `noise-canceling-headphones-for-tinnitus` long form.

**It does not compress the long cut.** The long form walks the mechanism, the
reversal, the real downsides and the fix in full. What survives at forty-five
seconds is the one thing a scroller has not heard - noise-canceling helps in
noise and can backfire in total silence, because the brain turns its own gain
up to fill the quiet - plus the downsides worth a glance and the one fix.

**Two drawn beats, two silhouettes.** `grid` for the downsides, `steps` for
the fix - both portrait-safe. `compare` has no portrait layout, so the long
form's central reversal is carried by narration alone here instead.

**Headphones in every frame.** Same footage brief as the long form, and for
the same reason - the subject of this pair is a device, so there is no excuse
for a shot that is only atmosphere. See `footage.md`.

**No medical claims.** Nothing here promises relief; it states what the
article states and closes on the actionable fix, not a question.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/noise-canceling-headphones-for-tinnitus.py
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "noise-canceling-headphones-for-tinnitus"

# Same roster as the long form from this post (a pair is one video), and the
# same brief: every shot has headphones in it.
PUT_ON = STOCK / "videos/man-calm-listening-music-headphones-dark-room-eyes-closed"
SOFA = STOCK / "videos/man-sitting-couch-headphones-dark-room-evening"
DESK_W = STOCK / "videos/person-headphones-sitting-window-calm-evening"
TRAVEL = STOCK / "videos/noise-cancelling-headphones-travel"
STREET = STOCK / "videos/person-walking-city-street-night-headphones-dark-alone"
CALM_W = STOCK / "videos/woman-listening-headphones-calm-dark-room-evening"

THUMB_PHOTO = (STOCK / "photos"
               / "woman-holding-headphones-close-up" / "3757028.jpg")

VOICE = "mia"                        # the explainer default, per the project doc
MUSIC = music.track("night-drift")

SENTENCES = [
    # A Short has no title card - the first line is the title question.
    ("Do noise-canceling headphones actually help tinnitus?",),

    # The payoff, in sentence two - not hedged with "maybe."
    ("In a noisy place, they usually help.",
     "In total silence, they can backfire."),

    ("Silence removes every outside sound,",
     "so your brain turns up its own internal gain to fill the gap,",
     "and your tinnitus gets louder."),

    # The lead-in question is spoken here, in the sentence before the beat.
    ("So before you wear them all day, here is what to watch for.",),

    # grid - one caption chunk per card.
    ("A feeling of pressure in the ear,",
     "a faint hiss of their own,",
     "muffled alarms and voices,",
     "and a real cost for the good ones."),

    ("None of that means they are wrong for you.",
     "It just means they are not magic."),

    ("The fix is simple.",),

    # steps - one caption chunk per node.
    ("Play a soft, steady sound through them.",
     "Keep it just under your tinnitus.",
     "And save real silence for when you sleep."),

    # Cold close: a directive with a reason, not a question.
    ("Never wear them into total silence -",
     "always leave a little sound on."),
]

# One float per sentence, placed where the meaning turns, not spread evenly.
GAPS = [0.90, 0.55, 0.70, 0.45, 0.70, 0.55, 0.45, 0.70, 0.65]

SHOTS = [
    Shot(clip=PUT_ON / "6614768.mp4", clip_at=0.0),
    Shot(clip=STREET / "7948198.mp4", clip_at=0.0),
    Shot(clip=CALM_W / "6688133.mp4", clip_at=0.0),
    Shot(clip=TRAVEL / "6700181.mp4", clip_at=0.0),
    Shot(graphic="grid",
         payload=([("Pressure or fullness in the ear", "", "\U0001F616"),
                   ("A faint hiss of their own", "", "\U000026A1"),
                   ("Muffled alarms and voices", "", "\U0001F514"),
                   ("A real cost, for the good ones", "", "\U0001F4B0")],
                  "WHAT TO WATCH FOR")),
    Shot(clip=SOFA / "5708839.mp4", clip_at=0.0),
    Shot(clip=DESK_W / "6892729.mp4", clip_at=0.0),
    Shot(graphic="steps",
         payload=([("A soft, steady sound underneath", "\U0001F30A"),
                   ("Just under your tinnitus", "\U0001F509"),
                   ("Real silence, saved for sleep", "\U0001F634")],
                  "THE ONE FIX")),
    Shot(clip=PUT_ON / "6614768.mp4", clip_at=15.0),
]


HEADLINE = "Headphones on.\nRinging\n[louder?]"

def thumbs(out: Path) -> Path:
    """Her side of the photo, scaled to the width on the bottom of the frame;
    the teal backdrop continues above and takes the rows in dark ink."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(THUMB_PHOTO).convert("RGB")
    im = T.bleed_portrait(src.crop((int(src.width * 0.12), 0,
                                    int(src.width * 0.72), src.height)))
    fill, ink = T.ACCENTS["red"]
    T._headline(im, HEADLINE, 240, 1080 - 2 * 52, 52, fill, ink, max_lines=4,
                max_block=1920 * 0.36, leading=1.02, band="top",
                margin=int(1920 * 0.13), shadow=14, drop=(6, 8),
                text=(20, 20, 20))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/noise-canceling-headphones-for-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.noise-canceling-headphones-for-tinnitus-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)

    # Same picture and words as the long form (re-set 2026-10-26). One
    # vertical cover only - the 1280x720 second file this wrote is gone; the
    # long form's cover is the YouTube one (thumbnails.md).
    thumb = thumbs(out.with_name(out.stem + "-thumb.jpg"))

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/tinnitus-noise-canceling-short-thumb.jpg"))
    else:
        main()
