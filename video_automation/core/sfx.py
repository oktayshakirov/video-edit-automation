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


RISER_DUR = 2.0         # the cinematic riser, ending on the card's first frame


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


def tension(sr: int = SR, dur: float = RISER_DUR) -> np.ndarray:
    """The cinematic riser: a big synth swell climbing from low to high.

    Second version (2026-10-20). The first was a high Shepard shimmer, and the
    user's note was that the sound on trailer-style channels starts *low* and
    climbs - the whole register in one gesture. So this is the classic trailer
    riser, built from three layers:

    * **Three detuned sawtooth voices gliding four octaves**, 55 Hz to 880 Hz,
      exponentially, so most of the climb happens late. They are additive
      (band-limited harmonics), so the top of the glide does not alias.
    * **A low-pass that opens with the pitch**, from a few hundred Hz to the
      top of the spectrum. Applied per harmonic as a smooth roll-off rather
      than by a moving IIR, which would ring. The opening filter is what makes
      it read as "rising into something" rather than as a pitch bend.
    * **Noise swelling under it**, its colour brightening with the filter, and
      a sub layer that holds the low end so the start has weight.

    It crescendoes and **stops dead** on the cut - no tail - so the card's
    impact lands on silence.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    p = t / dur
    rng = np.random.default_rng(43)

    glide = p ** 1.6
    f0 = 55.0 * 2.0 ** (4.0 * glide)
    cutoff = 260.0 * 2.0 ** (5.2 * glide)               # ~260 Hz -> ~9.5 kHz

    voices = np.zeros(n)
    for detune, ph in ((1.0, 0.0), (1.008, 1.1), (0.993, 2.3)):
        f = f0 * detune
        phase = 2 * np.pi * np.cumsum(f) / sr + ph
        for k in range(1, 41):
            fk = f * k
            # A smooth 4th-order low-pass on each partial, and silence above
            # Nyquist rather than a fold-back.
            amp = (1.0 / k) / (1.0 + (fk / cutoff) ** 4)
            amp = np.where(fk < sr / 2 - 500, amp, 0.0)
            voices += amp * np.sin(k * phase)
    voices /= np.max(np.abs(voices)) + 1e-9

    # Noise, coloured by a one-pole low-pass whose cutoff tracks the filter.
    white = rng.normal(0.0, 1.0, n)
    coef = np.exp(-2 * np.pi * np.minimum(cutoff * 1.4, sr / 2.2) / sr)
    noise = np.empty(n)
    acc = 0.0
    for i in range(n):
        acc = (1.0 - coef[i]) * white[i] + coef[i] * acc
        noise[i] = acc
    noise /= np.max(np.abs(noise)) + 1e-9

    sub = np.sin(2 * np.pi * np.cumsum(f0 * 0.5) / sr) * (1.0 - glide) * 0.6

    out = (voices * 0.85 + noise * 0.45 * p + sub) * (0.08 + 0.92 * p ** 1.8)
    tail = int(sr * 0.010)
    out[-tail:] *= np.linspace(1.0, 0.0, tail)
    return out / (np.max(np.abs(out)) + 1e-9)


def tv_off(sr: int = SR, dur: float = 0.45) -> np.ndarray:
    """A CRT switching off: a click, then a tone falling away fast.

    For `overlay.TvOff`, the video's last half second. The click is the
    relay; the falling sine is the flyback whine collapsing with the picture.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    p = t / dur
    f = 1400.0 * (60.0 / 1400.0) ** (p ** 0.6)
    tone = np.sin(2 * np.pi * np.cumsum(f) / sr) * np.exp(-t / 0.16)
    out = 0.7 * tone + 0.6 * _noise_transient(n, sr, 0.004)
    return out / (np.max(np.abs(out)) + 1e-9)


