"""Assemble a crypto short: narration, picture track, captions.

Same three-layer order as the tinnitus format — measure the voice first, cut the
picture to it, burn captions last. What differs is that the picture here is a
sequence of the site's own photographs rather than one generated backdrop, so
there is a shot list and it has to line up with the sentences.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..core import sfx
from ..core.frame import VERTICAL, Frame
from ..core.vertical import add_caption_emoji, render_text_png
from ..core.voiceover import CAPTION_MAX_W, build_narration_aligned, profile_args
from ..core.vertical import FONT_CAPTION, FONT_CAPTION_INDEX
from .shots import PhotoShot, Shot, caption_sprite, plan_shots, render_shots


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


def caption_line(shots: list[Shot], y_frac: float,
                 floor: float | None = None,
                 frame: Frame = VERTICAL) -> float:
    """One y for every caption in the piece, clearing the lowest photograph.

    Captions sit **under the photograph, not over it**: every source image is
    landscape, so even cropped it leaves a band of blurred backdrop below, and
    that band is where the type belongs. Putting it over the photo covers the
    thing it is describing and wastes the empty space.

    But **the y has to be the same for every shot**, not measured per shot.
    Captions are held until the next one starts, and shots dissolve over
    `XFADE`, so the outgoing sentence's last caption is still on screen while
    the incoming photograph is already visible. With a per-shot y the type
    jumped mid-dissolve, and on the shots whose photographs sit lowest it jumped
    *into* the incoming picture. Solving the worst case solves all of them: take
    the lowest caption line any shot needs and hold every caption there.

    The cost is that the tightest shots get slightly more air under the photo
    than they strictly need, which nobody notices. The jump, everybody did.
    """
    floor = frame.caption_floor if floor is None else floor
    lows = [y_frac]
    for sh in shots:
        if sh.image is None:
            continue
        # Measured at f=0.5, the middle of the Ken Burns move; the drift over a
        # five-second shot is small next to the margin below.
        _, y, _, h = PhotoShot(sh.image, sh.zoom, sh.pan,
                               sh.aspect, sh.bias, frame=frame).photo_box(0.5)
        lows.append((y + h + 96) / frame.h)
    return min(max(lows), floor)


def render_crypto_short(sentences: list, shots: list[Shot], out: Path,
                        workdir: Path, voice: str = "theo",
                        gap: "float | list[float]" = 0.34, tail: float = 1.2,
                        font_size: int = 46, y_frac: float = 0.70,
                        emoji: dict[str, str] | None = None,
                        sound: bool = True,
                        fps: int = 30,
                        frame: Frame = VERTICAL) -> tuple[Path, float]:
    """One short, end to end.

    `gap` is tighter than the drone quotes' 0.65. A quote wants air between
    lines; an explainer with a thirty-second budget does not, and the pauses
    are what a viewer scrolls away during. Pass a list to buy one beat more
    room than the others — a checklist needs the silence after its last option
    for the verdicts to land in.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    track, captions, total = build_narration_aligned(
        [list(s) for s in sentences], workdir, gap=gap, tail=tail,
        **profile_args(voice))

    plan_shots(shots, sentence_spans(sentences, captions))

    # Close the inter-sentence gaps: a shot's span ends at its last caption, so
    # the silence after it belonged to no shot and `render_shots` fell through
    # to the next one at f=0. Extending each shot to where the next begins keeps
    # the picture on screen through the pause, which is also what makes room for
    # a checklist's verdicts to land after its last option is spoken.
    for a, b in zip(shots, shots[1:]):
        a.hold = max(a.hold, b.start - a.start)
    shots[-1].hold = max(shots[-1].hold, total - shots[-1].start)

    first = 0
    for sh, sent in zip(shots, sentences):
        if sh.graphic:
            starts = [captions[first + k].start for k in range(len(sent))]
            n = len(sh.payload[0])
            # Options appear on the caption starts of their own sentence, so a
            # line arrives exactly as it is spoken. Even fractions of the shot
            # look synced until you watch it, and then every item is a beat
            # early or late. One caption per item and this needs no tuning.
            if sh.reveals is None:
                sh.reveals = (starts + [starts[-1]] * n)[:n]
            # The verdicts come afterwards, in the pause, evenly spaced with the
            # last one held back — the tick is the payoff and it wants the beat
            # before it to be longer than the beats between the crosses.
            if sh.marks is None:
                sh.marks = _mark_times(starts[-1], sh.start + sh.hold, n)
        first += len(sent)

    line = caption_line(shots, y_frac, frame=frame)

    pngs, ci = [], 0
    for sh, sent in zip(shots, sentences):
        for _ in sent:
            c = captions[ci]
            ci += 1
            # **A drawn beat carries no captions.** Its items already are the
            # type, set larger and in the middle of the frame, so a caption
            # underneath restates the line being read at that exact moment —
            # the viewer gets the same words twice in two places and neither
            # one is where the eye should be. The voice still speaks them and
            # the caption timings still drive `reveals`; only the burn goes.
            if sh.graphic or not c.text.strip():
                pngs.append(None)
                continue
            p = workdir / f"cap{len(pngs):02d}.png"
            # bg_luma is irrelevant here: stroke=4 selects the white-ink,
            # black-border treatment, the only one that survives type on a photo.
            render_text_png(c.text, p, size=font_size, bg_luma=0.0,
                            font_path=FONT_CAPTION, font_index=FONT_CAPTION_INDEX,
                            y_frac=line, stroke=4, max_w=CAPTION_MAX_W,
                            frame=frame)
            if emoji and c.text in emoji:
                add_caption_emoji(p, c.text, emoji[c.text], font_size,
                                  line, FONT_CAPTION, FONT_CAPTION_INDEX,
                                  frame=frame)
            pngs.append(p)

    sprites = [s for s in
               (caption_sprite(p, c.start, c.end)
                for p, c in zip(pngs, captions) if p is not None)
               if s is not None]

    picture = render_shots(workdir / "picture.mp4", shots, total,
                           fps=fps, captions=sprites, frame=frame)

    # A mark that lands silently is a graphic; one that lands with a sound is an
    # event. The cues come from the same list that drives the drawing, so they
    # cannot drift apart.
    if sound:
        cues = [(t, "tick" if ok else "cross")
                for sh in shots if sh.graphic and sh.marks
                for t, (_, ok) in zip(sh.marks, sh.payload[0])]
        if cues:
            track = sfx.mix(track, workdir / "track-sfx.wav", cues)

    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(picture), "-i", str(track),
         "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-crf", "18", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(out)],
        check=True, capture_output=True)
    return out, total


SPEAK_LAST = 0.95       # room left for the final option to actually be read
MARK_TAIL = 0.30        # the tick is on screen this long before the dissolve
MARK_STEP = 0.30        # between verdicts, when there is room for it


def _mark_times(last_start: float, end: float, n: int) -> list[float]:
    """When each verdict lands, inside the pause the checklist bought itself.

    Anchored on the **start** of the last option, not its end. A sentence's
    final caption is deliberately stretched to where the next sentence begins,
    so its `end` is already the end of the shot — anchoring there left exactly
    zero room and the marks were scheduled past the last frame, which is why the
    first build of this beat drew no verdicts at all.

    The tick is held back to 1.7 steps. It is the payoff, and a payoff needs the
    beat before it to be longer than the beats between the things it settles.
    """
    first = last_start + SPEAK_LAST
    room = (end - MARK_TAIL) - first
    step = MARK_STEP if n < 2 else min(MARK_STEP, max(0.10, room / (n - 1 + 0.7)))
    times = [first + i * step for i in range(n - 1)]
    return times + [(times[-1] if times else first) + step * 1.7]
