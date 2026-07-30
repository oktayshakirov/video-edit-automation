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
import subprocess
from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import (
    EVENT_NAME,
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


def render(cuts: list[Cut], music: Path, fps: int, width: int, height: int,
           project_name: str, event_name: str = EVENT_NAME) -> str:
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

    # If the footage runs out before the track does, end the music under the
    # last shot and fade it, rather than letting it play on over black.
    if music_frames > video_end:
        fade_frames = min(int(MUSIC_FADE_SECONDS * fps), video_end)
        audio["duration"] = _rational(video_end, fps)
        audio["fade_from"] = _rational(video_end - fade_frames, fps)
        audio["fade_to"] = _rational(video_end, fps)
    seq_frames = max(video_end, music_frames if music_frames <= video_end else video_end)

    return env.get_template("timeline.fcpxml.j2").render(
        fmt_name=_FORMAT_NAMES.get((width, height, fps), f"FFVideoFormat{width}x{height}p{fps}"),
        frame_duration=_rational(1, fps),
        width=width,
        height=height,
        video_assets=list(assets.values()),
        audio=audio,
        cuts=rendered_cuts,
        sequence_duration=_rational(seq_frames, fps),
        project_name=project_name,
        event_name=event_name,
    )
