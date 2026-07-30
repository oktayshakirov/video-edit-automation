---
name: drone-edit
description: Cut a folder of graded drone selects to a music track and produce a Final Cut Pro timeline. Use when the user runs /drone-edit, points at a new footage folder, or asks to edit drone footage for YouTube or TikTok. Also use to tune an existing edit (pacing, shot choice, speed, clip swaps), save an approved stage, place the location-pin overlay, or diagnose an FCPXML that Final Cut refused to import.
---

# Drone Automation

Turns graded drone selects plus a music track into a Final Cut Pro XML timeline.
**It never renders video** — it reads, analyses and writes XML.

**Repo:** `~/coding/drone-edit-automation` — run everything from there. Footage
lives outside it.

## First question: YouTube or TikTok?

If the user did not say, ask before doing anything. The two are not the same job.

- **YouTube** — built and validated across seven approved edits. Proceed.
- **TikTok** — **not built.** `profile = "tiktok"` is accepted by the project
  loader but does nothing: no vertical reframing, no 9:16 conform, no subject
  tracking, no short-form pacing model. Say so plainly rather than producing a
  16:9 timeline and calling it a TikTok edit. What is possible today is a normal
  16:9 cut, shorter, reframed by hand afterwards. Building the real thing is
  separate work.

## New footage folder

```bash
cd ~/coding/drone-edit-automation
.venv/bin/python -m drone_automation index /path/to/footage      # slow once, then cached
```

Create `projects/<name>.toml` (copy `plovdiv.toml`, repoint `footage` and
`music`). Then the loop:

```bash
.venv/bin/python -m drone_automation build --project <name> --dry-run   # seconds
.venv/bin/python -m drone_automation build --project <name>             # writes FCPXML
```

**Always `--dry-run` while tuning.** It reruns the whole engine off cached
proxies and prints the full edit list — clip, timecode, length, section, source
in-point, speed, effects — plus coverage and per-clip usage.

`--click` writes the track with clicks on every bar line. Worth doing once per
track: downbeat phase is the weakest inference in the pipeline, and if it is off
by two beats every cut lands on the backbeat.

## Tuning

Every knob is in `drone_automation/config.py`, grouped by phase, `GUESS`-marked
where unvalidated. **Per-video changes go in `projects/<name>.toml` under
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

## Locking — the most important rule here

The scorer is **greedy**: any change to weights, section boundaries or slot
lengths re-lays the grid downstream and reshuffles every clip after the change
point. Tuning cannot preserve an approved order. This was attempted three times
on Plovdiv and reshuffled it every time, once silently changing the opening shot.

**As soon as the user approves an edit, lock it:**

```bash
.venv/bin/python -m drone_automation build --project <name> \
    --lock-out projects/<name>.lock.toml
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

## When Final Cut rejects the import

`build` validates against Final Cut's own DTD plus semantic checks. If FCP still
complains, reproduce it locally instead of guessing:

```bash
.venv/bin/python -c "
from pathlib import Path; from drone_automation.validate import check
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

## Do not

- Add dependencies without saying what they buy.
- Let CV touch source files.
- Present a guessed parameter as validated — say when something is a guess.
- Change `config.py` for one video's taste; that is what project overrides are for.
- Claim a TikTok edit exists when only a 16:9 cut was produced.
