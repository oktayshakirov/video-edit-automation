# Approved stages

One row per edit signed off in Final Cut. Metrics come straight from the `build`
output, so a stage can be compared to the next without re-running it.

Return to any stage with `git checkout <tag>`.

## Plovdiv

| tag | cuts | mean shot | coverage | effects | notes |
|---|---|---|---|---|---|
| `plovdiv-v5` | 47 | 4.81s | 81% | 16 sped up, 1 escalate, 4 reversed | Phrase-snapped sections: 2:11 and 2:21 now on the beat. Pinned City 2 @0:32.83 and City 7 @0:37.87. Picture and music fade together 222.03→226.03s. |
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
  of re-laying the slot grid (37 of 47 positions moved). Added `PIN_CLIPS` /
  `PIN_SLOT_BARS` for hand-placing a clip in a slot, and a picture fade to black
  under the closing music fade.

### Known open items

- **3:22 lands 1.07s early.** The accent sits at bar 80.42 — roughly beat 3 —
  and the engine cuts only on bar lines, so 3:20.93 and 3:23.44 are the only
  reachable points. Needs slot lengths expressed in beats.
- **2:11 and 2:21 land a bar late**, because section boundaries sit off-phrase
  (bars 25, 49, 57...) and slots restart at every boundary.
  `SNAP_SECTIONS_TO_PHRASE = true` fixes the timing but re-lays the slot grid and
  moved 39 of 49 clip positions, so it is **off** while the running order is
  being approved by hand. Half-bar cutting would likely allow both at once.
- **Nine positions after 2:28 differ from v3**, all shuffles around Hills
  Monument: the escalate consumes 29s of it instead of 10s, so its later slices
  move. Unavoidable while that clip carries the effect and appears five times.
- **City 7 wanted somewhere in the first minute**; currently first appears later.
  A deadline-based placement mechanism was built and reverted — it worked, but
  arrived bundled with changes that altered the opening.
- **Slice selection is sequential**, so the back half of the longest takes is
  reached only through reuse. Spreading each clip's slices across its full length
  is the obvious next improvement.
