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

Outputs go to the Desktop like every other project: `<name>-long.mp4`,
`<name>-short.mp4`, their SRTs and sidecars.

Screen recordings are `screens/<file>.*` in the same folder, made with
`tools/screenrec.py record <name> <file>`; `screen()` turns one into a shot
(`core/screenrec.py`: auto-zoom, click ripples, blur, the brand window).

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
DESKTOP = Path(os.environ.get("OKTAI_OUT", Path.home() / "Desktop"))


def folder(name: str) -> Path:
    return RECORDINGS / name


def _find(name: str, stem: str) -> Path | None:
    d = folder(name)
    if not d.is_dir():
        return None
    hits = [p for p in d.iterdir()
            if p.stem.lower() == stem and p.suffix.lower() in MEDIA]
    return sorted(hits)[0] if hits else None


def recording(name: str, part: str) -> Recording | None:
    """The `long` or `short` recording of project `name`, or None."""
    audio = _find(name, part)
    if audio is None:
        return None
    return Recording(audio, video=_find(name, f"{part}-cam"))


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


def _voice(name: str, part: str, draft: bool):
    rec = None if draft else recording(name, part)
    if rec is None:
        why = "asked for" if draft else f"no {part}.* in {folder(name)}"
        print(f"DRAFT ({why}): Kokoro '{DRAFT_VOICE}' reads the {part} script")
        return DRAFT_VOICE, None
    print(f"recorded {part}: {rec.audio.name}"
          + (f" + camera {rec.video.name}" if rec.video else ""))
    return rec, rec


def _camera(video: Path, rec: Recording | None, face, hook, last) -> None:
    """The camera box, written over the render in place."""
    if rec is None or rec.face is None or rec.edl is None:
        if rec is not None:
            print("no face video - built without the camera box")
        return
    tmp = video.with_name(video.stem + ".cam" + video.suffix)
    facecam.apply(video, tmp, rec.edl, srt=video.with_suffix(".srt"),
                  on=list(face), hook=hook, last=last)
    os.replace(tmp, video)


def screen(name: str, file: str, *, window=("browser", ""), vertical=False,
           at: float = 0.0, fallback=None, **opts):
    """A shot of the screen recording `screens/<file>.*` - zoomed to the
    work, framed in `window` (a browser with the page's real address, or
    `("terminal", "")`). Landscape windows are the wide size. `at` skips into
    the render (its idle stretches are already sped up, so read the time off
    the render, not the raw recording). `opts` go to `screenrec.Spec`:
    `crop=`, `blur=`, `zoom=`, `idle=`, `trim=`.

    Before the recording exists (a draft) it is `fallback`, or a dark
    placeholder in the same window naming the file - so the draft's timing
    is the real one."""
    from ..core import screenrec
    from ..crypto.shots import Shot
    if isinstance(window, str):
        window = (window, "")
    if not vertical and len(window) == 2:
        window = (*window, "wide")
    src = _find_in(folder(name) / "screens", file)
    if src is None:
        if fallback is not None:
            return fallback
        return Shot(image=_placeholder(name, file, vertical), window=window,
                    zoom=1.0)
    clip = screenrec.path(src, vertical=vertical, color=OKTAI.primary,
                          wide=len(window) > 2, **opts)
    return Shot(clip=clip, raw=True, window=window, clip_at=at)


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
               hook: float | None = 3.0, last: float | None = 4.0, **kw) -> dict:
    """`render_long` with OktAI's brand, voice and camera box.

    `face`: phrases (as their caption starts) where the box comes in, each
    with how long to stay - `("this one cost me a week", 4.0)`.
    """
    from ..core.screenrec import make_pending
    from ..longform import render_long
    make_pending()
    voice, rec = _voice(name, "long", draft)
    is_draft = rec is None
    out, work = _out(name, "long", is_draft)
    made = render_long(sections, out, work, brand=OKTAI, voice=voice, **kw)
    _camera(Path(made["video"]), rec, face, hook, last)
    if rec is not None and rec.report:
        made["report"] = rec.report
    return made


def build_short(sentences, shots, name: str, *, face=(), draft: bool = False,
                hook: float | None = 3.0, last: float | None = 3.0,
                **kw) -> tuple[Path, float]:
    """The Short through the same engine as crypto's, with OktAI's brand."""
    from ..core.screenrec import make_pending
    from ..crypto.build import render_crypto_short
    make_pending()
    voice, rec = _voice(name, "short", draft)
    is_draft = rec is None
    out, work = _out(name, "short", is_draft)
    out, total = render_crypto_short(sentences, shots, out, work, voice=voice,
                                     brand=OKTAI, **kw)
    if rec is not None and rec.captions and not out.with_suffix(".srt").exists():
        # The Short's engine writes no SRT; the camera box cues on one, and
        # it is worth uploading anyway.
        from ..longform.meta import write_srt
        write_srt(rec.captions, out.with_suffix(".srt"))
    _camera(out, rec, face, hook, last)
    if rec is not None and rec.report:
        print(f"report: {rec.report}")
    return out, total

