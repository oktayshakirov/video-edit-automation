"""Phase 4 — FCPXML export.

Written straight from a Jinja template rather than through OpenTimelineIO. The
OTIO FCP X adapter is the weakest in that set and argues about formats and
asset references; direct generation is less work and the failure modes are
visible in the output.

Four things FCPXML is unforgiving about, all handled here:

* **Rational time.** Every value is emitted over the same denominator as the
  format's frameDuration. At 30p that is n*100/3000s. Mixing denominators is
  legal but invites rounding surprises inside FCP.

* **media-rep.** An <asset> without a <media-rep> child imports as offline
  media. The src must be a percent-encoded file:// URL — these filenames have
  spaces in them.

* **Connected clip offset.** A clip connected to a spine clip expresses its
  offset in the *parent's* local time base, which starts at the parent's
  `start` value, not at zero. So the music's offset equals the first clip's
  source in-point. Getting this wrong slides the whole track out of sync —
  and it slides by the in-point, which is small enough to look like a
  sync bug rather than a structural one.

* **timeMap and `start` are mutually exclusive.** A clip carrying a <timeMap>
  must have `start="0s"`; its in-point lives in the timeMap's first `value`.
  Setting both makes FCP reject the edit with "Invalid edit with no respective
  media", because `start` and the timeMap disagree about where the media
  begins. Every retimed, reversed or ramped clip goes through _time_map below,
  which owns that rule in one place.
"""

from __future__ import annotations

import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape

from xml.sax.saxutils import escape

from .config import (
    EVENT_NAME,
    LOCATION_PIN,
    LOCATION_TITLE_TEXT,
    LOCATION_TITLE_STYLE,
    SOUND_EFFECTS,
    LOCATION_PIN_SECONDS,
    LOCATION_PIN_START,
    ESCALATE_BODY_SPEED,
    ESCALATE_TAIL_SECONDS,
    ESCALATE_TAIL_SPEED,
    FADE_TO_BLACK,
    MUSIC_FADE_SECONDS,
    RAMP_POINTS,
)
from .edit import Cut

TEMPLATE_DIR = Path(__file__).parent / "templates"

# FCP's own naming for common formats; anything unrecognised still imports,
# the name is cosmetic.
_FORMAT_NAMES = {
    (3840, 2160, 30): "FFVideoFormat3840x2160p30",
    (3840, 2160, 25): "FFVideoFormat3840x2160p25",
    (1920, 1080, 30): "FFVideoFormat1080p30",
    (1920, 1080, 25): "FFVideoFormat1080p25",
}


def _rational(frames: int, fps: int) -> str:
    """Frames -> an FCPXML time string over the format's timebase."""
    num, den = frames * 100, fps * 100
    g = math.gcd(num, den) or 1
    return f"{num // g}/{den // g}s" if den // g != 1 else f"{num // g}s"


def _file_url(path: Path) -> str:
    return "file://" + quote(str(path.resolve()))


