"""Voice examples for OktAI: the same lines read the way the channels' AI
voice first sounded, and the way it sounds today (2026-11-21).

Both are the same Kokoro voice (`af_heart`, the `mia` profile's), so the
difference a viewer hears is only what we changed - the two causes the
docs measured (`docs/video/voice.md`, "Sentences are synthesised in runs";
`audio-book-automation/docs/voice.md`, "Robotic usually means too slow"):

* `robotic` - slowed down, every sentence synthesised alone (a cold start,
  high in the voice's range), hard-trimmed and joined with digital silence,
  no post chain.
* `today` - the `mia` profile as the videos use it: its own speed and
  chain, the sentences spoken as one run.

`wpm(path, text)` measures what a viewer hears, so a script cites the real
pace of the clip it plays, not the setting.
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

import numpy as np

SR = 48000


def robotic(lines: list[str], out: Path, speed: float = 0.72,
            gap: float = 0.55) -> Path:
    import librosa
    import soundfile as sf
    from ..core.voiceover import _kokoro, say_as_word, voice_style
    out = Path(out)
    parts = []
    for line in lines:
        audio, sr = _kokoro().create(say_as_word(line), voice=voice_style("af_heart"),
                                     speed=speed, lang="en-us")
        audio, _ = librosa.effects.trim(np.asarray(audio, np.float32), top_db=35)
        if sr != SR:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=SR)
        parts += [audio, np.zeros(int(gap * SR), np.float32)]
    sf.write(str(out), np.concatenate(parts[:-1]), SR)
    return out


def today(lines: list[str], out: Path, profile: str = "mia") -> Path:
    import shutil
    from ..core.voiceover import build_narration_aligned, profile_args
    out = Path(out)
    with tempfile.TemporaryDirectory() as tmp:
        track, _, _ = build_narration_aligned([[ln] for ln in lines], Path(tmp),
                                              gap=0.35, tail=0.0,
                                              **profile_args(profile))
        shutil.copy(track, out)
    return out


def wpm(path: Path, text: str) -> float:
    """Words a minute over the clip's speech (its silence at the ends cut)."""
    import librosa
    y, sr = librosa.load(str(path), sr=None)
    y, _ = librosa.effects.trim(y, top_db=35)
    words = len(re.findall(r"[A-Za-z0-9']+", text))
    return words / (len(y) / sr) * 60


def make(folder: Path, lines: list[str]) -> dict[str, Path]:
    """Both clips in `folder`, made once (delete them to remake)."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    made = {}
    for name, fn in (("robotic", robotic), ("today", today)):
        p = folder / f"voice-{name}.wav"
        if not p.exists():
            fn(lines, p)
        made[name] = p
    return made
