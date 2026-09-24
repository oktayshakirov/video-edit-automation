# Handoff: Can Neck Tension Cause Tinnitus? (tinnitus long + short pair)

Built and committed 2026-09-24 (`17a789e`). The working tree is clean.

## Source

- Article: `can-neck-tension-cause-tinnitus`
  (`tinnitus-blog/content/posts/can-neck-tension-cause-tinnitus.mdx`)
- URL: https://tinnitushelp.me/blog/can-neck-tension-cause-tinnitus
- The long-form title is the article's own title, which is already a search
  phrase people type: "Can Neck Tension Cause Tinnitus?". The Short takes the
  self-test angle ("the 30-second neck test"), so the two are not competing
  for one results page.

## Files, long form

- Video: `/Users/oktayshakirov/Desktop/can-neck-tension-cause-tinnitus-long.mp4` (3:36)
- Thumbnail: `/Users/oktayshakirov/Desktop/can-neck-tension-cause-tinnitus-long-thumb.jpg`
- Captions: `/Users/oktayshakirov/Desktop/can-neck-tension-cause-tinnitus-long.srt`
- Metadata sidecar: `/Users/oktayshakirov/Desktop/can-neck-tension-cause-tinnitus-long.md`
  (title, description, chapters, tags, credits with the medical disclaimer)
- Script: `projects/tinnitus-long/can-neck-tension-cause-tinnitus.py`

Seven chapters, first at 0:00, all over 10s — `meta.check_chapters` is clean.

## Files, Short

- Video: `/Users/oktayshakirov/Desktop/can-neck-tension-cause-tinnitus-short.mp4` (44.4s)
- Thumbnail: `/Users/oktayshakirov/Desktop/can-neck-tension-cause-tinnitus-short-thumb.jpg`
- Script: `projects/tinnitus-short/can-neck-tension-cause-tinnitus.py`
- Opening line, and the natural title: **"Can Your Neck Really Change Your
  Tinnitus?"** No sidecar, as with every previous Short; the publish step
  writes its description.

## The medical line, which this topic needs

Nothing is diagnosed and no relief is promised. The strongest claim in either
cut is that the neck can be "part of the volume"; both close by saying
explicitly that the neck is **not** the cause. The red flags are spoken and on
screen in the long form (`grid`, "NOT A NECK PROBLEM") and the disclaimer is
in `Meta.credits`, so it is already in the sidecar's description — **do not
drop it when pasting.** Same-day items: sudden hearing loss, tinnitus keeping
time with the pulse, severe pain after a head or neck injury, dizziness that
will not settle, new facial weakness.

## Anything still undecided

The user approved both renders after three rounds of re-cuts. Notes, none of
them blocking:

- Voice `mia`, music `night-drift`, the same on both — the pair reads in one
  voice as the project doc requires.
- Both thumbnails share one portrait source
  (`assets/stock/photos/woman-holding-her-neck-pain-dark-portrait-portrait/12572742.jpg`),
  headline "THE / 30-SECOND / [NECK TEST]". The 16:9 crop cuts the face above
  the chin deliberately, keeping the hand and neck as the subject; that was
  reviewed and kept.
- The therapist shot at ~0:19 in the Short is red-dominant. Flagged at review,
  judged acceptable, not re-cut.
- The Short's tail is 2.6s so the revealed outro card is readable before the
  loop; that is deliberate, not dead air.

## What changed in the engine this session (context, not a task)

The opener and outro were rebuilt during review and the rules are in
`docs/video/shorts.md` — the two hook modes and the cover-the-bar test, the
outro as the opener's twin, and casting a Short from close or medium shots.
Nothing here needs action at publish time; it is only relevant if a re-render
is ever required, in which case both scripts reproduce these exact cuts.
