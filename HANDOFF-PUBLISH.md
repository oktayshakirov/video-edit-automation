# Handoff → /publish-video

**Built:** `waterfall-478-breathing` — a tinnitushelp.me sound-therapy
session, long form (20 min) **and its own vertical Short** (Mode 2, not an
article pair).
**Source article:** none — off-site topic, `SOURCE_POST = None`.
**Date:** 2026-09-14
**Voice:** `luna` (`af_nicole` 0.90, SOFT chain) — the session-format default.
Still `candidate`.
**Approved by the user.** Built in this session, one re-cut round (the long
form's intro narration slightly overran the ring-reveal timing; trimmed).

## Files (all on the Desktop)

### Long form (YouTube)
| what | path |
| --- | --- |
| video (16:9) | `/Users/oktayshakirov/Desktop/Waterfall + 4-7-8 Breathing for Tinnitus (20 Minutes).mp4` |
| thumbnail (16:9) | `/Users/oktayshakirov/Desktop/Waterfall + 4-7-8 Breathing for Tinnitus (20 Minutes).jpg` |

Runtime **exactly 20:00** (1200.0s, ffprobe-checked). 1920x1080, h264/aac.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)
| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/Waterfall + 4-7-8 Breathing for Tinnitus (Short).mp4` |
| thumbnail (9:16) | `/Users/oktayshakirov/Desktop/Waterfall + 4-7-8 Breathing for Tinnitus (Short).jpg` |

Runtime **58.0s**, 1080x1920, h264/aac. Same pattern, bed and palette as the
long form, same seed — built as its companion, not a trailer for it: 2 cycles
of 4-7-8 (38s breathing block) instead of the long form's twenty.

Neither file has an SRT or a `.md` metadata sidecar — sessions have no
dialogue track worth captioning line-by-line, same precedent as every prior
ASMR build. Title/description material below is raw material, not
pre-written copy.

## What this is

A single already-mixed field recording — a waterfall with soft pads laid
under it — instead of generated noise. Source file:
`~/Desktop/waterfall-pads.mp3` (copied from the file the user attached this
session; keep it on the Desktop, both scripts reference it by that path and
need it to be re-runnable). Paired with **4-7-8 paced breathing** (inhale 4s,
hold 7s, exhale 8s) — the same pattern as the existing
`478-breathing-white-noise` pair, so a viewer who liked one recognises the
pattern in the other, but a **fresh star-field seed and a teal/aqua palette**
(not that pair's blue) so it reads as its own session on sight, not a re-skin.

**The user's stated reason for this build**: the earlier 4-7-8 white-noise
Short got 30k views on Facebook specifically (weaker elsewhere), and this is
a second piece in the same format to build on that. Worth weighting Facebook
in the Short's distribution/promotion if `/publish-video`'s workflow has any
per-platform discretion.

Both formats end with no CTA — a piece built to lower arousal doesn't end by
asking for something; the Short's outro just points at the full session on
the channel, the long form's outro invites another round.

**Suggested title** (matches the filenames): "Waterfall + 4-7-8 Breathing for
Tinnitus" (+ "(20 Minutes)" for the long form). "4-7-8 breathing" is a real
search phrase; "waterfall sounds for tinnitus" / "waterfall white noise" is
plausible but less established than "white noise" was — use judgement, or
lean on the pattern name carrying the search intent. Same title angle for the
Short is fine, or the Shorts-feed curiosity-hook convention if that reads
better for that surface.

**Angle for the description: partial masking.** Set the volume just below
your tinnitus so you can still faintly hear it — burying it completely is
what most people already do and what the site argues against
(`brown-noise-vs-white-noise-for-tinnitus.mdx`).

**No medical claims — this is a sound to listen to, not a treatment.** Never
say it relieves, improves, or cures tinnitus. **Do not claim any specific
frequency coverage** — unlike the generated beds, this one is a real
recording and nobody has run `soundbed.band_energy()` on it (see the doc note
added this session), so there is no measurement backing a claim like "covers
high-pitched ringing". The copy in both scripts only ever says "just below
your tinnitus", never a frequency range. If useful, the standard red-flag
routing line: "If your tinnitus lasts more than a few weeks, is getting
louder, is in one ear only, pulses with your heartbeat, or comes with
dizziness or hearing loss, see a doctor." — fits the long-form description;
use judgement on the Short (it reads more like the product itself than an
article Short does, per the precedent on the white-noise pair's own handoff).

## Distribution

Long form to YouTube. Short to the full table (YouTube Shorts + IG Reel + FB
Reel + TikTok) — see the Facebook note above for why this one in particular
is worth pushing there.

## Engine changes shipped with this build (commit `2693e58`)

- `tinnitus/asmr.py` (`render_asmr_short`) and `longform/asmr.py`
  (`render_asmr_long`): new `bed_file` (+ `bed_file_skip`) parameter — a
  single already-mixed real recording, trimmed to length from the given
  offset and given the same `loudnorm`/fade treatment the generated-bed and
  `(low, high)`/`bed_files` paths already get. Pass exactly one of `bed`,
  `bed_file`, or `(low, high)` / `bed_files`.
- `docs/video/projects/tinnitus.md`: documented the new `bed_file` path and
  its honest-limit caveat (run `band_energy()` before claiming coverage of
  anything, same as a generated bed).
- No changes to the visual engine — this session deliberately uses the
  existing procedural nebula + breathing ring (no stock footage, no gradient
  animation), per the documented rule that a cutting picture fights the
  audio in this format. "Matching colours" is the `palette` parameter, not a
  new visual mechanism.

## Repo state

All code committed and pushed to `origin/main`:
- `2693e58` — long + short build, `bed_file` engine support, doc update
- this commit — handoff

Nothing has been uploaded or posted anywhere yet.
