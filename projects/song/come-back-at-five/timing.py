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


# What the take sings where the sheet and Whisper's vocal-stem pass disagree,
# timed by hand from a Whisper pass over the full mix (2026-11-06). The take
# merged two hook-3 lines into one, and sang only "I went outside" of the
# bridge's last line; the screen shows what is sung, in the sheet's words.
# Each entry: (section, text, adlibs, [word start times], end, replaces).
OVERRIDES = [
    ("verse", "I wrote one line by hand and I'm already sick", [],
     [64.0, 64.16, 64.44, 64.66, 64.92, 65.08, 65.28, 65.42, 65.56, 65.8], 66.2, None),
    ("hook", "Five o'clock hit, back in and I typed one line", ["one line"],
     [100.48, 100.88, 101.36, 102.34, 102.58, 102.8, 102.98, 103.18, 103.38, 103.58], 103.9,
     "Logged back in and I typed one line"),
    ("bridge - spoken word", "I went outside", ["wow"],
     [85.08, 85.18, 85.28], 85.9, "I went outside, the graphics are insane"),
]


def apply_overrides(lines: list[dict]) -> list[dict]:
    for section, text, adlibs, starts, end, replaces in OVERRIDES:
        words = text.split()
        assert len(words) == len(starts), text
        ends = starts[1:] + [end]
        entry = {"section": section, "text": text, "adlibs": adlibs,
                 "words": [{"w": w, "s": a, "e": b} for w, a, b in zip(words, starts, ends)],
                 "s": starts[0], "e": end, "heard": "by hand"}
        if replaces:
            lines = [ln for ln in lines if ln["text"] != replaces]
        lines.append(entry)
    return sorted(lines, key=lambda ln: ln["s"])


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
    lines = apply_overrides(align(sheet_lines(SHEET), json.loads(heard_json.read_text())))
    (HERE / "timing.json").write_text(json.dumps(
        {"source": str(FINAL.name), "lines": lines}, indent=1))
    for line in lines:
        print(f"{line['s']:6.2f}-{line['e']:6.2f} {line['heard']!s:>7} [{line['section']}] {line['text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
