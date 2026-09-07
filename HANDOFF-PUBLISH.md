# Handoff → /publish-video

**Built:** `quiz-tinnitus-basics` — the first video in the new **quiz Short**
format (`/video-quiz`), for tinnitushelp.me.
**Source article:** none. `SOURCE_POST = None` in
`projects/quiz-tinnitus/tinnitus-basics.py` — see "Not sourced from an
article" below before publishing.
**Date:** 2026-09-08
**Voice:** `otis` (`am_puck`, ENERGETIC chain, speed 1.00) — the male article
reader, same voice both channels' explainers use. Still `candidate`, not
approved.
**Approved by the user** after four review rounds on this exact content: the
pacing (letters and cards running together, a countdown starting mid-word),
the tick level against a new music bed, the reveal wording, and the voice.

---

## Files (Desktop)

| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/quiz-tinnitus-basics.mp4` |
| thumbnail (9:16) | `/Users/oktayshakirov/Desktop/quiz-tinnitus-basics-thumb.jpg` |

**75.5s**, 1080x1920, h264/aac. No SRT and no `.md` sidecar — a quiz burns its
own type as drawn cards rather than captions, and there is no long form to
carry chapters.

No title, description or tags are written anywhere. `/publish-video` will
need them; nothing here should be treated as already decided.

## What it is

Three general tinnitus questions, each a four-card multiple choice with an
eight-second countdown and a marked reveal:

1. Where tinnitus actually comes from (brain filling a gap in the signal, not
   earwax or blood pressure).
2. Whether silence makes it louder (it can make it more *noticeable* — a
   masking-sound point, not a severity claim).
3. Which of four statements is a myth ("nothing can be done" is the myth;
   habituation is real).

Outro: "How many did you get?" — no "tell me in the comments," on the user's
call that a scored quiz prompts comments on its own.

## Not sourced from an article — read this before publishing

**Every other video this repo ships is built from one post's own content**, so
a wrong-answer card is a misconception the source article corrects, not a
claim this session made up. This one is not: `SOURCE_POST = None`, and the
three questions are general audiology rather than any tinnitushelp.me post's
`quickFacts`.

This was a deliberate tradeoff, not an oversight — the user was asked whether
to pick a real article and build from it, or approve this exact
engine-verification render as-is, and chose the latter. Flagging it here
because `/publish-video` cannot see that conversation and the render alone
does not show which path was taken.

Nothing in the three questions makes a diagnostic or treatment claim — checked
against `docs/video/projects/tinnitus.md`'s rule before this was written up —
but "checked by the build session" is a lower bar than "corrects a specific
article's content," and that gap is worth knowing about before this goes to a
health audience.

## The engine this shipped

`docs/video/projects/quiz.md` has the full account; the short version is that
three things were tried, measured wrong, and fixed on this exact render before
it was approved:

- A scripted pause under `RUN_BREAK_GAP` is a request `_pad_pause` can only
  honour where the model happened to leave a pause — not a guarantee. Fixed
  with a `run_break` threshold the quiz lowers to make every card boundary a
  real silence.
- A letter spoken alone ("A.") is flat and sounds wrong — measured on the
  pitch track, 127→127 Hz alone against 137→208 Hz in context. The letter now
  travels with its option as one utterance.
- The countdown ticks were inaudible under a new -32 LUFS music bed at their
  original level; raised until they measured +6 dB over the bed.

## What `/publish-video` still needs to do

Same sequence as every other Short: YouTube Shorts upload with a title,
description and the thumbnail above; the Reel workflows in n8n for Instagram
and Facebook; the TikTok draft; a `videos.json` entry on tinnitushelp.me. No
long form exists for this format, so there is nothing to pair it with and no
16:9 thumbnail to make.

**No title has been proposed.** `docs/video/shorts.md`'s title conventions are
written for an article Short with a source post to search-bind against; this
one has none, so pick a title fresh rather than reaching for that section.
