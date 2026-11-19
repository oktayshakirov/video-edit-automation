# Video ledger: how each video was built, and how it did

One row per video. **A build run appends the row** at its handoff
(`tools/video_log.py <long script> <short script>` - the build tags are read
from the script, never typed). **A review run fills the last three
columns** for every row old enough to read, and then rewrites "What works"
below from the rows. The build skills read "What works" before suggesting a
topic and before scripting.

This is the loop: build, log, measure, write the lesson, read the lessons
before the next build. `experiments.md` holds only the few tests still
running; this file is where a verdict on a *video* lives.

## How to fill a row (review runs)

- **result** - Short: views, seconds per counted view, half-gone second.
  Long form: views at 14 days, average view seconds and %, main traffic
  source. One platform per number, named.
- **verdict** - `worked` (clearly above the channel's median for its
  format), `average`, `did not` (clearly below), or `too early` (a Short
  under 7 days or 60 views; a long form under 14 days).
- **lesson** - one line, only when the row teaches something a script
  could act on: the topic kind, the title promise, the opening, the
  picture. "-" is a fine answer. Never a guess about cause from one video;
  write "one video" when it is one.

## What works, and what does not

Rewritten every review from the rows and the snapshots. Short, dated, and
each line names its evidence. **Read this before step 1 of a build.**

*As of 2026-11-17 (`history/2026-11-17.md`).*

**Works**

- **Tinnitus sound sessions - the only part of either channel that grows.**
  Session long forms rose six weeks running (52 to 489 YouTube views a
  week), live on suggested, and draw 4.9% CTR against 1.25% for explainers.
  Most new subscribers came from sessions and session Shorts.
- **A named masking noise.** 2:1 + White Noise (47 views a day) and 4-7-8 +
  White Noise (7.6) are two of the top three sessions; jungle, space, bird,
  cat and fire beds sit at 0.6-4. Nebula (19.8) is the exception. Length did
  not decide it: the other three 1-hour sessions are among the slowest.
- **A Short whose second sentence starts at 4 seconds or later.** 11 of 12
  held (lab, 11-17), up from 8 of 9. The first crypto Short past the 9s
  goal (Logan Paul, 11.1s a view) is one.
- **A Short people replay.** Opening 125%+: 10 of 12 held.
- **A long form titled as a brand-new search term.** GTA 6: 1,734 views,
  1,423 from search, still ~224 a week. Off-audience (no subscribers, no
  suggested to later uploads), so a reach asset, not a channel builder.
- **Crypto topics from the demand map, over coverage picks**: 29 against 8
  median views (E11, 11-17). Better, still small.

**Does not work**

- **Tinnitus explainer long forms.** Flat at 50-110 views a week for three
  months; shown to thousands (6,356 impressions on New Tinnitus) and
  clicked by under 1%. A cover that repeats the title over a stock person
  holding their head is every one of them since 09-20.
- **Crypto explainer long forms on evergreen terms.** Median 156
  impressions in a lifetime: YouTube does not show them. Nothing since GTA
  6 passed 33 views.
- **A subject borrowed without its format.** `what-makes-tinnitus-worse`
  took Doctor Cliff's subject (152x) and not his number ("5 Things...").
- **Themed ambience as the session's lead** (jungle, space, cat, fire).
- **A Short most people swipe before it starts** (Tesla, 93% swiped).
- **Instagram** on both accounts, **crypto on Facebook** (1-9 on every
  upload for a month), and **TikTok** past its 250/770 batches (48 uploads,
  none over 1,000).

**Not known yet**

- Whether numbered lists (tinnitus) and heist stories (crypto) lift the
  explainers (proposed 11-17).
- Whether 30-40s crypto Shorts hold more (E17); whether a rumour title
  draws more (E24).

## The rows

