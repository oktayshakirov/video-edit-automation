"""Where will this script lose its viewers? And did the last ones lose them there?

The goal since 2026-11-10 is videos people watch to the end
(`docs/video/retention.md`). Three things about a Short's first eight seconds
were found on the curves that day, and none of them can be seen by reading a
script from memory - they are timings:

- **Sentence 2 starting at 4.0s or later held on 8 of 9 Shorts; earlier, on 9
  of 23** (32 curves, "held" = half the opening audience still there at 11s).
  The steepest drop sits at 4.5-7s whatever the script says, so a Short whose
  partial answer is still being said then has not yet given the viewer a
  reason to go.
- **The frame went bare right at that drop.** Captions resume with the first
  sentence that starts after the opener has gone (`shorts.md`), so an opener
  leaving at ~4.5s left 2-4 seconds with no type on screen at all. On 4 of 7
  Shorts with a timed opener the steepest step was within 0.6s of its exit.
  `opener_holds=True` on the render call closes it.
- **Length.** Crypto Shorts are testing 30-40 seconds (E17), article long
  forms 3 minutes or less (E18).

This prints the timeline a script implies - at 3.25 words a second plus its
written gaps, the same estimate `video-views-audit` maps curves with - and
flags those shapes:

    PYTHONPATH=. .venv/bin/python tools/retention_check.py \\
        projects/crypto-short/<name>.py projects/crypto-long/<name>.py

A flag is a prompt, like the opening check's: answer it in the handover or
rewrite. It exits 1 when anything is flagged.

**The lab** re-tests those findings on every curve there is, so a flag that
stops predicting gets retired instead of obeyed:

    PYTHONPATH=. .venv/bin/python tools/retention_check.py --lab <dir>

`<dir>` holds one `youtube-audit retention <id> --json` file per Short. Each
is matched to its script by title, and the table splits half-gone, seconds
per counted view and the share holding by each feature. The performance
review runs it every time.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics as st
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import opening_check as oc          # noqa: E402
import script_check as sc           # noqa: E402

RATE = 3.25                 # spoken words a second, both voices
DEFAULT_GAP = 0.34          # `render_crypto_short`'s default between sentences
OPENER_HOLD, OPENER_EXIT = 0.9, 0.28
S2_LATE = 4.0               # sentence 2 starts here or later
BARE_MAX = 1.0              # seconds with no opener and no caption
HELD = 11.0                 # half the opening audience still there
SHORT_SECS = {"crypto": (30, 40)}       # E17
LONG_MAX = 180                          # E18


def _gaps(mod, n: int) -> list[float]:
    g = getattr(mod, "GAPS", None)
    if isinstance(g, (int, float)):
        return [float(g)] * n
    g = list(g or [])
    return (g + [DEFAULT_GAP] * n)[:n]


def timeline(sentences, gaps) -> list[tuple[float, float, str]]:
    """(start, end, text) per sentence, estimated."""
    t, out = 0.0, []
    for s, g in zip(sentences, gaps):
        tx = oc.text(s)
        d = len(tx.split()) / RATE
        out.append((t, t + d, tx))
        t += d + g
    return out


def _word_at(tl, word: str, earliest: float = 1.0) -> float | None:
    key = re.sub(r"[^a-z0-9]", "", word.split()[0].lower())
    for a, _b, tx in tl:
        for i, w in enumerate(tx.split()):
            t = a + i / RATE
            if t >= earliest and re.sub(r"[^a-z0-9]", "", w.lower()) == key:
                return t
    return None


def features(path: Path) -> dict | None:
    """What a Short's script implies about its first seconds. None if it has
    no two-sentence `SENTENCES` (a session Short, a quiz)."""
    mod = oc.load(path)
    sentences = getattr(mod, "SENTENCES", None)
    if not sentences or len(sentences) < 2:
        return None
    tl = timeline(sentences, _gaps(mod, len(sentences)))
    src = path.read_text(errors="replace")
    shown, word = oc.opener(path, mod)
    kind = shown.split("=")[0] if shown == "none" else (
        re.search(r"(Counter|Stamp|Split|Search|Flash)", shown) or [None])[0] or "hook"
    hold = re.search(r"\bhold\s*=\s*([0-9.]+)", shown)
    hold = float(hold.group(1)) if hold else OPENER_HOLD
    exit_ = None
    if kind != "none":
        land = _word_at(tl, word) if word else None
        if land is None:
            # No timed word: Search lands when the query has typed (about a
            # second after the question is read), the rest at their default.
            land = max(2.6, tl[0][1] + 1.0) if kind == "Search" else 2.6
        exit_ = land + hold + OPENER_EXIT
    holds = bool(re.search(r"^[^#\n]*\bopener_holds\s*=\s*True", src, re.M))
    resume = bare = None
    if exit_ is not None:
        resume = next((a for a, _b, _t in tl if a >= exit_), None)
        if resume is not None:
            bare = 0.0 if holds else max(0.0, resume - exit_)
    shots = sc.shots_of(mod)
    total = tl[-1][1] + 1.2
    return dict(
        path=str(path), channel=sc.classify(path)[0],
        w1=len(tl[0][2].split()), s1_end=tl[0][1], s2_start=tl[1][0],
        s2_end=tl[1][1], opener=kind, opener_exit=exit_, resume=resume,
        bare=bare, opener_holds=holds, secs=total,
        words=sum(len(t.split()) for _a, _b, t in tl),
        first=tl[0][2], last=tl[-1][2], timeline=tl,
        stock=(sum(1 for s in shots if sc.is_plain_stock(s)) / len(shots)
               if shots else None))


def long_seconds(path: Path) -> tuple[float, int] | None:
    """A long form's estimated runtime and its chapter count."""
    mod = oc.load(path)
    secs = getattr(mod, "SECTIONS", None)
    if not secs:
        return None
    words = gaps = 0.0
    for sec in secs:
        for s in getattr(sec, "sentences", []):
            words += len(oc.text(s).split())
            gaps += 0.6
    cards = sum(1 for s in secs if getattr(s, "card", True))
    return words / RATE + gaps + cards * 2.2 + 8.0, len(secs)


