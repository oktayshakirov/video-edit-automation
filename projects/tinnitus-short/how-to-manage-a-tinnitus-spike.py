"""What to do during a tinnitus spike - ~45s Short.

Source: tinnitus-blog/content/posts/why-does-tinnitus-spike.mdx, the same
post as the `how-to-manage-a-tinnitus-spike` long form - a re-angle of the
2026-08-28 `why-does-tinnitus-spike` pair onto the promise that stands out
on five channels (`docs/video/demand/teardowns/manage-a-tinnitus-spike.md`).

**Opener: `Search`, like the long form, on its own query.** The user's
preference since 2026-10-24 is `Search` whenever the title is something
people type, and "what to do during a tinnitus spike" is - a different angle
from the long form's "how to manage". Sentence 1 is that question.

**Sentence 2 is a task, not the verdict** (`narration.md`, 2026-10-01):
"Start here: are your shoulders up near your ears right now?" It hands over
one step as something to check on your own body and keeps the plan back. A
viewer who left at five seconds would have one step and no reason for it.

**Not the long form compressed** (`shorts.md`, 2026-10-13): the plain answer
in the order a viewer would ask it - what first, why it works, what else,
how long it lasts, what if it keeps coming back - with one drawn beat, the
`reel`, for the three other steps.

**A cold close that loops.** It ends on "start with your shoulders", which
is what sentence 2 asked, so the replay reads as continuing. No question.

**No medical claims.** The red flags and the disclaimer live in the long
form and the description.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/how-to-manage-a-tinnitus-spike.py
"""

from pathlib import Path

import sys

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Search
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "why-does-tinnitus-spike"
DEMAND = ("re-angle: 'how to manage a tinnitus spike' stands out on 5 channels "
          "(Treble Health 5.8x, Still Tinnitus 3.9x, Alice Moyle 7.0x); "
          "teardowns/manage-a-tinnitus-spike.md")

# Same roster as the long form - a pair is one video. A Short runs under a
# minute, so no clip appears twice in it.
V = STOCK / "videos"
SITTER = V / "person-sitting-still-in-quiet-dark-room/8860237.mp4"
SHOULDERS = V / "woman-massaging-her-own-shoulders/5978076.mp4"
JAW = V / "woman-touching-jaw-tension/4862833.mp4"
SPEAKER = V / "bluetooth-speaker-on-table-dark/29594574.mp4"
FADERS = V / "audio-equalizer-lights-dark/7087627.mp4"
BREATHE_W = V / "woman-breathing-slowly-eyes-closed-dark-room/5114850.mp4"
PHONES = V / "putting-on-headphones-dark-room/6890229.mp4"
SOFA = V / "woman-relaxing-on-sofa-evening-lamp/6264055.mp4"
CURTAIN = V / "dawn-light-through-window-curtains/15671645.mp4"
PEN = V / "hand-writing-in-journal-dark-moody/7612023.mp4"
SITTING = V / "man-meditating-eyes-closed-dark-room/6447702.mp4"

# The long form's still and headline - one source for both aspects.
THUMB_PHOTO = STOCK / "photos/user-pick-woman-laptop/5908779.jpg"   # the user's pick
THUMB_HEADLINE = "Tinnitus\n[spike?]\nDo this\nfirst"

VOICE = "noah"          # the noah test, pair 2 of 5 - same voice as the long form
MUSIC = music.track("night-drift")

OPENER = Search("what to do during a tinnitus spike")

OUTRO = "Skip the silence. Start with your [shoulders]."

SENTENCES = [
    # The title question - the Search opener types it.
    ("What do you do during a tinnitus spike?",),
    # A task on the body; the rest of the plan is kept back.
    ("Start here: are your shoulders up near your ears right now?",),
    ("Let them drop, and unclench your jaw.",),
    # The why.
    ("A spike is your brain on alert, turning its own volume up.",),
    # The hinge into the reel: what feeds the alert.
    ("Tense shoulders and a clenched jaw are part of that alert, and so is "
     "silence.",),
    # reel - one phrase per card.
    ("So calm it. Breathe out longer than you breathe in,",
     "put on a gentle sound, not silence,",
     "and give your mind something else to do."),
    ("Most spikes settle within hours to a few days.",),
    ("If they keep coming back, write down what came before each one.",),
    # The cold close, drawn by `outro=`.
    ("So next time, skip the silent room. Start with your shoulders.",),
]

# 1.20 after sentence 1: this opener clears at 2.9s, and at 1.00 sentence 2
# began under it, so the task ran with no captions at all (first cut,
# 2026-10-27). 1.00 was enough for Beethoven's shorter query.
GAPS = [1.20,   # into the task, after the opener has gone
        0.90,   # let them check
        0.60,
        0.55,
        0.80,   # into the reel
        1.00,   # the reel's last card holds
        0.70,
        0.85,   # before the close
        0.34]   # cold close, nothing after it

SHOTS = [
    # A figure low in a dark room, clear of the search bar.
    Shot(clip=SITTER, clip_at=0.5, clip_ax=0.20),
    Shot(clip=SHOULDERS, clip_at=1.0, clip_ax=0.80),
    # From 16s her hands are at her jaw; at 20s she smiles into her palms,
    # which reads as cute under "unclench your jaw" (first cut).
    Shot(clip=JAW, clip_at=16.0, clip_ax=0.50),
    Shot(clip=SPEAKER, clip_at=0.5, clip_ax=0.50),
    Shot(clip=FADERS, clip_at=0.5, clip_ax=0.35),
    Shot(graphic="reel",
         payload=([(BREATHE_W, "BREATHE OUT LONGER"),
                   (PHONES, "A GENTLE SOUND", 8.0),
                   (SOFA, "SOMETHING ELSE")],
                  "THEN THESE THREE")),
    Shot(clip=CURTAIN, clip_at=10.5, clip_ax=0.55),
    Shot(clip=PEN, clip_at=2.0, clip_ax=0.60),
    # The outro card lands on this one and holds to the final frame.
    Shot(clip=SITTING, clip_at=2.0, clip_ax=0.78),
]


def thumbs(out: Path) -> Path:
    """Her side of the photo on the bottom of the frame; the busy room is
    continued above as a blur (`thumbnails.md`, rule 6) and takes the rows
    in dark ink, clear of her face."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(THUMB_PHOTO).convert("RGB")
    w, h = src.size
    im = T.bleed_portrait(src.crop((int(w * 0.35), int(h * 0.06), int(w * 0.95), h)),
                          fill="blur")
    fill, ink = T.ACCENTS["red"]
    T._headline(im, THUMB_HEADLINE, 240, 1080 - 2 * 52, 52, fill, ink,
                max_lines=4, max_block=600, leading=1.02, band="top",
                margin=int(1920 * 0.13), shadow=14, drop=(6, 8),
                text=(20, 20, 20))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/how-to-manage-a-tinnitus-spike-short.mp4"
    work = Path.home() / "Desktop/.how-to-manage-a-tinnitus-spike-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, outro=OUTRO,
                                        tail=2.0)
    thumb = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home()
                     / "Desktop/how-to-manage-a-tinnitus-spike-short-thumb.jpg"))
    else:
        main()
