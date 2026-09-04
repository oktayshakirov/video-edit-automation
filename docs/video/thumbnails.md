# Thumbnails

One per video. A Short's is vertical and a long's is 16:9, and when both come
from one article they share a source image.

## `render_thumb`, and what it does not take

`render_thumb(headline=, subline=, image=, accent=)`. **No zoom, no focus, no
watermark** — the first two are searched and the third was removed.

## The landscape headline fills the empty half vertically — many big rows, not two small ones

**The user's rule, from the Ruja pair, against a reference set (The Code
Report's "WHERE / DID THE / MONEY / COME / FROM?").** A headline sitting small
in one or two lines with dead space around it looks amateur; the type should
grow until it fills the empty half top to bottom, wrapping to four or five
short rows. `_headline` now does this: a **narrow column** (`W * 0.46`) plus a
high starting `size` forces a big font into short wrapped lines, then it shrinks
only as far as `max_lines` / `max_block` / the one-accent-line rule require.

Two things this needs from the caller:

- **The accent must be ONE word.** A two-word accent (`[never existed]`) cannot
  both stay on one line and be large in a column this narrow, so the size
  search collapses back to two small lines. Bracket the single word that
  carries the tension: `"The coin that never [existed]"`, not `"The coin that
  [never existed]"`.
- **A short headline still wants to be 3–5 words.** Very short ("KIMI fallout")
  is fine, but a two-word headline in a narrow column is one word per line and
  looks thin. Aim for a phrase that naturally breaks into four rows.

**`render_short_thumb` is unchanged** — its column is full-width, `band`-placed,
and two lines clear of the face is the right look there. Do not carry the
narrow-column change across; a 9:16 thumbnail that fills vertically runs its
type over the subject. The pair can use a one-word accent on the long and a
two-word accent on the short and still read as a set.

**When the user asks to make a thumbnail bigger or realign it, do not also
change the words.** Text is a separate decision. Bring back the previous
headline and change only the layout.

- **Brackets mark the accent phrase**, which gets a solid vibrant box:
  `"Nobody has [passed it]"`. Every reference thumbnail that works does this;
  the box is what the eye lands on first, and a headline with no focal word is
  a wall. `accent` is `red` / `yellow` / `orange` / `blue` / `cyan` —
  deliberately **not** the brand palette, which is low-contrast against the
  channel's own dark imagery and disappears in a grid.
- One box per *run* of accent words, not per word. Per-word boxing leaves a seam
  of background between them and reads as a rendering fault.
- **The accent must land on one line**, and the size search enforces it: it
  takes the largest size at which the whole accent run sits on a single line,
  falling back to merely fitting if no size does. An accent that wraps draws two
  plates on two lines and loses the single focal point the device exists for.
  Nothing to tune per thumbnail.
- **The box is sized from the cap band**, not the line box, so uppercase sits
  optically centred in it. A font's line box carries ascender and descender room
  that caps never use, and padding that left the words riding high in the plate.
- **No subline.** A second smaller line under the headline was tried and cut:
  the headline is the whole hook, and a subtitle competes with the video title
  sitting directly beneath the thumbnail anyway.
- **Ask what the title does not.** The title carries the search phrase; the
  thumbnail spending its words on the same question wastes half the click
  decision. `Does Tinnitus Go Away?` as the title, `Which kind do you have?` on
  the image.
- **No watermark.** The channel name is already under the thumbnail everywhere
  it appears; a mark on the image is a tell of a template.
- **The scorer loses to the subject.** `render_long(thumb_side=)` overrides the
  searched side, and on Saylor it was used: the two sources that scored clean
  are him twenty years ago, and a thumbnail is a promise about who the video is
  about. The +0.91 on the shipped one is a studio backdrop's lettering, which
  the eye reads as a flat blue field. Look at the render before believing
  either the score or the override — but note that **all three thumbnails so
  far ship overridden**, which says as much about the scorer as the pictures.

### Check three things on every thumbnail before shipping it

The user's standing list, from reviewing the crypto-exchanges pair:

1. **The subject fits.** Half a face against the frame edge is not a promise
   about who the video is about. `_layout` now penalises a face the crop cuts —
   compared against the *clamped* box, because the cascade routinely returns a
   box running off the source and testing the raw one made every candidate
   equally clipped, so the penalty discriminated between nothing.