| built | channel, format | script | demand evidence | build | result | verdict | lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
<!-- rows: newest last; tools/video_log.py appends here -->
| 2026-11-12 | crypto long | `hardware-wallet` | Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' 16.3x (3... | drawn 17/23, stock 1/23; grid, spotlight, callout, airgap, blindsign, steps, compare, bars, breach, stat, diagram, checklist; opener Stamp; cover arrow; voice mia | YT 17 at 5 days, avg 19s (11%), search 11 of 12; FB 3 | too early | - |
| 2026-11-12 | crypto short | `hardware-wallet` | Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' 16.3x (3... | drawn 4/6, stock 2/6; grid, blindsign, breach; opener Stamp; cover arrow; voice mia | YT 21, no curve; TikTok 769 | too early | - |
| 2026-11-13 | tinnitus long | `what-makes-tinnitus-worse` | Doctor Cliff '5 Things That are Making your Tinnitus LOUDER' 1.5M (138... | drawn 16/24, stock 8/24; grid, steps, diary, diagram, chart, checklist, spotlight, callout, bars; opener Stamp; cover cutout; voice mia | YT 3 at 4 days, CTR 0.84% on 238; FB 163 | too early | borrowed Doctor Cliff's subject, not his number ("5 Things..."): the list format was left on the table |
| 2026-11-13 | tinnitus short | `what-makes-tinnitus-worse` | Doctor Cliff '5 Things That are Making your Tinnitus LOUDER' 1.5M (138... | drawn 5/8, stock 3/8; spotlight, diary, checklist, steps; opener Stamp; cover cutout; voice mia | YT 40, 8.3s a view, half-gone 25.0s (4 days); FB 167; TikTok 756 | too early | - |
| 2026-11-17 | crypto long | `stablecoin-interest` | Clearly Finance 'Is the US Planning a $37 Trillion Crypto Debt Reset?'... | drawn 15/22, stock 10/22; post, grid, reserve, stat, bars, timeline, checklist; opener Search; cover cutout; voice mia | YT 5, 1 day (E24) | too early | - |
| 2026-11-17 | crypto short | `stablecoin-interest` | Clearly Finance 'Is the US Planning a $37 Trillion Crypto Debt Reset?'... | drawn 5/8, stock 3/8; reserve, bars; opener Counter; cover cutout; voice mia | YT 7, 1 day; TikTok 705 | too early | - |
| 2026-11-17 | tinnitus long | `soft-flames-66-breathing-60min` | E13 session queue row 5 (coherent 6-6 breathing, path guide); E12 hour... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 2, FB 41, 1 day | too early | - |
| 2026-11-17 | tinnitus short | `soft-flames-66-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 25, FB 108, 1 day | too early | - |
| 2026-11-17 | crypto long | `logan-paul` | 'logan paul cryptozoo': Coffeezilla 'Investigating Logan Paul's Bigges... | drawn 7/22, stock 9/22; diagram, pile, checklist, behind, timeline; opener Search; cover arrow; voice mia | YT 8 at 6 days, avg 112s (67%), search 7; FB 9 | too early | holds the ones who come (67%); nobody comes |
| 2026-11-17 | crypto short | `logan-paul` | 'logan paul cryptozoo': Kyle Boland egg-hatching Short 11.2x; George J... | drawn 3/8, stock 2/8; reel, pile, behind; opener Stamp; cover arrow; voice mia | YT 103, 11.1s a view, half-gone 13.4s (6 days); TikTok 740 | too early | first crypto Short past the 9s goal; sentence 2 at 4.5s, held Stamp |
| 2026-11-17 | tinnitus long | `tinnitus-in-one-ear` | 'tinnitus in one ear': Treble 'Should You Ring The Alarm For Tinnitus ... | drawn 8/17, stock 8/17; compare, checklist, dial, steps, audiogram, behind; opener Search; cover text; voice noah | YT 14 at 6 days, avg 60s (34%), suggested 7; FB 163 | too early | - |
| 2026-11-17 | tinnitus short | `tinnitus-in-one-ear` | 'tinnitus in one ear': Treble 'Should You Ring The Alarm For Tinnitus ... | drawn 5/10, stock 4/10; grid, audiogram, post, checklist, dial; opener Search; cover text; voice noah | YT 117, 11.7s a view, half-gone 17.3s (6 days); FB 123; TikTok 724 | too early | - |
| 2026-11-17 | tinnitus long | `tranquil-zenith-21-breathing-60min` | E13 session queue row 4 (2:1 breathing, path guide); E12 hour-plus ses... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | **YT 292 at 6 days** (47/day, fastest on the channel), CTR 5.66%, avg 394s, suggested 111 of 130; FB 340 | worked | a named masking noise (white noise) out-draws themed ambiences; 2 of the top 3 sessions are white noise |
| 2026-11-17 | tinnitus short | `tranquil-zenith-21-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 406, 12.4s a view (6 days); TikTok 729; FB 51 | worked | "Play this white noise just below your tinnitus": a masking instruction on a known noise |
| 2026-11-18 | tinnitus long | `brown-noise-478-breathing-60min` | E25 a named masking noise leads the session (white-noise sessions 47 a... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | - | too early | - |
| 2026-11-18 | tinnitus short | `brown-noise-478-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | - | too early | - |
| 2026-11-19 | crypto long | `squid-game-token` | 'squid game crypto scam': TheClipZone 'Live RUG PULL of $SQUID' Short ... | drawn 32/42, stock 19/42; spotlight, diagram, honeypot, pool, steps, stat, checklist; opener Counter; cover cutout; voice mia | - | too early | - |
| 2026-11-19 | crypto short | `squid-game-token` | 'squid game crypto scam': TheClipZone 'Live RUG PULL of $SQUID' Short ... | drawn 6/8, stock 3/8; honeypot, spotlight; opener Stamp; cover cutout; voice mia | - | too early | - |
| 2026-11-20 | tinnitus long | `tinnitus-treatments-ranked` | HearingTracker 'Four BEST Tinnitus Treatments' 402k (109x); Doctor Cli... | drawn 39/49, stock 12/49; post, tiers, diagram, grid, callout, spotlight, checklist, steps; opener Split; cover tiers; voice mia | - | too early | - |
| 2026-11-20 | tinnitus short | `tinnitus-treatments-ranked` | HearingTracker 'Four BEST Tinnitus Treatments' 402k (109x); Doctor Cli... | drawn 6/9, stock 3/9; tiers; opener Stamp; cover tiers; voice mia | - | too early | - |
