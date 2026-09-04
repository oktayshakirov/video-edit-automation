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
disclaimer sentence entirely and close on the question alone - a Short has no
room to earn the line's own weight, and the long form it is paired with
already carries it, so the pair as a whole is never missing it. Do not mirror
the long form's disclaimer into a Short "for consistency"; the two formats
are deliberately asymmetric here.

**When that compliance line is spoken, put the disclaimer on screen too.** The
shot under it carries a payload statement — `Shot(clip=..., payload=("", "This
is not financial advice."))` — so it is seen as well as heard, every time. Run
it over a quiet contemplative clip (rain on a window, dark water), never a
person or a stage.

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

Sources: [vidIQ](https://vidiq.com/blog/post/write-youtube-video-script/),
[Storyflow](https://storyflow.so/blog/youtube-video-script-template-7-part-framework-retention-2025),
[Sumera](https://sumera.io/blog/youtube-hook-formulas-script-examples).

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
