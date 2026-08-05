"""Narrated shorts — spoken quote with captions synced to it.

Sync approach: **speak each caption phrase separately and measure it.**

The obvious alternative is to speak the whole line, then recover word timings
with a forced aligner or Whisper. That works but drags in a model download and
can drift. Speaking phrase by phrase makes the timing exact by construction —
each caption is shown for precisely as long as its own audio runs — and the
small pauses it creates between phrases suit motivational delivery, which is
already pausey, rather than fighting it.

The TTS backend is isolated in `synth_phrase`. Three are wired up, in order of
quality: kokoro (local, unlimited, default), edge (Microsoft neural voices over
the network, free, no key), say (macOS, legacy, last resort). A hosted API drops
in at the same seam. Because caption timing comes from *measured* audio duration
rather than a prediction, changing engine cannot desynchronise the captions.
"""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .vertical import OUT_H, OUT_W, render_short, render_text_png, sample_bg_luma

TTS_BACKEND = "kokoro"                      # "kokoro" | "edge" | "say"

# Kokoro-82M, Apache 2.0, fully local and unlimited. Installed as kokoro-onnx
# rather than the PyTorch package: the latter pulls spacy, which has no Python
# 3.13 wheels and fails to build, and ~2.5GB of torch besides. The ONNX build
# reuses the onnxruntime already present and totals ~350MB.
KOKORO_DIR = Path.home() / ".local/share/kokoro"
KOKORO_VOICE = "am_michael"
KOKORO_SPEED = 0.88     # unhurried; motivational reads are not brisk

# Kokoro has no emotion parameter, so mood is carried by pace and voice choice.
# Stated plainly because it is a real limit, not a tuned feature.
KOKORO_MOODS = {
    "reflective": 0.84,
    "motivational": 0.95,
    "sad": 0.80,
    "neutral": 0.90,
}

# Microsoft's current neural voices, reached through the Edge endpoint: free,
# no API key, ~1MB install, and clearly the most natural of the three. The
# "Multilingual" variants are the newest generation and the ones worth using.
# Trade-off: it is a network call and heavy use can be rate-limited, so it is
# the fallback rather than the default now that Kokoro runs locally.
EDGE_VOICE = "en-US-AndrewMultilingualNeural"
# Delivery per mood. The free Edge endpoint ignores SSML express-as styles, so
# tone is shaped with the levers it does honour — rate and pitch — plus voice
# choice, which does more for mood than either.
EDGE_MOODS = {
    "reflective": {"rate": "-14%", "pitch": "-3Hz"},
    "motivational": {"rate": "-6%", "pitch": "+2Hz"},
    "sad": {"rate": "-18%", "pitch": "-6Hz"},
    "neutral": {"rate": "-10%", "pitch": "+0Hz"},
}

DEFAULT_VOICE = "Samantha"                  # only used by the `say` backend
GAP = 0.18          # seconds of silence between phrases
TAIL = 1.0          # hold the last caption this long after the audio ends


_KOKORO = None


def _kokoro():
    """Load the model once — it is ~325MB and the load dominates a short script."""
    global _KOKORO
    if _KOKORO is None:
        from kokoro_onnx import Kokoro
        _KOKORO = Kokoro(str(KOKORO_DIR / "kokoro-v1.0.onnx"),
                         str(KOKORO_DIR / "voices-v1.0.bin"))
    return _KOKORO


@dataclass
class Caption:
    text: str
    start: float
    end: float


def split_phrases(text: str, max_words: int = 6, min_words: int = 3) -> list[str]:
    """Break a quote into caption-sized phrases.

    Punctuation wins over word count — a phrase ending where the sentence
    breathes reads and speaks better than one chopped at an arbitrary sixth
    word. But splitting on every comma throws up two-word fragments that flash
    past before they can be read ("lost here," measured 0.65s), so anything
    under `min_words` is merged forward into its neighbour.
    """
    parts = [p.strip() for p in re.split(r"(?<=[.,;:!?])\s+", text) if p.strip()]

    merged: list[str] = []
    for part in parts:
        if merged and len(part.split()) < min_words:
            merged[-1] = f"{merged[-1]} {part}"
        elif merged and len(merged[-1].split()) < min_words:
            merged[-1] = f"{merged[-1]} {part}"
        else:
            merged.append(part)

    out: list[str] = []
    for part in merged:
        words = part.split()
        while len(words) > max_words:
            out.append(" ".join(words[:max_words]))
            words = words[max_words:]
        if words:
            # Avoid leaving a runt at the end of a long part.
            if out and len(words) < min_words:
                out[-1] = f"{out[-1]} {' '.join(words)}"
            else:
                out.append(" ".join(words))
    return out


