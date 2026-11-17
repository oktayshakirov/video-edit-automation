"""`_pad_pause` puts a sentence gap in the pause, never inside the last word.

The shape that broke it (soft-flames-66-breathing Short, 2026-11-17):
"...even breaths." read by luna at 0.90 ends in a quiet voiceless /θ/, a loud
/s/, then the model's own long pause - which starts at the very edge of the
search window. The pause was judged on its clipped length and dropped, the
/θ/ won, and the silence went between "breath" and "s".
"""

from __future__ import annotations

import numpy as np

from video_automation.core import voiceover as vo

SR = vo.KOKORO_SR


def seg(seconds: float, rms: float, seed: int = 0) -> np.ndarray:
    n = int(seconds * SR)
    if rms == 0:
        return np.zeros(n, np.float32)
    x = np.random.default_rng(seed).standard_normal(n).astype(np.float32)
    return x * (rms / float(np.sqrt(np.mean(x ** 2))))


def breaths_then_pause() -> tuple[np.ndarray, float, float]:
    """Vowel, quiet /θ/, loud /s/, a long real pause, the next sentence.

    Returns the audio, where the /θ/ starts and where the /s/ ends."""
    parts = [seg(1.00, 0.10, 1),      # "...even brea-"
             seg(0.15, 0.008, 2),     # /θ/: under PAUSE_FLOOR, longer than MIN_PAUSE
             seg(0.16, 0.08, 3),      # /s/
             seg(1.50, 0.0),          # the model's own pause
             seg(0.80, 0.10, 4)]      # "Keep it low..."
    th = 1.00
    s_end = 1.00 + 0.15 + 0.16
    return np.concatenate(parts), th, s_end


def test_the_gap_never_lands_between_th_and_s():
    audio, th, s_end = breaths_then_pause()
    # The alignment estimate lands just before the /s/, as it did in the
    # shipped build, so the real pause starts at the window's far edge.
    at = s_end - vo.PAUSE_WIN + 0.01
    out, added, stop, resume = vo._pad_pause(audio, at, want=2.0)
    assert stop is not None and stop >= s_end - 0.02, (
        f"speech judged to stop at {stop:.3f}s, inside the word "
        f"(the /s/ ends at {s_end:.3f}s)")
    # Everything up to the end of the /s/ is untouched.
    n = int(s_end * SR)
    assert np.array_equal(out[:n], audio[:n])
    assert added > 0


def test_a_long_enough_model_pause_is_left_alone():
    audio, _, s_end = breaths_then_pause()
    out, added, stop, _ = vo._pad_pause(audio, s_end - vo.PAUSE_WIN + 0.01,
                                        want=0.55)
    assert added == 0.0 and len(out) == len(audio)
    assert stop >= s_end - 0.02


def test_a_stop_closure_alone_is_still_not_a_pause():
    """The original guard ("bro - ke"): a 40ms closure inside speech, no pause."""
    audio = np.concatenate([seg(0.6, 0.1, 5), seg(0.04, 0.0),
                            seg(0.6, 0.1, 6)])
    out, added, stop, _ = vo._pad_pause(audio, 0.62, want=0.5)
    assert added == 0.0 and stop is None and len(out) == len(audio)
