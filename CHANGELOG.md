# Approved stages

One row per edit signed off in Final Cut. Metrics come straight from the `build`
output, so a stage can be compared to the next without re-running it.

Return to any stage with `git checkout <tag>`.

## Plovdiv

| tag | cuts | mean shot | coverage | effects | notes |
|---|---|---|---|---|---|
| `plovdiv-v6` | 47 | 4.81s | 81% | 16 sped up, 2 escalates, 4 reversed | Locked timeline — opening restored to v4's order (City 1 first). Hill Tower's overexposed head skipped, cascading its remaining uses forward. Second escalate before 1:00, fitted to 160%→403% (footage-limited). |
| `plovdiv-v5` | 47 | 4.81s | 81% | 16 sped up, 1 escalate, 4 reversed | Phrase-snapped sections: 2:11 and 2:21 now on the beat. Pinned City 2 @0:32.83 and City 7 @0:37.87. Picture and music fade together 222.03→226.03s. Opener drifted to City 5 as a side effect — caught and fixed in v6. |
| `plovdiv-v4` | 49 | 4.61s | 83% | 14 sped up, 1 escalate, 5 reversed | Escalate on Hills Monument at 0:10–0:20: 200% body, 2000% final second. Order matches v3 through 2:28. |
| `plovdiv-v3` | 49 | 4.61s | 80% | 15 sped up, 2 punch ramps, 5 reversed | Opening order approved. Speed-up only, no slow motion. Zero repeated source ranges. |

### History

- **v1** — first working timeline. 62 cuts, mean 3.64s. Pacing liked; a
  60-second stretch of identical 2.50s cuts was not.
- **v2** — phrase accents broke up the metronomic run; reuse penalty changed
  from counting uses to decaying with recency, which stopped the engine
  degenerating into round-robin and putting hovers on the drop.
- **v3** — slow motion removed entirely after review (it read as a mistake on
  this footage); retiming became speed-up only. Punch ramps into peaks. Auto
  reverse for clips travelling the same direction. Coverage 59% → 80%.
- **v4** — the 1.0x-start punch ramp replaced by the escalate: 200% throughout,
  2000% across the last second, launching into the next clip. Placed explicitly
  via `ESCALATE_AT_BARS` rather than won by scoring, because a scored escalate
  took slots from other clips and reshuffled the running order.
- **v5** — `SNAP_SECTIONS_TO_PHRASE` turned on, fixing 2:11 and 2:21 at the cost
  of re-laying the slot grid (37 of 47 positions moved from v4). Added
  `PIN_CLIPS` / `PIN_SLOT_BARS` for hand-placing a clip in a slot, and a picture
  fade to black under the closing music fade. **Regression**: the opener shifted
  from City 1 to City 5 as an uncalled-out side effect of the re-lay.
- **v6** — the running order is now **locked** (`projects/plovdiv.lock.toml`):
  `build` replays the approved slot grid and clip assignment verbatim, so
  tuning elsewhere can no longer reshuffle it. The v5 opener regression is
  fixed — restored to v4's City 1. Hill Tower's overexposed first segment is
  skipped via `CLIP_HEAD_SKIP`, cascading each remaining use forward by one
  segment; the freed slot goes to unused footage. A second escalate added
  before the 1:00 cut, but the ideal 200%→2000% profile doesn't fit — City 11
  owes 22.5s to its later slots in the locked order, so the escalate fits
  itself down to whatever speed the spare footage can fund (160%→403% here)
  rather than borrowing from those slots and moving the timeline again.

### Known open items

- **3:22 lands 1.07s early.** The accent sits at bar 80.42 — roughly beat 3 —
  and the engine cuts only on bar lines, so 3:20.93 and 3:23.44 are the only
  reachable points. Needs slot lengths expressed in beats.
- **The 1:00 escalate is capped at 403%, not 2000%**, because City 11 is
  committed to three later slots in the locked order. Getting the full ramp
  there means freeing one of those slots (moves the timeline) or choosing a
  different, less-committed clip for that launch.
- **Slice selection is sequential**, so the back half of the longest takes is
  reached only through reuse. Spreading each clip's slices across its full
  length is the obvious next improvement.
- **Editing the timeline now means editing `plovdiv.lock.toml` directly**
  (swap a `clip` value, adjust `bars`, or set `rate`) rather than retuning
  `config.py` weights — that's the point of the lock, but worth remembering so
  a future request for "more variety" or "less repetition" isn't chased through
  scoring parameters that no longer apply to this project.
