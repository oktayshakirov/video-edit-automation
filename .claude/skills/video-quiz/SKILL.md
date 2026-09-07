---
name: video-quiz
description: Build a vertical quiz Short for either channel - three questions from one article, four answer cards each, a timed countdown and a marked reveal. Use when the user runs /video-quiz, asks for a quiz video, a trivia Short, or a "how much do you know about X" piece for thecrypto.wiki or tinnitushelp.me. Builds only; publishing is /publish-video. For article explainers use video-crypto or video-tinnitus, for drone footage use video-drone.
---

# Quiz videos

**One article, three questions, about 75 seconds.** The same format on both
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
| The thumbnail | `docs/video/thumbnails.md` |
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
4. **Hand over and wait.** Re-cut as many times as the user asks; that loop is
   the normal case.
5. **On approval: commit, write `HANDOFF-PUBLISH.md`, and tell the user to open
   a fresh session for `/publish-video`.**

## Three things that are settled, and are not to be re-litigated per run

- **Three questions, not five.** A question costs ~25s once its pauses are
  real (see `quiz.md`). Five would run past two minutes. The user chose three
  with that arithmetic in front of them; the countdown is what gives way first
  if a cut needs to come back down, not the pauses.
- **Cards carry type, not photographs.** Four stock images a question is
  twelve to twenty licensed images a video, and most answers have no
  photographable subject.
- **The voice is `otis`**, the male article reader for both channels - same
  voice, same reason a quiz sounds like it belongs to the channel rather than
  like a different show.
- **The outro asks the question and stops** - "How many did you get?", no
  "tell me in the comments." A quiz that has just scored the viewer generates
  comments on its own.

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
