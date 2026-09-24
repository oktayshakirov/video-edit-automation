---
name: video-views-audit
description: Pull and review how the user's videos are performing on every platform - YouTube (Shorts and long-form, with per-second retention curves), TikTok, Instagram Reels and Facebook - for the drone, Crypto Wiki and Tinnitus Help channels. Use whenever the user asks how a video or a channel is doing, wants views checked anywhere, wants a title, description, tags or thumbnail reviewed or rewritten, wants to know what is working and what is not, or runs /video-views-audit. Also use when they name one of their videos or paste a URL of their own and ask what to change, and when they want a metadata change applied. It can edit YouTube metadata and upload new videos with their thumbnails, but never deletes, and it is read-only everywhere else. For the recurring fortnightly review with snapshots and experiments use video-performance-review, which drives this skill; for the full publish sequence use publish-video.
---

# Video views audit

**How the videos are actually doing, on every platform they are published to.**
Fetch real numbers before giving any advice - never speculate about performance
that has not been pulled.

Renamed from `youtube-audit` on 2026-09-24. YouTube was never the whole
picture: on the 2026-09-21 review, Facebook carried the long-form (~145-200
views a video against 0-13 on YouTube) and TikTok carried the Shorts (~8,200
plays on tinnitus against ~2,000 on YouTube). An audit that reads only
YouTube reads the smallest platform of the three.

| | YouTube (`--channel`) | TikTok | Instagram | Facebook |
| --- | --- | --- | --- | --- |
| Tinnitus Help | `tinnitus` | `@tinnitushelp.me` | `tinnitushelp.me` | `TheTinnitusHelp` |
| Crypto Wiki | `crypto` | `@thecrypto.wiki` | `thecrypto.wiki` | `thecryptowiki` |
| Drone (Drone Pal) | `drone` | - | - | - |

Handles are in each site's footer (`~/Coding/tinnitus-blog`,
`~/Coding/crypto-wiki`) if they ever change.

