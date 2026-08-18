# Brand backgrounds

The moving ground behind a drawn beat, one per brand, named by
`Brand.backdrop` and loaded by `video_automation/core/backdrop.py`.

| file | brand | what it is |
|---|---|---|
| `tinnitus-aurora.mp4` | tinnitushelp.me | generated purple mesh gradient, 12 s |
| `crypto-blackwater.mp4` | thecrypto.wiki | black water, ping-ponged from stock, 12 s |

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

Keep new backgrounds in the same luma range as these two: the aurora runs a
mean of ~36, the water ~23. Much brighter and white or gold type stops holding
against it.
