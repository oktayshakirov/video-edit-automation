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

VERSION = 2          # 2: ad slots hidden on every page (2026-11-23)
REPO = Path(__file__).resolve().parents[2]
# Where a crypto or tinnitus project's takes are recorded. Reproducible from
# the project file, so out of git (`.gitignore`); OktAI keeps its own in the
# project's folder (`oktai.screen`).
TAKES = REPO / "assets/stock/takes"
TERM_PAGE = Path(__file__).with_name("screenplay_term.html")
CONSENT = ("#onetrust-consent-sdk", "#CybotCookiebotDialog", ".fc-consent-root",
           ".fc-message-root", ".fc-ccpa-root", ".fc-dialog-overlay",
           ".fc-monetization-dialog-container", "#usercentrics-root", "#didomi-host",
           ".cc-window", "#cookie-law-info-bar")

# **Removed, never clicked** (2026-11-21): Google's consent dialog on our own
# sites sets its own inline `!important` display and locks the page's scroll,
# so a style tag alone left it over the video grid. A script in every page
# removes any consent layer the moment it is added and gives the scroll back.
# Accepting on someone's behalf is not this tool's business, even in a
# throwaway browser.
_UNCONSENT = """(() => {
  const sel = %s;
  const sweep = () => {
    for (const el of document.querySelectorAll(sel)) el.remove();
    // Google's privacy note lives in an anonymous host's shadow root, out of
    // reach of any selector: removed by what it says.
    for (const el of document.body ? [...document.body.children] : []) {
      const sr = el.shadowRoot;
      if (sr && !el.id && !el.className &&
          /privacy|consent|cookie|data is used/i.test(sr.textContent || '')) el.remove();
    }
    for (const el of [document.documentElement, document.body]) {
      if (el && getComputedStyle(el).overflow === 'hidden') el.style.setProperty('overflow', 'auto', 'important');
    }
  };
  new MutationObserver(sweep).observe(document, {childList: true, subtree: true});
  document.addEventListener('DOMContentLoaded', sweep);
})();"""


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

def cmd(text: str, prompt: str = "~/app $ ", cps: float = 16,
        mark: bool = False) -> dict:
    """A prompt, the command typed, Enter. `mark` types it under a yellow
    highlighter - the line the viewer is meant to read (2026-11-24)."""
    step = {"do": "cmd", "text": text, "prompt": prompt, "cps": cps}
    if mark:
        step["mark"] = True
    return step


MARK_COLOR = "rgba(255, 214, 64, 0.55)"     # a highlighter pen on a white page


def mark(text: str, color: str = MARK_COLOR, secs: float = 0.7) -> dict:
    """A highlighter drawn across `text` on the page, left to right over
    `secs` - the line on a real page the narration is about (2026-11-24, the
    editor on YouTube's policy page: "highlight the relevant part in the
    screenshot with fitting colour"). The first place the text appears, in
    one text node; a phrase not on the page is a script error and raises."""
    code = """(() => {
  const want = %s, color = %s, secs = %s;
  const walk = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let node;
  while ((node = walk.nextNode())) {
    const i = node.textContent.replace(/\\s+/g, " ").indexOf(want);
    if (i < 0 || !node.parentElement || !node.parentElement.offsetParent) continue;
    const raw = node.textContent, map = [];
    for (let k = 0, n = 0; k < raw.length; k++) {
      if (/\\s/.test(raw[k]) && k > 0 && /\\s/.test(raw[k - 1])) continue;
      map.push(k);
    }
    const r = document.createRange();
    r.setStart(node, map[i]);
    r.setEnd(node, map[i + want.length - 1] + 1);
    const s = document.createElement("span");
    s.style.cssText = `background-image: linear-gradient(${color}, ${color});
      background-repeat: no-repeat; background-size: 0%% 100%%;
      transition: background-size ${secs}s ease-in-out; border-radius: 3px;
      -webkit-box-decoration-break: clone; box-decoration-break: clone;`;
    r.surroundContents(s);
    s.getBoundingClientRect();
    requestAnimationFrame(() => { s.style.backgroundSize = "100%% 100%%"; });
    const b = s.getBoundingClientRect();
    return [b.left + b.width / 2, b.top + b.height / 2];
  }
  throw new Error("mark: not on the page: " + want);
})()""" % (json.dumps(text), json.dumps(color), float(secs))
    # Its own step, so the capture logs where it is: the camera holds on a
    # highlight being drawn as it does on a click, with no ripple (the first
    # build drew both while zoomed out, too small to read - 2026-11-24).
    return {"do": "mark", "code": code, "secs": float(secs)}