**Scope.** YouTube is read *and* write (metadata edits, uploads - see "Editing
metadata"). **Every other platform is read-only**: never like, comment,
follow, post, or change a setting. The browser work runs in the user's own
logged-in Chrome (`claude-in-chrome`); close every tab opened.

## Pick the platform by the question

| the question | pull |
| --- | --- |
| "how is this video doing?" | every platform it was published to - the answer differs by 10x between them |
| "why did people stop watching?" | **YouTube `retention`** - the only per-second curve available anywhere |
| "is the title working?" | YouTube views + TikTok plays; CTR is unavailable everywhere |
| "how is the channel doing overall?" | all four, and compare against the last `video-performance-review` snapshot |
| "should I change this title/description?" | YouTube `videos`/`audit`, then "Editing metadata" |

## YouTube - the CLI

CLI at `~/Coding/youtube-audit` (the repo keeps its name; it is a YouTube Data
and Analytics API tool). Run from that directory, and use `npx tsx src/cli.ts`
rather than `npm run yt` when capturing JSON - npm prints a banner that
corrupts the output.

```bash
cd ~/Coding/youtube-audit && npx tsx src/cli.ts <command> [options]
```

| Command | Purpose |
| --- | --- |
| `channels` | Which channels exist and which are authorised |
| `whoami` | Confirm which channel is authorised |
| `videos` | All videos: title, description, views, likes, comments, duration, thumbnails |
| `analytics` | Per-video watch time and retention for a date range |
| `video <id\|url>` | Everything about one video |
| `retention <id\|url>` | Audience-retention curve - **where** a video loses people |
| `audit` | videos + analytics + heuristic flags - the usual starting point |
| `set <id\|url>` | Edit title / description / tags - dry run unless `--apply` |
| `upload` | Upload a video with its thumbnail - dry run unless `--apply` |

Options: `--channel <key>`, `--json`, `--thumbs`, `--all-res`, `--days <n>`, `--start`/`--end`,
`--since <YYYY-MM-DD>`, `--no-shorts`, `--shorts-only`, `--public-only`, `--limit <n>`.
Edit options: `--title`, `--description`, `--description-file`, `--tags`, `--add-tags`,
`--language`, `--category`, `--apply`. See "Editing metadata" below before using any of them.

**Always pass `--channel` explicitly.** With more than one channel authorised the CLI
refuses to guess, and a number pulled from the wrong channel is worse than no number.

**Loop over channels or ids through `bash -c '...'`, not zsh** - zsh does not
word-split `set -- $pair`, so every call silently gets an empty id and the
whole loop returns nothing.

If it reports "Not logged in", tell the user to run

```bash
cd ~/Coding/youtube-audit && npm run yt -- login --channel <key>
```

themselves - it opens a browser for Google consent and cannot be completed
non-interactively. They must pick the right channel on Google's account chooser;
whatever they pick is what gets stored under that key. Verify afterwards with
`whoami --channel <key>` before trusting any numbers.

## TikTok - per-video stats from each video page

Open `https://www.tiktok.com/@<handle>`, let it load, scroll a few times, then
run in the page:

```js
const ids=[...new Set([...document.querySelectorAll('a[href*="/video/"]')].map(a=>a.href.split('/video/')[1].split('?')[0]))];
const rows=[];
for (const id of ids){ try{ const h=await (await fetch(`/@x/video/${id}`)).text();
  const d=JSON.parse(h.match(/<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>([\s\S]*?)<\/script>/)[1]);
  const it=d.__DEFAULT_SCOPE__['webapp.video-detail'].itemInfo.itemStruct;
  rows.push([it.author.uniqueId, new Date(it.createTime*1000).toISOString().slice(0,10), it.stats.playCount, it.stats.diggCount, it.video.duration].join('|')); }catch(e){} }
rows.sort().join('\n')
```

- The grid thumbnails often do not paint in a background tab; the links are
  there anyway, which is why this reads the video pages rather than the grid.
- **Filter on `author.uniqueId`.** The page can carry the *other* account's
  links, and after navigating between two profiles the SPA can keep the first
  profile's grid - if the ids look wrong, `location.reload()`.
- **TikTok rate-limits after ~3 profile loads** ("Something went wrong"). Get
  each profile right the first time; if it trips, keep what was captured and
  say which days are missing rather than retrying in a loop.
- Follower count: `[data-e2e="followers-count"]`.

## Instagram - the reels grid

Open `https://www.instagram.com/<user>/reels/`. The grid is lazy: scroll to 0,
wait ~6s, scroll to 400, wait, then to the bottom a few times. Each
`a[href*="/reel/"]`'s `innerText` is the play count; dates come from
`fetch('/reel/<id>/')`, whose HTML contains "on <Month> <D>, <YYYY>".

- **Return plain arrays**, not strings joined with `=` or `;` - the tool blocks
  output that looks like cookie or query-string data.
- The `web_profile_info` API is blocked; do not bother.
- **A run of reels at exactly 0 plays means distribution has stopped**, not low
  interest. Ask the user to check Settings -> Account Status in the app; the
  web cannot see it.

## Facebook - the videos tab, not the reels tab

Open `https://www.facebook.com/<page>/videos` and read the main region's text:
each entry is `duration | title (long-form only) | age | N views`.

- **The /reels tab mixes Reels and long-form.** On 2026-09-21 that was misread
  as all-Reels and the long-form numbers were reported as Reels. Use `/videos`
  and split by duration - a Reel has no title line and runs under ~1:30.
- Only the recent ~10 load in a background tab. Older all-time hits (a zen
  session at ~29k) are best asked of the user, or read from Professional
  dashboard -> Content with the page's admin profile.
- Follower counts are in the page header.

## What the cross-platform numbers have already shown

From the 2026-09-21 review - re-check rather than assume, but start here:

- **Facebook is the long-form platform.** The same long-forms take ~145-200
  views there against 0-13 on YouTube, and a sound session reached ~29k.
  Crypto's Facebook page has 447 followers against 4 YouTube subscribers.
- **TikTok is the biggest Shorts platform** and every upload lands at almost
  exactly **~250 or ~770 plays** - its test batches. Nothing has escaped them
  yet, so a video clearing ~1,000 is the first real signal and worth studying.
- **Instagram tinnitus went to 0 plays** from 2026-09-14 with account status
  clear. Zero is a distribution stop, not weak content.
- **Every YouTube Short loses 13-27 points at ~5s**, which is what the opening
  hook and the opener variants exist to fix (`E1`/`E5` in
  `video-performance-review/experiments.md`).
- **Record which opener each video used** (redacted hook, Counter, Stamp,
  Split, Search, Flash) when reporting on a new video - it is read from the
  build script's `opener=`/`hook=`, and the variants cannot be compared
  without it.

## Comparisons are only honest within a platform

A Short's retention percentage, a TikTok play and a Facebook view are three
different things counted three different ways. Never put them in one ranking.
Compare a video against **its own platform's** history, and when reporting
across platforms give each its own row.

## Channel context — drone

- Focus is **2026-onwards drone videos**. Everything before 2026 is old, private and
  irrelevant — filter with `--since 2026-01-01`.
- Long-form and Shorts are different products. Default to `--no-shorts` unless asked.
  Never let Shorts into a baseline used to judge long-form.
- Start with:
  `npx tsx src/cli.ts audit --since 2026-01-01 --no-shorts --public-only --start 2026-01-01 --thumbs --json`
  Use a lifetime range (`--start 2026-01-01`) rather than the 90-day default, so older
  uploads are not judged on a truncated window.

## Channel context — crypto and tinnitus

Both are **new channels started in 2026**, Shorts-first, and produced by the
`video-crypto-short` and `video-tinnitus-short` skills. Treat everything about them as
unsettled: there is no agreed title template, no thumbnail system, no proven format.
Nothing in the drone section above carries over — different audience, different
product, different retention curve.

- Use `--shorts-only` for these. A Short's watch-time percentage is not comparable to
  any long-form number, so never mix them into one baseline or one comparison table.
- With only a handful of uploads, **do not rank videos or declare winners**. The
  baseline is suppressed below 5 videos with data for exactly this reason. Report what
  each video did, say the sample is too small to infer a pattern, and stop there.
- Start with:
  `npx tsx src/cli.ts audit --channel crypto --shorts-only --public-only --start 2026-01-01 --json`
  (same for `--channel tinnitus`).
- What is worth looking at this early: whether the hook survives the first 3 seconds
  (retention), whether titles carry the search term a person would actually type
  ("tinnitus masking sound", not a clever phrase), and whether the description links
  back to tinnitushelp.me / thecrypto.wiki. Say plainly when a question needs more
  uploads before data can answer it.
- **Tinnitus content is health-adjacent.** Do not propose titles that promise a cure,
  a fix, or relief, however softly. Describe what the video is.
- As conventions get settled for these channels, record them here the way the drone
  section records its own — but do not invent them retroactively from three videos.

### Settled on 2026-09-02 — one article link per long-form description

Every long-form description the pipeline generated carried the article URL
**twice**: a `Full article: <url>` line before the fold and a descriptive
`<phrase>: <url>` line after the chapters. YouTube renders that as a duplicate
link and it reads as sloppy. Fixed at the source in
`video-edit-automation/video_automation/longform/meta.py` (`Meta.description`
now emits the link once, using the descriptive phrasing) and swept across all 14
live long-form videos (7 crypto, 7 tinnitus) on 2026-09-02 via `set --apply`.
If a future audit finds a long-form description with the same URL on two lines,
it regressed — check that `meta.py` still folds `cta` into the top line.

### Settled on 2026-08-23 — the Shorts metadata baseline

Applied to all nine Shorts across both channels in one pass. Every new Short should
ship this way, and the `video-crypto-short` / `video-tinnitus-short` skills should
generate it rather than leaving it to a later audit:

- **`#shorts` goes at the end of every Short title.** The one Short that already had it
  was also the best performer at the time. That is one data point, not proof — it was
  adopted because it costs nothing, not because it was measured.
- **A Short's description must carry the real article URL**, not the bare phrase
  "Read more on thecrypto.wiki". Take the URL from the corresponding long-form video's
  `Full article:` line so the two never drift apart.
- **A Short links to its long with a trailing `Full video: https://youtu.be/<id>` line.**
  `upload --related` already does this; Shorts published without it need it added.
- **Tinnitus sound-therapy Shorts link to `https://tinnitushelp.me/zen`** — the hub page
  with the sessions on Spotify, Apple Music, YouTube Music, Amazon Music and Deezer.
  Sound-therapy videos have no source article, so do not invent a blog slug for them.
- `wFxUpwnIoI8` (Does Silence Make Tinnitus Worse?) was deliberately left untouched as
  the control. Do not edit it while this baseline is being tested.

### Audit 2026-09-01 — first read on the Tinnitus Shorts

Channel at 533 lifetime views, 4 subs, 8 Shorts + 7 longs, all published 2026-08-09 to
08-28. Sample still too small to rank, but the spread is wide enough to note direction.
Impressions/CTR unavailable as always, so "reach" below means view count, not clicks.

- **Reach: `wFxUpwnIoI8` "Does Silence Make Tinnitus Worse?" 220 views, retention 120%
  (loops).** Nothing else broke 55. Second was `NOJe3xgDNno` (AirPods) at 53 with 34%
  retention, then `Khi1L24OWYk` (night) 36 / 37%. `roCw_ra04XY` (gaming headset) got 2.
- **The pattern that worked: a counter-intuitive myth-flip the viewer can feel.**
  "Silence" and "Are These Tinnitus Myths True?" (retention 76%) both open by naming a
  thing the sufferer already believes and then overturning it. These are the two best
  retention Shorts that also got distribution.
- **The pattern that failed: safe-listening decibel math.** AirPods (34%), gaming
  headset (2 views), gaming long (27%) all lecture prevention-minded people with
  numbers. Wrong audience for this channel (sufferers, not the not-yet-affected) and
  the hook is a figure, not a feeling. De-prioritise dB-budget topics until the base
  is bigger.
- **The `Why Is Tinnitus Worse at Night?` Short (37%) underperformed its own long-form
  `How to Sleep With Tinnitus` (104 views).** Rare case where the long won. The long
  title leads with the actionable phrase ("How to Sleep With Tinnitus") people search;
  the Short leads with the question. Both retention numbers are poor though (long 11%).
- **`RR_qU3FA0OY` "Does Tinnitus Go Away?" is 2:40, 16:9, chaptered — a long-form the
  duration heuristic mislabels as a Short.** Keep it out of any Shorts baseline.
- Metadata hygiene is actually fine across the Shorts: `#shorts` in every title, real
  article URL or `/zen` in every description, `Full video:` cross-link present. The
  one cosmetic drift is `Q--p9uQAEvY` opening with "Read more on tinnitushelp.me:"
  instead of "Full article:", and mixed categoryId (27 vs 26) - neither worth a write.
- **Do not chase title rewrites on the low-retention Shorts.** Their titles are fine,
  searchable questions; the loss is in the first 3 seconds of the video, which is a
  `video-tinnitus-short` hook problem, not an audit problem. Diagnosed precisely on
  the caffeine Short 2026-09-11 (181 views, 20% retention, avg watch stopped one
  sentence before the payoff) and fixed at the source: `narration.md` in
  `video-edit-automation/docs/video` now has "The payoff belongs in sentence two,
  not behind a setup," which both `video-tinnitus-short` and `video-crypto-short`
  read before writing. An audit that finds another low-retention Short should check
  the script against that rule before proposing anything else.
- **Retention over 100% is a loop, and the ending line is why.** Reading every
  shipped Short's closing line against its retention (2026-09-11) split almost
  perfectly: every Short ending on an engagement question ("what do you
  think", "who do you blame") sits at 34-56%; every Short ending on a flat
  statement or a directive ("save this", "get it looked at") sits at 82-152%.
  Also fixed at the source: `narration.md` has "A Short's ending loops; it
  does not ask." When an audit finds a Short over 100%, check its closing line
  before crediting the topic or the title - the loop is very often doing the
  work.

### Notes for `video-tinnitus-short` (from the 2026-09-01 audit)

1. Lead topic selection with **"a belief the sufferer holds that is wrong"** - silence
   helps, it's permanent damage, nothing can be done, quiet rooms are safer. That
   framing is the channel's one demonstrated hit.
2. **First line must name the feeling, not a statistic.** "You get somewhere quiet and
   the ringing gets louder" beat "every three decibels halves your safe listening time".
3. Keep dB / safe-listening / gadget-blame topics (AirPods, gaming headsets) on the
   back burner - they pull the wrong viewer and retention craters.
4. Competitor tells - see "Competitor teardown 2026-09-04" below for the real
   numbers. Short version: Treble Health puts the **search keywords in ALL CAPS**
   inside a plain spoken question ("Why is my TINNITUS LOUDER IN ONE EAR?") and clears
   1.5-4.5k views a Short; device reviews (Lenire) are their runaway long-form. The
   evergreen viral Short in the niche is the **skull-thumping / "Reddit finger-drumming
   trick"** - worth one honest explainer (what it is, why it works = manual masking,
   relief is temporary).

### Audit 2026-09-02 — first read on the Crypto Wiki Shorts

Channel at 238 lifetime views, 3 subs, 8 Shorts + 8 longs, published 2026-08-09 to
08-31. The two newest Shorts (OneCoin, Quantum, both 08-31) had no retention data yet -
judge them again after a week. Same sample caveat as tinnitus: too small to rank.

- **Reach + retention hit: `xadIOyR6aUo` "How Would You Prove You're Satoshi
  Nakamoto?" - 52 views, 82% retention.** The only Short that both got distribution and
  held it. Its long-form sibling `The One Test That Settles Every Satoshi Nakamoto
  Claim` (35 views / 58%) is also the best long. **Identity / unsolved-mystery /
  "could you actually prove it" is this channel's demonstrated topic.**
- **Reach without retention: the ownership/power Shorts.** `Whales Move Bitcoin's
  Price` 44 views / 48%, `The Man Who Owns 4% of All Bitcoin` 37 / 41%. The
  "who secretly controls / who really owns" hook earns the click and then the payoff
  (an order-book mechanism, a balance sheet) underwhelms. Tighten the first 3 seconds
  or pick a punchier reveal.
- **Concept explainers (Proof of Stake 9v/68%, Coinbase-vs-Uniswap 12v/53%) are
  low-reach, OK-retention.** These are search plays that accrete slowly, not browse
  plays. Fine to keep making, do not expect a spike.
- **`PH8SBxjTA6M` "The $2 Mining Rig Part That Starts Fires" - 122% retention, 3
  views.** Content works, distribution didn't. Pure reach miss.
- Retention across the Shorts that *do* get reach sits at 41-53% - the mirror image of
  tinnitus, where the hit retained 120%. Only the Satoshi Short cleared both bars.
- Metadata hygiene mostly clean: `#shorts` in every title, real article URL in every
  description, `Full video:` cross-link present, all categoryId 27. Two gaps:
  `djk5GxqTag8` (Whales) and `nffdeYs5_Jo` (Coinbase) shipped with junk tags
  (`crypto, education, finances`) - flagged `few-tags` - and `nffdeYs5_Jo`'s title
  carries a filler `(Here's Why)` that trips `title-too-long`. Dry-runs prepared
  2026-09-02, awaiting approval.
- **Every pair is same-day with near-identical titles**: OneCoin, Quantum, Proof
  of Stake all short+long same day. The same-day timing is not the problem; the
  reworded long-form titles are - see "Same-day near-identical pairs
  underperform" below.

### Notes for `video-crypto-short` (from the 2026-09-02 audit)

1. **Lead with a mystery or an "could you prove/do it?" challenge.** Satoshi is the one
   topic that both reached and retained. Unsolved-identity, missing-money, and
   who-really-did-it framings beat "what is X".
2. **Scam / fraud stories are a proven viral lane in this niche** (OneCoin, FTX get
   millions elsewhere). The OneCoin Short is a good instinct. Same-day publishing
   with its long-form is fine - just make sure the long-form's title is a real
   search ("what was the OneCoin scam", "how did OneCoin collapse") and not the
   Short's hook reworded. See "Same-day near-identical pairs underperform" below.
3. **The "who controls / who owns" hook clicks but doesn't hold.** If you use it, the
   3-second payoff has to be a sharp visual or number, not a paragraph of mechanism.
4. **Add one concrete analogy per concept.** Whiteboard Crypto (~1M subs, the direct
   comparable) runs entirely on this: AMM = vending machine, private key = vault
   combination. The crypto-wiki Shorts explain mechanisms literally and analogy-light -
   this is the cheapest copyable upgrade.
5. Generate real search-term tags at build time (the Whales and Coinbase Shorts went
   out with three generic words).

### Same-day near-identical pairs underperform - it is the title, not cannibalisation

**The observation stands:** when the pipeline ships a Short and its long-form on
one topic the same day with near-identical titles, the Short takes almost all
the views and the long-form lands at 0-12. On 2026-08-23 the Short took 188
views and the long took 1. Every pair on both channels through the 2026-09-02
audit is same-day, and every long-form except one is in that band.

**The cause is not algorithmic cannibalisation.** YouTube runs Shorts and
long-form on separate ranking systems (different candidate generation and
serving infrastructure) and evaluates per video, not per channel - a weak Short
does not drag down the next long-form, and the Shorts feed actively surfaces a
channel's recent long-form to people who watched its Shorts. What actually
happens on a 3-week-old channel: every Short gets a small automatic push from
the Shorts feed, while a brand-new long-form gets almost no browse or suggested
impressions and has to win on search - so the Short is not taking views the
long-form would otherwise have had. The one long-form that beat its Short
("How to Sleep With Tinnitus", 95 to 36) has a title matching a real
high-volume evergreen search; the losing ones have curiosity titles nobody
searches ("Who Controls Bitcoin's Price? Not Who You Think").

**The fix is the long-form title**, not spacing. It must be a phrase people
type into YouTube search, on a different query angle from the Short (YouTube
rarely shows two videos from one channel on a single results page, so a
different angle also sidesteps the one real same-channel effect). The build
skills now bind this to the `Meta` title. An audit's job is to catch a
long-form title that is the Short's hook reworded and propose the searchable
version. Separating the two uploads by a day or two is optional polish with no
evidence behind it - mention it as an option, never require it.

## Competitor teardown 2026-09-04

Pulled via YouTube RSS (`feeds/videos.xml?channel_id=`) - gives the last 15 uploads
with real view counts, but **excludes most Shorts** and shows no retention. Directional,
not a full picture. Channel grids do not render in the headless browser here, so RSS is
the best available route; redo it the same way next audit.

### Tinnitus

**Treble Health** (`UCuH8CgFikmhRc2ALsI0j4uQ`, ~200k subs) - the category leader.
- Shorts land **1.5k-4.5k views each**. Title format is a plain question a patient
  would ask with the **search terms in ALL CAPS**: "Why is my TINNITUS LOUDER IN ONE
  EAR?", "Can EARWAX BUILDUP cause tinnitus", "Random TINNITUS SPIKES explained!",
  "Does NOTCHED MUSIC THERAPY work for TINNITUS?". No cleverness, pure search intent.
- Long-form runaway: **"Lenire Tinnitus Device: An Honest Review (2026)" - 64k views**,
  plus a Lenire unboxing and "The BEST Tinnitus Treatments of 2026 (And The WORST...)".
  Device reviews and ranked "best/worst treatments" are the long-form engine.
- "Does Tinnitus Cause Dementia? What the Research ACTUALLY Shows" (5.5k) - the
  health-scare question answered soberly. Same family as our "Silence" hit.

**Sound Relief Tinnitus & Hearing Center** (`UCLS1H0fJxJO2Fg7D6BY3sNQ`).
- Long-form sound-therapy audio is the giant: **"BEST Mountain Stream Sounds for Deep
  Sleep & Tinnitus Relief | No Ads | 10 Hours" - 44k views.** We have `/zen`; a couple
  of genuine multi-hour sound beds on YouTube itself (not just links out) is a proven
  play.
- Patient-transformation format: "Liam's Tinnitus Score Dropped From 47 to 5: Here's
  How" (9.7k), "Menopause Caused My Tinnitus, Here's What Research Says" (5.7k).
- "Are Earplugs Making Your Tinnitus Worse?" (1.7k) - counterintuitive, our lane.

**What to recreate (tinnitus):** (a) retitle to the Treble Health pattern - plain
patient question, keywords capitalised; our "Why Does Tinnitus Spike?" got 26 views
while their "Random TINNITUS SPIKES explained!" got 4.5k and Sound Relief's spike video
got 6.5k, so the topic works and the packaging is the gap. (b) A "Does tinnitus cause
X?" health-question Short (dementia, hearing loss, brain tumour) answered honestly.
(c) One real long sound-therapy bed hosted on the channel. (d) The finger-drumming
explainer.

### Crypto

**Whiteboard Crypto** (`UCsYYksPHiGqXHPoHI-fm5sg`, ~1M subs) - RSS shows long-form only.
- Biggest recent hits are **named-entity + "scam or opportunity?"**: "The Pi Network &
  Pi Token - A Daily Clicking Scam or HUGE airdrop?" (113k), "TRUMP Coin & MELANIA
  Memecoin (Explained with Animation)" (62k), "Earn Crypto With Political Predictions -
  Polymarket Explained" (42k). Evergreen mechanics videos (BIP39 seed phrases, liquid
  staking) sit at 25-40k.
