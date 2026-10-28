# Handoff: what-does-tinnitus-sound-like (long + Short)

Approved by the user 2026-10-28 after the re-cut (sound samples in, new
covers, the Short's ending and 0:03 clip changed). Channel: tinnitushelp.me.
Voice **`noah`** (male, the voice test - tinnitus pair 3 of 5,
`docs/video/projects/tinnitus.md`), music `night-drift`. Source article
slug: `what-is-tinnitus` (https://tinnitushelp.me/blog/what-is-tinnitus).
Build commit on `main`, pushed. **Nothing has been published yet.**

The subject is proven on two channels: MUSC Health's Short (593k, 4820x its
median) and UCI Otolaryngology's "Is tinnitus ringing or buzzing?" (1.1M,
932x). Teardown: `docs/video/demand/teardowns/what-does-tinnitus-sound-like.md`.

## Files

| What | Path |
| --- | --- |
| Long form (3:18) | `/Users/oktayshakirov/Desktop/what-does-tinnitus-sound-like-long.mp4` |
| Long thumbnail | `/Users/oktayshakirov/Desktop/what-does-tinnitus-sound-like-long-thumb.jpg` |
| Long captions | `/Users/oktayshakirov/Desktop/what-does-tinnitus-sound-like-long.srt` |
| Long sidecar (title, description, chapters, tags) | `/Users/oktayshakirov/Desktop/what-does-tinnitus-sound-like-long.md` |
| Short (55.5s) | `/Users/oktayshakirov/Desktop/what-does-tinnitus-sound-like-short.mp4` |
| Short cover | `/Users/oktayshakirov/Desktop/what-does-tinnitus-sound-like-short-thumb.jpg` |

Scripts: `projects/tinnitus-long/what-does-tinnitus-sound-like.py`,
`projects/tinnitus-short/what-does-tinnitus-sound-like.py`. Both carry
`DEMAND` and `SOURCE_POST`. Covers rebuild without a render: `--thumb` on
either script.

## Titles

- Long: **What Does Tinnitus Sound Like? Ringing, Hissing, Buzzing and More**
  (in the sidecar) - the search query first.
- Short: **Is Tinnitus Ringing or Buzzing?** - its own sentence 1 and its
  `Search` opener, UCI's query rather than the long form's. The Short has no
  sidecar; its description follows the channel's Short rules with the
  article URL and `Full video:` to the long form.

## Tagging for the review

- Openers: long `Search` ("what does tinnitus sound like"), Short `Search`
  ("is tinnitus ringing or buzzing").
- New: the `spectrum` beat's sounds mode, and **played sound samples**
  (`core/samples.py`) after a lower-your-volume notice card - the first
  video on this channel that plays the symptom it describes. Worth watching
  for comments about the samples, either way.
- Both cuts end on the same question: "If you had to name yours, which of
  the five would it be?"

## The description's next step

The long description's link line names what the article adds: "every
cause, what a professional check involves and the full list of red flags".
Social captions should carry the same link.

## Credits the descriptions owe

- Long: the disclaimer, already in the sidecar. No third-party press art.
  No Pexels or music line (dropped channel-wide 2026-10-20) - the covers'
  photo is Pexels 3761514, the user's pick.
- Short: no disclaimer, by the channel rule.

## Feed check (`workflow.md` step 4)

The query is big: NHS 24 651k, Treble Health 1M, Hearing Healthcare Centre
1.5M, Sound Relief's 7500 Hz tone 3.1M. Every top result plays examples, so
the first drawn-only cut was the weaker promise; the samples answer that.
The first cover nearly copied NHS 24's (big question over a person with a
hand at the ear); the user replaced the photo with a man listening to a
paper-cup phone on a white wall, which none of the top covers look like.

## Undecided

- **The site entry.** No video in `tinnitus-blog/src/data/videos.json`
  points at `what-is-tinnitus` yet, so a new entry is expected; the slug and
  poster are publish-video's call.
- **The description does not say the samples are played.** The sidecar's
  first line is "Here are the five people describe..." - the metadata pass
  may want "hear a short, quiet sample of each" in it, since hearing them is
  what this query promises.
