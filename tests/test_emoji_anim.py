"""Animated emoji: off changes nothing, on plays the right frame, a miss is
remembered, and a build never adds a credit line for them.

No network: a three-frame WebP written here stands in for Noto's file, and
the CDN is replaced when a test needs a 404.
"""

from __future__ import annotations

import urllib.error
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from PIL import Image, ImageDraw

from video_automation.core import emoji_anim
from video_automation.core.vertical import emoji_image


@pytest.fixture
def fake_noto(tmp_path, monkeypatch):
    """A 3-frame animation, 100ms each, whose ink grows frame to frame."""
    frames = []
    for k in range(3):
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        r = 20 + 15 * k
        ImageDraw.Draw(im).ellipse([64 - r, 64 - r, 64 + r, 64 + r],
                                   fill=(255, 80 * k, 0, 255))
        frames.append(im)
    p = tmp_path / "anim.webp"
    frames[0].save(p, save_all=True, append_images=frames[1:], duration=100,
                   loop=0, lossless=True)
    monkeypatch.setattr(emoji_anim, "DIR", tmp_path)
    monkeypatch.setattr(emoji_anim, "_clips", {})
    monkeypatch.setattr(emoji_anim, "fetch", lambda ch: p if ch == "🔥" else None)
    return p


def test_noto_file_names():
    assert emoji_anim.code("🔥") == "1f525"
    assert emoji_anim.code("❤️") == "2764"                  # VS16 dropped
    assert emoji_anim.code("👨‍💻") == "1f468_200d_1f4bb"     # ZWJ kept, joined


def test_off_is_the_static_glyph_exactly():
    assert not emoji_anim.active()
    a = np.asarray(emoji_image("🔥", 64))
    b = np.asarray(emoji_image("🔥", 64, t=1.23))
    assert np.array_equal(a, b)


def test_on_plays_the_frame_for_the_time(fake_noto):
    clip = emoji_anim.Clip(fake_noto)
    assert [clip.index(t) for t in (0.0, 0.15, 0.25, 0.31)] == [0, 1, 2, 0]
    # One crop box for every frame: the icon never changes size as it moves.
    assert len({f.size for f in clip.frames}) == 1
    with emoji_anim.enabled(True):
        a = np.asarray(emoji_image("🔥", 64, t=0.0))
        b = np.asarray(emoji_image("🔥", 64, t=0.21))
        still = np.asarray(emoji_image("🔑", 64, t=0.21))    # no animation
    assert a.shape == b.shape and not np.array_equal(a, b)
    assert np.array_equal(still, np.asarray(emoji_image("🔑", 64)))
    assert not emoji_anim.active()                           # restored after


def test_a_missing_animation_is_asked_for_once(tmp_path, monkeypatch):
    calls = []

    def urlopen(url, timeout=0):
        calls.append(url)
        raise urllib.error.HTTPError(url, 404, "nope", None, None)

    monkeypatch.setattr(emoji_anim, "DIR", tmp_path)
    monkeypatch.setattr(emoji_anim.urllib.request, "urlopen", urlopen)
    assert emoji_anim.fetch("💰") is None
    assert emoji_anim.fetch("💰") is None
    assert len(calls) == 1 and (tmp_path / "1f4b0.none").exists()


def test_animated_emoji_adds_no_credit_line(monkeypatch):
    # The editor's call (2026-11-05): no licence line for the icons, in a long
    # form's credits or anywhere else. `render_long` hands `meta` on untouched.
    from video_automation.longform import build
    seen = {}
    monkeypatch.setattr(build, "_render_long",
                        lambda *a, **kw: seen.update(kw) or {})
    meta = SimpleNamespace(credits=["Photo: someone"])
    build.render_long([], Path("out.mp4"), Path("work"), meta=meta,
                      animated_emoji=True)
    assert seen["meta"] is meta and meta.credits == ["Photo: someone"]
    assert not hasattr(emoji_anim, "CREDIT")