- Every title ends **"Explained with Animation(s)"** and every concept gets one
  concrete analogy. That is the whole channel.

**Coin Bureau** (`UCqK_GSMbpiV8spgD3ZGloSw`, ~2.7M subs) - news, not evergreen, but the
title mechanics are the lesson: one word in ALL CAPS carrying the emotion + a named
antagonist + a stake. "Germany Is Coming For YOUR Bitcoin." (29k), "The Financial
System Is BREAKING. Bitcoin Isn't." (85k), "The Real Reason Bitcoin EXPLODED Today"
(112k). Barely posts Shorts.

**What to recreate (crypto):** (a) the **"[named token/person] - scam or the real
thing?"** format - it is the single highest-view pattern in the niche and it is a
myth-flip, which is also what worked for us (Satoshi). Candidates from thecrypto.wiki
back-catalogue: any OG profile, any dead project. (b) Put ONE analogy in every Short's
first line the way Whiteboard Crypto does (private key = vault combo, validator stake =
security deposit). (c) Steal Coin Bureau's caps-one-word title punch for our Shorts:
"Quantum Computers Can't Break Bitcoin. YET." over "Can Quantum Computers Break
Bitcoin?".

## Use the retention curve — it is the difference between measuring and guessing

```bash
npx tsx src/cli.ts retention <id|url> --channel tinnitus --start 2026-01-01
```

