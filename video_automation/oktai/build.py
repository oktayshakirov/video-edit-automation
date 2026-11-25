"""Build an OktAI pair from Oktay's recordings - or a draft before them.

The run differs from crypto and tinnitus in one place: **the script is read
by a person between writing and building.** So a project has two states:

* **No recording yet** - `build_long` / `build_short` render a *draft* with a
  Kokoro voice (`DRAFT_VOICE`), so the picture can be checked and the script
  heard before Oktay reads it. Drafts are named `-draft` and never shipped.
* **Recorded** - the files are in `~/Movies/OktAI/<name>/`, named `long.*`
  and `short.*` (any extension ffmpeg reads: `.mov`, `.mp4`, `.m4a`, `.wav`).
  A separate camera file is `long-cam.*` / `short-cam.*`. The voice is the
  recording (`core/recorded.py`), and the camera box goes on after the render
  (`core/facecam.py`) at the hook, the last line and every phrase in `face`.
  **One file for both** (he reads the script page top to bottom, 2026-11-22)
  is `recording.*`: each part passes `window=(start, end)` in seconds, since
  the Short repeats the long form's opening lines and the last take of a line
  would otherwise be taken from the wrong script.

Outputs go to the Desktop like every other project: `<name>-long.mp4`,
`<name>-short.mp4`, their SRTs and sidecars.

Screens are scripted, never recorded by hand: `screen(name, file, take)`
plays a `core/screenplay.py` take (a browser or a terminal) in headless
Chromium, records it to `screens/<file>.mp4`, and `core/screenrec.py` cuts
it (auto-zoom, click ripples, a drawn cursor, blur, the brand window).

The script for Oktay to read comes from `tools/oktai_script.py`, which reads
the same `SECTIONS` / `SENTENCES` through `reading_order` - so what he reads
is exactly what the build will look for.
"""

from __future__ import annotations

import os
from pathlib import Path

from ..core import facecam
from ..core.brand import OKTAI
from ..core.recorded import Recording

RECORDINGS = Path(os.environ.get("OKTAI_RECORDINGS",
                                 Path.home() / "Movies/OktAI"))
# Only for drafts. Kokoro's `am_michael` at the crypto test's speed - a male
# voice, so the draft's pacing is closer to Oktay's than `mia` would be.
DRAFT_VOICE = "noah"
MEDIA = (".mov", ".mp4", ".m4v", ".m4a", ".wav", ".mp3", ".aiff", ".aif")
# His read, sped up to this (within `recorded.SPEED_RANGE`), pitch kept:
# 218 since 2026-11-25 ("make my voice 10-15% faster", then 10%, 9%, 7.5%;
# after 200: "sped up
# slightly"), 190 before - the long form 1.17x -> ~1.32x. Captions, cuts and
# the camera box are timed from the same edit, so they follow.
TARGET_WPM = 215
# The long form's subtitles: YouTube yellow, small, at the bottom (the
# editor, 2026-11-23). The Short has its own captions.
SUBTITLES = (255, 214, 10)
# The channel's own bed (2026-11-24, the editor: "different background music
# for this channel ... most competitors don't have bg music, so something
# soft"): a soft track of its own, 6 dB under the other channels' level, up
# for the opening and each chapter's way in. The examples from the other
# channels keep their own music.
MUSIC = "oktai-bed"
# 12 dB under the other channels' beds (6 until 2026-11-24): under his voice
# by ~17 dB, where mixing guides put music under narration (18-20 dB) - his
# pick of four samples, "new tone" with the bed 6 dB lower.
MUSIC_LUFS = -35.0
DESKTOP = Path(os.environ.get("OKTAI_OUT", Path.home() / "Desktop"))
# His face photos for covers, kept across videos (the editor, 2026-11-25:
# "keep couple of my faces for thumbnails ... we will create more in future
# videos"). `<expression>.<ext>` is the photo he sent, `<expression>-cutout.png`
# the cover-ready cut-out; everything else of a video goes once it is uploaded.
FACES = RECORDINGS / "faces"


def folder(name: str) -> Path:
    return RECORDINGS / name


def _find(name: str, stem: str) -> Path | None:
    d = folder(name)
    if not d.is_dir():
        return None
    hits = [p for p in d.iterdir()
            if p.stem.lower() == stem and p.suffix.lower() in MEDIA]
    return sorted(hits)[0] if hits else None


