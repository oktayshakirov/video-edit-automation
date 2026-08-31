# The drawn beats

The drawn-graphic library both formats share - `bars`, `grid`, `steps`,
`checklist`, `compare`, `logos`, `chapter`. Rendering quirks that cost a re-cut
live in `troubleshooting.md`.

## The drawn beats carry the video

The arithmetic is in the strategy doc and it is the whole design: ~30 shots
against the 3–5 photographs a post actually has. Beats are not decoration here,
they are the majority of the runtime.

`chapter` · `checklist` · `stat` · `compare` · `quote` · `bars` · `grid` ·
`steps` — in `longform/beats.py`. The first six share a content column left and
a picture column right; `grid` and `steps` span the full width. Video clips
(`Shot(clip=...)`) and the end-screen sting are the two things that are not
beats; see `longform/clip.py` and `longform/overlay.py`.

- **Vary the layout across the channel, not just within a video.** The user's
  note on the mining rig cut was that every list in every video looks the same,
  and they were right: `checklist` and `compare` both set type in a left column
  with a ragged right edge, so a four-item list and a three-a-side comparison
  read as one graphic at a glance. Across fifteen videos that is the templated
  sameness the strategy doc says gets a channel suppressed. **The fix is
  silhouette, not decoration** — a different typeface or accent changes nothing;
  a layout with no left column and no ragged edge changes everything. Before
  building, list the beats you have chosen and check you are not using the same
  two shapes four times. Vary the item counts too.
- **`grid` is for a *set*; `checklist` is for a set with verdicts.** Cards across
  the full width, three to a row from five items up, two below that. Nothing is
  ticked or struck — if items need verdicts, that is a checklist. Each card takes
  an optional second line, which is where the wide layout pays for itself: "8 GB
  of memory" is far more useful with "enough for any mining OS" under it, and a
  list row has no room for that.
- **`steps` is for a procedure, and order is what it shows.** A numbered track,
  four or five nodes. This is the `timeline` the strategy doc listed and never
  built. "Install the drivers, install the miner, join a pool" as a checklist is
  three unrelated facts; on a track it is a sequence, and a how-to video is
  mostly sequences. **Numbers are right here and banned on a chapter card**, and
  the two are not in tension: a numbered agenda tells the viewer they are being
  lectured, a numbered sequence *is* the content.

- **`logos` is the beat for named brands, and it is not optional when the
  script names them.** thecrypto.wiki owns 27 exchange cards in
  `public/images/exchanges/` — full-bleed brand tiles, not transparent icons —
  and a script that reads "Coinbase. Binance. Crypto.com." over a stock photo of
  a trading desk is asking the viewer to hold three names in their head for no
  reason. One caption per tile times the reveals. A third element per item adds
  a tick or a cross into the tile's corner on a black disc, so the beat can be
  two-phase exactly like a checklist — which is what keeps a lineup an open
  question rather than a table. **It raises on a missing logo** rather than
  drawing an empty tile: PancakeSwap is not in the library and the first build
  drew a blank card and said nothing.
- **`compare` takes `name_columns=True` and usually should.** With it, each
  heading becomes its own revealed item, so the order on screen is the order in
  the mouth: "Centralized", three items, "Decentralized", three items. Without
  it both headings are painted at f=0 and the viewer has to work out which
  column the voice is on — the user's note was that a comparison must never ask
  them to interpret, and they are right. Write the heading as its own caption
  chunk. It is opt-in only because the shipped mining-rig cut is written
  against the old reveal count.
- **Three `grid` cards go in one column, not a 2x2 with a hole in it.** Handled
  automatically now; four still take the 2x2, which is a complete rectangle.
- **The split layout is why this is sharp.** A 900px source — the site median —
  in a 660px picture column is a *downscale*. Full-frame photos are the only
  place the upscale ceiling bites. **Do not "fix" a beat by giving its picture
  the full frame.**
