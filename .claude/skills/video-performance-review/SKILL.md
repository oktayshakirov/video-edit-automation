---
name: video-performance-review
description: The fortnightly performance review of the AI-built videos on every platform - YouTube (Shorts and long-form, with retention curves), TikTok, Instagram Reels and Facebook (Reels and long-form) for both Tinnitus Help and Crypto Wiki. Pulls the numbers, compares them against the last snapshot, checks whether the running experiments worked, diagnoses what is and is not working, updates the video build rules where the evidence supports it, and plans the next phase. Use when the user runs /video-performance-review, asks how the videos are doing across platforms, asks what is working or not, wants the weekly/bi-weekly review, or wants to plan the next round of video improvements. For pulling the numbers from any one platform, or a single video's metadata, use video-views-audit; for building videos use video-tinnitus / video-crypto.
---

# Video performance review

A recurring review, every one to two weeks. Its whole value is **comparison
over time**, so every run reads the last snapshot first and writes a new one
last. Without that it is just another audit.

**Files in this skill:**

| file | what it holds |
| --- | --- |
| `history/YYYY-MM-DD.md` | one snapshot per review — the numbers, per platform, per video |
| `experiments.md` | the ledger: what is being tested, since when, what would prove it wrong |

**Where the rules it changes live** (`~/Coding/video-edit-automation/docs/video/`):
`narration.md` (script structure, sentence 2, endings), `shorts.md` (9:16,
the frame-zero hook), `longform.md` (16:9, the opener), `projects/tinnitus.md`
and `projects/crypto.md` (per-channel). Metadata rules live in the
`video-views-audit` skill.

## The run

1. **Read the previous snapshot and `experiments.md`.** Note today's date and
   how long each experiment has been running.
2. **Pull every platform** (procedures below). Record everything published
   since the last snapshot plus the running totals. Do not skip a platform
   because it was dull last time — Instagram went to zero without anyone
   noticing.
3. **Write the new snapshot** to `history/<today>.md` in the same shape as the
   last one, so the next run can diff them. **Record which opener each new
   video used** (redacted hook, Counter, Stamp, Split, Search, Flash) - it is
   read from the script's `opener=`/`hook=`, and without it E5 cannot be
   judged.
4. **Judge each experiment** against its own falsification line in
   `experiments.md`. Mark it *holding*, *failed* or *too early*. Write the
   verdict in the ledger with the numbers that decided it.
5. **Diagnose** — see "What to look at" below. Only curves and per-video
   numbers count as evidence; averages are a starting point.
6. **Check the scripts actually followed the rules** before blaming a rule.
   Read the `SENTENCES` of every new Short (opening two lines, hook, last
   line). On 2026-09-21 this is what separated "the rule failed" from "the rule
   wasn't applied".
7. **Update the build docs only where the evidence is strong**, and say in
   the doc what the evidence was. Retire or rewrite rules the data broke —
   do not just stack a new rule on top of a wrong one.
8. **Report to the user and propose the next phase**: what worked, what did
   not, what changes were made, what is being tested next and how it will be
   judged. Add any new experiment to the ledger.
9. **Commit** the `video-edit-automation` doc changes (only files this run
   touched — that repo often has unrelated work in progress). The skill folder
   is not a git repo; it just lives on disk.

## Where the numbers come from

**`video-views-audit` is the canonical how-to for every platform** - the
YouTube CLI and its `retention` curves, the TikTok per-video pull, the
Instagram reels grid, the Facebook videos tab, the accounts table, and each
platform's limits. It is not repeated here: two copies of a scraping
procedure drift, and this repo has paid for that before.

This skill is the **ritual around it** - the snapshot, the ledger, the
comparison over time, the decision about what changes next.

So step 2 above means: run `video-views-audit` over all four platforms for
both channels, then come back here to write the snapshot and judge the
experiments.

## What to look at

**Reach, per platform, per format.** Which platform is carrying which format
has already surprised this review once (see the snapshots) — Facebook, not
YouTube, is where long-form gets watched. Keep checking rather than assuming.

**The five-second cliff.** Every Short on both channels has lost 13-27 points
around 5s. The question each review answers is whether the running fixes
(frame-zero hook, sentence-2 partial answer) moved it. Compare *the drop at
~5s* and *half-gone second* between new Shorts and the pre-fix cohort in the
snapshots — not the average percentage, which mixes in everything after.

**The loop signal.** A Short whose curve opens well above 100% is being
replayed (Silence opened at 190%). Opening at ~100% means no loop.

**TikTok's test batches.** TikTok plays have landed almost exactly at ~250
or ~770 regardless of topic — those are the initial distribution pushes. A
video that clears ~1,000 is the first real signal of something working there;
flag it and study it.

**Rule compliance before rule verdicts.** A rule that was not applied has not
been tested.

## Evidence standards

- **Curves over averages.** An average says a video lost people; a curve says
  at which sentence. They have pointed at different sentences before.
- **Do not write a rule from fewer than three videos**, and say in the doc how
  many it rests on.
- **Mark external research as external.** It is a hypothesis until this
  channel's own numbers agree.
- **One change per experiment where possible.** If a batch changes the hook,
  sentence 2 and the ending at once, the review can say the batch improved but
  not which change did it — say that honestly.
- **Tinnitus is health content.** No experiment may push toward promising a
  cure, a fix or relief, however much it would help retention.
