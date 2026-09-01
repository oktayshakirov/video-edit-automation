# Project: tinnitushelp.me

Source site `~/Coding/tinnitus-blog`. Two products that share an engine: the
article explainer (long + Short pair) and the sound-therapy session.

## What differs from crypto

**The article-explainer voice and the sound-therapy voice are different
families, and mixing them up costs a rewrite, not just a re-render.** Measured
on one paragraph: the pitched-down family (`elias`) reads at 1.97 words/sec,
the explainer default (`mia`) at 3.06. A script written for one and read by
the other misses the runtime window by up to ninety seconds. `otis` (the male
explainer voice, bare `am_puck` at speed 1.00) sits close to `mia` but reads
a little slower and calmer. **Re-run the preflight after any voice change** —
do not assume the shot list survives it.
Full roster and roles are in *Voice*, below.

**`ivy` (bf_emma) was tried here and deleted from the roster entirely.** The
British read was not wanted on this channel, and a rejected voice left in the
profile list is one somebody picks again by accident. If a voice is out, take
it out of `core/voices.py` rather than noting it here.

**A short and the long video from the same post use the same voice** — two
voices on one channel is two channels.

## Ask which one first

**This skill makes two different videos and they share almost nothing but the
brand.** Always establish which before doing anything else:

| | **article** | **sound therapy** |
|---|---|---|
| what it is | a post explained | a session to leave running |
| runtime | 2:30–4:00 | 10–60 minutes |
| voice | **`mia`** (female) or **`otis`** (male) | **`luna`**, intro only |
| module | `longform/build.py` | `longform/asmr.py` |
| example | `projects/tinnitus-long/does-tinnitus-go-away.py` | see below |

If the user has not said, ask. Do not guess from the topic — "brown noise vs
white noise" is a legitimate article *and* a legitimate session.

---

# Mode 1 — article videos

**Read `.claude/skills/docs/video/longform.md` first.** It is the same
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

## Two formats, and they are not the same job

1. **ASMR / sound-therapy shorts** — **built**, in `video_automation/tinnitus/asmr.py`.
   The rest of this doc is about that one.
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
long video on one channel reading in different voices is two channels. Full
roster and roles are in *Voice*, below; the pace-mismatch measurement is in
*What differs from crypto*, above. Nothing here is specific to the short.

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

**Superseded in part - see "Put the title's own question on the thumbnail"
below, which replaced the "point at the part of the answer they do not have"
half of this. What survives is the first sentence.**

**The thumbnail must not answer the video's own question.** "Not the earbuds.
The volume." shipped on the AirPods pair and the user's note was that it
answers the title directly, so there is no point watching. The title carries
the search phrase and asks; **the thumbnail points at the part of the answer
the viewer does not have yet** — "The warning everyone ignores" — so reading it
creates the question instead of closing it. This is the sharper form of the
long skill's "ask what the title does not": not merely a different sentence, a
sentence that cannot be acted on without the video.

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

**`band="bottom"` clears the view count, and the clearance is already in the
renderer — do not re-tune it.** The bottom margin was `int(VH * 0.16)` and the
last line of type ran straight through the play-count YouTube draws across the
bottom of a Short's grid tile, so the user was opening the artwork and nudging
it up by hand before every upload. `render_short_thumb` now adds 20px to the
bottom band only. If a bottom-banded thumbnail ever looks slightly high in
isolation, that is correct: it is composed against a platform overlay that is
not in the file.

**Article shorts take a music bed, and it is the default now — pass nothing.**
Standing instruction from the user. `render_tinnitus_short` forwards `music` /
`music_gain` to `render_crypto_short`, which now **defaults** `music` to
`music.track("night-drift")` and `music_gain` to `0.85` — a build that passes
neither still gets the bed. A long video and the Short from the same post sit on
the same track at the same relative level instead of being mixed twice by hand.
Pass `music=None` to opt one short out; see `audio.md`.

Gain slightly under the long form's: a short is watched on a phone speaker with
the voice carrying all of the information. **It matters more here than in long
form, not less** — a short opens with no lead-in silence and is judged in its
first second, and forty seconds of synthesised speech over nothing sounds like
a voice memo. It also covers the written pauses, which is why the sidechain is
the right shape rather than a static mix now that the pauses are deliberate and
long.

**Do not close on "save this".** Asking for a save is asking for the wrong
action when the video is about something to do tonight — the user's call, and
they are right that saving a video is not the behaviour the piece is arguing
for. Close on the action itself: "Try it tonight." — and nothing after it: no
"let me know in the comments", no "subscribe". That is `narration.md`'s outro
rule; a how-to closes on the action where an argument closes on the question,
but neither appends a viewer-management line.

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