def _time_map(c: Cut, fps: int) -> list[dict] | None:
    """Output-time -> source-time control points, or None for a plain cut.

    Covers all three non-trivial cases with one curve:
      constant retime  two points, unequal slopes
      reverse          two points, source running backwards
      ramp             several points along an eased curve

    The curve is approximated with straight segments rather than relying on
    FCP's `interp` attribute, whose exact easing is not something this code can
    verify without a round trip through Final Cut. Enough points and the
    difference is invisible.
    """
    if c.rate == 1.0 and not c.reverse and not c.ramp:
        return None

    s, length, dur = c.source_start, c.source_duration, c.duration

    if c.ramp == "escalate":
        # Flat at ESCALATE_BODY_SPEED, then a linear rise to ESCALATE_TAIL_SPEED
        # across the last ESCALATE_TAIL_SECONDS. Source position is the integral
        # of that speed profile: linear through the body, quadratic through the
        # tail. The slope of this curve *is* the playback speed, so it holds at
        # 200% and only ever climbs. Normalised so the curve lands exactly on
        # the last frame of the allotted source.
        # The pair is whatever the clip could actually fund (see fit_escalate);
        # it falls back to the configured ideal for edits built without a lock.
        body = c.body_speed or ESCALATE_BODY_SPEED
        tail = c.tail_speed or ESCALATE_TAIL_SPEED
        tf = min(ESCALATE_TAIL_SECONDS * fps, dur) / dur
        knee = 1.0 - tf

        def _raw(u: float) -> float:
            if u <= knee or tf <= 0:
                return body * u
            v = u - knee
            return body * knee + body * v + (tail - body) * v * v / (2.0 * tf)

        span = _raw(1.0)

        def travelled(u: float) -> float:
            return _raw(u) / span
    else:
        knee = 0.0

        def travelled(u: float) -> float:
            return u

    if c.ramp == "escalate":
        # Sample where the curve actually bends. The body is constant speed, so
        # two points describe it exactly; spending points there instead left the
        # whole 200%->2000% launch as a single averaged segment, which plays as
        # a step rather than a ramp.
        tail_pts = max(RAMP_POINTS - 2, 4)
        us = [0.0, knee] + [knee + (1.0 - knee) * (i + 1) / tail_pts
                            for i in range(tail_pts)]
    elif c.ramp:
        us = [i / (RAMP_POINTS - 1) for i in range(RAMP_POINTS)]
    else:
        us = [0.0, 1.0]

    points = []
    for u in us:
        f = travelled(u)
        if c.reverse:
            f = 1.0 - f
        points.append({
            "time": _rational(round(dur * u), fps),
            "value": _rational(s + round(length * f), fps),
        })
    return points


def _audio_rate(path: Path) -> str:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=sample_rate", "-of", "csv=p=0", str(path)],
            capture_output=True, text=True, check=True).stdout.strip()
        return out.splitlines()[0] if out else "44100"
    except Exception:
        return "44100"


def _audio_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True).stdout.strip()
    return float(out.splitlines()[0])


ASSET_DIR = Path(__file__).resolve().parents[2] / "assets"
PIN_FRAGMENT = ASSET_DIR / "fcpxml" / "location-pin-overlay.xml"
PIN_SOURCE = ASSET_DIR / "location-pin-source.mp4"
TITLE_FRAGMENT = ASSET_DIR / "fcpxml" / "location-title-overlay.xml"

# In-point of the red pin inside the pack, from the captured export. By hue the
# red pin measures ~345 deg and classifies as pink, so this cannot be found by
# searching for "red" — it is a measured constant, not a derivation.
PIN_SRC_IN = Fraction(29500, 3000)


def _location_pin(offset_frames: int, dur_frames: int, fps: int,
                  asset_id: str, format_id: str, effect_id: str) -> dict | None:
    """Splice the captured pin overlay, rewritten onto our resource ids.

    The fragment is reused as text rather than rebuilt, because the keyer's UID
    and its two base64 payloads encode FCP-internal state that cannot be
    authored from a specification — guessing that class of value caused two
    failed imports earlier in this project. Only the ids and the timing are
    rewritten; everything inside <filter-video> is passed through untouched.
    """
    if not PIN_FRAGMENT.is_file() or not PIN_SOURCE.is_file():
        return None

    # Strip comments before locating anything. The fragment's header comment
    # explains itself using the literal text "<asset-clip>", so searching the
    # raw file finds the prose first and splices the comment into the spine.
    text = re.sub(r"<!--.*?-->", "", PIN_FRAGMENT.read_text(encoding="utf-8"),
                  flags=re.S)
    body = text[text.index("<asset-clip"):text.rindex("</asset-clip>") + len("</asset-clip>")]
    effect = re.search(r"<effect\b[^>]*/>", text).group(0)

    # The fragment's own ids (r4 asset, r5 format, r6 effect) collide with the
    # ones this timeline allocates, so they are rewritten rather than assumed.
    body = body.replace('ref="r4"', f'ref="{asset_id}"', 1)
    body = body.replace('format="r5"', f'format="{format_id}"', 1)
    body = body.replace('ref="r6"', f'ref="{effect_id}"')
    effect = re.sub(r'id="r6"', f'id="{effect_id}"', effect, count=1)

    body = re.sub(r'offset="[^"]*"', f'offset="{_rational(offset_frames, fps)}"', body, count=1)
    body = re.sub(r'duration="[^"]*"', f'duration="{_rational(dur_frames, fps)}"', body, count=1)

    return {"effect": effect, "clip": body, "asset_id": asset_id,
            "format_id": format_id, "src": _file_url(PIN_SOURCE)}


