# Instagram and Facebook

Both run through n8n workflows and both need the render reachable at a public
URL, which is what the tunnel is for. A Short goes up as a Reel; a long form
goes up as a native Page video. They are different products - see the table in
the skill.

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

**A quiz Short has no `-thumb.jpg`.** Every other format's build step renders
one with `render_short_thumb`; the quiz format's own skill does not, since the
picture is already four drawn cards and a generated headline card would just
repeat the hook. Grab a frame from the finished render instead - a moment with
all four cards on screen and none marked yet reads best as a static cover -
and serve that alongside the mp4 for `<cover>.jpg` above:

```bash
ffmpeg -y -ss <seconds into a fully-populated ask phase> -i <name>.mp4 \
  -frames:v 1 <name>-cover.jpg
```

## The Reel caption

The Publish Reel workflow takes **two** caption fields: `caption` goes to
Instagram, `facebookCaption` (optional) goes to the Facebook Reel and falls back
to `caption` when left blank. They are split because Instagram and Facebook
behave oppositely on links - see below. Write both for the person watching, not
for a crawler. The Reel has no separate title field: the burned-in hook text on
the video is the de-facto title, and the caption's first line is the rest of it.

- **Instagram caption: no links, no URLs, no "read the full article at ...".
  Settled 2026-09-01.** Instagram does not make caption links tappable, and a
  bare URL in the text only signals "this post wants you to leave" - which the
  ranking treats as a negative. Concretely: Facebook longs and shorts kept
  performing well, and it was **Instagram Reels reach that collapsed to almost
  zero** as the captions grew longer and link-heavy versus the short plain-hook
  captions of the first batch. The article link is carried by the **YouTube
  Short's** description and the **Facebook** Reel caption - not Instagram's.
  Don't write "link in bio" either, unless the account's bio link actually points
  at this article; a stale pointer is worse than none.
- **Facebook caption (`facebookCaption`): a link is fine and it *is* tappable.**
  Put the real article URL on its own line at the end, before the hashtags -
  same URL the YouTube Short uses. Everything else below (hook, length, tags)
  applies to both captions; the link is the only difference. If you pass only
  `caption`, the Facebook Reel reuses it and gets no link - acceptable, but
  prefer giving it the link since that half of the audience converts.