def synth_phrase(text: str, out: Path, voice: str | None = None,
                 rate: int = 165, backend: str = TTS_BACKEND,
                 mood: str = "reflective") -> float:
    """Render one phrase to audio and return its measured duration.

    The only place a TTS engine is named. Everything downstream works off the
    measured duration, so swapping engines — or moving to a hosted API — cannot
    desynchronise the captions.
    """
    raw = out.with_suffix(".raw.wav")

    if backend == "kokoro":
        import soundfile as sf
        audio, sr = _kokoro().create(
            text, voice=voice or KOKORO_VOICE,
            speed=KOKORO_MOODS.get(mood, KOKORO_SPEED), lang="en-us")
        sf.write(str(raw), audio, sr)
    elif backend == "edge":
        mood_args = EDGE_MOODS.get(mood, EDGE_MOODS["neutral"])
        raw = out.with_suffix(".raw.mp3")
        subprocess.run(
            [sys.executable, "-m", "edge_tts", "--voice", voice or EDGE_VOICE,
             f"--rate={mood_args['rate']}", f"--pitch={mood_args['pitch']}",
             "--text", text, "--write-media", str(raw)],
            check=True, capture_output=True)
    else:
        aiff = out.with_suffix(".aiff")
        subprocess.run(["say", "-v", voice or DEFAULT_VOICE, "-r", str(rate),
                        "-o", str(aiff), text], check=True, capture_output=True)
        raw = aiff

    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw),
                    "-ar", "48000", "-ac", "2", str(out)],
                   check=True, capture_output=True)
    raw.unlink(missing_ok=True)

    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(out)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(dur)


def build_narration(text: str, workdir: Path, voice: str | None = None,
                    rate: int = 165, backend: str = TTS_BACKEND,
                    mood: str = "reflective") -> tuple[Path, list[Caption], float]:
    """Speak the quote phrase by phrase; return the mixed track and caption times."""
    workdir.mkdir(parents=True, exist_ok=True)
    phrases = split_phrases(text)

    captions: list[Caption] = []
    pieces: list[Path] = []
    t = 0.0
    for i, ph in enumerate(phrases):
        wav = workdir / f"ph{i:02d}.wav"
        dur = synth_phrase(ph, wav, voice, rate, backend, mood)
        captions.append(Caption(ph, t, t + dur + GAP))
        pieces.append(wav)
        t += dur + GAP

    # Concatenate with the gaps baked in, so audio and captions cannot drift.
    listing = workdir / "concat.txt"
    silence = workdir / "gap.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    f"anullsrc=r=48000:cl=stereo:d={GAP}", str(silence)],
                   check=True, capture_output=True)
    lines = []
    for p in pieces:
        lines.append(f"file '{p.name}'")
        lines.append(f"file '{silence.name}'")
    listing.write_text("\n".join(lines), encoding="utf-8")

    track = workdir / "narration.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", str(track)],
                   check=True, capture_output=True, cwd=workdir)
    if captions:
        captions[-1].end += TAIL
    return track, captions, t + TAIL


def render_narrated(src: Path, out: Path, start: float,
                    box: tuple[int, int, int, int], text: str,
                    workdir: Path, voice: str | None = None,
                    rate: int = 165, font_size: int = 46,
                    backend: str = TTS_BACKEND, mood: str = "reflective") -> tuple[Path, float]:
    """Cut, crop, burn synced captions, and lay the narration underneath.

    Video length follows the narration rather than a fixed target — a caption
    cut off mid-sentence is worse than a clip a second longer than planned.
    """
    track, captions, total = build_narration(text, workdir, voice, rate, backend, mood)
    luma = sample_bg_luma(src, box, start + total / 2)

    pngs = []
    for i, c in enumerate(captions):
        p = workdir / f"cap{i:02d}.png"
        render_text_png(c.text, p, size=font_size, bg_luma=luma)
        pngs.append(p)

    x, y, w, h = box
    chain = [f"[0:v]crop={w}:{h}:{x}:{y},scale={OUT_W}:{OUT_H}:flags=lanczos[v0]"]
    for i, c in enumerate(captions):
        src_lbl, dst_lbl = f"[v{i}]", f"[v{i+1}]"
        chain.append(
            f"{src_lbl}[{i+1}:v]overlay=0:0:enable='between(t,{c.start:.3f},{c.end:.3f})'{dst_lbl}"
        )
    last = f"[v{len(captions)}]"
    chain.append(f"{last}fade=t=out:st={max(total-0.5,0):.2f}:d=0.5[vout]")

    cmd = ["ffmpeg", "-v", "error", "-y",
           "-ss", f"{start}", "-t", f"{total:.3f}", "-i", str(src)]
    for p in pngs:
        cmd += ["-i", str(p)]
    cmd += ["-i", str(track),
            "-filter_complex", ";".join(chain),
            "-map", "[vout]", "-map", f"{len(pngs)+1}:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out, total
