"""Does stress make tinnitus worse? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/your-tinnitus-as-stressometer.mdx.

**Why this post, and what it is not.** `why-does-tinnitus-spike` already
explains stress turning the hearing system's gain up. This post's own move is
the next one: if the loudness moves with stress, it can be *read*. So the
spine here is the meter and the log - give it a number, write down what was
happening, look back for the pattern, and change the reaction rather than
fight the sound. The fight-or-flight mechanism gets one section, drawn as a
loop, and no more.

**The title is the search.** "Does stress make tinnitus worse" is what
somebody types; it sits beside the channel's caffeine and silence titles.
The Short takes a different query ("why is my tinnitus louder some days").

**The opening is the article's own example log.** Its sample entries read 8
at 2:30 PM (a deadline, an argument with a colleague) and 4 at 7:00 PM (a
quiet evening, reading after a short walk). Sentence one is that number, so
the first five seconds carry a fact rather than a mood (`longform.md`, "The
first five seconds carry information"). `Split` puts the two readings on
screen, no winner: the question it leaves open is the video.

**The beats, and why these.** The last three scripts ran
`callout`/`quote`/`diagram`/`checklist`/`grid` (celebrities),
`stat`/`bars`/`gauge`/`chapter`/`grid` (musicians) and
`anatomy`/`checklist`/`chapter`/`steps`/`grid` (tmj). No `grid` for the first
time in five videos:

- `dial` - the stress meter itself, 0 to 10. This is the noun of the title,
  and stock has no picture of it. Built for fear-greed at 0-100; `top=10` was
  added for this video so the arc reads 0 / 5 / 10 and the readout "8".
- `diagram(loop=True)` - the alarm that keeps itself on: on alert, ringing
  seems louder, that feels like a threat, the threat keeps the alarm on. The
  article's own "if tinnitus itself feels threatening, it can keep this alarm
  blaring". A list would end; this does not.
- `bars` - the article's three sample log entries, verbatim, against one
  0-10 scale. Titled as an example, because that is what they are.
- `compare` - reacting against reading, the article's "mindful awareness"
  section. `name_columns=True`, so each heading arrives as it is said.
- `steps` - a routine with an order: note it, breathe, release, step away.
  All four come from the article's quick techniques.

**The pictures are the act.** Every clip is a hand, an object, a meter, a
walk, a window - the one face that breathes is under the one line about
breathing. The cache had nothing unused, so the whole roster is a fresh fetch;
verdicts are in `docs/video/footage.md`.

**The medical line.** Nothing here says a technique quietens tinnitus. The
article's "outcome" column ("tinnitus faded into the background") is left out
on purpose: it is a relief claim. What a breath or a walk does is described
as what it does to *stress*. Talking therapy is described as what it is built
around, not what it achieves. The red flags are the article's own (severe,
persistently distressing, changes suddenly, with hearing loss, dizziness or
pain), said and put on screen. Its speculative line about cortisol wearing
down hair cells is not used - it is the article's least certain claim and the
most frightening one.

**Phonemes**, checked with espeak-ng: cortisol, adrenaline, audiologist,
dizziness all read correctly. "Read" only ever appears in the present tense
("it reads four", "read it"), because espeak reads every "read" as /ri:d/.
"CBT" is "talking therapy" (`projects/tinnitus.md`).

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/your-tinnitus-as-stressometer.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Split

SOURCE_POST = "your-tinnitus-as-stressometer"

# Fetched 2026-10-12, contact-sheeted at 5/35/65/95% of each clip. None of
# these ids is cut by another project (`grep -rl <id> projects/`). Duration,
# then luma, then what is actually in the frame.
TYPE = STOCK / "videos/hands-typing-laptop-keyboard-night-dark/15872811.mp4"       # 7.1s, L55, a hand on a purple-lit keyboard
READ = STOCK / "videos/hands-turning-book-pages-lamp-night/11530072.mp4"           # 11.6s, L19-38, a book by candlelight
CLOCK = STOCK / "videos/wall-clock-ticking-dark/9160922.mp4"                      # 29.9s, L112, an alarm clock's second hand
WALK = STOCK / "videos/man-walking-alone-evening-path/20583507.mp4"               # 23.5s, L56, a figure walking off at dusk
VU = STOCK / "videos/vu-meter-needle-analog-audio/14232785.mp4"                   # 4.1s, L25, two amber VU meters on a rack
# The journal pair is the same shoot as the magnesium pair's `39425737`, which
# is a close face; these two are a lamp and a hand, and nothing in either
# frame repeats it.
JOURNAL = STOCK / "videos/person-writing-journal-night-lamp/39425736.mp4"         # 13.7s, L72, writing in a journal by a lamp
ALARM = STOCK / "videos/red-warning-light-flashing-dark/3882891.mp4"              # 13.0s, L21-31, a level crossing's red lights
WATCH = STOCK / "videos/smartwatch-heart-rate-wrist/5974322.mp4"                  # 15.2s, L105, a heart on a smartwatch
GAUGE = STOCK / "videos/pressure-gauge-needle/5637839.mp4"                        # 7.6s, L44, a gauge in a hand, needle moving
TOAST = STOCK / "videos/burnt-toast-toaster-smoke/4571351.mp4"                    # 13.0s, L100, burnt toast pops up at ~7.5s, smoking
WINDOW = STOCK / "videos/city-window-night-quiet-room/8591726.mp4"                # 38.7s, L33-37, a woman at a high window, from behind
NEURON = STOCK / "videos/neurons-firing-brain-animation-dark/40057909.mp4"        # 10.0s, L32-40, magenta filaments, the one abstract
AWAKE = STOCK / "videos/person-sleeping-peacefully-bed-dark/6941199.mp4"          # 18.7s, L87, awake at 1:28 by a sunrise lamp
SKY = STOCK / "videos/clouds-timelapse-dusk-sky/13282838.mp4"                     # 25.5s, L74-88, clouds over a sunset
STUDENT = STOCK / "videos/hand-writing-in-notebook-pen-dark/11025442.mp4"         # 14.7s, L56-68, numbers into an exercise book
FLIP = STOCK / "videos/flipping-through-notebook-pages/8247093.mp4"               # 13.1s, L83-92, paging back through a notebook
COFFEE = STOCK / "videos/pouring-coffee-cup-dark/7592661.mp4"                     # 36.9s, L44-51, an espresso pouring
CLOUD = STOCK / "videos/clouds-timelapse-dusk-sky/13286601.mp4"                   # 18.2s, L65-21, dusk clouds, black by 17s
THERAPY = STOCK / "videos/therapy-session-hands-notebook/7698448.mp4"             # 29.8s, L110, notes in a session. Bright;
                                                                                  # every session result is
BREATH = STOCK / "videos/hands-on-belly-deep-breathing/8795165.mp4"               # 25.8s, L86, a man breathing, hand on chest
RUN = STOCK / "videos/jogging-evening-feet-running/6573735.mp4"                   # 12.2s, L84-97, a runner up a hill at dusk
CANDLE = STOCK / "videos/candle-flame-dark-close/7033615.mp4"                     # 24.7s, L26-28, one flame on black
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/your-tinnitus-as-stressometer"

# The meter, 0 to 10, in the brand's peach running to a soft coral. No green:
# it is the one hue that cuts against this palette, and the site's own
# illustration of the same idea starts on it.
BANDS = [("Barely there", 0.35, "#ffdab9"),
         ("Noticeable", 0.70, "#f4a261"),
         ("Loud", 1.00, "#e76f51")]

SECTIONS = [
    # --- hook ---------------------------------------------------------------
    Section(
        title="Does stress make tinnitus worse?",
        card=False,
        sentences=[
            # A number, not a scene, in sentence one - and the subject named.
            ("Your tinnitus can read eight out of ten at half past two.",),
            # The `Split` opener lands on "four".
            ("By seven that evening, it reads four.",),
            ("Same ears, same day, five hours apart.",),
            # The reframe inside the first ten seconds (the user's call on
            # the first cut): the article's own "your very own
            # stress-o-meter" and "this shift in perspective". A change in
            # how it is seen, never a promise about how it sounds.
            ("That swing turns your tinnitus into your own personal "
             "stress-o-meter.",),
            ("And that one idea can change your whole perspective on it.",),
            ("Between those two readings came a deadline, an argument, and a "
             "short walk.",),
            # The retention promise. Paid off in the meter and routine
            # sections, and echoed in the close.
            ("By the end, you will know how to read yours, and what to do "
             "the moment it reads high.",),
        ],
        shots=[
            Shot(clip=TYPE, clip_at=0.0),
            Shot(clip=READ, clip_at=3.5),
            Shot(clip=CLOCK, clip_at=2.0),
            # "stress-o-meter" gets the meters.
            Shot(clip=VU, clip_at=0.0),
            # "Perspective" gets the widest view in the roster.
            Shot(clip=SKY, clip_at=1.0),
            Shot(clip=WALK, clip_at=6.0),
            Shot(clip=JOURNAL, clip_at=0.5),
        ],
        gaps=[0.55, 0.70, 0.60, 0.60, 0.85, 0.70, 0.90],
    ),

    # --- the mechanism, drawn as a loop -------------------------------------
    Section(
        title="Why would stress turn it up?",
        spoken_title="So why would stress turn the ringing up at all?",
        sentences=[
            ("When stress hits, your body's alarm system switches on.",),
            ("Adrenaline and cortisol rise, and every sense goes on high "
             "alert, your hearing included.",),
            # The hinge into the diagram - said, then shown.
            ("And it can keep itself going.",),
            # diagram, loop=True - one caption chunk per node.
            ("Stress puts you on alert,",
             "so the ringing seems louder,",
             "the louder ringing feels like a threat,",
             "and the threat keeps the alarm switched on."),
            # The article's own metaphor, and its "it's not you failing".
            ("It is a smoke alarm going off for burnt toast.",),
            ("Well-meaning, far too loud, and not your fault.",),
        ],
        shots=[
            Shot(clip=ALARM, clip_at=0.5),
            Shot(clip=WATCH, clip_at=1.0),
            None,                                       # hold the watch
            Shot(graphic="diagram",
                 payload=([("On alert", "stress switches it on", "⚡"),
                           ("Ringing seems louder", "every sense turned up",
                            "\U0001F514"),
                           ("Feels like a threat", "so you brace against it",
                            "⚠️"),
                           ("Alarm stays on", "and round it goes",
                            "\U0001F6A8")],
                          "WHY DOES IT FEED ITSELF?", True)),
            # The toast pops at ~7.5s; 6.0 puts it inside the sentence.
            Shot(clip=TOAST, clip_at=6.0),
            None,                                       # hold the smoke
        ],
        gaps=[0.55, 0.70, 0.80, 1.20, 0.60, 0.90],
    ),

    # --- attention, and the turn to the useful part -------------------------
    Section(
        title="Why does listening make it louder?",
        spoken_title="But why does listening for it make it louder?",
        sentences=[
            ("Stress narrows your focus, and your attention turns inward.",),
            ("The part of your brain that handles emotion talks constantly "
             "to your hearing pathways.",),
            ("So the harder you listen for the ringing, the louder it seems.",),
            ("That is the frustrating part, and it is also the useful one.",),
            ("Because if it climbs with stress, it can tell you when stress is "
             "climbing.",),
        ],
        shots=[
            Shot(clip=WINDOW, clip_at=2.0),
            Shot(clip=NEURON, clip_at=0.5),
            # 4.0s in: her eyes are open, beside a clock reading 1:28.
            Shot(clip=AWAKE, clip_at=4.0),
            # The candle, not the sky: the sky is the hook's and the close's.
            Shot(clip=CANDLE, clip_at=12.0),
            # The gauge, not the VU meter again: that clip is 4.1s and this
            # slot measured 4.2.
            Shot(clip=GAUGE, clip_at=0.5),
        ],
        gaps=[0.60, 0.70, 0.85, 0.80, 0.90],
    ),

    # --- reading the meter --------------------------------------------------
    Section(
        title="How do you read the meter?",
        spoken_title="So how do you actually read it?",
        sentences=[
            ("Start by giving it a number, the same way every time.",),
            # dial - scale first, needle second.
            ("Zero is silence, and ten is as loud as it gets.",
             "On a deadline afternoon, it might read an eight."),
            ("Then write down what was going on, and how you felt.",),
            # The hinge into the bars.
            ("Here is what a few log entries look like.",),
            # bars - one caption chunk per row, the article's sample entries.
            ("A deadline and an argument, eight.",
             "A quiet evening after a walk, four.",
             "A restless night before a presentation, five."),
            ("After a week or two, look back at what the high numbers have "
             "in common.",),
            # The article's own list of clues.
            ("A tense meeting. Coffee late in the day. A silent room at "
             "night.",),
            ("For many people, the high numbers start to line up with stress, "
             "like an early warning.",),
        ],
        shots=[
            Shot(clip=STUDENT, clip_at=1.0),
            Shot(graphic="dial",
                 payload=(BANDS, 0.8, "a deadline afternoon",
                          "HOW LOUD IS IT RIGHT NOW?", 10)),
            Shot(clip=JOURNAL, clip_at=6.0),
            None,                                       # hold the journal
            Shot(graphic="bars",
                 payload=([("A deadline, an argument", 0.8, "8"),
                           ("A quiet evening, after a walk", 0.4, "4"),
                           ("A restless night, a big day ahead", 0.5, "5")],
                          "AN EXAMPLE LOG")),
            Shot(clip=FLIP, clip_at=3.0),
            Shot(clip=COFFEE, clip_at=5.0),
            Shot(clip=ALARM, clip_at=6.0),
        ],
        gaps=[0.70, 1.20, 0.60, 0.80, 1.20, 0.70, 0.80, 0.90],
    ),

    # --- the twist: the reaction, not the reading ---------------------------
    Section(
        title="What makes a loud day worse?",
        spoken_title="So what makes a loud day even worse?",
        sentences=[
            ("Usually, it is how you react to it.",),
            # The hinge into the compare.
            ("Compare the two ways a high reading can go.",),
            # compare, name_columns - 8 chunks, heading then three items, twice.
            ("Take reacting first.",
             "You think, this is awful.",
             "You listen harder.",
             "And the alarm gets louder.",
             "Now compare that with reading it.",
             "You think, it is an eight.",
             "You ask what is going on.",
             "And you choose what to do next."),
            # The article's cloud.
            ("It is like noticing a cloud.",),
            ("You see it, and it does not have to ruin your day.",),
            # What talking therapy is built around - not what it does.
            ("Talking therapy is built around exactly that part: not the "
             "sound, but your reaction to it.",),
        ],
        shots=[
            Shot(clip=TYPE, clip_at=0.5),
            None,                                       # hold the keyboard
            Shot(graphic="compare",
                 payload=("REACTING",
                          ["This is awful", "Listen harder", "More alarm"],
                          "READING",
                          ["It's an eight", "What's going on?",
                           "Pick a response"], True)),
            Shot(clip=CLOUD, clip_at=3.0),
            None,                                       # hold the cloud
            Shot(clip=THERAPY, clip_at=2.0),
        ],
        gaps=[0.60, 0.80, 1.20, 0.55, 0.85, 0.90],
    ),

    # --- the routine --------------------------------------------------------
    Section(
        title="What do you do when it reads high?",
        spoken_title="So what do you do when it reads high?",
        sentences=[
            ("Have a routine ready before you need it.",),
            # steps - one caption chunk per node, all four from the article.
            ("First, note the number.",
             "Then breathe slowly, deep into your belly.",
             "Tense your shoulders and jaw, and let them go.",
             "And step away, even just around the room."),
            ("Practice it on calm days too, so it is there on the hard ones.",),
            ("Over weeks, the same log shows which habits bring your stress "
             "down.",),
        ],
        shots=[
            Shot(clip=WINDOW, clip_at=20.0),
            Shot(graphic="steps",
                 payload=(["Note the number", "Breathe into your belly",
                           "Tense, then let go", "Step away for a minute"],
                          "WHEN IT READS HIGH")),
            # 8.0s in: hand on his chest, mid-breath.
            Shot(clip=BREATH, clip_at=8.0),
            Shot(clip=RUN, clip_at=2.0),
        ],
        gaps=[0.80, 1.20, 0.70, 0.90],
    ),

    # --- red flags ----------------------------------------------------------
    Section(
        title="When is it not just stress?",
        spoken_title="But when is it not just stress?",
        sentences=[
            ("A meter like this is a self-check, not a diagnosis.",),
            ("If your tinnitus is severe, keeps distressing you, or changes "
             "suddenly, see a doctor or an audiologist.",),
            ("The same goes if it comes with hearing loss, dizziness, or "
             "pain.",),
        ],
        shots=[
            Shot(clip=GAUGE, clip_at=2.5),
            Shot(clip=CLOUD, clip_at=6.0),
            # The one labelled clip: the article's red flags, on screen as the
            # voice names them, over a flame rather than a person.
            Shot(clip=CANDLE, clip_at=2.0,
                 payload=("", "Sudden change, hearing loss, dizziness or "
                              "pain? Get it checked.")),
        ],
        gaps=[0.70, 0.60, 0.90],
    ),

    # --- close: echo the opening, then the question --------------------------
    Section(
        title="Back to that afternoon",
        spoken_title="So, back to that afternoon.",
        sentences=[
            ("Eight at half past two, four by seven, and the same ears both "
             "times.",),
            # The article's own "tinnitus isn't a gift".
            ("Tinnitus is not a gift, and none of this makes it one.",),
            ("But on the days it climbs, it may be telling you something about "
             "the day.",),
            ("So the next time yours reads high, what will you check first?",),
        ],
        shots=[
            Shot(clip=READ, clip_at=5.5),
            Shot(clip=WALK, clip_at=15.0),
            Shot(clip=SKY, clip_at=10.0),
            None,                                       # hold for the question
        ],
        gaps=[0.85, 0.80, 0.85, 3.00],
    ),
]

META = Meta(
    title="Does Stress Make Tinnitus Worse? Your Tinnitus as a Stress Meter",
    hook="Your tinnitus can read eight out of ten at half past two and four "
         "by seven - same ears, same day. That swing turns your tinnitus into "
         "your own personal stress-o-meter, and that one idea can change your "
         "whole perspective on it. Here is why stress can turn the ringing up, "
         "how to read it with a simple log, and what to do the moment it "
         "reads high.",
    url=URL,
    summary="Why stress can make tinnitus seem louder (the alarm that keeps "
            "itself on), how to rate it from zero to ten and keep a log, why "
            "the reaction to a loud day matters as much as the reading, a "
            "four-step routine for when it reads high, and the signs that "
            "mean see a doctor.",
    tags=["does stress make tinnitus worse", "stress and tinnitus",
          "tinnitus louder some days", "tinnitus stress", "tinnitus log",
          "tinnitus diary", "tinnitus anxiety", "tinnitus", "ringing in ears"],
    cta=f"The full article, with a sample log you can copy: {URL}",
    credits=["This video is general information, not medical advice. Rating "
             "your tinnitus is a self-check, not a diagnosis. If your "
             "tinnitus is severe, keeps distressing you, changes suddenly, or "
             "comes with hearing loss, dizziness or pain, please see a doctor "
             "or an audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/your-tinnitus-as-stressometer-long.mp4"
    work = Path.home() / "Desktop/.your-tinnitus-as-stressometer-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=11.0, title_hold=5.4,
        # The article's own two readings, no winner: why they differ is the
        # video. Lands as the voice says "four".
        opener=Split("8/10", "4/10", "Same ears?", at_word="four"),
        # The meter itself, as a still, with the title's own question.
        thumb_headline="Does stress make tinnitus [worse?]",
        thumb_image=THUMB_ART, thumb_accent="orange",
        thumb_crop_at=(0.5, 0.5), thumb_side="left", thumb_shift=0.24,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


# The dial drawn as a still for both thumbnails: `python <this> --thumb-art`.
# Needle at the midpoint - a needle pinned in the red on a thumbnail reads as
# a claim about somebody's ears (`beats.md`, `dial`).
ROOT = Path(__file__).resolve().parents[2]
THUMB_ART = ROOT / "assets/brand/graphics/stress-meter-dial.png"
THUMB_ART_V = ROOT / "assets/brand/graphics/stress-meter-dial-v.png"


def thumb_art() -> None:
    """The needle without the readout. A "5" under the hub on a thumbnail is
    a reading of nobody's ears; the needle sits wholly above the hub and the
    readout wholly below it, so the top of a needled render goes onto a
    needle-less one at the hub line. Same backdrop time, so no seam."""
    from video_automation.core.frame import LANDSCAPE, VERTICAL
    from video_automation.longform.beats import BEATS
    for frame, path in ((LANDSCAPE, THUMB_ART), (VERTICAL, THUMB_ART_V)):
        def dial(value):
            return BEATS["dial"](BANDS, value, "", "", 10, brand=TINNITUS,
                                 frame=frame, reveals=[0.2, 0.4], start=0.0,
                                 hold=6.0)
        needled = dial(0.5)
        _, cy, _, _, hub_r = needled._geom()
        cut = cy + hub_r + 24
        art = dial(None).draw(1.0)
        art.paste(needled.draw(1.0).crop((0, 0, frame.w, cut)), (0, 0))
        path.parent.mkdir(parents=True, exist_ok=True)
        art.save(path)
        print(path)


if __name__ == "__main__":
    import sys
    thumb_art() if "--thumb-art" in sys.argv else main()
