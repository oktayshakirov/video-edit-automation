"""Why AI videos feel fake - OktAI's first long form, the channel's opener.

**Sixth pass (2026-11-24 evening) - prepared, not rendered: he renders
when the laptop is on power.** His notes on the fifth cut, and where each is:

* 0:06 the "s" of "clips" played after the pause, on "and the same" - fixed
  in `recorded._split`: lines read in one breath split at the quietest
  30 ms, not at Whisper's boundary (15.36 -> 15.505 s).
* 0:50 the "s" of "mistakes" cut - a regression of the fifth pass: the
  pickups were matched *before* the gap clean-up, which then took the "s"
  for a breath. Now cleaned first, matched after (`build_narration_recorded`).
* 1:05 "footage" lost its "-ge" - the pin ended at 159.52; now 159.60.
* 2:13 "Claude made with code", no "the" - cut out (`DROPS`), caption too.
* 3:10 each quote with the question its Short answered (the Shorts'
  titles), grey beside it (16:9) or under it (9:16) - `bars` label notes.
* 3:39 the policy page: the rule's own words under a yellow highlighter
  drawn across them (`screenplay.mark`), wherever the page is shown.
* The end: after the TV-off, 2.5 s of black, a line and an arrow down to
  the description (`CODA`, `overlay.Coda`). What it links: the free prompt
  (`why-ai-videos-feel-fake.prompt.md`) on oktayshakirov.com/prompts - a
  page not built yet. Wording and the page: his call.
* The voice ("very punchy, maybe even loud, and reverb in it"), measured
  against his reference video: 11-20 dB more boom at 100-130 Hz, 8-11 dB
  more at 3-5 kHz (the chain aimed at the AI voice), the bed ~7 dB higher
  under the voice than research's 18-20 dB, and a room tail (words drop
  11 dB in 20-50 ms; the reference 26). Four samples on his Desktop
  (`voice-samples/`): now, new tone + bed 6 dB lower, and that with
  `recorded.dereverb` at two strengths. His pick: "2 - new tone sounds the
  best, better than the original" - now the chain (`recorded.TARGET_LTASS`,
  `clean_chain`) and the bed (`oktai.MUSIC_LUFS` -35); no de-reverb.

**Fifth pass (2026-11-24), the editor's review of the recorded cut with
pickups:** the slop strip read in written pauses; a different slop example
(the price video under a spinning coin); "#1"-"#5" over the roadmap; his
picks of a cameraman and a smiling girl for the stock clips; bit chirps under
the data clip; the overcorrection's labels as type on the footage; more time
on both walls; the Claude Code prompts highlighted; chapters opening on their
own window; the giveaway lines back in short quotes; a note under the two AI
voices; him as the judge; the script page cropped to the script, recording;
the "English isn't my first language" pickup and the last camera boxes out.

**Fourth pass (2026-11-23): one message.** The editor, watching the third
recorded cut: "I'm getting confused what the main message is - is it how to
stop making AI slop, because this is AI slop still; how I build videos with
Claude; how to make your AI videos better; what we learned after X videos?"
It was three of the channel plan's slate in one (#1 the lessons, #4 the
pipeline, #5 the tells). Decided, with him:

* **The message, in the first 30 seconds and proved by every chapter:** the AI
  was not the problem - nobody checking what it made was. In 89 videos, these
  are the five calls I had to make, and what fixed each.
* **Each chapter: what the AI did by default, what I noticed, the fix shown
  working - and one rule a viewer can use** ("If you make AI videos, ...").
* **The pipeline is one beat**, not a minute: "And Claude runs all of it."
  The whole pipeline is its own video (the plan's #4).
* **Title:** "I Made 89 AI Videos. 5 Mistakes Made Them Slop." **Cover:** a
  before/after split - a slop frame (stock clip, big label) desaturated with
  a red cross, one of the fixed frames bright with a green tick, his face cut
  out between them looking at the slop; three words at most, "MINE WAS SLOP".
* New lines to record are in `PICKUPS` (marked on the script page).

**Third pass (2026-11-23), from the editor's review of the second recorded
cut** ("generally it's getting better, but it needs to be easier for viewers
to follow ... very engaging, flowing easily, and clear about what we discuss
next; currently it's jumping through topics"):

* **The video is about AI slop now**, the editor's angle: the opener no longer
  starts on the voice ("too random to start with") but on the slop everyone
  has seen - the same robot voice, stock clips and template - why it gets no
  views, and then the twist: I made a lot of it. Claude is named early as
  what runs the whole process.
* **A promised list, counted out loud**: "the five mistakes that mattered
  most", each chapter "the second mistake was the music" - the structure
  three reference videos on the topic share (transcribed 2026-11-23:
  Kurzgesagt, "AI Slop Is Destroying The Internet", 11.5M views; ThioJoe,
  "YouTube's AI Slop Problem is Worse Than You Know", 123K; Kevis Unfiltered,
  "Why Your Claude AI Videos Get 0 Views", 44K - problem first, the personal
  stake, a numbered promise, "here's one example" before every example).
* **Chapter titles live inside a sentence** (`Section.lead`): "The second
  mistake / was the music." The roadmap is a `reel` of five windows; each
  chapter starts on the last chapter's window, travels to its own on the
  word and dives in - also the editor's fix for the slideshow at 1:20.
* **"I", not "we"** - one person, no team. **Short, plain sentences** (he
  reads in his second language; "a bed feels alive because of rhythm, not
  brightness" at 2:39 was the example of what not to write).
* Out: the TikTok views (unprovable, so it told the viewer nothing), "some of
  these get a video of their own soon", and the spoken chapter titles.

**Every claim is mine, and where it comes from:**

* The voices: the opener's first is a dramatization the editor asked for -
  `say` (Daniel), the "legacy, last resort" engine still in our code - not
  a file that shipped. The others are the explainer voice, `noah`, made by
  `oktai.examples` the two ways `docs/video/voice.md` measured ("Sentences
  are synthesised in runs"). 151 vs 192 words a minute rejected/approved:
  `audio-book-automation/docs/voice.md`. The one-word pitch, 211 to 274 Hz
  then level: `docs/video/voice.md`, "A one-word sentence has nothing to
  fall from".
* Almost ninety videos: `crypto-wiki/json/videos.json` (41) +
  `tinnitus-blog/src/data/videos.json` (48) = 89 on 2026-11-23, long forms
  and Shorts. Four months: the repo's first commit is 2026-07-29. Ten
  thousand lines: `wc -l docs/video/*.md`, 10,129.
* The tools are the ones the pipeline runs, and Claude Code runs them: Claude
  Code, Kokoro, Whisper (`core/recorded.py`), Python, FFmpeg, n8n
  (`/publish-video`); Pexels for stock (`core/stock.py`).
* Stock under specific claims, the quantum-computers cut stopped at three
  timestamps, 25 labelled clips in the Ethereum cut: `docs/video/
  longform.md`, "The screen has to say what the voice is saying". The clips
  shown are generic Pexels clips from our cache standing in for those cuts;
  the overcorrection is re-drawn with the same `payload` lines it used.
* No stock faces: memory `no-default-stock-portraits`, `footage.md`.
* More than forty drawn graphics: `longform.beats.BEATS`. The wall shows six
  with the payloads of the videos they shipped in (`tests/test_beats.py`).
* Music: `docs/video/audio.md` - pads alone read as "creepy mysterious";
  note events on a grid fixed it; every video uses `night-drift`. The old
  bed played is `calm`, the pad-only preset that is left (the retired ones
  are never played).
* Retention: `videos-performance/history/2026-10-11.md`, eleven Short
  curves; the six rows shown are real Shorts with their real second
  sentences and half-gone seconds.
* YouTube, 2025-07-15, "repetitive or mass-produced" content, always
  ineligible for monetization: the notice on support.google.com/youtube/
  answer/1311392, read 2026-11-21 (the screen).

**No audiobook** (his call, 2026-11-22: "it's out of topic").

Run: `PYTHONPATH=. .venv/bin/python projects/oktai-long/why-ai-videos-feel-fake.py [--draft]`
"""

