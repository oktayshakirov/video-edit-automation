"""Did Beethoven have tinnitus? ~45s Short.

Source: tinnitus-blog/content/posts/did-beethoven-have-tinnitus.mdx, the same
post as the `did-beethoven-have-tinnitus` long form.

**Opener: the long form's `Search`** - the editor's call on the first cut
(2026-10-24), so the pair opens identically (`shorts.md`, "A pair may share
its opener"). The first cut opened on the redacted hook, `[not silence]`,
over "What did Beethoven hear, day and night?".

**That makes the opening question yes/no**, the shape `narration.md`
("Confirmed 2026-10-11") records as cliffing when sentence 2 says "yes". So
sentence 2 skips the yes and opens the how, as that section allows: "He
wrote down exactly what he heard, in a letter he asked a friend to keep
secret." What he heard is kept back for the letter card at ~9s, in his own
words. A known risk on the curve - check the 4-7s drop when it has views.

**Not the long form compressed** (2026-10-13): the plain story in the order a
viewer would ask it - what did he hear, how do we know, what did they try,
did quiet help, what was it - with his own letter as the payoff and one
drawn beat, the `diagram`.

**A cold close that loops into the title.** It opens on what Beethoven heard
day and night and ends on most of us hearing it too, in silence. No question.

**No medical claims.** The red flags and the disclaimer live in the long form
and the description.

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/did-beethoven-have-tinnitus.py
"""

from pathlib import Path

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.openers import Search
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "did-beethoven-have-tinnitus"

ROOT = Path(__file__).resolve().parents[2]
B = ROOT / "assets/tinnitus/beethoven"
HORNEMANN = B / "hornemann-1803.jpg"
STIELER = B / "stieler-1820.jpg"
VILLAGE = B / "heiligenstadt-1821.jpg"
CHAMBER = B / "anechoic-4.jpg"

# Same roster as the long form - a pair is one video. A Short runs under a
# minute, so no clip appears twice in it.
V = STOCK / "videos"
PIANO_BW = V / "pianist-hands-piano-keys-dark/3822008.mp4"
PAGES = V / "old-letter-candle-close-up/11530055.mp4"
BARK = V / "tree-bark-texture-dark-moody/6250415.mp4"
ALONE = V / "person-sitting-alone-silent-dark-room/36623804.mp4"
MOON = V / "moon-clouds-night-slow/5229463.mp4"
SMOKE = V / "candle-blown-out-smoke-dark/26885208.mp4"

VOICE = "noah"          # the noah test, pair 1 of 5 - same voice as the long form
MUSIC = music.track("night-drift")

# Shared with the long form; it types the question sentence 1 asks.
OPENER = Search("did beethoven have tinnitus")

OUTRO = "In a silent room, [most of us] hear it too."

LETTER = {"name": "Ludwig van Beethoven", "to": "to Franz Wegeler",
          "date": "Vienna, 29 June 1801", "avatar": str(HORNEMANN),
          "text": "My ears are [buzzing and ringing perpetually, day and "
                  "night.]"}

# espeak reads 1953 as "one thousand...", so it is respelled in the spoken
# half. Heiligenstadt and Wegeler are never said aloud here.
SENTENCES = [
    # The title question - the Search opener types it.
    ("Did Beethoven have tinnitus?",),
    # Skips the yes and opens the how; what he heard is the letter card's.
    ("He wrote down exactly what he heard, in a letter he asked a friend to "
     "keep secret.",),
    # post, as a letter - the lead-in, then his own words.
    ("In his own words,",
     "my ears are buzzing and ringing perpetually, day and night."),
    ("His doctors tried almond oil, river baths, even bark blisters on his "
     "arms.",),
    ("A quiet village did not bring his hearing back either.",),
    # The hinge into the experiment.
    (("In 1953, researchers sat eighty people with normal hearing in a "
      "soundproof room.",
      "In nineteen fifty-three, researchers sat eighty people with normal "
      "hearing in a soundproof room."),),
    ("Ninety-four percent heard a sound.",),
    # diagram - one chunk per node.
    ("In silence, most ears make a faint sound.",
     "The brain usually filters it out.",
     "With tinnitus, it gets through."),
    # The cold close, drawn by `outro=`.
    ("Beethoven heard it day and night. In a silent room, most of us hear "
     "it too.",),
]

# 1.00, not 0.70: at 0.70 sentence 2 began at ~2.3s, before the Search
# opener clears (2.6s), so its captions were muted whole and the frame
# carried no type until 7.1s. 1.00 is a real silence (`narration.md`).
GAPS = [1.00,   # into sentence 2, after the opener has gone
        0.60,
        1.10,   # the letter's highlight holds
        0.60,
        0.85,   # before the turn
        0.55,
        0.85,   # the number lands
        1.00,   # the diagram closes
        0.34]   # cold close, nothing after it

SHOTS = [
    # The hand and keys sit low in the frame, clear of the search bar.
    Shot(clip=PIANO_BW, clip_at=0.5, clip_ax=0.45),
    # Past 4s: before it, the turning page is a legible title page of somebody
    # else's book.
    Shot(clip=PAGES, clip_at=5.0, clip_ax=0.55),
    Shot(graphic="post", payload=("letter", LETTER, "HIS LETTER, 1801")),
    Shot(clip=BARK, clip_at=2.0, clip_ax=0.40),
    Shot(image=VILLAGE, aspect=2168 / 1512, zoom=1.04),
    Shot(clip=ALONE, clip_at=2.0, clip_ax=0.50),
    # The chamber is near-white, and as a framed card it put the caption on
    # its bottom edge (`shorts.md`, 2026-10-21) - an inset over smoke instead.
    Shot(clip=SMOKE, clip_at=0.0, clip_ax=0.50, inset=(CHAMBER, "top", 0.50)),
    Shot(graphic="diagram",
         payload=([("A faint sound", "most ears, in silence", "\U0001F507"),
                   ("The brain filters it", "most of the time", "\U0001F9E0"),
                   ("Tinnitus", "it gets through", "\U0001F514")],
                  "WHY MOST OF US NEVER HEAR IT", False)),
    # The outro card lands on this one and holds to the final frame.
    # 0.85 keeps the bright moon out from under the closing card.
    Shot(clip=MOON, clip_at=3.0, clip_ax=0.85),
]


def main() -> None:
    out = Path.home() / "Desktop/did-beethoven-have-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.did-beethoven-have-tinnitus-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        opener=OPENER, outro=OUTRO,
                                        tail=2.0)

    # The long form's Stieler portrait and its headline - one source for
    # both aspects.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "What did\nBeethoven\n[hear?]", image=STIELER,
        accent="orange", ax=0.50, zoom=1.0, at=0.30, band="bottom", size=230)

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
