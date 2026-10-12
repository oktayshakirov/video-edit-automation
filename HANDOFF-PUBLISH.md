# Ready to publish: rain masking session, long + Short

Built 2026-10-12 by `/video-tinnitus`. **Nothing has been published yet.** Open
a fresh session and run `/publish-video`; this file is what it reads.

**Channel:** tinnitushelp.me. Voice `luna` (session intro and outro only), no
music.

**Source:** off-site. Both scripts set `SOURCE_POST = None`, so `tools/topics.py`
will not mark any post as covered - that is correct, not a bug. The related zen
page is `zen/nature-sounds`, whose album lists a **Rain** track; that is the
registry target below, **not** a `posts/` article.

## The files

| What | Path |
| --- | --- |
| Long MP4 (20:00, 1920x1080) | `/Users/oktayshakirov/Desktop/Rain Sounds for Tinnitus (20 Minutes).mp4` |
| Long thumbnail (1280x720) | `/Users/oktayshakirov/Desktop/Rain Sounds for Tinnitus (20 Minutes).jpg` |
| Short MP4 (52.6s, 1080x1920) | `/Users/oktayshakirov/Desktop/Rain Sounds for Tinnitus (Short).mp4` |
| Short thumbnail (1080x1920) | `/Users/oktayshakirov/Desktop/Rain Sounds for Tinnitus (Short).jpg` |

Build scripts: `projects/tinnitus-long/rain-masking-20min.py`,
`projects/tinnitus-short/rain-masking-short.py`.
Source recording: `/Users/oktayshakirov/Desktop/Rain.mp3` (10:00, 320 kbps, the
user's own).

**There is no `.srt` and no `.md` sidecar.** Sessions do not produce them. The
metadata below *is* the sidecar for this pair; take the title, description and
tags from here.

## Metadata

**Long form**

- **Title:** `Rain Sounds for Tinnitus Masking (20 Minutes)`
- **Description:**

      Twenty minutes of steady rain with a breathing circle to follow, four
      counts in and six counts out.

      Set the volume just below your tinnitus, so you can still hear it
      faintly underneath the rain. Burying it completely is what most people
      do; sitting just under it is the idea here.

      Why rain: about two-thirds of this recording's sound sits between 1 and
      8 kHz, the range where tinnitus is most often heard. It is soft and even
      from start to finish, with no thunder and nothing sudden in it.

      More sounds and sessions: https://www.tinnitushelp.me/zen/nature-sounds

      This is a sound to listen to, not a treatment. Nothing here diagnoses
      anything or promises relief. If your tinnitus is new, getting louder, in
      one ear only, or pulses with your heartbeat, please see a doctor.

- **Tags:** rain sounds, tinnitus, tinnitus masking, rain sounds for tinnitus,
  sound therapy, relaxing rain, breathing exercise, calm
- **Chapters:** none. A session is one continuous piece and chapter marks would
  invite skipping through it.

**Short**

- **Title:** `Play This Rain Just Below Your Tinnitus 🌧️`
- **Description:** short version of the above, keeping the "just below your
  tinnitus" instruction, the not-a-treatment line and the zen URL. **The Short's
  CTA is the app, not the blog** - the project doc is explicit that app install
  is the far better conversion from short-form.

All copy uses plain hyphens, no em dashes.

## What constrains the copy

**This is a masking session, and the measurement is what allows it** - the
opposite outcome from the cat purr pair. `band_energy` on the recording, four
30s windows from 0s to 540s, all within a point of each other: ~10% below
200 Hz, ~14% in 200 Hz-1 kHz, **~34% in 1-4 kHz, ~34% in 4-8 kHz**, ~8% above
8 kHz. Unchanged after tiling and mixing (33.7 / 33.1% on the finished long
audio).

- "Masking" and "just below your tinnitus" are supported. Promising relief,
  improvement or a cure is not - same rule as every video on the channel.
- "No thunder, nothing sudden" is measured: 1s RMS stays within -34 to
  -28.9 dB across the whole file and no second rises 3 dB over the median.

Audio checks on the long cut: both tile seams (557s, 1114s) measured with
`soundbed.seam_drop` at **-0.00 dB and -0.17 dB**. `bed_file_skip=35` drops the
recording's own quiet build-in so the seams join level audio. Both MP4s
-19.6 LUFS integrated.

No engine changes in this run.

## Registry entry

A session, so it takes `kind: "session"` and a **zen** target:

```json
{
  "slug": "rain-masking-20min",
  "kind": "session",
  "title": "Rain Sounds for Tinnitus Masking (20 Minutes)",
  "label": "Masking session",
  "description": "Twenty minutes of steady rain with a breathing circle to follow, four counts in and six counts out. Set it just below your tinnitus, so you can still hear it faintly underneath.",
  "duration": "PT20M",
  "seconds": 1200,
  "target": { "type": "zen", "slug": "nature-sounds" },
  "alsoOn": [],
  "placement": "auto"
}
```

`id`, `uploadDate` and `poster` are filled in by the publish step as usual.

## Still undecided

- Registry target: `zen/nature-sounds` (lists a Rain track) or
  `zen/water-sounds` (mentions rain in passing, but its tracks are streams,
  waves and waterfalls). Picked nature-sounds; the user may prefer otherwise.
- The working tree has unrelated uncommitted work from another session (the
  `video-glitch` skill, `core/datamosh.py`, two drone-short scripts, and edits
  to the `video-performance-review` and `video-views-audit` skills). It was
  deliberately left out of this commit. `/publish-video` expects a clean tree,
  so the user needs to commit or stash it first.
