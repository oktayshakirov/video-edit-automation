# Handoff: shut-up-tinnitus-sample (long form only)

Approved by the user 2026-10-14. Channel: tinnitushelp.me. **Nothing has been
published yet.**

The audiobook's Spotify retail sample (introduction and chapter one) as a
read-along: the cover, karaoke captions, the store badges. No new narration -
the audio is the delivered MP3, raised to -16 LUFS. Built by the new
`longform/readalong.py`, not `render_long`. There is no Short.

**No source article.** This is the audiobook, not a post. The audiobook's page
on the site is the link target instead (see below).

## Where it goes - the user's list, and only these

- **YouTube**
- **Facebook** (native video, as for any long form)
- **Telegram**
- **The site's /videos** (videos.json entry)

**Not** Instagram, **not** TikTok. Those are left out on purpose, not by
mistake.

## Files

| What | Path |
| --- | --- |
| Video (8:24) | `/Users/oktayshakirov/Desktop/shut-up-tinnitus-sample-long.mp4` |
| Thumbnail (the user's own, 1672x940 PNG) | `/Users/oktayshakirov/Desktop/shut-up-tinnitus.png` |
| Captions | `/Users/oktayshakirov/Desktop/shut-up-tinnitus-sample-long.srt` |
| Sidecar (title, description, tags, disclaimer) | `/Users/oktayshakirov/Desktop/shut-up-tinnitus-sample-long.md` |

Script: `projects/tinnitus-long/shut-up-tinnitus-sample.py`.

## Title

**Shut Up, Tinnitus - Free Audiobook Sample (Introduction and Chapter 1)**, in
the sidecar.

## Still open - check before uploading

- **`https://tinnitushelp.me/audiobook` does not exist yet.** It is the
  before-the-fold link in the description, picked over `/audio-book` because
  the site's routes are single words (`/zen`, `/videos`, `/faq`) and the code
  already calls it `AUDIOBOOK`. The user will build that page with the
  streaming links, more about the book, and this video. Until it is deployed
  the description's first link is a 404, so confirm it is live first, or ask
  the user whether to publish anyway.
- **YouTube will not make chapters** from the description's two timestamps (it
  needs three). They still work as clickable links. The sidecar flags this, and
  it is expected.

## Description notes

- Spotify and Google Play links come from `tinnitus-blog/src/const/audiobook.ts`.
- The Credits block carries the AI-narration label ("Kokoro (AI voice)") and
  the medical disclaimer with the red flags. Both stay on every platform.
