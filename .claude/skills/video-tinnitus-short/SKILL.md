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
PYTHONPATH=. .venv/bin/python projects/tinnitus-short/gaming-and-tinnitus.py
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

**The voice matches the long form from the same post, always** — a short and a
long video on one channel reading in two different voices is two channels. That
was `mia` for the gaming pair and is **`mia-calm`** for the sleep pair. `ivy`
(bf_emma) was tried and **deleted from the roster** — the British read was not
wanted on this channel, and a rejected voice left in the list is one somebody
picks again by accident. `luna-calm` is the sound-therapy voice and belongs to
`asmr.py`. All are still candidates.

**Drawn beats now sit on the brand background, not a drifting grid** — see the
long-form skill for `core/backdrop.py`. Nothing to pass per shot; `Brand`
carries it. It matters here because the shorts share `longform/beats.py`, so
the vertical beats changed too, and the square 512px asset is what makes one
background serve both aspects.

**Length: 40-50s, not 30.** The first sleep cut came in at 32s and the note was
to extend it. There was room — the reframe alone does not fill a short, and the
counterintuitive turn (chasing quiet backfires) is what keeps a viewer past the
first line.

**Shorts get a thumbnail now, and it does not use the landscape treatment.**
`thumb.render_short_thumb`, 1080x1920. Two things were wrong with reusing
`render_thumb`'s type: Futura Medium is a light, wide geometric that goes weak
at feed size, and an 8px black stroke around every glyph is the clearest tell
of an amateur thumbnail — "the font is not good and looks very generic", "our
solid color borders make it look very unprofessional". So it sets **Arial
Black** (the closest face on this machine to the Anton/Montserrat-ExtraBold
weight big channels use; Impact is heavier and was rejected as meme-coded) with
a **blurred drop shadow on its own layer instead of a stroke**, and a tighter
accent plate.

**Fetch the source with `orientation=portrait`.** A landscape photo cover-
cropped to 9:16 throws away the subject's long axis and no zoom or pan
recovers it — the long form's thumbnail once did exactly that.

**The long form now uses this same photo, and that is the rule going
forward: one source for both aspects, always.** `render_thumb` takes
`crop_at`/`crop_zoom` to place a manual landscape crop of a portrait source by
hand, since `_layout`'s automatic scorer optimises for empty space rather than
for the subject being visible and will happily crop the face out of frame. See
the long-form skill's `crop_at` section. Type sits in the upper half here,
because the Shorts player puts the title, channel and buttons across the
bottom and a button rail up the right.

**The article shorts still have no music bed** — long form gets one, this does
not. Requested and not yet built; `render_tinnitus_short` would need the
`music`/`music_gain` pair `render_long` already takes.

**Do not close on "save this".** Asking for a save is asking for the wrong
action when the video is about something to do tonight — the user's call, and
they are right that saving a video is not the behaviour the piece is arguing
for. Close on the action itself: "Try it tonight."

**`checklist` works here now, and it is the beat worth reaching for.** This file
used to say "do not use it": `ChecklistShot` was the last drawn object holding
thecrypto.wiki's gold as module constants, so the strongest and most
vertical-native beat in the format was ruled out on this site by a hard-coded
colour that would have rendered off-brand with nothing raising. It takes a
`Brand` now, like `grid`, `steps` and `bars` always did, and
`render_tinnitus_short` passes it. The portrait-safe set is **`checklist`,
`grid`, `steps` and `bars`**; anything else raises rather than falling through.
It used to fall through to `ChecklistShot`, which is how `bars` first "shipped":
it happened to blow up unpacking a three-tuple as `(text, ok)`, and a
two-element payload would have drawn the wrong beat silently.

**Watch the tick.** The brand's accent is `#ffdab9`, a pale peach, and against
white item text it carries much less contrast than gold does on the crypto
cut — the payoff mark reads weaker than the crosses that precede it. Look at
the frame before approving a checklist here. If it does not land, the fix is
the brand's `primary`, not a special case inside the beat.

**The photographs' hairline was gold too**, on every tinnitus short and every
tinnitus long-form video, for the same reason. `PhotoShot` takes the brand now.
Anything rendered before this is off-brand at the photo edges.

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

**The watermark can roam, and it is built.** Pass `roam=True` to
`render_asmr_short` or `render_tinnitus_short` (and `render_crypto_short`); it
holds the mark upper-left, cuts to lower-right, cuts back, the way TikTok's own
download watermark moves. Off by default, so every shipped cut is unchanged.
Two reasons to turn it on: a mark that moves is much harder to crop out of a
reposted video, and a mark that changes position resists the eye's habit of
learning where to ignore.

