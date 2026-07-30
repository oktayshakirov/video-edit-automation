---
name: drone-automation
description: Build or tune a music-synced Final Cut Pro timeline from graded drone selects. Use when the user wants to cut footage to a track, generate or regenerate an FCPXML, adjust pacing/speed/shot-selection of an existing edit, index a new batch of footage, save an approved edit stage, or diagnose an FCPXML that Final Cut refused to import.
---

# Drone Automation

Turns a folder of graded drone selects plus a music track into a Final Cut Pro
XML timeline. **It never renders video** — it reads, analyses and writes XML.

## Setup check

```bash
ffmpeg -version | head -1        # required; brew install ffmpeg
ls .venv || python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
```

All commands run from the repo root as `.venv/bin/python -m drone_automation ...`.

## The loop

```bash
.venv/bin/python -m drone_automation index  <footage>              # once per batch; slow, then cached
.venv/bin/python -m drone_automation build  --project <name> --dry-run   # edit list, seconds
.venv/bin/python -m drone_automation build  --project <name>             # writes the FCPXML
```

**Always `--dry-run` first when tuning.** It reruns the whole decision engine in
seconds off cached proxies and prints the full edit list — clip, timecode, shot
length, section, source in-point, speed, effects — plus coverage and per-clip
usage. Read that before regenerating XML.

## Tuning

Every knob is in `drone_automation/config.py`, grouped by phase, with `GUESS` marking
values never validated against real output. Per-video changes belong in
`projects/<name>.toml` under `[overrides]`, not in `config.py` — that file is
the shared baseline across all videos.

Map a complaint to the right knob:

| Symptom | Look at |
|---|---|
| too many / too few cuts | `SLOT_BARS_BY_ENERGY`, `PHRASE_ACCENT_MULTIPLIER` |
| one clip dominates | `MAX_USES_BY_MOVE`, `PENALTY_OVERUSE` |
| feels repetitive though frames differ | `REUSE_RECENCY_WINDOW`, `MIN_SLOT_BARS_BY_MOVE` |
| wrong footage on the drop | `W_ENERGY_MATCH`, and the Phase 1 `motion_energy` weights |
| shots too long | `MAX_SHOT_SECONDS`, `LEGAL_SLOT_BARS` |
| speed effects overused | `SPEEDUP_MIN_REMAINING`, `PENALTY_SPEEDUP_WHEN_CALM` |
| not enough footage used | `W_COVERAGE`, `W_BITE` |
| two clips move alike | `AUTO_REVERSE`, `REVERSIBLE_MOVES` |
| want a speed launch into a cut | `ESCALATE_AT_BARS` (per project) |
| cuts feel a beat late | `SNAP_SECTIONS_TO_PHRASE` — read the warning below |

## Protecting an approved running order

The scorer is greedy: any change to weights, section boundaries, or slot
lengths re-lays the whole grid downstream and can reshuffle every clip after
the change point. Tuning parameters cannot reliably preserve an approved
timeline — this was tried three separate times on Plovdiv and reshuffled the
order every time, including one round where the opening shot changed as an
uncalled-out side effect.

**Once a project has an approved edit, lock it.** `build --lock-out
projects/<name>.lock.toml` dumps the current slot grid and clip assignment.
Reference it from the project file (`lock = "<name>.lock.toml"`), and `build`
replays it verbatim — the scorer is bypassed entirely, so nothing tuned
elsewhere can move a clip that isn't named in the request.

With a lock in place, a request to swap or resize one shot is a **direct edit
to the lock file** — change the `clip` value, the `bars` count, or `rate` — not
a scoring change. This is the only way to guarantee everything else stays put.
Effects that consume extra source (escalates, 2x) can still be capped by what a
clip owes its *other* locked slots; when that happens, fit the effect down to
what's actually available (see `fit_escalate` in `edit.py`) and say what the
achieved numbers are, rather than silently taking footage from a later slot and
moving the timeline anyway.

For a project **without** a lock yet, dry-run any structural change and diff
the clip order against the last approved tag before presenting it:

```bash
git show <tag>:/dev/null 2>/dev/null; .venv/bin/python -m drone_automation build --project <p> --dry-run
```

If positions move, say so and let the user choose — never present a reshuffled
edit as if only the requested thing changed.

Change one thing per round. A batch of changes that includes one the user
dislikes tends to take the good parts down with it.

## Hard constraints

- **Never slower than 1.0x.** Slow motion is a non-goal; the validator fails the
  build if any timeMap segment drops below real time. Long clips get sped up,
  short clips lose the slot — a clip is never stretched to fit.
- **Analysis only touches proxies** in `<footage>/.analysis_cache/`, never the
  source files.
- **Cuts land on bar lines only.** An accent falling mid-bar cannot be hit; the
  nearest legal point is up to half a bar away. Fixing that needs slot lengths
  expressed in beats rather than bars.

## When Final Cut rejects the import

`build` already validates against Final Cut's own DTD plus semantic checks. If
FCP still complains, reproduce it locally rather than guessing:

```bash
.venv/bin/python -c "
from pathlib import Path; from drone_automation.validate import check
print(check(Path('<file>.fcpxml')) or 'clean')"
```

Two failure classes, and they need different tools:

- **DTD / element order** — caught by `xmllint` against the bundled FCP DTD.
  Note the DTD lives inside `Final Cut Pro.app`, whose path contains spaces, so
  it is staged to a space-free temp path first; pointing xmllint straight at the
  bundle fails with a misleading "Could not parse DTD".
- **Semantic** — attribute values a DTD cannot reason about. The known trap: a
  clip carrying a `<timeMap>` must have `start="0s"`, with its in-point in the
  first `timept value`. Setting both makes FCP report *"Invalid edit with no
  respective media"* and silently drop the clip.

## Saving an approved stage

When the user says an edit is good, record it so it can be returned to exactly:

```bash
git add -A
git commit -m "<project>: <what changed>"
git tag <project>-vN -m "49 cuts, 80% coverage, opening order approved"
```

Add a row to `CHANGELOG.md` with the metrics from the build output. Reverting is
then `git checkout <tag>` rather than reconstructing settings by hand.

## Do not

- Add dependencies without saying what they buy.
- Let CV touch source files.
- Present a guessed parameter as a validated one — say when something is a guess.
- Change `config.py` for a single video's taste; that is what project overrides
  are for.
