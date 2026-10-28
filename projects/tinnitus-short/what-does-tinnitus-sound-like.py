"""Is tinnitus ringing or buzzing? - ~55s Short.

Source: tinnitus-blog/content/posts/what-is-tinnitus.mdx, the same post as
the `what-does-tinnitus-sound-like` long form.

**Opener: `Search`, on the Short's own query.** "Is tinnitus ringing or
buzzing" is UCI Otolaryngology's title (1.1M, 932x its median, 10-28) and a
thing people type - a different angle from the long form's "what does
tinnitus sound like". Sentence 1 is that question.

**Sentence 2 overturns the title's either/or and keeps the answer back**
(`narration.md`, 2026-10-11): "Those are only two of the five sounds people
describe." A viewer who left at five seconds could not name the other three,
and sentence 3 opens the next question - which kinds keep time with the body.

**Easier to follow, not the twist alone** (`shorts.md`, 2026-10-13): what
tinnitus is, the four steady sounds on the `spectrum` (sounds mode - one
peak gliding low to high as each is named), the two that keep time with the
body on a `grid`, and the one worth a check.

**It ends on the long form's question** (the user's call, 2026-10-28): "If
you had to name yours, which of the five would it be?" - the same ask in
both cuts, for the comments. It still loops: the replay opens on "ringing,
or buzzing?", two of the five it just asked about.

**The sounds are played, after a warning** (`core/samples.py`, 2026-10-28):
the notice card over a hand turning a volume knob, said aloud, then a quiet
1.6s sample in the pause after each sound's name (`CHUNK_PAD`).

**No medical claims.** The full red-flag list and the disclaimer live in the
long form and the description; the Short names only the one its own content
reaches - a sound in time with the heartbeat - as the article does.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/what-does-tinnitus-sound-like.py
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Search
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "what-is-tinnitus"
DEMAND = ("'what does tinnitus sound like': MUSC Health Short 593k (4820x), "
          "UCI 'Is tinnitus ringing or buzzing?' 1.1M (932x); "
          "teardowns/what-does-tinnitus-sound-like.md")

# Same roster as the long form - a pair is one video. A Short runs under a
# minute, so no clip appears twice in it.
V = STOCK / "videos"
BOWL = V / "singing-bowl-ringing-dark/4488445.mp4"
WATER = V / "waterfall-at-night-dark/27591404.mp4"
WAVEFORM = V / "oscilloscope-sine-wave/34645273.mp4"
AMBER = V / "quiet-bedroom-at-night-window-light/36244322.mp4"
CHEST = V / "hand-on-chest-heartbeat-dark/9737994.mp4"
READER = V / "woman-sitting-by-window-at-night/17673702.mp4"
KNOB = V / "hand-turning-volume-knob-dark/12213088.mp4"

# The long form's sounds, the same peaks.
SOUNDS = [(5200, 6800, "RINGING"),
          (2800, 12000, "HISSING"),
          (110, 210, "HUMMING"),
          (140, 1400, "ROARING")]

# The long form's still and headline - one source for both aspects.
THUMB_PHOTO = STOCK / "photos/young-man-paper-cup-phone/3761514.jpg"
THUMB_HEADLINE = "What does\ntinnitus\n[sound like?]"

VOICE = "noah"          # the noah test, pair 3 of 5 - same voice as the long form
MUSIC = music.track("night-drift")

OPENER = Search("is tinnitus ringing or buzzing")

OUTRO = "If you had to name yours, which of the five would it be?"

# Silence after each naming chunk, for its sample: the flat chunk index
# (sentences walked in order) -> seconds. A Short is one shot per sentence, so
# the long form's one-sentence-per-sound is not open here. 1.6s sample + 0.25
# lead + air before it. The last sound of each beat takes the sentence gap.
CHUNK_PAD = {6: 2.10, 7: 2.10, 8: 2.10,      # ringing, hiss, hum
             10: 2.10}                        # the click

SENTENCES = [
    # The title question - the Search opener types it.
    ("Is tinnitus a ringing, or a buzzing?",),
    # Overturns the either/or; the other three are kept back.
    ("Those are only two of the five sounds people describe.",),
    ("And two kinds keep time with your own body.",),
    ("Tinnitus is any sound you hear that has no source outside you.",),
    # The warning, said and on the notice card, before any sample.
    ("Quiet samples next, so lower your volume if sounds bother you.",),
    # spectrum - the floor, then one phrase per sound, each sample in the
    # pause after it (`CHUNK_PAD`).
    ("Picture every pitch, from low to high.",
     "A ringing tone,",
     "a high hiss, like steam,",
     "a low hum, like insects,",
     "and a roar, like a waterfall."),
    # grid - one chunk per card, the same.
    ("The fifth, a click, can keep time with your jaw.",
     "And a whoosh can keep time with your heartbeat."),
    ("That one is called pulsatile tinnitus, and it is worth getting "
     "checked.",),
    # The long form's closing question, drawn by `outro=` (the user's call,
    # 2026-10-28): the pair ends on the same ask.
    ("If you had to name yours, which of the five would it be?",),
]

# 1.25 after sentence 1: the query is as long as the spike Short's, which
# needed 1.20 for sentence 2 to start after the opener clears.
GAPS = [1.25,   # into sentence 2, after the opener has gone
        0.70,
        0.80,
        0.55,
        0.55,   # into the spectrum
        2.30,   # the roar's sample
        2.80,   # the heartbeat's sample
        0.85,   # before the close
        0.34]   # cold close, nothing after it

SHOTS = [
    # A brass bowl low in the frame, clear of the search bar.
    Shot(clip=BOWL, clip_at=0.5, clip_ax=0.35),
    # The user cut the kettle, then the cricket close-up as disturbing
    # (2026-10-28): the waterfall, the roar - one of the other three.
    Shot(clip=WATER, clip_at=1.0, clip_ax=0.50),
    Shot(clip=WAVEFORM, clip_at=1.0, clip_ax=0.50),
    Shot(clip=AMBER, clip_at=1.0, clip_ax=0.60),
    Shot(clip=KNOB, clip_at=1.0, clip_ax=0.50,
         payload=("NOTICE", "Quiet sound samples next. Lower your volume if "
                            "sounds bother you.")),
    Shot(graphic="spectrum",
         payload=(SOUNDS, "FOUR SOUNDS, LOW TO HIGH", "", "peak"),
         samples=(None, "ringing", "hissing", "humming", "roaring")),
    Shot(graphic="grid",
         payload=([("Clicking", "with your jaw", "\U0001F9B7"),
                   ("Pulsing", "with your heartbeat", "\U0001F493")],
                  "WHAT IT KEEPS TIME WITH"),
         samples=("clicking", "pulsing")),
    Shot(clip=CHEST, clip_at=2.0, clip_ax=0.45),
    # The outro card lands on this one and holds to the final frame.
    Shot(clip=READER, clip_at=1.0, clip_ax=0.50),
]


def thumbs(out: Path) -> Path:
    """The long form's photograph, cut to him and the cup with the string
    coming in from the left, on the bottom of the frame; the white wall
    continued above it (`bleed_portrait`, edge fill) as the ground for three
    dark rows over his head (`thumbnails.md`, rule 3)."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(THUMB_PHOTO).convert("RGB")
    w, h = src.size
    im = T.bleed_portrait(src.crop((int(w * 0.32), 0, int(w * 0.76), h)),
                          fill="edge")
    fill, ink = T.ACCENTS["red"]
    T._headline(im, THUMB_HEADLINE, 240, 1080 - 2 * 52, 52, fill, ink,
                max_lines=3, max_block=560, leading=1.02, band="top",
                margin=int(1920 * 0.10), shadow=10, drop=(4, 6),
                text=(20, 20, 20), align="center")
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/what-does-tinnitus-sound-like-short.mp4"
    work = Path.home() / "Desktop/.what-does-tinnitus-sound-like-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, outro=OUTRO,
                                        chunk_pad=CHUNK_PAD,
                                        tail=2.0)
    thumb = thumbs(out.with_name(out.stem + "-thumb.jpg"))
    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home()
                     / "Desktop/what-does-tinnitus-sound-like-short-thumb.jpg"))
    else:
        main()
