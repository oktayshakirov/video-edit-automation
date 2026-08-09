# Approved stages

One row per edit signed off. Long-form metrics come straight from the `build`
output; short-form rows record the parameters the render was approved at, since
those are what reproduce it.

Return to any stage with `git checkout <tag>`.

## Tinnitus Help — shorts

| video | format | runtime | voice | notes |
|---|---|---|---|---|
| `tinnitus-breathe-60` | ASMR / sound therapy | 60.93s | `luna-calm` (new, still a candidate) | Approved as a first cut. First build of the format — nothing past the voices existed before it. Bed layers both source tracks because measurement said one is not enough: SpaceshipAmbience puts 86.8% of its energy under 200Hz and 0.1% above 4kHz, NebulaPulse carries the mids. Ducking is a sidechain at `threshold=0.03:ratio=8` over a `-23 LUFS` bed; at `-20` the voice had only 3 dB of headroom and was not intelligible. Picture is a procedural nebula in the app's own palette with a paced-breathing ring, 4s in / 6s out, three cycles. **The drift must be subpixel** — the first cut used an integer crop, moved ~25px/s, and the user called it laggy; `warpAffine` fixed it and a frame-difference check now shows no two consecutive frames identical. Angle is partial masking, from the brown-noise-vs-white-noise post. No lead-in silence and no end-card promo, both the user's call. Watermark is a mascot + `TinnitusHelp.me` lockup at (58, 292), full opacity, levitating 9px on a 5.5s sine (subpixel, or it stutters against a background that does not). Three placements before it landed: flush top-left corner sits under TikTok's LIVE button and Instagram's camera, dead centre read as part of the piece, inset upper-left is a watermark. Safe box recorded as `SAFE_TOP=230` / `SAFE_BOTTOM=1440` and `render_visual` now raises rather than shipping outside it. Headphones emoji set inline after "headphones on." via a second pass over the caption PNG — Apple Color Emoji only loads at its strike sizes, so it renders at 160 and scales down. |

## Shorts

| video | clip | runtime | voice | text | notes |
|---|---|---|---|---|---|
| Cingene — "cold water" (reveal format) | Sunset Sea 2, `crop=838:1490:1891:384` (zoom 1.45), start 15.0s | 14.23s | `leo`, aligned sentences, `gap=[0.65, 1.9, 0.65]` | Futura Medium 44px, stroke 4, `y_frac=0.50`, `tail=1.2`, punchline `COLD` at 88px, kicker shown on screen | Three approved changes came out of this one. **No fade to black** anywhere in the shorts pipeline — a looping short should end on picture, not on an announcement that it is over. **`tail` 2.2 → 1.2** so the loop comes back faster. **`font_size` may now be a callable**, which sets the turn word larger than the body; `COLD` at 88px was chosen over the same word at 44px. The kicker is a normal caption here rather than the empty-caption treatment, at the user's request. `pick_crop` wanted x=2808 — the dense tree on the right outscored the sun — so the box is manual again. Text centred at 0.50 after 0.64 was rejected as "lower half". |
| Cingene — "plant a tree" (reveal format) | Forest Coast Reveal 1, `crop=1215:2160:1512:0` (zoom 1.0), start 1.0s | 16.32s | `leo`, aligned sentences, `gap=[0.65, 1.9, 0.65]` | Futura Medium 44px, stroke 4, `y_frac=0.48`, `tail=2.2`, kicker is an empty caption | First short in the reveal format: opener, metaphor, then "this is not about trees btw" spoken but never shown. One continuous clip — the camera tilts off the canopy to open sea by itself, so the reveal lands with no tree in frame; a three-clip version was cutting to manufacture what this clip already did. 0.18s of headroom against the 17.5s source, so ffprobe mattered. Background music added by hand afterwards. |
| Cingene — "self-care" | Sunset Sea 5, `crop=838:1490:1632:624` (zoom 1.45), start 8.0s | 10.55s | `leo`, aligned sentences | Futura Medium 44px, stroke 4, `y_frac=0.64`, `gap=0.65`, `tail=2.2` | First short in `leo`. Approved as the plain-comma variant of a three-way punctuation test — em dashes and ellipses were measurably negligible and lost by ear. A `hover` clip, so framing does not drift and one sampled frame sets `y_frac` for the whole run. Quote is Katie Reed's; the "i read a quote that said" opener carries the attribution. |
| City 1 — "ordinary tuesday" | City 1, `crop=1215:2160:0:0`, start 2.0s | 10.91s | `am_onyx` 0.60 + `am_puck` 0.40, melancholic, aligned sentences | Futura Medium 44px, stroke 4, `y_frac=0.34`, `gap=0.65`, `tail=2.2` | First approved narrated short. Voice is a blend — straight `am_onyx` is graded D on minutes of data; the blend sounded more human across ten candidates. Crop is manual: `pick_crop` chose rooftops at x=1776 and left the sun out. That voice was retired when `leo` was approved; the recipe survives as the `melancholic` chain. |

