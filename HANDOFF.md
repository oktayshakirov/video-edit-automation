# Handoff — state as of 2026-08-13

Written to close out the session that built long form. Everything below is
committed and pushed; nothing is in flight.

**Repo:** `~/Coding/video-edit-automation` → https://github.com/oktayshakirov/video-edit-automation

Five skills, symlinked into `~/.claude/skills/` so they work from any folder.
**Read the relevant SKILL.md first** — it carries the rules that were paid for,
and this file deliberately does not repeat them.

| skill | what it makes |
|---|---|
| `/video-drone-long` | 4K YouTube films. Writes an FCPXML timeline. Never renders. |
| `/video-drone-short` | TikTok / Shorts from drone footage. |
| `/video-crypto-short` | 9:16 shorts from thecrypto.wiki. |
| `/video-tinnitus-short` | 9:16 shorts and ASMR for tinnitushelp.me. |
| **`/video-crypto-long`** | **16:9 YouTube explainers from thecrypto.wiki.** |
| **`/video-tinnitus-long`** | **16:9 explainers *and* sound-therapy sessions.** |

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
`/youtube-audit`. Neither is public.

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

## Next: the Michael Saylor long form

**This is the agreed next task.** `/video-crypto-long`, from
`crypto-wiki/content/crypto-ogs/michael-saylor.mdx` (1,379 words).

Everything needed is already on disk:

- **The short exists and is public** — `fvqxbVLa6Mg`, "The Man Who Owns 4% of
  All Bitcoin | Michael Saylor", 1:02, 31 views. Its script is
  `projects/crypto/michael-saylor.py`.
- **The portraits exist** — `assets/crypto/michael-saylor/`, four Wikimedia
  Commons photographs at 2000–8000px, the only images in the format that never
  upscale.

Three things to get right, in order of how badly they bite:

**Reuse the short's material freely.** Its angle is the strongest one the
article has and there is no reason to invent a weaker one to be different — the
treasury bet and what the company became belong in the long version too. What
three minutes buys is *depth on the same story*: the financing mechanics (debt
offerings and share sales funding coin purchases), the rename to Strategy, and
the honest bear case, none of which fit in sixty seconds.

**Attribution is mandatory and it is in `assets/crypto/michael-saylor/CREDITS.md`.**
Two of the four photographs are CC BY-SA, which makes the video a derivative
work. The block goes in the description of anything published. `Meta.credits`
exists for exactly this.

**No financial advice, and this topic invites it.** A piece about a man who bet
a company on one asset is one sentence away from sounding like a recommendation.
Report what the company did and what it cost; route to the article. The Satoshi
script's closing pattern — a question, not a verdict — is the safe shape.

The demand ranking in the strategy doc has better-trafficked candidates
(`how-to-build-a-mining-rig` at 1510 views, `understanding-crypto-exchanges` at
1038). Saylor is the user's pick, not the data's; worth saying once and then
building it.

---

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
- **The thumbnail scorer prints a warning on both current thumbnails** (+0.91
  crypto, +0.01 tinnitus). Both were overridden deliberately — the crypto type
  sits on soft dark foliage — but it is an override, not a pass.

## Still unbuilt

- **Phase 4: the site embeds.** MDX component plus `VideoObject` schema on both
  repos, with a facade embed and a locally served WebP poster. Deliberately
  parked until the videos have ~30 days of data — the embed is easier to justify
  once you know whether anyone watches past 30 seconds.
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