def recording(name: str, part: str, window=None, pins=None,
              drops=None, free: bool = False) -> Recording | None:
    """The `long` or `short` recording of project `name`, or None.

    `long.*` / `short.*` first; else one `recording.*` holding both, searched
    only inside `window` (seconds) when given.

    `free`: every line is taken from its best read wherever it is, not in
    script order - for a Short cut from the long form (`from_long`), whose
    lines were read all over the take (2026-11-24: "I know, because I made
    almost ninety of them" came out as the long form's "I know this,
    because I made a lot of it", the one read before the chapter's lines).
    """
    audio = _find(name, part) or _find(name, "recording")
    if audio is None:
        return None
    pick = _find(name, "pickups")
    start = None
    if pick is not None:
        # Lines added after the take, read on their own (the script page's
        # "Record these"): appended to the recording, so every time in it -
        # pins, drops, windows - still holds, and the window takes in the
        # pickups too.
        audio, start = _with_pickups(audio, pick)
        if window:
            ranges = [tuple(window)] if isinstance(window[0], (int, float)) else list(window)
            window = ranges + [(start, 1e9)]
    # Pauses between sentences capped at 0.40 s (0.55 until 2026-11-23,
    # "reduce the gap between some sentences"), not the default 0.75: "make
    # me sound structured and not too slow" (his note on the first recording,
    # 2026-11-22). Long pauses inside a sentence are cut by `_tighten`.
    # And sped up to about 190 words a minute, pitch kept (his note on the
    # first recorded long form, 2026-11-22: "speed up my voice with about
    # 1.25 or 1.5 ... I read slower because I'm not native").
    if window and isinstance(window[0], (int, float)):
        window = tuple(window)
    return Recording(audio, video=_find(name, f"{part}-cam"),
                     window=window or None, max_pause=0.40,
                     target_wpm=TARGET_WPM, pins=dict(pins or {}),
                     drops=list(drops or []),
                     pickups_from=0.0 if free else start, pickups_at=start)


def _with_pickups(take: Path, pick: Path) -> tuple[Path, float]:
    """`take` with `pick` joined on its end, made once: the joined file and
    the second the pickups start at."""
    import json
    import subprocess

    def dur(p):
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "json", str(p)], capture_output=True, text=True).stdout
        return float(json.loads(out)["format"]["duration"])
    out = take.with_name(f"{take.stem}+pickups{take.suffix}")
    if not out.exists() or out.stat().st_mtime < max(take.stat().st_mtime,
                                                     pick.stat().st_mtime):
        lst = out.with_suffix(".txt")
        lst.write_text(f"file '{take}'\nfile '{pick}'\n")
        ok = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                             "-i", str(lst), "-c", "copy", str(out)]).returncode == 0
        if not ok:      # different codecs: join by re-encoding
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(take), "-i", str(pick),
                            "-filter_complex", "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                            "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18",
                            "-c:a", "aac", "-b:a", "256k", str(out)], check=True)
        lst.unlink(missing_ok=True)
    return out, dur(take)


def reading_order(sections=None, sentences=None) -> list[list]:
    """The sentences the voice says, in order - chapter titles included.

    Long form: `Section.parts()` puts each carded section's spoken title in
    front of its sentences, so the title is read aloud too. Short: the
    sentence list as it is.
    """
    if sections is not None:
        from ..longform.plan import flatten
        return [list(s) for s in flatten(sections)[0]]
    return [list(s) for s in sentences]


def _voice(name: str, part: str, draft: bool, window=None, pins=None,
           drops=None, free: bool = False):
    rec = None if draft else recording(name, part, window, pins, drops, free)
    if rec is None:
        why = "asked for" if draft else f"no {part}.* in {folder(name)}"
        print(f"DRAFT ({why}): Kokoro '{DRAFT_VOICE}' reads the {part} script")
        return DRAFT_VOICE, None
    print(f"recorded {part}: {rec.audio.name}"
          + (f" + camera {rec.video.name}" if rec.video else ""))
    return rec, rec


def _bed(kw: dict) -> None:
    """The channel's bed and level, unless a project chose its own."""
    from ..core import music
    if "music" not in kw and (music.TRACKS / f"{MUSIC}.wav").exists():
        kw["music"] = str(music.track(MUSIC))
    kw.setdefault("music_lufs", MUSIC_LUFS)


def _camera(video: Path, rec: Recording | None, face, hook, last) -> None:
    """The camera box, written over the render in place - none when no cue
    asks for it (a chapter Short)."""
    if not face and not hook and not last:
        return
    if rec is None or rec.face is None or rec.edl is None:
        if rec is not None:
            print("no face video - built without the camera box")
        return
    tmp = video.with_name(video.stem + ".cam" + video.suffix)
    facecam.apply(video, tmp, rec.edl, srt=video.with_suffix(".srt"),
                  on=list(face), hook=hook, last=last,
                  sentences=rec.sentence_times)
    os.replace(tmp, video)


