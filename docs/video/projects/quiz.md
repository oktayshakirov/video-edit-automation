# The quiz format

**One article, three questions, four cards each, about a minute.** It runs on
both channels — thecrypto.wiki and tinnitushelp.me — and the only thing that
differs between them is a `Brand` and the safety rules further down this page.
There is no crypto quiz engine and no tinnitus quiz engine.

Everything general still applies: `workflow.md` for the run, `narration.md`
before writing a line, `voice.md` for the synthesiser, `audio.md` for the bed.
This page is only what is different.

## What it is, and what it is not

A quiz short is not an explainer with a question mark on the front. The
explainer formats buy their thirty seconds with a picture; this one buys them
by making the viewer *commit to an answer*. That is a stronger hook and a much
less forgiving one — a viewer who is being asked something and is not
interested leaves immediately, where a viewer watching a photograph will drift
for another ten seconds.

Three consequences, and they are the whole format:

- **The question has to be answerable by someone who does not know.** Four
  plausible options, not one real answer and three jokes. A viewer who can
  eliminate three options by reading them has not been asked anything.
- **The wrong answers are the content.** Each one should be a misconception the
  article actually corrects. This is why the format is tied to an article and
  not written from memory — "what people wrongly believe about this" is
  something the post already contains, and inventing it is how a quiz ends up
  teaching a wrong thing by implication.
- **The `answer` line is the payoff, and it is never "the answer is B".** It is
  the *because*. A viewer who got it wrong has to end the beat feeling
  informed, not caught out; a viewer who got it right needs something they did
  not already have. That line is the only place the article's substance lands.

## Shape

| | |
| --- | --- |
| Length | ~95-96s. Three questions, opening on a plain title card. |
| Format | 9:16 only. There is no long form — see below. |
| Voice | **`otis`** (bare `am_puck`, ENERGETIC chain). |
| Countdown | 6s (was 8s; brought down once the format had shipped and been watched). |
| Beat | `quiz.cards.QuizShot`, drawn across seven shots per question — see below. |
| Source | one article, `SOURCE_POST` set like every other project script. |

**Three questions, not five.** A question costs about thirty seconds — two to
ask, roughly thirteen to read four cards (letter and answer together as one
line, a pause between cards), six to wait, five to reveal and explain — so
five questions would run past two and a half minutes.

**The original estimate was 60s; the format has landed at ~96s across three
more rounds of real pauses.** That is the cost of the pauses being real, and
it was the user's call each time, after watching a cut that ran them
together. The only silence this engine can give a script is a scripted gap,
and each one is paid for in runtime; nothing recovers that time without
cutting a pause back to inaudible. The countdown moved the other way: it came
down from 8s to 6s once the format had shipped and been watched, which is 6s
recovered per question, 18s across three. It is still the largest single line
in the budget and the first thing to trade further if a run needs to come
down again.

**Voice `otis` — and the argument for a distinct one lost to the ear.** This
format was first built on a second, reserved-for-quiz male profile, on the
reasoning that both channels' explainers read in `mia` or `otis`, so a quiz in
either of those is the same show with a gimmick and a distinct reader is what
makes it register as a separate format. That reasoning was fine and it was
still wrong: on a full rendered cut the user's note was that the voice sounded
weird and had glitches. The quiz moved to `otis` — the male article reader for
both channels — on 2026-09-07, and the reserved profile was retired from the
roster rather than kept around unused. **Sounding like the channel beats
sounding distinct from it.** The format already reads as its own thing from
the cards and the countdown; it never needed the voice to carry that.

**No long form, for now.** The user's call. A twelve-question, four-minute quiz
is a real format and the engine would carry it, but the Short ships first and
earns it. `QuizShot`'s sizes scale with `frame.w`, so a 16:9 render *works* —
but the stack is portrait-shaped (a header over a 2x2 over a timer), and a
landscape version wants a different layout rather than the same one wider.

## The three phases

1. **Ask.** The question sets. The four cards arrive one at a time, each
   showing its letter — but the voice only reads the answer (see
   `LETTER_SPOKEN` below). Nothing is marked.
2. **Wait.** The narration stops for six seconds. A ring drains around a
   number and one clock tick lands per second, the last a fourth higher. This
   silence *is* the format. A quiz that answers itself immediately is a list.
