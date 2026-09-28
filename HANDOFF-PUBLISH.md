# Ready to publish: cat purr comfort session, long + Short

Built 2026-09-28 by `/video-tinnitus`, re-cut the same day for positive-only copy. **Nothing has been published yet.** Open
a fresh session and run `/publish-video`; this file is what it reads.

**Channel:** tinnitushelp.me. Voice `luna` (session intro only), no music.

**Source:** off-site. Both scripts set `SOURCE_POST = None`, so `tools/topics.py`
will not mark any post as covered — that is correct, not a bug. The related zen
page is `zen/cat-purr-sounds`, which is the registry target below, **not** a
`posts/` article.

## The files

| What | Path |
| --- | --- |
| Long MP4 (20:00, 1920x1080) | `/Users/oktayshakirov/Desktop/Cat Purring for Tinnitus and Calm (20 Minutes).mp4` |
| Long thumbnail (1280x720) | `/Users/oktayshakirov/Desktop/Cat Purring for Tinnitus and Calm (20 Minutes).jpg` |
| Short MP4 (58.0s, 1080x1920) | `/Users/oktayshakirov/Desktop/Cat Purring for Tinnitus and Calm (Short).mp4` |
| Short thumbnail (1080x1920) | `/Users/oktayshakirov/Desktop/Cat Purring for Tinnitus and Calm (Short).jpg` |

Build scripts: `projects/tinnitus-long/cat-purr-comfort-20min.py`,
`projects/tinnitus-short/cat-purr-comfort-short.py`.
Source recording: `/Users/oktayshakirov/Desktop/1.wav` (10:00, the user's own).

**There is no `.srt` and no `.md` sidecar.** Sessions do not produce them —
`render_asmr_long` is not the article path. The metadata below *is* the sidecar
for this pair; take the title, description and tags from here.

## Metadata

**Long form**

- **Title:** `Cat Purring Sounds for Tinnitus and Calm (20 Minutes)`
- **Description:**

      Twenty minutes of cat purring with a breathing circle to follow, four
      seconds in and six seconds out.

      A purr is deep, resonant and rhythmic, sitting around 27 Hz on this
      recording, steady and unhurried. It is a sound of comfort and
      contentment, and people have always found it settling. Let it fill the
      room around you, let your attention rest on it, and follow the circle
      when it appears.

      Keep the volume low and comfortable, quiet enough to sit in the
      background.

      More sounds and sessions: https://www.tinnitushelp.me/zen/cat-purr-sounds

      This is a sound to listen to, not a treatment. Nothing here diagnoses
      anything or promises relief.

- **Tags:** cat purr, purring sounds, tinnitus, sound therapy, relaxing sounds,
  sleep sounds, breathing exercise, calm, asmr
- **Chapters:** none. A session is one continuous piece and chapter marks would
  invite skipping through it.

**Short**

- **Title:** `Cat Purring for Calm and Sleep 🐱 (4 In / 6 Out)`
- **Description:** short version of the above, keeping the zen URL. **The Short's CTA is the app, not the blog** — the project doc is
  explicit that app install is the far better conversion from short-form.

## What is new here, and what it constrains

**This is the channel's first comfort session, not a masking session.** It is a
new class and the reasoning is committed in `docs/video/projects/tinnitus.md`.
Two things follow for publishing:

1. **Do not write masking into any caption, title or social post.** Measured
   `band_energy` on the recording: 85.3% below 200 Hz, 14.0% in 200 Hz–1 kHz,
   **0.67% in 1–4 kHz**, 0.03% in 4–8 kHz.

   **Equally: do not write a disclaimer.** The user's direction is that this
   piece carries no negative statements, so an earlier cut's "it will not cover
   your tinnitus" is gone from the videos and must not reappear in the metadata
   or the social copy. Not claiming masking is the requirement; denying it is
   not. Sell the purr on comfort, rhythm and calm, which is what it is.
2. **The site's own `zen/cat-purr-sounds` page does call purrs masking**, which
   this recording does not support. **Unresolved, and the user's call** — the
   page and this video currently disagree in public. Raise it, do not silently
   edit the page as part of publishing.

Engine changes shipped with it (commit `e06f0cc`, pushed): `soundbed.tile` /
`seam_drop`, `render_asmr_long(bed_file_loop=...)`, and an `emoji` argument on
both session thumbnails.

## Registry entry

A session, so it takes `kind: "session"` and a **zen** target, like
`masking-breathing-5min` does — not a `blog` target:

```json
{
  "slug": "cat-purr-comfort-20min",
  "kind": "session",
  "title": "Cat Purring Sounds for Tinnitus and Calm (20 Minutes)",
  "label": "Comfort session",
  "description": "Twenty minutes of cat purring with a breathing circle to follow, four seconds in and six seconds out. Deep, resonant and rhythmic: a sound of comfort to settle under.",
  "duration": "PT20M",
  "seconds": 1200,
  "target": { "type": "zen", "slug": "cat-purr-sounds" },
  "alsoOn": [],
  "placement": "auto"
}
```

`id`, `uploadDate` and `poster` are filled in by the publish step as usual.

## Still undecided

- Whether to correct the "natural masking effect" sentence on
  `zen/cat-purr-sounds`. The videos now simply omit the claim rather than
  contradicting it, so the two no longer disagree in public — but the page
  still says something the recording does not support.
- Whether the Short's CTA points at the app listing or at the zen page. The
  project doc favours the app; the user has not said for this pair.
