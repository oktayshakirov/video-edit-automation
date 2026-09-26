# Handoff: TMJ and tinnitus, long + Short

Built 2026-09-26 by `/video-tinnitus`. Committed as `6385a11`, pushed to
`main`. The working tree is clean apart from
`projects/drone-short/burgas-what-my-drone-sees.py`, which was already
untracked before this session and is nothing to do with this pair.

**Source article:** `tmj-and-tinnitus-the-jaw-connection`
(https://tinnitushelp.me/blog/tmj-and-tinnitus-the-jaw-connection)

**Channel:** tinnitushelp.me. Voice `mia`, music `night-drift`.

## The files

### Long form, 16:9, 3:38

| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/tmj-and-tinnitus-long.mp4` |
| thumbnail | `/Users/oktayshakirov/Desktop/tmj-and-tinnitus-long-thumb.jpg` |
| captions | `/Users/oktayshakirov/Desktop/tmj-and-tinnitus-long.srt` |
| metadata | `/Users/oktayshakirov/Desktop/tmj-and-tinnitus-long.md` |

Title, description, chapters, tags and the medical disclaimer are all in the
`.md` sidecar - take them from there rather than re-deriving them. YouTube
title is **Can TMJ Cause Tinnitus?**, which is the search phrase the whole
cut is aimed at.

### Short, 9:16, 45.1s

| what | path |
| --- | --- |
| video | `/Users/oktayshakirov/Desktop/tmj-and-tinnitus-short.mp4` |
| thumbnail | `/Users/oktayshakirov/Desktop/tmj-and-tinnitus-short-thumb.jpg` |

The Short has no sidecar (the format does not write one). Its own title
question is **Can your jaw change your tinnitus?** and the description should
carry the same article URL as the long form.

Build scripts: `projects/tinnitus-long/tmj-and-tinnitus.py` and
`projects/tinnitus-short/tmj-and-tinnitus.py`, both with
`SOURCE_POST = "tmj-and-tinnitus-the-jaw-connection"`.

## Worth knowing before publishing

- **Both halves open on a search bar**, with different queries so they are not
  competing for one results page: "can tmj cause tinnitus" on the long form,
  "why does my tinnitus change" on the Short. If the experiments ledger is
  being kept, tag both as `Search` openers, not `hook=`.
- **The Short closes cold on a directive** - "Teeth apart. Check again in an
  hour." - drawn in the opener's own type and held to the final frame.
- **The thumbnail source is the user's own pick** (Pexels 10648949), shared by
  both aspects with the same headline. It is a landscape file, so the vertical
  crop lands on the eye, cheek and jawline rather than the whole face; that is
  the known cost of a landscape source on a 9:16 thumbnail and it was
  accepted.
- **Nothing in either cut diagnoses or promises relief.** The strongest claim
  is "part of its volume", and the red flags (sudden hearing loss, a pulsing
  sound, a locked jaw or severe pain after a head injury, ear pain or fluid
  with a fever) are spoken, drawn on screen and routed to a doctor. The
  disclaimer in the sidecar's credits block must ship with the description.

## Still undecided

Nothing blocking. One judgement call the user may want revisited later: the
long form's closing section comes back to the jaw through a different shot
rather than re-using its own opening clip as a bookend, because the reuse
budget spent that second use on the Short.

## Next

Open a fresh session and run `/publish-video`.
