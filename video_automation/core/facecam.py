"""The camera box: Oktay's face in a small rounded box, at chosen moments.

**Built 2026-11-21 for OktAI.** A trust device, not a talking head - it
comes in for the hook, the twist, a personal aside and the last line, and is
off while the viewer has to read a screen (`docs/oktai-channel-plan.md`).

It runs **after** the render, on the finished MP4:

    from video_automation.core import facecam
    facecam.apply(out, out.with_name(out.stem + "-cam.mp4"),
                  edl=Path("~/Movies/oktai/take.ab12cd34.edl.json"),
                  srt=out.with_suffix(".srt"),
                  on=[("the twist line, as it starts", 5.0)])

**Why the edit file.** The voice was cut (`core/recorded.py`): retakes out,
pauses trimmed. The face has to be cut the same way or the lips drift off the
words after the first cut. The EDL says which source second plays at each
output second; a gap that was filled with room tone shows a still frame.

**Only the cue windows are decoded.** The box is on ~20% of the runtime, so
each cue's face clip is cut, cropped and composited (rounded corners, gold
border, soft shadow, a short slide and fade) on its own, small, as an RGBA
clip; the final pass only overlays those. A full-length face track through a
filter graph with a hundred trims would buffer the whole video in memory.

The face is found with OpenCV's frontal-face cascade on a few frames and the
crop centres on it; pass `crop=` (fractions of the source) to override.
"""

from __future__ import annotations

import json
import re
import subprocess
import tempfile
from pathlib import Path

import cv2
import numpy as np

from .brand import OKTAI, Brand

FPS = 30
FADE = 0.28                  # seconds of slide + fade at each end
SLIDE = 36                   # pixels the box travels while it fades
RADIUS = 26
BORDER = 3
SHADOW = 18


def _probe(path: Path) -> tuple[int, int, float]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height:format=duration", "-of", "json", str(path)],
        check=True, capture_output=True, text=True).stdout
    d = json.loads(out)
    s = d["streams"][0]
    return int(s["width"]), int(s["height"]), float(d["format"]["duration"])


# ---------------------------------------------------------------------------
# where the box goes, and when
# ---------------------------------------------------------------------------

def layout(w: int, h: int, corner: str | None = None) -> tuple[int, int, int, int]:
    """(x, y, box_w, box_h) for the frame. Inside every platform's safe box."""
    if h > w:                                     # 9:16 - top right, under the
        bw = bh = 300                             # top band, left of the rail
        x, y = 860 - bw - 24, 268
        if corner == "bl":
            x, y = 58, 1440 - bh - 24
    else:                                         # 16:9 - bottom right
        bw = bh = 320
        x, y = w - bw - 64, 950 - bh - 24
        if corner == "tr":
            y = 62
        elif corner == "bl":
            x = 64
    return x, y, bw, bh


def read_srt(path: Path) -> list[tuple[float, float, str]]:
    def sec(t):
        h, m, s = t.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)
    out = []
    for block in re.split(r"\n\s*\n", Path(path).read_text().strip()):
        lines = block.strip().splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            a, b = [sec(x.strip()) for x in lines[1].split("-->")]
            out.append((a, b, " ".join(lines[2:])))
    return out


def _n(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


def cues(srt: Path, on: list | None = None, hook: float | None = 3.0,
         last: float | None = 4.0) -> list[tuple[float, float]]:
    """Box windows in output seconds, from the captions.

    `hook`: from the first word to the end of the caption that finishes
    nearest `hook` seconds in. `last`: the final `last` seconds of speech.
    `on`: phrases as they start in the captions, each with how long to stay
    (`("this one cost me a week", 4.0)` or just the phrase for 4 s); the end
    snaps to a caption's end so the box never leaves mid-word.
    """
    caps = read_srt(srt)
    if not caps:
        return []
    out = []
    if hook:
        end = min(caps, key=lambda c: abs(c[1] - hook))[1]
        out.append((caps[0][0], max(end, caps[0][1])))
    for item in on or []:
        phrase, secs = (item, 4.0) if isinstance(item, str) else item
        want = _n(phrase)
        hit = None
        for i, (a, b, text) in enumerate(caps):
            joined = _n(" ".join(c[2] for c in caps[i:i + 6]))
            if joined.startswith(want) or (len(want) < 40 and want in _n(text)):
                hit = i
                break
        if hit is None:
            raise ValueError(f"facecam: no caption starts with {phrase!r}")
        a = caps[hit][0]
        b = min((c[1] for c in caps[hit:]), key=lambda e: abs(e - (a + secs)))
        out.append((a, b))
    if last:
        speech_end = caps[-1][1]
        a = next((c[0] for c in caps if c[0] >= speech_end - last), caps[-1][0])
        out.append((a, speech_end))
    out.sort()
    merged = []
    for a, b in out:                     # overlapping or near cues become one
        if merged and a <= merged[-1][1] + 1.0:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]))
        else:
            merged.append((a, b))
    return merged


