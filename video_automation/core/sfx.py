"""Sound effects, synthesized rather than sourced.

The drone project's SFX are hand-placed clips from a music library, carried
through rebuilds by path. That does not transfer here: a headless render cannot
depend on a file living inside a Final Cut bundle, and downloading "free" UI
clicks pulls in a licence question for two hundred milliseconds of audio.

So these are generated. Both marks are two lines of numpy, they cost nothing to
ship, they are ours to license, and — the part that actually matters — they are
*parameterised*, so the cross and the tick are audibly the same instrument at
different pitches rather than two unrelated sounds bolted together.

The design is a UI sound, not a cartoon: a short pitched body with a noise
transient on the front and an exponential decay. What separates a click that
feels like software from one that feels cheap is almost entirely the envelope —
an instant attack and a decay short enough that it never competes with a
syllable.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

SR = 48000


def _env(n: int, sr: int, attack: float, decay: float) -> np.ndarray:
    """Instant-ish attack, exponential decay. The whole character is here."""
    t = np.arange(n) / sr
    a = np.clip(t / max(attack, 1e-6), 0.0, 1.0)
    return a * np.exp(-t / decay)


def _noise_transient(n: int, sr: int, decay: float = 0.006) -> np.ndarray:
    """The click at the very front, which is what makes it read as a UI sound."""
    rng = np.random.default_rng(7)          # fixed, so renders are reproducible
    return rng.normal(0.0, 1.0, n) * _env(n, sr, 0.0002, decay)


def mark_cross(sr: int = SR, dur: float = 0.10) -> np.ndarray:
    """A dry, low knock for a struck-through item. Deliberately unmusical."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    body = (np.sin(2 * np.pi * 196.0 * t) + 0.5 * np.sin(2 * np.pi * 98.0 * t))
    out = body * _env(n, sr, 0.001, 0.030) + 0.35 * _noise_transient(n, sr)
    return out / (np.max(np.abs(out)) + 1e-9)


def mark_tick(sr: int = SR, dur: float = 0.55) -> np.ndarray:
    """A bright two-partial chime for the one item that counts.

    A fifth above the cross's fundamental and an octave above that, so the
    payoff sound is the same family resolving upward rather than a new noise.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    body = (np.sin(2 * np.pi * 1174.7 * t) * _env(n, sr, 0.001, 0.16)
            + 0.55 * np.sin(2 * np.pi * 1760.0 * t) * _env(n, sr, 0.001, 0.10)
            + 0.30 * np.sin(2 * np.pi * 2349.3 * t) * _env(n, sr, 0.001, 0.05))
    out = body + 0.20 * _noise_transient(n, sr, 0.004)
    return out / (np.max(np.abs(out)) + 1e-9)


def whoosh(sr: int = SR, dur: float = 0.62, down: bool = False) -> np.ndarray:
    """A band of noise sweeping across the spectrum. The transition sound.

    Made from noise rather than a tone because a pitched sweep is a siren and
    reads as an alert. What makes it a *whoosh* is that the band moves and the
    amplitude peaks in the middle rather than at the front — the opposite
    envelope to everything else in this file, which are all impacts.

    The sweep is eight overlapping band-passed blocks rather than one live
    filter: modulating an IIR's cutoff rings audibly, and at this length the
    block version costs nothing.
    """
    from scipy.signal import butter, sosfilt

    n = int(sr * dur)
    rng = np.random.default_rng(19)
    noise = rng.normal(0.0, 1.0, n)

    out = np.zeros(n)
    blocks = 8
    lo, hi = (2600.0, 320.0) if down else (320.0, 2600.0)
    for b in range(blocks):
        f = lo + (hi - lo) * (b / (blocks - 1))
        sos = butter(2, [max(80.0, f * 0.55), min(sr / 2 - 100, f * 1.8)],
                     btype="band", fs=sr, output="sos")
        band = sosfilt(sos, noise)
        centre = (b + 0.5) / blocks * n
        w = np.exp(-0.5 * ((np.arange(n) - centre) / (n / blocks * 0.9)) ** 2)
        out += band * w

    # Swell in, fall away — a transition covers a cut, so its loudest moment
    # belongs *on* the cut rather than before it.
    t = np.arange(n) / sr
    out *= np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.4
    return out / (np.max(np.abs(out)) + 1e-9)


def riser(sr: int = SR, dur: float = 0.9) -> np.ndarray:
    """Noise plus a rising partial, landing at full level. Goes *into* a card.

    Distinct from `whoosh`: a whoosh covers a cut that has already happened, a
    riser says one is coming. Only for chapter boundaries, where there is
    genuinely something to announce — anywhere else it is a drum roll before a
    sentence.
    """
    from scipy.signal import butter, sosfilt

    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(23)

    sos = butter(2, 900, btype="high", fs=sr, output="sos")
    air = sosfilt(sos, rng.normal(0.0, 1.0, n))

    # An exponential glide, so the rise accelerates the way a held breath does.
    f = 180.0 * (2.0 ** (2.4 * (t / dur) ** 1.6))
    tone = np.sin(2 * np.pi * np.cumsum(f) / sr) * 0.5

    out = (air * 0.85 + tone) * (t / dur) ** 1.7
    return out / (np.max(np.abs(out)) + 1e-9)


def impact(sr: int = SR, dur: float = 0.85) -> np.ndarray:
    """A low, soft thud for a chapter card landing. The riser's full stop."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    body = (np.sin(2 * np.pi * 58.0 * t) * _env(n, sr, 0.002, 0.22)
            + 0.4 * np.sin(2 * np.pi * 87.0 * t) * _env(n, sr, 0.002, 0.13))
    out = body + 0.18 * _noise_transient(n, sr, 0.010)
    return out / (np.max(np.abs(out)) + 1e-9)


