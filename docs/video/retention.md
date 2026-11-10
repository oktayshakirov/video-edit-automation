# Retention - keeping people to the end

The channel goal since 2026-11-10 is **videos people watch to the end**
(the editor). This doc holds what our own curves say about where people
leave, what the market's strongest videos do about it, and which of those
ideas are rules here and which are still experiments. The experiments and
their fail lines are in `video-performance-review/experiments.md`; the
numbers behind every claim below are in that skill's
`history/2026-11-10.md`.

## What our curves say (24 Shorts, 2026-10-01 to 11-08)

- **Most people are gone before the curve starts.** A Short's curve and
  average view cover a median 38% of its counted views. A counted view
  delivers **9.2s on tinnitus and 6.2s on crypto**. That is the number to
  move, and `youtube-audit retention` prints it.
- **3-8s is where the curve loses the most:** a median 34 points of the
  opening audience, and the steepest single step sits at 4.5-7s on 18 of
  24, whatever the script says there.
- **The ending is not where they leave:** the last 5 seconds cost a median 3
  points. Shortening a closing card helps those still watching, but there
  are few of them left by then.
- **Replay separates the Shorts that hold:** 6 of 7 opening at 125%+ held
  past 22s, none of the 17 under 125% passed 14s.
- **Sentence 2 decides the first exit:** a body-check task or a withheld
  answer holds, a verdict does not (`narration.md`).

## What the market does - external, a hypothesis until our curves agree

**MrBeast's production handbook** (leaked 2024, authenticity alleged, read
through its published summaries). The parts that apply to a faceless
explainer:

| principle | what it means here | status |
| --- | --- | --- |
| The first minute is the most important; it proves the thumbnail's promise | promise, proof, plan in the opening (`longform.md`) | rule already |
| Escalate as the video goes ("stair-stepping"), each part bigger than the last | order a long form's sections from strong to strongest; the best fact goes last, not first | experiment E20 (queued) |
| Withhold the outcome until the end | name in the first minute what the end will reveal, then pay it off last | experiment E20 (queued) |
| A re-engagement around minute 3 and minute 6 | on our 3-4 minute long forms, one pattern break at about a third and two thirds: a new beat type and a fresh question | experiment E20 (queued) |
| Quick cuts and simple content early | the first 8 seconds of a Short change picture about every 2 seconds | candidate, after E16/E17 |
| End abruptly | the cold close (`narration.md`); no slow outro | rule already |
| Never repeat a format back to back | opener rotation (`shorts.md`) | rule already |

**Practitioners on retention editing** (creator blogs and vendors, no
controlled studies): a pattern break every 15-90 seconds depending on the
source, a first re-hook around 25-35 seconds into a long form, open loops
that promise something later. Treat the intervals as heuristics.

**Shorts length** (vendor data, not peer-reviewed, and the sources disagree):
completion targets fall from ~40% under 15s to ~25% at 30-60s, and several
datasets find their best median views at 11-20s or 20-45s. That is why E17
tests 30-40 seconds rather than our current 41-72.

**Titles in capitals** (vendor and creator data): one or two words in caps
help in hype niches and hurt in education in one 2026 dataset; a whole title
in caps reads as shouting everywhere. Treble Health, the tinnitus category
leader, capitalises the search terms ("Why is my TINNITUS LOUDER IN ONE
EAR?"). That is why E19 tests one caps phrase on long-form titles through
Studio, on our own audience, rather than adopting it.

## Five channels to learn from

| channel | why it is on this list | the one thing to take |
| --- | --- | --- |
| **Kurzgesagt** (science, ~25M) | the strongest faceless explainer brand, and nearly every frame is drawn | custom screens carry an explainer; stock is the exception (`footage.md`, "Stock is at most half the shots") |
| **Zack D. Films** (Shorts, ~27M) | the faceless Shorts reference: 20-45 second animated "did you know" clips | one question per Short, answered fast, short (E17) |
| **Whiteboard Crypto** (crypto, ~1M) | our niche's animated explainer; its standouts sit at 2-4x its median (`demand/crypto.md`) | one concrete analogy per concept |
| **The Infographics Show** (~15M) | high-volume animated explainers built on countdowns and "what if" | a countdown is a promise the viewer waits out; it suits "N things" topics |
| **Coffeezilla** (crypto scams, on camera) | the lane our scam topics sit in; the evidence is on screen - documents, posts, pages | real pages in windows (`screencap`, the `post` beat, `window=`) |

Subscriber counts are approximate, from 2026 third-party lists.

## How a build uses this

1. **Shorts:** sentence 2 by `narration.md`; length and ending per the
   experiment running on that channel (E16 tinnitus, E17 crypto); no outro
   card (`shorts.md`).
2. **Long forms:** length per E18; packaging per `longform.md` and
   `thumbnails.md`; titles per E19 when the editor runs a Studio test.
3. **Every video:** stock clips are at most half the shots, and a stock clip
   can sit in a window (`footage.md`); `tools/script_check.py` checks the
   share.

Sources, read 2026-11-10: the MrBeast handbook summaries
(alexanderjarvis.com, tubefilter.com, creatorhandbook.net); Shorts length
(quso.ai, retensis.com, piktochart.com); retention editing (air.io,
pixflow.net); title capitals (air.io title study, vidIQ summary); faceless
channels (heydreaming.com, vidpros.com, outlierkit.com).
