---
name: video-performance-review
description: The recurring performance review of the AI-built videos, run 2-3 times a month - YouTube (Shorts and long-form, with retention curves), TikTok, Instagram Reels and Facebook for Tinnitus Help and Crypto Wiki, plus the drone channel when a drone experiment is running. Pulls the numbers, compares them against the last snapshot, judges the running experiments, turns findings into changes to the video build rules, tools and skills, reviews those changes with the user before applying them, and sets what the next run checks. Use when the user runs /video-performance-review, asks to "run the audit" or "a new audit", asks what is working and what is not, asks how the channels are doing overall, wants the regular review, or wants to plan the next round of video improvements. For one video, one platform, or a metadata change use video-views-audit; for building videos use video-tinnitus / video-crypto / video-drone.
---

# Video performance review

The loop that keeps the video pipeline learning. The user runs it **2-3 times a
month**, and its value comes from two things: **comparison over time** (every
run reads the last snapshot first and writes a new one), and **findings that
reach the build** (a finding that stays in a report changes nothing; the next
video is built from `docs/video/`, so that is where it has to land).

## Files

| file | holds |
| --- | --- |
| `history/YYYY-MM-DD.md` | one snapshot per run: the numbers per platform and per video, the cohorts, what the run found and changed |
| `experiments.md` | **Open checks** (what the next run must read), then the ledger: each experiment's start, change, judging number and fail line |

This folder is tracked in `~/Coding/video-edit-automation` (under
`.claude/skills/`, symlinked from `~/.claude/skills`), so snapshots and ledger
changes are committed like everything else.

## Where a finding goes

The build skills (`video-tinnitus`, `video-crypto`, `video-quiz`,
`video-drone`) point at `docs/video/` and deliberately do not restate it. **A
rule change goes into the doc, not into the skill.** Change a build skill only
when the run itself changes order or gains a step.

| the finding is about | change |
| --- | --- |
| script structure - sentence 2, endings, what a line may say | `docs/video/narration.md` |
| the Short - 9:16, openers, the hook, captions | `docs/video/shorts.md` |
| the long form | `docs/video/longform.md` |
| one channel - topics that work or flop, medical and claim limits | `docs/video/projects/tinnitus.md`, `crypto.md` |
| the order of a build run, or a new check in it | `docs/video/workflow.md` |
| a rule that can be checked from the script file | a tool in `tools/` plus a gate line in `workflow.md` (`tools/opening_check.py` is the pattern) |
| titles, descriptions, tags, publishing metadata | `video-views-audit` "settled" sections, and `longform/meta.py` if the generator is wrong |
| how to pull a number, or a platform's limits | `video-views-audit` |
| a subject or title format that does or does not draw viewers, ours or a competitor's | `docs/video/demand/<channel>.md` |

## The run

1. **Load the past.** Read the newest `history/` snapshot and all of
   `experiments.md`, **Open checks** first. Note today's date, days since the
   last run, and how long each experiment has run.
2. **Pull every platform** with `video-views-audit`'s procedures: both
   channels on all four platforms, and drone whenever a drone experiment is
   open. Do not skip a dull platform; Instagram went to zero without anyone
   noticing. **Ask the user for Studio's CSV export at the start**
   (Analytics, Advanced mode: Impressions and Impressions CTR per video, for
   each channel, since the last run). It is the only source of impressions
   and CTR, because the API refuses them, and without it a thumbnail cannot
   be judged. If the user skips it, say that every thumbnail verdict in the
   run is a guess. Pull `traffic <id>` for every long-form that moved, so a
   view is never credited to search or a thumbnail without knowing where it
   came from.