- **`compare` is the beat to reach for first** when the article has an "A vs B"
  in it. 16:9 is a bad shape for a list and a very good one for a comparison.
  **It reveals the whole left column, then the whole right one** — the first
  version alternated sides and that can never match the voice, because a script
  covers one column and then the other. Interleaved, the second column started
  filling while the narration was still on the first, which reads as the graphic
  being out of sync. Write **one caption chunk per item, in column order, with
  no lead-in sentence inside the beat's span** — a spare sentence in front eats
  reveal 0 and shunts every item one line late. Three per column beats two: two
  looks like a stub.
- **`stat` is the best value per second in the format.** A figure spoken and not
  shown is a figure not remembered. Use it for the one number that matters, not
  every number in the paragraph.
- **One caption per item — and this is every beat, not just `compare`.** The
  beat's own sentence *is* the list: one caption chunk per reveal, in reveal
  order, nothing else in the span. `reveals` come from the caption starts of
  that sentence, so a line appears exactly as it is spoken. The quantum cut
  broke this on `steps` (a 5-node track under a three-chunk narrative sentence)
  and the beat filled in visibly out of sync with the voice — the user's "the
  visuals don't match the script" note, three times in one video. A
  `name_columns` `compare` counts its two headings as reveals too, so its
  sentence is 8 chunks for 3+3 items. Write the beat sentence as the enumeration
  first, then the setup and payoff sentences around it.
- **A `checklist` needs a ~2.4s `gap` on its own sentence**, or the verdicts have
  nowhere to land and `mark_times` compresses to nothing.
- A checklist with every item ticked is a legitimate use — a procedure that ticks
  through. `satoshi-proof.py` uses it for the four verification steps.

## A struck item has to explain itself

**The user's note on the quantum cut: a lone ✗ in a list is confusing —
"sometimes when we do this it is confusing. We need proper check for those
lists."** A cross draws the eye and then makes the viewer work out what it
*means*, and under a bare title ("WHAT A QUANTUM-SAFE SWITCH NEEDS") a struck
item read as "not needed" rather than "cannot be done". Two ways to fix it, pick
one:

- **Title the beat as the yes/no question the marks answer**, and with
  `flow=True` have the narration say each verdict out loud. `"CAN IT BE
  MIGRATED?"` with the voice reading "Doable. Doable. Doable. Never." makes
  ✓✓✓✗ exactly what was just said — the mark confirms the word, it does not
  carry the meaning alone.
- **Or make them all the same mark** — an all-✓ procedure, or an all-✗ list of
  faults — when the split is not actually the point.

The failure is a mixed list whose title is a noun phrase, so the marks are the
only thing saying which items are good and which are bad. Never ship that.

## Checklist: two timing modes

`flow=False` (default) is the shorts' original — every item appears unmarked, so
the list is a genuine open question, then the verdicts land together. It has a
payoff and needs a written pause.

`flow=True` marks each item as it is spoken, and exists for when the **script
carries the verdict itself**: "Not a court ruling." "Not a writing style." When
the narration is already saying no, holding the cross back four seconds puts the
picture behind the voice. Use flow when the narration tells, two-phase when it
asks. Third element of the payload tuple.

## `checklist`'s `flow` is a presentation choice — both modes are live on this channel

**Neither mode is the default to reach for. Ask one question first: does the
narration itself say the verdict on each item as it is spoken, or does it
only reveal the verdict afterward, as one reaction?**

- **The narration says it item by item → `flow=True`.** The silence short's
  checklist narrates "So earplugs make it stand out more. A soundproofed room
  does the same..." — each line *is* the verdict, spoken as its own claim, so
  marking it false the instant it is said matches what the voice just told
  you. Holding the cross back four seconds would put the picture behind
  words already spoken.
