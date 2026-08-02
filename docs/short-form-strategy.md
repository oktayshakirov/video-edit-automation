# Short-form strategy — TikTok and YouTube Shorts

Grounded in the channel's own numbers (pulled 2026-08-02), not general advice.

## What the data says

**Shorts are the channel.** 30 Shorts published since Jan 2026 = **19,566 views**.
Five long-form videos in the same period = **1,518 combined**. Berlin, the best
long-form ever made, did 727 — five separate Shorts beat it.

**Length is the dominant variable.**

| length | median retention | median views | n |
|---|---|---|---|
| **10–19 s** | **85%** | **693** | 15 |
| 20–29 s | 71% | 176 | 10 |
| 30–39 s | 38% | 141 | 2 |
| 60 s | 26% | 80 | 1 |

Roughly a quarter of retention lost per extra 10 seconds. The 60-second Black Sea
POV got 80 views at 26%; the 10-second Berlin Gleisdreieck got 2,473.

**The angle beats the scenery.** Same drone, same skill, 24× spread:

```
2,075  Deutsche Bahn Germany Train Delays   a joke, told with a text overlay
1,157  How NOT to fly a Drone               mistake / relatable
  798  Drone Hyperlapse Camera Tutorial     180% retention — it loops
  693  Drone Crash                          drama
   85  Golden Hour Drone Footage            pure scenery
```

**Cadence compounds.** The Feb 12–24 run (seven Shorts in two weeks) averaged
~1,800 views. Everything since May averages ~200. That tracks posting frequency.

**Every Short has an empty description and zero tags.** Thirty times over.

## Vertical format: crop, don't rotate

The top Shorts used three different framings and all performed:

- cropped vertical — Gleisdreieck (2,473), Sunny Day (1,734)
- rotated landscape — City Skyline (1,930)
- three shots **stacked** in the 9:16 frame — Hbf Montage (1,528)

So framing did not decide those outcomes and there is no format to be loyal to.
Given that, pick on friction:

**Default to cropping.** "Please rotate your phone" asks for an action in the
first second, which is the one second that decides retention — and retention is
the whole game on this channel. Never spend it on an instruction.

**Use the stacked layout** for shots that refuse to crop (below). It keeps the
horizontal composition intact and still fills 9:16 — already proven at 1,528 views.

**Rotated landscape stays available** for a single hero shot where the full
horizontal sweep *is* the content, but it is the exception, not the house style.

## Which clips crop well

Predicted from the motion classification already in the index. A 9:16 window
keeps 28% of the frame width, so the enemy is lateral travel — the subject
leaves the window.

| fit | clips | why |
|---|---|---|
| ★★★★★ | Hill Tower (orbit), City Above (vertical) | subject holds centre; vertical move suits a vertical frame |
| ★★★★ | City 7, City 11, City 6, City 12 (push-in) · Hills Monument, City 10 (pull-back) · City 1, 2, 5, 9 (hover) | centre-weighted or static — crop is a pure composition choice |
| ★★★ | City 8 | centre-weighted but drifts sideways |
| ★ | City 3, City 4 (lateral) | subject travels across the frame and exits the window |

**13 of 15 crop cleanly.** The two laterals are the stacked-layout candidates.

## How to choose the crop

`3840×2160 → 1080×1920` is a **native crop, no upscaling**, leaving 2,760 px of
horizontal freedom. That choice matters more than any other single decision, so
it should be measured and then reviewed — never guessed and never left at centre.

Proposed method, reusing the cached proxies:

1. **Interest map per frame** — edge/detail energy plus saturation, with sky
   suppressed (low detail, high brightness, upper frame). Sky is what a centre
   crop wastes half the frame on.
2. **Collapse to a horizontal profile** — sum over rows to get `interest(x)`.
3. **Pick the window** — the 28%-wide window maximising integrated interest,
   evaluated across the whole clip rather than one frame.
4. **Hold it still.** Take the time-median position. A crop that wanders reads as
   a mistake.