def _location_title(text: str, offset_frames: int, dur_frames: int, fps: int,
                    effect_id: str) -> dict | None:
    """Splice the captured Basic Title, rewritten onto our effect id.

    Same reasoning as the pin: the generator's uid and the three `param key`
    paths are FCP-internal, so the fragment is reused as text and only the id,
    the timing and the words are rewritten. `start="3600s"` is Final Cut's
    convention for generators and is deliberately left alone — it is not an
    in-point into any media, and "correcting" it to 0s is a plausible-looking
    edit that would break the element.
    """
    if not text or not TITLE_FRAGMENT.is_file():
        return None

    raw = re.sub(r"<!--.*?-->", "", TITLE_FRAGMENT.read_text(encoding="utf-8"),
                 flags=re.S)
    body = raw[raw.index("<title"):raw.rindex("</title>") + len("</title>")]
    effect = re.search(r"<effect\b[^>]*/>", raw).group(0)

    body = body.replace("@@TEXT@@", escape(text))
    body = body.replace('ref="r7"', f'ref="{effect_id}"', 1)
    effect = re.sub(r'id="r7"', f'id="{effect_id}"', effect, count=1)

    body = re.sub(r'offset="[^"]*"', f'offset="{_rational(offset_frames, fps)}"', body, count=1)
    body = re.sub(r'duration="[^"]*"', f'duration="{_rational(dur_frames, fps)}"', body, count=1)

    if LOCATION_TITLE_STYLE:
        def restyle(m):
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
            attrs.update({k: str(v) for k, v in LOCATION_TITLE_STYLE.items()})
            return "<text-style " + " ".join(
                f'{k}="{escape(v, {chr(34): "&quot;"})}"'
                for k, v in attrs.items()) + m.group(2) + ">"
        # Only the definition carries styling; the <text-style ref="ts1"> inside
        # <text> is a reference and holds the words, so it must not be touched.
        # The definition is no longer self-closing — it wraps the MotionSimpleValues
        # block — so the tag form is preserved rather than assumed.
        body = re.sub(r"<text-style ((?:(?!ref=)[^>])*?)(/?)>", restyle, body, count=1)
        if "kerning" in LOCATION_TITLE_STYLE:
            # Kerning lives twice: as an attribute and inside MotionSimpleValues.
            # Changing only the attribute leaves Final Cut using the old spacing.
            body = re.sub(r'(name="motionTextKerning"[^>]*value=")[^"]*"',
                          rf'\g<1>{LOCATION_TITLE_STYLE["kerning"]}"', body)

    return {"effect": effect, "clip": body}


