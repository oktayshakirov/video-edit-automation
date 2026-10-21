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
2. **Suggest, do not pick** - `python3 tools/topics.py tinnitus`.
3. **Script both together** from the chosen article. On the opener,
   `workflow.md` says to pick deliberately and this channel sets the limit: a
   verdict stamp is about a *claim*, never about an outcome and never about
   anybody's prognosis.
4. **Decide what gets drawn, before writing a shot list.** The step that
   matters most here, because the subject cannot be photographed at all. List
   the beats first and raise the graphic share. `diagram(loop=True)` is the
   night loop this site's articles keep describing, `gauge` is decibels
   against safe exposure, `dial` is a severity or loudness scale. **Budget a
   new beat when the library cannot draw the subject.** The clips that remain
   are the *act* - headphones going in, a hand on a volume control, somebody
   at a window - never a portrait of somebody suffering.

   **`spectrum`** is the beat built for this channel: it draws the notch
   `core/soundbed.py` actually cuts, so reach for it before describing this
   site's own audio over a photograph. `timeline` and `chart` are available
   too. `docs/video/footage.md`, `docs/video/beats.md` and
   `docs/video/projects/tinnitus.md`.

   **Do not reach for `anatomy`.** It needs a real, accurate picture of the
   part being named, and one rarely exists for this channel's subjects - the
   drawn fallback it used to carry was tried four times and cut. It stays in
   the library for `tmj-and-tinnitus`, which has a head in profile worth
   pointing at, and that is the bar: a picture where the parts are genuinely
   visible. Without one, say it in the narration and put a `clip` or a
   `diagram` under it.

   **When the script names a real thing, show the real thing.** A product
   (AirPods, a hearing aid, an app), a study's institution, a named musician:
   pull its official press images or logo, put them under the line that names
   it (`Shot(image=)`) or over the stock (`Shot(inset=)`), and credit them in
   the description. All-stock about a real subject was rejected on the crypto
   channel as monotone (2026-10-20). `footage.md`, "When the subject is a
   real thing".
5. **Preflight, then build** - `projects/tinnitus-long/<name>.py` and
   `projects/tinnitus-short/<name>.py`, each setting `SOURCE_POST` (`None` for
   a session).
6. **Hand over, re-cut, and only then commit and hand off** - `workflow.md`
   steps 4 and 5.

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
- **The title and chapter sounds are files** in `assets/brand/sfx/`, kept out
  of git. On a machine without them the build falls back to synthesized
  stand-ins - copy them over before a build that ships.

## The line that outranks everything else

**Nothing here diagnoses, and nothing here promises relief.** This is a health
audience, much of it distressed, and a confident sentence about a cure does
real harm. The full statement of that rule, and what it means for a hook, is in
`docs/video/projects/tinnitus.md` - read it before writing, not after a re-cut.

Also standing: **no ear close-ups, in either format** - and **the picture has
to say the noun the narration says**, which on a channel whose subject cannot
be photographed means drawing it rather than searching harder. See step 4.