**The beat draws the brand background now, not the ruled grid.**
`ChecklistShot` was the last drawn object still painting
`int((f * 40) % 96)` lines, because `render_shots` builds it directly rather
than through `longform.beats` and it therefore never saw a `Brand.backdrop`.
The symptom that found it was one 44-second short whose `checklist` drew a navy
grid and whose `bars` ten seconds later drew the galaxy. Fixed; shipped crypto
shorts using `checklist` will look different if re-rendered, which was accepted.

**Watch the tick.** The brand's accent is `#ffdab9`, a pale peach, and against
white item text it carries much less contrast than gold does on the crypto
cut — the payoff mark reads weaker than the crosses that precede it. Look at
the frame before approving a checklist here. If it does not land, the fix is
the brand's `primary`, not a special case inside the beat.

**The photographs' hairline was gold too** - see *The brand mark, and what its height costs the picture* below.

**`bars` needs a frame-dependent fraction.** The value text travels with the end
of its own bar, so a long top bar pushes it off the right edge. The same data
took 0.90 at 1920 and 0.60 at 1080. Scale the whole set by one factor and the
proportions between rows — the only thing the beat claims — stay exact.

### Narration craft — read the long skill's section, it applies here

**`longform.md` carries the full rules** (pauses as punctuation,
chapter titles written as openers, hinge sentences into a beat, saying whole
product names, drawing a figure that is spoken). All of it applies to a short,
and two of them apply *harder* because forty seconds has no room to recover:

- **A beat's items must be written as one spoken sentence, not as a list read
  aloud.** The AirPods short's checklist chunks were "Not the earbuds." / "Not
  the noise cancelling." / "The volume." and the note back was that it does not
  flow. Written as speech it is *"It is not the earbuds. It is not the noise
  cancellation."* then, after a real pause, *"It is the volume."* Same three
  chunks, same three reveals, same sync - the difference is entirely in whether
  a person would say it that way.
- **The last two sentences of a short are the ones that get rushed.** The
  AirPods ending was called "totally messy": four short sentences with 0.4-0.55
  gaps stacked into eight seconds, so the instruction, the reassurance and the
  call to action all arrived on top of each other. Give a short **one** closing
  instruction, say it once, and put 0.70-0.90 in front of it.

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
- **No ear close-ups.** Rejected on sight in the AirPods pair — "a nasty close
  up of ear". `human-ear-close-up-dark` and `audiologist-hearing-test-ear` are
  in the cache and neither belongs in a cut. Show a person listening instead.
- **A folder name is the search query, not the contents.** Two clips filed
  under `hand-adjusting-phone-volume-dark` are a photo editor and a messaging
  keyboard, and either one under a line about a volume ceiling has the viewer
  reading the wrong screen. Look at the frame before trusting the path.
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

## Voice

