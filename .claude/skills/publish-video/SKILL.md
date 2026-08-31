---
name: publish-video
description: Publish a finished render to YouTube, Instagram Reels, Facebook (Reels for shorts, native video for long form) and TikTok, then to the site. Use when the user says "upload" or "publish" after a video has been built by any of the video-crypto, video-tinnitus or video-drone skills, or asks to post an existing render to the platforms. Covers the whole sequence - YouTube upload with thumbnail and metadata, the Reel workflows in n8n, the TikTok draft, the native Facebook upload for long form, and the videos.json site entry.
---

# Publish a video

The three `video-*` skills **build**. This one **publishes**. They hand over and
say nothing about uploading; when the user says "upload", load this file and run
the sequence below. Splitting it this way is deliberate: the sequence is
identical for all three projects, and a copy per project would drift.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with `PYTHONPATH=.`.

## Read these

The order of the job, the platform table and the gates are here. Everything
platform-specific lives once in `docs/publish/` - read the doc for the platform
you are on, when you get to it, rather than all of them up front.

| Doc | When |
| --- | --- |
| `docs/publish/youtube.md` | Every run |
| `docs/publish/instagram-facebook.md` | The tunnel, Reels, the native Page video |
| `docs/publish/tiktok.md` | Any Short |
| `docs/publish/telegram.md` | Long form only |
| `docs/publish/site.md` | Long form only - registry, poster, deploy gate, sync |
| `docs/publish/n8n.md` | Any workflow that reports success and seems to have done nothing |

## Start by reading the handoff

The build session ends by committing its work and writing
`HANDOFF-PUBLISH.md` at the repo root - what was built, the absolute path of
every file, the source article slug, and anything left undecided. **Read it
first, and check `git status` is clean.**

A dirty tree means the build session did not finish. Say so and stop rather
than publishing a render whose script is not committed - the site entry and the
social posts both cite work that has to exist in history afterwards.

If there is no handoff file, ask the user which render to publish and confirm
the paths before running anything. Do not guess from the Desktop's newest MP4.

## Where each video goes

| Project | YouTube | Instagram | Facebook | TikTok | Site entry |
| --- | --- | --- | --- | --- | --- |
| crypto long | yes | no | yes, native video | no | yes |
| crypto short | yes | Reel | Reel | yes (draft) | no |
| tinnitus long | yes | no | yes, native video | no | yes |
| tinnitus short | yes | Reel | Reel | yes (draft) | no |
| drone long | yes | no | no | no | no |
| drone short | yes | no | no | yes (draft) | no |

**The two Facebook columns are different products and are not interchangeable.**
A short goes up as a **Reel** (vertical, 3 to 90 seconds, the Publish Reel
workflow). A long goes up as a **native video** on the Page feed (16:9, no
duration cap, the Publish Facebook Video workflow). A 2 to 4 minute explainer is
not a Reel and must never be squeezed into one; a vertical short posted as a
feed video wastes the format. Pick by the video, not by the site.

**Instagram is shorts only.** It has no long-form equivalent here - a 16:9
explainer has nowhere sensible to go on that account.

**Drone posts to YouTube and TikTok only.** The user's decision, 2026-08-20. It
has no Instagram or Facebook page wired up, and no site entry.

## The order of the whole job

Run the whole thing on one "upload" without asking again per step. The gates at
the bottom are the exceptions, and they are not negotiable by a standing
instruction.

**Invoking this skill authorizes the full sequence across every platform in
the table above, for every video the run covers - not just YouTube and the
site.** Settled 2026-08-27, after a run stopped short of Instagram, Facebook
Reels and TikTok on the reasoning that "upload... to the crypto wiki pages"
meant the site only, and the user corrected it: when they say to run this
skill, run everything the table says that project gets. Do not re-derive a
narrower scope from the wording of the request - the table is the scope.
The per-post confirmation in the Gates section still stands for what a
caption says and for the moment of triggering, but it is not a reason to omit
a platform from the run.

1. **The long first, then the short.** The short's description links to the long,
   so the long needs an id before the short is uploaded.
2. **YouTube, via `youtube-audit`.** Dry run, then `--apply`.
3. **Start the tunnel once and keep it up for both.** Both the short's Reels and
   the long's native Facebook upload need a public URL, so serve the render
   folder and open one tunnel rather than one per video. Stop it after step 4.
4. **Short: Reels then TikTok. Long: native Facebook upload, then poster,
   `videos.json`, the deploy gate and `npm run sync-content`.** The site half is
   `docs/publish/site.md`. The Facebook
   step is the Publish Facebook Video workflow - the Share Video workflows it
   replaced were deleted on 2026-08-20. Pass the **full** YouTube description;
   that workflow trims it to the first paragraph plus the article link itself.
5. **Report what is still unlisted or private and what needs a manual tick.**
   The standing list: privacy in Studio, Studio's "Related video" field on a
   Short, the TikTok draft's caption and cover, and - for a Short - **the
   cover image itself**, which is a manual Studio step by design and not an
   API failure. Give the path to the vertical file rather than just naming
   the step.

## Gates

The whole sequence runs on one "upload". These do not:

- **Pushing to the live site and posting to social media are confirmed in the
  chat they happen in, every session**, regardless of any standing instruction.
  This is a standing rule of the publish sequence, not a per-run preference.

  **One phase, one confirmation. Settled 2026-08-31.** Do not stop the run
  mid-way to ask. Do the non-gated prep first - both YouTube uploads (unlisted,
  after their dry runs), the poster fetch, the `videos.json` entry, the tunnel,
  and every dry run - then post **one** message with the full caption/title text
  for every social post and the site push, and on a single "go" run the entire
  remainder top to bottom without pausing again. The gate is that one
  confirmation carries the exact wording and happens in this chat; it is not a
  licence to break the run into phases. The user's instruction: "do all in one
  phase always."
- **The `--apply` dry run is never skipped** on a YouTube upload. Show the plan.
- **A first post to a brand's Instagram or Facebook page is public the moment it
  succeeds** and cannot be made unlisted. There is no dry run for a Reel. Confirm
  the caption before triggering, not after.
