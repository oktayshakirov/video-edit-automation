# Handoff → /publish-video

**Built:** `pulsatile-tinnitus` — a tinnitushelp.me article explainer pair (long 16:9 + vertical Short).
**Source article:** `pulsatile-tinnitus-why-you-hear-your-heartbeat`
`https://tinnitushelp.me/blog/pulsatile-tinnitus-why-you-hear-your-heartbeat`
**Date:** 2026-09-02
**Voice:** `otis` (bare `am_puck`, ENERGETIC chain, speed 1.00) — the male article reader added this session. First shipped use of the profile. Still `candidate`.

---

## Files (all on the Desktop)

### Long form (YouTube)
| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/pulsatile-tinnitus-long.mp4` |
| captions (SRT) | `/Users/oktayshakirov/Desktop/pulsatile-tinnitus-long.srt` |
| metadata sidecar | `/Users/oktayshakirov/Desktop/pulsatile-tinnitus-long.md` |
| thumbnail (16:9) | `/Users/oktayshakirov/Desktop/pulsatile-tinnitus-long-thumb.jpg` |

Runtime **2:56** (176.06s). 7 chapters (in the sidecar). Title: **Why Can You Hear Your Heartbeat in Your Ear?**
The sidecar carries the full description, chapters, tags and the medical disclaimer — use it, do not re-derive.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)
| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/pulsatile-tinnitus-short.mp4` |
| thumbnail (9:16 Reel cover) | `/Users/oktayshakirov/Desktop/pulsatile-tinnitus-short-thumb.jpg` |
| thumbnail (16:9 YouTube) | `/Users/oktayshakirov/Desktop/pulsatile-tinnitus-short-thumb-yt.jpg` |

Runtime **49.1s**. No SRT (Shorts don't get one). No metadata sidecar — `/publish-video` writes the short captions.

**What the Short covers, for the captions:** why you hear your own heartbeat in your ear = pulsatile tinnitus; it's turbulent blood flow near the ear amplified into a whoosh; common causes (narrowed vessels, pressure around the brain, middle-ear fluid, anemia/thyroid); unlike ordinary ringing this kind often has a cause a doctor can find and sometimes treat; get it checked — especially if sudden, one-sided, or with headaches/vision changes; while you wait: soft sound at night, raise the head of the bed, track what changes it.
Distribution: full table (YouTube Short + IG Reel + FB Reel + TikTok).

---

## Crypto Short distribution note
Not relevant here (this is tinnitus), but per the standing rule the tinnitus Short goes to the full table above.

## Site registry
`videos.json` entry points at the source post slug `pulsatile-tinnitus-why-you-hear-your-heartbeat`.

---

## Undecided / worth a look before or during publish

- **`otis` voice** — this is the first video rendered on it. The user said the pair is ready to publish, so treat as approved, but it has not been A/B'd against `mia` on a full render.
- **Short thumbnail** — the source photo (`woman-holding-hands-on-her-chest`, Pexels 13419231) has the subject looking down, so her face is cropped at the top edge in both the 9:16 and 16:9 covers. The hands-on-chest gesture is the subject and it reads. A different source would be needed for a full face.
- **Long thumbnail** — same photo, straight cover crop, type on the left.

## Repo state
All code + docs committed and pushed to `main`:
- `voices: add otis (am_puck) as the male article reader, arlo (am_liam) as alternate` (9224e01)
- `tinnitus: pulsatile-tinnitus long + short pair` (this handoff's commit)

Working tree clean. Open a fresh session and run `/publish-video`.
