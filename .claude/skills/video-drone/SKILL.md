---
name: video-drone
description: Build drone-footage videos - a long-form Final Cut Pro timeline cut to music for YouTube, or a vertical 9:16 Short for TikTok and YouTube Shorts with quote text or AI narration. Use when the user runs /video-drone, points at a new footage folder, wants a full-length edit synced to music, wants a vertical or cropped version of drone footage, wants text or a quote over a clip, or wants an FCPXML diagnosed. Builds only; publishing is /publish-video. For article videos use video-crypto or video-tinnitus.
---

# Drone videos

**Usually one format, not a pair.** Unlike the two article projects, a drone
video is normally long *or* short - ask which, and do not build both unasked.
The two are different products with different audiences:

- **Long form** - a folder of graded selects cut to a music track, written out
  as an FCPXML and finished by hand in Final Cut. The footage *is* the product,
  so a human step in the loop is the point rather than a cost.
- **Short** - a 9:16 crop with quote text or narration, rendered headless.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with
`PYTHONPATH=.`.

## Read these, in this order

The steps live in `docs/video/workflow.md` - read it first, though a drone run
skips the topic-suggestion step, which is article-driven. Then:

| Step | Read |
| --- | --- |
| Either format | `docs/video/projects/drone.md` - the whole build lives here |
| Narration on a Short | `docs/video/narration.md` |
| Vertical mechanics | `docs/video/shorts.md` |
| Type on screen | `docs/video/design.md` |
| Music | `docs/video/audio.md` |
| Something rendered wrong | `docs/video/troubleshooting.md` |

Drone does not use the drawn beats, the site's photos or the stock shelf, so
`beats.md` and `footage.md` do not apply.

## The run

1. **Ask which format**, and for the long form, which footage folder.
2. **Build it.**
3. **Hand over and wait.** Re-cut as many times as the user asks - pacing, shot
   choice, speed, clip swaps.
4. **On approval: commit, write `HANDOFF-PUBLISH.md`, and tell the user to open
   a fresh session for `/publish-video`.**

## This skill does not publish

Everything about getting a render out is `/publish-video`'s, and it is the only
copy. Drone posts to **YouTube and TikTok only** - it has no Instagram or
Facebook page wired up and takes no site entry - but that table lives there, not
here. Do not describe upload steps or re-derive them from memory.

## The rule that matters most here

**Locking.** An approved cut is not to be silently re-derived. Read the locking
section in `docs/video/projects/drone.md` before touching an existing edit; it
is the one mistake in this project that destroys work rather than costing a
render.
