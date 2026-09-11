# Narration craft

How a script is written to be *spoken*. Applies to every project and both
formats. How the synthesiser then behaves is `voice.md`; the per-project safety
limits are in `projects/*.md`.

## Narration craft: write it to be spoken, not to be read

**This is the section to read before writing a single line of script.** It was
written on the tinnitus channel, where a cut was reviewed as "sometimes very
good, sometimes very bad" on exactly this axis and every instance was one of
the five faults below. **None of it is site-specific** - it is about how a
synthesiser reads a page, and the crypto scripts have the same faults. A
synthesiser has no judgement: it reads what is on the page at the pace the
`gaps` list tells it to. Everything that makes narration sound human has to be
**written into the script as words and numbers**, because there is nowhere else
for it to come from.

### 1. A pause is a punctuation mark and it belongs where the meaning turns

The old table gave values by *category*. Values are not the problem — placement
is. These are the four places a gap is load-bearing, and all four are worth
auditing in every opener:

| where | gap | why |
|---|---|---|
| before a line that **contradicts** the one before it | **0.85-1.00** | "Not your keys, not your coins." / "But almost nobody checks." The reversal is the whole point and it needs the silence to reverse *into* |
| after a **two- or three-word imperative** | **0.80-0.95** | "Do not." lands or it does not; a 0.34 runs the next sentence over the top of it |
| before a line that **answers** a question just asked | **0.70-0.90** | the gap is what makes it an answer rather than a continuation |
| between two **halves of one argument** ("not X - it is Y") | **0.55-0.70** on the first half | too short and it is one breathless sentence; too long and they stop being a pair |

**Read the section aloud with a stopwatch before setting the numbers.** Where
you naturally stop, write the gap. Where you naturally run on, write 0.34. This
takes two minutes per section and it is the single highest-value thing in this
file.

**A default-0.34 script is a first draft, never a shippable one.** If a
`Section` has no `gaps=` list, it is not finished.

### 2. Chapter titles have to be written as openers, because they cannot be read as one

Kokoro has no prosody control. There is no way to *direct* a lift into the
voice, so **the opener quality has to be in the words**. Three levers, and use
all three together:

- **A discourse marker on the front of `spoken_title`.** "So", "Now", "But",
  "And" - the words a person actually starts a new thought with. `spoken_title`
  exists precisely so the card can read as a clean headline while the voice
  says something conversational. `title="Nobody has passed it"` /
  `spoken_title="So has anyone ever actually proved it?"`.
- **A question mark, on anything shaped like a question.** Rising intonation is
  free and it is the strongest opener signal the synthesiser has. This is now a
  hard rule: **every chapter title that is a question gets a question mark, on
  the card and in the spoken line.**

  **The trap is the title phrased as a statement that a reader hears as a
  question**, and it is easy to miss because it scans fine on the page. Two
  shipped on the tinnitus channel before being caught on the title list: "Why
  it feels worse with them in" and "When it is not a settings problem" - both
  are answers to a question the card never asks. Inverted, they gain their
  mark and their lift. "Where the money is actually made" on this channel is
  the same fault. **Read the whole
  title list on its own, out of the script, before rendering** - the fault is
  invisible inside a section and obvious in a list of seven.
- **Silence in front of it.** The card lands into whatever the previous
  section's last sentence left behind, so give that sentence **0.80-0.90**. A
  card arriving 0.34 after the previous thought is a new chapter nobody heard
  start.

`card_gap` (1.10 by default) is the silence *after* the spoken title. Leave it
unless the card is the video's turning point, where 1.30 is right.

### 3. Every beat needs a hinge sentence, and a `compare` needs two

**This is the 1:10 fault and it is the most damaging one**, because it makes
the graphic look broken rather than the writing look thin. The AirPods
`compare` read:

    "...It holds your keys."         <- last item of the left column
    "Decentralized."                 <- first item of the right column

The left column was praised and the right one was "quick, no break, just
reading it". Nothing was wrong with the beat. The narration simply **stopped
describing and started reciting**, because a bare column heading is a label,
not a sentence, and a person changing subject says so out loud.

