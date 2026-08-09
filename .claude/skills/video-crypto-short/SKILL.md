---
name: video-crypto-short
description: Make vertical short-form videos for TikTok, YouTube Shorts and Instagram Reels from thecrypto.wiki articles — voiceover with synced captions over the site's own images and data graphics. Use when the user runs /video-crypto-short, asks for a crypto short or Reel, wants a post from thecrypto.wiki turned into a video, or wants to pick or tune the crypto voice. For drone footage shorts use video-drone-short instead.
---

# Crypto Wiki — short form

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
Shared with the drone and tinnitus projects. Renders go to the Desktop.

**Source content:** `~/Coding/crypto-wiki` — 60 posts, 27 exchanges, 33 crypto-ogs.

## Built

`video_automation/crypto/` — a photo-driven short assembled from the site's own
images.

```python
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot

out, total = render_crypto_short(SENTENCES, SHOTS, out_path, work, voice="theo")
```

One `Shot` per sentence, in order. `plan_shots` gives each shot the measured span
of its sentence, so the picture is cut to the voice and cannot drift.

**Still unbuilt:** script generation from MDX, upload, and the MDX embed. The
script is written by hand for now, which is the right way round — the script is
the product and 60 posts of automated scripts is the failure mode, not the goal.

## What the site gives you

**Images:** `crypto-wiki/public/images/{posts,crypto-ogs,exchanges}`. Already
licensed, already on brand, already attached to the post. **Do not reach for a
stock API** — generic stock loops under an AI voice is exactly the pattern both
platforms suppress, and the site's own library is better anyway.

**Structured data, which is where this scales:** every one of the 27 exchange
files and 33 OG files carries `quickFacts` and `faqs` in frontmatter, and there
are 26 exchange logos in `public/images/exchanges`. `ChecklistShot` already draws
from a list of `(label, bool)`; pointing it at `quickFacts` is the next step and
turns comparison shorts into a data problem rather than a design one.

**Palette** is `config/theme.json`: gold `#e5c200` on `#171717` / `#2f2f2f`.

**Demand data** is `json/views.json` — site pageviews, so it measures SEO demand,
**not** short-form appeal. Do not present it as evidence about video. Top pages:
`how-to-build-a-mining-rig` 1510, `understanding-crypto-exchanges` 1038,
`exchanges/cryptocom` 380, `crypto-ogs/satoshi-nakamoto` 372,
`crypto-etfs-explained` 362, `what-is-proof-of-stake` 317, `exchanges/okx` 304.

## The picture

**Blurred-fill layout, because the site's images are small.** Most are 700-1200px
and all are landscape, so none can fill 1080x1920 without a 3x upscale. The image
is scaled to cover the frame, blurred hard and dimmed to 42% as a backdrop, with
the sharp copy laid over it. The frame is full of picture and nothing is upscaled
past `MAX_UPSCALE = 1.45`.

- **Crop toward a taller shape first** (`aspect`, default 1.15). At full width a
  landscape source occupies about a third of a 9:16 frame and the rest is blur;
  cropping in gives it half or better. How far it can crop is bounded by
  resolution, not taste — cropping narrows the source and raises the upscale, so
  `MAX_UPSCALE` wins and the aspect target yields.
- **Do not use a source under ~750px wide.** Below that, `MAX_UPSCALE` leaves the
  photo as a small rectangle floating in blur. `crypto-ogs/satoshi.png` (400px)
  was tried and swapped for `posts/hacker.jpg` (996px).
- **The gold hairline spans the photo, not the frame.** Drawn full width it read
  as a band the picture had failed to fill.
- Backdrop and sharp layer pan in opposite directions at different rates — that
  separation is what makes a still photograph read as a shot. Subpixel, as
  everywhere in this repo.
- **Dissolve between shots** (`XFADE = 0.45`), do not cut. The piece is one
  continuous argument; a hard cut every five seconds fights the voice.

**`ChecklistShot` is the beat that earns the format.** A struck-through list that
fills in on the voice, ending on the one item that is ticked. It shows the
argument instead of illustrating it, which is the difference between this and
stock-footage-with-narration.

- **Reveal on caption starts, not on even fractions of the shot.** `build.py`
  fills `reveals` from the sentence's own caption times. Even fractions look
  synced until you watch it, and then every item is a beat early or late. Write
  the sentence with **one caption per item** and it needs no tuning.
- **White ink for every item, struck or not**, with a 3px black stroke. Grey-on-
  dark was shipped once and was not readable on a phone — the strike-through
  already says "this does not count", so the ink does not have to say it again by
  being harder to read.
