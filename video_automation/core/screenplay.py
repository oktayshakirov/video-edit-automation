"""Screen recordings with nobody at the keyboard: a real browser, or a
terminal, driven from a script and recorded with its own event log.

OktAI (2026-11-21, the editor's note): Oktay records the voice and nothing
else. Every screen in a video is made the way the drawn beats are - from
the project file, the same every time. A take is a list of steps:

    take = Browser("https://huggingface.co/spaces", [
        click("text=Spaces"),
        type_("image upscaler", into="input[type=search]"),
        press("Enter"),
        wait_for("article"),
        scroll(600),
    ])
    take = Terminal([
        cmd("claude"),
        out("Welcome to Claude Code"),
        cmd("build me a landing page for a dog-walking business", prompt="> "),
        think(6, "Thinking"),
        out(REAL_OUTPUT, secs=3),
    ])

`capture(take, out)` plays it in headless Chromium at 2x and records the
page with the DevTools screencast (a frame for every paint, with its own
time), and writes `out.events.json` from the steps themselves - every
mouse move, click, key and scroll at the moment it was sent. That is the
same log `screenrec.record` writes for a live recording, so the render is
the same: idle sped up, the camera zoomed to the work, a ripple on each
click, a drawn cursor (headless Chromium has none). No screen permission,
no hands, no private windows in the corner.

The cursor moves on an eased path at a hand's pace and typing has a
human, uneven rhythm, because a cut where the pointer teleports or text
appears at machine speed reads as fake.

`Terminal` runs in a page of our own (`screenplay_term.html`): the steps
type the command, stream the output, spin a "thinking" line. The output is
whatever the project gives it - paste the real output of the real run
(ANSI colours are kept), never invented results: `footage.md`, "Our own
screen".

A take's digest (its steps, viewport, this module's VERSION) is stored
next to the capture; `oktai.screen()` re-captures only when the take
changes. A live site changes too - the capture is from the day it ran.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import math
import random
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path

VERSION = 1
TERM_PAGE = Path(__file__).with_name("screenplay_term.html")
CONSENT = ("#onetrust-consent-sdk", "#CybotCookiebotDialog", ".fc-consent-root",
           "#usercentrics-root", "#didomi-host", ".cc-window",
           "#cookie-law-info-bar")


# -- steps --------------------------------------------------------------------
# Plain dicts, so a take hashes and prints as what it is.

def goto(url: str) -> dict:
    return {"do": "goto", "url": url}


def wait(secs: float) -> dict:
    return {"do": "wait", "secs": secs}


def wait_for(target: str, timeout: float = 30) -> dict:
    """Until `target` (a Playwright selector: css, `text=...`) is visible."""
    return {"do": "wait_for", "target": target, "timeout": timeout}


def move(target: str) -> dict:
    return {"do": "move", "target": target}


def click(target: str) -> dict:
    return {"do": "click", "target": target}


def type_(text: str, into: str | None = None, cps: float = 14) -> dict:
    """Type `text` (into `target`, clicked first) at about `cps` characters a
    second, unevenly."""
    return {"do": "type", "text": text, "into": into, "cps": cps}


def press(key: str) -> dict:
    return {"do": "press", "key": key}


def scroll(dy: float, at: str | None = None) -> dict:
    """Scroll by `dy` CSS pixels with the wheel, in a hand's few flicks."""
    return {"do": "scroll", "dy": dy, "at": at}


def js(code: str) -> dict:
    """Run `code` in the page (dismiss a banner, open a panel). Not shown as
    input: nothing is logged."""
    return {"do": "js", "code": code}


# Terminal steps.

def cmd(text: str, prompt: str = "~/app $ ", cps: float = 16) -> dict:
    """A prompt, the command typed, Enter."""
    return {"do": "cmd", "text": text, "prompt": prompt, "cps": cps}


def out(text: str, secs: float = 0.0) -> dict:
    """Output lines (ANSI colours kept), streamed line by line over `secs`."""
    return {"do": "out", "text": text, "secs": secs}


