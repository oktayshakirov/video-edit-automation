# Handoff to /publish-video

**Built:** 2026-09-01 · **Project:** drone, long form (`projects/drone-long/berlin.toml`)
**Source article:** none — off-site footage project (`SOURCE_POST` n/a)
**Committed:** `main` @ `b4b9e11`, tag **`berlin-v3`** (locked, current)

---

## ⚠️ There is no MP4 yet — this is a Final Cut timeline

The drone long-form pipeline **never renders video**. It writes an FCPXML the
user finishes by hand in Final Cut. Before `/publish-video` can do anything:

1. Import **`/Users/oktayshakirov/Desktop/Berlin 26 2_4/Berlin.fcpxml`** into
   Final Cut (it matches `berlin-v3`; the user's own tuning export
   `Berlin font update.fcpxmld` is already folded into the committed fragments).
2. Do any final grade / trims in FCP.
3. **Export a 4K MP4** to the Desktop — suggested name
   `drone-berlin-treptower-long.mp4`.
4. Grab a thumbnail frame (see below) — the pipeline generates none for drone
   long form.

Only then open a fresh session and run `/publish-video`.

---

## What was built

A 3:06 long-form cut of Treptower Park at golden hour — 35 shots from 17 graded
selects (13 "Spree Buildings", "Spree Boats", 3 "Spree Hyperlapse"), cut to
TheFatRat's *Fly Away feat. Anjulie (VAVO Remix) [Trap]*.

- **Track plays once** and ends on its real ending — no loop seam. (Speeding
  Buildings 10/8/4 to 2x dropped the timeline below the song's 3:03, so the
  loop had nothing to extend to.)
- **Hyperlapses on the drops:** HL1 @ 0:28, HL3 @ 1:06, HL2 @ 2:24 — each pinned
  inside a musical peak section.
- **Buildings 7 held to the back half** (first appears 1:32) — it was shot later
  in the evening and broke the colour progression at the front.
- **Location pin** "TREPTOWER PARK, BERLIN" at 1.5s, lower-left, white / not
  bold / drop shadow — restyled and repositioned by the user in FCP, now baked
  into `assets/fcpxml/location-{pin,title}-overlay.xml` for all future videos.
- Coverage 60% (the cost of a tight 3-minute cut from a folder of near-identical
  hover shots); nothing reused more than 3x.

## Where it goes

**YouTube only.** Per the publish table, drone **long form** posts to YouTube
and nothing else — no TikTok (that's drone *short*), no Instagram, no Facebook,
no `videos.json` site entry.

Channel: **`drone`** (`youtube-audit` / upload `--channel drone`).

## Files (all absolute)

| File | Status |
| --- | --- |
| `/Users/oktayshakirov/Desktop/Berlin 26 2_4/Berlin.fcpxml` | ✅ built, validates clean (DTD 1.10) |
| `…/Berlin 26 2_4/TheFatRat - Fly Away feat. Anjulie (VAVO Remix) [Trap].mp3` | ✅ the track, in the project |
| `…/Berlin 26 2_4/Music Credits.rtf` | ✅ composer + source |
| **The exported MP4** | ❌ **user must export from Final Cut first** |
| **The thumbnail JPG (1280x720)** | ❌ **none generated — user picks a frame** |
| SRT captions | n/a — drone long form produces none |

## Metadata (no sidecar — use this)

- **Title:** `Berlin From Above — Treptower Park at Golden Hour | 4K Drone`
- **Tags:** `berlin, treptower park, drone, 4k, golden hour, sunset, aerial, berlin drone, spree, dji, cinematic`
- **Description:**
  ```
  Golden hour over Treptower Park and the river Spree, Berlin — shot on a drone in 4K. Hyperlapses timed to the music.

  Music:
  Fly Away feat. Anjulie (VAVO Remix) [Trap] — TheFatRat
  https://www.youtube.com/user/ThisIsTheFatRat

  Filmed in Berlin, Germany.
  ```
- The title / description / tag em-dash and formatting rules are enforced by
  `youtube-audit` at upload — run it dry first and take its cleanup.

## Attribution — MANDATORY in the description

TheFatRat's music is free to use **with credit**. The block above must stay in
the published description verbatim (track name, artist, channel URL). Source:
`Music Credits.rtf` in the footage folder.

## Undecided / notes

- **Thumbnail:** no pipeline thumbnail for drone long form. The user should
  export a still from the FCP timeline (a wide building-and-sunset frame, not a
  hyperlapse) at 1280x720, or `/publish-video` can pull `maxresdefault.jpg`
  after upload as a placeholder — but a chosen frame is better.
- **Privacy:** upload `unlisted`, tell the user to flip to public in Studio when
  ready (the standing rule).
- **`berlin-v1` / `berlin-v2`** are earlier tags kept only as fallbacks. Publish
  from the **`berlin-v3`** export.
- **Pin `dx` guess is now moot** — at the lower-left placement the title clears
  the pin, so `dx = 0`. Still worth a glance on screen once the MP4 is out.
