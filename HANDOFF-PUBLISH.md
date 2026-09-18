# Handoff: Tinnitus After a Concert (tinnitus long + short pair)

Built and committed 2026-09-18 (commit `4e46163`). Working tree is clean.

## Source

- Article: `tinnitus-after-a-concert`
- URL: https://tinnitushelp.me/blog/tinnitus-after-a-concert
- The newest post on the blog, not previously covered by any video. Long-form
  title is the post's own first FAQ question ("How long does ringing in the
  ears last after a concert?"), a different search angle from the Short's
  curiosity hook.

## Files, long form

- Video: `~/Desktop/tinnitus-after-a-concert-long.mp4` (3:11)
- Thumbnail: `~/Desktop/tinnitus-after-a-concert-long-thumb.jpg`
- Captions: `~/Desktop/tinnitus-after-a-concert-long.srt`
- Metadata sidecar: `~/Desktop/tinnitus-after-a-concert-long.md` (title,
  description, chapters, tags, credits)
- Script: `projects/tinnitus-long/tinnitus-after-a-concert.py`

## Files, Short

- Video: `~/Desktop/tinnitus-after-a-concert-short.mp4` (42.7s)
- Thumbnail: `~/Desktop/tinnitus-after-a-concert-short-thumb.jpg`
- Script: `projects/tinnitus-short/tinnitus-after-a-concert.py`

## Anything still undecided

Nothing outstanding. The user reviewed both renders and approved as built,
no changes requested.

Two things worth a look during the metadata/social pass, not blockers:

- In the long form (~1:40), the empty-bedroom shot under "that last one
  surprises people" renders very dark (near-black). It reads correctly in
  context but is worth a glance before it goes out.
- The long-form thumbnail renderer's layout scorer flagged a low score
  (0.01) for the source photo, meaning the type sits over some real ceiling
  detail rather than empty space. It reads fine in the rendered file, but
  check it once more at feed size before upload.

## Repo-side changes in this commit

- New stock footage fetched and added to `assets/stock/videos/` and
  `assets/stock/photos/` (concert crowds, sound-desk faders, walking home,
  earplugs, earmuffs) plus `assets/stock/manifest.json`. None of the concert
  clips used here appear in any other video on the channel.
- No engine/doc changes - this was a content-only build.