- **`logo_hold` defaults to 13s**, inside the 10-15s range and sharing no factor
  with the 10s breathing cycle or the 5.5s levitation period, so the jump never
  lands on the same phase twice.
- **It cuts between positions, it does not slide.** A lockup travelling across
  frame would be a second moving object competing with the ring, which is the
  one thing the viewer is supposed to follow.
- **The levitation keeps running at each anchor** — it is what stops the mark
  reading as a sticker.
- `crypto.shots.roam_anchors` places the lower-right one. It is the tight
  corner: the right rail runs to `safe_right=860` and the caption block starts
  at `SAFE_BOTTOM=1440`, so it is set against those with 40px of air rather
  than against the frame's real corner, which is under the share button on all
  three platforms. **Every anchor is validated, not just the first** —
  `Frame.check_mark` checks all four edges where `check_top` checked one.
- Verified anchors: crypto logo `(58,268)`/`(520,1353)`, the tinnitus article
  lockup `(58,268)`/`(686,1262)`, the ASMR lockup `(58,292)`/`(622,1242)`.

**Still worth a look on the first real cut:** the lower-right anchor is only as
far right as `safe_right` allows, which for the 300px crypto mark is x=520 —
nearer the middle of the frame than a corner. It reads fine in a still. If it
reads as floating in motion, the lever is a narrower mark, not a wider safe box.

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


## Rules that arrived from the crypto side (2026-08-18)

All four of these are engine-level or cross-channel; they were found on
`crypto-exchanges` and they apply here unchanged.

**Silence is punctuation, and it has to be written.** `gaps` on the `Section`
(or the `gap` list in a short), one float per sentence. Leaving every sentence
at the default 0.34 is what "monotone" means — pace is the only prosody a
synthesiser has. 0.34 inside a thought, 0.45-0.60 at the end of one, 0.70-0.90
before a line that has to land, 2.10-2.40 for a two-phase beat. **Longer than
1.3 outside a beat is a hole, not a pause.**

**Music: `assets/brand/music/` is one library for both sites.** The tracks are
brand-neutral and the user's call is that a bed picked by ear beats a generated
one that only measures correctly. `music.track("night-drift")` is on both
channels now. Add another with `music.prepare_track`, which trims both ends —
untrimmed encoder delay becomes a hole in the bed once per loop.

**A ping-pong background must not fold at frame zero.** `pingpong` now drops one
frame from each end of the reversed half and `Backdrop.at` samples from a
quarter of the loop in, because a palindrome's turnaround is the one moment
motion stops and every video was opening on one. Only the crypto water was
affected — the aurora is generated on closed circular paths and has no fold —
but re-measure any new footage background the same way: step series over the
whole loop including the wrap, minimum must not land at a fold.

**Check phonemes with espeak rather than guessing.** Kokoro phonemizes through
espeak-ng, so `espeak-ng -v en-us -q --ipa "<word>"` is the whole check. It
caught a brand name that shipped mispronounced. Put any respelling in the
**spoken** half of a `(caption, spoken)` pair so the screen still reads
correctly.

**Thumbnails: three checks, every time.** The subject fits — no half faces at
the frame edge, and `_layout` now penalises a crop that cuts a detected face.
The type is not over the face — in 9:16 there is no search at all, so pass
`band="bottom"` whenever the head is in the top half of the crop. And the words
are the script's own words.

**Only a hyphen goes on screen.** Never an em or en dash in a spoken line or a
caption, on any channel — at caption size a long rule reads as a stray mark, and
it is a flourish in a place that wants plain type. Write `-`.

**A statement card needs a line handing off to it.** A full-screen card that
arrives with nothing in front of it reads as a title card dropped into the
middle of the video; one sentence makes it the thing the piece was building
toward.

**Two beats joined the portrait set**: `logos` (brand tiles, 2x2, optional
tick/cross badges) and `chapter` (a full-screen statement at 148px, which is the
strongest way a short can land its closing line). `compare` takes
`name_columns=True` in landscape, which makes each heading its own revealed item
so the graphic follows the voice instead of asking the viewer to interpret.

## Do not

- Make medical claims. YMYL niche — describe partial masking and paced breathing
  as things people do, never as treatment, and never imply a cure.
- Promote a candidate voice to approved without being told to.
- Add stock footage, a roaming watermark or any other cutting element to an
  **ASMR** short's picture. `roam` is available there and is the one exception
  worth considering, because it is a crop-resistance measure rather than a
  visual one — but the picture is deliberately calm and every extra moving
  thing fights the audio, which is the product.
- Default to driving traffic to the blog. **App install is the far better
  conversion from short-form**, and the only path here with a plausible route to
  revenue.
- Write copy that oversells the masking these two tracks can actually do above
  4 kHz.
