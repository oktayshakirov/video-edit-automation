"""Is tinnitus an ear problem or a brain problem? - ~50s Short.

Source: tinnitus-blog/content/posts/the-role-of-neural-pathways-in-tinnitus-
perception.mdx, the same post as the `is-tinnitus-in-the-ear-or-the-brain`
long form.

**Opener: `Split`, shared with the long form.** EAR against BRAIN is a
comparison, and the last three tinnitus Shorts all opened on `Search`. A pair
may share its opener (`shorts.md`, 2026-10-20); rotation is across videos.
No `winner`: the comparison is the open loop. Sentence 1 is UCI
Otolaryngology's title, the standout this pair was picked on (422k, 343x).

**Sentence 2 hands over a task, not a verdict** (`narration.md`,
2026-10-01): "Listen for yours right now. Is it louder than a second ago?"
Its first words stay on the title's subject, and its answer is one the
viewer does not already know - noticing it is part of what sets its
loudness (the article's prefrontal and attention section), which is what
the rest of the Short then explains. Nobody can answer the title from
sentences 1-2.

**Easier to follow, not the twist alone** (`shorts.md`, 2026-10-13): the
path a sound takes on a `reel`, the gain turned up, then the alarm loop as a
`diagram(loop=True)`. Two beats, two silhouettes.

**A cold close that recontextualises the opening** (`narration.md`, "A
Short's ending loops"): "Your ears start it. Your brain turns it up." answers
ear-or-brain without re-asking it, and the replay opens on the same question.
It closes on the clip it opened on (`shorts.md`, 2026-10-28).

**No medical claims.** Nothing here says the loop can be broken or the sound
lowered. The red flags and the disclaimer live in the long form and the
description.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/is-tinnitus-in-the-ear-or-the-brain.py
    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/is-tinnitus-in-the-ear-or-the-brain.py --thumb
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Split
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "the-role-of-neural-pathways-in-tinnitus-perception"
DEMAND = ("'is tinnitus in the ear or the brain': UCI 'Is tinnitus an ear "
          "problem or a brain problem?' Short 422k (343x), Treble 'The "
          "SHOCKING Truth About Tinnitus And Your Brain' 76k (7.4x); "
          "teardowns/is-tinnitus-in-the-ear-or-the-brain.md")

# Same roster as the long form - a pair is one video. No clip twice in a
# Short, except the opening clip again at the close, later in the file.
V = STOCK / "videos"
EARBUDS = V / "person-putting-in-earbuds-dark/5008497.mp4"
THINK = V / "woman-thinking-quietly-dark-room-evening-portrait/9808085.mp4"
SITTING = V / "person-sitting-still-in-quiet-dark-room/8860237.mp4"
SPEAKER = V / "concert-speaker-stack-stage/8513956.mp4"
WAVE = V / "sound-wave-visualization-dark/34645273.mp4"
FIBER = V / "fiber-optic-light-cables-dark/8817471.mp4"
ORANGE = V / "brain-neurons-abstract-dark/29184317.mp4"
KNOB = V / "hand-turning-volume-knob-dark/12213088.mp4"
ALARMCLK = V / "alarm-clock-night-dark-bedroom/35999376.mp4"
MEDSCAN = V / "medical-scan-radiology-monitor-dark/7088464.mp4"

# The long form's still and headline - one source for both aspects.
THUMB_PHOTO = STOCK / "photos/man-thinking-silhouette-white/30560359.jpg"
THUMB_HEADLINE = "Is it your\nears, or your\n[brain?]"

VOICE = "noah"          # the noah test, pair 4 of 5 - same voice as the long form
MUSIC = music.track("night-drift")

OPENER = Split("Ear", "Brain", "WHERE IS IT MADE?")

OUTRO = "Your ears start it. Your [brain] turns it up."

SENTENCES = [
    # The title question - the Split opener stands over it.
    ("Is tinnitus an ear problem, or a brain problem?",),
    # A task, not a verdict.
    ("Listen for yours right now.", "Is it louder than a second ago?"),
    ("If it is, nothing in your ears changed in that second.",),
    # The hinge into the reel.
    ("So follow the path a sound takes.",),
    # reel - one phrase per card, about two seconds each.
    ("Hair cells in your ear turn it into signals,",
     "the nerve carries them up,",
     "and your brain is where you actually hear it."),
    ("When hair cells wear down, less arrives, so the brain turns up its own "
     "volume, until its background activity sounds like ringing.",),
    # The hinge into the loop.
    ("And how loud it seems is set by attention and stress.",),
    # diagram, loop=True - one chunk per node.
    ("You notice it,",
     "your brain's alarm reacts,",
     "stress turns the volume up,",
     "and you notice it more."),
    ("Scans can see this activity, even in a silent room. It is real, not "
     "imagined.",),
    # The cold close, drawn by `outro=`.
    ("Your ears start it. Your brain turns it up.",),
]

GAPS = [1.20,   # into sentence 2, after the opener has gone
        0.90,   # the task - room to listen
        0.70,
        0.45,   # into the reel
        0.80,
        0.70,
        0.45,   # into the loop
        1.30,   # the loop arrow draws across this
        0.85,   # before the close
        0.34]   # cold close, nothing after it

SHOTS = [
    # A hand and the earbud case low in the frame, clear of the Split.
    Shot(clip=EARBUDS, clip_at=0.5, clip_ax=0.50),
    Shot(clip=THINK, clip_at=1.0, clip_ax=0.62),
    Shot(clip=SITTING, clip_at=2.0, clip_ax=0.52),
    Shot(clip=SPEAKER, clip_at=2.0, clip_ax=0.45),
    Shot(graphic="reel",
         payload=([(WAVE, "HAIR CELLS"),
                   (FIBER, "THE NERVE", 4.0),
                   (ORANGE, "THE BRAIN")],
                  "THE PATH OF A SOUND")),
    Shot(clip=KNOB, clip_at=1.0, clip_ax=0.55),
    Shot(clip=ALARMCLK, clip_at=1.0, clip_ax=0.45),
    Shot(graphic="diagram",
         payload=([("You notice it", "", "\U0001F56F"),
                   ("The alarm reacts", "stress kicks in", "\U0001F6A8"),
                   ("The volume goes up", "", "\U0001F50A"),
                   ("You notice it more", "", "\U0001F501")],
                  "THE ALARM LOOP", True)),
    # The monitor of brain scans, not his desk - it sits at the left edge.
    Shot(clip=MEDSCAN, clip_at=2.0, clip_ax=0.08),
    # The outro card lands on the opening clip, later in it.
    Shot(clip=EARBUDS, clip_at=8.0, clip_ax=0.50),
]


def thumbs(out: Path) -> Path:
    """The long form's silhouette, cut round his head and hand and set on
    the bottom of the frame; the studio white continued above it
    (`bleed_portrait`, edge fill) as the ground for three dark rows over his
    head (`thumbnails.md`, rule 3)."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(THUMB_PHOTO).convert("RGB")
    w, h = src.size
    im = T.bleed_portrait(src.crop((int(w * 0.10), int(h * 0.12), w, h)), y=440,
                          fill="edge")
    fill, ink = T.ACCENTS["red"]
    T._headline(im, THUMB_HEADLINE, 240, 1080 - 2 * 52, 52, fill, ink,
                max_lines=3, max_block=560, leading=1.02, band="top",
                margin=int(1920 * 0.10), shadow=10, drop=(4, 6),
                text=(20, 20, 20), align="center")
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/is-tinnitus-in-the-ear-or-the-brain-short.mp4"
    work = Path.home() / "Desktop/.is-tinnitus-in-the-ear-or-the-brain-short-work"
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
                     / "Desktop/is-tinnitus-in-the-ear-or-the-brain-short-thumb.jpg"))
    else:
        main()
