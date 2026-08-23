---
name: video-crypto-short
description: Make vertical short-form videos for TikTok, YouTube Shorts and Instagram Reels from thecrypto.wiki articles — voiceover with synced captions over the site's own images, screened stock clips and data graphics. Use when the user runs /video-crypto-short, asks for a crypto short or Reel, wants a post from thecrypto.wiki turned into a video, or wants to pick or tune the crypto voice. For drone footage shorts use video-drone-short instead.
---

# Crypto Wiki — short form

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
Shared with the drone and tinnitus projects. Renders go to the Desktop.

**Source content:** `~/Coding/crypto-wiki` — 60 posts, 27 exchanges, 33 crypto-ogs.

## After upload: metadata only, same as tinnitus

**A crypto Short stays YouTube-only, exactly like a tinnitus one.** It gets a
title, description and tags via `youtube-audit set` - see "The order of the
whole job" in `video-crypto-long`'s SKILL.md, which is the canonical copy - and
nothing else: no `videos.json` entry, no poster, no Facebook upload. A version
of this skill briefly said otherwise and it was wrong; both crypto and
tinnitus shorts follow the same rule for the same reason, there was never a
real per-site difference here.

## Built

`video_automation/crypto/` — a photo-driven short assembled from the site's own
images.

```python
from video_automation.crypto.build import render_crypto_short
from video_automation.crypto.shots import SITE_IMAGES, Shot

out, total = render_crypto_short(SENTENCES, SHOTS, out_path, work, voice="theo")
```

One `Shot` per sentence, in order. `plan_shots` gives each shot the measured span
of its sentence, so the picture is cut to the voice and cannot drift.

**Still unbuilt:** script generation from MDX, upload, and the MDX embed. The
script is written by hand for now, which is the right way round — the script is
the product and 60 posts of automated scripts is the failure mode, not the goal.

## What the site gives you

**Images:** `crypto-wiki/public/images/{posts,crypto-ogs,exchanges}`. Already
licensed, already on brand, already attached to the post. Start here — but do
**not** finish here, and that is a reversal, see below.

**The one exception is a short about a person.** The site's OG portraits are the
smallest images it has and most are under the ~750px floor — Saylor's are 700x348
and 500x472, so a piece about the man had no usable picture of him. Pull those
from **Wikimedia Commons**, which is licensed, attributable, and where the
photographs are 2000-8000px, i.e. the only images in the format that never
upscale at all. `assets/crypto/<person>/` holds them with a `CREDITS.md`, and the
CC BY-SA ones make the video a derivative work — **the attribution block goes in
the description of anything published**. This is not a licence to reach for
stock: it is a portrait of a named individual or it does not apply.

**Structured data, and it is built:** `video_automation/crypto/facts.py` reads
the frontmatter of all 27 exchange files and 32 OG files and hands
`quickFacts` straight to the beats. This is the one place the setup scales
without hitting the mass-production failure mode, because the *data* is the
script — numbers the site already publishes, fact-checks and keeps updated —
rather than a model's guess at one.

```python
from video_automation.crypto import facts as F

picked = [F.load("exchanges", s) for s in ("coinbase", "binance", "kraken", "uniswap")]
rows = F.compare(picked, "custody", F.contains("non-custodial"))
# -> [("Coinbase", False), ("Binance", False), ("Kraken", False), ("Uniswap", True)]
Shot(graphic="checklist", payload=(rows, "Who holds your keys?"))

F.facts_grid(F.load("exchanges", "kraken"))   # -> [(label, value), ...] for `grid`
```

- **Run `F.coverage(F.load_all("exchanges"))` before choosing what to compare
  on.** Four keys are on all 27 — `founded`, `type`, `custody`, `availability`
  — and only those support a comparison across the whole set. `headquarters`
  covers 24, `token` 19, `founder` 15. The gaps are not random: `token` is
  missing exactly from the exchanges that have no token, so a beat built on it
  silently drops the interesting cases.
- **`custody` is the first comparison worth making.** 21 of 27 are flatly
  "Custodial", 3 are non-custodial, 3 are custodial with a self-custody wallet
  alongside. That is a real answer to a real question, it is a judged list
  rather than a table, and the judgement is the site's rather than this repo's.
