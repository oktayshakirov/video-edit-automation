"""Screen recordings that read on a phone: record the Mac screen with a log of
the cursor, clicks and typing, then re-cut it offline with a camera that
zooms to where the work happens.

Built for OktAI (2026-11-21), where the proof is the real screen: a terminal
running Claude Code, a dashboard, a page we built. A raw full-screen
recording is unreadable in a video - a 3024px Retina screen shown 1536px
wide halves every letter, and the eye does not know where to look. Tools
like Screen Studio solve it with an automatic camera; this is that, offline
and repeatable, in the brand's own frame.

**Two steps, like `screencap`: capture once, move offline.**

    tools/screenrec.py record NAME FILE         # Ctrl+C to stop
    Shot(clip=screenrec.path(src, ...), raw=True,
         window=("terminal", "", "wide"))       # in the project
    screenrec.make_pending()                    # before the render

`record` runs ffmpeg's `avfoundation` screen capture and, beside it, polls
CoreGraphics at 60 Hz for the cursor position and the *times* of clicks,
key presses and scrolls - never which key: the log cannot leak a password
typed on camera. It is `FILE.events.json` next to `FILE.mov`. ffmpeg's own
progress reports give the wall-clock time of the first frame, so the log
and the picture line up to a frame or two. A QuickTime recording with no log
works too: the camera then follows what changes on screen (below).

The render, per output frame:

* **Idle is sped up.** A stretch with no input and nothing moving for more
  than `IDLE_AFTER` seconds - a page loading, a model thinking - plays at
  `idle`x (4 by default), keeping `IDLE_KEEP` at each end at real speed so
  the cut into and out of it is not a jump.
* **The camera.** A click zooms in on it (`zoom`: 1.8, 2.2 in 9:16) a third of
  a second *before* it lands, so the viewer is already looking when it
  happens; more clicks and typing nearby hold the zoom, the camera follows
  the cursor, and a scroll or `HOLD` seconds of nothing zooms back out.
  Typing with no click near it (a terminal) zooms to where the screen is
  changing - the text appearing. Every move is a critically damped spring,
  never a cut.
* **A gold ripple** on every click, in the brand colour.
* **Blur** - `blur=[(x0, y0, x1, y1), ...]` in fractions of the screen,
  optionally `(..., t0, t1)` in recording seconds: a coarse mosaic over
  anything private (an email, a balance, a key). Mosaic, not a Gaussian:
  small blurred text can be read back; 1/60-of-the-screen blocks cannot.
* `crop=(x0, y0, x1, y1)` - the part of the screen the video is about (the
  browser's page without its tabs and bookmarks, one terminal pane). The
  camera never leaves it.

The output is a frame-sized clip (1920x1080, or 1080x1920 with
`vertical=True`) whose picture fills exactly the area `window=` shows, so
`Shot(clip=..., raw=True, window=(...))` frames it in a browser or terminal
over the night sky with no second crop. `raw=True` stops `VideoShot`
greying the type and pushing in on top of this camera. Without a window,
the landscape clip fills the frame; the vertical one needs a window.

Without an event log, the camera reads the screen itself: changes between
frames at 10 fps, small and in one place (typing, a spinner, a result
appearing) pull the camera there; a large change (a scroll, a new page)
zooms out. It is a fallback - record with `tools/screenrec.py` when you can.
"""

from __future__ import annotations

import ctypes
import ctypes.util
import hashlib
import json
import math
import subprocess
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

FPS = 30
POLL = 60                 # Hz, the event log
IDLE_AFTER = 1.2          # s of nothing before a stretch counts as idle
IDLE_KEEP = 0.35          # s at each end of an idle stretch kept at 1x
LEAD = 0.35               # s the camera moves before a click lands
HOLD = 2.2                # s the zoom holds after the last nearby input
NEAR = 0.30               # a click this far away (of the width) re-aims
RIPPLE = 0.55             # s a click ripple lasts
MOSAIC = 60               # blur blocks across the screen's width
VERSION = 1               # bump when the render changes, to re-make caches


# -- recording ------------------------------------------------------------

