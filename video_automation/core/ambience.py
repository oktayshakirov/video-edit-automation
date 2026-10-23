"""Quiet place-sound under footage: a city, rain, an office, a server room.

The film surface gave the picture texture; this does it for the sound
(2026-10-23, the user's pick after an A/B). A footage shot of a place gets a
quiet bed of that place, crossfaded at the cuts; drawn beats get nothing, so
a chart still sits in clean air.

**Restraint is the rule** - the user's words were "make sure we don't
overdo it, only if it helps the delivery of the script". So a bed plays only
when all of these hold, and otherwise the shot is left as it was:

* the clip's own stock folder names a place we have a bed for
  (`KEYWORDS`) - abstract footage, faces, hands and graphics get none;
* the shot (or a run of consecutive shots of the same place, which share
  one continuous bed) lasts at least `MIN_RUN` seconds - a bed that
  arrives and leaves inside two seconds is a blip, not a place;
* it sits ~23dB under the finished mix (`LEVEL_DB`): audible in the pauses
  between sentences, gone under the voice.

Generated, like every other sound in this package: band-limited noise
shaped into each place, seeded, so a rebuild is identical and nothing needs
licensing. **Deliberately atonal** - no steady hum - because a sustained
pitch under a voice is the one thing a tinnitus audience must not be handed.
The tinnitus kit takes the beds down a further `KIT_GAIN`.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

SR = 48000
LEVEL_DB = -22.8        # under the finished mix's RMS. The approved A/B mixed
                        # at -22.0; the user asked for 5-10% quieter, and
                        # -0.8dB is 9% in amplitude.
MIN_RUN = 3.0           # seconds a place has to stay on screen to get a bed
XF = 0.6                # crossfade at each end of a bed
KIT_GAIN = {"tinnitus": 0.8}

# Stock folder keywords -> bed. Order matters: the first match wins.
KEYWORDS = [
    ("rain", "rain"), ("storm", "rain"),
    ("server", "servers"), ("data-center", "servers"),
    ("office", "office"), ("desk", "office"), ("laptop", "office"),
    ("keyboard", "office"),
    ("traffic", "city"), ("street", "city"), ("city", "city"),
]


def _noise(n: int, seed: int, slope: float = 1.0) -> np.ndarray:
    """Stereo noise with a 1/f**slope power spectrum (1 pink, 2 brown),
    shaped in the frequency domain - one FFT, not a per-sample filter."""
    rng = np.random.default_rng(seed)
    w = rng.normal(0, 1, (n, 2))
    spec = np.fft.rfft(w, axis=0)
    f = np.fft.rfftfreq(n, 1 / SR)
    f[0] = f[1] if len(f) > 1 else 1.0
    spec *= (1.0 / f ** (slope / 2))[:, None]
    out = np.fft.irfft(spec, n=n, axis=0)
    return out / (np.max(np.abs(out)) + 1e-9)


def _band(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    from scipy.signal import butter, sosfiltfilt
    return sosfiltfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"),
                       x, axis=0)


def _swells(n: int, seed: int, every=(3.0, 6.0), length=(2.0, 4.0)):
    """Slow bumps in level - a car passing, a gust - never a pulse."""
    rng = np.random.default_rng(seed)
    env = np.zeros(n)
    t = rng.uniform(0, every[0])
    while t * SR < n:
        L = rng.uniform(*length)
        a, b = int(t * SR), int(min(n, (t + L) * SR))
        if b > a:
            env[a:b] += (np.sin(np.linspace(0, np.pi, b - a)) ** 2
                         * rng.uniform(0.5, 1.0))
        t += rng.uniform(*every)
    return env[:, None]


def city(n: int, seed: int = 0) -> np.ndarray:
    rumble = _band(_noise(n, seed + 1, 2.0), 30, 300)
    traffic = _band(_noise(n, seed + 2), 150, 1200) * (0.25 + _swells(n, seed + 3))
    air = _band(_noise(n, seed + 4), 2000, 7000) * 0.08
    return rumble + traffic * 0.7 + air


def rain(n: int, seed: int = 0) -> np.ndarray:
    hiss = _band(_noise(n, seed + 5), 900, 9000)
    rng = np.random.default_rng(seed + 6)
    drops = np.zeros((n, 2))
    k = int(n / SR * 45)
    idx = rng.integers(0, n, k)
    drops[idx, rng.integers(0, 2, k)] = rng.uniform(-1, 1, k)
    kern = np.exp(-np.arange(90) / 12.0)
    drops = np.stack([np.convolve(drops[:, c], kern)[:n] for c in (0, 1)], 1)
    drops = _band(drops, 1500, 7000)
    low = _band(_noise(n, seed + 7, 2.0), 40, 250)
    return hiss * 0.55 + drops * 0.9 + low * 0.35


def office(n: int, seed: int = 0) -> np.ndarray:
    from . import sfx
    air = _band(_noise(n, seed + 8), 120, 1600)           # ventilation
    room = _band(_noise(n, seed + 9, 2.0), 40, 400) * 0.6
    keys = np.zeros((n, 2))
    rng = np.random.default_rng(seed + 10)
    t = rng.uniform(0.5, 2.0)
    while t * SR < n - SR:                                # someone typing, far off
        for _ in range(int(rng.integers(4, 12))):
            clip = sfx.key(SR, variant=int(rng.integers(0, 4))) * 0.5
            i = int(t * SR)
            m = max(0, min(len(clip), n - i))
            keys[i:i + m, int(rng.integers(0, 2))] += clip[:m]
            t += rng.uniform(0.09, 0.22)
        t += rng.uniform(1.5, 4.0)
    return air * 0.8 + room + _band(keys, 400, 3500) * 0.35


def servers(n: int, seed: int = 0) -> np.ndarray:
    fans = _band(_noise(n, seed + 11), 180, 4000)
    rush = _band(_noise(n, seed + 12, 2.0), 60, 500) * 0.8
    return fans * 0.7 + rush


BEDS = {"city": city, "rain": rain, "office": office, "servers": servers}


def bed_for(shot) -> str | None:
    """The bed a shot's footage calls for, or None."""
    if shot is None or getattr(shot, "clip", None) is None:
        return None
    name = Path(shot.clip).parent.name.lower()
    return next((bed for key, bed in KEYWORDS if key in name), None)


