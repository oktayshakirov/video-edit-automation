---
name: video-tinnitus-long
description: Make long-form 16:9 YouTube videos for tinnitushelp.me — either an article explainer from a post, or a sound-therapy session with a generated noise bed and a breathing ring. Use when the user runs /video-tinnitus-long, asks for a long or full-length tinnitus video, wants a post from tinnitushelp.me turned into a YouTube video, or wants a long sound therapy / masking / notched-audio video. For vertical Shorts use video-tinnitus-short instead.
---

# Tinnitus Help — long form

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
Renders go to the Desktop.

**Source content:** `~/Coding/tinnitus-blog/content` — 69 posts plus `zen/`,
which documents ten released sound albums. **There is also an app**,
`~/Coding/tinnitus-app`.

## Shorts do not get a site entry or a social share

**Settled, and it overrides the general publish order below for the short
specifically.** Only the long form goes into `videos.json` and up to Facebook as
a native video. A Short lives on YouTube alone.

## The order of the whole job

**Settled by the user; do not resequence it.** Each step waits on the one
before, and three of them are theirs, not yours:

1. **Build the videos, then stop.** Long and short. Hand them over and say
   nothing about uploading.
2. **They watch.** Either they ask for changes — go back to 1 — or they upload,
   always **unlisted**.
3. **Then audit and write the title and description onto the uploaded video**,
   with `youtube-audit`'s `set --apply`. This is a write, so it needs their
   explicit yes naming that video, after a dry run.
4. **They make it public.**
5. **Then share**, via the `publish-content` n8n workflow.
6. **Then add it to the website**, in `videos.json`.

The registry entry needs the **YouTube id**, which does not exist until step 2,
which is the mechanical reason the site comes last and not a matter of taste.
Upload is deliberately not automated.

## Ask which one first

**This skill makes two different videos and they share almost nothing but the
brand.** Always establish which before doing anything else:

| | **article** | **sound therapy** |
|---|---|---|
| what it is | a post explained | a session to leave running |
| runtime | 2:30–4:00 | 10–60 minutes |
| voice | **`mia`** | **`luna-calm`**, intro only |
| module | `longform/build.py` | `longform/asmr.py` |
| example | `projects/tinnitus-long/does-tinnitus-go-away.py` | see below |

If the user has not said, ask. Do not guess from the topic — "brown noise vs
white noise" is a legitimate article *and* a legitimate session.

---

# Mode 1 — article videos

**Read `.claude/skills/video-crypto-long/SKILL.md` first.** It is the same
engine and the same rules: the narrative arc, the three-phase opening, second
person, no burned captions, push transitions, unnumbered question cards, the
checklist's two timing modes, scene holds, screened stock, the thumbnail layout.
None of that is repeated here. **This file is only what differs.**

Built: `projects/tinnitus-long/does-tinnitus-go-away.py` and
`projects/tinnitus-long/gaming-and-tinnitus.py`.

```bash
PYTHONPATH=. .venv/bin/python projects/tinnitus-long/does-tinnitus-go-away.py
PYTHONPATH=. .venv/bin/python projects/tinnitus-long/gaming-and-tinnitus.py
```

## Choose the beats before writing the script

`does-tinnitus-go-away` shipped with four `checklist`s and they read as one
graphic four times — the crypto skill's silhouette rule, arriving here exactly
as it said it would. **List the beats first and check no two share an outline.**
The gaming cut uses each shape once: `quote`, `grid`, `bars`, `stat`, `compare`,
`steps`, one `checklist`.

`bars` is the beat this site's posts keep earning. Half of them carry a table of
figures against a limit — decibels against safe exposure time, one album's
energy against another's — and a proportion is the one thing narration cannot
say. Two notes from building one: the value text travels with the end of its
bar, so a full-width top row pushes its own label off frame (scale the whole set
by one factor and the proportions stay exact); and a `stat` for the same number
is weaker, because a figure with no scale behind it is just a figure.

## Label a contact sheet, or you will pick the wrong clip

A green-lit apartment block shipped into a short under the line "rain, a fan,
or brown noise" because three rain clips were laid out in one sheet and read
back against the wrong filenames. It screened **L15 S17** — comfortably inside
the box — and green is the one hue that cuts hardest against both palettes.

Two things follow. **The luma/saturation box measures brightness, not hue**, and
a dark green passes it easily; hue against the brand is a separate judgement
the numbers will not make for you. And **put the id in the frame** when
building a sheet, or check each pick individually before writing it into a
shot list. The cost of being wrong is a shot nobody notices until it is in a
render.

## Screen the site's own pictures, every time

The library is much brighter than it looks in a browser and it decides the shot
list. Measured for the gaming cut: `gamer` L22, `live-music-show` L27,
`neurons` L24 — and then `headphones-2` **L206**, `research` L195, `relaxing-
woman` L173, `audiologist` L179. Only the first three could take the full frame;
everything else belongs in a beat's picture column where it is downscaled and
small.

**A blurred `backdrop` does not rescue a bright picture, it spreads it.** Two
beats in the first gaming cut used `research.jpg` and `megaphone-noise.jpg`
behind them and both rendered as a grey wall behind the type — the brightest
frames in a near-black video. Dropping the backdrop entirely is usually the
right answer: a flat panel with the drifting grid is what those beats were
designed for.

## Narration craft: write it to be spoken, not to be read

**This is the section to read before writing a single line of script.** The
AirPods cut was reviewed as "sometimes very good, sometimes very bad" on
exactly this axis, and every instance was one of the five faults below. A
synthesiser has no judgement: it reads what is on the page at the pace the
`gaps` list tells it to. Everything that makes narration sound human has to be
**written into the script as words and numbers**, because there is nowhere else
for it to come from.

### 1. A pause is a punctuation mark and it belongs where the meaning turns

The old table gave values by *category*. Values are not the problem — placement
is. These are the four places a gap is load-bearing, and all four were missing
from the AirPods opener:

| where | gap | why |
|---|---|---|
| before a line that **contradicts** the one before it | **0.85-1.00** | "So you forgot about it." / "Do not." The reversal is the whole point and it needs the silence to reverse *into* |
| after a **two- or three-word imperative** | **0.80-0.95** | "Do not." lands or it does not; a 0.34 runs the next sentence over the top of it |
| before a line that **answers** a question just asked | **0.70-0.90** | the gap is what makes it an answer rather than a continuation |
| between two **halves of one argument** ("not X - it is Y") | **0.55-0.70** on the first half | too short and it is one breathless sentence; too long and they stop being a pair |

**Read the section aloud with a stopwatch before setting the numbers.** Where
you naturally stop, write the gap. Where you naturally run on, write 0.34. This
takes two minutes per section and it is the single highest-value thing in this
file.

**A default-0.34 script is a first draft, never a shippable one.** If a
`Section` has no `gaps=` list, it is not finished.

### 2. Chapter titles have to be written as openers, because they cannot be read as one

Kokoro has no prosody control. There is no way to *direct* a lift into the
voice, so **the opener quality has to be in the words**. Three levers, and use
all three together:

- **A discourse marker on the front of `spoken_title`.** "So", "Now", "But",
  "And" - the words a person actually starts a new thought with. `spoken_title`
  exists precisely so the card can read as a clean headline while the voice
  says something conversational. `title="It was never the earbud"` /
  `spoken_title="So what actually does the damage?"`.
- **A question mark, on anything shaped like a question.** Rising intonation is
  free and it is the strongest opener signal the synthesiser has. This is now a
  hard rule: **every chapter title that is a question gets a question mark, on
  the card and in the spoken line.**

  **The trap is the title phrased as a statement that a reader hears as a
  question**, and it is easy to miss because it scans fine on the page. Two
  shipped in the AirPods cut before being caught on the title list: "Why it
  feels worse with them in" and "When it is not a settings problem" - both are
  answers to a question the card never asks. Inverted: "Why does it feel worse
  with them in?" and "When is it not a settings problem?". **Read the whole
  title list on its own, out of the script, before rendering** - the fault is
  invisible inside a section and obvious in a list of seven.
- **Silence in front of it.** The card lands into whatever the previous
  section's last sentence left behind, so give that sentence **0.80-0.90**. A
  card arriving 0.34 after the previous thought is a new chapter nobody heard
  start.

`card_gap` (1.10 by default) is the silence *after* the spoken title. Leave it
unless the card is the video's turning point, where 1.30 is right.

### 3. Every beat needs a hinge sentence, and a `compare` needs two

**This is the 1:10 fault and it is the most damaging one**, because it makes
the graphic look broken rather than the writing look thin. The AirPods
`compare` read:

    "...Twice a year, if that."      <- last item of the left column
    "Your earbuds."                  <- first item of the right column

