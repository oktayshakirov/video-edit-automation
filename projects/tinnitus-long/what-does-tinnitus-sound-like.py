"""What does tinnitus sound like? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/what-is-tinnitus.mdx - its "Identifying
Tinnitus Symptoms", causes, diagnosis and "When Should You See a Doctor"
sections. Nothing here goes past what that article says.

**Why this subject (2026-10-28, E11).** `youtube-audit outliers` on 10-28
found "what does tinnitus sound like" standing out on two channels: MUSC
Health's "Ask an Audiologist: What Does Tinnitus Sound Like?" (593k, 4820x
its median) and UCI Otolaryngology's "Is tinnitus ringing or buzzing?"
(1.1M, 932x). Both are 11-19 second Shorts; the teardown is
`docs/video/demand/teardowns/what-does-tinnitus-sound-like.md`. Their
comment sections are viewers describing their own sound, and the most-liked
complaint under UCI's is that tinnitus does not always mean hearing loss -
which the article answers.

**The title is the search.** "What does tinnitus sound like" is the typed
question, so the opener is `Search` typing it. The Short takes "is tinnitus
ringing or buzzing".

**The spine.** Ringing is one of five sounds; each is described in the
article's own comparisons (steam, insects, a waterfall); on one picture they
sit at different pitches; the sound most often starts with worn hair cells
and a brain filling the gap - yet many people test as normal; two kinds keep
time with the body (a click with the jaw, a beat with the pulse); the beat is
one of the article's red flags; a check can match your sound to a tone. The
echo: ringing is only the best known.

**The beats.** The last three tinnitus long forms ran diagram/reel/dial/grid
(spike), post/checklist/bars/diagram/spotlight (Beethoven) and dial/bars/
diagram (stress). Here:

- `spectrum`, in the sounds mode built for this video (`beats.md`): one peak
  glides from the ringing to the hiss to the hum to the roar as each is
  named. The axis says LOW and HIGH, not Hz - the article describes pitch in
  words, so a kHz scale would be a precision nobody measured.
- `diagram` - hair cells, less signal, the brain fills the gap. Three nodes,
  no loop: it is a chain, not the spike's feedback loop.
- `grid`, two cards - the click with the jaw, the beat with the pulse.
- the notice card for the red flags.

**The sounds are played, short and quiet, after a warning** (`core/
samples.py`). The first cut drew them only, because much of this audience
has hyperacusis or is listening at night. The feed check reversed it: every
top result for this query plays examples, so drawn-only was the weaker
promise. The user's call (2026-10-28): a 1.6s sample of each, well under the
voice, the bed dipped under it, after the warning is said and shown on the
notice card over a hand turning a volume knob. Each sound is its own
sentence so its sample sits in the pause after the name, never under it.

**The medical line.** No sound is tied to a diagnosis. "Can point to" and
"can come from" are the article's own hedges. The red flags are the
article's list, on the notice card as they are said; jaw problems and an ear
specialist are never named by an initialism.

**Footage.** Fetched fresh on 2026-10-28, contact-sheeted at 15/50/85%
(verdicts in `docs/video/footage.md`). The nouns are the article's own
comparisons: steam, machinery, a waterfall, a singing bowl's tone, TV
static. No insect close-ups: the user cut the cricket as disturbing.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/what-does-tinnitus-sound-like.py
    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/what-does-tinnitus-sound-like.py --thumb
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "what-is-tinnitus"
DEMAND = ("'what does tinnitus sound like': MUSC Health Short 593k (4820x), "
          "UCI 'Is tinnitus ringing or buzzing?' 1.1M (932x); "
          "teardowns/what-does-tinnitus-sound-like.md")

V = STOCK / "videos"
# Duration, luma, what is in the frame. All fetched 2026-10-28.
BOWL = V / "singing-bowl-ringing-dark/4488445.mp4"                 # 20s, L13-17, a hand rings a brass bowl by candlelight
BOWL2 = V / "singing-bowl-ringing-dark/4487438.mp4"                # 41s, L12-28, the bowl and its striker, candles behind
KETTLE = V / "kettle-steam-dark-kitchen/32001621.mp4"              # 33s, L76, a steel kettle on a dark wall, a thread of steam
STEAM = V / "steam-rising-dark-background/29686188.mp4"            # 19s, L9-25, steam billowing on black
SMOKE = V / "steam-rising-dark-background/9694807.mp4"             # 39s, L28, slow wisps drifting on black
FAN = V / "electric-fan-spinning-dark-room/3069096.mp4"            # 15s, L4-7, a fan's blades, lit at the tips, spinning
WATER = V / "waterfall-at-night-dark/27591404.mp4"                 # 23s, L27-41, white water tumbling, blue night
FALLS = V / "waterfall-at-night-dark/4208224.mp4"                  # 22s, L28, water falling down a dark rock face
WAVES = V / "ocean-waves-at-night-dark/11287848.mp4"               # 30s, L20, dark sea, small glints
SURF = V / "ocean-waves-at-night-dark/40200251.mp4"                # 34s, L29-64, surf from above, violet
STATIC = V / "old-radio-static-dark/11999587.mp4"                  # 12s, L13-31, an old TV in a dark room comes on to static
WAVEFORM = V / "oscilloscope-sine-wave/34645273.mp4"               # 20s, L7, a dotted waveform on black
CHEST = V / "hand-on-chest-heartbeat-dark/9737994.mp4"             # 18s, L58-60, a woman's hand resting on her chest
CONCERT = V / "concert-crowd-lights/13082773.mp4"                  # 25s, L20-24, an arena from the crowd, stage lights
HANDS = V / "elderly-hands-close-up-dark/5214600.mp4"              # 21s, L75-79, an older man's hands on a tablet
LISTEN = V / "hearing-test-headphones/7651887.mp4"                 # 9s, L77-85, a man on a sofa, wired headphones on
WINDOW = V / "man-looking-out-window-at-night-city/4538212.mp4"    # 16s, L51, a figure at a window, city below
BALCONY = V / "man-looking-out-window-at-night-city/38380402.mp4"  # 12s, L50, a man at a balcony rail, towers lit
AMBER = V / "quiet-bedroom-at-night-window-light/36244322.mp4"     # 13s, L54, a man on a bed by a window, amber room
LAMP = V / "quiet-bedroom-at-night-window-light/19919755.mp4"      # 29s, L73, a man sitting up in bed by a lamp
BED = V / "woman-lying-awake-in-bed-dark/6944078.mp4"              # 15s, L27-32, somebody lying in bed, warm light
DESK = V / "headphones-on-desk-dark/8100340.mp4"                   # 38s, L34, a woman at a monitor, headphones round her neck
PEN = V / "hand-writing-notes-at-night-desk-lamp/8631662.mp4"      # 13s, L41-44, a hand writing under a lamp, a glass of water
READER = V / "woman-sitting-by-window-at-night/17673702.mp4"       # 14s, L31, a woman reading in a lit window
STREET = V / "strong-wind-trees-night/5765474.mp4"                 # 14s, L23, a street lamp in wind and rain
KNOB = V / "hand-turning-volume-knob-dark/12213088.mp4"            # 10s, L15-17, a hand turning a desk knob
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"          # the noah test, pair 3 of 5 (`projects/tinnitus.md`)
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/what-is-tinnitus"

# The four steady sounds, low to high on a log axis. Ringing is a narrow
# tone; hissing is the article's "high-pitched", wide; humming is its
# "low-frequency", narrow; roaring is low and "encompassing", wide.
SOUNDS = [(5200, 6800, "RINGING"),
          (2800, 12000, "HISSING"),
          (110, 210, "HUMMING"),
          (140, 1400, "ROARING")]

# Thumbnail - the title's own question, never its answer.
THUMB_HEADLINE = "What does\ntinnitus\n[sound like?]"
THUMB_PHOTO = STOCK / "photos/young-man-paper-cup-phone/3761514.jpg"   # the user's pick, Pexels 3761514


SECTIONS = [
    # --- hook ---------------------------------------------------------------
    Section(
        title="What does tinnitus actually sound like?",
        card=False,
        sentences=[
            # The Search opener types this as it is said.
            ("What does tinnitus actually sound like?",),
            ("Ringing is the one everybody has heard of. But people describe "
             "at least five.",),
            ("And two kinds keep time with something in your own body.",),
            # The proof: where this comes from.
            ("Everything here comes from the NHS, the Mayo Clinic, and "
             "America's National Institutes of Health.",),
            # The promise - paid off by the sections, in this order.
            ("By the end, you will know each sound, why two of them are "
             "different, and which one is worth getting checked.",),
        ],
        shots=[
            Shot(clip=BOWL, clip_at=0.5),
            Shot(clip=STEAM, clip_at=1.0),
            Shot(clip=CHEST, clip_at=1.0),
            Shot(clip=PEN, clip_at=1.0),
            # The title rides here.
            Shot(clip=WINDOW, clip_at=1.0),
        ],
        gaps=[1.00, 0.80, 0.80, 0.60, 0.90],
    ),

    # --- the five sounds ----------------------------------------------------
    Section(
        title="Is tinnitus always a ringing?",
        spoken_title="So, is tinnitus always a ringing?",
        kicker="FIVE SOUNDS",
        sentences=[
            ("Tinnitus is any sound you hear that has no source outside "
             "you.",),
            ("It is a symptom, not a disease, and it does not have one "
             "sound.",),
            ("Ringing is one of the most common: a tone that stays, or comes "
             "and goes.",),
            ("Hissing, or whistling, is high-pitched, like air or steam "
             "escaping.",),
            ("Buzzing, or humming, is low, and people compare it to "
             "machinery, or insects.",),
            ("Roaring is bigger, more like a waterfall, or a strong wind.",),
            # The warning, said and on the notice card, before any sample.
            ("Next, a short, quiet sample of each. If sounds bother you, turn "
             "your volume down now.",),
            # spectrum, sounds mode - the floor, then one sentence per sound,
            # its sample in the gap after it (`core/samples.py`).
            ("Here are four of them on one picture, from low to high.",),
            ("The ringing.",),
            ("The hiss.",),
            ("The hum.",),
            ("And the roar.",),
            ("The fifth, a click or a pop, does not sit on that picture at "
             "all.",),
            ("Whichever yours is, it often sounds louder in a quiet room, or "
             "when you are stressed.",),
        ],
        shots=[
            Shot(clip=SMOKE, clip_at=2.0),
            Shot(clip=WAVEFORM, clip_at=1.0),
            Shot(clip=BOWL2, clip_at=1.0),
            Shot(clip=KETTLE, clip_at=4.0),
            # The machinery: the user cut the cricket close-up as disturbing
            # (2026-10-28). Later in the fan clip than THE RHYTHM's use of it.
            Shot(clip=FAN, clip_at=8.0),
            Shot(clip=WATER, clip_at=1.0),
            Shot(clip=KNOB, clip_at=1.0,
                 payload=("NOTICE", "Quiet sound samples next. Lower your "
                                    "volume if sounds bother you.")),
            Shot(graphic="spectrum",
                 payload=(SOUNDS, "FOUR SOUNDS, LOW TO HIGH", "", "peak"),
                 samples=(None, "ringing", "hissing", "humming", "roaring")),
            None, None, None, None,
            Shot(clip=STATIC, clip_at=2.0),
            Shot(clip=AMBER, clip_at=1.0),
        ],
        # 2.30 after each sound: its 1.6s sample, and air either side.
        gaps=[0.60, 0.80, 0.55, 0.55, 0.55, 0.80, 0.90, 0.70,
              2.30, 2.30, 2.30, 2.30, 0.80, 0.90],
    ),

    # --- the source ---------------------------------------------------------
    Section(
        title="Where does the sound come from?",
        spoken_title="So where does the sound come from?",
        kicker="THE SOURCE",
        sentences=[
            ("Most often, it starts in the inner ear.",),
            # diagram - one chunk per node.
            ("Loud noise, or age, wears down the tiny hair cells that pick "
             "up sound.",
             "So less signal reaches the brain.",
             "And the brain fills the gap with a sound of its own."),
            ("That is why tinnitus so often comes with some hearing loss.",),
            ("But many people with tinnitus have only mild hearing loss, or "
             "even test as normal.",),
            ("So a normal hearing test does not mean you are imagining "
             "it.",),
        ],
        shots=[
            Shot(clip=CONCERT, clip_at=2.0),
            Shot(graphic="diagram",
                 payload=([("Hair cells wear down", "loud noise, or age",
                            "\U0001F50A"),
                           ("Less signal", "reaches the brain",
                            "\U0001F509"),
                           ("The brain fills the gap", "with a sound of its own",
                            "\U0001F9E0")],
                          "WHERE THE SOUND COMES FROM")),
            Shot(clip=HANDS, clip_at=2.0),
            Shot(clip=LISTEN, clip_at=0.5),
            Shot(clip=BALCONY, clip_at=1.0),
        ],
        gaps=[0.60, 1.10, 0.80, 0.70, 0.90],
    ),

    # --- the rhythm ---------------------------------------------------------
    Section(
        title="Does yours keep time with something?",
        spoken_title="Now, does yours keep time with something?",
        kicker="THE RHYTHM",
        sentences=[
            ("Two kinds of tinnitus are different, because they follow your "
             "body.",),
            # grid - one sentence per card, its sample in the gap after it.
            ("A click or a pop can seem to keep time with your jaw, or with "
             "swallowing.",),
            ("And a whoosh or a thump can keep time with your heartbeat.",),
            ("The click can point to the jaw joint, and the muscles around "
             "it.",),
            ("The beat has its own name: pulsatile tinnitus.",),
            ("It can come from blood flow near the ear.",),
        ],
        shots=[
            Shot(clip=FAN, clip_at=1.0),
            Shot(graphic="grid",
                 payload=([("Clicking", "with your jaw, or swallowing",
                            "\U0001F9B7"),
                           ("Pulsing", "with your heartbeat", "\U0001F493")],
                          "WHAT IT KEEPS TIME WITH"),
                 samples=("clicking", "pulsing")),
            None, None,
            Shot(clip=CHEST, clip_at=8.0),
            Shot(clip=BED, clip_at=1.0),
        ],
        gaps=[0.70, 2.30, 2.80, 0.80, 0.60, 0.90],
    ),

    # --- the red flags ------------------------------------------------------
    Section(
        title="When is the sound worth a check?",
        spoken_title="So when is the sound worth a doctor's look?",
        kicker="THE RED FLAGS",
        sentences=[
            ("A beat in time with your pulse is one of the signs worth a "
             "doctor's look.",),
            # The article's list, on the notice card as it is said.
            ("So is a sound in one ear only, one that came on suddenly, or "
             "one after a knock to the head.",),
            ("Or one that comes with dizziness, hearing loss, or pain in "
             "the ear.",),
            ("And if it is wearing down your sleep or your days, that counts "
             "too.",),
            ("At a check, a hearing specialist can match your sound to a "
             "tone: its pitch, and its loudness.",),
            ("So it helps to know which of the five yours is.",),
        ],
        shots=[
            Shot(clip=DESK, clip_at=2.0),
            Shot(clip=STREET, clip_at=1.0,
                 payload=("NOTICE", "Pulsing, one ear only, sudden, or "
                                    "after a head injury? See a doctor.")),
            Shot(clip=WAVES, clip_at=2.0),
            Shot(clip=LAMP, clip_at=2.0),
            Shot(clip=WAVEFORM, clip_at=10.0),
            Shot(clip=PEN, clip_at=5.0),
        ],
        gaps=[0.60, 0.70, 0.70, 0.90, 0.70, 0.90],
    ),

    # --- close: echo the opening, then the question -------------------------
    Section(
        title="So, what does yours sound like?",
        spoken_title="So, what does yours sound like?",
        kicker="THE ECHO",
        sentences=[
            ("Ringing is only the best known.",),
            ("Yours might hiss, hum, roar or click, and it is still "
             "tinnitus.",),
            ("And if it keeps time with your heartbeat, that is the one to "
             "get checked.",),
            ("If you had to name yours, which of the five would it be?",),
        ],
        shots=[
            Shot(clip=BOWL2, clip_at=14.0),
            Shot(clip=FALLS, clip_at=2.0),
            Shot(clip=SURF, clip_at=4.0),
            Shot(clip=READER, clip_at=1.0),
        ],
        gaps=[0.60, 0.80, 0.90, 3.00],
    ),
]

META = Meta(
    title="What Does Tinnitus Sound Like? Ringing, Hissing, Buzzing and More",
    hook="Ringing is only one of the sounds tinnitus can be. Here are the five "
         "people describe, where each sits from low to high, why the sound "
         "starts, the two kinds that keep time with your body, and which "
         "signs mean you should see a doctor.",
    url=URL,
    summary="What tinnitus is, the five sounds people describe (ringing, "
            "hissing or whistling, buzzing or humming, roaring, clicking or "
            "popping), why the sound most often starts in the inner ear, why "
            "a normal hearing test does not rule it out, the two kinds that "
            "keep time with the body (a click with the jaw, a beat with the "
            "pulse), and the red flags.",
    tags=["what does tinnitus sound like", "tinnitus sounds",
          "is tinnitus ringing or buzzing", "types of tinnitus sounds",
          "tinnitus hissing", "tinnitus buzzing", "pulsatile tinnitus",
          "tinnitus clicking", "tinnitus", "ringing in ears"],
    cta=f"The full article, with every cause, what a professional check "
        f"involves and the full list of red flags: {URL}",
    credits=["This video is general information, not medical advice. If your "
             "tinnitus pulses with your heartbeat, is in one ear only, came "
             "on suddenly or after a head injury, or comes with dizziness, "
             "hearing loss or ear pain, please see a doctor."],
)


def thumbs(out: Path) -> Path:
    """The user's pick (2026-10-28): a man on the floor against a white wall,
    a paper-cup phone at his ear, its string running in from the left. Cut to
    16:9 from the left edge, so the string leads from the headline to the
    cup; three dark rows on the plain wall to his left, under the string -
    the wall is light enough to take near-black type without a ramp
    (`thumb._headline`, `text=`)."""
    from PIL import Image
    from video_automation.longform import thumb as T
    src = Image.open(THUMB_PHOTO).convert("RGB")
    w, h = src.size
    # The left 88%, from just under the ceiling: he fills more of the frame
    # and sits right of centre; only the soles of his shoes are lost.
    cw = int(w * 0.88)
    y0 = int(h * 0.20)
    im = src.crop((0, y0, cw, y0 + cw * 9 // 16)).resize((1280, 720), Image.LANCZOS)
    fill, ink = T.ACCENTS["red"]
    # 365 wide: forced rows widen the column by 1.38x (`thumbnails.md`), and
    # his raised arm starts at x=540.
    T._headline(im, THUMB_HEADLINE, 240, 365, 40, fill, ink, max_lines=3,
                leading=1.02, band="middle", margin=36, shadow=11,
                drop=(5, 6), text=(20, 20, 20))
    im.save(out, quality=92)
    return out


def main() -> None:
    out = Path.home() / "Desktop/what-does-tinnitus-sound-like-long.mp4"
    work = Path.home() / "Desktop/.what-does-tinnitus-sound-like-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=16.0, title_hold=5.0,
        # The long form's title is the search, so the opener types it.
        opener=Search("what does tinnitus sound like"),
        emphasis=["five", "normal", "heartbeat"],
        thumb_headline=THUMB_HEADLINE, thumb_image=THUMB_PHOTO,
        thumb_accent="red",
    )
    made["thumb"] = thumbs(Path(made["thumb"]))
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        print(thumbs(Path.home()
                     / "Desktop/what-does-tinnitus-sound-like-long-thumb.jpg"))
    else:
        main()