- **Keep it short: a hook, one or two sentences, then the tags.**
  - **First line is the hook** - it is the only part most people read, showing
    above the "... more" fold at roughly 125 characters. Make it a curiosity gap
    or a concrete claim, in the video's own voice. No "In this video we..."
    throat-clearing, and do not just retype the burned-in on-screen text.
  - **Body: one or two plain sentences** that pay the hook off and add something
    the on-screen text did not. A wall of text gets skipped and reads as spam.
  - **No engagement bait.** "Comment YES", "follow for part 2", "tag 3 friends"
    are all downranked by Instagram directly. One light, honest prompt ("save
    this if you're mid-cycle", "full breakdown on the channel") is the ceiling,
    and it is optional.
  - **Emoji minimal** - none, or one. A caption sprinkled with them reads as
    automated.
- **Hashtags: 3 to 5, specific, at the end of the caption.**
  - Instagram's own guidance since 2024 is a handful of relevant tags, not a
    block of 20-30. A big pile is the clearest "spam" tell there is and it caps
    reach.
  - Mix one broad, two or three niche, one branded - e.g. `#tinnitus
    #tinnitusrelief #ringingears #tinnitushelp`, or `#crypto #bitcoin
    #cryptoexplained #thecryptowiki`.
  - **Vary them per video.** The identical block pasted on every Reel is read as
    automation and throttled; pick tags that match this specific video's subject.
  - Keep them in the caption, not a first comment - Instagram has said placement
    makes no ranking difference, the caption is simpler, and the workflow has no
    first-comment step anyway.
  - No banned or borderline tags: nothing cure-adjacent on tinnitus, no
    `#followforfollow`, no `#viral`, no `#fyp` (that is TikTok's and it looks
    copy-pasted on Instagram).
- **Facebook's `facebookCaption` is the Instagram caption plus the link line.**
  Do not write a different hook or different tags for it - keep them identical so
  the two posts read as one campaign; only the URL line is added. A video that is
  Instagram-only (over 90s, see below) needs only `caption`.
- **Confirm both caption texts in chat before triggering.** A Reel is public the
  instant it succeeds and there is no dry run - see the Gates section in the
  skill.

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

**`facebookCaption` is field index 4**, added after `durationSeconds` so the
`field-0..3` HTTP indexing stays stable. `Normalise Input` reads it by label and
by `field-4`, and defaults it to `caption` when empty; `FB Reel Finish` sends it
as the Facebook `description` while `IG Create Container` still sends `caption`.
Added 2026-09-01 - the two exports carry this, so if the live workflow predates
it, re-import `publish_reel.json` or add the field by hand (Form Trigger: a
non-required textarea named exactly `facebookCaption`, last in the list).

Two caveats on the older tracked exports: `share_post.json` and `share_og.json`
carry workflow ids that no longer exist live, and `share_video.json` describes
a workflow deleted on 2026-08-20. Do not trust a tracked export's id without
checking it against `GET /workflows`.

| Site | Workflow | formData |
| --- | --- | --- |
| Crypto Wiki | Publish Reel `uIV6956N14pMGMZ5` | `{ videoUrl, coverUrl, caption, durationSeconds, facebookCaption? }` |
| Tinnitus Help | Publish Reel `1GTSF6izfwA1gpig` | `{ videoUrl, coverUrl, caption, durationSeconds, facebookCaption? }` |
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

## The native Page video's cover

**`thumb_url` on `/me/videos` does nothing, and every long form published
before 2026-10-02 went up with an auto-picked frame.** The Graph API's
`/videos` edge has no URL-based thumbnail parameter; it accepts the query
string and ignores it. The fix, added to both Publish Facebook Video workflows
on 2026-10-02, is the pair `FB Fetch Cover` -> `FB Set Video Cover`, which
mirrors the Reel's working pair exactly: fetch the image as binary, then POST
it multipart to `/{video_id}/thumbnails?is_preferred=true`.

**The access log of the publish tunnel is what proved it, and nothing else
could have.** On the `first-bitcoin-transaction` run the `http.server` log
recorded exactly one GET for the long form's thumbnail - the pre-flight
verification curl - while the long mp4 was fetched twice and the short's mp4
and cover three times each for the two Reel legs. Facebook never asked for the
image. The `Publish Video` response body is `{"id": "..."}` and nothing more,
the execution was green, and `Summary` reported no cover field, so **neither
the API response nor the execution status nor the Page's own appearance can
tell you this went wrong.** Compare the matrix in `youtube.md`: an artifact's
appearance says nothing about how it got there.

- **Both new nodes carry `onError: continueRegularOutput`**, same argument as
  `FB Set Reel Cover` and `Telegram Post`: they run *after* the video is live on
  the Page, so a failure there must degrade to "no cover" rather than to a red
  execution that invites a re-run - and re-running Publish Facebook Video
  **re-uploads the whole video to the Page**. `Summary` now reports
  `facebookCoverSet`; read it, because these are the one part of the run that is
  allowed to fail quietly.
- **The cover is read from `127.0.0.1:8765`, not through the tunnel.**
  `Normalise Input` now derives `coverFetchUrl` with the same `localise()`
  helper the Reel uses, for the same reason: this machine's resolver does not
  resolve `*.trycloudflare.com` at all, so n8n fetching the public tunnel URL
  fails outright. It falls back to `posterUrl` -
  `i.ytimg.com/vi/<id>/maxresdefault.jpg` - when no `thumbUrl` was passed, which
  is also what makes a missing cover recoverable later.
- **A cover lost at publish time is never actually lost.** YouTube keeps the
  exact image we uploaded at `i.ytimg.com/vi/<id>/maxresdefault.jpg`, public and
  permanent, and `videos.json` carries every long form's id - so any Page video
  can be given its real cover afterwards by POSTing that URL's bytes to
  `/{video_id}/thumbnails`. The only missing link is the Facebook video id,
  which is reported in `Summary` at publish time and is otherwise recoverable by
  listing the Page's videos and matching on title.

**One latent bug found while fixing this, and fixed with it.** `Telegram Post`
read `$json.title`, `$json.hook`, `$json.youtubeUrl` and `$json.posterUrl`, but
`$json` at that node is whatever ran before the IF - `Publish Video`'s
`{id}`, never `Normalise Input`. So the inline Telegram branch could only ever
have sent an empty `file`, which is exactly the "Bad Request: there is no photo
in the request" failure described at the end of `telegram.md`. All four
references are now pinned to `$('Normalise Input').item.json`. The standalone
workflow was never affected and is still the one to prefer, for the retry
reason given there.

### How to verify a Page video's cover, since every success response lies

**Verified end to end on `1512459030720842` (the `first-bitcoin-transaction`
long form) on 2026-10-02.** The route that works, and the only one that proves
anything:

1. `POST /{video_id}/thumbnails?is_preferred=true` with the image as multipart
   `source` returns `{"success": true}`. **That response is worth nothing** - it
   is the same shape `thumbnails.set` returns on YouTube in every row of the
   matrix in `youtube.md`, including the rows where the cover ends up blank.
2. `GET /{video_id}/thumbnails?fields=id,uri,is_preferred,width,height` lists
   every thumbnail Facebook holds. A freshly published long form has about a
   dozen, all auto-extracted frames, and exactly one should come back
   `is_preferred: true` afterwards.
3. **The `width` and `height` in that listing are also wrong.** Ours reported
   `1920x1080` for an image that is `1280x720`; the auto-extracted frames
   genuinely are `1920x1080`, so the field cannot even be used to tell them
   apart. Download the preferred entry's `uri` and measure the file.
4. **Then compare the pixels.** Mean absolute difference against the thumbnail
   we uploaded was **0.35**, which is jpeg re-encoding noise - the same order as
   the 1.1 measured when `fetch_video_poster` replaced the locally composited
   poster. An auto-extracted frame scored **68.7** against the same image, so
   the two outcomes are not close and there is no judgement call to make.

Steps 2 to 4 need the Page credential, which lives encrypted in n8n. The way to
borrow it without touching a live workflow is a throwaway workflow - webhook ->
HTTP Request with `nodeCredentialType: facebookGraphApi` -> Code to summarise -
created through the REST API, activated, called once, then deactivated and
deleted. **Never add a test node to the real publish workflow to do this**; an
accidental run of that workflow re-uploads the video to the Page.

**A cover set this way is applied to an already-published video.** So the fix
above is also the backfill: any Page video can be given its real cover later
from `i.ytimg.com/vi/<id>/maxresdefault.jpg`, and nothing about the post has to
be re-made. What is *not* recoverable from our side is the Facebook video id of
an older post - `Summary` reports it at publish time and we have never stored
it, so a backfill of the videos published before 2026-10-02 has to list each
Page's videos and match on title.

### The backfill, done 2026-10-02

**All 39 native Page videos across both Pages now carry their real cover**, so
this is history rather than a pending job. What it took, in case it is ever
needed again:

1. **List each Page's videos.** `GET /me/videos?fields=id,title,description,
   created_time` with the HTTP Request node's own pagination
   (`responseContainsNextURL`, `nextURL` from `$response.body.paging.next`).
   38 on the crypto Page, 45 on tinnitus. **A Code node cannot do this** -
   `this.helpers.httpRequestWithAuthentication` is not reachable there and the
   workflow just errors, so the credential has to be used from an HTTP Request
   node.
2. **Match on `title`, and only titled videos are native videos.** A Reel has no
   `title` - its caption is the `description` - so the titled subset *is* the
   native-video subset. 17 of the 38 crypto Page videos were titled, and all 17
   matched a registry entry exactly; the same for 22 of 45 on tinnitus. No title
   matched two videos.
3. **Covers come from `i.ytimg.com/vi/<id>/maxresdefault.jpg`**, which resolved
   for all 38 - no `sddefault`/`hqdefault` fallback was needed, though the script
   checked for one.

**Two long forms are deliberately not in that count.** `rug-pull` and
`what-is-a-crypto-whale` have no native Page video at all - they reached the
crypto Page only as Reels, whose covers the Reel workflow already sets. A
registry entry is not evidence that a video was posted to the Page.

**The four tinnitus sound sessions are in it.** They are `kind: "session"`, not
`"long"`, but they are native Page videos with titles and registry entries, so
they were included. Filtering a backfill on `kind === "long"` would silently
skip them.

**The verification, for all 38:** mean absolute pixel difference against the
exact image sent was **0.00** on every one - Facebook serves back the bytes it
received, so there is no re-encode noise to allow for when the comparison source
is the same `maxresdefault.jpg` that was uploaded. The 0.35 recorded above came
from comparing against the local Desktop jpeg, which is a different encode of
the same picture. Either way the contrast with an auto-extracted frame (68.7) is
not close.
