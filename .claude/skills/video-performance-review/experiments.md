# Experiments ledger

One entry per thing being tested. Each has a start date, what it changes, the
number that judges it, and the result that would prove it wrong — written
*before* the data comes in. Update the status every review; never delete an
entry, mark it failed or retired and say why.

Baseline for everything below: `history/2026-09-21.md`.

## Open checks - read these first, every run

Rewritten at the end of each run (step 9). Each says what to read and from
when the data will exist. Answered checks move into that run's snapshot.

*Set 2026-10-23* (the 10-11 checks are answered in `history/2026-10-23.md`):

- **E6, drone thumbnail test: winner read dropped (user, 2026-10-23).** Do
  not ask for Studio's per-video winners. The test may still be running in
  Studio, so the no-API-title/thumbnail-writes constraint stays. Read API
  views and minutes watched against `history/2026-10-11.md` only when the
  user says the test is over or drone is back in scope. Mid-test
  (10-11..10-22) was flat: 149 views against 154, minutes 98 against 133.
- **E9, the engine overhaul, and its overlap with E7.** Every video in the
  next run has to be tagged old engine or new engine. The upgrades landed
  from `7aed772` (10-21: typed chapter cards, cinematic title, native
  outro, old-film surface, glitch cuts) through `d553559` (10-23:
  spotlight, post cards, reel beat). The user said on 10-23 that only one
  uploaded video uses them so far. History, Meme coins and Nebula were all
  built after `7aed772`, so confirm with the user which one it is, and tag
  the rest by build commit date. Everything published on or before 10-20
  is old engine.
- **E10, Nebula thumbnail test.** Ask the user whether the Studio Test &
  Compare on `r7NqyOv5_9Y` has ended, and for its winner (watch-time share)
  and each variant's share. Until it ends, never write that video's title
  or thumbnail through the API. Also ask for the Studio CSV (impressions,
  CTR) for every session, and fill the CTR column of the E10 baseline table.
- **E7, male voice `noah`.** On test from 2026-10-23: the next 5 crypto and
  5 tinnitus article pairs (long + Short) read in `noah`, then back to `mia`.
  The pairs are listed in the "Voice test" tables in
  `docs/video/projects/crypto.md` and `tinnitus.md`. Tag each new video from
  its build script's voice (`voice="noah"` / `VOICE`). First read once 3+
  `noah` Shorts have curves (about a week after the third ships). Compare
  only within the sentence-2 "keeps back" group. Also note whether
  `noah`'s ~6% slower read pushed any Short past its planned length.
- **Sentence 2 holds only sometimes.** Read every new withheld-or-reversal
  Short's curve and note where its cliff lands *inside* sentence 2 (Bear and
  Stress-o-meter both fell during sentence 2 itself). Curves still due:
  Decentralized AI, History, Meme coins.
- **E8, trend long-forms.** Read each new trend long-form at 7 days: YouTube
  views and `youtube-audit traffic <id>` search share. Fail line is in the
  entry.
- **GTA 6 long-form decay.** Pull traffic sources again: does search hold
  after the 11-19 launch, when many more videos will answer "dacity coin"?
- **Crypto Facebook.** Every crypto upload since 10-02 has failed (1-38), and
  tinnitus passes on the same workflows, so the cause is at the page. The
  user checked on 10-23: no visible restrictions, and both pages are typed
  Business, so the type cannot be what separates them. Re-read the next two
  uploads; if they also fail, compare what changed on the crypto page around
  10-02 (posting rate, topics, any shared or reposted content).
- **E11, demand-led topics (from 2026-10-25).** Tag every new video's
  `DEMAND` line. First read once a channel has 3 demand-backed long-forms
  14 days old. Also check that each run extended each demand map by one
  branch, and that standouts have real medians, not `?`.
- **Was GTA 6 on-audience?** Crypto subscribers around 10-20 to 10-27, and
  whether the uploads after it took suggested traffic from `FXW9Zd5vjYk`.
  If its viewers did not come back, E8 trend topics are reach, not channel
  growth, and the E8 entry says so.
- **Funnel.** Ask the user for GA4 sessions from youtube.com, facebook.com
  and tiktok.com on each site since 10-23, the first funnel reading.
