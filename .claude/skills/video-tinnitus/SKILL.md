---
name: video-tinnitus
description: Build tinnitushelp.me videos - either an article explainer as a long-form 16:9 plus its vertical Short in one run, or a sound-therapy session with a generated noise bed and breathing ring. Use when the user runs /video-tinnitus, asks for a tinnitus video, Short or Reel, wants a post from tinnitushelp.me turned into a video, or wants a masking, notched-audio or zen sound-therapy piece. Builds only; publishing is /publish-video. For crypto use video-crypto, for drone footage use video-drone.
---

# Tinnitus videos

**Two products that share an engine.** Ask which one before anything else:

- **Article explainer** - a long-form 16:9 and its vertical Short, built as a
  pair from one tinnitushelp.me post. The default.
- **Sound-therapy session** - a generated noise bed, a seamless picture loop and
  a breathing ring. No article, its own copy rules, and it lands on `/zen`.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with
`PYTHONPATH=.`. **Source site:** `~/Coding/tinnitus-blog`.

**No long dashes, ever:** a single `-` in every title, description, tag and
caption you write. The picture is enforced in code - see
[design.md](../../../docs/video/design.md#only-a-hyphen-goes-on-screen).

## What this channel is

Read this before the steps, because it is what the steps are in service of.
**tinnitushelp.me's subject is invisible and its audience is distressed.**
There is no photograph of a phantom sound, of gain, of habituation or of a
spike, and a meaningful share of the people watching found the video at two in
the morning because they are frightened. The job is to be the calm, honest
thing they find.

That has four consequences, and they are what separate this channel from
thecrypto.wiki rather than any difference in the run:

- **The pictures are drawn, and the subject has to be drawn too.** Measured:
  `airpods-and-tinnitus` ran 37 clips against 1 site image, and footage drifts
  to mood - somebody tired, somebody holding their head - every time.
- **The register is warm and plain.** Certainty is the harm here, where on the
  crypto channel precision is the product.
- **The sound is soft after the first second.** The body kit has no slam and
  no glitch, at 0.72 of the crypto levels, because hyperacusis is common in
  this audience. **The opener is the exception and keeps its full kit** - a
  Short nobody stays for is a Short nobody hears the soft middle of. This is
  automatic; no script passes it.
- **No ear close-ups, in either format.** Standing rule.

## Read these, in this order

| Step | Read |
| --- | --- |
| **Before anything** | `docs/video/projects/tinnitus.md` - which product, the voice roster, and the medical limits |
| **The run, every step** | **`docs/video/workflow.md`** - read it first, every run |
| Before writing a word | `docs/video/narration.md` |
| How the synthesiser behaves | `docs/video/voice.md` |
| The long form | `docs/video/longform.md` - shape, chapters, transitions, chrome |
| The Short | `docs/video/shorts.md` |
| Drawn graphics | `docs/video/beats.md` |
| Choosing and screening footage | `docs/video/footage.md` |
| Type and layout on screen | `docs/video/design.md` |
| Music and sound | `docs/video/audio.md` - the softer body kit is automatic; **the opener keeps its slam** |
| A session's bed and loop | `docs/video/projects/tinnitus.md` |
| Both thumbnails | `docs/video/thumbnails.md` |
| Something rendered wrong | `docs/video/troubleshooting.md` |

Do not work from memory of these rules. They are edited as the engine changes,
and a remembered version is a stale one.

## The run

**`workflow.md` is the procedure and it is not repeated here** - including
preflight, which is its step 3. What follows is only what is this channel's
own; restating the shared steps is how the publish sequence drifted into four
copies that disagreed with each other.

1. **Ask which product** - explainer pair, or session. A session has no article,
   skips topic suggestion, and takes the session copy rules in the project doc.
2. **Read what worked, then suggest - do not pick.** First
   `.claude/skills/video-performance-review/videos.md`, "What works, and
   what does not". Then `python3 tools/topics.py tinnitus`, crossed with
   `docs/video/demand/tinnitus.md`; every candidate shows its demand
   evidence or says "no evidence". The bridge matters most on this
   channel: our articles explain mechanisms (gain, habituation, somatic
   tinnitus) and sufferers search outcomes (sleep, spikes, "will it go
   away"). Name the outcome as the subject; promise understanding, never
   relief. A format that sells a result is closed here, however well it
   does elsewhere. An article that already has a video can be re-angled.
   Once picked, a standout gets its teardown before the script.
3. **Script both together** from the chosen article, in `mia` (the `noah`
   test ended with pair 5; sessions keep `luna`). A verdict stamp judges a
   *claim*, never an outcome or anybody's prognosis. The Short's spoken
   title question runs 10-13 words so sentence 2 - a body-check when the
   article has one - starts near 4s; its last line runs back into the
   title question; it ends on a plain sentence. The long form runs
   2:30-3:00. Sessions are exempt from all of this.
4. **Write the picture first** - the step that matters most here, because
   the subject cannot be photographed at all. Follow `workflow.md`, "Write
   the picture first: the visual plan": one line per sentence saying what
   the listener sees and which tool draws it, before fetching footage.
   - **Draw the mechanism:** `diagram(loop=True)` for the night loop,
     `spectrum` for the notch our own audio cuts, `audiogram`, `gauge` for
     decibels against safe exposure, `dial` for a scale. **Build a new beat
     when the library cannot draw the subject.**
   - **Show the real thing** the script names (a product, a study's page
     with `screencap` in `window="browser"`, a named musician), credited.
   - **Frame what is left:** `callout` or `spotlight` on a photo, a clip in
     a `window=`. Never two full-frame pictures in a row; at least half the
     long form drawn or framed; signature beats rest for two videos.
   - **Do not reach for `anatomy`** unless there is a real picture where
     the parts are visible (`tmj-and-tinnitus` is the bar).
   - Clips show an *act* (headphones going in, a hand on a volume control),
     never a portrait of suffering, never an ear close-up, never a social
     feed. The disclaimer sits on this video's own subject. No `title_at=`.
5. **Check, preflight, build** - `projects/tinnitus-long/<name>.py` and
   `projects/tinnitus-short/<name>.py`, each with `SOURCE_POST` (`None` for
   a session), `DEMAND` and `COVER_STYLE`. Run `tools/script_check.py`,
   `tools/opening_check.py` and `tools/retention_check.py` before fetching
   or rendering, fix every flag, and hand their output over.
6. **Hand over, re-cut, and only then commit and hand off** - `workflow.md`
   steps 4 and 5, which now include logging the pair with
   `tools/video_log.py`.
7. **Leave the skill better - every run.** `workflow.md`, "Every run leaves
   the skill better": each note the editor gave becomes a dated rule in
   the narrowest doc, a check when it can be checked, and an entry in
   `video-performance-review/changes.md` when a listener could notice it.
   Replace old rules, do not stack them. Tell the editor what was learned
   and where it went.

## What every build draws by default

On without asking, and listed once in `docs/video/workflow.md`, "What
every article build draws by default". Read it before writing: two of its
items are the script's job - a `Section(kicker=)` on every carded section,
and a real "But" or "Actually" where a sentence turns.

## The line that outranks everything else

**Nothing here diagnoses, and nothing here promises relief.** This is a health
audience, much of it distressed, and a confident sentence about a cure does
real harm. The full statement of that rule, and what it means for a hook, is in
`docs/video/projects/tinnitus.md` - read it before writing, not after a re-cut.

Also standing: **no ear close-ups, in either format** - and **the picture has
to say the noun the narration says**, which on a channel whose subject cannot
be photographed means drawing it rather than searching harder. See step 4.
