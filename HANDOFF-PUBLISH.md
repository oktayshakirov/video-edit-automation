# Handoff → /publish-video

**Built:** `what-is-a-rug-pull` — a long-form 16:9 explainer and its vertical
Short, built as a pair (`/video-crypto`) for thecrypto.wiki.
**Source article:**
`crypto-wiki/content/posts/what-is-a-rug-pull.mdx`. The scripts carry
`URL = "https://thecrypto.wiki/posts/what-is-a-rug-pull"` (which is how
`tools/topics.py` derives coverage); there is no separate `SOURCE_POST`.
Scripts: `projects/crypto-long/rug-pull.py` and
`projects/crypto-short/rug-pull.py`.
**Date:** 2026-09-11
**Voice:** `mia` (`af_heart`) — the crypto explainer default, on both cuts.
**Music:** `night-drift`, the prepared track, on both cuts.
**Approved by the user** after three review rounds. The last two rounds are
listed under "What changed after review" — worth a glance, because an earlier
cut that was screenshotted looks different (different thumbnail, different
0:04 and 0:40 shots, water behind every beat).
**Committed:** `de65838` on `main`, pushed. Working tree clean.

---

## Files (Desktop)

| what | path |
| --- | --- |
| long video (16:9) | `/Users/oktayshakirov/Desktop/crypto-rug-pull-long.mp4` |
| long captions | `/Users/oktayshakirov/Desktop/crypto-rug-pull-long.srt` |
| long thumbnail (16:9) | `/Users/oktayshakirov/Desktop/crypto-rug-pull-long-thumb.jpg` |
| long metadata sidecar | `/Users/oktayshakirov/Desktop/crypto-rug-pull-long.md` |
| short video (9:16) | `/Users/oktayshakirov/Desktop/crypto-rug-pull-short.mp4` |
| short thumbnail (9:16) | `/Users/oktayshakirov/Desktop/crypto-rug-pull-short-thumb.jpg` |

- **Long:** 3:12 (192.68s), 1920x1080, h264/aac. Six chapters, first at 0:00,
  no chapter-rule violations reported in the sidecar.
- **Short:** 45.1s, 1080x1920, h264/aac. One thumbnail file (9:16), matching
  the long's — same `hacker.jpg` source, same headline.

The long's `.md` sidecar carries a **proposed** title, description, chapter
list and tags — a draft for `/publish-video`, not a decision. Proposed title:
"How to Spot a Crypto Rug Pull". The Short keeps its own curiosity title
(it opens by asking "How does a token crash to almost nothing the second the
hype dies?"); the long-form title is a different search-query angle, per
`docs/video/longform.md`.

## What it is

**Long — six chapters:**

1. **The vanishing act** — hook: you buy a token, it jumps, then it is worth
   nothing and the team is gone. `stat` on `2020`.
2. **What actually holds the price up?** — the reframe: a new token trades on
   a DEX against a pool of real money; that pool *is* the price and the only
   thing a holder can sell back into.
3. **How the trick actually works** — `diagram` "THE FOUR MOVES": seed a
   pool → market it → buyers pour in → pull the pool.
4. **Is it always the liquidity?** — `grid` "FIVE SHAPES OF A RUG PULL"
   (liquidity pull, team dump, hidden backdoor, honeypot, slow bleed).
5. **What if the pool is locked?** — the decoy: a real lock still lets a team
   that kept most of the supply bleed buyers out. `gauge` "WHO HOLDS THE
   SUPPLY?" — 70-80% vs a healthy spread at ~20%.
6. **So how do you check?** — `steps` "THE FOUR-QUESTION CHECK", the echo
   ("a rug pull is a design, and a design leaves fingerprints"), the
   disclaimer on its own line, the closing question.

**Short — one move:** a new token only has a price because the creators
paired it with a pool of real money; control that pool, control the price.
Then a `steps` "THREE-STEP CHECK" (is the liquidity locked / who holds the
supply / can the owner rewrite it), a `chapter` payoff card
"IF THEY CAN PULL THE POOL, THEY WILL.", and the close:
"the next time a coin is mooning on your feed — check who actually controls
its liquidity pool." **No disclaimer line** (long-form only, per
`docs/video/narration.md`).

## No financial advice

No token is named, no price level or direction is given, no platform is rated,
nothing is recommended to buy or sell — in either cut, including titles,
descriptions and thumbnails. The `diagram` draws the scam's mechanism; the
`gauge` draws a distribution; the abstract `CHART` graphic
(`assets/brand/graphics/`) names nothing tradeable (the site's own
`rugpull.jpg` is a real PancakeSwap screenshot and was not used). The
disclaimer line is spoken and on screen in the long form's outro.

## New brand assets committed with this

- `assets/brand/graphics/rug-pull-chart.png` (16:9) and
  `rug-pull-chart-vertical.png` (9:16) — the abstract price-to-zero chart.
- `assets/brand/beat-ground-crypto.jpg` — a warm near-black gradient passed to
  the drawn beats as `Shot(backdrop=)`, so `crypto-blackwater` (the brand
  default) is now reserved for the chapter cards. `docs/video/beats.md`
  records the pattern.

## What changed after review

**Round 2 (long form):**
- Thumbnail → the site's own `hacker.jpg` (hooded figure with a laptop),
  pinned crop, text on the dark left. Short thumbnail matches.
- 0:04 phone-over-rubble clip (read as a war zone) → the abstract `CHART`.
- Foreign banknotes → a US-dollar photo for "a pool of real money".
- 0:40 Instagram-reels clip → the `CHART` on the buy/sell line.
- `crypto-blackwater` was behind every graphic → now the chapter cards only;
  the five drawn beats sit on `beat-ground-crypto.jpg`; the title stamp and
  the disclaimer moved to a slow gold-dust clip.
- `grid` dropped its five card icons (smudges at five-up size).

**Round 3 (Short only):**
- Added the vertical `CHART` on "pull the money straight out" (0:13), which
  also replaced a fire-escape clip that cropped its subject.
- The flat `checklist` → an animated `steps` track with icon nodes.
- Closing line rewritten to "check who actually controls its liquidity pool".

## Undecided / notes for publish

- **Long-form title** in the sidecar ("How to Spot a Crypto Rug Pull") is a
  proposal. The Short has no separate title yet — needs one that keeps its
  curiosity-hook angle, distinct from the long's search query.
- The `hacker.jpg` source is 996px; it upscales acceptably at thumbnail size
  but check it at feed size before publishing.
- Everything about which file goes to which platform, the metadata pass, the
  `videos.json` entry and the social posts is `/publish-video`'s to decide —
  this handoff does not pre-empt it.

**Open a fresh session and run `/publish-video`.** Nothing here is posted,
scheduled, or entered into any registry.
