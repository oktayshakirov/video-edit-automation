---
name: video-tinnitus
description: Build tinnitushelp.me videos - either an article explainer as a long-form 16:9 plus its vertical Short in one run, or a sound-therapy session with a generated noise bed and breathing ring. Use when the user runs /video-tinnitus, asks for a tinnitus video, Short or Reel, wants a post from tinnitushelp.me turned into a video, or wants a masking, notched-audio or zen sound-therapy piece. Builds only; publishing is /publish-video. For crypto use video-crypto, for drone footage use video-drone.
---

# Tinnitus videos

**Two products that share an engine.** Ask which one before anything else:

- **Article explainer** - a long-form 16:9 and its vertical Short, built as a
  pair from one tinnitushelp.me post. The default.
- **Sound-therapy session** - a generated noise bed, a seamless picture loop and
  a breathing ring. No article, its own copy rules, and it lands on `/zen`.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with
`PYTHONPATH=.`. **Source site:** `~/Coding/tinnitus-blog`.

## Read these, in this order

The steps live in `docs/video/workflow.md` - read it first, every run. Then read
only what this build touches:

| Step | Read |
| --- | --- |
| Before anything | `docs/video/projects/tinnitus.md` - which product, the voice roster, and the medical limits |
| Before writing a word | `docs/video/narration.md` |
| The long form | `docs/video/longform.md` |
| The Short | `docs/video/shorts.md` |
| Drawn graphics | `docs/video/beats.md` |
| Choosing and screening footage | `docs/video/footage.md` |
| Type and layout on screen | `docs/video/design.md` |
| Music and sound | `docs/video/audio.md` |
| A session's bed and loop | `docs/video/projects/tinnitus.md` |
| Both thumbnails | `docs/video/thumbnails.md` |
| Something rendered wrong | `docs/video/troubleshooting.md` |

Do not work from memory of these rules. They are edited as the engine changes,
and a remembered version is a stale one.

## The run

1. **Ask which product** - explainer pair, or session.
2. **Suggest, do not pick.** For an explainer: `python3 tools/topics.py
   tinnitus`. Offer three to five candidates with a reason each, then stop and
   wait. An off-site topic is fine when asked for and never offered.
3. **Script both together** from the chosen article. A session has no article
   and takes the session copy rules instead.
4. **Build** - `projects/tinnitus-long/<name>.py` and
   `projects/tinnitus-short/<name>.py`, each setting `SOURCE_POST` (`None` for a
   session).
5. **Hand over and wait.** Re-cut as many times as the user asks.
6. **On approval: commit, write `HANDOFF-PUBLISH.md`, and tell the user to open
   a fresh session for `/publish-video`.**

## This skill does not publish

Everything about getting a render out - which file goes to which platform, the
metadata pass, the site registry entry, the social posts and their order - is
`/publish-video`'s, and it is the only copy. That sequence used to be duplicated
into every build skill; the copies drifted and cost a registry entry that had to
be reverted and a social post that could not be un-sent.

Do not describe upload steps, pre-empt them, or re-derive them from memory.

## The line that outranks everything else

**Nothing here diagnoses, and nothing here promises relief.** This is a health
audience, much of it distressed, and a confident sentence about a cure does real
harm. The full statement of that rule, and what it means for a hook, is in
`docs/video/projects/tinnitus.md` - read it before writing, not after a re-cut.

Also standing: **no ear close-ups, in either format.**
