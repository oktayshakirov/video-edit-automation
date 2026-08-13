"""Therapy sound beds, synthesized: noise colours and notched audio.

The sound-therapy short was built on two MP3s from the brand's own album, and
`video-tinnitus-short` records an honest limitation of them:

> even mixed, there is very little energy above 4 kHz, so a high whistling
> tinnitus will not be well covered by these two files. That is a property of
> the tracks, not the method.

It is also a property that disappears the moment the bed is generated instead of
sourced. **A noise colour is a specification, not a recording** — pink noise is
"equal energy per octave", brown is "-6 dB per octave", and both are exactly
producible. So the ceiling the short had to write copy around is gone: this can
put energy wherever the listener's tinnitus actually sits, including above
4 kHz where the album could not reach.

Two more things follow from generating it, and both matter more here than they
did for the music bed:

* **Notched sound therapy becomes possible.** The short skill lists tone
  matching as "the obvious next variant" and notes it "needs tone synthesis the
  repo still does not have". Removing a narrow band around a stated tinnitus
  frequency is a filter, and the whole approach rests on the audio being
  synthetic in the first place.
* **Any length, no loop.** A sound-therapy video wants ten minutes to an hour.
  Noise generated to length has no seam to hide, where a looped track has one
  every few minutes.

**This is not a treatment and nothing here should be described as one.** These
are the sounds people use; the site's own copy is careful about that and so is
this module's. See the skill.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.signal import butter, iirnotch, lfilter, sosfilt

SR = 48000


def _white(n: int, rng: np.random.Generator) -> np.ndarray:
    return rng.normal(0.0, 1.0, n).astype(np.float32)


def _pink(n: int, rng: np.random.Generator) -> np.ndarray:
    """Equal energy per octave, via the Voss-McCartney style IIR approximation.

    A true 1/f filter needs an FFT over the whole signal, which at an hour is
    gigabytes. This three-pole recursion is the standard cheap approximation and
    is within a fraction of a dB across the audible band.
    """
    w = _white(n, rng)
    b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
    a = [1.0, -2.494956002, 2.017265875, -0.522189400]
    return lfilter(b, a, w).astype(np.float32)


def _brown(n: int, rng: np.random.Generator) -> np.ndarray:
    """-6 dB per octave: white noise integrated, with the DC drift removed.

    A running sum wanders away from zero over minutes, which shows up as the
    waveform slowly leaving the centre and eventually clipping one side. The
    highpass at 12 Hz is inaudible and stops it.
    """
    w = np.cumsum(_white(n, rng)).astype(np.float32)
    sos = butter(1, 12.0, btype="high", fs=SR, output="sos")
    return sosfilt(sos, w).astype(np.float32)


def _green(n: int, rng: np.random.Generator) -> np.ndarray:
    """Mid-weighted noise, the "nature" colour — a broad band around 500 Hz."""
    sos = butter(2, [120.0, 2200.0], btype="band", fs=SR, output="sos")
    return sosfilt(sos, _pink(n, rng)).astype(np.float32)


COLOURS = {"white": _white, "pink": _pink, "brown": _brown, "green": _green}


@dataclass(frozen=True)
class Bed:
    """One therapy bed. `colour` is the base; the rest shapes it.

    `notch_hz` removes a narrow band, which is what "notched sound therapy"
    means — the listener states their tinnitus pitch and the bed is built with
    that band taken out. `notch_q` sets how narrow: higher is tighter.
    """
    colour: str = "pink"
    notch_hz: float | None = None
    notch_q: float = 6.0
    tilt_hz: float | None = None     # gentle lowpass, for a softer bed
    breathe: float = 0.0             # depth of a slow amplitude swell, 0-1
    breathe_period: float = 10.0     # seconds per swell


def render(duration: float, bed: Bed = Bed(), sr: int = SR,
           seed: int = 3) -> np.ndarray:
    """`duration` seconds of stereo bed as float32, peak-normalised to 0.9.

    The two channels are generated from different seeds rather than one signal
    duplicated. Identical channels collapse to a point between the ears, which
    is fatiguing over ten minutes; decorrelated noise is what makes a bed feel
    like a room instead of a headphone.
    """
    n = int(duration * sr)
    out = []
    for ch in range(2):
        rng = np.random.default_rng(seed + ch * 977)
        x = COLOURS[bed.colour](n, rng)

        if bed.tilt_hz:
            sos = butter(2, min(bed.tilt_hz, sr / 2 - 100), btype="low",
                         fs=sr, output="sos")
            x = sosfilt(sos, x).astype(np.float32)

        if bed.notch_hz:
            # Cascaded twice: one biquad notch is about 20 dB deep, which is
            # audible as a dip but not as a hole. Notched therapy wants the band
            # genuinely absent.
            b, a = iirnotch(bed.notch_hz, bed.notch_q, sr)
            x = lfilter(b, a, lfilter(b, a, x)).astype(np.float32)

        out.append(x)

    stereo = np.stack(out, axis=1)

    if bed.breathe > 0:
        t = np.arange(n) / sr
        env = (1.0 - bed.breathe
               + bed.breathe * (0.5 + 0.5 * np.sin(
                   2 * np.pi * t / bed.breathe_period - np.pi / 2)))
        stereo *= env[:, None].astype(np.float32)

    peak = float(np.max(np.abs(stereo))) or 1.0
    return (stereo / peak * 0.9).astype(np.float32)


def write(out: Path, duration: float, bed: Bed = Bed(), sr: int = SR,
          seed: int = 3) -> Path:
    import soundfile as sf

    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), render(duration, bed, sr, seed), sr)
    return out


def band_energy(x: np.ndarray, sr: int = SR) -> dict[str, float]:
    """Percent of energy per band — the check that a bed does what it claims.

    The short's two source tracks measured 87% below 200 Hz and 0.1% above
    4 kHz. Run this on anything new before writing copy about what it masks.
    """
    mono = x.mean(axis=1) if x.ndim > 1 else x
    seg = mono[:sr * 30] * np.hanning(min(len(mono), sr * 30))
    S = np.abs(np.fft.rfft(seg)) ** 2
    fr = np.fft.rfftfreq(len(seg), 1 / sr)
    tot = S.sum() or 1.0
    band = lambda lo, hi: 100.0 * S[(fr >= lo) & (fr < hi)].sum() / tot
    return {"<200": band(0, 200), "200-1k": band(200, 1000),
            "1k-4k": band(1000, 4000), "4k-8k": band(4000, 8000),
            ">8k": band(8000, sr / 2)}