def screen(name: str, file: str, take=None, *, window=None, vertical=False,
           at: float = 0.0, fallback=None, **opts):
    """A screen shot, zoomed to the work and framed in the brand window.

    **`take`** - the normal case (2026-11-21, the editor's note: Oktay records
    the voice only). A `screenplay.Browser` or `screenplay.Terminal` script:
    `build_long` / `build_short` play it in a headless browser, record it
    as `screens/<file>.mp4` with its event log, and render the cut. It is
    played again only when the take changes. A Short plays a terminal in its
    own narrower screen (the lines wrap instead of running off the side).
    The window defaults to a browser showing the take's real address, or a
    terminal.

    Without `take`, `screens/<file>.*` is a recording someone made by hand
    (`tools/screenrec.py record`); before it exists the shot is `fallback`
    or a placeholder naming the file, so a draft's timing is still real.

    `at` skips into the render (idle is already sped up: read times off the
    render's report). `opts` go to `screenrec.Spec`: `crop=`, `blur=`,
    `zoom=`, `idle=`, `trim=`. `rec=True` puts the REC dot over it
    (`core/rec.py`)."""
    from ..core import screenplay, screenrec
    from ..crypto.shots import Shot
    rec = bool(opts.pop("rec", False))
    shots = folder(name) / "screens"
    if take is not None:
        sh = screenplay.shot(take, file, color=OKTAI.primary, vertical=vertical,
                             window=window, at=at, where=shots, **opts)
        sh.rec = rec
        return sh
    window = window or ("browser", "")
    if isinstance(window, str):
        window = (window, "")
    if not vertical and len(window) == 2:
        window = (*window, "wide")
    src = _find_in(shots, file)
    if src is None:
        if fallback is not None:
            return fallback
        return Shot(image=_placeholder(name, file, vertical), window=window,
                    zoom=1.0)
    clip = screenrec.path(src, vertical=vertical, color=OKTAI.primary,
                          wide=len(window) > 2, **opts)
    return Shot(clip=clip, raw=True, window=window, clip_at=at)


def from_long(sections, keys: list, extra: dict | None = None):
    """Sentences, shots and gaps for a Short cut from a long form - the
    chapter Shorts (2026-11-23, the editor: "create more Shorts for each step
    with the same or similar introduction, using the footage from the long
    version - part of the skill: I read one script, we make the long, then
    use some of the content for Shorts").

    `keys` are the opening words of each line wanted, in order, matched
    against the long form's lines (chapter leads included); a line keeps the
    long form's shot (a fresh copy) and its pause, and a `None` shot still
    holds the picture before it. `extra` maps a key to `(sentence, shot,
    gap)` for a line or picture of the Short's own - a screen recorded
    vertical, an opener read only for the Short.

    Every line is one he already read, so a Short needs no new recording:
    `build_short(..., window=None)` finds each in the take.
    """
    import copy
    from ..core.recorded import norm
    from ..longform.plan import flatten
    sents, shots, gaps = flatten(sections)

    def spoken(s):
        return " ".join(norm(" ".join(c if isinstance(c, str) else c[1] for c in s)))

    texts = [spoken(s) for s in sents]
    out_s, out_sh, out_g = [], [], []
    for key in keys:
        if extra and key in extra:
            sent, sh, g = extra[key]
            out_s.append(sent)
            out_sh.append(sh)
            out_g.append(g)
            continue
        want = " ".join(norm(key))
        i = next((k for k, t in enumerate(texts) if t.startswith(want)), None)
        if i is None:
            raise ValueError(f"from_long: no line of the long form starts {key!r}")
        out_s.append(sents[i])
        out_sh.append(copy.deepcopy(shots[i]) if shots[i] is not None else None)
        out_g.append(gaps[i])
    return out_s, out_sh, out_g


def still(name: str, clip: Path, at: float = 1.0) -> Path:
    """A frame of `clip` as a picture, for a tile that shows footage (a
    roadmap's row of chapters). Made once, in the project's folder."""
    import subprocess
    clip = Path(clip)
    out = folder(name) / "stills" / f"{clip.parent.name}-{clip.stem}-{at:g}.jpg"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(at), "-i", str(clip),
                        "-frames:v", "1", "-q:v", "2", str(out)], check=True)
    return out


def own(name: str, video_id: str) -> Path:
    """One of our own published videos, as shipped: `own/<id>.mp4` in the
    project's folder (the `phones` beat draws an empty phone until it is
    there). `fetch_own` puts it there with yt-dlp; it is our own upload, and
    fetched only when the editor has said yes to it."""
    return folder(name) / "own" / f"{video_id}.mp4"


