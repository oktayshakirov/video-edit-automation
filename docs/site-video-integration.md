# Site-side video integration - the plan for Phase 4

Companion to `long-form-strategy.md`, which already settled *why* and *how many*.
This file settles *where the video goes on the site* and *what carries the link
between an upload and a page*. Read the strategy doc's "What the SEO claim is
actually worth" first - nothing here overturns it, and the honest expectations it
sets still apply.

## What exists today

Seven uploads, four crypto and three tinnitus:

| channel | id | len | target |
|---|---|---|---|
| crypto | `cuHZGLligzA` | 3:52 | `/crypto-ogs/michael-saylor` |
| crypto | `Sbxrw7ZFI9o` | 2:47 | `/posts/what-it-actually-takes-to-prove-someone-is-satoshi-nakamoto` |
| crypto | `fvqxbVLa6Mg` | 1:02 | short - Saylor |
| crypto | `xadIOyR6aUo` | 0:35 | short - Satoshi |
| tinnitus | `O5uCEwgOwvM` | 5:00 | sound session - masking + breathing |
| tinnitus | `RR_qU3FA0OY` | 2:40 | `/blog/does-tinnitus-go-away` |
| tinnitus | `VI_CrobXOFk` | 1:01 | short - masking session |

Two things this table already proves, before any code:

**The target is not always a post.** The best-performing crypto long form points
at a `crypto-ogs` page. The component and the registry must address
`posts`, `exchanges`, `crypto-ogs`, `blog` and `zen` - not "the post".

**Titles drift between script and upload.** `satoshi-proof.py` carries
`META.title = "The One Test That Proves Someone Is Satoshi Nakamoto"`; the video
on the channel is titled *"The One Test That Settles Every Satoshi Nakamoto
Claim"*. Any sync that matches a render to an upload **by title will break**, and
it will break silently - see below for the key that does not.

## Decision 1 - a registry, not frontmatter

The strategy doc sketched frontmatter `video: { id, title, uploadDate, duration }`.
Reverse that: the **registry is the source of truth**, frontmatter is at most an
override. Four reasons, all of which bite specifically at volume:

- Mass creation means the alternative is hand-editing MDX frontmatter per video,
  in the repo, for a value (`id`, `uploadDate`, `duration`) that only exists
  *after* upload. That is a second manual step per video, forever.
- The feed pages need a list. A list assembled by globbing 130 MDX files to find
  the six that have a `video:` key is a build-time scan for a 5% hit rate.
- The doc's own "embed one video across several posts" idea is a one-to-many
  relation. Frontmatter can only express it by duplicating the video's metadata
  onto every host page, which then drifts.
- `duration` and `uploadDate` must be **truthful** for `VideoObject`. They belong
  to YouTube, so they should be read from YouTube, not retyped by a human.

### Shape

`crypto-wiki/json/videos.json` (next to the existing `posts.json`, `views.json`)
and `tinnitus-blog/src/data/videos.json`.

```jsonc
{
  "videos": [
    {
      "id": "Sbxrw7ZFI9o",
      "kind": "long",                       // "long" | "short" | "session"
      "title": "The One Test That Settles Every Satoshi Nakamoto Claim",
      "description": "…",                   // first paragraph of the YT description
      "uploadDate": "2026-08-13T00:00:00Z", // from YouTube, never hand-written
      "duration": "PT2M47S",                // ISO 8601, for VideoObject
      "poster": "/images/videos/satoshi-proof.webp",
      "target": { "type": "posts", "slug": "what-it-actually-takes-…" },
      "alsoOn": [ { "type": "posts", "slug": "…" } ],
      "placement": "auto",                  // "auto" | "inline" | "none"
      "chapters": [ { "start": 0, "title": "…" } ],
      "transcript": "videos/satoshi-proof.srt"
    }
  ]
}
```

`kind` matters because the three behave differently on the site (Decision 3).
`placement: "auto"` is what makes volume survivable - the layout renders it in a
fixed slot and the MDX file is never touched.

## Decision 2 - the join key is `Meta.url`, and it already exists

`longform/meta.py:104` writes `f"Full article: {self.url}"` into every generated
YouTube description, and `Meta.url` is documented in the dataclass as "the post
this video came from". So **every upload already carries its target page in its
own public description**, and `youtube-audit videos --channel <ch> --json`
already returns descriptions.

That means the sync is: read the live video list, pull the article URL out of
each description, resolve it to `{type, slug}`, and write the registry. No
per-video bookkeeping file, no title matching, nothing to keep in step.

