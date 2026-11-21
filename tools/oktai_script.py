"""The script Oktay reads aloud, from the pair's project files.

    PYTHONPATH=. .venv/bin/python tools/oktai_script.py NAME

Reads `projects/oktai-long/NAME.py` (its `SECTIONS`, or `sections()`) and
`projects/oktai-short/NAME.py` (its `SENTENCES`), and writes **to the
Desktop** (the editor, 2026-11-21: "place the script always on my desktop"):

* `NAME-script.html` - a dark page to read from: numbered sentences, chapter
  breaks, a camera mark on every line where the box comes in, the reading
  time, and a teleprompter (Start button or P, space or a tap to pause,
  - / + or the arrows for speed).
* `NAME-script.txt` - the same as plain text, for a phone or a print.

A copy of both stays in the recording folder `~/Movies/OktAI/NAME/` as
`script.html` / `script.txt`, where a video's own screen of the page reads it.

Oktay records the voice (and the camera box) only. Screens are scripted
takes the build plays itself (`oktai.screen`, `core/screenplay.py`), so
there is nothing on this page to capture (the editor's note, 2026-11-21).

**It prints what the voice will say, not the captions.** A `(caption,
spoken)` pair is read as its spoken half, and a carded chapter's title is a
sentence of its own (`oktai.reading_order`). That is exactly the text the
build searches the recording for, so a read of this page always matches.
"""

from __future__ import annotations

import html
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from video_automation.core.recorded import norm  # noqa: E402
from video_automation.oktai import folder, reading_order  # noqa: E402
from video_automation.oktai.build import DESKTOP  # noqa: E402

WPM = 150                      # a relaxed explainer read, measured on Kokoro


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _spoken(sentence) -> str:
    parts = [c if isinstance(c, str) else c[1] for c in sentence]
    return " ".join(p.strip() for p in parts if p.strip())


def _caption_titles(sections) -> dict[int, str]:
    """Sentence index -> chapter title, for every carded section."""
    out, i = {}, 0
    for sec in sections:
        if sec.card:
            out[i] = sec.title
        i += len(sec.parts()[0])
    return out


def _face_marks(sentences: list[str], face, hook: bool = True) -> set[int]:
    """Lines where the camera box comes in: the first (unless the project
    sets `FACE_HOOK = False`), the last, and `face`."""
    marks = ({0} if hook else set()) | {len(sentences) - 1} if sentences else set()
    flat = [" ".join(norm(s)) for s in sentences]
    for item in face or []:
        phrase = item if isinstance(item, str) else item[0]
        want = " ".join(norm(phrase))
        for i, s in enumerate(flat):
            if want and want in s:
                marks.add(i)
                break
    return marks


def part(path: Path, kind: str):
    mod = _load(path)
    if kind == "long":
        sections = mod.SECTIONS if hasattr(mod, "SECTIONS") else mod.sections()
        order = reading_order(sections=sections)
        chapters = _caption_titles(sections)
    else:
        order = reading_order(sentences=mod.SENTENCES)
        chapters = {}
    lines = [_spoken(s) for s in order]
    marks = _face_marks(lines, getattr(mod, "FACE", ()),
                        getattr(mod, "FACE_HOOK", True))
    title = getattr(mod, "TITLE", None) or getattr(getattr(mod, "META", None),
                                                    "title", path.stem)
    return {"kind": kind, "title": title, "lines": lines,
            "chapters": chapters, "marks": marks,
            "words": sum(len(norm(x)) for x in lines)}


def _minutes(words: int) -> str:
    s = round(words / WPM * 60)
    return f"{s // 60}:{s % 60:02d}"


def text(name: str, parts: list[dict]) -> str:
    out = [f"OktAI - {name} - script to read", ""]
    out += ["Read each line as written. On a mistake, say the whole line again.",
            "[CAM] = the camera box is on for this line: look into the lens.", ""]
    for p in parts:
        out += [f"=== {p['kind'].upper()}: {p['title']} "
                f"({len(p['lines'])} lines, about {_minutes(p['words'])}) ===", ""]
        for i, line in enumerate(p["lines"]):
            if i in p["chapters"]:
                out += ["", f"--- chapter: {p['chapters'][i]} ---"]
            cam = "[CAM] " if i in p["marks"] else ""
            out.append(f"{i + 1:>3}. {cam}{line}")
        out.append("")
    return "\n".join(out) + "\n"


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>OktAI script</title>
<style>
:root {{ --bg:#050507; --panel:#141417; --ink:#f2f2f2; --dim:#9a9aa2;
         --gold:#ffdb70; --gold2:#ffc05c; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
       font:18px/1.6 Poppins, -apple-system, "Helvetica Neue", sans-serif; }}
