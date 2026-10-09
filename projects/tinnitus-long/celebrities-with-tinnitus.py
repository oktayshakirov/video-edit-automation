"""Celebrities with tinnitus - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/celebrities-with-tinnitus.mdx.

**Why this post.** "Celebrities with tinnitus" is the phrase people type, and
the user asked for it with real names and real photographs - which on a
channel whose subject cannot be photographed is the rare case where the
picture can say the noun exactly. The photographs are Wikimedia Commons,
public domain or CC BY / BY-SA, credited in
`assets/tinnitus/celebrities/CREDITS.md` and in `Meta.credits`.

**Not the musicians again.** `tinnitus-in-musicians` already put Townshend,
Chris Martin, Ulrich and Clapton on a `grid`, so this video is built on the
four stories that are *not* about a loud career: Kirk and Spock (one
explosion, one ear each), Steve Martin (a gunfight scene), Neil Young (the
one musician, because his story is about what he did next) and Barbra
Streisand (a classroom, no noise at all). The rock stars get one line.

**Fact-checked, not copied.** The article hedges several of its own claims.
What survived the check is in `CREDITS.md`; the two changes that matter here:
Streisand is "as a child", not the article's "around age seven", and
Letterman, Butler, Kiedis and Cher are out. Shatner's account of suicidal
thoughts is left out on purpose - true, and the wrong thing to hand a
frightened viewer inside a roundup.

**The beats, and why these.** The last three scripts ran
`stat`/`bars`/`gauge`/`chapter`/`grid` (musicians),
`anatomy`/`checklist`/`chapter`/`steps`/`grid` (tmj) and
`diagram`/`compare`/`callout`/`steps`/`grid` (neck). So no `grid`, `steps`,
`chapter` or `bars`:

- `callout` - the 1968 Kirk and Spock still, a label on each side, each one
  level with the ear it names. Nimoy's right ear is on the viewer's left;
  Shatner's left ear is on the viewer's right. The picture literally shows
  the noun.
- `quote` - Steve Martin's "You just get used to it.", his photograph in the
  picture column.
- `diagram` - Neil Young's chain: a loud tour and a loud mix, then sound
  sensitivity, then the ringing. Not a loop; a sequence with "therefore".
- `checklist` - "WAS IT NOISE?" over the four stories, `flow=True` because
  the narration says each verdict, with Streisand's portrait beside it, the
  one where the answer is no.

**Opener: `Search`.** `Flash` shipped on the first cut and was cut on
review: it showed Kirk and Spock as "later in this video" and sentence two
said it outright five seconds later, so the tease spoiled itself. The title
already is the phrase people type, which is what `Search` is for.

**And the names, at the end.** The user asked for the rest of the list as
names only, so the video closes on a `grid` of nine - each checked against a
public account (CREDITS.md). It is the one `grid` in the cut and the reason
the rotation rule above bends.

**The medical line.** Nothing is promised. "You just get used to it" is
quoted as one man's experience and immediately called that - not a promise,
and for Shatner it took decades. Shatner's sound therapy and counselling are
described as what he did, not what they do for anyone. The routing line is
the article's own (a child's tinnitus is worth an early check) plus the
channel's standing "new ringing - get it checked".

**Phonemes.** espeak reads Nimoy as NIM-oy and Streisand as STRAY-sand, so
the spoken half respells both (`es()` below). "Habituated" has no respelling
that comes out right, so the voice says "used to it" and never the word.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/celebrities-with-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "celebrities-with-tinnitus"

ROOT = Path(__file__).resolve().parents[2]
CELEB = ROOT / "assets/tinnitus/celebrities"
# Wikimedia Commons, credited in CREDITS.md. Every still is used once.
KIRK_SPOCK = CELEB / "kirk-spock-1968.jpg"              # 1507x1911 portrait, PD - the thumbnail
KIRK_SPOCK_WIDE = CELEB / "kirk-spock-1968-wide.jpg"    # 1507x848, the callout and the flash
SHATNER_NIMOY = CELEB / "shatner-nimoy-2009.jpg"        # 3840x2560, L61, both laughing - the close
NIMOY_SALUTE = CELEB / "nimoy-salute-2011.jpg"          # 3840x2560, L15, the Vulcan salute on stage
STEVE_MARTIN = CELEB / "steve-martin-banjo-2017.jpg"    # portrait, L111 - picture column only
NEIL_YOUNG = CELEB / "neil-young-2012.jpg"              # 3296x2418, L27, electric guitar on stage
STREISAND = CELEB / "streisand-1966.jpg"                # portrait, L141 - picture column only
STREISAND_CLOSE = CELEB / "streisand-close.jpg"         # 2527x1893, L49, close and smiling - her section
PECK_STREISAND = CELEB / "peck-streisand-1969.jpg"      # 1600x1279, L74, PD, the Golden Globes - the hook
SHATNER_TALK = CELEB / "shatner-on-stage-talking.jpg"  # 3840x2560, L33, on stage, mid-sentence
SHATNER_SMILE = CELEB / "shatner-on-stage-smiling.jpg"  # 3840x2560, L25, smiling with a mic

V = STOCK / "videos"
# Contact-sheeted at 12/45/80% of each clip; duration and luma in the comment.
# None of these ids is in another project's roster.
TV = V / "vintage-television-static-dark-room/11999587.mp4"              # 12s, L13-29, an old set in a dark room
TVS = V / "vintage-television-static-dark-room/6955102.mp4"              # 13s, L32-34, a wall of old sets
FILMSET = V / "movie-studio-lights-camera-crew-dark/36604687.mp4"        # 8s, L13-14, a film set, lights and crew
FILMSET2 = V / "film-set-behind-the-scenes-night/14367163.mp4"           # 10s, L40-42, a crew on a lit stage
BLAST = V / "special-effects-explosion-film-set/17807763.mp4"            # 6s, L3-23, a fireball on black
PROJECTOR = V / "old-film-projector-dark/5434505.mp4"                    # 15s, L4-15, an old projector's lens, dark
# `old-film-projector-dark/3223854` was cut on the first render: a frame of
# film in the gate reads as a flat brown rectangle at 16:9.
COWBOY = V / "western-cowboy-silhouette-sunset/26624668.mp4"             # 6s, L82-92, a rider at sunset. Bright,
                                                                         # and here because the line is a western
MIC = V / "stand-up-comedian-microphone-spotlight/8513955.mp4"           # 13s, L63-67, a mic under a spotlight
SEATS = V / "theater-audience-applause-dark/7986777.mp4"                 # 18s, L20-30, an audience in red seats
STAGE = V / "guitar-amplifier-stage-loud-concert/8513956.mp4"            # 18s, L28-38, a guitarist on a dark stage
CONSOLE = V / "sound-engineer-mixing-console-dark/7586172.mp4"           # 13s, L26-32, an engineer at a desk
ACOUSTIC = V / "acoustic-guitar-playing-dark/5686177.mp4"                # 13s, L27-30, hands on an acoustic neck
CORRIDOR = V / "school-hallway-dark-empty/19217895.mp4"                  # 10s, L25-28, an empty dark corridor
# Cut on review (2026-10-09): the phone's white screen, the man putting
# headphones on (read as a gamer) and the woman at the window all said
# nothing about the person the line was about; the child at a desk did not
# read as Streisand. Real photographs of the people replaced most of them.
KNOB = V / "hand-turning-volume-knob-dark/12213088.mp4"                  # 10s, L15-17, a hand turning a desk knob
SPEAKER = V / "speaker-playing-sound-nightstand-dark/37349230.mp4"       # 6s, L13-20, a speaker playing by candlelight
COUNSEL = V / "therapist-counseling-session-hands/7200765.mp4"           # 19s, L90-101, hands and a notebook in a
                                                                         # session. Bright; every result was
PARENT = V / "white-noise-machine-bedroom-night/7505432.mp4"             # 12s, L77-79, a mother and daughter on a bed
WALK = V / "man-walking-alone-night-street-lamp/11839713.mp4"            # 27s, L38-41, a man walking under lamps
WALK2 = V / "man-walking-alone-night-street-lamp/11839716.mp4"           # 16s, L21-22, lamps, a figure far off
VINYL = V / "vinyl-record-player-spinning-dark/19281032.mp4"               # 22s, L17-22, a record spinning, dark deck
EVENT = V / "speaker-at-podium-microphone-dark-stage/19197406.mp4"          # 26s, L67-80, a big event stage, soft focus
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/celebrities-with-tinnitus"

# espeak gets both surnames wrong (NIM-oy, STRAY-sand). Respell in the spoken
# half only; the captions keep the real spelling.
_RESPELL = {"Nimoy": "Neemoy", "Streisand": "Strysand", "Ulrich": "Ulrick",
            "Gallagher": "Gallaher", "will.i.am": "Will I Am"}


def es(text: str) -> tuple[str, str] | str:
    spoken = text
    for k, v in _RESPELL.items():
        spoken = spoken.replace(k, v)
    return text if spoken == text else (text, spoken)


def S(*chunks: str) -> tuple:
    return tuple(es(c) for c in chunks)


SECTIONS = [
    # --- hook ---------------------------------------------------------------
    Section(
        title="Celebrities with tinnitus",
        card=False,
        sentences=[
            # Subject named in sentence one, under ten words.
            S("Which celebrities have tinnitus, and how did they get it?"),
            # The partial answer: a name and a fact, true on its own, and it
            # opens the bigger question of what happened next.
            # Names the actors, not only the characters: not everybody has
            # watched Star Trek (the user's note on the first cut).
            S("Start with the strangest one.",
              "Two Star Trek actors, the men who played Kirk and Spock, got "
              "theirs on the same day."),
            S("The rock stars are only part of the story."),
            S("A comedian got his on a film set."),
            S("A singer has had hers since she was a child, with no loud "
              "noise anywhere near it."),
            # The retention promise. Paid off in the checklist section.
            S("By the end, you will know which of these causes you can do "
              "something about, and which one you cannot."),
        ],
        shots=[
            Shot(clip=TV, clip_at=0.5),
            Shot(clip=FILMSET, clip_at=0.0),
            Shot(clip=STAGE, clip_at=1.0),
            Shot(clip=MIC, clip_at=0.5),
            Shot(image=PECK_STREISAND, zoom=1.08, pan=(0.0, -0.01)),
            Shot(clip=SEATS, clip_at=1.0),
        ],
        gaps=[0.85, 0.90, 0.60, 0.55, 0.85, 0.90],
    ),

    # --- Kirk and Spock -----------------------------------------------------
    Section(
        title="How did Kirk and Spock get it?",
        spoken_title="So how did Kirk and Spock both end up with it?",
        sentences=[
            S("It was nineteen sixty-seven, and they were filming an episode "
              "of Star Trek."),
            # Its own sentence: the fireball burns out to black after about
            # three seconds, and the first render held it for six.
            S("A special-effects explosion went off close to them."),
            S("Both men walked away with ringing in their ears."),
            # The hinge into the callout - said, then shown.
            S("And the same blast landed on each of them differently."),
            # callout - one caption chunk per label, in the order the labels
            # are placed: Nimoy on the viewer's left, Shatner on the right.
            S("Leonard Nimoy's tinnitus was in his right ear.",
              "William Shatner's is in his left."),
            S("For both of them, it never really went away.",
              "Nimoy lived with it for the rest of his life."),
        ],
        shots=[
            Shot(clip=PROJECTOR, clip_at=0.5),
            Shot(clip=BLAST, clip_at=0.0),
            Shot(clip=TVS, clip_at=0.5),
            None,                                       # hold the wall of sets
            Shot(graphic="callout",
                 # Read off the crop: Spock's ear sits about 27% down the
                 # frame on the left, Kirk's about 46% down on the right.
                 payload=(KIRK_SPOCK_WIDE,
                          [("Nimoy: right ear", 0.0, 0.27),
                           ("Shatner: left ear", 1.0, 0.46)],
                          "ONE EXPLOSION, TWO EARS")),
            Shot(image=NIMOY_SALUTE, zoom=1.08, pan=(0.02, 0.0)),
        ],
        gaps=[0.60, 0.55, 0.80, 0.80, 1.10, 0.90],
    ),

    # --- what Shatner did ---------------------------------------------------
    Section(
        title="What did Shatner do about it?",
        spoken_title="So what did William Shatner do about it?",
        sentences=[
            S("He has called the years that followed a long run of ups and "
              "downs."),
            S("Eventually he went looking for help, and found the American "
              "Tinnitus Association."),
            # Split so each noun gets its own picture: the counselling, then
            # the sound.
            S("What he took up was sound therapy and counselling."),
            S("It is an approach built around getting used to the sound, "
              "rather than removing it."),
            S("Today he describes himself not as cured, but as used to it."),
            S("And he has spent years speaking up for tinnitus research."),
        ],
        shots=[
            Shot(clip=WALK, clip_at=1.0),
            Shot(image=SHATNER_TALK, zoom=1.08, pan=(0.02, 0.0)),
            Shot(clip=COUNSEL, clip_at=1.0),
            # 2.0s in: the clip opens on a dark foreground blur sliding past.
            Shot(clip=SPEAKER, clip_at=2.0),
            Shot(image=SHATNER_SMILE, zoom=1.08, pan=(-0.02, 0.0)),
            Shot(clip=EVENT, clip_at=2.0),
        ],
        gaps=[0.70, 0.80, 0.60, 0.90, 1.00, 0.90],
    ),

    # --- Steve Martin -------------------------------------------------------
    Section(
        title="What happened to Steve Martin?",
        spoken_title="And what happened to Steve Martin?",
        sentences=[
            S("In nineteen eighty-six he was filming the western comedy Three "
              "Amigos."),
            S("He has said the ringing started during a gunfight scene,",
              "and it never left."),
            # The hinge into the quote.
            S("Ask him how he lives with it, and his answer is short."),
            # quote - the beat's own sentence is the quotation.
            S("You just get used to it."),
            S("It is the same thing Shatner says, from a man who has had it "
              "for about forty years."),
            # The honesty line, said straight after the quote so it cannot
            # be read as a promise.
            S("That is their experience, not a promise,",
              "and for Shatner, getting there took decades."),
        ],
        shots=[
            Shot(clip=COWBOY, clip_at=0.5),
            Shot(clip=FILMSET2, clip_at=0.5),
            Shot(clip=MIC, clip_at=6.0),
            Shot(graphic="quote",
                 payload=("You just get used to it.", "STEVE MARTIN"),
                 picture=STEVE_MARTIN),
            Shot(clip=SEATS, clip_at=10.0),
            Shot(clip=WALK2, clip_at=1.0),
        ],
        gaps=[0.60, 0.85, 0.90, 1.20, 0.80, 0.90],
    ),

    # --- Neil Young ---------------------------------------------------------
    Section(
        title="Why did Neil Young go quiet?",
        spoken_title="So why did Neil Young suddenly go quiet?",
        sentences=[
            S("In nineteen ninety-one, Neil Young toured one of the loudest "
              "shows of his career."),
            S("Then he mixed the live album from it, called Weld,",
              "and has said he hurt his ears doing it."),
            S("What followed came in that order."),
            # diagram - one caption chunk per node.
            S("A loud tour and a loud mix,",
              "then everyday sound that felt far too loud,",
              "and then the ringing."),
            S("So the next album he made was a quiet one,",
              "Harvest Moon, because he did not want to hear anything "
              "loud."),
            S("Decades on, he says he still has mild tinnitus,",
              "and his hearing is not perfect, but okay."),
        ],
        shots=[
            Shot(image=NEIL_YOUNG, zoom=1.10, pan=(-0.02, 0.0)),
            Shot(clip=CONSOLE, clip_at=0.5),
            Shot(clip=STAGE, clip_at=9.0),
            Shot(graphic="diagram",
                 payload=([("A loud tour", "and a loud mix", "\U0001F3B8"),
                           ("Sound too loud", "everyday noise hurt",
                            "\U0001F4A5"),
                           ("Tinnitus", "and it stayed", "\U0001F514")],
                          "HOW DID IT HAPPEN?", False)),
            Shot(clip=VINYL, clip_at=0.5),
            Shot(clip=ACOUSTIC, clip_at=0.5),
        ],
        gaps=[0.60, 0.85, 0.80, 1.00, 0.85, 0.90],
    ),

    # --- Streisand, and the four lined up ----------------------------------
    Section(
        title="What if there was no loud noise at all?",
        spoken_title="But what if there was no loud noise at all?",
        sentences=[
            S("Barbra Streisand has said hers started when she was a child, "
              "sitting in a classroom."),
            S("No concert. No explosion. Nothing anybody could point to."),
            # The hinge into the checklist.
            S("So line the four stories up, and ask one question of each."),
            # checklist, flow=True - the narration says each verdict.
            S("The explosion on set was noise.",
              "So was the gunfire.",
              "So was the tour.",
              "The classroom was not."),
            # The retention promise, paid.
            S("Three of the four came from noise,",
              "and noise is the one cause you can actually turn down."),
            S("The fourth is the reminder that not every case has a cause "
              "you can find."),
            S("That is exactly when it is worth getting checked, especially "
              "in a child."),
        ],
        shots=[
            Shot(image=STREISAND_CLOSE, zoom=1.08, pan=(0.02, 0.0)),
            Shot(clip=CORRIDOR, clip_at=0.5),
            None,                                       # hold the corridor
            Shot(graphic="checklist",
                 payload=([("An explosion on set", True),
                           ("Gunfire on set", True),
                           ("A loud tour", True),
                           ("A classroom", False)],
                          "WAS IT NOISE?", True),
                 picture=STREISAND),
            Shot(clip=KNOB, clip_at=0.5),
            # Static: a signal with no source anybody can point to.
            Shot(clip=TV, clip_at=6.0),
            # The one labelled clip in the video: the routing line on screen.
            Shot(clip=PARENT, clip_at=0.5,
                 payload=("", "New ringing? Get your hearing checked.")),
        ],
        gaps=[0.85, 0.90, 0.80, 1.20, 0.85, 0.60, 0.90],
    ),

    # --- close: echo the opening, then the question --------------------------
    Section(
        title="Back to Kirk and Spock",
        spoken_title="So, back to Kirk and Spock.",
        sentences=[
            S("One explosion, nearly sixty years ago, and two of the most "
              "famous faces on television have carried it ever since."),
            S("Three of the four stories you just heard began with a loud "
              "noise,",
              "and only one of them began in a quiet room."),
        ],
        shots=[
            Shot(image=SHATNER_NIMOY, zoom=1.08, pan=(0.0, -0.01)),
            Shot(clip=WALK, clip_at=12.0),
        ],
        gaps=[0.85, 0.90],
    ),

    # --- the rest of the list, names only (the user's call on the first cut) -
    # Every name checked against a public account of their own tinnitus;
    # Sting, Hetfield and Moby were left off as only second-hand. See
    # assets/tinnitus/celebrities/CREDITS.md.
    Section(
        title="Who else has tinnitus?",
        spoken_title="And there are more celebrities known to have tinnitus.",
        sentences=[
            # grid - one caption chunk per card, names only.
            S("Pete Townshend,", "Chris Martin,", "Lars Ulrich,", "Eric Clapton,", "Phil Collins,", "Ozzy Osbourne,", "Jeff Beck,", "Liam Gallagher,",
              "and will.i.am."),
            S("So,",
              "which of these stories sounded most like your own?"),
        ],
        shots=[
            Shot(graphic="grid",
                 payload=([("Pete Townshend", ""), ("Chris Martin", ""), ("Lars Ulrich", ""), ("Eric Clapton", ""), ("Phil Collins", ""), ("Ozzy Osbourne", ""), ("Jeff Beck", ""), ("Liam Gallagher", ""), ("will.i.am", "")],
                          "ALSO ON THE RECORD")),
            Shot(clip=WALK2, clip_at=8.0),
        ],
        gaps=[1.20, 3.00],
    ),
]

META = Meta(
    title="Celebrities With Tinnitus - and How Each of Them Got It",
    hook="William Shatner and Leonard Nimoy both got tinnitus from the same "
         "special-effects explosion while filming Star Trek in 1967 - one in "
         "the left ear, one in the right. Steve Martin got his filming a "
         "gunfight scene for Three Amigos. Neil Young's came from one of the "
         "loudest tours of his career, and changed the next album he made. "
         "And Barbra Streisand has had hers since she was a child, with no "
         "loud noise at all.",
    url=URL,
    summary="How Kirk and Spock got tinnitus on the same day, what William "
            "Shatner did about it (sound therapy, counselling and the "
            "American Tinnitus Association), Steve Martin's six-word answer "
            "to living with it, why Neil Young made Harvest Moon quiet, and "
            "why Barbra Streisand's childhood tinnitus is the one story "
            "without a loud noise in it.",
    tags=["celebrities with tinnitus", "famous people with tinnitus",
          "william shatner tinnitus", "leonard nimoy tinnitus",
          "steve martin tinnitus", "neil young tinnitus",
          "barbra streisand tinnitus", "star trek tinnitus", "tinnitus",
          "ringing in ears"],
    cta=f"The full list, from the article: {URL}",
    credits=["Photographs via Wikimedia Commons: Leonard Nimoy and William "
             "Shatner, NBC Television, public domain. Shatner and Nimoy at "
             "Dragon Con 2009 by Christopher Stadler, CC BY 2.0. Leonard "
             "Nimoy and William Shatner by Gage Skidmore, CC BY-SA 2.0. Steve "
             "Martin by Davidwbaker, CC BY-SA 4.0. Neil Young by Man Alive!, "
             "CC BY 2.0. Barbra Streisand by lifescript, CC BY 2.0; 1966 "
             "publicity photo and with Gregory Peck, 1969, public domain. This "
             "video is shared under CC BY-SA 4.0.",
             "Additional footage: Pexels (Pexels licence, no attribution "
             "required).",
             "Music: night-drift.",
             "",
             "This video is general information, not medical advice. Each "
             "person's experience is their own. New ringing, or ringing that "
             "has not settled, is worth a hearing check - and in a child, "
             "worth one early."],
)


def main() -> None:
    out = Path.home() / "Desktop/celebrities-with-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.celebrities-with-tinnitus-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        title_at=8.5, title_hold=5.4,
        # `Search`, not `Flash`: the flash showed Kirk and Spock as "later in
        # this video" and the voice then gave it away five seconds later, so
        # the tease spoiled itself (the user's note on the first cut). The
        # title already is the phrase people type.
        opener=Search("celebrities with tinnitus"),
        # The thumbnail asks the title's question about the two faces on it.
        # Portrait source, panelled beside the type rather than cropped
        # through, so both faces stay whole (`thumbnails.md`).
        # "Two Star Trek actors", not "Kirk and Spock": not everybody has
        # watched it (the user's note on the first cut).
        # Forced rows, so STAR TREK cannot split across two (it did).
        thumb_headline="How did two\nStar Trek actors\nget [tinnitus?]",
        thumb_image=KIRK_SPOCK, thumb_accent="red",
        thumb_crop_at=(0.80, 0.10), thumb_crop_zoom=0.62, thumb_side="left",
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
