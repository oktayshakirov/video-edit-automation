"""Did Star Trek give Kirk and Spock tinnitus? - vertical Short.

Source: tinnitus-blog/content/posts/celebrities-with-tinnitus.mdx. Paired with
`projects/tinnitus-long/celebrities-with-tinnitus.py`, same voice, same
photographs, same thumbnail.

**The single move.** The long form walks four stories; this does the one that
stops a scroll - Captain Kirk and Spock got tinnitus from the same explosion,
one in each ear - and follows Shatner to where he is now. Steve Martin, Neil
Young and Streisand belong to the long form.

**Frame one is a still, deliberately.** `shorts.md` says open on motion; it
also says the picture must say the noun of its own sentence, and sentence one
names Captain Kirk and Spock. The 1968 publicity still is the most
recognisable picture this channel has ever had, and the hook's punch-in and
the blurred-fill drift give it motion. The second shot is the explosion clip.

**The hook sits low (`hook_centre_y=0.68`).** At its default 34% it covers
both faces; the still is portrait, so no crop can move them. 0.68 puts it
over the starship model and the uniforms. The passthrough was added to
`render_crypto_short` for this cut; it defaults to `None`, so nothing shipped
moves.

**The hook passes the cover-the-bar test.** "One [explosion] gave them both
tinnitus" - a scene, an episode, a concert, a stunt would all fit the gap.
Sentence two says the word in its first three words.

**Cold close, no question** (`narration.md`, "A Short's ending loops"). It
lands on Shatner's own description - not cured, used to it - over the 2009
photograph of the two of them laughing, which answers the opening still
without re-asking it. "Used to it" is his account of himself, never a promise
to the viewer; the narration says "he says".

Run from the repo root:

    PYTHONPATH=. .venv/bin/python projects/tinnitus-short/celebrities-with-tinnitus.py
"""

from pathlib import Path

from PIL import Image

from video_automation.core import music
from video_automation.core.brand import TINNITUS
from video_automation.core.stock import CACHE as STOCK
from video_automation.crypto.shots import Shot
from video_automation.longform.thumb import render_short_thumb
from video_automation.tinnitus.article import render_tinnitus_short

SOURCE_POST = "celebrities-with-tinnitus"

ROOT = Path(__file__).resolve().parents[2]
CELEB = ROOT / "assets/tinnitus/celebrities"
KIRK_SPOCK = CELEB / "kirk-spock-1968.jpg"
SHATNER_NIMOY = CELEB / "shatner-nimoy-2009.jpg"
NIMOY_SALUTE = CELEB / "nimoy-salute-2011.jpg"
SHATNER_STAGE = CELEB / "shatner-stage-2020.jpg"
SHATNER_TALK = CELEB / "shatner-on-stage-talking.jpg"


def _ratio(p: Path) -> float:
    w, h = Image.open(p).size
    return w / h


V = STOCK / "videos"
BLAST = V / "special-effects-explosion-film-set/17807763.mp4"
TV = V / "vintage-television-static-dark-room/11999587.mp4"
WALK = V / "man-walking-alone-night-street-lamp/11839713.mp4"
VINYL = V / "vinyl-record-player-spinning-dark/19281032.mp4"
EVENT = V / "speaker-at-podium-microphone-dark-stage/19197406.mp4"
WALK2 = V / "man-walking-alone-night-street-lamp/11839716.mp4"

VOICE = "mia"
MUSIC = music.track("night-drift")

HOOK = "One [explosion] gave them both tinnitus"
OUTRO = "Not cured. Just [used to it.]"

SENTENCES = [
    ("Did Star Trek give Captain Kirk and Spock tinnitus?",),
    # Says the hidden word in its first three words. A fact, not the
    # verdict: it opens "so what happened to them".
    (("One explosion did, on set in 1967, and it hit them in opposite ears.",
      "One explosion did, on set in nineteen sixty-seven, and it hit them "
      "in opposite ears."),),
    (("Leonard Nimoy's was in his right ear.",
      "Leonard Neemoy's was in his right ear."),),
    ("William Shatner's is in his left.",),
    ("Shatner later said it never really went away.",),
    (("Nimoy lived with it for the rest of his life.",
      "Neemoy lived with it for the rest of his life."),),
    ("For Shatner, the years after were a long run of ups and downs.",),
    ("So he went looking for help, and found sound therapy and "
     "counselling.",),
    ("It is built around getting used to the sound, not removing it.",),
    ("And he has spent years since speaking up for tinnitus research.",),
    # The outro card lands on this one.
    ("Nearly sixty years on, he says he is not cured.",
     "Just used to it."),
]

GAPS = [0.85,   # into the partial answer
        0.80,   # into the two ears
        0.55,   # the two halves of one fact
        0.85,
        0.80,   # Shatner's own line
        0.85,
        0.70,
        0.55,
        0.80,
        0.90,   # into the closing line
        0.34]   # cold close

SHOTS = [
    Shot(image=KIRK_SPOCK, aspect=_ratio(KIRK_SPOCK)),
    Shot(clip=BLAST, clip_at=0.0, clip_ax=0.45),
    Shot(image=NIMOY_SALUTE, aspect=1.0, bias=0.40),
    Shot(image=SHATNER_STAGE, aspect=_ratio(SHATNER_STAGE)),
    Shot(clip=TV, clip_at=0.5, clip_ax=0.50),
    # Both of them, decades later - on Nimoy's line, not under the outro
    # card, which sits at 50% of the height and covered both faces.
    Shot(image=SHATNER_NIMOY, aspect=1.15, bias=0.40),
    Shot(clip=WALK, clip_at=1.0, clip_ax=0.50),
    # Shatner himself, not the hands-on-a-white-phone clip the first cut ran
    # here (cut on review).
    Shot(image=SHATNER_TALK, aspect=1.0, bias=0.35),
    # Not the headphones clip: a stranger's face filling a 9:16 frame under
    # a line about Shatner reads as Shatner. The sound itself, playing.
    Shot(clip=VINYL, clip_at=0.5, clip_ax=0.30),   # the label, not the bare platter
    Shot(clip=EVENT, clip_at=2.0, clip_ax=0.50),
    # The outro rides over lamps and a far-off figure: nothing under the card.
    Shot(clip=WALK2, clip_at=1.0, clip_ax=0.50),
]


def main() -> None:
    out = Path.home() / "Desktop/celebrities-with-tinnitus-short.mp4"
    work = Path.home() / "Desktop/.celebrities-with-tinnitus-short-work"
    path, total = render_tinnitus_short(SENTENCES, SHOTS, out, work,
                                        voice=VOICE, gap=GAPS,
                                        music=MUSIC, music_gain=0.85,
                                        hook=HOOK, hook_centre_y=0.68,
                                        outro=OUTRO, tail=2.0)

    # Same source and headline as the long form - "two Star Trek actors",
    # not "Kirk and Spock", because not everybody has watched it (the user's
    # note on the first cut). The faces are in the top half, so the type
    # takes the bottom band.
    thumb = render_short_thumb(
        out.with_name(out.stem + "-thumb.jpg"), TINNITUS,
        "How did two\nStar Trek actors\nget [tinnitus?]", image=KIRK_SPOCK,
        accent="red", ax=0.92, zoom=1.0, at=0.20, band="bottom", size=240)

    print(f"{path}  {total:.1f}s")
    print(f"{thumb}   <- Short cover")


if __name__ == "__main__":
    main()