The left column was praised and the right one was "quick, no break, just
reading it". Nothing was wrong with the beat. The narration simply **stopped
describing and started reciting**, because a bare column heading is a label,
not a sentence, and a person changing subject says so out loud.

**The rule: the chunk that opens the second column must be a hinge, not a
heading.** Put the turn in words:

    "Now compare that with your earbuds."     not     "Your earbuds."
    "For comparison, your earbuds."           not     "Your earbuds."

The same applies to the first column - "Take a concert." beats "A concert." -
and to every other multi-item beat. **A `steps` or `checklist` gets one hinge
sentence in front of it** ("So here is the whole fix, and it is five settings"),
which already exists as the "say the point, then show the graphic" rule; the
new part is that **the beat's own first chunk also has to sound spoken.**

**The caption chunk count still has to match the reveal count**, so a hinge
does not get its own extra chunk - it is written *into* the chunk that was
already there. "Your earbuds." and "Now compare that with your earbuds." are
both one chunk and both reveal item four.

### 4. Say the whole name of a thing, every time

Half a product name is a guess the viewer has to make while the next sentence
is already playing. The AirPods cut said "cancelling" and "transparency" alone
and both were flagged as confusing.

| write | never |
|---|---|
| noise cancellation, or noise cancelling **mode** | cancelling |
| transparency **mode** | transparency |
| headphone **safety**, in **settings** | headphone safety |
| the **hearing test** in the Health app | the test |

The cost is two syllables. The saving is a viewer who does not have to
back-fill a noun.

### 5. A number that is spoken must also be seen

Not every figure earns a `stat` or a `bars` beat, and the ones that do not used
to be said into the air and lost. `Shot(clip=..., note=("92 dB", "music on a
train"))` draws a small figure card in the lower left - the figure in the brand
accent at display weight, one plain-English line under it saying what that
level actually *sounds* like, on a short vertical rule.

- **It is not `payload`.** `payload` is the 96px centred statement the shot
  exists for; a note annotates while the footage stays the picture. One shot
  should never carry both.
- **The gloss is the point.** "92 dB" alone is a number; "92 dB / music on a
  train" is a thing the viewer has done this week.
- **Lower left, not lower centre** - centre collides with burned captions in
  9:16 and with the YouTube player's own SRT line in 16:9.

## Two things that put the silence cut 25% over its ceiling

Both found on `can-silence-make-tinnitus-worse`, which preflighted at **5:10
against a 4:00 ceiling** on its first complete draft. Neither was fixed by
shaving gaps, and trying that first wasted a pass.

**A chapter's `spoken_title` is already the beat's hinge - do not write a
lead-in sentence as well.** The `grid` section opened with
`spoken_title="And there are three of these stacking up together."` and then a
first sentence reading "Three different problems, with three different fixes."
That is the same sentence twice, 3.5s apart, and the second one exists only
because "say the point, then show the graphic" was applied without noticing
the card had already said it. Deleting it improved the writing and bought back
more time than every gap in the section put together. **Check every beat whose
section is carded**: if the spoken title hands off to the graphic, the beat's
own first chunk is the next thing that should be heard.

**Cast clips by duration before writing them into the shot list.** Eight of
thirty-four slots failed preflight on the first pass, all the same way: a 6.0s
traffic clip under a 9.4s sentence, an 8.4s clip under a 10.4s one. The slot
length is not knowable until the narration is measured, but the **clip
lengths are knowable immediately** - `ffprobe` the whole folder once and keep
the long ones (20s+) for the paragraphs and the short ones for the one-line
sentences. A clip that is short can still be used twice at different
`clip_at`; a clip that is short in the wrong slot is a re-render.

## A `compare` heading has about 18 characters, and nothing warns you

"A room with quiet sound in it" clipped mid-word at the right edge of the
frame in the silence cut's first render, visible at 2:22 and invisible
everywhere else - the beat draws, the preflight passes, and the only way to
find it is to look at the frame. A heading is set at display weight inside
half the frame's width, so **roughly 18 characters is the ceiling**; the left
column can carry more only because it has the same budget and shorter words.
Shorten the label and leave the spoken hinge alone - "A room with sound" on
screen while the voice still says "a room with a low sound in it" is exactly
what the `(caption, spoken)` split exists for.

## The short's thumbnail clears the view count by 20px

`render_short_thumb`'s `band="bottom"` margin is `int(VH * 0.16) + 20`. At the
bare 0.16 the last line of type ran straight through the play count YouTube
draws across the bottom of a Short's grid tile, and the user was opening the
artwork and lifting it by hand before every upload. **It is composed against a
platform overlay that is not in the file**, so a bottom-banded thumbnail that
looks marginally high in isolation is correct. `band="top"` is unchanged.

## Type sits on a blurred shadow, never inside a stroke

**`core.draw.shadow_text` replaced `stroke_width=` on every drawn beat and
every statement over footage, on both channels.** The user's note on a
chapter card was that "the solid border makes it look ugly, use a similar one
like the thumbnails" - and the thumbnails had already been through this
exact argument, where an 8px stroke around every glyph was called out as the
clearest tell of an amateur graphic. A stroke traces each glyph at constant
width, so it reads as an *outline around* the type; a blurred layer under the
type reads as the type sitting on something. The thumbnail renderer had solved
it and the video had not, purely because nobody had carried the fix across.

Two things to know before touching it:

- **It takes the `ImageDraw`, not the image**, reading the image back off
  `d._image`, so the call sites it replaced stayed one line each.
- **`RGB` and `RGBA` are not the same operation.** On `RGB` the shadow
  composites black through the mask. On `RGBA` it has to *add alpha*, because
  `grid` and `steps` draw onto a transparent overlay where a shadow with no
  alpha of its own is simply invisible. Both paths are in the helper; a
  fading beat passes its own `alpha` so the shadow ramps with the type.

**Burned captions in `core/vertical.py` keep their stroke, deliberately.**
They sit over arbitrary moving footage at small size, where a hard edge is
doing real legibility work rather than decoration.

## A photograph bleeds off every edge, or it is not a full-frame shot

The silence cut put the site's `neurons.jpg` (900x599) in a full-frame slot.
Under `max_upscale=1.90` a 900px source cannot reach 1920, so it rendered
**fitted** - a letterboxed panel with a hairline and black bands above and
below - and the user's note at 0:54 was to remove that treatment completely
and show the picture full screen the way the one at 3:27 is.

So the rule is now absolute: **a photograph in a full-frame shot must be large
enough to bleed off all four edges.** Do the arithmetic before writing the shot
(source width x 1.90 must clear the frame width), and when the site's own
library cannot make it - which on both sites is most of the library - either
put the picture in a beat's picture column, where the same file is a
*downscale* at 660px, or use a stock source big enough. The picture column is
what that layout exists for; the fitted panel was never a design, only what
the renderer does when it runs out of pixels.

## Screen a clip by watching it, not by looking at one frame of it

`woman-sitting-alone-dark-room-thinking/6073058` screened at L13-14 / S8 and
appeared on a labelled contact sheet as a woman alone under a single bulb in
an empty room - the exact subject of the script. It shipped into two cuts.
Played, she is **shaving her head**, which is a specific and arresting act
under a line about quiet rooms, and the user caught it in the first five
seconds of both videos.

The luma/saturation box measures brightness. A contact sheet at one timestamp
measures one four-hundredth of a clip. **Neither can see what is happening in
the shot**, and "what is happening" is the only thing that decides whether the
footage illustrates the line. Sample a few seconds of anything before it goes
in a shot list - this is the same failure as the green apartment block and the
unlabelled water, arriving through the one door those rules left open.

## Do not write a two-word imperative for a synthesiser to read

"Do not." was written as its own sentence with a 0.90 after it, straight out
of this file's own advice about imperatives landing in silence. On the page it
is the strongest line in the section; read by Kokoro it is **two syllables and
then nothing**, and the user's note was that it loses the human sound of the
voiceover. A person saying "Do not." carries it with emphasis and a falling
pitch, and there is no emphasis to give.

**Write the full sentence and let the gap do the work.** "Do not make that
mistake." is the same beat, still lands on its own, and gives the synthesiser
enough to read as speech. The gap table is unchanged - what changed is that a
fragment cannot cash the pause the table buys it. This does not retire the
imperative rule; it bounds it: **an imperative needs a subject and a verb.**

## The landscape thumbnail shows the same whole face the vertical one does

**The user's standing rule, and it is now a check on every pair.** The
silence cut's long thumbnail was called "zoomed in too much on the woman" -
and it was not a bad `ay`, it was arithmetic. Her head spans 1036px of the
scaled source against a **720px window**, so no crop of that source could
contain it: the whole family of cover crops was wrong, not the one that
shipped.

