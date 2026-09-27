"""The narration cache key, and the bug that poisoned it.

**None of this synthesises speech.** The cache's value is proved by using it
in a real build; what is worth testing cheaply is the *key* - because a key
that collides serves one video another video's narration, and a key that is
too eager never hits at all. Both failures are silent.

The regression at the bottom is the real reason this file exists. The first
version of the cache named its hash `key`, and `build_narration_aligned`
already uses `key` as a loop variable when it shifts `stop_at` / `resume`
after a forced pad. The loop clobbered the hash with a chunk index, so an
entry was written as `2.wav` - a name that two unrelated scripts would both
compute. It was caught only because a parallel build wrote 49 seconds of a
completely different script under it.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from video_automation.core import voiceover as vo

SENT = [["A whale is a holder", "big enough to move a market."],
        ["But a wallet never tells you who is behind it."]]
GAPS = [0.8, 0.8]
BASE = dict(sentences=SENT, voice="af_heart", mood="melancholic", gaps=GAPS,
            tail=0.9, run_break=0.55, chunk_pad=None)


def key(**over):
    return vo._narration_key(**{**BASE, **over})


def test_the_key_is_stable_across_calls():
    assert key() == key()


def test_the_key_is_a_hex_digest():
    """The shape a purge can recognise. Anything else in the cache directory
    was written by a broken version and must not be trusted - see the module
    docstring."""
    assert re.fullmatch(r"[0-9a-f]{32}", key())


@pytest.mark.parametrize("field,value", [
    ("sentences", [["Different words entirely."]]),
    ("voice", "af_bella"),
    ("mood", "reflective"),
    ("gaps", [0.9, 0.8]),
    ("tail", 1.4),
    ("run_break", 0.7),
    ("chunk_pad", {1: 0.4}),
])
def test_every_input_that_changes_a_sample_changes_the_key(field, value):
    """A miss costs the synthesis we were going to do anyway. A false *hit*
    ships the wrong audio, so each of these has to be in the hash."""
    assert key(**{field: value}) != key()


def test_chunking_a_caption_differently_changes_the_key():
    """Same words, different caption split. The audio is one utterance either
    way, but the caption boundaries come back different - so it is a different
    cache entry."""
    assert key(sentences=[["A whale is a holder big enough to move a market."],
                          SENT[1]]) != key()


def test_the_model_identity_is_in_the_key():
    """A swapped checkpoint has to miss, or the cache serves the old voice
    forever."""
    ident = vo._model_ident()
    assert ident
    assert ident == vo._model_ident()


def test_the_voice_packages_are_in_the_model_identity():
    """**The regression.** Recreating the venv moved `kokoro-onnx` 0.5.0 ->
    0.6.1 and swapped `phonemizer-fork` for plain `phonemizer`; the same
    script then synthesised 20ms longer with different audio, while the
    `.onnx` file on disk was untouched. Keyed on the weights alone, the cache
    would have served the old environment's narration to the new one.
    """
    ident = vo._model_ident()
    for name in vo._VOICE_PACKAGES:
        assert f"{name}=" in ident, f"{name} missing from {ident}"
    # And the weights are still in there - the packages are an addition, not
    # a replacement.
    assert "weights=" in ident


def test_a_voice_package_change_changes_the_key(monkeypatch):
    """The same script under a different TTS stack is a different entry."""
    real = key()
    monkeypatch.setattr(vo, "_model_ident", lambda: "kokoro:pretend-upgraded")
    assert key() != real


def test_a_corrupt_entry_is_a_miss_not_a_crash(tmp_path, monkeypatch):
    """A half-written or hand-edited entry must never fail a build."""
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    k = "0" * 32
    (tmp_path / f"{k}.wav").write_bytes(b"not a wav")
    (tmp_path / f"{k}.json").write_text("{ truncated")
    assert vo._cache_load(k, tmp_path / "work") is None


def test_a_missing_entry_is_a_miss(tmp_path, monkeypatch):
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    assert vo._cache_load("1" * 32, tmp_path / "work") is None


def test_store_then_load_round_trips(tmp_path, monkeypatch):
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    src = tmp_path / "narration.wav"
    src.write_bytes(b"RIFF....WAVEfmt ")
    caps = [vo.Caption("A whale is a holder", 0.0, 1.8, 1.6),
            vo.Caption("big enough to move a market.", 1.8, 3.9, 3.7)]

    vo._cache_store("a" * 32, src, caps, 4.8)
    work = tmp_path / "work"
    got = vo._cache_load("a" * 32, work)

    assert got is not None
    track, loaded, total = got
    assert track == work / "narration.wav"
    assert track.read_bytes() == src.read_bytes()
    assert total == 4.8
    # `speech_end` is the one field a naive round trip loses, and the karaoke
    # captions are the consumer that needs it.
    assert [(c.text, c.start, c.end, c.speech_end) for c in loaded] == \
           [(c.text, c.start, c.end, c.speech_end) for c in caps]


def test_a_store_leaves_no_partial_file(tmp_path, monkeypatch):
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    src = tmp_path / "n.wav"
    src.write_bytes(b"x" * 64)
    vo._cache_store("b" * 32, src, [], 1.0)
    assert not list(tmp_path.glob("*.part"))


def test_the_cache_key_is_not_shadowed_by_a_loop_variable():
    """**The regression.** `build_narration_aligned` uses `key` as a loop
    variable over `stop_at`; the cache's own hash must not share that name, or
    it is overwritten with a chunk index and entries collide across scripts.

    Asserted on the source rather than by running a synthesis, because
    reproducing it for real means a full build with a forced pad in it.
    """
    src = Path(vo.__file__).read_text(encoding="utf-8")
    body = src[src.index("def build_narration_aligned("):]
    body = body[:body.index("\ndef ", 1)]

    assert "cache_key = _narration_key(" in body
    assert "_cache_store(cache_key," in body
    assert "_cache_load(cache_key," in body
    # The loop that did the clobbering is still there and still uses `key`;
    # that is fine, and this test is what keeps the two names apart.
    assert "for key in stop_at" in body
    assert "_cache_store(key," not in body


# --- eviction --------------------------------------------------------------
#
# A long form's narration is 30-40MB of wav and every re-cut that changes a
# word stores another. Nothing else would ever delete one, in a directory
# nobody looks at.

def _entry(d, key, size, mtime):
    (d / f"{key}.wav").write_bytes(b"\0" * size)
    (d / f"{key}.json").write_text('{"total": 1.0, "captions": []}')
    for suffix in (".wav", ".json"):
        import os
        os.utime(d / f"{key}{suffix}", (mtime, mtime))


def test_prune_is_a_no_op_under_the_cap(tmp_path, monkeypatch):
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    _entry(tmp_path, "a" * 32, 1000, 1000)
    assert vo._prune(limit=10_000) == 0
    assert (tmp_path / f"{'a' * 32}.wav").exists()


def test_prune_evicts_least_recently_used_first(tmp_path, monkeypatch):
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    _entry(tmp_path, "a" * 32, 1000, 3000)      # newest
    _entry(tmp_path, "b" * 32, 1000, 2000)
    _entry(tmp_path, "c" * 32, 1000, 1000)      # oldest

    # Room for roughly two entries (each is 1000 + a small json).
    vo._prune(limit=2200)

    assert (tmp_path / f"{'a' * 32}.wav").exists()
    assert (tmp_path / f"{'b' * 32}.wav").exists()
    assert not (tmp_path / f"{'c' * 32}.wav").exists()
    # The metadata goes with it - a stranded .json is a hit on missing audio.
    assert not (tmp_path / f"{'c' * 32}.json").exists()


def test_a_hit_makes_an_entry_recently_used(tmp_path, monkeypatch):
    """Eviction is by last *use*, not by age: the script being re-cut all
    afternoon has to survive, however old the entry is."""
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    _entry(tmp_path, "a" * 32, 1000, 3000)
    _entry(tmp_path, "o" * 32, 1000, 1000)      # oldest, but about to be used

    assert vo._cache_load("o" * 32, tmp_path / "work") is not None
    vo._prune(limit=2200)

    assert (tmp_path / f"{'o' * 32}.wav").exists(), "a touched entry was evicted"


def test_prune_survives_a_stranded_json(tmp_path, monkeypatch):
    monkeypatch.setattr(vo, "NARRATION_CACHE", tmp_path)
    (tmp_path / f"{'d' * 32}.json").write_text("{}")
    assert vo._prune(limit=0) == 0               # no wav, nothing to free
