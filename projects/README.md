# Projects

One directory per **site and format**. The format is in the directory name, and
that is the whole point of the naming: `projects/crypto` and
`projects/crypto-long` sat side by side for months and nothing said which one
held the Shorts — you had to open a file and look at the frame size. Renamed
2026-08-18 on the user's instruction.

| directory | site | format | entry point |
|---|---|---|---|
| `crypto-short/` | thecrypto.wiki | vertical 1080x1920, 30-60 s | `render_crypto_short` |
| `crypto-long/` | thecrypto.wiki | 16:9 1920x1080, 2:30-4:00 | `render_long` |
| `tinnitus-short/` | tinnitushelp.me | vertical, article shorts and ASMR | `render_crypto_short` / `asmr` |
| `tinnitus-long/` | tinnitushelp.me | 16:9, explainers and sound sessions | `render_long` |
| `drone-long/` | drone channel | 16:9 Final Cut timeline, cut to music | `drone build --project` |

Drone **shorts** have no project directory: that pipeline takes a clip and a
line of text on the command line and keeps nothing per video. If it ever grows
a recipe file it goes in `drone-short/`, not back into `drone-long/`.

## One file per video, hand-written

Every file here is a script: the narration, the shot list, and a docstring
saying why this angle and not another one. **Script generation from the site's
MDX is deliberately not built** and is recorded in both long-form skills as a
thing not to build — the script is the product, and 130 generated ones is the
mass-production failure mode the platforms suppress, arrived at by a different
route.

Run every one of them from the repo root:

```bash
PYTHONPATH=. .venv/bin/python projects/<dir>/<name>.py
```

Renders go to the Desktop. They are uploads, not repo artifacts, and nothing
here writes into the site repos.

## What is kept, and where

`crypto-long/transcripts/` holds the `.srt` and the `.md` sidecar for each
long-form cut. They are kept because they were lost once: both were cleaned off
the Desktop before the site's `/videos/<slug>` transcript pages needed them, and
the transcripts had to be rebuilt from `SECTIONS[].sentences` plus the chapter
times in the YouTube description. That only worked because the script was in the
repo. Copy them here on every render.

Drone projects keep a `.toml` recipe and a `.lock.toml` of the approved edit;
footage is never committed. See `drone-long/README.md`.
