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

import shutil
import subprocess
from pathlib import Path

from ..core import music as music_mod
from ..core import samples, sfx
from ..core import transitions, typewriter
from ..core.brand import Brand
from ..core.frame import LANDSCAPE, Frame
from ..core.vertical import (FONT_CAPTION, FONT_CAPTION_INDEX,
                             add_caption_emoji, render_text_png)
from ..core.voiceover import (CAPTION_MAX_W, build_narration_aligned,
                              profile_args)
from ..crypto.build import sentence_spans
from ..crypto.shots import caption_sprite, render_shots
from . import audio as audio_mod
from . import chrome as chrome_mod
from .beats import Checklist, item_count, make_beat
from .meta import Meta, write_srt
from .overlay import (CinematicTitle, ClipOverlay, Emphasis, EndCard,
                      TitleOverlay, TvOff)
from .plan import (Section, flatten, lay_out, mark_times, reveal_times,
                   style_chapters)
from .thumb import render_thumb



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
                thumb_accent2: str | None = None,
                # Overrides the searched side. The scorer answers "where is the
                # picture empty enough to take type", which a flat studio
                # backdrop can fail on its texture while still reading clean —
                # so the override exists, and using it is a judgement recorded
                # in the script rather than a silent default.
                thumb_side: str | None = None,
                thumb_crop_at: tuple[float, float] | None = None,
                thumb_crop_zoom: float = 1.0,
                thumb_crop_band: str = "middle",
                thumb_shift: float = 0.0,
                # The band-card look on the thumbnail, opt-in for an A/B:
                # `thumb_accent="band"`, a glowing kicker, film grain.
                thumb_kicker: str | None = None,
                thumb_grain: bool = False,
                # The navigation layer: a ticked progress bar along the
                # bottom and "3 of 5" under each chapter card. **Off since
                # 2026-10-02, by the editor's call** - the bar along the bottom
                # was not wanted on these videos, and the A/B `chrome.py`
                # argues for is settled by that rather than by a curve. Pass
                # True to put it back on one video.
                chrome_nav: bool = False,
                # "band" (the default since 2026-10-21): the section's kicker
                # (or "CHAPTER n") glowing over a band in the brand colour, the
                # title typed into it. "type" is the centred typed card. See
                # `beats.column.ChapterCard.band`.
                chapter_style: str = "band",
                endcard: Path | None = None, endcard_lead: float = 7.0,
                # The title sequence. `title_at` is the second it starts and
                # turns the whole thing on; `title` defaults to `meta.title`
                # and `title_eyebrow` to the brand's own domain. See
                # `overlay.TitleOverlay` — this supersedes putting the title in
                # a `Shot(payload=)` statement, which is a different device
                # doing a job it was never designed for.
                title_at: float | None = None,
                title: str | None = None,
                title_hold: float = 5.0,
                title_eyebrow: str | None = None,
                # "cinematic" (the default since 2026-10-20): a centred trailer
                # card - `overlay.CinematicTitle`. "lower" brings back the
                # typed lower third, `overlay.TitleOverlay`.
                title_style: str = "cinematic",
                # The old-film surface - grain, dust, a light leak, flicker -
                # arranged per shot by `core.filmfx.plan`; on by default since
                # 2026-10-21. False turns it off, a number scales it.
                film: "bool | float" = True,
                # Glitch and TV-static cuts on a few meaningful cuts - a
                # turn, a chapter, a jump in time. `transitions.plan_special`.
                special_cuts: "bool | int" = True,
                # Key words, punched in large as they are spoken, over
                # footage only - once or twice a minute. `overlay.Emphasis`.
                emphasis: "list[str] | None" = None,
                # A quiet bed of the place a clip shows - city, rain, office,
                # servers - under long enough footage shots only. False off,
                # a number scales it. `core/ambience.py`.
                ambience: "bool | float" = True,
                # The redacted opening hook - see `overlay.HookOverlay` and
                # longform.md's "The first five seconds carry information".
                # The `[bracketed]` word is hidden until the voice says it;
                # `hook_until` is the fallback reveal if it is never said.
                hook: str | None = None,
                # An opener variant from `longform.openers`; takes precedence
                # over `hook=`. See docs/video/longform.md.
                opener=None,
                hook_until: float = 3.0,
                sound: bool = True, fps: int = 30,
                # Intermediates are deleted on success. See the note at the end
                # of this function; set True while iterating on a cut.
                keep_work: bool = False,
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
    # The thumbnail is drawn last, after the MP4: a clip passed as its image
    # used to fail there, in `cv2.imread`, and cost the sidecar with it.
    if thumb_image is not None and Path(thumb_image).suffix.lower() in (
            ".mp4", ".mov", ".webm"):
        raise ValueError(f"thumb_image must be a still, got {Path(thumb_image).name}"
                         f" - export a frame, or build the cover in thumbs()")
    workdir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    callouts = set(callouts or ())

    sentences, shots, gaps = flatten(sections)
    style_chapters(shots, chapter_style)
    track, captions, total = build_narration_aligned(
        [list(s) for s in sentences], workdir, gap=gaps, **profile_args(voice))

    spans = sentence_spans(sentences, captions)
    shots, groups, chapters = lay_out(sections, shots, spans, total)
    # A reel that dives into its last card, or opens out of its first, is
    # joined to the clip beside it here, once the holds are final.
    from .beats.reel import link_reels
    link_reels(shots)
    if special_cuts:
        # A few glitch and TV-static cuts where the cut means something -
        # `transitions.plan_special` has the rules and the budget.
        lines = [transitions.sentence_text(sentences[g[0]]) if g else ""
                 for g in groups]
        n = None if special_cuts is True else int(special_cuts)
        for t, mode, why in transitions.plan_special(shots, lines, total,
                                                     budget=n):
            print(f"special cut: {mode} at {t:.1f}s ({why})")

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
        # `logos` carries optional verdicts on the same two-phase clock. Only
        # when the items actually have one — a plain lineup has no marks and
        # must not get a mark *sound* either.
        if (sh.marks is None and sh.graphic == "logos"
                and any(len(it) > 2 and it[2] is not None
                        for it in sh.payload[0])):
            sh.marks = mark_times(starts[-1], sh.start + sh.hold, n)
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
    hook_ov = ([opener.build(frame, brand, captions)] if opener is not None
               else _hook(hook, hook_until, brand, frame, captions))
    title_ov = _title(title_at, title, title_hold, title_eyebrow,
                      meta, brand, frame, title_style)
    end_ov = _endcard(endcard, endcard_lead, total, frame, brand)
    tv_ov = [TvOff(total, frame)]
    emph_ov = _emphasis(emphasis, captions, shots, total, brand, frame,
                        avoid=[(o.start - 0.5, o.end + 0.5)
                               for o in title_ov + end_ov])
    film_ov = []
    if film:
        # The old-film surface, placed per shot (`core.filmfx.plan`). An
        # underlay: under the watermark, burned captions and every overlay,
        # so all type stays clean over a textured picture.
        from ..core.filmfx import FilmOverlay
        windows = ([(o.start, o.end, "title") for o in title_ov]
                   + [(o.start, o.end, "end") for o in end_ov])
        film_ov = [FilmOverlay(shots, total, windows,
                               strength=1.0 if film is True else float(film),
                               fps=fps)]

    picture = render_shots(
        workdir / "picture.mp4", shots, total, fps=fps, captions=sprites,
        frame=frame, transition="push", xfade=0.34,
        factory=lambda s, fr: make_beat(s, brand, fr),
        # The beats have always taken the brand; the *photographs* did not, and
        # their hairline was drawn in thecrypto.wiki's gold whichever site the
        # video was for. No roaming watermark here: it exists to survive a
        # reposted vertical crop and to defeat corner blindness in a feed, and
        # a 16:9 video is watched in a player, not scrolled past.
        brand=brand,
        mark=brand.mark(int(frame.logo_w * brand.mark_scale)),
        underlays=film_ov,
        overlays=(emph_ov + end_ov
                  + title_ov
                  + _chrome(chrome_nav, chapters, shots, total, brand, frame)
                  + hook_ov
                  # Last, over everything: the video switches off.
                  + tv_ov))

    # --- sound -----------------------------------------------------------
    if sound:
        # **The kit comes from the brand, not from the caller.** Which sounds a
        # site uses is a property of that site's audience - tinnitushelp.me's
        # viewers frequently have hyperacusis, so that kit has no slam, no
        # glitch and no bitcrushing in it (see `core/sfx.py`, `KITS`). Making
        # it an argument would mean every script had to remember; making it the
        # brand's means a script cannot get it wrong. `KITS["crypto"]` is
        # empty, so thecrypto.wiki renders exactly as it always did.
        track = sfx.mix(track, workdir / "track-sfx.wav",
                        _cues(shots, total)
                        + transitions.cues(shots)
                        + [c for h in hook_ov for c in h.cues()]
                        + [c for o in title_ov + end_ov + tv_ov + emph_ov
                           for c in o.cues()],
                        kit=brand.name)
        # Sound samples a beat names, in the pause after each is spoken
        # (`core/samples.py`) - and the bed dips under them below.
        sample_cues = samples.cues(shots, [c.start for c in captions], total)
        if sample_cues:
            track = sfx.mix(track, workdir / "track-samples.wav", sample_cues,
                            kit=brand.name)
    else:
        sample_cues = []

    if music:
        if isinstance(music, str) and music in music_mod.PRESETS:
            src = music_mod.write(workdir / "bed-src.wav", total + 4, music)
        else:
            src = Path(music)
        bed = audio_mod.render_bed(src, workdir / "bed.wav", total,
                                   gain=music_gain)
        if sample_cues:
            bed = audio_mod.dip(bed, workdir / "bed-dip.wav",
                                samples.windows(sample_cues))
        track = audio_mod.mix_voice_over_bed(bed, track, workdir / "mix.wav",
                                             total)

    if sound and ambience:
        # Quiet place-sound under footage that shows a place - restrained by
        # rule, not by taste (`core/ambience.py`).
        from ..core import ambience as ambience_mod
        track = ambience_mod.mix(track, workdir / "mix-ambience.wav", shots,
                                 total, kit=brand.name,
                                 gain=1.0 if ambience is True else float(ambience))

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
                     accent=thumb_accent, accent2=thumb_accent2,
                     side=thumb_side,
                     crop_at=thumb_crop_at, crop_zoom=thumb_crop_zoom,
                     crop_band=thumb_crop_band, shift=thumb_shift,
                     kicker=thumb_kicker, grain=thumb_grain)
        made["thumb"] = thumb

    if meta is not None:
        sidecar = out.with_suffix(".md")
        meta.write(sidecar, chapters, total, out, srt, made.get("thumb"))
        made["meta"] = sidecar

    # --- scratch ----------------------------------------------------------
    # The work directory is intermediates only: raw narration and bed WAVs, the
    # silent picture pass, per-shot PNGs. It runs 130-330 MB per video and
    # nothing in it is needed once the MP4, SRT, thumbnail and sidecar exist.
    # Seven videos had left 937 MB of it sitting on the Desktop.
    #
    # Deleted only on success, and only below `out`'s parent, so a failed render
    # keeps everything needed to debug it. Pass `keep_work=True` when you are
    # iterating on a cut and want the intermediates back without a re-render.
    if not keep_work:
        shutil.rmtree(workdir, ignore_errors=True)

    return made


