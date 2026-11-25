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


@pytest.mark.parametrize("kind,fields", [
    ("post", {"name": "A", "text": "one [two three] four"}),
    ("headline", {"source": "S", "headline": "one [two] three"}),
    ("tx", {"rows": [("*Value", "10 BTC"), ("For", "x")]}),
])
def test_post_highlighter_every_frame(kind, fields):
    """Every sweep fraction draws - the first sliver once had x1 < x0."""
    b = BEATS["post"](kind, fields, brand=CRYPTO, reveals=[0.2, 1.0],
                      start=0.0, hold=3.0)
    for i in range(31):
        b.draw(i / 30)


def test_a_path_starts_on_its_first_card_and_dives_into_its_last():
    """A chapter's way in (2026-11-23): the camera sits on the last
    chapter's window, travels to the next on the word, and dives into it -
    not into the strip's last card."""
    items = [(None, str(k)) for k in range(5)]
    r = BEATS["reel"](items, "", True, False, [1, 2], brand=CRYPTO,
                      reveals=[0.0, 2.0], start=0.0, hold=4.0)
    assert abs(r.camera(1.5)[0] - r.pitch) < 20         # on card 1, swaying
    cam, _, imm = r.camera(4.0 - 1 / 30)
    assert imm > 0.97 and abs(cam - 2 * r.pitch) < 2.0  # inside card 2
    from video_automation.longform.beats import item_count
    assert item_count("reel", (items, "", True, False, [1, 2])) == 2


def test_a_long_way_back_arrives_on_the_card():
    items = [(None, str(k)) for k in range(5)]
    r = BEATS["reel"](items, "", False, False, [4, 0], brand=CRYPTO,
                      reveals=[0.0, 1.5], start=0.0, hold=4.0)
    assert abs(r.camera(1.2)[0] - 4 * r.pitch) < 20
    assert abs(r.camera(3.5)[0]) < 20


def test_link_reels_keeps_the_path():
    sh = _shot(graphic="reel", payload=([(None, "A"), (None, "B"), (None, "C")],
                                        "", True, False, [0, 1]))
    nxt = _shot(clip=CLIP)
    link_reels([sh, nxt])
    assert sh.payload[4] == [0, 1]


def test_an_open_window_starts_on_its_own_card_with_its_neighbours_in_view():
    """A chapter's way in (2026-11-24): no travel from the last window - on
    its own card from the first frame, zoomed out so the covered window and
    its check show beside it, then the dive."""
    items = [(None, str(k)) for k in range(5)]
    r = BEATS["reel"](items, "", True, False, [2], {"open": 0.78}, brand=CRYPTO,
                      reveals=[0.0, 1.2], start=0.0, hold=4.0)
    cam, zoom, _ = r.camera(0.0)
    assert abs(cam - 2 * r.pitch) < 2.0 and zoom == pytest.approx(0.78)
    # The card before it is on screen at the opening zoom.
    left = r.frame.w / 2 + (r.pitch - cam) * zoom
    assert left > 0
    cam, _, imm = r.camera(4.0 - 1 / 30)
    assert imm > 0.97 and abs(cam - 2 * r.pitch) < 2.0


def test_a_stop_with_a_long_lead_arrives_on_its_word():
    """The slop strip's template (2026-11-24): its travel runs in the pause
    before "and the same template", so the card is there as it is said."""
    items = [(None, str(k)) for k in range(3)]
    r = BEATS["reel"](items, "", False, False, [0, 1, 2],
                      {"lead": [0.1, 0.1, 0.8]}, brand=CRYPTO,
                      reveals=[0.0, 1.5, 4.0], start=0.0, hold=6.0)
    assert abs(r.camera(4.2)[0] - 2 * r.pitch) < 0.1 * r.pitch    # nearly there
    assert abs(r.camera(1.6)[0] - 1 * r.pitch) > 0.5 * r.pitch     # default lead: still far


def test_a_reels_sounds_follow_its_path():
    """A pan when the camera leaves, at its lead; a tick when a card is first
    named; nothing on a stop that stays on the same card."""
    from video_automation.longform.beats.reel import sound_cues
    sh = _shot(graphic="reel", payload=([(None, "A"), (None, "B")], "", False, False,
                                        [0, 1, 1], {"lead": [0.1, 0.6, 0.1]}))
    sh.reveals = [0.0, 1.0, 2.0]
    cues = sound_cues(sh)
    assert [k for _, k in cues].count("pan") == 1
    assert [k for _, k in cues].count("reveal") == 2
    assert any(k == "pan" and abs(t - (1.0 - 0.6 - 0.02)) < 1e-6 for t, k in cues)


def test_labels_over_the_footage_draw_no_pill(tmp_path):
    """The overcorrection's labels as plain type on the footage (2026-11-24):
    the frame differs from the pill's under the card."""
    items = [(CLIP, "Quantum computers")]
    kw = dict(brand=CRYPTO, reveals=[0.0], start=0.0, hold=2.0)
    over = BEATS["reel"](items, "", False, False, None, {"labels": "over"}, **kw)
    pill = BEATS["reel"](items, "", False, False, None, **kw)
    import numpy as np
    a, b = np.asarray(over.draw(0.9)), np.asarray(pill.draw(0.9))
    H = a.shape[0]
    y = int(H * 0.5 + pill.card_h / 2)          # where the pill sits
    band = slice(y - 10, y + 10)
    assert np.abs(a[band].astype(int) - b[band].astype(int)).mean() > 3


def test_link_reels_keeps_the_options():
    sh = _shot(graphic="reel", payload=([(None, "A"), (None, "B")], "", True, False,
                                        [1], {"open": 0.78}))
    link_reels([sh, _shot(clip=CLIP)])
    assert sh.payload[5] == {"open": 0.78}
