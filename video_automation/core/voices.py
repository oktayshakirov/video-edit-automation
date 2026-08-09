"""Named, reproducible voice profiles — the record of what was auditioned.

A profile is the whole recipe, not just a voice name: Kokoro renders from a
`(voice, speed)` pair and the post chain does at least as much work as either.
`af_nicole` through the energetic chain and `af_nicole` through a pitch-shifted
soft chain are different voices in every way that matters, so the profile is
the unit that gets named, approved and referenced.

Kokoro's ONNX inference is deterministic, so a profile plus its reference
script reproduces the audition WAV byte for byte. `python -m video_automation
voices verify` checks exactly that against the files on the Desktop.

**Status is not a rating.** `approved` means it has shipped in a finished
video. `candidate` means the user shortlisted it by ear and it is waiting on a
decision. Nothing here should be promoted without them saying so.
"""

from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

SR = 24000          # Kokoro's native rate — every asetrate below is relative to it


# --- chain fragments -----------------------------------------------------

def pitch(factor: float) -> str:
    """Tape-speed shift with real time restored.

    asetrate moves pitch and formants together, which is the classic
    female->male shift; atempo puts the duration back. The stretch costs some
    quality, so prefer `pitch_slow` where a slower read is wanted anyway.
    """
    return f"asetrate={SR}*{factor},aresample={SR},atempo={1/factor:.5f}"


def pitch_slow(factor: float) -> str:
    """Tape-speed shift with the slowdown kept — deeper *and* slower.

    No atempo, so no time-stretch artifacts. Duration changes, which is safe:
    `build_narration_aligned` measures the processed audio and scales caption
    boundaries onto it rather than assuming the chain preserves length.
    """
    return f"asetrate={SR}*{factor},aresample={SR}"


# Punchy, dry and close. Built for TikTok: ~3% pitch up brightens the read,
# compression carries it on a phone speaker, the 3.5k lift keeps it over the
# platform's own audio, -14 LUFS is the shorts target. atempo cancels the
# asetrate so real time is preserved.
ENERGETIC = (
    "highpass=f=90,"
    f"asetrate={SR}*1.03,aresample={SR},atempo=0.97087,"
    "acompressor=threshold=-18dB:ratio=3:attack=5:release=90:makeup=2,"
    "equalizer=f=3500:t=q:w=1.2:g=3,"
    "loudnorm=I=-14:TP=-1.5:LRA=11"
)

# Intimate and unforced: no pitch shift, gentle compression, the presence band
# pulled *down* and air added instead, -16 LUFS. For quotes and ASMR, where
# punch is the wrong quality.
SOFT = (
    "highpass=f=80,"
    "acompressor=threshold=-20dB:ratio=2.5:attack=15:release=250:makeup=2,"
    "equalizer=f=3500:t=q:w=1.2:g=-1.5,"
    "equalizer=f=9000:t=q:w=1.0:g=3,"
    "loudnorm=I=-16:TP=-1.5:LRA=11"
)

# Aspiration boost — lifts the bands where breath and consonant noise already
# live. Emphasises what the voice is doing rather than adding anything.
AIR = "equalizer=f=6000:t=q:w=0.8:g=6,equalizer=f=11000:t=q:w=0.9:g=5"

# The approved drone chain. Do not re-tune: the ~4% pitch-down and the short
# echo tail are what sell it — without them it is the same voice reading slower.
MELANCHOLIC = (
    f"asetrate={SR}*0.96,aresample={SR},atempo=1.0417,"
    "aecho=0.85:0.8:55:0.18,equalizer=f=250:t=q:w=1.5:g=2,loudnorm=I=-16"
)


# --- reference scripts ---------------------------------------------------
# Each profile was auditioned on one of these. Reproduction needs the matching
# one. Note "i red a quote" — espeak phonemizes from spelling, so `read` is
# /riːd/ in every context and has to be spelled for the engine.

