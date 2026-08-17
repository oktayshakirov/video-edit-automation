"""Why tinnitus is worse at night. ~40s tinnitus short.

Source: tinnitus-blog/content/posts/tinnitus-and-sleep.mdx, the same post as
the `tinnitus-sleep-long` explainer.

**It does not compress the long cut.** That video walks the whole guide — the
contrast mechanism, why chasing quiet backfires, what to play, the volume rule,
the twenty-minute rule, when to see somebody. None of that fits in forty
seconds and trying would produce a trailer for a video nobody has watched.

What survives is the **one reframe plus the one setting**: your room got
quieter, and the sound goes *just below* the ringing rather than on top of it.
That pairing is deliberate — the reframe is what makes somebody stop scrolling,
and the volume rule is the thing they can act on tonight and the thing almost
nobody already knows. A viewer who sees both videos gets the reframe twice and
the guide once, which is the right way round.

**Two drawn beats, two silhouettes**: `grid` for the two rooms and `steps` for
the three things to do. Cards against a numbered track are genuinely different
outlines; the fix has an order, which is what `steps` shows and a list does not.
Neither is a `checklist` — that beat still carries thecrypto.wiki's gold as a
module constant and renders off-brand here.

**The long cut draws the two rooms with `compare` and this one cannot.** Only
`grid`, `steps` and `bars` are wired for 9:16 — `compare` raises rather than
falling through, which is the right failure. It is no loss here: `compare`
wants three items a side and the portrait layout stacks the columns, so three
and three would be six rows of type on a phone. Two `grid` cards with a second
line each carry the same contrast in half the height.

**No site photographs at all.** The long-form module docstring has the full
screening — the library's sleep images are a daylight hammock, a woman cheering
at a television, and a sleeping child at L220. In 9:16 the crop is tighter and
the problem is worse, so this cut is stock clips and the two beats.

**No medical claims**, and short form is where that is hardest because there is
no room to qualify anything. The sound is described as covering the ringing,
never as treating it. The close asks for a save rather than promising sleep.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus/tinnitus-and-sleep.py
"""

from pathlib import Path

from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.tinnitus.article import render_tinnitus_short

# Screened across their length by the long-form build from this post; the
# trailing comment is the luma/saturation range over the whole clip.
AWAKE = STOCK / "videos/insomnia-awake-night-bed"
NIGHT = STOCK / "videos/sleeping-night-calm-dark"
WATER = STOCK / "videos/calm-water-ripple-dark"
SOUND = STOCK / "videos/sound-wave-visualization-dark"

VOICE = "mia"                   # the same reader as the long form from this
                                # post. Still a candidate, not approved.

SENTENCES = [
    ("Your tinnitus is not worse at night.",),

    ("Your room is.",),

    # **The lead-in goes here, not inside the beat.** A drawn beat times its
    # reveals off the caption starts of its own sentence, so a spare line in
    # that span eats reveal zero and shunts every row one line late.
    ("All day, traffic and voices",
     "cover part of the sound.",
     "Then you turn everything off."),

    # The beat. One caption chunk per card, in card order, nothing else in
    # the span.
    ("All day, something is covering it.",
     "At night, nothing is."),

    ("So do not sleep in silence.",
     "Put steady sound in the room."),

    ("And here is the part",
     "almost everybody gets wrong."),

    ("Do not turn it up",
     "until the ringing disappears."),

    ("Set it just below.",
     "Quiet enough that you can still",
     "faintly hear it underneath."),

    # The fix as a vertical track — a completely different silhouette from
    # the comparison, which is the point of using two beats at all.
    ("On a speaker, not in your ears.",
     "Just below the ringing.",
     "Up if you are still awake in twenty minutes."),

    ("Save this for tonight.",),
]

SHOTS = [
    # 1 — motion on frame one, and a face. A Short is judged in its first
    # second and this reads as "awake at 3am" in a fifth of one.
    Shot(clip=AWAKE / "6944078.mp4"),                # L27-35 S24-33

    Shot(clip=NIGHT / "11956328.mp4"),               # L28 S4-5

    Shot(clip=SOUND / "34645273.mp4"),               # L7 S2

    Shot(graphic="grid",
         payload=([("Your day",
                    "Traffic, voices, something to do"),
                   ("Your bedroom at 11pm",
                    "Silence, and nothing but the ringing")],
                  "SAME EARS, DIFFERENT ROOM")),

    Shot(clip=AWAKE / "8376628.mp4", clip_at=2.0),   # L25-30 S13-17

    Shot(clip=WATER / "36117653.mp4"),               # L27-28 S3-4

    Shot(clip=SOUND / "34645273.mp4", clip_at=8.0),

    Shot(clip=WATER / "11028763.mp4"),               # L28-31 S6-7

    Shot(graphic="steps",
         payload=(["On a speaker, not earbuds",
                   "Just below the ringing",
                   "Up after 20 minutes awake"],
                  "TONIGHT")),

    Shot(clip=NIGHT / "11956219.mp4", clip_at=5.0),  # L29-31 S6
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-sleep-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-sleep-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE)
    print(f"{path}  {total:.1f}s")


if __name__ == "__main__":
    main()
