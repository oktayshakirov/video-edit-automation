# Project: drone, long form

A folder of graded selects cut to a music track and written out as an **FCPXML
timeline** - it never renders a video. You finish it in Final Cut, which is the
point rather than a cost: here the footage *is* the product.

Nothing in `beats.md`, `footage.md` or `shorts.md` applies. The vertical cut is
a different engine - see `drone-short.md`.

## Scope

Long-form YouTube only — a Final Cut timeline, cut to music, finished by hand.
**This pipeline never renders video.**

Vertical short-form (TikTok, Shorts, Reels) is a different product with its own
pacing model, its own crop problem and its own numbers. That is the vertical half of this doc.
The clip index is shared, so a folder indexed here is ready for both.

## New footage folder

```bash
cd ~/Coding/video-edit-automation
.venv/bin/python -m video_automation drone index /path/to/footage      # slow once, then cached
```

Create `projects/drone-long/<name>.toml` (copy `projects/drone-long/plovdiv.toml`, repoint `footage` and
`music`). Then the loop:

```bash
.venv/bin/python -m video_automation drone build --project <name> --dry-run   # seconds
.venv/bin/python -m video_automation drone build --project <name>             # writes FCPXML
```

**Always `--dry-run` while tuning.** It reruns the whole engine off cached
proxies and prints the full edit list — clip, timecode, length, section, source
in-point, speed, effects — plus coverage and per-clip usage.

`--click` writes the track with clicks on every bar line. Worth doing once per
track: downbeat phase is the weakest inference in the pipeline, and if it is off
by two beats every cut lands on the backbeat.

## Tuning

Every knob is in `video_automation/drone/config.py`, grouped by phase, `GUESS`-marked
where unvalidated. **Per-video changes go in `projects/drone-long/<name>.toml` under
`[overrides]`**, never in `config.py` — that is the shared baseline.

| Symptom | Look at |
|---|---|
| too many / too few cuts | `SLOT_BARS_BY_ENERGY`, `PHRASE_ACCENT_MULTIPLIER` |
| one clip dominates | `MAX_USES_BY_MOVE`, `PENALTY_OVERUSE` |
| feels repetitive though frames differ | `REUSE_RECENCY_WINDOW`, `MIN_SLOT_BARS_BY_MOVE` |
| wrong footage on the drop | `W_ENERGY_MATCH`, Phase 1 `motion_energy` weights |
| shots too long | `MAX_SHOT_SECONDS`, `LEGAL_SLOT_BARS` |
| speed effects overused | `SPEEDUP_MIN_REMAINING`, `PENALTY_SPEEDUP_WHEN_CALM` |
| not enough footage used | `W_COVERAGE`, `W_BITE` |
| two clips move alike | `AUTO_REVERSE`, `REVERSIBLE_MOVES` |
| want a speed launch into a cut | `ESCALATE_AT_BARS` |
| cuts feel a beat late | `SNAP_SECTIONS_TO_PHRASE` — read the warning below |
| the head of a clip is weak | `CLIP_HEAD_SKIP` |
| a specific clip must sit in a specific slot | `PIN_CLIPS`, `PIN_SLOT_BARS` |
| a clip must never appear | `CLIP_EXCLUDE` |
| a clip must run at a speed you chose | `CLIP_SPEED` |
| each location needs its own stretch | `CLIP_BAR_WINDOWS` |
| one clip is graded differently to the rest | `CLIP_LUT` |
| more than one song | `music = [...]`, `MUSIC_MEDLEY_*` |

**Two traps around pins and windows**, both found the hard way on Bulgaria:

- **A slot may not cross a section boundary.** `PIN_SLOT_BARS = 3` at a bar
  with one bar left in its section is not shortened — the pin simply cannot be
  placed. Lay pin lengths out *backwards* from the next boundary.
- **A window that runs out of footage ends the timeline**, it does not move on
  to the next window. Size each location's window to what that folder can
  actually fund at the speeds set — which is `sum(clip_seconds / rate)`, so
  speed-ups *reduce* how much timeline a location can fill. Asking Akra for
  166s when it could fund 158s emptied it and stopped the build 5 minutes
  short.

A pin that cannot be funded is no longer fatal — the slot falls back to normal
scoring and says so. It used to fall through to "out of unused footage" and
truncate the video with the library barely touched.

## Locking — the most important rule here

The scorer is **greedy**: any change to weights, section boundaries or slot
lengths re-lays the grid downstream and reshuffles every clip after the change
point. Tuning cannot preserve an approved order. This was attempted three times
on Plovdiv and reshuffled it every time, once silently changing the opening shot.

**As soon as the user approves an edit, lock it:**

```bash
.venv/bin/python -m video_automation drone build --project <name> \
    --lock-out projects/drone-long/<name>.lock.toml
```

Add `lock = "<name>.lock.toml"` to the project file. `build` then replays the
slot grid and assignment verbatim, scorer bypassed.

**With a lock in place, a request to swap or resize one shot is a direct edit to
the lock file** — change `clip`, `bars` or `rate`. Never reach for scoring
weights; they no longer apply to that project.