- **Zen sessions on Facebook and YouTube.** TikTok is closed (5 of 5 in
  batches). Keep counting Facebook long/reel per session against the 29k
  outlier, and YouTube suggested growth on the 09-05 session (388 on 10-23).
  The user's sessions focus runs to ~11-12.

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
- **Parked 2026-10-12: localization (other languages).** The user deferred it:
  too much work for the result at current channel size. Dubbing multiplies
  existing reach (YouTube: ~25% of watch time from dub tracks on channels that
  use them), so on a channel with 4-6 subscribers it adds next to nothing.
  **Re-raise it when any of these holds:** a YouTube channel passes ~1k
  subscribers; a long-form video passes ~5k views; Studio's geography report
  shows 15%+ of a channel's views from non-English countries; or sound
  sessions become a regular format (they have no speech, so they would only
  need a translated title and description, and that is the cheapest test).
  What was found on 2026-10-12:
  - **Automatable:** translated title and description (Data API
    `localizations`; `youtube-audit/src/edit.ts` already sets
    `defaultLanguage`), translated captions (`captions.insert`, from the SRT
    every build already writes), and the dub audio itself (Kokoro has ES, FR,
    HI, IT, PT-BR, JA voices).
  - **Studio only, by hand:** uploading the dub track (Languages → Add dub)
    and per-language thumbnails. Both need Advanced features. An existing
    YouTube auto-dub has to be deleted before our own can go up in that
    language.
  - **Order to test in:** metadata only, then captions, then audio. Crypto
    long-form → ES + PT. Localize thumbnails only where they carry text.

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

## Status 2026-10-23

- **E1 (redacted hook): unchanged.** The only new hooked Short
  (Decentralized AI, a placeholder `[one job]`) has no curve.
