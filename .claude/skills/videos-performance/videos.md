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

*As of 2026-11-24 (`history/2026-11-24.md`).*

**Works**

- **Tinnitus sound sessions - still the only part of either channel that
  grows.** Seven weeks up running (751 YouTube views in the 11-16 week,
  2,586 watch minutes), all on suggested, 3.6-6.5% CTR against 0-1.4% for
  explainers. The channel gained 13 subscribers that week, its best.
- **A named masking noise.** 2:1 + White Noise 41 views a day at 13 days,
  the fastest video on the channel. The first E25 sessions start faster
  than the themed one built beside them (Brown 10.3 a day, Fan 9.5, Pink
  6.0 against Fireplace 5.0) and their Shorts hold twice as long (Fan
  13.1s a view, White noise 13.2, Fire 6.4). Early days; E25 reads them
  at 14.
- **A Short whose second sentence starts at 4 seconds or later.** 12 of
  14 held (lab, 11-24). New-build medians are past the goal on both
  channels: tinnitus 12.7s a view (target 12), crypto 10.7s (target 9).
  Hardware wallet is the miss: necessary, not sufficient.
- **A Short people replay.** Opening 125%+: 11 of 14 held.
- **A rumour as the title, checked by mechanism (crypto, one video).**
  Stablecoin: 45 views in 7 days, 13% CTR, 68% average viewed, from
  search - the best crypto start since GTA 6.
- **A long form titled as a brand-new search term.** GTA 6: 2,160 views,
  1,817 from search. Off-audience. Its launch week halved its CTR (8.6%
  -> 4.6%) as competitors arrived; the build-in-48h window was missed.
- **Crypto topics from the demand map, over coverage picks** (E11 rule).

**Does not work**

- **Tinnitus explainer long forms.** 58 views in the 11-16 week, the
  lowest since September; 0-1.4% CTR. The ranking (E26) took 1.05% and
  37 on Facebook, where explainers used to take 163 - too early, one video.
- **Crypto scam stories in the how-to-scam search pool.** Squid Game was
  shown 9,241 times in five days at 0.01% CTR, on "how to rug pull" and
  "exit scam" - as Rug pull (13,875 at 0.01%) and Meme coins (11,339 at
  0.05%) were. Three videos. Those impressions are not interest.
- **Crypto evergreen explainers.** Logan Paul 10 views and One ear 15 at
  13 days: they hold who comes (52%, 31%), nobody comes.
- **Themed ambience as the session's lead** (jungle, space, cat, fire);
  the Fireplace Short at 6.4s a view.
- **A subject borrowed without its format** (`what-makes-tinnitus-worse`).
- **Shorts reach, this week**: tinnitus 722 -> 233, crypto 148 -> 67
  weekly views, while retention rose. One week.
- **Instagram** on both accounts, **crypto on Facebook** (0-10 on every
  upload, five weeks), and **TikTok** past its batches (60 uploads, none
  over 1,000).

**Not known yet**

- Whether numbered lists, rankings (tinnitus) and heist stories (crypto)
  lift the explainers (E26, 1 of 3 each).
- Whether a rumour title holds over three videos (E24, 1 of 3); whether
  30-40s crypto Shorts hold more (E17, 2 of 5).

## The rows

