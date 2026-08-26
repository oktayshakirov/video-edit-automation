---
name: video-drone-short
description: Make vertical short-form videos for TikTok and YouTube Shorts from drone footage — 9:16 crop, quote or motivational text, optional AI voiceover with synced captions. Use when the user runs /video-drone-short, asks for a TikTok or Short or Reel, wants a vertical or cropped version of drone footage, wants text or a quote over a clip, or wants narration read over footage. For long-form YouTube edits cut to music, use video-drone-long instead.
---

# Drone Automation — short form

Renders finished vertical MP4s. **This is the one part of the project that
renders video**; the long-form pipeline (`video-drone-long`) only writes FCPXML.

**Repo:** `~/Coding/video-edit-automation` — run from there, with `PYTHONPATH=.`
so `video_automation` imports from the working copy. The repo is shared with the
crypto and tinnitus projects; drone code lives in `video_automation/drone/`, and
everything voice- and render-related in `video_automation/core/`.
Footage must already be indexed: `.venv/bin/python -m video_automation drone index <folder>`
(shared with `video-drone-long`; the proxies and clip index are the same).

## When the cut is approved, hand off to `/publish-video`

**This skill builds. It does not publish, and it deliberately no longer
describes how.** Everything about getting a finished render out - which file
goes to which platform, the metadata pass, thumbnails and covers, the site
registry entry and poster, the social posts and the order they run in - lives
in **`/publish-video`**, which is the single source of truth for all six video
skills.

That section used to be duplicated here. Two copies of one sequence drift, and
these did: they disagreed about which steps run on a Short, and the
disagreement cost a registry entry that had to be reverted and a social post
that could not be un-sent. So it is removed rather than summarised - a summary
is just a third copy waiting to go stale.

The flow ends here:

1. Build the cut and hand over the files.
2. The user reviews it and confirms it is good.
3. **Run `/publish-video`** and follow what it says.

Do not describe upload steps, do not pre-empt them, and do not re-derive them
from memory. Read the skill.


## TikTok and YouTube are not one audience

**Everything in the next section is YouTube data.** It was written before the
TikTok account was ever measured, and it does not describe TikTok. Pulled
2026-08-09:

| | views |
|---|---|
| YouTube, lifetime since 2015 | 26,113 |
| TikTok, last 365 days | **678,600** |

TikTok is the bigger platform by a wide margin — 86.3% For You, healthy
distribution, one video at 621K. Three YouTube-derived rules **measurably do not
hold there**: 30s+ posts do fine (best recent is 0:31 with 231 likes), Bulgaria
is TikTok's *strongest* material rather than off-audience, and plain scenery
beats angle-driven quote videos on engagement — the reverse of YouTube.

Like-for-like on TikTok, same weeks: scenery posts run ~2–5% likes, narrated
quote shorts ~0.4–0.9%. The user has seen this and chose to keep posting quotes
to both, because one asset for two platforms is worth more than the delta.
**Do not re-litigate that; do not quote YouTube numbers as if they cover TikTok.**

Note the 678.6K is skewed by that one 621K video — the realistic per-post
baseline is closer to ~1,000.

## What the channel's own numbers say

YouTube only. Do not re-derive these, and do not apply them to TikTok.

**Length correlated strongly with performance in past uploads:**

| length | median retention | median views |
|---|---|---|
| 10–19 s | 85% | 693 |
| 20–29 s | 71% | 176 |
| 30–39 s | 38% | 141 |
| 60 s | 26% | 80 |

**Do not treat this as a fixed target.** It is historic correlation on a small
sample, from before the quote/voiceover format existed, and a narrated piece may
hold attention differently than a silent scenery clip did. The format is still
being tested.

**Working rule: keep it under 30 seconds**, and shorter when nothing is lost by
it. Report the runtime and let the user judge rather than trimming a script to
hit a number. Revisit once there are real numbers on the new format.

