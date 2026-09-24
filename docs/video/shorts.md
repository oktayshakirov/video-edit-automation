# Vertical engine (9:16)

Shorts, Reels and TikToks. One engine for every project - what changes per
project is the voice, the source material and the safety rules, not this.

## Seven beats transfer to 9:16 now, not two

`checklist`, `grid`, `steps`, `bars`, `logos`, `chapter` — and **`diagram`**,
added 2026-09-10. `gauge` and `callout` still raise: a horizontal scale wastes
a vertical frame and a bordered photo with margin labels has no room for the
margins. Everything else raises too, which is the honest answer — the
remaining landscape beats lay a content column beside a picture column at 1920
and have no portrait layout.

**`diagram` is the one to reach for when every recent Short has run
`grid` + `steps`** — which, on the tinnitus channel, is all of them. Its
portrait layout runs the causal chain down the frame; `loop=True` returns the
feedback arrow up an inset left channel, filleted corners and all, and the
connectors draw against the voice (`span_p`). It is the beat for a mechanism a
scroller has not seen drawn — the tinnitus night loop, a volume arms race —
and it is a different silhouette from anything else the format has.

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
- **To show a photograph whole, set `aspect` to the source's own ratio.**
  `crop_w = min(src.w, src.h * aspect)`, so when `aspect == src.w / src.h` the
  crop is a no-op and the picture is letterboxed into the blurred fill instead
  of cut into. The default 1.15 is a *crop* target, and on an already-tall
  portrait it takes the top of the head and the chest off — which is what the
  user saw as "cropped" on the Ethereum short's opening face. **`bias` cannot
  fix this; it only slides the same-sized window.** Reach for the source ratio
  whenever the subject is a person and the shot is the one the viewer decides
  on: `FACE_ASPECT = 1670 / 2553` reads far better than a tighter crop, and the
  blur band above and below is what the layout is for.
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

**Exception, and it is about intonation rather than structure (2026-09-20).**
Kokoro reads a question mark with a rising contour, and on
`new-tinnitus-what-to-do-first-week` the user's note was that the opener
"sounds like a question but would be better to sound as advice statement in
this case". A how-to Short whose whole proposition is *do this tonight* is
weakened by an opener that asks rather than tells. So the rule is really
**name the subject and frame the payoff in line one** - a question is the
usual way to do that and not the only one. `"Tinnitus just started. Tonight
is the part you can actually change."` names the subject in three words and
still leaves sentence two to answer. Keep the question for a Short whose
proposition is a claim being tested ("Does silence make tinnitus worse?");
reach for the statement when the piece is an instruction.

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

**The closing line does not mirror this.** Open on the question; close on the
answer, never on another question - `narration.md`'s "A Short's ending loops;
it does not ask" has the retention split. Asking again at the end ("what do
you think?") is the long-form outro habit leaking into the wrong format.

## The opening hook: a redacted headline — `hook=`

**Added 2026-09-21. The first version (a static headline) was rejected the same
day as "just a headline with very ugly font and styling on a frame", which was
right.** This is the replacement. Every Short on both channels lost 13-27
points at ~5s, and the curves put the cliff before sentence 2 had finished —
so the fix has to work in the first second, work muted (most of Instagram, a
lot of TikTok), and give the viewer a reason to still be there at five.

```python
render_tinnitus_short(SENTENCES, SHOTS, out, work, ...,
                      hook="Quitting caffeine can make it [louder]")
```

The `[bracketed]` word is **hidden** — a bar of animated static in the brand's
colours, the width of the word — and **revealed on the frame the narration
says it**. `hook_reveal_time()` finds the word in the caption timings; the
render prints a warning and falls back to `hook_until` (3.4s) if it is never
spoken. Timeline (`longform/overlay.py`, `HookOverlay`):

| time | picture | sound | the job |
|---|---|---|---|
| 0.00s | picture punches in 1.14→1.0; headline slams in with overshoot | `hook_slam` — an 808-style drop with a punch on top | pattern interrupt, in the window a swipe is decided |
| 0.3s → word | hidden word: animated static + a light sweep + a slow pulse; every ~0.8s the headline **tears** (slice glitch + RGB split, 3 frames) | `hook_glitch` blip on each tear; `hook_swell` (reverse cymbal) over the last second, cut dead on the reveal | curiosity gap — the bar's width is a clue, the answer is seconds away |
| word spoken | bar wipes off, word lands in the brand pill, small pop and shake | `hook_pop` — a glitch resolving into a two-note chime | the gap closes *at* the old 5s cliff |
| +0.9s | headline slides up and out | `hook_swish` | clears the frame for the video |