| built | channel, format | script | demand evidence | build | result | verdict | lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
<!-- rows: newest last; tools/video_log.py appends here -->
| 2026-11-12 | crypto long | `hardware-wallet` | Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' 16.3x (3... | drawn 17/23, stock 1/23; grid, spotlight, callout, airgap, blindsign, steps, compare, bars, breach, stat, diagram, checklist; opener Stamp; cover arrow; voice mia | YT 25 at 12 days, avg 57s (32%), search; cover swapped 11-21 (74 impr. at 4.05% before, 20 at 0% after); FB 5 | too early | - |
| 2026-11-12 | crypto short | `hardware-wallet` | Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' 16.3x (3... | drawn 4/6, stock 2/6; grid, blindsign, breach; opener Stamp; cover arrow; voice mia | YT 27, 8.9s a view, half-gone 10.5s, 27% at the last frame (12 days); TikTok 769 | average | sentence 2 at 4.5s and 37s long, still under 11s: the late sentence 2 is necessary, not sufficient (one video) |
| 2026-11-13 | tinnitus long | `what-makes-tinnitus-worse` | Doctor Cliff '5 Things That are Making your Tinnitus LOUDER' 1.5M (138... | drawn 16/24, stock 8/24; grid, steps, diary, diagram, chart, checklist, spotlight, callout, bars; opener Stamp; cover cutout; voice mia | YT 5 at 11 days; retitled 11-17 (237 impr. at 0.84% before, 146 at 1.37% after); FB 163 | too early | borrowed Doctor Cliff's subject, not his number ("5 Things..."): the list format was left on the table |
| 2026-11-13 | tinnitus short | `what-makes-tinnitus-worse` | Doctor Cliff '5 Things That are Making your Tinnitus LOUDER' 1.5M (138... | drawn 5/8, stock 3/8; spotlight, diary, checklist, steps; opener Stamp; cover cutout; voice mia | YT 44, 9.5s a view, half-gone 25.0s (11 days); FB 167; TikTok 756 | average | held its curve (25s) and nobody came: retention without reach |
| 2026-11-17 | crypto long | `stablecoin-interest` | Clearly Finance 'Is the US Planning a $37 Trillion Crypto Debt Reset?'... | drawn 15/22, stock 10/22; post, grid, reserve, stat, bars, timeline, checklist; opener Search; cover cutout; voice mia | **YT 45 at 7 days**, avg 120s (68%), CTR 13.16% on 114, search 28 of 34; 1 like; FB 3 (E24) | too early | - |
| 2026-11-17 | crypto short | `stablecoin-interest` | Clearly Finance 'Is the US Planning a $37 Trillion Crypto Debt Reset?'... | drawn 5/8, stock 3/8; reserve, bars; opener Counter; cover cutout; voice mia | YT 9 at 7 days, no curve; TikTok 712; FB 0 | too early | - |
| 2026-11-17 | tinnitus long | `soft-flames-66-breathing-60min` | E13 session queue row 5 (coherent 6-6 breathing, path guide); E12 hour... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 35 at 7 days (5.0/day), CTR 6.44% on 295 | too early | - |
| 2026-11-17 | tinnitus short | `soft-flames-66-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 66, 6.4s a view, half-gone 11.6s (7 days); TikTok 699 | did not | a themed ambience (fire) Short: 6.4s a view against 13.1-13.2 for the white- and fan-noise Shorts (one video) |
| 2026-11-17 | crypto long | `logan-paul` | 'logan paul cryptozoo': Coffeezilla 'Investigating Logan Paul's Bigges... | drawn 7/22, stock 9/22; diagram, pile, checklist, behind, timeline; opener Search; cover arrow; voice mia | YT 10 at 13 days, avg 86s (52%), 276 impr. at 0.36% (11-10 to 11-16); FB 10 | did not | holds the ones who come (52-67%); nobody comes |
| 2026-11-17 | crypto short | `logan-paul` | 'logan paul cryptozoo': Kyle Boland egg-hatching Short 11.2x; George J... | drawn 3/8, stock 2/8; reel, pile, behind; opener Stamp; cover arrow; voice mia | YT 104, 11.1s a view, half-gone 13.4s (13 days); TikTok 744 | worked | first crypto Short past the 9s goal; sentence 2 at 4.5s, held Stamp |
| 2026-11-17 | tinnitus long | `tinnitus-in-one-ear` | 'tinnitus in one ear': Treble 'Should You Ring The Alarm For Tinnitus ... | drawn 8/17, stock 8/17; compare, checklist, dial, steps, audiogram, behind; opener Search; cover text; voice noah | YT 15 at 13 days, avg 54s (31%), 392 impr. at 1.53% (11-10 to 11-16); FB 163 | did not | - |
| 2026-11-17 | tinnitus short | `tinnitus-in-one-ear` | 'tinnitus in one ear': Treble 'Should You Ring The Alarm For Tinnitus ... | drawn 5/10, stock 4/10; grid, audiogram, post, checklist, dial; opener Search; cover text; voice noah | YT 123, 12.7s a view, half-gone 19.4s (13 days); FB 123; TikTok 724 | worked | - |
| 2026-11-17 | tinnitus long | `tranquil-zenith-21-breathing-60min` | E13 session queue row 4 (2:1 breathing, path guide); E12 hour-plus ses... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | **YT 536 at 13 days** (41/day, fastest on the channel), CTR 5.72% on 2,010 (11-17 to 11-22), avg 366s, suggested 333 of 463; FB 340 | worked | a named masking noise (white noise) out-draws themed ambiences; 2 of the top 3 sessions are white noise |
| 2026-11-17 | tinnitus short | `tranquil-zenith-21-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 418, 13.2s a view, half-gone 12.9s (13 days); TikTok 729; FB 51 | worked | "Play this white noise just below your tinnitus": a masking instruction on a known noise |
| 2026-11-18 | tinnitus long | `brown-noise-478-breathing-60min` | E25 a named masking noise leads the session (white-noise sessions 47 a... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 62 at 6 days (10.3/day), CTR 5.36% on 560, suggested 28 of 34; FB 183 (E25) | too early | - |
| 2026-11-18 | tinnitus short | `brown-noise-478-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 31, no curve (6 days); TikTok 699 | too early | - |
| 2026-11-19 | crypto long | `squid-game-token` | 'squid game crypto scam': TheClipZone 'Live RUG PULL of $SQUID' Short ... | drawn 32/42, stock 19/42; spotlight, diagram, honeypot, pool, steps, stat, checklist; opener Counter; cover cutout; voice mia | YT 26 at 5 days, avg 39s (13%); **9,241 impressions at 0.01%**, search "how to rug pull", "exit scam"; FB 2 (E26) | too early | a scam story is shown to how-to-scam searchers and not clicked, as Rug pull and Meme coins were; the cover names neither Squid Game nor the $3.4M |
| 2026-11-19 | crypto short | `squid-game-token` | 'squid game crypto scam': TheClipZone 'Live RUG PULL of $SQUID' Short ... | drawn 6/8, stock 3/8; honeypot, spotlight; opener Stamp; cover cutout; voice mia | YT 32, 10.7s a view, half-gone 28.4s, 8% at the last frame (5 days); 4,867 impr. at 0.02%; TikTok 700 | too early | - |
| 2026-11-20 | tinnitus long | `tinnitus-treatments-ranked` | HearingTracker 'Four BEST Tinnitus Treatments' 402k (109x); Doctor Cli... | drawn 39/49, stock 12/49; post, tiers, diagram, grid, callout, spotlight, checklist, steps; opener Split; cover tiers; voice mia | YT 10 at 5 days, avg 103s (30%), 286 impr. at 1.05%, search 6 of 8; **FB 37** (E26) | too early | - |
| 2026-11-20 | tinnitus short | `tinnitus-treatments-ranked` | HearingTracker 'Four BEST Tinnitus Treatments' 402k (109x); Doctor Cli... | drawn 6/9, stock 3/9; tiers; opener Stamp; cover tiers; voice mia | YT 9 at 5 days, no curve; FB 164; TikTok 671 | too early | - |
| 2026-11-20 | tinnitus long | `fan-noise-444-breathing-60min` | E25 a named noise leads the session (white-noise sessions 47 and 7.6 v... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 38 at 4 days (9.5/day), CTR 3.66% on 766, suggested 30 of 31; FB 215 (E25) | too early | - |
| 2026-11-20 | tinnitus short | `fan-noise-444-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 57, 13.1s a view, half-gone 9.9s (4 days); FB 194; TikTok 655 | too early | - |
| 2026-11-21 | crypto long | `optimizely-hack` | The CryptoDad 'Ledger Website Hacked! Is Your Crypto Safe?' 51k in 2 d... | drawn 20/23, stock 1/23; spotlight, grid, diagram, relay, compare, steps, stat, checklist; opener Search; cover beat; voice mia | YT 9 at 3 days, 82 impr. at 2.44%; FB 7 | too early | - |
| 2026-11-21 | crypto short | `optimizely-hack` | The CryptoDad 'Ledger Website Hacked! Is Your Crypto Safe?' 51k in 2 d... | drawn 5/7, stock 2/7; grid, relay; opener Split; cover beat; voice mia | YT 20 at 3 days, no curve; 155 impr. at 0.65%; TikTok 605; FB 1 | too early | - |
| 2026-11-21 | tinnitus long | `pink-noise-box-breathing-60min` | E25 a named noise leads the session (white-noise sessions 47 and 7.6 v... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 18 at 3 days (6.0/day), CTR 3.57% on 112; FB 237 (E25) | too early | - |
| 2026-11-21 | tinnitus short | `pink-noise-box-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 29 at 3 days, no curve; FB 195; TikTok 693 | too early | - |
| 2026-11-23 | tinnitus long | `white-noise-sigh-breathing-60min` | E25 a named noise leads the session (white-noise sessions 47 and 7.6 v... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 41 at 1 day, CTR 5.45% on 312; FB 217 (E25) | too early | - |
| 2026-11-23 | tinnitus short | `white-noise-sigh-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | YT 80 at 1 day; FB 118; TikTok 583 | too early | - |
| 2026-11-25 | oktai long | `why-ai-videos-feel-fake` | no evidence | drawn 57/60, stock 3/60; reel, steps, lesson, logos, diagram, wall, voice, phones, bars, chart; opener -; cover -; voice - | - | too early | - |
| 2026-11-25 | oktai short | `why-ai-videos-feel-fake` | no evidence | drawn 8/8, stock 0/8; reel, voice, bars; opener -; cover -; voice - | - | too early | - |
| 2026-11-25 | tinnitus long | `green-noise-46-breathing-60min` | a named noise leads (E25: Brown 10.3, Fan 9.5, Pink 6.0, HF white 41 v... | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | - | too early | - |
| 2026-11-25 | tinnitus short | `green-noise-46-breathing-short` | no evidence | drawn 0/1, stock 0/1; -; opener -; cover -; voice - | - | too early | - |
