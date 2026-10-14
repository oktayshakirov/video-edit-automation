# Handoff: you-are-the-problem (drone quote Short)

Approved by the user 2026-10-15. Channel: drone. **Nothing has been published
yet.**

A 9:16 stacked quote Short: Sunset 6 (sun going down over Grunewald) on top,
Teufelsberg 2 (the radar domes at sunset) below, with the line read by `leo`
on the black band between them. A sarcastic motivational quote, said straight
with no "i read a quote" opener:

> everything bad in your life happens for a reason. and the reason is that you
> are STUPID and make bad decisions. you are the problem.

Ink karaoke captions (Iowan italic), "STUPID" as an 80px set-piece word with a
shake. Footage ungraded, as the user asked.

**No source article** - it is an off-site line, so there is no slug.

## Files

| What | Path |
| --- | --- |
| Video (11.91s, ffprobed, 1080x1920, narration only) | `/Users/oktayshakirov/Desktop/you-are-the-problem.mp4` |

Script: `projects/drone-short/you-are-the-problem.py`. No thumbnail, SRT or
metadata sidecar - this engine does not write one.

## Still open - decide during publishing

- **Title, caption and tags are not written yet.** The line itself is the
  hook; nothing has been drafted or agreed.
- **Audio.** The render carries the narration only. Whether music goes under it
  before upload has not been discussed.

---

# Also pending from the previous build session

The handoff below was already in this file, uncommitted to any publish, when
the Short above was approved. Kept rather than overwritten - check with the
user whether it has gone out yet.

## Handoff: shut-up-tinnitus-sample (long form only)

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
