# Handoff → /publish-video

**Built:** `does-magnesium-help-tinnitus` — an article-explainer pair
(`/video-tinnitus`), long form + Short, both from one tinnitushelp.me post.
**Source article:** `https://tinnitushelp.me/blog/does-magnesium-help-tinnitus`
(`SOURCE_POST = "does-magnesium-help-tinnitus"` in both scripts).
**Scripts:**
- `projects/tinnitus-long/does-magnesium-help-tinnitus.py`
- `projects/tinnitus-short/does-magnesium-help-tinnitus.py`

**Date:** 2026-09-13.
**Voice:** `mia` (`af_heart` 1.10) — the explainer default, same voice on both
videos per the project doc.
**Approved by the user.** Built in this session; no re-cut rounds requested.
**Committed:** this commit, on `main`. Working tree clean once pushed.

---

## Files (Desktop)

| what | path |
| --- | --- |
| long video (16:9) | `/Users/oktayshakirov/Desktop/does-magnesium-help-tinnitus-long.mp4` |
| long captions | `/Users/oktayshakirov/Desktop/does-magnesium-help-tinnitus-long.srt` |
| long thumbnail | `/Users/oktayshakirov/Desktop/does-magnesium-help-tinnitus-long-thumb.jpg` |
| long metadata sidecar | `/Users/oktayshakirov/Desktop/does-magnesium-help-tinnitus-long.md` |
| short video (9:16) | `/Users/oktayshakirov/Desktop/does-magnesium-help-tinnitus-short.mp4` |
| short cover (Reels/Facebook, 1080x1920) | `/Users/oktayshakirov/Desktop/does-magnesium-help-tinnitus-short-thumb.jpg` |
| short cover (YouTube, 1280x720) | `/Users/oktayshakirov/Desktop/does-magnesium-help-tinnitus-short-thumb-yt.jpg` |

- Long form: **3:47** (227.95s), six chapters, `SRT` only (no burned
  captions, per the long-form engine).
- Short: **47.9s**, karaoke captions on by default, music bed
  `music.track("night-drift")` at gain 0.85 (same track as the long form, at
  1.0).
- **The `.md` sidecar carries the finished long-form title, description,
  chapters, tags and credits block — read it rather than re-deriving any of
  that from this handoff or from the script.** The Short has no sidecar (per
  the engine); its title/description need writing at publish time from the
  script's own docstring and sentence list below.

## What it is

**Long form** — "Does Magnesium Help Tinnitus?" The honest answer is that
nobody knows: the one placebo-controlled trial people cite tested magnesium
combined with vitamins and a plant extract, so it can't isolate what the
magnesium did. Walks the research, the plausible-but-unproven calcium-gate
mechanism, real milligram counts in ordinary food (`bars`), and a four-week
self-test with the drug-interaction warnings on screen (`steps`). Closes by
routing to a professional for the real red flags.

Beats: `quote`, `diagram`, `bars`, `steps` — none shared with the three most
recent tinnitus long forms (which ran grid/compare in every one).

**Short** — same post, a different single move: the honest "nobody knows" is
sentence two (no hedge), and what survives is what's actually knowable off
the label in front of the viewer — oxide is cheap and poorly absorbed,
glycinate is gentlest, read the elemental magnesium not the compound weight.
One `checklist` beat with `flow=True`, closes cold on "Check your label
tonight." — no question, no disclaimer line (per the Short/long-form
asymmetry in `narration.md`).

**No medical claims in either cut.** Nothing promises relief; magnesium is
described only as something possibly worth correcting if a viewer is short of
it. Full reasoning and every claim's source is in each script's own
docstring.

## Where it goes

Standard tinnitushelp.me pair distribution — YouTube (long + Shorts),
Instagram Reels, Facebook, TikTok, and a site `videos.json` entry. Follow
`/publish-video`'s own sequence for the exact steps; nothing here pre-empts
it.

Channel: **`tinnitus`**.

## Metadata

**Long form:** fully written in
`~/Desktop/does-magnesium-help-tinnitus-long.md` — title, description,
chapters, tags, credits, hashtags. Use it as-is.

**Short:** no sidecar generated (the engine doesn't produce one for Shorts).
Starting point for publish time:

- **Title:** `Does Magnesium Help Tinnitus?` (or add `#shorts`, per whatever
  the channel's settled Shorts title convention is)
- **Description:**
  ```
  Nobody knows yet - but there's one thing about magnesium and tinnitus that is actually knowable. Full research breakdown: https://tinnitushelp.me/blog/does-magnesium-help-tinnitus

  #tinnitus #magnesium #ringinginears
  ```
- **Tags:** reuse the long form's tag list from the `.md` sidecar above.

## Undecided / notes for publish

- Both videos and both thumbnails were checked against the docs' three
  thumbnail rules (face not covered, subject fits, words are the script's
  own) and against the crop rules for a portrait source cover-cropped into
  16:9 and 9:16 — the automatic scorer initially cropped the capsules out of
  frame on both, and both now use a hand-set `crop_at`/`ax`. Nothing else
  flagged for review.
- All footage is freshly fetched stock (the site's own two images for this
  post are too bright and too small to use, per the script's own docstring)
  — every clip's folder is new to the tinnitus channel, so there's no
  reused-asset risk to check here.
- `assets/stock/manifest.json` updated with the 22 new assets used across the
  pair (21 clips + the shared thumbnail photo), same commit.

**Open a fresh session and run `/publish-video`.**