## Nessebar

| tag | cuts | mean shot | coverage | effects | notes |
|---|---|---|---|---|---|
| `nessebar-v6` **shipped** | 31 | 7.74s | 82% | 0 sped up, 1 escalate, 5 reversed, 3 SFX | **The version to use.** Picture is byte-identical to v5; what changed is the asset uids, without which Final Cut refuses the whole document. Tag v5 alone does not import. The intro-burst variant was built and reviewed at this point and set aside — kept as `nessebar-burst` for testing on a future video, not a rejection. |
| `nessebar-v5` | 31 | 7.74s | 82% | 0 sped up, 1 escalate, 5 reversed, 3 SFX | Title re-captured after a hand fix — the authored version rendered solid black for two reasons the DTD cannot express: **strokeWidth must be negative** for an outside stroke (positive strokes inward and eats the fill), and the **`MotionSimpleValues` param block carrying the face fill must be present**. Attribute *names* are DTD-declared and safe to author; these values are not. `SOUND_EFFECTS` carries hand-placed audio through rebuilds — three seagull placements recorded, since the build overwrites the FCPXML wholesale and anything added by hand in FCP would otherwise be lost. Also strips `<adjust-colorConform>` (an FCPXML 1.11 element FCP adds to everything, which fails the 1.10 DTD) and narrows the connected-clip sync check, which was flagging correctly-placed SFX. |
| `nessebar-v4` | 31 | 7.74s | 82% | 0 sped up, 1 escalate, 5 reversed | Title styled — white, dark outline, widened kerning, via `LOCATION_TITLE_STYLE`. Every key is a declared FCPXML text-style attribute per the 1.10 DTD, so this is ordinary authoring, not the guess-a-uid trap; only strokeWidth's sign convention is unverified. Ends on Coast Above 2 running out to the last frame of its source (39.8→49.4s of 49.9s), closing Coast 2 dropped. Coast Houses Above 2 off 2x at 0:57 — no constant speed-ups left in the video. The 2:27 escalate re-fitted itself to 100%→1600% to fund the longer ending, which is `owed_after` working as intended. |
| `nessebar-v3` | 32 | 7.50s | 84% | 1 sped up, 1 escalate, 5 reversed | Title text beside the pin, captured from a user FCP export and committed to `assets/fcpxml/location-title-overlay.xml` — the Basic Title uid and its three `param key` paths are FCP-internal, same class as the keyer. Coast Above 2 doubled to 12.8s at 0:38 (Coast Above 1 moved to 3:37 to fund it). Coast 1 plays straight at 100% with its first 2s cut, no ramp. Coast Houses Above 2 un-reversed via `CLIP_REVERSE_OVERRIDE` — AUTO_REVERSE had it driving traffic backwards. **Fixed the escalate budget double-count**: `build_locked` charged a clip for every other slot including ones already consumed, so lengthening an earlier shot silently starved a later ramp. The 2:27 escalate now reaches its full 100%→2000%. |
| `nessebar-v2` | 34 | 7.06s | 86% | 1 sped up, 2 escalates, 8 reversed | Locked. **Escalate body speeds are now whole multiples only** — 160% stutters because 1.6 source frames per timeline frame forces an uneven repeat/drop cycle; confirmed on Coast 1, smooth at 100% and 200%, laggy at 160%. `fit_escalate` stepped 0.1 at a time hunting the fastest fundable profile, which is how 160%/150% got in. Both ramps now run a 100% body: Coast 1 at 1:10 → 1000%, Coast Above 2 at 2:27 → 2000%. Also: location pin overlay at 1.5s; `CLIP_SKIP_RANGES` excludes Coast Above 3's 6.7–9.9s off-angle rotation; Coast 1 reduced to a single ramped shot; first minute rebuilt as a showcase (8 distinct clips, all three Coast Above at 6.4s each) because it is cut for shorts; Coast 4 pulled to 1:04, Coast 3 pushed to 2:56. Title text next to the pin still outstanding — needs a generator UID captured from a real FCP export. |
| `nessebar-v1` | 38 | 6.32s | 83% | 3 sped up, 9 reversed, 0 repeated ranges | First edit on a correctly-detected grid. **librosa reported 152.11 BPM for a 75.00 BPM track**, and the least-squares fit made that look clean — off-beat onsets measured *stronger* than on-beat. Tempo is now found by direct (period, phase) search scored on onset energy: wrong grid scores 0.008, right grid 2.296; downbeat confidence 0.08 → 0.53. Track looped once (hands off 2:08.1, re-enters 0:38.5, 6.4s crossfade, both phrase lines, energy 0.93 vs 0.90) to carry a 2:36 song over a 4:00 picture. Approved on cuts and on the loop seam. |

