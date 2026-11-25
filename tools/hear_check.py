"""Listen to a built video: transcribe it and diff it against its own SRT.

    PYTHONPATH=. .venv/bin/python tools/hear_check.py VIDEO.mp4 [VIDEO.srt]

Prints each difference at its output time: script words not heard (-) and
words heard that the script lacks (+). A played sound example shows as +,
and so does Whisper inventing words over music. Anything else is a cut to
check: transcribe that line alone (and the raw take) before calling it a
fault - out of context Whisper hears "code" as "Colt" and "same" as "sim"
(the OktAI opener, 2026-11-24/25).
"""
import difflib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from video_automation.core.recorded import norm, transcribe

video = Path(sys.argv[1])
srt = Path(sys.argv[2]) if len(sys.argv) > 2 else video.with_suffix(".srt")
cues = []
for block in srt.read_text().strip().split("\n\n"):
    lines = block.strip().splitlines()
    if len(lines) < 3:
        continue
    t = lines[1].split(" --> ")[0]
    h, m, s = t.replace(",", ".").split(":")
    cues.append((int(h) * 3600 + int(m) * 60 + float(s), " ".join(lines[2:])))
script = []
for t, text in cues:
    for w in norm(text):
        script.append((t, w))

with tempfile.TemporaryDirectory() as d:
    wav = Path(d) / f"{video.stem}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vn", "-ac", "1",
                    "-ar", "16000", str(wav)], check=True)
    heard = []
    for w in transcribe(wav):
        for tok in norm(w["w"]):
            heard.append((w["s"], tok))

a = [w for _, w in script]
b = [w for _, w in heard]
sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
n = 0
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == "equal":
        continue
    t = heard[j1][0] if j1 < len(heard) else script[i1][0]
    miss = " ".join(a[i1:i2])
    extra = " ".join(b[j1:j2])
    n += 1
    print(f"{t:7.1f}  " + (f"-[{miss}] " if miss else "") + (f"+[{extra}]" if extra else ""))
print(f"{video.name}: {len(a)} script words, {len(b)} heard, ratio {sm.ratio():.3f}, {n} diffs")
