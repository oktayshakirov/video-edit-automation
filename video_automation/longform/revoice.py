"""Re-speak one sentence of a finished long form, and keep its picture.

**Built 2026-11-20 for `tinnitus-treatments-ranked`**, where Kokoro read
"ginkgo" with a soft J (espeak: `dʒˈɪŋkɡoʊ`) and the editor asked for a fix
without re-rendering the whole video. A respelling in the script changes the
narration's cache key, so the whole read is synthesised again, every
sentence lands a little earlier or later, and the picture has to be cut
again - twenty minutes for one word.

This keeps the cached narration and changes only the sentence that is
wrong: it is synthesised alone with the respelling, its silence trimmed,
fitted by `atempo` to the exact length of the original sentence's speech,
and written over it with short fades. Every caption, cue and shot keeps its
time, so the old render's picture is copied, not re-encoded, and only the
sound is mixed again (`render_long(revoice=, reuse_picture=)`).

The cost is prosody: the sentence is a cold start rather than part of its
run (`voiceover.build_narration_aligned`). Fine for one line; a respelling
that changes a sentence's length by more than `MAX_STRETCH` is refused,
because stretching past it is audible.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import numpy as np

MAX_STRETCH = 0.12           # the most `atempo` may change the new read's speed
FADE = 0.012                 # seconds, each side of the seam
LEVEL = 0.01                 # what counts as voiced, on the peak-normalised read


def _voiced(a: np.ndarray, sr: int, lo: int, hi: int) -> tuple[int, int]:
    """First and last voiced sample of `a[lo:hi]` (absolute indices)."""
    seg = np.abs(a[lo:hi]).max(axis=1)
    peak = seg.max() or 1.0
    on = np.nonzero(seg > peak * LEVEL)[0]
    if not len(on):
        raise ValueError("revoice: no voice found in the sentence's span")
    return lo + int(on[0]), lo + int(on[-1]) + 1


def _run(captions, said: str) -> list:
    """The consecutive captions that read `said`, word for word."""
    want = said.split()
    for i in range(len(captions)):
        got, j = [], i
        while j < len(captions) and len(got) < len(want):
            got += captions[j].text.split()
            j += 1
        if got == want:
            return captions[i:j]
    raise ValueError(f"revoice: no run of captions reads {said!r}")


def patch_track(track: Path, captions, revoice: dict, workdir: Path,
                voice: str) -> Path:
    import soundfile as sf
    from ..core.voiceover import profile_args, synth_phrase
    audio, sr = sf.read(str(track), always_2d=True)
    for k, (said, spoken) in enumerate(revoice.items()):
        run = _run(captions, said)
        t0 = run[0].start
        t1 = max((c.speech_end or c.end) for c in run)
        a0, a1 = _voiced(audio, sr, max(0, int((t0 - 0.15) * sr)),
                         min(len(audio), int((t1 + 0.15) * sr)))
        raw = workdir / f"revoice-{k}.wav"
        synth_phrase(spoken, raw, **profile_args(voice))
        new, nsr = sf.read(str(raw), always_2d=True)
        if nsr != sr:
            raise ValueError(f"revoice: {nsr} Hz against the track's {sr} Hz")
        b0, b1 = _voiced(new, sr, 0, len(new))
        ratio = (b1 - b0) / (a1 - a0)
        if abs(ratio - 1) > MAX_STRETCH:
            raise ValueError(
                f"revoice: {spoken!r} reads {ratio:.2f}x the original's length "
                f"- past {MAX_STRETCH:.0%}; re-render instead")
        cut = workdir / f"revoice-{k}-cut.wav"
        sf.write(str(cut), new[b0:b1], sr)
        fit = workdir / f"revoice-{k}-fit.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(cut),
                        "-af", f"atempo={ratio:.5f}", str(fit)],
                       check=True, capture_output=True)
        fitted, _ = sf.read(str(fit), always_2d=True)
        n = a1 - a0
        fitted = (fitted[:n] if len(fitted) >= n
                  else np.vstack([fitted, np.zeros((n - len(fitted),
                                                    fitted.shape[1]))]))
        f = max(1, int(FADE * sr))
        ramp = np.linspace(0, 1, f)[:, None]
        fitted[:f] *= ramp
        fitted[-f:] *= ramp[::-1]
        audio[a0:a1] = fitted
        print(f"revoice: {said[:40]!r}... re-spoken over "
              f"{a0 / sr:.2f}-{a1 / sr:.2f}s (x{ratio:.3f})")
    out = workdir / "track-revoiced.wav"
    sf.write(str(out), audio, sr)
    return out


def reuse(mp4: Path, workdir: Path, total: float) -> Path:
    """The old render, copied aside (the new one may overwrite it), after
    checking its length still matches the timeline."""
    secs = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(mp4)],
        check=True, capture_output=True, text=True).stdout)
    if abs(secs - total) > 0.6:
        raise ValueError(f"reuse_picture: {mp4.name} is {secs:.2f}s, the "
                         f"timeline {total:.2f}s - the narration changed, "
                         f"re-render instead")
    dst = workdir / "picture-reused.mp4"
    shutil.copy2(mp4, dst)
    return dst