**The rule: the chunk that opens the second column must be a hinge, not a
heading.** `name_columns=True` puts each heading on screen as its own revealed
item, which fixed *which* column the viewer is looking at; it did nothing for
whether the voice sounds like it changed subject. Put the turn in words:

    "Now compare that with a decentralized one."   not   "Decentralized."
    "For comparison, the decentralized side."      not   "Decentralized."

The same applies to the first column - "Take a centralized exchange." beats
"Centralized." -
and to every other multi-item beat. **A `steps` or `checklist` gets one hinge
sentence in front of it** ("So here is the whole check, and it is four steps"),
which already exists as the "say the point, then show the graphic" rule; the
new part is that **the beat's own first chunk also has to sound spoken.**

**The caption chunk count still has to match the reveal count**, so a hinge
does not get its own extra chunk - it is written *into* the chunk that was
already there. "Your earbuds." and "Now compare that with your earbuds." are
both one chunk and both reveal item four.

### 4. Say the whole name of a thing, every time

Half a product name is a guess the viewer has to make while the next sentence
is already playing. The AirPods cut said "cancelling" and "transparency" alone
and both were flagged as confusing.

On this channel that means the whole name of a product, a mechanism or a fee:

| write | never |
|---|---|
| a **hardware** wallet, a **custodial** exchange | a wallet, an exchange |
| the **network** fee, the **trading** fee | the fee |
| a **centralized** exchange | an exchange, when the contrast is the point |
| your **private** keys | your keys, on first mention |

The cost is two syllables. The saving is a viewer who does not have to
back-fill a noun. It found this on the tinnitus channel, where "cancelling"
and "transparency" shipped without "noise" and "mode" and both were flagged as
confusing; the failure mode is identical anywhere a product has a two-word
name and the script keeps one of them.

### 5. A number that is spoken must also be seen

Not every figure earns a `stat` or a `bars` beat, and the ones that do not used
to be said into the air and lost. `Shot(clip=..., note=("21M", "the whole supply, ever"))` draws a small figure
card in the lower left - the figure in the brand accent at display weight, one
plain-English line under it saying what the number actually *means*, on a short
vertical rule.

- **It is not `payload`.** `payload` is the 96px centred statement the shot
  exists for; a note annotates while the footage stays the picture. One shot
  should never carry both.
- **The gloss is the point.** "21M" alone is a number; "21M / the whole supply,
  ever" is the fact the number was standing in for.
- **Lower left, not lower centre** - centre collides with burned captions in
  9:16 and with the YouTube player's own SRT line in 16:9.

## Silence is punctuation, and it has to be written

`gaps` on the `Section`, one float per sentence. **Leaving every sentence at the
default 0.34 is what "monotone" means** — that was the user's word for the first
crypto-exchanges cut and it is the correct diagnosis: pace is the only prosody
a synthesiser has, so a script that never varies the space between sentences is
a script read at one pitch for four minutes.

The convention, applied to every section of that cut:

| gap | where |
|---|---|
| 0.34 | inside a thought — clauses of one idea, the items of a list |
| 0.45-0.60 | end of a thought, before the next one starts |
| 0.70-0.90 | before a line that has to land, and on a section's last sentence |
| 1.10-1.30 | before a single-word answer, or after a full-screen statement |
| 2.10-2.40 | a two-phase beat, so the verdicts have somewhere to land |

**Longer than 1.3 outside a beat is a hole, not a pause.** The first build of
this format learned that from the other direction — chapter cards sitting in
2.4s of silence made every section boundary sound like a dropout, which is why
the card titles are spoken. The same number that is right for a checklist is
wrong for a sentence.

Writing them costs one line per section and it is the cheapest quality change
available in this format.

**The table above gives values; the narration-craft section above gives
placement, which is the half that was missing.** A script can have a `gaps`
list on every section and still read as flat, because the numbers were spread
evenly instead of put where the sense turns.

## Silence is punctuation here too

`gap` takes a list, one per sentence, and **leaving every one at 0.34 is what
"monotone" means**. 0.34 inside a thought, 0.55-0.90 at the end of one, 2.10 for
a two-phase beat, and ~1.3 after a full-screen statement so it is allowed to
sit. A forty-second short has less room than a long form and needs the pauses
more, not less: the pauses are what stop three instructions in a row sounding
like one sentence.

