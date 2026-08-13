"""The music bed, and getting the voice to sit on top of it.

Three minutes of dry narration is a retention problem the shorts never had — at
35 seconds the voice carries itself, and at three it does not. The bed is the
cheapest fix available and the one piece of prior art in this space conspicuously
lacks it.

**The ducking numbers here are not new.** They were measured while building the
tinnitus sound-therapy short and they transfer directly: a bed at `-20 LUFS`
left only 3 dB over the narration and was not intelligible; `-23` with a
sidechain compressor at `threshold=0.03:ratio=8` is the working value. Sidechain
rather than a static mix because the bed should be at full strength wherever
there are no words — under a chapter card, in the pause a checklist buys itself,
over the outro — and step back only where there are.

**Licensing, and it has an edge worth remembering.** The intended source is the
YouTube Audio Library: free, cleared for use in YouTube videos, and that
clearance covers the site embed too because the embed *is* the YouTube player.
It does **not** cover reposting the same cut to TikTok or Instagram. Some tracks
also require attribution — that is per track, and it belongs in the description.
`bed_credit` exists so the metadata sidecar can carry it and nobody has to
remember.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

# Measured, not guessed — see the module docstring.
BED_LUFS = -23
DUCK = "threshold=0.03:ratio=8:attack=15:release=500:makeup=1"

# The bed steps down under a chapter card too, not just under words: a card is
# a punctuation mark and it reads better with the music opening up, which is the
# opposite of ducking. That is why the sidechain key is the voice alone.


def render_bed(track: Path, out: Path, duration: float,
               start: float = 0.0, gain: float = 1.0,
               fade_in: float = 2.0, fade_out: float = 4.0,
               lufs: int = BED_LUFS) -> Path:
    """Trim, loop and normalise a music track to exactly `duration`.

    `aloop` rather than requiring a long enough track: the Audio Library's
    pieces are frequently shorter than three minutes, and a bed that runs out
    two thirds of the way through is worse than no bed. The loop is seamless
    only if the track is; check it by ear once per track, not once per video.

    The fade out is long — four seconds — because it lands under the outro card
    and a bed that stops dead makes the end of the video feel like a dropout.
    """
    filt = (
        f"[0:a]atrim=start={start},asetpts=N/SR/TB,"
        f"aloop=loop=-1:size=2e9,atrim=duration={duration},"
        f"volume={gain},"
        f"loudnorm=I={lufs}:TP=-2:LRA=7,"
        f"afade=t=in:st=0:d={fade_in},"
        f"afade=t=out:st={max(duration - fade_out, 0):.2f}:d={fade_out}[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(track),
                    "-filter_complex", filt, "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(out)],
                   check=True, capture_output=True)
    return out


def mix_voice_over_bed(bed: Path, voice: Path, out: Path,
                       duration: float, voice_at: float = 0.0) -> Path:
    """Lay the narration over the bed, ducking the bed under it."""
    filt = (
        f"[1:a]adelay={int(voice_at * 1000)}|{int(voice_at * 1000)},"
        f"apad=whole_dur={duration}[vo];"
        f"[vo]asplit=2[vo1][key];"
        f"[0:a][key]sidechaincompress={DUCK}[duck];"
        f"[duck][vo1]amix=inputs=2:duration=first:normalize=0,"
        f"alimiter=limit=0.95[out]"
    )
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(bed), "-i", str(voice),
                    "-filter_complex", filt, "-map", "[out]",
                    "-ar", "48000", "-ac", "2", str(out)],
                   check=True, capture_output=True)
    return out


def duration_of(path: Path) -> float:
    """Seconds, via ffprobe. Used to check a bed actually covers the piece."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(out)
