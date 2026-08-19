# Handoff — state as of 2026-08-19 (corrected)

Written immediately after the previous entry in this file turned out to
describe a mistake as if it were a decision.

**Repo:** `~/Coding/video-edit-automation` → https://github.com/oktayshakirov/video-edit-automation

## Two mistakes in the post-upload pipeline, both fixed the same day

**The short got a site entry and a social share it should never have had.**
The previous handoff entry claimed this was deliberate - "unlike tinnitus...
crypto shorts go through the full pipeline" - and that was an unwarranted
inference from an ambiguous instruction, not something the user actually
asked for. Corrected: **only the long form gets a `videos.json` entry and a
Share Video run. A Short is YouTube-only**, exactly matching
`video-tinnitus-long`'s already-settled rule. There was never a real
per-site difference here.

What that cost: `crypto-exchanges-short`'s registry entry and poster are
reverted out of `crypto-wiki`. The Facebook and Telegram posts **cannot be
unsent** - the ids are recorded (Telegram message 141 in chat
-1003019225999, Facebook post `140513256083904_122249053136045514`) in case
the user wants them taken down, but nothing was deleted without asking.

**`render_video_poster` was solving a problem YouTube already solves.** It
rendered a blurred-letterbox composite locally for a Short's 1080x1920
thumbnail, reasoning that the registry's fixed 1280x720 slot needed it built
by hand. It did not: YouTube composites *any* uploaded thumbnail into
1280x720 itself and serves it from `i.ytimg.com/vi/<id>/maxresdefault.jpg` -
measured against the pre-existing `saylor-treasury-short.webp`, that CDN
image is pixel-identical to 1.1 mean difference (re-encoding noise only).
Replaced with `fetch_video_poster(out, video_id)`, which downloads that URL
and converts it to WebP. No image processing, no blur, no letterbox logic -
and it only ever runs on the long now regardless.

**Read both corrections in the skill files, not just here.**
`video-crypto-long/SKILL.md`'s "The order of the whole job" and "The
video-registry poster" sections are rewritten; `video-crypto-short/SKILL.md`
now says plainly that a short gets metadata and nothing past it.

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
