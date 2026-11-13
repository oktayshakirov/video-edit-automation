"""Coffee, wine, salt - which one is making your tinnitus louder? ~45s Short.

Source: tinnitus-blog/content/posts/tinnitus-trigger-tracking.mdx, the same
post as the `what-makes-tinnitus-worse` long form, written in the same pass.

**The promise that stands out on this search** (2026-11-12, three
channels): the things making it louder. Teardown in
`demand/teardowns/what-makes-tinnitus-worse.md`. The long form takes the
search ("what makes tinnitus worse"); the Short names the suspects.

**Opening** (`shorts.md`, "The first eight seconds"): an 11-word title
question carrying the suspects, so sentence 2 starts near 4s. Sentence 2
is the article's own body-check - clench your jaw and listen
(`narration.md`, "Settled 2026-11-10": a check they can do in two seconds
with an answer they do not know) - and its first words stay on the
suspects ("Before you blame any of them"). The long form's `Stamp`
("It's the coffee." UNTESTED) lands on "blame". `opener_holds=True`.

**Easier to follow** (`shorts.md`, 2026-10-13): the check, then why the
rest needs a month (`diary`, built for this pair), then what the research
backs (`checklist`), then the instruction.

**Close (E16): a plain line that hands back to the title** - "Then you
will know which one it really is." runs into "Coffee, wine, salt - which
one...", on the clip it opened on. No `outro=`, no disclaimer.

**No medical claims.** The jaw check is a check, not a fix: "worth telling
a clinician". Nothing says cutting anything quietens it.

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/what-makes-tinnitus-worse.py
"""

import sys
from pathlib import Path

from video_automation.core import music
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Stamp
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "tinnitus-trigger-tracking"
DEMAND = ("Doctor Cliff '5 Things That are Making your Tinnitus LOUDER' 1.5M "
          "(138x), Treble 'Tinnitus Getting Worse? STOP These 7 Mistakes' "
          "202k (~19x); teardowns/what-makes-tinnitus-worse.md")
COVER_STYLE = "cutout"     # picked by the editor, 2026-11-13

V = STOCK / "videos"
P = STOCK / "photos"

# The long form's roster (screened there, see its header), plus the jaw.
COFFEE = V / "coffee-cup-steam-dark-background/6950169.mp4"   # 16s, B47, an espresso cup on a dark table (the long form has its own coffee)
CLOCK = V / "alarm-clock-night-dark/30039319.mp4"   # the long form uses it once, at 1.0
PROFILE = P / "man-profile-portrait-dark-background/19068090.jpg"

VOICE = "mia"           # same voice as the long form
MUSIC = music.track("night-drift")

# Low, on his sweater: the stamp lands while the spotlight's profile is
# already up, and centred it sat across his face (first cut).
OPENER = Stamp("It's the coffee.", "UNTESTED", at_word="blame",
               centre_y=0.70,
               # Not on frame one (the editor, 2026-11-13: it "stays for way
               # too long"): the title question plays clean, the quote comes
               # in on "louder", the stamp on "blame".
               enter_word="louder")

MONTH = [5, 4, 6, 9, 5, 4, 5,
         3, 5, 8, 6, 4, 3, 5,
         6, 4, 5, 9, 5, 4, 6,
         5, 8, 4, 6, 5, 9, 4]
WINE_DAYS = [3, 7, 12, 19]
GROUPS = [("Remembered", "the bad night after wine", [3]),
          ("Forgotten", "four bad nights, no wine", [9, 17, 22, 26]),
          ("Forgotten", "wine before a fine night", [7, 12, 19])]

SENTENCES = [
    ("Coffee, wine, salt - which one is really making your tinnitus louder?",),
    # spotlight - the whole profile, then the jaw.
    ("Before you blame any of them,",
     "clench your jaw and listen."),
    # The result, after a sentence gap long enough to do the check. It was
    # one sentence with silence spliced into it (`chunk_pad`), and the
    # splice cut the voice at "if the sound" (the editor, 2026-11-13).
    ("If the sound changed, that is worth telling a clinician about.",),
    # diary - the month, then one chunk per ringed group.
    ("The others take a month to test, because memory cheats.",
     "You remember the bad night after the wine,",
     "not the four bad nights without it,",
     "or the wine before a night that was fine."),
    ("Tinnitus moves on its own, so every bad day finds a culprit.",),
    # checklist, flow - one chunk per verdict.
    ("In the research, sleep holds up,",
     "stress holds up,",
     "but caffeine has shown no link."),
    # steps - one chunk per stop.
    ("So log it every day,",
     "for four weeks,",
     "before you give anything up."),
    # The close, said and captioned; it hands back to the title question.
    ("Then you will know which one it really is.",),
]

GAPS = [0.85,   # into sentence 2, after the opener
        1.30,   # the check needs time to be done
        0.80,   # into the diary
        1.30,
        0.80,   # into the checklist
        1.10,
        0.90,   # before the close
        0.34]

SHOTS = [
    Shot(clip=COFFEE, clip_at=0.5, clip_ax=0.50),
    Shot(graphic="spotlight",
         payload=(PROFILE, [(None, ""),
                            ((0.40, 0.42, 0.62, 0.72), "Clench your jaw")],
                  "")),
    # Picks up on the jaw where the last one stopped (`open_tight`).
    Shot(graphic="spotlight",
         # The same box as the jaw before it, or the cut zooms out.
         payload=(PROFILE, [((0.40, 0.42, 0.62, 0.72), "Changed? Tell a clinician")],
                  "", True, True)),
    Shot(graphic="diary",
         payload=(MONTH, WINE_DAYS, GROUPS, "ONE MONTH - AN EXAMPLE",
                  ("a glass of wine", "brighter = louder"), "\U0001F377")),
    Shot(clip=CLOCK, clip_at=5.0, clip_ax=0.50),
    Shot(graphic="checklist",
         payload=([("Sleep", True), ("Stress", True), ("Caffeine", False)],
                  "DOES IT HOLD UP?", True)),
    Shot(graphic="steps", ground="grid",
         payload=(["Log it daily", "For four weeks", "Then decide"],
                  "BEFORE YOU CUT ANYTHING")),
    # The close on the clip it opened on, later in it.
    Shot(clip=COFFEE, clip_at=7.5, clip_ax=0.50),
]

THUMB_HEADLINE = "What makes tinnitus\n[worse?]"


def thumbs(out: Path) -> list[Path]:
    """The long form's covers, drawn for 9:16 - the pair
    shares a picture and a question (`what-makes-tinnitus-worse` long,
    `cover()`)."""
    import importlib.util
    src = Path(__file__).resolve().parents[1] / "tinnitus-long/what-makes-tinnitus-worse.py"
    spec = importlib.util.spec_from_file_location("wmtw_long", src)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.thumbs(out, portrait=True)


def main() -> None:
    out = Path.home() / "Desktop/what-makes-tinnitus-worse-short.mp4"
    work = Path.home() / "Desktop/.what-makes-tinnitus-worse-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        # Not held: the next captions are two
                                        # beats away, so holding kept the stamp
                                        # over the spotlight to 10s. The
                                        # spotlight carries its own label, so
                                        # its exit leaves no bare frame.
                                        opener=OPENER, opener_holds=False,
                                        tail=1.5)
    print(f"{path}  {total:.1f}s")


if __name__ == "__main__":
    if "--thumb" in sys.argv:
        for p in thumbs(Path.home() / "Desktop/what-makes-tinnitus-worse-short-thumb.jpg"):
            print(p)
    else:
        main()