**Placement: centred.** Every line is centred and the block sits on the frame's
vertical axis, its centre at 34% of the height — clear of the watermark above,
of the platforms' right-hand button rail (from ~45% down) and of the caption
line. A soft full-width dark band behind it (not a panel, not a top gradient)
keeps it legible. (Revised the same day: the first placement was top-left and
read as a corner label.) `centre_y=` moves it if a clip needs it.

The five sounds are their own kit in `core/sfx.py` (`hook_*`), synthesised
like everything else there and levelled so each sits within a few dB of the
voice — felt, not a sound-effects reel. Measured on the test cut: nothing
clips, the slam and pop peak around −3 to −4 dB against a −1 dB ceiling.

Type is the karaoke captions' own — Arial Black, upper case, the brand pill —
so it reads as part of the video, not a title bolted on. Nothing flashes on
frame zero: that is the frame a paused feed shows.

**Why this and not a bigger headline.** Three documented mechanisms, one per
phase: the swipe is decided in about a second and only something *happening*
stops it (pattern interrupt); an information gap the viewer can almost close is
what they will wait for (Loewenstein; the "redacted detail" hook is a named
short-form format); and a gap that closes on a sound and a pop is a small
reward exactly where the audience used to leave.

### Revised 2026-09-24: two modes, and the gap closes by three seconds

**The redaction is not the default any more, and the reason is the reveal
nobody was waiting for.** The user's note on the neck-tension pair:
*"we are waiting just to reveal the word up"*, plus *"the karaoke captions
under it are distracting"* and *"too much happening in the beginning"*. Three
separate faults, and only one of them was the mechanism.

**1. Hide only what cannot be guessed.** Every hook this channel had shipped
redacted a *direction word* - `[up]`, `[louder]`, `[worse]` - which is the
most guessable class of word there is. Cover the bar on any of them and the
sentence fills itself in, so there was never a gap: the viewer knew the word
at half a second and then waited four more for the video to agree. The rule
now has a test, and it takes five seconds to run:

> **Cover the bar and read the line. If you can write the word in, it is not
> a hook.**

What passes: a **number**, a **count**, a **duration**, a **name**, a **body
part**, a **mechanism**. What fails: any word the sentence's own grammar
implies. `It takes [30 seconds] to find out` passes; `Your neck can turn the
ringing [up]` does not.

**2. Statement mode is the other half, and it is not a lesser hook.** A hook
written with **no brackets at all** keeps the punch-in, the slam, the band and
the type, and drops the bar, the static, the tear and the swell
(`HookOverlay.redacted` is set from the text). Use it whenever the surprise is
the *proposition* rather than a token inside it - which is most of the time on
both channels. The stake is still on frame zero and still readable muted; the
piece simply does not pretend to a gap it has not got. It clears at
`SLAM + statement_hold` (2.2s) instead of waiting for a word.

**Pick the mode before writing sentence 2**, because the two want different
second sentences: redacted mode needs the token *said*, statement mode is free
to go straight to the partial answer.

**3. The gap closes by ~3s, not at 5.** `hook_reveal_time`'s `latest` is
**4.2s** (was 7.0) and the fallback is **3.0s** (was 3.4). The old target was
"land the reveal on the 5s cliff"; what that produced was an opener whose
whole first act is a holding pattern. Three seconds is long enough to make a
promise and short enough that the video is still moving. **Put the token in
the first few words of sentence 2**, not at its end - on the neck-tension cut
it sat five words in and landed at 5.3s.

`[30 seconds]` matches a caption reading "thirty": `_NUMBER_WORDS` in
`crypto/build.py` maps the common figures both ways, because a silent match
failure reveals on the fallback and is invisible until you watch the render.

