# Brand backgrounds

The moving ground behind a drawn beat, one per brand, named by
`Brand.backdrop` and loaded by `video_automation/core/backdrop.py`.

| file | brand | what it is |
|---|---|---|
| `tinnitus-galaxy.mp4` | tinnitushelp.me | supplied nebula starfield, ping-ponged, 12 s |
| `crypto-blackwater.mp4` | thecrypto.wiki | black water, ping-ponged from stock, 12 s |

## `tinnitus-aurora` is gone, and do not regenerate it

The tinnitus background used to be `tinnitus-aurora`, a *generated* mesh
gradient built from `backdrop.TINNITUS_AURORA`. It was replaced because the
user had already ruled that particular purple out in an earlier session and it
shipped anyway. **The asset is deleted, not just unreferenced** — a background
left in this folder is one somebody points a `Brand` at by name later, which is
exactly how it survived the first rejection. The spec that drew it is still in
`backdrop.py` as `_RETIRED_TINNITUS_AURORA`, renamed so it reads as a worked
example of `generate()`'s argument shape rather than as a live preset.

`tinnitus-violet` replaced it and lasted one review: a supplied mesh gradient
at **L89 / S201**, which needed dimming to 0.55 before peach type held against
it and still read as a flat magenta wall.

**`tinnitus-galaxy` is the current one** — a nebula starfield the user
supplied, at **L27 / S242** before any grading, which is already inside the
range the water and the old aurora sit in. It needs almost no dimming as a
result:

```python
bd.pingpong(src, bd.BACKGROUNDS / "tinnitus-galaxy.mp4",
            start=2.0, seconds=6.0, dim=0.92, saturation=0.80)
```

It is also the one background here that is *on brand by subject* rather than
only by palette: the app's own album is *Quiet Universe* and its artwork is
space, which is the same argument `longform/asmr.py` makes for its procedural
nebula.

**It breaks the "soft and low-frequency only" rule and gets away with it.**
Stars are high-frequency detail and the asset is 512px upscaled ~3.75x, so they
arrive as soft points rather than pinpricks. Checked on a real beat before
shipping: they read as texture, they do not fight type, and no star is sharp
enough to alias. Do not take this as licence for a background with *legible*
content — the test it passes is that the detail turns to mush attractively.

**Its wrap step is the largest in the loop (0.80 against a 0.087 median) and
that is fine here.** The rule that matters — the minimum step must not land on
a fold — passes: the minimum is 0.010 at frame 224, and the folds are at 0 and
149. The large steps are scattered GOP boundaries, not folds, and the whole
distribution is fifty times smaller than the water's (median 4.4) because a
nebula barely moves. **Read the shape of the distribution, not one number.**

## What replaced what

Both channels used to draw a ruled grid drifting behind every beat. It went
for two reasons: it stepped a **whole pixel at a time** on a layer moving
40 px/s, which is the judder the rest of this repo fixed years ago and which
showed worst on long beats; and it was the same graph paper in every video on
both channels, which is the templated sameness that gets a channel suppressed.

## They are square, and 512x512

One asset serves a 1920x1080 beat and a 1080x1920 one — scaled to fill and
centre-cropped. That only works because these are deliberately soft,
low-frequency images with no fine detail to lose. **A background with legible
content in it does not belong here**: the type is the subject and a backdrop
that pulls the eye is a bug.

## They loop, by construction

Generated ones move every blob on a **closed circular path** whose period
divides the loop, so the last frame equals the first. Measured on the aurora
before encoding: seam 0.0022 against an ordinary step range of 0.0007–0.0029,
so the join is an ordinary step.

Footage cannot do that, so it is made seamless the other way — forward, then
reversed. Measured on the water: seam 2.91 against a median ordinary step of
4.41, so the join is *less* change than a normal frame. **Only use ping-pong on
subjects with no arrow of time** — water, smoke, cloth, drifting particles.

## Adding another

```python
from video_automation.core import backdrop as bd

# generated
bd.generate(bd.BACKGROUNDS / "tinnitus-ember.mp4", MY_SPEC)

# from footage
bd.pingpong(src, bd.BACKGROUNDS / "crypto-smoke.mp4",
            start=2.0, seconds=6.0, dim=0.78, saturation=0.55)
```

Then point a `Brand` at it by name. **`dim` multiplies** — ffmpeg's
`eq=brightness` adds a constant, and dimming already-dark footage that way
returned pure black the first time (measured at mean luma 0.0).

Keep new backgrounds in the same luma range as these two: the galaxy runs a
mean of ~27, the water ~23. Much brighter and white or peach type stops holding
against it — which is not a hypothetical, it is exactly what the supplied
violet source did at L89 before it was dimmed.

**Check a new background by drawing a real beat on it, not by reading its
mean.** `backdrop.get()` caches by name, so rendering three variants under one
filename silently compares the first one against itself three times.
