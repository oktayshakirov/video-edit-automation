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

## What this channel is

Read this before the steps, because it is what the steps are in service of.
**thecrypto.wiki's subject is an abstraction and its audience is sceptical.**
A whale, a fee, a score, a supply, a custodian - none of these has a
photograph, and every one of them has a confident wrong explanation already in
circulation. So the video's job is to show a *mechanism* and to be the version
that does not overclaim.

That has three consequences, and they are what separate this channel from
tinnitushelp.me rather than any difference in the run:

- **The pictures are drawn, not found.** Stock has no photograph of an
  abstraction, so a shot list built from footage drifts to mood every time -
  and has been rejected for exactly that. Beats carry the argument here.
- **The register is cool, not warm.** The viewer is deciding whether to trust
  you. Precision is the persuasion; enthusiasm reads as a pitch.
- **The sound is hard.** The full kit, the bitcrushed slam, the glitch. This
  is the genre's own punctuation and the channel keeps it.

## Read these, in this order

| Step | Read |
| --- | --- |
| **The run, every step** | **`docs/video/workflow.md`** - read it first, every run |
| Before writing a word | `docs/video/narration.md`, `docs/video/projects/crypto.md` |
| How the synthesiser behaves | `docs/video/voice.md` |
| The long form | `docs/video/longform.md` - shape, chapters, transitions, chrome |
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

**`workflow.md` is the procedure and it is not repeated here.** What follows is
only what is this channel's own - restating the shared steps is how the publish
sequence drifted into four copies that disagreed.

1. **Suggest, do not pick** - `python3 tools/topics.py crypto`.
2. **Script both together** from the chosen article.
3. **Decide what gets drawn, before writing a shot list.** This is the step
   that matters most here. Read the script's nouns back: most of them are
   abstractions, and **stock has no photograph of an abstraction**. List the
   beats first, and **budget a new beat when the library cannot draw the
   subject** - that is cheaper than a second stock fetch and reusable forever.
   The clips that remain are the *act*: a hand on a lit phone, a thumb on a
   feed, a carriage of people on screens - never a portrait of somebody
   feeling something.

   Three of the five full-width beats were built for this channel: **`chart`**
   is a line drawing itself with the turn marked, the trajectory `bars` could
   never show; **`timeline`** spaces dated events by their real distance in
   time rather than evenly like `steps`; **`map`** is regulation and domicile
   when *clustering* is the point, not merely when countries are named.
   `docs/video/footage.md` and `docs/video/beats.md`.
4. **Preflight, then build both** - `projects/crypto-long/<name>.py` and
   `projects/crypto-short/<name>.py`, each setting `SOURCE_POST`.
5. **Hand over, re-cut, and only then commit and hand off** - `workflow.md`
   steps 4 and 5.

## The line that outranks everything else

**No financial advice, ever.** A script describes a *mechanism* and never a
direction: it names no price level, predicts nothing, rates no platform, and
recommends buying or selling nothing. This is a YMYL niche and the constraint
is not negotiable by a good hook. Full detail in
`docs/video/projects/crypto.md`.

It reaches into the opener too. A verdict stamp here judges a *claim* - "this
is how people say it works, and it does not" - never an outcome, an asset or a
platform.

Also standing: **the picture has to say the noun the narration says** - and
when the noun is an abstraction, that means drawing it rather than searching
harder. A cut was rejected for exactly this; see step 3.
