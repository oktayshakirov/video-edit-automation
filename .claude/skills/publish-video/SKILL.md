---
name: publish-video
description: Publish a finished render to YouTube, Instagram Reels, Facebook (Reels for shorts, native video for long form) and TikTok, then to the site. Use when the user says "upload" or "publish" after a video has been built by any of the video-crypto / video-tinnitus / video-drone skills, or asks to post an existing render to the platforms. Covers the whole sequence - YouTube upload with thumbnail and metadata, the Reel workflows in n8n, the TikTok draft, the native Facebook upload for long form, and the videos.json site entry.
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

1. **The long first, then the short.** The short's description links to the long,
   so the long needs an id before the short is uploaded.
2. **YouTube, via `youtube-audit`.** Dry run, then `--apply`.
3. **Start the tunnel once and keep it up for both.** Both the short's Reels and
   the long's native Facebook upload need a public URL, so serve the render
   folder and open one tunnel rather than one per video. Stop it after step 4.
4. **Short: Reels then TikTok. Long: native Facebook upload, then poster,
   `videos.json`, the deploy gate and `npm run sync-content`.** The site half is unchanged from what
   `video-crypto-long` documents; that is still the canonical copy. The Facebook
   step is the Publish Facebook Video workflow - the Share Video workflows it
   replaced were deleted on 2026-08-20. Pass the **full** YouTube description;
   that workflow trims it to the first paragraph plus the article link itself.
5. **Report what is still unlisted or private and what needs a manual tick.**
   The standing list: privacy in Studio, Studio's "Related video" field on a
   Short, the TikTok draft's caption and cover, and - for a Short - **the
   cover image itself**, which the Data API cannot set. Give the path to the
   vertical file rather than just naming the step.

## YouTube

```bash
cd ~/Coding/youtube-audit && npx tsx src/cli.ts upload \
  --channel crypto --file out.mp4 --thumbnail thumb.jpg \
  --title "..." --description-file meta.md --tags "a,b" --privacy unlisted
```

Dry run without `--apply`, exactly like `set`. See the `youtube-audit` skill for
the quota arithmetic, the em dash rule the tool now enforces, and why
`--related` cannot set Studio's "Related video" field.

- **Pass `--captions <the .srt>` on a long form.** Added 2026-08-23. The
  long-form build already writes an exact SRT next to the MP4, and uploading it
  costs nothing extra: `force-ssl` already covers `captions.insert`, so no
  re-authorisation was needed. It replaces nothing - YouTube's auto-generated
  track stays alongside ours and viewers get the accurate one, which matters
  because ASR guesses at brand names, figures and jargon (it has no idea what
  "SegWit" or "3.125 BTC" is). Captions are also indexed for search and are
  what a sound-off viewer reads.

  Shorts burn their captions into the picture, so an SRT adds less there - and
  `render_crypto_short` does not produce one anyway. Long form only, in
  practice.

  **A "already has a caption track" error can mean it worked.** The insert is
  not safely retryable and googleapis retries it, so the first real run
  reported a conflict while the track was live and serving with our exact
  timings - the retry had collided with what the first attempt created.
  `uploadCaptions` now lists before inserting and returns the existing track
  id, so this is idempotent; if you ever see that message from something else,
  **list the tracks before concluding anything**, and never upload a second
  copy by hand.
- **Reuse the `Meta` the long-form build already generated** - the `.md` sidecar
  in `<project>/transcripts/` - rather than re-deriving the description.
- **`--related <long-id>` on the short.** It appends the long's URL to the
  description. Tell the user to tick Studio's Related video field by hand; the
  Data API has no field for it.
- **Verify the description-file actually contains a working link before
  `--apply`.** An audit on 2026-08-23 found nine already-live crypto and
  tinnitus Shorts whose descriptions said "Read more on thecrypto.wiki" or
  "More at tinnitushelp.me" with no URL attached - a dead end for every viewer
  who wanted to click through. Read the `.md` sidecar before uploading and
  confirm it carries the real article URL, the same one the long's
  `Full article:` line uses; a tinnitus sound-therapy short with no source
  article links to `https://tinnitushelp.me/zen` instead (the sessions hub -
  Spotify, Apple Music, YouTube Music, Amazon Music, Deezer), never an
  invented blog slug.