Prints watch-share at each point in the video, the change between samples, the
three steepest drops and where half the opening audience is gone. `--json` for
the raw points.

**This is now the first thing to reach for on any retention question**, because
an average tells you a video lost people and the curve tells you at which
sentence — and on every video compared so far those two have pointed at
different places. The caffeine Short's average (20.3% of 57s ≈ 11.6s) suggested
viewers drifted off around sentence three; the curve showed 100% still present
at 4.6s and half gone by 6.3s, i.e. a cliff at the *end of sentence two*. Same
video, different conclusion, and only one of them was right.

**How to read one:**

- **Map drops onto the script, not onto the footage.** Time the narration at
  3.25 words/sec plus the written gaps and find which sentence the cliff lands
  on. The `video-*` build skills keep every script as a `SENTENCES` or
  `SECTIONS` list, so this is exact rather than approximate.
- **Above 100% is replays, not a bug.** A looping Short is counted again, so a
  good Short *opens* high — "Does Silence Make Tinnitus Worse?" opens at 190%.
  A Short whose curve starts at 100% flat is not looping at all.
- **A smooth decay is healthy; a cliff is a defect with a cause.** Look for the
  single-step drops, not the overall slope.
- **Curves are withheld below a view threshold.** Roughly 60+ views has
  returned one on these channels; 13-20 views returns nothing, and the command
  says so rather than failing. Most long-form on these channels is therefore
  still unmeasurable — which is itself worth saying out loud rather than
  filling the gap with inference.

