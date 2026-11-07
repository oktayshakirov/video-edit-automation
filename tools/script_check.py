"""Does a project script say something the docs already forbid?

`opening_check.py` exists because a rule in `narration.md` was broken by four
Shorts in ten days: it was checked from memory of the script, not against the
file. The rules that outrank everything else - **no financial advice** on
thecrypto.wiki, **no promise of relief** on tinnitushelp.me - were in the same
state: stated in prose, in two skills and two project docs, and checked by
nobody. This reads what a script will actually show and say and flags the
shapes those docs name:

    PYTHONPATH=. .venv/bin/python tools/script_check.py \\
        projects/crypto-long/<name>.py projects/crypto-short/<name>.py
    PYTHONPATH=. .venv/bin/python tools/script_check.py --all     # audit

Run it on both scripts of a pair before preflight, beside the opening check
(`workflow.md` step 2). It exits 1 when anything is flagged.

**A flag is a prompt to look, not a verdict** - the same contract as the
opening check. "There is no cure" trips nothing (the negation is read), but
"a cure for the worry" would, and only the writer can say which it is. When a
flag is wrong for a good reason, say why in the handover and move on; when a
pattern is wrong every time, fix the pattern here.

**A rule only binds scripts written after it.** Each check carries the date
its rule was settled. A script first committed on or before that day reports
`predates` instead of a flag (the same day is ambiguous by a few hours, and
gets the benefit of it), so `--all` is an audit of the back catalogue, not 40
failures for a kicker rule that did not exist yet. A file git does not know
about (a new draft) is always checked in full.

What it reads: spoken text is the second half of a `(caption, spoken)` pair
and shown text the first, exactly as `core/voiceover.py` treats them; a
phoneme rule reads only the spoken half, a claim rule reads both - a claim on
screen is a claim. Where each rule is written down is in `RULES` below; the
docs remain the reference and this file only points at them.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------
# What a script shows and says


@dataclass
class Line:
    where: str          # "s3", "'How are the words made?' s2", "q1 option C"
    shown: str
    spoken: str

    @property
    def both(self) -> str:
        return self.shown if self.shown == self.spoken else (
            f"{self.shown} {self.spoken}".strip())


@dataclass
class Script:
    path: Path
    channel: str        # crypto | tinnitus | drone | other
    fmt: str            # long | short | quiz | other
    mod: object
    lines: list[Line] = field(default_factory=list)
    titles: list[tuple[str, str]] = field(default_factory=list)
    added: str | None = None   # first-commit date, YYYY-MM-DD


def classify(path: Path) -> tuple[str, str]:
    d = path.parent.name
    if d.startswith("quiz-"):
        return d.removeprefix("quiz-"), "quiz"
    for ch in ("crypto", "tinnitus", "drone"):
        if d.startswith(ch + "-"):
            return ch, d.removeprefix(ch + "-")
    return "other", "other"


def pieces(sentence) -> list[tuple[str, str]]:
    """A sentence as (shown, spoken) chunks. A chunk is a string, or a pair
    whose first item is shown and whose second is said."""
    if isinstance(sentence, str):
        return [(sentence, sentence)]
    out = []
    for p in sentence:
        if isinstance(p, str):
            out.append((p, p))
        elif (isinstance(p, (tuple, list)) and len(p) >= 2
              and isinstance(p[0], str) and isinstance(p[1], str)):
            out.append((p[0], p[1]))
        elif isinstance(p, (tuple, list)) and p and isinstance(p[0], str):
            out.append((p[0], p[0]))
    return out


def as_line(where: str, sentence) -> Line:
    ch = pieces(sentence)
    return Line(where, " ".join(s for s, _ in ch).strip(),
                " ".join(k for _, k in ch).strip())


def load(path: Path) -> Script:
    spec = importlib.util.spec_from_file_location(
        "script_check_" + path.stem.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    channel, fmt = classify(path)
    sc = Script(path, channel, fmt, mod, added=first_commit(path))

    sections = getattr(mod, "SECTIONS", None)
    if sections:
        for sec in sections:
            t = getattr(sec, "title", "")
            if getattr(sec, "card", True):
                spoken = getattr(sec, "spoken_title", None) or t
                sc.lines.append(Line(f"card {t!r}", t, spoken))
                sc.titles.append((f"chapter {t!r}", t))
            for i, s in enumerate(getattr(sec, "sentences", []), 1):
                sc.lines.append(as_line(f"{t!r} s{i}", s))
    for i, s in enumerate(getattr(mod, "SENTENCES", None) or [], 1):
        sc.lines.append(as_line(f"s{i}", s))
    if fmt == "short" and sc.lines:
        sc.titles.append(("s1, the title question", sc.lines[0].shown))

    title = getattr(mod, "TITLE", None)
    if isinstance(title, tuple) and title and isinstance(title[0], str):
        sc.lines.append(Line("title card", title[0],
                             title[1] if len(title) > 1 else title[0]))
    for qi, q in enumerate(getattr(mod, "QUESTIONS", None) or [], 1):
        sc.lines.append(Line(f"q{qi}", q.question, q.question))
        for oi, o in enumerate(q.options):
            sc.lines.append(Line(f"q{qi} option {'ABCD'[oi]}", o, o))
        sc.lines.append(Line(f"q{qi} answer", q.answer, q.answer))

    meta = getattr(mod, "META", None)
    if meta is not None:
        sc.titles.insert(0, ("Meta.title", meta.title))
        for k in ("hook", "summary"):
            v = getattr(meta, k, "")
            if v:
                sc.lines.append(Line(f"Meta.{k}", v, ""))
    return sc


def first_commit(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "log", "--diff-filter=A", "--follow",
             "--format=%as", "--", str(path.resolve().relative_to(REPO))],
            capture_output=True, text=True, timeout=20).stdout.split()
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return None
    return out[-1] if out else None


# --------------------------------------------------------------------------
# The rules


@dataclass
class Rule:
    id: str
    doc: str                     # where the rule is written down
    channels: tuple[str, ...]    # () = every channel
    formats: tuple[str, ...]     # () = every format
    since: str | None = None     # binds scripts first committed after this day

    def applies(self, sc: Script) -> bool:
        return ((not self.channels or sc.channel in self.channels)
                and (not self.formats or sc.fmt in self.formats))


def rx(*alts: str) -> re.Pattern:
    return re.compile("|".join(f"(?:{a})" for a in alts), re.I)


# A claim word is excused when a negation sits just before it: "there is no
# cure", "nothing reliably removes it", "not a fix".
NEGATION = re.compile(
    r"\b(no|not|never|nothing|none|isn't|aren't|won't|doesn't|don't|can't|"
    r"cannot|without|nor|neither|no one|nobody|myth|claims?|promises?|"
    r"sold as|marketed as|called)\b[^.?!]{0,28}$", re.I)


# ...and so is a claim about the past: "every old cure went wrong", "the
# cures his doctors tried". History is the subject there, not a promise.
HISTORY_BEFORE = re.compile(
    r"\b(?:old|ancient|folk|medieval|historical|quack|miracle|so-called)\s+$",
    re.I)
HISTORY_AFTER = re.compile(
    r"^\s+(?:(?:his|her|their)\s+(?:doctors?|physicians?)|went wrong|"
    r"failed|did not work|didn't work)\b", re.I)


def unnegated(pattern: re.Pattern, text: str) -> list[str]:
    hits = []
    for m in pattern.finditer(text):
        before, after = text[:m.start()], text[m.end():]
        if NEGATION.search(before) or HISTORY_BEFORE.search(before) \
                or HISTORY_AFTER.match(after):
            continue
        hits.append(m.group(0))
    return hits


WINDUP = rx(r"here(?:'s| is) the (?:question|thing)",
            r"almost nobody asks", r"what you need to understand is",
            r"the question you should be asking")

ENGAGEMENT_CTA = rx(r"\bin the comments\b", r"\blet me know\b",
                    r"\bsubscribe\b", r"\b(?:linked|link) below\b",
                    r"\bsources? (?:are )?below\b", r"\bhit the bell\b")

DISCLAIMER = rx(r"\bfinancial advice\b", r"\bmedical advice\b")

# thecrypto.wiki: "names no price level, predicts nothing, rates no
# platform, and recommends buying or selling nothing" (video-crypto skill).
ADVICE = rx(
    r"\byou (?:should|must|need to|ought to|have to) (?:buy|sell|invest|hold|hodl|get in)\b",
    r"\b(?:buy|sell) (?:now|the dip|before it)\b",
    r"\b(?:good|right|best) (?:time|moment) to (?:buy|sell|invest|get in)\b",
    r"\bto the moon\b",
    r"\bguaranteed (?:returns?|profits?|gains?)\b",
    r"\bprice target\b",
    r"\b(?:will|is going to|is about to) (?:go up|go down|moon|pump|crash|skyrocket|explode|double|10x)\b",
    r"\b(?:will|is going to|could) (?:hit|reach) \$?\d",
    r"\b(?:best|safest) (?:exchange|wallet|coin|token|platform|crypto|place) (?:to|for)\b",
    r"\bworth (?:buying|investing in)\b",
    r"\b(?:easy|free|passive) money\b",
)

# tinnitushelp.me: "Never promise relief, improvement, or a cure - not even
# softly, not even as 'this can help'" (projects/tinnitus.md).
RELIEF = rx(
    r"\bcur(?:e|es|ed|ing)\b",
    r"\brelie(?:f|ve|ves|ved)\b",
    r"\bget rid of\b",
    r"\b(?:stop|silence|fix|eliminate|end|beat|kill) (?:your|the|my) (?:tinnitus|ringing)\b",
    r"\b(?:can|will|could|may|might|should) help\b",
    r"\bhelps? (?:you|with|reduce|ease|calm|quiet)\b",
    r"\bmake (?:it|the ringing|your tinnitus) go away\b",
    r"\breduces? (?:your|the) (?:tinnitus|ringing)\b",
    r"\bgo away for good\b",
)

# Initialisms and words espeak mangles; say what they mean instead
# (projects/tinnitus.md, "Phonemes to avoid outright").
PHONEMES = re.compile(
    r"\b(?:ENT|CBT|TMJ)\b|presbycusis|m[eé]ni[eè]re", re.I)
PHONEME_CASE = re.compile(r"\b(?:ENT|CBT|TMJ)\b")   # "ent" in a word is fine

# A clause in question word order: an auxiliary first ("Does Tinnitus Go
# Away"), or a wh-word straight into one ("What Is a Seed Phrase", "How Long
# Does It Last"). A wh-word into a subject is a noun clause and a statement -
# "How North Korea Stole $6.36 Billion" shipped that way on purpose - so it
# is left alone; whether a statement *reads* as a question is the writer's
# call (the "Why It Is Worse at Night" case in narration.md).
AUX = r"(?:is|are|was|were|does|do|did|can|could|should|will|would|has|have)"
QUESTION_ORDER = re.compile(
    rf"^(?:{AUX}|(?:how|why|what|which|who|when|where)"
    rf"(?:\s+(?:much|many|long|often|loud|far|big|bad|safe|exactly))?"
    rf"\s+{AUX})\b", re.I)

ANSWER_LETTER = rx(r"\bthe (?:correct |right )?answer is [A-D]\b",
                   r"^[A-D][.)]\s")


# `since` is the date of the commit that first wrote the rule down (found with
# `git log -S` on its wording, 2026-11-05). A rule without one has held since
# the channel's first commit.
RULES = {
    "windup": Rule("windup", "narration.md, 'Phrases that are banned'", (), (),
                   since="2026-08-19"),
    "outro-cta": Rule("outro-cta", "narration.md, 'The outro asks the question and stops'; "
                      "video-quiz skill", ("crypto", "tinnitus"), ("long", "quiz"),
                      since="2026-08-31"),
    "short-disclaimer": Rule("short-disclaimer", "narration.md, 'The compliance line is "
                             "long-form only'", ("crypto", "tinnitus"), ("short",),
                             since="2026-09-04"),
    "financial-advice": Rule("financial-advice", "video-crypto skill, 'The line that "
                             "outranks everything else'; projects/crypto.md", ("crypto",), ()),
    "relief-promise": Rule("relief-promise", "projects/tinnitus.md, 'The rule that "
                           "outranks every production consideration'", ("tinnitus",), ()),
    "phoneme": Rule("phoneme", "projects/tinnitus.md, 'Phonemes to avoid outright'",
                    ("tinnitus",), ()),
    "title-question-mark": Rule("title-question-mark", "narration.md, 'Titles: a question "
                                "gets a question mark'", ("crypto", "tinnitus"), (),
                                since="2026-08-18"),
    "answer-letter": Rule("answer-letter", "video-quiz skill; Question.answer docstring",
                          (), ("quiz",)),
    "source-post": Rule("source-post", "workflow.md step 3", ("crypto", "tinnitus"), (),
                        since="2026-08-27"),
    "demand": Rule("demand", "workflow.md step 3 (E11)", ("crypto", "tinnitus"),
                   ("long", "short"), since="2026-10-25"),
    "kicker": Rule("kicker", "video-crypto / video-tinnitus skills, 'Chapter cards are "
                   "the band card'", ("crypto", "tinnitus"), ("long",), since="2026-10-21"),
    # The editor's notes on `random-tokens-in-wallet` (2026-11-06): the new
    # tools went unused, the disclaimer sat on rain again, and four phone
    # clips showed a social feed.
    "toolbox": Rule("toolbox", "workflow.md, 'The toolbox is not optional'",
                    ("crypto", "tinnitus"), ("long",), since="2026-11-06"),
    "disclaimer-bg": Rule("disclaimer-bg", "narration.md, 'The compliance line is "
                          "long-form only' (its background)", ("crypto", "tinnitus"),
                          ("long",), since="2026-11-06"),
    "feed-clip": Rule("feed-clip", "footage.md, 'A phone's screen is part of the "
                      "picture'", ("crypto", "tinnitus"), ("long", "short"),
                      since="2026-11-06"),
    # The editor (2026-11-06): the closing card is slow and viewers already
    # leave before the end - the last line is a plain captioned sentence.
    "short-outro": Rule("short-outro", "shorts.md, 'No outro card on a Short'",
                        ("crypto", "tinnitus"), ("short",), since="2026-11-06"),
    # The editor (2026-11-08): no one cover style is forced - pick per topic
    # and picture - but every video says which it used, so the review can
    # compare views and clicks by style.
    "cover-style": Rule("cover-style", "thumbnails.md, 'Cover styles are a choice, "
                        "and every video says which'", ("crypto", "tinnitus"),
                        ("long", "short"), since="2026-11-08"),
}

# The cover styles a build may declare in `COVER_STYLE`. Add a name here
# when a new kind of cover ships, with a line in thumbnails.md.
COVER_STYLES = {
    "text": "a picture and the headline, no marks",
    "arrow": "an arrow and/or a ring pointing at something in the picture",
    "beat": "a drawn graphic from the video as the cover",
}

# `outro=` given anything but None, in code (not a comment or docstring).
OUTRO_KW = re.compile(r"^[^#\n]*\boutro\s*=\s*(?!None\b)\S", re.M)

# A depth move, a cutout, physics, or a captured page - any one of these.
TOOL_GRAPHICS = ("behind", "pile")
# Weather and water: the disclaimer's old default, which has nothing to do
# with any one video.
WEATHER = re.compile(r"rain|water|ocean|sea-|waves?|storm|fog|mist", re.I)
# A stock search for a scrolling phone returns social feeds.
FEED = re.compile(r"scroll|feed|social|instagram|tiktok|reels", re.I)


def shots_of(mod) -> list:
    out = []
    for sec in getattr(mod, "SECTIONS", None) or []:
        out += [sh for sh in getattr(sec, "shots", []) if sh is not None]
    out += [sh for sh in getattr(mod, "SHOTS", None) or [] if sh is not None]
    return out


@dataclass
class Finding:
    rule: str
    where: str
    detail: str


def check(sc: Script) -> list[Finding]:
    f: list[Finding] = []
    on = {k for k, r in RULES.items() if r.applies(sc)}

    for ln in sc.lines:
        if "windup" in on:
            for m in WINDUP.finditer(ln.both):
                f.append(Finding("windup", ln.where, f"{m.group(0)!r} - ask the "
                                 f"question instead of announcing it"))
        if "financial-advice" in on:
            for h in unnegated(ADVICE, ln.both):
                f.append(Finding("financial-advice", ln.where,
                                 f"{h!r} in {ln.both!r}"))
        if "relief-promise" in on:
            for h in unnegated(RELIEF, ln.both):
                f.append(Finding("relief-promise", ln.where,
                                 f"{h!r} in {ln.both!r} - say what it is, "
                                 f"not what it will do"))
        if "phoneme" in on and ln.spoken:
            for m in PHONEMES.finditer(ln.spoken):
                w = m.group(0)
                if w.upper() in ("ENT", "CBT", "TMJ") and not PHONEME_CASE.match(w):
                    continue
                f.append(Finding("phoneme", ln.where, f"{w!r} is spoken - "
                                 f"give the line a (caption, spoken) pair"))
        if "short-disclaimer" in on and DISCLAIMER.search(ln.both):
            f.append(Finding("short-disclaimer", ln.where,
                             "a Short never carries the compliance line"))
        if "answer-letter" in on and ln.where.endswith("answer") \
                and ANSWER_LETTER.search(ln.shown):
            f.append(Finding("answer-letter", ln.where,
                             "the format names the letter; `answer` is the "
                             "because only"))

    if "outro-cta" in on and sc.lines:
        spoken = [ln for ln in sc.lines if ln.spoken and not
                  ln.where.startswith("Meta.")]
        for ln in spoken[-2:]:
            for m in ENGAGEMENT_CTA.finditer(ln.both):
                f.append(Finding("outro-cta", ln.where,
                                 f"{m.group(0)!r} - the closing line asks and "
                                 f"stops; the description carries the CTA"))

    if "title-question-mark" in on:
        for where, t in sc.titles:
            for part in re.split(r"(?<=\?)|[:–—|]| - ", t):
                part = part.strip()
                if QUESTION_ORDER.match(part) and not part.endswith("?"):
                    f.append(Finding("title-question-mark", where,
                                     f"{part!r} reads as a question - "
                                     f"invert it and punctuate it"))

    if "source-post" in on and not hasattr(sc.mod, "SOURCE_POST"):
        text = sc.path.read_text(errors="replace")
        if not re.search(r"/posts/[a-z0-9-]+|content/posts/[a-z0-9-]+\.mdx",
                         text):
            f.append(Finding("source-post", "module",
                             "no SOURCE_POST - topics.py cannot see which "
                             "article this covers (None for an off-site topic)"))
    if "demand" in on and not hasattr(sc.mod, "DEMAND"):
        f.append(Finding("demand", "module", "no DEMAND - the review cannot "
                         "tag this video (None when it had no evidence)"))
    if "cover-style" in on:
        style = getattr(sc.mod, "COVER_STYLE", None)
        if style is None:
            f.append(Finding("cover-style", "module",
                             "no COVER_STYLE - the review cannot compare this "
                             f"cover's style ({', '.join(COVER_STYLES)})"))
        elif style not in COVER_STYLES:
            f.append(Finding("cover-style", "module",
                             f"COVER_STYLE {style!r} is not one of "
                             f"{', '.join(COVER_STYLES)} - add it to "
                             "COVER_STYLES and thumbnails.md if it is new"))
    shots = shots_of(sc.mod)
    if "toolbox" in on and shots:
        used = [sh for sh in shots
                if getattr(sh, "graphic", None) in TOOL_GRAPHICS
                or getattr(sh, "parallax", 0) or getattr(sh, "isolate", 0)
                or getattr(sh, "pop", False)
                or "captures/" in str(getattr(sh, "clip", "") or "")]
        if not used:
            f.append(Finding("toolbox", "shots", "no captured page, depth move, "
                             "cutout or pile anywhere - a real page "
                             "(`screencap`), the site's photo with `behind`/"
                             "`isolate`/`parallax`, or `pile` for money moving"))
    if "disclaimer-bg" in on:
        from video_automation.longform.meta import is_disclaimer
        for sh in shots:
            pay = getattr(sh, "payload", ()) or ()
            line = pay[1] if (isinstance(pay, tuple) and len(pay) > 1
                              and isinstance(pay[1], str)) else ""
            clip = getattr(sh, "clip", None)
            if line and is_disclaimer(line) and clip is not None \
                    and WEATHER.search(Path(clip).parent.name):
                f.append(Finding("disclaimer-bg", Path(clip).parent.name,
                                 "the disclaimer sits on weather - put it on "
                                 "this video's own subject (`stillclip`)"))
    if "short-outro" in on:
        try:
            src = sc.path.read_text()
        except OSError:
            src = ""
        # Drop the module docstring, which may quote the old call.
        doc = getattr(sc.mod, "__doc__", None) or ""
        if doc:
            src = src.replace(doc, "", 1)
        if OUTRO_KW.search(src):
            f.append(Finding("short-outro", "render call",
                             "an `outro=` closing card - say the last line as an "
                             "ordinary sentence instead"))
    if "feed-clip" in on:
        seen = set()
        for sh in shots:
            clip = getattr(sh, "clip", None)
            if clip is None or "captures/" in str(clip):
                continue
            slug = Path(clip).parent.name
            if FEED.search(slug) and clip not in seen:
                seen.add(clip)
                f.append(Finding("feed-clip", f"{slug}/{Path(clip).name}",
                                 "from a scrolling-phone search - look at what is "
                                 "on its screen; a social feed is off-topic"))
    if "kicker" in on:
        for sec in getattr(sc.mod, "SECTIONS", None) or []:
            if getattr(sec, "card", True) and not getattr(sec, "kicker", ""):
                f.append(Finding("kicker", f"chapter {sec.title!r}",
                                 "no kicker - the band card shows 'CHAPTER n'"))
    return f


# --------------------------------------------------------------------------


def environmental(e: Exception) -> bool:
    """An import that fails for want of this machine, not of the script.

    A sibling package (`audiobook_automation` for the read-along samples) or a
    macOS font used at import time - `crypto-short/crypto-exchanges` measures
    its `compare` text when it loads. `core.fontshim` is deliberately not
    installed here: what a script draws should be judged in the real fonts.
    (No script *writes* at import any more - `workflow.md` step 3.)
    """
    if isinstance(e, ModuleNotFoundError):
        return not (e.name or "").startswith("video_automation")
    return isinstance(e, OSError) and "cannot open resource" in str(e)


def shallow() -> bool:
    try:
        return subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "--is-shallow-repository"],
            capture_output=True, text=True, timeout=10).stdout.strip() == "true"
    except (OSError, subprocess.TimeoutExpired):
        return False


def report(path: Path, quiet: bool = False) -> tuple[int, int]:
    """Print one script's findings. Returns (flags, predates)."""
    try:
        sc = load(path)
    except Exception as e:
        if environmental(e):
            print(f"\n{path}\n  - not checked here: {type(e).__name__}: {e}")
            return 0, 0
        print(f"\n{path}\n  ! does not import: {type(e).__name__}: {e}")
        return 1, 0
    flags, old = [], []
    for fd in check(sc):
        since = RULES[fd.rule].since
        (old if since and sc.added and sc.added <= since else flags).append(fd)
    if quiet and not flags:
        return 0, len(old)
    print(f"\n{path}  [{sc.channel} {sc.fmt}"
          f"{', added ' + sc.added if sc.added else ', not committed'}]")
    for fd in flags:
        print(f"  ! {fd.rule:20s} {fd.where}: {fd.detail}")
    if old:
        rules = sorted({fd.rule for fd in old})
        print(f"  - predates {', '.join(rules)} ({len(old)} finding(s), "
              f"not flagged)")
    if not flags and not old:
        print("  ok")
    return len(flags), len(old)


