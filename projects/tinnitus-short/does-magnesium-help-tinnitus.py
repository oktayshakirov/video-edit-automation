"""Does magnesium help tinnitus - ~45s vertical Short.

Source: tinnitus-blog/content/posts/does-magnesium-help-tinnitus.mdx, the same
post as the `does-magnesium-help-tinnitus` long form.

**It does not compress the long cut.** The long form walks the evidence, the
plausible mechanism, the milligrams in real food and a four-week self-test
across six chapters. What survives here is the single move a scroller has not
heard: the honest answer to "does it help" is that nobody knows, and the thing
that *is* knowable is on the label in front of them - magnesium oxide is the
cheapest and the least absorbed, and the number that matters is the elemental
magnesium, not the weight of the compound.

**One drawn beat, and it is not the long form's.** The long form runs quote,
diagram, bars and steps; this runs `checklist` with `flow=True`, because the
narration says each verdict as it lands ("Oxide? Cheap, and barely absorbed.")
and a cross held back four seconds would put the picture behind the voice.
The close is a `chapter` full-screen statement - a different silhouette, and
the strongest way a Short lands its last line.

**The opening question is the title question**, asked plainly over the same
face the long form opens on, and sentence 2 answers it flat rather than
hedging. "Maybe" at five seconds is where the caffeine Short lost half its
viewers.

**No medical claims.** Nothing here says magnesium will change anyone's
tinnitus - the whole point is that nobody knows. The forms are described by
absorption and stomach tolerance, which is what the article says about them.
It closes cold on a directive the video earned, with no question and no
disclaimer line (long-form only, per `narration.md`).

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/does-magnesium-help-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb, render_thumb
from video_automation.tinnitus.article import render_tinnitus_short

# Same roster as the long form from this post (a pair is one video), and every
# clip screened across its length and looked at on a contact sheet.
BED_W = STOCK / "videos/woman-searching-phone-in-bed-at-night-dark"          # 7986748 13s L26-38 - woman under a duvet, phone on her face
DOUBT_M = STOCK / "videos/man-shrugging-uncertain-dark-studio-portrait"      # 4588478 10s L32 - sceptical face
CAPSULES = STOCK / "videos/vitamin-supplement-moody-low-key-product-shot"    # 3752510 17s L24-41 - amber softgels, macro
BOTTLE = STOCK / "videos/pills-medication-bottle-dark"                       # 9510262 5s L40 - brown bottle, one tablet above it
LENTILS = STOCK / "videos/black-beans-bowl-dark-moody"                       # 20598195 8s L24-25 - bowl of pulses on black
PENSIVE_W = STOCK / "videos/woman-thinking-quietly-dark-room-evening-portrait"  # 9808085 24s L43-45 - woman resting her chin
GLASSES_W = STOCK / "videos/woman-thinking-quietly-dark-room-evening-portrait"  # 39425737 17s L39-47 - woman in glasses, close, reading

# A hand holding two amber softgels against near-black, fetched portrait so
# the cover keeps the subject's long axis. Shared with the long form.
THUMB_PHOTO = (STOCK / "photos"
               / "magnesium-supplement-capsules-dark-portrait"
               / "31555271.jpg")

VOICE = "mia"
MUSIC = music.track("night-drift")

SENTENCES = [
    # A Short has no title card - the first line is the title question, and
    # sentence 2 answers it instead of hedging.
    ("Does magnesium help tinnitus?",),

    ("Nobody knows yet.",),

    ("There is one placebo-controlled trial,",
     "and it tested magnesium mixed with vitamins and a plant extract,",
     "so it cannot tell you what the magnesium did."),

    ("But there is something on your label that is knowable.",),

    # A hinge sentence of its own, immediately before the beat, so it claims
    # no reveal slot.
    ("Not every form of magnesium absorbs the same way.",),

    # checklist, flow=True - the narration says each verdict as it lands.
    ("Oxide is the cheapest, and the least absorbed.",
     "Citrate absorbs better, and can loosen your bowels.",
     "Malate is somewhere in between.",
     "Glycinate is the gentlest on the stomach."),

    ("And read the elemental magnesium on the back,",
     "not the weight of the whole compound."),

    ("Or skip the bottle entirely.",
     "An ounce of pumpkin seeds carries about a hundred and fifty milligrams."),

    # chapter - full-screen statement, the payoff line.
    ("Which is the part nobody argues about.",),

    ("Check your label tonight.",),
]

# One float per sentence. Load-bearing: 0.70 after the question so the flat
# answer lands as an answer, 1.20 on the checklist's own sentence because
# `flow` marks each item on the word rather than in the pause, 0.90 before the
# full-screen line and 0.80 before the cold close.
GAPS = [0.70,
        0.80,
        0.55,
        0.70,
        0.55,
        1.20,
        0.60,
        0.70,
        0.90,
        0.80]

SHOTS = [
    # Opens on the same face the long form opens on - somebody looking this
    # up in bed at one in the morning.
    Shot(clip=BED_W / "7986748.mp4", clip_at=4.0),
    Shot(clip=DOUBT_M / "4588478.mp4", clip_at=2.0),
    Shot(clip=PENSIVE_W / "9808085.mp4", clip_at=2.0),
    Shot(clip=BOTTLE / "9510262.mp4"),
    Shot(clip=CAPSULES / "3752510.mp4", clip_at=2.0),
    Shot(graphic="checklist",
         payload=([("Oxide - cheapest, least absorbed", False),
                   ("Citrate - absorbs well, loosens", False),
                   ("Malate - somewhere in between", False),
                   ("Glycinate - gentlest on the stomach", True)],
                  "NOT ALL THE SAME",
                  True)),                       # flow
    Shot(clip=GLASSES_W / "39425737.mp4", clip_at=2.0),
    Shot(clip=LENTILS / "20598195.mp4"),
    Shot(graphic="chapter", payload=("THE FOOD IS NOT IN DOUBT.",)),
    Shot(clip=PENSIVE_W / "9808085.mp4", clip_at=16.0),
]


def main() -> None:
    out = Path.home() / "Desktop/does-magnesium-help-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.magnesium-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        keep_work=True)

    # The title's own question, accent on the word carrying the tension, the
    # question mark inside the plate. `ax=0.82` keeps the open palm and the
    # capsules in the 9:16 crop - centred, the hand is cut in half. `size` is
    # down from the 168 default because MAGNESIUM is one long word and at 168
    # the size search leaves it running off the right edge as "MAGNESIU".
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "Does magnesium help [tinnitus?]", image=THUMB_PHOTO,
        accent="orange", ax=0.82, band="top", size=145)

    yt = render_thumb(
        out.with_name(out.stem + "-thumb-yt.jpg"), TINNITUS,
        "Does magnesium help [tinnitus?]", image=THUMB_PHOTO,
        accent="orange", crop_at=(0.5, 0.74))

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Reel cover (Instagram, Facebook)")
    print(f"{yt}   <- YouTube thumbnail")


if __name__ == "__main__":
    main()