**The angle beats the scenery.** A joke about German train delays did 2,075; a
hyperlapse tutorial hit 180% retention (people watching twice); "Golden Hour
Drone Footage" did 85. Same drone, 24× spread. Every short needs a reason to
watch beyond the view.

**Cadence compounds.** A seven-in-two-weeks run averaged ~1,800 views; sparse
months average ~200.

**Shorts carry the channel** — 30 of them total ~19.5k views against ~1.5k for
five long-form videos over the same period.

## Building one

```python
from video_automation.core.vertical import (pick_crop, pick_crop_tile, stack_tile_size,
                                             render_text_png, render_short, sample_bg_luma)
from video_automation.core.voiceover import (render_narrated, render_narrated_cuts,
                                              render_narrated_stack, profile_args)
```

**Given two clips for a narrated quote, stack them by default** — see
*One clip vs. two stacked* below. Cut sequentially only when the user says so.

Silent quote card:

```python
box  = pick_crop(proxy, zoom=1.45)              # zoom only for wide landscapes
luma = sample_bg_luma(src, box, mid_timecode)
png  = render_text_png(text, tmp/"t.png", bg_luma=luma)
render_short(src, out, start, 12.0, box, png)
```

Narrated with synced captions, one clip:

```python
# One inner list = one spoken sentence, chunked only for the captions.
# (caption, spoken) where screen and engine differ — heteronyms, quote marks.
SENTENCES = [
    [("i read a quote that said", "i red a quote that said,")],
    [("“you'll spend years", "you'll spend years"),
     ("chasing a feeling",        "chasing a feeling"),
     ("tuesday.",                 "tuesday,"),      # comma = the breath
     ...],
]

render_narrated(
    src, out, start=2.0, box=box,
    text=" ".join(c for s in SENTENCES for c, _ in s), workdir=work,
    sentences=SENTENCES,    # NOT phrases= — see Caption sync
    # font_path/font_index default to FONT_QUOTE (Iowan Old Style Italic) —
    # see Text below. No need to pass them.
    stroke=4, y_frac=0.34,
    gap=0.65, tail=1.2,     # gap is between sentences only; tail stays 1-2s
    **profile_args("leo"))
```

Across several clips cut in sequence — `render_narrated_cuts` takes
`(src, in-point, box)` per clip and returns `(out, total, cuts)`:

```python
render_narrated_cuts(
    [(clip_a, 2.0, box_a), (clip_b, 8.0, box_b), (clip_c, 8.0, box_c)],
    out, SENTENCES, work, y_frac=0.48, gap=[0.65, 1.9, 0.65], tail=1.2,
    stroke=4, fps=30, **profile_args("leo"))
```

`plan_cuts` snaps cut points to **caption boundaries**, never to even time —
cutting mid-caption reads as a mistake, because the eye is on a line of type
and the ground changes underneath it. Every segment gets at least `min_hold`
(2s); a shot too short to register is worse than an uneven cut. Sources must
share fps and dimensions, because `concat` demands it.

**But reach for one clip first.** See *The reveal format* below — a clip that
already moves usually beats cutting between clips that do not.

**Two clips stacked into one frame** — approved on Sunset Sea Stack, the first
short built from two unrelated clips rather than one clip or a sequence of
cuts. Both tiles fill the whole width; the quote reads on the black band
between them rather than over either picture:

```python
tile_w, tile_h = stack_tile_size()                 # band=140 by default
box_top    = pick_crop_tile(proxy_top, tile_w, tile_h)
box_bottom = pick_crop_tile(proxy_bottom, tile_w, tile_h)

ORANGE = (255, 150, 60, 255)     # pulled off a sun track — pick from the actual footage

out, total = render_narrated_stack(
    (clip_top, 2.0, box_top), (clip_bottom, 1.0, box_bottom),
    out, SENTENCES, work,
    font_size=lambda c: 88 if c == "LUCKY" else 44,
    ink=lambda c: ORANGE if c == "LUCKY" else None,
    gap=[0.6, 0.6, 1.7, 0.6],
    **profile_args("leo"))
```