def _music_clips(audio: dict, music_frames: int, video_end: int, base: int,
                 fps: int, track) -> list[dict]:
    """Lay the music out, once or looped, as connected clips.

    Unlooped this is one clip. Looped it is two passes of the same asset on
    separate lanes, overlapping across the crossfade — connected clips on one
    lane may not overlap, and a butt join between two passes of the same song
    is exactly the click the crossfade exists to avoid.

    Volume keyframe times live in each clip's own time base, which starts at its
    `start` value rather than at zero. For pass 2 that base is the source
    in-point, not the timeline position, which is the easy thing to get wrong
    here: the fade would still render, just in the wrong place.
    """
    if track is None or track.loop is None:
        clip = dict(audio, lane=-1, offset=_rational(base, fps), start="0s",
                    duration=_rational(min(music_frames, video_end), fps))
        # Footage outlasting the track is the caller's problem; footage running
        # out first ends the music under the last shot rather than over black.
        if music_frames > video_end:
            fade = min(int(MUSIC_FADE_SECONDS * fps), video_end)
            clip["volume"] = [(video_end - fade, "0dB"), (video_end, "-96dB")]
        return [clip]

    lp = track.loop
    xf = int(round(lp.crossfade_bars * track.bar_period * fps))
    handoff = round(track.bar_time(lp.handoff_bar) * fps)
    return_at = round(track.bar_time(lp.return_bar) * fps)

    # Pass 1: source 0 up to the handoff, fading out across the crossfade.
    first = dict(audio, lane=-1, offset=_rational(base, fps), start="0s",
                 duration=_rational(handoff, fps),
                 volume=[(handoff - xf, "0dB"), (handoff, "-96dB")])

    # Pass 2: re-enters so that the return bar lands exactly on the handoff.
    src_in = max(return_at - xf, 0)
    tl_in = handoff - xf
    dur = min(video_end - tl_in, music_frames - src_in)
    vol = [(src_in, "-96dB"), (src_in + xf, "0dB")]
    if tl_in + dur >= video_end:
        fade = min(int(MUSIC_FADE_SECONDS * fps), dur - xf)
        if fade > 0:
            vol += [(src_in + dur - fade, "0dB"), (src_in + dur, "-96dB")]
    second = dict(audio, lane=-2, offset=_rational(base + tl_in, fps),
                  start=_rational(src_in, fps), duration=_rational(dur, fps),
                  volume=vol)

    return [first, second]


