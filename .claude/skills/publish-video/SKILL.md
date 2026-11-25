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

**No long dashes, ever:** a single `-` in every title, description, tag and
caption you write. The picture is enforced in code - see
[design.md](../../../docs/video/design.md#only-a-hyphen-goes-on-screen).

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

## Three checks that ride in the one confirmation (2026-10-25)

Part of the non-gated prep. They do not add a stop: their results go into the
single confirmation message under the captions, one line each, and the user's
"go" covers them. They exist because a title, a thumbnail or a link is
cheapest to change before the upload and expensive after (`docs/video/demand/README.md`).

- **Demand.** Quote the build script's `DEMAND` line for the pair. `None`,
  or a script without the line, is reported as "no demand evidence" - not a
  blocker, but the user should see it before the video goes public.
- **The feed check, long form only.** If the handover reports it
  (`workflow.md` step 4), quote it. If not, run it now: search the `Meta`
  title on YouTube in the built-in browser and report whether the query
  returns videos with real views and whether our thumbnail stands out beside
  the top three at 320px. A title that returns nothing relevant is not a
  search anyone makes; say so and offer the searchable alternative.
- **The description's next step.** The line with the article link must name
  what the article gives that the video could not (the full table, the
  sources, the sessions), not "read more". A bare "read more" or "Full
  article:" line is flagged with a suggested rewrite. Never rewrite it
  silently - the description is what the editor approved at the build.

The same applies to both channels' Facebook captions: the `facebookCaption`
link line is the same next step, in the same words.

## Where each video goes

| Project | YouTube | Instagram | Facebook | TikTok | Site entry |
| --- | --- | --- | --- | --- | --- |
| crypto long | yes | no | yes, native video | no | yes |
| crypto short | yes | Reel | Reel | yes (draft) | no |
| tinnitus long | yes | no | yes, native video | no | yes |
| tinnitus short | yes | Reel | Reel | yes (draft) | no |
| drone long | yes | no | no | no | no |
| drone short | yes | no | no | yes (draft) | no |
| oktai long | yes (`--channel oktai`, with `--captions`) | no | no | no | the video's card on oktayshakirov.com/prompts gets its YouTube link |
| oktai short | yes | no | no | yes (draft, project `oktai`) | no |

**The two Facebook columns are different products and are not interchangeable.**
A short goes up as a **Reel** (vertical, 3 to 90 seconds, the Publish Reel
workflow). A long goes up as a **native video** on the Page feed (16:9, no
duration cap, the Publish Facebook Video workflow). A 2 to 4 minute explainer is
not a Reel and must never be squeezed into one; a vertical short posted as a
feed video wastes the format. Pick by the video, not by the site.

**Instagram is shorts only.** It has no long-form equivalent here - a 16:9
explainer has nowhere sensible to go on that account.

**OktAI posts to YouTube and TikTok only** (2026-11-25, "connect the oktai
youtube and tiktok to the sharing pipeline"). Its TikTok uses the drone
account's sandbox app with its own token (`publish/tiktok.py`, `PROJECTS`);
its long form's description links the free prompt at
`oktayshakirov.com/prompts/<id>/` (each prompt has its own page since
2026-11-25; old `#<id>` links redirect). After upload, set the entry's
`video` (`id`, `url`, `uploadDate`) in the portfolio's `data/prompts.json`,
run `node scripts/build-prompts.mjs` there, and push.
Until its TikTok token exists, Shorts are scheduled in TikTok Studio in
Chrome (2026-11-25): copies under 10 MB in a folder inside the repo (the
extension's file upload reads only session folders and refuses larger
files), the description typed, "Edit cover" -> upload the cover (it must
pass the 3:4 grid crop, `docs/video/thumbnails.md`), Schedule, date and
17:00 GMT+1. A scheduled post cannot be edited afterwards, and Studio has
no draft button. On YouTube, an API-uploaded Short gets no Related video
(`--related` only adds the "Full video" line): set it to the long form in
YouTube Studio (Details -> Related video). When the API quota is spent,
Studio uploads in Chrome work the same way; Chrome's file upload takes
10 MB at most, so a larger Short is two-pass encoded just under it first.

**Every channel's TikTok cover passes the 3:4 grid crop** (2026-11-25, the
editor: "make it a rule for every tiktok video upload, also for other
channels"). Run `tools/short_cover_check.py COVER.jpg` and look at the
`-tiktok-crop.jpg` it writes before any Short goes to TikTok; a flag means
rebuild the cover (`docs/publish/tiktok.md`).

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
meant the site only, and the editor corrected it: when they say to run this
skill, run everything the table says that project gets. Do not re-derive a
narrower scope from the wording of the request - the table is the scope.
The per-post confirmation in the Gates section still stands for what a
caption says and for the moment of triggering, but it is not a reason to omit
a platform from the run.

1. **The long first, then the short.** The short's description links to the long,
   so the long needs an id before the short is uploaded.
2. **YouTube, via `video-audit`.** Dry run, then `--apply`.
3. **Serve the render folder with `tools/range_server.py`, and tunnel it for
   the Reels.** The short's Reels need a public URL; the long's Facebook upload
   reads `127.0.0.1:8765` directly, so one server and one tunnel cover both. Stop it after step 4.
   **Stop n8n too once the last workflow has finished** (the long's Telegram
   share and Facebook video included) - the editor's instruction, 2026-10-27:
   always stop n8n when you finish using it, whether or not you started it.
4. **Short: Reels then TikTok. Long: native Facebook upload, then poster,
   `videos.json`, the deploy gate and `npm run sync-content`.** The Reel caption
   rules - short hook plus one or two sentences, 3 to 5 varied hashtags, **no
   link in the Instagram `caption`** but the article link **does** go in the
   optional `facebookCaption` - are in `docs/publish/instagram-facebook.md`. The
   site half is `docs/publish/site.md`. The Facebook
   step is the **Publish Facebook Video (Resumable)** workflow (2026-11-20),
   which pushes the render from `tools/range_server.py` on `127.0.0.1:8765` in
   chunks, so the long form needs no tunnel. The file_url Publish Facebook
   Video workflow is the fallback: Facebook dropped its fetch of a 508 MB
   session twice. Pass the **full** YouTube description; both workflows trim
   it to the first paragraph plus the article link themselves.
5. **Report what is still unlisted or private and what needs a manual tick.**
   The standing list: privacy in Studio, Studio's "Related video" field on a
   Short, the TikTok draft's caption and cover, and - for a Short - **the
   cover image itself**, which is a manual Studio step by design and not an
   API failure. Give the path to the vertical file rather than just naming
   the step. The user may also stagger the two publishes if they want - long
   form first, the Short a day or two later - but that is their call and
   changes nothing this skill does; do not add a pause for it.

## After the run - prune the stock cache

Once the project file is committed and the video is up, the screening pool it
left behind is dead weight. The cache reached 26 GB this way before anyone
looked.

```bash
cd ~/Coding/video-edit-automation
.venv/bin/python tools/prune_stock.py            # report
.venv/bin/python tools/prune_stock.py --apply    # delete the rest
```

It keeps every file a committed project cuts and drops the rest; the dropped
bytes are re-fetchable by Pexels id from `assets/stock/manifest.json`. Two
conditions: the shot list must already be **written into the project file** (it
reads the files on disk, committed or not - a clip chosen but not yet pinned in
a `.py` is a clip it deletes), and if it exits non-zero naming a missing path,
re-fetch that id rather than swapping in another clip.
The reasoning is in `docs/video/footage.md`.

**Then everything else the run leaves behind.** The editor's instruction,
2026-10-14: don't keep files that won't be used again on the laptop.

```bash
.venv/bin/python tools/prune_work.py --apply     # stale render work folders
```

That drops every `~/Desktop/.<name>-work` / `.work-<name>` folder and leftover
preflight directory not touched in 3 days. On 2026-10-14 they held 6.5 GB of intermediates
from failed renders and from drone and glitch builds, which never clean up after
themselves. An active re-cut touches its folder every run, so it is kept. Also
delete the publish tunnel's staging copies, and close any `.claude/worktrees/*`
checkout that a site or automation repo is left with **when its branch has no
commits missing from `main` and no uncommitted changes**; ask before touching
one that does. The `.srt` and `.md` sidecars on the Desktop stay - see
`docs/video/projects/crypto.md`.

## Gates

The whole sequence runs on one "upload". These do not:

- **Pushing to the live site and posting to social media are confirmed in the
  chat they happen in, every session**, regardless of any standing instruction.
  This is a standing rule of the publish sequence, not a per-run preference.

  **One phase, one confirmation. Settled 2026-08-31.** Do not stop the run
  mid-way to ask. Do the non-gated prep first - both YouTube uploads (unlisted,
  after their dry runs), the poster fetch, the `videos.json` entry, the tunnel,
  every dry run and the three checks above - then post **one** message with the
  full caption/title text for every social post and the site push, followed by
  the three check lines, and on a single "go" run the entire
  remainder top to bottom without pausing again. The gate is that one
  confirmation carries the exact wording and happens in this chat; it is not a
  licence to break the run into phases. The editor's instruction: "do all in one
  phase always."

  **Resuming after an interruption - do not re-confirm. Settled 2026-09-02.**
  If the run was already approved with a "go" this session and then broke
  part-way (a killed background task, an authorization-classifier denial on a
  curl to the tunnel URL, a process teardown), reconcile what actually landed -
  n8n executions (`?limit`, then `?status=running`), `git log` in the site repo,
  the YouTube channel, the `.secrets/tiktok-tokens.json` mtime - and finish the
  remaining steps without asking again. The captions were already shown and
  approved; the wording does not change on a resume. The editor: "always run all
  steps in one go, no need to ask me."
- **The `--apply` dry run is never skipped** on a YouTube upload. Show the plan.
- **A first post to a brand's Instagram or Facebook page is public the moment it
  succeeds** and cannot be made unlisted. There is no dry run for a Reel. Confirm
  the caption before triggering, not after.
