# Handoff — state as of 2026-08-19 (later)

Written after the crypto-exchanges pair went through the full post-upload
pipeline for the first time: metadata, site registry, social share.

**Repo:** `~/Coding/video-edit-automation` → https://github.com/oktayshakirov/video-edit-automation

## The post-upload pipeline is now a documented, standing workflow

Recorded in `video-crypto-long/SKILL.md` ("The order of the whole job, after
the build") and cross-referenced from `video-crypto-short/SKILL.md`. On the
user's instruction: once they say a video is uploaded, the whole sequence runs
without being asked again per step - `youtube-audit set` (dry run, then
apply), `render_video_poster` + a `videos.json` commit, the deploy-gate poll,
then the Share Video n8n workflow for both long and short.

**Two things do not become automatic, on every future upload, regardless of
that instruction:** posting to social media and pushing to the live site are
each confirmed in the chat they happen in. This is a standing operating rule,
not a project decision, and it does not relax because the user asked for less
friction - it was said plainly back to them rather than silently skipped or
silently kept.

**Crypto shorts now go through the full pipeline, unlike tinnitus shorts.**
`video-tinnitus-long`'s "Shorts do not get a site entry or a social share" is
untouched - that is a settled, site-specific decision. Crypto's short got a
`videos.json` entry (`target: null, placement: "none"`, same as
`satoshi-proof-short`) and its own Share Video run, because the user asked for
both videos to go through everything this time.

**`render_video_poster` is new**, in `longform/thumb.py`. It is the function
version of a treatment that existed only as two hand-made files
(`saylor-treasury-short.webp`, `satoshi-proof-short.webp`): a long's landscape
thumbnail passes through as a format change, a short's 1080x1920 one gets
letterboxed into 1280x720 with a blurred-cover-crop backdrop rather than
stretched.

**Nothing in this pipeline can publish a video.** `youtube-audit`'s scopes stay
capped at `list` + `update` on snippet fields; flipping privacy from unlisted
to public is a `status` write that was deliberately never added, per that
skill's "What is still off-limits". Both crypto-exchanges videos are live on
the site and shared to socials while still **unlisted** on YouTube itself -
say this plainly rather than letting the user assume the pipeline made them
public.

## PancakeSwap gained a page mid-session

`crypto-wiki/content/exchanges/pancakeswap.mdx` appeared on disk (not
committed by this session) between the short's first draft, which hard-coded
its custody verdict as a literal, and its rebuild. The literal's own comment
said "if the site ever gains the page, delete the literal and let `F.compare`
cover all four" - done, in `projects/crypto-short/crypto-exchanges.py`. The
page itself and its logo (`public/images/exchanges/pancakeswap.webp`) are
**still uncommitted** in `crypto-wiki` as of this writing; that repo's
`publish-content` pipeline, not this one, is what would ship them.

---

## What was built

A long-form 16:9 format shared by both sites, in `video_automation/longform/`.
The strategy — why it exists, what the SEO claim is actually worth, and which
post to do next — is `docs/long-form-strategy.md`. Read that before picking a
topic; it caps the whole programme at 15–20 videos and says why.

The engine became frame- and brand-agnostic to get here:

- `core/frame.py` — `VERTICAL` / `LANDSCAPE`. Geometry, safe box, upscale
  ceiling. **The shipped vertical shorts render byte-identical through all of
  it**, verified against a pre-refactor baseline.
- `core/brand.py` — palette and watermark per site.
- `core/draw.py` — drawing primitives, lifted out of `crypto/shots.py`.
- `core/music.py` — synthesized music beds. `pulse` is the crypto default.
- `core/soundbed.py` — synthesized therapy noise, with notching.
- `core/stock.py` — Pexels photos and video, on the `publish-content` key.
- `longform/` — `plan`, `beats`, `clip`, `overlay`, `audio`, `meta`, `thumb`,
  `build`, `asmr`.

Six drawn beats (`chapter`, `checklist`, `stat`, `compare`, `quote`, `bars`),
video clips, an end-screen sting, a generated bed, SRT, chapters, a description
sidecar and a thumbnail. Everything is generated or screened; nothing needs a
licence chased.

---

## The two videos, and what is left to do on them

Both are **uploaded, unlisted, with title/description/tags applied** via
`/youtube-audit`. Neither is public. The Saylor long form (below) is the third.

| | crypto | tinnitus |
|---|---|---|
| id | `Sbxrw7ZFI9o` | `RR_qU3FA0OY` |
| title | The One Test That Settles Every Satoshi Nakamoto Claim | Does Tinnitus Go Away? Temporary vs Chronic Explained |
| runtime | 2:47 | 2:40 |
| tag | `satoshi-long-v1` | — |

**Three things must be done by hand in Studio**, because the audit tool's scopes
are deliberately limited to title/description/tags and must not be widened:

1. **Visibility → Public.**
2. **Upload the thumbnail** — `~/Desktop/*-thumb.jpg` for each.
3. **Upload the SRT** (Subtitles → Add → With timing). The user has already done
   this for the tinnitus one.

Note the CLI flags both as `short-length` — under three minutes. They are not
Shorts (16:9 landscape), but it is a real variable and the strategy doc targets
2:30–4:00 partly on that basis.

---

## The Saylor long form — built, approved, uploaded

`crypto-saylor-treasury-long`, 3:51, from `crypto-ogs/michael-saylor`. Script is
`projects/crypto-long/saylor-treasury.py`; metrics are in `CHANGELOG.md`. The
user approved it and uploaded it; title and description were applied with
`/youtube-audit`. **The thumbnail and the SRT still have to go in by hand in
Studio**, as with the other two.

It kept the short's angle deliberately and spent the extra three minutes on the
financing mechanics, the rename, and the bear case. The Commons attribution
block is in the description and there is an explicit no-advice line.

**Three of the faults in it were bad pictures, and all three were invisible in
the logs.** Six site images were far brighter than the palette takes,
`ftx-collapse.jpg` under a line about leverage read as exchange fraud, and
`one-coin.jpg` is OneCoin — Ruja Ignatova's fraud — which beside Saylor is an
accusation the script never makes. **Screen the site's own images too**, not
just stock: `stock.screen` works on any file, the pilot's brightest photograph
measured L82, and anything much above that fights the gold-on-near-black frame.

## Two engine fixes came out of that cut

Both are in `crypto/shots.py`, both affect every video the repo makes, and both
are documented in `/video-crypto-long`.

**A fitted photograph's gold hairline no longer crosses the watermark.**
`PhotoShot` pushes the shot down — or scales it into the available band when it
is too tall — by a constant offset computed from the extreme of the Ken Burns
travel, so the motion is unchanged. A full-frame photograph draws no top
hairline and is left alone. It reads the mark's real box, so the tinnitus
lockup pushes roughly four times as far as the crypto wordmark.

**The Ken Burns on a still is one float affine.** It was three integer steps —
`int()` on the width, `int()` on the height, `round()` on the paste — so the two
axes crossed their rounding boundaries on different frames and the picture grew
taller and wider a few frames apart. Measured, the frame-to-frame delta swung
3.4–4.5x between consecutive frames; it is now within 1.15x with no frozen
frames. The user saw it as flickering and lagging before any measurement did.

**This retires an invariant.** The vertical shorts are **no longer
byte-identical** to their shipped renders — the old bytes contained the judder,
and `crypto/shots.py` had claimed subpixel motion in its own docstring since it
was written. Re-rendering a short now gives a slightly smoother, different file.
That was a deliberate call and it is the one thing in this session worth
revisiting if it turns out to matter.

## Next

Nothing is agreed. The demand ranking in the strategy doc still points at
`how-to-build-a-mining-rig` (1510 views) and `understanding-crypto-exchanges`
(1038), and the programme is capped at 15–20 videos. Phase 4 — the site embeds —
is still parked until there are ~30 days of data.

## What is unverified, and should be said rather than assumed

- **Nobody has heard the audio.** Every mix decision this session was made on
  measurements — bed at −25 dB under speech at −18, voice ~9.5 dB over the bed,
  hiss at 0.006% above 4 kHz. The numbers say the mix is right; they cannot say
  it sounds good.
- **No retention data exists for either channel.** Both are new and Shorts-only
  so far. `/youtube-audit` suppresses baselines below five videos for exactly
  this reason. Do not rank or declare winners.
- **`max_upscale=1.90` and the landscape safe box are still `GUESS`** in
  `core/frame.py`. They want checking full-screen against a real upload.
- **`mia` and `luna-calm` are candidates, not approved voices.**
- **The thumbnail scorer is overridden on all three thumbnails** (+0.91 satoshi,
  +0.01 tinnitus, +0.91 saylor). Each was a deliberate call; on Saylor the score
  is the CPAC backdrop's lettering, which the eye reads as a flat blue field,
  and the two sources that scored clean are Saylor twenty years ago. An
  override is not a pass — but three in a row is worth reading as a signal
  about the scorer, not only about the pictures.

## Still unbuilt

- **Phase 4 step A is done.** `<PostVideo />` facade plus `VideoObject` shipped
  on both site repos, driven by a `videos.json` registry rather than MDX
  frontmatter. Details and the rest of the plan: `docs/site-video-integration.md`.
- **Sound-therapy sessions are live on tinnitus.** `ZenSessions` on every /zen
  album page plus a `/zen/videos` tab listing them all. Sessions are
  many-to-one with an album - the registry expects several entries sharing one
  `target`, each with a short `label`.
- **The registry sync is deliberately not built.** At the current cadence,
  hand-editing `videos.json` on upload beats maintaining a script; the design is
  recorded in `docs/site-video-integration.md` if the cadence ever changes.
- **Keep the SRT and the sidecar.** Both were cleaned off the Desktop before the
  site pages needed them, and the transcripts had to be rebuilt from
  `SECTIONS[].sentences` plus the chapter times in the YouTube description. That
  worked, but only because the script is in the repo. Copy the `.srt` somewhere
  durable on the next render.
- **Upload.** `/youtube-audit` can edit metadata but must never gain upload or
  delete scopes.
- **Vertical layouts for the drawn beats.** Only `checklist` has one, so
  long-form cannot yet spawn vertical extracts for TikTok and Reels. Sized as
  comparable to Phase 2 if it is ever wanted; the reasoning is in the answer to
  "should I cross-post this".

## Working agreements

- **Change one thing per round.** A batch containing one bad change takes the
  good ones down with it.
- **Look at the frames.** Every real fault this session — the ghosted
  transitions, the graph-paper grid, the counting year, the video judder, the
  thumbnail overlap — was invisible in the logs and obvious in a frame.
- **Measure before writing copy about it.** `soundbed.band_energy`,
  `stock.screen`, `thumb._layout` all exist because an eyeball got it wrong once.
- **Say when something is a guess.** `GUESS` in `core/frame.py`, and this file.
- Commit and tag when the user says a cut is good; add a `CHANGELOG.md` row with
  the metrics from the build output.
