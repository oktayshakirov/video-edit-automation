# Video Automation

A Python engine that turns articles, raw drone footage and a written script
into finished, platform-ready videos: long-form 16:9 explainers, vertical
Shorts and Reels, quiz Shorts, 20-minute sound-therapy sessions, and Final Cut
Pro timelines cut to music. It runs three real channels end to end, from topic
research to upload.

| Channel | What it builds |
|---|---|
| **The Crypto Wiki** ([thecrypto.wiki](https://thecrypto.wiki)) | An article becomes a narrated long-form explainer and its vertical Short, written together so the Short is not a trailer |
| **Tinnitus Help** ([tinnitushelp.me](https://tinnitushelp.me)) | The same explainer pair, plus sound-therapy sessions: generated or recorded noise beds with a paced-breathing guide |
| **Drone** | A Final Cut Pro timeline (FCPXML) cut to the bar grid of a music track, or a vertical quote / POV Short |

About 60 long-form videos and their Shorts, around 20 drone Shorts and seven
drone edits have been built with it.

## How a video is made

1. **Script.** Every video is a hand-written Python file in `projects/`: the
   narration, the shot list, and a docstring saying why this angle and not
   another. Scripts are deliberately not generated from the article.
2. **Voice.** Local [Kokoro](https://github.com/thewh1teagle/kokoro-onnx) TTS
   through named voice profiles, with a pronunciation layer and word-level
   caption alignment.
3. **Picture.** Drawn data beats (bars, grids, checklists, comparisons,
   annotated photos), screened Pexels stock, site photography and archive
   images, composed per sentence so the visual always matches the line being
   spoken.
4. **Sound.** Generated music beds and sound effects, ambience under footage,
   and a small library of licensed tracks.
5. **Render.** FFmpeg and Pillow for 16:9 and 9:16, HDR (HLG) where the source
   is HDR, thumbnails for both shapes, an SRT and a metadata sidecar.
6. **Publish.** YouTube via the Data API (from a separate analytics CLI), Instagram and Facebook Reels and
   Telegram through n8n workflows, TikTok as an inbox draft, and the site's
   video registry.

Drone long-form takes a different route: it indexes a folder of clips with
OpenCV, fits a bar grid to the music with librosa, picks clip, length and speed
for every slot, and writes FCPXML that is validated against Final Cut's own DTD
before it is opened.

## Repository layout

```
video_automation/
  core/        shared engine: voices, TTS and captions, vertical crop, type,
               brand, backgrounds, music, sound effects, stock, HDR, datamosh
  longform/    the 16:9 format shared by both sites: plan, beats, openers,
               overlays, thumbnails, metadata
  crypto/      the vertical article format and its fact extraction
  tinnitus/    vertical article cuts and the sound-therapy sessions
  quiz/        three-question quiz Shorts with a timed reveal
  drone/       clip analysis, music analysis, edit decisions, FCPXML export
  publish/     the TikTok uploader
projects/      one script per video, one directory per site and format
docs/video/    every build rule, once: start at docs/video/README.md
docs/publish/  the per-platform publishing notes
.claude/skills/ the build, publish and audit workflows as Claude Code skills
assets/        brand assets, credited archive images, the stock manifest
tests/         fast checks that never render, synthesise or touch the network
tools/         asset audits, stock pruning, topic suggestions
```

## Setup

Requires macOS (Final Cut Pro for the drone timelines), Python 3.11+ and
FFmpeg.

```bash
brew install ffmpeg espeak-ng
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest tests
```

The Kokoro model (~350MB) lives in `~/.local/share/kokoro`. Footage, renders,
stock bytes and credentials are never committed.

## Usage

Render one video from its script:

```bash
PYTHONPATH=. .venv/bin/python projects/crypto-long/bitcoin-price.py
PYTHONPATH=. .venv/bin/python projects/crypto-short/bitcoin-price.py
```

Cut a drone edit to music:

```bash
.venv/bin/python -m video_automation drone index ~/Desktop/Plovdiv          # once per batch
.venv/bin/python -m video_automation drone build --project plovdiv --dry-run
.venv/bin/python -m video_automation drone build --project plovdiv
```

`build --dry-run` reruns the whole decision engine and prints the edit list
without writing XML; `--click` writes the track with a click on every bar line
to check the beat grid by ear.

Audition and verify voices:

```bash
.venv/bin/python -m video_automation voices list
.venv/bin/python -m video_automation voices verify
```

A profile is the whole recipe (voice, Kokoro speed and post chain), named
after a person rather than the model voice underneath. Kokoro's ONNX inference
is deterministic, so `verify` checks each profile still reproduces its
audition sample-for-sample.

## Agent workflows

The build and publish steps run as [Claude Code](https://claude.com/claude-code)
skills in `.claude/skills/`: `/video-crypto`, `/video-tinnitus`, `/video-drone`,
`/video-quiz` and `/video-glitch` build; `/publish-video` uploads;
`/video-views-audit` and `/video-performance-review` read the analytics back and
turn them into rule changes. The skills hold only the order of the work. Every
rule they rely on lives once in `docs/video/`, with the reason it exists.

## Design notes: the drone edit engine

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
