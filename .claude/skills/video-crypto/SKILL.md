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
   **Voice: check the `noah` test table first** (`projects/crypto.md`,
   *Voice test*). Until it has 5 rows, the pair reads in `noah` (male,
   `voice="noah"` on both builders) and gets a row; after that, `mia`
   (female, the default). One voice for the whole pair. `noah` reads ~6%
   slower, so size the script to its pace.
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

   **When the subject is a real, named thing, its real pictures come
   first.** A game, an app, a company, a coin: pull the owner's official
   art, screenshots and logo (its press or official site), put them under
   the lines that name it with `Shot(image=)` and over the remaining stock
   with `Shot(inset=)`, and use its key art for the thumbnail. All-stock
   about a real game was rejected as monotone (2026-10-20). Never a token
   logo you cannot tie to the right contract - draw a `ticker_card`.
   `footage.md`, "When the subject is a real thing".
4. **Preflight, then build both** - `projects/crypto-long/<name>.py` and
   `projects/crypto-short/<name>.py`, each setting `SOURCE_POST`.
5. **Hand over, re-cut, and only then commit and hand off** - `workflow.md`
   steps 4 and 5. Before a re-cut, measure the draft against the channel's
   best-performing recent pair (words, sentences, holds, roster) - that is
   what found the `market-cap` gaps.
6. **Leave the skill better.** Record every lesson the run produced in the
   narrowest doc, a few lines each, in the same commit. Short and specific
   beats long and general.

## What every build draws by default (2026-10-21)

These are on without asking - a script only supplies the words. Detail in
`docs/video/longform.md` and `docs/video/audio.md`.

- **Chapter cards are the band card**, long form and Short: the title typed
  into a band of the brand colour on key clicks, the riser into it and the
  cinematic flashback out of it. **Write a `Section(kicker=)` for every
  carded section** - two or three words naming the stake ("THE REJECTION",
  "THE CATCH"). Without one the long form shows "CHAPTER n" and a Short
  shows no label.
- **The opening title is the cinematic card** (`title_at=`), on the title
  intro sound. Keep its hold clear of the first chapter card.
- **A disclaimer `payload` becomes the notice card** on the notification
  chime - no flag needed.
- **The video ends on the band end card** - THANKS FOR WATCHING, retyped as
  LIKE & COMMENT - **and switches off like a TV.** `endcard=` turns the card
  on; the TV-off is always there.
- **The old-film surface is arranged, not blanketed** (`core/filmfx.py`):
  the first shot clean, a section's first clip full, the rest rotating
  grain-only / clean / dust-only / full, nothing on drawn beats. `film=False`
  turns it off for one video, a number scales it.
- **A few cuts become glitch or TV static on their own**
  (`transitions.plan_special`): a glitch into a sentence that turns ("But…"),
  static or glitch alternating into chapter cards, static on a jump in time -
  about one per 45 seconds. **Open a turning sentence with "But" or
  "Actually" when it really turns**; that is what places the glitch. A
  transition set by hand on a shot always wins.
- **`reel` is the beat for a sequence the viewer should feel move** - days,
  versions, dates, steps: a strip of cards (clips, photos or text) the camera
  travels along, one card per sentence (a Short: one phrase per card, ~2s
  each). It can **dive into its last card and continue as that clip**, or
  open out of the previous clip (`enter` / `emerge`) - use it where the
  script moves from an overview into one example. `docs/video/beats.md`.
- **`post` puts what someone actually wrote on screen** - a post, a news
  headline, a transaction - and highlights the `[bracketed]` line as it is
  read. Real, sourced wording only; write its sentence as two phrases, the
  lead-in and the quote. `docs/video/beats.md`, "`post`".
- **`emphasis=[...]` punches the word a sentence hinges on onto the screen**
  as it is spoken, long form only, once or twice a minute. Pick one word or
  short phrase per minute that the whole sentence turns on.
- **`spotlight` directs a still**: the camera glides into the part of a
  photo the voice names (a line of a document, one face), one region per
  sentence; the ring snaps to the content, so regions can be rough.
  `docs/video/beats.md`, "`spotlight`".
- **Footage of a place gets a quiet bed of it** (city, rain, office,
  servers) automatically, only on clips of 3s or more - nothing to write.
  Pick clips whose folder names the place when the sound would help.
- **The title and chapter sounds are files** in `assets/brand/sfx/`, kept out
  of git. On a machine without them the build falls back to synthesized
  stand-ins - copy them over before a build that ships.

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
