# Handoff → /publish-video

**Built:** `perpetual-futures` — a thecrypto.wiki article explainer pair (long 16:9 + vertical Short).
**Source article:** `what-are-perpetual-futures`
`https://thecrypto.wiki/posts/what-are-perpetual-futures`
**Date:** 2026-09-04
**Voice:** `mia` (`af_heart`) — the crypto explainer default. Still `candidate`.

---

## Files (all on the Desktop)

### Long form (YouTube)
| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/perpetual-futures-long.mp4` |
| captions (SRT) | `/Users/oktayshakirov/Desktop/perpetual-futures-long.srt` |
| metadata sidecar | `/Users/oktayshakirov/Desktop/perpetual-futures-long.md` |
| thumbnail (16:9) | `/Users/oktayshakirov/Desktop/perpetual-futures-long-thumb.jpg` |

Runtime **3:22** (202.96s). 6 chapters (in the sidecar). Title: **What Are Perpetual Futures?**
The sidecar carries the full description, chapters, tags and the financial-advice disclaimer — use it, do not re-derive.

> **Note on the long thumbnail:** the `.mp4`/`.srt`/`.md` are from the approved render, unchanged.
> The `-thumb.jpg` was regenerated standalone afterwards (review caught "EXPIRES" clipping off
> the right edge on the first headline, and asked for simpler text) — same source photo, new
> headline "What Are Perpetual [Futures]?". The video itself was never re-rendered. A fresh
> `render_long` from the committed script would reproduce today's thumbnail exactly.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)
| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/perpetual-futures-short.mp4` |
| thumbnail (9:16 Reel cover) | `/Users/oktayshakirov/Desktop/perpetual-futures-short-thumb.jpg` |

Runtime **47.5s**. No SRT (Shorts don't get one). No metadata sidecar — `/publish-video` writes the short captions.

**What the Short covers, for the captions:** why a contract with no expiration date doesn't just
drift away from the real price — a perpetual future lets you trade something like Bitcoin with
leverage and never expires; an ordinary futures contract settles on a date and that date is what
pulls its price back to reality, this one has none; so a fee does that job instead, paid directly
between traders every few hours — above the real price, longs pay shorts, below it, shorts pay
longs; it's a small fee, not the exchange getting rich, just two traders settling up automatically;
closes on "so what's actually keeping a price like that honest?". **No financial-advice line** —
per the user's standing rule (2026-09-04), Shorts on this channel never carry the compliance line,
only the paired long form does; do not add one during captioning.
Distribution: **full table** (YouTube Short + IG Reel + FB Reel + TikTok) — per the standing note
that crypto Short distribution is contested/full-table now, not YouTube-only.

---

## Site registry
`videos.json` (crypto-wiki repo) entry should point at the source post slug `what-are-perpetual-futures`.

## Meta / Facebook token
Per the standing note, the n8n Facebook Graph credential expires ~every 60 days and blocks the IG Reel + FB Reel + FB long video steps. If those fail, the user re-auths in n8n and the run resumes.

---

## Undecided / worth a look before or during publish

- **Exchange logos in the long form** (`logos` beat: Binance, Bybit, Kraken, Hyperliquid, grouped
  centralized vs. decentralized) — no per-tile verdict marks, since this isn't a judgement, just
  where the contract trades. Confirmed rendering correctly on a pulled frame.
- **`bars` beat** (leverage vs. how far the price can move against you) is pure arithmetic, no
  price level or recommendation — confirmed on review, nothing to flag.
- **Assets are entirely fresh** for this post — nothing shared with any other crypto video, so no
  cross-video reuse to reconcile in the manifest beyond what's already committed.
- **`mia` voice** — still `candidate`, but every shipped crypto explainer pair uses it and the user
  approved this pair without comment on the voice.

## Repo state
All code + docs committed on `main` (commit `acca8eb`):
- `projects/crypto-long/perpetual-futures.py`, `projects/crypto-short/perpetual-futures.py`
- `docs/video/narration.md` — new rule: Shorts on this channel never carry the financial-advice
  compliance line, only the paired long form does.
- `docs/video/voice.md` — new finding: a `chapter` beat's on-screen card and its spoken sentence
  must be split into a `(caption, spoken)` pair when the card is ALL CAPS; a bare capitalised `IT`
  phonemizes as the initialism "I.T." (caught by the user on the first cut, at 0:34, fixed and
  re-rendered before this handoff).

Working tree clean. Open a fresh session and run `/publish-video`.
