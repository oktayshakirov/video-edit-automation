"""Where glitch and TV-static cuts go (`transitions.plan_special`).

The editor's rule: used sometimes, not too often - and on cuts that mean
something.
"""

from video_automation.core.transitions import XF, plan_special
from video_automation.crypto.shots import Shot


def lay(kinds, step=10.0):
    """Shots `step` seconds apart: "f" footage, "c" chapter card, "b" beat."""
    out = []
    for i, k in enumerate(kinds):
        sh = (Shot(clip="c.mp4") if k == "f" else
              Shot(graphic="chapter", payload=("A turn",)) if k == "c" else
              Shot(graphic="checklist", payload=([],)))
        sh.start, sh.hold = i * step, step
        out.append(sh)
    return out


def test_a_turn_gets_a_glitch_on_the_cut_into_it():
    shots = lay("fff")
    got = plan_special(shots, ["", "", "But it never shipped."], 30.0)
    assert got == [(20.0, "glitch", "turn")]
    assert shots[1].transition == "glitch" and shots[1].xfade == XF["glitch"]


def test_chapter_cards_alternate_static_and_glitch():
    shots = lay("f" + "fffcfff" * 3, step=5.0)
    plan_special(shots, [""] * len(shots), 110.0, budget=3)
    modes = [shots[i - 1].transition for i, s in enumerate(shots)
             if s.graphic == "chapter"]
    assert modes[0] == "static" and modes[1] == "glitch"


def test_budget_spacing_and_guards():
    shots = lay("f" * 20, step=3.0)
    lines = ["But no."] * 20
    got = plan_special(shots, lines, 60.0)
    assert len(got) == 1                         # ~1 per 45s
    assert all(6.0 <= t <= 52.0 for t, _, _ in got)
    got = plan_special(lay("f" * 20, step=3.0), lines, 60.0, budget=5)
    times = [t for t, _, _ in got]
    assert all(b - a >= 20.0 for a, b in zip(times, times[1:]))


def test_hand_picked_and_data_beats_are_left_alone():
    shots = lay("fbf")
    plan_special(shots, ["", "But no.", "But no."], 30.0)
    assert shots[0].transition is None and shots[1].transition is None
    shots = lay("fff")
    shots[1].transition = "wipe"
    plan_special(shots, ["", "", "But no."], 30.0)
    assert shots[1].transition == "wipe"


def test_a_time_jump_gets_static():
    shots = lay("fff")
    got = plan_special(shots, ["", "", "In twenty fourteen, it launched."], 30.0)
    assert got and got[0][1] == "static"
