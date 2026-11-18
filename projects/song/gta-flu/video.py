"""The music video for "GTA Flu": 16:9 for YouTube, 9:16 for Shorts.

    .venv/bin/python projects/song/gta-flu/video.py long|short [--from S --to S] [--still S]

Karaoke lyrics over one drawn scene per line: a phone call to the boss, a
fever thermometer through every hook, and a prop per verse line (the "before
GTA 6" list, three delayed dates, the console at the barber's, a pre-load that
flatlines, a doctor's note signed by Florida Man, drizzle against a neon sunset).
The long one is the master; the Short is the cut without hook 2 (the user's
call, 2026-11-17), whole, at 9:16.

Look: the first song's layout (neutral, no watermark), recoloured to 80s Miami
dusk. Round 2 (the user, 2026-11-18): plain SF Pro karaoke with whole-word
highlights, "ME -> BOSS" tags on the call lines, and official GTA VI
screenshots in a few places - Lucia cut out on her card, the real Vice City
skyline, the night skyline behind the hooks and countdown, Jason and Lucia
cut out on the end card. No logo. See ROCKSTAR below for the policy note.

Timing comes from `timing.py` (`timing.json`), every word's start and end in
the master; the Short maps it across the cut (`T()`).
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
FMT = "short" if sys.argv[1:2] == ["short"] else "long"
AUDIO = Path.home() / ("Desktop/songs/gta-flu-short.flac" if FMT == "short" else
                       "Desktop/songs/gta-flu-take4-sfx.flac")
MIX = Path.home() / f".cache/video-automation/song/gta-flu/mix-{FMT}.wav"
OUT = Path.home() / "Desktop/songs/video"

# The Short's audio is the master with hook 2 cut out: 82.78s joined to
# 103.35s (`~/.local/share/song-automation/gta_flu_short.py`).
CUT_A, CUT_LEN = 82.78, 20.5725
CUT_SUNG = 82.13     # hook 2's first words are muted from here (they start before the join)


def T(t: float) -> float:
    """A time on the master, on this format's audio."""
    return t - CUT_LEN if FMT == "short" and t >= CUT_A + CUT_LEN else t


# Palette: Vice City at dusk - deep violet, hot pink, a cyan sea. Generic 80s
# Miami, nothing taken from the game's own art (the song repo's originality rule).
BG = (18, 10, 28)
PANEL = (36, 24, 52)
PANEL2 = (58, 40, 80)
INK = (250, 240, 246)
DIM = (150, 128, 160)
ACCENT = (255, 64, 160)
CYAN = (50, 224, 224)
RED = (255, 72, 84)
GREEN = (70, 226, 140)
BLUE = (90, 160, 255)
YELLOW = (255, 204, 70)

SONG = Brand(name="song", site="", primary=ACCENT, ink=INK, bg=BG, panel=PANEL,
             negative=RED, strike=RED, grid=PANEL2)
BRANDS[SONG.name] = SONG       # beats look a brand up by name; no logo, no watermark

F_HEAVY = ("/System/Library/Fonts/Avenir Next.ttc", 8)
F_BOLD = ("/System/Library/Fonts/Avenir Next.ttc", 0)
F_MED = ("/System/Library/Fonts/Avenir Next.ttc", 5)
F_COND = ("/System/Library/Fonts/Avenir Next Condensed.ttc", 8)
F_MONO = ("/System/Library/Fonts/Menlo.ttc", 0)
F_MONOB = ("/System/Library/Fonts/Menlo.ttc", 1)
# The lyrics: SF Pro Bold, plain. Avenir Next Heavy with a per-letter sweep read
# as low quality (the user, 2026-11-18); SF Pro won a side-by-side.
F_LYRIC = ("/System/Library/Fonts/SFNS.ttf", b"Bold")
F_LYRIC_HEAVY = ("/System/Library/Fonts/SFNS.ttf", b"Heavy")


@lru_cache(maxsize=256)
def font(spec, size: int) -> ImageFont.FreeTypeFont:
    if isinstance(spec[1], bytes):          # a variable font and its named weight
        f = ImageFont.truetype(spec[0], max(8, int(size)))
        f.set_variation_by_name(spec[1])
        return f
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

def _timing():
    lines = json.loads((HERE / "timing.json").read_text())["lines"]
    if FMT == "long":
        return lines
    out = []
    for ln in lines:
        if CUT_SUNG <= ln["s"] < CUT_A + CUT_LEN:
            continue            # hook 2, cut from the Short
        if ln["s"] >= CUT_A + CUT_LEN:
            ln = {**ln, "s": T(ln["s"]), "e": T(ln["e"]),
                  "words": [{**w, "s": T(w["s"]), "e": T(w["e"])} for w in ln["words"]]}
        out.append(ln)
    return out


TIMING = _timing()


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


# --------------------------------------------------------------------------
# Nothing pops in unless it can stay up long enough to be read (the user's
# note, 2026-11-18: stickers and emoji kept appearing half a second before
# the next line or scene replaced them). render_frame sets the scene's end;
# every timed pop checks it. `video.py <fmt> --audit` lists what the rule hid.
MIN_HOLD = 1.0
SCENE = {"start": 0.0, "end": 1e9, "name": ""}
AUDIT: dict = {}


def at(t0):
    """A pop's start, pulled early enough to hold MIN_HOLD before its scene ends.

    A punchline prop timed to a line's last word ("FRESH FADE", "ALL DAY")
    would otherwise flash for 0.2s before the next line's scene: it comes in
    up to a second early instead (never before its scene starts).
    """
    if t0 is None:
        return None
    return max(min(t0, SCENE["end"] - MIN_HOLD), SCENE["start"] + 0.1)


def shows(t0, what="", until=None) -> bool:
    """True if something appearing at t0 stays on screen MIN_HOLD seconds."""
    if t0 is None:
        return True
    end = SCENE["end"] if until is None else min(SCENE["end"], until)
    if end - t0 >= MIN_HOLD - 1e-6:      # at() lands exactly on the limit
        return True
    AUDIT.setdefault((SCENE["name"], str(what), round(t0, 2)), round(end - t0, 2))
    return False


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
    t0 = at(t0) if until is None else t0
    if t < t0 or (until is not None and t > until + 0.2):
        return
    if not shows(t0, ch, None if until is None else until + 0.2):
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
            d.point((x, y), fill=(60, 44, 78, 255))
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


# Lines a character says to someone, so the viewer knows who is talking (the
# user's note, 2026-11-18: the boss calls were confusing). Matched by prefix.
SPEAKER = {
    "Hey boss": "ME  →  BOSS", "I don't think": "ME  →  BOSS", "Or Friday": "ME  →  BOSS",
    "Or this year": "ME  →  BOSS", "Boss? Here": "ME  →  BOSS",
}


def speaker_of(text):
    return next((v for k, v in SPEAKER.items() if text.startswith(k)), None)


