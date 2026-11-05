"""The real page, on screen: scripted captures of a website, and camera moves
over them.

`footage.md` (2026-10-20): when the subject is a real thing, its real
pictures lead. For a lot of this channel's subjects the real picture is a
*page* - the block explorer showing the transaction, the market's odds, the
exchange's own announcement, the article the video links to. Screenshots
pasted in by hand are the wrong size, carry cookie banners and are never the
same twice. This captures a page the same way every time, and moves a camera
over the capture offline:

    python -m video_automation screencap grab URL NAME \\
        --select odds="css=.market-odds" --hide "#cookie-banner" [--mobile]
    python -m video_automation screencap clip NAME \\
        --path top,odds --ring odds --secs 7 [--vertical]

**Capture once, move offline.** `grab` takes one full-page screenshot at 2x
(3x for `--mobile`) with reduced motion, a fixed viewport, locale and
timezone, after scrolling the page once so lazy images load - and records
where each `--select`ed element sits. `clip` is pure image work on that PNG:
an eased camera from framing to framing, a ring in the brand colour on the
element the voice names. No timing jitter, any length, re-cut for free.

**What is committed is the record, not the bytes.** `NAME.json` carries the
URL, the date, the viewport and every selector, which is what makes a
capture reproducible (`screencap regrab NAME`); the PNG is a third party's
page and stays out of git, like `assets/stock/press/`. A page changes - a
regrab shows today's version, and the record's date says which one shipped.

Rules for what goes on screen are in `footage.md`, "A real page": no logged-
in views, nobody's private data, and the page has to say what the line says.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw

from .brand import CRYPTO, Brand
from .draw import ease_out
from .frame import LANDSCAPE, VERTICAL, Frame

REPO = Path(__file__).resolve().parents[2]
CAPTURES = REPO / "assets/stock/captures"

# Consent layers that cover the page on first visit. Hidden, never clicked:
# clicking "accept" on someone's behalf is not this tool's business.
CONSENT = ("#onetrust-consent-sdk", "#CybotCookiebotDialog", ".fc-consent-root",
           "#usercentrics-root", "#didomi-host", ".cc-window", "#cookie-law-info-bar")


@dataclass
class Capture:
    name: str
    url: str
    viewport: tuple[int, int] = (1280, 800)
    scale: int = 2
    mobile: bool = False
    dark: bool = False
    select: dict[str, str] = field(default_factory=dict)
    hide: list[str] = field(default_factory=list)
    captured: str = ""
    title: str = ""
    size: tuple[int, int] = (0, 0)            # the PNG, in pixels
    boxes: dict[str, list[float]] = field(default_factory=dict)  # PNG pixels

    @property
    def png(self) -> Path:
        return CAPTURES / self.name / f"{self.name}.png"

    @property
    def record(self) -> Path:
        return CAPTURES / self.name / f"{self.name}.json"

    def save(self) -> None:
        self.record.parent.mkdir(parents=True, exist_ok=True)
        self.record.write_text(json.dumps(asdict(self), indent=2) + "\n")

    @classmethod
    def load(cls, name_or_path) -> "Capture":
        p = Path(name_or_path)
        if p.suffix != ".json":
            p = CAPTURES / str(name_or_path) / f"{name_or_path}.json"
        d = json.loads(p.read_text())
        d["viewport"] = tuple(d["viewport"])
        d["size"] = tuple(d["size"])
        return cls(**d)

    def fractions(self, key: str) -> tuple[float, float, float, float]:
        """An element's box as fractions of the capture, for `spotlight`."""
        x0, y0, x1, y1 = self.boxes[key]
        w, h = self.size
        return (x0 / w, y0 / h, x1 / w, y1 / h)


def _selector(s: str) -> str:
    return s[4:] if s.startswith("css=") else s


