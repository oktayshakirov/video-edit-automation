# Build changes: what the videos were built with, and from when

A review compares videos. It can only do that fairly if it knows which
rules each one was built under. **Every time a build rule, the engine's
look, or a skill changes in a way a viewer could notice, add a dated entry
here** - in the same commit as the change. Newest first. A review run reads
this before step 3 (tagging), and treats videos on either side of an entry
as different cohorts.

Keep an entry to what changed for the viewer and where the rule lives.

## 2026-11-18 - first E25 session; beds fetched from DistroKid

- **`brown-noise-478-breathing` is E25's first session**: "Brown Noise"
  leads the title and cover, the album track (Cloudscape Serenity) is named
  only in the description. Count E25's four from here.
- **Session beds now come from DistroKid, picked by the build** from the
  unused tracks (`projects/tinnitus-sounds.md`, "Fetching the next track"),
  not from a file the editor drops. Nothing a viewer hears changes; the
  choice of track is now the build's, under E25 and the measurement.

## 2026-11-17 - the review: sessions first, new formats, covers

From the 11-17 review, on the editor's yes (`history/2026-11-17.md`).

- **Tinnitus mix: about two sessions per article pair** (`projects/
  tinnitus.md`, "The mix"). Sessions lead with a named masking noise -
  white, pink, brown, rain - in title and cover (E25). One 8-hour
  white-noise sleep bed as a probe.
- **E26 formats:** tinnitus article pairs as a numbered list or a ranking
  by evidence; crypto pairs as one heist told as a story. These long forms
  run 5-8 minutes (`FORMAT` in the script; `retention_check` knows it).
  Every other article long form stays at 2:30-3:00.
- **Covers add to the title, never repeat it**; a list cover carries its
  number; no stock person holding their head on tinnitus
  (`thumbnails.md`). `script_check` gained `cover-repeats-title`.
- **Titles of older videos rewritten** where a better search phrase or
  format existed (the list is in the snapshot). A title change splits that
  video's own history: read it before/after, not against new builds.
- E11 became a rule, E12 / E18 / E23 retired (`experiments.md`).

## 2026-11-17 - fireside session; sentence gaps stay out of words

- `soft-flames-66-breathing`: session queue row 5, coherent 6-6 breathing
  on the path guide, 1 hour, a generated campfire look. A comfort session
  (no masking line): the bed is almost all below 4 kHz.
- Narration: a sentence gap could be inserted inside a word ending in a
  quiet consonant ("breath ... s"); `_pad_pause` now finds the real pause
  (`voice.md`, "A sentence gap can land inside the last word"). Shipped
  videos are unaffected unless re-rendered; a re-render can differ where
  the fault fired.

## 2026-11-16 - a rumour as the title (crypto, `stablecoin-interest`)

- The long form is titled with a circulating rumour, as people search it
  ("Is the US Using Stablecoins to Reset Its Debt?"), and checks it by
  mechanism, ending on a checklist of the claims and a question for the
  comments. The editor's ask: try the conspiracy side for engagement. Read
  views and likes + comments per view against the plain mechanism titles.
- New beat `reserve`: a dollar lent on, the interest to the issuer, the
  line back to you blocked at $0 (`beats.md`).
- First crypto cover with a cut-out real official (public-domain portrait)
  and extruded type (`cutout`).

## 2026-11-13 - covers rotate, light overlays, the ruled ground

- Covers: no style three videos running (`cover-rotation`); new styles
  `cutout` and `vector` (`thumbnails.md`).
- Footage carries lens flares and floating motes in the overlay rotation;
  key words and the opener sit in the empty side of the shot; the opener
  enters on a word, not on frame one (`longform.md`).
- Explaining beats can sit on a dark ruled ground; the grid chapter card
  replaces the band card as the long-form default (`beats.md`). First on
  `what-makes-tinnitus-worse`, approved there.

## 2026-11-12 - picture first (crypto and tinnitus article videos)

From the editor's review of the `hardware-wallet` pair. First pair built
this way: `hardware-wallet`. Tested as E23.

- **The picture is planned before the footage**, one line per sentence
  (`docs/video/workflow.md`, "Write the picture first").
- **No two full-frame pictures in a row; at least half a long form is
  drawn or framed** - beats, `window=`, `callout`, `spotlight`, captured
  pages (`footage.md`).
- **Signature beats rest for two videos** - the coin `pile` in particular
  (`beats.md`). Two new beats: `airgap`, `breach`.
- **No title slate** on long forms (`longform.md`).
- **Covers:** six words or fewer on two rows, the accent on the subject's
  word, tighter word spacing (`thumbnails.md`).
- **Voice:** acronyms said as words are read as words (PIN) (`voice.md`).
- `script_check` gained `full-frame-run`, `drawn-share`, `beat-rotation`,
  `title-slate`, `cover-headline`.
- **The review itself changed:** five live tests at most, the rest retired
  (`experiments.md`); a row per video in `videos.md`; this file.

## 2026-11-10 - written to be watched to the end

- Shorts: a 10-13 word title question so sentence 2 starts near 4s (E21),
  the opener held until captions resume (E22), 30-40s on crypto (E17), a
  loop-back last line on tinnitus.
- Long forms: 2:30-3:00 (E18). Stock at most half the shots; `window=`.

## 2026-11-06 to 11-08

- Shorts end on a plain sentence, no outro card. The 11-05 toolbox
  (captured pages, depth moves, `behind`, `pile`, shaders) made required.
- Covers declare `COVER_STYLE`; arrow-and-ring covers begin.

## 2026-10-21 to 10-25

- The engine overhaul (band chapter cards, old-film surface, glitch cuts,
  reel / post / spotlight beats). `noah` voice test begins 10-23 and ended
  with pair 5 on each channel; `mia` is the voice from 2026-11-12.
- Topics carry demand evidence from 10-25 (E11).