def reveal(sr: int = SR, dur: float = 0.16) -> np.ndarray:
    """A very short, soft tick for an item arriving on a drawn beat.

    Deliberately quieter and duller than `mark_cross`: an item appearing is not
    an event, it is punctuation. At `mark_cross`'s level a five-item list turns
    into a typewriter.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    body = np.sin(2 * np.pi * 660.0 * t) * _env(n, sr, 0.001, 0.016)
    out = body + 0.25 * _noise_transient(n, sr, 0.0025)
    return out / (np.max(np.abs(out)) + 1e-9)


def link(sr: int = SR, dur: float = 0.13) -> np.ndarray:
    """A soft two-partial click for a connector landing on a diagram box — the
    sound of "and therefore".

    Fuller than `reveal` (one partial, for a line of type arriving) because
    this marks a *relationship* being made, but still well under a struck
    mark. A fifth stacked on the fundamental, the same interval `mark_tick`
    uses, so the drawn beats sound like one instrument.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    body = (np.sin(2 * np.pi * 523.3 * t) * _env(n, sr, 0.001, 0.020)
            + 0.5 * np.sin(2 * np.pi * 784.0 * t) * _env(n, sr, 0.001, 0.013))
    out = body + 0.28 * _noise_transient(n, sr, 0.003)
    return out / (np.max(np.abs(out)) + 1e-9)


def loop_close(sr: int = SR, dur: float = 0.42) -> np.ndarray:
    """A low, round tone easing downward — the feedback arrow closing a cycle.

    Distinct from `impact` (lower and heavier, a full stop) and `mark_cross`
    (a dry knock): this one is pitched and a little warm, because a loop
    closing is a resolution rather than a hit. It is the one moment in a
    `diagram` that is about the mechanism as a whole.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    f = 233.0 * (2.0 ** (-0.28 * (t / dur)))          # a slight fall
    tone = np.sin(2 * np.pi * np.cumsum(f) / sr)
    out = (tone * _env(n, sr, 0.004, 0.20)
           + 0.4 * np.sin(2 * np.pi * 116.5 * t) * _env(n, sr, 0.004, 0.14)
           + 0.12 * _noise_transient(n, sr, 0.006))
    return out / (np.max(np.abs(out)) + 1e-9)


def limit(sr: int = SR, dur: float = 0.34) -> np.ndarray:
    """A firm low note with a touch of grit — the `gauge` marker crossing its
    threshold.

    Not a siren: a pitched sweep reads as an alert and this is not an alarm,
    it is a fact landing. One weighted note that says "past the line" and
    stops. D2 with a fifth under it and a quiet octave over.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    body = (np.sin(2 * np.pi * 146.8 * t) * _env(n, sr, 0.002, 0.19)
            + 0.45 * np.sin(2 * np.pi * 98.0 * t) * _env(n, sr, 0.002, 0.12)
            + 0.20 * np.sin(2 * np.pi * 220.0 * t) * _env(n, sr, 0.002, 0.06))
    out = body + 0.22 * _noise_transient(n, sr, 0.008)
    return out / (np.max(np.abs(out)) + 1e-9)


