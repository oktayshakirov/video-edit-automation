# Drone Automation

Turns a folder of graded drone selects plus a music track into a **Final Cut Pro
XML timeline** — clips chosen, ordered, trimmed and cut on the music's bar grid.
Open it in Final Cut and do the taste pass.

**It never renders video.** It reads, analyses and writes an XML file. No
transcoding, no proxy rendering of output, no MP4 export.

## Status

| Phase | What | State |
|---|---|---|
| 1 | Clip index — proxy cache, CV metrics, motion classification | working; motion thresholds **unvalidated guesses** |
| 2 | Music analysis — tempo, bar grid, downbeat, energy, sections | working; **downbeat phase is heuristic** |
| 3 | Edit decisions — shot choice, length, speed, variety | working; taste weights tuned by hand against real output |
| 4 | FCPXML export | working; validated against Final Cut's own DTD |

## Setup

```bash
brew install ffmpeg
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

# make the skills available in any session, from any folder
ln -s "$PWD/.claude/skills/video-drone-long"  ~/.claude/skills/video-drone-long
ln -s "$PWD/.claude/skills/video-drone-short" ~/.claude/skills/video-drone-short
```

The symlinks matter: skills under `.claude/skills/` are project-scoped, so
without them the commands are invisible when a session starts in a footage
folder rather than in this repo.

Two skills, deliberately. **`/video-drone-long`** produces a long-form FCPXML
timeline and never renders video. **`/video-drone-short`** renders vertical MP4s for
TikTok and Shorts, with text and optional narration. They share the clip index
but have different pacing models, different output, and different numbers behind
them — one skill covering both would need a description vague enough to hurt
routing.

Requires macOS with Final Cut Pro (its DTD is used for validation) and Python
3.11+ (`tomllib`).

## Use

```bash
.venv/bin/python -m drone_automation index ~/Desktop/Plovdiv          # once per batch
.venv/bin/python -m drone_automation build --project plovdiv --dry-run
.venv/bin/python -m drone_automation build --project plovdiv
```

`index` is incremental — clips are identified by a partial hash (size + first
and last 1MB), so re-running skips anything already indexed. `--reanalyze`
keeps the cached proxies but recomputes every metric; that is the flag for
tuning indexer thresholds, and it costs seconds rather than minutes.

`build --dry-run` reruns the entire decision engine and prints the edit list
without writing XML. **This is the tuning loop** — read the list, adjust, repeat.
`--click` writes a WAV of the track with clicks on every bar line, to check the
beat grid by ear.

The older explicit form still works: `build <footage> --music <track>`.

## Repository layout

```
drone_automation/           the package
  config.py         every tunable, grouped by phase, GUESS-marked where unvalidated
  media.py          ffprobe/ffmpeg wrappers, clip hashing, proxy build
  analysis.py       per-frame CV, motion fit, move classification
  music.py          beat grid, downbeat phase, energy envelope, sections
  edit.py           slot filling, clip scoring, speed decisions, frame snapping
  fcpxml.py         Jinja-rendered FCPXML
  validate.py       DTD + semantic checks before anything reaches Final Cut
  project.py        per-video TOML loading and config overrides
  cli.py            subcommands: index, report, build
projects/           one .toml per video — see projects/README.md
.claude/skills/     video-drone-long, video-drone-short — symlink into ~/.claude/skills/
assets/             reusable overlays + captured FCPXML fragments
CHANGELOG.md        approved stages and their metrics
```

Footage and proxies are **not** in the repo. Proxies and the SQLite index live
in `.analysis_cache/` inside each footage folder, so a batch carries its own
analysis and archiving a shoot keeps it.

## Adding a video

See [projects/README.md](projects/README.md). Short version: copy a `.toml`,
repoint `footage` and `music`, index, dry-run, tune under `[overrides]`, build.

`config.py` is the shared baseline across all videos. Per-video taste goes in
that video's project file, never in `config.py`.

## Saving an approved stage

When an edit is good, tag it so it can be returned to exactly:

