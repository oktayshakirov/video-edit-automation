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

## The Reel caption

One `caption` field, passed to **both** Instagram and Facebook by the Publish
Reel workflow. Write it for the person watching, not for a crawler. The Reel has
no separate title field - the burned-in hook text on the video is the de-facto
title, and the caption's first line is the rest of it.

- **No links. No URLs. No "read the full article at ...". Settled 2026-09-01.**
  Instagram does not make caption links clickable, and a bare URL in the text
  does nothing but signal "this post wants you to leave" - which the ranking
  treats as a negative. The early Reels on the crypto and tinnitus accounts were
  a line or two of plain hook and did well; reach fell off as later captions got
  longer and link-heavy. The article link lives on the **YouTube Short's**
  description and nowhere else in the short's distribution. Do not write "link in
  bio" either, unless the account's bio link actually points at this article - a
  stale pointer is worse than none.
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
- **The same caption goes to the Facebook Reel.** Facebook Reel captions are
  equally dead for links, so the no-link rule covers both. A video that is
  Instagram-only (over 90s, see below) still follows these rules.
- **Confirm the exact caption text in chat before triggering.** A Reel is public
  the instant it succeeds and there is no dry run - see the Gates section in the
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
