# Type, colour and layout

What goes on screen as graphics rather than footage.

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

## Only a hyphen goes on screen

**Never an em or en dash in a spoken line or a caption.** The user's rule, for
every video on every channel: write `-`. At caption size a long rule is easy to
read as a stray mark, and it is a typographic flourish in a place that wants
plain type. It also survives being pasted into a YouTube description, a TikTok
caption and the site's transcript unchanged, which "—" does not always.

This applies to the script's own strings, not to prose in a docstring.

## The watermark sits high

`logo_at=(64, 62)` with `safe_top=40`. It was at y=150 and collided with both
the full-frame photographs and the beat kickers — a 16:9 player puts nothing
there persistently, so the first guess of a 120px top reserve was paying a real
cost against a hypothetical one. The guard checks **`logo_at` minus the 8px
float**, so a mark that clears `safe_top` at rest can still raise.

Beat kickers moved to y=214 for the same reason: at 176 a 34px kicker read as
the second line of the logo lockup rather than as the beat's own heading.

### A photo's border never crosses the watermark

**There are two kinds of picture frame and only one of them has this problem.**
A photograph that fills the frame bleeds off every edge and draws no hairline at
the top, so the mark simply sits over the image — that is fine and is left
alone. A photograph that *fits* carries a gold hairline along its top edge, and
that line ran straight under the wordmark: two graphics crossing, which a viewer
reads as a fault rather than as framing.

`PhotoShot` dodges it automatically — nothing to set per shot.

`LOGO_CLEAR` came down from 16 to 10 while fixing the tinnitus mark, so a
dodging photograph now sits 6px higher here as well. **Every pixel of it is
charged twice** — once as dead space above the picture and again as size, since
a photo too tall for the remaining band is scaled into it. Under a 33px wordmark
that is invisible; under a square lockup it was the complaint that found it.

- **The push is a constant offset for the whole shot, not a per-frame clamp.**
  `y` travels across a Ken Burns move, so clamping each frame would hold the
  picture against the floor and then release it. The offset comes from the
  extreme of the travel and the motion is preserved exactly.
- **It fires only when the picture actually reaches the mark, in both axes.** A
  shot already below the wordmark, or sitting to its right, is untouched — which
  is also what keeps the shipped vertical shorts byte-identical, since 9:16 puts
  the mark at y=268 and the photograph 200px below it.
- **A photo too tall to fit under the mark is shrunk, not shoved.** Translating
  a picture that already reaches within 60px of the bottom pushes its lower edge
  off frame, so the bottom hairline vanishes mid-shot — one artifact traded for
  another. It is scaled into the band that is actually available instead, which
  costs a few percent on what is a downscale of the source anyway.

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
