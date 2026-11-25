"""A narration the editor recorded, in place of a synthesised one.

**Built 2026-11-21 for OktAI**, the channel Oktay presents himself. Every
other format speaks its script with Kokoro, and the whole engine is timed off
what `voiceover.build_narration_aligned` returns: one track, one `Caption` per
script chunk, the total length. This returns exactly that triple from a
recording, so the long form, the Short, the beats, the captions and the mix
need no other change:

    from video_automation.core.recorded import Recording
    render_long(SECTIONS, out, work, brand=OKTAI,
                voice=Recording(Path("~/Movies/oktai/pipeline-long.mov")))

## What happens to the recording

1. **Transcribed word by word** with timestamps (`transcribe`): Whisper large
   v3 turbo on MLX, run offline. The model and `mlx_whisper` live in
   `create-song-automation`'s venv - installing them here would pull torch,
   ~2.5 GB, into a venv that was kept free of it on purpose (`voice.md`). So
   it runs as a subprocess of that interpreter (`WHISPER_PYTHON` overrides
   it), and the result is cached by the file's hash. The file goes in as
   pieces cut at pauses, and any stretch of speech Whisper left without
   words is read again (`_pieces`, `_WHISPER`): on a whole eleven-minute
   file it skipped a retake and the last line.
2. **Matched to the script** (`align`). Each sentence is searched for in the
   transcript, every take of it is a candidate, and one take per sentence is
   chosen in script order. **The last good take wins**: the way to fix a
   stumble while recording is to say the sentence again, and that is the
   take that is kept. False starts, re-reads and anything not in the script
   between takes are cut. A first or last word Whisper misheard ("Cloud" for
   "Claude") stays in (`_edges`). A stumble *inside* a read is spliced out:
   both parts of the sentence are kept and the words between them cut
   (`_trim`, `_junk`).
3. **Cut and joined** (`_assemble`). Consecutive sentences from one take keep
   the real pause between them - that is the human prosody a synthesised read
   never had - capped at `max_pause`. Where a retake was cut out, the join
   gets the scripted gap, filled with the recording's own room tone rather
   than digital silence, which would sound like a dropout. A long pause
   *inside* a sentence is shortened (`_tighten`, `inner_pause`), and every
   gap between words is room tone, not the breath or click that was in it
   (`clean_gaps`). Then the cut is listened to: transcribed on its own, a
   phrase it holds that the script does not is a stumble Whisper hid - each
   way of cutting it is built and heard, and the best kept (`_extra_words`,
   `_choose_cut`). Last, the speech is sped up to `target_wpm`, pitch kept
   (`_speed_up`).
4. **Cleaned and levelled** (`clean_chain`): a high-pass, a de-noise set from
   the room's own level, a small presence lift, de-ess, gentle compression,
   and `loudnorm` to -14 LUFS - where the Kokoro narrations measure, so the
   bed and the sidechain behave exactly as they do now.

## What it writes next to the recording

- `NAME.report.txt` - per sentence: the take used, what was said that the
  script does not have, and what the script has that was not said. **Read it
  before the build is reviewed**: a word the editor changed while reading is
  in the voice and not in the captions until the script is changed to match.
- `NAME.edl.json` - the edit: which source seconds went where. The camera
  box (`core/facecam.py`) cuts the face video with it, so the lips match the
  voice that was kept.

`NAME` is the recording's name plus the script's hash, so a long form and its
Short recorded into one file each get their own.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SR = 48000
CACHE = Path(os.environ.get("VIDEO_AUTOMATION_TRANSCRIPTS",
                            Path.home() / ".cache/video-automation/transcripts"))
WHISPER_PYTHON = Path(os.environ.get(
    "WHISPER_PYTHON",
    Path.home() / "Coding/create-song-automation/.venv/bin/python"))
WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"

# The clean-up chain. Light on purpose: a home recording should sound like a
# person in a room, not like a processed voice.
#
# **The de-noiser is set from the room, not fixed (2026-11-22, the first
# OktAI recording).** It was `afftdn=nf=-25`: a noise floor of -25 dB, for a
# room at -62. Measured on that recording it took 5 dB off everything from
# 4 to 8 kHz and 9 dB above 8 kHz - the consonants that make a voice clear -
# while the room was already quiet. Now the floor is the recording's own
# (`_floor_db`, plus a margin) and the reduction a gentle 8 dB; a small lift
# at 3 kHz keeps the words in front of the music bed.
#
# **The voice is matched to the channel's, and sits lower (2026-11-22, his
# note on the first Short: "the voice is too loud, doesn't really fit that
# well, need some equalizing").** Against `noah`, the voice the mixes were
# tuned around, his read had 3-6 dB more boom and mud (100-400 Hz) and 6-10
# dB less presence (2.5-6.5 kHz): heavy enough to sound loud and to fight
# the bed. `match_eq` measures each recording's long-term spectrum and moves
# it 60 % of the way to `TARGET_LTASS`, never more than 4 dB a band - a
# person still, just sitting where the mix expects a voice. The level is
# `Recording.loudness`, 4 dB under the Kokoro reads, set in one step with
# no compressor (`clean_chain`).

# Third-octave bands, 100 Hz to 10 kHz, and `noah`'s long-term spectrum in
# them (dB, relative to its own mean), measured 2026-11-22 on four of the
# OktAI opener's example clips.
LTASS_BANDS = [100 * 2 ** (k / 3) for k in range(21)]
NOAH_LTASS = [14.5, 13.8, 12.7, 5.8, 9.3, 8.4, 9.3, 10.0, 6.1, 2.7, -2.8,
              -4.5, -5.8, -9.5, -7.8, -4.2, -4.9, -9.4, -7.5, -14.6, -21.8]
# **The target is a creator's voice, not `noah` (2026-11-24, his pick of four
# samples: "new tone sounds the best, better than the original").** Aimed at
# the bright synthetic voice, his read came out 8-11 dB hotter at 3-5 kHz
# than a voice recorded by a person - "very punchy, maybe even loud". This
# is the long-term spectrum of the reference video he sent (a creator's
# Claude Code tutorial), measured in the same bands; matched 80 %, 6 dB a
# band at most (0.6 / 4 dB toward `noah` until 2026-11-24).
TARGET_LTASS = [3.83, 9.85, 11.86, 12.02, 11.43, 11.14, 13.61, 12.84, 10.15, 6.5,
                1.44, -0.45, -2.37, -6.29, -7.56, -10.27, -14.46, -14.44, -13.95,
                -14.2, -20.68]
EQ_STRENGTH = 0.8
EQ_MAX = 6.0


def ltass(audio: np.ndarray, sr: int = SR) -> np.ndarray:
    """Long-term spectrum of the speech in `audio`, per `LTASS_BANDS`, dB
    relative to its own mean."""
    hop = sr // 100
    n = len(audio) // hop
    db = 10 * np.log10((audio[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    loud = np.where(db > db.max() - 30)[0]
    seg = np.concatenate([audio[i * hop:(i + 1) * hop] for i in loud])
    N = 8192
    w = np.hanning(N)
    P = np.zeros(N // 2 + 1)
    for k in range(0, max(1, len(seg) - N), N // 2):
        chunk = seg[k:k + N]
        if len(chunk) == N:
            P += np.abs(np.fft.rfft(chunk * w)) ** 2
    f = np.fft.rfftfreq(N, 1 / sr)
    out = np.array([P[(f >= c / 2 ** (1 / 6)) & (f < c * 2 ** (1 / 6))].mean()
                    for c in LTASS_BANDS])
    out = 10 * np.log10(out + 1e-20)
    return out - out.mean()


def eq_gains(audio: np.ndarray, sr: int = SR) -> np.ndarray:
    """dB per `LTASS_BANDS` that moves this voice toward `TARGET_LTASS`."""
    def smooth(x):
        return np.convolve(np.pad(np.asarray(x, float), 1, mode="edge"),
                           np.ones(3) / 3, mode="valid")
    diff = smooth(TARGET_LTASS) - smooth(ltass(audio, sr))
    diff -= diff[6:14].mean()           # the mids (400 Hz - 2 kHz) stay put
    return np.clip(EQ_STRENGTH * diff, -EQ_MAX, EQ_MAX)


def match_eq(audio: np.ndarray, sr: int = SR) -> str:
    g = eq_gains(audio, sr)
    entries = ";".join(f"entry({c:.0f},{x:.2f})" for c, x in zip(LTASS_BANDS, g))
    return f"firequalizer=gain_entry='entry(20,{g[0]:.2f});{entries};entry(20000,{g[-1]:.2f})'"


# **What the reference showed (2026-11-24).** The editor: "my voice sounds
# very punchy, maybe even loud, and reverb in it". Against his reference
# video (mids level): 11-20 dB more at 100-130 Hz (his close-mic boom and
# his pitch), 8-11 dB more at 3-5 kHz, the bed ~7 dB higher under the voice,
# and words that died away 11 dB in 20-50 ms where the reference's die
# 26 dB: the room. He chose the new tone and the lower bed, without the
# de-reverb below (samples on his Desktop, `voice-samples/`); it is kept
# for a room that needs it.


def dereverb(x: np.ndarray, t60: float = 0.45, delay: float = 0.05,
             floor_db: float = -15.0, sr: int = SR) -> np.ndarray:
    """The room's tail taken out of a voice: late-reverberation spectral
    subtraction (Lebart, Boucher and Denbigh, 2001), plain numpy.

    The power of the tail at a moment is the signal's power `delay` earlier,
    decayed at the room's `t60`; that much is subtracted from each frequency,
    never more than `floor_db`, the gain smoothed over 5 bins and 3 frames
    so it does not warble. On the OktAI take (prepared 2026-11-24): a word's
    tail 20-50 ms after it ends went from 11 dB under the word to 21 dB
    (t60 0.45, floor -15) or 23 dB (0.6, -20) - the reference sits at 26 -
    with Whisper hearing the words as well as before. Compression does the
    opposite: it lifts tails (11 -> 9 dB), so the new chain has none.
    """
    from scipy.ndimage import uniform_filter
    from scipy.signal import istft, stft
    nper, hop = 1024, 256
    _, _, X = stft(x, sr, nperseg=nper, noverlap=nper - hop)
    P = np.abs(X) ** 2
    Ps = P.copy()
    for k in range(1, P.shape[1]):
        Ps[:, k] = 0.6 * P[:, k] + 0.4 * Ps[:, k - 1]
    d = max(1, int(round(delay * sr / hop)))
    late = np.zeros_like(Ps)
    late[:, d:] = np.exp(-6.9 * 2 * d * hop / sr / t60) * Ps[:, :-d]
    g = np.maximum(1 - late / (Ps + 1e-12), 10 ** (floor_db / 10))
    g = uniform_filter(g, size=(5, 3))
    _, y = istft(X * np.sqrt(g), sr, nperseg=nper, noverlap=nper - hop)
    return y[:len(x)].astype(x.dtype if x.dtype.kind == "f" else np.float32)


PICKUP_EQ_MAX = 6.0   # dB a pickup's band may move toward the take's


def match_pickups(audio: np.ndarray, at: float, sr: int = SR) -> np.ndarray:
    """`audio` with everything after `at` - the pickups joined on the end -
    shaped and levelled to sound like what comes before it.

    **Why (2026-11-24, the editor on the pickups: "try to make the pickup
    voice match the first one").** The pickups were read a day later in
    another room: against the take, measured, they had 1-2 dB more low end
    (100-500 Hz), 2-5 dB less at 1.2-3 kHz and 5 dB more air at 10 kHz -
    another mic distance and another wall. One EQ for the whole file
    (`match_eq`) cannot fix a difference *inside* it. So the pickups get the
    take's long-term spectrum (`ltass`), band by band, at full strength but
    never more than `PICKUP_EQ_MAX`, as a linear-phase FIR, and the take's
    speech level; then the whole goes through the chain as one voice.
    """
    from scipy.signal import fftconvolve, firwin2
    k = int(at * sr)
    if k <= sr or len(audio) - k <= sr:
        return audio
    ref, pk = audio[:k], audio[k:].astype(np.float64)
    diff = ltass(ref, sr) - ltass(pk, sr)
    diff = np.convolve(np.pad(diff, 1, mode="edge"), np.ones(3) / 3, mode="valid")
    diff = np.clip(diff - diff[6:14].mean(), -PICKUP_EQ_MAX, PICKUP_EQ_MAX)
    freqs = [0.0, 50.0] + list(LTASS_BANDS) + [16000.0, sr / 2]
    gains = [diff[0], diff[0]] + list(diff) + [diff[-1], diff[-1]]
    fir = firwin2(2047, freqs, 10 ** (np.array(gains) / 20), fs=sr)
    shaped = fftconvolve(pk, fir, mode="same")

    def speech_db(x):
        hop = sr // 100
        n = len(x) // hop
        db = 10 * np.log10((x[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
        loud = db[db > db.max() - 30]
        return 10 * np.log10(np.mean(10 ** (loud / 10)))
    shaped *= 10 ** ((speech_db(ref) - speech_db(shaped)) / 20)
    return np.concatenate([ref, shaped.astype(ref.dtype)])


def speech_db(audio: np.ndarray, sr: int = SR) -> float:
    """The level of the speech in `audio`: its loud 10 ms frames, averaged in
    power (dBFS)."""
    hop = sr // 100
    n = len(audio) // hop
    db = 10 * np.log10((audio[:n * hop].reshape(n, hop).astype(np.float64) ** 2).mean(axis=1) + 1e-12)
    loud = db[db > db.max() - 30]
    return float(10 * np.log10(np.mean(10 ** (loud / 10))))


def clean_chain(floor_db: float, eq: str | None = None,
                speech: float | None = None) -> str:
    """The ffmpeg filter chain that shapes a recording whose room sits at
    `floor_db`. The level is set after it, in one step (`_level`).

    **No compressor (2026-11-22, his second note: "my voice is very quiet but
    loud, as if I'm too close to the mic").** That is what a close mic plus
    compression sounds like: the proximity boom, and every breath and mouth
    sound pulled up to the level of the words. So the low end gets a further
    shelf on top of `match_eq`, breaths between phrases are lowered softly
    (a 6 dB downward expander set from the room), and the voice keeps its own
    dynamics: one gain for the whole read and a limiter for the odd peak,
    where `loudnorm` used to ride the level line by line.
    """
    nf = int(max(-80, min(-20, round(floor_db + 6))))
    # **Just over the room, not over the breaths (2026-11-23).** The gaps
    # are room tone now (`clean_gaps`), so the expander only has to keep the
    # room down; at +26 dB it also held back a soft first syllable ("AI")
    # and every final "s". The de-esser is lighter for the same "s".
    gate = 10 ** ((floor_db + 14) / 20)
    # **The new tone (2026-11-24, his pick):** 24 dB an octave under 100 Hz
    # and 3 dB off around 200 Hz for the close mic's boom (it was a 90 Hz
    # high-pass and a 160 Hz shelf), a firmer de-esser, a peak catcher 10.5
    # dB over the speech - it touches plosives, not words, so it does not
    # lift the room's tail - and a faster expander release (200 -> 90 ms).
    comp = (f"acompressor=threshold={10 ** ((speech + 10.5) / 20):.5f}:ratio=2.5"
            ":attack=8:release=150:knee=6:makeup=1") if speech is not None else None
    return ",".join(x for x in (
        "highpass=f=100:poles=2",
        "highpass=f=100:poles=2",
        "equalizer=f=200:t=o:w=1.2:g=-3",
        f"afftdn=nr=8:nf={nf}",
        eq,
        "deesser=i=0.3",
        comp,
        f"agate=threshold={gate:.5f}:range=0.4:ratio=2:attack=5:release=90",
    ) if x)


def _level(src: Path, dst: Path, chain: str, target: float) -> None:
    """`chain`, then one gain to `target` LUFS and a -2 dBTP limiter."""
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(src), "-af",
         ",".join(x for x in (chain, "loudnorm=print_format=json") if x),
         "-f", "null", "-"], capture_output=True, text=True, check=True).stderr
    m = json.loads(re.findall(r"\{[^{}]*\}", probe)[-1])
    gain = target - float(m["input_i"])
    tail = f"volume={gain:.2f}dB,alimiter=limit=0.79:attack=5:release=60:level=disabled"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
                    ",".join(x for x in (chain, tail) if x),
                    "-ar", str(SR), "-ac", "2", str(dst)],
                   check=True, capture_output=True)

MATCH = 0.78          # two words are "the same" at this difflib ratio or above
MIN_SCORE = 0.55      # a take must match at least this share of its sentence
LATER = 0.30          # how much the latest take is preferred over the first
GOOD = 0.75           # ...when it matches at least this share of the sentence
LONG_GAP = 1.0        # a scripted gap this long is silence, even inside one take


class Pause(float):
    """A scripted gap shorter than `LONG_GAP` that is still a written pause:
    `Pause(0.7)` is 0.7 s of room tone between two lines read in one breath
    (2026-11-25, the slop list: 1.0 s after "the same stock clips" was "too
    big", the natural 0.4 too little for the card to be read)."""


def _written(g: float) -> bool:
    return isinstance(g, Pause) or g >= LONG_GAP
PRE = 0.06            # seconds kept before a sentence's first word
POST = 0.20           # ...and after its last, for the release of the word
                      # (0.14 clipped a final "s", 2026-11-23)
FADE = 0.010


@dataclass
class Recording:
    """The voice to use, and optionally the face to go with it.

    `audio` may be a WAV, M4A, MP3 or a video file (its audio is used).
    `video` is the face recording for the camera box; leave it None when the
    face is in `audio`'s own file, or there is no face. `window` limits the
    search to a stretch of the file, in seconds - for one file holding both
    the long form's and the Short's scripts, when the two share sentences.
    """

    audio: Path
    video: Path | None = None
    window: tuple | list | None = None    # (start, end) or a list of them
    max_pause: float = 0.75       # longest natural pause kept between sentences
    # A pause inside a sentence longer than `inner_pause` is cut to
    # `inner_keep` (`_tighten`); None keeps every pause as read.
    inner_pause: float | None = 0.45
    inner_keep: float = 0.28
    # Check every cut on the take transcribed alone (`_refine`).
    refine: bool = True
    # Room tone between the words, in place of breaths and clicks
    # (`clean_gaps`).
    gaps_clean: bool = True
    # Rounds of listening to the cut and cutting what the script lacks
    # (`_extra_words`); 0 to skip. `extra` lists what was cut.
    check_rounds: int = 3
    extra: list = field(default_factory=list, init=False)
    # Integrated loudness of the cleaned voice, and whether its tone is
    # matched to the channel's voice (`match_eq`).
    loudness: float = -18.0
    match: bool = True
    # How much faster the speech plays (`_speed_up`, pitch kept). With
    # `target_wpm`, the speed is whatever brings this read to that many
    # words a minute, within `SPEED_RANGE`.
    speed: float = 1.0
    target_wpm: float | None = None
    applied_speed: float = field(default=1.0, init=False)
    clean: bool = True
    # Set by the build: where this recording's edit file and report went,
    # so the camera box can find the edit without recomputing its name.
    edl: Path | None = field(default=None, init=False)
    report: Path | None = field(default=None, init=False)
    captions: list | None = field(default=None, init=False, repr=False)
    # (start, end) of each sentence's speech in the output, in seconds.
    sentence_times: list | None = field(default=None, init=False, repr=False)
    # The editor's pick: a sentence (as written) -> (start, end) seconds of
    # the recording to use for it, whole, when the matching chose wrong. A
    # read broken off and said again whole ("AI tools love... AI tools love
    # stock footage") came back spliced from both, "love" twice (2026-11-23).
    pins: dict = field(default_factory=dict)
    # Source ranges (seconds) cut out of whatever take holds them: a word he
    # said that the video should not ("Now it's hands, screens and drawings"
    # - there are no hands on screen, 2026-11-23). The sentence keeps what
    # he said as its spoken half, so it still matches; its caption drops it.
    drops: list = field(default_factory=list)
    # Where lines read again or added after the take begin, when they are
    # joined on its end (`oktai.recording`): a good read there wins.
    pickups_from: float | None = None
    # Where the pickups start in the file, whatever the matching does: from
    # there on the voice is shaped to the take's (`match_pickups`).
    pickups_at: float | None = None

    def __post_init__(self):
        self.audio = Path(self.audio).expanduser()
        if self.video is not None:
            self.video = Path(self.video).expanduser()

    @property
    def face(self) -> Path | None:
        if self.video is not None:
            return self.video
        return self.audio if _has_video(self.audio) else None


# ---------------------------------------------------------------------------
# transcription
# ---------------------------------------------------------------------------

def _has_video(path: Path) -> bool:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries",
         "stream=codec_type", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True).stdout
    return "video" in out


def _hash(path: Path) -> str:
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()[:16]


def load_audio(path: Path, sr: int = SR) -> np.ndarray:
    """Mono float32 at `sr`, from any file ffmpeg can read."""
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1",
         "-ar", str(sr), "-f", "f32le", "-"],
        check=True, capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


_WHISPER = r"""
import json, sys
import numpy as np
import mlx_whisper
from mlx_whisper.audio import load_audio
SR = 16000
HOP = SR // 20
audio = load_audio(sys.argv[1])
fr = audio[:len(audio) // HOP * HOP].reshape(-1, HOP)
db = 10 * np.log10((fr ** 2).mean(axis=1) + 1e-12)
loud = db > np.percentile(db, 10) + 20          # speech, 20 dB over the room

DET = len(sys.argv) > 4 and sys.argv[4] == "det"

def heard(a, b):
    kw = {"temperature": 0.0} if DET else {}
    r = mlx_whisper.transcribe(audio[a:b], path_or_hf_repo=sys.argv[2],
                               word_timestamps=True, language="en",
                               condition_on_previous_text=False, **kw)
    off = a / SR
    return r["text"].strip(), [
        {"w": w["word"], "s": w["start"] + off, "e": w["end"] + off,
         "p": w.get("probability", 1.0)}
        for seg in r["segments"] for w in seg.get("words", [])]

def holes(ws, a, b):
    # Loud stretches of [a, b) no word covers, as (from, to) samples between
    # the words around them. A "word" Whisper stretched over seconds (one
    # "were" ran eight, over a whole re-read it never wrote) counts as one
    # second long, so what it hides is read again.
    edges = [a / SR] + [t for w in ws for t in (w["s"], min(w["e"], w["s"] + 1.0))] + [b / SR]
    out = []
    for k in range(0, len(edges), 2):
        lo, hi = edges[k], edges[k + 1]
        i0, i1 = int((lo + 0.3) * SR) // HOP, int((hi - 0.3) * SR) // HOP
        if i1 > i0 and loud[i0:i1].sum() * HOP / SR >= 0.5:
            out.append((max(a, int((lo + 0.05) * SR)), min(b, int((hi - 0.05) * SR))))
    return out

words, text, per = [], [], []
for a, b in json.loads(sys.argv[3]):
    t, ws = heard(a, b)
    text.append(t)
    # Whisper can stop after one sentence with more speech still in the piece,
    # or step over a stretch: read every loud stretch it left without words.
    for _ in range(3):
        found = []
        for lo, hi in holes(ws, a, b):
            if hi - lo >= SR // 2:
                t2, w2 = heard(lo, hi)
                if w2:
                    text.append(t2)
                    found += w2
        if not found:
            break
        ws = sorted(ws + found, key=lambda w: w["s"])
    # No word runs into the next, or past 1.5 s: a stretched end would carry
    # the audio after it into a cut.
    for w, nxt in zip(ws, ws[1:] + [None]):
        w["e"] = min(w["e"], w["s"] + 1.5, nxt["s"] if nxt else w["e"])
        w["e"] = max(w["e"], w["s"])
    words += ws
    per.append(ws)
json.dump({"text": " ".join(text), "words": words, "pieces": per}, sys.stdout)
"""

# Whisper is fed the recording in pieces of about this many seconds, each
# cut at the quietest point near its end (`_pieces`).
PIECE = (16.0, 26.0)
TRANSCRIPT_VERSION = 4


def _pieces(audio: np.ndarray, sr: int = 16000,
            span: tuple[float, float] = PIECE) -> list[tuple[int, int]]:
    """Sample ranges of at most `span[1]` seconds, each ending in a pause.

    **Why (2026-11-22, the first OktAI recording):** fed all eleven minutes
    at once, Whisper skipped whole stretches - a full retake of a sentence in
    the music chapter and the last line came back with no words - while the
    same stretches cut out on their own were transcribed word for word.
    Whisper reads 30-second windows and decides where the next one starts
    from its own timestamps; after a long pause or a repeat that decision
    jumps. Pieces shorter than a window, each ending in a pause, leave it
    nothing to skip.
    """
    n = len(audio)
    lo, hi = int(span[0] * sr), int(span[1] * sr)
    hop = sr // 20                              # 50 ms
    out, a = [], 0
    while n - a > hi:
        seg = audio[a + lo:a + hi]
        frames = seg[:len(seg) // hop * hop].reshape(-1, hop)
        energy = (frames ** 2).mean(axis=1)
        # A pause is several quiet frames in a row: smooth over 300 ms.
        smooth = np.convolve(energy, np.ones(6) / 6, mode="same")
        cut = a + lo + int(np.argmin(smooth)) * hop + hop // 2
        out.append((a, cut))
        a = cut
    out.append((a, n))
    return out


def transcribe(path: Path, deterministic: bool = False) -> list[dict]:
    """Every spoken word with `s`/`e` seconds, cached by the file's content.

    `condition_on_previous_text=False` because a recording with retakes is
    exactly where Whisper, conditioned on its own last sentence, "corrects"
    a repeated read into one copy - and the repeat is the thing to find.
    The recording goes in as pieces cut at pauses (`_pieces`), one model
    load for all of them.
    """
    path = Path(path).expanduser()
    CACHE.mkdir(parents=True, exist_ok=True)
    det = ".det" if deterministic else ""
    key = CACHE / f"{_hash(path)}.v{TRANSCRIPT_VERSION}{det}.json"
    if key.exists():
        return json.loads(key.read_text())["words"]
    if not WHISPER_PYTHON.exists():
        raise RuntimeError(
            f"no Whisper interpreter at {WHISPER_PYTHON}. Set WHISPER_PYTHON to "
            f"a python with mlx-whisper installed (pip install mlx-whisper).")
    # A 16 kHz mono WAV, so Whisper does not have to decode a camera file.
    wav = CACHE / f"{key.stem}.16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vn",
                    "-ac", "1", "-ar", "16000", str(wav)],
                   check=True, capture_output=True)
    pieces = _pieces(load_audio(wav, 16000))
    print(f"transcribing {path.name} (Whisper, local, {len(pieces)} pieces)...")
    try:
        data = _whisper(wav, pieces, deterministic)
    finally:
        wav.unlink(missing_ok=True)
    data.pop("pieces", None)
    data["source"] = str(path)
    key.write_text(json.dumps(data, indent=1))
    return data["words"]


