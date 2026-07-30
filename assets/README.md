# Assets

Reusable overlay elements, and the FCPXML fragments needed to place them.

These *are* committed — they are small, needed on every machine, and
re-deriving them by hand is exactly the step that gets lost between videos.

> The pin animation is third-party stock (its source pack opens with a
> "pixel edge" branding card) and this repository is public. Committing it was
> a deliberate call; check it against the pack's licence if the repo ever
> matters commercially.

## Location pin

| file | what |
|---|---|
| `location-pin-source.mp4` | the full source pack — 1920×1080, 24 fps, 54.8 s, nine ~5 s pin animations in different colours behind a branding card |
| `pins/location-pin-red.mp4` | the red pin alone, 5.04 s, standalone |
| `fcpxml/location-pin-overlay.xml` | the exact keyer + placement, captured from a real Final Cut export |

**The red pin is source 9.833 – 14.867 s** of the pack. Worth stating plainly
because it is not guessable: measured by hue it reads as ~345°, which
classifies as pink/magenta, and the block that *measures* as red (14.88 s) is
visibly orange. The value above came from a real FCPXML export, not analysis.

```bash
ffmpeg -ss 9.8333 -to 14.8667 -i assets/location-pin-source.mp4 -an \
  -c:v libx264 -crf 12 -preset slow -pix_fmt yuv420p \
  assets/pins/location-pin-red.mp4
```

CRF 12 is deliberate: chroma keying degrades badly through a second lossy pass
and the source is already 4:2:0 at a low bitrate.

## How it is placed

From the Final Cut export, verbatim:

```xml
<asset-clip ref="r4" lane="1" offset="0s" name="location"
            start="29500/3000s" duration="15100/3000s" format="r5" tcFormat="NDF">
    <conform-rate scaleEnabled="0" srcFrameRate="24"/>
    <adjust-transform position="-81.524 42.1759" scale="0.06 0.06"/>
    <filter-video ref="r6" name="Green Screen Keyer"> … </filter-video>
</asset-clip>
```

- **lane 1**, offset `0s` — sits over the first spine clip, at the very start.
- `start="29500/3000s"` = 9.833 s into the source; duration 5.033 s.
- **scale 0.06** — six percent. A 1920×1080 element shrunk into a corner badge.
- position `-81.524 42.1759` — left of centre, above.
- `conform-rate srcFrameRate="24"` handles 24 fps into the 30 fps timeline.

## The keyer cannot be authored by hand

`uid="FxPlug:41122549-B8A6-470E-94DA-211294D20B62"` plus two base64 payloads
(`effectConfig`, `effectData`) that encode the keyer's internal state. Those are
FCP-internal — there is no way to write them from a specification, which is why
`fcpxml/location-pin-overlay.xml` stores the whole thing captured rather than
generated. Reuse it as-is: declare the `<effect>` in `<resources>`, nest the
`<asset-clip>` in the spine clip it belongs over.

## Still to capture

The export contained **no colour corrections** on the drone clips — only
`adjust-colorConform` (automatic), the pin's transform, the music `adjust-volume`
and the fade's `adjust-blend`. So the colour pass in `projects/plovdiv-colour.md`
is still unapplied, and the effect UID for Final Cut's colour tools is still
unknown. One clip with a colour correction, exported, would settle it the same
way this file settled the keyer.
