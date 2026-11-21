"""A narration the editor recorded, in place of a synthesised one.

**Built 2026-11-21 for OktAI**, the channel Oktay presents himself. Every
other format speaks its script with Kokoro, and the whole engine is timed off
what `voiceover.build_narration_aligned` returns: one track, one `Caption` per
script chunk, the total length. This returns exactly that triple from a
recording, so the long form, the Short, the beats, the captions and the mix
need no other change:

    from video_automation.core.recorded import Recording
    render_long(SECTIONS, out, work, brand=OKTAI,
                voice=Recording(Path("~/Movies/oktai/pipeline-long.mov")))

## What happens to the recording

1. **Transcribed word by word** with timestamps (`transcribe`): Whisper large
   v3 turbo on MLX, run offline. The model and `mlx_whisper` live in
   `create-song-automation`'s venv - installing them here would pull torch,
   ~2.5 GB, into a venv that was kept free of it on purpose (`voice.md`). So
   it runs as a subprocess of that interpreter (`WHISPER_PYTHON` overrides
   it), and the result is cached by the file's hash.
2. **Matched to the script** (`align`). Each sentence is searched for in the
   transcript, every take of it is a candidate, and one take per sentence is
   chosen in script order. **The last good take wins**: the way to fix a
   stumble while recording is to say the sentence again, and that is the
   take that is kept. False starts, re-reads and anything not in the script
   between takes are cut.
3. **Cut and joined** (`_assemble`). Consecutive sentences from one take keep
   the real pause between them - that is the human prosody a synthesised read
   never had - capped at `max_pause`. Where a retake was cut out, the join
   gets the scripted gap, filled with the recording's own room tone rather
   than digital silence, which would sound like a dropout.
4. **Cleaned and levelled**: a high-pass, light de-noise, de-ess, gentle
   compression, and `loudnorm` to -14 LUFS - where the Kokoro narrations
   measure, so the bed and the sidechain behave exactly as they do now.

## What it writes next to the recording

- `NAME.report.txt` - per sentence: the take used, what was said that the
  script does not have, and what the script has that was not said. **Read it
  before the build is reviewed**: a word the editor changed while reading is
  in the voice and not in the captions until the script is changed to match.
- `NAME.edl.json` - the edit: which source seconds went where. The camera
  box (`core/facecam.py`) cuts the face video with it, so the lips match the
  voice that was kept.

`NAME` is the recording's name plus the script's hash, so a long form and its
Short recorded into one file each get their own.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SR = 48000
CACHE = Path(os.environ.get("VIDEO_AUTOMATION_TRANSCRIPTS",
                            Path.home() / ".cache/video-automation/transcripts"))
WHISPER_PYTHON = Path(os.environ.get(
    "WHISPER_PYTHON",
    Path.home() / "Coding/create-song-automation/.venv/bin/python"))
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"

# The clean-up chain. Light on purpose: a home recording should sound like a
# person in a room, not like a processed voice. `afftdn` at -25 dB takes the
# hiss and fan out without the underwater artefact stronger settings leave.
CLEAN = ("highpass=f=75,"
         "afftdn=nf=-25,"
         "deesser=i=0.35,"
         "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=120:makeup=2,"
         "loudnorm=I=-14:TP=-1.5:LRA=9")

MATCH = 0.78          # two words are "the same" at this difflib ratio or above
MIN_SCORE = 0.55      # a take must match at least this share of its sentence
LATER = 0.30          # how much the latest take is preferred over the first
GOOD = 0.75           # ...when it matches at least this share of the sentence
PRE = 0.06            # seconds kept before a sentence's first word
POST = 0.14           # ...and after its last, for the release of the word
FADE = 0.010


@dataclass
class Recording:
    """The voice to use, and optionally the face to go with it.

    `audio` may be a WAV, M4A, MP3 or a video file (its audio is used).
    `video` is the face recording for the camera box; leave it None when the
    face is in `audio`'s own file, or there is no face. `window` limits the
    search to a stretch of the file, in seconds - for one file holding both
    the long form's and the Short's scripts, when the two share sentences.
    """

    audio: Path
    video: Path | None = None
    window: tuple[float, float] | None = None
    max_pause: float = 0.75       # longest natural pause kept between sentences
    clean: bool = True
    # Set by the build: where this recording's edit file and report went,
    # so the camera box can find the edit without recomputing its name.
    edl: Path | None = field(default=None, init=False)
    report: Path | None = field(default=None, init=False)
    captions: list | None = field(default=None, init=False, repr=False)

    def __post_init__(self):
        self.audio = Path(self.audio).expanduser()
        if self.video is not None:
            self.video = Path(self.video).expanduser()

    @property
    def face(self) -> Path | None:
        if self.video is not None:
            return self.video
        return self.audio if _has_video(self.audio) else None


# ---------------------------------------------------------------------------
# transcription
# ---------------------------------------------------------------------------

def _has_video(path: Path) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
         "stream=codec_type", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True).stdout
    return "video" in out


def _hash(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()[:16]


def load_audio(path: Path, sr: int = SR) -> np.ndarray:
    """Mono float32 at `sr`, from any file ffmpeg can read."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
         "-ar", str(sr), "-f", "f32le", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


