"""Why AI videos feel fake - OktAI's first long form, the channel's opener.

**Second pass (2026-11-21), from the editor's notes on the first draft:**
the male explainer voice (`noah`) for the AI examples; the opener's first
voice *intentionally* worse (macOS `say`, as in the first test, a little
slower so it stays understandable); no name in the intro; the voice chapter
moved to the end with a reason to stay for it; a tools chapter; the music
played in a player with the bed paused; stock footage shown and marked
wrong; logos for every platform and tool named; the outro a plain thanks.
And the main note: **more happening, more real examples** - "at the 2 and 3
minute marks too much context with plain visuals". So every chapter now
carries something real (a screen, a clip, a sound, a logo, our own
graphics), and `tools/visual_check.py` plans it before the render.

**Every claim is ours, and where it comes from:**

* The voices: the opener's first is a dramatization the editor asked for -
  `say` (Daniel), the "legacy, last resort" engine still in our code - not
  a file that shipped. The others are our explainer voice, `noah`, made by
  `oktai.examples` the two ways `docs/video/voice.md` measured ("Sentences
  are synthesised in runs"). 151 vs 192 words a minute rejected/approved:
  `audio-book-automation/docs/voice.md`. The one-word pitch, 211 to 274 Hz
  then level: `docs/video/voice.md`, "A one-word sentence has nothing to
  fall from".
* 87 videos: `crypto-wiki/json/videos.json` (41) + `tinnitus-blog/src/data/
  videos.json` (46), 2026-11-21, long forms and Shorts. Four months: the
  repo's first commit is 2026-07-29. 10,129 lines: `wc -l docs/video/*.md`.
* The tools are the ones the pipeline runs: Claude Code, Kokoro, Whisper
  (`core/recorded.py`), Python, FFmpeg, Pexels (`core/stock.py`),
  Playwright (`core/screenplay.py`), n8n (`/publish-video`).
* Stock under specific claims, the quantum-computers cut flagged at three
  timestamps, 25 labelled clips in the Ethereum cut: `docs/video/
  longform.md`, "The screen has to say what the voice is saying". The clips
  shown are generic Pexels clips from our cache standing in for those cuts;
  the overcorrection is re-drawn with the same `payload` lines it used.
* No stock faces: memory `no-default-stock-portraits`, `footage.md`.
* 42 drawn graphics: `longform.beats.BEATS` before `voice` and `wall` were
  added for this video. The wall shows six of them with the payloads of
  the videos they shipped in (`tests/test_beats.py`).
* Music: `docs/video/audio.md` - pads alone read as "creepy mysterious";
  note events on a grid fixed it; every video uses `night-drift`. The old
  bed played is `calm`, the pad-only preset that is left (the retired ones
  are never played).
* Retention: `videos-performance/history/2026-10-11.md`, eleven Short
  curves; the six rows shown are real Shorts with their real second
  sentences and half-gone seconds.
* TikTok bands, ~250 / ~770, hand-made 1,379-1,984: *Stop Making AI Slop*
  chapter 9 sources, `history/2026-10-11.md`. Cause unproven; said so.
* YouTube, 2025-07-15, "repetitive or mass-produced" content, always
  ineligible for monetization: the notice on support.google.com/youtube/
  answer/1311392, read 2026-11-21 (the screen).

**[CHECK] before Oktay reads:** "87 videos" counts long forms and Shorts on
both sites. The book is *Stop Making AI Slop* on Spotify (1 hr 2 min,
2026-11-06), its page on screen and its link in the description (the
editor, 2026-11-21: "show the cover too if not the page").

Run: `PYTHONPATH=. .venv/bin/python projects/oktai-long/why-ai-videos-feel-fake.py [--draft]`
"""

import sys

from video_automation.core import logos, samples
from video_automation.core import screenplay as sp
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section
from video_automation.oktai import build_long, examples, folder, own, screen