def grab(url: str, name: str, select: dict[str, str] | None = None,
         hide: list[str] | None = None, mobile: bool = False,
         dark: bool = False, viewport: tuple[int, int] | None = None,
         scale: int | None = None, out: Path | None = None,
         timeout: float = 45.0) -> Capture:
    """Capture `url` as `assets/stock/captures/NAME/NAME.png` + its record."""
    from playwright.sync_api import sync_playwright

    select, hide = dict(select or {}), list(hide or [])
    cap = Capture(name=name, url=url, mobile=mobile, dark=dark,
                  viewport=viewport or ((430, 932) if mobile else (1280, 800)),
                  scale=scale or (3 if mobile else 2), select=select, hide=hide)
    png = Path(out) if out else cap.png
    png.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": cap.viewport[0], "height": cap.viewport[1]},
            device_scale_factor=cap.scale, is_mobile=mobile, has_touch=mobile,
            color_scheme="dark" if dark else "light", reduced_motion="reduce",
            locale="en-US", timezone_id="UTC")
        page = ctx.new_page()
        page.goto(url, wait_until="load", timeout=timeout * 1000)
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass                            # a page that never idles still loads
        css = ", ".join(map(_selector, list(CONSENT) + hide))
        page.add_style_tag(content=f"{css} {{ display: none !important; }}"
                                   "html { scroll-behavior: auto !important; }")
        # Scroll once, top to bottom, so lazy images are real in the capture.
        page.evaluate("""async () => {
            const step = innerHeight * 0.8;
            for (let y = 0; y < document.body.scrollHeight; y += step) {
                scrollTo(0, y); await new Promise(r => setTimeout(r, 120));
            }
            scrollTo(0, 0); await new Promise(r => setTimeout(r, 250));
        }""")
        boxes = {}
        for key, sel in select.items():
            box = page.evaluate("""(sel) => {
                const el = document.querySelector(sel);
                if (!el) return null;
                const r = el.getBoundingClientRect();
                return [r.left + scrollX, r.top + scrollY,
                        r.right + scrollX, r.bottom + scrollY];
            }""", _selector(sel))
            if box is None:
                browser.close()
                raise ValueError(f"{name}: --select {key}={sel!r} matched nothing "
                                 f"on {url}")
            boxes[key] = [v * cap.scale for v in box]
        cap.title = page.title()
        page.screenshot(path=str(png), full_page=True, animations="disabled")
        browser.close()

    cap.boxes = boxes
    cap.size = Image.open(png).size
    cap.captured = _dt.date.today().isoformat()
    if out is None:
        cap.save()
    return cap


# --- the camera ------------------------------------------------------------


def _framing(cap: Capture, frame: Frame, key: str | None, fill: float):
    """(centre x, centre y, scale): the page's width across the frame, or
    the element `key` filling `fill` of it."""
    W, H = frame.size
    pw, ph = cap.size
    base = W / pw
    if key in (None, "top"):
        return pw / 2, min(ph, H / base) / 2, base
    if key == "bottom":
        return pw / 2, ph - H / base / 2, base
    x0, y0, x1, y1 = cap.boxes[key]
    s = min(W * fill / (x1 - x0), H * fill / (y1 - y0))
    # Never past 2.4x: type turns soft. And a little *under* the page's own
    # width when the element is as wide as the page - a full-width paragraph
    # on a phone capture otherwise put its ring on the screen's edges.
    s = max(base * 0.86, min(s, base * 2.4))
    return (x0 + x1) / 2, (y0 + y1) / 2, s


def _clamp(cx, cy, s, cap: Capture, frame: Frame):
    """Keep the view on the page: no grey margins past its edges."""
    W, H = frame.size
    pw, ph = cap.size
    hw, hh = W / s / 2, H / s / 2
    cx = pw / 2 if hw * 2 >= pw else min(max(cx, hw), pw - hw)
    cy = ph / 2 if hh * 2 >= ph else min(max(cy, hh), ph - hh)
    return cx, cy


def clip(cap: Capture | str, out: Path, path: list[str], secs: float = 6.0,
         frame: Frame = LANDSCAPE, ring: list[str] | None = None,
         brand: Brand = CRYPTO, fill: float = 0.72, fps: int = 30,
         move: float = 1.1) -> Path:
    """Render a camera move over a capture to `out` (an MP4, silent).

    `path` is a list of framings, held in turn over `secs`: "top", "bottom",
    or a `--select` key. Each move between them takes `move` seconds, eased;
    the rest of each slot is a slow push. `ring` keys get a rounded ring in
    the brand colour once the camera has arrived on them.
    """
    cap = Capture.load(cap) if isinstance(cap, str) else cap
    page = cv2.cvtColor(cv2.imread(str(cap.png)), cv2.COLOR_BGR2RGB)
    W, H = frame.size
    ring = set(ring or [])
    keys = [None if k == "top" else k for k in path] or [None]
    slot = secs / len(keys)
    stops = [_framing(cap, frame, k, fill) for k in keys]

    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264",
         "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    n = int(round(secs * fps))
    for i in range(n):
        t = i / fps
        k = min(len(keys) - 1, int(t / slot))
        into = t - k * slot
        cx, cy, s = stops[k]
        if k > 0 and into < move:
            p = _ease(into / move)
            px, py, ps = stops[k - 1]
            cx, cy = px + (cx - px) * p, py + (cy - py) * p
            s = math.exp(math.log(ps) + (math.log(s) - math.log(ps)) * p)
        s *= 1.0 + 0.010 * max(0.0, into - (move if k else 0.0))
        cx, cy = _clamp(cx, cy, s, cap, frame)
        m = np.float32([[s, 0, W / 2 - cx * s], [0, s, H / 2 - cy * s]])
        # Warp only the rows on screen. A phone capture at 3x runs past
        # 35,000px, and cv2's warp refuses any side over 32,767 (SHRT_MAX) -
        # the first vertical demo died on exactly that.
        r0 = max(0, int(cy - H / s / 2) - 4)
        r1 = min(page.shape[0], int(cy + H / s / 2) + 5)
        mc = m.copy()
        mc[1, 2] += s * r0
        img = cv2.warpAffine(page[r0:r1], mc, (W, H), flags=cv2.INTER_AREA
                             if s < 1 else cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)
        key = keys[k]
        if key in ring:
            settle = into - (move if k else 0.0)
            q = ease_out(min(1.0, max(0.0, settle / 0.45)))
            if q > 0:
                img = _ring(img, cap.boxes[key], m, q, brand, W)
        proc.stdin.write(np.ascontiguousarray(img).tobytes())
    proc.stdin.close()
    proc.wait()
    return out


