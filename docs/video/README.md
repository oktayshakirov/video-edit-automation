# The video docs

Three skills build videos - `/video-crypto`, `/video-tinnitus`, `/video-drone` -
and one publishes them, `/publish-video`. The skills are thin: they hold the
*order of the work*. Everything a build actually needs to know lives here, once.

## Map

| Doc | What it owns |
| --- | --- |
| `workflow.md` | The run itself: suggest, pick, script, render, review, hand off |
| `narration.md` | Writing a script to be spoken - silence, phrasing, banned phrases, pronunciation |
| `longform.md` | The 16:9 explainer: shape, chapters, timing, opener, outro |
| `shorts.md` | The 9:16 cut: crop, captions, the four beats that transfer |
| `beats.md` | The drawn graphics - `bars`, `grid`, `steps`, `checklist`, `compare`, `logos` |
| `footage.md` | Stock and site photos: screening, contact sheets, reuse, motion |
| `design.md` | Type, colour, layout, backgrounds |
| `audio.md` | Music, generated beds, sound effects |
| `thumbnails.md` | One per video, and how the pair share a source image |
| `troubleshooting.md` | Engine faults that already cost a re-cut once |
| `projects/crypto.md` | thecrypto.wiki: voice, copy, what the site gives you |
| `projects/tinnitus.md` | tinnitushelp.me: article explainers *and* sound-therapy sessions |
| `projects/drone.md` | Drone: the Final Cut long form and the vertical cut |

Read `workflow.md` first, then the docs for the format you are building. Do not
read all of them - most of a build touches four or five.

## Where a new lesson goes

This is the rule that keeps these docs from becoming what they replaced. The six
skill files this replaced totalled 6,827 lines, and 31 section titles appeared in
two to five files each - the same rule, copy-pasted, then edited in one copy and
not the others. Two of them had drifted into contradicting each other.

**One lesson, one doc, no exceptions.**

1. **Write it in the narrowest doc that owns it.** A crop rule goes in
   `footage.md`, not in `projects/crypto.md`, even when a crypto video taught it.
   A rule about the tinnitus voice roster goes in `projects/tinnitus.md`, because
   nothing else has that roster.
2. **Never cross-post a summary.** If a second doc needs the rule, link to it -
   `see footage.md` - and stop. A summary is a second copy that starts drifting
   the day it is written. That is exactly how the old files broke.
3. **If the code now prevents the mistake, do not write a rule at all.** A fixed
   bug is not documentation. Write it down only when the trap can recur - a
   judgement call, an asset that screens clean and is still wrong, a limit with
   no error message. Everything else belongs in the commit message.
4. **Record it in the same commit as the fix**, while the reason is still known.
   A rule with no reason attached gets deleted by someone later who cannot tell
   whether it still applies.
5. **Date anything settled by a decision** - "settled 2026-08-26" - so a future
   run can tell a decision from a guess.

When a rule turns out to be wrong, **replace it and say so in place**. Do not
leave the old one standing next to the new one; that is the state the thumbnail
rules were in, where one doc said never put the answer on a thumbnail and
another said put the title's question on it.
