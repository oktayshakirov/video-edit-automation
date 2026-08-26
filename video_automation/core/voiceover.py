"""Narrated shorts — spoken quote with captions synced to it.

Two sync modes, and the second one replaced the first for narrated quotes.

**Per-phrase** (`build_narration`) — each caption is spoken as its own file and
shown for exactly its measured duration. Timing is exact by construction. Its
cost is prosody: the engine sees each fragment with no context, so every one
gets a terminal falling contour and its own pause. Rejected on real output — a
single-word caption like "tuesday" came out as an isolated announcement, and the
whole read landed robotic. Still correct when the captions really are separate
utterances.

**Per-sentence with alignment** (`build_narration_aligned`) — the sentence is
spoken *whole*, so the prosody is a real sentence contour, and caption
boundaries inside it are recovered afterwards. That means chunking the captions
finely no longer slows the delivery down, which is the whole point.

Recovering those boundaries needs no aligner model. Each chunk is also
synthesised alone as a throwaway timing reference, the references are
concatenated, and the two are DTW-aligned on log-mel — same voice, same engine,
same speed, so the only difference between the sequences is the prosody the
context added. Measured against a syllable-count expectation the boundaries
agree to ~0.19s mean, and they disagree in the direction that favours the
alignment (it gives a pre-comma word its real length, which syllable counting
cannot know). Chunks are on screen for a second or more, so a fifth of a second
of placement error is not visible.

Trimming matters: Kokoro pads each isolated render with silence, and leaving it
in shifts the reference enough to put a boundary a full word early.

The TTS backend is isolated in `synth_phrase`. Three are wired up, in order of
quality: kokoro (local, unlimited, default), edge (Microsoft neural voices over
the network, free, no key), say (macOS, legacy, last resort). A hosted API drops
in at the same seam. Because caption timing comes from *measured* audio duration
rather than a prediction, changing engine cannot desynchronise the captions.
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from . import voices
from .vertical import (FONT_CAPTION, FONT_CAPTION_INDEX, FONT_CAPTION_SIZE,
                       FONT_QUOTE, FONT_QUOTE_INDEX, FONT_QUOTE_SIZE,
                       OUT_H, OUT_W,
                       render_short, render_text_png, sample_bg_luma,
                       stack_tile_size)

TTS_BACKEND = "kokoro"                      # "kokoro" | "edge" | "say"

# Kokoro-82M, Apache 2.0, fully local and unlimited. Installed as kokoro-onnx
# rather than the PyTorch package: the latter pulls spacy, which has no Python
# 3.13 wheels and fails to build, and ~2.5GB of torch besides. The ONNX build
# reuses the onnxruntime already present and totals ~350MB.
KOKORO_DIR = Path.home() / ".local/share/kokoro"

# A voice is a (510, 1, 256) style tensor, not a model, so a weighted sum of
# two of them is a new speaker identity the model renders as one person — not
# two voices mixed as audio.
#
# The approved voice is a blend. `am_onyx` was chosen by ear over five
# alternatives, but the model card grades it D on 10-100 minutes of data, the
# weakest of the American males. `am_puck` is C+ with hours. 60/40 keeps the
# onyx character on the steadier base and was picked over straight onyx and
# eight other mixes for sounding more human.
KOKORO_VOICE: "str | dict[str, float]" = voices.APPROVED_DRONE.voice
KOKORO_SPEED = 0.88     # unhurried; motivational reads are not brisk

# Kokoro has no emotion parameter, so mood is carried by pace, voice choice and
# post-processing. Stated plainly because it is a real limit, not a tuned
# feature — nothing here makes the model perform an emotion.
KOKORO_MOODS = {
    "reflective": 0.84,
    "motivational": 0.95,
    "melancholic": 0.82,
    "sad": 0.80,
    "neutral": 0.90,
}

# Post-processing does more for mood than pace does. The melancholic chain is
# approved and should not be re-tuned: the ~4% pitch-down (asetrate, with atempo
# restoring real time) and the short echo tail are what sell it. Without them it
# is the same voice reading slower.
POST_CHAINS = {
    # Deliberately the MELANCHOLIC chain rather than the approved profile's —
    # those were the same thing until leo was approved, and leo uses SOFT.
    # Wiring this to APPROVED_DRONE.chain would silently redefine what the
    # "melancholic" mood means for anything still asking for it.
    "melancholic": voices.MELANCHOLIC,
}

# Every registered profile is also reachable as a mood, because a mood here is
# exactly what a profile is: a speed plus a post chain. Registering them means
# the render path needs no new parameter — `profile_args()` below hands back
# the `voice=`/`mood=` pair that `render_narrated` already accepts.
for _name, _p in voices.PROFILES.items():
    KOKORO_MOODS[_name] = _p.speed
    POST_CHAINS[_name] = _p.chain


def profile_args(name: str) -> dict:
    """Spread into `render_narrated` to use a named profile.

        render_narrated(..., **profile_args("nicole"))

    Voice and chain must travel together — half a profile is a different voice.
    """
    return {"voice": voices.get(name).voice, "mood": name}

# Microsoft's current neural voices, reached through the Edge endpoint: free,
# no API key, ~1MB install, and clearly the most natural of the three. The
# "Multilingual" variants are the newest generation and the ones worth using.
# Trade-off: it is a network call and heavy use can be rate-limited, so it is
# the fallback rather than the default now that Kokoro runs locally.
EDGE_VOICE = "en-US-AndrewMultilingualNeural"
# Delivery per mood. The free Edge endpoint ignores SSML express-as styles, so
# tone is shaped with the levers it does honour — rate and pitch — plus voice
# choice, which does more for mood than either.
EDGE_MOODS = {
    "reflective": {"rate": "-14%", "pitch": "-3Hz"},
    "motivational": {"rate": "-6%", "pitch": "+2Hz"},
    "sad": {"rate": "-18%", "pitch": "-6Hz"},
    "neutral": {"rate": "-10%", "pitch": "+0Hz"},
}

DEFAULT_VOICE = "Samantha"                  # only used by the `say` backend
# Silence between phrases is the one honest lever on total runtime — the script
# sets how long the speech takes, and trimming words to hit a number is the
# wrong trade. A melancholic read wants a real beat between lines anyway: ~1s
# reads as deliberate, where 0.18s reads as a list.
GAP = 0.18          # seconds of silence between phrases
TAIL = 1.0          # hold the last caption this long after the audio ends

CAPTION_MAX_W = 920         # wider than the silent card: one phrase, one line

KOKORO_SR = 24000           # the model's native rate; alignment works pre-resample
ALIGN_HOP = 128             # ~5.3ms frames — finer than the error we care about
TRIM_DB = 35                # Kokoro's padding sits well below this
MIN_CHUNK = 0.20            # floor on a caption's span, so a bad warp cannot
                            # collapse one to zero frames


_KOKORO = None


def _kokoro():
    """Load the model once — it is ~325MB and the load dominates a short script."""
    global _KOKORO
    if _KOKORO is None:
        from kokoro_onnx import Kokoro
        _KOKORO = Kokoro(str(KOKORO_DIR / "kokoro-v1.0.onnx"),
                         str(KOKORO_DIR / "voices-v1.0.bin"))
    return _KOKORO


@dataclass
class Caption:
    text: str
    start: float
    end: float
    # Where the voice actually stops, before `end` gets stretched to the next
    # caption's start (the hold-until-next rule a few lines below). Defaults
    # to `end` for any caller that never sets it, which is every use except
    # per-word karaoke — that is the one consumer that needs the real speech
    # boundary rather than the display boundary, because timing words across
    # the *displayed* span means the last word or two of a short sentence
    # lights up during the sentence's own trailing silence rather than while
    # it is being spoken.
    speech_end: float = 0.0

    def __post_init__(self):
        if not self.speech_end:
            self.speech_end = self.end


# A caption line, or a (caption, spoken) pair when the engine needs a different
# spelling than the screen does.
Phrase = str | tuple[str, str]

# A voice name, a {name: weight} blend, or None for the approved default.
VoiceSpec = "str | dict[str, float] | None"


def split_phrases(text: str, max_words: int = 6, min_words: int = 3) -> list[str]:
    """Break a quote into caption-sized phrases.

    Punctuation wins over word count — a phrase ending where the sentence
    breathes reads and speaks better than one chopped at an arbitrary sixth
    word. But splitting on every comma throws up two-word fragments that flash
    past before they can be read ("lost here," measured 0.65s), so anything
    under `min_words` is merged forward into its neighbour.
    """
    parts = [p.strip() for p in re.split(r"(?<=[.,;:!?])\s+", text) if p.strip()]

    merged: list[str] = []
    for part in parts:
        if merged and len(part.split()) < min_words:
            merged[-1] = f"{merged[-1]} {part}"
        elif merged and len(merged[-1].split()) < min_words:
            merged[-1] = f"{merged[-1]} {part}"
        else:
            merged.append(part)

    out: list[str] = []
    for part in merged:
        words = part.split()
        while len(words) > max_words:
            out.append(" ".join(words[:max_words]))
            words = words[max_words:]
        if words:
            # Avoid leaving a runt at the end of a long part.
            if out and len(words) < min_words:
                out[-1] = f"{out[-1]} {' '.join(words)}"
            else:
                out.append(" ".join(words))
    return out


def voice_style(voice=None):
    """Resolve a voice spec to something `Kokoro.create` accepts.

    A name passes through; a `{name: weight}` mapping is blended into a style
    tensor. `None` means the approved default, which is itself a blend.
    """
    if voice is None:
        voice = KOKORO_VOICE
    if isinstance(voice, dict):
        k = _kokoro()
        return sum(k.get_voice_style(n) * w for n, w in voice.items())
    return voice


def _synth_raw(text: str, voice, mood: str) -> "np.ndarray":
    """Kokoro samples at KOKORO_SR, trimmed of the padding it adds.

    Alignment-only path, so it stays on the kokoro backend rather than going
    through `synth_phrase`'s file round-trip and post-processing.
    """
    import librosa
    import numpy as np                                          # noqa: F401
    audio, _ = _kokoro().create(text, voice=voice_style(voice),
                                speed=KOKORO_MOODS.get(mood, KOKORO_SPEED),
                                lang="en-us")
    trimmed, _ = librosa.effects.trim(audio.astype("float32"), top_db=TRIM_DB)
    return trimmed


def align_chunks(sentence_audio: "np.ndarray", chunks: list[str],
                 voice: VoiceSpec = None, mood: str = "melancholic") -> list[float]:
    """End time of each caption chunk within a naturally-spoken sentence.

    Synthesises each chunk alone as a timing reference, concatenates them, and
    DTW-aligns that against the real sentence on log-mel. The warp path maps a
    reference boundary onto a timestamp in the natural read.

    The references are throwaway — none of that audio is used, only its
    boundaries. Same engine, voice and speed on both sides, so the warp is
    absorbing the prosody that sentence context added and nothing else.
    """
    import librosa
    import numpy as np

    if len(chunks) == 1:
        return [len(sentence_audio) / KOKORO_SR]

    ref_parts, bounds, t = [], [], 0.0
    for c in chunks:
        a = _synth_raw(c, voice, mood)
        ref_parts.append(a)
        t += len(a) / KOKORO_SR
        bounds.append(t)
    ref = np.concatenate(ref_parts)

    def logmel(y):
        m = librosa.feature.melspectrogram(y=y, sr=KOKORO_SR,
                                           hop_length=ALIGN_HOP, n_mels=40)
        return librosa.power_to_db(m)

    _, path = librosa.sequence.dtw(X=logmel(ref), Y=logmel(sentence_audio),
                                   metric="euclidean")
    path = path[::-1]                       # (ref_frame, sentence_frame), ascending
    fps = KOKORO_SR / ALIGN_HOP

    ends, last = [], 0.0
    total = len(sentence_audio) / KOKORO_SR
    for b in bounds:
        rf = min(int(b * fps), int(path[-1][0]))
        at = float(path[np.searchsorted(path[:, 0], rf)][1]) / fps
        last = min(max(at, last + MIN_CHUNK), total)   # monotonic, never zero-length
        ends.append(last)
    ends[-1] = total
    return ends


def synth_phrase(text: str, out: Path, voice: VoiceSpec = None,
                 rate: int = 165, backend: str = TTS_BACKEND,
                 mood: str = "reflective") -> float:
    """Render one phrase to audio and return its measured duration.

    The only place a TTS engine is named. Everything downstream works off the
    measured duration, so swapping engines — or moving to a hosted API — cannot
    desynchronise the captions.
    """
    raw = out.with_suffix(".raw.wav")

    if backend == "kokoro":
        import soundfile as sf
        audio, sr = _kokoro().create(
            text, voice=voice_style(voice),
            speed=KOKORO_MOODS.get(mood, KOKORO_SPEED), lang="en-us")
        sf.write(str(raw), audio, sr)
    elif backend == "edge":
        mood_args = EDGE_MOODS.get(mood, EDGE_MOODS["neutral"])
        raw = out.with_suffix(".raw.mp3")
        subprocess.run(
            [sys.executable, "-m", "edge_tts", "--voice", voice or EDGE_VOICE,
             f"--rate={mood_args['rate']}", f"--pitch={mood_args['pitch']}",
             "--text", text, "--write-media", str(raw)],
            check=True, capture_output=True)
    else:
        aiff = out.with_suffix(".aiff")
        subprocess.run(["say", "-v", voice or DEFAULT_VOICE, "-r", str(rate),
                        "-o", str(aiff), text], check=True, capture_output=True)
        raw = aiff

    post = ["-ar", "48000", "-ac", "2"]
    chain = POST_CHAINS.get(mood)
    if chain:
        post = ["-af", chain] + post
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), *post, str(out)],
                   check=True, capture_output=True)
    raw.unlink(missing_ok=True)

    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(out)],
        check=True, capture_output=True, text=True).stdout.strip()
    return float(dur)


def build_narration(text: str, workdir: Path, voice: VoiceSpec = None,
                    rate: int = 165, backend: str = TTS_BACKEND,
                    mood: str = "reflective",
                    phrases: list[Phrase] | None = None,
                    gap: float = GAP,
                    tail: float = TAIL) -> tuple[Path, list[Caption], float]:
    """Speak the quote phrase by phrase; return the mixed track and caption times.

    Pass `phrases` to override `split_phrases`. Written verse already carries its
    own line breaks, and those are better caption boundaries than anything the
    splitter can infer — it counts words, so a nine-word line becomes "the things
    you'll miss are never" / "the things you planned", which breaks the sentence
    in the one place it should not.

    An entry may be `(caption, speech)` to spell a word differently for the
    engine than for the screen. Needed for heteronyms: espeak phonemizes "read"
    as /ɹiːd/ in every context, so "i read a quote that said" is spoken in the
    present tense. The caption keeps the real spelling; only the engine sees
    "red".
    """
    workdir.mkdir(parents=True, exist_ok=True)
    pairs = [(p, p) if isinstance(p, str) else p
             for p in (phrases or split_phrases(text))]

    captions: list[Caption] = []
    pieces: list[Path] = []
    t = 0.0
    for i, (caption, spoken) in enumerate(pairs):
        wav = workdir / f"ph{i:02d}.wav"
        dur = synth_phrase(spoken, wav, voice, rate, backend, mood)
        captions.append(Caption(caption, t, t + dur + gap))
        pieces.append(wav)
        t += dur + gap

    # Concatenate with the gaps baked in, so audio and captions cannot drift.
    # The tail is real silence on the end of the track, not just a longer last
    # caption: the render maps this track with `-shortest`, so an audio track
    # shorter than the reported total silently truncates the video — which is
    # exactly what happened, and it cost 1.5s off the end of a finished cut.
    listing = workdir / "concat.txt"
    silence = workdir / "gap.wav"
    tail_wav = workdir / "tail.wav"
    for path, dur in ((silence, gap), (tail_wav, tail)):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                        f"anullsrc=r=48000:cl=stereo:d={dur}", str(path)],
                       check=True, capture_output=True)
    lines = []
    for p in pieces:
        lines.append(f"file '{p.name}'")
        lines.append(f"file '{silence.name}'")
    lines.append(f"file '{tail_wav.name}'")
    listing.write_text("\n".join(lines), encoding="utf-8")

    track = workdir / "narration.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", str(track)],
                   check=True, capture_output=True, cwd=workdir)
    if captions:
        captions[-1].end += tail
    return track, captions, t + tail


def build_narration_aligned(sentences: list[list[Phrase]], workdir: Path,
                            voice: VoiceSpec = None,
                            mood: str = "melancholic",
                            gap: "float | list[float]" = 0.55,
                            tail: float = TAIL,
                            ) -> tuple[Path, list[Caption], float]:
    """Speak each sentence whole; recover caption boundaries inside it.

    `sentences` is a list of sentences, each a list of caption chunks. A chunk
    may be a `(caption, spoken)` pair. The spoken halves are joined into one
    utterance, so punctuation on them shapes the delivery — keep the comma on
    "tuesday," and the engine will actually take that breath.

    `gap` is silence *between sentences only*. Chunking finely inside a sentence
    no longer costs anything, which is the reason this exists: captions can be
    one word without the read slowing to match.

    `gap` may be a float — the same silence after every sentence — or a list of
    exactly one float per sentence, when one beat has to be longer than the
    others. A reveal needs the pause before it to be longer than the pauses
    inside the setup, or it lands as just another line.

    A chunk whose *caption* is empty is spoken but never shown. The screen
    clears and only the voice carries it, which is a different instrument from
    a caption and worth having.
    """
    import soundfile as sf

    workdir.mkdir(parents=True, exist_ok=True)
    gaps = ([float(gap)] * len(sentences) if isinstance(gap, (int, float))
            else [float(g) for g in gap])
    if len(gaps) != len(sentences):
        raise ValueError(f"gap list must have one entry per sentence "
                         f"({len(sentences)}), got {len(gaps)}")
    captions: list[Caption] = []
    pieces: list[Path] = []
    t = 0.0

    for si, chunks in enumerate(sentences):
        pairs = [(c, c) if isinstance(c, str) else c for c in chunks]
        spoken = " ".join(s for _, s in pairs)

        audio = _synth_raw(spoken, voice, mood)
        raw = workdir / f"sent{si:02d}.raw.wav"
        wav = workdir / f"sent{si:02d}.wav"
        sf.write(str(raw), audio, KOKORO_SR)

        post = ["-ar", "48000", "-ac", "2"]
        chain = POST_CHAINS.get(mood)
        if chain:
            post = ["-af", chain] + post
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), *post, str(wav)],
                       check=True, capture_output=True)
        raw.unlink(missing_ok=True)

        # The post chain restores real time (atempo cancels asetrate) but its
        # echo adds a tail, so boundaries are scaled onto the processed length
        # rather than assumed equal.
        played = float(subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(wav)],
            check=True, capture_output=True, text=True).stdout.strip())
        scale = played / (len(audio) / KOKORO_SR)

        ends = align_chunks(audio, [s for _, s in pairs], voice, mood)
        prev = 0.0
        for (caption, _), end in zip(pairs, ends):
            captions.append(Caption(caption, t + prev * scale, t + end * scale))
            prev = end

        pieces.append(wav)
        t += played + gaps[si]

    listing = workdir / "concat.txt"
    tail_wav = workdir / "tail.wav"
    silences = [workdir / f"gap{i:02d}.wav" for i in range(len(gaps))]
    for path, dur in list(zip(silences, gaps)) + [(tail_wav, tail)]:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                        f"anullsrc=r=48000:cl=stereo:d={dur}", str(path)],
                       check=True, capture_output=True)
    lines = []
    for p, s in zip(pieces, silences):
        lines.append(f"file '{p.name}'")
        lines.append(f"file '{s.name}'")
    lines.append(f"file '{tail_wav.name}'")
    listing.write_text("\n".join(lines), encoding="utf-8")

    track = workdir / "narration.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", str(listing), "-c", "copy", str(track)],
                   check=True, capture_output=True, cwd=workdir)

    # Hold each caption until the next one arrives. Otherwise the inter-sentence
    # gap plays over an empty frame, which reads as a dropped caption rather than
    # as a beat.
    for a, b in zip(captions, captions[1:]):
        a.end = b.start
    if captions:
        captions[-1].end += tail
    return track, captions, t + tail


def render_narrated(src: Path, out: Path, start: float,
                    box: tuple[int, int, int, int], text: str,
                    workdir: Path, voice: VoiceSpec = None,
                    rate: int = 165,
                    font_size: "int | Callable[[str], int]" = FONT_QUOTE_SIZE,
                    backend: str = TTS_BACKEND, mood: str = "reflective",
                    phrases: list[Phrase] | None = None,
                    sentences: list[list[Phrase]] | None = None,
                    font_path: str = FONT_QUOTE,
                    font_index: int = FONT_QUOTE_INDEX,
                    y_frac: float = 0.34, stroke: int = 4,
                    max_w: int = CAPTION_MAX_W,
                    gap: "float | list[float]" = GAP, tail: float = TAIL) -> tuple[Path, float]:
    """Cut, crop, burn synced captions, and lay the narration underneath.

    Video length follows the narration rather than a fixed target — a caption
    cut off mid-sentence is worse than a clip a second longer than planned.

    Captions default to the stroked treatment rather than the halo: they move,
    so the type crosses whatever the footage happens to be doing under it, and a
    single ink colour chosen from one sampled frame will be wrong for some of
    them.

    Pass `sentences` for the aligned mode — whole sentences spoken naturally,
    captions chunked inside them. That is the right mode for a quote; `phrases`
    speaks each caption in isolation and reads robotic when the chunks are short.

    `font_size` may be a callable taking the caption text, so the one word a
    quote turns on can be set larger than the lines around it. `render_text_png`
    also takes `ink=`, so that word can be pulled out of the footage in colour
    on top of the size bump — pass a per-caption colour by wrapping the call,
    same pattern as `font_size`.

    Defaults to Iowan Old Style Italic — the approved quote face, chosen over
    Futura on the Sunset Sea Stack cut and now the default for every narrated
    quote, on one clip or stacked. Pass `font_path=FONT_CAPTION` to fall back
    to Futura if a particular cut wants the plainer face.
    """
    if sentences is not None:
        track, captions, total = build_narration_aligned(
            sentences, workdir, voice, mood, gap, tail)
    else:
        track, captions, total = build_narration(
            text, workdir, voice, rate, backend, mood, phrases, gap, tail)
    luma = sample_bg_luma(src, box, start + total / 2)

    # An empty caption is spoken but not shown — same rule as
    # `render_narrated_cuts`, so a reveal works on one clip or several.
    shown = [(i, c) for i, c in enumerate(captions) if c.text.strip()]
    pngs = []
    for i, c in shown:
        p = workdir / f"cap{i:02d}.png"
        size = font_size(c.text) if callable(font_size) else font_size
        render_text_png(c.text, p, size=size, bg_luma=luma,
                        font_path=font_path, font_index=font_index,
                        y_frac=y_frac, stroke=stroke, max_w=max_w)
        pngs.append(p)

    x, y, w, h = box
    chain = [f"[0:v]crop={w}:{h}:{x}:{y},scale={OUT_W}:{OUT_H}:flags=lanczos[v0]"]
    for n, (_, c) in enumerate(shown):
        src_lbl, dst_lbl = f"[v{n}]", f"[v{n+1}]"
        chain.append(
            f"{src_lbl}[{n+1}:v]overlay=0:0:enable='between(t,{c.start:.3f},{c.end:.3f})'{dst_lbl}"
        )
    # No fade to black — see `render_short`. Shorts loop, and the fade spent
    # the last half-second announcing the end instead of holding the picture.
    last = f"[v{len(shown)}]"
    chain.append(f"{last}null[vout]")

    cmd = ["ffmpeg", "-v", "error", "-y",
           "-ss", f"{start}", "-t", f"{total:.3f}", "-i", str(src)]
    for p in pngs:
        cmd += ["-i", str(p)]
    cmd += ["-i", str(track),
            "-filter_complex", ";".join(chain),
            "-map", "[vout]", "-map", f"{len(pngs)+1}:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out, total


def plan_cuts(captions: list[Caption], total: float, n: int,
              min_hold: float = 2.0) -> list[float]:
    """Cut points for `n` clips, snapped to caption boundaries.

    Cutting mid-caption reads as a mistake — the eye is on a line of type and
    the ground changes underneath it. Snapping to a boundary makes the cut
    land with the words, so it reads as punctuation instead.

    Targets are even thirds (or halves), then moved to the nearest caption
    start that leaves every segment at least `min_hold` long. A shot too short
    to register is worse than an uneven cut.
    """
    starts = [c.start for c in captions]
    cuts = [0.0]
    for k in range(1, n):
        target = total * k / n
        room = [s for s in starts
                if s >= cuts[-1] + min_hold and s <= total - min_hold * (n - k)]
        cuts.append(min(room, key=lambda s: abs(s - target)) if room else target)
    cuts.append(total)
    return cuts


def render_narrated_cuts(clips: list[tuple[Path, float, tuple[int, int, int, int]]],
                         out: Path, sentences: list[list[Phrase]], workdir: Path,
                         voice: VoiceSpec = None, mood: str = "melancholic",
                         font_size: "int | Callable[[str], int]" = FONT_QUOTE_SIZE,
                         font_path: str = FONT_QUOTE,
                         font_index: int = FONT_QUOTE_INDEX,
                         y_frac: float = 0.34, stroke: int = 4,
                         max_w: int = CAPTION_MAX_W,
                         ink: "Callable[[str], tuple[int,int,int,int] | None] | None" = None,
                         fps: int = 30,
                         gap: "float | list[float]" = GAP, tail: float = TAIL,
                         ) -> tuple[Path, float, list[float]]:
    """Narrated short cut across several clips instead of holding on one.

    `clips` is `[(src, source_in_point, crop_box), ...]`; each supplies one
    segment, in order. Cut points come from `plan_cuts`, so they land on
    caption boundaries rather than at arbitrary times.

    Sources must share frame rate and dimensions — `concat` demands it, and a
    silent conform would be worse than the refusal.

    Everything downstream of the narration is unchanged from `render_narrated`:
    same alignment, same caption treatment, same audio mapping.
    """
    track, captions, total = build_narration_aligned(
        sentences, workdir, voice, mood, gap, tail)

    cuts = plan_cuts(captions, total, len(clips))
    # Ink is sampled once, from the first clip, and the stroke carries the rest
    # — the type crosses several different backgrounds now, so no single
    # sampled colour could be right for all of them anyway.
    luma = sample_bg_luma(clips[0][0], clips[0][2], clips[0][1] + 1.0)

    # An empty caption is spoken but not shown — no PNG, no overlay, so the
    # frame is simply clear while the voice carries the line.
    shown = [(i, c) for i, c in enumerate(captions) if c.text.strip()]
    pngs = []
    for i, c in shown:
        p = workdir / f"cap{i:02d}.png"
        size = font_size(c.text) if callable(font_size) else font_size
        render_text_png(c.text, p, size=size, bg_luma=luma,
                        font_path=font_path, font_index=font_index,
                        y_frac=y_frac, stroke=stroke, max_w=max_w,
                        ink=ink(c.text) if ink else None)
        pngs.append(p)

    cmd = ["ffmpeg", "-v", "error", "-y"]
    for i, (src, src_in, _) in enumerate(clips):
        seg = cuts[i + 1] - cuts[i]
        cmd += ["-ss", f"{src_in}", "-t", f"{seg:.3f}", "-i", str(src)]
    for p in pngs:
        cmd += ["-i", str(p)]
    cmd += ["-i", str(track)]

    chain = []
    for i, (_, _, box) in enumerate(clips):
        x, y, w, h = box
        chain.append(f"[{i}:v]crop={w}:{h}:{x}:{y},scale={OUT_W}:{OUT_H}:"
                     f"flags=lanczos,fps={fps},setsar=1,settb=AVTB[c{i}]")
    chain.append("".join(f"[c{i}]" for i in range(len(clips)))
                 + f"concat=n={len(clips)}:v=1:a=0[base]")

    prev = "[base]"
    for n, (_, c) in enumerate(shown):
        dst = f"[v{n+1}]"
        chain.append(f"{prev}[{len(clips)+n}:v]overlay=0:0:"
                     f"enable='between(t,{c.start:.3f},{c.end:.3f})'{dst}")
        prev = dst
    chain.append(f"{prev}null[vout]")      # no fade to black — see `render_short`

    cmd += ["-filter_complex", ";".join(chain),
            "-map", "[vout]", "-map", f"{len(clips)+len(pngs)}:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out, total, cuts


def render_narrated_stack(top: tuple[Path, float, tuple[int, int, int, int]],
                          bottom: tuple[Path, float, tuple[int, int, int, int]],
                          out: Path, sentences: list[list[Phrase]],
                          workdir: Path, voice: VoiceSpec = None,
                          mood: str = "melancholic", band: int = 140,
                          font_size: "int | Callable[[str], int]" = FONT_QUOTE_SIZE,
                          font_path: str = FONT_QUOTE,
                          font_index: int = FONT_QUOTE_INDEX,
                          y_frac: float = 0.50, stroke: int = 4,
                          max_w: int = CAPTION_MAX_W,
                          ink: "Callable[[str], tuple[int,int,int,int] | None] | None" = None,
                          fps: int = 30,
                          gap: "float | list[float]" = GAP, tail: float = TAIL,
                          ) -> tuple[Path, float]:
    """Two clips stacked into one frame, quote read on the band between them.

    `top` and `bottom` are each `(src, source_in_point, box)` — get `box` from
    `pick_crop_tile(proxy, *stack_tile_size(band))`, so the tile search and this
    call agree on the same split. Both clips are cut to the narration's total
    length, so they must each run at least that long from their in-point.

    The `band` is a flat black strip between the tiles, not a seam — it gives
    the caption ground of its own instead of straddling two moving pictures,
    and it's why the default face here is a serif italic rather than
    `render_narrated`'s Futura: a stroke barely has to work on flat black, so
    the thin strokes of a serif survive it. `y_frac=0.50` centres the caption
    in the band by construction.

    `font_size` and `ink` may be callables taking the caption text, same
    pattern as `render_narrated` — pass both together to give one word a
    bigger size *and* a colour pulled from the footage, the way `LUCKY` shipped
    on Sunset Sea Stack.
    """
    (src_a, start_a, box_a), (src_b, start_b, box_b) = top, bottom
    tile_w, tile_h = stack_tile_size(band)

    track, captions, total = build_narration_aligned(
        sentences, workdir, voice, mood, gap, tail)

    shown = [(i, c) for i, c in enumerate(captions) if c.text.strip()]
    pngs = []
    for i, c in shown:
        p = workdir / f"cap{i:02d}.png"
        size = font_size(c.text) if callable(font_size) else font_size
        word_ink = ink(c.text) if callable(ink) else ink
        render_text_png(c.text, p, size=size, font_path=font_path,
                        font_index=font_index, y_frac=y_frac, stroke=stroke,
                        max_w=max_w, ink=word_ink)
        pngs.append(p)

    xa, ya, wa, ha = box_a
    xb, yb, wb, hb = box_b
    chain = [
        f"[0:v]crop={wa}:{ha}:{xa}:{ya},scale={tile_w}:{tile_h}:flags=lanczos[top]",
        f"[1:v]crop={wb}:{hb}:{xb}:{yb},scale={tile_w}:{tile_h}:flags=lanczos[bot]",
        f"color=c=black:s={tile_w}x{band}:r={fps}:d={total:.3f}[band]",
        "[top][band][bot]vstack=inputs=3[v0]",
    ]
    for n, (_, c) in enumerate(shown):
        chain.append(f"[v{n}][{n+2}:v]overlay=0:0:"
                     f"enable='between(t,{c.start:.3f},{c.end:.3f})'[v{n+1}]")
    chain.append(f"[v{len(shown)}]null[vout]")   # no fade to black — see `render_short`

    cmd = ["ffmpeg", "-v", "error", "-y",
           "-ss", f"{start_a}", "-t", f"{total:.3f}", "-i", str(src_a),
           "-ss", f"{start_b}", "-t", f"{total:.3f}", "-i", str(src_b)]
    for p in pngs:
        cmd += ["-i", str(p)]
    cmd += ["-i", str(track), "-filter_complex", ";".join(chain),
            "-map", "[vout]", "-map", f"{len(pngs)+2}:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "slow",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-shortest", "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True)
    return out, total