```bash
git add -A
git commit -m "plovdiv: <what changed>"
git tag plovdiv-v3 -m "49 cuts, 80% coverage, opening order approved"
```

Record the metrics in `CHANGELOG.md`. Going back is then `git checkout
plovdiv-v3` instead of reconstructing settings from memory.

## Design notes

- Analysis only ever touches the 320px/10fps proxy. Source files are read for
  hashing (2MB) and proxy generation, never by OpenCV.
- Motion is a RANSAC partial-affine fit over sparse Lucas-Kanade tracks. Dense
  Farneback was rejected: slower, and it degrades badly on the smooth sky and
  water that fill most drone frames.
- The bar grid is a **fitted regular grid**, not librosa's raw beat times.
  Produced music is metronomic; every bar line is computed closed-form as
  `phase + period * n`, so rounding error stays bounded at half a frame instead
  of accumulating over four minutes.
- Downbeat phase is voted using onset strength **restricted to the low band**.
  A full-band vote picks the snare on beats 2 and 4 and puts every cut on the
  backbeat. This remains the weakest inference in the pipeline — `--click`
  exists to check it.
- The engine works **backwards from the usual approach**: each slot picks clip
  and length together, so shot rhythm follows what the footage can deliver
  rather than a grid imposed on it. A select is never asked to be longer than
  it is.
- **Retiming is speed-up only.** Nothing plays below 1.0x. A clip that cannot
  fill a slot at natural speed loses the slot; long takes are run at 2x instead
  of being half-discarded. The validator fails the build if any timeMap segment
  drops under real time.
- Output is checked twice, and the layers catch different things. `xmllint`
  against Final Cut's **own** DTD catches element-order and structural errors.
  Hand-written checks catch what a DTD cannot see — a timeMap contradicting
  `start`, a spine discontinuity, an out-of-bounds source range, the same source
  seconds used twice.
- Clips whose framing barely changes over a short window (`orbit`, `lateral`)
  get a minimum shot length: two short cuts from one read as the same shot
  played twice.
- Two clips travelling the same direction are detected by the sign of their
  dominant translation axis, and every second one is reversed.
- The one ramp is an *escalate*: 200% through the body of the shot, launching to
  2000% across its final second so it slings into the next clip. Source position
  is the integral of that speed profile — linear through the body, quadratic
  through the tail — and the slope of that curve *is* the playback speed, so it
  holds at 200% and only ever climbs. Control points are concentrated in the
  tail: sampled evenly, the whole launch collapses into one averaged segment and
  plays as a step rather than a ramp.
- Escalates are placed by `ESCALATE_AT_BARS`, per project, **not** by scoring.
  When they competed for slots on merit they won them from other clips and
  reshuffled the running order. Applied as a positional upgrade after the clip
  is chosen, switching one on changes only how that clip plays — though it does
  consume more of that clip, which can still move its later appearances.

## Known limits

- **Cuts land on bar lines only.** An accent falling mid-bar cannot be hit
  exactly. Half-bar cut points would need slot lengths in beats, not bars.
- **Phrase-snapped section boundaries and an approved running order are mutually
  exclusive.** Slots restart at every boundary, so moving one re-lays the whole
  grid downstream and changes which clip lands where — 39 of 49 positions in
  practice. `SNAP_SECTIONS_TO_PHRASE` is the switch. Half-bar cutting would
  soften this, since an off-phrase boundary would cost half a bar, not a whole
  one.
- **Slice selection is sequential**, not content-aware: each clip is carved from
  the head forward. The back of a long take is used only if the clip is reused
  enough times to reach it, which biases against the *end* of push-ins and
  pull-backs where the reveal usually lands.
- **Location grouping is weak** — derived from the leading word of the filename,
  so the same-location variety penalty rarely fires. Real grouping needs visual
  clustering.
- `sharpness` measures texture density on a compressed proxy, not focus. Treat
  it as "how much detail is in frame", not as a quality gate.
- **TikTok profile is declared but not implemented.** Vertical reframing is not
  built; `profile` currently only labels a project.