SCRIPTS = {
    "crypto": (
        "okay, everyone keeps saying not your keys, not your coins. "
        "here is what that actually means. "
        "when your bitcoin sits on an exchange, you do not own it. "
        "the exchange owes it to you. that is not the same thing. "
        "move it to a wallet you control. it takes ten minutes."
    ),
    "quote": (
        "i red a quote that said, you'll spend years chasing a feeling "
        "you already had, on an ordinary tuesday. "
        "and you didn't know it was the good part."
    ),
}


@dataclass(frozen=True)
class VoiceProfile:
    """One complete, reproducible voice.

    `voice` is a Kokoro voice name or a `{name: weight}` blend. A blend is a
    weighted sum of (510,1,256) style tensors, so it is one new speaker the
    model renders as a single person — not two voices mixed as audio.
    """
    voice: "str | dict[str, float]"
    speed: float
    chain: str
    projects: tuple[str, ...]
    status: str                     # "approved" | "candidate"
    script: str                     # key into SCRIPTS
    note: str = ""
    source: str = ""                # audition WAV this profile reproduces
    folder: str = ""                # where the user filed that WAV


# Profiles are named after people, not after their ingredients — the Kokoro
# voice names underneath are an implementation detail, and "onyx-nicole-60"
# told you the recipe but never which voice it was. Male-sounding profiles get
# male names, female-sounding ones female names, so the roster reads at a
# glance. The recipe is still one `voices show <name>` away.
PROFILES: dict[str, VoiceProfile] = {

    # --- drone -----------------------------------------------------------
    "leo": VoiceProfile(
        voice={"am_onyx": 0.60, "af_nicole": 0.40}, speed=0.95, chain=SOFT,
        projects=("drone",), status="approved", script="quote",
        note="THE DRONE VOICE. Chosen over three other blends and the previous "
             "am_onyx/am_puck default, on two quotes and two clips. A blend of "
             "the old male voice with Kokoro's only breathy one.",
        source="A4_onyx60_nicole40.wav", folder="Drone voices",
    ),
    "max": VoiceProfile(
        voice={"am_michael": 0.60, "af_nicole": 0.40}, speed=0.95, chain=SOFT,
        projects=("drone",), status="candidate", script="quote",
        note="Runner-up. Same idea as leo on am_michael instead of am_onyx. "
             "Measured caveat on all these blends: they lose most of luna's "
             "slowness — 10.2s at speed 0.95 against luna's 11.7s at 1.05.",
        source="A2_michael60_nicole40.wav", folder="Drone voices",
    ),
    "noah": VoiceProfile(
        voice={"am_michael": 0.50, "af_nicole": 0.50}, speed=0.95, chain=SOFT,
        projects=("drone",), status="candidate", script="quote",
        note="Even split — the most breath that still reads male.",
        source="A3_michael50_nicole50.wav", folder="Drone voices",
    ),
    "luna": VoiceProfile(
        voice="af_nicole", speed=1.10, chain=ENERGETIC,
        projects=("drone", "tinnitus"), status="candidate", script="crypto",
        note="Female. Kokoro's only breathy/ASMR voice — renders 23.3s where "
             "every other female voice lands 12-15s on the same script. That "
             "is the voice's character, not a pace setting. The base voice "
             "inside leo, max, noah and every tinnitus profile.",
        source="03_af_nicole.wav", folder="Drone voices, Tinnitus Help Voice",
    ),

    # --- crypto ----------------------------------------------------------
    "mia": VoiceProfile(
        voice="af_heart", speed=1.10, chain=ENERGETIC,
        projects=("crypto",), status="candidate", script="crypto",
        note="Female. Graded A — the strongest English voice in Kokoro. Grade "
             "matters here because artifacts show at speed.",
        source="01_af_heart.wav", folder="Crypto Wiki Voices",
    ),
    "mia-calm": VoiceProfile(
        voice="af_heart", speed=1.00, chain=ENERGETIC,
        projects=("crypto",), status="candidate", script="crypto",
        note="Female. The same voice as mia, unhurried — kept as a suffix "
             "rather than a new name because it is one speaker, not two. "
             "Kokoro's speed is sublinear, so 1.00 vs 1.10 is only 15.6s vs "
             "14.9s: a delivery choice more than a runtime one.",
        source="20_pace_1.00_af_heart.wav", folder="Crypto Wiki Voices",
    ),
    "ivy": VoiceProfile(
        voice="bf_emma", speed=1.10, chain=ENERGETIC,
        projects=("crypto",), status="candidate", script="crypto",
        note="Female, British, graded B-. An audience choice as much as a "
             "voice one.",
        source="04_bf_emma.wav", folder="Crypto Wiki Voices",
    ),
    "sam": VoiceProfile(
        voice="am_puck", speed=1.10, chain=ENERGETIC,
        projects=("crypto",), status="candidate", script="crypto",
        note="Male. Graded C+ with hours of data — the steadiest American male.",
        source="M_am_puck.wav", folder="Crypto Wiki Voices",
    ),
    "theo": VoiceProfile(
        voice="am_adam", speed=1.10, chain=ENERGETIC,
        projects=("crypto",), status="candidate", script="crypto",
        note="Male. Lowest-graded voice on the shortlist (F on the model card) "
             "but shortlisted by ear, which outranks the grade.",
        source="M_am_adam.wav", folder="Crypto Wiki Voices",
    ),

    # --- tinnitus --------------------------------------------------------
    # All four are luna pitched toward a male register. That keeps 100% of the
    # breath by construction, which the cross-gender blends did not. They carry
    # male names because that is what they are *for* — but whether they read as
    # male or as a processed woman is still unconfirmed by ear.
    "elias": VoiceProfile(
        voice="af_nicole", speed=1.05, chain=f"{pitch(0.88)},{SOFT}",
        projects=("tinnitus",), status="candidate", script="quote",
        note="luna 12% down, real time restored.",
        source="B1_nicole_p88.wav", folder="Tinnitus Help Voice",
    ),
    "felix": VoiceProfile(
        voice="af_nicole", speed=1.05, chain=f"{pitch(0.84)},{SOFT}",
        projects=("tinnitus",), status="candidate", script="quote",
        note="luna 16% down, real time restored.",
        source="B2_nicole_p84.wav", folder="Tinnitus Help Voice",
    ),
    "jonas": VoiceProfile(
        voice="af_nicole", speed=1.05, chain=f"{pitch_slow(0.88)},{SOFT}",
        projects=("tinnitus",), status="candidate", script="quote",
        note="luna 12% down with the slowdown kept — no time-stretch artifacts.",
        source="D1_nicole_slow_p88.wav", folder="Tinnitus Help Voice",
    ),
    "caspar": VoiceProfile(
        voice="af_nicole", speed=1.05, chain=f"{pitch_slow(0.84)},{SOFT},{AIR}",
        projects=("tinnitus",), status="candidate", script="quote",
        note="luna 16% down, slowdown kept, plus the aspiration boost. The most "
             "processed of the set and the closest to male ASMR.",
        source="D4_nicole_slow_p84_aspirate.wav", folder="Tinnitus Help Voice",
    ),
    "luna-calm": VoiceProfile(
        voice="af_nicole", speed=0.90, chain=SOFT,
        projects=("tinnitus",), status="candidate", script="quote",
        note="Female, unhurried. luna's voice off the ENERGETIC chain and onto "
             "SOFT, which exists for exactly this — no pitch shift, presence "
             "pulled down, air added, -16 LUFS. luna itself is 1.10 through a "
             "chain built to punch on a phone speaker, which is the wrong "
             "instrument for a sound-therapy piece the listener is meant to "
             "breathe along with. Suffix, not a new name: one speaker.",
        folder="Tinnitus Help Voice",
    ),
}

