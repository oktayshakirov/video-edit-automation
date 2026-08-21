# Cingene — colour consistency pass

Hand-applied in Final Cut. **FCPXML cannot carry this**: version 1.10 has no
colour element at all — the whole `adjust-*` set covers crop, transform, blend,
stabilisation and volume, nothing else. Colour would have to go through
`<filter-video>` referencing an `<effect uid="...">`, where the UID and parameter
names are FCP-internal identifiers, the same class of guess that caused two
failed imports earlier in this project. So these are dial-in values, not
generated XML.

Everything below is **measured off the cached proxies in CIELAB**, twelve frames
sampled across each clip — not read off the index summary and not judged by eye.
`L` is lightness 0-100, `a*` is green(−)/red(+), `b*` is blue(−)/yellow(+).

The twelve golden-hour clips form a tight cluster. Those are the target:

| | L1 (black) | L5 | L50 (mid) | L95 | a* | b* | hue | chroma |
|---|---|---|---|---|---|---|---|---|
| **sunset cluster median** | 5.7 | 12.4 | 39.6 | 89.8 | +7.4 | +9.4 | 51.9° | 12.0 |

## The two before golden hour

Both are forest shots taken before the light turned, and both miss the cluster
in the same direction — too little red, too little yellow — but for different
reasons and by very different amounts.

### Forest Coast 1 — cut from the film

**This clip is no longer in the edit** (`CLIP_MAX_USES = 0`). Kept here as the
record of why: it is the one clip in the batch that grading could not rescue,
because its highlights are clipped rather than merely bright — L95 99.6, L99
100.0 — and that detail is gone, not recoverable. Everything below is what a
correction would have had to do.

Measured: L1 4.7, L50 **72.2**, L95 **99.6**, a* **−2.0**, b* +2.7, chroma 3.4.

| do this | amount | why |
|---|---|---|
| **exposure** | **−0.87 stops** | L50 is 72.2 against a cluster median of 39.6. It is not slightly bright, it is nearly a stop hot, and that alone makes every cut into it read as a flash |
| **highlight recovery** | as far as it goes | L95 99.6 and L99 100.0 — the top end is **clipped, not just bright**. Recovery will pull back what is left but some of this is gone and cannot be graded back |
| **warm the balance** | **a* +9.4, b* +6.7** | a* is **negative** — the only clip in the batch on the green side of neutral. In FCP: colour temperature well up, then a small push toward magenta to kill the remaining green |
| **saturation** | **chroma 3.4 → 12.0, roughly +250%** | it is almost monochrome next to the sunset material. This is the largest single delta in the batch |
| **black point** | leave it | L1 4.7 against 5.7 is already right |

Hue lands at **126°** — green — against a 52° cluster. That is the number that
makes it look like a different location rather than a different shot. Fix the
exposure first: at −0.87 stops the colour work gets much easier to judge.

### Forest Coast 2 — lifted blacks, mild cast

Measured: L1 **9.8**, L5 **15.3**, L50 45.9, L95 78.8, a* +1.4, b* +7.1, chroma 7.3.

| do this | amount | why |
|---|---|---|
| **black point down** | **−4.1 L** (L1 9.8 → 5.7) | this is the "correct black" fix. Nothing in the frame reaches true black — the shot sits on a raised floor and reads hazy and flat beside the sunset clips, which all bottom out near 5 |
| **warm the balance** | **a* +6.0, b* +2.3** | hue 79° against 52°. Much milder than Forest Coast 1 and mostly a red deficit rather than a green cast |
| **saturation** | **chroma 7.3 → 12.0, about +65%** | follows once the black point is set; pulling the floor down does part of this on its own |
| **exposure** | **−0.21 stops** | inside a quarter stop of the median. Do it last, or not at all |

Do the black point before the colour. Lifting the floor is what is flattening
the chroma, so the saturation number above may look like too much until the
blacks are down, and about right afterwards.

## Everything else

The twelve sunset clips span L50 20.8 to 54.9 and a* +2.8 to +10.4. That spread
is real evening light changing across the shoot, not a grading fault, and
flattening it would cost the film its arc. Two worth a glance only if something
looks off in context:

- **Sunset Sea 7** — a* +2.8, b* +6.0, hue 65°, and **L50 20.8, the darkest in
  the batch**. It opens the film and holds for 12.4s, so it sets the reference.
  It is cool because it faces away from the sun, which is the shot. If the first
  cut jumps, lift it a little rather than warming it.
- **Sunset Sea 3** — L1 **15.7**, the most lifted floor of any clip. Same fix as
  Forest Coast 2 if it reads hazy, but it is only on screen twice for 2.9s.

Detail is not worth correcting on this batch: the high scorers have trees and
buildings in frame, the low ones are open water and sky. That is subject, not
sharpening.