class _CG:
    """The few CoreGraphics calls the log needs, through ctypes - no
    pyobjc, and none of them needs Accessibility or Input Monitoring."""

    LEFT_DOWN, RIGHT_DOWN, KEY_DOWN, SCROLL = 1, 3, 10, 22
    STATE = 0                      # kCGEventSourceStateCombinedSessionState

    def __init__(self):
        class P(ctypes.Structure):
            _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]

        class S(ctypes.Structure):
            _fields_ = [("w", ctypes.c_double), ("h", ctypes.c_double)]

        class R(ctypes.Structure):
            _fields_ = [("o", P), ("s", S)]

        cg = ctypes.CDLL(ctypes.util.find_library("CoreGraphics"))
        cf = ctypes.CDLL(ctypes.util.find_library("CoreFoundation"))
        cg.CGEventCreate.restype = ctypes.c_void_p
        cg.CGEventCreate.argtypes = [ctypes.c_void_p]
        cg.CGEventGetLocation.restype = P
        cg.CGEventGetLocation.argtypes = [ctypes.c_void_p]
        cg.CGEventSourceSecondsSinceLastEventType.restype = ctypes.c_double
        cg.CGEventSourceSecondsSinceLastEventType.argtypes = [ctypes.c_int,
                                                              ctypes.c_uint32]
        cg.CGMainDisplayID.restype = ctypes.c_uint32
        cg.CGDisplayBounds.restype = R
        cg.CGDisplayBounds.argtypes = [ctypes.c_uint32]
        cf.CFRelease.argtypes = [ctypes.c_void_p]
        self.cg, self.cf = cg, cf

    def cursor(self) -> tuple[float, float]:
        e = self.cg.CGEventCreate(None)
        p = self.cg.CGEventGetLocation(e)
        self.cf.CFRelease(e)
        return p.x, p.y

    def since(self, kind: int) -> float:
        return self.cg.CGEventSourceSecondsSinceLastEventType(self.STATE, kind)

    def display(self) -> dict:
        b = self.cg.CGDisplayBounds(self.cg.CGMainDisplayID())
        return {"x": b.o.x, "y": b.o.y, "w": b.s.w, "h": b.s.h}


class Logger:
    """Polls the cursor and the input clocks on a thread; wall-clock times."""

    def __init__(self, cg=None, rate: int = POLL):
        self.cg = cg or _CG()
        self.rate = rate
        self.samples: list = []
        self.events = {"clicks": [], "keys": [], "scrolls": []}
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self._thread.start()
        return self

    def stop(self):
        self._stop.set()
        self._thread.join()

    def _run(self):
        cg = self.cg
        kinds = {"clicks": (cg.LEFT_DOWN, cg.RIGHT_DOWN), "keys": (cg.KEY_DOWN,),
                 "scrolls": (cg.SCROLL,)}
        # The clocks say how long ago the last event of a kind was; an event
        # is new when that moment moves later. Two key presses inside one
        # 16ms poll count as one, which is all a camera needs.
        now = time.time()
        last = {k: max(now - cg.since(c) for c in cs) for k, cs in kinds.items()}
        step = 1.0 / self.rate
        while not self._stop.is_set():
            now = time.time()
            x, y = cg.cursor()
            self.samples.append((round(now, 4), round(x, 1), round(y, 1)))
            for k, cs in kinds.items():
                at = max(now - cg.since(c) for c in cs)
                if at > last[k] + 0.004:
                    last[k] = at
                    if k == "clicks":
                        self.events[k].append((round(at, 4), round(x, 1), round(y, 1)))
                    else:
                        self.events[k].append(round(at, 4))
            self._stop.wait(max(0.0, step - (time.time() - now)))


