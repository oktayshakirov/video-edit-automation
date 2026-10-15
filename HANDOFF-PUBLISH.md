# Handoff: Jungle Waterfall + 4-7-8 Breathing session pair

**Built:** `jungle-waterfall-478-breathing`, a tinnitushelp.me sound-therapy
session: long form (20 min) **and its own vertical Short** (Mode 2, not an
article pair).
**Source article:** none. Off-site topic, `SOURCE_POST = None`.
**Date:** 2026-10-15
**Voice:** `luna` (`af_nicole` 0.90, SOFT chain), the session default. Still
`candidate`.
**Approved by the user.** One re-cut round: the Short's outro was rewritten
(see below). Build commit `7097efb` on `main`, **not pushed**.

## Files (all on the Desktop)

### Long form (YouTube)

| what | path |
| --- | --- |
| video (16:9) | `/Users/oktayshakirov/Desktop/Jungle Waterfall + 4-7-8 Breathing for Tinnitus (20 Minutes).mp4` |
| thumbnail (1280x720) | `/Users/oktayshakirov/Desktop/Jungle Waterfall + 4-7-8 Breathing for Tinnitus (20 Minutes).jpg` |
| build script | `projects/tinnitus-long/jungle-waterfall-478-breathing-20min.py` |

Runtime **exactly 20:00** (1200.0s, ffprobe-checked). 1920x1080, h264/aac,
-19.4 LUFS integrated.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)

| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/Jungle Waterfall + 4-7-8 Breathing for Tinnitus (Short).mp4` |
| thumbnail (1080x1920) | `/Users/oktayshakirov/Desktop/Jungle Waterfall + 4-7-8 Breathing for Tinnitus (Short).jpg` |
| build script | `projects/tinnitus-short/jungle-waterfall-478-breathing-short.py` |

Runtime **57.2s**, 1080x1920, h264/aac, -19.3 LUFS. Same recording, pattern
and picture as the long form, 2 cycles of 4-7-8 (38s breathing block).

Neither file has an SRT or a `.md` metadata sidecar, same precedent as every
prior session build. Title and description material below is raw material,
not pre-written copy.

## What this is

A real field recording, **a waterfall with birdsong**, tiled from five
minutes to twenty. Source file: `~/Desktop/WaterfallBirds.wav` (the file the
user attached this session; keep it on the Desktop, both scripts read it by
that path). Paired with **4-7-8 paced breathing** (inhale 4s, hold 7s, exhale
8s).

**The picture is new for the channel**: drawn fern silhouettes swaying round
the edges of a dark green, moonlit frame, with drifting mist and fireflies,
instead of the nebula every earlier session used. Generated, so there is no
stock footage and no picture credit. "Jungle" describes the picture; the
narration only ever names the sound ("a waterfall and birdsong").

**The Short ends on "If this helped, save it for the next time you need
it."** and nothing after it. This replaces "there's a full twenty-minute
version on the channel", because TikTok and Instagram never get the long
version. It is now the rule for every session Short (documented in
`docs/video/projects/tinnitus.md`). The long form's outro still invites
another round.

## Things the publish step needs to know

**The audio's source and licence are not recorded.** The user supplied
`WaterfallBirds.wav` and its origin was not discussed in the build session.
**Ask the user where it came from before writing the description's credits**,
and before uploading to any platform that does content-ID matching. Do not
guess an attribution.

**Title collision.** The channel already has "Waterfall + 4-7-8 Breathing
for Tinnitus (20 Minutes)" (published September 2026, waterfall + pads,
nebula picture). This one is a different recording and a different picture,
but the same sound family and the same pattern, so the title must separate
them on sight. The filenames lead with "Jungle Waterfall"; other candidates
are "Rainforest Waterfall & Birdsong" or leading on "birdsong". "4-7-8
breathing" is the search phrase to keep.

**Angle for the description: partial masking.** Set the volume just below
your tinnitus so you can still faintly hear it.
(`brown-noise-vs-white-noise-for-tinnitus.mdx` argues against burying it.)
Unlike the September waterfall session, this recording **has** been measured:
`band_energy` puts about 98% of its energy between 1 and 8 kHz (1-4 kHz
38-47%, 4-8 kHz 51-60%, under 1% below 1 kHz), which is why the
partial-masking instruction is used. **Still make no claim about what it does
for tinnitus**: it is a sound to listen to, not a treatment. Never say it
relieves, improves or cures anything, and do not turn the measurement into a
promise like "covers high-pitched ringing".

The standard red-flag line fits the long-form description: "If your tinnitus
lasts more than a few weeks, is getting louder, is in one ear only, pulses
with your heartbeat, or comes with dizziness or hearing loss, see a doctor."

## Distribution

Long form to YouTube only. Short to the full table (YouTube Shorts, IG Reel,
FB Reel, TikTok). The Short's save ending is written for the platforms that
never get the long version.

## Not done, and deliberately left to `/publish-video`

- The YouTube uploads, the Reel workflows, the TikTok draft and the Facebook
  upload.
- The `videos.json` registry entry on the site.
- Any social posts, and their order.
- Pushing `main`. The build commit is local only.

Nothing has been uploaded or posted anywhere.