def _whisper(wav16: Path, pieces, deterministic: bool = False) -> dict:
    """`deterministic`: temperature 0 only, no random fallback - for the
    checks that decide a cut, which must hear the same audio the same way
    every time (one stumble was cut in one run and kept in the next,
    2026-11-22)."""
    out = subprocess.run([str(WHISPER_PYTHON), "-c", _WHISPER, str(wav16),
                          WHISPER_MODEL, json.dumps([list(p) for p in pieces])]
                         + (["det"] if deterministic else []),
                         check=True, capture_output=True, text=True)
    return json.loads(out.stdout)


def transcribe_spans(path: Path, spans: list[tuple[float, float]]) -> list[list[dict]]:
    """Each stretch of the recording transcribed on its own, cached.

    For `_refine`: a take cut out of its context is transcribed with word
    times Whisper gets right - inside the whole file it put "Six of" over
    "And half of the viewers", a phrase said just before it.
    """
    path = Path(path).expanduser()
    if not WHISPER_PYTHON.exists():
        return [[] for _ in spans]
    CACHE.mkdir(parents=True, exist_ok=True)
    spans = [(round(a, 3), round(b, 3)) for a, b in spans]
    h = hashlib.sha1(json.dumps(spans).encode()).hexdigest()[:12]
    key = CACHE / f"{_hash(path)}.spans.v{TRANSCRIPT_VERSION}.{h}.json"
    if key.exists():
        return json.loads(key.read_text())
    wav = CACHE / f"{key.stem}.16k.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(path), "-vn",
                    "-ac", "1", "-ar", "16000", str(wav)],
                   check=True, capture_output=True)
    print(f"checking {len(spans)} cuts (Whisper on each take alone)...")
    try:
        per = _whisper(wav, [(int(a * 16000), int(b * 16000)) for a, b in spans])["pieces"]
    finally:
        wav.unlink(missing_ok=True)
    key.write_text(json.dumps(per))
    return per