header {{ padding:28px 20px 8px; max-width:900px; margin:auto; }}
h1 {{ font-size:26px; margin:0 0 4px; }}
h1 b {{ background:linear-gradient(90deg,var(--gold),var(--gold2));
        -webkit-background-clip:text; color:transparent; }}
.meta, .how {{ color:var(--dim); font-size:15px; }}
.how kbd {{ background:#222; border-radius:4px; padding:1px 6px; color:var(--ink); }}
main {{ max-width:900px; margin:auto; padding:0 20px 40vh; }}
h2 {{ margin:40px 0 6px; font-size:20px; color:var(--gold); }}
h3 {{ margin:28px 0 6px; font-size:14px; letter-spacing:.12em;
      text-transform:uppercase; color:var(--dim); }}
.line {{ display:flex; gap:14px; padding:10px 14px; margin:4px 0;
         border-radius:10px; background:var(--panel); }}
.line .n {{ color:var(--dim); min-width:2.2em; text-align:right;
           font-variant-numeric:tabular-nums; }}
.line.cam {{ box-shadow:inset 3px 0 0 var(--gold); }}
.line.cam .t::before {{ content:"CAM"; font-size:11px; font-weight:700;
           color:#0a0a0e; background:var(--gold); border-radius:4px;
           padding:2px 6px; margin-right:10px; vertical-align:2px; }}
body.prompter {{ font-size:40px; line-height:1.45; }}
body.prompter header {{ display:none; }}
body.prompter .line {{ background:none; padding:14px 0; }}
body.prompter .line .n {{ font-size:18px; padding-top:14px; }}
#bar {{ position:fixed; right:16px; bottom:16px; display:flex; gap:8px;
        align-items:center; background:var(--panel); color:var(--dim);
        padding:8px; border-radius:12px; font-size:14px; z-index:9; }}
#bar button {{ font:inherit; font-size:15px; color:var(--ink); background:#26262c;
              border:0; border-radius:8px; padding:8px 12px; cursor:pointer; }}
#bar button.go {{ background:var(--gold); color:#0a0a0e; font-weight:600; }}
#state {{ min-width:9em; text-align:center; }}
body.prompter main {{ padding-top:45vh; }}
body.prompter .line.now {{ color:var(--gold); }}
@media (max-width:600px) {{ body.prompter {{ font-size:28px; }} }}
</style></head><body>
<header>
<h1>okt<b>AI</b> &middot; {name}</h1>
<div class="meta">{summary}</div>
<p class="how">Read each line as written, one line per breath.
On a mistake, just say the whole line again; the last good take is kept.
Lines marked <b style="color:var(--gold)">CAM</b> are on camera: look into the lens.
<br>Teleprompter: press <b>Start</b> at the bottom right (or <kbd>P</kbd>).
<kbd>space</kbd> or a tap pauses, <kbd>&uarr;</kbd><kbd>&darr;</kbd> or
<b>&minus;</b> / <b>+</b> change the speed. Open this file in Safari or Chrome
(double-click it in Finder); a preview pane may not run it.</p>
</header>
<main>{body}</main>
<div id="bar">
<button id="go" class="go">Start</button>
<button id="slow" title="slower">&minus;</button>
<span id="state">speed 40</span>
<button id="fast" title="faster">+</button>
<button id="top" title="back to the start">&#8634;</button>
</div>
<script>
// The prompter keeps its own position as a float: a frame's step at a slow
// speed is under a pixel, and browsers round a fractional scrollBy to zero -
// the first version never moved (2026-11-21).
let on=false, run=false, speed=40, last=0, pos=0;
const $=id=>document.getElementById(id);
function show(){{
  $('go').textContent = !on ? 'Start' : (run ? 'Pause' : 'Resume');
  $('state').textContent = (on ? (run ? 'scrolling' : 'paused') + ' - ' : '') + 'speed ' + speed;
}}
function stop(){{ on=false; run=false; document.body.classList.remove('prompter'); show(); }}
function tick(t){{
  if(on&&run){{
    if(last) {{ pos += (t-last)/1000*speed; window.scrollTo(0, Math.round(pos)); }}
    last=t;
    if(window.innerHeight + window.scrollY >= document.body.scrollHeight - 2) {{ run=false; show(); }}
  }} else last=0;
  requestAnimationFrame(tick);
}}
requestAnimationFrame(tick);
$('go').onclick = e => {{ e.stopPropagation(); if(!on) {{ on=true; run=true;
  document.body.classList.add('prompter'); pos=window.scrollY; last=0; show(); }}
  else {{ run=!run; last=0; pos=window.scrollY; show(); }} }};