3. **Reveal.** On the cut, the three wrong cards go red and dim together; a
   moment later the right one goes green, grows and takes a tick. The voice
   comes back with **"The correct answer is B."**, takes a beat, then reads
   the `answer` line — the *because* — over the marked cards. Naming the
   letter out loud is the format's job, not the writer's: `answer` carries
   the reason only, and `Question.answer_line` puts the letter on the card.

**The outro asks the question and stops.** "How many did you get?" — and
nothing after it. It carried "Tell me in the comments" and the user cut it:
a quiz that has just scored the viewer generates comments on its own, and
saying the ask out loud is the one line in the format that sounds like a
channel asking for engagement rather than a quiz ending.

## A question is seven shots, not one

It used to be one `QuizShot` per phase — the whole point of drawing a phase as
one object was that its timings could not drift apart. That held for *drawing*
and broke for *speaking*: the question and all four lettered options were one
sentence of five caption chunks, and `gap` (the only silence
`build_narration_aligned` knows how to give a script) is silence **between
sentences**, never inside one. A chunk gets nothing but the model's own
punctuation-length pause, which on the ENERGETIC chain is close to nothing —
one option ran straight into the next, and the user's own word for it was
"instantly following."

The fix is more sentences: the question, each card, and each half of the
reveal are separate one-chunk sentences in `quiz.build.render_quiz_short`,
each with its own scripted gap —

| gap | value | buys |
|---|---|---|
| `QUESTION_GAP` | 0.65s | a breath after the question, before the first card |
| `CARD_GAP` | 0.70s | between one card and the next |
| `ANSWER_LEAD_GAP` | 0.40s | after "The correct answer is B.", before the why |
| `NEXT_Q_GAP` | 1.00s | after the answer line, before the next question |
| `TITLE_GAP` / `INTRO_GAP` | 1.00s | after the title card, and after the intro |

— and `plan_shots` requires one `Shot` per sentence, so a question is seven
shots: the question, four cards, and the two halves of the reveal. **This does
not reopen the "one object, agreeing timings" problem.** Every one of the
seven is a `QuizShot` built from the *same* absolute `reveals`,
`countdown_at` and `mark_at`, computed once per question in
`render_quiz_short`'s `plan()` closure and copied onto all seven — a card's
draw condition is `t < due` against an absolute clock, so which shot happens
to be active when `t` crosses `due` is invisible in the output. Every
internal edge is a hard cut (`shot.xfade = 0.0`): a cut between two frames
computed identically at the boundary costs nothing and shows nothing, where a
cross-dissolve would render two nearly-identical frames to produce what a cut
gives for free.

**The countdown ring gets a lead-in and a tail, for the same reason.** The
ring used to start the instant the model's audio ended — arithmetically
correct, and it still read as the video cutting the last option off mid-word,
because there was no daylight between the last syllable and the timer
appearing. `LEAD` (0.25s) is silence *after* real speech before the ring
shows; `TAIL` (0.25s) is stillness *after* the ring's last tick before the cut
to the marked cards. Both are added to the requested silence on the last
card's answer gap (`LEAD + countdown + TAIL`), not carved out of the wait
itself — the ring still runs for exactly `countdown` seconds, it just no
longer starts on top of the word that was still finishing.

A `whoosh` cues the cut into every question, including the first one off the
intro card, placed `WHOOSH_LEAD` (0.70s) *ahead* of the question so it has
finished before the voice starts — on the shot start it swelled over the
question's first word. That is what `NEXT_Q_GAP` and `INTRO_GAP` are sized to
hold. See `audio.md`.

## The card's letter: eight attempts, and the one that stopped trying

**A card shows its letter but never speaks it.** The voice reads only the
answer — "It has no effect." — and the letter is left to the card itself and
to the reveal, which names it out loud as a real sentence: "The correct
answer is B." Getting to that was eight attempts, seven of which put a
spoken letter into a card's audio and tried to make it sound right next to
its answer. The history is worth keeping in full, because the eighth
attempt's whole premise is that the other seven were solving the wrong
problem.

**Attempt 1: isolate the letter as its own one-word sentence,** so
`run_break` guarantees a gap after it. It changes how the model says the
letter — an isolated letter's pitch *falls*, and no punctuation variant
escapes it:

| spoken alone | F0 start → end | duration |
|---|---|---|
| `"A."` | 134 → 124 Hz | 0.47s |
| `"A"` | 128 → 119 Hz | 0.45s |
| `"A,"` | 131 → 121 Hz | 0.51s |
| in context, before an answer | **131 → 139 Hz** | ~0.18-0.36s |

Sent back "weird," "unnatural," "very weird and glitchy."

**Attempt 2: keep the two in one sentence and force a splice between them**
(`chunk_pad`/`_force_pad`). Needs to find *where* to cut inside continuous
speech; `align_chunks`' DTW anchor was off by -0.06s to +0.14s with no
consistent direction, because a one- or two-character chunk is a hopeless DTW
reference. "Weird cut," "letters sound weird."

**Attempt 3: synthesise the letter in its real answer's context, then
discard the answer's audio.** Measured clean on every check available at the
time and came back "not spoken properly," "cut in the middle."

**Attempt 4: isolate the letter again, but trim it much harder.** Came back
in nearly Attempt 1's words: "lengthened," "glitchy." Trimming only touches
length; the defect was the falling contour, which no trim reaches.

**Attempt 5: splice a short silence into the combined read, gated to cards
where the gap is genuinely quiet.** The closest yet at the time, and the
first to ship without a click — but the gate rejected about half the cards
(every "C." among them), so half the video had a pause and half did not, and
the pause it could place was capped near 0.15s by how little room there was.

### A measurement that was wrong for two sessions

Attempts 3, 4 and 5 all rested on one number: *Kokoro rushes the letter to
55-90ms once it can see an answer coming.* It came from an energy search, and
it was false.

Align the **answer** against the combined read with DTW — a long,
acoustically rich reference, the case DTW is reliable for, rather than the
letter that made Attempt 2's anchor useless — and the answer's onset lands at
**180-360ms**, cross-checked by the fact that what remains after it matches
the answer synthesised alone to within 0.02-0.17s on all twelve cards of the
tinnitus script. The letter was never rushed. **The old search was firing on
the /s/ → /iː/ transition inside "C" itself, so every cut built on it sliced
the letter in half — which is exactly what "the letters sound cut in the
middle" was.** A wrong measurement, trusted because it was a measurement,
cost three attempts.

Correcting it is necessary but not sufficient: at the answer's *true* onset
the letter is often still at full energy — 98% of its own peak on "C. Loud
noise", where /iː/ glides into /l/ with no boundary of any kind. No search
fixes that, because nothing is there to find.

**Attempt 6: give the letter a throwaway carrier word through synthesis**
(`"Because."`), so it keeps its in-context length, and cut in the stop
closure of the carrier's opening plosive — a plosive needs a silence before
its burst, so there would be something safe to cut in. Shipped, and came back
*"we cut it with a 'b' sound."* `/b/` is a **voiced** plosive: its closure is
not silence at all but a voice bar, and the burst after it was plainly
audible. **Nothing may be added to what is spoken.**

### A second measurement that was wrong

Attempts 1 and 4 were both read as "the isolated letter's falling pitch
contour is the defect." Isolated letters do fall (134 → 124 Hz for `"A."`,
and every punctuation variant behaves the same — there is no trick spelling
that escapes it), but two attempts built on fixing the contour and both came
back in the same words as the attempt before. The per-run `loudnorm` was
also suspected of over-boosting a lone 0.4s letter, and measured innocent:
about 1 dB. Neither explained it.

**Attempt 7: add nothing, isolate nothing.** The card is synthesised as one
natural utterance — exactly the read that was approved before any pause
existed — and the silence is *inserted into it*: the answer's onset is found
by DTW **on the answer**, the cut backs off past any fricative belonging to
the answer (an /s/ or /f/ onset otherwise leaves a stray hiss before the
pause), the letter is kept with a 25ms fade, and the answer is re-taken from
its own synthesis so it always starts at its own natural onset. Measured
across all twelve cards: letter 0.156-0.357s (its natural in-context length),
a full **0.70s of true digital silence on every card**, worst-case seam
discontinuity 0.06.