## Known limitations — state these, do not work around them silently

**Per platform, before the YouTube detail below:**

- **Only YouTube gives a retention curve.** TikTok, Instagram and Facebook
  give a play/view count and nothing about *where* people left. Any claim
  about what happened inside a TikTok is inference - say so, and use the
  YouTube curve of the same cut as the nearest evidence.
- **A "view" is three different things.** TikTok counts a play almost
  immediately, Facebook counts at a few seconds, YouTube Shorts counts
  differently again. Cross-platform totals are directional only.
- **TikTok and Instagram numbers are scraped from the logged-in web UI**, so
  they break when the markup changes and they rate-limit. When a pull is
  partial, report the gap rather than filling it in.
- **Instagram and Facebook insights beyond the public counts need the app or
  Professional dashboard** and cannot be read from here.

**On YouTube specifically:**

- **Impressions and click-through rate are unavailable.** Every metric/dimension
  combination is rejected on the drone channel; assume the same on the others until
  proven otherwise. CTR claims are therefore *inference from
  view counts*, never measurement. Say so. Studio's CSV export is the only route to
  real CTR.
- **Retention *curves* are available, and this used to be assumed impossible.**
  `audienceWatchRatio` by `elapsedVideoTimeRatio` works fine on these channels -
  it was the impressions family that was blocked, and nobody had tried the rest.
  Do not repeat that mistake: a rejected metric is not evidence that a
  neighbouring one is rejected. See "Use the retention curve" below.