3. **Tag every video published since the last run from its build script**,
   because a video cannot be compared without knowing what it tried:
   - opener (redacted hook, Counter, Stamp, Split, Search, Flash, none) and
     the word it lands on;
   - sentence 2 **as the whole `SENTENCES` entry**. On 10-11, reading only the
     first clause misfiled Whale and put a wrong rule into a commit.
     `tools/opening_check.py <script>` prints both for a Short;
   - the last line (cold close or question), and the title shape (yes/no, how
     or why, named person);
   - the voice (`mia`, `noah`) and the engine (old, or after the 10-21
     overhaul), for E7 and E9;
   - **the demand evidence**, from the script's `DEMAND` line (a standout and
     its ratio, one of ours, a new term, or `None`), and the title format it
     borrowed, for E11, and whether a teardown in `docs/video/demand/teardowns/`
     shaped it. A script built before 10-25 has no line: tag it "no
     evidence (pre-E11)";
   - **the thumbnail**, for every long-form and session. Download it and look
     at it at 320px (`sips -Z 320`), the size people see. Record the lead word
     and whether it is a term people already know ("4-7-8 BREATHING", "RAIN
     SOUNDS") or a name we invented ("NEBULA PULSE"), roughly how many words
     it has, the layout, and anything that is unreadable at 320px. Put its
     impressions and CTR next to it when the CSV is in.
4. **Write the snapshot** to `history/<today>.md` in the shape of the last
   one: totals table, per-platform rows, the retention cohort with tags.
   **Then extend each channel's demand map by one branch** - the next
   unticked seed term in `docs/video/demand/<channel>.md`, searched and
   followed per `demand/README.md`, plus the channel medians for any
   standout still marked `?`. One branch per channel per run keeps the map
   growing without a session of its own. Add any of our videos that stood
   out to "Our own standouts" with its traffic source. Map rows are
   bookkeeping and are written without asking.
5. **Judge.** Each experiment against its own fail line: *holding*,
   *failed*, *too early*, with the numbers. Each Open check: answered or
   still waiting. **Check compliance before blaming a rule.** If the videos did
   not follow it, the rule was not tested.
6. **Classify every finding on the ladder** below, then draft the changes.
7. **Review with the user.** This is the checkpoint. Present:
   - the numbers against the last run, per platform, never mixed;
   - each experiment's verdict;
   - a **proposed changes** table: finding | evidence (which videos, how
     many) | rung | file | the change.

   Snapshot, ledger statuses and Open checks are bookkeeping and are written
   without asking. **Rule, gate, tool and skill changes wait for the user's
   yes**, and the user may take some and not others.
8. **Apply, then commit.** Only files this run touched; the repo often has
   unrelated work in progress, so stage by path. Two commits: build docs,
   tools and skills first, then the snapshot and ledger. Follow the commit
   style already in `git log`.
9. **Set the next run.** Rewrite **Open checks** in `experiments.md`: what to
   read next time and from what date its data will exist (a curve needs ~60
   views; a Studio test needs its end date). Tell the user the earliest date a
   new run would learn something.

## The ladder - how far a finding may go

| rung | when | where it lands |
| --- | --- | --- |
| **Observation** | 1-2 videos, no curve, or a cause not yet visible | the snapshot; an Open check if it needs a second look |
| **Experiment** | a plausible cause that a build change can test | a ledger entry, with the fail line written *before* the data |
| **Rule** | 3+ videos with curves agreeing and nothing contradicting, or an experiment that held its line | the build doc, with the evidence and the count written next to it |
| **Gate** | a rule that videos built *after* it still broke, and that can be read from the script | a check in `tools/` and a gate in `workflow.md`, with its output shown in the build handover |
| **Retire** | the data broke a rule | rewrite or remove it, saying why. Do not stack a new rule on a wrong one |

The gate rung exists because of 2026-10-11: the sentence-2 rule sat in
`narration.md` for ten days and four Shorts still broke it. They broke it
because the check was done from memory, not because it was ignored. A rule
that keeps being broken needs a check that runs against the file.

## What to look at

**Reach per platform, per format.** Which platform carries which format has
surprised this review more than once: Facebook carries long-form, TikTok
carries Shorts, Instagram carries nothing. Keep checking rather than assuming.

**Pass-or-fail distribution.** TikTok lands at ~250 or ~770 and Facebook at
~150-360 or ~7-70, rarely in between. Read a video against its own
platform's two buckets, not against an average. A pipeline TikTok over
~1,000 is the first real signal there.

**The opening on YouTube curves.** The drop from 4s to 7s and the second
when half the opening audience is gone. Since 10-11 the main thing
splitting Shorts is sentence 2, not the opener: compare openers only within
the group where sentence 2 keeps the answer back.

**The loop signal.** A curve opening well above 100% is being replayed;
around 100% means no loop.

**Reach and retention separately.** The highest-reach Shorts on 10-11 were
all the worst-retaining ones. The title earns the click and sentence 2
keeps it, so a finding about one says nothing about the other.

**Thumbnails, by CTR, within one format.** A thumbnail earns impressions
into clicks, so CTR from the Studio CSV is the number that judges it, and
only against thumbnails of the same format (sessions against sessions,
explainers against explainers). Views alone mislead. On 10-24 the 4-7-8 hit
(388) and its near-twin (28) carried almost the same thumbnail. Their
difference was suggested traffic, not the image. Read a thumbnail claim
together with `traffic`: a video fed by suggested or browse lives on its
thumbnail, while one fed by search lives on its title. A Studio Test &
Compare (E6, E10) is the only clean thumbnail comparison. While one runs on
a video, never write that video's title or thumbnail through the API.

**Why a hit worked, before more of it.** For any video of ours that stood
out, name the reason - subject, title format, thumbnail, execution or
traffic source - with `traffic` read first. The finding is the reason, and
the proposed change is a new subject or angle that keeps it, never a
sequel of the same video (`demand/README.md`, "Doubling down").

**Whether a hit was on-audience.** A hit whose viewers ignore every upload
after it is worth less than its views say. Check subscribers around its
publish date and whether the following uploads took suggested traffic from
it. An off-topic hit is reported as one and is not a direction to follow.

**The funnel to the sites is parked (the editor, 2026-10-27).** Do not ask
for Google Analytics numbers; reach and retention are the focus for now.
If the user brings it back, the reading is: too few views, views that do
not click through, or clicks that leave.

## Evidence standards

- **Curves over averages.** An average says a video lost people; the curve
  says at which sentence.
- **Read the whole script entry.** A clause is not a sentence (10-11).
- **No rule from fewer than three videos**, and write the count into the doc.
- **A tool's flag is a prompt, not a verdict.** `opening_check.py` flags
  Whale and Jaw, and both held.
- **Correct earlier runs in place, with a dated note.** Never correct them
  silently: the 10-01 "same hook" claim and the 10-11 Whale reading both
  have their corrections next to them.
- **Mark external research as external.** It is a hypothesis until this
  channel's numbers agree.
- **Look for the failures too.** A format or subject judged only on the
  videos where it worked proves any bad idea. Before a rule says "do more
  of X", list the videos that did X and did not stand out, ours or the
  map's, and say why they differ.
- **One change per experiment where possible**, and say so when a batch
  changed several things at once.
- **Tinnitus is health content.** No change may push toward promising a cure,
  a fix or relief, however much it would help retention.
