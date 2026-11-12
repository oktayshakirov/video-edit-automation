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

1. **Read what worked, then suggest - do not pick.** First
   `.claude/skills/video-performance-review/videos.md`, "What works, and
   what does not". Then `python3 tools/topics.py crypto`, crossed with
   `docs/video/demand/crypto.md`. Every candidate shows its demand evidence
   or says "no evidence". Look first for a **brand-new named term few
   videos answer yet** (our only search win) and for a **named project
   people are unsure whether to trust** (the niche's biggest format). A
   mechanism with no demand of its own is bridged to what the viewer cares
   about - understanding a thing, not getting burned - never to profit. An
   article that already has a video can be re-angled. Once picked, a
   standout gets its teardown before the script (`demand/README.md`).
2. **Script both together** from the chosen article, in `mia` (the `noah`
   test ended 2026-11-12). The Short's spoken title question runs 10-13
   words so sentence 2 starts near 4s; it runs 30-40s and ends on a plain
   sentence. The long form runs 2:30-3:00.
3. **Write the picture first** - the step that matters most here, because
   most of this channel's nouns are abstractions and stock has no
   photograph of one. Follow `workflow.md`, "Write the picture first: the
   visual plan": one line per sentence saying what the viewer sees and
   which tool draws it, *before* fetching footage. The table there maps a
   sentence to its tool. In short:
   - **Draw the mechanism.** A beat from `beats.md`, or **a new beat when
     the library cannot draw the subject** - that is part of the run.
   - **Show the real thing** when the subject is named: the owner's own
     pictures, a Commons photo (credited), and **the real page** captured
     with `screencap` in `window="browser"`. Never a token logo you cannot
     tie to its contract.
   - **Frame what is left.** A photo gets `callout` or `spotlight`; a clip
     goes in a `window=`. Never two full-frame pictures in a row, and at
     least half the long form drawn or framed.
   - **Rotate.** A signature beat (`pile`, `behind`, `blindsign`...) rests
     for two videos.
   - Clips show an *act*, never a portrait of a feeling, never a social
     feed. Watch a clip's whole used span for unrelated text. The
     disclaimer sits on this video's own subject. No `title_at=`.
4. **Check, preflight, build both** - `projects/crypto-long/<name>.py` and
   `projects/crypto-short/<name>.py`, each with `SOURCE_POST`, `DEMAND` and
   `COVER_STYLE`. Run `tools/script_check.py`, `tools/opening_check.py` and
   `tools/retention_check.py` on both **before fetching or rendering** and
   fix every flag; hand their output over. Covers: `thumbnails.md` - the
   style that fits the picture, six words or fewer on two rows, the accent
   on the subject's word.
5. **Hand over, re-cut, and only then commit and hand off** - `workflow.md`
   steps 4 and 5, which now include logging the pair with
   `tools/video_log.py`.
6. **Leave the skill better - every run.** `workflow.md`, "Every run leaves
   the skill better": each note the editor gave becomes a dated rule in
   the narrowest doc, a check in `script_check` when it can be checked,
   and an entry in `video-performance-review/changes.md` when a viewer
   could notice it. Replace old rules, do not stack them. Tell the editor
   what was learned and where it went.

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