### History

- **v0** — built on the 152 BPM misread: 53 cuts, mean 2.94s, 63% coverage, cuts
  landing on a grid unrelated to the music. Superseded, never tagged.

## Plovdiv

| tag | cuts | mean shot | coverage | effects | notes |
|---|---|---|---|---|---|
| `plovdiv-v7` | 47 | 4.81s | 74% | 12 sped up, 2 escalates, 4 reversed | City 4 dropped from 2x to 100% (reverse kept) — it read too fast over the city. Order byte-identical to v6. |
| `plovdiv-v6` | 47 | 4.81s | 81% | 16 sped up, 2 escalates, 4 reversed | Locked timeline — opening restored to v4's order (City 1 first). Hill Tower's overexposed head skipped, cascading its remaining uses forward. Second escalate before 1:00, fitted to 160%→403% (footage-limited). |
| `plovdiv-v5` | 47 | 4.81s | 81% | 16 sped up, 1 escalate, 4 reversed | Phrase-snapped sections: 2:11 and 2:21 now on the beat. Pinned City 2 @0:32.83 and City 7 @0:37.87. Picture and music fade together 222.03→226.03s. Opener drifted to City 5 as a side effect — caught and fixed in v6. |
| `plovdiv-v4` | 49 | 4.61s | 83% | 14 sped up, 1 escalate, 5 reversed | Escalate on Hills Monument at 0:10–0:20: 200% body, 2000% final second. Order matches v3 through 2:28. |
| `plovdiv-v3` | 49 | 4.61s | 80% | 15 sped up, 2 punch ramps, 5 reversed | Opening order approved. Speed-up only, no slow motion. Zero repeated source ranges. |

### History

- **v1** — first working timeline. 62 cuts, mean 3.64s. Pacing liked; a
  60-second stretch of identical 2.50s cuts was not.
- **v2** — phrase accents broke up the metronomic run; reuse penalty changed
  from counting uses to decaying with recency, which stopped the engine
  degenerating into round-robin and putting hovers on the drop.
