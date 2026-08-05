# Handoff — state as of 2026-08-06

Written to close out a long session. Everything below is committed and pushed;
nothing is in-flight.

**Repo:** `~/coding/drone-edit-automation` → https://github.com/oktayshakirov/drone-edit-automation
**Footage:** `~/Desktop/Plovdiv` (15 graded selects, 3840×2160p30, ~6.3 min)

Two skills, symlinked into `~/.claude/skills/`, so they work from any folder:

- **`/video-drone-long`** — long-form YouTube. Writes an FCPXML timeline. Never renders.
- **`/video-drone-short`** — TikTok / Shorts. Renders finished vertical MP4s.

Read the relevant SKILL.md first; it carries the rules that were paid for.

---

## Where the long-form pipeline stands

**Done and approved.** Plovdiv is finished and published:
*Europe's Oldest City From Above — Plovdiv, Bulgaria in 4K*.

Seven tagged stages, `plovdiv-v3` through `plovdiv-v7`. `git checkout <tag>`
returns to any of them exactly.

Current state: 47 cuts, 4.81 s mean shot, 81% footage used, 2 escalates,
4 reversed clips, DTD-valid.

### The one rule that matters most

**The timeline is locked** (`projects/plovdiv.lock.toml`). The scorer is greedy —
any change to weights or section boundaries re-lays the grid and reshuffles every
clip after it. This was learned the hard way: three separate attempts to "swap
one clip" reshuffled the whole running order, one of them silently changing the
opening shot.

With a lock present, **a request to swap or resize a shot is a direct edit to the
lock file**, not a scoring change. Do not reach for `config.py` weights on a
locked project.

### Open items

- **3:22 cut lands 1.07 s early.** The accent sits mid-bar (bar 80.42) and the
  engine only cuts on bar lines. Needs slot lengths expressed in beats. This is
  the single most valuable remaining long-form change — it would also make
  off-phrase section boundaries far less destructive.
- **The 1:00 escalate is capped at 160%→403%** rather than the intended
  200%→2000%, because City 11 owes 22.5 s to its later locked slots. Freeing it
  means dropping one of those slots, which moves the timeline.
- **Colour pass unapplied.** Measured values are in `projects/plovdiv-colour.md`
  — City Above +0.61 stops, Hill Tower +0.56 stops and saturation ×0.52, plus
  small warm nudges on the four cool clips. Must be done by hand: FCPXML 1.10 has
  no colour element.
- **Slice selection is sequential**, so the back half of long takes is only
  reached through reuse. Spreading slices across each clip's full length is the
  obvious next improvement.

---

## Where the short-form work stands

**Working, untested on the platform.** Nothing has been posted yet, so no
performance data exists for the new formats.

Built and committed:

- `vertical.py` — 9:16 crop placement (2D interest search plus per-clip zoom),
  quote-card renderer
- `voiceover.py` — Kokoro / edge-tts / say backends, captions synced to measured
  audio duration

### Settled by testing

- **Text template** — SF Rounded Semibold 46px, centred at 40% height, no scrim,
  soft glyph halo, ink auto-picked from background luminance, no widows. A
  lower-third with a gradient scrim was tried first and rejected against real
  reference videos.
- **Crop needs a 2D search.** Scoring columns alone put ~60% of the frame on
  empty sky for wide landscapes. Zoom ≈1.45 for landscapes, 1.0 for clips with a
  strong vertical subject.
- **Voice: `am_onyx`** via Kokoro (local, unlimited, Apache 2.0).
- **The melancholic treatment is approved** and the exact filter chain is in the
  skill. The pitch-down and echo tail are what sell it.

### Explicitly not settled

- **The motivational treatment was rejected** — sample 1 was not what was wanted.
  Needs another pass.
- **Kokoro has no emotion parameter.** Mood is script construction plus pace plus
  post-processing. Do not describe it as the model performing an emotion.
- **Length.** The old 10–19 s retention curve is real but drawn from silent
  scenery clips predating this format. Working rule is **under 30 seconds**,
  report the runtime, and revisit once the new format has its own numbers.

### Next step agreed

Plan the short-form videos properly. The strategy document is
`docs/short-form-strategy.md` — nine concepts mapped to specific clips, plus the
channel analysis behind them. The headline finding: **angle beats scenery by
24×** on this channel (a joke about German train delays did 2,075 views; "Golden
Hour Drone Footage" did 85).

---

## Hard-won FCPXML knowledge — do not rediscover

- **A clip with a `<timeMap>` must have `start="0s"`.** Its in-point lives in the
  first `timept value`. Setting both makes Final Cut report *"Invalid edit with
  no respective media"* and silently drop the clip. Cost two failed imports.
- **`xmllint` against the bundled FCP DTD** catches element-order errors before
  import. The DTD lives inside `Final Cut Pro.app`, whose path contains spaces,
  so it is staged to a space-free temp path first — pointing xmllint at the
  bundle directly fails with a misleading "Could not parse DTD".
- **FCPXML has no colour or keying element.** The whole `adjust-*` set is crop,
  transform, blend, stabilisation, volume. Anything else needs `<filter-video>`
  plus an `<effect uid>` that is an FCP-internal identifier. **Never guess a
  UID.** Capture it: have the user apply the effect to one clip, `File ▸ Export
  XML`, and read the structure out. That is how the green-screen keyer in
  `assets/fcpxml/location-pin-overlay.xml` was obtained.
- **Never slower than 1.0×.** Slow motion reads as a mistake on this footage;
  the validator fails the build if any timeMap segment drops below real time.

## Assets

`assets/` holds the location pin used on every video, committed deliberately
despite being third-party stock (the repo is public — flagged in
`assets/README.md`). The red pin is source **9.833–14.867 s** of the pack; that
value came from a real FCPXML export and is **not** guessable, since by hue the
red pin measures ~345° and classifies as pink.

## Working agreements

- **Change one thing per round.** A batch containing one bad change takes the
  good ones down with it — this happened repeatedly.
- **Diff before presenting.** If a change moved clip positions, say so. Never
  present a reshuffled edit as though only the requested thing changed.
- **Say when something is a guess.** `config.py` marks unvalidated values `GUESS`.
- Commit and tag when the user says an edit is good; add a row to `CHANGELOG.md`
  with the metrics from the build output.
