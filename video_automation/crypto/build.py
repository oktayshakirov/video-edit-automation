"""Assemble a crypto short: narration, picture track, captions.

Same three-layer order as the tinnitus format — measure the voice first, cut the
picture to it, burn captions last. What differs is that the picture here is a
sequence of the site's own photographs rather than one generated backdrop, so
there is a shot list and it has to line up with the sentences.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..core.vertical import add_caption_emoji, render_text_png
from ..core.voiceover import CAPTION_MAX_W, build_narration_aligned, profile_args
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX
from .shots import OUT_H, PhotoShot, Shot, plan_shots, render_shots


def sentence_spans(sentences: list, captions: list) -> list[tuple[float, float]]:
    """Map each sentence onto the span its captions occupy.

    Captions are held until the next one starts, so a sentence's last caption
    already stretches across the gap that follows it. That is what the picture
    wants too — a shot should carry the pause, not cut away into silence.
    """
    spans, i = [], 0
    for s in sentences:
        chunks = len(s)
        spans.append((captions[i].start, captions[i + chunks - 1].end))
        i += chunks
    return spans


def render_crypto_short(sentences: list, shots: list[Shot], out: Path,
                        workdir: Path, voice: str = "theo",
                        gap: float = 0.34, tail: float = 1.2,
                        font_size: int = 46, y_frac: float = 0.70,
                        emoji: dict[str, str] | None = None,
                        fps: int = 30) -> tuple[Path, float]:
    """One short, end to end.

    Captions sit **under the photograph, not over it**. Every source image is
    landscape, so even cropped it leaves a band of blurred backdrop below — that
    band is where the type belongs, and putting it there stops the caption
    covering the thing it is describing. `y_frac` is only the fallback, used for
    drawn beats and for any shot whose photo runs too low to clear.

    `gap` is tighter than the drone quotes' 0.65. A quote wants air between
    lines; an explainer with a thirty-second budget does not, and the pauses
    are what a viewer scrolls away during.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    track, captions, total = build_narration_aligned(
        [list(s) for s in sentences], workdir, gap=gap, tail=tail,
        **profile_args(voice))

    plan_shots(shots, sentence_spans(sentences, captions))

    # A drawn beat reveals its items on the caption starts of its own sentence,
    # so a line appears exactly as it is spoken. Even fractions of the shot look
    # synced until you watch it, and then every item is a beat early or late.
    # Write the sentence with one caption per item and this needs no tuning.
    first = 0
    for sh, sent in zip(shots, sentences):
        if sh.graphic and sh.reveals is None:
            starts = [captions[first + k].start for k in range(len(sent))]
            n = len(sh.payload[0])
            sh.reveals = (starts + [starts[-1]] * n)[:n]
        first += len(sent)

    # Where each shot's photograph ends, so its captions can sit beneath it.
    # Measured at f=0.5, the middle of the Ken Burns move; the drift over a
    # five-second shot is small next to the margin below.
    below = []
    for sh in shots:
        if sh.image is None:
            below.append(y_frac)
            continue
        _, y, _, h = PhotoShot(sh.image, sh.zoom, sh.pan,
                               sh.aspect, sh.bias).photo_box(0.5)
        caption_y = (y + h + 96) / OUT_H
        below.append(min(max(caption_y, y_frac), 0.80))

    picture = render_shots(workdir / "picture.mp4", shots, total, fps=fps)

    pngs, ci = [], 0
    for si, sent in enumerate(sentences):
        for _ in sent:
            c = captions[ci]
            ci += 1
            if not c.text.strip():
                pngs.append(None)
                continue
            p = workdir / f"cap{len(pngs):02d}.png"
            # bg_luma is irrelevant here: stroke=4 selects the white-ink,
            # black-border treatment, the only one that survives type on a photo.
            render_text_png(c.text, p, size=font_size, bg_luma=0.0,
                            font_path=FONT_CAPTION, font_index=FONT_CAPTION_INDEX,
                            y_frac=below[si], stroke=4, max_w=CAPTION_MAX_W)
            if emoji and c.text in emoji:
                add_caption_emoji(p, c.text, emoji[c.text], font_size,
                                  below[si], FONT_CAPTION, FONT_CAPTION_INDEX)
            pngs.append(p)

    shown = [(i, c) for i, c in enumerate(captions) if pngs[i] is not None]
    chain, prev = [], "[0:v]"
    for n, (i, c) in enumerate(shown):
        dst = f"[v{n+1}]"
        chain.append(f"{prev}[{n+1}:v]overlay=0:0:"
                     f"enable='between(t,{c.start:.3f},{c.end:.3f})'{dst}")
        prev = dst

    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(picture)]
    for i, _ in shown:
        cmd += ["-i", str(pngs[i])]
    cmd += ["-i", str(track)]
    if chain:
        cmd += ["-filter_complex", ";".join(chain), "-map", prev]
    else:
        cmd += ["-map", "0:v"]
    cmd += ["-map", f"{len(shown)+1}:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out, total
