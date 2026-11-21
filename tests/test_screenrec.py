"""core/screenrec.py: the idle speed-up, the camera's targets, and a small
render end to end on a synthetic recording with a log."""

import json
import subprocess

import numpy as np
import pytest

from video_automation.core import screenrec as sr
from video_automation.core import window


def _mot(n, rate=10, boxes=None, frac=None):
    return {"rate": rate, "frac": np.array(frac if frac is not None else [0.0] * n),
            "boxes": boxes if boxes is not None else [None] * n}


def test_idle_is_sped_up_but_its_edges_are_not():
    fps = 30
    on = np.zeros(10 * fps, bool)
    on[: 2 * fps] = True                    # 2s busy, 8s idle
    t = sr.time_map(on, idle=4.0, fps=fps)
    # 2s + 2 x 0.35s at 1x, the remaining 7.3s at 4x.
    assert len(t) / fps == pytest.approx(2 + 0.7 + 7.3 / 4, abs=0.1)
    steps = np.diff(t)
    assert steps[: 2 * fps].max() == pytest.approx(1 / fps)
    assert steps.max() == pytest.approx(4 / fps)


def test_no_idle_speed_up_when_turned_off():
    on = np.zeros(90, bool)
    assert len(sr.time_map(on, idle=0)) == 90


def test_a_click_zooms_in_before_it_lands_and_out_after():
    W, H = 3000, 2000
    ev = sr.Events(t=np.array([0.0, 10.0]), x=np.array([600.0, 600.0]),
                   y=np.array([400.0, 400.0]), clicks=[(3.0, 600.0, 400.0)],
                   keys=np.array([]), scrolls=np.array([]))
    t = np.arange(0, 10, 0.1)
    a = sr.targets(t, W, H, ev, _mot(100), 1.8, (0, 0, W, H))
    at = lambda s: int(round(s * 10))
    assert a.zoom[at(1.0)] == 1.0
    assert a.zoom[at(2.8)] == 1.8           # LEAD: already in before the click
    assert (a.cx[at(3.0)], a.cy[at(3.0)]) == (600.0, 400.0)
    assert a.zoom[at(3.0 + sr.HOLD + 0.5)] == 1.0


def test_a_scroll_ends_the_zoom():
    W, H = 3000, 2000
    ev = sr.Events(t=np.array([0.0, 10.0]), x=np.array([600.0, 600.0]),
                   y=np.array([400.0, 400.0]), clicks=[(2.0, 600.0, 400.0)],
                   keys=np.array([]), scrolls=np.array([3.0]))
    a = sr.targets(np.arange(0, 6, 0.1), W, H, ev, _mot(60), 1.8, (0, 0, W, H))
    assert a.zoom[25] == 1.8 and a.zoom[32] == 1.0


def test_a_blinking_caret_draws_no_camera():
    # One character cell blinking forever: local, persistent, never growing.
    box = (0.10, 0.80, 0.106, 0.818)
    n = 80
    mot = _mot(n, boxes=[box if i % 5 < 3 else None for i in range(n)],
               frac=[0.0001 if i % 5 < 3 else 0.0 for i in range(n)])
    assert sr.change_runs(mot) == []
    # A reply arriving over a second is a run.
    grow = [(0.5, 0.2, 0.55 + 0.02 * i, 0.22 + 0.01 * i) for i in range(12)]
    mot = _mot(12, boxes=grow, frac=[0.003] * 12)
    assert len(sr.change_runs(mot)) == 1


def test_camera_stays_inside_the_region_and_keeps_its_shape():
    W, H = 3000, 2000
    aim = sr.Aim(zoom=np.full(60, 2.0), cx=np.full(60, 10.0), cy=np.full(60, 10.0))
    boxes = sr.camera(aim, W, H, (0, 0, W, H), 16 / 9)
    x0, y0, w, h = boxes[-1]
    assert x0 >= 0 and y0 >= 0
    assert w / h == pytest.approx(16 / 9)
    assert w == pytest.approx(W / 2.0, rel=0.01)   # 3:2 is width-limited at 16:9


def test_the_picture_fills_exactly_what_a_window_shows():
    for vertical in (False, True):
        size = (1080, 1920) if vertical else (1920, 1080)
        x, y, w, h = sr.content_rect(size, vertical)
        from video_automation.core.frame import LANDSCAPE, VERTICAL
        L = window.layout(VERTICAL if vertical else LANDSCAPE, wide=True)
        assert w / h == pytest.approx(L.w / L.ch, rel=0.01)
        assert x >= 0 and y >= 0 and x + w <= size[0] and y + h <= size[1]


def test_wide_window_clears_the_control_bar():
    from video_automation.core.frame import LANDSCAPE
    L = window.layout(LANDSCAPE, wide=True)
    assert L.y >= 0 and L.y + L.h <= LANDSCAPE.safe_bottom
    assert L.w > window.layout(LANDSCAPE).w
    assert window.is_wide(("terminal", "", "wide"))
    assert not window.is_wide(("terminal", ""))


def test_a_raw_clip_is_not_graded_or_pushed(monkeypatch):
    from video_automation.crypto.shots import Shot
    from video_automation.longform import clip as clipmod
    from video_automation.longform.beats import make_beat
    seen = {}

    class Fake:
        def __init__(self, path, hold, **kw):
            seen.update(kw)

    monkeypatch.setattr(clipmod, "VideoShot", Fake)
    make_beat(Shot(clip="x.mp4", hold=3.0, raw=True), brand=None, frame=None)
    assert seen["zoom"] == 1.0 and seen["dim"] == 1.0 and seen["saturation"] == 1.0
    seen.clear()
    make_beat(Shot(clip="x.mp4", hold=3.0), brand=None, frame=None)
    assert seen["zoom"] == Shot.zoom and "dim" not in seen


def test_render_end_to_end(tmp_path):
    """A 3s 640x400 'screen' with a click: renders, zooms, keeps the size."""
    src = tmp_path / "s.mov"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
                    "testsrc2=size=640x400:rate=30", "-t", "3", "-pix_fmt",
                    "yuv420p", str(src)], check=True)
    sr.events_path(src).write_text(json.dumps({
        "version": 1, "display": {"x": 0, "y": 0, "w": 320, "h": 200},
        "video_start": 0, "samples": [[0, 100, 50], [3, 100, 50]],
        "clicks": [[1.0, 100, 50]], "keys": [], "scrolls": []}))
    out = sr.render(sr.Spec(src, idle=0, blur=[(0, 0, 0.5, 0.5)]),
                    tmp_path / "o.mp4", say=lambda *a: None)
    W, H, dur = sr.probe(out)
    assert (W, H) == (1920, 1080)
    assert dur == pytest.approx(3.0, abs=0.1)
    info = json.loads(out.with_suffix(".json").read_text())
    assert info["log"] and info["clicks"] == 1 and info["zoomed_share"] > 0.3


def test_path_registers_without_rendering(tmp_path):
    src = tmp_path / "a.mov"
    src.write_bytes(b"x")
    out = sr.path(src, vertical=True)
    assert not out.exists() and out in sr._PENDING
    assert "9x16" in out.name and sr._PENDING[out].zoom == 2.2
    sr._PENDING.pop(out)
