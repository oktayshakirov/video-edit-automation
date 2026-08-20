# Cingene — colour consistency pass

Hand-applied in Final Cut. **FCPXML cannot carry this**: version 1.10 has no
colour element at all — the whole `adjust-*` set covers crop, transform, blend,
stabilisation and volume, nothing else. Colour would have to go through
`<filter-video>` referencing an `<effect uid="...">`, where the UID and parameter
names are FCP-internal identifiers, the same class of guess that caused two
failed imports earlier in this project. So these are dial-in values, not
generated XML.

Targets are the library medians: **brightness 0.509**, **saturation 0.343**,
**detail 100**. Deltas come from the measured index, not from eye.

The exposure spread is **0.80 stops** (0.376 to 0.653) — narrower than Nessebar's
1.26, and the reason the batch already mostly reads as one evening. The problems
here are not exposure. They are **two clips whose hue sits outside the golden
hour entirely**, and they matter more than any brightness step in the list.

## The two that do not belong

Twelve of the fourteen clips sit in a warm cluster between −19 and +45 degrees,
median **22.2 degrees**. Two do not.

| clip | measured | correction | why |
|---|---|---|---|
| **Forest Coast 1** | hue 111.5 (**+89 from the cluster**), sat 0.185 (**−46%**), 6.9% blown, 0.630 bright | **warm the white balance hard** — temp up until the greens read amber, not lime. Then **saturation +45%**, **highlight recovery**, **exposure −0.31 stops** | The only clip shot before golden hour, and it is the widest outlier in the batch on hue, on saturation and on blown highlights simultaneously. Green foliage under neutral daylight next to an orange sea reads as a different location, not a different shot. Also the brightest but one, so it steps up as well as sideways. Now used 4x (was 7x) |
| **Sunset Sea 7** | hue 164.6 (**+142 from the cluster**), sat 0.305 (−11%), 0.376 bright (**darkest**) | **exposure +0.44 stops**, then **warm the balance** toward the cluster. Judge the hue by eye rather than by the number | It is teal because it is looking at open water away from the sun, which is legitimate — this is not a grading error the way Forest Coast 1 is. But it **opens the film** and holds for 17.5s before anything cuts, so it sets the viewer's idea of what this evening looks like. Bring it far enough toward the cluster that the first cut is not a jump. Do not neutralise it completely; the cool water is the point of the shot |

Correct these two before touching anything below. If the film reads as one
evening after them, the rest of this document is optional.

## Exposure — worth a look after the above

Everything here is inside a third of a stop of the median, which is at or below
the threshold where a cut reads as a step. Listed for completeness.

| clip | measured | correction |
|---|---|---|
| **Sunset Sea 1** | 0.653 bright, 3.9% blown | **−0.36 stops**, slight highlight recovery |
| **Sunset Sea Houses** | 0.591 bright, 3.1% blown | **−0.21 stops**, slight highlight recovery |
| **Sunset Sea 3** | 0.584 bright | **−0.20 stops** |
| **Forest Coast Reveal 2** | 0.409 bright | **+0.32 stops** — it is the closer, so it wants to sit with its neighbours |

Sunset Sea 1 and Sunset Sea Houses are the two most-used clips in the top half
of the exposure range and both clip highlights above 3%. If you only do one
exposure fix, do those two together.

## Saturation

| clip | measured | correction |
|---|---|---|
| **Forest Coast 1** | 0.185 (−46%) | **+45%** — covered above, listed again because it is the largest single delta in the batch |
| **Sunset Sea 6** | 0.240 (−30%) | **+30%** |
| **Sunset Sea Houses** | 0.248 (−28%) | **+28%** |
| **Forest Coast Reveal 1** | 0.426 (+24%) | **−15%** — it is the ramped transition at 1:44 and the most saturated clip in the film; pulling it back keeps the launch from reading as a colour change too |

## Detail

**Forest Coast 2** (649) and **Sunset Sea 2** (1610) measure far above the
median of 100, and **Forest Coast Reveal 2** (56) and **Sunset Sea 7** (66) far
below. This is subject, not sharpening: the two high scorers have trees and
buildings in frame, the two low ones are open water and sky. Nothing to correct.
Leave detail alone on this batch.