- **The narration states the claims flat, then reacts once → `flow=False`
  (the default, `flow` simply omitted).** The myths short's checklist reads
  three claims with no verdict attached to any one of them ("Only loud noise
  causes it. It always goes away on its own..."), so `flow=True` there marked
  each false before the narration had said anything was wrong — the crosses
  answered the question before the voice asked it. Two-phase leaves every
  item unmarked while all three are read, then lands the verdicts together in
  the pause after the last one, which is where a single reaction line
  ("Turns out, none of that is true") gets written in — see below.

**Decide this per section, not per channel.** Both shipped on this channel
correctly; the fault was never in the beat, it was in applying `flow=True`
as a habit rather than checking which shape that section's script actually
has.

**A reaction line can be written into the same sentence, timed for free.**
"Turns out, none of that is true" was added as a fourth caption chunk on the
same three-claim sentence, after the three real items. `item_count` reads
`len(items)` from the payload (3), so the fourth chunk claims no reveal slot
— it is just more words the voice says inside the shot's own hold, landing
in the pause where two-phase mode already draws its crosses. No new shot,
no marks= override, no timing math: the existing two-phase mechanism and an
extra chunk did the whole thing.

**A hinge into a plain-narration list belongs in the same sentence as the
list, not a separate one.** "So here are some real reasons" was prepended as
the first chunk of the sentence that names the causes, rather than shipped as
its own sentence with its own gap — cheaper, and it reads as one breath
rather than a title card announcing a list. This is the long-form hinge rule
("the beat's own first chunk also has to sound spoken") applied to a beat-free
line: any list a script hands the viewer cold benefits from the same fix.

## `bars` — the beat for a proportion

`payload: ([(label, fraction, value_text), ...], title)`. `stat` shows one
number and `compare` shows two lists; neither can show a **proportion**, and a
proportion is the one thing a spoken number cannot convey. "One point one
million coins" means nothing without the supply; drawn against 21 million it is
instantly legible and needs no second sentence.

## A number needs its own meaning on screen

`stat` shows one figure large. That works when the figure *is* the point ("0
times passed", "1.1M coins") and fails when it is a count of things the viewer
cannot see — a bare "5 / SIGNS TO ACT ON" tells nobody what the five are, and it
sits in one corner with the rest of the frame empty. If the narration at that
moment is naming items, use a `checklist` of those exact items instead. The rule
is the general one: **show what is being said, not a summary of it.**

## Fill the right column, always

A `stat` or a `quote` with no `picture=` is a short block on the left and 40% of
a 16:9 frame showing nothing. `Beat.EMBLEM` draws counter-rotating concentric
arcs there instead — deliberately abstract and low contrast, there to balance
the composition and give the eye something moving, not to mean anything. On by
default for `stat` and `quote`; a `checklist` or `compare` already spans the
frame and does not need it.

## A year never counts up

`Stat` animates numeric values, but suppresses it for a bare four-digit year in
1900–2100. "2009" racing from zero spends most of the beat showing 1200, 1780,
2001 — all plausible years, all wrong, and a viewer reads the wrong one as an
error rather than as an animation. Counting is for magnitudes, where the
intermediate values are obviously partial.

## Give a beat time to be read

A drawn beat whose sentence is short gets a shot that is gone in under two
seconds. If a beat carries the line the video is built toward, buy it a pause
with the sentence's `gap` — the outro's "Did they sign?" takes 2.40.

## `logos` groups, when the split is the point

`payload=(items, title, groups)` where `groups` is `[(heading, count), ...]`.
It puts a centred heading over each run and forces a single column, and the
heading arrives with its own first tile rather than at f=0 — same reasoning as
`compare(name_columns=True)`. Two crosses and two ticks in a 2x2 still leave the
viewer inferring what the sides mean; `CENTRALIZED` over the first pair and
`DECENTRALIZED` over the second says it. **Drop the per-tile labels when you
group** — with a heading standing over the pair, "they hold" under each card is
the same fact twice, and the column has less room than the grid did.

**Marks only exist for beats `build` knows carry verdicts.** `logos` was added
with tick/cross badges and they rendered perfectly in an isolated draw and never
once in a built short, because the mark times were computed for `checklist`
alone and `marks` stayed None. If a new beat takes verdicts, wire it into both
`crypto/build.py` and `longform/build.py`, and read the verdict as the item's
**last** element — a checklist row is `(text, ok)` and a logo tile is
`(slug, label, ok)`, so the cue builder's fixed unpack raises on one of them.

## The vertical `checklist` draws the brand background now

`ChecklistShot` was the last drawn object still painting the ruled drifting
grid — `int((f * 40) % 96)`, the whole-pixel step everything else in this repo
was fixed for. It was missed when `core/backdrop.py` replaced the grid
everywhere else, because `render_shots` builds it directly rather than through
`longform.beats`, so it never saw a `Brand.backdrop`.

The symptom that found it: a tinnitus short whose `checklist` drew a navy grid
and whose `bars` ten seconds later drew the brand's own loop, in one 44-second
video. **Shipped crypto shorts that use `checklist` will look different if
re-rendered** — that was accepted deliberately, since the grid was already
documented as removed from both channels.

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

## Grid icons are 64px in landscape, not 46

A two-column `grid` card at 1920 is about 880px wide, and a 46px glyph in the
corner of it read as a smudge. The whole point of the icon is to be legible
*before* the label is. Portrait stays at 54, where the card is narrower and
the glyph is already proportionally larger.

## Screen an emoji against the card, not against your editor

**The plug glyph (U+1F50C) shipped into the proof-of-stake short and all but
vanished.** It renders as a dark grey object, and on a near-black card at the
size a `grid` icon gets, there was nothing to see. This is the same failure the
tinnitus skill already records for the stethoscope (🩺, near-black) and the
microbe (🦠, bright green) — it just arrived on a different glyph, because the
check being made was "is this the right *idea*" rather than "is this legible on
this ground".

So the rule for both channels' dark palettes: **an icon must be bright and
saturated, or it is not an icon.** Yellows, golds and oranges sit with the
brand and read instantly; greys, browns and dark blues disappear. On the
proof-of-stake pair the survivors were 🔒 🎲 📦 🗳️ 💰 on the `steps` track —
two of them gold, all five legible before their labels — and the fix in the
short was 🔌 → 😴, which is brighter *and* says "offline" more directly.

Check it on a rendered frame, never on the character in a code editor, where
everything sits on white.

## A diagram goes on a pre-composed slide, not into a `Shot`

**Refinement of the rule above, found by shipping it wrong once.** Removing the
Ken Burns move is necessary and *not sufficient*. `Shot(image=DIAGRAM,
zoom=1.0, pan=(0,0), aspect=<source ratio>)` still rendered with the diagram's
title clipped off the top.

The cause is the cover/fit boundary. `PhotoShot` scales to **cover** the frame
and only falls back to a fitted panel when the source cannot reach that size
under `max_upscale`. The site diagram is 1000x667: covering 1920 needs 1.92x
against a 1.90 ceiling — close enough that it filled the width and then cropped
~90px off the top and bottom to make the height fit. A slightly smaller source
would have rendered fitted; a slightly larger one would have covered cleanly.
This one landed exactly in the gap, which is the worst place to be.

**So do not try to land in the gap. Take the frame out of the equation:**

```bash
.venv/bin/python tools/make_slide.py <diagram> assets/brand/slides/<name>.jpg --brand crypto
```

`tools/make_slide.py` centres the diagram on a 1920x1080 brand-coloured canvas
with a 6% margin and the brand hairline. The asset then bleeds off all four
edges *by construction*, so no crop is possible at any `max_upscale`, and the
diagram gets room to breathe rather than being read at the frame edge.

The general lesson, worth more than the diagram: **when a renderer has two
behaviours and a threshold between them, do not tune an input to sit near the
threshold.** Move the input clearly to one side — here by making the source
frame-sized, so "cover" and "fit" are the same operation.

In 9:16 none of this applies: use `ImageOverlay` and keep the footage moving
underneath. See the short's skill.

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

**The starfield failed the rule this doc already carried, and the file had
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

This replaced a ruled grid that drifted behind every beat on both channels -
why it went, and the judder that gave it away, is in `troubleshooting.md`.

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
