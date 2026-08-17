"""Check a long-form cut's clip slots before paying for a render.

`clip.py` raises on the **first** shot whose footage cannot fill its slot, and
it raises from inside `render_long` — after the narration has been synthesised.
So a cut with four tight slots costs four full runs to find four problems, and
each run is minutes of speech synthesis for an error that was knowable the
moment the timeline existed.

This runs the timeline once and reports **every** slot, plus the runtime and the
chapter list, which are the other two things worth knowing before committing to
a render:

    PYTHONPATH=. .venv/bin/python -m video_automation.longform.preflight \\
        projects/tinnitus-long/tinnitus-and-sleep.py

**The error message this exists to make readable.** `clip.py` reports the
shortfall as `want / src_len` — the slot against the clip's *whole* length,
ignoring `clip_at`. A shot 9 seconds into an 11 second clip therefore reports
needing "0.93x slow motion" when what it actually has is 2.2 seconds for a 10.4
second slot. The number looks survivable and is not. The `margin` column here
is the honest one: `src_len - clip_at - hold`.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import cv2

from ..core.voiceover import build_narration_aligned, profile_args
from ..crypto.build import sentence_spans
from .plan import flatten, lay_out


def load(path: Path):
    """Import a project module by file path.

    Project files live under `projects/` with hyphens in their names, which are
    not importable as module names — hence the loader rather than `__import__`.
    """
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def report(sections: list, voice: str, workdir: Path) -> int:
    """Print the timeline and every clip slot. Returns the failure count."""
    sentences, shots, gaps = flatten(sections)
    _, captions, total = build_narration_aligned(
        [list(s) for s in sentences], workdir, gap=gaps,
        **profile_args(voice))
    spans = sentence_spans(sentences, captions)
    shots, _, chapters = lay_out(sections, shots, spans, total)

    mins, secs = divmod(total, 60)
    print(f"\nruntime {int(mins)}:{secs:04.1f}   "
          f"{len(shots)} shots   {len(chapters)} chapters")
    if not 150.0 <= total <= 240.0:
        print("  ! outside the 2:30-4:00 target for this format")

    print("\nchapters")
    for start, title in chapters:
        m, s = divmod(start, 60)
        print(f"  {int(m)}:{int(s):02d}  {title}")

    print("\nclip slots")
    bad = 0
    for sh in shots:
        if not sh.clip:
            continue
        cap = cv2.VideoCapture(str(sh.clip))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        cap.release()
        # cv2's frame count is what `clip.py` actually trims against, so use
        # it here too — ffprobe's duration disagrees by a frame or two and
        # that is exactly the margin a tight slot is arguing over.
        left = frames / fps - sh.clip_at
        margin = left - sh.hold
        bad += margin < 0
        print(f"  {'ok  ' if margin >= 0 else 'FAIL'} {sh.clip.name:16s} "
              f"at {sh.clip_at:5.1f}s   slot {sh.hold:5.1f}s   "
              f"left {left:5.1f}s   margin {margin:+6.1f}s")

    print(f"\n{bad} failing slot(s)")
    return bad


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project", type=Path, help="a projects/*.py build script")
    ap.add_argument("--voice", default=None,
                    help="defaults to the project's own VOICE")
    ap.add_argument("--workdir", type=Path, default=Path("/tmp/preflight"))
    args = ap.parse_args()

    mod = load(args.project)
    voice = args.voice or getattr(mod, "VOICE", "mia")
    args.workdir.mkdir(parents=True, exist_ok=True)
    raise SystemExit(1 if report(mod.SECTIONS, voice, args.workdir) else 0)


if __name__ == "__main__":
    main()
