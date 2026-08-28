"""Gaming and tinnitus — long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/the-gamers-guide-to-preventing-tinnitus.mdx.

**Why this post.** Second on the site's own demand ranking (351 views) and the
one page on it that is already a YouTube query — "gaming tinnitus", "is my
headset too loud" — asked by an audience that lives on the platform. It is also
the *safest* strong topic on the list: prevention and exposure limits, not
diagnosis, so almost nothing here needs hedging.

**Beat variety was chosen before the script was written**, per the crypto
skill's silhouette rule. `does-tinnitus-go-away` shipped with four checklists
and they read as one graphic; this uses each shape once — `quote`, `grid`,
`bars`, `stat`, `compare`, `steps`, one `checklist` — so no two beats have the
same outline. `bars` carries the piece: the decibel table is a *budget*, and a
budget is a proportion, which is the one thing narration cannot say.

**The medical line.** Everything factual is the article's own: the hair-cell
analogy, 85-91 decibels in a shooter, the 119 dB impulse peak, the exposure
table, the sixty-sixty rule, 10-25% of adults. Nothing promises that any of it
prevents or relieves anything — the playbook is described as what it is, and
the close routes to an audiologist. Disclaimer in `Meta.credits`.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/gaming-and-tinnitus.py

**Phonemes.** Avoided: `dB`, `ANC`, `SFX`, `CBT`, `TRT`, `WHO`, `NIHL` — every
one is an initialism espeak either mangles or reads as a word. The narration
says "decibels", "noise cancelling", "effects and music", "an audiologist".
Figures are spelled out rather than left as digits, which costs nothing and
removes the guesswork; the digits stay on screen where they read better.

**Pictures.** The site library is bright — screened, only `gamer` (L22),
`live-music-show` (L27) and `neurons` (L24) are dark enough to take the full
frame, so the rest sit in beat picture columns where they are downscaled. Six
stock clips were fetched and screened across their length; the gaming shelf is
mostly RGB neon and most of it failed on saturation.
"""

from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long

IMG = Path.home() / "Coding/tinnitus-blog/public/images"

# Screened with `stock.screen` at 0.5/3/6/9s; trailing comment is the range.
HEADSET = STOCK / "videos/gamer-headset-dark-room"
KEYB = STOCK / "videos/gaming-keyboard-hands-night"
CTRL = STOCK / "videos/video-game-controller-dark"
ESPORTS = STOCK / "videos/esports-player-computer-night"
PHONES = STOCK / "videos/young-man-headphones-listening-dark"
NEURONS = STOCK / "videos/brain-neurons-abstract-dark"
TIRED = STOCK / "videos/headache-stress-tired-woman-dark"
ENDCARD = STOCK / "videos/subscribe/4928934.mp4"

VOICE = "mia"                   # the article-video reader. `luna` is the
                                # sound-therapy voice and belongs to mode 2.
MUSIC = "bright"

URL = "https://tinnitushelp.me/blog/the-gamers-guide-to-preventing-tinnitus"
A = 16 / 9