def glide(dy: int, secs: float) -> dict:
    """The page scrolled `dy` px smoothly over `secs`, eased - a slow read
    down a page rather than a flick of the wheel (2026-11-25, the channel
    grids: "scroll slowly down"). Not logged as input: the camera does not
    treat it as a scroll's cut."""
    code = """(() => new Promise(done => {
  const y0 = window.scrollY, dy = %d, ms = %d, t0 = performance.now();
  const step = now => {
    const p = Math.min(1, (now - t0) / ms), e = p * p * (3 - 2 * p);
    window.scrollTo(0, y0 + dy * e);
    p < 1 ? requestAnimationFrame(step) : done(true);
  };
  requestAnimationFrame(step);
}))()""" % (int(dy), int(secs * 1000))
    return {"do": "js", "code": code}


def out(text: str, secs: float = 0.0) -> dict:
    """Output lines (ANSI colours kept), streamed line by line over `secs`."""
    return {"do": "out", "text": text, "secs": secs}


def think(secs: float, label: str = "Thinking") -> dict:
    """A spinner line for `secs`, then gone - the wait a model takes. The
    render speeds it up like any idle stretch."""
    return {"do": "think", "secs": secs, "label": label}


def clear() -> dict:
    return {"do": "clear"}


# A Claude Code session, as its terminal UI draws it.
CLAUDE = "\x1b[38;2;217;119;87m"       # Claude's orange
DIMMED = "\x1b[2m"
RESET = "\x1b[0m"


def claude_chat(prompt: str, reply: str, tools: list | None = None,
                done: str = "", think_s: float = 1.2,
                cwd: str = "~/Coding/video-edit-automation",
                box: int = 47, mark: bool = True) -> list:
    """Terminal steps for a Claude Code session: the welcome box, the prompt
    typed, the thinking, the reply and each tool call it made.

    **The prompt is highlighted** (`mark`, 2026-11-24, the editor: "mark the
    sentence the viewer should read, which is our prompt ... highlight it in
    yellow"): it is the line the narration is about; the rest is texture.

    **Why (2026-11-23, the editor: "instead of just showing a terminal with
    code, sometimes show a fake Claude Code chat where we give prompts").**
    The prompt is what was asked, said plainly; `tools` are `(call, result)`
    pairs - `("Write(video_automation/longform/beats/voice.py)", "Wrote 143
    lines")` - and they must be real: a file that exists, its real size, a
    command that ran. Reconstructed sessions say so in the project's
    docstring.
    """
    welcome = "\n".join([
        f"{CLAUDE}╭{'─' * box}╮{RESET}",
        f"{CLAUDE}│{RESET} {CLAUDE}✻{RESET} Welcome to {chr(27)}[1mClaude Code{RESET}!"
        + " " * (box - 26) + f"{CLAUDE}│{RESET}",
        f"{CLAUDE}│{RESET}" + " " * box + f"{CLAUDE}│{RESET}",
        f"{CLAUDE}│{RESET}   {DIMMED}cwd: {cwd}{RESET}"
        + " " * max(0, box - 8 - len(cwd)) + f"{CLAUDE}│{RESET}",
        f"{CLAUDE}╰{'─' * box}╯{RESET}", ""])
    # Quick enough to finish under two sentences of narration: the welcome
    # box is already up, the prompt types fast and the thinking is short (a
    # chat under one 3 s sentence was still on its welcome box, 2026-11-23).
    steps = [out(welcome, secs=0.0),
             cmd(prompt, prompt="> ", cps=38, mark=mark), think(think_s, "Thinking"),
             out(f"{CLAUDE}⏺{RESET} {reply}", secs=0.4)]
    for call, result in tools or []:
        steps.append(out(f"\n{CLAUDE}⏺{RESET} {chr(27)}[1m{call}{RESET}\n"
                         f"  {DIMMED}⎿  {result}{RESET}", secs=0.4))
    if done:
        steps.append(out(f"\n{CLAUDE}⏺{RESET} {done}", secs=0.3))
    return steps


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
    # Cookies set before the page loads: a site's own setting, like
    # YouTube's dark theme (`YOUTUBE_DARK`) - signed out, it ignores the
    # browser's colour scheme (2026-11-24).
    cookies: list = field(default_factory=list)
    # Steps done before filming starts, unseen: a sort picked, a filter run
    # (2026-11-25: "don't show how you click the popular filter, just go
    # straight to it"). `click`, `js` and `wait` steps; nothing is logged.
    before: list = field(default_factory=list)
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


