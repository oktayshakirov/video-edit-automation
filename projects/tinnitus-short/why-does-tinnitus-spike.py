"""Why does tinnitus spike - ~45s vertical Short.

Source: tinnitus-blog/content/posts/why-does-tinnitus-spike.mdx, the same post
as the `why-does-tinnitus-spike` long form.

**It does not compress the long cut.** The long form walks the gain model, the
delay, the trigger groups and the spike-vs-damage split across seven sections.
What survives here is the one reframe a scroller has not heard - a spike is
your hearing system turning its own gain up, not new damage - plus the two
moves that pay off in forty seconds: triggers stack, and there is a routine
for the first ten minutes.

**Two drawn beats, two silhouettes.** `grid` (one column) for what tips a
spike over, `steps` for the routine. Neither carries verdicts, so no `flow`.
`compare` and `quote` have no portrait layout.

**No medical claims.** The routine is described as calming the nervous
system, which is what the article says it does, never as a treatment. The
close is the action - try it tonight - not "save this".

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/why-does-tinnitus-spike.py

--- what the second cut changed ----------------------------------------------

**The outro was resequenced.** The first cut ran "...pulsing with your
heartbeat? See a doctor." and then "Try it tonight.", which read as "try a
doctor tonight". Now the call to action lands first ("So try it tonight.")
and the red-flag routing follows, explicitly framed as an exception.

**The vertical thumbnail moved to `band="top"`.** A bottom band covered the
subject's mouth; the type sits over her hair now.
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Same roster as the long form from this post (a pair is one video).
FACE_M = STOCK / "videos/man-portrait-dark-moody-serious-european"
FACE_M2 = STOCK / "videos/serious-man-portrait-low-key-dark-studio"
THINK_W = STOCK / "videos/woman-thinking-question-dark-portrait"
KNOB = STOCK / "videos/hand-turning-volume-knob-dark"
ANXIOUS = STOCK / "videos/anxious-woman-sitting-dark-room-night"
WALK = STOCK / "videos/man-walking-city-night-alone"
WNM = STOCK / "videos/white-noise-machine-bedroom-night"
QUIET_ROOM = STOCK / "videos/empty-quiet-room-dark-interior"
OFFICE = STOCK / "videos/man-working-computer-dark-office-night"

THUMB_PHOTO = (STOCK / "photos"
               / "woman-pressing-temples-headache-stress-dark-background"
               / "4865631.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # A Short has no title card - the first line is the title question.
    ("Why does tinnitus suddenly spike?",),

    ("Some days it is a faint hiss.",
     "Some days it roars."),

    ("Here is the part that helps:",
     "a spike is almost never new damage."),

    ("It is your hearing system turning up its own gain "
     "when you are stressed, tired, or on edge.",),

    # grid - one caption chunk per card.
    ("A loud night, or total silence.",
     "A stressful week.",
     "Broken sleep.",
     "Too much caffeine or salt."),

    ("And they stack.",
     "One rough night is fine.",
     "Three, plus a skipped meal, might tip you over."),

    ("When one hits, do this.",),

    # steps - one caption chunk per node.
    ("Call it a flare-up, not a setback.",
     "Slow your breathing right down.",
     "Add soft sound, just below the ringing, never silence.",
     "Then go get absorbed in something else."),

    ("It settles faster when you stop bracing against it.",),

    ("So try it tonight.",),

    # The red-flag routing comes after the call to action, and clearly framed
    # as an exception - not stacked right before "try it tonight", where it
    # read as "try a doctor tonight".
    ("One exception.",
     "If your tinnitus is new, in one ear only, "
     "or pulses in time with your heartbeat,",
     "get that checked by a doctor first."),
]

# One float per sentence. Load-bearing: 0.85 before the reassurance in 3,
# 0.80 after "they stack" so the reversal has room, 0.70 before "try it
# tonight" and again before the exception so the two do not run together.
GAPS = [0.60,
        0.55,
        0.85,
        0.55,
        0.55,
        0.80,
        0.55,
        0.55,
        0.70,
        0.70,
        0.34]

SHOTS = [
    Shot(clip=FACE_M / "30617205.mp4"),
    Shot(clip=ANXIOUS / "7279039.mp4"),
    Shot(clip=THINK_W / "8724510.mp4"),
    Shot(clip=KNOB / "12213088.mp4"),
    Shot(graphic="grid",
         payload=([("A loud night, or silence", "", "\U0001F4E2"),
                   ("A stressful week", "", "\U0001F630"),
                   ("Broken sleep", "", "\U0001F319"),
                   ("Too much caffeine or salt", "", "\U0001F964")],
                  "WHAT TIPS IT OVER")),
    Shot(clip=WALK / "16407855.mp4"),
    Shot(clip=WNM / "7505575.mp4"),
    Shot(graphic="steps",
         payload=([("Call it a flare-up", "\U0001F3F7️"),
                   ("Slow your breathing", "\U0001FAC1"),
                   ("Soft sound, not silence", "\U0001F30A"),
                   ("Get absorbed in something else", "\U0001F9E9")],
                  "THE FIRST TEN MINUTES")),
    Shot(clip=QUIET_ROOM / "2845962.mp4"),
    Shot(clip=FACE_M2 / "30617207.mp4", clip_at=6.0),
    Shot(clip=OFFICE / "8311535.mp4"),
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-spike-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-spike-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)

    # Same source and headline as the long form. `band="top"` - her face
    # fills the centre of the 9:16 crop, so a bottom band covers her mouth;
    # the type sits over her hair and forehead instead.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Why does tinnitus [spike?]", image=THUMB_PHOTO, accent="red",
        ax=0.5, zoom=1.0, band="top")

    # 16:9 thumbnail for YouTube. Let the auto-scorer place the type - no
    # `side` override without a manual `crop_at`.
    yt = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), TINNITUS,
        "Why does tinnitus [spike?]", image=THUMB_PHOTO, accent="red")

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Reel cover (Instagram, Facebook)")
    print(f"{yt}   <- YouTube thumbnail")


if __name__ == "__main__":
    main()
