# Experiments ledger

One entry per thing being tested. Each has a start date, what it changes, the
number that judges it, and the result that would prove it wrong — written
*before* the data comes in. Update the status every review; never delete an
entry, mark it failed or retired and say why.

Baseline for everything below: `history/2026-09-21.md`.

## Open checks - read these first, every run

Rewritten at the end of each run (step 9). Each says what to read and from
when the data will exist. Answered checks move into that run's snapshot.

*Set 2026-10-11:*

- **E6, drone thumbnail test.** Ask the user for Studio's per-video winner
  and whether the test has ended. After winners apply, compare 14 days of
  views and average view duration against `history/2026-10-11.md`. Not
  readable before ~10-25.
- **Bitcoin halving Short `HSUtPLAJlcg`, the first prediction from the
  sentence-2 rule.** Its sentence 2 keeps the answer back, so it should hold
  (half gone past ~12s). Its curve exists once it passes ~60 views; it had 284
  on day one.
- **Gate compliance.** Run `tools/opening_check.py` on every Short built
  after 2026-10-12 and check its handover carried the output. A Short that
  skipped the gate is a compliance finding, not a rule finding.
- **Crypto Facebook long-form.** Scams 15, First tx 27, Market cap 36 against
  145-285 before 09-22. Watch the next two (halving first). If they also land
  under ~70, compare the passing and failing publish runs: cover frame,
  caption, posting time, and whether n8n finished.
- **Sound beds outside YouTube** (proposed 10-11, not started). Sessions are
  the tinnitus outlier on Facebook (29k) and on pre-pipeline TikTok (~1.9k).
  If the user builds a 30-60s cut for TikTok, open it as an experiment with a
  fail line of "lands in the 250/770 batch like the rest".

---

## E1 — The redacted opening hook

- **Started:** 2026-09-21 (first videos built after this date).
- **Change:** `hook="... [word] ..."` on every Short and long-form. It slams in
  over a camera punch-in with an `impact`, hides the key word under animated
  static with a `riser`, and reveals it with `reveal`+`tick` on the frame the
  narration says it (sentence 2, ~3.5-5s). Spec in `shorts.md` "The opening
  hook: a redacted headline". The static-headline version from earlier the
  same day was rejected on sight and never shipped.
- **Why:** every Short loses 13-27 points around 5s, before sentence 2 has
  been heard; on muted feeds (Instagram, much of TikTok) the voice does not
  land at all.
- **Judged by:** the drop at ~5s and the half-gone second on YouTube curves,
  against the pre-hook cohort (drops −13 to −27, half gone 6.7-9.4s). Also
  check the reveal lands where it should: the curve should flatten or tick
  up around the reveal second, not fall off before it. Also:
  do TikTok videos start clearing the ~770 test-batch ceiling?
- **Fails if:** across the first 4+ hooked Shorts with curves, the ~5s drop is
  still ≥13 points *and* half-gone stays under 9s.
- **Confounded with E2** — both ship together. If the cohort improves, say "the
  pair worked"; to separate them later, ship a few with one and not the other.
- **Status:** not yet shipped.

## E2 — Sentence 2 as a partial answer that opens a bigger question