NAME = "why-ai-videos-feel-fake"
TITLE = "I Made 87 AI Videos. Here's What Made Them Feel Fake."

# --- sounds: made once from our own engines (`oktai/examples.py`) -----------

EXAMPLE = ["Hi, I'm the voice of this channel.",
           "I read every script you hear on it."]
LIST = ["Every sentence went in on its own.",
        "So every sentence started from scratch.",
        "Like the first line of a list."]
CLIPS = examples.make(folder(NAME) / "examples", {
    "oldest": ("oldest", EXAMPLE),
    "today": ("today", EXAMPLE),
    "split": ("one_at_a_time", LIST),
    "run": ("today", LIST),
    "money": ("phrase", "Money."),
    "money-full": ("phrase", "That's where the money goes."),
    "bed-old": ("bed", "calm", {"seconds": 7.0}),
    "bed-now": ("track", "night-drift", {"seconds": 7.0}),
})
OLDEST = samples.register(CLIPS["oldest"], "oktai-oldest")
TODAY = samples.register(CLIPS["today"], "oktai-today")
SPLIT = samples.register(CLIPS["split"], "oktai-split")
RUN = samples.register(CLIPS["run"], "oktai-run")
MONEY = samples.register(CLIPS["money"], "oktai-money")
MONEY_FULL = samples.register(CLIPS["money-full"], "oktai-money-full")
# Music examples: as loud as the voice, and the bed stops under them.
BED_OLD = samples.register(CLIPS["bed-old"], "oktai-bed-old", level=1.0, bed=0.0)
BED_NOW = samples.register(CLIPS["bed-now"], "oktai-bed-now", level=1.0, bed=0.0)


def _after(clip: str) -> float:
    """The gap after a line that a clip plays behind."""
    return round(samples.DUR[clip] + samples.LEAD + 0.6, 2)


VOICES = [("AI, at first", "a computer voice, one line at a time", OLDEST),
          ("AI, today", "the same script, our explainer voice", TODAY),
          ("Me", "reading it myself", None)]
MUSIC = [("Our first bed", "generated: three chords and a filter", BED_OLD),
         ("Today", "night-drift, under every video", BED_NOW)]


def L(slug: str, label: str) -> tuple:
    return (str(logos.path(slug)), label)


# --- real pictures --------------------------------------------------------------

V = STOCK / "videos"
GENERIC = V / "abstract-digital-data-particles-dark/34645139.mp4"
SERVERS = V / "data-center-servers-rack-dark/3130182.mp4"
CODE = V / "code-scrolling-screen-terminal-dark/34268861.mp4"
CHAIN = V / "blockchain-blocks-chain-digital-dark/34127877.mp4"
MEETING = V / "business-meeting-boardroom-night/8847933.mp4"
HANDS = V / "hands-typing-keyboard-dark-close-up/34771078.mp4"
CITY = next((V / "city-at-night-timelapse").glob("*.mp4"))
# The cover, if the Spotify page ever cannot be captured: `Shot(image=BOOK)`.
BOOK = "/Users/oktayshakirov/Coding/audio-book-automation/projects/ai-content/book/cover-original.webp"