**4. The captions stand down while the hook is up.**
`render_crypto_short(..., hook_mutes_captions=True)`, the default. The hook
block and the karaoke line are independent layers and both ran from frame
zero, so a Short opened with two blocks of type saying the same sentence - one
at 34% of the height, one at 70% - over the watermark, the static bar and its
tears. **The long form's opener reads cleaner for exactly one reason: it burns
no captions, so the hook has the frame to itself.** The voice is already
saying the line the hook is showing.

**The mute ends on a sentence boundary, and that is the whole rule.** The
first version dropped sprites whose own `start` fell under the hook - and with
karaoke every *word* is a sprite, so a sentence that began under the hook came
back for its last second: the viewer read the tail of a line whose beginning
they never saw, which looks like a bug rather than a choice. Captions now
resume at **the first sentence that starts after the hook has gone**
(`sentence_spans`), so every burned line is seen whole. The outro takes the
same boundary: it attaches to the last *sentence*, not to its final caption
chunk, or a closing line long enough to split would burn its first half under
the card.

**5. One tear, not four.** The glitch fired every ~0.8s, so a late reveal drew
four of them with a blip on each. One tear reads as the bar being unstable;
four read as the render being broken. Statement mode draws none, and carries
two sound cues instead of five.

**How to judge it:** the two modes are separate cohorts in the E1 ledger. A
statement-mode win and a redacted-mode loss average into "no effect", which is
the one result that would teach us nothing.

### The outro is the opener's twin — `outro=`, added 2026-09-24

**A Short used to close on a `chapter` card and open on the hook, and they
were drawn by two different videos.** `ChapterCard` is the long form's chapter
slate: a hairline rule over a flat brand panel, set in the body face, with no
motion and no sound. Against an opener built from Arial Black, a dark band, a
brand pill and a slam, the user's verdict on the closing card was **"very old
and ugly"** — and the first and last thing a viewer sees are the two frames
that decide whether the piece reads as made or as generated.

```python
render_tinnitus_short(..., hook="It takes [30 seconds] to find out",
                      outro="Your neck is not the cause. It might be the [volume].")
```

It is the **same `HookOverlay`**, which is the point — one type system, one
band, one pill, one slam, top and tail:

- **It rides over footage, not a panel.** The last sentence keeps its clip, so
  the video ends on a moving picture with the statement over it. A flat card is
  a full stop; this is the piece still running as it says its last line.
- **`leave=False`: it never slides off.** The closing statement holds to the
  final frame. A Short that ends on an empty frame cannot loop into its own
  first frame, which is the whole retention argument behind the cold close
  (`narration.md`, "A Short's ending loops; it does not ask").
- **`[brackets]` put the pill on the payoff word**, and the reveal is timed to
  the frame the voice says it — searched inside the outro's own span, so an
  earlier mention of the same word cannot steal the cue. A fixed delay was
  tried first and drifts half a second either way.
- **The captions mute under it**, same rule as the hook: the card *is* the
  closing line, so burning it underneath is the duplication the opener
  already dropped.
- **No punch-in and no swish.** Both belong to an arrival; the outro is
  already there.

Written with no brackets it is a plain statement in the same type — the
outro's version of statement mode.

**The card still has its uses in long form**, where a chapter slate is a
chapter slate. This replaces it only as a Short's closing statement.

**How to write it** — the hook, sentence 1 and sentence 2 are one unit:

- **Sentence 1 (voice)** is the title question, unchanged.
- **The hook (screen)** is a 5-9 word *statement* of the surprising answer
  with its key word hidden. Not the title again.
- **Sentence 2 (voice)** is the partial answer from `narration.md`, and it
  **must say the hidden word**, ideally 3.5-5s in. That spoken word is the
  reveal cue — it is what makes the gap close on the beat.

| title question (voice) | hook (screen) | sentence 2 must contain |
|---|---|---|
| Does caffeine make tinnitus worse? | Quitting caffeine can make it `[louder]` | "...make the ringing *louder*..." |
| What's hidden in Bitcoin's first block? | Satoshi hid a `[newspaper headline]` inside Bitcoin | "A line from a *newspaper*..." |
| Do noise-canceling headphones help? | In a silent room they can make it `[worse]` | "...in total silence they make it *worse*." |

- **Hide one word or a two-word phrase** — the one that is the surprise. Hiding
  a filler word ("it", "the") makes the gap meaningless.