## Phrases that are banned, and why one of them got here

**Never write "here is the question almost nobody asks about it".** It went into
three scripts before the user caught it. "About it" has nothing to attach to, so
it is not English, and the whole clause is a windup that *announces* a question
instead of asking one — which costs two seconds in the exact stretch where
retention is decided. Ask the question: "But who is actually holding it?"

The general rule behind it: **cut any clause whose only job is to introduce the
next clause.** "Here is the thing", "what you need to understand is", "the
question you should be asking" — all of them are the same tic, and second person
present tense does the work without them.

## The outro asks the question and stops

**This section is long-form's rule.** A Short's outro follows a different and
now better-evidenced rule - see "A Short's ending loops; it does not ask"
below - because a Short is optimised for the replay YouTube counts as watch
time, not for a comment, and the two goals want opposite last lines.

**The user's standing rule, on every channel.** The closing line is a real
question the viewer can answer in their head — "So, what do you think: would you
have asked to see the blockchain?" — and nothing else. No "let me know in the
comments", no "the sources are linked below", no "subscribe for more". Those
lines were a pattern copied from an early script; they spend the last seconds
of the video managing the viewer instead of leaving them with the thought. The
one exception is the bare compliance line where a topic needs it — "Nothing in
this video is financial advice." — which stands on its own with no "sources
below" tail. The description carries the link and the CTA; the narration does
not.

**The compliance line is long-form only. A Short never carries it.** The
user's note on the `perpetual-futures` short: shorts on this channel drop the
disclaimer sentence entirely and close clean, with nothing tacked on after
the video's own last line - a Short has no room to earn the disclaimer's own
weight, and the long form it is paired with already carries it, so the pair
as a whole is never missing it. Do not mirror the long form's disclaimer into
a Short "for consistency"; the two formats are deliberately asymmetric here.
(That short's own closing line was still a question, which the section below
now flags - the two notes are about different things and neither excuses the
other.)

**When that compliance line is spoken, put the disclaimer on screen too.** The
shot under it carries a payload statement — `Shot(clip=..., payload=("", "This
is not financial advice."))` — so it is seen as well as heard, every time. Run
it over a quiet contemplative clip (rain on a window, dark water), never a
person or a stage.

## A Short's ending loops; it does not ask

**Found by reading every shipped Short's closing line against its retention,
2026-09-11.** Split every Short on both channels by how it ends and the split
is nearly total:

| ends on | retention | example |
|---|---|---|
| an engagement question ("what do you think", "who do you blame", "where is she now") | **34-56%** | Whales 48%, Saylor 41% ("Tell me what you think."), OneCoin 34%, Ethereum 56% ("who do you blame?") |
| a flat statement or a directive ("save this", "try it", "get it looked at") | **82-152%** | Pulsatile 82% ("So don't just live with it - get it looked at."), Silence 118% ("Silence is not neutral. Try it in the next quiet room."), Mining rig 122% / Gaming headset 152% (both "Save this before...") |

Retention above 100% is YouTube Studio counting a replay as watch time - the
video looped. **Every Short that closes cold, with no question, is the one
that loops; every Short that closes by asking the viewer something stays
under 100% even when it did well.**

**Confirmed against the curves, 2026-09-11** (`youtube-audit`'s `retention`
command), which is what turns this from a correlation across averages into a
visible mechanism. Two Shorts of near-identical length:

| | opens at | closes at | final seconds |
|---|---|---|---|
| Silence, cold close | **190.4%** | **88.5%** | dead flat - no drop at all |
| Ethereum, "who do you blame?" | 128.1% | **25.0%** | -3.1, then -6.2 |

The question-closer **loses people during its own closing question** - two
drops inside the last four seconds - and only a quarter of its audience
reaches the final frame, against 88.5% for the cold close. The loop signal
tracks it too: 190% against 128%. So the ask is not merely failing to earn a
comment, it is actively spending the seconds that would otherwise have rolled
into a replay.

