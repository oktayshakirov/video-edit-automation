# The site entry

Long form only. A Short has no `/videos/<slug>` page for a notification to open,
so it takes no registry entry - that is consistent with the design, not a gap.

## The order, and where the registry lives

| Site | `videos.json` | Poster |
| --- | --- | --- |
| thecrypto.wiki | `~/Coding/crypto-wiki/json/videos.json` | `public/images/videos/<slug>.webp` |
| tinnitushelp.me | `~/Coding/tinnitus-blog/src/data/videos.json` | `public/images/videos/<slug>.webp` |

The two paths are different. Check which site before writing anything.

1. **Fetch the poster, do not render one.**
   `fetch_video_poster(out, video_id)` in `video_automation/longform/thumb.py`
   downloads `i.ytimg.com/vi/<id>/maxresdefault.jpg` and converts it to WebP.
   YouTube composites any uploaded thumbnail into 1280x720 itself, so building a
   letterboxed composite locally was solving a problem that did not exist - it
   was measured pixel-identical to the CDN image to 1.1 mean difference, which
   is re-encoding noise. Removed 2026-08-19.
2. **Write the registry entry.** The field-by-field shape, the `target` join key
   and the chapter format are in `docs/site-video-integration.md`, which is the
   reference for the schema - do not re-derive it here.
3. **The deploy gate.** Pushing the site is confirmed in the chat it happens in,
   every session. See the skill's Gates section.
4. **`npm run sync-content`, after the deploy is live.** Details below.

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