# ---------------------------------------------------------------------------
# matching the script
# ---------------------------------------------------------------------------

_ONES = ("zero one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def number_words(n: int) -> list[str]:
    """587 -> five hundred eighty seven. No "and": it is dropped on both sides."""
    if n < 20:
        return [_ONES[n]]
    if n < 100:
        return [_TENS[n // 10]] + ([_ONES[n % 10]] if n % 10 else [])
    for size, name in ((10 ** 9, "billion"), (10 ** 6, "million"),
                       (1000, "thousand"), (100, "hundred")):
        if n >= size:
            rest = n % size
            return number_words(n // size) + [name] + (number_words(rest) if rest else [])
    return [str(n)]


def norm(text: str) -> list[str]:
    """Comparable tokens: lower case, no punctuation, hyphens split.

    **Numbers become words, and "and" inside a number goes.** Whisper writes
    "587" where the script may say "five hundred and eighty seven" (or the
    other way round); both sides end up as "five hundred eighty seven".
    Thousands separators and a trailing "%" are handled; years read as
    "twenty twenty six" will not match "2026" and show in the report.
    """
    text = text.lower().replace("’", "'").replace("-", " ")
    # "10,000", and Whisper's "10 ,000"; "a hundred" is "one hundred".
    text = re.sub(r"(\d)\s*,\s*(\d{3})\b", r"\1\2", text)
    text = re.sub(r"\ba (hundred|thousand|million)\b", r"one \1", text)
    text = text.replace("%", " percent")
    text = re.sub(r"[^a-z0-9' ]+", " ", text)
    toks = []
    for t in text.split():
        t = t.strip("'")
        if not t:
            continue
        if t == "000":                  # Whisper's "10 ,000" is two words
            toks.append("thousand")
        elif t.isdigit() and len(t) <= 12:
            toks += number_words(int(t))
        else:
            toks.append(t)
    numeric = set(_ONES + _TENS[2:] + ["hundred", "thousand", "million", "billion"])
    return [t for i, t in enumerate(toks)
            if not (t == "and" and 0 < i < len(toks) - 1
                    and toks[i - 1] in numeric and toks[i + 1] in numeric)]


# Names Whisper writes as another word, script word -> what it writes.
SOUNDS_LIKE = {"claude": {"cloud", "clod", "clawed"}}


def _same(a: str, b: str) -> bool:
    return (a == b or b in SOUNDS_LIKE.get(a, ())
            or difflib.SequenceMatcher(None, a, b).ratio() >= MATCH)


def _sim(script: list[str], heard: list[str]) -> np.ndarray:
    return np.array([[1.0 if _same(a, b) else 0.0 for b in heard]
                     for a in script], np.float32)


def _ends(S: np.ndarray) -> np.ndarray:
    """Semi-global alignment score of the whole sentence ending at each word.

    Rows are script words, columns transcript words. The sentence must be
    consumed whole; the transcript may start and end anywhere. Match +2,
    mismatch -1, a skipped or an added word -1. The horizontal gap (words
    said that are not in the script) is the running-max trick, so each row is
    one vectorised pass rather than a Python loop over the transcript.
    """
    m, n = S.shape
    idx = np.arange(n + 1, dtype=np.float32)
    prev = np.zeros(n + 1, np.float32)              # row 0: free start
    for i in range(m):
        diag = np.full(n + 1, -1e9, np.float32)
        diag[1:] = prev[:-1] + np.where(S[i] > 0, 2.0, -1.0)
        up = prev - 1.0                             # script word not said
        x = np.maximum(diag, up)
        x[0] = prev[0] - 1.0
        # left: H[j] = max(x[j], H[j-1] - 1) == max_k<=j (x[k] - (j - k))
        cur = np.maximum.accumulate(x + idx) - idx
        prev = cur
    return prev                                     # score of a take ending at j


def _backtrace(script: list[str], heard: list[str], lo: int, hi: int):
    """The best alignment of one sentence ending at heard[hi - 1]: index pairs.

    The same scoring as `_ends` (match +2, mismatch, skipped or added word
    -1), traced back from the end, so the take is the one that ends there.

    **Why (2026-11-22):** this used to be `difflib.SequenceMatcher` over a
    window reaching two sentence-lengths back. With a retake close behind
    its first read, the longest common run sat in the *first* read, the
    match straddled both, and the retake was trimmed to half a sentence - so
    the first read won though the last one was meant.
    """
    sub = heard[lo:hi]
    m, n = len(script), len(sub)
    if not m or not n:
        return {}
    S = _sim(script, sub)
    H = np.zeros((m + 1, n + 1), np.float32)
    H[1:, 0] = -np.arange(1, m + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            H[i, j] = max(H[i - 1, j - 1] + (2.0 if S[i - 1, j - 1] else -1.0),
                          H[i - 1, j] - 1.0, H[i, j - 1] - 1.0)
    pairs = {}
    i, j = m, n
    while i > 0 and j > 0:
        d = H[i - 1, j - 1] + (2.0 if S[i - 1, j - 1] else -1.0)
        if H[i, j] == d:
            if S[i - 1, j - 1]:
                pairs[i - 1] = lo + j - 1
            i, j = i - 1, j - 1
        elif H[i, j] == H[i - 1, j] - 1.0:
            i -= 1
        else:
            j -= 1
    return pairs


def _backtrace_difflib(script: list[str], heard: list[str], lo: int, hi: int):
    """The old window matcher, kept for comparison in tests."""
    sub = heard[lo:hi]
    sm = difflib.SequenceMatcher(None, script, sub, autojunk=False)
    pairs = {}
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            pairs[a + k] = lo + b + k
    # Fuzzy matches the exact matcher missed (a misheard plural, a number).
    # In order, but not position by position: Whisper writes "FFmpeg" as
    # "FFM FFMPAG", and the script word belongs with the second.
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        if op == "replace":
            j = b0
            for i in range(a0, a1):
                for jj in range(j, b1):
                    if _same(script[i], sub[jj]):
                        pairs[i] = lo + jj
                        j = jj + 1
                        break
    return pairs


def _trim(pairs: dict, slack: int = 3) -> dict:
    """Drop matches stranded away from the take's main run.

    The search window is wider than the sentence, so a common word ("the",
    "it") at the window's edge can match a word of the sentence before -
    and a take that starts inside its neighbour breaks the order the
    takes are chosen in.
    """
    if len(pairs) < 2:
        return pairs
    items = sorted(pairs.items(), key=lambda kv: kv[1])
    # Split into runs wherever more words were said than the script skips
    # (plus `slack` for an ad-lib); keep the run with the most matches. A
    # false start ("I let AI read five hundred... sorry") is its own run.
    runs, cur = [], [items[0]]
    for prev, it in zip(items, items[1:]):
        if it[1] - prev[1] > slack + max(1, it[0] - prev[0]):
            runs.append(cur)
            cur = []
        cur.append(it)
    runs.append(cur)
    # A neighbouring run of three or more words, a few words away, is the
    # same read with a stumble in the middle ("stock footage and it was love
    # stock food and stock footage loves"): it stays, and the stumble between
    # is cut out of the audio (`_junk`). Dropping it lost half the sentence
    # (2026-11-22, the second recording).
    k = max(range(len(runs)), key=lambda r: len(runs[r]))
    lo = hi = k
    while lo > 0 and len(runs[lo - 1]) >= 3 and \
            runs[lo][0][1] - runs[lo - 1][-1][1] - 1 <= SPLICE_MAX:
        lo -= 1
    while hi + 1 < len(runs) and len(runs[hi + 1]) >= 3 and \
            runs[hi + 1][0][1] - runs[hi][-1][1] - 1 <= SPLICE_MAX:
        hi += 1
    return dict(x for r in runs[lo:hi + 1] for x in r)


SPLICE_MAX = 12      # words of stumble a sentence can be spliced across


@dataclass
class Take:
    sentence: int
    first: int                    # transcript word index, inclusive
    last: int                     # inclusive
    score: float                  # share of the sentence's words matched
    pairs: dict                   # script word index -> transcript word index
    others: int                   # how many other takes were found and dropped
    # Word-index ranges inside the take that are cut out: a stumble between
    # two parts of one read (`_junk`).
    cuts: list = field(default_factory=list)


RESTART_GAP = 4.0     # seconds: a phrase said again within this is a restart
RESTART_SIM = 0.7     # ...when the two copies are at least this alike


def _word_alike(a: str, b: str) -> bool:
    return _same(a, b) or (min(len(a), len(b)) >= 2 and (a in b or b in a))


def _alike(c1: list[str], c2: list[str]) -> bool:
    """Two copies of one phrase: the same first two words, nearly the same
    letters.

    The letters are compared without spaces, so "AI tools love" and its
    misheard repeat "AirTools log" are alike. The words have to line up at
    the start, so a phrase and the same words shifted by one ("seconds, then
    the edit" against "seconds of it, then the edit") never are.
    """
    if not c1 or not c2 or not _word_alike(c1[0], c2[0]):
        return False
    if len(c1) > 1 and not any(_word_alike(c1[1], x) for x in c2[:2]):
        return False
    a, b = "".join(c1).replace(" ", ""), "".join(c2).replace(" ", "")
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    if sm.ratio() < RESTART_SIM:
        return False
    # ...and end together: "the first seconds, then the edit" is not a
    # restart of "the first ten seconds of it" - their shared letters stop
    # in the middle of the first.
    last = [blk for blk in sm.get_matching_blocks() if blk.size][-1]
    return len(a) - (last.a + last.size) <= 3 and len(b) - (last.b + last.size) <= 3


def restarts(heard: list[list[str]], words: list[dict],
             sentences: list[list[str]]) -> set[int]:
    """Word indices of a phrase that was said and then straight away again.

    **Why (2026-11-22, the first OktAI recording):** a person reading fixes
    a stumble mid-sentence: "AI tools love... AI tools love stock footage",
    "About 250 views or... About 250 views, about 770". The whole-sentence
    retake rule never sees these - the stumble is inside the one take - so
    the kept take carried both copies, or was cut short where the repeat
    broke the match. The first copy goes, the second is kept: the same rule
    as for whole retakes, inside a sentence.

    A restart is three to seven words, then straight away the same phrase
    again (a word more or less; `_alike`), within `RESTART_GAP` seconds. A
    repeat the script itself has ("stock footage, and stock footage") is
    left alone. A whole sentence read twice is not this: the takes are
    chosen by `align`, the last good one kept.
    """
    W = [" ".join(t) for t in heard]
    script = " " + " ".join(t for s in sentences for t in s) + " "
    n = len(W)
    out: set[int] = set()
    for i in range(n):
        if i in out or not W[i]:
            continue
        for L in range(7, 2, -1):
            j = i + L
            if j >= n or words[j]["s"] - words[j - 1]["e"] > RESTART_GAP:
                continue
            # A restart never runs over the end of a sentence: "...a beat
            # underneath. What we learned?" is the end of one read and the
            # start of the next, not a phrase said twice.
            if any(words[k]["w"].strip().endswith((".", "?", "!"))
                   for k in range(i, j - 1)):
                continue
            hit = False
            for L2 in (L, L - 1, L + 1):
                if L2 < 2 or not _alike(W[i:j], W[j:j + L2]):
                    continue
                if f" {' '.join(W[i:j + L2])} " in script:
                    continue
                hit = True
                break
            if hit:
                out.update(range(i, j))
                break
    return out


def _in_window(window, t: float) -> bool:
    """`window` is None, one (start, end), or a list of them (a take plus
    its pickups appended at the end, 2026-11-23)."""
    if not window:
        return True
    ranges = [window] if isinstance(window[0], (int, float)) else window
    return any(a <= t <= b for a, b in ranges)


def align(sentences: list[list[str]], words: list[dict],
          window: tuple | list | None = None,
          free_from: float | None = None) -> list[Take]:
    """One take per sentence, in order, preferring the last good one.

    **`free_from`: where pickups start** (lines read again or added after
    the take, joined on its end, 2026-11-24). A line with a good read there
    takes it, wherever the line sits in the script - a pickup is a deliberate
    re-read - and the in-order rule applies only to the take before it.
    """
    heard = [norm(w["w"]) for w in words]
    # `restarts` is not applied here any more (2026-11-22, the second
    # recording): it always kept the second copy, and in "AI tools love stock
    # footage and it was love stock food and stock footage loves" the second
    # copy was the broken one. A stumble is now aligned past and cut out of
    # the take (`_trim` keeps both parts, `_junk` cuts what is between), so
    # the alignment picks whichever copy matches the script.
    skip: set[int] = set()
    # A Whisper "word" can be two tokens ("thirty-day"); flatten, keeping the
    # word each token came from.
    flat, owner = [], []
    for i, toks in enumerate(heard):
        if not _in_window(window, words[i]["s"]):
            continue
        if i in skip:
            continue
        for t in toks:
            flat.append(t)
            owner.append(i)
    n = len(flat)
    if not n:
        raise ValueError("the recording has no words in it (or in `window`)")

    cands: list[list[tuple[int, int, float, dict]]] = []
    for si, sent in enumerate(sentences):
        m = len(sent)
        end = _ends(_sim(sent, flat))[1:]           # end[j]: take ends at j
        best = 2.0 * m
        found = []
        # Peaks, best first, suppressing the neighbourhood of each.
        order = np.argsort(-end)
        taken = np.zeros(n, bool)
        for j in order:
            if end[j] < best * MIN_SCORE * 0.5 or len(found) >= 6:
                break
            if taken[j]:
                continue
            lo, hi = max(0, j - 2 * m - 4), j + 1
            pairs = _trim(_backtrace(sent, flat, lo, hi))
            if not pairs:
                continue
            score = len(pairs) / m
            if score < MIN_SCORE:
                taken[max(0, j - m // 2):j + m // 2 + 1] = True
                continue
            a, b = min(pairs.values()), max(pairs.values())
            taken[max(0, a - 1):b + 2] = True
            # The same read, found again from a later end: the first find is
            # the best-scoring one. A copy starting a word late would earn the
            # later-take bonus and cut the sentence's first words (2026-11-22).
            if any(a <= c[1] and c[0] <= b for c in found):
                continue
            # Words said inside the take that the script does not have: "the
            # first ten seconds" holds all of "the first seconds", but it is
            # another sentence, not a read of this one.
            ins = max(0, (b - a + 1) - m)
            found.append((a, b, score, pairs, ins))
        cands.append(found)

    # Pickups first: a line with a good read in them takes the best of those
    # (the latest on a tie), and leaves the in-order choice below.
    fixed: dict[int, tuple] = {}
    if free_from is not None:
        for si, cs in enumerate(cands):
            m = len(sentences[si])
            late = [c for c in cs if words[owner[c[0]]]["s"] >= free_from]
            good = [c for c in late if c[2] - c[4] / m >= GOOD]
            if good:
                fixed[si] = max(good, key=lambda c: (round(c[2] - c[4] / m, 2), c[0]))
            cands[si] = [c for c in cs if words[owner[c[0]]]["s"] < free_from]
            # Read only there, and not well enough heard: still its read
            # ("AI tools love..." spliced by Whisper, in a Short cut from the
            # long form, where everything is free - 2026-11-24).
            if late and not cands[si] and si not in fixed:
                fixed[si] = max(late, key=lambda c: (round(c[2] - c[4] / m, 2), c[0]))
        for si in fixed:
            cands[si] = cands[si] or [fixed[si]]

    missing = [i for i, c in enumerate(cands) if not c]
    if missing:
        lines = "\n".join(f"  {i + 1}. {' '.join(sentences[i])}" for i in missing)
        raise ValueError(f"not found in the recording - re-record these, or "
                         f"change the script to what was said:\n{lines}")

    # Choose one candidate per sentence, monotonic in time, maximising score
    # plus a bonus for being a later take (the retake rule). The bonus is by
    # rank, not by seconds: a re-read two seconds after the first is still
    # the one meant, and Whisper cannot hear the intonation that made the
    # editor read it again. Only a nearly complete take earns it, so a
    # false start after a full read never wins.
    for cs in cands:
        cs.sort(key=lambda c: c[0])
    INF = -1e9
    order_ = [si for si in range(len(cands)) if si not in fixed]
    best: dict[int, list[float]] = {}
    back: dict[int, list[int]] = {}
    prev = None
    for si in order_:
        cs = cands[si]
        row, brow = [], []
        m = len(sentences[si])
        for r, (a, b, score, _, ins) in enumerate(cs):
            rank = r / (len(cs) - 1) if len(cs) > 1 else 1.0
            fit = score - ins / m
            gain = fit + (LATER * rank if fit >= GOOD else 0.0)
            if prev is None:
                row.append(gain)
                brow.append(-1)
                continue
            top, arg = INF, -1
            for k, (pa, pb, *_) in enumerate(cands[prev]):
                if pb < a and best[prev][k] > top:
                    top, arg = best[prev][k], k
            row.append(top + gain if arg >= 0 else INF)
            brow.append(arg)
        best[si], back[si] = row, brow
        prev = si
    chosen: dict[int, int] = {}
    if order_:
        last = order_[-1]
        k = int(np.argmax(best[last]))
        if best[last][k] <= INF / 2:
            raise ValueError("the takes found are not in script order - is the "
                             "right recording paired with this script?")
        for si in reversed(order_):
            chosen[si] = k
            k = back[si][k]

    takes = []
    for si, cs in enumerate(cands):
        if si in fixed:
            cs = [fixed[si]]
            k = 0
        else:
            k = chosen[si]
        a, b, score, pairs, _ = cs[k]
        # Retakes worth mentioning: other nearly complete reads of it - one
        # per stretch, since the search finds the same read from several ends.
        seen = [(a, b)]
        others = 0
        for j, c in enumerate(cs):
            if j == k or c[2] < GOOD or any(c[0] <= y and x <= c[1] for x, y in seen):
                continue
            seen.append((c[0], c[1]))
            others += 1
        takes.append(Take(si, owner[a], owner[b], score,
                          {s: owner[t] for s, t in pairs.items()}, others))
    _edges(takes, words, [len(s) for s in sentences], window)
    _junk(takes, words)
    return takes


def _junk(takes: list[Take], words: list[dict]) -> None:
    """Mark what was said inside a take that the script does not have.

    **Why (2026-11-22, the second recording; his note: "better cut
    everything between sentences or even words if it's messy").** Between
    two script words that follow each other, any words said are a stumble:
    "we built a *new library.* new one", "stock footage and *it was love stock
    food* and stock footage". Two or more words, or half a second or more of
    them, are cut out; a single short word ("half *of* the viewers") stays,
    as Whisper adds those where nothing was said wrong.
    """
    for tk in takes:
        items = sorted(tk.pairs.items())
        cuts = []
        for (i1, w1), (i2, w2) in zip(items, items[1:]):
            if i2 - i1 != 1 or w2 - w1 < 2:
                continue
            n = w2 - w1 - 1
            if n >= 2 or words[w2]["s"] - words[w1]["e"] >= 0.5:
                cuts.append((w1, w2))
        tk.cuts = cuts


def _pin_pairs(toks: list[str], words: list[dict], a: float, b: float) -> dict:
    """Script token -> word index, matched again inside a pinned stretch, so
    a pinned line's captions follow its words and not an even spread."""
    idx = [k for k, w in enumerate(words) if a - 0.05 <= w["s"] and w["e"] <= b + 0.15]
    flat, owner = [], []
    for k in idx:
        for t in norm(words[k]["w"]):
            flat.append(t)
            owner.append(k)
    if not flat or not toks:
        return {}
    j = int(np.argmax(_ends(_sim(toks, flat))[1:]))
    pairs = _trim(_backtrace(toks, flat, 0, j + 1))
    return {ti: owner[fi] for ti, fi in pairs.items()}


def _cut_out(parts, cuts):
    """Each sentence's pieces with the (start, end) source ranges removed."""
    out = []
    for pieces, ranges in zip(parts, cuts):
        for c0, c1 in ranges:
            nxt = []
            for a, b in pieces:
                if c1 <= a or c0 >= b:
                    nxt.append((a, b))
                    continue
                if c0 > a:
                    nxt.append((a, c0))
                if c1 < b:
                    nxt.append((c1, b))
            pieces = [(a, b) for a, b in nxt if b - a > 0.01]
        out.append(pieces)
    return out


GAP_SPEECHY = 20      # dB over the room: still a word's tail or onset
GAP_HISS = 18         # dB over the room's own hiss band: an "s", "f" or "t"
GAP_REACH = 0.35      # seconds a tail or an onset may run past Whisper's time
RELEASE_REACH = 0.16  # seconds of a final stop's closure before its release
RELEASE_OVER = 20     # dB the release's hiss stands over the closure's
RELEASE_LONG = 0.20   # a burst longer than this is a word's "s", not a release
LONG_WORD = 1.2       # seconds: a word this long hides a stumble (Whisper caps at 1.5)
GAP_LOUD = 36         # dB over the room: louder than a breath - keep it
GAP_CLICK = 0.04      # seconds over +30 dB that are only a click


def _hiss_db(audio: np.ndarray, sr: int = SR, room=None) -> np.ndarray:
    """Per 10 ms, the 3.5-11 kHz band in dB over its own quiet floor.

    **Why (the third recording, 2026-11-23: "the s of graphics is cut off",
    "minutes", "seconds", "sentence", "FFmpeg" heard as "FMPEG").** A final
    "s" or a starting "f" is all hiss and little level: after "minutes" the
    whole band sat 16-18 dB over the room, under `GAP_SPEECHY`, while the
    hiss band was 30-39 dB over its floor for a tenth of a second - and the
    gap clean-up gave it to the room tone. This band hears it.
    """
    from scipy.signal import butter, sosfilt
    sos = butter(4, [3500, min(11000, sr / 2 - 100)], btype="band", fs=sr,
                 output="sos")
    hop = sr // 100
    hf = sosfilt(sos, audio).astype(np.float32)
    n = len(hf) // hop
    db = 10 * np.log10((hf[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    # The floor is the room's own hiss: the band where the whole signal is
    # at the room's level (`room`: per-frame dB over the floor), not the
    # band's quietest frames - a vowel has none of it.
    quiet = db[room[:n] < 6] if room is not None and (room[:n] < 6).any() else db
    return db - np.median(quiet)


def _bridge(hiss: np.ndarray, i: int, lim: int) -> int:
    """Frame `i`, the end of a word's tail, moved past a final stop's
    release: a burst of hiss within `RELEASE_REACH` that is over within
    `RELEASE_LONG`. A longer one is a breath, which stays room tone."""
    k = next((x for x in range(i, min(i + int(RELEASE_REACH * 100), lim))
              if hiss[x] > GAP_HISS), None)
    if k is None:
        return i
    e = k
    while e + 1 < lim and hiss[e + 1] > GAP_HISS:
        e += 1
    if (e - k + 1) / 100 > RELEASE_LONG or e + 1 >= lim:
        return i
    return e + 1


def clean_gaps(audio: np.ndarray, words: list[dict], sr: int = SR) -> np.ndarray:
    """`audio` with the space between words replaced by the room's own tone.

    **Why (2026-11-22, his note on the first recorded render: "it had gaps
    between sentences where you could hear noises").** The pauses kept
    between sentences and inside them carried every breath, click and creak.
    Now each gap between two words, trimmed to where the first word's tail
    and the next one's onset actually are, is crossfaded to room tone -
    unless something in it is louder than a breath for longer than a click,
    which may be a word Whisper did not write down, and stays.
    """
    out = audio.copy()
    hop = sr // 100
    n = len(audio) // hop
    floor = _floor_db(audio, sr)
    db = 10 * np.log10((audio[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12) - floor
    hiss = _hiss_db(audio, sr, db)[:n]
    speechy = (db > GAP_SPEECHY) | (hiss > GAP_HISS)
    reach = int(GAP_REACH * 100)
    tone = room_tone(audio, sr=sr)
    fade = int(0.01 * sr)
    ws = sorted(words, key=lambda w: w["s"])
    for a, b in zip(ws, ws[1:]):
        i, j = int(a["e"] * 100), int(b["s"] * 100)
        if j - i < 8:
            continue
        # A dip of up to 30 ms is inside the word - the closure of a "t"
        # before its "s" ("minutes") - not the end of it. Nor is a final
        # stop's closure, up to `RELEASE_REACH` of silence before the burst
        # that ends the word: "code" lost its "d" and was heard as "Colt"
        # (2026-11-24).
        lim = min(i + reach, j)
        while i < lim and speechy[i:min(i + 4, lim)].any():  # the word's tail
            i += 1
        i = _bridge(hiss, i, lim)
        lim = max(j - reach, i)
        while j > lim and speechy[max(j - 4, lim):j].any():  # the next onset
            j -= 1
        i, j = i + 2, j - 2
        if j - i < 6:
            continue
        seg = db[i:j]
        if seg.max() > GAP_LOUD and (seg > 30).sum() / 100 > GAP_CLICK:
            continue
        a0, a1 = i * hop, j * hop
        fill = _tone(tone, a1 - a0)
        ramp = np.linspace(0, 1, min(fade, (a1 - a0) // 2), dtype=np.float32)
        k = len(ramp)
        if k:
            fill[:k] = out[a0:a0 + k] * (1 - ramp) + fill[:k] * ramp
            fill[-k:] = fill[-k:] * (1 - ramp) + out[a1 - k:a1] * ramp
        out[a0:a1] = fill
    return out


EDGE_GAP = 0.35     # seconds between a take and a misheard word at its edge


def _edges(takes: list[Take], words: list[dict], lengths: list[int],
           window) -> None:
    """Take in a misheard first or last word, so it is not cut off.

    **Why (2026-11-22, the first OktAI recording):** Whisper wrote "Claude"
    as "Cloud" and the outro's "Thanks" as "Short", so the take matched from
    the second word and the cut started a word late - the name itself was
    cut away. When a sentence's first (or last) one or two script words are
    unmatched and the transcript has that many words right against the take
    (under `EDGE_GAP`), not belonging to the neighbouring take, they are
    the same words misheard: the take grows to cover them.
    """
    for k, tk in enumerate(takes):
        if not tk.pairs:
            continue
        lead = min(tk.pairs)
        floor = takes[k - 1].last if k > 0 else -1
        i = tk.first
        for _ in range(min(lead, 2)):
            j = i - 1
            if j <= floor or not _in_window(window, words[j]["s"]):
                break
            if words[i]["s"] - words[j]["e"] > EDGE_GAP:
                break
            i = j
        # A word said in two goes: Whisper wrote a slow "FF... M... peg" as
        # "FFM" then "FFMPAG", and the take began on the second - the cut
        # started on "peg" (2026-11-22). A word just before that the first
        # word starts with belongs to it.
        while i - 1 > floor and _in_window(window, words[i - 1]["s"]):
            prev = "".join(norm(words[i - 1]["w"]))
            cur = "".join(norm(words[i]["w"]))
            if (len(prev) >= 2 and cur != prev and cur.startswith(prev)
                    and words[i]["s"] - words[i - 1]["e"] <= 0.6):
                i -= 1
            else:
                break
        trail = lengths[k] - 1 - max(tk.pairs)
        ceil = takes[k + 1].first if k + 1 < len(takes) else len(words)
        e = tk.last
        for _ in range(min(trail, 2)):
            j = e + 1
            if j >= ceil or not _in_window(window, words[j]["s"]):
                break
            if words[j]["s"] - words[e]["e"] > EDGE_GAP:
                break
            e = j
        tk.first, tk.last = i, e


# ---------------------------------------------------------------------------
# cutting
# ---------------------------------------------------------------------------

def _quietest(audio: np.ndarray, a: float, b: float, sr: int = SR) -> float:
    """The quietest 10 ms point between a and b, in seconds."""
    i0, i1 = int(a * sr), int(b * sr)
    if i1 - i0 < int(0.02 * sr):
        return (a + b) / 2
    hop = int(0.005 * sr)
    seg = audio[i0:i1]
    win = int(0.010 * sr)
    e = np.array([np.sqrt(np.mean(seg[k:k + win] ** 2) + 1e-12)
                  for k in range(0, max(1, len(seg) - win), hop)])
    return a + (int(np.argmin(e)) * hop + win / 2) / sr


def room_tone(audio: np.ndarray, seconds: float = 0.6, sr: int = SR) -> np.ndarray:
    """The quietest stretch of the recording: its own silence, to fill gaps."""
    win = int(seconds * sr)
    if len(audio) <= win:
        return np.zeros(win, np.float32)
    hop = int(0.05 * sr)
    rms = [np.sqrt(np.mean(audio[k:k + win] ** 2))
           for k in range(0, len(audio) - win, hop)]
    k = int(np.argmin(rms)) * hop
    return audio[k:k + win].copy()


def _tone(tone: np.ndarray, n: int) -> np.ndarray:
    if n <= 0:
        return np.zeros(0, np.float32)
    reps = int(np.ceil(n / len(tone)))
    out = np.tile(tone, reps)[:n].copy()
    f = min(len(out) // 2, int(FADE * SR))
    if f:
        ramp = np.linspace(0, 1, f, dtype=np.float32)
        out[:f] *= ramp
        out[-f:] *= ramp[::-1]
    return out


def _fade(x: np.ndarray) -> np.ndarray:
    f = min(len(x) // 2, int(FADE * SR))
    if f:
        ramp = np.linspace(0, 1, f, dtype=np.float32)
        x[:f] *= ramp
        x[-f:] *= ramp[::-1]
    return x


def _bounds(takes: list[Take], words: list[dict], audio: np.ndarray,
            gaps: list[float], max_pause: float, edges=None):
    """Source (start, end) per sentence and whether it joins its neighbour.

    `edges`: (start, end) per sentence already found from the audio
    (`_refine`), used as they are in place of the word times.
    """
    total = len(audio) / SR
    spans, joined = [], []
    for i, tk in enumerate(takes):
        if edges is not None and edges[i] is not None:
            a, b = edges[i]
        else:
            s, e = words[tk.first]["s"], words[tk.last]["e"]
            before = words[tk.first - 1]["e"] if tk.first > 0 else 0.0
            after = words[tk.last + 1]["s"] if tk.last + 1 < len(words) else total
            a = max(before, s - PRE)
            b = min(after, e + POST)
            a = _quietest(audio, a, s) if s - a > 0.03 else a
        spans.append([max(0.0, a), min(total, b)])
        # Same take, nothing cut between: keep the real pause - unless the
        # script asks for a long one (a sound example plays in it, 2026-11-21):
        # that gap is a written beat, filled with room tone to its length.
        joined.append(i > 0 and takes[i - 1].last + 1 == tk.first
                      and not _written(gaps[i - 1]))
    for i in range(1, len(spans)):
        if not joined[i]:
            continue
        pause = spans[i][0] - spans[i - 1][1]
        if pause <= 0:
            mid = (spans[i - 1][1] + spans[i][0]) / 2
            spans[i - 1][1] = spans[i][0] = mid
            continue
        keep = min(pause, max(max_pause, gaps[i - 1]))
        if keep < pause:                 # trim the middle of a long pause
            spans[i - 1][1] += keep / 2
            spans[i][0] -= keep / 2
        else:                            # the whole pause stays
            spans[i - 1][1] = spans[i][0]
    return spans, joined


REFINE_PRE = 0.8      # seconds of context before a take when it is checked alone
REFINE_POST = 0.7     # ...and after it (0.4 cost Whisper a last word)
REFINE_MIN = 0.7      # the share of the sentence the check must find to be used
EDGE_TRUST = 0.15     # a word this close to a clip's edge has lost its context


def _edge(audio: np.ndarray, t: float, limit: float, quiet_db: float,
          back: bool, reach: float = 0.4, sr: int = SR) -> float:
    """Where the speech going on at `t` starts (`back`) or stops: the
    nearest 10 ms frame under `quiet_db`, at most `reach` away, never past
    `limit`. Whisper puts a word's start on its vowel; an "F" before it is
    quiet enough to be cut off (the take of "FFmpeg cuts the video" began
    "...peg", 2026-11-22)."""
    hop = int(0.01 * sr)
    step = -hop if back else hop
    stop = max(limit, t - reach) if back else min(limit, t + reach)
    k = int(t * sr)
    best, best_db = k, None
    while (k + step >= int(stop * sr)) if back else (k + step <= int(stop * sr)):
        seg = audio[k + step:k] if back else audio[k:k + step]
        if len(seg):
            db = 10 * np.log10(float((seg ** 2).mean()) + 1e-12)
            if db < quiet_db:
                return k / sr
            if best_db is None or db < best_db:
                best, best_db = k, db
        k += step
    # Nothing quiet in reach: speech runs straight into the word, so the
    # cut goes at the quietest point found, not the far end of the reach.
    # The far end was inside the word before - "paragraph. And here, the
    # whole paragraph" kept "...graph." (the second recording, 2026-11-23).
    return best / sr


def _release(audio: np.ndarray, b: float, limit: float, quiet_db: float,
             sr: int = SR) -> float:
    """The end `b` moved past a final stop's release, if one follows.

    **Why (2026-11-24, "Claude made it with the code" heard as "...the
    Colt"):** a "d", "t" or "k" at the end of a sentence is a tenth of a
    second of silence - the closure - and then a short burst of hiss, the
    release. `_edge` stops at the first quiet frame, which is the closure,
    so the word lost its last sound. The release is found as hiss
    `RELEASE_OVER` over the closure's, within `RELEASE_REACH`, no longer
    than `RELEASE_LONG`, with no voice after it - a longer burst followed by
    a vowel is the next word's "s", and the end stays.
    """
    from scipy.signal import butter, sosfilt
    hop = sr // 100
    lead = 15                                   # frames before b: the filter settles
    k0 = int(b * sr) - lead * hop
    k1 = int(min(limit, b + RELEASE_REACH + RELEASE_LONG + 0.08) * sr)
    if k0 < 0 or k1 - k0 < (lead + 8) * hop:
        return b
    seg = audio[k0:k1].astype(np.float64)
    sos = butter(4, [3500, min(11000, sr / 2 - 100)], btype="band", fs=sr,
                 output="sos")
    hf = sosfilt(sos, seg)
    # The voice's own band: a vowel is loud in it, a release is not.
    lf = sosfilt(butter(4, [80, 1000], btype="band", fs=sr, output="sos"), seg)
    n = len(seg) // hop
    low = 10 * np.log10((lf[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    hiss = 10 * np.log10((hf[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    reach = min(n, lead + int(RELEASE_REACH * 100))
    base = hiss[lead - 5:reach].min()
    k = next((i for i in range(lead, reach) if hiss[i] > base + RELEASE_OVER), None)
    if k is None:
        return b
    e = k
    while e + 1 < n and hiss[e + 1] > base + RELEASE_OVER:
        e += 1
    if (e - k + 1) / 100 > RELEASE_LONG or e + 1 >= n:
        return b
    if (low[k:e + 7] > quiet_db + 6).any():
        return b                                # voiced: a word, not a release
    return min(limit, (k0 + (e + 1) * hop) / sr + 0.02)


def _refine(path: Path, audio: np.ndarray, spans, sent_words: list[list[str]],
            last_starts: list | None = None):
    """(start, end) per sentence from the take transcribed on its own, or
    None where that check is not sure.

    **Why (2026-11-22, the first OktAI recording):** the whole-file word
    times are right almost everywhere and wrong exactly where it matters -
    at a stumble. "And half of the viewers... Six of them gave the answer
    away" came back with "Six of" over the first phrase, and the cut kept
    it. Each kept take, with a little context, is transcribed alone; the
    sentence is matched to it again, and the cut goes from where its first
    word starts to where its last word ends, measured on the audio.
    """
    total = len(audio) / SR
    clips = []
    for i, (a, b) in enumerate(spans):
        lo = spans[i - 1][1] if i else 0.0
        hi = spans[i + 1][0] if i + 1 < len(spans) else total
        # A pickup's neighbours are elsewhere in the file (2026-11-24).
        if lo > a:
            lo = 0.0
        if hi < b:
            hi = total
        clips.append((max(lo, a - REFINE_PRE), min(hi, b + REFINE_POST)))
    per = transcribe_spans(path, clips)
    quiet = _floor_db(audio) + 8
    edges: list = []
    for (lo, hi), ws, toks, (a0, b0) in zip(clips, per, sent_words, spans):
        flat, owner = [], []
        for k, w in enumerate(ws):
            for t in norm(w["w"]):
                flat.append(t)
                owner.append(k)
        if not flat or not toks:
            edges.append(None)
            continue
        j = int(np.argmax(_ends(_sim(toks, flat))[1:]))
        pairs = _trim(_backtrace(toks, flat, 0, j + 1))
        if len(pairs) / len(toks) < REFINE_MIN:
            edges.append(None)
            continue
        f, l = owner[min(pairs.values())], owner[max(pairs.values())]
        f0, l0 = f, l
        for _ in range(min(min(pairs), 2)):          # a misheard first word
            if f > 0 and ws[f]["s"] - ws[f - 1]["e"] <= EDGE_GAP:
                f -= 1
        for _ in range(min(len(toks) - 1 - max(pairs), 2)):
            if l + 1 < len(ws) and ws[l + 1]["s"] - ws[l]["e"] <= EDGE_GAP:
                l += 1
        # Words the check could not hear at all - the clip's edge cost
        # Whisper the last ones - leave that edge to the whole file, which
        # heard them: "AI tools love stock footage" lost "stock footage" and
        # "Claude made with code" its "code" (the third recording,
        # 2026-11-23).
        short_head = min(pairs) > f0 - f
        short_tail = len(toks) - 1 - max(pairs) > l - l0
        # Never back over the word before, or on into the word after: the
        # reach for a quiet onset ran into "...whole paragraph." and kept its
        # tail in front of the retake (2026-11-23).
        lo_w = max(lo, ws[f - 1]["e"]) if f > 0 else lo
        hi_w = min(hi, ws[l + 1]["s"]) if l + 1 < len(ws) else hi
        a = max(lo_w, _edge(audio, ws[f]["s"], lo_w, quiet, back=True) - 0.02)
        b = min(hi_w, _edge(audio, ws[l]["e"], hi_w, quiet, back=False) + 0.04)
        b = _release(audio, b, hi_w, quiet)
        # A word Whisper puts at the very edge of the clip is the clip's cut
        # landing in speech - the end of a stumble just before ("...earn
        # money. Content that's repetitive" came back as one long
        # "content"). Its time is not to be trusted; that edge stays.
        if ws[f]["s"] - lo < EDGE_TRUST or short_head:
            a = a0
        if hi - ws[l]["e"] < EDGE_TRUST or short_tail:
            b = b0
        # Nor may the end fall before the last word even starts, where the
        # whole file heard it: alone, Whisper put "footage" and "code" a
        # second early and the cut ended on "love" (2026-11-23).
        if last_starts is not None and b < last_starts[len(edges)] + 0.12:
            b = b0
        edges.append((a, b) if b - a > 0.2 else None)
    # Neighbours never overlap: where they would, they meet in the middle.
    for i in range(1, len(edges)):
        p, c = edges[i - 1], edges[i]
        if p and c and p[0] < c[0] < p[1]:
            mid = (p[1] + c[0]) / 2
            edges[i - 1], edges[i] = (p[0], mid), (mid, c[1])
    # Neighbours read in one breath meet where the audio is quietest, not
    # where Whisper put the word boundary.
    for i in range(1, len(edges)):
        p, c = edges[i - 1], edges[i]
        if p and c and -0.05 <= c[0] - p[1] <= SPLIT_NEAR:
            t = _split(audio, min(p[1], c[0]) - SPLIT_BACK, max(p[1], c[0]) + SPLIT_AHEAD)
            if p[0] + 0.2 < t < c[1] - 0.2:
                edges[i - 1], edges[i] = (p[0], t), (t, c[1])
    return edges


SPLIT_NEAR = 0.35     # two lines closer than this in the take were read as one
SPLIT_BACK = 0.12     # how far before Whisper's boundary a split may fall
SPLIT_AHEAD = 0.30    # ...and after it


def _split(audio: np.ndarray, t0: float, t1: float, sr: int = SR) -> float:
    """The quietest 30 ms in [t0, t1]: where one line read straight into the
    next can be cut in two.

    **Why (2026-11-24, "at 0:06 the end of the letter S at the word 'clips'
    is cut and brought in at the beginning of 0:09 when we say 'and the
    same'"):** the slop list was split into lines with a written pause
    between them, read without one. Whisper started "and" at 15.36 s, in
    the middle of the "s" (15.30-15.46); both edges met there, and half the
    "s" played after the pause. The quiet after it, at ~15.55, is the cut.
    """
    a, b = max(0, int(t0 * sr)), min(len(audio), int(t1 * sr))
    hop = sr // 100
    n = (b - a) // hop
    if n < 3:
        return (t0 + t1) / 2
    e = (audio[a:a + n * hop].reshape(n, hop).astype(np.float64) ** 2).mean(axis=1)
    e = np.convolve(e, np.ones(3) / 3, mode="same")
    k = int(np.argmin(e[1:-1])) + 1
    return (a + k * hop + hop / 2) / sr


def _floor_db(audio: np.ndarray, sr: int = SR) -> float:
    """The room's level: the 10th percentile of 10 ms frames, in dB."""
    hop = int(0.01 * sr)
    n = len(audio) // hop
    e = 10 * np.log10((audio[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    return float(np.percentile(e, 10))


def _inner_pauses(audio: np.ndarray, a: float, b: float, quiet_db: float,
                  longer: float, sr: int = SR) -> list[tuple[float, float]]:
    """Silent runs inside (a, b) longer than `longer` seconds, edges excluded."""
    hop = int(0.01 * sr)
    seg = audio[int(a * sr):int(b * sr)]
    n = len(seg) // hop
    if n < 3:
        return []
    e = 10 * np.log10((seg[:n * hop].reshape(n, hop) ** 2).mean(axis=1) + 1e-12)
    quiet = e < quiet_db
    runs, k = [], 0
    while k < n:
        if not quiet[k]:
            k += 1
            continue
        j = k
        while j < n and quiet[j]:
            j += 1
        s, t = a + k * hop / sr, a + j * hop / sr
        if k > 0 and j < n and t - s > longer:
            runs.append((s, t))
        k = j
    return runs


def _tighten(audio: np.ndarray, spans, longer: float, keep: float):
    """Each sentence's span as pieces, with its long inner pauses shortened.

    **Why (2026-11-22, the first OktAI recording):** "make me sound
    structured and not too slow". A person reading pauses mid-sentence to
    find the next words - four seconds once, in a retake of the outro - and
    the kept take carried every one of them. A silence longer than `longer`
    inside a sentence keeps `keep` seconds of itself, from its middle cut out;
    commas and breaths shorter than that are left alone.
    """
    quiet_db = _floor_db(audio) + 15
    parts = []
    for a, b in spans:
        cut = [a]
        for s, t in _inner_pauses(audio, a, b, quiet_db, longer):
            cut += [s + keep / 2, t - keep / 2]
        cut.append(b)
        parts.append([(cut[k], cut[k + 1]) for k in range(0, len(cut), 2)])
    return parts


def _assemble(audio, spans, joined, gaps, tail, parts=None):
    tone = room_tone(audio)
    parts = parts or [[tuple(s)] for s in spans]
    out, edl, t = [], [], 0.0
    for i, (a, b) in enumerate(spans):
        if i > 0 and not joined[i]:
            g = _tone(tone, int(gaps[i - 1] * SR))
            out.append(g)
            edl.append({"out": round(t, 4), "dur": round(len(g) / SR, 4),
                        "gap": True})
            t += len(g) / SR
        for pa, pb in parts[i]:
            piece = _fade(audio[int(pa * SR):int(pb * SR)].copy())
            out.append(piece)
            edl.append({"out": round(t, 4), "dur": round(len(piece) / SR, 4),
                        "src": round(pa, 4)})
            t += len(piece) / SR
    tl = _tone(tone, int(tail * SR))
    out.append(tl)
    edl.append({"out": round(t, 4), "dur": round(len(tl) / SR, 4), "gap": True})
    return np.concatenate(out), edl


def _span(seg: dict) -> float:
    """Source seconds a segment plays: its output length times its rate."""
    return seg["dur"] * seg.get("rate", 1.0)


def src_to_out(edl: list[dict], src: float, snap: bool = False) -> float | None:
    """Where a source second landed in the output, or None if it was cut.

    `snap`: a second inside a shortened pause lands where the cut is - a
    Whisper word's edge often sits a little inside the silence around it.
    A segment with a `rate` (`_speed_up`) plays its source that much faster.
    """
    for seg in edl:
        if seg.get("gap"):
            continue
        if seg["src"] <= src <= seg["src"] + _span(seg):
            return seg["out"] + (src - seg["src"]) / seg.get("rate", 1.0)
    if snap:
        # The neighbours in the *source*: with pickups joined on the end
        # (2026-11-24) the output no longer runs through the source in
        # order, and the first later piece by output was a pickup a minute
        # earlier - a caption after a sound example started 8 s early.
        segs = [s for s in edl if not s.get("gap")]
        prev = max((s for s in segs if s["src"] + _span(s) < src),
                   key=lambda s: s["src"], default=None)
        nxt = min((s for s in segs if s["src"] > src),
                  key=lambda s: s["src"], default=None)
        if prev and nxt and nxt["out"] - (prev["out"] + prev["dur"]) < 1e-3:
            return nxt["out"]            # inside a cut made within one take
    return None


def out_to_src(edl: list[dict], t: float, near: float = 0.0) -> float | None:
    """The source second an output second plays, or None in a gap.

    `near`: a second up to that far into a gap takes the nearest speech -
    a word at a sentence's very start sits right against the gap before it.
    """
    for seg in edl:
        if seg.get("gap"):
            continue
        if seg["out"] <= t <= seg["out"] + seg["dur"]:
            return seg["src"] + (t - seg["out"]) * seg.get("rate", 1.0)
    if near:
        best = None
        for seg in edl:
            if seg.get("gap"):
                continue
            for edge, src in ((seg["out"], seg["src"]),
                              (seg["out"] + seg["dur"], seg["src"] + _span(seg))):
                d = abs(edge - t)
                if d <= near and (best is None or d < best[0]):
                    best = (d, src)
        if best:
            return best[1]
    return None


def _extra_words(voice: np.ndarray, script: list[str], workdir: Path,
                 bounds: set[int] | None = None):
    """Output-second ranges of phrases heard in `voice` the script lacks.

    **Why (2026-11-22, the second recording).** Whisper on the whole file
    wrote a repeated phrase once and stretched a word over the repeat ("So the
    rule became [so the rule became] simple", "The [second... the] second
    sentence"), so no cut based on its words could find it. The assembled
    voice, transcribed on its own, is what a viewer hears: a run of two or
    more words there that the script does not have is a stumble.

    **One word is enough at a sentence's edge** (`bounds`: the script
    indices where a sentence starts; 2026-11-23, his review of that cut:
    "we let some parts of the sound which are not part of the sentence in
    between"). The leftovers were single words of the failed attempt just
    before a retake - "stops *begin*, and one track every time", "*paragraph.*
    And here, the whole paragraph". Inside a sentence one word is more often
    Whisper's than his, so there it still takes two.
    """
    import soundfile as sf
    wav = workdir / "check.wav"
    sf.write(str(wav), voice, SR)
    ws = transcribe(wav, deterministic=True)
    flat, owner = [], []
    for k, w in enumerate(ws):
        for t in norm(w["w"]):
            flat.append(t)
            owner.append(k)
    sm = difflib.SequenceMatcher(None, script, flat, autojunk=False)
    out = []
    for op, a0, a1, b0, b1 in sm.get_opcodes():
        edge = b1 - b0 == 1 and bounds is not None and a0 in bounds
        if op == "insert" and (b1 - b0 >= 2 or edge):
            # The same many words just before it: the earlier copy, which
            # may be the one to cut (`_choose_cut`). A single edge word has
            # none - the word before it is the last of another sentence.
            pb = b0 - (b1 - b0)
            out.append({"t0": ws[owner[b0]]["s"], "t1": ws[owner[b1 - 1]]["e"],
                        "prev": ws[owner[pb]]["s"] if pb >= 0 and not edge else None,
                        "text": " ".join(ws[k]["w"].strip()
                                         for k in range(owner[b0], owner[b1 - 1] + 1))})
    return out


def _render(audio: np.ndarray, pieces) -> np.ndarray:
    return np.concatenate([_fade(audio[int(a * SR):int(b * SR)].copy())
                           for a, b in pieces] or [np.zeros(1, np.float32)])


def _choose_cut(audio: np.ndarray, pieces, tokens: list[str], options, workdir: Path,
                before=(), after=(), before_tokens=(), after_tokens=()):
    """Of `options` (each a list of source ranges to cut from this
    sentence's `pieces`), the one whose result reads most like `tokens`,
    transcribed on its own - or None when no cut reads better than none.

    A phrase said twice is heard twice, but which copy is the clean one,
    and whether Whisper heard one word too many, it cannot say: "So the rule
    became... so the rule became simple" lost its only "simple" when the
    later copy was cut (2026-11-22). So each choice is built and listened to,
    with the sentence before and after it (`before`/`after` pieces, and their
    tokens): a title like "The voice" on its own is too short for Whisper to
    read at all.
    """
    import soundfile as sf
    variants = [pieces] + [_cut_out([pieces], [opt])[0] for opt in options]
    tokens = list(before_tokens) + list(tokens) + list(after_tokens)
    gap = np.zeros(SR, np.float32)
    pause = np.zeros(int(0.4 * SR), np.float32)
    pre = [_render(audio, before), pause] if before else []
    post = [pause, _render(audio, after)] if after else []
    chunks, spans, t = [], [], 0
    for v in variants:
        x = np.concatenate(pre + [_render(audio, v)] + post)
        chunks += [x, gap]
        spans.append((t, t + len(x)))
        t += len(x) + len(gap)
    wav = workdir / "choose.wav"
    sf.write(str(wav), np.concatenate(chunks), SR)
    wav16 = workdir / "choose16.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(wav), "-ar", "16000",
                    "-ac", "1", str(wav16)], check=True, capture_output=True)
    if not WHISPER_PYTHON.exists():
        return None
    per = _whisper(wav16, [(a // 3, b // 3) for a, b in spans], deterministic=True)["pieces"]
    def score(ws):
        heard = [t for w in ws for t in norm(w["w"])]
        return difflib.SequenceMatcher(None, tokens, heard, autojunk=False).ratio()
    scores = [score(ws) for ws in per]
    if os.environ.get("RECORDED_DEBUG"):
        for s, ws in zip(scores, per):
            print(f"    {s:.3f} {' '.join(w['w'].strip() for w in ws)}")
    # The phrase was heard in the whole cut; with only a sentence either
    # side Whisper may hear past it ("The second said. The second sentence"
    # read back as clean, 2026-11-22). So a cut that reads no worse than
    # none is taken; one that loses a script word reads worse and is not.
    best = 1 + int(np.argmax(scores[1:]))
    if scores[best] < scores[0] - 0.005:
        return None
    return options[best - 1]


SPEED_RANGE = (1.0, 1.5)


def _wpm(sentences, voice_s: float) -> float:
    words = sum(len(norm(_spoken(c)[1])) for s in sentences for c in s)
    return words / max(voice_s, 1e-6) * 60


def _speed_up(voice: np.ndarray, edl: list[dict], speed: float):
    """The speech `speed` times faster at the same pitch; gaps as they are.

    **Why (2026-11-22, his review of the first recorded long form):** "speed
    up my voice with about 1.25 or 1.5 without sounding high pitched. I read
    slower because I'm not native." Each run of speech between two gaps is
    stretched with ffmpeg's `atempo` (pitch kept); the gaps - room tone where
    a sound example plays, the scripted pauses, the tail - keep their length,
    so the examples still land where the captions put them. Every speech
    segment gets a `rate`, which `src_to_out` and the camera box
    (`facecam`, the face sped up with it) read.
    """
    if abs(speed - 1.0) < 1e-3:
        return voice, edl
    import soundfile as sf
    import tempfile
    starts = [int(round(s["out"] * SR)) for s in edl] + [len(voice)]
    out, new, t = [], [], 0.0
    k = 0
    tmp = Path(tempfile.mkdtemp(prefix="speed-"))
    while k < len(edl):
        if edl[k].get("gap"):
            piece = voice[starts[k]:starts[k + 1]]
            out.append(piece)
            new.append({"out": round(t, 4), "dur": round(len(piece) / SR, 4), "gap": True})
            t += len(piece) / SR
            k += 1
            continue
        j = k
        while j < len(edl) and not edl[j].get("gap"):
            j += 1
        x = voice[starts[k]:starts[j]]
        sf.write(str(tmp / "in.wav"), x, SR)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp / "in.wav"),
                        "-af", f"atempo={speed:.4f}", "-ar", str(SR), "-ac", "1",
                        str(tmp / "out.wav")], check=True, capture_output=True)
        y, _ = sf.read(str(tmp / "out.wav"), dtype="float32")
        ratio = len(y) / max(1, len(x))
        for m in range(k, j):
            new.append({"out": round(t + (starts[m] - starts[k]) / SR * ratio, 4),
                        "dur": round((starts[m + 1] - starts[m]) / SR * ratio, 4),
                        "src": edl[m]["src"], "rate": round(1 / ratio, 5)})
        out.append(_fade(y))
        t += len(y) / SR
        k = j
    return np.concatenate(out).astype(np.float32), new


# ---------------------------------------------------------------------------
# the entry point the engine calls
# ---------------------------------------------------------------------------

def _spoken(chunk) -> tuple[str, str]:
    return (chunk, chunk) if isinstance(chunk, str) else (chunk[0], chunk[1])


def build_narration_recorded(sentences, workdir: Path, rec: Recording,
                             gap=0.55, tail: float = 1.2):
    """`build_narration_aligned`'s contract, from a recording.

    Returns `(track, captions, total)`. Captions are the script's chunks,
    timed by the words of the take that was kept.
    """
    import soundfile as sf
    from .voiceover import Caption

    workdir = Path(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    gaps = ([float(gap)] * len(sentences) if isinstance(gap, (int, float))
            else [g if isinstance(g, Pause) else float(g) for g in gap])
    # A recording keeps its scripted pauses only where they are written beats
    # (a sound example, a chapter's way in: `LONG_GAP` and up); every other
    # pause is at most `max_pause` - the scripts' 0.45-0.6 s are for a
    # synthetic voice (2026-11-23, "reduce the gap between some sentences").
    gaps = [g if _written(g) else min(g, rec.max_pause) for g in gaps]

    # Script words per sentence, and which chunk each word belongs to.
    sent_words, word_chunk = [], []
    for sent in sentences:
        toks, owner = [], []
        for ci, chunk in enumerate(sent):
            for t in norm(_spoken(chunk)[1]):
                toks.append(t)
                owner.append(ci)
        sent_words.append(toks)
        word_chunk.append(owner)

    words = transcribe(rec.audio)
    takes = align(sent_words, words, rec.window, rec.pickups_from)
    audio = load_audio(rec.audio)
    spans, joined = _bounds(takes, words, audio, gaps, rec.max_pause)
    if rec.refine:
        edges = _refine(rec.audio, audio, spans, sent_words,
                        [words[tk.last]["s"] for tk in takes])
        spans, joined = _bounds(takes, words, audio, gaps, rec.max_pause, edges)
    for key, (pa, pb) in (rec.pins or {}).items():
        want = norm(key)
        i = next((k for k, sw in enumerate(sent_words) if sw == want), None)
        if i is None:
            # A Short cut from a long form shares its pins and may leave the
            # line out; a typo shows here too.
            print(f"recorded: the pin {key!r} matches no line here - skipped")
            continue
        spans[i] = [float(pa), float(pb)]
        takes[i].cuts, takes[i].pairs = [], _pin_pairs(sent_words[i], words, pa, pb)
        joined[i] = False
        if i + 1 < len(joined):
            joined[i + 1] = False
    # The pauses carried breaths and clicks: room tone between the words,
    # then the stumbles inside a take cut out (`clean_gaps`, `_junk`).
    src = clean_gaps(audio, words) if rec.gaps_clean else audio
    # The pickups shaped to the take *after* the gaps are cleaned, on the
    # cleaned audio: every decision before it - the edges, which hiss is a
    # word's "s" and which is a breath - is made on the recording as it was.
    # Matched first, the "s" of "mistakes" read as a breath and went
    # (2026-11-24, "we cut the S from the word mistakes at the end").
    if rec.pickups_at:
        src = match_pickups(src, rec.pickups_at)
    parts = (_tighten(src, spans, rec.inner_pause, rec.inner_keep)
             if rec.inner_pause else [[tuple(s)] for s in spans])
    quiet = _floor_db(audio) + 15
    ranges = [[(_edge(audio, words[w1]["e"], words[w2]["s"], quiet, back=False) + 0.02,
                _edge(audio, words[w2]["s"], words[w1]["e"], quiet, back=True) - 0.02)
               for w1, w2 in tk.cuts] for tk in takes]
    ranges = [[(a, b) for a, b in r if b - a > 0.05] for r in ranges]
    if any(ranges):
        print(f"recorded: {sum(map(len, ranges))} stumble(s) cut out inside takes")
        parts = _cut_out(parts, ranges)
    if rec.drops:
        parts = _cut_out(parts, [[tuple(d) for d in rec.drops]] * len(parts))
    voice, edl = _assemble(src, spans, joined, gaps, tail, parts)
    # Listen to the cut: a phrase heard in it that the script lacks is a
    # stumble Whisper hid on the whole file - cut it and listen again.
    script = [t for s in sent_words for t in s]
    bounds, k = {len(script)}, 0
    for s in sent_words:
        bounds.add(k)
        k += len(s)
    rec.extra = []
    for _ in range(rec.check_rounds):
        changed = []
        for x in _extra_words(voice, script, workdir, bounds):
            s0 = out_to_src(edl, x["t0"] - 0.02, near=0.15)
            s1 = out_to_src(edl, x["t1"] + 0.02, near=0.15)
            if s0 is None or s1 is None or s1 - s0 < 0.1:
                print(f"recorded: heard \"{x['text']}\", not placed in the source")
                continue
            i = next((k for k, (a, b) in enumerate(spans) if a - 0.05 <= s0 <= b + 0.05), None)
            if i is None:
                print(f"recorded: heard \"{x['text']}\", outside every take")
                continue
            # Cut at the quietest point right at each word boundary: sliding
            # to the nearest silence ran into "the" when "now the" had none
            # between them (2026-11-22).
            s0 = _quietest(audio, s0 - 0.08, s0 + 0.04)
            s1 = _quietest(audio, s1 - 0.04, s1 + 0.08)
            options = [[(s0, s1)]]                            # the later copy
            p0 = out_to_src(edl, x["prev"] - 0.02, near=0.15) if x["prev"] is not None else None
            if p0 is not None and p0 < s0 - 0.1:
                p0 = _quietest(audio, p0 - 0.08, p0 + 0.04)
                options.append([(p0, s0)])                    # the earlier one
            pick = _choose_cut(
                src, parts[i], sent_words[i], options, workdir,
                before=parts[i - 1] if i else (), after=parts[i + 1] if i + 1 < len(parts) else (),
                before_tokens=sent_words[i - 1] if i else (),
                after_tokens=sent_words[i + 1] if i + 1 < len(parts) else ())
            if pick is None:
                print(f"recorded: heard \"{x['text']}\" in line {i + 1}; no cut reads better")
                continue
            parts[i] = _cut_out([parts[i]], [pick])[0]
            which = "earlier" if pick is not options[0] else "later"
            changed.append(f"{x['text']} ({which} copy)")
        if not changed:
            break
        rec.extra += changed
        print(f"recorded: heard {len(changed)} phrase(s) the script lacks; cut: "
              + "; ".join(changed))
        voice, edl = _assemble(src, spans, joined, gaps, tail, parts)
    speed = rec.speed
    if rec.target_wpm:
        spoken = sum(s["dur"] for s in edl if not s.get("gap"))
        speed = float(np.clip(rec.target_wpm / _wpm(sentences, spoken), *SPEED_RANGE))
    rec.applied_speed = speed
    if abs(speed - 1.0) >= 1e-3:
        print(f"recorded: speech {speed:.2f}x faster, pitch kept")
        voice, edl = _speed_up(voice, edl, speed)

    raw = workdir / "recorded.raw.wav"
    track = workdir / "narration.wav"
    sf.write(str(raw), voice, SR)
    if rec.clean:
        _level(raw, track, clean_chain(_floor_db(audio),
                                       match_eq(src) if rec.match else None,
                                       speech_db(voice)),
               rec.loudness)
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw),
                        "-ar", str(SR), "-ac", "2", str(track)],
                       check=True, capture_output=True)
    raw.unlink(missing_ok=True)
    total = len(voice) / SR

    # Captions: each chunk runs from its first heard word to its last.
    captions, rec.sentence_times = [], []
    for si, (sent, tk) in enumerate(zip(sentences, takes)):
        a_out = src_to_out(edl, spans[si][0]) or 0.0
        b_out = src_to_out(edl, spans[si][1] - 1e-4) or a_out
        times: dict[int, list[float]] = {}
        for wi, ci in enumerate(word_chunk[si]):
            ti = tk.pairs.get(wi)
            if ti is None:
                continue
            # A word is timed inside its own line's audio: where a line read
            # straight into the next is split after Whisper's boundary
            # (`_split`), the next line's first word starts earlier than its
            # line, inside this one - and "and the same template" came up
            # 1.8 s early, before the pause, the reel's card with it
            # (2026-11-24).
            ws_, we_ = words[ti]["s"], words[ti]["e"]
            a_, b_ = spans[si]
            if a_ + 2e-3 < b_ - 2e-3:
                lo_, hi_ = a_ + 1e-3, b_ - 1e-3       # clear of the rounded edges
                ws_, we_ = min(max(ws_, lo_), hi_), min(max(we_, lo_), hi_)
            s = src_to_out(edl, ws_, snap=True)
            e = src_to_out(edl, we_, snap=True)
            if s is None or e is None:
                continue
            times.setdefault(ci, []).extend([s, e])
        n = len(sent)
        starts, ends = [], []
        for ci in range(n):
            if ci in times:
                starts.append(min(times[ci]))
                ends.append(max(times[ci]))
            else:                        # a chunk none of whose words matched
                starts.append(None)
                ends.append(None)
        # Fill the unmatched ones by spreading them over the gap they sit in.
        for ci in range(n):
            if starts[ci] is None:
                lo = ends[ci - 1] if ci > 0 and ends[ci - 1] is not None else a_out
                hi_i = next((k for k in range(ci + 1, n) if starts[k] is not None), None)
                hi = starts[hi_i] if hi_i is not None else b_out
                k = (hi_i if hi_i is not None else n) - ci
                step = max(hi - lo, 0.0) / max(k, 1)
                starts[ci], ends[ci] = lo, lo + step
        first = len(captions)
        for ci, chunk in enumerate(sent):
            cap = _spoken(chunk)[0]
            s = max(starts[ci], captions[-1].end if captions else 0.0)
            captions.append(Caption(cap, s, max(ends[ci], s + 0.05)))
        # Where the sentence is spoken, before captions are held over the
        # pause - the camera box leaves with it (`facecam.cues`).
        rec.sentence_times.append((captions[first].start,
                                   max(c.end for c in captions[first:])))
    # Hold each caption until the next one, as the synthesised path does;
    # `speech_end` (set at construction) keeps where the voice stopped.
    for a, b in zip(captions, captions[1:]):
        a.end = max(a.end, b.start)
    if captions:
        captions[-1].end += tail

    _write_sidecars(rec, sentences, sent_words, takes, words, edl, spans)
    rec.captions = captions
    return track, captions, total


def _stem(rec: Recording, sentences) -> Path:
    h = hashlib.sha1(json.dumps(
        [[_spoken(c)[1] for c in s] for s in sentences]).encode()).hexdigest()[:8]
    return rec.audio.with_name(f"{rec.audio.stem}.{h}")


def sidecar(rec: Recording, sentences, kind: str) -> Path:
    """`NAME.<script hash>.edl.json` / `.report.txt` next to the recording."""
    stem = _stem(rec, sentences)
    return stem.with_name(f"{stem.name}.{kind}")


def _write_sidecars(rec, sentences, sent_words, takes, words, edl, spans):
    edl_path = sidecar(rec, sentences, "edl.json")
    rec.edl = edl_path
    edl_path.write_text(json.dumps({
        "audio": str(rec.audio),
        "face": str(rec.face) if rec.face else None,
        "segments": edl,
    }, indent=1))

    lines = [f"Recording: {rec.audio.name}", ""]
    pinned = {tuple(norm(k)) for k in (rec.pins or {})}
    kept = 0.0
    flags = 0
    for si, (tk, toks) in enumerate(zip(takes, sent_words)):
        # What is heard in the cut: the stumbles cut out are not in it.
        gone = {k for w1, w2 in tk.cuts for k in range(w1 + 1, w2)}
        heard = [t for k in range(tk.first, tk.last + 1) if k not in gone
                 for t in norm(words[k]["w"])]
        sm = difflib.SequenceMatcher(None, toks, heard, autojunk=False)
        notes = [f"cut out: \"{' '.join(words[k]['w'].strip() for k in range(w1 + 1, w2))}\""
                 for w1, w2 in tk.cuts]
        for op, a0, a1, b0, b1 in sm.get_opcodes():
            if op == "equal":
                continue
            s_txt, h_txt = " ".join(toks[a0:a1]), " ".join(heard[b0:b1])
            if op == "replace" and all(_same(x, y) for x, y in
                                       zip(toks[a0:a1], heard[b0:b1])) \
                    and a1 - a0 == b1 - b0:
                continue
            if op == "delete":
                notes.append(f"not said: \"{s_txt}\"")
            elif op == "insert":
                notes.append(f"added: \"{h_txt}\"")
            else:
                notes.append(f"said \"{h_txt}\" for \"{s_txt}\"")
        # A word Whisper stretched over a second hides what it did not
        # write down: "Here is", a throat-clear, then the whole line again
        # came back as one 1.5 s "what" (the pickups, 2026-11-24). Listen,
        # and pin the clean read (`pins=`).
        if tuple(toks) not in pinned:
            for k in range(tk.first, tk.last + 1):
                long = words[k]["e"] - words[k]["s"]
                if k not in gone and long >= LONG_WORD:
                    notes.append(f"\"{words[k]['w'].strip()}\" lasts {long:.1f}s at "
                                 f"{words[k]['s']:.2f}: a stumble may hide in it - "
                                 f"listen, and pin the clean read")
                    print(f"recorded: line {si + 1}: \"{words[k]['w'].strip()}\" "
                          f"lasts {long:.1f}s at {words[k]['s']:.2f}s - listen to it")
        a, b = spans[si]
        kept += b - a
        mark = "!" if notes else " "
        flags += bool(notes)
        retake = f", {tk.others} other take(s) cut" if tk.others else ""
        lines.append(f"{mark} {si + 1:>3}. [{a:7.2f}-{b:7.2f}s, "
                     f"{tk.score:.0%} matched{retake}] {' '.join(toks)}")
        for nline in notes:
            lines.append(f"        {nline}")
    src_total = words[-1]["e"] if words else 0.0
    lines += ["", f"{len(takes)} sentences, {flags} with differences. "
                  f"Kept {kept:.1f}s of {src_total:.1f}s recorded."]
    report = sidecar(rec, sentences, "report.txt")
    rec.report = report
    report.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[-1:]) + f"  Report: {report}")