def karaoke(img: Image.Image, ctx: Ctx, size=None, y=None):
    """Plain karaoke: sung words white, the word being sung pink, the rest grey.

    Whole words change colour - no sweep through a letter, no bounce, no
    next-line preview. A thin dark outline keeps it legible over photos.
    """
    t = ctx.t
    sch = next((x for x in SCHEDULE if x["appear"] <= t < x["leave"]), None)
    if sch is None:
        return
    cur = sch["ln"]
    W = ctx.W
    max_w = (W - 140) if ctx.tall else W * 0.84
    size = size or (84 if ctx.tall else 80)
    y = y or (1250 if ctx.tall else ctx.H * 0.81)
    words = [w["w"] for w in cur["words"]]
    f = font(F_LYRIC, size)

    def width(ix):
        return f.getlength(" ".join(words[j] for j in ix))
    allw = list(range(len(words)))
    rows = None
    for nrows in ((1, 2, 3) if ctx.tall else (1, 2)):
        rows = _split(allw, nrows, width)
        if max(width(r) for r in rows) <= max_w:
            break
    else:
        return karaoke(img, ctx, int(size * 0.9), y)
    lh = size * 1.2
    top = y - lh * (len(rows) - 1) / 2
    a = min(ease((t - sch["appear"]) / 0.15), 1 - ease((t - (sch["leave"] - 0.12)) / 0.12))
    if a <= 0:
        return
    # a soft dark band behind the lines
    band_h = int(lh * (len(rows) + 1.8))
    shade = Image.new("L", (1, 256))
    shade.putdata([int(130 * math.sin(math.pi * k / 255) ** 0.8) for k in range(256)])
    alpha = shade.resize((img.width, band_h)).point(lambda v: int(v * a))
    img.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (img.width, band_h), 0)] * 3, alpha)),
                        (0, max(0, int(top - lh * 0.9))))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    sp = f.getlength(" ")
    sw = max(2, int(size * 0.04))
    for r, row in enumerate(rows):
        x = ctx.cx - width(row) / 2
        yy = top + r * lh
        for i in row:
            a0, a1 = sch["sweeps"][i]
            if t >= a1:
                col = (*INK, 255)
            elif t >= a0:
                col = (*ACCENT, 255)
            else:
                col = (172, 160, 180, 255)
            d.text((x, yy), words[i], font=f, fill=col, anchor="lm", stroke_width=sw,
                   stroke_fill=(14, 8, 20, 255))
            x += f.getlength(words[i]) + sp
    # who is talking, above the line
    who = speaker_of(cur["text"])
    if who:
        fs = font(F_LYRIC_HEAVY, size * 0.52)
        tw = fs.getlength(who) + 50 * ctx.u
        th = size * 0.8
        tag = Image.new("RGBA", (int(tw), int(th)), (0, 0, 0, 0))
        td = ImageDraw.Draw(tag)
        rounded(td, (0, 0, tag.width - 1, tag.height - 1), th / 2, (*CYAN, 255))
        td.text((tag.width / 2, tag.height / 2), who, font=fs, fill=(14, 8, 20, 255), anchor="mm")
        layer.alpha_composite(tag, (int(ctx.cx - tw / 2), int(top - lh * 0.5 - th - 6 * ctx.u)))
    # ad-libs: a small sticker once the line is sung - if it can stay up long
    # enough, and not when the next line sings the same words ("Or Friday
    # (or this year)" put its sticker up right before "Or this year").
    i_cur = SCHEDULE.index(sch)
    nxt = SCHEDULE[i_cur + 1]["ln"]["text"].lower() if i_cur + 1 < len(SCHEDULE) else ""
    ad_t0 = cur["words"][-1]["s"] - 0.05
    ad_ok = (cur["adlibs"] and not any(x.lower().strip("!?. ") in nxt for x in cur["adlibs"])
             and shows(ad_t0, "adlib " + " ".join(cur["adlibs"]), sch["leave"]))
    if ad_ok and t > ad_t0:
        q = pop((t - ad_t0) / 0.3)
        tag = "  ".join(f"({x})" for x in cur["adlibs"])
        fs = font(F_LYRIC_HEAVY, size * 0.48)
        tw = fs.getlength(tag) + 40 * ctx.u
        last = rows[-1]
        bx = min(ctx.cx + max_w / 2 - tw, ctx.cx + width(last) / 2 - tw * 0.4)
        by = top + (len(rows) - 1) * lh + lh * 0.72
        st = Image.new("RGBA", (int(tw), int(size * 0.8)), (0, 0, 0, 0))
        sd = ImageDraw.Draw(st)
        rounded(sd, (0, 0, st.width - 1, st.height - 1), st.height / 2, (*ACCENT, 255))
        sd.text((st.width / 2, st.height / 2), tag, font=fs, fill=(20, 10, 22, 255), anchor="mm")
        paste(layer, st, bx + tw / 2, by, q, -4)
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
            text(d, (bx0, y - bh - 8 * u), m.get("name", "Boss"), font(F_BOLD, 24 * u), DIM, "lb")
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
    t0 = at(t0)
    q = 1.0 if t0 is None else pop((t - t0) / 0.3)
    if t0 is not None and t < t0:
        return
    if not shows(t0, s):
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



def _duration() -> float:
    import soundfile as sf
    return sf.info(str(AUDIO)).duration


END = _duration() - 0.07     # the video's last frame time; the TV switches off into it


# --------------------------------------------------------------------------
# props

# Official GTA VI screenshots from rockstargames.com/VI/media/screenshots, kept
# out of the repo (`~/.cache/video-automation/song/gta-flu/rockstar/`). The user
# asked for real GTA images (2026-11-18), cut out with core.vision where a
# character is the point. Rockstar's fan policy is non-commercial and excludes
# music videos, so a claim on the upload is possible; the user's call.
ROCKSTAR = Path.home() / ".cache/video-automation/song/gta-flu/rockstar"


@lru_cache(maxsize=16)
def rs_photo(name: str, w: int, h: int, blur: float = 0.0, focus=(0.5, 0.5)) -> Image.Image:
    """An official screenshot, cover-cropped to w x h."""
    im = Image.open(ROCKSTAR / f"{name}.jpg").convert("RGB")
    sc = max(w / im.width, h / im.height)
    im = im.resize((max(w, int(im.width * sc)), max(h, int(im.height * sc))), Image.LANCZOS)
    ox = int((im.width - w) * focus[0])
    oy = int((im.height - h) * focus[1])
    im = im.crop((ox, oy, ox + w, oy + h))
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    return im.convert("RGBA")


@lru_cache(maxsize=16)
def rs_cut(name: str, h: int, crop=None) -> Image.Image:
    """A character cut out of an official screenshot (made once by vision.cutout)."""
    im = Image.open(ROCKSTAR / f"{name}-cut.png").convert("RGBA")
    if crop:
        im = im.crop((int(crop[0] * im.width), int(crop[1] * im.height),
                      int(crop[2] * im.width), int(crop[3] * im.height)))
    return im.resize((int(im.width * h / im.height), int(h)), Image.LANCZOS)


def backdrop(img, ctx, name, amount=0.3, blur=5.0):
    """A dim, soft official screenshot behind a scene."""
    ph = rs_photo(name, ctx.W, ctx.H, blur)
    img.alpha_composite(Image.blend(img, ph, amount))


