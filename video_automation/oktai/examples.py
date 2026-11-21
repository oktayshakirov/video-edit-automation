"""Sound examples for OktAI videos - voices and music beds played on screen,
made from our own engines so every difference is one we can name.

**Voices** (2026-11-21, the editor's notes on the opener draft):

* `oldest` - macOS's built-in `say` voice (Daniel), the engine our code still
  keeps as its "legacy, last resort" backend, read sentence by sentence and
  joined with dead silence. The editor asked for the opener's first voice to
  be *intentionally* worse than the Kokoro reconstruction - "like the first
  test", which was this voice at 175 words a minute - "just slightly more
  understandable": so 160.
* `one_at_a_time` - the explainer voice (`noah`), every sentence synthesised
  alone and joined with digital silence: the fault `docs/video/voice.md`
  measured ("Sentences are synthesised in runs") at the approved speed.
* `today` - `noah` as the explainers use it: one run, its own chain.
* `phrase` - one line in `noah`, for "Money." against a full sentence.

**Music**: `bed(preset)` renders a generated bed (`calm` is pads alone - the
"creepy mysterious" sound `docs/video/audio.md` describes); `track(name)`
cuts a stretch of a prepared track. Retired presets cannot be rendered and
are never played as examples either (`music.RETIRED`).

`make(folder, recipes)` renders each once, keyed by its recipe, so changing a
line or a voice remakes that clip and nothing else. `wpm` measures what a
viewer hears.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np

SR = 48000
VOICE = "noah"                 # the male explainer voice (`core/voices.py`)


def _trim(audio: np.ndarray, sr: int) -> np.ndarray:
    import librosa
    audio, _ = librosa.effects.trim(np.asarray(audio, np.float32), top_db=35)
    if sr != SR:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=SR)
    return audio


def _join(parts: list[np.ndarray], gap: float) -> np.ndarray:
    out = []
    for p in parts:
        out += [p, np.zeros(int(gap * SR), np.float32)]
    return np.concatenate(out[:-1])


def oldest(lines: list[str], out: Path, voice: str = "Daniel", rate: int = 160,
           gap: float = 0.6) -> Path:
    import soundfile as sf
    parts = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, line in enumerate(lines):
            aiff = Path(tmp) / f"{i}.aiff"
            subprocess.run(["say", "-v", voice, "-r", str(rate), "-o", str(aiff), line],
                           check=True)
            a, sr = sf.read(str(aiff), dtype="float32", always_2d=True)
            parts.append(_trim(a.mean(axis=1), sr))
    sf.write(str(out), _join(parts, gap), SR)
    return Path(out)


def one_at_a_time(lines: list[str], out: Path, profile: str = VOICE,
                  gap: float = 0.6) -> Path:
    import soundfile as sf
    from ..core.voiceover import profile_args, synth_phrase
    parts = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, line in enumerate(lines):
            wav = Path(tmp) / f"{i}.wav"
            synth_phrase(line, wav, **profile_args(profile))
            a, sr = sf.read(str(wav), dtype="float32", always_2d=True)
            parts.append(_trim(a.mean(axis=1), sr))
    sf.write(str(out), _join(parts, gap), SR)
    return Path(out)


def today(lines: list[str], out: Path, profile: str = VOICE) -> Path:
    import shutil
    from ..core.voiceover import build_narration_aligned, profile_args
    with tempfile.TemporaryDirectory() as tmp:
        track, _, _ = build_narration_aligned([[ln] for ln in lines], Path(tmp),
                                              gap=0.35, tail=0.0,
                                              **profile_args(profile))
        shutil.copy(track, out)
    return Path(out)


def phrase(text: str, out: Path, profile: str = VOICE) -> Path:
    return today([text], out, profile)


def bed(preset: str, out: Path, seconds: float = 7.0) -> Path:
    import soundfile as sf
    from ..core import music
    x = music.render(seconds, preset)
    n = int(0.4 * music.SR)
    env = np.ones(len(x))
    env[:n] = np.linspace(0, 1, n)
    env[-n:] = np.linspace(1, 0, n)
    sf.write(str(out), (x * env[:, None]).astype(np.float32), music.SR)
    return Path(out)


def track(name: str, out: Path, start: float = 0.0, seconds: float = 7.0) -> Path:
    """`seconds` of a prepared track; a short loop (night-drift is 7.7 s)
    plays round, the way the bed does under a video."""
    from ..core import music
    src = music.track(name)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1",
                    "-ss", str(start), "-t", str(seconds), "-i", str(src), "-af", f"afade=t=in:d=0.4,afade=t=out:st={seconds - 0.4}:d=0.4",
                    "-ar", str(SR), str(out)], check=True)
    return Path(out)


MAKERS = {"oldest": oldest, "one_at_a_time": one_at_a_time, "today": today,
          "phrase": phrase, "bed": bed, "track": track}


def make(folder: Path, recipes: dict[str, tuple]) -> dict[str, Path]:
    """`{name: (maker, first_arg, {kwargs})}` -> `{name: wav}`, each made once
    per recipe (the recipe's hash is in the file name)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    made = {}
    for name, (maker, arg, *kw) in recipes.items():
        kw = kw[0] if kw else {}
        key = hashlib.sha1(json.dumps([maker, arg, kw], sort_keys=True).encode()
                           ).hexdigest()[:8]
        p = folder / f"{name}-{key}.wav"
        if not p.exists():
            MAKERS[maker](arg, p, **kw)
        made[name] = p
    return made


def wpm(path: Path, text: str) -> float:
    """Words a minute over the clip's speech (its silence at the ends cut)."""
    import librosa
    y, sr = librosa.load(str(path), sr=None)
    y, _ = librosa.effects.trim(y, top_db=35)
    words = len(re.findall(r"[A-Za-z0-9']+", text))
    return words / (len(y) / sr) * 60
