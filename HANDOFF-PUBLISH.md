# Handoff → /publish-video

**Built:** `caffeine-and-tinnitus` — a tinnitushelp.me article explainer pair (long 16:9 + vertical Short).
**Source article:** `caffeine-and-tinnitus`
`https://tinnitushelp.me/blog/caffeine-and-tinnitus`
**Date:** 2026-09-04
**Voice:** `mia` (`af_heart`, ENERGETIC chain, 1.10) — the explainer default. Still `candidate`.

---

## Files (all on the Desktop)

### Long form (YouTube)
| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/caffeine-and-tinnitus-long.mp4` |
| captions (SRT) | `/Users/oktayshakirov/Desktop/caffeine-and-tinnitus-long.srt` |
| metadata sidecar | `/Users/oktayshakirov/Desktop/caffeine-and-tinnitus-long.md` |
| thumbnail (16:9) | `/Users/oktayshakirov/Desktop/caffeine-and-tinnitus-long-thumb.jpg` |

Runtime **3:37** (217.86s). 9 chapters (in the sidecar). Title: **Does Caffeine Make Tinnitus Worse?**
The sidecar carries the full description, chapters, tags and the medical disclaimer — use it, do not re-derive.

> **Note on the long thumbnail:** the `.mp4`/`.srt`/`.md` are from the approved render; the
> `-thumb.jpg` was regenerated afterwards against the `INTER_AREA` fix (below), so it is a
> few KB smaller and visibly less grainy than what that render first emitted. Content is
> identical. A fresh `render_long` would reproduce exactly this thumbnail.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)
| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/caffeine-and-tinnitus-short.mp4` |
| thumbnail (9:16 Reel cover) | `/Users/oktayshakirov/Desktop/caffeine-and-tinnitus-short-thumb.jpg` |
| thumbnail (16:9 YouTube) | `/Users/oktayshakirov/Desktop/caffeine-and-tinnitus-short-thumb-yt.jpg` |

Runtime **56.1s**. No SRT (Shorts don't get one). No metadata sidecar — `/publish-video` writes the short captions.

**What the Short covers, for the captions:** does caffeine make tinnitus worse — for most people it does not universally, and quitting suddenly can be the bigger mistake; abrupt withdrawal brings headaches, poor sleep and irritability, all of which push tinnitus up, so cold turkey *looks* like proof caffeine was the culprit; what actually stacks a spike (a cup too late, the bad night after, a stressful week, energy drinks on top); how to test it — log drinks/sleep/ringing, move the last cup earlier before cutting, only then taper slowly, judge after two weeks; usually it is the timing, not the caffeine; **exception**: if tinnitus is new, one-sided, or pulses with the heartbeat, see a doctor first.
Distribution: **full table** (YouTube Short + IG Reel + FB Reel + TikTok).

---

## Site registry
`videos.json` entry points at the source post slug `caffeine-and-tinnitus`.

## Meta / Facebook token
Per the standing note, the n8n Facebook Graph credential expires ~every 60 days and blocks the IG Reel + FB Reel + FB long video steps. If those fail, the user re-auths in n8n and the run resumes.

---

## Undecided / worth a look before or during publish

- **Short runtime 56s** — a little over the 40–50s target for the format. It reads fine; the extra came from adding a proper hinge sentence before the `grid` list (a review fix). Not worth a re-cut, but noted.
- **Short's final shot** — the 9:16 crop of the kitchen-silhouette clip (`man-drinking-from-mug`, `clip_at=10`) sits mostly on the man's dark back under "get that checked by a doctor first". Murky but brief; acceptable.
- **Thumbnail** — shared source `man-coffee-mug-dark-serious/32536421.jpg` (Pexels), subject right, type left, orange accent, question mark inside the plate. `render_thumb`'s scorer still prints a marginal-composition warning (score 0.04); it reads fine at feed size.
- **`mia` voice** — still `candidate`, but every shipped tinnitus explainer pair uses it and the user approved this pair.

## Repo state
All code + docs committed and pushed to `main`:
- `thumb: resample thumbnail downscales with INTER_AREA, not INTER_LANCZOS4` — general fix (crypto + tinnitus), so the 16:9 thumbnail stops coming back grainier than the 9:16 from the same source.
- `tinnitus: caffeine-and-tinnitus long + short pair` (this handoff's commit) — also adds the "a drawn beat in a short needs a hinge sentence in front of it" rule to `shorts.md` and the fetched stock to `assets/stock/manifest.json`.

Working tree clean. Open a fresh session and run `/publish-video`.