# ---------------------------------------------------------------------------
# the face
# ---------------------------------------------------------------------------

def find_face(video: Path, at: list[float]) -> tuple[float, float, float] | None:
    """(cx, cy, size) as fractions of the frame, from a few sampled frames."""
    casc = cv2.CascadeClassifier(cv2.data.haarcascades +
                                 "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(str(video))
    hits = []
    for t in at:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, img = cap.read()
        if not ok:
            continue
        H, W = img.shape[:2]
        g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = casc.detectMultiScale(g, 1.1, 6, minSize=(W // 12, W // 12))
        if len(faces):
            x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
            hits.append(((x + w / 2) / W, (y + h / 2) / H, h / H))
    cap.release()
    if not hits:
        return None
    a = np.median(np.array(hits), axis=0)
    return float(a[0]), float(a[1]), float(a[2])


def _crop_box(W: int, H: int, bw: int, bh: int, face) -> tuple[int, int, int, int]:
    """Source crop (x, y, w, h) at the box's aspect, around the face."""
    aspect = bw / bh
    if face is None:                          # centred, full height
        ch = H
        cw = int(ch * aspect)
        if cw > W:
            cw, ch = W, int(W / aspect)
        return (W - cw) // 2, (H - ch) // 2, cw, ch
    cx, cy, size = face
    ch = min(H, int(size * H * 2.4))          # head and shoulders
    cw = int(ch * aspect)
    if cw > W:
        cw, ch = W, int(W / aspect)
    x = int(np.clip(cx * W - cw / 2, 0, W - cw))
    y = int(np.clip(cy * H - ch * 0.45, 0, H - ch))   # eyes a little high
    return x, y, cw, ch


def sync_offset(audio: Path, video: Path, seconds: float = 120.0) -> float:
    """Seconds to add to a time in `audio` to get the same moment in `video`.

    For a voice recorded on a separate mic: the camera's own sound is
    cross-correlated with the mic's, on loudness envelopes at 200 Hz.
    """
    from .recorded import load_audio
    sr, hop = 8000, 40
    def env(p):
        a = load_audio(p, sr)[: int(seconds * sr)]
        n = len(a) // hop
        e = np.sqrt(np.mean(a[: n * hop].reshape(n, hop) ** 2, axis=1))
        e = np.log1p(e * 100)
        return (e - e.mean()) / (e.std() + 1e-9)
    x, y = env(audio), env(video)
    n = 1 << int(np.ceil(np.log2(len(x) + len(y))))
    c = np.fft.irfft(np.fft.rfft(y, n) * np.conj(np.fft.rfft(x, n)), n)
    lag = int(np.argmax(c))
    if lag > n // 2:
        lag -= n
    return lag * hop / sr


# ---------------------------------------------------------------------------
# compositing
# ---------------------------------------------------------------------------

def _chrome(bw: int, bh: int, brand: Brand):
    """Canvas-sized arrays: the box's alpha, the border+shadow layer."""
    pad = SHADOW + SLIDE
    W, H = bw + 2 * pad, bh + 2 * SHADOW
    yy, xx = np.mgrid[0:bh, 0:bw].astype(np.float32)

    def rounded(w, h, r):
        y, x = np.mgrid[0:h, 0:w].astype(np.float32)
        dx = np.maximum(np.maximum(r - x, x - (w - 1 - r)), 0)
        dy = np.maximum(np.maximum(r - y, y - (h - 1 - r)), 0)
        return np.clip(r + 0.5 - np.hypot(dx, dy), 0, 1)

    inner = rounded(bw, bh, RADIUS)
    outer = rounded(bw + 2 * BORDER, bh + 2 * BORDER, RADIUS + BORDER)
    shadow = np.zeros((H, W), np.float32)
    s0 = SHADOW - BORDER
    shadow[s0:s0 + bh + 2 * BORDER, pad - BORDER:pad - BORDER + bw + 2 * BORDER] = outer
    shadow = cv2.GaussianBlur(shadow, (0, 0), SHADOW / 2.2) * 0.55
    ring = np.zeros((H, W), np.float32)
    ring[s0:s0 + bh + 2 * BORDER, pad - BORDER:pad - BORDER + bw + 2 * BORDER] = outer
    return inner, ring, shadow, (W, H, pad)


def _cue_clip(face: Path, pieces: list[tuple[str, float, float]], crop,
              bw: int, bh: int, brand: Brand, out: Path) -> Path:
    """One cue's face, composited onto an RGBA canvas, faded and slid."""
    x, y, cw, ch = crop
    vf = f"crop={cw}:{ch}:{x}:{y},scale={bw}:{bh}:flags=lanczos,fps={FPS}"
    tmp = Path(tempfile.mkdtemp(prefix="facecam-"))
    parts = []
    for k, (kind, s, d) in enumerate(pieces):
        p = tmp / f"p{k:03d}.mp4"
        if kind == "src":
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-t", f"{d:.3f}",
                   "-i", str(face), "-an", "-vf", vf]
        else:                                     # a still frame for d seconds
            cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{s:.3f}", "-i", str(face),
                   "-an", "-vf", f"{vf},trim=end_frame=1,tpad=stop_mode=clone:"
                   f"stop_duration={d:.3f}", "-t", f"{d:.3f}"]
        subprocess.run(cmd + ["-c:v", "libx264", "-crf", "12", "-pix_fmt",
                              "yuv420p", str(p)], check=True, capture_output=True)
        parts.append(p)
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))

    inner, ring, shadow, (W, H, pad) = _chrome(bw, bh, brand)
    reader = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-r", str(FPS), "-"],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    writer = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "png",
         str(out)], stdin=subprocess.PIPE)
    total = sum(d for _, _, d in pieces)
    n_total = int(round(total * FPS))
    gold = np.array(brand.primary, np.float32)
    size = bw * bh * 3
    i = 0
    while True:
        buf = reader.stdout.read(size)
        if len(buf) < size:
            break
        img = np.frombuffer(buf, np.uint8).reshape(bh, bw, 3).astype(np.float32)
        t = i / FPS
        k = min(1.0, t / FADE, max(0.0, (total - t) / FADE))
        k = 0.5 - 0.5 * np.cos(np.pi * k)          # ease
        off = int(round((1 - k) * SLIDE))
        # Black shadow, the gold ring over it, the face inside the ring; the
        # whole box shifted right by `off` and faded by `k` while it enters.
        ring_s = np.roll(ring, off, axis=1)
        rgb = gold * ring_s[..., None]
        alpha = np.maximum(np.roll(shadow, off, axis=1), ring_s)
        y0, x0 = SHADOW, pad + off
        a = inner[..., None]
        rgb[y0:y0 + bh, x0:x0 + bw] = rgb[y0:y0 + bh, x0:x0 + bw] * (1 - a) + img * a
        alpha[y0:y0 + bh, x0:x0 + bw] = np.maximum(alpha[y0:y0 + bh, x0:x0 + bw], inner)
        rgba = np.dstack([np.clip(rgb, 0, 255), np.clip(alpha * k * 255, 0, 255)])
        writer.stdin.write(rgba.astype(np.uint8).tobytes())
        i += 1
        if i >= n_total:
            break
    # The concat can run a frame or two past the cue; those are not wanted.
    reader.kill()
    reader.stdout.close()
    reader.wait()
    writer.stdin.close()
    if writer.wait():
        raise RuntimeError(f"facecam: writing {out} failed")
    for p in parts:
        p.unlink(missing_ok=True)
    lst.unlink(missing_ok=True)
    tmp.rmdir()
    return out


