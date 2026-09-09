# Handoff → /publish-video

**Built:** `quiz-tinnitus-myths-vs-reality` — a quiz Short (`/video-quiz`) for
tinnitushelp.me.
**Source article:** `tinnitus-blog/content/posts/tinnitus-myths-vs-reality.mdx`
— `SOURCE_POST = "tinnitus-myths-vs-reality"` in
`projects/quiz-tinnitus/tinnitus-myths-vs-reality.py`. Every wrong option on
every card traces to that article's own "Reality" paragraphs; nothing here is
invented.
**Date:** 2026-09-10
**Voice:** `otis` (`am_puck`, ENERGETIC chain) — the male article reader, same
voice both channels' explainers use.
**Approved by the user** after several review rounds, all on the same one
question: how the four lettered options on each card should sound. See "The
letter is shown, never spoken" below — that is the one piece of this build
worth reading in full before publishing, because it changed what the audio
actually contains partway through the project's history.

---

## Files (Desktop)

| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/quiz-tinnitus-myths-vs-reality.mp4` |

**81.7s**, 1080x1920, h264/aac. No SRT, no thumbnail file, no `.md` sidecar —
a quiz burns its own type as drawn cards rather than captions, and the format
does not call `render_short_thumb` at all (see "No thumbnail render" below).
There is no long form to pair this with.

No title, description or tags are written anywhere yet. `/publish-video` will
need them; nothing here should be treated as already decided. The on-screen
title card reads "Tinnitus Quiz: Myths Edition" — that is narration/caption
text burned into the video, not a proposed YouTube/social title.

## What it is

Three questions from the article, each a "which of these is a myth about
tinnitus?" with four lettered cards, a 6-second countdown, and a marked
reveal:

1. **Cause.** Myth: "loud noise is the only cause." Reality: ear infections,
   aging and certain medications cause it too.
2. **Duration.** Myth: "it always resolves within a few days." Reality: it
   can fade, but for many it becomes chronic.
3. **Treatment.** Myth: "there is nothing that can be done about it." Reality:
   sound therapy, CBT and hearing aids all help manage it.

Outro: "How many did you get?" — no "tell me in the comments," on the
format's standing call that a scored quiz prompts comments on its own.

Every wrong option is one of the article's own true statements about an
*adjacent* myth, not an invented distractor — checked against
`docs/video/projects/tinnitus.md`'s rule before any of the three questions
were written. No diagnostic or treatment claim, no ear close-ups.

## The letter is shown, never spoken — read this before publishing

**This is the one thing about this build that is not routine**, because it
changed the audio itself after the video had already been sent for review
more than once. A card reads "B. It has no effect." on screen. The voice only
ever says "It has no effect." — the letter is never sent to the synthesiser
as its own utterance, on any card, anywhere in the format.

That is the end state of eight attempts at making a *spoken* letter sound
right next to its answer — isolated, forced-spliced, synthesised in context
then cut free, gated to half the cards, given a carrier word whose consonant
leaked through, and finally a correctly measured, cleanly bounded silence
inserted into an untouched natural read. That last one passed every waveform
check and was still rejected by ear: a letter's own spoken length is
0.15-0.36s, and a sound that short, spoken alone, reads as clipped no matter
how cleanly it is cut. The fix was not a better cut — it was not asking
Kokoro to say the letter at all. Full account: `LETTER_SPOKEN` in
`video_automation/quiz/build.py`, and `docs/video/projects/quiz.md`.

**Why this belongs in a publish handoff and not just a commit message:** if
this render is ever compared against an earlier cut of the same video, or
against screenshots/notes from an earlier review round, the letters will
sound different — earlier cuts spoke every letter (badly, which is why they
were sent back), this one speaks none of them. That is not a regression to
flag; it is the fix landing. The reveal is unaffected either way — "The
correct answer is B." was never part of the problem and still speaks the
letter out loud, as a real sentence.

## No thumbnail render

The format does not call `render_short_thumb` — the video's own picture is
already four drawn cards, and a generated headline plate would restate the
hook a viewer is about to see in the first two seconds. Pull the Reel cover
from a frame of the finished render instead, per
`docs/publish/instagram-facebook.md`. A Short gets no thumbnail from the
YouTube API regardless of format, and TikTok's draft cover is set by hand.

## What `/publish-video` needs to do

This is a **short only** — the standard "tinnitus short" row of the platform
table: YouTube (Short), Instagram Reel, Facebook Reel, TikTok (draft). **No
site entry** — shorts do not get one, and there is no long form to pair this
with or attach a `videos.json` row to.

- **YouTube Shorts** — title, description, the usual `youtube-audit` dry run
  then `--apply`.
- **Instagram Reel** and **Facebook Reel** — via the tunnel, per
  `docs/publish/instagram-facebook.md`. Cover pulled from a render frame, not
  a generated thumbnail (see above).
- **TikTok** — draft, per `docs/publish/tiktok.md`; cover set by hand in the
  draft.

No title has been proposed for any platform — pick one fresh rather than
reaching for `docs/video/shorts.md`'s source-bound conventions, since this is
a quiz format with its own on-screen title already burned in.