This also matches how the mechanism is documented externally: a loop is a video that does not visibly end, so the next frame
(its own first frame) reads as a continuation rather than a restart, and the
strongest loops chain a matching image, a matching motion, or an ending that
recontextualises the opening line rather than re-asking it. An explicit
question is the opposite of that - it is a full stop dressed as a sentence,
it tells the viewer the video is over and a response is now expected, and a
three-second sign-off on a 40-50s Short is 6-8% of the runtime spent
announcing the ending instead of extending it.

**The fix, and it costs nothing:** end a Short on the fact, the rule, or the
directive the video earned - never on "what do you think" / "tell me" / a
question inviting an opinion. The two mechanisms that work, in order of
strength:

- **Recontextualise the opening line instead of re-asking it.** The mining
  rig short's close ("Cheap adapter, expensive mistake.") answers its own
  opening arithmetic ("The part of a mining rig that burns houses down costs
  about two dollars.") without repeating the question - the viewer's last
  thought and first thought are now the same thought, which is what makes the
  replay read as continuous rather than as a restart.
- **A directive with a real reason to act, not a bare "save this."** It only
  works because the video just earned it - a how-to a viewer would want to
  reference again, or a rule worth remembering. A directive bolted onto a
  video that gave no reason to keep it is the outro-CTA problem in different
  words.

**This is a Short-only reversal of the long-form outro rule above, not a
replacement for it.** Long form wants the viewer to sit with a thought and
comment; a Short is judged on completion and replay, and a question that
would be the right close on the long form is the thing costing the Short its
loop. Keep both rules; apply the one that matches the format.

Sources: [Shortimize, YouTube Shorts retention](https://www.shortimize.com/blog/youtube-shorts-retention-rate),
[Virvid, looping structure](https://virvid.ai/blog/looping-structure-shorts-retention-2026).

## Name the subject in the first sentence, not on the first chapter card

**The myths cut opened on "You have probably heard at least one of these"
and did not say the word *tinnitus* until the card at 0:14.** The user's note
was to make it clearer what we are talking about, "specially in the beginning
of the videos", and they are right in the most expensive possible way: 74% of
viewers decide whether to keep watching inside the first 15 seconds, and more
than half of all drop-off happens in the first 60. Fourteen seconds of a
video that has not named its subject is the whole decision window spent on
nothing.

This is not the same rule as the three-phase opening already in
`longform.md`, and it is not covered by it. That rule is about
*pattern interrupt, promise, commit*; a script can do all three while still
being about an unnamed "it". **The subject noun goes in sentence one.**
"Almost everything you have been told about tinnitus is only half right"
does the pattern interrupt and the naming in one line.

**The same fault hides in chapter titles, and it is easier to miss there.**
"Myth: only loud noise causes it" - what is *it*? Every card in that cut had
the same hole, and read as a list they were a video about an unnamed
condition. Fixed by making each one a question that names its own subject:
"Is loud noise the only cause?", "Does tinnitus always go away on its own?".
That also satisfies the question-mark rule for free, because a title forced
to name its subject usually turns into a question on its own.

Two more things worth keeping from the retention research, both of which the
existing rules only half-cover:

- **Hook sentences run under ten words.** Not a stylistic preference - it is
  the same finding as "short, short, one longer that builds", stated as a
  hard ceiling for the opening span specifically.
- **Write the hook last.** When the body is finished you know exactly what
  the video delivers, so the promise can be specific rather than a tease.
  This is worth following literally: the myths cut's second-pass hook ("one
  of those is partly true, the other two are just wrong") is a promise that
  could only be written after the five myth sections existed, and it is a
  far better opener than the first pass's generic three-claim list.
- **Write every chapter's payoff before its setup, not only the video's
  hook.** The rule above is the general case of a wider one: a section that
  promises before it has confirmed what it delivers tends to promise the
  wrong thing. Draft the chapter card and the last sentence of a section
  first - the line that actually answers the question the card asks - then
  write backward into the sentences that earn it. A `Section` whose card and
  closing sentence do not yet exist is not ready to have its opening written.
- **A specific number or a named entity beats a vague claim, in a hook and
  everywhere else.** "A few patterns" persuades nobody; "three patterns" is
  checkable and therefore credible, which is most of why it lands. This
  channel already half-follows this on instinct - `stat` and `bars` exist
  because a number is the thing narration cannot make vivid alone (see "A
  number that is spoken must also be seen" above) - but it applies to the
  words too, not only the beats: prefer "one point one million coins" to
  "most of the early coins", prefer naming Ruja Ignatova over "the founder".
  A claim with nothing to check reads as marketing copy even when it is true.

Sources: [vidIQ](https://vidiq.com/blog/post/write-youtube-video-script/),
[Storyflow](https://storyflow.so/blog/youtube-video-script-template-7-part-framework-retention-2025),
[Sumera](https://sumera.io/blog/youtube-hook-formulas-script-examples),
[TubeAI, retention scripting](https://learn.tubeai.app/blog/youtube-script-writing-retention),
[Vugola, hook formulas](https://www.vugolaai.com/blog/hook-writing-tips).

## The payoff belongs in sentence two, not behind a setup

**Diagnosed from a real channel gap, not a style guide - and then confirmed
against the actual retention curve** (`youtube-audit`'s `retention` command,
2026-09-11). The caffeine-and-tinnitus Short opened on the title question, then
spent sentences 2-3 hedging and building the withdrawal-symptoms case before
sentence 4 revealed the actual point (withdrawal fakes the caffeine-culprit
signal). It shipped at 181 views and 20.3% average retention on a 57s video.

The curve says exactly where they went, and it is worse than the average
suggests. **100% of viewers are still there at 4.6 seconds. By 6.3 seconds
half of them are gone** - a 22-point drop at 5.1s, another 17 by 6.3s. Timing
the script against that: sentence 1 (the title question) ends around 2.4s,
and sentence 2 - *"Maybe - but quitting it suddenly might be the bigger
mistake."* - ends around 5.5s. **The exodus is the hedge.** They asked a
question, heard "maybe", and left. Nobody got near sentence 4.

Compare "Does Silence Make Tinnitus Worse?" (221 views, 118% average) on the
same channel: its curve **opens at 190%** - replays, the video loops - and
then decays *smoothly*, still at 128% by 13 seconds, with no cliff anywhere in
the opening. Its sentence 2 answers ("You get somewhere quiet and the ringing
gets louder") and sentence 3 reverses flat ("It did not."). Same channel, same
format, same length band; the difference is what sentence 2 did.
"Why Can You Hear Your Heartbeat in Your Ear?" (82%) does the same - sentence 2
names and validates the sensation ("has a name... pulsatile tinnitus"), no
hedge in front of it.

**So sentence 2 is not "early", it is the decision point.** The viewer is
deciding at roughly five seconds whether this video is going to tell them
anything, and sentence 2 is the whole of the evidence they have.

**The title-question opener (see above, and standing in every Short) is not the
hook by itself - it is the setup for one.** The line that answers it, flips it, or
names the thing has to be sentence 2. If the honest answer to the title question is
"maybe" or "it's complicated," say the complicating fact plainly instead of
signalling uncertainty - "Usually not - it's quitting it suddenly that backfires"
lands as fast as a flat "It did not" and is just as true as "Maybe, but...". Any
setup that has to run before the payoff (symptoms, mechanism, list of causes) goes
*after* sentence 2-3, never before it - restructure the sentence order, not the
content.

**A quick self-check while scripting:** read sentences 1-3 alone. If they do not
already contain the one thing a scroller would repeat to a friend, the payoff is
buried too deep - move it up, don't just trust that a good idea later in the script
will be reached.

## A tip needs a reason before it is a tip

The first cut went straight from the custody beat into "turn on two-factor,
start small, withdraw the rest" and the user's note was that it arrives with no
introduction. A list of instructions with nothing saying *why* reads as generic
advice, and generic advice is the thing an explainer is supposed to not be. One
sentence fixes it, and it should tie back to the beat above rather than being a
new topic: "You cannot change who holds the keys. You can change how much they
are holding."

## Titles: a question gets a question mark, every time

The channel is consistent about this and it is worth keeping that way —
`How Loud Is Too Loud?`, `Does Tinnitus Go Away?`. The trap is a title that is
*phrased* as a statement but *reads* as a question: `Why It Is Worse at Night`
was drafted that way and had to become `Why Is It Worse at Night?` before
upload. If the second half of a colon title is an implied question, invert it
into a real one and punctuate it. The rising intonation is free.