_WHISPER = r"""
import json, sys
import mlx_whisper
r = mlx_whisper.transcribe(sys.argv[1], path_or_hf_repo=sys.argv[2],
                           word_timestamps=True, language="en",
                           condition_on_previous_text=False)
words = [{"w": w["word"], "s": w["start"], "e": w["end"],
          "p": w.get("probability", 1.0)}
         for seg in r["segments"] for w in seg.get("words", [])]
json.dump({"text": r["text"], "words": words}, sys.stdout)
"""


def transcribe(path: Path) -> list[dict]:
    """Every spoken word with `s`/`e` seconds, cached by the file's content.

    `condition_on_previous_text=False` because a recording with retakes is
    exactly where Whisper, conditioned on its own last sentence, "corrects"
    a repeated read into one copy - and the repeat is the thing to find.
    """
    path = Path(path).expanduser()
    CACHE.mkdir(parents=True, exist_ok=True)
    key = CACHE / f"{_hash(path)}.json"
    if key.exists():
        return json.loads(key.read_text())["words"]
    if not WHISPER_PYTHON.exists():
        raise RuntimeError(
            f"no Whisper interpreter at {WHISPER_PYTHON}. Set WHISPER_PYTHON to "
            f"a python with mlx-whisper installed (pip install mlx-whisper).")
    # A 16 kHz mono WAV, so Whisper does not have to decode a camera file.
    wav = CACHE / f"{key.stem}.16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vn",
                    "-ac", "1", "-ar", "16000", str(wav)],
                   check=True, capture_output=True)
    print(f"transcribing {path.name} (Whisper, local)...")
    try:
        out = subprocess.run([str(WHISPER_PYTHON), "-c", _WHISPER, str(wav),
                              WHISPER_MODEL],
                             check=True, capture_output=True, text=True)
    finally:
        wav.unlink(missing_ok=True)
    data = json.loads(out.stdout)
    data["source"] = str(path)
    key.write_text(json.dumps(data, indent=1))
    return data["words"]


