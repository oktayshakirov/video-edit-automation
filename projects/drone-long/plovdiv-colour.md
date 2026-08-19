# Plovdiv — colour consistency pass

Hand-applied in Final Cut. **FCPXML cannot carry this**: version 1.10 has no
colour element at all (the full `adjust-*` set covers crop, transform, blend,
stabilisation and volume, nothing else). Colour would have to go through
`<filter-video>` referencing an `<effect uid="…">`, where the UID and parameter
names are FCP-internal identifiers — the same class of guess that caused two
failed imports earlier in this project. So these are dial-in values, not
generated XML.

Targets are the library medians: **brightness 0.63**, **saturation 0.24**.
Deltas below are derived from the measured index, not estimated by eye.

## Apply

| clip | measured | correction | why |
|---|---|---|---|
| **City Above** | 0.41 bright | **exposure +0.61 stops** | darkest clip; ~1.5 stops under the brightest |
| **Hill Tower** | 0.43 bright, 0.59 sat | **exposure +0.56 stops**, **saturation ×0.52** (0.59 → 0.31) | darkest *and* ~3× the saturation of the least-saturated clip; reads as the most processed shot in the video |
| **City 11** | hue 184°, detail 186 | **small warm temperature nudge**, **contrast / dehaze lift** | lowest detail density of all 15 (~10× below the sharpest) — that is haze, and haze responds well |
| **City 4** | hue 195° | small warm temperature nudge | cool family |
| **City 2** | hue 201° | small warm temperature nudge | cool family |
| **City 3** | hue 195° | small warm temperature nudge | cool family |

## Leave alone

City 1, City 5, City 6, City 7, City 8, City 9, City 10, City 12,
Hills Monument — all sit inside the cluster on every axis.

## Deliberately not doing

- **Neutralising the warm/cool split.** The clips form two genuine families —
  warm 10–79° (ten clips) and cool 184–201° (four) — rather than drifting. That
  is time of day, not error. 20 of 46 cuts jump more than 120° in hue and this
  was never flagged across seven review passes; at ~4.8 s average shot length
  the alternation reads as energy. The temperature nudges above are meant to
  soften the transition, not erase it.
- **Recovering City 11's highlights.** 28.3% of the frame is clipped, uniformly
  across the whole clip (27.5–29.0% in every 5 s window), and it is the sunset
  cloud rather than the city. These are graded exports — pixels at 255 have
  nothing behind them, so pulling highlights down yields flat grey, not detail.
  Only a re-export from the original would change that.

## Order of work

Do the two exposure fixes first (City Above, Hill Tower) — brightness steps are
the most visible mismatch and the cheapest to fix. Judge the result before
touching temperature, which is the taste-dependent part.

## Making this automatable later

The reliable route is a round trip: apply one correction to one clip in Final
Cut, `File ▸ Export XML`, and read the exact `<effect uid>` and parameter names
out of the result. After that the values in this table can be generated
directly and this becomes a one-line-per-clip project setting rather than
manual work — for this video and every future one.
