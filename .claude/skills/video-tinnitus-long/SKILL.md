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

## Open on a face, moving

The first cut opened on a still of a worried woman and the note back was that it
is not an engaging way in. A **clip** of someone visibly dealing with it reads
instantly, needs no caption, and costs nothing — `headache-stress-tired-woman-dark`
screened at L46/S22. For a health topic the opening frame should be a person, not
a concept.

## What differs from crypto

**Voice is `mia`** — the same reader as the crypto long-form. The user's call.
`luna-calm` is the sound-therapy voice and belongs to mode 2.

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

The same height difference drives the **photo-border dodge** described in
`/video-crypto-long`: a picture that fits the frame is pushed down (or slightly
scaled) so its gold hairline never crosses the mark, while a full-frame picture
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

## Do not

- **Make medical claims, in either mode.** The one rule above all others.
- Write copy that oversells what a bed masks without running `band_energy`.
- Promote a candidate voice to approved. `mia` and `luna-calm` are both
  candidates.
- Present the app's zen albums as available — the audio files are not on disk.
- Mass-produce. Same cap as crypto: see `docs/long-form-strategy.md`.
