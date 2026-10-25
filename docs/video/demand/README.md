# Demand maps - what the market already chooses to watch

Added 2026-10-25, from a talk by Jake Trenda (a YouTube agency running 100+
channels) that the user reviewed. **External research: a hypothesis until
this channel's numbers agree** (`video-performance-review`, evidence
standards). It is being tested as E11.

The problem it fixes: `tools/topics.py` lists the articles that have no video
yet, and that is all it knows. An article existing proves the *site* wanted
the subject. It does not prove that anyone chooses to watch it on YouTube.
The pipeline has been picking topics the way the talk's "before" clients
did - on what the audience should need - and every outlier this pipeline has
had came from a subject with demand it did not plan for (GTA 6 searched as a
brand-new term, the 4-7-8 session fed by suggested).

**The question every topic has to answer before a word is written:** *what
evidence says the people we want are already choosing to watch this subject
on YouTube?* If there is none, either change the subject or bridge it to one
that has it (below).

## The files

| file | holds |
| --- | --- |
| `demand/tinnitus.md` | the tinnitus map: standout videos, the subjects they prove, the formats seen, our own outliers |
| `demand/crypto.md` | the same for crypto |
| `demand/teardowns/<slug>.md` | one standout taken apart: its promise, opening, structure, what viewers rewatched and thanked it for, the failures beside it, and what our version keeps (below) |

They are research databases, appended to, never rewritten. Each run of the
search adds rows; `video-performance-review` extends one branch per channel
per run so the map keeps growing without a dedicated session.

## The search - depth first, from the niche down

The map is built the way a crawler walks a site, so no corner of the niche is
missed:

```
niche
 -> seed searches (ask for a seed list of the terms the market uses)
     -> standout videos in the results
         -> that video's channel: its other standout videos
         -> that video's recommendations
             -> ...until a branch stops producing anything new,
                then back up one level and take the next branch
```

1. **Seed list.** The words the audience uses for the problem, not ours:
   "ringing in ears at night", "tinnitus spikes", not "auditory gain". Keep
   the seed list at the top of the channel's map and tick each term off as
   its branch is exhausted.
2. **Search one term.** The fast route is the YouTube CLI, which scores every
   result against its own channel's median and marks the standouts:

   ```bash
   cd ~/Coding/youtube-audit && npx tsx src/cli.ts outliers "tinnitus spikes" --channel tinnitus
   ```

   About 120 quota units a search (the search alone is 100, of a 10,000/day
   budget an upload takes 1,600 of), less once channel medians are cached.
   The browser works too when quota is short. Note every **standout**: well
   above what its own channel usually gets (below).
3. **Open that channel**, sort by popular, note its other standouts. The
   channel's median of its last ~15 uploads is its baseline (RSS:
   `https://www.youtube.com/feeds/videos.xml?channel_id=<id>` gives the last
   15 with views - see `video-views-audit`, "Competitor teardown").
4. **Follow that video's recommendations** one level, note standouts there.
5. Back up and take the next result, then the next term.

Every standout becomes one row in the map. It is slow work, which is the
point of writing it down: a branch explored once is never explored again.

### What counts as a standout

**Views at least 3x the channel's own median**, on a video old enough to have
settled (over ~2 weeks). Raw views do not count: a 50k video on a 2M-subscriber
channel is that channel underperforming, and a 6k video on a channel that
gets 400 is a real signal. Write the ratio, not just the views. When the
median was not measured, write "ratio: not measured" rather than guessing.

`outliers` takes the median over the channel's last 15 settled uploads of the
same kind, Short or long. So a video several years old is compared against
the channel as it is *now*: a channel that has declined makes its old videos
look like bigger standouts than they were. Trust a recent standout more, and
read a ratio on a 10-year-old video as "this subject lasted", not as its size.

### What one row records

| field | why |
| --- | --- |
| title, channel, views, channel median, ratio, age | the evidence itself |
| **subject** | the thing demanded, in the audience's words |
| **title format** | the frame, with the subject removed ("Does X cause Y? What the research ACTUALLY shows") |
| **thumbnail** | what it shows at 320px, and its one promise |
| **execution** | how the video delivers it: length, number of points, drawn or filmed, raw or polished, list or story |
| **awareness** | problem-aware or solution-aware viewer (below) |

The execution field is not optional. The talk's own example: an "I made 300
videos and learned this" title worked because the video then delivered 20-40
points; copies that kept the title and gave 3-5 points flopped. A title
copied without its structure is a different video.

## Reading the map

- **One standout is a clue, not a subject.** A subject goes on the
  "proven" list only when **2+ different channels** have standouts on it.
- **Look for the failures too.** For any format you mean to borrow, note the
  videos that used it and did *not* stand out, and why (weaker execution,
  wrong audience). Only researching winners proves any bad idea. Each format
  in a map has a "seen failing" column; "not yet looked" is an honest entry,
  an empty one is not.
- **Copy the reason, never the words.** For a format, write *why* that
  audience clicked: "a result they already want, faster than they thought
  possible" is why "so fast it feels like cheating" works for fat loss. Then
  ask whether our audience clicks for that reason. Most formats fail this
  test for one of our channels, and the map says so per channel.
- **The channel is one campaign.** A subject that would pull viewers who do
  not care about the rest of the channel (an off-topic hit) can top the view
  count and still be the least valuable video, because those viewers ignore
  every upload after it and the channel's satisfaction signal drops. Prefer a
  subject the core viewer of the channel would also watch the next video
  after.
