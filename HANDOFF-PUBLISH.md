# Handoff: Crypto Fear & Greed Index pair

Built and approved 2026-09-13. Commit `2f76089` on `main`, pushed. Working
tree clean at hand-off.

**Source article:** `crypto-fear-and-greed-index-for-beginners`
`https://thecrypto.wiki/posts/crypto-fear-and-greed-index-for-beginners`

Both videos are built from that one post and are published as a pair.

---

## Long form (16:9, YouTube)

| | |
| --- | --- |
| Video | `/Users/oktayshakirov/Desktop/crypto-fear-greed-index-long.mp4` |
| Thumbnail | `/Users/oktayshakirov/Desktop/crypto-fear-greed-index-long-thumb.jpg` |
| Captions | `/Users/oktayshakirov/Desktop/crypto-fear-greed-index-long.srt` |
| Metadata sidecar | `/Users/oktayshakirov/Desktop/crypto-fear-greed-index-long.md` |
| Runtime | 3:11 (191.16s) |
| Build script | `projects/crypto-long/fear-greed-index.py` |

**Title:** What Is the Crypto Fear and Greed Index?

**Chapters** (all six ≥10s, first at 0:00, no violations reported in the
sidecar):

```
0:00 The mood ring
0:20 What does the number actually measure?
0:53 How does that score get built?
1:29 Why does it swing so hard?
1:56 Why do millions watch a mood?
2:26 Can you trade off this number?
```

**The description, tags, chapter list and credits are all in the `.md`
sidecar — use it rather than re-deriving any of them.**

## Short (9:16)

| | |
| --- | --- |
| Video | `/Users/oktayshakirov/Desktop/crypto-fear-greed-index-short.mp4` |
| Thumbnail | `/Users/oktayshakirov/Desktop/crypto-fear-greed-index-short-thumb.jpg` |
| Runtime | 46.84s |
| Build script | `projects/crypto-short/fear-greed-index.py` |

No SRT and no metadata sidecar — the short format produces neither.

The Short carries **no financial-advice disclaimer**, which is the standing
rule for this channel: the paired long form carries it, and a Short closes
cold on its own last line.

---

## Things the publish step needs to know

**Both thumbnails carry the same headline, word for word** — "THIS NUMBER
CLAIMS TO KNOW CRYPTO'S MOOD" — and the same image, the index dial. That is
deliberate: a viewer who sees the second one should recognise it. The Short's
thumbnail is 1080x1920; YouTube Studio has no working way to set a 9:16 image
as a Short's cover, which is a platform quirk to solve at upload time.

**Credits that must appear in the description** (they are already in the
sidecar's credits block):

- Footage: Pexels (Pexels licence, no attribution required)
- Music: oosongoo, via Pixabay
- Fear & Greed Index scale: thecrypto.wiki
- Nothing in this video is financial advice

**Nothing in either video is financial advice, and the copy must not add
any.** No token, platform, price level or direction is named anywhere in
either script, and the dial is drawn parked at the midpoint on purpose — a
needle in the red would read as a claim about today's market. Do not write a
description, title or social post that implies a reading, a direction or a
recommendation.

## Not done, and deliberately left to `/publish-video`

- The YouTube uploads, the Reel workflows, the TikTok draft and the Facebook
  upload.
- The `videos.json` registry entry on the site.
- Any social posts, and their order.

Nothing here has been uploaded or posted anywhere.