def tv_static(sr: int = SR, dur: float = 0.36, soft: bool = False) -> np.ndarray:
    """Analog snow for the `static` cut: band-limited hiss plus crackle,
    swelling to the cut and gone after it. `soft` is the tinnitus kit's: lower
    and darker, no crackle."""
    from scipy.signal import butter, sosfilt
    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(37)
    lo, hi = (300.0, 2500.0) if soft else (900.0, 7500.0)
    sos = butter(2, [lo, hi], btype="band", fs=sr, output="sos")
    hiss = sosfilt(sos, rng.normal(0.0, 1.0, n))
    hiss /= np.max(np.abs(hiss)) + 1e-9
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    out = hiss * env
    if not soft:
        crack = np.zeros(n)
        idx = rng.integers(0, n, 40)
        crack[idx] = rng.uniform(-1, 1, 40)
        out += 0.8 * np.convolve(crack, np.exp(-np.arange(60) / 8.0))[:n] * env
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
    "tension": 0.62, "riser_soft": 0.55,
    # The file sounds, peak-normalised before these apply.
    "chapter_riser": 0.70, "title_intro": 0.80, "title_flashback": 0.70,
    "notification": 0.55, "tv_off": 0.55,
    # The special cuts: heard, but under the voice - they mark a cut, they
    # do not interrupt the sentence on either side of it.
    "tv_static": 0.42, "tv_static_soft": 0.30, "glitch_cut": 0.32,
    # The reel's camera move: a whoosh, but a quiet one - it fires per card.
    "pan": 0.40,
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
    # The hook kit. The slam is the one sound allowed to be the loudest thing
    # in the first second; the glitches are texture and sit well under it.
    "hook_slam": 1.10, "hook_glitch": 0.30, "hook_swell": 0.55,
    "hook_pop": 0.80, "hook_swish": 0.45,
    # Typed titles (2026-10-20). Twenty a second under a spoken line, so they
    # sit at texture level - under a `reveal`, which happens once.
    "key0": 0.36, "key1": 0.36, "key2": 0.36, "key3": 0.36,
}


# --------------------------------------------------------------------------
# The opening hook's own kit (2026-09-21). Designed as one set so the hit,
# the glitches, the swell and the pop sound like one piece of sound design
# rather than five utility cues. See `longform.overlay.HookOverlay`.
# --------------------------------------------------------------------------

def _bitcrush(x: np.ndarray, hold: int = 6, levels: int = 12) -> np.ndarray:
    """Sample-and-hold plus quantising: the digital texture of a glitch."""
    held = np.repeat(x[::hold], hold)[:len(x)]
    return np.round(held * levels) / levels


def hook_slam(sr: int = SR, dur: float = 0.95) -> np.ndarray:
    """The cut in: an 808-style drop with a punch on the front and air on top.

    The sub sweeps 110 -> 42 Hz, which reads as weight through a phone
    speaker's harmonics and as a proper drop on headphones. The punch is
    low-passed noise so it thuds rather than hisses.
    """
    from scipy.signal import butter, sosfilt
    n = int(sr * dur)
    t = np.arange(n) / sr
    f = 42.0 + 68.0 * np.exp(-t / 0.09)
    sub = np.sin(2 * np.pi * np.cumsum(f) / sr) * _env(n, sr, 0.002, 0.30)
    rng = np.random.default_rng(31)
    punch = sosfilt(butter(2, 2500, btype="low", fs=sr, output="sos"),
                    rng.normal(0, 1, n)) * _env(n, sr, 0.0005, 0.035)
    air = sosfilt(butter(2, 6000, btype="high", fs=sr, output="sos"),
                  rng.normal(0, 1, n)) * _env(n, sr, 0.01, 0.25)
    out = sub + punch * 0.9 + air * 0.12
    return out / (np.max(np.abs(out)) + 1e-9)


def hook_glitch(sr: int = SR, dur: float = 0.09) -> np.ndarray:
    """A tiny digital blip for the headline tearing sideways. Short and
    mid-high so it sits between the voice's syllables rather than on them."""
    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(37)
    sq = np.sign(np.sin(2 * np.pi * 1480.0 * t)) * 0.35
    out = _bitcrush(sq + rng.normal(0, 1, n) * 0.6, hold=9, levels=6)
    gate = (np.sin(2 * np.pi * 55.0 * t) > -0.2).astype(float)   # stutter
    out = out * gate * _env(n, sr, 0.001, 0.035)
    return out / (np.max(np.abs(out)) + 1e-9)


def hook_swell(sr: int = SR, dur: float = 1.0) -> np.ndarray:
    """A reverse cymbal: bright noise swelling exponentially and cut dead at
    the end, so the reveal lands in the gap the cut leaves."""
    from scipy.signal import butter, sosfilt
    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(41)
    hiss = sosfilt(butter(2, 3200, btype="high", fs=sr, output="sos"),
                   rng.normal(0, 1, n))
    shimmer = sum(np.sin(2 * np.pi * f * t) * 0.12 for f in (4186.0, 5274.0, 6272.0))
    env = (np.exp(4.2 * t / dur) - 1) / (np.exp(4.2) - 1)
    out = (hiss + shimmer) * env
    k = int(sr * 0.006)
    out[-k:] *= np.linspace(1, 0, k)          # hard cut, no click
    return out / (np.max(np.abs(out)) + 1e-9)