- **E2 (sentence 2): weakened, the "no overlap" claim retired.** Two
  compliant Shorts failed: Bear market (keeps back "one number", half gone
  7.0s) and Stress-o-meter (a task like Jaw's, 8.5s). Halving, the 10-11
  prediction, held (22.3s from a 166% open). Count across both runs: 6 of 8
  withheld/reversal Shorts hold, 0 of 6 verdicts. A withheld sentence 2
  seems to be needed, but it is not enough on its own.
- **E3 (cold close): no comparison possible.** Every new Short closes cold,
  so there is no question-close cohort left. Openings 103-109% except
  Halving (166) and Forest (182). Leave as is.
- **E4 (search-question titles): holding on reach,** but see the 10-23
  correction: the long-form "search title" cases were browse until GTA.
- **E5 (openers): no opener effect yet.** Search now has 1 hold (Jaw) and
  2 fails (Musk, Bear). The fails have different sentence-2 shapes, so the
  opener still cannot be separated out.
- **E6 (drone thumbnails): parked.** The user dropped the Studio winner
  read on 10-23; the Studio test itself is not ended by that.

## E7 - Male voice on the article Shorts and long-forms

- **Started:** 2026-10-23. The voice is `noah` (`am_michael` on mia's exact
  recipe, 1.10 ENERGETIC), picked by the user by ear from eight male
  candidates (`5aa11fe`). Every video before then is `mia` (female,
  af_heart), which makes them the baseline.
- **Change:** the next 5 article pairs per channel read in `noah`, then back
  to `mia` until the user decides. Nothing else changes. Keep sentence-2 shape, opener rotation and
  topic choice on their usual rules, so the voice is the one thing that
  changed.
- **Judged by:** on YouTube, half-gone second and the 4-7s drop for male
  Shorts against `mia` Shorts *within the same sentence-2 group* (the
  baseline is the 8 withheld/reversal curves: half gone 7.0-28.8s, median
  ~16s). Also the TikTok batch (250 vs 770) and the Facebook pass rate
  (≥150), each read against that platform's own history.
- **No effect if:** after 4+ male-voiced Shorts with curves, their
  withheld-group half-gone falls inside 7.0-28.8s with a median within ~3s
  of the female group, and TikTok and Facebook land in their usual buckets.
  Then the voice is a matter of taste: keep whichever the user prefers.
- **Fails if:** the male withheld group's median half-gone is 4s+ below the
  female one over 4+ curves.
- **Confound:** the 10 `noah` pairs are consecutive, not alternated with
  `mia`, so a change in topic mix or channel age over those weeks lands on
  the voice too. Compare against the `mia` Shorts from just before, and say
  so in the verdict.
- **Status:** voice chosen and added; no `noah` video has shipped yet.

## E8 - Crypto long-forms on a freshly coined search term

- **Started:** 2026-10-23, on the user's yes. Built on one video: GTA 6
  `FXW9Zd5vjYk` (2026-10-20), 619 YouTube views in three days, with 178 of
  its first 206 from YouTube search for "dacity coin" and variants. The
  launch trailer coined that term five days before the upload.
- **Change:** pick some crypto long-form topics for a term that has just
  appeared and that few videos answer yet. Title the long-form with the
  exact term first. Rule text in `docs/video/projects/crypto.md`, "A trend
  works as a new search term". Nothing else about the build changes. The
  Short is not part of the test.
- **Judged by:** each trend long-form's YouTube views at 7 days, and its
  search share from `youtube-audit traffic <id>`. Compare against the
  non-trend crypto long-forms of the same period, which mostly sit at 4-16
  views.
- **Fails if:** the next 3 trend long-forms each take under ~150 YouTube
  views in their first 7 days, or under half of their views from search.
- **Also watch:** GTA 6's own search share after the 11-19 game launch,
  when many more videos will answer "dacity coin". It shows how long the
  window stays open.
- **Status:** not yet shipped.

## E9 - The engine overhaul (cinematic look and new features)

- **Started:** 2026-10-21 to 10-23, per the user, as a set of build
  changes, not a single switch: typed band chapter cards and a cinematic
  title (`7aed772`), a native outro with a TV-off ending (`a32f7b1`), an
  old-film surface on every shot (`24be9b7`), glitch and TV-static cuts
  (`695fb74`), then the reel beat, post cards, key-word moments and the
  spotlight beat (`8eb5c29`, `575fe9d`, `d553559`). One uploaded video used
  them as of 10-23.
- **Why:** the videos look better and more cinematic. Looking better is a
  goal in its own right, so this entry can only fail on retention and
  reach, never on taste.
- **Judged by:** per platform, new-engine videos against old-engine videos
  of the same format (Short or long, article or session), on their own
  platform's numbers. On YouTube Shorts: half-gone second and the 4-7s
  drop, within the same sentence-2 group. On YouTube long-form: average
  view % and half-gone. On TikTok: the 250/770 batch and anything over
  ~1,000. On Facebook: the pass rate (≥150).
- **Fails if:** after 5+ new-engine Shorts with curves, their median
  half-gone sits 4s+ below the old-engine median for the same sentence-2
  group. Or new-engine long-forms show a lower average view % than the
  old ones, which would point at the longer title and outro.
- **Confounded with E7 (`noah`), and this is the main problem.** Both start
  on the same videos. If the next 10 article pairs carry `noah` *and* the
  new engine, neither effect can be separated from the other. Separation
  only comes from videos that have one and not the other: new-engine `mia`
  videos (the one already uploaded, History or Meme coins if new-engine,
  every zen session, and every pair after the 5-pair `noah` test), and
  old-engine `noah` videos (none exist). Say "noah + new engine" in every
  verdict until those exist, and do not credit either alone.
- **External view, recorded 2026-10-25, before any data:** the Trenda
  talk behind E11 holds that a visual which does not clarify, prove or help
  the viewer follow is decoration, and that an audience looking to learn
  cares least about it. Glitch cuts, static and the film surface are that
  kind of visual. If E9 fails, read this first; if it holds, the talk is
  wrong for these channels.
- **Status:** started; one upload.

## E10 - Session thumbnails: a known technique against an invented name

- **Started:** 2026-10-24, by the user, as a Studio Test & Compare on
  Nebula Pulse `r7NqyOv5_9Y` (published 10-22, 5 YouTube views on day two).
- **Change:** one variable, the thumbnail's lead words. A: the current
  "NEBULA PULSE" over a small "4-7-8 BREATHING". B: "4-7-8 BREATHING" as
  the lead, with "NEBULA PULSE" small or gone. Same layout, same "20
  MINUTES" circle, same background. The title is not changed.
- **Why:** the user's hypothesis. The best tinnitus long-form, "4-7-8
  Breathing + White Noise" `rvYOnvp7ufY` (388 views, growing: 56 on the
  latest day, 193 from suggested), leads with "4-7-8 BREATHING". The newest
  session leads with a name nobody knows. The sessions that lead with a
  known term (4-7-8, rain) have done better than the invented names
  (Jungle Waterfall 8, Forest Chorus 24, Nebula 5).
