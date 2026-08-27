# TikTok

Shorts only, and always as a draft - the caption and cover are finished by hand
in the app.

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