2. **The type is not over the face.** Landscape: the scorer already treats that
   as fatal. Vertical: it does not search at all, so pass `band="bottom"`
   whenever the subject's head is in the top half — which is most crops of a
   landscape source.
3. **The words are the video's own words.** "Your crypto", not "your coins", if
   that is what the script says.

**The scorer cannot always win, and hand-placing is not a failure.**
`futuristic-crypto-exchange.jpg` scores +0.90 at every zoom because the man's
detected box overlaps the type column wherever the type goes.
`crop_at=(0.0, 0.0)` with `side="right"` keeps his whole head and puts the words
on the dashboard's dark falloff. Record the reason in the script, as here.

### `shift` moves the subject when the crop cannot

A cover crop of a landscape source into 16:9 has **no horizontal slack** —
`nw == W` — so `crop_at`'s `ax` is inert and the only lever on where the subject
sits is zoom, which is what puts faces off the frame edge. `render_thumb(shift=)`
translates the picture toward the far edge as a fraction of the width and fades
what it uncovers to black over 260px.

That is not a compromise, it is a better thumbnail: the subject is entirely
clear on one side and the type gets a real black ground instead of a scrim laid
over detail. Sweep two or three values and look — on the crypto-exchanges
source, 0.10 still caught the first word on the hologram and 0.22 crowded the
subject against the edge, so 0.16 shipped.

### The layout is searched, and the search is the point

The question is **not** "where is the person" — it is **"where is the picture
empty enough to take type"**. Two attempts chased the subject and both failed
the same way: a face cascade finds a head, and no multiple of a head describes
the arms, hair and torso that actually collide with words. The second attempt
reported a clean layout while the type sat across a woman's chest, because the
box was honest about her face and wrong about her.

So `_layout` scores candidates on a blurred edge-energy map: **quiet under the
words, busy beside them** (`quiet - 0.6 * busy`), with a detected face under the
type treated as fatal. It searches zoom x pan x **side x vertical band** and
takes the best. A negative score means the composition works; positive prints a
warning.

**The band matters as much as the side.** Placing the block dead centre and only
choosing left or right ignores half the question — on a subject who fills the
lower frame the space is up in a corner, not beside them. Bands are top, middle
and bottom, scored over the region the type will actually occupy rather than the
whole column.

**Use the scorer to choose the source.** That is the real workflow now — run
`_layout` over a batch of candidates and read the scores, rather than eyeballing
one. The tinnitus thumbnail's source was picked that way: every image in the
site library scored "busy", so a batch of stock was fetched and scored and the
best one taken. Scoring is far more reliable than looking at a full-size file,
because the failure only shows at feed size.

Brightness is normalised toward a target rather than dimmed by a fixed factor —
a flat 0.80 crushed the dark portraits this selects for into near-black.

## Thumbnail: three checks, every time

1. **Text must not cover the face.** `render_short_thumb` defaults to
   `band="top"` because the Shorts player puts its chrome along the bottom, and
   that default is wrong the moment the subject's head is in the top half of the
   crop — which is most crops of a landscape source. Pass `band="bottom"` and
   look at the render. The user has now caught this twice.
2. **The subject fits.** No half faces at the frame edge.
3. **The words are the script's words.** "Your crypto", not "your coins".

**Match the Short's thumbnail to its long form's**, same source and same
headline, even where the two videos deliberately cover different ground — the
pairing and the angle are independent questions.

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

## A short's thumbnail is vertical, one file

**Settled 2026-08-26, correcting this doc's own former rule.** A Short is a
vertical video, and its thumbnail is `render_short_thumb`'s 1080x1920 cover -
one file, matching the video's own shape.

A second 1280x720 render was generated alongside it for a while, on the
reasoning that YouTube Studio has no working way to set a 9:16 image as a
Short's cover. That reasoning was correct as a fact about YouTube, but wrong as
a reason to make it a **build** output: it is a platform quirk to solve at
publish time, in Studio, by hand or however `/publish-video` solves it - not a
second file this doc hands over unasked. Producing it by default meant every
short generated a thumbnail the user had not asked for and did not want.

Check it the same way any thumbnail is checked: the subject fits, the type is
not over a face, and the words are the script's own words.

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