- **Evidence against it, written before the result:** Waterfall + 4-7-8
  `DKzUkSqIKS8` carries almost exactly the hit's thumbnail and has 28. So the
  lead words cannot be the whole story. Suggested traffic picked up one
  video and not the other.
- **Judged by:** Studio's winner (watch-time share) and each variant's
  share, which only the user can read. Then CTR from the Studio CSV, against
  the other sessions.
- **Holds if:** Studio picks B, the 4-7-8 lead. Then lead future session
  thumbnails with the technique or sound people know and keep invented names
  small, as a rule in `docs/video/thumbnails.md` once a second session agrees.
- **Fails if:** Studio picks A or calls it inconclusive. Then the lead words
  are not the lever, and the next thing to test is the layout (the "20
  MINUTES" circle takes about half the width, so the topic words stay small
  at 320px).
- **Constraint:** no API title or thumbnail writes to `r7NqyOv5_9Y` while the
  test runs.
- **Baseline, 10-24** (all the same layout; CTR waits on the Studio CSV):

  | session | published | lead words | YouTube views | top source | CTR |
  | --- | --- | --- | --- | --- | --- |
  | 4-7-8 + White Noise `rvYOnvp7ufY` | 09-05 | 4-7-8 BREATHING | 388 | suggested 193 | - |
  | Waterfall + 4-7-8 `DKzUkSqIKS8` | 09-14 | 4-7-8 BREATHING | 28 | suggested 20 | - |
  | Cat Purring `DQohsxR94NQ` | 09-28 | CAT PURRING | 17 | suggested 9 | - |
  | Rain `qaodCuHY6ss` | 10-12 | RAIN SOUNDS | 41 | suggested 24 | - |
  | Jungle Waterfall `6zJGsj3aCTU` | 10-15 | JUNGLE WATERFALL | 8 | - | - |
  | Forest Chorus `GIOaF-uas1s` | 10-15 | FOREST CHORUS | 24 | suggested 17 | - |
  | Nebula Pulse `r7NqyOv5_9Y` | 10-22 | NEBULA PULSE | 5 | - | - |
- **Status:** running since 2026-10-24 (user added variant B in Studio).

## E11 - Topics picked on demand evidence

- **Started:** 2026-10-25, every pair suggested after this date.
- **Change:** `workflow.md` step 1 now crosses `tools/topics.py` with the
  channel's demand map (`docs/video/demand/`). Every candidate carries its
  demand evidence - a standout at 3x+ its channel's median, one of our own
  standouts, or a brand-new term (E8) - or is labelled "no evidence". A
  mechanism with no demand is bridged to the outcome the viewer searches.
  The build script records it in `DEMAND`. The long form also gets a feed
  check at the handover (our thumbnail beside the top three results).
  From the same day, a standout named in `DEMAND` gets a **teardown** before
  the script (`demand/teardowns/`, from `youtube-audit transcript`), and a
  covered article can be **re-angled** onto the promise that wins. The
  first candidate is the spike re-angle. Judge re-angles against the video
  they replace, on the same article.
- **Why:** external research (a talk by Jake Trenda, a YouTube agency
  running 100+ channels, reviewed by the user 10-25): demand first, then
  packaging, then a video that keeps the promise. Locally, every outlier
  this pipeline has had came from demand it did not plan for (GTA 6 search,
  4-7-8 suggested), and topics were picked from what had no video yet.
- **Judged by:** YouTube long-form views at 14 days and the `traffic` split,
  demand-backed against "no evidence" videos of the same channel and
  format. Long-forms first, because search and suggested are where demand
  shows; Shorts are read too but not judged on it. Also the share of
  demand-backed long-forms passing Facebook's ~150 bucket.
- **Holds if:** after 5 demand-backed long-forms on a channel, their median
  14-day YouTube views is at least 2x the median of that channel's last 5
  "no evidence" long-forms (tinnitus sessions against sessions, explainers
  against explainers).
- **Fails if:** after those 5, the median is below 1.5x. Then the map's
  evidence is not transferring - check whether the videos borrowed the
  standouts' execution or only their subject before retiring it.
- **Confounded with E7 and E9.** Every pair after 10-25 is also `noah` for
  the first five and new engine. Compare demand-backed against "no
  evidence" videos built in the same period, not against the old baseline,
  and say so in the verdict.
- **Status:** started; no video built under it yet.
