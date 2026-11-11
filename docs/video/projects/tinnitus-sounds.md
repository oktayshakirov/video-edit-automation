# Sound-therapy album tracks: used and unused

Every track on the tinnitushelp.me zen albums (`~/Coding/tinnitus-blog/content/zen/*.mdx`),
and which session video has already used it. **Check this before building a
session, and add a row the moment a dropped file goes into a build** - a track
used twice makes the channel's sessions sound like one video.

A track counts as used when it is the bed of a session (long form and its
Short together). Pick the next one from the unused rows.

## Used

| album | track | session (long form + Short) | built |
| --- | --- | --- | --- |
| White Noise Therapy | Spaceship Ambience | `masking-breathing-5min` + `masking-breathing-1min` (layered with Nebula Pulse) | before 2026-10 |
| White Noise Therapy | Nebula Pulse | `masking-breathing-5min` (layered); `nebula-pulse-478-breathing` (on its own) | 2026-10-22 |
| Jungle Stillness | Waterfall Birds | `jungle-waterfall-478-breathing` | 2026-10 |
| Jungle Stillness | Nature's Chorus | `forest-chorus-box-breathing` | 2026-10 |
| Jungle Stillness | Wild Echoes | `wild-echoes-478-breathing` (1 hour) | 2026-11 |
| Feathered Tunes | one track, name not recorded (supplied as `1.wav`) | `bird-chirps-55-breathing` | 2026-10-28 |
| Purring Melodies | one track, name not recorded (supplied as `1.wav`) | `cat-purr-comfort` | 2026-10 |
| Quiet Universe | Low Gravity | `low-gravity-box-breathing` (1 hour) | 2026-11-07 |
| Quiet Universe | Soft Orbit | `soft-orbit-6666-breathing` (1 hour) | 2026-11-08 |
| White Noise Therapy | Tranquil Zenith | `tranquil-zenith-21-breathing` (1 hour) | 2026-11-11 |

**Not album tracks** (no row above takes them off the list):
`478-breathing-white-noise` is generated white noise (`soundbed.Bed`);
`waterfall-478-breathing` (`waterfall-pads.mp3`) and `rain-masking`
(`Rain.mp3`) are recordings whose album was not noted at build. If either came
from Water Sound Therapy or Nature Inspired Sound Therapy, move that track up
here.

## Unused

| album | site page | tracks not yet used |
| --- | --- | --- |
| Quiet Universe | `/zen/quiet-universe` | Gentle Cosmos, Weightless Journey, Interstellar Calm, Zero Pressure |
| Jungle Stillness | `/zen/jungle-stillness` | Wildlife Whisper, Quiet Creatures, Moonlight Calm, Flowing Night |
| White Noise Therapy | `/zen/white-noise` | Cloudscape Serenity, Ethereal Resonance |
| Feathered Tunes | `/zen/bird-sounds` | four of Morning Songbirds, Tree Top Tunes, Wings of Calm, Chirps & Tweets, Sky Echoes (one is used, name unknown) |
| Purring Melodies | `/zen/cat-purr-sounds` | four of Deep Sleep Purr, Violin Purr Serenade, Dreamy Purrs, Gentle Night Purr, Purr Therapy (one is used, name unknown) |
| Fireside Harmony | `/zen/fire-sounds` | Soft Flames & Breezes, Flickering Quiet, Twilight Musicbox, Breezy Warmth - **whole album unused** |
| Background Blur | `/zen/evening-sounds` | Crackle Lo-fi, Ambient Fan, Cozy Lo-fi Shelter, Hearthside Hours, Deep Resonance - **whole album unused** |
| Morning Ritual Ambiance | `/zen/morning-sounds` | Peaceful Start, Refreshing Shower, Hair Dryer Breeze, The Breakfast Flame, Laundry Background, Drying Serenity - **whole album unused** |
| Water Sound Therapy | `/zen/water-sounds` | Zen Flow, Harmonious Waves, Serenity Stream, Dreamy Lagoon, Mystic Brook |
| Nature Inspired Sound Therapy | `/zen/nature-sounds` | Waterfall, River, Rain, Crickets, Crickets2 |
| Notched Sound Therapy | `/zen/notched-sounds` | Tranquilify 5000 Hz, Harmonics 6000 Hz, Resonance 7000 Hz, Harmonics 8000 Hz, Tranquilify 9000 Hz - **whole album unused** |

**Measure before you plan the copy.** A track's album description is not its
spectrum: Low Gravity and Soft Orbit are both sold as "for tinnitus masking"
and both measured as comfort beds (almost nothing above 1 kHz). Tranquil Zenith went the other way: sold as "pure,
perfectly balanced white noise", it measured as a hiss with 84-89% of its
energy at 4-8 kHz and ~53 short pings a minute near 5 kHz on top - a
masking bed, but not a pure one. Run
`band_energy` and the near-silent-window share on the file
(`projects/tinnitus.md`, "A comfort session is not a masking session").