- **Pick the handful the script argues about, never the whole set.** `compare`
  raises past six rows, because a checklist reveals one item per caption and
  every row has to be spoken. 27 rows is not a graphic, it is a table. Pass
  `strict=False` to survey while choosing an angle.
- **It also raises on a row too wide for the line.** An over-long item draws
  straight off the right edge — nothing clips it and nothing raised before, the
  same bug class as marks scheduled past the last frame. `with_value=True` is
  usually what triggers it; the values are prose.
- **This is a payload generator, not a script generator.** The angle, the
  verdict and the wording stay hand-written. The script is the product.
- `Entry.image` resolves the frontmatter path into `public/images` and returns
  None when the asset is missing, rather than handing a shot list a path that
  fails at render time. The ~750px floor and the no-infographics rule apply to
  anything it returns exactly as they do to a hand-picked file.
- PyYAML is a dependency now. A hand parser was the first plan and is wrong
  here — the site's own values carry quoted colons ("Nasdaq: COIN") and
  semicolon-separated clauses, which is where naive splitting breaks. `head()`
  takes the clause before the semicolon, which is what fits on a card; the
  qualifier after it is the honest part and belongs in the narration.

**Palette** is `config/theme.json`: gold `#e5c200` on `#171717` / `#2f2f2f`.

**Demand data** is `json/views.json` — site pageviews, so it measures SEO demand,
**not** short-form appeal. Do not present it as evidence about video. Top pages:
`how-to-build-a-mining-rig` 1510, `understanding-crypto-exchanges` 1038,
`exchanges/cryptocom` 380, `crypto-ogs/satoshi-nakamoto` 372,
`crypto-etfs-explained` 362, `what-is-proof-of-stake` 317, `exchanges/okx` 304.

## Stock is allowed now, and motion is the point

**This reverses "do not reach for a stock API", which this file used to state
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

## Only a hyphen goes on screen

**Never an em or en dash in a spoken line or a caption.** The user's rule, for
every video on every channel: write `-`. At caption size a long rule is easy to
read as a stray mark, and it is a typographic flourish in a place that wants
plain type. It also survives being pasted into a YouTube description, a TikTok
caption and the site's transcript unchanged, which "—" does not always.

This applies to the script's own strings, not to prose in a docstring.

## A statement card needs a line handing off to it

A full-screen `chapter` card that arrives with nothing in front of it reads as a
title card dropped into the middle of the video. One sentence turns it into the
thing the piece has been building toward — "Always remember the golden rule."
before "Not your keys, not your coins." This is the same note the instruction
list got, and it generalises: **anything that changes the register of the video
needs a sentence saying why it is happening.**

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

## Silence is punctuation here too

`gap` takes a list, one per sentence, and **leaving every one at 0.34 is what
"monotone" means**. 0.34 inside a thought, 0.55-0.90 at the end of one, 2.10 for
a two-phase beat, and ~1.3 after a full-screen statement so it is allowed to
sit. A forty-second short has less room than a long form and needs the pauses
more, not less: the pauses are what stop three instructions in a row sounding
like one sentence.

## A tip needs a reason before it is a tip

The first cut went straight from the custody beat into "turn on two-factor,
start small, withdraw the rest" and the user's note was that it arrives with no
introduction. A list of instructions with nothing saying *why* reads as generic
advice, and generic advice is the thing an explainer is supposed to not be. One
sentence fixes it, and it should tie back to the beat above rather than being a
new topic: "You cannot change who holds the keys. You can change how much they
are holding."

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

## Sound

`core/sfx.py` **synthesizes** its effects rather than sourcing them. The drone
project's SFX are hand-placed clips living inside a Final Cut bundle, which a
headless render cannot depend on, and downloading a "free" UI click pulls in a
licence question over 200ms of audio. Two numpy functions cost nothing, are ours
to license, and are parameterised — `mark_cross` and `mark_tick` are the same
instrument at different pitches, which is why they read as one system.

- **The envelope is the whole character.** Instant attack, exponential decay,
  a noise transient on the front. A decay short enough that it never competes
  with a syllable is the difference between software and cartoon.
- **`gain` is against the narration's own peak**, not full scale. A fixed
  absolute level is inaudible under one voice profile and slapping over another;
  `0.22` is the working value. The mix ceilings rather than clips, because a
  mark landing on a stressed syllable will otherwise distort on exactly the beat
  meant to be satisfying.
