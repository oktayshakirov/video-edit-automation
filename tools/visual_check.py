"""The edit plan, before anything renders: what is on screen, line by line,
and where the picture goes plain.

    PYTHONPATH=. .venv/bin/python tools/visual_check.py projects/oktai-long/NAME.py [...]

**Why (2026-11-21, the editor's note on the OktAI opener draft):** "in the
2 minutes mark too much context without visual examples and it's getting
boring ... in the 3 minutes mark again, we give a lot of information with
very plain visuals, just text. We need to show more examples - if it's hard
for the session to keep up, create a workflow which plans the editing
better." The draft was 4:44 of mostly `stat`, `quote`, `compare`, `split`
and `steps`: each one fine, a run of them a slideshow. Nothing flagged it
until someone watched.

Every shot is put in one of four kinds:

* **real** - something that exists: a scripted screen, a clip or still of
  ours, a page, a logo lineup, a played sound (`samples=`), a `wall` of our
  own graphics, a framed window.
* **drawn** - a beat that draws a mechanism or data: `diagram`, `chart`,
  `bars`, `airgap`, `relay`, ... - a picture, not a sentence.
* **stock** - a clip or photo from `assets/stock/` with no mark on it.
* **text** - a beat whose picture is words: `stat`, `quote`, `compare`,
  `split`, `steps`, `grid`, `checklist`, a chapter card.

Then the time is estimated per sentence (150 words a minute, the read-aloud
pace, plus the gaps) and the plan is printed - time, kind, picture, line -
with a flag on anything the note was about:

* a run of **text** longer than `TEXT_RUN` seconds;
* a chapter with **no real example** in it;
* **text** over `TEXT_SHARE` of the runtime;
* the same graphic **three times in a row**;
* one picture held longer than `HOLD` seconds.

It is a plan, not a verdict: a flag is answered by changing the picture or by
a one-line reason in the project's docstring. The skill runs it in "Write
the picture first", before the draft (`.claude/skills/video-oktai/SKILL.md`).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "tools"))

WPM = 150
TEXT_RUN = 8.0
TEXT_SHARE = 0.35
HOLD = 14.0

TEXT = {"stat", "quote", "compare", "split", "steps", "grid", "checklist", "chapter"}
REAL_GRAPHICS = {"logos", "voice", "wall", "phones", "post", "reel", "spotlight",
                 "callout", "anatomy", "behind"}
# Pictures that keep changing on their own - a wall's tiles keep arriving, a
# screen take types and scrolls - get a longer hold before it is a flag.
MOVING_HOLD = 20.0


def kind(shot) -> str:
    if shot is None:
        return "hold"
    if getattr(shot, "verdict", None) or getattr(shot, "window", None):
        return "real"
    if getattr(shot, "samples", None):
        return "real"
    if shot.clip is not None or shot.image is not None:
        src = str(shot.clip or shot.image)
        if "assets/stock/" in src and "/press/" not in src and "/captures/" not in src:
            return "stock"
        return "real"
    g = shot.graphic
    if g in REAL_GRAPHICS:
        return "real"
    if g in TEXT:
        return "text"
    return "drawn" if g else "real"


def label(shot) -> str:
    if shot is None:
        return ""
    if getattr(shot, "window", None):
        w = shot.window
        return f"screen: {w[0]} {w[1]}".strip() if isinstance(w, tuple) else f"screen: {w}"
    if shot.clip is not None:
        return f"clip: {Path(str(shot.clip)).parent.name or Path(str(shot.clip)).name}"
    if shot.image is not None:
        return f"image: {Path(str(shot.image)).name}"
    p = shot.payload
    title = ""
    if isinstance(p, tuple) and p:
        title = next((x for x in reversed(p) if isinstance(x, str) and x.isupper()), "")
        if not title and isinstance(p[0], str):
            title = p[0]
    extra = " + sound" if getattr(shot, "samples", None) else ""
    return f"{shot.graphic}: {title[:38]}{extra}"


def _listening(shot) -> float:
    """Seconds a shot spends playing its sound examples: the viewer is
    listening then, and the picture is moving with it."""
    names = [n for n in (getattr(shot, "samples", None) or ()) if n]
    if not names:
        return 0.0
    from video_automation.core import samples
    return sum(samples.DUR.get(n, 0.0) for n in names)


def _limit(shot) -> float:
    moving = getattr(shot, "window", None) or shot.graphic in ("wall", "phones", "reel")
    return MOVING_HOLD if moving else HOLD


def words(sentence) -> int:
    from opening_check import text
    return len(re.findall(r"[A-Za-z0-9']+", text(sentence)))


def plan(path: Path):
    from opening_check import load
    mod = load(path)
    if hasattr(mod, "SECTIONS"):
        from video_automation.longform.plan import flatten
        out = []
        for sec in mod.SECTIONS:
            s, sh, g = sec.parts()
            out.append((sec.title, s, sh, g))
        return out
    gaps = getattr(mod, "GAPS", None)
    n = len(mod.SENTENCES)
    gaps = list(gaps) if isinstance(gaps, (list, tuple)) else [0.45] * n
    return [("Short", list(mod.SENTENCES), list(mod.SHOTS), gaps)]


def check(path: Path, show: bool = True) -> list[str]:
    secs = plan(path)
    rows, flags = [], []
    t = 0.0
    cur, cur_kind, held_from = None, None, 0.0
    run_start, run_len = None, 0.0
    text_total = total = 0.0
    last3: list[str] = []
    for title, sents, shots, gaps in secs:
        has_real = False
        for s, sh, g in zip(sents, shots, gaps):
            dur = words(s) / WPM * 60 + g
            if sh is not None:
                if cur is not None and t - held_from - _listening(cur) > _limit(cur):
                    flags.append(f"{_mm(held_from)} one picture for {t - held_from:.0f}s: "
                                 f"{label(cur)}")
                cur, cur_kind, held_from = sh, kind(sh), t
                g_name = sh.graphic or kind(sh)
                last3 = (last3 + [g_name])[-3:]
                if len(last3) == 3 and len(set(last3)) == 1 and sh.graphic:
                    flags.append(f"{_mm(t)} {sh.graphic} three times in a row")
            k = cur_kind
            has_real |= k == "real"
            if k == "text":
                text_total += dur
                if run_start is None:
                    run_start, run_len = t, 0.0
                run_len += dur
            else:
                if run_start is not None and run_len > TEXT_RUN:
                    flags.append(f"{_mm(run_start)} {run_len:.0f}s of text-only pictures "
                                 f"(until {_mm(run_start + run_len)})")
                run_start = None
            rows.append((t, k if sh is not None else "  \"", label(sh) if sh is not None else "",
                         _text(s)))
            t += dur
            total += dur
        if not has_real and len(sents) > 2:
            flags.append(f"chapter '{title}': no real example (a screen, a clip, a "
                         f"logo, a sound)")
    if run_start is not None and run_len > TEXT_RUN:
        flags.append(f"{_mm(run_start)} {run_len:.0f}s of text-only pictures")
    if total and text_total / total > TEXT_SHARE:
        flags.append(f"text-only pictures fill {text_total / total:.0%} of the runtime "
                     f"(goal: under {TEXT_SHARE:.0%})")
    if show:
        print(f"\n{path}  (~{_mm(total)} at {WPM} wpm)")
        for t0, k, lab, line in rows:
            mark = {"text": "T", "real": "R", "drawn": "D", "stock": "S"}.get(k, " ")
            print(f"  {_mm(t0)} {mark} {lab[:44]:44} {line[:70]}")
        shares = {}
        for t0, k, *_ in rows:
            pass
        print(f"  text {text_total / max(total, 1):.0%} of the time")
        for f in flags:
            print(f"  ! {f}")
        if not flags:
            print("  ok")
    return flags


def _text(sentence) -> str:
    from opening_check import text
    return text(sentence)


def _mm(t: float) -> str:
    return f"{int(t // 60)}:{int(t % 60):02d}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", type=Path)
    a = ap.parse_args()
    n = sum(bool(check(p)) for p in a.paths)
    print(f"\n{len(a.paths)} script(s), {n} with flags")


if __name__ == "__main__":
    main()
