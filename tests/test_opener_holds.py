"""`opener_holds=True` leaves no bare frame between an opener and the captions.

The opener's exit moves; captions never run under it. Checked on a stand-in
overlay with the three fields the real ones carry.
"""

from __future__ import annotations

from types import SimpleNamespace

from video_automation.crypto.build import (HOLD_LEAD, HOLD_MOST,
                                           settle_opener)


def opener(land=3.0, exit_at=3.9, end=4.18):
    return SimpleNamespace(start=0.0, land=land, exit_at=exit_at, end=end)


def test_it_stays_until_just_before_the_next_sentence():
    ov = opener()
    d = settle_opener(ov, [0.0, 2.7, 7.5])
    assert abs(ov.end - (7.5 - HOLD_LEAD)) < 1e-6 and d > 3
    assert abs((ov.end - ov.exit_at) - 0.28) < 1e-6      # the exit keeps its length


def test_it_never_holds_longer_than_the_cap():
    ov = opener()
    settle_opener(ov, [0.0, 2.7, 12.0])
    assert abs(ov.end - (4.18 + HOLD_MOST)) < 1e-6


def test_it_leaves_early_for_a_sentence_that_starts_just_before():
    ov = opener(land=2.6)
    settle_opener(ov, [0.0, 3.9, 9.6])
    assert abs(ov.end - 3.9) < 1e-6                      # sentence 2 keeps its captions


def test_but_not_if_that_would_cut_the_landing():
    ov = opener(land=3.6)                                # landed 0.3s before its exit
    settle_opener(ov, [0.0, 3.9, 6.0])
    assert abs(ov.end - (6.0 - HOLD_LEAD)) < 1e-6


def test_a_gap_already_closed_is_left_alone():
    ov = opener()
    assert settle_opener(ov, [0.0, 2.7, 4.4]) == 0.0 and ov.end == 4.18


def test_an_overlay_without_an_exit_is_left_alone():
    ov = SimpleNamespace(start=0.0, end=4.0)
    assert settle_opener(ov, [0.0, 6.0]) == 0.0 and ov.end == 4.0
