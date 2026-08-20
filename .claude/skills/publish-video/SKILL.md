---
name: publish-video
description: Publish a finished render to YouTube, Instagram Reels, Facebook Reels and TikTok, then to the site. Use when the user says "upload" or "publish" after a video has been built by any of the video-crypto / video-tinnitus / video-drone skills, or asks to post an existing render to the platforms. Covers the whole sequence - YouTube upload with thumbnail and metadata, the Reel workflows in n8n, the TikTok private direct post, and the videos.json site entry plus social share for long form.
---

# Publish a video

The six `video-*` skills **build**. This one **publishes**. They hand over and
say nothing about uploading; when the user says "upload", load this file and run
the sequence below. Splitting it this way is deliberate: the sequence is
identical for all three projects, and six copies of it would drift.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with `PYTHONPATH=.`.

## Where each video goes

| Project | YouTube | Instagram | Facebook | TikTok | Site entry |
| --- | --- | --- | --- | --- | --- |
| crypto long | yes | no | no | no | yes |
| crypto short | yes | yes | yes | yes | no |
| tinnitus long | yes | no | no | no | yes |
| tinnitus short | yes | yes | yes | yes | no |
| drone long | yes | no | no | no | no |
| drone short | yes | no | no | yes | no |

**Long form goes to YouTube and the site, nothing else.** Facebook Reels caps at
90 seconds and Instagram Reels is a vertical format; a 2 to 4 minute 16:9
explainer is not a Reel and must not be squeezed into one. This is the same rule
`video-crypto-long` already carries as "only the long form gets a site entry and
a social share" - it now has a second half.

**Drone posts to YouTube and TikTok only.** The user's decision, 2026-08-20. No
Meta leg exists for it and no Instagram or Facebook page is wired up.

## The order of the whole job

Run the whole thing on one "upload" without asking again per step. The gates at
the bottom are the exceptions, and they are not negotiable by a standing
instruction.

1. **The long first, then the short.** The short's description links to the long,
   so the long needs an id before the short is uploaded.
2. **YouTube, via `youtube-audit`.** Dry run, then `--apply`.
3. **Vertical only: start the tunnel**, publish the Reels, publish TikTok, stop
   the tunnel.
4. **Long only: poster, `videos.json`, deploy gate, Share Video.** Unchanged from
   what `video-crypto-long` already documents; that is still the canonical copy.
5. **Report what is still unlisted or private and what needs a manual tick.**

## YouTube

```bash
cd ~/Coding/youtube-audit && npx tsx src/cli.ts upload \
  --channel crypto --file out.mp4 --thumbnail thumb.jpg \
  --title "..." --description-file meta.md --tags "a,b" --privacy unlisted
```

Dry run without `--apply`, exactly like `set`. See the `youtube-audit` skill for
the quota arithmetic, the em dash rule the tool now enforces, and why
`--related` cannot set Studio's "Related video" field.

- **Reuse the `Meta` the long-form build already generated** - the `.md` sidecar
  in `<project>/transcripts/` - rather than re-deriving the description.
- **`--related <long-id>` on the short.** It appends the long's URL to the
  description. Tell the user to tick Studio's Related video field by hand; the
  Data API has no field for it.
- **Nothing here makes a video public.** Say so plainly at the end rather than
  letting the user assume the site entry published it.
- **A custom thumbnail on a Short never shows in the Shorts feed.** The vertical
  swipe feed always uses an auto-generated frame from the video. Custom Shorts
  thumbnails only landed in July 2026, are Partner Programme only, and appear in
  search, the channel Shorts tab, subscriptions and playlists - the surfaces
  where a thumbnail earns a click. So a Short's thumbnail looking "missing" in
  the feed is correct behaviour, not a failed `thumbnails.set`. Verify with
  `youtube-audit video <id>`: a `maxres` 1280x720 entry means it is set.
- **Letterboxing a 9:16 frame into a 1280x720 thumbnail wastes most of the
  frame.** A Short's thumbnail is still 16:9, so design it for that shape rather
  than padding the vertical render - the padded version reads as empty.