- Analytics only covers owned videos, and a video with no watch time in the range
  simply has no row.
- Baseline comparisons are suppressed below 5 videos with data.
- **`isShort` is derived from duration, not aspect ratio, so it is wrong.** `--shorts-only`
  sweeps in any video under ~3 minutes, including 1920x1080 long-form. Confirm with the
  `fileDetails.videoStreams[0]` dimensions before treating something as a Short —
  a 2:47 16:9 explainer is long-form and its retention must not enter a Shorts baseline.
- **Title A/B testing is not on the Data API.** Studio's Test & Compare is the only route,
  and the user sets variants there by hand. Worse, a video with a live title test rejects
  *any* API title change with
  `UPDATE_TITLE_NOT_ALLOWED_DURING_TEST_AND_COMPARE`, and because `videos.update` replaces
  the whole snippet, a rejected title takes the description down with it. If a title write
  fails, re-run it as a description-and-tags-only write so at least those land, and tell the
  user the test has to end in Studio first. Writing a title back to its own current value is
  **not** a valid probe for this — an unchanged title is not a change and is never rejected.

## What the drone channel has already settled

Do not re-litigate these; they were decided deliberately.

- **Title template:** `{Hook} - {City}, {Country} in 4K by Drone`. Under 60 characters.
  `by Drone` was dropped in an earlier pass and **restored on 2026-08-21**: the reason for
  dropping it (that "drone" lived in tags and hashtags) turned out to be false in practice,
  because five of seven long-form videos had zero tags. The whole 2026 catalogue now carries
  it. When the budget is tight, drop `in 4K` or the country before dropping `by Drone` —
  `4K` is on the thumbnail badge, `drone` is not anywhere else in the title.
