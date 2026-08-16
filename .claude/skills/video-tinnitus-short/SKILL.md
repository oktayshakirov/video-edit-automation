---
name: video-tinnitus-short
description: Make vertical short-form videos for TikTok, YouTube Shorts and Instagram Reels for tinnitushelp.me — article shorts with voiceover and synced captions, plus ASMR sound-therapy shorts. Use when the user runs /video-tinnitus-short, asks for a tinnitus short or Reel, wants a post from tinnitushelp.me turned into a video, wants sound therapy or masking or notched-audio content, or wants to pick or tune the tinnitus voice. For drone footage shorts use video-drone-short instead.
---

# Tinnitus Help — short form

**Repo:** `~/Coding/video-edit-automation` — run from there with `PYTHONPATH=.`.
Renders go to the Desktop; they are uploads, not repo artifacts.

**Source content:** `~/Coding/tinnitus-blog/content` — 75 posts plus a `zen/`
section documenting the brand's own released sound albums.
**There is also an app** — `~/Coding/tinnitus-app`.

## Two formats, and they are not the same job

1. **ASMR / sound-therapy shorts** — **built**, in `video_automation/tinnitus/asmr.py`.
   The rest of this file is about that one.
2. **Article shorts** — **built**, in `video_automation/tinnitus/article.py`.

The sound-therapy format is the one with a real reason to exist here: the audio
*is* the product, so it is not a talking head competing with a million others.
Tone-matching ("which frequency matches yours?") is the obvious next variant and
needs tone synthesis the repo still does not have.

## Article shorts

```bash
PYTHONPATH=. .venv/bin/python projects/tinnitus/gaming-and-tinnitus.py
```

`render_tinnitus_short` is `render_crypto_short` with two values passed in
rather than hard-coded — the `Brand` its beats and clips are drawn with, and
the watermark, which on this site is a lockup assembled at render time instead
of a file on disk. **Both default to crypto, so the shipped crypto shorts stay
byte-identical.** There is no second pipeline and there should not be one.

**The mark is `Brand.mark()` at `mark_scale`, which is 0.42** — 134px wide in a
9:16 frame, down from 186. It came down because a square lockup pushes a fitting
photograph down the frame and then shrinks it; that bites in landscape and not
here, since a 9:16 photograph sits ~490px down and never reaches the mark. The
ASMR shorts are on their own lockup path (`asmr.brand_lockup`, 100px face) and
are untouched by any of this.

**Voice is `mia`**, the tinnitus long-form reader — a short and a long video on
one channel reading in two different voices is two channels. `luna-calm` is the
sound-therapy voice and belongs to `asmr.py`. Both are still candidates.

**Do not use `checklist` here.** `ChecklistShot` is the vertical-native beat and
it is the one drawn object still carrying thecrypto.wiki's gold as a module
constant, so it renders off-brand and nothing raises. The portrait-safe beats
that take a brand are **`grid`, `steps` and `bars`** — and anything else now
raises rather than falling through. It used to fall through to `ChecklistShot`,
which is how `bars` first "shipped": it happened to blow up unpacking a
three-tuple as `(text, ok)`, and a two-element payload would have drawn the
wrong beat silently.

**`bars` needs a frame-dependent fraction.** The value text travels with the end
of its own bar, so a long top bar pushes it off the right edge. The same data
took 0.90 at 1920 and 0.60 at 1080. Scale the whole set by one factor and the
proportions between rows — the only thing the beat claims — stay exact.

### Inherited from the crypto short, and paid for there

- **Stock clips are allowed and the piece should open on one.** The crypto skill
  used to ban reaching for a stock API and that rule was reversed on review: a
  short built only from the site's photographs was judged boring, because eight
  Ken Burns pushes in a row is one move repeated eight times, and because a site
  library frequently owns no picture of the actual subject. **Stock supports;
  the site's images and the drawn beat lead.** Half the shots is comfortable,
  all of them is the failure both platforms suppress.
- **This bites harder here than on crypto.** tinnitushelp.me has 110 images
  across 69 posts — 2–3 per post against crypto's 3–5 — and its median source is
  **750px**, right on the floor the blurred-fill layout needs. The picture
  problem the reversal solves is strictly worse on this site.
- **Screen a clip across its length, not at one frame**, and remember hue is a
  separate judgement from the luma/saturation box.
- **A clip in a short carries no label** — the burned caption already is the
  statement, and a label prints the same words twice.
- **`grid` and `steps` have portrait layouts now** — one column of wide cards,
  and a track that runs down rather than across. Use them so two drawn beats in
  one short do not read as the same graphic twice; `steps` is right whenever the
  content has an order.
- **Cut between a drawn beat and a clip**, keep dissolving into a photograph. A
  dissolve slides type across moving footage and reads as a fault.
- **`flow` marks each checklist item as it is spoken**, for narration that
  carries the verdict itself. It needs a much shorter gap than the two-phase
  default.
- **Put a beat's lead-in question in the sentence before it**, never inside the
  beat's own span, or it eats the first reveal.

