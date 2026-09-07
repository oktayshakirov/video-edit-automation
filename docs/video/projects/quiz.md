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
| Length | ~75s. Three questions. |
| Format | 9:16 only. There is no long form — see below. |
| Voice | **`otis`** (bare `am_puck`, ENERGETIC chain). |
| Beat | `quiz.cards.QuizShot`, drawn across seven shots per question — see below. |
| Source | one article, `SOURCE_POST` set like every other project script. |

**Three questions, not five.** A question costs about twenty-five seconds —
two to ask, eight to read four cards with real pauses between them, eight to
wait, five to reveal and explain — so five questions is over two minutes.

**The original estimate was 60s and the format lands at ~75s.** That is the
cost of the pauses being real, and it was the user's call once the first two
cuts came back as "read all together". The only silence this engine can give
a script is a scripted gap between two sentences, and each one is paid for in
runtime; nothing recovers that time without cutting a pause back to
inaudible. **The countdown is the largest single line in the budget** — three
times `countdown`, so 24s of the 75 — and it is the first thing to trade if a
run has to come down. Trade it before trading the pauses.

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

1. **Ask.** The question sets. The four cards arrive one at a time, each as
   its own line is read. Nothing is marked.
2. **Wait.** The narration stops for eight seconds. A ring drains around a
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

There is no engine knob that buys a pause *inside* a sentence. The only fix
that is real is more sentences: the question, each card, and each half of the
reveal are separate one-chunk sentences in `quiz.build.render_quiz_short`,
each with its own scripted gap —

| gap | value | buys |
|---|---|---|
| `QUESTION_GAP` | 0.65s | a breath after the question, before the first card |
| `CARD_GAP` | 0.70s | between one card and the next |
| `ANSWER_LEAD_GAP` | 0.40s | after "The correct answer is B.", before the why |
| `NEXT_Q_GAP` | 1.00s | after the answer line, before the next question |

— and `plan_shots` requires one `Shot` per sentence, so a question is seven
shots: the question, the four cards, and the two halves of the reveal.
**This does not reopen the "one object, agreeing timings" problem.**
Every one of the seven is a `QuizShot` built from the *same* absolute
`reveals`, `countdown_at` and `mark_at`, computed once per question in
`render_quiz_short`'s `plan()` closure and copied onto all seven — a card's
draw condition is `t < due` against an absolute clock, so which of the seven
shots happens to be active when `t` crosses `due` is invisible in the output.
Every internal edge is a hard cut (`shot.xfade = 0.0`): a cut between two
frames that are computed identically at the boundary costs nothing and shows
nothing, where a cross-dissolve would render two nearly-identical frames to
produce what a cut gives for free.

**The countdown ring gets a lead-in and a tail, for the same reason.** The
ring used to start the instant the model's audio ended — arithmetically
correct, and it still read as the video cutting the last option off mid-word,
because there was no daylight between the last syllable and the timer
appearing. `LEAD` (0.25s) is silence *after* real speech before the ring
shows; `TAIL` (0.25s) is stillness *after* the ring's last tick before the cut
to the marked cards. Both are added to the requested silence on the last
option's gap (`LEAD + countdown + TAIL`), not carved out of the eight-second
wait itself — the ring still runs for exactly `countdown` seconds, it just no
longer starts on top of the word that was still finishing.

A `whoosh` cues the cut into every question, including the first one off the
intro card, placed `WHOOSH_LEAD` (0.70s) *ahead* of the question so it has
finished before the voice starts — on the shot start it swelled over the
question's first word. That is what `NEXT_Q_GAP` and `INTRO_GAP` are sized to
hold. See `audio.md`.

## A letter is never spoken on its own

**Measured, and it overturned the previous design.** The build that isolated
the letter — "A." as its own one-word run, so a guaranteed silence could
follow it — came back as the letters sounding weird and the voice unnatural.
The pitch track says exactly why. Inside "A. It has no effect." the letter
runs **137 Hz → 208 Hz**: a rising list-item contour that *leads into* the
answer. Synthesised alone it is flat and half again as long —

| spoken alone | F0 start → end | duration |
|---|---|---|
| `"A."` | 127 → 127 Hz | 0.55s |
| `"A,"` | 120 → 120 Hz | 0.60s |
| `"A?"` | 125 → 128 Hz | 0.55s |
| `"A"` | 116 → 143 Hz | 0.51s |
| in context | **137 → 208 Hz** | ~0.35s |

Flat and drawn out is the sound being complained about, and no punctuation
recovers the rise.

**So this is a genuine either/or, not a tuning problem.** The letter's
naturalness *consists of* it leading into its own answer, so any silence
inserted after it removes the thing that makes it sound right. A break after
the letter and a natural-sounding letter cannot both exist on this
synthesiser. The letter travels with its option as one utterance, and the
pauses live between cards, where they cost nothing. Do not split them again.

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