# Six graphics from videos that shipped, with the payloads they shipped with
# (crypto: the Optimizely hack, the Coldcard breach, Squid Game, address
# poisoning; tinnitus: the spike diary, the 2026 guideline).
SHIPPED = {
    "relay": ("1Kp7vQ2mXz9LrT4wBn6cHd8yFs3aJe5gUq", "19g9rZcPeiz8rUvyWpTRyXXhPnjsWrc3kW",
              ["The page", "Your wallet app", "Your hardware wallet"],
              "ONE ADDRESS, THREE SCREENS",
              ("EVERY SCREEN MATCHES", "THE ATTACKER'S ADDRESS")),
    "breach": ("5,200+ ADDRESSES", 1816, "BTC", 4, "COLDCARD, 2026", "DRAINED",
               "1 square = 25 addresses"),
    "diary": ([5, 4, 9, 3, 5, 8, 4], [2, 3],
              [("REMEMBERED", "the bad day with it", [2]),
               ("FORGOTTEN", "the bad day without", [5])],
              "A WEEK - AN EXAMPLE", ("the suspect", "brighter = louder")),
    "honeypot": (("YOU", "a SQUID holder"), ("THE CREATORS", "anonymous"),
                 ("THE POOL", "BNB, on PancakeSwap"), "NEEDS MARBLES",
                 "THE GAME NEVER LAUNCHED", "NO RULE FOR THEM", "WHO COULD SELL SQUID"),
    "tiers": ([("Recommended", "doctors should offer it"),
               ("An option", "doctors may offer it"),
               ("Advised against", "not for tinnitus itself", None, "Nothing here")],
              [(0, "Hearing aids", "\U0001F9BB"), (1, "Sound enrichment", ""),
               (0, "Talking therapy", "")], "THE 2026 GUIDELINE", 1),
    "lookalike": ("0x4b9e1c7d2a3f8e6b5c0d9a1f7e2b3c4d5a6e7f8b",
                  "0x4b9e5f20c8a1d7e3b96f0c2a4d8e1b7f3c9a7f8b", "THE LOOK-ALIKE", (4, 4)),
    "airgap": ([("Send", "0.5 BTC"), ("To", "bc1q7k...9x4f")],
               "SENDING FROM A HARDWARE WALLET"),
}
WALL = [(g, SHIPPED[g]) for g in ("relay", "breach", "diary", "honeypot", "tiers",
                                   "lookalike")]

HALF_GONE = 28.8

# Our own published Shorts, as they shipped (`oktai.own`): first-bitcoin-
# transaction ("Hal Finney.", half gone at 7.1 s) and tmj-and-tinnitus
# ("Quick check - are your teeth touching?", 28.8 s). Empty phones until
# the files are in `own/`.
HAL = own(NAME, "PcI9fAr1xoE")
JAW = own(NAME, "cQ2I3ZCv2EE")


def row(line: str, secs: float) -> tuple:
    return (f'"{line}"', secs / HALF_GONE, f"{secs:.1f}s")


# --- screens: scripted takes, output pasted from the real commands -------------

# Our own video grid. Headless, the ad slot above it collapses and the page
# is ~1,460 px tall; the take stays on the thumbnails, because near the
# bottom Google draws a privacy note no style can reach.
SITE_CRYPTO = sp.Browser("https://thecrypto.wiki/videos", [
    sp.wait(1.0), sp.move("a[href*='/videos/'] >> nth=0"), sp.wait(0.8),
    sp.scroll(200), sp.wait(1.2), sp.move("a[href*='/videos/'] >> nth=6"), sp.wait(1.0),
], dark=False, tail=8.0)

