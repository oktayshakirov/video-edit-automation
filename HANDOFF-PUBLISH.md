# Handoff: the crypto whale pair

Built 2026-09-24/25, approved 2026-09-25. Committed as `aa220f3` and pushed to
`main`; the working tree was clean before this file was written.

**Open a fresh session and run `/publish-video`.** That skill owns the whole
upload sequence — which file goes where, the metadata pass, the site registry
entry, the social posts and their order. Nothing about publishing is decided
here.

## Source

One article, both videos, written in one pass:

- **Slug:** `what-is-a-crypto-whale`
- **Post:** `~/Coding/crypto-wiki/content/posts/what-is-a-crypto-whale.mdx`
- **URL:** https://thecrypto.wiki/posts/what-is-a-crypto-whale

`SOURCE_POST` is set in both build scripts, so `tools/topics.py crypto` will
see the article as covered.

## Files

### Long form — 16:9, 3:01

| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/crypto-whale-long.mp4` |
| thumbnail | `/Users/oktayshakirov/Desktop/crypto-whale-long-thumb.jpg` |
| captions | `/Users/oktayshakirov/Desktop/crypto-whale-long.srt` |
| **sidecar** | `/Users/oktayshakirov/Desktop/crypto-whale-long.md` |
| build script | `projects/crypto-long/crypto-whale.py` |

**The sidecar carries the title, description, chapters and tags — use it, do
not re-derive them.** It was regenerated on 2026-09-25 after a credits line
changed, so it is current.

- **YouTube title:** `What Is a Crypto Whale? How Big Wallets Actually Work`
- **Chapters:** 0:00 / 0:24 / 1:00 / 1:29 / 1:59 / 2:32 — six, first at zero,
  all well clear of the 10s minimum. No violations were reported.

### Short — 9:16, 46.1s

| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/crypto-whale-short.mp4` |
| thumbnail | `/Users/oktayshakirov/Desktop/crypto-whale-short-thumb.jpg` |
| build script | `projects/crypto-short/crypto-whale.py` |

**There is no `.md` sidecar for the Short** — this engine does not write one.
Its own title question is **"Who Is the Biggest Bitcoin Whale?"**, and the
line the video closes on is *"The biggest whale is not a person. It is a
warehouse."*

Both thumbnails share a headline (`THE BIGGEST WHALE IS NOT A **PERSON**`) and
the same photograph, so the pair reads as a set in a feed.

## Things the publish step should know

- **No financial advice, and it was built to that line.** Neither video names
  a price, a level, a direction, or any exchange as safe, unsafe or worth
  using. The custody point is made about exchanges as a *category*. The long
  form speaks and shows the compliance line at ~2:52; the Short deliberately
  carries none, which is this channel's standing rule for Shorts.
- **Nothing in either cut dates.** Every figure is structural — the 1,000 BTC
  and 10,000 ETH thresholds, the 21,000,000 cap — and the one dated number
  (19.7M mined) is spoken with its year attached. No corporate treasury
  figure is used.
- **Credits, already in the sidecar:** footage and the thumbnail photograph
  are Pexels (Pexels licence, no attribution required); music is oosongoo via
  Pixabay. The thumbnail photograph is Pexels 15836295 by Adrien Daurenjou and
  is committed at `assets/crypto/whale/nyc-skyscrapers.jpg`.
- **Tag the opener when logging this for the fortnightly review.** The Short
  is the **first video on this channel to use an opener variant** — `Stamp`
  rather than the redacted `hook=` — so it belongs in its own cohort in the
  E1 ledger rather than lumped in with the hooked Shorts.

## Nothing is undecided

The user reviewed both cuts, approved the videos as they are, and asked only
for the thumbnails to be redone — bigger type, the spacing fixed and a
different photograph. That was done and re-approved. There are no outstanding
re-cuts and no open questions.
