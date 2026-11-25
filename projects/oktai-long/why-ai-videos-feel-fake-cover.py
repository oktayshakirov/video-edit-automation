"""The cover of "My 89 AI Videos Were Slop. Here's What Fixed Them." -
a before/after split (the concept agreed 2026-11-23, picked again
2026-11-25): the slop on the left, drained of colour under a red cross;
the fix on the right, bright, under a green tick; his cut-out between them,
looking at the slop with a wince (his photo, 2026-11-25); a short line on
top.

    PYTHONPATH=. .venv/bin/python projects/oktai-long/why-ai-videos-feel-fake-cover.py

Writes one cover per text option to `~/Desktop/<name>-cover-<n>.jpg` and a
sheet of all of them, for his pick. The panels are drawn from the video's
own pieces at full size: the stock clip with its big label (the slop he
made) and the voice waveforms (what he made instead).
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from video_automation.core.brand import OKTAI  # noqa: E402
from video_automation.core.frame import LANDSCAPE  # noqa: E402
from video_automation.crypto.shots import Shot  # noqa: E402
from video_automation.longform.beats import make_beat  # noqa: E402
from video_automation.longform.thumb import SAFE_BOTTOM, SAFE_TOP, stack_headline  # noqa: E402
from video_automation.oktai import folder  # noqa: E402

W, H = 1280, 720
RED, GREEN = (235, 64, 52), (74, 200, 120)
# His pick (2026-11-25): "I made AI slop", AI SLOP on the red plate, the
# line behind his head for depth. The panels: one clean subject each, the
# marks the same size in mirrored places ("those ones are bad, messy ... the
# red and green mark being different sizes and in different positions").
TEXT = "I MADE [AI SLOP]"
# (name, before, after): the slop shot and what replaced it.
# Then (2026-11-25): "the robot doesn't have to do anything with AI slop if
# you haven't watched the video, and the waveform without context means
# nothing - bad and good examples easy to understand without context". The
# bad is the faceless-channel look everyone knows: a stock clip under a giant
# clickbait caption and a robot voice; the good is a clean, specific
# explainer graphic from one of our real videos - on the same topic.
# His pick for the good card (2026-11-25): the Squid Game video's own cover,
# "only 1 winner" - a real, finished thumbnail of ours.
PAIRS = [("ai-chain", "slop", "aichain"), ("squid", "slop", "squid")]


def _long():
    p = Path(__file__).with_name("why-ai-videos-feel-fake.py")
    spec = importlib.util.spec_from_file_location("long", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _frame(shot: Shot, hold: float = 3.0, at: float = 0.8, reveals=None) -> Image.Image:
    shot.start, shot.hold = 0.0, hold
    shot.reveals = reveals
    beat = make_beat(shot, OKTAI, LANDSCAPE)
    return beat.draw(at).convert("RGB")


def _cover(img: Image.Image, w: int, h: int, ax: float = 0.5) -> Image.Image:
    k = max(w / img.width, h / img.height)
    im = img.resize((int(img.width * k) + 1, int(img.height * k) + 1), Image.LANCZOS)
    x = int((im.width - w) * ax)
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def _before(panel: Image.Image) -> Image.Image:
    """Drained of colour with a little red: the slop."""
    a = np.asarray(panel).astype(np.float32)
    grey = a.mean(axis=2, keepdims=True)
    a = grey * 0.70 + np.array(RED, np.float32) * 0.10
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def _after(panel: Image.Image) -> Image.Image:
    a = np.asarray(panel).astype(np.float32) * 1.3 + 6
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def _badge(base: Image.Image, cx: int, cy: int, ok: bool, r: int = 50) -> None:
    """A round mark: red with a cross, or green with a tick - one size, one
    stroke, so the two read as a pair."""
    ss = 4
    lay = Image.new("RGBA", (r * 2 * ss + 8, r * 2 * ss + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    c = (r * ss + 4, r * ss + 4)
    R = r * ss
    d.ellipse([c[0] - R, c[1] - R, c[0] + R, c[1] + R], fill=(*(GREEN if ok else RED), 255),
              outline=(255, 255, 255, 255), width=int(R * 0.09))
    w = int(R * 0.16)
    if ok:
        pts = [(c[0] - R * 0.42, c[1] + R * 0.02), (c[0] - R * 0.10, c[1] + R * 0.34),
               (c[0] + R * 0.46, c[1] - R * 0.30)]
        d.line(pts, fill="white", width=w, joint="curve")
        ends = (pts[0], pts[-1])
    else:
        k = R * 0.36
        d.line([(c[0] - k, c[1] - k), (c[0] + k, c[1] + k)], fill="white", width=w)
        d.line([(c[0] + k, c[1] - k), (c[0] - k, c[1] + k)], fill="white", width=w)
        ends = ((c[0] - k, c[1] - k), (c[0] + k, c[1] + k), (c[0] + k, c[1] - k), (c[0] - k, c[1] + k))
    for x, y in ends:
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill="white")
    lay = lay.resize((lay.width // ss, lay.height // ss), Image.LANCZOS)
    sh = Image.new("RGBA", lay.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 150), (0, 0), lay.getchannel("A"))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    base.paste(sh, (cx - lay.width // 2 + 3, cy - lay.height // 2 + 5), sh)
    base.paste(lay, (cx - lay.width // 2, cy - lay.height // 2), lay)


def panels(L) -> dict:
    """The candidate halves, drawn at full size from the video's pieces."""
    robot = _frame(Shot(clip=L.ROBOT), at=0.8)
    coin = _frame(Shot(clip=L.COIN), at=0.8)
    wave = _frame(Shot(graphic="voice", ground="grid", payload=(L.VOICES[1:2],)),
                  hold=8.0, at=0.9, reveals=[0.2])
    wave = wave.crop((760, 300, 1880, 780))              # the strip alone
    bars = _frame(Shot(graphic="bars", payload=([("Slower", 151 / 192, "151 a minute"),
                                                 ("Faster", 1.0, "192 a minute")],
                                                "WORDS PER MINUTE")),
                  hold=4.0, at=0.95, reveals=[0.2, 1.0])
    from video_automation.core.vertical import emoji_image
    from video_automation.longform.beats.base import _display
    slop = coin.copy()
    d = ImageDraw.Draw(slop)
    f = _display(190)
    for i, ln in enumerate(["THIS WILL", "SHOCK YOU"]):
        tw = d.textlength(ln, font=f)
        d.text(((slop.width - tw) / 2, 330 + i * 215), ln, font=f, fill=(255, 228, 0),
               stroke_width=16, stroke_fill=(0, 0, 0))
    em = emoji_image("\U0001F631", 230)
    slop.paste(em, (slop.width - 330, 90), em)
    pill = _display(64)
    d.rounded_rectangle([70, 90, 640, 200], radius=55, fill=(20, 20, 24))
    d.text((140, 108), "AI VOICE", font=pill, fill=(255, 255, 255))
    bot = emoji_image("\U0001F916", 80)
    slop.paste(bot, (540, 105), bot)
    relay = _frame(Shot(graphic="relay", payload=L.SHIPPED["relay"]), hold=6.0, at=0.98,
                   reveals=[0.3, 1.0, 1.8, 2.6])
    breach = _frame(Shot(graphic="breach", payload=L.SHIPPED["breach"]), hold=6.0, at=0.98,
                    reveals=[0.3, 1.2, 2.2])
    squid = Image.open(folder(L.NAME) / "cover" / "squid-game.jpg").convert("RGB")
    aichain = Image.open(folder(L.NAME) / "cover" / "ai-blockchain.jpg").convert("RGB")
    return {"aichain": (aichain, 0.5), "squid": (squid, 0.5), "slop": (slop, 0.5), "relay": (relay, 0.5), "breach": (breach, 0.5),
            "robot": (robot, 0.5), "coin": (coin, 0.48), "wave": (wave, 0.5),
            "bars": (bars.crop((60, 300, 1860, 900)), 0.5)}


