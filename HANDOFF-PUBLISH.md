# Handoff: Bitcoin miners for AI (crypto long + short pair)

Built and committed 2026-09-16 (commit `190dc55`). Working tree is clean.

## Source

- Article: `why-wall-street-is-betting-big-on-bitcoin-miners-for-ai`
- URL: https://thecrypto.wiki/posts/why-wall-street-is-betting-big-on-bitcoin-miners-for-ai
- The angle keeps only the evergreen mechanism (why a mining site already has
  what AI needs, the retrofit gap, the income comparison, the risk) and drops
  the article's news framing (the researcher resignation, the hedge fund and
  its named positions, the named mining stocks). No company, fund, ticker,
  price or direction is named in either video.

## Files, long form

- Video: `~/Desktop/crypto-miners-ai-long.mp4` (3:00)
- Thumbnail: `~/Desktop/crypto-miners-ai-long-thumb.jpg`
- Captions: `~/Desktop/crypto-miners-ai-long.srt`
- Metadata sidecar: `~/Desktop/crypto-miners-ai-long.md` (title, description,
  chapters, tags, credits)
- Script: `projects/crypto-long/miners-ai.py`

## Files, Short

- Video: `~/Desktop/crypto-miners-ai-short.mp4` (43s)
- Thumbnail: `~/Desktop/crypto-miners-ai-short-thumb.jpg` (regenerated after
  approval with `band="top"` so the headline sits above the pylons instead of
  over them - the script (`projects/crypto-short/miners-ai.py`) already has
  this change, so re-running it reproduces the same thumbnail)
- Script: `projects/crypto-short/miners-ai.py`

## Anything still undecided

Nothing outstanding. The user approved the pair as built, with one change
(the Short's vertical thumbnail headline moved from `band="bottom"` to
`band="top"`), which is already applied to both the committed script and the
rendered thumbnail on the Desktop.

Two things worth a look during the metadata/social pass, not blockers:

- In the Short, the line "The substation is built" plays over a construction
  crane clip, not a substation - it still reads as "site being built" but is
  not a literal substation shot.
- A trading-screen clip under "investors" shows a small on-screen exchange
  label (Binance). It is illegible at short/thumbnail size but is present in
  the frame.

## Repo-side engine changes in this commit

Not part of this video's content, but shipped in the same commit and worth
knowing about before touching any other thumbnail:

- Fixed two bugs in `video_automation/longform/thumb.py`'s headline fitter
  (see `docs/video/thumbnails.md`, "The headline fitter had two bugs that hid
  each other"). Re-rendering an older thumbnail may now lay out differently
  (bigger, properly wrapped) - that is the intended fix, not a regression.
- New stock footage added to `assets/stock/videos/` and the manifest for this
  pair (pylons, substations, night construction, racks, trading screens).
