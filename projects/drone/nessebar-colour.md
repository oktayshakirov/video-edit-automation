# Nessebar — colour consistency pass

Hand-applied in Final Cut. **FCPXML cannot carry this**: version 1.10 has no
colour element at all (the whole `adjust-*` set covers crop, transform, blend,
stabilisation and volume, nothing else). Colour would have to go through
`<filter-video>` referencing an `<effect uid="…">`, where the UID and parameter
names are FCP-internal identifiers — the same class of guess that caused two
failed imports earlier in this project. So these are dial-in values, not
generated XML.

Targets are the library medians: **brightness 0.675**, **saturation 0.433**,
**detail 536**. Deltas are derived from the measured index, not estimated by eye.

The exposure spread across the batch is **1.26 stops** (0.344 to 0.823), which
is wider than Plovdiv's and sits mostly between the low-altitude and
high-altitude shots — so it reads as a step every time the edit cuts between
them, which it does constantly.

## Apply — exposure

Do these first. Brightness steps are the most visible mismatch and the cheapest
to fix.

| clip | measured | correction | why |
|---|---|---|---|
| **Coast Houses Above 2** | 0.344 bright, detail 32 | **exposure +0.97 stops**, **dehaze / contrast lift** | darkest in the batch, and detail is **17× below the median** — that is haze, not softness. Used 3× |
| **Coast Above 1** | 0.353 bright, detail 314 | **exposure +0.94 stops** | second darkest; detail is low but not pathological |
| **Coast Above 2** | 0.356 bright, detail 64 | **exposure +0.92 stops**, **dehaze / contrast lift** | **highest-value fix in the list** — 8× below median detail *and* used 4×, more than any other clip |
| **Coast 4** | 0.420 bright | **exposure +0.69 stops** | still visibly under the cluster |
| **Coast Houses Above 1** | 0.485 bright | **exposure +0.48 stops** | borderline; judge after the four above |
| **Coast Above 3** | 0.495 bright | **exposure +0.45 stops** | borderline; judge after the four above |

The bright end (Coast Houses 2, 4, 3 and Coast 2, all −0.18 to −0.29 stops) is
within a third of a stop of the median. Pull them down only if the top end still
reads hot once the dark clips have come up — correcting both directions at once
tends to overshoot.

## Apply — saturation

| clip | measured | correction | why |
|---|---|---|---|
| **Coast 1** | 0.14 sat | **saturation ×3.1** (0.14 → 0.43) | by far the largest single outlier in the batch — less than a third the saturation of anything else. Combined with 6.1% clipped highlights it reads as a washed-out, hazy frame rather than a stylistic choice |
| **Coast 2** | 0.27 sat | **saturation ×1.6** | same family, milder |
| **Coast 3** | 0.32 sat | **saturation ×1.35** | same family, milder |
| **Windmill** | 0.30 sat | **saturation ×1.4** | the only orbit, so it is conspicuous whenever it appears |

Note this runs **opposite** to the Plovdiv pass, where the correction was to pull
an over-saturated clip down. Here the outliers are under-saturated.

## Leave alone

Coast Houses 1, Coast Houses 3, Coast Houses 4, Coast Houses 2 — all sit inside
the cluster on brightness and saturation both. Coast Houses 2 is the brightest
clip at −0.29 stops, which is close enough to leave until the dark end is fixed.

## Deliberately not doing

- **Flattening the hue spread.** Eleven of fourteen clips sit in a tight
  blue-cyan band (165–209°). The three that do not are Coast Houses Above 1 at
  30° (warm, and genuinely a different light), and the two green-reading clips
  at 111° and 123° — which are also the two haziest shots in the batch. That
  green is atmospheric scattering over water, not a grading error, and it should
  come back toward the cluster on its own once the dehaze above is applied.
  **Re-measure before touching temperature**, and only nudge what is still off.
- **Recovering Coast 1's highlights.** 6.1% of the frame is clipped. These are
  graded exports — pixels at 255 have nothing behind them, so pulling highlights
  down yields flat grey, not detail. Only a re-export from the original would
  change that. The saturation lift above is the useful half of this fix.

## Order of work

1. **Coast Above 2** — worst haze, most used (4 cuts). Exposure, then dehaze.
2. The other three exposure lifts of ~0.9 stops.
3. **Coast 1** saturation. It is the single most conspicuous frame in the batch.
4. Stop and look. Then decide on the two borderline exposures and any hue nudge.

## Making this automatable later

The reliable route is a round trip: apply one correction to one clip in Final
Cut, `File ▸ Export XML`, and read the exact `<effect uid>` and parameter names
out of the result. After that these values can be generated directly and this
becomes a one-line-per-clip project setting rather than manual work — for this
video and every future one. Unchanged from the Plovdiv write-up; still the
single highest-leverage unbuilt feature in the pipeline.
