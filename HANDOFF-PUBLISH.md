# Handoff - `market-cap`, ready to publish (2026-10-06)

Built and re-cut across a build session. **Open a fresh session and run
`/publish-video`** - that skill owns the sequence, the platform split and the
site registry entry, and this file does not restate any of it.

## What was built

The explainer pair for thecrypto.wiki, long form and Short, from one post.

**Source:** `what-is-market-cap-in-crypto`
(`~/Coding/crypto-wiki/content/posts/what-is-market-cap-in-crypto.mdx`)
-> https://thecrypto.wiki/posts/what-is-market-cap-in-crypto

**Build scripts, committed:**

- `projects/crypto-long/market-cap.py`
- `projects/crypto-short/market-cap.py`

### Long form - 4:13 (253.0s), 16:9

| | |
|---|---|
| video | `/Users/oktayshakirov/Desktop/market-cap-long.mp4` |
| thumbnail | `/Users/oktayshakirov/Desktop/market-cap-long-thumb.jpg` |
| captions | `/Users/oktayshakirov/Desktop/market-cap-long.srt` |
| metadata | `/Users/oktayshakirov/Desktop/market-cap-long.md` |

YouTube title: **What Is Market Cap in Crypto? Price x Supply Explained** - a
search phrase, a different angle from the Short. Eight chapters, first at
0:00, all over 10s. Description, chapters, tags and credits are in the `.md`;
**read it rather than re-deriving any of it.**

### Short - 53s (52.7s), 9:16

| | |
|---|---|
| video | `/Users/oktayshakirov/Desktop/market-cap-short.mp4` |
| cover | `/Users/oktayshakirov/Desktop/market-cap-short-thumb.jpg` |

There is no `.md` sidecar for a Short. The cover is 1080x1920, same image and
same words as the long form's ("Cheap coin. Easy [win?]"), on two rows.

## Things the publish session should know

- **The angle.** What people connect a cheap coin with is an easy jump. Both
  cuts overturn that belief with arithmetic: price is half of a
  multiplication, doubling a 5-cent and a $50 coin takes the same extra $50M,
  and $1 across 500 trillion coins is ~5x the world economy. Summarise *that*
  in any platform copy - as mechanism, never as a call on any coin.
- **Opener, for the ledger:** both cuts open on a **`Stamp`** - "A cheap coin
  can grow more", stamped MYTH. Tag it as `Stamp`.
- **No financial advice.** No coin, platform, price level or direction is
  named in the narration. The long form speaks and shows the compliance line
  at ~3:55 and it is in the description. The Short carries none, as usual.
- **One outside figure:** world economy ~$100T a year, IMF World Economic
  Outlook - credited in the `.md`.
- **The thumbnails are the user's own image**
  (`assets/crypto/market-cap/meme-coins.jpg`, see `CREDITS.md`). It shows a
  candlestick chart and meme-coin faces, which the channel's footage rules
  normally keep out; on the thumbnail it is the user's explicit choice.
  Do not swap it.
- **Known cosmetic issue, accepted:** in the long form's last seconds the
  subscribe sting shows through behind the disclaimer band. Fixed in
  `longform/build.py` for future renders; the user chose not to re-render this
  one for it.

## Approval

After reviewing the second cut the user asked for the thumbnail change, the
commit and this handoff in one message (2026-10-06). The thumbnails were
built after that message and are as specified.