- **Draw it over a dimmed photograph, not flat black.** A flat panel in the middle
  of a photo-driven piece reads as the video having stopped. `0.30` brightness was
  tried and was indistinguishable from black; `0.5` is the working value.
- Marks are **drawn from line segments, not set as glyphs** — Futura has no ✓ or ✕
  and PIL renders both as tofu, which is invisible in review and obvious in the
  frame.

**Watermark:** `public/images/logo.png`, upper-left at (58, 268), 300px wide,
full opacity, levitating 8px on a 6.5s sine. The asset already contains the
domain so nothing is added under it. Same safe box as the tinnitus shorts —
`SAFE_TOP=230`, `SAFE_BOTTOM=1440`, clear of `x>860` — and `render_shots` raises
rather than shipping outside it.

## Copy

**Captions go under the photograph, not over it.** Every source image is
landscape, so even cropped it leaves a band of blurred backdrop below, and that
band is where the type belongs — over the photo it covers the thing it is
describing, and it wasted the empty space. `build.py` reads each shot's
`photo_box(0.5)` and places that sentence's captions 96px beneath it, clamped to
0.80. `y_frac=0.70` is only the fallback, for drawn beats.

Futura Medium 46px, stroke 4, `max_w=CAPTION_MAX_W`.

**Emoji** via `core.vertical.add_caption_emoji` — shared with the tinnitus format.
One or two per script, where they add something: a padlock on "those coins have
never moved", a down-arrow on the closing question. More than that reads as
decoration.

`gap=0.34`, tighter than the drone quotes' 0.65. A quote wants air between lines;
a thirty-second explainer does not, and the pauses are what a viewer scrolls away
during.

**End on a question.** The last sentence asks the viewer something and the
caption carries a 👇. Comments are the cheapest engagement signal to earn and the
one a 35-second explainer can actually ask for without begging.

**The angle has to be in the first line.** The first cut is
`crypto-satoshi-proof` — "every few years someone claims they're satoshi, and
there is one test that settles it" — built from
`posts/what-it-actually-takes-to-prove-someone-is-satoshi-nakamoto.mdx`. It works
because the answer is concrete, surprising, and needs no financial advice.

**Check phonemes before rendering.** Years are fine (`2009` → "two thousand
nine"), names are fine (`satoshi nakamoto`), but `ecdsa` comes out `ˈɛkdsə` —
spell out or avoid any initialism.

## Voice

Five profiles, all reproducing their audition WAVs sample-for-sample:

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices show theo
```

| profile | voice | note |
|---|---|---|
| `sam` | male, `am_puck` 1.10 | **used by the current cut.** C+ with hours of data, steadiest American male |
| `theo` | male, `am_adam` 1.10 | the first cut. Lowest Kokoro grade on the list, shortlisted by ear anyway |
| `mia` | female, `af_heart` 1.10 | graded A, the strongest English voice in Kokoro |
| `mia-calm` | female, `af_heart` 1.00 | the same speaker, unhurried |
| `ivy` | female, `bf_emma` 1.10 | British — an audience choice as much as a voice one |

**None is approved.** `theo` took the first cut, `sam` the second, and the user
intends to work through the rest. Keep the script and shot list identical when
swapping, so the comparison is clean. The `ENERGETIC` chain they all share has
not been signed off either.

Pace, measured on the same script: both `theo` and `sam` at 1.10 land near 3.1
words a second, so ~105 words comes out around 35s.

## Decisions already taken

**Render headless with ffmpeg, not FCPXML.** Drone long-form writes XML to finish
by hand because there the footage *is* the product. Here it is support and the
script is the product; a human step in the loop means it never runs.

**Do not commit MP4s to the site repo.** Publish to YouTube Shorts and embed a
lazy-loaded facade, so the site carries no video bandwidth and gains a
`VideoObject` schema — the SEO win that lands whether or not the channels work.

**Evergreen before news.** News needs a live data dependency the repo does not
have, cannot be embedded as evergreen `VideoObject` content, carries per-video
accuracy risk in a YMYL niche, and is the shape the platforms suppress hardest.
News becomes a variant once the pipeline is proven, not the proving ground.

## Do not

- Mass-produce. Both platforms suppress the AI-script-plus-stock-footage pattern
  by policy; volume is the failure mode, not the goal.
- Give financial advice in a script, or imply one. Route to the site's exchange
  pages, which is where the affiliate revenue actually is.
- Promote a candidate voice to approved without being told to.
- Quote `views.json` as if it measured short-form performance. It is SEO demand.
- Use an image under ~750px wide.
