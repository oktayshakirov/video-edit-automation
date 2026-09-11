# Handoff → /publish-video

**Built:** `golden-girl-rejections` — a stacked vertical quote Short
(`/video-drone`), off-site (no article).
**Source clips:** the user's own footage, not tracked by `tools/topics.py`
(no `SOURCE_POST`) — `~/Desktop/Golden Girl Night Hyperlapse 3.mp4` and
`~/Desktop/Golden Girl Night.mp4`, both the Victory Column (Siegessäule) in
Berlin at golden hour.
**Script:** `projects/drone-short/golden-girl-rejections.py`
**Date:** 2026-09-11
**Voice:** `leo` (`am_onyx` 0.60 + `af_nicole` 0.40, speed 0.95, melancholic
chain) — the approved drone-quote voice.
**Approved by the user** after three review rounds (band trimmed 140→120→100,
the set-piece word removed then restored as two words — `excited` and `no`).
**Committed:** this commit, on `main`. Working tree clean once pushed.

---

## Files (Desktop)

| what | path |
| --- | --- |
| short video (9:16) | `/Users/oktayshakirov/Desktop/golden-girl-rejections.mp4` |

- **12.82s** (ffprobed), 1080x1920, h264/aac, silent (no narration audio track
  omitted — narration **is** the audio track; there is no music bed yet).
- No thumbnail, no `.srt`, no `.md` sidecar — drone short (like drone long)
  produces none of these. This handoff is the description carrier.
- **No music laid over yet.** Per `docs/video/projects/shorts.md`, background
  music for a drone quote short is added by hand after the render — the long
  gaps and 1.2s tail are sized for that. Decide before/if this gets a track;
  it will play with voice-only silence between lines otherwise.

## What it is

A single stacked-vertical quote, two Golden Girl / Victory Column clips top
and bottom, black band between them (100px), quote read on the band:

> i heard someone say, "if you know you were 100 rejections away from your
> dream, think how excited you'd be every time someone told you no." and then
> it stuck with me.

`excited` and `no` both render oversized (88px against the 44px body) — two
set-piece words rather than the usual one, on the user's explicit call: the
line has two turns, the reframe and the word it reframes. Every other caption
karaokes at the base size, highlight colour auto-pulled from the footage
(comes back red off this sunset — not re-pinned, the user didn't ask).

## Where it goes

**YouTube and TikTok only.** Per the publish table, drone Shorts have no
Instagram or Facebook page wired up and take no site entry.

Channel: **`drone`**.

## Metadata — proposed, not settled

Unlike drone **long** form, this repo has no documented settled template for a
drone **short's** title/description (the long-form template — cross-links,
Drone Pal, location/gear lines — is built for a 4K flight video and does not
fit a 13-second quote card). Treat the below as a starting draft, not a
paste-and-go block; sanity-check tags and description length against whatever
the drone Shorts channel has actually shipped before, if anything comparable
has.

- **Title:** `100 Rejections Away From Your Dream #shorts`
  (plain hyphen convention n/a — no hyphen in this one; `#shorts` at the end
  per the settled YouTube baseline)
- **Description:**
  ```
  If you know you're 100 rejections away from your dream, every "no" is one step closer.

  #motivation #mindset #rejection #shorts
  ```
- **Tags:** `motivation, mindset, rejection, quote, dreams, berlin, drone, aerial, golden hour, shorts`
- **TikTok caption:** same opening line as the description, no link (TikTok
  gets no site or article to point at here).

## Undecided / notes for publish

- **No music bed.** Confirm with the user whether this ships silent-with-voice
  or gets a track first — TikTok's own audio-strategy rule
  (`docs/video/projects/drone-short.md`) says a narrated short gives up the
  trending-sound lever either way, so silence isn't a TikTok-specific problem,
  but a long-form-quote short with no music under it may read as unfinished.
- **No thumbnail/cover file.** Per `docs/publish/youtube.md`, a Short's cover
  can only be set by hand in Studio anyway — pick a frame from the video
  (the Victory Column lit up, top or bottom tile, reads well) rather than
  generating one.
- **Karaoke highlight is red** (auto-pulled from the sunset). Flagged to the
  user during build and left as-is by their choice — not a bug, just noting it
  here in case it reads oddly on TikTok's smaller preview.
- Title/description above are a first draft — see "Metadata" note.

**Open a fresh session and run `/publish-video`.** Nothing here is posted,
scheduled, or entered into any registry.