$('slow').onclick = e => {{ e.stopPropagation(); speed=Math.max(5,speed-5); show(); }};
$('fast').onclick = e => {{ e.stopPropagation(); speed=Math.min(200,speed+5); show(); }};
$('top').onclick = e => {{ e.stopPropagation(); window.scrollTo(0,0); pos=0; show(); }};
// A tap on the text pauses or resumes, for a phone or a tablet on a stand.
document.querySelector('main').addEventListener('click', () => {{
  if(on) {{ run=!run; last=0; pos=window.scrollY; show(); }} }});
// Scrolling by hand while paused moves where it resumes from.
addEventListener('wheel', () => {{ if(!run) pos=window.scrollY; }}, {{passive:true}});
addEventListener('keydown',e=>{{
  if(e.key==='p'||e.key==='P'){{ if(on) stop(); else {{ on=true; run=true;
    document.body.classList.add('prompter'); pos=window.scrollY; last=0; show(); }} }}
  else if(e.key===' '&&on){{ run=!run; last=0; pos=window.scrollY; e.preventDefault(); show(); }}
  else if(e.key==='ArrowUp'){{ speed=Math.min(200,speed+5); e.preventDefault(); show(); }}
  else if(e.key==='ArrowDown'){{ speed=Math.max(5,speed-5); e.preventDefault(); show(); }}
  else if(e.key==='Escape'&&on) stop();
}});
show();
</script></body></html>
"""


def page(name: str, parts: list[dict]) -> str:
    body = []
    for p in parts:
        body.append(f"<h2>{p['kind'].title()}: {html.escape(str(p['title']))}</h2>"
                    f"<div class='meta'>{len(p['lines'])} lines, about "
                    f"{_minutes(p['words'])} - save the recording as "
                    f"<b>{p['kind']}.mov</b> (or .m4a / .wav)</div>")
        for i, line in enumerate(p["lines"]):
            if i in p["chapters"]:
                body.append(f"<h3>{html.escape(p['chapters'][i])}</h3>")
            cls = "line cam" if i in p["marks"] else "line"
            body.append(f"<div class='{cls}'><span class='n'>{i + 1}</span>"
                        f"<span class='t'>{html.escape(line)}</span></div>")
    total = sum(p["words"] for p in parts)
    summary = (f"{' + '.join(p['kind'] for p in parts)} - "
               f"about {_minutes(total)} of reading")
    return PAGE.format(name=html.escape(name), summary=summary,
                       body="\n".join(body))


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    name = argv[0]
    parts = []
    for kind in ("long", "short"):
        path = REPO / f"projects/oktai-{kind}/{name}.py"
        if path.exists():
            parts.append(part(path, kind))
    if not parts:
        print(f"no projects/oktai-long/{name}.py or projects/oktai-short/{name}.py")
        return 1
    d = folder(name)
    d.mkdir(parents=True, exist_ok=True)
    html, txt = page(name, parts), text(name, parts)
    (d / "script.html").write_text(html)
    (d / "script.txt").write_text(txt)
    desk = DESKTOP / f"{name}-script.html"
    desk.write_text(html)
    desk.with_suffix(".txt").write_text(txt)
    for p in parts:
        print(f"{p['kind']}: {len(p['lines'])} lines, ~{_minutes(p['words'])}")
    print(desk)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