import sys
from pathlib import Path

from video_automation.core import logos, samples
from video_automation.core.recorded import Pause
from video_automation.core import screenplay as sp
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform import Meta, Section
from video_automation.oktai import build_long, examples, folder, own, screen, still

NAME = "why-ai-videos-feel-fake"
TITLE = "I Made 89 AI Videos. 5 Mistakes Made Them Slop."

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


FOOTNOTE = "*Both are text-to-speech voices reading the same script."
VOICES = [("AI, at first", "a computer voice, one line at a time", OLDEST),
          ("AI, today", "the same script, my explainer voice", TODAY),
          ("Me", "reading it myself", None)]
MUSIC = [("My first track", "made by code: a few slow chords", BED_OLD),
         ("Today", "night-drift, under every video", BED_NOW)]


def L(slug: str, label: str) -> tuple:
    return (str(logos.path(slug)), label)


# --- real pictures --------------------------------------------------------------

V = STOCK / "videos"
GENERIC = V / "abstract-digital-data-particles-dark/34645139.mp4"
SERVERS = V / "data-center-servers-rack-dark/3130182.mp4"
CODE = V / "code-scrolling-screen-terminal-dark/34268861.mp4"
CHAIN = V / "blockchain-blocks-chain-digital-dark/34127877.mp4"
# Each window shows footage, never a text card (the editor, 2026-11-23): a
# robot for "the same robot voice", a copy-paste for the template, and a
# picture per chapter. Fetched from Pexels with `core.stock` that day.
ROBOT = V / "humanoid-robot-dark/8084493.mp4"
COPY = V / "copy-paste-laptop-keyboard-shortcut-dark/36036748.mp4"
EQUALIZER = V / "audio-equalizer-lights-dark/7087627.mp4"
STOPWATCH = V / "stopwatch-close-up/9944842.mp4"
MIC = next((V / "microphone-studio-dark-low-key").glob("*.mp4"))
# "Smiling strangers" that smile and look into the lens (the editor: "we
# mention smiling strangers but don't show people who smile or even look at
# the camera") - the one place a stock face is shown, marked wrong.
# The first is the editor's pick (2026-11-24, pexels.com/video/6184751:
# "change this person with this one").
SMILE_A = V / "girl-smiling-close-up/6184751.mp4"
SMILE_B = V / "man-smiling-looking-at-camera/6682448.mp4"
# Stock footage of stock footage being shot - the editor's pick for "AI tools
# love stock footage" (2026-11-24, pexels.com/video/8089229), fetched with
# `core.stock.video`.
CAMERAMAN = V / "cameraman-filming-video-camera/8089229.mp4"
# The opener's slop example is a different video from the picture chapter's
# quantum one (2026-11-24: "show different video example of ai slop so we
# don't repeat this video"): the price explainer, under a spinning coin.
COIN = V / "bitcoin-coin-rotating/7634144.mp4"

# My own videos, as they sit on YouTube (`core.window`, "youtube"): titles,
# channel and views read with yt-dlp on 2026-11-23.
CRYPTO_ICON = Path.home() / "Coding/crypto-wiki/public/images/app-icon.png"
# Me, as a round badge beside Claude's: the avatar he sent (2026-11-24).
ME = Path(__file__).resolve().parents[2] / "assets/brand/oktai/oktay-badge.png"
YT_QUANTUM = ("youtube", "Can Quantum Computers Break Bitcoin? What Would Actually Happen",
              "Crypto Wiki  ·  16 views  ·  2 months ago", str(CRYPTO_ICON))
