# YouTube

Both formats go here, and the long form goes first so the Short's description
can link to it. Driven by the `youtube-audit` skill, which owns the quota
arithmetic and the metadata rules.

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

  What follows from that matrix is the open decision below.

- **The swipe feed is YouTube's own choice regardless.** Even a correctly set
  cover governs the Shorts tab, search and playlists rather than the vertical
  feed, which picks its own frame.
- **A Short's YouTube cover is an open decision, and the build no longer
  settles it.** This is the one place where the build side and this side
  disagree, so read it before uploading a Short.

  What was measured here: uploading the 1080x1920 Reel cover to YouTube is
  actively bad. YouTube letterboxes a 9:16 upload into its 1280x720 slot with a
  **blurred, zoomed copy of the same image either side** - the silence pair went
  live as a narrow strip with "DOES ... NCE" bleeding across the bottom in huge
  soft letters, and the user replaced it by hand. `thumbnails.set` returns
  success either way and `youtube-audit video <id>` reports a `maxres 1280x720`
  entry, so **neither the upload nor the audit can tell you this went wrong -
  only looking at the image can.**

  What changed since: on **2026-08-26 the build stopped producing
  `<name>-thumb-yt.jpg`**, on the reasoning that a 9:16 cover is a platform
  quirk to solve at publish time rather than a second file every short hands
  over unasked. See `docs/video/thumbnails.md`. Three older scripts still emit
  it; nothing written since does.

  So the instruction this doc used to give - upload the 1280x720 - now names a
  file that usually does not exist. **Until that is resolved: upload no
  thumbnail for a Short, and put the vertical file's path in the closing manual
  list for the user to set in Studio by hand.** Per the matrix above, by hand is
  the only route that makes the cover actually display, so nothing is lost that
  the API could have delivered.

  **Two wrong explanations, recorded so they are not re-derived.** First: the
  four earlier Crypto Wiki shorts carry vertical covers that display correctly,
  which was read as proof the API should send 9:16. It was not - the user had
  set those by hand. *An artifact's appearance says nothing about how it got
  there.* Second: a Partner Programme limit was blamed; also wrong, since covers
  work on this 3-subscriber channel when set manually.

## Check a thumbnail's pixel dimensions, never its filename

**A Short's cover is vertical, one file** - `<name>-thumb.jpg` at 1080x1920,
from `render_short_thumb`. Settled 2026-08-26; see `docs/video/thumbnails.md`.

Three older scripts (`crypto-short/bitcoin-price.py`,
`tinnitus-short/can-silence-make-tinnitus-worse.py`,
`tinnitus-short/tinnitus-myths-vs-reality.py`) also emit a 1280x720
`<name>-thumb-yt.jpg`. That predates the rule and is not produced by anything
written since. It is not wrong to upload for those three; it is wrong to expect
it to exist.

**So check the pixels, not the name.** `bitcoin-price.py` was written with the
two files the other way round and was caught only by looking: had it shipped,
a 9:16 image would have gone to YouTube as a 16:9 thumbnail - letterboxed
between two blurred zoomed copies of itself, and reported as success by both
the upload and the audit. Nothing downstream validates aspect ratio.