**None of this applies to the sound-therapy format below**, and that is worth
being explicit about rather than assuming: `nebula_canvas` is procedural,
infinite, on-brand and licence-free, so the ASMR shorts never had the picture
problem the reversal exists to solve. **Do not add stock footage to an ASMR
short.** Its picture is deliberately calm and unchanging because the audio is
the product and a cutting picture track fights it.

## Building one

```python
from video_automation.tinnitus.asmr import render_asmr_short

out, total = render_asmr_short(
    INTRO, OUTRO,                  # sentence lists, same shape as the drone quotes
    low=Path("SpaceshipAmbience.mp3"),   # the deep bed
    high=Path("NebulaPulse.mp3"),        # the layer that does the masking
    out=Path("~/Desktop/tinnitus-breathe-60.mp4").expanduser(),
    workdir=work,
    cycles=3, inhale=4.0, hold=0.0, exhale=6.0,
)
```

Three layers, built in this order because each one's timing depends on the last:
narration (measured, via `build_narration_aligned`) → the breathing block dropped
into the gap between the two narration halves → the picture, generated to the
total.

**The two narration halves are synthesised separately, and must stay that way.**
One call with a very long `gap` looks equivalent and is not:
`build_narration_aligned` holds every caption until the next one starts, so the
last intro line would sit on screen across the whole breathing block, on top of
the ring.

**Always ffprobe the output.** The mux runs `-shortest`. `render_visual`
deliberately renders half a second of extra picture so an off-by-a-few-frames
video cannot silently clip the end of the audio.

## The audio bed — layer both files

Measured on a 30s sample, and this is why both are needed:

| track | centroid | <200 Hz | >4 kHz |
|---|---|---|---|
| SpaceshipAmbience | 128 Hz | 86.8% | 0.1% |
| NebulaPulse | 807 Hz | 63.1% | 6.5% |

SpaceshipAmbience is a beautiful floor that masks nothing in the band tinnitus
actually occupies. NebulaPulse carries the mid and upper content. `render_bed`
layers them.

**Honest limit, and do not write copy that contradicts it:** even mixed, there
is very little energy above 4 kHz, so a high whistling tinnitus will not be well
covered by these two files. That is a property of the tracks, not the method.

**Ducking is measured, not eyeballed.** The bed at -20 LUFS left only 3 dB over
the narration, which is not intelligible; the bed is now `loudnorm=I=-23` with a
`sidechaincompress` at `threshold=0.03:ratio=8`. Sidechain rather than a static
mix because the bed should be at full strength through the breathing block,
which is most of the piece, and step back only where there are words.

## The picture

Procedural, in `nebula_canvas` — no stock, no licence, regenerable at any length,
and on-brand by construction because the brand's own album is *Quiet Universe*
and its artwork is space. The palette is lifted straight from the app's
`constants/Colors`: `#5B3964` background, `#ffdab9` highlight, `#ffd2a6` ring.

- **The drift must be subpixel.** It moves tens of pixels per second, so an
  integer crop jumps a whole pixel every few frames and holds still in between.
  The user's word for the first cut was "laggy". `cv2.warpAffine` at
  `INTER_LINEAR` costs a few ms a frame and fixes it completely — verify with a
  frame-difference check that no two consecutive frames are identical.
- **The ring's rim glows; its fill does not.** Blurring a filled disc put a haze
  over the whole circle and the nebula behind it went to mud. The disc has to
  stay a window onto the background.
- **Stars need a linear distribution, not a cube law.** The first pass cubed the
  faint population and they vanished entirely once the video was scaled to a
  phone.
- Frames are piped to ffmpeg as rawvideo. A minute at 1080x1920 is 1800 PNGs and
  none of them are wanted afterwards.

**The watermark is an upper-left lockup, inset below the chrome band** — the
mascot with `TinnitusHelp.me` under it, `brand_at=(58, 292)`, 100px face, 27px
wordmark, **full opacity**. Two placements were rejected getting here: flush to
the corner, which is where TikTok's LIVE button and Instagram's camera sit; and
dead centre, which reads as part of the piece rather than as a mark. Inset to one
side is a watermark and is still safe.

**Do not dim it.** A watermark nobody can read is not a watermark, and the point
of carrying the domain is that it is actionable.

**It levitates** — `brand_float=9px` on a `brand_period=5.5s` sine. A static mark
in a corner is dead weight the eye skips in about two seconds. The period shares
no factor with the 10s breathing cycle, so it never syncs up into a second thing
to follow. **The bob has to be subpixel too**: it peaks near 10px/s, so rounding
to whole pixels stutters the logo against a background that no longer does.
Verified at 11.07px peak-to-peak travel with zero identical consecutive frames.

**Safe area, all three platforms, at 1080x1920:** `SAFE_TOP=230`,
`SAFE_BOTTOM=1440`, and keep clear of roughly `x>860`. `render_visual` raises if
the lockup's *float-adjusted* top crosses `SAFE_TOP`, rather than letting it ship
covered.

