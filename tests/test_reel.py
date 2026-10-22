"""The `reel` beat's dives into and out of a card (`beats/reel.py`)."""

from pathlib import Path

import pytest

from video_automation.core.brand import CRYPTO
from video_automation.core.frame import LANDSCAPE, VERTICAL
from video_automation.crypto.shots import Shot
from video_automation.longform.beats import BEATS
from video_automation.longform.beats.reel import link_reels

CLIP = (Path(__file__).resolve().parents[1]
        / "assets/stock/videos/digital-network-grid-gold-dark/28561594.mp4")


@pytest.mark.parametrize("frame", [LANDSCAPE, VERTICAL])
def test_enter_fills_the_frame_by_the_last_frame(frame):
    r = BEATS["reel"]([(None, "A"), (None, "B")], "", True,
                      brand=CRYPTO, frame=frame, reveals=[0.5, 2.0],
                      start=0.0, hold=4.0)
    cam, zoom, imm = r.camera(4.0 - 1 / 30)
    assert imm > 0.97 and zoom * r.card_w >= frame.w * 0.97
    assert zoom * r.card_h >= frame.h * 0.97
    assert abs(cam - r.pitch) < 2.0         # centred on the last card


def test_emerge_starts_inside_the_first_card():
    r = BEATS["reel"]([(None, "A"), (None, "B")], "", False, True,
                      brand=CRYPTO, reveals=[0.5, 2.0], start=0.0, hold=4.0)
    _, zoom, imm = r.camera(0.0)
    assert imm == pytest.approx(1.0) and zoom > r.fill
    assert r.camera(2.0)[2] == pytest.approx(0.0)


def _shot(**kw):
    sh = Shot(**kw)
    sh.start, sh.hold = 0.0, 3.0
    return sh


@pytest.mark.skipif(not CLIP.exists(), reason="stock cache not present")
def test_link_continues_the_same_clip_on_both_sides():
    prev = _shot(clip=CLIP)
    prev.clip_at = 1.0
    reel = _shot(graphic="reel",
                 payload=([(CLIP, "A"), (None, "B"), (CLIP, "C")], "", True, True))
    reel.hold = 6.0
    nxt = _shot(clip=CLIP)
    link_reels([prev, reel, nxt])
    assert prev.xfade == 0.0 and reel.xfade == 0.0
    items = reel.payload[0]
    assert items[0][2] == pytest.approx(4.0)     # prev's clip_at + hold
    assert nxt.clip_at == pytest.approx(6.0)     # card C's offset + reel hold


def test_link_leaves_a_plain_reel_alone():
    reel = _shot(graphic="reel", payload=([(None, "A")], ""))
    nxt = _shot(clip=CLIP)
    link_reels([reel, nxt])
    assert reel.xfade is None and nxt.clip_at == 0.0
