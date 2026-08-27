# The publish docs

`/publish-video` carries the order of the job, the platform table and the gates.
Everything platform-specific lives here, once - same rule as `docs/video/`: one
lesson, one doc, never cross-post a summary. See `docs/video/README.md` for the
full policy.

| Doc | What it owns |
| --- | --- |
| `youtube.md` | Upload, metadata, captions, thumbnails |
| `instagram-facebook.md` | The tunnel, Reels, the native Page video |
| `tiktok.md` | The draft, and what stays manual |
| `telegram.md` | The channel post, long form only |
| `site.md` | `videos.json`, the deploy gate, `npm run sync-content` |
| `n8n.md` | Workflow traps that report success and do nothing |

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
