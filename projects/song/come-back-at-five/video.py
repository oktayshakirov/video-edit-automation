"""The music video for "Come Back at Five": 16:9 for YouTube, 9:16 for Shorts.

    .venv/bin/python projects/song/come-back-at-five/video.py long|short [--from S --to S] [--still S]

Karaoke lyrics over one drawn scene per line: a parody chat window, a
terminal, Noto's animated emoji, a usage bar, a clock running to five, and
three `behind` shots (the word set between a photo's room and its subject).
The whole song in both formats (the user's call, 2026-11-06).

Look, decided with the user 2026-11-06: neutral, no watermark, no Claude
logo or anything copied from Claude's interface. The chat is a generic
window that says "Claude" in our own type; the song's own rule
(create-song-automation docs/originality.md) is no logo and nothing that
reads as official.

Timing comes from `timing.py` (`timing.json`): every word's start and end
in the final mix. Scenes are keyed to the lines, so a re-timed word moves
its picture with it.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))

from video_automation.core import emoji_anim, shaderfx  # noqa: E402
from video_automation.core.brand import BRANDS, Brand  # noqa: E402
from video_automation.core.frame import LANDSCAPE, VERTICAL, Frame  # noqa: E402
from video_automation.core.vertical import emoji_image  # noqa: E402
from video_automation.longform.overlay import TvOff  # noqa: E402

FPS = 30
END = 121.83                 # the video's last frame time; the TV switches off into it
AUDIO = Path.home() / "Desktop/songs/come-back-at-five-final.flac"
MIX = Path.home() / ".cache/video-automation/song/come-back-at-five/mix.wav"
OUT = Path.home() / "Desktop/songs/video"
STOCK = REPO / "assets/stock/photos"
PHOTO = {
    "grass": STOCK / "man-lying-on-grass-relaxing/25835010.jpg",
    "manager": STOCK / "angry-boss-in-suit-office/7794084.jpg",
    "outside": STOCK / "man-arms-open-nature-sunshine/35933169.jpg",
}

# Palette: a dark terminal with one warm accent. Not Claude's orange.
BG = (13, 13, 16)
PANEL = (28, 28, 34)
PANEL2 = (40, 40, 48)
INK = (242, 239, 234)
DIM = (120, 118, 128)
ACCENT = (255, 138, 61)
RED = (255, 77, 77)
GREEN = (61, 220, 132)
BLUE = (90, 160, 255)

SONG = Brand(name="song", site="", primary=ACCENT, ink=INK, bg=BG, panel=PANEL,
             negative=RED, strike=RED, grid=PANEL2)
BRANDS[SONG.name] = SONG       # beats look a brand up by name; no logo, no watermark

F_HEAVY = ("/System/Library/Fonts/Avenir Next.ttc", 8)
F_BOLD = ("/System/Library/Fonts/Avenir Next.ttc", 0)
F_MED = ("/System/Library/Fonts/Avenir Next.ttc", 5)
F_COND = ("/System/Library/Fonts/Avenir Next Condensed.ttc", 8)
F_MONO = ("/System/Library/Fonts/Menlo.ttc", 0)
F_MONOB = ("/System/Library/Fonts/Menlo.ttc", 1)


@lru_cache(maxsize=256)
def font(spec, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(spec[0], max(8, int(size)), index=spec[1])


# --------------------------------------------------------------------------
# small motion helpers

def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def pop(x):
    """0 -> 1 with an overshoot, for things that land."""
    x = clamp(x)
    c1 = 1.70158
    return 1 + (c1 + 1) * (x - 1) ** 3 + c1 * (x - 1) ** 2      # ease-out-back


def window(t, a, b, fade=0.18):
    """1 inside [a, b], easing in and out over `fade`."""
    if t < a - fade or t > b + fade:
        return 0.0
    return min(ease((t - (a - fade)) / fade) if t < a else 1.0,
               ease(((b + fade) - t) / fade) if t > b else 1.0)


# --------------------------------------------------------------------------
# timing and audio

TIMING = json.loads((HERE / "timing.json").read_text())["lines"]


def line_at(prefix: str, n: int = 1) -> dict:
    """The n-th sung line whose text starts with `prefix`."""
    hits = [ln for ln in TIMING if ln["text"].lower().startswith(prefix.lower())]
    return hits[n - 1]


def kick_envelope(n_frames: int) -> np.ndarray:
    """Low-end energy per frame, 0..1: the 808s, so things breathe with them."""
    import soundfile as sf
    from scipy.signal import butter, sosfilt
    x, sr = sf.read(MIX, dtype="float32")
    x = x.mean(1) if x.ndim > 1 else x
    low = sosfilt(butter(4, 140, "lowpass", fs=sr, output="sos"), x)
    hop = sr // FPS
    e = np.array([np.sqrt(np.mean(low[i * hop:(i + 1) * hop] ** 2)) for i in range(n_frames)])
    e = e / (np.percentile(e, 98) + 1e-9)
    out = np.zeros_like(e)          # fast attack, slow release
    for i in range(len(e)):
        out[i] = max(e[i], out[i - 1] * 0.86 if i else 0)
    return np.clip(out, 0, 1)


# --------------------------------------------------------------------------
# drawing context

@dataclass
class Ctx:
    frame: Frame
    t: float
    kick: float

    @property
    def W(self):
        return self.frame.w

    @property
    def H(self):
        return self.frame.h

    @property
    def tall(self):
        return self.frame.h > self.frame.w

    @property
    def u(self):            # one unit: 1px at 1080 on the short side
        return min(self.W, self.H) / 1080

    @property
    def cx(self):           # the safe centre, left of a Short's button rail
        return self.W / 2       # centred in both formats (the user's note, 2026-11-06)

    @property
    def stage(self):
        """(x0, y0, x1, y1): where a scene's picture goes, clear of the karaoke."""
        if self.tall:
            return (70, self.frame.safe_top + 20, self.W - 70, 1090)
        return (120, 70, self.W - 120, int(self.H * 0.66))


def emoji(ch: str, h: int, t: float) -> Image.Image:
    im = emoji_anim.frame(ch, int(h), t) if emoji_anim.active() else None
    if im is None:
        im = emoji_image(ch, int(h))
    return im.convert("RGBA")


def paste(base: Image.Image, im: Image.Image, cx, cy, scale=1.0, rot=0.0, alpha=1.0):
    if alpha <= 0.01 or scale <= 0.01:
        return
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))),
                       Image.BICUBIC)
    if rot:
        im = im.rotate(rot, Image.BICUBIC, expand=True)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im = im.copy()
        im.putalpha(a)
    base.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def emo(base, ctx: Ctx, ch, cx, cy, h, t0, rot=0.0, until=None, bounce=True):
    """An emoji that pops in at t0 and bounces on the kick."""
    t = ctx.t
    if t < t0 or (until is not None and t > until + 0.2):
        return
    s = pop((t - t0) / 0.35)
    if until is not None and t > until:
        s *= 1 - ease((t - until) / 0.2)
    s *= 1 + (0.07 * ctx.kick if bounce else 0)
    paste(base, emoji(ch, h, t - t0), cx, cy, s, rot)


