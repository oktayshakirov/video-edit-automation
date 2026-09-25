"""A reel exercising the 2026-09-25 format additions. **Not a publishable video.**

Two 16:9 clips, one per site, that exist so the additions can be *seen* without
building a whole video around them - the regression reel for this vocabulary:

* five beat shapes - `timeline`, `chart`, `map`, `anatomy`, `spectrum`
  (`longform/beats.py`)
* five new shot-to-shot moves - whip, glitch, flash, wipe, punch
  (`core/transitions.py`)
* the navigation chrome - a ticked progress bar and "2 of 5"
  (`longform/chrome.py`)
* a sound kit per site, which is why there are two clips rather than one
  (`core/sfx.py`, `KITS`)

**There is no narration**, deliberately. Every timing here is hard-coded
instead of measured from a voice track, so the reel costs no TTS and can be
re-rendered as many times as review takes. That is the one way it differs from
a real build: in production every `reveals` value comes from
`build_narration_aligned`, exactly as it does today.

The content of each beat is real subject matter from the two sites rather than
lorem ipsum, because a layout can only be judged against the length of text it
will actually have to hold.

    PYTHONPATH=. .venv/bin/python projects/demo/format-upgrades.py
"""

from pathlib import Path

from video_automation.core import music, sfx, transitions
from video_automation.core.brand import CRYPTO, TINNITUS
from video_automation.core.frame import LANDSCAPE
from video_automation.crypto.shots import Shot, render_shots
from video_automation.longform import audio as audio_mod
from video_automation.longform import chrome
from video_automation.longform.beats import make_beat

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "projects/demo/out"
BEATGROUND = ROOT / "assets/brand/beat-ground-crypto.jpg"
FPS = 30

CARD = 3.6          # a label card
BEAT = 9.0          # a beat, long enough to read every reveal land


def ev(start: float, n: int, first: float = 0.9, gap: float = 1.5) -> list[float]:
    """Reveal times, evenly spaced - the stand-in for measured caption times.

    In a real build these come from the narration. Spacing them by hand here
    is the only honest way to show the beats without paying for a voice track,
    and 1.5s is close to the real median gap between caption chunks.
    """
    return [start + first + i * gap for i in range(n)]


def sequence(items: list[tuple[str, tuple, str, float]], t0: float = 0.0,
             ground: Path | None = None):
    """Lay out shots end to end, each carrying the move it leaves on.

    `items` is (graphic, payload, transition, hold). The transition length
    comes from `transitions.XF` rather than one global number, which is the
    proposal: a whip has to be fast to read as a whip and a dissolve has to be
    slow to read as one at all.
    """
    shots, t = [], t0
    for graphic, payload, move, hold in items:
        shots.append(Shot(graphic=graphic, payload=payload,
                          backdrop=ground if graphic != "chapter" else None,
                          start=t, hold=hold,
                          transition=move, xfade=transitions.XF[move]))
        t += hold
    return shots, t


def label(text: str, note: str = "") -> tuple:
    """A chapter card used as a section label for the reel."""
    return (text, note)


# ---------------------------------------------------------------------------
# thecrypto.wiki - timeline, chart, map, and the loud sound kit.
# ---------------------------------------------------------------------------

CRYPTO_ITEMS = [
    ("chapter", label("A dated axis", "timeline"), "whip", CARD),
    ("timeline", ([("2009", "The first block is mined"),
                   ("2010", "Ten thousand coins buy two pizzas"),
                   ("2017", "The first retail mania"),
                   ("2021", "A country makes it legal tender"),
                   ("2024", "Spot funds list in the US")],
                  "WHY THE GAPS MATTER"), "flash", BEAT),

    ("chapter", label("A line that draws itself", "chart"), "whip", CARD),
    ("chart", ([12, 14, 13, 18, 26, 24, 31, 46, 42, 58, 77, 71, 64, 69, 66],
               "THE SHAPE, NOT THE NUMBER", 10,
               "the turn, not the top"), "glitch", BEAT),

    ("chapter", label("Pins on a plate", "map"), "whip", CARD),
    ("map", ([("Switzerland", 0.50, 0.34),
              ("Singapore", 0.76, 0.62),
              ("El Salvador", 0.20, 0.58),
              ("UAE", 0.62, 0.50)],
             "WHERE THE RULES ARE WRITTEN"), "wipe", BEAT),

    ("chapter", label("The moves themselves", "transitions"), "punch", CARD),
    ("grid", ([("whip", "into a chapter card"),
               ("glitch", "a contradiction"),
               ("flash", "a reveal"),
               ("wipe", "a comparison"),
               ("punch", "escalation"),
               ("push", "the default, unchanged")],
              "CHOSEN BY WHAT THE CUT MEANS"), "push", BEAT + 1.5),
]