def plan(shots) -> list[tuple[float, float, str]]:
    """(start, end, bed) runs: consecutive shots of one place share a bed,
    and a run shorter than `MIN_RUN` gets none."""
    runs: list[list] = []
    for sh in shots:
        if sh is None:
            continue
        bed = bed_for(sh)
        end = sh.start + sh.hold
        if bed and runs and runs[-1][2] == bed and abs(runs[-1][1] - sh.start) < 0.05:
            runs[-1][1] = end
        elif bed:
            runs.append([sh.start, end, bed])
    return [(a, b, k) for a, b, k in runs if b - a >= MIN_RUN]


def track(shots, total: float) -> np.ndarray:
    """The beds as one stereo track, each at unit RMS before its fades."""
    n = int(total * SR)
    out = np.zeros((n, 2))
    for i, (a, b, kind) in enumerate(plan(shots)):
        i0 = max(0, int((a - XF / 2) * SR))
        i1 = min(n, int((b + XF / 2) * SR))
        if i1 - i0 < SR // 2:
            continue
        seg = BEDS[kind](i1 - i0, seed=i * 101)
        seg /= np.sqrt(np.mean(seg ** 2)) + 1e-9
        ramp = min(int(XF * SR), (i1 - i0) // 2)
        env = np.ones(i1 - i0)
        env[:ramp] = np.linspace(0.0, 1.0, ramp)
        env[-ramp:] = np.minimum(env[-ramp:], np.linspace(1.0, 0.0, ramp))
        out[i0:i1] += seg * env[:, None]
    return out


def mix(src: Path, out: Path, shots, total: float,
        kit: str | None = None, gain: float = 1.0) -> Path:
    """Lay the beds under a finished mix, `LEVEL_DB` under its own RMS."""
    import soundfile as sf
    beds = track(shots, total)
    if not np.any(beds):
        return src
    audio, sr = sf.read(str(src), always_2d=True, dtype="float64")
    if sr != SR:
        raise ValueError(f"ambience expects {SR} Hz, got {sr}")
    rms = float(np.sqrt(np.mean(audio ** 2))) or 1e-4
    level = rms * 10 ** (LEVEL_DB / 20) * gain * KIT_GAIN.get(kit or "", 1.0)
    m = min(len(audio), len(beds))
    if audio.shape[1] == 1:
        audio = np.repeat(audio, 2, axis=1)
    audio[:m] += beds[:m] * level
    peak = float(np.max(np.abs(audio)))
    if peak > 0.99:
        audio *= 0.99 / peak
    sf.write(str(out), audio.astype(np.float32), SR)
    return out
