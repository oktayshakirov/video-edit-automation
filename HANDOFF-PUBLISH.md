# Handoff to /publish-video

**Built:** 2026-08-31 · **Project:** crypto (article explainer pair)
**Source article slug:** `quantum-computers-and-crypto`
(`~/Coding/crypto-wiki/content/posts/quantum-computers-and-crypto.mdx`)
**Article URL:** https://thecrypto.wiki/posts/quantum-computers-and-crypto
**Committed:** `33120fc` on branch `skills/three-per-project-build`
(branch is 13 commits ahead of `main`; the video-skill infrastructure lives
here, not on main.)

## What was built

A long-form 16:9 explainer and its vertical Short, from one article.

- **Long form** - 3:26, six chapters. Beats: `stat` (qubits to break one key),
  `compare` (signatures vs hashing, name_columns), `steps` (how a key gets
  exposed, 5 nodes), `quote` (harvest now, decrypt later), `checklist`
  ("CAN IT BE MIGRATED?", flow, ✓✓✓✗). Voice `mia`, music `night-drift`.
- **Short** - 50s. One beat: `checklist` ("IS THE KEY STILL HIDDEN?", flow,
  ✓✗✗). Opens on its own title question; closes on the comment prompt.
  Voice `mia`, music `night-drift` at 0.85.

The angle is the article's own: the overnight-doomsday version is real but
distant; the live risk is that your address is a hash of your public key, so
the key goes on the permanent record the first time you spend, and "harvest
now, decrypt later" plus a slow migration is what makes today matter.

**No financial advice.** Mechanism only - no price, no prediction (timelines
hedged), nothing rated, nothing recommended. Both cuts close on a comment
question ("Are you worried about quantum computers yet? And what are you doing
to keep your crypto safe?"). Disclaimer is in `Meta.credits` so it lands in
the YouTube description.

## Files (all absolute)

### Long form (16:9) - YouTube, Facebook native video, Telegram, site entry
- Video:     `/Users/oktayshakirov/Desktop/quantum-crypto-long.mp4`
- Captions:  `/Users/oktayshakirov/Desktop/quantum-crypto-long.srt`
- Thumbnail: `/Users/oktayshakirov/Desktop/quantum-crypto-long-thumb.jpg` (1280x720)
- Metadata:  `/Users/oktayshakirov/Desktop/quantum-crypto-long.md` (title, description, chapters, tags)

### Short (9:16) - YouTube, Instagram Reel, Facebook Reel, TikTok draft
- Video:      `/Users/oktayshakirov/Desktop/quantum-crypto-short.mp4`
- Cover:      `/Users/oktayshakirov/Desktop/quantum-crypto-short-thumb.jpg` (1080x1920)
- No metadata sidecar for the Short - use the block below.

## Metadata

### Long form
Full title, description and chapter list are in `quantum-crypto-long.md`.
- **Title:** `Quantum Computers vs. Crypto: What Actually Breaks`
- **Thumbnail headline (both):** `Can quantum computers [break] Bitcoin?`
  ("break" on the orange accent plate; source is the magnetic-field image)
- **Tags:** quantum computers crypto, quantum computing bitcoin, is bitcoin
  quantum safe, post-quantum cryptography, harvest now decrypt later, quantum
  computing explained, crypto security, crypto for beginners

### Short (no sidecar - use this)
- **Title:** `Can Quantum Computers Break Bitcoin?`
- **Description:**
  ```
  A quantum computer cracking Bitcoin overnight is the headline. The real risk is narrower - your public key goes on the permanent record the first time you spend from an address.

  Full breakdown: https://thecrypto.wiki/posts/quantum-computers-and-crypto

  Nothing in this video is financial advice.
  ```
- **Hashtags:** #quantumcomputers #bitcoin #crypto #cryptosecurity

## Undecided / notes

- **Crypto Shorts stay YouTube-only** per channel policy - only the long form
  gets a site `videos.json` entry, a poster and a social share. The Short is
  published to YouTube Shorts and nowhere else. (See `docs/video/` and the
  earlier memory note.)
- **Video poster:** fetch YouTube's own `maxresdefault.jpg` after upload;
  do not composite one locally.
- **Voice delivery** is at Kokoro's ceiling (no prosody control). The user is
  weighing an engine swap (ElevenLabs / Orpheus) - not decided, not blocking
  this publish.
- Project files: `projects/crypto-long/quantum-crypto.py`,
  `projects/crypto-short/quantum-crypto.py`.
