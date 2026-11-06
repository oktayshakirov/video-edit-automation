"""Word timings for the karaoke: the sheet's lyrics, timed against the final mix.

    .venv/bin/python projects/song/come-back-at-five/timing.py

1. Separates the vocal from the final FLAC with demucs (htdemucs). Whisper
   times words far better on a dry vocal than over 808s.
2. Transcribes it with Whisper (large-v3-turbo, word timestamps).
3. Aligns Whisper's words to the *sheet's* words, so the screen shows what
   the lyric says, not what Whisper heard ("Limit reach", "a Jedi").
   A sheet word Whisper missed is placed between its matched neighbours.
   A sheet line with no matched word at all was not sung, and is dropped.

Writes `timing.json` next to this file: one entry per sung line, with each
word's start and end. That file is committed; the audio is not.

The two helpers run in other environments, because neither belongs in this
repo's venv: Whisper in `~/Coding/song-automation/.venv` (it transcribes
takes there too), demucs in `~/.local/share/song-automation/sepvenv`, which
borrows the ACE-Step engine's torch.
"""

from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINAL = Path.home() / "Desktop/songs/come-back-at-five-final.flac"
SHEET = Path.home() / "Coding/create-song-automation/projects/usage-limit/ace-step.md"
CACHE = Path.home() / ".cache/video-automation/song/come-back-at-five"
WHISPER_PY = Path.home() / "Coding/song-automation/.venv/bin/python"
DEMUCS_PY = Path.home() / ".local/share/song-automation/sepvenv/bin/python"

SEPARATE = r'''
import sys, torch, torchaudio, soundfile as sf
from demucs.pretrained import get_model
from demucs.apply import apply_model
m = get_model("htdemucs"); m.eval()
x, sr = sf.read(sys.argv[1], dtype="float32"); x = torch.from_numpy(x.T)[None]
y = apply_model(m, torchaudio.functional.resample(x, sr, m.samplerate), device="cpu")[0]
voc = torchaudio.functional.resample(y[m.sources.index("vocals")], m.samplerate, sr)
sf.write(sys.argv[2], voc.numpy().T, sr)
'''

TRANSCRIBE = r'''
import sys, json, mlx_whisper
r = mlx_whisper.transcribe(sys.argv[1], path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                           language="en", word_timestamps=True, condition_on_previous_text=False)
json.dump([{"w": w["word"].strip(), "s": w["start"], "e": w["end"]}
           for s in r["segments"] for w in s["words"]], open(sys.argv[2], "w"))
'''

NUMBERS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
           "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten",
           "21": "twenty one", "58": "fifty eight", "59": "fifty nine",
           "100": "hundred", "101": "hundred one", "9th": "nine"}


def norm(tok: str) -> list[str]:
    """One token as the words it would be sung as, lower case, no punctuation."""
    t = tok.lower().replace("%", " percent").replace("’", "'")
    out = []
    for part in re.split(r"[\s.:\-]+", t):
        part = re.sub(r"[^a-z0-9']", "", part).strip("'")
        if not part:
            continue
        out += NUMBERS.get(part, part).split()
    return out


def sheet_lines(path: Path) -> list[dict]:
    """[{section, text, words: [display words], adlibs: [...]}], in sung order."""
    body = path.read_text().split("---", 1)[1]
    lines, section = [], ""
    for raw in body.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith("["):
            section = raw.strip("[]").lower()
            continue
        adlibs = re.findall(r"\(([^)]*)\)", raw)
        text = re.sub(r"\s*\([^)]*\)", "", raw).strip()
        lines.append({"section": section, "text": text, "adlibs": adlibs,
                      "words": text.split()})
    return lines