## The tunnel, for Instagram

Instagram's API takes a **public https URL** and cannot accept a file upload, so
the render has to be reachable from the internet for the length of the run.

```bash
cd <folder with the mp4 and the cover>
python3 -m http.server 8765 &
cloudflared tunnel --url http://localhost:8765
```

`cloudflared` prints a `https://<random>.trycloudflare.com` URL. Pass
`<tunnel>/<file>.mp4` and `<tunnel>/<cover>.jpg` to the workflow.

- **Stop both when the run finishes.** The tunnel is ephemeral and needs no
  account, which is exactly why it must not be left running - it is an
  unauthenticated public URL onto a local directory.
- **Serve the render folder, not the Desktop.** Whatever is in that directory is
  public for the duration.
- Facebook's leg reads the same URL, so one tunnel covers both.

## Instagram and Facebook Reels

One n8n form workflow per site. n8n must be running at `http://localhost:5678`;
if it is not, ask the user to start it.

| Site | Workflow | formData |
| --- | --- | --- |
| Crypto Wiki | `uIV6956N14pMGMZ5` | `{ videoUrl, coverUrl, caption, durationSeconds }` |
| Tinnitus Help | `1GTSF6izfwA1gpig` | `{ videoUrl, coverUrl, caption, durationSeconds }` |

Trigger and poll them the way the `publish-content` skill describes - the
multipart requirement and the `field-N` indexing trap apply here too, and this
workflow's Normalise Input node reads both forms for that reason.

- **`durationSeconds` is required** and is checked before anything uploads,
  because **Facebook Reels accepts 3 to 90 seconds only**. A short over 90s
  cannot go to Facebook at all; publish it to Instagram and TikTok and say so.
- The workflow does Instagram first (container, poll to `FINISHED`, publish),
  then Facebook (start, upload, finish). A failure after the Instagram publish
  means the Reel is already live on Instagram - **do not re-run the whole
  workflow**, that double-posts. Fix the Facebook half and finish it by hand.
- **Instagram's encode is the slow part and it varies.** On the 2026-08-20 smoke
  test the crypto container was `FINISHED` on the second poll, about 30s, and the
  tinnitus one took roughly 100s for the identical 5s file. The 20-attempt cap is
  five minutes and is not generous - do not lower it.
- `FB Reel Upload` authenticates by query string rather than the documented
  header. Verified working on both Pages; see the note in `publish-content`.

## TikTok

```bash
PYTHONPATH=. .venv/bin/python -m video_automation.publish post crypto out.mp4 \
  --caption "..."                          # dry run
```

`--apply` uploads. Projects are `crypto`, `tinnitus`, `drone`.

**It uploads a DRAFT to the account's inbox. It does not post.** The user opens
TikTok, finds it in the inbox, writes the caption, picks the cover and publishes.
Never describe a TikTok upload as published.

**Direct post does not work and is not a choice we made.** It was tried on
2026-08-20 and TikTok returned
`unaudited_client_can_only_post_to_private_accounts`: an unaudited client may
direct-post only to an account whose *profile* is private, and all three of these
are public brand accounts. The post's own privacy level is irrelevant -
`creator_info` lists SELF_ONLY among `privacy_level_options` and `init` refuses
regardless, so that response cannot be used to predict whether a post will be
accepted. `post_video(direct=True)` still exists, and still fails; do not reach
for it as a fix.

- **`PROCESSING_UPLOAD` at the end is not a failure.** Once `init` has returned a
  publish id and `uploaded_bytes` equals the file size, TikTok has the video and
  the draft arrives on its own; their status endpoint just lags, unevenly - on
  2026-08-20 the crypto upload reported `SEND_TO_USER_INBOX` immediately and the
  drone one was still `PROCESSING_UPLOAD` three minutes later with every byte
  received. **Never re-run on a timeout.** A second run uploads a second copy,
  and there is no API to list or delete inbox drafts to clean it up.
- **TikTok accepts no caption and no cover on a draft.** Not a limitation of this
  code - the inbox endpoint takes only `source_info`. Generate the caption
  anyway and print it for the user to paste. Do not offer to set a thumbnail.
