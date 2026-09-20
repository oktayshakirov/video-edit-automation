# Handoff: New Tinnitus - The First Week (tinnitus long + short pair)

Built and committed 2026-09-20. Working tree is clean.

## Source

- Article: `new-tinnitus-what-to-do-first-week`
- URL: https://tinnitushelp.me/blog/new-tinnitus-what-to-do-first-week
- The highest-intent page on the site - somebody whose tinnitus started this
  week. Long-form title is the search phrase ("New Tinnitus? What To Do In The
  First Week"); the Short takes the tonight angle, so the two are not
  competing for one results page.

## Files, long form

- Video: `~/Desktop/new-tinnitus-first-week-long.mp4` (3:35)
- Thumbnail: `~/Desktop/new-tinnitus-first-week-long-thumb.jpg`
- Captions: `~/Desktop/new-tinnitus-first-week-long.srt`
- Metadata sidecar: `~/Desktop/new-tinnitus-first-week-long.md` (title,
  description, chapters, tags, credits)
- Script: `projects/tinnitus-long/new-tinnitus-what-to-do-first-week.py`

## Files, Short

- Video: `~/Desktop/new-tinnitus-first-week-short.mp4` (47.9s)
- Thumbnail: `~/Desktop/new-tinnitus-first-week-short-thumb.jpg`
- Script: `projects/tinnitus-short/new-tinnitus-what-to-do-first-week.py`

## Anything still undecided

The user reviewed both renders across several re-cuts and the pair ships as
built. The metadata sidecar is current with the final render (3:35, chapters
verified). Both thumbnails were regenerated after that render from the
user-picked photo, at the same paths the sidecar names.

Two notes, neither a blocker:

- **The Short opens on a statement, not a question.** "Tinnitus just started.
  Tonight is the part you can actually change." This is a deliberate departure
  from the standing "every Short opens by asking its own title question" rule,
  made on the user's note that a question mark opener read as a query rather
  than as advice. `docs/video/shorts.md` records it as an exception. Worth
  watching how it performs against the question-opener Shorts.
- **`tools/audit_assets.py` reports two false positives on this pair**
  ("CURTAINS reused only N slots apart"). The real separations are 7 and 9
  slots; the tool only indexes shots that carry an explicit `clip_at`, so it
  misjudges spacing. A fix is queued as its own task and was deliberately not
  attempted here - widening the regex surfaced a flood of unrelated
  pre-existing errors channel-wide.

## Repo-side changes in this commit

**Content**

- New stock fetched and manifested: a bedroom with curtains being drawn, a
  filament bulb on black, a ceiling fan, a bedside sound box, a lamplit
  street, and the thumbnail photo the user picked
  (pexels.com/photo/a-man-in-black-shirt-8638769). 11 new entries in
  `assets/stock/manifest.json`.

**The male explainer voice is off the roster**

- `otis` was used for one cut of this pair and rejected: it "reads the script
  very wrong - always starts with high tone and sounds excited but ends low".
  Kokoro has no prosody control, so that is not fixable in the chain.
- Removed from the explainer rosters in `docs/video/longform.md`,
  `docs/video/projects/tinnitus.md` and `docs/video/projects/crypto.md`.
  **Every article pair now reads in `mia` until a new male voice is chosen.**
- Two shipped pairs repointed to `mia` so they stay re-runnable:
  `pulsatile-tinnitus` (long + short) and `vitalik-ethereum` (long + short).
  **A re-render of either no longer reproduces its original audio.**
- **The profile stays registered, and the quiz stays on it.** The user's
  explicit call. `video_automation/quiz/build.py` still defaults to `otis`;
  `docs/video/projects/quiz.md` records why the quiz moved to it. Do not
  delete the profile as tidy-up.

**Doc updates earned by this build** (narrowest doc, no cross-posting)

- `beats.md` - three more emoji that render grey/muddy on the plum card, and
  the pattern behind it (prefer a symbol glyph over an object glyph); and that
  a `callout` needs a *landscape* photo, not just a landscape frame.
- `narration.md` - a gap under `RUN_BREAK_GAP` (1.00) is a request that drops
  silently; any pause the piece depends on goes to 1.00. Measured on this
  Short.
- `shorts.md` - the title-question opener has an exception for a how-to.
- `thumbnails.md` - forced rows for phrase integrity (and that three short
  rows set larger than two long ones); `band` is decided by where the
  subject's head is and can outrank a preference for the top; choosing
  different casting means picking by eye, because search terms do not steer it.

## Next

Open a fresh session and run `/publish-video`.