def clock(sr: int = SR, dur: float = 0.09) -> np.ndarray:
    """One second of a countdown clock. Wood-dry, no pitch to speak of.

    The quiz format lays one of these per second under a silent countdown, so
    it has to survive being heard eight times in a row without turning into a
    rhythm section. That rules out the `mark_cross` recipe: its 196 Hz body is
    a *note*, and eight of the same note in a row reads as music the bed is out
    of tune with. This is nearly all transient — a band-passed click with only
    enough body to give it a body — which is what a real escapement sounds
    like and what stays neutral against any bed.

    The tension comes from the spacing and from the silence around it, not from
    the sound. Anything more dramatic here and the viewer is being hurried
    rather than given time to think, which is the opposite of the beat's job.
    """
    from scipy.signal import butter, sosfilt

    n = int(sr * dur)
    rng = np.random.default_rng(31)
    sos = butter(2, [1400.0, 5200.0], btype="band", fs=sr, output="sos")
    click = sosfilt(sos, rng.normal(0.0, 1.0, n)) * _env(n, sr, 0.0003, 0.010)

    t = np.arange(n) / sr
    body = np.sin(2 * np.pi * 880.0 * t) * _env(n, sr, 0.001, 0.006) * 0.30

    out = click + body
    return out / (np.max(np.abs(out)) + 1e-9)


def clock_final(sr: int = SR, dur: float = 0.11) -> np.ndarray:
    """The last tick of a countdown — the same escapement, a fourth up.

    A countdown that ends on the same tick it has been making has no full stop,
    and the reveal then has to do the work of saying that time is up as well as
    saying what the answer was. One pitched tick at the end costs nothing and
    the beat lands on its own.
    """
    from scipy.signal import butter, sosfilt

    n = int(sr * dur)
    rng = np.random.default_rng(37)
    sos = butter(2, [1900.0, 6400.0], btype="band", fs=sr, output="sos")
    click = sosfilt(sos, rng.normal(0.0, 1.0, n)) * _env(n, sr, 0.0003, 0.012)

    t = np.arange(n) / sr
    body = np.sin(2 * np.pi * 1174.7 * t) * _env(n, sr, 0.001, 0.009) * 0.35

    out = click + body
    return out / (np.max(np.abs(out)) + 1e-9)


# Per-cue level against the narration peak. A single `gain` for everything was
# tried and cannot work: a transition covering a cut has to be heard over the
# bed, while an item tick has to sit under a syllable, and those are a factor of
# four apart.
LEVELS = {
    "cross": 1.00, "tick": 1.00,
    "whoosh": 0.85, "riser": 0.55, "impact": 0.95, "reveal": 0.34,
    # The drawn-beat cues (2026-09-10). `link` sits just above `reveal` — it is
    # still punctuation, not an event. `loop_close` and `limit` each fire once
    # per beat at the one structural moment, so they can carry like an impact.
    "link": 0.42, "loop_close": 0.60, "limit": 0.74,
    # A countdown tick is heard eight times in a row, and it is the only thing
    # in the mix for those eight seconds — **except that it is not, any more.**
    # These started at 0.18/0.30, set against silence and judged as nagging at
    # anything higher. Then the quiz gained a music bed, and under it the ticks
    # were inaudible: at 0.18 a tick lands ~0.04 of the narration peak, which
    # sits under a -32 LUFS bed rather than over it. Raised to carry over the
    # bed while staying below a struck mark, which is still the loudest cue in
    # the file. If the bed is ever removed from this format, these come back
    # down — the pair only makes sense together.
    "clock": 0.70, "clock_final": 0.95,
}


def mix(track: Path, out: Path, cues: list[tuple[float, str]],
        gain: float = 0.22) -> Path:
    """Lay sound effects over a finished narration track.

    `gain` is against the narration's own peak rather than full scale — a fixed
    absolute level is either inaudible under one voice profile or slapping over
    another, and the profiles differ by more than you would guess.
    """
    import soundfile as sf

    audio, sr = sf.read(str(track), always_2d=True, dtype="float32")
    peak = float(np.max(np.abs(audio))) or 1.0
    makers = {"cross": mark_cross, "tick": mark_tick, "whoosh": whoosh,
              "riser": riser, "impact": impact, "reveal": reveal,
              "link": link, "loop_close": loop_close, "limit": limit,
              "clock": clock, "clock_final": clock_final}

    for at, kind in cues:
        clip = makers[kind](sr) * peak * gain * LEVELS.get(kind, 1.0)
        i = int(at * sr)
        if i < 0:
            continue
        j = min(len(audio), i + len(clip))
        if j <= i:
            continue
        audio[i:j] += clip[:j - i, None]

    # Ceiling rather than hard clip: a mark landing on a stressed syllable can
    # push past 1.0, and clipping it is audible on exactly the beat meant to be
    # the satisfying one.
    top = float(np.max(np.abs(audio)))
    if top > 0.99:
        audio *= 0.99 / top

    sf.write(str(out), audio, sr)
    return out