`pick_crop_tile` runs the same 2D interest search as `pick_crop`, but at the
tile's own aspect (wider, shorter than 9:16) rather than one derived from
`zoom` — it keeps far more of the sensor width, so a `lateral` move can survive
here where it would exit a 28% 9:16 window. `stack_tile_size(band)` is the one
source of truth for the tile size, so the crop search and the render call can't
disagree about the split — always get `tile_w, tile_h` from it rather than
hand-computing `OUT_H // 2`.

Write outputs to the Desktop unless told otherwise — they are for uploading, not
for the repo.

## The crop is the biggest quality decision

`3840×2160 → 1080×1920` keeps only 28% of the width. `pick_crop` scores an
interest map (edge energy plus saturation, which suppresses sky without
special-casing it) and searches **x and y together** over an integral image.

**Searching x alone is not enough** — this was the first version and it failed.
On a wide landscape the content sits in a horizontal band near the ground, so a
full-height window spent ~60% of the frame on empty sky. Use `zoom` to tighten:

- `zoom=1.0` — subject with strong vertical extent (a tower, a vertical move)
- `zoom≈1.45` — wide landscapes, pulls the frame down off the sky

At 1.45 the window is ~1490 lines upscaled to 1920, which stays sharp from 4K.

**Move type predicts croppability** — check the index before choosing a clip:

| fit | move | why |
|---|---|---|
| best | `orbit`, `vertical` | subject holds centre; vertical move suits a vertical frame |
| good | `push_in`, `pull_back`, `hover` | centre-weighted or static |
| poor | `lateral` | subject travels across and exits a 28% window |

For laterals, use the stacked layout (two or three horizontal crops filling the
9:16 frame) rather than cropping — already proven at 1,528 views on this channel.

**The stacked layout wants a band, not a seam.** Approved on Sunset Sea Stack,
now a repo function — `render_narrated_stack` in `voiceover.py`, tiles from
`pick_crop_tile` — see *Building one* above for the call. Default is two
1080x890 tiles with a 140px black band between them, captions centred at
`y_frac=0.50` so they sit *in* the band. The first cut butted the tiles
together and put the type across the join, which worked but made the type
fight two moving pictures at once. The band gives it ground of its own and
reads as a deliberate frame rather than a crop artifact.

**Never use "rotate your phone".** It spends the one second that decides
retention on an instruction. Cropping and stacking both perform; friction does not.

## Text — two templates, pick by whether there is narration

Both live in `render_text_png`; `stroke` selects between them. Neither should be
redesigned — each was iterated against real reference videos.

**Silent quote card** (`stroke=0`, the default)

- **SF Rounded Semibold, 46px**, block max 780px wide
- **Centred at 40% height** — clear of TikTok's bottom bar and right rail
- **No box, no scrim.** Legibility comes from a soft blurred halo drawn from the
  glyphs themselves, invisible until it is needed
- **Ink follows the footage** — `sample_bg_luma` reads the actual crop at the
  actual timecode, because a sunset clip is bright sky up top and near-black
  where type lands. White below 0.62, near-black above

**Narrated captions** (`stroke=4`) — approved on the City 1 cut, font revised
on Sunset Sea Stack

- **Iowan Old Style Italic 44px** (`Iowan Old Style.ttc`, index 2) is the
  default for every narrated quote now — `render_narrated`,
  `render_narrated_cuts` and `render_narrated_stack` all default `font_path`
  to `FONT_QUOTE`/`FONT_QUOTE_INDEX` from `video_automation.core.vertical`.
  Chosen over Futura on the Sunset Sea Stack cut and kept as the standing
  default by the user's own call, on one clip or stacked — this **supersedes**
  the earlier "serifs and a stroke do not mix" finding below, which was true of
  Futura-vs-serif on that specific City 1 frame but was never re-tested once a
  flat band existed. Also tested against Gill Sans SemiBold, Seravek Medium,
  Avenir Next Medium Italic and Charter Italic