**Next: make the watermark roam.** Requested after the first cut and not built
yet. Hold it upper-left for a stretch, cut to bottom-right, cut back — the way
TikTok's own download watermark moves. Two reasons it is worth doing: a mark that
moves is much harder to crop out of a reposted video, and a mark that changes
position resists the eye's habit of learning where to ignore.

Building it, the constraints already established here apply and one is new:

- Both anchors must sit inside the safe box, which for the bottom-right corner is
  the tight one — the right rail runs to about `x=860` and the caption block
  starts around `SAFE_BOTTOM=1440`, so the lower anchor wants roughly
  `(820 - lockup_width, 1300)` rather than a true corner. Validate both anchors
  the way `brand_at` is validated now, not just the first.
- **Cut between positions, do not slide.** A lockup travelling across frame is a
  second moving object competing with the ring, which is the one thing the viewer
  is supposed to follow. TikTok cuts for the same reason.
- Keep the levitation running at each anchor; it is what stops the mark reading
  as a sticker.
- Hold each position long enough to be read — 10-15s is the range worth trying
  first, and the hold should not divide evenly into the breathing cycle.

The domain carries the plug, not the face alone: the site prompts for the app
install on arrival, so one legible URL does the job the end card was doing. The
mascot is cropped live from `tinnitus-app/assets/images/splash-icon.png` — take
the top 82% of the asset, because `getbbox` alone includes the faint wordmark
underneath the face.

## Copy

Captions use the drone skill's stroked template — Futura Medium 44px, stroke 4,
centred at `y_frac=0.50`. Pass `max_w=CAPTION_MAX_W`; `render_text_png` defaults
to the silent quote card's narrower 780px and will wrap a line that would
otherwise have set on one.

**Emoji go through `add_caption_emoji`**, a second pass over the finished PNG —
`render_text_png` is shared with the drone shorts and is not to be redesigned.
The text layer shifts left by half the emoji block so the pair stays centred as
one unit. Apple Color Emoji is a bitmap font that only loads at the sizes it has
strikes for (32/64/96/160 work; 44 and 137 raise "invalid pixel size"), so it is
rendered at 160 and scaled down. Single-line captions only.

**The angle is partial masking**, straight out of
`content/posts/brown-noise-vs-white-noise-for-tinnitus.mdx`: set the sound just
below your tinnitus so you can still faintly hear it. It is useful,
counterintuitive, and it is the reason to watch rather than scroll. Burying the
sound completely is what most people do and what the post argues against.

**Open on the hook with no lead-in silence.** A silent opening frame is a
scroll-past; `lead_in` defaults to 0.

**No end-card promo.** The user's call: a curious viewer will find the page, and
the link goes in the description. The persistent lockup is the only on-screen
plug.

## Voice

Six profiles, all reproducing their audition WAVs sample-for-sample:

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices show luna-calm
.venv/bin/python -m video_automation voices render felix
```

| profile | recipe | note |
|---|---|---|
| `luna-calm` | female, `af_nicole` 0.90, soft | **the one used by the built format** |
| `luna` | female, `af_nicole` 1.10, energetic | the only breathy voice Kokoro has, and the base for every profile here |
| `elias` | 12% down, time restored | |
| `felix` | 16% down, time restored | |
| `jonas` | 12% down, slowdown kept | no time-stretch artifacts |
| `caspar` | 16% down, slowdown kept, aspiration boost | most processed of the set |

**None is approved.** `luna-calm` is what the sound-therapy short is built on and
is still a candidate until the user says otherwise. It exists because `luna` runs
1.10 through ENERGETIC — a chain built to punch on a phone speaker — which is the
wrong instrument for a piece the listener is meant to breathe along with. SOFT is
the chain that exists for ASMR.

elias, felix, jonas and caspar are all luna pitched down. They exist because
**Kokoro has no male breathy voice** — measured, not assumed. All twelve male
voices ran 11.7–16.2s where `af_nicole` ran 23.3s on the same script.
Cross-gender style blends were tried and lose the character: they came in
*shorter* at a slower speed setting. Pitching luna down keeps 100% of the breath
by construction. Kokoro has released no fine-tuning code, so blending and DSP are
the whole ceiling.

**Open risk:** a pitch-shifted female voice can read as "a processed woman"
rather than "a man". No measurement settles that; only the user's ear does.

**Check phonemes before rendering, not after** — same espeak traps as the drone
skill. `tinnitus` is fine (`tˈɪnɪɾəs`). Abbreviations are not.

## Audio strategy

Unlike the drone shorts, **do not export silent for a trending sound.** The bed
and the voice are the content; a trending sound would replace the thing the
viewer came for.

## Do not

- Make medical claims. YMYL niche — describe partial masking and paced breathing
  as things people do, never as treatment, and never imply a cure.
- Promote a candidate voice to approved without being told to.
- Use `checklist` in an article short — it is the one beat still hard-coded to
  the crypto palette.
- Default to driving traffic to the blog. **App install is the far better
  conversion from short-form**, and the only path here with a plausible route to
  revenue.
- Write copy that oversells the masking these two tracks can actually do above
  4 kHz.