Where it breaks and what to do:

- **Sessions have no article.** The 5:00 masking video is not derived from a
  page. Give session projects a `url` pointing at the zen page they belong to
  (`/zen/notched-sounds` or similar), or the sync leaves `target: null` and the
  video appears only in the feed.
- **Shorts** are built by the short skills, which may not use `Meta`. Either add
  the same "Full article:" line to short descriptions or accept `target: null`
  for them - which is fine, because shorts are not embedded on articles anyway.
- **A missing or unresolvable URL must fail loudly.** Print it and exit non-zero.
  A silently unmatched video is a video nobody notices is missing from the site.

## Decision 3 - longs embed, shorts do not

This is the recommendation that is not in the original sketch, and it is the one
worth arguing about.

**Long form embeds on its target article.** A 2–4 minute explainer answers the
same question the article does; a reader who would rather watch is served, and
the page keeps them.

**Shorts do not embed on articles.** A 35-second vertical clip on an article is a
trailer for the long video, in a 9:16 box that wrecks the reading column on
desktop. It competes with the real video for the one click, and it adds no
indexable content. Shorts belong on the feed page and on social, which is what
they were made for.

**Tinnitus sessions embed, and they are the exception that matters.** On a zen /
sound-therapy page the video *is* the content - a 5-minute masking bed with a
breathing ring is the thing the visitor came to use. Those pages are the only
ones on either site that plausibly qualify for a video rich result under the
August 2023 rule the strategy doc cites, because video is genuinely the main
content there. Prioritise them.

A session player needs the existing `MedicalDisclaimer` component next to it and
a headphone/volume note. Same YMYL discipline the skills already carry.

### Sessions are many-to-one, and that drives their whole shape

One zen album spawns *many* sessions - a 1-minute, a 5-minute and a 30-minute
cut of the same white noise, with or without a breathing ring. This is the one
place the article model does not transfer, and it decides three things:

- **The lookup returns a list, not a video.** `getAlbumSessions(slug)` for zen;
  `getPageVideo` stays single and now explicitly skips sessions. Several
  registry entries pointing at the same `target` is normal here and a bug
  everywhere else.
- **Sessions carry a `label`.** The page title is already the album name, so a
  card that repeats it says nothing. `label` is the short phrase that separates
  one session from its siblings - `Paced breathing`, not `White noise with
  paced breathing`. Cards show `label` + duration; the full YouTube title is
  only in the schema and the aria-label.
- **Sorted shortest first.** Someone scanning for "the quick one" is the common
  case; upload order is meaningless across cuts of one album.

Shorts stay off zen pages even though a 1-minute masking clip is arguably usable
content - it is 9:16, and a vertical box in a reading column is the thing to
avoid. If those turn out to be wanted, list them on `/zen/videos`, not on the
album page.

## Decision 4 - facade only, and it is a legal point too

The strategy doc already requires a facade with a locally served WebP poster on
Core Web Vitals grounds. There is a second reason: both sites run a German
Impressum. A stock YouTube iframe contacts Google and sets cookies on page load,
before any consent - the facade is also the pattern that makes an embed
defensible. Load `youtube-nocookie.com` and only on click.

Poster images go through the existing `/webp` skill into
`public/images/videos/<slug>.webp`, at 1280×720, with explicit `width`/`height`
so nothing shifts.

## The component

### crypto-wiki (JS, `next-mdx-remote`)

- `layouts/components/PostVideo.js` - the facade card.
- Register in `lib/mdxComponents.js` alongside `ArticleAd`, `ExchangeButton`.
- `layouts/PostSingle.js` renders it in the auto slot; `ExchangeSingle.js` and
  `CryptoOgSingle.js` need the same slot (Saylor is a `crypto-ogs` page).
- `VideoObject` appends to the existing `jsonLd` array - the prop is already
  threaded through `Baseof.js:90`.

### tinnitus-blog (TS)

- `src/components/MDX/PostVideo/` - same card, styled-components.
- Register in the `components` map in `src/components/MDX/index.tsx`.
- `src/ui/pages/BlogPost` gets the auto slot; the zen page gets the session
  player.
- Schema through the existing `JsonLd` component.

### Both - the compact card

The user's ask is "compact somewhere if they just want to watch it", which means
**above the fold, collapsed**. A single horizontal bar directly under the title
meta row:

    ┌──────────────────────────────────────────────────┐
    │ [▶ 160px poster]  Watch: The One Test That…       │
    │                   2:47 · chapters · transcript    │
    └──────────────────────────────────────────────────┘

