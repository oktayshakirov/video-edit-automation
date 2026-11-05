"""Scripted captures: the page is captured the same way every time, and the
camera lands where the record says the element is.

Runs against a local page (`file://`), never the network. Skips where the
Playwright browser is not installed
(`.venv/bin/python -m playwright install chromium`).

The tall page is the regression: a phone capture at 3x runs past 35,000px,
and cv2's warp refuses any side over 32,767 - the first vertical demo
raised on exactly that.
"""

from __future__ import annotations

import cv2
import numpy as np
import pytest

from video_automation.core import screencap
from video_automation.core.brand import CRYPTO
from video_automation.core.frame import VERTICAL


def _browser_ok() -> bool:
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            p.chromium.launch().close()
        return True
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _browser_ok(),
                                reason="Playwright's chromium is not installed")

PAGE = """<!doctype html><html><head><meta name=viewport content="width=device-width">
<style>body{margin:0;background:#202020}#banner{position:fixed;top:0;left:0;right:0;
height:120px;background:#ff00ff}#target{position:absolute;top:11000px;left:40px;
width:200px;height:150px;background:#00ff00}#tall{height:12000px}</style></head>
<body><div id=banner></div><div id=tall></div><div id=target></div></body></html>"""


@pytest.fixture(scope="module")
def cap(tmp_path_factory):
    """One capture for the module - a browser launch is the slow part."""
    tmp = tmp_path_factory.mktemp("captures")
    old, screencap.CAPTURES = screencap.CAPTURES, tmp
    try:
        page = tmp / "page.html"
        page.write_text(PAGE)
        yield screencap.grab(page.as_uri(), "t", {"target": "#target"},
                             hide=["#banner"], mobile=True)
    finally:
        screencap.CAPTURES = old


def test_the_capture_records_where_the_element_is(cap):
    assert cap.size[0] == 430 * 3                  # the phone viewport, at 3x
    assert cap.size[1] > 32767                     # taller than cv2 allows
    x0, y0, x1, y1 = cap.boxes["target"]
    assert (x0, y0, x1, y1) == pytest.approx((120, 33000, 720, 33450), abs=3)
    again = screencap.Capture.load(cap.record)
    assert again.boxes == cap.boxes and again.url == cap.url


def test_a_hidden_layer_is_not_in_the_capture(cap):
    png = cv2.imread(str(cap.png))
    assert tuple(png[60, 600]) == (32, 32, 32)     # the page, not the banner


def test_the_camera_lands_on_the_element_and_rings_it(cap, tmp_path):
    out = tmp_path / "t.mp4"
    screencap.clip(cap, out, ["top", "target"], secs=2.0, frame=VERTICAL,
                   ring=["target"], brand=CRYPTO, move=0.5)
    v = cv2.VideoCapture(str(out))
    frames = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    assert frames == 60
    v.set(cv2.CAP_PROP_POS_FRAMES, frames - 1)
    ok, last = v.read()
    assert ok and last.shape[:2] == (VERTICAL.h, VERTICAL.w)
    green = (last[:, :, 1] > 200) & (last[:, :, 0] < 80) & (last[:, :, 2] < 80)
    ys, xs = np.nonzero(green)
    # The element is on screen, near the middle...
    assert abs(ys.mean() - VERTICAL.h / 2) < VERTICAL.h * 0.1
    # ...and the brand ring is drawn around it.
    r, g, b = CRYPTO.primary
    gold = ((np.abs(last[:, :, 2].astype(int) - r) < 40)
            & (np.abs(last[:, :, 1].astype(int) - g) < 40)
            & (last[:, :, 0] < 90))
    assert gold.sum() > 500


def test_still_cuts_a_screen_around_the_element_for_spotlight(cap, tmp_path):
    out, regions = screencap.still(cap, "target", out=tmp_path / "s.png")
    w, h = cv2.imread(str(out)).shape[1::-1]
    assert h < cap.size[1] and w == cap.size[0]
    x0, y0, x1, y1 = regions["target"]
    assert 0 <= y0 < y1 <= 1 and 0 <= x0 < x1 <= 1
