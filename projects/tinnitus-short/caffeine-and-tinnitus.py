"""Does caffeine make tinnitus worse - ~45s vertical Short.

Source: tinnitus-blog/content/posts/caffeine-and-tinnitus.mdx, the same post
as the `caffeine-and-tinnitus` long form.

**It does not compress the long cut.** The long form walks the mechanism, the
half-life, the dose table and the two-week test across nine sections. What
survives here is the one move a scroller has not heard: quitting caffeine
suddenly brings headaches, bad sleep and irritability, all of which make
tinnitus louder, so cold turkey *looks* like proof caffeine was the culprit.
Then the two payoffs - what actually stacks, and the test that starts by
moving the cup, not cutting it.

**Two drawn beats, two silhouettes.** `grid` (one column) for what stacks a
spike, `steps` for the test. Neither carries verdicts, so no `flow`.
`compare` and `quote` have no portrait layout.

**No medical claims.** Caffeine is described by what it does; the test is a
way to learn your own response, never a treatment. The close is the action -
try the earlier cup - not "save this". The red-flag routing lands after the
call to action, framed as an exception.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/caffeine-and-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Same roster as the long form from this post (a pair is one video).
CONCERN_W = STOCK / "videos/close-up-woman-face-thinking-concerned-dark"       # 4584772 L60
MUG_KITCHEN = STOCK / "videos/man-drinking-from-mug-dark-kitchen-morning"      # 35674404 L27-46
ENERGY = STOCK / "videos/energy-drink-can-dark"                              # 7033926 L15
CUP = STOCK / "videos/cup-of-coffee-morning-dark-moody"                      # 6950170 L53
AWAKE = STOCK / "videos/person-lying-awake-in-bed-night-dark"                # 6943537 L42
THINK_M = STOCK / "videos/man-thinking-worried-dark-room-window"             # 7280528 L42
WATER = STOCK / "videos/person-adding-water-to-coffee-glass-dark"            # 5542396 L50
WINDOW = STOCK / "videos/man-contemplating-window-night-city-dark"          # 4538212 L51

THUMB_PHOTO = STOCK / "photos/man-coffee-mug-dark-serious/32536421.jpg"        # L48, subject right

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # A Short has no title card - the first line is the title question.
    ("Does caffeine make tinnitus worse?",),

    ("Maybe - but quitting it suddenly might be the bigger mistake.",),

    ("Stop caffeine cold, and you get headaches, bad sleep, and irritability "
     "for days.",),

    ("And all three of those make tinnitus louder.",),

    ("So going cold turkey feels like proof that caffeine was the problem,",
     "when it was really the withdrawal."),

    # Hinge into the grid - say the point, then show the graphic, the same
    # setup the long form gives every list. A grid's reveals come from the
    # first N caption starts of its own sentence, so the hinge cannot ride
    # inside the beat sentence without shunting every card a line late - it
    # gets its own sentence and its own shot.
    ("And caffeine is rarely the only thing pushing it.",
     "It stacks with everything else that day."),

    # grid - one caption chunk per card.
    ("A cup too late in the day.",
     "The bad night after it.",
     "A stressful week.",
     "Energy drinks stacked on all of it."),

    ("If you want to test it, do this.",),

    # steps - one caption chunk per node.
    ("Log your drinks, your sleep, and your ringing.",
     "Move your last cup earlier, don't cut it yet.",
     "Only then taper, slowly.",
     "Judge it after two weeks."),

    ("Most people find it is the timing, not the caffeine.",),

    ("So try the earlier cup first.",),

    # Red-flag routing after the call to action, framed as an exception.
    ("One exception.",
     "If your tinnitus is new, in one ear only, "
     "or pulses in time with your heartbeat,",
     "get that checked by a doctor first."),
]

# One float per sentence. Load-bearing: 0.80 after "make tinnitus louder" so
# the reversal has room, 0.70 before "try the earlier cup" and again before
# the exception so the two do not run together.
GAPS = [0.60,
        0.55,
        0.55,
        0.80,
        0.55,   # ...when it was really the withdrawal.
        0.55,   # hinge: it stacks with everything else
        0.55,   # grid
        0.55,   # if you want to test it, do this
        0.55,   # steps
        0.70,
        0.70,
        0.34]

SHOTS = [
    Shot(clip=CONCERN_W / "4584772.mp4", clip_ax=0.5),
    Shot(clip=MUG_KITCHEN / "35674404.mp4", clip_at=2.0, clip_ax=0.55),
    Shot(clip=ENERGY / "7033926.mp4", clip_ax=0.5),
    Shot(clip=AWAKE / "6943537.mp4", clip_ax=0.5),
    Shot(clip=THINK_M / "7280528.mp4", clip_ax=0.5),
    Shot(clip=CUP / "6950170.mp4", clip_ax=0.5),
    Shot(graphic="grid",
         payload=([("A cup too late in the day", "", "☕"),
                   ("The bad night after it", "", "\U0001F634"),
                   ("A stressful week", "", "\U0001F630"),
                   ("Energy drinks on top", "", "⚡")],
                  "WHAT ACTUALLY STACKS")),
    Shot(clip=WATER / "5542396.mp4", clip_ax=0.5),
    Shot(graphic="steps",
         payload=([("Log drinks, sleep, ringing", "\U0001F4D2"),
                   ("Move the last cup earlier", "⏰"),
                   ("Only then taper, slowly", "\U0001F4C9"),
                   ("Judge it after two weeks", "\U0001F4C5")],
                  "THE TWO-WEEK TEST")),
    Shot(clip=CONCERN_W / "4584772.mp4", clip_at=8.0, clip_ax=0.5),
    Shot(clip=WINDOW / "4538212.mp4", clip_ax=0.62),
    Shot(clip=MUG_KITCHEN / "35674404.mp4", clip_at=10.0, clip_ax=0.55),
]


def main() -> None:
    out = Path.home() / "Desktop/caffeine-and-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.caffeine-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)

    # Same source and headline as the long form. `band="bottom"` - his head
    # sits in the upper third of the 9:16 crop, so a top band runs over it;
    # `ax=0.7` keeps him in frame.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Does caffeine make tinnitus [worse?]", image=THUMB_PHOTO,
        accent="orange", ax=0.7, zoom=1.0, band="bottom")

    # 16:9 thumbnail for YouTube. Auto-scorer places the type - no `side`
    # override without a manual `crop_at`.
    yt = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), TINNITUS,
        "Does caffeine make tinnitus [worse?]", image=THUMB_PHOTO,
        accent="orange")

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Reel cover (Instagram, Facebook)")
    print(f"{yt}   <- YouTube thumbnail")


if __name__ == "__main__":
    main()