Click expands it in place to a 16:9 player. It costs ~90px of the hero area,
tells a scanner within one second that a video exists, and costs zero
third-party bytes to anyone who does not click. Sessions get the reverse
treatment - player open by default, because that is the content.

### MDX usage

```mdx
<PostVideo />                      {/* this page's video, at this exact spot */}
<PostVideo id="Sbxrw7ZFI9o" />     {/* someone else's video, explicit */}
```

With `placement: "auto"` in the registry no MDX edit is needed at all - that is
the mass-production path. Setting `placement: "inline"` suppresses the auto slot
so the tag in the body is the only render. `"none"` keeps a video in the feed
without putting it on the article.

## The feed pages

Three surfaces, in descending order of value:

**`/videos/<slug>` - one page per long-form video.** This is the highest-value
piece and it is not in the original sketch. The page carries the player (open),
the chapter list as jump links, and **the SRT rendered as a readable
transcript**. That transcript is 450–700 words of text that exists nowhere else
on the site - the script is written narration, not the article's prose - so this
is not a thin page, and it is a page where video is unambiguously the main
content. Link it back to the source article prominently.

Only long form and sessions get these. Shorts would be thin pages and should not.

**`/videos` - the index.** Grid of poster cards, grouped long / sessions /
shorts. Links to `/videos/<slug>` for the first two, out to YouTube for shorts.

**Home page row.** Three most recent cards under "Latest Posts" on crypto and the
equivalent on tinnitus, linking to `/videos/<slug>` - not to YouTube. Keep the
click on the site; the video page has the player anyway.

Category and tag pages get nothing. Extra surface, no demand.

## Sitemap

`next-sitemap` has no video extension on either site, so add a post-build script
that reads the registry and writes `public/video-sitemap.xml` with
`<video:video>` entries for the `/videos/<slug>` pages, then list it in
`robotsTxtOptions.additionalSitemaps`. Both configs already have that key -
tinnitus uses it today.

`/videos/*` needs a `transform` branch in both configs (priority ~0.8) or the
new routes inherit whatever the catch-all rule gives them. On crypto, the
existing `/^\/[a-zA-Z0-9-]+$/` branch will catch `/videos` at 0.8 already but
not `/videos/<slug>`.

## Schema detail

On an article with an embedded long video, append to the existing graph:

```jsonc
{
  "@type": "VideoObject",
  "name": …, "description": …,
  "thumbnailUrl": "https://…/images/videos/<slug>.webp",
  "uploadDate": …,           // truthful, from YouTube
  "duration": "PT2M47S",
  "embedUrl": "https://www.youtube-nocookie.com/embed/<id>",
  "contentUrl": "https://www.youtube.com/watch?v=<id>"
}
```

On `/videos/<slug>`, add `hasPart` as `Clip` nodes from the chapter list - that
is what feeds key moments. The chapters are already validated by
`meta.check_chapters`, so the data is trustworthy by the time it reaches here.

Do **not** set the article as the video's canonical, and do not expect a video
thumbnail next to the article's blue link. The strategy doc is right about that.

## Build order

Original order was A, C, B. What actually happened: **A, then D**, with C
dropped - see the notes under each.

**A - make the seven current videos work. DONE.** What shipped:

| | crypto-wiki | tinnitus-blog |
|---|---|---|
| registry | `json/videos.json` | `src/data/videos.json` |
| lookup | `lib/videos.js` | `src/lib/videos.ts` |
| component | `layouts/components/PostVideo.js` | `src/components/MDX/PostVideo/` |
| context | `context/video.js` | `PostVideo.context.tsx` |
| registered | `lib/mdxComponents.js` | `src/components/MDX/index.tsx` |
| auto slot | `PostSingle`, `CryptoOgSingle`, `ExchangeSingle` | `src/pages/BlogPost` |
| schema | `videoObjectSchema` in `lib/utils/jsonLd.js` | `videoObjectSchema` in `src/lib/videos.ts` |
| posters | `public/images/videos/*.webp` (29–66 KB) | same |

Verified: facade renders and expands to the nocookie player on both sites;
`VideoObject` present and correct on the two article pages and absent on pages
without a video; **zero requests to any Google origin before the click**; both
production builds and typecheck pass.

Two things the build taught:

**The auto slot goes above the quick-facts table, not below it.** On
`crypto-ogs` and `exchanges` the facts table runs most of a screen, and the
first placement pushed the video far out of sight - which defeats the only
reason the card is compact.

**Clamp the title to two lines.** A four-line title on mobile turns the compact
bar into a 160px block sitting between the reader and the article.