YT_ETHEREUM = ("youtube", "Why Was Ethereum Created?",
               "Crypto Wiki  ·  22 views  ·  2 months ago", str(CRYPTO_ICON))
# Read with yt-dlp on 2026-11-24: 3 views, uploaded 2026-08-23.
YT_PRICE = ("youtube", "What Determines the Price of Bitcoin? Explained Simply",
            "Crypto Wiki  ·  3 views  ·  3 months ago", str(CRYPTO_ICON))

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


def row(line: str, secs: float, said: str, asked: str = "") -> tuple:
    """A Short's bar: its second sentence, said short and generic, in quotes,
    and its time. `line` is the sentence as it shipped, kept as the source.
    The full quotes came off (2026-11-23: "remove the sentences in quotes");
    a short one came back (2026-11-24: "add the word or sentence which gave
    it away in quotes, but keep it generic and simple, you can paraphrase")."""
    # And the question the Short answered, from its title (2026-11-24: "next
    # to the quote write the answer simplified, like 'are your teeth
    # touching?' - can your jaw cause tinnitus?").
    quote = f"\u201c{said}\u201d"
    return ((quote, asked) if asked else quote, secs / HALF_GONE, f"{secs:.1f}s")


# --- screens: scripted takes, output pasted from the real commands -------------

# The channels themselves, not our sites' video pages (2026-11-25: "instead
# of showing our websites, show the YouTube channels. Sort by popular, show
# longs and shorts, and make sure it's in dark mode"): the Videos tab sorted
# by Popular, then the Shorts tab, Popular. YouTube's dark theme is its own
# cookie (`screenplay.YOUTUBE_DARK`); its EU consent page is declined before
# the take is filmed (`screenplay._decline`).
# Only the popular long videos, scrolled (2026-11-25: "don't show the
# channel's name and profile photo, instead scroll the most popular videos,
# show only long popular videos so we fit in the small time"): the header,
# tabs and side menu hidden. Then "it's hard to focus ... we do too much":
# Popular picked before filming (`before`), one slow scroll (`glide`), no
# cursor, no zoom.
CHANNEL_CHROME = ["#page-header-container", "#page-header", "yt-page-header-renderer",
                  "#page-header-banner", "#tabs-container", "#guide",
                  "ytd-mini-guide-renderer", "tp-yt-app-drawer"]
CH_CRYPTO = sp.Browser("https://www.youtube.com/@TheCrypto_Wiki/videos", [
    sp.wait(0.3), sp.glide(600, 3.5),
], dark=True, tail=8.0, lead=0.05, cookies=sp.YOUTUBE_DARK, hide=CHANNEL_CHROME,
    before=[sp.click("text=Popular >> nth=0"), sp.wait(1.5)])

# Tinnitus Help's most popular uploads are its sound-therapy sessions, not
# what the line is about (2026-11-25: "hide the sound therapies from the
# screen with code"): every grid item whose title ends in a duration -
# "(20 Minutes)", "(1 Hour)" - is removed as it renders, sorting included.
NO_SESSIONS = {"do": "js", "code": """(() => {
  const session = /\\(\\s*\\d+\\s*(minutes?|hours?)\\s*\\)\\s*$/i;
  const sweep = () => document.querySelectorAll("ytd-rich-item-renderer").forEach(el => {
    const t = el.querySelector("h3, #video-title");
    if (t && session.test(t.textContent.trim())) el.remove();
  });
  sweep();
  new MutationObserver(sweep).observe(document.body, {childList: true, subtree: true});
})()"""}
CH_TINNITUS = sp.Browser("https://www.youtube.com/@TinnitusHelpMe/videos", [
    sp.wait(0.3), sp.glide(900, 5.0),
], dark=True, tail=8.0, lead=0.05, cookies=sp.YOUTUBE_DARK, hide=CHANNEL_CHROME,
    before=[NO_SESSIONS, sp.click("text=Popular >> nth=0"), sp.wait(1.5)])

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

# Claude Code at work, as I use it (the editor, 2026-11-23: "sometimes show
# a Claude Code chat where we give prompts"). Reconstructed sessions: the
# prompts are what I asked, said plainly; the files are real, with their
# real sizes (`wc -l`, 2026-11-23) - the voice and wall beats were built for
# this video, the beat in `core/music.py` after "creepy and mysterious".
CLAUDE_BEATS = sp.Terminal(sp.claude_chat(
    "the opener needs the three voices as waveforms, with the real clips playing",
    "I'll add a voice beat: each row draws its clip's waveform and plays it "
    "as the row appears.",
    [("Write(video_automation/longform/beats/voice.py)", "Wrote 143 lines"),
     ("Write(video_automation/longform/beats/wall.py)", "Wrote 95 lines")],
    done="Both beats are registered. The opener renders with them."),
    viewport=(960, 540), lead=0.2, tail=10.0)

CLAUDE_MUSIC = sp.Terminal(sp.claude_chat(
    "the background music sounds creepy and mysterious, make it feel alive",
    "Pads alone have no pulse. I'll put the notes on a grid and add a soft "
    "kick underneath.",
    [("Update(video_automation/core/music.py)",
      "momentum: bpm=100, arp=0.26, kick=0.13")],
    done="Rendered night-drift with the new preset."),
    viewport=(960, 540), lead=0.2, tail=10.0)