def screen_device() -> str:
    """avfoundation's index for the main screen ("Capture screen 0")."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-f", "avfoundation",
                          "-list_devices", "true", "-i", ""],
                         capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Capture screen 0" in line:
            return line.split("[")[-1].split("]")[0]
    raise RuntimeError("no screen in `ffmpeg -f avfoundation -list_devices "
                       "true -i ''` - is this a Mac?")


def record(out: Path, secs: float | None = None, fps: int = FPS,
           source: list[str] | None = None, logger: Logger | None = None,
           say=print) -> Path:
    """Record the main screen to `out` (.mov) and its log beside it.

    Stops after `secs`, or on Ctrl+C. `source` replaces the avfoundation
    input (tests use a lavfi pattern). The terminal running this needs
    Screen Recording permission (System Settings, Privacy & Security); the
    first run asks for it, and a refused capture never delivers a frame, so
    a run that has none after ten seconds stops and says so.
    """
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if source is None:
        source = ["-f", "avfoundation", "-capture_cursor", "1",
                  "-pixel_format", "nv12", "-framerate", str(fps),
                  "-i", f"{screen_device()}:none"]
    cmd = (["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + source
           + (["-t", str(secs)] if secs else [])
           + ["-c:v", "h264_videotoolbox", "-b:v", "24M", "-pix_fmt", "yuv420p",
              "-r", str(fps), "-progress", "pipe:1", "-stats_period", "0.1",
              str(out)])
    log = (logger or Logger()).start()
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True)
    starts: list[float] = []

    def progress():
        # The first frame's wall time is (now - out_time) at every report;
        # the smallest is the one with the least pipe delay.
        for line in proc.stdout:
            if line.startswith("out_time_us="):
                v = line.split("=", 1)[1].strip()
                if v.isdigit() and int(v) > 0:
                    starts.append(time.time() - int(v) / 1e6)

    reader = threading.Thread(target=progress, daemon=True)
    reader.start()
    began = time.time()
    try:
        while proc.poll() is None:
            if not starts and time.time() - began > 10:
                proc.kill()
                raise RuntimeError(
                    "no frames after 10s - give this terminal Screen Recording "
                    "permission (System Settings > Privacy & Security), then "
                    "quit and reopen it")
            time.sleep(0.1)
    except KeyboardInterrupt:
        say("stopping...")
        try:
            proc.stdin.write("q")
            proc.stdin.flush()
        except (BrokenPipeError, OSError):
            pass
        proc.wait(timeout=30)
    finally:
        log.stop()
        reader.join(timeout=5)
    err = proc.stderr.read()
    if proc.returncode not in (0, 255) or not out.exists():
        raise RuntimeError(f"ffmpeg failed: {err[-800:]}")
    if not starts:
        raise RuntimeError("ffmpeg reported no progress - cannot sync the log")
    t0 = min(starts)
    rel = lambda t: round(t - t0, 4)
    data = {
        "version": 1,
        "display": log.cg.display() if hasattr(log.cg, "display") else None,
        "video_start": t0,
        "samples": [(rel(t), x, y) for t, x, y in log.samples if t >= t0 - 1],
        "clicks": [(rel(t), x, y) for t, x, y in log.events["clicks"]],
        "keys": [rel(t) for t in log.events["keys"]],
        "scrolls": [rel(t) for t in log.events["scrolls"]],
    }
    events_path(out).write_text(json.dumps(data))
    return out


def events_path(video: Path) -> Path:
    return Path(video).with_suffix(".events.json")


# -- reading a recording ------------------------------------------------------

@dataclass
class Events:
    """The log in recording seconds and source pixels."""
    t: np.ndarray                 # cursor samples
    x: np.ndarray
    y: np.ndarray
    clicks: list                  # (t, x, y)
    keys: np.ndarray
    scrolls: np.ndarray

    @classmethod
    def load(cls, path: Path, size: tuple[int, int], shift: float = 0.0
             ) -> "Events | None":
        """`size` is the video's (w, h): points times the Retina scale.
        `shift` moves every event later by that many seconds - the manual fix
        if the ripples ever land before or after the cursor clicks."""
        path = Path(path)
        if not path.exists():
            return None
        d = json.loads(path.read_text())
        disp = d.get("display") or {"x": 0, "y": 0, "w": size[0], "h": size[1]}
        sx, sy = size[0] / disp["w"], size[1] / disp["h"]
        px = lambda x, y: ((x - disp["x"]) * sx, (y - disp["y"]) * sy)
        s = np.array(d["samples"], float).reshape(-1, 3)
        xs, ys = px(s[:, 1], s[:, 2])
        return cls(t=s[:, 0] + shift, x=xs, y=ys,
                   clicks=[(t + shift, *px(x, y)) for t, x, y in d["clicks"]],
                   keys=np.array(d["keys"], float) + shift,
                   scrolls=np.array(d["scrolls"], float) + shift)

    def cursor(self, t: float) -> tuple[float, float]:
        if not len(self.t):
            return (float("nan"), float("nan"))
        return (float(np.interp(t, self.t, self.x)),
                float(np.interp(t, self.t, self.y)))


def probe(path: Path) -> tuple[int, int, float]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height:format=duration",
                          "-of", "json", str(path)],
                         capture_output=True, text=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    return int(s["width"]), int(s["height"]), float(d["format"]["duration"])


def motion(path: Path, rate: int = 10, width: int = 384,
           ev: "Events | None" = None) -> dict:
    """What changes on screen, `rate` times a second, at low resolution:
    the share of pixels that changed, and the box around them (fractions).
    With a log, the cursor's own trail is masked out first - a moving arrow
    is not the screen changing."""
    W, H, _ = probe(path)
    h = int(round(width * H / W / 2)) * 2
    proc = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf",
         f"fps={rate},scale={width}:{h},format=gray", "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE)
    n = width * h
    cw, ch = max(3, int(width * 0.016)), max(4, int(h * 0.035))
    prev, frac, boxes = None, [], []
    i = 0
    while True:
        buf = proc.stdout.read(n)
        if len(buf) < n:
            break
        g = np.frombuffer(buf, np.uint8).reshape(h, width).astype(np.int16)
        if prev is None:
            frac.append(0.0)
            boxes.append(None)
        else:
            m = np.abs(g - prev) > 12
            if ev is not None and len(ev.t):
                for t in (i / rate, (i - 1) / rate):
                    x, y = ev.cursor(t)
                    x, y = int(x / W * width), int(y / H * h)
                    m[max(0, y - 2):y + ch, max(0, x - 2):x + cw] = False
            share = float(m.mean())
            frac.append(share)
            if share > 0:
                ys, xs = np.nonzero(m)
                boxes.append((xs.min() / width, ys.min() / h,
                              (xs.max() + 1) / width, (ys.max() + 1) / h))
            else:
                boxes.append(None)
        prev = g
        i += 1
    proc.wait()
    return {"rate": rate, "frac": np.array(frac), "boxes": boxes}


# -- the plan: time map and camera -----------------------------------------

def busy(duration: float, ev: Events | None, mot: dict, fps: int = FPS
         ) -> np.ndarray:
    """Per source frame: is anything happening (input, or the picture moving
    more than a cursor's worth)?"""
    n = max(1, int(math.ceil(duration * fps)))
    t = np.arange(n) / fps
    on = np.zeros(n, bool)
    if ev is not None:
        pts = [c[0] for c in ev.clicks] + list(ev.keys) + list(ev.scrolls)
        if len(ev.t) > 1:
            speed = np.hypot(np.diff(ev.x), np.diff(ev.y)) / np.maximum(np.diff(ev.t), 1e-3)
            pts += list(ev.t[1:][speed > 40])          # px/s: the hand is moving
        for p in pts:
            on |= np.abs(t - p) < 0.5
    r = mot["rate"]
    for i, share in enumerate(mot["frac"]):
        if share > 0.002:
            on[int(i / r * fps): int((i + 1) / r * fps) + 1] = True
    return on


def time_map(on: np.ndarray, idle: float, fps: int = FPS,
             trim: tuple | None = None) -> np.ndarray:
    """Source seconds for each output frame: idle stretches at `idle`x."""
    n = len(on)
    speed = np.ones(n)
    if idle and idle > 1:
        i = 0
        while i < n:
            if on[i]:
                i += 1
                continue
            j = i
            while j < n and not on[j]:
                j += 1
            if (j - i) / fps > IDLE_AFTER:
                k = int(IDLE_KEEP * fps)
                speed[i + k: j - k] = idle
            i = j
    a, b = (0.0, n / fps) if trim is None else trim
    out, t = [], a
    while t < min(b, n / fps) - 1e-6:
        out.append(t)
        t += speed[min(n - 1, int(t * fps))] / fps
    return np.array(out) if out else np.array([a])


@dataclass
class Aim:
    """Targets for the camera, per output frame, before smoothing."""
    zoom: np.ndarray
    cx: np.ndarray
    cy: np.ndarray


LOCAL = 0.06              # a change under this share of the screen is local
BIG = 0.20                # one over this is a new page or a scroll


def _local(share: float, box) -> bool:
    # One typed character on a Retina screen is ~0.01% of it at the motion
    # pass's resolution, so the floor is just above noise.
    return (box is not None and 0.00003 <= share < LOCAL
            and box[2] - box[0] < 0.5 and box[3] - box[1] < 0.5)


def change_runs(mot: dict, min_len: float = 0.3) -> list[tuple]:
    """Stretches where the screen changes in one place for a while - text
    typing on, a result arriving: (t0, t1, union box)."""
    r, runs, cur = mot["rate"], [], None
    for i, (share, box) in enumerate(zip(mot["frac"], mot["boxes"])):
        if _local(share, box):
            if cur and i - cur[1] <= 3:
                b = cur[2]
                cur = [cur[0], i, (min(b[0], box[0]), min(b[1], box[1]),
                                   max(b[2], box[2]), max(b[3], box[3]))]
            else:
                if cur:
                    runs.append(cur)
                cur = [i, i, box]
    if cur:
        runs.append(cur)
    # A blinking caret is a run too, forever, in one character cell: a run
    # counts only once it has grown past one (3% of the screen) and changed
    # more than a few characters' worth in all.
    frac = mot["frac"]
    return [(a / r, (b + 1) / r, box) for a, b, box in runs
            if (b + 1 - a) / r >= min_len
            and max(box[2] - box[0], box[3] - box[1]) >= 0.03
            and float(frac[a:b + 1].sum()) >= 0.001]


def _base(region: tuple, aspect: float) -> tuple[float, float]:
    """The widest box with the output's shape inside the region, in pixels."""
    rw, rh = region[2] - region[0], region[3] - region[1]
    return (rh * aspect, rh) if rw / rh > aspect else (rw, rw / aspect)


def targets(src_t: np.ndarray, W: int, H: int, ev: Events | None, mot: dict,
            zoom: float, region: tuple, aspect: float = 16 / 9) -> Aim:
    """Where the camera wants to be. Source pixels; `region` in pixels.

    Attention comes in spans `[t0, t1, focus, kind, zoom]`. Input makes
    them - a click, typing - and so does the screen changing in one place
    for a while (a reply arriving), which is all there is without a log.
    Input wins where they overlap. A scroll, or a change over `BIG` of the
    screen (a new page), ends a span: the viewer needs the whole picture."""
    n = len(src_t)
    rx0, ry0, rx1, ry1 = region
    bw0, bh0 = _base(region, aspect)
    home = ((rx0 + rx1) / 2, (ry0 + ry1) / 2)
    z = np.ones(n)
    cx = np.full(n, home[0])
    cy = np.full(n, home[1])

    spans: list[list] = []
    if ev is not None:
        for t, x, y in ev.clicks:
            if spans and t - spans[-1][1] < HOLD and \
                    math.hypot(x - spans[-1][2][0], y - spans[-1][2][1]) < NEAR * W:
                spans[-1][1] = t + HOLD
                spans[-1][2] = (x, y)
            else:
                spans.append([t - LEAD, t + HOLD, (x, y), "click", zoom])
        for t in ev.keys:
            hit = next((s for s in spans if s[0] <= t <= s[1] + HOLD), None)
            if hit:
                hit[1] = max(hit[1], t + HOLD)
            else:
                spans.append([t - LEAD, t + HOLD, None, "type", zoom])
    inputs = len(spans)
    for t0, t1, b in change_runs(mot):
        bw, bh = b[2] - b[0], b[3] - b[1]
        # Zoom only as far as the whole change still fits, with a margin.
        zz = min(zoom, 0.8 * bw0 / W / max(bw, 1e-3), 0.8 * bh0 / H / max(bh, 1e-3))
        if zz < 1.15:
            continue
        if any(s[0] < t1 and t0 < s[1] for s in spans[:inputs]):
            continue
        spans.append([t0 - LEAD, t1 + HOLD,
                      ((b[0] + b[2]) / 2 * W, (b[1] + b[3]) / 2 * H), "change", zz])
    ends = list(ev.scrolls) if ev is not None else []
    r = mot["rate"]
    ends += [i / r for i, share in enumerate(mot["frac"]) if share > BIG]
    for t in ends:
        for s in spans:
            # Not in the first half second of a click: a button often
            # repaints most of the page the moment it is pressed.
            if s[0] < t < s[1] and not (s[3] == "click" and t - s[0] < LEAD + 0.6):
                s[1] = t
    spans.sort(key=lambda s: (s[3] == "change", s[0]))

    def change_at(t: float, z: float):
        """Where to look while text is appearing: the whole of what changed
        in the last few seconds when it fits the view at zoom `z`, else
        the newest part, kept 85% of the way across."""
        hits = [mot["boxes"][i] for i in range(max(0, int((t - 3.0) * r)),
                                               min(len(mot["boxes"]), int(t * r) + 1))
                if _local(mot["frac"][i], mot["boxes"][i])]
        if not hits:
            return None
        new = hits[-1]
        ux0, ux1 = min(b[0] for b in hits) * W, max(b[2] for b in hits) * W
        ny = (new[1] + new[3]) / 2 * H
        view = bw0 / z
        if ux1 - ux0 <= 0.8 * view:
            return ((ux0 + ux1) / 2, ny)
        return ((new[0] + new[2]) / 2 * W - 0.35 * view, ny)

    clicks = sorted(c[0] for c in ev.clicks) if ev is not None else []
    keys = ev.keys if ev is not None else np.array([])
    for k, t in enumerate(src_t):
        tl = t + LEAD
        s = next((s for s in spans if s[0] <= tl <= s[1]), None)
        if s is None:
            continue
        z[k] = s[4]
        if s[3] in ("type", "change"):
            f = change_at(t, s[4]) or s[2] or (ev.cursor(t) if ev is not None else home)
        elif s[3] == "click":
            # Aim at the click before it lands, then follow the hand - or,
            # while keys are pressed, the text appearing (it runs away from
            # the cursor, which stays where it clicked).
            done = any(s[0] <= c <= t for c in clicks)
            typing = len(keys) and np.any((keys > t - 1.0) & (keys <= t))
            f = ((typing and change_at(t, s[4])) or ev.cursor(t)) if done else s[2]
        else:
            f = s[2]
        if f is not None and not any(map(math.isnan, f)):
            cx[k], cy[k] = f
    return Aim(z, cx, cy)


def spring(x: np.ndarray, omega: float, fps: int = FPS) -> np.ndarray:
    """A critically damped spring chasing `x`: no overshoot, no cut."""
    out = np.empty_like(x, dtype=float)
    p, v = float(x[0]), 0.0
    dt = 1.0 / fps
    for i, target in enumerate(x):
        a = omega * omega * (target - p) - 2 * omega * v
        v += a * dt
        p += v * dt
        out[i] = p
    return out


def camera(t: Aim, W: int, H: int, region: tuple, aspect: float
           ) -> np.ndarray:
    """Smoothed crop boxes (x0, y0, w, h) in source pixels, per frame."""
    z = spring(t.zoom, 5.0)
    cx, cy = spring(t.cx, 4.0), spring(t.cy, 4.0)
    rx0, ry0, rx1, ry1 = region
    bw, bh = _base(region, aspect)
    w, h = bw / np.maximum(z, 1.0), bh / np.maximum(z, 1.0)
    x0 = np.clip(cx - w / 2, rx0, rx1 - w)
    y0 = np.clip(cy - h / 2, ry0, ry1 - h)
    return np.stack([x0, y0, w, h], axis=1)


# -- the render ----------------------------------------------------------------

def content_rect(size: tuple[int, int], vertical: bool, wide: bool = True
                 ) -> tuple[int, int, int, int]:
    """Where the picture goes in the output frame: the area `WindowShot`
    keeps (it trims the inner frame's edges, then centre-crops to its
    content's shape), so a window shows it without a second crop."""
    from .frame import LANDSCAPE, VERTICAL
    from .window import layout
    L = layout(VERTICAL if vertical else LANDSCAPE, wide=wide)
    want = L.w / L.ch
    W, H = size
    e = max(4, int(min(W, H) * 0.006))
    iw, ih = W - 2 * e, H - 2 * e
    if iw / ih > want:
        cw, ch = int(round(ih * want)), ih
    else:
        cw, ch = iw, int(round(iw / want))
    return ((W - cw) // 2, (H - ch) // 2, cw, ch)


def _mosaic(img: np.ndarray, box: tuple, block: int) -> None:
    import cv2
    x0, y0, x1, y1 = box
    roi = img[y0:y1, x0:x1]
    if roi.size == 0:
        return
    h, w = roi.shape[:2]
    small = cv2.resize(roi, (max(1, w // block), max(1, h // block)),
                       interpolation=cv2.INTER_AREA)
    img[y0:y1, x0:x1] = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)


def _view(src: np.ndarray, box, cw: int, ch: int) -> np.ndarray:
    """The crop box, resampled to (cw, ch) at sub-pixel position: an area
    resize for the scale (no shimmer on text), then a fractional shift."""
    import cv2
    x0, y0, w, h = box
    s = cw / w
    ix0, iy0 = int(math.floor(x0)), int(math.floor(y0))
    ix1 = min(src.shape[1], int(math.ceil(x0 + w)) + 2)
    iy1 = min(src.shape[0], int(math.ceil(y0 + h)) + 2)
    part = src[iy0:iy1, ix0:ix1]
    pw, ph = max(1, int(round(part.shape[1] * s))), max(1, int(round(part.shape[0] * s)))
    part = cv2.resize(part, (pw, ph), interpolation=cv2.INTER_AREA if s < 1
                      else cv2.INTER_CUBIC)
    m = np.float32([[1, 0, -(x0 - ix0) * s], [0, 1, -(y0 - iy0) * s]])
    return cv2.warpAffine(part, m, (cw, ch), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_REPLICATE)


@dataclass
class Spec:
    src: Path
    vertical: bool = False
    zoom: float | None = None     # 1.8, or 2.2 in 9:16 (a phone screen)
    idle: float = 4.0
    crop: tuple | None = None
    blur: tuple = ()
    trim: tuple | None = None
    ripples: bool = True
    wide: bool = True
    color: tuple = (255, 219, 112)
    shift: float = 0.0            # seconds, see `Events.load`

    def __post_init__(self):
        if self.zoom is None:
            self.zoom = 2.2 if self.vertical else 1.8

    def key(self) -> str:
        st = Path(self.src).stat()
        ev = events_path(self.src)
        evs = ev.stat().st_mtime if ev.exists() else 0
        raw = (f"{VERSION}|{Path(self.src).resolve()}|{st.st_size}|{st.st_mtime}|"
               f"{evs}|{self.vertical}|{self.zoom}|{self.idle}|{self.crop}|"
               f"{tuple(map(tuple, self.blur))}|{self.trim}|{self.ripples}|"
               f"{self.wide}|{self.color}|{self.shift}")
        return hashlib.sha1(raw.encode()).hexdigest()[:8]

    def out(self) -> Path:
        src = Path(self.src)
        kind = "9x16" if self.vertical else "16x9"
        return src.parent / ".render" / f"{src.stem}-{kind}-{self.key()}.mp4"


def render(spec: Spec, out: Path | None = None, say=print) -> Path:
    import cv2
    src = Path(spec.src)
    out = Path(out) if out else spec.out()
    W, H, dur = probe(src)
    ev = Events.load(events_path(src), (W, H), spec.shift)
    mot = motion(src, ev=ev)
    region = (0, 0, W, H) if spec.crop is None else (
        spec.crop[0] * W, spec.crop[1] * H, spec.crop[2] * W, spec.crop[3] * H)

    on = busy(dur, ev, mot)
    src_t = time_map(on, spec.idle, trim=spec.trim)
    size = (1080, 1920) if spec.vertical else (1920, 1080)
    rx, ry, cw, ch = content_rect(size, spec.vertical, spec.wide)
    tg = targets(src_t, W, H, ev, mot, spec.zoom, region, cw / ch)
    boxes = camera(tg, W, H, region, cw / ch)

    blocks = max(8, W // MOSAIC)
    blur = []
    for b in spec.blur:
        x0, y0, x1, y1 = (int(b[0] * W), int(b[1] * H), int(math.ceil(b[2] * W)),
                          int(math.ceil(b[3] * H)))
        t0, t1 = (b[4], b[5]) if len(b) >= 6 else (-1e9, 1e9)
        blur.append(((x0, y0, x1, y1), t0, t1))

    # Clicks on the output timeline: the first output frame at or after each.
    clicks = []
    if ev is not None and spec.ripples:
        for t, x, y in ev.clicks:
            k = int(np.searchsorted(src_t, t))
            if 0 <= k < len(src_t) and src_t[k] - t < 0.2:
                clicks.append((k, x, y))

    out.parent.mkdir(parents=True, exist_ok=True)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(src), "-vf",
                            f"fps={FPS}", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
                           stdout=subprocess.PIPE)
    tmp = out.with_suffix(".part.mp4")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-s", f"{size[0]}x{size[1]}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264",
                            "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p",
                            "-movflags", "+faststart", str(tmp)],
                           stdin=subprocess.PIPE)
    n = W * H * 3
    idx, frame = -1, None
    canvas = np.zeros((size[1], size[0], 3), np.uint8)
    canvas[:] = (6, 6, 9)
    ring = tuple(int(c) for c in spec.color)
    try:
        for k, t in enumerate(src_t):
            want = min(int(round(t * FPS)), int(dur * FPS) - 1)
            while idx < want:
                buf = dec.stdout.read(n)
                if len(buf) < n:
                    break
                idx += 1
                frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
            if frame is None:
                break
            img = frame
            live = [b for b, t0, t1 in blur if t0 <= t <= t1]
            if live:
                img = frame.copy()
                for b in live:
                    _mosaic(img, b, blocks)
            box = boxes[k]
            view = np.ascontiguousarray(_view(img, box, cw, ch))
            s = cw / box[2]
            for ck, x, y in clicks:
                age = (k - ck) / FPS
                if 0 <= age < RIPPLE:
                    p = age / RIPPLE
                    e = 1 - (1 - p) ** 3
                    r = int(10 + 34 * e * max(1.0, s * 0.6))
                    a = (1 - p) ** 1.5
                    px, py = int((x - box[0]) * s), int((y - box[1]) * s)
                    over = view.copy()
                    cv2.circle(over, (px, py), r, ring, max(2, int(5 * (1 - p) + 2)),
                               cv2.LINE_AA)
                    if p < 0.35:
                        cv2.circle(over, (px, py), 9, ring, -1, cv2.LINE_AA)
                    view = cv2.addWeighted(over, a, view, 1 - a, 0)
            canvas[ry:ry + ch, rx:rx + cw] = view
            enc.stdin.write(canvas.tobytes())
            if k % (FPS * 10) == 0:
                say(f"  {k / FPS:5.1f}s of {len(src_t) / FPS:.1f}s")
    finally:
        enc.stdin.close()
        enc.wait()
        dec.stdout.close()
        dec.kill()
        dec.wait()
    if enc.returncode != 0:
        raise RuntimeError(f"encoding {out.name} failed")
    tmp.replace(out)
    report = {"source": str(src), "seconds_in": round(dur, 2),
              "seconds_out": round(len(src_t) / FPS, 2),
              "log": ev is not None, "clicks": len(ev.clicks) if ev else 0,
              "zoomed_share": round(float((tg.zoom > 1.01).mean()), 3)}
    out.with_suffix(".json").write_text(json.dumps(report, indent=1))
    return out


# -- in a project ---------------------------------------------------------------

_PENDING: dict[Path, Spec] = {}


def path(src: Path, **opts) -> Path:
    """Where the render of `src` with these options goes - without making
    it, so a gate that imports a script renders nothing. `make_pending()`
    (called by `oktai.build_long` / `build_short`) makes every one asked for."""
    spec = Spec(Path(src).expanduser(), **opts)
    out = spec.out()
    _PENDING[out] = spec
    return out


def make_pending(say=print) -> list[Path]:
    made = []
    for out, spec in list(_PENDING.items()):
        if not out.exists():
            say(f"screen: {Path(spec.src).name} -> {out.name}")
            render(spec, out, say=say)
            made.append(out)
    return made


if __name__ == "__main__":       # pragma: no cover
    sys.exit("use tools/screenrec.py")
