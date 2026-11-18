# Sound-therapy album tracks: used and unused

Every track on the tinnitushelp.me zen albums (`~/Coding/tinnitus-blog/content/zen/*.mdx`),
and which session video has already used it. **Check this before building a
session, and add a row the moment a dropped file goes into a build** - a track
used twice makes the channel's sessions sound like one video.

A track counts as used when it is the bed of a session (long form and its
Short together). Pick the next one from the unused rows.

## Fetching the next track (from 2026-11-18)

**A session build fetches its own bed from DistroKid; it does not wait for
the editor to drop a file.** The masters live at
`https://distrokid.com/mymusic/` (the editor's account, signed in in Chrome).
That list mixes the sound-therapy albums with the editor's music releases
(GTA FLU, Indica, Mask Off, Genesis and the rest) - **only the ten releases
in the table below are sound therapy.** Several are released under a
different name from the album page on the site, so go by this table, not by
the name.

1. **Pick the track here first**, from "Unused" below, before opening the
   browser: E25 and the session queue in `tinnitus.md` decide which kind of
   sound comes next (a named noise, a theme), and the measurement decides
   whether the copy can call it masking.
2. **Open the release** (Claude in Chrome; the uuid is in the table) and
   take the vault id for the track: each track row has a "Download" link to
   `https://distrokid.com/vault/download/?id=<id>`. Check the id sits in the
   row of the track you picked - the links carry no name.
3. **Navigate the tab to that vault URL.** Clicking the link through the
   extension did nothing on 2026-11-18; navigating to it downloads at once.
   Chrome saves to **`~/Desktop`** (not Downloads) as the track title without
   spaces (`CloudscapeSerenity.mp3`, a ten-minute 320k MP3, 48 kHz), which is
   where every session script reads its bed from. Close the tab after.
4. **Measure it** (`band_energy` per 30s window, the near-silent share,
   self-correlation, the first and last seconds for a fade) and write the
   numbers into the long form's docstring.
5. **Move the track to "Used" in the same commit as the build.**

| site album (`/zen/...`) | DistroKid release | albumuuid |
| --- | --- | --- |
| White Noise Therapy (`white-noise`) | **Infinite Horizons** | `4DEDA6DC-01F3-46F4-ABF73B43E89EF495` |
| Quiet Universe (`quiet-universe`) | Quiet Universe | `B56AE14E-DC30-4AB1-983FEFC3E4C04F3F` |
| Jungle Stillness (`jungle-stillness`) | Jungle Stillness | `E840920D-5BD2-4147-A98EBC39693CA449` |
| Fireside Harmony (`fire-sounds`) | **Fireside Comfort** | `EA1B53A5-195E-48D2-AD42BC41D7C0E8A5` |
| Purring Melodies (`cat-purr-sounds`) | **Purrfect Calm** | `19EDA37A-64A9-4277-81DDCE17CB04FED4` |
| Feathered Tunes (`bird-sounds`) | Feathered Tunes | `E077F302-6111-43E9-99EEC594A6F69738` |
| Water Sound Therapy (`water-sounds`) | **Aqua Rhapsody** | `570842A9-87B4-4A31-ACF4ABF84A9B466A` |
| Nature Inspired Sound Therapy (`nature-sounds`) | **Earth's Lullaby** | `B27DAF52-E86F-4F52-BB776B447AA3A6C2` |
| Notched Sound Therapy (`notched-sounds`) | **Pitch Perfection** | `A43F3236-F018-4C6C-AD54E46ADCE0F6CE` |
| Morning Ritual Ambiance (`morning-sounds`) | **Morning Unfolding** | `9C3F7C3B-45AE-4F4B-BE56AF67DBC51332` |
| Background Blur (`evening-sounds`) | Background Blur | `9BF3AA67-70C9-4F16-A0517B8E9EF9D128` |

Release URL: `https://distrokid.com/dashboard/album/?albumuuid=<uuid>`.
Track lists match the site except **Background Blur**, whose DistroKid tracks
3-5 are "Lofi, Rain & Fireplace", "Stillness" and "A Quiet Goodnight" where
the site lists Cozy Lo-fi Shelter, Hearthside Hours and Deep Resonance. Name
the DistroKid title in the ledger and the site's in the description.

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
| Fireside Harmony | Soft Flames & Breezes | `soft-flames-66-breathing` (1 hour) | 2026-11-17 |
| White Noise Therapy | Cloudscape Serenity (fetched from DistroKid) | `brown-noise-478-breathing` (1 hour) | 2026-11-18 |

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
| White Noise Therapy | `/zen/white-noise` | Ethereal Resonance |
| Feathered Tunes | `/zen/bird-sounds` | four of Morning Songbirds, Tree Top Tunes, Wings of Calm, Chirps & Tweets, Sky Echoes (one is used, name unknown) |
| Purring Melodies | `/zen/cat-purr-sounds` | four of Deep Sleep Purr, Violin Purr Serenade, Dreamy Purrs, Gentle Night Purr, Purr Therapy (one is used, name unknown) |
| Fireside Harmony | `/zen/fire-sounds` | Flickering Quiet, Twilight Musicbox, Breezy Warmth |
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
masking bed, but not a pure one. Soft Flames & Breezes, sold as "a pleasant and natural masking effect",
measured 59% at 200 Hz-1 kHz and 0.6% at 4-8 kHz: a comfort bed.
Cloudscape Serenity, on the "white noise" album, is a deep broadband noise
(flatness ~0.56, 75% below 200 Hz, 0.2% at 1-4 kHz, centroid 144 Hz) - close
to generated brown noise (96 / 3.1 / 0.6%), so it was titled "Brown Noise"
under E25 with comfort copy. Run
`band_energy` and the near-silent-window share on the file
(`projects/tinnitus.md`, "A comfort session is not a masking session").