# Chromium-based browsers a take can fall back to when Playwright's own is
# not installed, in the order tried.
INSTALLED = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium",
             "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]


async def _launch(p, args: list):
    """Playwright's headless Chromium, or an installed Chromium browser.

    **Why (2026-11-24):** the Mac's `ms-playwright` cache was gone - a
    storage clean-up takes it - and every take stopped with "Executable
    doesn't exist" until `playwright install` downloaded it again. An
    installed Chrome, Chromium, Brave or Edge runs the same takes headless,
    in a throwaway profile of Playwright's own (no sign-ins, no history).
    """
    try:
        return await p.chromium.launch(args=args)
    except Exception as e:                          # noqa: BLE001
        if "Executable doesn't exist" not in str(e):
            raise
        for exe in INSTALLED:
            if Path(exe).exists():
                print(f"screen: Playwright's Chromium is not installed - "
                      f"using {Path(exe).name}")
                return await p.chromium.launch(executable_path=exe, args=args)
        raise


YOUTUBE_DARK = [{"name": "PREF", "value": "f6=400&hl=en", "domain": ".youtube.com",
                 "path": "/"}]


def _digest(take) -> str:
    d = {"kind": type(take).__name__, "v": VERSION, **take.__dict__}
    for k in ("cookies", "before"):
        if not d.get(k):
            d.pop(k, None)             # takes from before these keep their digest
    if d.get("before"):
        d["before_v"] = 2              # 2: no resting cursor, mouse parked (2026-11-25)
    raw = json.dumps(d, sort_keys=True, default=str)
    if isinstance(take, Terminal):
        raw += TERM_PAGE.read_text()
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def address(url: str) -> str:
    """What a browser's address bar shows: no scheme, no trailing slash."""
    return url.split("://", 1)[-1].rstrip("/")


