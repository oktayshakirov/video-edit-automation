"""Why AI videos feel fake - OktAI's first long form, the channel's opener.

The editor's brief (2026-11-21): open on the robotic AI voice, then the one
the videos use today, then the twist - Oktay reads it himself, AI and a
person together - and go through everything else we learned: editing, stock,
animations, music.

**Every claim is ours, and where it comes from:**

* The robotic voice: `audio-book-automation/docs/voice.md` (151 wpm
  rejected as "too slow, robotic", 192 approved, same voice and script);
  `docs/video/voice.md`, "Sentences are synthesised in runs" (cold starts at
  227-271 Hz, one run at 199 falling to 193). The clips played are made by
  `oktai.examples` from the same Kokoro voice, so what changes between them
  is only what we changed.
* The one-word line: `docs/video/voice.md`, "A one-word sentence has
  nothing to fall from" (pitch 211 to 274 Hz, then level); *Stop Making AI
  Slop*, chapter 7.
* Stock under specific claims, the quantum-computers cut flagged at three
  timestamps, and the twenty-five labelled clips of the Ethereum cut:
  `docs/video/longform.md`, "The screen has to say what the voice is saying".
* No stock faces: memory `no-default-stock-portraits`, `footage.md`.
* 42 drawn beats: `longform.beats.BEATS` on 2026-11-21 (the `voice` beat in
  this video's opener is the 42nd, built for it).
* Music: `docs/video/audio.md` - the first generated bed was "creepy
  mysterious", what fixed it was note events on a grid; every video now uses
  `night-drift`.
* Retention: *Slop* `SOURCES.md` chapter 3, from `videos-performance/history/
  2026-10-11.md` - eleven Short curves, six with the answer in sentence two
  (half gone at 7.1-11.0 s, mean 8.95), five holding it back (11.6-28.8 s,
  mean 18.3). Opener style did not separate them.
* TikTok bands: *Slop* chapter 9, `history/2026-10-11.md` - pipeline uploads
  at ~250 or ~770, hand-made clips 1,379-1,984. Cause unproven; the script
  says so.
* YouTube, 2025-07-15: the "repetitious content" policy renamed "inauthentic
  content", covering "repetitive or mass-produced" content, always
  ineligible for monetization - the notice at the top of
  support.google.com/youtube/answer/1311392, read 2026-11-21 (the screen).
* 87 videos: `crypto-wiki/json/videos.json` (41) + `tinnitus-blog/src/data/
  videos.json` (46), 2026-11-21. First commit of this repo 2026-07-29.
  10,129 lines of lessons: `wc -l docs/video/*.md`, 2026-11-21.

**[CHECK] before Oktay reads:** "87 videos since July" counts every video on
both sites (long forms and Shorts). And the book line in the close names
*Stop Making AI Slop* as out - its store link goes in the description.

Run: `PYTHONPATH=. .venv/bin/python projects/oktai-long/why-ai-videos-feel-fake.py [--draft]`
"""

import sys

from video_automation.core import samples
from video_automation.core import screenplay as sp
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section
from video_automation.oktai import build_long, examples, folder, screen

NAME = "why-ai-videos-feel-fake"
TITLE = "I Made 87 AI Videos. Here's What Made Them Feel Fake."

# The two AI reads in the opener say the same lines, so only the voice changes.
EXAMPLE = ["Hi, I'm the voice of this channel.",
           "I read every script you hear on it."]
CLIPS = examples.make(folder(NAME) / "examples", EXAMPLE)
ROBOTIC = samples.register(CLIPS["robotic"], "oktai-robotic")
TODAY = samples.register(CLIPS["today"], "oktai-today")
ROOM = 0.6                     # after a clip, before the next line


def _after(clip: str) -> float:
    return round(samples.DUR[clip] + samples.LEAD + ROOM, 2)


VOICES = [("AI, at first", "slowed down, one line at a time", ROBOTIC),
          ("AI, today", "the same voice, whole paragraphs", TODAY),
          ("Me", "reading it myself", None)]


# --- screens: scripted takes, the output pasted from the real commands -----

LESSONS = sp.Terminal([
    sp.cmd("wc -l docs/video/*.md"),
    sp.out("""      73 docs/video/README.md
     310 docs/video/audio.md
    1968 docs/video/beats.md
     225 docs/video/design.md
    2012 docs/video/footage.md
     828 docs/video/longform.md
     672 docs/video/narration.md
     111 docs/video/retention.md
    1427 docs/video/shorts.md
    1243 docs/video/thumbnails.md
     195 docs/video/troubleshooting.md
     563 docs/video/voice.md
     502 docs/video/workflow.md
\x1b[1;33m   10129 total\x1b[0m""", secs=1.6),
], viewport=(820, 461), lead=0.4, tail=12.0)

