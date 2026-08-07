"""Structural check on a generated FCPXML before it ever reaches Final Cut.

Catches the failures that are painful to diagnose inside FCP itself: a spine
with a one-frame gap, a clip whose source range runs past the end of its media,
an offline asset, or a connected audio clip whose offset was written in the
wrong time base.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path
from urllib.parse import unquote, urlparse

# Final Cut ships the DTD it actually validates against. Checking locally beats
# discovering element-order violations from an import dialog.
DTD_DIR = Path("/Applications/Final Cut Pro.app/Contents/Frameworks/"
               "Interchange.framework/Versions/A/Resources")


def find_dtd(version: str) -> Path | None:
    p = DTD_DIR / f"FCPXMLv{version.replace('.', '_')}.dtd"
    return p if p.exists() else None


def _staged_dtd(src: Path) -> Path:
    """Copy the DTD somewhere without spaces in the path.

    xmllint treats --dtdvalid as a URI, and 'Final Cut Pro.app' contains
    spaces, so pointing it straight at the app bundle fails with a misleading
    "Could not parse DTD" that looks like the DTD itself is broken.
    """
    dst = Path(tempfile.gettempdir()) / "video_automation-dtd" / src.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        shutil.copyfile(src, dst)
    return dst


def dtd_check(path: Path) -> list[str]:
    """Validate against Final Cut's own DTD via xmllint, if both are present."""
    version = ET.parse(path).getroot().get("version", "")
    dtd = find_dtd(version)
    if dtd is None:
        return [f"note: no local DTD for FCPXML {version}; skipped DTD validation"]
    if shutil.which("xmllint") is None:
        return ["note: xmllint not found; skipped DTD validation"]

    r = subprocess.run(
        ["xmllint", "--noout", "--dtdvalid", str(_staged_dtd(dtd)), str(path)],
        capture_output=True, text=True,
    )
    if r.returncode == 0:
        return []
    return [ln.strip() for ln in r.stderr.splitlines() if ln.strip()][:15]


def parse_time(s: str) -> Fraction:
    """FCPXML rational time -> Fraction of seconds."""
    s = s.strip()
    if not s.endswith("s"):
        raise ValueError(f"malformed time value: {s!r}")
    body = s[:-1]
    if "/" in body:
        num, den = body.split("/")
        return Fraction(int(num), int(den))
    return Fraction(body)


