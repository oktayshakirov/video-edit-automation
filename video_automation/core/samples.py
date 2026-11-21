"""Short, quiet examples of the sounds tinnitus is described as (2026-10-28).

**Played on purpose, and only after a warning.** `what-does-tinnitus-sound-
like` was first cut drawn-only, on the reasoning that a played ringing is the
last thing a hyperacusis listener at 2am needs. The feed check overturned it:
every top result for "what does tinnitus sound like" plays examples, so a
video that only draws them makes a weaker promise on the one search it is
for. The editor's call: play them, short and quiet, with a lower-your-volume
card on screen and in the voice before the first one.

So each sample is:

- **short** - 1.6s, a breath, not a demonstration to sit inside;
- **quiet** - well under the voice (`LEVELS` in `core/sfx.py`), and the bed
  dips under it (`longform.audio.dip`) so it can stay quiet and still be
  heard;
- **soft-edged** - long fades both ends, nothing that starts as a transient.

**Placed in the pause after the sound is named, never under the voice.** A
beat names the sounds it plays in `Shot(samples=)`, one entry per reveal
(`None` for a reveal that plays nothing, such as the spectrum's floor). Each
sample ends `LEAD` seconds before the next caption begins, so the script buys
its room with a gap or a `chunk_pad` after the naming chunk - `cues` warns
when the room is not there.

Synthesised rather than recorded, so the level, length and band are ours and
match the drawn `spectrum` peak each one plays under.
"""

from pathlib import Path

import numpy as np

SR = 48000

DUR = {"ringing": 1.6, "hissing": 1.6, "humming": 1.6, "roaring": 1.6,
       "clicking": 1.6, "pulsing": 2.2}

LEAD = 0.25         # silence between a sample's end and the next caption
SPOKEN = 0.45       # the least a naming chunk takes to say - `cues` warns below it


def _fade(x: np.ndarray, sr: int, fin: float = 0.30, fout: float = 0.40) -> np.ndarray:
    n = len(x)
    env = np.ones(n)
    a, b = int(fin * sr), int(fout * sr)
    env[:a] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    env[n - b:] = 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, b))
    return x * env


def _band(noise: np.ndarray, sr: int, lo: float, hi: float) -> np.ndarray:
    """Noise band-passed in the frequency domain, with soft shoulders."""
    spec = np.fft.rfft(noise)
    f = np.fft.rfftfreq(len(noise), 1 / sr)
    w = (np.clip((f - lo * 0.8) / (lo * 0.2), 0, 1)
         * np.clip((hi * 1.2 - f) / (hi * 0.2), 0, 1))
    return np.fft.irfft(spec * w, len(noise))


def _rms(x: np.ndarray, target: float = 0.25) -> np.ndarray:
    """Equal RMS across samples, so `LEVELS` compares like with like."""
    return x * target / (np.sqrt(np.mean(x ** 2)) + 1e-12)


def ringing(sr: int = SR) -> np.ndarray:
    """A steady tone near 6 kHz - the middle of the spectrum's RINGING band."""
    t = np.arange(int(DUR["ringing"] * sr)) / sr
    return _fade(_rms(np.sin(2 * np.pi * 5950 * t)), sr)


def hissing(sr: int = SR) -> np.ndarray:
    """Noise from 2.8 to 12 kHz - steam, air escaping."""
    n = int(DUR["hissing"] * sr)
    noise = np.random.default_rng(11).standard_normal(n)
    return _fade(_rms(_band(noise, sr, 2800, 12000)), sr)


def humming(sr: int = SR) -> np.ndarray:
    """A 120 Hz buzz with its harmonics up to ~1.2 kHz.

    The fundamental alone is inaudible on a phone speaker, so the harmonics
    carry it there - which is also what makes a hum sound like a buzz.
    """
    t = np.arange(int(DUR["humming"] * sr)) / sr
    x = sum(np.sin(2 * np.pi * 120 * k * t) / k ** 1.3 for k in range(1, 11))
    return _fade(_rms(x), sr)


def roaring(sr: int = SR) -> np.ndarray:
    """Low, wide noise with a slow swell - a waterfall, a strong wind."""
    n = int(DUR["roaring"] * sr)
    noise = np.random.default_rng(13).standard_normal(n)
    t = np.arange(n) / sr
    swell = 0.8 + 0.2 * np.sin(2 * np.pi * 0.7 * t)
    return _fade(_rms(_band(noise, sr, 140, 1400) * swell), sr)


