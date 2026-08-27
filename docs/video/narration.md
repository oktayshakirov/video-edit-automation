# Narration craft

How a script is written to be *spoken*. Applies to every project and both
formats; the per-project safety limits sit in `projects/*.md`.

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

## Do not write a two-word imperative for a synthesiser to read

"Do not." was written as its own sentence with a 0.90 after it, straight out
of this doc's own advice about imperatives landing in silence. On the page it
is the strongest line in the section; read by Kokoro it is **two syllables and
then nothing**, and the user's note was that it loses the human sound of the
voiceover. A person saying "Do not." carries it with emphasis and a falling
pitch, and there is no emphasis to give.

**Write the full sentence and let the gap do the work.** "Do not make that
mistake." is the same beat, still lands on its own, and gives the synthesiser
enough to read as speech. The gap table is unchanged - what changed is that a
fragment cannot cash the pause the table buys it. This does not retire the
imperative rule; it bounds it: **an imperative needs a subject and a verb.**

## A tip needs a reason before it is a tip

The first cut went straight from the custody beat into "turn on two-factor,
start small, withdraw the rest" and the user's note was that it arrives with no
introduction. A list of instructions with nothing saying *why* reads as generic
advice, and generic advice is the thing an explainer is supposed to not be. One
sentence fixes it, and it should tie back to the beat above rather than being a
new topic: "You cannot change who holds the keys. You can change how much they
are holding."

## Hold a word by writing a pause, not by respelling the vowel

The outro's "So - would you rather..." was asked to sound like a drawn-out
"soo would you rather", for a more human close. **Respelling does not work:**
espeak reads `Soo` as `sˈuː` ("sue") and `Sooo` as `sˈuːoʊ`, both the wrong
vowel, and Kokoro has no per-phoneme duration control.

What does work is punctuation, measured in the engine rather than guessed:

| written | pause after "So" |
|---|---|
| `So -` | **none** — it runs straight through |
| `So,` | ~150ms |
| `So...` | ~170ms, vowel intact |

So the hold is a *pause*, not a longer vowel. The ellipsis goes in the **spoken**
half of a `(caption, spoken)` pair so the caption keeps its hyphen, per this
file's own "only a hyphen goes on screen" rule.

## Sentences are synthesised in runs, not one at a time

**The user's note was that the presentation "doesn't sound human" and that the
breaks are unnatural, and the largest cause was architectural rather than the
model.** `build_narration_aligned` used to call the synthesiser once per
sentence and concatenate the results with `anullsrc` silence. Two consequences,
both measured on the proof-of-stake script:

- **Every sentence was a cold start.** Five consecutive lines synthesised alone
  opened at 258, 271, 229, 227 and 246 Hz — every one a fresh sentence-initial
  reset, high in the speaker's range. The same five as one utterance sat at
  199 Hz falling to 193: a calm register with real paragraph declination. A
  script of cold starts is what "reading a list" sounds like.
- **Every pause was digital zero.** Each sentence was also hard-trimmed at both
  ends by `librosa.effects.trim`, so the audio floor dropped to absolute
  silence roughly sixty times in a 3:30 video, with no breath and no decay.

Sentences now go to the model in **runs**, and a run breaks where the *script*
asks for a real pause (`RUN_BREAK_GAP`, 1.0s) — a checklist's verdict silence
or a statement card is a written beat and the silence is the point, so joining
across it would smooth away what the gap was buying. Inside a run the model's
own breaths are kept and `_pad_pause` tops them up to the scripted `gap` by
inserting into the **quietest point** of the existing pause, so the decay
before and the onset after survive. Measured on the same seven lines: internal
absolute-silence gaps went 7 → 3.

**What this does not fix.** Kokoro is an 82M model with no prosody control and
no emotion parameter. The register and the joins are much better; the ceiling
is unchanged. Anything beyond it is an engine change, and the options
researched — ElevenLabs (word-level timestamps, `<break>` tags, an IPA
pronunciation dictionary; needs a paid tier for monetised video), Chatterbox
(MIT, but CPU-only on Apple Silicon) and Orpheus (Apache, needs a GGUF/LM
Studio path) — are a decision the user takes by ear, not a default to change.
`synth_phrase` remains the only place an engine is named, so the swap stays
cheap whenever they want it.

## A one-word sentence has nothing to fall from

**"Money." was flagged as sounding like a question rather than a statement.**
Measured on the shipped audio, the pitch runs 211 → 255 → **274** → 200 → 206
Hz: it peaks mid-word and ends roughly *level*. A contour that does not resolve
downward is heard as unfinished, which is heard as a question.

This is the same failure this doc already records for "Do not." — a fragment
cannot cash the pause the gap table buys it — arriving on a one-word *answer*
rather than a one-word imperative. Run-based synthesis helps, because the line
now falls out of the sentence before it instead of starting cold. But the rule
generalises: **a one-word sentence is a rhetorical device on the page and a
liability in the mouth.** Keep it only where the preceding line hands it real
momentum, and never as the first line of a run.

## Check every proper noun with espeak, not just the risky-looking ones

`Ethereum` shipped mispronounced. It phonemizes to `ˌiːθɚɹˈiːəm` —
"ee-thuh-REE-um", stress on the wrong syllable — where `Etheerium` returns the
correct `iːθˈɪɹiəm`. The phoneme rule was being applied only to words that
*looked* risky: initialisms, tickers, invented brand names. **A proper noun
that looks like an ordinary English word is exactly where this hides.** Respell
in the spoken half of a `(caption, spoken)` pair.

## Ethereum, and checking a brand name you think you know

`Ethereum` phonemizes to `ˌiːθɚɹˈiːəm` — "ee-thuh-REE-um", stress on the wrong
syllable and a schwa where the vowel wants to be `ɪɹ`. It shipped, and the user
caught it.

    espeak-ng -v en-us -q --ipa "Ethereum"    # ˌiːθɚɹˈiːəm   wrong
    espeak-ng -v en-us -q --ipa "Etheerium"   # iːθˈɪɹiəm     right

The respell goes in the **spoken** half of a `(caption, spoken)` pair, exactly
as `Binance`/`Bynanse` already does. The wider lesson is that this doc's
phoneme rule was being applied only to words that *looked* risky — initialisms,
tickers, invented brand names. **`Ethereum` looks like an ordinary English
word and is not one.** Check every proper noun in the script, not the ones that
feel like they need it.

## Titles: a question gets a question mark, every time

The channel is consistent about this and it is worth keeping that way —
`How Loud Is Too Loud?`, `Does Tinnitus Go Away?`. The trap is a title that is
*phrased* as a statement but *reads* as a question: `Why It Is Worse at Night`
was drafted that way and had to become `Why Is It Worse at Night?` before
upload. If the second half of a colon title is an implied question, invert it
into a real one and punctuate it. The rising intonation is free.
