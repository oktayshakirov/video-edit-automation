# Handoff to /publish-video

**Built:** 2026-08-28 · **Project:** tinnitus (article explainer pair)
**Source article slug:** `why-does-tinnitus-spike`
(`~/Coding/tinnitus-blog/content/posts/why-does-tinnitus-spike.mdx`)
**Article URL:** https://tinnitushelp.me/blog/why-does-tinnitus-spike
**Committed:** `21d37b6` on branch `skills/three-per-project-build`

## What was built

A long-form 16:9 explainer and its vertical Short, from one article.

- **Long form** - 3:19, seven chapters. Beats: `stat` (how long spikes last),
  `grid` (trigger groups), `steps` (the first-ten-minutes routine), `compare`
  (a spike vs real damage). Voice `mia`, music `night-drift`.
- **Short** - 51s. Beats: `grid` (what tips a spike over), `steps` (the
  routine). Outro is call-to-action first ("So try it tonight."), then the
  red-flag routing as an explicit exception. Voice `mia`, music `night-drift`
  at 0.85.

Medical line held: the routine is described as calming the nervous system,
never as treatment; both cuts route to a doctor and carry the article's red
flags (new, one-sided, pulsatile, with hearing loss or dizziness). No
initialisms spoken. Disclaimer is in `Meta.credits` so it lands in the
YouTube description.

## Files (all absolute)

### Long form (16:9) - YouTube, Facebook native video, Telegram, site entry
- Video:     `/Users/oktayshakirov/Desktop/tinnitus-spike-long.mp4`
- Captions:  `/Users/oktayshakirov/Desktop/tinnitus-spike-long.srt`
- Thumbnail: `/Users/oktayshakirov/Desktop/tinnitus-spike-long-thumb.jpg` (1280x720)
- Metadata:  `/Users/oktayshakirov/Desktop/tinnitus-spike-long.md` (title, description, chapters, tags)

### Short (9:16) - YouTube, Instagram Reel, Facebook Reel, TikTok draft
- Video:        `/Users/oktayshakirov/Desktop/tinnitus-spike-short.mp4`
- Reel cover:   `/Users/oktayshakirov/Desktop/tinnitus-spike-short-thumb.jpg` (1080x1920)
- YT thumbnail: `/Users/oktayshakirov/Desktop/tinnitus-spike-short-thumb-yt.jpg` (1280x720)

## Metadata

- **Long title:** `Why Does Tinnitus Spike?`
- **Short title:** use the long title or a tightened form; the Short has no
  separate metadata sidecar.
- **Thumbnail headline (both):** `Why does tinnitus spike?` with "spike?" on
  the red accent plate.
- **Tags:** tinnitus, tinnitus spike, tinnitus flare up, why does tinnitus get
  louder, ringing in ears louder, tinnitus worse today
- Full description text is in `tinnitus-spike-long.md`.

## Undecided / notes

- The Short's YouTube cover is the 16:9 `-thumb-yt.jpg`; the 9:16
  `-thumb.jpg` is the Reel/TikTok cover. YouTube Studio has no clean way to
  set a 9:16 image on a Short - handle per `docs/publish/youtube.md`.
- Project files: `projects/tinnitus-long/why-does-tinnitus-spike.py`,
  `projects/tinnitus-short/why-does-tinnitus-spike.py`.
