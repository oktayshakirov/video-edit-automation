"""Did Beethoven have tinnitus? - long-form 16:9 for YouTube.

Source: tinnitus-blog/content/posts/did-beethoven-have-tinnitus.mdx.

**The title is the search.** "Did Beethoven have tinnitus" is the phrase, so
the opener is `Search` typing it - the long form's title already *is* what
somebody types. The Short takes the teasing angle ("What did Beethoven hear,
day and night?"). Last three tinnitus pairs opened Stamp / Split / hook, and
the last `Search` was `tmj-and-tinnitus`, five pairs back.

**The spine.** A letter he asked a friend to keep secret, the cures his
doctors tried and his verdict on each, a quiet village that did not bring his
hearing back - and then the turn: a soundproof room in 1953 where 94% of
people with normal hearing heard a sound. The close echoes the opening: he
went looking for quiet to escape a sound he was carrying with him.

**Fact-checked against the sources, not the article.** Every quoted line is
Lady Wallace's 1866 translation (Project Gutenberg 13065), read in the text:
"buzzing and ringing perpetually, day and night", "I can distinguish the
tones, but not the words", "In any other profession this might be more
tolerable, but in mine such a condition is truly frightful", oil of almonds
"did me no good whatever", the Danube baths after which "my hearing remained
the same, or in fact rather got worse", the bark blisters and the ringing
"rather decreased, particularly in the left ear" while his hearing was "not
at all improved". The cold baths are left out: his letter dismisses the
doctor and never says whether he took them. Heller and Bergman (1953): 80
adults, 94%. Del Bo et al. (2008): 53 young adults, 83% in an empty chamber,
92% with a dummy loudspeaker.

**The Heiligenstadt Testament is told without its darkest line.** The letter
says he came close to ending his life. On a channel whose audience is often
distressed at two in the morning, the video says what the document is about
- how alone his deafness made him - routes the viewer to someone to talk to,
and does not quote the line.

**The beats.** The last three long forms ran `timeline`/`diagram`/`grid`/
`quote` (history), `dial`/`bars`/`diagram` (stress) and `diagram`/`steps`
(spike). Here:

- `post` as a **letter** - a new kind, built for this video: the real line
  on paper, the writer and recipient over a hairline, highlighted as read.
- `checklist`, flow - the cures, each struck as his verdict is said.
- `bars` - 94 / 83 / 92, the three rooms.
- `diagram` - a faint sound in silence, the brain filtering it, the filter
  letting it through. The article's own reframe, as a chain.
- `spotlight` - the Testament manuscript.

**The medical line.** Nothing here says what will help. The background-sound
line describes what clinicians suggest and why, from the article. The red
flags are the article's own (one ear, pulsing, a sudden drop in hearing), on
the notice card as the voice says them.

**Phonemes**, checked with espeak-ng: Beethoven, Bonn, Vienna, Danube,
Heller, Bergman, Morris, Moe are fine. Respelled in the spoken half only:
Wegeler (espeak: "WEDGE-uh-ler"), Heiligenstadt ("HY-ly-jen-stat") and the
years. "Anechoic" is never said - "soundproof room" is.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/did-beethoven-have-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section, render_long
from video_automation.longform.openers import Search

SOURCE_POST = "did-beethoven-have-tinnitus"

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "assets/tinnitus/beethoven"
# Wikimedia Commons, credited in CREDITS.md. Each still is used once, except
# the 1803 portrait, which is the letter card's avatar as well as an inset.
HORNEMANN = B / "hornemann-1803.jpg"        # 800x912, the closest portrait to 1801
MAHLER = B / "mahler-1804.jpg"              # 3840x4906, portrait - inset
STIELER = B / "stieler-1820.jpg"            # 3840x4779, the famous one - inset, thumbnail
TESTAMENT = B / "testament.jpg"             # 3840x6054, the manuscript - spotlight
WEGELER = B / "wegeler.jpg"                 # 283x305 - a small inset only
VILLAGE = B / "heiligenstadt-1821.jpg"      # 2168x1512, Raulino's watercolour - full frame
VALLEY = B / "heiligenstadt-19c.jpg"        # 3812x2951, Heiligenstadt and the Danube - full frame
CHAMBER = B / "anechoic-4.jpg"              # 3840x2880, the wedges of a soundproof room
CHAMBER_W = B / "anechoic-pano.jpg"         # 3840x1017, the whole room - full frame

V = STOCK / "videos"
# Fetched 2026-10-24, contact-sheeted at 5/35/65/95%. None of these ids is cut
# by another project. Duration, luma, what is in the frame.
PIANO_BW = V / "pianist-hands-piano-keys-dark/3822008.mp4"     # 31s, L18, a grand piano in black and white, a hand on the keys
PIANO = V / "pianist-hands-piano-keys-dark/15363847.mp4"       # 27s, L15, two hands playing, a dark coat
VIOLIN = V / "violin-player-dark-stage/7095850.mp4"            # 15s, L29-32, a violinist on a dark stage
STRINGS = V / "violin-player-dark-stage/7097482.mp4"           # 28s, L36-62, a string section; brighter after 12s
PAGES = V / "old-letter-candle-close-up/11530055.mp4"          # 21s, L32-37, hands turning old pages by a candle
CANDLES = V / "old-letter-candle-close-up/6032025.mp4"         # 11s, L37-48, a brass candelabra, wax running
WATER = V / "river-water-flowing-at-night-dark/4192175.mp4"    # 16s, L5-6, moonlight on moving water
TOWN = V / "river-at-night-old-town-lights/11466624.mp4"       # 31s, L35-37, an old town and its canal at night, aerial
ALONE = V / "person-sitting-alone-silent-dark-room/36623804.mp4"  # 23s, L6, a man seated alone, back to us, one lamp
FRIDGE = V / "refrigerator-kitchen-at-night/6898048.mp4"       # 31s, L22-65, a fridge opened in a dark kitchen
FLAME = V / "candle-blown-out-smoke-dark/4061908.mp4"          # 30s, L8-20, one candle flame; it goes out at ~19s
SMOKE = V / "candle-blown-out-smoke-dark/26885208.mp4"         # 4s, L4-7, smoke from a candle just put out
BARK = V / "tree-bark-texture-dark-moody/6250415.mp4"          # 30s, L16-18, dark tree bark and a fern
MOON = V / "moon-clouds-night-slow/5229463.mp4"                # 24s, L5-8, the moon behind moving cloud
ENDCARD = V / "subscribe/4928934.mp4"

VOICE = "noah"          # the noah test, pair 1 of 5 (`projects/tinnitus.md`)
MUSIC = music.track("night-drift")

URL = "https://tinnitushelp.me/blog/did-beethoven-have-tinnitus"

# espeak reads a four-digit year as "one thousand eight hundred...", Wegeler
# as "WEDGE-uh-ler" and Heiligenstadt as "HY-ly-jen-stat". Respell in the
# spoken half only; the SRT keeps the real spelling.
_RESPELL = {"1801": "eighteen oh one", "1802": "eighteen oh two",
            "1953": "nineteen fifty-three", "2008": "two thousand and eight",
            "Wegeler": "Vay gheler", "Heiligenstadt": "Hyliggenshtaht"}


def es(text: str) -> tuple[str, str] | str:
    spoken = text
    for k, v in _RESPELL.items():
        spoken = spoken.replace(k, v)
    return text if spoken == text else (text, spoken)


def S(*chunks: str) -> tuple:
    return tuple(es(c) for c in chunks)


LETTER = {"name": "Ludwig van Beethoven", "to": "to Franz Wegeler",
          "date": "Vienna, 29 June 1801", "avatar": str(HORNEMANN),
          "text": "I certainly do feel better and stronger, but my ears are "
                  "[buzzing and ringing perpetually, day and night.]"}


SECTIONS = [
    # --- hook ---------------------------------------------------------------
    Section(
        title="Did Beethoven have tinnitus?",
        card=False,
        sentences=[
            # The Search opener types this as it is said.
            S("Did Beethoven have tinnitus?"),
            # Yes - and the reason to stay is how we know.
            S("He did, and he described it himself, in a letter he asked a "
              "friend to keep secret."),
            S("He was thirty, already famous, and his ears were ringing day "
              "and night."),
            # The retention promise - paid off in the letter card, the cures
            # and the soundproof room, and echoed in the close.
            S("By the end, you will know what he wrote, what his doctors "
              "tried, and what a silent room revealed about the sound he "
              "heard."),
        ],
        shots=[
            Shot(clip=PIANO_BW, clip_at=0.5),
            # Past 4s: before it, the turning page is a legible title page of
            # somebody else's book.
            Shot(clip=PAGES, clip_at=5.0),
            Shot(clip=CANDLES, clip_at=0.5, inset=(HORNEMANN, "right", 0.24)),
            # The title rides here. Its own clip: the candelabra is 11s and
            # could not hold both sentences.
            Shot(clip=VIOLIN, clip_at=1.0),
        ],
        gaps=[0.70, 0.60, 0.80, 0.90],
    ),

    # --- the letter ---------------------------------------------------------
    Section(
        title="Who did he tell?",
        spoken_title="So who did he tell?",
        kicker="THE SECRET",
        sentences=[
            S("Franz Wegeler, a doctor who had known him since they were boys "
              "in Bonn."),
            S("In June 1801, Beethoven wrote to him from Vienna: his hearing "
              "had been failing for three years."),
            S("He heard none of the high notes of the orchestra, and in "
              "conversation he could make out the tones, but not the words."),
            S("For two years he had avoided company, because he could not "
              "bring himself to say he was deaf."),
            # Wallace's wording, near enough to quote: "In any other
            # profession this might be more tolerable, but in mine such a
            # condition is truly frightful."
            S("In any other profession, he wrote, this might be more "
              "tolerable, but in mine it is truly frightful."),
        ],
        shots=[
            Shot(clip=TOWN, clip_at=2.0, inset=(WEGELER, "right", 0.15)),
            Shot(clip=FLAME, clip_at=1.0, inset=(MAHLER, "right", 0.24)),
            Shot(clip=STRINGS, clip_at=1.0),
            Shot(clip=ALONE, clip_at=2.0),
            Shot(clip=PIANO, clip_at=10.0),
        ],
        gaps=[0.60, 0.70, 0.70, 0.85, 0.90],
    ),

    # --- the cures ----------------------------------------------------------
    Section(
        title="What did his doctors try?",
        spoken_title="So what did his doctors try?",
        kicker="THE CURES",
        sentences=[
            # checklist, flow - each chunk says its own verdict, so the cross
            # lands as it is spoken. The hinge is inside the first chunk.
            S("The same letter lists them: oil of almonds, which did him, in "
              "his words, no good whatever.",
              "Warm baths in the Danube, which helped his stomach, not his "
              "hearing.",
              "And a lotion for his ears."),
            # post, as a letter - the lead-in, then the quoted words.
            S("He felt better and stronger, he wrote.",
              "But my ears are buzzing and ringing perpetually, day and "
              "night."),
            S("By November, he was wearing blisters of tree bark on both "
              "arms."),
            S("Then the ringing eased a little, especially in his left ear."),
            S("But his hearing did not come back. If anything, it got worse."),
            S("If your own ringing rises and falls, that may sound "
              "familiar."),
        ],
        shots=[
            Shot(graphic="checklist",
                 payload=([("Oil of almonds", False),
                           ("Warm baths in the Danube", False),
                           ("A lotion for his ears", False)],
                          "DID HIS HEARING IMPROVE?", True)),
            Shot(graphic="post", payload=("letter", LETTER, "")),
            Shot(clip=BARK, clip_at=2.0),
            Shot(clip=PIANO_BW, clip_at=18.0),
            # The flame goes out at ~19s, under "did not come back".
            Shot(clip=FLAME, clip_at=16.0),
            None,
        ],
        gaps=[1.20, 1.10, 0.80, 0.60, 0.80, 0.90],
    ),

    # --- the village --------------------------------------------------------
    Section(
        title="Could quiet fix it?",
        spoken_title="So could rest and quiet fix it?",
        kicker="THE VILLAGE",
        sentences=[
            S("In 1802, to spare his hearing, he spent six months in "
              "Heiligenstadt, a village outside Vienna."),
            S("Rest, distance from the city, and quiet."),
            S("It did not bring his hearing back."),
            # spotlight - the whole page, then the line to his brothers.
            S("That October, he wrote a long letter to his brothers, about "
              "how alone his deafness had made him."),
            S("He never sent it. It was found among his papers after he "
              "died."),
            # The Testament's darkest line is not quoted; this is where the
            # viewer who recognises the feeling is pointed at a person.
            S("If your ears ever leave you feeling that alone, please talk to "
              "your doctor, or someone you trust."),
            S("Advice has changed: today, clinicians tend to suggest gentle "
              "background sound, because silence can make the ringing stand "
              "out."),
        ],
        shots=[
            Shot(image=VILLAGE, zoom=1.08, pan=(0.01, 0.0)),
            Shot(image=VALLEY, zoom=1.08, pan=(-0.01, 0.0)),
            Shot(clip=SMOKE, clip_at=0.0),
            Shot(graphic="spotlight", payload=(TESTAMENT, [
                (None, ""),
                ((0.15, 0.012, 0.75, 0.05), "To his brothers"),
            ], "")),
            None,                                       # hold the page
            Shot(clip=MOON, clip_at=1.0),
            Shot(clip=WATER, clip_at=2.0),
        ],
        gaps=[0.60, 0.80, 0.90, 0.70, 0.90, 0.90, 0.90],
    ),

    # --- the experiment -----------------------------------------------------
    Section(
        title="What was he actually hearing?",
        spoken_title="But what was he actually hearing?",
        kicker="THE EXPERIMENT",
        sentences=[
            S("The best clue came a hundred and fifty years later, from a very "
              "simple experiment."),
            S("In 1953, Morris Heller and Moe Bergman took eighty adults with "
              "normal hearing and no tinnitus."),
            S("They sat them, one at a time, in a soundproof room."),
            S("Ninety-four percent of them heard a sound."),
            S("Maybe a strange room just makes people imagine things?"),
            S("In 2008, an Italian team tested exactly that."),
            # bars - one chunk per room.
            S("In 1953, ninety-four percent heard a sound.",
              "In 2008, in an empty room, eighty-three percent did.",
              "And with a dummy loudspeaker, connected to nothing, "
              "ninety-two."),
            S("So suggestion played a part, but only a small one."),
        ],
        shots=[
            Shot(image=CHAMBER, zoom=1.08, pan=(0.0, -0.01)),
            Shot(clip=ALONE, clip_at=10.0,
                 note=("80", "adults, normal hearing, no tinnitus")),
            None,                                       # hold the room
            Shot(image=CHAMBER_W, zoom=1.06, pan=(0.01, 0.0)),
            None,
            Shot(clip=PAGES, clip_at=12.0),
            Shot(graphic="bars",
                 payload=([("1953, a soundproof room", 0.94, "94%"),
                           ("2008, an empty room", 0.83, "83%"),
                           ("2008, a dummy speaker", 0.92, "92%")],
                          "HEARD A SOUND IN SILENCE")),
            Shot(clip=PIANO, clip_at=20.0),
        ],
        gaps=[0.60, 0.55, 0.80, 1.00, 0.70, 0.80, 1.20, 0.90],
    ),

    # --- the filter ---------------------------------------------------------
    Section(
        title="Why don't we all notice it?",
        spoken_title="So why do most of us never notice it?",
        kicker="THE FILTER",
        sentences=[
            S("Think of the hum of a fridge, which you stop hearing after a "
              "minute."),
            # diagram - one chunk per node. A chain, not a loop.
            S("In silence, most ears make a faint sound of their own.",
              "Most of the time, the brain filters it out.",
              "With tinnitus, something it used to ignore gets through."),
            S("That is not the whole story."),
            S("Lasting tinnitus is usually louder, does not stop when you "
              "leave a quiet room, and is often tied to hearing loss, as "
              "Beethoven's was."),
            S("But it does change the question: not, what is this strange "
              "sound, but why has my brain stopped ignoring it?"),
        ],
        shots=[
            Shot(clip=FRIDGE, clip_at=8.0),
            Shot(graphic="diagram",
                 payload=([("A faint sound", "most ears, in silence",
                            "\U0001F507"),
                           ("The brain filters it", "like a fridge's hum",
                            "\U0001F9E0"),
                           ("Tinnitus", "it gets through", "\U0001F514")],
                          "WHY MOST OF US NEVER HEAR IT", False)),
            Shot(clip=TOWN, clip_at=18.0),
            None,
            Shot(clip=VIOLIN, clip_at=7.0),
        ],
        gaps=[0.80, 1.20, 0.60, 0.80, 0.90],
    ),

    # --- close: echo the opening, then the question --------------------------
    Section(
        title="Back to that letter",
        spoken_title="So, back to that letter.",
        kicker="THE ECHO",
        sentences=[
            S("Beethoven went looking for quiet, to escape a sound he was "
              "carrying with him."),
            S("And he kept composing, for another quarter of a century."),
            # The article's own red flags, on the notice card as said.
            S("If your own ringing is new, in one ear only, or comes with a "
              "sudden drop in hearing, get it checked promptly."),
            S("If you could send Beethoven one line back, what would it say?"),
        ],
        shots=[
            Shot(clip=WATER, clip_at=9.0, inset=(STIELER, "right", 0.24)),
            Shot(clip=STRINGS, clip_at=4.0),
            Shot(clip=MOON, clip_at=14.0,
                 payload=("NOTICE", "New, one-sided, or with sudden hearing "
                                    "loss? Get it checked.")),
            Shot(clip=CANDLES, clip_at=2.0),
        ],
        gaps=[0.80, 0.90, 0.90, 3.00],
    ),
]

META = Meta(
    title="Did Beethoven Have Tinnitus?",
    hook="Beethoven had tinnitus, and he described it himself. In June 1801 "
         "he wrote to a friend that his ears were buzzing and ringing "
         "perpetually, day and night. Here is what his letters say, what his "
         "doctors tried, why a quiet village did not bring his hearing back, "
         "and what a soundproof room revealed in 1953 about the sound he "
         "heard.",
    url=URL,
    summary="Beethoven's 1801 letters to Franz Wegeler, the cures his "
            "doctors tried (oil of almonds, Danube baths, an ear lotion, bark "
            "blisters), the Heiligenstadt Testament, and the 1953 Heller and "
            "Bergman experiment, in which 94% of people with normal hearing "
            "heard a sound in a soundproof room - and its 2008 replication.",
    tags=["did beethoven have tinnitus", "beethoven tinnitus",
          "beethoven deafness", "beethoven hearing loss",
          "heiligenstadt testament", "beethoven letter wegeler",
          "heller and bergman", "tinnitus in silence", "tinnitus",
          "ringing in ears"],
    cta=f"The full article: {URL}",
    credits=["Images via Wikimedia Commons: portraits of Beethoven by "
             "Christian Horneman (1803), Joseph Willibrord Mähler (1804) and "
             "Joseph Karl Stieler (1820); the Heiligenstadt Testament (1802); "
             "Franz Wegeler; Heiligenstadt by Tobias Raulino (1821) and an "
             "anonymous 19th-century view: public domain. Soundproof chamber "
             "photographs by Togabi, CC BY-SA 4.0.",
             "Letter quotations: Beethoven's Letters, translated by Lady "
             "Wallace (1866).",
             "",
             "This video is general history, not medical advice. If your "
             "ringing is new, in one ear only, or comes with a sudden drop "
             "in hearing, please see a doctor promptly."],
)


def main() -> None:
    out = Path.home() / "Desktop/did-beethoven-have-tinnitus-long.mp4"
    work = Path.home() / "Desktop/.did-beethoven-have-tinnitus-long-work"
    made = render_long(
        SECTIONS, out, work, brand=TINNITUS, meta=META, voice=VOICE,
        music=MUSIC, callouts=None,
        endcard=ENDCARD, endcard_lead=7.0,
        # On the promise (11.7s): at 9.5 it covered the 1803 portrait inset.
        # Its 5.4s hold ends at 17.4, clear of the first card at 19.1.
        title_at=12.0, title_hold=5.4,
        # The long form's title is the search, so the opener types it.
        opener=Search("did beethoven have tinnitus"),
        emphasis=["frightful", "Ninety-four percent"],
        # The Short's own question, on the famous portrait - one source for
        # both aspects.
        thumb_headline="What did\nBeethoven\n[hear?]",
        thumb_image=STIELER, thumb_accent="orange",
        thumb_crop_at=(0.5, 0.25), thumb_crop_zoom=0.70, thumb_side="left",
        thumb_shift=0.28,
    )
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
