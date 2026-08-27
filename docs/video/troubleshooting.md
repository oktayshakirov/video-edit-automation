# Rules paid for in blood

Engine faults that already cost a re-cut once. Read this before blaming a
script for something the renderer did.

## Rules paid for in blood

**Cut between drawn beats; dissolve between photographs.** The shorts' "always
dissolve" is a rule about *photographs*. Dissolving a pull quote into a checklist
cross-fades two sets of type through each other and reads as a rendering fault.
`plan.lay_out` sets `xfade=0` automatically between beats and on both sides of a
chapter card. Do not override it.

**The drifting grid is gone, on both channels.** It stepped a whole pixel at a
time — `int((f * 40) % 96)` on a layer moving 40 px/s — which is the judder
this repo fixed everywhere else years ago, and it was the same ruled lines
behind every beat of every video on both sites.

`core/backdrop.py` replaces it with a looping asset per brand, named by
`Brand.backdrop` and living in `assets/brand/backgrounds/`. **thecrypto.wiki is
`crypto-blackwater`** — black water, ping-ponged from the calm-water stock,
dimmed and desaturated. The user's call, and it is the better ground: gold type
on a near-black surface with slow specular movement reads as depth where ruled
lines read as a template.

Three constraints, all of which will bite if ignored:

- **Backgrounds are square, 512x512.** One file serves 1920x1080 and 1080x1920,
  scaled to fill and centre-cropped. Only viable because they are soft and
  low-frequency; anything with legible content in it does not belong here.
- **Sampled by timeline seconds, not the beat's `f`** — otherwise the whole
  loop plays inside every beat and the background changes speed at each cut.
- **`dim` must multiply.** ffmpeg's `eq=brightness` adds a constant, and
  dimming already-dark footage that way returned pure black, measured at mean
  luma 0.0. `pingpong()` uses `colorchannelmixer`.

Ping-pong is what makes real footage loop without a blend, and it is **only**
invisible on subjects with no arrow of time — water, smoke, cloth. Measured on
the water: seam 2.91 against a median ordinary step of 4.41, so the join is
less change than a normal frame.

Over a photograph the backdrop still drifts instead; that path is unchanged.

**A ping-pong background must not fold at frame zero, and must not repeat a
frame at either fold.** Both were true of the first `crypto-blackwater` and
together they are what the user saw as "the animation starts rewound and sorts
itself out in the first second". A palindrome turns around at frame 0 and again
at its midpoint; a naive forward-plus-reverse also *repeats* the frame at each
turn, and a repeated frame is a dead frame — motion stops. Measured on the old
asset, the two smallest steps in the whole 302-frame loop were 0->1 and 1->2, at
2.66 and 2.73 against a median of 4.36.

`pingpong` now drops one frame from each end of the reversed half, and
`Backdrop.at` samples from a quarter of the loop in, so no video ever opens on a
fold. After: minimum step 2.82 at frame 109 — an ordinary quiet moment in the
water — and the wrap step 4.81 against a 4.49 median. **Re-measure this way
after adding any footage background**: `d[i] = mean|f[i+1]-f[i]|` over the whole
loop including the wrap, and check the minimum is not at a fold.

**Measure the block, then centre it.** Every beat was first laid out from
fractions of frame height and every one left the bottom 40–50% of the frame
empty. Wrapping decides height, so measure before placing.

**Callouts are for the five to eight lines that carry the argument**, not for
every line. Full burned captions for three minutes fight every drawn beat for
the same space. The complete transcript ships as the SRT, which YouTube indexes
and which is exact where its automatic captions guess.

**Pick callouts from lines whose shot is a photograph.** `build` drops a callout
on a drawn beat — the shorts' rule, and for the shorts' reason: the beat's items
already *are* the type, set larger and mid-frame, so a line underneath restates
what is being read at that moment in a worse position. The natural instinct is
to call out the punchiest closing line of each section, which is exactly the
line a script tends to give a `stat` or a `quote` to. Three of the pilot's first
five callouts were silently dropped for this. A callout also cannot outlive its
own sentence's audio, so it can never bleed across the silence a chapter card
occupies — that is automatic now, but it is why the first pilot burned "There is
no third answer." straight over chapter card 03.

**Check phonemes with espeak, not by guessing.** Kokoro phonemizes through
espeak-ng, so the answer is one command away and there is no reason to ship a
mispronounced brand name:

```bash
espeak-ng -v en-us -q --ipa "Binance"
```

`Binance` comes back `baɪnˈæns` — bye-NANCE, stress on the second syllable —
which is what shipped and what the user caught. `Bynanse` comes back
`bˈaɪnæns`, which is the brand's own BY-nance. Put the respelling in the
**spoken** half of a `(caption, spoken)` pair so the screen still reads
correctly. Same trick for `USD` (`jˌuːˌɛsdˈiː`, the three letters, which is what
to say when the pair on screen reads USD) and `Crypto.com` -> "Crypto dot com".

**Check phonemes before rendering.** `ecdsa` comes out `ˈɛkdsə` and `secp256k1`
is worse — `satoshi-proof.py` says "a cryptographic signature" throughout
instead. Years are fine (`2009` → "two thousand nine"). Spell out or avoid any
initialism.

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