def align(lines: list[dict], heard: list[dict]) -> list[dict]:
    # Flatten the sheet into sung tokens, remembering which display word each
    # came from ("twenty-one" may be two tokens, "AI's" one).
    sheet_tok, owner = [], []
    for li, line in enumerate(lines):
        for wi, w in enumerate(line["words"]):
            for t in norm(w):
                sheet_tok.append(t)
                owner.append((li, wi))
    heard_tok, heard_at = [], []
    for h in heard:
        for t in norm(h["w"]):
            heard_tok.append(t)
            heard_at.append((h["s"], h["e"]))
    times: dict[tuple[int, int], list[float]] = {}
    for a, b in _global_align(sheet_tok, heard_tok):
        s, e = heard_at[b]
        key = owner[a]
        times.setdefault(key, [s, e])
        times[key][1] = e
    out = []
    for li, line in enumerate(lines):
        got = [wi for wi in range(len(line["words"])) if (li, wi) in times]
        # A line counts as sung when a third of its words were heard. Below
        # that the matches are stray hook words borrowed by a neighbour.
        if len(got) < max(1, len(line["words"]) / 3):
            continue
        words = []
        for wi, w in enumerate(line["words"]):
            words.append({"w": w, "s": None, "e": None, **(
                {"s": times[(li, wi)][0], "e": times[(li, wi)][1]} if (li, wi) in times else {})})
        _fill(words)
        out.append({"section": line["section"], "text": line["text"],
                    "adlibs": line["adlibs"], "words": words,
                    "s": words[0]["s"], "e": words[-1]["e"],
                    "heard": round(len(got) / len(line["words"]), 2)})
    # Lines never overlap: a line ends by the time the next one starts.
    for a, b in zip(out, out[1:]):
        if a["e"] > b["s"]:
            a["e"] = b["s"]
            a["words"][-1]["e"] = min(a["words"][-1]["e"], b["s"])
    return out


def _similar(a: str, b: str) -> int:
    if a == b:
        return 3
    if len(a) > 2 and len(b) > 2 and (a[:3] == b[:3] or
                                       difflib.SequenceMatcher(a=a, b=b).ratio() >= 0.7):
        return 1
    return -2


def _global_align(a: list[str], b: list[str]) -> list[tuple[int, int]]:
    """Needleman-Wunsch: the one monotonic pairing of sheet and heard tokens.

    A greedy longest-match (difflib's) pairs a repeated hook with the wrong
    chorus and skips the verse between them - it dropped 50 seconds of
    verse on the first run. A global alignment cannot, because every token
    on both sides is accounted for in order.
    """
    GAP = -1
    n, m = len(a), len(b)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    move = [[0] * (m + 1) for _ in range(n + 1)]   # 0 diag, 1 up (skip a), 2 left (skip b)
    for i in range(1, n + 1):
        score[i][0], move[i][0] = i * GAP, 1
    for j in range(1, m + 1):
        score[0][j], move[0][j] = j * GAP, 2
    for i in range(1, n + 1):
        ai, row, prev = a[i - 1], score[i], score[i - 1]
        for j in range(1, m + 1):
            d = prev[j - 1] + _similar(ai, b[j - 1])
            u = prev[j] + GAP
            l = row[j - 1] + GAP
            if d >= u and d >= l:
                row[j], move[i][j] = d, 0
            elif u >= l:
                row[j], move[i][j] = u, 1
            else:
                row[j], move[i][j] = l, 2
    pairs, i, j = [], n, m
    while i > 0 and j > 0:
        mv = move[i][j]
        if mv == 0:
            if _similar(a[i - 1], b[j - 1]) > 0:
                pairs.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif mv == 1:
            i -= 1
        else:
            j -= 1
    return pairs[::-1]


def _fill(words: list[dict]) -> None:
    """Give every unheard word a slot between its heard neighbours, by length."""
    n = len(words)
    i = 0
    while i < n:
        if words[i]["s"] is not None:
            i += 1
            continue
        j = i
        while j < n and words[j]["s"] is None:
            j += 1
        left = words[i - 1]["e"] if i > 0 else (words[j]["s"] - 0.3 * (j - i) if j < n else 0)
        right = words[j]["s"] if j < n else left + 0.3 * (j - i)
        span = max(right - left, 0.12 * (j - i))
        total = sum(len(words[k]["w"]) for k in range(i, j))
        t = left
        for k in range(i, j):
            d = span * len(words[k]["w"]) / total
            words[k]["s"], words[k]["e"] = t, t + d
            t += d
        i = j