**`crop_zoom` below 1.0 now means "stop covering the frame".** The picture is
scaled to the size asked for and set on black at `crop_at`, with the same
260px falloff `shift` uses, so a tall source becomes a **panel beside the
type** instead of a crop through the subject. On the silence pair that is
`crop_at=(0.86, 0.0), crop_zoom=0.50`. It is a better thumbnail than the crop
was, not a fallback: the subject is whole, and the type sits on real black
rather than on a scrim laid over detail.

So: **render the vertical thumbnail first, then match the landscape one to
it.** If the face does not fit at cover scale, panel it.

## Put the title's own question on the thumbnail

**This replaces "ask what the title does not", which went too far.** That rule
was written against a thumbnail that *answered* its own title ("Not the
earbuds. The volume."), leaving no reason to watch - and that part still
holds. But the silence pair shipped with "Silence is not neutral" to satisfy
it, and the user's verdict was that it is "kinda boring", while "does silence
make tinnitus worse" makes the viewer curious.

They are right, and the distinction is clean: **asking the question is not
answering it.** A question on the thumbnail opens the loop the title opened
and closes nothing, so it costs no click. Use the video's own title, or a
tighter version of it, and put the accent plate on the word that carries the
tension - `"Does silence make tinnitus [worse?]"`. Keep the question mark
inside the brackets; outside the plate it hangs off the end looking detached.

What survives of the old rule: **never put the answer on the thumbnail.**

## Name the subject in the first sentence, not on the first chapter card

**The myths cut opened on "You have probably heard at least one of these"
and did not say the word *tinnitus* until the card at 0:14.** The user's note
was to make it clearer what we are talking about, "specially in the beginning
of the videos", and they are right in the most expensive possible way: 74% of
viewers decide whether to keep watching inside the first 15 seconds, and more
than half of all drop-off happens in the first 60. Fourteen seconds of a
video that has not named its subject is the whole decision window spent on
nothing.

This is not the same rule as the three-phase opening already in
`/video-crypto-long`, and it is not covered by it. That rule is about
*pattern interrupt, promise, commit*; a script can do all three while still
being about an unnamed "it". **The subject noun goes in sentence one.**
"Almost everything you have been told about tinnitus is only half right"
does the pattern interrupt and the naming in one line.

**The same fault hides in chapter titles, and it is easier to miss there.**
"Myth: only loud noise causes it" - what is *it*? Every card in that cut had
the same hole, and read as a list they were a video about an unnamed
condition. Fixed by making each one a question that names its own subject:
"Is loud noise the only cause?", "Does tinnitus always go away on its own?".
That also satisfies the question-mark rule for free, because a title forced
to name its subject usually turns into a question on its own.

Two more things worth keeping from the retention research, both of which the
existing rules only half-cover:

- **Hook sentences run under ten words.** Not a stylistic preference - it is
  the same finding as "short, short, one longer that builds", stated as a
  hard ceiling for the opening span specifically.
- **Write the hook last.** When the body is finished you know exactly what
  the video delivers, so the promise can be specific rather than a tease.
  This is worth following literally: the myths cut's second-pass hook ("one
  of those is partly true, the other two are just wrong") is a promise that
  could only be written after the five myth sections existed, and it is a
  far better opener than the first pass's generic three-claim list.

Sources: [vidIQ](https://vidiq.com/blog/post/write-youtube-video-script/),
[Storyflow](https://storyflow.so/blog/youtube-video-script-template-7-part-framework-retention-2025),
[Sumera](https://sumera.io/blog/youtube-hook-formulas-script-examples).

## Icons on `grid` and `steps`, and the emoji is the icon

**Built, and it closes the skill's own oldest open request.** A `grid` card
takes an emoji as a third element - `("Sound therapy", "makes it less
noticeable", "🌊")` - and a `steps` item takes one as a pair -
`("Hearing aids", "🦻")`. The user's note on the myths cut was to put "small
image boxes or icons, vectors" under the listed items; an emoji is the only
icon set on this machine that is already licensed, already colour, and
already solved for the Apple Color Emoji bitmap-strike problem.

- **`core.vertical.emoji_image(char, height)`** is the shared helper, and it
  **caches by `(char, height)`** — a beat draws the same five glyphs on every
  one of its ~480 frames, so rendering a 160px glyph and LANCZOS-scaling it
  per frame is pure waste. Never mutate what it returns; fade a copy.
- **`out` is RGB, so an emoji goes on with `paste(im, xy, im)`, not
  `alpha_composite`.** The background pass returns RGB and
  `alpha_composite` raises on it. The drawn beats' `ImageDraw.Draw(out,
  "RGBA")` is an RGBA *draw context* over an RGB image, which is easy to
  misread as the image being RGBA.
- **On `steps` the icon replaces the numeral inside the node**, rather than
  sitting beside the label. A number and an icon competing in one layout is
  two systems, and the track itself already carries the order — which is what
  it was always for.
- **On `grid` the icon eats into the wrap width before anything is
  measured.** Laying the glyph in afterwards puts it over the last word of a
  label that wrapped to the full card.

**Two glyphs to avoid on this brand.** 🦠 is bright green, which the file
already records as the one hue that cuts hardest against both palettes; 🩺
renders near-black and disappears against a dark card. 🌡️ and 🫀 were the
replacements.

## Forcing `render_thumb(side=)` fights the auto-scorer, it does not steer it

`render_thumb` without `crop_at` runs its own layout pass — it does not just
slice the raw photograph in half and put type on the empty side. It
re-crops and repositions the subject as part of scoring where the type can
go. Passing `side="left"`/`"right"` on that same call does not tell it which
half the subject is on; it forces which half gets the type *inside whatever
crop the scorer already chose* — and if you guess wrong about which side that
crop left empty, the result is type printed straight across the face, not
type on the wrong-but-safe half.

This bit the myths thumbnail directly: a photo with the subject in the raw
image's left third rendered perfectly with no `side` argument at all (the
scorer put him on the left and the type on the right, correctly). Passing
`side="right"` on the same call — reasoning from the raw photo's geometry,
"he's on the left, so put type on the right" — produced type overlapping his
face, because the auto-scored crop was not a literal left-right split of the
source. **The fix is to not pass `side` unless a manual `crop_at` is also
given.** `side` is an escape hatch for when you are placing the picture by
hand (`crop_at` bypasses the scorer entirely, see the docstring), not a
shortcut for telling the automatic layout something it already knows.

## A thumbnail's `render_thumb` will happily upscale a 600x400 site image 5x

`tinnitus-myths-vs-reality`'s first thumbnail render used the article's own
hero, `tinnitus-myths-reality.jpg` — 600x400, like almost every image in this
site's library. `render_thumb` has no size floor: it scaled the source to
cover 1280x720 (a 3.2x upscale minimum, more once the scorer picked its crop)
and the auto-scorer chose a patch that was a stranger's laptop and a pencil —
blurry, off-subject, and nothing raised. The failure is silent in exactly the
way the "photograph must bleed off every edge" rule already named for
full-frame video shots; it had just never been checked for thumbnails.

**The fix was a stock photo, not a smaller crop.** `assets/stock/photos/`
already had one from an earlier fetch —
`woman-stressed-dark-background-copy-space/8011883.jpg`, 6475x4317, L15/S3 —
with the subject sitting in the right third and a wall of black to her left.
That composition needs no `crop_at` at all for the 16:9 long thumbnail, and
for the short's 9:16 one it only needed `ax=0.90` to keep her in frame: a
landscape source with real copy space on one side can serve *both* aspects
by cropping alone, which is a cheaper fix than fetching a second, portrait
orientation photo when one is already sitting in the cache. Check an
image's actual pixel size before handing it to either thumbnail renderer —
`Image.open(path).size` — the same way a clip's duration gets checked before
it goes in a shot list.

## `Section.number` puts a big numeral on a chapter card — for a counted series only

**`ChapterCard`'s own docstring bans a numeral before every title, and that
rule is unchanged.** A numbered agenda tells the viewer they are being
lectured. `number` is the one deliberate exception: a script that is
genuinely enumerating something and *says the number out loud* ("myth one",
"myth two") gets it on screen too, because the viewer is already tracking the
count — the user's note on the myths cut was exactly this, that the count
should show when the narration says it.

Pass `Section(number=1)` only on sections where `spoken_title` (or the
narration right after the card) actually says that number. A numeral with no
matching word is right back to being a slide deck; that is the whole
distinction between this and the agenda pattern the beat refuses to draw by
default. It draws above the card's rule, sized off the title (`NUM_SCALE`,
`NUM_GAP` on `ChapterCard`), and the whole group re-centres around one
vertical middle rather than pushing the title down.

## A clip is over-used long before it is used twice

**Every note the user gave on the myths cut's footage was one of three
faults, and they compound.** The rules now:

- **No clip plays more than twice, and never twice inside a minute.** That
  cut ran `stressed-man.../6415592` three times and two more clips twice, and
  the note was that it "looks very repetitive". A second use is fine as a
  deliberate echo — the myths re-cut re-opens on its own opening face at the
  close — and a third is not.
- **No clip holds longer than about eight seconds.** Two slots ran 14.7s and
  10.4s and the user flagged the first one by timestamp. **The fix is usually
  not a longer clip, it is splitting the sentence**: both offenders were a
  single `Section` sentence with four or five caption chunks, which is one
  span and therefore one picture. Splitting "See a doctor if it is new, will
  not settle, sits in one ear only, or comes with hearing loss" into two
  sentences turned one 14.7s hold into two shots without touching a word.
- **Cast a clip against the line it sits under, then check the list for
  clips that are only atmosphere.** The skill already says a concert line
  gets a concert; the corollary is that a slot with no obvious subject is
  where a wrong clip hides.

**Adjacent Pexels ids are the same shoot, and nothing in the pipeline knows
that.** Searching for a replacement for `6415592` returned `6415611`,
`6415649` and `6415877` — all screened at L13-18, all perfect on the numbers,
and all *the same bearded man in the same black studio*. Using one would have
made the repetition worse while looking like a fix. **Treat a candidate whose
id is within a few hundred of a clip already in the cut as the same clip
until a contact sheet proves otherwise.**

## Screening for brightness is not screening for who is in the shot

**The hook's two replacement faces repeated the exact fault they replaced.**
The first cut's opener was called out and swapped for two new clips; both
landed as Black actors, and with `TEMPLES` — also Black — as the very next
shot, the hook opened on three Black faces in a row. Nobody chose that
deliberately either time. It is a structural side effect of screening stock
purely on `luma`: a pale face against a dark backdrop is *brighter* by
definition than a dark face against the same backdrop, so the `MAX_LUMA`
ceiling this whole pipeline screens on rejects lighter-skinned candidates
more often. Every query tried afterwards — "caucasian woman", "man portrait
dark moody european", explicit ethnicity terms in the search string — kept
returning the same small set of darker-skinned actors, because the Pexels
tags on a clip are not reliable and the luma filter is doing the real
selecting underneath the query.

**So casting is a thing to look at on the finished contact sheet, not just
infer from a search query.** After screening a batch for brightness, look at
who is actually in it before writing the shot list, and count how many
people of the same appearance land in a row — the same discipline this file
already applies to subject matter and to over-used clips, extended to who is
on screen rather than what they are doing.

**Two closeup faces back to back is the practical ceiling; three reads as a
wall of faces regardless of who they are.** The fix here was not "swap two
more faces for two different ones" — it was also removing the third shot
entirely and giving it to an abstract instead, so the hook is two people and
then a change of register, not three portraits in the same "studio, dark
background" setup.

**A shoot rejected for being over-used stops being over-used once nothing
from it ships.** `man-serious-portrait-dark-studio-black-background/6415611`
and its siblings were flagged on an earlier cut as "the same man as the
clip already over-used." By the time this fault was found, that whole shoot
had been removed from the video — so a single clip from it was a legitimate,
first-time use, not a repeat of anything. Re-check whether an old rejection
still applies before re-applying it; a stale "cannot use this" is as much a
bug as a stale "safe to reuse."

## A clip already in the cache has *not* been screened. Sheet everything.

**This is the rule the myths re-cut broke while writing the rule above it.**
The second pass carefully contact-sheeted every *newly fetched* clip and then
reused a dozen cached ones on the strength of their folder names — and four
of those were wrong in ways no measurement could see:

| clip | folder name says | what it actually is |
|---|---|---|
| `man-sitting-alone.../7280519` | man alone, dark apartment | head in hands with **a row of beer bottles** on the floor — reads as drinking |
| `tired-woman-hands-on-face/7676117` | tired woman, studio | woman in a **surgical mask and black leather gloves** |
| `tired-woman-hands-on-face/7676122` | tired woman, studio | hair completely covering her face — horror-adjacent |
| `quiet-library-reading-dark/10480415` | quiet library | a **red-lit antique treasure map** and a magnifying glass |

The beer-bottle one shipped into a rendered Short under "it does not just
fade, it can last for years" and was only caught by looking at the finished
frames. **A folder name is the search query somebody typed, not a description
of the footage** — Pexels returned it, the luma box passed it, and nothing
between those two facts looked at the picture.

So: **build one labelled contact sheet of every clip in the shot list, cached
or fetched, before the first render.** Three timestamps across each clip, id
burned into the frame. It costs about a minute for a whole cut and it is the
only step that catches subject faults, which are the only faults the user
ever notices.

## The stock shelf for anything medical is lit bright, and the dark ones are worse

Screened for the myths cut: every `doctor-consultation`, `hearing-clinic`,
`therapy-session` and `stethoscope` result came back **L82 to L195** against
a ceiling of 48. Medical stock is shot on white. There is no grading fix —
`VideoShot`'s dim only reaches so far, and a dimmed white clinic is a grey
clinic.

**The one dark result was worse than the bright ones.**
`doctor-night-shift-dark-hospital-corridor` screened at L36-40, comfortably
inside the box, and is **a bald child in a hospital gown being pushed in a
wheelchair** — it reads as a children's cancer ward, under a script about
ringing ears. `man-talking-to-camera-dark-room-interview/7230790` screened at
L27-30 and has a handgun on the table. Both would have shipped on the
numbers.

So for the "see a professional" beat, stop looking for a clinic. What works
is **the act rather than the place**: a hand on a phone, somebody at a window,
a person sitting with it — with the red flags carried as a `payload`
statement card over the shot, which is also how the medical rule's "put the
red flags on screen" gets satisfied without spending a sixth beat shape.

## Per-word captions on shorts, and why the sprite had to change

**`karaoke=True` is the default on `render_tinnitus_short` now.** The user
asked for the treatment every short-form platform uses: the whole phrase
stays up and the word being spoken is picked out in colour at a slight
scale. `core.vertical.render_caption_karaoke` draws one frame per word and
`crypto/build._karaoke_sprites` emits one sprite per word.

Four things that are load-bearing:

- **The layout is measured once at the base size and never re-flowed.** The
  active word is drawn larger *about its own centre, inside the advance the
  base font reserved for it*, so no other word moves. Re-measuring the line
  with one word enlarged makes the sentence twitch sideways on every
  syllable, which is much worse than no highlight.
- **`grow` is 1.08, not 1.14.** The enlarged word overhangs its box by half
  the difference each side, and at 1.14 a long word visibly touched its
  neighbours — the inter-word gap is one space at caption size. The colour is
  doing most of the work.
- **`CaptionSprite` needed per-sprite `fade_in`/`fade_out`.** Every sprite
  used to run the same 0.13s scale-and-fade entrance, which for a per-word
  caption re-fires on every syllable and cross-dissolves the phrase against a
  near-identical copy of itself — a soft flicker that reads as a broken
  render. Only the first word frame of a caption animates in and only the
  last animates out; the ones between hard-cut.
- **Word timings are apportioned, not aligned.** `_word_spans` splits a
  caption's span by `len(word) + 1`. The chunk boundaries either side are
  real DTW timestamps and a chunk is three to six words, so the drift is
  under a syllable; aligning per word would mean synthesising every word of
  the script alone as a timing reference.

**And it shipped with a real lag anyway, on the first cut to use it — see
"The karaoke lag" below.** The fix landed after this section was first
written; read that one too before touching `_karaoke_sprites` again.

Captions carrying an emoji keep the single-PNG treatment: `add_caption_emoji`
re-centres the whole line around the glyph, which the per-word layout does
not model.

## The karaoke lag, and why it was invisible in testing

**The first myths short shipped with every word lighting up late**, and the
user could see it as a real lag rather than a rounding error. The bug was in
the one place a still-frame check of `render_caption_karaoke` could never
have caught it: `_karaoke_sprites` computed "where the voice stops inside
this caption" by looking for the next caption's `start` — but
`build_narration_aligned` had *already* stretched `Caption.end` to equal that
same value, via the hold-until-next rule two dozen lines earlier in the same
function. So the "fix" was a no-op: `speech` always equalled the already-
stretched `end`, and every word's span was apportioned across the caption's
full *displayed* window, silence included. Short sentence, long trailing gap
— worst lag. Long sentence, short gap — barely visible, which is exactly the
shape of case a spot-check on one line would miss.

**The fix is a field, not a recomputation.** `Caption` now carries
`speech_end`, defaulted to `end` in `__post_init__` and therefore captured at
construction time — *before* the later loop mutates `.end`. Nothing else has
to change: the hold-until-next loop only ever touches `.end`, so
`speech_end` is the true boundary for the whole life of the object.
`_karaoke_sprites` reads `c.speech_end` directly now, with no search over
neighbouring captions.

**The general lesson: a "stretched for display, but I need the original"
value has to be captured at the moment it is still original, not
reconstructed from the stretched value later.** Searching forward through
`captions[i+1:]` for the next caption's start looked like it was recovering
the pre-stretch boundary; it was recovering the *post*-stretch one, because
that is what `.start` on the following object always was regardless of when
you look.

## Shorts get the music bed too

`render_crypto_short` has taken `music`/`music_gain` for a while and the
article shorts were simply not passing them — recorded in both short skills
as "requested and not yet built" long after it was built. **Every short gets
`music.track("night-drift")` at `music_gain=0.85`.**

**The generated presets are retired on this channel.** `bright`, `pulse` and
`tension` are not to be used again — the user's call. `night-drift` is the
prepared track, it is shared with thecrypto.wiki, and it is stored trimmed so
its loop has no hole in it.

## A short's `Shot` list has no `None` holds — that is longform-only

The long-form `lay_out` treats `None` in the shots list as "keep the previous
shot running", which is how a section holds one picture across several
sentences. The short's own `plan_shots` (`crypto/shots.py`) has no such
branch — it zips shots against sentence spans one-to-one and a `None` raises
`AttributeError: 'NoneType' object has no attribute 'start'`. Copying a
longform section's shot list into a short and swapping in `None` for a hold
is the mistake this caught: **every sentence in a short needs its own `Shot`
instance**, even if it is the same clip file at a different `clip_at` — that
reads as a continuation on screen without being one in the code.

## A site image's filename is a promise its photograph does not keep

**`young-tinnitus.jpg` is a bright classroom with a child in a VR headset.**
It went into the myths cut's closing `checklist` as the picture column on the
strength of its name — the beat busts "only elderly people get it", so a file
called *young-tinnitus* is the obvious pick. The actual photograph says
nothing about age, ears or hearing, and at L172 it was the brightest thing in
the frame.

Same class of error as trusting a stock folder name, and this library is full
of it: `silence.jpg` is a teal studio "shh" shot, `tinnitus-myths-reality.jpg`
is a desk with a laptop and a textbook. **Open the file before writing it into
a beat.** The replacement here — `kid-and-dad-with-headphones.jpg`, L71, a
child and a parent both wearing headphones — is the picture the line was
actually about, and it is a hundred luma darker.

## Grid icons are 64px in landscape, not 46

A two-column `grid` card at 1920 is about 880px wide, and a 46px glyph in the
corner of it read as a smudge. The whole point of the icon is to be legible
*before* the label is. Portrait stays at 54, where the card is narrower and
the glyph is already proportionally larger.

## A background's blobs need `sigma` past ~0.6, or they read as separate clouds

**`tinnitus-plum` shipped once at `sigma` 0.26-0.36 per blob and the user's
note was "we can see where each color starts and ends".** That is not 8-bit
banding — the dithering already fixes that — it is the blobs themselves:
individually wide, but still small enough relative to the frame that each one
has a visible edge where it fades into the next, worst in a beat with an
empty half (`compare`, `chapter`) where nothing else on screen competes for
the eye.

**The fix is fewer, much wider blobs — `sigma` 0.62 and 0.70, not three
around 0.3.** Past about 0.6 a blob's falloff sits mostly outside the visible
frame in every direction, so two of them overlap into one continuous field
with no seam a contact sheet can find. Verified by drawing a real `compare`
on the new generation and a real chapter card, the same way the original
PLUM was judged.

**The vignette was part of the same fault, not a separate one.** The old
`(1 - 0.55 * clip(r2 * 2.4, 0, 1))` term saturates its `clip` at r ~= 0.645
from centre — so outside that radius the multiplier is one flat number while
inside it the field is still changing, and a plateau butting up against a
gradient reads as an edge of its own. `0.35 * clip(r2 * 1.6, 0, 1)` still
darkens the corners; it just never stops changing before the frame edge.

Both constants live in `core/backdrop.py`'s `aurora()` and `PLUM`. `aurora()`
is the only spec generator on either brand, so tuning it once fixes every
generated background this repo has — there is no per-preset version to
forget.

## Music: the generated presets are retired

**`bright`, `pulse` and `tension` are not to be used on this channel again.**
The myths cut shipped with `bright` and the user's note was that it is "the
one which we decided to not use anymore, delete it and never use it again".
Every video, long and short, uses `music.track("night-drift")` — the prepared
track that lives in `assets/brand/music/` and is shared with thecrypto.wiki.

The presets stay in `core/music.py` because they are the safer licence story
for anything new and `render_long` still accepts a preset name; they are just
not the pick here. If a second real track is ever added, add it with
`music.prepare_track`, which trims both ends — untrimmed encoder delay
becomes an audible hole in the bed once per loop.

## Keep this file current, every time

**The user's standing instruction: update the skill on every video.** These
files are the only thing that carries a lesson from one cut to the next - a fix
that lives in one project file is a fix that gets re-learned the hard way three
videos later. After every round of review notes:

1. Write the rule into the relevant skill, with **the specific failure that
   produced it**, not just the rule. "Say noise cancellation, not cancelling"
   is forgettable; "the AirPods cut said 'cancelling' alone and it was flagged
   as confusing" is not.
2. Put engine-level findings in the engine's own docstring too, so somebody
   reading the code sees them without the skill.
3. If a rule turns out to be wrong later, **replace it and say what replaced
   it** - a skill that only accretes becomes a file nobody reads.

## No ear close-ups, in either format

**Two were shipped in the AirPods cut and both were rejected on sight**, in the
user's words as "a nasty close up of ear which dont look good". A macro of an
ear canal at full frame is unpleasant to look at, and it is not even
informative — the viewer knows what an ear is. `human-ear-close-up-dark` and
`audiologist-hearing-test-ear` are both in the stock cache and neither should
go in a cut; the clinic one is a backlit red ear against grass at L140-156, so
it fails the brightness box as well.

**A video about hearing does not have to show an ear.** The subject is a person
listening — a commuter with headphones, someone putting an earbud in, a hand on
a volume control. Those read faster and are pleasant to watch, which is the
whole job of a shot nobody is reading.

## Show the thing the line is about

**A concert line gets a concert.** The AirPods cut ran an empty night street
under "a concert is loud, and then you go home" and the user's note was to use
something relevant. Stock searched for atmosphere ("city traffic night") comes
back as atmosphere, and atmosphere under a specific noun is a shot that
illustrates nothing — the same failure as the sleep cut's unlabelled water,
arriving through a different door.

Concert footage screens well for these palettes, which is not obvious: a gig is
mostly dark with coloured stage light, so `concert-crowd-night-stage-lights`
measured L20-32 and a crowd with raised hands L27-32. **Check the hue, not just
the box** — two clips in the same batch were green-lit and green is the one
colour that cuts hardest against both brands.

## Open on a face, moving

The first cut opened on a still of a worried woman and the note back was that it
is not an engaging way in. A **clip** of someone visibly dealing with it reads
instantly, needs no caption, and costs nothing — `headache-stress-tired-woman-dark`
screened at L46/S22. For a health topic the opening frame should be a person, not
a concept.

## The background behind a drawn beat is an asset, not a drawing

`assets/brand/backgrounds/`, named by `Brand.backdrop`, loaded by
`core/backdrop.py`. **tinnitushelp.me is `tinnitus-galaxy`** — a nebula
starfield the user supplied, ping-ponged — and thecrypto.wiki is
`crypto-blackwater`.

**`tinnitus-galaxy` is gone too, and the brand is now `tinnitus-plum`.** The
galaxy shipped on the silence cut and the user's note was simply that they
were not happy with it; what they asked for instead is "a high quality dark
purple background which makes the text pop and looks clean". `tinnitus-plum`
is generated - a near-black plum base, three very wide very soft blooms, the
standard vignette - at **L29.8 / S30.4**, and it is the one that got approved
after all four candidates were judged the only valid way, by drawing a real
chapter card and a real `compare` on each.

**The starfield failed the rule this file already carried, and the file had
talked itself out of it.** "Soft, low-frequency only" was the rule; the galaxy
section argued the stars got away with breaking it because at 512px upscaled
3.75x their detail "turns to mush attractively". That was a defence of the
asset, not a test it passed - high-frequency detail behind type competes with
the type, and three rejections on this brand now all point the same way.
**Do not put content behind the words.** The other half of it is that
**clean is not flat**: `tinnitus-violet` was rejected for flatness, so the
blooms in `PLUM` are what stop it being a dark rectangle - they are simply too
wide and too dim to read as shapes.

**Three purples have now been rejected here** (`aurora` generated and the
wrong shade, `violet` a bright supplied gradient, `galaxy` a supplied
starfield) and all three assets are **deleted from the folder**, not merely
unreferenced - leaving one there is how a rejected background gets pointed at
by name a second time. `crypto-blackwater` is untouched; this change is
tinnitus-only.

**`tinnitus-aurora` is gone and must not come back.** It was a *generated*
purple mesh gradient, and it shipped on the AirPods cut after the user had
already ruled that particular purple out in an earlier session. The asset is
**deleted from the folder**, not merely unreferenced — leaving it there is how
a rejected background gets pointed at by name a second time. Its spec survives
in `backdrop.py` as `_RETIRED_TINNITUS_AURORA`, renamed so it reads as an
example of `generate()`'s argument shape rather than as a live preset.

**Two supplied backgrounds have now been through here and the second one is
the lesson.** `tinnitus-violet` was a bright mesh gradient (**L89 / S201**)
that needed dimming to 0.55 before peach type held, and it still read as a flat
magenta wall — it lasted exactly one review. `tinnitus-galaxy` arrives at
**L27 / S242**, already inside the range the water (L23) and the old aurora
(L19) occupy, and ships at `pingpong(..., dim=0.92, saturation=0.80)`.

**So the useful test on a supplied clip is its luma before you touch it.** A
source that needs heavy dimming to take type is usually the wrong image rather
than an image needing grading — dimming a bright flat gradient gives you a
darker flat gradient, and the flatness was the actual problem. A source already
near L25 needs almost nothing and keeps its own depth.

The galaxy is also the first background here that is on brand **by subject**
and not only by palette: the app's own album is *Quiet Universe* and its
artwork is space, the same argument `longform/asmr.py` makes for its procedural
nebula.

**It breaks the "soft, low-frequency only" rule and gets away with it**, which
is worth knowing before somebody cites that rule to reject the next one. Stars
are high-frequency detail, and at 512px upscaled 3.75x they arrive as soft
points that read as texture. The test it passes is that its detail turns to
mush attractively — not that detail is allowed. A background with *legible*
content is still wrong.

This replaced a ruled grid that drifted behind every beat on both channels. It
went for two reasons and only one was cosmetic: it stepped a **whole pixel at a
time** (`int((f * 40) % 96)` on a layer moving 40 px/s), which is the judder
every other moving element here was fixed for years ago and which the user
reported as "the background is laggy at 1:00 and 1:35"; and ruled lines behind
type read as graph paper, identically, in every video on both channels.

Three things about the asset design, all of which will bite if ignored:

- **Backgrounds are square and small (512x512).** One file serves a 1920x1080
  beat and a 1080x1920 one, scaled to fill and centre-cropped. Only viable
  because they are deliberately soft and low-frequency. **Anything with legible
  content in it does not belong here** — the type is the subject.
- **Sampled by timeline seconds, not by the beat's `f`.** Sampling by beat
  progress runs the whole loop inside every beat, so the background visibly
  changes speed at every cut. `Backdrop.at(t, w, h)` wraps absolute time, so
  motion is one constant rate across the video and carries through a cut.
- **Match the luma range**: the violet runs a mean of ~48, the water ~23. Much
  brighter and peach type stops holding against it, which is not hypothetical —
  it is what the violet source did at L89 before it was dimmed.
- **Judge a new background by drawing a real beat on it.** The mean tells you
  almost nothing about whether type reads. And **`backdrop.get()` caches by
  name**, so rendering three candidate variants under one filename silently
  compares the first against itself three times — give each variant its own
  name or the comparison is worthless.

Generated backgrounds loop because every element travels a **closed circular
path** whose period divides the loop. Footage cannot, so `pingpong()` does it
the other way — forward then reversed — which is only invisible on subjects
with no arrow of time. Water, smoke, cloth. Measured on the water: the seam is
2.91 against a median ordinary step of 4.41, so the join is *less* change than
a normal frame.

## What differs from crypto

**Voice is a candidate and it moves.** The first two cuts used `mia`;
`tinnitus-and-sleep` uses **`mia-calm`** — af_heart at 1.00, the channel's own
reader unhurried, which is the delivery a bedtime script wanted anyway.

### The male voice for an article video comes from the crypto roster

**`elias`, `felix`, `jonas` and `caspar` are all ASMR voices and none of them
belongs on an explainer.** The AirPods cut shipped with `elias` on the reading
that only `caspar` was the ASMR one, because that is the only profile whose
note says so. That was wrong, and the construction says why: **every "male"
profile on this channel is `af_nicole` pitched down through the SOFT chain** —
the chain that exists for sound therapy, with the presence band pulled down and
air added. They differ from each other only in how far the pitch moves and
whether the slowdown is kept. Picking a different one does not get you out of
the ASMR read, it gets you a differently-processed ASMR read.

**Use `sam` (`am_puck`, ENERGETIC).** A real male voice rather than a processed
female one, and the roster's own note is "graded C+ with hours of data, the
steadiest American male". `theo` (`am_adam`) is the alternative, 9% faster and
graded F on the model card but shortlisted by ear. The tinnitus male set stays
in `core/voices.py` because mode 2 is where it belongs.

**Changing between these families rewrites the script, not just the voice.**
Measured on one paragraph: `elias` 1.97 words/sec, `sam` 3.31, `theo` 3.60,
`mia` 3.06. So the tinnitus male profiles need ~400 words to fill four minutes
and `sam` needs ~620 for the same runtime — the crypto skill's 440-700 budget
holds for `sam` and `mia` and does *not* hold for the pitched-down set. A
script written for one and read by the other misses the window by ninety
seconds in whichever direction. Re-run the preflight after any voice change.

**`ivy` (bf_emma) was tried here and deleted from the roster entirely.** The
British read was not wanted on this channel, and a rejected voice left in the
profile list is one somebody picks again by accident. If a voice is out, take
it out of `core/voices.py` rather than noting it here.

`luna-calm` is the sound-therapy voice and belongs to mode 2. **A short and a
long video from the same post must use the same voice** — two voices on one
channel is two channels.

**Changing the voice changes every clip slot.** `mia-calm` reads ~9% slower
than `mia`, which pushed this cut from 3:47 to 4:09 and broke a slot whose clip
was exactly 10s. Re-run the preflight after any voice change; do not assume the
shot list survives it.

## Open requests — both now built

Both came from review of the sleep cut, were deferred, and were finally built
on the myths re-cut. Kept here as a pointer to where they landed.

- **~~An emoji beside each `grid` card.~~** Built, and extended to `steps`.
  See "Icons on `grid` and `steps`" above.
- **~~The article shorts have no music bed.~~** Built —
  `render_crypto_short` had taken `music`/`music_gain` all along and the
  project files simply never passed them. See "Shorts get the music bed too".

## Line breaks are balanced, and no short word strands alone

`thumb._wrap_balanced` replaced a first-fit greedy wrap with the standard
minimum-raggedness line break (the algorithm behind CSS `text-wrap: balance`).
Greedy fill stops at the first word that would overflow the column and never
looks ahead — which is how "STOP SLEEPING IN SILENCE" rendered as four
one-word lines even though "IN SILENCE" fits together with room to spare. The
DP scores every legal split by how much slack it leaves against the column
width, so a pairing that leaves less slack always wins over stranding a
two-letter connector on its own row.

**Two things had to be true for this to actually fix it, not just move the
bug:**

- **A multi-word line is never allowed to overflow the column**, full stop.
  The first version penalised overflow by a near-constant score regardless of
  degree, which made a wildly-overflowing three-word line look almost as cheap
  as a genuinely unavoidable single wide word — and the DP picked it, running
  text off the edge of the frame. Only a lone word with nowhere else to go may
  overflow.
- **The size search cannot stop at the first size that merely fits.** The
  largest size clears `max_lines` almost immediately — one word per line is
  always short — which is exactly the size that produced the orphan in the
  first place. `_headline` now keeps shrinking past a fitting size while any
  line is a stranded word of three letters or fewer, and only accepts a size
  where that stops being true (falling back to the best "fits" size if no
  smaller size ever clears it).

## `crop_at` — a manual crop for when the scorer picks the wrong region

`render_thumb(crop_at=(ax, ay), crop_zoom=)` bypasses `_layout`'s automatic
subject search entirely. Needed the moment the long and the Short started
sharing one source photo: `_layout` optimises for the quietest patch of frame
for the type, not for whether the subject is actually visible, and on a
portrait photo cover-cropped to landscape it chose a towel and a shoulder over
the band with her face and the phone's glow in it. Same failure the shorts
skill already named ("the scorer loses to the subject"), arriving at this
renderer once it started taking pictures that were not composed for it.
`(ax, ay)` are fractions of the leftover crop space after scaling to cover the
frame — sweep a few values and look, the same way a face is found by eye
everywhere else in this pipeline.

## The long and the Short from one post share a thumbnail

Same headline, same type treatment, different aspect and crop. They are
published as a pair and a viewer who sees both should recognise the second one.
`thumb._headline` draws the type for **both** `render_thumb` (1280x720) and
`render_short_thumb` (1080x1920), which is the mechanism that stops them
drifting — do not fork it.

The treatment, settled against reference thumbnails from large channels:

- **Arial Black**, not Futura. A light wide geometric goes weak at feed size.
  Impact is heavier still and reads as meme-coded.
- **A blurred drop shadow on its own layer, never a stroke.** A stroke traces
  every glyph at constant width and reads as an outline; that was the single
  thing called out as making these "look very unprofessional".
- **One accent run on a solid plate**, padded from the cap band.

**The two aspects need different source photographs, and that is not optional.**
A landscape picture of someone lying down cannot be cover-cropped to 9:16 — the
subject's long axis is the one being thrown away, and no zoom or pan recovers
it. Fetch the Short's picture with `orientation=portrait`.

## Titles: a question gets a question mark, every time

The channel is consistent about this and it is worth keeping that way —
`How Loud Is Too Loud?`, `Does Tinnitus Go Away?`. The trap is a title that is
*phrased* as a statement but *reads* as a question: `Why It Is Worse at Night`
was drafted that way and had to become `Why Is It Worse at Night?` before
upload. If the second half of a colon title is an implied question, invert it
into a real one and punctuate it. The rising intonation is free.

## A dark gradient does not have the bit depth to be smooth

The aurora shipped once with visible contour rings and the note was "I can
clearly see the changes in the background colors in the shapes". That is not a
flaw in the gradient — measured, the whole 1920px centre row spans **levels 14
to 45**, so the entire frame is drawn with 31 distinct 8-bit values and every
one of those steps is an edge.

`Backdrop._dither` trades the contour for noise below the threshold of vision.
Two things about it that are not optional:

- **It happens after the upscale.** Dithering the 512px source and then
  resizing 3.75x runs the noise through a low-pass filter and the bands come
  straight back — the interpolation averages exactly what the dither varied.
- **It changes every frame.** A fixed field reads as dirt on the lens. Frames
  come from a rotating pool of eight rather than fresh per call, because a new
  1920x1080 random field per frame is 2M values on every frame of every video.

Measured: longest run of identical values along a row went **158px to 7px**,
mean run 23.1px to 1.5px, at 8.7 ms/frame. If a background ever bands again,
measure run lengths — level *count* barely moves and will tell you nothing.

## Music can be a real track, and it must be stored trimmed

`assets/brand/music/`, via `music.track(name)`. `night-drift` is the user's
pick over the generated `bright` preset.

**`render_bed` loops a short track to fill the video, so silence on either end
becomes a hole in the bed once per loop.** An mp3 decodes with encoder delay
bolted to the front: this one arrived with **54.4 ms** of digital silence
against an end running at full level — twenty-nine audible gaps across a four
minute video. `render_bed` has a `start=` offset that hides it, but then the
right offset is a number somebody has to remember per track.
`music.prepare_track` trims both ends once and stores WAV, so the asset is
correct by construction.

Generated presets remain the default and the safer licence choice. **Check a
new track's loop before using it** — trimming fixes silence, not a piece that
was never written to loop.

**Do not let stock footage become wallpaper.** The first sleep cut used the
calm-water stock four times with nothing on it and the user called it out: the
script is about bedrooms, so unlabelled water illustrates nothing. Two rules
came out of it. **Footage should be the subject of the line it sits under** —
rain on a window earned its place in the "what to play" section because rain is
one of the sounds the post recommends. And **if a clip is only atmosphere, it
needs a line on it**, which is the `Shot(clip=..., payload=("", "..."))`
treatment the format already has. The user's phrasing: use it less often, and
only with text over it.

**Music is `bright`**, not `pulse`. Warmer and less tense. This audience is
frequently here *because* sound is a problem; the bed should not be one.

**The picture library is thin and small.** 105 images, only 27 reach 900px, and
none exceed 1000px. At `max_upscale=1.90` a 900px source cannot fill 1920 — so
**prefer beats with `picture=` over full-frame photos**, where the same source in
the 660px column is a downscale. Fill the rest with screened stock; the article
video uses six clips and eleven site images.

**The watermark is a different shape and it moves the kickers.** thecrypto.wiki's
mark is a wide 33px wordmark; this one is a mascot with the domain under it,
159px tall at the same scale. Beat kickers derive their y from the mark's actual
bottom (`_mark_bottom`) — at the old fixed y=214 the heading printed straight
through the wordmark. `Brand.mark_scale` is 0.62 here for the same reason: a
tall lockup at a wide wordmark's width dominates the frame.

### The mark's height is charged to the picture, twice

**`mark_scale` is 0.42, down from 0.62, and `PhotoShot.LOGO_CLEAR` is 10, down
from 16.** The gaming cut shipped at the old numbers and the user's note was
that the watermark was so big it pushed the photographs down and left an empty
band across the top — which is exactly what the arithmetic does. A photo that
*fits* the frame must clear the whole lockup, so at 159px tall the top hairline
landed at y=272 in a 1080 frame, and then the picture was **scaled down** to fit
the band that was left. Both costs come out of the same number. At 113x110 the
same shot starts at y=220 and renders larger.

Do not read this as "the mark can always shrink". It is legible at 0.42 and the
domain has to stay readable — that is the whole reason the lockup carries it. If
it needs to come down again, **set the mascot beside the domain instead of above
it**: a wide mark costs the picture nothing, which is why thecrypto.wiki has
never had this problem.

`LOGO_CLEAR` is shared, so crypto long form gains 6px too. It cannot move the
shipped vertical shorts — measured, their photographs sit ~550px down a 9:16
frame and the dodge never fires.

**That hairline is this brand's peach now, not thecrypto.wiki's gold.**
`PhotoShot` took its colour from a module constant, so every photograph in every
tinnitus video — long and short — carried a gold edge, and nothing raised. It
takes the `Brand` now, like the drawn beats always did. Anything rendered before
this is off-brand at the photo edges.

The same height difference drives the **photo-border dodge** described in
`/video-crypto-long`: a picture that fits the frame is pushed down (or slightly
scaled) so its hairline never crosses the mark, while a full-frame picture
is left alone. It reads the mark's real box rather than a constant, so this
159px lockup pushes a photograph roughly four times as far as the wordmark
does — which is exactly why it could not be a number in the source.

## The rule that outranks every production consideration

**No medical claims. Ever.** This is YMYL health content and the site's own copy
is careful; the video must be at least as careful.

- Describe what the article says and no more. `does-tinnitus-go-away` says
  temporary tinnitus often resolves, chronic tinnitus tied to hearing loss is
  *unlikely to disappear on its own*, and there is **no treatment that reliably
  removes it for everyone**. The script says exactly that.
- Never promise relief, improvement, or a cure — not even softly, not even as
  "this can help". Say what a thing *is* ("sound therapy makes it less
  noticeable"), never what it will do for the viewer.
- **Route to a professional**, and put the red flags on screen: lasting more
  than a few weeks, getting louder, one ear only, pulsing with the heartbeat,
  with dizziness or hearing loss. Those come from the article; do not invent
  additions.
- Put the disclaimer in `Meta.credits` so it lands in the description.

**Phonemes to avoid outright**: `ENT`, `CBT`, `TMJ`, `presbycusis`, `Meniere's`.
Every one is an initialism espeak mangles or a word it guesses at. Say "an ear
specialist", "talking therapy", "jaw problems", "certain inner-ear conditions" —
which is what they mean to this audience anyway. `tinnitus` itself is safe.

---

# Mode 2 — sound-therapy sessions

`video_automation/longform/asmr.py`.

```python
from video_automation.core import soundbed
from video_automation.core.brand import TINNITUS
from video_automation.longform.asmr import render_asmr_long

made = render_asmr_long(out, work, brand=TINNITUS, minutes=20,
                        bed=soundbed.Bed("pink", breathe=0.10, breathe_period=10.0),
                        intro=INTRO)          # spoken by luna-calm
```

## The bed is generated, not recorded

`core/soundbed.py` synthesizes white, pink, brown and green noise, with an
optional notch. **The album tracks the short was built on are gone from disk**
(like the Plovdiv footage), so this was going to be rebuilt regardless — but
generating it is better on the merits:

- **It removes the limitation the short skill records as unfixable.** Those two
  tracks put ~87% of their energy below 200 Hz and 0.1% above 4 kHz, so a high
  whistling tinnitus was never well covered — "a property of the tracks, not the
  method". Measured on the generated beds: pink runs 41/20/17/9/13% across
  <200 / 200–1k / 1k–4k / 4k–8k / >8k. White puts 67% above 8 kHz. The ceiling
  is gone.
- **Notched therapy is now possible** — the variant the short skill wanted and
  could not build. `Bed(notch_hz=6000)` cuts 35 dB at 6 kHz while leaving
  2 kHz untouched, measured. That is a real notch, not a dip; it is cascaded
  twice because one biquad is only ~20 dB deep.
- Any length, no loop seam, ours to license on every platform.

**Run `soundbed.band_energy()` on anything new before writing copy about what it
masks.** That is how the original limitation was found, and it is the only thing
standing between a description and an overclaim.

## The picture is a seamless loop — and everything must divide it

A 40-minute video is 72,000 frames of Python compositing. Instead one loop is
rendered and ffmpeg repeats it, so **render cost is fixed at the loop length**:
a 2-minute test and a 40-minute session both cost about 70 seconds.

That only works because the loop is genuinely seamless, which constrains every
moving element:

- The nebula drifts around a **closed circle**, period equal to the loop. A
  linear drift cannot return.
- **The breathing cycle must divide the loop** — 60s at a 10s breath is six
  whole cycles. `render_loop` raises rather than shipping the jump.
- **So must the watermark float**, so its period is derived from the loop, not
  inherited from the short's 5.5s.

Verified on a real render: mean frame difference **across the splice 1.038**
versus **1.348 for a normal mid-loop step** — the seam is less of a change than
an ordinary frame. Re-measure if any of the three periods change.

**The audio is never looped.** Noise is generated to the exact length, so the
one thing a listener would notice repeating never does. Loop what nobody watches
closely; generate what they are listening to.

## The intro

Thirty seconds of `luna-calm` at the front, then nothing. A forty-minute noise
file with no voice is indistinguishable from every other one on the platform;
the intro is where the video says what the sound is, who it is from, and **how
to set the level**. The bed sidechains under it and returns to full afterwards.

`luna-calm` and not `mia`: SOFT chain, unhurried, no pitch shift. An explainer
wants the reader who explains; this wants the one the listener settles under.

## Copy for a session

**The angle is partial masking**, straight out of
`brown-noise-vs-white-noise-for-tinnitus.mdx`: set the sound *just below* your
tinnitus so you can still faintly hear it. It is useful, counterintuitive, and
it is the reason to pick this video over any other noise video. Burying the
sound completely is what most people do and what the post argues against.

Same medical rule as mode 1, and it bites harder here because a session looks
like a treatment. It is a sound to listen to. Say that.

---


## Rules that arrived from the crypto side (2026-08-18)

All four of these are engine-level or cross-channel; they were found on
`crypto-exchanges` and they apply here unchanged.

**Silence is punctuation, and it has to be written.** `gaps` on the `Section`
(or the `gap` list in a short), one float per sentence. Leaving every sentence
at the default 0.34 is what "monotone" means — pace is the only prosody a
synthesiser has. 0.34 inside a thought, 0.45-0.60 at the end of one, 0.70-0.90
before a line that has to land, 2.10-2.40 for a two-phase beat. **Longer than
1.3 outside a beat is a hole, not a pause.**

**Music: `assets/brand/music/` is one library for both sites.** The tracks are
brand-neutral and the user's call is that a bed picked by ear beats a generated
one that only measures correctly. `music.track("night-drift")` is on both
channels now. Add another with `music.prepare_track`, which trims both ends —
untrimmed encoder delay becomes a hole in the bed once per loop.

**A ping-pong background must not fold at frame zero.** `pingpong` now drops one
frame from each end of the reversed half and `Backdrop.at` samples from a
quarter of the loop in, because a palindrome's turnaround is the one moment
motion stops and every video was opening on one. Only the crypto water was
affected — the aurora is generated on closed circular paths and has no fold —
but re-measure any new footage background the same way: step series over the
whole loop including the wrap, minimum must not land at a fold.

**Check phonemes with espeak rather than guessing.** Kokoro phonemizes through
espeak-ng, so `espeak-ng -v en-us -q --ipa "<word>"` is the whole check. It
caught a brand name that shipped mispronounced. Put any respelling in the
**spoken** half of a `(caption, spoken)` pair so the screen still reads
correctly.

**Thumbnails: three checks, every time.** The subject fits — no half faces at
the frame edge, and `_layout` now penalises a crop that cuts a detected face.
The type is not over the face — in 9:16 there is no search at all, so pass
`band="bottom"` whenever the head is in the top half of the crop. And the words
are the script's own words.

**Only a hyphen goes on screen.** Never an em or en dash in a spoken line or a
caption, on any channel — at caption size a long rule reads as a stray mark, and
it is a flourish in a place that wants plain type. Write `-`.

**A statement card needs a line handing off to it.** A full-screen card that
arrives with nothing in front of it reads as a title card dropped into the
middle of the video; one sentence makes it the thing the piece was building
toward.

**Two beats joined the portrait set**: `logos` (brand tiles, 2x2, optional
tick/cross badges) and `chapter` (a full-screen statement at 148px, which is the
strongest way a short can land its closing line). `compare` takes
`name_columns=True` in landscape, which makes each heading its own revealed item
so the graphic follows the voice instead of asking the viewer to interpret.

## Do not

- **Make medical claims, in either mode.** The one rule above all others.
- Write copy that oversells what a bed masks without running `band_energy`.
- Promote a candidate voice to approved. `mia` and `luna-calm` are both
  candidates.
- Present the app's zen albums as available — the audio files are not on disk.
- Mass-produce. Same cap as crypto: see `docs/long-form-strategy.md`.

## `bars` reserves a column for its values, and that was a real bug

**A bar at fraction 1.000 fills the track by definition, so its value label has
nowhere to go.** The halving chart's top row is `("2009", 1.000, "50 BTC")` and
it printed as **"50 BT" against the frame edge**: the old code clamped the
label's *start* x to ten pixels inside the track, which is a clamp on the anchor
rather than on the extent, so the rest of the string drew straight off the
frame. Nothing clipped it and nothing raised - the same bug class as a
`compare` row too wide for its line, and as marks scheduled past the last frame.

Two fixes were tried and only the second is right:

- **Moving that one label inside the bar does not work.** The value font is
  46px against a 30px bar, so a label set inside is cut off top and bottom; and
  one row treated differently from the other four reads as a fault rather than
  as a rule.
- **Shorten the track for every row instead.** `Bars.content` now measures the
  widest value in the payload and takes `that + 44px` off the track width
  before laying anything out, so every value sits outside its bar in one
  consistent treatment. It costs a few percent of bar length, which is
  invisible because bars are read against each other rather than against the
  frame.

Nothing to set per beat. **But if a beat ever draws type near an edge, check
whether the code clamps the anchor or the extent** - clamping where a string
starts says nothing about where it ends.


## A thumbnail may open the loop; it may not point at the wrong answer

**The off-message rule applies to the thumbnail, not just to the shots**, and
it outranks the scorer. `hacker.jpg` is the most arresting picture in the
crypto library - a hooded figure at a laptop, whole subject, real black beside
it for the type - and `_layout` scored it -0.15 against the shipped
`analysis.jpg`'s -0.07. It was still rejected: under the headline "Who controls
Bitcoin's price?" a hooded figure answers **hackers**, and that is a thing the
video explicitly denies.

That is a different failure from "never put the answer on the thumbnail". This
one puts *an* answer there and the answer is wrong, which is worse than
answering correctly - it sets the viewer up to click for a video that does not
exist and bounce.

Two more from the same sweep, both scored and both rejected on subject:

- `bitcoin-vs-fiat.jpg` is a man setting fire to a dollar bill. It promises a
  currency-collapse video.
- `gold.jpg` is the prettiest of the batch, scored best of all at -0.29, and
  says nothing about price at all.

So the order is: **score the batch, then read what each picture claims**, and
let the claim veto the score. The shipped choice promises what the video is -
a market being read.

## Telegram gets the long form, and only the long form

**Settled 2026-08-23, on both channels at once.** Every long-form video now
gets a link post in the site's Telegram channel - `@tinnitushelpme` here,
`@thecryptowiki` on the other - posted by the Publish Facebook Video workflow
once the video is live, or by the standalone Share Video To Telegram workflow
when it has to be retried or deliberately held until the video is public.

Shorts do not get one. They already reach Instagram, Facebook Reels and
TikTok, and a channel announcement per short is noise rather than reach - the
same reasoning that keeps a Short off the site registry.

`publish-video` carries the workflow ids, the form fields and the two silent
n8n traps that branch hit while being built.