- **Futura Medium 44px** (`Futura.ttc`, index 0) is still there as
  `FONT_CAPTION`/`FONT_CAPTION_INDEX`, and is the right call if a specific cut's
  footage fights the serif — pass `font_path=FONT_CAPTION,
  font_index=FONT_CAPTION_INDEX` to override. Chosen originally against Avenir
  Next, Baskerville SemiBold Italic and Didot Bold: the stroke swallowed the
  thin strokes on every serif face tried at the time, over moving footage with
  no band behind the type
- **`y_frac` follows the frame, not a fixed number.** 0.50 on Hills Monument,
  where the horizon sits low; 0.34 on City 1, to clear the sun and skyline and
  put the type in open sky. Sample the crop and place the block in the emptiest
  band above the bottom UI — dead centre is a default, not a rule.
  **But the user's stated preference is centre**: 0.64 on Sunset Sea 2 was
  rejected as "lower half", and 0.50 approved in its place. Treat the emptiest
  band as the tie-breaker among centre-ish values, not a licence to drop low
- **White ink, solid black border.** Not the halo: captions move, so the type
  crosses whatever the footage is doing under it. One ink colour sampled from
  one frame will be wrong for some of the captions — the stroke is the only
  treatment that survives a line lying across a horizon
- **`max_w` is wider than the silent card on purpose.** A spoken phrase wrapped
  onto two lines reads as two thoughts. At 920px every phrase up to about eight
  words sets on one line; if one wraps, shorten the phrase rather than the font
- **One word may be coloured, pulled out of the footage.** `render_text_png`
  takes `ink=`; on the stroked template the black border carries legibility, so
  the fill is free. Approved on Sunset Sea Stack as `LUCKY` in `(255, 150, 60)`,
  the orange of the sun track. One word per script, the same word that gets the
  larger size — two coloured words is a theme, not an accent
- **`font_size` may be a callable** `(caption) -> int`, so the one word the quote
  turns on can be set larger than the lines around it. Size is the only emphasis
  left — the treatment is already white-on-black-stroke, so there is no weight or
  colour to reach for. **Approved on Sunset Sea 2** as `COLD` at 88px against a
  44px body, chosen over the same word at body size. Drop the comma from the
  caption — a set-piece word does not want punctuation hanging off it — but keep
  it in the spoken half so the engine still takes the breath. One per script, on
  the same turn that would otherwise get its own small caption

Both wrap with **no widows** — the wrap pulls a word back so the last line is
never a single orphan; that is the usual tell that a card was generated.

Copy style: lowercase, conversational, six to twelve words. Payoff in the second
half so the eye has to finish — that is what drives the rewatch.

**Open a narrated quote with "i read a quote that said".** Approved by the user
on City 1. It does more than add warmth: it promises a payoff, so the first
second buys the next nineteen, and it frames the line as something overheard
rather than something the channel is preaching.

**Put the quote itself in curly quotes** — `“` on the first quoted caption, `”`
on the last, and only around the quote, never the opener. Straight `"` sets as a
double-prime and looks like a typo. The marks go in the caption half of the
`(caption, spoken)` pair; the engine never sees them.

**Give one word its own caption where the line turns.** On City 1 the sequence
is "on an ordinary" / "tuesday." — the whole line is the deflation from spending
years chasing a feeling to something as small as a Tuesday, and holding the beat
before that word is what lands it. One or two per script, on the turn. Doing it
to every line is just slow, and `split_phrases` merges sub-three-word fragments
for exactly that reason — this is a deliberate override, not a new default.

**Write the quotes rather than sourcing them.** Aphorisms of this kind circulate
with confident but wrong attributions, and a misattributed line in a caption is
the sort of thing the comments catch. Original lines in the voice of a quote
carry the same weight with nothing to get wrong.

## Voiceover

Backends live behind `synth_phrase`, in quality order: **kokoro** (local,
unlimited, Apache 2.0, default), **edge** (Microsoft neural voices, free, no key,
but a network call and throttleable), **say** (macOS legacy, last resort).