- **Guessable, not obvious.** If every viewer knows the word, there is no gap;
  if nobody could, there is no pull.
- **It must be true, and the video must pay it off.** A hidden word the video
  never earns is clickbait. **On tinnitus, never hide a promise** — no
  `[cure]`, `[relief]`, `[stop it]`.
- **Pick an opening clip whose subject is not at 30-40% of the height.** The
  headline is centred there, and a close-up's eyes usually are too — the
  caffeine test cut lost the woman's eyes behind it. Use a clip whose subject
  sits lower (hands, an object, a figure in a room), or shift the crop with
  `clip_ay`, or the hook with `centre_y`.

**This is an experiment (E1 in the `video-performance-review` ledger).**
Judged on the ~5s drop and the half-gone second against the pre-hook cohort.
If hooked Shorts still lose 13+ points at 5s, the cliff is about something
else and this section should say so.

## Cast a Short from close and medium shots — a wide becomes background

**The rule above says to crop onto the subject; this one says some clips have
no crop that works.** A 9:16 cut keeps about **32% of a landscape source's
width**, so a wide shot whose subject occupies a third of the frame arrives as
a frame of wall. The neck-tension Short's first cut opened on three of them
and the user's note was that the opening clips are irrelevant and "cropping
the main part and showing the empty part" — a silhouette in the bottom corner
with four seconds of lit wall beside it, and a top-down keyboard whose hands
sat outside the crop. Every one had been approved on a landscape contact sheet
with the crop band drawn on it, which shows *where* the band lands and not how
little is inside it.

**Preview the actual 9:16 crop before writing the shot**, not the landscape
frame with a rectangle on it: take the frame, crop `h*9/16` at the shot's
`clip_ax`, scale it to a phone-sized tile and look at that. Six of eight
candidates failed this check on the re-cut and none of the failures was
visible on the landscape sheet.

**So prefer a close or a medium shot** — hands filling the frame, a person
from the chest up, an object — and treat a wide as a long-form picture. The
one exception is a wide whose subject is *centred and lit*, like a figure
walking under a street lamp, where the middle third is the whole composition.

**Only the first shot has to clear the hook band.** The hook leaves by ~4s, so
shot one needs its subject away from 34% of the height and nothing after it
does. That is a much smaller constraint than it looks, and it is the reason
the opening slot should be the tightest shot in the cut rather than the most
atmospheric.

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
- **1.08 is not always small enough, and repositioning cannot fix it.** "Do
  noise-canceling **headphones** actually help tinnitus?" shipped with
  `headphones` fused to both neighbours - measured, its `grow`'d width
  overhangs 13px a side against a 9px space at size 46, so even perfect
  centring already eats the whole gap, and the 4px stroke on every glyph
  closes what little was left. Sliding the oversized glyph run left or right
  only moves the overhang from one side to the other; it cannot remove it,
  because the glyph itself is not shrinking. The fix shrinks the *enlarged*
  font for that one word, one point at a time, until its stroked width fits
  inside `adv + (space - 2*stroke)` - so a long highlighted word still pops,
  just not at the full 1.08 - and a short one keeps the full growth
  untouched. Check any highlighted word over ~8 characters on a fresh script;
  this is cheapest to catch on the render, not by eye in the editor.
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

**Which means an emoji silently switches karaoke off for that line, and a viewer
reads that as the effect breaking.** The user caught it by timestamp on the
Ethereum short — the highlight ran for seven seconds, stopped dead on the one
caption carrying a 🏢, and came back afterwards. It is not a bug; it is the
trade, and it was never written down as one.

**Karaoke wins. Default to no emoji on a short that has it on** (settled 2026-09-06). Two glyphs are
decoration; a highlight that stops mid-video is a fault the viewer notices. If a
line genuinely needs the glyph, put it on the **last** caption of the piece,
where the break has nothing after it to be inconsistent with — and never on a
line in the first fifteen seconds.

## Box karaoke is the default: a coloured box instead of a coloured word

