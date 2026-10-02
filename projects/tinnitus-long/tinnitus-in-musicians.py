"""Why do so many musicians have tinnitus? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/tinnitus-in-musicians.mdx.

**Why this post.** "Why do musicians get tinnitus" is a phrase people type,
the article carries a 2026 meta-analysis with a real proportion in it
(42.6% against 13.2%), and the names in its table are the rare case where
this channel can be specific about people rather than about a mechanism -
`narration.md`'s "a named entity beats a vague claim", available for once.

**The beats, and why these five.** The last three scripts on this channel
ran `anatomy`/`checklist`/`chapter`/`steps`/`grid` (tmj),
`diagram`/`compare`/`callout`/`steps`/`grid` (neck) and
`diagram`/`dial`/`steps`/`grid`/`compare` (explain). So `steps`, `compare`
and `diagram` are out on rotation, and three of the five here have not been
drawn on this channel in the last three videos at all:

- `stat` - the weight of the evidence (28,000 musicians, 67 studies). The
  figure *is* the point, which is the one case `stat` is right for, and
  `count=False` because a mid-animation "12,000 musicians" reads as a fact.
- `bars` - 42.6% against 13.2%. A proportion is the one thing narration
  cannot say, and `beats.md` lists `bars` as under-used at nine.
- `gauge` - decibels against safe exposure, which the project doc calls the
  commonest claim this site makes. `frac`/`threshold` are *positions*: the
  scale is drawn 70-120 dB, not 0-120.
- `chapter` - the turn, full screen.
- `grid` - the four musicians, named. It repeats from tmj and that is
  deliberate: a set of different named things is what `grid` is, and no
  other shape in the library draws four names without implying a verdict
  (`checklist`), an order (`steps`) or a side (`compare`).

The red flags do not get a sixth beat - they ride as a `payload` statement
over a clip, which is the project doc's own answer for this.

**Footage is the act, not the emotion.** Hands on a guitar neck, a mic, a
mixing desk, a lit stage from the floor, a corridor with a guitar case. No
ear close-ups, and no portrait of somebody suffering. Every clip was
contact-sheeted at three points across its length.

**Three "earplug" folders in the cache are a crushed chilli, a bursting
water balloon and a lit match** - `earplugs-in-hand-dark/19286012`,
`silicone-earplug-macro-black-background/855709` and
`earplugs-in-hand-dark/10602563`, all of which pass the luma box. Pexels has
no musician earplug, the same way it has no ASIC farm, so the protection
section is carried by the narration and by hands on real equipment rather
than by a fetch that keeps returning props.

**The medical line.** Nothing is diagnosed and nothing is promised. Hearing
protection is described as what lowers the dose, never as relief; the one
routing line ("still there after about a week - get a hearing test") and the
annual test are both the article's own, and nothing was added to them.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/tinnitus-in-musicians.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Counter

SOURCE_POST = "tinnitus-in-musicians"

V = STOCK / "videos"
# Contact-sheeted at 12/45/80% of each clip; duration and luma in the comment.
# Every id was checked against the other projects' rosters first - nothing
# here is spent elsewhere (`footage.md`, "An asset used in another video").
SINGER = V / "singer-microphone-live-concert-dark/4142312.mp4"              # 21.0s, L10-13, a singer close on a mic, near black
GUITAR = V / "guitarist-live-concert-dark-stage/15348443.mp4"               # 19.8s, L6, hands working a guitar neck, very dark
CROWD = V / "concert-crowd-night-stage-lights/13082773.mp4"                 # 25.0s, L20-38, the stage seen from the floor
BAND = V / "band-rehearsal-room-dark/8513516.mp4"                           # 19.0s, L40, a band playing under magenta light
DJ = V / "dj-headphones-booth-night/30896727.mp4"                           # 15.0s, L21-26, a DJ at the decks, warm
ORCH = V / "orchestra-rehearsal-dark-hall/37569621.mp4"                     # 13.0s, L42-45, violins in rehearsal. The brightest
                                                                           # clip in the roster, and it is here because the
                                                                           # classical line needs the classical picture.
PRODUCER = V / "music-producer-studio-headphones-night-dark/6892729.mp4"    # 27.0s, L38-40, headphones at a mic in a warm room
CORRIDOR = V / "guitar-case-corridor-night-dark/35130887.mp4"               # 16.0s, L18-26, a guitar case down a dim corridor
BED = V / "man-sitting-bed-night-awake-dark-room/30285721.mp4"              # 32.0s, L19-20, awake in bed with a phone
EMPTY = V / "backstage-corridor-concert-night-dark/7598737.mp4"             # 10.0s, L11-12, an empty corridor, one shot throughout
BACKSTAGE = V / "backstage-corridor-concert-night-dark/7901217.mp4"         # 15.0s, L27-34, a smoke-lit corridor backstage
DESK = V / "sound-engineer-mixing-desk-concert/13968826.mp4"                # 7.6s, L18, hands on a lit digital console
FADERS = V / "hands-on-mixing-console-faders-dark/12213084.mp4"             # 8.0s, L14-18, one hand over a mixing desk
MONITOR = V / "microphone-studio-dark-low-key/4962188.mp4"                  # 10.0s, L39, a studio monitor, a session on screen
SEATS = V / "empty-conference-stage-dark/7984190.mp4"                       # 22.1s, L8, an empty auditorium, one person in it
AUDIENCE = V / "concert-crowd-stage-lights-dark/28833086.mp4"               # 10.2s, L19-40, a seated audience, blue-lit stage
PIANO = V / "piano-player-low-light-dark/5706964.mp4"                       # 40.0s, L16-24, hands on a keyboard. **Both uses sit
                                                                           # past 14s**: the clip opens green-lit, which is the one
                                                                           # hue that cuts worst against peach, and turns blue.
AWAKE = V / "man-sitting-bed-night-awake-dark-room/6944078.mp4"             # 15.0s, L24-35, awake in bed, warm lamp
ENDCARD = V / "subscribe/4928934.mp4"

# **Four clips were cut on the sheet and none of them by a number.**
# `drummer-concert-stage-lights-dark/9737883` is a drummer so far off in a
# forest that two thirds of the frame is black with no subject in it;
# `dj-booth-nightclub-dark/2498731` is an unreadable green column;
# `tour-bus-night-window-musician/36147810` is a Las Vegas casino street,
# not a tour bus; `empty-stage-after-show-night/8515272` screens at L60 and
# is a lit conference riser.

# The thumbnail source, portrait and the same file for both aspects
# (`thumbnails.md`). A drummer mid-strike: whole subject, face lit, real
# dark either side for the type - and a person is the right ground here
# because the video's subject *is* people.
THUMB_PHOTO = STOCK / "photos/drummer-playing-dark-portrait/15324096.jpg"   # 8000x10000, L23/S25

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/tinnitus-in-musicians"


SECTIONS = [
    # --- hook: the question, then the figure the Counter is spinning to ----
    Section(
        title="Why so many musicians",
        card=False,
        sentences=[
            # Subject named in sentence one.
            ("Why do so many musicians end up with tinnitus?",),
            # The opener lands on "forty-three" here. It is a fact, not a
            # scene - `longform.md`, "a pattern interrupt has to be a fact,
            # a number or a reversal" - and it does not close the loop,
            # because the video is about why and about what to do next.
            ("Pool sixty-seven studies together,",
             "and it is about forty-three percent of them."),
            ("For everybody else, it is about thirteen.",),
            ("And the part that surprises musicians is where the dose comes "
             "from -",
             "not the big shows,",
             "but the rehearsals, the sound checks and the practice hours "
             "nobody counts."),
            ("By the end you will know where the dose really comes from, "
             "what protects a working musician's hearing, and when ringing "
             "after a show needs a hearing test.",),
        ],
        shots=[
            Shot(clip=SINGER, clip_at=0.5),
            None,                                   # hold the singer
            Shot(clip=CROWD, clip_at=1.0),
            Shot(clip=BAND, clip_at=0.5),
            Shot(clip=CORRIDOR, clip_at=1.0),
        ],
        gaps=[0.90, 0.85, 0.90, 0.80, 0.85],
    ),

    # --- how well established is that number -------------------------------
    Section(
        title="How common is it, really?",
        spoken_title="So how common is it, really?",
        sentences=[
            ("That figure is not one survey of one orchestra.",),
            # stat - the weight of the evidence. count=False: a partial
            # "12,000 musicians" is a plausible wrong fact, not a loading
            # state (`beats.md`).
            ("A review published this year pooled more than twenty-eight "
             "thousand of them.",),
            ("And the proportions it found look like this.",),
            # bars - two caption chunks, one per row.
            ("Musicians, about forty-three percent reporting tinnitus.",
             "People who are not musicians, about thirteen."),
            ("Roughly three times the rate, with more hearing loss behind "
             "it.",),
            ("And it was not only the loud genres -",
             "the classical players came out about the same as the rock and "
             "pop ones."),
        ],
        shots=[
            Shot(clip=PRODUCER, clip_at=1.0),
            Shot(graphic="stat",
                 payload=("28,000", "MUSICIANS POOLED",
                          "Across 67 studies, in one 2026 review.", False)),
            Shot(clip=GUITAR, clip_at=0.5),
            Shot(graphic="bars",
                 payload=([("Musicians", 0.85, "42.6%"),
                           ("Everybody else", 0.26, "13.2%")],
                          "WHO REPORTS TINNITUS")),
            Shot(clip=CROWD, clip_at=13.0),
            Shot(clip=ORCH, clip_at=0.5),
        ],
        gaps=[0.80, 0.90, 0.85, 1.00, 0.85, 0.90],
    ),

    # --- why the job does it ------------------------------------------------
    Section(
        title="Why does the job do this?",
        spoken_title="But why does the job itself do this?",
        sentences=[
            ("Three things stack up, and only the first one is obvious.",),
            # gauge - limit first, value second, as the beat's two reveals
            # require. The track is drawn 70-120 decibels, so `frac` and
            # `threshold` are positions on that scale rather than raw
            # numbers divided by anything.
            ("Safe listening sits around eighty-five decibels.",
             "A loud show runs past a hundred, and parts of an orchestra "
             "peak between a hundred and a hundred and twenty."),
            ("The second is time.",),
            ("A show is two hours; a career is thousands of them, and the "
             "dose is cumulative.",),
            ("The third is the only one anybody chooses:",
             "the protection gets left out, because plugs are supposed to "
             "ruin the sound."),
        ],
        shots=[
            Shot(clip=BAND, clip_at=10.0),
            Shot(graphic="gauge",
                 payload=("105 dB", 0.70, "a loud show", 0.30,
                          "85 dB, safe for long exposure",
                          "HOW LOUD IS THE JOB?")),
            Shot(clip=MONITOR, clip_at=0.5),
            Shot(clip=DESK, clip_at=0.0),
            Shot(clip=FADERS, clip_at=0.0),
        ],
        gaps=[0.85, 1.00, 0.70, 0.85, 0.90],
    ),

    # --- the turn, full screen ----------------------------------------------
    Section(
        title="One thing worth being clear about",
        card=False,
        sentences=[
            ("So before the gear, one thing worth being clear about.",),
            # chapter - the statement the section built to. It burns no
            # caption; the spoken half is this sentence.
            ("The sound is the job. The dose is the choice.",),
            ("You cannot turn the music down to nothing and still do the "
             "work -",
             "but how much of it reaches your ears is something you can put "
             "your hands on."),
        ],
        shots=[
            Shot(clip=EMPTY, clip_at=0.5),
            Shot(graphic="chapter",
                 payload=("THE SOUND IS THE JOB.\nTHE DOSE IS THE CHOICE.",)),
            Shot(clip=BACKSTAGE, clip_at=0.5),
        ],
        gaps=[0.85, 1.30, 0.90],
    ),

    # --- the names -----------------------------------------------------------
    Section(
        title="Who else is in this room?",
        spoken_title="And who else is in this room?",
        sentences=[
            ("If it has already happened to you, you are in very large "
             "company.",),
            # grid - one caption chunk per card, each one a sentence a
            # person would say rather than a name read off a list.
            ("Pete Townshend of The Who has spoken for years about severe "
             "tinnitus and hearing loss.",
             "Chris Martin of Coldplay says he has had it since early in "
             "his career.",
             "Lars Ulrich of Metallica talks about it from behind the drum "
             "kit.",
             "And Eric Clapton has described tinnitus and hearing loss as "
             "part of what the work cost him."),
            ("Sting, Phil Collins, Neil Young and Ozzy Osbourne have all "
             "said the same thing publicly.",),
            ("And nearly every one of them went public for one reason:",
             "to tell the people coming up behind them to protect it "
             "early."),
        ],
        shots=[
            Shot(clip=SINGER, clip_at=11.0),
            Shot(graphic="grid",
                 payload=([("Pete Townshend", "The Who", "\U0001F3B8"),
                           ("Chris Martin", "Coldplay", "\U0001F3A4"),
                           ("Lars Ulrich", "Metallica", "\U0001F941"),
                           ("Eric Clapton", "guitar", "\U0001F3B5")],
                          "ON THE RECORD")),
            Shot(clip=DJ, clip_at=0.5),
            Shot(clip=CORRIDOR, clip_at=8.0),
        ],
        gaps=[0.85, 1.00, 0.85, 0.90],
    ),

    # --- what actually protects it -------------------------------------------
    Section(
        title="What actually protects a musician's hearing?",
        spoken_title="So what actually protects a working musician's "
                     "hearing?",
        sentences=[
            ("Mostly not the foam plugs from the chemist.",),
            ("Foam takes the high frequencies down first,",
             "so the mix goes muddy, and the plugs come straight back out."),
            ("Musician earplugs lower the whole thing evenly instead.",),
            ("The high fidelity ones, or a custom pair moulded by an "
             "audiologist.",),
            ("The music still sounds like music. Quieter.",),
            ("In-ear monitors do the same job from the other side:",
             "a clean mix at a level you set, rather than a wall of stage "
             "volume to shout over."),
            ("And for ordinary headphone listening there is the sixty "
             "sixty rule:",
             "sixty percent of the volume, sixty minutes, then a break."),
            ("None of that is a treatment, and none of it undoes anything.",),
            ("It is how the dose stays smaller for the next twenty years of "
             "playing.",),
        ],
        shots=[
            Shot(clip=AUDIENCE, clip_at=0.5),
            Shot(clip=GUITAR, clip_at=10.0),
            Shot(clip=FADERS, clip_at=2.0),
            Shot(clip=AWAKE, clip_at=6.0),
            Shot(clip=DESK, clip_at=3.0),
            Shot(clip=PIANO, clip_at=14.0),
            Shot(clip=PRODUCER, clip_at=12.0),
            Shot(clip=BACKSTAGE, clip_at=8.0),
            Shot(clip=BED, clip_at=1.0),
        ],
        gaps=[0.85, 0.80, 0.60, 0.85, 0.90, 0.85, 0.90, 0.85, 0.90],
    ),

    # --- when ringing is more than a loud night ------------------------------
    Section(
        title="When does ringing need a hearing test?",
        spoken_title="But when does ringing after a show need a hearing "
                     "test?",
        sentences=[
            ("Ringing and muffled hearing straight after a loud night "
             "usually settle within hours to a couple of days.",),
            # The one on-screen routing line. `payload` is a repair, not a
            # default - this is the medical rule's "put it on screen", and
            # it is the only labelled clip in the video.
            ("Ringing still there after about a week, or after loud night "
             "following loud night, is more likely to be lasting.",),
            ("That one is worth a hearing test rather than another "
             "weekend.",),
            ("And if you play regularly, get one once a year anyway.",),
        ],
        shots=[
            Shot(clip=AWAKE, clip_at=0.5),
            Shot(clip=PIANO, clip_at=28.0,
                 payload=("", "Still there after a week? Get a hearing "
                              "test.")),
            Shot(clip=MONITOR, clip_at=5.0),
            Shot(clip=AUDIENCE, clip_at=5.0),
        ],
        gaps=[0.85, 1.00, 0.85, 0.90],
    ),

    # --- close: echo the opening, then the question --------------------------
    Section(
        title="Loud job, long hours, one choice",
        sentences=[
            ("So, back to why it is so many.",),
            ("Not because musicians have weaker ears.",),
            ("Because the job is loud, the hours are long, and only one "
             "part of that is optional.",),
            ("So,",
             "what would it take to put the plugs in at the next rehearsal, "
             "rather than at the next big show?"),
        ],
        shots=[
            Shot(clip=ORCH, clip_at=6.0),
            Shot(clip=DJ, clip_at=7.0),
            Shot(clip=BED, clip_at=14.0),
            Shot(clip=SEATS, clip_at=2.0),
        ],
        gaps=[0.85, 0.80, 0.90, 3.00],
    ),
]

META = Meta(
    title="Why Do So Many Musicians Have Tinnitus?",
    hook="Pooling 67 studies and more than 28,000 musicians, a 2026 review "
         "found tinnitus in about 42.6% of musicians against 13.2% of "
         "non-musicians - roughly three times the rate, and about the same "
         "for classical players as for rock and pop. Here is where the dose "
         "actually comes from, the musicians who have spoken about it, what "
         "protects hearing without ruining the sound, and when ringing "
         "after a show is worth a hearing test.",
    url=URL,
    summary="The 2026 meta-analysis behind the 42.6% figure, why volume, "
            "cumulative hours and skipped protection stack up on this one "
            "job, the musicians who have spoken publicly about tinnitus "
            "(Pete Townshend, Chris Martin, Lars Ulrich, Eric Clapton, "
            "Sting, Phil Collins, Neil Young, Ozzy Osbourne), why foam "
            "plugs get taken out and what high-fidelity earplugs and "
            "in-ear monitors do differently, the 60/60 rule, and when "
            "post-gig ringing is worth a hearing test.",
    tags=["tinnitus in musicians", "why do musicians get tinnitus",
          "musicians hearing loss", "musician earplugs", "in ear monitors",
          "hearing protection for musicians", "tinnitus", "ringing in ears"],
    cta=f"Full article, with the protection options: {URL}",
    credits=["Footage: Pexels (Pexels licence, no attribution required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. "
             "Ringing or muffled hearing that lasts more than about a week "
             "after loud exposure, or that follows repeated loud nights, is "
             "worth a hearing test. Musicians are advised to have their "
             "hearing checked once a year."],
)


def main() -> None:
    out = Path.home() / "Desktop/tinnitus-in-musicians-long.mp4"
    work = Path.home() / "Desktop/.tinnitus-in-musicians-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
        # **The opener rotates.** The last three on this channel were
        # `Search`, `hook` and `hook`. `Counter` is the one the shape of
        # this topic asks for - the payoff genuinely is a figure - and it
        # lands on "forty-three" as the voice says it in sentence two.
        opener=Counter("42.6%", "of musicians", at_word="forty-three"),
        # The thumbnail asks the title's own question and answers nothing.
        # One accent word, which is what the narrow landscape column needs.
        thumb_headline="Why do so many musicians have [tinnitus?]",
        thumb_image=THUMB_PHOTO, thumb_accent="red",
        # **Panelled, not cropped.** The source is 8000x10000, so a 1280x720
        # cover crop takes a thin band across it and cuts the drummer's head
        # in half - which the vertical cover does not do, and `thumbnails.md`
        # requires the two to show the same whole face. `crop_zoom` below 1.0
        # sets the picture on black instead of covering the frame.
        thumb_crop_at=(0.70, 0.10), thumb_crop_zoom=0.55, thumb_side="left",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