- **Put `#shorts` at the end of a Short's title.** Settled as the metadata
  baseline in the `youtube-audit` skill on 2026-08-23 after the one Short that
  already had it was also the channel's best performer to date - one data
  point, adopted because it costs nothing, not because it was measured. Build
  it into the title at upload time rather than leaving it for a later audit
  pass.
- **If a video ever comes up mislabelled with the wrong `defaultLanguage`**
  (a fully English crypto Short once went live as `de`, before the channel's
  own default language was set to English on 2026-08-23), fix it with
  `youtube-audit set <id> --channel <ch> --language en --apply` (added the
  same day). Studio's "Video language" control does not reach this field - it
  only writes `defaultAudioLanguage` - so that field is API-only to fix.
- **Nothing here makes a video public.** Say so plainly at the end rather than
  letting the user assume the site entry published it.
- **A Short's cover cannot be set through the Data API. It is a manual step in
  Studio, and this is settled - the rule flipped twice before landing here, so
  do not move it again without new evidence.** The full matrix, all measured on
  the bitcoin-price short:

  | Cover image | How it was set | What Studio shows |
  | --- | --- | --- |
  | 1280x720 | API, at upload | a video frame |
  | 1080x1920 | API, after upload | **blank** |
  | 1080x1920 | API, at upload | **blank** |
  | either | by hand in Studio | **the cover** |

  `thumbnails.set` reports success in every one of those rows, and every
  thumbnail URL serves the uploaded image in every one of them, so **neither
  the API response nor `youtube-audit video <id>` nor diffing
  `maxresdefault.jpg` can tell you which row you are in.** Only Studio can.
  That is why this took three attempts to pin down.

  So: **upload `<name>-thumb-yt.jpg` (1280x720) for a Short**, exactly as for a
  long form. A 9:16 upload is strictly worse - it renders blank rather than
  falling back to a frame, and it letterboxes every 16:9 surface (search,
  playlists, embeds) with blurred side-fill.

  **Then tell the user to set the cover by hand in Studio, and give them the
  path to the vertical file.** It belongs in the closing list beside the
  "Related video" tick and the TikTok draft - things the API cannot do.

  **Two wrong explanations, recorded so they are not re-derived.** First: the
  four earlier Crypto Wiki shorts carry vertical covers that display
  correctly, which was read as proof the API should send 9:16. It was not -
  the user had set those by hand. *An artifact's appearance says nothing about
  how it got there.* Second: a Partner Programme limit was blamed; also wrong,
  since covers work on this 3-subscriber channel when set manually.
- **The swipe feed is YouTube's own choice regardless.** Even a correctly set
  cover governs the Shorts tab, search and playlists rather than the vertical
  feed, which picks its own frame.