Trialled on the drone channel first (`berlin-column-believe-in-you`, 2026-09-16
— see `projects/drone-short.md`), then ported here the same session so both
channels can reach for it: `render_crypto_short(..., karaoke_box=True,
karaoke_upper=True)` (and `render_tinnitus_short`, which forwards both
straight through). **On by default since 2026-09-21** — the user's call, for
every short with karaoke text on all three channels (crypto, tinnitus, drone).
Every script approved before that date pins `karaoke_box=False,
karaoke_upper=False` so a re-render of a locked cut does not change style.

Instead of colouring the active word's ink, a rounded rectangle in `brand.primary`
is drawn behind it and the word itself stays white-on-black-stroke like every
other word — the auto-caption look several TikTok templates use. `karaoke_upper`
uppercases the whole line to match; the two are meant to travel together, not
as independent toggles. `karaoke_box` also switches the caption font from
`FONT_CAPTION` (Futura) to `FONT_KARAOKE_BOX` (Arial Black) for **every**
caption in the short — including the ones that fall through to the plain-PNG
path (a one-word caption, an emoji line) — because a short with Futura on one
caption and Arial Black on the rest reads as two different videos cut
together, not a deliberate choice.

See `core.vertical.render_caption_karaoke`'s `box=`/`upper=` for
the mechanics, including two things that are not obvious from a still-PNG
review: the box sits on a separate layer behind the text, so a neighbour's own
glyphs always draw on top of it and are never hidden outright — but a pill
wide enough to *reach* the neighbour still reads as overlapping it, which is
what shipped once on drone's "STAND" and is a padding problem, not a layering
one. `box_pad`'s x is clamped to the real blank gap between two words'
*stroked* ink (every word's own stroke halo already eats into the plain
`space`), and `box=True` skips `grow` entirely, since enlarging the hot word
on top of the pill only spent more of that same tight gap.

**This is unrelated to `single_line=True`**, the other flag that shipped
alongside it. That one forces the whole karaoke'd line onto one row by
shrinking the font instead of wrapping — built for the drone channel's
stacked layout, where a second line overflows the black band between the
tiles. Crypto and tinnitus captions burn over full-bleed footage with no such
band, so wrapping to two lines is still the right, already-approved behaviour
here; `single_line` defaults off and neither channel's build code sets it.

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

## `diagram` and `gauge` transfer to 9:16; `callout` is landscape-first

Added with the three new beats (see `beats.md`), and screened in portrait
rather than assumed:

- **`diagram` is the strongest of the three here.** The chain turns ninety
  degrees and runs down the frame, which is the axis 9:16 has to spare - the
  same argument `steps` makes for its own track. Boxes stay the size their
  content needs and the *gaps* stretch to fill the height, because at the
  landscape gap a three-node chain ended a third of the way up the frame with
  nothing under it, and a drawn beat burns no caption there to fill it.
  `loop=True` works in portrait: the boxes inset from the left and the return
  arrow runs down that channel, filleted corners and all. The connectors draw
  against the voice (`span_p`), same as landscape.
- **`gauge` works but is landscape-first.** A horizontal scale in a vertical
  frame is the wrong way round by nature and leaves the lower third empty; it
  is legible and on-brand, and the track thickens to 46px because 34 across
  1080 reads as a hairline. Use it in a short when the *limit* is the whole
  point of the section, not as a general-purpose figure - `stat` is still the
  better vertical beat for a number that stands alone.
- **`dial` is the one that prefers portrait** (added 2026-09-13, see
  `beats.md`). A radial scale is as tall as it is wide, so where `gauge`
  wastes a 9:16 frame this one fills it, with the readout sitting under the
  hub and the burned caption clearing it below. It is also the beat to reach
  for when a Short's subject is an instrument or a graduated scale - which is
  a thing a Short otherwise has no way to show at all, since the alternative
  is a stock clip of somebody looking worried.
- **`callout` is landscape only in practice.** In 9:16 there is no width for
  side gutters, so the labels fall back to a column below the image and the
  beat loses the clean side rails that are the whole point of the rebuild.
  It renders, but the answer to "explain this picture" in a short is still
  `ImageOverlay` over moving footage - see that section. Reach for `callout`
  in the long form and let the short use the same photograph differently,
  exactly as the pair already shares its opening face.

The rule the vertical format already had applies unchanged: **two drawn beats
in one short must not share a silhouette.** With twelve shapes now there is no
excuse for a second `checklist`.