def thermometer(img, ctx: Ctx, cx, cy, h, frac, hot=False):
    """A fever thermometer, drawn at 3x on its own tile and reduced (smooth edges)."""
    SS = 3
    u = ctx.u * SS
    H = h * SS
    tw = H * 0.17
    br = H * 0.15
    pad = int(30 * u)
    W = int(br * 2 + 2 * pad)
    tile = Image.new("RGBA", (W, int(H + 2 * pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(tile)
    c = W / 2
    top, bulb = pad, pad + H - br
    col = RED if hot else ACCENT
    sw = 1 + 0.03 * ctx.kick
    # glass
    d.rounded_rectangle([c - tw / 2 - 8 * u, top - 8 * u, c + tw / 2 + 8 * u, bulb], radius=int(tw / 2 + 8 * u),
                        fill=(*INK, 255))
    d.ellipse([c - br - 8 * u, bulb - br - 8 * u, c + br + 8 * u, bulb + br + 8 * u], fill=(*INK, 255))
    d.rounded_rectangle([c - tw / 2, top, c + tw / 2, bulb], radius=int(tw / 2), fill=(*PANEL, 255))
    d.ellipse([c - br, bulb - br, c + br, bulb + br], fill=(*col, 255))
    # mercury
    span = bulb - top - tw / 2
    lvl = bulb - span * clamp(frac) * sw
    d.rounded_rectangle([c - tw * 0.3, lvl, c + tw * 0.3, bulb], radius=int(tw * 0.3), fill=(*col, 255))
    # ticks
    for k in range(9):
        y = bulb - span * (k + 1) / 10
        d.line([c + tw / 2 + 14 * u, y, c + tw / 2 + (40 if k % 2 else 26) * u, y], fill=(*INK, 255),
               width=int(4 * u))
    small = tile.resize((tile.width // SS, tile.height // SS), Image.LANCZOS)
    img.alpha_composite(small, (int(round(cx - small.width / 2)), int(round(cy - small.height / 2))))


def card(w, h, fill=(246, 242, 236), r=30):
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    rounded(ImageDraw.Draw(im), (0, 0, w - 1, h - 1), r, (*fill, 255))
    return im


def stamp(img, ctx, s, cx, cy, size, t0, color=RED, rot=-12):
    """A rubber stamp: outlined, slammed in."""
    t = ctx.t
    t0 = at(t0)
    if t < t0 or not shows(t0, s):
        return
    f = font(F_HEAVY, size)
    w = f.getlength(s)
    pad = size * 0.3
    lab = Image.new("RGBA", (int(w + 2 * pad), int(size * 1.45)), (0, 0, 0, 0))
    d = ImageDraw.Draw(lab)
    rounded(d, (2, 2, lab.width - 3, lab.height - 3), size * 0.18, None, (*color, 255), max(3, int(size * 0.09)))
    d.text((lab.width / 2, lab.height / 2), s, font=f, fill=(*color, 255), anchor="mm")
    q = 1 + 1.2 * (1 - ease((t - t0) / 0.18))
    paste(img, lab, cx, cy, q, rot, min(1.0, (t - t0) / 0.08))


def phone(img, ctx: Ctx, cx, cy, h, name, status, status_col=INK, t0=0.0, dim=0.0):
    """A generic phone mid-call: avatar, name, status, the red button. Our own drawing."""
    t, u = ctx.t, ctx.u
    w = h * 0.52
    ph = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(ph)
    rounded(d, (0, 0, w - 1, h - 1), w * 0.16, (10, 8, 14, 255))
    rounded(d, (12 * u, 12 * u, w - 12 * u, h - 12 * u), w * 0.13, (*PANEL, 255))
    # a soft pink-to-violet screen
    grad = Image.new("L", (1, 256))
    grad.putdata([int(90 * (1 - k / 255)) for k in range(256)])
    tint = Image.new("RGBA", ph.size, (*ACCENT, 255))
    mask = grad.resize(ph.size)
    inner = Image.new("L", ph.size, 0)
    ImageDraw.Draw(inner).rounded_rectangle([12 * u, 12 * u, w - 12 * u, h - 12 * u], radius=int(w * 0.13), fill=255)
    ph = Image.composite(Image.alpha_composite(ph, Image.merge("RGBA", (*tint.split()[:3], mask))), ph, inner)
    d = ImageDraw.Draw(ph)
    d.rounded_rectangle([w / 2 - 50 * u, 26 * u, w / 2 + 50 * u, 44 * u], radius=int(9 * u), fill=(10, 8, 14, 255))
    ar = w * 0.22
    d.ellipse([w / 2 - ar, h * 0.26 - ar, w / 2 + ar, h * 0.26 + ar], fill=(*PANEL2, 255))
    face = emoji("🧑‍💼", int(ar * 1.4), t)
    ph.alpha_composite(face, (int(w / 2 - face.width / 2), int(h * 0.26 - face.height / 2)))
    d.text((w / 2, h * 0.47), name, font=fit_font(F_HEAVY, name, w * 0.85, int(h * 0.075)),
           fill=(*INK, 255), anchor="mm")
    d.text((w / 2, h * 0.55), status, font=fit_font(F_MED, status, w * 0.85, int(h * 0.045)),
           fill=(*status_col, 255), anchor="mm")
    br = w * 0.13
    d.ellipse([w / 2 - br, h * 0.82 - br, w / 2 + br, h * 0.82 + br], fill=(*RED, 255))
    d.rounded_rectangle([w / 2 - br * 0.55, h * 0.82 - br * 0.16, w / 2 + br * 0.55, h * 0.82 + br * 0.16],
                        radius=int(br * 0.16), fill=(255, 255, 255, 255))
    if dim:
        veil = Image.new("RGBA", ph.size, (0, 0, 0, int(140 * dim)))
        ph = Image.composite(Image.alpha_composite(ph, veil), ph, inner)
    paste(img, ph, cx, cy, pop((t - t0) / 0.35), math.sin(t * 1.3) * 1.5)


def name_tag(img, ctx, s, cx, cy, col=CYAN):
    u = ctx.u
    f = font(F_LYRIC_HEAVY, 40 * u)
    w, h = f.getlength(s) + 44 * u, 60 * u
    rounded(ImageDraw.Draw(img), (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, (*col, 255))
    ImageDraw.Draw(img).text((cx, cy), s, font=f, fill=(14, 8, 20, 255), anchor="mm")


def call_timer(t, t0):
    s = max(0, int(t - t0))
    return f"{s // 60:02d}:{s % 60:02d}"


def struck(img, ctx, s, cx, cy, size, t0, t_strike, box=PANEL2, ink=INK):
    """A label that gets a red line through it."""
    if ctx.t < t0 or not shows(t0, s):
        return
    big_label(img, ctx, s, cx, cy, size, t0=t0, box=box, ink_on=ink)
    t_strike = at(t_strike)
    if ctx.t > t_strike:
        k = ease((ctx.t - t_strike) / 0.2)
        f = font(F_HEAVY, size)
        w = f.getlength(s) + size * 0.7
        ImageDraw.Draw(img).line([cx - w / 2, cy + size * 0.3, cx - w / 2 + w * k, cy + size * 0.3 - size * 0.6 * k],
                                 fill=(*RED, 255), width=int(size * 0.14))


def progress(img, ctx, cx, cy, w, frac, label, col=None):
    d = ImageDraw.Draw(img)
    u = ctx.u
    h = 64 * u
    rounded(d, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), h / 2, (*PANEL2, 255))
    col = col or CYAN
    if frac > 0.01:
        rounded(d, (cx - w / 2 + 8 * u, cy - h / 2 + 8 * u, cx - w / 2 + 8 * u + (w - 16 * u) * clamp(frac),
                    cy + h / 2 - 8 * u), (h - 16 * u) / 2, (*col, 255))
    text(d, (cx - w / 2, cy - h / 2 - 22 * u), label, font(F_HEAVY, 44 * u), INK, "lb")
    text(d, (cx + w / 2, cy - h / 2 - 22 * u), f"{int(round(clamp(frac) * 100))}%", font(F_HEAVY, 44 * u),
         col, "rb")


def word_t(ln, word, default=None):
    """When `word` (a prefix, any case) is sung in this line."""
    for w in ln["words"]:
        if w["w"].lower().strip(",.?!'").startswith(word.lower()):
            return w["s"]
    return ln["s"] if default is None else default


def mid(ctx):
    x0, y0, x1, y1 = ctx.stage
    return (x0 + x1) / 2, (y0 + y1) / 2


def side(ctx, k):
    """k = -1 left, +1 right of the stage's centre, clear of a centred prop."""
    cx, cy = mid(ctx)
    return cx + k * (430 if not ctx.tall else 320) * ctx.u


# --------------------------------------------------------------------------
# scenes: (start, end, fn). Each draws the picture; the karaoke goes on top.

def L(prefix, n=1):
    return line_at(prefix, n)


HANGUP = 13.50       # the hang-up click, right before the drop
DROP = 13.60


def sc_intro(ctx: Ctx, img):
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    tall = ctx.tall
    h = 600 * u if not tall else 700 * u
    px, py = (cx - 260 * u, cy) if not tall else (cx - 110 * u, cy + 60 * u)
    ended = t >= HANGUP and shows(HANGUP, "call ended")    # 0.1s before the drop: not shown
    phone(img, ctx, px, py, h, "BOSS", "Call ended" if ended else call_timer(t, 0.0),
          RED if ended else INK, t0=-0.3, dim=0.5 if ended else 0)
    # the caller: feverish, then the cough down the line
    ex, ey = (px + 420 * u, cy - 190 * u) if not tall else (cx + 300 * u, py - 120 * u)
    coughing = 2.95 <= t < 3.95
    emo(img, ctx, "🤧" if coughing else "🤒", ex, ey, 180 * u, 0.2)
    name_tag(img, ctx, "ME", ex, ey + (110 if not tall else 115) * u)
    if coughing:
        big_label(img, ctx, "*cough cough*", ex, ey - 120 * u, int(38 * u), t0=2.95, box=ACCENT, rot=-6)
    # Thursday, Friday, this year: each one struck off
    a, b, c = L("I don't think"), L("Or Friday"), L("Or this year")
    days = [("THU", word_t(a, "Thursday"), a["e"] + 0.1), ("FRI", b["s"], b["e"]),
            ("2026", c["s"] + 0.2, c["e"])]
    for k, (s, t0, ts) in enumerate(days):
        if tall:
            x, y = cx + 300 * u, py + 140 * u + k * 115 * u
        else:
            x, y = px + 420 * u, cy + 60 * u + k * 105 * u
        struck(img, ctx, s, x, y, int(56 * u), t0, ts)


def _hook_groups():
    out, cur = [], []
    for ln in TIMING:
        if ln["section"] == "hook" and not ln["text"].startswith(("Texted", "Whole office")):
            if cur and ln["s"] - cur[-1]["e"] > 3:
                out.append(cur)
                cur = []
            cur.append(ln)
    out.append(cur)
    return out


def sc_hook(n):
    """A hook: the fever thermometer climbing, a stamp and an emoji per line."""
    def draw(ctx: Ctx, img):
        t, u = ctx.t, ctx.u
        g = _hook_groups()[n - 1]
        backdrop(img, ctx, "Vice_City_27", 0.28, 4.0)
        cx = ctx.cx
        cy = 345 * u if not ctx.tall else 600 * u
        h = 450 * u if not ctx.tall else 600 * u
        p = clamp((t - g[0]["s"]) / (g[-1]["e"] - g[0]["s"]))
        fever = [ln for ln in g if ln["text"].lower().startswith("two-twelve")]
        hot = any(ln["s"] - 0.1 <= t <= ln["e"] + 0.4 for ln in fever)
        thermometer(img, ctx, cx, cy, h, 0.35 + 0.6 * p + (0.05 if hot else 0), hot=hot)
        lab_y = cy + h / 2 + (45 if not ctx.tall else 60) * u
        lx, rx = cx - (400 if not ctx.tall else 300) * u, cx + (400 if not ctx.tall else 300) * u
        ey = cy - (60 if not ctx.tall else 160) * u
        size = (200 if not ctx.tall else 180) * u
        for i, ln in enumerate(g):
            txt = ln["text"].lower()
            s, e = ln["s"], ln["e"] + 0.3
            if not (s - 0.2 <= t <= e + 0.25):
                continue
            if txt.startswith("can't come in"):
                big_label(img, ctx, "OUT SICK", cx, lab_y, int(70 * u), t0=s, box=RED, ink_on=(255, 255, 255),
                          rot=-4 if i % 2 else 4)
                emo(img, ctx, "🤧" if i % 2 else "🤒", lx, ey, size, s, until=e)
            elif txt.startswith("thirteen"):
                big_label(img, ctx, "13 YEARS", cx, lab_y, int(70 * u), t0=s, box=PANEL2, ink_on=INK)
                emo(img, ctx, "⏳", lx, ey, size, s, until=e)
                emo(img, ctx, "👴", rx, ey, size, word_t(ln, "wait", s + 0.8), until=e)
            elif txt.startswith("two-twelve"):
                big_label(img, ctx, "212 GB FEVER", cx, lab_y, int(70 * u), t0=s, box=ACCENT)
                emo(img, ctx, "🥵", rx, ey, size, s, until=e)
                emo(img, ctx, "🔥", lx, ey, size * 0.9, s + 0.3, until=e)
            elif txt.startswith("tell the boss"):
                emo(img, ctx, "💀", lx, ey, size, word_t(ln, "dying"), until=e)
                emo(img, ctx, "💔", rx, ey, size, word_t(ln, "girl"), until=e)
            elif txt.startswith("see you"):
                big_label(img, ctx, "BACK IN 2027", cx, lab_y, int(70 * u), t0=s, box=CYAN)
                emo(img, ctx, "😎", rx, ey, size, s, until=e)
    return draw


def sc_before(ctx, img):
    """GTA Five dropped, we got Silksong before Six: the list of things we got first."""
    ln = L("GTA Five dropped")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    w, h = (900 * u, 420 * u) if not ctx.tall else (900 * u, 520 * u)
    pc = card(w, h, (246, 242, 236), 36 * u)
    d = ImageDraw.Draw(pc)
    d.text((w / 2, 70 * u), "WE GOT IT BEFORE GTA 6", font=fit_font(F_HEAVY, "WE GOT IT BEFORE GTA 6", w - 80 * u, int(58 * u)),
           fill=(30, 22, 36, 255), anchor="mm")
    rows = [("👽", "Aliens", ln["s"] + 0.5), ("🐛", "Silksong", word_t(ln, "Silksong"))]
    for k, (ch, s, t0) in enumerate(rows):
        if t < t0 or not shows(t0, s):
            continue
        y = (190 + k * (130 if not ctx.tall else 170)) * u
        q = ease((t - t0) / 0.25)
        pc.alpha_composite(emoji(ch, int(90 * u), t - t0), (int(70 * u), int(y - 45 * u)))
        d.text((190 * u, y), s, font=font(F_HEAVY, 56 * u), fill=(30, 22, 36, int(255 * q)), anchor="lm")
        ok = emoji("✅", int(76 * u), t - t0)
        pc.alpha_composite(ok, (int(w - 140 * u), int(y - 38 * u)))
    paste(img, pc, cx, cy + 10 * u, pop((t - (ln["s"] - 0.2)) / 0.35), -2)
    big_label(img, ctx, "GTA V · 2013", cx, cy - h / 2 - (10 if not ctx.tall else 60) * u, int(48 * u),
              t0=ln["s"], box=ACCENT, rot=-4)


def sc_refreshing(ctx, img):
    """Still refreshing for a fix: a search box asks, the answer stays no."""
    ln = L("Lived through")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    w = 1100 * u if not ctx.tall else 900 * u
    d = ImageDraw.Draw(img)
    y = cy - 90 * u
    rounded(d, (cx - w / 2, y - 55 * u, cx + w / 2, y + 55 * u), 55 * u, (246, 242, 236, 255))
    q = "is gta 6 out yet"
    n = int(clamp((t - ln["s"]) / 1.0) * len(q))
    d.text((cx - w / 2 + 50 * u, y), q[:n], font=font(F_MED, 50 * u), fill=(30, 22, 36, 255), anchor="lm")
    tr = word_t(ln, "refreshing")
    if t > tr:
        spins = (t - tr) * 400
        paste(img, emoji("🔄", int(80 * u), t), cx + w / 2 - 70 * u, y, 1, -spins)
        # every refresh: the same answer
        k = int((t - tr) / 0.5)
        big_label(img, ctx, "No." if k % 2 == 0 else "Still no.", cx, y + 160 * u, int(90 * u), t0=tr + 0.1,
                  box=RED, ink_on=(255, 255, 255), rot=-3)
    emo(img, ctx, "😷", cx - w / 2 + 40 * u, y - 170 * u, 150 * u, ln["s"])


def calendar(img, ctx, cx, cy, top, big, t0, scale=1.0, rot=0.0):
    t0 = at(t0)
    if ctx.t < t0 or not shows(t0, f"calendar {top}"):
        return
    u = ctx.u * scale
    w, h = 340 * u, 360 * u
    cal = card(w, h, (246, 242, 236), 30 * u)
    d = ImageDraw.Draw(cal)
    rounded(d, (0, 0, w - 1, 100 * u), 30 * u, (*ACCENT, 255))
    d.rectangle([0, 60 * u, w, 100 * u], fill=(*ACCENT, 255))
    d.text((w / 2, 52 * u), top, font=fit_font(F_HEAVY, top, w - 40 * u, int(48 * u)), fill=(255, 255, 255, 255),
           anchor="mm")
    d.text((w / 2, 225 * u), big, font=fit_font(F_HEAVY, big, w - 40 * u, int(120 * u)), fill=(30, 22, 36, 255),
           anchor="mm")
    paste(img, cal, cx, cy, pop((ctx.t - t0) / 0.35), rot)


def sc_delays(ctx, img):
    """Fall became May, then they pushed it one more time: three dates, two stamps."""
    ln = L("Fall became May")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    gap = 380 * u if not ctx.tall else 310 * u
    sc = 1.0 if not ctx.tall else 0.85
    tm, tp = word_t(ln, "May"), word_t(ln, "pushed")
    cards = [("FALL", "2025", ln["s"], tm), ("MAY 26", "2026", tm, tp),
             ("NOV 19", "2026", word_t(ln, "time", tp + 0.6), None)]
    for k, (top, big, t0, t_stamp) in enumerate(cards):
        x = cx + (k - 1) * gap
        calendar(img, ctx, x, cy, top, big, t0 - 0.1, sc, (k - 1) * 4)
        if t_stamp is not None:
            stamp(img, ctx, "DELAYED", x, cy + 215 * u * sc, int(50 * u * sc), t_stamp, rot=-8)


def sc_polish(ctx, img):
    """Needs more polish? Cool, I polished my PS Five."""
    ln = L("Needs more polish")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    big_label(img, ctx, "“needs more polish”", cx, cy - 210 * u, int(56 * u), t0=ln["s"], box=PANEL2,
              ink_on=INK, rot=-3)
    tp = word_t(ln, "polished")
    emo(img, ctx, "🎮", cx, cy + 60 * u, 260 * u, word_t(ln, "Cool") - 0.1)
    if t > tp and shows(tp, "sponge"):
        k = t - tp
        paste(img, emoji("🧽", int(130 * u), t), cx + 150 * u * math.sin(k * 9), cy + 40 * u + 30 * u * math.cos(k * 9))
        for j, (dx, dy) in enumerate(((-230, -60), (230, -20), (-170, 170), (200, 180))):
            emo(img, ctx, "✨", cx + dx * u, cy + 60 * u + dy * u, 110 * u, tp + 0.15 * j)


def sc_towel(ctx, img):
    """Wrapped it in a towel and I gave it a fade: the console at the barber's."""
    ln = L("Wrapped it")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    d = ImageDraw.Draw(img)
    tw, th = 380 * u, 300 * u
    q = ease((t - ln["s"]) / 0.4)
    if q > 0:
        d.polygon([(cx - tw / 2, cy + 40 * u), (cx + tw / 2, cy + 40 * u), (cx + tw / 2 * 1.1, cy + th),
                   (cx - tw / 2 * 1.1, cy + th)], fill=(70, 190, 120, int(255 * q)))
        for k in range(4):
            yy = cy + 80 * u + k * 50 * u
            d.line([cx - tw / 2, yy, cx + tw / 2, yy], fill=(50, 150, 95, int(255 * q)), width=int(6 * u))
    emo(img, ctx, "🎮", cx, cy - 40 * u, 230 * u, ln["s"] - 0.1)
    tf = word_t(ln, "fade")
    emo(img, ctx, "✂️", cx + 230 * u + 20 * u * math.sin(t * 14), cy - 150 * u, 140 * u, word_t(ln, "gave"), rot=-20)
    emo(img, ctx, "💈", side(ctx, -1), cy, 170 * u, ln["s"] + 0.3)
    big_label(img, ctx, "FRESH FADE", cx, cy - 280 * u, int(64 * u), t0=tf, box=CYAN, rot=4)


def sc_dust(ctx, img):
    """Blew the dust out the fan and now I'm coughing all day."""
    ln = L("Blew the dust")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    emo(img, ctx, "🌀", cx - 200 * u, cy, 240 * u, ln["s"], rot=-t * 600)
    tb = ln["s"] + 0.2
    if t > tb:
        d = ImageDraw.Draw(img)
        rng = np.random.default_rng(3)
        for k in range(70):
            ph = ((t - tb) * 0.6 + rng.random()) % 1
            x = cx - 120 * u + ph * 650 * u + 40 * u * math.sin(k + t * 3)
            y = cy + (rng.random() - 0.5) * 300 * u - ph * 80 * u
            r = (6 + 16 * rng.random()) * u * (1 - ph * 0.5)
            d.ellipse([x - r, y - r, x + r, y + r], fill=(170, 160, 170, int(200 * (1 - ph))))
    tc = word_t(ln, "coughing")
    emo(img, ctx, "🤧", cx + 280 * u, cy - 40 * u, 220 * u, tc)
    if t > tc:
        big_label(img, ctx, "ALL DAY", cx + 280 * u, cy + 150 * u, int(56 * u), t0=word_t(ln, "day"), box=ACCENT)


def sc_price(ctx, img):
    """Eighty for the game and there's no disc in the box."""
    ln = L("Eighty for the game")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    big_label(img, ctx, "$79.99", cx - (300 if not ctx.tall else 0) * u, cy - (40 if not ctx.tall else 280) * u,
              int(110 * u), t0=ln["s"], box=YELLOW, rot=-6)
    bx = cx + (260 if not ctx.tall else 0) * u
    by = cy + (0 if not ctx.tall else 120) * u
    emo(img, ctx, "📦", bx, by, 260 * u, word_t(ln, "there's"))
    td = word_t(ln, "disc")
    emo(img, ctx, "💿", bx, by - 230 * u, 140 * u, td)
    emo(img, ctx, "❌", bx, by - 230 * u, 170 * u, td + 0.25)
    if t > td + 0.4:
        big_label(img, ctx, "just a download code", bx, by + 200 * u, int(42 * u), t0=td + 0.4, box=PANEL2,
                  ink_on=INK)


def sc_preload(ctx, img):
    """Pre-load day, the broadband had a heart attack: the line flatlines."""
    ln = L("Pre-load day")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    x0, y0, x1, y1 = ctx.stage
    th = word_t(ln, "heart")
    w = (x1 - x0) * 0.86
    frac = 0.12 + 0.55 * clamp((t - ln["s"]) / max(0.5, th - ln["s"]))
    progress(img, ctx, cx, cy - 170 * u, w, frac, "Pre-load · 212 GB", RED if t > th else CYAN)
    # the broadband's heartbeat
    d = ImageDraw.Draw(img)
    pts = []
    flat = t > th
    for k in range(240):
        x = cx - w / 2 + w * k / 239
        ph = (k / 239 * 4 - t * 1.6) % 1
        beat = 0 if flat else (-120 * math.exp(-((ph - 0.5) * 22) ** 2) + 50 * math.exp(-((ph - 0.56) * 22) ** 2))
        pts.append((x, cy + 90 * u + beat * u))
    d.line(pts, fill=(*(RED if flat else GREEN), 255), width=int(8 * u), joint="curve")
    emo(img, ctx, "💔", cx, cy + (260 if not ctx.tall else 280) * u, 150 * u, th)
    if flat:
        big_label(img, ctx, "CONNECTION LOST", cx, cy + 90 * u, int(56 * u), t0=th + 0.25, box=RED,
                  ink_on=(255, 255, 255), rot=-3)


def sc_delete(ctx, img):
    """Deleted all my games, they're never coming back: into the bin, one by one."""
    ln = L("Deleted all my games")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    x0, y0, x1, y1 = ctx.stage
    progress(img, ctx, cx, y0 + 90 * u, (x1 - x0) * 0.8, 0.98 - 0.6 * clamp((t - ln["s"]) / 2.2),
             "Storage", RED)
    bin_x, bin_y = cx + (380 if not ctx.tall else 300) * u, cy + 120 * u
    emo(img, ctx, "🗑️", bin_x, bin_y, 210 * u, ln["s"])
    for k in range(5):
        t0 = ln["s"] + 0.15 + k * 0.38
        sx, sy = cx - (420 if not ctx.tall else 330) * u + k * 70 * u, cy + 60 * u
        if t < t0:
            paste(img, emoji("🎮", int(110 * u), t), sx, sy)
            continue
        k_ = ease((t - t0) / 0.45)
        if k_ < 1:
            x = sx + (bin_x - sx) * k_
            y = sy - 200 * u * math.sin(k_ * math.pi) + (bin_y - 40 * u - sy) * k_
            paste(img, emoji("🎮", int(110 * u), t), x, y, 1 - 0.5 * k_, k_ * 300)
    emo(img, ctx, "👋", cx - 60 * u, cy - 120 * u, 160 * u, word_t(ln, "never"))


def sc_lucia(ctx, img):
    """Girl said it's me or Lucia, I said lemme think. Lucia is the real one, cut out."""
    ln = L("Girl said")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    gap = 360 * u if not ctx.tall else 270 * u
    w, h = (330 * u, 440 * u) if not ctx.tall else (300 * u, 420 * u)
    for k, (name, col, t0) in enumerate((("ME", CYAN, word_t(ln, "me")), ("LUCIA", ACCENT, word_t(ln, "Lucia")))):
        x = cx + (-1 if k == 0 else 1) * gap
        c = card(w, h, (246, 242, 236), 30 * u)
        d = ImageDraw.Draw(c)
        pic = (int(w - 40 * u), int(h * 0.72))
        win = Image.new("RGBA", pic, (*col, 255))
        if k == 0:
            e = emoji("👩", int(200 * u), t)
            win.alpha_composite(e, (int(pic[0] / 2 - e.width / 2), int(pic[1] / 2 - e.height / 2)))
        else:
            luc = rs_cut("Lucia_Caminos_11", int(pic[1] * 1.25), crop=(0.42, 0.0, 1.0, 0.86))
            win.alpha_composite(luc, (int(pic[0] / 2 - luc.width / 2), int(pic[1] - luc.height + 30 * u)))
        mask = Image.new("L", pic, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, pic[0] - 1, pic[1] - 1], radius=int(22 * u), fill=255)
        c.paste(win, (int(20 * u), int(20 * u)), mask)
        d.text((w / 2, h * 0.88), name, font=font(F_HEAVY, 60 * u), fill=(30, 22, 36, 255), anchor="mm")
        if t >= t0 - 0.1 and shows(t0 - 0.1, f"card {name}"):
            paste(img, c, x, cy, pop((t - t0 + 0.1) / 0.35), (-1 if k == 0 else 1) * 5)
    big_label(img, ctx, "OR", cx, cy, int(70 * u), t0=word_t(ln, "or"), box=PANEL2, ink_on=INK)
    emo(img, ctx, "🤔", cx, cy - 260 * u, 170 * u, word_t(ln, "think"))


def sc_fridge(ctx, img):
    """She left a note on the fridge, I'll read it in a week."""
    ln = L("She left a note")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    d = ImageDraw.Draw(img)
    fw, fh = 360 * u, 600 * u if not ctx.tall else 760 * u
    fx = cx - (200 if not ctx.tall else 0) * u
    q = ease((t - (ln["s"] - 0.2)) / 0.3)
    if q > 0:
        rounded(d, (fx - fw / 2, cy - fh / 2, fx + fw / 2, cy + fh / 2), 34 * u, (230, 232, 236, int(255 * q)))
        d.line([fx - fw / 2, cy - fh / 2 + fh * 0.36, fx + fw / 2, cy - fh / 2 + fh * 0.36], fill=(190, 192, 198, 255),
               width=int(5 * u))
        for yy in (cy - fh / 2 + fh * 0.12, cy - fh / 2 + fh * 0.48):
            rounded(d, (fx + fw / 2 - 50 * u, yy, fx + fw / 2 - 30 * u, yy + 120 * u), 10 * u, (170, 172, 180, 255))
    tn = word_t(ln, "note")
    if t > tn and shows(tn, "fridge note"):
        nw = 230 * u
        note = card(nw, nw, (255, 226, 90), 8 * u)
        nd = ImageDraw.Draw(note)
        for k, s in enumerate(("we need", "to talk")):
            nd.text((nw / 2, nw * (0.4 + 0.24 * k)), s, font=font(F_HEAVY, 38 * u), fill=(60, 40, 20, 255), anchor="mm")
        paste(img, note, fx - 20 * u, cy - fh * 0.2, pop((t - tn) / 0.3), 6)
    tw = word_t(ln, "week")
    rx = cx + (300 if not ctx.tall else 0) * u
    ry = cy + (0 if not ctx.tall else fh / 2 + 10 * u)
    if not ctx.tall:
        emo(img, ctx, "🙈", rx, ry - 120 * u, 190 * u, word_t(ln, "read"))
        big_label(img, ctx, "READ LATER", rx, ry + 90 * u, int(58 * u), t0=tw, box=CYAN, rot=-4)
    else:
        stamp(img, ctx, "READ LATER", fx, cy + fh * 0.25, int(64 * u), tw, CYAN, -8)
        emo(img, ctx, "🙈", fx + fw / 2 + 80 * u, cy - fh * 0.32, 150 * u, word_t(ln, "read"))


def sc_note(ctx, img):
    """Bought a doctor's note off a guy named Florida Man."""
    ln = L("Bought a doctor's note")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    w, h = (760 * u, 600 * u) if not ctx.tall else (860 * u, 760 * u)
    pc = card(w, h, (250, 248, 242), 18 * u)
    d = ImageDraw.Draw(pc)
    d.text((w / 2, 70 * u), "DOCTOR'S NOTE", font=font(F_HEAVY, 60 * u), fill=(30, 22, 36, 255), anchor="mm")
    d.line([50 * u, 120 * u, w - 50 * u, 120 * u], fill=(200, 190, 200, 255), width=int(4 * u))
    rows = [("Patient:", "me"), ("Diagnosis:", "GTA flu"), ("Rest until:", "2027")]
    for k, (a, b) in enumerate(rows):
        y = (190 + k * 85) * u
        d.text((60 * u, y), a, font=font(F_MED, 46 * u), fill=(120, 100, 120, 255), anchor="lm")
        d.text((330 * u, y), b, font=font(F_HEAVY, 50 * u), fill=(30, 22, 36, 255), anchor="lm")
    tf = word_t(ln, "Florida")
    if t > tf and shows(tf, "signature"):
        sig = "Florida Man"
        n = int(clamp((t - tf) / 0.6) * len(sig))
        d.text((60 * u, h - 110 * u), "Signed:", font=font(F_MED, 46 * u), fill=(120, 100, 120, 255), anchor="lm")
        d.text((280 * u, h - 110 * u), sig[:n], font=font(F_BOLD, 64 * u), fill=(40, 70, 190, 255), anchor="lm")
    paste(img, pc, cx, cy, pop((t - (ln["s"] - 0.2)) / 0.35), -2)
    emo(img, ctx, "🐊", cx + w / 2 - 60 * u, cy + h / 2 - 60 * u, 180 * u, tf + 0.3, rot=-10)


def sc_countdown(ctx, img):
    """Refresh, eleven fifty-nine: the last two minutes before midnight."""
    a, b = L("Refresh"), L("Eleven fifty-nine")
    t, u = ctx.t, ctx.u
    backdrop(img, ctx, "Vice_City_27", 0.4, 3.0)
    cx, cy = mid(ctx)
    s = "11:59 PM" if t >= b["s"] else "11:58 PM"
    big_label(img, ctx, s, cx, cy - 30 * u, int((200 if not ctx.tall else 160) * u), color=INK)
    if a["s"] - 0.1 <= t <= a["e"] + 0.6:
        big_label(img, ctx, "refresh", cx + 40 * u, cy + 170 * u, int(60 * u), t0=a["s"], box=ACCENT)
        paste(img, emoji("🔄", int(90 * u), t), cx - 170 * u, cy + 170 * u, 1, -(t - a["s"]) * 360)
    cough = T(107.62)
    ey = cy + (190 if not ctx.tall else -300) * u
    if cough <= t < cough + 1.0:
        emo(img, ctx, "🤧", cx + (440 if not ctx.tall else 0) * u, ey, 170 * u, cough)
    emo(img, ctx, "⏳", cx - (440 if not ctx.tall else 0) * u, ey, 160 * u, a["s"], until=cough - 0.05)


def sc_midnight(ctx, img):
    """Midnight, press start."""
    ln = L("Midnight")
    t, u = ctx.t, ctx.u
    backdrop(img, ctx, "Vice_City_27", 0.62, 0.0)
    cx, cy = mid(ctx)
    big_label(img, ctx, "12:00 AM", cx, cy - 120 * u, int(170 * u), color=YELLOW, t0=ln["s"] - 0.05)
    tp = word_t(ln, "press")
    if t > tp and int((t - tp) * 3) % 2 == 0:
        big_label(img, ctx, "PRESS START", cx, cy + 120 * u, int(90 * u), t0=tp, box=ACCENT)
    emo(img, ctx, "🎮", side(ctx, 1) + (60 if not ctx.tall else 0) * u, cy + (120 if not ctx.tall else 330) * u,
        180 * u, tp)


def synth_sun(w, h, t, u):
    """A striped 80s sunset over a grid sea. Generic Miami, drawn here."""
    im = Image.new("RGBA", (int(w), int(h)), (*BG, 255))
    d = ImageDraw.Draw(im)
    for y in range(int(h * 0.62)):         # sky
        k = y / (h * 0.62)
        col = tuple(int(a + (b - a) * k) for a, b in zip((40, 12, 70), (255, 90, 150)))
        d.line([0, y, w, y], fill=(*col, 255))
    r = min(w, h) * 0.3
    sx, sy = w / 2, h * 0.58
    for y in range(int(sy - r), int(sy)):
        k = (y - (sy - r)) / r
        if k > 0.45 and int((y - (sy - r)) / (r * 0.07)) % 2 == 1:
            continue                      # the stripes
        half = math.sqrt(max(0.0, r * r - (y - sy) ** 2))
        col = tuple(int(a + (b - a) * k) for a, b in zip((255, 220, 90), (255, 70, 150)))
        d.line([sx - half, y, sx + half, y], fill=(*col, 255))
    sea = h * 0.62
    d.rectangle([0, sea, w, h], fill=(20, 10, 40, 255))
    for k in range(1, 12):                # receding grid
        y = sea + (h - sea) * (k / 11) ** 2.2
        d.line([0, y, w, y], fill=(*CYAN, 200), width=max(1, int(2 * u)))
    off = (t * 0.25) % 1
    for k in range(-12, 13):
        x2 = w / 2 + (k + off) * w * 0.16
        d.line([w / 2 + (k + off) * w * 0.02, sea, x2, h], fill=(*CYAN, 160), width=max(1, int(2 * u)))
    return im


def sc_vice(ctx, img):
    """Vice City got better graphics than outside: drizzle against neon."""
    ln = L("Vice City got")
    t, u = ctx.t, ctx.u
    W, H = ctx.W, ctx.H
    tall = ctx.tall
    # left (top, in 9:16): outside, grey and wet
    # 9:16: outside on top, Vice City under it, both clear of the karaoke
    a_box = (0, 0, W // 2, H) if not tall else (0, 0, W, int(640 * u))
    b_box = (W // 2, 0, W, H) if not tall else (0, int(640 * u), W, int(1160 * u))
    grey = Image.new("RGBA", (a_box[2] - a_box[0], a_box[3] - a_box[1]), (86, 90, 98, 255))
    gd = ImageDraw.Draw(grey)
    rng = np.random.default_rng(5)
    for k in range(90):
        x = (rng.random() * grey.width + t * 120) % grey.width
        y = (rng.random() * grey.height + t * 900) % grey.height
        gd.line([x, y, x - 8 * u, y + 40 * u], fill=(170, 176, 186, 200), width=int(3 * u))
    img.alpha_composite(grey, a_box[:2])
    # the real thing: Rockstar's own Vice City skyline, pushing in slowly
    bw, bh = b_box[2] - b_box[0], b_box[3] - b_box[1]
    z = 1 + 0.05 * clamp((t - ln["s"]) / 4)
    sun = rs_photo("Vice_City_15", int(bw * z), int(bh * z), 0.0, (0.45, 0.5))
    sun = sun.crop((int((sun.width - bw) / 2), int((sun.height - bh) / 2),
                    int((sun.width - bw) / 2) + bw, int((sun.height - bh) / 2) + bh))
    q = clamp((t - word_t(ln, "graphics")) / 0.6)
    if q > 0:
        try:
            sun = shaderfx.apply(sun.convert("RGB"), f"bloom:{0.6 * q:.2f}", t, SONG).convert("RGBA")
        except Exception:
            pass
    img.alpha_composite(sun, b_box[:2])
    ax, ay = (a_box[0] + a_box[2]) / 2, (a_box[1] + a_box[3]) / 2
    bx, by = (b_box[0] + b_box[2]) / 2, (b_box[1] + b_box[3]) / 2
    if tall:
        ay, by = ay + 90 * u, by - 40 * u
    else:
        ay, by = ay - 120 * u, by - 120 * u
    big_label(img, ctx, "OUTSIDE", ax, ay - 60 * u, int(80 * u), t0=word_t(ln, "outside") - 0.1, box=PANEL2,
              ink_on=INK)
    big_label(img, ctx, "VICE CITY", bx, by - 60 * u, int(80 * u), t0=ln["s"], box=ACCENT)
    tg = word_t(ln, "graphics")
    big_label(img, ctx, "4/10", ax, ay + 70 * u, int(70 * u), t0=tg + 0.2, box=RED, ink_on=(255, 255, 255), rot=-5)
    big_label(img, ctx, "10/10", bx, by + 70 * u, int(70 * u), t0=tg, box=GREEN, rot=5)
    emo(img, ctx, "🌴", bx + (300 if not tall else 360) * u, by + 30 * u, 170 * u, ln["s"] + 0.3)


def sms(img, ctx, msgs, box):
    """A text thread: [{who: me|them, text, t0, name?}]."""
    t, u = ctx.t, ctx.u
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    rounded(d, (x0, y0, x1, y1), 40 * u, (*PANEL, 255), (*PANEL2, 255), 3 * u)
    d.text(((x0 + x1) / 2, y0 + 50 * u), "Messages · Boss", font=font(F_HEAVY, 40 * u), fill=(*INK, 255),
           anchor="mm")
    d.line([x0, y0 + 95 * u, x1, y0 + 95 * u], fill=(*PANEL2, 255), width=int(2 * u))
    f = font(F_MED, 46 * u)
    y = y0 + 160 * u
    for m in msgs:
        m = {**m, "t0": at(m["t0"])}
        if t < m["t0"] or not shows(m["t0"], "sms " + m["text"]):
            continue
        lines, cur = [], ""
        for w in m["text"].split():
            trial = (cur + " " + w).strip()
            if f.getlength(trial) > (x1 - x0) * 0.62 and cur:
                lines.append(cur)
                cur = w
            else:
                cur = trial
        lines.append(cur)
        lh = f.size * 1.3
        bw = max(f.getlength(s) for s in lines) + 60 * u
        bh = lh * len(lines) + 34 * u
        me = m["who"] == "me"
        bx = x1 - 40 * u - bw if me else x0 + 40 * u
        q = pop((t - m["t0"]) / 0.3)
        who = "ME" if me else "BOSS"
        d.text((bx + (bw - 10 * u if me else 10 * u), y - 6 * u), who, font=font(F_LYRIC_HEAVY, 30 * u),
               fill=(*(ACCENT if me else CYAN), 255), anchor="rb" if me else "lb")
        y += 6 * u
        bub = Image.new("RGBA", (int(bw), int(bh)), (0, 0, 0, 0))
        bd = ImageDraw.Draw(bub)
        rounded(bd, (0, 0, bw - 1, bh - 1), 30 * u, (*(ACCENT if me else PANEL2), 255))
        for k, s in enumerate(lines):
            bd.text((30 * u, 17 * u + k * lh), s, font=f, fill=(*((30, 14, 30) if me else INK), 255))
        paste(img, bub, bx + bw / 2, y + bh / 2, q)
        y += bh + 30 * u


def sc_texted(ctx, img):
    """Texted in to work and my boss replied, me too."""
    ln = L("Texted in")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    box = (cx - 520 * u, ctx.stage[1] + 40 * u, cx + 520 * u, ctx.stage[1] + 470 * u) if not ctx.tall else \
        (ctx.stage[0], ctx.stage[1] + 200 * u, ctx.stage[2], ctx.stage[1] + 760 * u)
    tr = word_t(ln, "replied")
    sms(img, ctx, [{"who": "me", "text": "can't come in, got the GTA flu", "t0": ln["s"]},
                   {"who": "them", "text": "me too", "t0": word_t(ln, "me", tr + 0.4)}], box)
    # the boss sneezes in the empty corner, clear of both bubbles
    emo(img, ctx, "🤧", box[2] - 110 * u, box[3] - 100 * u, 150 * u, word_t(ln, "me", tr + 0.4) + 0.2)


def sc_office(ctx, img):
    """Whole office got the GTA flu."""
    ln = L("Whole office")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    cols, rows = (6, 2) if not ctx.tall else (4, 3)
    step = 170 * u
    for k in range(cols * rows):
        x = cx + (k % cols - (cols - 1) / 2) * step
        y = cy + 60 * u + (k // cols - (rows - 1) / 2) * step
        emo(img, ctx, ("🤒", "🤧", "😷")[k % 3], x, y, 140 * u, ln["s"] + 0.05 * k)
    big_label(img, ctx, "OFFICE CLOSED", cx, cy - (rows * step / 2 + 80 * u), int(76 * u),
              t0=word_t(ln, "office"), box=RED, ink_on=(255, 255, 255), rot=-3)


def sc_outro(ctx, img):
    """Boss? Here we go again: the same call, and nobody answers."""
    ln = L("Boss? Here")
    t, u = ctx.t, ctx.u
    cx, cy = mid(ctx)
    beeps = T(147.70)
    tall = ctx.tall
    h = 600 * u if not tall else 700 * u
    px, py = (cx - 260 * u, cy) if not tall else (cx - 110 * u, cy + 60 * u)
    ended = t >= beeps and shows(beeps, "call ended")
    phone(img, ctx, px, py, h, "BOSS", "Call ended" if ended else "Calling…", RED if ended else INK,
          t0=ln["s"] - 0.6, dim=0.5 if ended else 0)
    ex, ey = (px + 420 * u, cy - 190 * u) if not tall else (cx + 300 * u, py - 120 * u)
    emo(img, ctx, "🤒", ex, ey, 180 * u, ln["s"] - 0.4)
    if t > ln["s"] - 0.3:
        name_tag(img, ctx, "ME", ex, ey + 115 * u)


def sc_end(ctx, img):
    """The title, the thermometer, and Jason and Lucia cut out of an official shot."""
    t0 = SCENE["start"]
    q = ease((ctx.t - t0) / 0.5)
    d = ImageDraw.Draw(img)
    u = ctx.u
    backdrop(img, ctx, "Vice_City_27", 0.3 * q, 6.0)
    duo = rs_cut("Jason_and_Lucia_17", int(ctx.H * 0.86))
    paste(img, duo, ctx.W * 0.30, ctx.H - duo.height / 2 + 20 * u * (1 - q), 1.0, 0, q)
    tx = ctx.W * 0.74
    f = fit_font(F_COND, "GTA FLU", ctx.W * 0.42, int(230 * u))
    d.text((tx, ctx.H * 0.33), "GTA FLU", font=f, fill=(*ACCENT, int(255 * q)), anchor="mm")
    if q > 0.3:
        thermometer(img, ctx, tx, ctx.H * 0.66, 340 * u, 0.97, hot=True)



def scenes() -> list[tuple[float, float, object, dict]]:
    """(start, end, draw, opts). opts: karaoke=False hides the lyric layer."""
    g = _hook_groups()
    v = [L(p) for p in ("GTA Five dropped", "Lived through", "Fall became May", "Needs more polish",
                        "Wrapped it", "Blew the dust", "Eighty for the game", "Pre-load day",
                        "Deleted all my games", "Girl said", "She left a note", "Bought a doctor's note")]
    br = [L("Refresh"), L("Midnight"), L("Vice City got")]
    last = g[-1]
    texted, office, outro = L("Texted in"), L("Whole office"), L("Boss? Here")
    S = [(0.0, DROP, sc_intro, {}),
         (DROP, v[0]["s"] - 0.25, sc_hook(1), {})]
    fns = [sc_before, sc_refreshing, sc_delays, sc_polish, sc_towel, sc_dust, sc_price, sc_preload,
           sc_delete, sc_lucia, sc_fridge, sc_note]
    for k, fn in enumerate(fns):
        a = v[k]["s"] - 0.25
        b = v[k + 1]["s"] - 0.25 if k + 1 < len(v) else None
        S.append((a, b, fn, {}))
    if FMT == "long":
        S[-1] = (S[-1][0], g[1][0]["s"] - 0.25, S[-1][2], {})
        S.append((g[1][0]["s"] - 0.25, br[0]["s"] - 0.25, sc_hook(2), {}))
    else:
        S[-1] = (S[-1][0], br[0]["s"] - 0.25, S[-1][2], {})
    S += [(br[0]["s"] - 0.25, br[1]["s"] - 0.25, sc_countdown, {}),
          (br[1]["s"] - 0.25, br[2]["s"] - 0.25, sc_midnight, {}),
          (br[2]["s"] - 0.25, last[0]["s"] - 0.25, sc_vice, {}),
          (last[0]["s"] - 0.25, texted["s"] - 0.25, sc_hook(len(g)), {}),
          (texted["s"] - 0.25, office["s"] - 0.2, sc_texted, {}),
          (office["s"] - 0.2, outro["s"] - 0.7, sc_office, {}),
          (outro["s"] - 0.7, outro["e"] + 0.4, sc_outro, {}),
          # the long one's end card holds ~2.5s (it came in 1s before the TV-off)
          (outro["e"] + 0.4, 999, sc_end, {"karaoke": False})]
    if FMT == "short":          # it loops: the call ends and the intro's call starts again
        S[-2] = (S[-2][0], 999, sc_outro, {})
        S.pop()
    return S


HITS = [(DROP, 0.9)]


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
    out = MIX.parent / f"soundtrack-{FMT}.wav"
    sf.write(out, np.clip(x, -1, 1), sr, subtype="PCM_24")
    return out


def render_frame(frame: Frame, t: float, kick: float, S) -> Image.Image:
    ctx = Ctx(frame, t, kick)
    sc = next(s for s in S if s[0] <= t < s[1])
    SCENE["start"], SCENE["end"], SCENE["name"] = sc[0], sc[1], getattr(sc[2], "__name__", "scene")
    hue = RED if sc[2] in (sc_office,) else ACCENT
    img = background(ctx, hue)
    sc[2](ctx, img)
    if sc[3].get("karaoke", True):
        karaoke(img, ctx)
    # a cut flash in the first frames of a scene
    age = t - sc[0]
    if 0 <= age < 0.12 and sc[0] > 0.5:
        img = Image.blend(img, Image.new("RGBA", img.size, (255, 255, 255, 255)), 0.12 * (1 - age / 0.12))
    out = img.convert("RGB")
    # the drop and the office closing shake and split colour
    for h, dur in HITS + [(word_t(L("Whole office"), "office"), 0.7)]:
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
    ap.add_argument("--audit", action="store_true",
                    help="list every pop the MIN_HOLD rule hides (samples 5 fps, writes nothing)")
    a = ap.parse_args()
    frame = LANDSCAPE if a.fmt == "long" else VERTICAL
    if not MIX.exists():
        MIX.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AUDIO), str(MIX)], check=True)
    import soundfile as sf
    dur = sf.info(str(AUDIO)).duration
    n = int(dur * FPS)
    kick = kick_envelope(n)
    S = scenes()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.audit:
        with emoji_anim.enabled(False):
            for i in range(0, n, FPS // 5):
                render_frame(frame, i / FPS, float(kick[i]), S)
        for (scene, what, t0), held in sorted(AUDIT.items(), key=lambda kv: kv[0][2]):
            print(f"{t0:7.2f}  {held:5.2f}s  {scene:14s} {what}")
        print(f"{len(AUDIT)} hidden (shorter than {MIN_HOLD}s on screen)")
        return 0
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
        out = OUT / f"gta-flu-{a.fmt}{suffix}.mp4"
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