# ---------------------------------------------------------------------------
# matching the script
# ---------------------------------------------------------------------------

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def number_words(n: int) -> list[str]:
    """587 -> five hundred eighty seven. No "and": it is dropped on both sides."""
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + ([_ONES[n % 10]] if n % 10 else [])
    for size, name in ((10 ** 9, "billion"), (10 ** 6, "million"),
                       (1000, "thousand"), (100, "hundred")):
        if n >= size:
            rest = n % size
            return number_words(n // size) + [name] + (number_words(rest) if rest else [])
    return [str(n)]


def norm(text: str) -> list[str]:
    """Comparable tokens: lower case, no punctuation, hyphens split.

    **Numbers become words, and "and" inside a number goes.** Whisper writes
    "587" where the script may say "five hundred and eighty seven" (or the
    other way round); both sides end up as "five hundred eighty seven".
    Thousands separators and a trailing "%" are handled; years read as
    "twenty twenty six" will not match "2026" and show in the report.
    """
    text = text.lower().replace("’", "'").replace("-", " ")
    text = re.sub(r"(\d),(\d{3})", r"\1\2", text)
    text = text.replace("%", " percent")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    toks = []
    for t in text.split():
        t = t.strip("'")
        if not t:
            continue
        if t.isdigit() and len(t) <= 12:
            toks += number_words(int(t))
        else:
            toks.append(t)
    numeric = set(_ONES + _TENS[2:] + ["hundred", "thousand", "million", "billion"])
    return [t for i, t in enumerate(toks)
            if not (t == "and" and 0 < i < len(toks) - 1
                    and toks[i - 1] in numeric and toks[i + 1] in numeric)]


def _same(a: str, b: str) -> bool:
    return a == b or difflib.SequenceMatcher(None, a, b).ratio() >= MATCH


def _sim(script: list[str], heard: list[str]) -> np.ndarray:
    return np.array([[1.0 if _same(a, b) else 0.0 for b in heard]
                     for a in script], np.float32)


def _ends(S: np.ndarray) -> np.ndarray:
    """Semi-global alignment score of the whole sentence ending at each word.

    Rows are script words, columns transcript words. The sentence must be
    consumed whole; the transcript may start and end anywhere. Match +2,
    mismatch -1, a skipped or an added word -1. The horizontal gap (words
    said that are not in the script) is the running-max trick, so each row is
    one vectorised pass rather than a Python loop over the transcript.
    """
    m, n = S.shape
    idx = np.arange(n + 1, dtype=np.float32)
    prev = np.zeros(n + 1, np.float32)              # row 0: free start
    for i in range(m):
        diag = np.full(n + 1, -1e9, np.float32)
        diag[1:] = prev[:-1] + np.where(S[i] > 0, 2.0, -1.0)
        up = prev - 1.0                             # script word not said
        x = np.maximum(diag, up)
        x[0] = prev[0] - 1.0
        # left: H[j] = max(x[j], H[j-1] - 1) == max_k<=j (x[k] - (j - k))
        cur = np.maximum.accumulate(x + idx) - idx
        prev = cur
    return prev                                     # score of a take ending at j


def _backtrace(script: list[str], heard: list[str], lo: int, hi: int):
    """Exact alignment of one sentence inside heard[lo:hi]: index pairs."""
    sub = heard[lo:hi]
    sm = difflib.SequenceMatcher(None, script, sub, autojunk=False)
    pairs = {}
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            pairs[a + k] = lo + b + k
    # Fuzzy matches the exact matcher missed (a misheard plural, a number).
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "replace":
            for k in range(min(a1 - a0, b1 - b0)):
                if _same(script[a0 + k], sub[b0 + k]):
                    pairs[a0 + k] = lo + b0 + k
    return pairs


def _trim(pairs: dict, slack: int = 3) -> dict:
    """Drop matches stranded away from the take's main run.

    The search window is wider than the sentence, so a common word ("the",
    "it") at the window's edge can match a word of the sentence before -
    and a take that starts inside its neighbour breaks the order the
    takes are chosen in.
    """
    if len(pairs) < 2:
        return pairs
    items = sorted(pairs.items(), key=lambda kv: kv[1])
    # Split into runs wherever more words were said than the script skips
    # (plus `slack` for an ad-lib); keep the run with the most matches. A
    # false start ("I let AI read five hundred... sorry") is its own run.
    runs, cur = [], [items[0]]
    for prev, it in zip(items, items[1:]):
        if it[1] - prev[1] > slack + max(1, it[0] - prev[0]):
            runs.append(cur)
            cur = []
        cur.append(it)
    runs.append(cur)
    return dict(max(runs, key=len))


@dataclass
class Take:
    sentence: int
    first: int                    # transcript word index, inclusive
    last: int                     # inclusive
    score: float                  # share of the sentence's words matched
    pairs: dict                   # script word index -> transcript word index
    others: int                   # how many other takes were found and dropped


def align(sentences: list[list[str]], words: list[dict],
          window: tuple[float, float] | None = None) -> list[Take]:
    """One take per sentence, in order, preferring the last good one."""
    heard = [norm(w["w"]) for w in words]
    # A Whisper "word" can be two tokens ("thirty-day"); flatten, keeping the
    # word each token came from.
    flat, owner = [], []
    for i, toks in enumerate(heard):
        if window and not (window[0] <= words[i]["s"] <= window[1]):
            continue
        for t in toks:
            flat.append(t)
            owner.append(i)
    n = len(flat)
    if not n:
        raise ValueError("the recording has no words in it (or in `window`)")

    cands: list[list[tuple[int, int, float, dict]]] = []
    for si, sent in enumerate(sentences):
        m = len(sent)
        end = _ends(_sim(sent, flat))[1:]           # end[j]: take ends at j
        best = 2.0 * m
        found = []
        # Peaks, best first, suppressing the neighbourhood of each.
        order = np.argsort(-end)
        taken = np.zeros(n, bool)
        for j in order:
            if end[j] < best * MIN_SCORE * 0.5 or len(found) >= 6:
                break
            if taken[j]:
                continue
            lo, hi = max(0, j - 2 * m - 4), j + 1
            pairs = _trim(_backtrace(sent, flat, lo, hi))
            if not pairs:
                continue
            score = len(pairs) / m
            if score < MIN_SCORE:
                taken[max(0, j - m // 2):j + m // 2 + 1] = True
                continue
            a, b = min(pairs.values()), max(pairs.values())
            found.append((a, b, score, pairs))
            taken[max(0, a - 1):b + 2] = True
        cands.append(found)

    missing = [i for i, c in enumerate(cands) if not c]
    if missing:
        lines = "\n".join(f"  {i + 1}. {' '.join(sentences[i])}" for i in missing)
        raise ValueError(f"not found in the recording - re-record these, or "
                         f"change the script to what was said:\n{lines}")

    # Choose one candidate per sentence, monotonic in time, maximising score
    # plus a bonus for being a later take (the retake rule). The bonus is by
    # rank, not by seconds: a re-read two seconds after the first is still
    # the one meant, and Whisper cannot hear the intonation that made the
    # editor read it again. Only a nearly complete take earns it, so a
    # false start after a full read never wins.
    for cs in cands:
        cs.sort(key=lambda c: c[0])
    INF = -1e9
    best: list[list[float]] = []
    back: list[list[int]] = []
    for si, cs in enumerate(cands):
        row, brow = [], []
        for r, (a, b, score, _) in enumerate(cs):
            rank = r / (len(cs) - 1) if len(cs) > 1 else 1.0
            gain = score + (LATER * rank if score >= GOOD else 0.0)
            if si == 0:
                row.append(gain)
                brow.append(-1)
                continue
            top, arg = INF, -1
            for k, (pa, pb, _, _) in enumerate(cands[si - 1]):
                if pb < a and best[si - 1][k] > top:
                    top, arg = best[si - 1][k], k
            row.append(top + gain if arg >= 0 else INF)
            brow.append(arg)
        best.append(row)
        back.append(brow)
    k = int(np.argmax(best[-1]))
    if best[-1][k] <= INF / 2:
        raise ValueError("the takes found are not in script order - is the "
                         "right recording paired with this script?")
    chosen = []
    for si in range(len(cands) - 1, -1, -1):
        chosen.append(k)
        k = back[si][k]
    chosen.reverse()

    takes = []
    for si, (cs, k) in enumerate(zip(cands, chosen)):
        a, b, score, pairs = cs[k]
        # Retakes worth mentioning: other nearly complete reads of it.
        others = sum(1 for j, c in enumerate(cs) if j != k and c[2] >= GOOD)
        takes.append(Take(si, owner[a], owner[b], score,
                          {s: owner[t] for s, t in pairs.items()}, others))
    return takes


# ---------------------------------------------------------------------------
# cutting
# ---------------------------------------------------------------------------

def _quietest(audio: np.ndarray, a: float, b: float, sr: int = SR) -> float:
    """The quietest 10 ms point between a and b, in seconds."""
    i0, i1 = int(a * sr), int(b * sr)
    if i1 - i0 < int(0.02 * sr):
        return (a + b) / 2
    hop = int(0.005 * sr)
    seg = audio[i0:i1]
    win = int(0.010 * sr)
    e = np.array([np.sqrt(np.mean(seg[k:k + win] ** 2) + 1e-12)
                  for k in range(0, max(1, len(seg) - win), hop)])
    return a + (int(np.argmin(e)) * hop + win / 2) / sr


def room_tone(audio: np.ndarray, seconds: float = 0.6, sr: int = SR) -> np.ndarray:
    """The quietest stretch of the recording: its own silence, to fill gaps."""
    win = int(seconds * sr)
    if len(audio) <= win:
        return np.zeros(win, np.float32)
    hop = int(0.05 * sr)
    rms = [np.sqrt(np.mean(audio[k:k + win] ** 2))
           for k in range(0, len(audio) - win, hop)]
    k = int(np.argmin(rms)) * hop
    return audio[k:k + win].copy()


def _tone(tone: np.ndarray, n: int) -> np.ndarray:
    if n <= 0:
        return np.zeros(0, np.float32)
    reps = int(np.ceil(n / len(tone)))
    out = np.tile(tone, reps)[:n].copy()
    f = min(len(out) // 2, int(FADE * SR))
    if f:
        ramp = np.linspace(0, 1, f, dtype=np.float32)
        out[:f] *= ramp
        out[-f:] *= ramp[::-1]
    return out


def _fade(x: np.ndarray) -> np.ndarray:
    f = min(len(x) // 2, int(FADE * SR))
    if f:
        ramp = np.linspace(0, 1, f, dtype=np.float32)
        x[:f] *= ramp
        x[-f:] *= ramp[::-1]
    return x


def _bounds(takes: list[Take], words: list[dict], audio: np.ndarray,
            gaps: list[float], max_pause: float):
    """Source (start, end) per sentence and whether it joins its neighbour."""
    total = len(audio) / SR
    spans, joined = [], []
    for i, tk in enumerate(takes):
        s, e = words[tk.first]["s"], words[tk.last]["e"]
        before = words[tk.first - 1]["e"] if tk.first > 0 else 0.0
        after = words[tk.last + 1]["s"] if tk.last + 1 < len(words) else total
        a = max(before, s - PRE)
        b = min(after, e + POST)
        a = _quietest(audio, a, s) if s - a > 0.03 else a
        spans.append([max(0.0, a), min(total, b)])
        # Same take, nothing cut between: keep the real pause.
        joined.append(i > 0 and takes[i - 1].last + 1 == tk.first)
    for i in range(1, len(spans)):
        if not joined[i]:
            continue
        pause = spans[i][0] - spans[i - 1][1]
        if pause <= 0:
            mid = (spans[i - 1][1] + spans[i][0]) / 2
            spans[i - 1][1] = spans[i][0] = mid
            continue
        keep = min(pause, max(max_pause, gaps[i - 1]))
        if keep < pause:                 # trim the middle of a long pause
            spans[i - 1][1] += keep / 2
            spans[i][0] -= keep / 2
        else:                            # the whole pause stays
            spans[i - 1][1] = spans[i][0]
    return spans, joined


def _assemble(audio, spans, joined, gaps, tail):
    tone = room_tone(audio)
    out, edl, t = [], [], 0.0
    for i, (a, b) in enumerate(spans):
        if i > 0 and not joined[i]:
            g = _tone(tone, int(gaps[i - 1] * SR))
            out.append(g)
            edl.append({"out": round(t, 4), "dur": round(len(g) / SR, 4),
                        "gap": True})
            t += len(g) / SR
        piece = _fade(audio[int(a * SR):int(b * SR)].copy())
        out.append(piece)
        edl.append({"out": round(t, 4), "dur": round(len(piece) / SR, 4),
                    "src": round(a, 4)})
        t += len(piece) / SR
    tl = _tone(tone, int(tail * SR))
    out.append(tl)
    edl.append({"out": round(t, 4), "dur": round(len(tl) / SR, 4), "gap": True})
    return np.concatenate(out), edl


def src_to_out(edl: list[dict], src: float) -> float | None:
    """Where a source second landed in the output, or None if it was cut."""
    for seg in edl:
        if seg.get("gap"):
            continue
        if seg["src"] <= src <= seg["src"] + seg["dur"]:
            return seg["out"] + (src - seg["src"])
    return None


# ---------------------------------------------------------------------------
# the entry point the engine calls
# ---------------------------------------------------------------------------

def _spoken(chunk) -> tuple[str, str]:
    return (chunk, chunk) if isinstance(chunk, str) else (chunk[0], chunk[1])


def build_narration_recorded(sentences, workdir: Path, rec: Recording,
                             gap=0.55, tail: float = 1.2):
    """`build_narration_aligned`'s contract, from a recording.

    Returns `(track, captions, total)`. Captions are the script's chunks,
    timed by the words of the take that was kept.
    """
    import soundfile as sf
    from .voiceover import Caption

    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    gaps = ([float(gap)] * len(sentences) if isinstance(gap, (int, float))
            else [float(g) for g in gap])

    # Script words per sentence, and which chunk each word belongs to.
    sent_words, word_chunk = [], []
    for sent in sentences:
        toks, owner = [], []
        for ci, chunk in enumerate(sent):
            for t in norm(_spoken(chunk)[1]):
                toks.append(t)
                owner.append(ci)
        sent_words.append(toks)
        word_chunk.append(owner)

    words = transcribe(rec.audio)
    takes = align(sent_words, words, rec.window)
    audio = load_audio(rec.audio)
    spans, joined = _bounds(takes, words, audio, gaps, rec.max_pause)
    voice, edl = _assemble(audio, spans, joined, gaps, tail)

    raw = workdir / "recorded.raw.wav"
    track = workdir / "narration.wav"
    sf.write(str(raw), voice, SR)
    chain = ["-af", CLEAN] if rec.clean else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), *chain,
                    "-ar", str(SR), "-ac", "2", str(track)],
                   check=True, capture_output=True)
    raw.unlink(missing_ok=True)
    total = len(voice) / SR

    # Captions: each chunk runs from its first heard word to its last.
    captions = []
    for si, (sent, tk) in enumerate(zip(sentences, takes)):
        a_out = src_to_out(edl, spans[si][0]) or 0.0
        b_out = src_to_out(edl, spans[si][1] - 1e-4) or a_out
        times: dict[int, list[float]] = {}
        for wi, ci in enumerate(word_chunk[si]):
            ti = tk.pairs.get(wi)
            if ti is None:
                continue
            s = src_to_out(edl, words[ti]["s"])
            e = src_to_out(edl, words[ti]["e"])
            if s is None or e is None:
                continue
            times.setdefault(ci, []).extend([s, e])
        n = len(sent)
        starts, ends = [], []
        for ci in range(n):
            if ci in times:
                starts.append(min(times[ci]))
                ends.append(max(times[ci]))
            else:                        # a chunk none of whose words matched
                starts.append(None)
                ends.append(None)
        # Fill the unmatched ones by spreading them over the gap they sit in.
        for ci in range(n):
            if starts[ci] is None:
                lo = ends[ci - 1] if ci > 0 and ends[ci - 1] is not None else a_out
                hi_i = next((k for k in range(ci + 1, n) if starts[k] is not None), None)
                hi = starts[hi_i] if hi_i is not None else b_out
                k = (hi_i if hi_i is not None else n) - ci
                step = max(hi - lo, 0.0) / max(k, 1)
                starts[ci], ends[ci] = lo, lo + step
        for ci, chunk in enumerate(sent):
            cap = _spoken(chunk)[0]
            s = max(starts[ci], captions[-1].end if captions else 0.0)
            captions.append(Caption(cap, s, max(ends[ci], s + 0.05)))
    # Hold each caption until the next one, as the synthesised path does;
    # `speech_end` (set at construction) keeps where the voice stopped.
    for a, b in zip(captions, captions[1:]):
        a.end = max(a.end, b.start)
    if captions:
        captions[-1].end += tail

    _write_sidecars(rec, sentences, sent_words, takes, words, edl, spans)
    rec.captions = captions
    return track, captions, total


def _stem(rec: Recording, sentences) -> Path:
    h = hashlib.sha1(json.dumps(
        [[_spoken(c)[1] for c in s] for s in sentences]).encode()).hexdigest()[:8]
    return rec.audio.with_name(f"{rec.audio.stem}.{h}")


def sidecar(rec: Recording, sentences, kind: str) -> Path:
    """`NAME.<script hash>.edl.json` / `.report.txt` next to the recording."""
    stem = _stem(rec, sentences)
    return stem.with_name(f"{stem.name}.{kind}")


def _write_sidecars(rec, sentences, sent_words, takes, words, edl, spans):
    edl_path = sidecar(rec, sentences, "edl.json")
    rec.edl = edl_path
    edl_path.write_text(json.dumps({
        "audio": str(rec.audio),
        "face": str(rec.face) if rec.face else None,
        "segments": edl,
    }, indent=1))

    lines = [f"Recording: {rec.audio.name}", ""]
    kept = 0.0
    flags = 0
    for si, (tk, toks) in enumerate(zip(takes, sent_words)):
        heard = [t for w in words[tk.first:tk.last + 1] for t in norm(w["w"])]
        sm = difflib.SequenceMatcher(None, toks, heard, autojunk=False)
        notes = []
        for op, a0, a1, b0, b1 in sm.get_opcodes():
            if op == "equal":
                continue
            s_txt, h_txt = " ".join(toks[a0:a1]), " ".join(heard[b0:b1])
            if op == "replace" and all(_same(x, y) for x, y in
                                       zip(toks[a0:a1], heard[b0:b1])) \
                    and a1 - a0 == b1 - b0:
                continue
            if op == "delete":
                notes.append(f"not said: \"{s_txt}\"")
            elif op == "insert":
                notes.append(f"added: \"{h_txt}\"")
            else:
                notes.append(f"said \"{h_txt}\" for \"{s_txt}\"")
        a, b = spans[si]
        kept += b - a
        mark = "!" if notes else " "
        flags += bool(notes)
        retake = f", {tk.others} other take(s) cut" if tk.others else ""
        lines.append(f"{mark} {si + 1:>3}. [{a:7.2f}-{b:7.2f}s, "
                     f"{tk.score:.0%} matched{retake}] {' '.join(toks)}")
        for nline in notes:
            lines.append(f"        {nline}")
    src_total = words[-1]["e"] if words else 0.0
    lines += ["", f"{len(takes)} sentences, {flags} with differences. "
                  f"Kept {kept:.1f}s of {src_total:.1f}s recorded."]
    report = sidecar(rec, sentences, "report.txt")
    rec.report = report
    report.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-1:]) + f"  Report: {report}")