def check(path: Path) -> list[str]:
    channel, fmt = sc.classify(path)
    flags: list[str] = []
    print(f"\n{path}")
    if fmt == "long":
        est = long_seconds(path)
        if est is None:
            print("  no SECTIONS - nothing to time")
            return flags
        secs, n = est
        print(f"  runtime         ~{int(secs // 60)}:{int(secs % 60):02d} "
              f"in {n} sections (estimate)")
        if secs > LONG_MAX + 10:
            flags.append(f"over 3:00 - article long forms run 2:30-3:00 "
                         f"(E18). Cut a chapter whole")
        for f in flags:
            print(f"  ! {f}")
        return flags

    ft = features(path)
    if ft is None:
        print("  no SENTENCES with two entries - nothing to time")
        return flags
    print(f"  title question  {ft['w1']} words, read by {ft['s1_end']:.1f}s")
    print(f"  sentence 2      {ft['s2_start']:.1f}s to {ft['s2_end']:.1f}s")
    if ft["opener_exit"] is not None:
        tail = (" (held to the captions)" if ft["opener_holds"] else
                f", captions back at {ft['resume']:.1f}s"
                if ft["resume"] is not None else "")
        print(f"  opener          {ft['opener']}, gone by ~{ft['opener_exit']:.1f}s{tail}")
    print(f"  at 5.5s         {said_at(ft['timeline'], 5.5)}")
    print(f"  runtime         ~{ft['secs']:.0f}s, {ft['words']} words (estimate)")
    if ft["stock"] is not None:
        print(f"  plain stock     {ft['stock']:.0%} of shots")
    print(f"  the loop reads  \"{ft['last']}\" -> \"{ft['first']}\"")

    if round(ft["s2_start"], 1) < S2_LATE:
        flags.append(
            f"sentence 2 starts at {ft['s2_start']:.1f}s - at {S2_LATE:.0f}s or "
            f"later held on 8 of 9 Shorts, earlier on 9 of 23. Ask a fuller "
            f"title question (10-13 words), not a longer pause")
    if ft["opener"] != "none" and not ft["opener_holds"]:
        est = (f" (~{ft['bare']:.1f}s here by estimate; the build prints the "
               f"real figure)" if ft["bare"] is not None else "")
        flags.append(
            "no opener_holds=True on the render call - when the opener "
            "leaves mid-sentence the frame has no type until the next "
            f"sentence, right at the steepest drop{est}")
    lo_hi = SHORT_SECS.get(channel)
    if lo_hi and not (lo_hi[0] - 2 <= ft["secs"] <= lo_hi[1] + 3):
        flags.append(f"~{ft['secs']:.0f}s - {channel} Shorts run "
                     f"{lo_hi[0]}-{lo_hi[1]}s (E17). Cut the middle, never "
                     f"sentence 2 or the close")
    for f in flags:
        print(f"  ! {f}")
    return flags


def said_at(tl, t: float) -> str:
    for i, (a, b, tx) in enumerate(tl, 1):
        if a <= t < b:
            words = tx.split()
            k = min(len(words) - 1, int((t - a) * RATE))
            return (f"sentence {i}, word {k + 1} of {len(words)}: "
                    f"\"... {' '.join(words[max(0, k - 2):k + 1])}\"")
        if t < a:
            return f"the pause before sentence {i}"
    return "after the last sentence"


