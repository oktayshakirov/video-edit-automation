"""Render a short clip of every visual tool added on 2026-11-05, to look at.

    PYTHONPATH=. .venv/bin/python tools/visual_demo.py            # all
    PYTHONPATH=. .venv/bin/python tools/visual_demo.py pile behind

Writes `~/Desktop/visual-demo/<name>.mp4` (and a `.jpg` of a middle frame)
from images already in `assets/`, with the real fonts on the Mac - the
point of running it there. Each demo is independent: one whose model,
browser or GL context is missing says so and the rest still render.

| name | what it shows | needs |
| --- | --- | --- |
| parallax | a still moving in depth vs the flat Ken Burns | `vision fetch` |
| isolate | the room dimming around two people | `vision fetch` |
| pop | a head breaking out of a Short's photo frame | `vision fetch` |
| behind | the word behind the subject, 16:9 and 9:16 | `vision fetch` |
| pile | coins pouring in, then the trapdoors opening | pymunk |
| emoji | a grid whose icons animate | network once |
| shaders | bloom, leak, aberration, vignette on real frames | OpenGL |
| screencap | the camera ringing passages of a local article page | chromium |
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import traceback
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from video_automation.core.brand import CRYPTO  # noqa: E402
from video_automation.core.frame import LANDSCAPE, VERTICAL  # noqa: E402

OUT = Path.home() / "Desktop/visual-demo"
A = REPO / "assets"
SKYLINE = A / "crypto/whale/nyc-skyscrapers.jpg"
DUROV = A / "crypto/billionaires/durov.jpg"
VITALIK = A / "crypto/vitalik-buterin/vitalik-techcrunch-wide.jpg"
SAYLOR = A / "crypto/billionaires/saylor.jpg"


def write(name, frames_fn, n, frame, fps=30):
    """Encode `frames_fn(i)` for i in range(n); keep the middle frame."""
    OUT.mkdir(parents=True, exist_ok=True)
    out = OUT / f"{name}.mp4"
    p = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{frame.w}x{frame.h}", "-r", str(fps), "-i", "-",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(out)],
        stdin=subprocess.PIPE)
    for i in range(n):
        im = frames_fn(i)
        if i == n // 2:
            im.save(out.with_suffix(".jpg"), quality=90)
        p.stdin.write(np.asarray(im.convert("RGB")).tobytes())
    p.stdin.close()
    p.wait()
    print(f"  {out}")


def photo(path, frame, **kw):
    from video_automation.crypto.shots import PhotoShot
    aspect = 1.15 if frame is VERTICAL else 1.78
    return PhotoShot(path, 1.12, (0.0, 0.0), aspect, frame=frame,
                     logo_box=(60, 40, 300, 90), **kw)


def demo_parallax():
    flat, deep = photo(SKYLINE, LANDSCAPE), photo(SKYLINE, LANDSCAPE, parallax=1.0)

    def fr(i):
        f = i / 149
        a, b = np.asarray(flat.draw(f)), np.asarray(deep.draw(f))
        w = LANDSCAPE.w
        half = np.concatenate([a[:, w // 4: 3 * w // 4], b[:, w // 4: 3 * w // 4]], 1)
        return Image.fromarray(np.ascontiguousarray(half))
    write("parallax-vs-flat", fr, 150, LANDSCAPE)    # left flat, right depth


def demo_isolate():
    s = photo(DUROV, LANDSCAPE, isolate=1.0)
    write("isolate", lambda i: s.draw(i / 149), 150, LANDSCAPE)


def demo_pop():
    s = photo(VITALIK, VERTICAL, pop=True)
    write("pop", lambda i: s.draw(i / 149), 150, VERTICAL)


def demo_behind():
    from video_automation.longform.beats import BEATS
    for name, img, word, line, frame in (
            ("behind-16x9", VITALIK, "Ethereum", "The world computer", LANDSCAPE),
            ("behind-9x16", SAYLOR, "Billions", "Bought with borrowed money", VERTICAL)):
        b = BEATS["behind"](img, word, line, brand=CRYPTO, frame=frame,
                            reveals=[0.4, 2.2], start=0.0, hold=5.0)
        write(name, lambda i, b=b: b.draw(i / 149), 150, frame)


def demo_pile():
    from video_automation.longform.beats import BEATS
    for name, frame in (("pile-16x9", LANDSCAPE), ("pile-9x16", VERTICAL)):
        b = BEATS["pile"]([(30, "Buyers pay in", "$"), (30, "More buyers", "$")],
                          "WHERE THE MONEY GOES", "Liquidity pulled", brand=CRYPTO,
                          frame=frame, reveals=[0.6, 2.6, 5.2], start=0.0, hold=8.0)
        write(name, lambda i, b=b: b.draw(i / 239), 240, frame)


def demo_emoji():
    from video_automation.core import emoji_anim
    from video_automation.longform.beats import BEATS
    items = [("A hot wallet", "online, signs fast", "🔥"),
             ("A hardware wallet", "offline, signs slow", "🔒"),
             ("Your seed phrase", "the key to both", "🔑")]
    b = BEATS["grid"](items, "WHERE THE KEYS LIVE", brand=CRYPTO, frame=LANDSCAPE,
                      reveals=[0.2, 0.5, 0.8], start=0.0, hold=4.0)
    with emoji_anim.enabled(True):
        write("emoji-grid",    # fire and lock animate; the key has none
              lambda i: b.draw(i / 119), 120, LANDSCAPE)


def demo_shaders():
    from video_automation.core import shaderfx
    from video_automation.longform.beats import BEATS
    card = BEATS["chapter"]("HOW THE WORDS ARE MADE", None, None, None, "THE CATCH",
                            brand=CRYPTO, frame=LANDSCAPE, start=0.0, hold=4.0)
    sky, face = photo(SKYLINE, LANDSCAPE), photo(VITALIK, LANDSCAPE)
    for name, shot, spec in (("shader-bloom", card, "bloom"),
                             ("shader-leak", sky, "leak"),
                             ("shader-aberration", face, "aberration"),
                             ("shader-vignette", sky, "vignette")):
        write(name, lambda i, s=shot, sp=spec: shaderfx.apply(
            s.draw(i / 119), sp, i / 30.0), 120, LANDSCAPE)


def demo_screencap():
    from video_automation.core import screencap
    post = Path.home() / "Coding/crypto-wiki/content/posts/what-is-a-seed-phrase.mdx"
    body = post.read_text().split("---", 2)[2]
    parts, n = [], 0
    for block in re.split(r"\n\s*\n", body):
        b = block.strip()
        if not b or b.startswith("<"):
            continue
        b = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", html.escape(b)).replace("**", "")
        if b.startswith("## "):
            parts.append(f"<h2>{b[3:].splitlines()[0]}</h2>")
            b = "\n".join(b.splitlines()[1:])
        if b:
            n += 1
            parts.append(f'<p id="p{n}">{b}</p>')
    page = OUT / "seed-phrase.html"
    OUT.mkdir(parents=True, exist_ok=True)
    page.write_text(
        "<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width'>"
        "<style>body{margin:0;background:#171717;color:#e8e8e8;font:18px/1.65 sans-serif}"
        "main{max-width:760px;margin:0 auto;padding:24px 28px 80px}h2{color:#e5c200}</style>"
        f"<main><h1>What Is a Seed Phrase?</h1>{''.join(parts)}</main>")
    old = screencap.CAPTURES
    screencap.CAPTURES = OUT / "captures"     # a demo is not a committed record
    try:
        for name, mobile, frame in (("screencap-16x9", False, LANDSCAPE),
                                    ("screencap-9x16", True, VERTICAL)):
            cap = screencap.grab(page.as_uri(), name, {"words": "#p4", "odds": "#p7"},
                                 mobile=mobile)
            out = OUT / f"{name}.mp4"
            screencap.clip(cap, out, ["top", "words", "odds"], 9.0, frame,
                           ring=["words", "odds"])
            print(f"  {out}")
    finally:
        screencap.CAPTURES = old


DEMOS = {n[5:]: f for n, f in globals().items() if n.startswith("demo_")}


def main() -> int:
    want = sys.argv[1:] or list(DEMOS)
    failed = 0
    for name in want:
        print(name)
        try:
            DEMOS[name]()
        except Exception as e:          # noqa: BLE001 - report and carry on
            failed += 1
            print(f"  ! skipped: {type(e).__name__}: {e}")
            if "-v" in sys.argv:
                traceback.print_exc()
    print(f"\n{OUT}  ({len(want) - failed} of {len(want)} rendered)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