**Sent back anyway** — *"the letter is said very quick so it sounds like
it's cut."* This is the finding that ended the search rather than refining
it further: a letter's natural, in-context spoken length genuinely is
0.15-0.36s — the number Attempt 7 correctly measured and correctly used —
and a syllable that short, spoken once and followed by silence, reads as
clipped regardless of how cleanly it is bounded. **A single letter does not
carry enough acoustic content to be its own spoken moment.** Every attempt
before this one had been chasing a synthesis problem; underneath all of them
was a structural one.

### Attempt 8, which ships: stop speaking the letter

The letter is shown on the card exactly as before — the countdown, the
reveal band, and the whole visual identity of the format depend on the
viewer reading it there — and is never sent to Kokoro as its own utterance.
`Question.option_line` still returns "B. It has no effect." as the *caption*;
the *spoken* half is only "It has no effect." `LETTER_SPOKEN = False` in
`quiz.build` is the flag, though there is no longer a code path that reads
it any other way — it exists to name the decision so a future session does
not reopen it without reading this history first.

The reveal is unaffected and was never part of the problem: "The correct
answer is B." is a real, multi-word sentence with its own natural contour,
never the isolated one-syllable case every attempt above was fighting.

`chunk_pad`/`_force_pad` in `core/voiceover.py` stay as general capability
for a case where the *kept* side of a cut is the one that matters — this
format has no cut to make inside continuous speech any more, for the letter
or anything else.

## A scripted gap under `RUN_BREAK_GAP` is a request, not a guarantee

**This is the trap, it cost two review rounds, and it is not specific to the
quiz format — every script in this repo is exposed to it.**

Splitting the ask into nine sentences was necessary and not sufficient. The
nine gaps were set to 0.15-0.45s and *none of them happened*. `gap` under
`RUN_BREAK_GAP` (1.00s) does not concatenate a silence; it asks `_pad_pause`
to insert silence into the pause the model already left at that boundary, and
`_pad_pause` needs to find a quiet stretch of at least `MIN_PAUSE` (0.12s)
below `PAUSE_FLOOR` to insert into. Where the model ran two sentences
together there is nothing to find, and **the gap is dropped without a word** —
no warning, no error, and a rendered file that sounds exactly like the one
before the fix.

Measured on the shipped render: a run that asked for 2.45s of internal gaps
received 0.00s of them.

Kokoro leaves no usable pause after a bare letter. This was checked rather
than assumed — `"A. It has no effect."`, `"A... It has no effect."`,
`"A, it has no effect."` and `"Option A. It has no effect."` were each
synthesised and scanned for quiet runs, and not one of them clears the floor.
The letter is absorbed into the phrase every time. **There is no punctuation
trick here; do not go looking for one again** — and per the section above,
the letter should not be pulled out to hang a silence off in any case.

So the quiz lowers the threshold instead. `render_crypto_short` takes a
`run_break` (defaulted to `RUN_BREAK_GAP`, so nothing else moves) and this
format passes `RUN_BREAK = 0.30`. Every gap at or above it ends the run, which
makes it a real silence file in the concat — it always happens. The cost is
that each item is synthesised without the one before it for context, the
cold-start prosody the run machinery exists to avoid. **For a quiz that is
correct rather than a regression:** four lettered options are a list of
discrete items, not a paragraph, and an item-by-item read is what the format
wants. Do not carry this setting into a prose format.

## The spoken half needs a full stop the card does not

An option is written `"It has no effect"` because a card does not carry a full
stop — and handing that string to the synthesiser is what cut the D option's
last words off. Without terminal punctuation Kokoro gives the utterance no
sentence-final fall, and `librosa.effects.trim(top_db=35)` in `_synth_raw`
then takes the end of the word with it. Measured on the same run text: the
audio ends at 0.047 RMS without the stop and 0.006 with it.

`Question._say` appends the stop to the **spoken** half only, so the card
still reads clean. It was reported twice as "it damages ... doesn't finish the
text" and both times the cause was this, not the countdown.

**The wrongs land together and the right one lands alone.** Staggering all four
makes the viewer read three verdicts before the one they came for, and the
payoff arrives fourth. The wrong cards are *dimmed towards the background*
rather than filled red — three red cards next to one green one is a traffic
light, and the eye goes to the red because there is more of it.

## Every video opens on a title card, and it carries no number