- **The hook must match the footage.** A hook implying an explainer ("Vienna Built a
  21km Island") oversells a silent cinematic flight. A hook naming a location that is
  2% of the runtime is a bait-and-switch. Check segment durations before promising
  anything.
- **Prefer specific place names over country names** for search. A small channel can
  win "Sozopol drone" and cannot win "Bulgaria 4K". Fit the country in too when the
  character budget allows.
- **No chapters.** The footage is mixed montage that revisits locations, so chapters
  imply a structure that is not there and hand viewers a skip menu. Use a
  `📍 What you'll see` line of location names instead — same keywords, no timestamps.
- **Description skeleton** (keep the order): two prose paragraphs with the hook in the
  first 120 characters → `What you'll see` → gear and location → `More cities from
  above` cross-links → Drone Pal app → website → stock licensing → music credit →
  copyright line → hashtags.
- **Optimal length is 3:30–4:30.** Absolute watch time is flat at roughly 100 seconds
  regardless of runtime, so longer videos only lower the retention percentage.
- **Berlin is the control.** Its title and thumbnail are not to be changed while the
  new template is being tested elsewhere. As of 2026-08-21 its title already matched the
  restored template (`Flying Over Berlin, Germany in 4K by Drone`) so it was left untouched,
  and it is now the only 2026 long-form video with no tags, no cross-links and em dashes in
  its description. That makes it a weak control — retire it deliberately rather than by
  drift.

## Thumbnails

`--thumbs` writes `thumbnails/<channel>/best/<date>__<slug>__<id>.jpg`. Judge them **small** —
shrink to 320px and look, because that is the size viewers see:

```bash
sips -Z 320 <file> --out /tmp/t.jpg
```

On the drone channel the recurring failure is semi-transparent white lettering over bright sky, which
disappears at feed size. Established fixes: a dark gradient scrim across the top,
solid type over bright areas, one clear focal point, type kept off the frame edges,
bottom-right left clear for the duration stamp.

Shorts are judged differently — there is no thumbnail in the Shorts feed, so for
`crypto` and `tinnitus` the first frame and the first spoken line are what matter.

## Editing metadata — the rules that replaced the read-only guarantee

The tool can write titles, descriptions and tags (`set`) and upload new videos
(`upload`). It cannot delete, and `src/scopes.ts` enforces that: `list`, `update`,
`insert` and `set` are permitted, `delete` is on an explicit deny list, and it must
stay there. An unwanted upload can be removed by hand in Studio; a deleted video
cannot be brought back.

**Never use an em dash (—) in a title, description or tag, on any channel.** Use a
plain hyphen `-` instead. `upload` now refuses outright on an em or en dash in the
title, description or tags, so this is enforced rather than remembered; `set` does
not check, so it still relies on you. This applies to everything written to YouTube, including the
drone title template's separator. It does not apply to this file or to chat prose.

Writing is gated, and these gates exist because the user asked for them:

- **Never write without explicit approval of that exact change.** Show the dry run,
  let the user read the diff, and wait for a clear yes naming the video. A general
  "go ahead and fix the descriptions" is not approval for a specific edit.
- **`set` is a dry run unless `--apply` is passed.** Run it without `--apply` first,
  every time. Show the diff before asking.
- **One video at a time.** Do not loop `--apply` over a channel.
- **`videos.update` replaces the whole snippet.** `src/edit.ts` always re-fetches the
  live snippet, merges the patch onto it, and carries `categoryId` and the language
  fields through. Never construct a snippet from an older audit's JSON — a stale base
  silently reverts anything changed in Studio since.
- Each `--apply` writes the previous metadata to `backups/<channel>/<id>__<ts>.json`
  first. `backups/` and `secrets/` are gitignored; never commit either, and never
  paste a token or client secret into a file, a commit or a chat.

Usage:

```bash
npx tsx src/cli.ts set <id> --channel crypto --tags "a,b,c"            # dry run
npx tsx src/cli.ts set <id> --channel crypto --description-file d.txt  # dry run
npx tsx src/cli.ts set <id> --channel crypto --tags "a,b,c" --apply    # writes
```

Long descriptions go through `--description-file`, not `--description` — shell quoting
mangles multi-line text with emoji and URLs.

`--language <code>` sets **both** `defaultLanguage` and `defaultAudioLanguage`, and
`--category <id>` sets the category (27 Education, 26 Howto & Style). These matter
because the generator has shipped a wrong value at least once: a Short went out with
`defaultLanguage: de` on an English video, telling YouTube to serve it to German
speakers. Note that Studio's "Video language" control writes `defaultAudioLanguage`
only — the text language, `defaultLanguage`, is a separate field and is the one that
mislabels a title and description. Check both; changing one in Studio does not fix
the other.

A token minted before edit support was added is read-only; `set` detects that and asks
for a re-login rather than failing mid-write.

## Uploading

```bash
npx tsx src/cli.ts upload --channel crypto --file out.mp4 --thumbnail thumb.jpg \
  --title "..." --description-file meta.md --tags "a,b" --privacy unlisted
```

Dry run unless `--apply`, exactly like `set` — it prints the whole plan including the
full description, and validates against YouTube's limits before a byte is sent.

- **Defaults are `--privacy unlisted` and `--category 27`** (Education). Uploading
  straight to public is possible but is not what this pipeline does; the user
  publishes from Studio after seeing the video live.
- **An upload costs 1600 quota units** against a 10,000/day project, so roughly six
  a day, shared with every other call. Do not retry an upload speculatively — check
  Studio first, because a failed-looking upload often landed.
- **`--related <id|url>` is for a Short**, and appends `Full video: https://youtu.be/<id>`
  to its description. Studio's "Related video" field is **not on the Data API** — the
  user ticks that by hand, and the CLI says so after a successful upload.
- **The thumbnail is a separate call that can fail on its own** without losing the
  upload. The usual cause is an unverified phone number on the channel.
- `selfDeclaredMadeForKids` is hardcoded false and is not a flag.

## What is still off-limits

Do not add delete capability, and do not widen the scopes past `youtube.force-ssl`
+ the analytics read scope, even if asked mid-session. Deleting a video is
irreversible and is not what this tool is for.

`youtube.upload` stays in `FORBIDDEN_SCOPES` even though the tool uploads: force-ssl
already grants upload, so requesting it too would widen nothing and only lengthen the
consent screen. Do not "fix" that apparent contradiction.