Model files: `~/.local/share/kokoro` (~350MB). Installed as **kokoro-onnx**, not
the PyTorch `kokoro` package — that one depends on spacy, which has no Python
3.13 wheels and fails to build, and would add ~2.5GB of torch.

**Approved voice: `leo`** — `am_onyx` 0.60 + `af_nicole` 0.40 at speed 0.95 on
the soft chain. Chosen over three other blends and the previous default, tested
on two quotes and two clips.

```python
render_narrated(..., **profile_args("leo"))
```

**Always pass the profile explicitly.** `voice=None` still resolves to leo's
voice, but the mood defaults independently, so the defaults no longer describe
one coherent recipe. `profile_args` is the only call that keeps voice and chain
together — and half a profile is a different voice.

The previous default (`am_onyx` 0.60 + `am_puck` 0.40 on the melancholic chain)
was **retired** when leo was approved. The chain itself is still registered as
the `melancholic` mood, because shipped videos and CHANGELOG entries refer to
that sound — but no profile uses it now.

**Every voice lives in `video_automation/core/voices.py`.** A profile is the
whole recipe — voice, Kokoro speed and post chain — because those three are one
decision, not three. Profiles are named after people; the Kokoro voices
underneath are an implementation detail.

```bash
.venv/bin/python -m video_automation voices list        # all profiles
.venv/bin/python -m video_automation voices show leo    # full recipe
.venv/bin/python -m video_automation voices render leo  # sample to Desktop
```

**`status` is not a rating.** `approved` means it shipped in a finished video;
`candidate` means the user shortlisted it by ear and has not decided. Do not
promote one without being told to.

**Three alternates are kept for experiments**, not for shipping:

| profile | what it is |
|---|---|
| `max` | runner-up — leo's idea on `am_michael` instead of `am_onyx` |
| `noah` | even 50/50 split — the most breath that still reads male |
| `luna` | female. `af_nicole`, the only breathy voice Kokoro has, and the base inside all three blends |

Measured caveat on the blends: they lose most of luna's slowness — 10.2s at
speed 0.95 against luna's 11.7s at the *faster* 1.05. Whatever encodes that
character averages away in the sum.

**A voice is a `(510, 1, 256)` style tensor, not a model**, so a weighted sum is
a new speaker identity the model renders as one person — not two voices mixed as
audio. `voice_style()` accepts a name, a `{name: weight}` mapping, or `None`.
`Kokoro.create` takes the resulting array directly.

Why a blend: `am_onyx` was chosen by ear over five alternatives, but the model
card grades it **D on 10–100 minutes of data**, the weakest of the American
males. `am_puck`, `am_michael` and `am_fenrir` are all **C+ with hours**. The
60/40 keeps the onyx character on a steadier base, and was picked over straight
onyx and eight other mixes for sounding more human. Grades are in the model
card's `VOICES.md`; the best English voices overall are `af_heart` (A) and
`af_bella` (A−), both female.

**Kokoro cannot clone a voice.** No training or fine-tuning code has been
released, so blending existing embeddings is the ceiling without leaving Kokoro.
A small CC0 community collection exists at `n33kos/kokoro-voices`.

**Kokoro has no emotion parameter.** Mood comes from three stacked levers, and
the writing carries most of it:

1. **Script construction.** Motivational = short declaratives, hard consonants,
   imperatives, full stops as beats. Melancholic = long vowels, soft consonants,
   no imperatives, clauses that trail rather than land.
2. **Pace** — `KOKORO_MOODS`, roughly 0.80 sad to 0.95 motivational.
3. **Post-processing**, which does more than expected.

**The melancholic chain is approved and should be reused verbatim.** It is wired
into `POST_CHAINS["melancholic"]` and applied inside `synth_phrase`, before the
duration is measured — so the echo tail is counted and captions stay in sync:

```
asetrate=24000*0.96,aresample=24000,atempo=1.0417,
aecho=0.85:0.8:55:0.18,equalizer=f=250:t=q:w=1.5:g=2,loudnorm=I=-16
```