def _chrome(on: bool, chapters: list[tuple[float, str]], shots, total: float,
            brand: Brand, frame: Frame) -> list:
    """The progress bar and the per-card "n of N", or nothing.

    Built here rather than in the scripts because it is derived entirely from
    what `lay_out` already returned: a script that adds a section gets the
    extra tick and the recounted cards for free, and one that reorders them
    cannot get the pair out of step.

    A video with fewer than the two chapters `meta.MIN_CHAPTERS` expects gets
    no bar at all - a progress rule with no ticks in it is a plain wipe across
    the bottom of the frame that says nothing about structure.
    """
    if not on or len(chapters) < 2:
        return []
    out = [chrome_mod.ProgressBar([t for t, _ in chapters], total, brand,
                                  frame)]
    # The counter belongs to the *cards*, not to the chapter list: the opening
    # section takes `card=False` (see `longform.md`), so its chapter entry has
    # no card on screen to annotate.
    cards = [sh for sh in shots if sh.graphic == "chapter"]
    out += [chrome_mod.ChapterCount(i + 1, len(cards), sh.start, sh.hold,
                                    brand, frame)
            for i, sh in enumerate(cards)]
    return out


def _endcard(path: "Path | None", lead: float, total: float,
             frame, brand: Brand) -> list:
    """"THANKS FOR WATCHING", then "LIKE & COMMENT!" - `overlay.EndCard`.

    **No sting and no arrow (2026-10-21).** This used to screen-blend a stock
    subscribe clip whose arrow pointed down and right, toward the side YouTube
    does not put its subscribe element on. Silent: the narration is still
    asking.

    `path` only switches it on; any truthy value does, so every shipped
    script's `endcard=ENDCARD` keeps working without the clip on disk.
    """
    if not path:
        return []
    start = max(0.0, total - lead)
    return [EndCard(start, total, brand, frame=frame)]