- **A Short needs TWO thumbnails and YouTube gets the 16:9 one.** This was
  written as advice and then ignored on the silence pair, which uploaded the
  1080x1920 Reel cover to YouTube. It is not merely wasteful - YouTube
  letterboxes a 9:16 upload into its 1280x720 slot with a **blurred, zoomed
  copy of the same image either side**, so the live thumbnail was a narrow
  strip of picture with "DOES ... NCE" bleeding across the bottom in huge soft
  letters. The user replaced it by hand. `thumbnails.set` returns success
  either way, and `youtube-audit video <id>` reports a `maxres 1280x720`
  entry, so **neither the upload nor the audit can tell you this went wrong -
  only looking at the image can.**

  The short project files render both: `<name>-thumb.jpg` (vertical, for the
  Reel workflows and for the user's manual Studio step) and
  `<name>-thumb-yt.jpg` (1280x720, for `youtube-audit upload`). That split
  stands - and note the letterboxing described above is the *only* thing a
  9:16 YouTube upload buys you, since it does not produce a working cover
  either. See the Studio matrix above.

  A shorts-only cut with no long form still needs both; render the landscape
  one with `render_thumb`, reusing the vertical's headline and `crop_at`.

## The tunnel, for Instagram

Instagram's API takes a **public https URL** and cannot accept a file upload, so
the render has to be reachable from the internet for the length of the run.

**Start both yourself.** `video-edit-automation/.claude/settings.json` carries
the permission rules that make this possible - `Bash(python3 -m http.server *)`
and `Bash(cloudflared tunnel *)` - so neither needs a prompt and neither is the
user's job any more.

```bash
python3 -m http.server 8765 --directory <folder with the mp4 and the cover>
```

```bash
cloudflared tunnel --url http://localhost:8765
```

Run the server with `run_in_background: true`; it never exits on its own.

**Use `--directory`, not `cd <folder> && python3 ...`.** A permission rule
matches the command string from its start, so a compound `cd X && python3 ...`
does not match `Bash(python3 -m http.server *)` and gets classified as if no
rule existed. This is the general shape of the trap: **an allowlisted command
loses its allowlisting the moment you prefix it with anything.**

`cloudflared` prints a `https://<random>.trycloudflare.com` URL. Pass
`<tunnel>/<file>.mp4` and `<tunnel>/<cover>.jpg` to the workflow.

**Read the tunnel URL yourself; never ask the user to paste it.** A quick
tunnel serves its own hostname on the metrics port, so the URL is one request
away even when `cloudflared` was started in somebody else's terminal:

```bash
lsof -nP -iTCP -sTCP:LISTEN -a -p $(pgrep -f 'cloudflared tunnel') | tail -1
curl -s http://127.0.0.1:20241/quicktunnel     # {"hostname":"...trycloudflare.com"}
```

20241 is the default metrics port; the `lsof` line finds it when it is not.
**Then `curl` both URLs and check for `200` and the right byte count before
triggering anything** - a workflow that starts against a dead tunnel fails
halfway, and the Instagram half is not safely re-runnable.

**This used to be blocked by the permission classifier**, on 2026-08-23, and
the tunnel was the one part of the run the user had to start by hand. That is
fixed: the project settings file above allowlists both commands, verified by
running them. If a future session is denied anyway, check that
`.claude/settings.json` still exists in `video-edit-automation` and that the
command is not wrapped in a `cd ... &&` prefix. Never make the user read the
tunnel URL off their screen - take it from the metrics endpoint.

- **Stop both when the run finishes.** The tunnel is ephemeral and needs no
  account, which is exactly why it must not be left running - it is an
  unauthenticated public URL onto a local directory.
- **Serve the render folder, not the Desktop.** Whatever is in that directory is
  public for the duration.
- Facebook's leg reads the same URL, so one tunnel covers both.

## Instagram and Facebook Reels

One n8n form workflow per site. n8n must be running at `http://localhost:5678`.
**If it is not, start it yourself** - just run `n8n` in the terminal. The
user's instruction, 2026-08-23; do not stop and ask them to do it.

**The workflows are version-controlled**, one JSON per workflow at the root of
each automation repo: `publish_facebook_video.json`, `publish_reel.json` and
`share_video_telegram.json` in both `crypto-wiki-automation` and
`tinnitus-help-automation`. Re-export after changing one in n8n, stripping
`createdAt`/`updatedAt`/`versionId`/`triggerCount` so the diff carries meaning.
Credentials are referenced by id and name only, so an export holds no secrets.

Two caveats on the older tracked exports: `share_post.json` and `share_og.json`
carry workflow ids that no longer exist live, and `share_video.json` describes
a workflow deleted on 2026-08-20. Do not trust a tracked export's id without
checking it against `GET /workflows`.

| Site | Workflow | formData |
| --- | --- | --- |
| Crypto Wiki | Publish Reel `uIV6956N14pMGMZ5` | `{ videoUrl, coverUrl, caption, durationSeconds }` |
| Tinnitus Help | Publish Reel `1GTSF6izfwA1gpig` | `{ videoUrl, coverUrl, caption, durationSeconds }` |
| Crypto Wiki | Publish Facebook Video `zS3xX6tbXpXnF32N` | `{ videoUrl, title, description, thumbUrl }` |
| Tinnitus Help | Publish Facebook Video `Lyhn5U7pYhrAs9x7` | `{ videoUrl, title, description, thumbUrl }` |

Trigger and poll them the way the `publish-content` skill describes - the
multipart requirement and the `field-N` indexing trap apply here too, and this
workflow's Normalise Input node reads both forms for that reason.

**`GET /api/v1/executions` hides running executions, and on this workflow that
looks exactly like a failed trigger.** The form POST returns `{"status":200}`
immediately and the run then takes three to five minutes, so a poll of
`?limit=1` comes back with the *previous* execution - on 2026-08-23 that was
the August smoke test, complete with its "Pipeline test - please ignore"
caption and a full set of successful nodes. It reads as "my run never
started", and the obvious next move is to fire it again, which double-posts to
Instagram with no way to undo it.

**So find the id with `?status=running` first, then poll
`/executions/<id>` directly.** Never conclude a trigger failed from the
default listing, and never re-fire on that basis. Confirm from the execution's
own `Normalise Input` output that the caption and URLs are yours before
believing a run is the one you started.

- **The Facebook Reel's cover is set after publishing, by two nodes that must
  never fail the run.** `coverUrl` reaches Instagram as `cover_url` on the
  container and reached Facebook **not at all** - the Reels finish phase takes
  `video_state` and `description` and has no cover parameter, so every Facebook
  Reel published before 2026-08-23 went up with an auto-picked frame and the
  user set the cover by hand. `FB Fetch Cover` pulls the image as binary and
  `FB Set Reel Cover` POSTs it multipart to
  `/{video_id}/thumbnails?is_preferred=true`.

  **Both carry `onError: continueRegularOutput`, deliberately.** They run
  *after* the Reel is live on both platforms, so a failure there must degrade
  to "no cover" rather than to a red execution that invites a re-run - and a
  re-run double-posts to Instagram. `Summary` reports `facebookCoverSet` so
  the outcome is visible without reading node output.

  **Verified working, 2026-08-23**, on the bitcoin-price short: execution 504
  returned `facebookCoverSet: true` on a real publish. The two nodes do what
  they were written to do and need no further babysitting; keep reading
  `facebookCoverSet` in the Summary anyway, since they are the one part of the
  run that is allowed to fail quietly.
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

**TikTok takes no cover image, on any endpoint, ever.** Asked again on
2026-08-23: the inbox endpoint accepts `source_info` and nothing else, and
even direct post (which these accounts cannot use at all) has no thumbnail
parameter. The cover is picked in the app when the user publishes the draft.
This is not a gap to be closed later - do not offer to fix it, and do not
describe a TikTok upload as having a thumbnail.

**It uploads a DRAFT to the account's inbox. It does not post.** The user opens
TikTok, finds it in the inbox, writes the caption, picks the cover and publishes.
Never describe a TikTok upload as published.

**Direct post does not work on any of these accounts, and is not a choice we
made.** It was tried on 2026-08-20 and TikTok returned
`unaudited_client_can_only_post_to_private_accounts`: an unaudited client may
direct-post only to an account whose *profile* is private, i.e. the Private
account toggle in Settings. All three of these are public - two Business
accounts and one personal - so all three are refused. Business versus personal
is a different setting and makes no difference here. The post's own privacy level is irrelevant -
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
- **No hashtags in that caption.** The user's decision, 2026-08-21. Print plain
  sentences and stop there - they add the tags in the app, where TikTok's own
  suggestions are live and a tag can be picked against what is actually
  trending that day. A pasted `#drone #sunset` is a guess made hours earlier.
  **TikTok only** - the YouTube description still carries its hashtags, and the
  Instagram and Facebook captions are unchanged.
- **Scopes are `user.info.basic,video.upload,video.publish`.** `video.upload` is
  the draft scope and is the one that matters. `video.publish` is kept only
  because `creator_info` needs it, and that is the only way to read the account
  nickname. A token minted before `video.upload` was added fails the inbox call
  with `scope_not_authorized` and needs a fresh authorisation, not a refresh.
- **Delivery is slow and wildly uneven, and `status` lags behind reality.**
  On 2026-08-20 the identical 5s file reached Crypto Wiki and Tinnitus Help in
  seconds, while `oktay.shakirov` sat at `PROCESSING_UPLOAD` for over an hour
  before the draft appeared - and the status endpoint only caught up afterwards.
  A long `PROCESSING_UPLOAD` means nothing is wrong. All three accounts work,
  including the public personal one. **Never re-run because a draft has not
  shown up yet**: a second run uploads a second copy and there is no API to list
  or delete inbox drafts. Tell the user it may take a while and stop there.
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

## Telegram, on the long form only

**Added 2026-08-23, on the user's instruction.** Both sites' Telegram channels
now get a link post for every long-form video - `@thecryptowiki` and
`@tinnitushelpme`, on the same credentials the article workflows use.

**Long form only.** Shorts stay off Telegram: they already go to Instagram,
Facebook Reels and TikTok, and a channel post for every short is noise. This
matches the "only the long form gets a social share" line in
`video-crypto-long`, which the Reel table does not contradict - a Reel is
distribution, a channel post is an announcement.

**It is a link post, not an upload.** `sendMessage` with title, hook and the
YouTube URL; Telegram unfurls that into its own play card. A native
`sendVideo` would keep the view inside Telegram and off YouTube, and the long
form is 140 MB.

Two places it lives, deliberately:

| What | Crypto | Tinnitus |
| --- | --- | --- |
| Inline, in Publish Facebook Video | `zS3xX6tbXpXnF32N` | `Lyhn5U7pYhrAs9x7` |
| Standalone Share Video To Telegram | `5x8Kaq91qqPl6pmp` | `2WlbdJ1qQ7HKU9m6` |

The inline branch is what makes it "always run with the skill" - pass
`youtubeUrl` as `field-4` to the Facebook workflow and it posts after the video
is live. The **standalone** one exists because the inline branch cannot be
retried: re-running Publish Facebook Video re-uploads the video to the Page.
Its form fields are `title, hook, youtubeUrl` at
`/form/share-video-telegram-{crypto,tinnitus}`.

Use the standalone when the inline branch did not fire, or - the case worth
planning for - when you deliberately hold the announcement until the user has
flipped the video to Public in Studio. Omitting `youtubeUrl` on the Facebook
run skips the branch cleanly, which is what the IF gate is for.

- **`Telegram Post` carries `onError: continueRegularOutput`**, same argument
  as `FB Set Reel Cover`: the Facebook video is already live by then, so a
  Telegram failure must not produce a red execution that invites a re-run.
- `Summary` reports `telegramSent` and `telegramMessageId`. **Read it** - the
  branch failing silently is the whole failure mode here, see below.

## Two n8n traps that both fail silently

Both were hit building the Telegram branch, and neither produces an error.

**An IF node after another node reads *that* node's output, not the form's.**
`Share To Telegram?` was written with `leftValue: {{ $json.youtubeUrl }}` and
sits after `Publish Video`, so `$json` was the Facebook API response and
`youtubeUrl` was simply `undefined`. The condition took the false branch, the
Facebook video published normally, `Summary` reported `telegramSent: false`,
and **nothing anywhere reported an error**. Reference the node by name:
`{{ $('Normalise Input').item.json.youtubeUrl }}`. The same trap applies to any
node reaching back past its immediate predecessor.

**A form workflow's `path` must equal its `webhookId`.** n8n registers the form
route under `webhookId`; the `path` parameter alone is not enough. A workflow
created via the API with a `path` that does not match activates cleanly -
`POST /activate` returns `active: true` - and then serves **"Problem loading
form"** on the URL you asked for. Every shipped workflow here has the two set
to the same string, which is why the older ones carry a UUID-looking `path`
like `b3f2a2c7-1a9a-4c1a-9a0b-fb-video-crypto`: it *is* the webhookId. When
creating a form workflow, set both fields to the same value and probe
`/form/<path>` for a 200 before trusting it.

## The short's two thumbnails are named, and the names are load-bearing

`<name>-thumb.jpg` is the **vertical** Reel cover and `<name>-thumb-yt.jpg` is
the **1280x720** one for YouTube. `bitcoin-price-short.py` was written with the
two the other way round and was caught before the upload, but only by checking:
had it shipped, `-thumb.jpg` would have sent a 9:16 image to YouTube, which is
exactly the silence-pair failure this file already documents - letterboxed
between two blurred zoomed copies, reported as success by both the upload and
the audit. **Check the pixel dimensions of both files before uploading**, not
the filenames.

## The Telegram post is a photo, because the link preview never rendered

**Settled 2026-08-23 after three attempts, and it replaces the advice this
file gave a paragraph earlier the same day.** The original design was a
`sendMessage` link post left for Telegram to unfurl into a play card. It did
not unfurl - not while the video was unlisted, not after it was public, and
not on the `youtu.be` form either. Telegram builds that card by fetching the
URL's OpenGraph tags on its own schedule and caches per URL, and none of that
is under our control. What shipped instead was three lines of text and a bare
link: the weakest post in the channel.

I had written "do not fix this with `sendPhoto`, it trades a play button for a
still". That was wrong on the evidence - **there was no play button to trade**,
because the card never appeared. A photo post always renders, we control the
image, and the caption carries the ask.

So every Telegram node now sends:

- **`sendPhoto`**, with `file` set to
  `https://i.ytimg.com/vi/<id>/maxresdefault.jpg` - YouTube's copy of the
  thumbnail we uploaded with the video. Public, permanent, no tunnel and no
  binary handling. `Normalise Input` pulls the id out of `youtubeUrl` with
  `/(?:v=|youtu\.be\/)([A-Za-z0-9_-]{11})/` so either URL form works.
- **A caption that asks**: title, the hook, and `▶️ Watch the full video: <url>`.
  Captions cap at 1024 characters, which the hook is nowhere near.

**The n8n parameter is named `file`, not `photo`.** The node does
`body.photo = getNodeParameter('file')`, so setting `photo` leaves the file
empty and Telegram replies **"Bad Request: there is no photo in the request"** -
which reads like a bad image URL and is not. Check the node's own definition
in `n8n-nodes-base/dist/nodes/Telegram/Telegram.node.js` before trusting a
parameter name; several of them do not match the Bot API's.

## Never let n8n sign the message

**Every Telegram node appends "This message was sent automatically with n8n"
unless `additionalFields.appendAttribution` is explicitly `false`.** It is the
node's default and the field had never been set, so it had been going out on
*every* channel post on both sites - articles, exchanges, crypto OGs, sound
sessions and now videos. Nine workflows, all fixed on 2026-08-23.

**Set it on any new Telegram node**, and re-check the whole set with one sweep
after adding one:

```
GET /api/v1/workflows?limit=100  ->  for each node of type n8n-nodes-base.telegram,
                                     parameters.additionalFields.appendAttribution
```

Anything not `false` is signing your posts.

## The public API rejects settings keys the n8n UI happily stores

`PUT /workflows/<id>` validates `settings` strictly and 400s with
`request/body/settings must NOT have additional properties` on keys the editor
writes itself - `callerPolicy`, `availableInMCP`, `binaryMode` were the three
that bit. Filter the object to the keys the API accepts before sending:

    executionOrder, saveExecutionProgress, saveManualExecutions,
    saveDataErrorExecution, saveDataSuccessExecution, executionTimeout,
    errorWorkflow, timezone

Omitted keys keep their stored value, so filtering loses nothing. This only
shows up on the older workflows, which is why a script can update four and
then fail on the fifth.

## The site entry is not what notifies the apps

**`npm run sync-content`, in the site repo, after the deploy gate.** Writing
`videos.json` and pushing puts the video on the site; it tells the mobile apps
nothing. The push comes from a Firestore document being *created* in the
`videos` collection, and that script is what creates it.

Missing this is invisible: the video appears on `/videos`, the article carries
its embed, `content-index.json` lists it, and nothing anywhere reports that the
app never heard about it. That is how it went unnoticed on 2026-08-23.

**The command was also broken, and had been all along.** `npm run sync-content`
is a bare `node scripts/syncContent.js`, so it never got the `.env` loading
Next does for `dev` and `build`; it threw `Missing Firebase credentials` and
exited before writing anything. Fixed by loading `@next/env` at the top of the
script. If a future run reports missing credentials, suspect env loading rather
than the credentials themselves.

- **Run it after the deploy gate.** The script deliberately holds back a new
  item whose URL is not live yet instead of writing it silently, because
  `notify` is only set on creation - a silent write would suppress that
  video's notification forever.
- **Re-running is safe.** An existing slug is updated, and an update never
  fires `onDocumentCreated`, so retitling cannot re-notify.
- **Only long form reaches it.** `lib/contentIndex.js` filters
  `kind === "long"`, because only long form has a `/videos/<slug>` page for a
  notification to open. A Short having no registry entry is consistent with
  that, not a gap.
- **It is a fast path, not the only one.** Each app also polls
  `content-index.json` on a schedule, so a missed run delays the push rather
  than losing it. Run it anyway - seconds instead of hours.

