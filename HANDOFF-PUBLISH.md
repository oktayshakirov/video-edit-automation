# Handoff → /publish-video

**Built:** `478-breathing-white-noise` — a tinnitushelp.me sound-therapy session, long form (20 min) **and its own vertical Short** (Mode 2, not an article pair).
**Source article:** none — off-site topic, `SOURCE_POST = None`.
**Date:** 2026-09-05
**Voice:** `luna` (`af_nicole` 0.90, SOFT chain) — the session-format default. Still `candidate`.

---

## Files (all on the Desktop)

### Long form (YouTube)
| what | path |
| --- | --- |
| video (16:9) | `/Users/oktayshakirov/Desktop/4-7-8 Breathing + White Noise for Tinnitus (20 Minutes).mp4` |
| thumbnail (16:9) | `/Users/oktayshakirov/Desktop/4-7-8 Breathing + White Noise for Tinnitus (20 Minutes).jpg` |

Runtime **exactly 20:00** (1200.0s, ffprobe-checked). 1920x1080, h264/aac.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)
| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/4-7-8 Breathing + White Noise for Tinnitus (Short).mp4` |
| thumbnail (9:16) | `/Users/oktayshakirov/Desktop/4-7-8 Breathing + White Noise for Tinnitus (Short).jpg` |

Runtime **57.3s**, 1080x1920, h264/aac. Same pattern, bed and nebula palette
as the long form, same seed — built as its companion, not a trailer for it:
2 cycles of 4-7-8 (38s breathing block) instead of the long form's twenty.

Neither file has an SRT or a `.md` metadata sidecar — sessions have no
dialogue track worth captioning line-by-line, same precedent as the earlier
5-minute masking session. Title/description material below is raw material,
not pre-written copy.

## What this is

Generated white noise (`soundbed.Bed(colour="white")` — 67% of its energy
sits above 8 kHz, per `docs/video/projects/tinnitus.md`, so it covers a high
whistling tinnitus better than the pink/brown default) paired with **4-7-8
paced breathing** (inhale 4s, hold 7s, exhale 8s) — Dr. Andrew Weil's
pattern, distinct from every other session on the channel, which use
4-in/6-out. Both formats end with no CTA — a piece built to lower arousal
doesn't end by asking for something; the Short's outro just points at the
full session on the channel.

**Suggested title** (working, matches the filename): "4-7-8 Breathing + White
Noise for Tinnitus" (+ "(20 Minutes)" for the long form). Both halves are
real search phrases ("4-7-8 breathing", "white noise for tinnitus") — pick
whichever ordering reads best, or split into title + a first-line-of-
description mention of the other. Same title angle for the Short is fine, or
lean into the Shorts-feed curiosity-hook convention if that reads better for
that surface — the video opens on the pattern named, not a question, so pick
whichever framing the captioning pass finds most natural.

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
loss, see a doctor." Put it in the long-form description; the Shorts-carry-
no-disclaimer memory is about article Shorts specifically — use judgement on
whether a session Short needs it (it reads more like the product itself than
an article Short does).

## Distribution

No standing rule for sound-therapy sessions specifically (the crypto/tinnitus
Short distribution notes in memory are about article Shorts). Suggest: long
form to YouTube; Short to the full table (YouTube Shorts + IG Reel + FB Reel
+ TikTok) since it's now built and self-contained — but confirm with the user
if unsure, since this is the first ASMR Short actually built in this repo.

## Engine changes shipped with this build (two commits, see below)

- `longform/asmr.py`: `_breath`/`render_loop`/`render_bookend`/
  `render_asmr_long` take `inhale`/`hold`/`exhale` (default 4/0/6,
  byte-identical to every prior session) and an optional `palette`
  (`bg_deep, nebula_a, nebula_b, ring`; `None` keeps the app's purple/peach).
- `longform/thumb.py`: `render_session_thumb` and `render_session_thumb_short`
  take the same `palette`.
- `tinnitus/asmr.py`: `render_asmr_short` took only `(low, high)` — the
  brand's own album MP3s — and both are confirmed gone from disk, so no fresh
  ASMR short could be rendered at all before this. It now also takes
  `bed: soundbed.Bed | None`, generated and loudness-matched the same way
  `render_bed`'s output is. `render_visual` takes the same `palette`.
- Fixed: the intro's "4-7-8" is a `(caption, spoken)` pair in both formats —
  Kokoro/espeak read the hyphens literally as "dash" (`espeak-ng --ipa
  "4-7-8"` → `fˈɔːɹ dˈæʃ sˈɛvən dˈæʃ ˈeɪt`), so the caption keeps the numerals
  and the voice gets "four, seven, eight".
- This session uses `inhale=4, hold=7, exhale=8` and a blue palette + orange
  thumbnail accent so it reads as a different video from the existing
  purple/cyan 5-minute session on sight, not just a different number.

## Repo state

All code committed and pushed to `origin/main`:
- `e443a48` — long-form build + engine parameterisation (pattern, palette)
- `c77e038` — first handoff write (superseded by this one)
- `671b531` — Short build + `render_asmr_short` generated-bed support

Files:
- `projects/tinnitus-long/478-breathing-white-noise-20min.py`
- `projects/tinnitus-short/478-breathing-white-noise-short.py`
- `video_automation/longform/asmr.py`, `video_automation/longform/thumb.py`,
  `video_automation/tinnitus/asmr.py`

Working tree clean. Open a fresh session and run `/publish-video`.