def text(d: ImageDraw.ImageDraw, xy, s, f, fill, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def rounded(d, box, r, fill, outline=None, width=0):
    d.rounded_rectangle([int(v) for v in box], radius=int(r), fill=fill, outline=outline,
                        width=int(width))


def fit_font(spec, s: str, max_w: float, size: int) -> ImageFont.FreeTypeFont:
    f = font(spec, size)
    while f.getlength(s) > max_w and size > 14:
        size = int(size * 0.92)
        f = font(spec, size)
    return f


# --------------------------------------------------------------------------
# background

def background(ctx: Ctx, hue=ACCENT, glow_at=(0.5, 0.42)) -> Image.Image:
    W, H = ctx.W, ctx.H
    img = Image.new("RGBA", (W, H), (*BG, 255))
    # a slow glow that swells with the 808
    gx, gy = glow_at
    r = int(min(W, H) * (0.55 + 0.08 * ctx.kick))
    glow = Image.new("L", (W, H), 0)
    gd = ImageDraw.Draw(glow)
    ox = math.sin(ctx.t * 0.31) * W * 0.06
    oy = math.cos(ctx.t * 0.23) * H * 0.04
    gd.ellipse([W * gx - r + ox, H * gy - r + oy, W * gx + r + ox, H * gy + r + oy],
               fill=int(46 + 40 * ctx.kick))
    glow = glow.filter(ImageFilter.GaussianBlur(min(W, H) * 0.18))
    tint = Image.new("RGBA", (W, H), (*hue, 255))
    img = Image.composite(tint, img, glow)
    # dotted grid, drifting, like a canvas
    d = ImageDraw.Draw(img)
    step = int(54 * ctx.u)
    off = int((ctx.t * 12) % step)
    for y in range(-step + off, H, step):
        for x in range(-step + off, W, step):
            d.point((x, y), fill=(52, 52, 60, 255))
    return img


# --------------------------------------------------------------------------
# the karaoke

def _split(ix, n, width):
    """`ix` in n rows, splits chosen so the widest row is as narrow as it can be."""
    if n == 1 or len(ix) < n:
        return [ix]
    best = None
    for k in range(1, len(ix) - n + 2):
        rest = _split(ix[k:], n - 1, width)
        rows = [ix[:k]] + rest
        wmax = max(width(r) for r in rows)
        if best is None or wmax < best[0]:
            best = (wmax, rows)
    return best[1]


# When each line is on screen, and when each word's sweep runs (2026-11-06,
# the user's note: the sweep lagged the voice and a line left before it was
# lit). A word sweeps from its own start to the next word's start, a touch
# ahead of the voice; a line comes in 0.3s early but never before the last
# one is fully sung, and leaves as the next one comes in.
LEAD = 0.08


def _schedule():
    out = []
    for i, ln in enumerate(TIMING):
        appear = ln["s"] - 0.3
        if i:
            appear = max(appear, TIMING[i - 1]["e"] + 0.02)
        ws = ln["words"]
        sweeps = []
        for k, w in enumerate(ws):
            a = w["s"] - LEAD
            nxt = ws[k + 1]["s"] if k + 1 < len(ws) else None
            b = (nxt - LEAD) if nxt is not None and nxt - w["s"] < 0.9 else w["e"] + 0.12 - LEAD
            sweeps.append((a, max(a + 0.06, b)))
        out.append({"ln": ln, "appear": appear, "sweeps": sweeps})
    for i, sch in enumerate(out):
        nxt = out[i + 1]["appear"] if i + 1 < len(out) else 1e9
        sch["leave"] = min(nxt, sch["ln"]["e"] + 0.8)
    return out


SCHEDULE = _schedule()


def karaoke(img: Image.Image, ctx: Ctx, size=None, y=None, upper=False):
    t = ctx.t
    sch = next((x for x in SCHEDULE if x["appear"] <= t < x["leave"]), None)
    if sch is None:
        return
    cur = sch["ln"]
    i_cur = SCHEDULE.index(sch)
    nxt = SCHEDULE[i_cur + 1]["ln"] if i_cur + 1 < len(SCHEDULE) else None
    W = ctx.W
    max_w = (W - 160) if ctx.tall else W * 0.84
    size = size or (88 if ctx.tall else 84)
    y = y or (1250 if ctx.tall else ctx.H * 0.80)
    words = [w["w"].upper() if upper else w["w"] for w in cur["words"]]
    f = font(F_HEAVY, size)
    # wrap into lines that fit
    def width(ix):
        return f.getlength(" ".join(words[j] for j in ix))
    allw = list(range(len(words)))
    rows = None
    for nrows in ((1, 2, 3) if ctx.tall else (1, 2)):
        rows = _split(allw, nrows, width)
        if max(width(r) for r in rows) <= max_w:
            break
    else:
        return karaoke(img, ctx, int(size * 0.9), y, upper)
    lh = size * 1.18
    top = y - lh * (len(rows) - 1) / 2
    life_in = ease((t - sch["appear"]) / 0.15)
    life_out = 1 - ease((t - (sch["leave"] - 0.12)) / 0.12)
    a = max(0.0, min(life_in, life_out))
    if a <= 0:
        return
    lift = (1 - life_in) * 20 * ctx.u - (1 - life_out) * 20 * ctx.u
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    sp = f.getlength(" ")
    shade_top = int(top - lh * 1.1)
    shade = Image.new("L", (1, 256), 0)
    shade.putdata([int(150 * math.sin(math.pi * k / 255) ** 0.8) for k in range(256)])
    sh_h = int(lh * (len(rows) + 2.6))
    img.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (img.width, sh_h), 0)] * 3,
                                             shade.resize((img.width, sh_h)).point(lambda v: int(v * a)))),
                        (0, max(0, shade_top)))
    for r, row in enumerate(rows):
        line = " ".join(words[i] for i in row)
        x = ctx.cx - f.getlength(line) / 2
        yy = top + r * lh + lift
        for i in row:
            w, info = words[i], cur["words"][i]
            wl = f.getlength(w)
            a0, a1 = sch["sweeps"][i]
            prog = clamp((t - a0) / (a1 - a0))
            # the unsung word dimmed, then the sung part swept in. No drop
            # shadow: the user found it muddy (2026-11-06); the band behind
            # the lines carries the contrast.
            d.text((x, yy), w, font=f, fill=(*INK, 110), anchor="lm")
            if prog > 0:
                sweep = Image.new("RGBA", img.size, (0, 0, 0, 0))
                sd = ImageDraw.Draw(sweep)
                active = 0 < prog < 1
                lift_w = -6 * ctx.u * math.sin(prog * math.pi) if active else 0
                sd.text((x, yy + lift_w), w, font=f, fill=(*ACCENT, 255) if active else (*INK, 255),
                        anchor="lm")
                if prog < 1:
                    m = Image.new("L", img.size, 0)
                    ImageDraw.Draw(m).rectangle([0, 0, int(x + wl * prog), img.height], fill=255)
                    sweep.putalpha(Image.composite(sweep.getchannel("A"), m, m))
                layer.alpha_composite(sweep)
            x += wl + sp
    # ad-libs: small stickers once the line is sung
    if cur["adlibs"] and t > cur["e"] - 0.1:
        q = pop((t - (cur["e"] - 0.1)) / 0.3)
        tag = "  ".join(f"({x})" for x in cur["adlibs"])
        fs = font(F_HEAVY, size * 0.55)
        tw = fs.getlength(tag) + 40 * ctx.u
        bx = min(ctx.cx + max_w / 2 - tw, ctx.cx + f.getlength(" ".join(words[i] for i in rows[-1])) / 2 - tw * 0.4)
        by = top + (len(rows) - 1) * lh + lh * 0.72 + lift
        st = Image.new("RGBA", (int(tw), int(size * 0.85)), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        rounded(sd, (0, 0, st.width - 1, st.height - 1), st.height / 2, (*ACCENT, 255))
        sd.text((st.width / 2, st.height / 2), tag, font=fs, fill=(20, 16, 12, 255), anchor="mm")
        paste(layer, st, bx + tw / 2, by, q, -4)
    # the next line, dimmed, so the eye knows what comes
    if nxt and nxt["s"] - cur["e"] < 1.5 and not ctx.tall:
        fn = font(F_HEAVY, size * 0.48)
        nt = nxt["text"].upper() if upper else nxt["text"]
        fn = fit_font(F_HEAVY, nt, max_w, int(size * 0.48))
        d.text((ctx.cx, top + len(rows) * lh + 14 * ctx.u), nt, font=fn,
               fill=(*DIM, int(150 * life_in)), anchor="mt")
    if a < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(layer)


# --------------------------------------------------------------------------
# the parody chat window - generic, our own type, no logo

def chat_window(img, ctx: Ctx, msgs: list[dict], box=None, title="New chat"):
    """msgs: [{who: "you"|"ai"|"banner"|"dots", text, t0, words?: timing words, color?}]"""
    t = ctx.t
    x0, y0, x1, y1 = box or ctx.stage
    d = ImageDraw.Draw(img)
    u = ctx.u
    rounded(d, (x0 + 10 * u, y0 + 14 * u, x1 + 10 * u, y1 + 14 * u), 30 * u, (0, 0, 0, 120))
    rounded(d, (x0, y0, x1, y1), 30 * u, (*PANEL, 255), (*PANEL2, 255), 3 * u)
    # title bar
    for i, c in enumerate(((255, 95, 87), (255, 189, 46), (40, 200, 64))):
        d.ellipse([x0 + (28 + 30 * i) * u, y0 + 26 * u, x0 + (46 + 30 * i) * u, y0 + 44 * u], fill=c)
    text(d, ((x0 + x1) / 2, y0 + 35 * u), title, font(F_BOLD, 26 * u), DIM, "mm")
    d.line([x0, y0 + 70 * u, x1, y0 + 70 * u], fill=(*PANEL2, 255), width=int(2 * u))
    # messages stack from the bottom up
    pad = 30 * u
    inner_w = (x1 - x0) - 2 * pad
    blocks = []
    for m in msgs:
        if t < m["t0"]:
            continue
        blocks.append(m)
    y = y1 - pad
    f = font(F_MED, (42 if ctx.tall else 46) * u)
    for m in reversed(blocks):
        age = t - m["t0"]
        if m["who"] == "banner":
            fb = font(F_BOLD, (36 if ctx.tall else 40) * u)
            h = 96 * u
            q = pop(age / 0.3)
            col = m.get("color", RED)
            bw = min(inner_w, fb.getlength(m["text"]) + 150 * u)
            fb = fit_font(F_BOLD, m["text"], bw - 140 * u, fb.size)
            bx0 = (x0 + x1) / 2 - bw / 2
            ban = Image.new("RGBA", (int(bw), int(h)), (0, 0, 0, 0))
            bd = ImageDraw.Draw(ban)
            rounded(bd, (0, 0, bw - 1, h - 1), 22 * u, (*[int(c * 0.22) for c in col], 255),
                    (*col, 255), 3 * u)
            warn = emoji("⚠️", int(52 * u), age)
            ban.alpha_composite(warn, (int(30 * u), int(h / 2 - warn.height / 2)))
            bd.text((bw / 2 + 30 * u, h / 2), m["text"], font=fb, fill=(*col, 255), anchor="mm")
            paste(img, ban, bx0 + bw / 2, y - h / 2, q)
            y -= h + 24 * u
            continue
        if m["who"] == "dots":
            if m.get("until") and t > m["until"]:
                continue
            bh = 70 * u
            rounded(d, (x0 + pad, y - bh, x0 + pad + 150 * u, y), bh / 2, (*PANEL2, 255))
            for k in range(3):
                ph = (t * 3 - k * 0.25) % 1
                rr = (8 + 5 * math.sin(ph * math.pi)) * u
                cxk = x0 + pad + (45 + 30 * k) * u
                d.ellipse([cxk - rr, y - bh / 2 - rr, cxk + rr, y - bh / 2 + rr], fill=(*DIM, 255))
            y -= bh + 20 * u
            continue
        # the text typed so far: word-timed for the user, streamed for the ai
        if m.get("words"):
            shown = " ".join(w["w"] for w in m["words"] if w["s"] - 0.05 <= t)
            if m.get("adlib") and t > m["words"][-1]["e"]:
                shown += f" ({m['adlib']})"
        else:
            n = int((t - m["t0"]) * m.get("cps", 38))
            shown = m["text"][:n]
        if not shown:
            continue
        maxw = inner_w * 0.80
        lines, cur = [], ""
        for word in shown.split(" "):
            trial = (cur + " " + word).strip()
            if f.getlength(trial) > maxw - 50 * u and cur:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        lines.append(cur)
        lh = f.size * 1.32
        bw = max(f.getlength(ln) for ln in lines) + 56 * u
        bh = lh * len(lines) + 34 * u
        you = m["who"] == "you"
        bx0 = x1 - pad - bw if you else x0 + pad + (64 * u)
        col = (*ACCENT, 255) if you else (*PANEL2, 255)
        ink = (24, 18, 12, 255) if you else (*INK, 255)
        q = ease(age / 0.18)
        rounded(d, (bx0, y - bh, bx0 + bw, y), 26 * u, col)
        for k, ln in enumerate(lines):
            d.text((bx0 + 28 * u, y - bh + 17 * u + k * lh), ln, font=f, fill=ink)
        if not you:
            paste(img, emoji("🤖", int(46 * u), t), x0 + pad + 26 * u, y - 30 * u, q)
            text(d, (bx0, y - bh - 8 * u), m.get("name", "Claude"), font(F_BOLD, 24 * u), DIM, "lb")
            y -= 34 * u
        y -= bh + 22 * u
    return img


# --------------------------------------------------------------------------
# a terminal

def terminal(img, ctx: Ctx, rows: list[tuple], box=None, title="~/startup — zsh"):
    """rows: [(t0, text, color, cps)] typed in order."""
    t = ctx.t
    x0, y0, x1, y1 = box or ctx.stage
    u = ctx.u
    d = ImageDraw.Draw(img)
    rounded(d, (x0 + 10 * u, y0 + 14 * u, x1 + 10 * u, y1 + 14 * u), 22 * u, (0, 0, 0, 120))
    rounded(d, (x0, y0, x1, y1), 22 * u, (10, 10, 12, 255), (*PANEL2, 255), 3 * u)
    for i, c in enumerate(((255, 95, 87), (255, 189, 46), (40, 200, 64))):
        d.ellipse([x0 + (24 + 28 * i) * u, y0 + 22 * u, x0 + (40 + 28 * i) * u, y0 + 38 * u], fill=c)
    text(d, ((x0 + x1) / 2, y0 + 30 * u), title, font(F_MONO, 22 * u), DIM, "mm")
    size = (34 if ctx.tall else 32) * u
    room = (x1 - x0) - 34 * u - 50 * u
    longest = max((r[1] for r in rows), key=len, default="")
    f = fit_font(F_MONO, longest + " ", room, int(size))
    y = y0 + 80 * u
    last = None
    for t0, s, col, cps in rows:
        if t < t0:
            break
        n = len(s) if cps <= 0 else int((t - t0) * cps)
        shown = s[:n]
        d.text((x0 + 34 * u, y), shown, font=f, fill=(*col, 255))
        last = (x0 + 34 * u + f.getlength(shown), y)
        y += f.size * 1.5
    if last and (t * 2) % 1 < 0.5:
        d.rectangle([last[0] + 4 * u, last[1] + 4 * u, last[0] + 22 * u, last[1] + f.size * 1.05],
                    fill=(*INK, 255))


# --------------------------------------------------------------------------
# props

def clock(img, ctx: Ctx, cx, cy, r, hh, mm, face=PANEL, hot=False):
    """Drawn at 3x on its own tile and reduced, so its edges are smooth and
    its 808 swell is sub-pixel. Drawn straight onto the frame, the rim and
    hands were aliased and the swell stepped a whole pixel at a time (the
    user's note, 2026-11-06)."""
    SS = 3
    u = ctx.u * SS
    R = r * SS
    rr = R * (1 + 0.025 * ctx.kick)
    pad = int(R * 0.12 + 12 * u)
    size = int(2 * R + 2 * pad)
    tile = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    c = size / 2
    rim = RED if hot else ACCENT
    d.ellipse([c - rr - 8 * u, c - rr - 8 * u, c + rr + 8 * u, c + rr + 8 * u], fill=(*rim, 255))
    d.ellipse([c - rr, c - rr, c + rr, c + rr], fill=(*face, 255))

    def stroke(a, l0, l1, w, col):
        x0, y0 = c + math.sin(a) * l0, c - math.cos(a) * l0
        x1, y1 = c + math.sin(a) * l1, c - math.cos(a) * l1
        d.line([x0, y0, x1, y1], fill=col, width=int(w))
        for x, y in ((x0, y0), (x1, y1)):           # round caps
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=col)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        stroke(a, rr * (0.80 if k % 3 else 0.72), rr * 0.9, (6 if k % 3 == 0 else 3) * u, (*INK, 255))
    stroke(((hh % 12) + mm / 60) / 12 * 2 * math.pi, 0, rr * 0.5, 14 * u, (*INK, 255))
    stroke((mm / 60) * 2 * math.pi, 0, rr * 0.75, 8 * u, (*rim, 255))
    d.ellipse([c - 12 * u, c - 12 * u, c + 12 * u, c + 12 * u], fill=(*INK, 255))
    small = tile.resize((size // SS, size // SS), Image.LANCZOS)
    img.alpha_composite(small, (int(round(cx - small.width / 2)), int(round(cy - small.height / 2))))


def big_label(img, ctx: Ctx, s, cx, cy, size, color=INK, t0=None, rot=0.0, box=None, ink_on=(20, 16, 12)):
    t = ctx.t
    q = 1.0 if t0 is None else pop((t - t0) / 0.3)
    if t0 is not None and t < t0:
        return
    f = font(F_HEAVY, size)
    w = f.getlength(s)
    pad = size * 0.35
    lab = Image.new("RGBA", (int(w + 2 * pad), int(size * 1.5)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lab)
    if box:
        rounded(d, (0, 0, lab.width - 1, lab.height - 1), size * 0.3, (*box, 255))
        d.text((lab.width / 2, lab.height / 2), s, font=f, fill=(*ink_on, 255), anchor="mm")
    else:
        d.text((lab.width / 2 + 4, lab.height / 2 + 5), s, font=f, fill=(0, 0, 0, 160), anchor="mm")
        d.text((lab.width / 2, lab.height / 2), s, font=f, fill=(*color, 255), anchor="mm")
    paste(img, lab, cx, cy, q, rot)


def bar(img, ctx: Ctx, cx, cy, w, frac, label=True):
    d = ImageDraw.Draw(img)
    u = ctx.u
    h = 70 * u
    rounded(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, (*PANEL2, 255))
    col = GREEN if frac < 0.5 else (ACCENT if frac < 0.9 else RED)
    if frac > 0.01:
        rounded(d, (cx - w / 2 + 8 * u, cy - h / 2 + 8 * u, cx - w / 2 + 8 * u + (w - 16 * u) * frac,
                    cy + h / 2 - 8 * u), (h - 16 * u) / 2, (*col, 255))
    if label:
        text(d, (cx, cy - h / 2 - 50 * u), f"Usage  {int(round(frac * 100))}%", font(F_HEAVY, 54 * u),
             INK if frac < 0.9 else RED, "mm")


def swipe_card(img, ctx: Ctx, cx, cy, t0, t_swipe):
    """A dating card for a horse; it swipes right on the snort."""
    t, u = ctx.t, ctx.u
    w, h = 440 * u, 580 * u
    card = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    rounded(d, (0, 0, w - 1, h - 1), 36 * u, (245, 240, 232, 255))
    rounded(d, (24 * u, 24 * u, w - 24 * u, h * 0.70), 26 * u, (255, 214, 170, 255))
    horse = emoji("🐎", int(260 * u), t - t0)
    card.alpha_composite(horse, (int(w / 2 - horse.width / 2), int(h * 0.36 - horse.height / 2)))
    d.text((36 * u, h * 0.75), "Horse, 7", font=font(F_HEAVY, 46 * u), fill=(30, 26, 22, 255))
    d.text((36 * u, h * 0.86), "2 km away · loves hay", font=font(F_MED, 28 * u), fill=(110, 100, 92, 255))
    q = pop((t - t0) / 0.35)
    k = ease((t - t_swipe) / 0.45) if t > t_swipe else 0
    paste(img, card, cx + k * ctx.W * 0.7, cy - k * 60 * u, q, -k * 22 + math.sin(t * 2) * 2)
    if t > t_swipe:
        big_label(img, ctx, "IT'S A MATCH", cx, cy - 40 * u, int(96 * u), t0=t_swipe + 0.12,
                  box=(255, 77, 140), ink_on=(255, 255, 255), rot=-6)
        emo(img, ctx, "❤️", cx - 230 * u, cy + 150 * u, 170 * u, t_swipe + 0.2, rot=12)
        emo(img, ctx, "🐎", cx + 220 * u, cy + 150 * u, 230 * u, t_swipe + 0.3, rot=-8)


# --------------------------------------------------------------------------
# the `behind` shots

_BEHIND: dict = {}


def behind(ctx: Ctx, key: str, word: str, start: float, hold: float, entry="fly") -> Image.Image:
    from video_automation.longform.beats import BEATS
    k = (key, word, ctx.frame.name, start)
    if k not in _BEHIND:
        _BEHIND[k] = BEATS["behind"](PHOTO[key], word, "", entry, brand=SONG, frame=ctx.frame,
                                     reveals=[0.15], start=0.0, hold=hold)
    return _BEHIND[k].draw(clamp((ctx.t - start) / hold)).convert("RGBA")


# --------------------------------------------------------------------------
# scenes: (start, end, fn). Each draws the picture; the karaoke goes on top.

def L(prefix, n=1):
    return line_at(prefix, n)


def sc_intro(ctx: Ctx, img):
    a, b, c = L("Okay Claude"), L("Fix the bug"), L("And make it pop")
    msgs = [
        {"who": "you", "t0": a["s"] - 0.1, "words": a["words"]},
        {"who": "dots", "t0": a["e"] + 0.3, "until": b["s"] - 0.2},
        {"who": "you", "t0": b["s"] - 0.1, "words": b["words"], "adlib": "yeah"},
        {"who": "you", "t0": c["s"] - 0.1, "words": c["words"], "adlib": "hello?"},
        {"who": "dots", "t0": c["e"] + 0.1},
        {"who": "banner", "t0": 13.35, "text": "Usage limit reached · resets 5:00 PM"},
    ]
    chat_window(img, ctx, msgs, box=_chat_box(ctx))


def _chat_box(ctx):
    if ctx.tall:
        return (60, ctx.frame.safe_top + 40, ctx.W - 60, 1400)
    return (ctx.W * 0.18, 60, ctx.W * 0.82, ctx.H - 60)


def sc_hook(n):
    """A hook: the clock running toward five, an emoji per line."""
    def draw(ctx: Ctx, img):
        t = ctx.t
        x0, y0, x1, y1 = ctx.stage
        cx = ctx.cx if ctx.tall else ctx.W * 0.5
        cy = 640 if ctx.tall else ctx.H * 0.38
        r = 250 * ctx.u
        # the clock: noon at the hook's start, sweeping on toward five
        hook = [ln for ln in TIMING if ln["section"] == "hook"]
        groups = _hook_groups()
        g = groups[n - 1]
        land = L("Five o'clock hit")["s"] if n == 3 else g[-1]["e"]
        p = clamp((t - g[0]["s"]) / (land - g[0]["s"]))
        start_h = {1: 12.0, 2: 14.5, 3: 16.4}[n]
        end_h = {1: 13.6, 2: 16.2, 3: 17.0}[n]
        hours = start_h + (end_h - start_h) * p
        five = n == 3 and p >= 1
        clock(img, ctx, cx, cy, r, int(hours), (hours % 1) * 60, hot=five)
        if five:
            big_label(img, ctx, "5:00 PM", cx, (cy + r + 70 * ctx.u) if ctx.tall else (cy - r - 70 * ctx.u),
                      int(80 * ctx.u), t0=land, box=GREEN)
        side = r * 1.55

        def spot(left: bool, dy: float = 0.0):
            """Beside the clock, clear of its rim, in both formats."""
            if ctx.tall:
                return (cx + (-1 if left else 1) * (r + 150 * ctx.u), cy - r * 0.55 + dy * 0.2)
            return (cx + (-1 if left else 1) * side, cy + dy)
        for ln in g:
            txt = ln["text"].lower()
            s, e = ln["s"], ln["e"] + 0.3
            if not (s - 0.2 <= t <= e + 0.25):
                continue
            if txt.startswith("limit reached"):
                big_label(img, ctx, "LIMIT REACHED", cx, cy + r + 60 * ctx.u,
                          int(64 * ctx.u), t0=s, box=RED, ink_on=(255, 255, 255),
                          rot=-4 if (hook.index(ln) % 2) else 4)
                emo(img, ctx, "⏰" if hook.index(ln) % 2 else "⏳", *spot(True, -r * 0.3),
                    (200 if not ctx.tall else 170) * ctx.u, s, until=e)
            elif "startup" in txt:
                emo(img, ctx, "🚀", *spot(False, -r * 0.4), (230 if not ctx.tall else 170) * ctx.u, s, until=e, rot=-10)
            elif "staring" in txt:
                emo(img, ctx, "👀", *spot(True), (230 if not ctx.tall else 170) * ctx.u, s, until=e)
            elif "paid for the max" in txt:
                emo(img, ctx, "💸", *spot(True, -r * 0.2), (210 if not ctx.tall else 170) * ctx.u, s, until=e)
                emo(img, ctx, "👋", *spot(False, r * 0.1), (210 if not ctx.tall else 170) * ctx.u, s + 1.2, until=e, rot=-8)
            elif "five o'clock" in txt:
                emo(img, ctx, "🎉", *spot(True, -r * 0.4), (230 if not ctx.tall else 170) * ctx.u, s, until=e)
                emo(img, ctx, "🥳", *spot(False), (230 if not ctx.tall else 170) * ctx.u, s + 0.25, until=e)
    return draw


def _hook_groups():
    out, cur = [], []
    for ln in TIMING:
        if ln["section"] == "hook":
            if cur and ln["s"] - cur[-1]["e"] > 3:
                out.append(cur)
                cur = []
            cur.append(ln)
    out.append(cur)
    return out


def sc_grass(word="GRASS"):
    def draw(ctx: Ctx, img):
        ln = L("So I'm touching grass", 1 if ctx.t < 50 else 2)
        img.alpha_composite(behind(ctx, "grass", word, ln["s"] - 0.3, ln["e"] - ln["s"] + 0.9))
        emo(img, ctx, "🌱", ctx.W * (0.22 if not ctx.tall else 0.2), ctx.H * (0.25 if not ctx.tall else 0.62),
            170 * ctx.u, ln["s"] + 0.3)
        emo(img, ctx, "🤖", ctx.W * (0.80 if not ctx.tall else 0.62), ctx.H * (0.25 if not ctx.tall else 0.62),
            170 * ctx.u, ln["s"] + 1.4)
    return draw


def sc_woke(ctx, img):
    ln = L("Woke up")
    x0, y0, x1, y1 = ctx.stage
    box = (x0, y0, x1 - ctx.W * 0.18, y1) if not ctx.tall else (x0, y0 + 230 * ctx.u, x1, y1)
    terminal(img, ctx, [(ln["s"], "$ ai --agents 10 --goal startup", INK, 40),
                        (ln["s"] + 1.0, "> 10 agents online", GREEN, 0)], box=box)
    emo(img, ctx, "☕", (x1 - 90 * ctx.u) if not ctx.tall else ctx.cx,
        (y1 - 120 * ctx.u) if not ctx.tall else (y0 + 110 * ctx.u), (220 if not ctx.tall else 180) * ctx.u,
        ln["s"] + 0.2)


def sc_agents(ctx, img):
    ln = L("Ten agents")
    x0, y0, x1, y1 = ctx.stage
    cols = 5
    cw = (x1 - x0) / cols
    ch = (y1 - y0) * (0.62 if not ctx.tall else 0.36)
    for k in range(10):
        cxk = x0 + cw * (k % cols + 0.5)
        cyk = y0 + (y1 - y0) * (0.55 if not ctx.tall else 0.62) + ch * (k // cols - 0.5) * 0.9
        emo(ctx=ctx, base=img, ch="🤖", cx=cxk, cy=cyk, h=min(cw, ch) * 0.75, t0=ln["s"] + k * 0.09)
    emo(img, ctx, "😎", ctx.cx, y0 + (y1 - y0) * (0.13 if not ctx.tall else 0.2), 200 * ctx.u, ln["s"] + 0.9)


def sc_horse(ctx, img):
    ln = L("Told it build me Tinder")
    x0, y0, x1, y1 = ctx.stage
    swipe_card(img, ctx, ctx.cx, (y0 + y1) / 2 + 20 * ctx.u, ln["s"], 36.85)


def sc_laptop(ctx, img):
    ln = L("Laptop on my lap")
    x0, y0, x1, y1 = ctx.stage
    u = ctx.u
    cy = (y0 + y1) / 2 + 30 * u
    emo(img, ctx, "💻", ctx.cx, cy, 330 * u, ln["s"])
    side = 290 * u
    for k, sgn in enumerate((-1, 1)):
        ph = (ctx.t * 1.4 + k * 0.5) % 1
        emo(img, ctx, "🔥", ctx.cx + sgn * side, cy + 40 * u - ph * 50 * u, (170 + 30 * math.sin(ph * math.pi)) * u,
            ln["s"] + 0.5 + k * 0.1, bounce=False)
    words = {w["w"].lower(): w["s"] for w in ln["words"]}
    emo(img, ctx, "🥵", ctx.cx, cy - 290 * u, 180 * u, words.get("thighs", ln["s"] + 1.6))


def sc_fan(ctx, img):
    ln = L("Fan screaming")
    x0, y0, x1, y1 = ctx.stage
    cy = (y0 + y1) / 2
    shake = 10 * ctx.u * math.sin(ctx.t * 70)
    emo(img, ctx, "🌀", ctx.cx - 220 * ctx.u + shake, cy + (60 if not ctx.tall else 160) * ctx.u,
        260 * ctx.u, ln["s"], rot=-ctx.t * 720)
    emo(img, ctx, "😵", ctx.cx + 220 * ctx.u, cy + (60 if not ctx.tall else 160) * ctx.u, 200 * ctx.u, ln["s"] + 1.1)
    p = clamp((ctx.t - (ln["s"] + 0.5)) / 1.8)
    if 0 < p < 1:
        x = x0 - 200 * ctx.u + (x1 - x0 + 400 * ctx.u) * p
        paste(img, emoji("✈️", int(170 * ctx.u), ctx.t), x,
              cy - (170 if not ctx.tall else 180) * ctx.u + 40 * ctx.u * (1 - p), 1, 0)


def sc_snack(ctx, img):
    ln = L("Went to grab a snack")
    x0, y0, x1, y1 = ctx.stage
    cy = (y0 + y1) / 2
    gap = (330 if not ctx.tall else 300) * ctx.u
    emo(img, ctx, "🍿", ctx.cx - gap, cy, 210 * ctx.u, ln["s"])
    emo(img, ctx, "💻", ctx.cx, cy, 240 * ctx.u, ln["s"] + 0.6)
    emo(img, ctx, "😴", ctx.cx + gap, cy, 190 * ctx.u, ln["s"] + 1.0)


def sc_interrupted(ctx, img):
    ln = L("Came back, task interrupted")
    x0, y0, x1, y1 = ctx.stage
    terminal(img, ctx, [(ln["s"] - 1.9, "$ ai build --everything", INK, 0),
                        (ln["s"] - 1.9, "  * building...  [##########---] 83%", DIM, 0),
                        (ln["s"] + 0.2, "x Task interrupted.", RED, 0),
                        (ln["s"] + 0.9, "$ ai build --everything   # again", INK, 30)],
             box=(x0, y0, x1 - 230 * ctx.u, y1) if not ctx.tall else (x0, y0 + 200 * ctx.u, x1, y1))
    emo(img, ctx, "❌", (x1 - 100 * ctx.u) if not ctx.tall else ctx.cx,
        (y0 + 150 * ctx.u) if not ctx.tall else (y0 + 90 * ctx.u), 160 * ctx.u, ln["s"] + 0.2)


def sc_shipped(ctx, img):
    ln = L("Shipped three features")
    x0, y0, x1, y1 = ctx.stage
    cy = (y0 + y1) / 2
    clock(img, ctx, ctx.cx - (330 if not ctx.tall else 0) * ctx.u,
          cy - (0 if not ctx.tall else 230) * ctx.u, 180 * ctx.u, 8, 59)
    for k in range(3):
        emo(img, ctx, "✅", ctx.cx + ((150 + k * 180) if not ctx.tall else (-200 + k * 200)) * ctx.u,
            cy + (0 if not ctx.tall else 190) * ctx.u, 150 * ctx.u, ln["s"] + 0.25 + k * 0.3)
    big_label(img, ctx, "8:59 AM", ctx.cx - (330 if not ctx.tall else 0) * ctx.u,
              cy + (240 if not ctx.tall else -470) * ctx.u, int(60 * ctx.u), t0=ln["s"], box=PANEL2,
              ink_on=INK)


def sc_usage(ctx, img):
    """The bar climbs to 21%, jumps to 100% - and, because the take sings
    that line twice, drops back and does it again."""
    a = L("Then I watched")
    runs = [L("Twenty one percent", 1), L("Twenty one percent", 2)]
    x0, y0, x1, y1 = ctx.stage
    t = ctx.t
    w = (x1 - x0) * 0.85
    run = runs[1] if t >= runs[1]["s"] - 0.1 else runs[0]
    words = {w_["w"].lower().strip(","): w_["s"] for w_ in run["words"]}
    t21, t100 = words.get("percent", run["s"] + 0.6), words.get("hundred", run["s"] + 1.4)
    start = a["s"] if run is runs[0] else run["s"] - 0.1
    if t < t21:
        frac = 0.21 * ease((t - start) / max(0.3, t21 - start))
    elif t < t100:
        frac = 0.21
    else:
        frac = 0.21 + 0.79 * ease((t - t100) / 0.25)
    shake = (8 * ctx.u * math.sin(t * 90)) if frac > 0.99 and t < t100 + 0.8 else 0
    cy = (y0 + y1) / 2 + 40 * ctx.u
    bar(img, ctx, ctx.cx + shake, cy, w, frac)
    if t > t100:
        emo(img, ctx, "🤯", ctx.cx, cy - 250 * ctx.u, 180 * ctx.u, t100 + 0.1, until=run["e"] + 0.15)
        if run is runs[1]:
            big_label(img, ctx, "1 prompt", ctx.cx, cy + 130 * ctx.u, int(46 * ctx.u),
                      t0=words.get("prompt", t100 + 0.4), box=PANEL2, ink_on=INK, rot=-4)


def sc_compact(ctx, img):
    ln = L("Compacting conversation")
    t = ctx.t
    x0, y0, x1, y1 = ctx.stage
    u = ctx.u
    p = ease((t - (ln["s"] + 0.2)) / 1.0)
    d = ImageDraw.Draw(img)
    cy = (y0 + y1) / 2 + 30 * u
    n = 6
    for k in range(n):              # the conversation, collapsing into its middle
        w = (x1 - x0) * (0.42 + 0.25 * ((k * 37) % 5) / 5)
        h = 64 * u
        yk = cy + (k - (n - 1) / 2) * 84 * u * (1 - p)
        right = k % 2 == 0
        xs = (x1 - 40 * u - w) if right else (x0 + 40 * u)
        xs = xs + ((ctx.cx - w / 2) - xs) * p
        a = int(255 * (1 - p))
        if a < 8:
            continue
        rounded(d, (xs, yk - h / 2, xs + w, yk + h / 2), h / 2, (*(ACCENT if right else PANEL2), a))
        for r in range(2):
            d.rounded_rectangle([xs + 30 * u, yk - 14 * u + r * 18 * u, xs + w * (0.75 - 0.2 * r), yk - 6 * u + r * 18 * u],
                                radius=int(4 * u), fill=(0, 0, 0, int(a * 0.35)))
    if p > 0.6:
        big_label(img, ctx, "Summary: you were building… something?", ctx.cx, cy, int(40 * u),
                  t0=ln["s"] + 0.9, box=PANEL2, ink_on=INK)
    big_label(img, ctx, "Compacting conversation…", ctx.cx, y0 + 40 * u, int(44 * u),
              t0=ln["s"], box=ACCENT)
    words = {w["w"].lower(): w["s"] for w in ln["words"]}
    tg = words.get("genius", ln["s"] + 1.2)
    if t > tg - 0.3:
        k = ease((t - tg) / 0.9)
        paste(img, emoji("🧠", int(170 * u), t), ctx.cx + k * (x1 - ctx.cx - 60 * u),
              cy + 150 * u - k * 260 * u, 1 - 0.6 * k, k * 120, 1 - k * 0.85)


def sc_max(ctx, img):
    ln = L("Max plan flexing")
    x0, y0, x1, y1 = ctx.stage
    cy = (y0 + y1) / 2
    big_label(img, ctx, "MAX", ctx.cx, cy - 40 * ctx.u, int(170 * ctx.u), t0=ln["s"], box=ACCENT)
    emo(img, ctx, "💪", ctx.cx - (380 if not ctx.tall else 250) * ctx.u, cy - 40 * ctx.u, 200 * ctx.u, ln["s"] + 0.2)
    for k in range(3):
        emo(img, ctx, "👏", ctx.cx + (380 if not ctx.tall else 250) * ctx.u,
            cy - 170 * ctx.u + k * 140 * ctx.u, 130 * ctx.u, ln["s"] + 0.7 + k * 0.15)


def sc_loggedout(ctx, img):
    ln = L("Five minutes later")
    x0, y0, x1, y1 = ctx.stage
    cy = (y0 + y1) / 2
    emo(img, ctx, "🔒", ctx.cx, cy - 60 * ctx.u, 280 * ctx.u, ln["s"] + 0.6)
    big_label(img, ctx, "Session limit reached", ctx.cx, cy + 160 * ctx.u, int(50 * ctx.u),
              t0=ln["s"] + 0.9, box=RED, ink_on=(255, 255, 255))


@lru_cache(maxsize=4)
def _photo(key: str, w: int, h: int) -> Image.Image:
    im = Image.open(PHOTO[key]).convert("RGB")
    sc = max(w / im.width, h / im.height) * 1.12
    return im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)


def sc_manager(ctx, img):
    """The manager: the photo pushing in, and the question stamped over it.

    It was a `behind` shot first ("FIX?", then "THE FIX"); his head and
    shoulders cover the top third of the frame, so the word was never read.
    """
    ln = L("Manager pulled up")
    big = _photo("manager", ctx.W, ctx.H)
    p = ease((ctx.t - ln["s"]) / (ln["e"] - ln["s"] + 1.5))
    z = 1 + 0.06 * p
    im = big.resize((int(big.width * z), int(big.height * z)), Image.BICUBIC)
    ox = (im.width - ctx.W) / 2
    oy = (im.height - ctx.H) * (0.35 if not ctx.tall else 0.15)
    img.paste(im.crop((int(ox), int(oy), int(ox) + ctx.W, int(oy) + ctx.H)).convert("RGBA"), (0, 0))
    words = {w["w"].lower().strip("'s"): w["s"] for w in ln["words"]}
    tw = words.get("where", ln["s"] + 1.2)
    big_label(img, ctx, "WHERE'S THE FIX?", ctx.cx, (ctx.H * 0.18) if not ctx.tall else 520,
              int(80 * ctx.u), t0=tw, box=RED, ink_on=(255, 255, 255), rot=-5)
    emo(img, ctx, "😤", ctx.W * 0.82 if not ctx.tall else ctx.cx + 250 * ctx.u,
        ctx.H * 0.40 if not ctx.tall else 760, 200 * ctx.u, tw + 0.3)


def sc_byhand(ctx, img):
    ln = L("I wrote one line")
    x0, y0, x1, y1 = ctx.stage
    terminal(img, ctx, [(ln["s"], "1  const fix = ", INK, 6)], box=(x0, y0, x1, y1),
             title="fix.ts — written by hand")
    emo(img, ctx, "✍️", x1 - 380 * ctx.u, y1 - 140 * ctx.u, 170 * ctx.u, ln["s"])
    emo(img, ctx, "🤢", x1 - 130 * ctx.u, y1 - 140 * ctx.u, 170 * ctx.u, ln["s"] + 1.0)


def sc_refresh(ctx, img):
    a, b = L("Four fifty eight"), L("Four fifty nine")
    x0, y0, x1, y1 = ctx.stage
    cy = (y0 + y1) / 2
    t = ctx.t
    s = "4:59 PM" if t >= b["s"] else "4:58 PM"
    big_label(img, ctx, s, ctx.cx, cy - 40 * ctx.u, int(200 * ctx.u), color=INK)
    for t0 in (a["e"] + 0.05, b["e"] + 0.05):
        if t0 <= t <= t0 + 0.6:
            big_label(img, ctx, "refresh", ctx.cx + 40 * ctx.u, cy + 170 * ctx.u, int(60 * ctx.u), t0=t0,
                      box=ACCENT)
            emo(img, ctx, "🔄", ctx.cx - 170 * ctx.u, cy + 170 * ctx.u, 90 * ctx.u, t0, bounce=False)
    emo(img, ctx, "⏳", ctx.cx + (600 if not ctx.tall else 0) * ctx.u,
        cy + (-40 if not ctx.tall else -330) * ctx.u, 170 * ctx.u, a["s"])


def sc_docs(ctx, img):
    ln = L("The docs don't say")
    x0, y0, x1, y1 = ctx.stage
    d = ImageDraw.Draw(img)
    u = ctx.u
    px0, px1 = x0 + 30 * u, x1 - 30 * u
    rounded(d, (px0, y0, px1, y1), 22 * u, (238, 236, 232, 255))
    d.text((px0 + 50 * u, y0 + 50 * u), "Docs", font=font(F_HEAVY, 54 * u), fill=(30, 30, 34, 255))
    for k in range(7):
        yy = y0 + (150 + k * 52) * u
        if yy > y1 - 40 * u:
            break
        d.rounded_rectangle([px0 + 50 * u, yy, px0 + 50 * u + (px1 - px0 - 100 * u) * (0.6 + 0.35 * ((k * 53) % 7) / 7),
                             yy + 18 * u], radius=int(9 * u), fill=(200, 198, 194, 255))
    words = {w["w"].lower().strip("'"): w["s"] for w in ln["words"]}
    ta = words.get("absolutely", ln["s"] + 1.2)
    if ctx.t > ta - 0.2:
        cy = (y0 + y1) / 2 + 40 * u
        big_label(img, ctx, "You're absolutely right!", ctx.cx, cy, int(58 * u), t0=ta - 0.2,
                  box=PANEL2, ink_on=INK, rot=-3)
        if ctx.t > ln["e"] - 0.2:
            k = ease((ctx.t - (ln["e"] - 0.2)) / 0.25)
            f = font(F_HEAVY, 58 * u)
            w = f.getlength("You're absolutely right!") * 1.05
            d.line([ctx.cx - w / 2, cy + 20 * u, ctx.cx - w / 2 + w * k, cy - 20 * u], fill=(*RED, 255),
                   width=int(12 * u))


def sc_outside(ctx, img):
    ln = L("I went outside")
    start = ln["s"] - 0.3
    pic = behind(ctx, "outside", "OUTSIDE", start, 88.0 - start)
    # "the graphics are insane": the real world, in bloom
    q = clamp((ctx.t - (ln["e"] - 0.1)) / 0.6)
    if q > 0:
        try:
            pic = shaderfx.apply(pic.convert("RGB"), f"bloom:{0.6 * q:.2f},leak:{0.7 * q:.2f}",
                                 ctx.t, SONG).convert("RGBA")
        except Exception:
            pass
    img.alpha_composite(pic)
    emo(img, ctx, "🤩", ctx.W * (0.86 if not ctx.tall else 0.80), ctx.H * (0.56 if not ctx.tall else 0.50),
        200 * ctx.u, ln["e"] + 0.1)


def sc_weekly(ctx, img):
    ln = L("Weekly limit")
    msgs = [
        {"who": "you", "t0": 100.3, "text": "one line", "cps": 30},
        {"who": "banner", "t0": ln["s"] + 0.1, "text": "Weekly limit reached · resets Thursday"},
    ]
    chat_window(img, ctx, msgs, box=(ctx.W * 0.2, 50, ctx.W * 0.8, ctx.H * 0.66) if not ctx.tall else
                (60, ctx.frame.safe_top + 40, ctx.W - 60, 1080))
    emo(img, ctx, "😱", ctx.W * 0.88 if not ctx.tall else ctx.cx, (ctx.H * 0.36) if not ctx.tall else 560,
        260 * ctx.u, ln["s"] + 1.4)


def sc_thursday(ctx, img):
    ln = L("It's Thursday")
    x0, y0, x1, y1 = ctx.stage
    cy = (y0 + y1) / 2
    u = ctx.u
    w, h = 420 * u, 440 * u
    cal = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(cal)
    rounded(d, (0, 0, w - 1, h - 1), 36 * u, (245, 242, 236, 255))
    rounded(d, (0, 0, w - 1, 120 * u), 36 * u, (*RED, 255))
    d.rectangle([0, 80 * u, w, 120 * u], fill=(*RED, 255))
    d.text((w / 2, 62 * u), "THURSDAY", font=font(F_HEAVY, 56 * u), fill=(255, 255, 255, 255), anchor="mm")
    d.text((w / 2, 280 * u), "∞", font=font(F_HEAVY, 230 * u), fill=(30, 30, 34, 255), anchor="mm")
    paste(img, cal, ctx.cx, cy, pop((ctx.t - (ln["s"] - 0.3)) / 0.4), math.sin(ctx.t * 3) * 3)


def sc_again(ctx, img):
    ln = L("Okay Claude", 2)
    msgs = [{"who": "you", "t0": ln["s"] - 0.1, "words": ln["words"], "adlib": "here we go again"},
            {"who": "dots", "t0": ln["e"] + 0.3}]
    chat_window(img, ctx, msgs, box=_chat_box(ctx))


def sc_end(ctx, img):
    """The title and a clock at five, centred as one block, nothing else."""
    t0 = 114.0
    q = ease((ctx.t - t0) / 0.6)
    d = ImageDraw.Draw(img)
    u = ctx.u
    r = 120 * u
    if ctx.tall:
        f2 = fit_font(F_COND, "COME BACK", ctx.W - 160, int(200 * u))
        lh = f2.size * 1.02
        block = 2 * lh + 70 * u + 2 * r
        top = ctx.H * 0.45 - block / 2
        for k, s_ in enumerate(("COME BACK", "AT FIVE")):
            d.text((ctx.cx, top + lh * (k + 0.5)), s_, font=f2,
                   fill=(*(ACCENT if k else INK), int(255 * q)), anchor="mm")
        ccy = top + 2 * lh + 70 * u + r
    else:
        f = fit_font(F_COND, "COME BACK AT FIVE", ctx.W * 0.8, int(170 * u))
        block = f.size + 70 * u + 2 * r
        top = ctx.H / 2 - block / 2
        d.text((ctx.cx, top + f.size / 2), "COME BACK AT FIVE", font=f, fill=(*INK, int(255 * q)), anchor="mm")
        ccy = top + f.size + 70 * u + r
    if q > 0.3:
        clock(img, ctx, ctx.cx, ccy, r, 5, 0)


def scenes() -> list[tuple[float, float, object, dict]]:
    """(start, end, draw, opts). opts: karaoke=False hides the lyric layer."""
    g = _hook_groups()
    grass1, grass2 = L("So I'm touching grass", 1), L("So I'm touching grass", 2)
    v = [L(p) for p in ("Woke up", "Ten agents", "Told it build me Tinder", "Laptop on my lap",
                        "Fan screaming", "Went to grab a snack", "Came back, task interrupted",
                        "Shipped three features", "Then I watched", "Compacting conversation",
                        "Max plan flexing", "Five minutes later", "Manager pulled up",
                        "I wrote one line")]
    S = [
        (0.0, 14.45, sc_intro, {"karaoke": False}),
        (14.45, grass1["s"] - 0.3, sc_hook(1), {}),
        (grass1["s"] - 0.3, v[0]["s"] - 0.15, sc_grass("GRASS"), {}),
        (v[0]["s"] - 0.15, v[1]["s"], sc_woke, {}),
        (v[1]["s"], v[2]["s"], sc_agents, {}),
        (v[2]["s"], v[3]["s"] - 0.1, sc_horse, {}),
        (v[3]["s"] - 0.1, v[4]["s"], sc_laptop, {}),
        (v[4]["s"], v[5]["s"], sc_fan, {}),
        (v[5]["s"], v[6]["s"], sc_snack, {}),
        (v[6]["s"], v[7]["s"], sc_interrupted, {}),
        (v[7]["s"], v[8]["s"], sc_shipped, {}),
        (v[8]["s"], v[9]["s"], sc_usage, {}),
        (v[9]["s"], v[10]["s"], sc_compact, {}),
        (v[10]["s"], v[11]["s"], sc_max, {}),
        (v[11]["s"], v[12]["s"] - 0.2, sc_loggedout, {}),
        (v[12]["s"] - 0.2, v[13]["s"], sc_manager, {}),
        (v[13]["s"], g[1][0]["s"] - 0.2, sc_byhand, {}),
        (g[1][0]["s"] - 0.2, grass2["s"] - 0.3, sc_hook(2), {}),
        (grass2["s"] - 0.3, L("Four fifty eight")["s"] - 0.2, sc_grass("AI'S ALIVE"), {}),
        (L("Four fifty eight")["s"] - 0.2, L("The docs")["s"] - 0.2, sc_refresh, {}),
        (L("The docs")["s"] - 0.2, L("I went outside")["s"] - 0.3, sc_docs, {}),
        (L("I went outside")["s"] - 0.3, g[2][0]["s"] - 0.2, sc_outside, {}),
        (g[2][0]["s"] - 0.2, L("Weekly limit")["s"] - 0.1, sc_hook(3), {}),
        (L("Weekly limit")["s"] - 0.1, L("It's Thursday")["s"] - 0.3, sc_weekly, {}),
        (L("It's Thursday")["s"] - 0.3, L("Okay Claude", 2)["s"] - 0.2, sc_thursday, {}),
        (L("Okay Claude", 2)["s"] - 0.2, 114.0, sc_again, {"karaoke": False}),
        (114.0, 999, sc_end, {"karaoke": False}),
    ]
    return S


# A few hits get a camera punch and colour split: the drop and the limits.
HITS = [13.35, 0.0]


TV_OFF = {f.name: TvOff(END, f) for f in (LANDSCAPE, VERTICAL)}


def soundtrack() -> Path:
    """The final mix with the TV-off zap laid in under the switch-off."""
    import soundfile as sf
    from video_automation.core import sfx
    x, sr = sf.read(AUDIO, dtype="float32")
    zap = sfx.tv_off(sr) * sfx.LEVELS["tv_off"]
    at = int(TV_OFF["landscape"].start * sr)
    end = min(len(x), at + len(zap))
    x[at:end] += zap[:end - at, None]
    out = MIX.parent / "soundtrack.wav"
    sf.write(out, np.clip(x, -1, 1), sr, subtype="PCM_24")
    return out


def render_frame(frame: Frame, t: float, kick: float, S) -> Image.Image:
    ctx = Ctx(frame, t, kick)
    sc = next(s for s in S if s[0] <= t < s[1])
    hue = RED if sc[2] in (sc_loggedout, sc_weekly) else ACCENT
    img = background(ctx, hue)
    sc[2](ctx, img)
    if sc[3].get("karaoke", True):
        karaoke(img, ctx)
    # a cut flash in the first frames of a scene
    age = t - sc[0]
    if 0 <= age < 0.12 and sc[0] > 0.5:
        img = Image.blend(img, Image.new("RGBA", img.size, (255, 255, 255, 255)), 0.12 * (1 - age / 0.12))
    out = img.convert("RGB")
    # the drop and the two limit banners shake and split colour
    for h, dur in ((13.35, 0.9), (L("Weekly limit")["s"] + 0.1, 0.9)):
        if h <= t < h + dur:
            k = 1 - (t - h) / dur
            dx = int(math.sin(t * 95) * 18 * k * ctx.u)
            dy = int(math.cos(t * 77) * 12 * k * ctx.u)
            out = Image.fromarray(np.roll(np.asarray(out), (dy, dx), (0, 1)))
            try:
                out = shaderfx.apply(out, f"aberration:{1.2 * k:.2f}", t, SONG).convert("RGB")
            except Exception:
                pass
    # fade in from black, out to black
    if t < 0.4:
        out = Image.blend(Image.new("RGB", out.size), out, t / 0.4)
    # the end: the picture switches off like a CRT, as on the channels' Shorts
    return TV_OFF[frame.name].draw(out, t)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fmt", choices=("long", "short"))
    ap.add_argument("--from", dest="t0", type=float, default=0.0)
    ap.add_argument("--to", dest="t1", type=float, default=None)
    ap.add_argument("--still", type=float, action="append", help="write a JPG at this time")
    ap.add_argument("--static-emoji", action="store_true")
    a = ap.parse_args()
    frame = LANDSCAPE if a.fmt == "long" else VERTICAL
    import soundfile as sf
    dur = sf.info(str(AUDIO)).duration
    n = int(dur * FPS)
    kick = kick_envelope(n)
    S = scenes()
    OUT.mkdir(parents=True, exist_ok=True)
    with emoji_anim.enabled(not a.static_emoji):
        if a.still:
            for s in a.still:
                p = OUT / f"still-{a.fmt}-{s:06.2f}.jpg"
                render_frame(frame, s, float(kick[min(n - 1, int(s * FPS))]), S).save(p, quality=90)
                print(p)
            return 0
        i0, i1 = int(a.t0 * FPS), int((a.t1 or dur) * FPS)
        i1 = min(i1, n)
        suffix = "" if (a.t0 == 0 and a.t1 is None) else f"-{a.t0:.0f}-{(a.t1 or dur):.0f}"
        out = OUT / f"come-back-at-five-{a.fmt}{suffix}.mp4"
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
               "-s", f"{frame.w}x{frame.h}", "-r", str(FPS), "-i", "-",
               "-ss", f"{i0 / FPS:.4f}", "-t", f"{(i1 - i0) / FPS:.4f}", "-i", str(soundtrack()),
               "-map", "0:v", "-map", "1:a",
               "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", str(out)]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        import time
        t_start = time.time()
        for i in range(i0, i1):
            im = render_frame(frame, i / FPS, float(kick[i]), S)
            p.stdin.write(im.tobytes())
            if (i - i0) % 300 == 0:
                el = time.time() - t_start
                print(f"  {i / FPS:6.1f}s  ({el:.0f}s elapsed)", flush=True)
        p.stdin.close()
        p.wait()
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
