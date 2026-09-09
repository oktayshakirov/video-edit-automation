---
name: video-quiz
description: Build a vertical quiz Short for either channel - three questions from one article, four answer cards each, a timed countdown and a marked reveal. Use when the user runs /video-quiz, asks for a quiz video, a trivia Short, or a "how much do you know about X" piece for thecrypto.wiki or tinnitushelp.me. Builds only; publishing is /publish-video. For article explainers use video-crypto or video-tinnitus, for drone footage use video-drone.
---

# Quiz videos

**One article, three questions, about 95 seconds.** The same format on both
channels - `/video-quiz crypto` and `/video-quiz tinnitus` - because the only
things that differ are a `Brand` and the safety rules.

A quiz short is not an explainer with a question mark on it. The explainers buy
their thirty seconds with a picture; this one buys them by making the viewer
commit to an answer, which is a stronger hook and a much less forgiving one.

**Repo:** `~/Coding/video-edit-automation`. Run Python from there with
`PYTHONPATH=.`. **Source sites:** `~/Coding/crypto-wiki`,
`~/Coding/tinnitus-blog`.

## Read these, in this order

The steps live in `docs/video/workflow.md` - read it first, every run. Then:

| Step | Read |
| --- | --- |
| Before anything | `docs/video/projects/quiz.md` - the format, the phases, the layout, the limits |
| Before writing a word | `docs/video/narration.md`, and the channel's own page - `projects/crypto.md` or `projects/tinnitus.md` |
| How the synthesiser behaves | `docs/video/voice.md` |
| Shorts pacing and titles | `docs/video/shorts.md` |
| Type and layout on screen | `docs/video/design.md` |
| Music and sound | `docs/video/audio.md` |
| Something rendered wrong | `docs/video/troubleshooting.md` |

Do not work from memory of these rules. They are edited as the engine changes,
and a remembered version is a stale one.

## The run

1. **Suggest, do not pick.** `python3 tools/topics.py crypto --quiz` (or
   `tinnitus --quiz`). **This is not the explainer list and the difference
   matters**: an article that already has a long form and a Short is the
   *best* quiz source, not a used-up one, because the audience has been taught
   the thing they are about to be tested on. Offer three to five candidates
   with a reason each - what the four options would be, and which misconception
   the article corrects - then stop and wait.
2. **Write the questions.** Three of them, each a `Question`: the question,
   four options, the index of the right one, and `answer` — the *because*
   only, never "the answer is B." The format itself says the letter
   ("The correct answer is B.", a beat, then `answer`); do not put a letter in
   the text you write. The wrong options come from the article, never from
   invention.
3. **Build** - `projects/quiz-crypto/<name>.py` or
   `projects/quiz-tinnitus/<name>.py`, calling
   `video_automation.quiz.build.render_quiz_short` and setting `SOURCE_POST`.
   - **Open on a plain title card.** `title=(caption, spoken)` — "Tinnitus
     Quiz: Myths Edition" and so on. **No number, and no second intro card
     after it** — both were tried and cut on the user's call (2026-09-08): the
     number as an unnecessary flourish, a second stake-setting card as
     redundant with the title. `title_number` and `intro` both still exist as
     parameters if a later run is explicitly asked to bring either back, but
     do not add them by default.
   - **No thumbnail render.** Every other format calls `render_short_thumb`
     because it has a site photo or a headline worth a dedicated card; a quiz
     has neither — the picture *is* the four cards, and a frame pulled from the
     finished video already shows the hook (the question, or the countdown) in
     a way a generated headline card would just repeat. `/publish-video` pulls
     the cover frame from the render itself for this format; do not add a
     `render_short_thumb` call to a quiz project script.
4. **Hand over and wait.** Re-cut as many times as the user asks; that loop is
   the normal case.
5. **On approval: commit, write `HANDOFF-PUBLISH.md`, and tell the user to open
   a fresh session for `/publish-video`.**

## Five things that are settled, and are not to be re-litigated per run

- **Three questions, not five.** A question costs ~30s once its pauses are
  real (see `quiz.md`). Five would run past two and a half minutes. The user
  chose three with that arithmetic in front of them; the countdown is what
  gives way first if a cut needs to come back down, not the pauses.
- **Cards carry type, not photographs.** Four stock images a question is
  twelve to twenty licensed images a video, and most answers have no
  photographable subject.
- **The voice is `otis`**, the male article reader for both channels - same
  voice, same reason a quiz sounds like it belongs to the channel rather than
  like a different show.
- **The outro asks the question and stops** - "How many did you get?", no
  "tell me in the comments." A quiz that has just scored the viewer generates
  comments on its own.
- **A card is read "B." - a real 0.70s silence - "It has no effect.", and
  that pause took six attempts.** The letter and the answer are synthesised
  separately and joined around real silence (`synth_letter_then_answer` in
  `core/voiceover.py`), so nothing ever has to find a boundary inside
  continuous speech. The letter gets a throwaway carrier word through
  synthesis so the model still gives it in-context length and contour, and the
  carrier starts with a plosive whose stop closure is a genuine silence to cut
  in. Five earlier attempts shipped and were sent back: isolated letter
  (twice - it reads with a falling contour, and no trim reaches that), forced
  splice mid-sentence, in-context-then-discarded, and a gated short splice
  that only reached half the cards. **Three of those rested on a measurement
  that was simply wrong** - "Kokoro rushes the letter to 55-90ms" came from an
  energy search firing on the /s/ to /iː/ transition inside "C" itself; the
  letter actually occupies 180-360ms. See `LETTER_ANSWER_GAP` in `quiz.build`
  for the full account. Do not re-derive any of this from scratch, and do not
  change `LETTER_CARRIER` without re-measuring letter length, cut energy and
  contour across all four letters.

## What makes a question work

- **Answerable by someone who does not know.** Four plausible options. If three
  can be eliminated by reading them, nothing has been asked.
- **The wrong answers are the content.** Each is a misconception the article
  actually corrects. A distractor the post does not support is a *claim*: a
  viewer who watches "too much earwax" go red has been told earwax does not
  cause tinnitus whether or not the script said so.
- **The `answer` line is the *because*, never "the answer is B."** It is the
  only place the article's substance lands, and it is what stops a viewer who
  got it wrong from feeling caught out.

## This skill does not publish

Everything about getting a render out - which file goes to which platform, the
metadata pass, the site registry entry, the social posts and their order - is
`/publish-video`'s, and it is the only copy. That sequence used to be
duplicated into every build skill; the copies drifted and cost a registry entry
that had to be reverted and a social post that could not be un-sent.

Do not describe upload steps, pre-empt them, or re-derive them from memory.

## The line that outranks everything else

**The channel's own rule governs, and this format is one careless option away
from breaking it.**

On **crypto**: no financial advice, ever. An answer may not be a direction.
"Which of these is the safest place to keep your coins?" is a recommendation
wearing a question mark, and so is any option that names a platform as the
right one. Ask about mechanism.

On **tinnitus**: nothing diagnoses and nothing promises relief. "What cures
tinnitus?" has no correct card and must not be asked; "which of these is a
myth?" is the safe shape. **No ear close-ups.**

The full statements are in `docs/video/projects/crypto.md` and
`docs/video/projects/tinnitus.md`. Read the one for the channel before writing,
not after a re-cut.