def _pieces(segments: list[dict], a: float, b: float, offset: float):
    """The face-video ranges that play between output seconds a and b."""
    out = []
    srcs = [s for s in segments if not s.get("gap")]
    for seg in segments:
        s0, s1 = seg["out"], seg["out"] + seg["dur"]
        lo, hi = max(a, s0), min(b, s1)
        if hi - lo < 1 / FPS:
            continue
        if seg.get("gap"):
            nxt = next((s for s in srcs if s["out"] >= s1 - 1e-3), None)
            prv = [s for s in srcs if s["out"] + s["dur"] <= s0 + 1e-3]
            at = nxt["src"] if nxt else (prv[-1]["src"] + prv[-1]["dur"] - 0.05
                                         if prv else 0.0)
            out.append(("still", at + offset, hi - lo))
        else:
            out.append(("src", seg["src"] + (lo - s0) + offset, hi - lo))
    return out


def apply(video: Path, out: Path, edl: Path, srt: Path | None = None,
          cue_list: list[tuple[float, float]] | None = None,
          on: list | None = None, hook: float | None = 3.0,
          last: float | None = 4.0, corner: str | None = None,
          crop: tuple[float, float, float] | None = None,
          offset: float | None = None, brand: Brand = OKTAI) -> Path:
    """Overlay the camera box on a finished render.

    `cue_list` (output seconds) wins over the caption-derived `cues()`.
    `offset`: face-video time minus recording time; None = 0 when the face
    and voice are one file, else measured with `sync_offset`.
    """
    video, out, edl = Path(video), Path(out), Path(edl).expanduser()
    plan = json.loads(edl.read_text())
    face = Path(plan["face"]) if plan.get("face") else None
    if face is None:
        raise ValueError("facecam: this recording has no face video - pass "
                         "Recording(audio, video=...) when building")
    if offset is None:
        offset = 0.0 if face == Path(plan["audio"]) else sync_offset(
            Path(plan["audio"]), face)
        print(f"facecam: face offset {offset:+.3f}s")
    W, H, dur = _probe(video)
    x, y, bw, bh = layout(W, H, corner)
    windows = cue_list if cue_list is not None else cues(
        srt or video.with_suffix(".srt"), on, hook, last)
    if not windows:
        raise ValueError("facecam: no cue windows")

    fw, fh, fdur = _probe(face)
    if crop is None:
        srcs = [s["src"] + offset for s in plan["segments"] if not s.get("gap")]
        sample = [srcs[int(k * (len(srcs) - 1) / 4)] + 0.5 for k in range(5)] if srcs else [1.0]
        found = find_face(face, sample)
        print("facecam: face", "found" if found else "not found, centre crop")
    else:
        found = crop
    box_crop = _crop_box(fw, fh, bw, bh, found)

    work = Path(tempfile.mkdtemp(prefix="facecam-cues-"))
    clips = []
    for k, (a, b) in enumerate(windows):
        a, b = max(0.0, a - 0.1), min(dur, b + 0.2)
        pieces = _pieces(plan["segments"], a, b, offset)
        if not pieces:
            continue
        clip = _cue_clip(face, pieces, box_crop, bw, bh, brand,
                         work / f"cue{k:02d}.mov")
        clips.append((a, clip))

    pad = SHADOW + SLIDE
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(video)]
    for a, clip in clips:
        cmd += ["-itsoffset", f"{a:.3f}", "-i", str(clip)]
    chain, last_lbl = [], "0:v"
    for k in range(len(clips)):
        lbl = f"v{k}"
        chain.append(f"[{last_lbl}][{k + 1}:v]overlay=x={x - pad}:y={y - SHADOW}"
                     f":eof_action=pass:format=auto[{lbl}]")
        last_lbl = lbl
    cmd += ["-filter_complex", ";".join(chain), "-map", f"[{last_lbl}]",
            "-map", "0:a?", "-c:a", "copy", "-c:v", "libx264", "-crf", "17",
            "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(out)]
    subprocess.run(cmd, check=True)
    for _, clip in clips:
        clip.unlink(missing_ok=True)
    work.rmdir()
    print(f"facecam: {len(clips)} cue(s) -> {out}")
    return out