def hook_pop(sr: int = SR, dur: float = 0.75) -> np.ndarray:
    """The reveal: a 50 ms glitch resolving into a bright two-note chime.

    E6 and B6, a fifth apart, each doubled a few cents sharp so the tone
    shimmers instead of beeping; a soft thump underneath gives it body.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(43)
    g = int(sr * 0.05)
    glitch = np.zeros(n)
    glitch[:g] = _bitcrush(rng.normal(0, 1, g), hold=7, levels=5) * np.linspace(1, 0.2, g)
    chime = np.zeros(n)
    for f, a, dly in ((1318.5, 1.0, 0.035), (1975.5, 0.7, 0.075)):
        k = int(sr * dly)
        tt = t[:n - k]
        tone = (np.sin(2 * np.pi * f * tt) + np.sin(2 * np.pi * f * 1.004 * tt)) * 0.5
        chime[k:] += a * tone * _env(n - k, sr, 0.002, 0.22)
    thump = np.sin(2 * np.pi * 92.0 * t) * _env(n, sr, 0.001, 0.06)
    out = glitch * 0.45 + chime + thump * 0.6
    return out / (np.max(np.abs(out)) + 1e-9)


def hook_swish(sr: int = SR, dur: float = 0.38) -> np.ndarray:
    """The exit: a short, light upward swish - a smaller cousin of `whoosh`."""
    from scipy.signal import butter, sosfilt
    out = sosfilt(butter(2, 700, btype="high", fs=sr, output="sos"), whoosh(sr, dur))
    return out / (np.max(np.abs(out)) + 1e-9)


# --------------------------------------------------------------------------
# Sounds from files (2026-10-21). The user supplied these three after two
# synthesized risers missed what they meant. They are third-party library
# sounds, so like the music bed they live in `assets/brand/sfx/` and are
# gitignored - the repo is public. Each has a synthesized stand-in, used
# automatically when the file is missing.
#
# The anchor is the moment in the file that lands on the cue's time,
# measured on the files with a 0.1s RMS envelope:
#
# * chapter-riser.mp3 (3.84s) climbs to a hard stop at 3.75s - that stop
#   lands on the chapter card's first frame.
# * title-intro.mp3 (7.68s) has 0.2s of silence, a swell peaking at 1.3s as
#   the title's letters resolve, and a second swell and tail under the hold.
# * title-flashback.mp3 (2.04s) peaks at 0.83s - placed on the title's exit.
# --------------------------------------------------------------------------

SFX_DIR = Path(__file__).resolve().parents[2] / "assets/brand/sfx"

FILE_SFX = {
    # cue: (file, anchor seconds, synthesized stand-in)
    "chapter_riser": ("chapter-riser.mp3", 3.75, "tension"),
    "title_intro": ("title-intro.mp3", 0.20, "impact"),
    "title_flashback": ("title-flashback.mp3", 0.83, "whoosh"),
    # A two-note chime, its first note at 0.05s - the disclaimer notice.
    "notification": ("notification.mp3", 0.05, "reveal"),
}

# Anchors for the synthesized sounds that do not start on their moment.
# **Not `whoosh`**: every existing whoosh cue is timed as its start, and
# anchoring it would shift every transition in every video.
ANCHOR = {"tension": RISER_DUR, "riser_soft": RISER_DUR}

_FILE_CACHE: dict = {}


def _file_clip(kind: str, sr: int) -> "np.ndarray | None":
    """A file cue decoded to mono at `sr`, peak-normalised, or None."""
    key = (kind, sr)
    if key not in _FILE_CACHE:
        import subprocess
        path = SFX_DIR / FILE_SFX[kind][0]
        clip = None
        if path.exists():
            raw = subprocess.run(
                ["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1",
                 "-ar", str(sr), "-f", "f32le", "-"],
                capture_output=True, check=True).stdout
            x = np.frombuffer(raw, np.float32).astype(np.float64)
            clip = x / (np.max(np.abs(x)) + 1e-9)
        _FILE_CACHE[key] = clip
    return _FILE_CACHE[key]


def mix(track: Path, out: Path, cues: list[tuple[float, str]],
        gain: float = 0.22, kit: str | None = None) -> Path:
    """Lay sound effects over a finished narration track.

    `gain` is against the narration's own peak rather than full scale — a fixed
    absolute level is either inaudible under one voice profile or slapping over
    another, and the profiles differ by more than you would guess.

    `kit` names a per-site sound kit in `KITS`, which remaps cue names before
    they are rendered and scales the whole lot by `KIT_GAIN`. Left None, every
    caller renders byte-identically to what it did before kits existed — which
    is what keeps the shipped videos reproducible.
    """
    sub = KITS.get(kit or "", {})
    kit_gain = KIT_GAIN.get(kit or "", 1.0)
    import soundfile as sf

    audio, sr = sf.read(str(track), always_2d=True, dtype="float32")
    peak = float(np.max(np.abs(audio))) or 1.0
    makers = {"cross": mark_cross, "tick": mark_tick, "whoosh": whoosh,
              "riser": riser, "impact": impact, "reveal": reveal,
              "tension": tension, "tv_off": tv_off,
              "tv_static": tv_static,
              "tv_static_soft": lambda sr: tv_static(sr, soft=True),
              "glitch_cut": hook_glitch,
              "pan": lambda sr: whoosh(sr, dur=0.48),
              "riser_soft": lambda sr: riser(sr, RISER_DUR),
              "link": link, "loop_close": loop_close, "limit": limit,
              "clock": clock, "clock_final": clock_final,
              "hook_slam": hook_slam, "hook_glitch": hook_glitch,
              "hook_swell": hook_swell, "hook_pop": hook_pop,
              "hook_swish": hook_swish, **_MAKERS_EXTRA}

    for at, kind in cues:
        # An exempt cue takes neither the remap nor the kit's level - the
        # opener is the same sound on both channels. See `KIT_EXEMPT`.
        if kind in KIT_EXEMPT:
            g = gain
        else:
            kind, g = sub.get(kind, kind), gain * kit_gain
        # A file cue swaps to its synthesized stand-in when the file is not
        # on this machine - the sounds are licensed and stay out of git.
        if kind in FILE_SFX and _file_clip(kind, sr) is None:
            kind = FILE_SFX[kind][2]
        if kind in FILE_SFX:
            raw = _file_clip(kind, sr)
            anchor = FILE_SFX[kind][1]
        else:
            raw, anchor = makers[kind](sr), ANCHOR.get(kind, 0.0)
        clip = raw * peak * g * LEVELS.get(kind, 1.0)
        # `at` is when the clip's anchor lands, not when the clip starts. A
        # riser that must end on a card starts before it; near the top of the
        # timeline its front is trimmed rather than the cue dropped.
        i = int(round((at - anchor) * sr))
        if i < 0:
            clip, i = clip[-i:], 0
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


# --------------------------------------------------------------------------
# The new beats' own cues, and one sound kit per site (2026-09-25).
# --------------------------------------------------------------------------

def sweep(sr: int = SR, dur: float = 1.30) -> np.ndarray:
    """A quiet rising band under a line drawing itself across a chart.

    Unlike every other cue in this file this one is not an *event* - it is a
    sustained bed lasting as long as the draw, so the line has something under
    it for the whole travel rather than a tick at the start. Noise, band-passed
    by a moving filter and rising a fifth over its length, so it resolves
    upward whichever direction the data goes. Kept very dull on purpose: a
    bright sweep under a chart reads as a sci-fi interface.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    q = t / dur
    noise = np.random.default_rng(7).standard_normal(n)
    # A one-pole band-pass swept by hand, which is enough at this level.
    centre = 380.0 * (1.5 ** q)
    phase = np.cumsum(2 * np.pi * centre / sr)
    band = noise * np.sin(phase) * 0.6 + np.sin(phase) * 0.12
    env = np.minimum(q / 0.18, 1.0) * np.minimum((1.0 - q) / 0.24, 1.0)
    out = band * np.clip(env, 0.0, 1.0)
    return out / (np.max(np.abs(out)) + 1e-9)