# --------------------------------------------------------------------------
# the lab

STOP = set("the a is in of to your you do does what how why and for tinnitus "
           "crypto it did with from can are be or".split())


def _tok(s: str) -> set[str]:
    return set(re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("#shorts", "")
                      ).split()) - STOP


def curve_stats(points: list[dict]) -> dict | None:
    if not points:
        return None
    o = points[0]["watchPct"]
    half = next((p["seconds"] for p in points if p["watchPct"] <= o / 2), None)
    return dict(open=o, half=half, never=half is None,
                last=100 * points[-1]["watchPct"] / o,
                dur=points[-1]["seconds"])


def lab(folder: Path) -> int:
    scripts = {}
    for d in ("crypto-short", "tinnitus-short"):
        for p in sorted((REPO / "projects" / d).glob("*.py")):
            try:
                ft = features(p)
            except Exception:
                continue
            if ft:
                scripts[p] = ft
    rows = []
    for f in sorted(folder.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except ValueError:
            continue
        cv = d.get("curve") or {}
        stats = curve_stats(cv.get("points") or [])
        title = cv.get("title") or ""
        if stats is None or "#shorts" not in title.lower():
            continue
        t = _tok(title)
        best, score = None, 0.0
        for p, ft in scripts.items():
            if ft["channel"] != d.get("channelKey", ft["channel"]):
                continue
            s = len(t & (_tok(ft["first"]) | _tok(p.stem.replace("-", " ")))) / max(1, len(t))
            if s > score:
                best, score = p, s
        if best is None or score < 0.5:
            continue
        dl = d.get("delivery") or {}
        rows.append({**scripts[best], **stats, "title": title,
                     "spv": dl.get("secondsPerView"),
                     "covers": dl.get("curveCovers")})
    if not rows:
        print(f"no Short in {folder} matched a script")
        return 1

    def held(r):
        return r["never"] or r["half"] >= HELD

    def h(r):
        return r["dur"] if r["never"] else r["half"]

    rows.sort(key=lambda r: r["s2_start"])
    print(f"{'s2 at':>6} {'bare':>5} {'secs':>5} {'open':>5} {'half':>6} "
          f"{'s/view':>6}  title")
    for r in rows:
        print(f"{r['s2_start']:6.1f} "
              f"{r['bare'] if r['bare'] is not None else float('nan'):5.1f} "
              f"{r['secs']:5.0f} {r['open']:5.0f} "
              f"{'never' if r['never'] else format(r['half'], '6.1f'):>6} "
              f"{format(r['spv'], '6.1f') if r['spv'] else '     -'}  "
              f"{'*' if held(r) else ' '} {r['title'][:52]}")
    print(f"\n{len(rows)} Shorts matched; * = held (half still there at "
          f"{HELD:.0f}s)\n")

    def split(label, test, rs=rows):
        a = [r for r in rs if test(r)]
        b = [r for r in rs if not test(r)]

        def line(g):
            if not g:
                return "none"
            spv = [r["spv"] for r in g if r["spv"]]
            return (f"{sum(map(held, g))} of {len(g)} held, median half-gone "
                    f"{st.median(map(h, g)):.1f}s"
                    + (f", {st.median(spv):.1f}s a view" if spv else ""))
        print(f"  {label:<34} yes: {line(a)}\n  {'':<34}  no: {line(b)}")

    split(f"sentence 2 starts at {S2_LATE:.0f}s+", lambda r: round(r["s2_start"], 1) >= S2_LATE)
    timed = [r for r in rows if r["bare"] is not None]
    if timed:
        split(f"bare stretch over {BARE_MAX:.0f}s", lambda r: r["bare"] > BARE_MAX, timed)
    split("40 seconds or under", lambda r: r["secs"] <= 40)
    split("opens at 125%+ (replay)", lambda r: r["open"] >= 125)
    split("plain stock over half", lambda r: (r["stock"] or 0) > 0.5)
    print("\nEstimates from the scripts (3.25 words/s). A split under ~5 on "
          "either side is a lead, not a finding.")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("paths", nargs="*", type=Path)
    ap.add_argument("--lab", type=Path, metavar="DIR",
                    help="retention --json files to join to their scripts")
    args = ap.parse_args()
    if args.lab:
        sys.exit(lab(args.lab))
    if not args.paths:
        ap.error("give a script, or --lab DIR")
    flagged = sum(bool(check(p)) for p in args.paths)
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
