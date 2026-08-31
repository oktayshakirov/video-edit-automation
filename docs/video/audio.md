# Music, beds and sound effects

Everything under the voice. Sound-therapy beds are a different product - see
`projects/tinnitus.md`.

## Music — a small shared library, or generated

`assets/brand/music/` holds real tracks picked by ear, and **it serves both
sites**: the tracks are brand-neutral and the user's call is one library, not
one per channel. `music.track("night-drift")` is what the crypto-exchanges cut
uses. Add another with `music.prepare_track(src, name)`, which trims both ends
and stores WAV — **an mp3 decodes with encoder delay bolted to the front and
`render_bed` loops the track, so untrimmed silence becomes a hole in the bed
once per loop**, twenty-nine times in a four minute video.

Check the source's licence before anything monetised, and check the loop by
ear: trimming fixes silence, not a track that was never written to loop.

The generated presets below remain the licence-safe default and the right
choice when nobody has picked a track.

## The generated beds

`core/music.py` synthesizes the bed. **`pulse`** is the crypto default —
112 BPM, plucked sixteenths, soft kick. Also `momentum` (100 BPM, calmer),
`bright` (warmer), and the pad-only `tension` / `calm`. Pass a `Path`
instead to use a real track.

- **Pads alone read as creepy.** The first bed was three chords and a filter
  and the user's word for it was "creepy mysterious". What makes a bed feel
  dynamic is *note events on a grid* — an arpeggio and a kick give the piece
  a tempo, and tempo is what the ear reads as momentum rather than
  atmosphere. Brightness alone does not fix it.
- **`air` is 0 on every preset with a rhythm section.** That layer is
  broadband high-passed noise; under a bare pad it reads as space, with
  plucks present it is plainly audible hiss. Measured at 0.6% of energy
  above 4 kHz before, 0.03% after.

This is `sfx.py`'s argument at three-minute scale. A YouTube Audio Library track
is cleared for YouTube and **not** for a TikTok repost, which this repo does
routinely; its tracks are usually shorter than the video so `render_bed` has to
loop them, and a loop is only invisible if the track was written to loop. A
generated bed has no licence edge on any platform, is rendered to the exact
length, and — the part that matters for a channel — is the *same* bed every
time, which is a brand rather than a different stock track each video.

- **Voice ~7 dB over the bed** under speech, bed at full strength through card
  silence. Measured on the pilot. The sidechain numbers come from the tinnitus
  build and did not need changing.
- **The register is the whole thing.** First pass voiced the pad one octave
  above a 55 Hz root, which put 96% of the bed's energy below 200 Hz — a rumble,
  not music. Two octaves up, with `1/k` partials instead of `1/k²`, puts ~22% in
  the 200 Hz–1 kHz band where a pad belongs.
- **Nobody has listened to these on speakers yet.** The measurements say the mix
  is right; they cannot say it sounds good.

## Music: the generated presets are retired

**`bright`, `pulse` and `tension` are not to be used on this channel again.**
The myths cut shipped with `bright` and the user's note was that it is "the
one which we decided to not use anymore, delete it and never use it again".
Every video, long and short, uses `music.track("night-drift")` — the prepared
track that lives in `assets/brand/music/` and is shared with thecrypto.wiki.

The presets stay in `core/music.py` because they are the safer licence story
for anything new and `render_long` still accepts a preset name; they are just
not the pick here. If a second real track is ever added, add it with
`music.prepare_track`, which trims both ends — untrimmed encoder delay
becomes an audible hole in the bed once per loop.

## Music can be a real track, and it must be stored trimmed

`assets/brand/music/`, via `music.track(name)`. `night-drift` is the user's
pick over the generated `bright` preset.

**`render_bed` loops a short track to fill the video, so silence on either end
becomes a hole in the bed once per loop.** An mp3 decodes with encoder delay
bolted to the front: this one arrived with **54.4 ms** of digital silence
against an end running at full level — twenty-nine audible gaps across a four
minute video. `render_bed` has a `start=` offset that hides it, but then the
right offset is a number somebody has to remember per track.
`music.prepare_track` trims both ends once and stores WAV, so the asset is
correct by construction.

Generated presets remain the default and the safer licence choice. **Check a
new track's loop before using it** — trimming fixes silence, not a piece that
was never written to loop.