**D - sessions on zen pages. DONE**, and it arrived before B because sessions
turned out to be the more valuable half. What shipped:

- `getAlbumSessions` / `allSessions` in `src/lib/videos.ts`, with `label` added
  to `SiteVideo`.
- `src/components/ZenSessions/` - a card grid, one player open at a time, with
  the partial-masking volume note underneath.
- `src/pages/ZenPost` renders it under the album content and emits one
  `VideoObject` per session.
- `/zen/videos` (`src/pages/ZenVideos/`) - every session grouped by album, as a
  third tab on `/zen` beside Latest and Most popular. `ItemList` of
  `VideoObject`s, `MedicalDisclaimer` at the foot, priority 0.8 in the sitemap.
- `ListingTabs` gained an opt-in `showVideos`; `/blog` is unchanged.

The 5:00 masking session is attached to `/zen/white-noise`, which is the album
its sound came from.

**C - the sync script. Dropped.** At a video every day or two, hand-editing the
registry on upload is cheaper than maintaining a script, and the `_fields` block
inside each `videos.json` documents the shape at the point of editing. Revisit
only if the cadence changes: the design (parse the `Full article:` line out of
the live description) is recorded above and still correct.

**C - the sync script.** `scripts/sync-videos.mjs` in each site repo (or one
script in `video-edit-automation` that writes both): call `youtube-audit videos
--channel <ch> --json`, parse the "Full article:" line, resolve to `{type,
slug}`, fetch and convert the thumbnail, write `videos.json`, fail loudly on any
unmatched video. After this the per-video human cost is *upload, run sync,
commit* - no MDX, no JSON editing. This is the piece that makes "a lot in the
next days" possible.

**B - the feed and the video pages. DONE.**

- crypto: `/videos` (`layouts/VideosList.js`) and `/videos/<slug>`
  (`layouts/VideoSingle.js`), `VideoCard`, a WATCH row plus ALL VIDEOS button on
  the home page, a footer nav link, and a `/videos` branch in the sitemap
  transform at 0.8.
- tinnitus: `/zen/videos` already covered this half; the home page gained a
  Video Sessions button beside Zen Library.
- `videoObjectSchema` now takes `withClips`, emitting `Clip` key moments from
  the chapter list - but **only on `/videos/<slug>`**, where video is the main
  content. On an article the embed is supplementary and Google will not surface
  them.

**Where the transcripts came from, since the SRTs were gone.** The renders had
been cleaned off the Desktop, and re-rendering to recover captions would have
been absurd. The narration is in the project scripts (`SECTIONS[].sentences` -
the script *is* the product, as the strategy doc says) and the chapter
timestamps are in each video's own YouTube description. Joining them gives
chapter title + start + spoken text, which is better than an SRT for a readable
page anyway. All 14 chapter titles matched across the two sources.

**The title-drift warning paid off immediately.** Pairing scripts to uploads by
`META.title` matched Satoshi and silently missed Saylor - the script says "How
One Software Company Bought $35 Billion of Bitcoin", the upload says "Michael
Saylor: The $35 Billion Bitcoin Bet...". Pairing by the article URL in the
description matched both. Use the URL, never the title.

**D - sessions on zen pages.** Tinnitus only. Player open by default,
disclaimer, headphone note. Small, high value, do it as soon as there are three
or four sessions.

## Recommendations beyond the ask

- **Do not embed on all 130 posts, and do not spread a video across neighbours
  either.** The strategy doc caps production at 15–20 videos because YouTube
  suppresses templated volume. This section used to recommend `alsoOn` as the
  way to get page coverage without more uploads; **that was reversed on
  2026-08-16** — a video under a page it does not answer is worse than no video,
  and page coverage was never a ranking input to begin with. `alsoOn` remains
  supported and stays empty. One video, one post: its own.
- **Put the article link first in every YouTube description.** It is currently
  after the hook. `/youtube-audit`'s `set` command can rewrite the existing seven
  in one pass.
- **Count video plays.** Both sites already have a views API
  (`pages/api/views/[type]/[slug]`). A `videos` type reusing it gives real data
  on whether anyone clicks the facade, which is the number that decides whether
  any of this was worth it. Cheap, and it answers Phase 5's question directly.
- **Keep the shorts' vertical aspect off article pages entirely.** Repeating: a
  9:16 box in a reading column is the single easiest way to make the whole
  feature look like an ad.
- **Re-measure at 30 days, per Phase 5.** Two videos per channel is not a
  pattern; do not read the first week's numbers as one.