- Cues come from the same `marks` list that drives the drawing, so picture and
  sound cannot drift apart.

**Watermark:** `public/images/logo.png`, upper-left at (58, 268), 300px wide,
full opacity, levitating 8px on a 6.5s sine. The asset already contains the
domain so nothing is added under it. Same safe box as the tinnitus shorts —
`SAFE_TOP=230`, `SAFE_BOTTOM=1440`, clear of `x>860` — and `render_shots` raises
rather than shipping outside it.

**It can roam:** `render_crypto_short(..., roam=True)` cuts the mark between
upper-left and lower-right every `logo_hold` seconds (13s by default). Off
unless asked for, so the shipped cuts are unchanged. A mark that moves is much
harder to crop out of a repost and defeats the corner blindness that makes a
static watermark worthless. It **cuts, never slides** — a lockup travelling
across frame is a second moving object competing with the picture — and keeps
levitating at each anchor. Every anchor is validated against all four safe
edges, not just the top. Full reasoning in `video-tinnitus-short`, where it was
specced.

## Copy

**Captions go under the photograph, not over it.** Every source image is
landscape, so even cropped it leaves a band of blurred backdrop below, and that
band is where the type belongs — over the photo it covers the thing it is
describing, and it wasted the empty space.

**One caption line for the whole piece, not one per shot.** `caption_line()`
takes the lowest line any shot needs — `photo_box(0.5)` plus 96px, clamped to
0.80 — and every caption in the video sits there. Measuring per shot was shipped
once and was wrong: captions are held until the next one starts and shots
dissolve over `XFADE`, so the outgoing sentence's last caption is still on
screen while the incoming photograph is already visible, and the type jumped
mid-dissolve — on the shots whose photos sit lowest, jumping *into* the incoming
picture. Solving the worst case solves all of them. The tightest shots get a
little more air under the photo than they need, which nobody notices; the jump,
everybody did. `y_frac=0.70` is only the floor.

**Watch the shot that sets the line.** It is whichever photo runs lowest, and if
its bottom lands within ~10px of 1536 the type has no air. Widen that shot's
`aspect` rather than lowering the clamp — 0.80 comes from the safe box.

**Captions are composited in Python, in `render_shots`, not burned by ffmpeg.**
They used to be full-frame PNG overlays gated with `enable='between(t,..)'`,
which is a hard on and a hard off — against a voice with a real sentence contour
that snap is the one part of the piece that still reads as generated. Every
frame is already drawn in Python, so `CaptionSprite` costs nothing and buys a
per-frame entrance: fade up over 0.13s while rising 12px and settling from 94%
**with a slight overshoot**. The overshoot is the trick — a linear scale-in
reads as a zoom, one that passes its mark and comes back reads as being
*placed*. Captions also cross-dissolve into each other, which is what stops a
four-caption sentence looking like four separate cards. It also deletes a
thirty-stream ffmpeg filter chain; the final pass is now just a mux.

Futura Medium 46px, stroke 4, `max_w=CAPTION_MAX_W`.

**Emoji** via `core.vertical.add_caption_emoji` — shared with the tinnitus format.
One or two per script, where they add something: a padlock on "those coins have
never moved", a down-arrow on the closing question. More than that reads as
decoration.

`gap=0.34`, tighter than the drone quotes' 0.65. A quote wants air between lines;
a thirty-second explainer does not, and the pauses are what a viewer scrolls away
during.

**End on a question — unless the video is a how-to, and then end on the rule and
a save.** The question exists to earn a comment, which is the cheapest signal a
35-second explainer can ask for. But it has to be a question the viewer can
actually answer from what they just watched: the mining rig short closed on
"would you have caught that before switching it on?" and the user cut it as
confusing, correctly — "that" had three possible referents by then, and it asked
the viewer to audit a build they have not made.

What replaced it: the rule restated as an echo of the opening line (`Cheap
adapter, expensive mistake.`) and then `Save this before you build one.` with a
🔖. **A save is a stronger signal than a comment on instructional content**, and
unlike "what do you think?" it is something the viewer has a concrete reason to
do. Match the ask to the video: a question for an argument, a save for a
procedure.

