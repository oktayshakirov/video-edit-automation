"""Why does tinnitus spike - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/why-does-tinnitus-spike.mdx.

**Why this post.** The title is the exact phrase people type into YouTube at
2am, and the honest answer is counterintuitive and reassuring: a spike is a
stress response in the auditory system turning its own gain up, not new
damage, and it is almost always several small triggers stacking rather than
one. That gives the long form its arc - name the fear, reframe it, walk the
mechanism, then hand over a routine for the first ten minutes of a spike.

**Beat variety, chosen before the script** (silhouette rule): `stat` (how
long the bigger spikes last), `grid` (the trigger groups, with icons),
`steps` (the five-step routine, with icons), `compare` with `name_columns`
(a spike vs real damage). No two carded sections share an outline.

**The medical line.** Nothing here promises relief or a cure. The routine is
described as calming the nervous system, which is what the article says it
does - never as a treatment. The close routes to a doctor and puts the
article's own red flags on screen as a statement card. No initialisms are
spoken.

**Footage.** Fresh topic, so its own stock roster - the channel's popular
clips are already recycled across six videos. The two site images for this
topic are bright (why-does-tinnitus-spike.jpg L180, stress-tinnitus-man.jpg
L186), so only the `stat`'s picture column uses one, where it is a downscale.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/why-does-tinnitus-spike.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

# Screened with `stock.screen` across each clip and then watched. The trailing
# comment is the luma range; a folder note flags why a clip was chosen.
FACE_M = STOCK / "videos/man-portrait-dark-moody-serious-european"   # L21-34, low-key
FACE_M2 = STOCK / "videos/serious-man-portrait-low-key-dark-studio"  # same man, close bookend
FACE_W = STOCK / "videos/blonde-woman-portrait-dark-moody-serious"   # 8512365, warm wall
THINK_W = STOCK / "videos/woman-thinking-question-dark-portrait"     # 8724510, sage/grey
DECISION_M = STOCK / "videos/man-sitting-alone-thinking-dark-room-decision"  # 8458662
MIXER = STOCK / "videos/audio-mixer-volume-fader-dark-studio"        # 37050520, dark desk
KNOB = STOCK / "videos/hand-turning-volume-knob-dark"                # 12213088, L17
ANXIOUS = STOCK / "videos/anxious-woman-sitting-dark-room-night"     # 7279039, restless, purple
TRAIN = STOCK / "videos/tired-man-commuting-train-night-window"      # 36244106, L20 dark windows
WALK = STOCK / "videos/man-walking-city-night-alone"                 # 16407855, hooded, bokeh
AWAKE_M = STOCK / "videos/young-man-lying-awake-dark-bedroom-night-white"  # 6943537, amber
NOTES = STOCK / "videos/writing-notes-notebook-desk-dark"            # 5212605 / 854162
QUIET_ROOM = STOCK / "videos/empty-quiet-room-dark-interior"         # 2845962, bare room
MEDITATE = STOCK / "videos/woman-meditating-dark-room-candle"        # 7191271 / 7265749
OFFICE = STOCK / "videos/man-working-computer-dark-office-night"     # 8311535, glow at night
WNM = STOCK / "videos/white-noise-machine-bedroom-night"             # 7505575
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                       # same reader as the channel's other pairs. Candidate.
MUSIC = music.track("night-drift")  # the prepared track, not a generated preset

URL = "https://tinnitushelp.me/blog/why-does-tinnitus-spike"
A = 16 / 9


SECTIONS = [
    # --- hook: name tinnitus in sentence one -----------------------------
    Section(
        title="Some days it roars",
        card=False,
        sentences=[
            ("Some days, your tinnitus is a faint hiss.",
             "Some days, it roars."),
            ("That sharp jump has a name.",
             "It is a spike."),
            ("It can follow a loud night, a bad sleep, a stressful week,",
             "or what feels like nothing at all."),
            ("You are not back to square one,",
             "and it is almost certainly not new damage."),
            ("Stay with this and you will know why spikes happen,",
             "and what to do in the first ten minutes of one."),
        ],
        shots=[
            Shot(clip=FACE_M / "30617205.mp4"),
            Shot(clip=ANXIOUS / "7279039.mp4"),
            Shot(clip=TRAIN / "36244106.mp4"),
            # Title stamp on the promise line, not the opening frame.
            Shot(clip=MIXER / "37050520.mp4",
                 payload=("", "WHY DOES TINNITUS SPIKE?")),
            Shot(clip=FACE_W / "8512365.mp4"),
        ],
        gaps=[0.55, 0.60, 0.55, 0.85, 0.45],
    ),

    # --- what a spike is, so `stat` -------------------------------------
    Section(
        title="So what is a spike, exactly?",
        spoken_title="So what is a spike, exactly?",
        sentences=[
            ("A spike is a short-term rise in how loud, sharp, "
             "or intrusive your tinnitus feels.",),
            ("It often follows a trigger,",
             "though the trigger can be hours, or even a day, behind it."),
            ("Most spikes fade within hours to a few days.",),
            ("Some of the bigger ones, after a loud event or an illness,",
             "can last one to three weeks."),
            ("Almost all of them are reversible.",),
        ],
        shots=[
            Shot(clip=THINK_W / "8724510.mp4"),
            Shot(clip=DECISION_M / "8458662.mp4"),
            None,
            Shot(graphic="stat",
                 payload=("1-3 weeks", "THE LONGER SPIKES",
                          "Most settle in days, not weeks."),
                 picture=IMG / "why-does-tinnitus-spike.jpg"),
            Shot(clip=MEDITATE / "7191271.mp4"),
        ],
        gaps=[0.34, 0.60, 0.45, 0.55, 0.80],
    ),

    # --- the mechanism, the twist: gain + stacking ----------------------
    Section(
        title="Why does it spike when nothing happened?",
        spoken_title="Now, the part that trips people up. "
                     "Why does it spike when nothing happened?",
        sentences=[
            ("There are two reasons, and neither one is damage.",),
            ("First, your hearing system runs on high alert,",
             "and it turns up its own internal gain "
             "the moment it senses stress or threat."),
            ("Louder background, louder tinnitus.",),
            ("Second, triggers stack.",),
            ("One rough night does not do it.",
             "Three rough nights, a skipped meal, "
             "and a noisy commute together might."),
            ("That is also why the cause is so hard to spot,",
             "the spike you notice on Tuesday "
             "may have started with lost sleep on Sunday."),
        ],
        shots=[
            # Second, far-apart use of the hook's closing face - not THINK_W
            # again, which would be two uses of one shoot inside a minute.
            Shot(clip=FACE_W / "8512365.mp4", clip_at=4.0),
            Shot(clip=KNOB / "12213088.mp4"),
            None,
            Shot(clip=WALK / "16407855.mp4",
                 note=("~24 hrs", "how far a spike can lag its trigger")),
            Shot(clip=AWAKE_M / "6943537.mp4"),
            Shot(clip=NOTES / "5212605.mp4"),
        ],
        gaps=[0.70, 0.34, 0.55, 0.80, 0.55, 0.85],
    ),

    # --- the triggers, so `grid` --------------------------------------
    Section(
        title="So what actually sets it off?",
        spoken_title="So what actually sets it off?",
        sentences=[
            ("The common triggers fall into a handful of groups.",),
            ("Loud noise, or sudden total silence.",
             "Stress, which tightens your neck and jaw.",
             "Broken sleep.",
             "Caffeine, alcohol, or salty food, if you are sensitive.",
             "A blocked ear, from wax or a cold."),
            ("Most spikes are two or three of these at once, not one.",),
        ],
        shots=[
            Shot(clip=QUIET_ROOM / "2845962.mp4"),
            Shot(graphic="grid",
                 payload=([("Loud noise, or silence",
                            "Both push the brain to raise gain", "\U0001F4E2"),
                           ("Stress and anxiety",
                            "Tighter neck and jaw, higher alertness",
                            "\U0001F630"),
                           ("Broken sleep",
                            "Less resilience, louder perception", "\U0001F319"),
                           ("Caffeine, alcohol, salt",
                            "Personal, not universal", "\U0001F964"),
                           ("A blocked ear",
                            "Wax, a cold, a pressure change", "\U0001F927")],
                          "WHAT SETS A SPIKE OFF")),
            Shot(clip=TRAIN / "36244106.mp4"),
        ],
        gaps=[0.55, 0.34, 0.70],
    ),

    # --- the routine, so `steps` -------------------------------------
    Section(
        title="A spike just hit. What do you do?",
        spoken_title="Right. A spike just hit. What do you actually do?",
        sentences=[
            ("Here is the whole routine, and it is five steps, in order.",),
            ("Name it a flare-up, not a setback, "
             "which on its own lowers the alarm.",
             "Slow your breathing, in for four and out for six, "
             "for a few minutes.",
             "Add quiet sound, a fan or soft noise, "
             "kept just below your tinnitus, not loud enough to bury it.",
             "Loosen your jaw and your shoulders.",
             "Then go do something absorbing, "
             "so you stop monitoring the sound."),
            ("Most of that is calming your nervous system,",
             "which is the thing driving the volume up."),
        ],
        shots=[
            Shot(clip=MEDITATE / "7265749.mp4"),
            Shot(graphic="steps",
                 payload=([("Name it a flare-up", "\U0001F3F7️"),
                           ("Slow the breathing", "\U0001FAC1"),
                           ("Add quiet sound, not silence", "\U0001F30A"),
                           ("Loosen jaw and shoulders", "\U0001F486"),
                           ("Do something absorbing", "\U0001F9E9")],
                          "THE FIRST TEN MINUTES")),
            # Same shoot as the hinge shot, later in the clip - reads as
            # "after the routine" rather than a static repeat.
            Shot(clip=MEDITATE / "7265749.mp4", clip_at=8.0),
        ],
        gaps=[0.34, 0.34, 0.60],
    ),

    # --- the fear underneath, so `compare` --------------------------
    Section(
        title="Is a spike damaging your hearing?",
        spoken_title="One more thing, because it is the fear underneath all "
                     "of this. Is a spike damaging your hearing? "
                     "Compare a spike with real damage.",
        sentences=[
            ("Take a spike first.",
             "It comes and then goes.",
             "It is a stress response, not an injury.",
             "And your hearing tests stay stable.",
             "Now compare that with real damage.",
             "It does not just reverse.",
             "It usually follows a clear, loud cause.",
             "And it shows up when your hearing is tested."),
            ("If a spike will not settle after a few weeks, "
             "or it only ever hits one ear,",
             "get it checked, not because a spike is dangerous, "
             "but because that pattern is worth ruling out."),
        ],
        shots=[
            Shot(graphic="compare",
                 payload=("A spike",
                          ["It comes and then goes",
                           "A stress response, not an injury",
                           "Hearing tests stay stable"],
                          "Real damage",
                          ["It does not just reverse",
                           "Usually a clear, loud cause",
                           "Shows up on a hearing test"],
                          True)),
            Shot(clip=OFFICE / "8311535.mp4"),
        ],
        gaps=[0.34, 0.85],
    ),

    # --- close: the echo, then the red flags ------------------------
    Section(
        title="So the next time it spikes",
        sentences=[
            ("So the next time your tinnitus climbs for no obvious reason:",),
            ("It is a flare-up, not a setback.",),
            ("It is triggers stacking up, not your ears breaking.",),
            ("Slow your breathing, keep gentle sound around you, "
             "and protect tonight's sleep.",),
            ("Spikes usually fade on their own,",
             "and bracing against them tends to make them "
             "feel louder for longer."),
            ("If yours is new, one-sided, pulsing with your heartbeat, "
             "or comes with hearing loss or dizziness,",
             "see a doctor first."),
            ("And if this helped,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(clip=NOTES / "854162.mp4"),
            None,
            Shot(clip=MIXER / "37050520.mp4", clip_at=2.0),
            Shot(clip=WNM / "7505575.mp4", clip_at=0.5),
            Shot(clip=MEDITATE / "7191271.mp4", clip_at=6.0),
            # The red flags on screen, which the medical rule requires.
            Shot(clip=DECISION_M / "8458662.mp4", clip_at=14.0,
                 payload=("SEE A DOCTOR IF",
                          "It is new, one-sided, pulses with your heartbeat, "
                          "or comes with hearing loss or dizziness.")),
            Shot(clip=FACE_M2 / "30617207.mp4"),
        ],
        gaps=[0.70, 0.55, 0.55, 0.60, 0.80, 0.34, 3.20],
    ),
]

META = Meta(
    title="Why Does Tinnitus Spike?",
    hook="Some days your tinnitus is a faint hiss. Some days it roars. A "
         "spike is almost never new damage - here is what is actually "
         "happening, and what to do in the first ten minutes of one.",
    url=URL,
    summary="What a tinnitus spike is and how long one lasts, why the "
            "hearing system turns its own gain up under stress, how triggers "
            "stack so the cause is delayed and hard to spot, the common "
            "trigger groups, a five-step routine for the first ten minutes, "
            "and why a spike is not the same as hearing damage.",
    tags=["tinnitus", "tinnitus spike", "tinnitus flare up", "why does "
          "tinnitus get louder", "ringing in ears louder", "tinnitus "
          "worse today"],
    cta=f"Full article and sources: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: night-drift.",
             "",
             "This video is general information, not medical advice. If "
             "your tinnitus is new, persistent, in one ear only, pulses "
             "with your heartbeat, or comes with hearing loss or dizziness, "
             "see a doctor or audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-spike-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-spike-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # Large dark stock portrait, direct gaze. Same image and headline as
        # the Short, per the standing pairing rule. The type is placed by
        # hand top-left over her forehead and hair - a manual `crop_at`
        # (which bypasses the scorer) so `side` and `crop_band` take effect;
        # `ay=0.15` keeps the accent plate clear of her eyebrows so every
        # facial feature stays visible.
        thumb_headline="Why does tinnitus [spike?]",
        thumb_image=STOCK / "photos"
        / "woman-pressing-temples-headache-stress-dark-background"
        / "4865631.jpg",
        thumb_accent="red",
        thumb_side="left",
        thumb_crop_at=(0.5, 0.15),
        thumb_crop_band="top",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
