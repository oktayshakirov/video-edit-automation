# Projects

One TOML file per video. Each pins its footage folder, its track, and any tuning
that differs from the shared defaults, so a video is reproducible from one file
and `drone_automation/config.py` stays the common baseline rather than being rewritten
per shoot.

```bash
.venv/bin/python -m drone_automation build --project plovdiv
.venv/bin/python -m drone_automation build --project plovdiv --dry-run     # edit list only, seconds
```

## Fields

| key | required | meaning |
|---|---|---|
| `name` | no | project label; defaults to the filename |
| `footage` | **yes** | folder of graded selects; `~` is expanded |
| `music` | **yes** | the track |
| `profile` | no | `youtube` (default) or `tiktok` |
| `out` | no | where to write the FCPXML; defaults next to the footage |
| `[overrides]` | no | any constant from `drone_automation/config.py` |

Footage is never committed. Only the recipe is.

## Overrides

Keys must exist in `config.py` — a typo is an error, not a silent no-op, so a
misspelled override can't leave the default in place while you hunt through the
edit wondering why nothing changed.

Overrides reach phases 2–4 (music, edit decisions, export). Indexing constants
(proxy size, tracker settings, motion thresholds) are baked into the clip index
when it is built, so changing those means re-running `index --reanalyze`.

## Adding a video

1. Copy an existing `.toml` and repoint `footage` and `music`.
2. `.venv/bin/python -m drone_automation index <footage>` — slow once, cached afterwards.
3. `.venv/bin/python -m drone_automation build --project <name> --dry-run` and read the edit list.
4. Tune under `[overrides]`, repeat step 3.
5. `.venv/bin/python -m drone_automation build --project <name>`, import, review in Final Cut.
6. When it's good, commit and tag — see the root README.
