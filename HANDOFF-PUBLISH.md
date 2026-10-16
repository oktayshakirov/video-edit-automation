# Handoff: akra-what-my-drone-sees (drone POV Short)

Approved by the user 2026-10-16. Channel: drone. **Nothing has been published
yet.**

A 9:16 POV Short at Akra Castle, Sozopol: "what i see" (the first 4s of the
phone clip of the RC controller, panning up to the Akra headland), then
"what my drone sees" in three drone shots at normal speed: Coast 2 (the
headland and the isthmus to Sozopol), Coast 8 (top-down along the cliffs),
Castle Bulgarian Flag (the ruins and the flag at sunset). Lowercase labels on
the first two beats only, no quote, no narration.

**No source article** - an off-site format piece, `SOURCE_POST = None`.

## Files

| What | Path |
| --- | --- |
| Video (19.15s, ffprobed, 1080x1920, 60fps, h264 SDR BT.709, AAC 48k stereo) | `/Users/oktayshakirov/Desktop/akra-what-my-drone-sees.mp4` |
| Sound the cut is timed to | `/Users/oktayshakirov/Downloads/v24044gl0000d34jdnvog65k02okpo0g.MP4` |

Script: `projects/drone-short/akra-what-my-drone-sees.py`. No thumbnail, SRT
or metadata sidecar - this engine does not write one.

**Cut to the user's TikTok sound**, which breaks the POV format's
silent-always default on the user's call (as Spree did). The render carries
the track from 13.871s in; cuts at 4.000s, 9.050s and 14.100s and the end at
19.150s each sit on one of its strong hits.

## Still open - decide during publishing

- **Title, caption and tags are not written yet.** Nothing has been drafted or
  agreed. Bulgaria is TikTok's strongest drone material per `drone-short.md`.
- **Which audio goes up where.** The file has the TikTok track baked in. On
  TikTok the user may prefer to attach the same sound natively so the video
  joins the sound's page; whether to upload this file as-is or a silent copy
  (`-an`) has not been discussed. The sound's origin and title are not
  recorded - ask before crediting it.

---

# Also pending from the previous build session

The handoff below was already in this file when the Short above was approved.
Kept rather than overwritten - check with the user whether it has gone out
yet.

## Handoff: Forest Chorus + Box Breathing session pair

**Built:** `forest-chorus-box-breathing`, a tinnitushelp.me sound-therapy
session: long form (20 min) **and its own vertical Short** (Mode 2, not an
article pair).
**Source article:** none. Off-site topic, `SOURCE_POST = None`.
**Date:** 2026-10-15
**Voice:** `luna`, the session default. Still `candidate`.
**Approved by the user** on the first cut, no re-cuts. Build commit `b0a25cc`
on `main`, **not pushed**.

## Files (all on the Desktop)

### Long form (YouTube)

| what | path |
| --- | --- |
| video (16:9) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (20 Minutes).mp4` |
| thumbnail (1280x720) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (20 Minutes).jpg` |
| build script | `projects/tinnitus-long/forest-chorus-box-breathing-20min.py` |

Runtime **exactly 20:00** (1200.0s, ffprobe-checked). 1920x1080, h264/aac,
-19.6 LUFS integrated.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)

| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (Short).mp4` |
| thumbnail (1080x1920) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (Short).jpg` |
| build script | `projects/tinnitus-short/forest-chorus-box-breathing-short.py` |

Runtime **55.6s**, 1080x1920, h264/aac, -19.6 LUFS. Same recording, pattern
and picture as the long form, 2 cycles of box breathing (32s breathing block).

Neither file has an SRT or a `.md` metadata sidecar, same precedent as every
prior session build. Title and description material below is raw material,
not pre-written copy.

## What this is

A real nature recording, **a forest chorus**, tiled from ten minutes to
twenty. Source file: `~/Desktop/NaturesChorus.wav` (the file the user attached
this session; keep it on the Desktop, both scripts read it by that path). The
narration calls it "a forest chorus" and never names species, so neither
should the description.

**Box breathing** (in 4s, hold 4s, out 4s, hold 4s), the first session on the
channel with that pattern. Earlier sessions were all 4-in/6-out or 4-7-8. The
intro instructions are new too: bring the sound up from low until the
tinnitus starts to blend in, and "if a hold feels like too much, let it go
and just breathe".

**The picture** is misty jungle-canopy footage, graded dark, with a few
fireflies (the `canopy-fog` look the user picked in the 2026-10-15 test
round). It is **stock footage, so it needs a credit**: Pexels video 19366762
by Florian Delee,
https://www.pexels.com/video/fog-tropic-jungle-latin-america-19366762/
(Pexels licence; attribution is optional, follow the channel's usual stock-credit practice).

**The Short ends on "If this helped, save it for the next time you need
it."** and nothing after it, per the session-Short rule. The long form's outro
invites another round.

## Things the publish step needs to know

**The audio's source and licence are not recorded.** The user supplied
`NaturesChorus.wav` and its origin was not discussed in the build session.
**Ask the user where it came from before writing the description's credits**,
and before uploading to any platform that does content-ID matching. Do not
guess an attribution.

**Copy angle: partial masking.** Set the sound so the tinnitus still faintly
shows underneath, which is the channel's angle
(`brown-noise-vs-white-noise-for-tinnitus.mdx` argues against burying it).
`band_energy` puts about 95% of the recording between 4 and 8 kHz (4-8 kHz
93-96%, everything else under 4% per band), which is why the instruction is
used. **Still make no claim about what it does for tinnitus**: it is a sound
to listen to, not a treatment. Never say it relieves, improves or cures
anything, and do not turn the measurement into a promise like "covers
high-pitched ringing". Same for box breathing: describe it as something
people do, not as a treatment.

The standard red-flag line fits the long-form description: "If your tinnitus
lasts more than a few weeks, is getting louder, is in one ear only, pulses
with your heartbeat, or comes with dizziness or hearing loss, see a doctor."

No em dashes in any published copy (titles, descriptions, tags).

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