# What the take sings, where it differs from the sheet (checked by ear and by
# Whisper over the full mix, 2026-11-06). Each edit removes the aligned lines
# that start inside [a, b) and puts in the sung lines, with a rough window
# only - forced alignment times the words. The screen shows what is sung, in
# the sheet's spelling, and **a repeat is its own line** (the user's note: a
# line repeated by the take must start fresh, not wait half-lit mid-line).
EDITS = [
    # "refactor everything" is not sung
    (6.0, 11.0, [("intro - spoken word", "Fix the bug, write the tests", ["yeah"], 6.3, 10.7)]),
    # sounds like "B-Bye" here (the user's ear, 2026-11-06); hook 2 says "bye"
    (24.0, 25.5, [("hook", "Paid for the Max and it still told me B-Bye", [], 24.7, 27.7)]),
    # sung twice, the first time ending on the previous line's "bar climb"
    (52.0, 53.0, [("verse", "Twenty one percent, then a hundred, bar climb", [], 52.2, 53.95),
                  ("verse", "Twenty one percent, then a hundred, one prompt", [], 53.95, 55.8)]),
    # Whisper missed it on the vocal stem; it is there on the mix
    (63.95, 64.05, [("verse", "I wrote one line by hand and I'm already sick", [], 63.9, 66.25)]),
    # only "I went outside" of the line is sung
    (83.5, 84.5, [("bridge - spoken word", "I went outside", ["wow"], 84.9, 86.2)]),
    # hook 3: the take doubles the second line and runs "almost" into "only five"
    (86.0, 100.0, [("hook", "Limit reached, come back at five", ["five!"], 86.6, 90.1),
                   ("hook", "Limit reached, limit reached, come back at five", [], 90.1, 93.45),
                   ("hook", "Had a startup at noon, it was almost… it's only five", [], 93.45, 96.95),
                   ("hook", "Limit reached, come back at five", [], 96.95, 100.45)]),
    # two sheet lines merged into one
    (100.0, 102.0, [("hook", "Five o'clock hit, back in and I typed one line", ["one line"], 100.45, 103.9)]),
]


def apply_edits(lines: list[dict]) -> list[dict]:
    for a, b, sung in EDITS:
        lines = [ln for ln in lines if not (a <= ln["s"] < b)]
        for section, text, adlibs, s, e in sung:
            lines.append({"section": section, "text": text, "adlibs": adlibs, "s": s, "e": e,
                          "words": [{"w": w, "s": s, "e": e} for w in text.split()],
                          "heard": "edit"})
    return sorted(lines, key=lambda ln: ln["s"])


# Forced alignment: wav2vec2 (torchaudio WAV2VEC2_ASR_BASE_960H) fits each
# line's own words into its window on the vocal stem. Whisper's word times
# ran late and stretched, so the sweep lagged the voice and lines changed
# before they were lit (the user's note, 2026-11-06).
FORCE = r'''
import json, sys, torch, torchaudio, soundfile as sf
import torchaudio.functional as F
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().eval()
labels = bundle.get_labels(); idx = {c: i for i, c in enumerate(labels)}
x, sr = sf.read(sys.argv[1], dtype="float32"); x = x.mean(1) if x.ndim > 1 else x
x = torchaudio.functional.resample(torch.from_numpy(x), sr, 16000)
jobs = json.load(open(sys.argv[2])); out = []
for job in jobs:
    a, b = int(job["a"] * 16000), int(job["b"] * 16000)
    seg = x[a:b][None]
    with torch.inference_mode():
        em, _ = model(seg)
    lp = torch.log_softmax(em, -1)
    toks, owner = [], []
    for wi, w in enumerate(job["words"]):
        for c in w:
            toks.append(idx[c]); owner.append(wi)
    ali, scores = F.forced_align(lp, torch.tensor([toks], dtype=torch.int32), blank=0)
    spans = F.merge_tokens(ali[0], scores[0].exp())
    ratio = seg.shape[1] / lp.shape[1] / 16000
    words = [[None, None] for _ in job["words"]]
    for k, sp in enumerate(spans):
        w = words[owner[k]]
        t0, t1 = job["a"] + sp.start * ratio, job["a"] + sp.end * ratio
        w[0] = t0 if w[0] is None else min(w[0], t0)
        w[1] = t1 if w[1] is None else max(w[1], t1)
    out.append(words)
json.dump(out, open(sys.argv[3], "w"))
'''