def check(path: Path) -> list[str]:
    problems: list[str] = [p for p in dtd_check(path) if not p.startswith("note:")]
    root = ET.parse(path).getroot()

    if root.tag != "fcpxml":
        problems.append(f"root element is <{root.tag}>, expected <fcpxml>")

    fmt = root.find(".//format")
    frame_dur = parse_time(fmt.get("frameDuration"))
    fps = 1 / frame_dur

    assets = {a.get("id"): a for a in root.findall(".//asset")}
    for aid, a in assets.items():
        rep = a.find("media-rep")
        if rep is None:
            problems.append(f"asset {aid} ({a.get('name')}) has no <media-rep> — imports offline")
            continue
        src = Path(unquote(urlparse(rep.get("src")).path))
        if not src.exists():
            problems.append(f"asset {aid} points at a missing file: {src}")

    spine = root.find(".//spine")
    clips = [c for c in spine if c.tag == "asset-clip"]
    if not clips:
        problems.append("spine contains no asset-clip elements")
        return problems

    seq = root.find(".//sequence")
    seq_dur = parse_time(seq.get("duration")) if seq is not None else None

    expected = Fraction(0)
    for i, c in enumerate(clips):
        off = parse_time(c.get("offset"))
        dur = parse_time(c.get("duration"))
        start = parse_time(c.get("start"))

        if off != expected:
            delta_frames = float((off - expected) * fps)
            problems.append(
                f"clip {i+1} ({c.get('name')}): offset {c.get('offset')} breaks continuity "
                f"by {delta_frames:+.3f} frames"
            )
        expected = off + dur

        # Source range must fit inside the media.
        tm = c.find("timeMap")
        asset = assets.get(c.get("ref"))
        adur = parse_time(asset.get("duration")) if asset is not None else None

        if tm is not None:
            pts = tm.findall("timept")
            if len(pts) < 2:
                problems.append(f"clip {i+1} ({c.get('name')}): timeMap needs at least 2 timepts")
            # A timeMap carries the in-point itself; `start` must be zero or FCP
            # rejects the edit with "Invalid edit with no respective media".
            if start != 0:
                problems.append(
                    f"clip {i+1} ({c.get('name')}): has a timeMap but start={c.get('start')} "
                    f"— must be 0s, the in-point belongs in the first timept"
                )
            times = [parse_time(p.get("time")) for p in pts]
            if times[0] != 0 or times[-1] != dur:
                problems.append(
                    f"clip {i+1} ({c.get('name')}): timeMap spans {float(times[0])}.."
                    f"{float(times[-1])}s but the clip is {float(dur)}s"
                )
            if any(b <= a for a, b in zip(times, times[1:])):
                problems.append(f"clip {i+1} ({c.get('name')}): timeMap times are not increasing")

            # No segment may play slower than real time. Slow motion is a
            # deliberate non-goal, and a ramp that dips below 1.0 anywhere is
            # the exact artefact that made the curves look wrong.
            vals = [parse_time(p.get("value")) for p in pts]
            reverse = len(vals) > 1 and vals[-1] < vals[0]
            for (ta, tb), (va, vb) in zip(zip(times, times[1:]), zip(vals, vals[1:])):
                if tb == ta:
                    continue
                speed = abs(vb - va) / (tb - ta)
                if speed < Fraction(99, 100):
                    problems.append(
                        f"clip {i+1} ({c.get('name')}): timeMap segment at "
                        f"{float(ta):.2f}s plays at {float(speed):.2f}x — slower than real time"
                    )
                    break
            del reverse
            values = [parse_time(p.get("value")) for p in pts]
            if adur is not None and (max(values) > adur or min(values) < 0):
                problems.append(
                    f"clip {i+1} ({c.get('name')}): timeMap reaches source "
                    f"{float(max(values)):.2f}s, media is {float(adur):.2f}s"
                )
        elif adur is not None and start + dur > adur:
            over = float((start + dur - adur) * fps)
            problems.append(
                f"clip {i+1} ({c.get('name')}): source range runs {over:.1f} frames "
                f"past the end of the media"
            )

        # Fractional frames anywhere means FCP will round for us, unpredictably.
        for attr in ("offset", "duration", "start"):
            v = parse_time(c.get(attr)) * fps
            if v.denominator != 1:
                problems.append(f"clip {i+1}: {attr} is not a whole number of frames ({v})")

    # Connected clips express offset in the parent's time base, which begins at
    # the parent's `start` — not at zero. So the timeline position of a
    # connected clip is (its offset - the parent's start), and it is that
    # position, not the raw offset, that has to make sense.
    #
    # This used to require offset == parent start, i.e. every connected clip
    # beginning at timeline zero. That held only while there was exactly one
    # music clip; a looped track has a second pass that is *supposed* to start
    # partway in, and the old rule called the correct output a sync error.
    for i, c in enumerate(clips):
        parent_start = parse_time(c.get("start"))
        connected = [ch for ch in c.findall("asset-clip")
                     if ch.get("lane") is not None]
        for j, child in enumerate(connected):
            pos = parse_time(child.get("offset")) - parent_start
            if pos < 0:
                problems.append(
                    f"connected clip '{child.get('name')}' on clip {i+1}: starts "
                    f"{float(-pos):.3f}s before the timeline"
                )
            elif j == 0 and pos != 0:
                problems.append(
                    f"connected clip '{child.get('name')}' on clip {i+1}: offset "
                    f"{child.get('offset')} != parent start {c.get('start')} — "
                    f"audio will sit {float(pos):.3f}s out of sync"
                )
            if seq_dur is not None and pos + parse_time(child.get("duration")) > seq_dur:
                problems.append(
                    f"connected clip '{child.get('name')}' on clip {i+1}: runs "
                    f"{float(pos + parse_time(child.get('duration')) - seq_dur):.3f}s "
                    f"past the end of the sequence"
                )

        # Two connected clips on one lane may not overlap; a looped track puts
        # its crossfading passes on separate lanes precisely to avoid this.
        by_lane: dict[str, list] = {}
        for child in connected:
            by_lane.setdefault(child.get("lane"), []).append(child)
        for lane, group in by_lane.items():
            spans = sorted((parse_time(ch.get("offset")) - parent_start,
                            parse_time(ch.get("duration")), ch.get("name"))
                           for ch in group)
            for (a0, ad, an), (b0, _, bn) in zip(spans, spans[1:]):
                if b0 < a0 + ad:
                    problems.append(
                        f"connected clips '{an}' and '{bn}' overlap by "
                        f"{float(a0 + ad - b0):.3f}s on lane {lane}"
                    )

    return problems


def summarise(path: Path) -> str:
    root = ET.parse(path).getroot()
    spine = root.find(".//spine")
    clips = [c for c in spine if c.tag == "asset-clip"]
    total = sum(parse_time(c.get("duration")) for c in clips)
    fmt = root.find(".//format")
    return (f"{len(clips)} clips, {float(total):.2f}s timeline, "
            f"{len(root.findall('.//asset'))} assets, "
            f"format {fmt.get('name')} @ {fmt.get('frameDuration')}")
