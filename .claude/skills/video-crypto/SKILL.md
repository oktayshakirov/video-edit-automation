---
name: video-crypto
description: Build a long-form YouTube explainer and its vertical Short together from a thecrypto.wiki article - topic suggestions, script, voiceover, drawn data beats, thumbnails, an SRT and a metadata sidecar. Use when the user runs /video-crypto, asks for a crypto video, Short or Reel, or wants a post from thecrypto.wiki turned into a video. Builds only; publishing is /publish-video. For tinnitus use video-tinnitus, for drone footage use video-drone.
---

# Crypto videos

**One article, two videos, one run.** A long-form 16:9 explainer and a vertical
Short are built as a pair from the same thecrypto.wiki post, because writing
them together is what stops the Short from being a trailer for the long one.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with
`PYTHONPATH=.`. **Source site:** `~/Coding/crypto-wiki`.

## Read these, in this order

The steps live in `docs/video/workflow.md` - read it first, every run. Then read
only what this build touches:

| Step | Read |
| --- | --- |
| Before writing a word | `docs/video/narration.md`, `docs/video/projects/crypto.md` |
| How the synthesiser behaves | `docs/video/voice.md` |
| The long form | `docs/video/longform.md` |
| The Short | `docs/video/shorts.md` |
| Drawn graphics | `docs/video/beats.md` |
| Choosing and screening footage | `docs/video/footage.md` |
| Type and layout on screen | `docs/video/design.md` |
| Music and sound | `docs/video/audio.md` |
| Both thumbnails | `docs/video/thumbnails.md` |
| Something rendered wrong | `docs/video/troubleshooting.md` |

Do not work from memory of these rules. They are edited as the engine changes,
and a remembered version is a stale one.

## The run

1. **Suggest, do not pick.** `python3 tools/topics.py crypto`. Offer three to
   five candidates with a reason each, then stop and wait for the user to
   choose. An off-site topic is fine when asked for and never offered.
2. **Script both together** from the chosen article.
3. **Decide what gets drawn, before writing a shot list.** Read the script's
   nouns back. Most topics here are abstractions - a number, a score, a
   supply, a fee - and **stock has no photograph of an abstraction**, so a
   shot list built from footage drifts to mood every time and gets rejected
   for it. List the beats first, and **budget a new beat when the library
   cannot draw the subject** - that is cheaper than a second stock fetch and
   reusable forever. The clips that remain are the *act*: a hand on a lit
   phone, a thumb on a feed, a carriage of people on screens - not a
   portrait of somebody feeling something. `docs/video/footage.md`.
4. **Build both** - `projects/crypto-long/<name>.py` and
   `projects/crypto-short/<name>.py`, each setting `SOURCE_POST`.
5. **Hand over and wait.** Re-cut as many times as the user asks; that loop is
   the normal case.
6. **On approval: commit, write `HANDOFF-PUBLISH.md`, and tell the user to open
   a fresh session for `/publish-video`.**

## This skill does not publish

Everything about getting a render out - which file goes to which platform, the
metadata pass, the site registry entry, the social posts and their order - is
`/publish-video`'s, and it is the only copy. That sequence used to be duplicated
into every build skill; the copies drifted, disagreed about what a Short gets,
and cost a registry entry that had to be reverted and a social post that could
not be un-sent.

Do not describe upload steps, pre-empt them, or re-derive them from memory.

## The line that outranks everything else

**No financial advice, ever.** A script describes a *mechanism* and never a
direction: it names no price level, predicts nothing, rates no platform, and
recommends buying or selling nothing. This is a YMYL niche and the constraint is
not negotiable by a good hook. Full detail in `docs/video/projects/crypto.md`.

Also standing: **the picture has to say the noun the narration says** - and
when the noun is an abstraction, that means drawing it rather than searching
harder. A cut was rejected for exactly this; see step 3.
