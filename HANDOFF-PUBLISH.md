# Handoff → /publish-video

**Built:** `478-breathing-white-noise-20min` — a tinnitushelp.me sound-therapy session (Mode 2, not an article pair).
**Source article:** none — off-site topic, `SOURCE_POST = None`. No Short; a session is its own single long-form video.
**Date:** 2026-09-05
**Voice:** `luna` (`af_nicole` 0.90, SOFT chain) — the session-format default. Still `candidate`.

---

## Files (all on the Desktop)

| what | path |
| --- | --- |
| video (16:9) | `/Users/oktayshakirov/Desktop/4-7-8 Breathing + White Noise for Tinnitus (20 Minutes).mp4` |
| thumbnail (16:9) | `/Users/oktayshakirov/Desktop/4-7-8 Breathing + White Noise for Tinnitus (20 Minutes).jpg` |

Runtime **exactly 20:00** (1200.0s, ffprobe-checked). 1920x1080, h264/aac.
No SRT — sessions have no dialogue track worth captioning, same as the earlier
5-minute masking session. No `.md` metadata sidecar was generated (same
precedent) — title/description/tags below are raw material, not pre-written copy.

## What this video is

Twenty minutes of generated white noise (`soundbed.Bed(colour="white")` —
67% of its energy sits above 8 kHz, per `docs/video/projects/tinnitus.md`,
so it covers a high whistling tinnitus better than the pink/brown default)
paired with **4-7-8 paced breathing** (inhale 4s, hold 7s, exhale 8s) —
Dr. Andrew Weil's pattern, distinct from every other session on the channel,
which use 4-in/6-out. 30s spoken intro (what the sound is, how to set the
level, the pattern by name and by count), a body of twenty 19s loops, 26s
outro (no CTA — a piece built to lower arousal doesn't end by asking for
something).

**Suggested title** (working, matches the filename): "4-7-8 Breathing + White
Noise for Tinnitus (20 Minutes)". Both halves are real search phrases
("4-7-8 breathing", "white noise for tinnitus") — pick whichever ordering
reads best, or split into title + a first-line-of-description mention of the
other.

**Angle for the description: partial masking.** Set the volume just below
your tinnitus so you can still faintly hear it — burying it completely is
what most people do and what the site's own post
(`brown-noise-vs-white-noise-for-tinnitus.mdx`) argues against.

**Required disclaimer language** (no medical claims — the rule that outranks
everything else in this project, see `docs/video/projects/tinnitus.md`):
this is a sound to listen to, not a treatment; never say it relieves,
improves, or cures tinnitus. If useful, the standard red-flag routing line:
"If your tinnitus lasts more than a few weeks, is getting louder, is in one
ear only, pulses with your heartbeat, or comes with dizziness or hearing
loss, see a doctor."

## Distribution

No standing rule for sound-therapy sessions specifically (the crypto/tinnitus
Short distribution notes in memory are about article Shorts). This is a
single long-form video with no Short counterpart — default to YouTube long
form only unless the user says otherwise.

## Engine changes shipped with this build (see commit below)

- `longform/asmr.py`: `_breath`/`render_loop`/`render_bookend`/
  `render_asmr_long` now take `inhale`/`hold`/`exhale` (default 4/0/6,
  byte-identical to every prior session) and an optional `palette`
  (`bg_deep, nebula_a, nebula_b, ring`; `None` keeps the app's purple/peach).
  `render_session_thumb` in `longform/thumb.py` takes the same `palette`.
- This session uses `inhale=4, hold=7, exhale=8`, `loop=57` (three 19s
  cycles), and a blue palette + orange thumbnail accent so it reads as a
  different video from the existing purple/cyan 5-minute session on sight,
  not just a different number.
- Fixed: the intro's "4-7-8" is a `(caption, spoken)` pair — Kokoro/espeak
  read the hyphens literally as "dash" (`espeak-ng --ipa "4-7-8"` →
  `fˈɔːɹ dˈæʃ sˈɛvən dˈæʃ ˈeɪt`), so the caption keeps the numerals and the
  voice gets "four, seven, eight".

## Repo state

All code committed and pushed to `origin/main` (commit `e443a48`):
- `projects/tinnitus-long/478-breathing-white-noise-20min.py` (new)
- `video_automation/longform/asmr.py`, `video_automation/longform/thumb.py`,
  `video_automation/tinnitus/asmr.py` (parameterised breathing pattern + palette)

Working tree clean. Open a fresh session and run `/publish-video`.