APPROVED = {n: p for n, p in PROFILES.items() if p.status == "approved"}

# The single source of truth for what video-drone-short ships with. voiceover.py
# derives KOKORO_VOICE from this, so the approved recipe is written down once
# and cannot drift between the two files.
#
# The previous default — am_onyx 0.60 + am_puck 0.40 on the MELANCHOLIC chain —
# was retired when leo was approved. The chain itself is kept above and still
# registered as the "melancholic" mood, because videos already shipped with it
# and CHANGELOG entries refer to that sound.
APPROVED_DRONE = PROFILES["leo"]

# Where the user filed the shortlists. Used only by `voices verify`.
AUDITION_DIRS = [
    Path.home() / "Desktop/Crypto Wiki Voices",
    Path.home() / "Desktop/Drone voices",
    Path.home() / "Desktop/Tinnitus Help Voice",
]


def get(name: str) -> VoiceProfile:
    if name not in PROFILES:
        raise KeyError(f"unknown voice profile: {name}\n"
                       f"known: {', '.join(sorted(PROFILES))}")
    return PROFILES[name]


def for_project(project: str) -> dict[str, VoiceProfile]:
    return {n: p for n, p in PROFILES.items() if project in p.projects}


def render(name: str, out: Path, text: str | None = None) -> float:
    """Render a profile to a WAV. Returns the ffprobed duration."""
    import soundfile as sf
    from .voiceover import _kokoro, voice_style

    p = get(name)
    audio, sr = _kokoro().create(text or SCRIPTS[p.script],
                                 voice=voice_style(p.voice),
                                 speed=p.speed, lang="en-us")
    out.parent.mkdir(parents=True, exist_ok=True)
    raw = out.with_suffix(".raw.wav")
    sf.write(str(raw), audio, sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw),
                    "-af", p.chain, "-ar", "48000", "-ac", "2", str(out)],
                   check=True)
    raw.unlink(missing_ok=True)
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(out)],
        check=True, capture_output=True, text=True).stdout.strip())