- **Started:** 2026-09-21. Replaces the 09-11 version ("answer it in sentence
  2"), which was applied in every Short 09-13 → 09-21 and did not move the 5s
  cliff: a complete answer is also an exit (Concert, Magnesium, Fear & Greed).
- **Change:** `narration.md` "Revised 2026-09-21".
- **Judged by / fails if:** same as E1.
- **Status:** not yet shipped.

## E3 — Shorts close cold, never on a question

- **Started:** 2026-09-11.
- **Evidence it was built on:** Silence (cold) last frame 88.5%, opens 190%;
  Ethereum (question) last frame 25% with drops inside the question itself.
- **Judged by:** last-frame % and opening % (loop) on cold-close Shorts.
- **Fails if:** cold-close Shorts show no more replay (opening ≤110%) than
  question-close ones once 5+ of each have curves.
- **Status 2026-09-21: too early / weak.** Applied in all new crypto Shorts.
  Openings 100-122% — no strong loop yet — but last-frame share is also tiny
  (4-19%) because most viewers leave at 5s, so the ending barely gets a
  chance to matter until E1/E2 fix the opening.

## E4 — Shorts titled as the question people actually search

- **Started:** ~2026-09-13 (Treble Health pattern: plain patient question).
- **Observed 2026-09-21:** YouTube Short reach up 3-6x (typical new Short
  100-335 views vs 20-50 in August). Channel totals ×4.
- **Caveat:** confounded with channel age and upload volume. Holding, not
  proven.
- **Status:** holding.

---

## Open observations (not yet experiments)

- **Facebook is the long-form platform.** Same long-forms: ~145-200 views on
  Facebook vs 0-13 on YouTube; a sound session reached ~29k there. Candidate
  experiment: optimise long-form for Facebook first (its cover frame, its
  captions, posting time), not YouTube.
- **Instagram tinnitus at 0 plays since 09-14**, account status clear. Watch
  for recovery; if still zero next review, try one reel uploaded natively in
  the app to see whether the upload path is the cause.
- **TikTok caps at ~770** on every video so far — nothing has escaped the test
  batches. E1 is the first change aimed at the first-second behaviour TikTok
  scores on.

## E5 — Opener variants (rotation)

- **Started:** 2026-09-24.
- **Change:** four alternatives to the redacted hook (`longform/openers.py`):
  Counter, Stamp, Split, Search, Flash. Chosen by the shape of the topic, and
  rotated so the same opener does not run three videos in a row. Spec in
  `shorts.md` "Choosing the opener".
- **Why:** the user's call - every video opening identically reads as a
  template. Variety is the goal in itself; retention is the constraint, not
  the target.
- **Judged by:** the ~5s drop and half-gone second *per opener type*, against
  the redacted-hook cohort. **Tag the opener in every snapshot row** or this
  cannot be judged at all.
- **Fails if:** a variant's cohort is consistently worse at 5s than the
  redacted hook over 3+ videos - then it is retired to a narrower use, or
  dropped.
- **Note:** this deliberately makes E1's cohort less uniform. Keep the
  redacted hook as the default so it stays the control.
- **Status:** not yet shipped.

---

## Status 2026-10-11 (from the video-views-audit run)

- **E1 (redacted hook): not the active ingredient.** Five hooked Shorts with
  curves: Scams and Explain hold (half gone 11.6s, 15.8s), and Neck, Star Trek
  and First tx do not (9.5s, 8.8s, 7.1s). The fail condition (4+ hooked,
  drop ≥13 and half gone <9s) is met by 2 of 5, so E1 has not failed. But
  the hook alone has no effect. What it gets depends on sentence 2.
- **E2 (sentence 2): confirmed, with a tighter definition.** Across 11 curves
  and four opener types, every Short whose sentence 2 answers the title
  question plainly or confirms it sits at half gone 7.1-11.0s, the same as
  pre-hook. Every one that keeps the answer back, or plainly overturns the
  title (Whale), sits at 11.6-28.8s. No overlap.
  `narration.md` "Confirmed 2026-10-11" records it, and `workflow.md` step 2
  now gates it with `tools/opening_check.py`. Watch whether Shorts built
  after this date stay in the holding group.
- **E5 (opener variants): no opener effect can be read yet.** Search (Jaw
  holds, Musk does not), Stamp (Whale holds, Market cap does not) and Counter
  (Musicians does not, Halving has no curve) each split along the
  sentence-2 line. To judge an opener, compare it only within the group that
  keeps the answer back.
- **E4 (search-question titles): holding.** YouTube views roughly +900 a
  channel in ten days.

## E6 - Drone long-form thumbnail A/B (Studio Test & Compare)

- **Started:** 2026-10-11, by the user in Studio, on every drone long-form
  video. Berlin (`zjCQxJcJGN4`) is included, so there is no untouched control.
- **Change:** a new thumbnail format against the current one.
- **Judged by:** (1) Studio's per-video winner (watch-time share), which
  only the user can read. (2) YouTube views per day across the 9 videos
  after the winners are applied, against the baseline: 178 views in 14 days
  (12.7/day), 72 in the last 7 (10.3/day). The per-video baseline table is
  in `history/2026-10-11.md`. (3) Average view duration: it
  must not fall.
- **Fails if:** Studio picks the old thumbnail on most videos, or views per
  day after the switch are no higher than ~13/day with view duration down.
- **Constraint:** no API title or thumbnail writes on drone long-forms while
  the test runs.
- **Status:** running.