The ~4% pitch-down and the short echo tail are what sell it — without them it is
the same voice reading slower. The motivational treatment is **not yet approved**
and needs more work.

**Melancholic scripts need ~25% fewer words** than motivational ones for the
same runtime — slow delivery eats the budget fast. Roughly 30 words lands near
12 seconds at melancholic pace, useful as a sanity check when drafting.

## Utterance-final words get dragged, and it sounds like a glitch

Measured on the approved voice, the word "sky" in one line, only its position
and punctuation changed:

| position | duration |
|---|---|
| mid-sentence, no punctuation | **0.459s** |
| before a comma | 1.067s |
| ending its own sentence | 0.624s |

The user heard the comma version as "skyy" and flagged it as a glitch in the
voice. It is not a glitch — Kokoro applies phrase-final lengthening, and on an
open diphthong like `skˈaɪ` it stretches into something that sounds broken.
Long vowels are exactly what a melancholic script is full of, so this will
recur.

**The fix is the word's position, not the audio chain.** Kokoro is
deterministic, so re-rendering the same text reproduces the same drag exactly.
Move the word off the boundary: drop the comma, or add a word after it. A
second instance in the same script measured 0.747s before an `and`; changing
"look at the same sky" to "look **up** at the same sky" brought it to 0.520s.

Check any long-vowel word landing before a comma or a full stop:

```python
words = text.split()
ends = align_chunks(_synth_raw(text, voice, mood), words, voice, mood)
```

Anything over ~0.6s on a one-syllable word is the drag. Captions are free to
keep the comma — this only ever concerns the spoken half.

## Punctuation in the spoken half

Tested against measured audio, three finished renders compared by ear, and
**settled: keep writing with plain commas.** Do not re-run this.

Punctuation only affects the `spoken` half of a `(caption, spoken)` pair, so
none of it ever reaches the screen. Longest internal pause, one voice, one
line, only the mark changed:

| mark | pause | vs comma |
|---|---|---|
| nothing | 0.213s | — |
| comma | 0.235s | baseline |
| em dash `—` | 0.256s | +0.02s |
| ellipsis `...` | 0.299s | +0.06s |
| period | 0.341s | +0.11s |

**The ordering is real but the magnitude is not.** Em dashes and ellipses pause
longer than a comma by amounts too small to hear: a full render written with
them came out 10.46s against the comma baseline's 10.55s — *shorter*. They buy
nothing. The user compared all three and chose the plain-comma version.

**The period is the only mark that moves anything**, at 2–3× a comma. It costs
what it buys: a period makes Kokoro treat the clause as a sentence and give it
a terminal falling contour, which is exactly the robotic per-fragment delivery
that `sentences=` exists to avoid. Reach for it only when a line genuinely
needs a full stop.

**`--` is silently dropped.** Only the real `—` survives into the phoneme
string. Nothing warns you; you just get no pause.

**`!` buys a pause, not excitement.** It measured the same as an ellipsis.
Kokoro has no emotion parameter, so intensity comes from the writing, the pace
and the post chain — never from a mark.

**`gap` is the real lever.** At 0.65s between sentences it is roughly double
what any punctuation mark buys, and it is exact rather than inferred. If a line
needs a beat, split it into another sentence entry instead of decorating it.

None of these marks are ever spoken aloud — they stay punctuation in the
phonemes. ALL CAPS and bracketed emotion tags were not tested; keep avoiding
them.

## The reveal format

**An approved format, and the first one that gives a viewer a reason to rewatch
rather than a hope that they will.** Three beats:

1. `i read a quote that said` — the approved opener
2. a metaphor with a concrete vehicle — trees, rivers, weather, maps, gardens
3. `this is not about <the vehicle> btw` — **spoken, never shown**

Rewatch is the one thing this channel has hard evidence for: the hyperlapse
tutorial hit 180% retention and the best TikTok hit 228%. Both were watched
twice. This format engineers that instead of hoping for it.

