"""Does caffeine make tinnitus worse? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/caffeine-and-tinnitus.mdx

**Why this post.** "Does caffeine make tinnitus worse" is a high-volume
evergreen search and the honest answer is counterintuitive: for most people
caffeine does not universally worsen tinnitus, and quitting it suddenly can
look exactly like proof that it did. The arc: kill the single-cause idea,
walk the adenosine / sleep / attention mechanism, spend a chapter on the
withdrawal trap, then hand over a two-week experiment and the red flags.

**Beat variety, chosen before the script** (silhouette rule): `quote` (the
context line), `stat` (the 5-6 hour half-life, `count=False`), `compare` with
`name_columns` (quit cold vs taper down), `bars` (caffeine per drink),
`steps` (the two-week test, with icons), `checklist` with `flow` (the red
flags). No two carded sections share an outline.

**The medical line.** Every claim is the article's own: caffeine acts on
arousal, stress hormones, sleep pressure and attention; individual response
varies; abrupt withdrawal brings headache, irritability and poor sleep;
taper 10-25% every 2-3 days; a commonly cited ceiling of 300-400 mg, many
feel best under 200. Nothing promises relief or a cure - caffeine is
described by what it *does*, never by what it will do for the viewer. The
close routes to a professional with the article's red flags on screen.
No initialisms spoken - "an ear specialist", "talking therapy".

**Footage.** Fresh dark roster plus the drawn beats. Every site image for
this post is medical/lifestyle stock shot bright (`anxiety.jpg` L159,
`stress-tinnitus-man.jpg` L186, the hero `caffeine-and-tinnitus.jpg` L85 and
only 700px), so nothing from the site library is dark enough to cut - the
pair is stock plus beats, the same call the pulsatile pair made.

**Phonemes.** `caffeine` -> `kˈafiːn`, `adenosine` -> `ɐdˈɛnəsiːn`,
`espresso`, `milligrams`, `tinnitus` all phonemize cleanly. No initialisms.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/caffeine-and-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

SOURCE_POST = "caffeine-and-tinnitus"

# Screened with `stock.screen` at 0.5/4/8/12s and then watched. Trailing
# comment is the luma range across the clip.
MUG_KITCHEN = STOCK / "videos/man-drinking-from-mug-dark-kitchen-morning"      # 35674404 19s L27-46
CONCERN_W = STOCK / "videos/close-up-woman-face-thinking-concerned-dark"       # 4584772 19s L60
PORT_M = STOCK / "videos/man-portrait-serious-low-light-dark-studio"          # 6415877 15s L14 (nothing else from this shoot ships)
THINK_M = STOCK / "videos/man-thinking-worried-dark-room-window"              # 7280528 18s L42
NECK_W = STOCK / "videos/woman-touching-her-neck-dark-portrait"               # 5387557 L10
BEANS = STOCK / "videos/coffee-beans-grinder-dark"                           # 32896425 20s L8
ENERGY = STOCK / "videos/energy-drink-can-dark"                              # 7033926 11s L15
CUP = STOCK / "videos/cup-of-coffee-morning-dark-moody"                      # 6950170 13s L53
DESK_PM = STOCK / "videos/woman-drinking-coffee-at-office-desk-evening-dark"  # 8100340 38s L35
HIGHWAY = STOCK / "videos/night-highway-traffic-long-exposure-dark"          # 4062948 22s L18-23
AWAKE = STOCK / "videos/person-lying-awake-in-bed-night-dark"                # 6943537 24s L42
RESTED = STOCK / "videos/person-relaxing-in-bed-propped-up-pillows-dark-bedroom"  # 7986968 L40
CALM_W = STOCK / "videos/woman-relaxing-calm-eyes-closed-dark"               # 5114850 L44 (first ~6s only)
WATER = STOCK / "videos/person-adding-water-to-coffee-glass-dark"            # 5542396 30s L50
WINDOW = STOCK / "videos/man-contemplating-window-night-city-dark"          # 4538212 16s L51
READCUP = STOCK / "videos/man-setting-down-coffee-mug-dark-table"           # 7062991 17s L71 (warm desk, reading with coffee)
OCEAN = STOCK / "videos/ocean-waves-dark-night-moody"                       # 11287848 20s L20
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

# Downscaled in the beat picture column - the luma ceiling bites less there.
PH_WDRINK = STOCK / "photos/woman-drinking-coffee-dark-background/37363589.jpg"   # L38
PH_MUG = STOCK / "photos/man-coffee-mug-dark-serious/32536421.jpg"                # L48

VOICE = "mia"                      # the explainer default, per the project doc
MUSIC = music.track("night-drift")  # the prepared track, shared with thecrypto.wiki

URL = "https://tinnitushelp.me/blog/caffeine-and-tinnitus"
A = 16 / 9


SECTIONS = [
    # --- hook: name the subject in sentence one -------------------------
    Section(
        title="The morning cup",
        card=False,
        sentences=[
            ("You had your usual coffee this morning.",),
            ("An hour later, the ringing in your ears got louder.",),
            ("So you blamed the coffee.",),
            ("But the next day, the same cup did nothing at all.",),
            ("By the end of this you will know whether caffeine is really "
             "your trigger,",
             "and how to test it",
             "without giving up coffee to find out."),
        ],
        shots=[
            Shot(clip=MUG_KITCHEN / "35674404.mp4", clip_at=2.0),
            Shot(clip=CONCERN_W / "4584772.mp4"),
            None,
            None,
            Shot(clip=BEANS / "32896425.mp4",
                 payload=("", "DOES CAFFEINE MAKE TINNITUS WORSE?")),
        ],
        gaps=[0.50, 0.60, 0.45, 0.90, 0.50],
    ),

    # --- reframe: no single answer, so `quote` ------------------------
    Section(
        title="Is caffeine the problem, or not?",
        spoken_title="So is caffeine the problem, or not?",
        sentences=[
            ("For most people, caffeine does not simply make tinnitus worse.",),
            ("Some do notice a clear spike after a strong coffee or an energy "
             "drink.",
             "Others feel worse on the days they try to quit."),
            ("Both of those things can be true.",),
            ("What decides it is rarely the caffeine on its own.",
             "It is your sleep, your stress, and where your attention already "
             "is."),
        ],
        shots=[
            Shot(clip=ENERGY / "7033926.mp4"),
            Shot(clip=THINK_M / "7280528.mp4"),
            None,
            Shot(graphic="quote",
                 payload=("It is rarely the caffeine alone. It is the context.",
                          "why the same cup feels different each day"),
                 picture=PH_WDRINK),
        ],
        gaps=[0.50, 0.55, 0.80, 0.60],
    ),

    # --- the mechanism -----------------------------------------------
    Section(
        title="What is caffeine actually doing?",
        spoken_title="So what is caffeine actually doing?",
        sentences=[
            ("Caffeine blocks a chemical called adenosine.",
             "Adenosine is the one that builds up sleep pressure and calms "
             "the nervous system down."),
            ("Block it, and you feel sharper, more awake, more focused.",),
            ("But if your brain is already on alert for the ringing,",
             "that sharper focus can land straight on the sound."),
            ("On a rested day, the same cup can do the opposite,",
             "and help you hold your attention somewhere else."),
        ],
        shots=[
            Shot(clip=CUP / "6950170.mp4",
                 payload=("", "Caffeine blocks a signal called adenosine")),
            Shot(clip=DESK_PM / "8100340.mp4",
                 payload=("", "Block it, and you feel wired")),
            Shot(clip=PORT_M / "6415877.mp4",
                 payload=("", "On alert, your attention finds the ringing")),
            Shot(clip=WINDOW / "4538212.mp4",
                 payload=("", "Rested, the same cup helps you look away")),
        ],
        gaps=[0.50, 0.55, 0.70, 0.60],
    ),

    # --- half-life + sleep, so `stat` -------------------------------
    Section(
        title="It does not leave when the cup is empty",
        spoken_title="And it does not leave when the cup is empty.",
        sentences=[
            ("Caffeine also lingers.",
             "Six hours after that afternoon coffee, half of it is still in "
             "you."),
            ("A cup at three in the afternoon is still working at nine at "
             "night.",),
            ("And broken sleep is one of the most reliable ways to make "
             "tinnitus louder the next day.",),
        ],
        shots=[
            Shot(graphic="stat",
                 payload=("5-6 hrs", "BEFORE HALF HAS CLEARED",
                          "An afternoon cup still works at bedtime.", False)),
            Shot(clip=HIGHWAY / "4062948.mp4",
                 payload=("", "A 3 p.m. coffee is still active at 9 p.m.")),
            Shot(clip=AWAKE / "6943537.mp4",
                 payload=("", "Lost sleep is the bigger trigger")),
        ],
        gaps=[0.50, 0.55, 0.80],
    ),

    # --- the withdrawal trap, so `compare` --------------------------
    Section(
        title="Why quitting can backfire",
        spoken_title="So why can quitting backfire?",
        sentences=[
            ("Stopping caffeine suddenly brings on headaches, poor sleep, and "
             "irritability for a few days.",),
            ("All three of those push tinnitus up on their own.",
             "So going cold turkey can look exactly like proof that caffeine "
             "was the problem."),
            ("Quit cold.",
             "A withdrawal headache.",
             "Worse sleep for days.",
             "A louder week that misleads you.",
             "Taper down instead.",
             "No rebound.",
             "Sleep stays protected.",
             "A clean read on your trigger."),
            ("If you do want to cut back, taper.",
             "Drop it by ten to twenty-five percent every two to three days."),
        ],
        shots=[
            Shot(clip=CUP / "6950170.mp4",
                 payload=("", "Withdrawal alone can raise the volume")),
            None,
            Shot(graphic="compare",
                 payload=("Quit cold",
                          ["A withdrawal headache",
                           "Worse sleep for days",
                           "A louder week that misleads you"],
                          "Taper down",
                          ["No rebound headache",
                           "Sleep stays protected",
                           "A clean read on your trigger"],
                          True)),
            Shot(clip=WATER / "5542396.mp4",
                 payload=("", "Cut by 10-25% every few days, never all at once")),
        ],
        gaps=[0.50, 0.70, 0.45, 0.80],
    ),

    # --- how much is in a drink, so `bars` --------------------------
    Section(
        title="What are you actually drinking?",
        spoken_title="So what are you actually drinking?",
        sentences=[
            ("It helps to know the numbers.",),
            ("An energy drink can run to two hundred milligrams.",
             "A mug of brewed coffee, around a hundred.",
             "A shot of espresso, about seventy.",
             "Black tea, roughly fifty.",
             "A cola, forty.",
             "Green tea, thirty."),
            ("Energy drinks and pre-workout are where people get caught out.",
             "It adds up across the whole day, not just at breakfast."),
        ],
        shots=[
            Shot(clip=DESK_PM / "8100340.mp4", clip_at=14.0,
                 payload=("", "Most adults sit fine under 200 mg a day")),
            # Fractions scaled by one factor so the value text on the top bar
            # does not travel off the right edge - the `bars` note in beats.md.
            Shot(graphic="bars",
                 payload=([("Energy drink", 0.62, "up to 200"),
                           ("Brewed coffee", 0.31, "100 mg"),
                           ("Espresso shot", 0.217, "70 mg"),
                           ("Black tea", 0.155, "50 mg"),
                           ("Cola", 0.124, "40 mg"),
                           ("Green tea", 0.093, "30 mg")],
                          "CAFFEINE, A TYPICAL SERVING")),
            Shot(clip=ENERGY / "7033926.mp4",
                 payload=("", "It adds up across the whole day")),
        ],
        gaps=[0.60, 0.50, 0.75],
    ),

    # --- the experiment, so `steps` --------------------------------
    Section(
        title="How to test your own caffeine window",
        spoken_title="So how do you test your own caffeine window?",
        sentences=[
            ("Run a two-week experiment instead of guessing.",),
            ("Log every drink, with the time, your sleep, and your ringing.",
             "Keep the amount the same, but move your last cup earlier.",
             "Only if you still suspect it, start tapering, slowly.",
             "Add a glass of water with every caffeinated drink.",
             "Judge it after two weeks, not after one bad night."),
            ("Most people find the fix is the timing, not the coffee itself.",),
        ],
        shots=[
            Shot(clip=MUG_KITCHEN / "35674404.mp4", clip_at=9.0,
                 payload=("", "Two weeks of notes beats one bad morning")),
            Shot(graphic="steps",
                 payload=([("Log drinks, sleep and ringing", "\U0001F4D2"),
                           ("Move the last cup earlier", "⏰"),
                           ("Only then taper, slowly", "\U0001F4C9"),
                           ("Water with every cup", "\U0001F4A7"),
                           ("Judge it after two weeks", "\U0001F4C5")],
                          "THE TWO-WEEK TEST")),
            Shot(clip=RESTED / "7986968.mp4",
                 payload=("", "Usually it is the timing, not the caffeine")),
        ],
        gaps=[0.60, 0.50, 0.80],
    ),

    # --- the red flags, so `checklist` with flow -------------------
    Section(
        title="When it is not about caffeine",
        spoken_title="But sometimes it is not about caffeine at all.",
        sentences=[
            ("Some tinnitus needs a doctor, not an experiment.",),
            ("It is new, and it is not settling.",
             "It is only in one ear.",
             "It pulses in time with your heartbeat.",
             "It comes with dizziness, or with hearing loss.",
             "It is keeping you awake night after night."),
            ("Any one of those,",
             "book an appointment with an ear specialist,",
             "to get the cause looked at."),
        ],
        shots=[
            Shot(clip=PORT_M / "6415877.mp4", clip_at=6.0),
            Shot(graphic="checklist",
                 payload=([("New, and not settling", True),
                           ("Only one ear", True),
                           ("Pulses with your heartbeat", True),
                           ("With dizziness or hearing loss", True),
                           ("Keeping you awake nightly", True)],
                          "SEE A PROFESSIONAL IF",
                          True),
                 picture=PH_MUG),
            Shot(clip=NECK_W / "5387557.mp4",
                 payload=("", "To identify the cause, not to panic")),
        ],
        gaps=[0.70, 1.20, 0.80],
    ),

    # --- close: echo the opening ----------------------------------
    Section(
        title="So where does that leave your coffee?",
        spoken_title="So where does that leave your coffee?",
        sentences=[
            ("If your ringing is steady and your sleep is solid, your usual "
             "coffee is probably fine.",),
            ("If you suspect it, do not quit overnight.",
             "Move it earlier, taper slowly, and watch the trend across "
             "weeks."),
            ("Because the question was never really caffeine, yes or no.",
             "It was how it sits with everything else in your day."),
            ("So tomorrow morning, same cup:",
             "is it the coffee, or the night before it?"),
        ],
        shots=[
            Shot(clip=CALM_W / "5114850.mp4"),
            Shot(clip=WATER / "5542396.mp4", clip_at=12.0),
            Shot(clip=READCUP / "7062991.mp4"),
            Shot(clip=OCEAN / "11287848.mp4"),
        ],
        gaps=[0.34, 0.55, 0.90, 2.60],
    ),
]

META = Meta(
    title="Does Caffeine Make Tinnitus Worse?",
    hook="For most people caffeine does not universally make tinnitus worse - "
         "and quitting it suddenly can look exactly like proof that it did. "
         "Here is what it actually does, and how to test your own window.",
    url=URL,
    summary="Why the same cup feels different each day, how caffeine acts on "
            "adenosine, sleep and attention, the withdrawal trap that fakes a "
            "trigger, how much is in common drinks, a two-week test, and the "
            "red flags that mean see a professional.",
    tags=["tinnitus", "caffeine and tinnitus", "does caffeine make tinnitus "
          "worse", "coffee and tinnitus", "tinnitus triggers",
          "ringing in ears"],
    cta=f"Full article, the dose table and sources: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: licensed for this channel.",
             "",
             "This video is general information, not medical advice. If your "
             "tinnitus is new, one-sided, pulsing with your heartbeat, "
             "worsening, or comes with dizziness or hearing loss, see a "
             "doctor or an ear specialist."],
)


def main() -> None:
    out = Path.home() / "Desktop/caffeine-and-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.caffeine-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, music_gain=1.0, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # Same source and headline as the Short. Subject sits in the right
        # third with a wall of night bokeh to his left, so the type goes left
        # and `shift` nudges him further right onto black.
        thumb_headline="Does caffeine make tinnitus [worse?]",
        thumb_image=PH_MUG,
        thumb_accent="orange",
        thumb_shift=0.12,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
