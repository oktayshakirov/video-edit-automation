"""Why AI videos feel fake - the Short of OktAI's opener (~40 s).

**Third pass (2026-11-23), the long form's new angle - AI slop:** the slop
everyone has seen, the stake (I made almost ninety of these), the voice then
and now, and the twist last - this voice is me. Told in order, one plain
sentence each, "I" and never "we" (one person, no team). Sources and the
example clips are the long form's (`projects/oktai-long/
why-ai-videos-feel-fake.py`); the Short never pitches.

The first voice is the deliberately worse one the editor asked for (macOS
`say`, Daniel), today's is the explainer voice (`noah`) - different engines,
so the line names what changed (a faster read, whole paragraphs) and never
"the same voice". The videos are shown, not counted: my own video page.

Run: `PYTHONPATH=. .venv/bin/python projects/oktai-short/why-ai-videos-feel-fake.py [--draft]`
"""

import sys

from video_automation.core import samples
from video_automation.core import screenplay as sp
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.oktai import build_short, examples, folder, screen

NAME = "why-ai-videos-feel-fake"
TITLE = "I made almost 90 AI videos. This is how they sounded."

EXAMPLE = ["Hi, I'm the voice of this channel.",
           "I read every script you hear on it."]
CLIPS = examples.make(folder(NAME) / "examples", {
    "oldest": ("oldest", EXAMPLE),
    "today": ("today", EXAMPLE),
})
OLDEST = samples.register(CLIPS["oldest"], "oktai-oldest")
TODAY = samples.register(CLIPS["today"], "oktai-today")


def _after(clip: str) -> float:
    return round(samples.DUR[clip] + samples.LEAD + 0.6, 2)


# "line by line" ran under the camera box on the last line (2026-11-22).
FOOTNOTE = "*Both are text-to-speech voices reading the same script."
ROWS = [("AI, at first", "a computer voice", OLDEST),
        ("AI, today", "my explainer voice", TODAY),
        ("Me", "reading it myself", None)]

V = STOCK / "videos"
GENERIC = V / "abstract-digital-data-particles-dark/34645139.mp4"
SERVERS = V / "data-center-servers-rack-dark/3130182.mp4"
# Footage in every card, never a text card (the editor, 2026-11-23).
ROBOT = V / "humanoid-robot-dark/8084493.mp4"
SLOP = [(GENERIC, "AI videos"), (ROBOT, "The same robot voice"),
        (SERVERS, "The same stock clips")]

# The channels themselves, not our sites' video pages (2026-11-25: "instead
# of showing our websites, show the YouTube channels. Sort by popular, show
# longs and shorts, and make sure it's in dark mode"): the Videos tab sorted
# by Popular, then the Shorts tab, Popular. YouTube's dark theme is its own
# cookie (`screenplay.YOUTUBE_DARK`); its EU consent page is declined before
# the take is filmed (`screenplay._decline`).
# The long form's take, the same steps.
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

# The long form's policy page, the same take (same steps, same capture).
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

# **Why we say all this first (2026-11-23, the editor: "the Short is good
# but maybe needs an introduction, why we say all this, like the long").**
# Lines 2 and 3 are the long form's, from the same take - the Short searches
# the whole recording (`WINDOW = None`), and every line it shares with the
# long form is worded differently, so each finds its own read.
SENTENCES = [
    ("The internet is full of AI videos right now,", "all with the same robot voice,",
     "and the same random stock clips."),
    ("People call it AI slop.",),
    ("Viewers swipe it away in seconds,", "and YouTube won't pay for it."),
    ("I know, because I made almost ninety of them.",),
    # 2026-11-24: "in both long and Short the intro is missing 'here is what
    # I learned'".
    ("Here is what I learned.",),
    ("This is how my AI voice sounded at first.",),
    ("And this is how it sounds today.",),
    ("A faster read, and whole paragraphs instead of single lines.",),
    ("But on this channel, a person reads the script.", "This voice is me."),
]
# No pause for the examples: they play under the next line (2026-11-24,
# `samples.cues(under=)`).
# Each voice example plays out in its own pause before the next line
# (2026-11-24: "the shorts still overlap the music example or AI voice
# example with my voice over, we don't wait for it to finish"), and the stock
# clips card is up a full second after its words (the long form's 0:06 note).
GAPS = [1.0, 0.4, 0.4, 0.4, 0.4, _after(OLDEST), _after(TODAY), 0.4, 0.4]
SHOTS = [
    Shot(graphic="reel", payload=(SLOP, "")),
    Shot(graphic="chapter", payload=("AI slop.", None, "headline", None, None)),
    screen(NAME, "policy", POLICY, vertical=True),
    screen(NAME, "yt-crypto", CH_CRYPTO, vertical=True, zoom=1.0),
    None,
    Shot(graphic="voice", ground="grid", payload=(ROWS[:1],), samples=(OLDEST,)),
    Shot(graphic="voice", ground="grid", payload=(ROWS[:2], FOOTNOTE),
         samples=(None, TODAY)),
    # The Short has no "hold the last shot": a picture of its own. 151 vs 192
    # words a minute: `audio-book-automation/docs/voice.md`.
    Shot(graphic="bars", payload=([("Slower", 151 / 192, "151 a minute"),
                                   ("Faster", 1.0, "192 a minute")], "A FASTER READ")),
    # The person, not a fourth row: a headline with the camera box under it
    # (2026-11-23: the box over the rows "is not optimal at this position").
    Shot(graphic="chapter", payload=("This voice is me.", None, "headline", None, None)),
]

# Lines to record after a take, listed first on the script page. This
# Short's own and the chapter Shorts' seven are recorded (2026-11-24,
# `pickups.mov`) and used by the build.
PICKUPS: list[str] = []

# No box on the hook: the slop comes first; the face arrives with "a person
# reads the script". Read by `build_short` below and by the script page.
FACE_HOOK = False
FACE = [("But on this channel", 4.5)]

# Its own recording now (`short.mov`); a shared `recording.mov` needs
# `(start, end)` seconds here (`oktai.recording`).
# The whole take (2026-11-23): the Short now borrows two lines from the long
# form's read. Every shared line is worded differently, so each finds its own.
WINDOW = None
# The Short's own read of its first line (the long form's opener is close
# enough to win the match otherwise, 81%): from 8:17 in the third take.
PINS = {"The internet is full of AI videos right now, all with the same robot voice, "
        "and the same random stock clips.": (497.38, 504.2),
        # The clean read in the pickups, as in the long form's `PINS`.
        "Here is what I learned.": (604.98, 606.45),
        # Whisper's "A" took in a second of room and a lip click before it
        # (the report's "lasts 1.2s"): the line starts on the word.
        "A faster read, and whole paragraphs instead of single lines.": (517.24, 521.17)}


def main() -> None:
    out, total = build_short(SENTENCES, SHOTS, NAME, face=FACE,
                             hook=3.0 if FACE_HOOK else None, gap=GAPS,
                             opener_holds=True, emblem="microphone", window=WINDOW,
                             pins=PINS,
                             draft="--draft" in sys.argv)
    print(out, round(total, 1))


if __name__ == "__main__":
    main()
