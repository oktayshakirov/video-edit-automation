"""The read-along's paragraph finder picks scripted gaps, not the voice's own.

The trap it exists for: Kokoro leaves pauses inside a paragraph that are as
long as the shortest scripted gap between paragraphs, so a threshold either
misses boundaries or splits paragraphs. Synthetic audio with a decoy pause
inside each paragraph is enough to show the DP choosing by length and gap
rather than by "longest silence wins".
"""

from __future__ import annotations

import numpy as np

from video_automation.longform.readalong import KOKORO_SR, Part, find_parts


def _tone(s: float) -> np.ndarray:
    t = np.arange(int(s * KOKORO_SR)) / KOKORO_SR
    return 0.3 * np.sin(2 * np.pi * 220 * t).astype("float32")


def _quiet(s: float) -> np.ndarray:
    return np.zeros(int(s * KOKORO_SR), dtype="float32")


def test_scripted_gaps_beat_decoy_pauses():
    # (gap before, speech length, a decoy pause at this fraction of it)
    plan = [(1.5, 2.0, None), (1.3, 8.0, 0.4), (0.55, 6.0, 0.5),
            (1.0, 2.0, None), (0.55, 10.0, 0.3)]
    chunks, want, t = [], [], 0.0
    for gap, length, decoy in plan:
        chunks.append(_quiet(gap + 0.08 if t else gap))
        t += gap + (0.08 if t else 0)
        if decoy is None:
            chunks.append(_tone(length))
        else:
            # Same length as the shortest scripted gap: indistinguishable by
            # duration alone.
            a = length * decoy
            chunks += [_tone(a), _quiet(0.6), _tone(length - a - 0.6)]
        want.append((t, t + length))
        t += length
    chunks.append(_quiet(1.5))
    y = np.concatenate(chunks)

    # Text lengths in proportion to speech, as a real paragraph's would be.
    parts = [Part("x" * int(length * 15), gap) for gap, length, _ in plan]
    got = find_parts(y, parts, tail=1.5)

    assert len(got) == len(want)
    for (a, b), (wa, wb) in zip(got, want):
        assert abs(a - wa) < 0.05 and abs(b - wb) < 0.05
