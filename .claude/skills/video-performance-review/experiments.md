# Experiments ledger

One entry per thing being tested. Each has a start date, what it changes, the
number that judges it, and the result that would prove it wrong — written
*before* the data comes in. Update the status every review; never delete an
entry, mark it failed or retired and say why.

Baseline for everything below: `history/2026-09-21.md`.

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