# The page Oktay reads from (`tools/oktai_script.py`), scrolling the way the
# teleprompter does. The window names the file, not the folder it is in.
# Only the script: the page's header, instructions and Start button are
# hidden (2026-11-24: "crop the top of the screenshot where the instructions
# are and only leave the script"), and the shot carries a REC dot.
SCRIPT_PAGE = sp.Browser((folder(NAME) / "script.html").as_uri(), [
    sp.wait(0.8), sp.scroll(500), sp.wait(1.2), sp.scroll(500),
], dark=True, tail=8.0, hide=["header", "main > h2", "main > .meta", "#bar"])

RULE_RED = "rgba(235, 64, 52, 0.30)"
POLICY = sp.Browser("https://support.google.com/youtube/answer/1311392?hl=en", [
    sp.wait(0.8), sp.scroll(330), sp.wait(0.6),
    sp.click("text=repetitive or mass-produced"), sp.wait(0.6),
    # The rule's own words, highlighted (2026-11-24: "highlight the relevant
    # part in the screenshot with fitting colour"): red, a rule against the
    # viewer - and yellow vanished on the notice's own pale-yellow box.
    sp.mark("content that is repetitive or mass-produced", RULE_RED), sp.wait(1.0),
    sp.mark("always been ineligible for monetization", RULE_RED), sp.wait(3.4),
], dark=False, tail=10.0)


# --- the five windows: the roadmap, and every chapter's way in ------------------
#
# A strip of text cards the camera travels along (`reel`). The roadmap walks
# all five as they are named; each chapter's lead starts on the window before
# and travels to its own on the word that names it, then dives in.
CHAPTERS = [(GENERIC, "1 · The picture"), (EQUALIZER, "2 · The music"),
            (STOPWATCH, "3 · The first seconds"), (COPY, "4 · The template"),
            (MIC, "5 · The voice")]
# The roadmap: the five at once, a still of each, lit as they are named - a
# strip that travelled five windows in three seconds could not be read.
# Left to right is the order, so the tiles carry the names alone.
ROADMAP = Shot(graphic="logos", payload=(
    [(str(still(NAME, m, 2.0)), name) for (m, _), name in zip(
        CHAPTERS, ["The picture", "The music", "First seconds", "The template",
                   "The voice"])],
    "THE FIVE MISTAKES", None, True))


def chapter_window(path: list[int], enter: bool = True) -> Shot:
    """A chapter's way in: its own window from the first frame, a little
    further out so the windows already covered show beside it with their
    checks, then the dive (2026-11-24: "just start from the new card, no need
    to show the transition, just zoom out a bit to see the check on the
    previous one")."""
    return Shot(graphic="reel", payload=(CHAPTERS, "", enter, False, path[-1:],
                                         {"open": 0.78}))


# The slop, as the opener names it: one window per thing it repeats. Each
# is read in a written pause, and the template's travel runs in the pause so
# it lands on its words (2026-11-24: "add a gap on the voice before 'the same
# template' so there is also time to see the stock clips, then when the
# transition to the last card comes, continue the voice so it all matches").
SLOP = [(GENERIC, "AI videos"), (ROBOT, "The same robot voice"),
        (SERVERS, "The same stock clips"), (COPY, "The same template")]

# The pipeline, in the order it runs, on the one thing it all runs on.
PIPELINE = ([("Claude Code", str(logos.path("claude"))),
             ("Kokoro", str(logos.path("kokoro"))),
             ("Whisper", str(logos.path("openai"))),
             ("Python", str(logos.path("python"))),
             ("FFmpeg", str(logos.path("ffmpeg"))),
             ("n8n", str(logos.path("n8n")))],
            "HOW EVERY VIDEO IS MADE",
            (str(logos.path("claude")), "Claude Code runs every step"))


