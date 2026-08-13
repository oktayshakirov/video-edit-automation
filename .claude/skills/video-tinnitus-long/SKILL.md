---
name: video-tinnitus-long
description: Make long-form 16:9 YouTube videos from tinnitushelp.me articles — 2-4 minute explainers with voiceover, drawn data beats, chapters, an SRT and a thumbnail. Use when the user runs /video-tinnitus-long, asks for a long or full-length tinnitus video, wants a post from tinnitushelp.me turned into a YouTube video, or wants to embed a video on a tinnitus post. For vertical Shorts or ASMR sound-therapy pieces use video-tinnitus-short instead.
---

# Tinnitus Help — long form

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
Renders go to the Desktop.

**Source content:** `~/Coding/tinnitus-blog/content` — 69 posts plus `zen/`,
which documents ten released sound albums. **There is also an app**,
`~/Coding/tinnitus-app`.

**Read `docs/long-form-strategy.md` first**, then the crypto long-form skill —
the engine, the beats and the rules paid for in blood are shared and are
documented there rather than repeated here. This file is only what differs.

## Status

**The engine is built and the format is not.** `video_automation/longform/`
works and `TINNITUS` is a registered `Brand` whose mascot lockup renders. No
tinnitus long-form video has been made yet, so nothing below about pacing or
retention has been tested on this audience. The first cut should follow
`projects/crypto-long/satoshi-proof.py` closely and diverge only where this
section says to.

## What is different here

**The picture library is thinner and smaller.** 108 images, median **750px**
wide, 2–3 per post against crypto's 3–5. Two consequences:

- **Lean harder on drawn beats than the crypto videos do.** They are already the
  majority of the runtime there; here they should be more.
- **The picture column is doing real work.** A 750px source in the 660px column
  is a downscale; the same image full-frame at 1920 is a 2.6x upscale the
  ceiling will refuse. Prefer beats with `picture=` over full-frame photos.

**There is a procedural backdrop nobody else has.** `tinnitus/asmr.py`'s
`nebula_canvas` generates infinite on-brand picture with no licence question, in
the app's own palette. It is not wired into the long-form beats yet and it is
the obvious first extension — it would remove the image shortage entirely.

**Music should come from the brand's own albums.** The `zen/` section documents
ten released sound albums. Using one as the bed is licensed by construction,
on-brand, and doubles as a plug for the thing the channel is actually selling.
Prefer that to the YouTube Audio Library here. It also sidesteps the
repost-licensing edge the crypto skill has to carry.

**Voice.** `luna-calm` (`af_nicole` 0.90, SOFT) is what the sound-therapy short
is built on. Whether it is right for a three-minute explainer is untested —
SOFT exists for ASMR and an explainer may want the ENERGETIC chain. Try
`luna-calm` first, compare against `luna`, and settle it with `/youtube-audit`
rather than by ear alone. **Neither is approved.**

**Beat choice follows the content.** These posts are comparison-shaped and
source-backed, which suits two beats especially:

- **`compare`** — brown noise against white, silence against masking, one
  therapy against another. The top-performing pages are largely comparisons.
- **`quote`** — every post carries a `sources` frontmatter block with a title, a
  publisher and a URL. Putting the publisher on screen is the cheapest
  credibility signal available in a YMYL niche and the data is already written.

Every post also carries an `faq` block, which is a `checklist` or a `compare`
without anyone having to invent the content.

## The conversion goal is different

**App install beats blog traffic**, and the tinnitus short skill already settles
this. The watermark carries the domain, the site prompts for the install on
arrival, so one legible URL does the work an end card was doing.

Put the app in `Meta.cta` and the article in `Meta.url` — the first two lines of
the description are the only ones visible before the fold, and the article link
lives there because it is what the video is *about*. The app goes below it.

## Do not

- **Make medical claims.** YMYL. Describe partial masking and paced breathing as
  things people do, never as treatment, and never imply a cure. This is the one
  rule here that outranks every production consideration.
- Write copy that oversells what a masking track can do above 4 kHz — the
  measurement behind that limit is in the short skill and it has not changed.
- Present the format as proven. No tinnitus long-form video exists yet.
- Promote a candidate voice to approved without being told to.
- Mass-produce. Same cap as crypto: see the strategy doc.