def render(cuts: list[Cut], music: Path, fps: int, width: int, height: int,
           project_name: str, event_name: str = EVENT_NAME, track=None) -> str:
    if not cuts:
        raise ValueError("no cuts to write")

    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        autoescape=select_autoescape(["xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # One asset per distinct source clip, however many times it is used.
    assets: dict[str, dict] = {}
    for c in cuts:
        if c.clip.hash not in assets:
            assets[c.clip.hash] = {
                "id": f"r{len(assets) + 1}",
                "name": Path(c.clip.filename).stem,
                "uid": c.clip.hash,
                "duration": _rational(int(c.clip.duration * fps), fps),
                "src": _file_url(Path(c.clip.path)),
            }

    music_frames = int(_audio_duration(music) * fps)
    audio = {
        "id": f"r{len(assets) + 1}",
        "name": Path(music.name).stem,
        "uid": "music-" + str(abs(hash(str(music))))[:12],
        "duration": _rational(music_frames, fps),
        "src": _file_url(music),
        "rate": _audio_rate(music),
    }

    rendered_cuts = []
    for c in cuts:
        tm = _time_map(c, fps)
        rendered_cuts.append({
            "ref": assets[c.clip.hash]["id"],
            "name": Path(c.clip.filename).stem,
            "offset": _rational(c.timeline_start, fps),
            # A clip with a timeMap must start at 0s; its in-point is the
            # timeMap's first value. Setting both is the "invalid edit" bug.
            "start": "0s" if tm else _rational(c.source_start, fps),
            "duration": _rational(c.duration, fps),
            "timemap": tm,
            "fade": None,
        })

    video_end = max(c.timeline_start + c.duration for c in cuts)

    # Fade the picture out under the closing music fade so both land together.
    # Keyframe times are in the clip's own time base, which starts at `start` —
    # and `start` is 0s whenever a timeMap is present, so the base differs
    # between a plain cut and a retimed one.
    if FADE_TO_BLACK:
        last, entry = cuts[-1], rendered_cuts[-1]
        fade = min(int(MUSIC_FADE_SECONDS * fps), last.duration)
        base = 0 if entry["timemap"] else last.source_start
        entry["fade"] = {
            "from": _rational(base + last.duration - fade, fps),
            "to": _rational(base + last.duration, fps),
        }

    # A connected clip's offset is in the parent's local time base, which starts
    # at the parent's `start` — not at zero. That base is 0 whenever the first
    # clip carries a timeMap, and its source in-point otherwise.
    base = 0 if rendered_cuts[0]["timemap"] else cuts[0].source_start
    music_clips = _music_clips(audio, music_frames, video_end, base, fps, track)
    for mc in music_clips:
        mc["volume"] = [{"time": _rational(t, fps), "value": v}
                        for t, v in mc.get("volume", [])]

    # Hand-placed effects, anchored to whichever spine clip is on screen when
    # they start — the same shape Final Cut itself exports. Anchoring them all
    # to the first clip instead would work only while that clip is long enough
    # to span them.
    sfx_assets: list[dict] = []
    for i, fx in enumerate(SOUND_EFFECTS):
        path = Path(fx["file"]).expanduser()
        if not path.is_file():
            print(f"  note: sound effect not found, skipping: {path}")
            continue
        aid = next((a["id"] for a in sfx_assets if a["path"] == str(path)), None)
        if aid is None:
            aid = f"r{len(assets) + 6 + len(sfx_assets)}"
            sfx_assets.append({
                "id": aid, "path": str(path), "name": path.stem,
                "uid": "sfx-" + str(abs(hash(str(path))))[:12],
                "duration": _rational(int(_audio_duration(path) * fps), fps),
                "src": _file_url(path), "rate": _audio_rate(path),
            })
        at = int(round(float(fx["at"]) * fps))
        host = max((j for j, c in enumerate(cuts) if c.timeline_start <= at),
                   default=0)
        hc, he = cuts[host], rendered_cuts[host]
        hbase = 0 if he["timemap"] else hc.source_start
        he.setdefault("sfx", []).append({
            "ref": aid, "name": path.stem, "lane": -1,
            "offset": _rational(hbase + at - hc.timeline_start, fps),
            "start": _rational(int(round(float(fx.get("start", 0.0)) * fps)), fps),
            "duration": _rational(int(round(float(fx["duration"]) * fps)), fps),
        })

    pin = title = None
    if LOCATION_PIN:
        pin_off = int(round(LOCATION_PIN_START * fps))
        pin_dur = int(round(LOCATION_PIN_SECONDS * fps))
        # The pin is a connected clip, so it has to live inside a spine clip
        # that actually spans it; anchoring it past the first shot's outgoing
        # cut would put it on a clip that is no longer on screen.
        if pin_off + pin_dur > cuts[0].duration:
            pin_dur = max(cuts[0].duration - pin_off, 0)
        if pin_dur > 0:
            pin = _location_pin(
                base + pin_off, pin_dur, fps,
                asset_id=f"r{len(assets) + 2}", format_id=f"r{len(assets) + 3}",
                effect_id=f"r{len(assets) + 4}")
        if pin is None:
            print("  note: LOCATION_PIN is on but the overlay could not be "
                  "placed — check assets/ and the opening shot's length")
        elif LOCATION_TITLE_TEXT:
            # The title rides the pin's window so the two appear and leave
            # together; it sits on lane 2, above the pin's lane 1.
            title = _location_title(LOCATION_TITLE_TEXT, base + pin_off, pin_dur,
                                    fps, effect_id=f"r{len(assets) + 5}")

    seq_frames = video_end

    return env.get_template("timeline.fcpxml.j2").render(
        fmt_name=_FORMAT_NAMES.get((width, height, fps), f"FFVideoFormat{width}x{height}p{fps}"),
        frame_duration=_rational(1, fps),
        width=width,
        height=height,
        video_assets=list(assets.values()),
        audio=audio,
        music_clips=music_clips,
        sfx_assets=sfx_assets,
        pin=pin,
        title=title,
        cuts=rendered_cuts,
        sequence_duration=_rational(seq_frames, fps),
        project_name=project_name,
        event_name=event_name,
    )