def main(argv: list[str]) -> int:
    """`voices list|show|render|verify`."""
    cmd = argv[0] if argv else "list"

    if cmd == "list":
        for proj in ("drone", "crypto", "tinnitus"):
            print(f"\n{proj}")
            for n, p in for_project(proj).items():
                mark = "*" if p.status == "approved" else " "
                v = p.voice if isinstance(p.voice, str) else \
                    "+".join(f"{k}{int(w*100)}" for k, w in p.voice.items())
                print(f"  {mark} {n:24} {v:28} speed {p.speed}")
        print("\n* = approved (has shipped). Others are shortlisted candidates.")
        return 0

    if cmd == "show" and len(argv) > 1:
        p = get(argv[1])
        print(f"{argv[1]}\n  voice   {p.voice}\n  speed   {p.speed}\n"
              f"  chain   {p.chain}\n  status  {p.status}\n"
              f"  used by {', '.join(p.projects)}\n  from    {p.source or '-'}"
              f"\n\n  {p.note}")
        return 0

    if cmd == "render" and len(argv) > 1:
        out = Path(argv[2]) if len(argv) > 2 else \
            Path.home() / f"Desktop/{argv[1]}.wav"
        print(f"{out}  {render(argv[1], out):.2f}s")
        return 0

    if cmd == "verify":
        return _verify()

    print("usage: voices list | show <name> | render <name> [out] | verify",
          file=sys.stderr)
    return 1


def _verify() -> int:
    """Re-render every sourced profile and compare to the user's picked WAV.

    Kokoro is deterministic, so a correct profile reproduces its audition file
    exactly. Compares decoded samples rather than bytes, since the WAV header
    carries no meaning here.
    """
    import tempfile

    import numpy as np
    import soundfile as sf

    ok = failed = missing = 0
    with tempfile.TemporaryDirectory() as td:
        for name, p in PROFILES.items():
            if not p.source:
                continue
            orig = next((d / p.source for d in AUDITION_DIRS
                         if (d / p.source).exists()), None)
            if orig is None:
                print(f"  ?  {name:24} {p.source} not on Desktop")
                missing += 1
                continue
            got = Path(td) / f"{name}.wav"
            render(name, got)
            a, _ = sf.read(str(orig))
            b, _ = sf.read(str(got))
            if a.shape == b.shape and np.allclose(a, b, atol=1e-6):
                print(f"  ok {name:24} reproduces {p.source}")
                ok += 1
            else:
                print(f"  XX {name:24} DIFFERS from {p.source} "
                      f"({a.shape} vs {b.shape})")
                failed += 1
    print(f"\n{ok} reproduced, {failed} differ, {missing} missing")
    return 1 if failed else 0
