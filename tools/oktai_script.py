"""The script Oktay reads aloud, from the pair's project files.

    PYTHONPATH=. .venv/bin/python tools/oktai_script.py NAME

Reads `projects/oktai-long/NAME.py` (its `SECTIONS`, or `sections()`) and
`projects/oktai-short/NAME.py` (its `SENTENCES`), and writes into the
recording folder `~/Movies/OktAI/NAME/`:

* `script.html` - a dark page to read from: numbered sentences, chapter
  breaks, a camera mark on every line where the box comes in, the reading
  time, and a teleprompter mode (P: start, space: pause, arrows: speed).
* `script.txt` - the same as plain text, for a phone or a print.

A project's `SCREENS` - `[("file", "what to record"), ...]` - is listed at
the end: the screen recordings Oktay captures himself with
`tools/screenrec.py record NAME FILE`, which saves `screens/<file>.mov` and
the click log the auto-zoom reads (`core/screenrec.py`).

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


def _face_marks(sentences: list[str], face) -> set[int]:
    """Lines where the camera box comes in: the first, the last, and `face`."""
    marks = {0, len(sentences) - 1} if sentences else set()
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
    marks = _face_marks(lines, getattr(mod, "FACE", ()))
    title = getattr(mod, "TITLE", None) or getattr(getattr(mod, "META", None),
                                                    "title", path.stem)
    return {"kind": kind, "title": title, "lines": lines,
            "chapters": chapters, "marks": marks,
            "screens": list(getattr(mod, "SCREENS", ())),
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
    screens = [x for p in parts for x in p["screens"]]
    if screens:
        out += ["=== SCREEN RECORDINGS TO CAPTURE ===",
                "Record each with (Ctrl+C stops):",
                f"  PYTHONPATH=. .venv/bin/python tools/screenrec.py record {name} <file>",
                "Close anything private first. Work at a calm pace; pauses are sped up.", ""]
        out += [f"- {f}: {what}" for f, what in screens]
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
code {{ color:var(--gold); font-size:14px; }}
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
#bar {{ position:fixed; right:16px; bottom:16px; background:var(--panel);
        color:var(--dim); padding:8px 12px; border-radius:8px; font-size:14px; }}
@media (max-width:600px) {{ body.prompter {{ font-size:28px; }} }}
</style></head><body>
<header>
<h1>okt<b>AI</b> &middot; {name}</h1>
<div class="meta">{summary}</div>
<p class="how">Read each line as written, one line per breath.
On a mistake, just say the whole line again; the last good take is kept.
Lines marked <b style="color:var(--gold)">CAM</b> are on camera: look into the lens.
<br>Teleprompter: <kbd>P</kbd> start/stop, <kbd>space</kbd> pause,
<kbd>&uarr;</kbd><kbd>&darr;</kbd> speed.</p>
</header>
<main>{body}</main>
<div id="bar" hidden></div>
<script>
let on=false, run=false, speed=40, last=0;
const bar=document.getElementById('bar');
function show(){{ bar.hidden=!on; bar.textContent=(run?'scrolling':'paused')+' - speed '+speed; }}
function tick(t){{ if(on&&run&&last) window.scrollBy(0,(t-last)/1000*speed); last=t;
  requestAnimationFrame(tick); }}
requestAnimationFrame(tick);
addEventListener('keydown',e=>{{
  if(e.key==='p'||e.key==='P'){{ on=!on; run=on; document.body.classList.toggle('prompter',on); }}
  else if(e.key===' '&&on){{ run=!run; e.preventDefault(); }}
  else if(e.key==='ArrowUp'&&on){{ speed=Math.min(200,speed+5); e.preventDefault(); }}
  else if(e.key==='ArrowDown'&&on){{ speed=Math.max(5,speed-5); e.preventDefault(); }}
  show(); }});
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
    screens = [x for p in parts for x in p["screens"]]
    if screens:
        body.append("<h2>Screen recordings to capture</h2><div class='meta'>"
                    "In the repo, one per file, Ctrl+C to stop:<br><code>"
                    f"PYTHONPATH=. .venv/bin/python tools/screenrec.py record "
                    f"{html.escape(name)} &lt;file&gt;</code><br>It logs clicks "
                    "and typing (never which keys) so the video can zoom to "
                    "them. Close anything private first: mail, keys, balances. "
                    "Work at a calm pace; pauses are sped up.</div>")
        for f, what in screens:
            body.append(f"<div class='line'><span class='n'>&#9679;</span>"
                        f"<span class='t'><b>{html.escape(f)}</b> - "
                        f"{html.escape(what)}</span></div>")
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
    (d / "script.html").write_text(page(name, parts))
    (d / "script.txt").write_text(text(name, parts))
    for p in parts:
        print(f"{p['kind']}: {len(p['lines'])} lines, ~{_minutes(p['words'])}")
    print(d / "script.html")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
