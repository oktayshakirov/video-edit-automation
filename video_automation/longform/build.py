"""One long-form video, end to end.

The same three-layer order as every other format in this repo — measure the
voice first, cut the picture to it, lay the sound on last — with what only long
form needs: a music bed, transition effects, and a set of artifacts that go up
alongside the MP4.

What is deliberately *not* here is a script generator. The script is the
product; 130 posts of automated scripts is the failure mode both short skills
already name, and long form makes it worse rather than better because three
minutes cannot coast on a good first line.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..core import music as music_mod
from ..core import sfx
from ..core.brand import Brand
from ..core.frame import LANDSCAPE, Frame
from ..core.vertical import (FONT_CAPTION, FONT_CAPTION_INDEX,
                             add_caption_emoji, render_text_png)
from ..core.voiceover import (CAPTION_MAX_W, build_narration_aligned,
                              profile_args)
from ..crypto.build import sentence_spans
from ..crypto.shots import caption_sprite, render_shots
from . import audio as audio_mod
from .beats import Checklist, item_count, make_beat
from .meta import Meta, write_srt
from .overlay import ClipOverlay
from .plan import Section, flatten, lay_out, mark_times, reveal_times
from .thumb import render_thumb

RISER_LEAD = 0.75       # a riser starts this far before the card it announces


def render_long(sections: list[Section], out: Path, workdir: Path,
                brand: Brand, meta: Meta | None = None,
                voice: str = "mia",
                music: str | Path | None = "tension",
                music_gain: float = 1.0,
                callouts: set[str] | None = None,
                emoji: dict[str, str] | None = None,
                thumb_image: Path | None = None,
                thumb_headline: str | None = None,
                thumb_accent: str = "red",
                # Overrides the searched side. The scorer answers "where is the
                # picture empty enough to take type", which a flat studio
                # backdrop can fail on its texture while still reading clean —
                # so the override exists, and using it is a judgement recorded
                # in the script rather than a silent default.
                thumb_side: str | None = None,
                endcard: Path | None = None, endcard_lead: float = 7.0,
                sound: bool = True, fps: int = 30,
                frame: Frame = LANDSCAPE) -> dict:
    """Build the video and everything that ships with it.

    `music` is a `core.music` preset name, a path to a track, or None. The
    preset is the default because a generated bed is ours to license on every
    platform and is rendered to the exact length — see that module.

    `callouts` is the set of caption texts to burn as a lower third — **not**
    every line. Full burned captions for three minutes fight every drawn beat
    for the same space, and the drawn beats are what buy the runtime. The
    complete transcript still ships, as an SRT that YouTube will index.
    """
    workdir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    callouts = set(callouts or ())

    sentences, shots, gaps = flatten(sections)
    track, captions, total = build_narration_aligned(
        [list(s) for s in sentences], workdir, gap=gaps, **profile_args(voice))

    spans = sentence_spans(sentences, captions)
    shots, groups, chapters = lay_out(sections, shots, spans, total)

    # Where each sentence's captions begin, so a beat spanning several
    # sentences can draw its reveals from all of them.
    first_cap, ci = [], 0
    for sent in sentences:
        first_cap.append(ci)
        ci += len(sent)

    # --- time the drawn beats to the voice -------------------------------
    #
    # Reveals come from the caption starts of the sentences the beat covers, so
    # an item appears exactly as it is spoken.
    for sh, group in zip(shots, groups):
        n = item_count(sh.graphic, sh.payload) if sh.graphic else 0
        if not n:
            continue
        starts = [captions[first_cap[si] + k].start
                  for si in group for k in range(len(sentences[si]))]
        reveal_times(sh, starts, n)
        if sh.marks is None and sh.graphic == "checklist":
            # `flow` marks each item as it is spoken, because the narration is
            # already saying "not a court ruling" — the cross confirms the word
            # rather than answering a question posed earlier. Without it the
            # verdicts are held for the pause after the last item, which is the
            # right beat only when the script asks rather than tells.
            flow = len(sh.payload) > 2 and sh.payload[2]
            if flow:
                sh.marks = [t + Checklist.FLOW_LAG for t in sh.reveals]
            else:
                sh.marks = mark_times(starts[-1], sh.start + sh.hold, n)

    # --- the callouts ----------------------------------------------------
    #
    # Two rules, both found on real frames of the first pilot.
    #
    # **A callout must not outlive its own sentence's audio.** Captions are held
    # until the next one starts, so the last chunk of a sentence runs across the
    # silence that follows it. The cap is the sentence's speech end, recoverable
    # as span end minus its gap, except on the final sentence where the span
    # already carries `tail` and no gap.
    #
    # **A drawn beat carries no callout at all**, which is the shorts' rule: the
    # beat's items already *are* the type, set larger and mid-frame, so a line
    # underneath restates what is being read at that moment in a worse place.
    caps: dict[int, float] = {}
    drawn: set[int] = set()
    for sh, group in zip(shots, groups):
        for si in group:
            end = spans[si][1] - (gaps[si] if si < len(sentences) - 1 else 0.0)
            for k in range(len(sentences[si])):
                caps[first_cap[si] + k] = end
                if sh.graphic:
                    drawn.add(first_cap[si] + k)

    pngs = []
    for i, c in enumerate(captions):
        if c.text.strip() not in callouts or i in drawn:
            pngs.append(None)
            continue
        p = workdir / f"call{len(pngs):03d}.png"
        # stroke=4 selects the white-ink, black-border treatment — the only one
        # that survives type sitting on a photograph.
        render_text_png(c.text, p, size=54, bg_luma=0.0,
                        font_path=FONT_CAPTION, font_index=FONT_CAPTION_INDEX,
                        y_frac=frame.caption_floor, stroke=4,
                        max_w=CAPTION_MAX_W, frame=frame)
        if emoji and c.text in emoji:
            add_caption_emoji(p, c.text, emoji[c.text], 54,
                              frame.caption_floor, FONT_CAPTION,
                              FONT_CAPTION_INDEX, frame=frame)
        pngs.append(p)

    sprites = [s for s in
               (caption_sprite(p, c.start, min(c.end, caps[i]))
                for i, (p, c) in enumerate(zip(pngs, captions)) if p is not None)
               if s is not None]

    # --- picture ---------------------------------------------------------
    # **Push, not dissolve, and faster.** A cross-dissolve necessarily shows
    # both shots at once, so for a third of a second the outgoing shot's type
    # sits over the incoming picture — read as a fault, not a transition.
    # A push keeps every pixel showing exactly one shot. 0.34 rather than the
    # shorts' 0.45 because a move that travels is legible in less time than a
    # fade that has to reach 50% before it reads as anything.
    picture = render_shots(
        workdir / "picture.mp4", shots, total, fps=fps, captions=sprites,
        frame=frame, transition="push", xfade=0.34,
        factory=lambda s, fr: make_beat(s, brand, fr),
        mark=brand.mark(int(frame.logo_w * brand.mark_scale)),
        overlays=_endcard(endcard, endcard_lead, total, frame))

    # --- sound -----------------------------------------------------------
    if sound:
        track = sfx.mix(track, workdir / "track-sfx.wav",
                        _cues(shots, total))

    if music:
        if isinstance(music, str) and music in music_mod.PRESETS:
            src = music_mod.write(workdir / "bed-src.wav", total + 4, music)
        else:
            src = Path(music)
        bed = audio_mod.render_bed(src, workdir / "bed.wav", total,
                                   gain=music_gain)
        track = audio_mod.mix_voice_over_bed(bed, track, workdir / "mix.wav",
                                             total)

    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(picture), "-i", str(track),
         "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-crf", "18", "-preset", "slow",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", str(out)],
        check=True, capture_output=True)

    # --- what ships with it ----------------------------------------------
    made = {"video": out, "total": total, "chapters": chapters}

    srt = out.with_suffix(".srt")
    write_srt(captions, srt)
    made["srt"] = srt

    if thumb_headline:
        thumb = out.with_name(out.stem + "-thumb.jpg")
        render_thumb(thumb, brand, thumb_headline, image=thumb_image,
                     accent=thumb_accent, side=thumb_side)
        made["thumb"] = thumb

    if meta is not None:
        sidecar = out.with_suffix(".md")
        meta.write(sidecar, chapters, total, out, srt, made.get("thumb"))
        made["meta"] = sidecar

    return made


def _endcard(path: "Path | None", lead: float, total: float,
             frame) -> list:
    """The subscribe sting, screen-blended over the last few seconds.

    It rides *over* the outro footage rather than replacing it, because the
    outro shot is deliberately uncluttered so YouTube's own end-screen elements
    have somewhere to sit — and a gap with nothing in it is what the viewer
    actually sees while the ask is being spoken.
    """
    if path is None or not Path(path).exists():
        return []
    start = max(0.0, total - lead)
    # Measured on the asset: the artwork sits in a stable box at x 0.48-0.89,
    # y 0.71-0.89 of the source, on pure black. Cropped to it and placed in the
    # lower middle — clear of the upper-left watermark and of the corners where
    # YouTube stacks its own end-screen cards.
    w = int(frame.w * 0.42)
    at = ((frame.w - w) // 2, int(frame.h * 0.60))
    return [ClipOverlay(Path(path), start, total, frame=frame, scale=0.42,
                        at=at, fade=0.5, crop=(0.46, 0.69, 0.91, 0.91))]


def _cues(shots, total: float) -> list[tuple[float, str]]:
    """Every sound effect in the piece, from the same data that drives the picture.

    Cues come off the shot list rather than being placed by hand, so picture and
    sound cannot drift apart — the rule the shorts' checklist established, now
    applied to transitions as well as marks.

    The set is deliberately small. A sound on every event is a cartoon; these
    mark the three things that are genuinely structural — a section beginning, a
    verdict landing, and an item arriving.
    """
    cues: list[tuple[float, str]] = []
    for i, sh in enumerate(shots):
        if sh.graphic == "chapter":
            # Riser *into* the card, impact *on* it. The riser has to start
            # before the cut it announces, so it is clamped at zero rather than
            # scheduled negative on an opening card.
            cues.append((max(0.0, sh.start - RISER_LEAD), "riser"))
            cues.append((sh.start, "impact"))
            # And a whoosh on the way out, covering the cut back to content.
            end = sh.start + sh.hold
            if end < total - 0.4:
                cues.append((end - 0.18, "whoosh"))
        elif sh.graphic in ("checklist", "compare", "stat", "quote"):
            for t in (sh.reveals or [])[:8]:
                cues.append((t, "reveal"))
        if sh.graphic == "checklist" and sh.marks:
            for t, (_, ok) in zip(sh.marks, sh.payload[0]):
                cues.append((t, "tick" if ok else "cross"))
    return [(t, k) for t, k in cues if 0.0 <= t < total]
