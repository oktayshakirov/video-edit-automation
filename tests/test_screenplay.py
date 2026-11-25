"""core/screenplay.py: scripted takes are recorded in sync with their own
event log, last exactly as long as the take, and feed `oktai.screen`."""

import json
import subprocess

import numpy as np
import pytest

from video_automation.core import screenplay as sp
from video_automation.core import screenrec as sr


def _chromium() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:
        return False


needs_browser = pytest.mark.skipif(not _chromium(),
                                   reason="playwright chromium not installed")


def _frame_at(video, t, w=64):
    """The mean colour of a frame at `t` seconds, downscaled."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i",
                          str(video), "-frames:v", "1", "-vf", f"scale={w}:-2",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 3).mean(0)


@needs_browser
def test_a_click_is_logged_when_the_page_changes(tmp_path):
    """The page turns red on click: before the logged click it is white, a
    few frames after it red - the log and the picture share one clock."""
    page = tmp_path / "p.html"
    page.write_text("<body style='margin:0;background:#fff'>"
                    "<button id=b style='margin:300px;padding:20px'>go</button>"
                    "<script>b.onclick=()=>document.body.style.background="
                    "'#f00'</script></body>")
    out = tmp_path / "take.mp4"
    take = sp.Browser(page.as_uri(), [sp.click("#b")], viewport=(640, 360),
                      lead=0.5, tail=1.0)
    sp.capture(take, out, say=lambda *a: None)
    ev = json.loads(sr.events_path(out).read_text())
    assert len(ev["clicks"]) == 1 and ev["cursor"] == "draw"
    t, x, y = ev["clicks"][0]
    assert 300 < x < 400 and 300 < y < 360
    before, after = _frame_at(out, t - 0.15), _frame_at(out, t + 0.25)
    assert before[1] > 200 and after[1] < 120          # green channel: white -> red
    W, H, dur = sr.probe(out)
    assert (W, H) == (1280, 720)                       # 2x pixels
    assert dur == pytest.approx(json.loads(sp.take_path(out).read_text())
                                ["seconds"], abs=0.1)


@needs_browser
def test_a_terminal_take_types_and_lasts_as_long_as_it_ran(tmp_path):
    out = tmp_path / "t.mp4"
    take = sp.Terminal([sp.cmd("ls"), sp.out("a.txt\nb.txt"), sp.think(2.0)],
                       viewport=(480, 270), lead=0.3, tail=0.3)
    sp.capture(take, out, say=lambda *a: None)
    ev = json.loads(sr.events_path(out).read_text())
    assert len(ev["keys"]) == 3                        # "l", "s", Enter
    assert ev["cursor"] == "none" and ev["clicks"] == []
    info = json.loads(sp.take_path(out).read_text())
    assert sr.probe(out)[2] == pytest.approx(info["seconds"], abs=0.1)
    assert info["seconds"] > 2.5
    assert sp.fresh(take, out)
    assert not sp.fresh(sp.Terminal([sp.cmd("ls -la")]), out)


def test_a_take_digest_follows_its_steps():
    a = sp.Browser("https://example.com", [sp.click("#x")])
    assert a.digest() == sp.Browser("https://example.com", [sp.click("#x")]).digest()
    assert a.digest() != sp.Browser("https://example.com", [sp.click("#y")]).digest()


def test_oktai_screen_plays_a_take(tmp_path, monkeypatch):
    from video_automation.oktai import build
    monkeypatch.setattr(build, "RECORDINGS", tmp_path)
    term = sp.Terminal([sp.cmd("claude")])
    shot = build.screen("p", "claude", term, vertical=True)
    spec = sr._PENDING.pop(shot.clip)
    assert shot.raw and shot.window == ("terminal", "")
    assert spec.src.name == "claude-v.mp4" and spec.zoom == 1.0
    assert spec.take.viewport == sp.TERM_VERTICAL
    web = sp.Browser("https://example.com/page/", [])
    shot = build.screen("p", "web", web)
    spec = sr._PENDING.pop(shot.clip)
    assert shot.window == ("browser", "example.com/page", "wide")
    assert spec.src.name == "web.mp4" and not spec.src.exists()


def test_a_scripted_log_asks_for_a_drawn_cursor(tmp_path):
    p = tmp_path / "x.events.json"
    p.write_text(json.dumps({"display": {"x": 0, "y": 0, "w": 100, "h": 50},
                             "cursor": "draw", "samples": [[0, 10, 10]],
                             "clicks": [], "keys": [], "scrolls": []}))
    ev = sr.Events.load(p, (200, 100))
    assert ev.draw and ev.px == 2.0
    view = np.zeros((100, 200, 3), np.uint8)
    sr._cursor(view, ev.cursor(0), (0, 0, 200, 100), 1.0, ev.px)
    assert view[25:40, 21:26].max() == 255             # the arrow, below its tip


def test_any_channel_can_use_a_take():
    from video_automation.core.brand import CRYPTO
    s = sp.shot(sp.Browser("https://etherscan.io/", []), "explorer",
                color=CRYPTO.primary)
    spec = sr._PENDING.pop(s.clip)
    assert spec.src == sp.TAKES / "explorer.mp4"
    assert spec.color == tuple(CRYPTO.primary)
    assert s.window == ("browser", "etherscan.io", "wide") and s.raw


def test_ad_slots_are_hidden_on_every_page():
    """The editor (2026-11-23): "make sure there is no gap from ads" - an
    unfilled AdSense slot still reserves its box."""
    from video_automation.core.screenplay import ADS
    assert "ins.adsbygoogle" in ADS and ".ad-slot" in ADS


def test_a_claude_chat_marks_its_prompt():
    """The prompt is the line the viewer reads: typed under a highlighter
    (2026-11-24). Other commands keep their digest - no `mark` key."""
    steps = sp.claude_chat("the opener needs three voices", "Sure.")
    typed = [s for s in steps if s["do"] == "cmd"]
    assert typed and typed[0].get("mark") is True
    assert "mark" not in sp.cmd("ls")
