"""The per-site sound kits, and the one cue set no kit may touch.

The opener was softened once, on the reasoning that a hearing-sensitive
audience should not be hit with a transient. That was the wrong trade and the
user overruled it: a Short lives or dies in its first second, and an opener
that does not grab is an opener nobody hears the soft middle of either. This
file is what stops a future kit quietly taking it back.
"""

from __future__ import annotations

import hashlib

import numpy as np
import pytest
import soundfile as sf

from video_automation.core import sfx

HOOK = [(0.5, "hook_slam"), (1.2, "hook_glitch"), (1.6, "hook_pop"),
        (2.1, "hook_swish"), (2.6, "hook_swell")]
BODY = [(3.0, "impact"), (3.6, "drop"), (4.1, "reveal")]


@pytest.fixture
def bed(tmp_path):
    """A flat tone to lay cues over - `mix` works off the track's own peak,
    so it needs a track with one."""
    p = tmp_path / "bed.wav"
    sf.write(str(p), np.full((48000 * 6, 1), 0.2, dtype="float32"), 48000)
    return p


def _mix(bed, tmp_path, cues, kit, tag):
    out = tmp_path / f"{tag}.wav"
    sfx.mix(bed, out, cues, kit=kit)
    a, _ = sf.read(str(out), always_2d=True, dtype="float32")
    return hashlib.sha256(a.tobytes()).hexdigest(), a


def test_the_opener_is_the_same_sound_on_both_channels(bed, tmp_path):
    c, _ = _mix(bed, tmp_path, HOOK, "crypto", "c")
    t, _ = _mix(bed, tmp_path, HOOK, "tinnitus", "t")
    assert c == t


def test_no_kit_may_remap_an_exempt_cue():
    """Belt and braces: `mix` skips the substitution for these, but a kit that
    lists one is stating an intention this rule contradicts."""
    for name, kit in sfx.KITS.items():
        overlap = sfx.KIT_EXEMPT & set(kit)
        assert not overlap, f"{name} kit remaps exempt cue(s) {sorted(overlap)}"


def test_the_whole_hook_kit_is_exempt():
    """A hook cue added later must be added here too, or it gets softened on
    tinnitushelp.me the moment a kit names it."""
    hook_cues = {k for k in sfx.LEVELS if k.startswith("hook_")}
    assert hook_cues <= sfx.KIT_EXEMPT, sorted(hook_cues - sfx.KIT_EXEMPT)


def test_the_body_is_still_softened(bed, tmp_path):
    c, ca = _mix(bed, tmp_path, BODY, "crypto", "bc")
    t, ta = _mix(bed, tmp_path, BODY, "tinnitus", "bt")
    assert c != t
    # Quieter, not merely different - the kit gain has to actually apply.
    assert np.abs(ta - 0.2).sum() < np.abs(ca - 0.2).sum()


def test_crypto_is_byte_identical_to_no_kit_at_all(bed, tmp_path):
    """`KITS["crypto"]` is empty at gain 1.0, which is what keeps every
    shipped thecrypto.wiki video reproducible."""
    a, _ = _mix(bed, tmp_path, HOOK + BODY, "crypto", "k")
    b, _ = _mix(bed, tmp_path, HOOK + BODY, None, "n")
    assert a == b


def test_every_kit_names_a_real_cue():
    """A typo in a kit is silent: the cue is never substituted and nobody
    finds out until someone listens."""
    for name, kit in sfx.KITS.items():
        for src, dst in kit.items():
            assert src in sfx.LEVELS, f"{name}: unknown source cue {src!r}"
            assert dst in sfx.LEVELS, f"{name}: unknown target cue {dst!r}"


def test_every_kit_gain_is_defined():
    assert set(sfx.KITS) <= set(sfx.KIT_GAIN)