def _title(at: "float | None", text: "str | None", hold: float,
           eyebrow: "str | None", meta, brand, frame,
           style: str = "cinematic") -> list:
    """The title sequence, if this build asked for one.

    **Put it on the line that promises the payoff, not on frame one.** The
    format's own rule about the title stamp is unchanged by the new treatment:
    around eight seconds in, the video has already earned the first five
    seconds with a fact, and the title arriving there reads as a title
    sequence rather than as a slate the viewer has to sit through.
    """
    if at is None:
        return []
    line = text or (meta.title if meta is not None else None)
    if not line:
        raise ValueError("title_at was given but there is no title to draw - "
                         "pass `title=` or a `meta` with one")
    if style == "cinematic":
        return [CinematicTitle(line, at, hold, brand, frame=frame,
                               eyebrow=eyebrow)]
    return [TitleOverlay(line, at, hold, brand, frame=frame, eyebrow=eyebrow)]


def _emphasis(words, captions, shots, total: float, brand, frame,
              avoid=()) -> list:
    """An `Emphasis` for each script-chosen key word, where it is spoken.

    Each phrase is found in the captions, in order, case-insensitively, and
    timed by its position inside its caption chunk - the estimate the Shorts'
    karaoke uses. It is **dropped**, with a line in the build log, if it is
    never spoken, if it lands over anything but footage or a photograph (a
    drawn beat, a chapter card) or inside an `avoid` window (the title, the
    end card), or within 20s of the last one: once or twice a minute is the
    device; more is subtitles.
    """
    from .meta import is_disclaimer
    out, used, last = [], 0, -1e9
    for phrase in words or ():
        key = phrase.lower()
        hit = None
        for ci in range(used, len(captions)):
            text = captions[ci].text.lower()
            k = text.find(key)
            if k >= 0:
                c = captions[ci]
                span = max(0.2, c.speech_end - c.start)
                hit = (c.start + span * k / max(1, len(text)), ci)
                break
        if hit is None:
            print(f"emphasis: '{phrase}' is never spoken - skipped")
            continue
        at, used = hit[0], hit[1] + 1
        sh = next((s for s in shots
                   if s is not None and s.start <= at < s.start + s.hold), None)
        line = (sh.payload[1] if sh is not None and sh.payload
                and len(sh.payload) > 1 else "")
        ok_shot = (sh is not None and sh.graphic is None
                   and not (line and is_disclaimer(str(line))))
        if not ok_shot or any(a <= at <= b for a, b in avoid):
            print(f"emphasis: '{phrase}' at {at:.1f}s is over a graphic, "
                  f"the title or the end card - skipped")
            continue
        if at - last < 20.0:
            print(f"emphasis: '{phrase}' at {at:.1f}s is {at - last:.0f}s after "
                  f"the last one - skipped (20s apart)")
            continue
        out.append(Emphasis(phrase, at, brand, frame))
        last = at
    return out