SITE_TINNITUS = sp.Browser("https://tinnitushelp.me/videos", [
    sp.wait(0.6), sp.scroll(430), sp.wait(1.6), sp.scroll(480),
], dark=False, tail=8.0)

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
annotate.py   breach.py     honeypot.py   post.py       spotlight.py  wall.py
base.py       column.py     lookalike.py  reel.py       stake.py      wide.py
behind.py     mnemonic.py   pile.py       relay.py      sweep.py
reserve.py    scale.py      tiers.py""", secs=0.8),
], viewport=(960, 540), lead=0.4, tail=12.0)

# Playwright's own page, recorded by Playwright: the screen the line is about.
PLAYWRIGHT = sp.Browser("https://playwright.dev", [
    sp.wait(1.0), sp.move("text=Get started"), sp.wait(0.8), sp.scroll(420),
], dark=True, tail=6.0)

# The beds' own recipes, printed from `core/music.py` (output pasted from the
# real command): pads alone, against notes on a grid with a kick.
MUSIC_CODE = sp.Terminal([
    sp.cmd("grep -A3 '\"calm\": Preset' video_automation/core/music.py"),
    sp.out("""    "calm": Preset(
        name="calm", root=49.0, progression="plain", chord_len=11.0,
        cutoff=(520.0, 1150.0), sweep=27.0, detune=7.0, partials=3,
        sub=0.20, air=0.012, \x1b[1;31mpulse=0.0\x1b[0m,""", secs=0.8),
    sp.wait(2.0),
    sp.cmd("grep -A5 '\"momentum\": Preset' video_automation/core/music.py"),
    sp.out("""    "momentum": Preset(
        name="momentum", root=55.0, progression="andalusian", chord_len=7.0,
        cutoff=(900.0, 2400.0), sweep=15.0, detune=9.0, partials=4,
        sub=0.17, air=0.0, pulse=0.0,
        \x1b[1;32mbpm=100, arp=0.26\x1b[0m, arp_div=2, arp_decay=0.24, \x1b[1;32mkick=0.13\x1b[0m, kick_div=1,""", secs=0.8),
], viewport=(960, 540), lead=0.4, tail=14.0)

# The audiobook's own page. Spotify's sidebar and its "Preview of Spotify"
# banner are cropped off; the camera glides from the title to the sample.
BOOK_URL = "https://open.spotify.com/show/0u7ddJN4SFJBFzBG1NWrvA"
SPOTIFY = sp.Browser(BOOK_URL, [
    sp.wait(1.2), sp.move("h1"), sp.wait(1.2), sp.move("text=Sample"), sp.wait(1.0),
], dark=True, tail=8.0)

# The page Oktay reads from (`tools/oktai_script.py`), scrolling the way the
# teleprompter does. The window names the file, not the folder it is in.
SCRIPT_PAGE = sp.Browser((folder(NAME) / "script.html").as_uri(), [
    sp.wait(0.8), sp.scroll(500), sp.wait(1.2), sp.scroll(500),
], dark=True, tail=8.0)

POLICY = sp.Browser("https://support.google.com/youtube/answer/1311392?hl=en", [
    sp.wait(0.8), sp.scroll(330), sp.wait(0.6),
    sp.click("text=repetitive or mass-produced"), sp.wait(5.0),
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
            ("For four months,", "I've let AI make almost everything",
             "on two YouTube channels."),
            ("Eighty seven videos so far,", "written, voiced, edited and uploaded",
             "by AI."),
            ("Along the way,", "I wrote down everything", "that made those videos feel fake."),
            ("It's ten thousand lines long now.",),
            ("Today, the tools,", "the picture,", "the music,", "and the first ten seconds."),
            ("And stay to the end,", "because what we learned about the voice",
             "is why I'm reading this myself."),
        ],
        gaps=[_after(OLDEST), _after(TODAY), 0.55, 0.45, 0.5, 0.45, 0.6, 0.45, 0.9],
        shots=[
            Shot(graphic="voice", ground="grid", payload=(VOICES,),
                 samples=(OLDEST, TODAY, None)),
            None,
            None,
            screen(NAME, "site-crypto", SITE_CRYPTO),
            None,
            screen(NAME, "lessons", LESSONS),
            None,
            # A teaser: four of the pictures still to come.
            Shot(graphic="wall", payload=([
                ("logos", ([L("claude", "Claude Code"), L("kokoro", "Kokoro"),
                            L("n8n", "n8n")], "THE TOOLS")),
                ("compare", ("THE VOICE SAYS", ["Something specific"],
                             "THE STOCK CLIP SAYS", ["Something else"])),
                ("voice", (MUSIC,)),
                ("bars", ([row("Hal Finney.", 7.1),
                           row("Quick check - are your teeth touching?", 28.8)],
                          "HALF THE VIEWERS GONE BY")),
            ], "IN THIS VIDEO")),
            Shot(graphic="voice", ground="grid", payload=(VOICES,), emblem="microphone"),
        ],
    ),

    # --- the tools ------------------------------------------------------------
    Section(
        title="The tools",
        sentences=[
            ("Claude Code writes the scripts.",),
            ("Kokoro reads them, on my laptop.",),
            ("Whisper lines the captions up with the voice.",),
            ("Python draws every graphic.",),
            ("FFmpeg cuts the video.",),
            ("Playwright records the screens,", "like this one."),
            ("And Pexels has the stock footage.",),
            ("And n8n posts every video",),
            ("to YouTube,", "TikTok,", "Instagram", "and Facebook."),
            ("Some of these get a video of their own soon.",),
        ],
        shots=[
            Shot(graphic="logos", payload=([L("claude", "Claude Code"),
                                            L("kokoro", "Kokoro"),
                                            L("openai", "Whisper")], "THE WORDS")),
            None,
            None,
            Shot(graphic="logos", payload=([L("python", "Python"),
                                            L("ffmpeg", "FFmpeg")], "THE EDIT")),
            None,
            screen(NAME, "playwright", PLAYWRIGHT),
            Shot(clip=CITY, inset=(str(logos.path("pexels")), "tr", 0.12)),
            Shot(graphic="logos", payload=([L("n8n", "n8n"), L("youtube", "YouTube"),
                                            L("tiktok", "TikTok"), L("instagram", "Instagram"),
                                            L("facebook", "Facebook")], "THE UPLOAD")),
            None,
            Shot(graphic="wall", payload=([
                ("logos", ([L("claude", "Claude Code"), L("kokoro", "Kokoro")], "")),
                ("logos", ([L("python", "Python"), L("ffmpeg", "FFmpeg")], "")),
                ("logos", ([L("playwright", "Playwright"), L("pexels", "Pexels")], "")),
                ("logos", ([L("n8n", "n8n"), L("openai", "Whisper")], "")),
            ], "COMING UP")),
        ],
    ),

    # --- the picture --------------------------------------------------------
    Section(
        title="The picture",
        sentences=[
            ("The first giveaway is the picture.",),
            ("AI tools love stock footage,", "and stock footage loves to say",
             "something your voice didn't."),
            ("In one video about quantum computers,", "I stopped the cut",
             "at three timestamps."),
            ("Each time,", "a generic clip was playing", "under a very specific claim."),
            ("So the rule became simple.", "The screen has to say",
             "what the voice is saying."),
            ("Then I overcorrected.",),
            ("I put a big line of text on almost every shot,",),
            ("and the next video read like a slideshow.",),
            ("Twenty five labels in four minutes.",),
            ("And then the faces.",),
            ("Stock libraries are full of smiling strangers,",
             "and a stranger's face says nothing", "about your topic."),
            ("So our videos don't use stock faces anymore.",),
            ("Hands, screens and drawings instead.",),
        ],
        shots=[
            Shot(clip=GENERIC, verdict=("wrong", "Says nothing"), verdict_at=0.55),
            None,
            Shot(graphic="stat", payload=("3", "timestamps", "flagged in one cut"),
                 emblem="clapper"),
            Shot(clip=SERVERS, verdict=("wrong", "Generic"), verdict_at=0.5),
            Shot(graphic="diagram", payload=([
                ("Your address", "hides your public key", "\U0001F512"),
                ("Your first spend", "publishes the key", "\U0001F4E4"),
                ("A quantum computer", "could work back from it", "⚠️")],
                "WHAT THE LINE SAYS", False),
                verdict=("right", "Names the thing"), verdict_at=0.7),
            Shot(clip=CODE, payload=("", "QUANTUM COMPUTERS")),
            Shot(clip=CHAIN, payload=("", "PUBLIC KEYS")),
            Shot(clip=GENERIC, payload=("", "THE BLOCKCHAIN"),
                 verdict=("wrong", "A slideshow"), verdict_at=0.35),
            Shot(graphic="stat", payload=("25", "labels", "in a four minute video"),
                 emblem="clapper"),
            Shot(clip=MEETING, verdict=("wrong", "A stranger"), verdict_at=0.62),
            None,
            Shot(clip=HANDS, verdict=("right", "Hands at work"), verdict_at=0.4),
            Shot(graphic="wall", payload=([
                ("relay", SHIPPED["relay"]),
                ("airgap", SHIPPED["airgap"]),
            ], "SCREENS AND DRAWINGS")),
        ],
    ),

    # --- the graphics ---------------------------------------------------------
    Section(
        title="The graphics",
        sentences=[
            ("That's where the drawings come in.",),
            ("When there's no real picture of an idea,", "we draw the idea itself,",
             "moving with the voice."),
            ("There are forty two of them now,", "from a single number to a whole mechanism."),
            ("And when the library can't draw something,", "we build a new one for that video."),
            ("The waveforms at the start of this video", "were built for this one."),
        ],
        shots=[
            Shot(graphic="wall", payload=(WALL, "OUR DRAWN GRAPHICS")),
            None,
            None,
            screen(NAME, "beats", BEAT_FILES),
            Shot(graphic="voice", ground="grid", payload=(VOICES,)),
        ],
    ),

    # --- the music: played, the bed paused under it -------------------------
    Section(
        title="The music",
        sentences=[
            ("This was our first background track, made by code.",),
            ("And this one is under every video now.",),
            ("The first was a few chords and a filter,", "and it sounded creepy and mysterious,",
             "the last thing an explainer needs."),
            ("What we learned:", "a bed feels alive because of rhythm,",
             "not brightness.", "Notes on a grid, and a beat underneath."),
            ("And one track every time", "stops being a stock song,",
             "and becomes the sound of the channel."),
        ],
        gaps=[_after(BED_OLD), _after(BED_NOW), 0.5, 0.5, 0.6],
        shots=[
            Shot(graphic="voice", ground="grid", payload=(MUSIC,),
                 samples=(BED_OLD, BED_NOW)),
            None,
            screen(NAME, "music-code", MUSIC_CODE),
            None,
            Shot(graphic="voice", ground="grid", payload=(MUSIC[1:],), emblem="note"),
        ],
    ),

    # --- the first seconds ----------------------------------------------------
    Section(
        title="The first seconds",
        sentences=[
            ("Then the edit,", "and the first ten seconds of it."),
            ("We pulled the retention curves of eleven of our Shorts.",),
            ("Six of them gave the answer away", "in their second sentence,",
             "and half the viewers were gone by about nine seconds."),
            ("The five that held it back", "kept half their viewers",
             "for about eighteen."),
            ("Twice as long,", "and the openers weren't even different."),
            ("The second sentence decided it.",),
        ],
        shots=[
            Shot(graphic="phones", payload=([
                (HAL, "Half gone at 7.1s", '"Hal Finney."'),
                (JAW, "Half gone at 28.8s", '"Quick check - are your teeth touching?"')],
                "TWO OF OUR SHORTS")),
            None,
            Shot(graphic="bars", payload=([row("Hal Finney.", 7.1),
                                           row("Not because of its price.", 8.0),
                                           row("One explosion did, on set in 1967.", 8.8)],
                                          "GAVE IT AWAY: HALF GONE BY")),
            Shot(graphic="bars", payload=([row("A line from a newspaper's front page.", 17.2),
                                           row("Not a person. It is an exchange.", 18.3),
                                           row("Quick check - are your teeth touching?", 28.8)],
                                          "HELD IT BACK: HALF GONE BY")),
            None,
            Shot(graphic="quote", payload=("The second sentence decides it.",
                                           "Eleven Shorts, one pattern"), emblem="chart"),
        ],
    ),

    # --- the template -------------------------------------------------------
    Section(
        title="The template",
        sentences=[
            ("The last giveaway is the one that costs money.",),
            ("When everything comes out of one pipeline,", "every video starts to look the same."),
            ("On TikTok, our automated uploads got stuck.",),
            ("About two hundred and fifty views,", "or about seven hundred and seventy."),
            ("A few clips made by hand", "reached well over twice that."),
            ("I can't prove the template was the reason.",),
            ("But YouTube's own rules name it.",),
            ("Content that's repetitive or mass produced", "can't earn money there."),
            ("No platform has banned AI.",),
            ("They've banned videos that all look the same.",),
        ],
        shots=[
            Shot(graphic="wall", payload=([
                ("stat", ("1.1M", "coins", "never moved")),
                ("stat", ("3", "timestamps", "flagged in one cut")),
                ("stat", ("25", "labels", "in a four minute video")),
                ("stat", ("87", "videos", "since July")),
            ], "SAME LAYOUT, EVERY TIME")),
            None,
            Shot(graphic="logos", payload=([L("tiktok", "TikTok")], "AUTOMATED UPLOADS")),
            Shot(graphic="bars", payload=([("First batch", 250 / 1984, "about 250"),
                                           ("Second batch", 770 / 1984, "about 770"),
                                           ("Made by hand", 1.0, "1,379 to 1,984")],
                                          "TIKTOK VIEWS")),
            None,
            None,
            screen(NAME, "policy", POLICY),
            None,
            Shot(graphic="logos", payload=([L("youtube", "YouTube"), L("tiktok", "TikTok"),
                                            L("instagram", "Instagram"),
                                            L("facebook", "Facebook")],
                                           "NO PLATFORM HAS BANNED AI")),
            None,
        ],
    ),

    # --- the voice: why I read it myself ----------------------------------------
    Section(
        title="The voice",
        sentences=[
            ("And now the voice,", "the reason I'm reading this myself."),
            ("When an AI voice sounds robotic,", "most people slow it down."),
            ("We measured it the other way round.",),
            ("At a hundred and fifty words a minute, it was rejected as robotic.",),
            ("At a hundred and ninety, the same voice was approved.",),
            ("The second cause was how the script went in.",),
            ("Here it is, one line at a time.",),
            ("And here, the whole paragraph at once.",),
            ("One at a time, every line starts high and bright,",
             "and the whole paragraph settles, and falls."),
            ("The third cause surprised me.",),
            ("Listen to a line of just one word.",),
            ("And the same word inside a sentence.",),
            ("The single word rises and never falls,", "so the full stop turns into a shrug."),
            ("The fix isn't a better voice.", "It's a full sentence."),
        ],
        gaps=[0.5, 0.45, 0.45, 0.45, 0.6, 0.45, _after(SPLIT), _after(RUN), 0.5, 0.45,
              _after(MONEY), _after(MONEY_FULL), 0.5, 0.9],
        shots=[
            Shot(graphic="voice", ground="grid", payload=(VOICES,)),
            Shot(graphic="quote", payload=("If it sounds robotic, slow it down.",
                                           "The obvious fix"), emblem="microphone",
                 verdict=("wrong", "Backwards"), verdict_at=0.62),
            None,
            Shot(graphic="bars", payload=([("Slowed down", 151 / 192, "151 a minute: robotic"),
                                           ("Faster", 1.0, "192 a minute: approved")],
                                          "WORDS PER MINUTE")),
            None,
            Shot(graphic="stat", payload=("2", "the second cause", "how the script goes in"),
                 emblem="wave"),
            Shot(graphic="voice", ground="grid", payload=([
                ("One line at a time", "every sentence its own call", SPLIT),
                ("The whole paragraph", "one call, one breath", RUN)],),
                samples=(SPLIT, RUN)),
            None,
            # Measured in `docs/video/voice.md`: five lines alone opened at
            # 227-271 Hz; the same five as one run sat at 199, falling to 193.
            Shot(graphic="bars", payload=([("One line at a time", 1.0, "227 to 271 Hz, every line"),
                                           ("The whole paragraph", 199 / 271,
                                            "199 Hz, falling to 193")],
                                          "WHERE EACH LINE STARTS")),
            Shot(graphic="stat", payload=("3", "the third cause", "one-word lines"),
                 emblem="microphone"),
            Shot(graphic="voice", ground="grid", payload=([
                ("Money.", "one word, on its own", MONEY),
                ("That's where the money goes.", "the same word, in a sentence", MONEY_FULL)],),
                samples=(MONEY, MONEY_FULL)),
            None,
            Shot(graphic="chart", payload=([211, 232, 251, 266, 274, 274, 274],
                                           "ONE WORD, ITS PITCH", 4, "never falls")),
            Shot(graphic="voice", ground="grid", payload=([
                ("Money.", "one word, on its own", MONEY),
                ("That's where the money goes.", "the same word, in a sentence", MONEY_FULL)],),
                verdict=("right", "A full sentence"), verdict_at=0.35),
        ],
    ),

    # --- why I read it myself -----------------------------------------------------
    Section(
        title="Why I read it myself",
        sentences=[
            ("Every fix on this list", "was a decision somebody had to make,",
             "listen to, and check."),
            ("The AI did the work.", "A person did the judging."),
            ("So on this channel,", "I read every script myself."),
            ("The AI still writes the drafts,", "edits the video,", "draws the graphics,",
             "and uploads it."),
            ("But the voice you hear is a person,", "and the numbers on screen are ours."),
            ("I wrote all of this up in a one-hour audiobook,", "Stop Making AI Slop,",
             "and the link is in the description."),
            ("Every video here is something I built with AI,", "and what it made, or didn't."),
            ("Thanks for watching,", "and if you enjoyed it,", "subscribe for more."),
        ],
        shots=[
            screen(NAME, "lessons", LESSONS),
            Shot(graphic="logos", payload=([L("claude", "The work"),
                                            L("kokoro", "The draft voice")],
                                           "THE AI")),
            screen(NAME, "script-page", SCRIPT_PAGE, window=("browser", "script.html")),
            Shot(graphic="logos", payload=([L("claude", "Drafts"), L("ffmpeg", "Edit"),
                                            L("python", "Graphics"), L("n8n", "Upload")],
                                           "STILL THE AI")),
            None,
            screen(NAME, "spotify", SPOTIFY, crop=(0.235, 0.055, 0.975, 0.9)),
            screen(NAME, "site-tinnitus", SITE_TINNITUS),
            Shot(graphic="quote", payload=("Thanks for watching.", "OktAI"), emblem="play"),
        ],
    ),
]

# The camera box: not on the opener (the AI voices come first), but the
# moment the person arrives, and on the asides. Read by the script page too.
FACE_HOOK = False
FACE = [("And this one is me", 5.0),
        ("Then I overcorrected", 3.0),
        ("I can't prove", 3.5),
        ("So on this channel", 4.5)]

META = Meta(
    title=TITLE,
    hook="My AI voice sounded robotic, so I did what everyone does and slowed it "
         "down. That was the mistake. Here is everything 87 AI videos taught me.",
    url="https://oktayshakirov.com",
    summary="The tools, the stock footage, the graphics, the music, the first "
            "ten seconds, the template and the voice: what made our AI videos "
            "feel fake, with our own numbers, and the fixes that worked.",
    tags=["ai video", "ai voice", "faceless youtube", "youtube automation",
          "claude code", "ai slop", "oktai"],
    cta=f"The audiobook with all of it, Stop Making AI Slop: {BOOK_URL}",
)


def main() -> None:
    made = build_long(SECTIONS, NAME, face=FACE, hook=3.0 if FACE_HOOK else None,
                      meta=META, emblem="microphone", draft="--draft" in sys.argv)
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
