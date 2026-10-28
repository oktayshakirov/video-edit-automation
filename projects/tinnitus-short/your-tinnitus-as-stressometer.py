"""Why is my tinnitus louder some days? ~48s Short.

Source: tinnitus-blog/content/posts/your-tinnitus-as-stressometer.mdx, the
same post as the `your-tinnitus-as-stressometer` long form.

**Sentence two is a task, not a verdict.** "Quick check - from zero to ten,
how loud is it right now?" is the article's own log rating, asked of the
viewer's own ears. The jaw Short's "are your teeth touching right now?" is
the channel's second-best Short and the shape `narration.md` now ranks first
("Sharpened 2026-10-01"). The title asks why; nothing in sentences 1-2 says.

**It does not compress the long cut.** The long form walks the loop, the log,
the reaction and a four-step routine. The Short does the single move: rate
it, see the same ears read 8 and then 4, and read the number instead of
fighting it.

**Opener: `Split`, the article's two sample readings.** 8/10 against 4/10,
"same ears?", no winner - the question stays open until sentence seven
answers it. The last three Shorts opened on Search, Counter and Search; this
is the first `Split` on the channel since the variants were built. Labels are
one token a side, because a wrapping label runs into the divider in 9:16
(`shorts.md`, "Split collides with its own labels").

**Two drawn beats, two silhouettes, and neither is `grid` or `steps`** -
every recent tinnitus Short ran those two. `dial` is the meter the title is
about; `diagram(loop=True)` is why a high reading feeds itself.

**A cold close** that recontextualises the opener: the Short opens on a high
number and ends "a high number is a reading, not a verdict". No question.

**No medical claims.** Breathing is named as part of reading the number, not
as something that turns it down. The red-flag routing lives in the long form
and the description, the same as the last four tinnitus Shorts.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/your-tinnitus-as-stressometer.py
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Split
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "your-tinnitus-as-stressometer"

# Same roster as the long form from this post - a pair is one video. A Short
# runs under a minute, so no clip appears twice in it.
TYPE = STOCK / "videos/hands-typing-laptop-keyboard-night-dark/15872811.mp4"
JOURNAL = STOCK / "videos/person-writing-journal-night-lamp/39425736.mp4"
VU = STOCK / "videos/vu-meter-needle-analog-audio/14232785.mp4"
DESK = STOCK / "videos/man-working-late-laptop-office-night/3140468.mp4"
READ = STOCK / "videos/hands-turning-book-pages-lamp-night/11530072.mp4"
ALARM = STOCK / "videos/red-warning-light-flashing-dark/3882891.mp4"
AWAKE = STOCK / "videos/person-sleeping-peacefully-bed-dark/6941199.mp4"
BREATH = STOCK / "videos/hands-on-belly-deep-breathing/8795165.mp4"
WINDOW = STOCK / "videos/city-window-night-quiet-room/8591726.mp4"
SKY = STOCK / "videos/clouds-timelapse-dusk-sky/13282838.mp4"

ROOT = Path(__file__).resolve().parents[2]
THUMB_ART_V = ROOT / "assets/brand/graphics/stress-meter-dial-v.png"

VOICE = "mia"
MUSIC = music.track("night-drift")

# The long form's meter, the same bands.
BANDS = [("Barely there", 0.35, "#ffdab9"),
         ("Noticeable", 0.70, "#f4a261"),
         ("Loud", 1.00, "#e76f51")]

# The article's two sample readings. Exits as the voice says "ten", so it is
# up for the title question and the task, and gone before the answer.
OPENER = Split("8/10", "4/10", "Same ears?", at_word="ten")

# The closing statement, in the opener's own type over the last shot.
OUTRO = "A high number is a [reading]. Not a verdict."

SENTENCES = [
    # The title question, as the viewer would type it.
    ("Why is your tinnitus louder on some days?",),
    # The task. Nothing here answers the title.
    ("Quick check - from zero to ten, how loud is it right now?",),
    # The reframe inside the first ten seconds (the editor's call on the first
    # cut), in the article's own words: "your very own stress-o-meter",
    # "this shift in perspective". It names stress at ~7s, a sentence after
    # the task - sentence 2 still keeps the answer back.
    ("Hold on to that number, because it is your own personal "
     "stress-o-meter.",),
    # And the hinge into the dial.
    ("And that one idea can change your whole perspective on it.",),
    # dial - scale first, needle second.
    ("Zero is silence, and ten is as loud as it gets.",
     "And for a lot of people, the needle climbs with stress."),
    # One sentence, not two: the two readings were split across two shots and
    # the reframe above needed the four seconds back.
    ("One example log reads eight during a deadline, and four that same "
     "evening, after a short walk.",),
    # The answer to the opener's question, and a reversal.
    ("The ears were the same. The stress was not.",),
    # The hinge into the diagram, its own sentence so it cannot eat reveal 0.
    ("And stress can keep itself going.",),
    # diagram, loop=True - one caption chunk per node.
    ("Stress puts you on alert,",
     "so the ringing seems louder,",
     "and that feels like a threat, which keeps the alarm on."),
    ("So panicking at a high number only adds fuel.",),
    ("Read it instead.",
     "Note the number, slow your breathing, and check what is going on "
     "around you."),
    # The cold close, drawn by `outro=`.
    ("A high number is a reading, not a verdict.",),
]

GAPS = [0.85,   # into the task
        1.10,   # time to actually rate it
        0.60,   # the reframe, into its second half
        0.80,   # the hinge into the dial
        1.00,   # the needle lands
        0.85,   # before the reversal
        0.90,   # the reversal lands
        0.70,   # the hinge into the loop
        1.00,   # the loop closes
        0.85,   # before "read it instead"
        0.90,   # before the closing statement
        0.34]   # cold close, nothing after it

SHOTS = [
    # Shot one is the only slot the opener constrains (its block sits at 34%
    # of the height). Previewed as real 9:16 crops: 0.30 was keyboard bokeh
    # with no hand, 0.0 was the back of a hand with no keyboard, 0.20 is the
    # fingers reaching the lit keys.
    Shot(clip=TYPE, clip_at=0.0, clip_ax=0.20),
    Shot(clip=JOURNAL, clip_at=0.5, clip_ax=0.60),
    Shot(clip=VU, clip_at=0.0, clip_ax=0.40),
    Shot(clip=SKY, clip_at=1.0, clip_ax=0.50),
    Shot(graphic="dial",
         payload=(BANDS, 0.8, "a deadline day", "HOW LOUD IS IT RIGHT NOW?",
                  10)),
    Shot(clip=DESK, clip_at=2.0, clip_ax=0.40),
    # The reversal over the evening's book: the walk went with the second
    # example sentence.
    Shot(clip=READ, clip_at=3.5, clip_ax=0.50),
    Shot(clip=ALARM, clip_at=0.5, clip_ax=0.50),
    Shot(graphic="diagram",
         payload=([("On alert", "stress switches it on", "⚡"),
                   ("Ringing seems louder", "every sense turned up",
                    "\U0001F514"),
                   ("Feels like a threat", "and the alarm stays on",
                    "⚠️")],
                  "WHY DOES IT FEED ITSELF?", True)),
    # 4.0s in: awake beside a clock reading 1:28.
    Shot(clip=AWAKE, clip_at=4.0, clip_ax=0.30),
    Shot(clip=BREATH, clip_at=8.0, clip_ax=0.25),
    # The outro card lands on this one and holds to the final frame.
    Shot(clip=WINDOW, clip_at=2.0, clip_ax=0.40),
]


COVER = STOCK / "photos/stressed-woman-laptop-user-picked/4226218.jpg"
HEADLINE = "Does\nstress make\ntinnitus\n[worse?]"


def thumbs(out: Path) -> Path:
    """She and the laptop cut round and scaled to the width on the bottom of
    the frame; above her, the wall's own flat white (sampled from the empty
    top-left corner) takes four rows in dark ink. Not `bleed_portrait`: her
    hair reaches the photo's top edge, and continuing that edge upward drew
    a brown streak to the top of the frame."""
    import numpy as np
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(COVER).convert("RGB")
    crop = src.crop((int(src.width * 0.30), 0, src.width, src.height))
    h = int(crop.height * 1080 / crop.width)
    crop = crop.resize((1080, h), Image.LANCZOS)
    wall = tuple(int(c) for c in np.asarray(
        src.crop((0, 0, src.width // 6, src.height // 6))).reshape(-1, 3).mean(0))
    im = Image.new("RGB", (1080, 1920), wall)
    y, feather = 1920 - h, 160
    im.paste(crop, (0, y))
    a = np.zeros((1920, 1), np.float32)
    a[:y, 0] = 1.0
    a[y:y + feather, 0] = np.linspace(1.0, 0.0, feather)
    mask = Image.fromarray((np.repeat(a, 1080, 1) * 255).astype("uint8"))
    im = Image.composite(Image.new("RGB", im.size, wall), im, mask)
    fill, ink = T.ACCENTS["orange"]
    T._headline(im, HEADLINE, 240, 1080 - 2 * 52, 52, fill, ink, max_lines=4,
                max_block=1920 * 0.36, leading=1.02, band="top",
                margin=int(1920 * 0.13), shadow=14, drop=(6, 8),
                text=(20, 20, 20))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/your-tinnitus-as-stressometer-short.mp4"
    work = Path.home() / "Desktop/.your-tinnitus-as-stressometer-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, outro=OUTRO,
                                        tail=2.0)

    # Same picture and words as the long form (re-done 2026-10-27).
    thumb = thumbs(out.with_name(out.stem + "-thumb.jpg"))

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home() / "Desktop/tinnitus-stress-short-thumb.jpg"))
    else:
        main()