- **Scopes are `user.info.basic,video.upload,video.publish`.** `video.upload` is
  the draft scope and is the one that matters. `video.publish` is kept only
  because `creator_info` needs it, and that is the only way to read the account
  nickname. A token minted before `video.upload` was added fails the inbox call
  with `scope_not_authorized` and needs a fresh authorisation, not a refresh.
- **The drone account cannot receive a TikTok upload by either route, and why is
  unknown.** Established 2026-08-20 with the identical 5s file: it delivered to
  Crypto Wiki and Tinnitus Help within seconds, while `oktay.shakirov` accepted
  the init, took every byte, issued a publish id, and stayed at
  `PROCESSING_UPLOAD` indefinitely without ever appearing. Direct post is refused
  there as well, correctly - it is a **public personal** account, and TikTok
  allows unaudited direct post only to a profile with the Private account toggle
  on. The only difference between it and the two that work is Business versus
  personal, which is a correlation across three accounts and **not** a
  established cause.
  **So drone TikTok is a manual step**: hand the user the file and the caption
  and let them post it in the app. Do not present a drone TikTok upload as done
  without checking `status`, and do not re-run on a timeout.
- **"Private" means two different things here and the distinction matters.**
  TikTok's `unaudited_client_can_only_post_to_private_accounts` is about the
  profile-level Private account toggle, not about Business versus personal. A
  public personal account is refused exactly like a public Business one.
- **The account guard runs before every upload.** It compares the token's
  `open_id` against the one bound at authorisation and refuses on a mismatch. If
  it fires, re-authorise in a private window logged in as the right account; do
  not work around it.
- Tokens refresh automatically. The refresh token expires after about a year and
  needs a browser round trip - `auth-url`, then `auth` with the pasted callback.

**Two authorisation errors, both settings rather than code:**

- **`non_sandbox_target`** - the account being logged in is not on that sandbox's
  Target Users list. Dashboard: the app, Sandbox tab, Sandbox settings, Target
  Users, Add account. A sandbox with an empty list rejects every account,
  including the developer's own.
- **`redirect_uri`** - the URI sent does not byte-for-byte match what the app has
  registered. **The three apps use three different domains**, one per brand, and
  they live in `.secrets/tiktok.json` as `redirectUri` per project. Never assume
  they share one. A missing `www.` or a trailing slash fails the same way, and
  note `oktayshakirov.com` is registered without `www.` while the other two have
  it.

## Gates

The whole sequence runs on one "upload". These do not:

- **Pushing to the live site and posting to social media are confirmed in the
  chat they happen in, every session**, regardless of any standing instruction.
  That rule is inherited from `video-crypto-long` and is not relaxed here.
- **The `--apply` dry run is never skipped** on a YouTube upload. Show the plan.
- **A first post to a brand's Instagram or Facebook page is public the moment it
  succeeds** and cannot be made unlisted. There is no dry run for a Reel. Confirm
  the caption before triggering, not after.

## Proven, 2026-08-20

A 5-second test video went the whole way: three YouTube uploads with thumbnails
(crypto, tinnitus, drone), and Instagram plus Facebook Reels on both brand
accounts, served off the tunnel. What that run established beyond the code:

- **Activating one of these workflows needs `path` set on the Form Trigger.**
  Newer n8n rejects `POST /workflows/<id>/activate` with "Missing or invalid
  required parameters: path" otherwise. The older Share workflows predate the
  requirement and carry no `path`, so copying their node shape is not enough.
- **Trigger the form with `field-0..3` as multipart.** Same trap as every other
  workflow here.

## Known limits, so they are not rediscovered

- Studio's "Related video" for Shorts is not on the YouTube Data API.
- TikTok cannot take a custom cover image, on any endpoint.
- Facebook Reels: 3 to 90 seconds, 30 posts per 24 hours.
- Instagram: 25 posts per 24 hours, and the account must stay a Business or
  Creator account linked to the Page or publishing stops working entirely.
- A YouTube upload costs 1600 of 10,000 daily quota units.
