# Ready to publish: the Musk effect, long + Short

Built 2026-09-27 by `/video-crypto`. **Nothing has been published yet.** Open a
fresh session and run `/publish-video`; this file is what it reads.

**Channel:** thecrypto.wiki. Voice `mia`, music `night-drift`.

**Source:** `crypto-ogs/elon-musk` — the OG bio, **not** a `posts/` article.
https://thecrypto.wiki/crypto-ogs/elon-musk

Both scripts therefore set `SOURCE_POST = None` and carry `SOURCE_OG =
"elon-musk"`. `tools/topics.py` counts coverage off `SOURCE_POST`, so this pair
will not mark any post as covered — that is correct, not a bug.

## The files

| What | Path |
| --- | --- |
| Long MP4 (3:40) | `/Users/oktayshakirov/Desktop/musk-effect-long.mp4` |
| Long SRT | `/Users/oktayshakirov/Desktop/musk-effect-long.srt` |
| Long thumbnail (1280x720) | `/Users/oktayshakirov/Desktop/musk-effect-long-thumb.jpg` |
| Long metadata sidecar | `/Users/oktayshakirov/Desktop/musk-effect-long.md` |
| Short MP4 (47.1s) | `/Users/oktayshakirov/Desktop/musk-effect-short.mp4` |
| Short thumbnail (1080x1920) | `/Users/oktayshakirov/Desktop/musk-effect-short-thumb.jpg` |

Build scripts: `projects/crypto-long/musk-effect.py`,
`projects/crypto-short/musk-effect.py`.

**Take the title, description, tags and chapters from the `.md` sidecar.** Do
not re-derive them.

- Long-form title: **Why Do Elon Musk's Posts Move Crypto Prices?**
- Six chapters, first at 0:00, all over 10s — `check_chapters` reported no
  violations.

## Read this before writing any description — the attribution is not optional

**Two of the three photographs of Elon Musk are CC BY 2.0, which makes both
videos derivative works.** The line below must appear in the description of
anything published, on every platform that has one:

> Photographs of Elon Musk: Daniel Oberhaus (CC BY 2.0) and public-domain
> images, via Wikimedia Commons.

It is already in `Meta.credits`, so the **long form's sidecar description
carries it automatically** — do not strip it when trimming for length.

**The Short is the exposure here.** It uses the same CC BY 2.0 photograph and
has no description block in this pipeline, so the line has to be added by hand
wherever the Short goes and the platform allows a caption — YouTube Shorts
description, the Instagram/Facebook Reel caption, the TikTok caption. Full
detail and the per-file licences are in `assets/crypto/musk/CREDITS.md`.

## The safety line, since this one names a living person

The script describes a **mechanism** and never a direction: no price level, no
prediction, no recommendation, and no claim about what any post will do next.
Chapter four deliberately runs the 2021-22 Tesla sequence in **both**
directions so nothing reads as "watch his posts". The spoken compliance line
and its on-screen payload are in the close.

**Do not let a platform caption undo that.** A Reel or TikTok caption written
loose — anything shaped like "Musk moves the market" or naming a coin as a
thing to hold — reintroduces exactly the claim the script spent four minutes
avoiding, in a YMYL niche. Keep captions mechanism-shaped.

## Undecided / worth a look before it goes out

1. **The Short's thumbnail is a 9:16 file**, and YouTube Studio only accepts a
   Short cover set by hand. Same manual step as every previous pair.
2. **Nothing sets YouTube privacy.** Previous runs have gone up unlisted and
   been flipped in Studio; decide which you want here.
3. **No site `videos.json` entry is written by the build.** That is
   `/publish-video`'s step, and the registry is hand-edited by design. Note
   that the source is a `crypto-ogs/` page rather than a `posts/` one, so
   whatever the registry expects for a source slug may need the different
   prefix — check before appending.
4. **The thumbnail scorer is irrelevant on this pair.** Both thumbnails use an
   explicit `crop_at`/`crop_zoom`, which bypasses `_layout` entirely, so any
   remembered "busiest-case score" warning from an earlier render does not
   apply to the shipped files.

## What changed during the build, for the record

The first cut had **no photograph of Musk anywhere**, on the reasoning that the
video's subject is a queue of offers and a face is a promise about the subject.
The user's call was the opposite: he should be seen, and the thumbnail should
say "the Musk effect". Both were rebuilt accordingly — three Commons
photographs placed at the lines that name him, and new thumbnails on the
arms-crossed portrait.

**There is no usable video of him at any resolution** — Pexels does not licence
footage of a real public figure and Commons' only non-political clips are
500x374. If footage is ever wanted, it is a licensed-archive purchase, not
something this pipeline can fetch.
