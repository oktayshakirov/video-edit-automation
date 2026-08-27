# Telegram

A link post to each site's channel, long form only. Shorts stay off Telegram:
they already go to Instagram, Facebook Reels and TikTok, and a channel post per
short is noise.

## Telegram, on the long form only

**Added 2026-08-23, on the user's instruction.** Both sites' Telegram channels
now get a link post for every long-form video - `@thecryptowiki` and
`@tinnitushelpme`, on the same credentials the article workflows use.

**Long form only.** Shorts stay off Telegram: they already go to Instagram,
Facebook Reels and TikTok, and a channel post for every short is noise. Only the long form gets a
social share of this kind, which the Reel table does not contradict - a Reel is
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