- **v3** — slow motion removed entirely after review (it read as a mistake on
  this footage); retiming became speed-up only. Punch ramps into peaks. Auto
  reverse for clips travelling the same direction. Coverage 59% → 80%.
- **v4** — the 1.0x-start punch ramp replaced by the escalate: 200% throughout,
  2000% across the last second, launching into the next clip. Placed explicitly
  via `ESCALATE_AT_BARS` rather than won by scoring, because a scored escalate
  took slots from other clips and reshuffled the running order.
- **v5** — `SNAP_SECTIONS_TO_PHRASE` turned on, fixing 2:11 and 2:21 at the cost
  of re-laying the slot grid (37 of 47 positions moved from v4). Added
  `PIN_CLIPS` / `PIN_SLOT_BARS` for hand-placing a clip in a slot, and a picture
  fade to black under the closing music fade. **Regression**: the opener shifted
  from City 1 to City 5 as an uncalled-out side effect of the re-lay.
- **v6** — the running order is now **locked** (`projects/plovdiv.lock.toml`):
  `build` replays the approved slot grid and clip assignment verbatim, so
  tuning elsewhere can no longer reshuffle it. The v5 opener regression is
  fixed — restored to v4's City 1. Hill Tower's overexposed first segment is
  skipped via `CLIP_HEAD_SKIP`, cascading each remaining use forward by one
  segment; the freed slot goes to unused footage. A second escalate added
  before the 1:00 cut, but the ideal 200%→2000% profile doesn't fit — City 11
  owes 22.5s to its later slots in the locked order, so the escalate fits
  itself down to whatever speed the spare footage can fund (160%→403% here)
  rather than borrowing from those slots and moving the timeline again.

- **v7** — City 4's four instances dropped from 2x to 100%, reverse retained.
  First change made purely by editing the lock file; the running order came out
  byte-identical, which is what the lock exists to guarantee.

### Colour notes (measured, not yet acted on)

The 15 clips split into two colour families rather than drifting: warm 10-79°
(ten clips) and cool 184-201° (City 11, 4, 3, 2), with City Above alone at 346°.
**20 of 46 cuts jump more than 120° in hue** and this was never flagged during
review — on a ~4.8s average shot length the warm/cool alternation reads as
energy, not error. Treated as taste, not a fault.

More visible than hue, and worth addressing first:

- **Brightness**: City Above (0.41) and Hill Tower (0.43) sit well under the
  0.56-0.70 cluster — roughly a 1.5-stop step at some cuts.
- **Saturation**: Hill Tower (0.59) is ~3x City 1 (0.18) and City 11 (0.19),
  so it reads as the most processed shot whenever it appears.
- **City 11's 28.3% blown highlights are NOT recoverable.** The clipping is the
  sunset cloud, uniform across the whole clip (27.5-29.0% in every 5s window),
  and these are graded exports — pixels at 255 have nothing behind them. What
  *is* fixable there is haze: City 11 measures 186 on detail density, the lowest
  of all 15 and ~10x below the sharpest.

### Known open items

- **3:22 lands 1.07s early.** The accent sits at bar 80.42 — roughly beat 3 —
  and the engine cuts only on bar lines, so 3:20.93 and 3:23.44 are the only
  reachable points. Needs slot lengths expressed in beats.
- **The 1:00 escalate is capped at 403%, not 2000%**, because City 11 is
  committed to three later slots in the locked order. Getting the full ramp
  there means freeing one of those slots (moves the timeline) or choosing a
  different, less-committed clip for that launch.
- **Slice selection is sequential**, so the back half of the longest takes is
  reached only through reuse. Spreading each clip's slices across its full
  length is the obvious next improvement.
- **Editing the timeline now means editing `plovdiv.lock.toml` directly**
  (swap a `clip` value, adjust `bars`, or set `rate`) rather than retuning
  `config.py` weights — that's the point of the lock, but worth remembering so
  a future request for "more variety" or "less repetition" isn't chased through
  scoring parameters that no longer apply to this project.
