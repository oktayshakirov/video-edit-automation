# Approved stages

One row per edit signed off. Long-form metrics come straight from the `build`
output; short-form rows record the parameters the render was approved at, since
those are what reproduce it.

Return to any stage with `git checkout <tag>`.

## Shorts

| video | clip | runtime | voice | text | notes |
|---|---|---|---|---|---|
| Cingene — "self-care" | Sunset Sea 5, `crop=838:1490:1632:624` (zoom 1.45), start 8.0s | 10.55s | `leo`, aligned sentences | Futura Medium 44px, stroke 4, `y_frac=0.64`, `gap=0.65`, `tail=2.2` | First short in `leo`. Approved as the plain-comma variant of a three-way punctuation test — em dashes and ellipses were measurably negligible and lost by ear. A `hover` clip, so framing does not drift and one sampled frame sets `y_frac` for the whole run. Quote is Katie Reed's; the "i read a quote that said" opener carries the attribution. |
| City 1 — "ordinary tuesday" | City 1, `crop=1215:2160:0:0`, start 2.0s | 10.91s | `am_onyx` 0.60 + `am_puck` 0.40, melancholic, aligned sentences | Futura Medium 44px, stroke 4, `y_frac=0.34`, `gap=0.65`, `tail=2.2` | First approved narrated short. Voice is a blend — straight `am_onyx` is graded D on minutes of data; the blend sounded more human across ten candidates. Crop is manual: `pick_crop` chose rooftops at x=1776 and left the sun out. That voice was retired when `leo` was approved; the recipe survives as the `melancholic` chain. |

## Nessebar

| tag | cuts | mean shot | coverage | effects | notes |
|---|---|---|---|---|---|
| `nessebar-v1` | 38 | 6.32s | 83% | 3 sped up, 9 reversed, 0 repeated ranges | First edit on a correctly-detected grid. **librosa reported 152.11 BPM for a 75.00 BPM track**, and the least-squares fit made that look clean — off-beat onsets measured *stronger* than on-beat. Tempo is now found by direct (period, phase) search scored on onset energy: wrong grid scores 0.008, right grid 2.296; downbeat confidence 0.08 → 0.53. Track looped once (hands off 2:08.1, re-enters 0:38.5, 6.4s crossfade, both phrase lines, energy 0.93 vs 0.90) to carry a 2:36 song over a 4:00 picture. Approved on cuts and on the loop seam. |

### History

- **v0** — built on the 152 BPM misread: 53 cuts, mean 2.94s, 63% coverage, cuts
  landing on a grid unrelated to the music. Superseded, never tagged.

## Plovdiv

| tag | cuts | mean shot | coverage | effects | notes |
|---|---|---|---|---|---|
| `plovdiv-v7` | 47 | 4.81s | 74% | 12 sped up, 2 escalates, 4 reversed | City 4 dropped from 2x to 100% (reverse kept) — it read too fast over the city. Order byte-identical to v6. |
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

- **v7** — City 4's four instances dropped from 2x to 100%, reverse retained.
  First change made purely by editing the lock file; the running order came out
  byte-identical, which is what the lock exists to guarantee.

### Colour notes (measured, not yet acted on)

The 15 clips split into two colour families rather than drifting: warm 10-79°
(ten clips) and cool 184-201° (City 11, 4, 3, 2), with City Above alone at 346°.
**20 of 46 cuts jump more than 120° in hue** and this was never flagged during
review — on a ~4.8s average shot length the warm/cool alternation reads as
energy, not error. Treated as taste, not a fault.

More visible than hue, and worth addressing first:

- **Brightness**: City Above (0.41) and Hill Tower (0.43) sit well under the
  0.56-0.70 cluster — roughly a 1.5-stop step at some cuts.
- **Saturation**: Hill Tower (0.59) is ~3x City 1 (0.18) and City 11 (0.19),
  so it reads as the most processed shot whenever it appears.
- **City 11's 28.3% blown highlights are NOT recoverable.** The clipping is the
  sunset cloud, uniform across the whole clip (27.5-29.0% in every 5s window),
  and these are graded exports — pixels at 255 have nothing behind them. What
  *is* fixable there is haze: City 11 measures 186 on detail density, the lowest
  of all 15 and ~10x below the sharpest.

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