def shot(take, file: str, *, color=(255, 219, 112), vertical: bool = False,
         window=None, at: float = 0.0, where: Path | None = None, **opts):
    """The `Shot` for a take, in any channel's project: recorded to
    `where/<file>.mp4` (default `TAKES`) and cut by `core/screenrec.py` when
    the render starts (`render_long` / `render_crypto_short` call
    `screenrec.make_pending()`), not when the project is imported.

    `color` is the click ripple's - the brand's `primary`. The window
    defaults to a browser showing the take's address, or a terminal; in
    16:9 it is the wide one. A Short plays a terminal in its own narrow
    screen with no zoom, so the lines wrap rather than run off the side.
    `opts` go to `screenrec.Spec` (`crop=`, `blur=`, `zoom=`, `idle=`,
    `trim=`); `at` skips into the cut (read it off the render's report)."""
    from dataclasses import replace
    from . import screenrec
    from ..crypto.shots import Shot
    term = isinstance(take, Terminal)
    if window is None:
        window = ("terminal", "") if term else ("browser", address(take.url))
    if isinstance(window, str):
        window = (window, "")
    if not vertical and len(window) == 2:
        window = (*window, "wide")
    if term:
        # The type is already big; a closer camera only cuts lines (a
        # Short's terminal is drawn at the window's size, so none at all).
        opts.setdefault("zoom", 1.0 if vertical else 1.5)
        if vertical and take.viewport == Terminal.viewport:
            take = replace(take, viewport=TERM_VERTICAL)
    src = Path(where or TAKES) / f"{file}{'-v' if term and vertical else ''}.mp4"
    clip = screenrec.path(src, vertical=vertical, color=tuple(color),
                          wide=len(window) > 2, take=take, **opts)
    return Shot(clip=clip, raw=True, window=window, clip_at=at)


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
        self.focus = []         # (t, x, y): a highlight being drawn - `mark`
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
          "scrolls": log.scrolls, "focus": log.focus}
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
        browser = await _launch(p, [f"--force-device-scale-factor={take.scale}"])
        is_term = isinstance(take, Terminal)
        ctx = await browser.new_context(
            viewport={"width": vw, "height": vh}, device_scale_factor=take.scale,
            color_scheme="dark" if (is_term or take.dark) else "light",
            locale="en-US", timezone_id="UTC")
        if not is_term:
            sel = ", ".join(list(CONSENT) + list(take.hide))
            await ctx.add_init_script(_UNCONSENT % json.dumps(sel))
        page = await ctx.new_page()
        if is_term:
            await page.goto(TERM_PAGE.as_uri())
            await page.evaluate("([f, t]) => term.setup(f, t)",
                                [take.font, take.title])
        else:
            if getattr(take, "cookies", None):
                await ctx.add_cookies(take.cookies)
            await page.goto(take.url, wait_until="load", timeout=60000)
            await _decline(page)
            try:
                await page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            await _hide(page, take.hide)
            for st in getattr(take, "before", None) or []:
                if st["do"] == "click":
                    await page.locator(st["target"]).first.click(timeout=15000)
                elif st["do"] == "js":
                    await page.evaluate(st["code"])
                elif st["do"] == "wait":
                    await page.wait_for_timeout(st["secs"] * 1000)
                else:
                    raise ValueError(f"before: {st['do']!r} is not a setup step")
            if getattr(take, "before", None):
                # The mouse parked in an empty corner: left where the setup
                # click was, it hovered the first video card through the take.
                await page.mouse.move(2, take.viewport[1] - 2)
                await page.wait_for_timeout(400)
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
        # Where the hand rests - only in a take that uses the mouse: a take
        # of scrolls alone drew a still pointer over the page (2026-11-25,
        # "don't hover any video with the mouse").
        if not is_term and any(st.get("do") in ("move", "click", "type") or
                               (st.get("do") == "scroll" and st.get("at"))
                               for st in take.steps):
            log.at(vw * 0.62, vh * 0.58)
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


# **Ad slots collapse, everywhere** (2026-11-23, the editor: "when showing
# screenshots from tinnitus and crypto make sure there is no gap from ads").
# Headless gets no ad, but the slot still reserves its box: tinnitushelp.me
# showed a band of empty page between its menu and "VIDEOS". Hidden by style
# only - removing a node React rendered breaks the page's next update.
ADS = ("ins.adsbygoogle", "div:has(> ins.adsbygoogle)", ".ad-slot",
       "[data-ad-slot]", "iframe[id^='aswift']", "div[id^='google_ads']")


async def _decline(page):
    """A consent *page* in place of the one asked for - YouTube from the EU
    redirects to consent.youtube.com - answered "Reject all", before the
    recording starts, in the take's throwaway profile.

    **Why (2026-11-24, the channel pages):** a consent *layer* is removed
    (`_UNCONSENT`), never clicked; a whole page in its place cannot be
    removed, and declining is the privacy-keeping answer - nothing of
    anyone's is accepted. Not on camera: the screencast starts after."""
    if "consent." not in page.url:
        return
    btn = page.get_by_role("button", name="Reject all").first
    await btn.click(timeout=15000)
    await page.wait_for_url(lambda u: "consent." not in u, timeout=30000)
    await page.wait_for_load_state("load")


async def _hide(page, hide):
    css = ", ".join(list(CONSENT) + list(ADS) + list(hide))
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
    elif do == "mark":
        x, y = await page.evaluate(s["code"])
        log.focus.append([round(log.now(), 4), round(x, 2), round(y, 2)])
        await asyncio.sleep(s["secs"])
        log.focus.append([round(log.now(), 4), round(x, 2), round(y, 2)])
    elif do == "cmd":
        await page.evaluate("([p, m]) => term.prompt(p, m)",
                            [s["prompt"], bool(s.get("mark"))])
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
