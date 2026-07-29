# Approved stages

One row per edit signed off in Final Cut. Metrics come straight from the `build`
output, so a stage can be compared to the next without re-running it.

Return to any stage with `git checkout <tag>`.

## Plovdiv

| tag | cuts | mean shot | coverage | effects | notes |
|---|---|---|---|---|---|
| `plovdiv-v3` | 49 | 4.61s | 80% | 15 sped up, 2 punch ramps, 5 reversed | Opening order approved. Speed-up only, no slow motion. Zero repeated source ranges. |

### History leading to v3

- **v1** — first working timeline. 62 cuts, mean 3.64s. Pacing liked; a
  60-second stretch of identical 2.50s cuts was not.
- **v2** — phrase accents broke up the metronomic run; reuse penalty changed
  from counting uses to decaying with recency, which stopped the engine
  degenerating into round-robin and putting hovers on the drop.
- **v3** — slow motion removed entirely after review (it read as a mistake on
  this footage); retiming became speed-up only. Punch ramps into peaks. Auto
  reverse for clips travelling the same direction. Coverage 59% → 80%.

### Known open items

- 3:22 cut lands 1.07s early. The accent falls mid-bar and the engine only cuts
  on bar lines — needs slot lengths in beats.
- Section boundaries are placed by equal division, not by detecting where the
  track actually changes. A novelty-based version was tried and reverted
  together with an unrelated batch of changes; worth retrying **on its own**.
- City 7 wanted somewhere in the first minute; currently first appears later.
