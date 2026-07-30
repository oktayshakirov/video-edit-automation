# Assets

Overlay elements reused across videos.

## The media files are deliberately NOT committed

`.gitignore` excludes `*.mp4`, and that is intentional here rather than
incidental: **this repository is public**, and the pin animation is licensed
third-party stock (it carries a "pixel edge" branding card at its head).
Publishing it would redistribute someone else's asset. The files stay local;
this README records what belongs here so another machine can be set up.

## Location pin

Source: `location.mp4` — 1920×1080, 24 fps, 54.8 s, a pack of nine ~5-second
pin animations in different colours, preceded by a branding card.

| file | source range | colour | notes |
|---|---|---|---|
| `pins/location-pin-red.mp4` | 24.88 – 29.80 s | **red** | the one in use |
| `pins/location-pin-orange.mp4` | 14.88 – 19.80 s | orange | same animation, warmer pin |

Both are 4.96 s, extracted at CRF 12 (visually lossless) so the green screen
survives a second encode — chroma keying suffers badly from repeated
compression, and the source is already 4:2:0 at a low bitrate.

The pin **slides left to right** across the frame over its ~5 s, so the in-point
chosen determines where it sits horizontally.

### Setting this up on another machine

Put the original at `~/Movies/location.mp4`, then:

```bash
ffmpeg -ss 24.88 -to 29.80 -i ~/Movies/location.mp4 -an \
  -c:v libx264 -crf 12 -preset slow -pix_fmt yuv420p \
  assets/pins/location-pin-red.mp4
```

### Points to watch when placing it

- **24 fps into a 30 fps timeline.** Final Cut conforms it, but that means
  duplicated frames. It is a graphic on a static background, so this is
  invisible in practice — worth knowing rather than fixing.
- **Trim past 6.67 s of the original.** Everything before that is the stock
  provider's branding card.
- Keying is not something the generated FCPXML can carry (see below), so the
  keyer, position and scale are applied by hand for now.

## Automating this

FCPXML 1.10 has no colour or keying element — the whole `adjust-*` set is crop,
transform, blend, stabilisation and volume. A keyer has to go through
`<filter-video>` referencing an `<effect uid="…">`, where the UID is an
FCP-internal identifier. Guessing one is what caused two failed imports earlier
in this project, so it is not guessed.

**The fix is a round trip.** Export the finished timeline as FCPXML
(`File ▸ Export XML…`) and the exact structure can be read out of it: the
keyer's effect UID and parameters, the pin's lane, offset, duration, scale and
position, and any colour corrections applied to the drone clips. After that all
of it can be generated automatically, for this video and every future one.
