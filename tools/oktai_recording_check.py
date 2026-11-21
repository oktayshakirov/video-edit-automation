"""Is this recording good enough to build from? Run it on a test take first.

    PYTHONPATH=. .venv/bin/python tools/oktai_recording_check.py FILE [CAMERA_FILE]

Says, in plain words, what to fix before reading a whole script:

* **Level** - the speech's own loudness and peak. Too quiet means noise is
  lifted with it when it is levelled to -14 LUFS; a peak at 0 dBFS is
  clipping, which no clean-up removes.
* **Noise** - the room between sentences (the quietest half second) against
  the speech: the gap is the signal-to-noise ratio. Under ~35 dB a fan, a
  fridge or the street is audible once the voice is levelled.
* **Echo** - how long the voice rings after a sentence stops (energy decay
  over the first 300 ms of each pause). A bare room rings; clothes,
  curtains and a bed nearby stop it.
* **Camera** (a video file, or the second argument) - resolution, frame
  rate, whether a face is found, where it sits, and how bright it is.

Thresholds are from podcast practice (-16 to -20 LUFS raw speech, 40 dB SNR
good, 30 dB the floor), not measured on our own recordings yet - adjust them
when the first real takes come in.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from video_automation.core.recorded import SR, load_audio  # noqa: E402


def db(x: float) -> float:
    return 20 * np.log10(max(x, 1e-9))


def loudness(path: Path) -> tuple[float, float]:
    """Integrated LUFS and true peak, from ffmpeg's ebur128."""
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-vn",
                          "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    summary = out[out.rfind("Summary:"):]
    lufs = peak = float("nan")
    for line in summary.splitlines():
        line = line.strip()
        if line.startswith("I:"):
            lufs = float(line.split()[1])
        if line.startswith("Peak:"):
            peak = float(line.split()[1])
    return lufs, peak


def frames(a: np.ndarray, win: float = 0.05) -> np.ndarray:
    n = int(win * SR)
    k = len(a) // n
    return np.sqrt(np.mean(a[: k * n].reshape(k, n) ** 2, axis=1) + 1e-12)


def audio_report(path: Path) -> list[tuple[str, str, str]]:
    a = load_audio(path)
    rows = []
    secs = len(a) / SR
    lufs, peak = loudness(path)
    rows.append(("length", f"{secs:.1f}s", "ok" if secs >= 10 else
                 "short - record at least 20-30 s for a fair test"))

    if lufs < -30:
        verdict = "too quiet - move the mic closer or raise its gain"
    elif lufs > -10:
        verdict = "very loud - lower the gain a little"
    else:
        verdict = "ok"
    rows.append(("loudness", f"{lufs:.1f} LUFS", verdict))
    rows.append(("peak", f"{peak:.1f} dBTP",
                 "CLIPPING - lower the mic gain and record again" if peak > -0.5
                 else "ok" if peak > -20 else "low"))

    e = frames(a)
    noise = np.percentile(e, 5)
    speech = np.percentile(e, 90)
    snr = db(speech) - db(noise)
    rows.append(("room noise", f"{db(noise):.0f} dBFS",
                 "ok" if db(noise) < -55 else
                 "audible - turn off fans, close the window, mic closer"))
    rows.append(("voice over noise", f"{snr:.0f} dB",
                 "good" if snr >= 40 else "ok" if snr >= 30 else
                 "too noisy - the room will be heard under the voice"))

    # Echo: in each pause that follows speech, how fast does energy fall?
    loud = e > noise * 10
    decays = []
    for i in range(2, len(e) - 6):
        if loud[i - 1] and not loud[i] and not loud[i + 1:i + 6].any():
            drop = db(e[i - 1]) - db(e[i + 5])          # over 300 ms
            decays.append(drop)
    if decays:
        d = float(np.median(decays))
        rows.append(("echo", f"{d:.0f} dB drop in 0.3 s",
                     "dry - good" if d >= 30 else "some room sound - ok"
                     if d >= 20 else "echoey - add soft things around you"))
    return rows


def video_report(path: Path) -> list[tuple[str, str, str]]:
    from video_automation.core import facecam
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                          "-show_entries", "stream=width,height,r_frame_rate",
                          "-of", "json", str(path)],
                         capture_output=True, text=True).stdout
    streams = json.loads(out or "{}").get("streams") or []
    if not streams:
        return [("camera", "no video", "audio only - no camera box")]
    s = streams[0]
    w, h = int(s["width"]), int(s["height"])
    num, den = (int(x) for x in s["r_frame_rate"].split("/"))
    fps = num / den if den else 0
    rows = [("camera", f"{w}x{h} at {fps:.0f} fps",
             "ok" if min(w, h) >= 720 else "low resolution - 1080p if you can")]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                "format=duration", "-of", "csv=p=0", str(path)],
                               capture_output=True, text=True).stdout or 0)
    at = [dur * k / 6 for k in range(1, 6)]
    face = facecam.find_face(path, at)
    if face is None:
        rows.append(("face", "not found", "face the camera, light from the front"))
        return rows
    cx, cy, size = face
    rows.append(("face", f"centre {cx:.2f},{cy:.2f}, {size:.0%} of the height",
                 "ok" if 0.12 <= size <= 0.6 else
                 "too small - sit closer" if size < 0.12 else
                 "very close - the box crops head and shoulders"))
    import cv2
    cap = cv2.VideoCapture(str(path))
    cap.set(cv2.CAP_PROP_POS_MSEC, at[2] * 1000)
    ok, img = cap.read()
    cap.release()
    if ok:
        H, W = img.shape[:2]
        x0, y0 = int((cx - size / 3) * W), int((cy - size / 3) * H)
        x1, y1 = int((cx + size / 3) * W), int((cy + size / 3) * H)
        patch = cv2.cvtColor(img[max(0, y0):y1, max(0, x0):x1], cv2.COLOR_BGR2GRAY)
        lum = float(patch.mean()) if patch.size else 0.0
        rows.append(("face light", f"{lum:.0f}/255",
                     "too dark - light from the front, a window or a lamp"
                     if lum < 70 else "very bright - soften the light"
                     if lum > 210 else "ok"))
    return rows


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    voice = Path(argv[0]).expanduser()
    cam = Path(argv[1]).expanduser() if len(argv) > 1 else voice
    rows = audio_report(voice) + video_report(cam)
    width = max(len(r[0]) for r in rows)
    bad = 0
    for name, value, verdict in rows:
        flag = " " if verdict.startswith(("ok", "good", "dry")) else "!"
        bad += flag == "!"
        print(f"{flag} {name:<{width}}  {value:<28} {verdict}")
    print("\nReady to record." if not bad else f"\n{bad} thing(s) to fix first.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