def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("projects", nargs="*", type=Path,
                    help="projects/*/*.py build scripts")
    ap.add_argument("--all", action="store_true",
                    help="every crypto, tinnitus and quiz script, flagged "
                         "ones only")
    ap.add_argument("--rules", action="store_true",
                    help="list the rules and where each is written down")
    args = ap.parse_args()

    if args.rules:
        for r in RULES.values():
            scope = "/".join(r.channels or ("all",)) + " " + "/".join(
                r.formats or ("all",))
            since = f"  since {r.since}" if r.since else ""
            print(f"{r.id:20s} {scope:28s} {r.doc}{since}")
        return
    paths = list(args.projects)
    if args.all:
        paths = sorted(p for d in ("crypto-long", "crypto-short",
                                   "tinnitus-long", "tinnitus-short",
                                   "quiz-crypto", "quiz-tinnitus")
                       for p in (REPO / "projects" / d).glob("*.py"))
    if not paths:
        ap.error("name one or more scripts, or pass --all")
    if shallow():
        print("! shallow clone: first-commit dates stop at the clone boundary, "
              "so older scripts look new. Run `git fetch --unshallow` first.")
    total = old = flagged = 0
    for p in paths:
        n, o = report(p, quiet=args.all)
        total += n
        old += o
        flagged += bool(n)
    print(f"\n{len(paths)} script(s): {total} flag(s) in {flagged}, "
          f"{old} older finding(s) predate their rule")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
