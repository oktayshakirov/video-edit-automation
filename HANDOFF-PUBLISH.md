**This file holds two approved pairs, neither published yet:** `decentralized-ai` (thecrypto.wiki, first section) and `forest-chorus-box-breathing` (tinnitushelp.me, second section below). Publish them as two separate runs.

# Handoff: decentralized-ai (long + Short)

Approved by the user 2026-10-16. Channel: thecrypto.wiki. Voice `mia`, music
`night-drift`. Source article slug:
`decentralized-ai-can-ai-run-on-the-blockchain`
(https://thecrypto.wiki/posts/decentralized-ai-can-ai-run-on-the-blockchain).
Build commit `4a3c7d3` on `main`, **not pushed**. **Nothing has been
published yet.**

## Files

| What | Path |
| --- | --- |
| Long form (3:39) | `/Users/oktayshakirov/Desktop/decentralized-ai-long.mp4` |
| Long thumbnail | `/Users/oktayshakirov/Desktop/decentralized-ai-long-thumb.jpg` |
| Long captions | `/Users/oktayshakirov/Desktop/decentralized-ai-long.srt` |
| Long sidecar (title, description, chapters, tags, credits) | `/Users/oktayshakirov/Desktop/decentralized-ai-long.md` |
| Short (47s) | `/Users/oktayshakirov/Desktop/decentralized-ai-short.mp4` |
| Short cover | `/Users/oktayshakirov/Desktop/decentralized-ai-short-thumb.jpg` |

Scripts: `projects/crypto-long/decentralized-ai.py`,
`projects/crypto-short/decentralized-ai.py`.

## Titles

- Long: **Can AI Run on the Blockchain? Decentralized AI Explained** (in the
  sidecar). A search query, the article's own title plus the phrase people
  type.
- Short: **What Does a Blockchain Actually Do for AI?** - its opening line,
  word for word. A different query angle from the long form on purpose. The
  Short has no sidecar; write its caption from the script, keeping: the chain
  does not do the thinking, thousands of computers repeat every step, one
  word of a mid-sized model would fill hundreds of blocks, and the one job
  the chain does is checking a proof. Link the article.

## Openers (tag for the fortnightly review)

- Long: redacted hook `One word from an AI fills [hundreds] of blocks`,
  revealed in **sentence 1** at ~2s (the first long form to do that).
- Short: redacted hook `The blockchain does [one job] for AI`. Sentence 2 is
  "Not the thinking. One job the AI cannot do for itself." - it overturns
  the assumption and names only the *kind* of answer.
- Short close: cold, outro card "The blockchain does not run the AI. It
  [checks] it." No disclaimer in the Short; the long form speaks it and
  shows it on screen.

## No financial advice, and what the copy must not add

Both videos describe how computation is priced and checked. They name no
token, no project, no platform and no price, and predict nothing. Keep the
descriptions the same: do not name "AI coins" or decentralized-AI projects,
and do not turn the outlook into a forecast. The article's two case studies
(an unnamed trading agent with a return figure, a DAO moderation system)
were left out of both videos as unverifiable; leave them out of the copy too.

## Figures, in case a comment asks

From the article: a 7-billion-parameter model, proof checks at 200,000 to
1.5 million gas, verification in under a second, 12-second Ethereum blocks,
storing weights on-chain costing millions. Arithmetic from the EVM price
list: one token is ~7 billion multiply-adds, MUL 5 gas + ADD 3 gas, so 56
billion gas at the cheapest. Mainnet's block gas limit is 60 million
(October 2026, with ~200 million tested on Sepolia), so "hundreds of blocks"
holds either way (933 today, ~280 at 200M). "One word" means one token,
which the long description already says.

## Credits

Footage is Pexels only (no attribution required); music night-drift. No
CC BY-SA material in either video. The long sidecar's Credits block is
complete.

## Still undecided

Nothing. Both thumbnails are the new `replicate` beat drawn as a still, on
black, with the long form's headline - a concept video, so no face, per
`thumbnails.md`.


---

# Handoff: Forest Chorus + Box Breathing session pair

**Built:** `forest-chorus-box-breathing`, a tinnitushelp.me sound-therapy
session: long form (20 min) **and its own vertical Short** (Mode 2, not an
article pair).
**Source article:** none. Off-site topic, `SOURCE_POST = None`.
**Date:** 2026-10-15
**Voice:** `luna`, the session default. Still `candidate`.
**Approved by the user** on the first cut, no re-cuts. Build commit `b0a25cc`
on `main`, **not pushed**.

## Files (all on the Desktop)

### Long form (YouTube)

| what | path |
| --- | --- |
| video (16:9) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (20 Minutes).mp4` |
| thumbnail (1280x720) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (20 Minutes).jpg` |
| build script | `projects/tinnitus-long/forest-chorus-box-breathing-20min.py` |

Runtime **exactly 20:00** (1200.0s, ffprobe-checked). 1920x1080, h264/aac,
-19.6 LUFS integrated.

### Short (YouTube Shorts / Instagram Reel / Facebook Reel / TikTok)

| what | path |
| --- | --- |
| video (9:16) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (Short).mp4` |
| thumbnail (1080x1920) | `/Users/oktayshakirov/Desktop/Forest Chorus + Box Breathing for Tinnitus (Short).jpg` |
| build script | `projects/tinnitus-short/forest-chorus-box-breathing-short.py` |

Runtime **55.6s**, 1080x1920, h264/aac, -19.6 LUFS. Same recording, pattern
and picture as the long form, 2 cycles of box breathing (32s breathing block).

Neither file has an SRT or a `.md` metadata sidecar, same precedent as every
prior session build. Title and description material below is raw material,
not pre-written copy.

## What this is

A real nature recording, **a forest chorus**, tiled from ten minutes to
twenty. Source file: `~/Desktop/NaturesChorus.wav` (the file the user attached
this session; keep it on the Desktop, both scripts read it by that path). The
narration calls it "a forest chorus" and never names species, so neither
should the description.

**Box breathing** (in 4s, hold 4s, out 4s, hold 4s), the first session on the
channel with that pattern. Earlier sessions were all 4-in/6-out or 4-7-8. The
intro instructions are new too: bring the sound up from low until the
tinnitus starts to blend in, and "if a hold feels like too much, let it go
and just breathe".

**The picture** is misty jungle-canopy footage, graded dark, with a few
fireflies (the `canopy-fog` look the user picked in the 2026-10-15 test
round). It is **stock footage, so it needs a credit**: Pexels video 19366762
by Florian Delee,
https://www.pexels.com/video/fog-tropic-jungle-latin-america-19366762/
(Pexels licence; attribution is optional, follow the channel's usual stock-credit practice).

**The Short ends on "If this helped, save it for the next time you need
it."** and nothing after it, per the session-Short rule. The long form's outro
invites another round.

## Things the publish step needs to know

**The audio's source and licence are not recorded.** The user supplied
`NaturesChorus.wav` and its origin was not discussed in the build session.
**Ask the user where it came from before writing the description's credits**,
and before uploading to any platform that does content-ID matching. Do not
guess an attribution.

**Copy angle: partial masking.** Set the sound so the tinnitus still faintly
shows underneath, which is the channel's angle
(`brown-noise-vs-white-noise-for-tinnitus.mdx` argues against burying it).
`band_energy` puts about 95% of the recording between 4 and 8 kHz (4-8 kHz
93-96%, everything else under 4% per band), which is why the instruction is
used. **Still make no claim about what it does for tinnitus**: it is a sound
to listen to, not a treatment. Never say it relieves, improves or cures
anything, and do not turn the measurement into a promise like "covers
high-pitched ringing". Same for box breathing: describe it as something
people do, not as a treatment.

The standard red-flag line fits the long-form description: "If your tinnitus
lasts more than a few weeks, is getting louder, is in one ear only, pulses
with your heartbeat, or comes with dizziness or hearing loss, see a doctor."

No em dashes in any published copy (titles, descriptions, tags).

## Distribution

Long form to YouTube only. Short to the full table (YouTube Shorts, IG Reel,
FB Reel, TikTok). The Short's save ending is written for the platforms that
never get the long version.

## Not done, and deliberately left to `/publish-video`

- The YouTube uploads, the Reel workflows, the TikTok draft and the Facebook
  upload.
- The `videos.json` registry entry on the site.
- Any social posts, and their order.
- Pushing `main`. The build commit is local only.

Nothing has been uploaded or posted anywhere.