SECTIONS = [
    # --- hook: the thing every one of them has done ----------------------
    Section(
        title="The footsteps",
        card=False,
        sentences=[
            ("You turned the volume up",
             "to hear the footsteps."),
            ("Everybody does.",),
            ("Then the session ends,",
             "the headset comes off,",
             "and your ears are ringing."),
            ("That ringing has a name.",
             "And it is not nothing."),
            # Split, because as one sentence this ran nine seconds on a single
            # still — and it sat at 10-20s, which is exactly where the
            # retention drop is steepest. A held photograph is the slowest
            # thing this format has and that is the worst place for it.
            ("By the end of this",
             "you will know how loud your headset actually is,",
             "and how long you can play at that level."),
            ("Plus the one audio setting",
             "that fixes the footstep problem",
             "without touching the volume."),
        ],
        shots=[
            # A face, moving, on frame one — the note from the first tinnitus
            # cut. This one reads as "gamer" in about a fifth of a second,
            # which no photograph in the library manages.
            Shot(clip=HEADSET / "9070656.mp4"),      # L32-38 S28-32
            None,
            Shot(clip=HEADSET / "10620277.mp4", clip_at=1.0),   # L18-22 S4-5
            # The title stamp, on the promise rather than the opening frame.
            Shot(clip=KEYB / "9071216.mp4",          # L41-54 S9-10
                 payload=("", "HOW LOUD IS TOO LOUD?")),
            Shot(image=IMG / "gamer.jpg", zoom=1.10, pan=(0.02, 0.01),
                 aspect=A, bias=0.45),
            Shot(clip=ESPORTS / "7915045.mp4"),      # L49-54 S20-26
        ],
    ),

    # --- reframe: the ringing is the report ------------------------------
    Section(
        title="The ringing is a report",
        spoken_title="First, the ringing is a report.",
        sentences=[
            ("Tinnitus is not a disease.",
             "It is a symptom."),
            ("Inside your ear",
             "sit thousands of microscopic hair cells",
             "that turn sound into signal."),
            ("Think of them as blades of grass.",
             "Ordinary sound is a breeze.",
             "Eight hours of loud audio",
             "is a boot."),
            ("Bent grass stands back up.",
             "Broken grass does not.",
             "Those cells do not grow back."),
            ("So the ringing after a long session",
             "is not the damage.",
             "It is your ears reporting it."),
        ],
        shots=[
            Shot(graphic="quote",
                 payload=("The ringing is not the damage. It is the report.",
                          "what tinnitus actually is"),
                 picture=IMG / "neurons.jpg"),
            Shot(clip=NEURONS / "29184317.mp4"),     # L26 S46
            None,
            Shot(image=IMG / "neurons.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.5),
            None,
        ],
    ),

    # --- why gaming specifically: a set, so `grid` -----------------------
    Section(
        title="Why gaming is a worse risk than a concert",
        spoken_title="So why is gaming worse than a concert?",
        sentences=[
            ("A concert is two hours",
             "and then it is over.",
             "A session can run eight.",
             "Three things stack up."),
            # One caption chunk per card, in card order, with no lead-in
            # inside the beat's own span — the `compare` rule, and `grid`
            # times its reveals the same way.
            ("How loud the game is.",
             "How long you sit in it.",
             "And headphones, which deliver all of it straight into the canal."),
            ("A shooter averages",
             "around ninety decibels",
             "for as long as you are in it."),
        ],
        shots=[
            Shot(clip=ESPORTS / "9071228.mp4"),      # L50-56 S13-17
            Shot(graphic="grid",
                 payload=([("Intensity", "85 to 91 decibels in a shooter"),
                           ("Duration", "Sessions of eight hours or more"),
                           ("Isolation", "Headphones put it in the ear canal")],
                          "THE PERFECT STORM")),
            Shot(clip=CTRL / "8128022.mp4"),         # L25-27 S21-24
        ],
    ),

    # --- the numbers: a budget, so `bars` --------------------------------
    Section(
        title="What your ears are rated for",
        spoken_title="So what are your ears actually rated for?",
        sentences=[
            ("Safe listening is not a matter of taste.",
             "It is a weekly budget,",
             "and it collapses fast."),
            ("Eighty decibels buys you forty hours.",
             "Eighty five, twelve and a half.",
             "Ninety two — an average shooter — two and a half.",
             "A loud concert, two and a half minutes."),
            ("And a gunshot in game",
             "can peak at a hundred and nineteen decibels."),
            ("That is not a session limit.",
             "That is a limit measured in seconds."),
        ],
        shots=[
            Shot(image=IMG / "live-music-show.jpg", zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="bars",
                 # Every fraction is hours-per-week over forty, times 0.9.
                 # A full-width top bar puts its own value text off the right
                 # edge — "40 ho" — and the value travels with the bar end, so
                 # there is nowhere else for it to go. Scaling the whole set
                 # by one factor leaves the proportions between them exact,
                 # which is the only thing this beat is claiming.
                 payload=([("80 dB · doorbell", 0.90, "40 hours"),
                           ("85 dB · heavy traffic", 0.28, "12h 30"),
                           ("92 dB · average shooter", 0.056, "2h 30"),
                           ("110 dB · loud concert", 0.009, "2.5 min")],
                          "SAFE TIME PER WEEK")),
            Shot(graphic="stat",
                 payload=("119", "DECIBEL PEAK",
                          "What an in-game gunshot can hit.")),
            None,
        ],
        # The stat is the line the section is built toward; buy it a beat.
        gaps=[0.34, 0.34, 0.34, 1.10],
    ),

    # --- the twist: it is a mixing problem -------------------------------
    Section(
        title="It is a mixing problem, not a volume problem",
        spoken_title="But here is the part nobody says out loud.",
        sentences=[
            ("You are not turning it up",
             "because you like it loud."),
            ("You are turning it up",
             "because footsteps are mixed almost silent",
             "and gunfire is mixed deafening."),
            ("So to hear the thing that wins the round,",
             "you swallow the thing that costs you your hearing."),
            ("That is a mixing problem.",
             "And a mixing problem has a mixing fix."),
            # Six chunks, one per compare item, left column then right.
            ("Footsteps too quiet to place.",
             "Gunshots peaking over a hundred.",
             "So you raise the master.",
             "With a compressor, footsteps lifted.",
             "Peaks held down.",
             "So the master comes back down."),
            ("A compressor narrows the gap",
             "between the quietest sound and the loudest one.",
             "You hear more,",
             "at less."),
        ],
        shots=[
            Shot(clip=KEYB / "9071216.mp4", clip_at=6.0),
            None,
            Shot(image=IMG / "girl-with-headphones2.jpg", zoom=1.10,
                 pan=(-0.02, 0.01), aspect=A, bias=0.45),
            None,
            Shot(graphic="compare",
                 payload=("Raw game audio",
                          ["Footsteps almost silent",
                           "Gunshots over 100 dB",
                           "So you raise the master"],
                          "With a compressor",
                          ["Footsteps lifted",
                           "Peaks held down",
                           "So the master drops"])),
            None,
        ],
    ),

    # --- the playbook: a procedure, so `steps` ---------------------------
    Section(
        title="The setup that costs you nothing",
        spoken_title="So what does the fix actually look like?",
        sentences=[
            ("Five changes, none of which cost you a single kill.",),
            ("Keep the master around sixty percent.",
             "Break every hour.",
             "Pull effects and music down, leave dialogue up.",
             "Add a compressor or a limiter.",
             "And use a closed-back headset with noise cancelling."),
            ("That last one is the quiet win.",
             "Less noise leaking in",
             "means less volume needed",
             "to hear the same detail."),
            ("And if you want a check with no meters:",
             "hold the headset at arm's length.",
             "If you can still hear it clearly,",
             "it is too loud."),
        ],
        shots=[
            Shot(image=IMG / "gamer.jpg", zoom=1.11, pan=(-0.02, -0.01),
                 aspect=A, bias=0.5),
            Shot(graphic="steps",
                 payload=(["Master at 60%",
                           "Break every hour",
                           "Effects down, dialogue up",
                           "Add a limiter",
                           "Closed-back, noise cancelling"],
                          "THE PLAYBOOK")),
            Shot(clip=ESPORTS / "7915045.mp4", clip_at=4.0),
            Shot(clip=PHONES / "7948198.mp4", clip_at=4.0,   # L42 S8
                 payload=("THE ARM'S LENGTH TEST",
                          "If you can still hear it, it is too loud.")),
        ],
    ),

    # --- if it already started -------------------------------------------
    Section(
        title="If the ringing is already there",
        spoken_title="And if the ringing is already there?",
        sentences=[
            ("Two things are worth knowing.",
             "It is common —",
             "somewhere between ten and twenty five percent of adults",
             "hear something."),
            ("And the ringing itself",
             "does not make you deaf.",
             "Carrying on at the same volume",
             "is what does the rest."),
            ("These are the ones to act on.",),
            ("It is new, or it will not settle.",
             "It is only in one ear.",
             "It came with hearing loss or dizziness.",
             "Or it is genuinely wearing you down."),
            ("Any of those",
             "is a reason to see an audiologist.",
             "Not to panic.",
             "To get the cause named."),
        ],
        shots=[
            Shot(clip=TIRED / "4588228.mp4"),           # L30-32 S14
            None,
            Shot(image=IMG / "musician.jpg", zoom=1.10, pan=(0.02, -0.01),
                 aspect=A, bias=0.45),
            Shot(graphic="checklist",
                 payload=([("New, or it will not settle", True),
                           ("Only in one ear", True),
                           ("With hearing loss or dizziness", True),
                           ("Wearing you down", True)],
                          "SEE A PROFESSIONAL IF",
                          True),                     # flow
                 picture=IMG / "audiologist.jpg"),
            Shot(image=IMG / "doctor.jpg", zoom=1.11, pan=(-0.02, 0.01),
                 aspect=A, bias=0.45),
        ],
    ),

    # --- close: the echo --------------------------------------------------
    Section(
        title="Stay in the game",
        spoken_title="So where does that leave your setup?",
        sentences=[
            ("Your reflexes are not the thing",
             "that ages out of this hobby.",
             "Your hearing is."),
            ("Master down.",
             "Dialogue up.",
             "Let the limiter do the shouting."),
            ("Because you turned it up",
             "to hear the footsteps.",
             "You can hear them at sixty percent instead."),
            ("If that was useful,",
             "subscribe for more videos like this one."),
        ],
        shots=[
            Shot(image=IMG / "girl-with-headphones2.jpg", zoom=1.10,
                 pan=(0.02, 0.01), aspect=A, bias=0.45),
            Shot(clip=CTRL / "8128022.mp4", clip_at=1.0),
            Shot(clip=HEADSET / "9070656.mp4", clip_at=4.0),
            Shot(clip=ESPORTS / "9071228.mp4", clip_at=8.0),
        ],
        gaps=[0.34, 0.34, 0.90, 3.20],
    ),
]

META = Meta(
    title="Gaming and Tinnitus: How Loud Is Too Loud?",
    hook="An average shooter runs at ninety decibels and an in-game gunshot "
         "peaks at a hundred and nineteen — here is what that buys you per "
         "week, and the audio setting that fixes the footstep problem without "
         "the volume.",
    url=URL,
    summary="Why gaming is a worse hearing risk than a concert, what the "
            "decibel budget actually looks like per week, why turning it up "
            "for footsteps is a mixing problem rather than a volume problem, "
            "and the five-step setup that costs you nothing competitively.",
    tags=["tinnitus", "gaming and tinnitus", "hearing loss gamers",
          "headset volume", "safe listening", "ringing in ears"],
    cta=f"Full guide, the decibel table and sources: {URL}",
    credits=["Additional footage: Pexels (Pexels licence, no attribution "
             "required).", "Music: generated for this channel.",
             "",
             "This video is general information, not medical advice. If your "
             "tinnitus is new, persistent, in one ear only, or comes with "
             "hearing loss or dizziness, see a doctor or audiologist."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-gaming-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-gaming-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # The title carries the search phrase, so the thumbnail asks what the
        # title does not.
        thumb_headline="Your headset is [too loud]",
        thumb_image=IMG / "gamer.jpg",
        thumb_accent="red",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
