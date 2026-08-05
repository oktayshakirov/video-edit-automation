---
name: video-drone-short
description: Make vertical short-form videos for TikTok and YouTube Shorts from drone footage — 9:16 crop, quote or motivational text, optional AI voiceover with synced captions. Use when the user runs /video-drone-short, asks for a TikTok or Short or Reel, wants a vertical or cropped version of drone footage, wants text or a quote over a clip, or wants narration read over footage. For long-form YouTube edits cut to music, use video-drone-long instead.
---

# Drone Automation — short form

Renders finished vertical MP4s. **This is the one part of the project that
renders video**; the long-form pipeline (`video-drone-long`) only writes FCPXML.

**Repo:** `~/coding/video-drone-long-automation` — run from there.
Footage must already be indexed: `.venv/bin/python -m drone_automation index <folder>`
(shared with `video-drone-long`; the proxies and clip index are the same).

## What the channel's own numbers say

Do not re-derive these. Pulled from the real channel, and they decide the format.

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
from drone_automation.vertical import pick_crop, render_text_png, render_short, sample_bg_luma
from drone_automation.voiceover import render_narrated
```

Silent quote card:

```python
box  = pick_crop(proxy, zoom=1.45)              # zoom only for wide landscapes
luma = sample_bg_luma(src, box, mid_timecode)
png  = render_text_png(text, tmp/"t.png", bg_luma=luma)
render_short(src, out, start, 12.0, box, png)
```

Narrated with synced captions:

```python
render_narrated(src, out, start, box, script, workdir, mood="reflective")
```

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

**Never use "rotate your phone".** It spends the one second that decides
retention on an instruction. Cropping and stacking both perform; friction does not.

## Text template — settled, do not redesign

Matches the genre the user referenced. A lower-third with a scrim was tried
first and rejected.

- **SF Rounded Semibold, 46px**, block max 780px wide
- **Centred at 40% height** — clear of TikTok's bottom bar and right rail
- **No box, no scrim.** Legibility comes from a soft blurred halo drawn from the
  glyphs themselves, invisible until it is needed
- **Ink follows the footage** — `sample_bg_luma` reads the actual crop at the
  actual timecode, because a sunset clip is bright sky up top and near-black
  where type lands. White below 0.62, near-black above
- **No widows.** The wrap pulls a word back so the last line is never a single
  orphan; that is the usual tell that a card was generated

Copy style: lowercase, conversational, six to twelve words. Payoff in the second
half so the eye has to finish — that is what drives the rewatch.

## Voiceover

Backends live behind `synth_phrase`, in quality order: **kokoro** (local,
unlimited, Apache 2.0, default), **edge** (Microsoft neural voices, free, no key,
but a network call and throttleable), **say** (macOS legacy, last resort).

Model files: `~/.local/share/kokoro` (~350MB). Installed as **kokoro-onnx**, not
the PyTorch `kokoro` package — that one depends on spacy, which has no Python
3.13 wheels and fails to build, and would add ~2.5GB of torch.

**Approved voice: `am_onyx`.**

**Kokoro has no emotion parameter.** Mood comes from three stacked levers, and
the writing carries most of it:

1. **Script construction.** Motivational = short declaratives, hard consonants,
   imperatives, full stops as beats. Melancholic = long vowels, soft consonants,
   no imperatives, clauses that trail rather than land.
2. **Pace** — `KOKORO_MOODS`, roughly 0.80 sad to 0.95 motivational.
3. **Post-processing**, which does more than expected.

**The melancholic chain is approved and should be reused verbatim:**

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

## Caption sync

Each caption phrase is spoken as its own file and shown for exactly its
**measured** duration. Sync is exact by construction — no aligner, no Whisper,
no drift — and because timing is measured rather than predicted, changing TTS
engine cannot desynchronise the captions.

Phrases under three words are merged forward; splitting on every comma produced
fragments that flashed past unread ("lost here," measured 0.65s).

Video length follows the narration, so **the script is what controls runtime**.
Stay under 30 seconds; beyond that, say what it is costing.

## Audio strategy

- **TikTok** — a trending sound is a real reach lever, and these renders are
  silent by default so nothing is lost. Export with no audio track at all so the
  platform treats the chosen sound as the only audio.
- **Shorts** — trends matter far less; own music is fine.
- **Voiceover competes with the trending sound.** They cannot both be the
  audio. Narrated shorts give up that lever and must earn it on retention.

## Do not

- Exceed 30 seconds. Under that, report the runtime rather than forcing a number.
- Ship pure scenery with no angle — it measurably does not work here.
- Redesign the text template; it was iterated against real references.
- Claim an emotion was synthesised when it was pace and post-processing.
- Commit rendered MP4s to the repo — they are outputs. `assets/` is for reusable
  overlays only.
