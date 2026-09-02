"""Why can you hear your heartbeat in your ear - ~45s vertical Short.

Source: tinnitus-blog/content/posts/pulsatile-tinnitus-why-you-hear-your-heartbeat.mdx,
the same post as the `pulsatile-tinnitus` long form.

**It does not compress the long cut.** The long form walks subjective vs
objective, the mechanism, the four cause groups, the spike-vs-damage split and
a full routine. What survives at forty-five seconds is the one reframe a
scroller has not heard - this kind of tinnitus usually has a physical cause a
doctor can find, often blood flow near the ear - plus the red flags and two
practical steps.

**Two drawn beats, two silhouettes.** `grid` (one column) for the causes,
`steps` for what to do while you wait. `compare` and `quote` have no portrait
layout, and `checklist` still carries thecrypto.wiki's gold as a constant.

**No medical claims.** "A cause a doctor can find, and sometimes treat" is the
article's own framing, stated as what the article says and paired with "get it
checked". The close is the action - get it looked at - not "save this".

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/pulsatile-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "pulsatile-tinnitus-why-you-hear-your-heartbeat"

# Same roster as the long form from this post (a pair is one video).
BED_M = STOCK / "videos/man-awake-in-bed-at-night-dark-bedroom-listening"
WORRIED_M = STOCK / "videos/close-up-worried-man-face-dark-room"
WAKE = STOCK / "videos/person-waking-up-sitting-on-edge-of-bed-night-dark"
BLOOD = STOCK / "videos/red-blood-cells-flowing-artery-medical-animation-dark"
SCAN = STOCK / "videos/medical-scan-radiology-monitor-dark"
PHONE = STOCK / "videos/hand-holding-phone-booking-appointment-at-night-dark"

THUMB_PHOTO = (STOCK / "photos"
               / "woman-holding-hands-on-her-chest" / "13419231.jpg")

VOICE = "otis"                     # the male article reader (bare am_puck, ENERGETIC)
MUSIC = music.track("night-drift")

SENTENCES = [
    # A Short has no title card - the first line is the title question. It
    # gets a real break after it (GAPS[0]) so it does not run straight into
    # the next line, which read as robotic on the first cut.
    ("Why can you hear your own heartbeat in your ear?",),

    ("That soft whooshing, in time with your pulse,",
     "has a name.",
     "It is called pulsatile tinnitus."),

    # The lead-in question is spoken here, in the sentence before the beat -
    # not left for the card to carry alone.
    ("It happens when a blood vessel near your ear narrows,",
     "so the flow turns turbulent",
     "and your ear amplifies it into a whoosh.",
     "So what is behind it?"),

    # grid - one caption chunk per card. The first chunk carries the spoken
    # hinge ("It might be...") so the list does not start cold.
    ("It might be narrowed blood vessels,",
     "pressure around the brain,",
     "fluid in the middle ear,",
     "or something like anemia or a thyroid problem."),

    ("But here is the useful part.",
     "Unlike the usual ringing,",
     "this kind often has a cause a doctor can find,",
     "and sometimes treat."),

    ("So get it checked,",
     "especially if it came on suddenly, only affects one ear,",
     "or comes with headaches or vision changes."),

    # steps - one caption chunk per node.
    ("For now, add soft sound at night, just below the whoosh.",
     "Raise the head of your bed.",
     "And note what makes it louder or quieter."),

    ("So don't just live with it - get it looked at.",),
]

# One float per sentence, placed where the meaning turns, not spread evenly.
# GAPS[0] is the break the first cut was missing; 0.75 before the reframe in
# sentence 5; 0.65 before the closing instruction.
GAPS = [0.90, 0.55, 0.45, 0.55, 0.75, 0.55, 0.55, 0.65]

SHOTS = [
    Shot(clip=BED_M / "8376628.mp4"),
    Shot(clip=WORRIED_M / "7279026.mp4"),
    Shot(clip=BLOOD / "35217626.mp4"),
    Shot(graphic="grid",
         payload=([("Narrowed blood vessels", "", "\U0001F493"),
                   ("Pressure around the brain", "", "\U0001F9E0"),
                   ("Fluid in the middle ear", "", "\U0001F442"),
                   ("Anemia or a thyroid problem", "", "\U0001F321️")],
                  "COMMON CAUSES")),
    Shot(clip=SCAN / "7088464.mp4"),
    Shot(clip=WAKE / "30285726.mp4"),
    Shot(graphic="steps",
         payload=([("Soft sound, just below it", "\U0001F30A"),
                   ("Raise the head of the bed", "\U0001F634"),
                   ("Track what changes it", "\U0001F4DD")],
                  "WHILE YOU WAIT")),
    Shot(clip=PHONE / "6414098.mp4"),
]


def main() -> None:
    out = Path.home() / "Desktop/pulsatile-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.pulsatile-tinnitus-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)

    # Same source and headline as the long form. A straight cover crop at
    # cover scale (`zoom=1.0`) - the woman is centred with plain wall either
    # side, so the 9:16 crop fills the frame and only loses background.
    # `band="bottom"` keeps the type off her (downturned) face.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Why can you hear your [pulse?]", image=THUMB_PHOTO, accent="red",
        ax=0.5, zoom=1.0, band="bottom")

    # 16:9 thumbnail for YouTube - straight cover crop, type on the left.
    yt = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), TINNITUS,
        "Why can you hear your [pulse?]", image=THUMB_PHOTO, accent="red",
        crop_at=(0.5, 0.30), crop_zoom=1.0, side="left")

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Reel cover (Instagram, Facebook)")
    print(f"{yt}   <- YouTube thumbnail")


if __name__ == "__main__":
    main()
