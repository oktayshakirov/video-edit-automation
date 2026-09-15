# Handoff: noise-canceling headphones pair, ready for `/publish-video`

Built and approved 2026-09-15. Open a fresh session and run `/publish-video`.

**Source article:** `noise-canceling-headphones-for-tinnitus`
(tinnitushelp.me/blog/noise-canceling-headphones-for-tinnitus)
**Channel:** Tinnitus Help · **Voice:** `mia` · **Music:** `night-drift`

## What was built

A long + Short pair from one post. The angle is the article's own reversal:
active noise control removes the outside sound tinnitus was competing with,
which helps in a noisy place and can backfire in a silent one, because the
brain turns its own gain up to fill the quiet. The fix is pairing the
headphones with soft sound instead of total silence.

### Long form (16:9) — 2:44

| | |
| --- | --- |
| Video | `/Users/oktayshakirov/Desktop/noise-canceling-headphones-for-tinnitus-long.mp4` |
| Thumbnail | `/Users/oktayshakirov/Desktop/noise-canceling-headphones-for-tinnitus-long-thumb.jpg` |
| Captions | `/Users/oktayshakirov/Desktop/noise-canceling-headphones-for-tinnitus-long.srt` |
| Metadata | `/Users/oktayshakirov/Desktop/noise-canceling-headphones-for-tinnitus-long.md` |
| Script | `projects/tinnitus-long/noise-canceling-headphones-for-tinnitus.py` |

YouTube title: **Can Noise-Canceling Headphones Make Tinnitus Worse?**
Seven chapters, first at 0:00 — the full list is in the `.md` sidecar, which
also carries the description, tags and the medical disclaimer. Use it rather
than re-deriving any of them.

### Short (9:16) — 44.7s

| | |
| --- | --- |
| Video | `/Users/oktayshakirov/Desktop/noise-canceling-headphones-for-tinnitus-short.mp4` |
| Reel cover (Instagram, Facebook) | `/Users/oktayshakirov/Desktop/noise-canceling-headphones-for-tinnitus-short-thumb.jpg` |
| YouTube thumbnail | `/Users/oktayshakirov/Desktop/noise-canceling-headphones-for-tinnitus-short-thumb-yt.jpg` |
| Script | `projects/tinnitus-short/noise-canceling-headphones-for-tinnitus.py` |

Opens on its title question, closes cold on the directive ("Never wear them
into total silence - always leave a little sound on"), no engagement question.

## Notes for publishing

- **Both thumbnails share one source and one headline** ("Headphones on. /
  Ringing louder?"), so the pair reads as a set. The source is the user's own
  pick: pexels.com/photo/3757028.
- **The long form carries the disclaimer** in its description credits; the
  Short deliberately does not, per `narration.md`.
- **No medical claims anywhere.** Nothing promises relief or a cure; the red
  flags in the description are the article's own.
- Nothing about this build is undecided. The working tree is clean and
  pushed (`aa61a8d`).

## Shipped with it (engine, already committed)

Worth knowing only if something looks unfamiliar while publishing:

- The long form opens with a new **animated title sequence** at 0:08 —
  `overlay.TitleOverlay`, on by `render_long(title_at=)`. This is the
  treatment for both channels from now on; the old `Shot(payload=)` title
  stamp is superseded.
- `compare` now raises on `picture=`; thumbnail headlines accept a `\n` as a
  hard row break; karaoke captions shrink an over-wide highlighted word.
