"""Nebula Pulse, 4-7-8 breathing, 20 minutes — long-form sound therapy.

The bed is "Nebula Pulse", a track from the app's White Noise Therapy album
(tinnitushelp.me/zen/white-noise), back on disk as a ten-minute mp3. The
picture is this video's own look, `StarPulse` in
`tinnitus/session_looks/nebula_pulse_478.py`: stars, teal dust and an amber
core glow that swells on the inhale and holds with the breath.

* **This is a comfort session, not a masking one — measured.** `band_energy`
  over five 30s windows: **<200 Hz 99.7-99.8%, 200 Hz-1 kHz 0.2%, nothing
  above.** It is two tones (~87.6 Hz and ~175 Hz) beating against an 83 Hz
  partner at about 4.3 Hz, which is the "pulse". The album page calls it "a
  smooth white noise base"; the file has none, so the measurement wins
  (`docs/video/projects/tinnitus.md`, "A comfort session is not a masking
  session"). No "set it just below your tinnitus" line, and no denial either:
  the copy says what the sound is and how loud to keep it.
* **4-7-8 kept although a comfort piece usually takes an unnamed pattern** —
  the user asked for it by name. The intro gives the way out of the holds.
* **`inhale=4.0, hold=7.0, exhale=8.0`**, a 19s cycle, **`loop=57.0`** (three
  cycles). 20 minutes: 34s intro, 1140s body (twenty loops), 26s outro.
* **The recording is tiled** (`bed_file_loop=True`): 588s of source under a
  1200s piece. Its own fade-in runs about ten seconds (-52 dB to -21 dB), so
  `TRIM` starts at 12s; it has no fade-out. A steady two-tone drone, so the
  equal-power seam has nothing to hide behind — measured with `seam_drop`.

The caption reads "4-7-8"; the voice does not — the usual `(caption, spoken)`
pair, because espeak reads a bare `4-7-8` as "four dash seven dash eight".

    PYTHONPATH=. .venv/bin/python projects/tinnitus-long/nebula-pulse-478-breathing-20min.py
"""

import subprocess
from pathlib import Path

from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long
from video_automation.longform.thumb import render_session_thumb
from video_automation.tinnitus.session_looks.nebula_pulse_478 import StarPulse

SOURCE_POST = None  # off-site: a sound-therapy session, no article

DESKTOP = Path.home() / "Desktop"
OUT = DESKTOP / "Nebula Pulse + 4-7-8 Breathing for Tinnitus (20 Minutes).mp4"
SOURCE = DESKTOP / "NebulaPulse.mp3"
WORK = Path("/tmp/tinnitus-long-asmr-nebula-pulse-478-20min")
TRIM = (12.0, 600.9)         # past the track's own ten-second fade-in

MINUTES = 20.0
INHALE, HOLD, EXHALE = 4.0, 7.0, 8.0
LOOP = 3 * (INHALE + HOLD + EXHALE)    # 57.0
LOOK = StarPulse

# What the sound is, how loud to keep it, the pattern, and the way out of the
# holds. No masking line: the bed has nothing above 1 kHz to mask with.
INTRO = [
    ("Twenty minutes of Nebula Pulse,",
     "a deep, low hum with a soft pulse.",),
    ("Keep it low and comfortable.",),
    ("Follow the circle:",
     ("4-7-8 breathing.", "four, seven, eight breathing."),
     "Four in, seven hold, eight out.",),
    ("If a hold feels like too much,",
     "let it go and just breathe.",),
]

# Not a subscribe card. A piece built to lower arousal does not end by asking
# for something.
OUTRO = [
    ("That is twenty minutes.",),
    ("If it helped, start it again",
     "and take another round.",),
    ("There are other sounds and patterns",
     "on the channel for when you want them.",),
]


def trimmed_source() -> Path:
    WORK.mkdir(parents=True, exist_ok=True)
    out = WORK.parent / f"{WORK.name}-src.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(TRIM[0]),
                    "-to", str(TRIM[1]), "-i", str(SOURCE), "-ar", "48000",
                    str(out)], check=True)
    return out


if __name__ == "__main__":
    made = render_asmr_long(
        out=OUT,
        workdir=WORK,
        brand=TINNITUS,
        minutes=MINUTES,
        bed_file=trimmed_source(),
        bed_file_loop=True,
        intro=INTRO,
        outro=OUTRO,
        intro_len=34.0,
        outro_len=26.0,
        loop=LOOP,
        inhale=INHALE, hold=HOLD, exhale=EXHALE,
        look=LOOK,
    )
    print(made["video"], f"{made['total']:.0f}s")

    # A still of the same look. Orange on teal, the warm number on a cool
    # field, which also echoes the core glow.
    thumb = render_session_thumb(
        OUT.with_suffix(".jpg"), TINNITUS, minutes=int(MINUTES),
        headline="Nebula Pulse", pattern="4-7-8 breathing",
        accent="orange", look=LOOK)
    print(thumb)