**The angle has to be in the first line.** The first cut is
`crypto-satoshi-proof` — "every few years someone claims they're satoshi, and
there is one test that settles it" — built from
`posts/what-it-actually-takes-to-prove-someone-is-satoshi-nakamoto.mdx`. It works
because the answer is concrete, surprising, and needs no financial advice.

**Check phonemes with espeak rather than guessing** — Kokoro phonemizes through
espeak-ng, so `espeak-ng -v en-us -q --ipa "Binance"` is the whole check. It
returns `baɪnˈæns` (bye-NANCE), which is wrong for the brand and shipped once;
`Bynanse` returns `bˈaɪnæns`, which is right. Respell in the **spoken** half of
a `(caption, spoken)` pair so the caption still reads correctly.

**Check phonemes before rendering.** Years are fine (`2009` → "two thousand
nine"), names are fine (`satoshi nakamoto`), but `ecdsa` comes out `ˈɛkdsə` —
spell out or avoid any initialism.

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

## Voice

Five profiles, all reproducing their audition WAVs sample-for-sample:

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices show theo
```

| profile | voice | note |
|---|---|---|
| `sam` | male, `am_puck` 1.10 | **used by the current cut.** C+ with hours of data, steadiest American male |
| `theo` | male, `am_adam` 1.10 | the first cut. Lowest Kokoro grade on the list, shortlisted by ear anyway |
| `mia` | female, `af_heart` 1.10 | **the Saylor cut.** Graded A, the strongest English voice in Kokoro |
| `mia-calm` | female, `af_heart` 1.00 | the same speaker, unhurried |

**None is approved.** `theo` took the first cut, `sam` the second, `mia` the
Saylor short, and the user intends to work through the rest. Keep the script and
shot list identical when swapping, so the comparison is clean. The `ENERGETIC`
chain they all share has not been signed off either.

Pace, measured on the same script: both `theo` and `sam` at 1.10 land near 3.1
words a second, so ~105 words comes out around 35s. `mia` at 1.10 sits close
enough to reuse the estimate — 168 words of Saylor script came out at 58.0s,
about 2.9 words a second with `gap=0.34`, so **~175 words is a one-minute
short**.

**The long-form skill now gives 3.25 words/sec, measured on shipped cuts, and
it is the better number here too.** `bitcoin-price-short` is 141 words plus
12.24s of gaps: 141/3.25 + 12.24 predicts 55.6s and it rendered at **54.2s**,
inside a second and a half. The old 2.9 predicts 61s, which is enough error to
push a Short past the window without noticing. Use `words / 3.25 + sum(gaps)`
and check it before rendering.

## Decisions already taken

**Render headless with ffmpeg, not FCPXML.** Drone long-form writes XML to finish
by hand because there the footage *is* the product. Here it is support and the
script is the product; a human step in the loop means it never runs.

**Do not commit MP4s to the site repo.** Publish to YouTube Shorts and embed a
lazy-loaded facade, so the site carries no video bandwidth and gains a
`VideoObject` schema — the SEO win that lands whether or not the channels work.

**Evergreen before news.** News needs a live data dependency the repo does not
have, cannot be embedded as evergreen `VideoObject` content, carries per-video
accuracy risk in a YMYL niche, and is the shape the platforms suppress hardest.
News becomes a variant once the pipeline is proven, not the proving ground.

## Do not

- Mass-produce. Both platforms suppress the AI-script-plus-stock-footage pattern
  by policy; volume is the failure mode, not the goal.
- **Build a piece that is mostly stock.** The rule above permits stock; it does
  not permit a stock slideshow. If the site's images and the drawn beat are not
  carrying the argument, the reversal has been misread.
- Open on a still.
- Give financial advice in a script, or imply one. Route to the site's exchange
  pages, which is where the affiliate revenue actually is.
- Promote a candidate voice to approved without being told to.
- Quote `views.json` as if it measured short-form performance. It is SEO demand.
- Use an image under ~750px wide, or an infographic at any size.
- Ship a Commons-sourced portrait without its `CREDITS.md` block in the
  description. Two of the four Saylor photographs are share-alike.

## Narration craft — read `/video-crypto-long`'s section, it applies here

That skill carries the full rules: pauses placed where the sense turns rather
than spread evenly, chapter titles written as openers, a **hinge sentence** into
the second column of a `compare` ("Now compare that with a decentralized one",
never the bare heading), saying the whole name of a product every time, and
drawing a figure that is spoken. They were written on the tinnitus channel and
none of them is site-specific — it is about how a synthesiser reads a page.

Two land harder in short form, because thirty-five seconds cannot recover:

- **A beat's items must be written as one spoken sentence, not a list read
  aloud.** "Not X. / Not Y. / Z." reads as a bullet list. *"It is not X. It is
  not Y."* then, after a real pause, *"It is Z."* is the same chunk count, the
  same reveals and the same sync — the difference is only whether a person
  would say it that way.
- **The last two sentences are the ones that get rushed.** Stacking an
  instruction, a reassurance and a call to action into the final eight seconds
  reads as messy. Give a short **one** closing instruction, say it once, and put
  0.70-0.90 in front of it.

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

## Do not open two shots in a row on the same clip

The silence short's opening question and the line after it were both on
`tired-woman-hands-on-face/4867379`, because the question was added in front
of an existing opener and the obvious thing to do with a new first shot is
give it the picture that was already there. Six seconds on one face, and the
second shot landed mid-yawn. A Short's first two shots are the two the viewer
actually decides on: **give the question the face and the line after it the
room.** The same clip may come back later at a different `clip_at`; it may not
run twice consecutively.

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

## A short needs two thumbnails, and the vertical one is not for YouTube

**Render both.** `render_short_thumb` gives the 1080x1920 cover that Instagram
and Facebook Reels use; `render_thumb` gives the 1280x720 that **YouTube**
uses. Same headline, same source photo, same treatment - only the shape
differs, which is what keeps the pair recognisable.

The silence short shipped the vertical file to YouTube and it was wrong in a
way nothing reported: YouTube letterboxes a 9:16 upload into its 1280x720 slot
with a **blurred, zoomed copy of the same image either side**, so the live
thumbnail was a narrow strip of picture with "DOES ... NCE" bleeding across
the bottom in huge soft letters. The user replaced it by hand.
`thumbnails.set` returns success, and `youtube-audit video <id>` lists a
`maxres 1280x720` entry, so **neither the upload nor the audit catches this -
only looking at the image does.**

## Keep this file current, every time

**Standing instruction: update the skill on every video**, with the specific
failure that produced each rule rather than the bare rule. Cross-post anything
engine-level or craft-level to the tinnitus skills — one engine, one
synthesiser, and a lesson found on one channel is almost always true on the
other.

## Shorts take a music bed

`render_crypto_short(..., music=..., music_gain=...)` — the same arguments
`render_long` has always taken, running the same `render_bed` +
`mix_voice_over_bed` path. Shorts never had one, which was a gap rather than a
decision, and the user's call is that every short gets one from here on.
`music.track("night-drift")` serves both sites; the generated presets remain
the licence-safe default.

Gain slightly under long form's (0.85 is what tinnitus uses): a short is
watched on a phone speaker with the voice carrying all the information. It
matters more here than in long form — a short opens with no lead-in silence and
is judged in its first second, and a synthesised voice over silence sounds like
a voice memo.

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

## A Short's YouTube thumbnail is the vertical one

**Corrected 2026-08-23, replacing the rule that said YouTube gets the 16:9
file.** Upload `<name>-thumb.jpg` (1080x1920) to YouTube for a Short. The four
earlier Crypto Wiki shorts all carry the vertical image and their covers work;
the one uploaded with a clean 1280x720 showed a video frame in Studio instead,
even though every thumbnail URL carried the 16:9 file correctly.

The cost is real and was what caused the original mistaken rule: a 9:16 upload
is letterboxed into YouTube's 1280x720 slot with a blurred zoomed copy either
side, so it looks poor anywhere 16:9 is used. Take that trade - a Short is
watched in the Shorts feed, and the cover is what governs the Shorts tab,
search and playlists.

Keep rendering both files. `render_thumb`'s 1280x720 output is what a long form
uses and keeps the pair recognisable.

**Swap one after the fact with**
`youtube-audit set <id> --channel crypto --thumbnail <vertical.jpg> --apply`.

Note the opening seconds still matter for their own reason: YouTube picks a
frame wherever a cover does not apply, and the feed is judged in one second
regardless.