def _card(img: Image.Image, w: int, h: int, ax: float = 0.5) -> Image.Image:
    """A whole picture as a rounded card with a thin white rim."""
    im = _cover(img, w, h, ax).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], radius=int(h * 0.06), fill=255)
    im.putalpha(m)
    ImageDraw.Draw(im).rounded_rectangle([1, 1, w - 2, h - 2], radius=int(h * 0.06),
                                         outline=(255, 255, 255, 230), width=4)
    return im


def _shadowed(base: Image.Image, im: Image.Image, xy: tuple) -> None:
    sh = Image.new("RGBA", (im.width + 60, im.height + 60), (0, 0, 0, 0))
    sh.paste((0, 0, 0, 190), (30, 30), im.getchannel("A"))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    base.paste(sh, (xy[0] - 30 + 6, xy[1] - 30 + 10), sh)
    base.paste(im, xy, im)


def build(out: Path, before, after, face: Image.Image, text: str = TEXT) -> Path:
    base = Image.new("RGB", (W, H), OKTAI.bg)
    # A faint grid, the channel's ground.
    g = ImageDraw.Draw(base)
    for x in range(0, W, 48):
        g.line([(x, 0), (x, H)], fill=(24, 26, 36))
    for y in range(0, H, 48):
        g.line([(0, y), (W, y)], fill=(24, 26, 36))

    box = stack_headline(base, [text], (30, 14, W - 60, 150), max_size=140, weight=900)

    # The two cards, whole, either side of his head; tilted a touch inward.
    cw, ch = 450, 253
    left = _card(before[0], cw, ch, before[1]).rotate(4, resample=Image.BICUBIC, expand=True)
    right = _card(after[0], cw, ch, after[1]).rotate(-4, resample=Image.BICUBIC, expand=True)
    ly = int(box[3]) + 40
    _shadowed(base, left, (22, ly))
    _shadowed(base, right, (W - right.width - 22, ly))
    _badge(base, 22 + 40, ly + left.height - 40, ok=False, r=44)
    _badge(base, W - 22 - 40, ly + right.height - 40, ok=True, r=44)

    # Him in the middle, his head breaking into the line.
    fh = int(H * 0.80)
    f = face.resize((int(face.width * fh / face.height), fh), Image.LANCZOS)
    glow = Image.new("RGBA", (f.width + 80, f.height + 80), (0, 0, 0, 0))
    glow.paste((0, 0, 0, 255), (40, 40), f.getchannel("A"))
    glow = glow.filter(ImageFilter.GaussianBlur(22))
    # His head, not the cut-out's box, centred between the cards: in this
    # photo the head sits at 60 % of the width ("move my body slightly to the
    # left so I'm between both cards with my head").
    a = np.asarray(f.getchannel("A"))
    ys, xs = np.nonzero(a[: int(a.shape[0] * 0.35)] > 128)
    fx = W // 2 - int(xs.mean())
    fy = max(int(box[3]) - 30, H - f.height + 8)
    base.paste(glow, (fx - 40, fy - 30), glow)
    base.paste(f, (fx, fy), f)
    base.save(out, quality=92)
    return out