## Fit the subject and fill the gap. Never zoom to make it fill the frame.

**The proof-of-stake thumbnail shipped with one graphics card zoomed into and
the second cut in half, and the user's words were "too zoomed in and the
quality is terrible".** The source was 6750x4500, so nothing was upscaled - the
softness was the *crop*, not the resolution. A hard zoom into a wide subject
throws away the composition and leaves the eye nothing whole to land on, and at
feed size that reads as a low-quality image even when every pixel is sharp.

**A subject that cannot survive a cover crop must be fitted, with the leftover
space filled deliberately.** Two mechanisms, and both already existed:

- **`render_thumb(crop_zoom=<1.0)`** is the engine's own "stop covering the
  frame" mode: the picture is scaled to the size asked for and set on black
  with a 260px falloff, so the subject stays whole and the type gets real black
  instead of a scrim over detail. **Sweep it and look** - on the graphics cards
  0.55 left them small, 0.85 began clipping them at the bottom edge, and 0.78
  was the largest value that kept both cards entire. Pass `side` alongside
  `crop_at`, because a manual crop bypasses the scorer and there is no layout
  pass left to infer a side from.
- **`tools/make_slide.py`** for the 9:16 case, because
  `render_short_thumb` has **no** fit mode - its `zoom` multiplies the *cover*
  scale, so anything below 1.0 leaves the picture smaller than the frame rather
  than fitted. Compose the subject onto a 1080x1920 canvas once and let the
  thumbnail cover that exactly.

The general rule, which is the same one the diagram slide arrived at from the
other direction: **when a renderer has a cover mode and a fit mode with a
threshold between them, do not tune an input to sit near the threshold.** Move
it clearly to one side - by fitting explicitly, or by making the source
frame-sized so cover and fit become the same operation.

**A fitted panel needs the canvas to match the picture's own edge.** The first
vertical slide used the brand background and shipped with a visible lighter
rectangle around the photograph: the card shot's own surround measures
`(11, 12, 14)` and `CRYPTO.bg` is `(23, 23, 23)`. Two flat darks twelve levels
apart read as one shape with a seam through it. `make_slide(..., bg="auto")`
samples the source's border and uses that, which makes the join invisible
without needing the picture to fill the frame. Use `bg="brand"` for a *graphic*
that should sit on the channel's ground - a diagram - and `bg="auto"` for a
photograph.

**Check it on the rendered file at feed size, not on the source.** A crop that
looks fine full-screen is judged as a 210px-wide card in a grid.

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

## The short's thumbnail clears the view count by 20px

`render_short_thumb`'s `band="bottom"` margin is `int(VH * 0.16) + 20`. At the
bare 0.16 the last line of type ran straight through the play count YouTube
draws across the bottom of a Short's grid tile, and the user was opening the
artwork and lifting it by hand before every upload. **It is composed against a
platform overlay that is not in the file**, so a bottom-banded thumbnail that
looks marginally high in isolation is correct. `band="top"` is unchanged.

## The landscape thumbnail must resample with `INTER_AREA`, not `INTER_LANCZOS4`

**The caffeine pair shipped with a visibly grainy face on the 16:9 thumbnail
and a clean one on the 9:16 - from the same 7952px source photo.** The user's
note: "the person in the short thumbnail is very good quality but in the long
is noisy". It is not the source, the crop or the JPEG quality (both save at
92).

`render_short_thumb` resamples through PIL (`Image.LANCZOS`), which **always
prefilters on reduce**. `_layout` and `render_thumb`'s `crop_at` path used
`cv2.resize(..., INTER_LANCZOS4)`, and **OpenCV's interpolation filters do not
prefilter when shrinking** - a fixed 8x8 kernel sampling a 6x downscale of a
slightly noisy night photo aliases high-frequency grain straight into the
output. `cv2.INTER_AREA` is the correct decimation filter (it area-averages).

`thumb._scale(src, nw, nh)` now picks `INTER_AREA` when the target is smaller
than the source and `INTER_LANCZOS4` otherwise, and both downscale sites call
it. This is brand-agnostic - it fixes the crypto thumbnails too. **Never
resample a shrink with `INTER_CUBIC`/`INTER_LINEAR`/`INTER_LANCZOS4` in this
repo; they all skip the prefilter.**
