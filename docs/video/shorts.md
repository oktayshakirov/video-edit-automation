# Vertical engine (9:16)

Shorts, Reels and TikToks. One engine for every project - what changes per
project is the voice, the source material and the safety rules, not this.

## Four beats transfer to 9:16 now, not two

`checklist`, `grid`, `steps`, `bars` — and **`logos` and `chapter`**, added on
the crypto-exchanges short. Everything else still raises, which is the honest
answer: the landscape beats lay a content column beside a picture column at
1920 and have no portrait layout.

**`logos` is the beat for named platforms.** The site owns 27 exchange brand
cards in `public/images/exchanges/`, and in portrait the beat lays them 2x2
rather than stacking four (a stacked tile is 240px tall and its wordmark stops
being readable at arm's length). A third element per item lands a tick or a
cross into the tile's corner after the names are read, so it keeps the
checklist's two-phase payoff while being a completely different silhouette.

**A judged lineup needs balanced sides.** The first cut of this short listed
Coinbase, Binance, Crypto.com and Uniswap and marked three crosses and one
tick, and the user found it confusing — correctly: with a single tick at the
end there is nothing to say the tick means *decentralized* rather than "the
best one". Two and two, with the labels spelling out which is which, makes the
split the subject. **Check the site actually owns the logo first** — the
obvious fourth name was PancakeSwap and the site has no card for it, so the
beat raises rather than drawing a blank tile; `hyperliquid` is the site's own
second non-custodial exchange and carries real `quickFacts`.

**`chapter` is a full-screen statement, and it is the strongest way a short can
land its closing line.** It wraps to the frame and centres on both axes; in
9:16 it sets at 148px rather than the landscape 108, because 108 across 1080 is
body copy with two thirds of the frame empty around it. It burns no caption
over itself — `build` already suppresses captions on any shot with a `graphic`
— so pass the on-screen wording in the *caption* half of a `(caption, spoken)`
pair and the spoken wording in the other, and the card can be in capitals while
the voice reads a sentence.

## Stock is allowed now, and motion is the point

**This reverses "do not reach for a stock API", which this doc used to state
flatly.** The reversal was made on the mining rig short: it was built from eight
site photographs exactly as the rule required, and the user's verdict was that
it looked boring and not engaging. Both halves of that were true and neither was
a scripting problem.

- **Eight Ken Burns pushes in a row is one move repeated eight times.** A slow
  push is a good way to make *a* still photograph feel alive and a bad way to
  build a whole piece, because the variety a viewer perceives is variety of
  *shot type*, not of subject. Two photographs of different things moving
  identically read as the same shot twice.
- **The library often has no picture of the subject.** thecrypto.wiki owns no
  photograph of a graphics card, a riser or a power connector — so a short about
  mining hardware was illustrated with a server room, a neon bitcoin and an
  abstract orb. Generic pictures are what "boring" actually meant.

So the long-form rule now applies here too: **stock supports; the site's images
and the drawn beat lead.** The failure the old rule protected against is real
and unchanged — wall-to-wall stock loops under an AI voice is the pattern both
platforms suppress — but that is an argument about *proportion*, not about
whether a clip may appear at all. Half the shots is comfortable. All of them is
the failure.

- **Open on motion. Frame one is a clip, not a still.** A Short is judged in its
  first second, so this matters more here than in long form, not less.
- **`Shot(clip=..., clip_at=...)` now works in a short.** `render_shots` has
  taken a `factory` since long form needed one and the shorts simply never
  passed one, so a clip in a short used to render as an empty checklist rather
  than raise. `crypto/build.py:_short_factory` wires it up.
- **A clip in a short carries no label.** Long form puts a big centred statement
  on a clip because it burns no captions; a short burns one on every line, so a
  label prints the same words twice. `_short_factory` forces `label=None` — the
  same rule, and the same reason, as a drawn beat carrying no captions.
- **A clip is full-bleed; a photograph is a framed card.** That contrast is
  doing real work — it is what makes the alternation read as rhythm rather than
  as inconsistency. Do not "fix" it by framing the clips.
- **Screen every candidate, and screen a clip across its length.**
  `stock.screen(path, at=)` takes a timestamp. `MAX_LUMA=48`, `MAX_SAT=50`.
  `crypto-mining-rig-hardware/854969.mp4` measures L27 on frame one and **L88 by
  second six**; a single-frame check ships it.
- **Hue is a separate judgement the numbers do not make.** `data-center.jpg`
  passes the box at L41 and is green-lit, which is the one colour that cuts
  hardest against gold.
- **A landscape clip is centre-cropped hard into 9:16** — you see roughly the
  middle third. Pick clips whose subject is centred; a wide establishing shot
  loses its subject entirely.
- Cached stock is gitignored and `assets/stock/manifest.json` is what makes a
  build reproducible. Anything pulled must land in it.

**`grid` and `steps` transfer, but only because they were given real portrait
layouts.** Scaling the landscape versions gives a 293px card and a 216px step
slot, which is why they were briefly recorded here as untransferable. What they
have instead:

- **`grid` drops to one column** up to four items, two beyond that, with larger
  type. Wide cards down the frame, which is the axis 9:16 has to spare.
- **`steps` turns its track ninety degrees.** Nodes down the left, labels to the
  right. A vertical sequence is if anything the more natural reading order, and
  a 9:16 frame has height to spare and no width at all.

**Use them to stop every list looking the same.** A short with two drawn beats
should not use `checklist` twice — the mining rig cut pairs the judged list with
a `steps` track for the fix, and they read as two different graphics rather than
as the same one repeated. `steps` is the right beat whenever the content has an
order, which a how-to usually does.

**Cut between a drawn beat and a clip; keep dissolving into a photograph.** A
clip is full-bleed and already moving, so a half-second dissolve slides the
beat's type across travelling footage and reads as a rendering fault. This is
automatic in `render_crypto_short` in both directions and only where a clip is
involved.

**Never put a site infographic in a shot.** A 9:16 crop takes its title off the
top and its last row off the bottom. `proof-of-work.jpg` is the most on-topic
file in the crypto library and is unusable for exactly this reason.

## A statement card needs a line handing off to it

A full-screen `chapter` card that arrives with nothing in front of it reads as a
title card dropped into the middle of the video. One sentence turns it into the
thing the piece has been building toward — "Always remember the golden rule."
before "Not your keys, not your coins." This is the same note the instruction
list got, and it generalises: **anything that changes the register of the video
needs a sentence saying why it is happening.**

## The picture

**Blurred-fill layout, because the site's images are small.** Most are 700-1200px
and all are landscape, so none can fill 1080x1920 without a 3x upscale. The image
is scaled to cover the frame, blurred hard and dimmed to 42% as a backdrop, with
the sharp copy laid over it. The frame is full of picture and nothing is upscaled
past `MAX_UPSCALE = 1.45`.

- **Crop toward a taller shape first** (`aspect`, default 1.15). At full width a
  landscape source occupies about a third of a 9:16 frame and the rest is blur;
  cropping in gives it half or better. How far it can crop is bounded by
  resolution, not taste — cropping narrows the source and raises the upscale, so
  `MAX_UPSCALE` wins and the aspect target yields.
- **Do not use a source under ~750px wide.** Below that, `MAX_UPSCALE` leaves the
  photo as a small rectangle floating in blur. `crypto-ogs/satoshi.png` (400px)
  was tried and swapped for `posts/hacker.jpg` (996px).
- **The gold hairline spans the photo, not the frame.** Drawn full width it read
  as a band the picture had failed to fill.
- Backdrop and sharp layer pan in opposite directions at different rates — that
  separation is what makes a still photograph read as a shot. Subpixel, as
  everywhere in this repo.
- **Dissolve between shots** (`XFADE = 0.45`), do not cut. The piece is one
  continuous argument; a hard cut every five seconds fights the voice.

**`ChecklistShot` is the beat that earns the format.** A list that fills in on
the voice and is then judged, ending on the one item that is ticked. It shows
the argument instead of illustrating it, which is the difference between this
and stock-footage-with-narration.

- **A drawn beat carries no captions at all.** `build.py` suppresses them for
  any shot with a `graphic`. The items *are* the type — larger, and in the
  middle of the frame — so a caption underneath restated the exact line being
  spoken at that moment: the same words twice, in two places, and neither one
  where the eye should be. The voice still speaks them and the caption times
  still drive `reveals`; only the burn goes. This is automatic, not something
  the script has to remember.
- **Two phases: options first, verdicts after.** The items appear unmarked as
  they are spoken, so for a few seconds the list is a real open question; then,
  in the pause after the last option, the marks land one at a time — cross,
  cross, cross, tick. Marking each item as it arrived answered the question
  before it had been asked and the beat had no payoff. The tick is held back to
  **1.7 steps** after the last cross: a payoff needs the beat before it to be
  longer than the beats between the things it settles.
- **`flow` is the third payload element, and it exists for narration that says
  the verdict itself.** `payload=(items, title, True)` marks each item 0.30s
  after the word that names it, instead of holding every verdict for the pause.
  Use it when the script reads "Not the graphics cards. Not the power supply."
  — there, a cross held back four seconds puts the picture behind the voice.
  Keep the two-phase default when the narration only *lists* and the marks are
  the answer. A `flow` beat needs a much shorter gap (1.2s, not 2.1s): the
  silence that used to buy room for the marks is now dead air.
- **The question goes in the sentence before the beat, never inside it.** A
  checklist times its reveals off the caption starts of its own sentence, so a
  lead-in line inside that span eats reveal zero and shunts every item one line
  late. Ask it at the end of the previous sentence and the list has something to
  be an answer to — which is also just clearer, and was a review note.
- **The pause is bought with a per-sentence `gap`.** `gap` accepts a list, one
  per sentence; a checklist sentence takes ~2.0s against the usual 0.34 and the
  verdicts land in that silence. Without it there is no room and `_mark_times`
  compresses to nothing.
- **Anchor mark times on the last option's caption `start`, never its `end`.** A
  sentence's final caption is deliberately stretched to where the next sentence
  begins, so its `end` *is* the end of the shot. The first build of this beat
  anchored there, scheduled every mark past the last frame, and drew no verdicts
  at all — a bug that is invisible unless you actually look at the frames.
- **Marks and strikes draw on over ~0.16s**, and the marks are partial polylines
  (`_partial`) rather than whole shapes appearing. At this size an instant
  strike-through reads as a rendering glitch.
- **Reveal on caption starts, not on even fractions of the shot.** `build.py`
  fills `reveals` from the sentence's own caption times. Even fractions look
  synced until you watch it, and then every item is a beat early or late. Write
  the sentence with **one caption per item** and it needs no tuning.
- **White ink for every item, struck or not**, with a 3px black stroke. Grey-on-
  dark was shipped once and was not readable on a phone — the strike-through
  already says "this does not count", so the ink does not have to say it again by
  being harder to read.
- **Draw it over a dimmed photograph, not flat black.** A flat panel in the middle
  of a photo-driven piece reads as the video having stopped. `0.30` brightness was
  tried and was indistinguishable from black; `0.5` is the working value.
- Marks are **drawn from line segments, not set as glyphs** — Futura has no ✓ or ✕
  and PIL renders both as tofu, which is invisible in review and obvious in the
  frame. The happy accident is that a path can be drawn *partially*, which is
  what makes the draw-on above possible at all.

## Every short opens by asking its own title question

**The user's standing instruction, from the silence pair.** A short that opens
on the first line of its argument reads as random and confusing, and the
reason is structural rather than stylistic: a Short arrives with **no title
card, no thumbnail on screen and no chapter list**. Long form gets a title
stamp around eight seconds in and a description under it; a Short viewer has
literally nothing but the first sentence.

So the first line is the question the video answers, said plainly - "Does
silence make tinnitus worse?" - over the opening face, not over a card. It
costs about two seconds and it turns the next forty into an answer somebody is
waiting for. Budget for it: the format's 40-50s window did not move.

## A vertical cut must be cropped onto its subject

**`Shot(clip_ax=, clip_ay=)`**, fractions of the leftover cover-crop slack
exactly like `render_thumb`'s `crop_at`. 0.5 is centred and is what every clip
did before this existed, so nothing that does not set one changed.

It exists because a **16:9 source into a 9:16 frame keeps about 32% of the
width**, and `VideoShot._prepare` took that slice from the middle with a hard
`// 2`. The user's note on the silence short was the whole problem in one
line: "if there is a person we dont see it, if there is object we dont see
it". Its closing shot was a man standing at 0.80 of the source frame, so the
video ended on a brick wall and a plant with his shoulder clipped at the edge.

**The workflow is one contact sheet.** Pull a frame from every clip in the
cut, draw the centred crop band on it (31.6% of the width at the default
zoom) and decile ticks along the bottom, and read the subject's position off
the ticks. Then `ax = (cx * 3617 - 572) / 2474` for a 1920-wide source at the
default 1.06 zoom, or just sweep two values and look. It is inert in 16:9,
where a landscape source throws away almost nothing - **this is a shorts
problem, and every short should be checked for it.**

## Do not open two shots in a row on the same clip

The silence short's opening question and the line after it were both on
`tired-woman-hands-on-face/4867379`, because the question was added in front
of an existing opener and the obvious thing to do with a new first shot is
give it the picture that was already there. Six seconds on one face, and the
second shot landed mid-yawn. A Short's first two shots are the two the viewer
actually decides on: **give the question the face and the line after it the
room.** The same clip may come back later at a different `clip_at`; it may not
run twice consecutively.

## Check the 9:16 crop of every clip, not just its brightness

Two shots in the myths short's first pass were cropped onto the wrong thing —
the closing portrait landed on the subject's hair because the clip's first
seconds have her head down, and the meditation clip showed an empty brick
wall because the man stands at ~0.8 of a landscape frame. Both are the rule
this doc already carries ("a vertical cut must be cropped onto its
subject"), and both were missed because the *clip* had been approved on a
landscape contact sheet.

**A landscape source loses about 68% of its width in 9:16, so approving a
clip is not approving a shot.** `clip_ax` places the crop and `clip_at`
picks the moment; both have to be set per slot, and the only way to check is
to pull frames from the rendered file.

Everything `longform.md` now records about clip casting is true in
9:16 and some of it is worse: **no clip more than twice, never twice inside a
minute, nothing held past about eight seconds, and adjacent Pexels ids are
the same shoot.** The myths short's first cut opened on the same over-used
studio clip the long form opened on and then used it again two shots later —
so the note the user gave on the long form landed on both files at once.

**When the pair is built from one post, deliberately share the opening
face.** The myths short opens on the same low-key portrait the long form
opens on, which is the same argument the shared thumbnail already makes: a
viewer who sees both should recognise the second one.

## Per-word karaoke captions, on by default

**`karaoke=True` is the default on both `render_crypto_short` and
`render_tinnitus_short`.** The word being spoken is lit in `brand.primary` at a
slight scale while the rest of the phrase stays white - what every short-form
platform's own auto-captions do, and what the user asked for ("a lot of tiktok
videos do this"). Asked for on the tinnitus channel first and shipped there as
the default; flipped on for crypto 2026-08-27 after the drone stack-vs-cuts A/B,
same instinct - give the viewer more to track on screen. Pass `karaoke=False` to
opt out on a specific short.

`core.vertical.render_caption_karaoke` draws one frame per word and
`crypto/build._karaoke_sprites` emits one sprite per word.

**Five things are load-bearing, all found by building it:**

- **The layout is measured once at the base size and never re-flowed.** The
  active word is drawn larger *about its own centre, inside the advance the base
  font reserved for it*, so no other word moves. Re-measuring the line with one
  word enlarged makes the sentence twitch sideways on every syllable, which is
  much worse than no highlight at all.
- **`grow` is 1.08, not 1.14.** The enlarged word overhangs its box by half the
  difference each side, and at 1.14 - tried first - a long word visibly touched
  its neighbours, because the inter-word gap at caption size is a single space.
  The colour carries most of the "this word is live" signal; the scale only
  keeps the highlight from reading as flat.
- **`CaptionSprite` needed per-sprite `fade_in`/`fade_out`.** Every sprite used
  to run the same 0.13s scale-and-fade entrance, which on a per-word caption
  re-fires every syllable and cross-dissolves the phrase against a
  near-identical copy of itself - a soft flicker that reads as a broken render.
  Only a caption's first word frame animates in and only its last animates out;
  the ones between hard-cut.
- **Word timings are apportioned, not aligned.** `_word_spans` splits a
  caption's span by `len(word) + 1`. The chunk boundaries either side are real
  DTW timestamps and a chunk is three to six words, so drift stays under a
  syllable. Aligning per word would mean synthesising every word of the script
  alone as a timing reference.
- **Use `Caption.speech_end`, never `Caption.end`, as the stop point.** This is
  the one that shipped broken - see below.

**It shipped with a real, visible lag on every word.** The first cut tried to
recover "where the voice stops" by scanning forward for the next caption's
`start` - but `.end` had already been stretched to exactly that value by the
hold-until-next rule, so the scan was circular and every word lit late, worst on
a short sentence with a long trailing gap. `speech_end` is set once in
`Caption.__post_init__`, before the stretch loop runs, and is the only way to
get the pre-stretch boundary back. **Read this before touching
`_karaoke_sprites` again.**

**Confirmed fixed on the tinnitus channel's fifth myths cut** - checked against
the actual audio with a `silencedetect` pass on the mixdown rather than by
eyeballing frames.

Captions carrying an emoji keep the single-PNG treatment, because
`add_caption_emoji` re-centres the whole line around the glyph, which the
per-word layout does not model.

## A caption clears during the between-sentence pause

**A short caption goes up with its first word and comes down just after the
voice stops** — `voiceover.caption_window`, `CAPTION_GRACE = 0.15`. It is no
longer held across the scripted `gap` to the next sentence the way
`build_narration_aligned` stretches `Caption.end` for long form. On a phone a
held line sitting through a second of silence — worse, a karaoke word left lit
with nothing being said — reads as a stuck caption, not as a beat. This is what
every platform's own auto-captions do. Music laid over the render by hand fills
that silence, so the cleared frame is not dead air.

**The boundary itself is now pinned to the voice, not to the DTW estimate.**
`_pad_pause` returns where speech actually stops and resumes around each
internal sentence break; `build_narration_aligned` ends the last chunk there
and starts the next one there. Kokoro's own between-sentence pause is often
already longer than the scripted gap, and DTW smears that silence across the
boundary — which used to start the next caption (and its karaoke highlight)
half a second early, right after a break. This was the drone Berlin stack's
"karaoke doesn't match after the short break". The fix is in the shared
builder, so it covers the crypto and tinnitus shorts too. It also tightens
long form, where the next sentence's caption no longer appears during the
outgoing one's trailing silence — display stays continuous there because long
form does not use `caption_window`.

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

## A `backdrop=` on a vertical beat is dimmed to 0.5, and that is not enough

**`ChecklistShot` multiplies its backdrop by 0.5**, so a site photo at L172
(`young-tinnitus.jpg`, and most of this library) still arrives at **L86**
behind peach type — a pale, blurry wall filling a 9:16 frame, brighter than
anything else in the cut. It shipped into the myths short's first pass and
was obvious the moment the frames were looked at.

This is the long skill's "a blurred backdrop does not rescue a bright
picture, it spreads it" rule, in the one place that rule was not yet written
down. **On this site, default to no backdrop at all** — the drawn beats are
designed against `tinnitus-plum`, and a flat brand panel is what makes the
type pop. A backdrop is only worth it for a source already near L25, which on
this library means a stock clip's frame rather than a site photo.

Note the asymmetry with long form: there the same file goes in `picture=`,
the beat's own column, where it is a *downscale* at 660px and reads as a
deliberate inset. `backdrop=` and `picture=` are not interchangeable.

## `ImageOverlay` — a still over the footage, for the space 9:16 has spare

**Built for the proof-of-stake short.** The note was that the opening shot has
empty space above the footage and the site's own architecture diagram should
sit in it — "just overlay it". Nothing in this format could do that: a shot is
either a photograph *or* a clip *or* a drawn beat, and the only thing that had
ever composited over a finished frame was the subscribe sting.

`longform.overlay.ImageOverlay` is that sting's sibling, and
`render_crypto_short(..., overlays=[...])` now passes them through. Same
protocol — anything with `.draw(pic, t)`.

```python
from video_automation.core.frame import VERTICAL
w = int(VERTICAL.w * 0.86)
overlays = [ImageOverlay(DIAGRAM, 3.0, 7.8, frame=VERTICAL, scale=0.86,
                         at=((VERTICAL.w - w) // 2, 380))]
```

Three things it settled:

- **Opaque, not screen-blended**, which is the opposite of `ClipOverlay` and
  deliberately so. A screen blend leaves *pure black* transparent, which is
  perfect for a glowing button — but a diagram's ground is a dark **grey**, so
  screen-blending one lifts the footage under it everywhere and prints a
  washed rectangle. An opaque panel with the brand hairline reads as an inset.
- **Place it by hand in 9:16.** The class default sits a panel at 0.16 of frame
  height, which collides with the watermark at y=268. y=380 clears the mark,
  sits above the photo band, and leaves the caption line at ~0.80 alone.
- **The window is in absolute seconds**, so it is set before the narration is
  measured. Give it a generous span around the shot it belongs to and check the
  render, rather than trying to predict the boundary to a tenth.

This is the 9:16 answer to the long form's "an infographic is banned from a Ken
Burns shot, not from the video". Landscape shows the diagram as a fitted slide;
vertical lays it over moving footage and keeps both.

## `CaptionSprite` takes per-sprite `fade_in`/`fade_out`

**`CaptionSprite` now takes per-sprite `fade_in`/`fade_out`.** Defaults are
unchanged, so nothing shipped moves. It exists for per-word karaoke captions,
where the shared 0.13s entrance would re-fire on every syllable and
cross-dissolve the phrase against a near-identical copy of itself.

## A drawn beat in a short needs a hinge sentence in front of it, exactly like the long form

**The caffeine short listed its `grid` cards with no lead-in and the user's
note was that it "starts listing the 4 bullet points without good transition
... Make sure we have good flow always before listing those things like we do
in the long."** The long form's "say the point, then show the graphic" rule
(`longform.md`) applies here in full - a short is not exempt because it is
short.

**The hinge cannot ride inside the beat's own sentence.** `crypto/build.py`
fills `reveals` from the *first N* caption starts of the beat sentence
(`n = len(payload[0])`), so a hinge chunk prepended to a 4-item `grid`
sentence takes reveal 0 and shunts every card one caption late - the same
"eats reveal zero" failure `checklist` has. So the hinge gets **its own
sentence and its own `Shot`**, sitting immediately before the beat:
"And caffeine is rarely the only thing pushing it. It stacks with everything
else." then the grid.

A trailing *reaction* chunk is still fine (it claims no reveal slot); only a
leading hinge is the problem. When the sentence before the beat already does
the setup work ("If you want to test it, do this." before a `steps`), no
extra sentence is needed - check whether the flow is there before adding one.