**Let the footage run the misdirection.** The approved cut is `Forest Coast
Reveal 1` — a single continuous shot that tilts off dense canopy up to open
sunset sea. The trees leave frame by themselves, so the reveal lands on water
with no tree in shot. An earlier three-clip version was cutting to manufacture
exactly what that one clip already did continuously, and the cuts interrupted
the move that made the point. **Look for a clip that already performs the turn
before reaching for `render_narrated_cuts`.**

**Caption the kicker.** `("this is not about the sky, btw", "this is not about
the sky, by the way.")` — screen keeps the abbreviation, the engine gets the
words. The user asked for this on Sunset Sea Stack, and it reverses the earlier
rule: the kicker used to be an empty caption (`("", "...")`), voice only, so the
frame cleared and the line landed on the ear alone. It reads better on screen —
a muted viewer gets the payoff too, and on a looping short the last frame is
the one that has to sell the rewatch. The empty caption still exists in the
engine and is still the right tool when a line genuinely wants the frame to go
quiet; it is just no longer the default for the reveal.

**The pause before the reveal needs its own gap.** `gap=[0.65, 1.9, 0.65]` —
one value per sentence. A pause only reads as a beat if it is longer than the
pauses around it; at a uniform 0.65 the reveal landed as just another line.

**Abbreviations in the kicker are a phonemization trap.** `btw` comes out as
`bˌiːtˌiːdˈʌbəljˌuː` — Kokoro says "bee-tee-double-you" out loud. A casual
kicker invites exactly this, so `idk`, `fyi`, `rn`, `tbh` will all do it. The
`(caption, spoken)` pair fixes it; the point is to check the phonemes *before*
rendering, not after.

**Watch the runtime against the clip.** The approved cut leaves 0.18s of
headroom at `start=1.0` on a 17.5s clip. The render maps with `-shortest`, so
a video shorter than the audio truncates silently. Always ffprobe.

## Caption sync

**Use `sentences=`, not `phrases=`, for narrated quotes.** This reversed an
earlier decision, on real output.

Per-phrase synthesis (`phrases=`) gives exact sync by construction, but the
engine sees each fragment with no context, so every chunk lands with a terminal
falling contour and its own pause. The user's verdict on the City 1 cut was
"very robotic, especially the word 'years' and 'ordinary'" — and the finer the
captions, the worse it got, which is backwards. **Caption chunking and delivery
speed must not be the same knob.**

`sentences=` is a list of sentences, each a list of caption chunks. The sentence
is spoken *whole*, so the contour is a real sentence, and the chunk boundaries
are recovered afterwards by DTW-aligning it against throwaway solo renders of
each chunk on log-mel. No aligner model, no Whisper, no download — same engine
and voice on both sides, so the warp absorbs only the prosody that context added.

- **Boundaries land within ~0.19s** of a syllable-count expectation, and where
  they differ the alignment is the more credible one — it gives a pre-comma word
  its real length, which syllable counting cannot know. Chunks show for ~1s, so
  that error is invisible.
- **Trim the padding first.** Kokoro pads each solo render with silence; leaving
  it in shifted a boundary a full word early in testing.
- **Punctuation in the spoken half is the delivery.** Keep the comma on
  "tuesday," and the engine takes the breath. This is now the only way to get a
  pause inside a sentence — `gap` no longer applies there.
- **`gap` is between sentences only.**
- Captions are held until the next one starts, so an inter-sentence gap does not
  play over an empty frame.

`phrases=` is still right when the captions really are separate utterances.

Phrases under three words are merged forward by `split_phrases`; splitting on
every comma produced fragments that flashed past unread ("lost here," measured
0.65s).

**A natural read is much shorter than a chunked one** — the same script went
from 20.4s to 11.1s, because roughly 9s of it had been inter-phrase silence.
That is a real gain, not a shortfall: 10–19s is the channel's strongest bucket.
Do not pad silence to reach a number; write more quote instead.