# ---------------------------------------------------------------------------
# tinnitushelp.me - anatomy, spectrum, and the soft kit. Same reel, different
# instrument: nothing here slams, glitches or bitcrushes.
# ---------------------------------------------------------------------------

TINNITUS_ITEMS = [
    ("chapter", label("Callouts on a drawing", "anatomy"), "whip", CARD),
    ("anatomy", ([("The ear canal", 0.86, 0.22, "r"),
                  ("The eardrum", 0.72, 0.40, "l"),
                  ("The cochlea", 0.48, 0.52, "r"),
                  ("The hair cells", 0.30, 0.66, "l")],
                 "WHERE THE SOUND IS MADE"), "flash", BEAT),

    ("chapter", label("The sound, made visible", "spectrum"), "whip", CARD),
    ("spectrum", ((3400, 5200), "NOTCHED AUDIO",
                  "the notch, cut around your own tone", "notch"),
     "wipe", BEAT),

    ("chapter", label("Same reel, softer kit", "sound"), "punch", CARD),
    ("grid", ([("No slam", "the swell instead"),
               ("No glitch", "a reveal tick instead"),
               ("No bitcrush", "anywhere in the kit"),
               ("Whole kit at 0.72", "against the crypto levels")],
              "BUILT FOR A HEARING-SENSITIVE AUDIENCE"), "push", BEAT),
]


def beat_cues(shots) -> list[tuple[float, str]]:
    """A cue per reveal, plus the new beats' own sounds.

    A rough stand-in for `build._cues`, which resolves this from the shot list
    properly. It is here only so the reel has the item-level punctuation the
    real builds have - otherwise the transitions would be the only sound and
    the sound kits could not be compared.
    """
    out = []
    for s in shots:
        for r in (s.reveals or []):
            out.append((r, "reveal"))
        if s.graphic == "map":
            out += [(r, "drop") for r in (s.reveals or [])]
        if s.graphic in ("chart", "spectrum"):
            out.append((s.start + 0.9, "sweep"))
        if s.graphic == "chapter":
            out.append((s.start - 0.75, "riser"))
            out.append((s.start + 0.05, "impact"))
    return [(t, k) for t, k in out if t > 0]


def build(name: str, brand, items, preset: str, kit: str) -> Path:
    from video_automation.longform.beats import item_count

    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / f"{name}-work"
    work.mkdir(exist_ok=True)

    # **Only thecrypto.wiki has a beat ground.** Passing it to both was the
    # first render's mistake - it put the crypto photograph behind every
    # tinnitus beat. With none, `Beat.background` falls through to the brand's
    # own looping backdrop, which is what a real build does.
    shots, total = sequence(items, ground=BEATGROUND if brand is CRYPTO else None)
    for s in shots:
        n = item_count(s.graphic, s.payload)
        s.reveals = ev(s.start, n) if n else None

    # The chapter cards are the reel's own sections, so the progress bar's
    # ticks and the "n of N" counter come from where they start.
    cards = [i for i, s in enumerate(shots) if s.graphic == "chapter"]
    overlays = [chrome.ProgressBar([shots[i].start for i in cards], total,
                                   brand, LANDSCAPE)]
    overlays += [chrome.ChapterCount(k + 1, len(cards), shots[i].start,
                                     shots[i].hold, brand, LANDSCAPE)
                 for k, i in enumerate(cards)]

    picture = render_shots(
        work / "picture.mp4", shots, total, fps=FPS, frame=LANDSCAPE,
        transition="push", xfade=0.34,
        factory=lambda s, fr: make_beat(s, brand, fr),
        brand=brand, mark=brand.mark(int(LANDSCAPE.logo_w * brand.mark_scale)),
        overlays=overlays)

    # Sound. With no narration there is nothing to duck against, so the bed is
    # the track and the cues are mixed straight onto it - `sfx.mix` works off
    # the track's own peak either way.
    bed = music.write(work / "bed-src.wav", total + 4, preset)
    bed = audio_mod.render_bed(bed, work / "bed.wav", total, gain=0.5)
    track = sfx.mix(bed, work / "track.wav",
                    beat_cues(shots) + transitions.cues(shots),
                    gain=0.55, kit=kit)

    out = OUT / f"{name}.mp4"
    import subprocess
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(picture), "-i", str(track),
         "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "18",
         "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)],
        check=True)
    print(f"{out}  ({total:.1f}s)")
    return out


if __name__ == "__main__":
    build("crypto-upgrades", CRYPTO, CRYPTO_ITEMS, "tension", "crypto")
    build("tinnitus-upgrades", TINNITUS, TINNITUS_ITEMS, "calm", "tinnitus")