def _letters(word: str) -> str:
    w = word.upper().replace("’", "'")
    for k, v in {"AI'S": "A IS", "B-BYE": "BBYE"}.items():
        w = w.replace(k, v)
    return "".join(c for c in w if c.isalpha() or c == "'")


def force_align(lines: list[dict], vocal: Path) -> list[dict]:
    """Time every word by aligning whole runs of lines at once.

    Aligned one line per window, the first and last words reached into the
    neighbours and consecutive lines overlapped by ~0.3s. A run of lines
    with no real gap goes in as one transcript - ad-libs included, since
    they are sung and would otherwise be pinned onto a lyric word - so the
    model itself decides where each line ends.
    """
    groups, cur = [], [0]
    for i in range(1, len(lines)):
        if lines[i]["s"] - lines[i - 1]["e"] > 0.9:
            groups.append(cur)
            cur = []
        cur.append(i)
    groups.append(cur)
    jobs, slots = [], []
    for g in groups:
        a = max(0.0, lines[g[0]]["s"] - 0.5)
        b = lines[g[-1]]["e"] + 0.6
        words, slot = [], []
        for i in g:
            for wi, w in enumerate(lines[i]["words"]):
                words.append(_letters(w["w"]) or "A")
                slot.append((i, wi))
            for ad in lines[i]["adlibs"]:
                for piece in ad.split():
                    if _letters(piece):
                        words.append(_letters(piece))
                        slot.append(None)
        jobs.append({"a": a, "b": b, "words": words})
        slots.append(slot)
    tmp_in, tmp_out = CACHE / "force-in.json", CACHE / "force-out.json"
    tmp_in.write_text(json.dumps(jobs))
    subprocess.run([str(DEMUCS_PY), "-c", FORCE, str(vocal), str(tmp_in), str(tmp_out)], check=True)
    for slot, words in zip(slots, json.loads(tmp_out.read_text())):
        for where, (s, e) in zip(slot, words):
            if where is None:
                continue
            w = lines[where[0]]["words"][where[1]]
            w["s"], w["e"] = round(s, 3), round(e, 3)
    for ln in lines:
        ln["s"], ln["e"] = ln["words"][0]["s"], ln["words"][-1]["e"]
    return lines


def main() -> int:
    CACHE.mkdir(parents=True, exist_ok=True)
    vocal, heard_json = CACHE / "vocal.wav", CACHE / "heard.json"
    if not vocal.exists() or "--fresh" in sys.argv:
        print("separating the vocal")
        mix = CACHE / "mix.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(FINAL), str(mix)], check=True)
        subprocess.run([str(DEMUCS_PY), "-c", SEPARATE, str(mix), str(vocal)], check=True)
    if not heard_json.exists() or "--fresh" in sys.argv:
        print("transcribing")
        subprocess.run([str(WHISPER_PY), "-c", TRANSCRIBE, str(vocal), str(heard_json)], check=True)
    lines = apply_edits(align(sheet_lines(SHEET), json.loads(heard_json.read_text())))
    lines = force_align(lines, vocal)
    (HERE / "timing.json").write_text(json.dumps(
        {"source": str(FINAL.name), "lines": lines}, indent=1))
    for line in lines:
        print(f"{line['s']:6.2f}-{line['e']:6.2f} {line['heard']!s:>7} [{line['section']}] {line['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
