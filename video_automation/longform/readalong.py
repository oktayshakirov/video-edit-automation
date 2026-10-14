"""A read-along: audio that already exists, a still, and karaoke captions.

The third long-form shape, after the explainer (`build.py`) and the sound
session (`asmr.py`). Both of those synthesise their own narration, and
`render_long` cannot be pointed at a finished track: its timeline *is* the
synthesis - `build_narration_aligned` returns the audio, the caption spans and
the total in one call, and every beat is laid out from those. Audio rendered
somewhere else (the audiobook, in the sibling `audio-book-automation` repo)
has none of that, so it gets its own path rather than a flag on that one.

**Timing comes from the audio, not from the script.** Two stages:

1. **Paragraphs, from the silences.** The audiobook is built one synthesiser
   call per paragraph with fixed gaps between them, so the paragraph
   boundaries are real silences of known length. Kokoro also leaves pauses of
   its own *inside* a paragraph, some as long as the shortest scripted gap
   (measured on the Shut Up, Tinnitus sample: 65 silences over 0.4s for 47
   boundaries), so a threshold cannot tell them apart. `find_parts` picks the
   boundaries with a small DP instead, scoring each candidate on how close its
   length is to the scripted gap and how well the paragraph lengths it implies
   match the text.
2. **Phrases, by DTW inside each paragraph.** `align_chunks`, the same aligner
   the narrated builds use: each phrase synthesised alone as a reference,
   warped onto the real read. It needs the same voice and roughly the same
   speed on both sides, which holds because the audiobook is Kokoro too.

Words inside a phrase are apportioned the way the shorts' karaoke does it -
see `crypto.build._word_spans`.

**The picture is not rendered frame by frame.** Eight minutes is 15,000
frames, and nothing moves except which word is lit. Each caption state is one
PNG of the panel; ffmpeg's concat demuxer holds each for its duration and
overlays the stream on the still.
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..core.brand import Brand
from ..core.frame import LANDSCAPE, Frame
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX, render_caption_karaoke
from ..core.voiceover import (KOKORO_SR, Caption, align_chunks,
                              caption_window, split_phrases)
from ..crypto.build import _word_spans
from .meta import Meta, write_srt

FONT_FUTURA_BOLD = 2            # index into Futura.ttc

# Quiet-run detection. A run below SILENCE_DB (relative to the track's peak)
# lasting MIN_RUN or more is a boundary candidate; `find_parts` decides which.
HOP = 240                       # 10ms at KOKORO_SR
SILENCE_DB = -45.0
MIN_RUN = 0.30

# The audiobook trims each paragraph to TRIM_PAD (0.04s) of its own onset and
# decay, so a scripted gap measures this much longer than it was scripted.
PAD = 0.08

# DP weights. A gap that is 0.1s off its script costs the same as a paragraph
# whose length is ~20% off what its text predicts; the gap is the stronger
# evidence, since the scripted values (0.55, 1.0, 1.3) are far apart and the
# measured ones land within ~0.06 of them.
W_GAP = 10.0
W_LEN = 5.0


@dataclass
class Part:
    """One synthesiser call's worth of text: a title line or a paragraph.

    `gap` is the silence scripted *before* it. `chapter` names a chapter that
    starts here, for the description's timestamps and the panel's heading.
    """
    text: str
    gap: float
    chapter: str | None = None


def _quiet_runs(y: np.ndarray) -> list[tuple[float, float]]:
    import librosa
    rms = librosa.feature.rms(y=y, frame_length=2 * HOP, hop_length=HOP)[0]
    db = 20 * np.log10(rms / max(float(rms.max()), 1e-9) + 1e-9)
    quiet = db < SILENCE_DB
    runs, i, n = [], 0, len(quiet)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            a, b = i * HOP / KOKORO_SR, j * HOP / KOKORO_SR
            if b - a >= MIN_RUN or i == 0 or j == n:
                runs.append((a, b))
            i = j
        else:
            i += 1
    return runs


def find_parts(y: np.ndarray, parts: list[Part],
               tail: float) -> list[tuple[float, float]]:
    """`(start, end)` of each part's speech in `y`, chosen by DP.

    `tail` is the silence scripted after the last part. The track must begin
    and end on silence (the audiobook's lead and tail guarantee it).
    """
    runs = _quiet_runs(y)
    if not runs or runs[0][0] > 0.05:
        raise ValueError("audio does not start on silence")
    total = len(y) / KOKORO_SR
    n, k = len(runs), len(parts)

    # Lengths implied by character count, scaled so they sum to the speech.
    chars = np.array([len(p.text) + 8 for p in parts], dtype=float)
    speech = total - sum(p.gap for p in parts) - tail
    expect = chars / chars.sum() * speech

    def gap_cost(r, want):
        a, b = runs[r]
        # The first and last runs are the track's lead and tail; they are
        # bounded by the file, not by trimming, so no pad.
        pad = 0.0 if r in (0, n - 1) else PAD
        return W_GAP * abs((b - a) - (want + pad))

    inf = math.inf
    # cost[i][r]: best cost with part i ending at run r (its speech stops where
    # run r begins). Part i starts where the run chosen for part i-1 ends.
    cost = [[inf] * n for _ in range(k)]
    back = [[-1] * n for _ in range(k)]
    for r in range(1, n):
        c = gap_cost(0, parts[0].gap)
        seg = runs[r][0] - runs[0][1]
        if seg > 0:
            cost[0][r] = c + W_LEN * abs(math.log(seg / expect[0]))
    for i in range(1, k):
        for r in range(i + 1, n):
            best, arg = inf, -1
            for q in range(i, r):
                if cost[i - 1][q] == inf:
                    continue
                seg = runs[r][0] - runs[q][1]
                if seg <= 0:
                    continue
                c = (cost[i - 1][q] + gap_cost(q, parts[i].gap)
                     + W_LEN * abs(math.log(seg / expect[i])))
                if c < best:
                    best, arg = c, q
            cost[i][r], back[i][r] = best, arg
    # The last part must end on the final run, the tail.
    end = n - 1
    if cost[k - 1][end] == inf:
        raise ValueError("no segmentation found - check the parts list")
    chosen = [end]
    for i in range(k - 1, 0, -1):
        chosen.append(back[i][chosen[-1]])
    chosen.reverse()
    spans, prev = [], 0
    for r in chosen:
        spans.append((runs[prev][1], runs[r][0]))
        prev = r
    return spans


def align(audio: Path, parts: list[Part], workdir: Path, voice,
          speed: float, tail: float,
          spoken: Callable[[str], str] = lambda s: s,
          max_words: int = 7) -> tuple[list[Caption], list[tuple[float, str]],
                                       float]:
    """Captions, chapters and total runtime for `audio`.

    Cached in `workdir` against the audio's size and mtime and the text, since
    the alignment is the slow part (one synthesis per phrase) and the picture
    is what gets iterated on.
    """
    import librosa
    workdir.mkdir(parents=True, exist_ok=True)
    st = audio.stat()
    key = json.dumps([str(audio), st.st_size, st.st_mtime, speed, max_words,
                      [(p.text, p.gap, p.chapter) for p in parts]])
    cache = workdir / "align.json"
    if cache.exists():
        got = json.loads(cache.read_text())
        if got.get("key") == key:
            caps = [Caption(**c) for c in got["captions"]]
            return caps, [tuple(c) for c in got["chapters"]], got["total"]

    y, _ = librosa.load(str(audio), sr=KOKORO_SR, mono=True)
    total = len(y) / KOKORO_SR
    spans = find_parts(y, parts, tail)

    caps: list[Caption] = []
    chapters: list[tuple[float, str]] = []
    for part, (a, b) in zip(parts, spans):
        if part.chapter:
            chapters.append((a, part.chapter))
        chunks = split_phrases(part.text, max_words=max_words)
        seg = y[int(a * KOKORO_SR):int(b * KOKORO_SR)]
        ends = align_chunks(seg, [spoken(c) for c in chunks], voice,
                            speed=speed)
        t = 0.0
        for text, e in zip(chunks, ends):
            caps.append(Caption(text, a + t, a + e))
            t = e
    if chapters:
        chapters[0] = (0.0, chapters[0][1])

    cache.write_text(json.dumps({
        "key": key, "total": total, "chapters": chapters,
        "captions": [vars(c) for c in caps]}))
    return caps, chapters, total


# --- picture -------------------------------------------------------------

@dataclass
class Layout:
    """Where things go on a 16:9 frame with a square still on the left."""
    frame: Frame = LANDSCAPE
    bg: tuple[int, int, int] = (0, 0, 0)
    caption_size: int = 60
    caption_y: float = 0.47          # of the panel's height
    caption_max_w: int = 700

    @property
    def still(self) -> int:
        return self.frame.h            # the still is square, full height

    @property
    def panel(self) -> Frame:
        f = self.frame
        return Frame(name="panel", w=f.w - self.still, h=f.h, safe_top=0,
                     safe_bottom=0, safe_right=0,
                     caption_floor=self.caption_y, logo_at=(0, 0), logo_w=0,
                     max_upscale=1.0)


def _font(size: int, index: int = FONT_CAPTION_INDEX):
    return ImageFont.truetype(FONT_CAPTION, size, index=index)


def _spaced(d: ImageDraw.ImageDraw, xy, text: str, font, fill,
            tracking: float, anchor_center: bool = True) -> None:
    """Letter-spaced small caps line, centred on `xy[0]`."""
    widths = [d.textlength(ch, font=font) for ch in text]
    w = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - w / 2 if anchor_center else xy[0]
    for ch, cw in zip(text, widths):
        d.text((x, xy[1]), ch, font=font, fill=fill)
        x += cw + tracking


def base_frame(still: Path, layout: Layout) -> Image.Image:
    f = layout.frame
    sq = Image.open(still).convert("RGB").resize(
        (layout.still, layout.still), Image.LANCZOS)
    img = Image.new("RGB", f.size, layout.bg)
    img.paste(panel_ground(sq, layout), (layout.still, 0))
    img.paste(sq, (0, 0))
    return img


def panel_ground(sq: Image.Image, layout: Layout) -> Image.Image:
    """The still's own right edge, stretched across the panel.

    A flat fill shows a seam: covers are rarely a true black, and this one
    carries a vignette that is lighter at mid-height. Averaging the last few
    columns and stretching them keeps that vertical gradient continuous.
    """
    edge = sq.crop((sq.width - 6, 0, sq.width, sq.height)).resize(
        (1, sq.height), Image.BOX)
    return edge.resize(layout.panel.size, Image.NEAREST)


def panel_base(ground: Image.Image, layout: Layout, brand: Brand,
               eyebrow: str, heading: str | None, badges: list[Path],
               footer: str) -> Image.Image:
    """The panel's fixed type: eyebrow, chapter heading, the badge row.

    A heading with a colon is set as a label over a title ("Chapter 1" /
    "Beethoven's Letter from Vienna"); wrapped as one run it left a single
    word on the second line.
    """
    p = layout.panel
    img = ground.copy()
    d = ImageDraw.Draw(img)
    cx = p.w // 2

    _spaced(d, (cx, 118), eyebrow.upper(), _font(26, FONT_FUTURA_BOLD),
            brand.primary, tracking=5)
    if heading:
        label, _, title = heading.rpartition(": ")
        y = 166
        if label:
            f = _font(30)
            w = d.textlength(label, font=f)
            d.text((cx - w / 2, y), label, font=f, fill=(150, 150, 150))
            y += 44
        f = _font(40)
        for ln in _wrap(d, title, f, layout.caption_max_w):
            w = d.textlength(ln, font=f)
            d.text((cx - w / 2, y), ln, font=f, fill=(215, 215, 215))
            y += 52
    # A hairline under the heading block, so the caption has a top edge.
    d.line([(cx - 60, 300), (cx + 60, 300)], fill=brand.primary, width=2)

    if badges:
        h = 64
        imgs = []
        for b in badges:
            im = Image.open(b).convert("RGBA")
            imgs.append(im.resize((round(im.width * h / im.height), h),
                                  Image.LANCZOS))
        gap = 24
        w = sum(i.width for i in imgs) + gap * (len(imgs) - 1)
        x, y = cx - w // 2, p.h - 214
        for im in imgs:
            img.paste(im, (x, y), im)
            x += im.width + gap
        f = _font(26)
        tw = d.textlength(footer, font=f)
        d.text((cx - tw / 2, y - 52), footer, font=f, fill=(170, 170, 170))
    return img


def _wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if cur and d.textlength(t, font=font) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


def _states(captions: list[Caption], total: float
            ) -> list[tuple[float, float, int, int]]:
    """`(start, end, caption, word)` for every lit word. The last word stays
    lit until the line clears, as in the shorts."""
    out = []
    for i, c in enumerate(captions):
        cs, ce = caption_window(c)
        ce = min(ce, captions[i + 1].start if i + 1 < len(captions) else total)
        for k, (a, b) in enumerate(_word_spans(c.text, cs, ce, c.speech_end)):
            out.append((a, min(b, ce), i, k))
    return out


def render_readalong(audio: Path, still: Path, captions: list[Caption],
                     chapters: list[tuple[float, str]], total: float,
                     out: Path, workdir: Path, brand: Brand,
                     eyebrow: str = "Audiobook sample",
                     badges: list[Path] = (),
                     footer: str = "The full audiobook",
                     meta: Meta | None = None,
                     thumb: Path | None = None,
                     lufs: float | None = -16.0,
                     layout: Layout | None = None, fps: int = 30,
                     keep_work: bool = False) -> dict:
    """The MP4, its SRT, and the sidecar if `meta` is given.

    `lufs` lifts the track to the channel's loudness with a peak limiter in
    front of it. The audiobook is mastered to -20 LUFS for the retailers, and
    YouTube only ever turns a loud video *down*, so left alone it plays 4 dB
    under every other video on the channel. A static gain, not `loudnorm`'s
    dynamic mode, so the read's own dynamics are untouched. None leaves the
    audio exactly as delivered.
    """
    layout = layout or Layout()
    workdir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    frames = workdir / "panel"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir()

    base = base_frame(still, layout)
    base_png = workdir / "base.png"
    base.save(base_png)

    # One panel background per chapter.
    heads = sorted(chapters) or [(0.0, None)]
    ground = base.crop((layout.still, 0, layout.frame.w, layout.frame.h))
    bgs = [panel_base(ground, layout, brand, eyebrow, h, list(badges), footer)
           for _, h in heads]

    def bg_at(t):
        return max((j for j, (s, _) in enumerate(heads) if s <= t + 1e-6),
                   default=0)

    accent = (*brand.primary, 255)
    p = layout.panel
    seq: list[tuple[Path, float]] = []
    blank_paths: dict[int, Path] = {}

    def blank(i):
        if i not in blank_paths:
            bp = frames / f"blank{i}.png"
            bgs[i].save(bp)
            blank_paths[i] = bp
        return blank_paths[i]

    t = 0.0
    tmp = workdir / "kar.png"
    for n, (a, b, ci, k) in enumerate(_states(captions, total)):
        if b <= a:
            continue
        if a > t + 1e-3:
            seq.append((blank(bg_at(t)), a - t))
        i = bg_at(a)
        render_caption_karaoke(captions[ci].text, tmp, active=k,
                               size=layout.caption_size,
                               font_path=FONT_CAPTION,
                               font_index=FONT_CAPTION_INDEX,
                               y_frac=layout.caption_y, stroke=0,
                               max_w=layout.caption_max_w, frame=p,
                               accent=accent)
        im = bgs[i].copy()
        layer = Image.open(tmp)
        im.paste(layer, (0, 0), layer)
        fp = frames / f"s{n:05d}.png"
        im.save(fp)
        seq.append((fp, b - a))
        t = b
    if t < total:
        seq.append((blank(bg_at(t)), total - t))

    lst = workdir / "panel.txt"
    body = []
    for fp, d in seq:
        body += [f"file '{fp.resolve()}'", f"duration {d:.4f}"]
    body.append(f"file '{seq[-1][0].resolve()}'")   # concat's last-entry rule
    lst.write_text("\n".join(body) + "\n")

    af = []
    if lufs is not None:
        gain = lufs - _integrated(audio)
        af = ["-af", f"volume={gain:.2f}dB,alimiter=limit=0.891:level=0"]

    subprocess.run(
        ["ffmpeg", "-v", "error", "-y",
         "-loop", "1", "-framerate", str(fps), "-i", str(base_png),
         "-f", "concat", "-safe", "0", "-i", str(lst),
         "-i", str(audio),
         "-filter_complex",
         f"[1:v]fps={fps},format=rgb24[p];"
         f"[0:v][p]overlay={layout.still}:0:eof_action=repeat,"
         f"format=yuv420p[v]",
         "-map", "[v]", "-map", "2:a", *af,
         "-t", f"{total:.3f}", "-r", str(fps),
         "-c:v", "libx264", "-crf", "18", "-preset", "slow",
         "-tune", "stillimage",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-movflags", "+faststart", str(out)],
        check=True, capture_output=True)

    made = {"video": out, "total": total, "chapters": chapters}
    srt = out.with_suffix(".srt")
    write_srt(captions, srt)
    made["srt"] = srt
    if thumb is not None:
        made["thumb"] = thumb
    if meta is not None:
        sidecar = out.with_suffix(".md")
        meta.write(sidecar, chapters, total, out, srt, thumb)
        made["meta"] = sidecar
    if not keep_work:
        shutil.rmtree(frames, ignore_errors=True)
    return made


def _integrated(audio: Path) -> float:
    """Integrated loudness in LUFS, from ffmpeg's ebur128 summary."""
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(audio),
         "-af", "ebur128", "-f", "null", "-"],
        capture_output=True, text=True, check=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    for line in tail.splitlines():
        line = line.strip()
        if line.startswith("I:"):
            return float(line.split()[1])
    raise RuntimeError("no integrated loudness in ebur128 output")