def think(secs: float, label: str = "Thinking") -> dict:
    """A spinner line for `secs`, then gone - the wait a model takes. The
    render speeds it up like any idle stretch."""
    return {"do": "think", "secs": secs, "label": label}


def clear() -> dict:
    return {"do": "clear"}


# -- takes ----------------------------------------------------------------------

@dataclass
class Browser:
    url: str
    steps: list = field(default_factory=list)
    viewport: tuple = (1440, 810)          # 16:9, the wide window's shape
    scale: int = 2
    dark: bool = True
    hide: list = field(default_factory=list)
    lead: float = 1.2                      # s on the loaded page before step 1
    tail: float = 1.5                      # s held after the last step

    def digest(self) -> str:
        return _digest(self)


@dataclass
class Terminal:
    steps: list = field(default_factory=list)
    viewport: tuple = (1120, 630)          # 16:9, type ~32px tall in 1080p
    scale: int = 2
    font: int = 19
    title: str = ""
    lead: float = 0.8
    tail: float = 1.5

    def digest(self) -> str:
        return _digest(self)


# A Short's terminal: the shape of the 9:16 window's content, so the lines
# wrap there instead of running off the right edge.
TERM_VERTICAL = (440, 405)


def _digest(take) -> str:
    d = {"kind": type(take).__name__, "v": VERSION, **take.__dict__}
    raw = json.dumps(d, sort_keys=True, default=str)
    if isinstance(take, Terminal):
        raw += TERM_PAGE.read_text()
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def take_path(video: Path) -> Path:
    return Path(video).with_suffix(".take.json")


def fresh(take, video: Path) -> bool:
    """Is `video` a capture of this take as it is now?"""
    tp = take_path(video)
    return (Path(video).exists() and tp.exists()
            and json.loads(tp.read_text()).get("digest") == take.digest())


# -- the capture ----------------------------------------------------------------

class _Log:
    def __init__(self):
        self.t0 = None
        self.samples, self.clicks, self.keys, self.scrolls = [], [], [], []
        self.x, self.y = None, None

    def now(self) -> float:
        return time.time() - self.t0

    def at(self, x, y):
        self.x, self.y = x, y
        self.samples.append([round(self.now(), 4), round(x, 2), round(y, 2)])


