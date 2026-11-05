# Working from a cloud session

The build runs on the Mac. A Claude Code cloud session is a Linux container
with a fresh clone of this repo and none of what the Mac has collected: no
stock bytes (gitignored, re-fetched from Pexels by key), no brand sound
files, no macOS fonts, no credentials, no Final Cut. **So a cloud session
never renders a video that ships, and never publishes.** It can do most of
what comes before the render, and all of what keeps the engine honest.
Measured in the first one, 2026-11-05.

## Setup

```bash
bash tools/cloud_setup.sh             # venv from the pins, the two site repos
bash tools/cloud_setup.sh --kokoro    # ...and the Kokoro model, ~350MB, ~15s
git fetch --unshallow                 # script_check reads first-commit dates
```

The site repos are sparse, shallow clones into `~/Coding/`, where the engine
already looks for them - posts, the video registry and images only (~70MB).
The script refuses to run on macOS and never touches a checkout it did not
create.

## What works

| Work | How |
| --- | --- |
| The test suite | `.venv/bin/python -m pytest tests -q`. `core.fontshim` answers the missing macOS fonts with free ones; the suite asserts no typeface. Also runs in CI on every push (`.github/workflows/tests.yml`) |
| Topic suggestions | `python3 tools/topics.py crypto` - workflow step 1, against the cloned sites. Demand research on YouTube is a web search, so that works too |
| A teardown | `demand/README.md`, "Teardown" - reading and writing, nothing to render |
| Writing the pair | workflow step 2, in full. The script is a Python file and the rules are docs |
| Every static gate | `tools/opening_check.py`, `tools/script_check.py` |
| Runtime and chapters | `longform.preflight` with `--kokoro`: real synthesis, ~1m40s for a 3:40 long form. **Every clip slot reads FAIL** - the stock files are not there - so only the runtime and the chapter list mean anything |
| Engine work on beats and overlays | change the code, run the tests, draw a frame with the shim installed and look at the layout - not at the type |

**One caveat on preflight's runtime.** It is Kokoro on x86 Linux, not on the
Mac's ARM; the ONNX arithmetic can differ in the last bits, so treat the
runtime as within a fraction of a second, not sample-exact. The cache key
keys on package versions and weights, not on the CPU, so never copy a cloud
narration cache to the Mac.

## What does not

- **A render.** No stock bytes, no `assets/brand/sfx/` (the build would fall
  back to synthesized stand-ins), and the fonts are stand-ins. A frame drawn
  here is for checking layout, never a thumbnail or a cover.
- **Importing a few scripts.** Four call `ticker_card` or a memecoin card at
  module level, which draws *and saves* a PNG into `assets/` on import, so
  they need the real fonts. `script_check` and the suite skip them here. Do
  not install the font shim to get past it: it would overwrite a committed
  card with the stand-in face (it did, once, while the import test was being
  written).
- **Publishing**, the analytics pulls, the TikTok uploader - credentials stay
  on the Mac, and `/publish-video` gets a fresh local session by design
  (`workflow.md` step 5).
- **Drone.** The footage is on the Mac. `video_automation.drone` can be
  tested, not run.

## The hand-back

A cloud session that drafted a pair ends where step 2 ends: both scripts
committed to its branch with the opening check, the script check and the
preflight runtime in the commit message or the PR body. The Mac session picks
the branch up at step 3 - preflight again for the clip margins, then build.