def main() -> None:
    L = _long()
    # His photo came already cut out, with its own soft alpha: used as it is
    # (re-matting it on black made jagged hair - "the cutout is very bad"),
    # its edge softened, the pure red and yellow streaks in it repainted
    # (2026-11-25).
    face = Image.open(folder(L.NAME) / "cover" / "oktay-cutout-soft.png").convert("RGBA")
    P = panels(L)
    desk = Path.home() / "Desktop"
    outs = [build(desk / f"{L.NAME}-cover-{name}.jpg", P[b], P[a], face) for name, b, a in PAIRS]
    sheet = Image.new("RGB", (W, (H // 2) * -(-len(outs) // 2)), (30, 30, 30))
    for i, p in enumerate(outs):
        im = Image.open(p).resize((W // 2, H // 2))
        sheet.paste(im, ((i % 2) * (W // 2), (i // 2) * (H // 2)))
    sheet.save(desk / f"{L.NAME}-covers.jpg", quality=88)
    print(desk / f"{L.NAME}-covers.jpg")




# --- the Shorts' covers (2026-11-25: "we also need thumbnails for the shorts")
# The long cover's look, standing up: what the Short is about on top, its
# picture as a card with the red cross, him under it looking up at it.
# TikTok's profile grid shows a 9:16 cover cropped to 3:4 (the editor,
# 2026-11-25: "we dont crop the text and important graphics"), so the
# headline, the card and his head sit inside the centre 1080x1440 band.
SW, SH = 1080, 1920
SAFE = (SAFE_TOP, SAFE_BOTTOM)  # (240, 1680), from longform.thumb
SHORTS = {
    "": (["I MADE", "[AI SLOP]"], "slop"),
    "picture": (["MISTAKE 1", "[STOCK CLIPS]"], "GENERIC"),
    "music": (["MISTAKE 2", "[THE MUSIC]"], "EQUALIZER"),
    "first-seconds": (["MISTAKE 3", "[THE 2ND LINE]"], "STOPWATCH"),
    "template": (["MISTAKE 4", "[ONE TEMPLATE]"], "COPY"),
    "voice": (["MISTAKE 5", "[ROBOT VOICE]"], "ROBOT"),
}


def build_short(out: Path, rows: list[str], card_img: Image.Image, face: Image.Image) -> Path:
    base = Image.new("RGB", (SW, SH), OKTAI.bg)
    g = ImageDraw.Draw(base)
    for x in range(0, SW, 54):
        g.line([(x, 0), (x, SH)], fill=(24, 26, 36))
    for y in range(0, SH, 54):
        g.line([(0, y), (SW, y)], fill=(24, 26, 36))
    box = stack_headline(base, rows, (60, SAFE[0] + 30, SW - 120, 300), max_size=160, weight=900)
    cw, ch = 820, 461
    card = _card(card_img, cw, ch).rotate(-3, resample=Image.BICUBIC, expand=True)
    cy = int(box[3]) + 45
    _shadowed(base, card, ((SW - card.width) // 2, cy))
    _badge(base, (SW - card.width) // 2 + 70, cy + card.height - 70, ok=False, r=64)
    fh = int(SH * 0.44)
    f = face.resize((int(face.width * fh / face.height), fh), Image.LANCZOS)
    a = np.asarray(f.getchannel("A"))
    ys, xs = np.nonzero(a[: int(a.shape[0] * 0.35)] > 128)
    fx = SW // 2 - int(xs.mean())
    fy = SH - f.height + 10
    glow = Image.new("RGBA", (f.width + 80, f.height + 80), (0, 0, 0, 0))
    glow.paste((0, 0, 0, 255), (40, 40), f.getchannel("A"))
    glow = glow.filter(ImageFilter.GaussianBlur(26))
    base.paste(glow, (fx - 40, fy - 30), glow)
    base.paste(f, (fx, fy), f)
    base.save(out, quality=92)
    return out


def shorts_main() -> None:
    L = _long()
    face = Image.open(folder(L.NAME) / "cover" / "oktay-cutout-soft.png").convert("RGBA")
    P = panels(L)
    desk = Path.home() / "Desktop"
    made = []
    for tag, (rows, src) in SHORTS.items():
        img = P[src][0] if src in P else _frame(Shot(clip=getattr(L, src)), at=0.6)
        name = f"{L.NAME}-short{'-' + tag if tag else ''}-cover.jpg"
        made.append(build_short(desk / name, rows, img, face))
    sheet = Image.new("RGB", (SW // 4 * len(made), SH // 4), (30, 30, 30))
    for i, p in enumerate(made):
        sheet.paste(Image.open(p).resize((SW // 4, SH // 4)), (i * SW // 4, 0))
    g = ImageDraw.Draw(sheet)
    for i in range(len(made)):  # TikTok's 3:4 grid crop, to check nothing is cut
        x0 = i * SW // 4
        for y in SAFE:
            g.line([(x0, y // 4), (x0 + SW // 4, y // 4)], fill=(0, 220, 255), width=2)
    sheet.save(desk / f"{L.NAME}-short-covers.jpg", quality=88)
    print(desk / f"{L.NAME}-short-covers.jpg")


if __name__ == "__main__":
    shorts_main() if "--shorts" in sys.argv else main()