def capture(take, out: Path, say=print, seed: int = 7) -> Path:
    """Play `take` and record it to `out` (.mp4) + `out.events.json`."""
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="screenplay-"))
    try:
        frames, log, size, info = asyncio.run(_play(take, work, say, seed))
        _encode(frames, log, out, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    vw, vh = take.viewport
    ev = {"version": 1, "display": {"x": 0, "y": 0, "w": vw, "h": vh},
          "video_start": 0, "cursor": "draw" if log.samples else "none",
          "samples": log.samples, "clicks": log.clicks, "keys": log.keys,
          "scrolls": log.scrolls}
    out.with_suffix(".events.json").write_text(json.dumps(ev))
    take_path(out).write_text(json.dumps(
        {"digest": take.digest(), "captured": time.strftime("%Y-%m-%d"),
         "kind": type(take).__name__, **info}, indent=1))
    return out


async def _play(take, work: Path, say, seed: int):
    from playwright.async_api import async_playwright

    rnd = random.Random(seed)
    vw, vh = take.viewport
    log = _Log()
    frames: list[tuple[float, Path]] = []
    pending: list = []
    info: dict = {}

    async with async_playwright() as p:
        # The screencast sends frames at the CSS size whatever the context's
        # device_scale_factor; this flag is what gives it 2x pixels.
        browser = await p.chromium.launch(
            args=[f"--force-device-scale-factor={take.scale}"])
        is_term = isinstance(take, Terminal)
        ctx = await browser.new_context(
            viewport={"width": vw, "height": vh}, device_scale_factor=take.scale,
            color_scheme="dark" if (is_term or take.dark) else "light",
            locale="en-US", timezone_id="UTC")
        page = await ctx.new_page()
        if is_term:
            await page.goto(TERM_PAGE.as_uri())
            await page.evaluate("([f, t]) => term.setup(f, t)",
                                [take.font, take.title])
        else:
            await page.goto(take.url, wait_until="load", timeout=60000)
            try:
                await page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            await _hide(page, take.hide)
            info["url"] = take.url
            info["title"] = await page.title()

        cdp = await ctx.new_cdp_session(page)
        n = [0]

        async def on_frame(ev):
            k = n[0]
            n[0] += 1
            path = work / f"{k:06d}.jpg"
            import base64
            path.write_bytes(base64.b64decode(ev["data"]))
            # The frame's own swap time (epoch seconds); arrival time if absent.
            frames.append((ev["metadata"].get("timestamp") or time.time(), path))
            try:
                await cdp.send("Page.screencastFrameAck",
                               {"sessionId": ev["sessionId"]})
            except Exception:
                pass

        cdp.on("Page.screencastFrame",
               lambda ev: pending.append(asyncio.ensure_future(on_frame(ev))))
        log.t0 = time.time()
        await cdp.send("Page.startScreencast",
                       {"format": "jpeg", "quality": 92,
                        "maxWidth": vw * take.scale, "maxHeight": vh * take.scale,
                        "everyNthFrame": 1})
        # A first paint to start the stream on: nudge the page by nothing.
        await page.evaluate("document.body.style.outline='0px solid transparent'")
        if not is_term:
            log.at(vw * 0.62, vh * 0.58)            # where the hand rests
        await page.wait_for_timeout(take.lead * 1000)

        for i, step in enumerate(take.steps):
            try:
                await _step(page, step, log, rnd, take)
            except Exception as e:
                raise RuntimeError(f"step {i + 1} {step}: {e}") from e
        await page.wait_for_timeout(take.tail * 1000)
        end = log.now()
        await cdp.send("Page.stopScreencast")
        await asyncio.sleep(0.2)
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
        await browser.close()
    if not frames:
        raise RuntimeError("the screencast sent no frames")
    # Frame times onto the log's clock. Chromium's swap timestamps are epoch
    # seconds; anything else (or a clock that disagrees by more than a
    # second) falls back to arrival order on the log's clock.
    ts = [f[0] for f in frames]
    if not (abs(ts[0] - log.t0) < 5):
        say("screenplay: frame timestamps are not wall time; using arrival")
    frames = sorted(((t - log.t0, p) for t, p in frames), key=lambda f: f[0])
    info["frames"] = len(frames)
    info["seconds"] = round(end, 2)
    log.end = end
    return frames, log, (vw * take.scale, vh * take.scale), info


async def _hide(page, hide):
    css = ", ".join(list(CONSENT) + list(hide))
    await page.add_style_tag(content=f"{css} {{ display: none !important; }}")


async def _center(page, target: str):
    loc = page.locator(target).first
    await loc.scroll_into_view_if_needed(timeout=15000)
    box = await loc.bounding_box(timeout=15000)
    if box is None:
        raise RuntimeError(f"{target!r} is not visible")
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


async def _glide(page, log: _Log, x: float, y: float, rnd):
    """An eased move at a hand's pace: ~0.35-0.8 s depending on distance,
    a slight arc, 60 samples a second."""
    x0, y0 = log.x, log.y
    if x0 is None:
        x0, y0 = x, y
    d = math.hypot(x - x0, y - y0)
    if d < 2:
        await page.mouse.move(x, y)
        log.at(x, y)
        return
    secs = min(0.8, 0.30 + d / 2400)
    n = max(4, int(secs * 60))
    bend = rnd.uniform(-0.08, 0.08) * d
    nx, ny = -(y - y0) / d, (x - x0) / d
    start = time.time()
    for i in range(1, n + 1):
        p = i / n
        e = p * p * (3 - 2 * p)
        arc = math.sin(math.pi * e) * bend
        px, py = x0 + (x - x0) * e + nx * arc, y0 + (y - y0) * e + ny * arc
        await page.mouse.move(px, py)
        log.at(px, py)
        lag = start + secs * p - time.time()
        if lag > 0:
            await asyncio.sleep(lag)


async def _type(page, log: _Log, text: str, cps: float, rnd, term=False):
    for ch in text:
        if term:
            await page.evaluate("c => term.key(c)", ch)
        else:
            await page.keyboard.type(ch)
        log.keys.append(round(log.now(), 4))
        gap = rnd.lognormvariate(math.log(1 / cps), 0.35)
        if ch == " ":
            gap *= 1.3
        await asyncio.sleep(min(gap, 0.45))


async def _step(page, s: dict, log: _Log, rnd, take):
    do = s["do"]
    if do == "goto":
        await page.goto(s["url"], wait_until="load", timeout=60000)
        await _hide(page, getattr(take, "hide", []))
    elif do == "wait":
        await page.wait_for_timeout(s["secs"] * 1000)
    elif do == "wait_for":
        await page.locator(s["target"]).first.wait_for(
            state="visible", timeout=s["timeout"] * 1000)
    elif do in ("move", "click"):
        x, y = await _center(page, s["target"])
        await _glide(page, log, x, y, rnd)
        if do == "click":
            await asyncio.sleep(rnd.uniform(0.08, 0.16))
            log.clicks.append([round(log.now(), 4), round(x, 2), round(y, 2)])
            await page.mouse.down()
            await asyncio.sleep(0.07)
            await page.mouse.up()
            await asyncio.sleep(0.25)
    elif do == "type":
        if s["into"]:
            await _step(page, click(s["into"]), log, rnd, take)
        await _type(page, log, s["text"], s["cps"], rnd)
    elif do == "press":
        await asyncio.sleep(0.15)
        log.keys.append(round(log.now(), 4))
        await page.keyboard.press(s["key"])
        await asyncio.sleep(0.2)
    elif do == "scroll":
        if s["at"]:
            x, y = await _center(page, s["at"])
            await _glide(page, log, x, y, rnd)
        flicks = max(1, int(abs(s["dy"]) / 220))
        for _ in range(flicks):
            log.scrolls.append(round(log.now(), 4))
            await page.mouse.wheel(0, s["dy"] / flicks)
            await asyncio.sleep(rnd.uniform(0.09, 0.16))
        await asyncio.sleep(0.4)
    elif do == "js":
        await page.evaluate(s["code"])
    elif do == "cmd":
        await page.evaluate("p => term.prompt(p)", s["prompt"])
        await asyncio.sleep(0.35)
        await _type(page, log, s["text"], s["cps"], rnd, term=True)
        await asyncio.sleep(0.25)
        log.keys.append(round(log.now(), 4))
        await page.evaluate("term.enter()")
    elif do == "out":
        lines = s["text"].split("\n")
        gap = s["secs"] / max(1, len(lines))
        for ln in lines:
            await page.evaluate("l => term.line(l)", ln)
            if gap:
                await asyncio.sleep(gap)
        await asyncio.sleep(0.15)
    elif do == "think":
        await page.evaluate("l => term.think(l)", s["label"])
        await asyncio.sleep(s["secs"])
        await page.evaluate("term.done()")
    elif do == "clear":
        await page.evaluate("term.clear()")
    else:
        raise ValueError(f"unknown step {do!r}")


def _encode(frames, log: _Log, out: Path, work: Path, fps: int = 30) -> None:
    """The screencast's frames, each held until the next, as constant-rate
    H.264 from 0 (the log's start) to the end of the take. The JPEGs go to
    ffmpeg as they are, one per output frame - the concat demuxer's
    per-image durations drifted by seconds on a take with few paints."""
    times = [t for t, _ in frames]
    n = max(1, int(round(log.end * fps)))
    tmp = out.with_suffix(".part.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe",
                            "-c:v", "mjpeg", "-framerate", str(fps), "-i", "-",
                            "-vf", "format=yuv420p", "-c:v", "libx264",
                            "-preset", "fast", "-crf", "14", "-movflags",
                            "+faststart", str(tmp)], stdin=subprocess.PIPE)
    import bisect
    last, data = -1, b""
    for i in range(n):
        k = max(0, bisect.bisect_right(times, i / fps) - 1)
        if k != last:
            data, last = frames[k][1].read_bytes(), k
        enc.stdin.write(data)
    enc.stdin.close()
    if enc.wait() != 0:
        raise RuntimeError(f"encoding {out.name} failed")
    tmp.replace(out)
