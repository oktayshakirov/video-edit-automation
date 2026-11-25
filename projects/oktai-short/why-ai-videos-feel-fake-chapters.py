"""Why AI videos feel fake - five Shorts, one per mistake, cut from the long
form (2026-11-23).

The editor: "create more Shorts for each step using the same or similar
introduction, using the footage you have from the long version (optimally
part of the skill: I read one script, we first make the long, then use some
of the content for Shorts, like for the other projects)".

Every line here is one Oktay already read in the third take: the long form's
lines (`oktai.from_long` finds each by its opening words and keeps its
picture and pause) and the Short's own opener. So nothing new is recorded.
Each Short is the same three-line introduction - the slop, its name, "my
videos looked like slop too" - then one chapter told in order, ending on its
fix. Screens recorded for 16:9 are taken again vertical for these.

Run: `PYTHONPATH=. .venv/bin/python projects/oktai-short/why-ai-videos-feel-fake-chapters.py [picture|music|first-seconds|template|voice|all] [--draft]`
"""

import importlib.util
import sys
from pathlib import Path

from video_automation.core import screenplay as sp
from video_automation.crypto.shots import Shot
from video_automation.oktai import build_short, from_long, screen

HERE = Path(__file__).resolve().parent


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LONG = _load(HERE.parent / "oktai-long/why-ai-videos-feel-fake.py")
SHORT = _load(HERE / "why-ai-videos-feel-fake.py")
NAME = LONG.NAME

# The introduction (2026-11-24, the editor: "the Shorts can start the same
# with the cards, but not all should use 'people call it AI slop' and 'for a
# long time mine looked like slop too' ... a better transition into the step
# ... make clear this is one of five ... end with: check my channel for the
# other four"). The cards, the stake, "here is what I learned", which of the
# five this is - then the chapter, its rule, and the way to the other four.
OPENER = SHORT.SENTENCES[0]
NUMBER = {"picture": "one", "music": "two", "first-seconds": "three",
          "template": "four", "voice": "five"}
TOPIC = {"picture": "the picture", "music": "the music",
         "first-seconds": "the first seconds", "template": "the template",
         "voice": "the voice"}
INDEX = {k: i for i, k in enumerate(NUMBER)}
SLOP_NAME = ("picture", "template")     # the two about how slop looks


def extra(chapter: str) -> dict:
    """This Short's own lines: the opener, its number, and the ending."""
    lead = (f"Mistake {NUMBER[chapter]} of five: {TOPIC[chapter]}.",)
    return {
        "OPENER": (OPENER, Shot(graphic="reel", payload=(SHORT.SLOP, "")),
                   SHORT.GAPS[0]),
        "I know, because I made": (SHORT.SENTENCES[3], screen(
            NAME, "yt-crypto", SHORT.CH_CRYPTO, vertical=True, zoom=1.0), 0.4),
        "LEAD": (lead, LONG.chapter_window([INDEX[chapter]]), 0.9),
        "END": (("That's one of five mistakes.", "The other four are on my channel."),
                Shot(graphic="logos", payload=LONG.ROADMAP.payload), 0.6),
    }


def intro(chapter: str) -> list:
    keys = ["OPENER"]
    if chapter in SLOP_NAME:
        keys.append("People call it AI slop.")
    return keys + ["I know, because I made", "Here is what I learned.", "LEAD"]


CHAPTERS = {
    "picture": ["AI tools love stock footage", "But a stock clip almost never",
                "Here is one example", "I had to replace the clip",
                "Each time, a random clip", "So I made one rule"],
    "music": ["Here is the first background track", "And here is the one under",
              "The first one was just", "The fix was rhythm",
              "And because it's the same track"],
    "first-seconds": ["I checked how long viewers stayed", "In six of them",
                      "Half the viewers were gone", "The other five saved",
                      "They kept half their viewers", "That's twice as long",
                      "So now"],
    "template": ["When one pipeline makes every video", "Here's how that looked",
                 "And YouTube has a rule", "Videos that are repetitive",
                 "So the problem isn't AI", "It's videos that all look the same"],
    "voice": ["When an AI voice sounds robotic", "But I found the opposite",
              "At a hundred and fifty", "At a hundred and ninety",
              "Listen to just one word", "And the same word inside",
              "On its own", "It sounds like a question",
              "So the fix isn't a better voice"],
}