SECTIONS = [
    # --- the opener: the slop, then the twist ------------------------------------
    Section(
        title="AI slop",
        card=False,
        sentences=[
            ("The internet is full of AI videos right now.",),
            ("The same robot voice,",),
            ("the same stock clips,",),
            ("and the same template,", "over and over."),
            ("People call it AI slop.",),
            ("Viewers swipe it away in seconds,", "and YouTube won't pay for it."),
            ("I know this,", "because I made a lot of it myself."),
            ("For four months,", "I let AI make almost ninety videos",
             "for my two YouTube channels."),
            ("And Claude runs all of it.",),
            ("But for a long time,", "my videos looked like slop too."),
            # The message (fourth pass): said here, proved by every chapter.
            ("The AI wasn't the problem.",),
            ("The problem was that nobody checked what it made.",),
            ("So every time I found a mistake,", "I wrote it down."),
            ("That list is ten thousand lines long now.",),
            # A way into the five (2026-11-24: "we need an introduction to why
            # I list those five"), with "here is what I learned".
            ("Here is what I learned.",),
            ("Almost all of it comes down to five mistakes.",),
            ("The picture,", "the music,", "the first seconds,", "the template,",
             "and the voice."),
            ("Stay for the voice,", "because it's the reason I'm reading this myself."),
        ],
        # 1.0 after the slop strip: its last window is read before the cut
        # (2026-11-23: "very little time to see the stock clips card").
        # Pauses 1.0 / 1.8 -> natural / 1.0 (2026-11-25: "the first part with
        # the cards is too slow now, make it slightly faster", then "the gap
        # between the stock clips and the same template is too big").
        # A written pause under the 1.0 floor (`recorded.Pause`): 0.7 ("we
        # need to reduce it more"), then 0.3 (2026-11-25).
        gaps=[0.45, 0.4, Pause(0.3), 1.0, 0.45, 0.5, 0.45, 0.5, 0.45, 0.45, 0.4, 0.5,
              0.4, 0.5, 0.4, 0.4, 0.5, 0.6],
        shots=[
            # A strip of the slop: the camera reaches a window per thing named.
            # "The same template" waits for "over and over", so the stock
            # clips window is up for two phrases (2026-11-24: "still too
            # short ... I can't even read the text").
            Shot(graphic="reel", payload=(SLOP, "", False, False, [0, 1, 2, 3, 3],
                                          {"lead": [0.1, 0.1, 0.3, 0.25, 0.1],
                                           "travel": 0.8})),
            None,
            None,
            None,
            # A headline, typed big - as a quote it set small on the left
            # (draft, 2026-11-23).
            Shot(graphic="chapter", payload=("AI slop.", None, "headline", None, None)),
            screen(NAME, "policy", POLICY),
            screen(NAME, "yt-crypto", CH_CRYPTO, zoom=1.0),
            screen(NAME, "yt-tinnitus", CH_TINNITUS, zoom=1.0),
            # The pipeline as one beat: the steps arrive across the line.
            Shot(graphic="steps", ground="grid", payload=PIPELINE),
            Shot(clip=COIN, window=YT_PRICE, verdict=("wrong", "Slop"),
                 verdict_at=0.55),
            Shot(graphic="chapter", payload=("The AI wasn't the problem.", None,
                                             "headline", None, None)),
            Shot(graphic="lesson", payload=("problem", "Nobody checked what it made.",
                                            "the AI did the work, nobody judged it"),
                 emblem="clapper"),
            screen(NAME, "lessons", LESSONS),
            None,
            None,
            Shot(graphic="lesson", payload=("count", "mistakes", "it all comes down to",
                                            "5", True), emblem="clapper"),
            ROADMAP,
            None,
        ],
    ),

    # --- 1. the picture -----------------------------------------------------------
    Section(
        title="The picture",
        lead=("Let's start with the first one,", "the picture."),
        lead_shot=chapter_window([0]),
        lead_gap=2.2,
        sentences=[
            ("AI tools love stock footage.",),
            ("But a stock clip almost never shows", "what the voice is talking about."),
            ("Here is one example,", "from a video about quantum computers."),
            # "Replace", not "stopped that cut" (2026-11-24).
            ("I had to replace the clip three times.",),
            ("Each time, a random clip was playing", "under a very specific sentence."),
            # Three pieces for the three boxes (two arrived at once).
            ("So I made one rule:", "the screen has to show",
             "what the voice is saying."),
            ("Then I overcorrected.",),
            ("I put a big label", "on almost every shot,",
             "and the video turned into a slideshow."),
            ("Twenty five labels in four minutes.",),
            # A way in, not a jump (2026-11-24).
            ("And the last problem with the picture was the faces.",),
            ("Stock videos are full of smiling strangers,",
             "and a stranger's face says nothing about your topic."),
            ("So I stopped using stock faces.",),
            # No hands on screen: said, cut out of the voice (`DROPS`), not
            # in the subtitle (2026-11-23).
            (("Now it's screens,", "Now it's hands, screens,"), "and drawings."),
            ("When there's no real picture of an idea,", "I draw the idea itself."),
            ("There are more than forty of them now,", "and they move with the voice."),
            ("And when I need a new one,", "Claude builds it for that video."),
            ("If you make AI videos,", "check every clip against its sentence."),
        ],
        # 3.0 after the drawn graphics' wall, so its tiles play out (2026-11-24:
        # "give extra 2-3 seconds to see the animation screens").
        gaps=[0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 1.0, 0.4, 0.4, 0.4, 0.4, 0.4, 3.0,
              0.4, 0.4, 0.6],
        shots=[
            Shot(clip=CAMERAMAN, verdict=("wrong", "Says nothing"), verdict_at=0.62),
            None,
            # Data on screen, data in the ear: bit chirps, not a server
            # room's fans (2026-11-24: "unrelated background sfx").
            Shot(clip=SERVERS, window=YT_QUANTUM, ambience="digital"),
            Shot(graphic="lesson", payload=("count", "times", "I replaced the clip",
                                            "3", "\U0001F6D1"), emblem="clapper"),
            Shot(clip=CHAIN, window=YT_QUANTUM, verdict=("wrong", "Random"),
                 verdict_at=0.5),
            Shot(graphic="diagram", payload=([
                ("Your address", "hides your public key", "\U0001F512"),
                ("Your first spend", "publishes the key", "\U0001F4E4"),
                ("A quantum computer", "could work back from it", "⚠️")],
                "WHAT THE SENTENCE SAYS", False),
                # An example, so it is framed as one (2026-11-23).
                window=("player", "The same sentence, drawn"),
                verdict=("right", "Shows the idea"), verdict_at=0.75),
            Shot(clip=CODE, payload=("", "QUANTUM COMPUTERS"), window=YT_ETHEREUM),
            # The overcorrection, as a strip: a label on every window. Two
            # stops over three captions, so each can be read (the editor,
            # 2026-11-23: "the cards move way too fast").
            # The labels as they were: plain type on the footage, not a card's
            # title (2026-11-24: "put them on top of the footage ... like the
            # real example, just plain text on top").
            Shot(graphic="reel", payload=([(CODE, "Quantum computers"),
                                           (CHAIN, "Public keys"),
                                           (GENERIC, "The blockchain")], "", False,
                                          False, [0, 0, 1], {"labels": "over"}),
                 verdict=("wrong", "A slideshow"), verdict_at=0.82),
            Shot(graphic="lesson", payload=("count", "labels", "in a four minute video",
                                            "25", "\U0001F3F7\uFE0F"), emblem="clapper"),
            Shot(clip=SMILE_A),
            Shot(clip=SMILE_B, verdict=("wrong", "A stranger"), verdict_at=0.6),
            # Two small tiles in an empty frame read as nothing (2026-11-23):
            # the fix, on the lesson card.
            Shot(graphic="lesson", payload=("fix", "No stock faces.",
                                            "screens and drawings instead"),
                 emblem="clapper"),
            None,
            Shot(graphic="wall", payload=(WALL, "MY DRAWN GRAPHICS")),
            # The chat runs under two sentences, so it can finish.
            # No zoom, no idle sped up: the whole chat, at its own pace
            # (2026-11-24: "too quick to read the prompt ... don't zoom").
            screen(NAME, "claude-beats", CLAUDE_BEATS, zoom=1.0, idle=1.0),
            None,
            Shot(graphic="lesson", payload=("learned", "Check every clip against its sentence.", "", None, None,
                                            "IF YOU MAKE AI VIDEOS"), emblem="clapper"),
        ],
    ),

    # --- 2. the music: played, the bed paused under it -----------------------------
    Section(
        title="The music",
        lead=("The second mistake", "was the music."),
        lead_shot=chapter_window([0, 1]),
        lead_gap=2.2,
        sentences=[
            # Claude made it - human and AI together beat either alone (the
            # editor, 2026-11-23).
            # Said with "the"; "the" is cut (`DROPS`), not in the subtitle.
            (("Here is the first background track Claude made with code.",
              "Here is the first background track Claude made with the code."),),
            ("And here is the one under every video right now.",),
            ("The first one was just a few slow chords,", "and it sounded creepy."),
            ("The fix was rhythm:", "notes on a grid,", "and a soft beat underneath."),
            ("And because it's the same track every time,",
             "it became the sound of the channel."),
            ("If you make AI videos,", "listen to the music on its own before you use it."),
        ],
        gaps=[_after(BED_OLD), _after(BED_NOW), 0.5, 0.5, 0.5, 0.6],
        shots=[
            Shot(graphic="voice", ground="grid", payload=(MUSIC,),
                 samples=(BED_OLD, BED_NOW)),
            None,
            # "it sounded creepy" is my prompt; "the fix was rhythm" is Claude's
            # answer - one chat under both lines.
            screen(NAME, "claude-music", CLAUDE_MUSIC, zoom=1.0, idle=1.0),
            None,
            Shot(graphic="voice", ground="grid", payload=(MUSIC[1:],), emblem="note"),
            Shot(graphic="lesson", payload=("learned", "Listen to the music on its own first.", "", None, None,
                                            "IF YOU MAKE AI VIDEOS"), emblem="note"),
        ],
    ),

    # --- 3. the first seconds ---------------------------------------------------
    Section(
        title="The first seconds",
        lead=("The third mistake", "was in the first seconds."),
        lead_shot=chapter_window([1, 2]),
        lead_gap=2.2,
        sentences=[
            ("I checked how long viewers stayed", "on eleven of my Shorts."),
            ("In six of them,", "the second sentence gave the answer away."),
            ("Half the viewers were gone", "after about nine seconds."),
            ("The other five saved the answer for later.",),
            ("They kept half their viewers", "for about eighteen seconds."),
            ("That's twice as long.",),
            ("So now,", "the answer always comes later."),
            ("If you make AI videos,", "keep the answer out of your second sentence."),
        ],
        shots=[
            Shot(graphic="phones", payload=([
                # The times only (2026-11-23: "remove the sentences in quotes").
                (HAL, "Half gone at 7.1s", ""),
                (JAW, "Half gone at 28.8s", "")],
                "TWO OF MY SHORTS")),
            # The questions are the Shorts' titles, read with yt-dlp 2026-11-24.
            Shot(graphic="bars", payload=([row("Hal Finney.", 7.1, "It was Hal Finney.",
                                               "Who built digital money before Bitcoin?"),
                                           row("Not because of its price.", 8.0,
                                               "Not because of its price.",
                                               "Is a cheap coin easier to double?"),
                                           row("One explosion did, on set in 1967.", 8.8,
                                               "One explosion did it.",
                                               "Did Star Trek give Kirk and Spock tinnitus?")],
                                          "GAVE IT AWAY: HALF GONE BY")),
            None,
            Shot(graphic="bars", payload=([row("A line from a newspaper's front page.", 17.2,
                                               "It starts with a newspaper.",
                                               "What is hidden in Bitcoin's first block?"),
                                           row("Not a person. It is an exchange.", 18.3,
                                               "It's not a person.",
                                               "Who is the biggest Bitcoin whale?"),
                                           row("Quick check - are your teeth touching?", 28.8,
                                               "Are your teeth touching?",
                                               "Can your jaw change your tinnitus?")],
                                          "KEPT IT FOR LATER: HALF GONE BY")),
            None,
            None,
            Shot(graphic="lesson", payload=("fix", "Keep the answer for later.",
                                            "eleven Shorts, one pattern"), emblem="chart"),
            Shot(graphic="lesson", payload=("learned", "Keep the answer out of your second sentence.", "", None, None,
                                            "IF YOU MAKE AI VIDEOS"), emblem="chart"),
        ],
    ),

    # --- 4. the template -----------------------------------------------------------
    Section(
        title="The template",
        lead=("The fourth mistake", "was the template."),
        lead_shot=chapter_window([2, 3]),
        lead_gap=2.2,
        sentences=[
            ("When one pipeline makes every video,", "they all start to look the same."),
            ("Here's how that looked on my channel:", "the same layout,", "every time."),
            ("And YouTube has a rule about exactly this.",),
            ("Videos that are repetitive or mass produced", "can't earn money there."),
            ("So the problem isn't AI.",),
            ("It's videos that all look the same.",),
            ("So now every video gets something made just for it,",
             "like the sound waves in this one."),
            ("If you make AI videos,", "give each one something only it has."),
        ],
        # A beat after the wall, so its numbers finish counting (2026-11-24),
        # and more again (2026-11-24, fifth review: "give extra 1-2 seconds
        # to see the animations").
        gaps=[0.4, 2.7, 0.4, 0.4, 0.4, 0.4, 0.5, 0.6],
        shots=[
            Shot(graphic="lesson", payload=("problem", "One pipeline for every video.",
                                            "so every video looks the same"),
                 emblem="clapper"),
            Shot(graphic="wall", payload=([
                ("stat", ("1.1M", "coins", "never moved")),
                ("stat", ("3", "timestamps", "flagged in one cut")),
                ("stat", ("25", "labels", "in a four minute video")),
                ("stat", ("89", "videos", "since July")),
            ], "SAME LAYOUT, EVERY TIME")),
            screen(NAME, "policy", POLICY),
            None,
            Shot(graphic="logos", payload=([L("youtube", "YouTube"), L("tiktok", "TikTok"),
                                            L("instagram", "Instagram"),
                                            L("facebook", "Facebook")],
                                           "THE PROBLEM ISN'T AI")),
            None,
            # An example, so it plays in a window, not as this context's graph.
            Shot(graphic="voice", ground="grid", payload=(VOICES,),
                 window=("player", "Made for this video: the voices as waveforms"),
                 verdict=("right", "Made for this one"), verdict_at=0.6),
            Shot(graphic="lesson", payload=("learned", "Give each video something only it has.", "", None, None,
                                            "IF YOU MAKE AI VIDEOS"), emblem="clapper"),
        ],
    ),

    # --- 5. the voice: why I read it myself -----------------------------------------
    Section(
        title="The voice",
        lead=("And the last mistake", "was the voice."),
        lead_shot=chapter_window([3, 4]),
        lead_gap=2.2,
        sentences=[
            ("Here's how the AI voice on my channels sounded at first.",),
            ("And here is how it sounds today.",),
            ("It took three fixes to get there.",),
            ("The first fix was the speed.",),
            ("When an AI voice sounds robotic,", "most people slow it down."),
            ("But I found the opposite.",),
            ("At a hundred and fifty words a minute,", "it sounded robotic."),
            ("At a hundred and ninety,", "the same voice sounded natural."),
            ("The second fix was how the script goes in.",),
            # One caption: each caption plays a sample, and the second
            # started over the voice (draft, 2026-11-23).
            ("Here it is, one line at a time.",),
            ("And here is the whole paragraph at once.",),
            ("Line by line,", "every sentence starts high again."),
            ("As one paragraph,", "the voice settles down."),
            ("The third fix was one-word sentences.",),
            ("Listen to just one word.",),
            ("And the same word inside the sentence.",),
            ("On its own,", "the word goes up and never comes down."),
            ("It sounds like a question.",),
            ("So the fix isn't a better voice.", "It's a full sentence."),
            ("If you make AI videos,", "make the voice faster,", "and give it whole paragraphs."),
        ],
        gaps=[_after(OLDEST), _after(TODAY), 0.45, 0.4, 0.45, 0.4, 0.45, 0.6, 0.45,
              _after(SPLIT), _after(RUN), 0.45, 0.5, 0.45, _after(MONEY),
              _after(MONEY_FULL), 0.45, 0.5, 0.5, 0.9],
        shots=[
            # The two AI voices only: "Me" waits for me (2026-11-24).
            # The note keeps the comparison honest: two engines, one script
            # (2026-11-24, the editor asked for "both are created with the
            # same text to speech model"; the first is macOS `say`, so the
            # note says what is true, his choice).
            Shot(graphic="voice", ground="grid", payload=(VOICES[:2], FOOTNOTE),
                 samples=(OLDEST, TODAY)),
            None,
            Shot(graphic="lesson", payload=("count", "fixes", "to get there", "3",
                                            "\U0001F527"), emblem="microphone"),
            Shot(graphic="lesson", payload=("problem", "If it sounds robotic, slow it down.",
                                            "what most people do", None, None,
                                            "THE OBVIOUS FIX"), emblem="microphone",
                 verdict=("wrong", "Backwards"), verdict_at=0.75),
            None,
            Shot(graphic="bars", payload=([("Slower", 151 / 192, "151 a minute: robotic"),
                                           ("Faster", 1.0, "192 a minute: natural")],
                                          "WORDS PER MINUTE")),
            None,
            None,
            Shot(graphic="lesson", payload=("fix", "How the script goes in.", "", None,
                                            None, "FIX 2"), emblem="wave"),
            Shot(graphic="voice", ground="grid", payload=([
                ("One line at a time", "every sentence on its own", SPLIT),
                ("The whole paragraph", "all at once, one breath", RUN)],),
                samples=(SPLIT, RUN)),
            None,
            # Measured in `docs/video/voice.md`: five lines alone opened at
            # 227-271 Hz; the same five as one run sat at 199, falling to 193.
            Shot(graphic="bars", payload=([("Line by line", 1.0, "227 to 271 Hz, every line"),
                                           ("One paragraph", 199 / 271,
                                            "199 Hz, falling to 193")],
                                          "WHERE EACH SENTENCE STARTS")),
            None,
            # Where a one-word line came from: my old chapter titles, read on
            # their own (2026-11-23: "make clear why one word would be read").
            # An older video's chapter title, the word the next lines play
            # (2026-11-24: one from this video was confusing).
            Shot(graphic="chapter", payload=("Money.", None, "grid", 2, "CHAPTER"),
                 window=("player", "An older video: its chapter title, read on its own")),
            Shot(graphic="voice", ground="grid", payload=([
                ("Money.", "one word, on its own", MONEY),
                ("That's where the money goes.", "the same word, in a sentence", MONEY_FULL)],),
                samples=(MONEY, MONEY_FULL)),
            None,
            Shot(graphic="chart", payload=([211, 232, 251, 266, 274, 274, 274],
                                           "ONE WORD, ITS PITCH", 4, "never falls")),
            None,
            Shot(graphic="voice", ground="grid", payload=([
                ("Money.", "one word, on its own", MONEY),
                ("That's where the money goes.", "the same word, in a sentence", MONEY_FULL)],),
                verdict=("right", "A full sentence"), verdict_at=0.35),
            Shot(graphic="lesson", payload=("learned", "Faster, and whole paragraphs.", "", None, None,
                                            "IF YOU MAKE AI VIDEOS"), emblem="microphone"),
        ],
    ),

    # --- why I read it myself -----------------------------------------------------
    Section(
        title="Why I read it myself",
        card=False,
        sentences=[
            ("Every fix in this video", "was a choice I had to make,", "listen to,",
             "and check."),
            ("The AI did the work.", "I did the judging."),
            ("And that's the difference", "between slop and a real video."),
            ("So on this channel,", "I read every script myself."),
            # "English isn't my first language, but my own voice makes every
            # video mine" is out (2026-11-24): its pickup's voice and room did
            # not match the take, and the camera box is the take's only.
            ("Claude still writes the drafts,", "edits the video,", "and uploads it."),
            ("But the voice is mine,", "and every number on screen is real."),
            # As he said them on the third take (2026-11-23): "here is", "please".
            ("Thanks for watching,", "and if you enjoyed it,", "please subscribe for more."),
        ],
        shots=[
            screen(NAME, "lessons", LESSONS),
            # Me as the judge, not Kokoro (2026-11-24: "show me in the icon
            # because I'm the judge in the context ... replace the draft
            # voice with the judging").
            Shot(graphic="logos", payload=([L("claude", "The work"),
                                            (str(ME), "The judging")],
                                           "WHO DOES WHAT")),
            Shot(graphic="lesson", payload=("learned", "AI does the work. I do the judging.",
                                            "the difference between slop and a real video"),
                 emblem="clapper"),
            screen(NAME, "script-page", SCRIPT_PAGE, window=("browser", "script.html"),
                   rec=True),
            Shot(graphic="logos", payload=([L("claude", "Drafts"), L("ffmpeg", "Edit"),
                                            L("n8n", "Upload")],
                                           "STILL THE AI")),
            screen(NAME, "yt-tinnitus", CH_TINNITUS, zoom=1.0),
            # The end screen: big, centred, no channel name; the camera box
            # comes in with it and stays (2026-11-23).
            Shot(graphic="chapter", payload=("Thanks for watching", None, "headline",
                                             None, None)),
        ],
    ),
]

