"""Tinnitus myths vs reality — long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tinnitus-myths-vs-reality.mdx.

**Why this post.** It is the one page on the site built entirely out of
compare pairs — eight myth/reality splits — which makes it the natural home
for `compare` with `name_columns=True`. Five of the article's eight myths
carry the video; the other three (location, sound variety, ear wax) are
folded into one rapid `checklist` round rather than given a section each.

**Beat variety, chosen before the script was written**, per the crypto
skill's silhouette rule: `grid` (other causes), `compare` (temporary vs
chronic), `steps` (the five management options), `quote` (it is not minor),
`checklist` (the last three myths, busted). No two carded sections share an
outline.

**The medical line.** Nothing here promises relief or a cure. Myth three is
explicit that there is no universal cure and describes the five approaches as
what the article calls them — ways to manage and reduce impact. The close
routes to a professional and puts the article's own red flags on screen as a
statement card.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tinnitus-myths-vs-reality.py

--- what the second cut changed, and why -------------------------------------

**The subject is named in the first sentence now.** The first cut opened on
"You have probably heard at least one of these" and did not say the word
*tinnitus* until the chapter card at 0:14 — so for fourteen seconds the video
was about nothing in particular, which is the worst possible use of the span
where retention falls fastest. The chapter titles had the same fault: "Myth:
only loud noise causes it" never says what *it* is. Every card is now a
question that names its subject.

**Music is `night-drift`, not the `bright` preset.** The generated presets are
retired on this channel; the prepared track is the one both sites use.

**Clip repetition was the loudest note on the first cut.** One clip
(`stressed-man.../6415592`) played three times, twice for over fourteen
seconds, and two more were doubled. The rule this cut works to: **no clip
plays twice within a minute of itself, no clip holds longer than about eight
seconds, and a slot's footage has to be about the line it sits under.** The
long holds were not really clip problems — they were single sentences with
four or five chunks carrying one picture, so the fix was splitting the
sentence as much as swapping the clip.

**Four clips were rejected after being watched rather than measured.**
`man-serious-portrait.../6415611` and `6415877` screened perfectly at L15 and
are the *same man in the same studio* as the clip already over-used — adjacent
Pexels ids are the same shoot, which the luma box cannot see.
`doctor-night-shift-dark-hospital-corridor` screened at L37 and is a bald
child in a hospital gown in a wheelchair, which reads as a children's cancer
ward. `man-talking-to-camera-dark-room-interview/7230790` has a handgun on the
table. All four would have shipped on the numbers alone.

**Icons on the drawn beats.** `grid` and `steps` take an emoji per item now —
the skill's long-standing open request. A five-node track of bare labels was
"a list of words"; the same track with an icon in each node reads at a glance.

**Phonemes.** No initialisms are spoken — "cognitive behavioral therapy" is
said in full and never reduced to letters.

**Pictures.** The site's images for this topic are all bright (screened:
tinnitus-myths-reality.jpg L178, young-tinnitus.jpg L172,
stress-tinnitus-man.jpg L186) so none can take a full-frame slot at
`max_upscale=1.90`. They go in beat `picture=` columns, where the same file is
a downscale at 660px.

--- what the third cut changed, and why ---------------------------------------

**The background is a new generation, not a new asset.** `tinnitus-plum`'s
three small blobs (`sigma` 0.26-0.36) each read as a distinct "cloud" with a
visible edge where it faded into the next — the user's note, "we can see
where each color starts and ends" — worst behind an empty `compare` or
`chapter` card, where nothing else on screen competes for attention. Replaced
with two blobs at `sigma` 0.62/0.70, wide enough that their falloff mostly
sits outside the visible frame in every direction, so they overlap into one
continuous field with no seam. The vignette that darkens the corners was
*also* part of the fault — its old `0.55 * clip(r2*2.4, 0, 1)` saturated at
r ~= 0.645 from centre, so the ring where it stops changing butted up against
the still-changing centre and read as an edge of its own. Both are fixed in
`core/backdrop.py`; same base colour, same brand.

**Myth cards now carry a number.** `Section.number` draws a big numeral above
the card's rule, only on the four sections that are actually part of the
count the narration says out loud ("myth one", "myth two"...). This is not
the numbered-agenda pattern `ChapterCard`'s own docstring warns against — an
agenda numbers chapters the viewer never asked to count; this numbers the
thing the video is about, matching a word the narration says at that exact
moment.

**Two more clips replaced, both irrelevant to their line.**
`hand-adjusting-phone-volume-dark/17643375` turned out to be someone editing
a black-and-white forest photo in a Portuguese camera app — used twice, under
"worth getting checked" and under "a professional opinion", and relevant to
neither. Replaced with a woman looking at a laptop (research, concern) and a
man on a phone call (an actual professional opinion, by phone).

**Neither hook face survives.** `woman-portrait-low-key.../4587160` (the
opener) was called out as reading as too culturally specific for a general
myths video; `.../7298368` (the closing bookend) was flagged for visible skin
texture in its tight close-up. Both are swapped for two new faces, still used
as an open/close bookend pair.

**The karaoke caption lag is fixed at the source, not reverted.**
`_karaoke_sprites` was apportioning each word's on-screen window across a
caption's *displayed* span, which the hold-until-next rule stretches to the
start of the next caption — so on a short sentence with a long following
pause, every word lit late, worst on the final one or two. `Caption` now
carries `speech_end`, the true pre-stretch boundary captured once at
creation, and word timing is apportioned against that instead. This is a
long-form-adjacent fix (the engine is shared) even though captions are not
burned here.

--- what the fourth cut changed, and why --------------------------------------

**The two new hook faces were themselves a repeat of the fault they replaced.**
Both landed as Black actors, and with `TEMPLES` — also Black — as the very
next shot, the hook opened on three Black faces in a row. That was never a
deliberate choice on either pass; it was a side effect of screening stock
purely on `luma`, which structurally favours darker skin against a dark
background (a pale face reads brighter against the same backdrop and gets
rejected by the box more often). **Casting still has to be looked at, not
just measured** — the same lesson the "watch a clip, don't just screen it"
rule already carries, applied to who is in the shot rather than what they are
doing in it.

The replacements are `young-woman-portrait-dark-moody.../6068300` and
`man-serious-portrait-dark-studio.../6415877` — the second is from the same
shoot flagged as "already over-used" on the *second* cut, and reusing one of
its clips is correct now rather than contradictory: that shoot was rejected
for repetition, and by the fourth cut it was not used anywhere in this video
at all, so a single use is not a repeat of anything.

**The third hook shot is an abstract now, not a third face.** Two people back
to back was already the practical ceiling; `TEMPLES` there made it three, and
the fix is not a different face, it is no face — `NEURONS` carries the title
stamp instead, which also means the hook's first three shots are no longer
three near-identical "portrait against dark studio" setups back to back.

**The thumbnail changed again**, to a stronger single-subject portrait — a
direct, engaging gaze with real copy space rather than someone looking away
from camera. See `main()` for the source and why the scorer's own "busiest
region" warning here is fine to override.
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

# Screened with `stock.screen` across each clip's length, then **watched** —
# the trailing comment is the luma/saturation range. The letter is the slot
# label used in the shot plan in this file's docstring.
FACE1 = STOCK / "videos/young-woman-portrait-dark-moody-looking-away"  # L21 S11
FACE2 = STOCK / "videos/man-serious-portrait-dark-studio-black-background"  # L14-17
TEMPLES = STOCK / "videos/tired-man-rubbing-temples-dark"           # L37 S16
AWAKE = STOCK / "videos/person-waking-up-night-bedroom-dark"        # L23-29
LAPTOP = STOCK / "videos/woman-looking-at-laptop-screen-dark-serious"
CALL = STOCK / "videos/man-on-phone-call-dark-room-serious"         # L31 S7
MEDITATE = STOCK / "videos/man-meditating-dark-room-calm"           # L41 S6
WINDOWS = STOCK / "videos/woman-looking-out-window-dark-room-night"  # L13 S10
CONCERT = STOCK / "videos/concert-crowd-night-stage-lights"         # L20-42
NEURONS = STOCK / "videos/brain-neurons-abstract-dark"              # L26 S46
LIBRARY = STOCK / "videos/quiet-library-reading-dark"               # L36-44
ALONE = STOCK / "videos/man-sitting-alone-dark-apartment-night"     # L30-35
LISTEN = STOCK / "videos/man-listening-music-dark-room-night"       # L42 S8
DESK = STOCK / "videos/man-thinking-dark-room-window-night"         # L36-37 S13
BED = STOCK / "videos/person-sitting-on-bed-dark-bedroom-night-thinking"
WAVE = STOCK / "videos/sound-wave-visualization-dark"               # L7 S2
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"
# **The prepared track, not a generated preset.** `bright` is retired here.
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/tinnitus-myths-vs-reality"
A = 16 / 9


SECTIONS = [
    # --- hook: name the subject in sentence one --------------------------
    Section(
        title="What you have heard",
        card=False,
        sentences=[
            ("Almost everything you have been told about tinnitus",
             "is only half right."),
            ("Loud noise causes it.",
             "It goes away on its own.",
             "And there is nothing you can do about it."),
            ("One of those is partly true.",
             "The other two are just wrong."),
            ("So here is what the evidence actually says,",
             "myth by myth."),
        ],
        shots=[
            # A face, moving, on frame one. Distinct from every other person
            # in the cut, and dark enough to need no grading.
            Shot(clip=FACE1 / "6068300.mp4"),             # L21 S11
            Shot(clip=FACE2 / "6415877.mp4"),             # L14 S6
            # **Not a third face closeup in a row.** The first two hook shots
            # are already two people back to back; a third (the old build
            # used `TEMPLES` here) reads as a wall of faces. An abstract
            # carries the title stamp instead.
            Shot(clip=NEURONS / "34913063.mp4",
                 payload=("", "TINNITUS: MYTHS VS REALITY")),
            Shot(clip=NEURONS / "29184317.mp4"),
        ],
        gaps=[0.55, 0.60, 0.85, 0.45],
    ),

    # --- myth 1: only loud noise, so `grid` ------------------------------
    Section(
        title="Is loud noise the only cause?",
        spoken_title="So, myth one. Is loud noise the only thing "
                     "that causes tinnitus?",
        number=1,
        sentences=[
            ("A concert.",
             "A shooting range.",
             "Headphones turned up too high.",
             "That is the story almost everyone knows."),
            ("It is a real risk.",
             "But it is one cause among several."),
            ("Here is what else can set tinnitus off.",),
            ("An ear infection.",
             "Ordinary aging.",
             "Certain medications.",
             "Or a health condition, like high blood pressure "
             "or a jaw disorder."),
            ("So the loud noise story is not wrong.",
             "It is just not the whole story."),
        ],
        shots=[
            # A concert line gets a concert — the skill's own rule.
            Shot(clip=CONCERT / "13082773.mp4"),
            None,
            Shot(clip=DESK / "3585311.mp4", clip_at=8.0),
            Shot(graphic="grid",
                 payload=([("Ear infections",
                            "Inflammation, or a blocked signal", "🌡️"),
                           ("Ordinary aging",
                            "Wear on the hearing system", "⏳"),
                           ("Certain medications",
                            "Some antibiotics, and others", "💉"),
                           ("Underlying conditions",
                            "Blood pressure, thyroid, the jaw", "🫀")],
                          "OTHER CAUSES")),
            Shot(clip=ALONE / "36244102.mp4"),
        ],
        gaps=[0.34, 0.70, 0.34, 0.34, 0.60],
    ),

    # --- myth 2: always temporary, so `compare` --------------------------
    Section(
        title="Does tinnitus always go away on its own?",
        spoken_title="Myth two. Does tinnitus always go away on its own?",
        number=2,
        sentences=[
            ("Sometimes it does.",
             "A loud night out,",
             "then a day of quiet,",
             "and the ringing fades."),
            ("But for a lot of people, it does not work that way.",
             "Compare the two."),
            ("Take temporary tinnitus first.",
             "It follows one loud event.",
             "It settles within hours or days.",
             "And the hearing system recovers on its own.",
             "Now compare that with chronic tinnitus.",
             "It needs no single loud trigger.",
             "It can persist for months or years.",
             "And it is often tied to hearing loss "
             "or another underlying cause."),
            ("Either way,",
             "if it has been more than a few weeks,",
             "or it genuinely bothers you,",
             "that is worth getting checked."),
        ],
        shots=[
            Shot(clip=LIBRARY / "6549982.mp4"),
            None,
            Shot(graphic="compare",
                 payload=("Temporary tinnitus",
                          ["Follows one loud event",
                           "Settles within hours or days",
                           "Recovers on its own"],
                          "Chronic tinnitus",
                          ["No single loud trigger",
                           "Can persist for months or years",
                           "Often tied to hearing loss"],
                          True)),
            # "Worth getting checked" - a look-it-up moment, not a stranger's
            # photo library.
            Shot(clip=LAPTOP / "6346221.mp4"),
        ],
        gaps=[0.34, 0.70, 0.34, 0.55],
    ),

    # --- myth 3: no treatment, so `steps` --------------------------------
    Section(
        title="Is there really nothing you can do?",
        spoken_title="Myth three. Is there really nothing you can do?",
        number=3,
        sentences=[
            ("There is currently no single cure.",
             "That part of the myth is true."),
            ("But no cure is not the same as no options.",),
            ("Here is the actual playbook, and it is five approaches.",),
            ("Hearing aids, if hearing loss is part of the picture.",
             "Sound therapy, to make the tinnitus less noticeable.",
             "Cognitive behavioral therapy, for the distress around it.",
             "Medication, for the anxiety or the sleep it may be feeding.",
             "And everyday habits, around stress and sleep."),
            ("None of that erases it.",
             "All of it can shrink its impact."),
        ],
        shots=[
            Shot(clip=TEMPLES / "4588472.mp4", clip_at=5.0),
            # "No options" is the line — so show somebody using one.
            Shot(clip=LISTEN / "7948198.mp4"),
            Shot(clip=WAVE / "34645273.mp4"),
            Shot(graphic="steps",
                 payload=([("Hearing aids", "🦻"),
                           ("Sound therapy", "🌊"),
                           ("Talking therapy", "💬"),
                           ("Medication for what it feeds", "💊"),
                           ("Everyday habits", "🌙")],
                          "THE ACTUAL PLAYBOOK")),
            Shot(clip=MEDITATE / "6447702.mp4"),
        ],
        gaps=[0.85, 0.90, 0.34, 0.34, 0.60],
    ),

    # --- myth 4: not serious, so `quote` ----------------------------------
    Section(
        title="Is tinnitus really just annoying?",
        spoken_title="Myth four. Is tinnitus really just annoying?",
        number=4,
        sentences=[
            ("For some people, it barely registers.",),
            ("For a lot of others, it is not minor at all.",),
            ("It is not just a ringing in the ears.",),
            ("It can wreck a night of sleep,",
             "make it hard to concentrate,",
             "and wear down your mood, day after day."),
            ("Dismissing it does not make it smaller.",
             "It just delays taking it seriously."),
        ],
        shots=[
            Shot(clip=ALONE / "38136563.mp4"),
            None,
            Shot(graphic="quote",
                 payload=("It is not just a ringing in the ears.",
                          "on why tinnitus is taken seriously"),
                 picture=IMG / "stress-tinnitus-man.jpg"),
            # The line names sleep first, so the picture is somebody awake.
            Shot(clip=AWAKE / "11956220.mp4"),
            Shot(clip=DESK / "3585311.mp4", clip_at=16.0),
        ],
        gaps=[0.55, 0.85, 0.34, 0.60, 0.60],
    ),

    # --- three more myths, so `checklist` ---------------------------------
    Section(
        title="What else is not true?",
        spoken_title="And a few more, quickly. What else is not true?",
        sentences=[
            ("Three more claims worth clearing up.",),
            ("Only elderly people get it.",
             "It only ever affects one ear.",
             "And ear wax has nothing to do with it."),
            ("Tinnitus shows up in children and young adults too,",
             "it can sit in both ears or feel centered in the head,",
             "and a blocked ear canal can trigger or worsen it."),
        ],
        shots=[
            Shot(clip=BED / "7280521.mp4"),
            Shot(graphic="checklist",
                 payload=([("Only elderly people get it", False),
                           ("It only ever affects one ear", False),
                           ("Ear wax has nothing to do with it", False)],
                          "STILL FALSE",
                          True),                     # flow
                 # **Not `young-tinnitus.jpg`.** Its filename promises a young
                 # person with tinnitus; the actual photo is a bright
                 # classroom with a child in a VR headset (L172), which says
                 # nothing about age, ears or wax and was the brightest thing
                 # on screen. This one is a child and a parent in headphones
                 # at L71 — the subject the first myth on the list is about.
                 picture=IMG / "kid-and-dad-with-headphones.jpg"),
            None,
        ],
        gaps=[0.34, 0.90, 0.60],
    ),

    # --- close: route to a professional, then the echo --------------------
    Section(
        title="So where does that leave you?",
        sentences=[
            # **Split out of one five-chunk sentence.** As written the first
            # time this was a single span carrying one clip for 14.7 seconds,
            # which is the longest hold in the cut and was flagged as such.
            ("None of this replaces a professional opinion.",),
            ("See a doctor if it is new,",
             "if it will not settle,",
             "if it sits in one ear only,",
             "or if it comes with hearing loss or dizziness."),
            ("Getting it named is not overreacting.",
             "It is the fastest way to actually manage it."),
            ("So the next time someone tells you "
             "tinnitus only means one thing,",
             "you will know that is not how it works."),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            # "A professional opinion" - an actual phone call, not a stock
            # photo library.
            Shot(clip=CALL / "5281602.mp4"),
            # **The red flags on screen, which the medical rule requires.**
            # A statement card also gives this atmospheric shot the line the
            # skill says every atmosphere-only clip needs.
            Shot(clip=WINDOWS / "7292659.mp4",
                 payload=("SEE A DOCTOR IF",
                          "It is new, in one ear, or comes with "
                          "hearing loss.")),
            Shot(clip=MEDITATE / "6447702.mp4", clip_at=6.0),
            # The opening faces again, closing the loop they opened.
            Shot(clip=FACE1 / "6068300.mp4", clip_at=4.0),
            Shot(clip=FACE2 / "6415877.mp4", clip_at=4.0),
        ],
        gaps=[0.70, 0.60, 0.85, 0.34, 3.20],
    ),
]

META = Meta(
    title="Tinnitus Myths vs Reality: What Is Actually True?",
    hook="Only loud noise causes it. It always goes away. There is nothing "
         "you can do. Here is what the evidence actually says about the most "
         "common tinnitus myths.",
    url=URL,
    summary="The real causes beyond loud noise, why temporary and chronic "
            "tinnitus are not the same thing, the five real management "
            "options despite there being no single cure, why it is not "
            "minor for everyone, and three more myths about age, location "
            "and ear wax, busted.",
    tags=["tinnitus", "tinnitus myths", "tinnitus facts", "ringing in ears",
          "tinnitus causes", "tinnitus treatment"],
    cta=f"Full article and sources: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: night-drift.",
             "",
             "This video is general information, not medical advice. If "
             "your tinnitus is new, persistent, in one ear only, or comes "
             "with hearing loss or dizziness, see a doctor or audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-myths-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-myths-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # **The user's own pick, fetched by Pexels id (3958868) rather than a
        # search query.** Landscape 5760x3840, bright and pastel — the
        # opposite of every other thumbnail on this channel — but
        # `render_thumb`'s own scrim darkens the type's half regardless of
        # source brightness, so it composes cleanly with no renderer change.
        # Same image as the Short's thumbnail, per the standing pairing rule.
        thumb_headline="What tinnitus [myths] get wrong",
        thumb_image=STOCK / "photos" / "user-picked" / "3958868.jpg",
        thumb_accent="red",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
