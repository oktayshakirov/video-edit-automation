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

**No long dashes, ever:** a single `-` in every title, description, tag and
caption you write. The picture is enforced in code - see
[design.md](../../../docs/video/design.md#only-a-hyphen-goes-on-screen).

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

1. **Suggest, do not pick** - `python3 tools/topics.py crypto`, crossed with
   `docs/video/demand/crypto.md`. Every candidate shows its demand evidence
   or says "no evidence" (`workflow.md` step 1). Look first for a **brand-new
   named term few videos answer yet** (E8, our only search win) and for a
   **named project people are unsure whether to trust** (the niche's biggest
   format). A mechanism with no demand of its own is bridged to what the
   viewer cares about - understanding a thing, not getting burned - never to
   profit. An article that already has a video can be **re-angled** when the
   map shows the subject wins on another promise. Once picked, a standout
   gets its **teardown** before the script (`demand/README.md`, "Teardown").
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
   `footage.md`, "When the subject is a real thing". **When the real thing
   is a page** - the explorer showing the transaction, the market's odds,
   the announcement - capture it with `screencap` and let the camera ring
   the line the voice reads (`footage.md`, "A real page"). **A photo that
   carries a line can move in depth** (`parallax=`, `isolate=`, `pop=`), or
   put its one word behind the person with the `behind` beat (`"fly"` or
   `"rise"`; a rise always takes a different background, `room=`). Money moving
   in or out of something is a `pile` (coins pour in; `drain` opens the
   floor). `beats.md` and `design.md` also have animated icons and per-shot
   GPU effects; `tools/visual_demo.py` renders every one of these to look at.

   **Write the picture first** (2026-11-12, `workflow.md`, "Write the
   picture first: the visual plan"). One line per sentence - what the
   viewer sees, and which tool draws it - before fetching anything. The
   editor rejected a cut that passed every gate with 6 of 25 shots drawn.
   Never two full-frame pictures in a row; at least half the long form's
   shots are drawn or framed (`window=`, `callout`, `spotlight`, a beat).
   `pile` and the other signature beats rest for two videos: use `breach`
   for many drained addresses, `airgap` for a signer kept offline, or
   build the beat the subject needs. **No `title_at=`** - the title slate
   is retired. `script_check` flags all of these.

   **These are required, not a menu** (`workflow.md`, "The toolbox is not
   optional"). The first pair after they landed used none of them and the
   editor asked whether the skill knew they existed (2026-11-06). Before
   writing the shot list, write down which slots take: a captured page, the
   site's photo of the named object with `behind` / `isolate` / `parallax`,
   a `pile` (or `breach`, or a new beat - see the rotation rule) where money
   moves, a shader on the turning shot. When Pexels has
   nothing on topic, these come before a second fetch. **No phone clip whose
   screen is a social feed** - a scrolling-phone search returns feeds, and
   four of them were cut as irrelevant (`footage.md`). **The disclaimer
   sits on this video's subject, never rain** (`stillclip`). `script_check`
   flags all three (`toolbox`, `feed-clip`, `disclaimer-bg`). A stock clip
   with a **blank lit screen** can carry the page the narration names
   (`core/screenfill.py`), and Wikimedia Commons has real objects Pexels
   lacks (a hardware wallet) - credit them unless CC0.

   **The Short ends on a plain sentence - no `outro=` card** (2026-11-06,
   `shorts.md`, "No outro card on a Short"). The closing line is the last
   entry in `SENTENCES`, captioned like the rest; the card slowed the end
   where viewers leave. `script_check` flags it (`short-outro`).
   **Write for the first eight seconds, then check them** (2026-11-10,
   `shorts.md`, "The first eight seconds"): the Short's spoken title
   question runs 10-13 words so sentence 2 starts near 4s, its render call
   passes `opener_holds=True`, it runs 30-40s (E17), and the long form
   2:30-3:00 (E18). At most half of either script's shots are plain stock;
   put a clip in a `window=` or draw the beat (`footage.md`). Run
   `tools/retention_check.py` on both scripts with the other gates and
   hand its output over.
4. **Preflight, then build both** - `projects/crypto-long/<name>.py` and
   `projects/crypto-short/<name>.py`, each setting `SOURCE_POST`.

   **Pick the cover style that fits the topic and the picture** - no
   style is forced (the editor, 2026-11-08). An arrow and a ring pointing
   at the named thing when the picture has one (`tokenized-stocks`: a
   Tesla wordmark, `thumb.arrow_layer` / `ring_layer`, drawn at 4x so they
   are clean); the picture and the headline alone when it already says it;
   a drawn beat when there is no photograph. A second version is fine when
   the choice is close - show both. **Set `COVER_STYLE`** (`"text"`,
   `"arrow"`, `"beat"`) next to `DEMAND` in both scripts, so the views
   audit can compare views and clicks by style; `script_check` flags it
   missing. `docs/video/thumbnails.md`, "Cover styles are a choice, and
   every video says which".
5. **Hand over, re-cut, and only then commit and hand off** - `workflow.md`
   steps 4 and 5. Before a re-cut, measure the draft against the channel's
   best-performing recent pair (words, sentences, holds, roster) - that is
   what found the `market-cap` gaps.
6. **Leave the skill better.** Record every lesson the run produced in the
   narrowest doc, a few lines each, in the same commit. Short and specific
   beats long and general.

## What every build draws by default

On without asking, and listed once in `docs/video/workflow.md`, "What
every article build draws by default". Read it before writing: two of its
items are the script's job - a `Section(kicker=)` on every carded section,
and a real "But" or "Actually" where a sentence turns.

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