`render_quiz_short(..., title=(caption, spoken))` — a `ChapterCard` before the
first question: "Tinnitus Quiz: Myths Edition" and so on, one per channel.
There is no second card after it either — the first video carried a stake
card ("Three tinnitus myths. Most people believe at least one.") between the
title and the first question, and the user cut it (2026-09-08) as redundant
with the title alone.

**A numbered version shipped first and was cut on the same call.** The beat
supports it — `title_number` still exists, drawing a large numeral above the
title via `ChapterCard`'s own numbered mode ("a script that is genuinely
counting something the narration also counts out loud") — but the user asked
for the plain, un-numbered template instead. Leave `title_number` unset unless
a later run is explicitly asked to bring it back.

**If it ever comes back, never write the number into the caption text as
`#1`.** Checked, not assumed: Kokoro reads a bare `#1` as "hash one." The
number belongs in the numeral (`title_number`) and, if a sentence should say
it, spelled out in the *spoken* half of `title` — never in the caption.

## Cards carry type, not photographs

Considered and settled: four stock images per question is twelve to twenty
licensed images a video, most answers have no photographable subject at all
("the exchange owes it to you"), and a photograph big enough to read at phone
size leaves no room for the words that say what it is. A card is a letter chip,
a rule and an answer.

**Three lines an option, three lines a question.** `render_quiz_short` measures
every one with the real font at the real width and raises before anything
renders. Clipping quietly would put a *wrong answer on screen*, and a truncated
D option is exactly the fault that survives review because the reviewer already
knows what it says.

## No thumbnail render

Every article explainer calls `render_short_thumb` with a site photo or, at
worst, a headline card. A quiz project script does neither, on the user's
call (2026-09-08): the video's own picture is already four drawn cards, and a
generated headline plate would just restate the hook a viewer is about to see
anyway in the first two seconds. The Reel cover comes from a frame pulled out
of the finished render at publish time instead — see
`docs/publish/instagram-facebook.md`. A Short gets no thumbnail from the
YouTube API regardless of format, and TikTok's draft cover is always set by
hand, so the only real consumer of a generated thumbnail file was ever the
Instagram/Facebook Reel cover — which a video frame serves just as well.

## The safe box is the layout

The vertical frame gives this beat y=230 to y=1440, and the watermark takes the
top of it — about 1040 usable pixels for a three-line question, four cards and
a timer. The first layout used 320px cards on an 880px grid line, looked
correct in isolation, and put the bottom row and the entire countdown ring
under the Shorts title block: invisible in the app, perfectly visible in
review. The ring is bounds-checked against `frame.safe_bottom` on every frame
for that reason. Do not move the grid down to give the question more room —
shorten the question.

## Sound

`clock` and `clock_final` were added to `core/sfx.py` for this. The tick is
nearly all transient, with only enough body to have a body: `mark_cross`'s
recipe has a 196 Hz *note* in it, and eight of the same note in a row reads as
music the bed is out of tune with. The last tick is a fourth up so the
countdown has a full stop and the reveal does not have to also announce that
time is up.

The cues come from `QuizShot.cues()` — the same two numbers the ring is drawn
from — so the clock in the mix cannot drift from the ring on screen.

## The line that outranks everything else

**The channel's own rule still governs, and a quiz makes it easier to break.**

On crypto: `projects/crypto.md` in full, and no financial advice ever. A
question may not have a direction as an answer. "Which of these is the safest
place to keep your coins?" is a recommendation wearing a question mark, and so
is any option that names a platform as the right one. Ask about *mechanism* —
what custody means, what a validator does, what a chain cannot do.

On tinnitus: `projects/tinnitus.md` in full. Nothing diagnoses and nothing
promises relief, and a quiz format is one careless option away from both. "What
cures tinnitus?" has no correct card and must not be asked. "Which of these is
a myth?" is the safe shape, and the `answer` line still may not tell anyone
what to do about their own ears. **No ear close-ups** stands here as everywhere.

**A wrong option must be wrong for a reason the article gives.** An invented
distractor is a claim: a viewer who reads "too much earwax" as option B and
watches it go red has been told earwax does not cause tinnitus, whether or not
the script ever said so. If the post does not support the correction, do not
put the option on a card.
