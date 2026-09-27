"""The navigation overlays, and the cue collision they sit next to.

`_chrome` is derived entirely from what `lay_out` already returned, which is
the design: a script that adds a section gets the extra tick and the recounted
cards for free. The tests here are about the edges of that derivation - the
opening section that has a chapter entry but no card, the video too short to
have a spine worth drawing - plus the one rule that is easy to regress:
a chapter card leaving on a `whip` must not fire two whooshes 0.14s apart.
"""

from __future__ import annotations

import pytest
from PIL import Image

from video_automation.core import transitions
from video_automation.core.brand import CRYPTO, TINNITUS
from video_automation.core.frame import LANDSCAPE as F
from video_automation.crypto.shots import Shot
from video_automation.longform import chrome
from video_automation.longform.build import _chrome, _cues

TOTAL = 150.0
CHAPTERS = [(0.0, "Opening"), (31.0, "Two"), (78.0, "Three"), (120.0, "Four")]


def card(at, title="A turn", **kw):
    return Shot(graphic="chapter", payload=(title, ""), start=at, hold=3.4, **kw)


def beat(at, hold=9.0, **kw):
    return Shot(graphic="stat", payload=("9", "", ""), start=at, hold=hold, **kw)


SHOTS = [beat(0.0, 31.0), card(31.0), beat(35.0), card(78.0), card(120.0)]


def test_it_builds_one_bar_and_one_count_per_card():
    ovs = _chrome(True, CHAPTERS, SHOTS, TOTAL, CRYPTO, F)
    assert sum(isinstance(o, chrome.ProgressBar) for o in ovs) == 1
    assert sum(isinstance(o, chrome.ChapterCount) for o in ovs) == 3


def test_the_count_follows_the_cards_not_the_chapter_list():
    """The opening section takes `card=False`, so it has a chapter entry and
    nothing on screen to annotate. Counting the chapter list instead would
    label the first visible card "2 of 4" when it is the first one seen."""
    counts = [(o.index, o.count) for o in
              _chrome(True, CHAPTERS, SHOTS, TOTAL, CRYPTO, F)
              if isinstance(o, chrome.ChapterCount)]
    assert counts == [(1, 3), (2, 3), (3, 3)]


def test_it_can_be_turned_off():
    assert _chrome(False, CHAPTERS, SHOTS, TOTAL, CRYPTO, F) == []


def test_a_video_with_one_chapter_gets_no_bar():
    """A progress rule with no ticks in it is a plain wipe across the bottom
    of the frame that says nothing about structure."""
    assert _chrome(True, CHAPTERS[:1], SHOTS, TOTAL, CRYPTO, F) == []


@pytest.mark.parametrize("brand", [CRYPTO, TINNITUS])
@pytest.mark.parametrize("t", [0.0, 0.4, 32.0, 79.0, 149.9])
def test_the_overlays_render(brand, t):
    pic = Image.new("RGB", F.size, (20, 20, 20))
    for o in _chrome(True, CHAPTERS, SHOTS, TOTAL, brand, F):
        pic = o.draw(pic, t)
    assert pic.size == F.size and pic.mode == "RGB"


def test_the_bar_fades_in_rather_than_being_there_from_frame_zero():
    """Over the hook, the only thing on screen should be the hook."""
    bar = chrome.ProgressBar([t for t, _ in CHAPTERS], TOTAL, CRYPTO, F)
    blank = Image.new("RGB", F.size, (0, 0, 0))
    assert bar.draw(blank, 0.0).tobytes() == blank.tobytes()
    assert bar.draw(blank, 2.0).tobytes() != blank.tobytes()


def test_the_count_does_not_outlive_its_card():
    """A label that outlives the card it annotates reads as a stuck overlay."""
    c = chrome.ChapterCount(2, 5, 31.0, 3.4, CRYPTO, F)
    blank = Image.new("RGB", F.size, (0, 0, 0))
    assert c.draw(blank, 32.5).tobytes() != blank.tobytes()
    assert c.draw(blank, 30.0).tobytes() == blank.tobytes()
    assert c.draw(blank, 36.0).tobytes() == blank.tobytes()


def test_overlays_expose_cues_so_they_are_interchangeable():
    for o in _chrome(True, CHAPTERS, SHOTS, TOTAL, CRYPTO, F):
        assert o.cues() == []


# --- the collision ---------------------------------------------------------

def _whooshes(shots):
    cues = _cues(shots, TOTAL) + transitions.cues(shots)
    return sorted(t for t, k in cues if k == "whoosh")


def test_a_plain_card_keeps_its_exit_whoosh():
    assert len(_whooshes([card(30.0), beat(33.4)])) == 1


def test_a_card_on_a_whip_fires_exactly_one_whoosh():
    """Both sounds are a whoosh and they land 0.14s apart - a flam, not a
    transition. The transition wins, because its cue is timed to the move it
    is actually covering."""
    shots = [card(30.0, transition="whip", xfade=transitions.XF["whip"]),
             beat(33.4)]
    assert len(_whooshes(shots)) == 1


def test_a_card_on_a_soundless_move_keeps_its_own_whoosh():
    """`push` brings no sound, so suppressing the card's would leave the cut
    silent - the suppression is about collision, not about transitions."""
    shots = [card(30.0, transition="push", xfade=transitions.XF["push"]),
             beat(33.4)]
    assert len(_whooshes(shots)) == 1