# Lines added after a take, marked NEW on the script page and listed
# first for him to read into `pickups.mov`. The fourth pass's fourteen are
# recorded (2026-11-24, `pickups.mov`) and used by the build.
PICKUPS: list[str] = []

# The camera box: not on the opener (the slop comes first), but the moment
# the person arrives, and on the asides. Read by the script page too. Each
# leaves with its own sentence (`facecam.cues`, 2026-11-23).
FACE_HOOK = False
# Not "I know this" or "Then I overcorrected" (2026-11-23: "don't show the
# first and second face cams, it's not that good; leave the others").
# Only the take's own face: no box on a pickup (its room and light differ),
# none on the end screen (2026-11-24).
FACE = [("So on this channel", 4.5)]

META = Meta(
    title=TITLE,
    hook="AI didn't make my videos slop. Nobody checking what it made did. In 89 "
         "videos, these are the five mistakes I had to catch, and what fixed each.",
    url="https://oktayshakirov.com",
    summary="I made 89 videos with Claude Code running every step. The AI was never "
            "the problem - the slop came from nobody checking its picture, music, "
            "first seconds, template and voice. The five mistakes, with my own "
            "numbers, the fixes, and one rule for your own AI videos.",
    tags=["ai slop", "ai video", "ai voice", "faceless youtube", "youtube automation",
          "claude code", "oktai"],
    # No audiobook anywhere (his call, 2026-11-22: "out of topic").
    cta="More of what I build: https://oktayshakirov.com",
)

