"""What really causes tinnitus? Ear or brain - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/the-role-of-neural-pathways-in-tinnitus-
perception.mdx (2024) - the path of sound, central gain, maladaptive
plasticity, the limbic system and prefrontal attention, the imaging findings
and the brain-targeted approaches. Not the 2023 `what-role-does-the-brain-
play-in-tinnitus`, whose sections promise relief through nutrition. The red
flags are the site's own list from `what-is-tinnitus`, as the sound-like pair
used them. Nothing here goes past what those say.

**Why this subject (2026-11-02, E11).** `youtube-audit outliers "is tinnitus
in the ear or the brain"` returned 12 standouts of 15, the densest page the
map has: UCI Otolaryngology "Is tinnitus an ear problem or a brain problem?"
(422k, 343x), Treble Health "The SHOCKING Truth About Tinnitus And Your
Brain" (76k, 7.4x), Dr. Berg "The Real Cause of Tinnitus (It's Not in Your
Ears)" (2.1M, 4.8x). Teardown: `docs/video/demand/teardowns/is-tinnitus-in-
the-ear-or-the-brain.md`. Treble's heatmap skips its anatomy tour and peaks
on the brain's alarm response and on "the brain can change" - so the ear
gets one beat and the alarm gets the loop.

**The title is the search.** "What causes tinnitus" is the evergreen query;
"ear or brain" is the question the standouts win on. The Short takes the UCI
phrasing, "is tinnitus an ear problem or a brain problem".

**The spine.** It starts in the ear, but the sound is made in the brain; the
path a sound takes (ear, nerve, thalamus, cortex); less input, so the brain
turns its gain up and its own activity comes through as a sound; the alarm
loop - noticing, stress, more gain - which is why it is loudest in quiet,
stress and attention; made by the brain is not made up; what the brain side
means for research. The echo: starts in the ear, made in the brain.

**The beats.** The last three tinnitus long forms ran spectrum/diagram/grid
(sound-like), post/checklist/bars/diagram/spotlight (Beethoven) and
diagram/reel/dial/grid (spike). Here:

- `reel` - the path, ear to cortex, one card per stage, diving into the last
  card and continuing as that clip. A path is a thing the viewer should feel
  move, which is what the reel is for.
- `dial`, needle on, no unit - the article's own "volume knob": the brain's
  gain turned up. The needle is a claim about the mechanism, not about any
  viewer's reading.
- `diagram(loop=True)` - notice it, the alarm reacts, stress turns the gain
  up, so you notice it more. Four nodes where the spike pair had three.
- the notice card for the red flags.

`spotlight` was considered for the site's `brain-research.jpg` and refused:
it is a structural MRI film at 600px, and ringing a slice as "the auditory
cortex" would be a precision the picture does not have.

**The medical line.** Nothing here says an approach lowers the ringing.
Sound therapy and talking therapy are described by what they are (other
input, less contrast; work on the reaction even when the sound stays);
stimulation and notched sound are "still being studied"; and "none of these
reliably removes tinnitus for everyone" is said aloud. "Made by the brain"
is never "in your head": the proof section says the opposite, from the
article's imaging. Talking therapy, not the initialism.

**Footage.** From the cache, contact-sheeted at 15/50/85% on 2026-11-02:
neuron and signal animations for what cannot be filmed, a knob and a fader
for the gain, the act of listening for the rest. The ball-and-stick
"neural network" clips read as chemistry and are out.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/is-tinnitus-in-the-ear-or-the-brain.py
    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/is-tinnitus-in-the-ear-or-the-brain.py --thumb
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Split

SOURCE_POST = "the-role-of-neural-pathways-in-tinnitus-perception"
DEMAND = ("'is tinnitus in the ear or the brain': UCI 'Is tinnitus an ear "
          "problem or a brain problem?' Short 422k (343x), Treble 'The "
          "SHOCKING Truth About Tinnitus And Your Brain' 76k (7.4x); "
          "teardowns/is-tinnitus-in-the-ear-or-the-brain.md")

V = STOCK / "videos"
# Duration, luma, what is in the frame. Screened 2026-11-02.
EARBUDS = V / "person-putting-in-earbuds-dark/5008497.mp4"                  # 16s, L57-59, a hand takes earbuds from their case, warm bokeh
PINK = V / "neurons-firing-brain-animation-dark/40057909.mp4"              # 10s, L31-37, a cell firing pink threads outward
ORANGE = V / "brain-neurons-abstract-dark/29184317.mp4"                    # 10s, L23-27, orange cells, signals streaking between them
GOLD = V / "brain-neurons-abstract-dark/34913063.mp4"                      # 10s, L22-33, gold cells pulsing
BLUE = V / "neuron-electrical-signal-dark-blue-animation/34913408.mp4"     # 10s, L13-19, sparse blue cells, a few lit
VIOLET = V / "neuron-electrical-signal-dark-blue-animation/34914524.mp4"   # 10s, L9-33, violet cells, one firing large
WIRED = V / "neural-network-visualization/37101560.mp4"                    # 10s, L30-73, a gold fibre network (footage.md: kept)
FIBER = V / "fiber-optic-light-cables-dark/8817471.mp4"                    # 21s, L46-52, a bundle of fibres carrying light
WAVE = V / "sound-wave-visualization-dark/34645273.mp4"                    # 20s, L7, a dotted waveform on black
SPARK = V / "electric-spark-dark/35048273.mp4"                             # 10s, L29-33, a spark branching on black
MEDSCAN = V / "medical-scan-radiology-monitor-dark/7088464.mp4"            # 22s, L40, a man reading brain scans on a monitor
KNOB = V / "hand-turning-volume-knob-dark/12213088.mp4"                    # 10s, L15-18, a hand turning a desk knob
FADER = V / "audio-mixer-volume-fader-dark-studio/37050520.mp4"            # 10s, L38-61, a finger pushing a lit fader
EQ = V / "audio-equalizer-lights-dark/7087627.mp4"                         # 9s, L41-50, fingers on a purple-lit desk
SPEAKER = V / "concert-speaker-stack-stage/8513956.mp4"                    # 18s, L26-32, a guitarist in front of the amps
CONCERT = V / "concert-crowd-lights/13082773.mp4"                          # 25s, L20-24, an arena from the crowd, stage lights
SITTING = V / "person-sitting-still-in-quiet-dark-room/8860237.mp4"        # 30s, L47-49, a figure in a chair by a curtained window
THINK = V / "woman-thinking-quietly-dark-room-evening-portrait/9808085.mp4"  # 24s, L44-46, a woman sitting still under a lamp
BREATH = V / "man-breathing-deeply-eyes-closed-dark-room-calm/5495782.mp4"   # 12s, L32-34, a man in a hood, eyes down
CITYWIN = V / "city-window-night-quiet-room/8591726.mp4"                   # 39s, L33-36, a woman at a window over a lit city
HEADWIN = V / "person-headphones-sitting-window-calm-evening/6892729.mp4"  # 27s, L38-40, a man in headphones by a window
WOMANHP = V / "woman-listening-headphones-window-night/6688133.mp4"        # 30s, L35-37, a woman in headphones, hand at her chin
ALARMCLK = V / "alarm-clock-night-dark-bedroom/35999376.mp4"              # 11s, L35, a hand by a phone on a nightstand
MUG = V / "hands-holding-mug-talking-dark/6245131.mp4"                     # 13s, L51-63, hands round a mug, gesturing as they talk
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"          # the noah test, pair 4 of 5 (`projects/tinnitus.md`)
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/the-role-of-neural-pathways-in-tinnitus-perception"

# The brain's gain, as the article's "volume knob". No unit (top=0): this is
# a mechanism, not anybody's measurement.
GAIN = [("Quiet", 0.33, "#ffdab9"),
        ("Normal", 0.66, "#f4a261"),
        ("Turned up", 1.00, "#e76f51")]

# Thumbnail - the title's own question, never its answer. Pexels 30560359
# (Shamil V): a man in profile, thinking, a black silhouette on studio white.
# A head with nothing in it to read, which is the question. Not 4584294, a
# man holding his head - the suffering portrait this channel does not use.
THUMB_HEADLINE = "Is it your\nears, or your\n[brain?]"
THUMB_PHOTO = STOCK / "photos/man-thinking-silhouette-white/30560359.jpg"


SECTIONS = [
    # --- hook ---------------------------------------------------------------
    Section(
        title="Is tinnitus in your ears, or your brain?",
        card=False,
        sentences=[
            # The Split opener stands over this, EAR against BRAIN.
            ("Is tinnitus in your ears, or in your brain?",),
            # The reversal, in sentence 2.
            ("It usually starts in the ear. But the sound you hear is not "
             "made there.",),
            # The proof, said early.
            ("Brain scans show extra activity in the hearing part of the "
             "brain, even in total silence.",),
            ("And how loud it seems depends on what the rest of your brain "
             "is doing.",),
            # The promise - paid off by the sections, in this order.
            ("By the end, you will know where the sound is made, why "
             "noticing it turns it up, and why none of that means you are "
             "imagining it.",),
        ],
        shots=[
            Shot(clip=EARBUDS, clip_at=0.5),
            Shot(clip=PINK, clip_at=1.0),
            Shot(clip=MEDSCAN, clip_at=1.0),
            Shot(clip=THINK, clip_at=1.0),
            # The title rides here.
            Shot(clip=CITYWIN, clip_at=2.0),
        ],
        gaps=[1.00, 0.85, 0.70, 0.60, 0.90],
    ),

    # --- the path -----------------------------------------------------------
    Section(
        title="How does a sound reach your brain?",
        spoken_title="So how does a sound reach your brain at all?",
        kicker="THE PATH",
        sentences=[
            ("It starts as a vibration in the air.",),
            # reel - one sentence per card, held with None.
            ("In your inner ear, tiny hair cells turn it into electrical "
             "signals.",),
            ("The auditory nerve carries those signals out of the ear.",),
            ("They climb through the brainstem to the thalamus, a relay that "
             "filters what gets through.",),
            ("And only in the auditory cortex does a signal become something "
             "you hear.",),
            # The reel dives into the cortex card and continues as its clip.
            ("So your ears collect sound. Your brain is what hears it.",),
        ],
        shots=[
            Shot(clip=SPEAKER, clip_at=2.0),
            Shot(graphic="reel",
                 payload=([(WAVE, "HAIR CELLS"),
                           (FIBER, "THE NERVE", 4.0),
                           (None, "THE THALAMUS"),
                           (ORANGE, "THE CORTEX")],
                          "THE PATH OF A SOUND", True)),
            None,
            None,
            None,
            Shot(clip=ORANGE, clip_at=0.0),
        ],
        gaps=[0.55, 0.70, 0.70, 0.70, 0.90, 0.95],
    ),

    # --- the gain -----------------------------------------------------------
    Section(
        title="What happens when the signal goes quiet?",
        spoken_title="Now, what happens when part of that signal goes "
                     "missing?",
        kicker="THE GAIN",
        sentences=[
            ("Loud noise, or age, can wear down some of those hair cells.",),
            ("Then fewer signals reach the brain, for the pitches those cells "
             "used to carry.",),
            ("But the brain does not simply accept the quiet.",),
            # dial - the scale, then the needle.
            ("Think of a volume knob inside it, for everything you hear.",
             "With less coming in, the brain turns that knob up."),
            ("Researchers call this central gain.",),
            ("Turned up that far, the brain's own background activity starts "
             "to come through as a sound.",),
            ("That is the ringing. Not a noise in your ear, but your hearing "
             "system turned up too far.",),
            ("Over time the brain can rewire around the lost pitches, which "
             "may be part of why the sound stays.",),
        ],
        shots=[
            Shot(clip=CONCERT, clip_at=2.0),
            Shot(clip=BLUE, clip_at=1.0),
            Shot(clip=SITTING, clip_at=2.0),
            Shot(graphic="dial",
                 payload=(GAIN, 0.86, "the brain's gain", "THE VOLUME KNOB",
                          0)),
            Shot(clip=KNOB, clip_at=1.0),
            Shot(clip=SPARK, clip_at=1.0),
            Shot(clip=FADER, clip_at=1.0),
            Shot(clip=GOLD, clip_at=1.0),
        ],
        gaps=[0.55, 0.85, 0.70, 1.10, 0.60, 0.70, 0.90, 0.90],
    ),

    # --- the alarm ----------------------------------------------------------
    Section(
        title="Why does it get louder when you notice it?",
        spoken_title="So why does it get louder the moment you notice it?",
        kicker="THE ALARM",
        sentences=[
            ("Your hearing does not work alone.",),
            ("It is wired to the parts of the brain that handle emotion, "
             "memory and attention.",),
            ("One of them is the amygdala, the brain's alarm, which decides "
             "what counts as a threat.",),
            # diagram, loop=True - one chunk per node; the last closes it.
            ("You notice the sound in a quiet room.",
             "Your brain's alarm reacts, and stress kicks in.",
             "Stress turns the hearing system up further.",
             "So the sound seems louder, and you notice it more."),
            ("That is why it often seems loudest in a quiet room, on a "
             "stressful day, or the moment you check for it.",),
            ("Scans back this up. In people with tinnitus, the hearing areas "
             "and the alarm are more closely linked.",),
        ],
        shots=[
            Shot(clip=HEADWIN, clip_at=2.0),
            Shot(clip=WIRED, clip_at=1.0),
            Shot(clip=ALARMCLK, clip_at=1.0),
            Shot(graphic="diagram",
                 payload=([("You notice it", "in a quiet room",
                            "\U0001F56F"),
                           ("The alarm reacts", "stress kicks in",
                            "\U0001F6A8"),
                           ("The gain goes up", "the hearing system",
                            "\U0001F50A"),
                           ("It seems louder", "so you notice it more",
                            "\U0001F501")],
                          "THE ALARM LOOP", True)),
            Shot(clip=BREATH, clip_at=1.0),
            Shot(clip=MEDSCAN, clip_at=10.0),
        ],
        gaps=[0.55, 0.60, 0.80, 1.40, 0.85, 0.95],
    ),

    # --- the proof ----------------------------------------------------------
    Section(
        title="Does that mean it is all in your head?",
        spoken_title="But does that mean it is all in your head?",
        kicker="THE PROOF",
        sentences=[
            ("No. Made by the brain does not mean made up.",),
            ("The activity is real, it sits in real places, and researchers "
             "can measure it.",),
            ("Recordings of brain waves show different patterns in people "
             "with tinnitus, linked to how strong it is.",),
            ("It just has no source outside you.",),
        ],
        shots=[
            Shot(clip=PINK, clip_at=5.0),
            Shot(clip=BLUE, clip_at=4.0),
            Shot(clip=WAVE, clip_at=10.0),
            Shot(clip=CITYWIN, clip_at=20.0),
        ],
        gaps=[0.80, 0.55, 0.70, 0.95],
    ),

    # --- the research -------------------------------------------------------
    Section(
        title="What is research doing with the brain side?",
        spoken_title="So what are researchers doing with the brain side?",
        kicker="THE RESEARCH",
        sentences=[
            ("The brain's ability to rewire is called neuroplasticity, and it "
             "works both ways.",),
            ("So most newer approaches aim at the brain, not the ear.",),
            ("Sound therapy gives the hearing system something else to "
             "listen to, so the tinnitus stands out less.",),
            ("Talking therapy works on the alarm side: how the brain reacts, "
             "even when the sound itself stays.",),
            ("And magnetic stimulation, or music with your tone's pitch cut "
             "out, are still being studied.",),
            ("None of these reliably removes tinnitus for everyone.",),
            # The site's red flags, on the notice card as they are said.
            ("And if yours is new, in one ear only, pulses with your "
             "heartbeat, or comes with dizziness or hearing loss, see a "
             "doctor first.",),
        ],
        shots=[
            Shot(clip=ORANGE, clip_at=4.0),
            Shot(clip=SPARK, clip_at=5.0),
            Shot(clip=WOMANHP, clip_at=2.0),
            Shot(clip=MUG, clip_at=0.5),
            Shot(clip=EQ, clip_at=0.5),
            Shot(clip=THINK, clip_at=12.0),
            Shot(clip=ALARMCLK, clip_at=2.5,
                 payload=("NOTICE", "New, one ear only, pulsing, or with "
                                    "dizziness? See a doctor.")),
        ],
        gaps=[0.55, 0.80, 0.55, 0.55, 0.80, 0.90, 0.95],
    ),

    # --- close: echo the opening, then the question -------------------------
    Section(
        title="So, ears or brain?",
        spoken_title="So, is it your ears, or your brain?",
        kicker="THE ANSWER",
        sentences=[
            ("Most of the time, it starts in the ear.",),
            ("But the sound is made, turned up and noticed in the brain.",),
            ("Which is why it changes with silence, stress and attention.",),
            ("Next time yours gets louder, what was your brain busy noticing "
             "just before?",),
        ],
        shots=[
            Shot(clip=EARBUDS, clip_at=8.0),
            Shot(clip=VIOLET, clip_at=0.5),
            Shot(clip=SITTING, clip_at=15.0),
            Shot(clip=HEADWIN, clip_at=14.0),
        ],
        gaps=[0.60, 0.80, 0.90, 3.00],
    ),
]

META = Meta(
    title="What Really Causes Tinnitus? Your Ears or Your Brain",
    hook="Tinnitus usually starts in the ear, but the sound itself is made in "
         "the brain. Here is the path a sound takes, why the brain turns its "
         "own volume up when the ear sends less, why noticing it and stress "
         "make it seem louder, and why none of that means you are imagining "
         "it.",
    url=URL,
    summary="Where tinnitus comes from: hair cells in the inner ear, the "
            "auditory nerve, the thalamus and the auditory cortex; central "
            "gain, the brain turning up its sensitivity when less signal "
            "arrives; how the brain's emotional and attention systems (the "
            "amygdala, the prefrontal cortex) make it seem louder in quiet, "
            "under stress and when you check for it; what brain imaging and "
            "brain-wave studies have found; and what research is doing with "
            "the brain side.",
    tags=["what causes tinnitus", "is tinnitus in the brain",
          "tinnitus ear or brain", "tinnitus and the brain",
          "central gain tinnitus", "why is tinnitus louder at night",
          "tinnitus stress", "neuroplasticity tinnitus", "tinnitus",
          "ringing in ears"],
    cta=f"The full article, with each brain region, the imaging research and "
        f"the treatments being studied: {URL}",
    credits=["This video is general information, not medical advice. If your "
             "tinnitus is new, in one ear only, pulses with your heartbeat, "
             "or comes with dizziness or hearing loss, please see a doctor."],
)


def thumbs(out: Path) -> Path:
    """The silhouette from his hair to his chest, scaled to the frame's
    height and set against the right edge; the studio white continued to the
    left as the ground for three dark rows he is facing (`thumbnails.md`,
    rules 1 and 3 - the subject whole, dark ink on a flat light ground)."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(THUMB_PHOTO).convert("RGB")
    w, h = src.size
    cut = src.crop((0, int(h * 0.14), w, int(h * 0.78)))
    cw = int(cut.width * 720 / cut.height)
    im = Image.new("RGB", (1280, 720), cut.getpixel((8, 8)))
    im.paste(cut.resize((cw, 720), Image.LANCZOS), (1280 - cw, 0))
    fill, ink = T.ACCENTS["red"]
    T._headline(im, THUMB_HEADLINE, 240, 470, 40, fill, ink, max_lines=3,
                leading=1.02, band="middle", margin=40, shadow=11,
                drop=(5, 6), text=(20, 20, 20))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/is-tinnitus-in-the-ear-or-the-brain-long.mp4"
    work = Path.home() / "Desktop/.is-tinnitus-in-the-ear-or-the-brain-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=15.0, title_hold=5.0,
        # The pair shares the opener: the question is a comparison, and the
        # last three tinnitus long forms opened on `Search`.
        opener=Split("Ear", "Brain", "WHERE IS IT MADE?"),
        emphasis=["hears", "knob", "made up"],
        thumb_headline=THUMB_HEADLINE, thumb_image=THUMB_PHOTO,
        thumb_accent="red",
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home()
                     / "Desktop/is-tinnitus-in-the-ear-or-the-brain-long-thumb.jpg"))
    else:
        main()
