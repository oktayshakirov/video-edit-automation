# Brand music

Real tracks picked by ear, as an alternative to the generated presets in
`core/music.py`. Pass one to `render_long(music=...)` via `music.track(name)`.

| file | where it came from | length |
|---|---|---|
| `night-drift.wav` | Pixabay, `oosongoo-background-music-224633` | 7.68 s |

The generated presets are still the default and still the safer licence
choice — a generated bed is ours on every platform, and these are not. Check
the source's licence before a track goes on anything monetised or reposted.

## They are stored trimmed, and that is the point

`render_bed` loops a short track to fill the video, so **any silence on either
end becomes a hole in the bed, once per loop.** An mp3 decodes with encoder
delay bolted to the front: `night-drift` arrived with **54.4 ms of digital
silence** against an end running at full level, which over a 3:47 video is
twenty-nine audible gaps.

`render_bed` has a `start=` offset that would hide it, but then the correct
offset is a number somebody has to remember for every track. `prepare_track`
trims both ends once and stores WAV — lossless, so the stored asset decodes
sample-exact and re-encoding cannot reintroduce the delay.

Measured after trimming: loop-point discontinuity **0.00000** against a mean
absolute sample step of 0.00472, and across a real 30 s bed the seam's largest
step is 0.0227 against an ordinary maximum of 0.0997. The join is quieter than
the music.

## Adding another

```python
from video_automation.core import music
music.prepare_track(Path("~/Desktop/whatever.mp3").expanduser(), "name-it")
```

Then `render_long(music=music.track("name-it"))`. **Check the loop before
using it** — the trim fixes silence, not a track that was never written to
loop. A piece that ends on a resolving chord will still sound like it restarts.
