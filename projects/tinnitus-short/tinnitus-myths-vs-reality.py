"""Are these tinnitus myths actually true? ~40s tinnitus short.

Source: tinnitus-blog/content/posts/tinnitus-myths-vs-reality.mdx, the same
post as the `tinnitus-myths-long` explainer.

**It does not compress the long cut.** That video walks all eight myths
across five carded sections. What survives here is the three myths a viewer
is most likely to believe without question, busted in one `checklist`, plus
the one twist a viewer has not necessarily heard: no cure does not mean no
options.

**Two drawn beats, two silhouettes**: `checklist` with `flow=True` for the
three myths (the narration states each claim, so holding the crosses back
would put the picture behind the voice), `steps` — with an icon per node —
for all five real management approaches, matching the long form's playbook
rather than a trimmed version of it. `compare` and `quote` have no portrait
layout and raise rather than falling through, which is why the long form's
comparison is long-form only.

**No medical claims.** Sound therapy, hearing aids and talking therapy are
named as what the article calls them - ways to manage tinnitus - never as a
cure. The close asks for a save, not a result.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/tinnitus-myths-vs-reality.py

--- what the third cut changed -----------------------------------------------

**All five playbook items now, not three.** The user's note: cutting the
playbook down to three when the long form has five reads as incomplete, and a
Short is not bound to any runtime ceiling here - "up to a minute or more if
the content is interesting and relevant". The `steps` beat scales to five
nodes without a layout change.

**The per-word caption delay is fixed, not reverted.** It was a real bug, not
an inherent limit: `_karaoke_sprites` was apportioning each word's on-screen
window across the caption's *displayed* span, which the hold-until-next rule
stretches to the start of the next caption — so on a short sentence with a
long following pause, every word lit late, worst on the last one or two.
`Caption` now carries `speech_end`, the true pre-stretch boundary, captured
once at creation and never touched by the stretch. Word timing is apportioned
against that instead. See `core/voiceover.py` and `crypto/build.py`.

**Neither face from the first two cuts survives.** The opener
(`woman-portrait-low-key.../4587160`) was called out as reading as too
culturally specific for a general myths video, and the closer
(`.../7298368`) was flagged for visible skin texture in a tight close-up.
Both are replaced, not reframed - the pairing rule (open and close on the
same two faces) is what makes the loss worth just swapping the source.

--- what the fourth cut changed -----------------------------------------------

**The third cut's replacement faces repeated the fault they replaced.** Both
landed as Black actors, and immediately followed by `TEMPLES` (also Black) in
the long form's hook, three in a row. The short only stacks two (`FACE1` then
`TEMPLES`), which was not itself flagged, but `FACE1` is swapped again for the
same reason the long form's opener was: screening stock by `luma` alone
structurally favours darker skin against a dark backdrop, and casting has to
be looked at, not just measured. New faces, same bookend pair as the long
form: `young-woman-portrait-dark-moody.../6068300` and
`man-serious-portrait-dark-studio.../6415877` — the second is a single reuse
of a shoot flagged as over-used on an *earlier* cut, correct now because that
shoot is used nowhere else in either video.

**Thumbnail replaced.** Same reasoning as the long form: a direct, engaged
gaze reads better than a subject looking away. See `main()`.

--- what the fifth cut changed -------------------------------------------------

**The checklist was `flow=True` and it was the wrong instrument.** `flow`
marks each item false the instant it is spoken, which is right when the
narration itself carries the verdict ("Not a court ruling."). Here the
narration never says the claims are wrong — it just states three things a
viewer already half-believes — so marking them false in real time answered a
question before it was asked, and the user's note was exactly this: read the
myths first, *then* react, *then* let the strike land. Fixed by dropping
`flow` (back to the two-phase default: items appear unmarked, verdicts land
together in the pause after the last one) and adding a fourth caption chunk
to the same sentence — "Turns out, none of that is true." — so the reaction
is spoken into the pause the crosses draw during, rather than assumed.

**The causes list got a spoken hinge.** "Aging, medication, even an ear
infection can trigger it too" used to open cold, right off the checklist.
The user's ask was a natural lead-in, matching the hinge-sentence rule this
format already uses for beats: the sentence now opens "So here are some real
reasons" before the list, in the same continuous utterance rather than a
separate sentence with its own gap — no new shot needed.

**Thumbnail is the user's own pick**, not a stock search result: a Pexels
photo of a woman pressing her temples, fetched by id rather than found by
query. Bright and pastel, the opposite of this brand's usual dark palette —
`render_thumb`'s own scrim darkens the type's half regardless, so it composes
cleanly without any change to the renderer.
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Screened and watched; the trailing comment is the luma/saturation range
# over the whole clip.
FACE1 = STOCK / "videos/young-woman-portrait-dark-moody-looking-away"  # L21 S11
FACE2 = STOCK / "videos/man-serious-portrait-dark-studio-black-background"  # L14-17
TEMPLES = STOCK / "videos/tired-man-rubbing-temples-dark"           # L37 S16
DESK = STOCK / "videos/man-thinking-dark-room-window-night"         # L36-37 S13
BED = STOCK / "videos/person-sitting-on-bed-dark-bedroom-night-thinking"
NEURONS = STOCK / "videos/brain-neurons-abstract-dark"              # L26 S46
LISTEN = STOCK / "videos/man-listening-music-dark-room-night"       # L42 S8
MEDITATE = STOCK / "videos/man-meditating-dark-room-calm"           # L41 S6

# The user's own pick, fetched by Pexels id rather than a search query.
# Landscape 5760x3840, bright and pastel - `render_thumb`'s own scrim
# darkens the type's half regardless of source brightness.
THUMB_PHOTO = STOCK / "photos/user-picked/3958868.jpg"

VOICE = "mia"                   # the same reader as the long form from this
                                # post. Still a candidate, not approved.
MUSIC = music.track("night-drift")

SENTENCES = [
    # Every short opens by asking its own title question - a Short has no
    # title card and no chapter list, so the viewer arrives with nothing.
    ("Are these tinnitus myths actually true?",),

    ("You have probably heard all three.",),

    # The beat. One caption chunk per row for the three claims, then a
    # fourth chunk that is not an item at all - it is the reaction, spoken
    # into the pause where the crosses draw. `item_count` for `checklist` is
    # `len(items)` (3), so this fourth chunk never claims a reveal slot; it
    # is just words the voice says while the beat's own two-phase timing
    # marks the claims false on its own.
    ("Only loud noise causes tinnitus.",
     "It always goes away on its own.",
     "There is nothing you can do about it.",
     "Turns out, none of that is true."),

    # The hinge, in the same breath as the list it introduces - not a
    # separate sentence with its own gap.
    ("So here are some real reasons.",
     "Aging, medication, even an ear infection can trigger it too."),

    ("And for a lot of people, it does not just fade.",
     "It can last for years."),

    ("There is no single cure.",),

    ("But there are five real ways to manage it.",),

    # Five chunks, matching the long form's playbook exactly rather than a
    # trimmed version of it.
    ("Hearing aids.",
     "Sound therapy.",
     "Talking therapy for the distress.",
     "Medication for what it feeds.",
     "And everyday habits, around stress and sleep."),

    ("None of that erases it.",
     "It can still shrink the impact."),

    ("Save this before you repeat the myth.",),
]

# One float per sentence. The load-bearing ones: 0.90 after the checklist
# sentence, so the crosses finish drawing and hold a beat before the causes
# list starts; 0.65 after "There is no single cure", because the reversal
# that follows needs the silence to reverse into.
GAPS = [0.60,
        0.34, 0.90, 0.55, 0.85,
        0.65, 0.34,
        0.60, 0.60, 0.55]

SHOTS = [
    # The same face the long form opens on, so the pair reads as one piece.
    Shot(clip=FACE1 / "6068300.mp4"),

    Shot(clip=TEMPLES / "4588472.mp4"),

    # **Not `flow=True`.** The narration never says these are wrong until
    # the fourth chunk ("Turns out, none of that is true"); marking each one
    # false the instant it is spoken would answer the question before the
    # voice asks it. Two-phase (the default) shows all three unmarked, then
    # lands the crosses together in the pause after the last one - which is
    # exactly where "Turns out, none of that is true" is spoken.
    Shot(graphic="checklist",
         payload=([("Only loud noise causes it", False),
                   ("It always goes away on its own", False),
                   ("There is nothing you can do", False)],
                  "STILL FALSE")),

    Shot(clip=DESK / "3585311.mp4", clip_at=8.0, clip_ax=0.62),

    Shot(clip=BED / "7280521.mp4", clip_ax=0.55),

    Shot(clip=NEURONS / "29184317.mp4"),

    # "Real ways to manage it" - so show somebody using one.
    Shot(clip=LISTEN / "7948198.mp4"),

    Shot(graphic="steps",
         payload=([("Hearing aids", "🦻"),
                   ("Sound therapy", "🌊"),
                   ("Talking therapy", "💬"),
                   ("Medication for what it feeds", "💊"),
                   ("Everyday habits", "🌙")],
                  "REAL OPTIONS")),

    Shot(clip=MEDITATE / "6447702.mp4", clip_at=2.0, clip_ax=0.95),

    # The same face the long form closes on.
    Shot(clip=FACE2 / "6415877.mp4", clip_at=6.0),
]


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-myths-short.mp4"
    work = Path.home() / "Desktop/.tinnitus-myths-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85)

    # Same headline as the long form from this post, so the pair reads as one.
    # `band="bottom"` because his face and the beanie sit in the upper
    # two-thirds of every crop of this source; `ax=0.70` keeps him in frame
    # (the vertical crop is width-constrained on a landscape source, so most
    # of the leftover falls on the horizontal axis).
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "What tinnitus [myths] get wrong", image=THUMB_PHOTO, accent="red",
        ax=0.70, zoom=1.0, band="bottom")

    # A Short needs a 16:9 thumbnail too, for YouTube - it letterboxes a 9:16
    # upload otherwise. Same source, same headline. **No `side` override
    # here** - passing one fights the auto-scorer's own crop rather than
    # just picking a text side, since the scorer repositions the subject
    # within the frame rather than slicing the raw photo in half. Letting it
    # choose is what produced the clean landscape thumbnail in the first
    # place; forcing `side="right"` put the type across his face.
    yt = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), TINNITUS,
        "What tinnitus [myths] get wrong", image=THUMB_PHOTO, accent="red")

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Reel cover (Instagram, Facebook)")
    print(f"{yt}   <- YouTube thumbnail")


if __name__ == "__main__":
    main()
