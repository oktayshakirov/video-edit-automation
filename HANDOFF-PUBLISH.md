# Handoff → /publish-video

**Built:** `brown-noise-vs-white-noise-for-tinnitus` — a long-form 16:9
explainer and its vertical Short, built as a pair (`/video-tinnitus`) for
tinnitushelp.me.
**Source article:**
`tinnitus-blog/content/posts/brown-noise-vs-white-noise-for-tinnitus.mdx` —
`SOURCE_POST = "brown-noise-vs-white-noise-for-tinnitus"` in both
`projects/tinnitus-long/brown-noise-vs-white-noise-for-tinnitus.py` and
`projects/tinnitus-short/brown-noise-vs-white-noise-for-tinnitus.py`.
**Date:** 2026-09-10
**Voice:** `mia` (`af_heart`, 1.10) — the female article reader, the tinnitus
explainer default. Same voice on both cuts.
**Music:** `night-drift`, the prepared track, shared by both cuts.
**Approved by the user** after five review rounds. The last round was six
fixes on the first cut; all six landed and were checked in the frames before
approval. They are listed under "What changed on the last cut" — worth a
glance before publishing, because an earlier cut that may have been
screenshotted looks different.

---

## Files (Desktop)

| what | path |
| --- | --- |
| long video (16:9) | `/Users/oktayshakirov/Desktop/brown-noise-vs-white-noise-long.mp4` |
| long captions | `/Users/oktayshakirov/Desktop/brown-noise-vs-white-noise-long.srt` |
| long thumbnail | `/Users/oktayshakirov/Desktop/brown-noise-vs-white-noise-long-thumb.jpg` |
| long metadata sidecar | `/Users/oktayshakirov/Desktop/brown-noise-vs-white-noise-long.md` |
| short video (9:16) | `/Users/oktayshakirov/Desktop/brown-noise-vs-white-noise-short.mp4` |
| short Reel cover (9:16) | `/Users/oktayshakirov/Desktop/brown-noise-vs-white-noise-short-thumb.jpg` |
| short YouTube thumb (16:9) | `/Users/oktayshakirov/Desktop/brown-noise-vs-white-noise-short-thumb-yt.jpg` |

- **Long:** 3:23 (203.86s), 1920x1080, h264/aac.
- **Short:** 41.7s, 1080x1920, h264/aac. No SRT file — captions are burned in.

The long's `.md` sidecar carries a **proposed** title, description, chapter
list and tags. Treat it as a draft for `/publish-video` to work from, not a
decision. Proposed title there: "White Noise vs Brown Noise for Tinnitus".

## What it is

Six chapters from the article:

1. **The colour wheel** — the app has white/pink/brown/green and no guidance;
   here is the short version.
2. **What do the noise colours actually mean?** — `grid` beat, five colours
   (white, pink, brown, grey, green) each with a one-line description and an
   emoji.
3. **Which colour matches your tinnitus?** — `compare` beat, two named
   columns: a high whistle or ring (start white/pink) vs a low hum or roar
   (start brown).
4. **How loud should it be?** — `gauge` beat: the marker sits at "BURIED, the
   ringing is gone", past a threshold tick labelled "partial masking — aim
   here". The track turns red past the threshold.
5. **What about notched sound therapy?** — `diagram` beat, four nodes, forward
   flow (no loop): cut your exact pitch → that band goes quiet → neighbouring
   nerve cells turn it down (lateral inhibition) → the overactive signal
   weakens over months.
6. **So which one do you start with?** — close.

**The Short is not a compression of the long.** It keeps one move: the colour
barely matters, the real mistake is turning the volume up until the ringing
is gone — a "volume arms race". One drawn beat, `diagram` with `loop=True`
(turn it up → brain adjusts → turn it up again), then a `chapter` full-screen
payoff card "IT IS THE VOLUME." and the action close "try it tonight". No
disclaimer line (long-form only).

## Medical line

No diagnosis and no promise of relief anywhere in either cut. Masking is
described by what it does — overlaps the frequency, gives partial cover,
leaves room for habituation — never as a treatment. The long carries the
standard disclaimer in its credits; the Short does not, per
`docs/video/narration.md`. No ear close-ups in either format.

## What changed on the last cut (2026-09-10)

Six fixes on the first cut, all landed:

1. **Thumbnail image** — was a cropped face that lost its eyes and did not
   match the opener. Now a clean object shot: white earbuds on dark fabric,
   whole thing, no subject to place. Same shot on the long cover, the Short
   Reel cover and the Short's YouTube thumb.
2. **Two-colour headline plates** — `"{White noise} or [brown noise]?"` with
   `accent="brown"`, `accent2="paper"`: "white noise" on a pale cream plate,
   "brown noise" on a brown one. New `{...}` / `accent2` feature in
   `thumb.py`; see `docs/video/thumbnails.md`.
3. **Opening line** — "Your **favourite** tinnitus app has a colour wheel
   now" (was "your tinnitus app", which sounded like the channel was pushing
   its own app).
4. **The 0:03 clip** — was a phone screen with someone dragging an
   image-edit slider. Now a person in bed with a phone, screen facing away.
5. **Opener face** — now the night profile of a man with an earphone,
   matching the Short's opener.
6. **Short first line** — "White, pink, or brown?" is its own caption on its
   own line, with a 0.5s gap after the opening question, instead of racing
   out on its tail.

## What `/publish-video` needs to do

Standard **tinnitus explainer pair**:

- **Long form** → YouTube (long), the `videos.json` site entry on
  tinnitushelp.me, and the Share Video run. Use the `.md` sidecar's proposed
  title/description/tags/chapters as the starting draft, then the usual
  `youtube-audit` dry run before `--apply`.
- **Short** → YouTube (Short), Instagram Reel, Facebook Reel, TikTok (draft).
  **No site entry, no social Share for the Short** — that rule is settled
  (see `HANDOFF.md`). The Short attaches to the long only in that they are
  the same topic.
- **Reel cover** — `brown-noise-vs-white-noise-short-thumb.jpg` is the 9:16
  Reel cover; the YouTube Short thumb is `-thumb-yt.jpg` (16:9). TikTok cover
  is set by hand in the draft.

Nothing is posted or scheduled. All titles are proposals.