def fetch_own(name: str, video_ids: list[str]) -> list[Path]:
    import subprocess
    made = []
    for vid in video_ids:
        out = own(name, vid)
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["yt-dlp", "-q", "-f", "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
                            "--merge-output-format", "mp4", "-o", str(out),
                            f"https://www.youtube.com/shorts/{vid}"], check=True)
        made.append(out)
    return made


def _find_in(d: Path, stem: str) -> Path | None:
    if not d.is_dir():
        return None
    hits = [p for p in d.iterdir() if p.stem == stem
            and p.suffix.lower() in (".mov", ".mp4", ".m4v")]
    return sorted(hits)[0] if hits else None


def _placeholder(name: str, file: str, vertical: bool) -> Path:
    from PIL import Image, ImageDraw, ImageFont
    out = folder(name) / "screens" / ".render" / f"placeholder-{file}.png"
    if out.exists():
        return out
    out.parent.mkdir(parents=True, exist_ok=True)
    size = (1080, 1920) if vertical else (1920, 1080)
    im = Image.new("RGB", size, (20, 20, 24))
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype("/System/Library/Fonts/SFNSMono.ttf", 44)
    text = f"screen recording: {file}"
    w = d.textlength(text, font=f)
    d.text(((size[0] - w) / 2, size[1] / 2 - 22), text, font=f,
           fill=OKTAI.primary)
    im.save(out)
    return out


def _out(name: str, part: str, draft: bool) -> tuple[Path, Path]:
    tag = f"{name}-{part}" + ("-draft" if draft else "")
    return DESKTOP / f"{tag}.mp4", DESKTOP / f".{tag}-work"


def build_long(sections, name: str, *, face=(), draft: bool = False,
               hook: float | None = 3.0, last: float | None = 4.0,
               window=None, pins=None, drops=None, **kw) -> dict:
    """`render_long` with OktAI's brand, voice and camera box.

    `face`: phrases (as their caption starts) where the box comes in, each
    with how long to stay - `("this one cost me a week", 4.0)`. `window`:
    the seconds of a shared `recording.*` that hold this script.
    """
    from ..core.screenrec import make_pending
    from ..longform import render_long
    make_pending()
    voice, rec = _voice(name, "long", draft, window, pins, drops)
    is_draft = rec is None
    out, work = _out(name, "long", is_draft)
    kw.setdefault("subtitles", SUBTITLES)
    _bed(kw)
    kw.setdefault("music_swell", True)
    made = render_long(sections, out, work, brand=OKTAI, voice=voice, **kw)
    _camera(Path(made["video"]), rec, face, hook, last)
    if rec is not None and rec.report:
        made["report"] = rec.report
    return made


def build_short(sentences, shots, name: str, *, face=(), draft: bool = False,
                hook: float | None = 3.0, last: float | None = 3.0,
                window=None, pins=None, drops=None, tag: str = "",
                free: bool = False, **kw) -> tuple[Path, float]:
    """The Short through the same engine as crypto's, with OktAI's brand.

    `tag` names a second Short from the same recording (`<name>-short-<tag>`):
    a chapter Short cut from the long form (`from_long`), which passes
    `free=True` - its lines are read all over the take (`recording`)."""
    from ..core.screenrec import make_pending
    from ..crypto.build import render_crypto_short
    make_pending()
    voice, rec = _voice(name, "short", draft, window, pins, drops, free)
    is_draft = rec is None
    out, work = _out(name, "short" + (f"-{tag}" if tag else ""), is_draft)
    _bed(kw)
    # The examples play out in their own pause, as in the long form: under
    # the voice (the morning of 2026-11-24) they were talked over - "the
    # shorts still overlap the music example or AI voice example with my
    # voice over, we don't wait for it to finish" (that evening). The script
    # gives each example's line a gap the clip's length (`_after`).
    kw.setdefault("samples_under", False)
    out, total = render_crypto_short(sentences, shots, out, work, voice=voice,
                                     brand=OKTAI, **kw)
    if rec is not None and rec.captions:
        # The Short's engine writes no SRT; the camera box cues on one, and
        # it is worth uploading anyway. Always rewritten: a rebuild kept the
        # first build's timings while the cuts had moved (2026-11-22).
        from ..longform.meta import write_srt
        write_srt(rec.captions, out.with_suffix(".srt"))
    _camera(out, rec, face, hook, last)
    if rec is not None and rec.report:
        print(f"report: {rec.report}")
    return out, total