def _hook(text: str | None, fallback: float, brand: Brand, frame,
          captions: list) -> list:
    if not text:
        return []
    from .overlay import HookOverlay
    from ..crypto.build import hook_reveal_time
    reveal = hook_reveal_time(text, captions, fallback=fallback)
    return [HookOverlay(text, reveal_at=reveal, frame=frame,
                        accent=brand.primary, size=84, max_lines=2)]


def _cues(shots, total: float) -> list[tuple[float, str]]:
    """Every sound effect in the piece, from the same data that drives the picture.

    Cues come off the shot list rather than being placed by hand, so picture and
    sound cannot drift apart — the rule the shorts' checklist established, now
    applied to transitions as well as marks.

    The set is deliberately small. A sound on every event is a cartoon; these
    mark what is genuinely structural — a section beginning, an item arriving,
    a verdict landing, and (for the beats that draw a mechanism) the moment the
    mechanism turns: a causal link made, a feedback loop closing, a threshold
    crossed.
    """
    cues: list[tuple[float, str]] = []
    for i, sh in enumerate(shots):
        if sh.graphic == "chapter":
            # Riser *into* the card, impact *on* it. The riser has to start
            # before the cut it announces, so it is clamped at zero rather than
            # scheduled negative on an opening card.
            # The riser's hard stop lands on the cut - the cue time is its
            # anchor, not its start (`sfx.FILE_SFX`).
            cues.append((sh.start, "chapter_riser"))
            cues.append((sh.start, "impact"))
            # A key click per character as the title types on - the same
            # schedule `ChapterCard` draws from, so no click lands early.
            cues += typewriter.card_cues(sh.payload, sh.start, sh.hold)
            # And a whoosh on the way out, covering the cut back to content —
            # **unless the shot carries a transition that brings its own
            # sound.** A card leaving on a `whip` would otherwise fire this
            # whoosh at `end - 0.18` and the whip's at `end - 0.32`: two of
            # the same sound 0.14s apart, which is a flam rather than a
            # transition. The transition owns the cut when one is set, because
            # its cue is timed to the move it is actually covering.
            #
            # **The editor's cinematic flashback, not the synthesized whoosh**
            # (2026-10-21) - the same exit sound as the opening title, its hit
            # landing in the card's own close (`sfx.FILE_SFX` anchors it).
            end = sh.start + sh.hold
            if end < total - 0.4 and sh.transition not in transitions.CUES:
                cues.append((end - 0.20, "title_flashback"))
        elif sh.graphic == "spotlight":
            # A soft pan as the camera leaves for each framing.
            cues += [(t - 0.10, "pan") for t in (sh.reveals or [])[1:12]]
        elif sh.graphic == "post":
            # The card arriving on a pan, the highlighter on a tick.
            rv = sh.reveals or []
            if rv:
                cues.append((rv[0] - 0.05, "pan"))
            if len(rv) > 1:
                cues.append((rv[1] + 0.05, "reveal"))
        elif sh.graphic == "blindsign":
            # The card on a pan, a tick per approval, the scanline on a
            # glitch and its landing on a cross (`beats.blindsign`).
            from .beats.blindsign import sign_times, sweep_span
            rv = sh.reveals or []
            if rv:
                cues.append((rv[0] - 0.05, "pan"))
            if len(rv) > 1:
                cues += [(t, "tick") for t in sign_times(rv[1], len(sh.payload[2]))]
            if len(rv) > 2:
                t0, t1 = sweep_span(rv[2])
                cues += [(t0, "glitch_cut"), (t1 - 0.05, "cross")]
        elif sh.graphic == "reel":
            # A pan whoosh as the camera leaves for each next card, and the
            # label's tick as it lands (`beats.reel.Reel`).
            for i, t in enumerate((sh.reveals or [])[:12]):
                if i:
                    cues.append((t - 0.12, "pan"))
                cues.append((t + 0.20, "reveal"))
        elif sh.graphic == "diagram":
            # Each node lands with its connector, so one cue per reveal marks
            # "and therefore" — `link`, not `reveal`, because a causal step is
            # more than a line of type arriving.
            for t in (sh.reveals or [])[:8]:
                cues.append((t, "link"))
            # `loop=True` (payload[2]): the feedback arrow closes across the
            # closing sentence — one low tone as it lands, near the shot end.
            if len(sh.payload) > 2 and sh.payload[2] and sh.reveals:
                cues.append((sh.start + sh.hold - 0.45, "loop_close"))
        elif sh.graphic == "gauge":
            for t in (sh.reveals or [])[:2]:
                cues.append((t, "reveal"))
            # The marker crosses the threshold partway through the value
            # sentence — `limit` lands at that crossing, not at the reveal.
            frac = float(sh.payload[1]) if len(sh.payload) > 1 else 0.0
            thr = sh.payload[3] if len(sh.payload) > 3 else None
            if (thr is not None and frac > float(thr)
                    and sh.reveals and len(sh.reveals) > 1):
                r1 = sh.reveals[1]
                travel = min(1.5, max(0.5, (sh.start + sh.hold - r1) - 0.16))
                cues.append((r1 + 0.05 + travel * (float(thr) / frac), "limit"))
        if sh.clip is not None and sh.payload and len(sh.payload) > 1:
            # A disclaimer line takes the notice card, which lands on the
            # notification chime (`clip.VideoShot._notice`).
            from .clip import VideoShot
            from .meta import is_notice
            if is_notice(sh.payload):
                cues.append((sh.start + VideoShot.NOTICE_IN, "notification"))
        elif sh.graphic in ("checklist", "compare", "stat", "quote", "logos",
                            "callout", "replicate", "pool"):
            for t in (sh.reveals or [])[:8]:
                cues.append((t, "reveal"))
        if sh.graphic in ("checklist", "logos") and sh.marks:
            # The verdict is the item's **last** element whatever the beat: a
            # checklist row is `(text, ok)` and a logo tile is
            # `(slug, label, ok)`, so unpacking a fixed shape raises on one of
            # them.
            for t, item in zip(sh.marks, sh.payload[0]):
                if item[-1] is not None:
                    cues.append((t, "tick" if item[-1] else "cross"))
    return [(t, k) for t, k in cues if 0.0 <= t < total]