- **Go as broad as possible without losing the core viewer.** Specificity
  costs reach; pay that price only where the broad version would stop the
  real target viewer recognising the video is for them.

## Awareness - when the subject we want to explain has no demand

The audience can want an **outcome** without knowing the **mechanism**. Most
of our articles explain a mechanism (auditory gain, habituation, notched
sound; custody, validators, slippage). If a mechanism has no demand of its
own, do not drop it and do not make it anyway - **bridge it to the outcome
the viewer already searches for.** The talk's example: an insulin doctor's
channel took off on "If you don't understand insulin, you don't understand
fat loss": fat loss carries the demand, insulin is the new reason to click,
and the unfamiliar mechanism made the video stand out from every other fat
loss video rather than weaker.

**The outcome may be named, never promised.** On tinnitus the outcome is the
subject the sufferer searches ("tinnitus at night", "will it go away"); the
video promises understanding, never relief (`projects/tinnitus.md`). On
crypto the outcome is understanding or not getting burned, never profit
(`projects/crypto.md`). A format whose whole pull is a promised result - "so
fast it feels like cheating" - is closed to both channels.

## Packaging - the promise the title and thumbnail make together

Demand is the opportunity; packaging decides how much of it a video takes.
YouTube shows ~20 options and one gets clicked.

- **Title and thumbnail make one promise.** The thumbnail is read first and
  has to say who it is for and what changes in an instant; the title
  qualifies the exact problem.
- **Judge it against the feed it will actually sit in.** Search the
  long-form's title query, take the top results, and look at ours next to
  them at 320px. If ours does not stand out, or makes the same promise as
  the top result with less proof, revise before shipping. `workflow.md`
  step 4 runs this at the handover.
- **The opening keeps the promise.** After the click the question is
  "should I keep watching": promise (confirm what they clicked for), proof
  (why this video can deliver it), plan (where it is going).
  `longform.md`'s three-phase opening is the same shape; the talk adds
  that the proof step is the one usually missing.
- **The target is a satisfied viewer, not CTR or retention.** Those are
  noisy readings of whether the video kept the promise the packaging made.
  An overpromising title raises CTR and lowers satisfaction, and YouTube
  stops testing the video. A raw promise needs a raw video; a polished
  promise needs a polished one.

## Teardown - take a standout apart before making our version

A row in the map says *that* a video worked. A teardown says *how*, so our
version keeps the reason and not only the subject. Do one before scripting
any video whose `DEMAND` line names a standout.

```bash
cd ~/Coding/youtube-audit && npx tsx src/cli.ts transcript https://youtu.be/<id>
```

It writes `research/transcripts/<date>__<title>__<id>.md` in that repo:
metadata, chapters, the full transcript in 30-second paragraphs, words per
minute, the top comments and, when YouTube has one, the "most replayed"
heatmap. No `--channel` is needed (it reads the public page through
`yt-dlp`, not the API). **That file is someone else's words**: it stays
there, gitignored, and never enters this repo or a script.

Then write the teardown into `demand/teardowns/<slug>.md` (template below)
in our own words. Read in this order:

1. **The promise.** What title and thumbnail promise together, in one
   sentence, and the viewer's awareness level.
2. **The opening against the promise.** When the title's promise is
   restated, what the proof is (why trust this person), and whether the plan
   is spelled out. Time each from the transcript stamps.
3. **The structure.** Chapters, number of points, length, pace (wpm), where
   the turn is, how it ends and what the call to action offers.
4. **What viewers rewatched and skipped**, from the heatmap. Map peaks and
   troughs onto the transcript paragraph at that time. Peaks are the part
   people came for; a trough in the middle is a section that did not keep
   its place.
5. **What satisfied them**, from the comments. Comments thanking it for a
   specific thing name what the promise was really about. Comments saying it
   did not deliver are the warning.
6. **The failures beside it.** From the same `outliers` search, the videos on
   the same subject that did *not* stand out (under 1x). Their titles and
   openings against the standout's: what did the standout do that they did
   not? This is the negative evidence, and it is what stops a teardown from
   copying the luck along with the method.
7. **Our version.** What we keep (the promise, the structure, the length
   class, the kind of proof), what we cannot have (a doctor on camera, a
   patient's story) and what replaces it (cited sources on screen, a drawn
   mechanism), and what the medical or financial rule changes.

**Ours is never theirs reworded.** The script comes from our article, in our
words, with our sources. The teardown takes the *shape* - promise, order,
number of points, the kind of proof - and nothing else. A sentence that reads
like theirs is rewritten from the article. This is both the law and the
point: a reworded copy gives the viewer no reason to pick ours.

### Template - `demand/teardowns/<slug>.md`

```
# Teardown: <their title>
<channel>, <views> views, <ratio>x its median, <age>. <url>
Transcript: youtube-audit/research/transcripts/<file> (local only)

## The promise
## The opening (promise / proof / plan, with times)
## The structure (chapters, points, length, wpm, the turn, the CTA)
## Rewatched and skipped (heatmap)
## What satisfied viewers (comments)
## The failures beside it
## Our version - keep, cannot have, replaced by, rule limits
```

## Doubling down on a hit

When one of ours stands out, the next video is not the same video again.
Name **why** it worked - the subject, the format, the packaging, the
execution, or the traffic source (`traffic <id>`) - then find a new subject
or angle that keeps that reason. GTA 6 worked because it answered a
brand-new search term almost nobody else answered (E8); doubling down is the
next brand-new term, not another GTA video.