BEAT_FILES = sp.Terminal([
    sp.cmd("ls video_automation/longform/beats"),
    sp.out("""airgap.py     blindsign.py  diary.py      plot.py       shares.py     voice.py
annotate.py   breach.py     honeypot.py   post.py       spotlight.py  wide.py
base.py       column.py     lookalike.py  reel.py       stake.py
behind.py     mnemonic.py   pile.py       relay.py      sweep.py
reserve.py    scale.py      tiers.py""", secs=0.8),
], viewport=(960, 540), lead=0.4, tail=12.0)

POLICY = sp.Browser("https://support.google.com/youtube/answer/1311392?hl=en", [
    sp.wait(0.8),
    sp.scroll(330),
    sp.wait(0.6),
    sp.click("text=repetitive or mass-produced"),
    sp.wait(5.0),
], dark=False, tail=10.0)


SECTIONS = [
    # --- the opener: two AI reads, then the person ------------------------
    Section(
        title="Three voices",
        card=False,
        sentences=[
            ("This is how the AI voice on my channels sounded at first.",),
            ("And this is how it sounds today.",),
            ("And this one is me.",),
            ("I'm Oktay,", "and for four months", "I've let AI make", "almost everything",
             "on two YouTube channels."),
            ("It writes the scripts,", "reads them, edits them,", "and uploads them."),
            ("Along the way,", "I wrote down everything", "that made those videos",
             "feel fake."),
            ("It's ten thousand lines", "long now."),
            ("This video is that list,", "with the receipts,", "and the fixes",
             "that actually worked."),
        ],
        gaps=[_after(ROBOTIC), _after(TODAY), 0.55, 0.55, 0.55, 0.55, 0.55, 0.9],
        shots=[
            Shot(graphic="voice", ground="grid", payload=(VOICES,),
                 samples=(ROBOTIC, TODAY, None)),
            None,
            None,
            None,                    # the person arrives: hold on "Me"
            Shot(graphic="steps", payload=([("Script", None), ("Voice", None),
                                             ("Edit", None), ("Upload", None)],
                                            "87 VIDEOS SINCE JULY, MADE BY AI")),
            screen(NAME, "lessons", LESSONS),
            None,
            None,
        ],
    ),

    # --- the voice -------------------------------------------------------
    Section(
        title="The voice",
        sentences=[
            ("Let's start with the voice,", "because that's what people", "notice first."),
            ("When an AI voice sounds robotic,", "most people slow it down."),
            ("It feels like", "the careful thing to do."),
            ("We measured it", "in words per minute."),
            ("At about a hundred and fifty", "words a minute,", "the read was rejected",
             "as robotic."),
            ("At about a hundred and ninety,", "the same voice,", "reading the same script,",
             "was approved."),
            ("The second cause", "was how the script", "reached the voice."),
            ("Every sentence went in", "on its own,", "so every sentence",
             "started from scratch,", "high and bright,", "like the first line", "of a list."),
            ("Fed whole paragraphs instead,", "the voice settled", "into a calm,",
             "falling register."),
            ("That's most of the difference", "you heard at the start."),
            ("The third cause", "surprised me."),
            ("A dramatic line", "of just one word", "comes out sounding", "like a question."),
            ("The pitch rises", "through the word", "and never falls,",
             "so the full stop", "turns into a shrug."),
            ("The fix isn't", "a better voice."),
            ("It's a full sentence,", "with the pause", "written after it."),
        ],
        shots=[
            Shot(graphic="voice", ground="grid", payload=(VOICES[:2],)),
            Shot(graphic="quote", payload=("If it sounds robotic, slow it down.",
                                           "The obvious fix")),
            None,
            Shot(graphic="bars", payload=([
                ("Slowed down", 151 / 192, "151 a minute: robotic"),
                ("Faster", 1.0, "192 a minute: approved"),
            ], "WORDS PER MINUTE")),
            None,
            None,
            Shot(graphic="compare", payload=("ONE LINE AT A TIME", ["Every line a cold start",
                                                                 "High and bright"],
                                             "WHOLE PARAGRAPHS", ["The voice settles",
                                                                  "Calm, falling"])),
            None,
            None,
            None,
            Shot(graphic="chart", payload=([211, 232, 251, 266, 274, 274, 274],
                                           "ONE WORD, ITS PITCH", 4, "never falls")),
            None,
            None,
            Shot(graphic="compare", payload=("ONE WORD", ["Sounds like a question"],
                                             "A FULL SENTENCE", ["Lands like a statement"],
                                             True)),
            None,
        ],
    ),

    # --- the picture -----------------------------------------------------
    Section(
        title="The picture",
        sentences=[
            ("The second giveaway", "is the picture."),
            ("AI tools love stock footage,", "and stock footage loves",
             "to say something", "your voice didn't."),
            ("In one of our videos,", "about quantum computers,", "I stopped the cut",
             "at three timestamps."),
            ("Each time,", "a generic clip", "was playing under", "a very specific claim."),
            ("So the rule became simple.",),
            ("The screen has to say", "what the voice is saying."),
            ("Then I overcorrected.",),
            ("I put a big line of text", "on almost every shot,", "and the next video",
             "read like a slideshow."),
            ("Twenty five labelled clips", "in four minutes", "is a title", "every few seconds."),
            ("The fix for a clip", "that says nothing", "is a picture", "that names the thing,",
             "not a caption on top."),
            ("And then the faces.",),
            ("Stock libraries are full", "of smiling strangers,", "and a stranger's face",
             "says nothing", "about your topic."),
            ("So our videos", "don't use stock faces", "anymore."),
            ("Hands, screens", "and drawings instead."),
        ],
        shots=[
            Shot(graphic="compare", payload=("THE VOICE SAYS", ["Something specific"],
                                             "THE STOCK CLIP SAYS", ["Something else"])),
            None,
            Shot(graphic="stat", payload=("3", "timestamps", "flagged in one cut")),
            None,
            None,
            Shot(graphic="quote", payload=("The screen has to say what the voice is saying.",
                                           "Rule one of our edit")),
            None,
            None,
            Shot(graphic="stat", payload=("25", "labelled clips", "in a four minute video")),
            None,
            None,
            Shot(graphic="checklist", payload=([("A stranger smiling", False),
                                                ("Hands at work", True),
                                                ("The real screen", True),
                                                ("A drawing of the idea", True)],
                                               "WHAT GOES ON SCREEN")),
            None,
            None,
        ],
    ),

    # --- the graphics ----------------------------------------------------
    Section(
        title="The graphics",
        sentences=[
            ("That's where", "the animations come in."),
            ("When there's no real picture", "of an idea,", "we draw it."),
            ("There are forty two", "drawn graphics", "in our library now,",
             "from a single number", "to a whole mechanism."),
            ("And when the library", "can't draw something,", "we build a new one",
             "for that video."),
            ("The waveforms", "at the start of this video", "are the newest one."),
        ],
        shots=[
            Shot(graphic="diagram", payload=([("An idea", "with no photo of it", "\U0001F4A1"),
                                              ("A drawing", "that moves with the voice",
                                               "✏️"),
                                              ("The viewer", "sees what is said",
                                               "\U0001F440")],
                                             "WHEN THERE IS NO PICTURE", False)),
            None,
            screen(NAME, "beats", BEAT_FILES),
            None,
            None,
        ],
    ),

    # --- the sound -------------------------------------------------------
    Section(
        title="The music",
        sentences=[
            ("Music was", "the quietest mistake."),
            ("Our first background track", "was generated by code,", "three chords",
             "and a filter."),
            ("Played back,", "it sounded creepy and mysterious,", "which is the last thing",
             "an explainer needs."),
            ("What made it feel alive", "wasn't brightness."),
            ("It was rhythm,", "notes on a grid,", "and a beat underneath."),
            ("Today every one", "of our videos", "uses the same track."),
            ("The same bed every time", "stops being a stock song,", "and becomes",
             "the sound of the channel."),
        ],
        shots=[
            Shot(graphic="compare", payload=("THREE CHORDS", ["Creepy, mysterious"],
                                             "NOTES ON A GRID", ["Rhythm, a beat"])),
            None,
            None,
            None,
            None,
            Shot(graphic="stat", payload=("1", "track", "under every video")),
            None,
        ],
    ),

    # --- the first seconds -----------------------------------------------
    Section(
        title="The first seconds",
        sentences=[
            ("Then there's the edit,", "and the first ten seconds of it."),
            ("We pulled the retention curves", "of eleven of our Shorts."),
            ("Six of them", "gave the answer away", "in the second sentence."),
            ("Half their viewers", "were gone", "after about nine seconds."),
            ("The five that held", "the answer back", "kept half their viewers",
             "for about eighteen."),
            ("Twice as long,", "and the openers", "weren't even different."),
            ("The second sentence", "decided it."),
        ],
        shots=[
            Shot(graphic="stat", payload=("11", "Shorts", "retention curves pulled")),
            None,
            Shot(graphic="bars", payload=([
                ("Answer in sentence two", 9 / 18, "half gone at about 9s"),
                ("Answer held back", 1.0, "half gone at about 18s"),
            ], "HALF THE VIEWERS GONE")),
            None,
            None,
            None,
            Shot(graphic="quote", payload=("The second sentence decides it.",
                                           "Eleven Shorts, one pattern")),
        ],
    ),

    # --- the template ----------------------------------------------------
    Section(
        title="The template",
        sentences=[
            ("The last giveaway", "is the one", "that costs money."),
            ("When everything comes out", "of the same pipeline,", "every video",
             "starts to look the same."),
            ("Our automated TikTok uploads", "landed at about", "two hundred and fifty views,",
             "or about seven hundred and seventy,", "and almost nothing in between."),
            ("A few clips", "made by hand", "earlier in the year", "reached well over twice that."),
            ("I can't prove", "the template", "was the reason."),
            ("But YouTube's own rules", "name it."),
            ("Content that's repetitive", "or mass produced", "can't earn money there."),
            ("No platform has banned AI.",),
            ("They've banned videos", "that all look the same."),
        ],
        shots=[
            Shot(graphic="grid", payload=([("Same opener", "every video"),
                                           ("Same layout", "every shot"),
                                           ("Same pacing", "every line"),
                                           ("Same voice", "every script")],
                                          "WHAT A TEMPLATE LOOKS LIKE")),
            None,
            Shot(graphic="bars", payload=([
                ("Pipeline uploads", 770 / 1984, "about 250 or about 770"),
                ("Made by hand", 1.0, "1,379 to 1,984"),
            ], "TIKTOK VIEWS")),
            None,
            None,
            screen(NAME, "policy", POLICY),
            None,
            Shot(graphic="quote", payload=("No platform has banned AI.",
                                           "What the rules actually say")),
            None,
        ],
    ),

    # --- why I read it myself --------------------------------------------
    Section(
        title="Why I read it myself",
        sentences=[
            ("Which brings me back", "to the voice."),
            ("Every fix on this list", "was a decision", "somebody had to make,",
             "listen to,", "and check."),
            ("The AI did the work.", "A person did the judging."),
            ("So on this channel,", "I read every script myself."),
            ("The AI still writes the drafts,", "edits the video,", "draws the graphics,",
             "and uploads it."),
            ("But the voice you hear", "is a person,", "and the numbers on screen",
             "are ours."),
            ("I wrote all of this up", "in a short audiobook,", "Stop Making AI Slop,",
             "and the link is in the description."),
            ("Every video here", "is something I built", "with AI,", "and what it made,",
             "or didn't."),
            ("Okay, AI.", "Let's build."),
        ],
        shots=[
            Shot(graphic="voice", ground="grid", payload=(VOICES,)),
            Shot(graphic="steps", payload=([("Make the call", None), ("Listen", None),
                                             ("Check", None)], "WHAT A PERSON DOES")),
            Shot(graphic="compare", payload=("THE AI", ["Does the work"],
                                             "A PERSON", ["Does the judging"])),
            None,
            Shot(graphic="steps", payload=([("Drafts", None), ("Edit", None),
                                             ("Graphics", None), ("Upload", None)],
                                            "STILL THE AI")),
            None,
            Shot(graphic="stat", payload=("1", "audiobook", "Stop Making AI Slop")),
            None,
            Shot(graphic="quote", payload=("OK, AI. Let's build.", "OktAI")),
        ],
    ),
]

# The camera box: not on the opener (the AI voices come first), but the
# moment the person arrives, and on the asides.
# No box on the hook: the opener is the two AI voices; the face arrives with
# "this one is me". Read by `build_*` below and by the script page.
FACE_HOOK = False
FACE = [("And this one is me", 5.0),
        ("Then I overcorrected", 3.0),
        ("I can't prove", 3.5),
        ("So on this channel", 4.0)]

META = Meta(
    title=TITLE,
    hook="My AI voice sounded robotic, so I did what everyone does and slowed it "
         "down. That was the mistake. Here is everything 87 AI videos taught me.",
    url="https://oktayshakirov.com",
    summary="The voice, the stock footage, the graphics, the music, the first "
            "ten seconds and the template: what made our AI videos feel fake, "
            "with our own numbers, and the fixes that worked.",
    tags=["ai video", "ai voice", "faceless youtube", "youtube automation",
          "claude code", "ai slop", "oktai"],
    cta="The audiobook with all of it, Stop Making AI Slop: [LINK]",
)


def main() -> None:
    made = build_long(SECTIONS, NAME, face=FACE, hook=3.0 if FACE_HOOK else None, meta=META,
                      draft="--draft" in sys.argv)
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
