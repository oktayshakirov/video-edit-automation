# Handoff → /publish-video

**Built:** `vitalik-ethereum` — a thecrypto.wiki **long form + Short pair**, one
article at two angles.
**Source article:** `crypto-ogs/vitalik-buterin` (`SOURCE_POST` is set in both
project files).
**Date:** 2026-09-06
**Voice:** `otis` (`am_puck`, ENERGETIC chain, speed 1.00) — the male article
reader, used on both. Still `candidate`, not approved.
**Approved by the user** after three review passes.

---

## Files (all on the Desktop)

### Long form (YouTube)
| what | path |
| --- | --- |
| video (16:9) | `/Users/oktayshakirov/Desktop/crypto-vitalik-ethereum-long.mp4` |
| thumbnail (16:9) | `/Users/oktayshakirov/Desktop/crypto-vitalik-ethereum-long-thumb.jpg` |
| captions | `/Users/oktayshakirov/Desktop/crypto-vitalik-ethereum-long.srt` |
| **metadata sidecar** | `/Users/oktayshakirov/Desktop/crypto-vitalik-ethereum-long.md` |

**3:52.6** (232.61s), 1920x1080, h264/aac, 160 MB.

**Read the `.md` sidecar for the title, description, tags and chapter list —
they are already written. Do not re-derive them.** Title is
`Why Was Ethereum Created?`, a search query rather than the Short's hook.

Chapters (also in the sidecar, and they drive the site transcript page):

```
0:00 It started as a complaint about Bitcoin
0:35 A calculator, or a computer?
1:24 So what did that make possible?
2:00 So who is in charge?
2:33 How does a change actually happen?
3:19 So what did he actually build?
```

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)
| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/crypto-vitalik-ethereum-short.mp4` |
| thumbnail (9:16) | `/Users/oktayshakirov/Desktop/crypto-vitalik-ethereum-short-thumb.jpg` |

**48.7s**, 1080x1920, h264/aac, 29 MB. No SRT and no `.md` sidecar — the Short
burns its own captions, as every article Short on this channel does.

Working title, and it is deliberately **not** the long form's: *Who Is In
Charge Of Ethereum?* The two are on separate search angles so they are not
competing for one results page.

## What the pair says

The long form asks **why Ethereum exists at all** — a nineteen-year-old wanted
Bitcoin to run any program, the Bitcoin developers turned him down, so he built
a programmable network and then built it so nobody, himself included, runs it.
The Short takes only the governance half and does that one move: the founder
cannot change the rules, reverse a payment, freeze a wallet or switch it off,
and nobody else can either.

**No financial advice anywhere in either file** — design and governance history
only. No price, no prediction, no platform rated. The long form speaks and
displays the compliance line at 3:42; the Short carries none, which is this
channel's deliberate asymmetry for article Shorts.

## ⚠️ Attribution is required in the description — this is a licence condition

Both files use Creative Commons images. `Meta.credits` already carries the block
and it is inside the sidecar's description; **keep it there on upload.**

> Photographs of Vitalik Buterin by John Phillips / TechCrunch, CC BY 2.0, via
> Wikimedia Commons (TechCrunch Disrupt London 2015).
> Ethereum mark by the Ethereum Foundation, CC BY 3.0, via Wikimedia Commons
> (recoloured). Ethereum Classic mark: CC0.

CC BY is attribution-only, **not** share-alike, so neither video is forced under
a copyleft licence — unlike the Ruja pair. Full detail in
`assets/crypto/vitalik-buterin/CREDITS.md`. The Short uses the same portraits
and the same two marks, so the same block belongs on its description wherever a
platform has room for one.

## Undecided / for the publish session to call

- **The Short's title.** *Who Is In Charge Of Ethereum?* is what the script
  opens by asking, but it has not been chosen against anything.
- **Which surfaces the Short goes to.** No decision was taken in this session.
- **The long-form thumbnail trips the layout scorer** (`busiest-case score
  1.95`) because the TechCrunch step-and-repeat behind him has no quiet patch.
  It was looked at and judged fine — the type sits on the darkened right half
  and reads cleanly at feed size. Not a problem to re-fix, just don't be
  surprised by the warning if anything is re-rendered.

## Assets added by this build

`assets/crypto/vitalik-buterin/` is new — three crops of one 2015 TechCrunch
press shoot, the site's own studio photo promoted to frame size, the site's
Bitcoin neon photo cropped to 16:9, and the Ethereum / Ethereum Classic marks
recoloured to the brand palette. `CREDITS.md` in that folder is the source of
truth for every licence line above.

Twenty stock clips were fetched fresh and are recorded in
`assets/stock/manifest.json` (the bytes are gitignored; the manifest is what
makes the build reproducible).

## Docs changed by this build

Three review passes produced four rule changes, each written once in the doc
that owns it, per `docs/video/README.md`:

- `longform.md` — **reversed** "every clip carries a payload line". Labelling
  every clip put a statement on almost every frame and the user's verdict was
  "too many titles after each other". A payload now only survives where it adds
  something the narration does not say; this cut ships four in 3:52.
- `footage.md` — a portrait or square photograph must never fill a 16:9 frame
  (it becomes a band across the face); the picture must name the noun in *its
  own* sentence, not the next one; a brand-recoloured official logo is a
  legitimate asset. Also narrowed the old "label your video clips" section to
  match the reversal above.
- `shorts.md` — set `aspect` to the source's own ratio to show a photograph
  whole; an emoji caption silently switches per-word karaoke off for that line,
  and karaoke wins.
- `beats.md` — an all-struck checklist still needs a question for a title;
  a noun phrase over one reads as a double negative.
- `voice.md` — `live` is the heteronym a tech explainer actually hits: "went
  live" phonemizes as the verb.

## Repo state

Everything is committed and pushed to `origin/main`. Project files:

- `projects/crypto-long/vitalik-ethereum.py`
- `projects/crypto-short/vitalik-ethereum.py`

Working tree clean. Open a fresh session and run `/publish-video`.
