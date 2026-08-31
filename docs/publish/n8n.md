# n8n: traps that fail silently

Every workflow here reports success on inputs it quietly ignored. These are the
ones that have already cost a wrong post.

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

## The inline Telegram branch on Tinnitus Help's Facebook workflow is still broken

**Found 2026-08-26, publishing `tinnitus-myths-vs-reality`.** The Facebook
workflow's `Summary` reported `telegramSent: false`. The `Telegram Post`
node's own output was `{"error": "Bad Request: there is no photo in the
request"}` - the exact symptom this doc already documents under "The
Telegram post is a photo" - but the parameter name was correct
(`file`, not `photo`). The real cause was the *other* documented trap: **`Share
To Telegram?`'s IF condition correctly reads
`$('Normalise Input').item.json.youtubeUrl`, but `Telegram Post`'s own `file`
and `caption` fields still read plain `$json.posterUrl` / `$json.title` /
etc.** - which past the IF node resolves against `Publish Video`'s output
(`{id: "..."}`), not the form's data. The fix recorded as applied on
2026-08-23 only reached the IF node, never the Telegram node downstream of it,
on the Tinnitus Help workflow (`Lyhn5U7pYhrAs9x7`) at least - **check the
crypto workflow (`zS3xX6tbXpXnF32N`) for the same gap before trusting it.**

**Worked around, not fixed, this run:** an attempt to `PUT` the corrected
node (`$('Normalise Input').item.json.X` in place of `$json.X`) was blocked
by the session's own permission classifier as a workflow modification. Used
the **standalone Share Video To Telegram workflow instead** - it has no IF
node between `Normalise Input` and `Telegram Post`, so `$json.posterUrl`
there is already correct, and the send succeeded (message id confirmed in
`Summary`). This is exactly the retry path this doc already names for "the
inline branch did not fire" - it is now also the path for **the inline
branch fired and hit this bug**.

**Do not assume the 2026-08-23 fix landed everywhere it was described.** Pull
the live node's `parameters.file` and `parameters.additionalFields.caption`
before trusting `telegramSent` on any future run; if either still reads
`$json.X` rather than `$('Normalise Input').item.json.X`, the inline branch
will keep failing silently in exactly this shape.

**Confirmed still present on the crypto workflow, 2026-08-26** (publishing
`proof-of-stake`): `Telegram Post` errored `Bad Request: there is no photo in
the request` on the inline branch, same as the tinnitus one.

**Still present 2026-08-31** (publishing `ruja-ignatova`): live `Telegram Post`
node on `zS3xX6tbXpXnF32N` still reads `{{ $json.title }}` / `{{ $json.hook }}`
/ `{{ $json.youtubeUrl }}` / `{{ $json.posterUrl }}` - plain `$json`, which past
the IF node resolves against `Publish Video`'s `{id}` output. Did not trigger
the inline branch at all: omitted `field-4` (youtubeUrl) on the Facebook form so
`Share To Telegram?` took the false branch cleanly, then posted via the
**standalone** `5x8Kaq91qqPl6pmp` (`/form/share-video-telegram-crypto`, fields
`title, hook, youtubeUrl`) - succeeded first try, message id 152. This is now
the default path for the long-form Telegram post: skip the inline branch,
use the standalone. **Fell back to
the standalone workflow, and it also failed once - a genuine `ETIMEDOUT` to
Telegram's IPv6 address, not a workflow bug.** The standalone workflow has no
IF node ahead of `Telegram Post`, so its `$json.posterUrl` is correct by
construction; a second submission of the same form succeeded in 1.2s. **A
timeout on the standalone workflow is safe to retry immediately** - it is
idempotent by design (a fresh `sendPhoto` call, no state to double-write) and
this is a different failure class from the inline branch's silent
parameter bug. Read the execution's own error before deciding which one you
are looking at.