Effects that eat extra source (escalates, 2x) can still be limited by what a
clip owes its other locked slots. When that happens, fit the effect down to what
is available (`fit_escalate`) and report the achieved numbers — do not quietly
take footage from a later slot and move the timeline.

For an unlocked project, dry-run any structural change and diff the clip order
against the last approved tag before presenting it. If positions moved, say so.
Never present a reshuffled edit as though only the requested thing changed.

**Change one thing per round.** A batch containing one bad change takes the good
ones down with it.

## Hard constraints

- **Never slower than 1.0x.** Slow motion reads as a mistake on this footage; the
  validator fails the build if any timeMap segment drops below real time. Long
  clips get sped up, short clips lose the slot — a clip is never stretched.
- **Analysis only touches proxies** in `<footage>/.analysis_cache/`.
- **Cuts land on bar lines only.** A mid-bar accent cannot be hit; the nearest
  legal point is up to half a bar away. Fixing it needs slot lengths in beats.

## Saving an approved stage

```bash
git add -A
git commit -m "<project>: <what changed>"
git tag <project>-vN -m "<cuts>, <coverage>, <what was approved>"
git push origin main && git push origin --tags
```

Add a row to `CHANGELOG.md` with the metrics from the build output, and prune
open items the change actually resolved.

## Overlays

`assets/` holds the reusable location pin and, critically,
`assets/fcpxml/location-pin-overlay.xml` — the Green Screen Keyer captured
verbatim from a real Final Cut export. Its UID plus two base64 payloads encode
FCP-internal state that **cannot be authored from a specification**. Reuse the
fragment as-is. The red pin is source **9.833–14.867s** of the pack (not
guessable — by hue it measures ~345° and classifies as pink). Placement: lane 1,
`scale 0.06`, `position -81.524 42.1759`, `conform-rate srcFrameRate="24"`.

### More than one place, and the text that collides with the pin

`LOCATION_PINS` takes a list of `{start, text}` — a video cut from two locations
names each on its first appearance. The singular `LOCATION_PIN_START` /
`LOCATION_TITLE_TEXT` remain the one-location shorthand.

Two things bite once there is a second pin:

- **The captured title defines its text style as `ts1`.** Emitted twice that id
  repeats and Final Cut rejects **the whole document** — "ID ts1 already
  defined" — not just the second title. Each title now gets `ts2`, `ts3`…
- **The title's `Position` is centre-anchored** (`Alignment` is `1 (Center)`),
  so the words grow outward from one fixed point in both directions. A long
  place name reaches further left and lands on top of the pin; a short one sits
  with a gap. **The overlap is a function of how many characters the name has**,
  which is why it shows up on one video and not the next, and why it cannot be
  fixed once inside the fragment.

  Each entry takes `dx` (and `dy`) in Motion points, shifting the anchor right
  and up. Only a captured param's *value* changes — the key path is untouched —
  so this is ordinary authoring, not a guessed UID. Measured on the Bulgaria
  cut: **`dx = 110` for a ~23-character name, `dx = 65` for ~21.** Set it per
  pin and check it on screen; there is no way to compute the rendered width of
  the string from here.

### Colour is not something this pipeline can write

**There is no colour element in FCPXML** — see the import section below. A LUT
needs `<filter-video>` plus an `<effect uid>` that is FCP-internal, and the uid
must be **captured from a real export**, never guessed. Until that capture
exists, grading requests are answered either by reordering shots so mismatches
sit apart, or by baking the LUT into new media with ffmpeg's `lut3d` — which
re-encodes the selects and is the worse answer on a project where the footage
is the product.

The user's LUT library lives in
`~/Library/Application Support/ProApps/Custom LUTs/LUTs Library/`.

## When Final Cut rejects the import

`build` validates against Final Cut's own DTD plus semantic checks. If FCP still
complains, reproduce it locally instead of guessing:

```bash
.venv/bin/python -c "
from pathlib import Path; from video_automation.drone.validate import check
print(check(Path('<file>.fcpxml')) or 'clean')"
```

Two failure classes, different tools:

- **DTD / element order** — caught by `xmllint` against the bundled FCP DTD. The
  DTD lives inside `Final Cut Pro.app`, whose path contains spaces, so it is
  staged to a space-free temp path first; pointing xmllint at the bundle directly
  fails with a misleading "Could not parse DTD".
- **Semantic** — attribute values a DTD cannot reason about. The known trap: a
  clip with a `<timeMap>` must have `start="0s"`, its in-point living in the
  first `timept value`. Setting both makes FCP report *"Invalid edit with no
  respective media"* and silently drop the clip.

**FCPXML has no colour or keying element.** The entire `adjust-*` set is crop,
transform, blend, stabilisation and volume. Anything else needs `<filter-video>`
plus an `<effect uid>` that is an FCP-internal identifier. **Never guess a UID** —
that caused two failed imports. Capture it instead: have the user apply the
effect to one clip, `File ▸ Export XML`, and read the exact structure out.

## Do not - long form

- Add dependencies without saying what they buy.
- Let CV touch source files.
- Present a guessed parameter as validated — say when something is a guess.
- Change `config.py` for one video's taste; that is what project overrides are for.
- Produce a 16:9 cut when the user asked for vertical — hand that to the vertical half of this doc.