**Pass `phrases=` for written verse.** `split_phrases` counts words, so a
nine-word line becomes "the things you'll miss are never" / "the things you
planned" — broken in the one place it must not be. Verse already carries its own
line breaks, and those are the right caption *and* speech boundaries.

**Heteronyms are spoken wrong and you will not hear it unless you check.**
espeak phonemizes from spelling, not context: `read` is `/ɹiːd/` in every
sentence, so "i read a quote that said" is delivered in the present tense. A
`phrases` entry may be `(caption, spoken)` — screen keeps `read`, engine gets
`red`. Same trap waits on *lead, live, wind, tear, close, bow, wound, minute*.

Check before rendering rather than after:

```python
_kokoro().tokenizer.phonemize("i read a quote that said", lang="en-us")
```

**`gap` is the honest runtime lever.** Speech length is fixed by the script, and
trimming words to hit a number is the wrong trade. Silence between phrases is
not: at melancholic pace ~1.0s reads as deliberate where the 0.18s default reads
as a list. Hills Monument is 13.4s of speech + 5×1.02s + 1.5s tail = 20.0s.

**The tail is real silence on the audio track**, not just a longer last caption.
The render maps the narration with `-shortest`, so a track shorter than the
reported total silently truncates the video — this shipped once, reporting
20.01s for a file that was 18.51s. Always ffprobe the output and report *that*.

**Keep the tail to 1–2s.** A short loops, and every second after the last word
is a second before it comes back around. `tail=1.2` is the working value; 2.2
was tried and the user cut it for exactly this reason. This is not in tension
with "do not shorten a pause to avoid silence" — that rule is about *dead air*,
and a fast loop is a different reason with a different answer.

**No fade to black.** Removed from `render_short`, `render_narrated` and
`render_narrated_cuts`; the chain now ends `null[vout]`. A fade spends the last
half-second telling the viewer it is over, which is the opposite of what a
looping short wants — the loop point should land on picture.

## Audio strategy

- **TikTok** — a trending sound is a real reach lever, and these renders are
  silent by default so nothing is lost. Export with no audio track at all so the
  platform treats the chosen sound as the only audio.
- **Shorts** — trends matter far less; own music is fine.
- **Voiceover competes with the trending sound.** They cannot both be the
  audio. Narrated shorts give up that lever and must earn it on retention.
- **Background music is added by hand after the render.** The pipeline outputs
  narration only. This is why long gaps and a long `tail` are not a problem —
  under music they read as room for the quote to breathe rather than as dead
  air, so do not shorten a pause to avoid silence that will not exist.

## One clip vs. two stacked

**Stacked is the default for a narrated quote with two clips.** Use
`render_narrated_stack`. Only cut sequentially (`render_narrated_cuts`)
when the user explicitly asks for one clip after another.

## Do not

- Exceed 30 seconds. Under that, report the runtime rather than forcing a number,
  and report the **ffprobed** runtime, not the one the builder returned.
- Ship pure scenery with no angle — it measurably does not work here.
- Redesign either text template; both were iterated against real references.
- **Trust `pick_crop` without looking at it.** On Hills Monument it chose x=24 —
  dense city texture on the far left outscored the hill, and the monument was cut
  out of frame entirely. Any clip with a lone subject against busy ground will
  fail the same way. Render a still from the chosen box and look before rendering.
- Claim an emotion was synthesised when it was pace and post-processing.
- Reach for em dashes, ellipses or exclamation marks to add feeling. Measured,
  compared by ear, rejected — plain commas won. See *Punctuation in the spoken
  half*.
- Apply the YouTube length and angle rules to TikTok. They were measured on
  YouTube and three of them are false there.
- Shorten a pause to avoid silence. Music is laid over the render by hand, so
  that silence does not survive to the upload. Trimming the `tail` for a faster
  loop is a different call and is wanted — keep it to 1-2s.
- Fade to black. Removed from the pipeline; a looping short should end on
  picture.
- Cut between clips before checking whether one clip already makes the move.
- Commit rendered MP4s to the repo — they are outputs. `assets/` is for reusable
  overlays only.
