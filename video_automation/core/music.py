"""Music beds, synthesized rather than sourced.

`sfx.py` already argues this for two hundred milliseconds of UI click: a
downloaded "free" sound pulls in a licence question, a generated one is ours
forever and is *parameterised*. A three-minute bed is a bigger ask than a click,
but the argument gets stronger rather than weaker at that length:

* **Licensing stops being a footnote.** The YouTube Audio Library is free and
  cleared for YouTube — and that clearance does not travel to a TikTok repost,
  which is a thing this repo does routinely. A generated bed has no such edge.
* **No loop seam.** The library's tracks are frequently shorter than three
  minutes; `render_bed` loops them, and a loop is only invisible if the track
  was written to loop. This is generated to the exact length asked for.
* **It is the channel's sound.** Two or three named presets used across every
  video is a brand; a different stock track each time is not.

The design brief is deliberately narrow: **an explainer bed should be close to
subliminal.** It exists so three minutes of dry narration does not feel like a
voicemail. Anything with a melody competes with the words. So: slow chord pads,
a sub, a breath of air, and nothing that asks to be noticed.

What keeps it from sounding like a test tone is entirely the small stuff —
detuning between oscillators, a filter that drifts, per-channel spread, and
chords that cross-fade rather than switch. Those four things are the difference
between "music" and "an oscillator".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000

# Semitone offsets from the root. Minor keys throughout — an explainer wants
# "serious", and a major bed under a piece about fraud reads as sarcasm.
PROGRESSIONS = {
    # i - VI - III - VII. The most-used minor loop there is, because it never
    # resolves hard enough to draw attention to itself.
    "andalusian": [(0, 3, 7), (8, 12, 15), (3, 7, 10), (10, 14, 17)],
    # i - iv - i - V, sparser, for something that should sit further back.
    "plain": [(0, 3, 7), (5, 8, 12), (0, 3, 7), (7, 11, 14)],
}


@dataclass(frozen=True)
class Preset:
    """One bed. The numbers are the whole character; see `render`."""

    name: str
    root: float                 # Hz of the tonic, low
    progression: str
    chord_len: float            # seconds per chord — slow is the point
    cutoff: tuple[float, float]  # lowpass sweep range, Hz
    sweep: float                # seconds per filter breath
    detune: float               # cents between stacked oscillators
    partials: int               # harmonics per voice; more = brighter, reedier
    sub: float                  # level of the octave-down sine
    air: float                  # high noise bed. **Zero on every preset with
                                # a rhythm section**: under a bare pad it reads
                                # as space, but with plucks and a kick present
                                # it is simply audible hiss.
    pulse: float = 0.0          # depth of a slow amplitude pulse, 0 = none
    pulse_hz: float = 0.5
    # --- the rhythm section --------------------------------------------
    # Pads alone read as "mysterious" no matter how they are voiced — the first
    # cut of the Satoshi video was described as creepy, and it was three chords
    # and a filter. **What makes a bed feel dynamic is note events**, not
    # brightness: something that repeats on a grid gives the piece a tempo, and
    # a tempo is what the ear reads as momentum rather than atmosphere.
    bpm: float = 0.0            # 0 = no rhythm section at all
    arp: float = 0.0            # plucked arpeggio level
    arp_div: int = 2            # notes per beat
    arp_decay: float = 0.26     # pluck decay, seconds
    kick: float = 0.0           # soft kick level
    kick_div: int = 1           # kicks per beat


PRESETS = {
    # thecrypto.wiki. Dark, a slow pulse under it so the piece has a heartbeat
    # without having a rhythm.
    "tension": Preset(
        name="tension", root=55.0, progression="andalusian", chord_len=8.0,
        cutoff=(700.0, 1900.0), sweep=19.0, detune=11.0, partials=5,
        sub=0.22, air=0.020, pulse=0.16, pulse_hz=0.5,
    ),
    # tinnitushelp.me. No pulse at all, softer top, slower everything — the
    # audience for that channel is frequently there *because* sound is a
    # problem, and a bed with a throb in it is the wrong instrument.
    "calm": Preset(
        name="calm", root=49.0, progression="plain", chord_len=11.0,
        cutoff=(520.0, 1150.0), sweep=27.0, detune=7.0, partials=3,
        sub=0.20, air=0.012, pulse=0.0,
    ),
    # --- the dynamic set ------------------------------------------------
    # Everything above is atmosphere. These have a tempo, which is the whole
    # difference between "mysterious" and "going somewhere".

    # Mid-tempo, plucked, minor but open. The default for an explainer.
    "momentum": Preset(
        name="momentum", root=55.0, progression="andalusian", chord_len=7.0,
        cutoff=(900.0, 2400.0), sweep=15.0, detune=9.0, partials=4,
        sub=0.17, air=0.0, pulse=0.0,
        bpm=100, arp=0.26, arp_div=2, arp_decay=0.24, kick=0.13, kick_div=1,
    ),
    # Faster and more electronic — sixteenths, brighter, a firmer kick.
    "pulse": Preset(
        name="pulse", root=58.0, progression="andalusian", chord_len=6.0,
        cutoff=(1100.0, 3000.0), sweep=11.0, detune=12.0, partials=5,
        sub=0.16, air=0.0, pulse=0.0,
        bpm=112, arp=0.24, arp_div=4, arp_decay=0.15, kick=0.16, kick_div=1,
    ),
    # Warmer and less serious, for a piece that is not about risk.
    "bright": Preset(
        name="bright", root=62.0, progression="plain", chord_len=8.0,
        cutoff=(1000.0, 2600.0), sweep=17.0, detune=8.0, partials=4,
        sub=0.15, air=0.0, pulse=0.0,
        bpm=96, arp=0.28, arp_div=2, arp_decay=0.30, kick=0.10, kick_div=1,
    ),

    # Brighter and moving, for a piece with momentum.
    "drive": Preset(
        name="drive", root=62.0, progression="andalusian", chord_len=6.0,
        cutoff=(900.0, 2600.0), sweep=13.0, detune=14.0, partials=6,
        sub=0.20, air=0.028, pulse=0.24, pulse_hz=1.0,
    ),
}


# --------------------------------------------------------------------------
# Real tracks, as a small committed library
# --------------------------------------------------------------------------
#
# The generated presets above are still the default and still the safer choice
# on licence grounds. This is the escape hatch for a track the user has picked
# by ear, kept beside the backgrounds and for the same reasons: small, reusable,
# needed on every machine, and re-deriving it by hand is the step that gets
# lost.
#
# **Tracks are stored trimmed, and that is the whole point of storing them.**
# An mp3 decodes with encoder delay — a few dozen milliseconds of digital
# silence bolted to the front — and `render_bed` loops a short track to fill
# the video. Measured on the first track added here: 54.4 ms of leading silence
# against an end that runs at full level, so a naive loop drops a hole in the
# bed every 7.7 seconds, twenty-nine times in a four minute video. `render_bed`
# has a `start=` offset that would paper over it, but then the correct offset
# is a number somebody has to remember per track. Trimming once, at import
# time, makes the asset correct by construction.

TRACKS = Path(__file__).resolve().parents[2] / "assets/brand/music"


def prepare_track(src: Path, name: str, floor: float = 1e-4) -> Path:
    """Trim digital silence off both ends and store as WAV under `name`.

    WAV rather than mp3 so the stored asset decodes sample-exact — re-encoding
    would reintroduce exactly the delay this removes.
    """
    import subprocess
    import wave

    TRACKS.mkdir(parents=True, exist_ok=True)
    out = TRACKS / f"{name}.wav"
    tmp = TRACKS / f".{name}-probe.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src),
                    "-ar", str(SR), "-ac", "1", str(tmp)], check=True)
    with wave.open(str(tmp)) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    nz = np.nonzero(np.abs(a.astype(float) / 32768) > floor)[0]
    tmp.unlink()
    if not len(nz):
        raise ValueError(f"{src} is silent")
    start, end = nz[0] / SR, (len(a) - nz[-1]) / SR
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.6f}",
                    "-i", str(src), "-af", f"atrim=end={(len(a)/SR)-start-end:.6f}",
                    "-ar", "44100", "-ac", "2", str(out)], check=True)
    return out


def track(name: str) -> Path:
    """A prepared track by name, for passing to `render_long(music=...)`."""
    p = TRACKS / f"{name}.wav"
    if not p.exists():
        raise FileNotFoundError(
            f"no music track {name!r} in {TRACKS} — add one with "
            f"prepare_track(src, {name!r})")
    return p


def _semi(root: float, n: int) -> float:
    return root * (2.0 ** (n / 12.0))


def _voice(f: float, n: int, sr: int, p: Preset,
           rng: np.random.Generator) -> np.ndarray:
    """One note, as a small stack of detuned harmonic oscillators.

    Three copies at +/- `detune` cents is the cheapest thing that turns a sine
    into an instrument: the beating between them is slow, irregular and is what
    the ear reads as "an ensemble" rather than "a tone".
    """
    t = np.arange(n) / sr
    out = np.zeros(n, dtype=np.float32)
    for d in (-1.0, 0.0, 1.0):
        fd = f * (2.0 ** (d * p.detune / 1200.0))
        # A slow, per-oscillator vibrato at well under a Hz. Too little to hear
        # as pitch movement, enough to stop the beating settling into a pattern.
        vib = 1.0 + 0.0016 * np.sin(2 * np.pi * rng.uniform(0.05, 0.13) * t
                                    + rng.uniform(0, 6.28))
        for k in range(1, p.partials + 1):
            # 1/k, not 1/k². The squared roll-off was tried first and left the
            # pad as effectively a sine at its fundamental — with 96% of the
            # bed's energy under 200 Hz, which is a rumble rather than music.
            # The lowpass below is what sets brightness; the oscillator should
            # arrive with something for it to take away.
            out += (np.sin(2 * np.pi * fd * k * vib * t + rng.uniform(0, 6.28))
                    / k).astype(np.float32)
    return out / (p.partials * 3)


def _pluck(f: float, n: int, sr: int, decay: float) -> np.ndarray:
    """One short plucked note: a couple of partials under a fast decay.

    Deliberately simple. The pluck's job is to mark time, so what matters is
    that its envelope is short enough to leave a gap before the next one — a
    sustained note on a grid is just a pad again.
    """
    t = np.arange(n) / sr
    env = np.exp(-t / decay).astype(np.float32)
    return ((np.sin(2 * np.pi * f * t)
             + 0.5 * np.sin(2 * np.pi * f * 2 * t)
             + 0.22 * np.sin(2 * np.pi * f * 3 * t)) * env).astype(np.float32)


def _kick(n: int, sr: int) -> np.ndarray:
    """A soft kick: a sine dropping in pitch, with a click on the front."""
    t = np.arange(n) / sr
    f = 110.0 * np.exp(-t / 0.045) + 42.0
    body = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t / 0.16)
    click = np.exp(-t / 0.004) * np.random.default_rng(5).normal(0, 0.35, n)
    return (body + click * 0.5).astype(np.float32)


def _rhythm(p: Preset, notes: tuple, n: int, sr: int, start_beat: int
            ) -> tuple[np.ndarray, np.ndarray]:
    """The arpeggio and kick for one chord segment, as (left, right)."""
    left = np.zeros(n, dtype=np.float32)
    right = np.zeros(n, dtype=np.float32)
    if p.bpm <= 0:
        return left, right

    spb = 60.0 / p.bpm
    if p.arp > 0:
        step = spb / p.arp_div
        # Up and back down the chord, an octave higher than the pad so the
        # plucks sit above it instead of muddying the same band.
        order = list(notes) + [notes[-1] + 12] + list(reversed(notes))
        note_n = int(p.arp_decay * 3 * sr)
        i, k = 0, start_beat * p.arp_div
        while i * step < n / sr:
            at = int(i * step * sr)
            f = _semi(p.root, order[k % len(order)]) * 8
            v = _pluck(f, min(note_n, n - at), sr, p.arp_decay) * p.arp
            # Alternate the pan per note, which is what makes an arpeggio feel
            # like it is moving rather than repeating in one place.
            pan = 0.36 if (k % 2) else 0.64
            left[at:at + len(v)] += v * (1 - pan)
            right[at:at + len(v)] += v * pan
            i += 1
            k += 1

    if p.kick > 0:
        step = spb / p.kick_div
        kn = int(0.30 * sr)
        i = 0
        while i * step < n / sr:
            at = int(i * step * sr)
            v = _kick(min(kn, n - at), sr) * p.kick
            left[at:at + len(v)] += v
            right[at:at + len(v)] += v
            i += 1
    return left, right


def _lp(x: np.ndarray, hz: float, sr: int) -> np.ndarray:
    sos = butter(2, min(hz, sr / 2 - 100), btype="low", fs=sr, output="sos")
    return sosfilt(sos, x).astype(np.float32)


def render(duration: float, preset: str = "tension", sr: int = SR,
           seed: int = 11) -> np.ndarray:
    """`duration` seconds of stereo bed, as float32 in [-1, 1].

    Chords are overlap-added with a long cross-fade rather than butted together.
    A chord that switches is an event and the ear turns to look at it; a chord
    that dissolves into the next one is weather.
    """
    p = PRESETS[preset]
    rng = np.random.default_rng(seed)
    n = int(duration * sr)
    left = np.zeros(n, dtype=np.float32)
    right = np.zeros(n, dtype=np.float32)

    chords = PROGRESSIONS[p.progression]
    xf = min(p.chord_len * 0.45, 4.0)
    step = p.chord_len - xf
    seg_n = int(p.chord_len * sr)
    fade = np.minimum(np.arange(seg_n) / (xf * sr), 1.0).astype(np.float32)
    win = fade * fade[::-1]                  # equal-ish power in and out

    i, start = 0, 0.0
    while start < duration:
        notes = chords[i % len(chords)]
        i += 1
        seg_l = np.zeros(seg_n, dtype=np.float32)
        seg_r = np.zeros(seg_n, dtype=np.float32)
        for j, semi in enumerate(notes):
            # **Two octaves above the sub, not one.** At *2 the chord's own
            # fundamental was 110 Hz and the pad lived in the same band as
            # the bass — measured at 96% of total energy below 200 Hz. The
            # pad has to sit where a voice is not, which is above it.
            f = _semi(p.root, semi) * 4
            v = _voice(f, seg_n, sr, p, rng)
            # Spread the voices across the stereo field by index, so the chord
            # has width without anything being hard-panned.
            pan = 0.5 + 0.34 * ((j / max(len(notes) - 1, 1)) - 0.5) * 2
            seg_l += v * (1.0 - pan)
            seg_r += v * pan
        # The sub, centred — bass in the sides is what makes a mix feel loose.
        sub = np.sin(2 * np.pi * _semi(p.root, notes[0])
                     * np.arange(seg_n) / sr).astype(np.float32) * p.sub
        seg_l += sub
        seg_r += sub

        a = int(start * sr)
        b = min(n, a + seg_n)
        if b > a:
            left[a:b] += (seg_l * win)[:b - a]
            right[a:b] += (seg_r * win)[:b - a]

        # The rhythm is added *outside* the chord cross-fade window. Fading a
        # pluck in and out with its chord smears the attacks, and the attack is
        # the entire reason it is there.
        if p.bpm > 0 and b > a:
            beat = int(round(start / (60.0 / p.bpm)))
            rl, rr = _rhythm(p, notes, b - a, sr, beat)
            left[a:b] += rl
            right[a:b] += rr
        start += step

    # One filter breath across the whole piece, done by cross-fading a dark and
    # a bright copy rather than by sweeping a live filter. Cheaper, and it never
    # rings the way a modulated IIR can.
    t = np.arange(n) / sr
    lfo = (0.5 + 0.5 * np.sin(2 * np.pi * t / p.sweep)).astype(np.float32)
    out = []
    for ch in (left, right):
        dark = _lp(ch, p.cutoff[0], sr)
        bright = _lp(ch, p.cutoff[1], sr)
        out.append(dark * (1 - lfo) + bright * lfo)

    if p.air > 0:
        air = rng.normal(0, 1, n).astype(np.float32)
        sos = butter(2, 3600, btype="high", fs=sr, output="sos")
        air = sosfilt(sos, air).astype(np.float32) * p.air
        air *= (0.6 + 0.4 * np.sin(2 * np.pi * t / (p.sweep * 1.7))).astype(np.float32)
        out[0] = out[0] + air
        out[1] = out[1] + np.roll(air, 811)   # decorrelate, so the air is wide

    if p.pulse > 0:
        # A slow swell, not a beat. It gives the piece a pulse without giving
        # it a tempo the edit would then be expected to cut to.
        env = (1.0 - p.pulse
               + p.pulse * (0.5 + 0.5 * np.sin(2 * np.pi * p.pulse_hz * t
                                               - np.pi / 2))).astype(np.float32)
        out = [ch * env for ch in out]

    stereo = np.stack(out, axis=1)
    peak = float(np.max(np.abs(stereo))) or 1.0
    return (stereo / peak * 0.85).astype(np.float32)


def write(out: Path, duration: float, preset: str = "tension",
          sr: int = SR, seed: int = 11) -> Path:
    """Render a bed to a WAV. `render_bed` in longform/audio.py takes it from here."""
    import soundfile as sf

    out.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(out), render(duration, preset, sr, seed), sr)
    return out
