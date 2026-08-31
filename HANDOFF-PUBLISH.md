# Handoff to /publish-video

**Built:** 2026-08-31 · **Project:** crypto (crypto-og bio pair)
**Source article slug:** `ruja-ignatova`
(`~/Coding/crypto-wiki/content/crypto-ogs/ruja-ignatova.mdx`)
**Article URL:** https://thecrypto.wiki/crypto-ogs/ruja-ignatova
**Committed:** see the commit this handoff ships with, on `main`.

## What was built

A long-form 16:9 explainer and its vertical Short, from one crypto-og article.

- **Long form** — 3:55, seven chapters. Beats: `stat` x4 (`$4B+` taken in,
  `0` public blockchains, `$5M` reward, `1 minute` to check — all `count=False`),
  `compare` (ON THE SLIDES vs WHAT WAS REAL, `name_columns=True`), `quote`
  ("There was no blockchain. There was a spreadsheet."), `steps` (2014–2022
  timeline, 5 nodes), `checklist` ("COULD YOU VERIFY ANY OF IT?", flow, ✗✗✗✗),
  `grid` (the four convicted co-conspirators + sentences). Voice `mia`, music
  `night-drift`.
- **Short** — ~55s. One drawn beat: `checklist` ("COULD YOU CHECK ANY OF IT?",
  two-phase, all ✗) plus a `chapter` card ("STILL MISSING"). Opens on its own
  title question; closes on "So, what do you think — where is she now?". Voice
  `mia`, music `night-drift` at 0.85 (now the `render_crypto_short` default).

**The angle:** how do you sell a cryptocurrency that does not exist? OneCoin
took in $4B+ with no blockchain, no mined coins, no way to cash out — the "coin"
was rows in a company database and a mining animation. The long form walks the
MLM/Ponzi mechanism, the regulator warnings that started in year one, the
four-question check that would have caught it, the disappearance, and the
convictions of everyone who did not vanish. The Short does the single move.

**No financial advice.** Fraud mechanics only — no price level, no prediction,
nothing rated, nothing recommended. Both cuts end on a plain question and stop
(no "comment below", no "subscribe"). The bare line "Nothing in this video is
financial advice." is spoken in the long form **with "This is not financial
advice." on screen**, and the disclaimer is also in `Meta.credits` for the
YouTube description.

## Files (all absolute)

### Long form (16:9) — YouTube, Facebook native video, Telegram, site entry
- Video:     `/Users/oktayshakirov/Desktop/crypto-ruja-ignatova-long.mp4`
- Captions:  `/Users/oktayshakirov/Desktop/crypto-ruja-ignatova-long.srt`
- Thumbnail: `/Users/oktayshakirov/Desktop/crypto-ruja-ignatova-long-thumb.jpg` (1280x720)
- Metadata:  `/Users/oktayshakirov/Desktop/crypto-ruja-ignatova-long.md`

### Short (9:16) — YouTube Short, Instagram Reel, Facebook Reel, TikTok draft
- Video: `/Users/oktayshakirov/Desktop/crypto-ruja-ignatova-short.mp4`
- Cover: `/Users/oktayshakirov/Desktop/crypto-ruja-ignatova-short-thumb.jpg` (1080x1920)
- No metadata sidecar for the Short — use the block below.

## Metadata

### Long form
Full title, description and chapter list are in `crypto-ruja-ignatova-long.md`.
- **Title:** `How OneCoin Sold $4 Billion of a Coin That Didn't Exist`
- **Thumbnail headline (long):** `The coin that never [existed]`
  ("existed" on the yellow accent plate; source is `ruja-glamour.jpg`)
- **Thumbnail headline (short):** `The coin that [never existed]`
  (two-word accent on the Short so it stays two lines clear of her face)
- **Tags:** ruja ignatova, onecoin, cryptoqueen, crypto scams, ponzi scheme

### Short (no sidecar — use this)
- **Title:** `How OneCoin Sold a Coin That Never Existed`
- **Description:**
  ```
  OneCoin took in over $4 billion with no blockchain and no way to cash out. Ruja Ignatova, the "Cryptoqueen", vanished in 2017 and is still on the FBI's Ten Most Wanted list.

  Full story: https://thecrypto.wiki/crypto-ogs/ruja-ignatova

  Nothing in this video is financial advice.
  ```
- **Hashtags:** #rujaignatova #onecoin #cryptoqueen #cryptoscam

## Attribution — MANDATORY in every published description

Two of the images are CC BY-SA, which makes the video a derivative work:

> Portrait of Ruja Ignatova ("Dr. Ruja Ignatova") by OneCoin Corporation,
> CC BY-SA 2.0, via Wikimedia Commons. This video is shared under CC BY-SA 4.0.
> FBI Ten Most Wanted poster image: Federal Bureau of Investigation, public
> domain.

This block is already in `crypto-ruja-ignatova-long.md`'s Credits section. It
must also go in the Short's description and the site `videos.json` entry.

## Undecided / notes

- **Short distribution:** the full table — YouTube Short + Instagram Reel +
  Facebook Reel + TikTok draft — per the 2026-08-31 decision (the old
  "crypto Shorts stay YouTube-only" rule is stale; see MEMORY.md).
- **Video poster:** fetch YouTube's own `maxresdefault.jpg` after upload; do
  not composite one locally.
- **No photo of Konstantin Ignatov** exists (not on Wikimedia Commons, DOJ
  arrest photo not cleanly PD). His shot is a labelled courtroom clip — this is
  a known limitation, not a fix pending.
- **"Ruja" is pronounced "Roozha"** (Bulgarian Ружа). The voiceover respells it;
  Kokoro still puts the stress of "Ignatova" one syllable late and has no stress
  control — accepted for this cut.
- **Voice delivery** is at Kokoro's ceiling. Engine swap is a live user
  question, not blocking this publish.