def drop(sr: int = SR, dur: float = 0.34) -> np.ndarray:
    """A pin landing: a short pitched knock with a fast downward bend.

    The bend is what makes it read as something *arriving* rather than as a
    generic click - a fixed-pitch knock repeated five times across a map is
    the typewriter problem `reveal` already documents.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    f = 520.0 * np.exp(-6.0 * t)          # 520 Hz down to ~80 over the tail
    body = np.sin(2 * np.pi * np.cumsum(f) / sr) * _env(n, sr, 0.001, 0.055)
    out = body + 0.30 * _noise_transient(n, sr, 0.004)
    return out / (np.max(np.abs(out)) + 1e-9)


def count(sr: int = SR, dur: float = 0.05) -> np.ndarray:
    """A hair-thin click for a digit rolling in a counting `stat`.

    Fires many times a second, so it is barely a sound at all - almost pure
    transient with one high partial. It exists because a number racing upward
    in silence looks like a rendering artifact and the same number with a
    texture under it looks like a machine working.
    """
    n = int(sr * dur)
    t = np.arange(n) / sr
    body = np.sin(2 * np.pi * 2093.0 * t) * _env(n, sr, 0.0004, 0.006)
    out = body + 0.45 * _noise_transient(n, sr, 0.0015)
    return out / (np.max(np.abs(out)) + 1e-9)


LEVELS.update({"sweep": 0.30, "drop": 0.62, "count": 0.20})

def key(sr: int = SR, dur: float = 0.055, variant: int = 0) -> np.ndarray:
    """One digital keystroke, for a title typing itself out (`typewriter`).

    A soft tick rather than a mechanical clack: a bright, very short pitched
    body over a high-passed noise snap, with a faint low thock under it so it
    has some weight on a phone speaker. It fires once per character, twenty
    times a second, so the decay is the whole design - anything that rings
    past the next keystroke smears the train into a buzz.

    Four variants a few semitones apart, cycled by the cue list, because one
    identical sample repeated thirty times is audibly a loop.
    """
    from scipy.signal import butter, sosfilt

    n = int(sr * dur)
    t = np.arange(n) / sr
    rng = np.random.default_rng(31 + variant)
    f = 2350.0 * (1.0, 1.12, 0.94, 1.06)[variant % 4]

    sos = butter(2, 3200, btype="high", fs=sr, output="sos")
    snap = sosfilt(sos, rng.normal(0.0, 1.0, n)) * _env(n, sr, 0.0001, 0.0025)
    body = np.sin(2 * np.pi * f * t) * _env(n, sr, 0.0003, 0.006)
    thock = np.sin(2 * np.pi * 410.0 * t) * _env(n, sr, 0.0005, 0.010)
    out = 0.9 * snap + 0.55 * body + 0.35 * thock
    return out / (np.max(np.abs(out)) + 1e-9)


_MAKERS_EXTRA = {"sweep": sweep, "drop": drop, "count": count,
                 **{f"key{i}": (lambda sr, i=i: key(sr, variant=i))
                    for i in range(4)}}


# One kit per site. A cue name is looked up here first, so a script and a beat
# ask for "impact" and each channel gets its own idea of what that is.
#
# **This is not a style preference, it is an audience one.** thecrypto.wiki's
# viewer is watching a market explainer and a bitcrushed slam is the genre's
# own punctuation. tinnitushelp.me's viewer has a hearing condition, and a
# meaningful share of them have hyperacusis - a transient that slams is
# actively unpleasant for the exact people the channel is for. The tinnitus
# kit therefore has **no slam, no glitch and no bitcrushing anywhere in it**:
# every hard cue is remapped onto the swell, the soft pop or the reveal tick,
# and the whole kit is pulled down by `KIT_GAIN`.
KITS = {
    "crypto": {},                       # the shipped sound, unchanged
    "tinnitus": {
        "impact": "loop_close",
        # **No high tension riser for this audience.** A sustained, rising
        # high tone is close to what a tinnitus listener is trying not to
        # hear; the old soft noise riser stays here.
        "tension": "riser_soft",
        # The special cuts keep their picture on both channels, but this kit
        # takes the crackle out of the static and the bitcrush off the glitch.
        "tv_static": "tv_static_soft",
        "glitch_cut": "reveal",
        "drop": "link",
        # A whoosh is broadband noise sweeping - it is the one transition
        # sound that is genuinely fine here, and softening it would leave the
        # channel with no transition sound at all.
    },
}

# The whole kit's level against the shipped default, per site.
KIT_GAIN = {"crypto": 1.0, "tinnitus": 0.72}

# **The opening hook is exempt from the kit, on every channel.** The first
# version of this softened the hook too - the slam became a swell, the glitch
# became a reveal tick, and the whole thing came down to 0.72 - on the
# reasoning that a hearing-sensitive audience should not be hit with a
# transient. The user's call is that the opener is the wrong place to spend
# that: a Short lives or dies in its first second, and an opener that does not
# grab is an opener nobody hears the soft middle of either.
#
# So the hook kit passes through untouched and at full level on both sites,
# and the softening applies to everything after it - the chapter impacts, the
# map pins, the body cues. That is the part a viewer sits inside for three
# minutes, and it is where the difference actually accumulates.
#
# `hook_swish` and `hook_swell` are in here as themselves: they were never
# remapped, but a future kit must not quietly capture them either.
KIT_EXEMPT = frozenset({"hook_slam", "hook_glitch", "hook_pop", "hook_swish",
                        "hook_swell"})