def _ease(p: float) -> float:
    p = min(1.0, max(0.0, p))
    return p * p * (3 - 2 * p)


def _ring(img: np.ndarray, box, m, q: float, brand: Brand, W: int) -> np.ndarray:
    """The `spotlight` ring: the rest dims a little, the element is circled."""
    x0, y0, x1, y1 = box
    s, tx, ty = m[0, 0], m[0, 2], m[1, 2]
    pad = W * 0.010
    sx0, sy0, sx1, sy1 = x0 * s + tx - pad, y0 * s + ty - pad, x1 * s + tx + pad, y1 * s + ty + pad
    out = Image.fromarray(img)
    dim = Image.new("RGBA", out.size, (0, 0, 0, int(110 * q)))
    hole = Image.new("L", out.size, 255)
    ImageDraw.Draw(hole).rounded_rectangle([sx0, sy0, sx1, sy1],
                                           radius=int(W * 0.01), fill=0)
    dim.putalpha(Image.eval(hole, lambda v: int(v * 110 * q / 255)))
    out = out.convert("RGBA")
    out.alpha_composite(dim)
    grow = (1.0 - q) * W * 0.02
    ImageDraw.Draw(out).rounded_rectangle(
        [sx0 - grow, sy0 - grow, sx1 + grow, sy1 + grow], radius=int(W * 0.01),
        outline=(*brand.primary, int(255 * q)), width=max(3, int(W * 0.0035)))
    return np.asarray(out.convert("RGB"))


def still(cap: Capture | str, around: str, frame: Frame = LANDSCAPE,
          out: Path | None = None) -> tuple[Path, dict]:
    """A frame-shaped crop of the capture around `around`, for `spotlight`.

    A full page is far too tall for `spotlight` to frame whole; this cuts
    the screen's worth around the element and returns the crop with every
    selected element's box as fractions of it - ready for a `spotlight`
    payload's regions.
    """
    cap = Capture.load(cap) if isinstance(cap, str) else cap
    page = Image.open(cap.png)
    pw, ph = cap.size
    h = min(ph, int(pw * frame.h / frame.w))
    x0, y0, x1, y1 = cap.boxes[around]
    top = int(min(max((y0 + y1) / 2 - h / 2, 0), ph - h))
    crop = page.crop((0, top, pw, top + h))
    out = out or cap.png.with_name(f"{cap.name}-{around}.png")
    crop.save(out)
    regions = {k: ((b[0] / pw), (b[1] - top) / h, (b[2] / pw), (b[3] - top) / h)
               for k, b in cap.boxes.items() if b[1] >= top and b[3] <= top + h}
    return out, regions


# --- the command line ------------------------------------------------------


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="video_automation screencap")
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("grab", help="capture a page and record it")
    g.add_argument("url")
    g.add_argument("name")
    g.add_argument("--select", action="append", default=[],
                   help="key=css, an element to frame or ring later")
    g.add_argument("--hide", action="append", default=[], help="css to hide")
    g.add_argument("--mobile", action="store_true", help="a phone viewport, 3x")
    g.add_argument("--dark", action="store_true")
    r = sub.add_parser("regrab", help="capture again from NAME.json")
    r.add_argument("name")
    c = sub.add_parser("clip", help="render a camera move over a capture")
    c.add_argument("name")
    c.add_argument("--path", default="top", help="comma list: top,bottom,KEY")
    c.add_argument("--ring", default="", help="comma list of keys to ring")
    c.add_argument("--secs", type=float, default=6.0)
    c.add_argument("--vertical", action="store_true")
    c.add_argument("--out", type=Path, default=None)
    a = ap.parse_args(argv)

    if a.cmd == "grab":
        sel = dict(s.split("=", 1) for s in a.select)
        cap = grab(a.url, a.name, sel, a.hide, mobile=a.mobile, dark=a.dark)
    elif a.cmd == "regrab":
        old = Capture.load(a.name)
        cap = grab(old.url, old.name, old.select, old.hide, mobile=old.mobile,
                   dark=old.dark, viewport=old.viewport, scale=old.scale)
    else:
        cap = Capture.load(a.name)
        frame = VERTICAL if a.vertical else LANDSCAPE
        out = a.out or cap.png.with_name(
            f"{cap.name}-{'v' if a.vertical else 'l'}.mp4")
        clip(cap, out, a.path.split(","), a.secs, frame,
             ring=[k for k in a.ring.split(",") if k])
        print(out)
        return 0
    print(f"{cap.png}  {cap.size[0]}x{cap.size[1]}  '{cap.title}'")
    for k in cap.boxes:
        print(f"  {k}: {tuple(round(v, 3) for v in cap.fractions(k))}")
    return 0