def clicking(sr: int = SR) -> np.ndarray:
    """Three soft clicks, half a second apart - a jaw opening and closing."""
    n = int(DUR["clicking"] * sr)
    x = np.zeros(n)
    k = int(0.018 * sr)
    burst = _band(np.random.default_rng(17).standard_normal(k * 4), sr,
                  600, 3500)[:k] * np.exp(-np.arange(k) / (0.004 * sr))
    for at in (0.25, 0.75, 1.25):
        i = int(at * sr)
        x[i:i + k] += burst
    # RMS over the clicks alone, or the silence between them drags it down
    # and the level comes out as a slap.
    x *= 0.25 / (np.sqrt(np.mean(burst ** 2)) + 1e-12) * 0.6
    return x


def pulsing(sr: int = SR) -> np.ndarray:
    """A low whoosh on each heartbeat, at 72 a minute - pulsatile tinnitus."""
    n = int(DUR["pulsing"] * sr)
    t = np.arange(n) / sr
    noise = _band(np.random.default_rng(19).standard_normal(n), sr, 90, 700)
    env = np.zeros(n)
    for beat in np.arange(0.15, DUR["pulsing"] - 0.3, 60 / 72):
        d = t - beat
        env += np.where(d >= 0, (d / 0.09) * np.exp(1 - d / 0.09), 0.0)
    return _fade(_rms(noise * env), sr, fin=0.05, fout=0.25)


MAKERS = {f"sample_{k}": f for k, f in
          {"ringing": ringing, "hissing": hissing, "humming": humming,
           "roaring": roaring, "clicking": clicking,
           "pulsing": pulsing}.items()}


def cues(shots, caption_starts: list[float], total: float
         ) -> list[tuple[float, str]]:
    """One cue per named sample, anchored on its end (`sfx.ANCHOR`).

    The next caption after a reveal's own is where the room ends; the sample
    finishes `LEAD` before it. Room shorter than the sample plus `SPOKEN`
    means the sample would sit on the voice, so it says so.
    """
    out: list[tuple[float, str]] = []
    for sh in shots:
        names = getattr(sh, "samples", None)
        if not names or not sh.reveals:
            continue
        for name, r in zip(names, sh.reveals):
            if not name:
                continue
            nxt = next((s for s in caption_starts if s > r + 0.30), total)
            room = nxt - LEAD - DUR[name] - r
            if room < SPOKEN:
                print(f"sample {name} at {r:.1f}s has {room:.2f}s for the "
                      f"voice - widen the gap after it")
            out.append((nxt - LEAD, f"sample_{name}"))
    return out


BED: dict[str, float] = {}     # a sample's own bed level, if not 0.2


def windows(cue_list: list[tuple[float, str]], pad: float = 0.15
            ) -> list[tuple[float, float, float]]:
    """Where each sample plays, and how far the bed dips under it: to 20%,
    or all the way out for a music example (`register(bed=0.0)`), which also
    gets a longer margin so the two tracks never overlap."""
    out = []
    for t, k in cue_list:
        if not k.startswith("sample_"):
            continue
        name = k[7:]
        g = BED.get(name, 0.2)
        p = pad if g > 0 else 0.6
        out.append((t - DUR[name] - p, t + p, g))
    return out


# -- recorded clips (2026-11-21) ---------------------------------------------
#
# A voice example, played in the pause after the line that names it - the
# OktAI opener plays the robotic read and today's read before Oktay speaks.
# Same rules as the tinnitus samples (in the pause, cued on its end, the bed
# dips under it), but **as loud as the voice**: it is something to compare
# with the narration, not a sound to be careful with.

def register(path, name: str | None = None, level: float = 0.9,
             bed: float = 0.2) -> str:
    """Make the audio file `path` a sample; returns its name for
    `Shot(samples=...)`. `level` is its peak against the narration's; `bed`
    is how far the music bed dips under it - 0.0 stops it, for a music
    example (the editor, 2026-11-21: "it needs to be paused for this part")."""
    import soundfile as sf
    from . import sfx
    path = Path(path)
    name = name or path.stem
    audio, sr = sf.read(str(path), always_2d=True, dtype="float32")
    mono = audio.mean(axis=1).astype(np.float64)
    if sr != SR:
        from scipy.signal import resample_poly
        mono = resample_poly(mono, SR, sr)
    mono /= (np.max(np.abs(mono)) + 1e-9)
    # A breath of fade at each end: no click, and the read is not softened.
    mono = _fade(mono, SR, fin=0.01, fout=0.04)
    key = f"sample_{name}"
    DUR[name] = len(mono) / SR
    MAKERS[key] = lambda sr, m=mono: (m if sr == SR else _resample(m, sr))
    sfx.ANCHOR[key] = DUR[name]
    # `sfx.mix` scales every cue by its gain against the narration's peak.
    sfx.LEVELS[key] = level / sfx.DEFAULT_GAIN
    BED[name] = bed
    return name


def _resample(m: np.ndarray, sr: int) -> np.ndarray:
    from scipy.signal import resample_poly
    return resample_poly(m, sr, SR)