**Two roles.** Article explainers (long + Short pairs) use one roster;
sound-therapy sessions use another — they are different products with
different delivery needs, see *Two formats, and they are not the same job*.

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices show luna
```

**Explainer default: `mia`.** Female, `af_heart` 1.10. Every shipped tinnitus
long+short pair uses it except `airpods-and-tinnitus` and `tinnitus-and-sleep`,
which were rendered on now-retired profiles and were repointed at `mia` on
2026-08-28 so they stay re-runnable — a re-cut of either would no longer
reproduce the exact original audio.

**Explainer male reader: `otis`.** Bare `am_puck` (C+ on hours of data, the
steadiest American male) on the same `ENERGETIC` chain `mia` uses, at speed
1.00. The counterpart to `mia` when a pair wants a male voice — first used on
`pulsatile-tinnitus` (2026-09-02). `arlo` (bare `am_liam`, same chain) is the
alternate, held for the planned quiz format so the two formats do not sound
identical. Both chosen by the user by ear from a thirteen-voice demo.

**`max` is not an article voice.** It was briefly listed as the male
alternate here and that was wrong: it is a 60/40 `am_michael`/`af_nicole`
blend on the drone `SOFT` chain, and the breathy-female component makes it
read androgynous on a real explainer script. It stays a drone runner-up only.

**Sound-therapy primary: `luna`.** Female, `af_nicole` 0.90, soft chain — the
bare voice off the punchy `ENERGETIC` chain and onto `SOFT`, which exists for
exactly this: no pitch shift, presence pulled down, air added, -16 LUFS.
Renamed from `luna-calm` on 2026-08-28, once an earlier profile of the same
name (the bare voice unprocessed at 1.10) had been retired and the name was
free. `elias` is the alternate — the bare voice pitched 12% down toward a
male register, real time restored.

**Kokoro has no male breathy voice** — measured, not assumed. All twelve male
voices ran 11.7–16.2s where the bare `af_nicole` voice ran 23.3s on the same
script. Cross-gender style blends were tried and lose the character: they came
in *shorter* at a slower speed setting. Pitching the bare voice down keeps
100% of the breath by construction, which is why `elias` exists and why it is
a pitched female voice rather than a true male one. Kokoro has released no
fine-tuning code, so blending and DSP are the whole ceiling.

**Open risk:** a pitch-shifted female voice can read as "a processed woman"
rather than "a man". No measurement settles that; only the user's ear does.

**None of the four is approved.** All are `candidate` until the user says
otherwise.

**Check phonemes before rendering, not after** — same espeak traps as the drone
skill. `tinnitus` is fine (`tˈɪnɪɾəs`). Abbreviations are not.

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

## The stock shelf for anything medical is lit bright, and the dark ones are worse

Screened for the myths cut: every `doctor-consultation`, `hearing-clinic`,
`therapy-session` and `stethoscope` result came back **L82 to L195** against
a ceiling of 48. Medical stock is shot on white. There is no grading fix —
`VideoShot`'s dim only reaches so far, and a dimmed white clinic is a grey
clinic.

**The one dark result was worse than the bright ones.**
`doctor-night-shift-dark-hospital-corridor` screened at L36-40, comfortably
inside the box, and is **a bald child in a hospital gown being pushed in a
wheelchair** — it reads as a children's cancer ward, under a script about
ringing ears. `man-talking-to-camera-dark-room-interview/7230790` screened at
L27-30 and has a handgun on the table. Both would have shipped on the
numbers.

So for the "see a professional" beat, stop looking for a clinic. What works
is **the act rather than the place**: a hand on a phone, somebody at a window,
a person sitting with it — with the red flags carried as a `payload`
statement card over the shot, which is also how the medical rule's "put the
red flags on screen" gets satisfied without spending a sixth beat shape.

## No ear close-ups, in either format

**Two were shipped in the AirPods cut and both were rejected on sight**, in the
user's words as "a nasty close up of ear which dont look good". A macro of an
ear canal at full frame is unpleasant to look at, and it is not even
informative — the viewer knows what an ear is. `human-ear-close-up-dark` and
`audiologist-hearing-test-ear` are both in the stock cache and neither should
go in a cut; the clinic one is a backlit red ear against grass at L140-156, so
it fails the brightness box as well.

**A video about hearing does not have to show an ear.** The subject is a person
listening — a commuter with headphones, someone putting an earbud in, a hand on
a volume control. Those read faster and are pleasant to watch, which is the
whole job of a shot nobody is reading.

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
                        intro=INTRO)          # spoken by luna
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

Thirty seconds of `luna` at the front, then nothing. A forty-minute noise
file with no voice is indistinguishable from every other one on the platform;
the intro is where the video says what the sound is, who it is from, and **how
to set the level**. The bed sidechains under it and returns to full afterwards.

`luna` and not `mia`: SOFT chain, unhurried, no pitch shift. An explainer
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

## Audio strategy

Unlike the drone shorts, **do not export silent for a trending sound.** The bed
and the voice are the content; a trending sound would replace the thing the
viewer came for.

## The brand mark, and what its height costs the picture

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

**That hairline is this brand's peach now, not thecrypto.wiki's gold.**
`PhotoShot` took its colour from a module constant, so every photograph in every
tinnitus video — long and short — carried a gold edge, and nothing raised. It
takes the `Brand` now, like the drawn beats always did. Anything rendered before
this is off-brand at the photo edges.

The same height difference drives the **photo-border dodge** described in
`longform.md`: a picture that fits the frame is pushed down (or slightly
scaled) so its hairline never crosses the mark, while a full-frame picture
is left alone. It reads the mark's real box rather than a constant, so this
159px lockup pushes a photograph roughly four times as far as the wordmark
does — which is exactly why it could not be a number in the source.

## Do not

**Either format:**

- **Make medical claims.** The one rule above all others - describe partial
  masking and paced breathing as things people do, never as treatment, and never
  imply a cure.
- Write copy that oversells what a bed masks without running `band_energy`.
- Promote a candidate voice to approved. `mia` and `luna` are both
  candidates.
- Mass-produce. Same cap as crypto: see `docs/long-form-strategy.md`.

**Long form only:**

- Present the app's zen albums as available - the audio files are not on disk.

**The Short only:**

- Add stock footage, a roaming watermark or any other cutting element to an
  **ASMR** short's picture. `roam` is available there and is the one exception
  worth considering, because it is a crop-resistance measure rather than a
  visual one - but the picture is deliberately calm and every extra moving
  thing fights the audio, which is the product.
- Default to driving traffic to the blog. **App install is the far better
  conversion from short-form**, and the only path here with a plausible route to
  revenue.
