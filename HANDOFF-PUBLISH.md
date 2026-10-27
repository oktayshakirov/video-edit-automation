# Handoff: north-korea-crypto (long + Short)

Approved by the user 2026-10-27 ("super happy with the results").
Channel: thecrypto.wiki. Voice **`noah`** (male, the voice test - crypto
pair 2 of 5, `docs/video/projects/crypto.md`), music `night-drift`. Source
article slug: `how-does-north-korea-steal-crypto`
(https://thecrypto.wiki/posts/how-does-north-korea-steal-crypto). Build
commit on `main`, pushed. **Nothing has been published yet.**

**The E8 lane, partly.** Drift (April 2026) and Bitget (September 2026) are
heists few videos answer yet; both names are in the long form's tags,
description and chapters. The subject itself is proven on three channels
(`docs/video/demand/crypto.md`, 2026-10-27; teardown in
`docs/video/demand/teardowns/how-does-north-korea-steal-crypto.md`).

## Files

| What | Path |
| --- | --- |
| Long form (4:14) | `/Users/oktayshakirov/Desktop/north-korea-crypto-long.mp4` |
| Long thumbnail | `/Users/oktayshakirov/Desktop/north-korea-crypto-long-thumb.jpg` |
| Long captions | `/Users/oktayshakirov/Desktop/north-korea-crypto-long.srt` |
| Long sidecar (title, description, chapters, tags) | `/Users/oktayshakirov/Desktop/north-korea-crypto-long.md` |
| Short (48.2s) | `/Users/oktayshakirov/Desktop/north-korea-crypto-short.mp4` |
| Short cover | `/Users/oktayshakirov/Desktop/north-korea-crypto-short-thumb.jpg` |

Scripts: `projects/crypto-long/north-korea-crypto.py`,
`projects/crypto-short/north-korea-crypto.py`. Both carry `DEMAND`.
Covers rebuild without a render: `--thumb` on either script.

## Titles

- Long: **How Does North Korea Steal Crypto? The $1.5 Billion Bybit Heist,
  Explained** (in the sidecar) - the search query first, the familiar name
  after it.
- Short: **How Did North Korea Steal $1.5 Billion in One Transaction?** -
  its own sentence 1, a different query angle from the long form. The Short
  has no sidecar; its description follows the channel's Short rules with
  the article URL and `Full video:` to the long form.

## Tagging for the review

- Openers: long `Search` ("how does north korea steal crypto"), Short
  `Search` ("how did north korea steal $1.5 billion").
- New beat: `blindsign`, in both cuts.

## The description's next step

The long description's link line names what the article adds: "Every
heist, every source and the full laundering trail". Social captions should
carry the same link.

## Credits the descriptions owe

- Long: "Headline: FBI public service announcement I-022625-PSA, 26 February
  2025." and the disclaimer - both already in the sidecar. The site's own
  Bybit and Bitget exchange cards appear as insets; no third-party press art
  was used. No Pexels or music line (dropped channel-wide 2026-10-20).
- Short: no disclaimer, by the channel rule.

## Feed check (`workflow.md` step 4)

The long title's query returns real views: BBC World Service 326k, Lume
556k, Blackfiles 1.9M; CoinGecko's mechanism-first video sits at 3.6k. Ours
promises the mechanism (what the signers saw against what they signed)
where the top results promise the heist story or the totals. The first
cover lost at 320px - every competitor said "North Korea" with the flag or
a face - so both covers were redrawn on a code-drawn DPRK flag
(`assets/crypto/north-korea/`).

## Undecided

- **The site entry.** No video points at this article yet, so a new
  `videos.json` entry is expected; the slug and poster are publish-video's
  call.
- The long form's cinematic title card prints the full YouTube title on two
  lines. The user approved it as rendered; `render_long(title=...)` would
  shorten it on a future re-cut.
