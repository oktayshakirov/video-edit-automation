"""Does magnesium help tinnitus? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/does-magnesium-help-tinnitus.mdx

**Why this post.** "Does magnesium help tinnitus" is a high-volume evergreen
search and the honest answer is counterintuitive: nobody knows, and the single
placebo-controlled trial people cite tested magnesium *combined* with vitamins
and a plant extract, so it cannot tell you what the magnesium did. The arc:
replace "does it work" with "are you short of it", show what the research
actually found, explain why the idea is plausible anyway, put the real numbers
on food, and hand over a four-week self-test with the interaction warnings
attached. The close routes to a professional and echoes the food beat.

**Beats, chosen before the script.** The last three tinnitus long forms ran
grid + compare in every one of them (`brown-noise` grid/compare/gauge/diagram,
`myths` grid/compare/steps/quote/checklist, `pulsatile` compare/stat/grid/
checklist/steps), so this set drops both:

- `quote` - the article's own honest answer, set large, where the research
  section lands.
- `diagram` - the plausibility mechanism: magnesium low, the calcium gate
  opens wider, hearing nerve cells fire harder, a phantom sound gets
  amplified. A causal chain, four nodes, no loop. The one shape shared with
  the previous video, and it is the only beat in the library that draws
  *therefore* rather than *next*.
- `bars` - milligrams of magnesium in one ordinary serving against a day's
  worth. `bars` is the under-used beat this doc keeps pointing at (9 uses
  against checklist's 32) and a proportion is the one thing narration cannot
  say. Whole set scaled by 0.90 so the top row's value text stays on frame.
- `steps` - the article's four-week self-test, which has a real order.

Four distinct silhouettes: a set quotation, boxes and arrows, a row of bars, a
numbered track.

**The medical line.** Every claim is the article's own. The mechanism section
says out loud that a plausible mechanism is not evidence. Nothing here
promises relief: magnesium is described as possibly worth correcting if you
are short of it, never as something that will change your tinnitus. The
interactions (antibiotics, thyroid medication, reduced kidney function) and
the red flags are on screen as `payload` statements, per the project doc's
"put the red flags on screen". The disclaimer rides in `Meta.credits`.

**Footage.** Fetched fresh for this cut - none of these folders appears in any
other project file, checked by grep before the shot list was written. The
site's own two images are unusable: `does-magnesium-help-tinnitus.jpg` is
800x533 at L206 and `healthy-diet.jpg` 600x400 at L134, both far past the L82
ceiling for a site photograph and both too small for a 1920 frame. Every clip
was screened with `stock.screen` at four timestamps *and* looked at on a
contact sheet, which is how the CBD-oil bottles, the Jim Beam bottle and the
yellow capsules on green baize were caught - all three screened acceptably and
none of them belongs in this video. Trailing comment is the luma range.

**Phonemes.** `tinnitus` -> `tˈɪnɪɾəs`. `magnesium`, `glycinate`, `elemental`,
`antibiotics` and `milligrams` all phonemize cleanly. No initialisms are
spoken: "talking therapy" not the three letters, "an ear specialist" not the
three letters. "NMDA" is never said or written - the narration calls it the
calcium gate, which is what it means to this audience.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/does-magnesium-help-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "does-magnesium-help-tinnitus"

# Screened at 0.5/3/6/9s and looked at frame by frame. Trailing comment is the
# luma range and what is actually in the shot, because the folder name is the
# search query and several of these queries lied outright.
BED_W = STOCK / "videos/woman-searching-phone-in-bed-at-night-dark"          # 7986748 13s L26-38 - woman under a duvet, phone lighting her face
BED_M = STOCK / "videos/man-reading-phone-screen-night-bedroom-dark"         # 7988270 12s L20-30 - man awake in bed with a phone
GLASSES_M = STOCK / "videos/man-reading-phone-screen-night-bedroom-dark"     # 8212368 12s L9-10 - man in glasses reading a phone, dark room
SOFA_W = STOCK / "videos/person-sitting-on-sofa-at-night-dark-apartment"     # 6346221 11s L37-39 - woman lit by a laptop, pensive
QUIET = STOCK / "videos/person-sitting-on-sofa-at-night-dark-apartment"      # 7569777 11s L15-23 - figure in a blue-lit room, very dark
THINK_M = STOCK / "videos/man-shrugging-uncertain-dark-studio-portrait"      # 6415592 30s L18-20 - hand on chin, black ground
DOUBT_M = STOCK / "videos/man-shrugging-uncertain-dark-studio-portrait"      # 4588478 10s L32 - sceptical face, grey ground
LAPTOP_M = STOCK / "videos/scrolling-forum-posts-laptop-screen-dark-night"   # 8311535 24s L10-28 - man at a laptop at night
PAPERS = STOCK / "videos/research-papers-desk-lamp-night-dark"               # 30117914 14s L50-53 - hands over printed papers
WRITE_M = STOCK / "videos/research-papers-desk-lamp-night-dark"              # 7062990 14s L22-23 - man writing in a notebook at night
JOURNAL = STOCK / "videos/person-writing-journal-at-night-lamp"              # 8631662 13s L42-45 - hands writing under a lamp, glass of water
CAPSULES = STOCK / "videos/vitamin-supplement-moody-low-key-product-shot"    # 3752510 17s L24-41 - amber softgels, macro, warm on dark
BOTTLE = STOCK / "videos/pills-medication-bottle-dark"                       # 9510262 5s L40 - brown bottle, one tablet above it
LENTILS = STOCK / "videos/black-beans-bowl-dark-moody"                       # 20598195 8s L24-25 - bowl of pulses on black, plum rim light
CHOC = STOCK / "videos/dark-chocolate-macro-dark"                            # 4061791 26s L43-49 - dark chocolate, warm brown
GREENS = STOCK / "videos/spinach-cooking-pan-dark-kitchen"                   # 6975442 15s L38 at 12s - hands, greens and fruit in a bowl
PENSIVE_W = STOCK / "videos/woman-thinking-quietly-dark-room-evening-portrait"  # 9808085 24s L43-45 - woman resting her chin, warm lamp
DUSK_W = STOCK / "videos/woman-thinking-quietly-dark-room-evening-portrait"    # 5114840 11s L17-18 - woman outdoors at dusk, very dark
GLASSES_W = STOCK / "videos/woman-thinking-quietly-dark-room-evening-portrait"  # 39425737 17s L39-47 - woman in glasses, close, warm
OIL = STOCK / "videos/hands-preparing-food-dark-kitchen-night"               # 26620441 8s L21-32 - hands pouring oil into a pan
NEURON = STOCK / "videos/neuron-electrical-signal-dark-blue-animation"       # 34914524 10s L10-39 - magenta nerve cells firing
NEURON2 = STOCK / "videos/neuron-electrical-signal-dark-blue-animation"      # 34913408 10s L12-20 - teal nerve cells, sparser
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

# A hand holding two amber softgels against near-black, 4160x6240, L31/S18 -
# fetched portrait so the Short's cover keeps the subject's long axis, and
# cropped by hand for the 16:9. Shared with the Short, per the pair rule.
THUMB_PHOTO = (STOCK / "photos"
               / "magnesium-supplement-capsules-dark-portrait"
               / "31555271.jpg")

VOICE = "mia"                       # the explainer default, per the project doc
MUSIC = music.track("night-drift")  # the prepared track, shared with the Short

URL = "https://tinnitushelp.me/blog/does-magnesium-help-tinnitus"


SECTIONS = [
    # --- hook: the subject noun in sentence one, the payoff in sentence two --
    Section(
        title="The most recommended supplement",
        card=False,
        sentences=[
            ("Magnesium is the supplement people recommend most for tinnitus.",),
            ("There is one placebo-controlled trial behind that reputation,",
             "and magnesium was not the only ingredient in the pill they "
             "tested."),
            ("So the useful question is not whether magnesium treats your "
             "tinnitus.",),
            ("It is whether you are short of it in the first place.",),
            ("By the end you will know what the research actually found,",
             "how much magnesium is in ordinary food,",
             "and how to test it on yourself in four weeks."),
        ],
        shots=[
            # Opens on motion, and on the same face the Short opens on -
            # somebody looking this up in bed at one in the morning.
            Shot(clip=BED_W / "7986748.mp4", clip_at=4.0),
            Shot(clip=PAPERS / "30117914.mp4"),
            Shot(clip=THINK_M / "6415592.mp4", clip_at=2.0),
            None,  # hold the face through the reversal
            Shot(clip=CAPSULES / "3752510.mp4", clip_at=2.0,
                 payload=("", "DOES MAGNESIUM HELP TINNITUS?")),
        ],
        gaps=[0.55, 0.70, 0.55, 0.85, 0.80],
    ),

    # --- what the evidence is, so `quote` ---------------------------------
    Section(
        title="What does the research actually show?",
        spoken_title="So what does the research actually show?",
        sentences=[
            ("Two findings, and they pull in opposite directions.",),
            ("Some small studies have found lower magnesium levels in people "
             "with tinnitus.",
             "Others found no difference at all."),
            ("The one placebo-controlled trial did report less tinnitus "
             "handicap over three months.",
             "But it tested magnesium combined with vitamins and a plant "
             "extract,",
             "so nobody can say which part of that pill did the work."),
            ("Which leaves the article's own answer.",),
            # quote - one caption chunk, the whole line.
            ("The honest answer is that nobody knows yet.",),
            ("No health body recommends magnesium as a tinnitus treatment.",
             "Not one."),
        ],
        shots=[
            Shot(clip=DOUBT_M / "4588478.mp4", clip_at=2.0),
            Shot(clip=GLASSES_W / "39425737.mp4"),
            Shot(clip=LAPTOP_M / "8311535.mp4", clip_at=4.0),
            Shot(clip=SOFA_W / "6346221.mp4"),
            Shot(graphic="quote",
                 payload=("The honest answer is that nobody knows yet.",
                          "on whether magnesium helps tinnitus")),
            Shot(clip=WRITE_M / "7062990.mp4"),
        ],
        gaps=[0.60, 0.60, 0.55, 0.70, 1.20, 0.85],
    ),

    # --- why it is plausible anyway, so `diagram` -------------------------
    Section(
        title="So why does it keep coming up?",
        spoken_title="So why does the idea keep coming up?",
        sentences=[
            ("Because the biology behind it is genuinely reasonable.",),
            ("Magnesium sits in the doorway of a gate that lets calcium into "
             "nerve cells.",),
            # diagram - four nodes, one caption chunk each, no loop.
            ("When magnesium runs low, that gate opens more easily.",
             "More calcium moves into the hearing nerve cells.",
             "Those cells fire harder than they should.",
             "And a brain that is already generating a phantom sound has more "
             "to amplify."),
            ("Magnesium also supports blood flow in the inner ear.",),
            ("That is a good story.",),
            ("A good story is not evidence,",
             "and the gap between the two is where this whole topic lives."),
        ],
        shots=[
            Shot(clip=NEURON2 / "34913408.mp4"),
            Shot(clip=NEURON / "34914524.mp4"),
            Shot(graphic="diagram",
                 payload=([("Magnesium runs low", None, "\U0001F53B"),
                           ("The calcium gate opens wider", None,
                            "\U0001F6AA"),
                           ("Hearing nerve cells fire harder", None,
                            "\U000026A1"),
                           ("There is more phantom sound to amplify", None,
                            "\U0001F50A")],
                          "WHY THE IDEA IS PLAUSIBLE", False)),
            Shot(clip=QUIET / "7569777.mp4"),
            Shot(clip=BED_W / "7986748.mp4", clip_at=8.0),
            Shot(clip=GLASSES_M / "8212368.mp4"),
        ],
        gaps=[0.55, 0.60, 0.45, 0.60, 0.90, 0.85],
    ),

    # --- the numbers that are actually knowable, so `bars` ----------------
    Section(
        title="Can you just eat it?",
        spoken_title="So can you just eat it?",
        sentences=[
            ("Usually, yes, and this is the part that gets skipped.",),
            ("Most people who are genuinely low on magnesium are low because "
             "of what is on their plate.",),
            # bars - one caption chunk per row, five rows. The whole set is
            # scaled by 0.90 so the top row's value text stays on frame; the
            # proportions between rows are exact.
            ("A day's magnesium for an adult is roughly four hundred "
             "milligrams.",
             "An ounce of pumpkin seeds carries about a hundred and fifty six.",
             "A cup of black beans, a hundred and twenty.",
             "An ounce of almonds, eighty.",
             "An ounce of dark chocolate, sixty five."),
            ("None of that is exotic.",
             "Seeds, beans, nuts, leafy greens, wholegrains and dark "
             "chocolate."),
            ("Food is also much harder to overdo than a high-dose tablet.",),
        ],
        shots=[
            Shot(clip=GREENS / "6975442.mp4", clip_at=10.0),
            Shot(clip=JOURNAL / "8631662.mp4"),
            Shot(graphic="bars",
                 payload=([("A day's magnesium", 0.90, "400 mg"),
                           ("Pumpkin seeds, one ounce", 0.35, "156 mg"),
                           ("Black beans, one cup", 0.27, "120 mg"),
                           ("Almonds, one ounce", 0.18, "80 mg"),
                           ("Dark chocolate, one ounce", 0.15, "65 mg")],
                          "MAGNESIUM IN ONE SERVING")),
            Shot(clip=LENTILS / "20598195.mp4"),
            Shot(clip=CHOC / "4061791.mp4", clip_at=6.0),
        ],
        gaps=[0.55, 0.65, 0.45, 0.70, 0.85],
    ),

    # --- how to test it honestly, so `steps` ------------------------------
    Section(
        title="How would you test it on yourself?",
        spoken_title="So how would you test it on yourself?",
        sentences=[
            ("Check with a pharmacist or a doctor first, and that is not a "
             "formality.",),
            ("Magnesium can block the absorption of some antibiotics and of "
             "thyroid medication,",
             "and it needs real care if your kidneys are not working well."),
            ("If you get the go-ahead, run it as an experiment rather than as "
             "a habit.",),
            # steps - one caption chunk per node, five nodes.
            ("Week zero, log your tinnitus for seven days while you change "
             "nothing.",
             "Week one, start low, in the evening.",
             "Weeks two and three, hold every other routine steady.",
             "Week four, compare the log against your baseline.",
             "Then keep it or drop it, on what you wrote down."),
            ("Two things to check on the label.",),
            ("Read the elemental magnesium, not the weight of the whole "
             "compound.",),
            ("Glycinate is the gentlest on the stomach.",
             "Oxide is the cheapest, and the least absorbed."),
            ("And if it loosens your bowels, the dose is too high.",),
        ],
        shots=[
            Shot(clip=BOTTLE / "9510262.mp4",
                 payload=("CHECK FIRST",
                          "Magnesium interacts with some antibiotics, "
                          "bisphosphonates and thyroid medication.")),
            Shot(clip=LAPTOP_M / "8311535.mp4", clip_at=14.0),
            Shot(clip=WRITE_M / "7062990.mp4", clip_at=6.0),
            Shot(graphic="steps",
                 payload=([("Log a week with no magnesium", "\U0001F4D3"),
                           ("Start low, in the evening", "\U0001F319"),
                           ("Change nothing else", "\U00002696\U0000FE0F"),
                           ("Compare with your baseline", "\U0001F4CA"),
                           ("Keep it or drop it", "\U00002705")],
                          "A FOUR-WEEK SELF-TEST")),
            Shot(clip=CAPSULES / "3752510.mp4", clip_at=10.0),
            Shot(clip=JOURNAL / "8631662.mp4", clip_at=7.0),
            Shot(clip=OIL / "26620441.mp4"),
            Shot(clip=BED_M / "7988270.mp4"),
        ],
        gaps=[0.55, 0.65, 0.70, 0.45, 0.60, 0.55, 0.55, 0.85],
    ),

    # --- close: echo the food beat, route to a professional ---------------
    Section(
        title="So is it worth trying?",
        spoken_title="So is it worth trying?",
        sentences=[
            ("Magnesium is not a treatment for tinnitus, and nobody is "
             "claiming it is.",),
            ("What it can be is one variable you have settled.",),
            ("If your diet has been thin on magnesium, that is worth "
             "correcting anyway.",),
            ("The things with the strongest evidence behind them are slower, "
             "and much less exciting.",),
            ("Sound therapy, sleep, and talking therapy.",),
            ("And some tinnitus needs a person, not a supplement.",),
            ("If yours is new, one-sided, or pulsing with your heartbeat,",
             "or it comes with dizziness or hearing loss,"),
            ("see a doctor or an ear specialist.",),
            ("So before you buy anything:",
             "when did you last eat something off that list?"),
        ],
        shots=[
            Shot(clip=PENSIVE_W / "9808085.mp4", clip_at=2.0),
            Shot(clip=DUSK_W / "5114840.mp4"),
            Shot(clip=GLASSES_W / "39425737.mp4", clip_at=2.0),
            Shot(clip=BED_M / "7988270.mp4", clip_at=6.0),
            Shot(clip=PENSIVE_W / "9808085.mp4", clip_at=16.0),
            Shot(clip=GLASSES_M / "8212368.mp4", clip_at=4.0),
            Shot(clip=QUIET / "7569777.mp4", clip_at=2.0,
                 payload=("SEE SOMEONE IF",
                          "It is new, one-sided, pulsing with your heartbeat, "
                          "getting worse, or comes with dizziness or hearing "
                          "loss.")),
            Shot(clip=THINK_M / "6415592.mp4", clip_at=22.0),
            Shot(clip=CHOC / "4061791.mp4", clip_at=18.0),
        ],
        gaps=[0.80, 0.55, 0.70, 0.55, 0.85, 0.80, 0.55, 0.70, 2.40],
    ),
]

META = Meta(
    title="Does Magnesium Help Tinnitus?",
    hook="Nobody knows yet - and the single placebo-controlled trial people "
         "cite tested magnesium mixed with vitamins and a plant extract, so "
         "it cannot tell you what the magnesium did. Here is what the "
         "research found, how much is in ordinary food, and how to test it "
         "on yourself in four weeks.",
    url=URL,
    summary="What the studies on magnesium and tinnitus actually found, why "
            "the mechanism is plausible but not evidence, how many "
            "milligrams are in a normal serving of seeds, beans, nuts and "
            "dark chocolate, the interactions to check before you start, and "
            "a four-week self-test with a baseline.",
    tags=["tinnitus", "does magnesium help tinnitus", "magnesium tinnitus",
          "magnesium for ringing in ears", "magnesium glycinate",
          "tinnitus supplements", "tinnitus research", "ringing in ears"],
    cta=f"Full article, the dose notes and the sources: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: licensed for this channel.",
             "",
             "This video is general information, not medical advice. Talk to "
             "a pharmacist or doctor before starting any supplement, "
             "especially if you take other medication or have reduced kidney "
             "function. If your tinnitus is new, one-sided, pulsing with your "
             "heartbeat, worsening, or comes with dizziness or hearing loss, "
             "see a doctor or an ear specialist."],
)


def main() -> None:
    out = Path.home() / "Desktop/does-magnesium-help-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.magnesium-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, music_gain=1.0, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        keep_work=True,
        # The title's own question, accent on the word carrying the tension,
        # question mark inside the plate. The source is portrait and shared
        # with the Short, so the 16:9 takes a hand-placed crop rather than
        # letting the scorer find "empty" space in a 4160x6240 frame - the
        # automatic one landed on a shoulder and cropped the capsules out
        # entirely. 0.74 of the vertical slack centres the band on the open
        # palm and leaves the left third as real black for the type.
        thumb_headline="Does magnesium help [tinnitus?]",
        thumb_image=THUMB_PHOTO,
        thumb_accent="orange",
        thumb_crop_at=(0.5, 0.74),
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