5. **Allow a slow pan only when the optimum genuinely drifts** — capped at a few
   px/second so it reads as an intentional digital pan, never as jitter.
6. **Contact sheet for approval.** Render the proposed crop as a still per clip
   and review the set in seconds. Same principle as `--dry-run` for the long-form:
   the machine proposes, the eye decides, and one number per clip overrides it.

**Do not chase a perfect automatic crop.** Composition is taste. The win is
getting from "centre crop, hope for the best" to "a sensible proposal you adjust
in ten seconds".

Zoom is a second lever: cropping at 1080×1920 rather than the full-height
1215×2160 gives a tighter, punchier frame — still native resolution, less sky.
Worth exposing per clip.

## Nine Shorts from the Plovdiv batch

| # | angle | clips | why |
|---|---|---|---|
| 1 | "Older than Rome, Athens and Constantinople" | Hill Tower orbit | strongest fact available; Plovdiv predates all three |
| 2 | "6,000 years of sunsets" | City 11 (sunset) | beauty plus the fact |
| 3 | The reveal | Hills Monument pull-back | tight → wide is the best retention structure there is |
| 4 | "How I got this shot" — DJI orbit mode | Hill Tower orbit | copies the 180%-retention tutorial format directly |
| 5 | "3 spots in Plovdiv you'd walk past" | City 3, City Above, Hill Tower | listicle; "Best Things to do in Germany" did 1,150 |
| 6 | Speed-ramp punch | City 11 push-in, 200%→2000% | the escalate, as the entire video |
| 7 | "Europe's oldest city, from 400 ft" | City Above | vertical move, vertical format |
| 8 | Golden hour vs blue hour | City 1 ↔ City 4 | the footage splits into two colour families — use it |
| 9 | Cross-promo tease | best 8 s + "full flight on my channel" | the only one that funnels to long-form |

Target **12 seconds**, hard ceiling 15. One to three shots. Make the last frame
resemble the first — the 180% and 140% retention pieces are people watching twice,
and an orbit or pull-back loops almost for free.

## Audio

- **TikTok — trending sound.** Still a real reach multiplier, and these are silent
  flights so nothing is lost. Match the pace, not the mood.
- **Shorts — own royalty-free music.** Trends matter far less there.
- **Voiceover — test on #1 and #4 only.** The best retention on the channel came
  from an instructional piece. Twelve seconds is about 30 words. Leave the pure
  beauty pieces silent with text.

## Text

Hook text **in the first frame**, not at two seconds. Six words maximum:
"Older than Rome. Older than Athens."

Burn it in for cross-posting *and* add native captions on TikTok — TikTok reads
on-screen text for topic classification, which burned-in text does not feed.

## Cadence and housekeeping

- **4 per week beats 12 in one day** — the Feb run proves it on this channel.
  Nine Shorts is two and a half weeks of posting.
- **Export per platform.** Never cross-post carrying a TikTok watermark.
- **Fill in descriptions and tags.** Thirty Shorts currently have neither.

## Tool roadmap — the `tiktok` profile

Genuinely different from `youtube`, not a resize:

- **9:16 reframe** with a per-clip crop centre in the project file, auto-proposed
  by the method above, overridable by one number
- **Contact sheet** of proposed crops, for approval before any XML is written
- **10–15 s targets**, 1–3 slots — replaces the bar-grid pacing model entirely
- **Hook-first ordering** — highest `motion_energy` clip in slot 1, the opposite
  of the long-form's calm open
- **Loop matching** — prefer a closing shot whose framing resembles the opening
- **Stacked layout** as a fallback for clips that will not crop
- **Text overlay slots** — needs a title effect UID captured from a real export,
  the same way the green-screen keyer was

## Test first, build second

Cut **three** by hand: **#1 (fact hook)**, **#4 (tutorial)**, **#2 (sunset beauty)**.
Same footage, three different reasons to watch. Post on consecutive days, compare
retention at 72 hours, then produce the rest in whichever format wins — and only
then automate it.

Given the tutorial format already returned 180% retention on this channel, #4 is
the one to beat.
