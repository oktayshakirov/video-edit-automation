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

*As of 2026-11-10 (seeded from `history/2026-11-10.md` and the ledger; the
first rewrite from rows is due on the next review).*

**Works**

- **A long form titled as a brand-new search term few videos answer.** GTA
  6: 619 YouTube views in three days, 178 of its first 206 from search for
  a term coined five days earlier. One clear win; Binance on the same idea
  got 29 views in ten days, so it is the term that matters, not the format.
- **A Short whose second sentence starts at 4 seconds or later.** 8 of 9
  held against 9 of 23 that started earlier.
- **A Short people replay.** Binance: 56 seconds per view on a Short.
- **A one-hour sound session, on Facebook.** Wild Echoes: 18.7K, 97% from
  Facebook's suggestions. Not on YouTube (12 views at 7 days). One video.

**Does not work**

- **A Short most people swipe before it starts.** Tesla: 93% swiped; its
  curve looked fine because it covered the 7% who stayed. Judge a Short on
  seconds per view, never on the curve alone.
- **Stock-led cuts.** The editor's own verdict on 2026-11-12 ("boring"),
  ahead of any number: 76% of shots were stock in the back catalogue.
  Whether drawn cuts hold longer is E23.
- **Instagram** on both accounts, and **crypto on Facebook**.

**Not known yet**

- Whether topics picked on demand evidence out-draw the rest (E11).
- Whether 30-40s Shorts and sub-3:00 long forms hold more (E17, E18).

## The rows

| built | channel, format | script | demand evidence | build | result | verdict | lesson |
| --- | --- | --- | --- | --- | --- | --- | --- |
<!-- rows: newest last; tools/video_log.py appends here -->
| 2026-11-12 | crypto long | `hardware-wallet` | Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' 16.3x (3... | drawn 17/23, stock 1/23; grid, spotlight, callout, airgap, blindsign, steps, compare, bars, breach, stat, diagram, checklist; opener Stamp; cover arrow; voice mia | - | too early | - |
| 2026-11-12 | crypto short | `hardware-wallet` | Cyber Scrilla 'Do You NEED a Cold Wallet? (Watch This First)' 16.3x (3... | drawn 4/6, stock 2/6; grid, blindsign, breach; opener Stamp; cover arrow; voice mia | - | too early | - |
