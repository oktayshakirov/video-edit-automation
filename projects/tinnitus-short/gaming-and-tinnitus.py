"""How long your headset is actually safe for. ~40s tinnitus short.

Source: tinnitus-blog/content/posts/the-gamers-guide-to-preventing-tinnitus.mdx,
the same post as the `tinnitus-gaming-long` explainer.

**The first article short for this site**, on the pipeline added in
`video_automation/tinnitus/article.py` — which is the crypto short with this
brand and this watermark, not a second copy of it.

**It does not reuse the long form's shape.** That video walks the whole guide:
what tinnitus is, why gaming stacks three risks, the mixing problem, a
five-step playbook, the red flags. None of that compresses. What survives at
forty seconds is the single number nobody knows — **an average shooter is
ninety-two decibels, and ninety-two decibels is two and a half hours a week** —
plus the one line that reframes the ringing. A viewer who sees both gets the
guide and the number, not the same script twice.

**Two drawn beats, two silhouettes.** `bars` for the budget and `steps` for the
fix. A proportion is the one thing narration cannot say — "two and a half
hours" means nothing until it is drawn against forty — and the fix has an
order, which is what `steps` shows and a list does not. Neither is a
`checklist`, which is also the beat to avoid here for a mechanical reason: it
is the one drawn object still carrying thecrypto.wiki's gold as a constant.

**No medical claims, and short form is where that is hardest** because there is
no room to qualify anything. Every figure is the article's own. The playbook is
described as what it is — settings — never as something that will prevent or
fix anything for the viewer, and the close asks for a save rather than
promising a result.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/gaming-and-tinnitus.py
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

# Screened across their length; the trailing comment is the luma/saturation
# range over the whole clip. Cached by the long-form build from the same post.
HEADSET = STOCK / "videos/gamer-headset-dark-room"
KEYB = STOCK / "videos/gaming-keyboard-hands-night"
CTRL = STOCK / "videos/video-game-controller-dark"
ESPORTS = STOCK / "videos/esports-player-computer-night"

VOICE = "mia"                   # the same reader as the long form from this
                                # post. Still a candidate, not approved.

SENTENCES = [
    ("You turn the volume up",
     "to hear the footsteps."),

    # **The question goes here, not inside the beat.** A drawn beat times its
    # reveals off the caption starts of its own sentence, so a lead-in line
    # inside that span eats reveal zero and shunts every row one line late.
    ("An average shooter",
     "runs at ninety two decibels.",
     "So how long is that safe for?"),

    # The beat. One caption chunk per row, in row order, nothing else in the
    # span.
    ("Eighty decibels buys you forty hours a week.",
     "Ninety two buys two and a half.",
     "A loud concert buys two and a half minutes."),

    ("And the ringing after a long session",
     "is not the damage.",
     "It is your ears reporting it."),

    ("You are not turning it up",
     "because you like it loud.",
     "You turn it up because footsteps",
     "are mixed almost silent."),

    # The fix, as a vertical track — a completely different silhouette from
    # the bars, which is the point of using two beats at all.
    ("Master at sixty percent.",
     "Effects down, dialogue up.",
     "Add a limiter."),

    ("You still hear the footsteps.",
     "Your ears just stop paying for them."),

    ("Save this before your next session.",),
]

SHOTS = [
    # 1 — motion on frame one, and a face. A Short is judged in its first
    # second and this reads as "gamer" in a fifth of one.
    Shot(clip=HEADSET / "9070656.mp4"),              # L32-38 S28-32

    Shot(clip=KEYB / "9071216.mp4", clip_at=2.0),    # L41-54 S9-10

    # 2 — the budget. Fractions are hours-per-week over forty, times 0.60.
    # The value text travels with the end of its own bar, so a long top bar
    # pushes "40 hours" off the right edge — and the factor that clears it is
    # frame-dependent, not a property of the data: 0.90 fits at 1920 and had to
    # come down to 0.60 at 1080. One factor across the whole set leaves the
    # proportions between the rows exact, which is all this beat claims.
    Shot(graphic="bars",
         payload=([("80 dB · doorbell", 0.60, "40 hours"),
                   ("92 dB · shooter", 0.037, "2h 30"),
                   ("110 dB · concert", 0.006, "2.5 min")],
                  "SAFE TIME PER WEEK")),

    Shot(clip=HEADSET / "10620277.mp4", clip_at=1.0),   # L18-22 S4-5

    # The article's own hero, and the only picture in the library of somebody
    # actually at a desk with a headset on.
    Shot(image=IMG / "gamer.jpg", zoom=1.12, pan=(0.02, -0.02),
         aspect=1.15, bias=0.40),

    Shot(graphic="steps",
         payload=(["Master at 60%",
                   "Effects down, dialogue up",
                   "Add a limiter"],
                  "THE FIX")),

    Shot(clip=ESPORTS / "9071228.mp4", clip_at=6.0),    # L50-56 S13-17

    Shot(clip=CTRL / "8128022.mp4", clip_at=1.0),       # L25-27 S21-24
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-gaming-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-gaming-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE)

    # **Same source and same headline as the long form from this post** —
    # `gaming-and-tinnitus.py` in `tinnitus-long/` uses this exact site photo
    # and "Your headset is [too loud]". The pairing rule the sleep pair
    # settled: always match a Short to its long form.
    #
    # `band="bottom"`, not the default `"top"`. At `ax=0.6` his face sits in
    # the upper two-thirds of the crop and the type at the default top band
    # landed across his nose and mouth — swept both bands and looked at the
    # actual render rather than assuming from the crop's dark upper corner.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Your headset is [too loud]", image=IMG / "gamer.jpg", accent="red",
        ax=0.6, zoom=1.0, band="bottom")
    print(f"{path}  {total:.1f}s")
    print(f"{thumb}")


if __name__ == "__main__":
    main()