**Do not let stock footage become wallpaper.** The first sleep cut used the
calm-water stock four times with nothing on it and the user called it out: the
script is about bedrooms, so unlabelled water illustrates nothing. Two rules
came out of it. **Footage should be the subject of the line it sits under** —
rain on a window earned its place in the "what to play" section because rain is
one of the sounds the post recommends. And **if a clip is only atmosphere, it
needs a line on it**, which is the `Shot(clip=..., payload=("", "..."))`
treatment the format already has. The user's phrasing: use it less often, and
only with text over it.

**Music is `bright`**, not `pulse`. Warmer and less tense. This audience is
frequently here *because* sound is a problem; the bed should not be one.

## Sound effects

All synthesized, all in `core/sfx.py`, all cued from the shot list by
`build._cues` so picture and sound cannot drift.

| cue | where |
|---|---|
| `riser` | 0.75s before a chapter card — says a cut is coming |
| `impact` | on the card — the riser's full stop |
| `whoosh` | cutting *out* of a card, covering the return to content |
| `reveal` | an item arriving on any drawn beat |
| `cross` / `tick` | a checklist verdict landing |

`LEVELS` sets each against the narration peak, and one gain for all of them
cannot work: a transition has to be heard over the bed, an item tick has to sit
under a syllable, and those are a factor of four apart. **The set is
deliberately small** — a sound on every event is a cartoon. The `riser` is
subtle by design and has not been judged by ear.

## Sound

`core/sfx.py` **synthesizes** its effects rather than sourcing them. The drone
project's SFX are hand-placed clips living inside a Final Cut bundle, which a
headless render cannot depend on, and downloading a "free" UI click pulls in a
licence question over 200ms of audio. Two numpy functions cost nothing, are ours
to license, and are parameterised — `mark_cross` and `mark_tick` are the same
instrument at different pitches, which is why they read as one system.

- **The envelope is the whole character.** Instant attack, exponential decay,
  a noise transient on the front. A decay short enough that it never competes
  with a syllable is the difference between software and cartoon.
- **`gain` is against the narration's own peak**, not full scale. A fixed
  absolute level is inaudible under one voice profile and slapping over another;
  `0.22` is the working value. The mix ceilings rather than clips, because a
  mark landing on a stressed syllable will otherwise distort on exactly the beat
  meant to be satisfying.
- Cues come from the same `marks` list that drives the drawing, so picture and
  sound cannot drift apart.

**Watermark:** `public/images/logo.png`, upper-left at (58, 268), 300px wide,
full opacity, levitating 8px on a 6.5s sine. The asset already contains the
domain so nothing is added under it. Same safe box as the tinnitus shorts —
`SAFE_TOP=230`, `SAFE_BOTTOM=1440`, clear of `x>860` — and `render_shots` raises
rather than shipping outside it.

**It can roam:** `render_crypto_short(..., roam=True)` cuts the mark between
upper-left and lower-right every `logo_hold` seconds (13s by default). Off
unless asked for, so the shipped cuts are unchanged. A mark that moves is much
harder to crop out of a repost and defeats the corner blindness that makes a
static watermark worthless. It **cuts, never slides** — a lockup travelling
across frame is a second moving object competing with the picture — and keeps
levitating at each anchor. Every anchor is validated against all four safe
edges, not just the top. Full reasoning in `shorts.md`, where it was
specced.

## Shorts take a music bed, and it is not optional

**Every short gets `music.track("night-drift")` at `music_gain=0.85`, and this
is now the default in `render_crypto_short` itself** — the `music` parameter
defaults to a sentinel that resolves to the prepared track, and `music_gain`
defaults to `0.85`. A build that passes nothing gets the bed; pass `music=None`
to opt one specific short out, or a preset name / path to override. This covers
`render_tinnitus_short` too, which forwards straight through. Older shorts will
sound different if re-rendered — the same trade already accepted for the
backdrop and the karaoke captions.

`render_crypto_short` had taken `music`/`music_gain` for a long time and the
article shorts simply never passed them, while both short skills went on
recording it as "requested and not yet built" long after it was built — so the
default was moved into the function rather than left to each project file.

Gain sits slightly under the long form's: a short is watched on a phone speaker
with the voice carrying all of the information. It matters more here than in
long form - a short opens with no lead-in silence and is judged in its first
second, and a synthesised voice over silence sounds like a voice memo.

The generated presets are retired here too; see *Music: the generated presets
are retired* above.