RULE = {"picture": "If you make AI videos, check every clip",
        "music": "If you make AI videos, listen to the music",
        "first-seconds": "If you make AI videos, keep the answer",
        "template": "If you make AI videos, give each one",
        "voice": "If you make AI videos, make the voice faster"}

# The long form's music chat, in a phone's terminal: narrow, smaller type,
# the lines wrapping (the 16:9 one was cut at the left in 9:16).
CLAUDE_MUSIC_V = sp.Terminal(sp.claude_chat(
    "the background music sounds creepy and mysterious, make it feel alive",
    "Pads alone have no pulse. I'll put the notes on a grid and add a soft "
    "kick underneath.",
    [("Update(video_automation/core/music.py)",
      "momentum: bpm=100, arp=0.26, kick=0.13")],
    done="Rendered night-drift with the new preset.", box=40),
    viewport=sp.TERM_VERTICAL, font=15, lead=0.2, tail=10.0)

# Pictures of the Short's own: the screens taken again for 9:16, and a first
# picture where the long form held one from a line the Short leaves out.
OWN = {
    # The drawn sentence full-frame: in a 9:16 player its three boxes are cut.
    "picture": {"So I made one rule": Shot(
        graphic="diagram", payload=LONG.SECTIONS[1].shots[5].payload,
        verdict=("right", "Shows the idea"), verdict_at=0.75)},
    "music": {"The first one was just": screen(NAME, "claude-music-v", CLAUDE_MUSIC_V,
                                               vertical=True, zoom=1.0, idle=1.0)},
    "template": {"And YouTube has a rule": screen(NAME, "policy", SHORT.POLICY,
                                                  vertical=True)},
    "voice": {"When an AI voice sounds robotic": Shot(
        graphic="lesson", payload=("problem", "If it sounds robotic, slow it down.",
                                   "what most people do", None, None,
                                   "THE OBVIOUS FIX"), emblem="microphone",
        verdict=("wrong", "Backwards"), verdict_at=0.75)},
}


def lines(chapter: str):
    keys = intro(chapter) + CHAPTERS[chapter] + [RULE[chapter], "END"]
    sents, shots, gaps = from_long(LONG.SECTIONS, keys, extra(chapter))
    for k, key in enumerate(keys):
        if key in OWN.get(chapter, {}):
            shots[k] = OWN[chapter][key]
        if key == "Here is what I learned.":
            # Held on the site's grid of my videos, not the long form's terminal.
            shots[k] = None
    # Every pause the long form wrote stays: a sound example plays out in
    # it before the next line (2026-11-24: "the shorts still overlap the music
    # example or AI voice example with my voice over, we don't wait for it to
    # finish"), and a wall has its time to play.
    return sents, shots, gaps


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    which = list(CHAPTERS) if not args or args[0] == "all" else args
    for chapter in which:
        sents, shots, gaps = lines(chapter)
        # No camera box: these end on a picture the box would cover (the
        # drawn sentence's last box, 2026-11-23); the face is the main
        # Short's and the long form's.
        out, total = build_short(sents, shots, NAME, face=[], hook=None, last=None,
                                 gap=gaps, opener_holds=True, emblem="microphone",
                                 window=None, pins={**LONG.PINS, **SHORT.PINS},
                                 drops=LONG.DROPS, tag=chapter, free=True,
                                 draft="--draft" in sys.argv)
        print(chapter, out, round(total, 1))


if __name__ == "__main__":
    main()
