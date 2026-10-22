"""Does sentence 2 of a Short keep the answer back, or hand it over?

Eleven retention curves (2026-10-11, `docs/video/narration.md` "Confirmed
2026-10-11") split on one question: **after sentence 2, could the viewer leave
and say the answer to the title question?** Every Short where they could lost
half its audience by 7-11s, no better than before the frame-zero hook existed.
Every Short where they could not kept half to 11.6-28.8s. The opener made no
difference either way.

The rule was in `narration.md` from 2026-10-01 and four Shorts built after it
still broke it, because the check was done from memory of the script rather
than against it. This prints the actual opening - title question, sentence 2,
and the word the opener reveals on screen - so the question is asked of the
file that will be rendered:

    PYTHONPATH=. .venv/bin/python tools/opening_check.py \\
        projects/crypto-short/<name>.py

It cannot judge the answer; that is the writer's call. It flags the shapes
that were verdicts every time they shipped, and exits 1 when it does:

- a **yes/no title question** - any natural sentence 2 is "yes";
- sentence 2 **opening on a verdict** - "Yes", "It can", "Usually";
- a **very short first clause after a who/what question** - "Hal Finney.";
- a **redacted hook hiding only a placeholder** - `[one source]`,
  `[two things]` - which keeps the verdict back and reveals nothing.

It also prints the word the opener lands on, without flagging it: `hook=`
and `at_word=` are meant to be said in sentence 2, so the word is always
there. Look at it hardest anyway - when the hidden word *is* the answer,
the hook itself puts the verdict in sentence 2 (`[Hal Finney]`,
`[explosion]`, `[30 seconds]`).

A flag is a prompt to look, not a failure. "Not a person. It is an
exchange" trips the short-clause flag and held well, because it overturns
the title's assumption instead of confirming it.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import sys
from pathlib import Path

YES_NO = {"can", "could", "does", "do", "did", "is", "are", "was", "were",
          "will", "would", "should", "has", "have"}
WHO_WHAT = {"who", "what", "which", "where", "when"}
VERDICT_START = re.compile(
    r"^(yes|no|yep|nope|usually|sometimes|probably|maybe|not really|"
    r"it (can|does|did|is|will|was)|they (can|do|did|are|were))\b", re.I)
VERDICT_ANY = re.compile(r"\bthe answer is (yes|no)\b", re.I)
# Opener fields that are layout and timing, not what the viewer reads.
QUIET = {"frame", "accent", "built", "hold", "punch", "at_fixed"}
# A redacted word made only of these is a placeholder: it keeps the verdict
# back, but the reveal shows nothing worth seeing (`shorts.md`, "A hidden
# word must be worth revealing", 2026-10-22 - `[one source]`).
PLACEHOLDER = {"a", "an", "the", "one", "two", "three", "four", "five", "few",
               "thing", "things", "source", "sources", "reason", "reasons",
               "way", "ways", "part", "parts", "step", "steps", "kind",
               "kinds", "request", "question", "answer", "rule", "rules",
               "secret", "trick", "factor", "factors", "place", "job",
               "word", "words", "detail", "problem", "catch", "mistake"}


def load(path: Path):
    """Import a project module by path (hyphenated names are not importable)."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def text(sentence) -> str:
    """A SENTENCES entry as its caption text.

    An entry is a tuple of pieces; a piece is a string, or a pair whose first
    item is what is shown (a respelling or an overlay comes second).
    """
    pieces = sentence if isinstance(sentence, tuple) else (sentence,)
    out = []
    for p in pieces:
        if isinstance(p, str):
            out.append(p)
        elif isinstance(p, tuple) and p and isinstance(p[0], str):
            out.append(p[0])
    return " ".join(out)


def opener(path: Path, mod) -> tuple[str, str | None]:
    """The `hook=` / `opener=` passed to the render, and the word it lands on."""
    src = path.read_text()
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.Call):
            continue
        for kw in node.keywords:
            if kw.arg not in ("hook", "opener"):
                continue
            if isinstance(kw.value, ast.Name):
                value = getattr(mod, kw.value.id, None)
                described = repr(value) if isinstance(value, str) else (
                    f"{type(value).__name__}(" + ", ".join(
                        f"{k}={v!r}" for k, v in vars(value).items()
                        if v not in (None, "") and k not in QUIET) + ")")
                shown = f"{kw.arg}={kw.value.id} = {described}"
            else:
                value = None
                shown = f"{kw.arg}={ast.get_source_segment(src, kw.value)}"
            if kw.arg == "hook":
                hook = value if isinstance(value, str) else shown
                m = re.search(r"\[([^\]]+)\]", hook)
                return shown, m.group(1) if m else None
            m = re.search(r"at_word\s*=\s*['\"]([^'\"]+)['\"]", shown)
            if m:
                return shown, m.group(1)
            word = getattr(value, "at_word", None)
            return shown, word
    return "none", None


def check(path: Path) -> list[str]:
    mod = load(path)
    sentences = getattr(mod, "SENTENCES", None)
    if not sentences or len(sentences) < 2:
        print(f"{path}: no SENTENCES with two entries - nothing to check")
        return []
    s1, s2 = text(sentences[0]), text(sentences[1])
    shown, word = opener(path, mod)

    print(f"\n{path}")
    print(f"  title question  {s1}")
    print(f"  sentence 2      {s2}")
    print(f"  opener          {shown}")
    if word:
        print(f"  lands on        {word!r}")

    flags = []
    first = s1.split()[0].lower().strip("?,") if s1.split() else ""
    if first in YES_NO:
        flags.append("yes/no title question - sentence 2 must not say, or "
                     "let the viewer infer, the yes")
    if VERDICT_START.match(s2) or VERDICT_ANY.search(s2):
        flags.append("sentence 2 opens on a verdict")
    clause = re.split(r"[.!?]", s2, maxsplit=1)[0]
    if first in WHO_WHAT and len(clause.split()) <= 4:
        flags.append(f"short first clause after a {first}-question "
                     f"({clause!r}) - is it the answer itself?")

    if word and shown.startswith("hook") and all(
            w.strip(".,?!").lower() in PLACEHOLDER for w in word.split()):
        flags.append(f"the hidden word {word!r} is a placeholder - the reveal "
                     f"shows nothing worth seeing. Use the pair's opener, a "
                     f"Counter/Stamp, or a statement hook")
    for f in flags:
        print(f"  ! {f}")
    if word:
        said = "says" if word.lower() in s2.lower() else "does not say"
        print(f"  ? sentence 2 {said} the landing word {word!r} - is it the "
              f"answer to the title question?")
    print("  Cover everything after sentence 2. Can the title question be "
          "answered from these two lines? If no, good. If yes, the answer "
          "must overturn what the title assumed and open the next question "
          "in the same sentence - a plain or confirming answer is a verdict. "
          "Rewrite it.")
    return flags


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projects", nargs="+", type=Path,
                    help="projects/*-short/*.py build scripts")
    args = ap.parse_args()
    flagged = sum(bool(check(p)) for p in args.projects)
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