# Each script is its own recording now (`long.mov`, `short.mov`); a shared
# `recording.mov` needs `(start, end)` seconds here (`oktai.recording`).
WINDOW = (0.0, 492.1)   # both scripts in one take, 2026-11-23: "Short." at 8:12


# The editor's pick of a take where the matching spliced two reads: "AI
# tools love..." broken off, then the whole line again at 2:37 (third take).
# Ends at 159.60, after the "-ge" (159.44-159.56): at 159.52 the word lost
# its last sound (2026-11-24, "1:05 we cut the last letter from Footage").
PINS = {"AI tools love stock footage.": (157.38, 159.60),
        # The pickup (2026-11-24): "Here is", a throat-clear, then the whole
        # line again - Whisper made the first two one 1.5 s "what".
        "Here is what I learned.": (604.98, 606.45)}
# "hands," out of "Now it's hands, screens, and drawings" (third take, 3:31);
# "the" out of "made with the code" (2026-11-24: "made with code" is how it
# is said the first time it comes up): from the end of "with" to the
# closure before "code".
DROPS = [(211.455, 211.93), (240.778, 240.965)]


# After "Thanks for watching" and the TV-off: 2.5 s of black, a line and an
# arrow down to the description (2026-11-24, the editor: "quick 2-3 seconds
# black screen with simple text ... with arrow pointing down"). The link is
# the free prompt (`why-ai-videos-feel-fake.prompt.md`), on
# oktayshakirov.com/prompts once that page exists. Wording: his pick.
CODA = ("Free prompt for all 5 fixes", "in the description")


def main() -> None:
    made = build_long(SECTIONS, NAME, face=FACE, hook=3.0 if FACE_HOOK else None,
                      meta=META, emblem="microphone", window=WINDOW, pins=PINS,
                      drops=DROPS, last=None, coda=CODA,
                      draft="--draft" in sys.argv)
    for k, v in made.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
