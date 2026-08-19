# Handoff — state as of 2026-08-18

Written to close out the session that built the crypto-exchanges pair and the
review round that followed it.

**Repo:** `~/Coding/video-edit-automation` → https://github.com/oktayshakirov/video-edit-automation

Six skills, symlinked into `~/.claude/skills/` so they work from any folder.
**Read the relevant SKILL.md first** — it carries the rules that were paid for,
and this file deliberately does not repeat them.

| skill | what it makes |
|---|---|
| `/video-drone-long` | 4K YouTube films. Writes an FCPXML timeline. Never renders. |
| `/video-drone-short` | TikTok / Shorts from drone footage. |
| `/video-crypto-short` | 9:16 shorts from thecrypto.wiki. |
| `/video-tinnitus-short` | 9:16 shorts and ASMR for tinnitushelp.me. |
| `/video-crypto-long` | 16:9 YouTube explainers from thecrypto.wiki. |
| `/video-tinnitus-long` | 16:9 explainers *and* sound-therapy sessions. |

## `projects/` says the format now

`crypto-short/`, `crypto-long/`, `tinnitus-short/`, `tinnitus-long/`,
`drone-long/`. Renamed 2026-08-18: `projects/crypto` and `projects/crypto-long`
sat side by side and nothing said which one held the Shorts. See
`projects/README.md`.

## What the crypto-exchanges review changed in the engine

Nine notes came back on the first cut. The ones that became engine changes
rather than script changes:

- **The ping-pong background folded at frame zero.** A palindrome turns around
  at frame 0 and at its midpoint, and the naive build also repeated the frame at
  each fold — a dead frame, twice per loop, forever. Measured on the old
  `crypto-blackwater`: the two smallest steps in the whole 302-frame loop were
  0->1 and 1->2. `pingpong` drops one frame from each end of the reversed half
  and `Backdrop.at` samples from a quarter of the loop in. After: minimum step
  2.82 at an ordinary moment in the water, wrap step 4.81 against a 4.49 median.
  **`crypto-blackwater.mp4` was regenerated**; the aurora needed nothing, being
  generated on closed circular paths.
- **A new `logos` beat.** Brand tiles from the site's 27 exchange cards,
  revealed one per caption, with optional tick/cross badges so it keeps the
  checklist's two-phase payoff. Raises on a missing logo rather than drawing a
  blank tile. Portrait lays it 2x2.
- **`compare(name_columns=True)`.** Each heading becomes its own revealed item,
  so the graphic follows the voice instead of asking the viewer which column it
  is on. Opt-in, because the shipped mining-rig cut is written against the old
  reveal count.
- **`grid` puts three landscape cards in one column**, not a 2x2 with a hole.
- **`chapter` in portrait** sets at 148px and is routed by the short factory —
  a full-screen statement card for a Short's closing line.
- **The thumbnail scorer penalises a crop that cuts a face**, compared against
  the clamped box (the cascade returns boxes running off the source, and testing
  the raw one made every candidate equally clipped).
- **A shared music library.** `assets/brand/music/` serves both sites;
  `night-drift` is now on the crypto channel as well as tinnitus.

## Still unverified, and should be said rather than assumed

- **Nobody has heard the audio.** Every mix decision remains measurement-only.
- **No retention data for either channel.**
- **`max_upscale=1.90` and the landscape safe box are still `GUESS`.**
- **`mia` and `luna-calm` are candidates, not approved voices.**
- **`ChecklistShot` in `crypto/shots.py` still draws the old drifting grid** —
  `int((f * 40) % 96)` on a layer moving 40 px/s, which is the whole-pixel
  judder every other moving element in this repo was fixed for, and it is the
  last one left. The long-form beats replaced it with `core/backdrop.py` and the
  shorts never followed. Not changed here because it would alter every shipped
  short's look and neither current video uses that beat any more; it is the
  first thing to do next time a short is rebuilt.

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
